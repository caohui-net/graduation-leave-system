# Week 3 Follow-up List

**Created:** 2026-05-31  
**Based on:** Codex Path 5 Consensus  
**Status:** Ready for execution

---

## Context

Phase 2 (backend P0 fixes) and Phase A (miniprogram skeleton) are complete and verified. Per Codex analysis, we must now return to Week 3 original goal: **core workflow strengthening + v0.2 contract convergence**.

**Scope frozen:**
- ✓ Backend core APIs working
- ✓ Miniprogram skeleton created
- ✗ No further miniprogram development until DevTools verification
- ⏳ Focus on backend workflow completeness and contract stability

---

## P0: Core Workflow Strengthening

### 1. Application Submission Flow
**Status:** Partially complete  
**Gaps:**
- Missing validation for required fields (reason, leave_date)
- No file attachment support yet
- No draft save functionality

**Tasks:**
- [ ] Add field validation to POST /api/applications
- [ ] Document required vs optional fields in v0.2 contract
- [ ] Add validation error samples to contract

**Priority:** P0 (blocks complete workflow)

### 2. Approval List/Detail Views
**Status:** Complete  
**Evidence:**
- GET /api/approvals/?decision=pending works
- GET /api/applications/{id} returns full detail with approvals

**Verification:**
- [x] Smoke test passed
- [x] Cross-counselor protection verified (403)

**Priority:** P0 (already done)

### 3. Approve/Reject Actions
**Status:** Complete  
**Evidence:**
- POST /api/approvals/{id}/approve works
- POST /api/approvals/{id}/reject works
- State machine transitions correctly

**Verification:**
- [x] Smoke test passed (full workflow)
- [x] Negative test passed (cross-counselor blocked)

**Priority:** P0 (already done)

### 4. State Machine Validation
**Status:** Needs hardening  
**Current:** Basic state transitions work  
**Gaps:**
- No explicit state machine diagram in docs
- No validation that prevents invalid state transitions
- No audit trail for state changes

**Tasks:**
- [ ] Document state machine transitions in v0.2 contract
- [ ] Add state transition validation in backend
- [ ] Add state change audit logging

**Priority:** P1 (works but needs documentation)

### 5. Negative Permission Tests
**Status:** Partially complete  
**Current tests:**
- [x] Cross-counselor approve blocked (403)
- [x] Student cannot access other student's applications

**Missing tests:**
- [ ] Student cannot approve applications
- [ ] Counselor cannot approve dean-level approvals
- [ ] Dean cannot modify applications after approval

**Tasks:**
- [ ] Add negative permission test cases
- [ ] Document permission matrix in v0.2 contract

**Priority:** P1 (core protection exists, need comprehensive coverage)

---

## P0: v0.2 Contract Convergence

### 1. Request/Response Samples
**Status:** Incomplete  
**Current:** contract-v0.1.md has basic samples  
**Gaps:**
- No samples for error responses
- No samples for edge cases (empty lists, pagination)
- No samples for all decision filter values

**Tasks:**
- [ ] Create comprehensive API sample collection
- [ ] Add error response samples (400, 403, 404, 409, 500, 503)
- [ ] Add pagination samples
- [ ] Add filter samples (decision=pending/approved/rejected/all)

**Priority:** P0 (needed for frontend/miniprogram development)

### 2. Status Enums
**Status:** Defined but not documented  
**Current:** ApplicationStatus and ApprovalDecision exist in code  
**Gaps:**
- Not documented in contract
- No state transition rules documented
- No invalid state handling documented

**Tasks:**
- [ ] Document all status enums in v0.2 contract
- [ ] Document valid state transitions
- [ ] Document error handling for invalid states

**Priority:** P0 (critical for contract stability)

### 3. Error Codes
**Status:** Partially defined  
**Current:** contract-v0.1.md defines 8 error codes  
**Gaps:**
- Not all error codes have samples
- No error code usage guidelines
- No client-side error handling recommendations

