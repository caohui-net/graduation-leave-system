# Phase 4B Prep Note - Read-Only Verification

**Date:** 2026-05-31  
**Purpose:** Compact handoff note for Phase 4B implementation  
**Method:** Read-only verification (no code changes)  
**Time:** 30-45 minutes

---

## 1. Confirmed Miniprogram Architecture

### Page Registration

**app.json pages array:**
```json
{
  "pages": [
    "pages/login/login",
    "pages/approvals/approvals",
    "pages/detail/detail"
  ]
}
```

**Status:** 3 pages registered, student-application not registered (correct - page doesn't exist yet)

---

### API Client Usage

**All pages import shared ApiClient:**
- `miniprogram/pages/login/login.ts:5` - `import { ApiClient } from '../../services/api'`
- `miniprogram/pages/approvals/approvals.ts:6` - `import { ApiClient } from '../../services/api'`
- `miniprogram/pages/detail/detail.ts:6` - `import { ApiClient } from '../../services/api'`

**Duplication pattern (all 3 pages):**
```typescript
const apiClient = new ApiClient({
  baseUrl: 'http://localhost:8001',
  onUnauthorized: () => {
    wx.removeStorageSync('token');
    wx.removeStorageSync('user');
    wx.redirectTo({ url: '/pages/login/login' });
  }
});
```

**Finding:** Shared ApiClient class is used, but each page instantiates with duplicate config.

---

### Type Definitions Usage

**Imports verified:**
- `miniprogram/pages/approvals/approvals.ts` - `import type { ApprovalListItem } from '../../types/api'`
- `miniprogram/pages/detail/detail.ts` - `import type { ApplicationDetail } from '../../types/api'`

**Status:** Shared types are used. Login page doesn't import types (only uses inline types for login request/response).

---

## 2. Phase 4B Optimization Opportunities

### A. Centralize API Client Configuration

**Current state:** Each page duplicates baseUrl and onUnauthorized config.

**Optimization:**
```typescript
// services/api.ts - add default config
export const defaultApiClient = new ApiClient({
  baseUrl: 'http://localhost:8001',
  onUnauthorized: () => {
    wx.removeStorageSync('token');
    wx.removeStorageSync('user');
    wx.redirectTo({ url: '/pages/login/login' });
  }
});

// pages/*.ts - use default
import { defaultApiClient } from '../../services/api';
```

**Benefit:** Single source of truth for baseUrl and auth handling. Easier to update for production.

**Risk:** Low. Existing pattern works, this is pure refactor.

---

### B. Role-Based Post-Login Routing

**Current state:** All roles redirect to `/pages/approvals/approvals` after login (line 51 in login.ts).

**Problem:** Students hit 403 on approvals page (known Phase 4B gap).

**Optimization:**
```typescript
// After login success
const user = response.data.user;
if (user.role === 'student') {
  wx.redirectTo({ url: '/pages/student-application/student-application' });
} else {
  wx.redirectTo({ url: '/pages/approvals/approvals' });
}
```

**Prerequisite:** Student application page must exist first.

**Priority:** High - fixes known gap.

---

### C. Add Student Page Route Only When Implemented

**Current state:** student-application page not registered in app.json (correct).

**Action for Phase 4B:**
1. Implement student-application page files
2. Register in app.json
3. Update login redirect logic (see B above)

**Order matters:** Register page AFTER implementation, not before.

---

## 3. Checklist Sharp Edges

### 409 Conflict Scenario Precision

**Checklist scenario (lines 122-139):**
```
Test steps:
1. Login as counselor
2. Approve an application
3. Try to approve same application again (triggers 409)
```

**Sharp edge:** Step 3 "try to approve same application again" may be blocked by UI state.

**Potential issues:**
- Approval list may remove approved items immediately
- Detail page may disable approve button after first click
- Need to refresh or navigate back to trigger second approval attempt

**Recommendation for Phase 4A validation:**
- After step 2, explicitly refresh approval list or navigate away and back
- Or manually trigger API call via DevTools console
- Document exact steps that successfully trigger 409

**Alternative test:**
- Two counselors approve same application simultaneously (race condition)
- Requires two DevTools instances or coordination

---

## Summary

**Architecture verified:**
- ✅ Shared api.ts and types.ts are actually used by all pages
- ⚠️ ApiClient config duplicated across pages (low-priority refactor opportunity)
- ✅ Page registration correct (3 pages, student-application not registered)

**Phase 4B priorities:**
1. **High:** Implement student-application page + role-based routing (fixes known gap)
2. **Medium:** Centralize API client config (reduces duplication)
3. **Low:** Refine 409 test scenario (improve validation precision)

**No code changes made.** This is read-only verification only.

---

**Status:** Phase 4B prep note complete  
**Next gate:** WeChat DevTools availability for Phase 4A validation
