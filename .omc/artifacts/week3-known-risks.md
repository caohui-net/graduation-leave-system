# Week 3 Known Risks & Blockers

**Date:** 2026-05-31  
**Status:** Phase 1 Complete, Closure Gate In Progress

---

## P0 Risks (Block Frontend Start)

### 1. Business Semantics Not Frozen

**Issue:** Application.student unique constraint prevents resubmission after rejection.

**Impact:** If students need to resubmit after rejection, current model/API will fail.

**Decision Needed:** 
- Allow resubmission? → Remove unique constraint, add status-based logic
- One-shot only? → Document clearly in contract

---

### 2. Approved History Viewing Undefined

**Issue:** Current list endpoints only show pending approvals. No way to view completed approvals.

**Impact:** Counselors/deans cannot see their approval history.

**Decision Needed:**
- Add `?decision=approved` filter to `/api/approvals/`?
- Separate `/api/approvals/history/` endpoint?
- Include in application detail only?

---

## P1 Risks (Impact Stability)

### 3. CSV Import Not Production-Ready

**Current State:** Basic import works, but lacks:
- Transaction protection (partial import on error)
- Validation reports (which rows failed)
- Batch tracking (import history)
- Soft-disable strategy (missing users)
- UTF-8 BOM handling
- Duplicate/conflict resolution

**Impact:** Data import failures will be hard to diagnose and recover.

---

### 4. Mini-Program Integration Details Missing

**Undefined:**
- Base URL configuration (dev vs prod)
- JWT storage strategy (wx.storage)
- Error code display mapping
- Pagination response format confirmation
- Dev tools domain whitelist settings
- HTTPS/filing timeline

**Impact:** Frontend may make wrong assumptions, causing rework.

---

## P2 Risks (Known Issues)

### 5. Django Test Discovery Broken

**Issue:** `python manage.py test` finds 0 tests. pytest not installed.

**Workaround:** Smoke test script works. Manual verification possible.

**Impact:** No automated regression testing during development.

---

## P3 Risks (Frontend-Specific)

### 6. WeChat OAuth Not in v0.1

**Issue:** First narrow slice uses account/password login only. WeChat OAuth deferred.

**Impact:** Cannot test real WeChat user flow. 主体备案 and openid binding timeline unclear.

**Mitigation:** Document as known limitation. Plan OAuth integration for Phase 2.

---

### 7. HTTPS Domain Required for Real Device

**Issue:** Real device testing requires HTTPS domain. Dev tools OK with localhost.

**Impact:** Cannot test on real devices until domain + SSL configured.

**Mitigation:** Use dev tools for v0.1. Prepare 内网穿透 or test domain for Phase 2.

---

### 8. API Trailing Slash Handling

**Issue:** Django REST Framework requires trailing slash. Mini-program may omit it.

**Impact:** 404 errors if API client doesn't add trailing slash consistently.

**Mitigation:** API client must normalize URLs. Document in integration guide.

---

### 9. 403 Error Display Strategy

**Issue:** No UX design for permission denied scenarios.

**Impact:** Users may see raw error messages or unclear feedback.

**Mitigation:** Define error message mapping in acceptance checklist.

---

## Mitigation Status

- ✓ Smoke test passing (happy path + negative test)
- ✓ API samples collected
- ✓ v0.2 contract snapshot complete
- ✓ CSV import verification complete
- ✓ Frontend acceptance checklist created
- ✓ Frontend risks documented
- ⏳ Business semantics decisions (need user input)
- ⏳ Mini-program skeleton (next)

---

**Next Actions:**
1. Get user decisions on P0 business semantics (resubmission, approved history)
2. Start mini-program skeleton setup
3. Implement API client + auth store
4. Build login → approvals → detail → approve flow
