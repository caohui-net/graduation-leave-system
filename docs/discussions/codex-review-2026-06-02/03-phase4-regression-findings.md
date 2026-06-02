# Phase 4 Regression Test Findings

**Date:** 2026-06-02  
**Test Run:** 119 tests, 26 errors  
**Context:** Phase 4 regression testing after Step 4B Phase 3 (dorm_manager integration)

---

## Summary

Phase 4 regression tests revealed **breaking changes** from adding dorm_manager step to approval workflow. The 3-step workflow (counselor → dean) was expanded to 4-step (counselor → dorm_manager → dean), but enum definitions and approval creation logic were not updated consistently.

---

## Error Categories

### Error 1: IntegrityError - approver_name NULL (Multiple occurrences)

**Example:**
```
django.db.utils.IntegrityError: null value in column "approver_name" of relation "approvals" violates not-null constraint
DETAIL:  Failing row contains (apv_09824ea3, dorm_manager, null, pending, null, null, ...)
```

**Location:** `apps/applications/views.py:165` - `create_application()`

**Cause:**
When creating dorm_manager approval, code doesn't set `approver_name` field:
```python
dorm_manager_approval = Approval.objects.create(
    step=ApprovalStep.DORM_MANAGER,
    approver=class_mapping.dorm_manager,
    # approver_name=??? <- MISSING
    ...
)
```

**Impact:** All application creation tests fail when trying to create dorm_manager approval.

---

### Error 2: AttributeError - Missing Enum Values

**Example 1:**
```python
self.application.status = ApplicationStatus.PENDING_DEAN
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: PENDING_DEAN
```

**Example 2:**
```python
step=ApprovalStep.DEAN
     ^^^^^^^^^^^^^^^^^
AttributeError: DEAN
```

**Cause:**
- `ApplicationStatus` enum missing `PENDING_DEAN` value
- `ApprovalStep` enum missing `DEAN` value
- Tests assume 3-step workflow (counselor → dean) but code now has 4-step workflow

**Impact:** State machine tests fail when checking workflow transitions.

---

## Root Cause Analysis

**Original workflow (3-step):**
```
Student → Counselor → Dean
```

**New workflow (4-step):**
```
Student → Counselor → Dorm Manager → Dean
```

**What was updated:**
1. ✓ Added `dorm_manager` fields to ClassMapping model
2. ✓ Created migrations (0003, 0004)
3. ✓ Added `DORM_MANAGER` to `ApprovalStep` enum
4. ✓ Updated application creation logic to create dorm_manager approval

**What was NOT updated:**
1. ✗ `approver_name` not set when creating dorm_manager approvals
2. ✗ `ApplicationStatus` enum still has `PENDING_DEAN` instead of `PENDING_DORM_MANAGER` + `PENDING_DEAN`
3. ✗ State machine logic not updated for 4-step workflow
4. ✗ Tests still assume 3-step workflow

---

## Questions for Codex

1. **Workflow design:**
   - Should we keep 3-step workflow (counselor → dean) and make dorm_manager optional?
   - Or fully implement 4-step workflow (counselor → dorm_manager → dean)?
   - What are the implications for existing data and tests?

2. **Enum consistency:**
   - Should `ApplicationStatus` have `PENDING_DORM_MANAGER` state?
   - Should we keep `PENDING_DEAN` or is it redundant with `PENDING_DORM_MANAGER`?
   - How should `ApprovalStep.DEAN` be handled if dorm_manager comes before dean?

3. **approver_name field:**
   - Should we always set `approver_name` when creating approvals?
   - Should we derive it from `approver.name` or from `ClassMapping.dorm_manager_name`?
   - What's the source of truth for approver names?

4. **Migration strategy:**
   - Do we need a data migration to update existing Application statuses?
   - Should we add `PENDING_DORM_MANAGER` to ApplicationStatus enum?
   - How to handle tests that assume 3-step workflow?

---

## Test Failure Summary

**Total:** 119 tests  
**Errors:** 26  
**Pass rate:** ~78% (93 passed, 26 errors)

**Failed test categories:**
- Application creation tests (IntegrityError on dorm_manager approval)
- State machine tests (Missing enum values)
- Workflow transition tests (Inconsistent status checks)

---

## Next Steps

1. Consult Codex on workflow design decisions
2. Update enums based on agreed workflow
3. Fix approver_name assignment in approval creation
4. Update tests to match new workflow
5. Re-run Phase 4 regression tests
6. Verify all 119 tests pass
