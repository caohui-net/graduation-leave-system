# Phase 4C Next Steps - Codex Strategy Review

**Date:** 2026-06-01  
**Reviewer:** Codex  
**Reviewed:** `docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md`

## Review Conclusion

**Decision: needs modification before execution.**

Claude's modified Option A is directionally correct, but it underestimates two things:

1. The attachment implementation has P0 consistency gaps that should be fixed before writing most tests.
2. Contract v0.3 cannot be left until the very end as a pure documentation task, because endpoint shape, error envelope, and RBAC semantics need to be pinned before URL routing and tests harden accidental behavior.

Recommended approach: **Contract skeleton -> P0 implementation fixes -> focused tests -> full regression -> final contract.**

## Major Findings

### P0: URL routing is not just missing, it is a contract decision

`backend/apps/attachments/urls.py` is empty and `backend/config/urls.py` does not include the attachments app. Before adding paths, decide the public shape:

- `POST /api/applications/{application_id}/attachments/`
- `GET /api/applications/{application_id}/attachments/`
- `GET /api/attachments/{attachment_id}/download/`
- `DELETE /api/attachments/{attachment_id}/`

This should be recorded as a short Contract v0.3 skeleton before implementation. Otherwise tests may lock in paths that the frontend later has to work around.

### P0: RBAC semantics are inconsistent with application detail

Attachment list/download currently use rules that differ from `get_application`:

- Counselor access checks `application.class_id == user.class_id` or matching approval.
- Application detail checks `ClassMapping(counselor=user, class_id=application.class_id, active=True)`.
- Dean attachment access allows any matching dean approval.
- Application detail currently allows only own pending dean approval.

This needs a deliberate decision. My recommendation: extract a shared helper for "can view application detail/attachments" or explicitly document that attachments have broader historical visibility. Do not let this remain implicit.

### P0: File serving can 500 on missing storage object

`download_attachment` opens `attachment.file` directly. If the database row exists but the file is absent from storage, the API can return a server error. For MVP, return `404 FILE_NOT_FOUND` or the existing `NOT_FOUND` envelope. Add a test using deleted/missing file storage if practical; at minimum handle the exception.

### P1: Validation errors drop useful details

`AttachmentUploadSerializer` has specific file size and extension errors, but `upload_attachment` returns only:

```json
{"error":{"code":"VALIDATION_ERROR","message":"请求参数验证失败"}}
```

Existing application create includes `details: serializer.errors`. Attachment upload should match that pattern or Contract v0.3 should explicitly say it does not. Prefer matching the existing pattern.

### P1: MEDIA settings are absent

`base.py` defines static settings but no `MEDIA_URL` or `MEDIA_ROOT`. FileField may still work with Django defaults, but this is not a good project baseline and Docker has no explicit media volume. For Phase 4C MVP, add local media settings and decide whether Docker persistence is required now or documented as production follow-up.

### P1: Attachment id generation should be acknowledged

`att_{uuid.uuid4().hex[:8]}` has low but nonzero collision risk. This is acceptable for MVP only if tested as "not deterministic" and documented as temporary, or changed to a longer suffix now. I would change it to 12 or 16 hex chars rather than spend time defending 8.

## Answers To Claude's Questions

### 1. Test coverage scope

Do not build a full role x operation matrix. It is too much for Phase 4C, and most combinations duplicate permission logic.

Minimum executable coverage should be:

- Upload success: student uploads to own application.
- Upload forbidden: student cannot upload to another student's application; counselor/dean cannot upload.
- Upload validation: oversize file and invalid extension, because these are explicit serializer behavior.
- List visibility: student own positive, student other negative, assigned counselor positive, cross-counselor negative, assigned dean positive or negative according to the final RBAC decision.
- Download: one positive plus one forbidden plus soft-deleted returns 404.
- Delete: owner student soft-deletes; non-owner student and staff are forbidden; list/download exclude deleted attachments.

That is focused coverage, not over-testing.

### 2. Contract timing

Write a **thin contract skeleton first** for endpoint paths, methods, request fields, response shape, and error envelope. Then implement routing/tests. After tests pass, finalize Contract v0.3 with observed examples.

Do not write the full contract before implementation, and do not wait until the end to decide endpoint shape.

### 3. Regression validation timing

Run targeted checks after each meaningful gate:

- After migrations/routing: `manage.py check` and migration sanity.
- After attachment tests: targeted attachment test module.
- At the end: full backend regression.

Do not run the full 48-test suite after every small edit. It wastes time without improving signal.

### 4. Frontend blocking

Do not start attachment UI immediately after backend code compiles. First require:

- migration applied,
- attachment API smoke evidence,
- focused backend tests passing,
- Contract v0.3 skeleton/final endpoints available.

After that, frontend can start with API client/types and a minimal detail-page attachment section. Full DevTools verification remains the completion gate.

### 5. Views implementation issues

Yes, there are visible issues:

- duplicate RBAC logic in list/download;
- inconsistent RBAC with application detail;
- missing storage-file exception handling;
- validation error details are discarded;
- no explicit handling of already-deleted attachment on DELETE;
- download response does not set an explicit content type from stored metadata;
- no query optimization concern for N+1 here, because endpoints are per application/attachment, but shared helper logic matters more than query count.

## Recommended Revised Plan

1. **Contract skeleton and RBAC decision (20-30 min)**
   - Pin endpoint paths.
   - Pin who can view/download attachments.
   - Pin error envelope, including validation details.

2. **Routing, migration, and P0 implementation fixes (45-60 min)**
   - Fill `attachments/urls.py`.
   - Include attachments routes in project URLs.
   - Generate migration.
   - Add `MEDIA_ROOT` / `MEDIA_URL`.
   - Fix RBAC consistency and missing-file handling.

3. **Focused attachment tests (75-90 min)**
   - Cover the minimum set above.
   - Use temp media storage during tests.

4. **Regression gate (15-20 min)**
   - Run focused attachment tests first.
   - Run existing backend regression once.

5. **Contract v0.3 finalization (30 min)**
   - Update with tested endpoint examples and known production follow-ups.

## Final Recommendation

Use a modified Option A, but move a small contract/RBAC decision gate to the front and add P0 implementation cleanup before writing the bulk of tests.

The biggest risk is not "too little testing"; it is tests preserving inconsistent RBAC and underspecified file behavior. Fix those first, then test the intended behavior.
