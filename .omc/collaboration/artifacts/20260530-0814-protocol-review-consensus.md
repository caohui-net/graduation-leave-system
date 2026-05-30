# Protocol Review Consensus - Claude & Codex

**Task ID:** TASK-20260530-01  
**Consensus Date:** 2026-05-30  
**Participants:** Claude + Codex  
**Rounds:** 2 (Initial review + Response discussion)

## Status

**CONSENSUS REACHED** on protocol amendments and implementation priorities.

## Agreed P0 Changes (Block Production Testing)

The following 7 items MUST be implemented before any production testing:

1. **events.jsonl authoritative, state.json rebuildable**
   - events.jsonl is the source of truth for all workflow state
   - state.json is a disposable cache that can be rebuilt from events.jsonl
   - If state.json is invalid but events.jsonl is valid, rebuild state from log

2. **Required atomic journal.lock for all event/state writes**
   - Use `mkdir .omc/collaboration/locks/journal.lock` for atomic acquisition
   - Lock directory must contain `owner.json` with agent, task_id, timestamps
   - Lock must be held for all operations that modify events.jsonl or state.json
   - Lock must be released after write validation

3. **Event IDs allocated from max log ID while holding lock**
   - Compute `next_id = max(event.id) + 1` from events.jsonl, NOT from state.json
   - Allocation must happen while holding journal.lock
   - After append, `state.json.last_event_id` must equal max event id in log

4. **needs_repair behavior for malformed log or duplicate IDs**
   - If duplicate event IDs detected, set `state.status = "needs_repair"`
   - If malformed JSONL line detected, preserve original log and create repair artifact
   - Do not continue normal collaboration until repair is complete

5. **Atomic task claim under journal lock**
   - Before claiming task, acquire journal.lock
   - Reconstruct current task lifecycle state from events.jsonl
   - Check if task has active owner (claimed, in_progress, waiting, blocked, timeout_candidate)
   - If task has active owner, abort claim and release lock
   - If task is open/recovered, append task_claimed event
   - This prevents two agents from claiming the same task simultaneously

6. **Atomic state.json writes via temp file + rename**
   - Write to `.omc/collaboration/state.json.tmp.<agent>`
   - Validate JSON is well-formed
   - Atomically rename into place with `mv`
   - This prevents partial writes from corrupting state.json

7. **Filesystem requirement documentation**
   - Document that collaboration directory MUST be on filesystem with atomic mkdir
   - Local filesystems and NFSv4 are acceptable
   - NFSv2/NFSv3 and weak cache consistency mounts are unsupported
   - Production testing should not proceed on unsupported filesystems

## Agreed P1 Changes (Before Daily Use)

The following 3 items should be added after P0 validation:

1. **State transition table and ownership rules**
   - Define valid state transitions
   - Clarify `completed -> ready -> task_open` (not direct completed->task_open)
   - Add explicit `reopened` status if reopening completed tasks is needed
   - Document ownership rules for each status

2. **Simplified stale ownership detection**
   - NO periodic heartbeat events (reduces event log noise)
   - 60-minute manual threshold for stale task ownership
   - Before claiming, check latest task event timestamp
   - If no events for 60 minutes, may recover via explicit event (task_recovered, blocked, cancelled)
   - NO automatic timeout_candidate transition in MVP
   - Keep 15-minute threshold for stale journal locks (separate from task ownership)

3. **YAML front matter deferred**
   - Keep Markdown-only tasks for MVP
   - Add YAML front matter only when task querying/filtering is actually needed
   - Reduces parsing complexity for initial implementation

## Agreed P2 Items (Optional)

1. Globally unique `event_uid` (timestamp-agent-random suffix)
2. `tasks/index.json` for fast task queries
3. Validator script for events/state/tasks consistency

## Implementation Order

**Phase 1: P0 Protocol Amendments**
- Update protocol.md with all 7 P0 items
- Provide implementation-ready amendment text for each item

**Phase 2: Validation Testing**
- Test 1: Sequential ping-pong handoff (happy path)
- Test 3: Stale lock recovery
- Test 4: Partial write repair
- Test 2: Concurrent event append race (with barrier-based implementation)
- All tests must pass before proceeding

**Phase 3: P1 Protocol Cleanup**
- Add state transition table to protocol.md
- Document simplified stale ownership detection
- Note that YAML front matter is deferred

**Phase 4: Production Pilot**
- Use amended protocol for real collaboration task
- Monitor for issues
- Iterate based on findings

## Test 2 Implementation Details (Agreed)

Use barrier-based approach, not just rapid sequential writes:

1. Run against temp copy of `.omc/collaboration/`
2. Provide test writer with two modes: `unsafe` and `locked`
3. **Unsafe mode:**
   - Read `max(event.id)`
   - Write barrier marker file
   - Wait until both marker files exist
   - Append using stale `next_id`
4. **Locked mode:**
   - Acquire `locks/journal.lock` with `mkdir`
   - Read `max(event.id)`
   - Append event
   - Update state
   - Release lock
5. **Assertions:**
   - Unsafe mode creates duplicate IDs or validation failure
   - Locked mode creates unique contiguous IDs

## Key Decisions

**Task claim race condition:** Identified as P0 gap. Atomic read-check-write under lock is the solution.

**Heartbeat necessity:** Agreed as overdesigned for MVP. Simplified to 60-minute manual threshold without heartbeat events.

**NFS compatibility:** Must be documented. Local-only is acceptable for MVP if documented.

**completed->task_open:** Clarified as `completed -> ready -> task_open` for new tasks. Reopening requires explicit event.

**Atomic state.json writes:** Moved from P1 to P0 because state.json must not be left malformed even though it's rebuildable.

## Next Steps

1. **Immediate:** Update protocol.md with P0 amendments
2. **Next:** Implement validation tests
3. **Then:** Add P1 documentation
4. **Finally:** Production pilot

## Artifacts

- Initial review: `.omc/collaboration/artifacts/20260530-0805-codex-protocol-critical-review.md`
- Claude response: `.omc/collaboration/artifacts/20260530-0808-claude-response-to-codex-review.md`
- Codex second response: `.omc/collaboration/artifacts/20260530-1611-codex-second-response-to-claude.md`
- This consensus: `.omc/collaboration/artifacts/20260530-0814-protocol-review-consensus.md`
