# API阻塞问题解决方案 - 最终共识

**文档编号：** 40  
**共识日期：** 2026-05-30  
**参与方：** Claude Opus 4.7, Codex (GPT-5.5)  
**审查周期：** 37 → 38 → 39 → 40

---

## 一、共识结论

**方案名称：** Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配

**核心原则：**
1. 用户主数据（学生、辅导员、班级映射）通过CSV导入到本地数据库
2. ImportSource接口用于数据导入，不是运行时查询
3. 宿舍清退状态通过API实时查询（可缓存、可降级）
4. 本地数据库是认证、权限、审批的唯一运行时依据

**评分：** 9/10（Codex原评分7/10，修正后提升至9/10）

---

## 二、架构设计

### 2.1 数据流架构

```
外部数据源 (CSV/API/Mock)
    ↓
ImportSource (数据导入源接口)
    ↓
ImportService (导入服务：校验、staging、upsert、软停用)
    ↓
本地数据库 (认证、权限、审批的唯一运行时依据)
    ↑
    │ (运行时查询)
DormCheckoutProvider (宿舍清退实时查询)
```

### 2.2 核心接口设计

```python
# 1. 数据导入源接口（用于导入，非运行时查询）
class IUserDataImportSource(ABC):
    """用户数据导入源接口"""
    @abstractmethod
    def fetch_students(self) -> ImportResult[StudentDTO]:
        """获取学生数据用于导入"""
        pass
    
    @abstractmethod
    def fetch_counselors(self) -> ImportResult[CounselorDTO]:
        """获取辅导员数据用于导入"""
        pass
    
    @abstractmethod
    def fetch_class_mapping(self) -> ImportResult[ClassMappingDTO]:
        """获取班级映射数据用于导入"""
        pass

# 2. 宿舍清退Provider（用于运行时查询）
class IDormCheckoutProvider(ABC):
    """宿舍清退状态提供者接口"""
    @abstractmethod
    def check_status(self, student_id: str) -> CheckoutResult:
        """运行时查询宿舍清退状态"""
        pass
    
    @abstractmethod
    def health_check(self) -> HealthStatus:
        """健康检查"""
        pass

# 3. 导入服务
class UserDataImportService:
    def __init__(self, source: IUserDataImportSource):
        self.source = source
    
    def import_data(self):
        # 1. 从source获取数据
        result = self.source.fetch_students()
        
        # 2. 导入到staging表
        self.load_to_staging(result.data)
        
        # 3. 校验（必填字段、唯一性、班级覆盖率）
        errors = self.validate(result.data)
        
        # 4. Upsert到users表
        self.upsert_to_users()
        
        # 5. 软停用未导入的账号
        self.soft_delete_missing()
        
        # 6. 生成审计日志
        self.create_audit_log(result, errors)
```

### 2.3 DTO设计

```python
@dataclass
class StudentDTO:
    student_id: str
    name: str
    department: str
    major: str
    class_id: str
    grade: int
    graduation_year: int
    is_graduating: bool
    phone: Optional[str] = None
    email: Optional[str] = None

@dataclass
class ImportResult[T]:
    data: List[T]
    total_count: int
    source_updated_at: datetime
    metadata: Dict[str, Any]

@dataclass
class CheckoutResult:
    student_id: str
    status: CheckoutStatus  # completed/pending/not_started/unknown
    checkout_date: Optional[datetime]
    error: Optional[str]
```

---

## 三、配置管理

### 3.1 细粒度配置

```python
# settings/base.py
USER_DATA_SOURCE = env.str('USER_DATA_SOURCE', default='seed')  # seed|csv|api
DORM_CHECKOUT_SOURCE = env.str('DORM_CHECKOUT_SOURCE', default='mock')  # mock|api|csv
WECHAT_PROVIDER = env.str('WECHAT_PROVIDER', default='mock')  # mock|real

# settings/dev.py
USER_DATA_SOURCE = 'seed'  # 开发环境使用种子数据
DORM_CHECKOUT_SOURCE = 'mock'
WECHAT_PROVIDER = 'mock'

# settings/prod.py
USER_DATA_SOURCE = 'csv'  # 生产环境使用CSV导入
DORM_CHECKOUT_SOURCE = 'api'  # 宿舍清退使用API
WECHAT_PROVIDER = 'real'
```

