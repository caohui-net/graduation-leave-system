# API Contract v0.3 - Attachment Management

**Status:** Final  
**Date:** 2026-06-01  
**Supersedes:** Contract v0.2  
**Test Coverage:** 19 tests (upload: 5, list: 6, download: 4, delete: 4)

---

## Endpoints

### 1. Upload Attachment

**Endpoint:** `POST /api/applications/{application_id}/attachments/`

**Authorization:** Student only, must own the application

**Request:**
- Content-Type: `multipart/form-data`
- Fields:
  - `file`: File (required)
  - `attachment_type`: String (required) - one of: `dorm_checkout`, `library_clearance`, `finance_clearance`, `other`

**Response (201 Created):**
```json
{
  "attachment_id": "att_<12-char-hex>",
  "attachment_type": "dorm_checkout",
  "file_name": "example.pdf",
  "file_size": 1024000,
  "content_type": "application/pdf",
  "uploaded_at": "2026-06-01T07:00:00Z"
}
```

**Errors:**
- `400 VALIDATION_ERROR`: Invalid file type, size, or missing required fields
  - Includes `details` field with serializer errors
- `403 FORBIDDEN`: Not the application owner or not a student
- `404 NOT_FOUND`: Application does not exist

---

### 2. List Attachments

**Endpoint:** `GET /api/applications/{application_id}/attachments/`

**Authorization:** Users who can view the application (see RBAC rules)

**Response (200 OK):**
```json
{
  "attachments": [
    {
      "attachment_id": "att_<12-char-hex>",
      "attachment_type": "dorm_checkout",
      "file_name": "example.pdf",
      "file_size": 1024000,
      "content_type": "application/pdf",
      "uploaded_at": "2026-06-01T07:00:00Z"
    }
  ]
}
```

**Behavior:**
- Soft-deleted attachments are excluded from results
- Empty array if no attachments

**Errors:**
- `403 FORBIDDEN`: User cannot view this application
- `404 NOT_FOUND`: Application does not exist

---

### 3. Download Attachment

**Endpoint:** `GET /api/attachments/{attachment_id}/download/`

**Authorization:** Users who can view the parent application (see RBAC rules)

**Response (200 OK):**
- Content-Type: Set from `attachment.content_type`
- Content-Disposition: `attachment; filename="<original_filename>"`
- Body: File binary data

**Errors:**
- `403 FORBIDDEN`: User cannot view the parent application
- `404 NOT_FOUND`: Attachment does not exist, is soft-deleted, or file missing from storage

---

### 4. Delete Attachment

**Endpoint:** `DELETE /api/attachments/{attachment_id}/`

**Authorization:** Student only, must own the parent application

**Response (204 No Content):**
- Empty body

**Behavior:**
- Soft delete: sets `is_deleted=True`, `deleted_at=<timestamp>`
- Idempotent: deleting already-deleted attachment returns `404 NOT_FOUND`

**Errors:**
- `403 FORBIDDEN`: Not the application owner or not a student
- `404 NOT_FOUND`: Attachment does not exist or already deleted

---

## RBAC Rules

**Shared permission logic:** `can_view_application(user, application)`

- **Student:** Can view own application (`application.student_id == user.user_id`)
- **Counselor:** Can view if active class mapping exists (`ClassMapping.objects.filter(counselor=user, class_id=application.class_id, active=True).exists()`)
- **Dean:** Can view if has pending dean approval (`Approval.objects.filter(application=application, approver=user, step=ApprovalStep.DEAN, decision=ApprovalDecision.PENDING).exists()`)

**Upload/Delete:** Student only, must own the application

**View/Download:** Any user who can view the application

---

## Error Envelope

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}  // Optional, included for validation errors
  }
}
```

**Validation errors include `details`:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数验证失败",
    "details": {
      "file": ["文件大小超过限制"],
      "attachment_type": ["无效的附件类型"]
    }
  }
}
```

---

## Soft Delete Behavior

- Soft-deleted attachments (`is_deleted=True`) are treated as non-existent
- List endpoint excludes soft-deleted attachments
- Download endpoint returns `404 NOT_FOUND` for soft-deleted attachments
- Delete endpoint returns `404 NOT_FOUND` for already-deleted attachments (not idempotent success)

---

## File Storage Behavior

- Missing storage file (DB row exists but file absent): Download returns `404 NOT_FOUND`
- Content-Type set from `attachment.content_type` field
- File path pattern: `attachments/%Y/%m/%d/<filename>`

---

## Attachment ID Format

- Pattern: `att_<12-char-hex>`
- Example: `att_a1b2c3d4e5f6`
- Collision risk: ~0.0001% at 100K attachments (acceptable for MVP)

---

## Known Limitations

- No file virus scanning
- No file preview/thumbnail generation
- No batch upload
- No attachment versioning
- Docker volume persistence for media files not configured (production follow-up)

---

## Production Follow-Up Items

- Configure Docker volume for `MEDIA_ROOT`
- Add file virus scanning
- Consider increasing attachment ID length to 16 chars for production scale
- Add file size quotas per student
- Add attachment audit log

---

## Implementation Status

**Backend:** Complete (19/19 tests passing, verified 2026-06-01)
- RBAC permission helper implemented
- File upload/download/delete endpoints operational
- Multipart parser configuration fixed (P0 bug resolved)
- Soft delete behavior verified
- Error handling and validation complete
- Test coverage: upload (5), list (6), download (4), delete (4)

**Frontend:** In progress (Phase 4C)
- WeChat Miniprogram UI implementation
- Attachment list/upload/download/delete functionality
- P1 fixes complete: field alignment, error handling, status codes, file precheck
- Awaiting: WXSS styling, static validation, WeChat DevTools acceptance

**Contract Status:** Final (v0.3)
- All fields match backend serializer output
- Response formats verified with backend tests
- No further breaking changes planned for MVP
