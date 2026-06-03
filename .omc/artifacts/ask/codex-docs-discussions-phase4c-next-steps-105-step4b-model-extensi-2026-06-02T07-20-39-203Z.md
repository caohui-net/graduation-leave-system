# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-02T07:20:39.203Z

## Original task

docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md

## Final prompt

docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md

## Raw output

```text
Created the Codex strategy response at [106-step4b-model-extension-strategy-codex-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:1).

Key decision: recommend **选项组合2：扩展 `User.phone/email/department` + 不允许学工API覆盖 `name`**. The response also defines Step 4B scope, missing/empty API field behavior, mapper `email` requirement, and acceptance criteria.

No tests were run because this was a documentation/review artifact only.


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
session id: 019e8731-7ba4-7a91-bafe-0c5365dd638c
--------
user
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md
codex
I’ll inspect the referenced document and the project workflow rules first so I can respond in the project’s expected format.
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
/bin/bash -lc "sed -n '1,240p' docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Phase 4C Step 4B前置 - User模型扩展策略讨论请求

**请求日期：** 2026-06-02  
**请求方：** Claude  
**讨论目标：** User模型扩展决策（Step 4B实现前置条件）  
**文档编号：** 105

---

## 讨论背景

**Step 4A已完成：** 同步计划服务实现，测试8/8通过，Codex批准。

**Step 4B阻塞原因：** User模型字段gap（doc 95/99/103识别）
- mapper输出phone/department
- 字段契约定义phone/email/department为API补充字段
- User模型只到graduation_year，缺这些字段
- would_update_count为候选数，无实际可写补充字段

**Codex建议（doc 103）：** 优先决策模型扩展策略，再实现Step 4B真实upsert。

---

## 核心决策问题

### 问题1：是否新增phone/email/department字段？

**选项A：扩展User模型**
- 新增字段：phone, email, department
- 类型定义：CharField, nullable, blank=True
- migration影响：需创建migration，现有数据字段值为NULL

**选项B：不扩展模型**
- 保持当前7字段（user_id/name/role/active/class_id/is_graduating/graduation_year）
- API补充字段不持久化

### 问题2：name字段是否允许API覆盖？

**当前状态：**
- CSV导入时设置name（主要数据源）
- 学工API也返回name
- 字段契约定义name为CSV主导核心字段

**如果允许覆盖：**
- API返回name可更新本地User.name
- 需定义CSV与API冲突优先级（last-write-wins or CSV优先）

**如果不允许覆盖：**
- name保持CSV值不变
- API name字段被忽略或仅用于比对

---

## 选项分析

### 选项组合1：扩展模型 + 允许name覆盖

**优点：**
- Step 4B可实现完整API补充字段upsert
- phone/email/department可持久化
- name可从API同步更新（如学工系统修正）

**缺点：**
- 需要migration
- name覆盖可能与CSV冲突

**适用场景：** 学工系统为权威数据源，CSV只是初始导入

### 选项组合2：扩展模型 + 不允许name覆盖

**优点：**
- Step 4B可持久化phone/email/department
- name保持CSV主导，避免冲突
- 核心字段（name/class_id/毕业信息）仍由CSV控制

**缺点：**
- 需要migration
- name字段冗余（API返回但不使用）

**适用场景：** CSV为核心数据源，API只补充联系方式

### 选项组合3：不扩展模型 + 只报告

**优点：**
- 无migration风险
- 模型保持简单
- Step 4A的would_update报告已足够

**缺点：**
- Step 4B无实际可写补充字段
- API数据不持久化，只读分析
- would_update_count候选无法转为真实更新

**适用场景：** 学工API仅用于数据对比和差异报告

---

## 业务价值评估

### phone/email/department字段价值

**使用场景：**
- 联系学生（电话、邮件）
- 院系统计和筛选
- 用户个人信息展示

**数据源对比：**
- CSV：不包含phone/email/department
- 学工API：包含phone/department，email需补充提取

**当前系统需求：** 未明确需要这些字段

**潜在需求：** 通知推送、用户资料页

### name字段覆盖价值

**CSV name：** 导入时准确
**API name：** 实时同步学工系统

**冲突场景：**
- CSV导入后学工系统修正姓名
- API返回更新的name

**风险：** CSV重新导入可能覆盖API更新

---

## 技术影响评估

### Migration影响

**新增字段migration：**
```python
class Migration(migrations.Migration):
    operations = [
        migrations.AddField('User', 'phone', CharField(max_length=20, null=True, blank=True)),
        migrations.AddField('User', 'email', EmailField(max_length=254, null=True, blank=True)),
        migrations.AddField('User', 'department', CharField(max_length=100, null=True, blank=True)),
    ]
