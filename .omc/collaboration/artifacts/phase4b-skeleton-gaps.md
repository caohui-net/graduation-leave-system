# Phase 4B Skeleton Gap Audit

**Purpose:** Document existing miniprogram structure, missing pieces, and risky areas  
**Target audience:** Phase 4B implementer  
**Status:** Pre-validation audit (before DevTools testing)

---

## Existing Structure

### Pages

| Page | Path | Status | Purpose |
|------|------|--------|---------|
| Login | `pages/login/login` | ✅ Exists | User authentication |
| Approvals | `pages/approvals/approvals` | ✅ Exists | List pending approvals (counselor/dean) |
| Detail | `pages/detail/detail` | ✅ Exists | View approval details |
| Student Application | `pages/student-application/student-application` | ❌ Missing | Student submits leave application |

**Registered in app.json:**
- `pages/login/login`
- `pages/approvals/approvals`
- `pages/detail/detail`

**Not registered:**
- `pages/student-application/student-application` (page doesn't exist yet)

---

### Services

| Service | Path | Status | Purpose |
|---------|------|--------|---------|
| API Client | `services/api.ts` | ✅ Exists (2.9K) | HTTP request wrapper with auth |
| Auth Service | Config duplicated in pages | ⚠️ Risky | Token storage/retrieval and 401 handling |

**Current implementation:**
- Shared API client exists at `services/api.ts`
- Pages import and use shared API client
- Token injection and 401 callback are configured through `ApiClient`
- Each page still instantiates `ApiClient` with duplicated `baseUrl`, `getToken`, and `onUnauthorized` config

---

### Types

| Type | Path | Status | Purpose |
|------|------|--------|---------|
| API Types | `types/api.ts` | ✅ Exists (2.0K) | Shared type definitions for API |
| User | `types/api.ts` | ✅ Exists | User model (`user_id`, `name`, `role`, `class_id`) |
| Approval | `types/api.ts` | ✅ Exists | Approval detail/list/action models |
| Application | `types/api.ts` | ✅ Exists | Application model and create request |

**Current implementation:**
- Shared type definitions exist at `types/api.ts`
- `User`, `Application`, `ApplicationDetail`, `ApprovalDetail`, `ApprovalListItem`, and action request/response types are defined there
- Current residual risk is not missing types; it is whether future Phase 4B page work continues to import these shared types instead of reintroducing inline shapes

---

## Missing Pieces

### 1. Student Application Page

**Status:** ❌ Not implemented

**Required components:**
- Page files: `student-application.wxml`, `student-application.wxss`, `student-application.ts`, `student-application.json`
- Form fields: reason, leave_date (按当前API契约v0.2)
- Submit button with API call to `POST /api/applications/`
- Success/error handling
- Navigation back to home or status page

**Implementation status:** Ready to implement (blocker removed)

---

### 2. Student Home Page

**Status:** ❌ Not implemented

**Issue:** Student login redirects to `/pages/approvals/approvals` but students receive 403 FORBIDDEN (students cannot access approval list).

**Required:**
- Dedicated student home page or application list page
- Update login redirect logic for student role
- Navigation to student-application page (submit new application)
- Navigation to student's own applications (view status)

**Blocked by:** DevTools validation of navigation and page structure

---

### 3. Shared API Client Centralization

**Status:** ⚠️ Partially verified

**Current state:**
- `services/api.ts` exists and is imported by login, approvals, and detail pages
- `baseUrl`, `getToken`, and `onUnauthorized` are still duplicated in each page's `new ApiClient(...)` config

**Action:** Centralize the default API client/config during Phase 4B if DevTools validation does not reveal a base URL requirement that changes the design.

---

### 4. Shared Type Definition Discipline

**Status:** ✅ Existing, enforce during Phase 4B

**Required:**
- Reuse `types/api.ts` for user, approval, application, pagination, and error types
- Avoid adding inline response types in new student pages unless the API contract introduces a genuinely new shape

**Blocked by:** None. This is an implementation discipline item for future page work.

---

## Risky Areas

### 1. Hardcoded Base URL (Runtime Behavior Needs Verification)

**Location:** Page-level `new ApiClient(...)` config in login, approvals, and detail pages

**Status:** `services/api.ts` exists and is used, but `http://localhost:8001` is duplicated in page configs

**Potential risk if not centralized:**
- Duplicated across multiple files
- Needs manual update for production deployment
- May not work in DevTools (network policy unknown)

**Validation needed during Phase 4A:**
- Test if `http://localhost:8001` works in DevTools simulator
- Test if it works on real device preview
- Determine what base URL is needed for production

**Blocked by:** DevTools validation

---

### 2. Duplicated Auth Config

**Location:** Page-level `new ApiClient(...)` config in login, approvals, and detail pages

**Status:** Token injection and 401 behavior are implemented through `ApiClient`, but each page repeats the same `getToken` and `onUnauthorized` callback

**Potential risk if not centralized:**
- Auth logic duplicated across pages
- Inconsistent error handling
- Hard to maintain (change in one place requires updating all pages)

**Validation needed during Phase 4A:**
- Verify token storage/retrieval is centralized
- Verify `wx.reLaunch` on 401 behaves correctly in DevTools

**Recommendation if duplicated:**
- Extract default API client/auth config after DevTools validation
- Centralize token management
- Centralize 401 handling

**Blocked by:** DevTools validation of storage and auth flow

---

### 3. Missing Page Registration

**Location:** `miniprogram/app.json`

**Current state:**
```json
{
  "pages": [
    "pages/login/login",
    "pages/approvals/approvals",
    "pages/detail/detail"
  ]
}
```

**Risk:**
- `student-application` page not registered
- Will cause navigation error if page is implemented but not registered

**Action:**
- Do NOT register until page is implemented
- Register during Phase 4B implementation

**Blocked by:** Page implementation

---

### 4. Error Handling Completeness

**Location:** All pages

**Current implementation:**
- 401 handling: ✅ Implemented (logout + redirect)
- 403 handling: ⚠️ Partial (displays error, but UX unclear)
- 409 handling: ⚠️ Partial (displays error, but UX unclear)
- Network failure: ⚠️ Unknown (needs DevTools testing)

**Validation needed:**
- Test 401/403/409 error display in DevTools
- Test network failure scenarios
- Verify error messages are user-friendly

**Blocked by:** DevTools validation

---

## Blocked Items

### Items Requiring DevTools Validation

| Item | Reason | Validation Needed |
|------|--------|-------------------|
| Base URL behavior | Unknown if `localhost:8001` works | Test API calls in simulator |
| Form input behavior | Unknown form validation UX | Test student-application form |
| Error display UX | Unknown how errors render | Test 401/403/409 scenarios |
| Navigation flow | Unknown if redirects work | Test login → approvals → detail |
| Storage API | Unknown if `wx.setStorageSync` works | Test token persistence |
| Network failure | Unknown retry/error UX | Test with backend stopped |

**Action:** Execute Phase 4A validation checklist before implementing fixes

---

### Items Safe to Implement Now

| Item | Reason | Risk |
|------|--------|------|
| Enforce shared type imports in new pages | Existing `types/api.ts` already covers current API shapes | Low |
| Centralized API client config | Pure refactor, but should preserve any DevTools-discovered base URL requirement | Low |
| Documentation | No code changes | None |
| Test data preparation | No code changes | None |

**Action:** Can implement during blocked time, but low priority

---

## Implementation Priority (Phase 4B)

**After DevTools validation passes:**

1. **High Priority:**
   - Implement student-application page
   - Centralize API client configuration
   - Fix hardcoded baseUrl (use config or environment)

2. **Medium Priority:**
   - Reuse shared type definitions in new pages
   - Improve error handling UX
   - Add loading states

3. **Low Priority:**
   - Add form validation
   - Add retry logic for network failures
   - Add offline support

---

## Validation Gates

**Before starting Phase 4B implementation:**
- [ ] Phase 4A validation checklist complete
- [ ] DevTools setup complete
- [ ] Base URL behavior validated
- [ ] Error handling UX validated
- [ ] Navigation flow validated

**If validation fails:**
- Document failures in Phase 4A evidence
- Adjust implementation plan based on findings
- Re-validate after fixes

---

**Status:** Ready for Phase 4B planning  
**Blocker:** Phase 4A validation must complete first  
**Estimated Phase 4B effort:** 4-6 hours (after validation)