### 3.2 安全检查

```python
from django.core.checks import Error, register

@register()
def check_production_config(app_configs, **kwargs):
    errors = []
    if settings.ENVIRONMENT == 'production':
        if 'mock' in [settings.USER_DATA_SOURCE, 
                      settings.DORM_CHECKOUT_SOURCE, 
                      settings.WECHAT_PROVIDER]:
            errors.append(
                Error(
                    'Production environment cannot use mock providers',
                    hint='Set USER_DATA_SOURCE=csv, DORM_CHECKOUT_SOURCE=api, WECHAT_PROVIDER=real',
                    id='config.E001',
                )
            )
    return errors
```

---

## 四、实施计划

### 4.1 修正后的工期

| 周次 | 任务 | 交付物 |
|------|------|--------|
| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
| Week 2-3 | CSV导入功能、staging表、upsert逻辑、审计日志 | CSV导入模块、导入校验报告 |
| Week 3-6 | 申请、审批、附件、通知模块 | 核心业务功能 |
| Week 6-7 | 宿舍清退Provider、降级流程、缓存、错误分类 | 宿舍清退集成模块 |
| Week 8-9 | 前端开发 | React Native、微信小程序 |
| Week 10 | 联调、演示、验收清单 | 可演示版本（Mock数据） |

**API到位后：**
- 宿舍清退API集成：1周
- 用户主数据API替换CSV（如需）：另计2-4周

**总工期：** 10周演示版 + 1-2周生产集成缓冲

### 4.2 关键里程碑

1. **Week 1结束：** 数据契约冻结，接口定义完成
2. **Week 3结束：** CSV导入功能可用，种子数据就绪
3. **Week 6结束：** 核心业务逻辑完成
4. **Week 7结束：** 宿舍清退API对接完成
5. **Week 10结束：** 可演示版本交付

---

## 五、Mock数据设计

### 5.1 边界样本

```python
def generate_comprehensive_mock_data():
    students = [
        # 正常学生
        Student(student_id="2020001", name="张三", class_id="CS2020-01", is_graduating=True),
        
        # 边界情况
        Student(student_id="2020002", name="李四", class_id="INVALID", is_graduating=True),  # 无班级映射
        Student(student_id="2020003", name="王五", class_id="CS2020-99", is_graduating=True),  # 辅导员停用
        Student(student_id="2020004", name="赵六", class_id="CS2020-01", is_graduating=False),  # 非毕业生
        Student(student_id="2020005", name="钱七", class_id="CS2020-01", is_graduating=True, graduation_year=2027),  # 延期毕业
    ]
    
    counselors = [
        Counselor(employee_id="T001", name="李老师", is_active=True),
        Counselor(employee_id="T002", name="王老师", is_active=False),  # 停用辅导员
    ]
    
    dorm_statuses = {
        "2020001": CheckoutStatus(status="completed", date="2024-06-15"),
        "2020002": CheckoutStatus(status="pending", date=None),
        "2020003": CheckoutStatus(status="not_started", date=None),
        "2020004": CheckoutStatus(status="unknown", date=None),  # API失败
    }
    
    return students, counselors, dorm_statuses
```

### 5.2 数据规模

- **学生：** 100人（覆盖5个院系、10个班级）
- **辅导员：** 10人（包含停用账号）
- **班级映射：** 10个班级
- **宿舍清退状态：** 覆盖所有枚举值（completed/pending/not_started/unknown）

---

## 六、缓存策略

### 6.1 用户信息缓存

- **TTL：** 30分钟
- **缓存键：** `user:{user_id}`
- **更新策略：** 导入后清空缓存

### 6.2 宿舍清退状态缓存

- **completed：** 10-30分钟
- **pending/not_started：** 1-5分钟
- **unknown/error：** 30-60秒
- **提交申请前：** 必须重新校验

---

## 七、错误处理

### 7.1 错误分类

- 认证失败（401）
- 字段缺失（400）
- 学生不存在（404）
- 限流（429）
- 超时（504）
- 服务不可用（503）
- 数据不一致（422）

