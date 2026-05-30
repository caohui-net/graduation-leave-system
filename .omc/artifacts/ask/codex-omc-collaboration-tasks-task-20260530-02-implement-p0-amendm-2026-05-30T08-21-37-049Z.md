# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-05-30T08:21:37.050Z

## Original task

请执行新任务：.omc/collaboration/tasks/TASK-20260530-02-implement-p0-amendments.md

根据我们达成的共识（.omc/collaboration/artifacts/20260530-0814-protocol-review-consensus.md），需要将7个P0修订项集成到 protocol.md 中。

你在第一轮审查中已经提供了详细的修订文本（.omc/collaboration/artifacts/20260530-0805-codex-protocol-critical-review.md），现在请将这些修订应用到 protocol.md。

**关键要求：**
1. 更新 protocol.md 版本号为 0.2
2. 集成全部7个P0项（journal lock、event ID分配、atomic claim、needs_repair、atomic state writes、filesystem要求）
3. 保持现有协议结构
4. 使用清晰的强制性语言（MUST/SHOULD/MAY）
5. 不要添加P1项（state machine、timeout、YAML front matter）

完成后，按协议记录 task_claimed 和 completed 事件，并更新 state.json。

## Final prompt

请执行新任务：.omc/collaboration/tasks/TASK-20260530-02-implement-p0-amendments.md

根据我们达成的共识（.omc/collaboration/artifacts/20260530-0814-protocol-review-consensus.md），需要将7个P0修订项集成到 protocol.md 中。

你在第一轮审查中已经提供了详细的修订文本（.omc/collaboration/artifacts/20260530-0805-codex-protocol-critical-review.md），现在请将这些修订应用到 protocol.md。

**关键要求：**
1. 更新 protocol.md 版本号为 0.2
2. 集成全部7个P0项（journal lock、event ID分配、atomic claim、needs_repair、atomic state writes、filesystem要求）
3. 保持现有协议结构
4. 使用清晰的强制性语言（MUST/SHOULD/MAY）
5. 不要添加P1项（state machine、timeout、YAML front matter）

完成后，按协议记录 task_claimed 和 completed 事件，并更新 state.json。

## Raw output

```text
已完成任务。

更新内容：
- [protocol.md](/home/caohui/projects/graduation-leave-system/.omc/collaboration/protocol.md:3) 版本已升到 `0.2`
- 集成了 7 个 P0 项：`events.jsonl` authoritative、required `journal.lock`、事件 ID 从日志分配、`needs_repair`、atomic task claim、atomic `state.json` 写入、filesystem 要求
- 未加入 P1 项：没有 YAML front matter 要求、没有状态机表、没有 30/60 分钟任务超时规则

协作日志也已按协议更新：
- `events.jsonl` 追加了 `id=9 task_claimed`
- `events.jsonl` 追加了 `id=10 completed`
- [state.json](/home/caohui/projects/graduation-leave-system/.omc/collaboration/state.json:1) 已更新为 `status: completed`，`last_event_id: 10`，`active_agent: none`

验证通过：协议 7 个 P0 检查全为 true，事件日志 JSONL 可解析、无重复 ID，`state.json.last_event_id` 与最大事件 ID 一致，锁目录已清空。


OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019e77f5-78ee-7c03-8b70-5c623ad5dc57
--------
user
请执行新任务：.omc/collaboration/tasks/TASK-20260530-02-implement-p0-amendments.md

根据我们达成的共识（.omc/collaboration/artifacts/20260530-0814-protocol-review-consensus.md），需要将7个P0修订项集成到 protocol.md 中。

你在第一轮审查中已经提供了详细的修订文本（.omc/collaboration/artifacts/20260530-0805-codex-protocol-critical-review.md），现在请将这些修订应用到 protocol.md。

**关键要求：**
1. 更新 protocol.md 版本号为 0.2
2. 集成全部7个P0项（journal lock、event ID分配、atomic claim、needs_repair、atomic state writes、filesystem要求）
3. 保持现有协议结构
4. 使用清晰的强制性语言（MUST/SHOULD/MAY）
5. 不要添加P1项（state machine、timeout、YAML front matter）

完成后，按协议记录 task_claimed 和 completed 事件，并更新 state.json。
codex
我会先读取项目级执行规则、协作协议和任务/共识文档，确认事件记录与状态更新的格式后再改 `protocol.md`。
exec
/bin/bash -lc "pwd && sed -n '1,220p' /home/caohui/.codex/RTK.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
/home/caohui/projects/graduation-leave-system
# RTK - Rust Token Killer (Codex CLI)

**Usage**: Token-optimized CLI proxy for shell commands.

## Rule

Always prefix shell commands with `rtk`.

Examples:

```bash
rtk git status
rtk cargo test
rtk npm run build
rtk pytest -q
```

## Meta Commands

```bash
rtk gain            # Token savings analytics
rtk gain --history  # Recent command savings history
rtk proxy <cmd>     # Run raw command without filtering
```

## Verification

```bash
rtk --version
rtk gain
which rtk
```

exec
/bin/bash -lc "rtk sed -n '1,260p' .omc/collaboration/protocol.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Claude-Codex Collaboration Protocol

Version: 0.1
Status: active
Owner: Claude + Codex

## 1. Purpose

This protocol defines the shared operating contract for Claude-Codex collaboration in this repository. It covers task handoff, shared state, event logging, artifact creation, lock usage, and completion signaling.

Agents must read this file before participating in the collaboration workflow.

## 2. Directory Layout

All collaboration files live under `.omc/collaboration/`.

- `protocol.md`: this protocol.
- `state.json`: current shared workflow state.
- `events.jsonl`: append-only event log.
- `tasks/`: task specifications and task handoff documents.
- `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
- `locks/`: advisory lock files for serialized work.
- `codex-ready.md`: Codex readiness signal.

## 3. Authority And Conflicts

This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.

If a conflict is encountered, the active agent must follow the higher-priority instruction and record the conflict in its response or task artifact when material to the collaboration.

Codex-specific repository rules in `AGENTS.md` remain mandatory. Claude-specific repository rules in `CLAUDE.md` remain mandatory.

## 4. Shared State

`state.json` is the latest compact state snapshot. It must remain valid JSON.

Recommended schema:

```json
{
  "workflow_id": "claude-codex-collab-mvp",
  "current_task": null,
  "active_agent": "none",
  "status": "initialized",
  "last_event_id": 0,
  "updated_at": "2026-05-30T00:00:00.000Z"
}
```

Field meanings:

- `workflow_id`: stable collaboration workflow identifier.
- `current_task`: active task id or `null`.
- `active_agent`: `claude`, `codex`, or `none`.
- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
- `last_event_id`: numeric id of the last event written to `events.jsonl`.
- `updated_at`: UTC ISO-8601 timestamp for the state update.

State updates should be minimal and should not replace durable task or artifact content.

## 5. Event Log

