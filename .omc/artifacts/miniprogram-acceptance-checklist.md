# Mini-Program Acceptance Checklist

**Version:** v0.1 (First Narrow Slice)  
**Target:** Prove login→list→detail→action→refresh works with real API

---

## Test Environment

- **Backend:** http://localhost:8001 (Docker container running)
- **Test Accounts:**
  - Student: 2020001 / 2020001
  - Counselor: T001 / T001, T002 / T002
  - Dean: D001 / D001
- **Data Reset:** `docker compose exec backend python manage.py seed_data --reset`

---

## Acceptance Criteria

### 1. Login Flow

**Test Case 1.1: Counselor Login Success**
- [ ] Open mini-program
- [ ] Enter user_id: T001, password: T001
- [ ] Click login
- [ ] Verify: Token stored in wx.storage
- [ ] Verify: Redirect to approvals list
- [ ] Verify: User name displayed (李老师)

**Test Case 1.2: Student Login Success**
- [ ] Enter user_id: 2020001, password: 2020001
- [ ] Click login
- [ ] Verify: Redirect to applications list
- [ ] Verify: User name displayed (张三)

**Test Case 1.3: Login Failure**
- [ ] Enter invalid credentials
- [ ] Verify: Error message displayed
- [ ] Verify: No token stored
- [ ] Verify: Stay on login page

---

### 2. Approvals List (Counselor/Dean)

**Test Case 2.1: View Pending Approvals**
- [ ] Login as T001
- [ ] Verify: List shows pending approvals only
- [ ] Verify: Each item shows: student name, reason, leave_date
- [ ] Verify: Empty state if no pending approvals

**Test Case 2.2: Pagination**
- [ ] Scroll to bottom
- [ ] Verify: Load more if count > 20
- [ ] Verify: No more data message if all loaded

---

### 3. Application Detail

**Test Case 3.1: View Detail from Approvals List**
- [ ] Login as T001
- [ ] Click first pending approval
- [ ] Verify: Detail page shows:
  - Student info
  - Reason, leave_date
  - Application status
  - Approval records (counselor, dean)
  - Dorm checkout status (if available)

**Test Case 3.2: Permission Check**
- [ ] Login as T002
- [ ] Try to view T001's approval
- [ ] Verify: 403 error or redirect

---

### 4. Approve Action

**Test Case 4.1: Approve Success**
- [ ] Login as T001
- [ ] Enter detail of pending approval
- [ ] Click "通过" button
- [ ] Enter comment (optional)
- [ ] Confirm
- [ ] Verify: Success message
- [ ] Verify: Return to list
- [ ] Verify: Approved item removed from list
- [ ] Verify: Re-enter detail shows approval recorded

**Test Case 4.2: Approve Conflict**
- [ ] Login as T001
- [ ] Approve same application twice
- [ ] Verify: 403 error displayed
- [ ] Verify: Error message clear

---

### 5. Applications List (Student)

**Test Case 5.1: View Own Applications**
- [ ] Login as 2020001
- [ ] Verify: List shows own applications
- [ ] Verify: Each item shows: reason, leave_date, status
- [ ] Verify: Status badge (pending/approved/rejected)

**Test Case 5.2: View Detail**
- [ ] Click application
- [ ] Verify: Detail shows approval progress
- [ ] Verify: Can see counselor/dean decisions

---

### 6. Error Handling

**Test Case 6.1: 401 Unauthorized**
- [ ] Clear token from storage
- [ ] Try to access list
- [ ] Verify: Redirect to login
- [ ] Verify: Error message displayed

**Test Case 6.2: 403 Forbidden**
- [ ] Login as T001
- [ ] Try to access T002's approval
- [ ] Verify: Error message "权限不足"
- [ ] Verify: Return to previous page

**Test Case 6.3: Network Error**
- [ ] Stop backend container
- [ ] Try to load list
- [ ] Verify: Network error message
- [ ] Verify: Retry button available

---

## Mock Mode Testing

**Test Case 7.1: Mock Login**
- [ ] Switch to mock mode
- [ ] Login with any credentials
- [ ] Verify: Mock token returned
- [ ] Verify: Mock user data displayed

**Test Case 7.2: Mock Lists**
- [ ] Verify: Mock approvals list loads
- [ ] Verify: Mock applications list loads
- [ ] Verify: Data matches Week 3 samples

---

## Acceptance Gate

**Minimum passing criteria:**
- ✓ Counselor can login → see pending approvals → enter detail → approve → list refreshes
- ✓ Student can login → see own applications → enter detail
- ✓ 401/403 errors handled gracefully
- ✓ Mock mode works without backend

**Not required for v0.1:**
- Student submit application
- Reject action
- Search/filter
- Statistics
- WeChat OAuth
- Real device testing (dev tools only)

---

**Next:** After passing checklist, proceed to Phase 2 (skeleton setup)
