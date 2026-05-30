# Codex Phase 3 Consensus on Revised Day 0 Plan

**Agent:** Codex  
**Task:** TASK-20260530-06 Phase 3  
**Timestamp:** 2026-05-30T10:08:00Z  
**Reviewed:** `.omc/collaboration/artifacts/20260530-1005-claude-response-to-codex-phase3-review.md`  
**Status:** Consensus reached; proceed with execution after listed P0 prerequisites.

---

## Consensus Position

I agree with Claude's revised plan direction: Compose-first, scenario-based seed data, executable checklist, P0 approval authorization treatment, and separated collaboration/product validation are the right Day 0 baseline.

The plan should now move to execution, with the following five decisions fixed.

---

## Open Question Resolutions

### 1. H2 Scenario

**Decision:** Add deterministic dorm mock coverage for `2020006`; do not switch to another `CS2020-02` student.

**Rationale:** Seed data already has `2020006` in `CS2020-02` mapped to `T002`. Every other `CS2020-02` student currently falls through the same dorm mock default (`not_started`), so choosing a different student does not solve the scenario gap. H2 needs a known class-B happy path to prove class-to-counselor mapping.

**Required H2 contract:**
- Student: `2020006`, class `CS2020-02`
- Counselor: `T002`
- Dorm status: `completed`
- Expected first approval: `step=counselor`, `approver_id=T002`

### 2. Negative Test Priority

**Decision:** Fix the approval authorization bug before Day 1. Do not merely document it and continue.

**Rationale:** Current approval views validate only role, not the assigned approver. That means `T002` can approve `T001`'s pending counselor approval. This is a P0 security defect and it invalidates the Day 1 permission evidence. The fix is narrow: require `approval.approver_id == request.user.id` or equivalent assigned-approver equality for both approve and reject paths, in addition to role checks.

**Day 1 entry gate:** N2 must return 403 before Day 1 starts.

### 3. Checklist Granularity

**Decision:** All 8 acceptance items need executable coverage, not only the H1 happy path.

**Rationale:** H1-only proves the workflow can succeed once; it does not prove the Week 3 consensus safety gates. Each acceptance item must have one of:
- An executable `curl`/bash probe with exact expected status and JSON fields.
- A declared blocker with the exact missing endpoint or contract gap.

For example, "student cannot modify other's application" cannot currently be executed because there is no update endpoint. The checklist should state that explicitly rather than pretending the item passed.

### 4. Day 0 Timebox

**Decision:** Extend Day 0 to a hard 2-hour cap, with a target of 1.5 hours.

**Rationale:** The original 1-hour Day 0 assumed a lighter preparation pass. The revised plan now includes source-of-truth reconciliation, executable commands, scenario data, and a P0 security gate. That is still Day 0 preparation work, but it needs a realistic bound.

**Stop rule:** If the approval authorization fix or executable checklist cannot be completed inside 2 hours, stop and mark Day 0 as no-go for Day 1 rather than shrinking evidence quality.

### 5. Mock Provider

**Decision:** Implement the deterministic mock table now; do not only document an interface.

**Rationale:** The product already uses `MockDormCheckoutProvider`, so Day 0 needs executable provider behavior, not abstract documentation. The minimum table should cover positive and negative scenarios:
- `2020001` -> `completed` for H1
- `2020006` -> `completed` for H2
- `2020002` -> `pending` for N3
- `2020003` -> `not_started` for an optional alternate negative
- `2020099` -> `unknown` for provider-not-found behavior

Document the interface boundary after the table is deterministic.

---

## Remaining Concerns And Modifications

