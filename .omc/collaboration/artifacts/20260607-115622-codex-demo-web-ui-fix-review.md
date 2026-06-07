# Demo-Web UI Fix - Codex Review

**Task:** task-20260607-demo-web-ui-fix
**Reviewer:** Codex
**Date:** 2026-06-07
**Scope:** demo-web/index.html changes for contact_phone, student role, counselor timeline node

## Review Result

Overall conclusion: needs modification before accepting the 3 completed UI fixes.

## Per-Change Review

1. Add `contact_phone`: needs modification

- Backend schema match: partial. `ApplicationCreateSerializer` requires `contact_phone` and accepts max length 20, so adding the field is directionally correct.
- Issue: the input is not inside a form and the submit button has no validation handler, so `required` and `pattern="[0-9]{11}"` do not actually block submission in the current UI.
- Issue: no `name="contact_phone"` is present, which will matter once API payload collection is implemented.
- Note: backend does not enforce 11 digits; frontend is stricter than backend. That may be acceptable, but it is not a backend-schema requirement.

2. Add student role: needs modification

- Backend role value `student` matches `UserRole.STUDENT`.
- Issue: adding `student` as the first option makes the selector display "学生" by default, while `currentRole`, `role-display`, nav title, and approval buttons still initialize as dorm manager state.
- Issue: the change regresses dean wording. Backend treats dean as an archive/global approved-application role, but the UI now labels dean view as "我的申请" instead of the previous "备案查询".
- Issue: only `#approval-actions` is hidden for student/dean; the approval comment card remains visible, so the detail page still looks like an approval operation view.

3. Add counselor approval node: needs modification

- Backend workflow is `submit -> pending_dorm_manager -> pending_counselor -> approved`.
- Backend creates only dorm-manager approvals at submission time; counselor approval is created after dorm-manager approval.
- Issue: counselor node tag says "待宿管审批", which is an application-level current status, not the counselor step status. In this state, counselor should be shown as "未开始" or "待宿管通过后生成".
- Issue: `demo-web/index.html` removed the opening `<div style="position: relative; padding-left: 30px; margin-bottom: 20px;">` for the "提交申请" timeline item, leaving its absolute-positioned marker outside a timeline item wrapper.

## Findings

- P1: `demo-web/index.html:297` has broken timeline item structure for "提交申请"; restore the missing wrapper div.
- P1: `demo-web/index.html:123-128` and `demo-web/index.html:322-356` initialize inconsistent role state after adding student as the first option.
- P1: `demo-web/index.html:346-349` labels dean view as "我的申请", inconsistent with backend dean/archive behavior.
- P2: `demo-web/index.html:155` uses `required` and `pattern`, but no form submission or `checkValidity()` path triggers the validation.
- P2: `demo-web/index.html:275-283` uses misleading counselor timeline wording for the current `pending_dorm_manager` state.
- P2: `demo-web/index.html:307-317` leaves approval comment UI visible when actions are hidden for student/dean.

## Recommendations

- Put application inputs in a `<form>` and call `form.checkValidity()` / `reportValidity()` before API submission, or implement equivalent JS validation.
- Add `name="contact_phone"`, `maxlength="20"`, and preferably `inputmode="numeric"` to the phone input; decide whether 11 digits is a business rule and mirror it in backend validation if required.
- Either keep default role as dorm manager with `<option value="dorm_manager" selected>`, or initialize the whole UI by calling `switchRole(document.getElementById('roleSelector').value)` on load.
- Preserve dean wording as "备案查询" and hide approval operations for dean without turning the dean list into "我的申请".
- Hide the entire approval operation block for student/dean, not just the buttons.
- Model the static timeline for `pending_dorm_manager` as: counselor "未开始", dorm manager "待审批", submitted "已完成"; then add a status mapping for other states when API integration is added.

## Verification

- Reviewed backend schema and state machine in:
  - `backend/apps/applications/serializers.py`
  - `backend/apps/applications/models.py`
  - `backend/apps/applications/views.py`
  - `backend/apps/users/models.py`
  - `backend/apps/approvals/models.py`
  - `backend/apps/approvals/views.py`
  - `backend/apps/approvals/validators.py`
- Attempted backend tests with `python3 manage.py test ...`, but the environment lacks Django (`ModuleNotFoundError: No module named 'django'`).
- Attempted HTML validation with `tidy`, but `tidy` is not installed in this environment.
