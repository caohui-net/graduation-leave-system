# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-01T04:07:17.714Z

## Original task

我已经分析了你对测试覆盖方案的4个批评点，并创建了修订方案。请审查 .omc/collaboration/artifacts/test-coverage-claude-response.md 并提供反馈。

关键问题：
1. 我接受了你关于重复测试、产品规则冲突、时区范围的批评
2. 但我需要澄清状态机测试范围 - 我提议的是顺序逻辑测试（状态转换矩阵、终态保护、唯一性约束），不是真实并发测试
3. 修订后的时间估算是0.6-0.7天（略高于你的0.5天建议）

请评估：
- 修订后的测试范围是否合理？
- 时间估算是否现实？
- 是否需要进一步削减范围？
- 时区测试应该包含（合并到现有文件）还是完全跳过？

目标：达成一致的可执行方案，然后立即实施。

## Final prompt

我已经分析了你对测试覆盖方案的4个批评点，并创建了修订方案。请审查 .omc/collaboration/artifacts/test-coverage-claude-response.md 并提供反馈。

关键问题：
1. 我接受了你关于重复测试、产品规则冲突、时区范围的批评
2. 但我需要澄清状态机测试范围 - 我提议的是顺序逻辑测试（状态转换矩阵、终态保护、唯一性约束），不是真实并发测试
3. 修订后的时间估算是0.6-0.7天（略高于你的0.5天建议）

请评估：
- 修订后的测试范围是否合理？
- 时间估算是否现实？
- 是否需要进一步削减范围？
- 时区测试应该包含（合并到现有文件）还是完全跳过？

目标：达成一致的可执行方案，然后立即实施。

## Raw output

```text
结论：修订方案可以接受，但应小幅收窄后执行。我已把正式反馈写入 [20260601-0405-codex-test-coverage-feedback.md](/home/caohui/projects/graduation-leave-system/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md)，并记录 collaboration event `73`。

核心反馈：

- 状态机范围合理：顺序 API/validator 逻辑测试可以做，不做真实并发测试。
- 时间估算：`0.6 天`作为目标现实，`0.7 天`作为 buffer 可以接受；如果新建完整 8-case matrix，才会明显超。
- 需要削减：不要从零创建大矩阵。现有 `test_application_flow.py`、`test_rejection_flow.py`、`test_state_machine.py` 已覆盖不少路径，应只补缺口。
- 时区测试：保留，但只合并进 `test_serializer_validation.py`，做 2 个 mock 边界用例；若必须压到 `0.5 天`，时区测试第一优先砍。

最终建议执行范围：

1. 新增 3 个 application detail 权限测试：学生不能看他人、辅导员不能跨班、dean 只能看自己 pending dean approval 的申请。注意当前 dean detail 语义是 pending-only，见 [applications/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/views.py:161)。
2. `decision=all` 泄漏测试放进 approval list permissions 文件，不放 detail isolation 文件。
3. 状态机只补缺口：rejected 后重提、必要的终态反向操作保护、dean approval uniqueness。不要写“draft -> approved”这类模型级非法转换测试，当前 [models.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/models.py:36) 没有完整状态转换图验证。
4. 时区边界合并到 serializer validation，2 个 deterministic mock 测试即可。

可执行共识：按上述范围立即实施；不做真实并发、不做跨时区矩阵、不新建大而全的状态机测试套件。


OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019e815a-079e-7472-a526-e552564a505c
--------
user
我已经分析了你对测试覆盖方案的4个批评点，并创建了修订方案。请审查 .omc/collaboration/artifacts/test-coverage-claude-response.md 并提供反馈。

关键问题：
1. 我接受了你关于重复测试、产品规则冲突、时区范围的批评
2. 但我需要澄清状态机测试范围 - 我提议的是顺序逻辑测试（状态转换矩阵、终态保护、唯一性约束），不是真实并发测试
3. 修订后的时间估算是0.6-0.7天（略高于你的0.5天建议）

请评估：
- 修订后的测试范围是否合理？
- 时间估算是否现实？
- 是否需要进一步削减范围？
- 时区测试应该包含（合并到现有文件）还是完全跳过？

目标：达成一致的可执行方案，然后立即实施。
codex
我会先读取项目里的协作协议和 Codex review 规则，再看修订方案本身；这次按正式 review 处理，反馈会直接围绕可执行范围和风险点。
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

exec
/bin/bash -lc "sed -n '1,240p' .omc/collaboration/protocol.md" in /home/caohui/projects/graduation-leave-system
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


codex
已读取 review 协议和协作协议。注意到项目规则要求所有 shell 命令走 `rtk`，后续命令我会按这个约束执行；现在继续核对修订文档和相关测试上下文。
exec
/bin/bash -lc "rtk sed -n '1,260p' .omc/collaboration/artifacts/test-coverage-claude-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Claude Response to Codex Test Coverage Critique

**Created:** 2026-06-01T04:02:30Z  
**Context:** Response to Codex's critique of test-coverage-analysis.md

---

## Analysis of Codex's 4 Points

### Point 1: Duplication with Existing Tests ✅ ACCEPT

**Codex's critique:**
> "数据隔离测试不足" 中的列表隔离已经被 test_list_permissions.py 覆盖

**My analysis:**
- **Codex is RIGHT.** I reviewed existing tests:
  - `backend/apps/applications/tests/test_list_permissions.py` - student sees own, counselor sees own class
  - `backend/apps/approvals/tests/test_list_permissions.py` - counselor/dean see own approvals
- My proposal to test "辅导员A不能看到辅导员B的学生申请" in list context is **duplicate**.

**BUT - Real Gap Identified:**
- **Detail endpoint isolation NOT tested:**
  - Student accessing another student's application detail → should 403
  - Counselor accessing cross-class application detail → should 403
  - Dean accessing non-assigned application detail → should 403

**Revised scope:** Focus on detail endpoints only, drop list permission tests.

---

### Point 2: Product Rule Conflict ✅ ACCEPT

**Codex's critique:**
> "学工部可以看所有审批" 与代码不符

**My analysis:**
- **Codex is RIGHT.** I just verified `backend/apps/approvals/views.py` lines 36-40:
  ```python
  # 学工部: 只看自己的dean审批
  elif user.role == UserRole.DEAN:
      queryset = Approval.objects.filter(
          approver=user,  # ← Only assigned approvals
          step=ApprovalStep.DEAN
      )
  ```
- Dean sees **only assigned approvals**, not all approvals.
- My assumption was **wrong**.

**Revised understanding:**
- Student: sees own applications only
- Counselor: sees applications from assigned classes only
- Dean: sees applications with pending/completed dean approval assigned to them only

**Action:** Remove "学工部可以看所有审批" from test plan.

---

### Point 3: State Transition Scope ⚠️ CLARIFY

**Codex's critique:**
> 真实并发测试（threading/multiprocessing）在 0.5 天内不现实

**My analysis:**
- **Codex is RIGHT** about real concurrency testing being too complex.
- **BUT** - I need to clarify what I meant by "状态流转完整性测试":

**What I'm NOT proposing:**
- ❌ Real threading/multiprocessing race condition tests
- ❌ Load testing with concurrent requests
- ❌ Distributed transaction testing

**What I AM proposing:**
- ✅ **Legal path matrix:** Test all valid state transitions sequentially
  - draft → pending_counselor (submit)
  - pending_counselor → pending_dean (counselor approve)
  - pending_counselor → rejected (counselor reject)
  - pending_dean → approved (dean approve)
  - pending_dean → rejected (dean reject)
  - rejected → pending_counselor (resubmit)
  
- ✅ **Illegal transition rejection:** Test that invalid transitions are blocked
  - draft → approved (skip approval)
  - pending_counselor → approved (skip dean)
  - approved → pending_dean (reverse from terminal)
  - rejected → approved (reverse from terminal)

- ✅ **Terminal state protection:** Test that approved/rejected applications can't be modified
  - Try to approve already-approved application → 409
  - Try to reject already-rejected application → 409

- ✅ **Dean approval uniqueness:** Test that duplicate dean approval creation is blocked
  - Counselor approves twice → second attempt should detect existing dean approval → 409

**These are sequential tests, not concurrency tests.** They verify state machine logic and database constraints.

**Question for Codex:** Does this clarified scope align with your "状态流转矩阵" recommendation? Or do you see additional scope creep here?

---

### Point 4: Timezone Scope ✅ ACCEPT

**Codex's critique:**
> 跨时区测试矩阵过度，系统只用 Asia/Shanghai

**My analysis:**
- **Codex is RIGHT.** System uses `USE_TZ=True` + `TIME_ZONE='Asia/Shanghai'`.
- Cross-timezone matrix (UTC, US/Pacific, etc.) is **overkill**.

**Real edge case:**
- Midnight boundary: Student submits at 23:59:59 with leave_date="tomorrow" → does validation pass?
- Serializer uses `timezone.now().date()` (line 46 of serializers.py)

**Revised scope:**
- Test server-local date boundaries with **mocked timezone.now()**
- 2-3 deterministic tests:
  1. Submit at 23:59:59 with leave_date=tomorrow → should pass
  2. Submit at 00:00:01 with leave_date=today → should pass
  3. Submit at any time with leave_date=yesterday → should fail (400)

**Alternative:** Merge these into existing `test_serializer_validation.py` instead of separate file.

---

## Revised Test Plan

### Test File 1: test_detail_isolation.py (NEW)

**Purpose:** Verify detail endpoint access control

**Test cases:**
1. `test_student_cannot_access_other_student_application`
   - Student A creates application
   - Student B tries GET /api/applications/{A's app_id}
   - Expected: 403 FORBIDDEN

2. `test_counselor_cannot_access_cross_class_application`
   - Student from class CS2020-01 creates application
   - Counselor T002 (assigned to CS2020-02) tries GET /api/applications/{app_id}
   - Expected: 403 FORBIDDEN

3. `test_dean_cannot_access_non_assigned_application`
   - Student creates application, counselor approves (creates dean approval for D001)
   - Dean D002 (different dean) tries GET /api/applications/{app_id}
   - Expected: 403 FORBIDDEN (dean only sees applications with their own dean approval)

4. `test_decision_all_does_not_leak_cross_approver_data`
   - Counselor T001 has 2 approvals (1 pending, 1 approved)
   - Counselor T002 has 1 approval (pending)
   - T001 calls GET /api/approvals/?decision=all
   - Expected: Returns only T001's 2 approvals, not T002's

**Estimated time:** 2 hours

---

### Test File 2: test_state_machine_matrix.py (NEW)

**Purpose:** Verify complete state transition logic (sequential, not concurrent)

**Test cases:**

**Legal paths:**
1. `test_complete_approval_path`
   - draft → pending_counselor → pending_dean → approved

2. `test_counselor_rejection_path`
   - draft → pending_counselor → rejected

3. `test_dean_rejection_path`
   - draft → pending_counselor → pending_dean → rejected

4. `test_resubmission_after_rejection`
   - draft → pending_counselor → rejected → pending_counselor (new application)

**Illegal paths:**
5. `test_cannot_skip_counselor_approval`
   - Create application in pending_counselor state
   - Try to directly set status=approved
   - Expected: State machine validation prevents this

6. `test_cannot_modify_approved_application`
   - Application reaches approved state
   - Try to approve again → 409 CONFLICT
   - Try to reject → 409 CONFLICT

7. `test_cannot_modify_rejected_application`
   - Application reaches rejected state
   - Try to approve → 409 CONFLICT
   - Try to reject again → 409 CONFLICT

**Duplicate prevention:**
8. `test_dean_approval_uniqueness`
   - Counselor approves (creates dean approval)
   - Try to approve same counselor approval again
   - Expected: 409 CONFLICT "学工部审批已存在，不能重复创建"

**Estimated time:** 3 hours

---

### Test File 3: Timezone Boundaries (OPTIONAL)

**Option A:** Create `test_timezone_boundaries.py` (1 hour)

**Option B:** Merge into existing `test_serializer_validation.py` (30 minutes)

**Test cases (2-3 tests):**
1. `test_leave_date_validation_at_midnight_boundary`
   - Mock timezone.now() to 2026-06-01 23:59:59
   - Submit with leave_date="2026-06-02"
   - Expected: Pass (tomorrow is valid)

2. `test_leave_date_validation_after_midnight`
   - Mock timezone.now() to 2026-06-02 00:00:01
   - Submit with leave_date="2026-06-02"
   - Expected: Pass (today is valid)

3. `test_leave_date_cannot_be_past`
   - Mock timezone.now() to 2026-06-02 12:00:00
   - Submit with leave_date="2026-06-01"
   - Expected: 400 VALIDATION_ERROR

**Recommendation:** Option B (merge into existing file) to avoid file proliferation.

---

## Revised Time Estimate

**Core tests (必须做):**
- test_detail_isolation.py: 2 hours
- test_state_machine_matrix.py: 3 hours
- **Total: 5 hours (0.6 days)**

**Optional timezone tests:**
- Merge into test_serializer_validation.py: +30 minutes
- **Total with optional: 5.5 hours (0.7 days)**

**Codex's estimate was 0.5 days for narrowed scope.** My revised estimate is slightly higher (0.6-0.7 days) because:
- Detail isolation needs 4 test cases (not just 2-3)
- State machine matrix needs 8 test cases for complete coverage
- Timezone tests add 30 minutes if included

---

## Questions for Codex

1. **State machine scope:** Does my clarified scope (sequential logic tests, not concurrency) align with your "状态流转矩阵" recommendation?

2. **Time estimate:** Is 0.6-0.7 days realistic, or do you see further scope reduction needed?

3. **Timezone tests:** Should we include them (Option B, merge into existing file), or skip entirely?

4. **Priority:** If we must cut scope to hit 0.5 days, which should we drop first?
   - Option A: Drop timezone tests entirely (saves 30 min)
   - Option B: Reduce state machine tests from 8 to 5 (saves 1 hour)
   - Option C: Reduce detail isolation from 4 to 3 tests (saves 30 min)

---

## Proposed Next Steps

exec
/bin/bash -lc "rtk rg --files -g '*test*' -g '*spec*' . | head -200" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
./tests/test_p0_fixes.sh
./tests/smoke_test.sh
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md
./backend/apps/approvals/tests/test_rejection_flow.py
./backend/apps/approvals/tests/test_list_permissions.py
./backend/apps/approvals/tests/test_permissions.py
./backend/apps/approvals/tests/test_state_machine.py
./backend/apps/applications/tests/test_constraints.py
./backend/apps/applications/tests/test_p0_fixes.py
./backend/apps/applications/tests/test_application_flow.py
./backend/apps/applications/tests/test_serializer_validation.py
./backend/apps/applications/tests/test_list_permissions.py
./backend/apps/applications/tests/test_error_cases.py

exec
/bin/bash -lc "rtk rg -n \"leave|Leave|timezone|time zone|UTC|Asia|approval|status|state|状态|审批\" . --glob '"'!node_modules/**'"' --glob '"'!dist/**'"' --glob '"'!build/**'"'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
./task_plan.md:4:Respond to Claude's Week 3 closure questions, choose an executable compromise, then implement the agreed P0 security/state coverage and v0.2 contract/type alignment.
./task_plan.md:17:| 0. Load protocols and inspect Claude response | complete | RTK, collaboration protocol, review protocol, state/events, artifact, approvals/application code, and current tests inspected. |
./task_plan.md:19:| 2. Implement P0 security/state scope | complete | Added focused negative permission tests, reusable state validator, and state-machine tests. |
./task_plan.md:32:| Broad test label discovery failed for `apps.approvals.tests apps.applications.tests` | Full test attempt | Ran explicit test modules; 37 tests passed. |
./progress.md:4:- Loaded RTK rule, collaboration protocol, Codex review protocol, Claude response artifact, collaboration state/events, AGENTS.md, approval/application code, and existing tests.
./progress.md:5:- Determined consensus answer should choose Option B with P0 minimal security tests and a focused reusable state validator.
./progress.md:6:- Wrote `.omc/collaboration/artifacts/20260531-0405-codex-week3-consensus-response.md` and appended collaboration event 59 with state set to `in_progress`.
./progress.md:7:- Added `backend/apps/approvals/validators.py`, wired approve/reject endpoints through the reusable status/step validator, and expanded approval permission/state-machine tests.
./progress.md:8:- Targeted approval tests passed in Docker with `--keepdb`: 10 tests OK.
./progress.md:14:- Appended collaboration completion event 60 and set state to completed.
./CLAUDE.md:1:# 毕业生离校申请审批系统 - 项目配置
./CLAUDE.md:5:**项目名称：** 毕业生离校申请审批系统  
./CLAUDE.md:16:**强制规则：** When participating in Claude-Codex collaboration workflow, read and follow `.omc/collaboration/protocol.md` for task execution, artifact generation, and state management.
./AGENTS.md:6:- When participating in the Claude-Codex collaboration workflow, read and follow `.omc/collaboration/protocol.md` before acting. Treat it as the project-local contract for task execution, artifact generation, event logging, and shared state management.
./AGENTS.md:8:- If `docs/codex-review-protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.
./AGENTS.md:10:- If `.omc/collaboration/protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.
./miniprogram/services/api.ts:48:          if (res.statusCode === 401) {
./miniprogram/services/api.ts:54:          if (res.statusCode >= 400) {
./miniprogram/services/api.ts:101:      `/api/approvals/?decision=${decision}&limit=${limit}&offset=${offset}`
./miniprogram/services/api.ts:109:    return this.request(`/api/approvals/${id}/approve/`, {
./miniprogram/services/api.ts:119:    return this.request(`/api/approvals/${id}/reject/`, {
./miniprogram/project.config.json:2:  "description": "毕业离校申请审批系统",
./miniprogram/project.config.json:45:  "projectname": "graduation-leave-system",
./docker-compose.yml:7:      POSTGRES_DB: graduation_leave
./miniprogram/types/api.ts:39:  leave_date: string; // YYYY-MM-DD
./miniprogram/types/api.ts:48:  leave_date: string;
./miniprogram/types/api.ts:49:  status: ApplicationStatus;
./miniprogram/types/api.ts:55:  dorm_checkout_status: string;
./miniprogram/types/api.ts:56:  approvals: ApprovalDetail[];
./miniprogram/types/api.ts:61:  approval_id: string;
./miniprogram/types/api.ts:72:  approval_id: string;
./miniprogram/types/api.ts:86:  approval_id: string;
./miniprogram/app.json:5:    "pages/approvals/approvals",
./findings.md:6:- `state.json` currently reports `TASK-20260530-06` completed at event 58.
./findings.md:12:- Claude disputes my previous priority/time estimates for security tests, state validation, contract capture, and total duration.
./findings.md:14:- Code inspection shows both approve and reject views already contain inline step/status guards; the right compromise is to extract/reuse a validator and prove it with tests, not a large state-machine redesign.
./findings.md:17:- `backend/apps/approvals/views.py` has role checks, assigned approver check, duplicate-decision check, and inline status/step matching for both approve and reject.
./findings.md:18:- `backend/apps/approvals/tests/test_permissions.py` currently covers cross-counselor approve/reject only.
./findings.md:19:- `backend/apps/approvals/tests/test_state_machine.py` currently covers duplicate approve only.
./findings.md:20:- `backend/apps/applications/views.py` allows resubmission after rejected status because duplicate prevention blocks pending/approved only.
./findings.md:21:- `Application.clean()` mirrors duplicate prevention for pending/approved states.
./backend/config/urls.py:9:    path('api/approvals/', include('apps.approvals.urls')),
./miniprogram/pages/approvals/approvals.ts:10:    approvals: [] as ApprovalListItem[],
./miniprogram/pages/approvals/approvals.ts:45:        approvals: res.results,
./miniprogram/pages/approvals/approvals.wxml:3:    <text class="title">待审批列表</text>
./miniprogram/pages/approvals/approvals.wxml:7:  <view class="list" wx:if="{{!loading && approvals.length > 0}}">
./miniprogram/pages/approvals/approvals.wxml:8:    <view class="item" wx:for="{{approvals}}" wx:key="approval_id" bindtap="onItemTap" data-id="{{item.application_id}}">
./miniprogram/pages/approvals/approvals.wxml:11:        <text class="status pending">待审批</text>
./miniprogram/pages/approvals/approvals.wxml:18:        <text class="label">审批步骤:</text>
./miniprogram/pages/approvals/approvals.wxml:27:  <view class="empty" wx:if="{{!loading && approvals.length === 0}}">
./miniprogram/pages/approvals/approvals.wxml:28:    <text>暂无待审批项</text>
./tests/test_p0_fixes.sh:2:# Test P0 fixes: resubmission after rejection + approval history filter
./tests/test_p0_fixes.sh:25:  -d "{\"reason\":\"第一次申请\",\"leave_date\":\"$LEAVE_DATE\"}" | jq -r '.application_id')
./tests/test_p0_fixes.sh:33:  -d "{\"reason\":\"重复申请\",\"leave_date\":\"$LEAVE_DATE\"}")
./tests/test_p0_fixes.sh:42:APPROVAL_ID=$(curl -s -X GET "$BASE_URL/api/approvals/" \
./tests/test_p0_fixes.sh:43:  -H "Authorization: Bearer $COUNSELOR_TOKEN" | jq -r '.results[0].approval_id')
./tests/test_p0_fixes.sh:45:curl -s -X POST "$BASE_URL/api/approvals/$APPROVAL_ID/reject/" \
./tests/test_p0_fixes.sh:50:echo "   Rejected approval: $APPROVAL_ID"
./tests/test_p0_fixes.sh:57:  -d "{\"reason\":\"修改后重新申请\",\"leave_date\":\"$LEAVE_DATE\"}" | jq -r '.application_id')
./tests/test_p0_fixes.sh:66:# Test approval history filter
./tests/test_p0_fixes.sh:67:echo "7. Testing approval history filter..."
./tests/test_p0_fixes.sh:69:# Pending approvals (default)
./tests/test_p0_fixes.sh:70:PENDING_COUNT=$(curl -s -X GET "$BASE_URL/api/approvals/" \
./tests/test_p0_fixes.sh:72:echo "   Pending approvals: $PENDING_COUNT"
./tests/test_p0_fixes.sh:74:# Rejected approvals
./tests/test_p0_fixes.sh:75:REJECTED_COUNT=$(curl -s -X GET "$BASE_URL/api/approvals/?decision=rejected" \
./tests/test_p0_fixes.sh:77:echo "   Rejected approvals: $REJECTED_COUNT"
./tests/test_p0_fixes.sh:79:# All approvals
./tests/test_p0_fixes.sh:80:ALL_COUNT=$(curl -s -X GET "$BASE_URL/api/approvals/?decision=all" \
./tests/test_p0_fixes.sh:82:echo "   All approvals: $ALL_COUNT"
./docs/api/contract-v0.2.md:19:| `pending_counselor` | Awaiting counselor approval | 待辅导员审批 |
./docs/api/contract-v0.2.md:20:| `pending_dean` | Awaiting dean approval | 待学工部审批 |
./docs/api/contract-v0.2.md:26:**Location:** `backend/apps/approvals/models.py`
./docs/api/contract-v0.2.md:30:| `pending` | Pending approval | 待审批 |
./docs/api/contract-v0.2.md:36:**Location:** `backend/apps/approvals/models.py`
./docs/api/contract-v0.2.md:40:| `counselor` | Counselor approval step | 辅导员审批 |
./docs/api/contract-v0.2.md:41:| `dean` | Dean approval step | 学工部审批 |
./docs/api/contract-v0.2.md:81:| `pending_counselor` | `pending_dean` | Counselor approves | Creates dean approval |
./docs/api/contract-v0.2.md:82:| `pending_counselor` | `rejected` | Counselor rejects | Terminal state |
./docs/api/contract-v0.2.md:83:| `pending_dean` | `approved` | Dean approves | Terminal state |
./docs/api/contract-v0.2.md:84:| `pending_dean` | `rejected` | Dean rejects | Terminal state |
./docs/api/contract-v0.2.md:85:| `rejected` | `pending_counselor` | Student resubmits | New approval cycle |
./docs/api/contract-v0.2.md:89:**Terminal states:** `approved`, `rejected`
./docs/api/contract-v0.2.md:92:- No further approve/reject operations allowed on terminal state applications
./docs/api/contract-v0.2.md:93:- Attempting operations on terminal states returns `409 CONFLICT`
./docs/api/contract-v0.2.md:94:- Resubmission from `rejected` creates new application cycle with new approvals
./docs/api/contract-v0.2.md:99:- Counselor approval requires `application.status == pending_counselor`
./docs/api/contract-v0.2.md:100:- Dean approval requires `application.status == pending_dean`
./docs/api/contract-v0.2.md:104:- Once `approval.decision != pending`, no further operations allowed
./docs/api/contract-v0.2.md:108:- Counselor approval must complete before dean approval
./docs/api/contract-v0.2.md:121:| View approval list | ❌ | ✅ | ✅ | Only assigned approvals |
./docs/api/contract-v0.2.md:135:- Operations require `approval.approver_id == user.user_id`
./docs/api/contract-v0.2.md:225:      "leave_date": ["This field is required."]
./docs/api/contract-v0.2.md:237:POST /api/approvals/apv_001/approve/
./docs/api/contract-v0.2.md:256:**Scenario 2:** Cross-counselor approval attempt
./docs/api/contract-v0.2.md:260:POST /api/approvals/apv_001/approve/
./docs/api/contract-v0.2.md:281:**Scenario:** Invalid approval ID
./docs/api/contract-v0.2.md:285:POST /api/approvals/invalid_id/approve/
./docs/api/contract-v0.2.md:294:    "message": "审批记录不存在"
./docs/api/contract-v0.2.md:311:  "leave_date": "2024-06-30"
./docs/api/contract-v0.2.md:320:    "message": "已有待审批或已通过的申请，不能重复提交",
./docs/api/contract-v0.2.md:324:      "status": "pending_counselor"
./docs/api/contract-v0.2.md:330:**Scenario 2:** Duplicate approval
./docs/api/contract-v0.2.md:334:POST /api/approvals/apv_001/approve/
./docs/api/contract-v0.2.md:348:    "message": "审批已完成，不能重复操作"
./docs/api/contract-v0.2.md:357:POST /api/approvals/apv_001/approve/
./docs/api/contract-v0.2.md:366:**Response (when application.status != pending_counselor):**
./docs/api/contract-v0.2.md:371:    "message": "申请状态与审批步骤不匹配"
./docs/api/contract-v0.2.md:388:  "leave_date": "2024-06-30"
./docs/api/contract-v0.2.md:400:      "dorm_status": "pending",
./docs/api/contract-v0.2.md:421:  "leave_date": "2024-06-30"
./docs/api/contract-v0.2.md:433:  "leave_date": "2024-06-30",
./docs/api/contract-v0.2.md:434:  "status": "pending_counselor",
./docs/api/contract-v0.2.md:435:  "dorm_checkout_status": "completed",
./docs/api/contract-v0.2.md:436:  "approvals": [
./docs/api/contract-v0.2.md:438:      "approval_id": "apv_xyz789",
./docs/api/contract-v0.2.md:469:  "leave_date": "2024-06-30",
./docs/api/contract-v0.2.md:470:  "status": "pending_dean",
./docs/api/contract-v0.2.md:471:  "dorm_checkout_status": "completed",
./docs/api/contract-v0.2.md:472:  "approvals": [
./docs/api/contract-v0.2.md:474:      "approval_id": "apv_xyz789",
./docs/api/contract-v0.2.md:484:      "approval_id": "apv_def456",
./docs/api/contract-v0.2.md:499:### 7.3 GET /api/approvals/ - List Approvals (Paginated)
./docs/api/contract-v0.2.md:503:GET /api/approvals/?decision=pending&limit=20&offset=0
./docs/api/contract-v0.2.md:513:      "approval_id": "apv_xyz789",
./docs/api/contract-v0.2.md:522:      "approval_id": "apv_ghi012",
./docs/api/contract-v0.2.md:539:### 7.4 POST /api/approvals/{id}/approve/ - Approve
./docs/api/contract-v0.2.md:543:POST /api/approvals/apv_xyz789/approve/
./docs/api/contract-v0.2.md:555:  "approval_id": "apv_xyz789",
./docs/api/contract-v0.2.md:566:### 7.5 POST /api/approvals/{id}/reject/ - Reject
./docs/api/contract-v0.2.md:570:POST /api/approvals/apv_xyz789/reject/
./docs/api/contract-v0.2.md:582:  "approval_id": "apv_xyz789",
./docs/api/contract-v0.2.md:601:GET /api/approvals/?decision=pending
./docs/api/contract-v0.2.md:617:GET /api/approvals/?limit=20&offset=1000
./tests/smoke_test.sh:35:  -d "{\"reason\":\"毕业离校\",\"leave_date\":\"$LEAVE_DATE\"}")
./tests/smoke_test.sh:38:APP_STATUS=$(echo "$APP_RESPONSE" | jq -r '.status')
./tests/smoke_test.sh:47:  echo "✗ Application status wrong: $APP_STATUS (expected: pending_counselor)"
./tests/smoke_test.sh:51:echo "✓ Application submitted: $APP_ID (status: $APP_STATUS)"
./tests/smoke_test.sh:53:# Extract counselor approval ID
./tests/smoke_test.sh:54:COUNSELOR_APPROVAL_ID=$(echo "$APP_RESPONSE" | jq -r '.approvals[] | select(.step=="counselor") | .approval_id')
./tests/smoke_test.sh:57:  echo "✗ Counselor approval not created"
./tests/smoke_test.sh:61:echo "  Counselor approval: $COUNSELOR_APPROVAL_ID"
./tests/smoke_test.sh:78:APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$COUNSELOR_APPROVAL_ID/approve/" \
./tests/smoke_test.sh:93:# Verify application status changed
./tests/smoke_test.sh:96:  | jq -r '.status')
./tests/smoke_test.sh:99:  echo "✗ Application status not updated: $APP_STATUS_AFTER (expected: pending_dean)"
./tests/smoke_test.sh:103:echo "  Application status: $APP_STATUS_AFTER"
./tests/smoke_test.sh:105:# Extract dean approval ID
./tests/smoke_test.sh:108:  | jq -r '.approvals[] | select(.step=="dean") | .approval_id')
./tests/smoke_test.sh:111:  echo "✗ Dean approval not created"
./tests/smoke_test.sh:115:echo "  Dean approval: $DEAN_APPROVAL_ID"
./tests/smoke_test.sh:132:DEAN_APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$DEAN_APPROVAL_ID/approve/" \
./tests/smoke_test.sh:147:# 7. Verify final status
./tests/smoke_test.sh:148:echo "7. Verify final status..."
./tests/smoke_test.sh:151:  | jq -r '.status')
./tests/smoke_test.sh:154:  echo "✗ Final status wrong: $FINAL_STATUS (expected: approved)"
./tests/smoke_test.sh:158:echo "✓ Final status: $FINAL_STATUS"
./tests/smoke_test.sh:161:echo "--- N2: Cross-counselor approval (negative test) ---"
./tests/smoke_test.sh:163:# N2: T002 tries to approve T001's approval (should fail)
./tests/smoke_test.sh:194:  -d "{\"reason\":\"测试跨班级审批\",\"leave_date\":\"$LEAVE_DATE\"}")
./tests/smoke_test.sh:197:TEST_COUNSELOR_APPROVAL=$(echo "$TEST_APP_RESPONSE" | jq -r '.approvals[] | select(.step=="counselor") | .approval_id')
./tests/smoke_test.sh:200:echo "  Test approval (T002): $TEST_COUNSELOR_APPROVAL"
./tests/smoke_test.sh:202:# T002 tries to approve T001's approval
./tests/smoke_test.sh:203:echo "10. T002 tries to approve T001's approval (should fail)..."
./tests/smoke_test.sh:204:CROSS_APPROVE_STATUS=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/approvals/$COUNSELOR_APPROVAL_ID/approve/" \
./tests/smoke_test.sh:207:  -d '{"comment":"尝试跨班级审批"}' \
./docs/week3-day0-seed-data-requirements.md:4:**目标：** 支持最小闭环验证（登录→提交→审批→查询）
./docs/week3-day0-seed-data-requirements.md:35:- 学生1提交申请，辅导员1审批
./docs/week3-day0-seed-data-requirements.md:36:- 学生2提交申请，辅导员2审批
./docs/week3-day0-seed-data-requirements.md:44:**用途：** 测试辅导员审批、班级映射
./docs/week3-day0-seed-data-requirements.md:54:- 辅导员1只能审批CS2020-01班级的申请
./docs/week3-day0-seed-data-requirements.md:55:- 辅导员2只能审批CS2020-02班级的申请
./docs/week3-day0-seed-data-requirements.md:56:- 辅导员不能审批其他班级的申请（负向权限验证）
./docs/week3-day0-seed-data-requirements.md:63:**用途：** 测试学工部审批
./docs/week3-day0-seed-data-requirements.md:73:- 学工部能审批所有通过辅导员审批的申请
./docs/week3-day0-seed-data-requirements.md:74:- 学工部不能直接审批pending_counselor状态的申请
./docs/week3-day0-seed-data-requirements.md:96:### 宿舍清退状态（DormCheckoutProvider）
./docs/week3-day0-seed-data-requirements.md:100:| student_id | dorm_checkout_status | 用途 |
./docs/week3-day0-seed-data-requirements.md:172:### 历史数据（状态测试）
./docs/week3-day0-seed-data-requirements.md:179:**文档状态：** 已完成  
./miniprogram/pages/approvals/approvals.wxss:50:.status {
./miniprogram/pages/approvals/approvals.wxss:56:.status.pending {
./backend/config/settings/base.py:2:Django settings for graduation leave system project.
./backend/config/settings/base.py:35:    'apps.approvals',
./backend/config/settings/base.py:73:        'NAME': config('DB_NAME', default='graduation_leave'),
./backend/config/settings/base.py:94:TIME_ZONE = 'Asia/Shanghai'
./docs/week3-day0-acceptance-checklist.md:5:**范围：** 登录 → 提交 → 辅导员审批 → 学工部审批 → 查询状态
./docs/week3-day0-acceptance-checklist.md:20:- [ ] 所有表创建成功（users, applications, approvals, class_mappings）
./docs/week3-day0-acceptance-checklist.md:30:### 2. Seed数据足以支持两级审批 ✓/✗
./docs/week3-day0-acceptance-checklist.md:91:    "leave_date": "2024-07-01"
./docs/week3-day0-acceptance-checklist.md:100:  "status": "pending_counselor",
./docs/week3-day0-acceptance-checklist.md:101:  "dorm_checkout_status": "completed"
./docs/week3-day0-acceptance-checklist.md:108:- [ ] 状态为pending_counselor
./docs/week3-day0-acceptance-checklist.md:109:- [ ] 宿舍清退状态为completed
./docs/week3-day0-acceptance-checklist.md:118:### 4. 辅导员能审批对应学生申请 ✓/✗
./docs/week3-day0-acceptance-checklist.md:129:**Step 2: 审批申请**
./docs/week3-day0-acceptance-checklist.md:131:curl -X POST http://localhost:8000/api/approvals/1/approve \
./docs/week3-day0-acceptance-checklist.md:140:  "approval_id": 1,
./docs/week3-day0-acceptance-checklist.md:148:**Step 3: 验证申请状态变更**
./docs/week3-day0-acceptance-checklist.md:158:  "status": "pending_dean",
./docs/week3-day0-acceptance-checklist.md:159:  "approvals": [
./docs/week3-day0-acceptance-checklist.md:171:- [ ] 审批操作成功
./docs/week3-day0-acceptance-checklist.md:172:- [ ] 申请状态从pending_counselor变为pending_dean
./docs/week3-day0-acceptance-checklist.md:173:- [ ] 审批记录正确创建
./docs/week3-day0-acceptance-checklist.md:178:- 状态未变更：检查状态机逻辑
./docs/week3-day0-acceptance-checklist.md:182:### 5. 学工部能进行最终审批 ✓/✗
./docs/week3-day0-acceptance-checklist.md:193:**Step 2: 审批申请**
./docs/week3-day0-acceptance-checklist.md:195:curl -X POST http://localhost:8000/api/approvals/2/approve \
./docs/week3-day0-acceptance-checklist.md:204:  "approval_id": 2,
./docs/week3-day0-acceptance-checklist.md:212:**Step 3: 验证最终状态**
./docs/week3-day0-acceptance-checklist.md:222:  "status": "approved",
./docs/week3-day0-acceptance-checklist.md:223:  "approvals": [
./docs/week3-day0-acceptance-checklist.md:238:- [ ] 审批操作成功
./docs/week3-day0-acceptance-checklist.md:239:- [ ] 申请状态从pending_dean变为approved
./docs/week3-day0-acceptance-checklist.md:240:- [ ] 两条审批记录都存在
./docs/week3-day0-acceptance-checklist.md:244:- 检查状态机最终状态逻辑
./docs/week3-day0-acceptance-checklist.md:248:### 6. 学生能查询最终状态 ✓/✗
./docs/week3-day0-acceptance-checklist.md:261:  "status": "approved",
./docs/week3-day0-acceptance-checklist.md:263:  "leave_date": "2024-07-01",
./docs/week3-day0-acceptance-checklist.md:264:  "dorm_checkout_status": "completed",
./docs/week3-day0-acceptance-checklist.md:265:  "approvals": [
./docs/week3-day0-acceptance-checklist.md:286:- [ ] 状态显示正确（approved）
./docs/week3-day0-acceptance-checklist.md:287:- [ ] 审批历史完整
./docs/week3-day0-acceptance-checklist.md:292:- 检查审批记录关联
./docs/week3-day0-acceptance-checklist.md:320:**HTTP状态码：** 403
./docs/week3-day0-acceptance-checklist.md:337:**HTTP状态码：** 403
./docs/week3-day0-acceptance-checklist.md:362:- [ ] check_status方法实现
./docs/week3-day0-acceptance-checklist.md:363:- [ ] 返回completed状态（对于2020001、2020002）
./docs/week3-day0-acceptance-checklist.md:373:    "leave_date": "2024-07-01"
./docs/week3-day0-acceptance-checklist.md:381:  "dorm_checkout_status": "completed"
./docs/week3-day0-acceptance-checklist.md:393:- [ ] check_status方法签名
./docs/week3-day0-acceptance-checklist.md:398:- [ ] Mock返回completed状态
./docs/week3-day0-acceptance-checklist.md:433:  -d '{"reason": "毕业离校", "leave_date": "2024-07-01"}' \
./docs/week3-day0-acceptance-checklist.md:438:# 3. 辅导员审批
./docs/week3-day0-acceptance-checklist.md:444:curl -s -X POST http://localhost:8000/api/approvals/1/approve \
./docs/week3-day0-acceptance-checklist.md:449:echo "✓ 辅导员审批成功"
./docs/week3-day0-acceptance-checklist.md:451:# 4. 学工部审批
./docs/week3-day0-acceptance-checklist.md:457:curl -s -X POST http://localhost:8000/api/approvals/2/approve \
./docs/week3-day0-acceptance-checklist.md:462:echo "✓ 学工部审批成功"
./docs/week3-day0-acceptance-checklist.md:464:# 5. 查询最终状态
./docs/week3-day0-acceptance-checklist.md:467:  | jq -r '.status')
./docs/week3-day0-acceptance-checklist.md:470:  echo "✓ 最终状态正确: approved"
./docs/week3-day0-acceptance-checklist.md:472:  echo "✗ 最终状态错误: $STATUS"
./docs/week3-day0-acceptance-checklist.md:495:4. 辅导员审批
./docs/week3-day0-acceptance-checklist.md:497:6. 学工部审批
./docs/week3-day0-acceptance-checklist.md:498:7. 查询最终状态
./docs/week3-day0-acceptance-checklist.md:517:- 审批操作失败
./docs/week3-day0-acceptance-checklist.md:518:- 状态机不工作
./docs/week3-day0-acceptance-checklist.md:523:- 审批记录缺失字段
./docs/week3-day0-acceptance-checklist.md:546:- **停止并重设计**：发现架构级阻塞（状态机错误、数据模型缺陷、契约冲突）
./docs/week3-day0-acceptance-checklist.md:550:**文档状态：** 已完成  
./docs/week3-day0-acceptance-checklist.md:551:**Day 0准备状态：** 全部完成（环境策略、seed数据、验收清单）  
./miniprogram/pages/student-application/student-application.wxml:20:        value="{{leaveDate}}"
./miniprogram/pages/student-application/student-application.wxml:24:        <view class="picker">{{leaveDate || '请选择日期'}}</view>
./backend/config/wsgi.py:1:"""WSGI config for graduation leave system project."""
./miniprogram/pages/student-application/student-application.ts:11:    leaveDate: '',
./miniprogram/pages/student-application/student-application.ts:31:    this.setData({ leaveDate: e.detail.value });
./miniprogram/pages/student-application/student-application.ts:35:    const { reason, leaveDate } = this.data;
./miniprogram/pages/student-application/student-application.ts:45:    if (!leaveDate) {
./miniprogram/pages/student-application/student-application.ts:50:    if (leaveDate < today) {
./miniprogram/pages/student-application/student-application.ts:65:        leave_date: this.data.leaveDate
./miniprogram/pages/student-application/student-application.ts:87:            return '您已有待审批或已通过的申请，正在跳转...';
./miniprogram/pages/student-application/student-application.ts:89:          return '您已有待审批或已通过的申请';
./docs/templates/宿舍清退数据模板.csv:1:学号,姓名,班级,宿舍楼栋,宿舍房间号,床号,是否已清退,清退日期,清退状态,备注
./frontend/services/mock.ts:43:      leave_date: '2024-06-30',
./frontend/services/mock.ts:44:      status: 'pending_counselor',
./frontend/services/mock.ts:57:  leave_date: '2024-06-30',
./frontend/services/mock.ts:58:  status: 'pending_counselor',
./frontend/services/mock.ts:59:  dorm_checkout_status: 'completed',
./frontend/services/mock.ts:60:  approvals: [
./frontend/services/mock.ts:62:      approval_id: 'apv_c9f566c2',
./frontend/services/mock.ts:80:      approval_id: 'apv_c9f566c2',
./miniprogram/pages/login/login.ts:43:        wx.redirectTo({ url: '/pages/approvals/approvals' });
./frontend/services/api.ts:49:    if (response.status === 401) {
./frontend/services/api.ts:99:      `/api/approvals/?decision=${decision}&limit=${limit}&offset=${offset}`
./frontend/services/api.ts:107:    return this.request(`/api/approvals/${id}/approve/`, {
./frontend/services/api.ts:117:    return this.request(`/api/approvals/${id}/reject/`, {
./backend/apps/approvals/validators.py:10:def approval_step_matches_application_status(approval):
./backend/apps/approvals/validators.py:11:    expected_status = EXPECTED_STATUS_BY_STEP.get(approval.step)
./backend/apps/approvals/validators.py:12:    if expected_status is None:
./backend/apps/approvals/validators.py:14:    return approval.application.status == expected_status
./miniprogram/utils/date.ts:1:// Asia/Shanghai timezone date helper
./miniprogram/utils/date.ts:2:// Aligns with backend TIME_ZONE = 'Asia/Shanghai'
./docs/week3-day0-environment-strategy.md:110:**决策状态：** 已确认  
./miniprogram/utils/role-guard.ts:21:      : '/pages/approvals/approvals';
./frontend/types/api.ts:39:  leave_date: string; // YYYY-MM-DD
./frontend/types/api.ts:48:  leave_date: string;
./frontend/types/api.ts:49:  status: ApplicationStatus;
./frontend/types/api.ts:55:  dorm_checkout_status: string;
./frontend/types/api.ts:56:  approvals: ApprovalDetail[];
./frontend/types/api.ts:61:  approval_id: string;
./frontend/types/api.ts:72:  approval_id: string;
./frontend/types/api.ts:86:  approval_id: string;
./backend/apps/approvals/admin.py:7:    list_display = ['approval_id', 'application', 'step', 'approver', 'decision', 'decided_at']
./backend/apps/approvals/admin.py:9:    search_fields = ['approval_id', 'application__application_id', 'approver__user_id']
./docs/用户设计说明书.md:1:# 毕业生离校申请审批系统 - 用户设计说明书
./docs/用户设计说明书.md:13:本系统旨在实现毕业生离校申请的在线化、规范化管理，替代传统纸质审批流程，提高审批效率，减少人工成本。
./docs/用户设计说明书.md:17:- **学生端：** 在线提交离校申请、上传证明材料、查看审批进度、接收审批通知
./docs/用户设计说明书.md:18:- **辅导员端：** 审批本年级学生的离校申请、查看审批历史、接收待办提醒
./docs/用户设计说明书.md:19:- **学工部端：** 审批所有学生的离校申请、查看全校审批统计、导出审批数据
./docs/用户设计说明书.md:35:学生登录 → 填写申请信息 → 上传证明材料 → 提交申请 → 等待审批
./docs/用户设计说明书.md:48:### 2.2 审批流程
./docs/用户设计说明书.md:51:学生提交 → 辅导员审批 → 学工部审批 → 审批完成
./docs/用户设计说明书.md:56:**审批时限：**
./docs/用户设计说明书.md:57:- 辅导员审批：提交后1个工作日内
./docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
./docs/用户设计说明书.md:61:**审批结果：**
./docs/用户设计说明书.md:62:- **通过：** 进入下一审批环节或完成审批
./docs/用户设计说明书.md:69:- 辅导员审批通过 → 通知学生和学工部
./docs/用户设计说明书.md:71:- 学工部审批通过 → 通知学生（审批完成）
./docs/用户设计说明书.md:73:- 审批超时 → 通知审批人
./docs/用户设计说明书.md:128:| **辅导员** | 本年级学生 | 审批申请、查看历史、接收通知 |
./docs/用户设计说明书.md:129:| **学工部** | 全校学生 | 审批申请、查看统计、导出数据 |
./docs/用户设计说明书.md:136:- ✓ 修改草稿状态的申请
./docs/用户设计说明书.md:140:- ✓ 查看审批历史
./docs/用户设计说明书.md:145:- ✓ 审批负责班级学生的申请（通过/驳回）
./docs/用户设计说明书.md:146:- ✓ 填写审批意见
./docs/用户设计说明书.md:147:- ✓ 查看审批历史
./docs/用户设计说明书.md:148:- ✓ 接收待审批通知
./docs/用户设计说明书.md:149:- ✗ 审批其他班级学生
./docs/用户设计说明书.md:153:- ✓ 审批所有学生的申请（通过/驳回）
./docs/用户设计说明书.md:154:- ✓ 填写审批意见
./docs/用户设计说明书.md:155:- ✓ 查看全校审批统计
./docs/用户设计说明书.md:156:- ✓ 导出审批数据（Excel）
./docs/用户设计说明书.md:157:- ✓ 查看审批历史
./docs/用户设计说明书.md:218:**Q5：审批进度在哪里查看？**
./docs/用户设计说明书.md:219:A：登录后在"我的申请"列表中查看，点击详情可查看审批历史。
./docs/用户设计说明书.md:221:### 6.2 审批人常见问题
./docs/用户设计说明书.md:223:**Q1：如何查看待审批申请？**
./docs/用户设计说明书.md:224:A：登录后在"待审批"列表中查看，点击进入审批页面。
./docs/用户设计说明书.md:226:**Q2：审批意见是否必填？**
./docs/用户设计说明书.md:229:**Q3：审批后能否撤销？**
./docs/用户设计说明书.md:230:A：审批后不能撤销，如需修改请联系系统管理员。
./docs/用户设计说明书.md:232:**Q4：如何导出审批数据？**
./docs/用户设计说明书.md:233:A：学工部用户在"审批统计"页面点击"导出Excel"按钮。
./docs/用户设计说明书.md:240:**Q2：如何修改审批时限？**
./docs/用户设计说明书.md:241:A：在系统配置页面修改"审批时限"参数（单位：小时）。
./docs/用户设计说明书.md:287:2. **辅导员基本信息** - 创建辅导员账号，让辅导员能够审批申请
./docs/用户设计说明书.md:288:3. **班级-辅导员对应关系** - 系统自动分配审批人，学生提交申请时自动找到对应的辅导员
./docs/用户设计说明书.md:374:- 清退状态（已完成/进行中/未开始）
./docs/用户设计说明书.md:398:- 系统自动分配对应的辅导员审批
./docs/用户设计说明书.md:403:- 可以进行审批操作
./backend/apps/approvals/urls.py:5:    path('', views.list_approvals, name='list_approvals'),
./backend/apps/approvals/urls.py:6:    path('<str:approval_id>/approve/', views.approve_approval, name='approve_approval'),
./backend/apps/approvals/urls.py:7:    path('<str:approval_id>/reject/', views.reject_approval, name='reject_approval'),
./miniprogram/pages/detail/detail.ts:13:    statusText: '',
./miniprogram/pages/detail/detail.ts:15:      pending: '待审批',
./miniprogram/pages/detail/detail.ts:46:      const statusMap: Record<string, string> = {
./miniprogram/pages/detail/detail.ts:48:        pending_counselor: '待辅导员审批',
./miniprogram/pages/detail/detail.ts:49:        pending_dean: '待院长审批',
./miniprogram/pages/detail/detail.ts:55:      const pendingApproval = detail.approvals.find(
./miniprogram/pages/detail/detail.ts:61:        statusText: statusMap[detail.status] || detail.status,
./miniprogram/pages/detail/detail.ts:63:        pendingApprovalId: pendingApproval?.approval_id || '',
./miniprogram/pages/detail/detail.ts:102:      const approvalId = this.data.pendingApprovalId;
./miniprogram/pages/detail/detail.ts:105:        await apiClient.approveApproval(approvalId, { comment: '' });
./miniprogram/pages/detail/detail.ts:107:        await apiClient.rejectApproval(approvalId, { comment: '' });
./docs/contracts/contract-v0.2.md:4:**状态：** Week 3 closure baseline  
./docs/contracts/contract-v0.2.md:7:**范围：** 登录、申请提交/查询、审批列表/通过/驳回、错误响应、分页、权限与状态机  
./docs/contracts/contract-v0.2.md:43:  "leave_date": "2024-06-30",
./docs/contracts/contract-v0.2.md:44:  "status": "pending_counselor",
./docs/contracts/contract-v0.2.md:56:  "dorm_checkout_status": "completed",
./docs/contracts/contract-v0.2.md:57:  "approvals": [
./docs/contracts/contract-v0.2.md:59:      "approval_id": "apv_c9f566c2",
./docs/contracts/contract-v0.2.md:76:  "approval_id": "apv_c9f566c2",
./docs/contracts/contract-v0.2.md:90:  "approval_id": "apv_c9f566c2",
./docs/contracts/contract-v0.2.md:114:## 4. 状态机
./docs/contracts/contract-v0.2.md:116:| 当前状态 | 动作 | 角色 | 审批步骤 | 下一状态 | 副作用 |
./docs/contracts/contract-v0.2.md:118:| - | 提交申请 | student | - | pending_counselor | 创建 counselor 审批 |
./docs/contracts/contract-v0.2.md:119:| pending_counselor | 通过 | counselor | counselor | pending_dean | 创建 dean 审批 |
./docs/contracts/contract-v0.2.md:124:状态保护：
./docs/contracts/contract-v0.2.md:126:- 审批记录必须仍为 `pending`，否则返回 `409 CONFLICT`。
./docs/contracts/contract-v0.2.md:127:- `counselor` 审批只能处理 `pending_counselor` 申请。
./docs/contracts/contract-v0.2.md:128:- `dean` 审批只能处理 `pending_dean` 申请。
./docs/contracts/contract-v0.2.md:138:| 申请列表 | 仅本人申请 | 仅本人待处理 counselor 审批对应申请 | 仅本人待处理 dean 审批对应申请 |
./docs/contracts/contract-v0.2.md:139:| 申请详情 | 仅本人申请 | 仅负责班级申请 | 仅本人待处理 dean 审批对应申请 |
./docs/contracts/contract-v0.2.md:140:| 审批列表 | 禁止 | 仅本人 counselor 审批 | 仅本人 dean 审批 |
./docs/contracts/contract-v0.2.md:141:| counselor 审批动作 | 禁止 | 仅指定 approver | 禁止 |
./docs/contracts/contract-v0.2.md:142:| dean 审批动作 | 禁止 | 禁止 | 仅指定 approver |
./docs/contracts/contract-v0.2.md:174:{"reason":"毕业离校","leave_date":"2024-06-30"}
./docs/contracts/contract-v0.2.md:187:### GET `/api/approvals/?decision=pending&limit=20&offset=0`
./docs/contracts/contract-v0.2.md:193:### POST `/api/approvals/{approval_id}/approve/`
./docs/contracts/contract-v0.2.md:203:### POST `/api/approvals/{approval_id}/reject/`
./docs/contracts/contract-v0.2.md:235:| FORBIDDEN | 403 | 角色不符、非指定审批人、越权访问 |
./docs/contracts/contract-v0.2.md:236:| NOT_FOUND | 404 | 申请或审批记录不存在 |
./docs/contracts/contract-v0.2.md:237:| CONFLICT | 409 | 重复提交、重复审批、状态与审批步骤不匹配 |
./docs/Codex审查流程指南.md:178:**状态：** 已修复/通过
./miniprogram/pages/detail/detail.wxml:23:        <text class="value">{{detail.leave_date}}</text>
./miniprogram/pages/detail/detail.wxml:30:        <text class="label">状态:</text>
./miniprogram/pages/detail/detail.wxml:31:        <text class="value status-{{detail.status}}">{{statusText}}</text>
./miniprogram/pages/detail/detail.wxml:36:      <text class="section-title">审批记录</text>
./miniprogram/pages/detail/detail.wxml:37:      <view class="approval-item" wx:for="{{detail.approvals}}" wx:key="approval_id">
./miniprogram/pages/detail/detail.wxml:38:        <view class="approval-header">
./miniprogram/pages/detail/detail.wxml:42:        <view class="approval-body">
./miniprogram/pages/detail/detail.wxml:43:          <text class="approver">审批人: {{item.approver_name}}</text>
./backend/apps/approvals/migrations/0002_initial.py:14:        ('approvals', '0001_initial'),
./backend/apps/approvals/migrations/0002_initial.py:19:            model_name='approval',
./backend/apps/approvals/migrations/0002_initial.py:21:            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='approvals', to=settings.AUTH_USER_MODEL),
./docs/contracts/contract-v0.1.md:4:**状态：** ✅ 已冻结（可执行契约标准）  
./docs/contracts/contract-v0.1.md:40:    leave_date: str                  # 计划离校日期 (YYYY-MM-DD)
./docs/contracts/contract-v0.1.md:41:    status: ApplicationStatus
./docs/contracts/contract-v0.1.md:42:    dorm_checkout_status: DormCheckoutStatus
./docs/contracts/contract-v0.1.md:52:    """审批记录数据传输对象"""
./docs/contracts/contract-v0.1.md:53:    approval_id: str
./docs/contracts/contract-v0.1.md:68:    """宿舍清退状态数据传输对象"""
./docs/contracts/contract-v0.1.md:70:    status: DormCheckoutStatus   # completed/pending/not_started/unknown
./docs/contracts/contract-v0.1.md:78:## 2. 状态枚举
./docs/contracts/contract-v0.1.md:94:    PENDING_COUNSELOR = "pending_counselor"  # 待辅导员审批
./docs/contracts/contract-v0.1.md:95:    PENDING_DEAN = "pending_dean"        # 待学工部审批
./docs/contracts/contract-v0.1.md:124:    UNKNOWN = "unknown"              # 状态未知（API失败）
./docs/contracts/contract-v0.1.md:127:### 2.6 状态机契约
./docs/contracts/contract-v0.1.md:129:**申请状态流转规则：**
./docs/contracts/contract-v0.1.md:131:| 当前状态 | 触发动作 | 角色 | 下一状态 | 副作用 |
./docs/contracts/contract-v0.1.md:133:| - | 学生提交申请 | student | pending_counselor | 创建辅导员审批记录 |
./docs/contracts/contract-v0.1.md:134:| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
./docs/contracts/contract-v0.1.md:139:**宿舍清退状态处理规则：**
./docs/contracts/contract-v0.1.md:141:| 宿舍状态 | 提交申请行为 | HTTP状态 | 错误码 |
./docs/contracts/contract-v0.1.md:155:| 辅导员审批 | ✗ | ✓（本班级） | ✗ |
./docs/contracts/contract-v0.1.md:156:| 学工部审批 | ✗ | ✗ | ✓（所有） |
./docs/contracts/contract-v0.1.md:164:| 错误码 | HTTP状态 | 说明 | 示例场景 |
./docs/contracts/contract-v0.1.md:175:| 错误码 | HTTP状态 | 说明 | 示例场景 |
./docs/contracts/contract-v0.1.md:189:      "dorm_status": "pending"
./docs/contracts/contract-v0.1.md:235:  "leave_date": "2024-06-30"
./docs/contracts/contract-v0.1.md:247:  "leave_date": "2024-06-30",
./docs/contracts/contract-v0.1.md:248:  "status": "pending_counselor",
./docs/contracts/contract-v0.1.md:249:  "dorm_checkout_status": "completed",
./docs/contracts/contract-v0.1.md:265:  "leave_date": "2024-06-30",
./docs/contracts/contract-v0.1.md:266:  "status": "pending_counselor",
./docs/contracts/contract-v0.1.md:267:  "dorm_checkout_status": "completed",
./docs/contracts/contract-v0.1.md:268:  "approvals": [
./docs/contracts/contract-v0.1.md:270:      "approval_id": "apv_001",
./docs/contracts/contract-v0.1.md:284:### 4.3 审批
./docs/contracts/contract-v0.1.md:286:#### POST /api/approvals/{approval_id}/approve
./docs/contracts/contract-v0.1.md:298:  "approval_id": "apv_001",
./docs/contracts/contract-v0.1.md:309:#### POST /api/approvals/{approval_id}/reject
./docs/contracts/contract-v0.1.md:321:  "approval_id": "apv_001",
./docs/contracts/contract-v0.1.md:411:    def check_status(self, student_id: str) -> DormCheckoutStatusDTO:
./docs/contracts/contract-v0.1.md:412:        # 固定返回规则（覆盖所有状态）
./docs/contracts/contract-v0.1.md:416:                status=DormCheckoutStatus.COMPLETED,
./docs/contracts/contract-v0.1.md:423:                status=DormCheckoutStatus.PENDING,
./docs/contracts/contract-v0.1.md:430:                status=DormCheckoutStatus.NOT_STARTED,
./docs/contracts/contract-v0.1.md:437:                status=DormCheckoutStatus.UNKNOWN,
./docs/contracts/contract-v0.1.md:447:            status=DormCheckoutStatus.NOT_STARTED,
./docs/contracts/contract-v0.1.md:463:      "field": "leave_date",
./docs/contracts/contract-v0.1.md:525:      "dorm_status": "pending",
./docs/contracts/contract-v0.1.md:571:- 状态枚举（UserRole、ApplicationStatus、ApprovalStep、ApprovalDecision、DormCheckoutStatus）
./docs/contracts/contract-v0.1.md:573:- API端点（认证、申请、审批、查询）
./docs/contracts/contract-v0.1.md:582:- 审批转办、撤回、驳回重提
./docs/contracts/contract-v0.1.md:585:- 前端可用mock跑通登录→提交→审批→查询流程
./docs/contracts/contract-v0.1.md:635:        json={'reason': '毕业离校', 'leave_date': '2024-06-30'}
./docs/contracts/contract-v0.1.md:639:    # 3. 辅导员审批
./docs/contracts/contract-v0.1.md:640:    # 4. 学工部审批
./docs/contracts/contract-v0.1.md:641:    # 5. 查询状态
./docs/PROJECT-SUMMARY.md:1:# 毕业生离校申请审批系统 - 项目总结
./docs/PROJECT-SUMMARY.md:5:**项目名称：** 毕业生离校申请审批系统  
./docs/PROJECT-SUMMARY.md:6:**项目状态：** Week 0契约已冻结，准备启动Week 1 Day 1  
./docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
./docs/PROJECT-SUMMARY.md:42:- ✓ 完成审批流程设计（状态机、3个审批节点）
./docs/PROJECT-SUMMARY.md:66:- ✓ 审查第3、5、7、8、9、10章（API、审批、部署、安全、性能、测试）
./docs/PROJECT-SUMMARY.md:71:- ✓ 批次3：第5章审批流程（工作日计算、字段更新、历史审计）
./docs/PROJECT-SUMMARY.md:98:- ✓ P2修复：删除Postman引用、明确认证方式、统一审批时限、修改辅导员权限范围、统一性能指标
./docs/PROJECT-SUMMARY.md:154:- ✓ 修复OMC HUD状态栏显示问题
./docs/PROJECT-SUMMARY.md:211:- ✓ 创建contract-v0.1.md初稿（核心DTO、状态枚举、错误码、API端点、样例数据、Mock响应）
./docs/PROJECT-SUMMARY.md:215:  - 缺少状态机契约表
./docs/PROJECT-SUMMARY.md:220:- ✓ 修复全部6个问题（UserDTO可选字段、状态机表、Dorm Mock默认NOT_STARTED、扩展seed到10学生+密码、统一端点描述、优化降级条件）
./docs/PROJECT-SUMMARY.md:233:  - P1-2：降级方案逻辑矛盾（风险2说"砍学工部审批"又说"Day 4补学工部审批"）
./docs/PROJECT-SUMMARY.md:238:  - P1-2修复：修复风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1
./docs/PROJECT-SUMMARY.md:265:  - Application模型（application_id、student、reason、leave_date、status、dorm_checkout_status）
./docs/PROJECT-SUMMARY.md:271:  - Approval模型（approval_id、application、step、approver、decision、comment、decided_at）
./docs/PROJECT-SUMMARY.md:274:  - POST /api/approvals/{id}/approve（通过审批）
./docs/PROJECT-SUMMARY.md:275:  - POST /api/approvals/{id}/reject（驳回审批）
./docs/PROJECT-SUMMARY.md:277:  - 宿舍清退状态Mock服务
./docs/PROJECT-SUMMARY.md:278:  - 覆盖completed、pending、not_started、unknown四种状态
./docs/PROJECT-SUMMARY.md:279:- ✓ 状态机实现
./docs/PROJECT-SUMMARY.md:280:  - 提交申请→pending_counselor（创建辅导员审批记录）
./docs/PROJECT-SUMMARY.md:281:  - 辅导员通过→pending_dean（创建学工部审批记录）
./docs/PROJECT-SUMMARY.md:287:  - 辅导员只能审批辅导员步骤
./docs/PROJECT-SUMMARY.md:288:  - 学工部只能审批学工部步骤
./docs/PROJECT-SUMMARY.md:300:  - 完整流程：登录→提交→辅导员审批→学工部审批→查询
./docs/PROJECT-SUMMARY.md:301:  - 验证状态流转：pending_counselor→pending_dean→approved
./docs/PROJECT-SUMMARY.md:302:  - 验证审批记录创建和更新
./docs/PROJECT-SUMMARY.md:325:  - 自动分配对应辅导员到审批流程
./docs/PROJECT-SUMMARY.md:355:  2. Seed数据完整 - 支持两级审批
./docs/PROJECT-SUMMARY.md:356:  3. 学生登录并提交申请 - status=pending_counselor
./docs/PROJECT-SUMMARY.md:357:  4. 辅导员审批成功 - status→pending_dean
./docs/PROJECT-SUMMARY.md:358:  5. 学工部审批成功 - status→approved
./docs/PROJECT-SUMMARY.md:359:  6. 学生查询最终状态 - 完整审批链路
./docs/PROJECT-SUMMARY.md:361:  8. 宿舍清退Mock - dorm_checkout_status=completed
./docs/PROJECT-SUMMARY.md:372:  - P1-1：跨辅导员审批漏洞（任何辅导员都能审批任意approval）
./docs/PROJECT-SUMMARY.md:373:  - P1-2：重复审批漏洞（缺少事务保护和状态机验证）
./docs/PROJECT-SUMMARY.md:375:  - P1-4：Seed/mock数据错误（2020002班级不匹配，宿舍清退状态错误）
./docs/PROJECT-SUMMARY.md:378:  - P1-7：缺少列表接口（审批人无法发现待审批申请）
./docs/PROJECT-SUMMARY.md:406:  3. 核心一致性修复（2小时）：权限、状态机、重复提交约束
./docs/PROJECT-SUMMARY.md:426:  - 添加状态/步骤验证（防止状态机不一致）
./docs/PROJECT-SUMMARY.md:427:  - 添加重复dean审批检查（防止重复创建）
./docs/PROJECT-SUMMARY.md:431:  - 创建test_state_machine.py（重复审批返回409）
./docs/PROJECT-SUMMARY.md:432:  - 创建test_permissions.py（跨辅导员审批/驳回返回403）
./docs/PROJECT-SUMMARY.md:436:  - 核心代码已落地：约束、事务、权限、状态验证
./docs/PROJECT-SUMMARY.md:442:  - Scenario 3: 重复审批防护（200→409）✓
./docs/PROJECT-SUMMARY.md:452:  - Gap 2: status过滤功能未实现（Phase 1共识要求）
./docs/PROJECT-SUMMARY.md:453:  - Gap 3: smoke test负向测试逻辑错误（测试T002审批自己的approval而非T001的）
./docs/PROJECT-SUMMARY.md:456:  - 添加Dean detail endpoint权限检查（只能查看有pending dean approval的申请）
./docs/PROJECT-SUMMARY.md:457:  - 实现GET /api/applications/?status=过滤功能
./docs/PROJECT-SUMMARY.md:458:  - 修复smoke test使用正确的approval ID（$COUNSELOR_APPROVAL_ID而非$TEST_COUNSELOR_APPROVAL）
./docs/PROJECT-SUMMARY.md:460:  - Happy path: 学生→辅导员→学工部审批流程 ✓
./docs/PROJECT-SUMMARY.md:461:  - Negative test: 跨辅导员审批阻断（403）✓
./docs/PROJECT-SUMMARY.md:467:- ✓ 权限校验：辅导员只能审批分配班级、只能查看分配班级申请
./docs/PROJECT-SUMMARY.md:468:- ✓ 状态机验证：approval.step必须匹配application.status
./docs/PROJECT-SUMMARY.md:469:- ✓ 重复操作防护：重复审批返回409、重复提交返回409
./docs/PROJECT-SUMMARY.md:520:- 申请状态跟踪
./docs/PROJECT-SUMMARY.md:523:### 3. 审批流程
./docs/PROJECT-SUMMARY.md:524:- 两级审批（辅导员→学工部）
./docs/PROJECT-SUMMARY.md:525:- 审批意见记录
./docs/PROJECT-SUMMARY.md:537:- 审批状态变更通知
./docs/PROJECT-SUMMARY.md:552:3. **approvals** - 审批记录表
./docs/PROJECT-SUMMARY.md:582:- 状态机
./docs/PROJECT-SUMMARY.md:586:### 阶段4：审批管理模块（第4周）
./docs/PROJECT-SUMMARY.md:587:- 审批记录模型
./docs/PROJECT-SUMMARY.md:588:- 审批API
./docs/PROJECT-SUMMARY.md:589:- 审批流程逻辑
./docs/PROJECT-SUMMARY.md:671:- ✓ GET /api/approvals/支持decision过滤（pending/approved/rejected/all）
./docs/PROJECT-SUMMARY.md:683:- ✓ 测试覆盖：resubmission + approval filter
./docs/PROJECT-SUMMARY.md:694:- backend/apps/approvals/views.py（decision过滤）
./docs/PROJECT-SUMMARY.md:717:- ✓ 审批列表页面
./docs/PROJECT-SUMMARY.md:718:  - pages/approvals/approvals.wxml（列表UI）
./docs/PROJECT-SUMMARY.md:719:  - pages/approvals/approvals.wxss（样式）
./docs/PROJECT-SUMMARY.md:720:  - pages/approvals/approvals.ts（列表加载、导航）
./docs/PROJECT-SUMMARY.md:724:  - pages/detail/detail.ts（详情加载、审批操作）
./docs/PROJECT-SUMMARY.md:731:- miniprogram/pages/approvals/*（wxml, wxss, ts）
./docs/PROJECT-SUMMARY.md:743:  - 完整审批流程验证（student→counselor→dean）
./docs/PROJECT-SUMMARY.md:761:- Week 3核心流程补强（提交、审批列表/详情、审批/驳回、状态机、权限负向验证）
./docs/PROJECT-SUMMARY.md:762:- v0.2契约收敛（请求/响应样例、状态枚举、错误码、mock provider边界）
./docs/PROJECT-SUMMARY.md:766:- ✓ Codex接受Claude Option B混合方案：负向权限测试列为P0，状态机抽取轻量validator，v0.2契约保持精简
./docs/PROJECT-SUMMARY.md:767:- ✓ 新增审批负向权限覆盖：学生不可审批/驳回、角色步骤不匹配禁止、同角色非指定审批人禁止
./docs/PROJECT-SUMMARY.md:768:- ✓ 抽取审批步骤与申请状态匹配校验：approve/reject共用validator
./docs/PROJECT-SUMMARY.md:769:- ✓ 新增状态机覆盖：重复驳回冲突、counselor/dean步骤状态不匹配返回409
./docs/PROJECT-SUMMARY.md:770:- ✓ v0.2契约创建：明确`count/results`分页、权限矩阵、状态机、核心DTO和错误码
./docs/PROJECT-SUMMARY.md:774:- `docker compose exec backend python manage.py test apps.approvals.tests.test_permissions apps.approvals.tests.test_state_machine --keepdb`：10 tests OK
./docs/PROJECT-SUMMARY.md:775:- `docker compose exec backend python manage.py test [explicit approvals/applications test modules] --keepdb`：37 tests OK
./docs/PROJECT-SUMMARY.md:780:- `backend/apps/approvals/validators.py`
./docs/PROJECT-SUMMARY.md:790:- ✓ 文档化状态枚举（4个枚举类型）
./docs/PROJECT-SUMMARY.md:791:- ✓ 文档化状态机转换（6个有效转换）
./docs/PROJECT-SUMMARY.md:794:**Phase 1 - 安全+状态机（15分钟）：**
./docs/PROJECT-SUMMARY.md:796:  - test_permissions.py：5个安全测试（学生/角色/审批人权限）
./docs/PROJECT-SUMMARY.md:797:  - test_state_machine.py：4个状态机测试（重复操作/状态匹配）
./docs/PROJECT-SUMMARY.md:803:  - 4个状态枚举定义
./docs/PROJECT-SUMMARY.md:804:  - 状态机转换图+规则
./docs/PROJECT-SUMMARY.md:855:- 4页面：login, student-application, approvals（共享）, detail（共享）
./docs/PROJECT-SUMMARY.md:856:- 核心功能：登录、学生提交、列表、详情、辅导员/学工部审批
./docs/PROJECT-SUMMARY.md:857:- 必要状态：loading, empty, validation error, auth error, conflict error
./docs/PROJECT-SUMMARY.md:898:**状态：**
./docs/PROJECT-SUMMARY.md:909:- ✓ 学生重定向bug（学生禁止访问审批列表）
./docs/PROJECT-SUMMARY.md:918:- ✓ Step 1: 验证当前状态（运行时支持）- 所有4个问题已验证
./docs/PROJECT-SUMMARY.md:929:**状态：**
./docs/PROJECT-SUMMARY.md:950:**状态：**
./docs/PROJECT-SUMMARY.md:982:  - miniprogram/pages/login/login.ts（student→student-application, counselor/dean→approvals, 未知角色清理会话）
./docs/PROJECT-SUMMARY.md:986:  - backend/apps/applications/serializers.py（reason max_length=500 + trim, leave_date≥today）
./docs/PROJECT-SUMMARY.md:992:- 表单验证：reason trim非空且≤500字，leave_date必填且≥今天
./docs/PROJECT-SUMMARY.md:1002:**状态：**
./docs/PROJECT-SUMMARY.md:1011:- P1-2: 角色保护重复代码（student-application.ts和approvals.ts）
./docs/PROJECT-SUMMARY.md:1012:- P1-3: 时区不一致（前端UTC vs 后端Asia/Shanghai）
./docs/PROJECT-SUMMARY.md:1013:- P2-4: 审批列表UI显示审批人而非申请ID
./docs/PROJECT-SUMMARY.md:1023:- ✓ 3个修正建议：后端测试用timezone.now() + timedelta，前端创建date.ts工具，smoke测试用$(date -d "+1 day")
./docs/PROJECT-SUMMARY.md:1030:  - backend/apps/approvals/tests/test_rejection_flow.py
./docs/PROJECT-SUMMARY.md:1035:  - miniprogram/utils/date.ts（Asia/Shanghai时区helper）
./docs/PROJECT-SUMMARY.md:1038:  - miniprogram/pages/approvals/approvals.ts（使用role-guard）
./docs/PROJECT-SUMMARY.md:1039:  - miniprogram/pages/approvals/approvals.wxml（显示申请ID而非审批人）
./docs/PROJECT-SUMMARY.md:1051:**状态：**
./docs/superpowers/plans/2026-05-27-implementation-plan.md:1:# 毕业生离校申请审批系统 - 实施计划
./docs/superpowers/plans/2026-05-27-implementation-plan.md:12:实现一个完整的毕业生离校申请审批系统，支持：
./docs/superpowers/plans/2026-05-27-implementation-plan.md:14:- 辅导员和学工部两级审批
./docs/superpowers/plans/2026-05-27-implementation-plan.md:27:- 审批流程引擎
./docs/superpowers/plans/2026-05-27-implementation-plan.md:64:- ✓ 审批流程完整可用
./docs/superpowers/plans/2026-05-27-implementation-plan.md:89:graduation-leave-system/
./docs/superpowers/plans/2026-05-27-implementation-plan.md:111:│   │   │   ├── states.py
./docs/superpowers/plans/2026-05-27-implementation-plan.md:113:│   │   ├── approvals/          # 审批管理模块
./docs/superpowers/plans/2026-05-27-implementation-plan.md:272:   - 添加字段：application_no、status、planned_leave_date等
./docs/superpowers/plans/2026-05-27-implementation-plan.md:276:2. **实现状态机**
./docs/superpowers/plans/2026-05-27-implementation-plan.md:278:   - 定义状态转换规则
./docs/superpowers/plans/2026-05-27-implementation-plan.md:279:   - 实现状态转换方法
./docs/superpowers/plans/2026-05-27-implementation-plan.md:280:   - 编写状态机测试
./docs/superpowers/plans/2026-05-27-implementation-plan.md:292:   - 实现状态变更
./docs/superpowers/plans/2026-05-27-implementation-plan.md:296:   - 按状态过滤
./docs/superpowers/plans/2026-05-27-implementation-plan.md:304:- ✓ 提交申请后状态变更为pending_counselor
./docs/superpowers/plans/2026-05-27-implementation-plan.md:310:### 阶段4：审批管理模块（第4周）
./docs/superpowers/plans/2026-05-27-implementation-plan.md:312:**目标：** 实现审批流程和审批记录管理
./docs/superpowers/plans/2026-05-27-implementation-plan.md:316:1. **创建审批记录模型**
./docs/superpowers/plans/2026-05-27-implementation-plan.md:322:2. **实现审批API**
./docs/superpowers/plans/2026-05-27-implementation-plan.md:323:   - 获取待审批列表API
./docs/superpowers/plans/2026-05-27-implementation-plan.md:324:   - 审批通过API
./docs/superpowers/plans/2026-05-27-implementation-plan.md:325:   - 审批驳回API
./docs/superpowers/plans/2026-05-27-implementation-plan.md:326:   - 获取审批历史API
./docs/superpowers/plans/2026-05-27-implementation-plan.md:328:3. **实现审批流程逻辑**
./docs/superpowers/plans/2026-05-27-implementation-plan.md:329:   - 辅导员审批逻辑
./docs/superpowers/plans/2026-05-27-implementation-plan.md:330:   - 学工部审批逻辑
./docs/superpowers/plans/2026-05-27-implementation-plan.md:331:   - 审批记录创建
./docs/superpowers/plans/2026-05-27-implementation-plan.md:332:   - 状态变更触发
./docs/superpowers/plans/2026-05-27-implementation-plan.md:336:   - 检查超时审批
./docs/superpowers/plans/2026-05-27-implementation-plan.md:338:   - 标记超时状态
./docs/superpowers/plans/2026-05-27-implementation-plan.md:340:5. **实现审批权限控制**
./docs/superpowers/plans/2026-05-27-implementation-plan.md:341:   - 辅导员只能审批本年级
./docs/superpowers/plans/2026-05-27-implementation-plan.md:342:   - 学工部可以审批所有
./docs/superpowers/plans/2026-05-27-implementation-plan.md:346:- ✓ 辅导员审批通过后状态变更为pending_admin
./docs/superpowers/plans/2026-05-27-implementation-plan.md:347:- ✓ 学工部审批通过后状态变更为approved
./docs/superpowers/plans/2026-05-27-implementation-plan.md:348:- ✓ 驳回后状态变更为rejected
./docs/superpowers/plans/2026-05-27-implementation-plan.md:380:   - 权限验证（只能下载自己的或审批人的）
./docs/superpowers/plans/2026-05-27-implementation-plan.md:427:5. **集成通知到审批流程**
./docs/superpowers/plans/2026-05-27-implementation-plan.md:429:   - 审批通过时通知学生和下一审批人
./docs/superpowers/plans/2026-05-27-implementation-plan.md:430:   - 审批驳回时通知学生
./docs/superpowers/plans/2026-05-27-implementation-plan.md:431:   - 超时时通知审批人
./docs/superpowers/plans/2026-05-27-implementation-plan.md:437:- ✓ 审批流程触发通知
./docs/superpowers/plans/2026-05-27-implementation-plan.md:472:5. **集成到审批流程**
./docs/superpowers/plans/2026-05-27-implementation-plan.md:481:- ✓ 集成到审批流程
./docs/superpowers/plans/2026-05-27-implementation-plan.md:497:   - 配置状态管理（Redux/Context）
./docs/superpowers/plans/2026-05-27-implementation-plan.md:512:4. **实现审批页面**
./docs/superpowers/plans/2026-05-27-implementation-plan.md:513:   - 待审批列表页面
./docs/superpowers/plans/2026-05-27-implementation-plan.md:514:   - 审批详情页面
./docs/superpowers/plans/2026-05-27-implementation-plan.md:515:   - 审批操作页面
./docs/superpowers/plans/2026-05-27-implementation-plan.md:547:4. **实现审批页面**
./docs/superpowers/plans/2026-05-27-implementation-plan.md:548:   - 待审批列表页面
./docs/superpowers/plans/2026-05-27-implementation-plan.md:549:   - 审批操作页面
./docs/superpowers/plans/2026-05-27-implementation-plan.md:576:   - 编写完整审批流程测试
./miniprogram/pages/detail/detail.wxss:54:.status-pending_counselor, .status-pending_dean {
./miniprogram/pages/detail/detail.wxss:58:.status-approved {
./miniprogram/pages/detail/detail.wxss:62:.status-rejected {
./miniprogram/pages/detail/detail.wxss:66:.approval-item {
./miniprogram/pages/detail/detail.wxss:72:.approval-header {
./miniprogram/pages/detail/detail.wxss:105:.approval-body {
./backend/apps/approvals/migrations/0001_initial.py:19:                ('approval_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
./backend/apps/approvals/migrations/0001_initial.py:22:                ('decision', models.CharField(choices=[('pending', '待审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='pending', max_length=20)),
./backend/apps/approvals/migrations/0001_initial.py:27:                ('application', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='approvals', to='applications.application')),
./backend/apps/approvals/migrations/0001_initial.py:30:                'db_table': 'approvals',
./docs/plans/week-0-1-execution-plan.md:19:- [x] 定义状态枚举（5个枚举类型）
./docs/plans/week-0-1-execution-plan.md:33:  - POST /api/approvals/{id}/approve
./docs/plans/week-0-1-execution-plan.md:34:  - POST /api/approvals/{id}/reject
./docs/plans/week-0-1-execution-plan.md:45:- [ ] 前端可用mock跑通登录→提交→审批→查询流程
./docs/plans/week-0-1-execution-plan.md:56:交付可运行的后端最小闭环：薄认证 + 申请提交 + 两级审批 + 状态查询 + Dorm Mock。
./docs/plans/week-0-1-execution-plan.md:86:  - Dorm Mock集成：检查宿舍清退状态
./docs/plans/week-0-1-execution-plan.md:87:  - 状态初始化：pending_counselor
./docs/plans/week-0-1-execution-plan.md:88:  - 创建辅导员审批记录
./docs/plans/week-0-1-execution-plan.md:89:- [ ] 辅导员审批API（POST /api/approvals/{id}/approve|reject）
./docs/plans/week-0-1-execution-plan.md:90:  - 最小角色校验：只有对应班级辅导员可审批
./docs/plans/week-0-1-execution-plan.md:91:  - 状态流转：pending_counselor → pending_dean（通过）或 rejected（驳回）
./docs/plans/week-0-1-execution-plan.md:92:  - 创建学工部审批记录（通过时）
./docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
./docs/plans/week-0-1-execution-plan.md:94:  - 最小角色校验：只有学工部可审批
./docs/plans/week-0-1-execution-plan.md:95:  - 状态流转：pending_dean → approved（通过）或 rejected（驳回）
./docs/plans/week-0-1-execution-plan.md:96:- [ ] 状态查询API（GET /api/applications/{id}）
./docs/plans/week-0-1-execution-plan.md:107:- [ ] 辅导员可审批（通过/驳回）
./docs/plans/week-0-1-execution-plan.md:108:- [ ] 学工部可审批（通过/驳回）
./docs/plans/week-0-1-execution-plan.md:109:- [ ] 状态查询返回完整申请信息和审批记录
./docs/plans/week-0-1-execution-plan.md:110:- [ ] 角色校验生效（学生不能审批，辅导员不能跨班级审批）
./docs/plans/week-0-1-execution-plan.md:113:- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批
./docs/plans/week-0-1-execution-plan.md:114:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
./docs/plans/week-0-1-execution-plan.md:120:  - 测试1：学生登录 → 提交申请 → 辅导员审批通过 → 学工部审批通过 → 查询状态
./docs/plans/week-0-1-execution-plan.md:121:  - 测试2：学生登录 → 提交申请 → 辅导员审批驳回 → 查询状态
./docs/plans/week-0-1-execution-plan.md:123:  - 测试4：角色校验（学生不能审批，辅导员不能跨班级审批）
./docs/plans/week-0-1-execution-plan.md:164:- [ ] 可用mock跑通登录→提交→审批→查询流程
./docs/plans/week-0-1-execution-plan.md:180:**降级方案：** 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
./docs/plans/week-0-1-execution-plan.md:182:### 风险3：Week 1 Day 4学工部审批未完成
./docs/plans/week-0-1-execution-plan.md:186:**降级方案：** 推到Week 2 Day 1，Week 1只验证辅导员审批
./docs/plans/week-0-1-execution-plan.md:208:- [ ] 4个API端点可用（登录、提交、审批、查询）
./docs/plans/week-0-1-execution-plan.md:232:**状态：** 已批准，可执行
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:37:1. `GET /api/approvals/` (PRIORITY 1)
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:45:   - Dean: applications with own pending approvals (NOT all applications)
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:49:- Support `?status=` parameter
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:50:- **[Codex constraint]** Define `?status=pending` to map to both `pending_counselor` AND `pending_dean`
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:61:- Do NOT use full ApplicationSerializer with nested approvals
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:62:- Avoid expanding approval records exposure surface
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:78:2. Counselor cannot list other counselors' approvals
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:80:4. Dean cannot list other deans' approvals
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:82:6. **[Codex constraint]** Verify approvals list filters by decision=pending by default
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:92:- Counselor discovers approval via `GET /api/approvals/` (not from creation response)
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:94:- Dean discovers approval via `GET /api/approvals/` (not from creation response)
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:96:- Student verifies final status
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:106:- session-context.json: Update with Day 3 status
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:141:**Issue:** `Application.status` values are `pending_counselor`/`pending_dean`/`approved`/`rejected`, not single `pending`.
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:144:- Option A: Map `?status=pending` to both `pending_counselor` AND `pending_dean`
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:153:**Issue 1:** `GET /api/approvals/` should filter by `approver=user` AND `decision=pending` by default.
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:158:- Add `decision=pending` filter to approvals list
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:165:**Issue:** Current `ApplicationSerializer` includes nested approvals, expanding exposure surface.
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:167:**Action:** Create separate list serializer without nested approvals for `GET /api/applications/`.
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:198:6. **[Codex addition]** Default filter approvals by `decision=pending`
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:152:- 核心模块优先（认证、申请、审批）
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:239:**第5章 审批流程：**
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:4:**状态:** ✓ 共识达成  
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:19:### 1. GET /api/approvals/ 权限
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:27:- ✓ 学工部: 通过自己pending dean approvals反查
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:31:- ✓ 支持?status=过滤
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:35:- ✓ 使用lean ApplicationListSerializer（不含approvals）
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:73:### Step 2: 实现GET /api/approvals/ (45min)
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:76:- 排序: created_at DESC, approval_id DESC
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:82:- Dean权限: 通过pending approvals反查
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:83:- 支持?status=过滤
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:88:- 学生访问approvals返回403
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:89:- T002看不到T001的approvals
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:91:- 已审批记录不出现在approvals list
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:112:**共识状态:** 已达成  
./docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:131:`'status': 'password_setup_required'` 在密码设置前返回token。
./docs/数据对接说明文档.md:1:# 毕业生离校申请审批系统 - 数据对接说明文档
./docs/数据对接说明文档.md:16:2. **辅导员基本信息** - 创建辅导员账号，用于审批管理
./docs/数据对接说明文档.md:17:3. **班级-辅导员对应关系** - 自动分配审批人
./docs/数据对接说明文档.md:29:| 宿舍清退数据 | **API接口实时查询** | 需要实时验证清退状态 |
./docs/数据对接说明文档.md:55:- 自动分配审批人（根据班级匹配辅导员）
./docs/数据对接说明文档.md:135:- 所有学生账号标记为"待设置密码"状态
./docs/数据对接说明文档.md:141:- 本次未导入的学号：自动标记为"停用"状态
./docs/数据对接说明文档.md:156:- 审批权限管理
./docs/数据对接说明文档.md:172:- `is_active=false` 时不能登录、不能审批，但历史记录可查询
./docs/数据对接说明文档.md:195:学生提交申请时，系统根据学生的 `class_id` 自动查询对应的辅导员，分配审批人。
./docs/数据对接说明文档.md:243:- 无审批人的学生数：有多少学生没有对应的辅导员
./docs/数据对接说明文档.md:251:学生提交离校申请时，系统实时查询宿舍清退状态：
./docs/数据对接说明文档.md:258:**接口名称：** 查询学生宿舍清退状态
./docs/数据对接说明文档.md:262:**请求地址：** `http://宿舍管理系统域名/api/dorm/checkout/status`
./docs/数据对接说明文档.md:275:GET /api/dorm/checkout/status?student_id=2022001&name=张三
./docs/数据对接说明文档.md:291:    "checkout_status": "completed",
./docs/数据对接说明文档.md:302:| checkout_status | String | 是 | 清退状态 | "completed" |
./docs/数据对接说明文档.md:303:| checkout_date | String | 条件必填 | 清退完成时间（status=completed时必填） | "2026-05-20T14:30:00" |
./docs/数据对接说明文档.md:306:**清退状态枚举值：**
./docs/数据对接说明文档.md:353:- API查询失败时，返回 `checkout_status: "unknown"`
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:13:2. `GET /api/approvals/` - 审批列表
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:45:      "leave_date": "2024-06-30",
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:46:      "status": "pending_counselor",
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:59:### 2.2 GET /api/approvals/
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:61:**URL:** `/api/approvals/`  
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:66:- 学生: 返回自己申请的所有审批记录
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:67:- 辅导员: 返回待自己审批的记录（step='counselor', decision='pending'）
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:68:- 学工部: 返回待自己审批的记录（step='dean', decision='pending'）
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:73:  "approvals": [
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:75:      "approval_id": "apv_xxx",
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:90:- 文件: `apps/approvals/views.py`
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:91:- 函数: `list_approvals` (新增)
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:92:- URL: 在 `apps/approvals/urls.py` 中添加
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:104:### Step 2: 实现 list_approvals 视图
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:106:1. 在 `apps/approvals/views.py` 添加 `list_approvals` 函数
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:113:2. 创建 `apps/approvals/tests/test_list_approvals.py`
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:157:   - 例如: applications列表是否应该包含approvals数组?
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:171:   - 是否应该只返回待审批的? 还是所有状态的?
./docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:21:**状态：** ✅ 同意
./docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:40:**状态：** ✅ 同意
./docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:55:**状态：** ✅ 同意
./docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:96:    cutoff_date = timezone.now() - timedelta(days=settings.AUDIT_LOG_RETENTION_DAYS)
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:73:1. **实施周期：** CSV/Excel导入最快，DB直连需要安全审批和网络配置
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:88:- 宿舍清退数据保持API优先，因为需要实时校验学生提交时的清退状态
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:95:**Codex意见：** `checkout_status` 在本文档中标为可选，但既有字段共识中API响应建议必填。
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:101:1. **业务必要性：** 清退状态是提交前置校验的核心字段，必须明确
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:109:| `checkout_status` | 可选 | **必填**，枚举：`completed`/`pending`/`not_started`/`unknown` |
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:110:| `checkout_date` | 可选 | **条件必填**：当 `checkout_status = completed` 时必填 |
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:123:**Codex意见：** 缺少终审管理员分配规则、账号标识映射、历史审批人一致性规则、多辅导员场景处理。
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:180:#### 4.3 历史审批人一致性规则
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:187:这是一个重要的业务规则。如果班级映射变更后自动改写已提交申请的审批人，会导致：
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:188:1. 审批流程混乱（原审批人已审批，新审批人不知情）
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:189:2. 审计追溯困难（无法还原当时的审批人是谁）
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:190:3. 权限边界模糊（新审批人可能不应该看到旧申请）
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:193:1. 已提交的申请保持原审批人不变
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:200:1. **审批流程完整性：** 已提交申请的审批人是提交时确定的，不应因后续映射变更而改变
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:201:2. **审计追溯：** 保持历史审批人记录，便于追溯当时的审批责任
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:202:3. **权限边界：** 新辅导员不应自动获得旧申请的审批权限
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:209:| 映射变更后，已提交申请 | `counselor_id` **不变**，保持原审批人 |
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:211:| 需要改派审批人 | 管理员显式操作，记录审计日志（操作人、时间、原因） |
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:215:- 审计日志表记录审批人变更操作
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:228:2. 审批流程需要确定主审批人
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:229:3. 权限边界需要明确（所有辅导员都能审批？还是只有主辅导员？）
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:254:4. 所有辅导员都能查看本班申请，但只有主辅导员能审批
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:269:- 图书馆清书、财务结清、学籍状态不列为P0是合理的
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:276:1. `is_graduating` 建议改名或补充为 `eligible_for_leave`
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:290:- 延期毕业、结业等异常状态可以通过 `is_graduating=false` 排除
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:291:- 如果后续需要更细粒度的状态，再扩展为 `graduation_status` 枚举
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:383:6. 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:456:2. `checkout_status` 改为必填，增加枚举值
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:459:5. 明确历史审批人一致性规则（不自动改写）
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:486:- `checkout_status` 改为必填，增加枚举值说明
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:517:- 新增"历史审批人一致性规则"章节
./backend/apps/approvals/tests/test_rejection_flow.py:3:from rest_framework import status
./backend/apps/approvals/tests/test_rejection_flow.py:4:from django.utils import timezone
./backend/apps/approvals/tests/test_rejection_flow.py:9:from apps.approvals.models import ApprovalDecision
./backend/apps/approvals/tests/test_rejection_flow.py:60:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
./backend/apps/approvals/tests/test_rejection_flow.py:72:        counselor_approval = application.approvals.filter(step='counselor').first()
./backend/apps/approvals/tests/test_rejection_flow.py:75:        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/reject/', {
./backend/apps/approvals/tests/test_rejection_flow.py:78:        self.assertEqual(response.status_code, status.HTTP_200_OK)
./backend/apps/approvals/tests/test_rejection_flow.py:81:        # Verify application status
./backend/apps/approvals/tests/test_rejection_flow.py:83:        self.assertEqual(application.status, ApplicationStatus.REJECTED)
./backend/apps/approvals/tests/test_rejection_flow.py:97:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
./backend/apps/approvals/tests/test_rejection_flow.py:109:        counselor_approval = application.approvals.filter(step='counselor').first()
./backend/apps/approvals/tests/test_rejection_flow.py:112:        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/approve/', {
./backend/apps/approvals/tests/test_rejection_flow.py:115:        self.assertEqual(response.status_code, status.HTTP_200_OK)
./backend/apps/approvals/tests/test_rejection_flow.py:125:        dean_approval = application.approvals.filter(step='dean').first()
./backend/apps/approvals/tests/test_rejection_flow.py:128:        response = self.client.post(f'/api/approvals/{dean_approval.approval_id}/reject/', {
./backend/apps/approvals/tests/test_rejection_flow.py:131:        self.assertEqual(response.status_code, status.HTTP_200_OK)
./backend/apps/approvals/tests/test_rejection_flow.py:134:        # Verify application status
./backend/apps/approvals/tests/test_rejection_flow.py:136:        self.assertEqual(application.status, ApplicationStatus.REJECTED)
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:30:- 申请/审批/附件/通知/集成模块
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:53:- 辅导员一级审批
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:90:- 审批流程设计
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:97:这份文档已经不仅是概要设计，而是包含了较多可指导实现的细节，例如 API 示例、状态机、索引策略、上传校验、限流策略、审计日志、超时计算、备份恢复和测试样例。
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:104:4. 审批流程具备状态机意识：草稿、待辅导员、待学工部、通过、驳回等状态明确。
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:119:   例如字段声明 `NOT NULL`，外键又写 `ON DELETE SET NULL`。这在数据库层面互相冲突。审批记录、审计日志这类历史数据建议优先使用软删除或 `PROTECT/RESTRICT`，避免历史记录失真。
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:131:   Access Token 设计为 7 天。对审批和个人信息系统而言，这个时长偏长。虽然尚未实现，但它属于已完成认证设计的一部分，建议在设计文档阶段调整。
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:144:4. 审批管理模块
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:187:**Round 2：API、审批、部署、安全、性能、测试**
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:191:- 补充审批工作日计算、字段更新、历史审计
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:230:目录结构与实施计划基本一致，能够承接 Django 后端、移动端、小程序、Docker 配置等后续工作。当前为空目录是正常状态，因为只完成了结构创建。
./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:330:- 审批状态机实现
./backend/apps/approvals/views.py:1:from rest_framework import status
./backend/apps/approvals/views.py:5:from django.utils import timezone
./backend/apps/approvals/views.py:10:from .validators import approval_step_matches_application_status
./backend/apps/approvals/views.py:18:def list_approvals(request):
./backend/apps/approvals/views.py:24:            {'error': {'code': 'FORBIDDEN', 'message': '学生不能访问审批列表'}},
./backend/apps/approvals/views.py:25:            status=status.HTTP_403_FORBIDDEN
./backend/apps/approvals/views.py:28:    # 辅导员: 只看自己的counselor审批
./backend/apps/approvals/views.py:35:    # 学工部: 只看自己的dean审批
./backend/apps/approvals/views.py:45:            status=status.HTTP_403_FORBIDDEN
./backend/apps/approvals/views.py:54:    queryset = queryset.order_by('-created_at', '-approval_id')
./backend/apps/approvals/views.py:69:def approve_approval(request, approval_id):
./backend/apps/approvals/views.py:71:        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
./backend/apps/approvals/views.py:73:        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
./backend/apps/approvals/views.py:74:                        status=status.HTTP_404_NOT_FOUND)
./backend/apps/approvals/views.py:77:    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
./backend/apps/approvals/views.py:79:                        status=status.HTTP_403_FORBIDDEN)
./backend/apps/approvals/views.py:80:    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
./backend/apps/approvals/views.py:82:                        status=status.HTTP_403_FORBIDDEN)
./backend/apps/approvals/views.py:84:    if approval.approver_id != user.user_id:
./backend/apps/approvals/views.py:86:                        status=status.HTTP_403_FORBIDDEN)
./backend/apps/approvals/views.py:88:    if approval.decision != ApprovalDecision.PENDING:
./backend/apps/approvals/views.py:89:        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
./backend/apps/approvals/views.py:90:                        status=status.HTTP_409_CONFLICT)
./backend/apps/approvals/views.py:92:    if not approval_step_matches_application_status(approval):
./backend/apps/approvals/views.py:93:        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
./backend/apps/approvals/views.py:94:                        status=status.HTTP_409_CONFLICT)
./backend/apps/approvals/views.py:99:                        status=status.HTTP_400_BAD_REQUEST)
./backend/apps/approvals/views.py:101:    approval.decision = ApprovalDecision.APPROVED
./backend/apps/approvals/views.py:102:    approval.comment = serializer.validated_data.get('comment', '')
./backend/apps/approvals/views.py:103:    approval.decided_at = timezone.now()
./backend/apps/approvals/views.py:104:    approval.save()
./backend/apps/approvals/views.py:106:    application = approval.application
./backend/apps/approvals/views.py:107:    if approval.step == ApprovalStep.COUNSELOR:
./backend/apps/approvals/views.py:108:        # Check for existing dean approval to prevent duplicates
./backend/apps/approvals/views.py:109:        existing_dean_approval = Approval.objects.filter(
./backend/apps/approvals/views.py:114:        if existing_dean_approval:
./backend/apps/approvals/views.py:115:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
./backend/apps/approvals/views.py:116:                            status=status.HTTP_409_CONFLICT)
./backend/apps/approvals/views.py:118:        application.status = ApplicationStatus.PENDING_DEAN
./backend/apps/approvals/views.py:121:            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
./backend/apps/approvals/views.py:128:    elif approval.step == ApprovalStep.DEAN:
./backend/apps/approvals/views.py:129:        application.status = ApplicationStatus.APPROVED
./backend/apps/approvals/views.py:132:    return Response(ApprovalSerializer(approval).data)
./backend/apps/approvals/views.py:138:def reject_approval(request, approval_id):
./backend/apps/approvals/views.py:140:        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
./backend/apps/approvals/views.py:142:        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
./backend/apps/approvals/views.py:143:                        status=status.HTTP_404_NOT_FOUND)
./backend/apps/approvals/views.py:146:    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
./backend/apps/approvals/views.py:148:                        status=status.HTTP_403_FORBIDDEN)
./backend/apps/approvals/views.py:149:    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
./backend/apps/approvals/views.py:151:                        status=status.HTTP_403_FORBIDDEN)
./backend/apps/approvals/views.py:153:    if approval.approver_id != user.user_id:
./backend/apps/approvals/views.py:155:                        status=status.HTTP_403_FORBIDDEN)
./backend/apps/approvals/views.py:157:    if approval.decision != ApprovalDecision.PENDING:
./backend/apps/approvals/views.py:158:        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
./backend/apps/approvals/views.py:159:                        status=status.HTTP_409_CONFLICT)
./backend/apps/approvals/views.py:161:    if not approval_step_matches_application_status(approval):
./backend/apps/approvals/views.py:162:        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
./backend/apps/approvals/views.py:163:                        status=status.HTTP_409_CONFLICT)
./backend/apps/approvals/views.py:168:                        status=status.HTTP_400_BAD_REQUEST)
./backend/apps/approvals/views.py:170:    approval.decision = ApprovalDecision.REJECTED
./backend/apps/approvals/views.py:171:    approval.comment = serializer.validated_data.get('comment', '')
./backend/apps/approvals/views.py:172:    approval.decided_at = timezone.now()
./backend/apps/approvals/views.py:173:    approval.save()
./backend/apps/approvals/views.py:175:    application = approval.application
./backend/apps/approvals/views.py:176:    application.status = ApplicationStatus.REJECTED
./backend/apps/approvals/views.py:179:    return Response(ApprovalSerializer(approval).data)
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:4:**状态:** 修订中  
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:25:**原提案:** 学生可以看自己的审批记录  
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:26:**Day 3共识:** 学生访问GET /api/approvals/应返回403  
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:31:**Day 3共识:** Dean只看自己pending审批对应的申请  
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:36:**Day 3共识:** 固定limit 20、支持?status=、返回count  
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:41:**Codex指出:** ApplicationSerializer嵌套approvals，不能复用  
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:53:### 3.1 GET /api/approvals/ (PRIORITY 1)
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:55:**URL:** `/api/approvals/`  
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:61:    return 403  # 学生不允许访问审批列表
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:82:      "approval_id": "apv_xxx",
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:92:**排序:** `created_at DESC, approval_id DESC`
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:119:    # Dean只看自己pending审批对应的申请
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:120:    pending_approval_app_ids = Approval.objects.filter(
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:126:        application_id__in=pending_approval_app_ids
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:131:- `?status=pending_counselor`
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:132:- `?status=pending_dean`
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:133:- `?status=approved`
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:134:- `?status=rejected`
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:136:**Serializer:** 新建`ApplicationListSerializer`（不包含approvals）
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:143:            'class_id', 'reason', 'leave_date', 'status',
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:159:      "leave_date": "2024-06-30",
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:160:      "status": "pending_counselor",
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:177:- 不包含approvals字段
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:180:### Step 2: 实现GET /api/approvals/ (45min)
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:181:- 文件: `apps/approvals/views.py`
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:182:- 函数: `list_approvals`
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:190:- Dean权限: 通过pending approvals反查
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:191:- 支持?status=过滤
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:195:- 学生访问approvals返回403
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:196:- T002看不到T001的approvals
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:198:- 已审批记录不出现在approvals list
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:211:1. **关联数据:** applications列表不包含approvals
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:215:5. **辅导员范围:** 所有负责班级的申请，可用?status=过滤
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:221:1. ✓ 学生访问GET /api/approvals/必须403
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:222:2. ✓ 辅导员/学工部只看自己pending审批
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:223:3. ✓ Dean通过pending approvals反查applications
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:226:6. ✓ 支持?status=过滤
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:238:- Dean只看自己pending审批对应的申请
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:239:- 学生访问approvals返回403
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:132:3. **关键模块强制TDD**：认证、审批、支付等
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:136:P0: 核心业务逻辑（认证、审批、状态机）
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:157:--cov=apps/approvals/permissions.py --cov-fail-under=90
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:203:Locust测试场景只有3个任务（查看列表、查看详情、审批），权重固定（3:2:1）。
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:227:        """辅导员查看待审批"""
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:228:        self.client.get("/api/v1/approvals/pending")
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:232:        """辅导员审批"""
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:233:        self.client.post("/api/v1/approvals/1/approve", json={...})
./backend/apps/approvals/tests/test_list_permissions.py:5:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
./backend/apps/approvals/tests/test_list_permissions.py:40:            leave_date='2024-07-01',
./backend/apps/approvals/tests/test_list_permissions.py:41:            status=ApplicationStatus.PENDING_COUNSELOR
./backend/apps/approvals/tests/test_list_permissions.py:44:        # Create approvals
./backend/apps/approvals/tests/test_list_permissions.py:45:        self.approval_c1 = Approval.objects.create(
./backend/apps/approvals/tests/test_list_permissions.py:46:            approval_id='apv_c1',
./backend/apps/approvals/tests/test_list_permissions.py:54:        self.approval_d1 = Approval.objects.create(
./backend/apps/approvals/tests/test_list_permissions.py:55:            approval_id='apv_d1',
./backend/apps/approvals/tests/test_list_permissions.py:63:    def test_student_403_on_approval_list(self):
./backend/apps/approvals/tests/test_list_permissions.py:65:        response = self.client.get('/api/approvals/')
./backend/apps/approvals/tests/test_list_permissions.py:66:        self.assertEqual(response.status_code, 403)
./backend/apps/approvals/tests/test_list_permissions.py:69:    def test_counselor_sees_only_own_pending_approvals(self):
./backend/apps/approvals/tests/test_list_permissions.py:71:        response = self.client.get('/api/approvals/')
./backend/apps/approvals/tests/test_list_permissions.py:72:        self.assertEqual(response.status_code, 200)
./backend/apps/approvals/tests/test_list_permissions.py:74:        self.assertEqual(response.data['results'][0]['approval_id'], 'apv_c1')
./backend/apps/approvals/tests/test_list_permissions.py:76:    def test_counselor_cannot_see_other_counselor_approvals(self):
./backend/apps/approvals/tests/test_list_permissions.py:78:        response = self.client.get('/api/approvals/')
./backend/apps/approvals/tests/test_list_permissions.py:81:    def test_dean_sees_only_own_pending_approvals(self):
./backend/apps/approvals/tests/test_list_permissions.py:83:        response = self.client.get('/api/approvals/')
./backend/apps/approvals/tests/test_list_permissions.py:84:        self.assertEqual(response.status_code, 200)
./backend/apps/approvals/tests/test_list_permissions.py:86:        self.assertEqual(response.data['results'][0]['approval_id'], 'apv_d1')
./backend/apps/approvals/tests/test_list_permissions.py:88:    def test_dean_cannot_see_other_dean_approvals(self):
./backend/apps/approvals/tests/test_list_permissions.py:90:        response = self.client.get('/api/approvals/')
./backend/apps/approvals/tests/test_list_permissions.py:95:        response = self.client.get('/api/approvals/')
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:11:Day 3 proposal direction is correct (list endpoints are the right priority), but scope and prerequisites are wrong. Day 2 evidence has drifted from actual code state, and Day 3 scope is too ambitious.
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:55:- Filtering (status, date range)
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:69:- `GET /api/approvals/`: "Dean: own pending approvals only"
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:71:**Evidence:** These are contradictory. "All applications" is admin view, not approval workflow.
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:108:- Only support `?status=` filtering (whitelist)
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:132:1. `GET /api/approvals/` (priority 1)
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:134:   - Counselor: own pending approvals only
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:135:   - Dean: own pending approvals only
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:139:   - Dean: applications with own pending approvals (not all)
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:144:3. T002 cannot see T001 approvals
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:145:4. Dean only sees own pending approvals
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:148:- Update smoke test to discover approvals via `/api/approvals/`
./backend/apps/approvals/serializers.py:6:    """Lean serializer for approval lists - includes created_at"""
./backend/apps/approvals/serializers.py:12:        fields = ['approval_id', 'application_id', 'step', 'approver_id',
./backend/apps/approvals/serializers.py:14:        read_only_fields = ['approval_id', 'application_id', 'step',
./backend/apps/approvals/serializers.py:24:        fields = ['approval_id', 'application_id', 'step', 'approver_id',
./backend/apps/approvals/serializers.py:26:        read_only_fields = ['approval_id', 'application_id', 'step',
./backend/apps/approvals/tests/test_permissions.py:3:from rest_framework import status
./backend/apps/approvals/tests/test_permissions.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
./backend/apps/approvals/tests/test_permissions.py:76:            leave_date='2024-06-30',
./backend/apps/approvals/tests/test_permissions.py:77:            status=ApplicationStatus.PENDING_COUNSELOR
./backend/apps/approvals/tests/test_permissions.py:80:        # Create counselor approval for application1
./backend/apps/approvals/tests/test_permissions.py:81:        self.approval1 = Approval.objects.create(
./backend/apps/approvals/tests/test_permissions.py:82:            approval_id='apv_test001',
./backend/apps/approvals/tests/test_permissions.py:92:    def _create_dean_approval(self):
./backend/apps/approvals/tests/test_permissions.py:93:        self.application1.status = ApplicationStatus.PENDING_DEAN
./backend/apps/approvals/tests/test_permissions.py:96:            approval_id='apv_test002',
./backend/apps/approvals/tests/test_permissions.py:105:        """学生不能调用审批操作接口"""
./backend/apps/approvals/tests/test_permissions.py:109:            f'/api/approvals/{self.approval1.approval_id}/approve/',
./backend/apps/approvals/tests/test_permissions.py:114:            f'/api/approvals/{self.approval1.approval_id}/reject/',
./backend/apps/approvals/tests/test_permissions.py:119:        self.assertEqual(approve_response.status_code, status.HTTP_403_FORBIDDEN)
./backend/apps/approvals/tests/test_permissions.py:120:        self.assertEqual(reject_response.status_code, status.HTTP_403_FORBIDDEN)
./backend/apps/approvals/tests/test_permissions.py:123:        """学工部不能处理辅导员审批步骤"""
./backend/apps/approvals/tests/test_permissions.py:127:            f'/api/approvals/{self.approval1.approval_id}/approve/',
./backend/apps/approvals/tests/test_permissions.py:132:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
./backend/apps/approvals/tests/test_permissions.py:135:        """辅导员不能处理学工部审批步骤"""
./backend/apps/approvals/tests/test_permissions.py:136:        dean_approval = self._create_dean_approval()
./backend/apps/approvals/tests/test_permissions.py:140:            f'/api/approvals/{dean_approval.approval_id}/approve/',
./backend/apps/approvals/tests/test_permissions.py:145:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
./backend/apps/approvals/tests/test_permissions.py:148:        """同角色但非指定学工部审批人不能处理审批"""
./backend/apps/approvals/tests/test_permissions.py:149:        dean_approval = self._create_dean_approval()
./backend/apps/approvals/tests/test_permissions.py:153:            f'/api/approvals/{dean_approval.approval_id}/reject/',
./backend/apps/approvals/tests/test_permissions.py:158:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
./backend/apps/approvals/tests/test_permissions.py:161:        """测试跨辅导员审批返回403"""
./backend/apps/approvals/tests/test_permissions.py:165:            f'/api/approvals/{self.approval1.approval_id}/approve/',
./backend/apps/approvals/tests/test_permissions.py:169:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
./backend/apps/approvals/tests/test_permissions.py:176:            f'/api/approvals/{self.approval1.approval_id}/reject/',
./backend/apps/approvals/tests/test_permissions.py:180:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
./backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:112:docker exec backend python manage.py test apps.applications.tests.test_application_flow apps.applications.tests.test_error_cases apps.approvals.tests.test_rejection_flow --keepdb
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:10:`29-data-source-analysis.md` 的方向是正确的：当前数据对接文档只覆盖宿舍清退，无法完整支撑 student、counselor、admin 三类角色的账号初始化、权限边界和自动审批分配。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:14:1. **班级-辅导员对应关系应明确列为 P0。** 这是自动分配审批人的核心数据。没有它，系统提交申请时无法稳定设置 `counselor_id` 和 `current_approver_id`，只能退化为人工逐个配置或人工改派。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:26:| 辅导员基本信息 | 人事系统或人工台账 | P0 | 用于创建 counselor 账号和审批权限主体。实时同步不是 P0，但账号数据本身是 P0。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:29:| 毕业资格/离校资格字段 | 教务系统 | P0 字段，非 P0 独立接口 | 如果系统只导入当届毕业生，可通过导入范围满足；如果导入全量学生，则必须在学生基本信息中带 `graduation_year`、`graduation_status` 或 `eligible_for_leave`。不建议首版单独建设学籍 API。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:36:| 图书馆清书状态 | 图书馆系统 | P1 | 当前已有上传截图的人工方案。接口集成能降低审核成本和伪造风险，但不应阻塞首版上线。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:37:| 财务结清状态 | 财务系统 | P1 | 当前已有上传截图的人工方案。由于财务状态更敏感，若后续接口条件成熟，优先级可高于图书馆，但仍不是首版 P0。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:38:| 独立学籍状态接口 | 教务系统 | P1 | 只有在多届学生并行、延期毕业、结业/退学实时变化等需求明确时，才需要独立 API。首版可并入学生基础数据。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:46:| 学生基本信息 | CSV/Excel 批量导入 | 教务系统 API | 首版按毕业届别导入更容易落地。字段建议包括 `student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:48:| 班级-辅导员对应关系 | CSV/Excel 批量导入并强校验 | 教务系统 API | 必须优先支持。建议用 `class_id + counselor_employee_id + effective_term` 表达关系，不要只靠 `class_name`。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无审批人的学生数。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:51:| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 后续对接时只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，不要引入借阅明细。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:52:| 财务结清状态 | 首版手动上传截图 | API 优先于 CSV | 后续对接时只返回是否结清和结清日期，不同步欠费明细；外部系统失败时保留人工审核通道。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:53:| 学籍/毕业资格 | 并入学生基本信息导入 | 教务系统 API | 首版不要单独拆接口。若后续存在延期毕业、结业、退学状态的实时变更，再建设独立同步。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:77:- 学生提交时能否自动设置辅导员审批人；
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:78:- 辅导员是否只能查看和审批负责班级；
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:80:- 审批统计能否按院系、班级、辅导员追踪。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:82:建议数据对接文档单独增加“审批关系数据”章节，并把导入覆盖率 100% 作为上线验收条件之一。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:92:图书馆和财务可保持 P1。首版延续截图上传和人工审核，后续按审核量、造假风险、外部系统接口成熟度决定是否对接。若只能先选一个，建议先评估财务结清状态，因为财务数据的业务风险通常高于图书馆清书。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:94:学籍状态不建议作为首版独立接口，但毕业资格字段必须进入学生基础数据。换句话说，“是否允许提交离校申请”必须有数据依据，只是不一定需要实时 API。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:108:5. **审批人变更后的历史一致性。** 已提交申请中的 `counselor_id` 应保持历史一致，不应因后续班级映射变更自动改写。若需改派，应由管理员显式操作并记录审计日志。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:110:6. **多辅导员和代理审批。** 现实中可能有主辅导员、代管辅导员、临时代理。首版可只要求一个主审批人，但后台应预留人工改派能力。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:126:1. **重构数据对接说明文档目录。** 从单一“宿舍对接”扩展为“账号基础数据、审批关系数据、业务校验数据、降级与审计”四类。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:151:2. 新增“辅导员基本信息导入”章节，明确 `employee_id`、联系方式和账号状态。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:163:- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:165:- **最高优先级行动：** 立即补充班级-辅导员映射的数据规范和导入校验，这是自动审批闭环的关键缺口。
./docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:57:rsync -avz /data/backups/ backup-server:/backups/graduation-leave/
./docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:59:aws s3 sync /data/backups/ s3://backup-bucket/graduation-leave/
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:53:### 1.5 审批超时监控
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:145:Index(fields=['current_approver_id', 'status', 'submit_time'])
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:146:Index(fields=['student_id', 'status', 'created_at'])
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:147:Index(fields=['status', 'is_deleted', 'submit_time'])
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:149:# approvals表
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:150:Index(fields=['application_id', '-approval_time'])
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:204:    if self.status in ['draft', 'pending_counselor', 'pending_admin']:
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:207:            status__in=['draft', 'pending_counselor', 'pending_admin'],
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:212:            raise ValidationError("您已有进行中的申请，请等待审批完成")
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:325:**文档状态：** 共识已达成，准备更新设计文档
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:4:**状态:** ✓ 完成  
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:40:- `apps/approvals/tests/test_rejection_flow.py`
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:60:**问题:** 测试使用2020002，但mock数据中2020002已改为COMPLETED状态
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:64:2. 测试改用2020003（mock数据中为NOT_STARTED状态）
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:74:docker exec graduation-leave-system-backend-1 python manage.py test \
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:77:  apps.approvals.tests.test_rejection_flow
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:109:**修复:** 测试改用2020003（NOT_STARTED状态）  
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:143:**Phase 0状态:** **完成**
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:154:4. `apps/approvals/tests/test_rejection_flow.py` - 添加ClassMapping
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:27:- `test_state_machine`: 1 passing
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:86:**Action:** Clarify Dean scope: default to own pending approvals, not all applications.
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:113:1. `GET /api/approvals/` (PRIORITY 1)
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:115:   - Counselor: own pending approvals only (filter by approver_id)
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:116:   - Dean: own pending approvals only (filter by approver_id)
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:121:   - Dean: applications with own pending approvals (NOT all applications)
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:124:- Only support `?status=` parameter (whitelist: pending, approved, rejected)
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:149:2. Counselor cannot list other counselors' approvals
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:151:4. Dean cannot list other deans' approvals
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:164:- Counselor discovers approval via `GET /api/approvals/` (not from creation response)
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:166:- Dean discovers approval via `GET /api/approvals/` (not from creation response)
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:168:- Student verifies final status
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:180:- session-context.json: Update with Day 3 status
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:228:**Example (approvals list):**
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:235:    return Response({'error': 'Forbidden'}, status=403)
./docs/codex-review-protocol.md:178:**状态：** 已修复/通过
./backend/apps/approvals/tests/test_state_machine.py:3:from rest_framework import status
./backend/apps/approvals/tests/test_state_machine.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
./backend/apps/approvals/tests/test_state_machine.py:52:            leave_date='2024-06-30',
./backend/apps/approvals/tests/test_state_machine.py:53:            status=ApplicationStatus.PENDING_COUNSELOR
./backend/apps/approvals/tests/test_state_machine.py:56:        # Create counselor approval
./backend/apps/approvals/tests/test_state_machine.py:57:        self.approval = Approval.objects.create(
./backend/apps/approvals/tests/test_state_machine.py:58:            approval_id='apv_test001',
./backend/apps/approvals/tests/test_state_machine.py:68:    def test_duplicate_approval_conflict(self):
./backend/apps/approvals/tests/test_state_machine.py:69:        """测试重复审批返回409"""
./backend/apps/approvals/tests/test_state_machine.py:72:        # First approval
./backend/apps/approvals/tests/test_state_machine.py:74:            f'/api/approvals/{self.approval.approval_id}/approve/',
./backend/apps/approvals/tests/test_state_machine.py:78:        self.assertEqual(response1.status_code, status.HTTP_200_OK)
./backend/apps/approvals/tests/test_state_machine.py:80:        # Second approval attempt
./backend/apps/approvals/tests/test_state_machine.py:82:            f'/api/approvals/{self.approval.approval_id}/approve/',
./backend/apps/approvals/tests/test_state_machine.py:86:        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
./backend/apps/approvals/tests/test_state_machine.py:93:            f'/api/approvals/{self.approval.approval_id}/reject/',
./backend/apps/approvals/tests/test_state_machine.py:97:        self.assertEqual(response1.status_code, status.HTTP_200_OK)
./backend/apps/approvals/tests/test_state_machine.py:100:            f'/api/approvals/{self.approval.approval_id}/reject/',
./backend/apps/approvals/tests/test_state_machine.py:104:        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
./backend/apps/approvals/tests/test_state_machine.py:106:    def test_counselor_step_requires_pending_counselor_status(self):
./backend/apps/approvals/tests/test_state_machine.py:107:        """测试辅导员审批步骤与申请状态不匹配时返回409"""
./backend/apps/approvals/tests/test_state_machine.py:108:        self.application.status = ApplicationStatus.PENDING_DEAN
./backend/apps/approvals/tests/test_state_machine.py:113:            f'/api/approvals/{self.approval.approval_id}/approve/',
./backend/apps/approvals/tests/test_state_machine.py:118:            f'/api/approvals/{self.approval.approval_id}/reject/',
./backend/apps/approvals/tests/test_state_machine.py:123:        self.assertEqual(approve_response.status_code, status.HTTP_409_CONFLICT)
./backend/apps/approvals/tests/test_state_machine.py:124:        self.assertEqual(reject_response.status_code, status.HTTP_409_CONFLICT)
./backend/apps/approvals/tests/test_state_machine.py:126:    def test_dean_step_requires_pending_dean_status(self):
./backend/apps/approvals/tests/test_state_machine.py:127:        """测试学工部审批步骤与申请状态不匹配时返回409"""
./backend/apps/approvals/tests/test_state_machine.py:128:        self.application.status = ApplicationStatus.APPROVED
./backend/apps/approvals/tests/test_state_machine.py:130:        dean_approval = Approval.objects.create(
./backend/apps/approvals/tests/test_state_machine.py:131:            approval_id='apv_test002',
./backend/apps/approvals/tests/test_state_machine.py:141:            f'/api/approvals/{dean_approval.approval_id}/approve/',
./backend/apps/approvals/tests/test_state_machine.py:146:            f'/api/approvals/{dean_approval.approval_id}/reject/',
./backend/apps/approvals/tests/test_state_machine.py:151:        self.assertEqual(approve_response.status_code, status.HTTP_409_CONFLICT)
./backend/apps/approvals/tests/test_state_machine.py:152:        self.assertEqual(reject_response.status_code, status.HTTP_409_CONFLICT)
./backend/apps/approvals/models.py:12:    PENDING = 'pending', '待审批'
./backend/apps/approvals/models.py:18:    approval_id = models.CharField(max_length=50, primary_key=True)
./backend/apps/approvals/models.py:19:    application = models.ForeignKey(Application, on_delete=models.PROTECT, related_name='approvals')
./backend/apps/approvals/models.py:21:    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approvals')
./backend/apps/approvals/models.py:30:        db_table = 'approvals'
./backend/apps/users/views.py:1:from rest_framework import status
./backend/apps/users/views.py:13:        return Response(serializer.validated_data, status=status.HTTP_200_OK)
./backend/apps/users/views.py:14:    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:32:**问题6：** 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:55:- A. 数据库直连（需要安全审批和网络配置）
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:104:| 宿舍清退数据 | API实时查询 | 需要实时校验清退状态 |
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:165:**目标：** 实现宿舍清退状态实时查询
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:172:   - 响应解析（清退状态、完成时间）
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:174:   - API失败：返回 `checkout_status: "unknown"`
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:210:   - 无审批人的学生：0个
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:217:   - 辅导员登录和审批
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:219:   - 宿舍清退状态查询
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:220:   - 申请提交和审批流程
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:248:   - 辅导员审批效率
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:252:   - 审批流程优化
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:42:测试：学生看到表单UI，教师进审批页
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:73:    wx.redirectTo({ url: '/pages/approvals/approvals' });
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:98:  const { reason, leaveDate } = this.data;
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:108:  if (!leaveDate) {
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:113:  if (leaveDate < today) {
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:131:      leave_date: this.data.leaveDate
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:146:      CONFLICT: '您已有待审批或已通过的申请',
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:160:  wx.redirectTo({ url: '/pages/approvals/approvals' });
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:199:**状态：** 等待Codex反馈
./backend/apps/applications/admin.py:7:    list_display = ['application_id', 'student', 'student_name', 'class_id', 'status', 'created_at']
./backend/apps/applications/admin.py:8:    list_filter = ['status', 'dorm_checkout_status']
./docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:81:- 当前需求只是验证清退状态，不需要存储床号
./docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:121:| checkout_status | String | 清退状态 | 是 | "已完成" |
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:90:1. **存储冗余**：每次状态变更存储完整JSON，数据量大
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:122:1. **并发场景罕见**：同一申请同时被两个审批人操作的概率极低
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:123:2. **状态机已保护**：状态转换规则已限制非法操作
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:132:1. **Phase 1不实现乐观锁**：先用数据库事务+状态机保护
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:133:2. **监控实际冲突**：记录状态转换失败次数
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:140:- `idx_approver_status` (current_approver_id, status, submit_time)
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:141:- `idx_student_status` (student_id, status, created_at)
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:142:- `idx_status_deleted` (status, is_deleted, submit_time)
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:158:   - `idx_status` (按状态筛选)
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:205:部分表有`is_deleted`字段（users, applications, attachments），部分表没有（approvals, notifications）。不一致的设计增加理解成本。
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:210:- **不需要软删除**：审批记录、通知（历史数据，不删除）
./backend/apps/applications/providers.py:9:    status: str
./backend/apps/applications/providers.py:16:    def check_status(self, student_id: str) -> DormCheckoutStatusDTO:
./backend/apps/applications/providers.py:20:                status=DormCheckoutStatus.COMPLETED,
./backend/apps/applications/providers.py:27:                status=DormCheckoutStatus.COMPLETED,
./backend/apps/applications/providers.py:34:                status=DormCheckoutStatus.NOT_STARTED,
./backend/apps/applications/providers.py:41:                status=DormCheckoutStatus.COMPLETED,
./backend/apps/applications/providers.py:48:                status=DormCheckoutStatus.UNKNOWN,
./backend/apps/applications/providers.py:57:            status=DormCheckoutStatus.NOT_STARTED,
./docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:29:- ✅ 覆盖审批队列、通知查询、审计追踪
./docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:85:## 最终数据库设计状态
./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:10:**状态：** 已修复所有问题，达成共识
./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:18:6. ✓ P2 - 统一审批时限（1个工作日）
./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:124:### 修复6：统一审批时限 [P2]
./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:130:- 辅导员审批：提交后24小时内
./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:131:- 学工部审批：辅导员通过后24小时内
./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:136:- 辅导员审批：提交后1个工作日内
./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:137:- 学工部审批：辅导员通过后1个工作日内
./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:152:- 审批本年级学生的申请
./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:153:- 审批其他年级学生
./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:160:- 审批负责班级学生的申请
./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:161:- 审批其他班级学生
./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:205:- ✓ `docs/用户设计说明书.md` - 初始密码、审批时限、辅导员权限、性能指标
./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:219:**最终状态：** 通过
./backend/apps/users/migrations/0001_initial.py:22:                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
./docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:5:**审查范围：** API设计、审批流程、部署架构、安全设计、性能优化、测试策略
./docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:51:- 添加审批API版本检查
./docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:53:- 修正HTTP状态码（201/204）
./docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:55:### 批次3：审批流程
./docs/数据确认清单.md:31:**问题6：** 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
./docs/数据确认清单.md:54:- A. 数据库直连（需要安全审批和网络配置）
./docs/数据确认清单.md:103:| 宿舍清退数据 | API实时查询 | 需要实时校验清退状态 |
./docs/数据确认清单.md:151:**目标：** 实现宿舍清退状态实时查询
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:57:            status__in=['pending_counselor', 'pending_admin']
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:59:            raise ValidationError("该用户有待审批申请，无法删除")
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:73:**状态：** ✅ 同意修复
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:87:            models.Index(fields=['current_approver_id', 'status', 'submit_time'], 
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:88:                        name='idx_approver_status'),
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:89:            models.Index(fields=['student_id', 'status', 'created_at'], 
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:90:                        name='idx_student_status'),
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:91:            models.Index(fields=['status', 'is_deleted', 'submit_time'], 
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:92:                        name='idx_status_deleted'),
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:98:            models.Index(fields=['application_id', '-approval_time'], 
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:132:**状态：** ✅ 完全同意
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:19:## 2. 当前仓库状态
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:48:当前工作区已有未提交/未跟踪文件，包括 `.omc/` 下状态文件，以及 `docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md`、`11-remaining-sections-response.md`、`12-remaining-sections-consensus.md`。本次分析未回退这些文件。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:62:- 审批流程
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:188:- approvals：`approver_id BIGINT NOT NULL`，但外键 `ON DELETE SET NULL`
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:193:- 审批记录和审计日志优先保留历史，用户删除应使用软删除或 `PROTECT`
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:210:- `idx_approvals_application_id`
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:235:    condition=Q(status__in=["draft", "pending_counselor", "pending_admin"], is_deleted=False),
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:240:### 6.7 审批超时动作与枚举不一致
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:242:approvals 表字段说明写 `action: approve/reject`，但超时任务会创建 `action='timeout'`。需要把 `timeout` 加入枚举，或把超时记录拆成独立 `approval_timeouts`/notification 事件，避免审批记录语义混乱。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:246:审批记录字段说明写“1个工作日(24小时)”，第 5 章又写“1个工作日 = 8小时工作时间”。建议统一为：
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:278:审批 API 已有 `version` 字段和 409 响应，但更新申请、重新提交、附件变更、生成凭证等也可能改变申请状态或可审批性。建议明确所有会影响审批判断的写操作都必须纳入版本控制。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:280:### 7.3 驳回后重新提交的权限与状态未完全对齐
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:282:RBAC 描述中学生只能“修改草稿状态的申请”，但流程允许 rejected 重新提交。需要明确：
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:284:- rejected 状态允许学生修改
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:293:建议新增 `counselor_assignments` 或在用户/班级模型中维护负责关系，并在查询和审批时同时校验 `current_approver_id`。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:309:设计中 Access Token 有效期为 7 天，Refresh Token 30 天。对审批、附件、个人信息系统来说，7 天 access token 偏长。建议：
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:381:- 外部系统状态码映射
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:384:- 人工跳过验证的审批责任归属
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:385:- 外部系统不可用时是否允许提交还是只允许审批时跳过
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:452:单实例 Gunicorn 4 workers 下，`500 并发用户` 与 `>500 QPS` 可能对只读列表接口可达，但对审批写入、附件上传、外部系统调用不现实。建议性能指标按接口分类：
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:457:- 审批操作：P95/QPS
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:463:设计中缓存申请详情、申请状态、学生申请列表。对含个人信息和审批信息的数据，必须保证：
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:476:- 审批人待办列表
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:515:3. 附件上传、微信授权、Token 刷新、审批待办这四个流程应先做端到端原型。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:543:3. 审批状态机：明确 rejected 重新提交、version 递增、附件替换规则。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:545:5. 宿舍系统集成契约：状态码、超时、降级、人工跳过责任。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:575:建议把当前仓库状态定义为：
./docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:11:**状态：** 需要修改
./docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:101:### 问题6：审批时限口径不一致 [P2]
./docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:108:用户文档与系统设计文档审批时限口径不一致。
./docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:143:辅导员查看/审批权限按"本年级"划分过粗，实际应按学院、专业、班级或辅导员负责范围授权。
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:33:    response_status = models.IntegerField(null=True)
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:48:**状态：** ✅ 完全同意
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:63:    # 新增：固定审批人追踪
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:79:    planned_leave_date = models.DateField()
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:80:    status = models.CharField(max_length=20)
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:109:            models.Index(fields=['status']),
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:111:            models.Index(fields=['planned_leave_date']),
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:127:**状态：** ✅ 完全同意
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:180:**状态：** ✅ 完全同意
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:195:        if self.status in ['draft', 'pending_counselor', 'pending_admin']:
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:198:                status__in=['draft', 'pending_counselor', 'pending_admin'],
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:203:                raise ValidationError("您已有进行中的申请，请等待审批完成")
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:219:WHERE status IN ('draft', 'pending_counselor', 'pending_admin') 
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:223:**状态：** ✅ 同意修复
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:80:    return '您已有待审批或已通过的申请';
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:104:**当前方案：** 提交时验证reason非空且trim后非空，leave_date非空
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:107:- 是否需要验证leave_date不早于今天？（虽然picker设置了start=today，但用户可能修改系统时间）
./docs/discussions/codex-review-2026-05-27/01-architecture-review.md:80:- DoS审批队列（垃圾申请提交）
./docs/discussions/codex-review-2026-05-27/01-architecture-review.md:128:### 5. 审批超时监控不完整
./docs/discussions/codex-review-2026-05-27/01-architecture-review.md:156:- 但模块设计紧耦合，阻止真正的无状态扩展
./docs/discussions/codex-review-2026-05-27/01-architecture-review.md:169:- 无批量操作（辅导员审批50个申请需点击50次）
./docs/discussions/codex-review-2026-05-27/01-architecture-review.md:175:- 无审批重新分配
./docs/discussions/codex-review-2026-05-27/01-architecture-review.md:185:3. **"电子离校凭证"** - PDF证书 vs 数据库状态标志？
./docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:25:- ✅ 从外部数据库读取数据（如宿舍清退状态）
./docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:68:    def get_checkout_status(self, student_id):
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:71:学号,姓名,班级,宿舍楼栋,宿舍房间号,床号,是否已清退,清退日期,清退状态,备注
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:139:- 清退信息：is_checked_out、checkout_date、checkout_status
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:39:| 辅导员基本信息 | P0 | 创建辅导员账号、审批权限 | **CSV/Excel首版优先** / 人事或统一身份API增强 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:40:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:46:- **DB备选**：直接读取宿管系统数据库（需要安全审批和网络配置）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:50:1. **实施周期**：CSV/Excel导入最快，DB直连需要安全审批和网络配置
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:64:- 自动分配审批人（根据班级匹配辅导员）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:111:- 展示清退状态和完成时间
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:119:| 清退状态 | checkout_status | 枚举 | **是** | 清退状态（**v2改为必填**） | completed |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:120:| 清退完成时间 | checkout_date | 日期时间 | 条件必填 | 当status=completed时必填 | 2026-05-20 14:30:00 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:135:  "checkout_status": "completed",
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:142:- API查询失败时，返回 `checkout_status: "unknown"`
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:151:- 审批权限管理
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:167:- `is_active`：标识是否在职，`false`时不能登录、不能审批，但历史记录可查询
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:183:| 账号状态 | 登录 | 创建申请 | 审批 | 查看历史 | 接收通知 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:193:- 学生提交申请时自动分配辅导员审批人
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:228:- 导入后输出校验报告：未匹配班级、未匹配辅导员、重复映射、无审批人的学生数
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:378:    import_status ENUM('pending', 'success', 'partial', 'failed'),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:491:    planned_leave_date_start DATE,              -- 允许的最早离校日期
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:492:    planned_leave_date_end DATE,                -- 允许的最晚离校日期
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:522:6. 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:680:    planned_leave_date_start DATE,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:681:    planned_leave_date_end DATE,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:701:    import_status ENUM('pending', 'success', 'partial', 'failed'),
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:28:| 辅导员 | counselor | ~50人 | 一级审批 | 人事系统 + 教务系统 |
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:42:- 自动分配审批人（根据班级）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:58:**当前状态：** ❌ 未在数据对接文档中说明
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:74:- 清退状态（is_checked_out, checkout_date）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:80:**当前状态：** ✅ 已在数据对接文档中详细说明
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:90:- 分配审批权限
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:104:**当前状态：** ❌ 未在数据对接文档中说明
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:113:- 自动分配审批人
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:126:**当前状态：** ❌ 未在数据对接文档中说明
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:129:- 如果没有这个数据，系统无法自动分配审批人
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:153:**当前状态：** ❌ 未在数据对接文档中说明
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:163:### 4.1 图书馆清书状态
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:189:### 4.2 财务结清状态
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:215:### 4.3 学籍状态（毕业生识别）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:227:- 学籍状态（status：在读/毕业/结业/肄业）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:258:| 数据源 | 来源系统 | 对接方式 | 当前状态 |
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:270:| 图书馆清书状态 | 图书馆系统 | API/CSV | 手动上传截图 |
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:271:| 财务结清状态 | 财务系统 | API/CSV | 手动上传截图 |
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:272:| 学籍状态 | 教务系统 | API | 包含在学生信息中 |
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:282:- 🔴 **影响：** 系统无法自动分配审批人
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:324:6. **学籍状态是否需要单独对接？**
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:13:- ✓ Round 2审查：API、审批、部署、安全、性能、测试（2 CRITICAL + 21 MAJOR + 6 MINOR）
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:16:### 当前状态
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:35:- 6个核心模块（accounts, applications, approvals, attachments, notifications, integrations）
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:50:- applications表的复合索引（idx_approver_status, idx_student_status, idx_status_deleted）
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:70:### 4. 审批流程审查
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:73:- [ ] 状态机设计是否完整？
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:74:- [ ] 状态转换规则是否清晰？
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:80:- 5个状态（draft, pending_counselor, pending_admin, approved, rejected）
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:82:- 乐观锁防止并发审批
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:83:- 审批历史追踪（applications_history表）
./docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:117:  - 如果只用于验证清退状态：不需要存储
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:14:2. 角色保护闭环未完成（onShow逻辑错误 + approvals缺保护）
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:24:**Codex指出：** 新增`leave_date≥today`校验后，旧测试使用`2024-06-30`导致提交返回400而非201/422/409
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:34:# 旧：'leave_date': '2024-06-30'
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:35:# 新：'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:41:# - backend/apps/approvals/tests/test_rejection_flow.py (lines 58, 95)
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:53:- 当前逻辑：onLoad redirectTo approvals，onShow reLaunch login
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:68:    wx.redirectTo({ url: '/pages/approvals/approvals' });
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:77:### P1-3：approvals.ts缺少角色保护
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:79:**Codex指出：** 审批页只检查登录，不检查角色，学生可访问并收到403错误
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:84:- 实际影响：学生手动访问审批页，调用API后显示403
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:88:// miniprogram/pages/approvals/approvals.ts:16-35
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:134:### P2-4：UTC vs Asia/Shanghai时区错位
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:136:**Codex指出：** 前端用UTC日期，后端用Asia/Shanghai，北京时间00:00-07:59可能错一天
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:139:- 前端：`new Date().toISOString().split('T')[0]` = UTC日期
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:140:- 后端：`timezone.now().date()` = Asia/Shanghai日期
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:141:- 风险窗口：北京时间00:00-07:59（UTC前一天16:00-23:59）
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:164:  if (leaveDate < today) {
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:173:### P2-5：审批列表信息弱
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:175:**Codex指出：** 列表显示approver_name（审批人自己），不是学生信息
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:180:- 可用性：审批人看到自己名字，无法识别是哪个学生的申请
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:186:<!-- miniprogram/pages/approvals/approvals.wxml:10 -->
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:192:- 扩展ApprovalListSerializer添加student_name/class_id/leave_date
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:207:   - P1-3：添加approvals.ts角色保护（onLoad + onShow）
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:208:   - P2-4：创建本地日期helper，替换UTC日期
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:209:   - P2-5：快速修复审批列表显示（不改后端）
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:213:   - 手工验证角色保护：student不能进approvals，counselor/dean不能停留student-application
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:229:4. `backend/apps/approvals/tests/test_rejection_flow.py` - 动态日期
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:234:3. `miniprogram/pages/approvals/approvals.ts` - 添加角色保护
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:235:4. `miniprogram/pages/approvals/approvals.wxml` - 快速修复列表显示
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:33:- backend/apps/approvals/tests/test_rejection_flow.py
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:70:      : '/pages/approvals/approvals';
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:97:### 3. P2-4日期helper严格对齐Asia/Shanghai
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:101:- 但后端明确`TIME_ZONE = 'Asia/Shanghai'`
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:103:- 建议命名为`getShanghaiDateString()`，用UTC+8生成
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:139:  if (leaveDate < today) {
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:162:4. backend/apps/approvals/tests/test_rejection_flow.py - 动态日期
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:168:2. **miniprogram/utils/date.ts** - 新建Asia/Shanghai日期helper
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:170:4. miniprogram/pages/approvals/approvals.ts - 使用role-guard
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:172:6. miniprogram/pages/approvals/approvals.wxml - 快速修复列表显示
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:193:5. 列表UI：审批列表显示申请ID而非审批人名
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:40:4. ✅ **MAJOR - 审批API缺少版本检查**
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:44:   - 将添加：当前审批人验证
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:51:6. ✅ **MINOR - HTTP状态码不符合RESTful**
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:60:- 添加审批API版本检查
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:62:- 修正HTTP状态码
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:66:## 第5章：审批流程设计 - 响应
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:78:   - 同意。`is_timeout`在`approvals`表，不在`applications`表
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:79:   - 将修改：标记超时到`approvals`记录
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:81:3. ✅ **MAJOR - 工作流未设置审批人字段**
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:89:   - 将添加：每次状态转换创建`applications_history`快照
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:237:6. ✅ **MINOR - API测试状态码**
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:247:- 修正测试示例状态码
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:257:- 第3章API设计（微信绑定、配置、版本、上传、状态码）
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:260:- 第5章审批流程（工作日、字段更新、历史、审计）
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:246:    -- 认证状态字段
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:276:修正后的 `chk_auth_method` 允许三种认证状态：
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:333:    # 检查账号状态
./docs/discussions/codex-review-2026-05-27/02-architecture-response.md:36:**状态：** ✅ 同意修复
./docs/discussions/codex-review-2026-05-27/02-architecture-response.md:96:                'status': 'password_required',
./docs/discussions/codex-review-2026-05-27/02-architecture-response.md:98:            }, status=400)
./docs/discussions/codex-review-2026-05-27/02-architecture-response.md:115:        'status': 'password_setup_required',
./docs/discussions/codex-review-2026-05-27/02-architecture-response.md:132:**状态：** ⚠️ 部分同意，提出改进方案
./docs/discussions/codex-review-2026-05-27/02-architecture-response.md:164:**状态：** ✅ 完全同意
./docs/discussions/codex-review-2026-05-27/02-architecture-response.md:199:**状态：** ✅ 完全同意
./docs/discussions/codex-review-2026-05-27/02-architecture-response.md:203:### 5. 审批超时监控 - **完全同意**
./docs/discussions/codex-review-2026-05-27/02-architecture-response.md:239:**状态：** ✅ 完全同意
./docs/discussions/codex-review-2026-05-27/02-architecture-response.md:266:**状态：** ✅ 同意修复
./backend/apps/users/management/commands/seed_data.py:13:            help='Clear applications and approvals before loading seed data',
./backend/apps/users/management/commands/seed_data.py:18:            self.stdout.write('Resetting applications and approvals...')
./backend/apps/users/management/commands/seed_data.py:20:            from apps.approvals.models import Approval
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:281:    user.wechat_bind_time = timezone.now()
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:352:CREATE INDEX idx_status ON applications(status);
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:365:def check_approval_timeout():
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:366:    """检查审批超时（简化版）"""
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:368:        status__in=['pending_counselor', 'pending_admin'],
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:433:+ 核心模块强制TDD：认证、审批、状态机
./docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:10:**状态：** 已修复所有问题，达成共识
./docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:92:    "checkout_status": "completed"
./docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:101:- 新增 `checkout_status`
./docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:121:| checkout_status | String | 清退状态 | 是 | "completed" |
./docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:162:**最终状态：** 通过
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:17:3. 宿舍清退字段与上一轮字段共识存在轻微不一致：`checkout_status` 在本文件中标为可选，但既有字段共识中 API 响应建议必填。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:18:4. 缺少若干实施级关键问题，例如账号标识映射、终审管理员分配规则、同步覆盖策略、历史审批人不被后续映射变更自动改写等。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:34:| 辅导员基本信息 | 完整 | 支撑辅导员账号和一级审批主体。 |
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:40:图书馆清书状态、财务结清状态、独立学籍状态没有列为 P0 是合理的。当前用户设计和系统设计仍保留截图上传、人工审核和宿舍系统异常时人工降级的方案，因此这三类不应阻塞首版上线。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:60:1. `is_graduating` 建议改名或补充为 `eligible_for_leave` / `graduation_status`。  
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:61:   仅“是否毕业生”不足以表达延期毕业、结业、休学、退学、已毕业归档等异常状态。首版可以保留 `is_graduating`，但建议增加一个更直接的离校资格字段。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:75:1. `checkout_status` 建议改为必填，且给出枚举：`completed`、`pending`、`not_started`、`unknown`。  
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:76:   既有字段共识已将 `checkout_status` 作为 API 响应必填字段，本文件标为可选会造成实现歧义。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:78:2. `checkout_date` 应明确条件必填：当 `is_checked_out = true` 或 `checkout_status = completed` 时必填，未清退时允许为空。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:93:   `is_active` 已有，但应补充离职、调岗、停用后如何处理其名下未完成审批，以及是否允许历史审批记录继续引用已停用账号。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:111:3. 管理员离岗后未完成审批任务如何转交。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:181:2. 是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:258:| 离校申请资格 | eligible_for_leave | 布尔 | 建议是 | 是否允许提交本批次离校申请 | true |
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:259:| 学籍/毕业状态 | graduation_status | 文本 | 否 | graduating/delayed/graduated/suspended/withdrawn | graduating |
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:269:| checkout_status | 可选 | 必填，枚举：completed/pending/not_started/unknown |
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:279:3. `is_active=false` 时不再分配新申请，但历史审批记录仍保留。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:287:| 是否主辅导员 | is_primary | 布尔 | 否 | 多辅导员场景下标识主审批人 |
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:311:3. 统一宿舍清退字段必填性，特别是 `checkout_status`。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:312:4. 补充终审管理员/终审组配置、账号标识映射、历史审批人一致性规则。
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:17:| 辅导员基本信息 | P0 | 创建辅导员账号、审批权限 | DB优先 / API备选 / CSV降级 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:18:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | DB优先 / API备选 / CSV降级 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:36:- 自动分配审批人（根据班级匹配辅导员）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:110:| 清退状态 | checkout_status | 文本 | 否 | completed/pending/not_started | completed |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:117:- 接口地址：`/api/dorm/checkout/status`
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:131:    checkout_status,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:148:- 分配审批权限
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:149:- 作为一级审批人
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:193:- 自动分配审批人（学生提交申请时，根据班级自动找到对应辅导员）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:194:- 辅导员权限边界（辅导员只能查看和审批负责班级的学生）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:196:- 审批统计按班级、辅导员追踪
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:199:- 如果没有这个数据，系统无法自动分配审批人
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:331:- 参考当前数据对接文档中的宿舍清退状态查询接口
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:376:- 清退状态必须真实准确
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:431:1. 除了宿舍清退状态查询接口，是否可以提供其他数据查询接口？
./docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:111:### 问题6：审批时限口径不一致 [P2]
./docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:122:3. 与审批流程设计一致
./docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:232:7. ✓ 问题6：统一审批时限
./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:23:- 状态管理复杂（temp_token vs limited_token）
./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:37:  "status": "success|need_bind|need_setup",
./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:172:2. **学工部权限过大**：admin既能审批又能管理系统配置
./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:182:admin_approver   # 学工部审批员（只能审批）
./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:183:admin_manager    # 学工部管理员（审批+配置管理）
./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:246:**下一部分：** Part 3 - 审批流程与外部集成
./docs/discussions/codex-review-2026-05-27/04-database-review.md:27:- 查询`applications WHERE is_deleted=FALSE`会返回申请，但关联的用户是已删除状态
./docs/discussions/codex-review-2026-05-27/04-database-review.md:67:**查询1：** "显示辅导员X的待审批申请"
./docs/discussions/codex-review-2026-05-27/04-database-review.md:70:WHERE status = 'pending_counselor' 
./docs/discussions/codex-review-2026-05-27/04-database-review.md:75:-- 当前索引：idx_status, 无current_approver_id索引
./docs/discussions/codex-review-2026-05-27/04-database-review.md:93:CREATE INDEX idx_approver_status ON applications(current_approver_id, status, submit_time);
./docs/discussions/codex-review-2026-05-27/04-database-review.md:94:CREATE INDEX idx_student_status ON applications(student_id, status, created_at);
./docs/discussions/codex-review-2026-05-27/04-database-review.md:95:CREATE INDEX idx_status_deleted ON applications(status, is_deleted, submit_time);
./docs/discussions/codex-review-2026-05-27/04-database-review.md:97:-- approvals表
./docs/discussions/codex-review-2026-05-27/04-database-review.md:98:CREATE INDEX idx_app_time ON approvals(application_id, approval_time DESC);
./docs/discussions/codex-review-2026-05-27/04-database-review.md:128:- "追踪这个审批工作流中的所有操作" → 无correlation_id
./docs/discussions/codex-review-2026-05-27/04-database-review.md:149:    response_status INT,
./docs/discussions/codex-review-2026-05-27/04-database-review.md:165:- 无`admin_id`（谁做的最终审批？）
./docs/discussions/codex-review-2026-05-27/04-database-review.md:171:2. 并发bug：两个审批人同时批准 → 无乐观锁
./docs/discussions/codex-review-2026-05-27/04-database-review.md:179:    -- 新增固定审批人追踪
./docs/discussions/codex-review-2026-05-27/04-database-review.md:237:- 但无约束防止：学生创建多个草稿、同时提交多个申请、待审批时重复提交
./docs/discussions/codex-review-2026-05-27/04-database-review.md:244:WHERE status IN ('draft', 'pending_counselor', 'pending_admin') 
./docs/discussions/codex-review-2026-05-27/04-database-review.md:251:        if self.status in ['draft', 'pending_counselor', 'pending_admin']:
./docs/discussions/codex-review-2026-05-27/04-database-review.md:254:                status__in=['draft', 'pending_counselor', 'pending_admin'],
./docs/discussions/codex-review-2026-05-27/04-database-review.md:259:                raise ValidationError("您已有进行中的申请，请等待审批完成")
./docs/discussions/codex-review-2026-05-27/04-database-review.md:279:`send_status`追踪失败，但无重试计数器。
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:36:2. 即使使用 `DELETE FROM users`，也会导致历史申请记录中的审批人引用失效
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:281:    planned_leave_date_start DATE,              -- 允许的最早离校日期
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:282:    planned_leave_date_end DATE,                -- 允许的最晚离校日期
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:316:    import_status ENUM('pending', 'success', 'partial', 'failed'),
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:342:| 账号状态 | 登录 | 创建申请 | 审批 | 查看历史 | 接收通知 |
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:486:- 第186-196行：历史审批人一致性规则的思考过程
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:1:# Round 3 Claude分析 - Part 3: 审批流程与外部集成
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:5:**分析范围：** 第5-6章（审批流程设计、外部系统集成设计）
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:9:## 第5章：审批流程设计
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:35:def check_approval_timeout():
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:37:        status__in=['pending_counselor', 'pending_admin']
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:54:`check_approval_timeout()`每小时执行一次，扫描所有待审批申请。
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:74:def check_approval_timeout():
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:77:        status__in=['pending_counselor', 'pending_admin'],
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:85:#### MINOR - 状态机转换规则缺少并发保护
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:88:状态转换规则定义清晰，但代码实现中缺少并发保护：
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:97:如果两个审批人同时审批同一申请，可能导致状态不一致。
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:109:    # 验证审批人
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:111:        raise PermissionDenied("不是当前审批人")
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:113:    # 验证状态转换
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:115:        if app.status == 'pending_counselor':
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:116:            app.status = 'pending_admin'
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:117:        elif app.status == 'pending_admin':
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:118:            app.status = 'approved'
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:125:- ✓ 状态机设计清晰
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:126:- ✓ 状态转换规则完整
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:127:- ✓ 审批历史记录完善
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:133:3. 添加并发保护（状态转换加锁）
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:179:    result = dorm_api.check_status(student_id, timeout=2)
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:183:    return {"status": "pending", "message": "正在验证，请稍后刷新"}
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:188:    result = dorm_api.check_status(student_id)
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:189:    # 更新申请状态
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:195:设计提到"审批人可选择'跳过验证'并备注原因"，但未说明如何审计这些操作。
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:251:5. 状态转换并发保护
./docs/design/2026-05-27-system-design.md:1:# 毕业生离校申请审批系统 - 系统设计文档
./docs/design/2026-05-27-system-design.md:3:**项目名称：** 毕业生离校申请审批系统  
./docs/design/2026-05-27-system-design.md:16:5. [审批流程设计](#5-审批流程设计)
./docs/design/2026-05-27-system-design.md:35:2. **一级审批：** 毕业年级辅导员审核
./docs/design/2026-05-27-system-design.md:138:graduation_leave/
./docs/design/2026-05-27-system-design.md:149:│   │   ├── workflows.py   # 审批流程
./docs/design/2026-05-27-system-design.md:150:│   │   └── states.py      # 状态机定义
./docs/design/2026-05-27-system-design.md:152:│   ├── approvals/         # 审批管理模块
./docs/design/2026-05-27-system-design.md:153:│   │   ├── models.py      # 审批记录
./docs/design/2026-05-27-system-design.md:154:│   │   ├── views.py       # 审批操作API
./docs/design/2026-05-27-system-design.md:196:   - 申请状态查询
./docs/design/2026-05-27-system-design.md:200:3. **approvals（审批管理）**
./docs/design/2026-05-27-system-design.md:201:   - 辅导员审批操作
./docs/design/2026-05-27-system-design.md:203:   - 审批意见记录
./docs/design/2026-05-27-system-design.md:205:   - 审批时限监控
./docs/design/2026-05-27-system-design.md:217:   - 审批状态变更通知
./docs/design/2026-05-27-system-design.md:219:   - 审批完成通知
./docs/design/2026-05-27-system-design.md:225:   - 宿舍清退状态查询
./docs/design/2026-05-27-system-design.md:248:3. approvals - 审批记录表
./docs/design/2026-05-27-system-design.md:312:    -- 固定审批人追踪
./docs/design/2026-05-27-system-design.md:316:    planned_leave_date DATE NOT NULL COMMENT '计划离校日期',
./docs/design/2026-05-27-system-design.md:317:    status VARCHAR(20) NOT NULL COMMENT '状态',
./docs/design/2026-05-27-system-design.md:318:    current_approver_id BIGINT COMMENT '当前审批人ID',
./docs/design/2026-05-27-system-design.md:343:    INDEX idx_status (status),
./docs/design/2026-05-27-system-design.md:345:    INDEX idx_planned_leave_date (planned_leave_date),
./docs/design/2026-05-27-system-design.md:346:    INDEX idx_approver_status (current_approver_id, status, submit_time),
./docs/design/2026-05-27-system-design.md:347:    INDEX idx_student_status (student_id, status, created_at),
./docs/design/2026-05-27-system-design.md:348:    INDEX idx_status_deleted (status, is_deleted, submit_time)
./docs/design/2026-05-27-system-design.md:352:**状态枚举（status）：**
./docs/design/2026-05-27-system-design.md:356:- `approved` - 审批通过
./docs/design/2026-05-27-system-design.md:362:### 2.4 审批记录表（approvals）
./docs/design/2026-05-27-system-design.md:365:CREATE TABLE approvals (
./docs/design/2026-05-27-system-design.md:368:    approver_id BIGINT NOT NULL COMMENT '审批人ID',
./docs/design/2026-05-27-system-design.md:369:    approver_role VARCHAR(20) NOT NULL COMMENT '审批人角色',
./docs/design/2026-05-27-system-design.md:371:    opinion TEXT COMMENT '审批意见',
./docs/design/2026-05-27-system-design.md:372:    approval_time TIMESTAMP NOT NULL COMMENT '审批时间',
./docs/design/2026-05-27-system-design.md:381:    INDEX idx_approval_time (approval_time),
./docs/design/2026-05-27-system-design.md:382:    INDEX idx_app_time (application_id, approval_time DESC)
./docs/design/2026-05-27-system-design.md:383:) COMMENT='审批记录表';
./docs/design/2026-05-27-system-design.md:437:    send_status VARCHAR(20) DEFAULT 'pending' COMMENT '发送状态',
./docs/design/2026-05-27-system-design.md:448:    INDEX idx_send_status (send_status),
./docs/design/2026-05-27-system-design.md:455:- `approval_pending` - 待审批
./docs/design/2026-05-27-system-design.md:458:- `approval_timeout` - 审批超时提醒
./docs/design/2026-05-27-system-design.md:460:**发送状态（send_status）：**
./docs/design/2026-05-27-system-design.md:523:    response_status INT COMMENT '响应状态码',
./docs/design/2026-05-27-system-design.md:544:- `approve` - 审批通过
./docs/design/2026-05-27-system-design.md:545:- `reject` - 审批驳回
./docs/design/2026-05-27-system-design.md:553:- `approval` - 审批
./docs/design/2026-05-27-system-design.md:593:  ├─1:N─→ approvals (审批人审批多个申请)
./docs/design/2026-05-27-system-design.md:600:  ├─N:1─→ users (当前审批人)
./docs/design/2026-05-27-system-design.md:601:  ├─1:N─→ approvals (一个申请多条审批记录)
./docs/design/2026-05-27-system-design.md:607:approvals (审批记录表)
./docs/design/2026-05-27-system-design.md:608:  ├─N:1─→ applications (多条审批记录属于一个申请)
./docs/design/2026-05-27-system-design.md:609:  └─N:1─→ users (审批人)
./docs/design/2026-05-27-system-design.md:627:2. 一个申请必须经过2级审批（辅导员→学工部）
./docs/design/2026-05-27-system-design.md:628:3. 每个审批节点记录一条审批记录
./docs/design/2026-05-27-system-design.md:641:- 合理的HTTP状态码
./docs/design/2026-05-27-system-design.md:668:    "planned_leave_date": ["日期不能早于今天"]
./docs/design/2026-05-27-system-design.md:856:  "planned_leave_date": "2026-06-15",
./docs/design/2026-05-27-system-design.md:866:    "status": "draft",
./docs/design/2026-05-27-system-design.md:867:    "planned_leave_date": "2026-06-15",
./docs/design/2026-05-27-system-design.md:875:GET /api/v1/applications?status=pending_counselor&page=1&page_size=20
./docs/design/2026-05-27-system-design.md:891:        "status": "pending_counselor",
./docs/design/2026-05-27-system-design.md:892:        "planned_leave_date": "2026-06-15",
./docs/design/2026-05-27-system-design.md:917:    "status": "pending_counselor",
./docs/design/2026-05-27-system-design.md:918:    "planned_leave_date": "2026-06-15",
./docs/design/2026-05-27-system-design.md:927:    "approvals": [
./docs/design/2026-05-27-system-design.md:932:        "approval_time": "2026-05-27T14:00:00Z"
./docs/design/2026-05-27-system-design.md:946:  "planned_leave_date": "2026-06-20",
./docs/design/2026-05-27-system-design.md:967:    "status": "pending_counselor",
./docs/design/2026-05-27-system-design.md:973:### 3.4 审批相关API
./docs/design/2026-05-27-system-design.md:975:**1. 获取待审批列表**
./docs/design/2026-05-27-system-design.md:977:GET /api/v1/approvals/pending?page=1&page_size=20
./docs/design/2026-05-27-system-design.md:990:        "planned_leave_date": "2026-06-15",
./docs/design/2026-05-27-system-design.md:999:**2. 审批通过**
./docs/design/2026-05-27-system-design.md:1001:POST /api/v1/approvals/{application_id}/approve
./docs/design/2026-05-27-system-design.md:1013:  "message": "审批成功",
./docs/design/2026-05-27-system-design.md:1015:    "status": "pending_admin",
./docs/design/2026-05-27-system-design.md:1031:**3. 审批驳回**
./docs/design/2026-05-27-system-design.md:1033:POST /api/v1/approvals/{application_id}/reject
./docs/design/2026-05-27-system-design.md:1047:    "status": "rejected",
./docs/design/2026-05-27-system-design.md:1315:├─ 修改草稿状态的申请
./docs/design/2026-05-27-system-design.md:1321:├─ 审批申请（通过/驳回）
./docs/design/2026-05-27-system-design.md:1322:├─ 查看审批历史
./docs/design/2026-05-27-system-design.md:1327:├─ 最终备案审批
./docs/design/2026-05-27-system-design.md:1341:辅导员审批         | ✗       | ✓         | ✗
./docs/design/2026-05-27-system-design.md:1342:学工部审批         | ✗       | ✗         | ✓
./docs/design/2026-05-27-system-design.md:1388:## 5. 审批流程设计
./docs/design/2026-05-27-system-design.md:1390:### 5.1 流程状态机
./docs/design/2026-05-27-system-design.md:1392:**状态定义：**
./docs/design/2026-05-27-system-design.md:1401:approved（审批通过）
./docs/design/2026-05-27-system-design.md:1404:**状态转换规则：**
./docs/design/2026-05-27-system-design.md:1408:    'pending_counselor': ['pending_admin', 'rejected'],  # 辅导员审批
./docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
./docs/design/2026-05-27-system-design.md:1425:  - 状态变更：draft → pending_counselor
./docs/design/2026-05-27-system-design.md:1427:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
./docs/design/2026-05-27-system-design.md:1428:  - 设置当前审批人：current_approver_id = counselor_id
./docs/design/2026-05-27-system-design.md:1437:- 触发条件：申请状态为 pending_counselor
./docs/design/2026-05-27-system-design.md:1442:    - 状态变更 → pending_admin
./docs/design/2026-05-27-system-design.md:1443:    - 更新当前审批人：current_approver_id = admin_id
./docs/design/2026-05-27-system-design.md:1445:    - 创建审批记录：approvals（approver_role='counselor', action='approve'）
./docs/design/2026-05-27-system-design.md:1446:    - 创建历史快照：applications_history（version=N, change_reason='辅导员审批通过'）
./docs/design/2026-05-27-system-design.md:1450:    - 状态变更 → rejected
./docs/design/2026-05-27-system-design.md:1451:    - 清空当前审批人：current_approver_id = NULL
./docs/design/2026-05-27-system-design.md:1453:    - 创建审批记录：approvals（approver_role='counselor', action='reject'）
./docs/design/2026-05-27-system-design.md:1457:  - 记录审批意见和时间
./docs/design/2026-05-27-system-design.md:1462:- 触发条件：申请状态为 pending_admin
./docs/design/2026-05-27-system-design.md:1467:    - 状态变更 → approved
./docs/design/2026-05-27-system-design.md:1468:    - 清空当前审批人：current_approver_id = NULL
./docs/design/2026-05-27-system-design.md:1472:    - 创建审批记录：approvals（approver_role='admin', action='approve'）
./docs/design/2026-05-27-system-design.md:1478:    - 状态变更 → rejected
./docs/design/2026-05-27-system-design.md:1479:    - 清空当前审批人：current_approver_id = NULL
./docs/design/2026-05-27-system-design.md:1481:    - 创建审批记录：approvals（approver_role='admin', action='reject'）
./docs/design/2026-05-27-system-design.md:1490:- 触发条件：申请状态为 rejected
./docs/design/2026-05-27-system-design.md:1506:def check_approval_timeout():
./docs/design/2026-05-27-system-design.md:1507:    # 查询待审批的申请
./docs/design/2026-05-27-system-design.md:1509:        status__in=['pending_counselor', 'pending_admin'],
./docs/design/2026-05-27-system-design.md:1514:        # 获取最新审批记录（当前节点）
./docs/design/2026-05-27-system-design.md:1515:        latest_approval = app.approvals.filter(
./docs/design/2026-05-27-system-design.md:1519:        if not latest_approval:
./docs/design/2026-05-27-system-design.md:1523:            # 已有审批记录，从上次审批时间开始计算
./docs/design/2026-05-27-system-design.md:1524:            start_time = latest_approval.approval_time
./docs/design/2026-05-27-system-design.md:1530:            # 创建超时审批记录
./docs/design/2026-05-27-system-design.md:1534:                approver_role=app.status.replace('pending_', ''),
./docs/design/2026-05-27-system-design.md:1583:- 第1次：办理时限到期时通知审批人
./docs/design/2026-05-27-system-design.md:1584:- 第2次：超时4小时后通知审批人上级
./docs/design/2026-05-27-system-design.md:1589:- 审批人可选择"跳过验证"并备注原因
./docs/design/2026-05-27-system-design.md:1608:验证学生宿舍清退状态，确保离校手续真实完成。
./docs/design/2026-05-27-system-design.md:1622:# 查询宿舍清退状态
./docs/design/2026-05-27-system-design.md:1623:GET /api/dorm/clearance/status
./docs/design/2026-05-27-system-design.md:1641:    "checkout_status": "completed"
./docs/design/2026-05-27-system-design.md:1657:    def get_checkout_status(self, student_id):
./docs/design/2026-05-27-system-design.md:1682:                f"{self.api_url}/clearance/status",
./docs/design/2026-05-27-system-design.md:1734:- 审批人可选择"跳过验证"并备注原因
./docs/design/2026-05-27-system-design.md:1999:    user.wechat_bind_time = timezone.now()
./docs/design/2026-05-27-system-design.md:2019:        response_status=200 if success else 400,
./docs/design/2026-05-27-system-design.md:2040:    user.wechat_bind_time = timezone.now()
./docs/design/2026-05-27-system-design.md:2053:        response_status=200 if success else 400,
./docs/design/2026-05-27-system-design.md:2233:- 审批操作：通过、驳回
./docs/design/2026-05-27-system-design.md:2256:    response_status = models.IntegerField()
./docs/design/2026-05-27-system-design.md:2272:    cutoff_date = timezone.now() - timedelta(days=int(retention_days))
./docs/design/2026-05-27-system-design.md:2347:CREATE INDEX idx_status ON applications(status);
./docs/design/2026-05-27-system-design.md:2349:CREATE INDEX idx_planned_leave_date ON applications(planned_leave_date);
./docs/design/2026-05-27-system-design.md:2352:CREATE INDEX idx_approver_status ON applications(current_approver_id, status, submit_time);
./docs/design/2026-05-27-system-design.md:2353:CREATE INDEX idx_student_status ON applications(student_id, status, created_at);
./docs/design/2026-05-27-system-design.md:2354:CREATE INDEX idx_status_deleted ON applications(status, is_deleted, submit_time);
./docs/design/2026-05-27-system-design.md:2356:-- approvals表索引
./docs/design/2026-05-27-system-design.md:2357:CREATE INDEX idx_application_id ON approvals(application_id);
./docs/design/2026-05-27-system-design.md:2358:CREATE INDEX idx_approver_id ON approvals(approver_id);
./docs/design/2026-05-27-system-design.md:2359:CREATE INDEX idx_approval_time ON approvals(approval_time);
./docs/design/2026-05-27-system-design.md:2360:CREATE INDEX idx_app_time ON approvals(application_id, approval_time DESC);
./docs/design/2026-05-27-system-design.md:2371:CREATE INDEX idx_send_status ON notifications(send_status);
./docs/design/2026-05-27-system-design.md:2386:- `idx_approver_status`: 待审批列表查询（按审批人+状态+时间）
./docs/design/2026-05-27-system-design.md:2387:- `idx_student_status`: 学生查看自己申请列表
./docs/design/2026-05-27-system-design.md:2388:- `idx_status_deleted`: 按状态筛选未删除申请
./docs/design/2026-05-27-system-design.md:2389:- `idx_app_time`: 申请的审批历史（按时间倒序）
./docs/design/2026-05-27-system-design.md:2406:        'NAME': 'graduation_leave',
./docs/design/2026-05-27-system-design.md:2420:graduation_leave = host=postgres port=5432 dbname=graduation_leave
./docs/design/2026-05-27-system-design.md:2438:# L2: 申请状态缓存（5分钟）
./docs/design/2026-05-27-system-design.md:2439:cache.set(f'app:{app_id}:status', status, 300)
./docs/design/2026-05-27-system-design.md:2441:# L3: 待审批数量缓存（1分钟）
./docs/design/2026-05-27-system-design.md:2454:    """申请状态变更时失效相关缓存"""
./docs/design/2026-05-27-system-design.md:2455:    cache.delete(f'app:{application_id}:status')
./docs/design/2026-05-27-system-design.md:2458:    # 失效审批人的待审批数量缓存
./docs/design/2026-05-27-system-design.md:2481:- 审批操作（必须实时）
./docs/design/2026-05-27-system-design.md:2565:    app = Application.objects.create(status='draft')
./docs/design/2026-05-27-system-design.md:2576:    self.status = 'pending_counselor'
./docs/design/2026-05-27-system-design.md:2586:def test_application_status_transition():
./docs/design/2026-05-27-system-design.md:2587:    app = Application.objects.create(status='draft')
./docs/design/2026-05-27-system-design.md:2589:    assert app.status == 'pending_counselor'
./docs/design/2026-05-27-system-design.md:2592:def test_approval_workflow():
./docs/design/2026-05-27-system-design.md:2594:    assert result['status'] == 'pending_admin'
./docs/design/2026-05-27-system-design.md:2599:    assert response.status_code == 201  # 创建资源返回201
./docs/design/2026-05-27-system-design.md:2605:    assert response.status_code == 400
./docs/design/2026-05-27-system-design.md:2612:    assert response.status_code == 403
./docs/design/2026-05-27-system-design.md:2625:    success_count = sum(1 for r in results if r.status_code == 200)
./docs/design/2026-05-27-system-design.md:2649:    """测试学生无法审批"""
./docs/design/2026-05-27-system-design.md:2651:    response = client.post(f'/api/v1/approvals/{app_id}/approve')
./docs/design/2026-05-27-system-design.md:2652:    assert response.status_code == 403
./docs/design/2026-05-27-system-design.md:2659:    assert response.status_code == 429  # Too Many Requests
./docs/design/2026-05-27-system-design.md:2666:    assert response.status_code == 400
./docs/design/2026-05-27-system-design.md:2676:def test_approval_creates_audit_log():
./docs/design/2026-05-27-system-design.md:2677:    """测试审批操作记录审计日志"""
./docs/design/2026-05-27-system-design.md:2685:    app = Application.objects.create(status='draft')
./docs/design/2026-05-27-system-design.md:2695:- 完整审批流程测试
./docs/design/2026-05-27-system-design.md:2712:2. 辅导员审批流程
./docs/design/2026-05-27-system-design.md:2732:class GraduationLeaveUser(HttpUser):
./docs/design/2026-05-27-system-design.md:2745:        self.client.post("/api/v1/approvals/1/approve", json={"opinion": "同意", "version": 0})
./docs/design/2026-05-27-system-design.md:2779:- 业务指标：申请数量、审批时效
./docs/design/2026-05-27-system-design.md:2787:- 审批超时 > 10个
./backend/apps/applications/migrations/0001_initial.py:21:                ('leave_date', models.DateField()),
./backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
./backend/apps/applications/migrations/0001_initial.py:23:                ('dorm_checkout_status', models.CharField(choices=[('completed', '已清退'), ('pending', '清退中'), ('not_started', '未开始'), ('unknown', '状态未知')], default='not_started', max_length=20)),
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:16:如果“立即启动”指完全跳过环境、基线、执行者授权确认，评分降为 **5/10**。原因是当前仍有会污染 Day 2 结论的前提未确认，包括工作树基线、Docker/DB状态、测试基线、`seed_data --reset` 是否存在、以及 migration 是否能承载重复提交约束。
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:49:3. **数据重置边界：** `seed_data --reset` 可以清理哪些表，尤其是 `applications` 和 `approvals`。这是重复提交约束和可重复 smoke 的前提。
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:50:4. **基线记录方式：** 启动时必须记录 `git status --short`、最新 commit、Docker服务状态、migration状态、测试基线结果。
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:55:1. **测试文件具体命名。** 可以新建 `test_permissions.py` / `test_state_machine.py`，也可以扩展现有测试文件，关键是覆盖点和可重复运行。
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:68:   `git status --short` 显示 `.omc` 状态文件、讨论文档和若干未跟踪文件。启动前不必清理，但必须记录基线，并约定 Day 2 只修改后端实现、测试、migration、smoke和必要文档。
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:79:5. **High - 审批状态机仍缺事务和状态/步骤匹配保护。**
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:80:   approve/reject 已有 approver 和 pending 检查，但没有 `transaction.atomic()`、`select_for_update()`、application.status 与 approval.step 匹配校验，也没有防重复 dean approval 的唯一约束或查询保护。
./docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md:30:   - `urls.py` 使用 `from . import views` 时，新增路由必须写为 `views.list_approvals`。
./docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md:36:   - 排序 `created_at DESC, approval_id DESC` 可作为稳定排序。
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:5:**状态:** 修订中
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:65:- 我的方案: `{'error': 'Students cannot access approval lists'}`
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:77:        {'error': {'code': 'FORBIDDEN', 'message': '学生不能访问审批列表'}},
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:78:        status=status.HTTP_403_FORBIDDEN
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:88:- 我的方案: `path('', list_approvals, ...)`
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:89:- 正确写法: `path('', views.list_approvals, ...)`
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:111:- `approval_id` 是 `CharField primary_key`
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:112:- 支持 `order_by('-approval_id')`
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:121:**文件:** `backend/apps/approvals/pagination.py` (新建)
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:142:### 4.2 实现list_approvals视图
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:144:**文件:** `backend/apps/approvals/views.py`
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:150:from rest_framework import status
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:159:def list_approvals(request):
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:165:            {'error': {'code': 'FORBIDDEN', 'message': '学生不能访问审批列表'}},
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:166:            status=status.HTTP_403_FORBIDDEN
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:169:    # 辅导员: 只看自己的pending counselor审批
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:177:    # 学工部: 只看自己的pending dean审批
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:188:            status=status.HTTP_403_FORBIDDEN
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:192:    queryset = queryset.order_by('-created_at', '-approval_id')
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:208:**文件:** `backend/apps/approvals/urls.py`
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:215:    path('', views.list_approvals, name='list_approvals'),  # GET
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:216:    path('<str:approval_id>/approve/', views.approve_approval, name='approve_approval'),
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:217:    path('<str:approval_id>/reject/', views.reject_approval, name='reject_approval'),
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:225:### Step 2 (修订版): 实现GET /api/approvals/ (50min)
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:228:   - 新建 `backend/apps/approvals/pagination.py`
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:233:   - 在 `backend/apps/approvals/views.py` 添加 `list_approvals`
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:236:   - 排序: created_at DESC, approval_id DESC
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:240:   - 在 `backend/apps/approvals/urls.py` 添加 `path('', views.list_approvals, ...)`
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:257:4. ✓ URL路由使用 `views.list_approvals`
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:260:7. ✓ 辅导员/学工部只看自己pending审批
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:261:8. ✓ 排序: created_at DESC, approval_id DESC
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:5:**状态：** 待Codex审查
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:23:### 当前状态评估
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:32:- ⚠ 当前代码基线状态（Day 1验证后是否有变更）
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:34:- ⚠ 测试基线当前状态
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:35:- ⚠ 执行者准备状态
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:49:- 环境状态未确认
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:86:2. **环境状态需要确认**
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:91:3. **执行者准备状态需要确认**
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:103:**1. 环境状态确认（5分钟）**
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:112:git status
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:136:# 1. 检查git状态
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:137:git status
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:165:4. **状态机保护**（第三优先级，最复杂）
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:173:文档12说"优先覆盖跨辅导员403、重复审批409、重复提交409"，但没有说具体测试文件和测试方法。
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:178:- `backend/apps/approvals/tests/test_permissions.py`
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:182:- `backend/apps/approvals/tests/test_state_machine.py`
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:183:  - `test_duplicate_approval_conflict`
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:184:  - `test_status_step_mismatch_conflict`
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:189:如果65分钟内无法完成全部5个测试，至少要完成前3个（跨辅导员403、重复审批409、重复提交409）。
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:201:- ✓ 状态机保护代码已落地（至少有事务和pending检查）
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:267:### 风险3：环境状态不符合预期
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:271:- 数据库状态不一致
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:286:1. 环境状态确认（5分钟）
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:329:**提案状态：** 已完成，等待Codex审查  
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:29:**1. 修审批权限（最高优先级）- 30分钟**
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:30:- 位置：`backend/apps/approvals/views.py`
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:31:- 修复：校验`approval.approver_id == request.user.user_id`
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:32:- 测试：T002不能审批T001班级的申请
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:34:**2. 增加状态机/事务保护 - 1小时**
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:35:- 位置：`backend/apps/approvals/views.py`
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:36:- 修复：审批前校验application.status匹配approval.step
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:38:- 测试：重复审批返回409
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:52:- 内容：动态读取token、application_id、approval_id
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:86:- 状态机/事务保护涉及并发测试，1小时够吗？
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:94:1. 审批权限（安全漏洞）
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:95:2. 状态机保护（数据一致性）
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:107:**问题1：审批权限修复**
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:109:- 是否需要同时校验`class_id`？（辅导员只能审批自己班级）
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:110:- 学工部审批是否也需要权限校验？（当前硬编码D001）
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:112:**问题2：状态机保护**
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:113:- 只校验status匹配step够吗？
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:114:- 是否需要防止重复审批同一个approval？
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:115:- 事务范围是否正确？（application更新 + approval更新）
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:140:2. ✓ 缺少审批状态机保护
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:148:- 辅导员如何知道有哪些申请需要审批？
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:149:- 学工部如何知道有哪些申请需要审批？
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:180:**请求状态：** 待审查  
./docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:5:**状态：** 需要Codex裁决
./docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md:154:**请求状态：** 等待Codex裁决  
./docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:54:- seed数据支持两级审批
./docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:55:- 登录 → 提交 → 辅导员审批 → 院长审批 → 查询状态
./docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:110:- 跑通完整闭环（登录→提交→审批→查询）
./docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:127:- seed数据足以支持两级审批
./docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:129:- 辅导员能审批对应学生申请
./docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:130:- 院长能进行最终审批
./docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md:131:- 学生能查询最终状态
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:14:计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:26:| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:27:| 状态机/事务保护 | 1h | 2-3h | 需要原子更新application+approval，防重复创建Dean approval，并补并发/重复测试 |
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:29:| 列表接口 | 可选 | 1.5-2h | 可重复验收和真实审批入口都需要它 |
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:34:- 如果Day 2是硬4小时，只能定义为“P1止血版”：seed/mock、审批权限、状态机基础保护、重复提交约束、最小smoke骨架。不能宣称全部P1完成。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:44:2. **审批权限与状态机合并修。** 二者在同一个approve/reject事务里实现，不应分散修改。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:47:5. **smoke test。** 可以先写骨架，但最终应在核心接口稳定后完成，且最好使用列表接口发现待审批记录。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:54:### P1-1 审批权限
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:56:Claude方案“只校验`approval.approver_id == request.user.user_id`”是必要但不完整。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:59:- `approval.step`与`user.role`匹配。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:60:- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:61:- 对辅导员，额外校验申请班级当前仍映射给该辅导员：`ClassMapping(class_id=application.class_id, counselor=user, active=True)`。这能防止历史/篡改approval把错误辅导员写进去。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:62:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:65:### P1-2 状态机/事务保护
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:67:只校验`status`匹配`step`不够。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:71:- 先验证`approval.decision == pending`。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:72:- 再验证状态机：`counselor`只能处理`pending_counselor`；`dean`只能处理`pending_dean`。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:73:- approval更新、application状态更新、Dean approval创建必须在同一事务内完成。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:74:- counselor approve创建Dean approval前检查是否已经存在该application的Dean approval，避免并发重复创建。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:75:- 建议给`Approval`加约束：同一`application + step`最多一个approval，至少MVP阶段如此。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:106:- 从创建申请响应或列表接口动态提取`application_id`和`approval_id`。建议依赖`jq`，脚本启动时检查依赖；或使用Python解析JSON。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:108:- 验证正向链路：`2020002`提交后由`T002`审批，再由`D001`审批，最终状态`approved`。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:109:- 验证负向链路：`T001`不能审批`2020002`的approval；重复审批返回409；重复提交返回409；错误step/status返回409。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:110:- 每一步失败应打印HTTP状态、响应体和当前步骤名。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:124:列表接口不应是可选。没有它，审批人不知道有哪些申请需要处理，Day 2仍然依赖“学生提交响应里带出的approval_id”或查库，不能称为可重复验收。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:129:- 辅导员：只看自己负责班级，默认返回`pending_counselor`待办，可支持`?status=`。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:131:- 返回字段包含`application_id`、`student_id/name`、`class_id`、`status`、当前待办`approval_id`。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:142:6. **approve/reject重复逻辑风险。** 两个函数权限、状态机、事务应抽成共享处理路径，避免只修approve漏掉reject。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:158:- 核心Django测试通过，至少覆盖申请、审批、驳回、权限、重复提交。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:160:- smoke test覆盖至少三个负向场景：跨辅导员403、重复审批409、重复提交409。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:166:仅当列表接口或并发压力测试未完成，但有明确替代验证证据和Day 3首项任务时，允许进入“修复继续”状态；不允许进入扩展功能开发。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:171:- 跨辅导员审批仍可成功。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:172:- 重复审批可改变状态或创建重复Dean approval。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:185:5. **权限面扩大风险。** 只修审批动作、不修列表和详情查看，会留下同等级的数据泄露问题。
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:5:**状态：** 已达成共识
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:29:- 真正打破timebox的是：6小时后继续修，或把未达标状态包装成Conditional Go
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:45:- 权限、状态机、重复提交代码基本落地
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:56:- 跨辅导员审批仍可成功
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:57:- 重复审批仍能改变状态或重复创建dean approval
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:113:- application.status与approval.step匹配
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:114:- pending approval限制
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:115:- 防重复dean approval
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:119:- 跨辅导员审批返回403
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:120:- 重复审批返回409
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:126:- 优先覆盖跨辅导员403、重复审批409、重复提交409
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:127:- 如果时间允许补step/status mismatch和正向路径
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:132:docker exec backend python manage.py test apps.approvals.tests apps.applications.tests
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:148:- 记录真实命令、HTTP状态码、关键响应字段
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:154:# 期望：全部步骤通过，最终status=approved
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:190:4. 审批状态机保护覆盖approve/reject，且不会重复生成dean approval
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:266:- 跨辅导员审批、重复审批、重复提交漏洞仍存在
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:278:5. **Day 3只允许收尾明确项目。** 如果Day 2剩余的是核心权限、状态机、重复提交这些未闭合问题，Day 3是P0修复日，不是进入Week 3前的普通补充。
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:307:- 不要把未达标状态包装成Conditional Go
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:312:**共识状态：** 已达成  
./docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:19:2. `GET /api/approvals/` - List approvals
./docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:21:   - Counselor: own pending approvals only
./docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:22:   - Dean: own pending approvals only
./docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:25:1. Add list views to applications/views.py and approvals/views.py
./docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:29:5. Add filtering (status, date range)
./docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:41:2. Counselor attempts dean approval (403)
./docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:42:3. Dean attempts counselor approval (403)
./docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:43:4. Invalid approval_id (404)
./docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:53:- Verify counselor is assigned to student's class before creating approval
./docs/discussions/week3-day1-review-2026-05-30/16-codex-authorization-ruling.md:70:**裁决状态：** 已完成  
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:25:Claude合理地指出：如果存在状态机、数据模型、权限链路等架构级问题，1-2天可能无法修完。这是成立的。
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:38:Codex原文给了“登录 → 提交 → 审批 → 查询”的轮廓，但没有把边界写死。Claude指出这里可能形成“假闭环”，这个批评成立。
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:44:- 辅导员审批。
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:45:- 院长审批。
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:46:- 学生查询自己的申请状态。
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:48:- 审批状态转换必须落库并可查询。
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:51:- 宿舍清退状态使用MockDormCheckoutProvider固定返回。
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:108:   两级审批依赖学生、辅导员、院长、班级映射、申请记录。没有明确seed数据，闭环测试很容易卡在角色和外键上。
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:114:   发现状态机或模型关系错误时，不能自动进入修复阶段。应先判断是局部补丁、迁移调整，还是契约需要重开。
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:123:   Week 1-2代码未经运行，首次迁移可能暴露默认值、nullable、外键约束、枚举状态不一致等问题。这类问题应作为P0验证项。
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:158:- 跑通登录、提交、辅导员审批、院长审批、状态查询。
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:169:- 如果发现状态机、数据模型、契约冲突等架构级问题，不启用Day 3修补，改为暂停Week 3扩展开发并重做设计决策。
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:182:- seed数据足以支持两级审批。
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:184:- 辅导员能审批对应学生申请。
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:185:- 院长能进行最终审批。
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:186:- 学生能查询最终状态。
./backend/apps/applications/tests/test_p0_fixes.py:4:from apps.approvals.models import Approval, ApprovalDecision, ApprovalStep
./backend/apps/applications/tests/test_p0_fixes.py:38:            leave_date='2024-06-30',
./backend/apps/applications/tests/test_p0_fixes.py:39:            status=ApplicationStatus.REJECTED
./backend/apps/applications/tests/test_p0_fixes.py:49:            leave_date='2024-06-30',
./backend/apps/applications/tests/test_p0_fixes.py:50:            status=ApplicationStatus.PENDING_COUNSELOR
./backend/apps/applications/tests/test_p0_fixes.py:54:        self.assertEqual(app2.status, ApplicationStatus.PENDING_COUNSELOR)
./backend/apps/applications/tests/test_p0_fixes.py:64:            leave_date='2024-06-30',
./backend/apps/applications/tests/test_p0_fixes.py:65:            status=ApplicationStatus.PENDING_COUNSELOR
./backend/apps/applications/tests/test_p0_fixes.py:75:            leave_date='2024-06-30',
./backend/apps/applications/tests/test_p0_fixes.py:76:            status=ApplicationStatus.PENDING_COUNSELOR
./backend/apps/applications/tests/test_p0_fixes.py:98:        # Create applications with different approval states
./backend/apps/applications/tests/test_p0_fixes.py:105:            leave_date='2024-06-30',
./backend/apps/applications/tests/test_p0_fixes.py:106:            status=ApplicationStatus.PENDING_COUNSELOR
./backend/apps/applications/tests/test_p0_fixes.py:115:            leave_date='2024-06-30',
./backend/apps/applications/tests/test_p0_fixes.py:116:            status=ApplicationStatus.APPROVED
./backend/apps/applications/tests/test_p0_fixes.py:125:            leave_date='2024-06-30',
./backend/apps/applications/tests/test_p0_fixes.py:126:            status=ApplicationStatus.REJECTED
./backend/apps/applications/tests/test_p0_fixes.py:129:        # Create approvals
./backend/apps/applications/tests/test_p0_fixes.py:130:        self.approval_pending = Approval.objects.create(
./backend/apps/applications/tests/test_p0_fixes.py:131:            approval_id='apv_pending',
./backend/apps/applications/tests/test_p0_fixes.py:139:        self.approval_approved = Approval.objects.create(
./backend/apps/applications/tests/test_p0_fixes.py:140:            approval_id='apv_approved',
./backend/apps/applications/tests/test_p0_fixes.py:148:        self.approval_rejected = Approval.objects.create(
./backend/apps/applications/tests/test_p0_fixes.py:149:            approval_id='apv_rejected',
./backend/apps/applications/tests/test_p0_fixes.py:157:    def test_filter_pending_approvals(self):
./backend/apps/applications/tests/test_p0_fixes.py:158:        approvals = Approval.objects.filter(
./backend/apps/applications/tests/test_p0_fixes.py:162:        self.assertEqual(approvals.count(), 1)
./backend/apps/applications/tests/test_p0_fixes.py:163:        self.assertEqual(approvals.first().approval_id, 'apv_pending')
./backend/apps/applications/tests/test_p0_fixes.py:165:    def test_filter_approved_approvals(self):
./backend/apps/applications/tests/test_p0_fixes.py:166:        approvals = Approval.objects.filter(
./backend/apps/applications/tests/test_p0_fixes.py:170:        self.assertEqual(approvals.count(), 1)
./backend/apps/applications/tests/test_p0_fixes.py:171:        self.assertEqual(approvals.first().approval_id, 'apv_approved')
./backend/apps/applications/tests/test_p0_fixes.py:173:    def test_filter_rejected_approvals(self):
./backend/apps/applications/tests/test_p0_fixes.py:174:        approvals = Approval.objects.filter(
./backend/apps/applications/tests/test_p0_fixes.py:178:        self.assertEqual(approvals.count(), 1)
./backend/apps/applications/tests/test_p0_fixes.py:179:        self.assertEqual(approvals.first().approval_id, 'apv_rejected')
./backend/apps/applications/tests/test_p0_fixes.py:181:    def test_filter_all_approvals(self):
./backend/apps/applications/tests/test_p0_fixes.py:182:        approvals = Approval.objects.filter(approver=self.counselor)
./backend/apps/applications/tests/test_p0_fixes.py:183:        self.assertEqual(approvals.count(), 3)
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:26:- 忽略了这些数据是系统基础主数据，影响认证、权限、审批人分配
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:82:    def check_status(self, student_id: str) -> CheckoutStatus:
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:83:        """运行时查询宿舍清退状态"""
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:139:    def check_status(self, student_id: str) -> CheckoutResult:
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:257:    dorm_statuses = {
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:258:        "2020001": CheckoutStatus(status="completed", date="2024-06-15"),
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:259:        "2020002": CheckoutStatus(status="pending", date=None),
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:260:        "2020003": CheckoutStatus(status="not_started", date=None),
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:261:        "2020004": CheckoutStatus(status="unknown", date=None),  # API失败
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:264:    return students, counselors, dorm_statuses
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:279:| Week 3-6 | 申请、审批、附件、通知模块 | 核心业务功能 |
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:305:本地数据库 (认证、权限、审批的唯一运行时依据)
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:316:4. **本地数据库为准：** 认证、权限、审批以本地数据库为唯一依据
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:377:**状态：** 完全接受Codex建议，方案已修正
./backend/apps/applications/tests/test_error_cases.py:3:from rest_framework import status
./backend/apps/applications/tests/test_error_cases.py:4:from django.utils import timezone
./backend/apps/applications/tests/test_error_cases.py:72:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
./backend/apps/applications/tests/test_error_cases.py:74:        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
./backend/apps/applications/tests/test_error_cases.py:90:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
./backend/apps/applications/tests/test_error_cases.py:92:        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
./backend/apps/applications/tests/test_error_cases.py:97:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
./backend/apps/applications/tests/test_error_cases.py:99:        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
./backend/apps/applications/tests/test_error_cases.py:114:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
./backend/apps/applications/tests/test_error_cases.py:127:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
./backend/apps/applications/tests/test_error_cases.py:140:        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
./backend/apps/applications/tests/test_error_cases.py:154:            # Missing leave_date
./backend/apps/applications/tests/test_error_cases.py:156:        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:5:**状态：** 已达成共识
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:46:   - 辅导员审批
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:47:   - 院长审批
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:48:   - 学生查询状态
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:80:- 发现状态机、数据模型、契约冲突等架构级问题
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:93:2. **seed数据足以支持两级审批**
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:103:4. **辅导员能审批对应学生申请**
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:105:   - 审批操作成功，状态转换正确
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:107:5. **院长能进行最终审批**
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:108:   - 院长能看到所有待审批申请
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:109:   - 审批操作成功，状态转换正确
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:111:6. **学生能查询最终状态**
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:113:   - 状态显示正确（draft/pending/approved/rejected）
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:136:- 发现架构级阻塞（状态机设计错误、数据模型根本缺陷、契约冲突）
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:179:4. **架构级问题处置门槛**：发现状态机或模型错误时，先判断是局部补丁还是契约重开
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:182:7. **迁移兼容性**：首次迁移可能暴露nullable、外键约束、枚举状态不一致
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:214:**共识状态：已确认**  
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:215:**执行状态：待开始Day 0**
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:5:**状态：** 待Codex审查
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:44:2. 审批权限修复（30分钟）
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:45:3. 基础状态机保护（1小时）
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:62:2. 任务2-4（权限、状态机、约束）相互独立，但都依赖任务1
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:68:- 第二阶段：任务2、3、4（权限、状态机、约束）- 可以跳过阻塞项
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:98:- 任务2：curl测试跨辅导员审批，期望403
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:99:- 任务3：curl测试重复审批，期望409
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:140:- 0:30-1:00：任务2（审批权限）
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:141:- 1:00-2:00：任务3（状态机）
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:173:- MockDormCheckoutProvider.get_status('2020002')返回completed
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:175:### 阶段2：审批权限修复（30分钟）
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:177:**位置：** `backend/apps/approvals/views.py`
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:180:1. 添加`approval.approver_id == request.user.user_id`校验
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:187:# T002尝试审批T001的申请，期望403
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:188:curl -X POST http://localhost:8001/api/approvals/{T001的approval_id}/approve \
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:195:- 跨辅导员审批返回403
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:198:### 阶段3：基础状态机保护（1小时）
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:200:**位置：** `backend/apps/approvals/views.py`
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:205:3. 验证`approval.decision == pending`
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:206:4. 验证`application.status`匹配`approval.step`
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:207:5. 防止重复创建Dean approval（exists检查）
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:211:# 重复审批同一个approval，期望409
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:212:curl -X POST http://localhost:8001/api/approvals/{approval_id}/approve \
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:217:curl -X POST http://localhost:8001/api/approvals/{approval_id}/approve \
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:224:- 重复审批返回409
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:225:- 状态不匹配返回409
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:242:  -d '{"reason": "first", "leave_date": "2024-07-01"}'
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:247:  -d '{"reason": "second", "leave_date": "2024-07-01"}'
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:262:3. 动态提取token/application_id/approval_id
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:269:# 期望：全部步骤通过，最终status=approved
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:275:- 最终状态为approved
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:309:2. 根据角色自动过滤（学生看自己，辅导员看待审批，学工部看待审批）
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:316:# 期望：返回T002待审批的申请列表
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:323:2. 重复审批409
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:333:- ✓ 跨辅导员审批已修复（403）
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:334:- ✓ 重复审批已修复（409或事务保护）
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:365:### 风险2：状态机保护实现复杂
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:369:- 状态机验证逻辑复杂
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:373:- 再添加状态验证（30分钟）
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:430:**提案状态：** 已完成，等待Codex审查  
./docs/discussions/week3-direction-2026-05-30/01-claude-proposal.md:5:**当前状态：** Week 0-2代码完成，环境未搭建
./docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:5:**状态：** 待Codex审查
./docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:16:当前状态：等待用户授权确认。
./docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:44:- Migration状态不一致
./docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:57:- 6项修复内容（权限、状态机、重复约束等）
./docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:80:- 在授权确认后、T0开始前，先快速检查Docker/DB状态
./docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:92:- 确保最关键的3项（权限、状态机、重复约束）必须完成
./docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:166:**请求状态：** 等待Codex审查  
./docs/discussions/week3-direction-2026-05-30/03-claude-response.md:32:- Day 2上午：手动测试最小闭环（登录→提交→审批→查询）
./docs/discussions/week3-direction-2026-05-30/03-claude-response.md:36:- 如果发现**架构级问题**怎么办？（例如：状态机设计根本错误）
./docs/discussions/week3-direction-2026-05-30/03-claude-response.md:49:- 是否包括宿舍清退状态检查（MockDormCheckoutProvider）？
./docs/discussions/week3-direction-2026-05-30/03-claude-response.md:87:- 范围：登录 → 提交 → 辅导员审批 → 院长审批 → 查询状态
./docs/discussions/week3-direction-2026-05-30/03-claude-response.md:128:- **必须包括**：JWT认证、提交申请、两级审批、状态查询
./docs/discussions/week3-direction-2026-05-30/03-claude-response.md:130:- **可以简化**：宿舍清退状态检查（先用mock，返回固定值）
./docs/discussions/week3-direction-2026-05-30/03-claude-response.md:160:- 能稳定复现：登录 → 提交 → 审批 → 查询
./docs/discussions/week3-direction-2026-05-30/02-codex-review.md:31:- 跑通登录 → 提交 → 审批 → 查询 的最小闭环
./docs/discussions/week3-direction-2026-05-30/02-codex-review.md:38:- 修复逻辑问题（状态机转换、权限检查）
./docs/discussions/week3-direction-2026-05-30/02-codex-review.md:77:3. **最小闭环的具体范围？** 是否包括宿舍清退状态检查？
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:44:- 4小时：最小止血版（seed/mock + 审批权限 + 基础状态机）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:52:**接受"先修seed/mock"，质疑"合并修审批权限+状态机"。**
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:62:2. **"审批权限与状态机合并修"** - 不同意
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:65:   - 建议：先修审批权限（30分钟），验证通过后再修状态机（1小时）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:72:2. 审批权限修复（30分钟）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:73:3. 基础状态机保护（1小时）- 不包括并发测试
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:86:### P1-1 审批权限
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:91:- ✓ `approval.step`与`user.role`匹配
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:92:- ✓ `approval.approver_id == user.user_id`
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:100:- Day 1的问题是"任何辅导员都能审批任意approval"
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:102:- ClassMapping校验防御的是"历史/篡改approval"场景
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:103:- 这个场景在MVP阶段不会发生（没有修改approval的接口）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:111:if approval.approver_id != request.user.user_id:
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:121:### P1-2 状态机/事务保护
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:125:Codex建议的完整状态机保护：
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:128:- ✓ 验证`approval.decision == pending`
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:129:- ✓ 验证状态机匹配
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:130:- ✓ 防止重复创建Dean approval
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:147:- 验证decision和status
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:148:- 防止重复创建Dean approval（exists检查）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:195:- ✓ 动态提取application_id/approval_id
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:233:Codex正确指出：没有列表接口，审批人无法发现待审批申请。
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:291:- ✓ 跨辅导员审批已修复（403）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:292:- ✓ 重复审批已修复（409或事务保护）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:305:- 跨辅导员审批仍可成功
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:306:- 重复审批仍可改变状态
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:325:**2. 审批权限修复（30分钟）**
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:326:- 位置：`backend/apps/approvals/views.py`
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:327:- 修复：校验`approval.approver_id == request.user.user_id`
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:331:- 验证：T002不能审批T001的申请（403）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:333:**3. 基础状态机保护（1小时）**
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:334:- 位置：`backend/apps/approvals/views.py`
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:337:- 修复：验证`approval.decision == pending`
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:338:- 修复：验证`application.status`匹配`approval.step`
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:339:- 修复：防止重复创建Dean approval（exists检查）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:340:- 验证：重复审批返回409
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:354:- 实现：动态提取token/application_id/approval_id
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:377:- 实现：重复审批409
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:437:2. 审批权限修复（包括查看权限）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:438:3. 基础状态机保护（包括事务和锁）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:477:**响应状态：** 已完成，等待Codex回应  
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:5:**状态：** 已达成共识
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:29:- 核心漏洞是"任何辅导员都能审批任意approval"
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:32:- 当前没有approval修改接口，Day 2不该当阻塞项
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:67:**2. 审批权限修复（30分钟）**
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:68:- 位置：`backend/apps/approvals/views.py`
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:69:- 修复：校验`approval.approver_id == request.user.user_id`
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:73:- 验证：T002不能审批T001的申请（403）
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:75:**3. 基础状态机保护（1小时）**
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:76:- 位置：`backend/apps/approvals/views.py`
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:79:- 修复：验证`approval.decision == pending`
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:80:- 修复：验证`application.status`匹配`approval.step`
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:81:- 修复：防止重复创建Dean approval（exists检查）
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:82:- 验证：重复审批返回409
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:96:- 实现：动态提取token/application_id/approval_id
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:119:- 实现：重复审批409
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:141:- ✓ 跨辅导员审批已修复（403）
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:142:- ✓ 重复审批已修复（409或事务保护）
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:163:- ✗ 跨辅导员审批仍可成功
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:164:- ✗ 重复审批仍可改变状态
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:237:**共识状态：** 已达成  
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:17:2. 把未满足证据标准的状态包装成Conditional Go。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:46:- 状态机修复不牵出URL、serializer、fixture或事务问题。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:70:   - 权限、状态机、重复提交的代码修复已基本落地；
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:83:   - 跨辅导员审批仍可成功；
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:84:   - 重复审批仍能改变状态或重复创建dean approval；
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:97:- **会污染结论的问题**：`seed_data --reset`不清理applications/approvals、唯一约束migration因重复数据失败。这些不能简单归为遗留，因为会直接破坏重复验证，必须在Day 2处理或明确No-Go。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:105:原因很直接：Day 2修的是权限、状态机、唯一约束，这些是最容易被后续开发再次破坏的契约。如果没有自动化测试，Week 3继续开发时没有回归刹车。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:135:- 当前git diff/关键文件状态；
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:136:- migration状态；
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:145:权限、`get_application`、dynamic dean、approve/reject状态机、事务、重复dean防护、唯一约束、IntegrityError处理放在1.5小时内，只有在代码结构非常顺、migration无历史数据问题、测试暂不跟进时才可能完成。更现实是2小时左右。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:149:Claude列出的最小测试包括403、409、step/status mismatch、重复提交DB约束、正向路径。它们需要fixture、认证、申请创建、approval链路和状态准备。45分钟可能够写一个很薄的测试文件，但不够稳定调通这组测试。合理预算是60-90分钟；如果基线完全顺，60分钟有机会。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:153:登录、token解析、application_id/approval_id提取、HTTP状态码判断、reset/cleanup、错误输出，任何一个字段与文档不一致都会吃时间。45分钟能搭骨架，但不一定能形成可信证据。可接受的压缩方式是：如果Django测试已经覆盖正向路径，smoke只保留最薄的端到端脚本。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:199:- application.status与approval.step匹配。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:200:- pending approval限制。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:201:- 防重复dean approval。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:206:- 优先覆盖跨辅导员403、重复审批409、重复提交409。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:207:- 如果时间允许补step/status mismatch和正向路径。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:223:- 记录真实命令、HTTP状态码、关键响应字段。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:243:4. **Day 3只允许收尾明确项目。** 如果Day 2剩余的是核心权限、状态机、重复提交这些未闭合问题，Day 3是P0修复日，不是进入Week 3前的普通补充。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:268:- 不把证据不足的状态包装成Conditional Go。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:272:**响应状态：** Codex建议按上述折中方案更新Day 2执行计划。  
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:36:- `seed_data --reset`语义是否包含清理applications/approvals
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:52:Codex正确指出任务2-4（权限、状态机、重复提交）不应视为可随意跳过的独立项。
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:61:- 如果状态机保护卡住，是否可以先跳过，完成重复提交约束？
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:76:- 重复审批返回409
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:77:- application.status与approval.step不匹配返回409
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:98:- 状态机、唯一约束、smoke test、文档验证都需要更多时间
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:109:- 核心修复：3小时（seed/mock、权限、状态机、约束）
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:123:- 审批必须只允许pending approval且status匹配step
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:124:- 辅导员通过只能创建一个dean approval
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:170:1. **状态机保护1小时 → 1.5-2小时** - 部分接受，但可以分阶段：基础版本1小时，完整版本1.5小时
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:177:- 状态机保护：先做基础版本（1小时），完整版本Day 3
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:202:2. **审批权限修复** - 接受，重点转为reject复核、get_application权限、dynamic dean
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:203:3. **状态机保护** - 接受，必须覆盖approve和reject，校验step/status匹配
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:205:5. **Smoke test骨架** - 接受，支持BASE_URL环境变量，检查HTTP status
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:342:**响应状态：** 已完成，等待Codex回应  
./docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:51:- 审批状态机缺事务/锁
./docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:57:17号说确保权限、状态机、重复约束三项完成，但文档12的不可跳过项包括7项。
./docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:95:- 明确哪些步骤不可跳过（seed/reset、权限、状态机、重复提交约束、证据链、文档同步）
./docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:113:**审查状态：** 已完成  
./docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md:32:现在的核心漏洞是"任何辅导员都能审批任意approval"，先修`approver_id == user.user_id`就能堵住主洞。
./docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md:34:ClassMapping防的是更弱、更后置的场景，而且当前没有approval修改接口，Day 2不该把它当阻塞项。
./docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md:84:**回应状态：** 已完成  
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:25:- ⚠ 部分达标：4/8（Seed数据、学工部审批、负向权限、宿舍清退Mock）
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:26:- ✗ 未达标：1/8（辅导员审批对应学生）
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:30:2. 没有验证权限边界（任何辅导员都能审批任意审批单）
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:46:- 任何辅导员都能审批任意审批单
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:49:**2. 缺少审批状态机保护**
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:51:- 重复审批、并发审批都有风险
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:64:**7. 缺少列表接口**：辅导员/学工部看不到待审批列表
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:115:**1. 修审批权限（最高优先级）**
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:116:- 位置：`backend/apps/approvals/views.py`
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:117:- 修复：校验`approval.approver_id == request.user.user_id`
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:118:- 测试：T002不能审批T001班级的申请
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:120:**2. 增加状态机/事务保护**
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:121:- 位置：`backend/apps/approvals/views.py`
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:122:- 修复：审批前校验application.status匹配approval.step
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:124:- 测试：重复审批返回409
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:138:- 内容：动态读取token、application_id、approval_id
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:180:1. 修审批权限：30分钟
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:181:2. 状态机/事务保护：1小时
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:199:**当前状态：**
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:223:- 建议：Day 2如果再次遇到，记录详细错误信息和网络状态
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:240:**响应状态：** 已完成  
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:19:- `2020001 -> T001 -> D001` 这一条链路在当前数据库状态下成功
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:27:| 标准 | 状态 | 说明 |
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:32:| 4. 辅导员审批对应学生 | ✗ 未达标 | 只校验角色，不校验approver_id |
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:33:| 5. 学工部最终审批 | ⚠ 部分达标 | 主路径达标，但缺列表接口，dean硬编码 |
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:34:| 6. 学生查询最终状态 | ✓ 达标 | 主路径达标 |
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:45:**位置：** `backend/apps/approvals/views.py:22`  
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:46:**问题：** 只按role放行，不按`approval.approver_id == request.user.user_id`校验  
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:47:**影响：** 任何辅导员都能审批任意辅导员审批单
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:49:### 2. 缺少审批状态机保护
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:50:**位置：** `backend/apps/approvals/views.py`  
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:51:**问题：** 审批时未校验application当前状态是否匹配approval step，且没有事务/锁  
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:52:**影响：** 重复或并发审批有风险
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:72:**问题：** "辅导员能看到自己班级申请""学工部能看到全部待审批申请"没有列表接口  
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:103:**判断：** 需要记录具体错误、容器网络状态和复现条件
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:114:2. **修审批权限**：必须校验审批人就是当前用户；补T002不能审批T001班级的负向测试
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:115:3. **增加状态机/事务保护**：审批必须匹配当前application status，重复审批返回409
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:117:5. **写真实smoke脚本**：动态读取`access_token`、`application_id`、`approval_id`，不要写死`1/2`
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:132:**审查状态：** 已完成  
./docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md:33:**正确形式：** 停止方案讨论，只保留一个阻塞状态和一个明确授权提示。
./docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md:37:"停止讨论、记录僵局状态"不是放弃任务，而是正确的流程收束。
./docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md:45:不是"再讨论一个二选一提示"，而是直接发最终确认，并规定只有明确回复才改变状态。
./docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md:65:**裁决状态：** 已完成  
./docs/discussions/week3-day1-review-2026-05-30/19-claude-deadlock-analysis.md:5:**状态：** 待Codex审查
./docs/discussions/week3-day1-review-2026-05-30/19-claude-deadlock-analysis.md:77:### 方案C：停止讨论，停止等待，记录僵局状态
./docs/discussions/week3-day1-review-2026-05-30/19-claude-deadlock-analysis.md:120:**请求状态：** 等待Codex裁决  
./backend/apps/applications/models.py:8:    PENDING_COUNSELOR = 'pending_counselor', '待辅导员审批'
./backend/apps/applications/models.py:9:    PENDING_DEAN = 'pending_dean', '待学工部审批'
./backend/apps/applications/models.py:18:    UNKNOWN = 'unknown', '状态未知'
./backend/apps/applications/models.py:27:    leave_date = models.DateField()
./backend/apps/applications/models.py:28:    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.DRAFT)
./backend/apps/applications/models.py:29:    dorm_checkout_status = models.CharField(max_length=20, choices=DormCheckoutStatus.choices, default=DormCheckoutStatus.NOT_STARTED)
./backend/apps/applications/models.py:37:        if self.status in [ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.PENDING_DEAN, ApplicationStatus.APPROVED]:
./backend/apps/applications/models.py:40:                status__in=[ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.PENDING_DEAN, ApplicationStatus.APPROVED]
./backend/apps/applications/models.py:43:                raise ValidationError('该学生已有待审批或已通过的申请，不能重复提交')
./backend/apps/applications/tests/test_constraints.py:3:from rest_framework import status
./backend/apps/applications/tests/test_constraints.py:4:from django.utils import timezone
./backend/apps/applications/tests/test_constraints.py:51:                'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
./backend/apps/applications/tests/test_constraints.py:55:        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
./backend/apps/applications/tests/test_constraints.py:62:                'leave_date': (timezone.now().date() + timedelta(days=2)).isoformat()
./backend/apps/applications/tests/test_constraints.py:66:        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
./backend/apps/applications/views.py:1:from rest_framework import status
./backend/apps/applications/views.py:5:from django.utils import timezone
./backend/apps/applications/views.py:10:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
./backend/apps/applications/views.py:32:    # Counselor: applications with own pending counselor approvals
./backend/apps/applications/views.py:34:        pending_approvals = Approval.objects.filter(
./backend/apps/applications/views.py:39:        queryset = Application.objects.filter(pk__in=pending_approvals)
./backend/apps/applications/views.py:41:    # Dean: applications with own pending dean approvals
./backend/apps/applications/views.py:43:        pending_approvals = Approval.objects.filter(
./backend/apps/applications/views.py:48:        queryset = Application.objects.filter(pk__in=pending_approvals)
./backend/apps/applications/views.py:53:            status=status.HTTP_403_FORBIDDEN
./backend/apps/applications/views.py:57:    status_param = request.query_params.get('status')
./backend/apps/applications/views.py:58:    if status_param:
./backend/apps/applications/views.py:59:        queryset = queryset.filter(status=status_param)
./backend/apps/applications/views.py:79:                        status=status.HTTP_403_FORBIDDEN)
./backend/apps/applications/views.py:84:        status__in=[ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.PENDING_DEAN, ApplicationStatus.APPROVED]
./backend/apps/applications/views.py:87:        return Response({'error': {'code': 'CONFLICT', 'message': '已有待审批或已通过的申请，不能重复提交',
./backend/apps/applications/views.py:88:                                    'details': {'student_id': user.user_id, 'existing_application_id': existing.application_id, 'status': existing.status}}},
./backend/apps/applications/views.py:89:                        status=status.HTTP_409_CONFLICT)
./backend/apps/applications/views.py:95:                        status=status.HTTP_400_BAD_REQUEST)
./backend/apps/applications/views.py:98:    dorm_status = provider.check_status(user.user_id)
./backend/apps/applications/views.py:100:    if dorm_status.status != DormCheckoutStatus.COMPLETED:
./backend/apps/applications/views.py:102:                                    'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
./backend/apps/applications/views.py:103:                                                'blocking_reason': dorm_status.blocking_reason}}},
./backend/apps/applications/views.py:104:                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
./backend/apps/applications/views.py:111:                        status=status.HTTP_404_NOT_FOUND)
./backend/apps/applications/views.py:119:        leave_date=serializer.validated_data['leave_date'],
./backend/apps/applications/views.py:120:        status=ApplicationStatus.PENDING_COUNSELOR,
./backend/apps/applications/views.py:121:        dorm_checkout_status=dorm_status.status
./backend/apps/applications/views.py:125:        approval_id=f'apv_{uuid.uuid4().hex[:8]}',
./backend/apps/applications/views.py:133:    return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
./backend/apps/applications/views.py:144:                        status=status.HTTP_404_NOT_FOUND)
./backend/apps/applications/views.py:151:                        status=status.HTTP_403_FORBIDDEN)
./backend/apps/applications/views.py:159:                            status=status.HTTP_403_FORBIDDEN)
./backend/apps/applications/views.py:161:    # Dean: can only view applications with own pending dean approvals
./backend/apps/applications/views.py:163:        has_pending_approval = Approval.objects.filter(
./backend/apps/applications/views.py:169:        if not has_pending_approval:
./backend/apps/applications/views.py:171:                            status=status.HTTP_403_FORBIDDEN)
./backend/apps/applications/serializers.py:6:    """Lean serializer for application lists - no nested approvals"""
./backend/apps/applications/serializers.py:12:                  'reason', 'leave_date', 'status', 'created_at', 'updated_at']
./backend/apps/applications/serializers.py:14:                            'class_id', 'status', 'created_at', 'updated_at']
./backend/apps/applications/serializers.py:19:    approvals = serializers.SerializerMethodField()
./backend/apps/applications/serializers.py:24:                  'reason', 'leave_date', 'status', 'dorm_checkout_status',
./backend/apps/applications/serializers.py:25:                  'approvals', 'created_at', 'updated_at']
./backend/apps/applications/serializers.py:27:                            'class_id', 'status', 'dorm_checkout_status',
./backend/apps/applications/serializers.py:30:    def get_approvals(self, obj):
./backend/apps/applications/serializers.py:31:        from apps.approvals.serializers import ApprovalSerializer
./backend/apps/applications/serializers.py:32:        return ApprovalSerializer(obj.approvals.all(), many=True).data
./backend/apps/applications/serializers.py:37:    leave_date = serializers.DateField()
./backend/apps/applications/serializers.py:44:    def validate_leave_date(self, value):
./backend/apps/applications/serializers.py:45:        from django.utils import timezone
./backend/apps/applications/serializers.py:46:        today = timezone.now().date()
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:35:- 状态枚举
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:57:- 辅导员审批API
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:58:- 学工部审批API
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:59:- 状态查询API
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:70:- 复杂审批流
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:82:6. 状态枚举和错误码稳定
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:97:- 核心流程（申请、审批、状态查询）
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:115:| **Week 0** (1-2工作日) | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog | 前端可用mock跑通登录→提交→审批→查询流程 |
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:116:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:119:| **Week 4-6** | 微信小程序并行开发 | 登录、申请、审批、查询主流程 | 小程序可用mock跑通完整流程，逐步联调真实后端 |
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:136:**验收标准：** 前端可用mock跑通登录→提交→审批→查询流程
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:160:**原方案A：** 认证→申请→审批→附件→通知→前端→联调
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:192:**Claude错误建议：** Week 1"审批API无权限校验"
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:196:**原因：** 纵向切片的价值是验证角色、数据、状态机和审批链路能否串起来
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:209:- Day 3结束仍无申请提交API → 只保留"学生提交→辅导员审批→查询"
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:210:- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:217:- 如果v0.2契约仍没有确定状态枚举、角色和核心路径，先用1-2天补契约
./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:262:**状态：** 已批准，进入执行阶段  
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:17:- 当前代码基线与提案一致。现有代码里 `approval.approver_id` 校验和 `approval.decision != pending` 已经存在，但事务、锁、动态 dean、数据库唯一约束仍缺失。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:20:- `seed_data --reset` 的语义是否包含清理 applications/approvals；否则加了"一人一申请"约束后 smoke test 不能重复跑。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:22:缺少这一步会让 Day 2 中途才发现测试基线或数据状态不可用，反而更浪费 timebox。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:30:2. 权限、状态机、重复提交应作为一个一致性修复组推进，代码可以串行改，但验证要合并成一组回归。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:42:- 重复审批返回 409，且不会重复创建 dean approval。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:43:- application.status 与 approval.step 不匹配时返回 409。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:57:- 状态机事务/锁/重复 dean 防护：90-120分钟。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:72:- 审批必须只允许 pending approval 且 application.status 匹配 step。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:73:- 辅导员通过只能创建一个 dean approval。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:98:2. **reset语义风险。** `seed_data` 当前使用 `get_or_create`，不会更新既有用户的 `class_id`；即使改成 `update_or_create`，也不一定清理 applications/approvals。重复 smoke 会被唯一约束挡住。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:100:4. **事务验证风险。** `select_for_update()` 需要在真实数据库事务中验证；如果只用普通 curl 串行验证，无法证明并发下不会重复创建 dean approval。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:101:5. **端点与文档漂移风险。** 提案里的部分 curl 缺少尾斜杠，但当前 URL 是 `/api/applications/` 和 `/api/approvals/<id>/approve/`。文档还需同步 `app_...`/`apv_...` 这类实际ID格式，而不是简单写"UUID"。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:109:- **状态机保护 1小时偏乐观。** 事务、锁、状态匹配、重复 dean 防护、approve/reject 两条路径和测试至少需要 1.5-2小时。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:111:- **Smoke test 1小时偏乐观。** 登录、动态ID提取、状态码断言、reset/cleanup、错误输出处理通常超过1小时。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:122:- 阶段3：审批状态机保护覆盖 approve/reject，且不会重复生成 dean approval。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:138:1. **Seed/mock修复：** 内容不完整。需要把 `--reset` 明确为 idempotent，并决定是否清理 applications/approvals；否则 smoke test 不能重复跑。Provider 方法名实际是 `check_status`，不是 `get_status`。模板路径不只 `docs/templates/`，还包括 `backend/data/templates/`。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:139:2. **审批权限修复：** 方向正确，但现有代码已部分实现 assigned approver 检查；剩余重点应转为 reject 复核、`get_application` 角色权限、dynamic dean 和测试。`get_application` 现在只限制学生，counselor/dean 仍可看任意申请。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:140:3. **状态机保护：** 必须覆盖 approve 和 reject。只校验重复审批不够，还要校验 step/status 匹配，例如 dean approval 不能在 `pending_counselor` 状态下被操作。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:142:5. **Smoke test骨架：** 建议支持 `BASE_URL` 环境变量，不要只硬编码；脚本必须检查 HTTP status，并在开头执行 reset/cleanup。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:151:- 状态机风险不只是语法不熟，而是事务边界、锁顺序、状态匹配和重复 dean 创建需要一起成立。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:152:- Smoke test 风险不只是 jq 调试，而是环境启动、数据复位、HTTP状态码断言和契约漂移。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:162:1. **0:00-0:30 前置校验：** git diff、migration状态、现有测试、Docker/API可用性、seed可执行。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:164:3. **1:15-3:15 核心一致性修复：** 权限、状态机、动态 dean、唯一约束、事务。
./backend/apps/applications/tests/test_list_permissions.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
./backend/apps/applications/tests/test_list_permissions.py:45:            leave_date='2024-07-01',
./backend/apps/applications/tests/test_list_permissions.py:46:            status=ApplicationStatus.PENDING_COUNSELOR
./backend/apps/applications/tests/test_list_permissions.py:55:            leave_date='2024-07-01',
./backend/apps/applications/tests/test_list_permissions.py:56:            status=ApplicationStatus.PENDING_DEAN
./backend/apps/applications/tests/test_list_permissions.py:59:        # Create approvals
./backend/apps/applications/tests/test_list_permissions.py:61:            approval_id='apv_001',
./backend/apps/applications/tests/test_list_permissions.py:70:            approval_id='apv_002',
./backend/apps/applications/tests/test_list_permissions.py:81:        self.assertEqual(response.status_code, 200)
./backend/apps/applications/tests/test_list_permissions.py:91:    def test_counselor_sees_only_pending_counselor_approvals(self):
./backend/apps/applications/tests/test_list_permissions.py:94:        self.assertEqual(response.status_code, 200)
./backend/apps/applications/tests/test_list_permissions.py:103:    def test_dean_sees_only_pending_dean_approvals(self):
./backend/apps/applications/tests/test_list_permissions.py:106:        self.assertEqual(response.status_code, 200)
./backend/apps/applications/tests/test_list_permissions.py:110:    def test_response_format_no_nested_approvals(self):
./backend/apps/applications/tests/test_list_permissions.py:115:        self.assertNotIn('approvals', response.data['results'][0])
./backend/apps/applications/tests/test_application_flow.py:3:from rest_framework import status
./backend/apps/applications/tests/test_application_flow.py:4:from django.utils import timezone
./backend/apps/applications/tests/test_application_flow.py:9:from apps.approvals.models import Approval, ApprovalDecision
./backend/apps/applications/tests/test_application_flow.py:50:        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
./backend/apps/applications/tests/test_application_flow.py:57:        self.assertEqual(response.status_code, status.HTTP_200_OK)
./backend/apps/applications/tests/test_application_flow.py:64:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
./backend/apps/applications/tests/test_application_flow.py:66:        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
./backend/apps/applications/tests/test_application_flow.py:67:        self.assertEqual(response.data['status'], ApplicationStatus.PENDING_COUNSELOR)
./backend/apps/applications/tests/test_application_flow.py:77:        # Step 4: 辅导员审批通过
./backend/apps/applications/tests/test_application_flow.py:79:        counselor_approval = application.approvals.filter(step='counselor').first()
./backend/apps/applications/tests/test_application_flow.py:82:        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/approve/', {
./backend/apps/applications/tests/test_application_flow.py:85:        self.assertEqual(response.status_code, status.HTTP_200_OK)
./backend/apps/applications/tests/test_application_flow.py:95:        # Step 6: 学工部审批通过
./backend/apps/applications/tests/test_application_flow.py:97:        self.assertEqual(application.status, ApplicationStatus.PENDING_DEAN)
./backend/apps/applications/tests/test_application_flow.py:98:        dean_approval = application.approvals.filter(step='dean').first()
./backend/apps/applications/tests/test_application_flow.py:101:        response = self.client.post(f'/api/approvals/{dean_approval.approval_id}/approve/', {
./backend/apps/applications/tests/test_application_flow.py:104:        self.assertEqual(response.status_code, status.HTTP_200_OK)
./backend/apps/applications/tests/test_application_flow.py:106:        # Step 7: 查询申请状态
./backend/apps/applications/tests/test_application_flow.py:108:        self.assertEqual(application.status, ApplicationStatus.APPROVED)
./backend/apps/applications/tests/test_application_flow.py:112:        self.assertEqual(response.status_code, status.HTTP_200_OK)
./backend/apps/applications/tests/test_application_flow.py:113:        self.assertEqual(response.data['status'], ApplicationStatus.APPROVED)
./backend/apps/applications/tests/test_application_flow.py:114:        self.assertEqual(len(response.data['approvals']), 2)
./docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:31:  4. POST /api/approvals/{id}/approve
./docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:32:  5. POST /api/approvals/{id}/reject
./docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:34:**理由：** 列表端点不是最小纵向切片必需的，核心流程是"登录→提交→审批→查询单个申请"。
./docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:85:  - 新：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
./backend/apps/applications/tests/test_serializer_validation.py:2:from django.utils import timezone
./backend/apps/applications/tests/test_serializer_validation.py:12:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
./backend/apps/applications/tests/test_serializer_validation.py:22:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
./backend/apps/applications/tests/test_serializer_validation.py:28:    def test_leave_date_past(self):
./backend/apps/applications/tests/test_serializer_validation.py:29:        """Test leave_date field rejects dates before today"""
./backend/apps/applications/tests/test_serializer_validation.py:32:            'leave_date': (timezone.now().date() - timedelta(days=1)).isoformat()
./backend/apps/applications/tests/test_serializer_validation.py:36:        self.assertIn('leave_date', serializer.errors)
./backend/apps/applications/tests/test_serializer_validation.py:38:    def test_leave_date_today(self):
./backend/apps/applications/tests/test_serializer_validation.py:39:        """Test leave_date field accepts today"""
./backend/apps/applications/tests/test_serializer_validation.py:42:            'leave_date': timezone.now().date().isoformat()
./backend/apps/applications/tests/test_serializer_validation.py:51:            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:29:原方案A确实是"认证→申请→审批→附件→通知→前端→联调"的横向模块堆叠，风险在Week 8-10才暴露。
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:67:- 宿舍API各种错误状态
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:106:> Week 1应交付可运行骨架、契约测试、seed数据、最小审批流，而不是只交文档和接口。
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:117:- 最小申请审批闭环
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:127:5. **最小申请审批闭环**：2-3天（Application模型、Approval模型、状态机、3个API）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:138:- Week 1目标：可运行的最小申请审批流（不含附件、通知）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:142:  - 申请提交API + 审批API（简化版，无权限校验）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:143:  - 状态查询API
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:144:  - Dorm Mock（返回固定状态）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:169:3. 核心流程后端API已实现（申请、审批、状态查询）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:178:- Week 2：后端核心API完成（申请、审批、状态查询）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:198:- 最小申请审批闭环
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:216:- Day 3-4：最小申请审批流
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:220:  - 审批API（简化版）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:221:  - 状态查询API
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:224:  - 端到端测试（登录→提交→审批→查询）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:253:- 核心流程（申请、审批、状态查询）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:284:- **选项A（最小）：** 只包含申请审批流需要的字段（student_id, name, application_id, status, approver_id）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:295:- [ ] 可以用Postman调用5个API（登录、提交、审批、查询、Mock宿舍）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:296:- [ ] 端到端测试通过（登录→提交→审批→查询）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:329:- Week 1（5天）：纵向切片（后端骨架 + 薄认证 + 最小审批流）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:341:**讨论状态：** 第一轮回应，待Codex第二轮
./docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:14:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
./docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:39:| HTTP状态 | 错误码 | 样例位置 | 结论 |
./docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:71:如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
./docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:77:2. 砍范围明确：砍学工部审批。
./docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:78:3. Day 4目标明确：集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环。
./docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:79:4. 顺延范围明确：学工部审批推到Week 2 Day 1。
./docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:10:## 一、当前状态
./docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:28:本地数据库 (认证、权限、审批的唯一运行时依据)
./docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:98:- 数据契约影响认证、审批、前端所有模块
./docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:103:- 当前计划是按模块顺序开发（认证→申请→审批→...）
./docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:105:- 例如：简化版申请+审批+通知，验证整体架构
./docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:126:- 但申请提交（Week 3）就需要校验宿舍清退状态
./docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:157:- 当前：认证→申请→审批→附件→通知→集成→前端
./docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:158:- 是否应该：申请+审批核心流程→认证→附件→通知→集成→前端？
./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:28:      "field": "leave_date",
./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:82:**问题：** 风险2降级方案说"砍学工部审批，Day 4补学工部审批"，逻辑矛盾
./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:88:降级方案：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:93:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:96:**验证：** 降级方案现在明确：Day 3触发后砍学工部审批，Day 4验证辅导员闭环，学工部推Week 2 Day 1
./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:141:**状态：** 等待Codex确认
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:30:`RealUserDataProvider` 不应成为认证、审批、班级映射的运行时依赖。用户、辅导员、班级映射是本系统的基础主数据，影响登录、权限、审批人分配和历史追溯。
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:48:2. Provider只用于宿舍清退状态的实时查询
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:73:- **用户主数据API（如果坚持）：** 2-4周（牵涉数据模型、导入/同步策略、账号状态、审批人映射和验收演练）
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:148:- 宿舍状态：`completed/pending/not_started/unknown`
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:167:Provider 契约、DTO、种子数据、导入接口应在 Week 1-2 完成，否则认证、审批、前端都会先绑定临时模型，后续返工。
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:177:| Week 3-6 | 申请、审批、附件、通知 | 核心业务模块 |
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:226:│  作为认证、权限、审批和历史记录的唯一运行时依据 │
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:229:│  - approvals表                              │
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:244:4. **本地数据库：** 作为认证、权限、审批和历史记录的唯一运行时依据
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:255:### 宿舍清退状态缓存
./docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:20:2. **P1-2：降级方案逻辑矛盾** - 风险2说"砍学工部审批"又说"Day 4补学工部审批"
./docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:46:降级方案：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
./docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:51:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:33:- 状态枚举（draft/pending_counselor/pending_dean/approved/rejected）
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:57:- 辅导员审批API
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:58:- 学工部审批API
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:59:- 状态查询API
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:70:- 复杂审批流（转办、撤回、驳回重提）
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:72:**我的错误：** 建议Week 1"无权限校验"是错误的。Codex正确指出：纵向切片的价值正是验证角色、数据、状态机和审批链路能否串起来。
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:82:4. 核心后端API可跑通（登录、提交、审批、查询）
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:84:6. 状态枚举和错误码稳定
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:116:| **Week 0** (1-2工作日) | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog | 前端可用mock跑通登录→提交→审批→查询流程 |
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:117:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:120:| **Week 4-6** | 微信小程序并行开发 | 登录、申请、审批、查询主流程 | 小程序可用mock跑通完整流程，逐步联调真实后端 |
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:144:## 2. 状态枚举
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:159:### 4.3 审批
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:180:**验收标准：** 前端可用mock跑通登录→提交→审批→查询流程
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:194:- [ ] 定义状态枚举
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:214:- [ ] 辅导员审批API
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:215:- [ ] 学工部审批API
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:216:- [ ] 状态查询API
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:227:- Day 3结束仍无申请提交API → 只保留"学生提交→辅导员审批→查询"
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:228:- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:242:2. ✓ v0.1包含OpenAPI/DTO、状态枚举、错误码、样例、mock、changelog
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:310:**讨论状态：** 达成共识，进入执行阶段
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:18:3. Week 1建议"审批API无权限校验"，会让纵向切片失去验证审批链路的意义。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:23:**采用Week 0-1拆分，但Week 0必须是1-2个工作日的timebox；v0.1应现在冻结最小可执行契约，不等到Week 1前半；Week 1只承诺后端端到端最小闭环；前端Week 4启动不要求后端完全稳定，只要求契约、mock和核心路径达到可消费状态。**
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:43:如果拖到Week 1前半才冻结，Week 1后半只剩2-3天，很难完成后端骨架、认证、申请、审批、状态查询和集成测试。Claude把这个拆法描述成"Week 1前半冻结，Week 1后半纵向切片"，本质上还是把Week 1压缩成半周开发，风险比Codex原建议更高。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:49:- 选项A过小：只有`student_id, name, application_id, status, approver_id`无法支撑班级映射、角色判断、审批层级、宿舍清退校验和错误处理。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:58:| 申请 | application_id、student_id、reason、leave_date或checkout_intent、status、created_at | 完整表单扩展字段 |
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:59:| 审批 | step、approver_id、decision、comment、decided_at | 会签、转办、复杂委托 |
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:60:| 宿舍清退 | provider_status、checked_at、blocking_reason、provider_error_code | 真实接口全部响应字段 |
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:72:- 前端负责人 reviews 契约可消费性：字段命名、状态展示、错误展示、登录态。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:73:- 用户或业务方只确认业务假设：角色、审批链路、宿舍清退是否阻断提交。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:96:- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:98:- 辅导员审批API
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:99:- 学工部审批API
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:100:- 状态查询API
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:102:- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:104:这里需要反驳Claude的一点：**"审批API简化版，无权限校验"不应该进入Week 1目标。** 纵向切片的价值正是验证角色、数据、状态机和审批链路能否串起来。可以不做完整RBAC、组织树和复杂权限，但最小角色校验不能砍，否则Week 1只能证明CRUD能跑，不能证明毕业离校审批流程能跑。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:116:- 审批转办、撤回、驳回后重提等复杂流
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:125:- 确认审批链路和状态枚举
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:138:- 两级审批
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:139:- 状态查询
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:149:如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:167:3. 前端mock server或mock JSON可用，覆盖登录、提交、审批、查询、错误态。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:168:4. 核心后端API在开发环境可跑通：登录、提交、审批、查询。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:170:6. 状态枚举和错误码稳定，前端能做状态页和错误提示。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:189:- 如果登录、提交、审批、查询四个核心端点还没有可运行实现，前端仍可做一周mock驱动开发，但Week 5必须切到真实开发环境联调。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:190:- 如果v0.2契约仍没有确定状态枚举、角色和核心路径，则不能启动页面开发，应先用1-2天补契约，否则前端会做成静态原型。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:215:Claude的Week 0列了StudentDTO、ApplicationDTO、ApprovalDTO，但缺少错误码、状态机、样例请求响应、mock、契约测试和变更规则。前端和测试真正依赖的是这些可执行产物，不只是字段名。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:219:最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:241:| Week 0 / 1-2工作日 | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog |
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:242:| Week 1 | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 |
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:245:| Week 4-6 | 微信小程序并行开发 | 登录、申请、审批、查询主流程，使用mock并逐步联调真实后端 |
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:261:   v0.2可消费契约、mock可用、核心API可跑、认证策略固定为演示期薄认证、状态枚举/错误码稳定、API owner和变更机制明确。不要求附件、通知、真实OAuth、真实宿舍API完成。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:274:1. `contract-v0.1.md`或OpenAPI草案：字段、状态、错误码、样例、mock、changelog。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:283:**讨论状态：** 第二轮回应，建议进入Week 0-1执行共识
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:14:**项目状态：**
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:23:- 该API字段不满足需求（缺少班级、院系、专业、宿舍清退状态等）
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:26:1. 完整的API文档（学生信息、辅导员信息、宿舍清退状态）
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:45:- Phase 4: 审批管理模块
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:80:    """宿舍清退状态提供者接口"""
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:82:    def check_status(self, student_id: str) -> CheckoutStatus:
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:83:        """查询学生宿舍清退状态"""
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:87:    def batch_check_status(self, student_ids: List[str]) -> Dict[str, CheckoutStatus]:
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:88:        """批量查询清退状态"""
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:120:    def check_status(self, student_id: str):
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:199:| Week 3-6 | 核心业务逻辑 | 申请、审批、附件、通知模块 |
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:298:- Redis缓存TTL设置（用户信息1小时、清退状态10分钟）是否合适？
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:394:- **项目名称：** 毕业生离校申请审批系统
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:398:- **当前状态：** 设计完成，准备实施
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:403:- Round 2: API、审批、部署、安全、性能（29个问题修复）
./docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:59:- 风险2降级方案：改为"保留提交→辅导员审批→查询闭环，砍学工部审批"
./docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:92:**状态：** 等待Codex审查确认
./docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:15:它比旧计划好，但仍然是"先后端模块、后前端、最后联调"的瀑布排期。最大风险不是数据契约，而是到Week 8-10才发现端到端流程、微信小程序、附件、审批权限、宿舍降级和通知串不起来。
./docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:29:- 2-3人2周做两个端、附件、审批、认证、联调，偏乐观
./docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:56:更好的做法是先做`seed/import minimal path`，让认证和审批用同一套落库数据跑起来，再完善CSV校验、staging、审计。
./docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:82:先做"学生登录/伪登录 → 提交申请 → 辅导员审批 → 学工部审批 → 状态可查"的端到端最小流程。
./docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:124:Week 1应交付可运行骨架、契约测试、seed数据、最小审批流，而不是只交文档和接口。
./docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:138:不要"认证完整后再申请、申请完整后再审批"。改成薄认证 + 申请审批核心流优先，通知/附件/完整微信登录后补。
./docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:151:- 最小申请审批闭环（提交→辅导员审批→学工部审批→状态查询）
./docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:162:- 申请/审批权限细化
./docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:164:- 状态机和审计补齐
./docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:254:**讨论状态：** 第一轮，待Claude回应
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:17:3. 宿舍清退状态通过API实时查询（可缓存、可降级）
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:18:4. 本地数据库是认证、权限、审批的唯一运行时依据
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:35:本地数据库 (认证、权限、审批的唯一运行时依据)
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:64:    """宿舍清退状态提供者接口"""
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:66:    def check_status(self, student_id: str) -> CheckoutResult:
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:67:        """运行时查询宿舍清退状态"""
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:126:    status: CheckoutStatus  # completed/pending/not_started/unknown
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:186:| Week 3-6 | 申请、审批、附件、通知模块 | 核心业务功能 |
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:229:    dorm_statuses = {
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:230:        "2020001": CheckoutStatus(status="completed", date="2024-06-15"),
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:231:        "2020002": CheckoutStatus(status="pending", date=None),
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:232:        "2020003": CheckoutStatus(status="not_started", date=None),
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:233:        "2020004": CheckoutStatus(status="unknown", date=None),  # API失败
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:236:    return students, counselors, dorm_statuses
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:244:- **宿舍清退状态：** 覆盖所有枚举值（completed/pending/not_started/unknown）
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:256:### 6.2 宿舍清退状态缓存
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:281:    def check_status(self, student_id: str) -> CheckoutResult:
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:287:            cached = self._get_cached_status(student_id)
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:293:                status=CheckoutStatus.MANUAL_PROOF_REQUIRED,
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:385:**状态：** 已批准，可执行  
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:5:**审查范围：** API设计、审批流程、部署架构、安全设计、性能优化、测试策略
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:44:4. **MAJOR**: 审批API（lines 907-945）缺少：
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:46:   - 当前审批人验证
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:56:6. **MINOR**: 创建/上传/删除使用`200`状态码（lines 770, 962, 989）
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:63:- 审批/更新端点要求`version`或`If-Match`
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:64:- 文档化角色范围列表语义：学生查看自己记录，辅导员查看分配年级/当前审批人，管理员查看全部
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:68:## 第5章：审批流程设计
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:80:   - `is_timeout`字段在`approvals`表，不在`applications`表（lines 371-372）
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:91:   - 提交/审批/驳回的审计日志
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:99:- 按审批节点跟踪超时，不是从原始提交时间
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:101:- 每次状态转换：验证状态+角色+当前审批人，锁定或检查版本，写入approval/audit/history行，更新`current_approver_id`
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:180:   - 缺少：`idx_approver_status`、`idx_student_status`、`idx_status_deleted`、`idx_app_time`、`idx_app_type`、`idx_user_read_time`、审计日志复合索引
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:186:3. **MINOR**: 缓存申请状态（lines 1778-1782）可能产生过期审批视图
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:193:- 用最终确定的数据库索引替换索引列表，并将每个映射到其查询：待审批、学生列表、未读通知、审计查找
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:195:- 不要缓存权限决策；仅缓存计数/状态，并显式失效
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:234:- 添加双重审批和微信绑定竞态的并发测试
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:243:- 第5章（审批流程）：REVISE - 5个MAJOR问题
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:37:4. `POST /api/approvals/{approval_id}/approve`
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:38:5. `POST /api/approvals/{approval_id}/reject`
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:40:列表端点 `GET /api/applications` 已不在契约中。移除列表端点是合理的，因为v0.1纵向切片只需要“登录 -> 提交 -> 审批 -> 查询单个申请”，不需要审批队列或学生申请列表。
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:42:剩余问题是计划文档仍写“4个API端点可用（登录、提交、审批、查询）”。这更像4个核心能力，而不是HTTP路由。建议统一术语：
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:45:- 核心能力：4个，登录、提交、审批、查询
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:96:计划已经移除了“申请提交API未完成 -> 只做查询API”的矛盾逻辑，新的方向是优先保留“提交 -> 辅导员审批 -> 查询”最短闭环。这符合纵向切片目标。
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:100:> 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:102:这里“砍学工部审批”和“Day 4补学工部审批”同时出现，口径冲突。更合理的表达是：
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:104:> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:128:      "field": "leave_date",
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:139:**问题：** 同一句话同时说“砍学工部审批”和“Day 4补学工部审批”。
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:141:**影响：** Day 3风险触发后团队不知道是保闭环，还是继续追两级审批。
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:143:**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:173:**当前状态：未完全达到可执行契约标准。**
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:186:2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:11:**状态：** ✅ 达到可执行契约标准
./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:33:**问题：** 风险2说"砍学工部审批"又说"Day 4补学工部审批"
./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:37:降级方案：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:42:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:70:**状态：** v0.1 Final（可执行契约标准）
./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:74:- 状态枚举（UserRole、ApplicationStatus、ApprovalStep、ApprovalDecision、DormCheckoutStatus）
./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:81:- 前端可用mock跑通登录→提交→审批→查询流程
./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:119:**状态：** 共识达成，准备启动Week 1

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/applications/tests/test_serializer_validation.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.applications.serializers import ApplicationCreateSerializer


class ApplicationCreateSerializerTest(TestCase):
    def test_reason_max_length_500(self):
        """Test reason field enforces 500 character limit"""
        data = {
            'reason': 'a' * 501,
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('reason', serializer.errors)

    def test_reason_empty_after_trim(self):
        """Test reason field rejects empty string after trim"""
        data = {
            'reason': '   ',
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('reason', serializer.errors)

    def test_leave_date_past(self):
        """Test leave_date field rejects dates before today"""
        data = {
            'reason': '毕业离校',
            'leave_date': (timezone.now().date() - timedelta(days=1)).isoformat()
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('leave_date', serializer.errors)

    def test_leave_date_today(self):
        """Test leave_date field accepts today"""
        data = {
            'reason': '毕业离校',
            'leave_date': timezone.now().date().isoformat()
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_valid_data(self):
        """Test serializer accepts valid data"""
        data = {
            'reason': '毕业离校',
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        }
        serializer = ApplicationCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['reason'], '毕业离校')

exec
/bin/bash -lc "rtk sed -n '260,420p' .omc/collaboration/artifacts/test-coverage-claude-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
## Proposed Next Steps

1. **Codex reviews this response** and provides feedback
2. **Reach consensus** on final test plan and time estimate
3. **Execute agreed-upon tests** without further user intervention
4. **Verify all tests pass**
5. **Commit and push** changes
6. **Update PROJECT-SUMMARY.md** and session-context.json

---

**Status:** Awaiting Codex review and consensus

exec
/bin/bash -lc "rtk sed -n '1,240p' backend/apps/approvals/tests/test_state_machine.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User, UserRole
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.users.class_mapping import ClassMapping


class ApprovalStateMachineTestCase(TestCase):
    def setUp(self):
        # Create student
        self.student = User.objects.create_user(
            user_id='2020001',
            name='张三',
            role=UserRole.STUDENT,
            class_id='CS2020-01',
            password='2020001'
        )

        # Create counselor
        self.counselor = User.objects.create_user(
            user_id='T001',
            name='李老师',
            role=UserRole.COUNSELOR,
            password='T001'
        )

        # Create dean
        self.dean = User.objects.create_user(
            user_id='D001',
            name='赵主任',
            role=UserRole.DEAN,
            password='D001'
        )

        # Create class mapping
        ClassMapping.objects.create(
            class_id='CS2020-01',
            counselor=self.counselor,
            counselor_name='李老师',
            active=True
        )

        # Create application
        self.application = Application.objects.create(
            application_id='app_test001',
            student=self.student,
            student_name='张三',
            class_id='CS2020-01',
            reason='测试原因',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        # Create counselor approval
        self.approval = Approval.objects.create(
            approval_id='apv_test001',
            application=self.application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name='李老师',
            decision=ApprovalDecision.PENDING
        )

        self.client = APIClient()

    def test_duplicate_approval_conflict(self):
        """测试重复审批返回409"""
        self.client.force_authenticate(user=self.counselor)

        # First approval
        response1 = self.client.post(
            f'/api/approvals/{self.approval.approval_id}/approve/',
            {'comment': '同意'},
            format='json'
        )
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        # Second approval attempt
        response2 = self.client.post(
            f'/api/approvals/{self.approval.approval_id}/approve/',
            {'comment': '再次同意'},
            format='json'
        )
        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)

    def test_reject_then_repeat_operation_conflict(self):
        """测试驳回后的重复操作返回409"""
        self.client.force_authenticate(user=self.counselor)

        response1 = self.client.post(
            f'/api/approvals/{self.approval.approval_id}/reject/',
            {'comment': '不同意'},
            format='json'
        )
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        response2 = self.client.post(
            f'/api/approvals/{self.approval.approval_id}/reject/',
            {'comment': '再次不同意'},
            format='json'
        )
        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)

    def test_counselor_step_requires_pending_counselor_status(self):
        """测试辅导员审批步骤与申请状态不匹配时返回409"""
        self.application.status = ApplicationStatus.PENDING_DEAN
        self.application.save()
        self.client.force_authenticate(user=self.counselor)

        approve_response = self.client.post(
            f'/api/approvals/{self.approval.approval_id}/approve/',
            {'comment': '同意'},
            format='json'
        )
        reject_response = self.client.post(
            f'/api/approvals/{self.approval.approval_id}/reject/',
            {'comment': '不同意'},
            format='json'
        )

        self.assertEqual(approve_response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(reject_response.status_code, status.HTTP_409_CONFLICT)

    def test_dean_step_requires_pending_dean_status(self):
        """测试学工部审批步骤与申请状态不匹配时返回409"""
        self.application.status = ApplicationStatus.APPROVED
        self.application.save()
        dean_approval = Approval.objects.create(
            approval_id='apv_test002',
            application=self.application,
            step=ApprovalStep.DEAN,
            approver=self.dean,
            approver_name='赵主任',
            decision=ApprovalDecision.PENDING
        )
        self.client.force_authenticate(user=self.dean)

        approve_response = self.client.post(
            f'/api/approvals/{dean_approval.approval_id}/approve/',
            {'comment': '同意'},
            format='json'
        )
        reject_response = self.client.post(
            f'/api/approvals/{dean_approval.approval_id}/reject/',
            {'comment': '不同意'},
            format='json'
        )

        self.assertEqual(approve_response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(reject_response.status_code, status.HTTP_409_CONFLICT)

exec
/bin/bash -lc "rtk sed -n '1,240p' backend/apps/approvals/tests/test_permissions.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User, UserRole
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.users.class_mapping import ClassMapping
import uuid


class ApprovalPermissionsTestCase(TestCase):
    def setUp(self):
        # Create students
        self.student1 = User.objects.create_user(
            user_id='2020001',
            name='张三',
            role=UserRole.STUDENT,
            class_id='CS2020-01',
            password='2020001'
        )
        self.student2 = User.objects.create_user(
            user_id='2020002',
            name='李四',
            role=UserRole.STUDENT,
            class_id='CS2020-02',
            password='2020002'
        )

        # Create counselors
        self.counselor1 = User.objects.create_user(
            user_id='T001',
            name='李老师',
            role=UserRole.COUNSELOR,
            password='T001'
        )
        self.counselor2 = User.objects.create_user(
            user_id='T002',
            name='王老师',
            role=UserRole.COUNSELOR,
            password='T002'
        )
        self.dean1 = User.objects.create_user(
            user_id='D001',
            name='赵主任',
            role=UserRole.DEAN,
            password='D001'
        )
        self.dean2 = User.objects.create_user(
            user_id='D002',
            name='钱主任',
            role=UserRole.DEAN,
            password='D002'
        )

        # Create class mappings
        ClassMapping.objects.create(
            class_id='CS2020-01',
            counselor=self.counselor1,
            counselor_name='李老师',
            active=True
        )
        ClassMapping.objects.create(
            class_id='CS2020-02',
            counselor=self.counselor2,
            counselor_name='王老师',
            active=True
        )

        # Create application for student1
        self.application1 = Application.objects.create(
            application_id='app_test001',
            student=self.student1,
            student_name='张三',
            class_id='CS2020-01',
            reason='测试原因',
            leave_date='2024-06-30',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        # Create counselor approval for application1
        self.approval1 = Approval.objects.create(
            approval_id='apv_test001',
            application=self.application1,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor1,
            approver_name='李老师',
            decision=ApprovalDecision.PENDING
        )

        self.client = APIClient()

    def _create_dean_approval(self):
        self.application1.status = ApplicationStatus.PENDING_DEAN
        self.application1.save()
        return Approval.objects.create(
            approval_id='apv_test002',
            application=self.application1,
            step=ApprovalStep.DEAN,
            approver=self.dean1,
            approver_name='赵主任',
            decision=ApprovalDecision.PENDING
        )

    def test_student_cannot_approve_or_reject(self):
        """学生不能调用审批操作接口"""
        self.client.force_authenticate(user=self.student1)

        approve_response = self.client.post(
            f'/api/approvals/{self.approval1.approval_id}/approve/',
            {'comment': '同意'},
            format='json'
        )
        reject_response = self.client.post(
            f'/api/approvals/{self.approval1.approval_id}/reject/',
            {'comment': '不同意'},
            format='json'
        )

        self.assertEqual(approve_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(reject_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_dean_cannot_act_on_counselor_step(self):
        """学工部不能处理辅导员审批步骤"""
        self.client.force_authenticate(user=self.dean1)

        response = self.client.post(
            f'/api/approvals/{self.approval1.approval_id}/approve/',
            {'comment': '同意'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_counselor_cannot_act_on_dean_step(self):
        """辅导员不能处理学工部审批步骤"""
        dean_approval = self._create_dean_approval()
        self.client.force_authenticate(user=self.counselor1)

        response = self.client.post(
            f'/api/approvals/{dean_approval.approval_id}/approve/',
            {'comment': '同意'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_assigned_dean_forbidden(self):
        """同角色但非指定学工部审批人不能处理审批"""
        dean_approval = self._create_dean_approval()
        self.client.force_authenticate(user=self.dean2)

        response = self.client.post(
            f'/api/approvals/{dean_approval.approval_id}/reject/',
            {'comment': '不同意'},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cross_counselor_approve_forbidden(self):
        """测试跨辅导员审批返回403"""
        # T002 tries to approve T001's application
        self.client.force_authenticate(user=self.counselor2)
        response = self.client.post(
            f'/api/approvals/{self.approval1.approval_id}/approve/',
            {'comment': '同意'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cross_counselor_reject_forbidden(self):
        """测试跨辅导员驳回返回403"""
        # T002 tries to reject T001's application
        self.client.force_authenticate(user=self.counselor2)
        response = self.client.post(
            f'/api/approvals/{self.approval1.approval_id}/reject/',
            {'comment': '不同意'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

codex
现有代码里已经有一部分状态机和权限负向测试，尤其是 approval 操作层；我会再读 detail endpoint 的实现和列表过滤逻辑，避免建议重复覆盖已经存在的路径。
exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/applications/models.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.db import models
from django.core.exceptions import ValidationError
from apps.users.models import User


class ApplicationStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    PENDING_COUNSELOR = 'pending_counselor', '待辅导员审批'
    PENDING_DEAN = 'pending_dean', '待学工部审批'
    APPROVED = 'approved', '已通过'
    REJECTED = 'rejected', '已驳回'


class DormCheckoutStatus(models.TextChoices):
    COMPLETED = 'completed', '已清退'
    PENDING = 'pending', '清退中'
    NOT_STARTED = 'not_started', '未开始'
    UNKNOWN = 'unknown', '状态未知'


class Application(models.Model):
    application_id = models.CharField(max_length=50, primary_key=True)
    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='applications')
    student_name = models.CharField(max_length=100)
    class_id = models.CharField(max_length=50)
    reason = models.TextField()
    leave_date = models.DateField()
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.DRAFT)
    dorm_checkout_status = models.CharField(max_length=20, choices=DormCheckoutStatus.choices, default=DormCheckoutStatus.NOT_STARTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'applications'

    def clean(self):
        if self.status in [ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.PENDING_DEAN, ApplicationStatus.APPROVED]:
            existing = Application.objects.filter(
                student=self.student,
                status__in=[ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.PENDING_DEAN, ApplicationStatus.APPROVED]
            ).exclude(application_id=self.application_id).exists()
            if existing:
                raise ValidationError('该学生已有待审批或已通过的申请，不能重复提交')

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/applications/serializers.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import serializers
from .models import Application


class ApplicationListSerializer(serializers.ModelSerializer):
    """Lean serializer for application lists - no nested approvals"""
    student_id = serializers.CharField(source='student.user_id', read_only=True)

    class Meta:
        model = Application
        fields = ['application_id', 'student_id', 'student_name', 'class_id',
                  'reason', 'leave_date', 'status', 'created_at', 'updated_at']
        read_only_fields = ['application_id', 'student_id', 'student_name',
                            'class_id', 'status', 'created_at', 'updated_at']


class ApplicationSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(source='student.user_id', read_only=True)
    approvals = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['application_id', 'student_id', 'student_name', 'class_id',
                  'reason', 'leave_date', 'status', 'dorm_checkout_status',
                  'approvals', 'created_at', 'updated_at']
        read_only_fields = ['application_id', 'student_id', 'student_name',
                            'class_id', 'status', 'dorm_checkout_status',
                            'created_at', 'updated_at']

    def get_approvals(self, obj):
        from apps.approvals.serializers import ApprovalSerializer
        return ApprovalSerializer(obj.approvals.all(), many=True).data


class ApplicationCreateSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=500, trim_whitespace=True)
    leave_date = serializers.DateField()

    def validate_reason(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('离校原因不能为空')
        return value

    def validate_leave_date(self, value):
        from django.utils import timezone
        today = timezone.now().date()
        if value < today:
            raise serializers.ValidationError('离校日期不能早于今天')
        return value

exec
/bin/bash -lc "rtk sed -n '1,300p' backend/apps/approvals/views.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from .models import Approval, ApprovalDecision, ApprovalStep
from .serializers import ApprovalSerializer, ApprovalActionSerializer, ApprovalListSerializer
from .pagination import ApprovalLimitOffsetPagination
from .validators import approval_step_matches_application_status
from apps.applications.models import Application, ApplicationStatus
from apps.users.models import UserRole
import uuid


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_approvals(request):
    user = request.user

    # 学生禁止访问
    if user.role == UserRole.STUDENT:
        return Response(
            {'error': {'code': 'FORBIDDEN', 'message': '学生不能访问审批列表'}},
            status=status.HTTP_403_FORBIDDEN
        )

    # 辅导员: 只看自己的counselor审批
    if user.role == UserRole.COUNSELOR:
        queryset = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.COUNSELOR
        ).select_related('application', 'approver')

    # 学工部: 只看自己的dean审批
    elif user.role == UserRole.DEAN:
        queryset = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.DEAN
        ).select_related('application', 'approver')

    else:
        return Response(
            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
            status=status.HTTP_403_FORBIDDEN
        )

    # Decision filtering (default: pending)
    decision_param = request.query_params.get('decision', 'pending')
    if decision_param != 'all':
        queryset = queryset.filter(decision=decision_param)

    # 排序
    queryset = queryset.order_by('-created_at', '-approval_id')

    # 分页
    paginator = ApprovalLimitOffsetPagination()
    page = paginator.paginate_queryset(queryset, request)

    # 序列化
    serializer = ApprovalListSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def approve_approval(request, approval_id):
    try:
        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
    except Approval.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
                        status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
                        status=status.HTTP_403_FORBIDDEN)
    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
                        status=status.HTTP_403_FORBIDDEN)

    if approval.approver_id != user.user_id:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
                        status=status.HTTP_403_FORBIDDEN)

    if approval.decision != ApprovalDecision.PENDING:
        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
                        status=status.HTTP_409_CONFLICT)

    if not approval_step_matches_application_status(approval):
        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
                        status=status.HTTP_409_CONFLICT)

    serializer = ApprovalActionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败'}},
                        status=status.HTTP_400_BAD_REQUEST)

    approval.decision = ApprovalDecision.APPROVED
    approval.comment = serializer.validated_data.get('comment', '')
    approval.decided_at = timezone.now()
    approval.save()

    application = approval.application
    if approval.step == ApprovalStep.COUNSELOR:
        # Check for existing dean approval to prevent duplicates
        existing_dean_approval = Approval.objects.filter(
            application=application,
            step=ApprovalStep.DEAN
        ).exists()

        if existing_dean_approval:
            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
                            status=status.HTTP_409_CONFLICT)

        application.status = ApplicationStatus.PENDING_DEAN
        application.save()
        Approval.objects.create(
            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
            application=application,
            step=ApprovalStep.DEAN,
            approver_id='D001',
            approver_name='赵主任',
            decision=ApprovalDecision.PENDING
        )
    elif approval.step == ApprovalStep.DEAN:
        application.status = ApplicationStatus.APPROVED
        application.save()

    return Response(ApprovalSerializer(approval).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def reject_approval(request, approval_id):
    try:
        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
    except Approval.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
                        status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
                        status=status.HTTP_403_FORBIDDEN)
    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
                        status=status.HTTP_403_FORBIDDEN)

    if approval.approver_id != user.user_id:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
                        status=status.HTTP_403_FORBIDDEN)

    if approval.decision != ApprovalDecision.PENDING:
        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
                        status=status.HTTP_409_CONFLICT)

    if not approval_step_matches_application_status(approval):
        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
                        status=status.HTTP_409_CONFLICT)

    serializer = ApprovalActionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败'}},
                        status=status.HTTP_400_BAD_REQUEST)

    approval.decision = ApprovalDecision.REJECTED
    approval.comment = serializer.validated_data.get('comment', '')
    approval.decided_at = timezone.now()
    approval.save()

    application = approval.application
    application.status = ApplicationStatus.REJECTED
    application.save()

    return Response(ApprovalSerializer(approval).data)

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/approvals/models.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.db import models
from apps.users.models import User
from apps.applications.models import Application


class ApprovalStep(models.TextChoices):
    COUNSELOR = 'counselor', '辅导员'
    DEAN = 'dean', '学工部'


class ApprovalDecision(models.TextChoices):
    PENDING = 'pending', '待审批'
    APPROVED = 'approved', '已通过'
    REJECTED = 'rejected', '已驳回'


class Approval(models.Model):
    approval_id = models.CharField(max_length=50, primary_key=True)
    application = models.ForeignKey(Application, on_delete=models.PROTECT, related_name='approvals')
    step = models.CharField(max_length=20, choices=ApprovalStep.choices)
    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approvals')
    approver_name = models.CharField(max_length=100)
    decision = models.CharField(max_length=20, choices=ApprovalDecision.choices, default=ApprovalDecision.PENDING)
    comment = models.TextField(null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'approvals'

exec
/bin/bash -lc "rtk sed -n '1,280p' backend/apps/applications/views.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Application, ApplicationStatus, DormCheckoutStatus
from .serializers import ApplicationSerializer, ApplicationCreateSerializer, ApplicationListSerializer
from .pagination import ApplicationLimitOffsetPagination
from .providers import MockDormCheckoutProvider
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.users.models import UserRole
from apps.users.class_mapping import ClassMapping
import uuid


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def applications_view(request):
    if request.method == 'GET':
        return list_applications(request)
    else:
        return create_application(request)


def list_applications(request):
    user = request.user

    # Student: own applications only
    if user.role == UserRole.STUDENT:
        queryset = Application.objects.filter(student=user)

    # Counselor: applications with own pending counselor approvals
    elif user.role == UserRole.COUNSELOR:
        pending_approvals = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.COUNSELOR,
            decision=ApprovalDecision.PENDING
        ).values_list('application', flat=True)
        queryset = Application.objects.filter(pk__in=pending_approvals)

    # Dean: applications with own pending dean approvals
    elif user.role == UserRole.DEAN:
        pending_approvals = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.DEAN,
            decision=ApprovalDecision.PENDING
        ).values_list('application', flat=True)
        queryset = Application.objects.filter(pk__in=pending_approvals)

    else:
        return Response(
            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
            status=status.HTTP_403_FORBIDDEN
        )

    # Status filtering
    status_param = request.query_params.get('status')
    if status_param:
        queryset = queryset.filter(status=status_param)

    # Sort by created_at DESC
    queryset = queryset.order_by('-created_at', '-application_id')

    # Paginate
    paginator = ApplicationLimitOffsetPagination()
    page = paginator.paginate_queryset(queryset, request)

    # Serialize
    serializer = ApplicationListSerializer(page, many=True)

    return paginator.get_paginated_response(serializer.data)


def create_application(request):
    user = request.user

    if user.role != UserRole.STUDENT:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以提交申请'}},
                        status=status.HTTP_403_FORBIDDEN)

    # Check for existing pending/approved applications
    existing = Application.objects.filter(
        student=user,
        status__in=[ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.PENDING_DEAN, ApplicationStatus.APPROVED]
    ).first()
    if existing:
        return Response({'error': {'code': 'CONFLICT', 'message': '已有待审批或已通过的申请，不能重复提交',
                                    'details': {'student_id': user.user_id, 'existing_application_id': existing.application_id, 'status': existing.status}}},
                        status=status.HTTP_409_CONFLICT)

    serializer = ApplicationCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
                                    'details': serializer.errors}},
                        status=status.HTTP_400_BAD_REQUEST)

    provider = MockDormCheckoutProvider()
    dorm_status = provider.check_status(user.user_id)

    if dorm_status.status != DormCheckoutStatus.COMPLETED:
        return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
                                    'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
                                                'blocking_reason': dorm_status.blocking_reason}}},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    try:
        class_mapping = ClassMapping.objects.get(class_id=user.class_id, active=True)
    except ClassMapping.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '班级映射不存在',
                                    'details': {'class_id': user.class_id}}},
                        status=status.HTTP_404_NOT_FOUND)

    application = Application.objects.create(
        application_id=f'app_{uuid.uuid4().hex[:8]}',
        student=user,
        student_name=user.name,
        class_id=user.class_id,
        reason=serializer.validated_data['reason'],
        leave_date=serializer.validated_data['leave_date'],
        status=ApplicationStatus.PENDING_COUNSELOR,
        dorm_checkout_status=dorm_status.status
    )

    Approval.objects.create(
        approval_id=f'apv_{uuid.uuid4().hex[:8]}',
        application=application,
        step=ApprovalStep.COUNSELOR,
        approver=class_mapping.counselor,
        approver_name=class_mapping.counselor_name,
        decision=ApprovalDecision.PENDING
    )

    return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_application(request, application_id):
    try:
        application = Application.objects.get(application_id=application_id)
    except Application.DoesNotExist:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在',
                                    'details': {'application_id': application_id}}},
                        status=status.HTTP_404_NOT_FOUND)

    user = request.user

    # Student: can only view own application
    if user.role == UserRole.STUDENT and application.student.user_id != user.user_id:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
                        status=status.HTTP_403_FORBIDDEN)

    # Counselor: can only view applications from assigned classes
    if user.role == UserRole.COUNSELOR:
        try:
            class_mapping = ClassMapping.objects.get(counselor=user, class_id=application.class_id, active=True)
        except ClassMapping.DoesNotExist:
            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
                            status=status.HTTP_403_FORBIDDEN)

    # Dean: can only view applications with own pending dean approvals
    if user.role == UserRole.DEAN:
        has_pending_approval = Approval.objects.filter(
            application=application,
            approver=user,
            step=ApprovalStep.DEAN,
            decision=ApprovalDecision.PENDING
        ).exists()
        if not has_pending_approval:
            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
                            status=status.HTTP_403_FORBIDDEN)

    return Response(ApplicationSerializer(application).data)

exec
/bin/bash -lc "rtk sed -n '1,280p' backend/apps/applications/tests/test_application_flow.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User, UserRole
from apps.users.class_mapping import ClassMapping
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalDecision


class ApplicationFlowTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test users
        self.student = User.objects.create_user(
            user_id='2020001',
            password='2020001',
            name='张三',
            role=UserRole.STUDENT,
            class_id='CS2020-01',
            is_graduating=True,
            graduation_year=2024
        )

        self.counselor = User.objects.create_user(
            user_id='T001',
            password='T001',
            name='李老师',
            role=UserRole.COUNSELOR
        )

        self.dean = User.objects.create_user(
            user_id='D001',
            password='D001',
            name='赵主任',
            role=UserRole.DEAN
        )

        # Create class mapping
        ClassMapping.objects.create(
            class_id='CS2020-01',
            counselor=self.counselor,
            counselor_name='李老师',
            active=True
        )

    def test_complete_application_flow(self):
        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""

        # Step 1: 学生登录
        response = self.client.post('/api/auth/login', {
            'user_id': '2020001',
            'password': '2020001'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        student_token = response.data['access_token']

        # Step 2: 学生提交申请
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
        response = self.client.post('/api/applications/', {
            'reason': '毕业离校',
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], ApplicationStatus.PENDING_COUNSELOR)
        application_id = response.data['application_id']

        # Step 3: 辅导员登录
        response = self.client.post('/api/auth/login', {
            'user_id': 'T001',
            'password': 'T001'
        }, format='json')
        counselor_token = response.data['access_token']

        # Step 4: 辅导员审批通过
        application = Application.objects.get(application_id=application_id)
        counselor_approval = application.approvals.filter(step='counselor').first()

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {counselor_token}')
        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/approve/', {
            'comment': '同意离校'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['decision'], ApprovalDecision.APPROVED)

        # Step 5: 学工部登录
        response = self.client.post('/api/auth/login', {
            'user_id': 'D001',
            'password': 'D001'
        }, format='json')
        dean_token = response.data['access_token']

        # Step 6: 学工部审批通过
        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.PENDING_DEAN)
        dean_approval = application.approvals.filter(step='dean').first()

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dean_token}')
        response = self.client.post(f'/api/approvals/{dean_approval.approval_id}/approve/', {
            'comment': '同意离校'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Step 7: 查询申请状态
        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.APPROVED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
        response = self.client.get(f'/api/applications/{application_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], ApplicationStatus.APPROVED)
        self.assertEqual(len(response.data['approvals']), 2)

exec
/bin/bash -lc "rtk sed -n '1,180p' backend/apps/approvals/validators.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from apps.applications.models import ApplicationStatus


EXPECTED_STATUS_BY_STEP = {
    'counselor': ApplicationStatus.PENDING_COUNSELOR,
    'dean': ApplicationStatus.PENDING_DEAN,
}


def approval_step_matches_application_status(approval):
    expected_status = EXPECTED_STATUS_BY_STEP.get(approval.step)
    if expected_status is None:
        return False
    return approval.application.status == expected_status

exec
/bin/bash -lc "rtk sed -n '1,280p' backend/apps/approvals/tests/test_rejection_flow.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User, UserRole
from apps.users.class_mapping import ClassMapping
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import ApprovalDecision


class RejectionFlowTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.student = User.objects.create_user(
            user_id='2020001',
            password='2020001',
            name='张三',
            role=UserRole.STUDENT,
            class_id='CS2020-01',
            is_graduating=True,
            graduation_year=2024
        )

        self.counselor = User.objects.create_user(
            user_id='T001',
            password='T001',
            name='李老师',
            role=UserRole.COUNSELOR
        )

        self.dean = User.objects.create_user(
            user_id='D001',
            password='D001',
            name='赵主任',
            role=UserRole.DEAN
        )

        # Create class mapping
        ClassMapping.objects.create(
            class_id='CS2020-01',
            counselor=self.counselor,
            counselor_name='李老师',
            active=True
        )

    def test_counselor_rejection(self):
        """测试辅导员驳回申请"""
        # Student login and submit
        response = self.client.post('/api/auth/login', {
            'user_id': '2020001',
            'password': '2020001'
        })
        student_token = response.data['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
        response = self.client.post('/api/applications/', {
            'reason': '毕业离校',
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        })
        application_id = response.data['application_id']

        # Counselor login and reject
        response = self.client.post('/api/auth/login', {
            'user_id': 'T001',
            'password': 'T001'
        })
        counselor_token = response.data['access_token']

        application = Application.objects.get(application_id=application_id)
        counselor_approval = application.approvals.filter(step='counselor').first()

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {counselor_token}')
        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/reject/', {
            'comment': '材料不齐全'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['decision'], ApprovalDecision.REJECTED)

        # Verify application status
        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.REJECTED)

    def test_dean_rejection(self):
        """测试学工部驳回申请"""
        # Student login and submit
        response = self.client.post('/api/auth/login', {
            'user_id': '2020001',
            'password': '2020001'
        })
        student_token = response.data['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
        response = self.client.post('/api/applications/', {
            'reason': '毕业离校',
            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
        })
        application_id = response.data['application_id']

        # Counselor approve
        response = self.client.post('/api/auth/login', {
            'user_id': 'T001',
            'password': 'T001'
        })
        counselor_token = response.data['access_token']

        application = Application.objects.get(application_id=application_id)
        counselor_approval = application.approvals.filter(step='counselor').first()

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {counselor_token}')
        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/approve/', {
            'comment': '同意'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Dean login and reject
        response = self.client.post('/api/auth/login', {
            'user_id': 'D001',
            'password': 'D001'
        })
        dean_token = response.data['access_token']

        application.refresh_from_db()
        dean_approval = application.approvals.filter(step='dean').first()

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dean_token}')
        response = self.client.post(f'/api/approvals/{dean_approval.approval_id}/reject/', {
            'comment': '不符合离校条件'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['decision'], ApprovalDecision.REJECTED)

        # Verify application status
        application.refresh_from_db()
        self.assertEqual(application.status, ApplicationStatus.REJECTED)

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/applications/tests/test_list_permissions.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.test import TestCase
from rest_framework.test import APIClient
from apps.users.models import User, UserRole
from apps.users.class_mapping import ClassMapping
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision


class ApplicationListPermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.student1 = User.objects.create(user_id='S001', name='学生1', role=UserRole.STUDENT, class_id='CS2020-01')
        self.student1.set_password('S001')
        self.student1.save()

        self.student2 = User.objects.create(user_id='S002', name='学生2', role=UserRole.STUDENT, class_id='CS2020-02')
        self.student2.set_password('S002')
        self.student2.save()

        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
        self.counselor1.set_password('T001')
        self.counselor1.save()

        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
        self.counselor2.set_password('T002')
        self.counselor2.save()

        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
        self.dean.set_password('D001')
        self.dean.save()

        # Create class mappings
        ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
        ClassMapping.objects.create(class_id='CS2020-02', counselor=self.counselor2, counselor_name='辅导员2', active=True)

        # Create applications
        self.app1 = Application.objects.create(
            application_id='app_001',
            student=self.student1,
            student_name='学生1',
            class_id='CS2020-01',
            reason='测试',
            leave_date='2024-07-01',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        self.app2 = Application.objects.create(
            application_id='app_002',
            student=self.student2,
            student_name='学生2',
            class_id='CS2020-02',
            reason='测试',
            leave_date='2024-07-01',
            status=ApplicationStatus.PENDING_DEAN
        )

        # Create approvals
        Approval.objects.create(
            approval_id='apv_001',
            application=self.app1,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor1,
            approver_name='辅导员1',
            decision=ApprovalDecision.PENDING
        )

        Approval.objects.create(
            approval_id='apv_002',
            application=self.app2,
            step=ApprovalStep.DEAN,
            approver=self.dean,
            approver_name='学工部',
            decision=ApprovalDecision.PENDING
        )

    def test_student_sees_only_own_applications(self):
        self.client.force_authenticate(user=self.student1)
        response = self.client.get('/api/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['application_id'], 'app_001')

    def test_student_cannot_see_other_student_applications(self):
        self.client.force_authenticate(user=self.student1)
        response = self.client.get('/api/applications/')
        app_ids = [app['application_id'] for app in response.data['results']]
        self.assertNotIn('app_002', app_ids)

    def test_counselor_sees_only_pending_counselor_approvals(self):
        self.client.force_authenticate(user=self.counselor1)
        response = self.client.get('/api/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['application_id'], 'app_001')

    def test_counselor_cannot_see_other_counselor_applications(self):
        self.client.force_authenticate(user=self.counselor2)
        response = self.client.get('/api/applications/')
        self.assertEqual(response.data['count'], 0)

    def test_dean_sees_only_pending_dean_approvals(self):
        self.client.force_authenticate(user=self.dean)
        response = self.client.get('/api/applications/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['application_id'], 'app_002')

    def test_response_format_no_nested_approvals(self):
        self.client.force_authenticate(user=self.student1)
        response = self.client.get('/api/applications/')
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertNotIn('approvals', response.data['results'][0])

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/approvals/tests/test_list_permissions.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.test import TestCase
from rest_framework.test import APIClient
from apps.users.models import User, UserRole
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision


class ApprovalListPermissionTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.student = User.objects.create(user_id='S001', name='学生', role=UserRole.STUDENT, class_id='CS2020-01')
        self.student.set_password('S001')
        self.student.save()

        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
        self.counselor1.set_password('T001')
        self.counselor1.save()

        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
        self.counselor2.set_password('T002')
        self.counselor2.save()

        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
        self.dean1.set_password('D001')
        self.dean1.save()

        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
        self.dean2.set_password('D002')
        self.dean2.save()

        # Create application
        self.app = Application.objects.create(
            application_id='app_001',
            student=self.student,
            student_name='学生',
            class_id='CS2020-01',
            reason='测试',
            leave_date='2024-07-01',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        # Create approvals
        self.approval_c1 = Approval.objects.create(
            approval_id='apv_c1',
            application=self.app,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor1,
            approver_name='辅导员1',
            decision=ApprovalDecision.PENDING
        )

        self.approval_d1 = Approval.objects.create(
            approval_id='apv_d1',
            application=self.app,
            step=ApprovalStep.DEAN,
            approver=self.dean1,
            approver_name='学工部1',
            decision=ApprovalDecision.PENDING
        )

    def test_student_403_on_approval_list(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/approvals/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')

    def test_counselor_sees_only_own_pending_approvals(self):
        self.client.force_authenticate(user=self.counselor1)
        response = self.client.get('/api/approvals/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['approval_id'], 'apv_c1')

    def test_counselor_cannot_see_other_counselor_approvals(self):
        self.client.force_authenticate(user=self.counselor2)
        response = self.client.get('/api/approvals/')
        self.assertEqual(response.data['count'], 0)

    def test_dean_sees_only_own_pending_approvals(self):
        self.client.force_authenticate(user=self.dean1)
        response = self.client.get('/api/approvals/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['approval_id'], 'apv_d1')

    def test_dean_cannot_see_other_dean_approvals(self):
        self.client.force_authenticate(user=self.dean2)
        response = self.client.get('/api/approvals/')
        self.assertEqual(response.data['count'], 0)

    def test_response_format_count_and_results(self):
        self.client.force_authenticate(user=self.counselor1)
        response = self.client.get('/api/approvals/')
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertNotIn('next', response.data)
        self.assertNotIn('previous', response.data)

codex
现在的关键判断是：修订方案方向对，但仍有两处会把工作量吃掉，一处是“非法路径”里有些只能测 API 行为，不能假装系统已有模型级状态机；另一处是 detail 权限里的 dean 语义要和当前实现的 pending-only 保持一致。
exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/views.py | sed -n '20,145p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
    20	
    21	    # 学生禁止访问
    22	    if user.role == UserRole.STUDENT:
    23	        return Response(
    24	            {'error': {'code': 'FORBIDDEN', 'message': '学生不能访问审批列表'}},
    25	            status=status.HTTP_403_FORBIDDEN
    26	        )
    27	
    28	    # 辅导员: 只看自己的counselor审批
    29	    if user.role == UserRole.COUNSELOR:
    30	        queryset = Approval.objects.filter(
    31	            approver=user,
    32	            step=ApprovalStep.COUNSELOR
    33	        ).select_related('application', 'approver')
    34	
    35	    # 学工部: 只看自己的dean审批
    36	    elif user.role == UserRole.DEAN:
    37	        queryset = Approval.objects.filter(
    38	            approver=user,
    39	            step=ApprovalStep.DEAN
    40	        ).select_related('application', 'approver')
    41	
    42	    else:
    43	        return Response(
    44	            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
    45	            status=status.HTTP_403_FORBIDDEN
    46	        )
    47	
    48	    # Decision filtering (default: pending)
    49	    decision_param = request.query_params.get('decision', 'pending')
    50	    if decision_param != 'all':
    51	        queryset = queryset.filter(decision=decision_param)
    52	
    53	    # 排序
    54	    queryset = queryset.order_by('-created_at', '-approval_id')
    55	
    56	    # 分页
    57	    paginator = ApprovalLimitOffsetPagination()
    58	    page = paginator.paginate_queryset(queryset, request)
    59	
    60	    # 序列化
    61	    serializer = ApprovalListSerializer(page, many=True)
    62	
    63	    return paginator.get_paginated_response(serializer.data)
    64	
    65	
    66	@api_view(['POST'])
    67	@permission_classes([IsAuthenticated])
    68	@transaction.atomic
    69	def approve_approval(request, approval_id):
    70	    try:
    71	        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
    72	    except Approval.DoesNotExist:
    73	        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
    74	                        status=status.HTTP_404_NOT_FOUND)
    75	
    76	    user = request.user
    77	    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
    78	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
    79	                        status=status.HTTP_403_FORBIDDEN)
    80	    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
    81	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
    82	                        status=status.HTTP_403_FORBIDDEN)
    83	
    84	    if approval.approver_id != user.user_id:
    85	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
    86	                        status=status.HTTP_403_FORBIDDEN)
    87	
    88	    if approval.decision != ApprovalDecision.PENDING:
    89	        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
    90	                        status=status.HTTP_409_CONFLICT)
    91	
    92	    if not approval_step_matches_application_status(approval):
    93	        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
    94	                        status=status.HTTP_409_CONFLICT)
    95	
    96	    serializer = ApprovalActionSerializer(data=request.data)
    97	    if not serializer.is_valid():
    98	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败'}},
    99	                        status=status.HTTP_400_BAD_REQUEST)
   100	
   101	    approval.decision = ApprovalDecision.APPROVED
   102	    approval.comment = serializer.validated_data.get('comment', '')
   103	    approval.decided_at = timezone.now()
   104	    approval.save()
   105	
   106	    application = approval.application
   107	    if approval.step == ApprovalStep.COUNSELOR:
   108	        # Check for existing dean approval to prevent duplicates
   109	        existing_dean_approval = Approval.objects.filter(
   110	            application=application,
   111	            step=ApprovalStep.DEAN
   112	        ).exists()
   113	
   114	        if existing_dean_approval:
   115	            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
   116	                            status=status.HTTP_409_CONFLICT)
   117	
   118	        application.status = ApplicationStatus.PENDING_DEAN
   119	        application.save()
   120	        Approval.objects.create(
   121	            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
   122	            application=application,
   123	            step=ApprovalStep.DEAN,
   124	            approver_id='D001',
   125	            approver_name='赵主任',
   126	            decision=ApprovalDecision.PENDING
   127	        )
   128	    elif approval.step == ApprovalStep.DEAN:
   129	        application.status = ApplicationStatus.APPROVED
   130	        application.save()
   131	
   132	    return Response(ApprovalSerializer(approval).data)
   133	
   134	
   135	@api_view(['POST'])
   136	@permission_classes([IsAuthenticated])
   137	@transaction.atomic
   138	def reject_approval(request, approval_id):
   139	    try:
   140	        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
   141	    except Approval.DoesNotExist:
   142	        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
   143	                        status=status.HTTP_404_NOT_FOUND)
   144	
   145	    user = request.user

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/views.py | sed -n '120,190p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   120	        status=ApplicationStatus.PENDING_COUNSELOR,
   121	        dorm_checkout_status=dorm_status.status
   122	    )
   123	
   124	    Approval.objects.create(
   125	        approval_id=f'apv_{uuid.uuid4().hex[:8]}',
   126	        application=application,
   127	        step=ApprovalStep.COUNSELOR,
   128	        approver=class_mapping.counselor,
   129	        approver_name=class_mapping.counselor_name,
   130	        decision=ApprovalDecision.PENDING
   131	    )
   132	
   133	    return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
   134	
   135	
   136	@api_view(['GET'])
   137	@permission_classes([IsAuthenticated])
   138	def get_application(request, application_id):
   139	    try:
   140	        application = Application.objects.get(application_id=application_id)
   141	    except Application.DoesNotExist:
   142	        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在',
   143	                                    'details': {'application_id': application_id}}},
   144	                        status=status.HTTP_404_NOT_FOUND)
   145	
   146	    user = request.user
   147	
   148	    # Student: can only view own application
   149	    if user.role == UserRole.STUDENT and application.student.user_id != user.user_id:
   150	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
   151	                        status=status.HTTP_403_FORBIDDEN)
   152	
   153	    # Counselor: can only view applications from assigned classes
   154	    if user.role == UserRole.COUNSELOR:
   155	        try:
   156	            class_mapping = ClassMapping.objects.get(counselor=user, class_id=application.class_id, active=True)
   157	        except ClassMapping.DoesNotExist:
   158	            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
   159	                            status=status.HTTP_403_FORBIDDEN)
   160	
   161	    # Dean: can only view applications with own pending dean approvals
   162	    if user.role == UserRole.DEAN:
   163	        has_pending_approval = Approval.objects.filter(
   164	            application=application,
   165	            approver=user,
   166	            step=ApprovalStep.DEAN,
   167	            decision=ApprovalDecision.PENDING
   168	        ).exists()
   169	        if not has_pending_approval:
   170	            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
   171	                            status=status.HTTP_403_FORBIDDEN)
   172	
   173	    return Response(ApplicationSerializer(application).data)

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/tests/test_serializer_validation.py | sed -n '1,120p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.test import TestCase
     2	from django.utils import timezone
     3	from datetime import timedelta
     4	from apps.applications.serializers import ApplicationCreateSerializer
     5	
     6	
     7	class ApplicationCreateSerializerTest(TestCase):
     8	    def test_reason_max_length_500(self):
     9	        """Test reason field enforces 500 character limit"""
    10	        data = {
    11	            'reason': 'a' * 501,
    12	            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
    13	        }
    14	        serializer = ApplicationCreateSerializer(data=data)
    15	        self.assertFalse(serializer.is_valid())
    16	        self.assertIn('reason', serializer.errors)
    17	
    18	    def test_reason_empty_after_trim(self):
    19	        """Test reason field rejects empty string after trim"""
    20	        data = {
    21	            'reason': '   ',
    22	            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
    23	        }
    24	        serializer = ApplicationCreateSerializer(data=data)
    25	        self.assertFalse(serializer.is_valid())
    26	        self.assertIn('reason', serializer.errors)
    27	
    28	    def test_leave_date_past(self):
    29	        """Test leave_date field rejects dates before today"""
    30	        data = {
    31	            'reason': '毕业离校',
    32	            'leave_date': (timezone.now().date() - timedelta(days=1)).isoformat()
    33	        }
    34	        serializer = ApplicationCreateSerializer(data=data)
    35	        self.assertFalse(serializer.is_valid())
    36	        self.assertIn('leave_date', serializer.errors)
    37	
    38	    def test_leave_date_today(self):
    39	        """Test leave_date field accepts today"""
    40	        data = {
    41	            'reason': '毕业离校',
    42	            'leave_date': timezone.now().date().isoformat()
    43	        }
    44	        serializer = ApplicationCreateSerializer(data=data)
    45	        self.assertTrue(serializer.is_valid())
    46	
    47	    def test_valid_data(self):
    48	        """Test serializer accepts valid data"""
    49	        data = {
    50	            'reason': '毕业离校',
    51	            'leave_date': (timezone.now().date() + timedelta(days=1)).isoformat()
    52	        }
    53	        serializer = ApplicationCreateSerializer(data=data)
    54	        self.assertTrue(serializer.is_valid())
    55	        self.assertEqual(serializer.validated_data['reason'], '毕业离校')

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/models.py | sed -n '1,90p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.db import models
     2	from django.core.exceptions import ValidationError
     3	from apps.users.models import User
     4	
     5	
     6	class ApplicationStatus(models.TextChoices):
     7	    DRAFT = 'draft', '草稿'
     8	    PENDING_COUNSELOR = 'pending_counselor', '待辅导员审批'
     9	    PENDING_DEAN = 'pending_dean', '待学工部审批'
    10	    APPROVED = 'approved', '已通过'
    11	    REJECTED = 'rejected', '已驳回'
    12	
    13	
    14	class DormCheckoutStatus(models.TextChoices):
    15	    COMPLETED = 'completed', '已清退'
    16	    PENDING = 'pending', '清退中'
    17	    NOT_STARTED = 'not_started', '未开始'
    18	    UNKNOWN = 'unknown', '状态未知'
    19	
    20	
    21	class Application(models.Model):
    22	    application_id = models.CharField(max_length=50, primary_key=True)
    23	    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='applications')
    24	    student_name = models.CharField(max_length=100)
    25	    class_id = models.CharField(max_length=50)
    26	    reason = models.TextField()
    27	    leave_date = models.DateField()
    28	    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.DRAFT)
    29	    dorm_checkout_status = models.CharField(max_length=20, choices=DormCheckoutStatus.choices, default=DormCheckoutStatus.NOT_STARTED)
    30	    created_at = models.DateTimeField(auto_now_add=True)
    31	    updated_at = models.DateTimeField(auto_now=True)
    32	
    33	    class Meta:
    34	        db_table = 'applications'
    35	
    36	    def clean(self):
    37	        if self.status in [ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.PENDING_DEAN, ApplicationStatus.APPROVED]:
    38	            existing = Application.objects.filter(
    39	                student=self.student,
    40	                status__in=[ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.PENDING_DEAN, ApplicationStatus.APPROVED]
    41	            ).exclude(application_id=self.application_id).exists()
    42	            if existing:
    43	                raise ValidationError('该学生已有待审批或已通过的申请，不能重复提交')

exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/tests/test_state_machine.py | sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.test import TestCase
     2	from rest_framework.test import APIClient
     3	from rest_framework import status
     4	from apps.users.models import User, UserRole
     5	from apps.applications.models import Application, ApplicationStatus
     6	from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
     7	from apps.users.class_mapping import ClassMapping
     8	
     9	
    10	class ApprovalStateMachineTestCase(TestCase):
    11	    def setUp(self):
    12	        # Create student
    13	        self.student = User.objects.create_user(
    14	            user_id='2020001',
    15	            name='张三',
    16	            role=UserRole.STUDENT,
    17	            class_id='CS2020-01',
    18	            password='2020001'
    19	        )
    20	
    21	        # Create counselor
    22	        self.counselor = User.objects.create_user(
    23	            user_id='T001',
    24	            name='李老师',
    25	            role=UserRole.COUNSELOR,
    26	            password='T001'
    27	        )
    28	
    29	        # Create dean
    30	        self.dean = User.objects.create_user(
    31	            user_id='D001',
    32	            name='赵主任',
    33	            role=UserRole.DEAN,
    34	            password='D001'
    35	        )
    36	
    37	        # Create class mapping
    38	        ClassMapping.objects.create(
    39	            class_id='CS2020-01',
    40	            counselor=self.counselor,
    41	            counselor_name='李老师',
    42	            active=True
    43	        )
    44	
    45	        # Create application
    46	        self.application = Application.objects.create(
    47	            application_id='app_test001',
    48	            student=self.student,
    49	            student_name='张三',
    50	            class_id='CS2020-01',
    51	            reason='测试原因',
    52	            leave_date='2024-06-30',
    53	            status=ApplicationStatus.PENDING_COUNSELOR
    54	        )
    55	
    56	        # Create counselor approval
    57	        self.approval = Approval.objects.create(
    58	            approval_id='apv_test001',
    59	            application=self.application,
    60	            step=ApprovalStep.COUNSELOR,
    61	            approver=self.counselor,
    62	            approver_name='李老师',
    63	            decision=ApprovalDecision.PENDING
    64	        )
    65	
    66	        self.client = APIClient()
    67	
    68	    def test_duplicate_approval_conflict(self):
    69	        """测试重复审批返回409"""
    70	        self.client.force_authenticate(user=self.counselor)
    71	
    72	        # First approval
    73	        response1 = self.client.post(
    74	            f'/api/approvals/{self.approval.approval_id}/approve/',
    75	            {'comment': '同意'},
    76	            format='json'
    77	        )
    78	        self.assertEqual(response1.status_code, status.HTTP_200_OK)
    79	
    80	        # Second approval attempt
    81	        response2 = self.client.post(
    82	            f'/api/approvals/{self.approval.approval_id}/approve/',
    83	            {'comment': '再次同意'},
    84	            format='json'
    85	        )
    86	        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
    87	
    88	    def test_reject_then_repeat_operation_conflict(self):
    89	        """测试驳回后的重复操作返回409"""
    90	        self.client.force_authenticate(user=self.counselor)
    91	
    92	        response1 = self.client.post(
    93	            f'/api/approvals/{self.approval.approval_id}/reject/',
    94	            {'comment': '不同意'},
    95	            format='json'
    96	        )
    97	        self.assertEqual(response1.status_code, status.HTTP_200_OK)
    98	
    99	        response2 = self.client.post(
   100	            f'/api/approvals/{self.approval.approval_id}/reject/',
   101	            {'comment': '再次不同意'},
   102	            format='json'
   103	        )
   104	        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
   105	
   106	    def test_counselor_step_requires_pending_counselor_status(self):
   107	        """测试辅导员审批步骤与申请状态不匹配时返回409"""
   108	        self.application.status = ApplicationStatus.PENDING_DEAN
   109	        self.application.save()
   110	        self.client.force_authenticate(user=self.counselor)
   111	
   112	        approve_response = self.client.post(
   113	            f'/api/approvals/{self.approval.approval_id}/approve/',
   114	            {'comment': '同意'},
   115	            format='json'
   116	        )
   117	        reject_response = self.client.post(
   118	            f'/api/approvals/{self.approval.approval_id}/reject/',
   119	            {'comment': '不同意'},
   120	            format='json'
   121	        )
   122	
   123	        self.assertEqual(approve_response.status_code, status.HTTP_409_CONFLICT)
   124	        self.assertEqual(reject_response.status_code, status.HTTP_409_CONFLICT)
   125	
   126	    def test_dean_step_requires_pending_dean_status(self):
   127	        """测试学工部审批步骤与申请状态不匹配时返回409"""
   128	        self.application.status = ApplicationStatus.APPROVED
   129	        self.application.save()
   130	        dean_approval = Approval.objects.create(
   131	            approval_id='apv_test002',
   132	            application=self.application,
   133	            step=ApprovalStep.DEAN,
   134	            approver=self.dean,
   135	            approver_name='赵主任',
   136	            decision=ApprovalDecision.PENDING
   137	        )
   138	        self.client.force_authenticate(user=self.dean)
   139	
   140	        approve_response = self.client.post(
   141	            f'/api/approvals/{dean_approval.approval_id}/approve/',
   142	            {'comment': '同意'},
   143	            format='json'
   144	        )
   145	        reject_response = self.client.post(
   146	            f'/api/approvals/{dean_approval.approval_id}/reject/',
   147	            {'comment': '不同意'},
   148	            format='json'
   149	        )
   150	
   151	        self.assertEqual(approve_response.status_code, status.HTTP_409_CONFLICT)
   152	        self.assertEqual(reject_response.status_code, status.HTTP_409_CONFLICT)

I have enough context to issue a formal review: the proposal is mostly aligned, but I will narrow the implementation scope against already-covered tests and current code behavior.
  ✓ Load review and collaboration protocols
  ✓ Inspect proposed test coverage response
  ✓ Compare proposal against current implementation/tests
  → Write durable Codex feedback artifact
  • Return consensus recommendation
codex
我会把这轮 Codex 反馈落成一个 collaboration artifact，便于 Claude 直接按最终范围实施；内容会给出通过/需调整的结论和一个削减后的测试清单。
exec
/bin/bash -lc 'rtk date -u +%Y%m%d-%H%M' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
20260601-0405

apply patch
patch: completed
/home/caohui/projects/graduation-leave-system/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
diff --git a/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
new file mode 100644
index 0000000000000000000000000000000000000000..297e3871620c049a4f427d0d43c9493220578115
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
@@ -0,0 +1,80 @@
+# Codex Feedback on Revised Test Coverage Plan
+
+**Created:** 2026-06-01T04:05Z  
+**Reviewer:** Codex  
+**Reviewed artifact:** `.omc/collaboration/artifacts/test-coverage-claude-response.md`
+
+## Review Conclusion
+
+**Decision:** Accept with small scope reductions.
+
+The revised direction is sound: remove duplicate list-isolation tests, align dean permissions with assigned approvals, treat state-machine coverage as sequential API logic rather than real concurrency, and avoid a cross-timezone matrix.
+
+The remaining issue is scope precision. Some proposed state-machine tests describe transitions the current system does not expose or enforce at model level. The executable test plan should verify the API/validator behavior that actually exists today.
+
+## Required Adjustments
+
+### 1. Detail isolation: keep, but align dean semantics
+
+Add focused detail endpoint tests for:
+
+1. Student cannot GET another student's application.
+2. Counselor cannot GET cross-class application.
+3. Dean cannot GET an application without their own pending dean approval.
+
+The dean detail test should explicitly use the current implementation semantics: `get_application` allows dean access only when a pending dean approval exists for that dean. It does not allow access to completed dean approvals.
+
+The `decision=all` approval list leak test is valid, but it belongs in `backend/apps/approvals/tests/test_list_permissions.py`, not a new detail-isolation file.
+
+### 2. State machine: keep sequential tests, reduce duplication
+
+The clarified "sequential, not concurrent" scope matches my recommendation.
+
+Do not implement this as a broad 8-case new matrix file from scratch. Current tests already cover:
+
+- complete approval path in `test_application_flow.py`
+- counselor/dean rejection paths in `test_rejection_flow.py`
+- duplicate approval/reject conflict and step/status mismatch in `test_state_machine.py`
+- cross-role and non-assigned approver checks in `test_permissions.py`
+
+Add only the missing high-value cases:
+
+1. Resubmission after rejection creates a new pending counselor application.
+2. Completed terminal operation protection is covered for duplicate same-decision attempts; add only an opposite-decision terminal check if not already covered by the existing duplicate tests.
+3. Dean approval uniqueness should be tested through the actual API path if feasible, but avoid relying on direct model mutation as the main assertion.
+
+Remove or reword proposed tests such as "draft -> approved" and "pending_counselor -> approved" unless you add a real state-transition validator outside the approval API. Current `Application.clean()` only prevents duplicate active applications; it does not enforce a full transition graph.
+
+### 3. Timezone boundaries: include only as merged serializer tests
+
+Include 2 deterministic serializer tests in `backend/apps/applications/tests/test_serializer_validation.py`:
+
+1. Mock `timezone.now()` at `2026-06-01 23:59:59` Asia/Shanghai and assert `2026-06-02` passes.
+2. Mock `timezone.now()` at `2026-06-02 00:00:01` Asia/Shanghai and assert `2026-06-01` fails.
+
+The existing `test_leave_date_today` and `test_leave_date_past` already cover the generic today/past rules, so a third timezone test is optional and not necessary for this iteration.
+
+## Final Executable Scope
+
+**Core implementation target:**
+
+1. Add `backend/apps/applications/tests/test_detail_permissions.py` with 3 detail GET isolation tests.
+2. Add `decision=all` leak coverage to `backend/apps/approvals/tests/test_list_permissions.py`.
+3. Extend existing state-machine tests only for missing terminal/opposite-decision or resubmission gaps.
+4. Add 2 mocked boundary tests to `test_serializer_validation.py`.
+
+## Time Estimate
+
+**Realistic estimate:** 0.6 day if implemented against existing fixtures and test files.
+
+0.7 day is a safe planning buffer, but not the target. The only way this becomes 0.7+ day is if the implementation creates a new broad matrix test suite instead of extending existing focused files.
+
+If the team must cap at 0.5 day, cut in this order:
+
+1. Drop timezone boundary tests first.
+2. Drop the opposite-decision terminal-state test if duplicate terminal tests already give enough confidence.
+3. Keep detail isolation and `decision=all` leak coverage; those are the highest-value security tests.
+
+## Consensus Recommendation
+
+Proceed with the narrowed scope above. No real concurrency tests and no cross-timezone matrix.

diff --git a/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
new file mode 100644
index 0000000000000000000000000000000000000000..297e3871620c049a4f427d0d43c9493220578115
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
@@ -0,0 +1,80 @@
+# Codex Feedback on Revised Test Coverage Plan
+
+**Created:** 2026-06-01T04:05Z  
+**Reviewer:** Codex  
+**Reviewed artifact:** `.omc/collaboration/artifacts/test-coverage-claude-response.md`
+
+## Review Conclusion
+
+**Decision:** Accept with small scope reductions.
+
+The revised direction is sound: remove duplicate list-isolation tests, align dean permissions with assigned approvals, treat state-machine coverage as sequential API logic rather than real concurrency, and avoid a cross-timezone matrix.
+
+The remaining issue is scope precision. Some proposed state-machine tests describe transitions the current system does not expose or enforce at model level. The executable test plan should verify the API/validator behavior that actually exists today.
+
+## Required Adjustments
+
+### 1. Detail isolation: keep, but align dean semantics
+
+Add focused detail endpoint tests for:
+
+1. Student cannot GET another student's application.
+2. Counselor cannot GET cross-class application.
+3. Dean cannot GET an application without their own pending dean approval.
+
+The dean detail test should explicitly use the current implementation semantics: `get_application` allows dean access only when a pending dean approval exists for that dean. It does not allow access to completed dean approvals.
+
+The `decision=all` approval list leak test is valid, but it belongs in `backend/apps/approvals/tests/test_list_permissions.py`, not a new detail-isolation file.
+
+### 2. State machine: keep sequential tests, reduce duplication
+
+The clarified "sequential, not concurrent" scope matches my recommendation.
+
+Do not implement this as a broad 8-case new matrix file from scratch. Current tests already cover:
+
+- complete approval path in `test_application_flow.py`
+- counselor/dean rejection paths in `test_rejection_flow.py`
+- duplicate approval/reject conflict and step/status mismatch in `test_state_machine.py`
+- cross-role and non-assigned approver checks in `test_permissions.py`
+
+Add only the missing high-value cases:
+
+1. Resubmission after rejection creates a new pending counselor application.
+2. Completed terminal operation protection is covered for duplicate same-decision attempts; add only an opposite-decision terminal check if not already covered by the existing duplicate tests.
+3. Dean approval uniqueness should be tested through the actual API path if feasible, but avoid relying on direct model mutation as the main assertion.
+
+Remove or reword proposed tests such as "draft -> approved" and "pending_counselor -> approved" unless you add a real state-transition validator outside the approval API. Current `Application.clean()` only prevents duplicate active applications; it does not enforce a full transition graph.
+
+### 3. Timezone boundaries: include only as merged serializer tests
+
+Include 2 deterministic serializer tests in `backend/apps/applications/tests/test_serializer_validation.py`:
+
+1. Mock `timezone.now()` at `2026-06-01 23:59:59` Asia/Shanghai and assert `2026-06-02` passes.
+2. Mock `timezone.now()` at `2026-06-02 00:00:01` Asia/Shanghai and assert `2026-06-01` fails.
+
+The existing `test_leave_date_today` and `test_leave_date_past` already cover the generic today/past rules, so a third timezone test is optional and not necessary for this iteration.
+
+## Final Executable Scope
+
+**Core implementation target:**
+
+1. Add `backend/apps/applications/tests/test_detail_permissions.py` with 3 detail GET isolation tests.
+2. Add `decision=all` leak coverage to `backend/apps/approvals/tests/test_list_permissions.py`.
+3. Extend existing state-machine tests only for missing terminal/opposite-decision or resubmission gaps.
+4. Add 2 mocked boundary tests to `test_serializer_validation.py`.
+
+## Time Estimate
+
+**Realistic estimate:** 0.6 day if implemented against existing fixtures and test files.
+
+0.7 day is a safe planning buffer, but not the target. The only way this becomes 0.7+ day is if the implementation creates a new broad matrix test suite instead of extending existing focused files.
+
+If the team must cap at 0.5 day, cut in this order:
+
+1. Drop timezone boundary tests first.
+2. Drop the opposite-decision terminal-state test if duplicate terminal tests already give enough confidence.
+3. Keep detail isolation and `decision=all` leak coverage; those are the highest-value security tests.
+
+## Consensus Recommendation
+
+Proceed with the narrowed scope above. No real concurrency tests and no cross-timezone matrix.

codex
反馈 artifact 已创建。接下来我会按 collaboration 协议记录一个 artifact_created 事件并更新共享状态，保证后续实施方能从事件流发现这轮结论。
exec
/bin/bash -lc 'rtk tail -20 .omc/collaboration/events.jsonl' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{"id":53,"type":"consensus_reached","agent":"codex","timestamp":"2026-05-30T15:48:34.202176Z","summary":"Codex accepted Claude Task #3 details for agent lifecycle events, permission changes, and read-only artifact scope.","task_id":"TASK-20260530-06","artifacts":[".omc/collaboration/artifacts/20260530-2347-codex-agent-lifecycle-consensus.md"],"status":"waiting","details":{"agent_joined_left_category":"INFO_EVENTS","agent_permission_changed_category":"INFO_EVENTS","permission_change_requires_reason":true,"core_agent_downgrade_forbidden":["claude","codex"],"read_only_artifact_root":".omc/collaboration/artifacts/{agent}/"}}
{"id":54,"type":"consensus_reached","agent":"codex","timestamp":"2026-05-30T16:03:08.347726Z","summary":"Codex recorded Task #4 consensus for the Phase 1a minimal validation script and confirmed implementation readiness.","task_id":"TASK-20260530-06","artifacts":[".omc/collaboration/task-4-consensus.md"],"status":"waiting","details":{"phase1a_checks":["journal-basic","registry","legacy-events","state-schema","behavioral-smoke"],"architecture":"thin Bash entrypoint with Python core logic","legacy_cutoff":"dynamic, not hardcoded","implementation_ready":true}}
{"id":55,"type":"consensus_reached","agent":"claude","timestamp":"2026-05-30T16:34:35.847Z","summary":"Phase 1b implementation consensus reached after 3-round discussion","task_id":"TASK-20260530-06","artifacts":[".omc/collaboration/phase1b-implementation-consensus.md"],"details":{"discussion_rounds":3,"key_decisions":["Phase A-E layered gates","Unify script entry first (P0)","Dynamic cutoff calculation","State fork decision before Phase B","Manual consensus event append"]}}
{"id":56,"type":"review_response","agent":"codex","timestamp":"2026-05-30T17:07:46.182Z","summary":"Codex approved the revised Step 2 implementation plan and confirmed execution readiness.","task_id":"TASK-20260530-06","artifacts":["docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md"],"status":"waiting","details":{"decision":"agree_to_execute","blockers":[],"non_blocking_notes":["Validate both offset=0 and offset=5 during execution.","Global DRF exception handler is only needed if framework-level errors must use the business error envelope."]}}
{"id": 57, "type": "completed", "agent": "codex", "timestamp": "2026-05-30T18:13:50.735455+00:00", "summary": "Step 5 full backend validation passed and approval list serializer fix committed.", "task_id": "TASK-20260530-06", "artifacts": ["3e429d9", "backend/apps/approvals/serializers.py"], "status": "completed"}
{"id": 58, "type": "completed", "agent": "codex", "timestamp": "2026-05-30T19:43:02.938242+00:00", "summary": "Codex completed critical analysis of completion boundary and recommended path5: short closure then return to Week 3 core workflow.", "task_id": "TASK-20260530-06", "artifacts": [".omc/collaboration/artifacts/20260530-1942-codex-completion-boundary-analysis.md"], "status": "completed"}
{"id":59,"type":"consensus_reached","agent":"codex","timestamp":"2026-05-30T20:06:51.294193+00:00","summary":"Codex accepted Option B hybrid Week 3 closure plan and began execution.","task_id":"TASK-20260530-06","artifacts":[".omc/collaboration/artifacts/20260531-0405-codex-week3-consensus-response.md"],"status":"in_progress","details":{"option":"B","p0_security_tests":true,"state_validator":"focused reusable validator plus tests","time_target_hours":"5.5-6","hard_stop_hours":"6.5 unless P0 regression found"}}
{"id":60,"type":"completed","agent":"codex","timestamp":"2026-05-30T20:15:41.420045+00:00","summary":"Codex completed Week 3 closure execution: P0 security/state coverage, v0.2 contract, and type/mock alignment validated.","task_id":"TASK-20260530-06","artifacts":[".omc/collaboration/artifacts/20260531-0405-codex-week3-consensus-response.md",".omc/collaboration/artifacts/20260531-0415-codex-week3-execution-summary.md","docs/contracts/contract-v0.2.md"],"status":"completed","details":{"tests":{"approval_targeted":"10 tests OK","backend_explicit_modules":"37 tests OK","django_check":"passed"},"notes":["Host Python lacks Django; Docker backend was used.","No frontend package/tsconfig exists for TypeScript check.","Existing unrelated worktree changes preserved."]}}
{"id":61,"type":"strategy_proposed","agent":"codex","timestamp":"2026-05-30T20:22:51.791419Z","summary":"Codex proposed next-phase strategy: miniprogram-first vertical slice plus attachments MVP, with DevTools as completion gate.","artifacts":[".omc/collaboration/artifacts/20260531-0421-codex-next-phase-strategy.md"],"status":"completed","details":{"recommendation":"B-first hybrid","include_now":["miniprogram UI/API vertical slice","attachments MVP"],"defer":["draft save","full audit trail","real dorm provider","Redis/load testing","React Native"]}}
{"id":62,"type":"review_response","agent":"codex","timestamp":"2026-05-30T20:27:17.531472Z","summary":"Codex accepted Claude validation-first challenge, narrowed MVP scope, and revised next-phase ordering.","artifacts":[".omc/collaboration/artifacts/20260531-0425-codex-response-to-claude-next-phase-strategy.md"],"status":"waiting","details":{"decision":"accept_validation_first_with_bounded_fallback","mvp_scope":"miniprogram minimal happy path: login, student application, shared approvals, shared detail","attachments":"after basic DevTools/API validation and narrow client MVP","react_native":"deferred for next phase pending stakeholder confirmation","dorm_provider":"start discovery immediately; production blocked on real integration or approved fallback"}}
{"id":63,"type":"review_response","agent":"codex","timestamp":"2026-05-30T20:42:05.045476Z","summary":"Codex analyzed Week 4 blocked preparation options and recommended a bounded low-rework A/C/E readiness bundle.","artifacts":[".omc/collaboration/artifacts/20260531-0439-codex-week4-blocked-prep-analysis.md"],"status":"waiting","details":{"recommendation":"bundle_A_C_E_plus_dependency_closure_pack","defer":["detailed_4_page_architecture","real_dorm_adapter_implementation","attachments_or_new_ui_expansion"],"decision_criteria":["shortens_phase_4A","survives_devtools_outcome","does_not_require_unknown_external_contracts","produces_durable_evidence","reveals_blockers_early"]}}
{"id":64,"type":"review_response","agent":"claude","timestamp":"2026-05-30T20:50:18.106123Z","summary":"Claude critically reviewed Codex prep bundle, proposed 3 modifications: immediate stale fix, 3 separate docs, tighter timebox.","artifacts":[".omc/collaboration/artifacts/20260530-2048-claude-response-codex-prep-analysis.md"],"status":"waiting","details":{"agreement":"A_C_E_bundle_strategy","challenges":["stale_fix_should_be_immediate","separate_docs_vs_unified","document_vs_fix_gaps"],"proposed_timebox":"1.75-2.5h","open_questions":3}}
{"id":65,"type":"review_response","agent":"codex","timestamp":"2026-05-30T20:54:48.860683579Z","summary":"Codex accepted Claude Week 4 prep modifications with artifact path counter-modification and fixed stale provider reference.","artifacts":[".omc/collaboration/artifacts/20260530-2053-codex-response-to-claude-week4-prep.md",".omc/collaboration/artifacts/20260531-0445-dorm-provider-discovery.md"],"status":"waiting","details":{"accepted":["immediate_stale_reference_fix","three_focused_prep_docs","document_only_for_unvalidated_miniprogram_gaps","two_point_five_hour_hard_stop"],"counter_modification":"Place the three prep docs under .omc/collaboration/artifacts/ per collaboration protocol instead of .omc/ root.","stale_fix":"backend/apps/applications/dorm_provider.py -> backend/apps/applications/providers.py"}}
{"id":66,"type":"execution_complete","agent":"claude","timestamp":"2026-05-30T21:02:00.000Z","summary":"Claude completed Week 4 prep bundle: created 3 focused prep docs under .omc/collaboration/artifacts/","artifacts":[".omc/collaboration/artifacts/phase4a-validation-checklist.md",".omc/collaboration/artifacts/phase4a-devtools-setup.md",".omc/collaboration/artifacts/phase4b-skeleton-gaps.md"],"status":"complete","details":{"completed_items":["moved_validation_checklist_to_correct_location","created_devtools_setup_guide","created_skeleton_gap_audit"],"timebox":"2.5h hard stop","scope":"document_only_no_fixes"}}
{"id":67,"type":"consensus_reached","agent":"codex","timestamp":"2026-05-31T03:13:05.311150Z","summary":"Codex confirmed Claude Phase 4A readiness repair plan with runtime-verification and collaboration-bookkeeping amendments.","artifacts":[".omc/collaboration/artifacts/20260531-0320-codex-readiness-repair-confirmation.md"],"status":"waiting","details":{"decision":"proceed_with_amendments","mandatory_steps":["verify_current_state","fix_validation_checklist","fix_skeleton_gaps"],"optional_steps":["dorm_system_stakeholder_request"],"hard_stop_minutes":90}}
{"id":68,"type":"task_start","agent":"claude","timestamp":"2026-05-31T03:20:00.000Z","summary":"Claude starting Phase 4A readiness repair pass (Codex amendments accepted)","artifacts":[".omc/collaboration/artifacts/20260531-0310-claude-response-readiness-repair.md",".omc/collaboration/artifacts/20260531-0320-codex-readiness-repair-confirmation.md"],"status":"in_progress","details":{"amendments":["runtime_backed_verification","collaboration_bookkeeping"],"steps":["verify_current_state","fix_validation_checklist","fix_skeleton_gaps","optional_dorm_request"],"timebox":"60min target, 90min hard stop"}}
{"id":69,"type":"task_complete","agent":"claude","timestamp":"2026-05-31T03:35:00.000Z","summary":"Phase 4A readiness repair complete - fixed 4 issues in prep docs","artifacts":[".omc/collaboration/artifacts/20260531-0325-step1-verification-results.md",".omc/collaboration/artifacts/phase4a-validation-checklist.md",".omc/collaboration/artifacts/phase4b-skeleton-gaps.md",".omc/collaboration/artifacts/dorm-system-stakeholder-request.md"],"status":"complete","details":{"issues_fixed":["stale_test_accounts","wrong_401_scenario","stale_skeleton_gaps","student_redirect_bug"],"verification":"runtime_backed","steps_completed":["verify_current_state","fix_validation_checklist","fix_skeleton_gaps","create_dorm_request"]}}
{"id":70,"type":"verification_complete","agent":"claude","timestamp":"2026-05-31T03:40:00.000Z","summary":"Read-only Phase 4B prep verification complete - confirmed architecture, identified optimizations","artifacts":[".omc/collaboration/artifacts/phase4b-prep-note.md"],"status":"complete","details":{"verified":["api_ts_used_by_all_pages","types_ts_used_by_pages","page_registration_correct"],"optimizations":["centralize_api_client_config","role_based_routing","refine_409_test"],"duplication":"each_page_instantiates_own_api_client"}}
{"id":71,"type":"blocked","agent":"codex","timestamp":"2026-05-31T03:56:52.552Z","summary":"Final consensus challenge found and fixed stale Phase 4 handoff docs; remaining work is blocked on WeChat DevTools evidence.","task_id":"phase4a_waiting_for_devtools","artifacts":[".omc/collaboration/artifacts/phase4a-devtools-setup.md",".omc/collaboration/artifacts/phase4b-prep-note.md",".omc/collaboration/artifacts/phase4b-skeleton-gaps.md",".omc/collaboration/artifacts/blocked-waiting-for-devtools.md"],"status":"blocked","details":{"answer":"C_then_A","missed_items_fixed":["stale DevTools setup login credential","stale ApiClient config snippet","stale shared API/types verification status"],"remaining_blocker":"WeChat DevTools installation/execution evidence"}}
{"id":72,"type":"blocker_removed","agent":"claude","timestamp":"2026-06-01T01:36:41.719650177Z","task_id":"phase4b_implementation","summary":"Phase 4B implementation unblocked after Codex review consensus","status":"in_progress","details":{"reason":"Codex review confirmed Phase 4A blocker was over-cautious","artifacts":[".omc/artifacts/ask/codex-phase-4a-blocked-on-phase4a-waiting-for-devtools-phase-4b-ph-2026-06-01T01-33-23-790Z.md",".omc/collaboration/artifacts/20260601-0135-claude-response-phase4a-blocker-challenge.md"],"p0_fix":"Fixed form fields in phase4b-skeleton-gaps.md (reason+leave_date)","scope":"student-application page + role routing + API centralization"}}

exec
/bin/bash -lc 'rtk python -m json.tool .omc/collaboration/state.json' in /home/caohui/projects/graduation-leave-system
 exited 127 in 0ms:
[rtk: No such file or directory (os error 2)]

diff --git a/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
new file mode 100644
index 0000000000000000000000000000000000000000..297e3871620c049a4f427d0d43c9493220578115
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
@@ -0,0 +1,80 @@
+# Codex Feedback on Revised Test Coverage Plan
+
+**Created:** 2026-06-01T04:05Z  
+**Reviewer:** Codex  
+**Reviewed artifact:** `.omc/collaboration/artifacts/test-coverage-claude-response.md`
+
+## Review Conclusion
+
+**Decision:** Accept with small scope reductions.
+
+The revised direction is sound: remove duplicate list-isolation tests, align dean permissions with assigned approvals, treat state-machine coverage as sequential API logic rather than real concurrency, and avoid a cross-timezone matrix.
+
+The remaining issue is scope precision. Some proposed state-machine tests describe transitions the current system does not expose or enforce at model level. The executable test plan should verify the API/validator behavior that actually exists today.
+
+## Required Adjustments
+
+### 1. Detail isolation: keep, but align dean semantics
+
+Add focused detail endpoint tests for:
+
+1. Student cannot GET another student's application.
+2. Counselor cannot GET cross-class application.
+3. Dean cannot GET an application without their own pending dean approval.
+
+The dean detail test should explicitly use the current implementation semantics: `get_application` allows dean access only when a pending dean approval exists for that dean. It does not allow access to completed dean approvals.
+
+The `decision=all` approval list leak test is valid, but it belongs in `backend/apps/approvals/tests/test_list_permissions.py`, not a new detail-isolation file.
+
+### 2. State machine: keep sequential tests, reduce duplication
+
+The clarified "sequential, not concurrent" scope matches my recommendation.
+
+Do not implement this as a broad 8-case new matrix file from scratch. Current tests already cover:
+
+- complete approval path in `test_application_flow.py`
+- counselor/dean rejection paths in `test_rejection_flow.py`
+- duplicate approval/reject conflict and step/status mismatch in `test_state_machine.py`
+- cross-role and non-assigned approver checks in `test_permissions.py`
+
+Add only the missing high-value cases:
+
+1. Resubmission after rejection creates a new pending counselor application.
+2. Completed terminal operation protection is covered for duplicate same-decision attempts; add only an opposite-decision terminal check if not already covered by the existing duplicate tests.
+3. Dean approval uniqueness should be tested through the actual API path if feasible, but avoid relying on direct model mutation as the main assertion.
+
+Remove or reword proposed tests such as "draft -> approved" and "pending_counselor -> approved" unless you add a real state-transition validator outside the approval API. Current `Application.clean()` only prevents duplicate active applications; it does not enforce a full transition graph.
+
+### 3. Timezone boundaries: include only as merged serializer tests
+
+Include 2 deterministic serializer tests in `backend/apps/applications/tests/test_serializer_validation.py`:
+
+1. Mock `timezone.now()` at `2026-06-01 23:59:59` Asia/Shanghai and assert `2026-06-02` passes.
+2. Mock `timezone.now()` at `2026-06-02 00:00:01` Asia/Shanghai and assert `2026-06-01` fails.
+
+The existing `test_leave_date_today` and `test_leave_date_past` already cover the generic today/past rules, so a third timezone test is optional and not necessary for this iteration.
+
+## Final Executable Scope
+
+**Core implementation target:**
+
+1. Add `backend/apps/applications/tests/test_detail_permissions.py` with 3 detail GET isolation tests.
+2. Add `decision=all` leak coverage to `backend/apps/approvals/tests/test_list_permissions.py`.
+3. Extend existing state-machine tests only for missing terminal/opposite-decision or resubmission gaps.
+4. Add 2 mocked boundary tests to `test_serializer_validation.py`.
+
+## Time Estimate
+
+**Realistic estimate:** 0.6 day if implemented against existing fixtures and test files.
+
+0.7 day is a safe planning buffer, but not the target. The only way this becomes 0.7+ day is if the implementation creates a new broad matrix test suite instead of extending existing focused files.
+
+If the team must cap at 0.5 day, cut in this order:
+
+1. Drop timezone boundary tests first.
+2. Drop the opposite-decision terminal-state test if duplicate terminal tests already give enough confidence.
+3. Keep detail isolation and `decision=all` leak coverage; those are the highest-value security tests.
+
+## Consensus Recommendation
+
+Proceed with the narrowed scope above. No real concurrency tests and no cross-timezone matrix.

exec
/bin/bash -lc 'rtk which python3' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
/usr/bin/python3

exec
/bin/bash -lc 'rtk python3 -m json.tool .omc/collaboration/state.json' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{
    "workflow_id": "claude-codex-collab-mvp",
    "current_task": "phase4b_implementation",
    "active_agent": "claude",
    "status": "in_progress",
    "last_event_id": 72,
    "updated_at": "2026-06-01T01:36:54.816207573Z"
}

diff --git a/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
new file mode 100644
index 0000000000000000000000000000000000000000..297e3871620c049a4f427d0d43c9493220578115
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
@@ -0,0 +1,80 @@
+# Codex Feedback on Revised Test Coverage Plan
+
+**Created:** 2026-06-01T04:05Z  
+**Reviewer:** Codex  
+**Reviewed artifact:** `.omc/collaboration/artifacts/test-coverage-claude-response.md`
+
+## Review Conclusion
+
+**Decision:** Accept with small scope reductions.
+
+The revised direction is sound: remove duplicate list-isolation tests, align dean permissions with assigned approvals, treat state-machine coverage as sequential API logic rather than real concurrency, and avoid a cross-timezone matrix.
+
+The remaining issue is scope precision. Some proposed state-machine tests describe transitions the current system does not expose or enforce at model level. The executable test plan should verify the API/validator behavior that actually exists today.
+
+## Required Adjustments
+
+### 1. Detail isolation: keep, but align dean semantics
+
+Add focused detail endpoint tests for:
+
+1. Student cannot GET another student's application.
+2. Counselor cannot GET cross-class application.
+3. Dean cannot GET an application without their own pending dean approval.
+
+The dean detail test should explicitly use the current implementation semantics: `get_application` allows dean access only when a pending dean approval exists for that dean. It does not allow access to completed dean approvals.
+
+The `decision=all` approval list leak test is valid, but it belongs in `backend/apps/approvals/tests/test_list_permissions.py`, not a new detail-isolation file.
+
+### 2. State machine: keep sequential tests, reduce duplication
+
+The clarified "sequential, not concurrent" scope matches my recommendation.
+
+Do not implement this as a broad 8-case new matrix file from scratch. Current tests already cover:
+
+- complete approval path in `test_application_flow.py`
+- counselor/dean rejection paths in `test_rejection_flow.py`
+- duplicate approval/reject conflict and step/status mismatch in `test_state_machine.py`
+- cross-role and non-assigned approver checks in `test_permissions.py`
+
+Add only the missing high-value cases:
+
+1. Resubmission after rejection creates a new pending counselor application.
+2. Completed terminal operation protection is covered for duplicate same-decision attempts; add only an opposite-decision terminal check if not already covered by the existing duplicate tests.
+3. Dean approval uniqueness should be tested through the actual API path if feasible, but avoid relying on direct model mutation as the main assertion.
+
+Remove or reword proposed tests such as "draft -> approved" and "pending_counselor -> approved" unless you add a real state-transition validator outside the approval API. Current `Application.clean()` only prevents duplicate active applications; it does not enforce a full transition graph.
+
+### 3. Timezone boundaries: include only as merged serializer tests
+
+Include 2 deterministic serializer tests in `backend/apps/applications/tests/test_serializer_validation.py`:
+
+1. Mock `timezone.now()` at `2026-06-01 23:59:59` Asia/Shanghai and assert `2026-06-02` passes.
+2. Mock `timezone.now()` at `2026-06-02 00:00:01` Asia/Shanghai and assert `2026-06-01` fails.
+
+The existing `test_leave_date_today` and `test_leave_date_past` already cover the generic today/past rules, so a third timezone test is optional and not necessary for this iteration.
+
+## Final Executable Scope
+
+**Core implementation target:**
+
+1. Add `backend/apps/applications/tests/test_detail_permissions.py` with 3 detail GET isolation tests.
+2. Add `decision=all` leak coverage to `backend/apps/approvals/tests/test_list_permissions.py`.
+3. Extend existing state-machine tests only for missing terminal/opposite-decision or resubmission gaps.
+4. Add 2 mocked boundary tests to `test_serializer_validation.py`.
+
+## Time Estimate
+
+**Realistic estimate:** 0.6 day if implemented against existing fixtures and test files.
+
+0.7 day is a safe planning buffer, but not the target. The only way this becomes 0.7+ day is if the implementation creates a new broad matrix test suite instead of extending existing focused files.
+
+If the team must cap at 0.5 day, cut in this order:
+
+1. Drop timezone boundary tests first.
+2. Drop the opposite-decision terminal-state test if duplicate terminal tests already give enough confidence.
+3. Keep detail isolation and `decision=all` leak coverage; those are the highest-value security tests.
+
+## Consensus Recommendation
+
+Proceed with the narrowed scope above. No real concurrency tests and no cross-timezone matrix.

exec
/bin/bash -lc 'rtk mkdir .omc/collaboration/locks/journal.lock' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
diff --git a/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
new file mode 100644
index 0000000000000000000000000000000000000000..297e3871620c049a4f427d0d43c9493220578115
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
@@ -0,0 +1,80 @@
+# Codex Feedback on Revised Test Coverage Plan
+
+**Created:** 2026-06-01T04:05Z  
+**Reviewer:** Codex  
+**Reviewed artifact:** `.omc/collaboration/artifacts/test-coverage-claude-response.md`
+
+## Review Conclusion
+
+**Decision:** Accept with small scope reductions.
+
+The revised direction is sound: remove duplicate list-isolation tests, align dean permissions with assigned approvals, treat state-machine coverage as sequential API logic rather than real concurrency, and avoid a cross-timezone matrix.
+
+The remaining issue is scope precision. Some proposed state-machine tests describe transitions the current system does not expose or enforce at model level. The executable test plan should verify the API/validator behavior that actually exists today.
+
+## Required Adjustments
+
+### 1. Detail isolation: keep, but align dean semantics
+
+Add focused detail endpoint tests for:
+
+1. Student cannot GET another student's application.
+2. Counselor cannot GET cross-class application.
+3. Dean cannot GET an application without their own pending dean approval.
+
+The dean detail test should explicitly use the current implementation semantics: `get_application` allows dean access only when a pending dean approval exists for that dean. It does not allow access to completed dean approvals.
+
+The `decision=all` approval list leak test is valid, but it belongs in `backend/apps/approvals/tests/test_list_permissions.py`, not a new detail-isolation file.
+
+### 2. State machine: keep sequential tests, reduce duplication
+
+The clarified "sequential, not concurrent" scope matches my recommendation.
+
+Do not implement this as a broad 8-case new matrix file from scratch. Current tests already cover:
+
+- complete approval path in `test_application_flow.py`
+- counselor/dean rejection paths in `test_rejection_flow.py`
+- duplicate approval/reject conflict and step/status mismatch in `test_state_machine.py`
+- cross-role and non-assigned approver checks in `test_permissions.py`
+
+Add only the missing high-value cases:
+
+1. Resubmission after rejection creates a new pending counselor application.
+2. Completed terminal operation protection is covered for duplicate same-decision attempts; add only an opposite-decision terminal check if not already covered by the existing duplicate tests.
+3. Dean approval uniqueness should be tested through the actual API path if feasible, but avoid relying on direct model mutation as the main assertion.
+
+Remove or reword proposed tests such as "draft -> approved" and "pending_counselor -> approved" unless you add a real state-transition validator outside the approval API. Current `Application.clean()` only prevents duplicate active applications; it does not enforce a full transition graph.
+
+### 3. Timezone boundaries: include only as merged serializer tests
+
+Include 2 deterministic serializer tests in `backend/apps/applications/tests/test_serializer_validation.py`:
+
+1. Mock `timezone.now()` at `2026-06-01 23:59:59` Asia/Shanghai and assert `2026-06-02` passes.
+2. Mock `timezone.now()` at `2026-06-02 00:00:01` Asia/Shanghai and assert `2026-06-01` fails.
+
+The existing `test_leave_date_today` and `test_leave_date_past` already cover the generic today/past rules, so a third timezone test is optional and not necessary for this iteration.
+
+## Final Executable Scope
+
+**Core implementation target:**
+
+1. Add `backend/apps/applications/tests/test_detail_permissions.py` with 3 detail GET isolation tests.
+2. Add `decision=all` leak coverage to `backend/apps/approvals/tests/test_list_permissions.py`.
+3. Extend existing state-machine tests only for missing terminal/opposite-decision or resubmission gaps.
+4. Add 2 mocked boundary tests to `test_serializer_validation.py`.
+
+## Time Estimate
+
+**Realistic estimate:** 0.6 day if implemented against existing fixtures and test files.
+
+0.7 day is a safe planning buffer, but not the target. The only way this becomes 0.7+ day is if the implementation creates a new broad matrix test suite instead of extending existing focused files.
+
+If the team must cap at 0.5 day, cut in this order:
+
+1. Drop timezone boundary tests first.
+2. Drop the opposite-decision terminal-state test if duplicate terminal tests already give enough confidence.
+3. Keep detail isolation and `decision=all` leak coverage; those are the highest-value security tests.
+
+## Consensus Recommendation
+
+Proceed with the narrowed scope above. No real concurrency tests and no cross-timezone matrix.

exec
/bin/bash -lc "rtk python3 -c 'import json, pathlib, datetime, os, tempfile; base=pathlib.Path(\".omc/collaboration\"); lock=base/\"locks\"/\"journal.lock\"; now=datetime.datetime.now(datetime.timezone.utc).isoformat().replace(\"+00:00\",\"Z\"); (lock/\"owner.json\").write_text(json.dumps({\"agent\":\"codex\",\"task_id\":\"phase4b_implementation\",\"created_at\":now,\"heartbeat_at\":now,\"reason\":\"record Codex test coverage feedback artifact\"}, ensure_ascii=False, separators=(\",\",\":\")), encoding=\"utf-8\"); events=base/\"events.jsonl\"; ids=[]; lines=events.read_text(encoding=\"utf-8\").splitlines(); [ids.append(json.loads(line)[\"id\"]) for line in lines if line.strip()]; eid=max(ids)+1 if ids else 1; event={\"id\":eid,\"type\":\"review_response\",\"agent\":\"codex\",\"timestamp\":now,\"summary\":\"Codex reviewed Claude revised test coverage plan and accepted it with narrowed executable scope.\",\"task_id\":\"phase4b_implementation\",\"artifacts\":[\".omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md\"],\"status\":\"in_progress\",\"details\":{\"decision\":\"accept_with_scope_reductions\",\"time_estimate\":\"0.6 day target, 0.7 day buffer\",\"include_timezone\":\"merge two deterministic serializer boundary tests\",\"state_machine_scope\":\"sequential API logic only, no real concurrency\"}}; existing=events.read_text(encoding=\"utf-8\"); events.write_text(existing + json.dumps(event, ensure_ascii=False, separators=(\",\",\":\")) + \"\\n\", encoding=\"utf-8\"); state_path=base/\"state.json\"; state=json.loads(state_path.read_text(encoding=\"utf-8\")); state.update({\"current_task\":\"phase4b_implementation\",\"active_agent\":\"claude\",\"status\":\"in_progress\",\"last_event_id\":eid,\"updated_at\":now}); tmp=base/\"state.json.tmp.codex\"; tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2)+\"\\n\", encoding=\"utf-8\"); json.loads(tmp.read_text(encoding=\"utf-8\")); os.replace(tmp, state_path); [json.loads(line) for line in events.read_text(encoding=\"utf-8\").splitlines() if line.strip()]; assert json.loads(state_path.read_text(encoding=\"utf-8\"))[\"last_event_id\"] == max(json.loads(line)[\"id\"] for line in events.read_text(encoding=\"utf-8\").splitlines() if line.strip()); print(eid)'" in /home/caohui/projects/graduation-leave-system
diff --git a/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
new file mode 100644
index 0000000000000000000000000000000000000000..297e3871620c049a4f427d0d43c9493220578115
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
@@ -0,0 +1,80 @@
+# Codex Feedback on Revised Test Coverage Plan
+
+**Created:** 2026-06-01T04:05Z  
+**Reviewer:** Codex  
+**Reviewed artifact:** `.omc/collaboration/artifacts/test-coverage-claude-response.md`
+
+## Review Conclusion
+
+**Decision:** Accept with small scope reductions.
+
+The revised direction is sound: remove duplicate list-isolation tests, align dean permissions with assigned approvals, treat state-machine coverage as sequential API logic rather than real concurrency, and avoid a cross-timezone matrix.
+
+The remaining issue is scope precision. Some proposed state-machine tests describe transitions the current system does not expose or enforce at model level. The executable test plan should verify the API/validator behavior that actually exists today.
+
+## Required Adjustments
+
+### 1. Detail isolation: keep, but align dean semantics
+
+Add focused detail endpoint tests for:
+
+1. Student cannot GET another student's application.
+2. Counselor cannot GET cross-class application.
+3. Dean cannot GET an application without their own pending dean approval.
+
+The dean detail test should explicitly use the current implementation semantics: `get_application` allows dean access only when a pending dean approval exists for that dean. It does not allow access to completed dean approvals.
+
+The `decision=all` approval list leak test is valid, but it belongs in `backend/apps/approvals/tests/test_list_permissions.py`, not a new detail-isolation file.
+
+### 2. State machine: keep sequential tests, reduce duplication
+
+The clarified "sequential, not concurrent" scope matches my recommendation.
+
+Do not implement this as a broad 8-case new matrix file from scratch. Current tests already cover:
+
+- complete approval path in `test_application_flow.py`
+- counselor/dean rejection paths in `test_rejection_flow.py`
+- duplicate approval/reject conflict and step/status mismatch in `test_state_machine.py`
+- cross-role and non-assigned approver checks in `test_permissions.py`
+
+Add only the missing high-value cases:
+
+1. Resubmission after rejection creates a new pending counselor application.
+2. Completed terminal operation protection is covered for duplicate same-decision attempts; add only an opposite-decision terminal check if not already covered by the existing duplicate tests.
+3. Dean approval uniqueness should be tested through the actual API path if feasible, but avoid relying on direct model mutation as the main assertion.
+
+Remove or reword proposed tests such as "draft -> approved" and "pending_counselor -> approved" unless you add a real state-transition validator outside the approval API. Current `Application.clean()` only prevents duplicate active applications; it does not enforce a full transition graph.
+
+### 3. Timezone boundaries: include only as merged serializer tests
+
+Include 2 deterministic serializer tests in `backend/apps/applications/tests/test_serializer_validation.py`:
+
+1. Mock `timezone.now()` at `2026-06-01 23:59:59` Asia/Shanghai and assert `2026-06-02` passes.
+2. Mock `timezone.now()` at `2026-06-02 00:00:01` Asia/Shanghai and assert `2026-06-01` fails.
+
+The existing `test_leave_date_today` and `test_leave_date_past` already cover the generic today/past rules, so a third timezone test is optional and not necessary for this iteration.
+
+## Final Executable Scope
+
+**Core implementation target:**
+
+1. Add `backend/apps/applications/tests/test_detail_permissions.py` with 3 detail GET isolation tests.
+2. Add `decision=all` leak coverage to `backend/apps/approvals/tests/test_list_permissions.py`.
+3. Extend existing state-machine tests only for missing terminal/opposite-decision or resubmission gaps.
+4. Add 2 mocked boundary tests to `test_serializer_validation.py`.
+
+## Time Estimate
+
+**Realistic estimate:** 0.6 day if implemented against existing fixtures and test files.
+
+0.7 day is a safe planning buffer, but not the target. The only way this becomes 0.7+ day is if the implementation creates a new broad matrix test suite instead of extending existing focused files.
+
+If the team must cap at 0.5 day, cut in this order:
+
+1. Drop timezone boundary tests first.
+2. Drop the opposite-decision terminal-state test if duplicate terminal tests already give enough confidence.
+3. Keep detail isolation and `decision=all` leak coverage; those are the highest-value security tests.
+
+## Consensus Recommendation
+
+Proceed with the narrowed scope above. No real concurrency tests and no cross-timezone matrix.

 succeeded in 145ms:
73

exec
/bin/bash -lc 'rtk rm -r .omc/collaboration/locks/journal.lock' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
diff --git a/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
new file mode 100644
index 0000000000000000000000000000000000000000..297e3871620c049a4f427d0d43c9493220578115
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
@@ -0,0 +1,80 @@
+# Codex Feedback on Revised Test Coverage Plan
+
+**Created:** 2026-06-01T04:05Z  
+**Reviewer:** Codex  
+**Reviewed artifact:** `.omc/collaboration/artifacts/test-coverage-claude-response.md`
+
+## Review Conclusion
+
+**Decision:** Accept with small scope reductions.
+
+The revised direction is sound: remove duplicate list-isolation tests, align dean permissions with assigned approvals, treat state-machine coverage as sequential API logic rather than real concurrency, and avoid a cross-timezone matrix.
+
+The remaining issue is scope precision. Some proposed state-machine tests describe transitions the current system does not expose or enforce at model level. The executable test plan should verify the API/validator behavior that actually exists today.
+
+## Required Adjustments
+
+### 1. Detail isolation: keep, but align dean semantics
+
+Add focused detail endpoint tests for:
+
+1. Student cannot GET another student's application.
+2. Counselor cannot GET cross-class application.
+3. Dean cannot GET an application without their own pending dean approval.
+
+The dean detail test should explicitly use the current implementation semantics: `get_application` allows dean access only when a pending dean approval exists for that dean. It does not allow access to completed dean approvals.
+
+The `decision=all` approval list leak test is valid, but it belongs in `backend/apps/approvals/tests/test_list_permissions.py`, not a new detail-isolation file.
+
+### 2. State machine: keep sequential tests, reduce duplication
+
+The clarified "sequential, not concurrent" scope matches my recommendation.
+
+Do not implement this as a broad 8-case new matrix file from scratch. Current tests already cover:
+
+- complete approval path in `test_application_flow.py`
+- counselor/dean rejection paths in `test_rejection_flow.py`
+- duplicate approval/reject conflict and step/status mismatch in `test_state_machine.py`
+- cross-role and non-assigned approver checks in `test_permissions.py`
+
+Add only the missing high-value cases:
+
+1. Resubmission after rejection creates a new pending counselor application.
+2. Completed terminal operation protection is covered for duplicate same-decision attempts; add only an opposite-decision terminal check if not already covered by the existing duplicate tests.
+3. Dean approval uniqueness should be tested through the actual API path if feasible, but avoid relying on direct model mutation as the main assertion.
+
+Remove or reword proposed tests such as "draft -> approved" and "pending_counselor -> approved" unless you add a real state-transition validator outside the approval API. Current `Application.clean()` only prevents duplicate active applications; it does not enforce a full transition graph.
+
+### 3. Timezone boundaries: include only as merged serializer tests
+
+Include 2 deterministic serializer tests in `backend/apps/applications/tests/test_serializer_validation.py`:
+
+1. Mock `timezone.now()` at `2026-06-01 23:59:59` Asia/Shanghai and assert `2026-06-02` passes.
+2. Mock `timezone.now()` at `2026-06-02 00:00:01` Asia/Shanghai and assert `2026-06-01` fails.
+
+The existing `test_leave_date_today` and `test_leave_date_past` already cover the generic today/past rules, so a third timezone test is optional and not necessary for this iteration.
+
+## Final Executable Scope
+
+**Core implementation target:**
+
+1. Add `backend/apps/applications/tests/test_detail_permissions.py` with 3 detail GET isolation tests.
+2. Add `decision=all` leak coverage to `backend/apps/approvals/tests/test_list_permissions.py`.
+3. Extend existing state-machine tests only for missing terminal/opposite-decision or resubmission gaps.
+4. Add 2 mocked boundary tests to `test_serializer_validation.py`.
+
+## Time Estimate
+
+**Realistic estimate:** 0.6 day if implemented against existing fixtures and test files.
+
+0.7 day is a safe planning buffer, but not the target. The only way this becomes 0.7+ day is if the implementation creates a new broad matrix test suite instead of extending existing focused files.
+
+If the team must cap at 0.5 day, cut in this order:
+
+1. Drop timezone boundary tests first.
+2. Drop the opposite-decision terminal-state test if duplicate terminal tests already give enough confidence.
+3. Keep detail isolation and `decision=all` leak coverage; those are the highest-value security tests.
+
+## Consensus Recommendation
+
+Proceed with the narrowed scope above. No real concurrency tests and no cross-timezone matrix.

exec
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
 M .omc/collaboration/artifacts/20260531-0445-dorm-provider-discovery.md
 M .omc/collaboration/artifacts/phase4a-devtools-setup.md
 M .omc/collaboration/artifacts/phase4b-prep-note.md
 M .omc/collaboration/artifacts/phase4b-skeleton-gaps.md
 M .omc/collaboration/events.jsonl
 M .omc/collaboration/state.json
 M .omc/state/hud-stdin-cache.json
 M backend/apps/applications/providers.py
 M backend/apps/applications/tests/test_application_flow.py
 M backend/apps/applications/tests/test_constraints.py
 M backend/apps/applications/tests/test_error_cases.py
 M backend/apps/approvals/tests/test_permissions.py
 M backend/apps/approvals/tests/test_rejection_flow.py
 M backend/apps/approvals/tests/test_state_machine.py
 M backend/apps/approvals/views.py
 M backend/data/templates/students_template.csv
 M frontend/services/api.ts
 M frontend/services/mock.ts
 M frontend/types/api.ts
 M miniprogram/pages/detail/detail.ts
 M miniprogram/types/api.ts
 M tests/smoke_test.sh
 M tests/test_p0_fixes.sh
?? .claude/scheduled_tasks.json
?? .claude/scheduled_tasks.lock
?? .omc/artifacts/api-samples-v0.2.sh
?? .omc/artifacts/api-samples/
?? .omc/artifacts/ask/claude-response-phase2-approach-2026-05-31.md
?? .omc/artifacts/ask/codex-claude-docs-discussions-codex-review-2026-05-27-35-claude-re-2026-06-01T01-59-52-222Z.md
?? .omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md
?? .omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-34-implementation-o-2026-06-01T01-50-38-091Z.md
?? .omc/artifacts/ask/codex-final-wording-fixes-complete-and-pushed-phase-4a-prep-docs-f-2026-05-31T03-34-09-147Z.md
?? .omc/artifacts/ask/codex-i-reviewed-your-phase-4a-readiness-repair-recommendation-com-2026-05-31T03-13-17-070Z.md
?? .omc/artifacts/ask/codex-i-reviewed-your-week-4-prep-bundle-recommendation-event-63-c-2026-05-30T20-55-24-390Z.md
?? .omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md
?? .omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md
?? .omc/artifacts/ask/codex-phase-1-a-skeleton-miniprogram-wechat-devtools-b-p0-1-applic-2026-05-30T18-57-33-443Z.md
?? .omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md
?? .omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-38-45-885Z.md
?? .omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-43-29-691Z.md
?? .omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md
?? .omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md
?? .omc/artifacts/ask/codex-phase-4a-blocked-on-phase4a-waiting-for-devtools-phase-4b-ph-2026-06-01T01-33-23-790Z.md
?? .omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md
?? .omc/artifacts/ask/codex-phase-4b-prep-note-complete-and-pushed-you-said-hard-stop-on-2026-05-31T03-47-21-588Z.md
?? .omc/artifacts/ask/codex-phase-4b-role-guard-ts-date-ts-p0-ui-phase-4a-wechat-devtool-2026-06-01T03-32-12-743Z.md
?? .omc/artifacts/ask/codex-phase-4b-student-application-miniprogram-pages-student-appli-2026-06-01T02-23-37-379Z.md
?? .omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md
?? .omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-27-45-286Z.md
?? .omc/artifacts/ask/codex-student-application-api-createdefaultapiclient-reason-leave--2026-06-01T01-42-06-938Z.md
?? .omc/artifacts/ask/codex-user-instruction-repeated-continue-discussing-next-steps-fin-2026-05-31T03-57-31-643Z.md
?? .omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md
?? .omc/artifacts/ask/codex-week-3-complete-need-next-phase-strategy-discussion-complete-2026-05-30T20-23-08-920Z.md
?? .omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md
?? .omc/artifacts/ask/codex-week-4-consensus-reached-but-execution-blocked-on-external-d-2026-05-30T20-33-00-011Z.md
?? .omc/artifacts/ask/codex-week-4-consensus-reached-but-execution-blocked-on-external-d-2026-05-30T20-42-36-193Z.md
?? .omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md
?? .omc/collaboration/artifacts/20260530-1625-claude-phase1b-response.md
?? .omc/collaboration/artifacts/20260530-1655-claude-step2-phase1-response.md
?? .omc/collaboration/artifacts/20260530-1718-claude-blocking-issues-response.md
?? .omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md
?? .omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md
?? .omc/collaboration/artifacts/20260530-2048-claude-response-codex-prep-analysis.md
?? .omc/collaboration/artifacts/20260530-2053-codex-response-to-claude-week4-prep.md
?? .omc/collaboration/artifacts/20260530-2251-codex-four-project-pattern-analysis.md
?? .omc/collaboration/artifacts/20260530-2301-codex-gemini-and-modular-agent-analysis.md
?? .omc/collaboration/artifacts/20260530-2347-codex-agent-lifecycle-consensus.md
?? .omc/collaboration/artifacts/20260531-0439-codex-week4-blocked-prep-analysis.md
?? .omc/collaboration/artifacts/20260601-0135-claude-response-phase4a-blocker-challenge.md
?? .omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
?? .omc/collaboration/artifacts/blocked-waiting-for-devtools.md
?? .omc/collaboration/artifacts/test-coverage-analysis.md
?? .omc/collaboration/artifacts/test-coverage-claude-response.md
?? .omc/collaboration/task-2-consensus.md
?? .omc/collaboration/task-3-consensus.md
?? .omc/collaboration/task-4-consensus.md
?? .omc/project-memory.json
?? .omc/sessions/
?? .omc/state/agent-replay-7afec07d-3b40-4e4c-8f86-86e9dc0e791c.jsonl
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
?? .omc/state/subagent-tracking.json
?? backend/.omc/
?? backend/apps/approvals/validators.py
?? backend/docs/
?? docs/contracts/contract-v0.2.md
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
?? docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md
?? docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md
?? docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md
?? docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md
?? docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
?? docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md
?? docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md
?? docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md
?? docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md
?? docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md
?? docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md
?? docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md
?? docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md
?? docs/discussions/week3-day1-review-2026-05-30/09-codex-execution-review.md
?? docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md
?? docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md
?? docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md
?? docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md
?? docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md
?? docs/discussions/week3-day1-review-2026-05-30/16-codex-authorization-ruling.md
?? docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md
?? docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md
?? docs/discussions/week3-day1-review-2026-05-30/19-claude-deadlock-analysis.md
?? docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md
?? docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md
?? docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md
?? docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md
?? docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md
?? docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md
?? findings.md
?? miniprogram/.omc/
?? progress.md
?? task_plan.md
?? "\346\257\225\344\270\232\347\246\273\346\240\241\347\263\273\347\273\237\347\224\250\346\210\267\346\226\207\346\241\243.zip"
exec
/bin/bash -lc 'rtk tail -3 .omc/collaboration/events.jsonl' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{"id":71,"type":"blocked","agent":"codex","timestamp":"2026-05-31T03:56:52.552Z","summary":"Final consensus challenge found and fixed stale Phase 4 handoff docs; remaining work is blocked on WeChat DevTools evidence.","task_id":"phase4a_waiting_for_devtools","artifacts":[".omc/collaboration/artifacts/phase4a-devtools-setup.md",".omc/collaboration/artifacts/phase4b-prep-note.md",".omc/collaboration/artifacts/phase4b-skeleton-gaps.md",".omc/collaboration/artifacts/blocked-waiting-for-devtools.md"],"status":"blocked","details":{"answer":"C_then_A","missed_items_fixed":["stale DevTools setup login credential","stale ApiClient config snippet","stale shared API/types verification status"],"remaining_blocker":"WeChat DevTools installation/execution evidence"}}
{"id":72,"type":"blocker_removed","agent":"claude","timestamp":"2026-06-01T01:36:41.719650177Z","task_id":"phase4b_implementation","summary":"Phase 4B implementation unblocked after Codex review consensus","status":"in_progress","details":{"reason":"Codex review confirmed Phase 4A blocker was over-cautious","artifacts":[".omc/artifacts/ask/codex-phase-4a-blocked-on-phase4a-waiting-for-devtools-phase-4b-ph-2026-06-01T01-33-23-790Z.md",".omc/collaboration/artifacts/20260601-0135-claude-response-phase4a-blocker-challenge.md"],"p0_fix":"Fixed form fields in phase4b-skeleton-gaps.md (reason+leave_date)","scope":"student-application page + role routing + API centralization"}}
{"id":73,"type":"review_response","agent":"codex","timestamp":"2026-06-01T04:06:28.001601Z","summary":"Codex reviewed Claude revised test coverage plan and accepted it with narrowed executable scope.","task_id":"phase4b_implementation","artifacts":[".omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md"],"status":"in_progress","details":{"decision":"accept_with_scope_reductions","time_estimate":"0.6 day target, 0.7 day buffer","include_timezone":"merge two deterministic serializer boundary tests","state_machine_scope":"sequential API logic only, no real concurrency"}}

exec
/bin/bash -lc 'rtk python3 -m json.tool .omc/collaboration/state.json' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{
    "workflow_id": "claude-codex-collab-mvp",
    "current_task": "phase4b_implementation",
    "active_agent": "claude",
    "status": "in_progress",
    "last_event_id": 73,
    "updated_at": "2026-06-01T04:06:28.001601Z"
}

diff --git a/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
new file mode 100644
index 0000000000000000000000000000000000000000..297e3871620c049a4f427d0d43c9493220578115
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
@@ -0,0 +1,80 @@
+# Codex Feedback on Revised Test Coverage Plan
+
+**Created:** 2026-06-01T04:05Z  
+**Reviewer:** Codex  
+**Reviewed artifact:** `.omc/collaboration/artifacts/test-coverage-claude-response.md`
+
+## Review Conclusion
+
+**Decision:** Accept with small scope reductions.
+
+The revised direction is sound: remove duplicate list-isolation tests, align dean permissions with assigned approvals, treat state-machine coverage as sequential API logic rather than real concurrency, and avoid a cross-timezone matrix.
+
+The remaining issue is scope precision. Some proposed state-machine tests describe transitions the current system does not expose or enforce at model level. The executable test plan should verify the API/validator behavior that actually exists today.
+
+## Required Adjustments
+
+### 1. Detail isolation: keep, but align dean semantics
+
+Add focused detail endpoint tests for:
+
+1. Student cannot GET another student's application.
+2. Counselor cannot GET cross-class application.
+3. Dean cannot GET an application without their own pending dean approval.
+
+The dean detail test should explicitly use the current implementation semantics: `get_application` allows dean access only when a pending dean approval exists for that dean. It does not allow access to completed dean approvals.
+
+The `decision=all` approval list leak test is valid, but it belongs in `backend/apps/approvals/tests/test_list_permissions.py`, not a new detail-isolation file.
+
+### 2. State machine: keep sequential tests, reduce duplication
+
+The clarified "sequential, not concurrent" scope matches my recommendation.
+
+Do not implement this as a broad 8-case new matrix file from scratch. Current tests already cover:
+
+- complete approval path in `test_application_flow.py`
+- counselor/dean rejection paths in `test_rejection_flow.py`
+- duplicate approval/reject conflict and step/status mismatch in `test_state_machine.py`
+- cross-role and non-assigned approver checks in `test_permissions.py`
+
+Add only the missing high-value cases:
+
+1. Resubmission after rejection creates a new pending counselor application.
+2. Completed terminal operation protection is covered for duplicate same-decision attempts; add only an opposite-decision terminal check if not already covered by the existing duplicate tests.
+3. Dean approval uniqueness should be tested through the actual API path if feasible, but avoid relying on direct model mutation as the main assertion.
+
+Remove or reword proposed tests such as "draft -> approved" and "pending_counselor -> approved" unless you add a real state-transition validator outside the approval API. Current `Application.clean()` only prevents duplicate active applications; it does not enforce a full transition graph.
+
+### 3. Timezone boundaries: include only as merged serializer tests
+
+Include 2 deterministic serializer tests in `backend/apps/applications/tests/test_serializer_validation.py`:
+
+1. Mock `timezone.now()` at `2026-06-01 23:59:59` Asia/Shanghai and assert `2026-06-02` passes.
+2. Mock `timezone.now()` at `2026-06-02 00:00:01` Asia/Shanghai and assert `2026-06-01` fails.
+
+The existing `test_leave_date_today` and `test_leave_date_past` already cover the generic today/past rules, so a third timezone test is optional and not necessary for this iteration.
+
+## Final Executable Scope
+
+**Core implementation target:**
+
+1. Add `backend/apps/applications/tests/test_detail_permissions.py` with 3 detail GET isolation tests.
+2. Add `decision=all` leak coverage to `backend/apps/approvals/tests/test_list_permissions.py`.
+3. Extend existing state-machine tests only for missing terminal/opposite-decision or resubmission gaps.
+4. Add 2 mocked boundary tests to `test_serializer_validation.py`.
+
+## Time Estimate
+
+**Realistic estimate:** 0.6 day if implemented against existing fixtures and test files.
+
+0.7 day is a safe planning buffer, but not the target. The only way this becomes 0.7+ day is if the implementation creates a new broad matrix test suite instead of extending existing focused files.
+
+If the team must cap at 0.5 day, cut in this order:
+
+1. Drop timezone boundary tests first.
+2. Drop the opposite-decision terminal-state test if duplicate terminal tests already give enough confidence.
+3. Keep detail isolation and `decision=all` leak coverage; those are the highest-value security tests.
+
+## Consensus Recommendation
+
+Proceed with the narrowed scope above. No real concurrency tests and no cross-timezone matrix.

  ✓ Load review and collaboration protocols
  ✓ Inspect proposed test coverage response
  ✓ Compare proposal against current implementation/tests
  ✓ Write durable Codex feedback artifact
  → Return consensus recommendation
diff --git a/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
new file mode 100644
index 0000000000000000000000000000000000000000..297e3871620c049a4f427d0d43c9493220578115
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
@@ -0,0 +1,80 @@
+# Codex Feedback on Revised Test Coverage Plan
+
+**Created:** 2026-06-01T04:05Z  
+**Reviewer:** Codex  
+**Reviewed artifact:** `.omc/collaboration/artifacts/test-coverage-claude-response.md`
+
+## Review Conclusion
+
+**Decision:** Accept with small scope reductions.
+
+The revised direction is sound: remove duplicate list-isolation tests, align dean permissions with assigned approvals, treat state-machine coverage as sequential API logic rather than real concurrency, and avoid a cross-timezone matrix.
+
+The remaining issue is scope precision. Some proposed state-machine tests describe transitions the current system does not expose or enforce at model level. The executable test plan should verify the API/validator behavior that actually exists today.
+
+## Required Adjustments
+
+### 1. Detail isolation: keep, but align dean semantics
+
+Add focused detail endpoint tests for:
+
+1. Student cannot GET another student's application.
+2. Counselor cannot GET cross-class application.
+3. Dean cannot GET an application without their own pending dean approval.
+
+The dean detail test should explicitly use the current implementation semantics: `get_application` allows dean access only when a pending dean approval exists for that dean. It does not allow access to completed dean approvals.
+
+The `decision=all` approval list leak test is valid, but it belongs in `backend/apps/approvals/tests/test_list_permissions.py`, not a new detail-isolation file.
+
+### 2. State machine: keep sequential tests, reduce duplication
+
+The clarified "sequential, not concurrent" scope matches my recommendation.
+
+Do not implement this as a broad 8-case new matrix file from scratch. Current tests already cover:
+
+- complete approval path in `test_application_flow.py`
+- counselor/dean rejection paths in `test_rejection_flow.py`
+- duplicate approval/reject conflict and step/status mismatch in `test_state_machine.py`
+- cross-role and non-assigned approver checks in `test_permissions.py`
+
+Add only the missing high-value cases:
+
+1. Resubmission after rejection creates a new pending counselor application.
+2. Completed terminal operation protection is covered for duplicate same-decision attempts; add only an opposite-decision terminal check if not already covered by the existing duplicate tests.
+3. Dean approval uniqueness should be tested through the actual API path if feasible, but avoid relying on direct model mutation as the main assertion.
+
+Remove or reword proposed tests such as "draft -> approved" and "pending_counselor -> approved" unless you add a real state-transition validator outside the approval API. Current `Application.clean()` only prevents duplicate active applications; it does not enforce a full transition graph.
+
+### 3. Timezone boundaries: include only as merged serializer tests
+
+Include 2 deterministic serializer tests in `backend/apps/applications/tests/test_serializer_validation.py`:
+
+1. Mock `timezone.now()` at `2026-06-01 23:59:59` Asia/Shanghai and assert `2026-06-02` passes.
+2. Mock `timezone.now()` at `2026-06-02 00:00:01` Asia/Shanghai and assert `2026-06-01` fails.
+
+The existing `test_leave_date_today` and `test_leave_date_past` already cover the generic today/past rules, so a third timezone test is optional and not necessary for this iteration.
+
+## Final Executable Scope
+
+**Core implementation target:**
+
+1. Add `backend/apps/applications/tests/test_detail_permissions.py` with 3 detail GET isolation tests.
+2. Add `decision=all` leak coverage to `backend/apps/approvals/tests/test_list_permissions.py`.
+3. Extend existing state-machine tests only for missing terminal/opposite-decision or resubmission gaps.
+4. Add 2 mocked boundary tests to `test_serializer_validation.py`.
+
+## Time Estimate
+
+**Realistic estimate:** 0.6 day if implemented against existing fixtures and test files.
+
+0.7 day is a safe planning buffer, but not the target. The only way this becomes 0.7+ day is if the implementation creates a new broad matrix test suite instead of extending existing focused files.
+
+If the team must cap at 0.5 day, cut in this order:
+
+1. Drop timezone boundary tests first.
+2. Drop the opposite-decision terminal-state test if duplicate terminal tests already give enough confidence.
+3. Keep detail isolation and `decision=all` leak coverage; those are the highest-value security tests.
+
+## Consensus Recommendation
+
+Proceed with the narrowed scope above. No real concurrency tests and no cross-timezone matrix.

  ✓ Load review and collaboration protocols
  ✓ Inspect proposed test coverage response
  ✓ Compare proposal against current implementation/tests
  ✓ Write durable Codex feedback artifact
  ✓ Return consensus recommendation
diff --git a/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
new file mode 100644
index 0000000000000000000000000000000000000000..297e3871620c049a4f427d0d43c9493220578115
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
@@ -0,0 +1,80 @@
+# Codex Feedback on Revised Test Coverage Plan
+
+**Created:** 2026-06-01T04:05Z  
+**Reviewer:** Codex  
+**Reviewed artifact:** `.omc/collaboration/artifacts/test-coverage-claude-response.md`
+
+## Review Conclusion
+
+**Decision:** Accept with small scope reductions.
+
+The revised direction is sound: remove duplicate list-isolation tests, align dean permissions with assigned approvals, treat state-machine coverage as sequential API logic rather than real concurrency, and avoid a cross-timezone matrix.
+
+The remaining issue is scope precision. Some proposed state-machine tests describe transitions the current system does not expose or enforce at model level. The executable test plan should verify the API/validator behavior that actually exists today.
+
+## Required Adjustments
+
+### 1. Detail isolation: keep, but align dean semantics
+
+Add focused detail endpoint tests for:
+
+1. Student cannot GET another student's application.
+2. Counselor cannot GET cross-class application.
+3. Dean cannot GET an application without their own pending dean approval.
+
+The dean detail test should explicitly use the current implementation semantics: `get_application` allows dean access only when a pending dean approval exists for that dean. It does not allow access to completed dean approvals.
+
+The `decision=all` approval list leak test is valid, but it belongs in `backend/apps/approvals/tests/test_list_permissions.py`, not a new detail-isolation file.
+
+### 2. State machine: keep sequential tests, reduce duplication
+
+The clarified "sequential, not concurrent" scope matches my recommendation.
+
+Do not implement this as a broad 8-case new matrix file from scratch. Current tests already cover:
+
+- complete approval path in `test_application_flow.py`
+- counselor/dean rejection paths in `test_rejection_flow.py`
+- duplicate approval/reject conflict and step/status mismatch in `test_state_machine.py`
+- cross-role and non-assigned approver checks in `test_permissions.py`
+
+Add only the missing high-value cases:
+
+1. Resubmission after rejection creates a new pending counselor application.
+2. Completed terminal operation protection is covered for duplicate same-decision attempts; add only an opposite-decision terminal check if not already covered by the existing duplicate tests.
+3. Dean approval uniqueness should be tested through the actual API path if feasible, but avoid relying on direct model mutation as the main assertion.
+
+Remove or reword proposed tests such as "draft -> approved" and "pending_counselor -> approved" unless you add a real state-transition validator outside the approval API. Current `Application.clean()` only prevents duplicate active applications; it does not enforce a full transition graph.
+
+### 3. Timezone boundaries: include only as merged serializer tests
+
+Include 2 deterministic serializer tests in `backend/apps/applications/tests/test_serializer_validation.py`:
+
+1. Mock `timezone.now()` at `2026-06-01 23:59:59` Asia/Shanghai and assert `2026-06-02` passes.
+2. Mock `timezone.now()` at `2026-06-02 00:00:01` Asia/Shanghai and assert `2026-06-01` fails.
+
+The existing `test_leave_date_today` and `test_leave_date_past` already cover the generic today/past rules, so a third timezone test is optional and not necessary for this iteration.
+
+## Final Executable Scope
+
+**Core implementation target:**
+
+1. Add `backend/apps/applications/tests/test_detail_permissions.py` with 3 detail GET isolation tests.
+2. Add `decision=all` leak coverage to `backend/apps/approvals/tests/test_list_permissions.py`.
+3. Extend existing state-machine tests only for missing terminal/opposite-decision or resubmission gaps.
+4. Add 2 mocked boundary tests to `test_serializer_validation.py`.
+
+## Time Estimate
+
+**Realistic estimate:** 0.6 day if implemented against existing fixtures and test files.
+
+0.7 day is a safe planning buffer, but not the target. The only way this becomes 0.7+ day is if the implementation creates a new broad matrix test suite instead of extending existing focused files.
+
+If the team must cap at 0.5 day, cut in this order:
+
+1. Drop timezone boundary tests first.
+2. Drop the opposite-decision terminal-state test if duplicate terminal tests already give enough confidence.
+3. Keep detail isolation and `decision=all` leak coverage; those are the highest-value security tests.
+
+## Consensus Recommendation
+
+Proceed with the narrowed scope above. No real concurrency tests and no cross-timezone matrix.

codex
结论：修订方案可以接受，但应小幅收窄后执行。我已把正式反馈写入 [20260601-0405-codex-test-coverage-feedback.md](/home/caohui/projects/graduation-leave-system/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md)，并记录 collaboration event `73`。

核心反馈：

- 状态机范围合理：顺序 API/validator 逻辑测试可以做，不做真实并发测试。
- 时间估算：`0.6 天`作为目标现实，`0.7 天`作为 buffer 可以接受；如果新建完整 8-case matrix，才会明显超。
- 需要削减：不要从零创建大矩阵。现有 `test_application_flow.py`、`test_rejection_flow.py`、`test_state_machine.py` 已覆盖不少路径，应只补缺口。
- 时区测试：保留，但只合并进 `test_serializer_validation.py`，做 2 个 mock 边界用例；若必须压到 `0.5 天`，时区测试第一优先砍。

最终建议执行范围：

1. 新增 3 个 application detail 权限测试：学生不能看他人、辅导员不能跨班、dean 只能看自己 pending dean approval 的申请。注意当前 dean detail 语义是 pending-only，见 [applications/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/views.py:161)。
2. `decision=all` 泄漏测试放进 approval list permissions 文件，不放 detail isolation 文件。
3. 状态机只补缺口：rejected 后重提、必要的终态反向操作保护、dean approval uniqueness。不要写“draft -> approved”这类模型级非法转换测试，当前 [models.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/models.py:36) 没有完整状态转换图验证。
4. 时区边界合并到 serializer validation，2 个 deterministic mock 测试即可。

可执行共识：按上述范围立即实施；不做真实并发、不做跨时区矩阵、不新建大而全的状态机测试套件。
diff --git a/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
new file mode 100644
index 0000000000000000000000000000000000000000..297e3871620c049a4f427d0d43c9493220578115
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
@@ -0,0 +1,80 @@
+# Codex Feedback on Revised Test Coverage Plan
+
+**Created:** 2026-06-01T04:05Z  
+**Reviewer:** Codex  
+**Reviewed artifact:** `.omc/collaboration/artifacts/test-coverage-claude-response.md`
+
+## Review Conclusion
+
+**Decision:** Accept with small scope reductions.
+
+The revised direction is sound: remove duplicate list-isolation tests, align dean permissions with assigned approvals, treat state-machine coverage as sequential API logic rather than real concurrency, and avoid a cross-timezone matrix.
+
+The remaining issue is scope precision. Some proposed state-machine tests describe transitions the current system does not expose or enforce at model level. The executable test plan should verify the API/validator behavior that actually exists today.
+
+## Required Adjustments
+
+### 1. Detail isolation: keep, but align dean semantics
+
+Add focused detail endpoint tests for:
+
+1. Student cannot GET another student's application.
+2. Counselor cannot GET cross-class application.
+3. Dean cannot GET an application without their own pending dean approval.
+
+The dean detail test should explicitly use the current implementation semantics: `get_application` allows dean access only when a pending dean approval exists for that dean. It does not allow access to completed dean approvals.
+
+The `decision=all` approval list leak test is valid, but it belongs in `backend/apps/approvals/tests/test_list_permissions.py`, not a new detail-isolation file.
+
+### 2. State machine: keep sequential tests, reduce duplication
+
+The clarified "sequential, not concurrent" scope matches my recommendation.
+
+Do not implement this as a broad 8-case new matrix file from scratch. Current tests already cover:
+
+- complete approval path in `test_application_flow.py`
+- counselor/dean rejection paths in `test_rejection_flow.py`
+- duplicate approval/reject conflict and step/status mismatch in `test_state_machine.py`
+- cross-role and non-assigned approver checks in `test_permissions.py`
+
+Add only the missing high-value cases:
+
+1. Resubmission after rejection creates a new pending counselor application.
+2. Completed terminal operation protection is covered for duplicate same-decision attempts; add only an opposite-decision terminal check if not already covered by the existing duplicate tests.
+3. Dean approval uniqueness should be tested through the actual API path if feasible, but avoid relying on direct model mutation as the main assertion.
+
+Remove or reword proposed tests such as "draft -> approved" and "pending_counselor -> approved" unless you add a real state-transition validator outside the approval API. Current `Application.clean()` only prevents duplicate active applications; it does not enforce a full transition graph.
+
+### 3. Timezone boundaries: include only as merged serializer tests
+
+Include 2 deterministic serializer tests in `backend/apps/applications/tests/test_serializer_validation.py`:
+
+1. Mock `timezone.now()` at `2026-06-01 23:59:59` Asia/Shanghai and assert `2026-06-02` passes.
+2. Mock `timezone.now()` at `2026-06-02 00:00:01` Asia/Shanghai and assert `2026-06-01` fails.
+
+The existing `test_leave_date_today` and `test_leave_date_past` already cover the generic today/past rules, so a third timezone test is optional and not necessary for this iteration.
+
+## Final Executable Scope
+
+**Core implementation target:**
+
+1. Add `backend/apps/applications/tests/test_detail_permissions.py` with 3 detail GET isolation tests.
+2. Add `decision=all` leak coverage to `backend/apps/approvals/tests/test_list_permissions.py`.
+3. Extend existing state-machine tests only for missing terminal/opposite-decision or resubmission gaps.
+4. Add 2 mocked boundary tests to `test_serializer_validation.py`.
+
+## Time Estimate
+
+**Realistic estimate:** 0.6 day if implemented against existing fixtures and test files.
+
+0.7 day is a safe planning buffer, but not the target. The only way this becomes 0.7+ day is if the implementation creates a new broad matrix test suite instead of extending existing focused files.
+
+If the team must cap at 0.5 day, cut in this order:
+
+1. Drop timezone boundary tests first.
+2. Drop the opposite-decision terminal-state test if duplicate terminal tests already give enough confidence.
+3. Keep detail isolation and `decision=all` leak coverage; those are the highest-value security tests.
+
+## Consensus Recommendation
+
+Proceed with the narrowed scope above. No real concurrency tests and no cross-timezone matrix.

tokens used
64,629

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