```

**影响：**
- 现有数据：字段值为NULL
- 查询性能：nullable字段无显著影响
- 回滚：可反向migration

**风险：** 低

### CSV/API数据源冲突

**当前策略（Phase 1）：**
- CSV主导：user_id/name/role/class_id/is_graduating/graduation_year
- API补充：phone/email/department

**name覆盖策略选项：**

**策略1：last-write-wins**
- API更新name → 覆盖
- CSV重新导入 → 覆盖

**策略2：CSV优先**
- API name被忽略
- 只有CSV可更新name

**策略3：时间戳比较**
- 需增加updated_at字段
- 复杂度高

**建议：** 策略2（CSV优先），避免冲突

---

## 请Codex审查

### 审查要点1：选项推荐

**基于：**
- 字段契约定义
- Phase 1策略
- 系统当前需求
- 未来扩展性

**请明确推荐：**
- 选项组合1/2/3中的优先选择
- 推荐理由

### 审查要点2：phone/email/department必要性

**请评估：**
- 这3个字段对系统的业务价值
- 是否值得增加migration
- 如果不扩展，Step 4B应实现什么

### 审查要点3：name覆盖策略

**如果扩展模型，请明确：**
- 是否允许API更新name
- CSV与API冲突优先级
- 是否需要updated_at字段

### 审查要点4：Step 4B实现范围

**请明确：**
- 扩展模型后Step 4B应实现什么
- 不扩展模型Step 4B应实现什么（或跳过）
- 是否需要Step 4B-lite（仅name更新）

---

## 关键质疑

### Q1：字段契约定义 vs 当前需求

字段契约定义phone/email/department为API补充字段，但当前系统明确需要这些字段吗？

**如果不需要：** 是否应该延后扩展，等需求明确？

### Q2：CSV与API权威性

CSV是初始导入工具还是持续数据源？
API是补充数据还是权威数据源？

**影响：** name覆盖策略和字段主导权

### Q3：migration时机

现在扩展模型 vs 等Phase 4C完成后再扩展？

**考虑：** 数据已存在，migration影响面

### Q4：mapper email提取

字段契约包含email，但mapper未提取。

**是否需要：** 补充mapper提取email字段？

### Q5：Step 4B最小范围

如果扩展模型，Step 4B最小实现是什么？
- 只更新phone/department？

exec
/bin/bash -lc "sed -n '1,220p' .omc/collaboration/protocol.md" in /home/caohui/projects/graduation-leave-system
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


exec
/bin/bash -lc "sed -n '1,220p' docs/codex-review-protocol.md" in /home/caohui/projects/graduation-leave-system
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

codex
The request is a formal Codex discussion/review document. I’ve loaded the collaboration and review protocols, and I’m checking the rest of the request plus nearby docs so the recommendation is grounded in the existing Phase 4C decisions.
exec
/bin/bash -lc 'rtk ls docs/discussions/phase4c-next-steps' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
01-claude-phase4c-strategy-proposal.md  3.8K
02-codex-phase4c-strategy-review.md  7.2K
03-claude-response-to-codex-review.md  6.4K
04-codex-response-to-claude.md  4.4K
05-claude-next-steps-strategy-request.md  4.5K
06-codex-next-steps-strategy-review.md  8.7K
07-claude-response-to-codex-strategy-review.md  6.2K
08-claude-phase2-implementation-review-request.md  10.5K
09-codex-phase2-implementation-review-response.md  9.7K
10-claude-response-to-codex-phase2-review.md  7.2K
100-claude-response-agree-modification.md  6.0K
101-implementation-review-and-test-request.md  5.2K
102-implementation-complete-summary.md  5.1K
102-implementation-review-and-test-codex-response.md  7.7K
103-step4a-implementation-final-codex-response.md  5.8K
104-step4a-final-consensus.md  3.3K
105-step4b-model-extension-strategy-request.md  6.4K
11-claude-p1-fixes-review-request.md  8.1K
12-codex-p1-fixes-review-response.md  7.0K
13-claude-response-to-codex-p1-review.md  8.2K
14-claude-p1-implementation-summary.md  7.5K
15-codex-p1-implementation-review-response.md  5.1K
16-claude-response-to-codex-p1-verification.md  5.9K
17-claude-p0-fix-verification-summary.md  3.1K
18-codex-p0-fix-verification-response.md  2.5K
19-claude-next-phase-strategy-request.md  7.0K
20-codex-next-phase-strategy-response.md  10.2K
21-claude-consensus-narrowed-strategy.md  6.5K
22-claude-post-execution-next-steps.md  4.9K
23-codex-post-execution-next-steps-response.md  7.1K
24-claude-consensus-evidence-closure.md  3.4K
25-claude-post-evidence-next-strategy.md  6.5K
26-codex-post-evidence-strategy-review.md  6.9K
27-claude-consensus-decision-gate.md  5.6K
28-claude-post-phase0-next-strategy.md  7.4K
29-codex-post-phase0-next-strategy-response.md  8.6K
29-codex-post-phase0-next-strategy-review.md  6.9K
30-claude-consensus-contract-revision-gate.md  5.8K
31-claude-post-contract-revision-next-strategy.md  10.5K
32-codex-post-contract-revision-next-strategy-response.md  7.5K
33-claude-consensus-authorization-gate.md  3.7K
34-claude-authorization-interpretation-request.md  3.6K
35-codex-authorization-interpretation-response.md  5.4K
36-claude-consensus-minimal-confirmation.md  1.9K
37-claude-post-phase1-next-strategy.md  6.6K
38-codex-post-phase1-next-strategy-response.md  9.3K
39-claude-consensus-option-a-lite.md  6.2K
40-claude-post-phase2a-next-strategy.md  8.3K
41-codex-post-phase2a-next-strategy-response.md  10.2K
42-claude-consensus-phase2a-stabilization.md  6.2K
43-claude-post-phase2a-stabilization-next-strategy.md  3.2K
44-codex-post-phase2a-stabilization-next-strategy-response.md  8.1K
45-claude-response-to-codex-option-e-lite-review.md  5.9K
46-claude-codex-consensus-option-e-lite.md  2.8K
47-claude-post-step2-next-strategy.md  5.2K
48-codex-post-step2-next-strategy-response.md  6.8K
49-claude-consensus-option-e-lite-complete.md  3.8K
50-claude-post-option-e-lite-next-strategy.md  6.5K
51-codex-option-e-lite-next-strategy-review.md  10.0K
52-claude-response-option-a-corrected.md  6.2K
53-codex-confirmation-option-a-corrected.md  1.9K
54-claude-codex-consensus-option-a-execution.md  2.2K
55-claude-post-api-schema-p1-next-strategy.md  4.1K
56-codex-post-api-schema-p1-next-strategy-response.md  4.9K
57-claude-response-accept-option-a-prime.md  4.1K
58-claude-codex-consensus-option-a-prime-partial.md  4.8K
59-claude-codex-final-consensus-option-2.md  3.9K
60-codex-final-consensus-option-2-review-response.md  6.5K
61-claude-codex-final-consensus-d0-a-lite.md  3.9K
62-phase2b-contract-decision-review-request.md  4.6K
63-phase2b-contract-decision-codex-response.md  8.0K
64-claude-response-accept-option-1.md  2.8K
65-phase2b-option1-execution-review-request.md  3.9K
66-phase2b-option1-execution-codex-response.md  6.7K
67-claude-response-accept-codex-fixes.md  1.9K
68-claude-codex-consensus-phase2b-option1.md  6.1K
69-api-data-reading-test-review-request.md  4.7K
69-claude-post-phase2b-step1-next-strategy.md  4.7K
70-codex-post-phase2b-step1-next-strategy-response.md  7.1K
71-claude-response-accept-b-mini.md  3.5K
72-claude-codex-consensus-phase2b-step2-strategy.md  5.8K
73-api-data-reading-test-codex-response.md  10.7K
74-claude-response-accept-codex-with-algo.md  8.4K
75-claude-codex-consensus-api-test-step0.md  2.0K
76-claude-post-step0-next-strategy-request.md  5.2K
77-codex-post-step0-strategy-response.md  9.3K
78-claude-response-accept-step1-segmented.md  3.3K
79-claude-codex-consensus-step1a.md  1.2K
80-step1a-completion-next-review-request.md  4.4K
81-step1a-completion-codex-response.md  7.1K
82-claude-response-agree-step1b-lite-first.md  7.7K
83-consensus-step1b-lite-first.md  2.4K
84-post-step1-next-strategy-request.md  5.5K
85-post-step1-next-strategy-codex-response.md  8.7K
86-claude-response-agree-step2-strategy.md  6.8K
87-step2b-implementation-review-request.md  4.5K
88-step2b-implementation-codex-response.md  3.8K
89-claude-response-agree-fixes.md  7.7K
90-next-priority-discussion-request.md  2.6K
91-next-priority-codex-response.md  8.3K
92-claude-response-agree-step2c-lite.md  8.5K
93-consensus-step2c-lite-first.md  3.4K
94-post-step3-next-priority-request.md  2.6K
95-post-step3-next-priority-codex-response.md  7.4K
96-claude-response-agree-step4a.md  6.6K
97-consensus-step4a-first.md  4.0K
98-step4a-implementation-review-request.md  5.3K
99-step4a-implementation-codex-response.md  7.8K

exec
/bin/bash -lc "rtk sed -n '241,520p' docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
- 包含email？
- 包含name？

---

## 期望输出

**Codex审查后请明确：**

1. **选项推荐（1/2/3）**
   - 优先选择及理由
   - 权衡分析

2. **字段扩展决策**
   - 是否新增phone/email/department
   - 如果是，migration方案
   - 如果否，替代方案

3. **name覆盖决策**
   - 是否允许API更新name
   - CSV/API冲突策略

4. **Step 4B实施范围**
   - 明确实现目标
   - 预计工作量
   - 验收标准

5. **Q1-Q5质疑点答案**
   - 澄清关键假设
   - 调整决策依据

---

**审查方式：** 使用 `/oh-my-claudecode:ask codex`

**文档状态：** 等待Codex审查

exec
/bin/bash -lc "rtk rg -n \"phone|email|department|graduation_year|would_update|Step 4B|字段契约|API补充|name覆盖|User模型\" docs . -g '"'!node_modules'"' -g '"'!venv'"'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
./DEPLOYMENT.md:126:- department (optional)
./DEPLOYMENT.md:137:- graduation_year (required)
./docs/PROJECT-SUMMARY.md:251:- ✓ User模型和认证
./docs/PROJECT-SUMMARY.md:252:  - User模型（user_id、name、role、class_id、is_graduating、graduation_year）
./docs/PROJECT-SUMMARY.md:1257:  - counselors.csv: active → is_active, 添加department字段
./docs/PROJECT-SUMMARY.md:1259:  - students.csv: 移除active字段, 添加department/major/grade字段
./docs/PROJECT-SUMMARY.md:2229:- API/CSV并存策略：Phase 1（CSV主导+API补充）
./docs/PROJECT-SUMMARY.md:2233:- ✅ API初期只补充phone/email/department，不创建新用户
./docs/PROJECT-SUMMARY.md:2234:- ✅ class_id/is_graduating/graduation_year继续由CSV维护
./docs/PROJECT-SUMMARY.md:2289:1. User模型缺失phone/email/department字段
./docs/PROJECT-SUMMARY.md:2291:   - 字段契约定义为API补充字段
./docs/PROJECT-SUMMARY.md:2292:   - 但模型只到graduation_year
./docs/PROJECT-SUMMARY.md:2293:   - Step 4B真实upsert阻塞
./docs/PROJECT-SUMMARY.md:2301:- ⏸ Step 4B：真实upsert（等待模型扩展决策）
./docs/PROJECT-SUMMARY.md:2302:- ⏸ Step 5：命令入口（等待Step 4B）
./docs/PROJECT-SUMMARY.md:2307:- 待讨论：User模型扩展策略（增加phone/email/department）
./docs/PROJECT-SUMMARY.md:2333:- existing_count, missing_local_count, would_update_count
./docs/PROJECT-SUMMARY.md:2339:- 关键质疑：5个Q（异常处理/would_update准确性/conflicts结构/skipped统计/测试场景5必要性）
./docs/PROJECT-SUMMARY.md:2359:- docstring明确would_update_count为候选数语义
./docs/PROJECT-SUMMARY.md:2381:- ⏭ 下一步：User模型扩展决策（增加phone/email/department字段）
./docs/PROJECT-SUMMARY.md:2382:- ⏸ Step 4B：真实upsert（等待模型扩展）
docs/acceptance/phase4c-evidence-index.md:103:| `students_template.csv` | student_id, name, class_id, is_graduating, graduation_year |
docs/acceptance/phase4c-acceptance-checklist.md:78:| counselors.csv字段统一 | ✅ 通过 | `employee_id, name, department, is_active` |
docs/acceptance/phase4c-acceptance-checklist.md:80:| students.csv字段统一 | ✅ 通过 | `student_id, name, class_id, is_graduating, graduation_year` |
./docs/phase4c-xg-field-coverage.md:32:| `phone` | string | 手机号 | 文档样例 |
./docs/phase4c-xg-field-coverage.md:34:| `department` | string | 院系/部门 | 文档样例 |
./docs/phase4c-xg-field-coverage.md:47:- `graduation_year`：毕业年份
./docs/phase4c-xg-field-coverage.md:48:- `email`：邮箱
./docs/phase4c-xg-field-coverage.md:52:## 三、内部User模型字段清单
./docs/phase4c-xg-field-coverage.md:68:| `graduation_year` | integer | 学生必填 | 毕业年份 |
./docs/phase4c-xg-field-coverage.md:74:| `phone` | string | 手机号（用于找回密码、通知） |
./docs/phase4c-xg-field-coverage.md:75:| `email` | string | 邮箱（用于通知） |
./docs/phase4c-xg-field-coverage.md:76:| `department` | string | 院系/部门（用于展示） |
./docs/phase4c-xg-field-coverage.md:96:| `User.phone` | `phone` | 🟡 待确认 | **可选**。缺失则置为NULL。 |
./docs/phase4c-xg-field-coverage.md:97:| `User.department` | `department` | 🟡 待确认 | **可选**。缺失则置为NULL。 |
./docs/phase4c-xg-field-coverage.md:121:| `User.graduation_year` | 未知 | 🔴 缺失 | **学生必填，API无法提供**。<br>- 继续由CSV/手工维护<br>- API同步时不覆盖此字段<br>- 新用户如果缺失，标记为`skip_reason: missing_graduation_year` |
./docs/phase4c-xg-field-coverage.md:144:| `phone`缺失 | 置为NULL（新用户）或保持原值（已存在用户） |
./docs/phase4c-xg-field-coverage.md:145:| `email`缺失 | 置为NULL（新用户）或保持原值（已存在用户） |
./docs/phase4c-xg-field-coverage.md:146:| `department`缺失 | 置为NULL（新用户）或保持原值（已存在用户） |
./docs/phase4c-xg-field-coverage.md:149:| `graduation_year`缺失 | 保持原值（不覆盖），新用户跳过并标记`missing_graduation_year` |
./docs/phase4c-xg-field-coverage.md:188:| **CSV导入（主）** | `user_id`, `name`, `role`, `class_id`, `is_graduating`, `graduation_year` | 学生创建和核心业务字段由CSV维护 |
./docs/phase4c-xg-field-coverage.md:189:| **学工API（补充）** | `phone`, `email`, `department`, `updated_at` | API仅补充或更新非核心字段 |
./docs/phase4c-xg-field-coverage.md:193:**Phase 1（当前）：CSV主导 + API补充**
./docs/phase4c-xg-field-coverage.md:194:- CSV导入创建所有学生用户（包含`class_id`/`is_graduating`/`graduation_year`）
./docs/phase4c-xg-field-coverage.md:195:- 学工API同步仅更新已存在用户的`phone`/`email`/`department`
./docs/phase4c-xg-field-coverage.md:199:- 前提：live测试确认学工API能提供`class_id`/`is_graduating`/`graduation_year`
./docs/phase4c-xg-field-coverage.md:226:    "phone": "13800138000",
./docs/phase4c-xg-field-coverage.md:227:    "department": "计算机学院",
./docs/phase4c-xg-field-coverage.md:234:    "phone": "13800138001",
./docs/phase4c-xg-field-coverage.md:254:    "phone": "13800138000",
./docs/phase4c-xg-field-coverage.md:255:    "department": "计算机学院",
./docs/phase4c-xg-field-coverage.md:258:    "graduation_year": None,  # API不提供
./docs/phase4c-xg-field-coverage.md:267:    "phone": "13800138001",
./docs/phase4c-xg-field-coverage.md:268:    "department": None,
./docs/phase4c-xg-field-coverage.md:271:    "graduation_year": None,
./docs/phase4c-xg-field-coverage.md:280:    "phone": None,
./docs/phase4c-xg-field-coverage.md:281:    "department": None,
./docs/phase4c-xg-field-coverage.md:284:    "graduation_year": None,
./docs/phase4c-xg-field-coverage.md:314:3. 是否提供`class_id`/`is_graduating`/`graduation_year`
docs/api说明.txt:28:phone	否	string	手机号
docs/api说明.txt:31:departmentId	否	string	部门Id ,查询多个用半角逗号分隔例如: 203,204
docs/api说明.txt:32:departmentCode	否	string	部门code ,查询多个用半角逗号分隔例如: 203,204
docs/api说明.txt:52:                "phone": "18626409896",
docs/api说明.txt:69:                        "department_code": "C100260159402712838523",
docs/api说明.txt:84:                        "department_code": "C100261159409057535680",
docs/api说明.txt:98:                    "phone": "18626409896",
docs/api说明.txt:112:                "department": [
docs/api说明.txt:119:                        "department_code": "C100261159409057535680",
docs/api说明.txt:129:                            "department_id": 47
docs/api说明.txt:168:phone	手机号
docs/api说明.txt:174:user.phone	手机号
docs/api说明.txt:185:department.name	部门名称 name
docs/api说明.txt:186:department.third_code	部门的在对接系统中的标识/来源可能为学校自建/钉钉接入/企业微信接入
docs/api说明.txt:187:department.department_code	当前部门的在青橄榄系统中对外提供的唯一Code
docs/api说明.txt:188:department.level	当前部门级别
docs/api说明.txt:189:department.parent_id	父级主键ID
docs/api说明.txt:190:department.key	该层级所对应的路由
./docs/templates/学生基本信息导入模板.csv:1:student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
./docs/contracts/contract-v0.1.md:26:    graduation_year: Optional[int] = None # 毕业年份（仅学生）
./docs/contracts/contract-v0.1.md:225:**说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。
./docs/contracts/contract-v0.1.md:343:    {"user_id": "2020001", "name": "张三", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
./docs/contracts/contract-v0.1.md:344:    {"user_id": "2020002", "name": "李四", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
./docs/contracts/contract-v0.1.md:345:    {"user_id": "2020003", "name": "王五", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
./docs/contracts/contract-v0.1.md:346:    {"user_id": "2020004", "name": "赵六", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
./docs/contracts/contract-v0.1.md:347:    {"user_id": "2020005", "name": "钱七", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
./docs/contracts/contract-v0.1.md:348:    {"user_id": "2020006", "name": "孙八", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
./docs/contracts/contract-v0.1.md:349:    {"user_id": "2020007", "name": "周九", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
./docs/contracts/contract-v0.1.md:350:    {"user_id": "2020008", "name": "吴十", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
./docs/contracts/contract-v0.1.md:351:    {"user_id": "2020009", "name": "郑十一", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
./docs/contracts/contract-v0.1.md:352:    {"user_id": "2020010", "name": "王十二", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
./docs/contracts/contract-v0.1.md:359:    {"user_id": "T001", "name": "李老师", "role": "counselor", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
./docs/contracts/contract-v0.1.md:360:    {"user_id": "T002", "name": "王老师", "role": "counselor", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
./docs/contracts/contract-v0.1.md:367:    {"user_id": "D001", "name": "赵主任", "role": "dean", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
./docs/contracts/contract-v0.1.md:383:{"user_id": "2020099", "name": "边界1", "role": "student", "class_id": "INVALID", "is_graduating": True, "graduation_year": 2024, "active": True}
./docs/contracts/contract-v0.1.md:393:{"user_id": "2021001", "name": "边界2", "role": "student", "class_id": "CS2021-01", "is_graduating": False, "graduation_year": 2025, "active": True}
./docs/contracts/contract-v0.1.md:398:{"user_id": "2019001", "name": "边界3", "role": "student", "class_id": "CS2019-01", "is_graduating": True, "graduation_year": 2024, "active": True}
docs/week3-day0-seed-data-requirements.md:31:| graduation_year | 2024 | 2024 |
./docs/数据对接说明文档.md:63:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
./docs/数据对接说明文档.md:68:| 毕业年份 | graduation_year | 整数 | 是 | 预计毕业年份 | 2026 |
./docs/数据对接说明文档.md:75:| 手机号 | phone | 文本 | 用于找回密码 | 13800138000 |
./docs/数据对接说明文档.md:76:| 邮箱 | email | 文本 | 用于通知 | zhangsan@example.com |
./docs/数据对接说明文档.md:92:student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
./docs/数据对接说明文档.md:165:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
./docs/数据对接说明文档.md:166:| 手机号 | phone | 文本 | 否 | 联系电话 | 13900139000 |
./docs/数据对接说明文档.md:167:| 邮箱 | email | 文本 | 否 | 联系邮箱 | wanglaoshi@example.com |
./docs/数据对接说明文档.md:180:employee_id,name,department,phone,email,is_active
./docs/superpowers/plans/2026-05-27-implementation-plan.md:225:   - 定义User模型（继承AbstractUser）
docs/phase4c-xg-field-coverage.md:32:| `phone` | string | 手机号 | 文档样例 |
docs/phase4c-xg-field-coverage.md:34:| `department` | string | 院系/部门 | 文档样例 |
docs/phase4c-xg-field-coverage.md:47:- `graduation_year`：毕业年份
docs/phase4c-xg-field-coverage.md:48:- `email`：邮箱
docs/phase4c-xg-field-coverage.md:52:## 三、内部User模型字段清单
docs/phase4c-xg-field-coverage.md:68:| `graduation_year` | integer | 学生必填 | 毕业年份 |
docs/phase4c-xg-field-coverage.md:74:| `phone` | string | 手机号（用于找回密码、通知） |
docs/phase4c-xg-field-coverage.md:75:| `email` | string | 邮箱（用于通知） |
docs/phase4c-xg-field-coverage.md:76:| `department` | string | 院系/部门（用于展示） |
docs/phase4c-xg-field-coverage.md:96:| `User.phone` | `phone` | 🟡 待确认 | **可选**。缺失则置为NULL。 |
docs/phase4c-xg-field-coverage.md:97:| `User.department` | `department` | 🟡 待确认 | **可选**。缺失则置为NULL。 |
docs/phase4c-xg-field-coverage.md:121:| `User.graduation_year` | 未知 | 🔴 缺失 | **学生必填，API无法提供**。<br>- 继续由CSV/手工维护<br>- API同步时不覆盖此字段<br>- 新用户如果缺失，标记为`skip_reason: missing_graduation_year` |
docs/phase4c-xg-field-coverage.md:144:| `phone`缺失 | 置为NULL（新用户）或保持原值（已存在用户） |
docs/phase4c-xg-field-coverage.md:145:| `email`缺失 | 置为NULL（新用户）或保持原值（已存在用户） |
docs/phase4c-xg-field-coverage.md:146:| `department`缺失 | 置为NULL（新用户）或保持原值（已存在用户） |
docs/phase4c-xg-field-coverage.md:149:| `graduation_year`缺失 | 保持原值（不覆盖），新用户跳过并标记`missing_graduation_year` |
docs/phase4c-xg-field-coverage.md:188:| **CSV导入（主）** | `user_id`, `name`, `role`, `class_id`, `is_graduating`, `graduation_year` | 学生创建和核心业务字段由CSV维护 |
docs/phase4c-xg-field-coverage.md:189:| **学工API（补充）** | `phone`, `email`, `department`, `updated_at` | API仅补充或更新非核心字段 |
docs/phase4c-xg-field-coverage.md:193:**Phase 1（当前）：CSV主导 + API补充**
docs/phase4c-xg-field-coverage.md:194:- CSV导入创建所有学生用户（包含`class_id`/`is_graduating`/`graduation_year`）
docs/phase4c-xg-field-coverage.md:195:- 学工API同步仅更新已存在用户的`phone`/`email`/`department`
docs/phase4c-xg-field-coverage.md:199:- 前提：live测试确认学工API能提供`class_id`/`is_graduating`/`graduation_year`
docs/phase4c-xg-field-coverage.md:226:    "phone": "13800138000",
docs/phase4c-xg-field-coverage.md:227:    "department": "计算机学院",
docs/phase4c-xg-field-coverage.md:234:    "phone": "13800138001",
docs/phase4c-xg-field-coverage.md:254:    "phone": "13800138000",
docs/phase4c-xg-field-coverage.md:255:    "department": "计算机学院",
docs/phase4c-xg-field-coverage.md:258:    "graduation_year": None,  # API不提供
docs/phase4c-xg-field-coverage.md:267:    "phone": "13800138001",
docs/phase4c-xg-field-coverage.md:268:    "department": None,
docs/phase4c-xg-field-coverage.md:271:    "graduation_year": None,
docs/phase4c-xg-field-coverage.md:280:    "phone": None,
docs/phase4c-xg-field-coverage.md:281:    "department": None,
docs/phase4c-xg-field-coverage.md:284:    "graduation_year": None,
docs/phase4c-xg-field-coverage.md:314:3. 是否提供`class_id`/`is_graduating`/`graduation_year`
./docs/templates/辅导员基本信息导入模板.csv:1:employee_id,name,department,phone,email,is_active
./docs/acceptance/phase4c-evidence-index.md:103:| `students_template.csv` | student_id, name, class_id, is_graduating, graduation_year |
docs/PROJECT-SUMMARY.md:251:- ✓ User模型和认证
docs/PROJECT-SUMMARY.md:252:  - User模型（user_id、name、role、class_id、is_graduating、graduation_year）
docs/PROJECT-SUMMARY.md:1257:  - counselors.csv: active → is_active, 添加department字段
docs/PROJECT-SUMMARY.md:1259:  - students.csv: 移除active字段, 添加department/major/grade字段
docs/PROJECT-SUMMARY.md:2229:- API/CSV并存策略：Phase 1（CSV主导+API补充）
docs/PROJECT-SUMMARY.md:2233:- ✅ API初期只补充phone/email/department，不创建新用户
docs/PROJECT-SUMMARY.md:2234:- ✅ class_id/is_graduating/graduation_year继续由CSV维护
docs/PROJECT-SUMMARY.md:2289:1. User模型缺失phone/email/department字段
docs/PROJECT-SUMMARY.md:2291:   - 字段契约定义为API补充字段
docs/PROJECT-SUMMARY.md:2292:   - 但模型只到graduation_year
docs/PROJECT-SUMMARY.md:2293:   - Step 4B真实upsert阻塞
docs/PROJECT-SUMMARY.md:2301:- ⏸ Step 4B：真实upsert（等待模型扩展决策）
docs/PROJECT-SUMMARY.md:2302:- ⏸ Step 5：命令入口（等待Step 4B）
docs/PROJECT-SUMMARY.md:2307:- 待讨论：User模型扩展策略（增加phone/email/department）
docs/PROJECT-SUMMARY.md:2333:- existing_count, missing_local_count, would_update_count
docs/PROJECT-SUMMARY.md:2339:- 关键质疑：5个Q（异常处理/would_update准确性/conflicts结构/skipped统计/测试场景5必要性）
docs/PROJECT-SUMMARY.md:2359:- docstring明确would_update_count为候选数语义
docs/PROJECT-SUMMARY.md:2381:- ⏭ 下一步：User模型扩展决策（增加phone/email/department字段）
docs/PROJECT-SUMMARY.md:2382:- ⏸ Step 4B：真实upsert（等待模型扩展）
docs/superpowers/plans/2026-05-27-implementation-plan.md:225:   - 定义User模型（继承AbstractUser）
docs/数据对接说明文档.md:63:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
docs/数据对接说明文档.md:68:| 毕业年份 | graduation_year | 整数 | 是 | 预计毕业年份 | 2026 |
docs/数据对接说明文档.md:75:| 手机号 | phone | 文本 | 用于找回密码 | 13800138000 |
docs/数据对接说明文档.md:76:| 邮箱 | email | 文本 | 用于通知 | zhangsan@example.com |
docs/数据对接说明文档.md:92:student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
docs/数据对接说明文档.md:165:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
docs/数据对接说明文档.md:166:| 手机号 | phone | 文本 | 否 | 联系电话 | 13900139000 |
docs/数据对接说明文档.md:167:| 邮箱 | email | 文本 | 否 | 联系邮箱 | wanglaoshi@example.com |
docs/数据对接说明文档.md:180:employee_id,name,department,phone,email,is_active
docs/templates/辅导员基本信息导入模板.csv:1:employee_id,name,department,phone,email,is_active
docs/templates/学生基本信息导入模板.csv:1:student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
./docs/acceptance/phase4c-acceptance-checklist.md:78:| counselors.csv字段统一 | ✅ 通过 | `employee_id, name, department, is_active` |
./docs/acceptance/phase4c-acceptance-checklist.md:80:| students.csv字段统一 | ✅ 通过 | `student_id, name, class_id, is_graduating, graduation_year` |
./docs/week3-day0-seed-data-requirements.md:31:| graduation_year | 2024 | 2024 |
docs/contracts/contract-v0.1.md:26:    graduation_year: Optional[int] = None # 毕业年份（仅学生）
docs/contracts/contract-v0.1.md:225:**说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。
docs/contracts/contract-v0.1.md:343:    {"user_id": "2020001", "name": "张三", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
docs/contracts/contract-v0.1.md:344:    {"user_id": "2020002", "name": "李四", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
docs/contracts/contract-v0.1.md:345:    {"user_id": "2020003", "name": "王五", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
docs/contracts/contract-v0.1.md:346:    {"user_id": "2020004", "name": "赵六", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
docs/contracts/contract-v0.1.md:347:    {"user_id": "2020005", "name": "钱七", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
docs/contracts/contract-v0.1.md:348:    {"user_id": "2020006", "name": "孙八", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
docs/contracts/contract-v0.1.md:349:    {"user_id": "2020007", "name": "周九", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
docs/contracts/contract-v0.1.md:350:    {"user_id": "2020008", "name": "吴十", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
docs/contracts/contract-v0.1.md:351:    {"user_id": "2020009", "name": "郑十一", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
docs/contracts/contract-v0.1.md:352:    {"user_id": "2020010", "name": "王十二", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
docs/contracts/contract-v0.1.md:359:    {"user_id": "T001", "name": "李老师", "role": "counselor", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
docs/contracts/contract-v0.1.md:360:    {"user_id": "T002", "name": "王老师", "role": "counselor", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
docs/contracts/contract-v0.1.md:367:    {"user_id": "D001", "name": "赵主任", "role": "dean", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
docs/contracts/contract-v0.1.md:383:{"user_id": "2020099", "name": "边界1", "role": "student", "class_id": "INVALID", "is_graduating": True, "graduation_year": 2024, "active": True}
docs/contracts/contract-v0.1.md:393:{"user_id": "2021001", "name": "边界2", "role": "student", "class_id": "CS2021-01", "is_graduating": False, "graduation_year": 2025, "active": True}
docs/contracts/contract-v0.1.md:398:{"user_id": "2019001", "name": "边界3", "role": "student", "class_id": "CS2019-01", "is_graduating": True, "graduation_year": 2024, "active": True}
./docs/api说明.txt:28:phone	否	string	手机号
./docs/api说明.txt:31:departmentId	否	string	部门Id ,查询多个用半角逗号分隔例如: 203,204
./docs/api说明.txt:32:departmentCode	否	string	部门code ,查询多个用半角逗号分隔例如: 203,204
./docs/api说明.txt:52:                "phone": "18626409896",
./docs/api说明.txt:69:                        "department_code": "C100260159402712838523",
./docs/api说明.txt:84:                        "department_code": "C100261159409057535680",
./docs/api说明.txt:98:                    "phone": "18626409896",
./docs/api说明.txt:112:                "department": [
./docs/api说明.txt:119:                        "department_code": "C100261159409057535680",
./docs/api说明.txt:129:                            "department_id": 47
./docs/api说明.txt:168:phone	手机号
./docs/api说明.txt:174:user.phone	手机号
./docs/api说明.txt:185:department.name	部门名称 name
./docs/api说明.txt:186:department.third_code	部门的在对接系统中的标识/来源可能为学校自建/钉钉接入/企业微信接入
./docs/api说明.txt:187:department.department_code	当前部门的在青橄榄系统中对外提供的唯一Code
./docs/api说明.txt:188:department.level	当前部门级别
./docs/api说明.txt:189:department.parent_id	父级主键ID
./docs/api说明.txt:190:department.key	该层级所对应的路由
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:277:2. `graduation_year` 示例应与当前项目日期保持一致（2026）
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:278:3. `phone` 是否可选需要结合微信绑定策略确认
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:285:| `graduation_year` 示例改为2026 | ✅ 接受，统一为2026 |
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:286:| `phone` 可选性确认 | ✅ 接受，需要在待反馈问题中询问宿管系统 |
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:482:- `graduation_year` 示例从2024改为2026
docs/design/2026-05-27-system-design.md:276:    phone VARCHAR(20) COMMENT '手机号',
docs/design/2026-05-27-system-design.md:277:    email VARCHAR(100) COMMENT '邮箱',
docs/design/2026-05-27-system-design.md:279:    department VARCHAR(100) COMMENT '院系',
docs/design/2026-05-27-system-design.md:915:      "department": "计算机学院"
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:47:- 院系（department）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:51:- 手机号（phone，可选）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:52:- 邮箱（email，可选）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:95:- 手机号（phone）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:96:- 邮箱（email）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:97:- 院系（department，可选）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:119:- 院系（department）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:145:- 手机号（phone）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:146:- 邮箱（email）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:44:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:49:| 毕业年份 | graduation_year | 整数 | 是 | 预计毕业年份 | 2024 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:56:| 手机号 | phone | 文本 | 否 | 用于通知 | 13800138000 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:57:| 邮箱 | email | 文本 | 否 | 用于通知 | student@example.com |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:67:    department,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:72:    graduation_year,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:74:    phone,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:75:    email
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:78:  AND graduation_year = 2024;
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:83:GET /api/students?graduation_year=2024&is_graduating=true
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:134:WHERE graduation_year = 2024;
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:157:| 手机号 | phone | 文本 | 是 | 用于通知 | 13900139000 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:158:| 邮箱 | email | 文本 | 否 | 用于通知 | teacher@example.com |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:159:| 院系 | department | 文本 | 否 | 所属院系 | 计算机学院 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:170:    phone,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:171:    email,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:172:    department,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:211:| 院系 | department | 文本 | 否 | 所属院系 | 计算机学院 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:225:    department,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:272:| 手机号 | phone | 文本 | 是 | 用于通知 | 13700137000 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:273:| 邮箱 | email | 文本 | 否 | 用于通知 | admin@example.com |
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:58:INSERT INTO users (student_id, name, department, ...)
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:59:SELECT student_id, name, department, ...
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:63:    department = VALUES(department),
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:121:    department VARCHAR(100),
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:125:    phone VARCHAR(20),
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:126:    email VARCHAR(100),
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:218:student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:277:    graduation_year INT NOT NULL,               -- 2026
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:289:-- 只导入is_graduating=true且graduation_year=2026的学生
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:292:  AND graduation_year = (SELECT graduation_year FROM graduation_batches WHERE is_active = true);
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:331:    {"row": 8, "field": "phone", "error": "手机号格式不正确"}
./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:195:            student__department=request.user.department
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:56:字段整体合理，能支撑首版业务。`student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`is_graduating` 作为必填基本可接受。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:63:2. `graduation_year` 示例应与当前项目日期保持一致。  
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:64:   文档创建时间为 2026-05-27，但 SQL 示例使用 `graduation_year = 2024`。建议统一为 `2026` 或说明“示例年份按实际毕业届别替换”。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:66:3. `phone` 是否可选需要结合微信绑定策略确认。  
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:89:1. `phone` 标为必填偏强。  
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:278:2. `phone` 是否必填取决于通知和找回密码方案；如果不依赖短信，可改为建议字段。
./backend/scripts/diagnose_xg_api.py:71:                    'phone': user.get('phone', '')[:3] + '****' + user.get('phone', '')[-4:] if user.get('phone') and len(user.get('phone', '')) > 7 else None
./backend/scripts/diagnose_xg_api.py:86:                    'phone': any('phone' in u for u in users)
./backend/scripts/diagnose_xg_api.py:131:        lines.append(f"字段覆盖: name={cov['name']} number={cov['number']} phone={cov['phone']}")
./backend/data/templates/counselors_template.csv:1:employee_id,name,department,is_active,password
./backend/data/templates/students_template.csv:1:student_id,name,department,major,class_id,grade,graduation_year,is_graduating,password
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:29:| 毕业资格/离校资格字段 | 教务系统 | P0 字段，非 P0 独立接口 | 如果系统只导入当届毕业生，可通过导入范围满足；如果导入全量学生，则必须在学生基本信息中带 `graduation_year`、`graduation_status` 或 `eligible_for_leave`。不建议首版单独建设学籍 API。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:46:| 学生基本信息 | CSV/Excel 批量导入 | 教务系统 API | 首版按毕业届别导入更容易落地。字段建议包括 `student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:47:| 辅导员基本信息 | CSV/Excel 批量导入 | 人事系统 API 或手动创建 | 约 50 人规模下，批量导入足够。字段建议包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:116:9. **通知联系方式。** `phone`、`email` 对提醒和异常联系有价值；微信 `openid` 应通过用户绑定产生，不应从外部系统导入。
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:152:    phone = models.CharField(max_length=20, null=True)
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:153:    email = models.CharField(max_length=100, null=True)
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:155:    department = models.CharField(max_length=100, null=True)
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:377:### 9.3 宿舍系统字段契约不足
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:72:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:77:| 毕业年份 | graduation_year | 整数 | 是 | 预计毕业年份 | 2026 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:84:| 手机号 | phone | 文本 | 用于找回密码或二次验证 | 13800138000 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:85:| 邮箱 | email | 文本 | 用于通知或找回密码 | zhangsan@example.com |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:91:- `graduation_year`：示例统一为2026（与当前项目日期保持一致）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:96:student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:102:- 只导入当届毕业生（`is_graduating=true` 且 `graduation_year=2026`）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:160:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:161:| 手机号 | phone | 文本 | 否 | 联系电话 | 13900139000 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:162:| 邮箱 | email | 文本 | 否 | 联系邮箱 | wanglaoshi@example.com |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:172:employee_id,name,department,phone,email,is_active
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:249:| 部门 | department | 文本 | 是 | 所属部门 | 学工部 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:250:| 手机号 | phone | 文本 | 否 | 联系电话 | 13700137000 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:251:| 邮箱 | email | 文本 | 否 | 联系邮箱 | zhaozr@example.com |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:298:    department VARCHAR(100),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:303:    graduation_year INT,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:305:    phone VARCHAR(20),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:306:    email VARCHAR(100)
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:313:    department VARCHAR(100),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:314:    phone VARCHAR(20),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:315:    email VARCHAR(100)
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:335:INSERT INTO users (student_id, name, department, class_id, role, is_active, password_setup_required, ...)
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:336:SELECT student_id, name, department, class_id, 'student', true, true, ...
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:340:    department = VALUES(department),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:396:    {"row": 8, "field": "phone", "error": "手机号格式不正确"}
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:474:| 学生账号 | 当届毕业生 | 1000人/届 | 只导入当届（`is_graduating=true` 且 `graduation_year=2026`） |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:487:    graduation_year INT NOT NULL,               -- 2026
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:505:  AND graduation_year = (SELECT graduation_year FROM graduation_batches WHERE is_active = true);
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:617:    department VARCHAR(100),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:622:    graduation_year INT,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:624:    phone VARCHAR(20),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:625:    email VARCHAR(100)
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:634:    department VARCHAR(100),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:635:    phone VARCHAR(20),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:636:    email VARCHAR(100)
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:676:    graduation_year INT NOT NULL,
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:151:    department: str
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:155:    graduation_year: int
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:157:    phone: Optional[str] = None
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:158:    email: Optional[str] = None
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:249:        Student(student_id="2020005", name="钱七", class_id="CS2020-01", is_graduating=True, graduation_year=2027),  # 延期毕业
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:107:    department: str
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:111:    graduation_year: int
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:113:    phone: Optional[str] = None
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:114:    email: Optional[str] = None
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:221:        Student(student_id="2020005", name="钱七", class_id="CS2020-01", is_graduating=True, graduation_year=2027),  # 延期毕业
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:56:| 学生/用户 | student_id、name、role、class_id、is_graduating、graduation_year、active | 微信openid、手机号、完整个人档案 |
./docs/design/2026-05-27-system-design.md:276:    phone VARCHAR(20) COMMENT '手机号',
./docs/design/2026-05-27-system-design.md:277:    email VARCHAR(100) COMMENT '邮箱',
./docs/design/2026-05-27-system-design.md:279:    department VARCHAR(100) COMMENT '院系',
./docs/design/2026-05-27-system-design.md:915:      "department": "计算机学院"
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:51:    department VARCHAR(100),
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:56:    graduation_year INT,
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:58:    phone VARCHAR(20),
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:59:    email VARCHAR(100)
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:66:    department VARCHAR(100),
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:67:    phone VARCHAR(20),
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:68:    email VARCHAR(100)
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:86:INSERT INTO users (student_id, name, department, major, class_id, role, is_active, ...)
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:87:SELECT student_id, name, department, major, class_id, 'student', true, ...
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:91:    department = VALUES(department),
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:151:    department: str
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:155:    graduation_year: int
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:157:    phone: Optional[str] = None
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:158:    email: Optional[str] = None
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:249:        Student(student_id="2020005", name="钱七", class_id="CS2020-01", is_graduating=True, graduation_year=2027),  # 延期毕业
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:56:| 学生/用户 | student_id、name、role、class_id、is_graduating、graduation_year、active | 微信openid、手机号、完整个人档案 |
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:72:> **说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:126:4. **薄认证**：1-2天（User模型、学号+密码登录、JWT）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:213:  - User模型
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:107:    department: str
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:111:    graduation_year: int
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:113:    phone: Optional[str] = None
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:114:    email: Optional[str] = None
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:221:        Student(student_id="2020005", name="钱七", class_id="CS2020-01", is_graduating=True, graduation_year=2027),  # 延期毕业
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:99:                department="计算机学院",
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:103:                graduation_year=2024,
./docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:72:> **说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。
./backend/config/settings/dev.py:8:# Console email backend for development
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:17:1. `would_update_count`在docstring中被定义为"现有学生同步候选数，不代表当前模型可持久化写入数"。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:18:2. 字段gap warning已强化，包含候选数量、`sync candidates exist`、`no API supplemental fields can be persisted`、`phone/email/department`以及name覆盖策略未批准的阻塞说明。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:51:`plan_xg_user_sync()`当前warning已经包含`lacks class_id/is_graduating/graduation_year`，符合Phase 1不创建边界。测试目前只断言`would_create_but_blocked`。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:58:self.assertIn('graduation_year', warning_text)
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:77:通过。`would_update_count`已明确为候选数，不是当前可持久化写入数。该定义与doc 99建议一致，也避免Step 4B误以为已有真实upsert能力。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:79:`would_update_count += 1`附近已有"已存在学生，计入would_update"注释。更严谨的写法可以改为"已存在学生，计入同步候选数；不代表当前模型可落库更新"，但不是阻塞项，因为docstring和warning已经说明完整语义。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:85:- 候选数量：`{would_update_count} sync candidates exist`
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:87:- 缺失字段：`phone/email/department`
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:103:2. `test_existing_student_to_candidate`：覆盖`existing_count=1`、`would_update_count=1`候选数语义。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:106:5. `test_core_fields_readonly`：覆盖服务执行后`class_id/is_graduating/graduation_year/name`不变。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:122:### Q1：would_update_count修复是否充分？
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:124:充分。docstring + warning已经解决P1语义风险。建议把`would_update_count += 1`附近注释也改成"候选数"措辞，但这只是清晰度增强，不影响通过。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:128:服务实现完整，测试基本完整。建议补充断言`class_id/is_graduating/graduation_year`出现在warning中，以锁定"为什么不创建"的核心字段gap。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:135:skipped_count + missing_local_count + len(conflicts) + would_update_count == total_fetched
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:142:- existing再分为`conflicts`和`would_update candidates`。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:148:足够。当前Step 4A不根据`graduation_year`做分支判断，只需要验证字段不被修改。不同毕业年份边界应留到出现年份过滤或Step 4B写入策略时再加。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:203:4. 进入Step 4B前置讨论：User模型扩展与name覆盖策略。
./docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:117:字段覆盖: name=yes number=yes phone=yes department=yes user_identity=yes
./docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:118:样本: name=张* number=17**** phone=186****9896
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:18:4. ✅ **最快路径正确**：字段契约 → 只读mapper → 幂等upsert → command 是最低风险路径
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:51:**必要动作：** 在字段契约中明确`class_id`来源，缺失时继续依赖CSV。
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:57:**Codex指出：** CSV导入要求`is_graduating`和`graduation_year`，学工API样例未证明能提供。
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:63:**必要动作：** 在字段契约中明确这两个字段缺失时的处理规则（继续CSV维护 or 禁止同步）。
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:76:**必要动作：** 在字段契约中明确`user_identity`值域映射，未知值跳过并报告。
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:107:### User模型必需字段
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:113:- graduation_year (学生必填)
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:126:| User.graduation_year | 未确认 | 缺失 | 继续由CSV/手工维护，API不覆盖 |
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:166:            'graduation_year': int | None,
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:182:7. graduation_year缺失返回None
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:99:                department="计算机学院",
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:103:                graduation_year=2024,
./docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:170:- CSV字段契约与数据对接文档一致。
./docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:109:2. **业务字段层：** 宽松采样，记录 `name/number/phone/identity_id/department/user_identity/user_auth_extra_field` 是否出现，不因业务字段缺失直接失败。
./docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:134:字段: name=yes number=yes phone=yes department=yes user_identity=yes
./docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:135:样本: name=张* number=17 phone=186****9896
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:277:2. `graduation_year` 示例应与当前项目日期保持一致（2026）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:278:3. `phone` 是否可选需要结合微信绑定策略确认
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:285:| `graduation_year` 示例改为2026 | ✅ 接受，统一为2026 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:286:| `phone` 可选性确认 | ✅ 接受，需要在待反馈问题中询问宿管系统 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:482:- `graduation_year` 示例从2024改为2026
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:29:| 毕业资格/离校资格字段 | 教务系统 | P0 字段，非 P0 独立接口 | 如果系统只导入当届毕业生，可通过导入范围满足；如果导入全量学生，则必须在学生基本信息中带 `graduation_year`、`graduation_status` 或 `eligible_for_leave`。不建议首版单独建设学籍 API。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:46:| 学生基本信息 | CSV/Excel 批量导入 | 教务系统 API | 首版按毕业届别导入更容易落地。字段建议包括 `student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:47:| 辅导员基本信息 | CSV/Excel 批量导入 | 人事系统 API 或手动创建 | 约 50 人规模下，批量导入足够。字段建议包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:116:9. **通知联系方式。** `phone`、`email` 对提醒和异常联系有价值；微信 `openid` 应通过用户绑定产生，不应从外部系统导入。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:12:**结论：通过。批准提交当前Step 4A实现与测试，可进入Step 4B模型扩展讨论。**
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:14:本轮P1修复已经落地：`would_update_count`被明确约束为"现有学生同步候选数"，不再暗示当前模型已有可持久化更新字段；warning文本也明确指出API补充字段暂不能落库。新增测试使用Django `TestCase`和真实测试数据库，覆盖doc 99要求的8个关键场景。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:24:`would_update_count`注释为"现有学生同步候选数，不代表当前模型可持久化写入数"，准确传达了doc 99要求的候选数语义。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:33:- 候选数量：`{would_update_count} sync candidates exist`
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:35:- 阻塞解除条件：增加`phone/email/department`或批准`name`覆盖策略
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:37:这足以避免把`would_update_count`误解为真实DB更新数。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:64:2. `test_existing_student_to_candidate`：覆盖`existing_count=1`、`would_update_count=1`候选数语义，通过。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:67:5. `test_core_fields_readonly`：覆盖`class_id/is_graduating/graduation_year/name`不变，通过。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:78:### Q1：would_update_count修复是否充分
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:80:充分。docstring和warning已锁定候选数语义。`would_update_count += 1`附近当前注释仍偏简短，但不构成阻塞；若要进一步降低歧义，可后续把该行注释改为"已存在学生，计入同步候选数；当前模型仍不可写入API补充字段"。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:84:完整。当前断言覆盖不创建、计数和`would_create_but_blocked`。服务warning已包含`class_id/is_graduating/graduation_year`，如需更强锁定可增加断言，但现有测试已经足够支撑Step 4A。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:90:`skipped_count + missing_local_count + len(conflicts) + would_update_count == total_fetched`
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:92:这避免了`existing_count`包含conflict和candidate导致的重复计数。更完整的关系也成立：`mapped = missing_local + existing`，`existing = would_update + conflicts`。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:140:3. **批准进入Step 4B模型扩展讨论。**
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:142:Step 4B前置建议：优先决策User模型是否新增`phone/email/department`，以及`name`是否允许由学工API覆盖；在该决策完成前，不应把Step 4A的`would_update_count`解释为真实可写更新数。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:377:### 9.3 宿舍系统字段契约不足
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:19:2. **Step 4B：在服务层实现受限真实写入**
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:28:当前 `map_xg_user_to_internal()` 输出 `phone` 和 `department`，字段覆盖契约也把 `phone`、`email`、`department`定义为 API 补充字段。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:38:- `graduation_year`
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:40:没有 `phone`、`email`、`department` 持久化字段。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:42:这意味着如果 Step 4 现在直接做“幂等 upsert 并写库”，实际可安全写入的 API 字段非常有限。`class_id`、`is_graduating`、`graduation_year`按共识不由 API 覆盖；`role`仅用于过滤学生；`user_id`是主键；剩下只有 `name` 可能可更新，但它属于 CSV 主导核心字段，不应在没有明确策略时被 API 静默覆盖。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:46:### P1：字段契约与 mapper 对“新用户是否可创建”的边界需要由 Step 4 承担
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:48:字段契约明确 Phase 1 中学工 API 不创建新学生，因为缺少 `class_id`、`is_graduating`、`graduation_year`。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:54:- `graduation_year=None`
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:90:3. 写入字段范围清晰：**目前不满足**，因为模型缺少 `phone`/`department`/`email`。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:119:- `would_update_count`
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:129:- 当前没有模型字段承接 `phone`/`department`：输出 warning，不能声明可写入。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:137:- 不覆盖 `class_id`、`is_graduating`、`graduation_year`
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:138:- 无 phone/department 模型字段时输出明确 warning
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:140:### Step 4B：受限真实写入（需 Step 4A 后再决定）
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:144:1. **模型扩展路线**：给 `User` 增加 `phone`、`email`、`department` 等 API 补充字段，再实现幂等更新。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:177:   - 当前模型与字段契约不一致，不能假装 `phone`/`department` 可 upsert。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:197:1. mapper 返回 `phone`/`department` 是合理的，但 Step 4 不能把它们视为可持久化字段，除非模型扩展。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:198:2. 字段契约中提到 `email`，但 mapper 当前不提取 `email`；如果未来模型扩展包含邮箱，需要补 mapper 和测试。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:210:3. 暂不做 Step 4B 真实 upsert，先由 Step 4A 暴露“当前无可写补充字段”的事实。
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:47:- 院系（department）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:51:- 手机号（phone，可选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:52:- 邮箱（email，可选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:95:- 手机号（phone）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:96:- 邮箱（email）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:97:- 院系（department，可选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:119:- 院系（department）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:145:- 手机号（phone）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:146:- 邮箱（email）
./docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:117:- CSV字段契约与数据对接文档一致
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:72:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:77:| 毕业年份 | graduation_year | 整数 | 是 | 预计毕业年份 | 2026 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:84:| 手机号 | phone | 文本 | 用于找回密码或二次验证 | 13800138000 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:85:| 邮箱 | email | 文本 | 用于通知或找回密码 | zhangsan@example.com |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:91:- `graduation_year`：示例统一为2026（与当前项目日期保持一致）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:96:student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:102:- 只导入当届毕业生（`is_graduating=true` 且 `graduation_year=2026`）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:160:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:161:| 手机号 | phone | 文本 | 否 | 联系电话 | 13900139000 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:162:| 邮箱 | email | 文本 | 否 | 联系邮箱 | wanglaoshi@example.com |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:172:employee_id,name,department,phone,email,is_active
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:249:| 部门 | department | 文本 | 是 | 所属部门 | 学工部 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:250:| 手机号 | phone | 文本 | 否 | 联系电话 | 13700137000 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:251:| 邮箱 | email | 文本 | 否 | 联系邮箱 | zhaozr@example.com |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:298:    department VARCHAR(100),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:303:    graduation_year INT,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:305:    phone VARCHAR(20),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:306:    email VARCHAR(100)
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:313:    department VARCHAR(100),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:314:    phone VARCHAR(20),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:315:    email VARCHAR(100)
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:335:INSERT INTO users (student_id, name, department, class_id, role, is_active, password_setup_required, ...)
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:336:SELECT student_id, name, department, class_id, 'student', true, true, ...
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:340:    department = VALUES(department),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:396:    {"row": 8, "field": "phone", "error": "手机号格式不正确"}
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:474:| 学生账号 | 当届毕业生 | 1000人/届 | 只导入当届（`is_graduating=true` 且 `graduation_year=2026`） |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:487:    graduation_year INT NOT NULL,               -- 2026
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:505:  AND graduation_year = (SELECT graduation_year FROM graduation_batches WHERE is_active = true);
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:617:    department VARCHAR(100),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:622:    graduation_year INT,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:624:    phone VARCHAR(20),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:625:    email VARCHAR(100)
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:634:    department VARCHAR(100),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:635:    phone VARCHAR(20),
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:636:    email VARCHAR(100)
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:676:    graduation_year INT NOT NULL,
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:1:# Phase 4C Step 4B前置 - User模型扩展策略讨论请求
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:5:**讨论目标：** User模型扩展决策（Step 4B实现前置条件）  
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:14:**Step 4B阻塞原因：** User模型字段gap（doc 95/99/103识别）
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:15:- mapper输出phone/department
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:16:- 字段契约定义phone/email/department为API补充字段
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:17:- User模型只到graduation_year，缺这些字段
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:18:- would_update_count为候选数，无实际可写补充字段
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:20:**Codex建议（doc 103）：** 优先决策模型扩展策略，再实现Step 4B真实upsert。
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:26:### 问题1：是否新增phone/email/department字段？
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:28:**选项A：扩展User模型**
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:29:- 新增字段：phone, email, department
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:34:- 保持当前7字段（user_id/name/role/active/class_id/is_graduating/graduation_year）
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:35:- API补充字段不持久化
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:42:- 字段契约定义name为CSV主导核心字段
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:56:### 选项组合1：扩展模型 + 允许name覆盖
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:59:- Step 4B可实现完整API补充字段upsert
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:60:- phone/email/department可持久化
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:65:- name覆盖可能与CSV冲突
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:69:### 选项组合2：扩展模型 + 不允许name覆盖
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:72:- Step 4B可持久化phone/email/department
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:87:- Step 4A的would_update报告已足够
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:90:- Step 4B无实际可写补充字段
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:92:- would_update_count候选无法转为真实更新
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:100:### phone/email/department字段价值
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:108:- CSV：不包含phone/email/department
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:109:- 学工API：包含phone/department，email需补充提取
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:136:        migrations.AddField('User', 'phone', CharField(max_length=20, null=True, blank=True)),
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:137:        migrations.AddField('User', 'email', EmailField(max_length=254, null=True, blank=True)),
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:138:        migrations.AddField('User', 'department', CharField(max_length=100, null=True, blank=True)),
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:152:- CSV主导：user_id/name/role/class_id/is_graduating/graduation_year
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:153:- API补充：phone/email/department
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:155:**name覆盖策略选项：**
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:178:- 字段契约定义
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:187:### 审查要点2：phone/email/department必要性
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:192:- 如果不扩展，Step 4B应实现什么
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:194:### 审查要点3：name覆盖策略
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:201:### 审查要点4：Step 4B实现范围
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:204:- 扩展模型后Step 4B应实现什么
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:205:- 不扩展模型Step 4B应实现什么（或跳过）
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:206:- 是否需要Step 4B-lite（仅name更新）
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:212:### Q1：字段契约定义 vs 当前需求
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:214:字段契约定义phone/email/department为API补充字段，但当前系统明确需要这些字段吗？
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:223:**影响：** name覆盖策略和字段主导权
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:231:### Q4：mapper email提取
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:233:字段契约包含email，但mapper未提取。
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:235:**是否需要：** 补充mapper提取email字段？
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:237:### Q5：Step 4B最小范围
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:239:如果扩展模型，Step 4B最小实现是什么？
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:240:- 只更新phone/department？
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:241:- 包含email？
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:255:   - 是否新增phone/email/department
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:259:3. **name覆盖决策**
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:263:4. **Step 4B实施范围**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:44:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:49:| 毕业年份 | graduation_year | 整数 | 是 | 预计毕业年份 | 2024 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:56:| 手机号 | phone | 文本 | 否 | 用于通知 | 13800138000 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:57:| 邮箱 | email | 文本 | 否 | 用于通知 | student@example.com |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:67:    department,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:72:    graduation_year,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:74:    phone,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:75:    email
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:78:  AND graduation_year = 2024;
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:83:GET /api/students?graduation_year=2024&is_graduating=true
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:134:WHERE graduation_year = 2024;
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:157:| 手机号 | phone | 文本 | 是 | 用于通知 | 13900139000 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:158:| 邮箱 | email | 文本 | 否 | 用于通知 | teacher@example.com |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:159:| 院系 | department | 文本 | 否 | 所属院系 | 计算机学院 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:170:    phone,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:171:    email,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:172:    department,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:211:| 院系 | department | 文本 | 否 | 所属院系 | 计算机学院 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:225:    department,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:272:| 手机号 | phone | 文本 | 是 | 用于通知 | 13700137000 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:273:| 邮箱 | email | 文本 | 否 | 用于通知 | admin@example.com |
./docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:140:5. 字段采样：仅检查人员记录是否包含 `name/number/phone/identity_id/department/user_identity/updated_at` 等文档字段。
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:51:    department VARCHAR(100),
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:56:    graduation_year INT,
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:58:    phone VARCHAR(20),
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:59:    email VARCHAR(100)
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:66:    department VARCHAR(100),
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:67:    phone VARCHAR(20),
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:68:    email VARCHAR(100)
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:86:INSERT INTO users (student_id, name, department, major, class_id, role, is_active, ...)
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:87:SELECT student_id, name, department, major, class_id, 'student', true, ...
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:91:    department = VALUES(department),
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:13:Codex与Claude完全同意：不单独做Step 3.5，不做Step 4B真实upsert（先解决模型字段gap）。
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:31:### 2. 关键发现：User模型字段gap（P1）
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:34:- mapper输出phone/department/email
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:35:- User模型只到graduation_year
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:36:- 缺失：phone, email, department字段
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:37:- 影响：Step 4B不能实现真实upsert
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:39:**User模型当前字段：**
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:46:- graduation_year
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:49:- phone（mapper输出，字段契约定义为API补充）
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:50:- email（字段契约定义，mapper未提取）
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:51:- department（mapper输出，字段契约定义为API补充）
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:58:- Phase 1：API不创建新用户（缺class_id/is_graduating/graduation_year）
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:71:4. **已存在学生：** 计入existing_count, would_update_count
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:72:5. **核心字段保护：** 不覆盖class_id/is_graduating/graduation_year
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:73:6. **补充字段警告：** phone/department无模型字段 → 输出warnings
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:88:    'would_update_count': int,
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:96:### 6. Step 4B延后（等待决策）
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:101:- 给User增加phone/email/department
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:126:- Step 4B完成后再做
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:153:### Phase 3：Step 4B + Step 5（模型扩展后）
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:161:**mapper改进（如果模型扩展包含email）：**
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:162:- mapper增加email字段提取
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:163:- 增加test_email_field测试
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:176:**暂停点：** Step 4A完成后，讨论模型扩展策略，不自动执行Step 4B。
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:58:INSERT INTO users (student_id, name, department, ...)
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:59:SELECT student_id, name, department, ...
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:63:    department = VALUES(department),
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:121:    department VARCHAR(100),
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:125:    phone VARCHAR(20),
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:126:    email VARCHAR(100),
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:218:student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:277:    graduation_year INT NOT NULL,               -- 2026
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:289:-- 只导入is_graduating=true且graduation_year=2026的学生
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:292:  AND graduation_year = (SELECT graduation_year FROM graduation_batches WHERE is_active = true);
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:331:    {"row": 8, "field": "phone", "error": "手机号格式不正确"}
./docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:45:- 其他过滤参数（name, number, phone等）可选
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:126:4. **薄认证**：1-2天（User模型、学号+密码登录、JWT）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:213:  - User模型
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:195:            student__department=request.user.department
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:152:    phone = models.CharField(max_length=20, null=True)
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:153:    email = models.CharField(max_length=100, null=True)
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:155:    department = models.CharField(max_length=100, null=True)
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:17:1. `would_update_count`在docstring中被定义为"现有学生同步候选数，不代表当前模型可持久化写入数"。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:18:2. 字段gap warning已强化，包含候选数量、`sync candidates exist`、`no API supplemental fields can be persisted`、`phone/email/department`以及name覆盖策略未批准的阻塞说明。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:51:`plan_xg_user_sync()`当前warning已经包含`lacks class_id/is_graduating/graduation_year`，符合Phase 1不创建边界。测试目前只断言`would_create_but_blocked`。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:58:self.assertIn('graduation_year', warning_text)
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:77:通过。`would_update_count`已明确为候选数，不是当前可持久化写入数。该定义与doc 99建议一致，也避免Step 4B误以为已有真实upsert能力。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:79:`would_update_count += 1`附近已有"已存在学生，计入would_update"注释。更严谨的写法可以改为"已存在学生，计入同步候选数；不代表当前模型可落库更新"，但不是阻塞项，因为docstring和warning已经说明完整语义。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:85:- 候选数量：`{would_update_count} sync candidates exist`
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:87:- 缺失字段：`phone/email/department`
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:103:2. `test_existing_student_to_candidate`：覆盖`existing_count=1`、`would_update_count=1`候选数语义。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:106:5. `test_core_fields_readonly`：覆盖服务执行后`class_id/is_graduating/graduation_year/name`不变。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:122:### Q1：would_update_count修复是否充分？
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:124:充分。docstring + warning已经解决P1语义风险。建议把`would_update_count += 1`附近注释也改成"候选数"措辞，但这只是清晰度增强，不影响通过。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:128:服务实现完整，测试基本完整。建议补充断言`class_id/is_graduating/graduation_year`出现在warning中，以锁定"为什么不创建"的核心字段gap。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:135:skipped_count + missing_local_count + len(conflicts) + would_update_count == total_fetched
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:142:- existing再分为`conflicts`和`would_update candidates`。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:148:足够。当前Step 4A不根据`graduation_year`做分支判断，只需要验证字段不被修改。不同毕业年份边界应留到出现年份过滤或Step 4B写入策略时再加。
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:203:4. 进入Step 4B前置讨论：User模型扩展与name覆盖策略。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:56:字段整体合理，能支撑首版业务。`student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`is_graduating` 作为必填基本可接受。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:63:2. `graduation_year` 示例应与当前项目日期保持一致。  
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:64:   文档创建时间为 2026-05-27，但 SQL 示例使用 `graduation_year = 2024`。建议统一为 `2026` 或说明“示例年份按实际毕业届别替换”。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:66:3. `phone` 是否可选需要结合微信绑定策略确认。  
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:89:1. `phone` 标为必填偏强。  
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:278:2. `phone` 是否必填取决于通知和找回密码方案；如果不依赖短信，可改为建议字段。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:117:字段覆盖: name=yes number=yes phone=yes department=yes user_identity=yes
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:118:样本: name=张* number=17**** phone=186****9896
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:1:# Phase 4C Step 4B前置 - User模型扩展策略讨论请求
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:5:**讨论目标：** User模型扩展决策（Step 4B实现前置条件）  
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:14:**Step 4B阻塞原因：** User模型字段gap（doc 95/99/103识别）
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:15:- mapper输出phone/department
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:16:- 字段契约定义phone/email/department为API补充字段
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:17:- User模型只到graduation_year，缺这些字段
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:18:- would_update_count为候选数，无实际可写补充字段
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:20:**Codex建议（doc 103）：** 优先决策模型扩展策略，再实现Step 4B真实upsert。
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:26:### 问题1：是否新增phone/email/department字段？
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:28:**选项A：扩展User模型**
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:29:- 新增字段：phone, email, department
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:34:- 保持当前7字段（user_id/name/role/active/class_id/is_graduating/graduation_year）
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:35:- API补充字段不持久化
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:42:- 字段契约定义name为CSV主导核心字段
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:56:### 选项组合1：扩展模型 + 允许name覆盖
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:59:- Step 4B可实现完整API补充字段upsert
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:60:- phone/email/department可持久化
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:65:- name覆盖可能与CSV冲突
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:69:### 选项组合2：扩展模型 + 不允许name覆盖
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:72:- Step 4B可持久化phone/email/department
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:87:- Step 4A的would_update报告已足够
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:90:- Step 4B无实际可写补充字段
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:92:- would_update_count候选无法转为真实更新
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:100:### phone/email/department字段价值
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:108:- CSV：不包含phone/email/department
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:109:- 学工API：包含phone/department，email需补充提取
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:136:        migrations.AddField('User', 'phone', CharField(max_length=20, null=True, blank=True)),
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:137:        migrations.AddField('User', 'email', EmailField(max_length=254, null=True, blank=True)),
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:138:        migrations.AddField('User', 'department', CharField(max_length=100, null=True, blank=True)),
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:152:- CSV主导：user_id/name/role/class_id/is_graduating/graduation_year
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:153:- API补充：phone/email/department
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:155:**name覆盖策略选项：**
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:178:- 字段契约定义
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:187:### 审查要点2：phone/email/department必要性
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:192:- 如果不扩展，Step 4B应实现什么
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:194:### 审查要点3：name覆盖策略
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:201:### 审查要点4：Step 4B实现范围
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:204:- 扩展模型后Step 4B应实现什么
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:205:- 不扩展模型Step 4B应实现什么（或跳过）
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:206:- 是否需要Step 4B-lite（仅name更新）
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:212:### Q1：字段契约定义 vs 当前需求
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:214:字段契约定义phone/email/department为API补充字段，但当前系统明确需要这些字段吗？
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:223:**影响：** name覆盖策略和字段主导权
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:231:### Q4：mapper email提取
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:233:字段契约包含email，但mapper未提取。
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:235:**是否需要：** 补充mapper提取email字段？
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:237:### Q5：Step 4B最小范围
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:239:如果扩展模型，Step 4B最小实现是什么？
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:240:- 只更新phone/department？
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:241:- 包含email？
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:255:   - 是否新增phone/email/department
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:259:3. **name覆盖决策**
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:263:4. **Step 4B实施范围**
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:35:- 学工文档样例字段：`name`、`number`、`phone`、`identity_id`、`department`、`user_identity`、`updated_at` 等
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:36:- 当前内部 `User` 模型字段：`user_id`、`name`、`role`、`active`、`class_id`、`is_graduating`、`graduation_year`
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:37:- 当前 CSV 导入命令的业务要求：学生导入要求 `student_id`、`name`、`class_id`、`is_graduating`、`graduation_year`
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:67:   - CSV 导入要求 `is_graduating` 和 `graduation_year`。
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:88:- `is_graduating`、`graduation_year` 从哪里来，缺失时是否禁止入库；
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:95:**最快达到可工作状态的方式不是直接写同步命令，而是先做一个短平快的字段契约。**
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:108:   - 没有 `is_graduating/graduation_year`：不可声明毕业生筛选可用
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:129:| `User.graduation_year` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:13:Codex与Claude完全同意：不单独做Step 3.5，不做Step 4B真实upsert（先解决模型字段gap）。
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:31:### 2. 关键发现：User模型字段gap（P1）
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:34:- mapper输出phone/department/email
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:35:- User模型只到graduation_year
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:36:- 缺失：phone, email, department字段
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:37:- 影响：Step 4B不能实现真实upsert
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:39:**User模型当前字段：**
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:46:- graduation_year
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:49:- phone（mapper输出，字段契约定义为API补充）
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:50:- email（字段契约定义，mapper未提取）
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:51:- department（mapper输出，字段契约定义为API补充）
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:58:- Phase 1：API不创建新用户（缺class_id/is_graduating/graduation_year）
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:71:4. **已存在学生：** 计入existing_count, would_update_count
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:72:5. **核心字段保护：** 不覆盖class_id/is_graduating/graduation_year
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:73:6. **补充字段警告：** phone/department无模型字段 → 输出warnings
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:88:    'would_update_count': int,
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:96:### 6. Step 4B延后（等待决策）
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:101:- 给User增加phone/email/department
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:126:- Step 4B完成后再做
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:153:### Phase 3：Step 4B + Step 5（模型扩展后）
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:161:**mapper改进（如果模型扩展包含email）：**
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:162:- mapper增加email字段提取
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:163:- 增加test_email_field测试
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:176:**暂停点：** Step 4A完成后，讨论模型扩展策略，不自动执行Step 4B。
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:13:Codex识别的P1问题准确且关键：`would_update_count`语义歧义会导致测试锁定错误业务含义，Step 4B也可能误判。同意修复策略：明确定义为"候选数"而非"可写更新数"，强化warning文本。
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:21:### P1：would_update_count语义歧义
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:25:- 问题：User模型无phone/email/department，name覆盖未决
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:32:- 理由1：符合文档97第4条"已存在学生计入would_update_count"
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:43:- 当前：只在would_update_count>0时输出
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:50:- 测试场景6明确为"存在would_update候选时输出warning"
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:88:            'would_update_count': int,  # 现有学生同步候选数，不代表当前模型可持久化写入数
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:99:result['warnings'].append("User model lacks phone/email/department fields - cannot persist API supplemental data")
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:105:    f"{result['would_update_count']} sync candidates exist, but no API supplemental fields can be persisted "
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:106:    "until User model adds phone/email/department or name overwrite policy is approved"
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:129:   - 本地存在且role='student' → existing_count=1, would_update_count=1
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:141:   - 服务执行后DB中class_id/is_graduating/graduation_year不变
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:145:   - would_update_count>0 → warning输出
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:188:场景2：断言existing_count=1且would_update_count=1（候选数语义）
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:18:- 修改1：docstring增加would_update_count语义说明
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:50:1. docstring中would_update_count注释是否准确传达"候选数"语义
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:66:- 验证existing_count=1, would_update_count=1（候选数语义）
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:76:- 验证服务执行后DB中class_id/is_graduating/graduation_year不变
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:109:### Q1：would_update_count修复是否充分
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:115:**建议：** 可以在`would_update_count += 1`附近添加行内注释
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:134:    would_update_count
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:143:- existing = would_update + conflicts
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:191:4. 讨论User模型扩展策略（Step 4B前置）
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:109:2. **业务字段层：** 宽松采样，记录 `name/number/phone/identity_id/department/user_identity/user_auth_extra_field` 是否出现，不因业务字段缺失直接失败。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:134:字段: name=yes number=yes phone=yes department=yes user_identity=yes
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:135:样本: name=张* number=17 phone=186****9896
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:14:但有一个必须先澄清并落地的小问题：`would_update_count`现在按"本地存在且role=student"计数。若该字段表示"真实可写更新数"，当前User模型没有`phone/email/department`，`name`是否允许API覆盖也未决，因此真实可更新字段数应为0。若该字段表示"未来可更新候选数"，则字段名有误导性，测试必须明确锁定这个语义。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:16:我的建议：Step 4A保持9字段结构不扩展，但在实现和测试中明确把`would_update_count`定义为"现有学生同步候选数，不代表当前模型可持久化写入数"，同时warning必须指出当前无补充字段可落库、真实upsert仍被Step 4B阻塞。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:20:### 问题1：`would_update_count`语义容易锁错测试 [P1]
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:24:**问题描述：** 当前实现只要本地用户存在且角色为`student`，就执行`would_update_count += 1`。这符合文档97第4条"已存在学生计入would_update_count"，但与字段覆盖文档的Phase 1事实存在张力：User模型当前没有`phone/email/department`字段，`name`是否允许由API覆盖仍未决。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:26:**影响：** 如果后续测试把`would_update_count`理解为"当前会真实更新DB的记录数"，测试会锁定错误业务语义。Step 4B实现时也可能误以为已有可写字段，可以直接做upsert。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:29:- 在函数docstring或返回注释中明确：`would_update_count`是"existing student candidate count"，不是当前可持久化更新数。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:30:- 保留当前计数也可以，但warning文本应更强：`would_update_count` candidates exist, but no supplemental API fields can be persisted until User model adds phone/email/department or name overwrite policy is approved。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:31:- 如果团队希望`would_update_count`严格表示真实可写更新数，则当前实现应改为0，并把现有学生只计入`existing_count`。不过这会偏离文档97的9字段契约，需先改共识文档。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:37:**问题描述：** 当前只有`would_update_count > 0`时才输出模型字段gap warning。若输入中只有missing_local用户，但mapper已经产出`phone/department`，仍然存在同一个字段gap和Phase 1创建阻塞问题，只是现在只有逐用户`would_create_but_blocked` warning。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:39:**影响：** 空更新候选但有API补充字段的批次，不会给出全局字段gap提示。对dry-run summary阅读者来说，可能不清楚Step 4B为什么仍不可做真实upsert。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:42:- 至少在`mapped_count > 0`且任一mapped结果包含`phone`或`department`时输出字段gap warning。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:43:- 如果保持当前规则，则测试场景6必须明确为"存在would_update候选时输出warning"，不要声称所有字段gap场景都会输出全局warning。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:65:7. 服务没有写DB，不会覆盖`class_id/is_graduating/graduation_year`。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:73:### Q2：would_update计数准确性
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:77:如果`would_update_count`表示"现有学生同步候选"，当前实现正确。如果表示"当前真实可写更新"，当前实现不准确，因为可安全写入字段未成立：`phone/email/department`不存在，`name`覆盖策略未决。建议在Step 4A把它定义为候选数，并用warning明确真实写入仍不可执行。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:91:- 服务执行后本地User的`class_id/is_graduating/graduation_year`保持不变；
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:99:1. "已存在学生进入existing"：断言`existing_count=1`，并按最终语义断言`would_update_count`。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:100:2. "不覆盖class_id/is_graduating/graduation_year"：断言服务只读后DB原值不变，不要模拟Step 4B写入行为。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:101:3. "phone/department无模型字段warning"：断言warning文本明确说明不能持久化补充字段，并且不会影响`existing_count`。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:109:1. 先小改服务注释/warning，解决`would_update_count`语义歧义。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:112:4. 测试通过后再进入Step 4B模型扩展决策，不要直接做真实upsert。
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:11:**一致决策：Step 4A同步计划服务实现完成，批准提交，进入Step 4B模型扩展讨论。**
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:21:**问题：** would_update_count语义歧义（doc 99识别）
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:64:3. ✅ 批准进入Step 4B模型扩展讨论
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:89:## Step 4B前置条件
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:91:**Codex建议：** 优先决策User模型扩展策略
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:95:**问题1：是否新增phone/email/department字段？**
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:96:- 选项A：扩展User模型，增加3个字段
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:105:- 选项A：Step 4B可实现完整API补充字段upsert
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:106:- 选项B：Step 4B受限，would_update实际无可写补充字段
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:112:**立即启动：** Step 4B前置讨论 - User模型扩展策略
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:115:1. 评估phone/email/department字段业务价值
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:131:**立即进入Step 4B前置讨论。**
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:12:**结论：通过。批准提交当前Step 4A实现与测试，可进入Step 4B模型扩展讨论。**
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:14:本轮P1修复已经落地：`would_update_count`被明确约束为"现有学生同步候选数"，不再暗示当前模型已有可持久化更新字段；warning文本也明确指出API补充字段暂不能落库。新增测试使用Django `TestCase`和真实测试数据库，覆盖doc 99要求的8个关键场景。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:24:`would_update_count`注释为"现有学生同步候选数，不代表当前模型可持久化写入数"，准确传达了doc 99要求的候选数语义。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:33:- 候选数量：`{would_update_count} sync candidates exist`
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:35:- 阻塞解除条件：增加`phone/email/department`或批准`name`覆盖策略
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:37:这足以避免把`would_update_count`误解为真实DB更新数。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:64:2. `test_existing_student_to_candidate`：覆盖`existing_count=1`、`would_update_count=1`候选数语义，通过。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:67:5. `test_core_fields_readonly`：覆盖`class_id/is_graduating/graduation_year/name`不变，通过。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:78:### Q1：would_update_count修复是否充分
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:80:充分。docstring和warning已锁定候选数语义。`would_update_count += 1`附近当前注释仍偏简短，但不构成阻塞；若要进一步降低歧义，可后续把该行注释改为"已存在学生，计入同步候选数；当前模型仍不可写入API补充字段"。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:84:完整。当前断言覆盖不创建、计数和`would_create_but_blocked`。服务warning已包含`class_id/is_graduating/graduation_year`，如需更强锁定可增加断言，但现有测试已经足够支撑Step 4A。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:90:`skipped_count + missing_local_count + len(conflicts) + would_update_count == total_fetched`
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:92:这避免了`existing_count`包含conflict和candidate导致的重复计数。更完整的关系也成立：`mapped = missing_local + existing`，`existing = would_update + conflicts`。
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:140:3. **批准进入Step 4B模型扩展讨论。**
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:142:Step 4B前置建议：优先决策User模型是否新增`phone/email/department`，以及`name`是否允许由学工API覆盖；在该决策完成前，不应把Step 4A的`would_update_count`解释为真实可写更新数。
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:18:4. ✅ **最快路径正确**：字段契约 → 只读mapper → 幂等upsert → command 是最低风险路径
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:51:**必要动作：** 在字段契约中明确`class_id`来源，缺失时继续依赖CSV。
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:57:**Codex指出：** CSV导入要求`is_graduating`和`graduation_year`，学工API样例未证明能提供。
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:63:**必要动作：** 在字段契约中明确这两个字段缺失时的处理规则（继续CSV维护 or 禁止同步）。
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:76:**必要动作：** 在字段契约中明确`user_identity`值域映射，未知值跳过并报告。
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:107:### User模型必需字段
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:113:- graduation_year (学生必填)
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:126:| User.graduation_year | 未确认 | 缺失 | 继续由CSV/手工维护，API不覆盖 |
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:166:            'graduation_year': int | None,
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:182:7. graduation_year缺失返回None
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:142:- `phone` - 手机号
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:144:- `department` - 部门（数组）
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:176:✓ 字段采样: name, number, phone存在
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:188:    "fields_present": ["name", "number", "phone"]
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:35:- 学工文档样例字段：`name`、`number`、`phone`、`identity_id`、`department`、`user_identity`、`updated_at` 等
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:36:- 当前内部 `User` 模型字段：`user_id`、`name`、`role`、`active`、`class_id`、`is_graduating`、`graduation_year`
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:37:- 当前 CSV 导入命令的业务要求：学生导入要求 `student_id`、`name`、`class_id`、`is_graduating`、`graduation_year`
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:67:   - CSV 导入要求 `is_graduating` 和 `graduation_year`。
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:88:- `is_graduating`、`graduation_year` 从哪里来，缺失时是否禁止入库；
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:95:**最快达到可工作状态的方式不是直接写同步命令，而是先做一个短平快的字段契约。**
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:108:   - 没有 `is_graduating/graduation_year`：不可声明毕业生筛选可用
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:129:| `User.graduation_year` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:15:1. ✅ **P1准确**：User模型缺失phone/email/department字段，mapper输出无法安全持久化
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:28:**Codex指出：** mapper输出phone/department，但User模型只到graduation_year，缺这些字段。
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:30:**Claude确认：** 完全同意。验证当前User模型：
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:41:    graduation_year = IntegerField(null=True, blank=True)
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:42:    # 缺失: phone, email, department
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:46:- 字段契约定义phone/email/department为"API补充字段"
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:49:- Step 4B不能实现真实upsert
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:57:**Codex指出：** 字段契约说Phase 1不创建新用户，但mapper对合法学生返回class_id=None且skip_reason=None。
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:61:- 但class_id/is_graduating/graduation_year都是None
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:100:            'would_update_count': int,
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:111:4. 本地存在且是student → 计入would_update（但当前无可写补充字段）
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:112:5. phone/department无模型字段 → 输出warning
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:121:5. 不覆盖class_id/is_graduating/graduation_year
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:122:6. phone/department无模型字段warning
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:130:### 延后：Step 4B - 真实写入
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:135:- 给User增加phone/email/department字段
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:145:- 字段契约已定义phone/email/department为API补充字段
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:148:- CSV不提供这些字段，API补充合理
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:181:Codex提到mapper当前不提取email字段。
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:184:- 当前提取：number, name, user_identity, phone, department
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:185:- 未提取：email
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:187:**后续：** 如果模型扩展包含email，需补充：
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:188:1. mapper增加email提取
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:189:2. 增加test_email_field测试
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:199:3. ✅ 不做Step 4B真实upsert（先解决模型字段gap）
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:201:5. ✅ 识别User模型缺phone/email/department
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:213:**决策：User模型扩展策略**
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:214:- 选项1：增加phone/email/department字段（推荐）
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:219:- 字段契约定义
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:236:2. 不执行：Step 4B（等待模型扩展决策）
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:237:3. 不执行：Step 5（等待Step 4B完成）
docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:42:3. **毕业范围风险**：`is_graduating`/`graduation_year`缺失导致范围模糊
docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:52:- 内部User模型必需字段清单
docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:67:| User.graduation_year | 未确认 | 缺失 | CSV维护，API不覆盖 |
docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:18:- 修改1：docstring增加would_update_count语义说明
docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:50:1. docstring中would_update_count注释是否准确传达"候选数"语义
docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:66:- 验证existing_count=1, would_update_count=1（候选数语义）
docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:76:- 验证服务执行后DB中class_id/is_graduating/graduation_year不变
docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:109:### Q1：would_update_count修复是否充分
docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:115:**建议：** 可以在`would_update_count += 1`附近添加行内注释
docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:134:    would_update_count
docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:143:- existing = would_update + conflicts
docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:191:4. 讨论User模型扩展策略（Step 4B前置）
./backend/apps/approvals/tests/test_rejection_flow.py:23:            graduation_year=2024
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:170:- CSV字段契约与数据对接文档一致。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:14:但有一个必须先澄清并落地的小问题：`would_update_count`现在按"本地存在且role=student"计数。若该字段表示"真实可写更新数"，当前User模型没有`phone/email/department`，`name`是否允许API覆盖也未决，因此真实可更新字段数应为0。若该字段表示"未来可更新候选数"，则字段名有误导性，测试必须明确锁定这个语义。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:16:我的建议：Step 4A保持9字段结构不扩展，但在实现和测试中明确把`would_update_count`定义为"现有学生同步候选数，不代表当前模型可持久化写入数"，同时warning必须指出当前无补充字段可落库、真实upsert仍被Step 4B阻塞。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:20:### 问题1：`would_update_count`语义容易锁错测试 [P1]
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:24:**问题描述：** 当前实现只要本地用户存在且角色为`student`，就执行`would_update_count += 1`。这符合文档97第4条"已存在学生计入would_update_count"，但与字段覆盖文档的Phase 1事实存在张力：User模型当前没有`phone/email/department`字段，`name`是否允许由API覆盖仍未决。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:26:**影响：** 如果后续测试把`would_update_count`理解为"当前会真实更新DB的记录数"，测试会锁定错误业务语义。Step 4B实现时也可能误以为已有可写字段，可以直接做upsert。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:29:- 在函数docstring或返回注释中明确：`would_update_count`是"existing student candidate count"，不是当前可持久化更新数。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:30:- 保留当前计数也可以，但warning文本应更强：`would_update_count` candidates exist, but no supplemental API fields can be persisted until User model adds phone/email/department or name overwrite policy is approved。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:31:- 如果团队希望`would_update_count`严格表示真实可写更新数，则当前实现应改为0，并把现有学生只计入`existing_count`。不过这会偏离文档97的9字段契约，需先改共识文档。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:37:**问题描述：** 当前只有`would_update_count > 0`时才输出模型字段gap warning。若输入中只有missing_local用户，但mapper已经产出`phone/department`，仍然存在同一个字段gap和Phase 1创建阻塞问题，只是现在只有逐用户`would_create_but_blocked` warning。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:39:**影响：** 空更新候选但有API补充字段的批次，不会给出全局字段gap提示。对dry-run summary阅读者来说，可能不清楚Step 4B为什么仍不可做真实upsert。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:42:- 至少在`mapped_count > 0`且任一mapped结果包含`phone`或`department`时输出字段gap warning。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:43:- 如果保持当前规则，则测试场景6必须明确为"存在would_update候选时输出warning"，不要声称所有字段gap场景都会输出全局warning。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:65:7. 服务没有写DB，不会覆盖`class_id/is_graduating/graduation_year`。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:73:### Q2：would_update计数准确性
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:77:如果`would_update_count`表示"现有学生同步候选"，当前实现正确。如果表示"当前真实可写更新"，当前实现不准确，因为可安全写入字段未成立：`phone/email/department`不存在，`name`覆盖策略未决。建议在Step 4A把它定义为候选数，并用warning明确真实写入仍不可执行。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:91:- 服务执行后本地User的`class_id/is_graduating/graduation_year`保持不变；
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:99:1. "已存在学生进入existing"：断言`existing_count=1`，并按最终语义断言`would_update_count`。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:100:2. "不覆盖class_id/is_graduating/graduation_year"：断言服务只读后DB原值不变，不要模拟Step 4B写入行为。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:101:3. "phone/department无模型字段warning"：断言warning文本明确说明不能持久化补充字段，并且不会影响`existing_count`。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:109:1. 先小改服务注释/warning，解决`would_update_count`语义歧义。
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:112:4. 测试通过后再进入Step 4B模型扩展决策，不要直接做真实upsert。
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:117:- CSV字段契约与数据对接文档一致
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:13:Codex识别的P1问题准确且关键：`would_update_count`语义歧义会导致测试锁定错误业务含义，Step 4B也可能误判。同意修复策略：明确定义为"候选数"而非"可写更新数"，强化warning文本。
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:21:### P1：would_update_count语义歧义
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:25:- 问题：User模型无phone/email/department，name覆盖未决
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:32:- 理由1：符合文档97第4条"已存在学生计入would_update_count"
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:43:- 当前：只在would_update_count>0时输出
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:50:- 测试场景6明确为"存在would_update候选时输出warning"
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:88:            'would_update_count': int,  # 现有学生同步候选数，不代表当前模型可持久化写入数
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:99:result['warnings'].append("User model lacks phone/email/department fields - cannot persist API supplemental data")
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:105:    f"{result['would_update_count']} sync candidates exist, but no API supplemental fields can be persisted "
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:106:    "until User model adds phone/email/department or name overwrite policy is approved"
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:129:   - 本地存在且role='student' → existing_count=1, would_update_count=1
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:141:   - 服务执行后DB中class_id/is_graduating/graduation_year不变
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:145:   - would_update_count>0 → warning输出
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:188:场景2：断言existing_count=1且would_update_count=1（候选数语义）
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:140:5. 字段采样：仅检查人员记录是否包含 `name/number/phone/identity_id/department/user_identity/updated_at` 等文档字段。
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:45:- 其他过滤参数（name, number, phone等）可选
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:34:4. 本地存在且是student → 计入would_update
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:35:5. phone/department无模型字段 → 输出warning
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:55:    'would_update_count': int,
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:75:5. 不覆盖class_id/is_graduating/graduation_year
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:76:6. phone/department无模型字段warning
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:90:- API不创建新用户（缺class_id/is_graduating/graduation_year）
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:102:- mapper输出phone/department
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:103:- User模型无这些字段
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:107:- warning是否在would_update_count>0时输出
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:109:- 是否影响existing_count/would_update_count判定
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:124:### Q2：would_update计数准确性
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:126:当本地用户存在且role='student'时，计入would_update。
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:130:- mapper输出的字段有哪些可以写入User模型？
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:131:- 如果没有可写字段，would_update是否误导性？
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:133:根据文档95/97，当前User模型可安全写入的API字段：
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:135:- phone/department（模型无字段，不能写）
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:137:**这是否意味着would_update实际为0？**
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:162:文档97要求测试"不覆盖class_id/is_graduating/graduation_year"。
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:166:- 这个测试是否应该在Step 4B实现？
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:200:- 字段契约：docs/phase4c-xg-field-coverage.md
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:19:2. **Step 4B：在服务层实现受限真实写入**
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:28:当前 `map_xg_user_to_internal()` 输出 `phone` 和 `department`，字段覆盖契约也把 `phone`、`email`、`department`定义为 API 补充字段。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:38:- `graduation_year`
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:40:没有 `phone`、`email`、`department` 持久化字段。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:42:这意味着如果 Step 4 现在直接做“幂等 upsert 并写库”，实际可安全写入的 API 字段非常有限。`class_id`、`is_graduating`、`graduation_year`按共识不由 API 覆盖；`role`仅用于过滤学生；`user_id`是主键；剩下只有 `name` 可能可更新，但它属于 CSV 主导核心字段，不应在没有明确策略时被 API 静默覆盖。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:46:### P1：字段契约与 mapper 对“新用户是否可创建”的边界需要由 Step 4 承担
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:48:字段契约明确 Phase 1 中学工 API 不创建新学生，因为缺少 `class_id`、`is_graduating`、`graduation_year`。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:54:- `graduation_year=None`
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:90:3. 写入字段范围清晰：**目前不满足**，因为模型缺少 `phone`/`department`/`email`。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:119:- `would_update_count`
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:129:- 当前没有模型字段承接 `phone`/`department`：输出 warning，不能声明可写入。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:137:- 不覆盖 `class_id`、`is_graduating`、`graduation_year`
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:138:- 无 phone/department 模型字段时输出明确 warning
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:140:### Step 4B：受限真实写入（需 Step 4A 后再决定）
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:144:1. **模型扩展路线**：给 `User` 增加 `phone`、`email`、`department` 等 API 补充字段，再实现幂等更新。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:177:   - 当前模型与字段契约不一致，不能假装 `phone`/`department` 可 upsert。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:197:1. mapper 返回 `phone`/`department` 是合理的，但 Step 4 不能把它们视为可持久化字段，除非模型扩展。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:198:2. 字段契约中提到 `email`，但 mapper 当前不提取 `email`；如果未来模型扩展包含邮箱，需要补 mapper 和测试。
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:210:3. 暂不做 Step 4B 真实 upsert，先由 Step 4A 暴露“当前无可写补充字段”的事实。
docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:15:- 修改1：docstring增加would_update_count语义注释
docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:54:**would_update_count语义歧义 - 已解决 ✓**
docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:57:- 测试验证existing_count=1, would_update_count=1（候选数语义）
docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:72:- class_id/is_graduating/graduation_year不变
docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:84:**P1：would_update_count语义 - 完全执行 ✓**
docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:90:- ✅ 保持当前规则（would_update_count>0触发）
docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:157:- 是否可以进入Step 4B模型扩展讨论
docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:175:   - 是否可以进入下一阶段（Step 4B模型扩展讨论）
docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:179:   - User模型扩展的优先建议
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:34:4. 本地存在且是student → 计入would_update
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:35:5. phone/department无模型字段 → 输出warning
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:55:    'would_update_count': int,
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:75:5. 不覆盖class_id/is_graduating/graduation_year
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:76:6. phone/department无模型字段warning
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:90:- API不创建新用户（缺class_id/is_graduating/graduation_year）
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:102:- mapper输出phone/department
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:103:- User模型无这些字段
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:107:- warning是否在would_update_count>0时输出
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:109:- 是否影响existing_count/would_update_count判定
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:124:### Q2：would_update计数准确性
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:126:当本地用户存在且role='student'时，计入would_update。
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:130:- mapper输出的字段有哪些可以写入User模型？
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:131:- 如果没有可写字段，would_update是否误导性？
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:133:根据文档95/97，当前User模型可安全写入的API字段：
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:135:- phone/department（模型无字段，不能写）
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:137:**这是否意味着would_update实际为0？**
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:162:文档97要求测试"不覆盖class_id/is_graduating/graduation_year"。
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:166:- 这个测试是否应该在Step 4B实现？
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:200:- 字段契约：docs/phase4c-xg-field-coverage.md
./docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:142:- `phone` - 手机号
./docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:144:- `department` - 部门（数组）
./docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:176:✓ 字段采样: name, number, phone存在
./docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:188:    "fields_present": ["name", "number", "phone"]
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:15:- 修改1：docstring增加would_update_count语义注释
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:54:**would_update_count语义歧义 - 已解决 ✓**
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:57:- 测试验证existing_count=1, would_update_count=1（候选数语义）
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:72:- class_id/is_graduating/graduation_year不变
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:84:**P1：would_update_count语义 - 完全执行 ✓**
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:90:- ✅ 保持当前规则（would_update_count>0触发）
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:157:- 是否可以进入Step 4B模型扩展讨论
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:175:   - 是否可以进入下一阶段（Step 4B模型扩展讨论）
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:179:   - User模型扩展的优先建议
./docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:42:3. **毕业范围风险**：`is_graduating`/`graduation_year`缺失导致范围模糊
./docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:52:- 内部User模型必需字段清单
./docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:67:| User.graduation_year | 未确认 | 缺失 | CSV维护，API不覆盖 |
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:15:1. ✅ **P1准确**：User模型缺失phone/email/department字段，mapper输出无法安全持久化
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:28:**Codex指出：** mapper输出phone/department，但User模型只到graduation_year，缺这些字段。
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:30:**Claude确认：** 完全同意。验证当前User模型：
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:41:    graduation_year = IntegerField(null=True, blank=True)
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:42:    # 缺失: phone, email, department
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:46:- 字段契约定义phone/email/department为"API补充字段"
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:49:- Step 4B不能实现真实upsert
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:57:**Codex指出：** 字段契约说Phase 1不创建新用户，但mapper对合法学生返回class_id=None且skip_reason=None。
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:61:- 但class_id/is_graduating/graduation_year都是None
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:100:            'would_update_count': int,
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:111:4. 本地存在且是student → 计入would_update（但当前无可写补充字段）
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:112:5. phone/department无模型字段 → 输出warning
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:121:5. 不覆盖class_id/is_graduating/graduation_year
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:122:6. phone/department无模型字段warning
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:130:### 延后：Step 4B - 真实写入
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:135:- 给User增加phone/email/department字段
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:145:- 字段契约已定义phone/email/department为API补充字段
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:148:- CSV不提供这些字段，API补充合理
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:181:Codex提到mapper当前不提取email字段。
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:184:- 当前提取：number, name, user_identity, phone, department
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:185:- 未提取：email
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:187:**后续：** 如果模型扩展包含email，需补充：
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:188:1. mapper增加email提取
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:189:2. 增加test_email_field测试
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:199:3. ✅ 不做Step 4B真实upsert（先解决模型字段gap）
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:201:5. ✅ 识别User模型缺phone/email/department
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:213:**决策：User模型扩展策略**
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:214:- 选项1：增加phone/email/department字段（推荐）
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:219:- 字段契约定义
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:236:2. 不执行：Step 4B（等待模型扩展决策）
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:237:3. 不执行：Step 5（等待Step 4B完成）
./backend/apps/users/integrations/xg_user_mapper.py:16:            'phone': str | None,
./backend/apps/users/integrations/xg_user_mapper.py:17:            'department': str | None,
./backend/apps/users/integrations/xg_user_mapper.py:20:            'graduation_year': None,  # API不提供
./backend/apps/users/integrations/xg_user_mapper.py:28:        'phone': None,
./backend/apps/users/integrations/xg_user_mapper.py:29:        'department': None,
./backend/apps/users/integrations/xg_user_mapper.py:32:        'graduation_year': None,
./backend/apps/users/integrations/xg_user_mapper.py:40:    phone = xg_user.get('phone')
./backend/apps/users/integrations/xg_user_mapper.py:41:    department = xg_user.get('department')
./backend/apps/users/integrations/xg_user_mapper.py:76:    result['phone'] = phone
./backend/apps/users/integrations/xg_user_mapper.py:77:    result['department'] = department
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:11:**一致决策：Step 4A同步计划服务实现完成，批准提交，进入Step 4B模型扩展讨论。**
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:21:**问题：** would_update_count语义歧义（doc 99识别）
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:64:3. ✅ 批准进入Step 4B模型扩展讨论
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:89:## Step 4B前置条件
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:91:**Codex建议：** 优先决策User模型扩展策略
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:95:**问题1：是否新增phone/email/department字段？**
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:96:- 选项A：扩展User模型，增加3个字段
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:105:- 选项A：Step 4B可实现完整API补充字段upsert
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:106:- 选项B：Step 4B受限，would_update实际无可写补充字段
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:112:**立即启动：** Step 4B前置讨论 - User模型扩展策略
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:115:1. 评估phone/email/department字段业务价值
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:131:**立即进入Step 4B前置讨论。**
./backend/apps/users/services/xg_user_sync.py:24:            'would_update_count': int,  # 现有学生同步候选数，不代表当前模型可持久化写入数
./backend/apps/users/services/xg_user_sync.py:36:        'would_update_count': 0,
./backend/apps/users/services/xg_user_sync.py:71:            # 已存在学生，计入would_update
./backend/apps/users/services/xg_user_sync.py:72:            result['would_update_count'] += 1
./backend/apps/users/services/xg_user_sync.py:77:            result['warnings'].append(f"would_create_but_blocked: {user_id} (lacks class_id/is_graduating/graduation_year)")
./backend/apps/users/services/xg_user_sync.py:80:    if result['would_update_count'] > 0:
./backend/apps/users/services/xg_user_sync.py:82:            f"{result['would_update_count']} sync candidates exist, but no API supplemental fields can be persisted "
./backend/apps/users/services/xg_user_sync.py:83:            "until User model adds phone/email/department or name overwrite policy is approved"
./backend/apps/users/models.py:34:    graduation_year = models.IntegerField(null=True, blank=True)
./backend/apps/users/tests/test_xg_user_mapper.py:14:            'phone': '13800138000',
./backend/apps/users/tests/test_xg_user_mapper.py:15:            'department': '计算机学院',
./backend/apps/users/tests/test_xg_user_mapper.py:24:        self.assertEqual(result['phone'], '13800138000')
./backend/apps/users/tests/test_xg_user_mapper.py:25:        self.assertEqual(result['department'], '计算机学院')
./backend/apps/users/tests/test_xg_user_mapper.py:28:        self.assertIsNone(result['graduation_year'])
./backend/apps/users/tests/test_xg_user_mapper.py:60:            'phone': '13800138001',
./backend/apps/users/tests/test_xg_user_mapper.py:112:        self.assertIsNone(result['phone'])
./backend/apps/users/tests/test_xg_user_mapper.py:113:        self.assertIsNone(result['department'])
./backend/apps/users/management/commands/import_csv.py:51:        required_fields = ['student_id', 'name', 'class_id', 'is_graduating', 'graduation_year']
./backend/apps/users/management/commands/import_csv.py:100:                                'graduation_year': int(row['graduation_year'].strip()),
./backend/apps/users/management/commands/seed_data.py:49:                    'graduation_year': 2024,
./backend/apps/applications/tests/test_error_cases.py:23:            graduation_year=2024
./backend/apps/applications/tests/test_error_cases.py:33:            graduation_year=2024
./backend/apps/applications/tests/test_error_cases.py:43:            graduation_year=2024
./backend/apps/users/serializers.py:9:        fields = ['user_id', 'name', 'role', 'class_id', 'active', 'is_graduating', 'graduation_year']
./backend/apps/applications/tests/test_constraints.py:20:            graduation_year=2024,
./backend/apps/users/migrations/0001_initial.py:29:                ('graduation_year', models.IntegerField(blank=True, null=True)),
./backend/apps/applications/tests/test_application_flow.py:24:            graduation_year=2024
./backend/apps/users/tests/test_xg_user_sync.py:22:            graduation_year=2025
./backend/apps/users/tests/test_xg_user_sync.py:58:                'phone': '13800138000',
./backend/apps/users/tests/test_xg_user_sync.py:59:                'department': '计算机学院'
./backend/apps/users/tests/test_xg_user_sync.py:69:        self.assertEqual(result['would_update_count'], 1)  # 候选数，非真实可写数
./backend/apps/users/tests/test_xg_user_sync.py:80:                'phone': '13900139000'
./backend/apps/users/tests/test_xg_user_sync.py:89:        self.assertEqual(result['would_update_count'], 0)
./backend/apps/users/tests/test_xg_user_sync.py:113:        self.assertEqual(result['would_update_count'], 0)  # 冲突不计入候选
./backend/apps/users/tests/test_xg_user_sync.py:129:        original_graduation_year = original_user.graduation_year
./backend/apps/users/tests/test_xg_user_sync.py:145:        self.assertEqual(user_after.graduation_year, original_graduation_year)
./backend/apps/users/tests/test_xg_user_sync.py:155:                'phone': '13800138000',
./backend/apps/users/tests/test_xg_user_sync.py:156:                'department': '计算机学院'
./backend/apps/users/tests/test_xg_user_sync.py:162:        self.assertEqual(result['would_update_count'], 1)
./backend/apps/users/tests/test_xg_user_sync.py:169:        self.assertIn('phone/email/department', warning_text)
./backend/apps/users/tests/test_xg_user_sync.py:180:        self.assertEqual(result['would_update_count'], 0)
./backend/apps/users/tests/test_xg_user_sync.py:210:        self.assertEqual(result['would_update_count'], 1)  # 只有2021001是学生候选
./backend/apps/users/tests/test_xg_user_sync.py:221:            result['would_update_count']
./backend/apps/attachments/tests/test_list.py:24:            graduation_year=2024
./backend/apps/attachments/tests/test_list.py:34:            graduation_year=2024
./backend/apps/attachments/tests/test_delete.py:23:            graduation_year=2024
./backend/apps/attachments/tests/test_delete.py:33:            graduation_year=2024
./backend/apps/attachments/tests/test_upload.py:23:            graduation_year=2024
./backend/apps/attachments/tests/test_upload.py:34:            graduation_year=2024
./backend/apps/attachments/tests/test_download.py:24:            graduation_year=2024
./backend/apps/attachments/tests/test_download.py:34:            graduation_year=2024
./backend/apps/users/tests/test_import_csv.py:26:        csv_content = "employee_id,name,department\nT003,张老师,计算机学院\nT004,赵老师,软件学院"
./backend/apps/users/tests/test_import_csv.py:102:        csv_content = "student_id,name,class_id,is_graduating,graduation_year\n2020001,张三,CS2020-01,true,2024"
./backend/apps/users/tests/test_import_csv.py:119:        csv_content = "student_id,name,class_id,is_graduating,graduation_year\n2020001,张三,CS2020-99,true,2024"

codex
I found the key existing contract: Phase 1 is already recorded as “CSV主导 + API补充”, with API limited to `phone/email/department` and no API creation of users. I’m checking the implementation surface now to make sure the Step 4B scope is feasible, not just desirable on paper.
exec
/bin/bash -lc "rtk sed -n '180,230p' docs/phase4c-xg-field-coverage.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
### 6.1 核心原则

**在字段未完全覆盖前，API只能补充或更新可确定字段，不能替代CSV导入。**

### 6.2 并存规则

| 数据来源 | 负责字段 | 说明 |
|---------|---------|------|
| **CSV导入（主）** | `user_id`, `name`, `role`, `class_id`, `is_graduating`, `graduation_year` | 学生创建和核心业务字段由CSV维护 |
| **学工API（补充）** | `phone`, `email`, `department`, `updated_at` | API仅补充或更新非核心字段 |

### 6.3 同步模式

**Phase 1（当前）：CSV主导 + API补充**
- CSV导入创建所有学生用户（包含`class_id`/`is_graduating`/`graduation_year`）
- 学工API同步仅更新已存在用户的`phone`/`email`/`department`
- 学工API **不创建新用户**（因为缺少`class_id`等必填字段）

**Phase 2（未来）：API主导 + CSV补充**
- 前提：live测试确认学工API能提供`class_id`/`is_graduating`/`graduation_year`
- 学工API可以创建新用户
- CSV仅补充学工API缺失的字段

### 6.4 停用策略

**初期策略：不自动停用**
- 学工API本次未返回某用户 ≠ 该用户应停用
- 原因：API可能因为权限、筛选条件、分页等原因遗漏部分用户
- 仅输出差异报告：`{api_user_ids} - {local_user_ids}` 和 `{local_user_ids} - {api_user_ids}`

**未来策略：**
- 等live数据稳定后，可考虑：
  - 连续N次同步都缺失 → 标记为待审查
  - 手工审查后 → 停用账号（`active=False`）

---

## 七、Step 3 mapper测试样例

### 7.1 输入样例

```python
# 样例1：完整字段
{
    "number": "2022001",
    "name": "张三",
    "phone": "13800138000",
    "department": "计算机学院",
    "user_identity": "1"  # 假设1代表学生
}


