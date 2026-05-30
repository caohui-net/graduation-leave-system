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