### 7.2 降级策略

```python
class DormCheckoutProvider:
    def check_status(self, student_id: str) -> CheckoutResult:
        try:
            # 尝试API查询
            return self._query_api(student_id)
        except APIUnavailableError:
            # 降级到缓存
            cached = self._get_cached_status(student_id)
            if cached:
                return cached
            # 降级到人工证明
            return CheckoutResult(
                student_id=student_id,
                status=CheckoutStatus.MANUAL_PROOF_REQUIRED,
                error="API不可用，需提供人工证明"
            )
```

---

## 八、关键变更

### 8.1 与原方案的差异

| 原方案 | 修正后方案 | 原因 |
|--------|-----------|------|
| RealUserDataProvider运行时查询 | CSV导入到本地数据库 | 用户主数据是基础数据，不应依赖外部API |
| USE_MOCK_DATA单一开关 | 细粒度配置（USER_DATA_SOURCE/DORM_CHECKOUT_SOURCE/WECHAT_PROVIDER） | 支持混合模式，生产环境安全 |
| 10周 + 3天 | 10周演示版 + 1-2周生产集成 | 更现实的工期评估 |
| Week 7做接口抽象 | Week 1做数据契约和接口 | 避免后续返工 |
| Provider用于运行时查询 | ImportSource用于数据导入 | 明确职责边界 |

### 8.2 核心教训

1. **不要偏离已达成的共识** - 原方案错误地将用户主数据API化，偏离了CSV导入的共识
2. **用户主数据应落入本地数据库** - 不应依赖外部API
3. **Provider抽象层的用途是数据导入** - 不是运行时查询
4. **工期评估要现实** - 考虑缺失信息的影响
5. **配置要细粒度** - 支持混合模式

---

## 九、验收标准

### 9.1 Week 10交付物

- [ ] 可演示版本（使用Mock/Seed数据）
- [ ] 数据契约文档
- [ ] CSV导入功能和校验逻辑
- [ ] 宿舍清退API适配器（Mock实现）
- [ ] 降级流程
- [ ] 契约测试
- [ ] 上线验收清单

### 9.2 生产就绪标准

- [ ] 真实API集成完成
- [ ] 性能测试通过（P95 < 500ms）
- [ ] 错误处理覆盖所有场景
- [ ] 监控和告警配置完成
- [ ] 数据导入审计日志完整
- [ ] 降级流程验证通过

---

## 十、风险管理

### 10.1 已识别风险

| 风险 | 等级 | 缓解措施 |
|------|------|---------|
| 真实API字段与Mock不一致 | P1 | Week 1冻结数据契约，预留扩展字段 |
| 真实API性能问题 | P1 | 缓存和重试机制 |
| 真实API数据结构差异大 | P2 | DTO适配层，预留2-3天调整时间 |
| API认证复杂度超预期 | P2 | 预留1-2天调试时间 |

### 10.2 应急预案

- **API延期：** 首版坚持CSV导入，不等待API
- **API不可用：** 降级到人工证明流程
- **数据质量问题：** 导入校验报告，人工审核

---

## 十一、参考文档

- **审查请求：** [37-api-blocking-solution-review-request.md](./37-api-blocking-solution-review-request.md)
- **Codex审查：** [38-codex-api-blocking-review.md](./38-codex-api-blocking-review.md)
- **Claude响应：** [39-claude-response-to-codex.md](./39-claude-response-to-codex.md)
- **系统设计：** [../../design/2026-05-27-system-design.md](../../design/2026-05-27-system-design.md)
- **数据对接：** [../../数据对接说明文档.md](../../数据对接说明文档.md)
- **共识v2：** [../codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md](../codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md)

---

## 十二、下一步行动

1. **立即执行：** 更新实施计划文档
2. **Week 1启动：** 数据契约和接口设计
3. **Week 2-3：** CSV导入功能开发
4. **持续跟进：** 外部API信息获取进度

---

**共识达成：** 2026-05-30  
**状态：** 已批准，可执行  
**有效期：** 至项目首版交付

---

**签署：**
- Claude Opus 4.7 - 方案设计与实施
- Codex (GPT-5.5) - 技术审查与验证
