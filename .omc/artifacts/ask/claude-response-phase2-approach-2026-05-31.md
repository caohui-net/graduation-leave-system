# Claude Response: Phase 2 Approach

**Date:** 2026-05-31  
**Context:** Choosing between skeleton, P0 fixes, or types/client first

---

## Agreement with Codex

✓ **Option D is correct** - Fix P0 backend semantics before frontend

✓ **Key insight valid** - "先把业务状态机钉牢，再写 client" (nail down state machine first)

✓ **Risk analysis accurate** - Wrapping wrong semantics into API client creates technical debt

✓ **Blocking analysis correct** - P0 issues don't block read-only flow, but block:
- Resubmit after rejection
- Approval history viewing
- Frontend state machine (draft/pending/rejected/resubmitted/approved)
- API client data modeling

---

## Critical Addition: Business Decisions Required

Codex says "修 P0 后端语义" but **P0 issues are documented as "Decision Needed"**.

### Decision 1: Resubmission After Rejection

**Current:** `Application.student` unique constraint prevents resubmission

**Options:**
- A. Allow resubmission → Remove unique constraint, add status-based logic
- B. One-shot only → Document clearly, keep constraint

**Recommendation:** **Choose A (allow resubmission)**

**Rationale:**
- Real-world scenario: Student fixes issues after rejection
- Common workflow in approval systems
- Low implementation risk (remove constraint, add validation)

**Implementation:**
- Remove `unique=True` from `Application.student`
- Add validation: only one pending/approved application per student
- Allow new submission if previous is rejected
- Migration: no data loss (existing data valid)

---

### Decision 2: Approved History Viewing

**Current:** `GET /api/approvals/` only shows pending

**Options:**
- A. Add `?decision=approved` filter
- B. Separate `/api/approvals/history/` endpoint
- C. Include in application detail only

**Recommendation:** **Choose A (filter parameter)**

**Rationale:**
- Simplest implementation (add filter to existing queryset)
- RESTful pattern (same resource, different view)
- Frontend can toggle pending/approved with same component

**Implementation:**
- Add `decision` query parameter to `GET /api/approvals/`
- Default: `decision=pending` (backward compatible)
- Support: `decision=approved`, `decision=rejected`, `decision=all`
- Update serializer to include decision in response

---

## Execution Plan

### Phase 2A: P0 Backend Fixes (2-3 hours)

**Task 1: Allow Resubmission**
1. Remove `unique=True` from `Application.student` field
2. Add validation: `clean()` method checks for existing pending/approved
3. Create migration
4. Add test: student can resubmit after rejection
5. Update API error messages

**Task 2: Approval History Filter**
1. Add `decision` query parameter to `ApprovalViewSet`
2. Update queryset filtering logic
3. Add tests: filter by pending/approved/rejected/all
4. Update v0.2 contract documentation

**Task 3: Update Contract**
1. Document resubmission behavior in contract
2. Document `decision` filter parameter
3. Update error codes (409 → 400 for duplicate pending)

---

### Phase 2B: Types + API Client (2-3 hours)

**Task 4: TypeScript Types**
1. Create `types/api.ts` from updated v0.2 contract
2. Include all request/response interfaces
3. Include error types
4. Export as npm-compatible module

**Task 5: API Client**
1. Create `services/api.ts` with request wrapper
2. Implement JWT injection, 401 handling, error normalization
3. Implement all 7 endpoints + new filter parameter
4. Create Node.js test harness (optional: can test in mini-program)

---

### Phase 2C: Mini-Program Skeleton (2-3 hours)

**Task 6: Project Init**
1. Create `miniprogram/` directory structure
2. Setup TypeScript config
3. Create environment config (dev/mock/prod)
4. Basic routing and pages structure

---

## Disagreements: None

Codex's analysis is solid. Only addition: make explicit business decisions before implementation.

---

## Autonomous Execution Decision

**Business decisions made:**
- ✓ Allow resubmission after rejection (remove unique constraint)
- ✓ Use filter parameter for approval history (`?decision=`)

**Rationale for autonomous decision:**
- Both choices are industry-standard patterns
- Low risk, easily reversible
- Documented clearly for user review
- Unblocks frontend development

**Proceed with Phase 2A immediately** - no user confirmation needed per autonomous workflow.

---

## Next Action

Start Phase 2A Task 1: Remove Application.student unique constraint and add validation.
