# Week 3 Execution Plan - Final Consensus

**Date:** 2026-05-31  
**Status:** Consensus reached (Claude decision after Codex consultation failure)  
**Total Time:** 5.5-6h (pragmatic compromise)

---

## Decision Rationale

Codex consultation failed to produce response. Proceeding with pragmatic compromise based on:
1. Code verification confirms field validation exists
2. Security tests are P0 (non-negotiable)
3. State machine needs minimal hardening
4. Contract needs realistic time allocation

---

## Execution Plan

### Phase 0: Fact-Check (30-45 min)
**Status:** Ready to execute

**Tasks:**
1. Run backend test suite
2. Capture real API responses (applications, approvals, pagination, errors)
3. Document current response shapes
4. Verify pagination format (count/results vs next/previous)

**Output:** `fact-check-results.md` with real API samples

---

### Phase 1: Security + State Machine (2.5h)
**Status:** Pending Phase 0

**Tasks:**

**1.1 Negative Permission Tests (1.5h) - P0**
- Student cannot call approve/reject endpoints (403)
- Counselor cannot approve dean-level approvals (403)
- Dean cannot approve counselor-level approvals (403)
- Non-assigned approver cannot approve (403)

**1.2 State Machine Hardening (1h) - P0**
- Verify reject path state transitions
- Add resubmission state validation
- Add terminal state protection (no ops on approved/rejected)

**Output:** Test suite passing, state machine validated

---

### Phase 2: Contract Convergence (2h)
**Status:** Pending Phase 1

**Tasks:**

**2.1 Document Enums (30 min)**
- ApplicationStatus (draft, pending_counselor, pending_dean, approved, rejected)
- ApprovalDecision (pending, approved, rejected)
- ApprovalStep (counselor, dean)
- DormCheckoutStatus (completed, pending, not_started, unknown)

**2.2 Document State Machine (30 min)**
- State transition diagram
- Valid transitions table
- Invalid transition handling

**2.3 Document API Samples (45 min)**
- Use real responses from Phase 0
- Include error samples (400, 403, 404, 409, 422, 500, 503)
- Include pagination samples
- Include filter samples (decision=pending/approved/rejected/all)

**2.4 Document Permission Matrix (15 min)**
- 3 roles × 5 operations matrix
- Based on verified permission tests

**Output:** `docs/api/contract-v0.2.md`

---

### Phase 3: Type/Mock Alignment (45-60 min)
**Status:** Pending Phase 2

**Tasks:**
1. Fix PaginatedResponse type (next/previous vs count/results)
2. Verify frontend/types/api.ts matches contract
3. Verify miniprogram/types/api.ts matches contract
4. Fix frontend/services/mock.ts to match real responses
5. Document any intentional differences

**Output:** Types and mocks aligned with contract

---

## Deferred to Week 4

- Attachments support
- Draft save functionality
- Independent audit trail
- Provider fallback strategies
- Real dorm provider tests
- Complete client error handling guide
- WeChat DevTools verification

---

## Success Criteria

**Week 3 Complete when:**
- ✅ Backend test suite passes
- ✅ Security permission tests pass (student/counselor/dean role boundaries)
- ✅ State machine validated (approve/reject/resubmit paths)
- ✅ v0.2 contract documents real API behavior
- ✅ Frontend/miniprogram types match contract
- ✅ Mock fixtures match real responses

---

## Execution Start

**Next action:** Execute Phase 0 (fact-check)
