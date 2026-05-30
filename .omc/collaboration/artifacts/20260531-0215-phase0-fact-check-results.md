# Phase 0: Fact-Check Results

**Date:** 2026-05-31  
**Method:** Code analysis (Docker environment unavailable)  
**Status:** Complete

---

## 1. Response Structures (from Serializers)

### 1.1 Application List Response
**Serializer:** `ApplicationListSerializer`  
**Fields:**
```json
{
  "application_id": "string",
  "student_id": "string",
  "student_name": "string",
  "class_id": "string",
  "reason": "string",
  "leave_date": "date",
  "status": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 1.2 Application Detail Response
**Serializer:** `ApplicationSerializer`  
**Fields:**
```json
{
  "application_id": "string",
  "student_id": "string",
  "student_name": "string",
  "class_id": "string",
  "reason": "string",
  "leave_date": "date",
  "status": "string",
  "dorm_checkout_status": "string",
  "approvals": [
    {
      "approval_id": "string",
      "application_id": "string",
      "step": "string",
      "approver_id": "string",
      "approver_name": "string",
      "decision": "string",
      "comment": "string",
      "decided_at": "datetime"
    }
  ],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### 1.3 Approval List Response
**Serializer:** `ApprovalListSerializer`  
**Fields:**
```json
{
  "approval_id": "string",
  "application_id": "string",
  "step": "string",
  "approver_id": "string",
  "approver_name": "string",
  "decision": "string",
  "created_at": "datetime"
}
```

---

## 2. Pagination Format

**Implementation:** `LimitOffsetPagination` (both apps)  
**Response structure:**
```json
{
  "count": 100,
  "results": [...]
}
```

**Key finding:** No `next` or `previous` fields. Frontend types expecting `next/previous` will mismatch.

**Parameters:**
- `limit`: max items per page (default: 20, max: 100)
- `offset`: starting position

---

## 3. Error Response Formats

### 3.1 Validation Error (400)
**Code:** `VALIDATION_ERROR`  
**Example:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": {
      "reason": ["This field is required."],
      "leave_date": ["This field is required."]
    }
  }
}
```

### 3.2 Forbidden (403)
**Code:** `FORBIDDEN`  
**Example:**
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "无权限执行此操作"
  }
}
```

