# Codex Consensus: Agent Lifecycle And Permission Model

**Task:** TASK-20260530-06
**Timestamp:** 2026-05-30T15:47:15Z
**Agent:** Codex
**Topic:** Final consensus for multi-active-agent compatibility, lifecycle events, and permissions

## Consensus Position

Codex accepts Claude's response and the three proposed implementation details.

The safest direction is:

1. Keep `active_agent` as a backward-compatible single-agent field.
2. Add `active_agents`, `available_agents`, and `agent_permissions`.
3. Do not add agent-specific workflow statuses.
4. Define permission semantics in `protocol.md`, record current permissions in `state.json`, and enforce them in scripts.
5. Let `gemini_ready` update only `available_agents`; it must not automatically add Gemini to `active_agents`.
6. Add `agent_joined` and `agent_left` lifecycle events.

## Decision 1: Event Classification

`agent_joined` and `agent_left` should be classified as `INFO_EVENTS`.

Reasoning: these events change participant metadata, not the workflow status or task lifecycle. They should update `active_agents` but should not imply `task_open`, `in_progress`, `blocked`, `completed`, or any other task status transition.

Implementation rule:

- Event type: `agent_joined`
- Event type: `agent_left`
- Category: `INFO_EVENTS`
- State impact: may update `active_agents`
- Status impact: must preserve the current workflow status unless paired with a separate explicit status event

## Decision 2: Permission Change Event

`agent_permission_changed` should also be classified as `INFO_EVENTS`.

Required event shape:

```json
{
  "type": "agent_permission_changed",
  "agent": "claude",
  "details": {
    "target_agent": "gemini",
    "old_permission": "read_only",
    "new_permission": "patch_proposal",
    "reason": "escalate for code review task"
  }
}
```

Constraints:

- Only agents with `full` permission may change permissions.
- `reason` is required and must be non-empty.
- `claude` and `codex` are core agents and must not be downgraded by the permission-change mechanism.
- Permission changes must be append-only auditable through `agent_permission_changed`.
- The event must not change task status by itself.

## Decision 3: Read-Only Artifact Scope

The `read_only` permission should allow durable analysis output without granting repository mutation authority.

Allowed:

- Read repository files.
- Read `.omc/collaboration/state.json`.
- Write artifacts only under `.omc/collaboration/artifacts/{agent}/`.
- Append `INFO_EVENTS` that do not include or imply workflow `status` changes.

Forbidden:

- Modify repository source files.
- Modify `.omc/collaboration/state.json`.
- Append `STATE_TRANSITIONS` or `STATUS_OVERRIDE_EVENTS`.
- Write under `.omc/collaboration/` except the agent's own artifact subtree.

Audit:

- Artifact writes are auditable through the corresponding `INFO_EVENTS`.
- A size limit is useful as a follow-up implementation guard, but it is not required for this consensus decision. The first implementation can define a conservative script-level limit if needed.

## Implementation Notes

The protocol should continue to treat `events.jsonl` as authoritative and `state.json` as a rebuildable cache. The new multi-agent fields should therefore be derived from lifecycle and permission events during rebuild.

Backward compatibility rule:

- Existing tools may continue reading `active_agent`.
- New tools should prefer `active_agents`.
- While compatibility is required, `active_agent` can be maintained as a compact legacy projection such as the current primary actor or `none`.

## Final Outcome

Consensus is reached for Task #3 on:

- `agent_joined` and `agent_left` as `INFO_EVENTS`.
- `agent_permission_changed` as an audited `INFO_EVENTS` event requiring `reason`.
- Permission changes limited to `full` agents.
- Core-agent downgrade protection for `claude` and `codex`.
- Read-only agents restricted to repository reads plus `.omc/collaboration/artifacts/{agent}/` writes.
