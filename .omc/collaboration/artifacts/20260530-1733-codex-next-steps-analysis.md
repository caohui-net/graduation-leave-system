# Codex Next Steps Analysis

**Task:** TASK-20260530-05  
**Agent:** Codex  
**Date:** 2026-05-30  
**Status:** Independent analysis completed  

## Independence Note

Independent analysis - did not read Claude's same-task analysis artifact before forming conclusions.

Process note: I first read the collaboration protocol, current state/events, the task sections outside "Claude's Initial Position", and the implemented P0 files. After forming my view, I read Claude's initial position and the referenced consensus documents for challenge/comparison. A heading search exposed the one-line proposal "skip P1 documentation, go straight to production pilot" before the comparison phase; I did not read its rationale until after forming my initial view.

## Executive View

The most valuable next step is **not** the consensus P1 order of documentation -> testing -> pilot, and it is also **not** an unguarded jump straight to production pilot.

Recommended next step:

**Run a short executable readiness gate, then use Week 3 Day 0 as a controlled pilot.**

Concretely:

1. Spend a hard timebox, ideally 60-90 minutes, fixing or explicitly waiving P0 implementation/protocol drift that can corrupt collaboration state.
2. Add/run a minimal executable test set for the collaboration protocol invariants.
3. Immediately pilot the protocol on the real Week 3 Day 0 preparation task, with validation before and after every collaboration state mutation.
4. Convert findings into documentation after the pilot, keeping only a thin operator checklist before the pilot.

This is a different framing from all three simple choices. The right next step is an **instrumented canary pilot**, preceded by a small mechanical gate.

## Why The Current P1 Order Is Weak

The docs -> tests -> pilot sequence assumes the protocol is conceptually settled and only needs explanation. Current evidence says otherwise.

Observed issues:

- `.omc/collaboration/protocol.md` still says `Version: 0.2`, while the task context says protocol v0.3 is complete. This is a small but real drift signal.
- The protocol requires atomic task claim under one `journal.lock`, but `.claude/skills/claude-codex-collab/scripts/collab_task.py` releases the lock after checking and then calls `append_event`, which reacquires it. That reopens the race the P0 rule was meant to close.
- `collab_task.py` does not reconstruct the latest task lifecycle. It checks historical `task_claimed` / `in_progress` events directly, so a later `completed` event does not cleanly affect the earlier claim event. This conflicts with the protocol's "latest effective lifecycle state" intent.
- `collab_event.py` maps unknown event types to `in_progress`. Therefore `independent_analysis_completed` will not naturally produce `waiting_synthesis`, even though chapter 15 defines that workflow.
- `invoke-gemini-analysis.sh` checks `command -v gemini` before `--dry-run`, so dry-run is not actually independent of local Gemini installation.
- Gemini live validation remains unresolved because prior runs reported API 500 failures. A 3-agent pilot is therefore not yet fully testable.
- The earlier consensus documents themselves diverge on what P1 means: one says state machine / stale ownership / YAML; another says next-action / checkpoints / health checks / config policy; this task summarizes P1 as docs -> tests -> pilot. That priority drift should be resolved by execution evidence, not more prose.

These are not reasons to stop. They are reasons to avoid writing a polished guide for behavior that the implementation does not yet enforce.

## Evaluation Of Options

### Option A: Documentation First

Benefits:

- Reduces ambiguity for future agents.
- Could clarify state transitions, stale ownership, and synthesis ownership.
- Low implementation risk.

Risks:

- High chance of documenting aspirational behavior instead of executable behavior.
- Does not expose atomicity defects, race conditions, or state/event drift.
- Can create false confidence because the protocol text is already ahead of some scripts.

Verdict: Useful, but not first. Limit pre-pilot documentation to a one-page checklist: validate before/after, allowed statuses, and recovery trigger.

### Option B: Validation Testing First

Benefits:

- Directly targets the safety properties that matter: event id uniqueness, lock behavior, atomic claim, state consistency, malformed log handling.
- Catches failures a real sequential pilot may never reveal.
- Produces durable evidence for whether P0 is actually done.

Risks:

- Synthetic tests can overfit implementation assumptions.
- Full test harness can become a project inside the project.
- May delay the real graduation-leave-system work if allowed to expand.

Verdict: Best first move if tightly scoped. Do not build a broad framework; write only invariant tests that protect collaboration state.

### Option C: Direct Production Pilot

Benefits:

