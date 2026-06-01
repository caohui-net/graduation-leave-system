# Week 4 Blocked Prep Analysis - Codex Recommendation

**Date:** 2026-05-31
**Context:** Phase 4A blocked on WeChat DevTools installation; production blocked on dorm provider access.
**Recommendation:** Do a bounded low-rework prep bundle: A + C + E, plus a small documentation/code alignment correction for dorm provider discovery. Defer B and D until runtime validation or external provider facts exist.

## Decision

Do multiple small tasks, not one larger speculative task.

Priority order:

1. **A. Create Phase 4A validation checklist**
2. **C. Document DevTools setup steps**
3. **E. Audit existing miniprogram skeleton and Phase 4B gaps**
4. **G. Better option: create a small "dependency closure pack" artifact that ties A/C/E together and fixes known stale references**

Do not start broad 4-page architecture design yet. Do not draft a full real dorm provider adapter yet.

## Why

The current consensus explicitly says that if DevTools remains unavailable, fallback work must be low-rework validation prep. A/C/E match that constraint. They improve execution speed without committing to UI structure that may fail in DevTools.

B has moderate rework risk because the current miniprogram runtime, page registration, API base URL behavior, and wx.request/auth behavior are still unvalidated. It is acceptable only as a gap inventory, not as detailed component architecture.

D has moderate to high rework risk because the real provider contract, auth method, schema, network constraints, and test data are all unknown. The backend already has a simple mock provider in `backend/apps/applications/providers.py`, so interface work should wait for facts or be limited to documenting expected contract questions.

## Option Ranking

| Option | Rework Risk | Execution Value | Recommendation |
| --- | --- | --- | --- |
| A. Phase 4A checklist | Lowest | High for 4A | Do first |
| C. DevTools setup guide | Lowest | High for 4A | Do first |
| E. Skeleton/gap audit | Low | High for 4B | Do after A/C |
| D. Dorm adapter interface | Medium/high | Medium later | Defer; only document unknowns |
| B. 4-page architecture | Medium | Medium/high later | Defer detailed design |
| F. Wait | No rework | No value | Reject |

## Concrete Findings From Quick Skeleton Check

- `miniprogram/app.json` currently registers `login`, `approvals`, and `detail`; the agreed `student-application` page does not exist yet.
- `miniprogram/services/api.ts` has useful wx.request coverage for login, create/list/get applications, list approvals, approve, and reject.
- API client instances are duplicated per page with repeated base URL and unauthorized handling.
- The current hardcoded base URL is `http://localhost:8001`; DevTools validation should confirm whether this maps correctly in the target environment.
- Dorm discovery brief references `backend/apps/applications/dorm_provider.py`, but the current provider file is `backend/apps/applications/providers.py`.

## Recommended Prep Bundle

Create one short "Phase 4A readiness pack" with:

- DevTools install/import/configuration runbook.
- Validation checklist with pass/fail fields and evidence slots.
- Test accounts/student IDs/API base URL placeholders.
- Required error scenarios: 401, 403, 409, network failure, validation error.
- Skeleton gap table for Phase 4B: existing, missing, risky, blocked.
- Known stale reference fixes, especially provider file naming.

Timebox: 2-3 hours.

## Decision Criteria

Choose prep work that satisfies all of these:

1. It shortens Phase 4A or prevents ambiguous Phase 4A results.
2. It survives either DevTools success or failure.
3. It does not require unknown external contracts.
4. It produces durable evidence or a checklist, not speculative UI code.
5. It reveals blockers earlier than implementation would.

By those criteria, A/C/E bundled together wins.

## Work To Defer

- Detailed 4-page component architecture until Phase 4A proves runtime/API assumptions.
- Real dorm provider adapter implementation until contact, schema, credentials, and test data exist.
- Attachments or new UI feature expansion until the validation gate is passed.

