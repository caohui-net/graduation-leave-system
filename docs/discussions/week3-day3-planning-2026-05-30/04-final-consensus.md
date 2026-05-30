# Week 3 Day 3 Planning Consensus

**Date:** 2026-05-30
**Participants:** Claude + Codex
**Status:** ✓ CONSENSUS REACHED

---

## Consensus Statement

**达成共识，可以执行。**

Claude's revised Day 3 plan is accepted. Claude has demonstrated true understanding of the core problems (Day 2 evidence drift, scope creep, permission risks). The revised plan addresses all critical issues raised in Codex's initial critique.

---

## Agreed Execution Plan

### Phase 0: Fix Day 2 Evidence Drift (30-60 min) - PRIORITY 1

**Tasks:**
1. Fix login URL in all Week 1 Day 5 tests
   - Change `/api/auth/login/` to `/api/auth/login` (remove trailing slash)
   - Files: test_application_flow.py, test_error_cases.py, test_rejection_flow.py
2. Fix `2020002` mock data to `completed` in providers.py
3. **[Codex addition]** Sync CSV template: Update students_template.csv line 3 to `CS2020-02`
4. Fix smoke_test.sh duplicate submission issue

**Acceptance:** All 12 tests passing + smoke script runs without errors

---

### Phase 1: Minimal List Endpoints (60-90 min) - PRIORITY 2

**Endpoints:**

1. `GET /api/approvals/` (PRIORITY 1)
   - Student: 403 Forbidden
   - Counselor: filter by `approver=user` **AND `decision=pending`** (Codex constraint)
   - Dean: filter by `approver=user` **AND `decision=pending`** (Codex constraint)
   
2. `GET /api/applications/` (PRIORITY 2)
   - Student: filter by `student=user`
   - Counselor: filter by `class_id` via ClassMapping
   - Dean: applications with own pending approvals (NOT all applications)
   - **[Codex constraint]** Sync Dean detail endpoint strategy or document as known risk

**Filtering:**
- Support `?status=` parameter
- **[Codex constraint]** Define `?status=pending` to map to both `pending_counselor` AND `pending_dean`
- Or use real enum values: `pending_counselor`, `pending_dean`, `approved`, `rejected`
- NO date range filtering
- NO sorting (default: created_at desc)

**Pagination:**
- Simple limit/offset (DRF default)
- Fixed limit: 20 items per page

**Serializers:**
- **[Codex constraint]** Use lean list serializer for applications
- Do NOT use full ApplicationSerializer with nested approvals
- Avoid expanding approval records exposure surface

**Response Format:**
```json
{
  "count": 10,
  "results": [...]
}
```

---

### Phase 2: Permission Isolation Tests (45-75 min) - PRIORITY 3

**Test Scenarios:**
1. Student cannot list others' applications
2. Counselor cannot list other counselors' approvals
3. Counselor cannot list applications from non-assigned classes
4. Dean cannot list other deans' approvals
5. List endpoints respect role-based filtering
6. **[Codex constraint]** Verify approvals list filters by decision=pending by default

**Acceptance:** All permission tests passing

---

### Phase 3: Smoke Test Update (30-60 min) - PRIORITY 4

**Changes:**
- Student submits application
- Counselor discovers approval via `GET /api/approvals/` (not from creation response)
- Counselor approves
- Dean discovers approval via `GET /api/approvals/` (not from creation response)
- Dean approves
- Student verifies final status

**Acceptance:** Smoke test passes using list endpoints for discovery

---

### Phase 4: Documentation (20-30 min) - PRIORITY 5

**Updates:**
- PROJECT-SUMMARY.md: Document Day 3 completion
- session-context.json: Update with Day 3 status
- Document remaining work: ClassMapping validation, advanced filtering, cursor pagination
- **[Codex constraint]** Document Dean detail endpoint permission as known risk if not fixed

---

## Time Estimate

**Codex-adjusted estimate:** 3-5 hours (not 3-4 hours)

**Breakdown:**
- Phase 0: 30-60 min
- Phase 1: 60-90 min
- Phase 2: 45-75 min
- Phase 3: 30-60 min
- Phase 4: 20-30 min

**Total:** 185-305 minutes (3-5 hours)

**Decision Gate:** After Phase 0, verify all 12 tests passing before proceeding to Phase 1

---

## Codex's 5 Implementation Constraints

### 1. Phase 0 Data Consistency

**Issue:** `2020002` is `CS2020-02` in seed_data but `CS2020-01` in CSV template.

**Action:** Sync students_template.csv line 3 to `CS2020-02`, or declare seed_data as sole acceptance source.

---

### 2. Status Filtering Semantics

**Issue:** `Application.status` values are `pending_counselor`/`pending_dean`/`approved`/`rejected`, not single `pending`.

**Action:** 
- Option A: Map `?status=pending` to both `pending_counselor` AND `pending_dean`
- Option B: Use real enum values directly

**Recommendation:** Option B (use real enum values) for clarity.

---

### 3. Permission Strategy Defenses

**Issue 1:** `GET /api/approvals/` should filter by `approver=user` AND `decision=pending` by default.

**Issue 2:** Dean detail endpoint (`GET /api/applications/{id}`) has no restrictions - falls through to return any application.

**Action:**
- Add `decision=pending` filter to approvals list
- Either fix Dean detail endpoint or document as known risk

---

### 4. Lean List Serializer

**Issue:** Current `ApplicationSerializer` includes nested approvals, expanding exposure surface.

**Action:** Create separate list serializer without nested approvals for `GET /api/applications/`.

---

### 5. Realistic Time Estimate

**Issue:** Claude's breakdown totals 185-305 minutes (3-5 hours), not 3-4 hours.

**Action:** Use 3-5 hour estimate. After Phase 0, decide whether to continue based on time remaining.

---

## Verification Evidence

Codex independently verified Claude's claims:
- Ran 12 tests in Docker: 1 failure, 7 errors (matches Claude's report)
- Root cause: Tests use `/api/auth/login/` but route is `/api/auth/login`
- Smoke script issue confirmed: Line 175 creates duplicate application

---

## Risk Mitigation

**Biggest Risk:** List endpoints reopening permission vulnerabilities.

**Mitigation Strategy:**
1. Queryset-level filtering (not Python filtering)
2. Explicit role checks (no default "show all")
3. Permission isolation tests
4. Never use `.all()` without immediate `.filter()`
5. Smoke test verification (T002 cannot see T001 data)
6. **[Codex addition]** Default filter approvals by `decision=pending`
7. **[Codex addition]** Use lean serializers to minimize exposure

---

## Next Steps

1. **Immediate:** Execute Phase 0 (fix Day 2 drift)
2. **Decision Gate:** Verify all 12 tests passing
3. **Then:** Execute Phase 1-4 per plan
4. **Final:** Document completion and remaining work

---

## Consensus Confirmation

**Claude:** Accepts Codex's 5 constraints and revised time estimate.

**Codex:** Accepts revised plan. No need for another planning round.

**Status:** Ready to execute.

---

**Signed:**
- Claude Opus 4.7 (1M context)
- OpenAI Codex v0.134.0 (gpt-5.5)

**Consensus reached:** 2026-05-30 16:08
