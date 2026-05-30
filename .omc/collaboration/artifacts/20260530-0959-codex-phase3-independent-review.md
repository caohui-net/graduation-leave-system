# Phase 3 Independent Review: Claude Week 3 Day 0 Analysis

**Agent:** Codex  
**Task:** TASK-20260530-06 Phase 3  
**Timestamp:** 2026-05-30T09:59:00Z  
**Review target:** `.omc/collaboration/artifacts/20260530-0955-claude-phase3-initial-analysis.md`  
**Independence note:** Targeted independent review. I intentionally read Claude's artifact because the user requested a review of that artifact; conclusions below are based on the Week 3 consensus, task definition, system design, and current repository state.

---

## 1. Agreement Points

1. **Day 0 scope is correct.**  
   Claude limits Phase 3 to environment strategy, seed data requirements, and acceptance checklist. That matches the Week 3 consensus Day 0 tasks and TASK-20260530-06 Phase 3 scope.

2. **The environment strategy is directionally aligned with consensus.**  
   The local -> Docker PostgreSQL -> full Compose progression appears in `docs/discussions/week3-direction-2026-05-30/06-consensus.md`. Using a progressive strategy is reasonable if the repository has no established runtime baseline.

3. **The 8 checklist categories are the right top-level categories.**  
   Migration, seed data, login, submit, counselor approval, dean approval, student status query, negative permission, and dorm checkout mock are the minimum loop agreed in Week 3 consensus.

4. **Seed data must include two classes and two counselors.**  
   Claude correctly identifies class-counselor mapping as a required data dependency, not optional test decoration.

5. **Collaboration validation must remain part of the pilot.**  
   TASK-20260530-06 requires validation before pilot, after handoffs, and after completion. Claude's proposal preserves that intent.

---

## 2. Disagreement Points

### D1. The environment decision tree should not be used as a rigid Priority 1 -> 2 -> 3 order now.

Claude's tree treats "local direct run" as Priority 1 and "full Docker Compose" as Priority 3. That is only correct before looking at repo reality. Current repository reality already includes:

- `backend/Dockerfile`
- `docker-compose.yml`
- `.env.docker` expectation
- Django app code under `backend/`
- docs that already selected full Compose in `docs/week3-day0-environment-strategy.md`

The current `docker-compose.yml` runs PostgreSQL 15 and maps backend `8001:8000`. Claude's proposal says to create Compose only if local Python dependencies are missing, and suggests a raw `postgres:14` container for Priority 2. That risks introducing a second, divergent environment path and port/version drift.

**Rationale:** Day 0's goal is reproducible evidence, not fastest local iteration. Once Compose exists, the default should be "use existing Compose unless it fails", with local-only execution treated as an optional fast path after parity is proven.

### D2. The local environment checks are incomplete and partly misleading.

Checking `python3 --version`, `pip3 list`, and `psql` is not sufficient. The checks should inspect:

- whether `backend/manage.py` exists and imports settings
- whether dependencies install through `backend/requirements/base.txt`
- whether `.env.docker` exists and matches Django settings
- whether `docker compose config` succeeds
- whether ports `5432` and `8001` are free, because Compose maps backend to host port `8001`
- whether the selected Python version is compatible with Django 4.2 and project requirements

`pip3 list | grep -E "(Django|Flask|psycopg2)"` is also wrong in emphasis: Flask is irrelevant, and installed global packages do not prove the app can run from `backend/requirements/base.txt`.

### D3. The proposed seed set is not sufficient as stated.

"2 students + 2 counselors + 1 dean" is sufficient only if the two students are in different classes, both can pass dorm checkout when needed, and each has deterministic login credentials. Current implementation does not satisfy that as-is:

- `backend/apps/users/management/commands/seed_data.py` puts `2020001` and `2020002` both in `CS2020-01`.
- The same command has students `2020006`-`2020010` in `CS2020-02`, but Claude's proposed student pair does not use them.
- `backend/apps/applications/providers.py` returns `completed` for `2020001`, but `pending` for `2020002`, so using `2020002` for a normal submit path will fail with dorm blockage.
- The dean is hard-coded as `D001` in `backend/apps/approvals/views.py`; seed data must guarantee that exact user exists or the final approval record creation can fail.

