# Phase 4C Complete - Next Steps Strategy Review

**Date:** 2026-06-01  
**Reviewer:** Codex  
**Reviewed:** `docs/discussions/phase4c-next-steps/05-claude-next-steps-strategy-request.md`  
**Review Type:** Strategic Planning Review

## Review Conclusion

**Recommendation: choose a narrowed Option A now, not Option B and not a full wait.**

Do not wait idle for WeChat DevTools. Phase 4C backend is now implemented and tested, and attachment endpoints are concrete enough for frontend integration work. However, the next frontend step should be treated as **Phase 4C frontend code-complete**, not Phase 4C fully complete, because DevTools remains the first real miniprogram compile/runtime gate.

The execution order should be:

1. Add attachment API types and client methods.
2. Add read-only attachment list/download/delete UI on the detail page.
3. Add upload UI to the student application flow only after deciding the UX boundary.
4. Run static/manual source checks now.
5. Require DevTools validation before marking Phase 4C frontend accepted.

This keeps momentum while avoiding the largest rework risk: spreading unverified miniprogram assumptions across multiple pages.

## Risk Assessment

### Option A: Phase 4C Frontend Attachment UI

**Rework risk: medium.** The risk is not the backend contract anymore; the backend has concrete attachment endpoints and tests. The risk is miniprogram runtime behavior because this repo has no local `package.json`, no `tsconfig.json`, and no CLI build/test harness for the miniprogram. DevTools is therefore the practical compiler and runtime verifier.

**Technical risk: medium.** `wx.uploadFile` is not just `wx.request` with a file. The client must handle multipart upload separately: pass `filePath`, use `name: 'file'`, send `attachment_type` via `formData`, include `Authorization`, parse `res.data` manually because upload responses commonly arrive as strings, and treat HTTP 4xx/5xx status codes as failures even when the transport callback succeeds. Download should use `wx.downloadFile` plus `wx.openDocument` for PDF/DOC/DOCX and image preview for JPG/PNG.

**Time risk: medium.** The 3-4 hour estimate is plausible for code-complete UI if scoped tightly, but not for accepted completion. Add 1-2 hours after DevTools becomes available for compile/runtime repair.

**Verdict:** best next option, but only with a bounded code-complete definition and a DevTools acceptance gate.

### Option B: Other Miniprogram Pages

**Rework risk: medium-high.** This spreads the same unverified miniprogram assumptions across more screens. The detail page needs improvement, but doing history pages and approval detail pages before validating current page patterns increases future cleanup.

**Technical risk: medium.** These pages are less exposed to file API quirks, but they still depend on unverified navigation, role routing, WXML binding, and approval action behavior.

**Time risk: high.** The 4-6 hour estimate is likely optimistic if it includes multiple user flows and polish. It also delays the attachment closure that Phase 4C is supposed to deliver.

**Verdict:** defer. Pull only the part that Option A needs: improve the existing detail page enough to show attachments.

### Option C: Wait for DevTools + Validation First

**Rework risk: low.** This is the cleanest path if minimizing frontend churn is the only objective.

**Technical risk: low.** DevTools would expose compile/runtime issues before new code accumulates.

**Time risk: high.** The wait is externally blocked and could cost 1-3 days with little product progress. This is not justified now because backend attachment endpoints are stable enough to integrate against.

**Verdict:** do not choose as the primary plan. Keep DevTools as the completion gate, not the start gate.

## Priority Recommendation

Proceed with **Option A-lite: attachment frontend integration on the existing pages**, with a hard boundary around what is allowed before DevTools.

Recommended first slice:

1. Extend `miniprogram/types/api.ts` with `Attachment`, `AttachmentType`, upload response/error assumptions.
2. Extend `miniprogram/services/api.ts` with:
   - `listAttachments(applicationId)`
   - `deleteAttachment(attachmentId)`
   - `downloadAttachment(attachmentId)` or a helper returning the download URL/header plan
   - `uploadAttachment(applicationId, filePath, attachmentType)` using `wx.uploadFile`, not the generic `request()`
