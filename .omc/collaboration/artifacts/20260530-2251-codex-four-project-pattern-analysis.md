# Codex Analysis: Four Collaboration Systems For Claude-Codex-Gemini-Collab

**Date:** 2026-05-30  
**Author:** Codex  
**Scope:** Dev Buddy Plugin, Claude-Team, cc-use-exp, ShakaCode Claude-Codex guidance  
**Local target:** `claude-codex-gemini-collab` skill and `.omc/collaboration` protocol

## Executive Summary

The strongest improvement path is not to copy any one project. The local system already has the right foundation: event sourcing (`events.jsonl`), a rebuildable state cache (`state.json`), atomic journal locking, artifacts, and basic handoff semantics. Its gaps are in enforcement, context budgeting, structured failure memory, and Gemini execution contract.

Recommended order:

1. **P0:** Add a passive next-action/state-machine layer, structured failure context, and stricter journal/state validation.
2. **P0:** Make Gemini a read-only artifact producer via direct CLI, because Gemini CLI is installed locally (`0.44.1`) and MCP is not required for the first useful workflow.
3. **P1:** Split the protocol into progressive-disclosure slices: always-on invariants, role-specific quickstarts, and task-specific workflows.
4. **P1:** Add worktree isolation and spec-first/checkpoint gates for risky code changes.
5. **P2:** Defer full Ralph pipeline, automatic MCP routing, user-global config sync, and marketplace/plugin distribution until the minimal protocol is proven.

## Sources Used

- Dev Buddy Plugin: https://github.com/Z-M-Huang/vcp/tree/main/plugins/dev-buddy
- Claude-Team: https://github.com/smart-lty/Claude-Team
- cc-use-exp: https://github.com/doccker/cc-use-exp
- ShakaCode Claude+Codex guide: https://github.com/shakacode/claude-code-commands-skills-agents/blob/main/docs/claude-code-with-codex.md
- Existing local Codex analysis: `.omc/collaboration/artifacts/20260530-1654-codex-github-projects-analysis.md`
- Existing local Claude analysis: `.omc/collaboration/artifacts/20260530-0848-claude-github-projects-analysis.md`
- Current skill project: `/home/caohui/projects/claude-codex-gemini-collab`

## 1. Dev Buddy Plugin

### Architecture And Pattern

Dev Buddy is the most engineered system in the set. Its Ralph loop decomposes work into discovery, requirements/UAT, decomposition, plan linting, build, code review, and UAT. The important detail is not the exact stage list. The important detail is that state transitions, executor selection, retry handling, and mechanical failure context are file-backed and script-visible.

Core patterns:

- Passive state machine: compute the next action; do not bury lifecycle decisions in model prose.
- Multi-AI orchestration: route stages to configured executors and synthesize results.
- Disk state: persist plan/unit/progress JSON so compaction or process restart does not erase working memory.
- Mechanical backpressure: compile/test/lint/review failures feed back into the next build attempt.
- Forced gates: plan lint and user checkpoints prevent premature build work.

### Strengths

- Best model for correctness pressure. It treats LLM output as one input to a workflow, not as the workflow itself.
- Failure memory is first-class. This directly addresses our current pattern where blockers can be described in events but not consistently attached to task state.
- Passive state-machine design maps well to our event-sourced journal.

### Weaknesses

- Too heavy for the current collaboration skill. Full Ralph introduces unit DAGs, stage runners, config portals, and retry loops before the local protocol has matured.
- A fixed pipeline can become ceremony for small discussion/review tasks.
- Multi-executor synthesis can obscure accountability if every result becomes a blended answer.

### What To Borrow

- Borrow **passive next-action computation**, not the whole Ralph pipeline.
- Borrow **mechanical failure context** as structured event/task data.
- Borrow **gate vocabulary** for high-risk tasks: requirements, plan-lint, implementation, review, UAT.

## 2. Claude-Team

### Architecture And Pattern

Claude-Team is a hub-and-spoke model. Claude is the user-facing coordinator and invokes Codex/Gemini through MCP integrations. Codex is framed as implementation/debugging support; Gemini is framed as long-context analysis support.

Core patterns:

- Single entry point: Claude owns user interaction and delegation.
- MCP bridge: tools are called inside Claude's environment.
- Role routing: each model has a default specialty.
- Installation-oriented templates: create/update Claude, Codex, and Gemini instruction files.

### Strengths

- Clear user experience: one coordinator routes work.
- Good default role mapping: Claude for orchestration, Codex for code, Gemini for large context.
- MCP is useful if Claude is the only interactive front door.

### Weaknesses

- It is not a durable collaboration journal. Without events, locks, artifacts, and repair rules, delegation becomes invisible after the chat scrolls away.
- Automatic routing can hide who decided what and why.
- MCP setup modifies user-level tool configuration and adds installation risk. That is too much for the first Gemini integration step here.

### What To Borrow

- Borrow **role routing**, not automatic MCP routing.
- Borrow **advisor semantics**: Codex/Gemini suggestions are evidence, not authority.
- Add MCP later only if every delegation also writes `.omc/collaboration` events/artifacts.

