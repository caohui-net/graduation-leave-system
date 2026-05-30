# TASK-20260530-06: Collaboration Readiness Gate + Week 3 Day 0 Canary Pilot

**Created:** 2026-05-30T09:38:30Z  
**Owner:** Claude + Codex  
**Status:** open  
**Type:** Implementation + Validation + Pilot  
**Priority:** P0  
**Estimated Time:** 3-4.5 hours

---

## Context

TASK-20260530-05 synthesis reached consensus: P0 implementation has verifiable gaps. Must fix before pilot.

**Consensus:** `readiness gate → minimal tests → canary pilot → evidence docs`

**Key finding:** Protocol claims v0.3 complete, but has 7 observable defects that will corrupt pilot results.

---

## Objective

Execute 4-phase workflow to validate collaboration protocol and pilot on real Week 3 Day 0 task.

---

## Phase 1: Readiness Gate (60-90min hard timebox)

**Owner:** Claude + Codex collaboration  
**Goal:** Fix P0 implementation gaps

### Must Fix (4 items)

1. **Protocol version drift**
   - Current: `.omc/collaboration/protocol.md` line 3 says `Version: 0.2`
   - Expected: `Version: 0.3` or document as intentionally 0.2
   - Action: Update version or add comment explaining 0.2 is correct

2. **Atomic claim race condition**
   - Current: `.claude/skills/claude-codex-collab/scripts/collab_task.py` lines 479-482 release lock before `append_event`
   - Expected: Hold lock for full check-append sequence
   - Action: Move `append_event` call inside lock, remove intermediate `release_lock()`

3. **Event status mapping incomplete**
   - Current: `collab_event.py` line 100 maps unknown types to `in_progress`
   - Expected: `independent_analysis_completed` → `waiting_synthesis`
   - Action: Add to `status_map`: `"independent_analysis_completed": "waiting_synthesis"`, `"synthesis_completed": "completed"`

4. **Gemini dry-run not independent**
   - Current: `.omc/collaboration/scripts/invoke-gemini-analysis.sh` line 83 checks CLI before dry-run
   - Expected: Dry-run works without Gemini installed
   - Action: Move `command -v gemini` check after `if [[ "$DRY_RUN" == true ]]` branch

### Validation

- Run `.omc/collaboration/scripts/validate-journal.sh` before fixes
- Run after each fix
- Run final validation before Phase 2
- All validations must pass

### Stop Rule

If fixes exceed 90min, stop and reassess P0 scope. Don't proceed to Phase 2.

---

## Phase 2: Minimal Invariant Tests (30-45min)

**Owner:** Codex leads  
**Goal:** Prove core protocol invariants

### Test Scope (4 tests, not full harness)

1. **Sequential event append consistency**
   - Append 3 events sequentially
   - Verify: IDs contiguous, state.last_event_id matches max, no duplicates

2. **Atomic claim simulation**
   - Use barrier-based approach from earlier consensus
   - Two processes attempt simultaneous claim
   - Verify: Only one succeeds, no duplicate claim events

3. **Independent analysis event status**
   - Append `independent_analysis_completed` event
   - Verify: Status becomes `waiting_synthesis` (not `in_progress`)

4. **Gemini dry-run artifact creation**
   - Run `invoke-gemini-analysis.sh --dry-run` without Gemini CLI
   - Verify: Artifact created, event logged, no CLI error

### Test Environment

- Run against temp copy of `.omc/collaboration/`
- Don't pollute production collaboration state

### Stop Rule

If any test fails, create repair task. Don't proceed to Phase 3.

---

## Phase 3: Week 3 Day 0 Canary Pilot (1-2 hours)

**Owner:** Claude + Codex collaboration  
**Goal:** Use protocol for real Week 3 Day 0 preparation task

### Pilot Task Scope

From `docs/discussions/week3-direction-2026-05-30/06-consensus.md`:

1. **Environment strategy decision**
   - Check local dependencies (Python, PostgreSQL, Django)
   - Decide: local / Docker PostgreSQL / full Compose
   - Document decision with rationale

2. **Seed data requirements**
   - List required accounts (students, counselors, dean)
   - List required mappings (class-counselor)
   - Specify minimum data for 2-level approval flow

3. **Acceptance checklist creation**
   - 8-item checklist from Week 3 consensus
   - Migration success, seed data, login, submit, approve, query, permissions, mock service

### Validation Checkpoints

- **Before pilot:** Run `validate-journal.sh`
- **After each handoff:** Run `validate-journal.sh`
- **After completion:** Run `validate-journal.sh`

All checkpoints must pass. If validation fails, stop and repair journal.

### Gemini Participation

- Optional/read-only
- If API returns 500, record failure artifact and continue
- Don't block pilot on Gemini success

### Stop Rules

- Validation fails → stop, repair journal, document failure mode
- Week 3 Day 0 discovers architecture blocker → follow Week 3 consensus decision gate (pause extension work)
- Collaboration state inconsistent → stop product work, repair first

---

## Phase 4: Evidence-Based Documentation (30-45min)

**Owner:** Claude leads  
**Goal:** Document what was proven, not what was planned

### Document Only

1. **Operator checklist**
   - What was validated (which checkpoints passed)
   - What commands to run (validation, handoff, completion)
   - What to check (event log, state consistency, locks)

2. **Failure modes found**
   - What broke during pilot
   - How it was detected
   - How it was repaired

3. **State transitions used**
   - Which statuses were actually used
   - Which event types were actually logged
   - Which workflows were actually executed

4. **Open risks**
   - What's still unknown
   - What wasn't tested
   - What needs future validation

### Defer

- Comprehensive protocol guide
- PROJECT-SUMMARY updates (wait for more evidence)
- Broad architectural documentation

---

## Acceptance Criteria

- [ ] Phase 1: All 4 fixes applied, validation passes
- [ ] Phase 2: All 4 tests pass
- [ ] Phase 3: Week 3 Day 0 artifacts created (environment strategy, seed data, checklist)
- [ ] Phase 3: All validation checkpoints passed
- [ ] Phase 4: Operator checklist exists
- [ ] Event log updated with all phases
- [ ] Git commit + push

---

## Success Criteria

**Minimum success:**
- Readiness gate complete
- Tests pass
- Pilot produces Week 3 Day 0 artifacts
- Validation passes at all checkpoints

**Full success:**
- Above + no failures during pilot
- Above + operator checklist reflects clean execution

---

## Failure Criteria

- Readiness gate exceeds 90min
- Any test fails and can't be fixed quickly
- Pilot validation fails
- Week 3 Day 0 discovers architecture blocker

---

## Time Budget

- Phase 1: 60-90min (hard timebox)
- Phase 2: 30-45min
- Phase 3: 1-2h
- Phase 4: 30-45min
- **Total:** 3-4.5 hours

---

## References

- Synthesis: `.omc/collaboration/artifacts/20260530-0937-claude-synthesis-next-steps.md`
- Codex analysis: `.omc/collaboration/artifacts/20260530-1733-codex-next-steps-analysis.md`
- Week 3 consensus: `docs/discussions/week3-direction-2026-05-30/06-consensus.md`
- Protocol: `.omc/collaboration/protocol.md`

---

## Notes

- This task serves the graduation system Week 3 plan, not protocol tooling
- Protocol work is means to an end, not the product goal
- Hard timeboxes prevent scope creep
- Validation checkpoints prevent blind trust
- Evidence-based docs prevent aspirational documentation
