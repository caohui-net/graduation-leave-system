# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-05T20:00:13.604Z

## Original task

审查Phase 0 P0阻塞分析文档 .omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md。问题：116个File2独有学生缺少楼栋数据，导致宿管员路由失败（98.0% vs 100%门禁要求）。文档提供3个决策选项：1)接受98%覆盖率 2)排除116人 3)等待用户提供数据。Claude推荐选项1+后续改进路径。请评估：1)推荐方案是否合理 2)是否有遗漏的风险或替代方案 3)业务决策建议。输出简洁评审意见。

## Final prompt

审查Phase 0 P0阻塞分析文档 .omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md。问题：116个File2独有学生缺少楼栋数据，导致宿管员路由失败（98.0% vs 100%门禁要求）。文档提供3个决策选项：1)接受98%覆盖率 2)排除116人 3)等待用户提供数据。Claude推荐选项1+后续改进路径。请评估：1)推荐方案是否合理 2)是否有遗漏的风险或替代方案 3)业务决策建议。输出简洁评审意见。

## Raw output

```text
**评审结论：不建议直接采纳“选项1=接受98%覆盖率并通过Phase 0”。**

Claude的方向有现实性：File2本身没有楼栋字段，继续让5830名已可路由学生被116条缺字段数据长期阻塞，确实不划算。但当前推荐把“继续实施主流程”和“降低验收门禁”混在一起了，风险偏高。

**主要问题**

1. 这会破坏既有门禁共识。前序共识明确要求 `validate_routing_coverage.py` 在 Phase 2 前强制 100% 覆盖，实施方案也写明5946人宿管/辅导员均需100%可路由。仅因116人缺楼栋就把门禁改成98%，需要用户明确批准，不能作为技术团队默认决策。

2. “导入116人”不等于“允许116人无法提交”。用户决策只是要求 File2 独有学生导入，不代表接受他们上线后不能走离校流程。文档第170行后的推荐理由把“符合用户导入决策”和“116人暂不可用”绑定，逻辑不充分。

3. 遗漏了更稳妥的混合方案：**导入5946人，但把116人标记为 `routing_incomplete` / `missing_building`，禁止提交或进入人工补录队列；Phase 0主流程按5830人通过，116人作为显式阻塞清单单独跟踪。** 这比简单接受98%更清晰，也比完全等待数据更可推进。

4. 还应补一个业务判断：这116人是否可能是校外住宿、无需宿管审批、非毕业离校对象或数据重复/异动学生。如果存在“无需宿管”的合法类别，应新增明确的业务路由规则，而不是让空楼栋静默失败。

**建议决策**

推荐采用“选项1的推进节奏 + 更严格的限制条件”，不要表述为“接受98%覆盖率”。

业务口径建议改为：

- 5946人全部导入，用于身份、辅导员、统计和后续补录。
- 5830名 File1 学生满足完整审批路由，可进入 Phase 1-5。
- 116名 File2-only 学生不得提交离校申请，直到补齐楼栋/寝室，或用户确认其为免宿管/特殊流程。
- 系统必须显式提示“住宿信息缺失，暂不能提交”，不能到审批创建时才失败。
- 保留100%门禁，但拆成两个门禁：`active_eligible_students` 100%可路由；`all_imported_students` 缺失清单为已知例外并需用户签字确认。

**最终意见**

Claude推荐“不要因116人阻塞主流程”是合理的；但“降低为98%验收通过”不够严谨。业务上应要求用户在三件事中明确确认：这116人是否必须使用系统、是否能补楼栋数据、补齐前是否允许他们不可提交。默认决策应是“主流程推进，116人导入但冻结申请能力并形成补录清单”。


Reading additional input from stdin...
OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019e995d-f997-7813-b46b-076f6d7b6e2a
--------
user
审查Phase 0 P0阻塞分析文档 .omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md。问题：116个File2独有学生缺少楼栋数据，导致宿管员路由失败（98.0% vs 100%门禁要求）。文档提供3个决策选项：1)接受98%覆盖率 2)排除116人 3)等待用户提供数据。Claude推荐选项1+后续改进路径。请评估：1)推荐方案是否合理 2)是否有遗漏的风险或替代方案 3)业务决策建议。输出简洁评审意见。
codex
我会先读取项目的协作与评审规则，再查看这份阻塞分析文档本身，确保评审意见按项目约定输出。
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
/bin/bash -lc "sed -n '1,260p' .omc/collaboration/protocol.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Claude-Codex Collaboration Protocol

Version: 0.3
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
- `locks/`: lock files or directories for serialized work.
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

exec
/bin/bash -lc "sed -n '1,260p' docs/codex-review-protocol.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Codex审查流程指南

**版本：** v2.0  
**更新日期：** 2026-05-28  
**适用范围：** 使用 `/oh-my-claudecode:ask codex` 进行文档审查

---

## Load Trigger (懒加载条件)

Read this file when ANY of these occur:
- 技术文档审查（Technical design documents）
- 数据库变更（Database schema changes）
- API设计（API interface design）
- 数据对接方案（Data integration plans）
- 系统架构调整（System architecture updates）
- 用户要求与Codex对话（User requests Codex review）

---

## 一、流程概述

本指南定义了与Codex进行对话式审查的标准流程，使用OMC内置的`/oh-my-claudecode:ask`技能。

**核心原则：**
- 使用统一的`/oh-my-claudecode:ask codex`方式
- 结构化的审查请求
- 批判性分析Codex建议
- 迭代式达成共识

---

## 二、完整流程（7步）

### 第1步：创建审查请求文档

**文件命名：** `XX-[主题]-review-request.md`

**文档结构：**
```markdown
# [主题] - Codex审查请求

**审查日期：** YYYY-MM-DD
**审查类型：** [类型]
**审查范围：** [范围]

## 一、背景/需求
[说明审查背景和目的]

## 二、已完成的工作
[列出已完成的修改]

## 三、审查要点
[列出需要Codex关注的具体问题]

## 四、潜在问题
[列出已知的潜在问题]

## 五、期望输出
1. 审查结论：通过/需要修改/不建议
2. 问题清单
3. 修复建议
4. 最终方案
```

---

### 第2步：调用Codex审查

**使用OMC内置技能：**
```
/oh-my-claudecode:ask codex "审查 docs/discussions/[路径]/XX-[主题]-review-request.md - [具体审查要求]"
```

**示例：**
```
/oh-my-claudecode:ask codex "审查 docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md - 这是我们对你第二轮审查的回应。请确认：1) 3个关键修正方案是否可行 2) 5个补充细节是否完整 3) 数据库模型调整方案是否有遗漏 4) 是否可以基于此创建v2共识文档"
```

**优点：**
- 自动保存结果为artifact：`.omc/artifacts/ask/codex-*.md`
- 统一的调用接口
- 更好的错误处理

---

### 第3步：保存Codex审查结果

**文件命名：** `XX+1-[主题]-codex-response.md`

**从artifact中提取关键内容：**
- 审查结论
- 发现的问题（按优先级分类）
- 具体修复建议
- 代码示例

**文档结构：**
```markdown
# [主题] - Codex审查响应

**审查日期：** YYYY-MM-DD
**审查人：** Codex
**Artifact路径：** .omc/artifacts/ask/codex-[timestamp].md

## 审查结论
[总体评价]

## 发现的问题

### 问题1：[标题] [优先级]
**位置：** 文件:行号
**问题描述：** [详细说明]
**影响：** [影响分析]
**修复建议：** [具体方案]

[重复其他问题]

## 审查通过的部分
[列出做得好的地方]
```

---

### 第4步：Claude响应Codex审查

**文件命名：** `XX+2-[主题]-claude-response.md`

**文档结构：**
```markdown
# [主题] - Claude响应

**响应日期：** YYYY-MM-DD
**针对：** Codex审查响应

## 对Codex审查的回应
[总体回应]

## 问题确认与修复方案

### 问题1：[标题]
**Codex指出：** [问题描述]
**Claude确认：** [确认分析]
**修复方案：** [具体方案]

[重复其他问题]

## 修改清单
[列出立即执行的修改]
```

---

### 第5步：执行修复

**按优先级修复：**
1. P0/CRITICAL问题 - 必须立即修复
2. P1/MAJOR问题 - 应该修复
3. P2/MINOR问题 - 可选修复

**修复后验证：**
- 使用Read工具验证修改正确
- 检查所有相关文档一致性

---

### 第6步：创建共识文档

**文件命名：** `XX+3-[主题]-consensus.md`

**文档结构：**
```markdown
# [主题] - 最终共识

**日期：** YYYY-MM-DD
**参与方：** Codex + Claude

## 审查结论
**状态：** 已修复/通过

## 已完成的修复
[列出所有修复，包含修改前后对比]

## 最终方案
[总结最终达成的方案]

## 文档一致性确认
[确认所有相关文档已更新]
```

---

### 第7步：归档到项目文档

**更新以下文件：**
1. `docs/PROJECT-SUMMARY.md` - 添加审查记录
2. `.omc/session-context.json` - 更新completed和artifacts
3. Git commit + push

---

## 三、讨论原则

### 1. 批判性思维
- **不要急于认同：** 收到Codex审查后，仔细分析每个问题
- **合理质疑：** 如果Codex建议不合理，在Claude响应中说明理由
- **深入分析：** 不只看表面问题，分析根本原因和影响范围

### 2. 迭代式讨论
- **不局限一次：** 如果修复后发现新问题，可再次提交Codex审查
- **及时发现问题：** 修复过程中发现不一致，立即记录
- **多轮达成共识：** 复杂问题可能需要2-3轮讨论才能完全解决

### 3. 分段处理
- **大篇幅分章节：** 超过500行的文档，按章节分别审查
- **分批修复：** 问题多时，按优先级分批修复和验证
- **渐进式共识：** 每个章节达成共识后再进入下一章节

---

## 四、文件编号规则

**连续编号：**
- XX号：审查请求
- XX+1号：Codex响应
- XX+2号：Claude响应
- XX+3号：最终共识

**示例：**
- 34-codex-second-review-response.md（审查请求）
- 35-response-to-codex-critical-issues.md（Claude响应）
- 36-data-confirmation-and-implementation.md（共识文档）

---

## 五、验证清单

**审查前：**
- [ ] 审查请求文档结构完整
- [ ] 审查范围明确
- [ ] 期望输出清晰

**审查中：**
- [ ] `/oh-my-claudecode:ask codex`调用成功
- [ ] Artifact已生成
- [ ] 问题优先级明确

**审查后：**
- [ ] 所有问题已修复
- [ ] 文档一致性已验证
- [ ] 项目文档已更新
- [ ] Git已提交推送

---

## 六、关键要点

### ✓ 成功要素
- 审查请求文档要详细、结构化
- 使用`/oh-my-claudecode:ask codex`（不是直接调用CLI）
- Claude响应要具体、可执行、有批判性分析

codex
规则里要求项目命令加 `rtk` 前缀；后续读取与检查我会按这个约定执行。接下来我看目标文档和相关数据口径，重点核对“98%是否可接受”和“宿管员路由是否有业务兜底”。
exec
/bin/bash -lc "rtk ls -la .omc/collaboration/artifacts .omc/collaboration/tasks docs | sed -n '1,220p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
acceptance/
api/
api-samples/
contracts/
design/
discussions/
plans/
superpowers/
templates/
ui-design-proposals/
20260530-0805-codex-protocol-critical-review.md  15.8K
20260530-0808-claude-response-to-codex-review.md  9.9K
20260530-0814-protocol-review-consensus.md  6.3K
20260530-0848-claude-github-projects-analysis.md  10.0K
20260530-0902-claude-codex-consensus-discussion.md  11.1K
20260530-0937-claude-synthesis-next-steps.md  8.3K
20260530-0955-claude-phase3-initial-analysis.md  6.0K
20260530-0959-codex-phase3-independent-review.md  13.8K
20260530-1005-claude-response-to-codex-phase3-review.md  9.5K
20260530-1008-codex-phase3-consensus.md  8.1K
20260530-1015-day0-completion.md  1.8K
20260530-1025-phase4-operator-checklist.md  5.4K
20260530-1611-codex-second-response-to-claude.md  7.3K
20260530-1625-claude-phase1b-response.md  3.6K
20260530-1654-codex-github-projects-analysis.md  15.5K
20260530-1655-claude-step2-phase1-response.md  12.9K
20260530-1703-codex-consensus-confirmation.md  4.3K
20260530-1711-gemini-test-gemini-workflow-.md  335B
20260530-1718-claude-blocking-issues-response.md  16.4K
20260530-1723-codex-review-claude-blocking-issues-response.md  9.6K
20260530-1725-claude-p0-fixes.md  16.0K
20260530-1733-codex-next-steps-analysis.md  9.9K
20260530-1747-codex-phase2-invariant-test-results.md  2.2K
20260530-1747-codex-phase2-invariant-tests.py  14.4K
20260530-1942-codex-completion-boundary-analysis.md  4.0K
20260530-2048-claude-response-codex-prep-analysis.md  5.5K
20260530-2053-codex-response-to-claude-week4-prep.md  3.2K
20260530-2225-codex-day0-verification.md  5.7K
20260530-2251-codex-four-project-pattern-analysis.md  15.8K
20260530-2301-codex-gemini-and-modular-agent-analysis.md  11.8K
20260530-2347-codex-agent-lifecycle-consensus.md  3.9K
20260531-0202-claude-codex-week3-response.md  10.0K
20260531-0210-week3-execution-consensus.md  3.3K
20260531-0215-phase0-fact-check-results.md  7.4K
20260531-0220-phase1-complete.md  2.5K
20260531-0225-phase3-complete.md  1.7K
20260531-0310-claude-response-readiness-repair.md  3.9K
20260531-0320-codex-readiness-repair-confirmation.md  2.0K
20260531-0325-step1-verification-results.md  3.9K
20260531-0405-codex-week3-consensus-response.md  3.9K
20260531-0415-codex-week3-execution-summary.md  2.5K
20260531-0421-codex-next-phase-strategy.md  7.4K
20260531-0425-codex-response-to-claude-next-phase-strategy.md  8.5K
20260531-0430-week3-final-summary.md  5.7K
20260531-0435-claude-response-next-phase-strategy.md  7.1K
20260531-0439-codex-week4-blocked-prep-analysis.md  4.0K
20260531-0440-week4-execution-plan-consensus.md  5.3K
20260531-0445-dorm-provider-discovery.md  3.7K
20260601-0135-claude-response-phase4a-blocker-challenge.md  5.5K
20260601-0405-codex-test-coverage-feedback.md  4.3K
20260601-1817-codex-events-jsonl-repair.md  672B
20260603-1502-claude-xg-data-gap-analysis.md  11.1K
20260603-1605-codex-xg-data-coverage-review.md  12.0K
20260603-1610-consensus-xg-data-coverage.md  7.9K
20260605-0852-codex-excel-association-review.md  11.4K
20260605-0910-claude-response-to-codex-excel-review.md  8.9K
20260605-0920-consensus-excel-association-strategy.md  11.6K
20260605-claude-response-implementation-plan-review.md  10.5K
20260605-codex-implementation-plan-review.md  10.2K
20260605-consensus-implementation-plan.md  9.5K
20260605-phase0-routing-coverage-blocker.md  7.3K
20260605-user-business-decisions.md  3.4K
blocked-waiting-for-devtools.md  2.2K
dorm-system-stakeholder-request.md  4.7K
events-jsonl-before-line95-repair-20260601T181700Z.bak  45.4K
events-jsonl-before-line95-repair-20260601T181800Z.bak  45.4K
phase4a-devtools-setup.md  6.9K
phase4a-validation-checklist.md  7.0K
phase4b-prep-note.md  5.2K
phase4b-skeleton-gaps.md  8.7K
test-coverage-analysis.md  3.2K
test-coverage-claude-response.md  9.4K
test-coverage-final-consensus.md  4.5K
TASK-20260530-01-protocol-critical-review.md  2.2K
TASK-20260530-02-implement-p0-amendments.md  3.2K
TASK-20260530-03-分析4个github项目并评估可借鉴内容（含gemini集成.md  473B
TASK-20260530-04-实施p0优先级项：角色路由+独立分析协议+journal校验.md  2.4K
TASK-20260530-05-next-steps-critical-discussion.md  2.6K
TASK-20260530-06-readiness-gate-canary-pilot.md  7.0K
TASK-20260602-01-ui-design-miniprogram.md  3.7K
TASK-20260602-02-step-4b-phase-3:-xg用户同步服务apply.md  1.8K
TASK-20260602-03-step-4b-phase-4:-回归验证---运行完整测试.md  1.3K
TASK-20260602-04-step-5:-xg用户同步管理命令---sync_xg_u.md  1.6K
TASK-20260603-01-xg-data-coverage-analysis.md  3.0K
TASK-20260603-02-xg-data-review-request.md  3.4K
TASK-20260605-01-excel-association-review-request.md  8.0K
TASK-20260605-01-excel数据源关联策略讨论---file1+file2通过.md  724B
TASK-20260605-03-implementation-plan-review.md  4.4K
TASK-20260605-04-phase-0-p0阻塞：116个file2独有学生缺少楼栋.md  1.0K
1-5830名毕业生（含研究生）.xls  1002.5K
2026届预计毕业生5675人.xlsx  900.7K
2026年学院辅导员信息统计表.xls  23.5K
2026年社区辅导员信息统计表.xls  30.0K
API-DATA-EXAMPLES.md  5.1K
COMPLETION-STATUS.md  4.1K
Codex审查流程指南.md  7.0K
Excel数据源分析与需求对比.md  8.0K
Excel数据源实际分析结果.md  9.7K
PROJECT-COMPLETION-DECLARATION.md  2.9K
PROJECT-SUMMARY.md  122.8K
XG-API-ACTUAL-DATA-SAMPLES.md  6.2K
XG-API-COLLECTION-TEST-GUIDE.md  4.1K
XG-API-DATA-EXAMPLES.md  6.7K
XG-API-DATA-SAMPLES.md  5.5K
XG-API-数据源全面分析报告.md  19.0K
XG-API与项目数据表对比分析.md  12.0K
XG-API数据不足解决方案讨论.md  11.2K
api说明.txt  7.5K
codex-review-protocol.md  7.0K
phase4c-xg-field-coverage.md  10.9K
project-completion-status-2026-06-02.md  4.1K
week3-day0-acceptance-checklist.md  11.7K
week3-day0-environment-strategy.md  2.2K
week3-day0-seed-data-requirements.md  4.1K
外部系统数据接口确认清单.md  5.6K
微信图片_20260528210617_553_47.jpg  85.9K
微信图片_20260528210618_554_47.jpg  192.1K
微信图片_20260528210619_555_47.jpg  121.0K
微信小程序备案说明.md  4.3K
微信小程序申请说明.md  2.4K
操作说明书-待改进事项.md  3.8K
操作说明书.md  10.7K
数据对接说明文档.md  13.8K
数据对接说明文档.md.backup  11.5K
数据确认清单.md  7.3K
用户设计说明书.md  12.2K
用户需求最终确认与实施方案.md  21.4K

exec
/bin/bash -lc "rtk sed -n '1,260p' .omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Phase 0 路由覆盖P0阻塞分析

**创建时间：** 2026-06-05T19:55:00Z  
**任务ID：** TASK-20260605-04  
**分析人：** Claude  
**严重程度：** P0 (阻塞Phase 0验证通过)

---

## 执行摘要

Phase 0 Task 0.5（路由覆盖验证）执行结果：
- **辅导员路由覆盖率：** 100.0% ✓ (5946/5946)
- **宿管员路由覆盖率：** 98.0% ✗ (5830/5946)
- **完整路由覆盖率：** 98.0% ✗ (5830/5946)

**门禁要求：** 100%路由覆盖率（文档要求）

**阻塞原因：** 116名File2独有学生缺少楼栋数据，无法路由至宿管员。

**业务影响：** 阻塞Phase 0验证通过，无法进入Phase 1-5实施。

---

## 问题详情

### 数据证据

**受影响学生数量：** 116人

**样本数据（前10人）：**
```
1. user_id=2020150140631, name=江羽抒, building=""
2. user_id=2020170140125, name=姜瑶, building=""
3. user_id=2021150240222, name=王鹏程, building=""
4. user_id=2021150140527, name=周若奕, building=""
5. user_id=2021120340233, name=张文君, building=""
6. user_id=2021280240108, name=刘谦民, building=""
7. user_id=2021170140110, name=饶梦琦, building=""
8. user_id=2021280240123, name=叶曌, building=""
9. user_id=2021280540124, name=冯璇, building=""
10. user_id=2021320140210, name=朱松竹, building=""
```

**特征：**
- 全部116人building字段为空字符串
- 拥有真实学号（2020/2021开头）
- user_id_source = 'file2_only'（来自File2但不在File1中）
- department字段非空（可以路由到辅导员）

---

## 根本原因分析

### 数据源对比

**File1字段（5830行）：**
- 学生姓名、学院名称、**楼栋名称**、**寝室号**、专业、年级、班级、层次

**File2字段（5675行）：**
- XH（学号）、XM（姓名）、FY（学院）、BH（班号）、SJHM（手机号）、email
- **缺失：** 楼栋名称、寝室号

**合并策略（merge_student_data.py）：**
1. File1作为基准（5830行）
2. File2补充学号、手机号、邮箱等字段
3. File2独有的116行学生追加到输出（用户决策3，2026-06-05）
4. File2独有学生的building_name和room_number字段为空字符串

**结论：** File2数据源本身不包含楼栋/寝室信息，因此File2独有的116名学生无法获得building_name字段，导致无法路由到宿管员。

---

## 影响评估

### 业务影响

**阻塞范围：**
- ✗ Phase 0 Task 0.5验证失败（98.0% vs 100%门禁要求）
- ✗ 无法进入Phase 1（数据准备与合并）
- ✗ 无法进入Phase 2-5（系统代码调整、数据导入、前端调整、测试验证）

**受影响学生：**
- 116名学生无法提交离校申请（缺少第一级审批人-宿管员）
- 占总学生数的1.95%（116/5946）
- 这些学生有真实学号，可能是合法在校生

### 系统影响

**审批流程设计：**
```
学生提交 → 宿管员审批(by 楼栋) → 辅导员审批(by 学院) → 完成
```

**第一级审批路由：** building_name → DormManager
- 必需字段：building_name（楼栋名称）
- 当前状态：116人building_name为空，路由失败

**第二级审批路由：** department → Counselor  
- 必需字段：department（学院）
- 当前状态：5946人全部有department，路由成功 ✓

---

## 决策选项分析

### 选项1: 接受98%覆盖率作为可接受标准

**描述：** 修改Phase 0门禁要求，将100%覆盖率降低为98%（或"File1学生100%覆盖率"）

**优点：**
- 立即解除P0阻塞，可以进入Phase 1-5实施
- 技术实现无需修改（验证脚本已完成）
- 承认数据源限制的现实

**缺点：**
- 降低数据质量标准
- 116名学生无法使用系统（占1.95%）
- 可能需要后续手工处理这116人的离校流程

**实施成本：** 低（仅需修改文档门禁标准）

**风险：** 中（用户可能要求这116人也能使用系统）

---

### 选项2: 排除File2独有学生，仅导入File1学生

**描述：** 回退用户决策3（2026-06-05），不导入File2独有的116名学生

**优点：**
- 达到100%覆盖率（5830/5830）
- 通过Phase 0门禁，可以进入Phase 1-5
- 数据一致性强（所有导入学生都有完整字段）

**缺点：**
- 违反用户明确决策（用户要求导入File2独有学生）
- 116名可能是合法在校生被排除系统外
- 需要修改merge_student_data.py
- 需要重新生成File5并更新文档

**实施成本：** 中（代码+数据+文档修改）

**风险：** 高（违反用户决策）

---

### 选项3: 要求用户提供File2独有学生的楼栋数据

**描述：** 暂停Phase 0，要求用户补充116名学生的楼栋/寝室数据

**优点：**
- 达到100%覆盖率（5946/5946）
- 数据完整性最高
- 所有学生都能正常使用系统

**缺点：**
- 阻塞Phase 0进度，等待用户提供数据
- 不确定数据提供时间
- 可能暴露File2数据质量问题

**实施成本：** 低（技术无需修改）

**风险：** 高（进度不确定）

---

## 推荐方案

**推荐：选项1（接受98%覆盖率）+ 后续改进路径**

### 理由

1. **业务现实：** File2独有的116名学生确实缺少楼栋数据，这是数据源限制而非技术问题
2. **影响范围可控：** 仅影响1.95%的学生（116/5946）
3. **辅导员路由完整：** 100%覆盖率已达成，第二级审批无阻塞
4. **进度考虑：** 避免长期阻塞，允许主流程（5830人）正常进行
5. **符合用户决策：** 用户明确要求导入File2独有学生（决策3），不应该回退

### 实施步骤

**短期（立即执行）：**

1. 修改Phase 0门禁标准：
   - 原标准：100%路由覆盖率
   - 新标准：File1学生100%覆盖率（5830/5830）+ 辅导员路由100%覆盖率（5946/5946）
   
2. 更新文档说明：
   - 在`docs/用户需求最终确认与实施方案.md`中记录此决策
   - 在Task 0.5验证结果中标注：98.0%宿管员覆盖率（File1学生100%，File2独有学生0%）
   
3. 记录已知限制：
   - 116名File2独有学生暂时无法使用系统
   - 需要用户后续提供楼栋数据
   
4. 通过Phase 0验证，进入Phase 1-5实施

**中期（Phase 1-5实施中）：**

5. 与用户沟通116名学生情况，确认：
   - 这些学生是否需要使用系统？
   - 用户是否能提供楼栋数据？
   - 预计提供时间？

**长期（系统上线后）：**

6. 如用户提供116名学生楼栋数据：
   - 更新File5数据
   - 重新导入这116名学生
   - 达到100%完整覆盖率

---

## 替代方案（如果推荐方案被拒绝）

**如果用户坚持100%覆盖率：** 执行选项3，暂停Phase 0，等待用户提供数据

**如果用户同意排除File2独有学生：** 执行选项2，回退决策3，仅导入5830名File1学生

---

## 附件

**相关文件：**
- Phase 0验证报告：`backend/data/routing_coverage_report.json`
- 合并脚本：`backend/scripts/merge_student_data.py`
- 合并输出：`backend/data/file5_students_merged.csv`（5946行）
- 用户决策文档：`.omc/collaboration/artifacts/20260605-user-business-decisions.md`

**数据快照：**
- File1学生：5830人（100%有楼栋数据）
- File2独有学生：116人（0%有楼栋数据）
- 总计：5946人
- 宿管员覆盖率：98.0%（5830/5946）
- 辅导员覆盖率：100.0%（5946/5946）

---

**分析完成时间：** 2026-06-05T19:57:00Z  
**下一步：** 等待Codex审查和用户决策


exec
/bin/bash -lc "rtk rg -n \"116|File2|98\\.0|100%|宿管|路由|门禁|楼栋|覆盖\" .omc/collaboration docs . -g '*.md' -g '*.json' -g '*.sql'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/api/notification-contract-v0.1.md:356:- 单元测试覆盖率>80%
.omc/collaboration/task-4-consensus.md:17:3. 过早覆盖完整 repair、权限矩阵和性能测试会扩大 Phase 1a 范围。
docs/ui-design-proposals/01-analysis-and-responsive-plan.md:82:   - 移动端：`width: 100%; max-width: 100%;`
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:34:重新深入检查File2后发现：
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:36:**File2确实包含学院字段（被遗漏）：**
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:43:File2 unique names: 5524
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:48:- 孙芮: File1=物理与电信学院, File2=物理与电信学院 ✓
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:49:- 徐茜茜: File1=物理与电信学院, File2=物理与电信学院 ✓
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:62:校区, 楼栋名称, 寝室号, 学生姓名, 性别, 专业, 学院名称, 班级, 层次, 年级
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:69:- 楼栋名称 (index 1) - 如"荷园2栋"
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:91:序号, 楼栋号, 职工号, 姓名, 电话
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:95:- 楼栋号 (index 1) - 如"紫园1栋"
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:119:- 补充：File2的XH(学号)
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:121:- 输出：File5包含{学号, 姓名, 学院, 班级, 楼栋, ...}
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:123:**Step 2: 建立楼栋→宿管员映射**
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:124:- File5的"楼栋名称" 关联 File3的"楼栋号"
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:125:- 生成：楼栋→宿管员工号映射表
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:126:- 用途：宿管员审批路由
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:131:- 用途：辅导员审批路由
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:143:**问题：** File1与File2通过"姓名+学院"关联是否可靠？
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:147:- File1有140个重名，File2有132个重名
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:152:2. **学院名称一致性：** File1"学院名称"与File2"FY"字段值是否完全一致？还是存在别名？
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:153:   - 示例：File1"物理与电信学院" vs File2可能的"物电学院"？
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:154:3. **未匹配记录：** File1有5830行，File2有5675行，差异155行如何处理？
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:157:### 4.2 楼栋→宿管员映射可行性
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:159:**问题：** File5"楼栋名称"与File3"楼栋号"能否建立可靠映射？
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:162:- File1楼栋示例："荷园2栋"
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:163:- File3楼栋示例："紫园1栋"
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:166:1. **格式一致性：** 楼栋名称格式是否统一？
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:167:2. **覆盖度：** File3是否包含File1中所有楼栋？
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:168:3. **一对多关系：** 一个楼栋是否对应多个宿管员？
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:169:4. **缺失工号：** File3部分宿管员"暂未申请"工号，如何处理这些楼栋的学生？
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:182:3. **覆盖度：** File4是否包含File1中所有学院？
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:189:- user_id (学号) - File2提供 ✓
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:204:2. **数据完整性：** 综合评估关联后的数据完整性（匹配率、覆盖率、准确率）
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:220:- 楼栋→宿管员映射可行性（✓/✗/⚠️）
.omc/collaboration/tasks/TASK-20260605-01-excel-association-review-request.md:249:我的初始分析得出"数据无法关联"结论是**错误的**（遗漏了File2的FY字段）。
.omc/collaboration/task-1-consensus.md:18:**问题：** 未知事件类型默认映射为`in_progress`，导致信息事件（如`artifact_created`）错误覆盖任务状态（如`blocked`）。
.omc/collaboration/task-1-consensus.md:175:3. **analysis_requested：** 同上，尤其覆盖原状态为`blocked`的场景
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:16:- 系统设计变更需求（数据模型、审批流程、路由逻辑、权限控制）
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:19:- 未来升级路径（寝室号精确路由）
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:29:- 2级审批流程（楼栋→学院）是否满足实际业务需求？
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:30:- 4类用户角色（学生/宿管员/辅导员/管理员）权限划分是否合理？
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:31:- ClassMapping移除后的路由方案（Building + Department）是否可行？
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:34:- [ ] File1+File2合并策略：5830行基准是否覆盖所有必需学生？
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:35:- [ ] 楼栋路由：一对多问题（一个楼栋多个宿管员）是否有明确规则？
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:36:- [ ] 学院路由：辅导员按学院级审批（非班级级）是否符合业务预期？
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:43:- 路由逻辑从ClassMapping改为Building+Department是否存在技术风险？
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:56:- File1、File2、File3、File4之间的数据关联是否清晰？
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:58:- 楼栋名称匹配（File1 vs File3）是否存在格式不一致风险？
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:59:- 5830行学生是否都能成功路由到宿管员和辅导员？
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:63:- [ ] 字段覆盖：File1+File2合并后所有必需字段是否完整？
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:64:- [ ] 路由验证：导入前门禁（每个学生必须能找到宿管员+辅导员）是否充分？
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:71:- 风险缓解措施（楼栋名称不匹配、多宿管员选择、管理员界面延后）是否充分？
.omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md:72:- 未来升级路径（寝室号精确路由）与当前实施是否存在架构冲突？
.omc/collaboration/tasks/TASK-20260603-02-xg-data-review-request.md:1:# Codex审查请求：XG API数据覆盖度分析
.omc/collaboration/tasks/TASK-20260603-02-xg-data-review-request.md:49:### 3.1 字段覆盖度
.omc/collaboration/tasks/TASK-20260603-02-xg-data-review-request.md:75:   - 必填字段覆盖情况
.omc/collaboration/tasks/TASK-20260605-01-excel数据源关联策略讨论---file1+file2通过.md:11:# Task: Excel数据源关联策略讨论 - File1+File2通过姓名+学院关联生成完整学生表(File5)，验证楼栋→宿管员、学院→辅导员映射可行性，评估数据完整性和匹配准确率
.omc/collaboration/tasks/TASK-20260605-01-excel数据源关联策略讨论---file1+file2通过.md:18:Excel数据源关联策略讨论 - File1+File2通过姓名+学院关联生成完整学生表(File5)，验证楼栋→宿管员、学院→辅导员映射可行性，评估数据完整性和匹配准确率
.omc/collaboration/tasks/TASK-20260530-04-实施p0优先级项：角色路由+独立分析协议+journal校验.md:11:# Task: 实施P0优先级项：角色路由+独立分析协议+journal校验+Gemini workflow
.omc/collaboration/tasks/TASK-20260530-04-实施p0优先级项：角色路由+独立分析协议+journal校验.md:26:### 1. 3-Agent角色路由定义 (Claude负责)
docs/acceptance/phase4c-known-issues.md:20:| 角色路由跳转 | 未验证 | 无法确认role-guard实际生效 | 模拟器/真机测试登录流程 |
.omc/collaboration/tasks/TASK-20260603-01-xg-data-coverage-analysis.md:1:# Task: XG API数据覆盖度分析
.omc/collaboration/tasks/TASK-20260603-01-xg-data-coverage-analysis.md:13:1. 哪些需求字段已被覆盖
.omc/collaboration/tasks/TASK-20260603-01-xg-data-coverage-analysis.md:27:1. 学生基本信息字段覆盖度
.omc/collaboration/tasks/TASK-20260603-01-xg-data-coverage-analysis.md:28:2. 辅导员基本信息字段覆盖度
.omc/collaboration/tasks/TASK-20260603-01-xg-data-coverage-analysis.md:60:2. 字段覆盖度矩阵（需求字段 vs 实际提供字段）
.omc/collaboration/tasks/TASK-20260603-01-xg-data-coverage-analysis.md:79:- ✓ 明确列出所有需求字段及其XG API覆盖状态
docs/acceptance/phase4c-evidence-index.md:65:**覆盖场景：**
.omc/collaboration/tasks/TASK-20260605-04-phase-0-p0阻塞：116个file2独有学生缺少楼栋.md:11:# Task: Phase 0 P0阻塞：116个File2独有学生缺少楼栋数据，导致宿管员路由失败（98.0% vs 100%门禁要求）。需要业务决策：1)接受98%覆盖率作为可接受标准 2)排除这116名学生直到补充楼栋数据 3)要求用户立即提供楼栋数据。辅导员路由已100%覆盖。此问题阻塞Phase 0验证通过及Phase 1-5实施。
.omc/collaboration/tasks/TASK-20260605-04-phase-0-p0阻塞：116个file2独有学生缺少楼栋.md:18:Phase 0 P0阻塞：116个File2独有学生缺少楼栋数据，导致宿管员路由失败（98.0% vs 100%门禁要求）。需要业务决策：1)接受98%覆盖率作为可接受标准 2)排除这116名学生直到补充楼栋数据 3)要求用户立即提供楼栋数据。辅导员路由已100%覆盖。此问题阻塞Phase 0验证通过及Phase 1-5实施。
docs/acceptance/phase4c-acceptance-checklist.md:83:### 2.3 测试覆盖 ✅
docs/acceptance/phase4c-acceptance-checklist.md:134:### 4.1 测试覆盖 ✅
docs/acceptance/phase4c-acceptance-checklist.md:152:### 4.2 错误场景覆盖 ✅
docs/acceptance/phase4c-acceptance-checklist.md:191:| 登录路由矩阵 | ✅ 通过 | student→student-application, counselor/dean→approvals |
docs/project-completion-status-2026-06-02.md:12:- 3步审批流程实现：宿管员 → 辅导员 → 学工部
docs/project-completion-status-2026-06-02.md:72:**收益**: 完整测试覆盖，CI/CD可用
docs/project-completion-status-2026-06-02.md:90:| 环境部署 | 100% | Docker + PostgreSQL 完整配置 |
docs/project-completion-status-2026-06-02.md:91:| 数据库模型 | 100% | 所有表结构及迁移完成 |
docs/project-completion-status-2026-06-02.md:92:| 核心API | 100% | 应用提交、审批、查询全部实现 |
docs/project-completion-status-2026-06-02.md:93:| 审批流程 | 100% | 3步工作流完整实现 |
docs/project-completion-status-2026-06-02.md:94:| XG集成 | 100% | 用户同步服务完成 (plan + apply) |
docs/project-completion-status-2026-06-02.md:95:| 管理命令 | 100% | CLI入口实现 |
docs/project-completion-status-2026-06-02.md:106:继续修复剩余17个测试问题，实现100%测试通过率
docs/project-completion-status-2026-06-02.md:111:3. 86% → 100%的最后一公里
docs/project-completion-status-2026-06-02.md:112:4. 完整测试覆盖保证后续开发质量
docs/XG-API数据不足解决方案讨论.md:45:- ✓ 业务完整性100%保障
docs/XG-API数据不足解决方案讨论.md:255:2. ✓ 业务完整性100%保障
docs/XG-API数据不足解决方案讨论.md:277:- [ ] 验证ClassMapping覆盖率
docs/XG-API数据不足解决方案讨论.md:378:2. 业务完整性100%保障
docs/XG-API数据不足解决方案讨论.md:396:- ✓ CSV导入成功率 100%
docs/XG-API数据不足解决方案讨论.md:397:- ✓ ClassMapping覆盖率 100%
docs/XG-API数据不足解决方案讨论.md:403:- ✓ 辅导员自动分配成功率 100%
docs/XG-API数据不足解决方案讨论.md:404:- ✓ 申请资格判定准确率 100%
docs/week3-day0-acceptance-checklist.md:531:- 测试覆盖不足
.omc/collaboration/task-2-consensus.md:22:**风险场景：** collab_event.py持锁写入时，repair()无锁覆盖state.json，导致状态不一致或数据丢失。
.omc/collaboration/task-2-consensus.md:32:3. ✅ 锁范围覆盖完整read-check-write
docs/superpowers/plans/2026-05-27-implementation-plan.md:69:- ✓ 单元测试覆盖率 > 80%
docs/superpowers/plans/2026-05-27-implementation-plan.md:534:   - 配置页面路由
docs/superpowers/plans/2026-05-27-implementation-plan.md:572:   - 确保覆盖率 > 80%
docs/superpowers/plans/2026-05-27-implementation-plan.md:628:**风险5：测试覆盖不足**
.omc/collaboration/phase1b-implementation-consensus.md:14:### 1. 实施顺序：Phase A-E分层门禁
.omc/collaboration/phase1b-implementation-consensus.md:18:**采纳方案：** Codex的Phase A-E分层，但明确为门禁式推进：
.omc/collaboration/phase1b-implementation-consensus.md:24:  - **门禁：** 验证脚本通过，旧日志可读
.omc/collaboration/phase1b-implementation-consensus.md:31:  - **门禁：** tempdir smoke通过，activation事件成功追加
.omc/collaboration/phase1b-implementation-consensus.md:38:  - **门禁：** 状态决策明确，canonical/legacy 解释一致或显式声明分歧
.omc/collaboration/phase1b-implementation-consensus.md:44:  - **门禁：** repair-smoke 在 tempdir 通过
.omc/collaboration/phase1b-implementation-consensus.md:49:  - **门禁：** Gemini dry-run 通过，不依赖 Gemini CLI 安装
.omc/collaboration/phase1b-implementation-consensus.md:124:- 每个 Phase 都有明确的验证门禁
.omc/collaboration/phase1b-implementation-consensus.md:291:- 并会覆盖 `state.status`（line 112）
docs/PROJECT-SUMMARY.md:73:- ✓ 批次5：第9-10章性能测试（索引、连接池、TDD、覆盖率）
docs/PROJECT-SUMMARY.md:227:  - 移除GET /api/applications列表端点（统一为5个HTTP路由）
docs/PROJECT-SUMMARY.md:232:  - P1-1：错误样例覆盖不完整（Section 3定义8个错误码，Section 6.2只有4个样例）
docs/PROJECT-SUMMARY.md:234:  - P2-1：术语不一致（"5个HTTP路由" vs "4个API端点"）
docs/PROJECT-SUMMARY.md:278:  - 覆盖completed、pending、not_started、unknown四种状态
docs/PROJECT-SUMMARY.md:470:- ✓ 自动化测试：4个测试覆盖403/409场景
docs/PROJECT-SUMMARY.md:642:5. **测试覆盖不足** - 采用TDD模式
docs/PROJECT-SUMMARY.md:654:- ✓ 单元测试覆盖率 > 80%
docs/PROJECT-SUMMARY.md:683:- ✓ 测试覆盖：resubmission + approval filter
docs/PROJECT-SUMMARY.md:703:  - app.json（页面路由、窗口配置）
docs/PROJECT-SUMMARY.md:767:- ✓ 新增审批负向权限覆盖：学生不可审批/驳回、角色步骤不匹配禁止、同角色非指定审批人禁止
docs/PROJECT-SUMMARY.md:769:- ✓ 新增状态机覆盖：重复驳回冲突、counselor/dean步骤状态不匹配返回409
docs/PROJECT-SUMMARY.md:798:- ✓ 无需新增代码，仅验证覆盖度
docs/PROJECT-SUMMARY.md:844:2. ✓ MVP = 最小可行路径 + 必要错误处理（非全覆盖）
docs/PROJECT-SUMMARY.md:943:1. 高优先级：实现student-application页面 + 基于角色的路由（修复已知gap）
docs/PROJECT-SUMMARY.md:966:1. ✓ 实施顺序：结构化骨架优先（完整UI结构 + 页面骨架 + 注册 + 登录路由smoke + 提交逻辑）
docs/PROJECT-SUMMARY.md:981:- ✓ 登录路由矩阵
docs/PROJECT-SUMMARY.md:1004:- ✅ 登录路由矩阵实现完成
docs/PROJECT-SUMMARY.md:1058:**后端测试覆盖增强（2026-06-01）：**
docs/PROJECT-SUMMARY.md:1061:- ✓ Claude创建初步测试覆盖分析（识别3个高优先级gap）
docs/PROJECT-SUMMARY.md:1070:3. ✓ State machine gaps: 已被现有测试覆盖（resubmission, terminal protection）
docs/PROJECT-SUMMARY.md:1087:- ✓ 测试覆盖关键安全和边界场景
docs/PROJECT-SUMMARY.md:1100:- ✅ 后端测试覆盖增强完成
docs/PROJECT-SUMMARY.md:1135:- ✓ 后端测试（19个测试，100%通过）
docs/PROJECT-SUMMARY.md:1155:- ✅ 19个测试100%通过
docs/PROJECT-SUMMARY.md:1218:- 增加单元测试覆盖
docs/PROJECT-SUMMARY.md:1310:- ✓ 字段校验覆盖所有必填字段和外键引用
docs/PROJECT-SUMMARY.md:1366:- ✓ Smoke test覆盖附件上传/下载/删除
docs/PROJECT-SUMMARY.md:1447:  1. Blocked by WeChat DevTools（6项：编译/运行/真机/上传/网络/路由）
docs/PROJECT-SUMMARY.md:1602:- ✓ URL路由配置
docs/PROJECT-SUMMARY.md:1636:- backend/apps/notifications/urls.py（URL路由）
docs/PROJECT-SUMMARY.md:1786:- ✅ API路径级测试覆盖完成
docs/PROJECT-SUMMARY.md:1862:4. **测试覆盖**
docs/PROJECT-SUMMARY.md:1895:**Step 1.0: Smoke可重复运行门禁（已完成）：**
docs/PROJECT-SUMMARY.md:1925:- ✓ 添加schema和Swagger UI路由
docs/PROJECT-SUMMARY.md:1934:- backend/config/urls.py（添加schema路由）
docs/PROJECT-SUMMARY.md:1946:- ✓ 补充DEPLOYMENT.md故障排查指南（覆盖8个真实场景）
docs/PROJECT-SUMMARY.md:1956:- 故障排查指南: 覆盖409/422/401/403/media/Docker/数据库/schema场景 ✓
docs/PROJECT-SUMMARY.md:1960:- ✅ Step 1.0: Smoke可重复运行门禁
docs/PROJECT-SUMMARY.md:1991:- ✓ 对齐13个function-based views的路由和响应结构
docs/PROJECT-SUMMARY.md:2135:  - Live probe硬门禁（XG_RUN_LIVE_API_TEST=1）
docs/PROJECT-SUMMARY.md:2212:- ⏭ 下一步：讨论Step 2C字段覆盖 vs Step 3同步命令优先级
docs/PROJECT-SUMMARY.md:2370:- 场景覆盖：skip透传/existing候选/missing不创建/role冲突/只读保证/字段gap warning/空输入/混合场景
docs/PROJECT-SUMMARY.md:2393:- 106：Codex推荐选项组合2（扩展模型+不覆盖name）
docs/PROJECT-SUMMARY.md:2401:- 不允许API覆盖name字段（避免CSV与API反复冲突）
docs/PROJECT-SUMMARY.md:2462:- 未同步后端已完成的审批流程变更（宿管员→辅导员）
docs/PROJECT-SUMMARY.md:2466:  - 审批列表页：当前用户角色"辅导员"→"宿管员"
docs/PROJECT-SUMMARY.md:2467:  - 审批列表项：审批步骤"辅导员审批"→"宿管员审批"
docs/PROJECT-SUMMARY.md:2469:  - 详情页时间轴：审批步骤"辅导员审批"→"宿管员审批"
docs/PROJECT-SUMMARY.md:2483:  - roleMap新增：dorm_manager: '宿管员'
docs/PROJECT-SUMMARY.md:2506:  - 角色选择器（宿管员/辅导员/学工部）
docs/PROJECT-SUMMARY.md:2531:- ✓ 内容覆盖：系统概述、部署指南、用户操作、常见问题、测试账号、API端点、数据库表结构
docs/PROJECT-SUMMARY.md:2538:- ✓ **测试账号错误**：文档写password123，实际学生密码=学号，辅导员=T001/T002，学工部=D001，宿管员未实现
docs/PROJECT-SUMMARY.md:2540:- ✓ **小程序角色守卫冲突**：文档说宿管员可进审批列表，实际小程序只允许counselor/dean；添加警告说明
docs/PROJECT-SUMMARY.md:2555:- docs/操作说明书.md:159-164 (宿管员登录警告)
docs/PROJECT-SUMMARY.md:2570:### Claude-Codex协作分析XG API数据覆盖度
docs/PROJECT-SUMMARY.md:2580:- **字段覆盖度：** 27% (3/11完全覆盖), 64% (7/11缺失)
docs/PROJECT-SUMMARY.md:2581:- **必填字段覆盖：** 57% (4/7), 关键业务字段0% (0/3)
docs/PROJECT-SUMMARY.md:2582:- **数据质量评分：** 95/100 (A级) - 提供的字段质量优秀但业务覆盖不足
docs/PROJECT-SUMMARY.md:2601:  - 优点：业务完整性100%, 风险可控, 实施快速
docs/PROJECT-SUMMARY.md:2632:- ✅ XG API数据覆盖度分析完成
docs/PROJECT-SUMMARY.md:2691:- 列：校区,楼栋,寝室,学生姓名,性别,专业,学院名称,班级,层次,年级
docs/PROJECT-SUMMARY.md:2701:- 列：序号,楼栋号,职工号,姓名,电话
docs/PROJECT-SUMMARY.md:2714:- 影响：无法唯一标识学生或无法路由到正确院系
docs/PROJECT-SUMMARY.md:2719:- 影响：审批路由失效，无法实现"辅导员只审批自己负责班级"
docs/PROJECT-SUMMARY.md:2721:**缺陷3：部分宿管员无工号**
docs/PROJECT-SUMMARY.md:2730:| 辅导员表 | 100% | ✅ 满足 | - |
docs/PROJECT-SUMMARY.md:2731:| 宿管员表 | 75% | ⚠️ 基本满足 | 部分工号缺失 |
docs/PROJECT-SUMMARY.md:2739:- 补充宿管员工号
docs/PROJECT-SUMMARY.md:2771:   - 错误：认为File1与File2"无法关联"
docs/PROJECT-SUMMARY.md:2772:   - 原因：遗漏了File2的FY字段（学院信息），只检查了YXMC（校名）
docs/PROJECT-SUMMARY.md:2777:   - File2有：XH(学号)、FY(学院)、BH(班号)
docs/PROJECT-SUMMARY.md:2784:   - 覆盖率：5,559/5,830行（95.35%），准确率~100%
docs/PROJECT-SUMMARY.md:2785:   - 缺口：271行研究生（File1班级为空，File2无研究生数据）
docs/PROJECT-SUMMARY.md:2788:4. **审批路由问题识别**
docs/PROJECT-SUMMARY.md:2789:   - 楼栋→宿管员：覆盖完整但一对多，184/196班级跨多个楼栋
docs/PROJECT-SUMMARY.md:2791:   - 需要3个业务确认（辅导员粒度、宿管员规则、研究生范围）
docs/PROJECT-SUMMARY.md:2812:- 量化分析优于主观判断：Codex提供覆盖率/准确率/缺口清单
docs/PROJECT-SUMMARY.md:2824:1. **数据合并策略** - File1为基准（5830行全保留），File2补充字段，缺失留空
docs/PROJECT-SUMMARY.md:2825:2. **班级字段处理** - class_id暂时为空，不用于路由
docs/PROJECT-SUMMARY.md:2826:3. **审批流程调整** - 2级审批（宿管员按楼栋→辅导员按学院），移除学工部审批
docs/PROJECT-SUMMARY.md:2828:5. **寝室号未来补充** - File3后续补充寝室号，实现一对一精确路由
docs/PROJECT-SUMMARY.md:2836:| ClassMapping缺失 | 决策3：改为楼栋+学院路由 | ✅ 已解除 |
docs/PROJECT-SUMMARY.md:2837:| 楼栋一对多问题 | 决策3：楼栋级路由 | ✅ 已解除 |
docs/PROJECT-SUMMARY.md:2844:| 审批流程 | 3级（宿管→辅导→学工部） | 2级（宿管→辅导） | 中等 |
docs/PROJECT-SUMMARY.md:2845:| 路由方式 | ClassMapping(class_id) | Building+College | 重大 |
docs/PROJECT-SUMMARY.md:2848:| 数据覆盖 | 5559行 | 5830行全部 | 扩大 |
docs/PROJECT-SUMMARY.md:2851:- Phase 1: 数据准备（0.5天）- 合并File1+File2，规范化学院
docs/PROJECT-SUMMARY.md:2852:- Phase 2: 系统调整（1-1.5天）- 审批流程、路由逻辑、权限控制
docs/PROJECT-SUMMARY.md:2853:- Phase 3: 数据导入（0.5天）- 导入5830学生+辅导员+宿管员
docs/PROJECT-SUMMARY.md:2870:1. **P0-1: 空学号无法导入** - User.user_id是必填主键，但271研究生+File2未匹配学生缺学号
docs/PROJECT-SUMMARY.md:2871:2. **P0-2: 多宿管员冲突** - Approval.approver是单FK，无法支持"任一宿管员审批"
docs/PROJECT-SUMMARY.md:2874:**Phase 0数据门禁脚本（已实现）：**
docs/PROJECT-SUMMARY.md:2879:| merge_student_data.py | File1+File2合并，输出user_id/student_no/source | ✅ 完成 |
docs/PROJECT-SUMMARY.md:2880:| validate_routing_coverage.py | 100%路由覆盖验证（楼栋→宿管，学院→辅导） | ✅ 完成 |
docs/PROJECT-SUMMARY.md:2885:- 多宿管员MVP简化：每楼栋指定唯一primary manager
docs/PROJECT-SUMMARY.md:2886:- 路由门禁：exit 0当100%覆盖，否则exit 1阻断实施
docs/PROJECT-SUMMARY.md:2889:- Phase 0: 数据验证门禁（1-1.5天，新增）
docs/PROJECT-SUMMARY.md:2902:**Commit:** a142ad8 "feat: Phase 0数据门禁脚本实现" (+547 lines)
docs/PROJECT-SUMMARY.md:2912:- File3后续补充room_number实现一对一精确路由
docs/PROJECT-SUMMARY.md:2913:- 路径：Phase 1楼栋级 → Phase 2寝室级
docs/PROJECT-SUMMARY.md:2915:**决策2：楼栋匹配规则**
docs/PROJECT-SUMMARY.md:2916:- 按楼栋名称吻合匹配（exact或normalized）
docs/PROJECT-SUMMARY.md:2919:**决策3：File2独有116行处理**
docs/PROJECT-SUMMARY.md:2921:- 总学生数：5830（File1）+ 116（File2独有）= 5946行
docs/PROJECT-SUMMARY.md:2930:- merge_student_data.py：增加File2独有行处理逻辑
docs/PROJECT-SUMMARY.md:2932:  - 追加未匹配File2行到输出
.omc/collaboration/artifacts/20260530-1942-codex-completion-boundary-analysis.md:50:路径4“继续扩展 skeleton”不建议。当前没有 WeChat DevTools 反馈，继续写页面很容易在组件语法、路由、生命周期、网络限制上返工，而且收益偏离 Week 3 共识。
docs/Excel数据源实际分析结果.md:17:校区, 楼栋名称, 寝室号, 学生姓名, 性别, 专业, 学院名称, 班级, 层次, 年级
docs/Excel数据源实际分析结果.md:77:Row 1 (header): 序号, 楼栋号, 职工号, 姓名, 电话
docs/Excel数据源实际分析结果.md:133:  - 选文件2 → 有学号，但无学院（审批路由失效）
docs/Excel数据源实际分析结果.md:153:- 审批路由无法工作
docs/Excel数据源实际分析结果.md:157:### 缺陷3：部分宿管员无工号
docs/Excel数据源实际分析结果.md:163:- 这些宿管员无法导入系统（user_id必填）
docs/Excel数据源实际分析结果.md:176:| 数据量 | 100% | 5675-5830人符合预期 |
docs/Excel数据源实际分析结果.md:183:| 字段完整性 | 100% | 所有必需字段齐全 |
docs/Excel数据源实际分析结果.md:184:| 数据质量 | 100% | 工号格式统一 |
docs/Excel数据源实际分析结果.md:185:| **综合评分** | **100%** | **满足要求** |
docs/Excel数据源实际分析结果.md:187:### 3.3 宿管员表（User - role=dorm_manager）
docs/Excel数据源实际分析结果.md:231:**步骤3：补充宿管员工号**
docs/Excel数据源实际分析结果.md:278:**宿管员文件必需列：**
docs/Excel数据源实际分析结果.md:335:| 辅导员表 | ✅ 100% | 无 | 可直接使用 |
docs/Excel数据源实际分析结果.md:336:| 宿管员表 | ⚠️ 75% | 部分工号缺失 | 补充工号 |
docs/XG-API-COLLECTION-TEST-GUIDE.md:142:- [ ] 分页测试覆盖至少3页
docs/XG-API-ACTUAL-DATA-SAMPLES.md:51:| number（学号） | 20 | 0 | 0 | 100% | ✓ 优秀 |
docs/XG-API-ACTUAL-DATA-SAMPLES.md:52:| name（姓名） | 20 | 0 | 0 | 100% | ✓ 优秀 |
docs/XG-API-ACTUAL-DATA-SAMPLES.md:54:| status（状态） | 20 | 0 | 0 | 100% | ✓ 优秀 |
docs/XG-API-ACTUAL-DATA-SAMPLES.md:65:| user_identity（身份信息） | 20 | 0 | 100% | ✓ 优秀 |
docs/XG-API-ACTUAL-DATA-SAMPLES.md:66:| department（部门） | 20 | 0 | 100% | ✓ 优秀 |
docs/XG-API-ACTUAL-DATA-SAMPLES.md:67:| parent_dep（父级部门） | 20 | 0 | 100% | ✓ 优秀 |
.omc/collaboration/artifacts/test-coverage-claude-response.md:13:> "数据隔离测试不足" 中的列表隔离已经被 test_list_permissions.py 覆盖
docs/用户需求最终确认与实施方案.md:19:| **File 3** | `2026年社区辅导员信息统计表.xls` | 宿管员数据（按楼栋） | 33楼栋 |
docs/用户需求最终确认与实施方案.md:21:| **File 5** | `file5_students_5946.csv` | 合并输出文件（File1+File2全部） | 5946行 |
docs/用户需求最终确认与实施方案.md:36:- File2 (5675行) 补充学号(XH)、班号(BH)等字段
docs/用户需求最终确认与实施方案.md:37:- File2没有的155行学生（File1独有）：补充字段留空
docs/用户需求最终确认与实施方案.md:38:- File2独有的116行学生：导入为额外学生（用户决策3）
docs/用户需求最终确认与实施方案.md:39:- 271行研究生：补充字段留空（File2无研究生数据）
docs/用户需求最终确认与实施方案.md:42:- ✓ 解决了"271研究生+116 File2独有学生"问题
docs/用户需求最终确认与实施方案.md:43:- ✓ 全部5946行学生可导入（5830 File1 + 116 File2独有）
docs/用户需求最终确认与实施方案.md:64:> "第一次审批按楼栋数据向宿管员申请，第一次审批通过后，再按学院向辅导员发起第二次审批"
docs/用户需求最终确认与实施方案.md:68:学生提交 → 宿管员审批(by class_id) → 辅导员审批(by class_id) → 学工部审批 → 完成
docs/用户需求最终确认与实施方案.md:73:学生提交 → 宿管员审批(by 楼栋) → 辅导员审批(by 学院) → 完成（保存结果）
docs/用户需求最终确认与实施方案.md:78:- 路由方式从 `class_id` 改为 `building` + `college`
docs/用户需求最终确认与实施方案.md:83:- ⚠️ 需要修改路由逻辑
docs/用户需求最终确认与实施方案.md:85:- ✓ 解决"楼栋跨班级"问题
docs/用户需求最终确认与实施方案.md:110:| 宿管员 (dorm_manager) | 第一次审批（按楼栋） | 只看自己负责楼栋的申请 |
docs/用户需求最终确认与实施方案.md:123:### 确认1: 楼栋审批关系
docs/用户需求最终确认与实施方案.md:126:> "楼栋按文件5与文件3中共同的楼栋字段为审批关系设定"
docs/用户需求最终确认与实施方案.md:129:- File5 (学生).楼栋名称 ↔ File3 (宿管员).楼栋号
docs/用户需求最终确认与实施方案.md:131:- 一个楼栋对应多个宿管员：任一人可审批（待确认）
docs/用户需求最终确认与实施方案.md:139:- File5 (学生) 有：楼栋名称 + 寝室号 ✓
docs/用户需求最终确认与实施方案.md:140:- File3 (宿管员) 有：楼栋号 ✓，无寝室号 ✗
docs/用户需求最终确认与实施方案.md:144:- 路由升级：楼栋级（一对多）→ 楼栋+寝室号级（一对一）
docs/用户需求最终确认与实施方案.md:147:- **Phase 1（当前）：** 按楼栋路由（building-level）
docs/用户需求最终确认与实施方案.md:148:- **Phase 2（File3补充后）：** 按楼栋+寝室号路由（room-level，精确一对一）
docs/用户需求最终确认与实施方案.md:166:- 271研究生 + File2未匹配学生缺少学号
docs/用户需求最终确认与实施方案.md:167:- 与"全部5946行可导入"矛盾（5830 File1 + 116 File2独有）
docs/用户需求最终确认与实施方案.md:178:#### P0-2: 多宿管员与单审批人模型冲突
docs/用户需求最终确认与实施方案.md:181:- 文档建议"任一宿管员可审批"
docs/用户需求最终确认与实施方案.md:189:- 每栋楼指定唯一主责宿管员
docs/用户需求最终确认与实施方案.md:196:- Phase 2只说"路由逻辑重构"但未列完整清单
docs/用户需求最终确认与实施方案.md:203:  2. 提交路由重构（apps/applications/views.py:147-179）
docs/用户需求最终确认与实施方案.md:204:  3. 审批通过路由重构（apps/approvals/views.py:149-174）
docs/用户需求最终确认与实施方案.md:223:| 班级字段缺失 | ⚠️ File1有，File2格式不同 | 决策2：暂时为空 | ✅ 已解除 |
docs/用户需求最终确认与实施方案.md:225:| 楼栋→宿管员一对多 | ⚠️ 无法确定选主规则 | 决策3：楼栋级路由 | ✅ 已解除 |
docs/用户需求最终确认与实施方案.md:239:user_id        # 学号（File2补充，可能为空）
docs/用户需求最终确认与实施方案.md:244:building_name  # 楼栋名称（File1） - 第一次审批路由键
docs/用户需求最终确认与实施方案.md:245:room_number    # 寝室号（File1） - 未来精确路由键
docs/用户需求最终确认与实施方案.md:246:department     # 学院名称（File1规范化） - 第二次审批路由键
docs/用户需求最终确认与实施方案.md:247:class_id       # 班级（可为空） - 不用于路由
docs/用户需求最终确认与实施方案.md:252:phone          # 手机号（File2补充）
docs/用户需求最终确认与实施方案.md:253:email          # 邮箱（File2补充）
docs/用户需求最终确认与实施方案.md:256:**DormManager (用户表 - 宿管员角色)：**
docs/用户需求最终确认与实施方案.md:261:building       # 负责楼栋（File3）
docs/用户需求最终确认与实施方案.md:296:- `PENDING`: 学生已提交，等待宿管员审批
docs/用户需求最终确认与实施方案.md:297:- `DORM_MANAGER_APPROVED`: 宿管员已通过，等待辅导员审批
docs/用户需求最终确认与实施方案.md:301:### 4.3 路由逻辑变更
docs/用户需求最终确认与实施方案.md:303:**当前路由（基于ClassMapping）：**
docs/用户需求最终确认与实施方案.md:313:**新路由（基于Building + Department）：**
docs/用户需求最终确认与实施方案.md:317:        # 第一次审批：按楼栋查宿管员
docs/用户需求最终确认与实施方案.md:333:| 操作 | 学生 | 宿管员 | 辅导员 | 学工管理员 |
docs/用户需求最终确认与实施方案.md:337:| 第一次审批（楼栋） | ✗ | ✓ | ✗ | ✗ |
docs/用户需求最终确认与实施方案.md:338:| 查看楼栋范围申请 | ✗ | ✓ | ✗ | ✗ |
docs/用户需求最终确认与实施方案.md:351:**修正后：** 4-6天（增加Phase 0数据门禁）
docs/用户需求最终确认与实施方案.md:353:### Phase 0: 数据画像与路由门禁（1-1.5天）
docs/用户需求最终确认与实施方案.md:355:**目标：** 关闭3个P0阻塞，确保数据可导入且路由100%覆盖
docs/用户需求最终确认与实施方案.md:365:    # File2未匹配：TMP2026_{row}
docs/用户需求最终确认与实施方案.md:371:- `student_no`: 真实学号（可空，来自File2的XH）
docs/用户需求最终确认与实施方案.md:375:**Task 0.2: File1+File2合并与完整报告（0.5天）**
docs/用户需求最终确认与实施方案.md:383:    # - file2_only_count: 116
docs/用户需求最终确认与实施方案.md:390:- `file5_students_5946.csv` - 全部5946行，user_id非空（5830 File1 + 116 File2独有）
docs/用户需求最终确认与实施方案.md:393:**Task 0.3: 学院/楼栋规范化字典（0.2天）**
docs/用户需求最终确认与实施方案.md:400:**楼栋规范化（需File3数据）：**
docs/用户需求最终确认与实施方案.md:401:- `building_normalization_map.json` - 33个楼栋映射（待File3提供后创建）
docs/用户需求最终确认与实施方案.md:402:- 依赖：需File3楼栋名称与File1对比，创建映射表
docs/用户需求最终确认与实施方案.md:405:**状态：** 学院规范化✓完成，楼栋规范化⏳pending File3
docs/用户需求最终确认与实施方案.md:407:**Task 0.4: 主责宿管员指定（0.3天）**
docs/用户需求最终确认与实施方案.md:411:- 如楼栋有多人，人工或按默认规则（首位/编号最小）选主责
docs/用户需求最终确认与实施方案.md:414:**Task 0.5: 路由覆盖验证（0.2天）**
docs/用户需求最终确认与实施方案.md:422:    # 输出100%覆盖报告或失败清单
docs/用户需求最终确认与实施方案.md:426:门禁标准：
docs/用户需求最终确认与实施方案.md:427:- ✓ 5946行学生user_id非空且唯一（5830 File1 + 116 File2独有）
docs/用户需求最终确认与实施方案.md:428:- ✓ 100%学生可路由到宿管员
docs/用户需求最终确认与实施方案.md:429:- ✓ 100%学生可路由到辅导员
docs/用户需求最终确认与实施方案.md:445:**任务1.2：File1 + File2合并脚本**
docs/用户需求最终确认与实施方案.md:450:    # 2. 读取File2 (5675行) 作为补充
docs/用户需求最终确认与实施方案.md:452:    # 4. File2有的：补充学号、专业、班号等字段
docs/用户需求最终确认与实施方案.md:453:    # 5. File2没有的：对应字段留空
docs/用户需求最终确认与实施方案.md:454:    # 6. File2独有的116行：追加为额外学生（用户决策3）
docs/用户需求最终确认与实施方案.md:455:    # 7. 输出File5 (5946行：5830+116)
docs/用户需求最终确认与实施方案.md:460:- `file5_students_5946.csv` - 完整学生数据（5830 File1 + 116 File2独有）
docs/用户需求最终确认与实施方案.md:461:- `file3_dorm_managers.csv` - 宿管员数据（33楼栋）
docs/用户需求最终确认与实施方案.md:471:**任务2.2：路由逻辑重构**
docs/用户需求最终确认与实施方案.md:472:- 创建 `BuildingApprovalRouter` - 楼栋→宿管员路由
docs/用户需求最终确认与实施方案.md:473:- 创建 `DepartmentApprovalRouter` - 学院→辅导员路由
docs/用户需求最终确认与实施方案.md:499:# Step 3: 导入宿管员（33楼栋）
docs/用户需求最终确认与实施方案.md:502:# Step 4: 验证路由
docs/用户需求最终确认与实施方案.md:507:**前置门禁：**
docs/用户需求最终确认与实施方案.md:509:- ✓ 每个学生的楼栋能找到至少1个宿管员
docs/用户需求最终确认与实施方案.md:517:- 宿管员界面：查看楼栋范围申请+第一次审批
docs/用户需求最终确认与实施方案.md:530:2. 按楼栋路由到正确宿管员
docs/用户需求最终确认与实施方案.md:531:3. 宿管员审批通过
docs/用户需求最终确认与实施方案.md:532:4. 按学院路由到正确辅导员
docs/用户需求最终确认与实施方案.md:536:8. 权限隔离验证（学生/宿管/辅导/管理员）
docs/用户需求最终确认与实施方案.md:538:**总时间：** 4-6天（原计划2.5-3天，增加Phase 0数据门禁1-1.5天）
docs/用户需求最终确认与实施方案.md:541:- M0: Phase 0完成，路由100%覆盖验证通过（1-1.5天）
docs/用户需求最终确认与实施方案.md:551:### 寝室号精确路由升级
docs/用户需求最终确认与实施方案.md:570:**路由逻辑升级：**
docs/用户需求最终确认与实施方案.md:576:    # 精确匹配：楼栋+寝室号 → 唯一宿管员
docs/用户需求最终确认与实施方案.md:595:### 风险1: 楼栋名称不匹配
docs/用户需求最终确认与实施方案.md:598:- File5楼栋名："荷园2栋"
docs/用户需求最终确认与实施方案.md:599:- File3楼栋号："荷园二栋"
docs/用户需求最终确认与实施方案.md:600:- 字符串不匹配导致路由失败
docs/用户需求最终确认与实施方案.md:603:- 建立楼栋名称规范化表（类似学院规范化）
docs/用户需求最终确认与实施方案.md:604:- 导入前验证：所有File5楼栋能在File3中找到对应
docs/用户需求最终确认与实施方案.md:607:### 风险2: 多宿管员选择规则未定
docs/用户需求最终确认与实施方案.md:610:- 一个楼栋有3个宿管员
docs/用户需求最终确认与实施方案.md:615:- 方案B：指定主责宿管员（File3补充主责标记）
docs/用户需求最终确认与实施方案.md:645:- ⏳ `scripts/merge_student_data.py` - File1+File2合并
docs/用户需求最终确认与实施方案.md:646:- ⏳ `scripts/validate_building_routing.py` - 楼栋路由验证
docs/用户需求最终确认与实施方案.md:647:- ⏳ `scripts/validate_department_routing.py` - 学院路由验证
docs/用户需求最终确认与实施方案.md:652:- ⏳ `file3_dorm_managers.csv` - 宿管员数据
docs/用户需求最终确认与实施方案.md:659:- ⏳ 楼栋路由器实现
docs/用户需求最终确认与实施方案.md:660:- ⏳ 学院路由器实现
docs/用户需求最终确认与实施方案.md:671:| DEC-001 | File1为基准合并File2 | 用户 | 2026-06-05 | 保留全部5830学生 |
docs/用户需求最终确认与实施方案.md:673:| DEC-003 | 2级审批（楼栋→学院） | 用户 | 2026-06-05 | 移除学工部审批 |
docs/用户需求最终确认与实施方案.md:675:| DEC-005 | 寝室号未来补充 | 用户 | 2026-06-05 | 精确路由需求 |
docs/contracts/contract-v0.1.md:412:        # 固定返回规则（覆盖所有状态）
docs/数据对接说明文档.md:237:- 班级映射覆盖率（所有学生的class_id都有对应辅导员）
docs/Excel数据源分析与需求对比.md:15:| 文件3 | 2026年社区辅导员信息统计表.xls | 30.0K | 宿管员信息 |
docs/Excel数据源分析与需求对比.md:28:| **class_id** | **班级ID** | string | ✓ | **审批路由关键字段** | **文件1或文件2** |
docs/Excel数据源分析与需求对比.md:54:### 2.3 宿管员表（User - role=dorm_manager）
docs/Excel数据源分析与需求对比.md:59:| name | 姓名 | string | ✓ | 宿管员姓名 | 文件3 |
docs/Excel数据源分析与需求对比.md:116:### 3.3 宿管员文件检查（文件3）
docs/Excel数据源分析与需求对比.md:133:5. ✅ 文件3包含宿管员工号、姓名
docs/Excel数据源分析与需求对比.md:197:3. `dorm_managers.csv` - 宿管员数据
docs/phase4c-xg-field-coverage.md:1:# 学工系统用户API字段覆盖报告
docs/phase4c-xg-field-coverage.md:31:| `number` | string | 100% | `"2025110140314"` | 学号/工号 |
docs/phase4c-xg-field-coverage.md:32:| `name` | string | 100% | `"乐绍钧"` | 用户姓名 |
docs/phase4c-xg-field-coverage.md:33:| `user_identity` | object | 100% | `{"id": 4, "name": "学生"}` | 身份类型（对象非字符串） |
docs/phase4c-xg-field-coverage.md:34:| `department` | array | 100% | `[{"name": "计算机学院", "level": 2}]` | 院系（数组非字符串） |
docs/phase4c-xg-field-coverage.md:36:| `status` | number | 100% | `1` | 账号状态（1=正常） |
docs/phase4c-xg-field-coverage.md:119:| `User.class_id` | 未知 | 🔴 缺失 | **学生必填，API无法提供**。<br>- 继续由CSV/手工维护<br>- API同步时不覆盖此字段<br>- 新用户如果缺失`class_id`，标记为`skip_reason: missing_class_id` |
docs/phase4c-xg-field-coverage.md:120:| `User.is_graduating` | 未知 | 🔴 缺失 | **学生必填，API无法提供**。<br>- 继续由CSV/手工维护<br>- API同步时不覆盖此字段<br>- 新用户如果缺失，标记为`skip_reason: missing_is_graduating` |
docs/phase4c-xg-field-coverage.md:121:| `User.graduation_year` | 未知 | 🔴 缺失 | **学生必填，API无法提供**。<br>- 继续由CSV/手工维护<br>- API同步时不覆盖此字段<br>- 新用户如果缺失，标记为`skip_reason: missing_graduation_year` |
docs/phase4c-xg-field-coverage.md:147:| `class_id`缺失 | 保持原值（不覆盖），新用户跳过并标记`missing_class_id` |
docs/phase4c-xg-field-coverage.md:148:| `is_graduating`缺失 | 保持原值（不覆盖），新用户跳过并标记`missing_is_graduating` |
docs/phase4c-xg-field-coverage.md:149:| `graduation_year`缺失 | 保持原值（不覆盖），新用户跳过并标记`missing_graduation_year` |
docs/phase4c-xg-field-coverage.md:182:**在字段未完全覆盖前，API只能补充或更新可确定字段，不能替代CSV导入。**
docs/PROJECT-COMPLETION-DECLARATION.md:40:✓ 单元测试：**172/172通过（100%）**  
docs/PROJECT-COMPLETION-DECLARATION.md:42:- H1: 正常审批流程（学生→宿管员→辅导员→学工部→批准）
docs/PROJECT-COMPLETION-DECLARATION.md:43:- H2: 驳回流程（学生→宿管员→辅导员驳回）  
docs/PROJECT-COMPLETION-DECLARATION.md:49:- 字段完整性：number100%, name100%, phone80%, status100%
docs/操作说明书-待改进事项.md:14:3. ✅ 小程序宿管员限制 - 已添加警告说明
docs/操作说明书-待改进事项.md:28:**当前状况：** 第2章"系统部署"仅覆盖安装部署，缺少运维管理内容
docs/操作说明书-待改进事项.md:93:- ✓ 两级审批流程（宿管员→辅导员）
docs/操作说明书-待改进事项.md:100:- ⚠️ 宿管员账号和映射（种子数据缺失）
docs/操作说明书-待改进事项.md:101:- ⚠️ 小程序宿管员审批页（角色守卫限制）
docs/API-DATA-EXAMPLES.md:56:  "approver_name": "宿管员1",
docs/API-DATA-EXAMPLES.md:71:| approver_name | string | 审批人姓名 | 宿管员1 |
docs/API-DATA-EXAMPLES.md:162:### 响应结构（辅导员/宿管员/学工部视角）
docs/API-DATA-EXAMPLES.md:187:- `pending_dorm_manager`: 待宿管员审批
docs/API-DATA-EXAMPLES.md:194:- `dorm_manager`: 宿管员审批
docs/XG-API-数据源全面分析报告.md:18:- 基础字段覆盖：27% (3/11)
docs/XG-API-数据源全面分析报告.md:19:- 必填字段覆盖：57% (4/7)
docs/XG-API-数据源全面分析报告.md:20:- **关键业务字段覆盖：0% (0/3)** ← 核心阻断
docs/XG-API-数据源全面分析报告.md:45:| 序号 | 需求字段 | 必填性 | XG提供字段 | 覆盖状态 | 完整性 | 不满足原因 |
docs/XG-API-数据源全面分析报告.md:47:| 1 | student_id | ✓ 必填 | number | ✅ 满足 | 100% | - |
docs/XG-API-数据源全面分析报告.md:48:| 2 | name | ✓ 必填 | name | ✅ 满足 | 100% | - |
docs/XG-API-数据源全面分析报告.md:49:| 3 | department | ✓ 必填 | department[0].name | ✅ 满足 | 100% | - |
docs/XG-API-数据源全面分析报告.md:56:**必填字段覆盖率：50% (4/8)**  
docs/XG-API-数据源全面分析报告.md:61:| 序号 | 需求字段 | 必填性 | XG提供字段 | 覆盖状态 | 完整性 | 不满足原因 |
docs/XG-API-数据源全面分析报告.md:67:**可选字段覆盖率：33% (1/3)**  
docs/XG-API-数据源全面分析报告.md:72:| 序号 | 需求字段 | 必填性 | XG提供字段 | 覆盖状态 | 不满足原因 |
docs/XG-API-数据源全面分析报告.md:81:**辅导员字段覆盖率：67% (4/6)**  
docs/XG-API-数据源全面分析报告.md:82:**注：** 辅导员数据未进行实际采样验证，覆盖度基于字段结构推断
docs/XG-API-数据源全面分析报告.md:86:| 序号 | 需求字段 | 必填性 | XG提供 | 覆盖状态 | 不满足原因 |
docs/XG-API-数据源全面分析报告.md:92:**班级映射覆盖率：0% (0/3)**  
docs/XG-API-数据源全面分析报告.md:97:| 序号 | 需求字段 | 必填性 | XG用户API提供 | 覆盖状态 | 不满足原因 |
docs/XG-API-数据源全面分析报告.md:103:**宿舍清退覆盖率：0% (0/3)**  
docs/XG-API-数据源全面分析报告.md:141:- ✓ 已实施：API同步时不覆盖class_id字段
docs/XG-API-数据源全面分析报告.md:176:- ✓ 已实施：API不创建新用户，不覆盖is_graduating
docs/XG-API-数据源全面分析报告.md:210:- ✓ 已实施：API不覆盖graduation_year字段
docs/XG-API-数据源全面分析报告.md:321:- 可能覆盖本地已有的有效phone值
docs/XG-API-数据源全面分析报告.md:330:- API同步时跳过空值，不覆盖已有有效值
docs/XG-API-数据源全面分析报告.md:426:| number | 20 | 20 | 0 | 0 | 100% | ✓ 优秀 |
docs/XG-API-数据源全面分析报告.md:427:| name | 20 | 20 | 0 | 0 | 100% | ✓ 优秀 |
docs/XG-API-数据源全面分析报告.md:429:| status | 20 | 20 | 0 | 0 | 100% | ✓ 优秀 |
docs/XG-API-数据源全面分析报告.md:430:| department | 20 | 20 | 0 | 0 | 100% | ✓ 优秀 |
docs/XG-API-数据源全面分析报告.md:431:| user_identity | 20 | 20 | 0 | 0 | 100% | ✓ 优秀 |
docs/XG-API-数据源全面分析报告.md:472:| **综合得分** | **93.5/100** | **100%** | **93.5** |
docs/XG-API-数据源全面分析报告.md:476:**结论：** XG API提供的字段数据质量优秀，但业务字段覆盖度严重不足。
docs/XG-API-数据源全面分析报告.md:501:  ↓ 不覆盖：class_id, is_graduating, graduation_year
docs/XG-API-数据源全面分析报告.md:516:- ✗ XG API覆盖class_id/is_graduating/graduation_year
docs/XG-API-数据源全面分析报告.md:563:- 规则：不覆盖已有有效值
docs/api-samples/notifications_list.json:36:      "message": "您的离校申请已通过宿管员审批。",
.omc/collaboration/artifacts/20260530-1654-codex-github-projects-analysis.md:112:- Codex 增量部署：使用 managed block 和 manifest，避免覆盖 `auth.json`、history、cache、用户默认模型等运行态。
.omc/collaboration/artifacts/20260530-1654-codex-github-projects-analysis.md:119:- **P0 借鉴：受管区块/manifest**。若未来要自动安装 Gemini/Codex/Claude 配置，不要整目录覆盖用户配置。采用 managed block、manifest、备份和 dry-run。
.omc/collaboration/artifacts/20260530-1654-codex-github-projects-analysis.md:160:- **P0 借鉴：清晰角色路由**。Gemini 适合大上下文、长日志、多文件分析；Codex 适合实现与 review；Claude/主 agent 做协调和最终判断。这个边界适合直接写进我们的协议。
.omc/collaboration/artifacts/20260530-1654-codex-github-projects-analysis.md:184:1. **定义三 agent 角色路由**
.omc/collaboration/artifacts/20260530-1654-codex-github-projects-analysis.md:225:3. 用户级全自动 MCP 安装和模板覆盖。
.omc/collaboration/artifacts/20260530-1654-codex-github-projects-analysis.md:250:1. 更新协议：加入角色路由、独立分析规则、Gemini 只读原则、handoff/open-for-peer-analysis 状态。
docs/api-samples/application_detail.json:16:      "approver_name": "宿管员1",
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:14:用户指出“File1与File2存在共同字段”是正确的，旧结论“无法关联”不成立。File2的 `FY/XSH` 确实提供学院字段，学生数据可以高覆盖合并。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:22:采用该规则后，File1中 **5,559/5,830行可安全补齐学号**，覆盖全部非研究生、非空班级学生；剩余 **271行研究生** 在File1中班级为空，且File2没有研究生数据，不能自动补齐学号和class_id。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:24:辅导员侧可从“学院→辅导员”机械生成“班级→辅导员”映射，但这是业务语义降级，不等价于真实班级负责关系。宿管侧“楼栋→宿管员”覆盖完整，但所有楼栋都是一对多宿管员，且当前系统按 `class_id` 的 `ClassMapping` 路由，一个班级普遍跨多个楼栋，不能把楼栋路由无损塞进单一班级宿管员字段。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:27:本科/专升本/第二学位学生学号补全质量高；研究生、宿管员选择规则、真实班级辅导员责任仍是P0上线门控。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:38:| File2行数 | 5,675 |
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:40:| File2唯一姓名 | 5,524 |
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:43:| File2重名姓名数/涉及行 | 132个 / 283行 |
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:45:| File2重复“姓名+学院”键 | 18个键 / 36行 |
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:49:| File1 | File2/File4 |
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:63:但这仍不够安全：File1有1名研究生 `陈静/数学与统计学院` 会被错误匹配到File2同名本科生。原因是该研究生班级为空，而File2不含研究生数据。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:75:这271行全部是File1中的研究生，且班级为空。File2按 `CC` 统计只有本科、专升本、第二学士学位，没有研究生。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:79:- 对非研究生住宿毕业生：可自动补齐学号，准确率可按接近100%处理，但仍建议抽样复核。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:80:- 对全部5,830名File1学生：覆盖率只有95.35%，研究生P0字段缺失。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:81:- 对File2：有116行在File1中没有对应 `姓名+规范化学院`，不能从File1补楼栋/寝室。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:90:4. 对未匹配清单输出人工核验文件，至少包含姓名、学院、专业、层次、年级、File2候选。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:91:5. 对File2存在但File1不存在的116行单独确认：如果不住校或不参与离校流程，可排除；否则需要补楼栋/寝室。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:95:### 3.1 楼栋→宿管员映射：⚠️ 覆盖完整，路由语义不完整
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:101:| File1唯一楼栋 | 33 |
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:102:| File3唯一楼栋 | 36 |
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:103:| File3覆盖File1楼栋 | 33/33 |
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:104:| File1未覆盖楼栋 | 0 |
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:105:| File1中楼栋覆盖学生 | 5,830/5,830 |
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:106:| File1涉及楼栋中含`暂未申请`工号 | 2栋 |
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:109:覆盖度本身没有问题，但存在两个P0级设计风险：
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:111:1. **楼栋到宿管员是一对多。** File1涉及的33栋楼全部在File3中对应多名宿管员，无法从数据本身判断审批应派给哪一位。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:112:2. **当前系统路由不是楼栋级。** 当前 `ClassMapping` 是 `class_id -> dorm_manager + counselor`；而File1中196个非空班级里，184个班级跨多个楼栋，涉及5,304名学生。用“班级→单一宿管员”会错误覆盖大多数班级的住宿实际。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:116:- 如果业务允许“每栋任一有效宿管员都可审批”，需要在系统里明确选主规则或支持多审批人。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:117:- 如果业务要求按学生所在楼栋审批，当前模型应改为提交申请时按学生的 `楼栋名称` 路由宿管员，而不是把宿管员塞进班级映射。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:118:- `暂未申请`工号不能创建用户；如果该楼栋另一名宿管员可作为审批人，可暂不阻塞，但必须确认排班/职责规则。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:122:学院名称规范化后，File4覆盖File1全部19个学院：
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:128:| 规范化后File4覆盖File1学院 | 19/19 |
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:165:### 4.2 ClassMapping / 审批路由
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:170:| class_id -> dorm_manager | 不适合由楼栋数据派生为单一班级宿管员 | ✗ |
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:171:| building -> dorm_manager | File3覆盖完整但一对多 | ⚠️ 需选主/多审批规则 |
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:172:| 研究生审批路由 | File1班级为空；File4有`研究生`辅导员但无法形成class_id | ✗ |
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:182:1. 271名研究生缺学号与class_id，不能通过File2补齐。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:184:3. 宿管员路由需要确认一对多选择规则，并且不应简单落到单一班级宿管员字段。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:196:- 学院辅导员覆盖完整，可快速生成可运行的班级映射草案。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:197:- 缺口集中且可列清单：271名研究生、116名File2独有学生、宿管员一对多规则、真实辅导员粒度确认。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:198:- 相比方案C全量重新获取，增强版更快；相比纯人工方案，自动匹配覆盖率更高、人工工作量更小。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:209:   - 用 `学生姓名 + 规范化学院 + 班级` 匹配 File2 `XM + FY + BH`。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:222:5. 宿管员映射：
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:223:   - 不建议生成 `class_id -> 单一宿管员`。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:224:   - 建议增加或使用学生住宿字段，在申请创建时按学生楼栋查宿管员。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:225:   - 对每栋多宿管员，确认规则：主责宿管员、轮值组、多审批人任选其一。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:228:6. 导入前门禁：
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:232:   - 每个导入学生的楼栋必须能找到至少一个有效 dorm_manager。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:237:1. 你的初始结论“File1/File2无法关联”应废弃；用户纠正成立。
.omc/collaboration/artifacts/20260605-0852-codex-excel-association-review.md:240:4. 如果系统保持当前 `ClassMapping(class_id -> counselor + dorm_manager)`，楼栋宿管策略与模型不匹配，需要改模型/路由或确认降级方案。
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:1:# XG API数据覆盖度审查报告
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:6:**审查类型：** 数据对接覆盖度 / 映射策略审查  
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:16:实际采集数据证明，XG API对身份识别基础字段覆盖较好：`number`、`name`、`status`为100%完整，`user_identity`、`department`、`parent_dep`关联对象为100%存在，`phone`为80%有效。数据量侧也确认有32,039条用户记录。
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:18:但毕业生离校审批的核心业务字段没有被实际样本覆盖：`class_id`、`graduation_year`、`is_graduating`、班级-辅导员映射、宿舍清退状态均缺失或不属于该用户API。缺这些字段时，系统无法可靠完成申请资格判定、辅导员自动分配、毕业批次归档和宿舍清退阻断。
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:20:推荐策略维持：**CSV主导 + XG API补充**。API仅更新已存在学生的非核心字段，如 `phone`、`email`、`department`、`active/status`；不创建新学生、不覆盖核心业务字段、不自动停用本地用户。
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:28:需求文档明确 `class_id` 用于班级-辅导员映射和审批人分配，且导入后需要验证班级映射覆盖率。见 `docs/数据对接说明文档.md:195`、`:237`。
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:36:- 20条采样中：`number`、`name`、`status`完整率100%，`phone`完整率80%。见 `docs/XG-API-ACTUAL-DATA-SAMPLES.md:47-54`。
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:37:- `user_identity`、`department`、`parent_dep`存在率100%，`user`对象90%。见 `docs/XG-API-ACTUAL-DATA-SAMPLES.md:65-67`。
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:46:## 3. 字段覆盖度评估
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:48:| 业务域 | 需求字段 | XG实际覆盖 | 覆盖结论 |
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:50:| 学生身份识别 | `student_id/name` | `number/name` 100% | 可用于匹配已有用户 |
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:54:| 审批路由 | `class_id` + `ClassMapping` | 未见稳定班级ID或映射关系 | P0缺口 |
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:56:| 班级-辅导员映射 | `class_id/counselor_employee_id` | 未覆盖 | P0缺口 |
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:57:| 宿舍清退 | `checkout_status/checkout_date/source_updated_at` | 当前XG用户API未覆盖 | 需独立宿舍API或人工凭证流程 |
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:58:| 账号状态 | `active` | `status` 100%，示例规则为1=>True | 可作为补充字段，但需枚举确认 |
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:60:从“学生CSV必填字段”角度看，XG实际样本只稳定覆盖 `student_id/name/department` 中的基础身份展示字段；`major/class_id/grade/graduation_year/is_graduating` 未覆盖。因此它不具备创建毕业生账号主数据的完整性。
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:102:| 业务覆盖质量 | 低 | 缺核心毕业/班级/映射字段 | 阻断API替代CSV |
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:105:特别注意：`backend/reports/xg_collection_test_20260603_033437.json` 中分页测试记录每页10条，但 `volume_tests.statistics` 使用 `per_page=1`，导致总页数和全量耗时估算与文档摘要不一致。该问题不影响字段覆盖结论，但会影响全量同步计划和运维估算。
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:133:### P1：字段覆盖文档仍是“待live测试确认”状态
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:152:- 用XG API覆盖 `class_id`、`is_graduating`、`graduation_year`。
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:163:3. 提供辅导员 `employee_id`及班级-辅导员关系，且能覆盖所有目标毕业班。
.omc/collaboration/artifacts/20260603-1605-codex-xg-data-coverage-review.md:180:| P2 | `phone` 20%空字符串 | 联系信息不完整 | 空字符串归一化，避免覆盖已有有效值 |
.omc/collaboration/artifacts/20260530-0902-claude-codex-consensus-discussion.md:34:| P0 #1 | 3-agent角色路由 | ✅ 同意，应写入协议 |
.omc/collaboration/artifacts/20260530-0902-claude-codex-consensus-discussion.md:181:1. **3-agent角色路由定义** (Codex P0 #1)
.omc/collaboration/artifacts/20260530-0902-claude-codex-consensus-discussion.md:257:1. 先实施P0其他3项(角色路由、独立分析协议、journal校验)
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:1:# Phase 0 路由覆盖P0阻塞分析
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:12:Phase 0 Task 0.5（路由覆盖验证）执行结果：
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:13:- **辅导员路由覆盖率：** 100.0% ✓ (5946/5946)
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:14:- **宿管员路由覆盖率：** 98.0% ✗ (5830/5946)
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:15:- **完整路由覆盖率：** 98.0% ✗ (5830/5946)
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:17:**门禁要求：** 100%路由覆盖率（文档要求）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:19:**阻塞原因：** 116名File2独有学生缺少楼栋数据，无法路由至宿管员。
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:29:**受影响学生数量：** 116人
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:46:- 全部116人building字段为空字符串
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:48:- user_id_source = 'file2_only'（来自File2但不在File1中）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:49:- department字段非空（可以路由到辅导员）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:58:- 学生姓名、学院名称、**楼栋名称**、**寝室号**、专业、年级、班级、层次
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:60:**File2字段（5675行）：**
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:62:- **缺失：** 楼栋名称、寝室号
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:66:2. File2补充学号、手机号、邮箱等字段
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:67:3. File2独有的116行学生追加到输出（用户决策3，2026-06-05）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:68:4. File2独有学生的building_name和room_number字段为空字符串
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:70:**结论：** File2数据源本身不包含楼栋/寝室信息，因此File2独有的116名学生无法获得building_name字段，导致无法路由到宿管员。
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:79:- ✗ Phase 0 Task 0.5验证失败（98.0% vs 100%门禁要求）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:84:- 116名学生无法提交离校申请（缺少第一级审批人-宿管员）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:85:- 占总学生数的1.95%（116/5946）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:92:学生提交 → 宿管员审批(by 楼栋) → 辅导员审批(by 学院) → 完成
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:95:**第一级审批路由：** building_name → DormManager
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:96:- 必需字段：building_name（楼栋名称）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:97:- 当前状态：116人building_name为空，路由失败
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:99:**第二级审批路由：** department → Counselor  
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:101:- 当前状态：5946人全部有department，路由成功 ✓
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:107:### 选项1: 接受98%覆盖率作为可接受标准
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:109:**描述：** 修改Phase 0门禁要求，将100%覆盖率降低为98%（或"File1学生100%覆盖率"）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:118:- 116名学生无法使用系统（占1.95%）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:119:- 可能需要后续手工处理这116人的离校流程
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:121:**实施成本：** 低（仅需修改文档门禁标准）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:123:**风险：** 中（用户可能要求这116人也能使用系统）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:127:### 选项2: 排除File2独有学生，仅导入File1学生
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:129:**描述：** 回退用户决策3（2026-06-05），不导入File2独有的116名学生
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:132:- 达到100%覆盖率（5830/5830）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:133:- 通过Phase 0门禁，可以进入Phase 1-5
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:137:- 违反用户明确决策（用户要求导入File2独有学生）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:138:- 116名可能是合法在校生被排除系统外
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:148:### 选项3: 要求用户提供File2独有学生的楼栋数据
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:150:**描述：** 暂停Phase 0，要求用户补充116名学生的楼栋/寝室数据
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:153:- 达到100%覆盖率（5946/5946）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:160:- 可能暴露File2数据质量问题
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:170:**推荐：选项1（接受98%覆盖率）+ 后续改进路径**
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:174:1. **业务现实：** File2独有的116名学生确实缺少楼栋数据，这是数据源限制而非技术问题
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:175:2. **影响范围可控：** 仅影响1.95%的学生（116/5946）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:176:3. **辅导员路由完整：** 100%覆盖率已达成，第二级审批无阻塞
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:178:5. **符合用户决策：** 用户明确要求导入File2独有学生（决策3），不应该回退
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:184:1. 修改Phase 0门禁标准：
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:185:   - 原标准：100%路由覆盖率
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:186:   - 新标准：File1学生100%覆盖率（5830/5830）+ 辅导员路由100%覆盖率（5946/5946）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:190:   - 在Task 0.5验证结果中标注：98.0%宿管员覆盖率（File1学生100%，File2独有学生0%）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:193:   - 116名File2独有学生暂时无法使用系统
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:194:   - 需要用户后续提供楼栋数据
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:200:5. 与用户沟通116名学生情况，确认：
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:202:   - 用户是否能提供楼栋数据？
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:207:6. 如用户提供116名学生楼栋数据：
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:209:   - 重新导入这116名学生
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:210:   - 达到100%完整覆盖率
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:216:**如果用户坚持100%覆盖率：** 执行选项3，暂停Phase 0，等待用户提供数据
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:218:**如果用户同意排除File2独有学生：** 执行选项2，回退决策3，仅导入5830名File1学生
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:231:- File1学生：5830人（100%有楼栋数据）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:232:- File2独有学生：116人（0%有楼栋数据）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:234:- 宿管员覆盖率：98.0%（5830/5946）
.omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md:235:- 辅导员覆盖率：100.0%（5946/5946）
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:14:**Codex判断正确：我的初始分析结论"File1与File2无法关联"应被废弃。**
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:17:- 在首次分析File2时，我只检查了 YXMC 字段（值为"黄冈师范学院"校名）
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:18:- 我错误地认为File2缺少学院/院系字段
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:37:   - 覆盖率95.35% (5,559/5,830行)
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:38:   - 准确率接近100%（需抽样验证）
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:39:   - 剩余271行研究生无法自动匹配（File1班级为空，File2无研究生数据）
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:41:3. **楼栋→宿管员映射问题** ✓
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:42:   - 覆盖度完整（33/33楼栋）
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:43:   - 但存在一对多关系（每栋多个宿管员）
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:44:   - 当前系统 `ClassMapping` 按 `class_id` 路由，184/196班级跨多个楼栋
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:45:   - **不应将楼栋宿管员强行塞入单一班级字段**
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:67:- Codex提供的5,559行自动匹配覆盖率95.35%，远高于我预期的人工工作量
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:84:- 宿管员按实际楼栋路由（同本科生）
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:124:- 输出3: `file2_unmatched_116.csv` (File2独有学生)
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:134:2. **宿管员路由规则确认** (P0)
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:135:   - [ ] 确认每栋多宿管员的选择规则（主责/轮值/任选）
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:144:**前置门禁（Codex建议）：**
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:148:- ✓ 每个楼栋能找到至少1个有效 dorm_manager
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:159:# Step 3: 导入辅导员和宿管员
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:170:- File2独有116名学生确认（住校 vs 非住校）
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:182:> ❌ "File1和File2无法通过共同字段关联"
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:190:- File1与File2**可以通过"姓名+规范化学院+班级/BH"关联**
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:191:- 自动匹配覆盖率：95.35% (5,559/5,830行)
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:192:- 准确率：接近100%（需抽样验证）
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:193:- 缺口：271名研究生（File1班级为空，File2无研究生数据）
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:195:- 数据质量评级：B-（本科数据高质量，研究生/宿管选主规则待补）
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:213:- Phase 2的3个业务确认（辅导员粒度、宿管员规则、研究生范围）
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:223:**A:** 是，完全同意。我遗漏了File2的FY字段，导致错误结论"无法关联"。
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:232:**A:** 建议调整。当前 `class_id -> dorm_manager` 与楼栋一对多、班级跨楼栋的现实不匹配。推荐改为：
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:235:- 或在申请创建时动态按学生楼栋路由宿管员
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:243:- 数据分析严谨：逐行统计、分层匹配策略、覆盖率/准确率量化评估 ✓
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:244:- 风险识别准确：学院别名、研究生误匹配、楼栋一对多、业务降级 ✓
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:245:- 方案建议实用：增强版策略平衡了自动化覆盖率与实施成本 ✓
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:246:- 门禁条件明确：Phase 3前置检查清单可直接用于UAT ✓
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:249:- 纠正了我的技术盲区（File2字段遗漏）
.omc/collaboration/artifacts/20260605-0910-claude-response-to-codex-excel-review.md:251:- 量化评估（5,559行覆盖、271行缺口）使决策更清晰
.omc/collaboration/artifacts/20260530-1718-claude-blocking-issues-response.md:554:2. 验证套件是否覆盖所有关键路径？
./docs/api/notification-contract-v0.1.md:356:- 单元测试覆盖率>80%
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:24:**Problem:** User.user_id required but 271 grad + File2 unmatched lack student numbers.
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:27:- Priority 1: Real XH from File2
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:29:- Priority 3: `TMP2026_{row:04d}` for File2 unmatched
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:35:- `student_no` (optional): Real XH from File2
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:74:**Validation gate:** `validate_routing_coverage.py` enforces 100% coverage before Phase 2.
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:83:- File1/File2 count discrepancy (155 vs 271+116) needs reconciliation
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:85:- File2-only 116 rows: User to decide import vs archive
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:99:- Both required for 100% routing coverage
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:128:   - `generate_tmp_user_id()`: Sequential for File2 unmatched
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:132:   - `merge_files()`: File1+File2 → File5 with source tracking
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:138:   - `validate_routing()`: 100% coverage gate check
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:140:   - Exit: 0 if 100%, 1 with detailed failure report
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:147:**Commit:** a142ad8 "feat: Phase 0数据门禁脚本实现" (+547 lines)
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:159:- File2: 2026届预计毕业生5675人.xlsx
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:169:**Step 1: Merge File1 + File2**
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:192:- Exit code 0 (100% coverage)
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:233:**Q3: File2-Only 116 Rows**
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:234:What to do with 116 students in File2 but not File1?
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:268:3. **Routing gaps:** 100% coverage gate blocks implementation until resolved
.omc/collaboration/artifacts/20260605-consensus-implementation-plan.md:283:**Next milestone:** Phase 0 execution passes 100% coverage gate
.omc/collaboration/artifacts/20260531-0202-claude-codex-week3-response.md:79:**Codex says:** "真正缺的是测试覆盖...所以 P0 是'补测试证明状态机'，不是'大改状态机'"
.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:88:### P1-2：state 预验证顺序仍不能覆盖 append 后失败
.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:129:5. `state.json` 预验证：覆盖了原始问题的一半，仍需处理 temp state 写入顺序、命名和 append 后失败窗口。
.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:132:## 验证覆盖度要求
.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:134:Claude 的 14 项验证清单需要补充以下测试，否则不能覆盖本轮新风险：
.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:143:8. `release_lock()` 覆盖 matching agent、mismatched agent、missing owner.json、malformed owner.json。
.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:159:**不批准直接实施。** 需要 Claude 至少修正 P0-1 到 P0-4，并扩展验证清单覆盖 wrapper/CLI/claim/release 四条路径后，才能进入 Phase 1a/1b 实施。
.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:508:- release_lock()覆盖：matching agent、mismatched agent、missing owner.json、malformed owner.json
.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:525:3. 验证覆盖度扩展
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:1:# XG API数据覆盖度分析 - Claude-Codex共识文档
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:20:- 基础字段质量优秀（number/name/status 100%完整）
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:35:## 二、字段覆盖度对比分析
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:39:| 维度 | 覆盖度 | 评分 |
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:41:| 完全覆盖字段 | 3/11 (27%) | name/number/department |
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:42:| 部分覆盖字段 | 1/11 (9%) | phone (80%完整) |
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:43:| 无覆盖字段 | 7/11 (64%) | 包括3个CRITICAL字段 |
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:48:| 业务域 | 覆盖情况 | 影响等级 |
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:50:| 身份识别 | ✓ 可用 | number/name 100% |
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:52:| 审批路由分配 | ✗ 不可用 | 缺class_id+映射关系 |
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:59:- 基础字段覆盖良好（身份识别可用）
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:61:- 数据质量优秀但覆盖度不足
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:74:**Codex评估：** P0 - 审批路由无法落地
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:134:### 4.3 字段覆盖文档状态过期（P1）
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:162:| 业务覆盖质量 | 低 | 缺核心字段阻断替代 |
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:168:- 但业务字段覆盖度严重不足
.omc/collaboration/artifacts/20260603-1610-consensus-xg-data-coverage.md:186:- ✗ XG API覆盖class_id/is_graduating/graduation_year
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:11:**用户要求：** "第一审批人学校要求是宿管员，第二审批人是辅导员"
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:22:学生提交申请 → 宿管员审批 → 辅导员审批 → 完成
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:45:    PENDING_DORM_MANAGER = 'pending_dorm_manager', '待宿管员审批'
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:61:    DORM_MANAGER = 'dorm_manager', '宿管员'
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:73:- 申请提交后创建宿管员审批记录（不是辅导员）
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:74:- 宿管员审批通过后创建辅导员审批记录（不是院长）
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:99:- "待辅导员审批" → "待宿管员审批"
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:117:3. 更新申请提交逻辑（创建宿管员审批）
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:118:4. 更新审批通过逻辑（宿管员→辅导员，辅导员→完成）
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:163:**风险：** 需要确保宿管员角色在系统中存在且配置正确
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:168:- 创建测试数据时包含宿管员角色
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:175:- [ ] 申请提交后创建宿管员审批记录
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:176:- [ ] 宿管员审批通过后创建辅导员审批记录
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:187:1. ✅ 两级审批足够（宿管员→辅导员）
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:189:3. ⚠️ 宿管员角色需要在系统中添加/确认
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:192:- 审批流程：学生提交 → 宿管员审批 → 辅导员审批 → **完成**
.omc/collaboration/artifacts/20260601-0135-claude-response-phase4a-blocker-challenge.md:57:- 角色路由（简单if判断）
.omc/collaboration/artifacts/20260601-0135-claude-response-phase4a-blocker-challenge.md:115:2. 角色路由
.omc/collaboration/artifacts/20260601-0135-claude-response-phase4a-blocker-challenge.md:136:- 验证新增学生流（student-application + 角色路由）
.omc/collaboration/artifacts/20260601-0135-claude-response-phase4a-blocker-challenge.md:178:3. ✅ 实现窄Phase 4B（学生页+路由+API集中化）
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:1:# XG API数据覆盖度分析报告
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:20:| 基础字段覆盖 | ✓ 良好 | name, number, phone, department可获取 |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:29:## 二、字段覆盖度矩阵
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:31:### 2.1 学生基本信息字段覆盖
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:33:| 需求字段 | 必填性 | XG API提供 | 覆盖状态 | 数据质量 | 影响等级 |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:35:| student_id（学号） | ✓ 必填 | ✓ number | ✅ 完全覆盖 | 100%完整 | - |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:36:| name（姓名） | ✓ 必填 | ✓ name | ✅ 完全覆盖 | 100%完整 | - |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:37:| department（院系） | ✓ 必填 | ✓ department[0].name | ✅ 完全覆盖 | 100%完整 | - |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:38:| phone（手机号） | 可选 | ✓ phone | ⚠️ 部分覆盖 | 80%完整 | LOW |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:39:| **class_id（班级ID）** | **✓ 必填** | **✗ 缺失** | **❌ 无覆盖** | **N/A** | **🔴 CRITICAL** |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:40:| **is_graduating（是否毕业生）** | **✓ 必填** | **✗ 缺失** | **❌ 无覆盖** | **N/A** | **🔴 CRITICAL** |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:41:| **graduation_year（毕业年份）** | **✓ 必填** | **✗ 缺失** | **❌ 无覆盖** | **N/A** | **🔴 CRITICAL** |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:42:| major（专业） | ✓ 必填 | ✗ 缺失 | ❌ 无覆盖 | N/A | 🟡 MAJOR |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:43:| grade（年级） | ✓ 必填 | ✗ 缺失 | ❌ 无覆盖 | N/A | 🟡 MAJOR |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:44:| class_name（班级名称） | 可选 | ✗ 缺失 | ❌ 无覆盖 | N/A | 🟢 MINOR |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:45:| email（邮箱） | 可选 | ✗ 缺失 | ❌ 无覆盖 | N/A | 🟢 MINOR |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:47:**覆盖度统计：**
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:48:- 完全覆盖：3/11 (27%)
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:49:- 部分覆盖：1/11 (9%)
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:50:- 无覆盖：7/11 (64%)
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:53:### 2.2 辅导员基本信息字段覆盖
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:55:| 需求字段 | 必填性 | XG API提供 | 覆盖状态 | 影响等级 |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:57:| employee_id（工号） | ✓ 必填 | ✓ number | ✅ 完全覆盖 | - |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:58:| name（姓名） | ✓ 必填 | ✓ name | ✅ 完全覆盖 | - |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:59:| department（院系） | ✓ 必填 | ✓ department | ✅ 完全覆盖 | - |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:60:| phone（手机号） | 可选 | ✓ phone | ⚠️ 部分覆盖 | 🟢 MINOR |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:61:| email（邮箱） | 可选 | ✗ 缺失 | ❌ 无覆盖 | 🟢 MINOR |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:62:| is_active（是否在职） | ✓ 必填 | ✓ status | ✅ 完全覆盖 | - |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:64:**辅导员字段覆盖度：** 4/6 (67%) - 基本满足需求
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:66:### 2.3 班级-辅导员对应关系覆盖
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:68:| 需求字段 | 必填性 | XG API提供 | 覆盖状态 | 影响等级 |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:70:| **class_id（班级ID）** | **✓ 必填** | **✗ 缺失** | **❌ 无覆盖** | **🔴 CRITICAL** |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:71:| class_name（班级名称） | 可选 | ✗ 缺失 | ❌ 无覆盖 | 🟢 MINOR |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:72:| counselor_employee_id | ✓ 必填 | ✗ 缺失 | ❌ 无覆盖 | 🔴 CRITICAL |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:74:**班级映射覆盖度：** 0/3 (0%) - ❌ 无法通过API建立映射关系
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:99:- ✓ API同步时不覆盖class_id字段（已实施）
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:149:| number | 20/20 | 0 | 100% | ✓ 优秀 |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:150:| name | 20/20 | 0 | 100% | ✓ 优秀 |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:152:| status | 20/20 | 0 | 100% | ✓ 优秀 |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:153:| department | 20/20 | 0 | 100% | ✓ 优秀 |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:154:| user_identity | 20/20 | 0 | 100% | ✓ 优秀 |
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:158:- department数组：20/20存在 (100% - ✓ 优秀)
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:159:- user_identity对象：20/20存在 (100% - ✓ 优秀)
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:240:**风险：** 学生手机号变更后，CSV未及时更新，API同步覆盖旧值
.omc/collaboration/artifacts/20260603-1502-claude-xg-data-gap-analysis.md:297:   - [ ] 定期检查class_id映射覆盖率
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:20:**Codex finding:** User.user_id is primary key, but 271 grad students + File2 unmatched lack student numbers. Contradicts "all 5830 rows can import."
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:22:**Root cause analysis:** Agreed. Current User model requires non-null user_id (backend/apps/users/models.py:12-17), but merge strategy allows empty student_no from File2.
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:29:# Priority 1: Real student number from File2
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:38:# Priority 3: File2 unmatched undergrad → sequential
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:81:Created `backend/scripts/validate_routing_coverage.py` to enforce 100% coverage gate:
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:88:    # Exit 0 if 100%, exit 1 otherwise
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:116:**Acknowledged:** File1/File2 count discrepancy (155 vs 271+116) needs reconciliation in merge report. Status machine naming (`PENDING` vs `pending_dorm_manager`) should align with existing codebase conventions.
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:120:- Merge report will clarify File2-only 116 rows disposition
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:153:- Function: `generate_tmp_user_id()` - Sequential temp IDs for File2 unmatched
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:157:- Function: `merge_files()` - File1 (base) + File2 (supplemental) → File5
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:163:- Function: `validate_routing()` - 100% coverage gate check
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:165:- Exit: Code 0 if 100% coverage, 1 otherwise
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:178:**Commit:** a142ad8 "feat: Phase 0数据门禁脚本实现"
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:229:- 100% routing coverage (exit code 0)
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:237:2. Phase 0 validation passes 100%
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:255:**Q3:** File2-only 116 rows - Import as additional students or archive only?
docs/XG-API与项目数据表对比分析.md:303:- 必须覆盖所有学生的class_id
./backend/data/routing_coverage_report.json:168:      "user_id": "2022130440116",
./backend/data/routing_coverage_report.json:348:      "user_id": "2022130340116",
./backend/data/routing_coverage_report.json:438:      "user_id": "2022320140116",
./backend/data/routing_coverage_report.json:911:      "user_id": "2022130440116",
./backend/data/routing_coverage_report.json:1271:      "user_id": "2022130340116",
./backend/data/routing_coverage_report.json:1451:      "user_id": "2022320140116",
./backend/data/routing_coverage_report.json:1751:  "dorm_manager_coverage_pct": 98.04910864446687,
./backend/data/routing_coverage_report.json:1753:  "fully_routable_pct": 98.04910864446687
docs/COMPLETION-STATUS.md:16:| 后端/API/数据库/Docker/Smoke演示环境 | 98-100% | 已完成 |
docs/COMPLETION-STATUS.md:34:### ✓ 已完成 (100%)
docs/COMPLETION-STATUS.md:37:- **测试覆盖：** 172/172 单元测试通过
docs/COMPLETION-STATUS.md:146:- ✓ 完整的后端API系统（172测试覆盖）
docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decision.md:46:1. 学生提交 → 宿管员审批 → 辅导员审批 → 状态变为已通过
docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decision.md:83:4. 宿管员/辅导员登录 → 列表页标题显示"审批列表"
docs/用户设计说明书.md:298:1. 宿管系统导出Excel文件（我们提供模板）
docs/用户设计说明书.md:412:**Q1：数据导入会不会覆盖原有数据？**
./docs/ui-design-proposals/01-analysis-and-responsive-plan.md:82:   - 移动端：`width: 100%; max-width: 100%;`
docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:58:   - 对宿管员/辅导员审批列表有意义，但对学工部“只看 approved”场景会产生冗余 UI。
docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:70:- 宿管员：第一审批
docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:80:2. 宿管员审批通过。
docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:109:   - 宿管员/辅导员：`审批列表`
docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:113:   - 宿管员/辅导员：`暂无待审批申请`
docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:117:   - 宿管员/辅导员且当前审批人匹配：显示同意/驳回按钮
docs/discussions/ui-design-2026-06-02/07-claude-response-to-gemini-ui-proposal.md:14:- 配色提取完整（主色、辅助色、背景、文本、状态色全覆盖）
docs/discussions/ui-design-2026-06-02/07-claude-response-to-gemini-ui-proposal.md:90:✅ 移动端width 100%：保持当前实现
.omc/collaboration/artifacts/test-coverage-analysis.md:1:# 后端测试覆盖分析
.omc/collaboration/artifacts/test-coverage-analysis.md:4:**目的：** 分析现有测试覆盖，识别gap，补充关键测试
.omc/collaboration/artifacts/test-coverage-analysis.md:19:   - 覆盖：基本申请流程
.omc/collaboration/artifacts/test-coverage-analysis.md:23:   - 覆盖：约束条件
.omc/collaboration/artifacts/test-coverage-analysis.md:27:   - 覆盖：错误场景
.omc/collaboration/artifacts/test-coverage-analysis.md:31:   - 覆盖：列表权限
.omc/collaboration/artifacts/test-coverage-analysis.md:35:   - 覆盖：P0修复（重新提交 + 审批过滤）
.omc/collaboration/artifacts/test-coverage-analysis.md:39:   - 覆盖：序列化器验证
.omc/collaboration/artifacts/test-coverage-analysis.md:45:   - 覆盖：审批列表权限
.omc/collaboration/artifacts/test-coverage-analysis.md:49:   - 覆盖：审批权限
.omc/collaboration/artifacts/test-coverage-analysis.md:53:   - 覆盖：驳回流程
.omc/collaboration/artifacts/test-coverage-analysis.md:57:    - 覆盖：状态机
./docs/acceptance/phase4c-known-issues.md:20:| 角色路由跳转 | 未验证 | 无法确认role-guard实际生效 | 模拟器/真机测试登录流程 |
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:158:- 覆盖率目标：核心90%、整体70%
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:250:- 分层覆盖率目标
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:277:| 测试覆盖率不足 | 低 | 渐进式TDD，分层目标 |
docs/discussions/ui-design-2026-06-02/10-final-consensus-dean-filing-ui.md:28:| 元素 | 宿管员/辅导员 | 学工部 |
docs/discussions/ui-design-2026-06-02/10-final-consensus-dean-filing-ui.md:69:4. 宿管员/辅导员列表页标题显示"审批列表"
docs/discussions/ui-design-2026-06-02/10-final-consensus-dean-filing-ui.md:70:5. 宿管员/辅导员详情页根据当前审批人显示按钮
./docs/acceptance/phase4c-evidence-index.md:65:**覆盖场景：**
docs/discussions/ui-design-2026-06-02/04-complete-ui-coverage-analysis.md:1:# 完整UI功能覆盖分析
docs/discussions/ui-design-2026-06-02/04-complete-ui-coverage-analysis.md:5:**目的：** 基于系统完整功能，识别UI覆盖缺口，提出完整页面清单
docs/discussions/ui-design-2026-06-02/04-complete-ui-coverage-analysis.md:88:## 4. UI覆盖缺口分析
docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:38:### 5. URL路由
docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:79:### Step 3: 重构/api/applications/路由 (60min)
docs/discussions/ui-design-2026-06-02/05-ui-enhancement-color-responsive.md:149:| 容器宽度 | 100% | max-width: 1200px, 居中 |
docs/discussions/ui-design-2026-06-02/05-ui-enhancement-color-responsive.md:254:- 移动端优先 (`max-width: 100%`, 单列布局)。
./docs/acceptance/phase4c-acceptance-checklist.md:83:### 2.3 测试覆盖 ✅
./docs/acceptance/phase4c-acceptance-checklist.md:134:### 4.1 测试覆盖 ✅
./docs/acceptance/phase4c-acceptance-checklist.md:152:### 4.2 错误场景覆盖 ✅
./docs/acceptance/phase4c-acceptance-checklist.md:191:| 登录路由矩阵 | ✅ 通过 | student→student-application, counselor/dean→approvals |
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:102:3. 添加 URL 路由
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:108:3. 添加 URL 路由
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:142:### R2: 测试覆盖不足
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:20:**Codex指出：** 文档写 `password123/counselor/dean/dorm_manager`，实际学生密码=学号，辅导员=`T001/T002`，学工部=`D001`，宿管员账号未创建
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:36:| 宿管员 | （暂未实现） | - | 第一级审批 |
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:38:**注意：** 当前版本宿管员账号和映射尚未在种子数据中实现。
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:84:### P0-3: 小程序宿管员角色守卫冲突
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:86:**Codex指出：** 文档说宿管员登录后进入审批列表，但 approvals.ts:19 只允许 `['counselor', 'dean']`
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:90:- 文档 docs/操作说明书.md:162 描述宿管员登录后自动进入"审批列表"页面
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:99:⚠️ **注意：** 当前版本小程序审批页面仅支持辅导员和学工部角色访问，宿管员功能暂未实现。
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:102:1. 输入账号：（宿管员账号暂未配置）
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:103:2. Demo Web支持宿管员审批流程
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:257:1. 修复测试账号表格（明确标注宿管员未实现）
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:259:3. 宿管员小程序限制说明（采用选项A标注）
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:14:- **用户洞察正确**：File1与File2可通过"姓名+学院"关联（Claude初始分析错误）
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:15:- **Codex增强方案**：升级为"姓名+规范化学院+班级/BH"，覆盖95.35%数据
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:18:- **前置条件**：3个业务确认（辅导员粒度、宿管员规则、研究生范围）
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:30:- File5（学生） ← File1 + File2（姓名+学院关联）
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:31:- File5楼栋 → File3楼栋号 → 宿管员
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:39:- ❌ "File1和File2无法关联"（遗漏了File2的FY字段）
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:44:Claude未发现File2的FY/XSH字段包含学院信息，只检查了YXMC（校名），导致错误判断"两文件无共同字段"。
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:49:- ✓ 用户方向正确，File1/File2确实可关联
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:51:- ✓ 升级后覆盖5,559/5,830行（95.35%），准确率接近100%
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:52:- ⚠️ 剩余271行研究生无法自动匹配（File1班级为空，File2无研究生）
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:53:- ⚠️ 楼栋→宿管员一对多，不应塞入单一班级字段
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:66:- 调整ClassMapping模型：分离楼栋路由与班级路由
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:85:| File1学院名称 | 规范化后 | File2/File4对应 |
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:95:- File2独有：116行（需确认是否住校）
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:97:### 2.2 审批路由策略
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:99:**辅导员路由（学院级）：**
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:107:**宿管员路由（楼栋级）：**
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:109:student.building -> File3楼栋号 -> List[宿管员] -> 选主规则
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:111:- 覆盖33/33楼栋
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:112:- **问题**：每栋多个宿管员（一对多）
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:116:  3. 或在申请时动态路由（不预存class_id映射）
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:118:**研究生路由（特殊处理）：**
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:127:| 数据表 | 覆盖率 | 准确率 | 质量等级 | 说明 |
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:129:| 学生表（本科） | 95.35% | ~100% | A | 需抽样验证 |
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:131:| 辅导员映射 | 100% | ⚠️ | B | 学院级≠班级级 |
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:132:| 宿管员映射 | 100% | ⚠️ | B | 一对多+跨楼栋问题 |
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:133:| **综合评级** | **95.35%** | **~100%** | **B-** | 本科可用，研究生待补 |
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:155:- `file2_unmatched_116.csv` - File2独有学生待确认
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:165:2. **宿管员路由规则** (P0)
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:166:   - [ ] 确认：每栋多宿管员的选择规则（主责/轮值/任选其一）
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:175:**前置门禁（必须全部通过）：**
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:186:# 4. 验证每个楼栋有宿管员
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:203:# Step 3: 辅导员和宿管员用户导入
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:207:# Step 4: 路由验证
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:214:- File2独有116名学生确认（住校vs非住校）
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:244:### 风险3: 宿管员路由与模型不匹配
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:247:**影响：** 当前ClassMapping按class_id，但184/196班级跨多个楼栋
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:250:- 方案A：改模型，分离楼栋路由（BuildingMapping）
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:251:- 方案B：申请时动态按学生楼栋路由，不预存映射
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:252:- 方案C：业务确认班级只对应主楼栋的主宿管员（降级）
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:260:| 方案 | 覆盖率 | 准确率 | 实施时间 | 数据质量 | 总分 | 排名 |
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:262:| **用户策略增强版** | 95.35% | ~100% | 2-3天 | B- | **90** | 🥇 |
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:263:| 方案C（重新获取） | 100%? | 高 | 1-2周 | A? | 85 | 🥈 |
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:264:| 方案A（纯人工补充） | 100% | 中 | 3-4天 | C | 70 | 🥉 |
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:268:- 用户策略增强版在覆盖率、准确率、实施时间三方面最优
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:296:- ⏳ `file2_unmatched_116.csv`
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:329:- 遗漏了File2的FY字段（学院信息）
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:334:- 逐行统计分析，量化覆盖率/准确率
.omc/collaboration/artifacts/20260605-0920-consensus-excel-association-strategy.md:340:- 提出完整关联思路（File1→File2→File3/File4）
./backend/data/merge_report.json:5:  "file2_only_count": 116,
./docs/project-completion-status-2026-06-02.md:12:- 3步审批流程实现：宿管员 → 辅导员 → 学工部
./docs/project-completion-status-2026-06-02.md:72:**收益**: 完整测试覆盖，CI/CD可用
./docs/project-completion-status-2026-06-02.md:90:| 环境部署 | 100% | Docker + PostgreSQL 完整配置 |
./docs/project-completion-status-2026-06-02.md:91:| 数据库模型 | 100% | 所有表结构及迁移完成 |
./docs/project-completion-status-2026-06-02.md:92:| 核心API | 100% | 应用提交、审批、查询全部实现 |
./docs/project-completion-status-2026-06-02.md:93:| 审批流程 | 100% | 3步工作流完整实现 |
./docs/project-completion-status-2026-06-02.md:94:| XG集成 | 100% | 用户同步服务完成 (plan + apply) |
./docs/project-completion-status-2026-06-02.md:95:| 管理命令 | 100% | CLI入口实现 |
./docs/project-completion-status-2026-06-02.md:106:继续修复剩余17个测试问题，实现100%测试通过率
./docs/project-completion-status-2026-06-02.md:111:3. 86% → 100%的最后一公里
./docs/project-completion-status-2026-06-02.md:112:4. 完整测试覆盖保证后续开发质量
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:10:当前方案的业务方向基本正确：用 File1 作为学生基准、改为“楼栋宿管员 -> 学院辅导员”的 2 级审批、把学工管理员定位为只读角色，整体符合用户最新决策。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:12:但文档不能按“所有 P0 已解除，可开始实施”执行。至少 3 个阻塞点仍未闭合：空学号/空 `user_id` 无法导入、楼栋多宿管员与当前单审批人模型冲突、`ClassMapping`/`dean`/`class_id` 的代码契约改造范围被明显低估。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:31:   - 影响范围：File2 未匹配学生、研究生、登录账号、审批记录外键、通知和导入脚本。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:34:2. “任一宿管员可审批”与当前审批模型不兼容
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:36:   - 证据：当前 `Approval.approver` 是单个用户外键；创建申请时只创建一个宿管审批记录。见 `backend/apps/approvals/models.py:14-22`, `backend/apps/applications/views.py:172-179`。方案中的 `return dorm_managers` 没有定义如何落到审批记录、权限过滤、重复审批和通知。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:38:   - 建议修正：MVP 不要实现“任一人可审批”的组任务，除非增加 group approval 模型。更现实的 P0 修正是要求 File3 或映射表生成一个 `primary_dorm_manager_user_id`，每栋楼唯一主责宿管员；其他宿管员作为后续代理/备份扩展。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:42:   - 证据：现有提交申请直接查 `ClassMapping` 并用它创建宿管审批，见 `backend/apps/applications/views.py:147-179`；宿管审批通过后仍用 `ClassMapping` 创建辅导员审批，见 `backend/apps/approvals/views.py:149-174`；详情权限也按 `ClassMapping` 判断，见 `backend/apps/applications/permissions.py:11-23`。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:44:   - 建议修正：把 Phase 2 拆成明确的改造清单：数据模型、提交路由、审批通过路由、列表过滤、详情权限、附件权限、导入命令、API schema、前端/miniprogram 类型、测试 fixture。未完成前不能导入真实数据并开放提交。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:50:   - 问题：文档同时写“File2 没有的 155 行”和“271 研究生 + 116 File2 独有”。这两个口径不能同时成立。按 5830 和 5675 的净差是 155，但若存在 271 个 File1 独有和 116 个 File2 独有，交集应为 5559。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:51:   - 建议修正：File5 生成报告必须输出 `file1_only_count`、`file2_only_count`、`matched_count`、`ambiguous_match_count`、`duplicate_key_count`，并把 File2 独有 116 行明确列为“不导入但归档报告”或“追加导入”。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:63:4. 路由键没有做申请时快照，后续人员/学院/楼栋变更会破坏审计
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:65:   - 问题：如果只从 `User.department/building_name` 动态读取，学生学院或宿管映射更新后，历史申请的可见范围和审批追溯会变化。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:68:5. 学院/楼栋规范化缺少完整字典和阻断标准
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:70:   - 问题：只给示例，没有说明 19 个学院、33 个楼栋的完整映射来源、冲突处理和失败阈值。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:71:   - 建议修正：将 `college_normalization_map.json` 和 `building_normalization_map.json` 列为 Phase 1 必交付；导入门禁应是 100% 路由覆盖，任何未匹配、重复唯一键、空路由键都阻断。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:80:   - 问题：现有后端、前端、miniprogram、测试和 API 契约都依赖原 3 级/班级模型。1-1.5 天系统调整加 0.5 天前端不足以覆盖迁移、测试修复和回归。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:85:   - 问题：风险章节只有缓解，没有数据库迁移失败、导入失败、上线后路由错误的回滚路径。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:91:2. 测试用例应增加负向权限：宿管员不能看其他楼栋、辅导员不能看其他学院、管理员不能审批、学生不能访问审批列表。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:98:1. 先把文档状态从“所有 P0 阻塞已解除”改为“业务方向确认，实施前仍需关闭 P0 技术/数据门禁”。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:99:2. 增加 Phase 0：数据画像和路由门禁。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:100:   - 输出 File1/File2 匹配报告。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:101:   - 输出完整学院/楼栋规范化字典。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:103:   - 输出每名学生的宿管和辅导员路由结果。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:104:3. 把楼栋多宿管员规则收敛为一个 MVP 决策。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:105:   - 推荐：每栋楼唯一主责宿管员。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:108:   - `User` 增加学生楼栋、寝室、专业、年级字段。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:109:   - `Application.class_id` 改可空或废弃展示依赖，并新增申请时路由快照字段。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:112:   - Phase 0 数据门禁。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:113:   - Phase 1 后端模型和路由，带单元测试。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:124:2. 每个学生都能唯一确定一个宿管审批主体，或系统模型已支持多人待办。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:128:6. 导入脚本支持 dry-run，并输出 100% 路由覆盖报告。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:11:**重要说明：本项目只对接宿管系统，不直接对接教务、人事、学工等其他系统。**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:16:- **唯一数据源：** 宿管系统
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:17:- **数据获取方式：** 通过宿管系统提供的数据库、API或CSV文件
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:18:- **数据责任方：** 宿管系统负责人
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:20:### 1.2 为什么只对接宿管系统
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:22:1. **项目定位：** 本系统是宿管系统的配套子系统，不是全校级统一离校平台
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:23:2. **数据归集：** 宿管系统已从教务、人事、学工等系统归集了所需数据
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:25:4. **权责清晰：** 数据质量、更新时效由宿管系统统一负责
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:31:- ❌ **不接受：** 将反馈对象从"宿管系统"改为"多方数据负责人"
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:32:- 🔄 **调整：** 待反馈问题需明确"宿管系统能否提供这些数据"
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:40:**Codex意见：** 将"提交给宿管系统方"改为"提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人"。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:46:基于项目约束（只对接宿管系统），原文档的反馈对象是正确的：
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:47:1. 本系统只对接宿管系统，不直接对接教务、人事、学工
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:48:2. 学生、辅导员、班级映射等数据由宿管系统负责提供
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:49:3. 宿管系统如何获取这些数据（是否从教务/人事归集）是宿管系统的内部实现
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:50:4. 我们的职责是明确需求，由宿管系统确认能否提供
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:54:需要在待反馈问题中明确询问宿管系统：
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:55:- 这些数据是否在宿管系统数据库中？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:56:- 如果不在，宿管系统能否从其他系统归集后提供？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:60:- 保持反馈对象为"宿管系统方"
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:61:- 在待反馈问题中增加："宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？如不包含，能否从教务/人事/学工系统归集后提供？"
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:256:**修改方案：** 在文档中明确说明首版只支持一班一主辅导员，并在待反馈问题中询问宿管系统是否存在多辅导员场景。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:264:**Codex结论：** P0数据源覆盖完整，未遗漏关键数据。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:286:| `phone` 可选性确认 | ✅ 接受，需要在待反馈问题中询问宿管系统 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:298:3. CSV需补充导入覆盖策略、重复数据处理、失败回滚
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:330:- 导入策略：首版采用**全量覆盖**（清空后重新导入）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:360:- 宿管系统能否只提供当届毕业生数据？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:369:基于项目约束（只对接宿管系统），我们接受Codex建议的问题方向，但需要调整提问对象和表述。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:373:将Codex建议的12个问题调整为"向宿管系统确认的问题清单"：
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:376:1. 宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:392:11. CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:422:1. 向宿管系统提交本需求文档
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:431:4. 重点校验：学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:434:1. 对接宿管系统宿舍清退API
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:467:1. 将反馈对象从"宿管系统"改为"多方数据负责人"
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:468:   - 理由：项目只对接宿管系统，不直接对接教务/人事/学工
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:472:2. 待反馈问题：接受问题方向，但调整为"向宿管系统确认"
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:530:3. 提交给宿管系统方反馈
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:531:4. 根据宿管系统反馈调整方案
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:540:1. **项目约束确认：** 我们明确项目只对接宿管系统，不直接对接教务/人事/学工。Codex是否认同这个约束下，原文档的反馈对象（宿管系统方）是正确的？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:556:- **核心约束：** 项目只对接宿管系统
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:558:- **保持立场：** 反馈对象为宿管系统方
.omc/collaboration/artifacts/20260605-user-business-decisions.md:19:- 升级路径：Phase 1楼栋级路由 → Phase 2寝室级精确一对一路由
.omc/collaboration/artifacts/20260605-user-business-decisions.md:23:### 决策2：楼栋名称匹配规则
.omc/collaboration/artifacts/20260605-user-business-decisions.md:25:**问题：** File1与File3楼栋名称是否需要规范化？如何匹配？
.omc/collaboration/artifacts/20260605-user-business-decisions.md:28:> "按楼栋名称吻合的匹配"
.omc/collaboration/artifacts/20260605-user-business-decisions.md:31:- 使用楼栋名称直接匹配（exact match或normalized match）
.omc/collaboration/artifacts/20260605-user-business-decisions.md:32:- 如File3楼栋名与File1不同，需创建building_normalization_map.json
.omc/collaboration/artifacts/20260605-user-business-decisions.md:33:- validate_routing_coverage.py将检测未匹配楼栋
.omc/collaboration/artifacts/20260605-user-business-decisions.md:36:- Phase 0.3：File3到达后分析楼栋名称
.omc/collaboration/artifacts/20260605-user-business-decisions.md:38:- 100%覆盖门禁确保所有学生可路由
.omc/collaboration/artifacts/20260605-user-business-decisions.md:42:### 决策3：File2独有116行处理
.omc/collaboration/artifacts/20260605-user-business-decisions.md:44:**问题：** File2中116个File1没有的学生如何处理？
.omc/collaboration/artifacts/20260605-user-business-decisions.md:50:- File2独有116行作为额外学生导入
.omc/collaboration/artifacts/20260605-user-business-decisions.md:51:- 总学生数：5830（File1）+ 116（File2 only）= 5946行
.omc/collaboration/artifacts/20260605-user-business-decisions.md:59:# 修改：输出File1 + File2独有行
.omc/collaboration/artifacts/20260605-user-business-decisions.md:63:# 2. File2匹配的：补充字段
.omc/collaboration/artifacts/20260605-user-business-decisions.md:64:# 3. File2独有的（116行）：作为新行追加
.omc/collaboration/artifacts/20260605-user-business-decisions.md:65:#    - user_id: 从File2的XH
.omc/collaboration/artifacts/20260605-user-business-decisions.md:72:- file2_only_count: 116
.omc/collaboration/artifacts/20260605-user-business-decisions.md:108:- 增加File2独有行处理逻辑
.omc/collaboration/artifacts/20260605-user-business-decisions.md:113:- 验证目标：5946行学生100%路由覆盖
.omc/collaboration/artifacts/20260605-user-business-decisions.md:116:- 实施方案：数据覆盖5830→5946
.omc/collaboration/artifacts/20260605-user-business-decisions.md:135:**下一步：** 修改merge脚本支持File2独有行，更新文档反映5946行total
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:126:- 测试覆盖率反而下降
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:142:#### MAJOR - 80%覆盖率目标缺少分层
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:145:测试覆盖率目标80%，但未区分不同类型代码：
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:146:- 业务逻辑代码应该100%覆盖
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:151:**分层覆盖率目标**：
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:245:2. **分层覆盖率目标**（核心90%、API 80%、模型70%）
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:258:3. 分层覆盖率目标
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:5:**目的：** 提交给宿管系统方，确认数据可用性和实施计划  
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:10:## 一、待宿管系统确认的问题清单
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:14:**问题1：** 宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:63:**问题11：** CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:117:1. 向宿管系统提交本确认清单
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:151:   - 班级映射覆盖率（所有学生的class_id都有对应辅导员）
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:168:1. 对接宿管系统宿舍清退API
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:176:   - 数据过期：提示学生联系宿管
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:281:| 宿管系统无法提供完整数据 | 高 | 提前确认数据可用性，必要时调整对接范围 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:293:**宿管系统联系人：** [待填写]  
./docs/API-DATA-EXAMPLES.md:56:  "approver_name": "宿管员1",
./docs/API-DATA-EXAMPLES.md:71:| approver_name | string | 审批人姓名 | 宿管员1 |
./docs/API-DATA-EXAMPLES.md:162:### 响应结构（辅导员/宿管员/学工部视角）
./docs/API-DATA-EXAMPLES.md:187:- `pending_dorm_manager`: 待宿管员审批
./docs/API-DATA-EXAMPLES.md:194:- `dorm_manager`: 宿管员审批
./docs/XG-API与项目数据表对比分析.md:303:- 必须覆盖所有学生的class_id
docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:11:5. ✅ **登录路由矩阵**（新问题3）
docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:38:**第2步：注册 + 路由 + smoke（15分钟）**
docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:41:login.ts         - 实现角色路由矩阵
docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:145:      DORM_BLOCKED: (d) => `宿舍清退未完成：${d?.blocking_reason || '请联系宿管'}`,
docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:154:**5. 登录路由矩阵**
docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:191:- ✅ 实现登录路由矩阵
./docs/COMPLETION-STATUS.md:16:| 后端/API/数据库/Docker/Smoke演示环境 | 98-100% | 已完成 |
./docs/COMPLETION-STATUS.md:34:### ✓ 已完成 (100%)
./docs/COMPLETION-STATUS.md:37:- **测试覆盖：** 172/172 单元测试通过
./docs/COMPLETION-STATUS.md:146:- ✓ 完整的后端API系统（172测试覆盖）
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:56:`docs/design/2026-05-27-system-design.md` 内容覆盖较全面：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:276:### 7.2 乐观锁覆盖面不够明确
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:481:单列索引如果被复合索引覆盖，应避免重复创建。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:487:测试策略方向正确：pytest、PostgreSQL、TDD、覆盖率 80%+、并发测试、文件安全测试、限流测试、审计测试。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:495:- 并发测试需要真实 PostgreSQL，SQLite 无法覆盖 `select_for_update`
./docs/用户设计说明书.md:298:1. 宿管系统导出Excel文件（我们提供模板）
./docs/用户设计说明书.md:412:**Q1：数据导入会不会覆盖原有数据？**
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:147:3. **可能未使用**：部分索引可能查询覆盖不到
./docs/外部系统数据接口确认清单.md:12:根据XG API数据覆盖度分析（2026-06-03），当前XG用户API缺失3个P0关键业务字段，导致无法独立支持毕业生离校申请审批系统。需向相关外部系统确认是否能提供缺失数据。
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:6:**目的：** 明确毕业离校系统所需的数据源，提交给宿管系统方反馈
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:14:1. **CSV导入策略**：从"全量覆盖"改为"staging表 + upsert + 软停用"
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:45:- **API优先**：调用宿管系统提供的API接口（实时校验场景）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:46:- **DB备选**：直接读取宿管系统数据库（需要安全审批和网络配置）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:510:## 五、待宿管系统确认的问题清单
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:514:1. 宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:533:11. CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:559:1. 向宿管系统提交本需求文档
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:571:7. 重点校验：学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:574:1. 对接宿管系统宿舍清退API
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:722:1. ✅ CSV导入策略从"全量覆盖"改为"staging + upsert + 软停用"
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:730:1. 提交本文档给宿管系统方反馈
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:731:2. 根据宿管系统反馈调整方案
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:11:1. ✅ 学生宿舍清退数据（来源：宿管系统）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:64:**数据来源：** 宿管系统
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:245:### 5.1 宿管员信息
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:249:- 宿管员不需要在本系统中登录
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:250:- 不需要宿管员数据
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:261:| 宿舍清退数据 | 宿管系统 | API/CSV | ✅ 已有 |
./docs/PROJECT-SUMMARY.md:73:- ✓ 批次5：第9-10章性能测试（索引、连接池、TDD、覆盖率）
./docs/PROJECT-SUMMARY.md:227:  - 移除GET /api/applications列表端点（统一为5个HTTP路由）
./docs/PROJECT-SUMMARY.md:232:  - P1-1：错误样例覆盖不完整（Section 3定义8个错误码，Section 6.2只有4个样例）
./docs/PROJECT-SUMMARY.md:234:  - P2-1：术语不一致（"5个HTTP路由" vs "4个API端点"）
./docs/PROJECT-SUMMARY.md:278:  - 覆盖completed、pending、not_started、unknown四种状态
./docs/PROJECT-SUMMARY.md:470:- ✓ 自动化测试：4个测试覆盖403/409场景
./docs/PROJECT-SUMMARY.md:642:5. **测试覆盖不足** - 采用TDD模式
./docs/PROJECT-SUMMARY.md:654:- ✓ 单元测试覆盖率 > 80%
./docs/PROJECT-SUMMARY.md:683:- ✓ 测试覆盖：resubmission + approval filter
./docs/PROJECT-SUMMARY.md:703:  - app.json（页面路由、窗口配置）
./docs/PROJECT-SUMMARY.md:767:- ✓ 新增审批负向权限覆盖：学生不可审批/驳回、角色步骤不匹配禁止、同角色非指定审批人禁止
./docs/PROJECT-SUMMARY.md:769:- ✓ 新增状态机覆盖：重复驳回冲突、counselor/dean步骤状态不匹配返回409
./docs/PROJECT-SUMMARY.md:798:- ✓ 无需新增代码，仅验证覆盖度
./docs/PROJECT-SUMMARY.md:844:2. ✓ MVP = 最小可行路径 + 必要错误处理（非全覆盖）
./docs/PROJECT-SUMMARY.md:943:1. 高优先级：实现student-application页面 + 基于角色的路由（修复已知gap）
./docs/PROJECT-SUMMARY.md:966:1. ✓ 实施顺序：结构化骨架优先（完整UI结构 + 页面骨架 + 注册 + 登录路由smoke + 提交逻辑）
./docs/PROJECT-SUMMARY.md:981:- ✓ 登录路由矩阵
./docs/PROJECT-SUMMARY.md:1004:- ✅ 登录路由矩阵实现完成
./docs/PROJECT-SUMMARY.md:1058:**后端测试覆盖增强（2026-06-01）：**
./docs/PROJECT-SUMMARY.md:1061:- ✓ Claude创建初步测试覆盖分析（识别3个高优先级gap）
./docs/PROJECT-SUMMARY.md:1070:3. ✓ State machine gaps: 已被现有测试覆盖（resubmission, terminal protection）
./docs/PROJECT-SUMMARY.md:1087:- ✓ 测试覆盖关键安全和边界场景
./docs/PROJECT-SUMMARY.md:1100:- ✅ 后端测试覆盖增强完成
./docs/PROJECT-SUMMARY.md:1135:- ✓ 后端测试（19个测试，100%通过）
./docs/PROJECT-SUMMARY.md:1155:- ✅ 19个测试100%通过
./docs/PROJECT-SUMMARY.md:1218:- 增加单元测试覆盖
./docs/PROJECT-SUMMARY.md:1310:- ✓ 字段校验覆盖所有必填字段和外键引用
./docs/PROJECT-SUMMARY.md:1366:- ✓ Smoke test覆盖附件上传/下载/删除
./docs/PROJECT-SUMMARY.md:1447:  1. Blocked by WeChat DevTools（6项：编译/运行/真机/上传/网络/路由）
./docs/PROJECT-SUMMARY.md:1602:- ✓ URL路由配置
./docs/PROJECT-SUMMARY.md:1636:- backend/apps/notifications/urls.py（URL路由）
./docs/PROJECT-SUMMARY.md:1786:- ✅ API路径级测试覆盖完成
./docs/PROJECT-SUMMARY.md:1862:4. **测试覆盖**
./docs/PROJECT-SUMMARY.md:1895:**Step 1.0: Smoke可重复运行门禁（已完成）：**
./docs/PROJECT-SUMMARY.md:1925:- ✓ 添加schema和Swagger UI路由
./docs/PROJECT-SUMMARY.md:1934:- backend/config/urls.py（添加schema路由）
./docs/PROJECT-SUMMARY.md:1946:- ✓ 补充DEPLOYMENT.md故障排查指南（覆盖8个真实场景）
./docs/PROJECT-SUMMARY.md:1956:- 故障排查指南: 覆盖409/422/401/403/media/Docker/数据库/schema场景 ✓
./docs/PROJECT-SUMMARY.md:1960:- ✅ Step 1.0: Smoke可重复运行门禁
./docs/PROJECT-SUMMARY.md:1991:- ✓ 对齐13个function-based views的路由和响应结构
./docs/PROJECT-SUMMARY.md:2135:  - Live probe硬门禁（XG_RUN_LIVE_API_TEST=1）
./docs/PROJECT-SUMMARY.md:2212:- ⏭ 下一步：讨论Step 2C字段覆盖 vs Step 3同步命令优先级
./docs/PROJECT-SUMMARY.md:2370:- 场景覆盖：skip透传/existing候选/missing不创建/role冲突/只读保证/字段gap warning/空输入/混合场景
./docs/PROJECT-SUMMARY.md:2393:- 106：Codex推荐选项组合2（扩展模型+不覆盖name）
./docs/PROJECT-SUMMARY.md:2401:- 不允许API覆盖name字段（避免CSV与API反复冲突）
./docs/PROJECT-SUMMARY.md:2462:- 未同步后端已完成的审批流程变更（宿管员→辅导员）
./docs/PROJECT-SUMMARY.md:2466:  - 审批列表页：当前用户角色"辅导员"→"宿管员"
./docs/PROJECT-SUMMARY.md:2467:  - 审批列表项：审批步骤"辅导员审批"→"宿管员审批"
./docs/PROJECT-SUMMARY.md:2469:  - 详情页时间轴：审批步骤"辅导员审批"→"宿管员审批"
./docs/PROJECT-SUMMARY.md:2483:  - roleMap新增：dorm_manager: '宿管员'
./docs/PROJECT-SUMMARY.md:2506:  - 角色选择器（宿管员/辅导员/学工部）
./docs/PROJECT-SUMMARY.md:2531:- ✓ 内容覆盖：系统概述、部署指南、用户操作、常见问题、测试账号、API端点、数据库表结构
./docs/PROJECT-SUMMARY.md:2538:- ✓ **测试账号错误**：文档写password123，实际学生密码=学号，辅导员=T001/T002，学工部=D001，宿管员未实现
./docs/PROJECT-SUMMARY.md:2540:- ✓ **小程序角色守卫冲突**：文档说宿管员可进审批列表，实际小程序只允许counselor/dean；添加警告说明
./docs/PROJECT-SUMMARY.md:2555:- docs/操作说明书.md:159-164 (宿管员登录警告)
./docs/PROJECT-SUMMARY.md:2570:### Claude-Codex协作分析XG API数据覆盖度
./docs/PROJECT-SUMMARY.md:2580:- **字段覆盖度：** 27% (3/11完全覆盖), 64% (7/11缺失)
./docs/PROJECT-SUMMARY.md:2581:- **必填字段覆盖：** 57% (4/7), 关键业务字段0% (0/3)
./docs/PROJECT-SUMMARY.md:2582:- **数据质量评分：** 95/100 (A级) - 提供的字段质量优秀但业务覆盖不足
./docs/PROJECT-SUMMARY.md:2601:  - 优点：业务完整性100%, 风险可控, 实施快速
./docs/PROJECT-SUMMARY.md:2632:- ✅ XG API数据覆盖度分析完成
./docs/PROJECT-SUMMARY.md:2691:- 列：校区,楼栋,寝室,学生姓名,性别,专业,学院名称,班级,层次,年级
./docs/PROJECT-SUMMARY.md:2701:- 列：序号,楼栋号,职工号,姓名,电话
./docs/PROJECT-SUMMARY.md:2714:- 影响：无法唯一标识学生或无法路由到正确院系
./docs/PROJECT-SUMMARY.md:2719:- 影响：审批路由失效，无法实现"辅导员只审批自己负责班级"
./docs/PROJECT-SUMMARY.md:2721:**缺陷3：部分宿管员无工号**
./docs/PROJECT-SUMMARY.md:2730:| 辅导员表 | 100% | ✅ 满足 | - |
./docs/PROJECT-SUMMARY.md:2731:| 宿管员表 | 75% | ⚠️ 基本满足 | 部分工号缺失 |
./docs/PROJECT-SUMMARY.md:2739:- 补充宿管员工号
./docs/PROJECT-SUMMARY.md:2771:   - 错误：认为File1与File2"无法关联"
./docs/PROJECT-SUMMARY.md:2772:   - 原因：遗漏了File2的FY字段（学院信息），只检查了YXMC（校名）
./docs/PROJECT-SUMMARY.md:2777:   - File2有：XH(学号)、FY(学院)、BH(班号)
./docs/PROJECT-SUMMARY.md:2784:   - 覆盖率：5,559/5,830行（95.35%），准确率~100%
./docs/PROJECT-SUMMARY.md:2785:   - 缺口：271行研究生（File1班级为空，File2无研究生数据）
./docs/PROJECT-SUMMARY.md:2788:4. **审批路由问题识别**
./docs/PROJECT-SUMMARY.md:2789:   - 楼栋→宿管员：覆盖完整但一对多，184/196班级跨多个楼栋
./docs/PROJECT-SUMMARY.md:2791:   - 需要3个业务确认（辅导员粒度、宿管员规则、研究生范围）
./docs/PROJECT-SUMMARY.md:2812:- 量化分析优于主观判断：Codex提供覆盖率/准确率/缺口清单
./docs/PROJECT-SUMMARY.md:2824:1. **数据合并策略** - File1为基准（5830行全保留），File2补充字段，缺失留空
./docs/PROJECT-SUMMARY.md:2825:2. **班级字段处理** - class_id暂时为空，不用于路由
./docs/PROJECT-SUMMARY.md:2826:3. **审批流程调整** - 2级审批（宿管员按楼栋→辅导员按学院），移除学工部审批
./docs/PROJECT-SUMMARY.md:2828:5. **寝室号未来补充** - File3后续补充寝室号，实现一对一精确路由
./docs/PROJECT-SUMMARY.md:2836:| ClassMapping缺失 | 决策3：改为楼栋+学院路由 | ✅ 已解除 |
./docs/PROJECT-SUMMARY.md:2837:| 楼栋一对多问题 | 决策3：楼栋级路由 | ✅ 已解除 |
./docs/PROJECT-SUMMARY.md:2844:| 审批流程 | 3级（宿管→辅导→学工部） | 2级（宿管→辅导） | 中等 |
./docs/PROJECT-SUMMARY.md:2845:| 路由方式 | ClassMapping(class_id) | Building+College | 重大 |
./docs/PROJECT-SUMMARY.md:2848:| 数据覆盖 | 5559行 | 5830行全部 | 扩大 |
./docs/PROJECT-SUMMARY.md:2851:- Phase 1: 数据准备（0.5天）- 合并File1+File2，规范化学院
./docs/PROJECT-SUMMARY.md:2852:- Phase 2: 系统调整（1-1.5天）- 审批流程、路由逻辑、权限控制
./docs/PROJECT-SUMMARY.md:2853:- Phase 3: 数据导入（0.5天）- 导入5830学生+辅导员+宿管员
./docs/PROJECT-SUMMARY.md:2870:1. **P0-1: 空学号无法导入** - User.user_id是必填主键，但271研究生+File2未匹配学生缺学号
./docs/PROJECT-SUMMARY.md:2871:2. **P0-2: 多宿管员冲突** - Approval.approver是单FK，无法支持"任一宿管员审批"
./docs/PROJECT-SUMMARY.md:2874:**Phase 0数据门禁脚本（已实现）：**
./docs/PROJECT-SUMMARY.md:2879:| merge_student_data.py | File1+File2合并，输出user_id/student_no/source | ✅ 完成 |
./docs/PROJECT-SUMMARY.md:2880:| validate_routing_coverage.py | 100%路由覆盖验证（楼栋→宿管，学院→辅导） | ✅ 完成 |
./docs/PROJECT-SUMMARY.md:2885:- 多宿管员MVP简化：每楼栋指定唯一primary manager
./docs/PROJECT-SUMMARY.md:2886:- 路由门禁：exit 0当100%覆盖，否则exit 1阻断实施
./docs/PROJECT-SUMMARY.md:2889:- Phase 0: 数据验证门禁（1-1.5天，新增）
./docs/PROJECT-SUMMARY.md:2902:**Commit:** a142ad8 "feat: Phase 0数据门禁脚本实现" (+547 lines)
./docs/PROJECT-SUMMARY.md:2912:- File3后续补充room_number实现一对一精确路由
./docs/PROJECT-SUMMARY.md:2913:- 路径：Phase 1楼栋级 → Phase 2寝室级
./docs/PROJECT-SUMMARY.md:2915:**决策2：楼栋匹配规则**
./docs/PROJECT-SUMMARY.md:2916:- 按楼栋名称吻合匹配（exact或normalized）
./docs/PROJECT-SUMMARY.md:2919:**决策3：File2独有116行处理**
./docs/PROJECT-SUMMARY.md:2921:- 总学生数：5830（File1）+ 116（File2独有）= 5946行
./docs/PROJECT-SUMMARY.md:2930:- merge_student_data.py：增加File2独有行处理逻辑
./docs/PROJECT-SUMMARY.md:2932:  - 追加未匹配File2行到输出
docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:24:- 4个Django测试文件覆盖当前7个失败点
./docs/Excel数据源实际分析结果.md:17:校区, 楼栋名称, 寝室号, 学生姓名, 性别, 专业, 学院名称, 班级, 层次, 年级
./docs/Excel数据源实际分析结果.md:77:Row 1 (header): 序号, 楼栋号, 职工号, 姓名, 电话
./docs/Excel数据源实际分析结果.md:133:  - 选文件2 → 有学号，但无学院（审批路由失效）
./docs/Excel数据源实际分析结果.md:153:- 审批路由无法工作
./docs/Excel数据源实际分析结果.md:157:### 缺陷3：部分宿管员无工号
./docs/Excel数据源实际分析结果.md:163:- 这些宿管员无法导入系统（user_id必填）
./docs/Excel数据源实际分析结果.md:176:| 数据量 | 100% | 5675-5830人符合预期 |
./docs/Excel数据源实际分析结果.md:183:| 字段完整性 | 100% | 所有必需字段齐全 |
./docs/Excel数据源实际分析结果.md:184:| 数据质量 | 100% | 工号格式统一 |
./docs/Excel数据源实际分析结果.md:185:| **综合评分** | **100%** | **满足要求** |
./docs/Excel数据源实际分析结果.md:187:### 3.3 宿管员表（User - role=dorm_manager）
./docs/Excel数据源实际分析结果.md:231:**步骤3：补充宿管员工号**
./docs/Excel数据源实际分析结果.md:278:**宿管员文件必需列：**
./docs/Excel数据源实际分析结果.md:335:| 辅导员表 | ✅ 100% | 无 | 可直接使用 |
./docs/Excel数据源实际分析结果.md:336:| 宿管员表 | ⚠️ 75% | 部分工号缺失 | 补充工号 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:5:**目的：** 明确毕业离校系统所需的数据源，提交给宿管系统方反馈
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:22:- **DB优先**：直接读取宿管系统数据库（推荐，支持MySQL/SQL Server/Oracle）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:23:- **API备选**：调用宿管系统提供的API接口
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:63:-- 示例查询（假设宿管系统有学生表）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:105:| 宿舍楼栋 | dorm_building | 文本 | 否 | 宿舍楼栋名称 | 1号楼 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:166:-- 示例查询（假设宿管系统有辅导员表）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:201:- 上线前必须达到100%覆盖率
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:248:- 上线前必须达到100%当届学生可解析到有效辅导员
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:290:- 网络连通性：本系统服务器能访问宿管系统数据库
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:353:1. 宿管系统方按模板导出CSV文件
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:394:**如果宿管系统数据库包含所有数据：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:399:**如果宿管系统数据库只包含部分数据：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:411:4. 班级-辅导员对应关系：CSV导入（必须100%覆盖）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:418:请宿管系统方反馈以下问题：
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:421:1. 宿管系统使用的数据库类型？（MySQL / SQL Server / Oracle / PostgreSQL / 其他）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:448:1. **宿管系统方**：反馈上述问题，提供数据库/API/CSV的可行性
./docs/contracts/contract-v0.1.md:412:        # 固定返回规则（覆盖所有状态）
./docs/Excel数据源分析与需求对比.md:15:| 文件3 | 2026年社区辅导员信息统计表.xls | 30.0K | 宿管员信息 |
./docs/Excel数据源分析与需求对比.md:28:| **class_id** | **班级ID** | string | ✓ | **审批路由关键字段** | **文件1或文件2** |
./docs/Excel数据源分析与需求对比.md:54:### 2.3 宿管员表（User - role=dorm_manager）
./docs/Excel数据源分析与需求对比.md:59:| name | 姓名 | string | ✓ | 宿管员姓名 | 文件3 |
./docs/Excel数据源分析与需求对比.md:116:### 3.3 宿管员文件检查（文件3）
./docs/Excel数据源分析与需求对比.md:133:5. ✅ 文件3包含宿管员工号、姓名
./docs/Excel数据源分析与需求对比.md:197:3. `dorm_managers.csv` - 宿管员数据
./docs/PROJECT-COMPLETION-DECLARATION.md:40:✓ 单元测试：**172/172通过（100%）**  
./docs/PROJECT-COMPLETION-DECLARATION.md:42:- H1: 正常审批流程（学生→宿管员→辅导员→学工部→批准）
./docs/PROJECT-COMPLETION-DECLARATION.md:43:- H2: 驳回流程（学生→宿管员→辅导员驳回）  
./docs/PROJECT-COMPLETION-DECLARATION.md:49:- 字段完整性：number100%, name100%, phone80%, status100%
./docs/api-samples/notifications_list.json:36:      "message": "您的离校申请已通过宿管员审批。",
./docs/api-samples/application_detail.json:16:      "approver_name": "宿管员1",
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:230:   - 同意。需要完整覆盖
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:267:- 第10章测试策略（TDD、PostgreSQL、覆盖）
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:477:3. 提交给宿管系统方反馈
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:11:**用户要求：** "第一审批人学校要求是宿管员，第二审批人是辅导员"
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:22:学生提交申请 → 宿管员审批 → 辅导员审批 → 完成
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:45:    PENDING_DORM_MANAGER = 'pending_dorm_manager', '待宿管员审批'
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:61:    DORM_MANAGER = 'dorm_manager', '宿管员'
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:73:- 申请提交后创建宿管员审批记录（不是辅导员）
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:74:- 宿管员审批通过后创建辅导员审批记录（不是院长）
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:99:- "待辅导员审批" → "待宿管员审批"
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:117:3. 更新申请提交逻辑（创建宿管员审批）
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:118:4. 更新审批通过逻辑（宿管员→辅导员，辅导员→完成）
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:163:**风险：** 需要确保宿管员角色在系统中存在且配置正确
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:168:- 创建测试数据时包含宿管员角色
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:175:- [ ] 申请提交后创建宿管员审批记录
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:176:- [ ] 宿管员审批通过后创建辅导员审批记录
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:187:1. ✅ 两级审批足够（宿管员→辅导员）
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:189:3. ⚠️ 宿管员角色需要在系统中添加/确认
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:192:- 审批流程：学生提交 → 宿管员审批 → 辅导员审批 → **完成**
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decision.md:46:1. 学生提交 → 宿管员审批 → 辅导员审批 → 状态变为已通过
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decision.md:83:4. 宿管员/辅导员登录 → 列表页标题显示"审批列表"
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:58:   - 对宿管员/辅导员审批列表有意义，但对学工部“只看 approved”场景会产生冗余 UI。
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:70:- 宿管员：第一审批
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:80:2. 宿管员审批通过。
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:109:   - 宿管员/辅导员：`审批列表`
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:113:   - 宿管员/辅导员：`暂无待审批申请`
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:117:   - 宿管员/辅导员且当前审批人匹配：显示同意/驳回按钮
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:58:- [ ] 19个API端点是否覆盖所有业务场景？
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:149:- [ ] 测试覆盖率目标是否合理？
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:155:- 单元测试覆盖率 >80%
./docs/discussions/ui-design-2026-06-02/10-final-consensus-dean-filing-ui.md:28:| 元素 | 宿管员/辅导员 | 学工部 |
./docs/discussions/ui-design-2026-06-02/10-final-consensus-dean-filing-ui.md:69:4. 宿管员/辅导员列表页标题显示"审批列表"
./docs/discussions/ui-design-2026-06-02/10-final-consensus-dean-filing-ui.md:70:5. 宿管员/辅导员详情页根据当前审批人显示按钮
docs/外部系统数据接口确认清单.md:12:根据XG API数据覆盖度分析（2026-06-03），当前XG用户API缺失3个P0关键业务字段，导致无法独立支持毕业生离校申请审批系统。需向相关外部系统确认是否能提供缺失数据。
./docs/XG-API数据不足解决方案讨论.md:45:- ✓ 业务完整性100%保障
./docs/XG-API数据不足解决方案讨论.md:255:2. ✓ 业务完整性100%保障
./docs/XG-API数据不足解决方案讨论.md:277:- [ ] 验证ClassMapping覆盖率
./docs/XG-API数据不足解决方案讨论.md:378:2. 业务完整性100%保障
./docs/XG-API数据不足解决方案讨论.md:396:- ✓ CSV导入成功率 100%
./docs/XG-API数据不足解决方案讨论.md:397:- ✓ ClassMapping覆盖率 100%
./docs/XG-API数据不足解决方案讨论.md:403:- ✓ 辅导员自动分配成功率 100%
./docs/XG-API数据不足解决方案讨论.md:404:- ✓ 申请资格判定准确率 100%
./docs/week3-day0-acceptance-checklist.md:531:- 测试覆盖不足
docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:15:2. ✗ URL路由实现有坑（/api/applications/已绑定POST）
docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:44:### 错误5: URL路由方案不可行
docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:45:**原提案:** 直接添加GET路由到/api/applications/  
docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:187:### Step 3: 重构/api/applications/路由 (45min)
docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:242:- 合并GET/POST路由
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:471:- 覆盖率：核心90%、整体70%
./docs/XG-API-ACTUAL-DATA-SAMPLES.md:51:| number（学号） | 20 | 0 | 0 | 100% | ✓ 优秀 |
./docs/XG-API-ACTUAL-DATA-SAMPLES.md:52:| name（姓名） | 20 | 0 | 0 | 100% | ✓ 优秀 |
./docs/XG-API-ACTUAL-DATA-SAMPLES.md:54:| status（状态） | 20 | 0 | 0 | 100% | ✓ 优秀 |
./docs/XG-API-ACTUAL-DATA-SAMPLES.md:65:| user_identity（身份信息） | 20 | 0 | 100% | ✓ 优秀 |
./docs/XG-API-ACTUAL-DATA-SAMPLES.md:66:| department（部门） | 20 | 0 | 100% | ✓ 优秀 |
./docs/XG-API-ACTUAL-DATA-SAMPLES.md:67:| parent_dep（父级部门） | 20 | 0 | 100% | ✓ 优秀 |
docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md:29:4. **路由写法正确**
docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md:30:   - `urls.py` 使用 `from . import views` 时，新增路由必须写为 `views.list_approvals`。
docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md:40:- 执行验证时建议同时覆盖 `?limit=5&offset=0` 和 `?limit=5&offset=5`，避免只证明第一页可用。
docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:84:### 错误4: URL路由导入问题
docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:206:### 4.3 更新URL路由
docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:239:3. **更新路由** (5min)
docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:257:4. ✓ URL路由使用 `views.list_approvals`
docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:271:- URL路由使用 `views.` 前缀
./docs/XG-API-数据源全面分析报告.md:18:- 基础字段覆盖：27% (3/11)
./docs/XG-API-数据源全面分析报告.md:19:- 必填字段覆盖：57% (4/7)
./docs/XG-API-数据源全面分析报告.md:20:- **关键业务字段覆盖：0% (0/3)** ← 核心阻断
./docs/XG-API-数据源全面分析报告.md:45:| 序号 | 需求字段 | 必填性 | XG提供字段 | 覆盖状态 | 完整性 | 不满足原因 |
./docs/XG-API-数据源全面分析报告.md:47:| 1 | student_id | ✓ 必填 | number | ✅ 满足 | 100% | - |
./docs/XG-API-数据源全面分析报告.md:48:| 2 | name | ✓ 必填 | name | ✅ 满足 | 100% | - |
./docs/XG-API-数据源全面分析报告.md:49:| 3 | department | ✓ 必填 | department[0].name | ✅ 满足 | 100% | - |
./docs/XG-API-数据源全面分析报告.md:56:**必填字段覆盖率：50% (4/8)**  
./docs/XG-API-数据源全面分析报告.md:61:| 序号 | 需求字段 | 必填性 | XG提供字段 | 覆盖状态 | 完整性 | 不满足原因 |
./docs/XG-API-数据源全面分析报告.md:67:**可选字段覆盖率：33% (1/3)**  
./docs/XG-API-数据源全面分析报告.md:72:| 序号 | 需求字段 | 必填性 | XG提供字段 | 覆盖状态 | 不满足原因 |
./docs/XG-API-数据源全面分析报告.md:81:**辅导员字段覆盖率：67% (4/6)**  
./docs/XG-API-数据源全面分析报告.md:82:**注：** 辅导员数据未进行实际采样验证，覆盖度基于字段结构推断
./docs/XG-API-数据源全面分析报告.md:86:| 序号 | 需求字段 | 必填性 | XG提供 | 覆盖状态 | 不满足原因 |
./docs/XG-API-数据源全面分析报告.md:92:**班级映射覆盖率：0% (0/3)**  
./docs/XG-API-数据源全面分析报告.md:97:| 序号 | 需求字段 | 必填性 | XG用户API提供 | 覆盖状态 | 不满足原因 |
./docs/XG-API-数据源全面分析报告.md:103:**宿舍清退覆盖率：0% (0/3)**  
./docs/XG-API-数据源全面分析报告.md:141:- ✓ 已实施：API同步时不覆盖class_id字段
./docs/XG-API-数据源全面分析报告.md:176:- ✓ 已实施：API不创建新用户，不覆盖is_graduating
./docs/XG-API-数据源全面分析报告.md:210:- ✓ 已实施：API不覆盖graduation_year字段
./docs/XG-API-数据源全面分析报告.md:321:- 可能覆盖本地已有的有效phone值
./docs/XG-API-数据源全面分析报告.md:330:- API同步时跳过空值，不覆盖已有有效值
./docs/XG-API-数据源全面分析报告.md:426:| number | 20 | 20 | 0 | 0 | 100% | ✓ 优秀 |
./docs/XG-API-数据源全面分析报告.md:427:| name | 20 | 20 | 0 | 0 | 100% | ✓ 优秀 |
./docs/XG-API-数据源全面分析报告.md:429:| status | 20 | 20 | 0 | 0 | 100% | ✓ 优秀 |
./docs/XG-API-数据源全面分析报告.md:430:| department | 20 | 20 | 0 | 0 | 100% | ✓ 优秀 |
./docs/XG-API-数据源全面分析报告.md:431:| user_identity | 20 | 20 | 0 | 0 | 100% | ✓ 优秀 |
./docs/XG-API-数据源全面分析报告.md:472:| **综合得分** | **93.5/100** | **100%** | **93.5** |
./docs/XG-API-数据源全面分析报告.md:476:**结论：** XG API提供的字段数据质量优秀，但业务字段覆盖度严重不足。
./docs/XG-API-数据源全面分析报告.md:501:  ↓ 不覆盖：class_id, is_graduating, graduation_year
./docs/XG-API-数据源全面分析报告.md:516:- ✗ XG API覆盖class_id/is_graduating/graduation_year
./docs/XG-API-数据源全面分析报告.md:563:- 规则：不覆盖已有有效值
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:20:**Codex指出：** 文档写 `password123/counselor/dean/dorm_manager`，实际学生密码=学号，辅导员=`T001/T002`，学工部=`D001`，宿管员账号未创建
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:36:| 宿管员 | （暂未实现） | - | 第一级审批 |
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:38:**注意：** 当前版本宿管员账号和映射尚未在种子数据中实现。
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:84:### P0-3: 小程序宿管员角色守卫冲突
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:86:**Codex指出：** 文档说宿管员登录后进入审批列表，但 approvals.ts:19 只允许 `['counselor', 'dean']`
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:90:- 文档 docs/操作说明书.md:162 描述宿管员登录后自动进入"审批列表"页面
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:99:⚠️ **注意：** 当前版本小程序审批页面仅支持辅导员和学工部角色访问，宿管员功能暂未实现。
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:102:1. 输入账号：（宿管员账号暂未配置）
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:103:2. Demo Web支持宿管员审批流程
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:257:1. 修复测试账号表格（明确标注宿管员未实现）
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:259:3. 宿管员小程序限制说明（采用选项A标注）
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:50:**Codex指出：** onShow中非学生统一reLaunch到login，覆盖onLoad的角色矩阵
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:54:- 生命周期冲突：onShow在onLoad后触发，会覆盖redirectTo
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:146:**文件：** `docs/用户设计说明书.md:116, 144-145, 149`
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:23:**Codex意见：** "全量覆盖（清空后重新导入）"会导致外键约束冲突，必须改为"staging表 + upsert + 软停用"。
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:31:导入策略：首版采用**全量覆盖**（清空后重新导入）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:422:导入策略：首版采用**全量覆盖**（清空后重新导入）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:447:- 删除"全量覆盖"描述
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:464:1. ✅ CSV导入从"全量覆盖"改为"staging + upsert + 软停用"
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:477:3. 提交给宿管系统方反馈
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:95:- ✓ 19个API端点覆盖完整
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:19:6. 修改login.ts添加角色路由
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:27:**当前方案：** 先完整实现student-application页面（4个文件），最后修改login.ts路由
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:30:- 如果先实现页面但不修改路由，学生登录后无法访问新页面
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:31:- 如果先修改路由但页面不存在，会导致404错误
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:34:**替代方案A：** 先修改login.ts路由（添加条件判断但暂时注释），再实现页面，最后取消注释
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:35:**替代方案B：** 先创建空页面骨架（4个文件最小化内容），注册+路由，再逐步填充逻辑
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:36:**替代方案C：** 保持当前顺序，但在app.json注册后立即测试404，确认路由前页面可访问
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:58:- 如果login.ts路由已正确实现，角色保护是否冗余？
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:60:- 但如果login.ts路由有bug，角色保护会掩盖路由问题
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:62:**替代方案A：** 先不实现角色保护，依赖login.ts路由，测试通过后再添加防御性保护
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:63:**替代方案B：** 先实现角色保护，即使login.ts路由有bug也能防御
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:77:    return `宿舍清退未完成：${err.error.blocking_reason || '请联系宿管'}`;
./docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:14:更合理的下一步是 **Option A-prime：主动关闭API Schema P1验证门禁**。55号文档把P1描述为“已完成”，但同时列出三个关键待验证项：schema生成无警告、schema/swagger-ui可访问、operationId唯一。只要这些未验证，P1还不能视为完成。
./docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:52:1. **先做P1关闭门禁。**
./docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:57:   - 示例只覆盖最关键端点即可，不要扩大成完整文档重写。
./docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:65:- **P1关闭门禁：** 环境可用时约0.5-1.5小时；若需要修依赖、数据库或settings，可能更久。
./docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:66:- **P2示例：** 45-90分钟较合理，不建议默认1.5小时以上，除非要覆盖大量错误分支。
./docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:108:> 下一步不直接执行API Schema P2。先执行Option A-prime：主动关闭API Schema P1验收门禁，修复已发现的login成功响应schema不匹配，并在可用Django环境中验证schema生成无警告、schema/swagger-ui可访问、operationId唯一。只有P1真实绿灯后，再执行一个收敛版P2，为登录、申请提交、审批操作、通知列表和通用错误补OpenApiExample。如果当前环境无法完成P1验证，则硬停止并将P1状态标记为“代码完成，未验收”，等待可验证环境。
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:218:4. **MAJOR**: 缺少覆盖：
./docs/superpowers/plans/2026-05-27-implementation-plan.md:69:- ✓ 单元测试覆盖率 > 80%
./docs/superpowers/plans/2026-05-27-implementation-plan.md:534:   - 配置页面路由
./docs/superpowers/plans/2026-05-27-implementation-plan.md:572:   - 确保覆盖率 > 80%
./docs/superpowers/plans/2026-05-27-implementation-plan.md:628:**风险5：测试覆盖不足**
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:71:学号,姓名,班级,宿舍楼栋,宿舍房间号,床号,是否已清退,清退日期,清退状态,备注
./docs/discussions/ui-design-2026-06-02/07-claude-response-to-gemini-ui-proposal.md:14:- 配色提取完整（主色、辅助色、背景、文本、状态色全覆盖）
./docs/discussions/ui-design-2026-06-02/07-claude-response-to-gemini-ui-proposal.md:90:✅ 移动端width 100%：保持当前实现
./docs/XG-API-COLLECTION-TEST-GUIDE.md:142:- [ ] 分页测试覆盖至少3页
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:173:文档12说"优先覆盖跨辅导员403、重复审批409、重复提交409"，但没有说具体测试文件和测试方法。
./docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:77:- test断言是否覆盖了Option 1的核心验证点？
./docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:85:### 4. 测试覆盖
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:116:| dorm_building | String | 宿舍楼栋 | 是 | "1号楼" |
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:26:| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:77:并发测试不能只用普通`TestCase`。SQLite下`select_for_update()`基本不能证明锁语义，应至少用`TransactionTestCase`覆盖重复请求返回409；真正并发正确性最好在Docker/Postgres环境跑集成测试。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:104:- `BASE_URL`默认`http://localhost:8001`，可通过环境变量覆盖。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:158:- 核心Django测试通过，至少覆盖申请、审批、驳回、权限、重复提交。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:160:- smoke test覆盖至少三个负向场景：跨辅导员403、重复审批409、重复提交409。
./docs/用户需求最终确认与实施方案.md:19:| **File 3** | `2026年社区辅导员信息统计表.xls` | 宿管员数据（按楼栋） | 33楼栋 |
./docs/用户需求最终确认与实施方案.md:21:| **File 5** | `file5_students_5946.csv` | 合并输出文件（File1+File2全部） | 5946行 |
./docs/用户需求最终确认与实施方案.md:36:- File2 (5675行) 补充学号(XH)、班号(BH)等字段
./docs/用户需求最终确认与实施方案.md:37:- File2没有的155行学生（File1独有）：补充字段留空
./docs/用户需求最终确认与实施方案.md:38:- File2独有的116行学生：导入为额外学生（用户决策3）
./docs/用户需求最终确认与实施方案.md:39:- 271行研究生：补充字段留空（File2无研究生数据）
./docs/用户需求最终确认与实施方案.md:42:- ✓ 解决了"271研究生+116 File2独有学生"问题
./docs/用户需求最终确认与实施方案.md:43:- ✓ 全部5946行学生可导入（5830 File1 + 116 File2独有）
./docs/用户需求最终确认与实施方案.md:64:> "第一次审批按楼栋数据向宿管员申请，第一次审批通过后，再按学院向辅导员发起第二次审批"
./docs/用户需求最终确认与实施方案.md:68:学生提交 → 宿管员审批(by class_id) → 辅导员审批(by class_id) → 学工部审批 → 完成
./docs/用户需求最终确认与实施方案.md:73:学生提交 → 宿管员审批(by 楼栋) → 辅导员审批(by 学院) → 完成（保存结果）
./docs/用户需求最终确认与实施方案.md:78:- 路由方式从 `class_id` 改为 `building` + `college`
./docs/用户需求最终确认与实施方案.md:83:- ⚠️ 需要修改路由逻辑
./docs/用户需求最终确认与实施方案.md:85:- ✓ 解决"楼栋跨班级"问题
./docs/用户需求最终确认与实施方案.md:110:| 宿管员 (dorm_manager) | 第一次审批（按楼栋） | 只看自己负责楼栋的申请 |
./docs/用户需求最终确认与实施方案.md:123:### 确认1: 楼栋审批关系
./docs/用户需求最终确认与实施方案.md:126:> "楼栋按文件5与文件3中共同的楼栋字段为审批关系设定"
./docs/用户需求最终确认与实施方案.md:129:- File5 (学生).楼栋名称 ↔ File3 (宿管员).楼栋号
./docs/用户需求最终确认与实施方案.md:131:- 一个楼栋对应多个宿管员：任一人可审批（待确认）
./docs/用户需求最终确认与实施方案.md:139:- File5 (学生) 有：楼栋名称 + 寝室号 ✓
./docs/用户需求最终确认与实施方案.md:140:- File3 (宿管员) 有：楼栋号 ✓，无寝室号 ✗
./docs/用户需求最终确认与实施方案.md:144:- 路由升级：楼栋级（一对多）→ 楼栋+寝室号级（一对一）
./docs/用户需求最终确认与实施方案.md:147:- **Phase 1（当前）：** 按楼栋路由（building-level）
./docs/用户需求最终确认与实施方案.md:148:- **Phase 2（File3补充后）：** 按楼栋+寝室号路由（room-level，精确一对一）
./docs/用户需求最终确认与实施方案.md:166:- 271研究生 + File2未匹配学生缺少学号
./docs/用户需求最终确认与实施方案.md:167:- 与"全部5946行可导入"矛盾（5830 File1 + 116 File2独有）
./docs/用户需求最终确认与实施方案.md:178:#### P0-2: 多宿管员与单审批人模型冲突
./docs/用户需求最终确认与实施方案.md:181:- 文档建议"任一宿管员可审批"
./docs/用户需求最终确认与实施方案.md:189:- 每栋楼指定唯一主责宿管员
./docs/用户需求最终确认与实施方案.md:196:- Phase 2只说"路由逻辑重构"但未列完整清单
./docs/用户需求最终确认与实施方案.md:203:  2. 提交路由重构（apps/applications/views.py:147-179）
./docs/用户需求最终确认与实施方案.md:204:  3. 审批通过路由重构（apps/approvals/views.py:149-174）
./docs/用户需求最终确认与实施方案.md:223:| 班级字段缺失 | ⚠️ File1有，File2格式不同 | 决策2：暂时为空 | ✅ 已解除 |
./docs/用户需求最终确认与实施方案.md:225:| 楼栋→宿管员一对多 | ⚠️ 无法确定选主规则 | 决策3：楼栋级路由 | ✅ 已解除 |
./docs/用户需求最终确认与实施方案.md:239:user_id        # 学号（File2补充，可能为空）
./docs/用户需求最终确认与实施方案.md:244:building_name  # 楼栋名称（File1） - 第一次审批路由键
./docs/用户需求最终确认与实施方案.md:245:room_number    # 寝室号（File1） - 未来精确路由键
./docs/用户需求最终确认与实施方案.md:246:department     # 学院名称（File1规范化） - 第二次审批路由键
./docs/用户需求最终确认与实施方案.md:247:class_id       # 班级（可为空） - 不用于路由
./docs/用户需求最终确认与实施方案.md:252:phone          # 手机号（File2补充）
./docs/用户需求最终确认与实施方案.md:253:email          # 邮箱（File2补充）
./docs/用户需求最终确认与实施方案.md:256:**DormManager (用户表 - 宿管员角色)：**
./docs/用户需求最终确认与实施方案.md:261:building       # 负责楼栋（File3）
./docs/用户需求最终确认与实施方案.md:296:- `PENDING`: 学生已提交，等待宿管员审批
./docs/用户需求最终确认与实施方案.md:297:- `DORM_MANAGER_APPROVED`: 宿管员已通过，等待辅导员审批
./docs/用户需求最终确认与实施方案.md:301:### 4.3 路由逻辑变更
./docs/用户需求最终确认与实施方案.md:303:**当前路由（基于ClassMapping）：**
./docs/用户需求最终确认与实施方案.md:313:**新路由（基于Building + Department）：**
./docs/用户需求最终确认与实施方案.md:317:        # 第一次审批：按楼栋查宿管员
./docs/用户需求最终确认与实施方案.md:333:| 操作 | 学生 | 宿管员 | 辅导员 | 学工管理员 |
./docs/用户需求最终确认与实施方案.md:337:| 第一次审批（楼栋） | ✗ | ✓ | ✗ | ✗ |
./docs/用户需求最终确认与实施方案.md:338:| 查看楼栋范围申请 | ✗ | ✓ | ✗ | ✗ |
./docs/用户需求最终确认与实施方案.md:351:**修正后：** 4-6天（增加Phase 0数据门禁）
./docs/用户需求最终确认与实施方案.md:353:### Phase 0: 数据画像与路由门禁（1-1.5天）
./docs/用户需求最终确认与实施方案.md:355:**目标：** 关闭3个P0阻塞，确保数据可导入且路由100%覆盖
./docs/用户需求最终确认与实施方案.md:365:    # File2未匹配：TMP2026_{row}
./docs/用户需求最终确认与实施方案.md:371:- `student_no`: 真实学号（可空，来自File2的XH）
./docs/用户需求最终确认与实施方案.md:375:**Task 0.2: File1+File2合并与完整报告（0.5天）**
./docs/用户需求最终确认与实施方案.md:383:    # - file2_only_count: 116
./docs/用户需求最终确认与实施方案.md:390:- `file5_students_5946.csv` - 全部5946行，user_id非空（5830 File1 + 116 File2独有）
./docs/用户需求最终确认与实施方案.md:393:**Task 0.3: 学院/楼栋规范化字典（0.2天）**
./docs/用户需求最终确认与实施方案.md:400:**楼栋规范化（需File3数据）：**
./docs/用户需求最终确认与实施方案.md:401:- `building_normalization_map.json` - 33个楼栋映射（待File3提供后创建）
./docs/用户需求最终确认与实施方案.md:402:- 依赖：需File3楼栋名称与File1对比，创建映射表
./docs/用户需求最终确认与实施方案.md:405:**状态：** 学院规范化✓完成，楼栋规范化⏳pending File3
./docs/用户需求最终确认与实施方案.md:407:**Task 0.4: 主责宿管员指定（0.3天）**
./docs/用户需求最终确认与实施方案.md:411:- 如楼栋有多人，人工或按默认规则（首位/编号最小）选主责
./docs/用户需求最终确认与实施方案.md:414:**Task 0.5: 路由覆盖验证（0.2天）**
./docs/用户需求最终确认与实施方案.md:422:    # 输出100%覆盖报告或失败清单
./docs/用户需求最终确认与实施方案.md:426:门禁标准：
./docs/用户需求最终确认与实施方案.md:427:- ✓ 5946行学生user_id非空且唯一（5830 File1 + 116 File2独有）
./docs/用户需求最终确认与实施方案.md:428:- ✓ 100%学生可路由到宿管员
./docs/用户需求最终确认与实施方案.md:429:- ✓ 100%学生可路由到辅导员
./docs/用户需求最终确认与实施方案.md:445:**任务1.2：File1 + File2合并脚本**
./docs/用户需求最终确认与实施方案.md:450:    # 2. 读取File2 (5675行) 作为补充
./docs/用户需求最终确认与实施方案.md:452:    # 4. File2有的：补充学号、专业、班号等字段
./docs/用户需求最终确认与实施方案.md:453:    # 5. File2没有的：对应字段留空
./docs/用户需求最终确认与实施方案.md:454:    # 6. File2独有的116行：追加为额外学生（用户决策3）
./docs/用户需求最终确认与实施方案.md:455:    # 7. 输出File5 (5946行：5830+116)
./docs/用户需求最终确认与实施方案.md:460:- `file5_students_5946.csv` - 完整学生数据（5830 File1 + 116 File2独有）
./docs/用户需求最终确认与实施方案.md:461:- `file3_dorm_managers.csv` - 宿管员数据（33楼栋）
./docs/用户需求最终确认与实施方案.md:471:**任务2.2：路由逻辑重构**
./docs/用户需求最终确认与实施方案.md:472:- 创建 `BuildingApprovalRouter` - 楼栋→宿管员路由
./docs/用户需求最终确认与实施方案.md:473:- 创建 `DepartmentApprovalRouter` - 学院→辅导员路由
./docs/用户需求最终确认与实施方案.md:499:# Step 3: 导入宿管员（33楼栋）
./docs/用户需求最终确认与实施方案.md:502:# Step 4: 验证路由
./docs/用户需求最终确认与实施方案.md:507:**前置门禁：**
./docs/用户需求最终确认与实施方案.md:509:- ✓ 每个学生的楼栋能找到至少1个宿管员
./docs/用户需求最终确认与实施方案.md:517:- 宿管员界面：查看楼栋范围申请+第一次审批
./docs/用户需求最终确认与实施方案.md:530:2. 按楼栋路由到正确宿管员
./docs/用户需求最终确认与实施方案.md:531:3. 宿管员审批通过
./docs/用户需求最终确认与实施方案.md:532:4. 按学院路由到正确辅导员
./docs/用户需求最终确认与实施方案.md:536:8. 权限隔离验证（学生/宿管/辅导/管理员）
./docs/用户需求最终确认与实施方案.md:538:**总时间：** 4-6天（原计划2.5-3天，增加Phase 0数据门禁1-1.5天）
./docs/用户需求最终确认与实施方案.md:541:- M0: Phase 0完成，路由100%覆盖验证通过（1-1.5天）
./docs/用户需求最终确认与实施方案.md:551:### 寝室号精确路由升级
./docs/用户需求最终确认与实施方案.md:570:**路由逻辑升级：**
./docs/用户需求最终确认与实施方案.md:576:    # 精确匹配：楼栋+寝室号 → 唯一宿管员
./docs/用户需求最终确认与实施方案.md:595:### 风险1: 楼栋名称不匹配
./docs/用户需求最终确认与实施方案.md:598:- File5楼栋名："荷园2栋"
./docs/用户需求最终确认与实施方案.md:599:- File3楼栋号："荷园二栋"
./docs/用户需求最终确认与实施方案.md:600:- 字符串不匹配导致路由失败
./docs/用户需求最终确认与实施方案.md:603:- 建立楼栋名称规范化表（类似学院规范化）
./docs/用户需求最终确认与实施方案.md:604:- 导入前验证：所有File5楼栋能在File3中找到对应
./docs/用户需求最终确认与实施方案.md:607:### 风险2: 多宿管员选择规则未定
./docs/用户需求最终确认与实施方案.md:610:- 一个楼栋有3个宿管员
./docs/用户需求最终确认与实施方案.md:615:- 方案B：指定主责宿管员（File3补充主责标记）
./docs/用户需求最终确认与实施方案.md:645:- ⏳ `scripts/merge_student_data.py` - File1+File2合并
./docs/用户需求最终确认与实施方案.md:646:- ⏳ `scripts/validate_building_routing.py` - 楼栋路由验证
./docs/用户需求最终确认与实施方案.md:647:- ⏳ `scripts/validate_department_routing.py` - 学院路由验证
./docs/用户需求最终确认与实施方案.md:652:- ⏳ `file3_dorm_managers.csv` - 宿管员数据
./docs/用户需求最终确认与实施方案.md:659:- ⏳ 楼栋路由器实现
./docs/用户需求最终确认与实施方案.md:660:- ⏳ 学院路由器实现
./docs/用户需求最终确认与实施方案.md:671:| DEC-001 | File1为基准合并File2 | 用户 | 2026-06-05 | 保留全部5830学生 |
./docs/用户需求最终确认与实施方案.md:673:| DEC-003 | 2级审批（楼栋→学院） | 用户 | 2026-06-05 | 移除学工部审批 |
./docs/用户需求最终确认与实施方案.md:675:| DEC-005 | 寝室号未来补充 | 用户 | 2026-06-05 | 精确路由需求 |
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:116:| dorm_building | String | 宿舍楼栋 | 是 | "1号楼" |
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:29:- ✅ 覆盖审批队列、通知查询、审计追踪
./docs/discussions/phase4c-next-steps/19-claude-next-phase-strategy-request.md:87:- 有完整测试覆盖，风险可控
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:80:- smoke test 中的负向场景脚本化，如果 Django 自动化测试已经覆盖负向用例。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:91:提案方向与 Day 2 共识一致，任务拆分也覆盖了主要漏洞。但执行策略低估了测试和数据可复现成本，"手工验证为主"和"允许跳过阻塞项"会削弱 Conditional Go 的可信度。若加入前置校验、最低自动化测试和不可跳过边界，评分可提升到 7.5/10。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:121:- 阶段2：assigned approver 权限覆盖 approve/reject；`get_application` 不再让任意 counselor/dean 查看所有申请。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:122:- 阶段3：审批状态机保护覆盖 approve/reject，且不会重复生成 dean approval。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:129:- smoke shell 脚本中的完整负向场景，前提是 Django 测试已覆盖负向用例。
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:140:3. **状态机保护：** 必须覆盖 approve 和 reject。只校验重复审批不够，还要校验 step/status 匹配，例如 dean approval 不能在 `pending_counselor` 状态下被操作。
./docs/discussions/ui-design-2026-06-02/04-complete-ui-coverage-analysis.md:1:# 完整UI功能覆盖分析
./docs/discussions/ui-design-2026-06-02/04-complete-ui-coverage-analysis.md:5:**目的：** 基于系统完整功能，识别UI覆盖缺口，提出完整页面清单
./docs/discussions/ui-design-2026-06-02/04-complete-ui-coverage-analysis.md:88:## 4. UI覆盖缺口分析
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:15:1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:18:4. 缺少若干实施级关键问题，例如账号标识映射、终审管理员分配规则、同步覆盖策略、历史审批人不被后续映射变更自动改写等。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:26:### 2.1 P0 数据源覆盖情况
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:28:当前 P0 数据源覆盖了系统运行所需的核心闭环：
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:134:4. CSV 需补充导入覆盖策略：全量覆盖、增量更新、软删除/停用、重复数据处理、失败回滚。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:168:当前问题覆盖了数据库、API、CSV 和数据范围，基本可用，但建议扩展为面向多方的数据确认清单。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:172:将“请宿管系统方反馈以下问题”改为：
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:174:> 请教务系统、人事系统、学工部数据负责人、宿管系统方分别确认其可提供的数据范围、字段、对接方式和联系人。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:176:原因：学生、辅导员、班级映射通常不是宿管系统的权责数据。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:188:9. CSV 导入时是否采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:199:共识文档中的推荐方案整体合理，但“如果宿管系统数据库包含所有数据”这个前提不够现实。学生、辅导员、班级映射不应假设都在宿管系统数据库中。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:203:1. 宿舍清退：优先使用宿管系统 API；若不可用，使用每日 CSV 导入；异常时保留人工证明。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:206:4. 班级-辅导员映射：首版优先 CSV/Excel 强校验，上线前必须 100% 覆盖当届学生。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:220:1. 先确认数据权责方和联系人，不把所有问题都压给宿管系统。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:222:3. 实现导入校验报告，重点校验学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:235:> 明确毕业离校系统所需的数据源，提交给宿管系统方反馈
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:239:> 明确毕业离校系统所需的数据源，提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人反馈。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:305:`31-data-source-requirements-consensus.md` 已经覆盖首版上线所需的主要 P0 数据源，字段设计也基本能支撑业务。它可以作为对接需求基础稿。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:309:1. 将反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
./docs/数据对接说明文档.md:237:- 班级映射覆盖率（所有学生的class_id都有对应辅导员）
docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md:49:> 请明确确认：是否授权 Claude 执行 Day 2，并接受 T0 启动门禁计入 6 小时硬封顶？  
docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md:50:> 回复"授权"即进入 T0 门禁；回复"不授权"则停止 Day 2 执行，改为整理 runbook/方案。  
./docs/phase4c-xg-field-coverage.md:1:# 学工系统用户API字段覆盖报告
./docs/phase4c-xg-field-coverage.md:31:| `number` | string | 100% | `"2025110140314"` | 学号/工号 |
./docs/phase4c-xg-field-coverage.md:32:| `name` | string | 100% | `"乐绍钧"` | 用户姓名 |
./docs/phase4c-xg-field-coverage.md:33:| `user_identity` | object | 100% | `{"id": 4, "name": "学生"}` | 身份类型（对象非字符串） |
./docs/phase4c-xg-field-coverage.md:34:| `department` | array | 100% | `[{"name": "计算机学院", "level": 2}]` | 院系（数组非字符串） |
./docs/phase4c-xg-field-coverage.md:36:| `status` | number | 100% | `1` | 账号状态（1=正常） |
./docs/phase4c-xg-field-coverage.md:119:| `User.class_id` | 未知 | 🔴 缺失 | **学生必填，API无法提供**。<br>- 继续由CSV/手工维护<br>- API同步时不覆盖此字段<br>- 新用户如果缺失`class_id`，标记为`skip_reason: missing_class_id` |
./docs/phase4c-xg-field-coverage.md:120:| `User.is_graduating` | 未知 | 🔴 缺失 | **学生必填，API无法提供**。<br>- 继续由CSV/手工维护<br>- API同步时不覆盖此字段<br>- 新用户如果缺失，标记为`skip_reason: missing_is_graduating` |
./docs/phase4c-xg-field-coverage.md:121:| `User.graduation_year` | 未知 | 🔴 缺失 | **学生必填，API无法提供**。<br>- 继续由CSV/手工维护<br>- API同步时不覆盖此字段<br>- 新用户如果缺失，标记为`skip_reason: missing_graduation_year` |
./docs/phase4c-xg-field-coverage.md:147:| `class_id`缺失 | 保持原值（不覆盖），新用户跳过并标记`missing_class_id` |
./docs/phase4c-xg-field-coverage.md:148:| `is_graduating`缺失 | 保持原值（不覆盖），新用户跳过并标记`missing_is_graduating` |
./docs/phase4c-xg-field-coverage.md:149:| `graduation_year`缺失 | 保持原值（不覆盖），新用户跳过并标记`missing_graduation_year` |
./docs/phase4c-xg-field-coverage.md:182:**在字段未完全覆盖前，API只能补充或更新可确定字段，不能替代CSV导入。**
docs/操作说明书.md:13:毕业生离校申请审批系统用于管理毕业生离校申请的提交、审批和备案流程。系统采用两级审批模式：宿管员审批 → 辅导员审批，学工部进行备案查询。
docs/操作说明书.md:20:| 宿管员 (dorm_manager) | 第一级审批 | 审批宿舍清退相关事项 |
docs/操作说明书.md:29:宿管员审批（通过/驳回）
docs/操作说明书.md:152:   - **待宿管员审批**：等待宿管员处理
docs/操作说明书.md:153:   - **待辅导员审批**：宿管员已通过，等待辅导员处理
docs/操作说明书.md:162:4. 审批流程从第一级（宿管员）重新开始
docs/操作说明书.md:164:### 3.2 宿管员操作
docs/操作说明书.md:168:⚠️ **注意：** 当前版本宿管员功能尚未完全实现：
docs/操作说明书.md:169:- 种子数据未包含宿管员测试账号
docs/操作说明书.md:173:宿管员功能在Demo Web中可正常使用（需先配置测试账号）
docs/操作说明书.md:219:操作步骤与宿管员相同：
docs/操作说明书.md:220:1. 查看待审批列表（仅显示宿管员已通过的申请）
docs/操作说明书.md:222:3. 查看审批记录（可见宿管员的审批意见）
docs/操作说明书.md:250:   - 完整审批记录（宿管员 + 辅导员）
docs/操作说明书.md:278:A: 您所在班级尚未配置审批流程（辅导员或宿管员信息缺失）。请联系系统管理员配置班级映射关系。
docs/操作说明书.md:324:**注意：** 运行 `python manage.py seed_data` 后可用上述账号。当前版本宿管员账号和映射尚未在种子数据中实现。
docs/操作说明书.md:329:2. 切换宿管员账号审批通过
./docs/discussions/phase4c-next-steps/89-claude-response-agree-fixes.md:18:4. ✅ **测试覆盖gap真实**：遗漏doc 85明确要求的边界场景
./docs/discussions/phase4c-next-steps/89-claude-response-agree-fixes.md:196:### 修复5：补充测试（覆盖gap）
docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:34:**16号明确：** 授权后"立即进入T0门禁"，T0计入硬封顶。
docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:108:> 请明确确认：是否授权 Claude 执行 Day 2，并接受 T0启动门禁计入6小时硬封顶？  
docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:109:> 回复"授权"即立即进入 T0门禁；回复"不授权"则停止 Day 2 执行，改为只整理 runbook/方案。
docs/数据确认清单.md:13:**问题1：** 宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？
docs/数据确认清单.md:62:**问题11：** CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/数据确认清单.md:116:1. 向宿管系统提交本确认清单
docs/数据确认清单.md:154:1. 对接宿管系统宿舍清退API
docs/数据确认清单.md:225:| 宿管系统无法提供完整数据 | 高 | 提前确认数据可用性，必要时调整对接范围 |
docs/数据确认清单.md:237:**宿管系统联系人：** [待填写]  
./docs/操作说明书-待改进事项.md:14:3. ✅ 小程序宿管员限制 - 已添加警告说明
./docs/操作说明书-待改进事项.md:28:**当前状况：** 第2章"系统部署"仅覆盖安装部署，缺少运维管理内容
./docs/操作说明书-待改进事项.md:93:- ✓ 两级审批流程（宿管员→辅导员）
./docs/操作说明书-待改进事项.md:100:- ⚠️ 宿管员账号和映射（种子数据缺失）
./docs/操作说明书-待改进事项.md:101:- ⚠️ 小程序宿管员审批页（角色守卫限制）
docs/design/2026-05-27-system-design.md:2553:- 覆盖率目标：80%+
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:153:登录、token解析、application_id/approval_id提取、HTTP状态码判断、reset/cleanup、错误输出，任何一个字段与文档不一致都会吃时间。45分钟能搭骨架，但不一定能形成可信证据。可接受的压缩方式是：如果Django测试已经覆盖正向路径，smoke只保留最薄的端到端脚本。
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:206:- 优先覆盖跨辅导员403、重复审批409、重复提交409。
./docs/discussions/ui-design-2026-06-02/05-ui-enhancement-color-responsive.md:149:| 容器宽度 | 100% | max-width: 1200px, 居中 |
./docs/discussions/ui-design-2026-06-02/05-ui-enhancement-color-responsive.md:254:- 移动端优先 (`max-width: 100%`, 单列布局)。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:10:`29-data-source-analysis.md` 的方向是正确的：当前数据对接文档只覆盖宿舍清退，无法完整支撑 student、counselor、admin 三类角色的账号初始化、权限边界和自动审批分配。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:28:| 宿舍清退数据 | 宿管系统 | P0 | 当前业务把宿舍清退作为提交前校验项，现有对接文档已覆盖。即使保留人工证明降级，正式流程仍应具备自动校验或批量数据导入能力。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:49:| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入、人工证明降级 | 当前文档策略合理。提交申请时实时性较强，API 价值高；若宿管系统暂不支持 API，则每日文件导入加人工证明降级。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:63:原因不是“方便展示”，而是学生账号、身份识别、申请资格、班级映射都依赖它。当前数据对接文档的目标用户也应从“宿舍管理系统管理员”扩展为“教务系统、人事系统、宿管系统及业务数据负责人”。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:82:建议数据对接文档单独增加“审批关系数据”章节，并把导入覆盖率 100% 作为上线验收条件之一。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:106:4. **导入校验和差异报告。** P0 数据导入不能只要求字段格式，还应要求失败明细、重复数据处理、覆盖策略、回滚策略和导入审计日志。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:132:4. **实现班级-辅导员映射导入。** 这是最关键步骤。上线前必须校验当届学生 100% 能解析到有效辅导员，否则不应开放提交。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:152:3. 新增“班级-辅导员对应关系导入”章节，列为 P0，并写明覆盖率和异常报告要求。
./docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:131:### 3. 阻断测试覆盖了Option 1核心行为
./docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:133:`backend/apps/notifications/tests/test_auto_notifications_api.py:245-257`覆盖了三点：
./docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:140:这已经覆盖Option 1的核心验收点。验证422错误message可以作为P2增强，但不是当前commit门禁；当前断言已足够证明“阻断不产生申请、不产生通知”。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:40:整体质量较好：需求目标明确，技术路线已基本固定，设计文档覆盖面广，评审过程记录完整，并且多轮审查已经识别并修正了若干关键方向性问题，例如“本项目数据库统一为 PostgreSQL”“外部系统 API 优先”“单实例部署”“上传安全”“工作日计算”“PostgreSQL 测试基线”等。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:84:`docs/design/2026-05-27-system-design.md` 已覆盖 10 个主要部分：
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:169:   Phase 1 同时包含 Django 初始化、Docker、Celery、开发工具等任务。作为计划本身没有问题，但当前已完成部分只覆盖了目录、`.gitignore`、requirements。项目总结中已经正确标注其余任务为暂停/待继续。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:193:- 补充 PostgreSQL 测试、覆盖率、性能目标
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:239:已配置内容覆盖：
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:255:`.gitignore` 覆盖面合理，适合当前技术栈。尤其是 `.env`、`node_modules/`、`.pytest_cache/`、`staticfiles/`、`db.sqlite3` 等常见噪声和敏感文件都已排除。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:322:## 10. 本次分析没有覆盖的内容
./docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:135:4. 真实API测试通过 `XG_RUN_LIVE_API_TEST=1` 门禁
./docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:249:### Step 2：实现Mock测试（CI覆盖）
./docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:259:- 测试覆盖签名生成、请求构造、响应解析
./docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:271:4. 记录响应结构和字段覆盖情况
./docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:299:4. ✅ 真实API不进CI，通过环境变量门禁
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:131:- Smoke test负向场景脚本化（如果Django测试已覆盖）
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:203:3. **状态机保护** - 接受，必须覆盖approve和reject，校验step/status匹配
./docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md:49:- 当前路由是`/api/auth/login`（无尾斜杠）
./docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md:55:- 精确记录当前路由和响应
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:126:- 优先覆盖跨辅导员403、重复审批409、重复提交409
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:188:2. Assigned approver权限覆盖approve/reject
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:190:4. 审批状态机保护覆盖approve/reject，且不会重复生成dean approval
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:197:2. Smoke shell脚本中的完整负向场景（前提是Django测试已覆盖负向用例）
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:229:- 如果Django测试已覆盖正向路径，smoke只保留最薄的端到端脚本
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:102:| 宿舍清退API集成 | 1-2周 | API契约明确、字段覆盖、认证跑通 |
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:14:这里的“立即启动”应定义为：用户授权执行者后，立刻进入 Day 2 计时；前 10-15 分钟只做启动门禁和基线记录，不重新讨论方案。
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:18:Claude 的选项 B 基本正确，但应把“最后确认”改名为 **Day 2 T0启动门禁**，并计入 Day 2 时间盒，避免它变成新讨论阶段。
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:22:用户授权后可以启动 Day 2。T0门禁最多 15 分钟；通过则继续执行文档12；失败则只允许判断“快速修复/降级/No-Go候选”，不能开新方案评审。
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:48:2. **计时规则：** T0门禁是否计入 6 小时硬封顶。建议计入。
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:55:1. **测试文件具体命名。** 可以新建 `test_permissions.py` / `test_state_machine.py`，也可以扩展现有测试文件，关键是覆盖点和可重复运行。
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:96:- 授权内容只需回答：“是否授权 Claude 执行 Day 2，并接受 T0门禁计入6小时”。
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:108:> 授权 Claude 执行 Day 2。现在进入 Day 2 T0启动门禁，T0计入6小时硬封顶。15分钟内完成基线记录和环境/测试/seed/migration检查；通过则按文档12继续，失败则按文档12判定快速修复、降级或No-Go候选。不再新增方案讨论。
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:96:- 微信小程序（覆盖主要用户群）
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:38:### 5. URL路由
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:79:### Step 3: 重构/api/applications/路由 (60min)
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:158:- ✓ Smoke test覆盖负向场景
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:124:- 是否需要更多测试数据覆盖边界情况？
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:102:3. 添加 URL 路由
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:108:3. 添加 URL 路由
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:142:### R2: 测试覆盖不足
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:117:优先微信小程序或一个Web/RN壳，不要默认双端完整交付。生产就绪不现实，尤其原计划还要求80%覆盖率、P95、1000并发。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:13:**推荐选项组合2：扩展User模型 + 不允许学工API覆盖name。**
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:17:不推荐组合1，因为允许API覆盖`name`会破坏已达成的CSV主导边界，并引入CSV重新导入与API同步之间的反复覆盖问题。不推荐组合3，因为它会让Step 4B没有真实写入目标，最终只能停留在Step 4A的候选报告。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:25:当前`User`模型只包含`user_id/name/role/active/class_id/is_graduating/graduation_year`，mapper输出的`phone/department`无处落库。若选择“不扩展模型”，Step 4B不应改为`name`覆盖或其他轻量写入；应明确标记为跳过，保留Step 4A只读报告，并将后续Step 5命令限定为dry-run/plan命令。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:29:字段覆盖契约已经定义CSV负责`user_id/name/role/class_id/is_graduating/graduation_year`，API负责`phone/email/department`。`name`虽然来自API，但它是核心身份展示字段，且CSV导入当前会更新`name`。允许API覆盖会造成数据源权威性不清晰。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:67:## name覆盖决策
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:100:- 不做`name`覆盖。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:122:2. mapper测试覆盖`email`存在、缺失两个场景。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:123:3. 服务测试覆盖已存在学生更新`phone/email/department`。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:124:4. 服务测试覆盖API缺失补充字段时保持本地原值。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:125:5. 服务测试覆盖幂等：第二次同步`updated_count=0`或等价无变化统计。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:126:6. 服务测试覆盖不创建本地缺失用户。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:127:7. 服务测试覆盖角色冲突不更新。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:128:8. 服务测试覆盖`name/class_id/is_graduating/graduation_year`不被API覆盖。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:145:因此，CSV可持续导入并覆盖核心字段；API只更新补充字段。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:177:4. API不覆盖`name`和毕业业务核心字段。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:180:7. Step 4B测试以“真实写入 + 幂等 + 不覆盖核心字段”为验收核心。
./docs/discussions/phase4c-next-steps/94-post-step3-next-priority-request.md:83:   - 测试覆盖是否充分？
./docs/discussions/phase4c-next-steps/94-post-step3-next-priority-request.md:100:- mapper已完整实现且测试覆盖充分
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:15:2. ✗ URL路由实现有坑（/api/applications/已绑定POST）
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:44:### 错误5: URL路由方案不可行
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:45:**原提案:** 直接添加GET路由到/api/applications/  
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:187:### Step 3: 重构/api/applications/路由 (45min)
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:242:- 合并GET/POST路由
docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:12:> "授权 Claude 执行 Day 2。现在进入 Day 2 T0启动门禁..."
docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:26:- 授权内容："是否授权 Claude 执行 Day 2，并接受 T0门禁计入6小时"
docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:66:- 立即进入Day 2 T0门禁
docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:69:### 问题3：如果启动，是否需要再次确认T0门禁规则？
docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:71:文档14定义的T0门禁：
docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:141:   - 是否应该立即启动Day 2 T0门禁？
./docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:55:- AttachmentType是否覆盖所有业务场景？
./docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:86:- res.data解析逻辑是否覆盖所有边界情况？
./docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:206:2. **类型安全：** TypeScript类型是否完全覆盖？
./docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:207:3. **错误边界：** 是否覆盖所有可能的错误场景？（网络错误、401、403、404、500、文件过大、文件类型不支持）
docs/discussions/week3-day1-review-2026-05-30/16-codex-authorization-ruling.md:20:- 必须确认"T0门禁是否计入6小时硬封顶"
docs/discussions/week3-day1-review-2026-05-30/16-codex-authorization-ruling.md:49:> 请明确确认：是否授权 Claude 执行 Day 2，并接受 T0启动门禁计入6小时硬封顶？  
docs/discussions/week3-day1-review-2026-05-30/16-codex-authorization-ruling.md:50:> 回复"授权"即立即进入 T0门禁；回复"不授权"则停止 Day 2 执行，改为只整理 runbook/方案。
./docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:52:- 5种通知类型全覆盖（APPLICATION_SUBMITTED、APPROVAL_APPROVED、APPROVAL_REJECTED、DORM_CLEARANCE_BLOCKED、APPROVAL_TIMEOUT_WARNING）
./docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:66:- 测试覆盖：1-2小时
./docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:132:- 补充smoke test覆盖通知API
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:30:1. T0门禁（0:00-0:25，25分钟）
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:41:**问题1：T0门禁可能发现环境不可用**
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:47:**风险：** 如果T0门禁失败，需要快速判断是否No-Go，可能浪费25分钟。
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:79:**优化1：T0门禁前置准备**
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:81:- 优势：可重复，覆盖全面
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:348:- ✓ Smoke test覆盖负向场景
./docs/discussions/phase4c-next-steps/23-codex-post-execution-next-steps-response.md:66:3. **演示脚本**：覆盖 seed/import、登录、申请提交、附件、审批、错误处理、权限验证。
./docs/discussions/phase4c-next-steps/23-codex-post-execution-next-steps-response.md:141:脚本应覆盖：
./docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md:29:4. **路由写法正确**
./docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md:30:   - `urls.py` 使用 `from . import views` 时，新增路由必须写为 `views.list_approvals`。
./docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md:40:- 执行验证时建议同时覆盖 `?limit=5&offset=0` 和 `?limit=5&offset=5`，避免只证明第一页可用。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:14:本轮P1修复已经落地：`would_update_count`被明确约束为"现有学生同步候选数"，不再暗示当前模型已有可持久化更新字段；warning文本也明确指出API补充字段暂不能落库。新增测试使用Django `TestCase`和真实测试数据库，覆盖doc 99要求的8个关键场景。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:35:- 阻塞解除条件：增加`phone/email/department`或批准`name`覆盖策略
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:51:## 测试覆盖审查
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:58:- `setUp`创建1个学生和1个辅导员，足够覆盖existing、conflict、readonly主路径
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:63:1. `test_mapper_skip_transparency`：覆盖skip透传和`skipped_by_reason`统计，通过。修正为断言实际mapper输出`missing_user_id`、`missing_name`是合理的。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:64:2. `test_existing_student_to_candidate`：覆盖`existing_count=1`、`would_update_count=1`候选数语义，通过。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:65:3. `test_missing_local_not_created`：覆盖`missing_local_count`、不创建用户、`would_create_but_blocked` warning，通过。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:66:4. `test_local_role_conflict`：覆盖`user_id/reason/local_role/api_role`结构，通过。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:67:5. `test_core_fields_readonly`：覆盖`class_id/is_graduating/graduation_year/name`不变，通过。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:68:6. `test_field_gap_warning_with_candidates`：覆盖强化warning关键文本，通过。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:69:7. `test_empty_input`：覆盖空输入全零计数和空列表，通过。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:70:8. `test_mixed_scenario`：覆盖skip、missing、conflict、existing分类关系和多个skip reason，通过。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:72:**结论：测试覆盖完整，满足Step 4A验收。**
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:84:完整。当前断言覆盖不创建、计数和`would_create_but_blocked`。服务warning已包含`class_id/is_graduating/graduation_year`，如需更强锁定可增加断言，但现有测试已经足够支撑Step 4A。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:142:Step 4B前置建议：优先决策User模型是否新增`phone/email/department`，以及`name`是否允许由学工API覆盖；在该决策完成前，不应把Step 4A的`would_update_count`解释为真实可写更新数。
./docs/discussions/phase4c-next-steps/53-codex-confirmation-option-a-corrected.md:38:- Schema必须匹配当前API行为，除非同时提交有测试覆盖的行为变更。
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:84:### 错误4: URL路由导入问题
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:206:### 4.3 更新URL路由
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:239:3. **更新路由** (5min)
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:257:4. ✓ URL路由使用 `views.list_approvals`
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:271:- URL路由使用 `views.` 前缀
./docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:57:- Live probe后输出字段覆盖报告
./docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:150:- Live调用门禁
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:75:5. Smoke test骨架（1小时）- 只覆盖正向路径
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:275:- smoke test覆盖三个负向场景
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:167:3. 前端mock server或mock JSON可用，覆盖登录、提交、审批、查询、错误态。
./backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:37:- 项目设计为JSON-only API（base.py:116只启用JSONParser）
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:173:文档12说"优先覆盖跨辅导员403、重复审批409、重复提交409"，但没有说具体测试文件和测试方法。
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:19:5. ✅ **遗漏识别有效**：字段覆盖表必须包含"内部写库字段+缺失字段策略"，不只是API字段清单
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:101:# 学工系统用户API字段覆盖报告
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:124:| User.class_id | 未确认 | 缺失 | 继续由CSV/手工维护，API不覆盖 |
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:125:| User.is_graduating | 未确认 | 缺失 | 继续由CSV/手工维护，API不覆盖 |
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:126:| User.graduation_year | 未确认 | 缺失 | 继续由CSV/手工维护，API不覆盖 |
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:132:[在字段未完全覆盖前，API只能补充或更新可确定字段，不能替代CSV导入]
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:236:5. ✅ API/CSV并存策略：字段未完全覆盖前，API不能替代CSV
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:14:Phase 2A稳定化的前置门禁已经成立：我验证了通知服务层和API层两个测试模块，12/12通过。下一步继续推进smoke增强、OpenAPI基线和部署文档补漏是合理的。
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:54:### P1：Smoke前置条件不能只是注释，必须成为执行门禁
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:70:1. **保守方案：文档门禁**  
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:128:API测试已覆盖提交、审批通过、审批驳回和负向路径，足以支撑进入Option E-lite。但API层对`entity_id`的精确断言还不完整，当前主要断言了`type`、`entity_type`和message内容。
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:130:这不是阻塞项，因为服务层测试已覆盖`entity_id=approval.pk`，但若下一步smoke要验证`entity_id`，最好同步补1-2个API测试断言，避免脚本和API语义漂移。
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:179:> 下一步执行Option E-lite。先处理smoke可重复运行门禁，再增强通知字段和审批驳回路径；随后引入drf-spectacular作为OpenAPI基线，只验收schema可访问、端点清单和认证可见，并记录待完善项；最后补部署文档的环境变量表、smoke前置条件和故障排查。不要在本轮承诺完整API schema，也不要无条件自动重置数据库。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:26:| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:77:并发测试不能只用普通`TestCase`。SQLite下`select_for_update()`基本不能证明锁语义，应至少用`TransactionTestCase`覆盖重复请求返回409；真正并发正确性最好在Docker/Postgres环境跑集成测试。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:104:- `BASE_URL`默认`http://localhost:8001`，可通过环境变量覆盖。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:158:- 核心Django测试通过，至少覆盖申请、审批、驳回、权限、重复提交。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:160:- smoke test覆盖至少三个负向场景：跨辅导员403、重复审批409、重复提交409。
./docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:122:### AttachmentType是否覆盖所有业务场景？
./docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:124:覆盖当前MVP。四类与后端 `AttachmentType` 一致。不要在Phase 2扩展类型，除非业务明确要求新证明材料。
./docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:164:- `.btn-upload` 使用主按钮样式，宽度100%，放在列表/空状态之后。
./docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:167:响应式方面，rpx已经覆盖大部分机型，但长文件名和窄屏按钮组必须处理。核心不是复杂媒体查询，而是 `min-width:0`、`flex-wrap`、固定按钮尺寸和文本溢出策略。
./docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:11:**一致决策：采用选项组合2（扩展User模型+不允许API覆盖name），立即执行Step 4B实现。**
./docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:44:- 核心字段不覆盖
./docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:70:2. ✅ mapper测试覆盖email
./docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:71:3. ✅ 服务测试覆盖更新补充字段
./docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:72:4. ✅ 服务测试覆盖API缺失保持本地值
./docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:73:5. ✅ 服务测试覆盖幂等
./docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:74:6. ✅ 服务测试覆盖不创建用户
./docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:75:7. ✅ 服务测试覆盖角色冲突
./docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:76:8. ✅ 服务测试覆盖核心字段不覆盖
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:80:- smoke test 中的负向场景脚本化，如果 Django 自动化测试已经覆盖负向用例。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:91:提案方向与 Day 2 共识一致，任务拆分也覆盖了主要漏洞。但执行策略低估了测试和数据可复现成本，"手工验证为主"和"允许跳过阻塞项"会削弱 Conditional Go 的可信度。若加入前置校验、最低自动化测试和不可跳过边界，评分可提升到 7.5/10。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:121:- 阶段2：assigned approver 权限覆盖 approve/reject；`get_application` 不再让任意 counselor/dean 查看所有申请。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:122:- 阶段3：审批状态机保护覆盖 approve/reject，且不会重复生成 dean approval。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:129:- smoke shell 脚本中的完整负向场景，前提是 Django 测试已覆盖负向用例。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:140:3. **状态机保护：** 必须覆盖 approve 和 reject。只校验重复审批不够，还要校验 step/status 匹配，例如 dean approval 不能在 `pending_counselor` 状态下被操作。
./docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md:116:- 提升测试覆盖率
./docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md:219:5. **是否违反了之前的共识？** 硬停止共识是否应该被用户的新指令覆盖？
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:31:3. ✓ 添加schema和Swagger UI路由
./docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:38:**缺点:** 可能过度工程，测试覆盖可能不必要
./docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:52:**缺点:** 测试覆盖不足，可能遗漏边界情况
./docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:94:1. **测试覆盖范围:** 是否需要完整测试矩阵（所有角色×所有操作），还是核心场景足够？
./docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:112:- 测试覆盖是否充分但不过度
./docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md:49:> 请明确确认：是否授权 Claude 执行 Day 2，并接受 T0 启动门禁计入 6 小时硬封顶？  
./docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md:50:> 回复"授权"即进入 T0 门禁；回复"不授权"则停止 Day 2 执行，改为整理 runbook/方案。  
./docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:34:**16号明确：** 授权后"立即进入T0门禁"，T0计入硬封顶。
./docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:108:> 请明确确认：是否授权 Claude 执行 Day 2，并接受 T0启动门禁计入6小时硬封顶？  
./docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:109:> 回复"授权"即立即进入 T0门禁；回复"不授权"则停止 Day 2 执行，改为只整理 runbook/方案。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:153:登录、token解析、application_id/approval_id提取、HTTP状态码判断、reset/cleanup、错误输出，任何一个字段与文档不一致都会吃时间。45分钟能搭骨架，但不一定能形成可信证据。可接受的压缩方式是：如果Django测试已经覆盖正向路径，smoke只保留最薄的端到端脚本。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:206:- 优先覆盖跨辅导员403、重复审批409、重复提交409。
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:131:- Smoke test负向场景脚本化（如果Django测试已覆盖）
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:203:3. **状态机保护** - 接受，必须覆盖approve和reject，校验step/status匹配
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:14:这里的“立即启动”应定义为：用户授权执行者后，立刻进入 Day 2 计时；前 10-15 分钟只做启动门禁和基线记录，不重新讨论方案。
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:18:Claude 的选项 B 基本正确，但应把“最后确认”改名为 **Day 2 T0启动门禁**，并计入 Day 2 时间盒，避免它变成新讨论阶段。
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:22:用户授权后可以启动 Day 2。T0门禁最多 15 分钟；通过则继续执行文档12；失败则只允许判断“快速修复/降级/No-Go候选”，不能开新方案评审。
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:48:2. **计时规则：** T0门禁是否计入 6 小时硬封顶。建议计入。
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:55:1. **测试文件具体命名。** 可以新建 `test_permissions.py` / `test_state_machine.py`，也可以扩展现有测试文件，关键是覆盖点和可重复运行。
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:96:- 授权内容只需回答：“是否授权 Claude 执行 Day 2，并接受 T0门禁计入6小时”。
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:108:> 授权 Claude 执行 Day 2。现在进入 Day 2 T0启动门禁，T0计入6小时硬封顶。15分钟内完成基线记录和环境/测试/seed/migration检查；通过则按文档12继续，失败则按文档12判定快速修复、降级或No-Go候选。不再新增方案讨论。
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:124:- 是否需要更多测试数据覆盖边界情况？
./docs/discussions/week3-day1-review-2026-05-30/16-codex-authorization-ruling.md:20:- 必须确认"T0门禁是否计入6小时硬封顶"
./docs/discussions/week3-day1-review-2026-05-30/16-codex-authorization-ruling.md:49:> 请明确确认：是否授权 Claude 执行 Day 2，并接受 T0启动门禁计入6小时硬封顶？  
./docs/discussions/week3-day1-review-2026-05-30/16-codex-authorization-ruling.md:50:> 回复"授权"即立即进入 T0门禁；回复"不授权"则停止 Day 2 执行，改为只整理 runbook/方案。
./docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:30:1. T0门禁（0:00-0:25，25分钟）
./docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:41:**问题1：T0门禁可能发现环境不可用**
./docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:47:**风险：** 如果T0门禁失败，需要快速判断是否No-Go，可能浪费25分钟。
./docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:79:**优化1：T0门禁前置准备**
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:81:- 优势：可重复，覆盖全面
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:348:- ✓ Smoke test覆盖负向场景
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:75:5. Smoke test骨架（1小时）- 只覆盖正向路径
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:275:- smoke test覆盖三个负向场景
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:126:- 优先覆盖跨辅导员403、重复审批409、重复提交409
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:188:2. Assigned approver权限覆盖approve/reject
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:190:4. 审批状态机保护覆盖approve/reject，且不会重复生成dean approval
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:197:2. Smoke shell脚本中的完整负向场景（前提是Django测试已覆盖负向用例）
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:229:- 如果Django测试已覆盖正向路径，smoke只保留最薄的端到端脚本
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:158:- ✓ Smoke test覆盖负向场景
./docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:12:> "授权 Claude 执行 Day 2。现在进入 Day 2 T0启动门禁..."
./docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:26:- 授权内容："是否授权 Claude 执行 Day 2，并接受 T0门禁计入6小时"
./docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:66:- 立即进入Day 2 T0门禁
./docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:69:### 问题3：如果启动，是否需要再次确认T0门禁规则？
./docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:71:文档14定义的T0门禁：
./docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:141:   - 是否应该立即启动Day 2 T0门禁？
./docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:90:- 增加单元测试/管理命令测试，覆盖成功导入、字段缺失、映射缺失、重复行。
./docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:171:- 导入测试覆盖成功和主要失败路径。
./docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:181:- smoke覆盖核心申请审批链路。
./docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:182:- smoke至少覆盖附件上传、列表、下载、删除之一到多个。
./docs/discussions/phase4c-next-steps/43-claude-post-phase2a-stabilization-next-strategy.md:54:- 添加schema和Swagger UI路由
./docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:13:2. **测试覆盖评估**：评估当前测试充分性
./docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:70:**当前测试覆盖：**
./docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:98:   - Mock测试应覆盖哪些场景？
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:102:| 宿舍清退API集成 | 1-2周 | API契约明确、字段覆盖、认证跑通 |
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:16:1. **先做 Phase 2A稳定化门禁**：修正自动通知实现与契约不一致的问题，补足现有测试缺口。
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:52:先修正服务层使用`NotificationType.APPLICATION_SUBMITTED`等枚举值，而不是裸字符串常量名；同步修正测试断言为枚举值/小写值。这个修复应作为所有文档工作的前置门禁。
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:54:### P1：Phase 2A测试覆盖没有达到前一轮共识验收
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:58:当前自动通知测试覆盖了服务函数的正向创建和幂等，但没有覆盖关键API路径和负向路径：
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:86:1. 本轮：生成可访问的schema和Swagger UI，覆盖端点清单、认证、主要请求/响应对象。
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:113:- 增加审批驳回路径，覆盖`APPROVAL_REJECTED`；
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:119:验收标准改为“覆盖关键端到端风险”，不要固定为“至少20个场景”。
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:165:2. smoke脚本增强，覆盖真实API行为。
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:181:**推荐执行 Option E-lite + Phase 2A稳定化门禁，暂不执行Phase 2B/2C。**
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:183:### Step 0：Phase 2A稳定化门禁（优先，0.5-1小时）
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:200:- 至少覆盖认证、申请、审批、附件、通知端点清单。
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:215:3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:237:**Codex状态：** 建议按“Phase 2A稳定化门禁 + Option E-lite”达成共识后执行。
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:96:- 微信小程序（覆盖主要用户群）
./docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md:74:1. **Track 1硬化：** CSV导入已完成，但可能有边界情况未覆盖
./docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md:117:- 测试覆盖的最小标准是什么？
./docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:117:优先微信小程序或一个Web/RN壳，不要默认双端完整交付。生产就绪不现实，尤其原计划还要求80%覆盖率、P95、1000并发。
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:72:5. **核心字段保护：** 不覆盖class_id/is_graduating/graduation_year
./docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:14:1. 用户新指令覆盖的是"可以继续讨论"，不是自动授权P2功能实现
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:167:3. 前端mock server或mock JSON可用，覆盖登录、提交、审批、查询、错误态。
./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:76:**验证：** Section 6.2现在有8个错误样例，覆盖Section 3定义的全部8个错误码
./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:104:**问题：** 执行计划中"5个HTTP路由" vs "4个API端点"表述不一致
./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:108:**建议：** 统一为"5个HTTP路由（login + 4个业务端点）"或"4个业务API端点"
./docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:87:- 添加测试覆盖详情：upload (5), list (6), download (4), delete (4)
./docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:14:理由很直接：上一轮共识已经把通知契约草案定义为纯文档任务，并明确“完成后硬停止”。`docs/api/notification-contract-v0.1.md` 自身也写明 Phase 1 “需单独授权”。因此，“继续讨论下一步”或再次要求 Claude/Codex 讨论，只能覆盖“可以重新评估”，不能自动覆盖“可以落库、加 API、加测试”。
./docs/discussions/phase4c-next-steps/05-claude-next-steps-strategy-request.md:11:- 19个attachment测试100%通过
./docs/discussions/phase4c-next-steps/05-claude-next-steps-strategy-request.md:21:- ✅ 测试覆盖：48个后端测试 + 19个附件测试
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:76:**验证：** Section 6.2现在有8个错误样例，覆盖Section 3定义的全部8个错误码
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:104:**问题：** 执行计划中"5个HTTP路由" vs "4个API端点"表述不一致
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:108:**建议：** 统一为"5个HTTP路由（login + 4个业务端点）"或"4个业务API端点"
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:14:但有一个必须先澄清并落地的小问题：`would_update_count`现在按"本地存在且role=student"计数。若该字段表示"真实可写更新数"，当前User模型没有`phone/email/department`，`name`是否允许API覆盖也未决，因此真实可更新字段数应为0。若该字段表示"未来可更新候选数"，则字段名有误导性，测试必须明确锁定这个语义。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:24:**问题描述：** 当前实现只要本地用户存在且角色为`student`，就执行`would_update_count += 1`。这符合文档97第4条"已存在学生计入would_update_count"，但与字段覆盖文档的Phase 1事实存在张力：User模型当前没有`phone/email/department`字段，`name`是否允许由API覆盖仍未决。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:65:7. 服务没有写DB，不会覆盖`class_id/is_graduating/graduation_year`。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:77:如果`would_update_count`表示"现有学生同步候选"，当前实现正确。如果表示"当前真实可写更新"，当前实现不准确，因为可安全写入字段未成立：`phone/email/department`不存在，`name`覆盖策略未决。建议在Step 4A把它定义为候选数，并用warning明确真实写入仍不可执行。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:89:有必要保留，但应调整断言目标。Step 4A只读，不需要测试"写入后未覆盖"；应该测试：
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:92:- summary不暴露任何会覆盖这些核心字段的计划项；
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:95:## 测试覆盖建议
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:97:文档97列出的8个场景覆盖了关键路径，可以执行，但建议对其中两个场景做精确定义：
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:100:2. "不覆盖class_id/is_graduating/graduation_year"：断言服务只读后DB原值不变，不要模拟Step 4B写入行为。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:110:2. 创建`backend/apps/users/tests/test_xg_user_sync.py`，使用真实Django测试数据库覆盖8个场景。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:57:3天只适用于"API 契约已冻结、测试环境可用、认证已跑通、字段完全覆盖、只写一个薄适配器"的场景。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:139:100学生、10辅导员可以支撑演示，但不足以覆盖风险。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:217:│  校验必填字段、唯一性、班级覆盖率、辅导员有效性 │
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:243:3. **Import/Sync Service：** 校验必填字段、唯一性、班级覆盖率、辅导员有效性
./docs/操作说明书.md:13:毕业生离校申请审批系统用于管理毕业生离校申请的提交、审批和备案流程。系统采用两级审批模式：宿管员审批 → 辅导员审批，学工部进行备案查询。
./docs/操作说明书.md:20:| 宿管员 (dorm_manager) | 第一级审批 | 审批宿舍清退相关事项 |
./docs/操作说明书.md:29:宿管员审批（通过/驳回）
./docs/操作说明书.md:152:   - **待宿管员审批**：等待宿管员处理
./docs/操作说明书.md:153:   - **待辅导员审批**：宿管员已通过，等待辅导员处理
./docs/操作说明书.md:162:4. 审批流程从第一级（宿管员）重新开始
./docs/操作说明书.md:164:### 3.2 宿管员操作
./docs/操作说明书.md:168:⚠️ **注意：** 当前版本宿管员功能尚未完全实现：
./docs/操作说明书.md:169:- 种子数据未包含宿管员测试账号
./docs/操作说明书.md:173:宿管员功能在Demo Web中可正常使用（需先配置测试账号）
./docs/操作说明书.md:219:操作步骤与宿管员相同：
./docs/操作说明书.md:220:1. 查看待审批列表（仅显示宿管员已通过的申请）
./docs/操作说明书.md:222:3. 查看审批记录（可见宿管员的审批意见）
./docs/操作说明书.md:250:   - 完整审批记录（宿管员 + 辅导员）
./docs/操作说明书.md:278:A: 您所在班级尚未配置审批流程（辅导员或宿管员信息缺失）。请联系系统管理员配置班级映射关系。
./docs/操作说明书.md:324:**注意：** 运行 `python manage.py seed_data` 后可用上述账号。当前版本宿管员账号和映射尚未在种子数据中实现。
./docs/操作说明书.md:329:2. 切换宿管员账号审批通过
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:23:**问题：** 契约列出6个HTTP路由，计划说"5个核心API端点"（Week 0 Day 1）和"4个API端点"（Week 1 Day 3-4），口径不一致。
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:27:- 统一为5个HTTP路由：
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:103:- [ ] 5个HTTP路由是否足以支撑最小纵向切片？
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:106:- [ ] 503样例是否覆盖了PROVIDER_UNAVAILABLE场景？
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:107:- [ ] 错误样例是否覆盖了所有Section 3定义的错误码？
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:67:### 3. 测试覆盖策略
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:75:5. 不覆盖class_id/is_graduating/graduation_year
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:81:- 这8个场景是否覆盖所有关键路径
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:134:- name（但CSV主导，是否允许API覆盖未决）
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:162:文档97要求测试"不覆盖class_id/is_graduating/graduation_year"。
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:179:2. **测试覆盖是否充分**
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:95:1. `week-0-1-execution-plan.md` 仍有“4个API端点可用”的表述，和契约“5个HTTP路由”容易产生术语混淆。建议后续改为“4个业务HTTP路由可用，不含Day 1-2登录路由”，或在Week 1验收处统一写“5个HTTP路由覆盖4个核心能力”。
./docs/discussions/phase4c-next-steps/58-claude-codex-consensus-option-a-prime-partial.md:12:**执行Option A-prime：主动关闭API Schema P1验收门禁。**
./docs/数据确认清单.md:13:**问题1：** 宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？
./docs/数据确认清单.md:62:**问题11：** CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
./docs/数据确认清单.md:116:1. 向宿管系统提交本确认清单
./docs/数据确认清单.md:154:1. 对接宿管系统宿舍清退API
./docs/数据确认清单.md:225:| 宿管系统无法提供完整数据 | 高 | 提前确认数据可用性，必要时调整对接范围 |
./docs/数据确认清单.md:237:**宿管系统联系人：** [待填写]  
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:47:- 首版：微信小程序（覆盖主要用户群）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:60:100学生/10辅导员只够演示，不够测试。需要fixture matrix覆盖：
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:25:- 问题：User模型无phone/email/department，name覆盖未决
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:182:## 测试覆盖补充
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:37:### 问题2：name字段是否允许API覆盖？
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:44:**如果允许覆盖：**
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:48:**如果不允许覆盖：**
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:56:### 选项组合1：扩展模型 + 允许name覆盖
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:65:- name覆盖可能与CSV冲突
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:69:### 选项组合2：扩展模型 + 不允许name覆盖
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:115:### name字段覆盖价值
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:124:**风险：** CSV重新导入可能覆盖API更新
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:155:**name覆盖策略选项：**
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:158:- API更新name → 覆盖
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:159:- CSV重新导入 → 覆盖
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:194:### 审查要点3：name覆盖策略
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:223:**影响：** name覆盖策略和字段主导权
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:259:3. **name覆盖决策**
./docs/discussions/completion-review-2026-06-03/02-claude-response.md:15:- 后端/Docker/测试环境：98-100% ✓
./docs/discussions/phase4c-next-steps/71-claude-response-accept-b-mini.md:85:**测试覆盖：**
./docs/discussions/phase4c-next-steps/84-post-step1-next-strategy-request.md:32:  - Live probe硬门禁（XG_RUN_LIVE_API_TEST=1）
./docs/discussions/phase4c-next-steps/84-post-step1-next-strategy-request.md:81:- Mock测试覆盖
./docs/discussions/phase4c-next-steps/84-post-step1-next-strategy-request.md:110:- 例如：前端优化、测试覆盖提升、文档完善
./docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:167:**测试覆盖：**
./docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:237:   - 401/403/404 处理是否覆盖所有关键场景？
./docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:246:5. **后端测试覆盖充分性**
./docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:247:   - 6个测试是否覆盖了P1修复的所有场景？
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:19:1. **P1-1：错误样例覆盖不完整** - Section 3定义8个错误码，Section 6.2只有4个样例
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:38:**验证点：** Section 6.2现在有8个错误样例，覆盖Section 3全部8个错误码
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:62:- [ ] 错误样例是否完整覆盖8个错误码？
./docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:14:Phase 4C 证据闭环已经完成，之前的「完成证据包后硬停止」共识仍然正确。用户的新指令可以覆盖硬停止，但覆盖的是「可以继续讨论/重新决策」，不是自动授权进入新的 P2 功能实现。
./docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:118:之前共识是「证据闭环后硬停止，等待 DevTools、用户授权或外部系统信息」。用户的新要求如果只是「继续讨论」，它触发的是重新评估。只有当用户明确选择 Track 3 或授权继续内部开发时，才构成对硬停止的覆盖。
./docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:120:即使覆盖硬停止，也不应覆盖以下冻结边界：
./docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:19:   - 只记录脱敏摘要和字段覆盖。
./docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:25:   - 用 mock 测试覆盖多页、空页、最后页、业务错误、schema 异常。
./docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:27:3. **Step 2C：字段覆盖/映射决策。**
./docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:47:但它不应该成为分页实现的硬阻塞。当前 `diagnose_xg_api.py` 已经具备硬门禁，继续保持：
./docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:116:- Step 2B：实现 `fetch_all_users()`，mock 测试覆盖分页边界。
./docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:117:- Step 2C：整理字段覆盖清单，判断能否支撑用户同步。
./docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:123:- live 成功时有脱敏字段覆盖报告；live 失败时有明确错误分类和外部问题清单。
./docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:184:4. **字段覆盖不足以替代 CSV。**
./docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:186:   - 缓解：Step 3 前不得接 Provider 落库；先做字段覆盖报告和缺口表。
./docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:198:   - 缓解：继续强制脱敏；禁止保存原始响应；字段覆盖只记录布尔值和掩码样本。
./docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:200:**最终建议：立即执行 Step 2A 条件式 live probe，同时推进 Step 2B 分页读取。Step 2B 完成后，不要直接落库；先用 live 字段覆盖或平台字段说明完成 Step 3 的字段映射决策。**
./docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.md:126:4. **Mock测试**：全场景覆盖
./docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.md:166:   - 硬门禁：`XG_RUN_LIVE_API_TEST=1` 且配置齐全
./docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:53:- Live后输出覆盖报告
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:15:理由是 Option E-lite 的边界已经在 46 号共识文档中明确：Smoke 增强、OpenAPI 基线、部署文档补漏。Step 1/Step 2 已经覆盖主要工程风险，继续扩展 API schema P1 项会把本轮从“基线交付”扩大成“文档精修”，不适合混入 Option E-lite 收尾。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:28:- smoke 覆盖 H1 happy path、H2 counselor reject、N2 cross-counselor 403。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:30:- notification 断言覆盖 `type`、`entity_type`、`message`。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:50:- `docs/api/api-schema-todo.md` 中 notification mark-as-read 路径写成 `/api/notifications/mark_as_read/`，实际路由和 schema 是 `/api/notifications/{notification_id}/read/`。Step 3 或收尾时应修正这个清单。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:73:环境变量表应以实际代码读取为准，优先覆盖：
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:95:建议覆盖这些高频场景：
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:13:Codex的分析准确且全面：扩展模型+不覆盖name方案与Phase 1策略一致，migration风险低，字段权威性清晰，实施范围明确。
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:28:### 决策2：name不允许API覆盖
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:34:**Claude确认：** 完全同意。避免CSV重新导入与API同步的反复覆盖冲突，保持数据源权威性清晰。
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:80:- ❌ name覆盖
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:92:2. ✅ mapper测试覆盖email存在/缺失
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:93:3. ✅ 服务测试覆盖更新补充字段
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:94:4. ✅ 服务测试覆盖API缺失时保持本地值
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:95:5. ✅ 服务测试覆盖幂等（第二次sync unchanged）
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:96:6. ✅ 服务测试覆盖不创建missing_local
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:97:7. ✅ 服务测试覆盖role冲突不更新
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:98:8. ✅ 服务测试覆盖核心字段不被API覆盖
./docs/discussions/phase4c-next-steps/72-claude-codex-consensus-phase2b-step2-strategy.md:106:- 覆盖：counselor/dean超时场景
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:14:4个修复方向都正确，且主要阻塞点已经明显收敛：契约正文现在只有5个HTTP路由，列表端点已移除；503 `PROVIDER_UNAVAILABLE`样例已补；登录响应的DTO子集问题已说明；原先“申请未完成却只做查询”的降级方向已被替换。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:18:1. **P1：错误样例未覆盖Section 3定义的全部错误码。**
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:20:3. **P2：计划文档仍混用“5个HTTP路由”和“4个API端点/能力”的口径；AuthUserDTO最好正式纳入Section 1。**
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:32:契约Section 4现在实际列出5个HTTP路由：
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:42:剩余问题是计划文档仍写“4个API端点可用（登录、提交、审批、查询）”。这更像4个核心能力，而不是HTTP路由。建议统一术语：
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:44:- HTTP路由：5个
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:46:- Day 3-4新增HTTP路由：4个，不含Day 1-2已完成的login
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:70:如果v0.1目标是“前端可用mock跑通并处理错误态”，错误样例应至少覆盖Section 3列出的全部错误码。否则前端mock、契约测试和后端异常处理仍会自行发挥。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:112:### P1：错误样例覆盖不完整
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:116:**问题：** Section 3定义8个错误码，但错误Mock只覆盖4个。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:149:**问题：** 计划中“4个API端点”实际指4个核心能力或Day 3-4新增HTTP路由，不等于契约的5个HTTP路由。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:155:- Week 0：5个HTTP路由样例
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:156:- Day 3-4交付物：4个业务HTTP路由可用，不含登录
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:157:- Week 1验收：5个HTTP路由可用，覆盖4个核心能力
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:175:不是因为方向错，而是因为仍有两个会影响执行验收的P1口径缺口：错误样例未全覆盖，降级风险表仍有冲突措辞。它们都属于半天内可以修完的收尾问题。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:187:3. 将计划中的“4个API端点”改成“4个核心能力”或“4个业务HTTP路由”，避免和5个HTTP路由冲突。
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:13:Codex与Claude完全同意：P1修复已落地，测试覆盖完整，8/8通过验收。
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:30:### 2. 测试覆盖验收通过
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:34:**场景覆盖（全部通过）：**
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:44:**Codex评估：** 测试策略正确（Django TestCase + 真实DB），覆盖完整。
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:99:**问题2：name字段是否允许API覆盖？**
./docs/design/2026-05-27-system-design.md:2553:- 覆盖率目标：80%+
./docs/discussions/phase4c-next-steps/83-consensus-step1b-lite-first.md:73:- Live probe硬门禁（XG_RUN_LIVE_API_TEST=1+单页）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:87:        # 3. 校验（必填字段、唯一性、班级覆盖率）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:241:- **学生：** 100人（覆盖5个院系、10个班级）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:244:- **宿舍清退状态：** 覆盖所有枚举值（completed/pending/not_started/unknown）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:338:- [ ] 错误处理覆盖所有场景
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:57:3天只适用于"API 契约已冻结、测试环境可用、认证已跑通、字段完全覆盖、只写一个薄适配器"的场景。
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:139:100学生、10辅导员可以支撑演示，但不足以覆盖风险。
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:217:│  校验必填字段、唯一性、班级覆盖率、辅导员有效性 │
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:243:3. **Import/Sync Service：** 校验必填字段、唯一性、班级覆盖率、辅导员有效性
./docs/discussions/completion-review-2026-06-03/01-codex-final-assessment.md:14:| 后端/API/数据库/Docker/Smoke演示环境 | 98-100% | 已完成 |
./docs/discussions/completion-review-2026-06-03/01-codex-final-assessment.md:26:当前状态覆盖：
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:87:### Step 1.0: Smoke可重复运行门禁（1-1.5小时）
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:125:- 添加schema和Swagger UI路由
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:162:2. smoke覆盖审批驳回路径
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:184:> 下一步执行Option E-lite。先实现smoke可重复运行门禁（SMOKE_RESET=1），再增强通知字段和审批驳回路径；随后引入drf-spectacular作为OpenAPI基线，只验收schema可访问、端点清单和认证可见，并记录待完善项；最后补部署文档的环境变量表、smoke前置条件和故障排查。不承诺完整API schema，不无条件自动重置数据库。
./docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:14:2. 错误处理覆盖所有关键路径
./docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:249:   - 是否需要额外的测试覆盖
./docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:274:2. 错误处理覆盖所有关键路径
./docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:12:**完全接受Codex的Phase 2A稳定化门禁 + Option E-lite建议。**
./docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:25:### 1. Phase 2A稳定化门禁优先
./docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:58:1. Phase 2A稳定化门禁（0.5-1小时）
./docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:76:### Step 0: Phase 2A稳定化门禁（0.5-1小时）
./docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:119:- 添加schema和Swagger UI路由
./docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:153:4. 权限拒绝、状态冲突、宿舍阻断不创建通知（测试覆盖）
./docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:158:2. 覆盖审批驳回路径
./docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:181:- "至少20个smoke场景"数字目标 - 改为"覆盖关键风险"
./docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:187:根据用户的"继续讨论+直接执行"指令和Codex的Phase 2A稳定化建议，现在启动Phase 2A稳定化门禁实施，无需额外用户授权。
./docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:195:**Claude状态：** 立即启动Phase 2A稳定化门禁实施
./docs/discussions/phase4c-next-steps/87-step2b-implementation-review-request.md:87:### 3. 测试覆盖
./docs/discussions/phase4c-next-steps/87-step2b-implementation-review-request.md:148:4. **测试覆盖充分性**
./docs/discussions/phase4c-next-steps/87-step2b-implementation-review-request.md:149:   - 8个测试是否覆盖所有边界条件？
./docs/discussions/phase4c-next-steps/87-step2b-implementation-review-request.md:172:## 4. 测试覆盖审查
./docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:23:**问题：** 契约列出6个HTTP路由，计划说"5个核心API端点"（Week 0 Day 1）和"4个API端点"（Week 1 Day 3-4），口径不一致。
./docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:27:- 统一为5个HTTP路由：
./docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:103:- [ ] 5个HTTP路由是否足以支撑最小纵向切片？
./docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:106:- [ ] 503样例是否覆盖了PROVIDER_UNAVAILABLE场景？
./docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:107:- [ ] 错误样例是否覆盖了所有Section 3定义的错误码？
./docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:95:1. `week-0-1-execution-plan.md` 仍有“4个API端点可用”的表述，和契约“5个HTTP路由”容易产生术语混淆。建议后续改为“4个业务HTTP路由可用，不含Day 1-2登录路由”，或在Week 1验收处统一写“5个HTTP路由覆盖4个核心能力”。
./docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:30:- ✅ 验证通过：契约修改完整、实体修正合理、测试覆盖完整、无其他引用
./docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:103:- ✅ test_auto_notifications_api.py：3个断言覆盖核心语义
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:47:- 首版：微信小程序（覆盖主要用户群）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:60:100学生/10辅导员只够演示，不够测试。需要fixture matrix覆盖：
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:21:- 8个测试场景（覆盖skip/existing/missing/conflict/readonly/warning/empty/mixed）
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:97:### 测试覆盖对比Codex建议
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:143:- 8个测试场景是否覆盖所有关键路径
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:151:**3. 测试覆盖充分性**
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:167:   - 测试覆盖是否充分
./docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:19:1. **P1-1：错误样例覆盖不完整** - Section 3定义8个错误码，Section 6.2只有4个样例
./docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:38:**验证点：** Section 6.2现在有8个错误样例，覆盖Section 3全部8个错误码
./docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:62:- [ ] 错误样例是否完整覆盖8个错误码？
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:14:4个修复方向都正确，且主要阻塞点已经明显收敛：契约正文现在只有5个HTTP路由，列表端点已移除；503 `PROVIDER_UNAVAILABLE`样例已补；登录响应的DTO子集问题已说明；原先“申请未完成却只做查询”的降级方向已被替换。
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:18:1. **P1：错误样例未覆盖Section 3定义的全部错误码。**
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:20:3. **P2：计划文档仍混用“5个HTTP路由”和“4个API端点/能力”的口径；AuthUserDTO最好正式纳入Section 1。**
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:32:契约Section 4现在实际列出5个HTTP路由：
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:42:剩余问题是计划文档仍写“4个API端点可用（登录、提交、审批、查询）”。这更像4个核心能力，而不是HTTP路由。建议统一术语：
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:44:- HTTP路由：5个
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:46:- Day 3-4新增HTTP路由：4个，不含Day 1-2已完成的login
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:70:如果v0.1目标是“前端可用mock跑通并处理错误态”，错误样例应至少覆盖Section 3列出的全部错误码。否则前端mock、契约测试和后端异常处理仍会自行发挥。
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:112:### P1：错误样例覆盖不完整
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:116:**问题：** Section 3定义8个错误码，但错误Mock只覆盖4个。
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:149:**问题：** 计划中“4个API端点”实际指4个核心能力或Day 3-4新增HTTP路由，不等于契约的5个HTTP路由。
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:155:- Week 0：5个HTTP路由样例
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:156:- Day 3-4交付物：4个业务HTTP路由可用，不含登录
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:157:- Week 1验收：5个HTTP路由可用，覆盖4个核心能力
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:175:不是因为方向错，而是因为仍有两个会影响执行验收的P1口径缺口：错误样例未全覆盖，降级风险表仍有冲突措辞。它们都属于半天内可以修完的收尾问题。
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:187:3. 将计划中的“4个API端点”改成“4个核心能力”或“4个业务HTTP路由”，避免和5个HTTP路由冲突。
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:158:- 覆盖率目标：核心90%、整体70%
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:250:- 分层覆盖率目标
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:277:| 测试覆盖率不足 | 低 | 渐进式TDD，分层目标 |
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:87:        # 3. 校验（必填字段、唯一性、班级覆盖率）
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:241:- **学生：** 100人（覆盖5个院系、10个班级）
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:244:- **宿舍清退状态：** 覆盖所有枚举值（completed/pending/not_started/unknown）
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:338:- [ ] 错误处理覆盖所有场景
./docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:19:- 统一为5个HTTP路由
./docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:37:- 错误样例现在覆盖：401, 403, 422, 503
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:75:- 测试覆盖良好（applications/approvals/attachments/notifications）
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:234:- 扩展smoke_test.sh覆盖更多场景
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:261:   - 端到端测试覆盖不足（质量保障）
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:290:2. smoke_test.sh覆盖至少20个场景（当前15个）
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:298:4. 测试覆盖通过
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:11:**重要说明：本项目只对接宿管系统，不直接对接教务、人事、学工等其他系统。**
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:16:- **唯一数据源：** 宿管系统
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:17:- **数据获取方式：** 通过宿管系统提供的数据库、API或CSV文件
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:18:- **数据责任方：** 宿管系统负责人
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:20:### 1.2 为什么只对接宿管系统
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:22:1. **项目定位：** 本系统是宿管系统的配套子系统，不是全校级统一离校平台
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:23:2. **数据归集：** 宿管系统已从教务、人事、学工等系统归集了所需数据
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:25:4. **权责清晰：** 数据质量、更新时效由宿管系统统一负责
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:31:- ❌ **不接受：** 将反馈对象从"宿管系统"改为"多方数据负责人"
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:32:- 🔄 **调整：** 待反馈问题需明确"宿管系统能否提供这些数据"
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:40:**Codex意见：** 将"提交给宿管系统方"改为"提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人"。
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:46:基于项目约束（只对接宿管系统），原文档的反馈对象是正确的：
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:47:1. 本系统只对接宿管系统，不直接对接教务、人事、学工
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:48:2. 学生、辅导员、班级映射等数据由宿管系统负责提供
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:49:3. 宿管系统如何获取这些数据（是否从教务/人事归集）是宿管系统的内部实现
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:50:4. 我们的职责是明确需求，由宿管系统确认能否提供
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:54:需要在待反馈问题中明确询问宿管系统：
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:55:- 这些数据是否在宿管系统数据库中？
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:56:- 如果不在，宿管系统能否从其他系统归集后提供？
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:60:- 保持反馈对象为"宿管系统方"
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:61:- 在待反馈问题中增加："宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？如不包含，能否从教务/人事/学工系统归集后提供？"
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:256:**修改方案：** 在文档中明确说明首版只支持一班一主辅导员，并在待反馈问题中询问宿管系统是否存在多辅导员场景。
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:264:**Codex结论：** P0数据源覆盖完整，未遗漏关键数据。
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:286:| `phone` 可选性确认 | ✅ 接受，需要在待反馈问题中询问宿管系统 |
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:298:3. CSV需补充导入覆盖策略、重复数据处理、失败回滚
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:330:- 导入策略：首版采用**全量覆盖**（清空后重新导入）
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:360:- 宿管系统能否只提供当届毕业生数据？
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:369:基于项目约束（只对接宿管系统），我们接受Codex建议的问题方向，但需要调整提问对象和表述。
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:373:将Codex建议的12个问题调整为"向宿管系统确认的问题清单"：
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:376:1. 宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:392:11. CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:422:1. 向宿管系统提交本需求文档
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:431:4. 重点校验：学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:434:1. 对接宿管系统宿舍清退API
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:467:1. 将反馈对象从"宿管系统"改为"多方数据负责人"
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:468:   - 理由：项目只对接宿管系统，不直接对接教务/人事/学工
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:472:2. 待反馈问题：接受问题方向，但调整为"向宿管系统确认"
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:530:3. 提交给宿管系统方反馈
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:531:4. 根据宿管系统反馈调整方案
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:540:1. **项目约束确认：** 我们明确项目只对接宿管系统，不直接对接教务/人事/学工。Codex是否认同这个约束下，原文档的反馈对象（宿管系统方）是正确的？
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:556:- **核心约束：** 项目只对接宿管系统
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:558:- **保持立场：** 反馈对象为宿管系统方
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:126:- 测试覆盖率反而下降
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:142:#### MAJOR - 80%覆盖率目标缺少分层
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:145:测试覆盖率目标80%，但未区分不同类型代码：
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:146:- 业务逻辑代码应该100%覆盖
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:151:**分层覆盖率目标**：
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:245:2. **分层覆盖率目标**（核心90%、API 80%、模型70%）
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:258:3. 分层覆盖率目标
./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:53:1. **术语不一致：** 执行计划"4个API端点" vs 契约"5个HTTP路由"
./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:54:   - 建议：后续统一为"5个HTTP路由（login + 4个业务端点）"
./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:76:- API端点（5个HTTP路由：login + submit + query + approve + reject）
./docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:65:| User.class_id | 未确认 | 缺失 | CSV维护，API不覆盖 |
./docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:66:| User.is_graduating | 未确认 | 缺失 | CSV维护，API不覆盖 |
./docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:67:| User.graduation_year | 未确认 | 缺失 | CSV维护，API不覆盖 |
./docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:74:- 字段未完全覆盖前，API只能补充或更新可确定字段
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:5:**目的：** 提交给宿管系统方，确认数据可用性和实施计划  
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:10:## 一、待宿管系统确认的问题清单
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:14:**问题1：** 宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:63:**问题11：** CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:117:1. 向宿管系统提交本确认清单
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:151:   - 班级映射覆盖率（所有学生的class_id都有对应辅导员）
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:168:1. 对接宿管系统宿舍清退API
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:176:   - 数据过期：提示学生联系宿管
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:281:| 宿管系统无法提供完整数据 | 高 | 提前确认数据可用性，必要时调整对接范围 |
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:293:**宿管系统联系人：** [待填写]  
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:18:1. **Step 2C-lite：字段覆盖与映射契约**
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:42:### 能否在实现Step 3时增量确定字段覆盖？
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:44:可以增量修正字段覆盖，但不应在入库同步命令里首次确定字段覆盖。
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:78:### 缺失字段覆盖文档会导致什么问题？
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:99:1. 创建字段覆盖表，不追求真实字段全集，只覆盖“同步写库必需字段”。
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:112:完成这个文档后，Step 3 的 mapper/provider 可以很快实现，而且测试目标明确。反过来，如果直接写 DB 同步命令，测试会被迫同时覆盖字段猜测、数据转换、幂等 upsert、事务和命令输出，反馈周期会变慢。
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:118:Step 2系列还有一个关键遗漏：**字段覆盖报告不能只列 API 字段，还必须列内部写库字段和缺失字段策略。**
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:127:| `User.class_id` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:128:| `User.is_graduating` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:129:| `User.graduation_year` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:135:   - 在字段未完全覆盖前，API 只能补充或更新可确定字段，不能替代 CSV 导入。
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:173:- 单元测试覆盖字段缺失、角色未知、班级缺失、毕业字段缺失等场景。
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:11:5. ✅ **登录路由矩阵**（新问题3）
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:38:**第2步：注册 + 路由 + smoke（15分钟）**
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:41:login.ts         - 实现角色路由矩阵
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:145:      DORM_BLOCKED: (d) => `宿舍清退未完成：${d?.blocking_reason || '请联系宿管'}`,
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:154:**5. 登录路由矩阵**
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:191:- ✅ 实现登录路由矩阵
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:56:### 审查要点2：测试文件是否覆盖8个关键场景
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:170:2. **测试覆盖是否完整**
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:244:4. 充分的单元测试覆盖
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:309:**问题11：Mock数据测试覆盖度？**
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:147:3. **可能未使用**：部分索引可能查询覆盖不到
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:18:4. ✅ **风险识别全面**：5个关键风险点（无可写字段/创建边界/核心字段覆盖/停用策略/命令膨胀）
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:121:5. 不覆盖class_id/is_graduating/graduation_year
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:111:   学生只能查自己的申请不是边界条件，而是核心安全契约。最小闭环至少要覆盖一条负向权限验证。
./docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:68:- 优点：测试覆盖先就绪，不依赖外部信息
./docs/discussions/phase4c-next-steps/88-step2b-implementation-codex-response.md:29:**共识要求：** doc 85明确要求覆盖"缺失`data.data`、`users`不是list"。
./docs/discussions/phase4c-next-steps/88-step2b-implementation-codex-response.md:71:## 4. 测试覆盖审查
./docs/discussions/phase4c-next-steps/88-step2b-implementation-codex-response.md:73:现有8个新增测试覆盖了正常分页、空页、业务错误、HTTP错误、`max_pages`，但遗漏了几个共识要求：
./docs/discussions/phase4c-next-steps/88-step2b-implementation-codex-response.md:80:5. doc 86要求的`page_size=1`场景未覆盖
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:11:1. ✅ 学生宿舍清退数据（来源：宿管系统）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:64:**数据来源：** 宿管系统
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:245:### 5.1 宿管员信息
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:249:- 宿管员不需要在本系统中登录
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:250:- 不需要宿管员数据
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:261:| 宿舍清退数据 | 宿管系统 | API/CSV | ✅ 已有 |
./docs/discussions/week3-direction-2026-05-30/03-claude-response.md:68:**Codex的P2包括"Docker Compose覆盖必要依赖"，但：**
./docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:45:3. Phase 1 会产生迁移、后端路由和测试资产，性质明显高于 Phase 0 的纯文档工作。
./docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:47:如果用户原话确实包含“直接执行，直到项目完成”，它可以覆盖“停止讨论”的等待状态，但仍建议用一次极短确认把实现范围锁死，避免把外部验收阻塞误读成允许无限扩张 P2 功能。
./docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:86:当前后端使用函数视图和 app-level urls，不是 ViewSet/router 风格。Phase 1 应遵循现有风格，除非先统一路由模式。
./docs/discussions/week3-direction-2026-05-30/02-codex-review.md:41:- Docker Compose覆盖必要依赖（PostgreSQL、Django）
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:24:- 4个Django测试文件覆盖当前7个失败点
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:18:2. 字段gap warning已强化，包含候选数量、`sync candidates exist`、`no API supplemental fields can be persisted`、`phone/email/department`以及name覆盖策略未批准的阻塞说明。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:21:**测试文件覆盖了8个关键场景，并使用Django `TestCase` + 真实测试数据库。**
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:67:测试名/注释写"skip/missing/conflict/existing各1个"，实际数据有2个skip。这是合理的，因为同一测试还要验证多个skip reason；但建议把注释改为"覆盖skip/missing/conflict/existing，skip包含两个reason"。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:98:## 测试覆盖审查
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:102:1. `test_mapper_skip_transparency`：覆盖mapper skip、`skipped_count`、`skipped_by_reason`。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:103:2. `test_existing_student_to_candidate`：覆盖`existing_count=1`、`would_update_count=1`候选数语义。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:104:3. `test_missing_local_not_created`：覆盖`missing_local_count=1`、不创建用户、`would_create_but_blocked` warning。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:105:4. `test_local_role_conflict`：覆盖`user_id/reason/local_role/api_role`冲突结构。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:106:5. `test_core_fields_readonly`：覆盖服务执行后`class_id/is_graduating/graduation_year/name`不变。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:107:6. `test_field_gap_warning_with_candidates`：覆盖强化warning关键文本。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:108:7. `test_empty_input`：覆盖空输入计数和列表为空。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:109:8. `test_mixed_scenario`：覆盖skip、missing、conflict、existing并验证分区计数关系。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:115:- `setUp()`创建1个学生和1个辅导员，足够覆盖当前8个场景。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:203:4. 进入Step 4B前置讨论：User模型扩展与name覆盖策略。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:28:当前 `map_xg_user_to_internal()` 输出 `phone` 和 `department`，字段覆盖契约也把 `phone`、`email`、`department`定义为 API 补充字段。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:42:这意味着如果 Step 4 现在直接做“幂等 upsert 并写库”，实际可安全写入的 API 字段非常有限。`class_id`、`is_graduating`、`graduation_year`按共识不由 API 覆盖；`role`仅用于过滤学生；`user_id`是主键；剩下只有 `name` 可能可更新，但它属于 CSV 主导核心字段，不应在没有明确策略时被 API 静默覆盖。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:60:- 本地存在但核心字段缺失：不覆盖核心字段，计入冲突或跳过
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:137:- 不覆盖 `class_id`、`is_graduating`、`graduation_year`
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:182:3. **核心字段覆盖策略**
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:183:   - `name`、`class_id`、毕业字段由 CSV 主导，API 覆盖必须有明确规则。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:200:测试覆盖对只读 mapper 足够；对 Step 4 还缺服务级测试，尤其是本地存在性、角色冲突、不可创建、不可覆盖核心字段、summary 结构稳定性。
./docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:18:> 下一步执行Option E-lite。先实现smoke可重复运行门禁（SMOKE_RESET=1），再增强通知字段和审批驳回路径；随后引入drf-spectacular作为OpenAPI基线，只验收schema可访问、端点清单和认证可见，并记录待完善项；最后补部署文档的环境变量表、smoke前置条件和故障排查。不承诺完整API schema，不无条件自动重置数据库。
./docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:24:1. **Smoke前置条件必须成为执行门禁**
./docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:38:### Step 1.0: Smoke可重复运行门禁（1-1.5小时）
./docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:68:2. smoke覆盖审批驳回路径
./docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:90:**下一步：** 立即启动Step 1.0（Smoke可重复运行门禁）
./docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:18:- 官方样例测试覆盖了显式 `sha1` 和默认 `sha1`。
./docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:87:- live probe 硬门禁：`XG_RUN_LIVE_API_TEST=1`，配置齐全，固定 `page=1/pageNum=1`。
./docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:117:字段覆盖: name=yes number=yes phone=yes department=yes user_identity=yes
./docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:78:- 单元测试覆盖官方签名样例、md5、非法 `encryptionType`、缺失必填环境变量。
./docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:111:live probe 成功后，应输出“字段覆盖报告”，再决定是否接入 Provider。没有班级/辅导员/宿舍字段前，不应把该接口宣称为完整业务数据源。
./docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:234:- 产出脱敏字段覆盖报告。
./docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:235:- 根据字段覆盖再开“是否接入 Provider”的新决策门。
./docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:270:5. live probe 只产出字段覆盖报告，不直接触发 Provider 接入。
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:5:**目的：** 明确毕业离校系统所需的数据源，提交给宿管系统方反馈
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:22:- **DB优先**：直接读取宿管系统数据库（推荐，支持MySQL/SQL Server/Oracle）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:23:- **API备选**：调用宿管系统提供的API接口
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:63:-- 示例查询（假设宿管系统有学生表）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:105:| 宿舍楼栋 | dorm_building | 文本 | 否 | 宿舍楼栋名称 | 1号楼 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:166:-- 示例查询（假设宿管系统有辅导员表）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:201:- 上线前必须达到100%覆盖率
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:248:- 上线前必须达到100%当届学生可解析到有效辅导员
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:290:- 网络连通性：本系统服务器能访问宿管系统数据库
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:353:1. 宿管系统方按模板导出CSV文件
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:394:**如果宿管系统数据库包含所有数据：**
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:399:**如果宿管系统数据库只包含部分数据：**
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:411:4. 班级-辅导员对应关系：CSV导入（必须100%覆盖）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:418:请宿管系统方反馈以下问题：
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:421:1. 宿管系统使用的数据库类型？（MySQL / SQL Server / Oracle / PostgreSQL / 其他）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:448:1. **宿管系统方**：反馈上述问题，提供数据库/API/CSV的可行性
./docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:19:我的55号提案存在判断失误：将"代码修改完成"误认为"P1完成"，忽略了验证门禁的重要性。
./docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:68:- P1关闭门禁：0.5-1.5小时（环境可用）
./docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:111:2. 忽略了验证门禁的重要性
./docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:118:接受Codex的Option A-prime建议，先关闭P1验证门禁，再讨论下一步。
./docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:124:> 下一步执行Option A-prime：主动关闭API Schema P1验收门禁。首先修复login成功响应schema不匹配（创建LoginResponseSerializer），然后在可用Django环境中验证schema生成无警告、schema/swagger-ui可访问、operationId唯一。只有P1真实绿灯后，再执行收敛版P2（为关键端点补OpenApiExample）。如果当前环境无法完成P1验证，则硬停止并将P1状态标记为"代码完成，未验收"，等待可验证环境。
./docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:7:**说明：** 原请求期望输出 `70-api-data-reading-test-codex-response.md`，但本目录已有 `70-codex-post-phase2b-step1-next-strategy-response.md`；为避免覆盖既有讨论文档，本响应使用编号 `73`。
./docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:90:- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
./docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:128:- `test_xg_user_client.py`：mock HTTP响应，覆盖签名候选、字段解析、错误处理，不调用真实网络。
./docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:130:不建议把真实API调用写进Django常规测试套件。若确实需要live测试，使用 pytest marker 或环境变量硬门禁，并默认跳过。
./docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:178:当前 `.gitignore` 已覆盖 `.env`、`.env.local`、`.env.*.local`，方向正确。但建议增加一个可提交的示例文件：
./docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:246:- 成功记录响应结构、总数、字段覆盖情况。
./docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:264:- **实现可mock的客户端单元测试，覆盖签名候选和响应解析。**
./docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:76:- 增加单元测试/管理命令测试，覆盖成功导入、字段缺失、映射缺失、重复行
./docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:118:- 导入测试覆盖成功和主要失败路径
./docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:124:- smoke覆盖核心申请审批链路
./docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:125:- smoke至少覆盖附件上传、列表、下载、删除之一到多个
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:23:**Codex意见：** "全量覆盖（清空后重新导入）"会导致外键约束冲突，必须改为"staging表 + upsert + 软停用"。
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:31:导入策略：首版采用**全量覆盖**（清空后重新导入）
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:422:导入策略：首版采用**全量覆盖**（清空后重新导入）
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:447:- 删除"全量覆盖"描述
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:464:1. ✅ CSV导入从"全量覆盖"改为"staging + upsert + 软停用"
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:477:3. 提交给宿管系统方反馈
./docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:37:**选项A：Step 2C - 字段覆盖报告**
./docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:38:- doc 86原话："Step 2C：字段覆盖报告（依赖Step 2A结果）"
./docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:39:- 由于Step 2A未执行（无凭证），需基于文档样例创建字段覆盖草案
./docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:47:- 需依赖字段覆盖规则（Step 2C）
./docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:50:- 理由：字段覆盖可以在实现时边做边确定
./docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:66:   - 能否在实现Step 3时增量确定字段覆盖？
./docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:70:   - 缺失字段覆盖文档会导致什么问题？
./docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:94:- XG API客户端已完整实现且测试覆盖充分
./docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:110:4. 更新实施总结文档反映真实测试覆盖
./docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:191:2. 文档中声称的测试覆盖必须与实际运行的测试一致
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:110:4. 更新实施总结文档反映真实测试覆盖
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:191:2. 文档中声称的测试覆盖必须与实际运行的测试一致
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:14:理由很直接：上一轮共识已经把通知契约草案定义为纯文档任务，并明确“完成后硬停止”。`docs/api/notification-contract-v0.1.md` 自身也写明 Phase 1 “需单独授权”。因此，“继续讨论下一步”或再次要求 Claude/Codex 讨论，只能覆盖“可以重新评估”，不能自动覆盖“可以落库、加 API、加测试”。
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:75:- 测试覆盖良好（applications/approvals/attachments/notifications）
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:234:- 扩展smoke_test.sh覆盖更多场景
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:261:   - 端到端测试覆盖不足（质量保障）
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:290:2. smoke_test.sh覆盖至少20个场景（当前15个）
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:298:4. 测试覆盖通过
./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:95:- ✓ 19个API端点覆盖完整
./docs/discussions/phase4c-next-steps/22-claude-post-execution-next-steps.md:36:- 测试覆盖充分（48个后端测试 + 15步smoke test）
./docs/discussions/phase4c-next-steps/22-claude-post-execution-next-steps.md:111:- 测试覆盖率分析
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:218:4. **MAJOR**: 缺少覆盖：
docs/discussions/phase4c-next-steps/22-claude-post-execution-next-steps.md:36:- 测试覆盖充分（48个后端测试 + 15步smoke test）
docs/discussions/phase4c-next-steps/22-claude-post-execution-next-steps.md:111:- 测试覆盖率分析
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:87:- 添加测试覆盖详情：upload (5), list (6), download (4), delete (4)
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:55:- AttachmentType是否覆盖所有业务场景？
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:86:- res.data解析逻辑是否覆盖所有边界情况？
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:206:2. **类型安全：** TypeScript类型是否完全覆盖？
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:207:3. **错误边界：** 是否覆盖所有可能的错误场景？（网络错误、401、403、404、500、文件过大、文件类型不支持）
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:78:- 单元测试覆盖官方签名样例、md5、非法 `encryptionType`、缺失必填环境变量。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:111:live probe 成功后，应输出“字段覆盖报告”，再决定是否接入 Provider。没有班级/辅导员/宿舍字段前，不应把该接口宣称为完整业务数据源。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:234:- 产出脱敏字段覆盖报告。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:235:- 根据字段覆盖再开“是否接入 Provider”的新决策门。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:270:5. live probe 只产出字段覆盖报告，不直接触发 Provider 接入。
docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:11:**一致决策：采用选项组合2（扩展User模型+不允许API覆盖name），立即执行Step 4B实现。**
docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:44:- 核心字段不覆盖
docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:70:2. ✅ mapper测试覆盖email
docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:71:3. ✅ 服务测试覆盖更新补充字段
docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:72:4. ✅ 服务测试覆盖API缺失保持本地值
docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:73:5. ✅ 服务测试覆盖幂等
docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:74:6. ✅ 服务测试覆盖不创建用户
docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:75:7. ✅ 服务测试覆盖角色冲突
docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:76:8. ✅ 服务测试覆盖核心字段不覆盖
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:18:1. **Step 2C-lite：字段覆盖与映射契约**
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:42:### 能否在实现Step 3时增量确定字段覆盖？
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:44:可以增量修正字段覆盖，但不应在入库同步命令里首次确定字段覆盖。
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:78:### 缺失字段覆盖文档会导致什么问题？
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:99:1. 创建字段覆盖表，不追求真实字段全集，只覆盖“同步写库必需字段”。
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:112:完成这个文档后，Step 3 的 mapper/provider 可以很快实现，而且测试目标明确。反过来，如果直接写 DB 同步命令，测试会被迫同时覆盖字段猜测、数据转换、幂等 upsert、事务和命令输出，反馈周期会变慢。
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:118:Step 2系列还有一个关键遗漏：**字段覆盖报告不能只列 API 字段，还必须列内部写库字段和缺失字段策略。**
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:127:| `User.class_id` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:128:| `User.is_graduating` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:129:| `User.graduation_year` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:135:   - 在字段未完全覆盖前，API 只能补充或更新可确定字段，不能替代 CSV 导入。
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:173:- 单元测试覆盖字段缺失、角色未知、班级缺失、毕业字段缺失等场景。
./docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:116:| dorm_building | String | 宿舍楼栋 | 是 | "1号楼" |
docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:37:**选项A：Step 2C - 字段覆盖报告**
docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:38:- doc 86原话："Step 2C：字段覆盖报告（依赖Step 2A结果）"
docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:39:- 由于Step 2A未执行（无凭证），需基于文档样例创建字段覆盖草案
docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:47:- 需依赖字段覆盖规则（Step 2C）
docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:50:- 理由：字段覆盖可以在实现时边做边确定
docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:66:   - 能否在实现Step 3时增量确定字段覆盖？
docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:70:   - 缺失字段覆盖文档会导致什么问题？
docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:94:- XG API客户端已完整实现且测试覆盖充分
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:14:本轮P1修复已经落地：`would_update_count`被明确约束为"现有学生同步候选数"，不再暗示当前模型已有可持久化更新字段；warning文本也明确指出API补充字段暂不能落库。新增测试使用Django `TestCase`和真实测试数据库，覆盖doc 99要求的8个关键场景。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:35:- 阻塞解除条件：增加`phone/email/department`或批准`name`覆盖策略
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:51:## 测试覆盖审查
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:58:- `setUp`创建1个学生和1个辅导员，足够覆盖existing、conflict、readonly主路径
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:63:1. `test_mapper_skip_transparency`：覆盖skip透传和`skipped_by_reason`统计，通过。修正为断言实际mapper输出`missing_user_id`、`missing_name`是合理的。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:64:2. `test_existing_student_to_candidate`：覆盖`existing_count=1`、`would_update_count=1`候选数语义，通过。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:65:3. `test_missing_local_not_created`：覆盖`missing_local_count`、不创建用户、`would_create_but_blocked` warning，通过。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:66:4. `test_local_role_conflict`：覆盖`user_id/reason/local_role/api_role`结构，通过。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:67:5. `test_core_fields_readonly`：覆盖`class_id/is_graduating/graduation_year/name`不变，通过。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:68:6. `test_field_gap_warning_with_candidates`：覆盖强化warning关键文本，通过。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:69:7. `test_empty_input`：覆盖空输入全零计数和空列表，通过。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:70:8. `test_mixed_scenario`：覆盖skip、missing、conflict、existing分类关系和多个skip reason，通过。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:72:**结论：测试覆盖完整，满足Step 4A验收。**
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:84:完整。当前断言覆盖不创建、计数和`would_create_but_blocked`。服务warning已包含`class_id/is_graduating/graduation_year`，如需更强锁定可增加断言，但现有测试已经足够支撑Step 4A。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:142:Step 4B前置建议：优先决策User模型是否新增`phone/email/department`，以及`name`是否允许由学工API覆盖；在该决策完成前，不应把Step 4A的`would_update_count`解释为真实可写更新数。
docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:38:**缺点:** 可能过度工程，测试覆盖可能不必要
docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:52:**缺点:** 测试覆盖不足，可能遗漏边界情况
docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:94:1. **测试覆盖范围:** 是否需要完整测试矩阵（所有角色×所有操作），还是核心场景足够？
docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:112:- 测试覆盖是否充分但不过度
docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:56:### 审查要点2：测试文件是否覆盖8个关键场景
docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:170:2. **测试覆盖是否完整**
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:15:1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:18:4. 缺少若干实施级关键问题，例如账号标识映射、终审管理员分配规则、同步覆盖策略、历史审批人不被后续映射变更自动改写等。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:26:### 2.1 P0 数据源覆盖情况
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:28:当前 P0 数据源覆盖了系统运行所需的核心闭环：
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:134:4. CSV 需补充导入覆盖策略：全量覆盖、增量更新、软删除/停用、重复数据处理、失败回滚。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:168:当前问题覆盖了数据库、API、CSV 和数据范围，基本可用，但建议扩展为面向多方的数据确认清单。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:172:将“请宿管系统方反馈以下问题”改为：
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:174:> 请教务系统、人事系统、学工部数据负责人、宿管系统方分别确认其可提供的数据范围、字段、对接方式和联系人。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:176:原因：学生、辅导员、班级映射通常不是宿管系统的权责数据。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:188:9. CSV 导入时是否采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:199:共识文档中的推荐方案整体合理，但“如果宿管系统数据库包含所有数据”这个前提不够现实。学生、辅导员、班级映射不应假设都在宿管系统数据库中。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:203:1. 宿舍清退：优先使用宿管系统 API；若不可用，使用每日 CSV 导入；异常时保留人工证明。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:206:4. 班级-辅导员映射：首版优先 CSV/Excel 强校验，上线前必须 100% 覆盖当届学生。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:220:1. 先确认数据权责方和联系人，不把所有问题都压给宿管系统。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:222:3. 实现导入校验报告，重点校验学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:235:> 明确毕业离校系统所需的数据源，提交给宿管系统方反馈
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:239:> 明确毕业离校系统所需的数据源，提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人反馈。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:305:`31-data-source-requirements-consensus.md` 已经覆盖首版上线所需的主要 P0 数据源，字段设计也基本能支撑业务。它可以作为对接需求基础稿。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:309:1. 将反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:40:整体质量较好：需求目标明确，技术路线已基本固定，设计文档覆盖面广，评审过程记录完整，并且多轮审查已经识别并修正了若干关键方向性问题，例如“本项目数据库统一为 PostgreSQL”“外部系统 API 优先”“单实例部署”“上传安全”“工作日计算”“PostgreSQL 测试基线”等。
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:84:`docs/design/2026-05-27-system-design.md` 已覆盖 10 个主要部分：
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:169:   Phase 1 同时包含 Django 初始化、Docker、Celery、开发工具等任务。作为计划本身没有问题，但当前已完成部分只覆盖了目录、`.gitignore`、requirements。项目总结中已经正确标注其余任务为暂停/待继续。
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:193:- 补充 PostgreSQL 测试、覆盖率、性能目标
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:239:已配置内容覆盖：
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:255:`.gitignore` 覆盖面合理，适合当前技术栈。尤其是 `.env`、`node_modules/`、`.pytest_cache/`、`staticfiles/`、`db.sqlite3` 等常见噪声和敏感文件都已排除。
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:322:## 10. 本次分析没有覆盖的内容
docs/discussions/phase4c-next-steps/88-step2b-implementation-codex-response.md:29:**共识要求：** doc 85明确要求覆盖"缺失`data.data`、`users`不是list"。
docs/discussions/phase4c-next-steps/88-step2b-implementation-codex-response.md:71:## 4. 测试覆盖审查
docs/discussions/phase4c-next-steps/88-step2b-implementation-codex-response.md:73:现有8个新增测试覆盖了正常分页、空页、业务错误、HTTP错误、`max_pages`，但遗漏了几个共识要求：
docs/discussions/phase4c-next-steps/88-step2b-implementation-codex-response.md:80:5. doc 86要求的`page_size=1`场景未覆盖
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:10:`29-data-source-analysis.md` 的方向是正确的：当前数据对接文档只覆盖宿舍清退，无法完整支撑 student、counselor、admin 三类角色的账号初始化、权限边界和自动审批分配。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:28:| 宿舍清退数据 | 宿管系统 | P0 | 当前业务把宿舍清退作为提交前校验项，现有对接文档已覆盖。即使保留人工证明降级，正式流程仍应具备自动校验或批量数据导入能力。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:49:| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入、人工证明降级 | 当前文档策略合理。提交申请时实时性较强，API 价值高；若宿管系统暂不支持 API，则每日文件导入加人工证明降级。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:63:原因不是“方便展示”，而是学生账号、身份识别、申请资格、班级映射都依赖它。当前数据对接文档的目标用户也应从“宿舍管理系统管理员”扩展为“教务系统、人事系统、宿管系统及业务数据负责人”。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:82:建议数据对接文档单独增加“审批关系数据”章节，并把导入覆盖率 100% 作为上线验收条件之一。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:106:4. **导入校验和差异报告。** P0 数据导入不能只要求字段格式，还应要求失败明细、重复数据处理、覆盖策略、回滚策略和导入审计日志。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:132:4. **实现班级-辅导员映射导入。** 这是最关键步骤。上线前必须校验当届学生 100% 能解析到有效辅导员，否则不应开放提交。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:152:3. 新增“班级-辅导员对应关系导入”章节，列为 P0，并写明覆盖率和异常报告要求。
docs/discussions/phase4c-next-steps/05-claude-next-steps-strategy-request.md:11:- 19个attachment测试100%通过
docs/discussions/phase4c-next-steps/05-claude-next-steps-strategy-request.md:21:- ✅ 测试覆盖：48个后端测试 + 19个附件测试
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:14:但有一个必须先澄清并落地的小问题：`would_update_count`现在按"本地存在且role=student"计数。若该字段表示"真实可写更新数"，当前User模型没有`phone/email/department`，`name`是否允许API覆盖也未决，因此真实可更新字段数应为0。若该字段表示"未来可更新候选数"，则字段名有误导性，测试必须明确锁定这个语义。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:24:**问题描述：** 当前实现只要本地用户存在且角色为`student`，就执行`would_update_count += 1`。这符合文档97第4条"已存在学生计入would_update_count"，但与字段覆盖文档的Phase 1事实存在张力：User模型当前没有`phone/email/department`字段，`name`是否允许由API覆盖仍未决。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:65:7. 服务没有写DB，不会覆盖`class_id/is_graduating/graduation_year`。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:77:如果`would_update_count`表示"现有学生同步候选"，当前实现正确。如果表示"当前真实可写更新"，当前实现不准确，因为可安全写入字段未成立：`phone/email/department`不存在，`name`覆盖策略未决。建议在Step 4A把它定义为候选数，并用warning明确真实写入仍不可执行。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:89:有必要保留，但应调整断言目标。Step 4A只读，不需要测试"写入后未覆盖"；应该测试：
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:92:- summary不暴露任何会覆盖这些核心字段的计划项；
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:95:## 测试覆盖建议
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:97:文档97列出的8个场景覆盖了关键路径，可以执行，但建议对其中两个场景做精确定义：
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:100:2. "不覆盖class_id/is_graduating/graduation_year"：断言服务只读后DB原值不变，不要模拟Step 4B写入行为。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:110:2. 创建`backend/apps/users/tests/test_xg_user_sync.py`，使用真实Django测试数据库覆盖8个场景。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:56:`docs/design/2026-05-27-system-design.md` 内容覆盖较全面：
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:276:### 7.2 乐观锁覆盖面不够明确
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:481:单列索引如果被复合索引覆盖，应避免重复创建。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:487:测试策略方向正确：pytest、PostgreSQL、TDD、覆盖率 80%+、并发测试、文件安全测试、限流测试、审计测试。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:495:- 并发测试需要真实 PostgreSQL，SQLite 无法覆盖 `select_for_update`
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:6:**目的：** 明确毕业离校系统所需的数据源，提交给宿管系统方反馈
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:14:1. **CSV导入策略**：从"全量覆盖"改为"staging表 + upsert + 软停用"
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:45:- **API优先**：调用宿管系统提供的API接口（实时校验场景）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:46:- **DB备选**：直接读取宿管系统数据库（需要安全审批和网络配置）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:510:## 五、待宿管系统确认的问题清单
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:514:1. 宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:533:11. CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:559:1. 向宿管系统提交本需求文档
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:571:7. 重点校验：学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:574:1. 对接宿管系统宿舍清退API
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:722:1. ✅ CSV导入策略从"全量覆盖"改为"staging + upsert + 软停用"
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:730:1. 提交本文档给宿管系统方反馈
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:731:2. 根据宿管系统反馈调整方案
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:230:   - 同意。需要完整覆盖
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:267:- 第10章测试策略（TDD、PostgreSQL、覆盖）
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:67:### 3. 测试覆盖策略
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:75:5. 不覆盖class_id/is_graduating/graduation_year
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:81:- 这8个场景是否覆盖所有关键路径
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:134:- name（但CSV主导，是否允许API覆盖未决）
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:162:文档97要求测试"不覆盖class_id/is_graduating/graduation_year"。
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:179:2. **测试覆盖是否充分**
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:122:### AttachmentType是否覆盖所有业务场景？
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:124:覆盖当前MVP。四类与后端 `AttachmentType` 一致。不要在Phase 2扩展类型，除非业务明确要求新证明材料。
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:164:- `.btn-upload` 使用主按钮样式，宽度100%，放在列表/空状态之后。
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:167:响应式方面，rpx已经覆盖大部分机型，但长文件名和窄屏按钮组必须处理。核心不是复杂媒体查询，而是 `min-width:0`、`flex-wrap`、固定按钮尺寸和文本溢出策略。
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:477:3. 提交给宿管系统方反馈
docs/discussions/phase4c-next-steps/58-claude-codex-consensus-option-a-prime-partial.md:12:**执行Option A-prime：主动关闭API Schema P1验收门禁。**
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:58:- [ ] 19个API端点是否覆盖所有业务场景？
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:149:- [ ] 测试覆盖率目标是否合理？
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:155:- 单元测试覆盖率 >80%
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:31:3. ✓ 添加schema和Swagger UI路由
docs/discussions/phase4c-next-steps/84-post-step1-next-strategy-request.md:32:  - Live probe硬门禁（XG_RUN_LIVE_API_TEST=1）
docs/discussions/phase4c-next-steps/84-post-step1-next-strategy-request.md:81:- Mock测试覆盖
docs/discussions/phase4c-next-steps/84-post-step1-next-strategy-request.md:110:- 例如：前端优化、测试覆盖提升、文档完善
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:471:- 覆盖率：核心90%、整体70%
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:13:2. **测试覆盖评估**：评估当前测试充分性
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:70:**当前测试覆盖：**
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:98:   - Mock测试应覆盖哪些场景？
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:50:**Codex指出：** onShow中非学生统一reLaunch到login，覆盖onLoad的角色矩阵
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:54:- 生命周期冲突：onShow在onLoad后触发，会覆盖redirectTo
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:37:### 问题2：name字段是否允许API覆盖？
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:44:**如果允许覆盖：**
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:48:**如果不允许覆盖：**
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:56:### 选项组合1：扩展模型 + 允许name覆盖
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:65:- name覆盖可能与CSV冲突
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:69:### 选项组合2：扩展模型 + 不允许name覆盖
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:115:### name字段覆盖价值
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:124:**风险：** CSV重新导入可能覆盖API更新
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:155:**name覆盖策略选项：**
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:158:- API更新name → 覆盖
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:159:- CSV重新导入 → 覆盖
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:194:### 审查要点3：name覆盖策略
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:223:**影响：** name覆盖策略和字段主导权
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:259:3. **name覆盖决策**
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:53:- Live后输出覆盖报告
./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:146:**文件：** `docs/用户设计说明书.md:116, 144-145, 149`
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:13:Codex与Claude完全同意：P1修复已落地，测试覆盖完整，8/8通过验收。
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:30:### 2. 测试覆盖验收通过
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:34:**场景覆盖（全部通过）：**
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:44:**Codex评估：** 测试策略正确（Django TestCase + 真实DB），覆盖完整。
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:99:**问题2：name字段是否允许API覆盖？**
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:13:**推荐选项组合2：扩展User模型 + 不允许学工API覆盖name。**
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:17:不推荐组合1，因为允许API覆盖`name`会破坏已达成的CSV主导边界，并引入CSV重新导入与API同步之间的反复覆盖问题。不推荐组合3，因为它会让Step 4B没有真实写入目标，最终只能停留在Step 4A的候选报告。
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:25:当前`User`模型只包含`user_id/name/role/active/class_id/is_graduating/graduation_year`，mapper输出的`phone/department`无处落库。若选择“不扩展模型”，Step 4B不应改为`name`覆盖或其他轻量写入；应明确标记为跳过，保留Step 4A只读报告，并将后续Step 5命令限定为dry-run/plan命令。
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:29:字段覆盖契约已经定义CSV负责`user_id/name/role/class_id/is_graduating/graduation_year`，API负责`phone/email/department`。`name`虽然来自API，但它是核心身份展示字段，且CSV导入当前会更新`name`。允许API覆盖会造成数据源权威性不清晰。
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:67:## name覆盖决策
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:100:- 不做`name`覆盖。
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:122:2. mapper测试覆盖`email`存在、缺失两个场景。
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:123:3. 服务测试覆盖已存在学生更新`phone/email/department`。
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:124:4. 服务测试覆盖API缺失补充字段时保持本地原值。
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:125:5. 服务测试覆盖幂等：第二次同步`updated_count=0`或等价无变化统计。
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:126:6. 服务测试覆盖不创建本地缺失用户。
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:127:7. 服务测试覆盖角色冲突不更新。
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:128:8. 服务测试覆盖`name/class_id/is_graduating/graduation_year`不被API覆盖。
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:145:因此，CSV可持续导入并覆盖核心字段；API只更新补充字段。
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:177:4. API不覆盖`name`和毕业业务核心字段。
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:180:7. Step 4B测试以“真实写入 + 幂等 + 不覆盖核心字段”为验收核心。
docs/discussions/phase4c-next-steps/83-consensus-step1b-lite-first.md:73:- Live probe硬门禁（XG_RUN_LIVE_API_TEST=1+单页）
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:13:Codex的分析准确且全面：扩展模型+不覆盖name方案与Phase 1策略一致，migration风险低，字段权威性清晰，实施范围明确。
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:28:### 决策2：name不允许API覆盖
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:34:**Claude确认：** 完全同意。避免CSV重新导入与API同步的反复覆盖冲突，保持数据源权威性清晰。
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:80:- ❌ name覆盖
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:92:2. ✅ mapper测试覆盖email存在/缺失
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:93:3. ✅ 服务测试覆盖更新补充字段
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:94:4. ✅ 服务测试覆盖API缺失时保持本地值
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:95:5. ✅ 服务测试覆盖幂等（第二次sync unchanged）
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:96:6. ✅ 服务测试覆盖不创建missing_local
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:97:7. ✅ 服务测试覆盖role冲突不更新
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:98:8. ✅ 服务测试覆盖核心字段不被API覆盖
docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:14:更合理的下一步是 **Option A-prime：主动关闭API Schema P1验证门禁**。55号文档把P1描述为“已完成”，但同时列出三个关键待验证项：schema生成无警告、schema/swagger-ui可访问、operationId唯一。只要这些未验证，P1还不能视为完成。
docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:52:1. **先做P1关闭门禁。**
docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:57:   - 示例只覆盖最关键端点即可，不要扩大成完整文档重写。
docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:65:- **P1关闭门禁：** 环境可用时约0.5-1.5小时；若需要修依赖、数据库或settings，可能更久。
docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:66:- **P2示例：** 45-90分钟较合理，不建议默认1.5小时以上，除非要覆盖大量错误分支。
docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:108:> 下一步不直接执行API Schema P2。先执行Option A-prime：主动关闭API Schema P1验收门禁，修复已发现的login成功响应schema不匹配，并在可用Django环境中验证schema生成无警告、schema/swagger-ui可访问、operationId唯一。只有P1真实绿灯后，再执行一个收敛版P2，为登录、申请提交、审批操作、通知列表和通用错误补OpenApiExample。如果当前环境无法完成P1验证，则硬停止并将P1状态标记为“代码完成，未验收”，等待可验证环境。
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:19:6. 修改login.ts添加角色路由
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:27:**当前方案：** 先完整实现student-application页面（4个文件），最后修改login.ts路由
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:30:- 如果先实现页面但不修改路由，学生登录后无法访问新页面
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:31:- 如果先修改路由但页面不存在，会导致404错误
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:34:**替代方案A：** 先修改login.ts路由（添加条件判断但暂时注释），再实现页面，最后取消注释
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:35:**替代方案B：** 先创建空页面骨架（4个文件最小化内容），注册+路由，再逐步填充逻辑
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:36:**替代方案C：** 保持当前顺序，但在app.json注册后立即测试404，确认路由前页面可访问
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:58:- 如果login.ts路由已正确实现，角色保护是否冗余？
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:60:- 但如果login.ts路由有bug，角色保护会掩盖路由问题
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:62:**替代方案A：** 先不实现角色保护，依赖login.ts路由，测试通过后再添加防御性保护
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:63:**替代方案B：** 先实现角色保护，即使login.ts路由有bug也能防御
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:77:    return `宿舍清退未完成：${err.error.blocking_reason || '请联系宿管'}`;
docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:21:- 8个测试场景（覆盖skip/existing/missing/conflict/readonly/warning/empty/mixed）
docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:97:### 测试覆盖对比Codex建议
docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:143:- 8个测试场景是否覆盖所有关键路径
docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:151:**3. 测试覆盖充分性**
docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:167:   - 测试覆盖是否充分
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:71:学号,姓名,班级,宿舍楼栋,宿舍房间号,床号,是否已清退,清退日期,清退状态,备注
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:12:**完全接受Codex的Phase 2A稳定化门禁 + Option E-lite建议。**
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:25:### 1. Phase 2A稳定化门禁优先
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:58:1. Phase 2A稳定化门禁（0.5-1小时）
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:76:### Step 0: Phase 2A稳定化门禁（0.5-1小时）
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:119:- 添加schema和Swagger UI路由
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:153:4. 权限拒绝、状态冲突、宿舍阻断不创建通知（测试覆盖）
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:158:2. 覆盖审批驳回路径
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:181:- "至少20个smoke场景"数字目标 - 改为"覆盖关键风险"
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:187:根据用户的"继续讨论+直接执行"指令和Codex的Phase 2A稳定化建议，现在启动Phase 2A稳定化门禁实施，无需额外用户授权。
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:195:**Claude状态：** 立即启动Phase 2A稳定化门禁实施
docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:65:| User.class_id | 未确认 | 缺失 | CSV维护，API不覆盖 |
docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:66:| User.is_graduating | 未确认 | 缺失 | CSV维护，API不覆盖 |
docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:67:| User.graduation_year | 未确认 | 缺失 | CSV维护，API不覆盖 |
docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:74:- 字段未完全覆盖前，API只能补充或更新可确定字段
./docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:116:| dorm_building | String | 宿舍楼栋 | 是 | "1号楼" |
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:72:5. **核心字段保护：** 不覆盖class_id/is_graduating/graduation_year
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:18:2. 字段gap warning已强化，包含候选数量、`sync candidates exist`、`no API supplemental fields can be persisted`、`phone/email/department`以及name覆盖策略未批准的阻塞说明。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:21:**测试文件覆盖了8个关键场景，并使用Django `TestCase` + 真实测试数据库。**
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:67:测试名/注释写"skip/missing/conflict/existing各1个"，实际数据有2个skip。这是合理的，因为同一测试还要验证多个skip reason；但建议把注释改为"覆盖skip/missing/conflict/existing，skip包含两个reason"。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:98:## 测试覆盖审查
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:102:1. `test_mapper_skip_transparency`：覆盖mapper skip、`skipped_count`、`skipped_by_reason`。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:103:2. `test_existing_student_to_candidate`：覆盖`existing_count=1`、`would_update_count=1`候选数语义。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:104:3. `test_missing_local_not_created`：覆盖`missing_local_count=1`、不创建用户、`would_create_but_blocked` warning。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:105:4. `test_local_role_conflict`：覆盖`user_id/reason/local_role/api_role`冲突结构。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:106:5. `test_core_fields_readonly`：覆盖服务执行后`class_id/is_graduating/graduation_year/name`不变。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:107:6. `test_field_gap_warning_with_candidates`：覆盖强化warning关键文本。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:108:7. `test_empty_input`：覆盖空输入计数和列表为空。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:109:8. `test_mixed_scenario`：覆盖skip、missing、conflict、existing并验证分区计数关系。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:115:- `setUp()`创建1个学生和1个辅导员，足够覆盖当前8个场景。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:203:4. 进入Step 4B前置讨论：User模型扩展与name覆盖策略。
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:18:4. ✅ **风险识别全面**：5个关键风险点（无可写字段/创建边界/核心字段覆盖/停用策略/命令膨胀）
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:121:5. 不覆盖class_id/is_graduating/graduation_year
./docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:29:- ✅ 覆盖审批队列、通知查询、审计追踪
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:18:- 官方样例测试覆盖了显式 `sha1` 和默认 `sha1`。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:87:- live probe 硬门禁：`XG_RUN_LIVE_API_TEST=1`，配置齐全，固定 `page=1/pageNum=1`。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:117:字段覆盖: name=yes number=yes phone=yes department=yes user_identity=yes
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:77:- test断言是否覆盖了Option 1的核心验证点？
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:85:### 4. 测试覆盖
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:68:- 优点：测试覆盖先就绪，不依赖外部信息
docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:19:我的55号提案存在判断失误：将"代码修改完成"误认为"P1完成"，忽略了验证门禁的重要性。
docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:68:- P1关闭门禁：0.5-1.5小时（环境可用）
docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:111:2. 忽略了验证门禁的重要性
docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:118:接受Codex的Option A-prime建议，先关闭P1验证门禁，再讨论下一步。
docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:124:> 下一步执行Option A-prime：主动关闭API Schema P1验收门禁。首先修复login成功响应schema不匹配（创建LoginResponseSerializer），然后在可用Django环境中验证schema生成无警告、schema/swagger-ui可访问、operationId唯一。只有P1真实绿灯后，再执行收敛版P2（为关键端点补OpenApiExample）。如果当前环境无法完成P1验证，则硬停止并将P1状态标记为"代码完成，未验收"，等待可验证环境。
docs/discussions/phase4c-next-steps/19-claude-next-phase-strategy-request.md:87:- 有完整测试覆盖，风险可控
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:14:Phase 2A稳定化的前置门禁已经成立：我验证了通知服务层和API层两个测试模块，12/12通过。下一步继续推进smoke增强、OpenAPI基线和部署文档补漏是合理的。
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:54:### P1：Smoke前置条件不能只是注释，必须成为执行门禁
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:70:1. **保守方案：文档门禁**  
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:128:API测试已覆盖提交、审批通过、审批驳回和负向路径，足以支撑进入Option E-lite。但API层对`entity_id`的精确断言还不完整，当前主要断言了`type`、`entity_type`和message内容。
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:130:这不是阻塞项，因为服务层测试已覆盖`entity_id=approval.pk`，但若下一步smoke要验证`entity_id`，最好同步补1-2个API测试断言，避免脚本和API语义漂移。
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:179:> 下一步执行Option E-lite。先处理smoke可重复运行门禁，再增强通知字段和审批驳回路径；随后引入drf-spectacular作为OpenAPI基线，只验收schema可访问、端点清单和认证可见，并记录待完善项；最后补部署文档的环境变量表、smoke前置条件和故障排查。不要在本轮承诺完整API schema，也不要无条件自动重置数据库。
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:25:- 问题：User模型无phone/email/department，name覆盖未决
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:182:## 测试覆盖补充
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:45:3. Phase 1 会产生迁移、后端路由和测试资产，性质明显高于 Phase 0 的纯文档工作。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:47:如果用户原话确实包含“直接执行，直到项目完成”，它可以覆盖“停止讨论”的等待状态，但仍建议用一次极短确认把实现范围锁死，避免把外部验收阻塞误读成允许无限扩张 P2 功能。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:86:当前后端使用函数视图和 app-level urls，不是 ViewSet/router 风格。Phase 1 应遵循现有风格，除非先统一路由模式。
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:14:Phase 4C 证据闭环已经完成，之前的「完成证据包后硬停止」共识仍然正确。用户的新指令可以覆盖硬停止，但覆盖的是「可以继续讨论/重新决策」，不是自动授权进入新的 P2 功能实现。
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:118:之前共识是「证据闭环后硬停止，等待 DevTools、用户授权或外部系统信息」。用户的新要求如果只是「继续讨论」，它触发的是重新评估。只有当用户明确选择 Track 3 或授权继续内部开发时，才构成对硬停止的覆盖。
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:120:即使覆盖硬停止，也不应覆盖以下冻结边界：
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:19:   - 只记录脱敏摘要和字段覆盖。
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:25:   - 用 mock 测试覆盖多页、空页、最后页、业务错误、schema 异常。
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:27:3. **Step 2C：字段覆盖/映射决策。**
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:47:但它不应该成为分页实现的硬阻塞。当前 `diagnose_xg_api.py` 已经具备硬门禁，继续保持：
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:116:- Step 2B：实现 `fetch_all_users()`，mock 测试覆盖分页边界。
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:117:- Step 2C：整理字段覆盖清单，判断能否支撑用户同步。
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:123:- live 成功时有脱敏字段覆盖报告；live 失败时有明确错误分类和外部问题清单。
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:184:4. **字段覆盖不足以替代 CSV。**
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:186:   - 缓解：Step 3 前不得接 Provider 落库；先做字段覆盖报告和缺口表。
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:198:   - 缓解：继续强制脱敏；禁止保存原始响应；字段覆盖只记录布尔值和掩码样本。
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:200:**最终建议：立即执行 Step 2A 条件式 live probe，同时推进 Step 2B 分页读取。Step 2B 完成后，不要直接落库；先用 live 字段覆盖或平台字段说明完成 Step 3 的字段映射决策。**
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:15:理由是 Option E-lite 的边界已经在 46 号共识文档中明确：Smoke 增强、OpenAPI 基线、部署文档补漏。Step 1/Step 2 已经覆盖主要工程风险，继续扩展 API schema P1 项会把本轮从“基线交付”扩大成“文档精修”，不适合混入 Option E-lite 收尾。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:28:- smoke 覆盖 H1 happy path、H2 counselor reject、N2 cross-counselor 403。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:30:- notification 断言覆盖 `type`、`entity_type`、`message`。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:50:- `docs/api/api-schema-todo.md` 中 notification mark-as-read 路径写成 `/api/notifications/mark_as_read/`，实际路由和 schema 是 `/api/notifications/{notification_id}/read/`。Step 3 或收尾时应修正这个清单。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:73:环境变量表应以实际代码读取为准，优先覆盖：
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:95:建议覆盖这些高频场景：
docs/discussions/phase4c-next-steps/87-step2b-implementation-review-request.md:87:### 3. 测试覆盖
docs/discussions/phase4c-next-steps/87-step2b-implementation-review-request.md:148:4. **测试覆盖充分性**
docs/discussions/phase4c-next-steps/87-step2b-implementation-review-request.md:149:   - 8个测试是否覆盖所有边界条件？
docs/discussions/phase4c-next-steps/87-step2b-implementation-review-request.md:172:## 4. 测试覆盖审查
docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md:116:- 提升测试覆盖率
docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md:219:5. **是否违反了之前的共识？** 硬停止共识是否应该被用户的新指令覆盖？
./docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:97:**Claude补充：** mock测试应覆盖多种page_size：
./docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:129:4. 记录结果（成功：字段覆盖报告；失败：问题清单）
./docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:170:### 待定执行：Step 2C - 字段覆盖报告（依赖Step 2A结果）
./docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:179:- 覆盖情况（完全覆盖/部分覆盖/缺失）
./docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:182:**如果Step 2A未执行：** 基于文档样例创建字段覆盖草案
./docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:191:2. ✅ Step 2顺序：2A（条件式live probe）+ 2B（分页mock）+ 2C（字段覆盖）
./docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:201:9. ✅ mock测试覆盖page_size=1场景（暴露边界条件）
./docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:220:4. Step 2C字段覆盖报告（依赖2A结果）
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:19:- 统一为5个HTTP路由
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:37:- 错误样例现在覆盖：401, 403, 422, 503
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:90:- 增加单元测试/管理命令测试，覆盖成功导入、字段缺失、映射缺失、重复行。
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:171:- 导入测试覆盖成功和主要失败路径。
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:181:- smoke覆盖核心申请审批链路。
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:182:- smoke至少覆盖附件上传、列表、下载、删除之一到多个。
docs/discussions/phase4c-next-steps/43-claude-post-phase2a-stabilization-next-strategy.md:54:- 添加schema和Swagger UI路由
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:28:当前 `map_xg_user_to_internal()` 输出 `phone` 和 `department`，字段覆盖契约也把 `phone`、`email`、`department`定义为 API 补充字段。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:42:这意味着如果 Step 4 现在直接做“幂等 upsert 并写库”，实际可安全写入的 API 字段非常有限。`class_id`、`is_graduating`、`graduation_year`按共识不由 API 覆盖；`role`仅用于过滤学生；`user_id`是主键；剩下只有 `name` 可能可更新，但它属于 CSV 主导核心字段，不应在没有明确策略时被 API 静默覆盖。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:60:- 本地存在但核心字段缺失：不覆盖核心字段，计入冲突或跳过
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:137:- 不覆盖 `class_id`、`is_graduating`、`graduation_year`
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:182:3. **核心字段覆盖策略**
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:183:   - `name`、`class_id`、毕业字段由 CSV 主导，API 覆盖必须有明确规则。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:200:测试覆盖对只读 mapper 足够；对 Step 4 还缺服务级测试，尤其是本地存在性、角色冲突、不可创建、不可覆盖核心字段、summary 结构稳定性。
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:53:1. **术语不一致：** 执行计划"4个API端点" vs 契约"5个HTTP路由"
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:54:   - 建议：后续统一为"5个HTTP路由（login + 4个业务端点）"
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:76:- API端点（5个HTTP路由：login + submit + query + approve + reject）
docs/discussions/completion-review-2026-06-03/02-claude-response.md:15:- 后端/Docker/测试环境：98-100% ✓
docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:18:> 下一步执行Option E-lite。先实现smoke可重复运行门禁（SMOKE_RESET=1），再增强通知字段和审批驳回路径；随后引入drf-spectacular作为OpenAPI基线，只验收schema可访问、端点清单和认证可见，并记录待完善项；最后补部署文档的环境变量表、smoke前置条件和故障排查。不承诺完整API schema，不无条件自动重置数据库。
docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:24:1. **Smoke前置条件必须成为执行门禁**
docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:38:### Step 1.0: Smoke可重复运行门禁（1-1.5小时）
docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:68:2. smoke覆盖审批驳回路径
docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:90:**下一步：** 立即启动Step 1.0（Smoke可重复运行门禁）
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:16:1. **先做 Phase 2A稳定化门禁**：修正自动通知实现与契约不一致的问题，补足现有测试缺口。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:52:先修正服务层使用`NotificationType.APPLICATION_SUBMITTED`等枚举值，而不是裸字符串常量名；同步修正测试断言为枚举值/小写值。这个修复应作为所有文档工作的前置门禁。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:54:### P1：Phase 2A测试覆盖没有达到前一轮共识验收
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:58:当前自动通知测试覆盖了服务函数的正向创建和幂等，但没有覆盖关键API路径和负向路径：
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:86:1. 本轮：生成可访问的schema和Swagger UI，覆盖端点清单、认证、主要请求/响应对象。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:113:- 增加审批驳回路径，覆盖`APPROVAL_REJECTED`；
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:119:验收标准改为“覆盖关键端到端风险”，不要固定为“至少20个场景”。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:165:2. smoke脚本增强，覆盖真实API行为。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:181:**推荐执行 Option E-lite + Phase 2A稳定化门禁，暂不执行Phase 2B/2C。**
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:183:### Step 0：Phase 2A稳定化门禁（优先，0.5-1小时）
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:200:- 至少覆盖认证、申请、审批、附件、通知端点清单。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:215:3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:237:**Codex状态：** 建议按“Phase 2A稳定化门禁 + Option E-lite”达成共识后执行。
docs/discussions/phase4c-next-steps/71-claude-response-accept-b-mini.md:85:**测试覆盖：**
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:244:4. 充分的单元测试覆盖
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:309:**问题11：Mock数据测试覆盖度？**
docs/discussions/completion-review-2026-06-03/01-codex-final-assessment.md:14:| 后端/API/数据库/Docker/Smoke演示环境 | 98-100% | 已完成 |
docs/discussions/completion-review-2026-06-03/01-codex-final-assessment.md:26:当前状态覆盖：
docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md:49:- 当前路由是`/api/auth/login`（无尾斜杠）
docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md:55:- 精确记录当前路由和响应
docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md:74:1. **Track 1硬化：** CSV导入已完成，但可能有边界情况未覆盖
docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md:117:- 测试覆盖的最小标准是什么？
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:167:**测试覆盖：**
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:237:   - 401/403/404 处理是否覆盖所有关键场景？
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:246:5. **后端测试覆盖充分性**
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:247:   - 6个测试是否覆盖了P1修复的所有场景？
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:14:1. 用户新指令覆盖的是"可以继续讨论"，不是自动授权P2功能实现
docs/discussions/phase4c-next-steps/89-claude-response-agree-fixes.md:18:4. ✅ **测试覆盖gap真实**：遗漏doc 85明确要求的边界场景
docs/discussions/phase4c-next-steps/89-claude-response-agree-fixes.md:196:### 修复5：补充测试（覆盖gap）
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:19:5. ✅ **遗漏识别有效**：字段覆盖表必须包含"内部写库字段+缺失字段策略"，不只是API字段清单
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:101:# 学工系统用户API字段覆盖报告
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:124:| User.class_id | 未确认 | 缺失 | 继续由CSV/手工维护，API不覆盖 |
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:125:| User.is_graduating | 未确认 | 缺失 | 继续由CSV/手工维护，API不覆盖 |
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:126:| User.graduation_year | 未确认 | 缺失 | 继续由CSV/手工维护，API不覆盖 |
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:132:[在字段未完全覆盖前，API只能补充或更新可确定字段，不能替代CSV导入]
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:236:5. ✅ API/CSV并存策略：字段未完全覆盖前，API不能替代CSV
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:111:   学生只能查自己的申请不是边界条件，而是核心安全契约。最小闭环至少要覆盖一条负向权限验证。
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:87:### Step 1.0: Smoke可重复运行门禁（1-1.5小时）
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:125:- 添加schema和Swagger UI路由
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:162:2. smoke覆盖审批驳回路径
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:184:> 下一步执行Option E-lite。先实现smoke可重复运行门禁（SMOKE_RESET=1），再增强通知字段和审批驳回路径；随后引入drf-spectacular作为OpenAPI基线，只验收schema可访问、端点清单和认证可见，并记录待完善项；最后补部署文档的环境变量表、smoke前置条件和故障排查。不承诺完整API schema，不无条件自动重置数据库。
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:52:- 5种通知类型全覆盖（APPLICATION_SUBMITTED、APPROVAL_APPROVED、APPROVAL_REJECTED、DORM_CLEARANCE_BLOCKED、APPROVAL_TIMEOUT_WARNING）
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:66:- 测试覆盖：1-2小时
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:132:- 补充smoke test覆盖通知API
docs/discussions/phase4c-next-steps/53-codex-confirmation-option-a-corrected.md:38:- Schema必须匹配当前API行为，除非同时提交有测试覆盖的行为变更。
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:14:2. 错误处理覆盖所有关键路径
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:249:   - 是否需要额外的测试覆盖
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:274:2. 错误处理覆盖所有关键路径
docs/discussions/phase4c-next-steps/94-post-step3-next-priority-request.md:83:   - 测试覆盖是否充分？
docs/discussions/phase4c-next-steps/94-post-step3-next-priority-request.md:100:- mapper已完整实现且测试覆盖充分
docs/discussions/phase4c-next-steps/23-codex-post-execution-next-steps-response.md:66:3. **演示脚本**：覆盖 seed/import、登录、申请提交、附件、审批、错误处理、权限验证。
docs/discussions/phase4c-next-steps/23-codex-post-execution-next-steps-response.md:141:脚本应覆盖：
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:76:- 增加单元测试/管理命令测试，覆盖成功导入、字段缺失、映射缺失、重复行
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:118:- 导入测试覆盖成功和主要失败路径
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:124:- smoke覆盖核心申请审批链路
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:125:- smoke至少覆盖附件上传、列表、下载、删除之一到多个
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:135:4. 真实API测试通过 `XG_RUN_LIVE_API_TEST=1` 门禁
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:249:### Step 2：实现Mock测试（CI覆盖）
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:259:- 测试覆盖签名生成、请求构造、响应解析
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:271:4. 记录响应结构和字段覆盖情况
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:299:4. ✅ 真实API不进CI，通过环境变量门禁
docs/discussions/week3-direction-2026-05-30/03-claude-response.md:68:**Codex的P2包括"Docker Compose覆盖必要依赖"，但：**
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:30:- ✅ 验证通过：契约修改完整、实体修正合理、测试覆盖完整、无其他引用
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md:103:- ✅ test_auto_notifications_api.py：3个断言覆盖核心语义
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:7:**说明：** 原请求期望输出 `70-api-data-reading-test-codex-response.md`，但本目录已有 `70-codex-post-phase2b-step1-next-strategy-response.md`；为避免覆盖既有讨论文档，本响应使用编号 `73`。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:90:- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:128:- `test_xg_user_client.py`：mock HTTP响应，覆盖签名候选、字段解析、错误处理，不调用真实网络。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:130:不建议把真实API调用写进Django常规测试套件。若确实需要live测试，使用 pytest marker 或环境变量硬门禁，并默认跳过。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:178:当前 `.gitignore` 已覆盖 `.env`、`.env.local`、`.env.*.local`，方向正确。但建议增加一个可提交的示例文件：
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:246:- 成功记录响应结构、总数、字段覆盖情况。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:264:- **实现可mock的客户端单元测试，覆盖签名候选和响应解析。**
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:131:### 3. 阻断测试覆盖了Option 1核心行为
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:133:`backend/apps/notifications/tests/test_auto_notifications_api.py:245-257`覆盖了三点：
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:140:这已经覆盖Option 1的核心验收点。验证422错误message可以作为P2增强，但不是当前commit门禁；当前断言已足够证明“阻断不产生申请、不产生通知”。
docs/discussions/phase4c-next-steps/72-claude-codex-consensus-phase2b-step2-strategy.md:106:- 覆盖：counselor/dean超时场景
docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:97:**Claude补充：** mock测试应覆盖多种page_size：
docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:129:4. 记录结果（成功：字段覆盖报告；失败：问题清单）
docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:170:### 待定执行：Step 2C - 字段覆盖报告（依赖Step 2A结果）
docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:179:- 覆盖情况（完全覆盖/部分覆盖/缺失）
docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:182:**如果Step 2A未执行：** 基于文档样例创建字段覆盖草案
docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:191:2. ✅ Step 2顺序：2A（条件式live probe）+ 2B（分页mock）+ 2C（字段覆盖）
docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:201:9. ✅ mock测试覆盖page_size=1场景（暴露边界条件）
docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:220:4. Step 2C字段覆盖报告（依赖2A结果）
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:57:- Live probe后输出字段覆盖报告
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:150:- Live调用门禁
docs/discussions/week3-direction-2026-05-30/02-codex-review.md:41:- Docker Compose覆盖必要依赖（PostgreSQL、Django）
docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.md:126:4. **Mock测试**：全场景覆盖
docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.md:166:   - 硬门禁：`XG_RUN_LIVE_API_TEST=1` 且配置齐全

codex
目标文档本身的事实链条基本清楚，但推荐方案把“降低门禁”和“116人暂不可用”合在一起处理，可能混淆了技术验收与上线业务承诺。我再核对前序共识和验证报告，看看100%门禁原先为什么设定、是否允许带限制通过。
exec
/bin/bash -lc "rtk sed -n '1,260p' .omc/collaboration/artifacts/20260605-user-business-decisions.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 用户业务决策记录（2026-06-05）

**背景：** Phase 0就绪后，用户回答4个开放问题

---

## 用户4项决策

### 决策1：寝室号字段（确认）

**问题：** File5是否需要room_number字段？File3何时补充？

**用户答复：**
> "文件5的数据中应该有寝室号字段，文件3中没有，后面会再确认提交文件3的寝室号字段数据，以形成单一对应关系"

**结论：**
- File5必须包含room_number字段 ✓（已在merge_student_data.py实现）
- File3后续补充room_number字段
- 升级路径：Phase 1楼栋级路由 → Phase 2寝室级精确一对一路由

---

### 决策2：楼栋名称匹配规则

**问题：** File1与File3楼栋名称是否需要规范化？如何匹配？

**用户答复：**
> "按楼栋名称吻合的匹配"

**结论：**
- 使用楼栋名称直接匹配（exact match或normalized match）
- 如File3楼栋名与File1不同，需创建building_normalization_map.json
- validate_routing_coverage.py将检测未匹配楼栋

**实施：**
- Phase 0.3：File3到达后分析楼栋名称
- 如需规范化，创建building normalization map
- 100%覆盖门禁确保所有学生可路由

---

### 决策3：File2独有116行处理

**问题：** File2中116个File1没有的学生如何处理？

**用户答复：**
> "导入"

**结论：**
- File2独有116行作为额外学生导入
- 总学生数：5830（File1）+ 116（File2 only）= 5946行
- 需修改合并策略

**影响：**

**merge_student_data.py需调整：**
```python
# 当前：只输出File1的5830行
# 修改：输出File1 + File2独有行

# 新逻辑：
# 1. File1为基准（5830行）
# 2. File2匹配的：补充字段
# 3. File2独有的（116行）：作为新行追加
#    - user_id: 从File2的XH
#    - user_id_source: 'file2_only'
#    - File1字段：空值
```

**merge_report.json需包含：**
- file1_only_count: 271（研究生等）
- file2_only_count: 116
- matched_count: 5559
- total_output_rows: 5946

---

### 决策4：学工管理员数据提供方式

**问题：** Admin角色如何实现？复用dean还是新增？

**用户答复：**
> "学工管理员数据后面会同样提供EXCEL表格或CSV数据（学工管理员，不做审批流程，但能查看全部进度数据）"

**结论：**
- 学工管理员数据单独提供（Excel/CSV格式）
- 角色定义：只读，可查看全部申请，无审批权限
- 不复用dean枚举，等待独立数据文件

**数据格式（待确认）：**
```
职工号,姓名,部门,手机号,邮箱
A001,张三,学工部,13800000001,zhangsan@example.com
```

**实施：**
- Phase 3增加：import_admins命令
- UserRole枚举：student | dorm_manager | counselor | admin
- 权限：admin可查看所有申请但不能审批

---

## 实施影响

### 立即需要修改

**1. merge_student_data.py**
- 增加File2独有行处理逻辑
- 输出5946行而非5830行
- 新增user_id_source: 'file2_only'

**2. validate_routing_coverage.py**
- 验证目标：5946行学生100%路由覆盖

**3. 文档更新**
- 实施方案：数据覆盖5830→5946
- Phase 3：增加import_admins命令

### 等待用户提供

**1. 真实数据文件**
- File1-4 Excel文件

**2. 学工管理员数据**
- Admin Excel/CSV文件
- 字段格式待确认

**3. File3寝室号补充**
- Phase 2升级时提供

---

**文档日期：** 2026-06-05  
**决策状态：** 4/4已回答  
**下一步：** 修改merge脚本支持File2独有行，更新文档反映5946行total

exec
/bin/bash -lc "rtk sed -n '1,220p' backend/data/routing_coverage_report.json" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{
  "total_students": 5946,
  "dorm_manager_coverage": 5830,
  "counselor_coverage": 5946,
  "fully_routable": 5830,
  "missing_dorm_manager": [
    {
      "user_id": "2020150140631",
      "name": "江羽抒",
      "building": ""
    },
    {
      "user_id": "2020170140125",
      "name": "姜瑶",
      "building": ""
    },
    {
      "user_id": "2021150240222",
      "name": "王鹏程",
      "building": ""
    },
    {
      "user_id": "2021150140527",
      "name": "周若奕",
      "building": ""
    },
    {
      "user_id": "2021120340233",
      "name": "张文君",
      "building": ""
    },
    {
      "user_id": "2021280240108",
      "name": "刘谦民",
      "building": ""
    },
    {
      "user_id": "2021170140110",
      "name": "饶梦琦",
      "building": ""
    },
    {
      "user_id": "2021280240123",
      "name": "叶曌",
      "building": ""
    },
    {
      "user_id": "2021280540124",
      "name": "冯璇",
      "building": ""
    },
    {
      "user_id": "2021320140210",
      "name": "朱松竹",
      "building": ""
    },
    {
      "user_id": "2021170340140",
      "name": "刘何雨欣",
      "building": ""
    },
    {
      "user_id": "2021110140308",
      "name": "黄浩钰",
      "building": ""
    },
    {
      "user_id": "2021140140304",
      "name": "涂腾",
      "building": ""
    },
    {
      "user_id": "2022140240107",
      "name": "吴祥东",
      "building": ""
    },
    {
      "user_id": "2022190540114",
      "name": "翟雨萱",
      "building": ""
    },
    {
      "user_id": "2022140240229",
      "name": "宋泽航",
      "building": ""
    },
    {
      "user_id": "2022150140510",
      "name": "纪宇澄",
      "building": ""
    },
    {
      "user_id": "2022110140303",
      "name": "黄汝鋆",
      "building": ""
    },
    {
      "user_id": "2022220040205",
      "name": "钟现代",
      "building": ""
    },
    {
      "user_id": "2022150140304",
      "name": "刘可欣",
      "building": ""
    },
    {
      "user_id": "2022150140203",
      "name": "徐奕婷",
      "building": ""
    },
    {
      "user_id": "2022150440104",
      "name": "杨谨硕",
      "building": ""
    },
    {
      "user_id": "2022150440108",
      "name": "郑秋晗",
      "building": ""
    },
    {
      "user_id": "2022130240102",
      "name": "胡开芸",
      "building": ""
    },
    {
      "user_id": "2022160240226",
      "name": "魏臻",
      "building": ""
    },
    {
      "user_id": "2022180240801",
      "name": "程若愚",
      "building": ""
    },
    {
      "user_id": "2022150140313",
      "name": "雷佳懿",
      "building": ""
    },
    {
      "user_id": "2022180340214",
      "name": "王居慧",
      "building": ""
    },
    {
      "user_id": "2022320140214",
      "name": "刘李乐",
      "building": ""
    },
    {
      "user_id": "2022150140222",
      "name": "徐晓佳",
      "building": ""
    },
    {
      "user_id": "2022280040122",
      "name": "李泽康",
      "building": ""
    },
    {
      "user_id": "2022150140128",
      "name": "盛周慧",
      "building": ""
    },
    {
      "user_id": "2022130440116",
      "name": "吕铭哲",
      "building": ""
    },
    {
      "user_id": "2022130440117",
      "name": "马蕴涵",
      "building": ""
    },
    {
      "user_id": "2022110340113",
      "name": "李魏魏",
      "building": ""
    },
    {
      "user_id": "2022210140316",
      "name": "马利伟",
      "building": ""
    },
    {
      "user_id": "2022110140317",
      "name": "杨欢",
      "building": ""
    },
    {
      "user_id": "2022110140519",
      "name": "周永炎",
      "building": ""
    },
    {
      "user_id": "2022110240118",
      "name": "周薇",
      "building": ""
    },
    {
      "user_id": "2022150140511",
      "name": "曹钰莹",
      "building": ""
    },
    {
      "user_id": "2022170340403",
      "name": "李雯娟",
      "building": ""
    },
    {
      "user_id": "2022170340305",
      "name": "柯雅馨",
      "building": ""
    },
    {
      "user_id": "2022170340306",
      "name": "郑淼文",
      "building": ""

exec
/bin/bash -lc "rtk sed -n '1,260p' .omc/collaboration/artifacts/20260605-consensus-implementation-plan.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Consensus: Implementation Plan Review

**Date:** 2026-06-05  
**Participants:** Claude, Codex  
**Topic:** 用户需求最终确认与实施方案.md review and P0 blocker resolution  
**Status:** ✅ Consensus achieved, implementation-ready

---

## Agreement Summary

**Codex assessment:** 22/40 score, 3 P0 blockers prevent immediate implementation.

**Claude response:** All P0 blockers addressed via Phase 0 data validation scripts.

**Consensus:** Implementation plan is sound after Phase 0 additions. Proceed with Phase 0 execution when real data files available.

---

## P0 Blocker Resolutions (Agreed)

### P0-1: Empty Student ID → Temp ID Strategy ✅

**Problem:** User.user_id required but 271 grad + File2 unmatched lack student numbers.

**Solution:** 3-tier ID generation
- Priority 1: Real XH from File2
- Priority 2: `GRAD2026_{hash8}` for graduates (SHA256 stable hash)
- Priority 3: `TMP2026_{row:04d}` for File2 unmatched

**Implementation:** `generate_temp_user_ids.py` (tested, committed)

**File5 schema extensions:**
- `user_id` (required): Login ID (real or generated)
- `student_no` (optional): Real XH from File2
- `user_id_source`: 'file2_xh' | 'grad_generated' | 'tmp_generated'
- `source_row_id`: File1 original row number

**Agreement:** This preserves data integrity while allowing full 5830-row import.

---

### P0-2: Multi-Approver Conflict → Primary Manager ✅

**Problem:** Document suggests "any manager" but Approval.approver is single FK.

**Solution:** MVP scope reduction
- File3 must provide `primary_dorm_manager_user_id` per building
- Each building has exactly one primary responsible manager
- Multi-manager approval deferred to Phase 2

**Implementation requirement:** File3 processing identifies single primary (first listed, manual spec, or default rule).

**Agreement:** This maintains clean FK model while providing Phase 2 upgrade path.

---

### P0-3: ClassMapping Removal → Explicit Task List ✅

**Problem:** ClassMapping deeply embedded, removal underestimated.

**Solution:** Phase 2 expanded to 10 explicit subtasks
1. Data model adjustments
2. Submission routing refactor
3. Approval pass routing refactor
4. List filtering refactor
5. Detail permissions refactor
6. Attachment permissions sync
7. Import command rewrite
8. API schema update
9. Frontend/miniprogram types sync
10. Test fixture and regression

**Validation gate:** `validate_routing_coverage.py` enforces 100% coverage before Phase 2.

**Agreement:** Expanded task list prevents underestimation. Gate ensures data readiness.

---

## P1 Findings (Acknowledged)

### Data Inconsistency
- File1/File2 count discrepancy (155 vs 271+116) needs reconciliation
- Merge report will output: `matched_count`, `file1_only_count`, `file2_only_count`
- File2-only 116 rows: User to decide import vs archive

### State Machine Naming
- Keep existing `pending_dorm_manager` / `pending_counselor` convention
- Avoid unnecessary migration from current backend/apps/applications/models.py

### Application Snapshots
- Add `student_building_name`, `student_department` to Application model
- Deferred to Phase 2 data model task
- Prevents routing corruption when User data changes

### Normalization Maps
- College: 18 mappings in `normalize_colleges.py` ✅
- Building: Requires File3 analysis, pending
- Both required for 100% routing coverage

**Agreement:** These are implementation details, not blockers. Address in Phase 0-2.

---

## User Supplemental Requirement

**User statement (2026-06-05):**
> "文件5的数据中应该有寝室号字段，文件3中没有，后面会再确认提交文件3的寝室号字段数据，以形成单一对应关系"

**Status:**
- ✅ File5 includes `room_number` field (merge_student_data.py line 131)
- ✅ Documented in implementation plan Section 2
- ✅ Two-phase strategy: Phase 1 building-level, Phase 2 room-level precise

**Agreement:** Room_number preserved for future File3 upgrade. No action required now.

---

## Phase 0 Implementation Status

### Completed (2026-06-05)

**Scripts created and tested:**

1. **generate_temp_user_ids.py** (94 lines)
   - `determine_user_id()`: 3-tier ID strategy
   - `generate_grad_user_id()`: SHA256 hash for graduates
   - `generate_tmp_user_id()`: Sequential for File2 unmatched
   - Tests: ✅ Pass (real XH, grad hash stability, tmp sequential)

2. **merge_student_data.py** (182 lines)
   - `merge_files()`: File1+File2 → File5 with source tracking
   - Matching key: "姓名+规范化学院+班级/BH"
   - Output: 14 fields including user_id, user_id_source, student_no, room_number
   - Statistics: matched/file1_only/grad/tmp counts, skipped rows

3. **validate_routing_coverage.py** (177 lines)
   - `validate_routing()`: 100% coverage gate check
   - Validates: building→manager, department→counselor
   - Exit: 0 if 100%, 1 with detailed failure report
   - Report: Missing buildings/departments with student counts

4. **normalize_colleges.py** (existing)
   - 18 college mappings
   - ValueError on unmapped names

**Commit:** a142ad8 "feat: Phase 0数据门禁脚本实现" (+547 lines)

**Documentation updated:**
- Implementation plan: File mapping table, Phase 0 section, adjusted timeline
- Status: "⚠️ Codex审查完成，3个P0技术阻塞待修正 (评分22/40)"

### Ready for Execution

**Prerequisites met:** ✅ All Phase 0 scripts implementation-ready

**Awaiting:** Real data files from user
- File1: 1-5830名毕业生（含研究生）.xls
- File2: 2026届预计毕业生5675人.xlsx
- File3: 2026年社区辅导员信息统计表.xls
- File4: 2026年学院辅导员信息统计表.xls

---

## Execution Plan

### Phase 0: Data Validation (Ready Now)

**Step 1: Merge File1 + File2**
```bash
python3 backend/scripts/merge_student_data.py \
  --file1 <path-to-file1> \
  --file2 <path-to-file2> \
  --output backend/data/file5_students_5830.csv \
  --report backend/data/merge_report.json
```

**Expected output:**
- file5_students_5830.csv (5830 rows, non-null user_id)
- merge_report.json (matched/file1_only/grad/tmp counts)

**Step 2: Validate Routing Coverage**
```bash
python3 backend/scripts/validate_routing_coverage.py \
  --file5 backend/data/file5_students_5830.csv \
  --file3 <path-to-file3> \
  --file4 <path-to-file4> \
  --report backend/data/routing_coverage_report.json
```

**Gate criteria:**
- Exit code 0 (100% coverage)
- No missing buildings or departments
- All 5830 students routable

**If gate fails:** Review failure report, fix missing mappings, repeat validation.

### Phase 1-5: Implementation (After Phase 0 Pass)

**Phase 1:** Data preparation (0.5 day)
- Building normalization map
- Primary manager selection per building
- Final CSV cleanup

**Phase 2:** System code adjustment (1-1.5 days)
- 10 explicit subtasks (data model, routing, permissions, etc.)

**Phase 3:** Data import (0.5 day)
**Phase 4:** Frontend adjustment (0.5 day)
**Phase 5:** Testing validation (0.5 day)

**Total timeline:** 4-6 days (increased from original 2.5-3 days)

---

## Open Questions for User

**Q1: Primary Dorm Manager Selection**
When building has multiple managers in File3, which to use?
- Option A: First listed in File3 (simplest)
- Option B: Manual specification via new column
- Option C: Alphabetical by name

**Recommendation:** Option A (first listed) for MVP simplicity.

**Q2: Building Normalization**
Does File3 use same building names as File1?
- If yes: No action needed
- If no: Need building normalization map like colleges

**Action:** Review File3 building names against File1 after file provided.

**Q3: File2-Only 116 Rows**
What to do with 116 students in File2 but not File1?
- Option A: Import as additional students (total 5946)
- Option B: Archive report only, don't import (keep 5830)

**Recommendation:** Option B (archive only) maintains File1 as authoritative base.

**Q4: Admin Role Implementation**
New admin role vs reusing existing dean enum?
- Option A: Reuse `dean`, change display to "学工管理员"
- Option B: Add new `admin` enum, migrate existing

**Recommendation:** Option A (reuse dean) avoids migration.

---

## Final Recommendations

### Immediate Actions (User)

1. **Provide data files** for Phase 0 execution
2. **Answer Q1-Q4** to unblock Phase 1 decisions
3. **Review building names** in File3 vs File1 for normalization needs

### Implementation Approach (Technical)

1. **Phase 0 first, no exceptions:** Gate prevents bad data from entering system
2. **Keep existing conventions:** State machine names, dean role reuse

exec
/bin/bash -lc "rtk nl -ba .omc/collaboration/artifacts/20260605-phase0-routing-coverage-blocker.md | sed -n '1,240p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# Phase 0 路由覆盖P0阻塞分析
     2	
     3	**创建时间：** 2026-06-05T19:55:00Z  
     4	**任务ID：** TASK-20260605-04  
     5	**分析人：** Claude  
     6	**严重程度：** P0 (阻塞Phase 0验证通过)
     7	
     8	---
     9	
    10	## 执行摘要
    11	
    12	Phase 0 Task 0.5（路由覆盖验证）执行结果：
    13	- **辅导员路由覆盖率：** 100.0% ✓ (5946/5946)
    14	- **宿管员路由覆盖率：** 98.0% ✗ (5830/5946)
    15	- **完整路由覆盖率：** 98.0% ✗ (5830/5946)
    16	
    17	**门禁要求：** 100%路由覆盖率（文档要求）
    18	
    19	**阻塞原因：** 116名File2独有学生缺少楼栋数据，无法路由至宿管员。
    20	
    21	**业务影响：** 阻塞Phase 0验证通过，无法进入Phase 1-5实施。
    22	
    23	---
    24	
    25	## 问题详情
    26	
    27	### 数据证据
    28	
    29	**受影响学生数量：** 116人
    30	
    31	**样本数据（前10人）：**
    32	```
    33	1. user_id=2020150140631, name=江羽抒, building=""
    34	2. user_id=2020170140125, name=姜瑶, building=""
    35	3. user_id=2021150240222, name=王鹏程, building=""
    36	4. user_id=2021150140527, name=周若奕, building=""
    37	5. user_id=2021120340233, name=张文君, building=""
    38	6. user_id=2021280240108, name=刘谦民, building=""
    39	7. user_id=2021170140110, name=饶梦琦, building=""
    40	8. user_id=2021280240123, name=叶曌, building=""
    41	9. user_id=2021280540124, name=冯璇, building=""
    42	10. user_id=2021320140210, name=朱松竹, building=""
    43	```
    44	
    45	**特征：**
    46	- 全部116人building字段为空字符串
    47	- 拥有真实学号（2020/2021开头）
    48	- user_id_source = 'file2_only'（来自File2但不在File1中）
    49	- department字段非空（可以路由到辅导员）
    50	
    51	---
    52	
    53	## 根本原因分析
    54	
    55	### 数据源对比
    56	
    57	**File1字段（5830行）：**
    58	- 学生姓名、学院名称、**楼栋名称**、**寝室号**、专业、年级、班级、层次
    59	
    60	**File2字段（5675行）：**
    61	- XH（学号）、XM（姓名）、FY（学院）、BH（班号）、SJHM（手机号）、email
    62	- **缺失：** 楼栋名称、寝室号
    63	
    64	**合并策略（merge_student_data.py）：**
    65	1. File1作为基准（5830行）
    66	2. File2补充学号、手机号、邮箱等字段
    67	3. File2独有的116行学生追加到输出（用户决策3，2026-06-05）
    68	4. File2独有学生的building_name和room_number字段为空字符串
    69	
    70	**结论：** File2数据源本身不包含楼栋/寝室信息，因此File2独有的116名学生无法获得building_name字段，导致无法路由到宿管员。
    71	
    72	---
    73	
    74	## 影响评估
    75	
    76	### 业务影响
    77	
    78	**阻塞范围：**
    79	- ✗ Phase 0 Task 0.5验证失败（98.0% vs 100%门禁要求）
    80	- ✗ 无法进入Phase 1（数据准备与合并）
    81	- ✗ 无法进入Phase 2-5（系统代码调整、数据导入、前端调整、测试验证）
    82	
    83	**受影响学生：**
    84	- 116名学生无法提交离校申请（缺少第一级审批人-宿管员）
    85	- 占总学生数的1.95%（116/5946）
    86	- 这些学生有真实学号，可能是合法在校生
    87	
    88	### 系统影响
    89	
    90	**审批流程设计：**
    91	```
    92	学生提交 → 宿管员审批(by 楼栋) → 辅导员审批(by 学院) → 完成
    93	```
    94	
    95	**第一级审批路由：** building_name → DormManager
    96	- 必需字段：building_name（楼栋名称）
    97	- 当前状态：116人building_name为空，路由失败
    98	
    99	**第二级审批路由：** department → Counselor  
   100	- 必需字段：department（学院）
   101	- 当前状态：5946人全部有department，路由成功 ✓
   102	
   103	---
   104	
   105	## 决策选项分析
   106	
   107	### 选项1: 接受98%覆盖率作为可接受标准
   108	
   109	**描述：** 修改Phase 0门禁要求，将100%覆盖率降低为98%（或"File1学生100%覆盖率"）
   110	
   111	**优点：**
   112	- 立即解除P0阻塞，可以进入Phase 1-5实施
   113	- 技术实现无需修改（验证脚本已完成）
   114	- 承认数据源限制的现实
   115	
   116	**缺点：**
   117	- 降低数据质量标准
   118	- 116名学生无法使用系统（占1.95%）
   119	- 可能需要后续手工处理这116人的离校流程
   120	
   121	**实施成本：** 低（仅需修改文档门禁标准）
   122	
   123	**风险：** 中（用户可能要求这116人也能使用系统）
   124	
   125	---
   126	
   127	### 选项2: 排除File2独有学生，仅导入File1学生
   128	
   129	**描述：** 回退用户决策3（2026-06-05），不导入File2独有的116名学生
   130	
   131	**优点：**
   132	- 达到100%覆盖率（5830/5830）
   133	- 通过Phase 0门禁，可以进入Phase 1-5
   134	- 数据一致性强（所有导入学生都有完整字段）
   135	
   136	**缺点：**
   137	- 违反用户明确决策（用户要求导入File2独有学生）
   138	- 116名可能是合法在校生被排除系统外
   139	- 需要修改merge_student_data.py
   140	- 需要重新生成File5并更新文档
   141	
   142	**实施成本：** 中（代码+数据+文档修改）
   143	
   144	**风险：** 高（违反用户决策）
   145	
   146	---
   147	
   148	### 选项3: 要求用户提供File2独有学生的楼栋数据
   149	
   150	**描述：** 暂停Phase 0，要求用户补充116名学生的楼栋/寝室数据
   151	
   152	**优点：**
   153	- 达到100%覆盖率（5946/5946）
   154	- 数据完整性最高
   155	- 所有学生都能正常使用系统
   156	
   157	**缺点：**
   158	- 阻塞Phase 0进度，等待用户提供数据
   159	- 不确定数据提供时间
   160	- 可能暴露File2数据质量问题
   161	
   162	**实施成本：** 低（技术无需修改）
   163	
   164	**风险：** 高（进度不确定）
   165	
   166	---
   167	
   168	## 推荐方案
   169	
   170	**推荐：选项1（接受98%覆盖率）+ 后续改进路径**
   171	
   172	### 理由
   173	
   174	1. **业务现实：** File2独有的116名学生确实缺少楼栋数据，这是数据源限制而非技术问题
   175	2. **影响范围可控：** 仅影响1.95%的学生（116/5946）
   176	3. **辅导员路由完整：** 100%覆盖率已达成，第二级审批无阻塞
   177	4. **进度考虑：** 避免长期阻塞，允许主流程（5830人）正常进行
   178	5. **符合用户决策：** 用户明确要求导入File2独有学生（决策3），不应该回退
   179	
   180	### 实施步骤
   181	
   182	**短期（立即执行）：**
   183	
   184	1. 修改Phase 0门禁标准：
   185	   - 原标准：100%路由覆盖率
   186	   - 新标准：File1学生100%覆盖率（5830/5830）+ 辅导员路由100%覆盖率（5946/5946）
   187	   
   188	2. 更新文档说明：
   189	   - 在`docs/用户需求最终确认与实施方案.md`中记录此决策
   190	   - 在Task 0.5验证结果中标注：98.0%宿管员覆盖率（File1学生100%，File2独有学生0%）
   191	   
   192	3. 记录已知限制：
   193	   - 116名File2独有学生暂时无法使用系统
   194	   - 需要用户后续提供楼栋数据
   195	   
   196	4. 通过Phase 0验证，进入Phase 1-5实施
   197	
   198	**中期（Phase 1-5实施中）：**
   199	
   200	5. 与用户沟通116名学生情况，确认：
   201	   - 这些学生是否需要使用系统？
   202	   - 用户是否能提供楼栋数据？
   203	   - 预计提供时间？
   204	
   205	**长期（系统上线后）：**
   206	
   207	6. 如用户提供116名学生楼栋数据：
   208	   - 更新File5数据
   209	   - 重新导入这116名学生
   210	   - 达到100%完整覆盖率
   211	
   212	---
   213	
   214	## 替代方案（如果推荐方案被拒绝）
   215	
   216	**如果用户坚持100%覆盖率：** 执行选项3，暂停Phase 0，等待用户提供数据
   217	
   218	**如果用户同意排除File2独有学生：** 执行选项2，回退决策3，仅导入5830名File1学生
   219	
   220	---
   221	
   222	## 附件
   223	
   224	**相关文件：**
   225	- Phase 0验证报告：`backend/data/routing_coverage_report.json`
   226	- 合并脚本：`backend/scripts/merge_student_data.py`
   227	- 合并输出：`backend/data/file5_students_merged.csv`（5946行）
   228	- 用户决策文档：`.omc/collaboration/artifacts/20260605-user-business-decisions.md`
   229	
   230	**数据快照：**
   231	- File1学生：5830人（100%有楼栋数据）
   232	- File2独有学生：116人（0%有楼栋数据）
   233	- 总计：5946人
   234	- 宿管员覆盖率：98.0%（5830/5946）
   235	- 辅导员覆盖率：100.0%（5946/5946）
   236	
   237	---
   238	
   239	**分析完成时间：** 2026-06-05T19:57:00Z  
   240	**下一步：** 等待Codex审查和用户决策

codex
前序共识明确把“100%覆盖”设为数据门禁，且用户的新决策只是“导入116人”，并没有等价授权这些人上线后不可提交。我的评审倾向会是：可以分阶段推进，但不能把98%直接改写成验收通过，除非有显式降级与兜底策略。
exec
/bin/bash -lc "rtk sed -n '1,260p' backend/scripts/validate_routing_coverage.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
#!/usr/bin/env python3
"""
Validate routing coverage for all students.
Ensures every student can be routed to dorm manager and counselor.
"""
import csv
import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))
from normalize_colleges import normalize_college_name


def load_students(file5_path: str) -> List[dict]:
    """Load File5 student data."""
    students = []
    with open(file5_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        students = list(reader)
    return students


def load_dorm_managers(file3_path: str) -> Dict[str, List[str]]:
    """
    Load File3 dorm manager data.
    Returns: {building_name: [manager_ids]}
    """
    building_managers = defaultdict(list)

    with open(file3_path, 'r', encoding='utf-8') as f:
        next(f)  # Skip title row
        reader = csv.DictReader(f)
        for row in reader:
            building = row['楼栋号'].strip()
            manager_id = row['职工号'].strip()

            if manager_id and manager_id != '暂未申请':
                building_managers[building].append(manager_id)

    return dict(building_managers)


def load_counselors(file4_path: str) -> Dict[str, str]:
    """
    Load File4 counselor data.
    Returns: {department: counselor_id}
    """
    dept_counselors = {}

    with open(file4_path, 'r', encoding='utf-8') as f:
        next(f)  # Skip title row
        reader = csv.DictReader(f)
        for row in reader:
            department_raw = row['学院'].strip()
            counselor_id = row['职工号'].strip()

            if counselor_id:
                try:
                    # Normalize department name to match File5
                    department_norm = normalize_college_name(department_raw)
                    dept_counselors[department_norm] = counselor_id
                except ValueError:
                    # Skip departments that can't be normalized
                    continue

    return dept_counselors


def validate_routing(file5_path: str, file3_path: str, file4_path: str) -> dict:
    """
    Validate that all students can be routed to approvers.

    Returns validation report with coverage statistics.
    """
    students = load_students(file5_path)
    building_managers = load_dorm_managers(file3_path)
    dept_counselors = load_counselors(file4_path)

    report = {
        'total_students': len(students),
        'dorm_manager_coverage': 0,
        'counselor_coverage': 0,
        'fully_routable': 0,
        'missing_dorm_manager': [],
        'missing_counselor': [],
        'unroutable_students': []
    }

    for student in students:
        user_id = student['user_id']
        name = student['name']
        building = student['building_name']
        department = student['department']

        # Check dorm manager routing
        has_dorm_manager = building in building_managers
        if has_dorm_manager:
            report['dorm_manager_coverage'] += 1
        else:
            report['missing_dorm_manager'].append({
                'user_id': user_id,
                'name': name,
                'building': building
            })

        # Check counselor routing
        has_counselor = department in dept_counselors
        if has_counselor:
            report['counselor_coverage'] += 1
        else:
            report['missing_counselor'].append({
                'user_id': user_id,
                'name': name,
                'department': department
            })

        # Check full routing
        if has_dorm_manager and has_counselor:
            report['fully_routable'] += 1
        else:
            report['unroutable_students'].append({
                'user_id': user_id,
                'name': name,
                'building': building,
                'department': department,
                'missing': {
                    'dorm_manager': not has_dorm_manager,
                    'counselor': not has_counselor
                }
            })

    # Calculate percentages
    total = report['total_students']
    report['dorm_manager_coverage_pct'] = (report['dorm_manager_coverage'] / total * 100) if total > 0 else 0
    report['counselor_coverage_pct'] = (report['counselor_coverage'] / total * 100) if total > 0 else 0
    report['fully_routable_pct'] = (report['fully_routable'] / total * 100) if total > 0 else 0

    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Validate routing coverage')
    parser.add_argument('--file5', required=True, help='Path to File5 (merged students)')
    parser.add_argument('--file3', required=True, help='Path to File3 (dorm managers)')
    parser.add_argument('--file4', required=True, help='Path to File4 (counselors)')
    parser.add_argument('--report', help='Optional JSON report output path')

    args = parser.parse_args()

    print("Validating routing coverage...")
    report = validate_routing(args.file5, args.file3, args.file4)

    print("\n=== Routing Coverage Report ===")
    print(f"Total students: {report['total_students']}")
    print(f"\nDorm manager coverage: {report['dorm_manager_coverage']}/{report['total_students']} ({report['dorm_manager_coverage_pct']:.1f}%)")
    print(f"Counselor coverage: {report['counselor_coverage']}/{report['total_students']} ({report['counselor_coverage_pct']:.1f}%)")
    print(f"Fully routable: {report['fully_routable']}/{report['total_students']} ({report['fully_routable_pct']:.1f}%)")

    # Gate check
    if report['fully_routable_pct'] == 100.0:
        print("\n✓ PASS: 100% routing coverage achieved")
        exit_code = 0
    else:
        print(f"\n✗ FAIL: {len(report['unroutable_students'])} students cannot be routed")
        print("\nMissing dorm managers for buildings:")
        missing_buildings = set(s['building'] for s in report['missing_dorm_manager'])
        for building in sorted(missing_buildings):
            count = sum(1 for s in report['missing_dorm_manager'] if s['building'] == building)
            print(f"  - {building}: {count} students")

        print("\nMissing counselors for departments:")
        missing_depts = set(s['department'] for s in report['missing_counselor'])
        for dept in sorted(missing_depts):
            count = sum(1 for s in report['missing_counselor'] if s['department'] == dept)
            print(f"  - {dept}: {count} students")

        exit_code = 1

    if args.report:
        with open(args.report, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\nFull report saved to: {args.report}")

    exit(exit_code)

exec
/bin/bash -lc 'rtk rg -n "dorm_manager|pending_dorm|building_name|student_building|approver|Approval|submit|route" backend/apps backend/scripts docs/用户需求最终确认与实施方案.md .omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md .omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:51:### P0-2: Multi-Approver vs Single Approval Model
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:53:**Codex finding:** Document suggests "any dorm manager can approve" but Approval.approver is single FK. No group approval model.
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:55:**Root cause analysis:** Correct. Current model (backend/apps/approvals/models.py:14-22, backend/apps/applications/views.py:172-179) creates one Approval per approver. Multi-approver requires either approval group model or selection algorithm.
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:58:- Document updated to require File3 provide `primary_dorm_manager_user_id` per building
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:64:- Maintains clean Approval.approver FK constraint
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:86:    # - building_name → dorm_manager exists?
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:99:3. Approval pass routing refactor (apps/approvals/views.py:149-174)
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:116:**Acknowledged:** File1/File2 count discrepancy (155 vs 271+116) needs reconciliation in merge report. Status machine naming (`PENDING` vs `pending_dorm_manager`) should align with existing codebase conventions.
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:125:**Acknowledged:** Application needs snapshot fields (`student_building_name`, `student_department`) to preserve routing context even if User data changes. College/building normalization maps required before import.
.omc/collaboration/artifacts/20260605-claude-response-implementation-plan-review.md:164:- Validates: building → dorm_manager, department → counselor
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:36:   - 证据：当前 `Approval.approver` 是单个用户外键；创建申请时只创建一个宿管审批记录。见 `backend/apps/approvals/models.py:14-22`, `backend/apps/applications/views.py:172-179`。方案中的 `return dorm_managers` 没有定义如何落到审批记录、权限过滤、重复审批和通知。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:38:   - 建议修正：MVP 不要实现“任一人可审批”的组任务，除非增加 group approval 模型。更现实的 P0 修正是要求 File3 或映射表生成一个 `primary_dorm_manager_user_id`，每栋楼唯一主责宿管员；其他宿管员作为后续代理/备份扩展。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:55:   - 证据：现有状态是 `pending_dorm_manager / pending_counselor / pending_dean / approved / rejected`，不是文档里的 `PENDING / DORM_MANAGER_APPROVED / COUNSELOR_APPROVED / COMPLETED`。见 `backend/apps/applications/models.py:6-12`。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:56:   - 建议修正：最终状态应继续使用 API 现有风格，例如 `pending_dorm_manager -> pending_counselor -> approved`。删除或迁移 `pending_dean`，并补充历史数据迁移规则。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:65:   - 问题：如果只从 `User.department/building_name` 动态读取，学生学院或宿管映射更新后，历史申请的可见范围和审批追溯会变化。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:66:   - 建议修正：`Application` 增加申请时快照字段：`student_building_name`、`student_room_number`、`student_department`、可选 `route_version`。`Approval` 已保存审批人和姓名，可保留。
.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md:76:   - 建议修正：新增或重写导入命令，不要在文档里直接使用不存在的 `import_students/import_counselors/import_dorm_managers` 命令名，除非 Phase 2 明确包含这些命令实现。
docs/用户需求最终确认与实施方案.md:98:- ✓ 当前系统已支持（Application + Approval模型）
docs/用户需求最终确认与实施方案.md:110:| 宿管员 (dorm_manager) | 第一次审批（按楼栋） | 只看自己负责楼栋的申请 |
docs/用户需求最终确认与实施方案.md:182:- 当前Approval.approver是单用户外键
docs/用户需求最终确认与实施方案.md:188:- File3或映射表提供`primary_dorm_manager_user_id`
docs/用户需求最终确认与实施方案.md:244:building_name  # 楼栋名称（File1） - 第一次审批路由键
docs/用户需求最终确认与实施方案.md:260:role = 'dorm_manager'
docs/用户需求最终确认与实施方案.md:305:def get_approver(application):
docs/用户需求最终确认与实施方案.md:308:        return class_mapping.dorm_manager
docs/用户需求最终确认与实施方案.md:315:def get_approver(application):
docs/用户需求最终确认与实施方案.md:318:        building = application.student.building_name
docs/用户需求最终确认与实施方案.md:319:        dorm_managers = DormManager.objects.filter(building=building)
docs/用户需求最终确认与实施方案.md:320:        return dorm_managers  # 任一可审批，或按选主规则
docs/用户需求最终确认与实施方案.md:410:- 每栋楼必须指定1个`primary_dorm_manager_user_id`
docs/用户需求最终确认与实施方案.md:412:- 输出：`file3_dorm_managers_with_primary.csv`
docs/用户需求最终确认与实施方案.md:420:    # - building_name能找到primary dorm manager
docs/用户需求最终确认与实施方案.md:461:- `file3_dorm_managers.csv` - 宿管员数据（33楼栋）
docs/用户需求最终确认与实施方案.md:472:- 创建 `BuildingApprovalRouter` - 楼栋→宿管员路由
docs/用户需求最终确认与实施方案.md:473:- 创建 `DepartmentApprovalRouter` - 学院→辅导员路由
docs/用户需求最终确认与实施方案.md:483:- 确保 `Student.building_name` 和 `Student.department` 非空
docs/用户需求最终确认与实施方案.md:500:python manage.py import_dorm_managers file3_dorm_managers.csv
docs/用户需求最终确认与实施方案.md:564:    dorm_manager = models.ForeignKey(User, on_delete=models.CASCADE)
docs/用户需求最终确认与实施方案.md:572:def get_dorm_manager(application):
docs/用户需求最终确认与实施方案.md:573:    building = application.student.building_name
docs/用户需求最终确认与实施方案.md:581:    return mapping.dorm_manager
docs/用户需求最终确认与实施方案.md:652:- ⏳ `file3_dorm_managers.csv` - 宿管员数据
backend/scripts/merge_student_data.py:136:                'building_name': building,
backend/scripts/merge_student_data.py:167:                'building_name': '',  # Not in File2
backend/scripts/validate_routing_coverage.py:4:Ensures every student can be routed to dorm manager and counselor.
backend/scripts/validate_routing_coverage.py:27:def load_dorm_managers(file3_path: str) -> Dict[str, List[str]]:
backend/scripts/validate_routing_coverage.py:30:    Returns: {building_name: [manager_ids]}
backend/scripts/validate_routing_coverage.py:75:    Validate that all students can be routed to approvers.
backend/scripts/validate_routing_coverage.py:80:    building_managers = load_dorm_managers(file3_path)
backend/scripts/validate_routing_coverage.py:85:        'dorm_manager_coverage': 0,
backend/scripts/validate_routing_coverage.py:88:        'missing_dorm_manager': [],
backend/scripts/validate_routing_coverage.py:96:        building = student['building_name']
backend/scripts/validate_routing_coverage.py:100:        has_dorm_manager = building in building_managers
backend/scripts/validate_routing_coverage.py:101:        if has_dorm_manager:
backend/scripts/validate_routing_coverage.py:102:            report['dorm_manager_coverage'] += 1
backend/scripts/validate_routing_coverage.py:104:            report['missing_dorm_manager'].append({
backend/scripts/validate_routing_coverage.py:122:        if has_dorm_manager and has_counselor:
backend/scripts/validate_routing_coverage.py:131:                    'dorm_manager': not has_dorm_manager,
backend/scripts/validate_routing_coverage.py:138:    report['dorm_manager_coverage_pct'] = (report['dorm_manager_coverage'] / total * 100) if total > 0 else 0
backend/scripts/validate_routing_coverage.py:161:    print(f"\nDorm manager coverage: {report['dorm_manager_coverage']}/{report['total_students']} ({report['dorm_manager_coverage_pct']:.1f}%)")
backend/scripts/validate_routing_coverage.py:170:        print(f"\n✗ FAIL: {len(report['unroutable_students'])} students cannot be routed")
backend/scripts/validate_routing_coverage.py:172:        missing_buildings = set(s['building'] for s in report['missing_dorm_manager'])
backend/scripts/validate_routing_coverage.py:174:            count = sum(1 for s in report['missing_dorm_manager'] if s['building'] == building)
backend/apps/approvals/validators.py:5:    'dorm_manager': ApplicationStatus.PENDING_DORM_MANAGER,
backend/apps/approvals/admin.py:2:from .models import Approval
backend/apps/approvals/admin.py:5:@admin.register(Approval)
backend/apps/approvals/admin.py:6:class ApprovalAdmin(admin.ModelAdmin):
backend/apps/approvals/admin.py:7:    list_display = ['approval_id', 'application', 'step', 'approver', 'decision', 'decided_at']
backend/apps/approvals/admin.py:9:    search_fields = ['approval_id', 'application__application_id', 'approver__user_id']
backend/apps/approvals/pagination.py:5:class ApprovalLimitOffsetPagination(LimitOffsetPagination):
backend/apps/approvals/migrations/0003_alter_approval_step.py:16:            field=models.CharField(choices=[('dorm_manager', '宿管员'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20),
backend/apps/approvals/migrations/0002_initial.py:20:            name='approver',
backend/apps/notifications/services.py:12:from apps.approvals.models import ApprovalDecision
backend/apps/notifications/services.py:17:def notify_application_submitted(application, approval):
backend/apps/notifications/services.py:19:    Create notification for counselor when student submits application.
backend/apps/notifications/services.py:32:        recipient=approval.approver,
backend/apps/notifications/services.py:49:        approval: Approval instance with decision
backend/apps/notifications/services.py:54:    approver_role_map = {
backend/apps/notifications/services.py:55:        "dorm_manager": "宿管员",
backend/apps/notifications/services.py:58:    approver_role = approver_role_map.get(approval.step, "审批人")
backend/apps/notifications/services.py:60:    if approval.decision == ApprovalDecision.APPROVED:
backend/apps/notifications/services.py:62:        message = f"您的离校申请已通过{approver_role}审批。"
backend/apps/notifications/services.py:66:        message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
backend/apps/notifications/services.py:75:            'actor': approval.approver,
backend/apps/notifications/services.py:93:    from apps.approvals.models import Approval
backend/apps/notifications/services.py:98:    dorm_manager_threshold = now - timedelta(days=2)
backend/apps/notifications/services.py:101:    pending_approvals = Approval.objects.filter(
backend/apps/notifications/services.py:102:        decision=ApprovalDecision.PENDING
backend/apps/notifications/services.py:103:    ).select_related('approver', 'application__student')
backend/apps/notifications/services.py:110:        threshold = counselor_threshold if approval.step == 'counselor' else dorm_manager_threshold
backend/apps/notifications/services.py:122:                'approver': approval.approver.name,
backend/apps/notifications/services.py:128:                recipient=approval.approver,
backend/apps/notifications/services.py:143:                    'approver': approval.approver.name,
backend/apps/approvals/migrations/0001_initial.py:17:            name='Approval',
backend/apps/approvals/migrations/0001_initial.py:21:                ('approver_name', models.CharField(max_length=100)),
backend/apps/approvals/serializers.py:2:from .models import Approval
backend/apps/approvals/serializers.py:5:class ApprovalListSerializer(serializers.ModelSerializer):
backend/apps/approvals/serializers.py:8:    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
backend/apps/approvals/serializers.py:11:        model = Approval
backend/apps/approvals/serializers.py:12:        fields = ['approval_id', 'application_id', 'step', 'approver_id',
backend/apps/approvals/serializers.py:13:                  'approver_name', 'decision', 'created_at']
backend/apps/approvals/serializers.py:15:                            'approver_id', 'approver_name', 'decision', 'created_at']
backend/apps/approvals/serializers.py:18:class ApprovalSerializer(serializers.ModelSerializer):
backend/apps/approvals/serializers.py:20:    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
backend/apps/approvals/serializers.py:23:        model = Approval
backend/apps/approvals/serializers.py:24:        fields = ['approval_id', 'application_id', 'step', 'approver_id',
backend/apps/approvals/serializers.py:25:                  'approver_name', 'decision', 'comment', 'decided_at']
backend/apps/approvals/serializers.py:27:                            'approver_id', 'approver_name', 'decision', 'decided_at']
backend/apps/approvals/serializers.py:30:class ApprovalActionSerializer(serializers.Serializer):
backend/apps/approvals/serializers.py:34:class ApprovalListResponseSerializer(serializers.Serializer):
backend/apps/approvals/serializers.py:37:    results = ApprovalListSerializer(many=True)
backend/apps/approvals/tests/test_rejection_flow.py:9:from apps.approvals.models import ApprovalDecision, ApprovalStep
backend/apps/approvals/tests/test_rejection_flow.py:33:        self.dorm_manager = User.objects.create_user(
backend/apps/approvals/tests/test_rejection_flow.py:43:            dorm_manager=self.dorm_manager,
backend/apps/approvals/tests/test_rejection_flow.py:44:            dorm_manager_name='宿管员',
backend/apps/approvals/tests/test_rejection_flow.py:50:    def _submit_application(self):
backend/apps/approvals/tests/test_rejection_flow.py:51:        # Student login and submit
backend/apps/approvals/tests/test_rejection_flow.py:66:    def _approve_dorm_manager_step(self, application):
backend/apps/approvals/tests/test_rejection_flow.py:71:        dorm_manager_token = response.data['access_token']
backend/apps/approvals/tests/test_rejection_flow.py:73:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/approvals/tests/test_rejection_flow.py:75:        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dorm_manager_token}')
backend/apps/approvals/tests/test_rejection_flow.py:76:        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/approve/', {
backend/apps/approvals/tests/test_rejection_flow.py:81:    def test_dorm_manager_rejection(self):
backend/apps/approvals/tests/test_rejection_flow.py:83:        application_id = self._submit_application()
backend/apps/approvals/tests/test_rejection_flow.py:89:        dorm_manager_token = response.data['access_token']
backend/apps/approvals/tests/test_rejection_flow.py:92:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/approvals/tests/test_rejection_flow.py:94:        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dorm_manager_token}')
backend/apps/approvals/tests/test_rejection_flow.py:95:        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/reject/', {
backend/apps/approvals/tests/test_rejection_flow.py:99:        self.assertEqual(response.data['decision'], ApprovalDecision.REJECTED)
backend/apps/approvals/tests/test_rejection_flow.py:106:        application_id = self._submit_application()
backend/apps/approvals/tests/test_rejection_flow.py:108:        self._approve_dorm_manager_step(application)
backend/apps/approvals/tests/test_rejection_flow.py:118:        counselor_approval = application.approvals.get(step=ApprovalStep.COUNSELOR)
backend/apps/approvals/tests/test_rejection_flow.py:125:        self.assertEqual(response.data['decision'], ApprovalDecision.REJECTED)
backend/apps/approvals/tests/test_permissions.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/approvals/tests/test_permissions.py:10:class ApprovalPermissionsTestCase(TestCase):
backend/apps/approvals/tests/test_permissions.py:41:        self.dorm_manager1 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:47:        self.dorm_manager2 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:69:            dorm_manager=self.dorm_manager1,
backend/apps/approvals/tests/test_permissions.py:70:            dorm_manager_name='宿管员1',
backend/apps/approvals/tests/test_permissions.py:77:            dorm_manager=self.dorm_manager2,
backend/apps/approvals/tests/test_permissions.py:78:            dorm_manager_name='宿管员2',
backend/apps/approvals/tests/test_permissions.py:96:        self.approval1 = Approval.objects.create(
backend/apps/approvals/tests/test_permissions.py:99:            step=ApprovalStep.COUNSELOR,
backend/apps/approvals/tests/test_permissions.py:100:            approver=self.counselor1,
backend/apps/approvals/tests/test_permissions.py:101:            approver_name='李老师',
backend/apps/approvals/tests/test_permissions.py:102:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_permissions.py:107:    def _create_dorm_manager_approval(self):
backend/apps/approvals/tests/test_permissions.py:110:        return Approval.objects.create(
backend/apps/approvals/tests/test_permissions.py:113:            step=ApprovalStep.DORM_MANAGER,
backend/apps/approvals/tests/test_permissions.py:114:            approver=self.dorm_manager1,
backend/apps/approvals/tests/test_permissions.py:115:            approver_name='宿管员1',
backend/apps/approvals/tests/test_permissions.py:116:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_permissions.py:149:    def test_counselor_cannot_act_on_dorm_manager_step(self):
backend/apps/approvals/tests/test_permissions.py:151:        dorm_manager_approval = self._create_dorm_manager_approval()
backend/apps/approvals/tests/test_permissions.py:155:            f'/api/approvals/{dorm_manager_approval.approval_id}/approve/',
backend/apps/approvals/tests/test_permissions.py:162:    def test_non_assigned_dorm_manager_forbidden(self):
backend/apps/approvals/tests/test_permissions.py:164:        dorm_manager_approval = self._create_dorm_manager_approval()
backend/apps/approvals/tests/test_permissions.py:165:        self.client.force_authenticate(user=self.dorm_manager2)
backend/apps/approvals/tests/test_permissions.py:168:            f'/api/approvals/{dorm_manager_approval.approval_id}/reject/',
backend/apps/approvals/tests/test_list_permissions.py:5:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/approvals/tests/test_list_permissions.py:8:class ApprovalListPermissionTest(TestCase):
backend/apps/approvals/tests/test_list_permissions.py:25:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
backend/apps/approvals/tests/test_list_permissions.py:26:        self.dorm_manager1.set_password('M001')
backend/apps/approvals/tests/test_list_permissions.py:27:        self.dorm_manager1.save()
backend/apps/approvals/tests/test_list_permissions.py:29:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
backend/apps/approvals/tests/test_list_permissions.py:30:        self.dorm_manager2.set_password('M002')
backend/apps/approvals/tests/test_list_permissions.py:31:        self.dorm_manager2.save()
backend/apps/approvals/tests/test_list_permissions.py:53:        self.approval_c1 = Approval.objects.create(
backend/apps/approvals/tests/test_list_permissions.py:56:            step=ApprovalStep.COUNSELOR,
backend/apps/approvals/tests/test_list_permissions.py:57:            approver=self.counselor1,
backend/apps/approvals/tests/test_list_permissions.py:58:            approver_name='辅导员1',
backend/apps/approvals/tests/test_list_permissions.py:59:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_list_permissions.py:62:        self.approval_m1 = Approval.objects.create(
backend/apps/approvals/tests/test_list_permissions.py:65:            step=ApprovalStep.DORM_MANAGER,
backend/apps/approvals/tests/test_list_permissions.py:66:            approver=self.dorm_manager1,
backend/apps/approvals/tests/test_list_permissions.py:67:            approver_name='宿管员1',
backend/apps/approvals/tests/test_list_permissions.py:68:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_list_permissions.py:89:    def test_dorm_manager_sees_only_own_pending_approvals(self):
backend/apps/approvals/tests/test_list_permissions.py:90:        self.client.force_authenticate(user=self.dorm_manager1)
backend/apps/approvals/tests/test_list_permissions.py:96:    def test_dorm_manager_cannot_see_other_dorm_manager_approvals(self):
backend/apps/approvals/tests/test_list_permissions.py:97:        self.client.force_authenticate(user=self.dorm_manager2)
backend/apps/approvals/tests/test_list_permissions.py:115:    def test_decision_all_does_not_leak_cross_approver_data(self):
backend/apps/approvals/tests/test_list_permissions.py:126:        approval_c1_approved = Approval.objects.create(
backend/apps/approvals/tests/test_list_permissions.py:129:            step=ApprovalStep.COUNSELOR,
backend/apps/approvals/tests/test_list_permissions.py:130:            approver=self.counselor1,
backend/apps/approvals/tests/test_list_permissions.py:131:            approver_name='辅导员1',
backend/apps/approvals/tests/test_list_permissions.py:132:            decision=ApprovalDecision.APPROVED
backend/apps/approvals/tests/test_list_permissions.py:145:        approval_c2 = Approval.objects.create(
backend/apps/approvals/tests/test_list_permissions.py:148:            step=ApprovalStep.COUNSELOR,
backend/apps/approvals/tests/test_list_permissions.py:149:            approver=self.counselor2,
backend/apps/approvals/tests/test_list_permissions.py:150:            approver_name='辅导员2',
backend/apps/approvals/tests/test_list_permissions.py:151:            decision=ApprovalDecision.PENDING
backend/apps/attachments/views.py:13:from apps.approvals.models import Approval, ApprovalStep
backend/apps/notifications/models.py:15:    APPLICATION_SUBMITTED = 'application_submitted', '申请已提交'
backend/apps/attachments/tests/test_download.py:8:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/approvals/models.py:6:class ApprovalStep(models.TextChoices):
backend/apps/approvals/models.py:7:    DORM_MANAGER = 'dorm_manager', '宿管员'
backend/apps/approvals/models.py:12:class ApprovalDecision(models.TextChoices):
backend/apps/approvals/models.py:18:class Approval(models.Model):
backend/apps/approvals/models.py:21:    step = models.CharField(max_length=20, choices=ApprovalStep.choices)
backend/apps/approvals/models.py:22:    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approvals')
backend/apps/approvals/models.py:23:    approver_name = models.CharField(max_length=100)
backend/apps/approvals/models.py:24:    decision = models.CharField(max_length=20, choices=ApprovalDecision.choices, default=ApprovalDecision.PENDING)
backend/apps/notifications/tests/test_auto_notifications_api.py:12:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/notifications/tests/test_auto_notifications_api.py:37:        self.dorm_manager = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications_api.py:40:            role='dorm_manager'
backend/apps/notifications/tests/test_auto_notifications_api.py:50:            dorm_manager=self.dorm_manager,
backend/apps/notifications/tests/test_auto_notifications_api.py:51:            dorm_manager_name=self.dorm_manager.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:57:    def test_application_submitted_notification_visible_via_api(self):
backend/apps/notifications/tests/test_auto_notifications_api.py:58:        """Test dorm manager can see APPLICATION_SUBMITTED notification via API after student submits."""
backend/apps/notifications/tests/test_auto_notifications_api.py:59:        # Student submits application (triggers notification)
backend/apps/notifications/tests/test_auto_notifications_api.py:68:        self.client.force_authenticate(user=self.dorm_manager)
backend/apps/notifications/tests/test_auto_notifications_api.py:74:        self.assertEqual(notifications[0]['type'], 'application_submitted')
backend/apps/notifications/tests/test_auto_notifications_api.py:91:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications_api.py:94:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications_api.py:95:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications_api.py:96:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:97:            decision=ApprovalDecision.PENDING
backend/apps/notifications/tests/test_auto_notifications_api.py:133:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications_api.py:136:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications_api.py:137:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications_api.py:138:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:139:            decision=ApprovalDecision.PENDING
backend/apps/notifications/tests/test_auto_notifications_api.py:178:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications_api.py:181:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications_api.py:182:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications_api.py:183:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:184:            decision=ApprovalDecision.PENDING
backend/apps/notifications/tests/test_auto_notifications_api.py:213:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications_api.py:216:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications_api.py:217:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications_api.py:218:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:219:            decision=ApprovalDecision.APPROVED  # Already approved
backend/apps/notifications/tests/test_auto_notifications_api.py:246:        # Student tries to submit application (should fail with 422 dorm blocked)
backend/apps/notifications/tests/test_auto_notifications_api.py:262:            recipient=self.dorm_manager,
backend/apps/notifications/tests/test_auto_notifications_api.py:263:            type='application_submitted'
backend/apps/notifications/tests/test_timeout_warnings.py:8:from apps.approvals.models import Approval, ApprovalDecision
backend/apps/notifications/tests/test_timeout_warnings.py:13:class ApprovalTimeoutWarningTests(TestCase):
backend/apps/notifications/tests/test_timeout_warnings.py:27:        self.dorm_manager = User.objects.create_user(
backend/apps/notifications/tests/test_timeout_warnings.py:30:            role='dorm_manager'
backend/apps/notifications/tests/test_timeout_warnings.py:40:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_timeout_warnings.py:43:            approver=self.counselor
backend/apps/notifications/tests/test_timeout_warnings.py:56:    def test_dorm_manager_timeout_2_days(self):
backend/apps/notifications/tests/test_timeout_warnings.py:63:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_timeout_warnings.py:65:            step='dorm_manager',
backend/apps/notifications/tests/test_timeout_warnings.py:66:            approver=self.dorm_manager
backend/apps/notifications/tests/test_timeout_warnings.py:76:            recipient=self.dorm_manager
backend/apps/notifications/tests/test_timeout_warnings.py:86:        Approval.objects.create(
backend/apps/notifications/tests/test_timeout_warnings.py:89:            approver=self.counselor
backend/apps/notifications/tests/test_timeout_warnings.py:104:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_timeout_warnings.py:107:            approver=self.counselor,
backend/apps/notifications/tests/test_timeout_warnings.py:108:            decision=ApprovalDecision.APPROVED
backend/apps/notifications/tests/test_timeout_warnings.py:125:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_timeout_warnings.py:128:            approver=self.counselor
backend/apps/notifications/tests/test_timeout_warnings.py:148:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_timeout_warnings.py:151:            approver=self.counselor
backend/apps/approvals/tests/test_state_machine.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/approvals/tests/test_state_machine.py:10:class ApprovalStateMachineTestCase(TestCase):
backend/apps/approvals/tests/test_state_machine.py:30:        self.dorm_manager = User.objects.create_user(
backend/apps/approvals/tests/test_state_machine.py:48:            dorm_manager=self.dorm_manager,
backend/apps/approvals/tests/test_state_machine.py:49:            dorm_manager_name='宿管员',
backend/apps/approvals/tests/test_state_machine.py:67:        self.approval = Approval.objects.create(
backend/apps/approvals/tests/test_state_machine.py:70:            step=ApprovalStep.COUNSELOR,
backend/apps/approvals/tests/test_state_machine.py:71:            approver=self.counselor,
backend/apps/approvals/tests/test_state_machine.py:72:            approver_name='李老师',
backend/apps/approvals/tests/test_state_machine.py:73:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_state_machine.py:136:    def test_dorm_manager_step_requires_pending_dorm_manager_status(self):
backend/apps/approvals/tests/test_state_machine.py:140:        dorm_manager_approval = Approval.objects.create(
backend/apps/approvals/tests/test_state_machine.py:143:            step=ApprovalStep.DORM_MANAGER,
backend/apps/approvals/tests/test_state_machine.py:144:            approver=self.dorm_manager,
backend/apps/approvals/tests/test_state_machine.py:145:            approver_name='宿管员',
backend/apps/approvals/tests/test_state_machine.py:146:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_state_machine.py:148:        self.client.force_authenticate(user=self.dorm_manager)
backend/apps/approvals/tests/test_state_machine.py:151:            f'/api/approvals/{dorm_manager_approval.approval_id}/approve/',
backend/apps/approvals/tests/test_state_machine.py:156:            f'/api/approvals/{dorm_manager_approval.approval_id}/reject/',
backend/apps/approvals/views.py:9:from .models import Approval, ApprovalDecision, ApprovalStep
backend/apps/approvals/views.py:10:from .serializers import ApprovalSerializer, ApprovalActionSerializer, ApprovalListSerializer, ApprovalListResponseSerializer
backend/apps/approvals/views.py:11:from .pagination import ApprovalLimitOffsetPagination
backend/apps/approvals/views.py:30:        200: ApprovalListResponseSerializer,
backend/apps/approvals/views.py:47:    # 宿管员: 只看自己的dorm_manager审批
backend/apps/approvals/views.py:49:        queryset = Approval.objects.filter(
backend/apps/approvals/views.py:50:            approver=user,
backend/apps/approvals/views.py:51:            step=ApprovalStep.DORM_MANAGER
backend/apps/approvals/views.py:52:        ).select_related('application', 'approver')
backend/apps/approvals/views.py:56:        queryset = Approval.objects.filter(
backend/apps/approvals/views.py:57:            approver=user,
backend/apps/approvals/views.py:58:            step=ApprovalStep.COUNSELOR
backend/apps/approvals/views.py:59:        ).select_related('application', 'approver')
backend/apps/approvals/views.py:63:        queryset = Approval.objects.all().select_related('application', 'approver')
backend/apps/approvals/views.py:80:    paginator = ApprovalLimitOffsetPagination()
backend/apps/approvals/views.py:84:    serializer = ApprovalListSerializer(page, many=True)
backend/apps/approvals/views.py:93:    request=ApprovalActionSerializer,
backend/apps/approvals/views.py:95:        200: ApprovalSerializer,
backend/apps/approvals/views.py:108:        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
backend/apps/approvals/views.py:109:    except Approval.DoesNotExist:
backend/apps/approvals/views.py:114:    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
backend/apps/approvals/views.py:117:    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
backend/apps/approvals/views.py:120:    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
backend/apps/approvals/views.py:124:    if approval.approver_id != user.user_id:
backend/apps/approvals/views.py:128:    if approval.decision != ApprovalDecision.PENDING:
backend/apps/approvals/views.py:136:    serializer = ApprovalActionSerializer(data=request.data)
backend/apps/approvals/views.py:141:    approval.decision = ApprovalDecision.APPROVED
backend/apps/approvals/views.py:149:    if approval.step == ApprovalStep.DORM_MANAGER:
backend/apps/approvals/views.py:151:        existing_counselor_approval = Approval.objects.filter(
backend/apps/approvals/views.py:153:            step=ApprovalStep.COUNSELOR
backend/apps/approvals/views.py:167:        Approval.objects.create(
backend/apps/approvals/views.py:170:            step=ApprovalStep.COUNSELOR,
backend/apps/approvals/views.py:171:            approver=class_mapping.counselor,
backend/apps/approvals/views.py:172:            approver_name=class_mapping.counselor_name,
backend/apps/approvals/views.py:173:            decision=ApprovalDecision.PENDING
backend/apps/approvals/views.py:175:    elif approval.step == ApprovalStep.COUNSELOR:
backend/apps/approvals/views.py:177:        existing_dean_approval = Approval.objects.filter(
backend/apps/approvals/views.py:179:            step=ApprovalStep.DEAN
backend/apps/approvals/views.py:197:        Approval.objects.create(
backend/apps/approvals/views.py:200:            step=ApprovalStep.DEAN,
backend/apps/approvals/views.py:201:            approver=dean_user,
backend/apps/approvals/views.py:202:            approver_name=dean_user.name,
backend/apps/approvals/views.py:203:            decision=ApprovalDecision.PENDING
backend/apps/approvals/views.py:205:    elif approval.step == ApprovalStep.DEAN:
backend/apps/approvals/views.py:209:    return Response(ApprovalSerializer(approval).data)
backend/apps/approvals/views.py:216:    request=ApprovalActionSerializer,
backend/apps/approvals/views.py:218:        200: ApprovalSerializer,
backend/apps/approvals/views.py:231:        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
backend/apps/approvals/views.py:232:    except Approval.DoesNotExist:
backend/apps/approvals/views.py:237:    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
backend/apps/approvals/views.py:240:    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
backend/apps/approvals/views.py:243:    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
backend/apps/approvals/views.py:247:    if approval.approver_id != user.user_id:
backend/apps/approvals/views.py:251:    if approval.decision != ApprovalDecision.PENDING:
backend/apps/approvals/views.py:259:    serializer = ApprovalActionSerializer(data=request.data)
backend/apps/approvals/views.py:264:    approval.decision = ApprovalDecision.REJECTED
backend/apps/approvals/views.py:275:    return Response(ApprovalSerializer(approval).data)
backend/apps/users/class_mapping.py:7:    dorm_manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='managed_dorms', null=True, blank=True)
backend/apps/users/class_mapping.py:8:    dorm_manager_name = models.CharField(max_length=100, null=True, blank=True)
backend/apps/notifications/tests/test_auto_notifications.py:5:- Student submits application (APPLICATION_SUBMITTED)
backend/apps/notifications/tests/test_auto_notifications.py:6:- Approval is approved (APPROVAL_APPROVED)
backend/apps/notifications/tests/test_auto_notifications.py:7:- Approval is rejected (APPROVAL_REJECTED)
backend/apps/notifications/tests/test_auto_notifications.py:15:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/notifications/tests/test_auto_notifications.py:17:from apps.notifications.services import notify_application_submitted, notify_approval_decided
backend/apps/notifications/tests/test_auto_notifications.py:38:        self.dorm_manager = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications.py:41:            role='dorm_manager'
backend/apps/notifications/tests/test_auto_notifications.py:44:    def test_application_submitted_notification(self):
backend/apps/notifications/tests/test_auto_notifications.py:56:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications.py:59:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications.py:60:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications.py:61:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:62:            decision=ApprovalDecision.PENDING
backend/apps/notifications/tests/test_auto_notifications.py:65:        notification, created = notify_application_submitted(application, approval)
backend/apps/notifications/tests/test_auto_notifications.py:70:        self.assertEqual(notification.type, 'application_submitted')
backend/apps/notifications/tests/test_auto_notifications.py:88:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications.py:91:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications.py:92:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications.py:93:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:94:            decision=ApprovalDecision.APPROVED
backend/apps/notifications/tests/test_auto_notifications.py:107:    def test_approval_approved_notification_dorm_manager(self):
backend/apps/notifications/tests/test_auto_notifications.py:119:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications.py:122:            step=ApprovalStep.DORM_MANAGER,
backend/apps/notifications/tests/test_auto_notifications.py:123:            approver=self.dorm_manager,
backend/apps/notifications/tests/test_auto_notifications.py:124:            approver_name=self.dorm_manager.name,
backend/apps/notifications/tests/test_auto_notifications.py:125:            decision=ApprovalDecision.APPROVED
backend/apps/notifications/tests/test_auto_notifications.py:132:        self.assertEqual(notification.actor, self.dorm_manager)
backend/apps/notifications/tests/test_auto_notifications.py:148:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications.py:151:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications.py:152:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications.py:153:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:154:            decision=ApprovalDecision.REJECTED,
backend/apps/notifications/tests/test_auto_notifications.py:167:    def test_idempotency_application_submitted(self):
backend/apps/notifications/tests/test_auto_notifications.py:179:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications.py:182:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications.py:183:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications.py:184:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:185:            decision=ApprovalDecision.PENDING
backend/apps/notifications/tests/test_auto_notifications.py:188:        notification1, created1 = notify_application_submitted(application, approval)
backend/apps/notifications/tests/test_auto_notifications.py:191:        notification2, created2 = notify_application_submitted(application, approval)
backend/apps/notifications/tests/test_auto_notifications.py:199:            type='application_submitted'
backend/apps/notifications/tests/test_auto_notifications.py:214:        approval = Approval.objects.create(
backend/apps/notifications/tests/test_auto_notifications.py:217:            step=ApprovalStep.COUNSELOR,
backend/apps/notifications/tests/test_auto_notifications.py:218:            approver=self.counselor,
backend/apps/notifications/tests/test_auto_notifications.py:219:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:220:            decision=ApprovalDecision.APPROVED
backend/apps/notifications/migrations/0001_initial.py:22:                ('type', models.CharField(choices=[('application_submitted', '申请已提交'), ('approval_approved', '审批通过'), ('approval_rejected', '审批驳回'), ('dorm_clearance_blocked', '宿舍清退阻断'), ('approval_timeout_warning', '审批超时提醒')], max_length=50, verbose_name='通知类型')),
backend/apps/notifications/management/commands/send_approval_timeout_warnings.py:31:                    f"  - Approval {warning['approval_id']}: "
backend/apps/notifications/management/commands/send_approval_timeout_warnings.py:32:                    f"{warning['approver']} ({warning['days']} days)"
backend/apps/notifications/migrations/0002_alter_notification_type.py:16:            field=models.CharField(choices=[('application_submitted', '申请已提交'), ('approval_approved', '审批通过'), ('approval_rejected', '审批驳回'), ('approval_timeout_warning', '审批超时提醒')], max_length=50, verbose_name='通知类型'),
backend/apps/users/models.py:7:    DORM_MANAGER = 'dorm_manager', '宿管员'
backend/apps/applications/tests/test_application_flow.py:9:from apps.approvals.models import ApprovalDecision, ApprovalStep
backend/apps/applications/tests/test_application_flow.py:34:        self.dorm_manager = User.objects.create_user(
backend/apps/applications/tests/test_application_flow.py:51:            dorm_manager=self.dorm_manager,
backend/apps/applications/tests/test_application_flow.py:52:            dorm_manager_name='宿管员',
backend/apps/applications/tests/test_application_flow.py:84:        dorm_manager_token = response.data['access_token']
backend/apps/applications/tests/test_application_flow.py:88:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
backend/apps/applications/tests/test_application_flow.py:90:        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dorm_manager_token}')
backend/apps/applications/tests/test_application_flow.py:91:        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/approve/', {
backend/apps/applications/tests/test_application_flow.py:95:        self.assertEqual(response.data['decision'], ApprovalDecision.APPROVED)
backend/apps/applications/tests/test_application_flow.py:108:        counselor_approval = application.approvals.get(step=ApprovalStep.COUNSELOR)
backend/apps/applications/tests/test_application_flow.py:115:        self.assertEqual(response.data['decision'], ApprovalDecision.APPROVED)
backend/apps/applications/tests/test_application_flow.py:129:        dean_approval = application.approvals.get(step=ApprovalStep.DEAN)
backend/apps/applications/tests/test_application_flow.py:136:        self.assertEqual(response.data['decision'], ApprovalDecision.APPROVED)
backend/apps/applications/views.py:13:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/applications/views.py:16:from apps.notifications.services import notify_application_submitted
backend/apps/applications/views.py:71:        pending_approvals = Approval.objects.filter(
backend/apps/applications/views.py:72:            approver=user,
backend/apps/applications/views.py:73:            step=ApprovalStep.DORM_MANAGER,
backend/apps/applications/views.py:74:            decision=ApprovalDecision.PENDING
backend/apps/applications/views.py:80:        pending_approvals = Approval.objects.filter(
backend/apps/applications/views.py:81:            approver=user,
backend/apps/applications/views.py:82:            step=ApprovalStep.COUNSELOR,
backend/apps/applications/views.py:83:            decision=ApprovalDecision.PENDING
backend/apps/applications/views.py:154:    if class_mapping.dorm_manager is None:
backend/apps/applications/views.py:159:    dorm_manager_name = class_mapping.dorm_manager_name or class_mapping.dorm_manager.name
backend/apps/applications/views.py:172:    dorm_manager_approval = Approval.objects.create(
backend/apps/applications/views.py:175:        step=ApprovalStep.DORM_MANAGER,
backend/apps/applications/views.py:176:        approver=class_mapping.dorm_manager,
backend/apps/applications/views.py:177:        approver_name=dorm_manager_name,
backend/apps/applications/views.py:178:        decision=ApprovalDecision.PENDING
backend/apps/applications/views.py:181:    notify_application_submitted(application, dorm_manager_approval)
backend/apps/applications/permissions.py:3:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/applications/permissions.py:13:            dorm_manager=user,
backend/apps/applications/serializers.py:31:        from apps.approvals.serializers import ApprovalSerializer
backend/apps/applications/serializers.py:32:        return ApprovalSerializer(obj.approvals.all(), many=True).data
backend/apps/applications/models.py:8:    PENDING_DORM_MANAGER = 'pending_dorm_manager', '待宿管员审批'
backend/apps/applications/tests/test_list_permissions.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/applications/tests/test_list_permissions.py:30:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
backend/apps/applications/tests/test_list_permissions.py:31:        self.dorm_manager1.set_password('M001')
backend/apps/applications/tests/test_list_permissions.py:32:        self.dorm_manager1.save()
backend/apps/applications/tests/test_list_permissions.py:34:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
backend/apps/applications/tests/test_list_permissions.py:35:        self.dorm_manager2.set_password('M002')
backend/apps/applications/tests/test_list_permissions.py:36:        self.dorm_manager2.save()
backend/apps/applications/tests/test_list_permissions.py:43:        ClassMapping.objects.create(class_id='CS2020-01', dorm_manager=self.dorm_manager1, dorm_manager_name='宿管员1', counselor=self.counselor1, counselor_name='辅导员1', active=True)
backend/apps/applications/tests/test_list_permissions.py:44:        ClassMapping.objects.create(class_id='CS2020-02', dorm_manager=self.dorm_manager2, dorm_manager_name='宿管员2', counselor=self.counselor2, counselor_name='辅导员2', active=True)
backend/apps/applications/tests/test_list_permissions.py:68:        Approval.objects.create(
backend/apps/applications/tests/test_list_permissions.py:71:            step=ApprovalStep.COUNSELOR,
backend/apps/applications/tests/test_list_permissions.py:72:            approver=self.counselor1,
backend/apps/applications/tests/test_list_permissions.py:73:            approver_name='辅导员1',
backend/apps/applications/tests/test_list_permissions.py:74:            decision=ApprovalDecision.PENDING
backend/apps/applications/tests/test_detail_permissions.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
backend/apps/applications/tests/test_detail_permissions.py:32:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
backend/apps/applications/tests/test_detail_permissions.py:33:        self.dorm_manager1.set_password('M001')
backend/apps/applications/tests/test_detail_permissions.py:34:        self.dorm_manager1.save()
backend/apps/applications/tests/test_detail_permissions.py:36:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
backend/apps/applications/tests/test_detail_permissions.py:37:        self.dorm_manager2.set_password('M002')
backend/apps/applications/tests/test_detail_permissions.py:38:        self.dorm_manager2.save()
backend/apps/applications/tests/test_detail_permissions.py:50:        ClassMapping.objects.create(class_id='CS2020-01', dorm_manager=self.dorm_manager1, dorm_manager_name='宿管员1', counselor=self.counselor1, counselor_name='辅导员1', active=True)
backend/apps/applications/tests/test_detail_permissions.py:51:        ClassMapping.objects.create(class_id='CS2020-02', dorm_manager=self.dorm_manager2, dorm_manager_name='宿管员2', counselor=self.counselor2, counselor_name='辅导员2', active=True)
backend/apps/applications/tests/test_constraints.py:31:        self.dorm_manager = User.objects.create_user(
backend/apps/applications/tests/test_constraints.py:41:            dorm_manager=self.dorm_manager,
backend/apps/applications/tests/test_constraints.py:42:            dorm_manager_name='宿管员',
backend/apps/applications/migrations/0005_alter_application_status.py:16:            field=models.CharField(choices=[('draft', '草稿'), ('pending_dorm_manager', '待宿管员审批'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20),
backend/apps/users/management/commands/seed_data.py:20:            from apps.approvals.models import Approval
backend/apps/users/management/commands/seed_data.py:21:            Approval.objects.all().delete()
backend/apps/users/management/commands/seed_data.py:79:        dorm_managers = [
backend/apps/users/management/commands/seed_data.py:84:        for dm_data in dorm_managers:
backend/apps/users/management/commands/seed_data.py:96:                self.stdout.write(f'Created dorm_manager: {user.user_id}')
backend/apps/users/management/commands/seed_data.py:114:            {'class_id': 'CS2020-01', 'dorm_manager_id': 'M001', 'counselor_id': 'T001'},
backend/apps/users/management/commands/seed_data.py:115:            {'class_id': 'CS2020-02', 'dorm_manager_id': 'M002', 'counselor_id': 'T002'},
backend/apps/users/management/commands/seed_data.py:119:            dorm_manager = User.objects.get(user_id=mapping_data['dorm_manager_id'])
backend/apps/users/management/commands/seed_data.py:124:                    'dorm_manager': dorm_manager,
backend/apps/users/management/commands/seed_data.py:125:                    'dorm_manager_name': dorm_manager.name,
backend/apps/users/management/commands/seed_data.py:132:                self.stdout.write(f'Created mapping: {mapping.class_id} -> M:{dorm_manager.user_id}/C:{counselor.user_id}')
backend/apps/applications/tests/test_error_cases.py:52:        self.dorm_manager = User.objects.create_user(
backend/apps/applications/tests/test_error_cases.py:69:            dorm_manager=self.dorm_manager,
backend/apps/applications/tests/test_error_cases.py:70:            dorm_manager_name='宿管员',
backend/apps/users/migrations/0004_backfill_dorm_manager.py:6:def backfill_dorm_manager(apps, schema_editor):
backend/apps/users/migrations/0004_backfill_dorm_manager.py:8:    for mapping in ClassMapping.objects.filter(dorm_manager__isnull=True):
backend/apps/users/migrations/0004_backfill_dorm_manager.py:9:        mapping.dorm_manager_id = mapping.counselor_id
backend/apps/users/migrations/0004_backfill_dorm_manager.py:10:        mapping.dorm_manager_name = mapping.counselor_name
backend/apps/users/migrations/0004_backfill_dorm_manager.py:11:        mapping.save(update_fields=["dorm_manager", "dorm_manager_name"])
backend/apps/users/migrations/0004_backfill_dorm_manager.py:16:    ClassMapping.objects.all().update(dorm_manager=None, dorm_manager_name=None)
backend/apps/users/migrations/0004_backfill_dorm_manager.py:22:        ('users', '0003_classmapping_dorm_manager_and_more'),
backend/apps/users/migrations/0004_backfill_dorm_manager.py:26:        migrations.RunPython(backfill_dorm_manager, reverse_backfill),
backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:17:            name='dorm_manager',
backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:22:            name='dorm_manager_name',
backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:28:            field=models.CharField(choices=[('student', '学生'), ('dorm_manager', '宿管员'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20),
backend/apps/applications/tests/test_p0_fixes.py:4:from apps.approvals.models import Approval, ApprovalDecision, ApprovalStep
backend/apps/applications/tests/test_p0_fixes.py:30:    def test_can_resubmit_after_rejection(self):
backend/apps/applications/tests/test_p0_fixes.py:56:    def test_cannot_resubmit_while_pending(self):
backend/apps/applications/tests/test_p0_fixes.py:84:class ApprovalDecisionFilterTest(TestCase):
backend/apps/applications/tests/test_p0_fixes.py:130:        self.approval_pending = Approval.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:133:            step=ApprovalStep.COUNSELOR,
backend/apps/applications/tests/test_p0_fixes.py:134:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:135:            approver_name=self.counselor.name,
backend/apps/applications/tests/test_p0_fixes.py:136:            decision=ApprovalDecision.PENDING
backend/apps/applications/tests/test_p0_fixes.py:139:        self.approval_approved = Approval.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:142:            step=ApprovalStep.COUNSELOR,
backend/apps/applications/tests/test_p0_fixes.py:143:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:144:            approver_name=self.counselor.name,
backend/apps/applications/tests/test_p0_fixes.py:145:            decision=ApprovalDecision.APPROVED
backend/apps/applications/tests/test_p0_fixes.py:148:        self.approval_rejected = Approval.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:151:            step=ApprovalStep.COUNSELOR,
backend/apps/applications/tests/test_p0_fixes.py:152:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:153:            approver_name=self.counselor.name,
backend/apps/applications/tests/test_p0_fixes.py:154:            decision=ApprovalDecision.REJECTED
backend/apps/applications/tests/test_p0_fixes.py:158:        approvals = Approval.objects.filter(
backend/apps/applications/tests/test_p0_fixes.py:159:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:160:            decision=ApprovalDecision.PENDING
backend/apps/applications/tests/test_p0_fixes.py:166:        approvals = Approval.objects.filter(
backend/apps/applications/tests/test_p0_fixes.py:167:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:168:            decision=ApprovalDecision.APPROVED
backend/apps/applications/tests/test_p0_fixes.py:174:        approvals = Approval.objects.filter(
backend/apps/applications/tests/test_p0_fixes.py:175:            approver=self.counselor,
backend/apps/applications/tests/test_p0_fixes.py:176:            decision=ApprovalDecision.REJECTED
backend/apps/applications/tests/test_p0_fixes.py:182:        approvals = Approval.objects.filter(approver=self.counselor)

exec
/bin/bash -lc "rtk sed -n '1,240p' .omc/collaboration/tasks/TASK-20260605-04-phase-0-p0阻塞：116个file2独有学生缺少楼栋.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
---
task_id: TASK-20260605-04
owner: claude
assignee: none
status: open
created_at: 2026-06-05T19:55:07.600463+00:00
updated_at: 2026-06-05T19:55:07.600486+00:00
priority: normal
---

# Task: Phase 0 P0阻塞：116个File2独有学生缺少楼栋数据，导致宿管员路由失败（98.0% vs 100%门禁要求）。需要业务决策：1)接受98%覆盖率作为可接受标准 2)排除这116名学生直到补充楼栋数据 3)要求用户立即提供楼栋数据。辅导员路由已100%覆盖。此问题阻塞Phase 0验证通过及Phase 1-5实施。

**Task ID:** TASK-20260605-04
**Status:** open

## Objective

Phase 0 P0阻塞：116个File2独有学生缺少楼栋数据，导致宿管员路由失败（98.0% vs 100%门禁要求）。需要业务决策：1)接受98%覆盖率作为可接受标准 2)排除这116名学生直到补充楼栋数据 3)要求用户立即提供楼栋数据。辅导员路由已100%覆盖。此问题阻塞Phase 0验证通过及Phase 1-5实施。

## Acceptance Criteria

- [ ] Task completed as described

exec
/bin/bash -lc "rtk nl -ba .omc/collaboration/artifacts/20260605-consensus-implementation-plan.md | sed -n '1,190p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# Consensus: Implementation Plan Review
     2	
     3	**Date:** 2026-06-05  
     4	**Participants:** Claude, Codex  
     5	**Topic:** 用户需求最终确认与实施方案.md review and P0 blocker resolution  
     6	**Status:** ✅ Consensus achieved, implementation-ready
     7	
     8	---
     9	
    10	## Agreement Summary
    11	
    12	**Codex assessment:** 22/40 score, 3 P0 blockers prevent immediate implementation.
    13	
    14	**Claude response:** All P0 blockers addressed via Phase 0 data validation scripts.
    15	
    16	**Consensus:** Implementation plan is sound after Phase 0 additions. Proceed with Phase 0 execution when real data files available.
    17	
    18	---
    19	
    20	## P0 Blocker Resolutions (Agreed)
    21	
    22	### P0-1: Empty Student ID → Temp ID Strategy ✅
    23	
    24	**Problem:** User.user_id required but 271 grad + File2 unmatched lack student numbers.
    25	
    26	**Solution:** 3-tier ID generation
    27	- Priority 1: Real XH from File2
    28	- Priority 2: `GRAD2026_{hash8}` for graduates (SHA256 stable hash)
    29	- Priority 3: `TMP2026_{row:04d}` for File2 unmatched
    30	
    31	**Implementation:** `generate_temp_user_ids.py` (tested, committed)
    32	
    33	**File5 schema extensions:**
    34	- `user_id` (required): Login ID (real or generated)
    35	- `student_no` (optional): Real XH from File2
    36	- `user_id_source`: 'file2_xh' | 'grad_generated' | 'tmp_generated'
    37	- `source_row_id`: File1 original row number
    38	
    39	**Agreement:** This preserves data integrity while allowing full 5830-row import.
    40	
    41	---
    42	
    43	### P0-2: Multi-Approver Conflict → Primary Manager ✅
    44	
    45	**Problem:** Document suggests "any manager" but Approval.approver is single FK.
    46	
    47	**Solution:** MVP scope reduction
    48	- File3 must provide `primary_dorm_manager_user_id` per building
    49	- Each building has exactly one primary responsible manager
    50	- Multi-manager approval deferred to Phase 2
    51	
    52	**Implementation requirement:** File3 processing identifies single primary (first listed, manual spec, or default rule).
    53	
    54	**Agreement:** This maintains clean FK model while providing Phase 2 upgrade path.
    55	
    56	---
    57	
    58	### P0-3: ClassMapping Removal → Explicit Task List ✅
    59	
    60	**Problem:** ClassMapping deeply embedded, removal underestimated.
    61	
    62	**Solution:** Phase 2 expanded to 10 explicit subtasks
    63	1. Data model adjustments
    64	2. Submission routing refactor
    65	3. Approval pass routing refactor
    66	4. List filtering refactor
    67	5. Detail permissions refactor
    68	6. Attachment permissions sync
    69	7. Import command rewrite
    70	8. API schema update
    71	9. Frontend/miniprogram types sync
    72	10. Test fixture and regression
    73	
    74	**Validation gate:** `validate_routing_coverage.py` enforces 100% coverage before Phase 2.
    75	
    76	**Agreement:** Expanded task list prevents underestimation. Gate ensures data readiness.
    77	
    78	---
    79	
    80	## P1 Findings (Acknowledged)
    81	
    82	### Data Inconsistency
    83	- File1/File2 count discrepancy (155 vs 271+116) needs reconciliation
    84	- Merge report will output: `matched_count`, `file1_only_count`, `file2_only_count`
    85	- File2-only 116 rows: User to decide import vs archive
    86	
    87	### State Machine Naming
    88	- Keep existing `pending_dorm_manager` / `pending_counselor` convention
    89	- Avoid unnecessary migration from current backend/apps/applications/models.py
    90	
    91	### Application Snapshots
    92	- Add `student_building_name`, `student_department` to Application model
    93	- Deferred to Phase 2 data model task
    94	- Prevents routing corruption when User data changes
    95	
    96	### Normalization Maps
    97	- College: 18 mappings in `normalize_colleges.py` ✅
    98	- Building: Requires File3 analysis, pending
    99	- Both required for 100% routing coverage
   100	
   101	**Agreement:** These are implementation details, not blockers. Address in Phase 0-2.
   102	
   103	---
   104	
   105	## User Supplemental Requirement
   106	
   107	**User statement (2026-06-05):**
   108	> "文件5的数据中应该有寝室号字段，文件3中没有，后面会再确认提交文件3的寝室号字段数据，以形成单一对应关系"
   109	
   110	**Status:**
   111	- ✅ File5 includes `room_number` field (merge_student_data.py line 131)
   112	- ✅ Documented in implementation plan Section 2
   113	- ✅ Two-phase strategy: Phase 1 building-level, Phase 2 room-level precise
   114	
   115	**Agreement:** Room_number preserved for future File3 upgrade. No action required now.
   116	
   117	---
   118	
   119	## Phase 0 Implementation Status
   120	
   121	### Completed (2026-06-05)
   122	
   123	**Scripts created and tested:**
   124	
   125	1. **generate_temp_user_ids.py** (94 lines)
   126	   - `determine_user_id()`: 3-tier ID strategy
   127	   - `generate_grad_user_id()`: SHA256 hash for graduates
   128	   - `generate_tmp_user_id()`: Sequential for File2 unmatched
   129	   - Tests: ✅ Pass (real XH, grad hash stability, tmp sequential)
   130	
   131	2. **merge_student_data.py** (182 lines)
   132	   - `merge_files()`: File1+File2 → File5 with source tracking
   133	   - Matching key: "姓名+规范化学院+班级/BH"
   134	   - Output: 14 fields including user_id, user_id_source, student_no, room_number
   135	   - Statistics: matched/file1_only/grad/tmp counts, skipped rows
   136	
   137	3. **validate_routing_coverage.py** (177 lines)
   138	   - `validate_routing()`: 100% coverage gate check
   139	   - Validates: building→manager, department→counselor
   140	   - Exit: 0 if 100%, 1 with detailed failure report
   141	   - Report: Missing buildings/departments with student counts
   142	
   143	4. **normalize_colleges.py** (existing)
   144	   - 18 college mappings
   145	   - ValueError on unmapped names
   146	
   147	**Commit:** a142ad8 "feat: Phase 0数据门禁脚本实现" (+547 lines)
   148	
   149	**Documentation updated:**
   150	- Implementation plan: File mapping table, Phase 0 section, adjusted timeline
   151	- Status: "⚠️ Codex审查完成，3个P0技术阻塞待修正 (评分22/40)"
   152	
   153	### Ready for Execution
   154	
   155	**Prerequisites met:** ✅ All Phase 0 scripts implementation-ready
   156	
   157	**Awaiting:** Real data files from user
   158	- File1: 1-5830名毕业生（含研究生）.xls
   159	- File2: 2026届预计毕业生5675人.xlsx
   160	- File3: 2026年社区辅导员信息统计表.xls
   161	- File4: 2026年学院辅导员信息统计表.xls
   162	
   163	---
   164	
   165	## Execution Plan
   166	
   167	### Phase 0: Data Validation (Ready Now)
   168	
   169	**Step 1: Merge File1 + File2**
   170	```bash
   171	python3 backend/scripts/merge_student_data.py \
   172	  --file1 <path-to-file1> \
   173	  --file2 <path-to-file2> \
   174	  --output backend/data/file5_students_5830.csv \
   175	  --report backend/data/merge_report.json
   176	```
   177	
   178	**Expected output:**
   179	- file5_students_5830.csv (5830 rows, non-null user_id)
   180	- merge_report.json (matched/file1_only/grad/tmp counts)
   181	
   182	**Step 2: Validate Routing Coverage**
   183	```bash
   184	python3 backend/scripts/validate_routing_coverage.py \
   185	  --file5 backend/data/file5_students_5830.csv \
   186	  --file3 <path-to-file3> \
   187	  --file4 <path-to-file4> \
   188	  --report backend/data/routing_coverage_report.json
   189	```
   190	

exec
/bin/bash -lc "rtk nl -ba backend/scripts/validate_routing_coverage.py | sed -n '70,180p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
    70	    return dept_counselors
    71	
    72	
    73	def validate_routing(file5_path: str, file3_path: str, file4_path: str) -> dict:
    74	    """
    75	    Validate that all students can be routed to approvers.
    76	
    77	    Returns validation report with coverage statistics.
    78	    """
    79	    students = load_students(file5_path)
    80	    building_managers = load_dorm_managers(file3_path)
    81	    dept_counselors = load_counselors(file4_path)
    82	
    83	    report = {
    84	        'total_students': len(students),
    85	        'dorm_manager_coverage': 0,
    86	        'counselor_coverage': 0,
    87	        'fully_routable': 0,
    88	        'missing_dorm_manager': [],
    89	        'missing_counselor': [],
    90	        'unroutable_students': []
    91	    }
    92	
    93	    for student in students:
    94	        user_id = student['user_id']
    95	        name = student['name']
    96	        building = student['building_name']
    97	        department = student['department']
    98	
    99	        # Check dorm manager routing
   100	        has_dorm_manager = building in building_managers
   101	        if has_dorm_manager:
   102	            report['dorm_manager_coverage'] += 1
   103	        else:
   104	            report['missing_dorm_manager'].append({
   105	                'user_id': user_id,
   106	                'name': name,
   107	                'building': building
   108	            })
   109	
   110	        # Check counselor routing
   111	        has_counselor = department in dept_counselors
   112	        if has_counselor:
   113	            report['counselor_coverage'] += 1
   114	        else:
   115	            report['missing_counselor'].append({
   116	                'user_id': user_id,
   117	                'name': name,
   118	                'department': department
   119	            })
   120	
   121	        # Check full routing
   122	        if has_dorm_manager and has_counselor:
   123	            report['fully_routable'] += 1
   124	        else:
   125	            report['unroutable_students'].append({
   126	                'user_id': user_id,
   127	                'name': name,
   128	                'building': building,
   129	                'department': department,
   130	                'missing': {
   131	                    'dorm_manager': not has_dorm_manager,
   132	                    'counselor': not has_counselor
   133	                }
   134	            })
   135	
   136	    # Calculate percentages
   137	    total = report['total_students']
   138	    report['dorm_manager_coverage_pct'] = (report['dorm_manager_coverage'] / total * 100) if total > 0 else 0
   139	    report['counselor_coverage_pct'] = (report['counselor_coverage'] / total * 100) if total > 0 else 0
   140	    report['fully_routable_pct'] = (report['fully_routable'] / total * 100) if total > 0 else 0
   141	
   142	    return report
   143	
   144	
   145	if __name__ == "__main__":
   146	    import argparse
   147	
   148	    parser = argparse.ArgumentParser(description='Validate routing coverage')
   149	    parser.add_argument('--file5', required=True, help='Path to File5 (merged students)')
   150	    parser.add_argument('--file3', required=True, help='Path to File3 (dorm managers)')
   151	    parser.add_argument('--file4', required=True, help='Path to File4 (counselors)')
   152	    parser.add_argument('--report', help='Optional JSON report output path')
   153	
   154	    args = parser.parse_args()
   155	
   156	    print("Validating routing coverage...")
   157	    report = validate_routing(args.file5, args.file3, args.file4)
   158	
   159	    print("\n=== Routing Coverage Report ===")
   160	    print(f"Total students: {report['total_students']}")
   161	    print(f"\nDorm manager coverage: {report['dorm_manager_coverage']}/{report['total_students']} ({report['dorm_manager_coverage_pct']:.1f}%)")
   162	    print(f"Counselor coverage: {report['counselor_coverage']}/{report['total_students']} ({report['counselor_coverage_pct']:.1f}%)")
   163	    print(f"Fully routable: {report['fully_routable']}/{report['total_students']} ({report['fully_routable_pct']:.1f}%)")
   164	
   165	    # Gate check
   166	    if report['fully_routable_pct'] == 100.0:
   167	        print("\n✓ PASS: 100% routing coverage achieved")
   168	        exit_code = 0
   169	    else:
   170	        print(f"\n✗ FAIL: {len(report['unroutable_students'])} students cannot be routed")
   171	        print("\nMissing dorm managers for buildings:")
   172	        missing_buildings = set(s['building'] for s in report['missing_dorm_manager'])
   173	        for building in sorted(missing_buildings):
   174	            count = sum(1 for s in report['missing_dorm_manager'] if s['building'] == building)
   175	            print(f"  - {building}: {count} students")
   176	
   177	        print("\nMissing counselors for departments:")
   178	        missing_depts = set(s['department'] for s in report['missing_counselor'])
   179	        for dept in sorted(missing_depts):
   180	            count = sum(1 for s in report['missing_counselor'] if s['department'] == dept)

exec
/bin/bash -lc "rtk nl -ba .omc/collaboration/artifacts/20260605-user-business-decisions.md | sed -n '35,120p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
    35	**实施：**
    36	- Phase 0.3：File3到达后分析楼栋名称
    37	- 如需规范化，创建building normalization map
    38	- 100%覆盖门禁确保所有学生可路由
    39	
    40	---
    41	
    42	### 决策3：File2独有116行处理
    43	
    44	**问题：** File2中116个File1没有的学生如何处理？
    45	
    46	**用户答复：**
    47	> "导入"
    48	
    49	**结论：**
    50	- File2独有116行作为额外学生导入
    51	- 总学生数：5830（File1）+ 116（File2 only）= 5946行
    52	- 需修改合并策略
    53	
    54	**影响：**
    55	
    56	**merge_student_data.py需调整：**
    57	```python
    58	# 当前：只输出File1的5830行
    59	# 修改：输出File1 + File2独有行
    60	
    61	# 新逻辑：
    62	# 1. File1为基准（5830行）
    63	# 2. File2匹配的：补充字段
    64	# 3. File2独有的（116行）：作为新行追加
    65	#    - user_id: 从File2的XH
    66	#    - user_id_source: 'file2_only'
    67	#    - File1字段：空值
    68	```
    69	
    70	**merge_report.json需包含：**
    71	- file1_only_count: 271（研究生等）
    72	- file2_only_count: 116
    73	- matched_count: 5559
    74	- total_output_rows: 5946
    75	
    76	---
    77	
    78	### 决策4：学工管理员数据提供方式
    79	
    80	**问题：** Admin角色如何实现？复用dean还是新增？
    81	
    82	**用户答复：**
    83	> "学工管理员数据后面会同样提供EXCEL表格或CSV数据（学工管理员，不做审批流程，但能查看全部进度数据）"
    84	
    85	**结论：**
    86	- 学工管理员数据单独提供（Excel/CSV格式）
    87	- 角色定义：只读，可查看全部申请，无审批权限
    88	- 不复用dean枚举，等待独立数据文件
    89	
    90	**数据格式（待确认）：**
    91	```
    92	职工号,姓名,部门,手机号,邮箱
    93	A001,张三,学工部,13800000001,zhangsan@example.com
    94	```
    95	
    96	**实施：**
    97	- Phase 3增加：import_admins命令
    98	- UserRole枚举：student | dorm_manager | counselor | admin
    99	- 权限：admin可查看所有申请但不能审批
   100	
   101	---
   102	
   103	## 实施影响
   104	
   105	### 立即需要修改
   106	
   107	**1. merge_student_data.py**
   108	- 增加File2独有行处理逻辑
   109	- 输出5946行而非5830行
   110	- 新增user_id_source: 'file2_only'
   111	
   112	**2. validate_routing_coverage.py**
   113	- 验证目标：5946行学生100%路由覆盖
   114	
   115	**3. 文档更新**
   116	- 实施方案：数据覆盖5830→5946
   117	- Phase 3：增加import_admins命令
   118	
   119	### 等待用户提供
   120	

exec
/bin/bash -lc "rtk nl -ba docs/用户需求最终确认与实施方案.md | sed -n '90,130p;400,430p;470,490p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
    90	> "二次审批完成后，将流程与审批结果数据进行保存"
    91	
    92	**解读：**
    93	- 保存完整审批流程记录
    94	- 保存每次审批结果（通过/驳回/意见）
    95	- 支持审批历史查询
    96	
    97	**影响：**
    98	- ✓ 当前系统已支持（Application + Approval模型）
    99	
   100	### 决策5: 新增学工管理员角色
   101	
   102	**用户原文：**
   103	> "学工管理员数据没有添加，但要保留。学工管理员不做审批，但要能查看学生离校审批的整体情况"
   104	
   105	**4类用户定义：**
   106	
   107	| 角色 | 职责 | 权限范围 |
   108	|------|------|----------|
   109	| 学生 (student) | 提交离校申请 | 查看自己的申请 |
   110	| 宿管员 (dorm_manager) | 第一次审批（按楼栋） | 只看自己负责楼栋的申请 |
   111	| 辅导员 (counselor) | 第二次审批（按学院） | 只看自己负责学院的申请 |
   112	| 学工管理员 (admin) | 查看全局数据 | 查看所有申请，但无审批权限 |
   113	
   114	**影响：**
   115	- 需要新增 `admin` 角色
   116	- 需要全局视图界面
   117	- 学工管理员数据后续提供（Excel/CSV格式）
   118	
   119	---
   120	
   121	## 二、补充确认：寝室号字段
   122	
   123	### 确认1: 楼栋审批关系
   124	
   125	**用户原文：**
   126	> "楼栋按文件5与文件3中共同的楼栋字段为审批关系设定"
   127	
   128	**解读：**
   129	- File5 (学生).楼栋名称 ↔ File3 (宿管员).楼栋号
   130	- 匹配规则：字符串精确匹配或规范化后匹配
   400	**楼栋规范化（需File3数据）：**
   401	- `building_normalization_map.json` - 33个楼栋映射（待File3提供后创建）
   402	- 依赖：需File3楼栋名称与File1对比，创建映射表
   403	- 当前：标记为Task 0.3依赖项，File3到达后补充
   404	
   405	**状态：** 学院规范化✓完成，楼栋规范化⏳pending File3
   406	
   407	**Task 0.4: 主责宿管员指定（0.3天）**
   408	
   409	File3处理：
   410	- 每栋楼必须指定1个`primary_dorm_manager_user_id`
   411	- 如楼栋有多人，人工或按默认规则（首位/编号最小）选主责
   412	- 输出：`file3_dorm_managers_with_primary.csv`
   413	
   414	**Task 0.5: 路由覆盖验证（0.2天）**
   415	
   416	```python
   417	# backend/scripts/validate_routing_coverage.py
   418	def validate_routing():
   419	    # 验证每个学生：
   420	    # - building_name能找到primary dorm manager
   421	    # - department能找到counselor
   422	    # 输出100%覆盖报告或失败清单
   423	    pass
   424	```
   425	
   426	门禁标准：
   427	- ✓ 5946行学生user_id非空且唯一（5830 File1 + 116 File2独有）
   428	- ✓ 100%学生可路由到宿管员
   429	- ✓ 100%学生可路由到辅导员
   430	- ✓ 无规范化失败
   470	
   471	**任务2.2：路由逻辑重构**
   472	- 创建 `BuildingApprovalRouter` - 楼栋→宿管员路由
   473	- 创建 `DepartmentApprovalRouter` - 学院→辅导员路由
   474	- 移除 `ClassMapping` 依赖
   475	
   476	**任务2.3：权限控制扩展**
   477	- 新增 `admin` 角色
   478	- 实现全局查看权限（无业务范围限制）
   479	- 更新权限装饰器
   480	
   481	**任务2.4：数据模型微调**
   482	- `Student.class_id` 改为可空
   483	- 确保 `Student.building_name` 和 `Student.department` 非空
   484	- 预留 `DormManager.room_numbers` 字段（未来使用）
   485	
   486	### Phase 3: 数据导入（0.5天）
   487	
   488	**导入脚本：**
   489	```bash
   490	# Step 1: 导入学生（5830行）

ERROR: Reconnecting... 1/5
2026-06-05T20:00:10.656890Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657363Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657371Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657374Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657378Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657380Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657383Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657386Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657389Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657392Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657394Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657398Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657401Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657404Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657406Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657419Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657423Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657425Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657428Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657430Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657433Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657435Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657437Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657439Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657442Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657444Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657447Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657449Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657452Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657454Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657456Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657458Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657461Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657464Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657466Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657469Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657480Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657482Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657484Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657486Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657488Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657491Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657493Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657496Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657498Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657500Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657502Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657505Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657508Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657510Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657512Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657514Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657524Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657526Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657528Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657530Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657532Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:10.657534Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788070Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788158Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788213Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788217Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788221Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788255Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788259Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788264Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788292Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788296Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788310Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788322Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788355Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788358Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788362Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788375Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788400Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788404Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788417Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788431Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788457Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788461Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788473Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788485Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788522Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788526Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788529Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788543Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788564Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788583Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788586Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788615Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788619Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788622Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788625Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788637Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788655Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788670Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788778Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788782Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788784Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788787Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788789Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788791Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788793Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788796Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788798Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788801Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788804Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788826Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788829Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788831Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788840Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788872Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788875Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.788878Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.789007Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.789047Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.789051Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.789061Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:11.789071Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879113Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879183Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879187Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879211Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879221Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879242Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879257Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879278Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879280Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879299Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879302Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879322Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879333Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879345Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879402Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879429Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879456Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879460Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879472Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879503Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879514Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879554Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879605Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879608Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879618Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879640Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879658Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879661Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879671Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879687Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879701Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879718Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879721Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879730Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879753Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879763Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879766Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879775Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879784Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879793Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879814Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879823Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879825Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879835Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879843Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879852Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879860Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879875Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879890Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879892Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879901Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879909Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879942Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879951Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879953Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879956Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879958Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879967Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879979Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.879988Z ERROR codex_core::util: OutputTextDelta without active item
2026-06-05T20:00:12.990134Z ERROR codex_core::util: OutputTextDelta without active item
codex
**评审结论：不建议直接采纳“选项1=接受98%覆盖率并通过Phase 0”。**

Claude的方向有现实性：File2本身没有楼栋字段，继续让5830名已可路由学生被116条缺字段数据长期阻塞，确实不划算。但当前推荐把“继续实施主流程”和“降低验收门禁”混在一起了，风险偏高。

**主要问题**

1. 这会破坏既有门禁共识。前序共识明确要求 `validate_routing_coverage.py` 在 Phase 2 前强制 100% 覆盖，实施方案也写明5946人宿管/辅导员均需100%可路由。仅因116人缺楼栋就把门禁改成98%，需要用户明确批准，不能作为技术团队默认决策。

2. “导入116人”不等于“允许116人无法提交”。用户决策只是要求 File2 独有学生导入，不代表接受他们上线后不能走离校流程。文档第170行后的推荐理由把“符合用户导入决策”和“116人暂不可用”绑定，逻辑不充分。

3. 遗漏了更稳妥的混合方案：**导入5946人，但把116人标记为 `routing_incomplete` / `missing_building`，禁止提交或进入人工补录队列；Phase 0主流程按5830人通过，116人作为显式阻塞清单单独跟踪。** 这比简单接受98%更清晰，也比完全等待数据更可推进。

4. 还应补一个业务判断：这116人是否可能是校外住宿、无需宿管审批、非毕业离校对象或数据重复/异动学生。如果存在“无需宿管”的合法类别，应新增明确的业务路由规则，而不是让空楼栋静默失败。

**建议决策**

推荐采用“选项1的推进节奏 + 更严格的限制条件”，不要表述为“接受98%覆盖率”。

业务口径建议改为：

- 5946人全部导入，用于身份、辅导员、统计和后续补录。
- 5830名 File1 学生满足完整审批路由，可进入 Phase 1-5。
- 116名 File2-only 学生不得提交离校申请，直到补齐楼栋/寝室，或用户确认其为免宿管/特殊流程。
- 系统必须显式提示“住宿信息缺失，暂不能提交”，不能到审批创建时才失败。
- 保留100%门禁，但拆成两个门禁：`active_eligible_students` 100%可路由；`all_imported_students` 缺失清单为已知例外并需用户签字确认。

**最终意见**

Claude推荐“不要因116人阻塞主流程”是合理的；但“降低为98%验收通过”不够严谨。业务上应要求用户在三件事中明确确认：这116人是否必须使用系统、是否能补楼栋数据、补齐前是否允许他们不可提交。默认决策应是“主流程推进，116人导入但冻结申请能力并形成补录清单”。
tokens used
62,105

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