## 3. cc-use-exp

### Architecture And Pattern

cc-use-exp is a configuration distribution and synchronization system, not a runtime collaboration engine. Its value is in how it separates rules, skills, commands, templates, and per-tool configuration for Claude, Gemini, Codex, Cursor, and related tools.

Core patterns:

- Layered configuration: always-on rules, context-triggered skills, explicit commands.
- Progressive disclosure: keep common rules short; load deeper workflow context only when needed.
- Single source, multiple targets: generate/sync tool-specific config from shared source material.
- Managed boundaries: avoid overwriting auth/history/cache/user preferences.
- Namespace isolation: prevent one tool's command/skill namespace from hijacking another's.

### Strengths

- Directly addresses our current protocol-loading problem. Our protocol is loaded whole every time; cc-use-exp suggests a better split.
- Strong model for safe distribution if this collaboration skill becomes reusable across projects.
- Its managed-block mindset is the right standard for any future `~/.codex`, `~/.gemini`, or `~/.claude` writes.

### Weaknesses

- It can overfit to personal global configuration.
- Global sync is operationally riskier than project-local `.omc` files.
- It does not solve runtime task ownership, event ordering, or failure recovery.

### What To Borrow

- Borrow **progressive disclosure** immediately.
- Borrow **managed config policy** before any user-home writes.
- Defer full cross-platform sync until the project-local skill is stable.

## 4. ShakaCode Claude-Codex

### Architecture And Pattern

ShakaCode's guide is a pragmatic operating model for Claude Code and Codex CLI. It relies on shared instructions, tool-specific extensions, sequential handoff, worktree isolation, cross-validation, and spec-first development.

Core patterns:

- Shared `AGENTS.md` as common instruction source.
- Tool-specific files for extra capabilities.
- Sequential handoff: one agent implements, another reviews.
- Worktrees for parallel or adversarial approaches.
- Spec-first: one side writes requirements/tests, another implements.

### Strengths

- Very compatible with the local repository model.
- Worktree isolation is the simplest answer to concurrent edits.
- Spec-first handoff improves review quality because the reviewer has something executable to judge against.

### Weaknesses

- It lacks event sourcing and state repair. It is an operating guide, not a collaboration runtime.
- Sequential handoff can be slow if every task waits for another agent.
- Shared instruction files alone do not solve stale state or hidden failures.

### What To Borrow

- Borrow **worktree isolation for write-capable parallelism**.
- Borrow **spec-first/checklist-first handoff**.
- Keep `.omc/collaboration` as the durable coordination layer.

## Current System Gaps

1. **State exists, but behavior is still manual.** `events.jsonl` and `state.json` record activity, but there is no first-class passive state machine that says "next legal action is X because event history says Y."

2. **Failure context is too free-form.** Blockers appear in summaries/details/artifacts, but there is no required schema for attempt count, failed command, evidence path, retry decision, or owner.

3. **Protocol loading is too monolithic.** Agents read the whole protocol even when they only need "how to claim" or "how to run Gemini read-only." This burns context and increases accidental instruction collisions.

4. **Gemini support is present but not yet disciplined.** Gemini CLI is installed and an invocation script exists, but the workflow still needs a stronger contract: input manifest, read-only guarantee, artifact output, event type, failure artifact, and validation.

5. **Flat peer collaboration lacks routing pressure.** The protocol defines roles, but task creation/claim/handoff scripts do not force route choice or explain why a task should go to Claude, Codex, or Gemini.

6. **The skill project is not a complete plugin distribution.** `/home/caohui/projects/claude-codex-gemini-collab` has `SKILL.md`, assets, and scripts, but no `.codex-plugin/plugin.json`. Treating marketplace/plugin distribution as P0 would be premature.

7. **Current scripts have correctness gaps.** The skill template says `active_agent` is `claude`, `codex`, or `none`, despite Gemini support. `collab_event.py` sets unknown event types to `in_progress`, which can corrupt state for analysis-only events. `repair()` writes state directly instead of using the journal lock/atomic temp contract. These need hardening before expanding automation.

8. **Existing state can drift semantically while passing basic last-event checks.** In this repo, event 49 restored blocked status for `TASK-20260530-06`, later review/artifact events moved `state.status` to `waiting`. That may be mechanically valid but operationally ambiguous.

## Critical Response To Claude's Earlier Direction

Claude's earlier priority list treated "Gemini integration" and "cross-platform skill distribution" as the highest ROI. I agree with Gemini, but not with broad distribution as an early priority.

The ordering should be:

1. First, harden the journal/state machine and failure context.
2. Then add Gemini as a minimal read-only artifact producer.
3. Only after that, consider cross-platform sync or MCP.

Why: adding more tools before enforcing state transitions multiplies ambiguity. A three-agent system with weak state semantics is worse than a two-agent system with strong evidence and recovery.

## Prioritized Integrable Patterns

### P0. Passive Next-Action State Machine

