# TASK-20260615-01 Project Code Audit And Analysis

## Goal
Audit the graduation leave system codebase for correctness, security, integration, deployment, and test risks, then report prioritized findings with concrete file references.

## Scope
- Backend Django/DRF APIs, auth/SSO, models, permissions, file handling, and settings.
- Frontend, mini program, and demo integration surfaces where they affect backend contracts.
- Deployment scripts/configuration and tests relevant to production readiness.
- No code fixes unless explicitly requested.

## Phases
| Phase | Status | Notes |
| --- | --- | --- |
| 0. Load protocols and restore context | complete | Read RTK, collaboration protocol, Codex review protocol, existing planning files, git status, and file inventory. |
| 1. Map architecture and dependencies | in_progress | Identify framework versions, entry points, settings, URL surfaces, and runtime assumptions. |
| 2. Audit backend security and business logic | pending | Review auth, permissions, SSO, workflows, uploads/downloads, data import, and serializers. |
| 3. Audit frontend/miniprogram contract alignment | pending | Compare client calls/types with backend API contracts. |
| 4. Audit deployment/config/test posture | pending | Inspect Docker, env handling, scripts, and test coverage. |
| 5. Summarize findings | pending | Produce prioritized audit report with references and verification notes. |

## Errors Encountered
| Error | Attempt | Resolution |
| --- | --- | --- |
| Initial rule read omitted `rtk` prefix | First command in this session before RTK was known | Subsequent project shell commands use `rtk`. |
