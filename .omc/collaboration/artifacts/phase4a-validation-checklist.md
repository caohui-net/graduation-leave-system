# Phase 4A Validation Checklist

**Purpose:** Validate miniprogram skeleton in WeChat DevTools  
**Estimated time:** 1-3 days (external dependency)  
**Blocker:** WeChat DevTools installation

---

## Prerequisites

- [ ] WeChat DevTools installed and configured
- [ ] Project imported successfully
- [ ] Backend running at `http://localhost:8001`
- [ ] Test accounts available (student, counselor, dean)

---

## Test Accounts

| Role | User ID | Password | Class ID |
|------|---------|----------|----------|
| Student | 2020006 | 2020006 | CS2020-02 |
| Counselor | T001 | T001 | CS2020-01 |
| Counselor | T002 | T002 | CS2020-02 |
| Dean | D001 | D001 | - |

**Setup command:**
```bash
docker compose exec backend python manage.py seed_data
```

**Reset command (clears applications/approvals):**
```bash
docker compose exec backend python manage.py seed_data --reset
```

---

## Validation Scenarios

### 1. Compile & Load

**Scenario:** Project compiles without errors

- [ ] **Pass:** Project compiles successfully
- [ ] **Pass:** No compilation errors in console
- [ ] **Pass:** All pages load without crashes

**Evidence slot:** Screenshot of successful compilation

**Fail action:** Document compilation errors, check project.config.json

---

### 2. Login Flow

**Scenario:** Login works for counselor and dean roles

**Test steps (Counselor):**
1. Open login page
2. Enter counselor credentials (T001/T001)
3. Submit login
4. Verify redirect to approvals page

- [ ] **Pass:** Login succeeds, token stored
- [ ] **Pass:** Redirect to /pages/approvals/approvals
- [ ] **Pass:** User info displayed correctly
- [ ] **Pass:** Approval list loads (counselor has access)

**Test steps (Dean):**
1. Logout if logged in
2. Enter dean credentials (D001/D001)
3. Submit login
4. Verify redirect to approvals page

- [ ] **Pass:** Login succeeds, token stored
- [ ] **Pass:** Redirect to /pages/approvals/approvals
- [ ] **Pass:** User info displayed correctly
- [ ] **Pass:** Approval list loads (dean has access)

**Known Phase 4B gap:** Student login (2020006/2020006) succeeds but redirects to /pages/approvals/approvals where students receive 403 FORBIDDEN. Students need dedicated home page or application list page.

**Evidence slot:** Screenshot of successful login + approvals page for counselor and dean

**Fail action:** Check network tab, verify API response format

---

### 3. API Call - List Approvals

**Scenario:** API call using wx.request succeeds

**Test steps:**
1. Login as counselor (T001/T001)
2. Navigate to approvals page
3. Observe network request to `/api/approvals/`

- [ ] **Pass:** Request sent to correct URL
- [ ] **Pass:** Authorization header present
- [ ] **Pass:** Response received and parsed
- [ ] **Pass:** Approval list displayed

**Evidence slot:** Network tab screenshot showing request/response

**Fail action:** Check baseUrl configuration, verify backend running

---

### 4. Error Handling - 401 Unauthorized

**Scenario:** 401 error triggers logout

**Test steps:**
1. Login as counselor (T001/T001)
2. Navigate to approvals page (verify it loads)
3. Open DevTools console
4. Manually delete token from storage:
   ```javascript
   wx.removeStorageSync('token')
   ```
5. Pull down to refresh or navigate to another page

- [ ] **Pass:** 401 detected by API client
- [ ] **Pass:** Token cleared from storage
- [ ] **Pass:** Redirect to login page
- [ ] **Pass:** Error message displayed

**Alternative test (if storage manipulation not available):**
1. Login successfully
2. Wait for token expiry (if tokens have short TTL)
3. Try to access approvals page

**Evidence slot:** Console log showing 401 handling

**Fail action:** Check onUnauthorized callback in api.ts

**Note:** Stopping backend server creates network failure (connection refused), not 401. This scenario requires token manipulation.

---

### 5. Error Handling - 403 Forbidden

**Scenario:** 403 error displays correctly

**Test steps:**
1. Login as student (2020006/password)
2. Try to access counselor-only approval
3. Observe 403 response

- [ ] **Pass:** 403 error caught
- [ ] **Pass:** Error message displayed to user
- [ ] **Pass:** No crash or blank screen

**Evidence slot:** Screenshot of 403 error display

**Fail action:** Check error handling in page logic

---

### 6. Error Handling - 409 Conflict

**Scenario:** 409 conflict (approval already decided) displays correctly

**Test steps:**
1. Login as counselor
2. Approve an application
3. Try to approve same application again (triggers 409)

- [ ] **Pass:** 409 error caught
- [ ] **Pass:** Conflict message displayed
- [ ] **Pass:** Page state remains consistent

**Evidence slot:** Screenshot of 409 error display

**Fail action:** Check conflict handling in approve/reject actions

---

### 7. Network Failure

**Scenario:** Network failure displays retry option

**Test steps:**
1. Disconnect network
2. Try to load approvals page
3. Observe network failure

- [ ] **Pass:** Network error caught
- [ ] **Pass:** Error message displayed
- [ ] **Pass:** Retry button available
- [ ] **Pass:** Retry works after reconnecting

**Evidence slot:** Screenshot of network error + retry

**Fail action:** Check wx.request fail callback

---

### 8. Form Validation

**Scenario:** Login form validates input

**Test steps:**
1. Open login page
2. Submit empty form
3. Observe validation error

- [ ] **Pass:** Empty fields prevented
- [ ] **Pass:** Error message displayed
- [ ] **Pass:** Form remains editable

**Evidence slot:** Screenshot of validation error

**Fail action:** Check form validation logic in login.ts

---

## Base URL Validation

**Critical check:** Verify hardcoded baseUrl works in DevTools

- [ ] **Pass:** `http://localhost:8001` accessible from DevTools
- [ ] **Pass:** API calls reach backend successfully
- [ ] **Pass:** No CORS or network policy issues

**Evidence slot:** Network tab showing successful API calls

**Fail action:** Document actual baseUrl needed, update all pages

---

## Gate Decision

### ✅ Validation Passes
- All scenarios pass or have minor UI fixes
- API contract validated
- Error handling works
- **Action:** Proceed to Phase 4B

### ⚠️ Small Fixes Needed
- 1-2 scenarios fail with clear fixes
- No contract/backend issues
- **Action:** Fix issues, re-validate, then proceed

### ❌ Contract/Backend Issues
- API responses don't match contract
- Backend errors or missing endpoints
- **Action:** Patch backend/contract first, then re-validate

### 🚫 DevTools Unavailable
- Cannot install/configure DevTools after 3 days
- **Action:** Document blocker, do low-rework prep only

---

## Evidence Collection

**Required artifacts:**
- Compilation success screenshot
- Login flow screenshots (all roles)
- Network tab screenshots (API calls)
- Error handling screenshots (401/403/409)
- Console logs (if errors occur)

**Storage location:** `.omc/phase4a-evidence/`

---

**Status:** Ready for execution when DevTools available  
**Owner:** Operator/QA  
**Estimated time:** 2-4 hours of active testing
