# TASK-20260615-01 Project Audit Findings

## Protocols
- Project shell commands must be prefixed with `rtk`.
- Formal Codex review workflows must follow `docs/codex-review-protocol.md`.
- Root `task_plan.md`, `findings.md`, and `progress.md` are from a completed 2026-05-31 task; this audit uses `.planning/2026-06-15-project-audit/` to avoid overwriting prior records.

## Findings
- Repository has multiple runtime surfaces: `backend/` Django/DRF API, `frontend/` React/Vite code, `miniprogram/` WeChat TypeScript pages, `demo-web/` static demo/admin SSO callback pages, Docker compose files, deployment scripts, and integration/test scripts.
- Worktree is dirty with many pre-existing `.omc`, `.collab`, `.wolf`, docs, and backend changes; audit must avoid reverting unrelated work.
- `rg --files` indicates backend apps include `users`, `applications`, `approvals`, `notifications`, `attachments`, `sso_qingganlian`, and `healthcheck`.
- Existing documentation contains prior architecture/security/data/API review artifacts, which are useful historical context but this audit is based on current code.
- Backend stack: Django 4.2.13, DRF 3.14, SimpleJWT, django-filter, drf-spectacular, PostgreSQL, optional Celery/Redis dependencies, WeChat/SSO dependencies.
- Production compose runs Gunicorn and avoids DB port exposure; development compose exposes PostgreSQL on `5432` and runs Django `runserver`.
- `backend/config/settings/base.py` defaults `SECRET_KEY`, `DEBUG=True`, DB password `postgres`, and embeds default Qingganlian SSO app key/secret values. `prod.py` blocks insecure Django SECRET_KEY and demo auth, but does not validate SSO secrets.
- URL config redirects `/` to hard-coded `http://218.75.196.218:7788/`; API docs are available under `/api/schema/`.
- `frontend/` has TypeScript service/types/component files but no `package.json` in that directory; `miniprogram/` is the concrete WeChat app and hard-codes default API base URL to `http://localhost:8001`.
- WeChat app stores JWT and user info in `wx` local storage/global data.