**Tasks:**
- [ ] Ensure all 8 error codes have samples
- [ ] Document when to use each error code
- [ ] Add client-side error handling guide

**Priority:** P0 (needed for robust error handling)

### 4. Mock Provider Boundaries
**Status:** Defined but not tested  
**Current:** MockDormCheckoutProvider exists  
**Gaps:**
- No documentation of mock vs real provider interface
- No test coverage for provider switching
- No fallback/degradation strategy documented

**Tasks:**
- [ ] Document DormCheckoutProvider interface
- [ ] Add tests for mock provider
- [ ] Document fallback strategy when real provider unavailable

**Priority:** P1 (mock works, need interface stability)

---

## P1: API Sample Alignment

### 1. Mock Fixtures vs TypeScript Types
**Status:** Needs verification  
**Tasks:**
- [ ] Compare frontend/services/mock.ts with frontend/types/api.ts
- [ ] Compare miniprogram mock data with types/api.ts
- [ ] Fix any field name mismatches
- [ ] Fix any type mismatches

**Priority:** P1 (reduces integration friction)

### 2. Backend Samples vs Frontend Expectations
**Status:** Needs verification  
**Tasks:**
- [ ] Run backend API and capture real responses
- [ ] Compare with frontend type definitions
- [ ] Document any differences
- [ ] Fix critical mismatches

**Priority:** P1 (prevents runtime errors)

---

## P2: DevTools Verification (External Blocker)

**Status:** Blocked by WeChat DevTools availability  
**Tasks:**
- [ ] Import miniprogram project into DevTools
- [ ] Verify compilation succeeds
- [ ] Test mock mode (login → list → detail)
- [ ] Test real API mode (connect to localhost:8001)
- [ ] Fix any issues found
- [ ] Document verification results

**Priority:** P2 (blocked externally, not on critical path)

**Blocker:** WeChat DevTools not available in current environment

---

## Execution Order

### Phase 1: Contract Stabilization (2-3 hours)
1. Document status enums and state transitions
2. Create comprehensive error code samples
3. Document request/response samples for all endpoints
4. Document permission matrix

**Output:** v0.2 contract document

### Phase 2: Workflow Hardening (2-3 hours)
1. Add field validation to application submission
2. Add state transition validation
3. Add comprehensive negative permission tests
4. Document mock provider interface

**Output:** Hardened backend + test coverage

### Phase 3: Alignment Verification (1-2 hours)
1. Verify mock fixtures match types
2. Verify backend responses match frontend expectations
3. Fix critical mismatches
4. Document known differences

**Output:** Alignment report + fixes

### Phase 4: DevTools Verification (When Available)
1. Import and compile miniprogram
2. Test mock mode
3. Test real API mode
4. Fix issues
5. Unfreeze miniprogram development

**Output:** Verified miniprogram + issue fixes

---

## Success Criteria

**Week 3 Complete When:**
- [ ] v0.2 contract document exists and is comprehensive
- [ ] All P0 workflow gaps are closed
- [ ] Negative permission test coverage is comprehensive
- [ ] Mock fixtures align with types
- [ ] Backend responses align with frontend expectations
- [ ] State machine is documented and validated
- [ ] Error handling is robust and documented

**Miniprogram Unfreeze When:**
- [ ] WeChat DevTools verification passes
- [ ] Mock mode works
- [ ] Real API mode works
- [ ] No critical issues found

---

## References

- Codex Path 5 analysis: `.omc/collaboration/artifacts/20260530-1942-codex-completion-boundary-analysis.md`
- Week 3 consensus: `docs/discussions/week3-direction-2026-05-30/06-consensus.md`
- Phase A completion: `.omc/artifacts/phase-a-completion-notes.md`
- Current contract: `docs/discussions/codex-review-2026-05-30/contract-v0.1.md`
