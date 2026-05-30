# API Contract v0.2

**Version:** 0.2  
**Date:** 2026-05-31  
**Status:** Draft  
**Based on:** Code analysis and existing implementation

---

## 1. Status Enums

### 1.1 ApplicationStatus

**Location:** `backend/apps/applications/models.py`

| Value | Description | Chinese |
|-------|-------------|---------|
| `draft` | Draft application | 草稿 |
| `pending_counselor` | Awaiting counselor approval | 待辅导员审批 |
| `pending_dean` | Awaiting dean approval | 待学工部审批 |
| `approved` | Approved | 已通过 |
| `rejected` | Rejected | 已驳回 |

### 1.2 ApprovalDecision

**Location:** `backend/apps/approvals/models.py`

| Value | Description | Chinese |
|-------|-------------|---------|
| `pending` | Pending approval | 待审批 |
| `approved` | Approved | 已通过 |
| `rejected` | Rejected | 已驳回 |

### 1.3 ApprovalStep

**Location:** `backend/apps/approvals/models.py`

| Value | Description | Chinese |
|-------|-------------|---------|
| `counselor` | Counselor approval step | 辅导员审批 |
| `dean` | Dean approval step | 学工部审批 |

### 1.4 DormCheckoutStatus

**Location:** `backend/apps/applications/models.py`

| Value | Description | Chinese |
|-------|-------------|---------|
| `completed` | Checkout completed | 已完成 |
| `pending` | Checkout in progress | 进行中 |
| `not_started` | Checkout not started | 未开始 |
| `unknown` | Status unknown | 未知 |

---

## 2. State Machine

### 2.1 State Transition Diagram

```
[New Application]
       ↓
   draft (optional)
       ↓
pending_counselor ──approve──→ pending_dean ──approve──→ approved (terminal)
       ↓                              ↓
    reject                         reject
       ↓                              ↓
   rejected ←──────────────────────────┘
       ↓
   resubmit
       ↓
pending_counselor (new cycle)
```

### 2.2 Valid State Transitions

| From | To | Trigger | Notes |
|------|----|---------| ------|
| `null` | `pending_counselor` | Student submits application | Initial submission |
| `pending_counselor` | `pending_dean` | Counselor approves | Creates dean approval |
| `pending_counselor` | `rejected` | Counselor rejects | Terminal state |
| `pending_dean` | `approved` | Dean approves | Terminal state |
| `pending_dean` | `rejected` | Dean rejects | Terminal state |
| `rejected` | `pending_counselor` | Student resubmits | New approval cycle |

### 2.3 Terminal States

**Terminal states:** `approved`, `rejected`

**Behavior:**
- No further approve/reject operations allowed on terminal state applications
- Attempting operations on terminal states returns `409 CONFLICT`
- Resubmission from `rejected` creates new application cycle with new approvals

### 2.4 State Validation Rules

**Rule 1: Status/Step Matching**
- Counselor approval requires `application.status == pending_counselor`
- Dean approval requires `application.status == pending_dean`
- Mismatch returns `409 CONFLICT`

**Rule 2: Decision Finality**
- Once `approval.decision != pending`, no further operations allowed
- Attempting repeat operations returns `409 CONFLICT`

**Rule 3: Approval Sequence**
- Counselor approval must complete before dean approval
- Dean cannot approve if counselor hasn't approved yet

---

## 3. Permission Matrix

### 3.1 Role-Based Access Control

| Operation | Student | Counselor | Dean | Notes |
|-----------|---------|-----------|------|-------|
| Submit application | ✅ | ❌ | ❌ | Own applications only |
| View own application | ✅ | ✅ | ✅ | Students see own, staff see assigned |
| View approval list | ❌ | ✅ | ✅ | Only assigned approvals |
| Approve counselor step | ❌ | ✅ | ❌ | Must be assigned counselor |
| Reject counselor step | ❌ | ✅ | ❌ | Must be assigned counselor |
| Approve dean step | ❌ | ❌ | ✅ | Must be assigned dean |
| Reject dean step | ❌ | ❌ | ✅ | Must be assigned dean |

### 3.2 Permission Checks

**Check 1: Role Check**
- Counselor operations require `user.role == COUNSELOR`
- Dean operations require `user.role == DEAN`
- Violation returns `403 FORBIDDEN`

**Check 2: Approver Assignment**
- Operations require `approval.approver_id == user.user_id`
- Violation returns `403 FORBIDDEN`

**Check 3: Step/Role Matching**
- Counselor can only act on `step == counselor`
- Dean can only act on `step == dean`
- Violation returns `403 FORBIDDEN`

---

## 4. Pagination Format

**Implementation:** `LimitOffsetPagination`

