# Code Audit and Analysis Report: Graduation Leave System

## Executive Summary
An in-depth code audit was conducted on the `graduation-leave-system` codebase. The architecture is built on Django (DRF) for the backend and a lightweight Vanilla JS SPA for the frontend. The system demonstrates solid transactional integrity and fundamental security controls. However, critical vulnerabilities regarding SSO token verification and significant performance bottlenecks (N+1 query issues) were identified.

## 1. Security Findings

### 1.1 SSO Token Verification Bypass (Severity: CRITICAL)
**Location:** `backend/apps/sso_qingganlian/views.py` and `backend/apps/sso_qingganlian/settings.py`
**Description:** The SSO login logic relies on environment variables (`QGL_VERIFY_ADMIN_TOKEN`, `QGL_VERIFY_MOBILE_TOKEN`) to determine whether to validate the token provided by the Qingganlan SSO callback. If these are set to `False`, the system blindly trusts the `user_id` provided in the request payload, completely bypassing authentication.
**Impact:** Total system compromise. An attacker can spoof any `user_id` (including administrators) and gain unauthorized access if deployed with these settings disabled.
**Remediation:**
1.  **Enforce Validation in Production:** Ensure `QGL_VERIFY_MOBILE_TOKEN=True` and `QGL_VERIFY_ADMIN_TOKEN=True` are strictly enforced in the production environment.
2.  **Code-level Safeguard:** Modify `settings/prod.py` to hard-fail or force these settings to `True` regardless of environment variables.

### 1.2 CSV Injection Protection (Severity: LOW - Mitigated)
**Location:** `backend/apps/approvals/views.py` (`sanitize_excel_formula`)
**Description:** The application correctly implements a `sanitize_excel_formula` function to prepend a single quote (`'`) to strings starting with `=`, `+`, `-`, or `@`. This successfully mitigates CSV/Excel injection attacks when administrators export data.
**Remediation:** No action needed. Good practice observed.

### 1.3 JWT Token Storage (Severity: MEDIUM)
**Location:** `demo-web/js/api.js`
**Description:** The frontend stores the JWT access token in `localStorage`.
**Impact:** Tokens stored in `localStorage` are vulnerable to Cross-Site Scripting (XSS) attacks. If an attacker injects malicious JavaScript, they can easily extract the tokens.
**Remediation:** Consider transitioning to `HttpOnly` secure cookies for token storage. This prevents JavaScript from accessing the token directly. If `localStorage` must be used, ensure rigorous Content Security Policy (CSP) headers are implemented.

### 1.4 File Upload Validation (Severity: LOW - Mitigated)
**Location:** `backend/apps/attachments/serializers.py`
**Description:** The `AttachmentUploadSerializer` correctly enforces a 10MB file size limit and restricts allowed file extensions to a safe list (`.jpg`, `.jpeg`, `.png`, `.pdf`, `.doc`, `.docx`).
**Remediation:** No action needed. Good practice observed.

## 2. Architecture and Code Quality Findings

### 2.1 N+1 Query Bottlenecks (Severity: HIGH)
**Location:** `backend/apps/applications/views.py` (`list_applications`)
**Description:** The `ApplicationListSerializer` utilizes a `SerializerMethodField` (`get_approvals`) that calls `obj.approvals.all()`. However, the `get_queryset` logic in `list_applications` does not use `prefetch_related('approvals')` or `select_related('student')`.
**Impact:** When listing applications (especially for Deans/Admins viewing the whole list), Django will execute one query to fetch the applications, and then **N additional queries** (where N is the number of applications on the page) to fetch the related `student` data and `approvals`. This will severely degrade database performance under load.
**Remediation:** Update `list_applications` to prefetch related data.
```python
# In backend/apps/applications/views.py -> list_applications
queryset = Application.objects.all().select_related('student').prefetch_related('approvals')
```
*(Note: Apply similar optimizations to the student, dorm manager, and counselor query paths).*

### 2.2 Approval Workflow Architecture (Severity: INFO)
**Location:** `backend/apps/approvals/views.py`
**Description:** The 2-level approval logic (Dorm Manager -> Counselor) is handled directly within the views and serializers. The system intelligently auto-completes duplicate manager roles to prevent workflow blockage.
**Remediation:** The logic is functionally correct and utilizes `select_for_update()` to prevent race conditions during concurrent approval actions.

## 3. General Recommendations

1.  **Django Debug Toolbar:** Install `django-debug-toolbar` in the development environment to proactively catch N+1 queries.
2.  **Environment Variables:** Ensure that the `SECRET_KEY` is securely generated and that `DEBUG=False` in the `.env.prod` file. The existing checks in `settings/prod.py` are excellent safeguards.
3.  **API Error Formatting:** Standardize all API error responses. Currently, DRF default validation errors might return arrays of strings, whereas custom views return `{'error': {'code': ..., 'message': ...}}`. A custom exception handler in DRF should be implemented to unify the payload structure.
