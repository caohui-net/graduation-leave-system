# 毕业生离校申请审批系统 - API测试流程演示

**版本：** v1.0  
**创建日期：** 2026-06-07  
**说明：** 使用API测试演示完整审批流程，替代UI截图展示系统功能

---

## 测试环境

- **后端API：** http://localhost:8001
- **数据库：** PostgreSQL 15
- **测试账号：**
  - 学生：2020001 / 2020001（张三）
  - 宿管员：M001 / M001（宿管员1）
  - 辅导员：T001 / T001（李老师）

---

## 完整审批流程演示

### 步骤1：学生登录

**请求：**
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2020001","password":"2020001"}'
```

**响应：**
```json
{
    "access_token": "eyJhbGci...(JWT Token)",
    "token_type": "Bearer",
    "user": {
        "user_id": "2020001",
        "name": "张三",
        "role": "student",
        "class_id": "CS2020-01"
    }
}
```

**说明：** 学生使用学号和密码登录，获取JWT访问令牌用于后续API调用。

---

### 步骤2：学生提交离校申请

**请求：**
```bash
curl -X POST http://localhost:8001/api/applications/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {access_token}" \
  -d '{
    "reason": "已完成毕业手续，申请离校",
    "leave_date": "2024-07-01"
  }'
```

**响应：**
```json
{
    "application_id": "app_43d97aed",
    "student_id": "2020001",
    "student_name": "张三",
    "class_id": "CS2020-01",
    "reason": "已完成毕业手续，申请离校",
    "leave_date": "2024-07-01",
    "status": "pending_dorm_manager",
    "created_at": "2026-06-07T03:37:04.875322+08:00"
}
```

**说明：** 申请提交成功，初始状态为`pending_dorm_manager`（等待宿管员审批）。

---

### 步骤3：学生查询申请状态

**请求：**
```bash
curl -X GET http://localhost:8001/api/applications/app_43d97aed/ \
  -H "Authorization: Bearer {access_token}"
```

**响应（初始状态）：**
```json
{
    "application_id": "app_43d97aed",
    "student_id": "2020001",
    "student_name": "张三",
    "status": "pending_dorm_manager",
    "approvals": [
        {
            "approval_id": "apv_7ae34163",
            "step": "dorm_manager",
            "approver_id": "M001",
            "approver_name": "宿管员1",
            "decision": "pending",
            "comment": null,
            "decided_at": null
        }
    ]
}
```

**说明：** 学生可以查看申请详情和当前审批状态。

---

### 步骤4：宿管员登录

**请求：**
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id":"M001","password":"M001"}'
```

**响应：**
```json
{
    "access_token": "eyJhbGci...(JWT Token)",
    "token_type": "Bearer",
    "user": {
        "user_id": "M001",
        "name": "宿管员1",
        "role": "dorm_manager",
        "class_id": null
    }
}
```

**说明：** 宿管员使用工号和密码登录系统。

---

### 步骤5：宿管员查看待审批列表

**请求：**
```bash
curl -X GET "http://localhost:8001/api/approvals/?decision=pending" \
  -H "Authorization: Bearer {access_token}"
```

**响应：**
```json
{
    "count": 1,
    "results": [
        {
            "approval_id": "apv_7ae34163",
            "application_id": "app_43d97aed",
            "student_name": "张三",
            "class_id": "CS2020-01",
            "reason": "已完成毕业手续，申请离校",
            "step": "dorm_manager",
            "decision": "pending"
        }
    ]
}
```

**说明：** 宿管员可以查看本楼栋学生的待审批申请列表。

---

### 步骤6：宿管员审批通过

**请求：**
```bash
curl -X POST http://localhost:8001/api/approvals/apv_7ae34163/approve/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {access_token}" \
  -d '{"comment":"宿舍清理完毕，同意离校"}'
```

**响应：**
```json
{
    "approval_id": "apv_7ae34163",
    "application_id": "app_43d97aed",
    "step": "dorm_manager",
    "approver_id": "M001",
    "approver_name": "宿管员1",
    "decision": "approved",
    "comment": "宿舍清理完毕，同意离校",
    "decided_at": "2026-06-07T03:37:05.061288+08:00"
}
```

**说明：** 宿管员审批通过后，申请自动流转到辅导员审批环节。

---

### 步骤7：辅导员登录

**请求：**
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id":"T001","password":"T001"}'
```

**响应：**
```json
{
    "access_token": "eyJhbGci...(JWT Token)",
    "token_type": "Bearer",
    "user": {
        "user_id": "T001",
        "name": "李老师",
        "role": "counselor",
        "class_id": null
    }
}
```

**说明：** 辅导员使用工号和密码登录系统。

---

### 步骤8：辅导员查看待审批列表

**请求：**
```bash
curl -X GET "http://localhost:8001/api/approvals/?decision=pending" \
  -H "Authorization: Bearer {access_token}"
