# Protocol Critical Review - Codex Response

**Task ID:** TASK-20260530-01
**Reviewer:** Codex
**Reviewed file:** `.omc/collaboration/protocol.md`
**Review time:** 2026-05-30T08:05:20.000Z

## Executive Assessment

The protocol is a workable MVP for low-frequency Claude-Codex handoff, but it currently relies on social compliance for the files with the highest contention: `events.jsonl` and `state.json`. That is acceptable for a first manual test only if both agents act sequentially. It is not safe enough for production-like collaboration, because the exact failures listed in the task can corrupt the event stream or leave the workflow permanently stuck.

The most important design correction is to make `events.jsonl` the source of truth and treat `state.json` as a rebuildable cache. The second correction is to define one serialized write path for shared files using atomic filesystem operations. These two changes solve most concurrency, recovery, and duplicate-id issues without adding a service, daemon, database, or cross-provider hook.

## 1. Concurrency Control

### Finding

This is a real issue, not just theoretical. The protocol says locks are advisory and says to use a lock when two agents might modify the same file, but it does not define an atomic acquisition operation, required write ordering, timeout, or validation step. If two agents append events and update state at the same time, `state.json` can point to the wrong event id, event ids can duplicate, and a later agent may silently build on corrupted state.

The question "what prevents two agents from ignoring locks?" has two answers:

- Technically, nothing, if locks remain advisory text files.
- Operationally, the protocol can still make ignoring locks a protocol violation and require every shared write to use an atomic lock acquisition sequence.

Because OMC has no cross-provider enforcement hook, the best realistic control is filesystem atomicity plus post-write validation.

### Recommended Solution

Define a single shared write lock for `events.jsonl` + `state.json`: `.omc/collaboration/locks/journal.lock`. Acquire it atomically before any write that changes either file.

Use one of these portable-enough atomic patterns:

- Preferred: `mkdir .omc/collaboration/locks/journal.lock`
- Alternative: create a lock file with noclobber semantics, for example `set -C; > locks/journal.lock`

The protocol should ban check-then-create locking, because `if missing, then write lock` is race-prone.

The lock content should include owner, pid/session if available, task id, timestamp, and heartbeat timestamp. If stale, the recovering agent must write a `lock_recovered` event after acquiring the lock, not before.

### Protocol Amendment

Add this to section 8:

```markdown
### Required Journal Lock

Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.

Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:

```bash
mkdir .omc/collaboration/locks/journal.lock
```

The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.

The lock directory MUST contain `owner.json`:

```json
{
  "agent": "codex",
  "task_id": "TASK-20260530-01",
  "created_at": "2026-05-30T08:00:00.000Z",
  "heartbeat_at": "2026-05-30T08:00:00.000Z",
  "reason": "append event and update state"
}
```

The lock owner MUST remove the lock after validating the write. If the lock is older than 15 minutes and `heartbeat_at` has not changed, another agent may recover it by moving the directory to `locks/stale/journal.lock.<timestamp>` after user-visible notice or explicit task-artifact documentation. The recovering agent MUST append a `lock_recovered` event after acquiring a new journal lock.
```

## 2. Event ID Management

### Finding

This is a real issue. Reading `state.json.last_event_id`, adding one, and appending is unsafe under concurrency. It also makes the cache authoritative over the log, which is backwards: the append-only log should be authoritative.

Duplicate numeric ids are especially harmful because downstream state reconstruction becomes ambiguous. However, preserving numeric ids is reasonable for backward compatibility.

### Recommended Solution

Keep numeric `id`, but allocate it only while holding the journal lock. Compute the next id from `events.jsonl`, not `state.json`:

1. Acquire journal lock.
2. Validate every existing JSONL line parses.
3. Compute `next_id = max(event.id) + 1`.
4. Append exactly one complete JSON object line.
5. Atomically rewrite `state.json` as a snapshot of the resulting workflow state.
6. Validate log and state.
7. Release lock.

Recovery rule:

- If `state.json.last_event_id` differs from max event id, repair `state.json` from the log.
- If duplicate ids exist, do not renumber historical events by default. Append an `event_log_repair` event with details and mark `state.status = "needs_repair"` unless the user explicitly approves log surgery.

Optional future improvement: add a stable `event_uid` such as timestamp-agent-random suffix. Keep numeric `id` for human ordering, use `event_uid` for uniqueness.

### Protocol Amendment

Replace event id rules in section 5 with:

```markdown
Event id rules:

- `events.jsonl` is the source of truth for event ordering.
- Numeric `id` starts at `1` and should normally increment by `1`.
- New event ids MUST be allocated while holding `locks/journal.lock`.
- The next id MUST be computed from the maximum valid `id` in `events.jsonl`, not from `state.json`.
- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
- If duplicate ids or malformed lines are detected, the agent MUST stop normal processing, preserve the original log, write a repair artifact, and set state status to `needs_repair`.
```