Add a read-only script:

```text
collab_next_action.py --task TASK-ID
```

It should inspect `events.jsonl`, task doc, artifacts, and state, then output:

- `claim_allowed`
- `blocked_requires_repair`
- `write_artifact_expected`
- `handoff_expected`
- `waiting_for_synthesis`
- `complete_allowed`
- `needs_user_decision`

It must not mutate files. This borrows Dev Buddy's passive state-machine pattern without importing Ralph.

### P0. Structured Failure Context

Require `blocked`, `analysis_failed`, `validation_failed`, and `review_response` events to include:

- `attempt`
- `failed_action`
- `evidence`
- `root_cause`
- `next_action`
- `owner`
- `retry_allowed`

This is the local equivalent of Dev Buddy's mechanical failure memory.

### P0. Gemini Read-Only Artifact Workflow

Use direct CLI, not MCP, for the first production path:

```bash
gemini -p "<prompt>" --approval-mode plan --output-format text
```

Contract:

- Gemini receives a prompt plus explicit file list or manifest.
- Gemini writes no repository files directly.
- Codex/Claude wrapper writes the artifact.
- Every live call creates success or failure artifact.
- Event types should be explicit: `analysis_requested`, `analysis_completed`, `analysis_failed`.
- Failed Gemini calls must not move task state to generic `in_progress`.

### P0. Journal/State Semantic Validation

Keep the existing JSONL/id/lock validator, but add semantic checks:

- `state.status` must match the latest status-relevant event, not necessarily the latest event.
- `analysis_requested` must not overwrite an existing blocked task unless it resolves the blocker.
- `active_agent` must allow `gemini` where protocol says tri-model.
- Every `handoff_requested` should identify target agent and expected next artifact.

### P1. Progressive Protocol Disclosure

Split the protocol into:

- `protocol.md`: short invariants only.
- `roles.md`: Claude/Codex/Gemini routing.
- `journal.md`: event/state/lock mechanics.
- `workflows/independent-analysis.md`.
- `workflows/gemini-readonly.md`.
- `workflows/code-change-with-review.md`.
- `workflows/repair.md`.

Agents load the invariant file first, then only the workflow slice needed. This is cc-use-exp's layered configuration idea applied to runtime collaboration.

### P1. Spec-First And Worktree Gates

For code-writing tasks:

- Require acceptance criteria before claim.
- Require another agent or script to validate evidence before completion.
- Use worktrees if two agents may write code in parallel.
- Gemini remains read-only unless the user explicitly authorizes write access and the work is isolated.

### P1. Role Routing Hints At Task Creation

Task creation should choose or suggest:

- `primary_agent`
- `review_agent`
- `analysis_agent`
- `requires_independent_analysis`
- `requires_worktree`
- `requires_mechanical_validation`

This gives Claude-Team's role clarity without hiding work behind automatic MCP routing.

### P2. Managed Multi-Tool Config Sync

Before writing any global config:

- dry-run preview
- manifest
- backup
- managed block markers
- never overwrite auth/history/cache
- user confirmation

This is cc-use-exp's safest lesson, but it should remain P2.

### P2. Optional MCP Adapter

MCP can be useful if Claude is the primary user interface, but it should be an adapter over `.omc/collaboration`, not a replacement. Every MCP delegation should produce the same artifacts/events as direct CLI.

### P2. Ralph-Lite Pipelines

Only for high-risk implementation tasks, add optional templates:

- discovery
- requirements
- plan-lint
- build
- review
- UAT

Do not make this mandatory for ordinary review/discussion tasks.

## Gemini CLI Considerations

Gemini CLI is installed and versioned locally (`0.44.1`). That makes direct CLI feasible. The right first integration is not "Gemini as a third writer"; it is "Gemini as a large-context read-only analyst whose output is persisted as an artifact."

Concrete improvements to the existing script:

- Avoid shell redirection for production artifact creation; use a Python wrapper with atomic temp+rename.
- Preserve both prompt manifest and CLI stderr/stdout.
- Add timeout and retry classification.
- Validate artifact path stays under `.omc/collaboration/artifacts`.
- Add `--dry-run` that does not mutate journal unless explicitly requested.
- Add a no-network/no-write disclaimer to the prompt.
- Do not use old `claude-codex-collab` paths from the renamed skill.

## Final Recommendation

Implement these first:

1. `collab_next_action.py` passive state-machine report.
2. Structured failure event schema and validator checks.
3. Hardened Gemini read-only artifact workflow.
4. Protocol progressive-disclosure split.
5. Worktree/spec-first gate for write-capable multi-agent tasks.

Do not implement these yet:

1. Full Ralph pipeline.
2. Automatic MCP routing.
3. Global `.claude`/`.codex`/`.gemini` sync.
4. Marketplace/plugin packaging.
5. Multi-agent auto-synthesis without explicit source artifacts.

This keeps the collaboration system's strongest property, the filesystem journal, while adding the enforcement and context-budgeting patterns that the four projects show are missing.
