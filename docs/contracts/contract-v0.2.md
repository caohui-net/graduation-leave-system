# 数据契约 v0.2 - Week 3 可执行契约

**版本：** v0.2  
**状态：** Week 3 closure baseline  
**日期：** 2026-05-31  
**依据：** 当前 Django serializers/views/tests 与 `.omc/artifacts/api-samples/` 实测样本  
**范围：** 登录、申请提交/查询、审批列表/通过/驳回、错误响应、分页、权限与状态机  

## 1. 枚举

```text
UserRole: student | counselor | dean
ApplicationStatus: draft | pending_counselor | pending_dean | approved | rejected
ApprovalStep: counselor | dean
ApprovalDecision: pending | approved | rejected
DormCheckoutStatus: completed | pending | not_started | unknown
```

## 2. DTO

### AuthUser

```json
{
  "user_id": "2020001",
  "name": "张三",
  "role": "student",
  "class_id": "CS2020-01"
}
```

`class_id` 对教师角色为 `null`。

### ApplicationListItem

```json
{
  "application_id": "app_eb41d2f5",
  "student_id": "2020001",
  "student_name": "张三",
  "class_id": "CS2020-01",
  "reason": "毕业离校",
  "leave_date": "2024-06-30",
  "status": "pending_counselor",
  "created_at": "2026-05-31T02:41:15.925017+08:00",
  "updated_at": "2026-05-31T02:41:15.925069+08:00"
}
```

### ApplicationDetail

`ApplicationDetail` 包含 `ApplicationListItem` 的全部字段，并额外包含：

```json
{
  "dorm_checkout_status": "completed",
  "approvals": [
    {
      "approval_id": "apv_c9f566c2",
      "application_id": "app_eb41d2f5",
      "step": "counselor",
      "approver_id": "T001",
      "approver_name": "李老师",
      "decision": "pending",
      "comment": null,
      "decided_at": null
    }
  ]
}
```

### ApprovalListItem

```json
{
  "approval_id": "apv_c9f566c2",
  "application_id": "app_eb41d2f5",
  "step": "counselor",
  "approver_id": "T001",
  "approver_name": "李老师",
  "decision": "pending",
  "created_at": "2026-05-31T02:41:15.930214+08:00"
}
```

### ApprovalDetail

```json
{
  "approval_id": "apv_c9f566c2",
  "application_id": "app_eb41d2f5",
  "step": "counselor",
  "approver_id": "T001",
  "approver_name": "李老师",
  "decision": "approved",
  "comment": "同意",
  "decided_at": "2026-05-31T02:41:16.440325+08:00"
}
```

## 3. 分页

列表接口使用精简分页格式，只返回 `count` 和 `results`。

```json
{
  "count": 1,
  "results": []
}
```

`next` 和 `previous` 不属于 v0.2 后端响应。

## 4. 状态机

| 当前状态 | 动作 | 角色 | 审批步骤 | 下一状态 | 副作用 |
| --- | --- | --- | --- | --- | --- |
| - | 提交申请 | student | - | pending_counselor | 创建 counselor 审批 |
| pending_counselor | 通过 | counselor | counselor | pending_dean | 创建 dean 审批 |
| pending_counselor | 驳回 | counselor | counselor | rejected | 无 |
| pending_dean | 通过 | dean | dean | approved | 无 |
| pending_dean | 驳回 | dean | dean | rejected | 无 |

状态保护：

- 审批记录必须仍为 `pending`，否则返回 `409 CONFLICT`。
- `counselor` 审批只能处理 `pending_counselor` 申请。
- `dean` 审批只能处理 `pending_dean` 申请。
- 已驳回申请允许学生重新提交新申请。
- 已处于 `pending_counselor`、`pending_dean`、`approved` 的申请会阻断重复提交。

## 5. 权限矩阵

| 操作 | student | counselor | dean |
| --- | --- | --- | --- |
| 登录 | 自己账号 | 自己账号 | 自己账号 |
| 提交申请 | 允许 | 禁止 | 禁止 |
| 申请列表 | 仅本人申请 | 仅本人待处理 counselor 审批对应申请 | 仅本人待处理 dean 审批对应申请 |
| 申请详情 | 仅本人申请 | 仅负责班级申请 | 仅本人待处理 dean 审批对应申请 |
| 审批列表 | 禁止 | 仅本人 counselor 审批 | 仅本人 dean 审批 |
| counselor 审批动作 | 禁止 | 仅指定 approver | 禁止 |
| dean 审批动作 | 禁止 | 禁止 | 仅指定 approver |

## 6. 端点

### POST `/api/auth/login`

请求：

```json
{"user_id":"2020001","password":"2020001"}
```

响应：

```json
{
  "access_token": "<jwt>",
  "token_type": "Bearer",
  "user": {
    "user_id": "2020001",
    "name": "张三",
    "role": "student",
    "class_id": "CS2020-01"
  }
}
```

### POST `/api/applications/`

请求：

```json
{"reason":"毕业离校","leave_date":"2024-06-30"}
```

响应：`201 ApplicationDetail`。

### GET `/api/applications/?limit=20&offset=0`

响应：`PaginatedResponse<ApplicationListItem>`。

### GET `/api/applications/{application_id}/`

响应：`ApplicationDetail`。

### GET `/api/approvals/?decision=pending&limit=20&offset=0`

`decision` 可取 `pending | approved | rejected | all`，默认 `pending`。

响应：`PaginatedResponse<ApprovalListItem>`。

### POST `/api/approvals/{approval_id}/approve/`

请求：

```json
{"comment":"同意"}
```

响应：`200 ApprovalDetail`。

### POST `/api/approvals/{approval_id}/reject/`

请求：

```json
{"comment":"材料不齐全"}
```

响应：`200 ApprovalDetail`。

## 7. 错误响应

业务错误统一使用：

```json
{
  "error": {
    "code": "CONFLICT",
    "message": "申请已存在，不能重复提交",
    "details": {
      "student_id": "2020001",
      "existing_application_id": "app_eb41d2f5"
    }
  }
}
```

当前 Week 3 核心错误码：

| code | HTTP | 场景 |
| --- | --- | --- |
| VALIDATION_ERROR | 400 | 申请提交字段缺失或格式错误 |
| FORBIDDEN | 403 | 角色不符、非指定审批人、越权访问 |
| NOT_FOUND | 404 | 申请或审批记录不存在 |
| CONFLICT | 409 | 重复提交、重复审批、状态与审批步骤不匹配 |
| DORM_BLOCKED | 422 | 宿舍清退未完成 |

说明：登录接口当前对凭据错误返回 DRF serializer error 结构，不保证业务错误 envelope。全局异常 envelope 属于 Week 4+ 范围。

## 8. Deferred To Week 4

- 附件、草稿、审计轨迹、通知、微信 OAuth。
- 全量 OpenAPI schema。
- 全局 DRF 异常 envelope 统一。
- 完整权限排列组合测试矩阵。