## 3. Task Format

### Finding

This is partly real and partly theoretical.

Markdown is good for human-readable task handoff and review context. It is not ideal as the only machine-readable task record if agents need reliable filtering by owner, status, task id, priority, dependencies, and acceptance criteria. But switching entirely to JSON would make task authoring worse and would not solve the larger concurrency problems.

### Recommended Solution

Use a hybrid format:

- Keep `.md` task documents as the canonical human artifact.
- Require a YAML front matter block for machine-readable metadata.
- Optionally add `tasks/index.json` later if queries become frequent.

This is simpler than parallel `.json` task files and more maintainable than parsing arbitrary Markdown headings.

Example:

```markdown
---
task_id: TASK-20260530-01
owner: claude
assignee: codex
status: open
created_at: 2026-05-30T08:03:29Z
updated_at: 2026-05-30T08:03:29Z
priority: high
---

# Task: Protocol Critical Review
```

### Protocol Amendment

Add to section 6:

```markdown
Task files remain Markdown for human review, but new task files SHOULD include YAML front matter with these fields: `task_id`, `owner`, `assignee`, `status`, `created_at`, `updated_at`, and `priority`. Agents MUST treat the front matter as the machine-readable task summary and the Markdown body as the durable human-readable specification.

Valid task statuses are: `open`, `claimed`, `in_progress`, `waiting`, `blocked`, `completed`, `cancelled`, `needs_repair`.
```

## 4. Failure Recovery

### Finding

This is a real production-readiness gap. The current protocol has no heartbeat, lease, partial-write handling, or recovery mode. A crashed agent can leave a lock forever, leave `state.json` malformed, or append a truncated event line.

The risk differs by file:

- `events.jsonl`: append failures can create a malformed final line.
- `state.json`: rewrite failures can make the whole snapshot invalid.
- task/artifact Markdown: usually recoverable manually, lower severity.

### Recommended Solution

Define `events.jsonl` as append-only and mostly immutable; define `state.json` as disposable cache that can be rebuilt from the event log. Require atomic state writes:

1. Write `.omc/collaboration/state.json.tmp.<agent>`.
2. Validate JSON.
3. Rename into place with atomic `mv`.

For event append, require post-append validation. If a final JSONL line is malformed:

- Do not rewrite immediately during normal operation.
- Move into recovery mode.
- Create `.omc/collaboration/artifacts/<timestamp>-event-log-repair.md`.
- If the malformed content is only the final line and clearly incomplete, a repair operation may move the original file to `events.jsonl.bak.<timestamp>` and rewrite a valid log, but only under journal lock and with a repair event.

Add heartbeat and lease:

- A claimed/in-progress task should update heartbeat via state or event every 10 minutes during long work.
- If no heartbeat for 30 minutes, status becomes `timeout_candidate`, not immediately failed.
- Another agent or user may recover by appending `task_recovered` and setting the task to `open` or `blocked`.

### Protocol Amendment

Add a failure recovery section:

```markdown
## Failure Recovery

`events.jsonl` is authoritative. `state.json` is a rebuildable snapshot.

Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions. If `state.json` is invalid but `events.jsonl` is valid, rebuild `state.json` from the latest valid event and append a `state_rebuilt` event.

Agents MUST update `state.json` by writing a temporary JSON file, validating it, then atomically renaming it into place.

If `events.jsonl` contains a malformed line or duplicate event id, normal collaboration MUST stop and `state.status` MUST be set to `needs_repair` if state can be written safely. A repair artifact MUST describe the malformed line, duplicate ids, proposed repair, and whether historical log rewriting is required.

For long-running tasks, the active agent SHOULD emit a `heartbeat` event at least every 10 minutes. If an active task has no heartbeat or event for 30 minutes, another agent may mark it `timeout_candidate`. Recovery requires a `task_recovered`, `blocked`, or `cancelled` event.
```

## 5. State Machine Logic

### Finding

This is a real gap for repeatable collaboration. The protocol lists statuses but does not define valid transitions or ownership semantics. That makes it unclear whether `active_agent = claude` and `status = completed` is valid, how handoff differs from waiting, or whether blocked tasks are owned by anyone.

### Recommended Solution

Define a small state machine. Keep it simple and workflow-level, not a full project tracker.

Recommended statuses:

- `initialized`: collaboration files exist, no readiness confirmed.
- `ready`: both sides or required side is ready.
- `task_open`: a task exists and is unclaimed.
- `claimed`: an agent has claimed but not started substantive work.
- `in_progress`: active agent is working.
- `waiting`: active work is paused waiting for the other agent or user.
- `blocked`: cannot proceed without external input or fix.
- `timeout_candidate`: active ownership may be stale.
- `needs_repair`: collaboration files are inconsistent or corrupted.
- `completed`: task/workflow completed.
- `cancelled`: task intentionally abandoned.

