# API数据示例表 - 毕业生离校申请系统

**生成日期：** 2026-06-03  
**数据来源：** 实际API响应（基于smoke test环境）

---

## 1. 申请详情 `GET /api/applications/{id}/`

### 响应示例

```json
{
  "application_id": "app_6411e95f",
  "student_id": "2020001",
  "student_name": "张三",
  "class_id": "CS2020-01",
  "reason": "毕业离校",
  "leave_date": "2026-06-04",
  "status": "approved",
  "dorm_checkout_status": "completed",
  "approvals": [...],
  "created_at": "2026-06-03T10:26:37Z",
  "updated_at": "2026-06-03T10:26:38Z"
}
```

### 字段说明表

| 字段 | 类型 | 说明 | 示例值 |
|---|---|---|---|
| application_id | string | 申请唯一标识 | app_6411e95f |
| student_id | string | 学号 | 2020001 |
| student_name | string | 学生姓名 | 张三 |
| class_id | string | 班级代码 | CS2020-01 |
| reason | string | 申请原因 | 毕业离校 |
| leave_date | date | 离校日期 | 2026-06-04 |
| status | string | 申请状态 | pending_dorm_manager / pending_counselor / pending_dean / approved / rejected |
| dorm_checkout_status | string | 宿舍退房状态 | not_started / completed |
| approvals | array | 审批记录列表 | 见下表 |
| created_at | datetime | 创建时间 | 2026-06-03T10:26:37Z |
| updated_at | datetime | 更新时间 | 2026-06-03T10:26:38Z |

---

## 2. 审批记录 `approvals` 数组

### 响应示例

```json
{
  "approval_id": "apv_5f59ad12",
  "application_id": "app_6411e95f",
  "step": "dorm_manager",
  "approver_id": "M001",
  "approver_name": "宿管员1",
  "decision": "approved",
  "comment": "同意",
  "decided_at": "2026-06-03T10:26:37Z"
}
```

### 字段说明表

| 字段 | 类型 | 说明 | 示例值 |
|---|---|---|---|
| approval_id | string | 审批唯一标识 | apv_5f59ad12 |
| application_id | string | 所属申请ID | app_6411e95f |
| step | string | 审批步骤 | dorm_manager / counselor / dean |
| approver_id | string | 审批人ID | M001 |
| approver_name | string | 审批人姓名 | 宿管员1 |
| decision | string | 审批决定 | pending / approved / rejected |
| comment | string | 审批意见 | 同意 |
| decided_at | datetime | 决定时间 | 2026-06-03T10:26:37Z |

---

## 3. 申请列表 `GET /api/applications/`

### 响应结构

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "application_id": "app_6411e95f",
      "student_name": "张三",
      "class_id": "CS2020-01",
      "status": "approved",
      "leave_date": "2026-06-04",
      "created_at": "2026-06-03T10:26:37Z"
    }
  ]
}
```

### 分页字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| count | integer | 总记录数 |
| next | string/null | 下一页URL |
| previous | string/null | 上一页URL |
| results | array | 当前页结果 |

---

## 4. 通知列表 `GET /api/notifications/`

### 响应结构

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "notification_id": "notif_...",
      "type": "approval_approved",
      "entity_type": "approval",
      "entity_id": "apv_...",
      "message": "您的申请已通过辅导员审批",
      "is_read": false,
      "created_at": "2026-06-03T10:26:38Z"
    }
  ]
}
```

### 通知字段说明表

| 字段 | 类型 | 说明 | 可选值 |
|---|---|---|---|
| notification_id | string | 通知唯一标识 | notif_... |
| type | string | 通知类型 | application_submitted / approval_approved / approval_rejected / dorm_checkout_required / dorm_checkout_completed / application_approved |
| entity_type | string | 关联实体类型 | application / approval |
| entity_id | string | 关联实体ID | app_... / apv_... |
| message | string | 通知消息 | 中文描述 |
| is_read | boolean | 是否已读 | true / false |
| created_at | datetime | 创建时间 | ISO 8601 |

---

## 5. 未读通知数 `GET /api/notifications/unread_count/`

### 响应示例

```json
{
  "unread_count": 3
}
```

---

## 6. 审批列表 `GET /api/approvals/`

### 响应结构（辅导员/宿管员/学工部视角）

```json
{
  "results": [
    {
      "approval_id": "apv_...",
      "application_id": "app_...",
      "student_name": "张三",
      "class_id": "CS2020-01",
      "step": "counselor",
      "decision": "pending",
      "created_at": "2026-06-03T10:26:37Z"
    }
  ]
}
```

---

## 数据类型说明

### 枚举值定义

**申请状态 (status):**
- `pending_dorm_manager`: 待宿管员审批
- `pending_counselor`: 待辅导员审批
- `pending_dean`: 待学工部审批
- `approved`: 已批准
- `rejected`: 已驳回

**审批步骤 (step):**
- `dorm_manager`: 宿管员审批
- `counselor`: 辅导员审批
- `dean`: 学工部审批

**审批决定 (decision):**
- `pending`: 待审批
- `approved`: 已通过
- `rejected`: 已驳回

**通知类型 (notification type):**
- `application_submitted`: 申请已提交
- `approval_approved`: 审批已通过
- `approval_rejected`: 审批已驳回
- `dorm_checkout_required`: 需要宿舍退房
- `dorm_checkout_completed`: 宿舍退房已完成
- `application_approved`: 申请最终批准

---

**数据来源文件：** `docs/api-samples/*.json`  
**采集脚本：** `tests/api_data_samples.sh`