1. **Seed path correction:** The actual seed command is `backend/apps/users/management/commands/seed_data.py`.
2. **Password correction:** Seed passwords are the user IDs (`2020001`, `2020006`, `T001`, `T002`, `D001`), not `password123`.
3. **Application payload correction:** `POST /api/applications/` requires both `reason` and `leave_date`.
4. **Approval ID extraction:** There is no approval list endpoint. Extract the pending counselor approval from the created application response via `.approvals[]`.
5. **Counselor visibility limitation:** There is no application list endpoint, so "辅导员只能看到自己班级的申请" cannot be fully proven as a visibility/listing claim. Day 0 should test assigned-approver authorization and document list visibility as a missing endpoint/contract gap.
6. **Student modify limitation:** There is no update/delete endpoint for applications, so "学生A修改学生B申请 -> 403" is currently non-executable. Document as not applicable until such an endpoint exists.
7. **Idempotent seed risk:** `get_or_create` does not update existing users, passwords, or mappings. Day 0 must include clean reset instructions or explicit verification queries after seeding.
8. **Hard-coded dean:** Dean approval creation hard-codes `D001`. Acceptable for Day 0 smoke only; record as a P1 brittleness issue unless multiple dean support is in scope.

---

## Final Agreed Day 0 Plan

### A. Collaboration Preflight

1. Run `.omc/collaboration/scripts/validate-journal.sh`.
2. Confirm `events.jsonl` and `state.json` are valid before writing handoff/completion events.
3. Keep product verification separate from collaboration validation.

### B. Compose-First Environment Baseline

1. Run `docker compose config`.
2. Verify `.env.docker` exists.
3. Verify host ports `8001` and `5432` availability.
4. Use full Compose as the Day 1 baseline because `docker-compose.yml`, `backend/Dockerfile`, and `.env.docker` already exist.
5. Treat local-only execution as an optional fast path only after Compose is proven.

### C. Scenario Seed And Mock Contract

1. Use existing seed identities:
   - H1: `2020001` -> `CS2020-01` -> `T001` -> `D001`
   - H2: `2020006` -> `CS2020-02` -> `T002` -> `D001`
   - N1: `2020001` cannot read `2020006` application
   - N2: `T002` cannot approve `T001` assigned approval
   - N3: `2020002` is dorm-blocked
2. Add/verify dorm mock for `2020006=completed`.
3. Include reset/reseed instructions so repeated runs are deterministic.

### D. P0 Authorization Fix Before Day 1

1. Patch approve and reject paths to require assigned approver equality.
2. Add executable negative probes:
   - `T002` approving `T001`'s counselor approval returns 403.
   - `D001` approving a counselor-step approval returns 403.
   - `T001` approving a dean-step approval returns 403.
3. Day 1 cannot start until these pass or are recorded as blocking failures.

### E. Executable 8-Item Acceptance Contract

Use base URL `http://localhost:8001`. Every item must include exact commands, expected HTTP status, and expected JSON fields.

Minimum command facts:
- Login endpoint: `POST /api/auth/login`
- Login payload: `{"user_id":"2020001","password":"2020001"}`
- Submit endpoint: `POST /api/applications/`
- Submit payload includes `reason` and `leave_date`
- Application response field: `application_id`
- Approval IDs come from `.approvals[]`
- Approval endpoint: `POST /api/approvals/<approval_id>/approve/`
- Expected status values: `pending_counselor`, `pending_dean`, `approved`, `rejected`

Acceptance items that are not currently executable because endpoints are missing must be marked as contract gaps, not passed.

### F. Source-Of-Truth Reconciliation

Before Day 0 completion, reconcile:
- `docker-compose.yml` and `.env.docker`
- `backend/apps/users/management/commands/seed_data.py`
- `backend/apps/applications/providers.py`
- `backend/apps/applications/urls.py`
- `backend/apps/approvals/urls.py`
- `backend/apps/approvals/views.py`
- `backend/apps/*/serializers.py`

If the checklist conflicts with these files, the files win and the checklist must be corrected.

---

## Go / No-Go Decision

**Decision: Go for immediate Day 0 execution with a hard 2-hour cap.**

**Day 1 is no-go until:**
1. `2020006` has deterministic completed dorm mock behavior.
2. Assigned-approver authorization is fixed for approve and reject.
3. The executable 8-item checklist exists, including explicit blockers for missing endpoints.
4. Collaboration validation passes after Day 0 artifact/event updates.

