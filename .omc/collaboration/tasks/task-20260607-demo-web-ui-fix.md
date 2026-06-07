# Task: Demo-Web UI Business Workflow Alignment

**Task ID:** task-20260607-demo-web-ui-fix
**Created:** 2026-06-07T11:52:00Z
**Status:** in_progress
**Owner:** claude
**Reviewer:** codex

## Objective

Align demo-web/index.html UI implementation with actual backend business workflow to reach production standards.

## Background

Codex analysis (artifact: codex-demo-web-index-html-ui-docs-design-2026-05-27-system-design--2026-06-07T11-48-29-324Z.md) identified 7 critical gaps between demo-web UI and backend workflow.

## Current Progress

**Completed (by Claude):**
1. ✅ Added contact_phone field (required by backend API)
2. ✅ Added student role to role selector
3. ✅ Added counselor approval node to timeline

**Remaining:**
4. ⏳ Integrate API calls for approve/reject actions
5. ⏳ Fix status mapping to backend codes
6. ⏳ Integrate attachment upload with backend
7. ⏳ Implement role-based data filtering

## Request for Codex Review

Please review the 3 completed changes and verify:
1. Implementation correctness against backend schema
2. UI/UX consistency
3. Missing edge cases or validation

Artifact locations:
- Modified file: demo-web/index.html
- Changes: Lines 150-159 (contact_phone), 123-126 (role selector), 271-295 (timeline)

## Next Steps

After review approval:
- Implement remaining 4 items
- Add API integration layer
- Test against localhost:8001 backend
- Verify production readiness