exec
/bin/bash -lc "rtk sed -n '1,140p' backend/apps/users/services/xg_user_sync.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
"""学工系统用户同步服务"""
from typing import Dict, List
from django.contrib.auth import get_user_model
from apps.users.integrations.xg_user_mapper import map_xg_user_to_internal

User = get_user_model()


def plan_xg_user_sync(xg_users: List[dict]) -> Dict:
    """
    生成学工用户同步计划（不写DB）

    Args:
        xg_users: 学工API返回的用户列表

    Returns:
        {
            'total_fetched': int,
            'mapped_count': int,
            'skipped_count': int,
            'skipped_by_reason': dict,
            'existing_count': int,
            'missing_local_count': int,
            'would_update_count': int,  # 现有学生同步候选数，不代表当前模型可持久化写入数
            'conflicts': list,
            'warnings': list
        }
    """
    result = {
        'total_fetched': len(xg_users),
        'mapped_count': 0,
        'skipped_count': 0,
        'skipped_by_reason': {},
        'existing_count': 0,
        'missing_local_count': 0,
        'would_update_count': 0,
        'conflicts': [],
        'warnings': []
    }

    for xg_user in xg_users:
        mapped = map_xg_user_to_internal(xg_user)

        # mapper skip
        if mapped['skip_reason']:
            result['skipped_count'] += 1
            reason = mapped['skip_reason']
            result['skipped_by_reason'][reason] = result['skipped_by_reason'].get(reason, 0) + 1
            continue

        result['mapped_count'] += 1
        user_id = mapped['user_id']

        # 检查本地是否存在
        # user_id是主键，不会出现MultipleObjectsReturned
        # 如果发生，说明数据库完整性已破坏，应让异常暴露
        try:
            local_user = User.objects.get(user_id=user_id)
            result['existing_count'] += 1

            # 角色冲突检查
            if local_user.role != 'student':
                result['conflicts'].append({
                    'user_id': user_id,
                    'reason': 'role_mismatch',
                    'local_role': local_user.role,
                    'api_role': mapped['role']
                })
                continue

            # 已存在学生，计入would_update
            result['would_update_count'] += 1

        except User.DoesNotExist:
            # 本地不存在，Phase 1不创建
            result['missing_local_count'] += 1
            result['warnings'].append(f"would_create_but_blocked: {user_id} (lacks class_id/is_graduating/graduation_year)")

    # 模型字段gap警告
    if result['would_update_count'] > 0:
        result['warnings'].append(
            f"{result['would_update_count']} sync candidates exist, but no API supplemental fields can be persisted "
            "until User model adds phone/email/department or name overwrite policy is approved"
        )

    return result