`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.

Required event fields:

```json
{
  "id": 1,
  "type": "codex_ready",
  "agent": "codex",
  "timestamp": "2026-05-30T00:00:00.000Z",
  "summary": "Short event summary."
}
```

Recommended optional fields:

- `task_id`: related task id.
- `artifacts`: array of artifact paths.
- `status`: resulting workflow status.
- `details`: compact structured metadata.

Event id rules:

- Start at `1`.
- Increment by `1` for every new event.
- After writing an event, update `state.json.last_event_id` to the new id.

Common event types:

- `claude_ready`
- `codex_ready`
- `task_created`
- `task_claimed`
- `artifact_created`
- `handoff_requested`
- `review_requested`
- `blocked`
- `completed`

## 6. Tasks

Task documents belong in `.omc/collaboration/tasks/`.

Recommended task filename:

```text
TASK-YYYYMMDD-NN-short-name.md
```

Recommended task content:

- Task id.
- Owner or requesting agent.
- Objective.
- Scope.
- Inputs and relevant files.
- Expected outputs.
- Constraints and mandatory rules.
- Acceptance criteria.
- Current status.

When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.

## 7. Artifacts

Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.

Artifacts should be durable and self-contained enough for the other agent to continue work without relying on chat history.

Recommended artifact filenames:

```text
YYYYMMDD-HHMM-agent-topic.md
```

For formal Codex review or OMC `/ask codex` workflows, the repository's `docs/codex-review-protocol.md` remains mandatory and takes precedence over this generic artifact convention.

## 8. Locks

Locks are advisory files under `.omc/collaboration/locks/`.

Use a lock when two agents might modify the same shared collaboration file at the same time.

Recommended lock filename:

```text
resource-name.lock
```

Recommended lock content:

```json
{
  "agent": "codex",
  "resource": "state.json",
  "created_at": "2026-05-30T00:00:00.000Z",
  "reason": "Updating state after event append."
}
```

Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.

## 9. Handoff Rules

When handing work to the other agent:

1. Write or update the task document.
2. Write any supporting artifact needed for context.
3. Append a `handoff_requested` event.
4. Update `state.json` with the current task, status, active agent, and last event id.
5. State the handoff clearly in the user-facing response when applicable.

Handoffs should include concrete next actions, relevant file paths, and any known blockers.

## 10. Completion Rules

A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.

Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.

## 11. Readiness Signal

Codex readiness is represented by both:

- A `codex_ready` event in `events.jsonl`.
- `.omc/collaboration/codex-ready.md`.

Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.

## 12. Minimal Operating Checklist

Before collaboration work:

- Read `AGENTS.md` or `CLAUDE.md`, as applicable.
- Read `.omc/collaboration/protocol.md`.
- Inspect `state.json` and recent `events.jsonl` entries.

During collaboration work:

- Keep edits scoped to the task.
- Preserve append-only event history.
- Keep shared JSON valid.
- Create durable artifacts for decisions that must survive chat context.

After collaboration work:

- Append the relevant event.
- Update `state.json`.
- Verify changed files.
- Report completed items and any remaining risk.

exec
/bin/bash -lc "rtk sed -n '1,260p' .omc/collaboration/artifacts/20260530-0814-protocol-review-consensus.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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

exec
/bin/bash -lc "rtk sed -n '1,320p' .omc/collaboration/artifacts/20260530-0805-codex-protocol-critical-review.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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

exec
/bin/bash -lc "rtk sed -n '1,240p' .omc/collaboration/tasks/TASK-20260530-02-implement-p0-amendments.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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

codex
我已经确认 P0/P1 的边界：这次只落地锁、事件 ID、修复模式、原子 claim/state 写入和文件系统要求，不加入状态机、超时或 YAML 任务格式。接下来先检查当前共享状态和事件尾部，然后按协议占用任务。
exec
/bin/bash -lc 'rtk find .omc/collaboration/locks -maxdepth 3 -type f -o -type d' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system
 exited 1 in 0ms:
rtk: rtk find does not support compound predicates or actions (e.g. -not, -exec). Use `find` directly.

 succeeded in 0ms:
 M .omc/state/hud-stdin-cache.json
 M AGENTS.md
 M CLAUDE.md
?? .claude/
?? .omc/artifacts/
?? .omc/collaboration/
?? .omc/project-memory.json
?? .omc/sessions/
?? .omc/state/agent-replay-7afec07d-3b40-4e4c-8f86-86e9dc0e791c.jsonl
?? .omc/state/agent-replay-97c93024-a4c1-4e03-93bf-7522ce3517ff.jsonl
?? .omc/state/checkpoints/
?? .omc/state/last-tool-error.json
?? .omc/state/mission-state.json
?? .omc/state/sessions/4aad264e-c3a4-460a-9be1-61247202bad3/
?? .omc/state/sessions/7afec07d-3b40-4e4c-8f86-86e9dc0e791c/
?? .omc/state/sessions/97c93024-a4c1-4e03-93bf-7522ce3517ff/
?? .omc/state/sessions/c8f47bca-464c-4b8c-bab5-42ba59354101/
?? .omc/state/sessions/dcf39a3e-1b72-449a-9897-852c3c7f1253/
?? .omc/state/sessions/e2566739-aaa7-4701-9354-a710639ac308/
?? .omc/state/sessions/f91e1567-b1b2-4cc2-bd9b-355702bc1ec4/
?? docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md
?? docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md
?? docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md
?? docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md
?? docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md
?? docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md
?? docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md
?? docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md
?? docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md
?? docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md
?? docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md
?? docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md
?? docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md
?? docs/discussions/codex-review-2026-05-27/21-final-consensus.md
?? docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md
?? docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
?? docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md
?? docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
?? docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md
?? docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
?? "\346\257\225\344\270\232\347\246\273\346\240\241\347\263\273\347\273\237\347\224\250\346\210\267\346\226\207\346\241\243.zip"
exec
/bin/bash -lc 'rtk cat .omc/collaboration/state.json' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{
  "workflow_id": "claude-codex-collab-mvp",
  "current_task": "TASK-20260530-02",
  "active_agent": "claude",
  "status": "task_open",
  "last_event_id": 8,
  "updated_at": "2026-05-30T08:15:00.000Z"
}

exec
/bin/bash -lc 'rtk tail -n 30 .omc/collaboration/events.jsonl' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{"id":1,"type":"codex_ready","agent":"codex","timestamp":"2026-05-30T07:57:25.000Z","summary":"Codex collaboration configuration completed and ready for Claude-Codex workflow.","artifacts":["AGENTS.md",".omc/collaboration/protocol.md",".omc/collaboration/codex-ready.md"],"status":"codex_ready"}
{"id":2,"type":"task_created","agent":"claude","timestamp":"2026-05-30T08:04:10.000Z","summary":"Created protocol critical review task for Codex.","task_id":"TASK-20260530-01","artifacts":[".omc/collaboration/tasks/TASK-20260530-01-protocol-critical-review.md"],"status":"task_open"}
{"id":3,"type":"task_claimed","agent":"codex","timestamp":"2026-05-30T08:05:20.000Z","summary":"Codex claimed protocol critical review task.","task_id":"TASK-20260530-01","status":"in_progress"}
{"id":4,"type":"completed","agent":"codex","timestamp":"2026-05-30T08:05:20.000Z","summary":"Completed critical review of collaboration protocol and wrote review artifact.","task_id":"TASK-20260530-01","artifacts":[".omc/collaboration/artifacts/20260530-0805-codex-protocol-critical-review.md"],"status":"completed"}
{"id":5,"type":"review_response","agent":"claude","timestamp":"2026-05-30T08:08:45.000Z","summary":"Claude responded to Codex protocol review with critical analysis and questions.","task_id":"TASK-20260530-01","artifacts":[".omc/collaboration/artifacts/20260530-0808-claude-response-to-codex-review.md"],"status":"waiting"}
{"id":6,"type":"review_response","agent":"codex","timestamp":"2026-05-30T08:11:56.000Z","summary":"Codex responded to Claude's second-round protocol review questions and agreed on adjusted P0/P1 priorities.","task_id":"TASK-20260530-01","artifacts":[".omc/collaboration/artifacts/20260530-1611-codex-second-response-to-claude.md"],"status":"waiting"}
{"id":7,"type":"consensus_reached","agent":"claude","timestamp":"2026-05-30T08:14:30.000Z","summary":"Claude and Codex reached consensus on protocol amendments after 2-round iterative review.","task_id":"TASK-20260530-01","artifacts":[".omc/collaboration/artifacts/20260530-0814-protocol-review-consensus.md"],"status":"completed"}
{"id":8,"type":"task_created","agent":"claude","timestamp":"2026-05-30T08:15:00.000Z","summary":"Created P0 protocol amendment implementation task for Codex.","task_id":"TASK-20260530-02","artifacts":[".omc/collaboration/tasks/TASK-20260530-02-implement-p0-amendments.md"],"status":"task_open"}

codex
当前 `state.json` 指向本任务且状态为 `task_open`，事件尾部到 `id=8`；工作区已有大量未跟踪/修改文件，我会只碰协作协议、事件日志、状态文件和临时锁目录。现在先按将要落地的 journal lock 规则占用任务。
exec
/bin/bash -lc 'rtk ls -la .omc/collaboration/locks' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
(empty)

exec
/bin/bash -lc 'rtk mkdir .omc/collaboration/locks/journal.lock' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
exec
/bin/bash -lc "rtk python3 - <<'PY'
import json, os
from datetime import datetime, timezone
from pathlib import Path

base = Path('.omc/collaboration')
lock = base / 'locks' / 'journal.lock'
agent = 'codex'
task_id = 'TASK-20260530-02'
now = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
owner = {
    'agent': agent,
    'task_id': task_id,
    'created_at': now,
    'heartbeat_at': now,
    'reason': 'claim task and update state'
}
(lock / 'owner.json').write_text(json.dumps(owner, indent=2) + '\\n', encoding='utf-8')

events_path = base / 'events.jsonl'
state_path = base / 'state.json'

events = []
for lineno, line in enumerate(events_path.read_text(encoding='utf-8').splitlines(), 1):
    if not line.strip():
        continue
    try:
        events.append(json.loads(line))
    except json.JSONDecodeError as exc:
        raise SystemExit(f'malformed events.jsonl line {lineno}: {exc}')
ids = [e['id'] for e in events]
if len(ids) "'!= len(set(ids)):
    raise SystemExit('"'duplicate event ids detected')

active_statuses = {'task_claimed', 'in_progress', 'waiting', 'blocked', 'timeout_candidate'}
terminal_statuses = {'completed', 'cancelled'}
latest_task_events = [e for e in events if e.get('task_id') == task_id]
active_owner = None
for e in latest_task_events:
    status = e.get('status') or e.get('type')
    if status in active_statuses or e.get('type') == 'task_claimed':
        active_owner = e.get('agent')
    if status in terminal_statuses or e.get('type') in terminal_statuses:
        active_owner = None
if active_owner:
    raise SystemExit(f'task already has active owner: {active_owner}')

next_id = max(ids, default=0) + 1
event = {
    'id': next_id,
    'type': 'task_claimed',
    'agent': agent,
    'timestamp': now,
    'summary': 'Codex claimed P0 protocol amendment implementation task.',
    'task_id': task_id,
    'status': 'in_progress'
}
with events_path.open('a', encoding='utf-8') as f:
    f.write(json.dumps(event, separators=(',', ':')) + '\\n')

state = json.loads(state_path.read_text(encoding='utf-8'))
state.update({
    'current_task': task_id,
    'active_agent': agent,
    'status': 'in_progress',
    'last_event_id': next_id,
    'updated_at': now
})
tmp_path = base / f'state.json.tmp.{agent}'
tmp_path.write_text(json.dumps(state, indent=2) + '\\n', encoding='utf-8')
json.loads(tmp_path.read_text(encoding='utf-8'))
os.replace(tmp_path, state_path)

# Post-write validation.
written_events = [json.loads(line) for line in events_path.read_text(encoding='utf-8').splitlines() if line.strip()]
written_ids = [e['id'] for e in written_events]
if len(written_ids) "'!= len(set(written_ids)):
    raise SystemExit('"'duplicate event ids after append')
written_state = json.loads(state_path.read_text(encoding='utf-8'))
if written_state.get('last_event_id') "'!= max(written_ids):
    raise SystemExit('"'state last_event_id mismatch after append')

(lock / 'owner.json').unlink()
lock.rmdir()
PY" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
codex
任务已通过 `task_claimed` 事件占用，`state.json` 已更新为 `in_progress`。我现在会直接修改 `protocol.md`，尽量在原章节内补充 P0 条款，只为故障恢复新增一个章节并相应顺延后续编号。
exec
/bin/bash -lc 'rtk nl -ba .omc/collaboration/protocol.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# Claude-Codex Collaboration Protocol
     2	
     3	Version: 0.1
     4	Status: active
     5	Owner: Claude + Codex
     6	
     7	## 1. Purpose
     8	
     9	This protocol defines the shared operating contract for Claude-Codex collaboration in this repository. It covers task handoff, shared state, event logging, artifact creation, lock usage, and completion signaling.
    10	
    11	Agents must read this file before participating in the collaboration workflow.
    12	
    13	## 2. Directory Layout
    14	
    15	All collaboration files live under `.omc/collaboration/`.
    16	
    17	- `protocol.md`: this protocol.
    18	- `state.json`: current shared workflow state.
    19	- `events.jsonl`: append-only event log.
    20	- `tasks/`: task specifications and task handoff documents.
    21	- `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
    22	- `locks/`: advisory lock files for serialized work.
    23	- `codex-ready.md`: Codex readiness signal.
    24	
    25	## 3. Authority And Conflicts
    26	
    27	This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
    28	
    29	If a conflict is encountered, the active agent must follow the higher-priority instruction and record the conflict in its response or task artifact when material to the collaboration.
    30	
    31	Codex-specific repository rules in `AGENTS.md` remain mandatory. Claude-specific repository rules in `CLAUDE.md` remain mandatory.
    32	
    33	## 4. Shared State
    34	
    35	`state.json` is the latest compact state snapshot. It must remain valid JSON.
    36	
    37	Recommended schema:
    38	
    39	```json
    40	{
    41	  "workflow_id": "claude-codex-collab-mvp",
    42	  "current_task": null,
    43	  "active_agent": "none",
    44	  "status": "initialized",
    45	  "last_event_id": 0,
    46	  "updated_at": "2026-05-30T00:00:00.000Z"
    47	}
    48	```
    49	
    50	Field meanings:
    51	
    52	- `workflow_id`: stable collaboration workflow identifier.
    53	- `current_task`: active task id or `null`.
    54	- `active_agent`: `claude`, `codex`, or `none`.
    55	- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
    56	- `last_event_id`: numeric id of the last event written to `events.jsonl`.
    57	- `updated_at`: UTC ISO-8601 timestamp for the state update.
    58	
    59	State updates should be minimal and should not replace durable task or artifact content.
    60	
    61	## 5. Event Log
    62	
    63	`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
    64	
    65	Required event fields:
    66	
    67	```json
    68	{
    69	  "id": 1,
    70	  "type": "codex_ready",
    71	  "agent": "codex",
    72	  "timestamp": "2026-05-30T00:00:00.000Z",
    73	  "summary": "Short event summary."
    74	}
    75	```
    76	
    77	Recommended optional fields:
    78	
    79	- `task_id`: related task id.
    80	- `artifacts`: array of artifact paths.
    81	- `status`: resulting workflow status.
    82	- `details`: compact structured metadata.
    83	
    84	Event id rules:
    85	
    86	- Start at `1`.
    87	- Increment by `1` for every new event.
    88	- After writing an event, update `state.json.last_event_id` to the new id.
    89	
    90	Common event types:
    91	
    92	- `claude_ready`
    93	- `codex_ready`
    94	- `task_created`
    95	- `task_claimed`
    96	- `artifact_created`
    97	- `handoff_requested`
    98	- `review_requested`
    99	- `blocked`
   100	- `completed`
   101	
   102	## 6. Tasks
   103	
   104	Task documents belong in `.omc/collaboration/tasks/`.
   105	
   106	Recommended task filename:
   107	
   108	```text
   109	TASK-YYYYMMDD-NN-short-name.md
   110	```
   111	
   112	Recommended task content:
   113	
   114	- Task id.
   115	- Owner or requesting agent.
   116	- Objective.
   117	- Scope.
   118	- Inputs and relevant files.
   119	- Expected outputs.
   120	- Constraints and mandatory rules.
   121	- Acceptance criteria.
   122	- Current status.
   123	
   124	When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
   125	
   126	## 7. Artifacts
   127	
   128	Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
   129	
   130	Artifacts should be durable and self-contained enough for the other agent to continue work without relying on chat history.
   131	
   132	Recommended artifact filenames:
   133	
   134	```text
   135	YYYYMMDD-HHMM-agent-topic.md
   136	```
   137	
   138	For formal Codex review or OMC `/ask codex` workflows, the repository's `docs/codex-review-protocol.md` remains mandatory and takes precedence over this generic artifact convention.
   139	
   140	## 8. Locks
   141	
   142	Locks are advisory files under `.omc/collaboration/locks/`.
   143	
   144	Use a lock when two agents might modify the same shared collaboration file at the same time.
   145	
   146	Recommended lock filename:
   147	
   148	```text
   149	resource-name.lock
   150	```
   151	
   152	Recommended lock content:
   153	
   154	```json
   155	{
   156	  "agent": "codex",
   157	  "resource": "state.json",
   158	  "created_at": "2026-05-30T00:00:00.000Z",
   159	  "reason": "Updating state after event append."
   160	}
   161	```
   162	
   163	Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
   164	
   165	## 9. Handoff Rules
   166	
   167	When handing work to the other agent:
   168	
   169	1. Write or update the task document.
   170	2. Write any supporting artifact needed for context.
   171	3. Append a `handoff_requested` event.
   172	4. Update `state.json` with the current task, status, active agent, and last event id.
   173	5. State the handoff clearly in the user-facing response when applicable.
   174	
   175	Handoffs should include concrete next actions, relevant file paths, and any known blockers.
   176	
   177	## 10. Completion Rules
   178	
   179	A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
   180	
   181	Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
   182	
   183	## 11. Readiness Signal
   184	
   185	Codex readiness is represented by both:
   186	
   187	- A `codex_ready` event in `events.jsonl`.
   188	- `.omc/collaboration/codex-ready.md`.
   189	
   190	Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
   191	
   192	## 12. Minimal Operating Checklist
   193	
   194	Before collaboration work:
   195	
   196	- Read `AGENTS.md` or `CLAUDE.md`, as applicable.
   197	- Read `.omc/collaboration/protocol.md`.
   198	- Inspect `state.json` and recent `events.jsonl` entries.
   199	
   200	During collaboration work:
   201	
   202	- Keep edits scoped to the task.
   203	- Preserve append-only event history.
   204	- Keep shared JSON valid.
   205	- Create durable artifacts for decisions that must survive chat context.
   206	
   207	After collaboration work:
   208	
   209	- Append the relevant event.
   210	- Update `state.json`.
   211	- Verify changed files.
   212	- Report completed items and any remaining risk.

apply patch
patch: completed
/home/caohui/projects/graduation-leave-system/.omc/collaboration/protocol.md
diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
index a831acc3f4534a3d2c3a48ce4720292ccf968809..1eebdca436b69938feee685c03e0eddd4f6407d9
--- a/.omc/collaboration/protocol.md
+++ b/.omc/collaboration/protocol.md
@@ -1,6 +1,6 @@
 # Claude-Codex Collaboration Protocol
 
-Version: 0.1
+Version: 0.2
 Status: active
 Owner: Claude + Codex
 
@@ -22,6 +22,13 @@
 - `locks/`: advisory lock files for serialized work.
 - `codex-ready.md`: Codex readiness signal.
 
+Filesystem requirements:
+
+- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
+- Local filesystems and NFSv4 are acceptable for this workflow.
+- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
+- Production testing MUST NOT proceed on an unsupported filesystem.
+
 ## 3. Authority And Conflicts
 
 This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
@@ -34,6 +41,8 @@
 
 `state.json` is the latest compact state snapshot. It must remain valid JSON.
 
+`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.
+
 Recommended schema:
 
 ```json
@@ -52,15 +61,23 @@
 - `workflow_id`: stable collaboration workflow identifier.
 - `current_task`: active task id or `null`.
 - `active_agent`: `claude`, `codex`, or `none`.
-- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
 - `last_event_id`: numeric id of the last event written to `events.jsonl`.
 - `updated_at`: UTC ISO-8601 timestamp for the state update.
 
 State updates should be minimal and should not replace durable task or artifact content.
 
+State write rules:
+
+- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
+- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
+- Agents MUST validate the temporary file as well-formed JSON before publishing it.
+- Agents MUST atomically rename the validated temporary file into place with `mv`.
+- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+
 ## 5. Event Log
 
-`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
 
 Required event fields:
 
@@ -83,9 +100,12 @@
 
 Event id rules:
 
-- Start at `1`.
-- Increment by `1` for every new event.
-- After writing an event, update `state.json.last_event_id` to the new id.
+- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
+- New event ids MUST be allocated while holding `locks/journal.lock`.
+- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
+- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
+- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.
 
 Common event types:
 