**Response structure:**
```json
{
  "count": 100,
  "results": [...]
}
```

**Query parameters:**
- `limit`: Items per page (default: 20, max: 100)
- `offset`: Starting position (default: 0)

**Note:** No `next` or `previous` URLs included. Clients must calculate pagination manually.

---

## 5. Error Codes

### 5.1 Error Response Format

All errors follow this structure:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}  // Optional, varies by error
  }
}
```

### 5.2 Error Code Reference

| Code | HTTP Status | Description | When Used |
|------|-------------|-------------|-----------|
| `VALIDATION_ERROR` | 400 | Request validation failed | Missing/invalid fields |
| `FORBIDDEN` | 403 | Permission denied | Role/approver mismatch |
| `NOT_FOUND` | 404 | Resource not found | Invalid ID |
| `CONFLICT` | 409 | State conflict | Duplicate/invalid operation |
| `DORM_BLOCKED` | 422 | Dorm checkout incomplete | Blocking condition |
| `PROVIDER_ERROR` | 503 | External service error | Provider unavailable |

---

**(Contract continues in next segment)**
# API Contract v0.2 - Part 2: Error Samples & API Examples

**Version:** 0.2  
**Date:** 2026-05-31

---

## 6. Error Code Samples

### 6.1 VALIDATION_ERROR (400)

**Scenario:** Missing required fields

**Request:**
```http
POST /api/applications/
Content-Type: application/json

{
  "reason": ""
}
```

**Response:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": {
      "reason": ["This field may not be blank."],
      "leave_date": ["This field is required."]
    }
  }
}
```

### 6.2 FORBIDDEN (403)

**Scenario 1:** Student attempts to approve

**Request:**
```http
POST /api/approvals/apv_001/approve/
Authorization: Bearer <student_token>
Content-Type: application/json

{
  "comment": "同意"
}
```

**Response:**
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "无权限执行此操作"
  }
}
```

**Scenario 2:** Cross-counselor approval attempt

**Request:**
```http
POST /api/approvals/apv_001/approve/
Authorization: Bearer <counselor2_token>
Content-Type: application/json

{
  "comment": "同意"
}
```

**Response:**
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "无权限执行此操作"
  }
}
```

### 6.3 NOT_FOUND (404)

**Scenario:** Invalid approval ID

**Request:**
```http
POST /api/approvals/invalid_id/approve/
Authorization: Bearer <counselor_token>
```

**Response:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "审批记录不存在"
  }
}
```

### 6.4 CONFLICT (409)

**Scenario 1:** Duplicate submission

**Request:**
```http
POST /api/applications/
Authorization: Bearer <student_token>
Content-Type: application/json

{
  "reason": "毕业离校",
  "leave_date": "2024-06-30"
}
```

**Response:**
```json
{
  "error": {
    "code": "CONFLICT",
    "message": "已有待审批或已通过的申请，不能重复提交",
    "details": {
      "student_id": "2020001",
      "existing_application_id": "app_abc123",
      "status": "pending_counselor"
    }
  }
}
```

**Scenario 2:** Duplicate approval

**Request:**
```http
POST /api/approvals/apv_001/approve/
Authorization: Bearer <counselor_token>
Content-Type: application/json

{
  "comment": "再次同意"
}
```

**Response:**
```json
{
  "error": {
    "code": "CONFLICT",
    "message": "审批已完成，不能重复操作"
  }
}
```

**Scenario 3:** Status/step mismatch

**Request:**
```http
POST /api/approvals/apv_001/approve/
Authorization: Bearer <counselor_token>
Content-Type: application/json

{
  "comment": "同意"
}
```

**Response (when application.status != pending_counselor):**
```json
{
  "error": {
    "code": "CONFLICT",
    "message": "申请状态与审批步骤不匹配"
  }
}
```

### 6.5 DORM_BLOCKED (422)

**Scenario:** Dorm checkout incomplete

**Request:**
```http
POST /api/applications/
Authorization: Bearer <student_token>
Content-Type: application/json

{
  "reason": "毕业离校",
  "leave_date": "2024-06-30"
}
```

**Response:**
```json
{
  "error": {
    "code": "DORM_BLOCKED",
    "message": "宿舍清退未完成，无法提交申请",
    "details": {
      "student_id": "2020001",
      "dorm_status": "pending",
      "blocking_reason": "物品未清空"
    }
  }
}
```

---

## 7. API Endpoint Samples

### 7.1 POST /api/applications/ - Submit Application

**Request:**
```http
POST /api/applications/
Authorization: Bearer <student_token>
Content-Type: application/json

