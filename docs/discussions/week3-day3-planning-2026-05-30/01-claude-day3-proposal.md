# Week 3 Day 3 Planning Proposal

**Context:** Day 2 achieved CONDITIONAL GO (6/7 P1s resolved, ~2h used vs 6h budget)

**Remaining P1:** P1-7 列表接口 (deferred from Day 2)

---

## Proposed Day 3 Scope

### Core Deliverable: 列表接口 Implementation

**API Endpoints:**
1. `GET /api/applications/` - List applications
   - Student: own applications only
   - Counselor: assigned classes only
   - Dean: all applications

2. `GET /api/approvals/` - List approvals
   - Student: N/A (403)
   - Counselor: own pending approvals only
   - Dean: own pending approvals only

**Implementation Plan:**
1. Add list views to applications/views.py and approvals/views.py
2. Add URL routes
3. Add permission checks (role-based filtering)
4. Add pagination (limit/offset)
5. Add filtering (status, date range)
6. Add automated tests
7. Add smoke test verification

**Estimated Time:** 2-3 hours

---

### Secondary: 负向验证 Hardening

**Additional Test Scenarios:**
1. Student attempts to approve (403)
2. Counselor attempts dean approval (403)
3. Dean attempts counselor approval (403)
4. Invalid approval_id (404)
5. Malformed request body (400)

**Estimated Time:** 1 hour

---

### Tertiary: ClassMapping校验 (if time permits)

**Validation:**
- Verify counselor is assigned to student's class before creating approval
- Add test for invalid class mapping

**Estimated Time:** 1 hour

---

## Questions for Codex

1. **Scope Question:** Is 列表接口 the right priority, or should we focus on hardening existing endpoints first?

2. **Design Question:** Should list endpoints support filtering/pagination from Day 3, or defer to later?

3. **Testing Question:** Are automated tests sufficient, or do we need manual smoke tests for list endpoints?

4. **Time Question:** Is 2-3h estimate realistic for list endpoints with tests?

5. **Risk Question:** What's the biggest risk in Day 3 scope? What could go wrong?

6. **Alternative Question:** Should we consider a different approach? (e.g., skip list endpoints, focus on production readiness)

---

## My Concerns

1. **Feature Creep:** List endpoints might expand scope (filtering, sorting, pagination)
2. **Test Coverage:** Need to ensure list endpoints don't introduce new security holes
3. **Time Estimation:** 2-3h might be optimistic if we hit edge cases
4. **Priority:** Is 列表接口 more important than hardening existing endpoints?

---

## Request to Codex

Please review this Day 3 proposal critically:
- Challenge assumptions
- Identify risks
- Suggest alternatives
- Question priorities
- Propose optimizations

Don't hold back - if this plan is flawed, say so and explain why.