- Fastest way to learn operator friction and real workflow gaps.
- Aligns with the Week 3 consensus: establish reproducible evidence for the graduation leave system, starting Day 0.
- Avoids spending a day polishing collaboration tooling before the product task resumes.

Risks:

- A normal pilot may not exercise concurrency, stale locks, malformed logs, or claim races.
- If the pilot mutates shared state through partially compliant scripts, it can create confusing history rather than evidence.
- If Gemini is included, API instability can dominate the outcome.

Verdict: Good after a readiness gate. Bad as the immediate next action without mechanical checks.

### Option D: New Approach - Executable Readiness Gate + Canary Pilot

Benefits:

- Preserves momentum toward the real Week 3 task.
- Forces protocol claims to match scripts before relying on them.
- Uses tests for invariants and pilot for usability, instead of asking one activity to do both.
- Keeps documentation evidence-based.

Risks:

- Requires discipline on the timebox.
- May reveal P0 is not actually complete, which can feel like scope regression.
- Needs a clear stop rule so protocol work does not consume the product schedule.

Verdict: Strongest path.

## Assumptions To Challenge

1. **"P0 implementation complete" may be too optimistic.** The protocol text is mostly present, but executable paths still have gaps.

2. **"Documentation before pilot prevents confusion" is only partly true.** If docs describe desired behavior while scripts do something else, docs increase confusion.

3. **"Real tasks expose actual problems faster than tests" is true only for workflow UX.** Real tasks are poor at exposing race conditions, partial writes, stale ownership, and malformed-log recovery.

4. **"Validation tests are based on assumptions" is not a decisive objection.** The protocol has explicit invariants. Tests for those invariants are not speculative.

5. **"Pilot" should not mean "production testing of the collaboration protocol under full trust."** It should mean a canary run with pre/post validation and rollback/repair criteria.

6. **"Gemini integration is P0 complete" is conditional.** Dry-run exists, but live API reliability remains unproven. The pilot should not depend on Gemini success unless the goal is specifically to test Gemini failure handling.

7. **The collaboration protocol is a means, not the product goal.** The next step should serve the graduation leave system Week 3 plan, not create a parallel tooling project.

## Recommended Next Task

Create a task named approximately:

**TASK: Collaboration readiness gate + Week 3 Day 0 canary pilot**

Scope:

1. **Mechanical gate, hard timebox 60-90 minutes**
   - Fix protocol version/status drift or document it as intentionally v0.2.
   - Make `collab_task.py claim` perform check and append within one lock, or stop using it for claims until fixed.
   - Add event status handling for `independent_analysis_completed` and `waiting_synthesis`.
   - Allow `invoke-gemini-analysis.sh --dry-run` without requiring Gemini CLI.
   - Run `.omc/collaboration/scripts/validate-journal.sh` before and after changes.

2. **Minimal validation**
   - Sequential event append/state consistency.
   - Atomic claim race or at least deterministic two-process claim simulation.
   - Independent-analysis completion event produces the expected next workflow state or an explicitly documented state.
   - Gemini dry-run artifact creation and event logging.

3. **Controlled pilot**
   - Use the protocol for Week 3 Day 0 preparation from `docs/discussions/week3-direction-2026-05-30/06-consensus.md`.
   - Artifacts expected: environment strategy, seed data requirements, acceptance checklist, issue log.
   - Run journal validation before the pilot, after each handoff/completion, and at the end.
   - Treat Gemini as optional/read-only; if API still fails, record failure artifact and continue without blocking Day 0.

4. **Post-pilot documentation**
   - Write only what was proven: operator checklist, failure modes found, state transitions actually used, and open risks.
   - Defer broad guide/PROJECT-SUMMARY updates until after the pilot has produced real evidence.

## Stop Rules

- If validation fails before pilot and cannot be fixed within the readiness timebox, do not run a collaboration pilot. Create a repair/hardening task.
- If the Week 3 Day 0 pilot discovers architecture-level product blockers, follow the Week 3 consensus decision gate and pause extension work.
- If Gemini API fails, do not block the two-agent pilot. Record it as a tool availability issue.
- If collaboration state becomes inconsistent, stop product work and repair the journal first.

## Final Recommendation

Adopt this order:

**readiness gate -> minimal invariant tests -> Week 3 Day 0 canary pilot -> evidence-based docs**

This keeps the useful part of Claude's likely instinct, which is to avoid over-documenting before real use, but rejects the unsafe part: skipping mechanical validation. It also keeps the useful part of the earlier consensus, which is validation before production pilot, but compresses documentation until after evidence exists.