**Required correction:** Define canonical actors by executable IDs, not placeholders:

- primary happy path: `2020001` / `T001` / `D001`
- cross-class or second-class path: either update mock for a `CS2020-02` student to `completed`, or choose an existing `CS2020-02` student and add mock data
- negative path: separate students for forbidden query and a separate counselor for forbidden cross-class approval

### D4. The 8-item checklist is conceptually right but not executable enough.

The checklist must become command- and ID-aware. Current implementation uses string IDs like `app_<uuid>` and `apv_<uuid>`, not numeric `1` and `2`. Any acceptance doc that uses `/api/applications/1` or `/api/approvals/1/approve/` will fail against the current code.

Other feasibility gaps:

- There is no approval list endpoint in `backend/apps/approvals/urls.py`, only direct approve/reject by `approval_id`. "Counselor only sees own class" cannot be proven by list visibility unless such an endpoint exists. It can only be approximated by direct cross-approval negative tests.
- Login returns `access_token`, not `token`.
- App base URL under Compose is likely `http://localhost:8001`, not `http://localhost:8000`.
- `MockDormCheckoutProvider` lives in `backend/apps/applications/providers.py`, not `backend/apps/applications/services/dorm_checkout.py`.
- The expected status should be exact: current code uses `pending_counselor`, `pending_dean`, `approved`, `rejected`. "pending_dean or similar" weakens the contract.

### D5. The negative permission checklist is too narrow.

Claude includes student A cannot query student B. That is necessary but not enough. The more dangerous current bug class is approver authorization:

- `backend/apps/approvals/views.py` verifies the user's role matches the approval step.
- It does not verify `approval.approver == request.user`.

That means any counselor may approve any counselor-step approval if they know the `approval_id`. This directly violates the Week 3 requirement that counselors only approve assigned classes.

The checklist must add:

- counselor `T002` attempts to approve `T001`'s pending approval -> `403`
- dean `D001` attempts to approve a `pending_counselor` approval -> `403`
- counselor attempts final dean approval -> `403`

### D6. Validation frequency should follow collaboration boundaries, not every product substep.

Claude proposes validation after environment decision, seed data creation, and checklist creation. That is acceptable as extra discipline, but it is not the core invariant. The task definition says:

- before pilot
- after each handoff
- after completion

The collaboration journal does not change merely because a product doc section was edited unless an event/state update happens. Running validation after every product substep can burn the Day 0 timebox and gives false confidence about product runtime correctness. Product runtime needs separate checks: `docker compose config`, `migrate`, `seed_data`, API login/submit/approve/query.

Recommended rule: validate journal after every collaboration event/state mutation and at required handoff/completion checkpoints; run product verification commands at product milestones.

---

## 3. Alternative Proposals

### A1. Replace the environment decision tree with a "single reproducible baseline first" strategy.

**Proposal:**

1. Run `docker compose config`.
2. Confirm `.env.docker` exists and required env vars are present.
3. Use existing Compose as the Day 1 baseline.
4. Only use local direct run if Compose fails for an environmental reason and local parity can be documented.
5. Do not introduce a raw `docker run postgres` path unless Compose is absent or demonstrably broken.

**Tradeoff:** This may be slower than local-only iteration, but it avoids three drifting runtime paths and produces better evidence for the Week 3 decision gate.

### A2. Make seed data scenario-based rather than count-based.

**Proposal:**

- Scenario H1: happy path student in class A, counselor A, dean.
- Scenario H2: happy path or at least class-mapping proof for class B.
- Scenario N1: student cannot read another student's application.
- Scenario N2: wrong counselor cannot approve another class.
- Scenario N3: dorm checkout blocked student returns deterministic 422.

**Tradeoff:** This requires either changing seed/mock data or selecting different existing users, but it prevents false success from "counts are present" while the actual flow fails.

### A3. Convert the checklist into a smoke-test contract.

**Proposal:**

Each checklist item should include:

- exact base URL
- exact endpoint
- token variable name
- how to extract `application_id`
- how to extract counselor and dean `approval_id`
- expected HTTP status
- expected JSON fields
- database query only as secondary verification

