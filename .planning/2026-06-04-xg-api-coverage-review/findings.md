# Findings & Decisions

## Requirements
- User requested review of XG API data coverage with four dimensions: field coverage, impact of key missing fields, data quality, and recommended integration strategy.
- Required sources: `docs/数据对接说明文档.md`, `docs/XG-API-ACTUAL-DATA-SAMPLES.md`, `docs/phase4c-xg-field-coverage.md`.
- Required output directory: `.omc/collaboration/artifacts/`.
- User included `--model opus`; record in artifact metadata as the requested model/context marker.

## Research Findings
- Project requires every shell command to be prefixed with `rtk`.
- Collaboration protocol requires durable artifacts under `.omc/collaboration/artifacts/` and completion reflected in the collaboration log when part of the workflow.
- Codex review protocol applies to data integration reviews; higher-priority direct user request makes this session itself the review producer.
- Document sizes: requirements 454 lines, actual samples 222 lines, mapping proposal 326 lines.
- Requirements require student `student_id`, `name`, `department`, `major`, `class_id`, `grade`, `graduation_year`, and `is_graduating`; `class_id` drives counselor assignment, and graduation fields drive eligibility/filing.
- XG actual sample covers `number`, `name`, `phone`, `status`, `department`, `parent_dep`, and `user_identity`; sample size is 20 for completeness checks over a 32,039-record API.
- Critical uncovered fields remain `class_id`, `major`, `grade`, `graduation_year`, `is_graduating`, counselor employee id, class-counselor mapping, and dorm checkout state.
- Actual `user_identity` sample is object-shaped (`{"id": 4, "name": "学生"}`), while current mapper accepts only `'1'` or `'student'`; actual `department` is a list but mapper assigns it directly.
- Actual data quality is good for identity/name/status, partial for phone, and incomplete as a source of core graduation workflow truth.
- JSON report has a volume-stat inconsistency: pagination test shows page size 10, but `volume_tests.statistics` uses page size 1, so full-fetch timing estimates need normalization.

## Technical Decisions
| Decision | Rationale |
|----------|-----------|

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| Existing mapping document predates live sample and marks fields as pending | Treat it as strategy baseline, then override with live sample evidence where available. |

## Resources
- `docs/数据对接说明文档.md`
- `docs/XG-API-ACTUAL-DATA-SAMPLES.md`
- `docs/phase4c-xg-field-coverage.md`
