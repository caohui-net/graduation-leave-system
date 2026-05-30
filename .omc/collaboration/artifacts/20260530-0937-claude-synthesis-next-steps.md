# Next Steps Synthesis - Claude & Codex

**Task:** TASK-20260530-05  
**Date:** 2026-05-30  
**Synthesis by:** Claude  
**Status:** Consensus reached

---

## Executive Summary

**Consensus:** Adopt Codex's recommendation with minor refinements.

**Next step:** `readiness gate (60-90min) → minimal invariant tests → Week 3 Day 0 canary pilot → evidence-based docs`

Both agents rejected the simple P1 sequence (docs → tests → pilot). Claude proposed skipping to pilot; Codex proposed instrumented pilot with mechanical gate first. **Codex's position is stronger** because it addresses the technical gaps Claude overlooked.

---

## Position Comparison

### Claude's Position
- **Proposal:** Skip P1 documentation, go straight to production pilot
- **Core insight:** Don't document untested systems
- **Weakness:** Underestimated P0 implementation gaps

### Codex's Position
- **Proposal:** Readiness gate → minimal tests → canary pilot → evidence-based docs
- **Core insight:** P0 has verifiable gaps that will corrupt pilot results
- **Strength:** Identified 7 specific technical issues with evidence

---

## Agreement Areas

Both agents agree on:

1. **Documentation-first is wrong** - Writing guides before execution creates aspirational docs
2. **Direct unguarded pilot is risky** - Need validation checkpoints
3. **Evidence-based approach** - Document what's proven, not what's planned
4. **Week 3 Day 0 as pilot target** - Real task, controlled scope
5. **Protocol is means, not end** - Serve graduation system, not tooling project

---

## Key Disagreement

**Claude:** Protocol is "untested but probably works" → pilot will expose issues  
**Codex:** Protocol has "known gaps with evidence" → pilot will produce confusing results

**Resolution:** Codex is correct. Evidence:
- Protocol version drift (0.2 vs claimed 0.3)
- `collab_task.py` claim race (releases lock before append)
- Event status mapping incomplete (`independent_analysis_completed` → `in_progress` not `waiting_synthesis`)
- Gemini dry-run requires CLI (not truly dry-run)

These aren't hypothetical risks. They're observable defects.

---

## Codex's Technical Findings - Validation

### Finding 1: Protocol Version Drift
**Claim:** Protocol says v0.2, context says v0.3  
**Verification:** Confirmed. `.omc/collaboration/protocol.md` line 3: `Version: 0.2`  
**Impact:** Minor but signals incomplete P0 work  
**Action:** Fix or document as intentional

### Finding 2: Atomic Claim Race Reopened
**Claim:** `collab_task.py` releases lock before calling `append_event`  
**Verification:** Confirmed. Lines 479-482 show `release_lock()` then `append_event()`  
**Impact:** P0 rule violated, race condition possible  
**Action:** Fix within readiness gate

### Finding 3: Task Lifecycle Not Reconstructed
**Claim:** Claim check doesn't reconstruct latest state from events  
**Verification:** Confirmed. Lines 470-476 check event types directly, no lifecycle rebuild  
**Impact:** Completed tasks might be re-claimable  
**Action:** Fix or document limitation

### Finding 4: Event Status Mapping Incomplete
**Claim:** `independent_analysis_completed` maps to `in_progress`  
**Verification:** Confirmed by event 29 result. `collab_event.py` line 100: `status_map.get(event_type, "in_progress")`  
**Impact:** Chapter 15 workflow broken  
**Action:** Add status mappings for new event types

### Finding 5: Gemini Dry-Run Not Independent
**Claim:** `invoke-gemini-analysis.sh` checks CLI before dry-run  
**Verification:** Confirmed. Line 83: `if ! command -v gemini` before dry-run check  
**Impact:** Can't test workflow without Gemini installed  
**Action:** Move CLI check after dry-run branch

### Finding 6: Gemini API Unvalidated
**Claim:** Live API still returns 500 errors  
**Verification:** Confirmed from prior session artifacts  
**Impact:** 3-agent pilot not fully testable  
**Action:** Treat as optional in pilot

### Finding 7: P1 Priority Drift
**Claim:** Different consensus docs define different P1 items  
**Verification:** Confirmed. Multiple P1 definitions across artifacts  
**Impact:** Unclear what "P1" means  
**Action:** Resolve through execution evidence

**Verdict:** All 7 findings are valid. P0 is not actually complete.

---

