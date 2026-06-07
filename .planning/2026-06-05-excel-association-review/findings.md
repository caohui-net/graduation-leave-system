# Findings & Decisions

## Request
- Review document: `.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md`
- Required output: `.omc/collaboration/artifacts/20260605-XXXX-codex-excel-association-review.md`
- Focus areas: File1+File2 name+college association, building-to-dorm-manager mapping, college-to-counselor versus class-to-counselor gap, P0 user strategy judgment.

## Protocol Findings
- Every project shell command must use `rtk`.
- Collaboration artifacts belong under `.omc/collaboration/artifacts/`.
- Current collaboration state has `TASK-20260605-01` owned by Claude in `in_progress`; Codex should produce the requested artifact without taking over ownership.

## Data Findings
- LibreOffice converted the four Excel files to CSV successfully.
- File1 rows: 5,830. File2 rows: 5,675. File3 rows: 74. File4 rows: 20.
- File1 levels: 4,365 本科, 1,185 专升本, 271 研究生, 9 第二学士学位. File1 blank class rows: 271, all research.
- File2 levels: 4,470 本科, 1,196 专升本, 9 第二学士学位. No research rows in File2.
- Raw name+college matching gives only 4,776 unique File1 row matches because File1/File2 college names differ for 文学院 parentheses and 政法学院 alias.
- With normalized college names, name+college gives 5,524 unique row matches, 36 ambiguous rows, and 270 no-match rows; it also falsely matches one blank-class research student 陈静 to an undergraduate 陈静.
- Safe student matching should require `姓名 + 规范化学院 + 班级/BH`: 5,559 exact matches and 271 no matches. The 271 no matches are the research rows without class in File1.
- File2 has 116 rows not present in File1 by name+normalized-college, likely expected graduates not present in the dorm baseline.
- File1 has 33 unique buildings; File3 covers all 33. Every File1 building maps to multiple File3 rows; two File1 buildings include a `暂未申请` employee id, affecting 300 students if that row is needed.
- File3 has 36 buildings total; 3 are not used by File1.
- File1 has 196 nonblank classes. 184 classes span multiple buildings, covering 5,304 students; a class-level single dorm manager cannot represent actual building-based routing.
- With college alias normalization, File4 covers all 19 File1 colleges and has one counselor per college plus one extra `研究生` row. Deriving class-to-counselor by college is mechanically possible for 196 nonblank classes, but it is a business downgrade from true class ownership.
- Current code path `applications_view.create_application` uses `ClassMapping.objects.get(class_id=user.class_id, active=True)` and requires `class_mapping.dorm_manager`; `ClassMapping` has one counselor and one optional dorm manager per class.

## Decisions
| Decision | Rationale |
| --- | --- |
| Treat user strategy as partially satisfying P0 only | It works for the undergraduate/nonblank-class subset after normalization and class-assisted matching, but not for research rows or exact class-level/dorm-routing semantics. |
| Recommend user strategy plus targeted补数 over full re-request | Existing data can produce a high-coverage import baseline; only research identifiers/classes, dorm approver disambiguation, and true counselor responsibility need confirmation. |

## Issues
| Issue | Resolution |
| --- | --- |
| Existing root planning files are from an older task | Created isolated active plan `.planning/2026-06-05-excel-association-review/`. |
