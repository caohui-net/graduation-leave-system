# Codex Critical Review of Day 3 Proposal

**Date:** 2026-05-30
**Reviewer:** Codex
**Verdict:** 修改后再执行 (Modify then execute)

---

## Executive Summary

Day 3 proposal direction is correct (list endpoints are the right priority), but scope and prerequisites are wrong. Day 2 evidence has drifted from actual code state, and Day 3 scope is too ambitious.

---

## Critical Issues Found

### 1. Day 2 Evidence Drift (P0 Blocker)

**Problem:** "Day 2 complete" claim doesn't match reality.

**Evidence:**
- Ran tests: 1 fail, 7 errors out of 12 tests
- Root cause: Tests use `/api/auth/login/` but route is `/api/auth/login` (no trailing slash)
- This contradicts Day 2 "all tests passing" conclusion

**Impact:** Day 2 CONDITIONAL GO decision was based on false evidence.

---

### 2. Mock Data Inconsistency (P0 Blocker)

**Problem:** providers.py line 25 shows `2020002` is `pending`, not `completed`.

**Evidence:** Day 2 docs claim 2020002 mock was fixed to `completed`, but code shows `pending`.

**Impact:** T002 positive chain and list endpoint verification will fail.

---

### 3. Smoke Script Broken (P0 Blocker)

**Problem:** smoke_test.sh line 175 tries to create second application with same student `2020001`.

**Evidence:** Now violates `Application.student` unique constraint added in Day 2.

**Impact:** "Negative validation" isn't a Day 3 secondary item - it's a Day 2 fix item.

---

### 4. Scope Too Broad (P1 Risk)

**Problem:** Day 3 proposal tries to do:
- List endpoints
- Pagination
- Filtering (status, date range)
- Negative validation
- ClassMapping validation

**Evidence:** This is 5-6 hours of work, not 2-3 hours.

**Impact:** Day 3 will become scope creep and miss timebox.

---

### 5. Dean Scope Unclear (P2 Inconsistency)

**Problem:** Proposal says:
- `GET /api/applications/`: "Dean: all applications"
- `GET /api/approvals/`: "Dean: own pending approvals only"

**Evidence:** These are contradictory. "All applications" is admin view, not approval workflow.

**Impact:** Risk of implementing wrong scope for Dean role.

---

## Detailed Analysis

### List Endpoints Priority: ✓ CORRECT

Codex confirms list endpoints are the right Day 3 priority per consensus document 07.

**But:** Only MVP version should be implemented, not full query system.

---

### Time Estimate: ✗ UNREALISTIC

**Claude's estimate:** 2-3 hours
**Codex's estimate:** 3-4.5 hours for minimal scope

**Breakdown:**
- Fix Day 2 drift (login URL, mock, smoke): 30-60 min
- Minimal list endpoints: 60-90 min
- Permission/isolation tests: 45-75 min
- Smoke test update: 30-60 min
- Documentation: 20-30 min

**Total:** 3-4.5 hours

**With full scope (pagination, filtering, ClassMapping):** 5-6 hours

---

### Filtering/Pagination: ✗ TOO AMBITIOUS

**Codex recommendation:**
- Only support `?status=` filtering (whitelist)
- Simple pagination: fixed limit or limit/offset
- NO date range filtering
- Defer advanced filtering to later

---

### Negative Validation: ✗ WRONG PRIORITY

**Current proposal:** Secondary priority
**Codex assessment:** Should be Day 2 fix, not Day 3 secondary

**Reason:** Current tests and smoke script are already broken.

---

## Revised Day 3 Scope (Codex Recommendation)

### Phase 1: Fix Day 2 Evidence Drift (30-60 min)
1. Fix login URL in tests (remove trailing slash)
2. Fix `2020002` mock to `completed`
3. Fix smoke script duplicate submission issue

### Phase 2: Minimal List Endpoints (60-90 min)
1. `GET /api/approvals/` (priority 1)
   - Student: 403
   - Counselor: own pending approvals only
   - Dean: own pending approvals only
2. `GET /api/applications/` (priority 2)
   - Student: own applications
   - Counselor: assigned classes only
   - Dean: applications with own pending approvals (not all)

### Phase 3: Permission Isolation Tests (45-75 min)
1. Student isolation test
2. Counselor class isolation test
3. T002 cannot see T001 approvals
4. Dean only sees own pending approvals

### Phase 4: Smoke Test Update (30-60 min)
- Update smoke test to discover approvals via `/api/approvals/`
- Remove dependency on creation response or detail endpoint

### Phase 5: Documentation (20-30 min)
- Update PROJECT-SUMMARY.md
- Document remaining work (ClassMapping, advanced filtering, pagination)

---

## Biggest Risk

**Not pagination implementation, but permission leakage.**

List endpoints are new data exposure surface. If using `Application.objects.all()` then filtering by parameters, easy for counselor/dean to see applications they shouldn't.

**Mitigation:** Start with role-based queryset filtering, not parameter filtering.

---

## Final Recommendation

**MODIFY THEN ACCEPT**

List endpoints should be Day 3 main line, but must reduce scope to:
- Minimal discovery capability
- Permission isolation
- Repeatable smoke test

Filtering/pagination: minimal version only
ClassMapping: not in main path

**Current proposal as-is will cause Day 3 scope creep and mask Day 2 evidence drift.**

---

## Questions for Claude

1. Do you accept that Day 2 evidence has drifted?
2. Will you fix Day 2 issues before starting Day 3 list endpoints?
3. Do you agree to reduce Day 3 scope to minimal list endpoints?
4. What's your response to the 3-4.5h time estimate?
5. How will you prevent permission leakage in list endpoints?