exec
/bin/bash -lc "rtk sed -n '1,140p' backend/apps/users/integrations/xg_user_mapper.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
"""学工系统用户数据映射器"""


def map_xg_user_to_internal(xg_user: dict) -> dict:
    """
    将学工API用户映射为内部User字段

    Args:
        xg_user: 学工API返回的用户字典

    Returns:
        dict: {
            'user_id': str | None,
            'name': str | None,
            'role': str | None,
            'phone': str | None,
            'department': str | None,
            'class_id': None,  # API不提供
            'is_graduating': None,  # API不提供
            'graduation_year': None,  # API不提供
            'skip_reason': str | None  # 如果应跳过，说明原因
        }
    """
    result = {
        'user_id': None,
        'name': None,
        'role': None,
        'phone': None,
        'department': None,
        'class_id': None,
        'is_graduating': None,
        'graduation_year': None,
        'skip_reason': None
    }

    # 提取字段
    number = xg_user.get('number')
    name = xg_user.get('name')
    user_identity = xg_user.get('user_identity')
    phone = xg_user.get('phone')
    department = xg_user.get('department')

    # 必填字段检查
    if not number:
        result['skip_reason'] = 'missing_user_id'
        return result

    if not name:
        result['user_id'] = number
        result['skip_reason'] = 'missing_name'
        return result

    # 角色映射（只接受明确的学生值）
    role = None
    if user_identity is not None:
        user_identity_str = str(user_identity)
        if user_identity_str == '1':
            role = 'student'
        elif user_identity_str.lower() == 'student':
            role = 'student'
        else:
            result['user_id'] = number
            result['name'] = name
            result['skip_reason'] = f'unknown_user_identity: {user_identity_str}'
            return result
    else:
        result['user_id'] = number
        result['name'] = name
        result['skip_reason'] = 'missing_user_identity'
        return result

    # 映射成功
    result['user_id'] = number
    result['name'] = name
    result['role'] = role
    result['phone'] = phone
    result['department'] = department

    return result

