# Step 1 Verification Results - Phase 4A Readiness Repair

**Date:** 2026-05-31 03:25  
**Status:** All 4 Codex issues verified  
**Method:** Runtime-backed verification (seed data, actual files, view permissions)

---

## Issue 1: Stale Test Accounts ✅ VERIFIED

**Checklist claims:**
- Student: 2020006/password
- Counselor: C001/password
- Dean: D001/password

**Actual seed data** (`backend/apps/users/management/commands/seed_data.py`):
- Students: user_id/user_id (line 54: `user.set_password(student_data['user_id'])`)
  - 2020001/2020001, 2020002/2020002, ..., 2020006/2020006
- Counselors: T001/T001, T002/T002 (line 74: `user.set_password(counselor_data['user_id'])`)
  - **C001 does not exist in seed data**
- Dean: D001/D001 (line 88: `user.set_password('D001')`)

**Impact:** Operator will fail all login tests. Critical blocker.

**Fix required:** Update checklist test accounts table with correct credentials.

---

## Issue 2: Wrong 401 Scenario ✅ VERIFIED

**Checklist scenario:**
```
Test steps:
1. Login successfully
2. Stop backend server
3. Navigate to approvals page (triggers 401)
```

**Analysis:** Stopping backend creates network failure (connection refused), not 401 Unauthorized.

**Correct 401 scenario:**
- 401 requires missing/expired/invalid token
- Need to manipulate token in storage, not stop backend
- Example: delete token, modify token to invalid value, or wait for expiry

**Impact:** Operator will see network error, not 401 handling. Wrong validation.

**Fix required:** Rewrite 401 scenario with token manipulation.

---

## Issue 3: Stale Skeleton Gaps ✅ VERIFIED

**Gaps doc claims:**
- `miniprogram/services/api.ts`: Missing
- `miniprogram/types/api.ts`: Missing

**Actual filesystem:**
```
miniprogram/services/api.ts  2.9K
miniprogram/types/api.ts  2.0K
```

**Impact:** Gaps doc misleading. Files already exist.

**Fix required:** Update skeleton gaps to reflect existing files, update missing pieces table.

---

## Issue 4: Student Redirect Bug ✅ VERIFIED

**Checklist scenario:**
```
Test steps:
1. Open login page
2. Enter student credentials (2020006/password)
3. Submit login
4. Verify redirect to /pages/approvals/approvals
```

**Actual behavior:**
- Student login redirects to `/pages/approvals/approvals` (line 51 in `miniprogram/pages/login/login.ts`)
- Approval list view explicitly forbids students (lines 21-26 in `backend/apps/approvals/views.py`):
  ```python
  if user.role == UserRole.STUDENT:
      return Response(
          {'error': {'code': 'FORBIDDEN', 'message': '学生不能访问审批列表'}},
          status=status.HTTP_403_FORBIDDEN
      )
  ```

**Impact:** Student login will succeed but immediately hit 403 on approvals page. This is a Phase 4B gap (need student home page), not a Phase 4A pass criterion.

**Fix required:** 
- Remove student login → approvals scenario from Phase 4A checklist OR mark as known failure
- Add to Phase 4B gaps: "Student login redirects to forbidden approvals page. Need student home page or application list."

---

## Additional Findings

### Reset/Setup Commands

**Seed command:**
```bash
docker compose exec backend python manage.py seed_data
```

**Reset command:**
```bash
docker compose exec backend python manage.py seed_data --reset
```

**Reset behavior** (lines 17-23):
- Deletes all applications
- Deletes all approvals
- Recreates seed users

---

## Verification Summary

| Issue | Status | Evidence |
|-------|--------|----------|
| Stale test accounts | ✅ Verified | seed_data.py lines 54, 74, 88 |
| Wrong 401 scenario | ✅ Verified | Logic analysis (backend stop ≠ 401) |
| Stale skeleton gaps | ✅ Verified | Filesystem check (files exist) |
| Student redirect bug | ✅ Verified | views.py lines 21-26 (403 FORBIDDEN) |

---

## Next Steps

- Step 2: Fix validation checklist (20 min)
- Step 3: Fix skeleton gaps (15 min)
- Step 4: Optional dorm request (10 min, skip if time risk)

---

**Status:** Step 1 complete, ready for Step 2