{
  "reason": "毕业离校",
  "leave_date": "2024-06-30"
}
```

**Success Response (201):**
```json
{
  "application_id": "app_abc123",
  "student_id": "2020001",
  "student_name": "张三",
  "class_id": "CS2020-01",
  "reason": "毕业离校",
  "leave_date": "2024-06-30",
  "status": "pending_counselor",
  "dorm_checkout_status": "completed",
  "approvals": [
    {
      "approval_id": "apv_xyz789",
      "application_id": "app_abc123",
      "step": "counselor",
      "approver_id": "T001",
      "approver_name": "李老师",
      "decision": "pending",
      "comment": null,
      "decided_at": null
    }
  ],
  "created_at": "2024-06-01T10:00:00Z",
  "updated_at": "2024-06-01T10:00:00Z"
}
```

### 7.2 GET /api/applications/{id} - Get Application Detail

**Request:**
```http
GET /api/applications/app_abc123
Authorization: Bearer <student_token>
```

**Success Response (200):**
```json
{
  "application_id": "app_abc123",
  "student_id": "2020001",
  "student_name": "张三",
  "class_id": "CS2020-01",
  "reason": "毕业离校",
  "leave_date": "2024-06-30",
  "status": "pending_dean",
  "dorm_checkout_status": "completed",
  "approvals": [
    {
      "approval_id": "apv_xyz789",
      "application_id": "app_abc123",
      "step": "counselor",
      "approver_id": "T001",
      "approver_name": "李老师",
      "decision": "approved",
      "comment": "同意",
      "decided_at": "2024-06-02T09:00:00Z"
    },
    {
      "approval_id": "apv_def456",
      "application_id": "app_abc123",
      "step": "dean",
      "approver_id": "D001",
      "approver_name": "赵主任",
      "decision": "pending",
      "comment": null,
      "decided_at": null
    }
  ],
  "created_at": "2024-06-01T10:00:00Z",
  "updated_at": "2024-06-02T09:00:00Z"
}
```

### 7.3 GET /api/approvals/ - List Approvals (Paginated)

**Request:**
```http
GET /api/approvals/?decision=pending&limit=20&offset=0
Authorization: Bearer <counselor_token>
```

**Success Response (200):**
```json
{
  "count": 45,
  "results": [
    {
      "approval_id": "apv_xyz789",
      "application_id": "app_abc123",
      "step": "counselor",
      "approver_id": "T001",
      "approver_name": "李老师",
      "decision": "pending",
      "created_at": "2024-06-01T10:00:00Z"
    },
    {
      "approval_id": "apv_ghi012",
      "application_id": "app_def456",
      "step": "counselor",
      "approver_id": "T001",
      "approver_name": "李老师",
      "decision": "pending",
      "created_at": "2024-06-01T11:00:00Z"
    }
  ]
}
```

**Query Parameters:**
- `decision`: Filter by decision (pending/approved/rejected/all)
- `limit`: Items per page (default: 20, max: 100)
- `offset`: Starting position (default: 0)

### 7.4 POST /api/approvals/{id}/approve/ - Approve

**Request:**
```http
POST /api/approvals/apv_xyz789/approve/
Authorization: Bearer <counselor_token>
Content-Type: application/json

{
  "comment": "同意离校申请"
}
```

**Success Response (200):**
```json
{
  "approval_id": "apv_xyz789",
  "application_id": "app_abc123",
  "step": "counselor",
  "approver_id": "T001",
  "approver_name": "李老师",
  "decision": "approved",
  "comment": "同意离校申请",
  "decided_at": "2024-06-02T09:00:00Z"
}
```

### 7.5 POST /api/approvals/{id}/reject/ - Reject

**Request:**
```http
POST /api/approvals/apv_xyz789/reject/
Authorization: Bearer <counselor_token>
Content-Type: application/json

{
  "comment": "材料不齐全，请补充"
}
```

**Success Response (200):**
```json
{
  "approval_id": "apv_xyz789",
  "application_id": "app_abc123",
  "step": "counselor",
  "approver_id": "T001",
  "approver_name": "李老师",
  "decision": "rejected",
  "comment": "材料不齐全，请补充",
  "decided_at": "2024-06-02T09:00:00Z"
}
```

---

## 8. Edge Cases

### 8.1 Empty List Response

**Request:**
```http
GET /api/approvals/?decision=pending
Authorization: Bearer <counselor_token>
```

**Response (200):**
```json
{
  "count": 0,
  "results": []
}
```

### 8.2 Pagination Beyond Last Page

**Request:**
```http
GET /api/approvals/?limit=20&offset=1000
Authorization: Bearer <counselor_token>
```

**Response (200):**
```json
{
  "count": 45,
  "results": []
}
```

---

**Contract v0.2 Complete**
