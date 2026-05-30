# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-05-30T07:07:49.087Z

## Original task

请审查 docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md 中提出的技术方案，重点评估：1) Mock+接口抽象方案的合理性 2) 风险识别和缓解措施 3) 10周+3天工期评估 4) 架构设计完善性。请提供详细的审查意见、风险评估和改进建议。

## Final prompt

请审查 docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md 中提出的技术方案，重点评估：1) Mock+接口抽象方案的合理性 2) 风险识别和缓解措施 3) 10周+3天工期评估 4) 架构设计完善性。请提供详细的审查意见、风险评估和改进建议。

## Raw output

```text
**结论**

Mock + 接口抽象方向是合理的，但当前方案不能按原文直接通过。评分：**7/10**。核心问题不是“能不能 Mock”，而是方案把“用户主数据 API 化”当成默认终局，偏离了此前已达成的首版共识：学生、辅导员、班级映射应优先走 CSV/Excel 导入，宿舍清退才是实时 API。现有共识明确写了学生/辅导员/班级映射首版 CSV，宿舍清退 API 实时查询：[31-data-source-requirements-consensus-v2.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:35)、[数据对接说明文档.md](/home/caohui/projects/graduation-leave-system/docs/数据对接说明文档.md:24)。

**主要问题**

P0：`RealUserDataProvider` 不应成为认证、审批、班级映射的运行时依赖。用户、辅导员、班级映射是本系统的基础主数据，影响登录、权限、审批人分配和历史追溯。应落入本地数据库，通过 CSV/API Provider 输入到 staging，再校验、upsert、软停用。此前设计已经定义了 staging + upsert + 软停用、导入审计和校验报告：[31-data-source-requirements-consensus-v2.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:282)。如果直接在业务中查询 Provider，会引入外部 API 可用性、分页、延迟、字段缺失、历史变更不可追溯等风险。

P0：`+3天生产就绪` 评估过于乐观。3天只适用于“API 契约已冻结、测试环境可用、认证已跑通、字段完全覆盖、只写一个薄适配器”的场景。但当前文档明确缺少完整 API 文档、认证信息、字段映射和交付时间：[37-api-blocking-solution-review-request.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:25)。在这种条件下，真实集成应预留 **1-2周**；如果坚持把用户主数据也 API 化，应预留 **2-4周**，因为会牵涉数据模型、导入/同步策略、账号状态、审批人映射和验收演练。

P1：接口设计粒度不够。`get_students(filters) -> List[Student]`、`get_counselors()`、`get_class_mapping() -> Dict[str, str]` 太粗，缺少分页、增量同步、源数据更新时间、数据质量报告、批次标识、字段映射版本、错误分类和健康检查。建议拆成：
- `StudentSourceProvider` / `CounselorSourceProvider` / `ClassMappingSourceProvider`
- `DormCheckoutProvider`
- `ProviderHealthCheck`
- `ImportAdapter` 或 `SyncService`

返回值应是 DTO，不是 Django ORM Model。Provider 负责“取数和标准化”，Import/Sync 层负责“校验、落库、审计、软停用”。

P1：`USE_MOCK_DATA` 太粗且有生产风险。当前设计用一个开关同时切用户数据和宿舍清退：[37-api-blocking-solution-review-request.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:160)。应改为细粒度配置：
- `USER_DATA_SOURCE=seed|csv|api`
- `DORM_CHECKOUT_SOURCE=mock|api|csv`
- `WECHAT_PROVIDER=mock|real`
- 生产环境禁止 `mock`，启动时 system check 直接失败
- 支持“用户主数据 CSV + 宿舍清退 API”的混合模式

P1：Mock 数据真实性不足。100学生、10辅导员可以支撑演示，但不足以覆盖风险。必须包含边界样本：无班级映射、辅导员停用、重复 class_id、多辅导员、延期毕业/非毕业生、姓名不一致、宿舍状态 `completed/pending/not_started/unknown`、API 404/401/429/500、超时、数据过期。宿舍清退枚举和降级规则已有定义：[数据对接说明文档.md](/home/caohui/projects/graduation-leave-system/docs/数据对接说明文档.md:306)。

**工期评估**

10周做“Mock/Seed 数据可演示版本”基本可行，但 Week 7 才做接口抽象偏晚。Provider 契约、DTO、种子数据、导入接口应在 Week 1-2 完成，否则认证、审批、前端都会先绑定临时模型，后续返工。

建议调整为：
- Week 1：数据契约、DTO、Provider 接口、种子数据、导入模型
- Week 2-3：CSV/staging/upsert/审计和核心账号数据
- Week 3-6：申请、审批、附件、通知
- Week 6-7：宿舍清退 Provider、降级流程、缓存、错误分类
- Week 8-9：前端
- Week 10：联调、演示、验收清单
- API 到位后：宿舍清退 API 1周；用户主数据 API 替换 CSV 另计 2-4周

因此，“10周 + 3天”建议改成：**10周演示版 + 1-2周生产集成缓冲**。若外部 API 字段继续缺失，首版应坚持 CSV/Excel 主数据导入，不等待 API。

**架构建议**

推荐架构是“反腐层 + 本地主数据”：

1. 外部数据源：CSV/API/DB view/Mock。
2. Provider：只负责读取外部数据并转换为标准 DTO。
3. Import/Sync Service：校验必填字段、唯一性、班级覆盖率、辅导员有效性。
4. 本地数据库：作为认证、权限、审批和历史记录的唯一运行时依据。
5. DormCheckoutProvider：运行时查询，可缓存，可降级到人工证明。

缓存方面，用户信息可按现有设计 30分钟左右缓存：[2026-05-27-system-design.md](/home/caohui/projects/graduation-leave-system/docs/design/2026-05-27-system-design.md:2433)。宿舍清退状态建议：
- `completed` 可缓存 10-30分钟；
- `pending/not_started` 缓存 1-5分钟；
- `unknown/error` 只短缓存 30-60秒，避免故障恢复后仍误判；
- 提交申请前必须重新校验或记录“校验时间 + source_updated_at”。

错误处理要区分：认证失败、字段缺失、学生不存在、限流、超时、服务不可用、数据不一致。现有设计已有重试和降级方向：[2026-05-27-system-design.md](/home/caohui/projects/graduation-leave-system/docs/design/2026-05-27-system-design.md:1697)，但需要补充监控指标：成功率、P95延迟、降级次数、unknown 比例、认证失败次数、429 次数。

**最终建议**

当前方案可作为开发解阻方案，但要改成：**“Seed/Mock + Provider 抽象 + CSV 主数据导入 + 宿舍清退 API 适配”**。不要把用户主数据 API 集成放到首版关键路径，也不要承诺 API 到位后三天生产就绪。真正的关键交付物应是稳定的数据契约、导入校验、降级流程、契约测试和上线验收清单。


Reading additional input from stdin...
OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019e77b2-c826-7cb1-a381-14feffb764be
--------
user
请审查 docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md 中提出的技术方案，重点评估：1) Mock+接口抽象方案的合理性 2) 风险识别和缓解措施 3) 10周+3天工期评估 4) 架构设计完善性。请提供详细的审查意见、风险评估和改进建议。
codex
我会先读取项目约束和评审请求文档，再对照仓库结构验证方案假设，最后给出按问题优先级组织的审查意见。
exec
/bin/bash -lc "sed -n '1,260p' docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# API阻塞问题解决方案 - Codex审查请求

**文档编号：** 37  
**创建日期：** 2026-05-30  
**审查类型：** 技术方案设计  
**优先级：** P0（阻塞开发进度）

---

## 一、背景说明

### 1.1 当前状况

**项目状态：**
- 设计阶段完成（3轮Codex审查通过）
- 准备开始Phase 1实施
- 遇到外部依赖阻塞

**阻塞原因：**
- 原设计采用CSV导入用户数据（学生、辅导员、班级）
- 现决定改用API对接方式
- 宿舍管理系统只提供了一个第三方API文档（goliveplus租户用户查询API）
- 该API字段不满足需求（缺少班级、院系、专业、宿舍清退状态等）

**缺失信息：**
1. 完整的API文档（学生信息、辅导员信息、宿舍清退状态）
2. API认证信息（appKey、appSecret、签名算法）
3. 数据字段映射关系
4. API提供时间不确定

### 1.2 核心问题

**如何在外部API信息缺失的情况下，避免开发进度被阻塞？**

---

## 二、Claude分析结果

### 2.1 依赖分析

**完全不依赖外部API（80%工作量）：**
- Phase 1: 项目初始化（Django、Docker、Celery）
- Phase 2: 用户认证模块（可用Mock数据）
- Phase 3: 离校申请模块
- Phase 4: 审批管理模块
- Phase 5: 附件管理模块
- Phase 6: 通知模块（可Mock微信）
- Phase 8: 前端开发（可用测试AppID）
- Phase 9: 测试（可用Mock数据）

**完全依赖外部API（20%工作量）：**
- Phase 7: 外部系统集成模块

### 2.2 推荐方案

**Mock + 接口抽象 + 种子数据混合方案**

**核心设计：**

```python
# 1. 定义抽象接口
class IUserDataProvider(ABC):
    """用户数据提供者接口"""
    @abstractmethod
    def get_students(self, filters: Dict) -> List[Student]:
        """获取学生列表"""
        pass
    
    @abstractmethod
    def get_counselors(self) -> List[Counselor]:
        """获取辅导员列表"""
        pass
    
    @abstractmethod
    def get_class_mapping(self) -> Dict[str, str]:
        """获取班级-辅导员映射"""
        pass

class IDormCheckoutProvider(ABC):
    """宿舍清退状态提供者接口"""
    @abstractmethod
    def check_status(self, student_id: str) -> CheckoutStatus:
        """查询学生宿舍清退状态"""
        pass
    
    @abstractmethod
    def batch_check_status(self, student_ids: List[str]) -> Dict[str, CheckoutStatus]:
        """批量查询清退状态"""
        pass

# 2. Mock实现（开发阶段使用）
class MockUserDataProvider(IUserDataProvider):
    def get_students(self, filters):
        # 返回预定义的测试数据
        return [
            Student(
                student_id="2020001",
                name="张三",
                department="计算机学院",
                major="计算机科学与技术",
                class_id="CS2020-01",
                grade=2020,
                graduation_year=2024,
                is_graduating=True
            ),
            # ... 更多测试数据
        ]
    
    def get_counselors(self):
        return [
            Counselor(
                employee_id="T001",
                name="李老师",
                managed_classes=["CS2020-01", "CS2020-02"]
            ),
            # ... 更多测试数据
        ]

class MockDormCheckoutProvider(IDormCheckoutProvider):
    def check_status(self, student_id: str):
        # 模拟查询逻辑
        return CheckoutStatus(
            student_id=student_id,
            is_checked_out=True,
            checkout_date="2024-06-15",
            dorm_building="1号楼",
            dorm_room="101"
        )

# 3. 真实实现（API信息到位后实现）
class RealUserDataProvider(IUserDataProvider):
    def __init__(self, api_config: APIConfig):
        self.api_url = api_config.url
        self.app_key = api_config.app_key
        self.app_secret = api_config.app_secret
    
    def get_students(self, filters):
        # 调用真实API
        sign = self._generate_sign()
        response = requests.post(
            self.api_url,
            headers={
                'appKey': self.app_key,
                'timestamp': str(int(time.time())),
                'sign': sign
            },
            data=filters
        )
        # 解析响应并映射到内部数据模型
        return self._parse_students(response.json())
    
    def _generate_sign(self):
        # 实现签名算法（待API文档提供）
        pass
    
    def _parse_students(self, api_data):
        # 将API数据映射到内部Student模型
        pass

# 4. 配置切换
def get_user_data_provider() -> IUserDataProvider:
    if settings.USE_MOCK_DATA:
        return MockUserDataProvider()
    else:
        return RealUserDataProvider(settings.API_CONFIG)

def get_dorm_checkout_provider() -> IDormCheckoutProvider:
    if settings.USE_MOCK_DATA:
        return MockDormCheckoutProvider()
    else:
        return RealDormCheckoutProvider(settings.API_CONFIG)
```

**配置文件：**

```python
# settings/base.py
USE_MOCK_DATA = env.bool('USE_MOCK_DATA', default=True)

# settings/dev.py
USE_MOCK_DATA = True  # 开发环境使用Mock

