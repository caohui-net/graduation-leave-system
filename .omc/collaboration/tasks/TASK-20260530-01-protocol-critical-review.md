# Task: Protocol Critical Review

**Task ID:** TASK-20260530-01  
**Owner:** Claude  
**Created:** 2026-05-30T08:03:29Z  
**Status:** open

## Objective

Critically review `.omc/collaboration/protocol.md` to identify design weaknesses, edge cases, and optimization opportunities before production testing.

## Scope

Review the following aspects of the protocol:

1. **Concurrency Control**
   - Lock mechanism is advisory only - no enforcement
   - What prevents two agents from ignoring locks?
   - What happens if lock file is stale (agent crashed)?

2. **Event ID Management**
   - Manual increment by reading `last_event_id` from state.json
   - Race condition: both agents read same ID, both write ID+1
   - How to detect and recover from duplicate event IDs?

3. **Task Format**
   - Protocol specifies `.md` files for tasks
   - Is markdown optimal for machine parsing?
   - Should tasks use structured JSON with markdown description field?

4. **Failure Recovery**
   - Agent crashes mid-task - how to detect?
   - Partial writes to state.json or events.jsonl - how to repair?
   - Timeout mechanism missing - task stuck forever?

5. **State Machine Logic**
   - Status transitions not fully defined
   - Valid transitions: initialized → ? → ? → completed
   - What status for: waiting, blocked, error, timeout?

6. **Testing Strategy**
   - No test cases defined
   - Need concrete scenarios: ping-pong, concurrent writes, failure injection
   - How to verify protocol works before production use?

## Expected Output

Codex should provide:

1. **Critical Analysis** - identify real problems vs theoretical concerns
2. **Proposed Solutions** - concrete fixes for identified issues
3. **Protocol Amendments** - specific changes to protocol.md
4. **Test Plan** - 3-5 test scenarios to validate the protocol

## Constraints

- Must maintain backward compatibility with existing state.json and events.jsonl
- Solutions must work within OMC framework limitations (no cross-provider hooks)
- Keep protocol simple - avoid over-engineering

## Acceptance Criteria

- [ ] All 6 review aspects addressed
- [ ] Concrete solutions proposed (not just "needs improvement")
- [ ] Test plan includes failure scenarios
- [ ] Protocol amendments are implementation-ready