3. Update `miniprogram/pages/detail/detail.*` to load and display attachments for all users who can view the application.
4. Add delete affordance only for the owning student where possible; still rely on backend RBAC.
5. Add upload entry from `student-application` only if the product decision is clear:
   - upload before submit requires draft semantics, which the backend does not currently expose;
   - upload after submit is safer: submit application, redirect to detail, upload attachments there.

That last point is important: the request says "学生申请页面：附件上传组件", but the current backend attachment API attaches files to an existing `application_id`. Unless the frontend first creates the application, there is nothing to upload against. For MVP, the lower-risk UX is **submit first, then upload attachments on detail page**. If the upload must appear on the application page, implement it as a post-submit step or pending-file queue, not as a real upload before application creation.

## Execution Strategy To Reduce Rework

### 1. Make the detail page the attachment hub

The existing detail page already has `applicationId` and loads `ApplicationDetail`. It is the natural place to list, download, and delete attachments. This avoids inventing draft attachment behavior.

### 2. Keep upload state simple

Use one selected file at a time for MVP. Track:

- `uploading`
- `uploadProgress`
- `attachmentError`
- `attachments`

Avoid multi-file batching until DevTools validates the base flow.

### 3. Keep the API adapter explicit

Do not force upload/download through the existing `request<T>()` wrapper. Add dedicated methods because `wx.uploadFile` and `wx.downloadFile` have different response shapes from `wx.request`.

### 4. Treat URL/domain behavior as validation risk

`project.config.json` currently has `urlCheck: false`, which helps local DevTools testing. Real device and production testing still need configured HTTPS request/upload/download domains. Do not let a DevTools-local pass imply production network readiness.

### 5. Define two completion levels

**Frontend code-complete:**

- Attachment types/client methods exist.
- Detail page can list attachments.
- Student can choose and upload an allowed file after an application exists.
- Student owner can delete.
- Viewers can download/open.
- Errors are displayed from backend `error.message` and validation details where useful.
- Source review finds no obvious WXML/TS binding mismatch.

**Phase 4C frontend accepted:**

- All code-complete items pass in WeChat DevTools.
- At least one upload success is proven against the local backend.
- Invalid type or oversize upload shows a backend validation error.
- Student cannot delete someone else's attachment.
- Counselor/dean can view/download according to backend RBAC.
- Re-launch/login/token expiration behavior still works.

Phase 4C frontend should not be marked accepted before DevTools validation. It can be marked "code-complete, pending DevTools".

## Parallel Work

Yes, but keep it bounded:

- Do dorm-system stakeholder/contact/document discovery now, because it is a production blocker and does not depend on DevTools.
- Update a short Phase 4C frontend validation checklist while coding.
- Do not start broad history pages or new approval-detail pages until the attachment detail-page pattern has been validated.

## Alternative Option D

**Option D: attachment adapter + detail read-only first, upload second.**

This is the safest variant if time is tight:

1. Add attachment types and list/download client methods.
2. Add detail-page attachment list and download/open behavior.
3. Stop and wait for DevTools if blocked.
4. Add upload/delete after list/download compiles.

This reduces exposure to `wx.uploadFile` while still making progress on the UI and shared data model. It is a good fallback if the team has less than 2 hours available before DevTools is ready.

## Final Ruling

Claude's initial Option A recommendation is mostly right, but it is too broad in one place: uploading directly on the student application page assumes pre-existing `application_id` semantics that the backend does not provide.

Proceed with **Option A-lite**:

- detail page attachment list/download/delete;
- post-submit upload on detail page;
- dedicated `wx.uploadFile`/`wx.downloadFile` API methods;
- DevTools required for accepted completion;
- dorm-system discovery in parallel.

Do not proceed with broad Option B until this vertical slice is validated.