@@ -121,8 +141,16 @@
 - Acceptance criteria.
 - Current status.
 
-When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+When claiming a task, the agent MUST use this atomic claim procedure:
 
+1. Acquire `locks/journal.lock`.
+2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
+3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
+4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
+5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
+6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
+7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.
+
 ## 7. Artifacts
 
 Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
@@ -139,7 +167,7 @@
 
 ## 8. Locks
 
-Locks are advisory files under `.omc/collaboration/locks/`.
+Locks are files or directories under `.omc/collaboration/locks/`.
 
 Use a lock when two agents might modify the same shared collaboration file at the same time.
 
@@ -162,8 +190,46 @@
 
 Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
 
-## 9. Handoff Rules
+### Required Journal Lock
+
+Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.
+
+Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:
+
+```bash
+mkdir .omc/collaboration/locks/journal.lock
+```
+
+The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.
+
+The lock directory MUST contain `owner.json`:
+
+```json
+{
+  "agent": "codex",
+  "task_id": "TASK-20260530-01",
+  "created_at": "2026-05-30T08:00:00.000Z",
+  "heartbeat_at": "2026-05-30T08:00:00.000Z",
+  "reason": "append event and update state"
+}
+```
+
+The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.
+
+## 9. Failure Recovery
+
+Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.
+
+If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.
+
+If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.
+
+If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.
 
+Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.
+
+## 10. Handoff Rules
+
 When handing work to the other agent:
 
 1. Write or update the task document.
@@ -174,13 +240,13 @@
 
 Handoffs should include concrete next actions, relevant file paths, and any known blockers.
 
-## 10. Completion Rules
+## 11. Completion Rules
 
 A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
 
 Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
 
-## 11. Readiness Signal
+## 12. Readiness Signal
 
 Codex readiness is represented by both:
 
@@ -189,19 +255,21 @@
 
 Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
 
-## 12. Minimal Operating Checklist
+## 13. Minimal Operating Checklist
 
 Before collaboration work:
 
 - Read `AGENTS.md` or `CLAUDE.md`, as applicable.
 - Read `.omc/collaboration/protocol.md`.
 - Inspect `state.json` and recent `events.jsonl` entries.
+- Verify that `.omc/collaboration/` is on a supported filesystem before production testing.
 
 During collaboration work:
 
 - Keep edits scoped to the task.
 - Preserve append-only event history.
 - Keep shared JSON valid.
+- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.
 - Create durable artifacts for decisions that must survive chat context.
 
 After collaboration work:

diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
index a831acc3f4534a3d2c3a48ce4720292ccf968809..1eebdca436b69938feee685c03e0eddd4f6407d9
--- a/.omc/collaboration/protocol.md
+++ b/.omc/collaboration/protocol.md
@@ -1,6 +1,6 @@
 # Claude-Codex Collaboration Protocol
 
-Version: 0.1
+Version: 0.2
 Status: active
 Owner: Claude + Codex
 
@@ -22,6 +22,13 @@
 - `locks/`: advisory lock files for serialized work.
 - `codex-ready.md`: Codex readiness signal.
 
+Filesystem requirements:
+
+- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
+- Local filesystems and NFSv4 are acceptable for this workflow.
+- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
+- Production testing MUST NOT proceed on an unsupported filesystem.
+
 ## 3. Authority And Conflicts
 
 This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
@@ -34,6 +41,8 @@
 
 `state.json` is the latest compact state snapshot. It must remain valid JSON.
 
+`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.
+
 Recommended schema:
 
 ```json
@@ -52,15 +61,23 @@
 - `workflow_id`: stable collaboration workflow identifier.
 - `current_task`: active task id or `null`.
 - `active_agent`: `claude`, `codex`, or `none`.
-- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
 - `last_event_id`: numeric id of the last event written to `events.jsonl`.
 - `updated_at`: UTC ISO-8601 timestamp for the state update.
 
 State updates should be minimal and should not replace durable task or artifact content.
 
+State write rules:
+
+- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
+- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
+- Agents MUST validate the temporary file as well-formed JSON before publishing it.
+- Agents MUST atomically rename the validated temporary file into place with `mv`.
+- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+
 ## 5. Event Log
 
-`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
 
 Required event fields:
 
@@ -83,9 +100,12 @@
 
 Event id rules:
 
-- Start at `1`.
-- Increment by `1` for every new event.
-- After writing an event, update `state.json.last_event_id` to the new id.
+- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
+- New event ids MUST be allocated while holding `locks/journal.lock`.
+- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
+- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
+- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.
 
 Common event types:
 
@@ -121,8 +141,16 @@
 - Acceptance criteria.
 - Current status.
 
-When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+When claiming a task, the agent MUST use this atomic claim procedure:
 
+1. Acquire `locks/journal.lock`.
+2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
+3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
+4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
+5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
+6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
+7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.
+
 ## 7. Artifacts
 
 Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
@@ -139,7 +167,7 @@
 
 ## 8. Locks
 
-Locks are advisory files under `.omc/collaboration/locks/`.
+Locks are files or directories under `.omc/collaboration/locks/`.
 
 Use a lock when two agents might modify the same shared collaboration file at the same time.
 
@@ -162,8 +190,46 @@
 
 Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
 
-## 9. Handoff Rules
+### Required Journal Lock
+
+Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.
+
+Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:
+
+```bash
+mkdir .omc/collaboration/locks/journal.lock
+```
+
+The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.
+
+The lock directory MUST contain `owner.json`:
+
+```json
+{
+  "agent": "codex",
+  "task_id": "TASK-20260530-01",
+  "created_at": "2026-05-30T08:00:00.000Z",
+  "heartbeat_at": "2026-05-30T08:00:00.000Z",
+  "reason": "append event and update state"
+}
+```
+
+The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.
+
+## 9. Failure Recovery
+
+Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.
+
+If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.
+
+If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.
+
+If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.
 
+Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.
+
+## 10. Handoff Rules
+
 When handing work to the other agent:
 
 1. Write or update the task document.
@@ -174,13 +240,13 @@
 
 Handoffs should include concrete next actions, relevant file paths, and any known blockers.
 
-## 10. Completion Rules
+## 11. Completion Rules
 
 A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
 
 Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
 
-## 11. Readiness Signal
+## 12. Readiness Signal
 
 Codex readiness is represented by both:
 
@@ -189,19 +255,21 @@
 
 Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
 
-## 12. Minimal Operating Checklist
+## 13. Minimal Operating Checklist
 
 Before collaboration work:
 
 - Read `AGENTS.md` or `CLAUDE.md`, as applicable.
 - Read `.omc/collaboration/protocol.md`.
 - Inspect `state.json` and recent `events.jsonl` entries.
+- Verify that `.omc/collaboration/` is on a supported filesystem before production testing.
 
 During collaboration work:
 
 - Keep edits scoped to the task.
 - Preserve append-only event history.
 - Keep shared JSON valid.
+- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.
 - Create durable artifacts for decisions that must survive chat context.
 
 After collaboration work:

codex
`protocol.md` 已完成第一版修订：版本号、事件源权威性、锁、ID 分配、原子 claim、原子 state 写入、故障修复和文件系统约束都已放入原有章节附近。现在我会通读并做结构/关键词检查，确认没有把 P1 的状态机、任务超时或 YAML 要求带进去。
exec
/bin/bash -lc "rtk sed -n '1,320p' .omc/collaboration/protocol.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Claude-Codex Collaboration Protocol

Version: 0.2
Status: active
Owner: Claude + Codex

## 1. Purpose

This protocol defines the shared operating contract for Claude-Codex collaboration in this repository. It covers task handoff, shared state, event logging, artifact creation, lock usage, and completion signaling.

Agents must read this file before participating in the collaboration workflow.

## 2. Directory Layout

All collaboration files live under `.omc/collaboration/`.

- `protocol.md`: this protocol.
- `state.json`: current shared workflow state.
- `events.jsonl`: append-only event log.
- `tasks/`: task specifications and task handoff documents.
- `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
- `locks/`: advisory lock files for serialized work.
- `codex-ready.md`: Codex readiness signal.

Filesystem requirements:

- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
- Local filesystems and NFSv4 are acceptable for this workflow.
- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
- Production testing MUST NOT proceed on an unsupported filesystem.

## 3. Authority And Conflicts

This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.

If a conflict is encountered, the active agent must follow the higher-priority instruction and record the conflict in its response or task artifact when material to the collaboration.

Codex-specific repository rules in `AGENTS.md` remain mandatory. Claude-specific repository rules in `CLAUDE.md` remain mandatory.

## 4. Shared State

`state.json` is the latest compact state snapshot. It must remain valid JSON.

`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.

Recommended schema:

```json
{
  "workflow_id": "claude-codex-collab-mvp",
  "current_task": null,
  "active_agent": "none",
  "status": "initialized",
  "last_event_id": 0,
  "updated_at": "2026-05-30T00:00:00.000Z"
}
```

Field meanings:

- `workflow_id`: stable collaboration workflow identifier.
- `current_task`: active task id or `null`.
- `active_agent`: `claude`, `codex`, or `none`.
- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
- `last_event_id`: numeric id of the last event written to `events.jsonl`.
- `updated_at`: UTC ISO-8601 timestamp for the state update.

State updates should be minimal and should not replace durable task or artifact content.

State write rules:

- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
- Agents MUST validate the temporary file as well-formed JSON before publishing it.
- Agents MUST atomically rename the validated temporary file into place with `mv`.
- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.

## 5. Event Log

`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.

Required event fields:

```json
{
  "id": 1,
  "type": "codex_ready",
  "agent": "codex",
  "timestamp": "2026-05-30T00:00:00.000Z",
  "summary": "Short event summary."
}
```

Recommended optional fields:

- `task_id`: related task id.
- `artifacts`: array of artifact paths.
- `status`: resulting workflow status.
- `details`: compact structured metadata.

Event id rules:

- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
- New event ids MUST be allocated while holding `locks/journal.lock`.
- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.

Common event types:

- `claude_ready`
- `codex_ready`
- `task_created`
- `task_claimed`
- `artifact_created`
- `handoff_requested`
- `review_requested`
- `blocked`
- `completed`

## 6. Tasks

Task documents belong in `.omc/collaboration/tasks/`.

Recommended task filename:

```text
TASK-YYYYMMDD-NN-short-name.md
```

Recommended task content:

- Task id.
- Owner or requesting agent.
- Objective.
- Scope.
- Inputs and relevant files.
- Expected outputs.
- Constraints and mandatory rules.
- Acceptance criteria.
- Current status.

When claiming a task, the agent MUST use this atomic claim procedure:

1. Acquire `locks/journal.lock`.
2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.

## 7. Artifacts

Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.

Artifacts should be durable and self-contained enough for the other agent to continue work without relying on chat history.

Recommended artifact filenames:

```text
YYYYMMDD-HHMM-agent-topic.md
```

For formal Codex review or OMC `/ask codex` workflows, the repository's `docs/codex-review-protocol.md` remains mandatory and takes precedence over this generic artifact convention.

## 8. Locks

Locks are files or directories under `.omc/collaboration/locks/`.

Use a lock when two agents might modify the same shared collaboration file at the same time.

Recommended lock filename:

```text
resource-name.lock
```

Recommended lock content:

```json
{
  "agent": "codex",
  "resource": "state.json",
  "created_at": "2026-05-30T00:00:00.000Z",
  "reason": "Updating state after event append."
}
```

Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.

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

The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.

## 9. Failure Recovery

Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.

If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.

If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.

If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.

Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.

## 10. Handoff Rules

When handing work to the other agent:

1. Write or update the task document.
2. Write any supporting artifact needed for context.
3. Append a `handoff_requested` event.
4. Update `state.json` with the current task, status, active agent, and last event id.
5. State the handoff clearly in the user-facing response when applicable.

Handoffs should include concrete next actions, relevant file paths, and any known blockers.

## 11. Completion Rules

A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.

Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.

## 12. Readiness Signal

Codex readiness is represented by both:

- A `codex_ready` event in `events.jsonl`.
- `.omc/collaboration/codex-ready.md`.

Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.

## 13. Minimal Operating Checklist

Before collaboration work:

- Read `AGENTS.md` or `CLAUDE.md`, as applicable.
- Read `.omc/collaboration/protocol.md`.
- Inspect `state.json` and recent `events.jsonl` entries.
- Verify that `.omc/collaboration/` is on a supported filesystem before production testing.

During collaboration work:

- Keep edits scoped to the task.
- Preserve append-only event history.
- Keep shared JSON valid.
- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.
- Create durable artifacts for decisions that must survive chat context.

After collaboration work:

- Append the relevant event.
- Update `state.json`.
- Verify changed files.
- Report completed items and any remaining risk.

exec
/bin/bash -lc "rtk python3 - <<'PY'
import json
from pathlib import Path
p = Path('.omc/collaboration/events.jsonl')
ids = []
for i, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
    if not line.strip():
        continue
    event = json.loads(line)
    ids.append(event['id'])
print({'events': len(ids), 'max_id': max(ids), 'duplicates': len(ids) - len(set(ids))})
PY" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk rg -n "Version:|events.jsonl|journal.lock|next id|needs_repair|state.json.tmp|atomic|NFS|YAML|front matter|transition table|heartbeat event|60 minutes|30 minutes" .omc/collaboration/protocol.md' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk python3 -m json.tool .omc/collaboration/state.json' in /home/caohui/projects/graduation-leave-system
 succeeded in 168ms:
3:Version: 0.2
19:- `events.jsonl`: append-only event log.
27:- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
28:- Local filesystems and NFSv4 are acceptable for this workflow.
29:- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
44:`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.
64:- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
65:- `last_event_id`: numeric id of the last event written to `events.jsonl`.
72:- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
73:- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
75:- Agents MUST atomically rename the validated temporary file into place with `mv`.
76:- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
80:`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
104:- New event ids MUST be allocated while holding `locks/journal.lock`.
105:- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
107:- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
144:When claiming a task, the agent MUST use this atomic claim procedure:
146:1. Acquire `locks/journal.lock`.
147:2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
149:4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
150:5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
151:6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
152:7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.
195:Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.
197:Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:
200:mkdir .omc/collaboration/locks/journal.lock
203:The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.
217:The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.
221:Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.
223:If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.
225:If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.
227:If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.
253:- A `codex_ready` event in `events.jsonl`.
264:- Inspect `state.json` and recent `events.jsonl` entries.
272:- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.

diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
index a831acc3f4534a3d2c3a48ce4720292ccf968809..1eebdca436b69938feee685c03e0eddd4f6407d9
--- a/.omc/collaboration/protocol.md
+++ b/.omc/collaboration/protocol.md
@@ -1,6 +1,6 @@
 # Claude-Codex Collaboration Protocol
 
-Version: 0.1
+Version: 0.2
 Status: active
 Owner: Claude + Codex
 
@@ -22,6 +22,13 @@
 - `locks/`: advisory lock files for serialized work.
 - `codex-ready.md`: Codex readiness signal.
 
+Filesystem requirements:
+
+- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
+- Local filesystems and NFSv4 are acceptable for this workflow.
+- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
+- Production testing MUST NOT proceed on an unsupported filesystem.
+
 ## 3. Authority And Conflicts
 
 This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
@@ -34,6 +41,8 @@
 
 `state.json` is the latest compact state snapshot. It must remain valid JSON.
 
+`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.
+
 Recommended schema:
 
 ```json
@@ -52,15 +61,23 @@
 - `workflow_id`: stable collaboration workflow identifier.
 - `current_task`: active task id or `null`.
 - `active_agent`: `claude`, `codex`, or `none`.
-- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
 - `last_event_id`: numeric id of the last event written to `events.jsonl`.
 - `updated_at`: UTC ISO-8601 timestamp for the state update.
 
 State updates should be minimal and should not replace durable task or artifact content.
 
+State write rules:
+
+- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
+- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
+- Agents MUST validate the temporary file as well-formed JSON before publishing it.
+- Agents MUST atomically rename the validated temporary file into place with `mv`.
+- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+
 ## 5. Event Log
 
-`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
 
 Required event fields:
 
@@ -83,9 +100,12 @@
 
 Event id rules:
 
-- Start at `1`.
-- Increment by `1` for every new event.
-- After writing an event, update `state.json.last_event_id` to the new id.
+- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
+- New event ids MUST be allocated while holding `locks/journal.lock`.
+- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
+- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
+- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.
 
 Common event types:
 
@@ -121,8 +141,16 @@
 - Acceptance criteria.
 - Current status.
 
-When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+When claiming a task, the agent MUST use this atomic claim procedure:
 
+1. Acquire `locks/journal.lock`.
+2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
+3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
+4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
+5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
+6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
+7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.
+
 ## 7. Artifacts
 
 Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
@@ -139,7 +167,7 @@
 
 ## 8. Locks
 
-Locks are advisory files under `.omc/collaboration/locks/`.
+Locks are files or directories under `.omc/collaboration/locks/`.
 
 Use a lock when two agents might modify the same shared collaboration file at the same time.
 
@@ -162,8 +190,46 @@
 
 Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
 
-## 9. Handoff Rules
+### Required Journal Lock
+
+Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.
+
+Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:
+
+```bash
+mkdir .omc/collaboration/locks/journal.lock
+```
+
+The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.
+
+The lock directory MUST contain `owner.json`:
+
+```json
+{
+  "agent": "codex",
+  "task_id": "TASK-20260530-01",
+  "created_at": "2026-05-30T08:00:00.000Z",
+  "heartbeat_at": "2026-05-30T08:00:00.000Z",
+  "reason": "append event and update state"
+}
+```
+
+The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.
+
+## 9. Failure Recovery
+
+Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.
+
+If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.
+
+If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.
+
+If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.
 
+Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.
+
+## 10. Handoff Rules
+
 When handing work to the other agent:
 
 1. Write or update the task document.
@@ -174,13 +240,13 @@
 
 Handoffs should include concrete next actions, relevant file paths, and any known blockers.
 
-## 10. Completion Rules
+## 11. Completion Rules
 
 A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
 
 Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
 
-## 11. Readiness Signal
+## 12. Readiness Signal
 
 Codex readiness is represented by both:
 
@@ -189,19 +255,21 @@
 
 Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
 
-## 12. Minimal Operating Checklist
+## 13. Minimal Operating Checklist
 
 Before collaboration work:
 
 - Read `AGENTS.md` or `CLAUDE.md`, as applicable.
 - Read `.omc/collaboration/protocol.md`.
 - Inspect `state.json` and recent `events.jsonl` entries.
+- Verify that `.omc/collaboration/` is on a supported filesystem before production testing.
 
 During collaboration work:
 
 - Keep edits scoped to the task.
 - Preserve append-only event history.
 - Keep shared JSON valid.
+- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.
 - Create durable artifacts for decisions that must survive chat context.
 
 After collaboration work:

 succeeded in 196ms:
{'events': 9, 'max_id': 9, 'duplicates': 0}

 succeeded in 264ms:
{
    "workflow_id": "claude-codex-collab-mvp",
    "current_task": "TASK-20260530-02",
    "active_agent": "codex",
    "status": "in_progress",
    "last_event_id": 9,
    "updated_at": "2026-05-30T08:18:38.469Z"
}

codex
校验结果显示协议为 0.2，事件日志和状态 JSON 当前有效，事件 ID 到 `9` 且无重复。我发现目录说明里还保留了“advisory lock files”的旧措辞，会把它改成同时覆盖强制 journal lock 的“lock files/directories”。
apply patch
patch: completed
/home/caohui/projects/graduation-leave-system/.omc/collaboration/protocol.md
diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
index a831acc3f4534a3d2c3a48ce4720292ccf968809..c07e6b15a0f90675f8257f004240b0ceca386f80
--- a/.omc/collaboration/protocol.md
+++ b/.omc/collaboration/protocol.md
@@ -1,6 +1,6 @@
 # Claude-Codex Collaboration Protocol
 
-Version: 0.1
+Version: 0.2
 Status: active
 Owner: Claude + Codex
 
@@ -19,9 +19,16 @@
 - `events.jsonl`: append-only event log.
 - `tasks/`: task specifications and task handoff documents.
 - `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
-- `locks/`: advisory lock files for serialized work.
+- `locks/`: lock files or directories for serialized work.
 - `codex-ready.md`: Codex readiness signal.
 
+Filesystem requirements:
+
+- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
+- Local filesystems and NFSv4 are acceptable for this workflow.
+- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
+- Production testing MUST NOT proceed on an unsupported filesystem.
+
 ## 3. Authority And Conflicts
 
 This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
@@ -34,6 +41,8 @@
 
 `state.json` is the latest compact state snapshot. It must remain valid JSON.
 
+`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.
+
 Recommended schema:
 
 ```json
@@ -52,15 +61,23 @@
 - `workflow_id`: stable collaboration workflow identifier.
 - `current_task`: active task id or `null`.
 - `active_agent`: `claude`, `codex`, or `none`.
-- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
 - `last_event_id`: numeric id of the last event written to `events.jsonl`.
 - `updated_at`: UTC ISO-8601 timestamp for the state update.
 
 State updates should be minimal and should not replace durable task or artifact content.
 
+State write rules:
+
+- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
+- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
+- Agents MUST validate the temporary file as well-formed JSON before publishing it.
+- Agents MUST atomically rename the validated temporary file into place with `mv`.
+- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+
 ## 5. Event Log
 
-`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
 
 Required event fields:
 
@@ -83,9 +100,12 @@
 
 Event id rules:
 
-- Start at `1`.
-- Increment by `1` for every new event.
-- After writing an event, update `state.json.last_event_id` to the new id.
+- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
+- New event ids MUST be allocated while holding `locks/journal.lock`.
+- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
+- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
+- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.
 
 Common event types:
 
@@ -121,8 +141,16 @@
 - Acceptance criteria.
 - Current status.
 
-When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+When claiming a task, the agent MUST use this atomic claim procedure:
 
+1. Acquire `locks/journal.lock`.
+2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
+3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
+4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
+5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
+6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
+7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.
+
 ## 7. Artifacts
 
 Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
@@ -139,7 +167,7 @@
 
 ## 8. Locks
 
-Locks are advisory files under `.omc/collaboration/locks/`.
+Locks are files or directories under `.omc/collaboration/locks/`.
 
 Use a lock when two agents might modify the same shared collaboration file at the same time.
 
@@ -162,8 +190,46 @@
 
 Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
 
-## 9. Handoff Rules
+### Required Journal Lock
+
+Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.
+
+Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:
+
+```bash
+mkdir .omc/collaboration/locks/journal.lock
+```
+
+The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.
+
+The lock directory MUST contain `owner.json`:
+
+```json
+{
+  "agent": "codex",
+  "task_id": "TASK-20260530-01",
+  "created_at": "2026-05-30T08:00:00.000Z",
+  "heartbeat_at": "2026-05-30T08:00:00.000Z",
+  "reason": "append event and update state"
+}
+```
 
+The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.
+
+## 9. Failure Recovery
+
+Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.
+
+If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.
+
+If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.
+
+If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.
+
+Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.
+
+## 10. Handoff Rules
+
 When handing work to the other agent:
 
 1. Write or update the task document.
@@ -174,13 +240,13 @@
 
 Handoffs should include concrete next actions, relevant file paths, and any known blockers.
 
-## 10. Completion Rules
+## 11. Completion Rules
 
 A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
 
 Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
 
-## 11. Readiness Signal
+## 12. Readiness Signal
 
 Codex readiness is represented by both:
 
@@ -189,19 +255,21 @@
 
 Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
 
-## 12. Minimal Operating Checklist
+## 13. Minimal Operating Checklist
 
 Before collaboration work:
 
 - Read `AGENTS.md` or `CLAUDE.md`, as applicable.
 - Read `.omc/collaboration/protocol.md`.
 - Inspect `state.json` and recent `events.jsonl` entries.
+- Verify that `.omc/collaboration/` is on a supported filesystem before production testing.
 
 During collaboration work:
 
 - Keep edits scoped to the task.
 - Preserve append-only event history.
 - Keep shared JSON valid.
+- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.
 - Create durable artifacts for decisions that must survive chat context.
 
 After collaboration work:

diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
index a831acc3f4534a3d2c3a48ce4720292ccf968809..c07e6b15a0f90675f8257f004240b0ceca386f80
--- a/.omc/collaboration/protocol.md
+++ b/.omc/collaboration/protocol.md
@@ -1,6 +1,6 @@
 # Claude-Codex Collaboration Protocol
 
-Version: 0.1
+Version: 0.2
 Status: active
 Owner: Claude + Codex
 
@@ -19,9 +19,16 @@
 - `events.jsonl`: append-only event log.
 - `tasks/`: task specifications and task handoff documents.
 - `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
-- `locks/`: advisory lock files for serialized work.
+- `locks/`: lock files or directories for serialized work.
 - `codex-ready.md`: Codex readiness signal.
 
+Filesystem requirements:
+
+- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
+- Local filesystems and NFSv4 are acceptable for this workflow.
+- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
+- Production testing MUST NOT proceed on an unsupported filesystem.
+
 ## 3. Authority And Conflicts
 
 This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
@@ -34,6 +41,8 @@
 
 `state.json` is the latest compact state snapshot. It must remain valid JSON.
 
+`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.
+
 Recommended schema:
 
 ```json
@@ -52,15 +61,23 @@
 - `workflow_id`: stable collaboration workflow identifier.
 - `current_task`: active task id or `null`.
 - `active_agent`: `claude`, `codex`, or `none`.
-- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
 - `last_event_id`: numeric id of the last event written to `events.jsonl`.
 - `updated_at`: UTC ISO-8601 timestamp for the state update.
 
 State updates should be minimal and should not replace durable task or artifact content.
 
+State write rules:
+
+- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
+- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
+- Agents MUST validate the temporary file as well-formed JSON before publishing it.
+- Agents MUST atomically rename the validated temporary file into place with `mv`.
+- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+
 ## 5. Event Log
 