```

**响应：**
```json
{
    "count": 1,
    "results": [
        {
            "approval_id": "apv_c174232a",
            "application_id": "app_43d97aed",
            "student_name": "张三",
            "class_id": "CS2020-01",
            "reason": "已完成毕业手续，申请离校",
            "step": "counselor",
            "decision": "pending",
            "dorm_manager_comment": "宿舍清理完毕，同意离校"
        }
    ]
}
```

**说明：** 辅导员可以查看本学院学生的待审批申请，并看到宿管员的审批意见。

---

### 步骤9：辅导员审批通过

**请求：**
```bash
curl -X POST http://localhost:8001/api/approvals/apv_c174232a/approve/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {access_token}" \
  -d '{"comment":"档案已办理，同意离校"}'
```

**响应：**
```json
{
    "approval_id": "apv_c174232a",
    "application_id": "app_43d97aed",
    "step": "counselor",
    "approver_id": "T001",
    "approver_name": "李老师",
    "decision": "approved",
    "comment": "档案已办理，同意离校",
    "decided_at": "2026-06-07T11:00:05.672470+08:00"
}
```

**说明：** 辅导员审批通过后，申请状态变更为`approved`（已通过）。

---

### 步骤10：学生查看最终状态

**请求：**
```bash
curl -X GET http://localhost:8001/api/applications/app_43d97aed/ \
  -H "Authorization: Bearer {access_token}"
```

**响应（最终状态）：**
```json
{
    "application_id": "app_43d97aed",
    "student_id": "2020001",
    "student_name": "张三",
    "class_id": "CS2020-01",
    "reason": "已完成毕业手续，申请离校",
    "leave_date": "2024-07-01",
    "status": "approved",
    "dorm_checkout_status": "completed",
    "approvals": [
        {
            "approval_id": "apv_7ae34163",
            "step": "dorm_manager",
            "approver_id": "M001",
            "approver_name": "宿管员1",
            "decision": "approved",
            "comment": "宿舍清理完毕，同意离校",
            "decided_at": "2026-06-07T03:37:05.061288+08:00"
        },
        {
            "approval_id": "apv_c174232a",
            "step": "counselor",
            "approver_id": "T001",
            "approver_name": "李老师",
            "decision": "approved",
            "comment": "档案已办理，同意离校",
            "decided_at": "2026-06-07T11:00:05.672470+08:00"
        }
    ],
    "created_at": "2026-06-07T03:37:04.875322+08:00",
    "updated_at": "2026-06-07T11:00:05.676123+08:00"
}
```

**说明：** 申请已完成所有审批流程，状态为`approved`，学生可以离校。

---

## 审批驳回流程演示

### 宿管员驳回申请

**请求：**
```bash
curl -X POST http://localhost:8001/api/approvals/{approval_id}/reject/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {access_token}" \
  -d '{"comment":"宿舍物品未清理完毕，请处理后重新申请"}'
```

**响应：**
```json
{
    "approval_id": "apv_xxx",
    "decision": "rejected",
    "comment": "宿舍物品未清理完毕，请处理后重新申请",
    "decided_at": "2026-06-07T12:00:00.000000+08:00"
}
```

**说明：** 审批驳回后，申请状态变更为`rejected`，学生需要处理驳回原因后重新提交申请。

---

## 多宿管员协同审批演示

当学生所在楼栋有多个宿管员时，系统会为所有宿管员创建审批任务：

### 查看多个宿管员的审批记录

**响应示例：**
```json
{
    "approvals": [
        {
            "approval_id": "apv_7ae34163",
            "step": "dorm_manager",
            "approver_id": "M001",
            "approver_name": "宿管员1",
            "decision": "approved",
            "comment": "同意",
            "decided_at": "2026-06-07T03:37:05.061288+08:00"
        },
        {
            "approval_id": "apv_3b9dd5c9",
            "step": "dorm_manager",
            "approver_id": "M003",
            "approver_name": "宿管员3",
            "decision": "approved",
            "comment": "已由宿管员1完成审批，无需重复操作",
            "decided_at": "2026-06-07T03:37:05.071285+08:00"
        }
    ]
}
```

**说明：** 任意一个宿管员审批通过后，其他宿管员的审批会自动完成，显示"已由XXX完成审批"。

---

## API端点总结

| 功能 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 登录 | POST | /api/auth/login | 获取JWT令牌 |
| 提交申请 | POST | /api/applications/ | 学生提交离校申请 |
| 查询申请列表 | GET | /api/applications/ | 查询本人申请列表 |
| 查询申请详情 | GET | /api/applications/{id}/ | 查询申请详细信息 |
| 查询待审批列表 | GET | /api/approvals/?decision=pending | 查询待审批任务 |
| 审批通过 | POST | /api/approvals/{id}/approve/ | 审批通过并添加意见 |
| 审批驳回 | POST | /api/approvals/{id}/reject/ | 审批驳回并说明原因 |

---

## 状态说明

| 状态 | 说明 |
|------|------|
| pending_dorm_manager | 等待宿管员审批 |
| pending_counselor | 等待辅导员审批 |
| approved | 已通过 |
| rejected | 已驳回 |

---

**注：** 本文档使用API测试演示系统功能，实际用户操作通过微信小程序界面进行，操作流程与API测试流程一致。