Minimum transition table:

```text
initialized -> ready
ready -> task_open
task_open -> claimed
claimed -> in_progress
in_progress -> waiting | blocked | completed | timeout_candidate
waiting -> claimed | in_progress | blocked | cancelled
blocked -> task_open | claimed | cancelled
timeout_candidate -> task_open | claimed | blocked | needs_repair
needs_repair -> task_open | blocked | cancelled
completed -> task_open
```

Ownership rules:

- `task_open`, `ready`, `completed`, `cancelled`: `active_agent` should be `none`.
- `claimed`, `in_progress`, `waiting`, `blocked`, `timeout_candidate`: `active_agent` should be the owning or last owning agent.
- `needs_repair`: `active_agent` should be the agent attempting repair, or `none` if awaiting user decision.

### Protocol Amendment

Add to section 4:

```markdown
Workflow state MUST follow the transition table in this protocol. Agents SHOULD NOT skip from `task_open` to `completed`; they should emit at least `task_claimed` and `completed` events. If a higher-priority direct user instruction requires a shortcut, the agent must record the reason in the event details.
```

## 6. Testing Strategy

### Finding

This is a real gap. The protocol is itself a coordination mechanism; it needs tests before relying on it for valuable project work. The tests do not need a full automation framework at first, but they should be scripted enough to repeat.

### Recommended Test Plan

#### Test 1: Sequential Ping-Pong Handoff

Goal: verify happy-path task creation, claim, artifact, handoff, completion.

Steps:

1. Claude creates a test task.
2. Codex claims it, writes a small artifact, appends events, updates state.
3. Claude resumes and completes it.

Expected result:

- Event ids are contiguous.
- `state.json.last_event_id` equals max event id.
- Task and artifact paths referenced by events exist.
- Final status is `completed`.

#### Test 2: Concurrent Event Append Race

Goal: verify journal lock prevents duplicate event ids.

Fault injection:

1. Start two shell processes or two agent turns attempting to append an event at the same time.
2. Force both to sleep after reading max id but before append in an unsafe branch; then repeat with journal lock enabled.

Expected result:

- Unsafe branch demonstrates duplicate ids or failed validation.
- Locked branch serializes writes; ids remain unique and contiguous.
- Losing writer waits, retries, or exits cleanly.

#### Test 3: Stale Lock Recovery

Goal: verify crashed-agent lock recovery.

Fault injection:

1. Manually create `locks/journal.lock/owner.json` with old `created_at` and `heartbeat_at`.
2. Attempt normal write.
3. Recover stale lock according to protocol.

Expected result:

- Agent refuses to ignore fresh lock.
- Agent may recover stale lock only after documenting recovery.
- `lock_recovered` event is appended after new lock is acquired.

#### Test 4: Partial Write Repair

Goal: verify invalid JSON handling.

Fault injection:

1. Append an incomplete final line to a copy of `events.jsonl`.
2. Corrupt a copy of `state.json`.
3. Run validation/recovery process.

Expected result:

- Invalid state is rebuilt from valid events.
- Invalid event log triggers `needs_repair`, not silent continuation.
- Repair artifact records original file backup and exact repair action.

#### Test 5: Timeout And Reclaim

Goal: verify stuck tasks do not remain owned forever.

Fault injection:

1. Set `state.status = "in_progress"` and `active_agent = "codex"`.
2. Ensure no heartbeat/event exists for more than timeout threshold.
3. Have Claude or Codex mark `timeout_candidate`, then recover task.

Expected result:

- Recovery path is explicit through `timeout_candidate`.
- Reclaim writes `task_recovered` or `task_claimed` event.
- No agent silently overwrites another active agent's task.

## Prioritized Changes

P0 changes before production testing:

1. Make `events.jsonl` authoritative and `state.json` rebuildable.
2. Require atomic `journal.lock` for all event/state writes.
3. Allocate event ids from max log id while holding the lock.
4. Define `needs_repair` behavior for malformed log or duplicate ids.

P1 changes before multi-agent daily use:

1. Add task YAML front matter.
2. Add state transition table and ownership rules.
3. Add heartbeat and timeout recovery.
4. Add atomic temp-file write rule for `state.json`.

P2 optional improvements:

1. Add globally unique `event_uid`.
2. Add `tasks/index.json` if task search becomes common.
3. Add a small validator script for events/state/tasks.

## Bottom Line

The protocol should not move to production testing until journal locking, log-authoritative event allocation, and recovery mode are specified. These are small amendments, but they change the protocol from "cooperative notes" into a minimally reliable coordination mechanism. Markdown task files can remain, provided machine-readable front matter is added.