# settings/prod.py
USE_MOCK_DATA = False  # 生产环境使用真实API
API_CONFIG = {
    'url': env.str('EXTERNAL_API_URL'),
    'app_key': env.str('EXTERNAL_API_KEY'),
    'app_secret': env.str('EXTERNAL_API_SECRET'),
}
```

### 2.3 实施计划

**阶段1：不等API（10周）**

| 周次 | 任务 | 交付物 |
|------|------|--------|
| Week 1-2 | 基础设施 + Mock数据 | Django项目、种子数据（100学生、10辅导员） |
| Week 3-6 | 核心业务逻辑 | 申请、审批、附件、通知模块 |
| Week 7 | 接口抽象层 | Provider接口、MockProvider、缓存框架 |
| Week 8-9 | 前端开发 | React Native、微信小程序（测试AppID） |
| Week 10 | 测试 | 单元测试、集成测试（Mock数据） |

**交付物：** 可演示版本（使用Mock数据，功能完整）

**阶段2：API到位后（+3天）**

| 天数 | 任务 | 交付物 |
|------|------|--------|
| Day 1-2 | 实现真实Provider | RealUserDataProvider、RealDormCheckoutProvider |
| Day 3 | 集成测试 | 真实API测试、数据验证 |

**交付物：** 生产就绪版本

### 2.4 优势分析

**技术优势：**
1. **解耦设计** - 业务逻辑不依赖具体数据源
2. **易于测试** - Mock数据可控，测试稳定
3. **快速迭代** - 不等外部依赖，开发不阻塞
4. **低风险切换** - 配置开关，无需改代码
5. **符合SOLID** - 依赖倒置原则，面向接口编程

**项目管理优势：**
1. **进度可控** - 80%工作不受阻塞
2. **分阶段交付** - 10周可交付演示版
3. **风险隔离** - API问题不影响核心功能
4. **灵活应对** - API延期也不影响整体进度

### 2.5 风险评估

**低风险：**
- 真实API字段与Mock不一致 → 调整适配器即可（1-2天）
- 真实API性能问题 → 已有缓存和重试机制

**中风险：**
- 真实API数据结构差异大 → 可能需要调整数据模型（2-3天）
- API认证复杂度超预期 → 可能需要额外调试时间（1-2天）

**缓解措施：**
1. 接口设计参考行业标准（RESTful、OAuth2等）
2. 预留扩展字段，避免硬编码
3. 完善的错误处理和日志记录
4. 充分的单元测试覆盖

---

## 三、请Codex审查的问题

### 3.1 技术方案合理性

**问题1：Mock + 接口抽象方案是否合理？**
- 这种设计是否符合最佳实践？
- 是否有更好的解耦方案？
- 接口定义是否完善？

**问题2：Provider接口设计是否合理？**
- `IUserDataProvider` 和 `IDormCheckoutProvider` 接口是否完整？
- 是否需要增加其他方法？
- 方法签名是否合理？

exec
/bin/bash -lc "sed -n '1,220p' /home/caohui/.codex/RTK.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# RTK - Rust Token Killer (Codex CLI)

**Usage**: Token-optimized CLI proxy for shell commands.

## Rule

Always prefix shell commands with `rtk`.

Examples:

```bash
rtk git status
rtk cargo test
rtk npm run build
rtk pytest -q
```

## Meta Commands

```bash
rtk gain            # Token savings analytics
rtk gain --history  # Recent command savings history
rtk proxy <cmd>     # Run raw command without filtering
```

## Verification

```bash
rtk --version
rtk gain
which rtk
```

exec
/bin/bash -lc 'rg --files' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
CLAUDE.md
docs/templates/宿舍清退数据模板.csv
docs/templates/学生基本信息导入模板.csv
docs/templates/班级辅导员对应关系导入模板.csv
docs/templates/辅导员基本信息导入模板.csv
docs/微信小程序申请说明.md
docs/数据确认清单.md
docs/superpowers/plans/2026-05-27-implementation-plan.md
毕业离校系统用户文档.zip
docs/数据对接说明文档.md
docs/微信小程序备案说明.md
docs/Codex审查流程指南.md
docs/用户设计说明书.md
docs/PROJECT-SUMMARY.md
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md
docs/design/2026-05-27-system-design.md
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md
docs/discussions/codex-review-2026-05-27/02-architecture-response.md
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md
docs/discussions/codex-review-2026-05-27/04-database-review.md
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md
docs/discussions/codex-review-2026-05-27/01-architecture-review.md
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md
docs/discussions/codex-review-2026-05-27/21-final-consensus.md
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md
backend/requirements/base.txt
backend/requirements/dev.txt
backend/requirements/prod.txt

codex
文档里方案本身已经很明确；我接下来会读系统设计和此前的数据源共识，确认这个“API替代CSV”的变化会影响哪些已定模型和流程。
exec
/bin/bash -lc "rtk sed -n '1,240p' docs/数据对接说明文档.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 毕业生离校申请审批系统 - 数据对接说明文档

**文档版本：** v2.0  
**发布日期：** 2026-05-27  
**目标用户：** 宿舍管理系统管理员、数据对接负责人

---

## 一、对接概述

### 1.1 对接目的

本系统需要与学校现有的**宿舍管理系统**进行数据对接，获取以下数据：

1. **学生基本信息** - 创建学生账号，用于登录和身份识别
2. **辅导员基本信息** - 创建辅导员账号，用于审批管理
3. **班级-辅导员对应关系** - 自动分配审批人
4. **宿舍清退数据** - 验证学生是否完成宿舍清退

### 1.2 对接方式

本系统支持两种对接方式：

| 数据源 | 对接方式 | 说明 |
|--------|---------|------|
| 学生基本信息 | **CSV/Excel文件导入** | 首版推荐，快速上线 |
| 辅导员基本信息 | **CSV/Excel文件导入** | 首版推荐，快速上线 |
| 班级-辅导员对应关系 | **CSV/Excel文件导入** | 首版推荐，需强校验 |
| 宿舍清退数据 | **API接口实时查询** | 需要实时验证清退状态 |

**为什么推荐CSV/Excel导入？**
- 实施周期短：无需开发API，1-2周即可上线
- 风险可控：可以先验证、再导入、可回滚
- 变更频率低：学生和辅导员信息每学期更新1-2次
- 后续可升级：如果数据变更频繁，可升级为API/数据库同步

### 1.3 对接时间表

| 阶段 | 时间 | 任务 |
|------|------|------|
| 数据确认 | 第1周 | 确认数据可用性、字段定义、CSV模板 |
| CSV导入开发 | 第2-3周 | 开发CSV导入功能、校验逻辑、审计日志 |
| 宿舍清退API对接 | 第4周 | 对接宿舍清退API、测试异常场景 |
| 上线验收 | 第5周 | 全量导入演练、功能测试、正式上线 |

---

## 二、学生基本信息（CSV导入）

### 2.1 数据用途

- 创建学生账号（用于登录系统）
- 身份识别和验证
- 展示学生院系、专业、班级信息
- 自动分配审批人（根据班级匹配辅导员）

### 2.2 必需字段

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 学号 | student_id | 文本 | 是 | 学生唯一标识 | 2022001 |
| 姓名 | name | 文本 | 是 | 学生姓名 | 张三 |
| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
| 专业 | major | 文本 | 是 | 所属专业 | 计算机科学与技术 |
| 班级ID | class_id | 文本 | 是 | 班级唯一标识（重要） | CS2022-01 |
| 班级名称 | class_name | 文本 | 否 | 班级名称（用于展示） | 计算机科学与技术2022级1班 |
| 年级 | grade | 整数 | 是 | 入学年份 | 2022 |
| 毕业年份 | graduation_year | 整数 | 是 | 预计毕业年份 | 2026 |
| 是否毕业生 | is_graduating | 布尔 | 是 | 是否为当届毕业生 | true |

**可选字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 说明 | 示例 |
|---------------|---------------|----------|------|------|
| 手机号 | phone | 文本 | 用于找回密码 | 13800138000 |
| 邮箱 | email | 文本 | 用于通知 | zhangsan@example.com |

**重要说明：**
- `class_id` 必须全校唯一，用于映射辅导员，不能重复、变更或跨届复用
- `class_name` 仅用于展示，可以重复
- `is_graduating=true` 表示具备本批次离校申请资格
- 只需导入当届毕业生（约1000人），不需要全部学生

### 2.3 CSV模板

**文件名：** `学生基本信息导入模板.csv`

**文件编码：** UTF-8（避免中文乱码）

**模板内容：**
```csv
student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
2022001,张三,计算机学院,计算机科学与技术,CS2022-01,计算机科学与技术2022级1班,2022,2026,true,13800138000,zhangsan@example.com
2022002,李四,计算机学院,软件工程,SE2022-01,软件工程2022级1班,2022,2026,true,13800138001,lisi@example.com
```

**注意事项：**
- 第一行必须是字段名（英文）
- 布尔值用 `true` 或 `false`
- 文本字段如果包含逗号，需要用双引号包裹
- 不要使用Excel的"另存为CSV"，建议使用专业工具导出UTF-8编码

### 2.4 导入流程

**步骤1：准备CSV文件**
- 从教务系统或学工系统导出当届毕业生数据
- 按照模板格式整理数据
- 确保 `class_id` 字段填写正确（后续用于匹配辅导员）

**步骤2：上传CSV文件**
- 登录系统管理后台
- 进入"数据导入"模块
- 选择"学生基本信息导入"
- 上传CSV文件

**步骤3：系统自动校验**
- 必填字段非空校验
- 学号唯一性校验
- 班级ID存在性校验（需要先导入班级映射）
- 数据格式校验

**步骤4：查看校验报告**
- 成功数、失败数、新增数、更新数、停用数
- 错误明细（行号、字段、错误原因）
- 如有错误，修改CSV后重新上传

**步骤5：确认导入**
- 校验通过后，点击"确认导入"
- 系统执行导入操作
- 导入完成后，生成导入日志

### 2.5 导入策略

**首次导入：**
- 所有学生账号标记为"待设置密码"状态
- 学生首次登录时需要设置密码

**后续导入：**
- 已存在的学号：更新信息，保持账号激活
- 新增的学号：创建新账号
- 本次未导入的学号：自动标记为"停用"状态

**停用规则：**
- 停用账号不能登录
- 停用账号不能创建新申请
- 停用账号可以查看历史申请记录
- 下次导入重新出现时，自动激活

---

## 三、辅导员基本信息（CSV导入）

### 3.1 数据用途

- 创建辅导员账号（用于登录系统）
- 审批权限管理
- 班级-辅导员映射

### 3.2 必需字段

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 工号 | employee_id | 文本 | 是 | 辅导员唯一标识 | T2022001 |
| 姓名 | name | 文本 | 是 | 辅导员姓名 | 王老师 |
| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
| 手机号 | phone | 文本 | 否 | 联系电话 | 13900139000 |
| 邮箱 | email | 文本 | 否 | 联系邮箱 | wanglaoshi@example.com |
| 是否在职 | is_active | 布尔 | 是 | 是否在职 | true |

**重要说明：**
- `employee_id` 必须全校唯一，与统一身份认证、人事系统工号一致
- `is_active=false` 时不能登录、不能审批，但历史记录可查询

### 3.3 CSV模板

**文件名：** `辅导员基本信息导入模板.csv`

**模板内容：**
```csv
employee_id,name,department,phone,email,is_active
T2022001,王老师,计算机学院,13900139000,wanglaoshi@example.com,true
T2022002,李老师,软件学院,13900139001,lililaoshi@example.com,true
```

### 3.4 导入流程

与学生导入流程相同，参考第二章2.4节。

---

## 四、班级-辅导员对应关系（CSV导入）

### 4.1 数据用途

学生提交申请时，系统根据学生的 `class_id` 自动查询对应的辅导员，分配审批人。

### 4.2 必需字段

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2022-01 |
| 班级名称 | class_name | 文本 | 否 | 班级名称（用于展示） | 计算机科学与技术2022级1班 |
| 辅导员工号 | counselor_employee_id | 文本 | 是 | 辅导员工号 | T2022001 |

**重要说明：**
- `class_id` 必须全校唯一，不能重复
- `counselor_employee_id` 必须在辅导员表中存在
- 首版只支持一班一主辅导员，同一 `class_id` 不能出现多次

### 4.3 CSV模板

**文件名：** `班级辅导员对应关系导入模板.csv`

**模板内容：**
```csv
class_id,class_name,counselor_employee_id
CS2022-01,计算机科学与技术2022级1班,T2022001
SE2022-01,软件工程2022级1班,T2022002
```

### 4.4 导入顺序

**重要：必须按以下顺序导入**
1. 先导入辅导员基本信息
2. 再导入班级-辅导员对应关系
3. 最后导入学生基本信息

**原因：**
- 班级映射需要验证辅导员工号是否存在
- 学生导入需要验证班级ID是否有对应的辅导员

### 4.5 校验要求

系统会自动校验以下内容：
- 班级ID唯一性（不能重复）
- 辅导员工号存在性（必须在辅导员表中）
- 班级映射覆盖率（所有学生的class_id都有对应辅导员）

**导入后输出校验报告：**
- 未匹配班级：学生表中的class_id在映射表中不存在

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/design/2026-05-27-system-design.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 毕业生离校申请审批系统 - 系统设计文档

**项目名称：** 毕业生离校申请审批系统  
**文档版本：** v1.0  
**创建日期：** 2026-05-27  
**设计方案：** Django单体架构 + 容器化部署

---

## 目录

1. [系统架构设计](#1-系统架构设计)
2. [数据库设计](#2-数据库设计)
3. [API设计](#3-api设计)
4. [认证授权设计](#4-认证授权设计)
5. [审批流程设计](#5-审批流程设计)
6. [外部系统集成设计](#6-外部系统集成设计)
7. [部署架构设计](#7-部署架构设计)
8. [安全设计](#8-安全设计)
9. [性能优化设计](#9-性能优化设计)
10. [测试策略](#10-测试策略)

---

## 需求概述

### 业务流程

1. **流程发起：** 毕业生个人申请
   - 登录离校管理系统（挂在微信公众号）
   - 填写离校申请表，明确计划离校日期
   - 上传规定附件（宿舍清退证明、图书馆清书证明、财务结清截图）
   - 提交申请（需提前3个工作日）

2. **一级审批：** 毕业年级辅导员审核
   - 核实学生各项离校手续
   - 同意或驳回（注明原因）
   - 办理时限：1个工作日

3. **终端备案：** 学工部管理科负责人终审
   - 最终备案审核
   - 生成电子离校凭证
   - 办理时限：1个工作日

### 技术选型

- **平台：** iOS/Android + 微信小程序
- **前端：** React Native + 小程序原生
- **后端：** Python Django 4.2 + DRF
- **数据库：** PostgreSQL（本项目）+ 外部系统对接（MySQL/SQL Server/Oracle）
- **认证：** 混合认证（学号+密码 + 微信OAuth2）
- **部署：** Docker容器化部署（本地部署，单实例）

---

## 1. 系统架构设计

### 1.1 整体架构

```
┌─────────────────────────────────────────────┐
│           客户端层(Client Layer)            │
├──────────────┬──────────────┬───────────────┤
│ React Native │ React Native │  微信小程序    │
│   (iOS)      │  (Android)   │               │
└──────────────┴──────────────┴───────────────┘
                      │
                      ↓ HTTPS
┌─────────────────────────────────────────────┐
│         负载均衡层 (Load Balancer)          │
│              Nginx (容器)                   │
└─────────────────────────────────────────────┘
                      │
                      ↓
              ┌──────────────┐
              │   Django     │
              │   App        │
              │  (容器)      │
              │ Gunicorn     │
              │ 4 workers    │
              └──────────────┘
                      │
        ┌─────────────┴─────────────┐
        ↓                           ↓
┌──────────────┐            ┌──────────────┐
│   数据库层    │            │   缓存层      │
│ PostgreSQL   │            │   Redis      │
│  (容器)      │            │  (容器)      │
│              │            │              │
└──────────────┘            └──────────────┘
└──────────────┘                    │
        │                   ┌──────────────┐
        │                   │  任务队列     │
        │                   │  Celery      │
        │                   │  Worker      │
        │                   │  (容器)      │
        │                   └──────────────┘
        ↓
┌──────────────────────────────────────────┐
│         外部系统集成层                    │
├──────────────┬───────────────────────────┤
│ 宿舍管理系统  │  微信公众平台 │ 文件存储   │
│  (HTTP API) │  (OAuth2)    │ (本地/MinIO)│
└──────────────┴───────────────────────────┘
```

### 1.2 技术栈明细

**后端框架：**
- Django 4.2 LTS（长期支持版本）
- Django REST Framework 3.14（API开发）
- django-cors-headers（跨域支持）
- django-filter（过滤查询）

**数据库驱动：**
- mysqlclient（MySQL）
- psycopg2（PostgreSQL）
- mssql-django（SQL Server）
- cx_Oracle（Oracle）

**认证授权：**
- djangorestframework-simplejwt（JWT令牌）
- django-allauth（多认证方式）
- wechatpy（微信SDK）

**任务队列：**
- Celery 5.3（异步任务）
- Redis 7.0（消息代理+缓存）

**文件存储：**
- django-storages（存储抽象层）
- 本地文件系统
- MinIO（可选，本地对象存储）

### 1.3 模块划分

```
graduation_leave/
├── apps/
│   ├── accounts/          # 用户账户模块
│   │   ├── models.py      # 用户模型
│   │   ├── views.py       # 登录/注册API
│   │   ├── serializers.py # 数据序列化
│   │   └── auth.py        # 认证逻辑
│   │
│   ├── applications/      # 离校申请模块
│   │   ├── models.py      # 申请模型
│   │   ├── views.py       # 申请CRUD API
│   │   ├── workflows.py   # 审批流程
│   │   └── states.py      # 状态机定义
│   │
│   ├── approvals/         # 审批管理模块
│   │   ├── models.py      # 审批记录
│   │   ├── views.py       # 审批操作API
│   │   └── permissions.py # 权限控制
│   │
│   ├── attachments/       # 附件管理模块
│   │   ├── models.py      # 附件模型
│   │   ├── views.py       # 上传/下载API
│   │   └── storage.py     # 存储配置
│   │
│   ├── notifications/     # 通知模块
│   │   ├── models.py      # 通知记录
│   │   ├── tasks.py       # Celery异步任务
│   │   └── wechat.py      # 微信推送
│   │
│   └── integrations/      # 外部系统集成
│       ├── dorm_system.py # 宿舍系统对接
│       └── base.py        # 集成基类
│
├── config/                # 配置模块
│   ├── settings/
│   │   ├── base.py        # 基础配置
│   │   ├── dev.py         # 开发环境
│   │   └── prod.py        # 生产环境
│   └── database.py        # 数据库动态配置
│
└── utils/                 # 工具模块
    ├── validators.py      # 数据校验
    ├── exceptions.py      # 异常定义
    └── responses.py       # 统一响应格式
