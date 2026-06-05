# Consensus: Implementation Plan Review

**Date:** 2026-06-05  
**Participants:** Claude, Codex  
**Topic:** 用户需求最终确认与实施方案.md review and P0 blocker resolution  
**Status:** ✅ Consensus achieved, implementation-ready

---

## Agreement Summary

**Codex assessment:** 22/40 score, 3 P0 blockers prevent immediate implementation.

**Claude response:** All P0 blockers addressed via Phase 0 data validation scripts.

**Consensus:** Implementation plan is sound after Phase 0 additions. Proceed with Phase 0 execution when real data files available.

---

## P0 Blocker Resolutions (Agreed)

### P0-1: Empty Student ID → Temp ID Strategy ✅

**Problem:** User.user_id required but 271 grad + File2 unmatched lack student numbers.

**Solution:** 3-tier ID generation
- Priority 1: Real XH from File2
- Priority 2: `GRAD2026_{hash8}` for graduates (SHA256 stable hash)
- Priority 3: `TMP2026_{row:04d}` for File2 unmatched

**Implementation:** `generate_temp_user_ids.py` (tested, committed)

**File5 schema extensions:**
- `user_id` (required): Login ID (real or generated)
- `student_no` (optional): Real XH from File2
- `user_id_source`: 'file2_xh' | 'grad_generated' | 'tmp_generated'
- `source_row_id`: File1 original row number

**Agreement:** This preserves data integrity while allowing full 5830-row import.

---

### P0-2: Multi-Approver Conflict → Primary Manager ✅

**Problem:** Document suggests "any manager" but Approval.approver is single FK.

**Solution:** MVP scope reduction
- File3 must provide `primary_dorm_manager_user_id` per building
- Each building has exactly one primary responsible manager
- Multi-manager approval deferred to Phase 2

**Implementation requirement:** File3 processing identifies single primary (first listed, manual spec, or default rule).

**Agreement:** This maintains clean FK model while providing Phase 2 upgrade path.

---

### P0-3: ClassMapping Removal → Explicit Task List ✅

**Problem:** ClassMapping deeply embedded, removal underestimated.

**Solution:** Phase 2 expanded to 10 explicit subtasks
1. Data model adjustments
2. Submission routing refactor
3. Approval pass routing refactor
4. List filtering refactor
5. Detail permissions refactor
6. Attachment permissions sync
7. Import command rewrite
8. API schema update
9. Frontend/miniprogram types sync
10. Test fixture and regression

**Validation gate:** `validate_routing_coverage.py` enforces 100% coverage before Phase 2.

**Agreement:** Expanded task list prevents underestimation. Gate ensures data readiness.

---

## P1 Findings (Acknowledged)

### Data Inconsistency
- File1/File2 count discrepancy (155 vs 271+116) needs reconciliation
- Merge report will output: `matched_count`, `file1_only_count`, `file2_only_count`
- File2-only 116 rows: User to decide import vs archive

### State Machine Naming
- Keep existing `pending_dorm_manager` / `pending_counselor` convention
- Avoid unnecessary migration from current backend/apps/applications/models.py

### Application Snapshots
- Add `student_building_name`, `student_department` to Application model
- Deferred to Phase 2 data model task
- Prevents routing corruption when User data changes

### Normalization Maps
- College: 18 mappings in `normalize_colleges.py` ✅
- Building: Requires File3 analysis, pending
- Both required for 100% routing coverage

**Agreement:** These are implementation details, not blockers. Address in Phase 0-2.

---

## User Supplemental Requirement

**User statement (2026-06-05):**
> "文件5的数据中应该有寝室号字段，文件3中没有，后面会再确认提交文件3的寝室号字段数据，以形成单一对应关系"

**Status:**
- ✅ File5 includes `room_number` field (merge_student_data.py line 131)
- ✅ Documented in implementation plan Section 2
- ✅ Two-phase strategy: Phase 1 building-level, Phase 2 room-level precise

**Agreement:** Room_number preserved for future File3 upgrade. No action required now.

---

## Phase 0 Implementation Status

### Completed (2026-06-05)

**Scripts created and tested:**

1. **generate_temp_user_ids.py** (94 lines)
   - `determine_user_id()`: 3-tier ID strategy
   - `generate_grad_user_id()`: SHA256 hash for graduates
   - `generate_tmp_user_id()`: Sequential for File2 unmatched
   - Tests: ✅ Pass (real XH, grad hash stability, tmp sequential)

2. **merge_student_data.py** (182 lines)
   - `merge_files()`: File1+File2 → File5 with source tracking
   - Matching key: "姓名+规范化学院+班级/BH"
   - Output: 14 fields including user_id, user_id_source, student_no, room_number
   - Statistics: matched/file1_only/grad/tmp counts, skipped rows

3. **validate_routing_coverage.py** (177 lines)
   - `validate_routing()`: 100% coverage gate check
   - Validates: building→manager, department→counselor
   - Exit: 0 if 100%, 1 with detailed failure report
   - Report: Missing buildings/departments with student counts