-`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
 
 Required event fields:
 
@@ -83,9 +100,12 @@
 
 Event id rules:
 
-- Start at `1`.
-- Increment by `1` for every new event.
-- After writing an event, update `state.json.last_event_id` to the new id.
+- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
+- New event ids MUST be allocated while holding `locks/journal.lock`.
+- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
+- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
+- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.
 
 Common event types:
 
@@ -121,8 +141,16 @@
 - Acceptance criteria.
 - Current status.
 
-When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+When claiming a task, the agent MUST use this atomic claim procedure:
 
+1. Acquire `locks/journal.lock`.
+2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
+3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
+4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
+5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
+6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
+7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.
+
 ## 7. Artifacts
 
 Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
@@ -139,7 +167,7 @@
 
 ## 8. Locks
 
-Locks are advisory files under `.omc/collaboration/locks/`.
+Locks are files or directories under `.omc/collaboration/locks/`.
 
 Use a lock when two agents might modify the same shared collaboration file at the same time.
 
@@ -162,8 +190,46 @@
 
 Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
 
-## 9. Handoff Rules
+### Required Journal Lock
+
+Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.
+
+Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:
+
+```bash
+mkdir .omc/collaboration/locks/journal.lock
+```
+
+The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.
+
+The lock directory MUST contain `owner.json`:
+
+```json
+{
+  "agent": "codex",
+  "task_id": "TASK-20260530-01",
+  "created_at": "2026-05-30T08:00:00.000Z",
+  "heartbeat_at": "2026-05-30T08:00:00.000Z",
+  "reason": "append event and update state"
+}
+```
 
+The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.
+
+## 9. Failure Recovery
+
+Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.
+
+If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.
+
+If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.
+
+If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.
+
+Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.
+
+## 10. Handoff Rules
+
 When handing work to the other agent:
 
 1. Write or update the task document.
@@ -174,13 +240,13 @@
 
 Handoffs should include concrete next actions, relevant file paths, and any known blockers.
 
-## 10. Completion Rules
+## 11. Completion Rules
 
 A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
 
 Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
 
-## 11. Readiness Signal
+## 12. Readiness Signal
 
 Codex readiness is represented by both:
 
@@ -189,19 +255,21 @@
 
 Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
 
-## 12. Minimal Operating Checklist
+## 13. Minimal Operating Checklist
 
 Before collaboration work:
 
 - Read `AGENTS.md` or `CLAUDE.md`, as applicable.
 - Read `.omc/collaboration/protocol.md`.
 - Inspect `state.json` and recent `events.jsonl` entries.
+- Verify that `.omc/collaboration/` is on a supported filesystem before production testing.
 
 During collaboration work:
 
 - Keep edits scoped to the task.
 - Preserve append-only event history.
 - Keep shared JSON valid.
+- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.
 - Create durable artifacts for decisions that must survive chat context.
 
 After collaboration work:

exec
/bin/bash -lc 'rtk git diff -- .omc/collaboration/protocol.md .omc/collaboration/events.jsonl .omc/collaboration/state.json' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
exec
/bin/bash -lc "rtk rg -n \"Version: 0.2|source of truth|rebuildable cache|journal.lock|owner.json|max\\(event.id\\)|needs_repair|state.json.tmp|atomic "'`mkdir`|NFSv2|NFSv3|YAML front matter|transition table|60-minute|60 minutes|30-minute|30 minutes" .omc/collaboration/protocol.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
error: the following required arguments were not provided:
  <dirs>...

Usage: mkdir [OPTION]... DIRECTORY...

For more information, try '--help'.
3:Version: 0.2
27:- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
29:- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
44:`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.
64:- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
72:- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
73:- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
80:`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
104:- New event ids MUST be allocated while holding `locks/journal.lock`.
105:- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
144:When claiming a task, the agent MUST use this atomic claim procedure:
146:1. Acquire `locks/journal.lock`.
149:4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
150:5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
151:6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
152:7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.
195:Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.
197:Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:
200:mkdir .omc/collaboration/locks/journal.lock
203:The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.
205:The lock directory MUST contain `owner.json`:
217:The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.
223:If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.
225:If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.
227:If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.
272:- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.

exec
/bin/bash -lc "rtk python3 - <<'PY'
from pathlib import Path
text = Path('.omc/collaboration/protocol.md').read_text(encoding='utf-8')
checks = {
    'version_0_2': 'Version: 0.2' in text,
    'events_authoritative': 'source of truth' in text and 'rebuildable cache' in text,
    'journal_lock': 'journal.lock' in text and 'owner.json' in text,
    'event_id_from_log': 'max(event.id) + 1' in text and 'MUST NOT allocate event ids from "'`state.json.last_event_id`'"' in text,
    'needs_repair': 'needs_repair' in text and 'Failure Recovery' in text,
    'atomic_claim': 'atomic claim procedure' in text and 'active owner' in text,
    'atomic_state_write': 'state.json.tmp.<agent>' in text and 'atomically rename' in text,
    'filesystem': 'atomic "'`mkdir` semantics'"' in text and 'NFSv2' in text and 'NFSv3' in text,
    'no_yaml_front_matter': 'YAML front matter' not in text,
    'no_transition_table': 'transition table' not in text,
    'no_task_timeout_rules': '60 minutes' not in text and '30 minutes' not in text and '60-minute' not in text and '30-minute' not in text,
}
for key, value in checks.items():
    print(f'{key}: {value}')
if not all(checks.values()):
    raise SystemExit(1)
PY" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
version_0_2: True
events_authoritative: True
journal_lock: True
event_id_from_log: True
needs_repair: True
atomic_claim: True
atomic_state_write: True
filesystem: True
no_yaml_front_matter: True
no_transition_table: True
no_task_timeout_rules: True

diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
index a831acc3f4534a3d2c3a48ce4720292ccf968809..c07e6b15a0f90675f8257f004240b0ceca386f80
--- a/.omc/collaboration/protocol.md
+++ b/.omc/collaboration/protocol.md
@@ -1,6 +1,6 @@
 # Claude-Codex Collaboration Protocol
 
-Version: 0.1
+Version: 0.2
 Status: active
 Owner: Claude + Codex
 
@@ -19,9 +19,16 @@
 - `events.jsonl`: append-only event log.
 - `tasks/`: task specifications and task handoff documents.
 - `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
-- `locks/`: advisory lock files for serialized work.
+- `locks/`: lock files or directories for serialized work.
 - `codex-ready.md`: Codex readiness signal.
 
+Filesystem requirements:
+
+- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
+- Local filesystems and NFSv4 are acceptable for this workflow.
+- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
+- Production testing MUST NOT proceed on an unsupported filesystem.
+
 ## 3. Authority And Conflicts
 
 This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
@@ -34,6 +41,8 @@
 
 `state.json` is the latest compact state snapshot. It must remain valid JSON.
 
+`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.
+
 Recommended schema:
 
 ```json
@@ -52,15 +61,23 @@
 - `workflow_id`: stable collaboration workflow identifier.
 - `current_task`: active task id or `null`.
 - `active_agent`: `claude`, `codex`, or `none`.
-- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
 - `last_event_id`: numeric id of the last event written to `events.jsonl`.
 - `updated_at`: UTC ISO-8601 timestamp for the state update.
 
 State updates should be minimal and should not replace durable task or artifact content.
 
+State write rules:
+
+- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
+- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
+- Agents MUST validate the temporary file as well-formed JSON before publishing it.
+- Agents MUST atomically rename the validated temporary file into place with `mv`.
+- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+
 ## 5. Event Log
 
-`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
 
 Required event fields:
 
@@ -83,9 +100,12 @@
 
 Event id rules:
 
-- Start at `1`.
-- Increment by `1` for every new event.
-- After writing an event, update `state.json.last_event_id` to the new id.
+- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
+- New event ids MUST be allocated while holding `locks/journal.lock`.
+- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
+- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
+- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.
 
 Common event types:
 
@@ -121,8 +141,16 @@
 - Acceptance criteria.
 - Current status.
 
-When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+When claiming a task, the agent MUST use this atomic claim procedure:
 
+1. Acquire `locks/journal.lock`.
+2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
+3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
+4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
+5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
+6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
+7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.
+
 ## 7. Artifacts
 
 Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
@@ -139,7 +167,7 @@
 
 ## 8. Locks
 
-Locks are advisory files under `.omc/collaboration/locks/`.
+Locks are files or directories under `.omc/collaboration/locks/`.
 
 Use a lock when two agents might modify the same shared collaboration file at the same time.
 
@@ -162,8 +190,46 @@
 
 Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
 
-## 9. Handoff Rules
+### Required Journal Lock
+
+Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.
+
+Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:
+
+```bash
+mkdir .omc/collaboration/locks/journal.lock
+```
+
+The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.
+
+The lock directory MUST contain `owner.json`:
+
+```json
+{
+  "agent": "codex",
+  "task_id": "TASK-20260530-01",
+  "created_at": "2026-05-30T08:00:00.000Z",
+  "heartbeat_at": "2026-05-30T08:00:00.000Z",
+  "reason": "append event and update state"
+}
+```
 
+The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.
+
+## 9. Failure Recovery
+
+Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.
+
+If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.
+
+If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.
+
+If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.
+
+Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.
+
+## 10. Handoff Rules
+
 When handing work to the other agent:
 
 1. Write or update the task document.
@@ -174,13 +240,13 @@
 
 Handoffs should include concrete next actions, relevant file paths, and any known blockers.
 
-## 10. Completion Rules
+## 11. Completion Rules
 
 A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
 
 Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
 
-## 11. Readiness Signal
+## 12. Readiness Signal
 
 Codex readiness is represented by both:
 
@@ -189,19 +255,21 @@
 
 Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
 
-## 12. Minimal Operating Checklist
+## 13. Minimal Operating Checklist
 
 Before collaboration work:
 
 - Read `AGENTS.md` or `CLAUDE.md`, as applicable.
 - Read `.omc/collaboration/protocol.md`.
 - Inspect `state.json` and recent `events.jsonl` entries.
+- Verify that `.omc/collaboration/` is on a supported filesystem before production testing.
 
 During collaboration work:
 
 - Keep edits scoped to the task.
 - Preserve append-only event history.
 - Keep shared JSON valid.
+- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.
 - Create durable artifacts for decisions that must survive chat context.
 
 After collaboration work:

exec
/bin/bash -lc 'rtk git status --short .omc/collaboration/protocol.md .omc/collaboration/events.jsonl .omc/collaboration/state.json .omc/collaboration/tasks/TASK-20260530-02-implement-p0-amendments.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
?? .omc/collaboration/events.jsonl
?? .omc/collaboration/protocol.md
?? .omc/collaboration/state.json
?? .omc/collaboration/tasks/TASK-20260530-02-implement-p0-amendments.md
exec
/bin/bash -lc 'rtk ls -la .omc/collaboration/locks' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
(empty)

exec
/bin/bash -lc "rtk sed -n '1,80p' .omc/collaboration/tasks/TASK-20260530-01-protocol-critical-review.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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

diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
index a831acc3f4534a3d2c3a48ce4720292ccf968809..c07e6b15a0f90675f8257f004240b0ceca386f80
--- a/.omc/collaboration/protocol.md
+++ b/.omc/collaboration/protocol.md
@@ -1,6 +1,6 @@
 # Claude-Codex Collaboration Protocol
 
-Version: 0.1
+Version: 0.2
 Status: active
 Owner: Claude + Codex
 
@@ -19,9 +19,16 @@
 - `events.jsonl`: append-only event log.
 - `tasks/`: task specifications and task handoff documents.
 - `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
-- `locks/`: advisory lock files for serialized work.
+- `locks/`: lock files or directories for serialized work.
 - `codex-ready.md`: Codex readiness signal.
 
+Filesystem requirements:
+
+- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
+- Local filesystems and NFSv4 are acceptable for this workflow.
+- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
+- Production testing MUST NOT proceed on an unsupported filesystem.
+
 ## 3. Authority And Conflicts
 
 This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
@@ -34,6 +41,8 @@
 
 `state.json` is the latest compact state snapshot. It must remain valid JSON.
 
+`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.
+
 Recommended schema:
 
 ```json
@@ -52,15 +61,23 @@
 - `workflow_id`: stable collaboration workflow identifier.
 - `current_task`: active task id or `null`.
 - `active_agent`: `claude`, `codex`, or `none`.
-- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
 - `last_event_id`: numeric id of the last event written to `events.jsonl`.
 - `updated_at`: UTC ISO-8601 timestamp for the state update.
 
 State updates should be minimal and should not replace durable task or artifact content.
 
+State write rules:
+
+- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
+- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
+- Agents MUST validate the temporary file as well-formed JSON before publishing it.
+- Agents MUST atomically rename the validated temporary file into place with `mv`.
+- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+
 ## 5. Event Log
 
-`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
 
 Required event fields:
 
@@ -83,9 +100,12 @@
 
 Event id rules:
 
-- Start at `1`.
-- Increment by `1` for every new event.
-- After writing an event, update `state.json.last_event_id` to the new id.
+- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
+- New event ids MUST be allocated while holding `locks/journal.lock`.
+- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
+- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
+- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.
 
 Common event types:
 
@@ -121,8 +141,16 @@
 - Acceptance criteria.
 - Current status.
 
-When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+When claiming a task, the agent MUST use this atomic claim procedure:
 
+1. Acquire `locks/journal.lock`.
+2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
+3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
+4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
+5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
+6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
+7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.
+
 ## 7. Artifacts
 
 Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
@@ -139,7 +167,7 @@
 
 ## 8. Locks
 
-Locks are advisory files under `.omc/collaboration/locks/`.
+Locks are files or directories under `.omc/collaboration/locks/`.
 
 Use a lock when two agents might modify the same shared collaboration file at the same time.
 
@@ -162,8 +190,46 @@
 
 Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
 
-## 9. Handoff Rules
+### Required Journal Lock
+
+Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.
+
+Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:
+
+```bash
+mkdir .omc/collaboration/locks/journal.lock
+```
+
+The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.
+
+The lock directory MUST contain `owner.json`:
+
+```json
+{
+  "agent": "codex",
+  "task_id": "TASK-20260530-01",
+  "created_at": "2026-05-30T08:00:00.000Z",
+  "heartbeat_at": "2026-05-30T08:00:00.000Z",
+  "reason": "append event and update state"
+}
+```
 
+The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.
+
+## 9. Failure Recovery
+
+Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.
+
+If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.
+
+If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.
+
+If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.
+
+Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.
+
+## 10. Handoff Rules
+
 When handing work to the other agent:
 
 1. Write or update the task document.
@@ -174,13 +240,13 @@
 
 Handoffs should include concrete next actions, relevant file paths, and any known blockers.
 
-## 10. Completion Rules
+## 11. Completion Rules
 
 A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
 
 Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
 
-## 11. Readiness Signal
+## 12. Readiness Signal
 
 Codex readiness is represented by both:
 
@@ -189,19 +255,21 @@
 
 Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
 
-## 12. Minimal Operating Checklist
+## 13. Minimal Operating Checklist
 
 Before collaboration work:
 
 - Read `AGENTS.md` or `CLAUDE.md`, as applicable.
 - Read `.omc/collaboration/protocol.md`.
 - Inspect `state.json` and recent `events.jsonl` entries.
+- Verify that `.omc/collaboration/` is on a supported filesystem before production testing.
 
 During collaboration work:
 
 - Keep edits scoped to the task.
 - Preserve append-only event history.
 - Keep shared JSON valid.
+- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.
 - Create durable artifacts for decisions that must survive chat context.
 
 After collaboration work:

codex
验证脚本已覆盖 7 个 P0 点，并确认没有加入 YAML front matter、transition table、30/60 分钟任务超时规则。现在我会按新锁规则写入 `completed` 事件并把 `state.json` 收尾为 `completed`。
exec
/bin/bash -lc 'rtk mkdir .omc/collaboration/locks/journal.lock' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
index a831acc3f4534a3d2c3a48ce4720292ccf968809..c07e6b15a0f90675f8257f004240b0ceca386f80
--- a/.omc/collaboration/protocol.md
+++ b/.omc/collaboration/protocol.md
@@ -1,6 +1,6 @@
 # Claude-Codex Collaboration Protocol
 
-Version: 0.1
+Version: 0.2
 Status: active
 Owner: Claude + Codex
 
@@ -19,9 +19,16 @@
 - `events.jsonl`: append-only event log.
 - `tasks/`: task specifications and task handoff documents.
 - `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
