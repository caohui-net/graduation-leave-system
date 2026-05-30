---
task_id: TASK-20260530-02
owner: claude
assignee: codex
status: open
created_at: 2026-05-30T08:15:00.000Z
updated_at: 2026-05-30T08:15:00.000Z
priority: high
---

# Task: Implement P0 Protocol Amendments

**Task ID:** TASK-20260530-02  
**Owner:** Claude  
**Assignee:** Codex  
**Created:** 2026-05-30T08:15:00Z  
**Status:** open

## Objective

Update `.omc/collaboration/protocol.md` with all 7 P0 amendments agreed in consensus document.

## Context

Consensus reached in TASK-20260530-01. All P0 items must be implemented before production testing.

Consensus document: `.omc/collaboration/artifacts/20260530-0814-protocol-review-consensus.md`

## Scope

Implement the following 7 P0 amendments to protocol.md:

### 1. events.jsonl Authoritative (Section 5)

Update event log section to specify:
- events.jsonl is source of truth
- state.json is rebuildable cache
- If state invalid but events valid, rebuild from log

### 2. Required Journal Lock (Section 8)

Add new subsection "Required Journal Lock":
- `mkdir .omc/collaboration/locks/journal.lock` for atomic acquisition
- Lock directory contains `owner.json` with agent, task_id, timestamps
- Must hold lock for all events.jsonl + state.json writes
- Release after validation

### 3. Event ID Allocation (Section 5)

Replace event ID rules:
- Compute next_id from max(events.jsonl), NOT state.json
- Allocation while holding journal.lock
- After append, state.last_event_id must equal max event id

### 4. needs_repair Behavior (New Section)

Add "Failure Recovery" section:
- Duplicate IDs → needs_repair status
- Malformed JSONL → preserve log, create repair artifact
- Stop normal collaboration until repair complete

### 5. Atomic Task Claim (Section 6)

Add claim procedure to tasks section:
- Acquire journal.lock before claim
- Reconstruct task lifecycle from events.jsonl
- Check for active owner (claimed/in_progress/waiting/blocked/timeout_candidate)
- If active owner exists, abort claim
- If open/recovered, append task_claimed

### 6. Atomic state.json Writes (Section 4)

Add to shared state section:
- Write to `.omc/collaboration/state.json.tmp.<agent>`
- Validate JSON
- Atomic rename with `mv`

### 7. Filesystem Requirements (Section 2 or new)

Add filesystem requirements:
- Collaboration directory needs atomic mkdir semantics
- Local filesystems and NFSv4 acceptable
- NFSv2/NFSv3 and weak cache unsupported

## Expected Output

Updated `protocol.md` with:
- All 7 P0 amendments integrated
- Clear, implementation-ready language
- Consistent with existing protocol structure
- Version bumped to 0.2

## Constraints

- Preserve existing protocol structure where possible
- Use amendment text from Codex's review artifact (20260530-0805-codex-protocol-critical-review.md)
- Keep language clear and mandatory (MUST/SHOULD/MAY)
- Do not add P1 items yet (state machine, timeout, YAML)

## Acceptance Criteria

- [ ] All 7 P0 items present in protocol.md
- [ ] Protocol version updated to 0.2
- [ ] Protocol remains valid Markdown
- [ ] No P1/P2 items added prematurely
- [ ] Amendment text matches consensus

## Verification

After implementation:
1. Read updated protocol.md
2. Verify all 7 P0 items present
3. Check for consistency and clarity
4. Confirm no unintended changes