## Synthesis Decision

**Adopt Codex's recommendation** with these refinements:

### Phase 1: Readiness Gate (60-90min hard timebox)

**Must fix:**
1. Protocol version → 0.3 or document as 0.2
2. `collab_task.py` atomic claim (don't release lock before append)
3. Event status mappings for `independent_analysis_completed`, `waiting_synthesis`
4. Gemini dry-run independence (check CLI after dry-run branch)

**Must validate:**
- Run `validate-journal.sh` before and after fixes
- Verify event 29 status issue is resolved

### Phase 2: Minimal Invariant Tests (30-45min)

**Test scope (not full harness):**
1. Sequential event append consistency
2. Atomic claim simulation (barrier-based, from earlier consensus)
3. Independent analysis event produces correct status
4. Gemini dry-run creates artifact without CLI

**Stop rule:** If tests fail, create repair task, don't proceed to pilot

### Phase 3: Week 3 Day 0 Canary Pilot (1-2 hours)

**Pilot task:** Week 3 Day 0 preparation (from consensus)
- Environment strategy decision
- Seed data requirements
- Acceptance checklist creation

**Validation checkpoints:**
- Before pilot: `validate-journal.sh`
- After each handoff: `validate-journal.sh`
- After completion: `validate-journal.sh`

**Gemini:** Optional/read-only. If API fails, record and continue.

### Phase 4: Evidence-Based Documentation (30-45min)

**Document only:**
- Operator checklist (what was validated)
- Failure modes found (what broke)
- State transitions used (what worked)
- Open risks (what's still unknown)

**Defer:**
- Comprehensive protocol guide
- PROJECT-SUMMARY updates
- Broad architectural docs

---

## Why Codex's Approach Is Better

Claude's instinct (avoid premature documentation) was correct but incomplete. Codex adds:

1. **Mechanical validation before trust** - Don't assume P0 works
2. **Instrumented pilot** - Validation checkpoints, not blind execution
3. **Evidence-based docs** - Write after proof, not before
4. **Hard timeboxes** - Prevent protocol work from consuming product schedule

The key insight: **A pilot without readiness gate will produce confusing evidence, not clean evidence.**

---

## Consensus Recommendation

**Next task:** TASK-20260530-06: Collaboration Readiness Gate + Week 3 Day 0 Canary Pilot

**Scope:**
1. Readiness gate (60-90min): Fix 4 P0 gaps, validate
2. Minimal tests (30-45min): 4 invariant tests
3. Canary pilot (1-2h): Week 3 Day 0 prep with validation checkpoints
4. Evidence docs (30-45min): Operator checklist + findings

**Total time:** 3-4.5 hours

**Success criteria:**
- Readiness gate: All fixes applied, validation passes
- Tests: All 4 invariants pass
- Pilot: Week 3 Day 0 artifacts created, validation passes at all checkpoints
- Docs: Operator checklist exists, reflects actual execution

**Failure criteria:**
- Readiness gate exceeds 90min → stop, reassess P0 scope
- Tests fail → create repair task, don't pilot
- Pilot validation fails → stop, repair journal, document failure mode
- Week 3 Day 0 discovers architecture blocker → follow Week 3 consensus decision gate

---

## Open Questions Resolved

**Q: Should we document first?**  
A: No. Document after pilot proves behavior.

**Q: Should we test first?**  
A: Yes, but only invariants, not full harness.

**Q: Should we pilot first?**  
A: Yes, but after readiness gate, not blindly.

**Q: What about P1 items?**  
A: Resolve priority drift through execution evidence, not more planning.

---

## Next Actions

1. **Immediate:** Create TASK-20260530-06 with detailed scope
2. **Phase 1:** Execute readiness gate (Claude + Codex collaboration)
3. **Phase 2:** Run minimal tests (Codex leads)
4. **Phase 3:** Execute canary pilot (Claude + Codex collaboration)
5. **Phase 4:** Write evidence-based docs (Claude leads)

---

## Artifacts Referenced

- Claude position: `.omc/collaboration/tasks/TASK-20260530-05-next-steps-critical-discussion.md` (lines 29-43)
- Codex analysis: `.omc/collaboration/artifacts/20260530-1733-codex-next-steps-analysis.md`
- This synthesis: `.omc/collaboration/artifacts/20260530-0937-claude-synthesis-next-steps.md`

---

**Consensus Status:** Reached  
**Recommended by:** Codex (primary), Claude (endorses with refinements)  
**Ready for execution:** Yes