-- `locks/`: advisory lock files for serialized work.
+- `locks/`: lock files or directories for serialized work.
 - `codex-ready.md`: Codex readiness signal.
 
+Filesystem requirements:
+
+- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
+- Local filesystems and NFSv4 are acceptable for this workflow.
+- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
+- Production testing MUST NOT proceed on an unsupported filesystem.
+
 ## 3. Authority And Conflicts
 
 This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
@@ -34,6 +41,8 @@
 
 `state.json` is the latest compact state snapshot. It must remain valid JSON.
 
+`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.
+
 Recommended schema:
 
 ```json
@@ -52,15 +61,23 @@
 - `workflow_id`: stable collaboration workflow identifier.
 - `current_task`: active task id or `null`.
 - `active_agent`: `claude`, `codex`, or `none`.
-- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
 - `last_event_id`: numeric id of the last event written to `events.jsonl`.
 - `updated_at`: UTC ISO-8601 timestamp for the state update.
 
 State updates should be minimal and should not replace durable task or artifact content.
 
+State write rules:
+
+- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
+- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
+- Agents MUST validate the temporary file as well-formed JSON before publishing it.
+- Agents MUST atomically rename the validated temporary file into place with `mv`.
+- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+
 ## 5. Event Log
 
-`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
 
 Required event fields:
 
@@ -83,9 +100,12 @@
 
 Event id rules:
 
-- Start at `1`.
-- Increment by `1` for every new event.
-- After writing an event, update `state.json.last_event_id` to the new id.
+- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
+- New event ids MUST be allocated while holding `locks/journal.lock`.
+- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
+- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
+- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.
 
 Common event types:
 
@@ -121,8 +141,16 @@
 - Acceptance criteria.
 - Current status.
 
-When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+When claiming a task, the agent MUST use this atomic claim procedure:
 
+1. Acquire `locks/journal.lock`.
+2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
+3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
+4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
+5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
+6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
+7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.
+
 ## 7. Artifacts
 
 Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
@@ -139,7 +167,7 @@
 
 ## 8. Locks
 
-Locks are advisory files under `.omc/collaboration/locks/`.
+Locks are files or directories under `.omc/collaboration/locks/`.
 
 Use a lock when two agents might modify the same shared collaboration file at the same time.
 
@@ -162,8 +190,46 @@
 
 Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
 
-## 9. Handoff Rules
+### Required Journal Lock
+
+Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.
+
+Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:
+
+```bash
+mkdir .omc/collaboration/locks/journal.lock
+```
+
+The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.
+
+The lock directory MUST contain `owner.json`:
+
+```json
+{
+  "agent": "codex",
+  "task_id": "TASK-20260530-01",
+  "created_at": "2026-05-30T08:00:00.000Z",
+  "heartbeat_at": "2026-05-30T08:00:00.000Z",
+  "reason": "append event and update state"
+}
+```
 
+The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.
+
+## 9. Failure Recovery
+
+Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.
+
+If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.
+
+If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.
+
+If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.
+
+Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.
+
+## 10. Handoff Rules
+
 When handing work to the other agent:
 
 1. Write or update the task document.
@@ -174,13 +240,13 @@
 
 Handoffs should include concrete next actions, relevant file paths, and any known blockers.
 
-## 10. Completion Rules
+## 11. Completion Rules
 
 A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
 
 Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
 
-## 11. Readiness Signal
+## 12. Readiness Signal
 
 Codex readiness is represented by both:
 
@@ -189,19 +255,21 @@
 
 Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
 
-## 12. Minimal Operating Checklist
+## 13. Minimal Operating Checklist
 
 Before collaboration work:
 
 - Read `AGENTS.md` or `CLAUDE.md`, as applicable.
 - Read `.omc/collaboration/protocol.md`.
 - Inspect `state.json` and recent `events.jsonl` entries.
+- Verify that `.omc/collaboration/` is on a supported filesystem before production testing.
 
 During collaboration work:
 
 - Keep edits scoped to the task.
 - Preserve append-only event history.
 - Keep shared JSON valid.
+- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.
 - Create durable artifacts for decisions that must survive chat context.
 
 After collaboration work:

exec
/bin/bash -lc "rtk python3 - <<'PY'
import json, os
from datetime import datetime, timezone
from pathlib import Path

base = Path('.omc/collaboration')
lock = base / 'locks' / 'journal.lock'
agent = 'codex'
task_id = 'TASK-20260530-02'
now = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
owner = {
    'agent': agent,
    'task_id': task_id,
    'created_at': now,
    'heartbeat_at': now,
    'reason': 'complete task and update state'
}
(lock / 'owner.json').write_text(json.dumps(owner, indent=2) + '\\n', encoding='utf-8')

events_path = base / 'events.jsonl'
state_path = base / 'state.json'

events = []
for lineno, line in enumerate(events_path.read_text(encoding='utf-8').splitlines(), 1):
    if not line.strip():
        continue
    try:
        events.append(json.loads(line))
    except json.JSONDecodeError as exc:
        raise SystemExit(f'malformed events.jsonl line {lineno}: {exc}')
ids = [e['id'] for e in events]
if len(ids) "'!= len(set(ids)):
    raise SystemExit('"'duplicate event ids detected')

next_id = max(ids, default=0) + 1
event = {
    'id': next_id,
    'type': 'completed',
    'agent': agent,
    'timestamp': now,
    'summary': 'Completed P0 protocol amendments and verified protocol contents.',
    'task_id': task_id,
    'artifacts': ['.omc/collaboration/protocol.md'],
    'status': 'completed',
    'details': {
        'version': '0.2',
        'p0_items_integrated': 7,
        'p1_items_deferred': ['state machine', 'timeout', 'YAML front matter']
    }
}
with events_path.open('a', encoding='utf-8') as f:
    f.write(json.dumps(event, separators=(',', ':')) + '\\n')

state = json.loads(state_path.read_text(encoding='utf-8'))
state.update({
    'current_task': task_id,
    'active_agent': 'none',
    'status': 'completed',
    'last_event_id': next_id,
    'updated_at': now
})
tmp_path = base / f'state.json.tmp.{agent}'
tmp_path.write_text(json.dumps(state, indent=2) + '\\n', encoding='utf-8')
json.loads(tmp_path.read_text(encoding='utf-8'))
os.replace(tmp_path, state_path)

written_events = [json.loads(line) for line in events_path.read_text(encoding='utf-8').splitlines() if line.strip()]
written_ids = [e['id'] for e in written_events]
if len(written_ids) "'!= len(set(written_ids)):
    raise SystemExit('"'duplicate event ids after append')
written_state = json.loads(state_path.read_text(encoding='utf-8'))
if written_state.get('last_event_id') "'!= max(written_ids):
    raise SystemExit('"'state last_event_id mismatch after append')
if written_state.get('status') "'!= '"'completed':
    raise SystemExit('state status mismatch after completion')

(lock / 'owner.json').unlink()
lock.rmdir()
PY" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
index a831acc3f4534a3d2c3a48ce4720292ccf968809..c07e6b15a0f90675f8257f004240b0ceca386f80
--- a/.omc/collaboration/protocol.md
+++ b/.omc/collaboration/protocol.md
@@ -1,6 +1,6 @@
 # Claude-Codex Collaboration Protocol
 
-Version: 0.1
+Version: 0.2
 Status: active
 Owner: Claude + Codex
 
@@ -19,9 +19,16 @@
 - `events.jsonl`: append-only event log.
 - `tasks/`: task specifications and task handoff documents.
 - `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
-- `locks/`: advisory lock files for serialized work.
+- `locks/`: lock files or directories for serialized work.
 - `codex-ready.md`: Codex readiness signal.
 
+Filesystem requirements:
+
+- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
+- Local filesystems and NFSv4 are acceptable for this workflow.
+- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
+- Production testing MUST NOT proceed on an unsupported filesystem.
+
 ## 3. Authority And Conflicts
 
 This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
@@ -34,6 +41,8 @@
 
 `state.json` is the latest compact state snapshot. It must remain valid JSON.
 
+`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.
+
 Recommended schema:
 
 ```json
@@ -52,15 +61,23 @@
 - `workflow_id`: stable collaboration workflow identifier.
 - `current_task`: active task id or `null`.
 - `active_agent`: `claude`, `codex`, or `none`.
-- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
 - `last_event_id`: numeric id of the last event written to `events.jsonl`.
 - `updated_at`: UTC ISO-8601 timestamp for the state update.
 
 State updates should be minimal and should not replace durable task or artifact content.
 
+State write rules:
+
+- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
+- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
+- Agents MUST validate the temporary file as well-formed JSON before publishing it.
+- Agents MUST atomically rename the validated temporary file into place with `mv`.
+- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+
 ## 5. Event Log
 
-`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
 
 Required event fields:
 
@@ -83,9 +100,12 @@
 
 Event id rules:
 
-- Start at `1`.
-- Increment by `1` for every new event.
-- After writing an event, update `state.json.last_event_id` to the new id.
+- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
+- New event ids MUST be allocated while holding `locks/journal.lock`.
+- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
+- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
+- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.
 
 Common event types:
 
@@ -121,8 +141,16 @@
 - Acceptance criteria.
 - Current status.
 
-When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+When claiming a task, the agent MUST use this atomic claim procedure:
 
+1. Acquire `locks/journal.lock`.
+2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
+3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
+4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
+5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
+6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
+7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.
+
 ## 7. Artifacts
 
 Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
@@ -139,7 +167,7 @@
 
 ## 8. Locks
 
-Locks are advisory files under `.omc/collaboration/locks/`.
+Locks are files or directories under `.omc/collaboration/locks/`.
 
 Use a lock when two agents might modify the same shared collaboration file at the same time.
 
@@ -162,8 +190,46 @@
 
 Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
 
-## 9. Handoff Rules
+### Required Journal Lock
+
+Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.
+
+Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:
+
+```bash
+mkdir .omc/collaboration/locks/journal.lock
+```
+
+The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.
+
+The lock directory MUST contain `owner.json`:
+
+```json
+{
+  "agent": "codex",
+  "task_id": "TASK-20260530-01",
+  "created_at": "2026-05-30T08:00:00.000Z",
+  "heartbeat_at": "2026-05-30T08:00:00.000Z",
+  "reason": "append event and update state"
+}
+```
 
+The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.
+
+## 9. Failure Recovery
+
+Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.
+
+If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.
+
+If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.
+
+If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.
+
+Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.
+
+## 10. Handoff Rules
+
 When handing work to the other agent:
 
 1. Write or update the task document.
@@ -174,13 +240,13 @@
 
 Handoffs should include concrete next actions, relevant file paths, and any known blockers.
 
-## 10. Completion Rules
+## 11. Completion Rules
 
 A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
 
 Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
 
-## 11. Readiness Signal
+## 12. Readiness Signal
 
 Codex readiness is represented by both:
 
@@ -189,19 +255,21 @@
 
 Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
 
-## 12. Minimal Operating Checklist
+## 13. Minimal Operating Checklist
 
 Before collaboration work:
 
 - Read `AGENTS.md` or `CLAUDE.md`, as applicable.
 - Read `.omc/collaboration/protocol.md`.
 - Inspect `state.json` and recent `events.jsonl` entries.
+- Verify that `.omc/collaboration/` is on a supported filesystem before production testing.
 
 During collaboration work:
 
 - Keep edits scoped to the task.
 - Preserve append-only event history.
 - Keep shared JSON valid.
+- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.
 - Create durable artifacts for decisions that must survive chat context.
 
 After collaboration work:

exec
/bin/bash -lc 'rtk ls -la .omc/collaboration/locks' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
(empty)

exec
/bin/bash -lc 'rtk tail -n 5 .omc/collaboration/events.jsonl' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{"id":6,"type":"review_response","agent":"codex","timestamp":"2026-05-30T08:11:56.000Z","summary":"Codex responded to Claude's second-round protocol review questions and agreed on adjusted P0/P1 priorities.","task_id":"TASK-20260530-01","artifacts":[".omc/collaboration/artifacts/20260530-1611-codex-second-response-to-claude.md"],"status":"waiting"}
{"id":7,"type":"consensus_reached","agent":"claude","timestamp":"2026-05-30T08:14:30.000Z","summary":"Claude and Codex reached consensus on protocol amendments after 2-round iterative review.","task_id":"TASK-20260530-01","artifacts":[".omc/collaboration/artifacts/20260530-0814-protocol-review-consensus.md"],"status":"completed"}
{"id":8,"type":"task_created","agent":"claude","timestamp":"2026-05-30T08:15:00.000Z","summary":"Created P0 protocol amendment implementation task for Codex.","task_id":"TASK-20260530-02","artifacts":[".omc/collaboration/tasks/TASK-20260530-02-implement-p0-amendments.md"],"status":"task_open"}
{"id":9,"type":"task_claimed","agent":"codex","timestamp":"2026-05-30T08:18:38.469Z","summary":"Codex claimed P0 protocol amendment implementation task.","task_id":"TASK-20260530-02","status":"in_progress"}
{"id":10,"type":"completed","agent":"codex","timestamp":"2026-05-30T08:20:59.862Z","summary":"Completed P0 protocol amendments and verified protocol contents.","task_id":"TASK-20260530-02","artifacts":[".omc/collaboration/protocol.md"],"status":"completed","details":{"version":"0.2","p0_items_integrated":7,"p1_items_deferred":["state machine","timeout","YAML front matter"]}}

exec
/bin/bash -lc 'rtk cat .omc/collaboration/state.json' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{
  "workflow_id": "claude-codex-collab-mvp",
  "current_task": "TASK-20260530-02",
  "active_agent": "none",
  "status": "completed",
  "last_event_id": 10,
  "updated_at": "2026-05-30T08:20:59.862Z"
}

exec
/bin/bash -lc "rtk python3 - <<'PY'
import json
from pathlib import Path
base = Path('.omc/collaboration')
state = json.loads((base / 'state.json').read_text(encoding='utf-8'))
ids = []
for i, line in enumerate((base / 'events.jsonl').read_text(encoding='utf-8').splitlines(), 1):
    if not line.strip():
        continue
    event = json.loads(line)
    ids.append(event['id'])
protocol = (base / 'protocol.md').read_text(encoding='utf-8')
checks = {
    'version_0_2': 'Version: 0.2' in protocol,
    'events_authoritative': 'source of truth' in protocol and 'rebuildable cache' in protocol,
    'journal_lock': 'journal.lock' in protocol and 'owner.json' in protocol,
    'event_id_from_log': 'max(event.id) + 1' in protocol and 'MUST NOT allocate event ids from "'`state.json.last_event_id`'"' in protocol,
    'needs_repair': 'needs_repair' in protocol and 'Failure Recovery' in protocol,
    'atomic_claim': 'atomic claim procedure' in protocol and 'active owner' in protocol,
    'atomic_state_write': 'state.json.tmp.<agent>' in protocol and 'atomically rename' in protocol,
    'filesystem': 'atomic "'`mkdir` semantics'"' in protocol and 'NFSv2' in protocol and 'NFSv3' in protocol,
    'no_yaml_front_matter': 'YAML front matter' not in protocol,
    'no_transition_table': 'transition table' not in protocol,
    'no_task_timeout_rules': '60 minutes' not in protocol and '30 minutes' not in protocol and '60-minute' not in protocol and '30-minute' not in protocol,
    'events_no_duplicates': len(ids) == len(set(ids)),
    'state_last_event_matches': state.get('last_event_id') == max(ids),
    'state_completed': state.get('status') == 'completed',
}
for key, value in checks.items():
    print(f'{key}: {value}')
if not all(checks.values()):
    raise SystemExit(1)
print(f'events={len(ids)} max_id={max(ids)} state_status={state.get(\"status\")}')
PY" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
version_0_2: True
events_authoritative: True
journal_lock: True
event_id_from_log: True
needs_repair: True
atomic_claim: True
atomic_state_write: True
filesystem: True
no_yaml_front_matter: True
no_transition_table: True
no_task_timeout_rules: True
events_no_duplicates: True
state_last_event_matches: True
state_completed: True
events=10 max_id=10 state_status=completed

diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
index a831acc3f4534a3d2c3a48ce4720292ccf968809..c07e6b15a0f90675f8257f004240b0ceca386f80
--- a/.omc/collaboration/protocol.md
+++ b/.omc/collaboration/protocol.md
@@ -1,6 +1,6 @@
 # Claude-Codex Collaboration Protocol
 
-Version: 0.1
+Version: 0.2
 Status: active
 Owner: Claude + Codex
 
@@ -19,9 +19,16 @@
 - `events.jsonl`: append-only event log.
 - `tasks/`: task specifications and task handoff documents.
 - `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