exec
/bin/bash -lc "rtk sed -n '1,130p' backend/apps/users/models.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserRole(models.TextChoices):
    STUDENT = 'student', '学生'
    COUNSELOR = 'counselor', '辅导员'
    DEAN = 'dean', '学工部'


class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        if not user_id:
            raise ValueError('user_id is required')
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('active', True)
        return self.create_user(user_id, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=UserRole.choices)
    active = models.BooleanField(default=True)
    class_id = models.CharField(max_length=50, null=True, blank=True)
    is_graduating = models.BooleanField(null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name', 'role']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.user_id} - {self.name}"

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/users/tests/test_xg_user_sync.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
"""学工用户同步计划服务测试"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.users.services.xg_user_sync import plan_xg_user_sync

User = get_user_model()


class XGUserSyncPlanTests(TestCase):
    """测试学工用户同步计划生成（不写DB）"""

    def setUp(self):
        """测试前准备：创建测试用户"""
        # 已存在的学生
        User.objects.create(
            user_id='2021001',
            name='张三',
            role='student',
            active=True,
            class_id='CS2021-1',
            is_graduating=True,
            graduation_year=2025
        )

        # 已存在的教师（角色冲突测试）
        User.objects.create(
            user_id='T001',
            name='李老师',
            role='counselor',
            active=True
        )

    def test_mapper_skip_transparency(self):
        """测试1：mapper skip透传统计"""
        xg_users = [
            {'number': None, 'name': '王五', 'user_identity': '1'},  # 缺number
            {'number': '2021003', 'name': None, 'user_identity': '1'},  # 缺name
            {'number': '2021004', 'name': '赵六', 'user_identity': '9'},  # 未知身份
        ]

        result = plan_xg_user_sync(xg_users)

        self.assertEqual(result['total_fetched'], 3)
        self.assertEqual(result['mapped_count'], 0)
        self.assertEqual(result['skipped_count'], 3)
        self.assertGreater(len(result['skipped_by_reason']), 0)
        # 验证统计了不同的skip_reason
        self.assertIn('missing_user_id', result['skipped_by_reason'])
        self.assertIn('missing_name', result['skipped_by_reason'])

    def test_existing_student_to_candidate(self):
        """测试2：已存在学生进入候选（验证候选数语义）"""
        xg_users = [
            {
                'number': '2021001',
                'name': '张三新名字',
                'user_identity': '1',
                'phone': '13800138000',
                'department': '计算机学院'
            }
        ]

        result = plan_xg_user_sync(xg_users)

        self.assertEqual(result['total_fetched'], 1)
        self.assertEqual(result['mapped_count'], 1)
        self.assertEqual(result['skipped_count'], 0)
        self.assertEqual(result['existing_count'], 1)
        self.assertEqual(result['would_update_count'], 1)  # 候选数，非真实可写数
        self.assertEqual(result['missing_local_count'], 0)
        self.assertEqual(len(result['conflicts']), 0)

    def test_missing_local_not_created(self):
        """测试3：本地不存在用户不创建（Phase 1边界）"""
        xg_users = [
            {
                'number': '2021999',
                'name': '新学生',
                'user_identity': '1',
                'phone': '13900139000'
            }
        ]

        result = plan_xg_user_sync(xg_users)

        self.assertEqual(result['mapped_count'], 1)
        self.assertEqual(result['existing_count'], 0)
        self.assertEqual(result['missing_local_count'], 1)
        self.assertEqual(result['would_update_count'], 0)

        # 验证确实没有创建
        self.assertFalse(User.objects.filter(user_id='2021999').exists())

        # 验证有warning提示不创建
        self.assertGreater(len(result['warnings']), 0)
        warning_text = ' '.join(result['warnings'])
        self.assertIn('would_create_but_blocked', warning_text)

    def test_local_role_conflict(self):
        """测试4：本地角色冲突检测"""
        xg_users = [
            {
                'number': 'T001',
                'name': '李老师',
                'user_identity': '1',  # API认为是学生
            }
        ]

        result = plan_xg_user_sync(xg_users)

        self.assertEqual(result['mapped_count'], 1)
        self.assertEqual(result['existing_count'], 1)
        self.assertEqual(result['would_update_count'], 0)  # 冲突不计入候选
        self.assertEqual(len(result['conflicts']), 1)

        # 验证conflict结构完整性
        conflict = result['conflicts'][0]
        self.assertEqual(conflict['user_id'], 'T001')
        self.assertEqual(conflict['reason'], 'role_mismatch')
        self.assertEqual(conflict['local_role'], 'counselor')
        self.assertEqual(conflict['api_role'], 'student')

    def test_core_fields_readonly(self):
        """测试5：服务只读，不修改核心字段"""
        # 记录原始值
        original_user = User.objects.get(user_id='2021001')
        original_class_id = original_user.class_id
        original_is_graduating = original_user.is_graduating
        original_graduation_year = original_user.graduation_year

        xg_users = [
            {
                'number': '2021001',
                'name': '张三',
                'user_identity': '1',
            }
        ]

        result = plan_xg_user_sync(xg_users)

        # 验证服务执行后DB不变
        user_after = User.objects.get(user_id='2021001')
        self.assertEqual(user_after.class_id, original_class_id)
        self.assertEqual(user_after.is_graduating, original_is_graduating)
        self.assertEqual(user_after.graduation_year, original_graduation_year)
        self.assertEqual(user_after.name, original_user.name)  # name也不变

    def test_field_gap_warning_with_candidates(self):
        """测试6：存在候选时输出字段gap warning"""
        xg_users = [
            {
                'number': '2021001',
                'name': '张三',
                'user_identity': '1',
                'phone': '13800138000',
                'department': '计算机学院'
            }
        ]

        result = plan_xg_user_sync(xg_users)

        self.assertEqual(result['would_update_count'], 1)
        self.assertGreater(len(result['warnings']), 0)

        # 验证强化后的warning文本
        warning_text = ' '.join(result['warnings'])
        self.assertIn('sync candidates exist', warning_text)
        self.assertIn('no API supplemental fields can be persisted', warning_text)
        self.assertIn('phone/email/department', warning_text)

    def test_empty_input(self):
        """测试7：空输入处理"""
        result = plan_xg_user_sync([])

        self.assertEqual(result['total_fetched'], 0)
        self.assertEqual(result['mapped_count'], 0)
        self.assertEqual(result['skipped_count'], 0)
        self.assertEqual(result['existing_count'], 0)
        self.assertEqual(result['missing_local_count'], 0)
        self.assertEqual(result['would_update_count'], 0)
        self.assertEqual(len(result['conflicts']), 0)
        self.assertEqual(len(result['warnings']), 0)

    def test_mixed_scenario(self):
        """测试8：混合场景（skip/missing/conflict/existing各1个）"""
        xg_users = [
            # skip - 缺number
            {'number': None, 'name': '测试1', 'user_identity': '1'},

            # skip - 未知身份（不同reason）
            {'number': '2021005', 'name': '测试2', 'user_identity': '9'},

            # missing_local
            {'number': '2021998', 'name': '测试3', 'user_identity': '1'},

            # conflict
            {'number': 'T001', 'name': '李老师', 'user_identity': '1'},

            # existing student
            {'number': '2021001', 'name': '张三', 'user_identity': '1'},
        ]

        result = plan_xg_user_sync(xg_users)

        self.assertEqual(result['total_fetched'], 5)
        self.assertEqual(result['mapped_count'], 3)  # skip的2个不计入
        self.assertEqual(result['skipped_count'], 2)
        self.assertEqual(result['existing_count'], 2)  # T001和2021001都存在
        self.assertEqual(result['missing_local_count'], 1)
        self.assertEqual(result['would_update_count'], 1)  # 只有2021001是学生候选
        self.assertEqual(len(result['conflicts']), 1)

        # 验证多个skip_reason统计
        self.assertEqual(len(result['skipped_by_reason']), 2)

        # 验证计数互不串类
        total_categorized = (
            result['skipped_count'] +
            result['missing_local_count'] +
            len(result['conflicts']) +
            result['would_update_count']
        )
        self.assertEqual(total_categorized, result['total_fetched'])

codex
The code confirms the blocker described in the request: mapper emits `phone` and `department`, the planner only counts update candidates, and `User` has no persistent supplemental fields. I’m going to write the Codex response as the next numbered discussion artifact, with a conservative implementation recommendation.
exec
/bin/bash -lc 'rtk find .omc/collaboration -maxdepth 2 -type f -o -type d | sort' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
rtk: rtk find does not support compound predicates or actions (e.g. -not, -exec). Use `find` directly.

exec
/bin/bash -lc "rtk sed -n '1,180p' docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Phase 4C Step 4A最终共识 - 实现完成

**日期：** 2026-06-02  
**参与方：** Codex + Claude  
**文档编号：** 104

---

## 共识结论

**一致决策：Step 4A同步计划服务实现完成，批准提交，进入Step 4B模型扩展讨论。**

Codex与Claude完全同意：P1修复已落地，测试覆盖完整，8/8通过验收。

---

## 核心共识点

### 1. P1修复执行完成

**问题：** would_update_count语义歧义（doc 99识别）

**修复完成：**
- ✅ docstring注释："候选数，不代表当前模型可持久化写入数"
- ✅ warning强化："{N} sync candidates exist, but no API supplemental fields can be persisted"
- ✅ user_id主键注释：不捕获MultipleObjectsReturned

**Codex评估：** 通过。语义已明确锁定，不再误导。

### 2. 测试覆盖验收通过

**测试结果：** 8/8 passed (0.032s)

**场景覆盖（全部通过）：**
1. ✅ mapper skip透传统计（修正断言匹配实际skip_reason）
2. ✅ existing student候选数语义验证
3. ✅ missing_local不创建用户（Phase 1边界）
4. ✅ role conflict结构完整性
5. ✅ 服务只读不修改DB核心字段
6. ✅ 字段gap warning强化文本
7. ✅ 空输入处理
8. ✅ 混合场景分类互斥性

**Codex评估：** 测试策略正确（Django TestCase + 真实DB），覆盖完整。

### 3. 发现处理

**发现：** mapper skip_reason实际值为字段级别
- 'missing_user_id'
- 'missing_name'
- 'unknown_user_identity: {value}'

**处理：** 测试断言调整匹配实际输出，合理且必要。

**Codex确认：** 修正正确。

---

## 批准决策

**Codex批准（doc 103）：**
1. ✅ 批准提交当前服务修改和测试
2. ✅ 批准创建最终共识文档
3. ✅ 批准进入Step 4B模型扩展讨论

**Claude同意。**

---

## 产出物

**代码文件：**
- backend/apps/users/services/xg_user_sync.py（修改）
- backend/apps/users/tests/test_xg_user_sync.py（新建）

**讨论文档：**
- doc 98：实施审查请求
- doc 99：Codex审查响应（P1识别）
- doc 100：Claude同意修复
- doc 101：实施与测试请求
- doc 102：完成总结
- doc 103：Codex最终审查通过

**提交记录：**
- feat: Phase 4C Step 4A完成 - 同步计划服务+测试

---

## Step 4B前置条件

**Codex建议：** 优先决策User模型扩展策略

**待决策问题：**

**问题1：是否新增phone/email/department字段？**
- 选项A：扩展User模型，增加3个字段
- 选项B：不扩展，只更新name字段

**问题2：name字段是否允许API覆盖？**
- 当前：CSV主导核心字段（包括name）
- 学工API也返回name
- 需定义冲突优先级

**影响：**
- 选项A：Step 4B可实现完整API补充字段upsert
- 选项B：Step 4B受限，would_update实际无可写补充字段

---

## 下一步执行

**立即启动：** Step 4B前置讨论 - User模型扩展策略

**讨论范围：**
1. 评估phone/email/department字段业务价值
2. 分析migration影响和风险
3. 定义CSV与API数据源冲突优先级
4. 决策选项A或B

**预计时间：** 讨论20-30分钟 + 实现（如选项A）40-60分钟

---

## 执行授权

✅ Codex与Claude已达成完整共识  
✅ Step 4A验收通过  
✅ 无遗留问题  
✅ 用户授权自主执行  

**立即进入Step 4B前置讨论。**

exec
/bin/bash -lc "rtk sed -n '1,180p' backend/apps/users/serializers.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name', 'role', 'class_id', 'active', 'is_graduating', 'graduation_year']
        read_only_fields = ['user_id']


class AuthUserSerializer(serializers.ModelSerializer):
    """登录响应中的用户摘要（UserDTO子集）"""
    class Meta:
        model = User
        fields = ['user_id', 'name', 'role', 'class_id']


class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        password = attrs.get('password')

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials')

        if not user.active:
            raise serializers.ValidationError('Account is inactive')

        refresh = RefreshToken.for_user(user)

        return {
            'access_token': str(refresh.access_token),
            'token_type': 'Bearer',
            'user': AuthUserSerializer(user).data
        }


class LoginResponseSerializer(serializers.Serializer):
    """登录成功响应（schema-only，用于OpenAPI文档）"""
    access_token = serializers.CharField(help_text="JWT access token")
    token_type = serializers.CharField(default='Bearer', help_text="Token type")
    user = AuthUserSerializer(help_text="用户信息")

exec
/bin/bash -lc "rtk sed -n '1,220p' docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Phase 4C Step 4A实现完成 - Codex最终审查响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**针对文档：** `docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md`、`docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md`  
**审查范围：** `backend/apps/users/services/xg_user_sync.py`、`backend/apps/users/tests/test_xg_user_sync.py`

---

## 审查结论

**结论：通过。批准提交当前Step 4A实现与测试，可进入Step 4B模型扩展讨论。**

本轮P1修复已经落地：`would_update_count`被明确约束为"现有学生同步候选数"，不再暗示当前模型已有可持久化更新字段；warning文本也明确指出API补充字段暂不能落库。新增测试使用Django `TestCase`和真实测试数据库，覆盖doc 99要求的8个关键场景。

---

## 服务修改审查

### 1. docstring语义

**位置：** `backend/apps/users/services/xg_user_sync.py:24`

`would_update_count`注释为"现有学生同步候选数，不代表当前模型可持久化写入数"，准确传达了doc 99要求的候选数语义。

**结论：通过。**

### 2. warning文本

**位置：** `backend/apps/users/services/xg_user_sync.py:80-84`

warning包含：
- 候选数量：`{would_update_count} sync candidates exist`
- 持久化阻塞：`no API supplemental fields can be persisted`
- 阻塞解除条件：增加`phone/email/department`或批准`name`覆盖策略

这足以避免把`would_update_count`误解为真实DB更新数。

**结论：通过。**

### 3. user_id主键说明

**位置：** `backend/apps/users/services/xg_user_sync.py:55-56`

注释说明`user_id`是主键，不捕获`MultipleObjectsReturned`是正确策略。`backend/apps/users/models.py:28`确认`user_id = models.CharField(..., unique=True, primary_key=True)`。

**结论：通过。**

---

## 测试覆盖审查

**测试文件：** `backend/apps/users/tests/test_xg_user_sync.py`

8个场景均已实现，并且测试策略符合要求：
- 使用Django `TestCase`
- 使用真实测试数据库
- `setUp`创建1个学生和1个辅导员，足够覆盖existing、conflict、readonly主路径
- 未mock `User.objects.get`

逐项结论：

1. `test_mapper_skip_transparency`：覆盖skip透传和`skipped_by_reason`统计，通过。修正为断言实际mapper输出`missing_user_id`、`missing_name`是合理的。
2. `test_existing_student_to_candidate`：覆盖`existing_count=1`、`would_update_count=1`候选数语义，通过。
3. `test_missing_local_not_created`：覆盖`missing_local_count`、不创建用户、`would_create_but_blocked` warning，通过。
4. `test_local_role_conflict`：覆盖`user_id/reason/local_role/api_role`结构，通过。
5. `test_core_fields_readonly`：覆盖`class_id/is_graduating/graduation_year/name`不变，通过。
6. `test_field_gap_warning_with_candidates`：覆盖强化warning关键文本，通过。
7. `test_empty_input`：覆盖空输入全零计数和空列表，通过。
8. `test_mixed_scenario`：覆盖skip、missing、conflict、existing分类关系和多个skip reason，通过。

**结论：测试覆盖完整，满足Step 4A验收。**

---

## Q1-Q5回答

### Q1：would_update_count修复是否充分

充分。docstring和warning已锁定候选数语义。`would_update_count += 1`附近当前注释仍偏简短，但不构成阻塞；若要进一步降低歧义，可后续把该行注释改为"已存在学生，计入同步候选数；当前模型仍不可写入API补充字段"。

### Q2：test_missing_local_not_created是否完整

完整。当前断言覆盖不创建、计数和`would_create_but_blocked`。服务warning已包含`class_id/is_graduating/graduation_year`，如需更强锁定可增加断言，但现有测试已经足够支撑Step 4A。

### Q3：test_mixed_scenario计数公式是否正确

正确。该公式不是用`existing_count`相加，而是使用最终互斥分类：

`skipped_count + missing_local_count + len(conflicts) + would_update_count == total_fetched`

这避免了`existing_count`包含conflict和candidate导致的重复计数。更完整的关系也成立：`mapped = missing_local + existing`，`existing = would_update + conflicts`。

### Q4：setUp测试数据是否足够

足够。Step 4A服务只读，不依据毕业年份做分支判断，因此不需要额外创建不同毕业年份学生。毕业年份边界应留给未来存在按年份筛选或写入策略时再测。

### Q5：Docker环境是否需要预检查

需要轻量预检查。建议先运行：

```bash
docker compose ps
```

本次环境中backend和db均已运行，db为healthy。原始命令格式正确，但非交互环境遇到已存在测试库时会触发Django删除确认并失败；建议使用：

```bash
docker compose exec backend python manage.py test apps.users.tests.test_xg_user_sync -v 2 --keepdb
```

---

## 测试执行结果

已执行：

```bash
docker compose exec backend python manage.py test apps.users.tests.test_xg_user_sync -v 2 --keepdb
```

结果：**8 tests passed**。

补充执行：

```bash
docker compose exec backend python manage.py test apps.users.tests.test_xg_user_mapper apps.users.tests.test_xg_user_sync -v 2 --keepdb
```

结果：**16 tests passed**。

说明：不带`--keepdb`时，本地已有`test_graduation_leave`测试库导致Django尝试交互确认删除，并在非交互执行中以`EOFError`退出。这是环境/命令参数问题，不是代码或测试失败。

---

## 批准决策

1. **批准提交当前服务修改和新增测试。**
2. **批准创建最终共识文档。**
3. **批准进入Step 4B模型扩展讨论。**

Step 4B前置建议：优先决策User模型是否新增`phone/email/department`，以及`name`是否允许由学工API覆盖；在该决策完成前，不应把Step 4A的`would_update_count`解释为真实可写更新数。


exec
/bin/bash -lc "rtk sed -n '2200,2390p' docs/PROJECT-SUMMARY.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
- ✓ 38/38 tests passed (0.072s)
- 原29测试 + 9新测试 = 38测试全部通过

**产出物：**
- docs/discussions/phase4c-next-steps/87-step2b-implementation-review-request.md
- docs/discussions/phase4c-next-steps/88-step2b-implementation-codex-response.md
- docs/discussions/phase4c-next-steps/89-claude-response-agree-fixes.md
- .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-87-*.md

**状态：**
- ✅ Step 2B完成（分页+测试+诊断优化）
- ✅ XG API客户端schema校验+无界保护完整
- ⏭ 下一步：讨论Step 2C字段覆盖 vs Step 3同步命令优先级

**Phase 4C：学工API数据对接 - Step 2C-lite完成（2026-06-02）：**

**Claude-Codex协作流程：**
- ✓ 下一步优先级讨论（doc 90-93）
- ✓ Codex推荐A-prime：Step 2C-lite字段映射契约优先
- ✓ Claude完全同意：不跳过Step 2C，不直接实现写库同步命令
- ✓ 识别5个直接写库风险（主键/权限链/毕业范围/角色/回滚成本）

**实施完成：**

*Step 2C-lite：字段映射契约文档：*
- ✓ docs/phase4c-xg-field-coverage.md
- 9个章节：API字段/内部模型/字段映射表/处理规则/并存策略/测试样例/验收标准
- 字段映射表：4类状态（可映射/角色高风险/无法映射/可选）
- 处理规则：跳过规则+部分映射规则+错误报告格式
- API/CSV并存策略：Phase 1（CSV主导+API补充）
- 测试样例：3个输入+3个预期输出

**核心决策：**
- ✅ API初期只补充phone/email/department，不创建新用户
- ✅ class_id/is_graduating/graduation_year继续由CSV维护
- ✅ user_identity值域未知，只接受明确学生值
- ✅ 不自动停用本地缺失用户，仅输出差异报告

**产出物：**
- docs/phase4c-xg-field-coverage.md（v0.1草案）
- docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md
- docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
- docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md
- docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md

**状态：**
- ✅ Step 2C-lite完成（30分钟）
- ⏭ 下一步：Step 3只读mapper/provider测试（40-50分钟）
- ⏭ 后续：Step 4幂等upsert + Step 5 management command


**Phase 4C：学工API数据对接 - Step 3完成（2026-06-02）：**

**实施内容：**

*只读mapper函数：*
- ✓ backend/apps/users/integrations/xg_user_mapper.py
- map_xg_user_to_internal(xg_user: dict) -> dict
- 纯转换逻辑，不写数据库，不依赖Provider接口
- 返回格式包含skip_reason字段

*单元测试（8个）：*
- ✓ backend/apps/users/tests/test_xg_user_mapper.py
- test_complete_fields_success（完整字段映射）
- test_user_identity_student_string（'student'字符串）
- test_missing_number_skip（number缺失）
- test_missing_name_skip（name缺失）
- test_unknown_user_identity_skip（未知user_identity）
- test_missing_user_identity_skip（缺失user_identity）
- test_optional_fields_missing（可选字段缺失不阻止）
- test_multiple_missing_fields_priority（多缺失优先级）

**测试结果：**
- ✓ 8/8 tests passed (0.011s)

**状态：**
- ✅ Step 3完成
- ⏭ 可选：Step 3.5 dry-run演示命令
- ⏭ 待定：Step 4幂等upsert + Step 5 management command

**Phase 4C：Claude-Codex讨论 - Step 3后续优先级共识（2026-06-02）：**

**讨论流程（doc 94-97）：**
- ✓ Claude提出优先级讨论请求
- ✓ Codex审查并推荐B-prime策略
- ✓ Claude完全同意Codex分析
- ✓ 达成共识：Step 4A同步计划服务优先

**Codex关键发现（2个P1）：**
1. User模型缺失phone/email/department字段
   - mapper输出这些字段
   - 字段契约定义为API补充字段
   - 但模型只到graduation_year
   - Step 4B真实upsert阻塞

2. 新用户创建边界需显式执行
   - Phase 1：API不创建缺核心字段的用户
   - mapper成功但本地不存在 → 不创建

**共识决策：B-prime**
- ✓ Step 4A：同步计划服务（内置dry-run summary，不写DB）
- ⏸ Step 4B：真实upsert（等待模型扩展决策）
- ⏸ Step 5：命令入口（等待Step 4B）
- ❌ 不单独做Step 3.5命令

**下一步：**
- 待执行：Step 4A实现（40-50分钟）
- 待讨论：User模型扩展策略（增加phone/email/department）

**产出物：**
- docs/discussions/phase4c-next-steps/94-post-step3-next-priority-request.md
- docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md
- docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md
- docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md

**状态：**
- ✅ 讨论完成，共识达成
- ⏸ 暂停执行（按用户要求）
- ⏭ 下次继续：Step 4A实现


**Phase 4C：学工API数据对接 - Step 4A启动（2026-06-02）：**

**实施内容：**

*服务文件创建：*
- ✓ backend/apps/users/services/xg_user_sync.py
- plan_xg_user_sync(xg_users: List[dict]) -> Dict
- 只读分析，不写数据库
- 实现6条判定规则（mapper skip/本地不存在/角色冲突/已存在学生/核心字段保护/补充字段警告）

*返回结构（9个字段）：*
- total_fetched, mapped_count, skipped_count, skipped_by_reason
- existing_count, missing_local_count, would_update_count
- conflicts, warnings

*讨论文档：*
- ✓ docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md
- 审查要点：5个核心逻辑验证
- 关键质疑：5个Q（异常处理/would_update准确性/conflicts结构/skipped统计/测试场景5必要性）

**状态：**
- ✓ 服务文件已创建
- ⏳ 等待Codex审查（doc 98）
- ⏭ 根据审查结果：创建测试 或 修正逻辑
- ⏭ 后续：8个测试场景 + 验证运行

**产出物：**
- backend/apps/users/services/xg_user_sync.py
- docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md



**Phase 4C：学工API数据对接 - Step 4A完成（2026-06-02）：**

**实施内容：**

*服务文件修改（3处P1修复）：*
- ✓ backend/apps/users/services/xg_user_sync.py
- docstring明确would_update_count为候选数语义
- warning文本强化（包含候选数量和持久化阻塞说明）
- 添加user_id主键特性注释

*测试文件创建：*
- ✓ backend/apps/users/tests/test_xg_user_sync.py
- 8个测试场景（Django TestCase + 真实数据库）
- 修正skip_reason断言匹配mapper实际值

**测试结果：**
- ✓ 8/8 tests passed (0.032s)
- 场景覆盖：skip透传/existing候选/missing不创建/role冲突/只读保证/字段gap warning/空输入/混合场景

**讨论记录（doc 98-102）：**
- 98：实施审查请求
- 99：Codex审查响应（P1语义歧义识别）
- 100：Claude同意修复方案
- 101：实施与测试请求
- 102：完成总结

**状态：**
- ✅ Step 4A完成
- ⏭ 下一步：User模型扩展决策（增加phone/email/department字段）
- ⏸ Step 4B：真实upsert（等待模型扩展）

**产出物：**
- backend/apps/users/services/xg_user_sync.py（修改）
- backend/apps/users/tests/test_xg_user_sync.py（新建）
- docs/discussions/phase4c-next-steps/98-102.md


exec
/bin/bash -lc 'rtk proxy find .omc/collaboration -maxdepth 2 -print | sort' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
.omc/collaboration
.omc/collaboration/.omc
.omc/collaboration/.omc/state
.omc/collaboration/artifacts
.omc/collaboration/artifacts/20260530-0805-codex-protocol-critical-review.md
.omc/collaboration/artifacts/20260530-0808-claude-response-to-codex-review.md
.omc/collaboration/artifacts/20260530-0814-protocol-review-consensus.md
.omc/collaboration/artifacts/20260530-0848-claude-github-projects-analysis.md
.omc/collaboration/artifacts/20260530-0902-claude-codex-consensus-discussion.md
.omc/collaboration/artifacts/20260530-0937-claude-synthesis-next-steps.md
.omc/collaboration/artifacts/20260530-0955-claude-phase3-initial-analysis.md
.omc/collaboration/artifacts/20260530-0959-codex-phase3-independent-review.md
.omc/collaboration/artifacts/20260530-1005-claude-response-to-codex-phase3-review.md
.omc/collaboration/artifacts/20260530-1008-codex-phase3-consensus.md
.omc/collaboration/artifacts/20260530-1015-day0-completion.md
.omc/collaboration/artifacts/20260530-1025-phase4-operator-checklist.md
.omc/collaboration/artifacts/20260530-1611-codex-second-response-to-claude.md
.omc/collaboration/artifacts/20260530-1625-claude-phase1b-response.md
.omc/collaboration/artifacts/20260530-1654-codex-github-projects-analysis.md
.omc/collaboration/artifacts/20260530-1655-claude-step2-phase1-response.md
.omc/collaboration/artifacts/20260530-1703-codex-consensus-confirmation.md
.omc/collaboration/artifacts/20260530-1711-gemini-test-gemini-workflow-.md
.omc/collaboration/artifacts/20260530-1718-claude-blocking-issues-response.md
.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md
.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md
.omc/collaboration/artifacts/20260530-1733-codex-next-steps-analysis.md
.omc/collaboration/artifacts/20260530-1747-codex-phase2-invariant-test-results.md
.omc/collaboration/artifacts/20260530-1747-codex-phase2-invariant-tests.py
.omc/collaboration/artifacts/20260530-1942-codex-completion-boundary-analysis.md
.omc/collaboration/artifacts/20260530-2048-claude-response-codex-prep-analysis.md
.omc/collaboration/artifacts/20260530-2053-codex-response-to-claude-week4-prep.md
.omc/collaboration/artifacts/20260530-2225-codex-day0-verification.md
.omc/collaboration/artifacts/20260530-2251-codex-four-project-pattern-analysis.md
.omc/collaboration/artifacts/20260530-2301-codex-gemini-and-modular-agent-analysis.md
.omc/collaboration/artifacts/20260530-2347-codex-agent-lifecycle-consensus.md
.omc/collaboration/artifacts/20260531-0202-claude-codex-week3-response.md
.omc/collaboration/artifacts/20260531-0210-week3-execution-consensus.md
.omc/collaboration/artifacts/20260531-0215-phase0-fact-check-results.md
.omc/collaboration/artifacts/20260531-0220-phase1-complete.md
.omc/collaboration/artifacts/20260531-0225-phase3-complete.md
.omc/collaboration/artifacts/20260531-0310-claude-response-readiness-repair.md
.omc/collaboration/artifacts/20260531-0320-codex-readiness-repair-confirmation.md
.omc/collaboration/artifacts/20260531-0325-step1-verification-results.md
.omc/collaboration/artifacts/20260531-0405-codex-week3-consensus-response.md
.omc/collaboration/artifacts/20260531-0415-codex-week3-execution-summary.md
.omc/collaboration/artifacts/20260531-0421-codex-next-phase-strategy.md
.omc/collaboration/artifacts/20260531-0425-codex-response-to-claude-next-phase-strategy.md
.omc/collaboration/artifacts/20260531-0430-week3-final-summary.md
.omc/collaboration/artifacts/20260531-0435-claude-response-next-phase-strategy.md
.omc/collaboration/artifacts/20260531-0439-codex-week4-blocked-prep-analysis.md
.omc/collaboration/artifacts/20260531-0440-week4-execution-plan-consensus.md
.omc/collaboration/artifacts/20260531-0445-dorm-provider-discovery.md
.omc/collaboration/artifacts/20260601-0135-claude-response-phase4a-blocker-challenge.md
.omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md
.omc/collaboration/artifacts/20260601-1817-codex-events-jsonl-repair.md
.omc/collaboration/artifacts/blocked-waiting-for-devtools.md
.omc/collaboration/artifacts/dorm-system-stakeholder-request.md
.omc/collaboration/artifacts/events-jsonl-before-line95-repair-20260601T181700Z.bak
.omc/collaboration/artifacts/events-jsonl-before-line95-repair-20260601T181800Z.bak
.omc/collaboration/artifacts/phase4a-devtools-setup.md
.omc/collaboration/artifacts/phase4a-validation-checklist.md
.omc/collaboration/artifacts/phase4b-prep-note.md
.omc/collaboration/artifacts/phase4b-skeleton-gaps.md
.omc/collaboration/artifacts/test-coverage-analysis.md
.omc/collaboration/artifacts/test-coverage-claude-response.md
.omc/collaboration/artifacts/test-coverage-final-consensus.md
.omc/collaboration/backup-20260530-084231
.omc/collaboration/backup-20260530-084231/events.jsonl
.omc/collaboration/backup-20260530-084231/state.json
.omc/collaboration/codex-ready.md
.omc/collaboration/events.jsonl
.omc/collaboration/locks
.omc/collaboration/phase1b-implementation-consensus.md
.omc/collaboration/protocol.md
.omc/collaboration/scripts
.omc/collaboration/scripts/invoke-gemini-analysis.sh
.omc/collaboration/scripts/validate-journal.sh
.omc/collaboration/state.json
.omc/collaboration/task-1-consensus.md
.omc/collaboration/task-2-consensus.md
.omc/collaboration/task-3-consensus.md
.omc/collaboration/task-4-consensus.md
.omc/collaboration/tasks
.omc/collaboration/tasks/TASK-20260530-01-protocol-critical-review.md
.omc/collaboration/tasks/TASK-20260530-02-implement-p0-amendments.md
.omc/collaboration/tasks/TASK-20260530-03-分析4个github项目并评估可借鉴内容（含gemini集成.md
.omc/collaboration/tasks/TASK-20260530-04-实施p0优先级项：角色路由+独立分析协议+journal校验.md
.omc/collaboration/tasks/TASK-20260530-05-next-steps-critical-discussion.md
.omc/collaboration/tasks/TASK-20260530-06-readiness-gate-canary-pilot.md

exec
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
 M .omc/collaboration/events.jsonl
 M .omc/collaboration/state.json
 M .omc/session-context.json
 M .omc/state/hud-stdin-cache.json
 M backend/apps/applications/providers.py
 M backend/apps/applications/tests/test_application_flow.py
 M backend/apps/applications/tests/test_constraints.py
 M backend/apps/applications/tests/test_error_cases.py
 M backend/apps/approvals/tests/test_permissions.py
 M backend/apps/approvals/tests/test_rejection_flow.py
 M backend/apps/approvals/tests/test_state_machine.py
 M backend/apps/notifications/services.py
 M backend/apps/users/integrations/xg_user_client.py
 M backend/apps/users/tests/test_xg_user_client.py
 M backend/scripts/diagnose_xg_api.py
 M docs/PROJECT-SUMMARY.md
 M docs/api/notification-contract-v0.1.md
 M frontend/services/api.ts
 M frontend/services/mock.ts
 M frontend/types/api.ts
 M tests/test_p0_fixes.sh
?? .claude/scheduled_tasks.json
?? .claude/scheduled_tasks.lock
?? .omc/artifacts/api-samples-v0.2.sh
?? .omc/artifacts/api-samples/
?? .omc/artifacts/ask/claude-response-phase2-approach-2026-05-31.md
?? .omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md
?? .omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md
?? .omc/artifacts/ask/codex-claude-docs-discussions-codex-review-2026-05-27-35-claude-re-2026-06-01T01-59-52-222Z.md
?? .omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md
?? .omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-34-implementation-o-2026-06-01T01-50-38-091Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-01-claude-phase4c-strate-2026-06-01T07-04-35-149Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-03-claude-response-to-co-2026-06-01T07-08-03-331Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-05-claude-next-steps-str-2026-06-01T07-43-59-071Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-08-claude-phase2-impleme-2026-06-01T08-18-49-202Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-101-implementation-revie-2026-06-02T07-11-16-872Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-101-implementation-revie-2026-06-02T07-14-19-550Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-102-implementation-compl-2026-06-02T07-14-57-846Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-11-claude-p1-fixes-revie-2026-06-01T09-07-37-351Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-14-claude-p1-implementat-2026-06-01T09-18-42-163Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-17-claude-p0-fix-verific-2026-06-01T09-57-25-216Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-17-18-356Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-22-claude-post-execution-2026-06-01T14-27-35-376Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-34-claude-authorization--2026-06-01T15-56-02-973Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-48-37-499Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-47-claude-post-step2-nex-2026-06-01T17-43-18-137Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-47-claude-post-step2-nex-2026-06-01T17-57-59-267Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-47-claude-post-step2-nex-2026-06-01T18-03-30-703Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-50-claude-post-option-e--2026-06-01T18-13-55-411Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-52-claude-response-optio-2026-06-01T18-20-09-573Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-55-claude-post-api-schem-2026-06-01T18-53-35-201Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-58-claude-codex-consensu-2026-06-01T19-03-31-790Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-44-17-027Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-80-step1a-completion-nex-2026-06-02T03-26-34-821Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-80-step1a-completion-nex-2026-06-02T03-27-49-873Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-84-post-step1-next-strat-2026-06-02T03-46-46-328Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-87-step2b-implementation-2026-06-02T03-59-39-871Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-90-next-priority-discuss-2026-06-02T06-16-33-857Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-90-next-priority-discuss-2026-06-02T06-16-51-131Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-94-post-step3-next-prior-2026-06-02T06-40-37-130Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-98-step4a-implementation-2026-06-02T06-52-41-433Z.md
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
?? .omc/collaboration/artifacts/20260601-1817-codex-events-jsonl-repair.md
?? .omc/collaboration/task-2-consensus.md
?? .omc/collaboration/task-3-consensus.md
?? .omc/collaboration/task-4-consensus.md
?? .omc/project-memory.json
?? .omc/sessions/
?? .omc/state/agent-replay-1975d66f-d9f9-404a-aee5-c702658630c2.jsonl
?? .omc/state/checkpoints/
?? .omc/state/last-tool-error.json
?? .omc/state/mission-state.json
?? .omc/state/sessions/1975d66f-d9f9-404a-aee5-c702658630c2/
?? .omc/state/sessions/4aad264e-c3a4-460a-9be1-61247202bad3/
?? .omc/state/sessions/7afec07d-3b40-4e4c-8f86-86e9dc0e791c/
?? .omc/state/sessions/97c93024-a4c1-4e03-93bf-7522ce3517ff/
?? .omc/state/sessions/c8f47bca-464c-4b8c-bab5-42ba59354101/
?? .omc/state/sessions/dcf39a3e-1b72-449a-9897-852c3c7f1253/
?? .omc/state/sessions/e2566739-aaa7-4701-9354-a710639ac308/
?? .omc/state/sessions/f91e1567-b1b2-4cc2-bd9b-355702bc1ec4/
?? .omc/state/subagent-tracking.json
?? backend/.omc/
?? backend/app
?? backend/apps/approvals/validators.py
?? backend/apps/notifications/management/commands/send_approval_timeout_warnings.py
?? backend/apps/notifications/tests/test_timeout_warnings.py
?? backend/docs/
?? "docs/api\350\257\264\346\230\216.txt"
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
?? docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md
?? docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md
?? docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md
?? docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md
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
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260528210617_553_47.jpg"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260528210618_554_47.jpg"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260528210619_555_47.jpg"
?? findings.md
?? miniprogram/.omc/
?? progress.md
?? task_plan.md
?? "\346\257\225\344\270\232\347\246\273\346\240\241\347\263\273\347\273\237\347\224\250\346\210\267\346\226\207\346\241\243.zip"
codex
One important nuance: adding the fields does not automatically mean exposing them in all API serializers or changing CSV import behavior. I’m keeping the Step 4B recommendation scoped to storage plus XG sync first, with API/CSV surface changes as separate follow-up decisions.
exec
/bin/bash -lc "rtk sed -n '1,90p' docs/phase4c-xg-field-coverage.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 学工系统用户API字段覆盖报告

**版本：** v0.1  
**日期：** 2026-06-02  
**状态：** 草案（基于文档样例，待live测试确认）

---

## 一、文档目的

本文档定义学工系统用户API字段与本系统内部`User`模型字段的映射关系，明确：

1. 哪些字段可以从学工API获取
2. 哪些字段必须由CSV/手工维护
3. 字段缺失时的处理规则
4. API与CSV的并存策略

**重要说明：** 本文档基于学工API文档样例和现有客户端实现推断，最终字段覆盖需通过live测试确认。

---

## 二、学工API字段清单（推断）

基于学工系统对接文档和客户端代码推断，学工用户API可能提供以下字段：

### 2.1 已知字段（基于文档样例）

| 字段名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `name` | string | 用户姓名 | 文档样例 |
| `number` | string | 学号/工号 | 文档样例 |
| `phone` | string | 手机号 | 文档样例 |
| `identity_id` | string | 身份证号 | 文档样例 |
| `department` | string | 院系/部门 | 文档样例 |
| `user_identity` | string/int | 用户身份类型 | 文档样例 |
| `updated_at` | string | 更新时间 | 文档样例 |

### 2.2 未知字段（需live测试确认）

以下字段在文档样例中未明确，需live测试确认是否提供：

- `class_id`：班级ID（业务关键字段）
- `class_name`：班级名称
- `major`：专业
- `grade`：年级
- `is_graduating`：是否毕业生
- `graduation_year`：毕业年份
- `email`：邮箱

---

## 三、内部User模型字段清单

### 3.1 核心字段（必填）

| 字段名 | 类型 | 业务约束 | 说明 |
|--------|------|---------|------|
| `user_id` | string | 主键，全局唯一 | 学生使用学号，其他用户使用工号 |
| `name` | string | 必填 | 用户姓名 |
| `role` | string | 必填，枚举值 | student/counselor/advisor/dean/admin |

### 3.2 学生特定字段（学生必填）

| 字段名 | 类型 | 业务约束 | 说明 |
|--------|------|---------|------|
| `class_id` | string | 学生必填 | 班级ID，用于辅导员映射（ClassMapping） |
| `is_graduating` | boolean | 学生必填 | 是否当届毕业生，决定离校申请资格 |
| `graduation_year` | integer | 学生必填 | 毕业年份 |

### 3.3 可选字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `phone` | string | 手机号（用于找回密码、通知） |
| `email` | string | 邮箱（用于通知） |
| `department` | string | 院系/部门（用于展示） |
| `active` | boolean | 账号状态（默认true） |

### 3.4 关联约束

**ClassMapping约束：**
- 学生的`class_id`必须能匹配`ClassMapping`表中的记录
- `ClassMapping.class_id` → `ClassMapping.counselor_id` → `User.user_id`（辅导员）
- 如果`class_id`缺失或无法匹配，学生申请将无法自动分配辅导员审批人

---

## 四、字段映射表

### 4.1 可映射字段

exec
/bin/bash -lc "rtk sed -n '1,180p' backend/apps/users/management/commands/import_csv.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.users.models import User, UserRole
from apps.users.class_mapping import ClassMapping


class Command(BaseCommand):
    help = 'Import users and class mappings from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('--students', type=str, help='Path to students CSV file')
        parser.add_argument('--counselors', type=str, help='Path to counselors CSV file')
        parser.add_argument('--mappings', type=str, help='Path to class mappings CSV file')
        parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be applied'))

        summary = {
            'students': {'created': 0, 'updated': 0, 'failed': 0, 'errors': []},
            'counselors': {'created': 0, 'updated': 0, 'failed': 0, 'errors': []},
            'mappings': {'created': 0, 'updated': 0, 'failed': 0, 'errors': []},
        }

        if options['students']:
            self.import_students(options['students'], dry_run, summary['students'])

        if options['counselors']:
            self.import_counselors(options['counselors'], dry_run, summary['counselors'])

        if options['mappings']:
            self.import_mappings(options['mappings'], dry_run, summary['mappings'])

        self.print_summary(summary, dry_run)

    def validate_required_fields(self, row, required_fields, row_num):
        """Validate required fields are present and non-empty"""
        errors = []
        for field in required_fields:
            if field not in row or not row[field].strip():
                errors.append(f"Row {row_num}: Missing required field '{field}'")
        return errors

    @transaction.atomic
    def import_students(self, filepath, dry_run, summary):
        """Import students from CSV with validation"""
        required_fields = ['student_id', 'name', 'class_id', 'is_graduating', 'graduation_year']

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                # Validate CSV has required columns
                if not all(field in reader.fieldnames for field in required_fields):
                    missing = [f for f in required_fields if f not in reader.fieldnames]
                    raise CommandError(f"CSV missing required columns: {', '.join(missing)}")

                seen_ids = set()
                for row_num, row in enumerate(reader, start=2):
                    # Validate required fields
                    errors = self.validate_required_fields(row, required_fields, row_num)
                    if errors:
                        summary['errors'].extend(errors)
                        summary['failed'] += 1
                        continue

                    # Check duplicate in CSV
                    student_id = row['student_id'].strip()
                    if student_id in seen_ids:
                        summary['errors'].append(f"Row {row_num}: Duplicate student_id '{student_id}'")
                        summary['failed'] += 1
                        continue
                    seen_ids.add(student_id)

                    # Validate class_id has mapping
                    class_id = row['class_id'].strip()
                    if not dry_run and not ClassMapping.objects.filter(class_id=class_id).exists():
                        summary['errors'].append(f"Row {row_num}: class_id '{class_id}' has no counselor mapping")
                        summary['failed'] += 1
                        continue

                    if dry_run:
                        exists = User.objects.filter(user_id=student_id).exists()
                        if exists:
                            summary['updated'] += 1
                        else:
                            summary['created'] += 1
                    else:
                        user, created = User.objects.update_or_create(
                            user_id=student_id,
                            defaults={
                                'name': row['name'].strip(),
                                'role': UserRole.STUDENT,
                                'class_id': class_id,
                                'is_graduating': row['is_graduating'].strip().lower() == 'true',
                                'graduation_year': int(row['graduation_year'].strip()),
                            }
                        )
                        if created:
                            user.set_password(row.get('password', student_id))
                            user.save()
                            summary['created'] += 1
                        else:
                            summary['updated'] += 1

                        self.stdout.write(f'{"Created" if created else "Updated"} student: {user.user_id}')

        except FileNotFoundError:
            raise CommandError(f"File not found: {filepath}")
        except Exception as e:
            raise CommandError(f"Error importing students: {str(e)}")

    @transaction.atomic
    def import_counselors(self, filepath, dry_run, summary):
        """Import counselors from CSV with validation"""
        required_fields = ['employee_id', 'name']

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                # Validate CSV has required columns
                if not all(field in reader.fieldnames for field in required_fields):
                    missing = [f for f in required_fields if f not in reader.fieldnames]
                    raise CommandError(f"CSV missing required columns: {', '.join(missing)}")

                seen_ids = set()
                for row_num, row in enumerate(reader, start=2):
                    # Validate required fields
                    errors = self.validate_required_fields(row, required_fields, row_num)
                    if errors:
                        summary['errors'].extend(errors)
                        summary['failed'] += 1
                        continue

                    # Check duplicate in CSV
                    employee_id = row['employee_id'].strip()
                    if employee_id in seen_ids:
                        summary['errors'].append(f"Row {row_num}: Duplicate employee_id '{employee_id}'")
                        summary['failed'] += 1
                        continue
                    seen_ids.add(employee_id)

                    if dry_run:
                        exists = User.objects.filter(user_id=employee_id).exists()
                        if exists:
                            summary['updated'] += 1
                        else:
                            summary['created'] += 1
                    else:
                        user, created = User.objects.update_or_create(
                            user_id=employee_id,
                            defaults={
                                'name': row['name'].strip(),
                                'role': UserRole.COUNSELOR,
                            }
                        )
                        if created:
                            user.set_password(row.get('password', employee_id))
                            user.save()
                            summary['created'] += 1
                        else:
                            summary['updated'] += 1

                        self.stdout.write(f'{"Created" if created else "Updated"} counselor: {user.user_id}')

        except FileNotFoundError:
            raise CommandError(f"File not found: {filepath}")
        except Exception as e:
            raise CommandError(f"Error importing counselors: {str(e)}")

    @transaction.atomic
    def import_mappings(self, filepath, dry_run, summary):
        """Import class mappings from CSV with validation"""
        required_fields = ['class_id', 'counselor_employee_id']


exec
/bin/bash -lc "rtk sed -n '60,95p' docs/数据对接说明文档.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
|---------------|---------------|----------|------|------|------|
| 学号 | student_id | 文本 | 是 | 学生唯一标识 | 2022001 |
| 姓名 | name | 文本 | 是 | 学生姓名 | 张三 |
| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
| 专业 | major | 文本 | 是 | 所属专业 | 计算机科学与技术 |
| 班级ID | class_id | 文本 | 是 | 班级唯一标识（重要） | CS2022-01 |
| 班级名称 | class_name | 文本 | 否 | 班级名称（用于展示） | 计算机科学与技术2022级1班 |
| 年级 | grade | 整数 | 是 | 入学年份 | 2022 |
| 毕业年份 | graduation_year | 整数 | 是 | 预计毕业年份 | 2026 |
| 是否毕业生 | is_graduating | 布尔 | 是 | 是否为当届毕业生 | true |

**可选字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 说明 | 示例 |
|---------------|---------------|----------|------|------|
| 手机号 | phone | 文本 | 用于找回密码 | 13800138000 |
| 邮箱 | email | 文本 | 用于通知 | zhangsan@example.com |

**重要说明：**
- `class_id` 必须全校唯一，用于映射辅导员，不能重复、变更或跨届复用
- `class_name` 仅用于展示，可以重复
- `is_graduating=true` 表示具备本批次离校申请资格
- 只需导入当届毕业生（约1000人），不需要全部学生

### 2.3 CSV模板

**文件名：** `学生基本信息导入模板.csv`

**文件编码：** UTF-8（避免中文乱码）

**模板内容：**
```csv
student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
2022001,张三,计算机学院,计算机科学与技术,CS2022-01,计算机科学与技术2022级1班,2022,2026,true,13800138000,zhangsan@example.com
2022002,李四,计算机学院,软件工程,SE2022-01,软件工程2022级1班,2022,2026,true,13800138001,lisi@example.com
```

exec
/bin/bash -lc "rtk sed -n '90,160p' docs/phase4c-xg-field-coverage.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
### 4.1 可映射字段

| 内部目标 | 来源字段 | 映射状态 | 处理规则 |
|---------|---------|---------|---------|
| `User.user_id` | `number` | 🟡 待确认 | **必填**。缺失则跳过该用户，记录到跳过日志。需live确认`number`是否等同学号/工号。 |
| `User.name` | `name` | 🟡 待确认 | **必填**。缺失则跳过该用户，记录到跳过日志。 |
| `User.phone` | `phone` | 🟡 待确认 | **可选**。缺失则置为NULL。 |
| `User.department` | `department` | 🟡 待确认 | **可选**。缺失则置为NULL。 |

### 4.2 角色映射（高风险）

| 内部目标 | 来源字段 | 映射状态 | 处理规则 |
|---------|---------|---------|---------|
| `User.role` | `user_identity` | 🔴 未确认 | **必填，高风险**。<br>- 需live确认`user_identity`值域（可能是1/2/3或student/teacher/staff）<br>- **初期策略：只接受明确的"学生"值，其他值一律跳过**<br>- 跳过原因：`unknown_user_identity: {value}` |

**角色映射规则（待live确认后补充）：**
```python
# 示例（需根据live数据调整）
USER_IDENTITY_MAP = {
    '1': 'student',      # 假设1代表学生
    'student': 'student', # 假设直接返回student
    # 其他值一律跳过，不做推断
}
```

### 4.3 无法映射字段（必须CSV维护）

| 内部目标 | 来源字段 | 映射状态 | 处理规则 |
|---------|---------|---------|---------|
| `User.class_id` | 未知 | 🔴 缺失 | **学生必填，API无法提供**。<br>- 继续由CSV/手工维护<br>- API同步时不覆盖此字段<br>- 新用户如果缺失`class_id`，标记为`skip_reason: missing_class_id` |
| `User.is_graduating` | 未知 | 🔴 缺失 | **学生必填，API无法提供**。<br>- 继续由CSV/手工维护<br>- API同步时不覆盖此字段<br>- 新用户如果缺失，标记为`skip_reason: missing_is_graduating` |
| `User.graduation_year` | 未知 | 🔴 缺失 | **学生必填，API无法提供**。<br>- 继续由CSV/手工维护<br>- API同步时不覆盖此字段<br>- 新用户如果缺失，标记为`skip_reason: missing_graduation_year` |

---

## 五、字段缺失处理规则

### 5.1 跳过规则（不创建/更新用户）

以下情况跳过该用户记录，不进行任何数据库操作：

| 场景 | 跳过原因标识 | 说明 |
|------|-------------|------|
| `number`缺失 | `missing_user_id` | 主键缺失，无法唯一识别用户 |
| `name`缺失 | `missing_name` | 必填字段缺失 |
| `user_identity`未知 | `unknown_user_identity: {value}` | 角色无法识别，不做推断 |
| `user_identity`非学生 | `not_student: {value}` | 初期只同步学生用户 |

### 5.2 部分映射规则（可创建/更新用户）

以下情况可以创建或更新用户，但某些字段置为NULL或保持原值：

| 场景 | 处理方式 |
|------|---------|
| `phone`缺失 | 置为NULL（新用户）或保持原值（已存在用户） |
| `email`缺失 | 置为NULL（新用户）或保持原值（已存在用户） |
| `department`缺失 | 置为NULL（新用户）或保持原值（已存在用户） |
| `class_id`缺失 | 保持原值（不覆盖），新用户跳过并标记`missing_class_id` |
| `is_graduating`缺失 | 保持原值（不覆盖），新用户跳过并标记`missing_is_graduating` |
| `graduation_year`缺失 | 保持原值（不覆盖），新用户跳过并标记`missing_graduation_year` |

### 5.3 错误报告格式

跳过的用户应输出到同步日志和错误报告：

```json
{
  "skipped_users": [
    {
      "number": "2022001",
      "name": "张三",

codex
I’m adding `106-step4b-model-extension-strategy-codex-response.md` now. The response will recommend “扩展模型 + 不允许 name 覆盖”, and it will explicitly reject a `name`-only Step 4B because that would undermine the earlier CSV/API authority split.
apply patch
patch: completed
/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md
diff --git a/docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md b/docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..c38f2e0921d9e92c4259897ff8a80282f341b713
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md
@@ -0,0 +1,181 @@
+# Phase 4C Step 4B前置 - User模型扩展策略Codex审查响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**针对文档：** `docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md`  
+**审查类型：** 模型扩展策略 / 数据源权威性决策 / Step 4B范围确认  
+**文档编号：** 106
+
+---
+
+## 审查结论
+
+**推荐选项组合2：扩展User模型 + 不允许学工API覆盖name。**
+
+Step 4B应该新增并持久化`phone`、`email`、`department`三个API补充字段，但继续保持`name`、`class_id`、`is_graduating`、`graduation_year`由CSV/手工维护。这个方案与既有Phase 1策略一致：CSV负责用户创建和核心业务字段，学工API只补充联系方式/院系等非核心字段。
+
+不推荐组合1，因为允许API覆盖`name`会破坏已达成的CSV主导边界，并引入CSV重新导入与API同步之间的反复覆盖问题。不推荐组合3，因为它会让Step 4B没有真实写入目标，最终只能停留在Step 4A的候选报告。
+
+---
+
+## 问题清单
+
+### P1：如果不扩展模型，Step 4B应取消而不是伪实现
+
+当前`User`模型只包含`user_id/name/role/active/class_id/is_graduating/graduation_year`，mapper输出的`phone/department`无处落库。若选择“不扩展模型”，Step 4B不应改为`name`覆盖或其他轻量写入；应明确标记为跳过，保留Step 4A只读报告，并将后续Step 5命令限定为dry-run/plan命令。
+
+### P1：name不应纳入API upsert字段
+
+字段覆盖契约已经定义CSV负责`user_id/name/role/class_id/is_graduating/graduation_year`，API负责`phone/email/department`。`name`虽然来自API，但它是核心身份展示字段，且CSV导入当前会更新`name`。允许API覆盖会造成数据源权威性不清晰。
+
+建议在Step 4B中完全不写`name`。如需观察差异，可以只输出`name_mismatch` warning或conflict报告，不修改数据库。
+
+### P2：email字段需要同时补mapper和测试
+
+字段契约包含`email`，但当前`map_xg_user_to_internal()`只提取`phone`和`department`。如果模型新增`email`，Step 4B应同步补充mapper提取和测试；否则会出现模型有字段但服务永远无法更新的半成品状态。
+
+### P2：不要新增API语义的updated_at字段
+
+`User`模型已有本地`updated_at = auto_now=True`。Step 4B不应直接把学工API的`updated_at`并入同名字段，也不建议现在新增`xg_updated_at`。API更新时间语义尚未live确认，且当前目标是解除补充字段落库阻塞。同步审计字段可在命令入口或审计需求明确后再设计。
+
+---
+
+## 字段扩展决策
+
+### 推荐新增字段
+
+```python
+phone = models.CharField(max_length=20, null=True, blank=True)
+email = models.EmailField(null=True, blank=True)
+department = models.CharField(max_length=100, null=True, blank=True)
+```
+
+迁移风险低：三个字段均为nullable，不影响现有行写入，不需要数据回填，回滚也清晰。`phone`使用`CharField`而不是整数类型是正确的，因为手机号可能包含前导0、区号、分机、符号或非大陆格式。
+
+### API缺失值处理
+
+对已存在用户，Step 4B应采用保守规则：
+
+- API返回非空值且与本地不同：更新该字段
+- API未返回字段、返回`None`或空字符串：保持本地原值
+- 不在本阶段实现“API清空本地联系方式”
+
+这个规则能避免API抽样、权限、分页或字段缺失导致已有联系方式被误清空。若未来确认API是权威联系方式源，再单独增加“允许清空”的策略开关。
+
+---
+
+## name覆盖决策
+
+**不允许API更新`name`。**
+
+推荐冲突优先级：
+
+| 字段类别 | 字段 | 权威来源 | API同步行为 |
+|---------|------|----------|-------------|
+| 身份核心 | `user_id` | CSV/本地主键 | 只匹配，不修改 |
+| 身份展示 | `name` | CSV | 不修改，可报告差异 |
+| 角色/权限 | `role` | CSV/本地 | 只验证学生身份，冲突则跳过 |
+| 业务核心 | `class_id/is_graduating/graduation_year` | CSV | 不修改 |
+| 补充资料 | `phone/email/department` | 学工API | 仅更新已存在学生 |
+
+不需要为`name`引入`updated_at`比较策略。时间戳比较不能解决“哪个系统更权威”的问题，只会把权威性决策隐藏到时间顺序里。
+
+---
+
+## Step 4B实施范围
+
+### 最小可交付范围
+
+1. User模型新增`phone/email/department`并生成migration。
+2. mapper新增`email`提取，缺失时返回`None`。
+3. 新增真实同步服务，或扩展现有服务为明确的dry-run/apply双模式。
+4. 仅对本地已存在且`role='student'`的用户更新补充字段。
+5. 本地不存在用户继续不创建。
+6. 本地角色不是student时继续输出conflict并跳过。
+7. 不更新`name/class_id/is_graduating/graduation_year/role/active`。
+8. 返回真实写入统计，例如`candidate_count`、`updated_count`、`unchanged_count`、`changed_fields_by_user`、`conflicts`、`warnings`。
+
+### 不建议纳入Step 4B
+
+- 不做`name`覆盖。
+- 不创建新用户。
+- 不扩展CSV导入器读取`phone/email/department`，除非另开CSV契约修订。
+- 不调整REST serializer公开字段，除非产品/API契约明确需要展示这些字段。
+- 不引入API时间戳权威判断。
+
+### 预计工作量
+
+预计40-70分钟：
+
+- 模型+migration：10-15分钟
+- mapper email补充+测试：10-15分钟
+- 同步服务真实更新+测试：25-40分钟
+- 回归验证：5-10分钟
+
+---
+
+## 验收标准
+
+Step 4B完成时应满足：
+
+1. `makemigrations`生成只包含`phone/email/department`的users migration。
+2. mapper测试覆盖`email`存在、缺失两个场景。
+3. 服务测试覆盖已存在学生更新`phone/email/department`。
+4. 服务测试覆盖API缺失补充字段时保持本地原值。
+5. 服务测试覆盖幂等：第二次同步`updated_count=0`或等价无变化统计。
+6. 服务测试覆盖不创建本地缺失用户。
+7. 服务测试覆盖角色冲突不更新。
+8. 服务测试覆盖`name/class_id/is_graduating/graduation_year`不被API覆盖。
+9. Step 4A中的“no API supplemental fields can be persisted” warning应被移除或改为只在字段不可写时触发。
+
+---
+
+## Q1-Q5回答
+
+### Q1：字段契约定义 vs 当前需求
+
+当前系统未证明页面或业务流程立即需要`phone/email/department`，但字段契约和Phase 1策略已经把它们定义为API补充字段；同时这三个字段是通知、联系、展示和院系统计的自然基础字段。考虑到nullable migration风险低，且Step 4B需要真实写入目标，现在扩展是合理的。
+
+关键边界是：新增字段不等于立即扩大所有API/CSV表面。先解决存储和同步闭环即可。
+
+### Q2：CSV与API权威性
+
+Phase 1应明确为：CSV是用户存在性、角色、班级、毕业资格、姓名的权威来源；学工API是联系方式和院系补充来源。API不是当前阶段的用户主数据源。
+
+因此，CSV可持续导入并覆盖核心字段；API只更新补充字段。
+
+### Q3：migration时机
+
+建议现在做，在Step 5命令入口前完成。原因是Step 5如果基于当前模型继续推进，只能做dry-run命令；真实同步命令仍会卡在字段gap。现在新增nullable字段影响面小，也能让后续命令、测试、验收基于同一套真实行为。
+
+### Q4：mapper email提取
+
+需要补充。即使live数据暂未确认`email`字段，也应让mapper支持直接字段提取：
+
+```python
+email = xg_user.get('email')
+result['email'] = email
+```
+
+如果API实际字段名不是`email`，后续live样本确认后再增加别名映射。当前不要猜测复杂字段名。
+
+### Q5：Step 4B最小范围
+
+最小范围应包含`phone/email/department`三字段的真实持久化。若担心email数据源不确定，也仍建议模型包含email，mapper先按直接`email`字段提取，服务自然只在API提供非空email时更新。
+
+不建议做Step 4B-lite仅更新`name`。这会绕开真正的字段gap，并制造新的CSV/API冲突。
+
+---
+
+## 最终建议
+
+批准进入Step 4B实现，采用以下决策：
+
+1. 新增`User.phone`、`User.email`、`User.department`。
+2. API只更新已存在学生的补充字段。
+3. API不创建用户。
+4. API不覆盖`name`和毕业业务核心字段。
+5. mapper补`email`。
+6. 缺失/空补充字段保持本地原值。
+7. Step 4B测试以“真实写入 + 幂等 + 不覆盖核心字段”为验收核心。
+

diff --git a/docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md b/docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..c38f2e0921d9e92c4259897ff8a80282f341b713
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md
@@ -0,0 +1,181 @@
+# Phase 4C Step 4B前置 - User模型扩展策略Codex审查响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**针对文档：** `docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md`  
+**审查类型：** 模型扩展策略 / 数据源权威性决策 / Step 4B范围确认  
+**文档编号：** 106
+
+---
+
+## 审查结论
+
+**推荐选项组合2：扩展User模型 + 不允许学工API覆盖name。**
+
+Step 4B应该新增并持久化`phone`、`email`、`department`三个API补充字段，但继续保持`name`、`class_id`、`is_graduating`、`graduation_year`由CSV/手工维护。这个方案与既有Phase 1策略一致：CSV负责用户创建和核心业务字段，学工API只补充联系方式/院系等非核心字段。
+
+不推荐组合1，因为允许API覆盖`name`会破坏已达成的CSV主导边界，并引入CSV重新导入与API同步之间的反复覆盖问题。不推荐组合3，因为它会让Step 4B没有真实写入目标，最终只能停留在Step 4A的候选报告。
+
+---
+
+## 问题清单
+
+### P1：如果不扩展模型，Step 4B应取消而不是伪实现
+
+当前`User`模型只包含`user_id/name/role/active/class_id/is_graduating/graduation_year`，mapper输出的`phone/department`无处落库。若选择“不扩展模型”，Step 4B不应改为`name`覆盖或其他轻量写入；应明确标记为跳过，保留Step 4A只读报告，并将后续Step 5命令限定为dry-run/plan命令。
+
+### P1：name不应纳入API upsert字段
+
+字段覆盖契约已经定义CSV负责`user_id/name/role/class_id/is_graduating/graduation_year`，API负责`phone/email/department`。`name`虽然来自API，但它是核心身份展示字段，且CSV导入当前会更新`name`。允许API覆盖会造成数据源权威性不清晰。
+
+建议在Step 4B中完全不写`name`。如需观察差异，可以只输出`name_mismatch` warning或conflict报告，不修改数据库。
+
+### P2：email字段需要同时补mapper和测试
+
+字段契约包含`email`，但当前`map_xg_user_to_internal()`只提取`phone`和`department`。如果模型新增`email`，Step 4B应同步补充mapper提取和测试；否则会出现模型有字段但服务永远无法更新的半成品状态。
+
+### P2：不要新增API语义的updated_at字段
+
+`User`模型已有本地`updated_at = auto_now=True`。Step 4B不应直接把学工API的`updated_at`并入同名字段，也不建议现在新增`xg_updated_at`。API更新时间语义尚未live确认，且当前目标是解除补充字段落库阻塞。同步审计字段可在命令入口或审计需求明确后再设计。
+
+---
+
+## 字段扩展决策
+
+### 推荐新增字段
+
+```python
+phone = models.CharField(max_length=20, null=True, blank=True)
+email = models.EmailField(null=True, blank=True)
+department = models.CharField(max_length=100, null=True, blank=True)
+```
+
+迁移风险低：三个字段均为nullable，不影响现有行写入，不需要数据回填，回滚也清晰。`phone`使用`CharField`而不是整数类型是正确的，因为手机号可能包含前导0、区号、分机、符号或非大陆格式。
+
+### API缺失值处理
+
+对已存在用户，Step 4B应采用保守规则：
+
+- API返回非空值且与本地不同：更新该字段
+- API未返回字段、返回`None`或空字符串：保持本地原值
+- 不在本阶段实现“API清空本地联系方式”
+
+这个规则能避免API抽样、权限、分页或字段缺失导致已有联系方式被误清空。若未来确认API是权威联系方式源，再单独增加“允许清空”的策略开关。
+
+---
+
+## name覆盖决策
+
+**不允许API更新`name`。**
+
+推荐冲突优先级：
+
+| 字段类别 | 字段 | 权威来源 | API同步行为 |
+|---------|------|----------|-------------|
+| 身份核心 | `user_id` | CSV/本地主键 | 只匹配，不修改 |
+| 身份展示 | `name` | CSV | 不修改，可报告差异 |
+| 角色/权限 | `role` | CSV/本地 | 只验证学生身份，冲突则跳过 |
+| 业务核心 | `class_id/is_graduating/graduation_year` | CSV | 不修改 |
+| 补充资料 | `phone/email/department` | 学工API | 仅更新已存在学生 |
+
+不需要为`name`引入`updated_at`比较策略。时间戳比较不能解决“哪个系统更权威”的问题，只会把权威性决策隐藏到时间顺序里。
+
+---
+
+## Step 4B实施范围
+
+### 最小可交付范围
+
+1. User模型新增`phone/email/department`并生成migration。
+2. mapper新增`email`提取，缺失时返回`None`。
+3. 新增真实同步服务，或扩展现有服务为明确的dry-run/apply双模式。
+4. 仅对本地已存在且`role='student'`的用户更新补充字段。
+5. 本地不存在用户继续不创建。
+6. 本地角色不是student时继续输出conflict并跳过。
+7. 不更新`name/class_id/is_graduating/graduation_year/role/active`。
+8. 返回真实写入统计，例如`candidate_count`、`updated_count`、`unchanged_count`、`changed_fields_by_user`、`conflicts`、`warnings`。
+
+### 不建议纳入Step 4B
+
+- 不做`name`覆盖。
+- 不创建新用户。
+- 不扩展CSV导入器读取`phone/email/department`，除非另开CSV契约修订。
+- 不调整REST serializer公开字段，除非产品/API契约明确需要展示这些字段。
+- 不引入API时间戳权威判断。
+
+### 预计工作量
+
+预计40-70分钟：
+
+- 模型+migration：10-15分钟
+- mapper email补充+测试：10-15分钟
+- 同步服务真实更新+测试：25-40分钟
+- 回归验证：5-10分钟
+
+---
+
+## 验收标准
+
+Step 4B完成时应满足：
+
+1. `makemigrations`生成只包含`phone/email/department`的users migration。
+2. mapper测试覆盖`email`存在、缺失两个场景。
+3. 服务测试覆盖已存在学生更新`phone/email/department`。
+4. 服务测试覆盖API缺失补充字段时保持本地原值。
+5. 服务测试覆盖幂等：第二次同步`updated_count=0`或等价无变化统计。
+6. 服务测试覆盖不创建本地缺失用户。
+7. 服务测试覆盖角色冲突不更新。
+8. 服务测试覆盖`name/class_id/is_graduating/graduation_year`不被API覆盖。
+9. Step 4A中的“no API supplemental fields can be persisted” warning应被移除或改为只在字段不可写时触发。
+
+---
+
+## Q1-Q5回答
+
+### Q1：字段契约定义 vs 当前需求
+
+当前系统未证明页面或业务流程立即需要`phone/email/department`，但字段契约和Phase 1策略已经把它们定义为API补充字段；同时这三个字段是通知、联系、展示和院系统计的自然基础字段。考虑到nullable migration风险低，且Step 4B需要真实写入目标，现在扩展是合理的。
+
+关键边界是：新增字段不等于立即扩大所有API/CSV表面。先解决存储和同步闭环即可。
+
+### Q2：CSV与API权威性
+
+Phase 1应明确为：CSV是用户存在性、角色、班级、毕业资格、姓名的权威来源；学工API是联系方式和院系补充来源。API不是当前阶段的用户主数据源。
+
+因此，CSV可持续导入并覆盖核心字段；API只更新补充字段。
+
+### Q3：migration时机
+
+建议现在做，在Step 5命令入口前完成。原因是Step 5如果基于当前模型继续推进，只能做dry-run命令；真实同步命令仍会卡在字段gap。现在新增nullable字段影响面小，也能让后续命令、测试、验收基于同一套真实行为。
+
+### Q4：mapper email提取
+
+需要补充。即使live数据暂未确认`email`字段，也应让mapper支持直接字段提取：
+
+```python
+email = xg_user.get('email')
+result['email'] = email
+```
+
+如果API实际字段名不是`email`，后续live样本确认后再增加别名映射。当前不要猜测复杂字段名。
+
+### Q5：Step 4B最小范围
+
+最小范围应包含`phone/email/department`三字段的真实持久化。若担心email数据源不确定，也仍建议模型包含email，mapper先按直接`email`字段提取，服务自然只在API提供非空email时更新。
+
+不建议做Step 4B-lite仅更新`name`。这会绕开真正的字段gap，并制造新的CSV/API冲突。
+
+---
+
+## 最终建议
+
+批准进入Step 4B实现，采用以下决策：
+
+1. 新增`User.phone`、`User.email`、`User.department`。
+2. API只更新已存在学生的补充字段。
+3. API不创建用户。
+4. API不覆盖`name`和毕业业务核心字段。
+5. mapper补`email`。
+6. 缺失/空补充字段保持本地原值。
+7. Step 4B测试以“真实写入 + 幂等 + 不覆盖核心字段”为验收核心。
+

codex
The review artifact is created. I’m doing a quick readback and status check now to catch formatting issues and confirm I only added the intended document.
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Phase 4C Step 4B前置 - User模型扩展策略Codex审查响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**针对文档：** `docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md`  
**审查类型：** 模型扩展策略 / 数据源权威性决策 / Step 4B范围确认  
**文档编号：** 106

---

## 审查结论

**推荐选项组合2：扩展User模型 + 不允许学工API覆盖name。**

Step 4B应该新增并持久化`phone`、`email`、`department`三个API补充字段，但继续保持`name`、`class_id`、`is_graduating`、`graduation_year`由CSV/手工维护。这个方案与既有Phase 1策略一致：CSV负责用户创建和核心业务字段，学工API只补充联系方式/院系等非核心字段。

不推荐组合1，因为允许API覆盖`name`会破坏已达成的CSV主导边界，并引入CSV重新导入与API同步之间的反复覆盖问题。不推荐组合3，因为它会让Step 4B没有真实写入目标，最终只能停留在Step 4A的候选报告。

---

## 问题清单

### P1：如果不扩展模型，Step 4B应取消而不是伪实现

当前`User`模型只包含`user_id/name/role/active/class_id/is_graduating/graduation_year`，mapper输出的`phone/department`无处落库。若选择“不扩展模型”，Step 4B不应改为`name`覆盖或其他轻量写入；应明确标记为跳过，保留Step 4A只读报告，并将后续Step 5命令限定为dry-run/plan命令。

### P1：name不应纳入API upsert字段

字段覆盖契约已经定义CSV负责`user_id/name/role/class_id/is_graduating/graduation_year`，API负责`phone/email/department`。`name`虽然来自API，但它是核心身份展示字段，且CSV导入当前会更新`name`。允许API覆盖会造成数据源权威性不清晰。

建议在Step 4B中完全不写`name`。如需观察差异，可以只输出`name_mismatch` warning或conflict报告，不修改数据库。

### P2：email字段需要同时补mapper和测试

字段契约包含`email`，但当前`map_xg_user_to_internal()`只提取`phone`和`department`。如果模型新增`email`，Step 4B应同步补充mapper提取和测试；否则会出现模型有字段但服务永远无法更新的半成品状态。

### P2：不要新增API语义的updated_at字段

`User`模型已有本地`updated_at = auto_now=True`。Step 4B不应直接把学工API的`updated_at`并入同名字段，也不建议现在新增`xg_updated_at`。API更新时间语义尚未live确认，且当前目标是解除补充字段落库阻塞。同步审计字段可在命令入口或审计需求明确后再设计。

---

## 字段扩展决策

### 推荐新增字段

```python
phone = models.CharField(max_length=20, null=True, blank=True)
email = models.EmailField(null=True, blank=True)
department = models.CharField(max_length=100, null=True, blank=True)
```

迁移风险低：三个字段均为nullable，不影响现有行写入，不需要数据回填，回滚也清晰。`phone`使用`CharField`而不是整数类型是正确的，因为手机号可能包含前导0、区号、分机、符号或非大陆格式。

### API缺失值处理

对已存在用户，Step 4B应采用保守规则：

- API返回非空值且与本地不同：更新该字段
- API未返回字段、返回`None`或空字符串：保持本地原值
- 不在本阶段实现“API清空本地联系方式”

这个规则能避免API抽样、权限、分页或字段缺失导致已有联系方式被误清空。若未来确认API是权威联系方式源，再单独增加“允许清空”的策略开关。

---

## name覆盖决策

**不允许API更新`name`。**

推荐冲突优先级：

| 字段类别 | 字段 | 权威来源 | API同步行为 |
|---------|------|----------|-------------|
| 身份核心 | `user_id` | CSV/本地主键 | 只匹配，不修改 |
| 身份展示 | `name` | CSV | 不修改，可报告差异 |
| 角色/权限 | `role` | CSV/本地 | 只验证学生身份，冲突则跳过 |
| 业务核心 | `class_id/is_graduating/graduation_year` | CSV | 不修改 |
| 补充资料 | `phone/email/department` | 学工API | 仅更新已存在学生 |

不需要为`name`引入`updated_at`比较策略。时间戳比较不能解决“哪个系统更权威”的问题，只会把权威性决策隐藏到时间顺序里。

---

## Step 4B实施范围

### 最小可交付范围

1. User模型新增`phone/email/department`并生成migration。
2. mapper新增`email`提取，缺失时返回`None`。
3. 新增真实同步服务，或扩展现有服务为明确的dry-run/apply双模式。
4. 仅对本地已存在且`role='student'`的用户更新补充字段。
5. 本地不存在用户继续不创建。
6. 本地角色不是student时继续输出conflict并跳过。
7. 不更新`name/class_id/is_graduating/graduation_year/role/active`。
8. 返回真实写入统计，例如`candidate_count`、`updated_count`、`unchanged_count`、`changed_fields_by_user`、`conflicts`、`warnings`。

### 不建议纳入Step 4B

- 不做`name`覆盖。
- 不创建新用户。
- 不扩展CSV导入器读取`phone/email/department`，除非另开CSV契约修订。
- 不调整REST serializer公开字段，除非产品/API契约明确需要展示这些字段。
- 不引入API时间戳权威判断。

### 预计工作量

预计40-70分钟：

- 模型+migration：10-15分钟
- mapper email补充+测试：10-15分钟
- 同步服务真实更新+测试：25-40分钟
- 回归验证：5-10分钟

---

## 验收标准

Step 4B完成时应满足：

1. `makemigrations`生成只包含`phone/email/department`的users migration。
2. mapper测试覆盖`email`存在、缺失两个场景。
3. 服务测试覆盖已存在学生更新`phone/email/department`。
4. 服务测试覆盖API缺失补充字段时保持本地原值。
5. 服务测试覆盖幂等：第二次同步`updated_count=0`或等价无变化统计。
6. 服务测试覆盖不创建本地缺失用户。
7. 服务测试覆盖角色冲突不更新。
8. 服务测试覆盖`name/class_id/is_graduating/graduation_year`不被API覆盖。
9. Step 4A中的“no API supplemental fields can be persisted” warning应被移除或改为只在字段不可写时触发。

---

## Q1-Q5回答

### Q1：字段契约定义 vs 当前需求

当前系统未证明页面或业务流程立即需要`phone/email/department`，但字段契约和Phase 1策略已经把它们定义为API补充字段；同时这三个字段是通知、联系、展示和院系统计的自然基础字段。考虑到nullable migration风险低，且Step 4B需要真实写入目标，现在扩展是合理的。

关键边界是：新增字段不等于立即扩大所有API/CSV表面。先解决存储和同步闭环即可。

### Q2：CSV与API权威性

Phase 1应明确为：CSV是用户存在性、角色、班级、毕业资格、姓名的权威来源；学工API是联系方式和院系补充来源。API不是当前阶段的用户主数据源。

因此，CSV可持续导入并覆盖核心字段；API只更新补充字段。

### Q3：migration时机

建议现在做，在Step 5命令入口前完成。原因是Step 5如果基于当前模型继续推进，只能做dry-run命令；真实同步命令仍会卡在字段gap。现在新增nullable字段影响面小，也能让后续命令、测试、验收基于同一套真实行为。

### Q4：mapper email提取

需要补充。即使live数据暂未确认`email`字段，也应让mapper支持直接字段提取：

```python
email = xg_user.get('email')
result['email'] = email
```

如果API实际字段名不是`email`，后续live样本确认后再增加别名映射。当前不要猜测复杂字段名。

### Q5：Step 4B最小范围

最小范围应包含`phone/email/department`三字段的真实持久化。若担心email数据源不确定，也仍建议模型包含email，mapper先按直接`email`字段提取，服务自然只在API提供非空email时更新。

不建议做Step 4B-lite仅更新`name`。这会绕开真正的字段gap，并制造新的CSV/API冲突。

---

## 最终建议

批准进入Step 4B实现，采用以下决策：

1. 新增`User.phone`、`User.email`、`User.department`。
2. API只更新已存在学生的补充字段。
3. API不创建用户。
4. API不覆盖`name`和毕业业务核心字段。
5. mapper补`email`。
6. 缺失/空补充字段保持本地原值。
7. Step 4B测试以“真实写入 + 幂等 + 不覆盖核心字段”为验收核心。


exec
/bin/bash -lc 'rtk git status --short docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
?? docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md
diff --git a/docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md b/docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..c38f2e0921d9e92c4259897ff8a80282f341b713
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md
@@ -0,0 +1,181 @@
+# Phase 4C Step 4B前置 - User模型扩展策略Codex审查响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**针对文档：** `docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md`  
+**审查类型：** 模型扩展策略 / 数据源权威性决策 / Step 4B范围确认  
+**文档编号：** 106
+
+---
+
+## 审查结论
+
+**推荐选项组合2：扩展User模型 + 不允许学工API覆盖name。**
+
+Step 4B应该新增并持久化`phone`、`email`、`department`三个API补充字段，但继续保持`name`、`class_id`、`is_graduating`、`graduation_year`由CSV/手工维护。这个方案与既有Phase 1策略一致：CSV负责用户创建和核心业务字段，学工API只补充联系方式/院系等非核心字段。
+
+不推荐组合1，因为允许API覆盖`name`会破坏已达成的CSV主导边界，并引入CSV重新导入与API同步之间的反复覆盖问题。不推荐组合3，因为它会让Step 4B没有真实写入目标，最终只能停留在Step 4A的候选报告。
+
+---
+
+## 问题清单
+
+### P1：如果不扩展模型，Step 4B应取消而不是伪实现
+
+当前`User`模型只包含`user_id/name/role/active/class_id/is_graduating/graduation_year`，mapper输出的`phone/department`无处落库。若选择“不扩展模型”，Step 4B不应改为`name`覆盖或其他轻量写入；应明确标记为跳过，保留Step 4A只读报告，并将后续Step 5命令限定为dry-run/plan命令。
+
+### P1：name不应纳入API upsert字段
+
+字段覆盖契约已经定义CSV负责`user_id/name/role/class_id/is_graduating/graduation_year`，API负责`phone/email/department`。`name`虽然来自API，但它是核心身份展示字段，且CSV导入当前会更新`name`。允许API覆盖会造成数据源权威性不清晰。
+
+建议在Step 4B中完全不写`name`。如需观察差异，可以只输出`name_mismatch` warning或conflict报告，不修改数据库。
+
+### P2：email字段需要同时补mapper和测试
+
+字段契约包含`email`，但当前`map_xg_user_to_internal()`只提取`phone`和`department`。如果模型新增`email`，Step 4B应同步补充mapper提取和测试；否则会出现模型有字段但服务永远无法更新的半成品状态。
+
+### P2：不要新增API语义的updated_at字段
+
+`User`模型已有本地`updated_at = auto_now=True`。Step 4B不应直接把学工API的`updated_at`并入同名字段，也不建议现在新增`xg_updated_at`。API更新时间语义尚未live确认，且当前目标是解除补充字段落库阻塞。同步审计字段可在命令入口或审计需求明确后再设计。
+
+---
+
+## 字段扩展决策
+
+### 推荐新增字段
+
+```python
+phone = models.CharField(max_length=20, null=True, blank=True)
+email = models.EmailField(null=True, blank=True)
+department = models.CharField(max_length=100, null=True, blank=True)
+```
+
+迁移风险低：三个字段均为nullable，不影响现有行写入，不需要数据回填，回滚也清晰。`phone`使用`CharField`而不是整数类型是正确的，因为手机号可能包含前导0、区号、分机、符号或非大陆格式。
+
+### API缺失值处理
+
+对已存在用户，Step 4B应采用保守规则：
+
+- API返回非空值且与本地不同：更新该字段
+- API未返回字段、返回`None`或空字符串：保持本地原值
+- 不在本阶段实现“API清空本地联系方式”
+
+这个规则能避免API抽样、权限、分页或字段缺失导致已有联系方式被误清空。若未来确认API是权威联系方式源，再单独增加“允许清空”的策略开关。
+
+---
+
+## name覆盖决策
+
+**不允许API更新`name`。**
+
+推荐冲突优先级：
+
+| 字段类别 | 字段 | 权威来源 | API同步行为 |
+|---------|------|----------|-------------|
+| 身份核心 | `user_id` | CSV/本地主键 | 只匹配，不修改 |
+| 身份展示 | `name` | CSV | 不修改，可报告差异 |
+| 角色/权限 | `role` | CSV/本地 | 只验证学生身份，冲突则跳过 |
+| 业务核心 | `class_id/is_graduating/graduation_year` | CSV | 不修改 |
+| 补充资料 | `phone/email/department` | 学工API | 仅更新已存在学生 |
+
+不需要为`name`引入`updated_at`比较策略。时间戳比较不能解决“哪个系统更权威”的问题，只会把权威性决策隐藏到时间顺序里。
+
+---
+
+## Step 4B实施范围
+
+### 最小可交付范围
+
+1. User模型新增`phone/email/department`并生成migration。
+2. mapper新增`email`提取，缺失时返回`None`。
+3. 新增真实同步服务，或扩展现有服务为明确的dry-run/apply双模式。
+4. 仅对本地已存在且`role='student'`的用户更新补充字段。
+5. 本地不存在用户继续不创建。
+6. 本地角色不是student时继续输出conflict并跳过。
+7. 不更新`name/class_id/is_graduating/graduation_year/role/active`。
+8. 返回真实写入统计，例如`candidate_count`、`updated_count`、`unchanged_count`、`changed_fields_by_user`、`conflicts`、`warnings`。
+
+### 不建议纳入Step 4B
+
+- 不做`name`覆盖。
+- 不创建新用户。
+- 不扩展CSV导入器读取`phone/email/department`，除非另开CSV契约修订。
+- 不调整REST serializer公开字段，除非产品/API契约明确需要展示这些字段。
+- 不引入API时间戳权威判断。
+
+### 预计工作量
+
+预计40-70分钟：
+
+- 模型+migration：10-15分钟
+- mapper email补充+测试：10-15分钟
+- 同步服务真实更新+测试：25-40分钟
+- 回归验证：5-10分钟
+
+---
+
+## 验收标准
+
+Step 4B完成时应满足：
+
+1. `makemigrations`生成只包含`phone/email/department`的users migration。
+2. mapper测试覆盖`email`存在、缺失两个场景。
+3. 服务测试覆盖已存在学生更新`phone/email/department`。
+4. 服务测试覆盖API缺失补充字段时保持本地原值。
+5. 服务测试覆盖幂等：第二次同步`updated_count=0`或等价无变化统计。
+6. 服务测试覆盖不创建本地缺失用户。
+7. 服务测试覆盖角色冲突不更新。
+8. 服务测试覆盖`name/class_id/is_graduating/graduation_year`不被API覆盖。
+9. Step 4A中的“no API supplemental fields can be persisted” warning应被移除或改为只在字段不可写时触发。
+
+---
+
+## Q1-Q5回答
+
+### Q1：字段契约定义 vs 当前需求
+
+当前系统未证明页面或业务流程立即需要`phone/email/department`，但字段契约和Phase 1策略已经把它们定义为API补充字段；同时这三个字段是通知、联系、展示和院系统计的自然基础字段。考虑到nullable migration风险低，且Step 4B需要真实写入目标，现在扩展是合理的。
+
+关键边界是：新增字段不等于立即扩大所有API/CSV表面。先解决存储和同步闭环即可。
+
+### Q2：CSV与API权威性
+
+Phase 1应明确为：CSV是用户存在性、角色、班级、毕业资格、姓名的权威来源；学工API是联系方式和院系补充来源。API不是当前阶段的用户主数据源。
+
+因此，CSV可持续导入并覆盖核心字段；API只更新补充字段。
+
+### Q3：migration时机
+
+建议现在做，在Step 5命令入口前完成。原因是Step 5如果基于当前模型继续推进，只能做dry-run命令；真实同步命令仍会卡在字段gap。现在新增nullable字段影响面小，也能让后续命令、测试、验收基于同一套真实行为。
+
+### Q4：mapper email提取
+
+需要补充。即使live数据暂未确认`email`字段，也应让mapper支持直接字段提取：
+
+```python
+email = xg_user.get('email')
+result['email'] = email
+```
+
+如果API实际字段名不是`email`，后续live样本确认后再增加别名映射。当前不要猜测复杂字段名。
+
+### Q5：Step 4B最小范围
+
+最小范围应包含`phone/email/department`三字段的真实持久化。若担心email数据源不确定，也仍建议模型包含email，mapper先按直接`email`字段提取，服务自然只在API提供非空email时更新。
+
+不建议做Step 4B-lite仅更新`name`。这会绕开真正的字段gap，并制造新的CSV/API冲突。
+
+---
+
+## 最终建议
+
+批准进入Step 4B实现，采用以下决策：
+
+1. 新增`User.phone`、`User.email`、`User.department`。
+2. API只更新已存在学生的补充字段。
+3. API不创建用户。
+4. API不覆盖`name`和毕业业务核心字段。
+5. mapper补`email`。
+6. 缺失/空补充字段保持本地原值。
+7. Step 4B测试以“真实写入 + 幂等 + 不覆盖核心字段”为验收核心。
+

codex
Created the Codex strategy response at [106-step4b-model-extension-strategy-codex-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:1).

Key decision: recommend **选项组合2：扩展 `User.phone/email/department` + 不允许学工API覆盖 `name`**. The response also defines Step 4B scope, missing/empty API field behavior, mapper `email` requirement, and acceptance criteria.

No tests were run because this was a documentation/review artifact only.
diff --git a/docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md b/docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..c38f2e0921d9e92c4259897ff8a80282f341b713
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md
@@ -0,0 +1,181 @@
+# Phase 4C Step 4B前置 - User模型扩展策略Codex审查响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**针对文档：** `docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md`  
+**审查类型：** 模型扩展策略 / 数据源权威性决策 / Step 4B范围确认  
+**文档编号：** 106
+
+---
+
+## 审查结论
+
+**推荐选项组合2：扩展User模型 + 不允许学工API覆盖name。**
+
+Step 4B应该新增并持久化`phone`、`email`、`department`三个API补充字段，但继续保持`name`、`class_id`、`is_graduating`、`graduation_year`由CSV/手工维护。这个方案与既有Phase 1策略一致：CSV负责用户创建和核心业务字段，学工API只补充联系方式/院系等非核心字段。
+
+不推荐组合1，因为允许API覆盖`name`会破坏已达成的CSV主导边界，并引入CSV重新导入与API同步之间的反复覆盖问题。不推荐组合3，因为它会让Step 4B没有真实写入目标，最终只能停留在Step 4A的候选报告。
+
+---
+
+## 问题清单
+
+### P1：如果不扩展模型，Step 4B应取消而不是伪实现
+
+当前`User`模型只包含`user_id/name/role/active/class_id/is_graduating/graduation_year`，mapper输出的`phone/department`无处落库。若选择“不扩展模型”，Step 4B不应改为`name`覆盖或其他轻量写入；应明确标记为跳过，保留Step 4A只读报告，并将后续Step 5命令限定为dry-run/plan命令。
+
+### P1：name不应纳入API upsert字段
+
+字段覆盖契约已经定义CSV负责`user_id/name/role/class_id/is_graduating/graduation_year`，API负责`phone/email/department`。`name`虽然来自API，但它是核心身份展示字段，且CSV导入当前会更新`name`。允许API覆盖会造成数据源权威性不清晰。
+
+建议在Step 4B中完全不写`name`。如需观察差异，可以只输出`name_mismatch` warning或conflict报告，不修改数据库。
+
+### P2：email字段需要同时补mapper和测试
+
+字段契约包含`email`，但当前`map_xg_user_to_internal()`只提取`phone`和`department`。如果模型新增`email`，Step 4B应同步补充mapper提取和测试；否则会出现模型有字段但服务永远无法更新的半成品状态。
+
+### P2：不要新增API语义的updated_at字段
+
+`User`模型已有本地`updated_at = auto_now=True`。Step 4B不应直接把学工API的`updated_at`并入同名字段，也不建议现在新增`xg_updated_at`。API更新时间语义尚未live确认，且当前目标是解除补充字段落库阻塞。同步审计字段可在命令入口或审计需求明确后再设计。
+
+---
+
+## 字段扩展决策
+
+### 推荐新增字段
+
+```python
+phone = models.CharField(max_length=20, null=True, blank=True)
+email = models.EmailField(null=True, blank=True)
+department = models.CharField(max_length=100, null=True, blank=True)
+```
+
+迁移风险低：三个字段均为nullable，不影响现有行写入，不需要数据回填，回滚也清晰。`phone`使用`CharField`而不是整数类型是正确的，因为手机号可能包含前导0、区号、分机、符号或非大陆格式。
+
+### API缺失值处理
+
+对已存在用户，Step 4B应采用保守规则：
+
+- API返回非空值且与本地不同：更新该字段
+- API未返回字段、返回`None`或空字符串：保持本地原值
+- 不在本阶段实现“API清空本地联系方式”
+
+这个规则能避免API抽样、权限、分页或字段缺失导致已有联系方式被误清空。若未来确认API是权威联系方式源，再单独增加“允许清空”的策略开关。
+
+---
+
+## name覆盖决策
+
+**不允许API更新`name`。**
+
+推荐冲突优先级：
+
+| 字段类别 | 字段 | 权威来源 | API同步行为 |
+|---------|------|----------|-------------|
+| 身份核心 | `user_id` | CSV/本地主键 | 只匹配，不修改 |
+| 身份展示 | `name` | CSV | 不修改，可报告差异 |
+| 角色/权限 | `role` | CSV/本地 | 只验证学生身份，冲突则跳过 |
+| 业务核心 | `class_id/is_graduating/graduation_year` | CSV | 不修改 |
+| 补充资料 | `phone/email/department` | 学工API | 仅更新已存在学生 |
+
+不需要为`name`引入`updated_at`比较策略。时间戳比较不能解决“哪个系统更权威”的问题，只会把权威性决策隐藏到时间顺序里。
+
+---
+
+## Step 4B实施范围
+
+### 最小可交付范围
+
+1. User模型新增`phone/email/department`并生成migration。
+2. mapper新增`email`提取，缺失时返回`None`。
+3. 新增真实同步服务，或扩展现有服务为明确的dry-run/apply双模式。
+4. 仅对本地已存在且`role='student'`的用户更新补充字段。
+5. 本地不存在用户继续不创建。
+6. 本地角色不是student时继续输出conflict并跳过。
+7. 不更新`name/class_id/is_graduating/graduation_year/role/active`。
+8. 返回真实写入统计，例如`candidate_count`、`updated_count`、`unchanged_count`、`changed_fields_by_user`、`conflicts`、`warnings`。
+
+### 不建议纳入Step 4B
+
+- 不做`name`覆盖。
+- 不创建新用户。
+- 不扩展CSV导入器读取`phone/email/department`，除非另开CSV契约修订。
+- 不调整REST serializer公开字段，除非产品/API契约明确需要展示这些字段。
+- 不引入API时间戳权威判断。
+
+### 预计工作量
+
+预计40-70分钟：
+
+- 模型+migration：10-15分钟
+- mapper email补充+测试：10-15分钟
+- 同步服务真实更新+测试：25-40分钟
+- 回归验证：5-10分钟
+
+---
+
+## 验收标准
+
+Step 4B完成时应满足：
+
+1. `makemigrations`生成只包含`phone/email/department`的users migration。
+2. mapper测试覆盖`email`存在、缺失两个场景。
+3. 服务测试覆盖已存在学生更新`phone/email/department`。
+4. 服务测试覆盖API缺失补充字段时保持本地原值。
+5. 服务测试覆盖幂等：第二次同步`updated_count=0`或等价无变化统计。
+6. 服务测试覆盖不创建本地缺失用户。
+7. 服务测试覆盖角色冲突不更新。
+8. 服务测试覆盖`name/class_id/is_graduating/graduation_year`不被API覆盖。
+9. Step 4A中的“no API supplemental fields can be persisted” warning应被移除或改为只在字段不可写时触发。
+
+---
+
+## Q1-Q5回答
+
+### Q1：字段契约定义 vs 当前需求
+
+当前系统未证明页面或业务流程立即需要`phone/email/department`，但字段契约和Phase 1策略已经把它们定义为API补充字段；同时这三个字段是通知、联系、展示和院系统计的自然基础字段。考虑到nullable migration风险低，且Step 4B需要真实写入目标，现在扩展是合理的。
+
+关键边界是：新增字段不等于立即扩大所有API/CSV表面。先解决存储和同步闭环即可。
+
+### Q2：CSV与API权威性
+
+Phase 1应明确为：CSV是用户存在性、角色、班级、毕业资格、姓名的权威来源；学工API是联系方式和院系补充来源。API不是当前阶段的用户主数据源。
+
+因此，CSV可持续导入并覆盖核心字段；API只更新补充字段。
+
+### Q3：migration时机
+
+建议现在做，在Step 5命令入口前完成。原因是Step 5如果基于当前模型继续推进，只能做dry-run命令；真实同步命令仍会卡在字段gap。现在新增nullable字段影响面小，也能让后续命令、测试、验收基于同一套真实行为。
+
+### Q4：mapper email提取
+
+需要补充。即使live数据暂未确认`email`字段，也应让mapper支持直接字段提取：
+
+```python
+email = xg_user.get('email')
+result['email'] = email
+```
+
+如果API实际字段名不是`email`，后续live样本确认后再增加别名映射。当前不要猜测复杂字段名。
+
+### Q5：Step 4B最小范围
+
+最小范围应包含`phone/email/department`三字段的真实持久化。若担心email数据源不确定，也仍建议模型包含email，mapper先按直接`email`字段提取，服务自然只在API提供非空email时更新。
+
+不建议做Step 4B-lite仅更新`name`。这会绕开真正的字段gap，并制造新的CSV/API冲突。
+
+---
+
+## 最终建议
+
+批准进入Step 4B实现，采用以下决策：
+
+1. 新增`User.phone`、`User.email`、`User.department`。
+2. API只更新已存在学生的补充字段。
+3. API不创建用户。
+4. API不覆盖`name`和毕业业务核心字段。
+5. mapper补`email`。
+6. 缺失/空补充字段保持本地原值。
+7. Step 4B测试以“真实写入 + 幂等 + 不覆盖核心字段”为验收核心。
+

tokens used
127,345

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
