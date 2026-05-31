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
| API Client | Duplicated in each page | ⚠️ Risky | HTTP request wrapper with auth |
| Auth Service | Inline in pages | ⚠️ Risky | Token storage/retrieval |

**Current implementation:**
- Each page has its own `api` object with `baseUrl` and request methods
- No shared API client module
- Auth logic duplicated across pages

---

### Types

| Type | Path | Status | Purpose |
|------|------|--------|---------|
| User | Inline in pages | ⚠️ Risky | User model (id, name, role) |
| Approval | Inline in pages | ⚠️ Risky | Approval model |
| Application | Not defined | ❌ Missing | Student application model |

**Current implementation:**
- Types defined inline in page `.ts` files
- No shared type definitions
- Risk of type inconsistency across pages

---

## Missing Pieces

### 1. Student Application Page

**Status:** ❌ Not implemented

**Required components:**
- Page files: `student-application.wxml`, `student-application.wxss`, `student-application.ts`, `student-application.json`
- Form fields: reason, start_date, end_date, destination
- Submit button with API call to `POST /api/applications/`
- Success/error handling
- Navigation back to home or status page

**Blocked by:** DevTools validation of form behavior and API integration

---

### 2. Shared API Client

**Status:** ❌ Not implemented

**Current state:**
- API client code duplicated in:
  - `pages/login/login.ts`
  - `pages/approvals/approvals.ts`
  - `pages/detail/detail.ts`

**Required:**
- Shared module: `services/api.ts` or `utils/request.ts`
- Centralized baseUrl configuration
- Centralized auth header injection
- Centralized error handling (401 → logout, 403/409 → display)
- Export reusable request methods

**Blocked by:** DevTools validation of `baseUrl` behavior (does `http://localhost:8001` work?)

---

### 3. Shared Type Definitions

**Status:** ❌ Not implemented

**Required:**
- `types/user.ts`: User interface
- `types/approval.ts`: Approval interface
- `types/application.ts`: Application interface
- `types/api.ts`: API response interfaces

**Blocked by:** None (can implement anytime, but low priority until pages stabilize)

---

## Risky Areas

### 1. Hardcoded Base URL

**Location:** Each page file

**Current implementation:**
```typescript
const baseUrl = 'http://localhost:8001';
```

**Risk:**
- Duplicated across 3+ files
- Needs manual update for production deployment
- May not work in DevTools (network policy unknown)

**Validation needed:**
- Does `http://localhost:8001` work in DevTools simulator?
- Does it work on real device preview?
- What base URL is needed for production?

**Blocked by:** DevTools validation

---

### 2. Duplicated Auth Logic

**Location:** Each page file

**Current implementation:**
```typescript
// Login page
wx.setStorageSync('token', response.data.token);
wx.setStorageSync('user', response.data.user);

// Other pages
const token = wx.getStorageSync('token');
headers['Authorization'] = `Bearer ${token}`;
```

**Risk:**
- Auth logic duplicated across pages
- Inconsistent error handling
- Hard to maintain (change in one place requires updating all pages)

**Recommendation:**
- Extract to shared auth service after DevTools validation
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
| Shared type definitions | No runtime dependency | Low |
| Documentation | No code changes | None |
| Test data preparation | No code changes | None |

**Action:** Can implement during blocked time, but low priority

---

## Implementation Priority (Phase 4B)

**After DevTools validation passes:**

1. **High Priority:**
   - Implement student-application page
   - Extract shared API client
   - Fix hardcoded baseUrl (use config or environment)

2. **Medium Priority:**
   - Extract shared type definitions
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
