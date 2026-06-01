# Test Coverage Enhancement - Final Consensus

**Created:** 2026-06-01T04:08Z  
**Participants:** Claude, Codex  
**Status:** APPROVED - Ready for execution

---

## Consensus Summary

**Decision:** Proceed with narrowed test scope focusing on gap-filling rather than comprehensive matrix creation.

**Key agreements:**
1. ✅ State machine testing = sequential API/validator logic (NOT real concurrency)
2. ✅ Detail endpoint isolation is the real gap (list permissions already tested)
3. ✅ Dean permission model: only sees applications with own pending dean approval
4. ✅ Extend existing test files rather than create large new test suites
5. ✅ Timezone testing: 2 mocked boundary cases merged into existing file

**Time estimate:** 0.6 days (target), 0.7 days (buffer)

---

## Executable Test Plan

### 1. Detail Endpoint Isolation (NEW FILE)

**File:** `backend/apps/applications/tests/test_detail_permissions.py`

**Tests (3):**

1. `test_student_cannot_access_other_student_application`
   - Student A creates application
   - Student B tries GET /api/applications/{A's app_id}
   - Expected: 403 FORBIDDEN

2. `test_counselor_cannot_access_cross_class_application`
   - Student from CS2020-01 creates application
   - Counselor T002 (assigned to CS2020-02) tries GET /api/applications/{app_id}
   - Expected: 403 FORBIDDEN

3. `test_dean_cannot_access_non_assigned_application`
   - Student creates application, counselor approves (creates dean approval for D001)
   - Dean D002 tries GET /api/applications/{app_id}
   - Expected: 403 FORBIDDEN
   - Note: Dean detail semantics = only sees applications with own pending dean approval

**Estimated time:** 2 hours

---

### 2. Approval List Leak Test (EXTEND EXISTING)

**File:** `backend/apps/approvals/tests/test_list_permissions.py`

**Test (1):**

4. `test_decision_all_does_not_leak_cross_approver_data`
   - Counselor T001 has 2 approvals (1 pending, 1 approved)
   - Counselor T002 has 1 approval (pending)
   - T001 calls GET /api/approvals/?decision=all
   - Expected: Returns only T001's 2 approvals, not T002's

**Estimated time:** 30 minutes

---

### 3. State Machine Gap Filling (EXTEND EXISTING)

**Files:** Extend existing `test_state_machine.py` or `test_p0_fixes.py`

**Tests (1-2):**

5. `test_resubmission_after_rejection` (if not already covered in test_p0_fixes.py)
   - Application rejected
   - Student creates new application
   - Expected: New application in pending_counselor state

6. `test_cannot_reverse_terminal_state_with_opposite_decision` (optional, if not covered)
   - Application approved
   - Try to reject → 409 CONFLICT
   - Application rejected
   - Try to approve → 409 CONFLICT

**Note:** Check existing tests first. test_p0_fixes.py already has resubmission test. test_state_machine.py already has duplicate operation tests. Only add if gaps exist.

**Estimated time:** 1 hour (or 0 if already covered)

---

### 4. Timezone Boundary Tests (EXTEND EXISTING)

**File:** `backend/apps/applications/tests/test_serializer_validation.py`

**Tests (2):**

7. `test_leave_date_validation_at_midnight_boundary`
   - Mock timezone.now() to 2026-06-01 23:59:59 Asia/Shanghai
   - Submit with leave_date="2026-06-02"
   - Expected: Pass (tomorrow is valid)

8. `test_leave_date_validation_after_midnight`
   - Mock timezone.now() to 2026-06-02 00:00:01 Asia/Shanghai
   - Submit with leave_date="2026-06-01"
   - Expected: 400 VALIDATION_ERROR (past date)

**Estimated time:** 30 minutes

---

## Total Estimated Time

**Core tests:** 4 hours (0.5 days)  
**With state machine check:** 5 hours (0.6 days)  
**Buffer:** 5.5 hours (0.7 days)

---

## Implementation Order

1. **Phase 1:** Detail permissions (2 hours) - highest security value
2. **Phase 2:** Approval list leak (30 min) - security
3. **Phase 3:** Timezone boundaries (30 min) - edge case coverage
4. **Phase 4:** State machine gaps (1 hour or skip if covered) - data integrity

---

## Verification Criteria

After implementation:
- [ ] All new tests pass
- [ ] Existing tests still pass (no regression)
- [ ] Test coverage report shows increased coverage
- [ ] Commit and push changes
- [ ] Update PROJECT-SUMMARY.md
- [ ] Update session-context.json

---

## Scope Exclusions (Agreed)

**NOT included:**
- ❌ Real concurrency/threading tests
- ❌ Cross-timezone matrix
- ❌ Comprehensive state machine matrix from scratch
- ❌ Model-level illegal transition tests (draft → approved)
- ❌ List permission tests (already covered)

---

**Status:** Ready for immediate execution per user directive
