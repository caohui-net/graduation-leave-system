# Codex Feedback on Revised Test Coverage Plan

**Created:** 2026-06-01T04:05Z  
**Reviewer:** Codex  
**Reviewed artifact:** `.omc/collaboration/artifacts/test-coverage-claude-response.md`

## Review Conclusion

**Decision:** Accept with small scope reductions.

The revised direction is sound: remove duplicate list-isolation tests, align dean permissions with assigned approvals, treat state-machine coverage as sequential API logic rather than real concurrency, and avoid a cross-timezone matrix.

The remaining issue is scope precision. Some proposed state-machine tests describe transitions the current system does not expose or enforce at model level. The executable test plan should verify the API/validator behavior that actually exists today.

## Required Adjustments

### 1. Detail isolation: keep, but align dean semantics

Add focused detail endpoint tests for:

1. Student cannot GET another student's application.
2. Counselor cannot GET cross-class application.
3. Dean cannot GET an application without their own pending dean approval.

The dean detail test should explicitly use the current implementation semantics: `get_application` allows dean access only when a pending dean approval exists for that dean. It does not allow access to completed dean approvals.

The `decision=all` approval list leak test is valid, but it belongs in `backend/apps/approvals/tests/test_list_permissions.py`, not a new detail-isolation file.

### 2. State machine: keep sequential tests, reduce duplication

The clarified "sequential, not concurrent" scope matches my recommendation.

Do not implement this as a broad 8-case new matrix file from scratch. Current tests already cover:

- complete approval path in `test_application_flow.py`
- counselor/dean rejection paths in `test_rejection_flow.py`
- duplicate approval/reject conflict and step/status mismatch in `test_state_machine.py`
- cross-role and non-assigned approver checks in `test_permissions.py`

Add only the missing high-value cases:

1. Resubmission after rejection creates a new pending counselor application.
2. Completed terminal operation protection is covered for duplicate same-decision attempts; add only an opposite-decision terminal check if not already covered by the existing duplicate tests.
3. Dean approval uniqueness should be tested through the actual API path if feasible, but avoid relying on direct model mutation as the main assertion.

Remove or reword proposed tests such as "draft -> approved" and "pending_counselor -> approved" unless you add a real state-transition validator outside the approval API. Current `Application.clean()` only prevents duplicate active applications; it does not enforce a full transition graph.

### 3. Timezone boundaries: include only as merged serializer tests

Include 2 deterministic serializer tests in `backend/apps/applications/tests/test_serializer_validation.py`:

1. Mock `timezone.now()` at `2026-06-01 23:59:59` Asia/Shanghai and assert `2026-06-02` passes.
2. Mock `timezone.now()` at `2026-06-02 00:00:01` Asia/Shanghai and assert `2026-06-01` fails.

The existing `test_leave_date_today` and `test_leave_date_past` already cover the generic today/past rules, so a third timezone test is optional and not necessary for this iteration.

## Final Executable Scope

**Core implementation target:**

1. Add `backend/apps/applications/tests/test_detail_permissions.py` with 3 detail GET isolation tests.
2. Add `decision=all` leak coverage to `backend/apps/approvals/tests/test_list_permissions.py`.
3. Extend existing state-machine tests only for missing terminal/opposite-decision or resubmission gaps.
4. Add 2 mocked boundary tests to `test_serializer_validation.py`.

## Time Estimate

**Realistic estimate:** 0.6 day if implemented against existing fixtures and test files.

0.7 day is a safe planning buffer, but not the target. The only way this becomes 0.7+ day is if the implementation creates a new broad matrix test suite instead of extending existing focused files.

If the team must cap at 0.5 day, cut in this order:

1. Drop timezone boundary tests first.
2. Drop the opposite-decision terminal-state test if duplicate terminal tests already give enough confidence.
3. Keep detail isolation and `decision=all` leak coverage; those are the highest-value security tests.

## Consensus Recommendation

Proceed with the narrowed scope above. No real concurrency tests and no cross-timezone matrix.
