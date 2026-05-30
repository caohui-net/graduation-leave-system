# Day 0 Verification: Phase 3 Entry Gate

**Task:** TASK-20260530-06 Phase 3  
**Verifier:** Codex  
**Verified at:** 2026-05-30T14:25:00Z  
**Input artifact:** `.omc/collaboration/artifacts/20260530-1015-day0-completion.md`

## 1. Code Review

### P0 fix 1: 2020006 dorm mock

**Status:** PASS

`backend/apps/applications/providers.py` includes a deterministic mock entry for student `2020006`:

- `student_id="2020006"`
- `status=DormCheckoutStatus.COMPLETED`
- no blocking reason or provider error

This satisfies the class B happy-path prerequisite. Seed data also includes `2020006` in `CS2020-02`, mapped to counselor `T002`, so this mock can exercise the second class/counselor path.

### P0 fix 2: approval authorization

**Status:** PASS

`backend/apps/approvals/views.py` now checks assigned approver identity in both action handlers:

- `approve_approval`: rejects when `approval.approver_id != user.user_id`
- `reject_approval`: rejects when `approval.approver_id != user.user_id`

This closes the cross-counselor approve/reject gap for pending approval records. The check is correctly placed after role validation and before mutation.

### Residual code concerns

- Existing automated tests do not cover the new cross-counselor negative case. Add explicit approve and reject tests for `T001` attempting to act on a `T002` approval.
- Existing test modules are stale against current routes. `python manage.py test apps.applications.tests.test_application_flow apps.applications.tests.test_error_cases apps.approvals.tests.test_rejection_flow` finds 8 tests but fails because tests call `/api/auth/login/` while the current route is `/api/auth/login`.
- `GET /api/applications/{id}/` still only restricts students from viewing others' applications. Counselors/deans can still view arbitrary applications. This is outside the Day 0 P0 fix scope but should remain a Day 1/Day 2 security finding.

## 2. Entry Gate Status

| Gate | Status | Evidence |
| --- | --- | --- |
| 2020006 dorm mock = completed | PASS | `backend/apps/applications/providers.py` has `2020006` with `DormCheckoutStatus.COMPLETED`. |
| Approval authorization fixed | PASS | `approve_approval` and `reject_approval` both check `approval.approver_id != user.user_id`. |
| Executable checklist exists | FAIL | `docs/week3-day0-acceptance-checklist.md` exists, but it is not executable as written. |
| Validation passed | PASS | `.omc/collaboration/scripts/validate-journal.sh` passed with 44 valid events, no duplicate IDs, matching state, and no residual locks. |

## 3. Checklist Readiness

**Status:** NOT READY

The checklist exists and has the right 8 acceptance categories, but several command examples are known-wrong for the current API/runtime:

- Uses `http://localhost:8000`; Docker Compose maps backend to host port `8001`.
- Documents login response field as `token`; implementation returns `access_token`.
- Uses hard-coded numeric IDs such as `/api/applications/1` and `/api/approvals/1/approve`; implementation creates IDs like `app_<hex>` and `apv_<hex>`.
- Omits trailing slashes on application and approval detail/action routes where current URL patterns require them.
- The embedded smoke script parses `.token`, hard-codes approval IDs `1` and `2`, and would not reproduce the current flow.
- Step 7 includes PATCH/update validation even though no update endpoint exists.

Because the Day 1 gate required an executable checklist, these issues are blockers for acceptance testing, even though the two P0 code fixes are correct.

## 4. Verification Performed

- Inspected Day 0 completion artifact.
- Inspected `backend/apps/applications/providers.py`.
- Inspected `backend/apps/approvals/views.py`.
- Inspected seed data for `2020006`, `CS2020-02`, `T002`, and `D001`.
- Inspected current auth/application/approval URL patterns and login serializer.
- Ran collaboration validation: passed.
- Ran existing targeted Django tests: tests are discoverable by module path but fail due stale test route assumptions; no product regression conclusion can be drawn from that suite.

## 5. Go/No-Go Decision

**Decision:** NO-GO for Day 1 acceptance testing as currently documented.

Day 1 should not start from `docs/week3-day0-acceptance-checklist.md` until the checklist is corrected or replaced with an executable smoke script. Starting now would waste the Day 1 window on known documentation/script drift rather than testing the product.

## 6. Required Blockers To Clear

1. Update `docs/week3-day0-acceptance-checklist.md` to use `BASE_URL=http://localhost:8001`.
2. Replace all `token` parsing with `access_token`.
3. Align endpoint paths with current URL patterns:
   - `/api/auth/login`
   - `/api/applications/`
   - `/api/applications/{application_id}/`
   - `/api/approvals/{approval_id}/approve/`
   - `/api/approvals/{approval_id}/reject/`
4. Remove hard-coded numeric application/approval IDs; dynamically extract `application_id` and pending `approval_id` values from API/database responses.
5. Remove or clearly mark PATCH/update validation as skipped because no update endpoint exists.
6. Add explicit cross-counselor negative checks for both approve and reject using the `2020006`/`T002` path and an unauthorized `T001` action.
7. Prefer creating `tests/smoke_test.sh` or equivalent executable script, because the checklist alone is currently too easy to drift.

After these blockers are cleared, the Day 1 execution plan should be:

1. Reset/migrate/seed the Docker Compose database.
2. Run a scripted happy path for `2020001`/`T001`/`D001`.
3. Run a scripted class B happy path or setup path for `2020006`/`T002`.
4. Run negative authorization checks: other student read, cross-counselor approve, cross-counselor reject.
5. Record exact command output, response status codes, response bodies, and any P0/P1/P2 findings.
