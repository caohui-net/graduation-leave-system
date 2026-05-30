# Next Phase Strategy - Codex Recommendation

Date: 2026-05-31
Context: Week 3 completed with core workflow, v0.2 contract, backend tests, and miniprogram skeleton.

## Recommendation

Choose a **B-first hybrid**:

1. Make the WeChat miniprogram the primary delivery surface.
2. Add only the smallest backend feature needed for a realistic first user journey: **attachments MVP**.
3. Defer draft save, full audit trail, real dorm provider integration, Redis caching, load testing, and React Native.
4. Do a short DevTools validation gate as soon as DevTools is available, but do not idle waiting for it.

This is not Option A+B at full size. It is **frontend-led MVP integration with one backend expansion**.

## Why This Path

The current product risk is no longer "can the backend enforce the workflow?" Week 3 reduced that risk with 37 backend tests, security coverage, state-machine coverage, and contract v0.2.

The highest remaining risk is now **whether real users can complete the workflow from a client**:

- student creates/submits an application;
- required dorm clearance evidence is visible or uploadable;
- counselor sees assigned work and acts;
- dean sees escalated work and acts;
- errors are understandable at the UI boundary.

More backend features before a usable client increases integration risk because it expands contract surface without exercising it. Pure infrastructure work is premature because there is not yet enough real traffic shape or frontend behavior to optimize around.

## Option Assessment

### A. Week 4 Backend Features

Value: mixed.

Attachments are high value because they are part of real graduation-leave evidence and are already in the design model. Draft save is useful but not essential for first approval flow. Audit trail is important for production accountability but can initially be covered by approval rows and backend logs. Real dorm integration is high-risk because it depends on external contract, credentials, network, and institutional data availability.

Risk: building all A items now creates a larger unvalidated API surface.

Decision: take attachments only, as an MVP.

### B. Frontend Development

Value: highest.

The system only becomes meaningful when students and approvers can operate it. It also flushes out missing contract details faster than backend-only development.

Risk: React Native plus miniprogram doubles effort. Existing discussions already converged toward miniprogram-first. React Native should stay out of the next phase unless there is a confirmed launch requirement.

Decision: B-first, but scope to miniprogram UI and API integration.

### C. Production Readiness

Value: low right now except for CI basics.

Redis caching, query tuning, load testing, monitoring, and logging become more useful once the end-to-end flow exists. Before that, they mostly optimize assumptions.

Risk: infrastructure can hide product gaps by making the project feel mature before it is usable.

Decision: only add a minimal CI smoke path if missing. Defer the rest.

### D. Wait For DevTools

Value: validation matters, but waiting blocks learnable work.

Risk: DevTools may reveal integration defects, but those defects are more likely in lifecycle/API/request handling than in every UI screen. A small contract-compatible UI can still be built now and corrected after validation.

Decision: do not wait. Keep a hard DevTools gate before declaring the frontend phase complete.

## Proposed Scope

### Phase 4A - Client-First Vertical Slice

Target: 3-5 working days.

Build a miniprogram vertical slice against v0.2:

- login role selection or existing auth-compatible mock login;
- student application create/submit screen;
- application list and detail screens;
- counselor/dean approval list;
- approve/reject actions;
- consistent loading, empty, forbidden, validation, and conflict states;
- API service integration using the existing contract types.

Acceptance:

- UI can drive the same core workflow already covered by backend tests;
- no new backend feature is required except attachment placeholder or MVP upload;
- screenshots or manual evidence captured for each role path;
- all backend tests still pass.

### Phase 4B - Attachments MVP

Target: 2-4 working days, can run in parallel with UI if capacity allows.

Implement only:

- attachment model and migration;
- upload endpoint for an application;
- list attachments by application;
- download endpoint with ownership/role authorization;
- delete or soft-delete only if required by current UI;
- file size/type allowlist;
- local storage only;
- backend tests for permissions, validation, and download access.

Do not implement object storage, antivirus, CDN, advanced preview, chunking, or retention policy yet.

Acceptance:

- student can attach required supporting material before or during submission;
- assigned approvers can view/download relevant attachments;
- unauthorized users cannot access attachments;
- contract v0.2 is updated to v0.3-draft only for attachment endpoints.

### Phase 4C - DevTools Gate

Target: immediately when available.

Run the real miniprogram in WeChat DevTools:

- compile passes;
- pages load without lifecycle/runtime errors;
- API base URL configuration works;
- role flows match backend contract;
- failed requests show usable UI states.

Decision after gate:

- if only UI/runtime defects: fix and continue frontend;
- if contract defects: patch contract and backend tests first;
- if platform restrictions affect upload/auth: reduce attachment scope or adjust endpoint design before expanding more backend.

## Explicit Deferrals

- Draft save: defer until users actually need interruption/resume behavior, or after attachments show a real form-length pain.
- Audit trail: defer as a production-control feature; keep approval event data reliable first.
- Real dorm provider: defer until external endpoint/schema/credentials and test data are available.
- Redis caching: defer until query patterns and load targets are known.
- Load testing: defer until a client-driven workflow exists.
- Monitoring/logging: defer full stack; add only basic request/error visibility when deploying a real environment.
- React Native: defer unless stakeholders confirm it is a launch blocker.

## Hidden Blockers To Check Early

- Miniprogram upload API constraints and local dev HTTPS/domain configuration.
- Backend media storage path and Docker volume persistence.
- Auth shape in miniprogram: mock/session/JWT/wechat login boundary.
- File authorization rules for student, counselor, dean, and unrelated users.
- Whether approval detail responses need embedded attachment metadata for UI efficiency.
- Whether the current frontend/miniprogram lacks package or TypeScript build verification.

## Suggested Work Order

1. Define Phase 4 acceptance checklist with role-based screens and attachment MVP boundaries.
2. Build miniprogram screens using mock data first if DevTools remains unavailable.
3. Add attachment backend MVP and tests.
4. Wire miniprogram API calls to backend contract.
5. Run backend tests and any available static checks.
6. Execute DevTools validation as the phase completion gate.

## Bottom Line

The optimal next phase is **not** production readiness and not broad backend expansion. The project should move from "backend workflow proven" to "usable end-to-end product slice proven." The smallest high-value path is miniprogram-first UI plus attachments MVP, with DevTools validation as a required gate before declaring the phase done.