```

**模块职责：**

1. **accounts（用户账户）**
   - 学生/辅导员/学工部用户管理
   - 学号+密码登录
   - 微信OAuth2授权登录
   - JWT令牌生成和验证
   - 用户权限管理

2. **applications（离校申请）**
   - 申请表单创建
   - 申请信息修改
   - 申请状态查询
   - 申请历史记录
   - 离校日期管理

3. **approvals（审批管理）**
   - 辅导员审批操作
   - 学工部备案操作
   - 审批意见记录
   - 驳回原因记录
   - 审批时限监控

4. **attachments（附件管理）**
   - 附件上传（宿舍清退证明、图书馆清书证明、财务结清截图）
   - 附件下载
   - 附件预览
   - 附件存储管理（本地文件系统/MinIO）
   - 附件大小和格式校验
   - 附件与申请关联

5. **notifications（通知模块）**
   - 微信模板消息推送
   - 审批状态变更通知
   - 驳回原因通知
   - 审批完成通知
   - 异步任务队列（Celery）
   - 通知发送记录

6. **integrations（外部系统集成）**
   - 宿舍管理系统API对接
   - 宿舍清退状态查询
   - 外部系统认证
   - 接口重试机制
   - 接口超时处理
   - 插件化设计（便于扩展其他系统）

---

## 2. 数据库设计

### 2.1 数据库概述

**设计原则：**
- 本项目使用PostgreSQL数据库
- 使用 Django ORM 抽象层
- 遵循第三范式（3NF）
- 预留扩展字段
- 软删除设计（Django应用层过滤 + PROTECT外键）
- 外部系统通过API对接（支持MySQL/SQL Server/Oracle等异构系统）

**核心表：**
1. users - 用户表
2. applications - 离校申请表
3. approvals - 审批记录表
4. attachments - 附件表
5. notifications - 通知表
6. system_configs - 系统配置表
7. audit_logs - 审计日志表
8. applications_history - 申请历史表

### 2.2 用户表（users）

**说明：** 以下SQL为概念示例，使用类MySQL语法便于阅读。实际实现以Django Model为准，Django ORM会自动生成符合PostgreSQL的DDL语句。

```sql
CREATE TABLE users (

exec
/bin/bash -lc "rtk sed -n '260,520p' docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
- 方法签名是否合理？

**问题3：配置切换机制是否合理？**
- 使用环境变量 `USE_MOCK_DATA` 切换是否合适？
- 是否需要更细粒度的控制（如部分Mock、部分Real）？

### 3.2 风险评估

**问题4：真实API到位后的集成风险有多大？**
- 3天工期评估是否合理？
- 可能遇到哪些意外情况？
- 如何降低集成风险？

**问题5：数据映射不一致的应对策略？**
- 如果真实API字段与预期差异很大怎么办？
- 是否需要预留更多的适配层？
- 数据转换逻辑应该放在哪一层？

**问题6：Mock数据的真实性问题？**
- Mock数据是否足够真实？
- 是否会遗漏边界情况？
- 如何保证Mock数据与真实数据的一致性？

### 3.3 工期评估

**问题7：10周 + 3天工期是否合理？**
- 各阶段工期评估是否准确？
- 哪些环节可能延期？
- 是否需要增加缓冲时间？

**问题8：并行开发的可行性？**
- 80%工作不依赖API的判断是否准确？
- 是否有隐藏的依赖关系？
- 团队规模对并行开发的影响？

### 3.4 架构设计

**问题9：缓存策略是否合理？**
- Redis缓存TTL设置（用户信息1小时、清退状态10分钟）是否合适？
- 缓存更新策略是否完善？
- 缓存失效处理是否考虑周全？

**问题10：错误处理和降级策略？**
- API不可用时的降级方案是否完善？
- 重试机制是否合理？
- 错误日志和监控是否充分？

### 3.5 测试策略

**问题11：Mock数据测试覆盖度？**
- 使用Mock数据能否充分测试业务逻辑？
- 哪些场景必须用真实API测试？
- 如何保证测试的有效性？

**问题12：真实API测试重点？**
- API到位后应该重点测试哪些方面？
- 如何设计集成测试用例？
- 性能测试如何进行？

### 3.6 替代方案

**问题13：是否有更好的方案？**
- 除了Mock + 接口抽象，是否有其他方案？
- 是否可以考虑使用Stub、Fake等其他测试替身？
- 是否可以考虑Contract Testing（契约测试）？

**问题14：是否需要API网关或BFF层？**
- 是否需要在中间增加一层API网关？
- BFF（Backend For Frontend）模式是否适用？
- 这样做的利弊是什么？

---

## 四、期望的审查输出

### 4.1 技术方案评估

**请评估：**
1. Mock + 接口抽象方案的合理性（1-10分）
2. 方案的优缺点分析
3. 是否有致命缺陷或重大风险
4. 改进建议

### 4.2 风险识别

**请识别：**
1. 方案中可能遗漏的风险点
2. 风险等级评估（P0/P1/P2）
3. 风险缓解措施建议

### 4.3 工期评估

**请评估：**
1. 10周 + 3天工期是否合理
2. 各阶段工期是否需要调整
3. 关键路径和瓶颈分析

### 4.4 架构改进建议

**请提供：**
1. 接口设计改进建议
2. 缓存策略优化建议
3. 错误处理和降级策略改进
4. 测试策略改进

### 4.5 替代方案

**如果当前方案不合理，请提供：**
1. 替代方案描述
2. 替代方案的优缺点
3. 实施难度和工期评估

---

## 五、审查范围

**本次审查聚焦：**
1. ✓ 技术方案的合理性和可行性
2. ✓ 风险识别和缓解措施
3. ✓ 工期评估的准确性
4. ✓ 架构设计的完善性

**不在本次审查范围：**
1. ✗ 具体代码实现细节
2. ✗ 前端UI/UX设计
3. ✗ 部署和运维方案
4. ✗ 安全审计（已在Round 2完成）

---

## 六、补充信息

### 6.1 项目背景

- **项目名称：** 毕业生离校申请审批系统
- **技术栈：** Python Django + PostgreSQL + Redis + React Native + 微信小程序
- **团队规模：** 2-3人
- **预计工期：** 8-10周（原计划）
- **当前状态：** 设计完成，准备实施

### 6.2 已完成的审查

- Round 1: 架构和数据库设计（10个问题修复）
- Round 2: API、审批、部署、安全、性能（29个问题修复）
- Round 3: P0修复、字段补充、用户文档（20+问题修复）

### 6.3 相关文档

- 系统设计文档：`docs/design/2026-05-27-system-design.md`
- 数据对接说明：`docs/数据对接说明文档.md`
- 项目总结：`docs/PROJECT-SUMMARY.md`

---

**审查请求人：** Claude Opus 4.7  
**创建时间：** 2026-05-30  
**期望审查时间：** 1-2小时  
**优先级：** P0（阻塞开发进度）

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 数据源需求共识文档

**文档版本：** v2.0  
**创建时间：** 2026-05-27  
**修订时间：** 2026-05-27  
**目的：** 明确毕业离校系统所需的数据源，提交给宿管系统方反馈

---

## 版本变更说明（v1 → v2）

**主要修正：**

1. **CSV导入策略**：从"全量覆盖"改为"staging表 + upsert + 软停用"
2. **数据库模型调整**：
   - users表：`student_id`改为可空，新增`employee_id`和`class_id`字段
   - 新增`class_counselor_mapping`表（班级-辅导员映射）
   - 新增`graduation_batches`表（批次配置）
   - 新增`import_logs`表（导入审计）
   - 拆分staging表：`students_staging`、`counselors_staging`、`class_mapping_staging`
3. **认证约束调整**：增加`password_setup_required`支持CSV预导入账号
4. **对接方式调整**：学生/辅导员/班级映射改为"CSV/Excel首版优先"
5. **约束增强**：学生必须有`class_id`，复用`system_configs`表

**修正依据：**
- Codex第二轮审查（34-codex-second-review-response.md）
- Codex关键问题审查（35-response-to-codex-critical-issues.md）

---

## 一、数据源概述

本系统需要以下数据源支持系统运行：

| 数据源 | 优先级 | 用途 | 对接方式 |
|--------|--------|------|----------|
| 学生基本信息 | P0 | 创建学生账号、身份识别、班级映射 | **CSV/Excel首版优先** / API或DB增强 |
| 宿舍清退数据 | P0 | 验证学生是否完成宿舍清退 | API优先 / DB备选 / CSV降级 |
| 辅导员基本信息 | P0 | 创建辅导员账号、审批权限 | **CSV/Excel首版优先** / 人事或统一身份API增强 |
| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |

**对接方式说明：**
- **CSV/Excel首版优先**：首版采用CSV/Excel批量导入，快速上线，后续根据数据变更频率决定是否升级为API/DB
- **API优先**：调用宿管系统提供的API接口（实时校验场景）
- **DB备选**：直接读取宿管系统数据库（需要安全审批和网络配置）
- **CSV降级**：当无法提供API或DB时，通过CSV文件导入

**首版策略调整理由：**
1. **实施周期**：CSV/Excel导入最快，DB直连需要安全审批和网络配置
2. **变更频率**：账号数据变更频率低（学期级），不需要实时同步
3. **风险控制**：CSV导入可以先验证、再导入、可回滚；DB直连风险更高

---

## 二、P0数据源详细要求

### 2.1 学生基本信息

**用途：**
- 创建学生账号（用于登录系统）
- 身份识别和验证
- 展示学生院系、专业、班级信息
- 自动分配审批人（根据班级匹配辅导员）

**必需字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 学号 | student_id | 文本 | 是 | 学生唯一标识 | 2022001 |
| 姓名 | name | 文本 | 是 | 学生姓名 | 张三 |
| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
| 专业 | major | 文本 | 是 | 所属专业 | 计算机科学与技术 |
| 班级ID | class_id | 文本 | 是 | 班级唯一标识（核心键） | CS2022-01 |
| 班级名称 | class_name | 文本 | 否 | 班级名称（用于展示） | 计算机科学与技术2022级1班 |
| 年级 | grade | 整数 | 是 | 入学年份 | 2022 |
| 毕业年份 | graduation_year | 整数 | 是 | 预计毕业年份 | 2026 |
| 是否毕业生 | is_graduating | 布尔 | 是 | 是否为当届毕业生 | true |

**可选字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 说明 | 示例 |
|---------------|---------------|----------|------|------|
| 手机号 | phone | 文本 | 用于找回密码或二次验证 | 13800138000 |
| 邮箱 | email | 文本 | 用于通知或找回密码 | zhangsan@example.com |

**字段说明：**
- `class_id`：班级唯一标识，全校唯一，用于映射辅导员（**v2新增必填要求**）
- `class_name`：班级显示名称，可能重复、变更或跨届复用，仅用于展示
- `is_graduating`：标识是否为当届毕业生，`true`表示具备本批次离校申请资格
- `graduation_year`：示例统一为2026（与当前项目日期保持一致）

**CSV模板示例：**

```csv
student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
2022001,张三,计算机学院,计算机科学与技术,CS2022-01,计算机科学与技术2022级1班,2022,2026,true,13800138000,zhangsan@example.com
2022002,李四,计算机学院,软件工程,SE2022-01,软件工程2022级1班,2022,2026,true,13800138001,lisi@example.com
```

**数据范围：**
- 只导入当届毕业生（`is_graduating=true` 且 `graduation_year=2026`）
- 约1000人/届

---

### 2.2 宿舍清退数据

**用途：**
- 验证学生是否完成宿舍清退（提交申请前置条件）
- 展示清退状态和完成时间

**必需字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 学号 | student_id | 文本 | 是 | 学生学号 | 2022001 |
| 姓名 | name | 文本 | 是 | 学生姓名（用于二次验证） | 张三 |
| 清退状态 | checkout_status | 枚举 | **是** | 清退状态（**v2改为必填**） | completed |
| 清退完成时间 | checkout_date | 日期时间 | 条件必填 | 当status=completed时必填 | 2026-05-20 14:30:00 |
| 数据更新时间 | source_updated_at | 日期时间 | 建议 | 外部系统数据更新时间（**v2新增**） | 2026-05-20 15:00:00 |

**枚举值说明（v2修订）：**
- `completed`：已完成清退
- `pending`：清退中（已申请但未完成）
- `not_started`：未开始清退
- `unknown`：查询失败或数据不可用（用于API异常时的降级）

**API响应示例：**

```json
{
  "student_id": "2022001",
  "name": "张三",
  "checkout_status": "completed",
  "checkout_date": "2026-05-20T14:30:00",
  "source_updated_at": "2026-05-20T15:00:00"
}
```

**降级处理：**
- API查询失败时，返回 `checkout_status: "unknown"`
- 系统允许学生提交申请，但需上传宿舍清退证明截图

---

### 2.3 辅导员基本信息

**用途：**
- 创建辅导员账号（用于登录系统）
- 审批权限管理
- 班级-辅导员映射

**必需字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 工号 | employee_id | 文本 | 是 | 辅导员唯一标识（**v2新增**） | T2022001 |
| 姓名 | name | 文本 | 是 | 辅导员姓名 | 王老师 |
| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
| 手机号 | phone | 文本 | 否 | 联系电话 | 13900139000 |
| 邮箱 | email | 文本 | 否 | 联系邮箱 | wanglaoshi@example.com |
| 是否在职 | is_active | 布尔 | 是 | 是否在职（**v2新增**） | true |

**字段说明：**
- `employee_id`：辅导员工号，必须全校唯一，与统一身份认证、人事系统工号一致
- `is_active`：标识是否在职，`false`时不能登录、不能审批，但历史记录可查询

**CSV模板示例：**

```csv
employee_id,name,department,phone,email,is_active
T2022001,王老师,计算机学院,13900139000,wanglaoshi@example.com,true
T2022002,李老师,软件学院,13900139001,lililaoshi@example.com,true
```

**数据范围：**
- 当前在职辅导员
- 约50人

**停用规则（v2新增）：**

| 账号状态 | 登录 | 创建申请 | 审批 | 查看历史 | 接收通知 |
|---------|------|---------|------|---------|---------|
| `is_active=true` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `is_active=false` | ❌ | ❌ | ❌ | ✅（仅自己的） | ❌ |

---

### 2.4 班级-辅导员对应关系

**用途：**
- 学生提交申请时自动分配辅导员审批人
- 支持辅导员变更和历史追溯

**必需字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2022-01 |
| 班级名称 | class_name | 文本 | 否 | 班级名称（用于展示） | 计算机科学与技术2022级1班 |
| 辅导员工号 | counselor_employee_id | 文本 | 是 | 辅导员工号 | T2022001 |

**可选字段（v2新增）：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 说明 | 示例 |
|---------------|---------------|----------|------|------|
| 生效日期 | effective_from | 日期 | 映射生效日期 | 2026-01-01 |
| 失效日期 | effective_until | 日期 | 映射失效日期，NULL表示长期有效 | NULL |
| 毕业批次ID | graduation_batch_id | 整数 | 关联毕业批次 | 1 |

**字段说明：**
- `class_id`：班级唯一标识，必须全校唯一，不能重复、变更或跨届复用
- `counselor_employee_id`：必须在辅导员表中存在且 `is_active=true`
- 首版只支持一班一主辅导员，同一 `class_id` 不能出现多次

**CSV模板示例：**

```csv
class_id,class_name,counselor_employee_id
CS2022-01,计算机科学与技术2022级1班,T2022001
SE2022-01,软件工程2022级1班,T2022002
```

**校验要求：**
- 学生表中的 `class_id` 必须在班级映射表中存在
- 班级映射表中的 `counselor_employee_id` 必须在辅导员表中存在
- 导入后输出校验报告：未匹配班级、未匹配辅导员、重复映射、无审批人的学生数

**历史一致性规则（v2新增）：**
- 已提交申请的 `counselor_id` 不自动改写，保持历史一致性
- 新提交申请使用新映射
- 如需改派，由管理员显式操作并记录审计日志

---

### 2.5 学工部管理员信息

**用途：**
- 创建管理员账号（终审权限）
- 系统配置和管理

**必需字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 工号 | employee_id | 文本 | 是 | 管理员唯一标识 | A2022001 |
| 姓名 | name | 文本 | 是 | 管理员姓名 | 赵主任 |
| 部门 | department | 文本 | 是 | 所属部门 | 学工部 |
| 手机号 | phone | 文本 | 否 | 联系电话 | 13700137000 |
| 邮箱 | email | 文本 | 否 | 联系邮箱 | zhaozr@example.com |

**数据范围：**
- 约5人
- 首版采用手动创建，不参与批量导入

**默认终审人配置（v2新增）：**
- 系统配置表（`system_configs`）存储默认终审人列表
- 配置项：`default_admin_ids`（如 `3,5,7`）
- 分配模式：`admin_assignment_mode`（fixed/round_robin/load_balance）

exec
/bin/bash -lc "rtk sed -n '240,520p' docs/数据对接说明文档.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
- 未匹配班级：学生表中的class_id在映射表中不存在
- 未匹配辅导员：映射表中的工号在辅导员表中不存在
- 重复映射：同一class_id出现多次
- 无审批人的学生数：有多少学生没有对应的辅导员

---

## 五、宿舍清退数据（API接口）

### 5.1 数据用途

学生提交离校申请时，系统实时查询宿舍清退状态：
- 已完成清退：允许提交申请
- 未完成清退：提示学生先完成宿舍清退手续
- 查询失败：允许学生上传宿舍清退证明截图

### 5.2 接口规范

**接口名称：** 查询学生宿舍清退状态

**请求方式：** GET 或 POST

**请求地址：** `http://宿舍管理系统域名/api/dorm/checkout/status`

**认证方式：** API Key + IP白名单

### 5.3 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| student_id | String | 是 | 学号 | "2022001" |
| name | String | 是 | 姓名（用于验证） | "张三" |

**请求示例（GET）：**
```
GET /api/dorm/checkout/status?student_id=2022001&name=张三
Host: dorm.example.com
Authorization: Bearer YOUR_API_KEY
```

### 5.4 响应参数

**成功响应（HTTP 200）：**

```json
{
  "code": 0,
  "message": "查询成功",
  "data": {
    "student_id": "2022001",
    "name": "张三",
    "checkout_status": "completed",
    "checkout_date": "2026-05-20T14:30:00",
    "source_updated_at": "2026-05-20T15:00:00"
  }
}
```

**响应字段说明：**

| 字段名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| checkout_status | String | 是 | 清退状态 | "completed" |
| checkout_date | String | 条件必填 | 清退完成时间（status=completed时必填） | "2026-05-20T14:30:00" |
| source_updated_at | String | 建议 | 数据更新时间 | "2026-05-20T15:00:00" |

**清退状态枚举值：**
- `completed` - 已完成清退
- `pending` - 清退中（已申请但未完成）
- `not_started` - 未开始清退
- `unknown` - 查询失败或数据不可用

### 5.5 错误响应

**学号不存在（HTTP 404）：**
```json
{
  "code": 1001,
  "message": "学号不存在",
  "data": null
}
```

**参数错误（HTTP 400）：**
```json
{
  "code": 1002,
  "message": "参数缺失：student_id",
  "data": null
}
```

**服务器错误（HTTP 500）：**
```json
{
  "code": 5000,
  "message": "服务器内部错误",
  "data": null
}
```

### 5.6 技术要求

**性能要求：**
- 响应时间：< 2秒
- 超时时间：5秒
- 重试次数：失败后重试3次

**限流要求：**
- 每分钟最多60次请求
- 超过限流返回HTTP 429

**降级处理：**
- API查询失败时，返回 `checkout_status: "unknown"`
- 允许学生上传宿舍清退证明截图
- 管理员审核通过后允许提交

---

## 六、技术要求和规范

### 6.1 CSV文件要求

**文件格式：**
- 编码：UTF-8（必须）
- 格式：CSV或Excel（.xlsx）
- 大小限制：单文件不超过10MB
- 行数限制：单文件不超过10000行

**数据格式：**
- 第一行必须是字段名（英文）
- 布尔值用 `true` 或 `false`
- 日期格式：`YYYY-MM-DD`
- 日期时间格式：`YYYY-MM-DD HH:MM:SS`
- 文本字段如果包含逗号，需要用双引号包裹

### 6.2 导入审计

系统会记录每次导入操作：
- 导入类型（学生/辅导员/班级映射）
- 文件名和文件哈希（SHA256）
- 操作人和操作时间
- 导入结果（成功数、失败数、新增数、更新数、停用数）
- 错误明细（JSON格式）

### 6.3 数据安全

**传输安全：**
- API接口必须使用HTTPS
- API Key定期更换（建议每季度）
- IP白名单限制访问

**存储安全：**
- 密码采用bcrypt加密存储
- 敏感字段（手机号、邮箱）加密存储
- 导入日志保留3个月

---

## 七、常见问题

### 7.1 CSV导入相关

**Q1：CSV文件中文乱码怎么办？**

A：确保文件编码为UTF-8。如果使用Excel编辑，保存时选择"CSV UTF-8（逗号分隔）"格式。

**Q2：导入时提示"学号重复"怎么办？**

A：检查CSV文件中是否有重复的学号。系统要求学号必须唯一。

**Q3：导入时提示"班级ID不存在"怎么办？**

A：需要先导入班级-辅导员对应关系，再导入学生信息。

**Q4：如何批量停用账号？**

A：在下次导入时，不包含需要停用的账号即可。系统会自动将本次未导入的账号标记为停用。

### 7.2 API接口相关

**Q5：API接口如何测试？**

A：提供测试环境和测试账号，使用Postman或curl工具测试。

**Q6：API查询失败怎么办？**

A：系统会自动重试3次。如果仍然失败，允许学生上传宿舍清退证明截图。

**Q7：API接口需要认证吗？**

A：是的，需要在请求头中传递API Key，并配置IP白名单。

### 7.3 数据更新相关

**Q8：数据多久更新一次？**

A：建议每学期更新1-2次。如果数据变更频繁，可以升级为API/数据库同步。

**Q9：如何更新单个学生信息？**

A：可以通过系统管理后台手动修改，或者重新导入包含该学生的CSV文件。

**Q10：辅导员调岗后如何处理？**

A：更新班级-辅导员对应关系，重新导入CSV文件。已提交的申请不受影响，新提交的申请使用新辅导员。

---

## 八、联系方式

**技术支持：** [待填写]  
**故障响应时间：** [待确认]  
**数据对接联系人：** [待填写]


exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 数据对接确认清单与实施计划

**文档版本：** v1.0  
**创建时间：** 2026-05-27  
**目的：** 提交给宿管系统方，确认数据可用性和实施计划  
**依据文档：** `31-data-source-requirements-consensus-v2.md`

---

## 一、待宿管系统确认的问题清单

### 1.1 数据可用性确认

**问题1：** 宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？

**问题2：** 如不包含，能否从教务/人事/学工系统归集后提供？

**问题3：** 能否只提供当届毕业生数据（约1000人），还是必须提供全部学生数据？

---

### 1.2 字段和标识确认

**问题4：** `class_id`（班级ID）是否全校唯一？班级名称是否可能重复、变更或跨届复用？

**背景说明：** 系统需要用 `class_id` 作为核心键映射辅导员，如果只有班级名称，可能导致映射错误。

**问题5：** 辅导员工号（`employee_id`）是否全校唯一？是否与统一身份认证、人事系统工号一致？

**背景说明：** 系统需要用工号作为辅导员唯一标识，确保与其他系统数据一致。

**问题6：** 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？

**背景说明：** 系统需要明确哪些学生具备离校申请资格，通过 `is_graduating` 字段标识。

---

### 1.3 多辅导员场景确认

**问题7：** 是否存在一个班级多个辅导员、代理辅导员、临时负责人或辅导员调岗场景？

**背景说明：** 首版系统只支持一班一主辅导员，如果存在多辅导员场景，需要明确主辅导员。

**问题8：** 班级-辅导员映射变更频率如何？是否能提供当前有效映射和历史有效期？

**背景说明：** 系统需要确定是否需要支持映射历史追溯和有效期管理。

---

### 1.4 对接方式确认

**问题9：** 优先推荐的对接方式是什么？

选项：
- A. 数据库直连（需要安全审批和网络配置）
- B. API接口（需要开发API）
- C. CSV/Excel文件导入（最快，首版推荐）

**问题10：** 各数据源能否提供测试数据、测试环境和字段字典？

**背景说明：** 开发和测试阶段需要测试数据验证对接逻辑。

**问题11：** CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？

**背景说明：** 系统采用"staging + upsert + 软停用"策略，本次未导入的账号自动标记为停用。

---

### 1.5 异常处理确认

**问题12：** 外部系统不可用、数据延迟或查询失败时，业务上允许怎样的人工降级？

**背景说明：** 例如宿舍清退API查询失败时，是否允许学生上传截图证明？

**问题13：** 是否有统一身份认证或微信绑定前置要求？

**背景说明：** 系统支持密码登录和微信登录，CSV导入的账号需要首次登录设置密码。

**问题14：** 是否需要导入手机号/邮箱用于找回密码或二次验证？

**背景说明：** 手机号和邮箱为可选字段，如果不提供，学生只能通过管理员重置密码。

---

### 1.6 实施保障确认

**问题15：** 数据提供方能否承诺导出频率、数据更新时间、联系人和故障响应时间？

**背景说明：** 需要明确数据更新周期和故障联系人，确保系统稳定运行。

---

## 二、实施计划

### 2.1 推荐方案

首版采用**CSV/Excel导入 + 宿舍清退API**组合方案：

| 数据源 | 对接方式 | 理由 |
|--------|---------|------|
| 学生基本信息 | CSV/Excel导入 | 变更频率低（学期级），快速上线 |
| 辅导员基本信息 | CSV/Excel导入 | 约50人，变更频率低 |
| 班级-辅导员映射 | CSV/Excel导入 | 变更频率低，需强校验 |
| 宿舍清退数据 | API实时查询 | 需要实时校验清退状态 |

**后续优化：** 根据数据变更频率决定是否升级为API/DB同步。

---

### 2.2 实施路径（5阶段）

**阶段1：数据确认（1周）**

**目标：** 明确数据可用性和对接方式

**任务：**
1. 向宿管系统提交本确认清单
2. 确认15个问题的答案
3. 获取测试数据和字段字典
4. 明确联系人和故障响应方式

**交付物：**
- 数据可用性确认表
- 测试数据样本
- 字段字典文档
- 联系人和响应时间承诺

---

**阶段2：CSV导入实现（2周）**

**目标：** 实现CSV批量导入功能

**任务：**
1. 设计三份CSV模板：
   - 学生基本信息模板
   - 辅导员基本信息模板
   - 班级-辅导员映射模板
2. 实现CSV导入功能：
   - 文件上传和解析
   - 数据校验（必填字段、唯一性、引用完整性）
   - Staging表和upsert逻辑
   - 软停用和重新激活逻辑
3. 实现导入审计日志
4. 生成导入校验报告：
   - 成功数、失败数、新增数、更新数、停用数
   - 错误明细（行号、字段、错误原因）
5. 重点校验：
   - 学号唯一性
   - 工号唯一性
   - 班级映射覆盖率（所有学生的class_id都有对应辅导员）
   - 无效辅导员工号（映射表中的工号在辅导员表中不存在）
   - 重复映射（同一班级多个辅导员）

**交付物：**
- CSV导入功能模块
- 三份CSV模板文件
- 导入校验报告示例
- 导入操作手册

---

**阶段3：宿舍清退API对接（1周）**

**目标：** 实现宿舍清退状态实时查询

**任务：**
1. 对接宿管系统宿舍清退API
2. 实现API调用逻辑：
   - 认证和鉴权
   - 请求参数构造（学号、姓名）
   - 响应解析（清退状态、完成时间）
3. 实现降级处理：
   - API失败：返回 `checkout_status: "unknown"`
   - 超时：重试3次后降级
   - 数据过期：提示学生联系宿管
4. 测试异常场景：
   - API不可用
   - 网络超时
   - 数据不一致
5. 实现人工证明流程：
   - 学生上传宿舍清退证明截图
   - 管理员审核通过后允许提交

**交付物：**
- 宿舍清退API对接模块
- API异常处理逻辑
- 人工证明审核流程
- API对接测试报告

---

**阶段4：上线前验收（1周）**

**目标：** 确保数据完整性和系统稳定性

**任务：**
1. 冻结当届数据批次：
   - 创建2026届毕业批次配置
   - 设置申请开放时间和截止时间
   - 设置允许的离校日期范围
2. 完成一次全量导入演练：
   - 导入学生数据（约1000人）
   - 导入辅导员数据（约50人）
   - 导入班级映射数据（约50-100条）
3. 清零异常清单：
   - 无效学号：0个
   - 无效工号：0个
   - 未映射班级：0个
   - 无审批人的学生：0个
4. 确认终审管理员配置：
   - 配置默认终审人列表（3-5人）
   - 配置分配模式（fixed/round_robin/load_balance）
   - 测试终审人分配逻辑
5. 系统功能测试：
   - 学生登录和首次设置密码
   - 辅导员登录和审批
   - 管理员登录和终审
   - 宿舍清退状态查询
   - 申请提交和审批流程

**交付物：**
- 全量导入演练报告
- 异常清单（应为空）
- 终审管理员配置确认
- 系统功能测试报告
- 上线检查清单

---

**阶段5：上线后优化（按需）**

**目标：** 根据实际运行情况优化系统

**任务：**
1. 监控数据变更频率：
   - 学生数据变更频率
   - 辅导员数据变更频率
   - 班级映射变更频率
2. 评估是否升级为API/DB同步：
   - 如果变更频率高（每周多次），考虑升级为API实时同步
   - 如果变更频率低（每学期1-2次），保持CSV导入
3. 评估是否支持多辅导员场景：
   - 如果存在多辅导员需求，扩展班级映射表支持多辅导员
   - 增加主辅导员标识字段
4. 收集用户反馈：
   - 学生使用体验
   - 辅导员审批效率
   - 管理员管理便利性
5. 持续优化：
   - 导入流程优化
   - 审批流程优化
   - 通知机制优化

**交付物：**
- 数据变更频率监控报告
- 优化方案建议
- 用户反馈汇总
- 持续优化计划


exec
/bin/bash -lc 'rtk rg -n "外部系统集成|宿舍|checkout|class_counselor|staging|import_logs|缓存|TTL|降级|unknown|重试" docs/design/2026-05-27-system-design.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
17:6. [外部系统集成设计](#6-外部系统集成设计)
32:   - 上传规定附件（宿舍清退证明、图书馆清书证明、财务结清截图）
86:│   数据库层    │            │   缓存层      │
100:│         外部系统集成层                    │
102:│ 宿舍管理系统  │  微信公众平台 │ 文件存储   │
128:- Redis 7.0（消息代理+缓存）
167:│   └── integrations/      # 外部系统集成
168:│       ├── dorm_system.py # 宿舍系统对接
208:   - 附件上传（宿舍清退证明、图书馆清书证明、财务结清截图）
223:6. **integrations（外部系统集成）**
224:   - 宿舍管理系统API对接
225:   - 宿舍清退状态查询
227:   - 接口重试机制
416:- `dorm_clearance` - 宿舍清退证明
438:    retry_count INT DEFAULT 0 COMMENT '重试次数',
439:    last_retry_at TIMESTAMP COMMENT '最后重试时间',
489:- `integration` - 外部系统集成配置
496:- `dorm_integration_type` - 宿舍系统集成类型（api/database）
497:- `dorm_api_url` - 宿舍系统API地址
498:- `dorm_api_key` - 宿舍系统API密钥（加密存储）
499:- `dorm_db_config` - 宿舍系统数据库配置（加密存储，JSON格式）
923:        "file_name": "宿舍清退证明.jpg",
1024:  "message": "申请已被修改，请刷新后重试",
1038:  "opinion": "宿舍清退证明不完整，请重新提交",
1055:  "message": "申请已被修改，请刷新后重试",
1080:    "file_name": "宿舍清退证明.jpg",
1189:      "description": "宿舍系统集成类型（api/database）"
1194:      "description": "宿舍系统API地址"
1199:      "description": "宿舍系统API密钥（加密存储）",
1228:- `integration` - 外部系统集成配置（宿舍系统等）
1421:  - 必须上传宿舍清退证明
1587:**降级策略：**
1588:- 外部系统（宿舍管理系统）不可用时，允许手动上传证明文件
1590:- 系统记录降级操作日志
1593:## 6. 外部系统集成设计
1603:2. **降级策略**：外部系统不可用时，允许手动上传证明文件
1605:### 6.2 宿舍管理系统对接
1608:验证学生宿舍清退状态，确保离校手续真实完成。
1622:# 查询宿舍清退状态
1640:    "checkout_date": "2026-05-25",
1641:    "checkout_status": "completed"
1657:    def get_checkout_status(self, student_id):
1659:            f'{self.base_url}/api/students/{student_id}/checkout',
1692:            raise ExternalSystemTimeout("宿舍系统超时")
1694:            raise ExternalSystemError(f"宿舍系统错误: {str(e)}")
1697:### 6.3 错误处理和重试机制
1706:    """超时异常 - 可重试"""
1710:    """服务不可用 - 可重试"""
1714:    """认证失败 - 不可重试"""
1718:**重试策略：**
1723:    stop=stop_after_attempt(3),  # 最多重试3次
1732:**降级策略：**
1735:- 系统记录降级操作日志
1749:  redis:          # 缓存+消息队列
2070:    'DEFAULT_THROTTLE_CLASSES': [
2074:    'DEFAULT_THROTTLE_RATES': {
2320:- `dorm_api_key` - 宿舍系统API密钥
2321:- `dorm_db_config` - 宿舍系统数据库配置（JSON格式）
2431:### 9.2 缓存策略
2433:**Redis缓存层级：**
2435:# L1: 用户信息缓存（30分钟）
2438:# L2: 申请状态缓存（5分钟）
2441:# L3: 待审批数量缓存（1分钟）
2445:**缓存更新策略：**
2448:- 缓存穿透：空值缓存
2449:- 缓存雪崩：随机过期时间
2451:**缓存失效规则：**
2454:    """申请状态变更时失效相关缓存"""
2458:    # 失效审批人的待审批数量缓存
2463:    # 失效学生的申请列表缓存
2467:    """用户信息变更时失效缓存"""
2479:**不缓存的内容：**
2484:**Django缓存配置：**
2532:- 本地缓存用户信息
2794:3. 微信通知依赖外部服务（需配置降级策略）

exec
/bin/bash -lc "rtk sed -n '260,620p' docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
- 分配模式：`admin_assignment_mode`（fixed/round_robin/load_balance）
- 首版采用固定分配（fixed），使用第一个可用管理员

---

## 三、数据对接方式详细说明

### 3.1 CSV/Excel导入（首版推荐）

**适用场景：**
- 学生基本信息
- 辅导员基本信息
- 班级-辅导员对应关系

**技术要求：**

**文件格式：**
- 编码：UTF-8（避免中文乱码）
- 格式：CSV或Excel（.xlsx）
- 大小限制：单文件不超过10MB
- 行数限制：单文件不超过10000行

**导入策略（v2修订）：**

采用**staging表 + upsert + 软停用**模式：

1. CSV导入到临时staging表（按类型拆分）
2. 存在则更新，不存在则插入（upsert）
3. 本次未导入的账号标记为 `is_active=false`
4. 下次导入重新出现时自动激活

**Staging表设计（v2新增）：**

```sql
-- 学生导入staging表
CREATE TABLE students_staging (
    student_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    major VARCHAR(100),
    class_id VARCHAR(50),
    class_name VARCHAR(100),
    grade INT,
    graduation_year INT,
    is_graduating BOOLEAN,
    phone VARCHAR(20),
    email VARCHAR(100)
);

-- 辅导员导入staging表
CREATE TABLE counselors_staging (
    employee_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100)
);

-- 班级映射导入staging表
CREATE TABLE class_mapping_staging (
    class_id VARCHAR(50) PRIMARY KEY,
    counselor_employee_id VARCHAR(50) NOT NULL
);
```

**导入流程：**

```sql
-- 1. 清空staging表
TRUNCATE students_staging;

-- 2. 导入CSV到staging表
LOAD DATA INFILE 'students.csv' INTO TABLE students_staging;

-- 3. Upsert到users表
INSERT INTO users (student_id, name, department, class_id, role, is_active, password_setup_required, ...)
SELECT student_id, name, department, class_id, 'student', true, true, ...
FROM students_staging
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    department = VALUES(department),
    class_id = VALUES(class_id),
    is_active = true,
    updated_at = NOW();

-- 4. 软停用：本次未导入的学生（使用NOT EXISTS避免NULL问题）
UPDATE users u
SET is_active = false, updated_at = NOW()
WHERE u.role = 'student'
  AND NOT EXISTS (
      SELECT 1 FROM students_staging s
      WHERE s.student_id = u.student_id
  );
```

**校验要求：**
- 必填字段非空校验
- 学号/工号唯一性校验
- 班级ID存在性校验
- 辅导员工号存在性校验
- 重复数据校验

**导入审计（v2新增）：**

```sql
CREATE TABLE import_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    import_type ENUM('student', 'counselor', 'class_mapping') NOT NULL,
    file_name VARCHAR(255),
    file_hash VARCHAR(64),                      -- SHA256
    uploaded_by INT,                            -- 操作人user_id
    total_rows INT,
    success_rows INT,
    failed_rows INT,
    new_rows INT,                               -- 新增
    updated_rows INT,                           -- 更新
    disabled_rows INT,                          -- 软停用
    error_details TEXT,                         -- JSON格式错误明细
    import_status ENUM('pending', 'success', 'partial', 'failed'),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE SET NULL
);
```

**错误报告示例：**

```json
{
  "errors": [
    {"row": 5, "field": "student_id", "error": "学号重复"},
    {"row": 12, "field": "class_id", "error": "班级ID不存在"}
  ],
  "warnings": [
    {"row": 8, "field": "phone", "error": "手机号格式不正确"}
  ]
}
```

---

### 3.2 API接口（实时校验场景）

**适用场景：**
- 宿舍清退数据（实时校验）

**技术要求：**

**接口规范：**
- 协议：HTTP/HTTPS
- 方法：GET或POST
- 认证：API Key或OAuth2
- 响应格式：JSON
- 超时时间：5秒

**分页支持：**
- 每页最多100条
- 支持 `page`/`page_size` 参数

**增量同步：**
- 支持 `updated_after` 参数
- 只返回指定时间后更新的数据

**错误码规范：**
- 200：成功
- 400：参数错误
- 401：认证失败
- 404：数据不存在
- 500：服务器错误

**限流策略：**
- 每分钟最多60次请求

**重试机制：**
- 失败后指数退避重试，最多3次

**幂等性：**
- 同一请求多次调用结果一致

---

### 3.3 数据库直连（后续增强）

**适用场景：**
- 数据变更频率高时升级使用

**技术要求：**

**安全边界：**
- 只读账号，不得有写权限
- 使用只读视图或同步库，不直接访问生产业务表
- IP白名单限制，只允许应用服务器访问

**连接池配置：**
- 最大连接数：5
- 超时时间：30秒
- 重试策略：失败后等待5秒重试

**支持数据库：**
- MySQL 5.7+
- SQL Server 2016+
- Oracle 11g+
- PostgreSQL 10+

---

## 四、数据量估算

**明确说明（v2修订）：**

| 数据项 | 首版范围 | 容量设计 | 说明 |
|--------|----------|----------|------|
| 学生账号 | 当届毕业生 | 1000人/届 | 只导入当届（`is_graduating=true` 且 `graduation_year=2026`） |
| 系统容量 | 支持多届历史 | 10000人 | 数据库设计按10000人容量 |
| 辅导员账号 | 当前在职 | 50人 | 离职辅导员标记 `is_active=false` |
| 班级映射 | 当届有效映射 | 50-100条 | 首版不考虑历史有效期 |
| 学工部管理员 | 当前在职 | 5人 | 手动创建 |
| 申请记录 | 当届申请 | 1000条/届 | 每个学生最多1个进行中申请 |

**批次配置（v2新增）：**

```sql
CREATE TABLE graduation_batches (
    id INT PRIMARY KEY AUTO_INCREMENT,
    batch_name VARCHAR(100) NOT NULL,           -- 如 "2026届本科毕业生"
    graduation_year INT NOT NULL,               -- 2026
    is_active BOOLEAN DEFAULT true,             -- 当前批次（仅一个）
    application_start_date DATE,                -- 申请开放时间
    application_end_date DATE,                  -- 申请截止时间
    planned_leave_date_start DATE,              -- 允许的最早离校日期
    planned_leave_date_end DATE,                -- 允许的最晚离校日期
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 约束：仅一个当前批次
    UNIQUE KEY uk_active_batch (is_active) WHERE is_active = true
);
```

**学生导入时只导入当前批次：**

```sql
SELECT * FROM students_external
WHERE is_graduating = true
  AND graduation_year = (SELECT graduation_year FROM graduation_batches WHERE is_active = true);
```

---

## 五、待宿管系统确认的问题清单

**数据可用性确认：**

1. 宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？
2. 如不包含，能否从教务/人事/学工系统归集后提供？
3. 能否只提供当届毕业生数据（约1000人），还是必须提供全部学生数据？

**字段和标识确认：**

4. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
5. 辅导员工号（`employee_id`）是否全校唯一？是否与统一身份认证、人事系统工号一致？
6. 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？

**多辅导员场景确认：**

7. 是否存在一个班级多个辅导员、代理辅导员、临时负责人或辅导员调岗场景？
8. 班级-辅导员映射变更频率如何？是否能提供当前有效映射和历史有效期？

**对接方式确认：**

9. 优先推荐的对接方式是什么？（DB直连 / API / CSV导入）
10. 各数据源能否提供测试数据、测试环境和字段字典？
11. CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？

**异常处理确认：**

12. 外部系统不可用、数据延迟或查询失败时，业务上允许怎样的人工降级？
13. 是否有统一身份认证或微信绑定前置要求？
14. 是否需要导入手机号/邮箱用于找回密码或二次验证？

**实施保障确认：**

15. 数据提供方能否承诺导出频率、数据更新时间、联系人和故障响应时间？

---

## 六、实施建议

**推荐方案（v2修订）：**

首版采用**CSV/Excel导入 + 宿舍清退API**组合方案：
- 学生、辅导员、班级映射：CSV/Excel批量导入
- 宿舍清退数据：API实时查询
- 后续根据数据变更频率决定是否升级为API/DB同步

**实施路径（v2修订）：**

**阶段1：数据确认（1周）**
1. 向宿管系统提交本需求文档
2. 确认数据可用性、字段定义、对接方式
3. 获取测试数据和字段字典
4. 明确联系人和故障响应方式

**阶段2：CSV导入实现（2周）**
1. 设计三份CSV模板：学生、辅导员、班级-辅导员映射
2. 实现CSV导入功能和校验逻辑
3. 实现staging表和upsert逻辑（v2新增）
4. 实现软停用和重新激活逻辑（v2新增）
5. 实现导入审计日志（v2新增）
6. 生成导入校验报告（成功数、失败数、错误明细）
7. 重点校验：学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射

**阶段3：宿舍清退API对接（1周）**
1. 对接宿管系统宿舍清退API
2. 实现API失败、超时、数据过期的降级处理
3. 测试API异常场景和人工证明流程

**阶段4：上线前验收（1周）**
1. 冻结当届数据批次
2. 完成一次全量导入演练
3. 清零异常清单（无效学号、无效工号、未映射班级）
4. 确认终审管理员配置

**阶段5：上线后优化（按需）**
1. 根据数据变更频率决定是否升级为API/DB同步
2. 根据实际需求决定是否支持多辅导员场景

---

## 七、数据库模型完整清单（v2新增）

### 7.1 修改既有表

**users表调整：**
- `student_id` 改为可空（原为 `UNIQUE NOT NULL`）
- 新增 `employee_id VARCHAR(50)` 字段（可空）
- 新增 `class_id VARCHAR(50)` 字段（可空）
- 修改 `chk_auth_method` 约束：增加 `password_setup_required = true` 条件
- 修改 `chk_user_identity` 约束：
  ```sql
  CONSTRAINT chk_user_identity CHECK (
      (role = 'student' AND student_id IS NOT NULL AND employee_id IS NULL AND class_id IS NOT NULL) OR
      (role IN ('counselor', 'admin') AND employee_id IS NOT NULL AND student_id IS NULL AND class_id IS NULL)
  )
  ```

**applications表调整：**
- 新增 `graduation_batch_id INT` 字段（可选，关联批次）

### 7.2 新增表

**1. students_staging - 学生导入临时表**
```sql
CREATE TABLE students_staging (
    student_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    major VARCHAR(100),
    class_id VARCHAR(50),
    class_name VARCHAR(100),

codex
现有共识与新方案有一个关键张力：此前已经把“学生/辅导员/班级映射”确定为首版 CSV/Excel，只有宿舍清退走实时 API；新方案把用户主数据也放进外部 Provider，需要评估是否会扩大阻塞面。
exec
/bin/bash -lc "rtk nl -ba docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md | sed -n '1,220p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# 数据源需求共识文档
     2	
     3	**文档版本：** v2.0  
     4	**创建时间：** 2026-05-27  
     5	**修订时间：** 2026-05-27  
     6	**目的：** 明确毕业离校系统所需的数据源，提交给宿管系统方反馈
     7	
     8	---
     9	
    10	## 版本变更说明（v1 → v2）
    11	
    12	**主要修正：**
    13	
    14	1. **CSV导入策略**：从"全量覆盖"改为"staging表 + upsert + 软停用"
    15	2. **数据库模型调整**：
    16	   - users表：`student_id`改为可空，新增`employee_id`和`class_id`字段
    17	   - 新增`class_counselor_mapping`表（班级-辅导员映射）
    18	   - 新增`graduation_batches`表（批次配置）
    19	   - 新增`import_logs`表（导入审计）
    20	   - 拆分staging表：`students_staging`、`counselors_staging`、`class_mapping_staging`
    21	3. **认证约束调整**：增加`password_setup_required`支持CSV预导入账号
    22	4. **对接方式调整**：学生/辅导员/班级映射改为"CSV/Excel首版优先"
    23	5. **约束增强**：学生必须有`class_id`，复用`system_configs`表
    24	
    25	**修正依据：**
    26	- Codex第二轮审查（34-codex-second-review-response.md）
    27	- Codex关键问题审查（35-response-to-codex-critical-issues.md）
    28	
    29	---
    30	
    31	## 一、数据源概述
    32	
    33	本系统需要以下数据源支持系统运行：
    34	
    35	| 数据源 | 优先级 | 用途 | 对接方式 |
    36	|--------|--------|------|----------|
    37	| 学生基本信息 | P0 | 创建学生账号、身份识别、班级映射 | **CSV/Excel首版优先** / API或DB增强 |
    38	| 宿舍清退数据 | P0 | 验证学生是否完成宿舍清退 | API优先 / DB备选 / CSV降级 |
    39	| 辅导员基本信息 | P0 | 创建辅导员账号、审批权限 | **CSV/Excel首版优先** / 人事或统一身份API增强 |
    40	| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
    41	| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |
    42	
    43	**对接方式说明：**
    44	- **CSV/Excel首版优先**：首版采用CSV/Excel批量导入，快速上线，后续根据数据变更频率决定是否升级为API/DB
    45	- **API优先**：调用宿管系统提供的API接口（实时校验场景）
    46	- **DB备选**：直接读取宿管系统数据库（需要安全审批和网络配置）
    47	- **CSV降级**：当无法提供API或DB时，通过CSV文件导入
    48	
    49	**首版策略调整理由：**
    50	1. **实施周期**：CSV/Excel导入最快，DB直连需要安全审批和网络配置
    51	2. **变更频率**：账号数据变更频率低（学期级），不需要实时同步
    52	3. **风险控制**：CSV导入可以先验证、再导入、可回滚；DB直连风险更高
    53	
    54	---
    55	
    56	## 二、P0数据源详细要求
    57	
    58	### 2.1 学生基本信息
    59	
    60	**用途：**
    61	- 创建学生账号（用于登录系统）
    62	- 身份识别和验证
    63	- 展示学生院系、专业、班级信息
    64	- 自动分配审批人（根据班级匹配辅导员）
    65	
    66	**必需字段：**
    67	
    68	| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
    69	|---------------|---------------|----------|------|------|------|
    70	| 学号 | student_id | 文本 | 是 | 学生唯一标识 | 2022001 |
    71	| 姓名 | name | 文本 | 是 | 学生姓名 | 张三 |
    72	| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
    73	| 专业 | major | 文本 | 是 | 所属专业 | 计算机科学与技术 |
    74	| 班级ID | class_id | 文本 | 是 | 班级唯一标识（核心键） | CS2022-01 |
    75	| 班级名称 | class_name | 文本 | 否 | 班级名称（用于展示） | 计算机科学与技术2022级1班 |
    76	| 年级 | grade | 整数 | 是 | 入学年份 | 2022 |
    77	| 毕业年份 | graduation_year | 整数 | 是 | 预计毕业年份 | 2026 |
    78	| 是否毕业生 | is_graduating | 布尔 | 是 | 是否为当届毕业生 | true |
    79	
    80	**可选字段：**
    81	
    82	| 字段名（中文） | 字段名（英文） | 数据类型 | 说明 | 示例 |
    83	|---------------|---------------|----------|------|------|
    84	| 手机号 | phone | 文本 | 用于找回密码或二次验证 | 13800138000 |
    85	| 邮箱 | email | 文本 | 用于通知或找回密码 | zhangsan@example.com |
    86	
    87	**字段说明：**
    88	- `class_id`：班级唯一标识，全校唯一，用于映射辅导员（**v2新增必填要求**）
    89	- `class_name`：班级显示名称，可能重复、变更或跨届复用，仅用于展示
    90	- `is_graduating`：标识是否为当届毕业生，`true`表示具备本批次离校申请资格
    91	- `graduation_year`：示例统一为2026（与当前项目日期保持一致）
    92	
    93	**CSV模板示例：**
    94	
    95	```csv
    96	student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
    97	2022001,张三,计算机学院,计算机科学与技术,CS2022-01,计算机科学与技术2022级1班,2022,2026,true,13800138000,zhangsan@example.com
    98	2022002,李四,计算机学院,软件工程,SE2022-01,软件工程2022级1班,2022,2026,true,13800138001,lisi@example.com
    99	```
   100	
   101	**数据范围：**
   102	- 只导入当届毕业生（`is_graduating=true` 且 `graduation_year=2026`）
   103	- 约1000人/届
   104	
   105	---
   106	
   107	### 2.2 宿舍清退数据
   108	
   109	**用途：**
   110	- 验证学生是否完成宿舍清退（提交申请前置条件）
   111	- 展示清退状态和完成时间
   112	
   113	**必需字段：**
   114	
   115	| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
   116	|---------------|---------------|----------|------|------|------|
   117	| 学号 | student_id | 文本 | 是 | 学生学号 | 2022001 |
   118	| 姓名 | name | 文本 | 是 | 学生姓名（用于二次验证） | 张三 |
   119	| 清退状态 | checkout_status | 枚举 | **是** | 清退状态（**v2改为必填**） | completed |
   120	| 清退完成时间 | checkout_date | 日期时间 | 条件必填 | 当status=completed时必填 | 2026-05-20 14:30:00 |
   121	| 数据更新时间 | source_updated_at | 日期时间 | 建议 | 外部系统数据更新时间（**v2新增**） | 2026-05-20 15:00:00 |
   122	
   123	**枚举值说明（v2修订）：**
   124	- `completed`：已完成清退
   125	- `pending`：清退中（已申请但未完成）
   126	- `not_started`：未开始清退
   127	- `unknown`：查询失败或数据不可用（用于API异常时的降级）
   128	
   129	**API响应示例：**
   130	
   131	```json
   132	{
   133	  "student_id": "2022001",
   134	  "name": "张三",
   135	  "checkout_status": "completed",
   136	  "checkout_date": "2026-05-20T14:30:00",
   137	  "source_updated_at": "2026-05-20T15:00:00"
   138	}
   139	```
   140	
   141	**降级处理：**
   142	- API查询失败时，返回 `checkout_status: "unknown"`
   143	- 系统允许学生提交申请，但需上传宿舍清退证明截图
   144	
   145	---
   146	
   147	### 2.3 辅导员基本信息
   148	
   149	**用途：**
   150	- 创建辅导员账号（用于登录系统）
   151	- 审批权限管理
   152	- 班级-辅导员映射
   153	
   154	**必需字段：**
   155	
   156	| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
   157	|---------------|---------------|----------|------|------|------|
   158	| 工号 | employee_id | 文本 | 是 | 辅导员唯一标识（**v2新增**） | T2022001 |
   159	| 姓名 | name | 文本 | 是 | 辅导员姓名 | 王老师 |
   160	| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
   161	| 手机号 | phone | 文本 | 否 | 联系电话 | 13900139000 |
   162	| 邮箱 | email | 文本 | 否 | 联系邮箱 | wanglaoshi@example.com |
   163	| 是否在职 | is_active | 布尔 | 是 | 是否在职（**v2新增**） | true |
   164	
   165	**字段说明：**
   166	- `employee_id`：辅导员工号，必须全校唯一，与统一身份认证、人事系统工号一致
   167	- `is_active`：标识是否在职，`false`时不能登录、不能审批，但历史记录可查询
   168	
   169	**CSV模板示例：**
   170	
   171	```csv
   172	employee_id,name,department,phone,email,is_active
   173	T2022001,王老师,计算机学院,13900139000,wanglaoshi@example.com,true
   174	T2022002,李老师,软件学院,13900139001,lililaoshi@example.com,true
   175	```
   176	
   177	**数据范围：**
   178	- 当前在职辅导员
   179	- 约50人
   180	
   181	**停用规则（v2新增）：**
   182	
   183	| 账号状态 | 登录 | 创建申请 | 审批 | 查看历史 | 接收通知 |
   184	|---------|------|---------|------|---------|---------|
   185	| `is_active=true` | ✅ | ✅ | ✅ | ✅ | ✅ |
   186	| `is_active=false` | ❌ | ❌ | ❌ | ✅（仅自己的） | ❌ |
   187	
   188	---
   189	
   190	### 2.4 班级-辅导员对应关系
   191	
   192	**用途：**
   193	- 学生提交申请时自动分配辅导员审批人
   194	- 支持辅导员变更和历史追溯
   195	
   196	**必需字段：**
   197	
   198	| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
   199	|---------------|---------------|----------|------|------|------|
   200	| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2022-01 |
   201	| 班级名称 | class_name | 文本 | 否 | 班级名称（用于展示） | 计算机科学与技术2022级1班 |
   202	| 辅导员工号 | counselor_employee_id | 文本 | 是 | 辅导员工号 | T2022001 |
   203	
   204	**可选字段（v2新增）：**
   205	
   206	| 字段名（中文） | 字段名（英文） | 数据类型 | 说明 | 示例 |
   207	|---------------|---------------|----------|------|------|
   208	| 生效日期 | effective_from | 日期 | 映射生效日期 | 2026-01-01 |
   209	| 失效日期 | effective_until | 日期 | 映射失效日期，NULL表示长期有效 | NULL |
   210	| 毕业批次ID | graduation_batch_id | 整数 | 关联毕业批次 | 1 |
   211	
   212	**字段说明：**
   213	- `class_id`：班级唯一标识，必须全校唯一，不能重复、变更或跨届复用
   214	- `counselor_employee_id`：必须在辅导员表中存在且 `is_active=true`
   215	- 首版只支持一班一主辅导员，同一 `class_id` 不能出现多次
   216	
   217	**CSV模板示例：**
   218	
   219	```csv
   220	class_id,class_name,counselor_employee_id

exec
/bin/bash -lc "rtk nl -ba docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md | sed -n '1,220p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# API阻塞问题解决方案 - Codex审查请求
     2	
     3	**文档编号：** 37  
     4	**创建日期：** 2026-05-30  
     5	**审查类型：** 技术方案设计  
     6	**优先级：** P0（阻塞开发进度）
     7	
     8	---
     9	
    10	## 一、背景说明
    11	
    12	### 1.1 当前状况
    13	
    14	**项目状态：**
    15	- 设计阶段完成（3轮Codex审查通过）
    16	- 准备开始Phase 1实施
    17	- 遇到外部依赖阻塞
    18	
    19	**阻塞原因：**
    20	- 原设计采用CSV导入用户数据（学生、辅导员、班级）
    21	- 现决定改用API对接方式
    22	- 宿舍管理系统只提供了一个第三方API文档（goliveplus租户用户查询API）
    23	- 该API字段不满足需求（缺少班级、院系、专业、宿舍清退状态等）
    24	
    25	**缺失信息：**
    26	1. 完整的API文档（学生信息、辅导员信息、宿舍清退状态）
    27	2. API认证信息（appKey、appSecret、签名算法）
    28	3. 数据字段映射关系
    29	4. API提供时间不确定
    30	
    31	### 1.2 核心问题
    32	
    33	**如何在外部API信息缺失的情况下，避免开发进度被阻塞？**
    34	
    35	---
    36	
    37	## 二、Claude分析结果
    38	
    39	### 2.1 依赖分析
    40	
    41	**完全不依赖外部API（80%工作量）：**
    42	- Phase 1: 项目初始化（Django、Docker、Celery）
    43	- Phase 2: 用户认证模块（可用Mock数据）
    44	- Phase 3: 离校申请模块
    45	- Phase 4: 审批管理模块
    46	- Phase 5: 附件管理模块
    47	- Phase 6: 通知模块（可Mock微信）
    48	- Phase 8: 前端开发（可用测试AppID）
    49	- Phase 9: 测试（可用Mock数据）
    50	
    51	**完全依赖外部API（20%工作量）：**
    52	- Phase 7: 外部系统集成模块
    53	
    54	### 2.2 推荐方案
    55	
    56	**Mock + 接口抽象 + 种子数据混合方案**
    57	
    58	**核心设计：**
    59	
    60	```python
    61	# 1. 定义抽象接口
    62	class IUserDataProvider(ABC):
    63	    """用户数据提供者接口"""
    64	    @abstractmethod
    65	    def get_students(self, filters: Dict) -> List[Student]:
    66	        """获取学生列表"""
    67	        pass
    68	    
    69	    @abstractmethod
    70	    def get_counselors(self) -> List[Counselor]:
    71	        """获取辅导员列表"""
    72	        pass
    73	    
    74	    @abstractmethod
    75	    def get_class_mapping(self) -> Dict[str, str]:
    76	        """获取班级-辅导员映射"""
    77	        pass
    78	
    79	class IDormCheckoutProvider(ABC):
    80	    """宿舍清退状态提供者接口"""
    81	    @abstractmethod
    82	    def check_status(self, student_id: str) -> CheckoutStatus:
    83	        """查询学生宿舍清退状态"""
    84	        pass
    85	    
    86	    @abstractmethod
    87	    def batch_check_status(self, student_ids: List[str]) -> Dict[str, CheckoutStatus]:
    88	        """批量查询清退状态"""
    89	        pass
    90	
    91	# 2. Mock实现（开发阶段使用）
    92	class MockUserDataProvider(IUserDataProvider):
    93	    def get_students(self, filters):
    94	        # 返回预定义的测试数据
    95	        return [
    96	            Student(
    97	                student_id="2020001",
    98	                name="张三",
    99	                department="计算机学院",
   100	                major="计算机科学与技术",
   101	                class_id="CS2020-01",
   102	                grade=2020,
   103	                graduation_year=2024,
   104	                is_graduating=True
   105	            ),
   106	            # ... 更多测试数据
   107	        ]
   108	    
   109	    def get_counselors(self):
   110	        return [
   111	            Counselor(
   112	                employee_id="T001",
   113	                name="李老师",
   114	                managed_classes=["CS2020-01", "CS2020-02"]
   115	            ),
   116	            # ... 更多测试数据
   117	        ]
   118	
   119	class MockDormCheckoutProvider(IDormCheckoutProvider):
   120	    def check_status(self, student_id: str):
   121	        # 模拟查询逻辑
   122	        return CheckoutStatus(
   123	            student_id=student_id,
   124	            is_checked_out=True,
   125	            checkout_date="2024-06-15",
   126	            dorm_building="1号楼",
   127	            dorm_room="101"
   128	        )
   129	
   130	# 3. 真实实现（API信息到位后实现）
   131	class RealUserDataProvider(IUserDataProvider):
   132	    def __init__(self, api_config: APIConfig):
   133	        self.api_url = api_config.url
   134	        self.app_key = api_config.app_key
   135	        self.app_secret = api_config.app_secret
   136	    
   137	    def get_students(self, filters):
   138	        # 调用真实API
   139	        sign = self._generate_sign()
   140	        response = requests.post(
   141	            self.api_url,
   142	            headers={
   143	                'appKey': self.app_key,
   144	                'timestamp': str(int(time.time())),
   145	                'sign': sign
   146	            },
   147	            data=filters
   148	        )
   149	        # 解析响应并映射到内部数据模型
   150	        return self._parse_students(response.json())
   151	    
   152	    def _generate_sign(self):
   153	        # 实现签名算法（待API文档提供）
   154	        pass
   155	    
   156	    def _parse_students(self, api_data):
   157	        # 将API数据映射到内部Student模型
   158	        pass
   159	
   160	# 4. 配置切换
   161	def get_user_data_provider() -> IUserDataProvider:
   162	    if settings.USE_MOCK_DATA:
   163	        return MockUserDataProvider()
   164	    else:
   165	        return RealUserDataProvider(settings.API_CONFIG)
   166	
   167	def get_dorm_checkout_provider() -> IDormCheckoutProvider:
   168	    if settings.USE_MOCK_DATA:
   169	        return MockDormCheckoutProvider()
   170	    else:
   171	        return RealDormCheckoutProvider(settings.API_CONFIG)
   172	```
   173	
   174	**配置文件：**
   175	
   176	```python
   177	# settings/base.py
   178	USE_MOCK_DATA = env.bool('USE_MOCK_DATA', default=True)
   179	
   180	# settings/dev.py
   181	USE_MOCK_DATA = True  # 开发环境使用Mock
   182	
   183	# settings/prod.py
   184	USE_MOCK_DATA = False  # 生产环境使用真实API
   185	API_CONFIG = {
   186	    'url': env.str('EXTERNAL_API_URL'),
   187	    'app_key': env.str('EXTERNAL_API_KEY'),
   188	    'app_secret': env.str('EXTERNAL_API_SECRET'),
   189	}
   190	```
   191	
   192	### 2.3 实施计划
   193	
   194	**阶段1：不等API（10周）**
   195	
   196	| 周次 | 任务 | 交付物 |
   197	|------|------|--------|
   198	| Week 1-2 | 基础设施 + Mock数据 | Django项目、种子数据（100学生、10辅导员） |
   199	| Week 3-6 | 核心业务逻辑 | 申请、审批、附件、通知模块 |
   200	| Week 7 | 接口抽象层 | Provider接口、MockProvider、缓存框架 |
   201	| Week 8-9 | 前端开发 | React Native、微信小程序（测试AppID） |
   202	| Week 10 | 测试 | 单元测试、集成测试（Mock数据） |
   203	
   204	**交付物：** 可演示版本（使用Mock数据，功能完整）
   205	
   206	**阶段2：API到位后（+3天）**
   207	
   208	| 天数 | 任务 | 交付物 |
   209	|------|------|--------|
   210	| Day 1-2 | 实现真实Provider | RealUserDataProvider、RealDormCheckoutProvider |
   211	| Day 3 | 集成测试 | 真实API测试、数据验证 |
   212	
   213	**交付物：** 生产就绪版本
   214	
   215	### 2.4 优势分析
   216	
   217	**技术优势：**
   218	1. **解耦设计** - 业务逻辑不依赖具体数据源
   219	2. **易于测试** - Mock数据可控，测试稳定
   220	3. **快速迭代** - 不等外部依赖，开发不阻塞

exec
/bin/bash -lc "rtk nl -ba docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md | sed -n '260,520p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   260	- 分配模式：`admin_assignment_mode`（fixed/round_robin/load_balance）
   261	- 首版采用固定分配（fixed），使用第一个可用管理员
   262	
   263	---
   264	
   265	## 三、数据对接方式详细说明
   266	
   267	### 3.1 CSV/Excel导入（首版推荐）
   268	
   269	**适用场景：**
   270	- 学生基本信息
   271	- 辅导员基本信息
   272	- 班级-辅导员对应关系
   273	
   274	**技术要求：**
   275	
   276	**文件格式：**
   277	- 编码：UTF-8（避免中文乱码）
   278	- 格式：CSV或Excel（.xlsx）
   279	- 大小限制：单文件不超过10MB
   280	- 行数限制：单文件不超过10000行
   281	
   282	**导入策略（v2修订）：**
   283	
   284	采用**staging表 + upsert + 软停用**模式：
   285	
   286	1. CSV导入到临时staging表（按类型拆分）
   287	2. 存在则更新，不存在则插入（upsert）
   288	3. 本次未导入的账号标记为 `is_active=false`
   289	4. 下次导入重新出现时自动激活
   290	
   291	**Staging表设计（v2新增）：**
   292	
   293	```sql
   294	-- 学生导入staging表
   295	CREATE TABLE students_staging (
   296	    student_id VARCHAR(50) PRIMARY KEY,
   297	    name VARCHAR(100) NOT NULL,
   298	    department VARCHAR(100),
   299	    major VARCHAR(100),
   300	    class_id VARCHAR(50),
   301	    class_name VARCHAR(100),
   302	    grade INT,
   303	    graduation_year INT,
   304	    is_graduating BOOLEAN,
   305	    phone VARCHAR(20),
   306	    email VARCHAR(100)
   307	);
   308	
   309	-- 辅导员导入staging表
   310	CREATE TABLE counselors_staging (
   311	    employee_id VARCHAR(50) PRIMARY KEY,
   312	    name VARCHAR(100) NOT NULL,
   313	    department VARCHAR(100),
   314	    phone VARCHAR(20),
   315	    email VARCHAR(100)
   316	);
   317	
   318	-- 班级映射导入staging表
   319	CREATE TABLE class_mapping_staging (
   320	    class_id VARCHAR(50) PRIMARY KEY,
   321	    counselor_employee_id VARCHAR(50) NOT NULL
   322	);
   323	```
   324	
   325	**导入流程：**
   326	
   327	```sql
   328	-- 1. 清空staging表
   329	TRUNCATE students_staging;
   330	
   331	-- 2. 导入CSV到staging表
   332	LOAD DATA INFILE 'students.csv' INTO TABLE students_staging;
   333	
   334	-- 3. Upsert到users表
   335	INSERT INTO users (student_id, name, department, class_id, role, is_active, password_setup_required, ...)
   336	SELECT student_id, name, department, class_id, 'student', true, true, ...
   337	FROM students_staging
   338	ON DUPLICATE KEY UPDATE
   339	    name = VALUES(name),
   340	    department = VALUES(department),
   341	    class_id = VALUES(class_id),
   342	    is_active = true,
   343	    updated_at = NOW();
   344	
   345	-- 4. 软停用：本次未导入的学生（使用NOT EXISTS避免NULL问题）
   346	UPDATE users u
   347	SET is_active = false, updated_at = NOW()
   348	WHERE u.role = 'student'
   349	  AND NOT EXISTS (
   350	      SELECT 1 FROM students_staging s
   351	      WHERE s.student_id = u.student_id
   352	  );
   353	```
   354	
   355	**校验要求：**
   356	- 必填字段非空校验
   357	- 学号/工号唯一性校验
   358	- 班级ID存在性校验
   359	- 辅导员工号存在性校验
   360	- 重复数据校验
   361	
   362	**导入审计（v2新增）：**
   363	
   364	```sql
   365	CREATE TABLE import_logs (
   366	    id INT PRIMARY KEY AUTO_INCREMENT,
   367	    import_type ENUM('student', 'counselor', 'class_mapping') NOT NULL,
   368	    file_name VARCHAR(255),
   369	    file_hash VARCHAR(64),                      -- SHA256
   370	    uploaded_by INT,                            -- 操作人user_id
   371	    total_rows INT,
   372	    success_rows INT,
   373	    failed_rows INT,
   374	    new_rows INT,                               -- 新增
   375	    updated_rows INT,                           -- 更新
   376	    disabled_rows INT,                          -- 软停用
   377	    error_details TEXT,                         -- JSON格式错误明细
   378	    import_status ENUM('pending', 'success', 'partial', 'failed'),
   379	    started_at TIMESTAMP,
   380	    completed_at TIMESTAMP,
   381	    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   382	    
   383	    FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE SET NULL
   384	);
   385	```
   386	
   387	**错误报告示例：**
   388	
   389	```json
   390	{
   391	  "errors": [
   392	    {"row": 5, "field": "student_id", "error": "学号重复"},
   393	    {"row": 12, "field": "class_id", "error": "班级ID不存在"}
   394	  ],
   395	  "warnings": [
   396	    {"row": 8, "field": "phone", "error": "手机号格式不正确"}
   397	  ]
   398	}
   399	```
   400	
   401	---
   402	
   403	### 3.2 API接口（实时校验场景）
   404	
   405	**适用场景：**
   406	- 宿舍清退数据（实时校验）
   407	
   408	**技术要求：**
   409	
   410	**接口规范：**
   411	- 协议：HTTP/HTTPS
   412	- 方法：GET或POST
   413	- 认证：API Key或OAuth2
   414	- 响应格式：JSON
   415	- 超时时间：5秒
   416	
   417	**分页支持：**
   418	- 每页最多100条
   419	- 支持 `page`/`page_size` 参数
   420	
   421	**增量同步：**
   422	- 支持 `updated_after` 参数
   423	- 只返回指定时间后更新的数据
   424	
   425	**错误码规范：**
   426	- 200：成功
   427	- 400：参数错误
   428	- 401：认证失败
   429	- 404：数据不存在
   430	- 500：服务器错误
   431	
   432	**限流策略：**
   433	- 每分钟最多60次请求
   434	
   435	**重试机制：**
   436	- 失败后指数退避重试，最多3次
   437	
   438	**幂等性：**
   439	- 同一请求多次调用结果一致
   440	
   441	---
   442	
   443	### 3.3 数据库直连（后续增强）
   444	
   445	**适用场景：**
   446	- 数据变更频率高时升级使用
   447	
   448	**技术要求：**
   449	
   450	**安全边界：**
   451	- 只读账号，不得有写权限
   452	- 使用只读视图或同步库，不直接访问生产业务表
   453	- IP白名单限制，只允许应用服务器访问
   454	
   455	**连接池配置：**
   456	- 最大连接数：5
   457	- 超时时间：30秒
   458	- 重试策略：失败后等待5秒重试
   459	
   460	**支持数据库：**
   461	- MySQL 5.7+
   462	- SQL Server 2016+
   463	- Oracle 11g+
   464	- PostgreSQL 10+
   465	
   466	---
   467	
   468	## 四、数据量估算
   469	
   470	**明确说明（v2修订）：**
   471	
   472	| 数据项 | 首版范围 | 容量设计 | 说明 |
   473	|--------|----------|----------|------|
   474	| 学生账号 | 当届毕业生 | 1000人/届 | 只导入当届（`is_graduating=true` 且 `graduation_year=2026`） |
   475	| 系统容量 | 支持多届历史 | 10000人 | 数据库设计按10000人容量 |
   476	| 辅导员账号 | 当前在职 | 50人 | 离职辅导员标记 `is_active=false` |
   477	| 班级映射 | 当届有效映射 | 50-100条 | 首版不考虑历史有效期 |
   478	| 学工部管理员 | 当前在职 | 5人 | 手动创建 |
   479	| 申请记录 | 当届申请 | 1000条/届 | 每个学生最多1个进行中申请 |
   480	
   481	**批次配置（v2新增）：**
   482	
   483	```sql
   484	CREATE TABLE graduation_batches (
   485	    id INT PRIMARY KEY AUTO_INCREMENT,
   486	    batch_name VARCHAR(100) NOT NULL,           -- 如 "2026届本科毕业生"
   487	    graduation_year INT NOT NULL,               -- 2026
   488	    is_active BOOLEAN DEFAULT true,             -- 当前批次（仅一个）
   489	    application_start_date DATE,                -- 申请开放时间
   490	    application_end_date DATE,                  -- 申请截止时间
   491	    planned_leave_date_start DATE,              -- 允许的最早离校日期
   492	    planned_leave_date_end DATE,                -- 允许的最晚离校日期
   493	    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   494	    
   495	    -- 约束：仅一个当前批次
   496	    UNIQUE KEY uk_active_batch (is_active) WHERE is_active = true
   497	);
   498	```
   499	
   500	**学生导入时只导入当前批次：**
   501	
   502	```sql
   503	SELECT * FROM students_external
   504	WHERE is_graduating = true
   505	  AND graduation_year = (SELECT graduation_year FROM graduation_batches WHERE is_active = true);
   506	```
   507	
   508	---
   509	
   510	## 五、待宿管系统确认的问题清单
   511	
   512	**数据可用性确认：**
   513	
   514	1. 宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？
   515	2. 如不包含，能否从教务/人事/学工系统归集后提供？
   516	3. 能否只提供当届毕业生数据（约1000人），还是必须提供全部学生数据？
   517	
   518	**字段和标识确认：**
   519	
   520	4. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？

exec
/bin/bash -lc "rtk nl -ba docs/design/2026-05-27-system-design.md | sed -n '1580,1745p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
  1580	```
  1581	
  1582	**超时通知：**
  1583	- 第1次：办理时限到期时通知审批人
  1584	- 第2次：超时4小时后通知审批人上级
  1585	- 第3次：超时8小时后通知系统管理员
  1586	
  1587	**降级策略：**
  1588	- 外部系统（宿舍管理系统）不可用时，允许手动上传证明文件
  1589	- 审批人可选择"跳过验证"并备注原因
  1590	- 系统记录降级操作日志
  1591	
  1592	---
  1593	## 6. 外部系统集成设计
  1594	
  1595	### 6.1 集成策略（Round 6共识）
  1596	
  1597	**本项目数据库：** PostgreSQL（单一数据库）
  1598	
  1599	**外部系统对接：** 支持多种数据库（MySQL/SQL Server/Oracle）
  1600	
  1601	**集成方案：**
  1602	1. **API集成（唯一方案）**：REST API对接，松耦合
  1603	2. **降级策略**：外部系统不可用时，允许手动上传证明文件
  1604	
  1605	### 6.2 宿舍管理系统对接
  1606	
  1607	**集成目的：**
  1608	验证学生宿舍清退状态，确保离校手续真实完成。
  1609	
  1610	**方案1：API集成（推荐）**
  1611	
  1612	**接口协议：**
  1613	```
  1614	HTTP REST API
  1615	认证方式：API Key
  1616	数据格式：JSON
  1617	超时时间：5秒
  1618	```
  1619	
  1620	**接口定义：**
  1621	```python
  1622	# 查询宿舍清退状态
  1623	GET /api/dorm/clearance/status
  1624	Headers:
  1625	  X-API-Key: {api_key}
  1626	Params:
  1627	  student_id: 2020001
  1628	
  1629	Response:
  1630	{
  1631	  "code": 200,
  1632	  "data": {
  1633	    "student_id": "2020001",
  1634	    "name": "张三",
  1635	    "class_name": "计算机2020级1班",
  1636	    "dorm_building": "1号楼",
  1637	    "dorm_room": "101",
  1638	    "bed_number": "1",
  1639	    "is_checked_out": true,
  1640	    "checkout_date": "2026-05-25",
  1641	    "checkout_status": "completed"
  1642	  }
  1643	}
  1644	```
  1645	
  1646	### 6.3 接口实现
  1647	
  1648	**方案1：API客户端（推荐）**
  1649	```python
  1650	# apps/integrations/dorm_system.py
  1651	class DormSystemClient:
  1652	    def __init__(self):
  1653	        config = SystemConfig.objects.get(config_key='dorm_api_url')
  1654	        self.base_url = config.config_value
  1655	        self.api_key = SystemConfig.objects.get(config_key='dorm_api_key').get_decrypted_value()
  1656	    
  1657	    def get_checkout_status(self, student_id):
  1658	        response = requests.get(
  1659	            f'{self.base_url}/api/students/{student_id}/checkout',
  1660	            headers={'X-API-Key': self.api_key},
  1661	            timeout=5
  1662	        )
  1663	        return response.json()
  1664	```
  1665	
  1666	### 6.4 配置存储
  1667	
  1668	**system_configs配置项：**
  1669	```sql
  1670	-- API集成配置
  1671	INSERT INTO system_configs (config_key, config_value, config_type, is_encrypted) VALUES
  1672	('dorm_integration_type', 'api', 'integration', FALSE),
  1673	('dorm_api_url', 'https://dorm.university.edu/api', 'integration', FALSE),
  1674	('dorm_api_key', 'encrypted_key_here', 'integration', TRUE);
  1675	```
  1676	        self.api_key = settings.DORM_SYSTEM_API_KEY
  1677	        self.api_secret = settings.DORM_SYSTEM_API_SECRET
  1678	    
  1679	    def verify_clearance(self, student_id):
  1680	        try:
  1681	            response = requests.get(
  1682	                f"{self.api_url}/clearance/status",
  1683	                params={"student_id": student_id},
  1684	                headers={
  1685	                    "X-API-Key": self.api_key,
  1686	                    "X-API-Secret": self.api_secret
  1687	                },
  1688	                timeout=5
  1689	            )
  1690	            return response.json()
  1691	        except requests.Timeout:
  1692	            raise ExternalSystemTimeout("宿舍系统超时")
  1693	        except Exception as e:
  1694	            raise ExternalSystemError(f"宿舍系统错误: {str(e)}")
  1695	```
  1696	
  1697	### 6.3 错误处理和重试机制
  1698	
  1699	**错误分类：**
  1700	```python
  1701	class ExternalSystemError(Exception):
  1702	    """外部系统基础异常"""
  1703	    pass
  1704	
  1705	class ExternalSystemTimeout(ExternalSystemError):
  1706	    """超时异常 - 可重试"""
  1707	    pass
  1708	
  1709	class ExternalSystemUnavailable(ExternalSystemError):
  1710	    """服务不可用 - 可重试"""
  1711	    pass
  1712	
  1713	class ExternalSystemAuthError(ExternalSystemError):
  1714	    """认证失败 - 不可重试"""
  1715	    pass
  1716	```
  1717	
  1718	**重试策略：**
  1719	```python
  1720	from tenacity import retry, stop_after_attempt, wait_exponential
  1721	
  1722	@retry(
  1723	    stop=stop_after_attempt(3),  # 最多重试3次
  1724	    wait=wait_exponential(multiplier=1, min=2, max=10),  # 指数退避
  1725	    retry=retry_if_exception_type((ExternalSystemTimeout, ExternalSystemUnavailable))
  1726	)
  1727	def verify_dorm_clearance(student_id):
  1728	    plugin = DormSystemPlugin()
  1729	    return plugin.verify_clearance(student_id)
  1730	```
  1731	
  1732	**降级策略：**
  1733	- 外部系统不可用时，允许手动上传证明文件
  1734	- 审批人可选择"跳过验证"并备注原因
  1735	- 系统记录降级操作日志
  1736	
  1737	---
  1738	
  1739	## 7. 部署架构设计
  1740	
  1741	### 7.1 Docker Compose配置
  1742	
  1743	**服务清单：**
  1744	```yaml
  1745	services:

exec
/bin/bash -lc "rtk nl -ba docs/design/2026-05-27-system-design.md | sed -n '2430,2495p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
  2430	
  2431	### 9.2 缓存策略
  2432	
  2433	**Redis缓存层级：**
  2434	```python
  2435	# L1: 用户信息缓存（30分钟）
  2436	cache.set(f'user:{user_id}', user_data, 1800)
  2437	
  2438	# L2: 申请状态缓存（5分钟）
  2439	cache.set(f'app:{app_id}:status', status, 300)
  2440	
  2441	# L3: 待审批数量缓存（1分钟）
  2442	cache.set(f'pending:count:{user_id}', count, 60)
  2443	```
  2444	
  2445	**缓存更新策略：**
  2446	- 写入时主动失效
  2447	- 定时刷新热点数据
  2448	- 缓存穿透：空值缓存
  2449	- 缓存雪崩：随机过期时间
  2450	
  2451	**缓存失效规则：**
  2452	```python
  2453	def invalidate_application_cache(application_id):
  2454	    """申请状态变更时失效相关缓存"""
  2455	    cache.delete(f'app:{application_id}:status')
  2456	    cache.delete(f'app:{application_id}:detail')
  2457	    
  2458	    # 失效审批人的待审批数量缓存
  2459	    app = Application.objects.get(id=application_id)
  2460	    if app.current_approver_id:
  2461	        cache.delete(f'pending:count:{app.current_approver_id}')
  2462	    
  2463	    # 失效学生的申请列表缓存
  2464	    cache.delete(f'student:{app.student_id}:applications')
  2465	
  2466	def invalidate_user_cache(user_id):
  2467	    """用户信息变更时失效缓存"""
  2468	    cache.delete(f'user:{user_id}')
  2469	    cache.delete(f'user:{user_id}:permissions')
  2470	
  2471	# 在模型保存时自动失效
  2472	from django.db.models.signals import post_save
  2473	
  2474	@receiver(post_save, sender=Application)
  2475	def application_saved(sender, instance, **kwargs):
  2476	    invalidate_application_cache(instance.id)
  2477	```
  2478	
  2479	**不缓存的内容：**
  2480	- 权限决策（每次实时检查）
  2481	- 审批操作（必须实时）
  2482	- 敏感配置（加密配置）
  2483	
  2484	**Django缓存配置：**
  2485	```python
  2486	CACHES = {
  2487	    'default': {
  2488	        'BACKEND': 'django_redis.cache.RedisCache',
  2489	        'LOCATION': 'redis://redis:6379/1',
  2490	        'OPTIONS': {
  2491	            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
  2492	            'CONNECTION_POOL_KWARGS': {'max_connections': 50}
  2493	        }
  2494	    }
  2495	}

exec
/bin/bash -lc "rtk nl -ba docs/数据对接说明文档.md | sed -n '1,120p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# 毕业生离校申请审批系统 - 数据对接说明文档
     2	
     3	**文档版本：** v2.0  
     4	**发布日期：** 2026-05-27  
     5	**目标用户：** 宿舍管理系统管理员、数据对接负责人
     6	
     7	---
     8	
     9	## 一、对接概述
    10	
    11	### 1.1 对接目的
    12	
    13	本系统需要与学校现有的**宿舍管理系统**进行数据对接，获取以下数据：
    14	
    15	1. **学生基本信息** - 创建学生账号，用于登录和身份识别
    16	2. **辅导员基本信息** - 创建辅导员账号，用于审批管理
    17	3. **班级-辅导员对应关系** - 自动分配审批人
    18	4. **宿舍清退数据** - 验证学生是否完成宿舍清退
    19	
    20	### 1.2 对接方式
    21	
    22	本系统支持两种对接方式：
    23	
    24	| 数据源 | 对接方式 | 说明 |
    25	|--------|---------|------|
    26	| 学生基本信息 | **CSV/Excel文件导入** | 首版推荐，快速上线 |
    27	| 辅导员基本信息 | **CSV/Excel文件导入** | 首版推荐，快速上线 |
    28	| 班级-辅导员对应关系 | **CSV/Excel文件导入** | 首版推荐，需强校验 |
    29	| 宿舍清退数据 | **API接口实时查询** | 需要实时验证清退状态 |
    30	
    31	**为什么推荐CSV/Excel导入？**
    32	- 实施周期短：无需开发API，1-2周即可上线
    33	- 风险可控：可以先验证、再导入、可回滚
    34	- 变更频率低：学生和辅导员信息每学期更新1-2次
    35	- 后续可升级：如果数据变更频繁，可升级为API/数据库同步
    36	
    37	### 1.3 对接时间表
    38	
    39	| 阶段 | 时间 | 任务 |
    40	|------|------|------|
    41	| 数据确认 | 第1周 | 确认数据可用性、字段定义、CSV模板 |
    42	| CSV导入开发 | 第2-3周 | 开发CSV导入功能、校验逻辑、审计日志 |
    43	| 宿舍清退API对接 | 第4周 | 对接宿舍清退API、测试异常场景 |
    44	| 上线验收 | 第5周 | 全量导入演练、功能测试、正式上线 |
    45	
    46	---
    47	
    48	## 二、学生基本信息（CSV导入）
    49	
    50	### 2.1 数据用途
    51	
    52	- 创建学生账号（用于登录系统）
    53	- 身份识别和验证
    54	- 展示学生院系、专业、班级信息
    55	- 自动分配审批人（根据班级匹配辅导员）
    56	
    57	### 2.2 必需字段
    58	
    59	| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
    60	|---------------|---------------|----------|------|------|------|
    61	| 学号 | student_id | 文本 | 是 | 学生唯一标识 | 2022001 |
    62	| 姓名 | name | 文本 | 是 | 学生姓名 | 张三 |
    63	| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
    64	| 专业 | major | 文本 | 是 | 所属专业 | 计算机科学与技术 |
    65	| 班级ID | class_id | 文本 | 是 | 班级唯一标识（重要） | CS2022-01 |
    66	| 班级名称 | class_name | 文本 | 否 | 班级名称（用于展示） | 计算机科学与技术2022级1班 |
    67	| 年级 | grade | 整数 | 是 | 入学年份 | 2022 |
    68	| 毕业年份 | graduation_year | 整数 | 是 | 预计毕业年份 | 2026 |
    69	| 是否毕业生 | is_graduating | 布尔 | 是 | 是否为当届毕业生 | true |
    70	
    71	**可选字段：**
    72	
    73	| 字段名（中文） | 字段名（英文） | 数据类型 | 说明 | 示例 |
    74	|---------------|---------------|----------|------|------|
    75	| 手机号 | phone | 文本 | 用于找回密码 | 13800138000 |
    76	| 邮箱 | email | 文本 | 用于通知 | zhangsan@example.com |
    77	
    78	**重要说明：**
    79	- `class_id` 必须全校唯一，用于映射辅导员，不能重复、变更或跨届复用
    80	- `class_name` 仅用于展示，可以重复
    81	- `is_graduating=true` 表示具备本批次离校申请资格
    82	- 只需导入当届毕业生（约1000人），不需要全部学生
    83	
    84	### 2.3 CSV模板
    85	
    86	**文件名：** `学生基本信息导入模板.csv`
    87	
    88	**文件编码：** UTF-8（避免中文乱码）
    89	
    90	**模板内容：**
    91	```csv
    92	student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
    93	2022001,张三,计算机学院,计算机科学与技术,CS2022-01,计算机科学与技术2022级1班,2022,2026,true,13800138000,zhangsan@example.com
    94	2022002,李四,计算机学院,软件工程,SE2022-01,软件工程2022级1班,2022,2026,true,13800138001,lisi@example.com
    95	```
    96	
    97	**注意事项：**
    98	- 第一行必须是字段名（英文）
    99	- 布尔值用 `true` 或 `false`
   100	- 文本字段如果包含逗号，需要用双引号包裹
   101	- 不要使用Excel的"另存为CSV"，建议使用专业工具导出UTF-8编码
   102	
   103	### 2.4 导入流程
   104	
   105	**步骤1：准备CSV文件**
   106	- 从教务系统或学工系统导出当届毕业生数据
   107	- 按照模板格式整理数据
   108	- 确保 `class_id` 字段填写正确（后续用于匹配辅导员）
   109	
   110	**步骤2：上传CSV文件**
   111	- 登录系统管理后台
   112	- 进入"数据导入"模块
   113	- 选择"学生基本信息导入"
   114	- 上传CSV文件
   115	
   116	**步骤3：系统自动校验**
   117	- 必填字段非空校验
   118	- 学号唯一性校验
   119	- 班级ID存在性校验（需要先导入班级映射）
   120	- 数据格式校验

exec
/bin/bash -lc "rtk nl -ba docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md | sed -n '520,620p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   520	4. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
   521	5. 辅导员工号（`employee_id`）是否全校唯一？是否与统一身份认证、人事系统工号一致？
   522	6. 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
   523	
   524	**多辅导员场景确认：**
   525	
   526	7. 是否存在一个班级多个辅导员、代理辅导员、临时负责人或辅导员调岗场景？
   527	8. 班级-辅导员映射变更频率如何？是否能提供当前有效映射和历史有效期？
   528	
   529	**对接方式确认：**
   530	
   531	9. 优先推荐的对接方式是什么？（DB直连 / API / CSV导入）
   532	10. 各数据源能否提供测试数据、测试环境和字段字典？
   533	11. CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
   534	
   535	**异常处理确认：**
   536	
   537	12. 外部系统不可用、数据延迟或查询失败时，业务上允许怎样的人工降级？
   538	13. 是否有统一身份认证或微信绑定前置要求？
   539	14. 是否需要导入手机号/邮箱用于找回密码或二次验证？
   540	
   541	**实施保障确认：**
   542	
   543	15. 数据提供方能否承诺导出频率、数据更新时间、联系人和故障响应时间？
   544	
   545	---
   546	
   547	## 六、实施建议
   548	
   549	**推荐方案（v2修订）：**
   550	
   551	首版采用**CSV/Excel导入 + 宿舍清退API**组合方案：
   552	- 学生、辅导员、班级映射：CSV/Excel批量导入
   553	- 宿舍清退数据：API实时查询
   554	- 后续根据数据变更频率决定是否升级为API/DB同步
   555	
   556	**实施路径（v2修订）：**
   557	
   558	**阶段1：数据确认（1周）**
   559	1. 向宿管系统提交本需求文档
   560	2. 确认数据可用性、字段定义、对接方式
   561	3. 获取测试数据和字段字典
   562	4. 明确联系人和故障响应方式
   563	
   564	**阶段2：CSV导入实现（2周）**
   565	1. 设计三份CSV模板：学生、辅导员、班级-辅导员映射
   566	2. 实现CSV导入功能和校验逻辑
   567	3. 实现staging表和upsert逻辑（v2新增）
   568	4. 实现软停用和重新激活逻辑（v2新增）
   569	5. 实现导入审计日志（v2新增）
   570	6. 生成导入校验报告（成功数、失败数、错误明细）
   571	7. 重点校验：学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射
   572	
   573	**阶段3：宿舍清退API对接（1周）**
   574	1. 对接宿管系统宿舍清退API
   575	2. 实现API失败、超时、数据过期的降级处理
   576	3. 测试API异常场景和人工证明流程
   577	
   578	**阶段4：上线前验收（1周）**
   579	1. 冻结当届数据批次
   580	2. 完成一次全量导入演练
   581	3. 清零异常清单（无效学号、无效工号、未映射班级）
   582	4. 确认终审管理员配置
   583	
   584	**阶段5：上线后优化（按需）**
   585	1. 根据数据变更频率决定是否升级为API/DB同步
   586	2. 根据实际需求决定是否支持多辅导员场景
   587	
   588	---
   589	
   590	## 七、数据库模型完整清单（v2新增）
   591	
   592	### 7.1 修改既有表
   593	
   594	**users表调整：**
   595	- `student_id` 改为可空（原为 `UNIQUE NOT NULL`）
   596	- 新增 `employee_id VARCHAR(50)` 字段（可空）
   597	- 新增 `class_id VARCHAR(50)` 字段（可空）
   598	- 修改 `chk_auth_method` 约束：增加 `password_setup_required = true` 条件
   599	- 修改 `chk_user_identity` 约束：
   600	  ```sql
   601	  CONSTRAINT chk_user_identity CHECK (
   602	      (role = 'student' AND student_id IS NOT NULL AND employee_id IS NULL AND class_id IS NOT NULL) OR
   603	      (role IN ('counselor', 'admin') AND employee_id IS NOT NULL AND student_id IS NULL AND class_id IS NULL)
   604	  )
   605	  ```
   606	
   607	**applications表调整：**
   608	- 新增 `graduation_batch_id INT` 字段（可选，关联批次）
   609	
   610	### 7.2 新增表
   611	
   612	**1. students_staging - 学生导入临时表**
   613	```sql
   614	CREATE TABLE students_staging (
   615	    student_id VARCHAR(50) PRIMARY KEY,
   616	    name VARCHAR(100) NOT NULL,
   617	    department VARCHAR(100),
   618	    major VARCHAR(100),
   619	    class_id VARCHAR(50),
   620	    class_name VARCHAR(100),

exec
/bin/bash -lc "rtk nl -ba docs/数据对接说明文档.md | sed -n '240,360p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   240	- 未匹配班级：学生表中的class_id在映射表中不存在
   241	- 未匹配辅导员：映射表中的工号在辅导员表中不存在
   242	- 重复映射：同一class_id出现多次
   243	- 无审批人的学生数：有多少学生没有对应的辅导员
   244	
   245	---
   246	
   247	## 五、宿舍清退数据（API接口）
   248	
   249	### 5.1 数据用途
   250	
   251	学生提交离校申请时，系统实时查询宿舍清退状态：
   252	- 已完成清退：允许提交申请
   253	- 未完成清退：提示学生先完成宿舍清退手续
   254	- 查询失败：允许学生上传宿舍清退证明截图
   255	
   256	### 5.2 接口规范
   257	
   258	**接口名称：** 查询学生宿舍清退状态
   259	
   260	**请求方式：** GET 或 POST
   261	
   262	**请求地址：** `http://宿舍管理系统域名/api/dorm/checkout/status`
   263	
   264	**认证方式：** API Key + IP白名单
   265	
   266	### 5.3 请求参数
   267	
   268	| 参数名 | 类型 | 必填 | 说明 | 示例 |
   269	|--------|------|------|------|------|
   270	| student_id | String | 是 | 学号 | "2022001" |
   271	| name | String | 是 | 姓名（用于验证） | "张三" |
   272	
   273	**请求示例（GET）：**
   274	```
   275	GET /api/dorm/checkout/status?student_id=2022001&name=张三
   276	Host: dorm.example.com
   277	Authorization: Bearer YOUR_API_KEY
   278	```
   279	
   280	### 5.4 响应参数
   281	
   282	**成功响应（HTTP 200）：**
   283	
   284	```json
   285	{
   286	  "code": 0,
   287	  "message": "查询成功",
   288	  "data": {
   289	    "student_id": "2022001",
   290	    "name": "张三",
   291	    "checkout_status": "completed",
   292	    "checkout_date": "2026-05-20T14:30:00",
   293	    "source_updated_at": "2026-05-20T15:00:00"
   294	  }
   295	}
   296	```
   297	
   298	**响应字段说明：**
   299	
   300	| 字段名 | 类型 | 必填 | 说明 | 示例 |
   301	|--------|------|------|------|------|
   302	| checkout_status | String | 是 | 清退状态 | "completed" |
   303	| checkout_date | String | 条件必填 | 清退完成时间（status=completed时必填） | "2026-05-20T14:30:00" |
   304	| source_updated_at | String | 建议 | 数据更新时间 | "2026-05-20T15:00:00" |
   305	
   306	**清退状态枚举值：**
   307	- `completed` - 已完成清退
   308	- `pending` - 清退中（已申请但未完成）
   309	- `not_started` - 未开始清退
   310	- `unknown` - 查询失败或数据不可用
   311	
   312	### 5.5 错误响应
   313	
   314	**学号不存在（HTTP 404）：**
   315	```json
   316	{
   317	  "code": 1001,
   318	  "message": "学号不存在",
   319	  "data": null
   320	}
   321	```
   322	
   323	**参数错误（HTTP 400）：**
   324	```json
   325	{
   326	  "code": 1002,
   327	  "message": "参数缺失：student_id",
   328	  "data": null
   329	}
   330	```
   331	
   332	**服务器错误（HTTP 500）：**
   333	```json
   334	{
   335	  "code": 5000,
   336	  "message": "服务器内部错误",
   337	  "data": null
   338	}
   339	```
   340	
   341	### 5.6 技术要求
   342	
   343	**性能要求：**
   344	- 响应时间：< 2秒
   345	- 超时时间：5秒
   346	- 重试次数：失败后重试3次
   347	
   348	**限流要求：**
   349	- 每分钟最多60次请求
   350	- 超过限流返回HTTP 429
   351	
   352	**降级处理：**
   353	- API查询失败时，返回 `checkout_status: "unknown"`
   354	- 允许学生上传宿舍清退证明截图
   355	- 管理员审核通过后允许提交
   356	
   357	---
   358	
   359	## 六、技术要求和规范
   360	

exec
/bin/bash -lc "rtk nl -ba docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md | sed -n '220,380p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   220	3. **快速迭代** - 不等外部依赖，开发不阻塞
   221	4. **低风险切换** - 配置开关，无需改代码
   222	5. **符合SOLID** - 依赖倒置原则，面向接口编程
   223	
   224	**项目管理优势：**
   225	1. **进度可控** - 80%工作不受阻塞
   226	2. **分阶段交付** - 10周可交付演示版
   227	3. **风险隔离** - API问题不影响核心功能
   228	4. **灵活应对** - API延期也不影响整体进度
   229	
   230	### 2.5 风险评估
   231	
   232	**低风险：**
   233	- 真实API字段与Mock不一致 → 调整适配器即可（1-2天）
   234	- 真实API性能问题 → 已有缓存和重试机制
   235	
   236	**中风险：**
   237	- 真实API数据结构差异大 → 可能需要调整数据模型（2-3天）
   238	- API认证复杂度超预期 → 可能需要额外调试时间（1-2天）
   239	
   240	**缓解措施：**
   241	1. 接口设计参考行业标准（RESTful、OAuth2等）
   242	2. 预留扩展字段，避免硬编码
   243	3. 完善的错误处理和日志记录
   244	4. 充分的单元测试覆盖
   245	
   246	---
   247	
   248	## 三、请Codex审查的问题
   249	
   250	### 3.1 技术方案合理性
   251	
   252	**问题1：Mock + 接口抽象方案是否合理？**
   253	- 这种设计是否符合最佳实践？
   254	- 是否有更好的解耦方案？
   255	- 接口定义是否完善？
   256	
   257	**问题2：Provider接口设计是否合理？**
   258	- `IUserDataProvider` 和 `IDormCheckoutProvider` 接口是否完整？
   259	- 是否需要增加其他方法？
   260	- 方法签名是否合理？
   261	
   262	**问题3：配置切换机制是否合理？**
   263	- 使用环境变量 `USE_MOCK_DATA` 切换是否合适？
   264	- 是否需要更细粒度的控制（如部分Mock、部分Real）？
   265	
   266	### 3.2 风险评估
   267	
   268	**问题4：真实API到位后的集成风险有多大？**
   269	- 3天工期评估是否合理？
   270	- 可能遇到哪些意外情况？
   271	- 如何降低集成风险？
   272	
   273	**问题5：数据映射不一致的应对策略？**
   274	- 如果真实API字段与预期差异很大怎么办？
   275	- 是否需要预留更多的适配层？
   276	- 数据转换逻辑应该放在哪一层？
   277	
   278	**问题6：Mock数据的真实性问题？**
   279	- Mock数据是否足够真实？
   280	- 是否会遗漏边界情况？
   281	- 如何保证Mock数据与真实数据的一致性？
   282	
   283	### 3.3 工期评估
   284	
   285	**问题7：10周 + 3天工期是否合理？**
   286	- 各阶段工期评估是否准确？
   287	- 哪些环节可能延期？
   288	- 是否需要增加缓冲时间？
   289	
   290	**问题8：并行开发的可行性？**
   291	- 80%工作不依赖API的判断是否准确？
   292	- 是否有隐藏的依赖关系？
   293	- 团队规模对并行开发的影响？
   294	
   295	### 3.4 架构设计
   296	
   297	**问题9：缓存策略是否合理？**
   298	- Redis缓存TTL设置（用户信息1小时、清退状态10分钟）是否合适？
   299	- 缓存更新策略是否完善？
   300	- 缓存失效处理是否考虑周全？
   301	
   302	**问题10：错误处理和降级策略？**
   303	- API不可用时的降级方案是否完善？
   304	- 重试机制是否合理？
   305	- 错误日志和监控是否充分？
   306	
   307	### 3.5 测试策略
   308	
   309	**问题11：Mock数据测试覆盖度？**
   310	- 使用Mock数据能否充分测试业务逻辑？
   311	- 哪些场景必须用真实API测试？
   312	- 如何保证测试的有效性？
   313	
   314	**问题12：真实API测试重点？**
   315	- API到位后应该重点测试哪些方面？
   316	- 如何设计集成测试用例？
   317	- 性能测试如何进行？
   318	
   319	### 3.6 替代方案
   320	
   321	**问题13：是否有更好的方案？**
   322	- 除了Mock + 接口抽象，是否有其他方案？
   323	- 是否可以考虑使用Stub、Fake等其他测试替身？
   324	- 是否可以考虑Contract Testing（契约测试）？
   325	
   326	**问题14：是否需要API网关或BFF层？**
   327	- 是否需要在中间增加一层API网关？
   328	- BFF（Backend For Frontend）模式是否适用？
   329	- 这样做的利弊是什么？
   330	
   331	---
   332	
   333	## 四、期望的审查输出
   334	
   335	### 4.1 技术方案评估
   336	
   337	**请评估：**
   338	1. Mock + 接口抽象方案的合理性（1-10分）
   339	2. 方案的优缺点分析
   340	3. 是否有致命缺陷或重大风险
   341	4. 改进建议
   342	
   343	### 4.2 风险识别
   344	
   345	**请识别：**
   346	1. 方案中可能遗漏的风险点
   347	2. 风险等级评估（P0/P1/P2）
   348	3. 风险缓解措施建议
   349	
   350	### 4.3 工期评估
   351	
   352	**请评估：**
   353	1. 10周 + 3天工期是否合理
   354	2. 各阶段工期是否需要调整
   355	3. 关键路径和瓶颈分析
   356	
   357	### 4.4 架构改进建议
   358	
   359	**请提供：**
   360	1. 接口设计改进建议
   361	2. 缓存策略优化建议
   362	3. 错误处理和降级策略改进
   363	4. 测试策略改进
   364	
   365	### 4.5 替代方案
   366	
   367	**如果当前方案不合理，请提供：**
   368	1. 替代方案描述
   369	2. 替代方案的优缺点
   370	3. 实施难度和工期评估
   371	
   372	---
   373	
   374	## 五、审查范围
   375	
   376	**本次审查聚焦：**
   377	1. ✓ 技术方案的合理性和可行性
   378	2. ✓ 风险识别和缓解措施
   379	3. ✓ 工期评估的准确性
   380	4. ✓ 架构设计的完善性

codex
**结论**

Mock + 接口抽象方向是合理的，但当前方案不能按原文直接通过。评分：**7/10**。核心问题不是“能不能 Mock”，而是方案把“用户主数据 API 化”当成默认终局，偏离了此前已达成的首版共识：学生、辅导员、班级映射应优先走 CSV/Excel 导入，宿舍清退才是实时 API。现有共识明确写了学生/辅导员/班级映射首版 CSV，宿舍清退 API 实时查询：[31-data-source-requirements-consensus-v2.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:35)、[数据对接说明文档.md](/home/caohui/projects/graduation-leave-system/docs/数据对接说明文档.md:24)。

**主要问题**

P0：`RealUserDataProvider` 不应成为认证、审批、班级映射的运行时依赖。用户、辅导员、班级映射是本系统的基础主数据，影响登录、权限、审批人分配和历史追溯。应落入本地数据库，通过 CSV/API Provider 输入到 staging，再校验、upsert、软停用。此前设计已经定义了 staging + upsert + 软停用、导入审计和校验报告：[31-data-source-requirements-consensus-v2.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:282)。如果直接在业务中查询 Provider，会引入外部 API 可用性、分页、延迟、字段缺失、历史变更不可追溯等风险。

P0：`+3天生产就绪` 评估过于乐观。3天只适用于“API 契约已冻结、测试环境可用、认证已跑通、字段完全覆盖、只写一个薄适配器”的场景。但当前文档明确缺少完整 API 文档、认证信息、字段映射和交付时间：[37-api-blocking-solution-review-request.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:25)。在这种条件下，真实集成应预留 **1-2周**；如果坚持把用户主数据也 API 化，应预留 **2-4周**，因为会牵涉数据模型、导入/同步策略、账号状态、审批人映射和验收演练。

P1：接口设计粒度不够。`get_students(filters) -> List[Student]`、`get_counselors()`、`get_class_mapping() -> Dict[str, str]` 太粗，缺少分页、增量同步、源数据更新时间、数据质量报告、批次标识、字段映射版本、错误分类和健康检查。建议拆成：
- `StudentSourceProvider` / `CounselorSourceProvider` / `ClassMappingSourceProvider`
- `DormCheckoutProvider`
- `ProviderHealthCheck`
- `ImportAdapter` 或 `SyncService`

返回值应是 DTO，不是 Django ORM Model。Provider 负责“取数和标准化”，Import/Sync 层负责“校验、落库、审计、软停用”。

P1：`USE_MOCK_DATA` 太粗且有生产风险。当前设计用一个开关同时切用户数据和宿舍清退：[37-api-blocking-solution-review-request.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:160)。应改为细粒度配置：
- `USER_DATA_SOURCE=seed|csv|api`
- `DORM_CHECKOUT_SOURCE=mock|api|csv`
- `WECHAT_PROVIDER=mock|real`
- 生产环境禁止 `mock`，启动时 system check 直接失败
- 支持“用户主数据 CSV + 宿舍清退 API”的混合模式

P1：Mock 数据真实性不足。100学生、10辅导员可以支撑演示，但不足以覆盖风险。必须包含边界样本：无班级映射、辅导员停用、重复 class_id、多辅导员、延期毕业/非毕业生、姓名不一致、宿舍状态 `completed/pending/not_started/unknown`、API 404/401/429/500、超时、数据过期。宿舍清退枚举和降级规则已有定义：[数据对接说明文档.md](/home/caohui/projects/graduation-leave-system/docs/数据对接说明文档.md:306)。

**工期评估**

10周做“Mock/Seed 数据可演示版本”基本可行，但 Week 7 才做接口抽象偏晚。Provider 契约、DTO、种子数据、导入接口应在 Week 1-2 完成，否则认证、审批、前端都会先绑定临时模型，后续返工。

建议调整为：
- Week 1：数据契约、DTO、Provider 接口、种子数据、导入模型
- Week 2-3：CSV/staging/upsert/审计和核心账号数据
- Week 3-6：申请、审批、附件、通知
- Week 6-7：宿舍清退 Provider、降级流程、缓存、错误分类
- Week 8-9：前端
- Week 10：联调、演示、验收清单
- API 到位后：宿舍清退 API 1周；用户主数据 API 替换 CSV 另计 2-4周

因此，“10周 + 3天”建议改成：**10周演示版 + 1-2周生产集成缓冲**。若外部 API 字段继续缺失，首版应坚持 CSV/Excel 主数据导入，不等待 API。

**架构建议**

推荐架构是“反腐层 + 本地主数据”：

1. 外部数据源：CSV/API/DB view/Mock。
2. Provider：只负责读取外部数据并转换为标准 DTO。
3. Import/Sync Service：校验必填字段、唯一性、班级覆盖率、辅导员有效性。
4. 本地数据库：作为认证、权限、审批和历史记录的唯一运行时依据。
5. DormCheckoutProvider：运行时查询，可缓存，可降级到人工证明。

缓存方面，用户信息可按现有设计 30分钟左右缓存：[2026-05-27-system-design.md](/home/caohui/projects/graduation-leave-system/docs/design/2026-05-27-system-design.md:2433)。宿舍清退状态建议：
- `completed` 可缓存 10-30分钟；
- `pending/not_started` 缓存 1-5分钟；
- `unknown/error` 只短缓存 30-60秒，避免故障恢复后仍误判；
- 提交申请前必须重新校验或记录“校验时间 + source_updated_at”。

错误处理要区分：认证失败、字段缺失、学生不存在、限流、超时、服务不可用、数据不一致。现有设计已有重试和降级方向：[2026-05-27-system-design.md](/home/caohui/projects/graduation-leave-system/docs/design/2026-05-27-system-design.md:1697)，但需要补充监控指标：成功率、P95延迟、降级次数、unknown 比例、认证失败次数、429 次数。

**最终建议**

当前方案可作为开发解阻方案，但要改成：**“Seed/Mock + Provider 抽象 + CSV 主数据导入 + 宿舍清退 API 适配”**。不要把用户主数据 API 集成放到首版关键路径，也不要承诺 API 到位后三天生产就绪。真正的关键交付物应是稳定的数据契约、导入校验、降级流程、契约测试和上线验收清单。
tokens used
66,035

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
