# 数据契约 v0.1 Final - 最小可执行契约

**版本：** v0.1 Final  
**状态：** ✅ 已冻结（可执行契约标准）  
**冻结日期：** 2026-05-30  
**适用范围：** Week 1纵向切片  
**下一版本：** v0.2（Week 3）  
**Codex审查：** 通过（文档52）

---

## 1. 核心DTO

### 1.1 UserDTO

```python
@dataclass
class UserDTO:
    """用户数据传输对象"""
    user_id: str                      # 学号/工号
    name: str                         # 姓名
    role: UserRole                    # 角色：student/counselor/dean
    active: bool                      # 账号是否激活
    class_id: Optional[str] = None    # 班级ID（学生必填，教师为None）
    is_graduating: Optional[bool] = None  # 是否毕业生（仅学生）
    graduation_year: Optional[int] = None # 毕业年份（仅学生）
```

### 1.2 ApplicationDTO

```python
@dataclass
class ApplicationDTO:
    """离校申请数据传输对象"""
    application_id: str
    student_id: str
    student_name: str
    class_id: str
    reason: str                      # 申请理由
    leave_date: str                  # 计划离校日期 (YYYY-MM-DD)
    status: ApplicationStatus
    dorm_checkout_status: DormCheckoutStatus
    created_at: str                  # ISO8601
    updated_at: str
```

### 1.3 ApprovalDTO

```python
@dataclass
class ApprovalDTO:
    """审批记录数据传输对象"""
    approval_id: str
    application_id: str
    step: ApprovalStep           # counselor/dean
    approver_id: str
    approver_name: str
    decision: ApprovalDecision   # approved/rejected/pending
    comment: Optional[str]
    decided_at: Optional[str]    # ISO8601
```

### 1.4 DormCheckoutStatusDTO

```python
@dataclass
class DormCheckoutStatusDTO:
    """宿舍清退状态数据传输对象"""
    student_id: str
    status: DormCheckoutStatus   # completed/pending/not_started/unknown
    checked_at: Optional[str]    # ISO8601
    blocking_reason: Optional[str]
    provider_error_code: Optional[str]
```

---

## 2. 状态枚举

### 2.1 UserRole

```python
class UserRole(str, Enum):
    STUDENT = "student"
    COUNSELOR = "counselor"
    DEAN = "dean"
```

### 2.2 ApplicationStatus

```python
class ApplicationStatus(str, Enum):
    DRAFT = "draft"                      # 草稿
    PENDING_COUNSELOR = "pending_counselor"  # 待辅导员审批
    PENDING_DEAN = "pending_dean"        # 待学工部审批
    APPROVED = "approved"                # 已通过
    REJECTED = "rejected"                # 已驳回
```

### 2.3 ApprovalStep

```python
class ApprovalStep(str, Enum):
    COUNSELOR = "counselor"
    DEAN = "dean"
```

### 2.4 ApprovalDecision

```python
class ApprovalDecision(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
```

### 2.5 DormCheckoutStatus

```python
class DormCheckoutStatus(str, Enum):
    COMPLETED = "completed"          # 已清退
    PENDING = "pending"              # 清退中
    NOT_STARTED = "not_started"      # 未开始
    UNKNOWN = "unknown"              # 状态未知（API失败）
```

### 2.6 状态机契约

**申请状态流转规则：**

| 当前状态 | 触发动作 | 角色 | 下一状态 | 副作用 |
|---------|---------|------|---------|--------|
| - | 学生提交申请 | student | pending_counselor | 创建辅导员审批记录 |
| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
| pending_counselor | 辅导员驳回 | counselor | rejected | 无 |
| pending_dean | 学工部通过 | dean | approved | 无 |
| pending_dean | 学工部驳回 | dean | rejected | 无 |

**宿舍清退状态处理规则：**