4. **normalize_colleges.py** (existing)
   - 18 college mappings
   - ValueError on unmapped names

**Commit:** a142ad8 "feat: Phase 0数据门禁脚本实现" (+547 lines)

**Documentation updated:**
- Implementation plan: File mapping table, Phase 0 section, adjusted timeline
- Status: "⚠️ Codex审查完成，3个P0技术阻塞待修正 (评分22/40)"

### Ready for Execution

**Prerequisites met:** ✅ All Phase 0 scripts implementation-ready

**Awaiting:** Real data files from user
- File1: 1-5830名毕业生（含研究生）.xls
- File2: 2026届预计毕业生5675人.xlsx
- File3: 2026年社区辅导员信息统计表.xls
- File4: 2026年学院辅导员信息统计表.xls

---

## Execution Plan

### Phase 0: Data Validation (Ready Now)

**Step 1: Merge File1 + File2**
```bash
python3 backend/scripts/merge_student_data.py \
  --file1 <path-to-file1> \
  --file2 <path-to-file2> \
  --output backend/data/file5_students_5830.csv \
  --report backend/data/merge_report.json
```

**Expected output:**
- file5_students_5830.csv (5830 rows, non-null user_id)
- merge_report.json (matched/file1_only/grad/tmp counts)

**Step 2: Validate Routing Coverage**
```bash
python3 backend/scripts/validate_routing_coverage.py \
  --file5 backend/data/file5_students_5830.csv \
  --file3 <path-to-file3> \
  --file4 <path-to-file4> \
  --report backend/data/routing_coverage_report.json
```

**Gate criteria:**
- Exit code 0 (100% coverage)
- No missing buildings or departments
- All 5830 students routable

**If gate fails:** Review failure report, fix missing mappings, repeat validation.

### Phase 1-5: Implementation (After Phase 0 Pass)

**Phase 1:** Data preparation (0.5 day)
- Building normalization map
- Primary manager selection per building
- Final CSV cleanup

**Phase 2:** System code adjustment (1-1.5 days)
- 10 explicit subtasks (data model, routing, permissions, etc.)

**Phase 3:** Data import (0.5 day)
**Phase 4:** Frontend adjustment (0.5 day)
**Phase 5:** Testing validation (0.5 day)

**Total timeline:** 4-6 days (increased from original 2.5-3 days)

---

## Open Questions for User

**Q1: Primary Dorm Manager Selection**
When building has multiple managers in File3, which to use?
- Option A: First listed in File3 (simplest)
- Option B: Manual specification via new column
- Option C: Alphabetical by name

**Recommendation:** Option A (first listed) for MVP simplicity.

**Q2: Building Normalization**
Does File3 use same building names as File1?
- If yes: No action needed
- If no: Need building normalization map like colleges

**Action:** Review File3 building names against File1 after file provided.

**Q3: File2-Only 116 Rows**
What to do with 116 students in File2 but not File1?
- Option A: Import as additional students (total 5946)
- Option B: Archive report only, don't import (keep 5830)

**Recommendation:** Option B (archive only) maintains File1 as authoritative base.

**Q4: Admin Role Implementation**
New admin role vs reusing existing dean enum?
- Option A: Reuse `dean`, change display to "学工管理员"
- Option B: Add new `admin` enum, migrate existing

**Recommendation:** Option A (reuse dean) avoids migration.

---

## Final Recommendations

### Immediate Actions (User)

1. **Provide data files** for Phase 0 execution
2. **Answer Q1-Q4** to unblock Phase 1 decisions
3. **Review building names** in File3 vs File1 for normalization needs

### Implementation Approach (Technical)

1. **Phase 0 first, no exceptions:** Gate prevents bad data from entering system
2. **Keep existing conventions:** State machine names, dean role reuse
3. **MVP scope discipline:** Primary manager only, room-level routing Phase 2
4. **Validation evidence required:** Merge report + routing report before Phase 1

### Risk Mitigation

1. **Data quality:** Handled by Phase 0 validation gates
2. **Scope creep:** 10-task Phase 2 checklist prevents underestimation
3. **Routing gaps:** 100% coverage gate blocks implementation until resolved
4. **Business logic:** User questions answered before proceeding

---

## Conclusion

**Consensus achieved:** ✅

**Technical readiness:** All P0 blockers resolved, Phase 0 scripts implementation-ready

**Business readiness:** Pending user answers to Q1-Q4 and data file provision

**Risk assessment:** Low technical risk. Data quality managed by gates. Business decisions need user input.

**Next milestone:** Phase 0 execution passes 100% coverage gate

**Recommendation:** Proceed with confidence once user provides files and answers open questions.

---

**Document Status:** ✅ Complete  
**Date:** 2026-06-05  
**Consensus:** Claude + Codex aligned on P0 resolutions and execution plan  
**Next Step:** Update PROJECT-SUMMARY.md and commit artifacts