**Tradeoff:** More work on Day 0, but Day 1/2 avoid manual guesswork and ID drift.

### A4. Treat mock dorm checkout as an executable interface now, not documentation only.

**Proposal:** Keep `MockDormCheckoutProvider` simple, but document and test its deterministic table. Include one completed student and one blocked student in the smoke test.

**Tradeoff:** Slightly expands Day 0 scope, but exposes a currently visible mismatch between seed requirements and provider behavior.

---

## 4. Risks Claude Missed

1. **Current repo state may already supersede the proposal.**  
   Day 0 docs and runtime files exist. The review should reconcile with existing files rather than continue from abstract unknowns.

2. **Seed docs and implementation can drift.**  
   Existing docs say `2020002` is in `CS2020-02` and dorm-completed; code puts it in `CS2020-01` and mock returns dorm `pending`.

3. **Approval authorization is likely P0.**  
   Role-only approval checks let the wrong counselor approve another class's request.

4. **Hard-coded dean identity is brittle.**  
   Approval creation hard-codes `D001` and `赵主任`, which couples seed data, code, and docs.

5. **Repeatability is not defined.**  
   Existing database volumes and duplicate application prevention can make a second smoke run fail with `409`. Day 0 should define reset or cleanup commands.

6. **API examples may not match real URLs.**  
   Compose maps host `8001`, auth path is `/api/auth/login`, application paths include trailing slash behavior, and IDs are string UUID-like values.

7. **"Sees only assigned class" may be unverifiable with current endpoints.**  
   Without list endpoints, visibility requirements need to be rewritten as direct authorization checks or the endpoint must be added.

8. **Role naming is inconsistent across documents.**  
   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.

9. **Migration success alone is too weak.**  
   It should include `showmigrations`, required table existence, and a clean migration run from an empty DB volume. Otherwise existing volumes can hide migration problems.

10. **No explicit architecture-blocker trigger in the Day 0 artifacts.**  
   Week 3 consensus says state machine, data model, or contract conflicts should stop expansion work. Day 0 checklist should mark these as stop conditions.

---

## 5. Recommended Changes

1. **Change environment recommendation:** use existing Docker Compose as the default Day 1 baseline; demote local-only and raw Docker PostgreSQL to fallback paths with explicit parity criteria.

2. **Update environment checks:** add `docker compose config`, `.env.docker` presence, `backend/manage.py check`, port `8001`, dependency file checks, and DB readiness checks.

3. **Fix seed specification:** replace placeholders with actual IDs and ensure at least one student per class can complete dorm checkout. Either update the mock for a `CS2020-02` student or choose seed users that match the mock.

4. **Add seed drift checks:** verify class distribution, active mappings, exact role values, `D001` existence, and idempotent rerun behavior. Include cleanup/reset instructions for repeated smoke tests.

5. **Make checklist executable:** remove numeric ID assumptions, capture IDs from API responses, use exact statuses, exact token field `access_token`, and exact Compose base URL.

6. **Expand negative permission tests:** add cross-counselor approval denial and wrong-step approval denial. This should be considered P0 because current code appears vulnerable.

7. **Clarify mock provider requirement:** document the real file path `backend/apps/applications/providers.py`, the DTO fields, deterministic statuses, timeout/failure placeholders, and at least one blocked response.

8. **Separate collaboration validation from product verification:** keep `validate-journal.sh` at protocol boundaries; add product commands for Compose, migration, seed, and API smoke path.

9. **Add a Day 0 source-of-truth reconciliation step:** compare `docs/week3-day0-*.md`, `seed_data.py`, `providers.py`, routes, serializers, and Compose before declaring the preparation complete.

10. **Record stop gates explicitly:** if state names, role names, approval ownership, or data model constraints conflict, stop Week 3 expansion and classify the issue before patching around it.

---

## Review Conclusion

Claude's analysis is aligned with the agreed Day 0 themes, but it is too abstract for the current repository state. The biggest flaws are the rigid environment priority order, count-based seed sufficiency, under-specified executable checklist, and missing approval authorization risk. I do not recommend proceeding to Day 1 until the Day 0 artifacts are reconciled with the actual code and the negative permission checks are expanded.
