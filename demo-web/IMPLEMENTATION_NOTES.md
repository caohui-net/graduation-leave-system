# Demo-Web UI Fixes Implementation

1. **API Integration (api.js)**:
   - Created demo-web/js/api.js to handle backend fetch requests.
   - Defined TestAccounts for student, dorm_manager, counselor, and dean.
   - Handled JWT token acquisition on role switch.

2. **Role Mapping and UI Flow**:
   - Wired up the role selector (switchRole) to trigger apiLogin.
   - Re-added the missing student role into roleMap.
   - Refactored switchRole so that logging in as student or dean hides approval buttons and shows the 'My Applications' text correctly.
   - Wired DOMContentLoaded to auto-login to the default selected role.

3. **Approval API Workflows**:
   - Created loadApprovals() to fetch real approval data from /api/v1/approvals/.
   - Created doApprove() and doReject() mapped to the respective buttons with apiApprove and apiReject.
   - Added openApproval(id) logic to render the application details correctly based on actual API data.

4. **Form Submission and Attachments**:
   - Created doSubmitApplication() function which wraps phone, reason, and uploadedFiles into a FormData object.
   - Bound it to the 提交申请 button.
   - Used fetch to submit a POST to /api/v1/applications/.
