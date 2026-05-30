# Frontend Contract v0.2

**Date:** 2026-05-31  
**Status:** Frozen for mini-program narrow slice  
**Base URL:** `http://localhost:8001` (dev), TBD (prod)

---

## Authentication

**Method:** JWT Bearer Token

```http
Authorization: Bearer <access_token>
```

**Token obtained from:** `POST /api/auth/login`

---

## Endpoints

### 1. POST /api/auth/login

**Request:**
```json
{
  "user_id": "string",
  "password": "string"
}
```

**Response (200):**
```json
{
  "access_token": "string",
  "user": {
    "user_id": "string",
    "name": "string",
    "role": "student|counselor|dean"
  }
}
```

**Errors:**
- 401: Invalid credentials

**Sample:** `api-samples/01-login-student.json`

---

### 2. POST /api/applications/

**Auth:** Required (Student only)

**Request:**
```json
{
  "reason": "string",
  "leave_date": "YYYY-MM-DD"
}
```

**Response (201):**
```json
{
  "application_id": "integer",
  "student": "string",
  "reason": "string",
  "leave_date": "YYYY-MM-DD",
  "status": "pending",
  "created_at": "ISO8601",
  "updated_at": "ISO8601"
}
```

**Errors:**
- 400: Validation error
- 409: Application already exists (unique constraint)

**Sample:** `api-samples/02-submit-application.json`

---

### 3. GET /api/applications/

**Auth:** Required

**Query Params:**
- `limit` (optional, default 20): Page size
- `offset` (optional, default 0): Pagination offset

**Response (200):**
```json
{
  "count": "integer",
  "next": "string|null",
  "previous": "string|null",
  "results": [
    {
      "application_id": "integer",
      "student": "string",
      "reason": "string",
      "leave_date": "YYYY-MM-DD",
      "status": "pending|approved|rejected",
      "created_at": "ISO8601",
      "updated_at": "ISO8601"
    }
  ]
}
```

**Behavior:**
- Student: sees own applications only
- Counselor/Dean: sees all applications

**Sample:** `api-samples/03-list-applications-student.json`

---

### 4. GET /api/applications/{id}/

**Auth:** Required

**Response (200):**
```json
{
  "application_id": "integer",
  "student": "string",
  "reason": "string",
  "leave_date": "YYYY-MM-DD",
  "status": "pending|approved|rejected",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "approvals": [
    {
      "approval_id": "integer",
      "approver": "string",
      "role": "counselor|dean",
      "decision": "pending|approved|rejected",
      "comment": "string|null",
      "decided_at": "ISO8601|null"
    }
  ]
}
```

**Errors:**
- 404: Application not found
- 403: Permission denied

**Sample:** `api-samples/04-get-application-detail.json`

---

### 5. GET /api/approvals/

**Auth:** Required (Counselor/Dean only)

**Query Params:**
- `limit` (optional, default 20)
- `offset` (optional, default 0)

**Response (200):**
```json
{
  "count": "integer",
  "next": "string|null",
  "previous": "string|null",
  "results": [
    {
      "approval_id": "integer",
      "application": {
        "application_id": "integer",
        "student": "string",
        "reason": "string",
        "leave_date": "YYYY-MM-DD"
      },
      "approver": "string",
      "role": "counselor|dean",
      "decision": "pending",
      "comment": "string|null",
      "decided_at": "ISO8601|null"
    }
  ]
}
```

**Behavior:**
- Only shows pending approvals for current user
- Counselor: sees approvals for students in their class
- Dean: sees approvals after counselor approval

**Sample:** `api-samples/06-list-approvals-counselor.json`

---

### 6. POST /api/approvals/{id}/approve/

**Auth:** Required (Counselor/Dean only)

**Request:**
```json
{
  "comment": "string (optional)"
}
```

**Response (200):**
```json
{
  "approval_id": "integer",
  "decision": "approved",
  "comment": "string|null",
  "decided_at": "ISO8601"
}
```

**Errors:**
- 403: Not your approval or already decided
- 404: Approval not found

**Sample:** `api-samples/07-approve.json`

---

### 7. POST /api/approvals/{id}/reject/

**Auth:** Required (Counselor/Dean only)

**Request:**
```json
{
  "comment": "string (required)"
}
```

**Response (200):**
```json
{
  "approval_id": "integer",
  "decision": "rejected",
  "comment": "string",
  "decided_at": "ISO8601"
}
```

**Errors:**
- 400: Comment required for rejection
- 403: Not your approval or already decided
- 404: Approval not found

---

## Error Format

**Standard error response:**
```json
{
  "error": "string",
  "detail": "string (optional)"
}
```

**HTTP Status Codes:**
- 400: Bad Request (validation error)
- 401: Unauthorized (missing/invalid token)
- 403: Forbidden (permission denied)
- 404: Not Found
- 409: Conflict (duplicate resource)
- 500: Internal Server Error

---

## Known Limitations (v0.2)

1. **No resubmission after rejection** - unique constraint on Application.student
2. **No approved history viewing** - `/api/approvals/` only shows pending
3. **No filtering/search** - list endpoints return all records (paginated)
4. **No sorting** - results ordered by creation time (newest first)

---

## Mini-Program Integration Notes

**Storage:**
- Store `access_token` in `wx.storage`
- Store `user` object for role-based UI

**Error Handling:**
- Map HTTP status codes to user-friendly messages
- 401 → redirect to login
- 403 → show "权限不足"
- 409 → show "申请已存在"

**Pagination:**
- Use `limit=20` for initial load
- Load more with `offset` when scrolling

**HTTPS:**
- Dev: HTTP OK for simulator/dev tools
- Prod: HTTPS required (filing in progress)

---

**API Samples:** `.omc/artifacts/api-samples/*.json`  
**Known Risks:** `.omc/artifacts/week3-known-risks.md`
