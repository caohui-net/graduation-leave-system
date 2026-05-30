# Week 4 Execution Plan - Final Consensus

**Date:** 2026-05-31  
**Status:** Consensus reached (Claude + Codex)  
**Approach:** Validation-first (Option E')

---

## Consensus Summary

**Core Agreement:**
1. ✅ Validation-first over build-first
2. ✅ MVP = minimal happy path + essential error handling (not full coverage)
3. ✅ React Native deferred for next phase (requires stakeholder confirmation)
4. ✅ Real dorm provider discovery starts immediately

**Key Revisions from Initial Proposals:**
- Codex's B-first revised to validation-first
- Vertical slice narrowed from 9 pages to 4 pages
- Attachments moved after validation (not before)
- DevTools validation becomes Phase 4A (blocking gate)

---

## Execution Plan

### Phase 4A: DevTools Validation (1-3 days)

**Goal:** Validate miniprogram skeleton in real WeChat environment

**Tasks:**
1. Install/configure WeChat DevTools
2. Import existing miniprogram project
3. Verify compile/page load
4. Verify login/token handling
5. Verify API calls using wx.request
6. Verify error handling (401/403/409)
7. Record defects and screenshots/logs

**Gate Decision:**
- ✅ Validation passes → Proceed to Phase 4B
- ⚠️ Small fixes needed → Fix and proceed
- ❌ Contract/backend issues → Patch backend first
- 🚫 DevTools unavailable after 3 days → Low-rework prep only

**Blocker:** External dependency (WeChat DevTools installation)

### Phase 4B: Narrow Miniprogram MVP (3-5 days)

**Scope:** 4 pages only

**Pages:**
1. `login` - Demo login for all roles, token persistence, 401 logout
2. `student-application` - Create/submit application, view status
3. `approvals` - Shared role-filtered list (counselor + dean)
4. `detail` - Shared detail page, approve/reject actions

**Core Features:**
- Login
- Student submit
- List own/assigned applications
- View detail
- Counselor approve/reject
- Dean approve/reject
- Status display

**Required States:**
- Loading (network calls)
- Empty list
- Form validation errors
- Auth/forbidden error
- Conflict error (approve/reject)
- Generic retryable failure

**Out of Scope:**
- Separate counselor/dean page sets
- Drafts
- Full attachment UX
- Advanced filtering/search
- Notification center
- Audit timeline UI
- React Native

**Acceptance Criteria:**
- Student can submit
- Counselor can approve/reject assigned application
- Dean can approve/reject escalated application
- Forbidden/conflict responses visible
- Backend tests still pass
- DevTools evidence exists

**Estimated:** 3-5 days after Phase 4A

### Phase 4C: Attachments MVP (2-4 days)

**Scope:** Local file upload/download only

**Features:**
- File upload (local storage backend)
- File list
- File download
- File size/type validation
- Role-based access tests

**Out of Scope:**
- Object storage (S3/OSS)
- CDN
- Antivirus scanning
- File preview
- Retention policies
- Chunked upload

**Estimated:** 2-4 days after Phase 4B

### Parallel Track: Dorm Provider Discovery

**Goal:** Remove external dependency blocker

**Tasks:**
1. Identify owner/contact
2. Confirm integration method (API vs database vs file)
3. Obtain schema/documentation
4. Obtain credentials or sandbox
5. Obtain test student IDs and expected states
6. Document network/access constraints

**Output:** Provider integration brief with:
- Access status
- API shape
- Test data
- Blockers
- Integration timeline

**Timeline:** Start immediately, complete before production pilot

---

## Timeline Summary

**Optimistic Path (DevTools available):**
- Phase 4A: 1-3 days
- Phase 4B: 3-5 days
- Phase 4C: 2-4 days
- **Total:** 6-12 days

**Pessimistic Path (DevTools blocked):**
- Phase 4A: 3 days attempt + blocker
- Low-rework prep: acceptance checklist, mock alignment, adapter tests
- Phase 4B/4C: Blocked until DevTools available

**Parallel Track:**
- Dorm provider discovery: Ongoing, non-blocking

---

## Risk Mitigation

**Risk 1: DevTools Unavailable**
- Mitigation: 3-day bounded attempt, then low-rework prep only
- Fallback: Document blocker, continue discovery work

**Risk 2: API Issues Found in Validation**
- Mitigation: Fix backend/contract before expanding UI
- Fallback: Patch and re-validate

**Risk 3: Scope Creep**
- Mitigation: Strict 4-page MVP, defer everything else
- Fallback: Review scope with stakeholder

**Risk 4: Dorm Provider Unavailable**
- Mitigation: Start discovery immediately
- Fallback: Manual fallback with stakeholder approval

---

## Success Criteria

**Phase 4A Success:**
- Miniprogram compiles in DevTools
- Login works
- At least 1 API call succeeds
- Errors display correctly

**Phase 4B Success:**
- All 3 roles can complete workflow
- Backend tests pass
- DevTools evidence captured

**Phase 4C Success:**
- File upload/download works
- Access control enforced
- Backend tests pass

**Overall Success:**
- End-to-end workflow validated
- User can complete application process
- Ready for stakeholder demo

---

## Next Actions

**Immediate (Can Start Now):**
1. ✅ Document consensus (this file)
2. 🔄 Start dorm provider discovery
3. 📋 Create Phase 4A validation checklist

**Blocked (Requires External Action):**
1. 🚫 Install WeChat DevTools (user/environment setup)
2. 🚫 Phase 4A validation (requires DevTools)
3. 🚫 Phase 4B/4C (requires Phase 4A completion)

---

**Status:** Consensus documented, ready to execute
**Blocker:** WeChat DevTools installation (external dependency)
**Parallel Work:** Dorm provider discovery (can start immediately)
