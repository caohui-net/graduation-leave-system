# Phase 4C P1 Implementation - Codex Review Response

**Review date:** 2026-06-01  
**Reviewer:** Codex  
**Reviewed input:** `docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md`  
**Review type:** P1 implementation validation

---

## Review Conclusion

**Status: Needs changes before acceptance.**

The frontend P1 fixes for attachment field narrowing, `loadAttachments()` error state, WXML mutually exclusive rendering, download status handling, and file extension precheck are broadly implemented as planned.

However, the current tree does **not** satisfy the summary's backend completion claim. The full attachment backend suite reports 3 upload failures with `415 Unsupported Media Type`, so Contract v0.3 cannot be treated as "Backend complete / 19 tests passing" yet.

---

## Findings

### P0: Upload endpoint rejects multipart requests with 415

**Location:** `backend/apps/attachments/views.py:17-28`, `backend/config/settings/base.py:121-123`

**Observed result:**

```text
python manage.py test apps.attachments.tests.test_upload apps.attachments.tests.test_list apps.attachments.tests.test_download apps.attachments.tests.test_delete -v 2
Ran 19 tests
FAILED (failures=3)

test_upload_success: 415 != 201
test_upload_validation_missing_file: 415 != 400
test_upload_validation_missing_type: 415 != 400
```

**Cause:**

`attachments_view` is the actual DRF entrypoint for both GET and POST. The multipart parser decorator is attached to `upload_attachment`, but `upload_attachment` is only called as a plain helper after DRF has already constructed/parsing the request through `attachments_view`.

Because global `DEFAULT_PARSER_CLASSES` only includes `JSONParser`, multipart upload requests are rejected before the helper-level parser configuration can take effect.

**Required fix:**

Apply `@parser_classes([MultiPartParser, FormParser])` to the DRF entrypoint, or split the upload/list handlers into separately decorated DRF views routed by method/path. After the fix, rerun the 19 explicit attachment tests.

---

### P1: Contract/status documentation overstates backend verification

**Location:** `docs/api/contract-v0.3.md:201-217`, `docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:213-220`

**Issue:**

The contract says backend is complete with 19 tests passing, but only the list suite was validated in the summary, and the full explicit suite currently fails upload tests.

**Impact:**

This can cause the frontend upload work to be accepted against a backend endpoint that currently returns 415 for multipart requests.

**Required fix:**

Either fix the upload parser issue and rerun all 19 tests, or downgrade the implementation status to reflect that only list tests are currently passing.

---

### P2: New attachment UI has no local WXSS coverage yet

**Location:** `miniprogram/pages/detail/detail.wxml:49-71`, `miniprogram/pages/detail/detail.wxss:1-150`

**Issue:**

The new attachment elements use classes such as `attachment-error`, `empty-attachments`, `attachment-list`, `attachment-item`, `attachment-info`, `attachment-actions`, `btn-small`, and `btn-upload`, but `detail.wxss` does not define them.

**Impact:**

This is not a data-contract blocker, and it matches the summary's Step 6 next step. It remains a UI completion gap before WeChat DevTools acceptance.

---

## Validated Items

- `miniprogram/types/api.ts` `Attachment` now matches backend serializer fields: `attachment_id`, `attachment_type`, `file_name`, `file_size`, `content_type`, `uploaded_at`.
- `docs/api/contract-v0.3.md` upload/list examples now match the backend serializer output fields.
- `miniprogram/pages/detail/detail.ts` `loadAttachments()` clears `attachmentError` on success and sets an explicit error state on failure.
- `miniprogram/pages/detail/detail.wxml` renders attachment error, empty state, and list as mutually exclusive branches.
- Download handling now branches on 401/403/404/200 and calls centralized unauthorized handling for 401.
- File extension precheck is aligned with backend extension allowlist: `.jpg`, `.jpeg`, `.png`, `.pdf`, `.doc`, `.docx`.

---

## Verification Commands

```bash
rtk docker compose exec -T backend python manage.py test apps.attachments.tests.test_list -v 2
```

Result: **pass**, 6/6 tests.

```bash
rtk docker compose exec -T backend python manage.py test apps.attachments.tests.test_upload apps.attachments.tests.test_list apps.attachments.tests.test_download apps.attachments.tests.test_delete -v 2
```

Result: **fail**, 16/19 tests pass, 3 upload tests fail with 415.

Package-level label note:

```bash
rtk docker compose exec -T backend python manage.py test apps.attachments.tests -v 2
```

This label fails during Django discovery with `TypeError: expected str, bytes or os.PathLike object, not NoneType`, so explicit test modules should be used for the attachment suite in this environment.

---

## Acceptance Gate

Do not mark Phase 4C P1 as accepted until:

1. Multipart parser configuration is fixed on the actual upload entrypoint.
2. The explicit 19-test attachment suite passes.
3. `contract-v0.3.md` implementation status is updated to match the verified state.
4. Step 6 WXSS styling is completed before WeChat DevTools UI acceptance.