| 宿舍状态 | 提交申请行为 | HTTP状态 | 错误码 |
|---------|------------|---------|--------|
| completed | 允许提交 | 201 | - |
| pending | 阻断提交 | 422 | DORM_BLOCKED |
| not_started | 阻断提交 | 422 | DORM_BLOCKED |
| unknown | 阻断提交 | 422 | DORM_BLOCKED |
| provider_unavailable | 阻断提交 | 503 | PROVIDER_UNAVAILABLE |

**角色权限矩阵：**

| 操作 | student | counselor | dean |
|------|---------|-----------|------|
| 提交申请 | ✓（仅自己） | ✗ | ✗ |
| 查看申请 | ✓（仅自己） | ✓（本班级） | ✓（所有） |
| 辅导员审批 | ✗ | ✓（本班级） | ✗ |
| 学工部审批 | ✗ | ✗ | ✓（所有） |

---

## 3. 错误码

### 3.1 业务错误 (4xx)

| 错误码 | HTTP状态 | 说明 | 示例场景 |
|--------|---------|------|---------|
| VALIDATION_ERROR | 400 | 请求参数校验失败 | 必填字段缺失、格式错误 |
| AUTH_REQUIRED | 401 | 未认证 | Token缺失或过期 |
| FORBIDDEN | 403 | 无权限 | 学生访问他人申请 |
| NOT_FOUND | 404 | 资源不存在 | 申请ID不存在 |
| CONFLICT | 409 | 资源冲突 | 重复提交申请 |
| DORM_BLOCKED | 422 | 宿舍清退未完成 | 提交申请时宿舍未清退 |

### 3.2 系统错误 (5xx)

| 错误码 | HTTP状态 | 说明 | 示例场景 |
|--------|---------|------|---------|
| PROVIDER_UNAVAILABLE | 503 | 外部服务不可用 | 宿舍清退API超时 |
| INTERNAL_ERROR | 500 | 内部错误 | 数据库连接失败 |

### 3.3 错误响应格式

```json
{
  "error": {
    "code": "DORM_BLOCKED",
    "message": "宿舍清退未完成，无法提交申请",
    "details": {
      "student_id": "2020001",
      "dorm_status": "pending"
    }
  }
}
```

---

## 4. API端点

### 4.1 认证

#### POST /api/auth/login

**请求：**
```json
{
  "user_id": "2020001",
  "password": "password123"
}
```