-- `locks/`: advisory lock files for serialized work.
+- `locks/`: lock files or directories for serialized work.
 - `codex-ready.md`: Codex readiness signal.
 
+Filesystem requirements:
+
+- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
+- Local filesystems and NFSv4 are acceptable for this workflow.
+- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
+- Production testing MUST NOT proceed on an unsupported filesystem.
+
 ## 3. Authority And Conflicts
 
 This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
@@ -34,6 +41,8 @@
 
 `state.json` is the latest compact state snapshot. It must remain valid JSON.
 
+`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.
+
 Recommended schema:
 
 ```json
@@ -52,15 +61,23 @@
 - `workflow_id`: stable collaboration workflow identifier.
 - `current_task`: active task id or `null`.
 - `active_agent`: `claude`, `codex`, or `none`.
-- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
 - `last_event_id`: numeric id of the last event written to `events.jsonl`.
 - `updated_at`: UTC ISO-8601 timestamp for the state update.
 
 State updates should be minimal and should not replace durable task or artifact content.
 
+State write rules:
+
+- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
+- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
+- Agents MUST validate the temporary file as well-formed JSON before publishing it.
+- Agents MUST atomically rename the validated temporary file into place with `mv`.
+- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+
 ## 5. Event Log
 
-`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
 
 Required event fields:
 
@@ -83,9 +100,12 @@
 
 Event id rules:
 
-- Start at `1`.
-- Increment by `1` for every new event.
-- After writing an event, update `state.json.last_event_id` to the new id.
+- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
+- New event ids MUST be allocated while holding `locks/journal.lock`.
+- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
+- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
+- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.
 
 Common event types:
 
@@ -121,8 +141,16 @@
 - Acceptance criteria.
 - Current status.
 
-When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+When claiming a task, the agent MUST use this atomic claim procedure:
 
+1. Acquire `locks/journal.lock`.
+2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
+3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
+4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
+5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
+6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
+7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.
+
 ## 7. Artifacts
 
 Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
@@ -139,7 +167,7 @@
 
 ## 8. Locks
 
-Locks are advisory files under `.omc/collaboration/locks/`.
+Locks are files or directories under `.omc/collaboration/locks/`.
 
 Use a lock when two agents might modify the same shared collaboration file at the same time.
 
@@ -162,8 +190,46 @@
 
 Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
 
-## 9. Handoff Rules
+### Required Journal Lock
+
+Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.
+
+Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:
+
+```bash
+mkdir .omc/collaboration/locks/journal.lock
+```
+
+The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.
+
+The lock directory MUST contain `owner.json`:
+
+```json
+{
+  "agent": "codex",
+  "task_id": "TASK-20260530-01",
+  "created_at": "2026-05-30T08:00:00.000Z",
+  "heartbeat_at": "2026-05-30T08:00:00.000Z",
+  "reason": "append event and update state"
+}
+```
 
+The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.
+
+## 9. Failure Recovery
+
+Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.
+
+If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.
+
+If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.
+
+If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.
+
+Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.
+
+## 10. Handoff Rules
+
 When handing work to the other agent:
 
 1. Write or update the task document.
@@ -174,13 +240,13 @@
 
 Handoffs should include concrete next actions, relevant file paths, and any known blockers.
 
-## 10. Completion Rules
+## 11. Completion Rules
 
 A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
 
 Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
 
-## 11. Readiness Signal
+## 12. Readiness Signal
 
 Codex readiness is represented by both:
 
@@ -189,19 +255,21 @@
 
 Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
 
-## 12. Minimal Operating Checklist
+## 13. Minimal Operating Checklist
 
 Before collaboration work:
 
 - Read `AGENTS.md` or `CLAUDE.md`, as applicable.
 - Read `.omc/collaboration/protocol.md`.
 - Inspect `state.json` and recent `events.jsonl` entries.
+- Verify that `.omc/collaboration/` is on a supported filesystem before production testing.
 
 During collaboration work:
 
 - Keep edits scoped to the task.
 - Preserve append-only event history.
 - Keep shared JSON valid.
+- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.
 - Create durable artifacts for decisions that must survive chat context.
 
 After collaboration work:

exec
/bin/bash -lc 'rtk nl -ba .omc/collaboration/protocol.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# Claude-Codex Collaboration Protocol
     2	
     3	Version: 0.2
     4	Status: active
     5	Owner: Claude + Codex
     6	
     7	## 1. Purpose
     8	
     9	This protocol defines the shared operating contract for Claude-Codex collaboration in this repository. It covers task handoff, shared state, event logging, artifact creation, lock usage, and completion signaling.
    10	
    11	Agents must read this file before participating in the collaboration workflow.
    12	
    13	## 2. Directory Layout
    14	
    15	All collaboration files live under `.omc/collaboration/`.
    16	
    17	- `protocol.md`: this protocol.
    18	- `state.json`: current shared workflow state.
    19	- `events.jsonl`: append-only event log.
    20	- `tasks/`: task specifications and task handoff documents.
    21	- `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
    22	- `locks/`: lock files or directories for serialized work.
    23	- `codex-ready.md`: Codex readiness signal.
    24	
    25	Filesystem requirements:
    26	
    27	- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
    28	- Local filesystems and NFSv4 are acceptable for this workflow.
    29	- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
    30	- Production testing MUST NOT proceed on an unsupported filesystem.
    31	
    32	## 3. Authority And Conflicts
    33	
    34	This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
    35	
    36	If a conflict is encountered, the active agent must follow the higher-priority instruction and record the conflict in its response or task artifact when material to the collaboration.
    37	
    38	Codex-specific repository rules in `AGENTS.md` remain mandatory. Claude-specific repository rules in `CLAUDE.md` remain mandatory.
    39	
    40	## 4. Shared State
    41	
    42	`state.json` is the latest compact state snapshot. It must remain valid JSON.
    43	
    44	`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.
    45	
    46	Recommended schema:
    47	
    48	```json
    49	{
    50	  "workflow_id": "claude-codex-collab-mvp",
    51	  "current_task": null,
    52	  "active_agent": "none",
    53	  "status": "initialized",
    54	  "last_event_id": 0,
    55	  "updated_at": "2026-05-30T00:00:00.000Z"
    56	}
    57	```
    58	
    59	Field meanings:
    60	
    61	- `workflow_id`: stable collaboration workflow identifier.
    62	- `current_task`: active task id or `null`.
    63	- `active_agent`: `claude`, `codex`, or `none`.
    64	- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
    65	- `last_event_id`: numeric id of the last event written to `events.jsonl`.
    66	- `updated_at`: UTC ISO-8601 timestamp for the state update.
    67	
    68	State updates should be minimal and should not replace durable task or artifact content.
    69	
    70	State write rules:
    71	
    72	- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
    73	- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
    74	- Agents MUST validate the temporary file as well-formed JSON before publishing it.
    75	- Agents MUST atomically rename the validated temporary file into place with `mv`.
    76	- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
    77	
    78	## 5. Event Log
    79	
    80	`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
    81	
    82	Required event fields:
    83	
    84	```json
    85	{
    86	  "id": 1,
    87	  "type": "codex_ready",
    88	  "agent": "codex",
    89	  "timestamp": "2026-05-30T00:00:00.000Z",
    90	  "summary": "Short event summary."
    91	}
    92	```
    93	
    94	Recommended optional fields:
    95	
    96	- `task_id`: related task id.
    97	- `artifacts`: array of artifact paths.
    98	- `status`: resulting workflow status.
    99	- `details`: compact structured metadata.
   100	
   101	Event id rules:
   102	
   103	- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
   104	- New event ids MUST be allocated while holding `locks/journal.lock`.
   105	- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
   106	- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
   107	- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
   108	- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.
   109	
   110	Common event types:
   111	
   112	- `claude_ready`
   113	- `codex_ready`
   114	- `task_created`
   115	- `task_claimed`
   116	- `artifact_created`
   117	- `handoff_requested`
   118	- `review_requested`
   119	- `blocked`
   120	- `completed`
   121	
   122	## 6. Tasks
   123	
   124	Task documents belong in `.omc/collaboration/tasks/`.
   125	
   126	Recommended task filename:
   127	
   128	```text
   129	TASK-YYYYMMDD-NN-short-name.md
   130	```
   131	
   132	Recommended task content:
   133	
   134	- Task id.
   135	- Owner or requesting agent.
   136	- Objective.
   137	- Scope.
   138	- Inputs and relevant files.
   139	- Expected outputs.
   140	- Constraints and mandatory rules.
   141	- Acceptance criteria.
   142	- Current status.
   143	
   144	When claiming a task, the agent MUST use this atomic claim procedure:
   145	
   146	1. Acquire `locks/journal.lock`.
   147	2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
   148	3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
   149	4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
   150	5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
   151	6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
   152	7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.
   153	
   154	## 7. Artifacts
   155	
   156	Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
   157	
   158	Artifacts should be durable and self-contained enough for the other agent to continue work without relying on chat history.
   159	
   160	Recommended artifact filenames:
   161	
   162	```text
   163	YYYYMMDD-HHMM-agent-topic.md
   164	```
   165	
   166	For formal Codex review or OMC `/ask codex` workflows, the repository's `docs/codex-review-protocol.md` remains mandatory and takes precedence over this generic artifact convention.
   167	
   168	## 8. Locks
   169	
   170	Locks are files or directories under `.omc/collaboration/locks/`.
   171	
   172	Use a lock when two agents might modify the same shared collaboration file at the same time.
   173	
   174	Recommended lock filename:
   175	
   176	```text
   177	resource-name.lock
   178	```
   179	
   180	Recommended lock content:
   181	
   182	```json
   183	{
   184	  "agent": "codex",
   185	  "resource": "state.json",
   186	  "created_at": "2026-05-30T00:00:00.000Z",
   187	  "reason": "Updating state after event append."
   188	}
   189	```
   190	
   191	Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
   192	
   193	### Required Journal Lock
   194	
   195	Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.
   196	
   197	Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:
   198	
   199	```bash
   200	mkdir .omc/collaboration/locks/journal.lock
   201	```
   202	
   203	The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.
   204	
   205	The lock directory MUST contain `owner.json`:
   206	
   207	```json
   208	{
   209	  "agent": "codex",
   210	  "task_id": "TASK-20260530-01",
   211	  "created_at": "2026-05-30T08:00:00.000Z",
   212	  "heartbeat_at": "2026-05-30T08:00:00.000Z",
   213	  "reason": "append event and update state"
   214	}
   215	```
   216	
   217	The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.
   218	
   219	## 9. Failure Recovery
   220	
   221	Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.
   222	
   223	If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.
   224	
   225	If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.
   226	
   227	If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.
   228	
   229	Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.
   230	
   231	## 10. Handoff Rules
   232	
   233	When handing work to the other agent:
   234	
   235	1. Write or update the task document.
   236	2. Write any supporting artifact needed for context.
   237	3. Append a `handoff_requested` event.
   238	4. Update `state.json` with the current task, status, active agent, and last event id.
   239	5. State the handoff clearly in the user-facing response when applicable.
   240	
   241	Handoffs should include concrete next actions, relevant file paths, and any known blockers.
   242	
   243	## 11. Completion Rules
   244	
   245	A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
   246	
   247	Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
   248	
   249	## 12. Readiness Signal
   250	
   251	Codex readiness is represented by both:
   252	
   253	- A `codex_ready` event in `events.jsonl`.
   254	- `.omc/collaboration/codex-ready.md`.
   255	
   256	Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
   257	
   258	## 13. Minimal Operating Checklist
   259	
   260	Before collaboration work:
   261	
   262	- Read `AGENTS.md` or `CLAUDE.md`, as applicable.
   263	- Read `.omc/collaboration/protocol.md`.
   264	- Inspect `state.json` and recent `events.jsonl` entries.
   265	- Verify that `.omc/collaboration/` is on a supported filesystem before production testing.
   266	
   267	During collaboration work:
   268	
   269	- Keep edits scoped to the task.
   270	- Preserve append-only event history.
   271	- Keep shared JSON valid.
   272	- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.
   273	- Create durable artifacts for decisions that must survive chat context.
   274	
   275	After collaboration work:
   276	
   277	- Append the relevant event.
   278	- Update `state.json`.
   279	- Verify changed files.
   280	- Report completed items and any remaining risk.

diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
index a831acc3f4534a3d2c3a48ce4720292ccf968809..c07e6b15a0f90675f8257f004240b0ceca386f80
--- a/.omc/collaboration/protocol.md
+++ b/.omc/collaboration/protocol.md
@@ -1,6 +1,6 @@
 # Claude-Codex Collaboration Protocol
 
-Version: 0.1
+Version: 0.2
 Status: active
 Owner: Claude + Codex
 
@@ -19,9 +19,16 @@
 - `events.jsonl`: append-only event log.
 - `tasks/`: task specifications and task handoff documents.
 - `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
-- `locks/`: advisory lock files for serialized work.
+- `locks/`: lock files or directories for serialized work.
 - `codex-ready.md`: Codex readiness signal.
 
+Filesystem requirements:
+
+- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
+- Local filesystems and NFSv4 are acceptable for this workflow.
+- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
+- Production testing MUST NOT proceed on an unsupported filesystem.
+
 ## 3. Authority And Conflicts
 
 This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
@@ -34,6 +41,8 @@
 
 `state.json` is the latest compact state snapshot. It must remain valid JSON.
 
+`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.
+
 Recommended schema:
 
 ```json
@@ -52,15 +61,23 @@
 - `workflow_id`: stable collaboration workflow identifier.
 - `current_task`: active task id or `null`.
 - `active_agent`: `claude`, `codex`, or `none`.
-- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
 - `last_event_id`: numeric id of the last event written to `events.jsonl`.
 - `updated_at`: UTC ISO-8601 timestamp for the state update.
 
 State updates should be minimal and should not replace durable task or artifact content.
 
+State write rules:
+
+- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
+- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
+- Agents MUST validate the temporary file as well-formed JSON before publishing it.
+- Agents MUST atomically rename the validated temporary file into place with `mv`.
+- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+
 ## 5. Event Log
 
-`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
 
 Required event fields:
 
@@ -83,9 +100,12 @@
 
 Event id rules:
 
-- Start at `1`.
-- Increment by `1` for every new event.
-- After writing an event, update `state.json.last_event_id` to the new id.
+- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
+- New event ids MUST be allocated while holding `locks/journal.lock`.
+- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
+- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
+- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.
 
 Common event types:
 
@@ -121,8 +141,16 @@
 - Acceptance criteria.
 - Current status.
 
-When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+When claiming a task, the agent MUST use this atomic claim procedure:
 
+1. Acquire `locks/journal.lock`.
+2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
+3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
+4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
+5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
+6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
+7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.
+
 ## 7. Artifacts
 
 Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
@@ -139,7 +167,7 @@
 
 ## 8. Locks
 
-Locks are advisory files under `.omc/collaboration/locks/`.
+Locks are files or directories under `.omc/collaboration/locks/`.
 
 Use a lock when two agents might modify the same shared collaboration file at the same time.
 
@@ -162,8 +190,46 @@
 
 Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
 
-## 9. Handoff Rules
+### Required Journal Lock
+
+Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.
+
+Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:
+
+```bash
+mkdir .omc/collaboration/locks/journal.lock
+```
+
+The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.
+
+The lock directory MUST contain `owner.json`:
+
+```json
+{
+  "agent": "codex",
+  "task_id": "TASK-20260530-01",
+  "created_at": "2026-05-30T08:00:00.000Z",
+  "heartbeat_at": "2026-05-30T08:00:00.000Z",
+  "reason": "append event and update state"
+}
+```
 
+The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.
+
+## 9. Failure Recovery
+
+Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.
+
+If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.
+
+If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.
+
+If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.
+
+Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.
+
+## 10. Handoff Rules
+
 When handing work to the other agent:
 
 1. Write or update the task document.
@@ -174,13 +240,13 @@
 
 Handoffs should include concrete next actions, relevant file paths, and any known blockers.
 
-## 10. Completion Rules
+## 11. Completion Rules
 
 A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
 
 Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
 
-## 11. Readiness Signal
+## 12. Readiness Signal
 
 Codex readiness is represented by both:
 
@@ -189,19 +255,21 @@
 
 Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
 
-## 12. Minimal Operating Checklist
+## 13. Minimal Operating Checklist
 
 Before collaboration work:
 
 - Read `AGENTS.md` or `CLAUDE.md`, as applicable.
 - Read `.omc/collaboration/protocol.md`.
 - Inspect `state.json` and recent `events.jsonl` entries.
+- Verify that `.omc/collaboration/` is on a supported filesystem before production testing.
 
 During collaboration work:
 
 - Keep edits scoped to the task.
 - Preserve append-only event history.
 - Keep shared JSON valid.
+- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.
 - Create durable artifacts for decisions that must survive chat context.
 
 After collaboration work:

codex
已完成任务。

更新内容：
- [protocol.md](/home/caohui/projects/graduation-leave-system/.omc/collaboration/protocol.md:3) 版本已升到 `0.2`
- 集成了 7 个 P0 项：`events.jsonl` authoritative、required `journal.lock`、事件 ID 从日志分配、`needs_repair`、atomic task claim、atomic `state.json` 写入、filesystem 要求
- 未加入 P1 项：没有 YAML front matter 要求、没有状态机表、没有 30/60 分钟任务超时规则

协作日志也已按协议更新：
- `events.jsonl` 追加了 `id=9 task_claimed`
- `events.jsonl` 追加了 `id=10 completed`
- [state.json](/home/caohui/projects/graduation-leave-system/.omc/collaboration/state.json:1) 已更新为 `status: completed`，`last_event_id: 10`，`active_agent: none`

验证通过：协议 7 个 P0 检查全为 true，事件日志 JSONL 可解析、无重复 ID，`state.json.last_event_id` 与最大事件 ID 一致，锁目录已清空。
diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
index a831acc3f4534a3d2c3a48ce4720292ccf968809..c07e6b15a0f90675f8257f004240b0ceca386f80
--- a/.omc/collaboration/protocol.md
+++ b/.omc/collaboration/protocol.md
@@ -1,6 +1,6 @@
 # Claude-Codex Collaboration Protocol
 
-Version: 0.1
+Version: 0.2
 Status: active
 Owner: Claude + Codex
 
@@ -19,9 +19,16 @@
 - `events.jsonl`: append-only event log.
 - `tasks/`: task specifications and task handoff documents.
 - `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
-- `locks/`: advisory lock files for serialized work.
+- `locks/`: lock files or directories for serialized work.
 - `codex-ready.md`: Codex readiness signal.
 
+Filesystem requirements:
+
+- `.omc/collaboration/` MUST live on a filesystem that provides atomic `mkdir` semantics for lock acquisition.
+- Local filesystems and NFSv4 are acceptable for this workflow.
+- NFSv2, NFSv3, and mounts with weak cache consistency are unsupported.
+- Production testing MUST NOT proceed on an unsupported filesystem.
+
 ## 3. Authority And Conflicts
 
 This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
@@ -34,6 +41,8 @@
 
 `state.json` is the latest compact state snapshot. It must remain valid JSON.
 
+`events.jsonl` is the authoritative workflow record. `state.json` is a rebuildable cache derived from the event log. Agents MUST NOT treat `state.json` as more authoritative than `events.jsonl`.
+
 Recommended schema:
 
 ```json
@@ -52,15 +61,23 @@
 - `workflow_id`: stable collaboration workflow identifier.
 - `current_task`: active task id or `null`.
 - `active_agent`: `claude`, `codex`, or `none`.
-- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `needs_repair`, `completed`.
 - `last_event_id`: numeric id of the last event written to `events.jsonl`.
 - `updated_at`: UTC ISO-8601 timestamp for the state update.
 
 State updates should be minimal and should not replace durable task or artifact content.
 
+State write rules:
+
+- Any operation that writes `state.json` MUST hold `locks/journal.lock`.
+- Agents MUST write state updates to `.omc/collaboration/state.json.tmp.<agent>`.
+- Agents MUST validate the temporary file as well-formed JSON before publishing it.
+- Agents MUST atomically rename the validated temporary file into place with `mv`.
+- After any event append, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+
 ## 5. Event Log
 
-`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+`events.jsonl` is append-only and is the source of truth for workflow state and event ordering. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
 
 Required event fields:
 
@@ -83,9 +100,12 @@
 
 Event id rules:
 
-- Start at `1`.
-- Increment by `1` for every new event.
-- After writing an event, update `state.json.last_event_id` to the new id.
+- Numeric `id` starts at `1` and SHOULD normally increment by `1`.
+- New event ids MUST be allocated while holding `locks/journal.lock`.
+- The next id MUST be computed as `max(event.id) + 1` from the valid events already present in `events.jsonl`.
+- Agents MUST NOT allocate event ids from `state.json.last_event_id`.
+- After appending an event, `state.json.last_event_id` MUST equal the maximum event id in `events.jsonl`.
+- If duplicate ids or malformed JSONL lines are detected, the agent MUST stop normal collaboration processing and follow the Failure Recovery rules.
 
 Common event types:
 
@@ -121,8 +141,16 @@
 - Acceptance criteria.
 - Current status.
 
-When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+When claiming a task, the agent MUST use this atomic claim procedure:
 
+1. Acquire `locks/journal.lock`.
+2. Validate `events.jsonl` and reconstruct the task lifecycle from events for the target `task_id`.
+3. Check whether the task has an active owner. `claimed`, `in_progress`, `waiting`, `blocked`, and `timeout_candidate` are active ownership states for claim purposes.
+4. If an active owner exists, abort the claim, release `locks/journal.lock`, and report the owner.
+5. If the task is open or recovered, append a `task_claimed` event while still holding `locks/journal.lock`.
+6. Update `state.json.active_agent`, `state.json.current_task`, `state.json.status`, and `state.json.last_event_id` while still holding `locks/journal.lock`.
+7. Validate `events.jsonl` and `state.json`, then release `locks/journal.lock`.
+
 ## 7. Artifacts
 
 Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
@@ -139,7 +167,7 @@
 
 ## 8. Locks
 
-Locks are advisory files under `.omc/collaboration/locks/`.
+Locks are files or directories under `.omc/collaboration/locks/`.
 
 Use a lock when two agents might modify the same shared collaboration file at the same time.
 
@@ -162,8 +190,46 @@
 
 Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
 
-## 9. Handoff Rules
+### Required Journal Lock
+
+Any operation that appends to `events.jsonl` or writes `state.json` MUST first acquire `.omc/collaboration/locks/journal.lock`.
+
+Lock acquisition MUST use an atomic filesystem operation. Preferred command pattern:
+
+```bash
+mkdir .omc/collaboration/locks/journal.lock
+```
+
+The agent that successfully creates the lock directory owns the lock. Agents MUST NOT use a non-atomic check-then-create sequence.
+
+The lock directory MUST contain `owner.json`:
+
+```json
+{
+  "agent": "codex",
+  "task_id": "TASK-20260530-01",
+  "created_at": "2026-05-30T08:00:00.000Z",
+  "heartbeat_at": "2026-05-30T08:00:00.000Z",
+  "reason": "append event and update state"
+}
+```
 
+The lock owner MUST hold `journal.lock` for the full read-check-write-validation sequence covering `events.jsonl` and `state.json`. The lock owner MUST remove the lock only after validating the write.
+
+## 9. Failure Recovery
+
+Agents MUST validate `events.jsonl` and `state.json` before using them for workflow decisions.
+
+If `state.json` is invalid but `events.jsonl` is valid, the agent MUST rebuild `state.json` from the valid log while holding `locks/journal.lock`. The rebuild MUST use the atomic state write procedure, and the agent MUST append a `state_rebuilt` event.
+
+If `events.jsonl` contains duplicate event ids, normal collaboration MUST stop. The agent MUST set `state.json.status` to `needs_repair` if state can be written safely, preserve the original log, and create a repair artifact describing the duplicate ids and proposed repair.
+
+If `events.jsonl` contains a malformed JSONL line, normal collaboration MUST stop. The agent MUST preserve the original log, create a repair artifact describing the malformed line and proposed repair, and set `state.json.status` to `needs_repair` if state can be written safely.
+
+Agents MUST NOT continue normal task claiming, handoff, or completion until the repair is complete.
+
+## 10. Handoff Rules
+
 When handing work to the other agent:
 
 1. Write or update the task document.
@@ -174,13 +240,13 @@
 
 Handoffs should include concrete next actions, relevant file paths, and any known blockers.
 
-## 10. Completion Rules
+## 11. Completion Rules
 
 A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
 
 Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
 
-## 11. Readiness Signal
+## 12. Readiness Signal
 
 Codex readiness is represented by both:
 
@@ -189,19 +255,21 @@
 
 Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
 
-## 12. Minimal Operating Checklist
+## 13. Minimal Operating Checklist
 
 Before collaboration work:
 
 - Read `AGENTS.md` or `CLAUDE.md`, as applicable.
 - Read `.omc/collaboration/protocol.md`.
 - Inspect `state.json` and recent `events.jsonl` entries.
+- Verify that `.omc/collaboration/` is on a supported filesystem before production testing.
 
 During collaboration work:
 
 - Keep edits scoped to the task.
 - Preserve append-only event history.
 - Keep shared JSON valid.
+- Hold `locks/journal.lock` for all `events.jsonl` and `state.json` writes.
 - Create durable artifacts for decisions that must survive chat context.
 
 After collaboration work:

tokens used
82,885

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