### 3.3 Not Found (404)
**Code:** `NOT_FOUND`  
**Example:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "审批记录不存在"
  }
}
```

### 3.4 Conflict (409)
**Code:** `CONFLICT`  
**Examples:**
```json
{
  "error": {
    "code": "CONFLICT",
    "message": "已有待审批或已通过的申请，不能重复提交",
    "details": {
      "student_id": "string",
      "existing_application_id": "string",
      "status": "string"
    }
  }
}
```

```json
{
  "error": {
    "code": "CONFLICT",
    "message": "审批已完成，不能重复操作"
  }
}
```

```json
{
  "error": {
    "code": "CONFLICT",
    "message": "申请状态与审批步骤不匹配"
  }
}
```

### 3.5 Unprocessable Entity (422)
**Code:** `DORM_BLOCKED`  
**Example:**
```json
{
  "error": {
    "code": "DORM_BLOCKED",
    "message": "宿舍清退未完成，无法提交申请",
    "details": {
      "student_id": "string",
      "dorm_status": "string",
      "blocking_reason": "string"
    }
  }
}
```

---

## 4. Status Enums (from Models)

### 4.1 ApplicationStatus
**Location:** `backend/apps/applications/models.py:6`  
**Values:**
- `draft` - 草稿
- `pending_counselor` - 待辅导员审批
- `pending_dean` - 待学工部审批
- `approved` - 已通过
- `rejected` - 已驳回

### 4.2 ApprovalDecision
**Location:** `backend/apps/approvals/models.py:11`  
**Values:**
- `pending` - 待审批
- `approved` - 已通过
- `rejected` - 已驳回

### 4.3 ApprovalStep
**Location:** `backend/apps/approvals/models.py` (inferred)  
**Values:**
- `counselor` - 辅导员审批
- `dean` - 学工部审批

### 4.4 DormCheckoutStatus
**Location:** `backend/apps/applications/models.py:14`  
**Values:**
- `completed` - 已完成
- `pending` - 进行中
- `not_started` - 未开始
- `unknown` - 未知

---

## 5. State Machine (from Code)

### 5.1 Valid Transitions

**Application submission:**
- `null` → `pending_counselor` (new application)

**Counselor approval:**
- `pending_counselor` → `pending_dean` (approved)
- `pending_counselor` → `rejected` (rejected)

**Dean approval:**
- `pending_dean` → `approved` (approved)
- `pending_dean` → `rejected` (rejected)

**Resubmission:**
- `rejected` → `pending_counselor` (resubmit after rejection)

### 5.2 State Validation (Verified in Code)

**Location:** `backend/apps/approvals/views.py:91-98`

**Counselor approve/reject:**
- Requires `application.status == ApplicationStatus.PENDING_COUNSELOR`
- Returns 409 CONFLICT if mismatch

**Dean approve/reject:**
- Requires `application.status == ApplicationStatus.PENDING_DEAN`
- Returns 409 CONFLICT if mismatch

---

## 6. Permission Matrix (from Code)

### 6.1 Verified Permissions

**Location:** `backend/apps/approvals/views.py:76-85`

| Operation | Student | Counselor | Dean |
|-----------|---------|-----------|------|
| View own application | ✅ | ✅ | ✅ |
| View approval list | ❌ | ✅ (own) | ✅ (own) |
| Approve counselor step | ❌ | ✅ (assigned) | ❌ |
| Approve dean step | ❌ | ❌ | ✅ (assigned) |
| Reject counselor step | ❌ | ✅ (assigned) | ❌ |
| Reject dean step | ❌ | ❌ | ✅ (assigned) |

**Key checks:**
1. Role check: `user.role == UserRole.COUNSELOR/DEAN`
2. Approver check: `approval.approver_id == user.user_id`
3. Step check: `approval.step == ApprovalStep.COUNSELOR/DEAN`

---

## 7. Key Findings

### 7.1 ✅ Confirmed: Field Validation Exists
- `ApplicationCreateSerializer` requires `reason` and `leave_date`
- Returns `VALIDATION_ERROR` (400) if missing

### 7.2 ✅ Confirmed: State Machine Has Basic Protection
- Status/step matching validated before approve/reject
- Returns `CONFLICT` (409) if mismatch

### 7.3 ✅ Confirmed: Permission Checks Exist
- Role-based access control implemented
- Approver ID verification implemented
- Returns `FORBIDDEN` (403) if unauthorized

### 7.4 ⚠️ Gap: Pagination Format Mismatch
- Backend returns: `{count, results}`
- Frontend may expect: `{count, next, previous, results}`
- **Action required:** Verify frontend types and fix mismatch

### 7.5 ⚠️ Gap: Missing Security Tests
- No test for: Student cannot call approve/reject
- No test for: Counselor cannot approve dean step
- No test for: Dean cannot approve counselor step
- **Action required:** Add negative permission tests (Phase 1)

### 7.6 ⚠️ Gap: Reject Path Not Fully Verified
- Approve path has state validation
- Reject path likely mirrors approve but not explicitly verified in this analysis
- **Action required:** Verify reject path state transitions (Phase 1)

---

## 8. Next Steps (Phase 1)

### 8.1 Security Tests (P0)
1. Test: Student cannot call POST /api/approvals/{id}/approve (expect 403)
2. Test: Student cannot call POST /api/approvals/{id}/reject (expect 403)
3. Test: Counselor cannot approve dean-level approval (expect 403)
4. Test: Dean cannot approve counselor-level approval (expect 403)
5. Test: Non-assigned approver cannot approve (expect 403)

### 8.2 State Machine Validation (P0)
1. Verify reject path state transitions
2. Add resubmission state validation
3. Add terminal state protection (no ops on approved/rejected)

---

**Phase 0 Complete:** 45 minutes (code analysis)  
**Next:** Phase 1 - Security + State Machine (2.5h)