**响应：**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "user": {
    "user_id": "2020001",
    "name": "张三",
    "role": "student",
    "class_id": "CS2020-01"
  }
}
```

**说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。

### 4.2 申请

#### POST /api/applications

**请求：**
```json
{
  "reason": "毕业离校",
  "leave_date": "2024-06-30"
}
```

**响应：**
```json
{
  "application_id": "app_001",
  "student_id": "2020001",
  "student_name": "张三",
  "class_id": "CS2020-01",
  "reason": "毕业离校",
  "leave_date": "2024-06-30",
  "status": "pending_counselor",
  "dorm_checkout_status": "completed",
  "created_at": "2024-05-30T10:00:00Z",
  "updated_at": "2024-05-30T10:00:00Z"
}
```

#### GET /api/applications/{application_id}

**响应：**
```json
{
  "application_id": "app_001",
  "student_id": "2020001",
  "student_name": "张三",
  "class_id": "CS2020-01",
  "reason": "毕业离校",
  "leave_date": "2024-06-30",
  "status": "pending_counselor",
  "dorm_checkout_status": "completed",
  "approvals": [
    {
      "approval_id": "apv_001",
      "step": "counselor",
      "approver_id": "T001",
      "approver_name": "李老师",
      "decision": "pending",
      "comment": null,
      "decided_at": null
    }
  ],
  "created_at": "2024-05-30T10:00:00Z",
  "updated_at": "2024-05-30T10:00:00Z"
}
```

### 4.3 审批

#### POST /api/approvals/{approval_id}/approve

**请求：**
```json
{
  "comment": "同意离校"
}
```

**响应：**
```json
{
  "approval_id": "apv_001",
  "application_id": "app_001",
  "step": "counselor",
  "approver_id": "T001",
  "approver_name": "李老师",
  "decision": "approved",
  "comment": "同意离校",
  "decided_at": "2024-05-30T11:00:00Z"
}
```

#### POST /api/approvals/{approval_id}/reject

**请求：**
```json
{
  "comment": "材料不齐全"
}
```

**响应：**
```json
{
  "approval_id": "apv_001",
  "application_id": "app_001",
  "step": "counselor",
  "approver_id": "T001",
  "approver_name": "李老师",
  "decision": "rejected",
  "comment": "材料不齐全",
  "decided_at": "2024-05-30T11:00:00Z"
}
```

---

## 5. 样例数据

### 5.1 正常样本

**默认密码：** 所有账号默认密码为 `password123`

**学生（10人）：**
```python
students = [
    {"user_id": "2020001", "name": "张三", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020002", "name": "李四", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020003", "name": "王五", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020004", "name": "赵六", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020005", "name": "钱七", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020006", "name": "孙八", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020007", "name": "周九", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020008", "name": "吴十", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020009", "name": "郑十一", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020010", "name": "王十二", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
]
```

**辅导员（2人）：**
```python
counselors = [
    {"user_id": "T001", "name": "李老师", "role": "counselor", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
    {"user_id": "T002", "name": "王老师", "role": "counselor", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
]
```

**学工部（1人）：**
```python
deans = [
    {"user_id": "D001", "name": "赵主任", "role": "dean", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
]
```

**班级映射：**
```python
class_mappings = [
    {"class_id": "CS2020-01", "counselor_id": "T001"},
    {"class_id": "CS2020-02", "counselor_id": "T002"},
]
```

### 5.2 边界样本

**无班级映射：**
```python
{"user_id": "2020099", "name": "边界1", "role": "student", "class_id": "INVALID", "is_graduating": True, "graduation_year": 2024, "active": True}
```

**辅导员停用：**
```python
{"user_id": "T099", "name": "停用老师", "role": "counselor", "class_id": None, "active": False}
```

**非毕业生：**
```python
{"user_id": "2021001", "name": "边界2", "role": "student", "class_id": "CS2021-01", "is_graduating": False, "graduation_year": 2025, "active": True}
```

**延期毕业：**
```python
{"user_id": "2019001", "name": "边界3", "role": "student", "class_id": "CS2019-01", "is_graduating": True, "graduation_year": 2024, "active": True}
```

---

## 6. Mock响应

### 6.1 宿舍清退Mock

**DormCheckoutProvider Mock实现：**

```python
class MockDormCheckoutProvider:
    def check_status(self, student_id: str) -> DormCheckoutStatusDTO:
        # 固定返回规则（覆盖所有状态）
        mock_data = {
            "2020001": DormCheckoutStatusDTO(
                student_id="2020001",
                status=DormCheckoutStatus.COMPLETED,
                checked_at="2024-05-15T10:00:00Z",
                blocking_reason=None,
                provider_error_code=None
            ),
            "2020002": DormCheckoutStatusDTO(
                student_id="2020002",
                status=DormCheckoutStatus.PENDING,
                checked_at=None,
                blocking_reason="宿舍物品未清理",
                provider_error_code=None
            ),
            "2020003": DormCheckoutStatusDTO(
                student_id="2020003",
                status=DormCheckoutStatus.NOT_STARTED,
                checked_at=None,
                blocking_reason="未提交清退申请",
                provider_error_code=None
            ),
            "2020099": DormCheckoutStatusDTO(
                student_id="2020099",
                status=DormCheckoutStatus.UNKNOWN,
                checked_at=None,
                blocking_reason="学生信息不存在",
                provider_error_code="STUDENT_NOT_FOUND"
            ),
        }
        
        # 默认返回NOT_STARTED（而非completed，避免掩盖失败路径）
        return mock_data.get(student_id, DormCheckoutStatusDTO(
            student_id=student_id,
            status=DormCheckoutStatus.NOT_STARTED,
            checked_at=None,
            blocking_reason="未在宿舍系统中找到记录",
            provider_error_code=None
        ))
```

### 6.2 错误Mock

**400 Validation Error：**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": {
      "field": "leave_date",
      "reason": "离校日期不能早于今天"
    }
  }
}
```

**401 Unauthorized：**
```json
{
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "Token缺失或过期"
  }
}
```

**403 Forbidden：**
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "无权限访问此资源"
  }
}
```

**404 Not Found：**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "申请不存在",
    "details": {
      "application_id": "app_999"
    }
  }
}
```

**409 Conflict：**
```json
{
  "error": {
    "code": "CONFLICT",
    "message": "申请已存在，不能重复提交",
    "details": {
      "student_id": "2020001",
      "existing_application_id": "app_001"
    }
  }
}
```

**422 Dorm Blocked：**
```json
{
  "error": {
    "code": "DORM_BLOCKED",
    "message": "宿舍清退未完成，无法提交申请",
    "details": {
      "student_id": "2020002",
      "dorm_status": "pending",
      "blocking_reason": "宿舍物品未清理"
    }
  }
}
```

**500 Internal Error：**
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "服务器内部错误",
    "details": {
      "error_id": "err_20240530_001",
      "message": "数据库连接失败"
    }
  }
}
```

**503 Provider Unavailable：**
```json
{
  "error": {
    "code": "PROVIDER_UNAVAILABLE",
    "message": "宿舍清退服务暂时不可用，请稍后重试",
    "details": {
      "student_id": "2020503",
      "provider": "dorm_checkout",
      "error": "Connection timeout"
    }
  }
}
```

---

## 7. 变更日志

### v0.1 (2026-05-30)

**初始版本 - 最小可执行契约**

**包含内容：**
- 核心DTO（User、Application、Approval、DormCheckoutStatus）
- 状态枚举（UserRole、ApplicationStatus、ApprovalStep、ApprovalDecision、DormCheckoutStatus）
- 错误码（8个核心错误码）
- API端点（认证、申请、审批、查询）
- 样例数据（正常样本 + 边界样本）
- Mock响应（宿舍清退Mock + 错误Mock）

**不包含内容（v0.2）：**
- 附件相关DTO和API
- 通知相关DTO和API
- 微信OAuth相关API
- 完整RBAC权限矩阵
- 审批转办、撤回、驳回重提

**验收标准：**
- 前端可用mock跑通登录→提交→审批→查询流程
- 后端可用seed数据跑通端到端测试

---

## 8. 使用说明

### 8.1 前端使用

**Mock Server配置：**
```javascript
// mock/handlers.js
export const handlers = [
  rest.post('/api/auth/login', (req, res, ctx) => {
    return res(ctx.json({
      access_token: 'mock_token',
      token_type: 'Bearer',
      user: {
        user_id: '2020001',
        name: '张三',
        role: 'student',
        class_id: 'CS2020-01'
      }
    }))
  }),
  // ... 其他端点
]
```

### 8.2 后端使用

**Seed数据加载：**
```bash
python manage.py seed_users
python manage.py seed_class_mappings
```

**端到端测试：**
```python
def test_application_flow():
    # 1. 学生登录
    response = client.post('/api/auth/login', {
        'user_id': '2020001',
        'password': 'password123'
    })
    token = response.json()['access_token']
    
    # 2. 提交申请
    response = client.post('/api/applications', 
        headers={'Authorization': f'Bearer {token}'},
        json={'reason': '毕业离校', 'leave_date': '2024-06-30'}
    )
    app_id = response.json()['application_id']
    
    # 3. 辅导员审批
    # 4. 学工部审批
    # 5. 查询状态
```

---

**契约负责人：** Claude Opus 4.7  
**前端Review：** 待确认  
**业务确认：** 待确认  
**冻结日期：** 2026-05-30  
**下一版本：** v0.2（Week 3）
