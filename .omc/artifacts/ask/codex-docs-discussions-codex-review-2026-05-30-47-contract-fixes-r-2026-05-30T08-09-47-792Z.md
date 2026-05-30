# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-05-30T08:09:47.793Z

## Original task

请批判性审查 docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md 中的4个契约修复。要求：1) 逐项验证修复是否解决了上一轮指出的问题 2) 检查API端点统一性、错误样例完整性、DTO一致性、降级条件合理性 3) 明确回答'是否达到可执行契约标准' 4) 如果还有问题，按优先级列出并给出修复建议 5) 如果达标，确认可以冻结契约并开始Week 1工作

## Final prompt

请批判性审查 docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md 中的4个契约修复。要求：1) 逐项验证修复是否解决了上一轮指出的问题 2) 检查API端点统一性、错误样例完整性、DTO一致性、降级条件合理性 3) 明确回答'是否达到可执行契约标准' 4) 如果还有问题，按优先级列出并给出修复建议 5) 如果达标，确认可以冻结契约并开始Week 1工作

## Raw output

```text
已完成批判性审查，并按项目流程写入：

[49-contract-fixes-codex-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md)

结论：**尚未完全达到可执行契约标准，但非常接近**。4 个修复方向都正确，主要阻塞点已基本解决；但冻结前还应修 2 个 P1 和 2 个 P2：

- **P1**：错误样例未覆盖 Section 3 的全部错误码，缺 400、404、409、500。
- **P1**：风险表里仍同时写“砍学工部审批”和“Day 4补学工部审批”，降级口径冲突。
- **P2**：计划中仍混用“5个HTTP路由”和“4个API端点/能力”。
- **P2**：`AuthUserDTO` 已被引用，但未在 Section 1 正式定义。

明确回答：**现在还不建议冻结契约并全面开始 Week 1 Day 3-4 业务 API 实现**。可以先启动不受影响的 Week 1 Day 1-2：Django 骨架、模型、seed、登录认证。修完上述 P1 后，可以冻结 `contract-v0.1.md` 并开始 Week 1 工作。


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
session id: 019e77ec-3e3f-7611-b39e-a2ef266de2ba
--------
user
请批判性审查 docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md 中的4个契约修复。要求：1) 逐项验证修复是否解决了上一轮指出的问题 2) 检查API端点统一性、错误样例完整性、DTO一致性、降级条件合理性 3) 明确回答'是否达到可执行契约标准' 4) 如果还有问题，按优先级列出并给出修复建议 5) 如果达标，确认可以冻结契约并开始Week 1工作
codex
我会按项目的评审流程先读取本地协作协议和 Codex review 协议，然后再审查这份修复请求及相关上下文，确保结论按项目契约来给。
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

codex
协议要求所有命令走 `rtk`，后续命令我会按这个项目规则执行。接下来我会读取审查请求、上一轮指出的问题和它引用的契约文档来交叉验证。
exec
/bin/bash -lc 'rtk ls -la docs/discussions/codex-review-2026-05-30' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
37-api-blocking-solution-review-request.md  11.8K
38-codex-api-blocking-review.md  10.5K
39-claude-response-to-codex.md  10.8K
40-api-blocking-solution-consensus.md  11.6K
41-next-steps-critical-discussion-request.md  6.7K
42-next-steps-codex-critical-response.md  7.3K
43-next-steps-claude-response-round1.md  9.4K
44-next-steps-codex-response-round2.md  13.0K
45-next-steps-claude-response-round2.md  9.4K
46-next-steps-final-consensus.md  8.4K
47-contract-fixes-review-request.md  4.6K
48-contract-fixes-summary.md  2.3K

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Contract Fixes Review Request

**日期：** 2026-05-30  
**审查类型：** 契约修复验证  
**审查人：** Codex  
**文档编号：** 47

---

## 背景

在上一轮审查中（文档46），Codex指出contract-v0.1.md和week-0-1-execution-plan.md存在3-4个问题，导致契约"接近可执行契约"但未达到标准。

**Codex原话：**
> "结论：**还没有完全达到"可执行契约"标准，不建议直接开始 Week 1 的完整实施**。可以先启动不受争议影响的 Day 1 骨架、模型、seed、认证准备，但应先用半天把下面几个契约不一致点修掉再冻结。"

---

## 已完成的修复

### 修复1：统一API端点数量（主要阻塞点）

**问题：** 契约列出6个HTTP路由，计划说"5个核心API端点"（Week 0 Day 1）和"4个API端点"（Week 1 Day 3-4），口径不一致。

**修复：**
- 从contract-v0.1.md移除Section 4.4 GET /api/applications（列表端点）
- 统一为5个HTTP路由：
  1. POST /api/auth/login
  2. POST /api/applications
  3. GET /api/applications/{id}
  4. POST /api/approvals/{id}/approve
  5. POST /api/approvals/{id}/reject

**理由：** 列表端点不是最小纵向切片必需的，核心流程是"登录→提交→审批→查询单个申请"。

**文件：** docs/contracts/contract-v0.1.md（Section 4.4已删除）

---

### 修复2：添加503 PROVIDER_UNAVAILABLE样例

**问题：** Dorm Mock和错误样例缺少503 PROVIDER_UNAVAILABLE场景。

**修复：**
- 在contract-v0.1.md Section 6.2添加503错误样例
- 样例内容：
```json
{
  "error": {
    "code": "PROVIDER_UNAVAILABLE",
    "message": "宿舍清退服务暂时不可用，请稍后重试",
    "details": {
      "student_id": "2020503",
      "provider": "dorm_checkout",
      "error": "Connection timeout"
    }
  }
}
```

**文件：** docs/contracts/contract-v0.1.md（Section 6.2新增503样例）

---

### 修复3：澄清登录响应DTO

**问题：** 登录响应返回部分UserDTO（只有user_id/name/role/class_id），未说明是完整DTO还是子集。

**修复：**
- 在contract-v0.1.md Section 4.1 POST /api/auth/login添加说明
- 说明内容：
> **说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。

**文件：** docs/contracts/contract-v0.1.md（Section 4.1新增说明）

---

### 修复4：移除矛盾的降级条件

**问题：** 风险表中"申请提交API未完成 → 只做查询API"与纵向切片目标矛盾（无法先查询后提交）。

**修复：**
- 修改week-0-1-execution-plan.md风险2降级方案：
  - 原：只做查询API，Day 4补申请提交
  - 新：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
- 同步修改Day 3-4降级条件，移除"列表API"引用（已从契约删除）

**文件：** docs/plans/week-0-1-execution-plan.md（风险2和Day 3-4降级条件已修改）

---

## 审查请求

请Codex批判性审查以下内容：

### 1. 修复完整性
- [ ] 4个修复是否完全解决了上一轮指出的问题？
- [ ] 是否有遗漏的修复点？

### 2. API端点统一性
- [ ] 契约和计划的API端点数量现在是否一致？
- [ ] 移除列表端点的决策是否合理？
- [ ] 5个HTTP路由是否足以支撑最小纵向切片？

### 3. 错误样例完整性
- [ ] 503样例是否覆盖了PROVIDER_UNAVAILABLE场景？
- [ ] 错误样例是否覆盖了所有Section 3定义的错误码？

### 4. DTO一致性
- [ ] AuthUserDTO说明是否清晰？
- [ ] 是否需要在Section 1添加AuthUserDTO的正式定义？

### 5. 降级条件合理性
- [ ] 新的降级条件是否保持了纵向切片完整性？
- [ ] 降级条件是否现实可行？

### 6. 可执行性评估
- [ ] 契约现在是否达到"可执行契约"标准？
- [ ] 是否可以冻结契约并开始Week 1 Day 1工作？
- [ ] 如果还有问题，优先级如何排序？

---

## 期望输出

1. **修复验证：** 逐项确认4个修复是否解决了问题
2. **剩余问题：** 如果还有问题，列出具体问题和修复建议
3. **可执行性判断：** 明确回答"是否达到可执行契约标准"
4. **下一步建议：** 如果达标，建议冻结契约；如果未达标，建议优先修复哪些点

---

**请求人：** Claude Opus 4.7  
**审查协议：** docs/codex-review-protocol.md  
**相关文档：**
- docs/contracts/contract-v0.1.md（已修改）
- docs/plans/week-0-1-execution-plan.md（已修改）
- docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md（上一轮共识）

exec
/bin/bash -lc "rtk tail -n 20 .omc/collaboration/events.jsonl && rtk sed -n '1,220p' .omc/collaboration/state.json" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{"id":1,"type":"codex_ready","agent":"codex","timestamp":"2026-05-30T07:57:25.000Z","summary":"Codex collaboration configuration completed and ready for Claude-Codex workflow.","artifacts":["AGENTS.md",".omc/collaboration/protocol.md",".omc/collaboration/codex-ready.md"],"status":"codex_ready"}
{"id":2,"type":"task_created","agent":"claude","timestamp":"2026-05-30T08:04:10.000Z","summary":"Created protocol critical review task for Codex.","task_id":"TASK-20260530-01","artifacts":[".omc/collaboration/tasks/TASK-20260530-01-protocol-critical-review.md"],"status":"task_open"}
{"id":3,"type":"task_claimed","agent":"codex","timestamp":"2026-05-30T08:05:20.000Z","summary":"Codex claimed protocol critical review task.","task_id":"TASK-20260530-01","status":"in_progress"}
{"id":4,"type":"completed","agent":"codex","timestamp":"2026-05-30T08:05:20.000Z","summary":"Completed critical review of collaboration protocol and wrote review artifact.","task_id":"TASK-20260530-01","artifacts":[".omc/collaboration/artifacts/20260530-0805-codex-protocol-critical-review.md"],"status":"completed"}
{
  "workflow_id": "claude-codex-collab-mvp",
  "current_task": "TASK-20260530-01",
  "active_agent": "none",
  "status": "completed",
  "last_event_id": 4,
  "updated_at": "2026-05-30T08:05:20.000Z"
}

codex
我已经看到了 47 号文档的 4 个修复声明。现在需要核对实际文件内容，而不是只看声明，同时回到 46 号共识确认上一轮问题边界。
exec
/bin/bash -lc "rtk sed -n '1,320p' docs/contracts/contract-v0.1.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 数据契约 v0.1 - 最小可执行契约

**版本：** v0.1  
**冻结日期：** 2026-05-30  
**适用范围：** Week 1纵向切片  
**下一版本：** v0.2（Week 3）

---

## 1. 核心DTO

### 1.1 UserDTO

```python
@dataclass
class UserDTO:
    """用户数据传输对象"""
    user_id: str                      # 学号/工号
    name: str                         # 姓名
    role: UserRole                    # 角色：student/counselor/dean
    active: bool                      # 账号是否激活
    class_id: Optional[str] = None    # 班级ID（学生必填，教师为None）
    is_graduating: Optional[bool] = None  # 是否毕业生（仅学生）
    graduation_year: Optional[int] = None # 毕业年份（仅学生）
```

### 1.2 ApplicationDTO

```python
@dataclass
class ApplicationDTO:
    """离校申请数据传输对象"""
    application_id: str
    student_id: str
    student_name: str
    class_id: str
    reason: str                      # 申请理由
    leave_date: str                  # 计划离校日期 (YYYY-MM-DD)
    status: ApplicationStatus
    dorm_checkout_status: DormCheckoutStatus
    created_at: str                  # ISO8601
    updated_at: str
```

### 1.3 ApprovalDTO

```python
@dataclass
class ApprovalDTO:
    """审批记录数据传输对象"""
    approval_id: str
    application_id: str
    step: ApprovalStep           # counselor/dean
    approver_id: str
    approver_name: str
    decision: ApprovalDecision   # approved/rejected/pending
    comment: Optional[str]
    decided_at: Optional[str]    # ISO8601
```

### 1.4 DormCheckoutStatusDTO

```python
@dataclass
class DormCheckoutStatusDTO:
    """宿舍清退状态数据传输对象"""
    student_id: str
    status: DormCheckoutStatus   # completed/pending/not_started/unknown
    checked_at: Optional[str]    # ISO8601
    blocking_reason: Optional[str]
    provider_error_code: Optional[str]
```

---

## 2. 状态枚举

### 2.1 UserRole

```python
class UserRole(str, Enum):
    STUDENT = "student"
    COUNSELOR = "counselor"
    DEAN = "dean"
```

### 2.2 ApplicationStatus

```python
class ApplicationStatus(str, Enum):
    DRAFT = "draft"                      # 草稿
    PENDING_COUNSELOR = "pending_counselor"  # 待辅导员审批
    PENDING_DEAN = "pending_dean"        # 待学工部审批
    APPROVED = "approved"                # 已通过
    REJECTED = "rejected"                # 已驳回
```

### 2.3 ApprovalStep

```python
class ApprovalStep(str, Enum):
    COUNSELOR = "counselor"
    DEAN = "dean"
```

### 2.4 ApprovalDecision

```python
class ApprovalDecision(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
```

### 2.5 DormCheckoutStatus

```python
class DormCheckoutStatus(str, Enum):
    COMPLETED = "completed"          # 已清退
    PENDING = "pending"              # 清退中
    NOT_STARTED = "not_started"      # 未开始
    UNKNOWN = "unknown"              # 状态未知（API失败）
```

### 2.6 状态机契约

**申请状态流转规则：**

| 当前状态 | 触发动作 | 角色 | 下一状态 | 副作用 |
|---------|---------|------|---------|--------|
| - | 学生提交申请 | student | pending_counselor | 创建辅导员审批记录 |
| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
| pending_counselor | 辅导员驳回 | counselor | rejected | 无 |
| pending_dean | 学工部通过 | dean | approved | 无 |
| pending_dean | 学工部驳回 | dean | rejected | 无 |

**宿舍清退状态处理规则：**

| 宿舍状态 | 提交申请行为 | HTTP状态 | 错误码 |
|---------|------------|---------|--------|
| completed | 允许提交 | 201 | - |
| pending | 阻断提交 | 422 | DORM_BLOCKED |
| not_started | 阻断提交 | 422 | DORM_BLOCKED |
| unknown | 阻断提交 | 422 | DORM_BLOCKED |
| provider_unavailable | 阻断提交 | 503 | PROVIDER_UNAVAILABLE |

**角色权限矩阵：**

| 操作 | student | counselor | dean |
|------|---------|-----------|------|
| 提交申请 | ✓（仅自己） | ✗ | ✗ |
| 查看申请 | ✓（仅自己） | ✓（本班级） | ✓（所有） |
| 辅导员审批 | ✗ | ✓（本班级） | ✗ |
| 学工部审批 | ✗ | ✗ | ✓（所有） |

---

## 3. 错误码

### 3.1 业务错误 (4xx)

| 错误码 | HTTP状态 | 说明 | 示例场景 |
|--------|---------|------|---------|
| VALIDATION_ERROR | 400 | 请求参数校验失败 | 必填字段缺失、格式错误 |
| AUTH_REQUIRED | 401 | 未认证 | Token缺失或过期 |
| FORBIDDEN | 403 | 无权限 | 学生访问他人申请 |
| NOT_FOUND | 404 | 资源不存在 | 申请ID不存在 |
| CONFLICT | 409 | 资源冲突 | 重复提交申请 |
| DORM_BLOCKED | 422 | 宿舍清退未完成 | 提交申请时宿舍未清退 |

### 3.2 系统错误 (5xx)

| 错误码 | HTTP状态 | 说明 | 示例场景 |
|--------|---------|------|---------|
| PROVIDER_UNAVAILABLE | 503 | 外部服务不可用 | 宿舍清退API超时 |
| INTERNAL_ERROR | 500 | 内部错误 | 数据库连接失败 |

### 3.3 错误响应格式

```json
{
  "error": {
    "code": "DORM_BLOCKED",
    "message": "宿舍清退未完成，无法提交申请",
    "details": {
      "student_id": "2020001",
      "dorm_status": "pending"
    }
  }
}
```

---

## 4. API端点

### 4.1 认证

#### POST /api/auth/login

**请求：**
```json
{
  "user_id": "2020001",
  "password": "password123"
}
```

**响应：**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "user": {
    "user_id": "2020001",
    "name": "张三",
    "role": "student",
    "class_id": "CS2020-01"
  }
}
```

**说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。

### 4.2 申请

#### POST /api/applications

**请求：**
```json
{
  "reason": "毕业离校",
  "leave_date": "2024-06-30"
}
```

**响应：**
```json
{
  "application_id": "app_001",
  "student_id": "2020001",
  "student_name": "张三",
  "class_id": "CS2020-01",
  "reason": "毕业离校",
  "leave_date": "2024-06-30",
  "status": "pending_counselor",
  "dorm_checkout_status": "completed",
  "created_at": "2024-05-30T10:00:00Z",
  "updated_at": "2024-05-30T10:00:00Z"
}
```

#### GET /api/applications/{application_id}

**响应：**
```json
{
  "application_id": "app_001",
  "student_id": "2020001",
  "student_name": "张三",
  "class_id": "CS2020-01",
  "reason": "毕业离校",
  "leave_date": "2024-06-30",
  "status": "pending_counselor",
  "dorm_checkout_status": "completed",
  "approvals": [
    {
      "approval_id": "apv_001",
      "step": "counselor",
      "approver_id": "T001",
      "approver_name": "李老师",
      "decision": "pending",
      "comment": null,
      "decided_at": null
    }
  ],
  "created_at": "2024-05-30T10:00:00Z",
  "updated_at": "2024-05-30T10:00:00Z"
}
```

### 4.3 审批

#### POST /api/approvals/{approval_id}/approve

**请求：**
```json
{
  "comment": "同意离校"
}
```

**响应：**
```json
{
  "approval_id": "apv_001",
  "application_id": "app_001",
  "step": "counselor",
  "approver_id": "T001",
  "approver_name": "李老师",
  "decision": "approved",
  "comment": "同意离校",
  "decided_at": "2024-05-30T11:00:00Z"
}
```

#### POST /api/approvals/{approval_id}/reject

**请求：**
```json
{
  "comment": "材料不齐全"
}
```

**响应：**
```json
{
  "approval_id": "apv_001",
  "application_id": "app_001",

exec
/bin/bash -lc "rtk sed -n '1,340p' docs/plans/week-0-1-execution-plan.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Week 0-1 执行计划

**版本：** v1.0  
**创建日期：** 2026-05-30  
**团队规模：** 2-3人  
**总工期：** 6-7个工作日

---

## Week 0：契约冻结（1-2工作日）

### 目标
冻结v0.1最小可执行契约，为Week 1纵向切片提供稳定基础。

### Day 0（0.5天）

**任务：**
- [x] 定义核心DTO（User、Application、Approval、DormCheckoutStatus）
- [x] 定义状态枚举（5个枚举类型）
- [x] 定义错误码（8个核心错误码）

**责任人：** 后端负责人

**交付物：** contract-v0.1.md初稿

### Day 1（0.5-1天）

**任务：**
- [ ] 创建样例请求/响应（5个核心API端点）
  - POST /api/auth/login
  - POST /api/applications
  - GET /api/applications/{id}
  - POST /api/approvals/{id}/approve
  - POST /api/approvals/{id}/reject
- [ ] 创建Mock响应（宿舍清退Mock + 错误Mock）
- [ ] 生成seed数据（10学生 + 2辅导员 + 1学工部 + 边界样本 + 默认密码）
- [ ] 前端review可消费性
- [ ] 业务方确认业务假设

**责任人：** 后端负责人 + 前端负责人

**交付物：** contract-v0.1.md冻结版

**验收标准：**
- [ ] 前端可用mock跑通登录→提交→审批→查询流程
- [ ] 样例数据包含至少4个边界样本

**降级条件：**
- 如Day 1结束未完成前端review → 冻结当前版本，Week 1开始后异步review

---

## Week 1：后端纵向切片（5工作日）

### 目标
交付可运行的后端最小闭环：薄认证 + 申请提交 + 两级审批 + 状态查询 + Dorm Mock。

### Day 1-2：可运行骨架

**任务：**
- [ ] Django项目初始化（settings分层、数据库配置）
- [ ] 基础模型迁移（User、Application、Approval）
- [ ] Seed命令实现（加载contract-v0.1.md中的样例数据）
- [ ] 薄认证实现（学号/工号 + 密码，JWT）

**责任人：** 后端负责人

**交付物：**
- Django项目可运行
- `python manage.py seed_users` 可用
- POST /api/auth/login 可用

**验收标准：**
- [ ] `python manage.py runserver` 启动成功
- [ ] Seed数据加载成功（10学生 + 2辅导员 + 1学工部）
- [ ] 登录API返回JWT token

**降级条件：**
- 如Day 2结束seed命令未完成 → 手动插入测试数据，Week 2补seed命令

### Day 3-4：最小流程

**任务：**
- [ ] 申请提交API（POST /api/applications）
  - 最小角色校验：只有学生可提交
  - Dorm Mock集成：检查宿舍清退状态
  - 状态初始化：pending_counselor
  - 创建辅导员审批记录
- [ ] 辅导员审批API（POST /api/approvals/{id}/approve|reject）
  - 最小角色校验：只有对应班级辅导员可审批
  - 状态流转：pending_counselor → pending_dean（通过）或 rejected（驳回）
  - 创建学工部审批记录（通过时）
- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
  - 最小角色校验：只有学工部可审批
  - 状态流转：pending_dean → approved（通过）或 rejected（驳回）
- [ ] 状态查询API（GET /api/applications/{id}）
  - 最小角色校验：学生只能查自己，辅导员/学工部可查所有

**责任人：** 后端负责人

**交付物：**
- 4个API端点可用
- 最小角色校验实现

**验收标准：**
- [ ] 学生可提交申请
- [ ] 辅导员可审批（通过/驳回）
- [ ] 学工部可审批（通过/驳回）
- [ ] 状态查询返回完整申请信息和审批记录
- [ ] 角色校验生效（学生不能审批，辅导员不能跨班级审批）

**降级条件：**
- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批
- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环

### Day 5：验收硬化

**任务：**
- [ ] 端到端自动化测试
  - 测试1：学生登录 → 提交申请 → 辅导员审批通过 → 学工部审批通过 → 查询状态
  - 测试2：学生登录 → 提交申请 → 辅导员审批驳回 → 查询状态
  - 测试3：宿舍清退未完成 → 提交申请失败（DORM_BLOCKED）
  - 测试4：角色校验（学生不能审批，辅导员不能跨班级审批）
- [ ] 契约测试（API响应格式符合contract-v0.1.md）
- [ ] 修复阻断bug
- [ ] 输出Week 2任务清单

**责任人：** 后端负责人 + QA

**交付物：**
- 4个自动化测试通过
- Week 2任务清单

**验收标准：**
- [ ] 所有测试通过
- [ ] 无P0/P1阻断bug
- [ ] Week 2任务清单明确

**降级条件：**
- 如Day 5结束仍有P0 bug → 推到Week 2 Day 1修复，或砍掉触发bug的边界场景

---

## 并行任务

### 前端准备（Week 1期间）

**任务：**
- [ ] 技术栈选型确认（微信小程序框架）
- [ ] 项目初始化
- [ ] Mock Server配置（基于contract-v0.1.md）
- [ ] API Client封装

**责任人：** 前端负责人

**时间：** Week 1 Day 1-5（与后端并行）

**交付物：**
- 微信小程序项目可运行
- Mock Server可用
- API Client可用

**验收标准：**
- [ ] 可用mock跑通登录→提交→审批→查询流程

---

## 风险和降级

### 风险1：Week 0契约定义延期

**概率：** 中  
**影响：** 高  
**缓解措施：** 1-2工作日timebox，超时冻结当前假设进入Week 1

### 风险2：Week 1 Day 3申请提交API未完成

**概率：** 中  
**影响：** 高  
**降级方案：** 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批

### 风险3：Week 1 Day 4学工部审批未完成

**概率：** 低  
**影响：** 中  
**降级方案：** 推到Week 2 Day 1，Week 1只验证辅导员审批

### 风险4：Week 1 Day 5测试未通过

**概率：** 中  
**影响：** 高  
**降级方案：** 周末加班修复，或Week 2 Day 1修复

---

## 验收检查清单

### Week 0验收

- [ ] contract-v0.1.md冻结
- [ ] 前端可用mock跑通完整流程
- [ ] 样例数据包含边界样本

### Week 1验收

- [ ] Django项目可运行
- [ ] Seed数据加载成功
- [ ] 4个API端点可用（登录、提交、审批、查询）
- [ ] 最小角色校验实现
- [ ] 4个自动化测试通过
- [ ] 无P0/P1阻断bug

---

## 下一步（Week 2）

**目标：** CSV导入v1

**任务：**
- Staging表设计
- 校验报告
- Upsert逻辑
- 软停用基础
- 导入审计基础

**工期：** 5工作日

---

**计划负责人：** Claude Opus 4.7  
**创建日期：** 2026-05-30  
**状态：** 已批准，可执行

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 下一步工作 - 最终共识

**文档编号：** 46  
**共识日期：** 2026-05-30  
**参与方：** Claude Opus 4.7, Codex (GPT-5.5)  
**讨论周期：** 41 → 42 → 43 → 44 → 45 → 46

---

## 一、共识结论

**采用纵向切片/MVP优先方法，Week 0-1拆分执行。**

经过两轮批判性讨论，达成以下核心共识：

1. **Week 0（1-2工作日）：** 冻结v0.1最小可执行契约
2. **Week 1（5工作日）：** 后端纵向切片（保留最小权限校验）
3. **Week 2：** CSV导入v1
4. **Week 3：** 核心流程补强 + v0.2契约
5. **Week 4-6：** 微信小程序并行开发
6. **Week 6-7：** 宿舍真实API或降级
7. **Week 8-9：** UAT和完善
8. **Week 10：** 验收演示（不新增功能）

---

## 二、核心决策

### 决策1：数据契约v0.1现在冻结（1-2工作日）

**范围：** 最小可执行契约（不是极简字段，也不是完整模型）

**包含内容：**
- OpenAPI/DTO草案
- 状态枚举
- 错误码
- 样例请求/响应
- Seed/fixture数据
- Mock响应
- Changelog机制

**责任边界：**
- 后端负责人owns契约包
- 前端负责人reviews可消费性
- 用户/业务方确认业务假设

**时间限制：** 1-2工作日完成，超时冻结当前假设进入Week 1

### 决策2：Week 1交付后端纵向切片

**必须保留：**
- 后端项目可运行
- Seed/fixture落库
- 薄认证（学号/工号+密码）
- **最小角色校验**（学生/辅导员/学工部边界）
- 申请提交API
- 辅导员审批API
- 学工部审批API
- 状态查询API
- Dorm Mock参与提交校验
- 端到端自动化测试

**推迟到Week 2+：**
- 完整CSV导入
- 附件上传/下载
- 通知推送
- 微信OAuth
- 完整RBAC
- 宿舍真实API
- 复杂审批流

**工作量：** 7-10人日（2-3人团队，5个工作日）

### 决策3：前端Week 4并行启动

**启动硬门槛：**
1. 单端范围确认（只做微信小程序）
2. OpenAPI/DTO达到v0.2（有changelog）
3. 前端mock server可用
4. 核心后端API可跑通
5. 认证策略固定（演示期学号/工号密码）
6. 状态枚举和错误码稳定
7. 至少一条端到端后端测试通过
8. API owner明确，破坏性变更当天通知

**不应阻塞启动：**
- 附件完整权限
- 通知推送
- 宿舍真实API
- 微信OAuth真实接入
- 完整CSV导入后台

### 决策4：单端交付（微信小程序优先）

**首版范围：**
- 微信小程序（覆盖主要用户群）
- 核心流程（申请、审批、状态查询）
- Mock数据（seed + fixture）
- 简化认证（学号+密码，无微信OAuth）
- 简化附件（只支持图片上传）
- 简化通知（邮件通知，无微信推送）

**后续迭代：**
- React Native（如有需求）
- 微信OAuth
- 完整附件支持
- 微信模板消息

---

## 三、最终执行计划

| 时间 | 目标 | 交付物 | 验收标准 |
|------|------|--------|---------|
| **Week 0** (1-2工作日) | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog | 前端可用mock跑通登录→提交→审批→查询流程 |
| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
| **Week 2** | CSV导入v1 | Staging表、校验报告、upsert、软停用基础、导入审计基础 | 可导入10学生+2辅导员，生成校验报告，软停用未导入账号 |
| **Week 3** | 核心流程补强 + v0.2契约 | 权限细化、异常流、API mock更新、前端启动检查 | v0.2契约冻结，前端mock可用，核心API稳定 |
| **Week 4-6** | 微信小程序并行开发 | 登录、申请、审批、查询主流程 | 小程序可用mock跑通完整流程，逐步联调真实后端 |
| **Week 6-7** | 宿舍真实API或降级方案 | 真实Provider、错误分类、缓存/降级、人工证明路径 | 真实API集成或降级方案可用 |
| **Week 8-9** | UAT和完善 | 通知、附件最小可用、异常流修复、导入演练 | UAT通过，主要缺陷修复 |
| **Week 10** | 验收演示 | 演示脚本、缺陷修复、文档 | 可演示版本交付，不新增功能 |

---

## 四、立即行动

### 行动1：创建contract-v0.1.md

**文件路径：** `docs/contracts/contract-v0.1.md`

**责任人：** Claude（后端负责人）

**时间限制：** 1-2工作日

**验收标准：** 前端可用mock跑通登录→提交→审批→查询流程

### 行动2：创建week-0-1-execution-plan.md

**文件路径：** `docs/plans/week-0-1-execution-plan.md`

**责任人：** Claude（项目负责人）

**时间限制：** 与contract-v0.1.md同步完成

**验收标准：** 按天列出责任人、交付物、降级条件和验收测试

### 行动3：更新总实施计划

**时机：** Week 0-1执行计划完成后

**内容：** 基于Week 0-1执行计划更新10周总实施计划

---

## 五、关键修正点

### 修正1：从瀑布式到纵向切片

**原方案A：** 认证→申请→审批→附件→通知→前端→联调

**修正后：** Week 1端到端最小流程 → Week 2-3扩展 → Week 4前端并行

**原因：** 避免Week 8-10才发现集成问题

### 修正2：从前端后置到并行开发

**原方案A：** Week 8-9前端，Week 10联调

**修正后：** Week 4前端启动，不等后端完全稳定

**原因：** 降低前端集成风险，提前发现问题

### 修正3：从双端到单端

**原方案A：** React Native + 微信小程序同时开发

**修正后：** 微信小程序优先，React Native后续迭代

**原因：** 2-3人10周无法同时交付双端

### 修正4：从Week 1数据契约到Week 0

**原方案A：** Week 1做数据契约和接口设计

**修正后：** Week 0（1-2工作日）冻结v0.1，Week 1用v0.1跑纵向切片

**原因：** 避免Week 1前半定义契约，后半只剩2-3天开发

### 修正5：保留最小权限校验

**Claude错误建议：** Week 1"审批API无权限校验"

**Codex修正：** 最小角色校验必须保留

**原因：** 纵向切片的价值是验证角色、数据、状态机和审批链路能否串起来

---

## 六、风险缓解

### 风险1：Week 0契约定义延期

**缓解措施：** 1-2工作日timebox，超时冻结当前假设进入Week 1

### 风险2：Week 1纵向切片未完成

**降级条件：**
- Day 3结束仍无申请提交API → 只保留"学生提交→辅导员审批→查询"
- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头

### 风险3：前端Week 4启动条件不满足

**应对策略：**
- 如果只是字段补充、错误码补充，不推迟
- 如果核心端点还没有可运行实现，前端做一周mock驱动开发，Week 5切真实环境
- 如果v0.2契约仍没有确定状态枚举、角色和核心路径，先用1-2天补契约

### 风险4：Week 10过载

**缓解措施：** Week 10只做验收和演示，前面延期的任务砍掉或推迟到生产集成阶段

---

## 七、讨论总结

### 讨论轮次

**第一轮（文档41-42）：**
- Claude提出方案A
- Codex批判：瀑布式排期、前端后置、Week 10过载
- Codex建议：纵向切片、前端并行、砍范围

**第二轮（文档43-44）：**
- Claude质疑：v0.1何时冻结、Week 1工作量、前端启动条件
- Codex澄清：v0.1现在冻结、7-10人日现实、Week 4启动不要求后端完全稳定
- Codex指出Claude方案问题：Week 0膨胀、v0.1过于字段化、Week 1砍权限校验

**第三轮（文档45-46）：**
- Claude完全接受Codex修正
- 达成共识：Week 0-1拆分、v0.1最小可执行契约、保留最小权限校验、前端Week 4并行

### 核心教训

1. **纵向切片优于横向模块堆叠** - 早期验证端到端集成
2. **前端并行优于前端后置** - 降低集成风险
3. **单端优于双端** - 资源有限时聚焦核心
4. **数据契约提前冻结** - 避免Week 1前半定义后半开发
5. **最小权限校验不能砍** - 纵向切片的价值在于验证完整链路

---

## 八、后续讨论点（非阻塞）

- CSV导入v1的详细设计（Week 2开始前）
- 微信小程序技术栈选择（Week 3开始前）
- 宿舍真实API集成方案（Week 5开始前）

---


codex
初步核对到一个需要进一步确认的点：计划里仍有“4个API端点可用”的口径，可能是在把两个审批动作合并成一个业务端点计数。我要继续看契约后半部分和全文端点引用，避免把术语问题误判成阻塞问题。
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Contract Fixes Summary

**日期：** 2026-05-30  
**执行人：** Claude Opus 4.7  
**文档编号：** 48

---

## 修复完成情况

基于上一轮Codex审查（文档46）指出的3-4个问题，已完成全部修复：

### ✅ 修复1：统一API端点数量（主要阻塞点）

**修改文件：** docs/contracts/contract-v0.1.md

**修改内容：**
- 删除Section 4.4 GET /api/applications（列表端点）
- 统一为5个HTTP路由

**验证：**
- Contract Section 4现在有5个端点
- Week 0 Day 1说"5个核心API端点"（一致）
- Week 1 Day 3-4交付物需要更新为"5个API端点"（待验证）

---

### ✅ 修复2：添加503样例

**修改文件：** docs/contracts/contract-v0.1.md

**修改内容：**
- Section 6.2新增503 PROVIDER_UNAVAILABLE错误样例
- 样例student_id: 2020503

**验证：**
- 错误样例现在覆盖：401, 403, 422, 503

---

### ✅ 修复3：澄清登录响应DTO

**修改文件：** docs/contracts/contract-v0.1.md

**修改内容：**
- Section 4.1 POST /api/auth/login添加说明
- 明确响应user对象为AuthUserDTO（UserDTO子集）

**验证：**
- 说明已添加，清晰说明字段范围

---

### ✅ 修复4：移除矛盾降级条件

**修改文件：** docs/plans/week-0-1-execution-plan.md

**修改内容：**
- 风险2降级方案：改为"保留提交→辅导员审批→查询闭环，砍学工部审批"
- Day 3-4降级条件：移除"列表API"引用

**验证：**
- 降级条件现在保持纵向切片完整性
- 不再有"只做查询API"的矛盾逻辑

---

## 待验证项

1. **Week 1 Day 3-4交付物：** 需要确认是否应该从"4个API端点"改为"5个API端点"（包含login）
2. **Codex审查：** 需要Codex确认修复是否达到"可执行契约"标准
3. **契约冻结：** 如果Codex确认达标，可以冻结contract-v0.1.md

---

## 下一步

**如果Codex确认达标：**
1. 冻结contract-v0.1.md（标记为v0.1 Final）
2. 更新PROJECT-SUMMARY.md记录修复
3. 更新.omc/session-context.json
4. 开始Week 1 Day 1工作（Django骨架、模型、seed、认证）

**如果Codex指出剩余问题：**
1. 按优先级修复剩余问题
2. 再次请求Codex审查
3. 直到达到"可执行契约"标准

---

**创建时间：** 2026-05-30T08:03:03Z  
**状态：** 等待Codex审查确认

exec
/bin/bash -lc "rtk sed -n '220,520p' docs/contracts/contract-v0.1.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
}
```

**说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。

### 4.2 申请

#### POST /api/applications

**请求：**
```json
{
  "reason": "毕业离校",
  "leave_date": "2024-06-30"
}
```

**响应：**
```json
{
  "application_id": "app_001",
  "student_id": "2020001",
  "student_name": "张三",
  "class_id": "CS2020-01",
  "reason": "毕业离校",
  "leave_date": "2024-06-30",
  "status": "pending_counselor",
  "dorm_checkout_status": "completed",
  "created_at": "2024-05-30T10:00:00Z",
  "updated_at": "2024-05-30T10:00:00Z"
}
```

#### GET /api/applications/{application_id}

**响应：**
```json
{
  "application_id": "app_001",
  "student_id": "2020001",
  "student_name": "张三",
  "class_id": "CS2020-01",
  "reason": "毕业离校",
  "leave_date": "2024-06-30",
  "status": "pending_counselor",
  "dorm_checkout_status": "completed",
  "approvals": [
    {
      "approval_id": "apv_001",
      "step": "counselor",
      "approver_id": "T001",
      "approver_name": "李老师",
      "decision": "pending",
      "comment": null,
      "decided_at": null
    }
  ],
  "created_at": "2024-05-30T10:00:00Z",
  "updated_at": "2024-05-30T10:00:00Z"
}
```

### 4.3 审批

#### POST /api/approvals/{approval_id}/approve

**请求：**
```json
{
  "comment": "同意离校"
}
```

**响应：**
```json
{
  "approval_id": "apv_001",
  "application_id": "app_001",
  "step": "counselor",
  "approver_id": "T001",
  "approver_name": "李老师",
  "decision": "approved",
  "comment": "同意离校",
  "decided_at": "2024-05-30T11:00:00Z"
}
```

#### POST /api/approvals/{approval_id}/reject

**请求：**
```json
{
  "comment": "材料不齐全"
}
```

**响应：**
```json
{
  "approval_id": "apv_001",
  "application_id": "app_001",
  "step": "counselor",
  "approver_id": "T001",
  "approver_name": "李老师",
  "decision": "rejected",
  "comment": "材料不齐全",
  "decided_at": "2024-05-30T11:00:00Z"
}
```

---

## 5. 样例数据

### 5.1 正常样本

**默认密码：** 所有账号默认密码为 `password123`

**学生（10人）：**
```python
students = [
    {"user_id": "2020001", "name": "张三", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020002", "name": "李四", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020003", "name": "王五", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020004", "name": "赵六", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020005", "name": "钱七", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020006", "name": "孙八", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020007", "name": "周九", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020008", "name": "吴十", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020009", "name": "郑十一", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
    {"user_id": "2020010", "name": "王十二", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
]
```

**辅导员（2人）：**
```python
counselors = [
    {"user_id": "T001", "name": "李老师", "role": "counselor", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
    {"user_id": "T002", "name": "王老师", "role": "counselor", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
]
```

**学工部（1人）：**
```python
deans = [
    {"user_id": "D001", "name": "赵主任", "role": "dean", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
]
```

**班级映射：**
```python
class_mappings = [
    {"class_id": "CS2020-01", "counselor_id": "T001"},
    {"class_id": "CS2020-02", "counselor_id": "T002"},
]
```

### 5.2 边界样本

**无班级映射：**
```python
{"user_id": "2020099", "name": "边界1", "role": "student", "class_id": "INVALID", "is_graduating": True, "graduation_year": 2024, "active": True}
```

**辅导员停用：**
```python
{"user_id": "T099", "name": "停用老师", "role": "counselor", "class_id": None, "active": False}
```

**非毕业生：**
```python
{"user_id": "2021001", "name": "边界2", "role": "student", "class_id": "CS2021-01", "is_graduating": False, "graduation_year": 2025, "active": True}
```

**延期毕业：**
```python
{"user_id": "2019001", "name": "边界3", "role": "student", "class_id": "CS2019-01", "is_graduating": True, "graduation_year": 2024, "active": True}
```

---

## 6. Mock响应

### 6.1 宿舍清退Mock

**DormCheckoutProvider Mock实现：**

```python
class MockDormCheckoutProvider:
    def check_status(self, student_id: str) -> DormCheckoutStatusDTO:
        # 固定返回规则（覆盖所有状态）
        mock_data = {
            "2020001": DormCheckoutStatusDTO(
                student_id="2020001",
                status=DormCheckoutStatus.COMPLETED,
                checked_at="2024-05-15T10:00:00Z",
                blocking_reason=None,
                provider_error_code=None
            ),
            "2020002": DormCheckoutStatusDTO(
                student_id="2020002",
                status=DormCheckoutStatus.PENDING,
                checked_at=None,
                blocking_reason="宿舍物品未清理",
                provider_error_code=None
            ),
            "2020003": DormCheckoutStatusDTO(
                student_id="2020003",
                status=DormCheckoutStatus.NOT_STARTED,
                checked_at=None,
                blocking_reason="未提交清退申请",
                provider_error_code=None
            ),
            "2020099": DormCheckoutStatusDTO(
                student_id="2020099",
                status=DormCheckoutStatus.UNKNOWN,
                checked_at=None,
                blocking_reason="学生信息不存在",
                provider_error_code="STUDENT_NOT_FOUND"
            ),
        }
        
        # 默认返回NOT_STARTED（而非completed，避免掩盖失败路径）
        return mock_data.get(student_id, DormCheckoutStatusDTO(
            student_id=student_id,
            status=DormCheckoutStatus.NOT_STARTED,
            checked_at=None,
            blocking_reason="未在宿舍系统中找到记录",
            provider_error_code=None
        ))
```

### 6.2 错误Mock

**401 Unauthorized：**
```json
{
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "Token缺失或过期"
  }
}
```

**403 Forbidden：**
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "无权限访问此资源"
  }
}
```

**422 Dorm Blocked：**
```json
{
  "error": {
    "code": "DORM_BLOCKED",
    "message": "宿舍清退未完成，无法提交申请",
    "details": {
      "student_id": "2020002",
      "dorm_status": "pending",
      "blocking_reason": "宿舍物品未清理"
    }
  }
}
```

**503 Provider Unavailable：**
```json
{
  "error": {
    "code": "PROVIDER_UNAVAILABLE",
    "message": "宿舍清退服务暂时不可用，请稍后重试",
    "details": {
      "student_id": "2020503",
      "provider": "dorm_checkout",
      "error": "Connection timeout"
    }
  }
}
```

---

## 7. 变更日志

### v0.1 (2026-05-30)

**初始版本 - 最小可执行契约**

**包含内容：**
- 核心DTO（User、Application、Approval、DormCheckoutStatus）
- 状态枚举（UserRole、ApplicationStatus、ApprovalStep、ApprovalDecision、DormCheckoutStatus）
- 错误码（8个核心错误码）
- API端点（认证、申请、审批、查询）
- 样例数据（正常样本 + 边界样本）
- Mock响应（宿舍清退Mock + 错误Mock）

**不包含内容（v0.2）：**

exec
/bin/bash -lc 'rtk rg -n "api/|API端点|端点|列表|applications|approvals|PROVIDER_UNAVAILABLE|DORM_BLOCKED|AuthUserDTO|错误码|降级|查询API" docs/contracts/contract-v0.1.md docs/plans/week-0-1-execution-plan.md docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:21:### 修复1：统一API端点数量（主要阻塞点）
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:23:**问题：** 契约列出6个HTTP路由，计划说"5个核心API端点"（Week 0 Day 1）和"4个API端点"（Week 1 Day 3-4），口径不一致。
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:26:- 从contract-v0.1.md移除Section 4.4 GET /api/applications（列表端点）
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:28:  1. POST /api/auth/login
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:29:  2. POST /api/applications
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:30:  3. GET /api/applications/{id}
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:31:  4. POST /api/approvals/{id}/approve
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:32:  5. POST /api/approvals/{id}/reject
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:34:**理由：** 列表端点不是最小纵向切片必需的，核心流程是"登录→提交→审批→查询单个申请"。
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:40:### 修复2：添加503 PROVIDER_UNAVAILABLE样例
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:42:**问题：** Dorm Mock和错误样例缺少503 PROVIDER_UNAVAILABLE场景。
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:50:    "code": "PROVIDER_UNAVAILABLE",
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:70:- 在contract-v0.1.md Section 4.1 POST /api/auth/login添加说明
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:72:> **说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:78:### 修复4：移除矛盾的降级条件
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:80:**问题：** 风险表中"申请提交API未完成 → 只做查询API"与纵向切片目标矛盾（无法先查询后提交）。
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:83:- 修改week-0-1-execution-plan.md风险2降级方案：
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:84:  - 原：只做查询API，Day 4补申请提交
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:86:- 同步修改Day 3-4降级条件，移除"列表API"引用（已从契约删除）
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:88:**文件：** docs/plans/week-0-1-execution-plan.md（风险2和Day 3-4降级条件已修改）
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:100:### 2. API端点统一性
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:101:- [ ] 契约和计划的API端点数量现在是否一致？
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:102:- [ ] 移除列表端点的决策是否合理？
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:106:- [ ] 503样例是否覆盖了PROVIDER_UNAVAILABLE场景？
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:107:- [ ] 错误样例是否覆盖了所有Section 3定义的错误码？
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:110:- [ ] AuthUserDTO说明是否清晰？
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:111:- [ ] 是否需要在Section 1添加AuthUserDTO的正式定义？
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:113:### 5. 降级条件合理性
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:114:- [ ] 新的降级条件是否保持了纵向切片完整性？
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:115:- [ ] 降级条件是否现实可行？
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:21:6. **Week 6-7：** 宿舍真实API或降级
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:36:- 错误码
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:59:- 状态查询API
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:82:6. 状态枚举和错误码稳定
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:115:| **Week 0** (1-2工作日) | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog | 前端可用mock跑通登录→提交→审批→查询流程 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:120:| **Week 6-7** | 宿舍真实API或降级方案 | 真实Provider、错误分类、缓存/降级、人工证明路径 | 真实API集成或降级方案可用 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:146:**验收标准：** 按天列出责任人、交付物、降级条件和验收测试
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:208:**降级条件：**
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:215:- 如果只是字段补充、错误码补充，不推迟
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:216:- 如果核心端点还没有可运行实现，前端做一周mock驱动开发，Week 5切真实环境
docs/contracts/contract-v0.1.md:139:| 宿舍状态 | 提交申请行为 | HTTP状态 | 错误码 |
docs/contracts/contract-v0.1.md:142:| pending | 阻断提交 | 422 | DORM_BLOCKED |
docs/contracts/contract-v0.1.md:143:| not_started | 阻断提交 | 422 | DORM_BLOCKED |
docs/contracts/contract-v0.1.md:144:| unknown | 阻断提交 | 422 | DORM_BLOCKED |
docs/contracts/contract-v0.1.md:145:| provider_unavailable | 阻断提交 | 503 | PROVIDER_UNAVAILABLE |
docs/contracts/contract-v0.1.md:158:## 3. 错误码
docs/contracts/contract-v0.1.md:162:| 错误码 | HTTP状态 | 说明 | 示例场景 |
docs/contracts/contract-v0.1.md:169:| DORM_BLOCKED | 422 | 宿舍清退未完成 | 提交申请时宿舍未清退 |
docs/contracts/contract-v0.1.md:173:| 错误码 | HTTP状态 | 说明 | 示例场景 |
docs/contracts/contract-v0.1.md:175:| PROVIDER_UNAVAILABLE | 503 | 外部服务不可用 | 宿舍清退API超时 |
docs/contracts/contract-v0.1.md:183:    "code": "DORM_BLOCKED",
docs/contracts/contract-v0.1.md:195:## 4. API端点
docs/contracts/contract-v0.1.md:199:#### POST /api/auth/login
docs/contracts/contract-v0.1.md:223:**说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。
docs/contracts/contract-v0.1.md:227:#### POST /api/applications
docs/contracts/contract-v0.1.md:253:#### GET /api/applications/{application_id}
docs/contracts/contract-v0.1.md:266:  "approvals": [
docs/contracts/contract-v0.1.md:284:#### POST /api/approvals/{approval_id}/approve
docs/contracts/contract-v0.1.md:307:#### POST /api/approvals/{approval_id}/reject
docs/contracts/contract-v0.1.md:478:    "code": "DORM_BLOCKED",
docs/contracts/contract-v0.1.md:493:    "code": "PROVIDER_UNAVAILABLE",
docs/contracts/contract-v0.1.md:515:- 错误码（8个核心错误码）
docs/contracts/contract-v0.1.md:516:- API端点（认证、申请、审批、查询）
docs/contracts/contract-v0.1.md:541:  rest.post('/api/auth/login', (req, res, ctx) => {
docs/contracts/contract-v0.1.md:553:  // ... 其他端点
docs/contracts/contract-v0.1.md:569:    response = client.post('/api/auth/login', {
docs/contracts/contract-v0.1.md:576:    response = client.post('/api/applications', 
docs/plans/week-0-1-execution-plan.md:20:- [x] 定义错误码（8个核心错误码）
docs/plans/week-0-1-execution-plan.md:29:- [ ] 创建样例请求/响应（5个核心API端点）
docs/plans/week-0-1-execution-plan.md:30:  - POST /api/auth/login
docs/plans/week-0-1-execution-plan.md:31:  - POST /api/applications
docs/plans/week-0-1-execution-plan.md:32:  - GET /api/applications/{id}
docs/plans/week-0-1-execution-plan.md:33:  - POST /api/approvals/{id}/approve
docs/plans/week-0-1-execution-plan.md:34:  - POST /api/approvals/{id}/reject
docs/plans/week-0-1-execution-plan.md:48:**降级条件：**
docs/plans/week-0-1-execution-plan.md:71:- POST /api/auth/login 可用
docs/plans/week-0-1-execution-plan.md:78:**降级条件：**
docs/plans/week-0-1-execution-plan.md:84:- [ ] 申请提交API（POST /api/applications）
docs/plans/week-0-1-execution-plan.md:89:- [ ] 辅导员审批API（POST /api/approvals/{id}/approve|reject）
docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
docs/plans/week-0-1-execution-plan.md:96:- [ ] 状态查询API（GET /api/applications/{id}）
docs/plans/week-0-1-execution-plan.md:102:- 4个API端点可用
docs/plans/week-0-1-execution-plan.md:112:**降级条件：**
docs/plans/week-0-1-execution-plan.md:122:  - 测试3：宿舍清退未完成 → 提交申请失败（DORM_BLOCKED）
docs/plans/week-0-1-execution-plan.md:139:**降级条件：**
docs/plans/week-0-1-execution-plan.md:168:## 风险和降级
docs/plans/week-0-1-execution-plan.md:180:**降级方案：** 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
docs/plans/week-0-1-execution-plan.md:186:**降级方案：** 推到Week 2 Day 1，Week 1只验证辅导员审批
docs/plans/week-0-1-execution-plan.md:192:**降级方案：** 周末加班修复，或Week 2 Day 1修复
docs/plans/week-0-1-execution-plan.md:208:- [ ] 4个API端点可用（登录、提交、审批、查询）

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 下一步工作批判性讨论 - Codex第二轮回应

**文档编号：** 44  
**响应日期：** 2026-05-30  
**响应人：** Codex  
**针对文档：** 43-next-steps-claude-response-round1.md  

---

## 总体结论

Claude的质疑是必要的，尤其是把"Week 0准备"和"Week 1纵向切片"拆开这一点，有助于避免把契约、数据、实现全塞进同一个5天窗口。

但Claude方案仍有几个危险倾向：

1. 把v0.1契约理解成"字段清单"，而不是可执行契约包。
2. 把前端启动条件抬得过高，可能再次滑回"后端稳定后再前端"的瀑布路径。
3. Week 1建议"审批API无权限校验"，会让纵向切片失去验证审批链路的意义。
4. Week 0如果没有明确时长和验收标准，很容易变成新的计划缓冲黑洞。

我的第二轮结论是：

**采用Week 0-1拆分，但Week 0必须是1-2个工作日的timebox；v0.1应现在冻结最小可执行契约，不等到Week 1前半；Week 1只承诺后端端到端最小闭环；前端Week 4启动不要求后端完全稳定，只要求契约、mock和核心路径达到可消费状态。**

---

## 一、数据契约v0.1：现在冻结还是Week 1前半？

### 结论

**应现在冻结v0.1，不应拖到Week 1前半。**

这里的"现在"不是指今天把完整未来模型一次性定死，而是指在正式Week 1编码前，用1-2个工作日完成一个可执行的v0.1基线：

- OpenAPI/接口草案
- DTO字段和枚举
- 样例请求/响应
- 样例CSV或seed fixture
- 错误码
- mock响应
- 契约变更记录

如果拖到Week 1前半才冻结，Week 1后半只剩2-3天，很难完成后端骨架、认证、申请、审批、状态查询和集成测试。Claude把这个拆法描述成"Week 1前半冻结，Week 1后半纵向切片"，本质上还是把Week 1压缩成半周开发，风险比Codex原建议更高。

### v0.1范围：不是"最小字段"，也不是"完整字段"

Claude给出的选项A和选项B都不够准确：

- 选项A过小：只有`student_id, name, application_id, status, approver_id`无法支撑班级映射、角色判断、审批层级、宿舍清退校验和错误处理。
- 选项B过大：把附件、通知、真实宿舍清退全部字段纳入v0.1，会拖慢Week 1并制造伪稳定。

建议采用**最小可执行契约**：

| 契约块 | v0.1必须包含 | v0.1不必完整包含 |
|---|---|---|
| 学生/用户 | student_id、name、role、class_id、is_graduating、graduation_year、active | 微信openid、手机号、完整个人档案 |
| 班级/辅导员 | class_id、counselor_id、counselor_active | 组织树、多辅导员复杂分配 |
| 申请 | application_id、student_id、reason、leave_date或checkout_intent、status、created_at | 完整表单扩展字段 |
| 审批 | step、approver_id、decision、comment、decided_at | 会签、转办、复杂委托 |
| 宿舍清退 | provider_status、checked_at、blocking_reason、provider_error_code | 真实接口全部响应字段 |
| 认证 | login_id、role、access_token mock/JWT格式 | 微信OAuth |
| 错误 | VALIDATION_ERROR、AUTH_REQUIRED、FORBIDDEN、NOT_FOUND、CONFLICT、DORM_BLOCKED、PROVIDER_UNAVAILABLE | 完整国际化错误文案 |
| CSV/seed | 正常样本 + 边界样本 | 完整生产导入模板 |

也就是说，v0.1的范围应是**能跑通纵向切片且为v0.2留扩展点**，不是"最小字段"和"完整模型"二选一。

### 谁来定义，样例数据从哪里来，mock由谁提供？

建议责任边界如下：

- 后端负责人 owns 契约包：OpenAPI/DTO/错误码/seed schema。
- 前端负责人 reviews 契约可消费性：字段命名、状态展示、错误展示、登录态。
- 用户或业务方只确认业务假设：角色、审批链路、宿舍清退是否阻断提交。
- 样例CSV/fixture先用合成数据，不等待真实样本；真实样本只用于v0.2/v1.0校准。
- 前端API mock由契约生成或从后端mock server导出，不能由前端手写一套与后端脱节的mock。

---

## 二、Week 1的7-10天工作量是否现实？

### 结论

**7-10人日现实，7-10日历天不现实。**

如果团队是2-3人，且Week 0已经完成v0.1契约，Week 1用5个工作日交付最小后端闭环是有机会的。但前提是严格砍范围，并且明确并行路径。

Claude的拆解把工作量估成7-10天，但没有区分人日和日历天。2名后端/全栈并行时，5个工作日约等于10人日；如果只有1名有效后端，这个目标就必须降级。

### Week 1应该保留什么

Week 1必须保留：

- 后端项目可运行
- seed/fixture落库
- 薄认证：学号/工号 + 密码或固定验证码
- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
- 申请提交API
- 辅导员审批API
- 学工部审批API
- 状态查询API
- Dorm Mock参与提交校验
- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询

这里需要反驳Claude的一点：**"审批API简化版，无权限校验"不应该进入Week 1目标。** 纵向切片的价值正是验证角色、数据、状态机和审批链路能否串起来。可以不做完整RBAC、组织树和复杂权限，但最小角色校验不能砍，否则Week 1只能证明CRUD能跑，不能证明毕业离校审批流程能跑。

### Week 1可以推迟什么

Week 1应推迟：

- 完整CSV staging、upsert、软停用、导入审计
- 附件上传/下载
- 通知推送
- 微信OAuth
- 完整RBAC权限矩阵
- 宿舍真实API
- 审批转办、撤回、驳回后重提等复杂流
- Postman集合可以有，但不应替代自动化端到端测试

### 调整后的Week 0-1安排

**Week 0 / Day 0-1：契约timebox**

- 冻结v0.1最小可执行契约
- 生成10-20条seed + 边界fixture
- 确认审批链路和状态枚举
- 输出mock响应和错误码

**Week 1 / Day 1-2：可运行骨架**

- Django/API项目启动
- 基础模型迁移
- seed命令
- 薄认证

**Week 1 / Day 3-4：最小流程**

- 申请提交
- 两级审批
- 状态查询
- Dorm Mock阻断/放行

**Week 1 / Day 5：验收硬化**

- 端到端测试
- 契约测试
- 修复阻断bug
- 输出Week 2任务清单

如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。

---

## 三、前端Week 4并行的前提条件是什么？

### 结论

**Week 4前端可以启动，但启动条件不应是"后端API完全稳定"。**

Claude列出的前提条件里，"核心流程后端API已实现"和"认证机制已确定"是对的；但"API契约稳定至少v0.2"如果理解成后端字段不再变化，就太重了。前端并行开发需要的是可消费契约，不是生产级冻结。

### Week 4启动的硬门槛

Week 4开始微信小程序主流程开发前，必须满足：

1. 单端范围已确认：首版只做微信小程序，不并行React Native。
2. OpenAPI/DTO达到v0.2，破坏性变更需要changelog。
3. 前端mock server或mock JSON可用，覆盖登录、提交、审批、查询、错误态。
4. 核心后端API在开发环境可跑通：登录、提交、审批、查询。
5. 认证策略固定为"演示期学号/工号密码，微信OAuth后置"，前端只封装token机制，不等待OAuth。
6. 状态枚举和错误码稳定，前端能做状态页和错误提示。
7. 至少有一条端到端后端测试通过，证明mock不是孤立样例。
8. API owner明确，接口破坏性变更需要当天通知并更新mock。

### 不应作为Week 4启动门槛的事项

以下事项不应阻塞前端启动：

- 附件完整权限
- 通知推送
- 宿舍真实API
- 微信OAuth真实接入
- 完整CSV导入后台
- 性能指标
- 完整生产权限矩阵

如果Week 3后端API还不稳定，是否推迟到Week 5？我的判断是：

- 如果只是字段补充、错误码补充、非破坏性变化，不推迟。
- 如果登录、提交、审批、查询四个核心端点还没有可运行实现，前端仍可做一周mock驱动开发，但Week 5必须切到真实开发环境联调。
- 如果v0.2契约仍没有确定状态枚举、角色和核心路径，则不能启动页面开发，应先用1-2天补契约，否则前端会做成静态原型。

---

## 四、Claude的Week 0-1拆分方案是否可行？

### 可行的部分

Claude提出的拆分方向可行：

- Week 0做契约和fixture
- Week 1做纵向切片
- Week 1不做附件、通知、微信OAuth
- Week 10只验收和修复

这比文档40的"Week 1只做数据契约、Week 8-9才做前端"更好。

### 需要修正的问题

**问题1：Week 0不能是2-3天的开放准备期。**

如果Week 0花3天定义契约，再Week 1花5天做切片，总体变成8个工作日。不是不可以，但这应被明确计入计划，而不是把"现在"当免费缓冲。建议Week 0限制为1-2个工作日，超过就冻结当前假设继续做，后续进入v0.2。

**问题2：v0.1不能只定义DTO。**

Claude的Week 0列了StudentDTO、ApplicationDTO、ApprovalDTO，但缺少错误码、状态机、样例请求响应、mock、契约测试和变更规则。前端和测试真正依赖的是这些可执行产物，不只是字段名。

**问题3：Week 1"无权限校验"会削弱纵向切片。**

最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。

**问题4：前端启动时间在文档内不一致。**

Claude前面说"前端Week 4并行"，后面修正建议又写"Week 2：CSV导入 + 前端开始"。这两个说法需要统一。我的建议是：Week 2可以开始前端技术预研和API client封装，但微信小程序主流程页面开发以Week 4为正式启动点。

**问题5：CSV导入仍可能挤压Week 2。**

Claude建议Week 2做CSV导入并让前端开始，但CSV staging、校验报告、upsert、软停用、审计日志本身就是一周以上风险项。Week 2的目标应定义为"CSV导入v1可用"，前端只做轻量准备；不要让Week 2同时承诺完整导入和主流程前端。

**问题6：Postman集合不是足够验收标准。**

Week 1可以交Postman集合，但必须有自动化端到端测试。否则每次契约变化都靠人工点接口，后续Week 2-4会快速失控。

---

## 五、建议形成第二轮共识

建议将执行计划修正为：

| 时间 | 目标 | 交付物 |
|---|---|---|
| Week 0 / 1-2工作日 | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog |
| Week 1 | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 |
| Week 2 | CSV导入v1 | staging、校验报告、upsert、软停用基础、导入审计基础 |
| Week 3 | 核心流程补强 + v0.2契约 | 权限细化、异常流、API mock更新、前端启动检查 |
| Week 4-6 | 微信小程序并行开发 | 登录、申请、审批、查询主流程，使用mock并逐步联调真实后端 |
| Week 6-7 | 宿舍真实API或降级方案 | 真实Provider、错误分类、缓存/降级、人工证明路径 |
| Week 8-9 | UAT和完善 | 通知、附件最小可用、异常流修复、导入演练 |
| Week 10 | 验收演示 | 演示脚本、缺陷修复、文档，不新增功能 |

---

## 直接回答Claude的4个问题

1. **数据契约v0.1应该现在冻结还是Week 1前半？范围最小还是完整？**  
   现在冻结，限制在1-2个工作日内完成。范围是"最小可执行契约"，不是极简字段，也不是完整未来模型。

2. **Week 1的7-10天工作量是否现实？如何调整？**  
   如果指7-10人日，在2-3人团队下现实；如果指7-10日历天，不现实。调整方式是Week 0先完成契约，Week 1只做后端最小闭环，推迟CSV完整导入、附件、通知、微信OAuth、真实宿舍API。

3. **前端Week 4并行的前提条件是什么？**  

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '520,640p' docs/contracts/contract-v0.1.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 161ms:
 succeeded in 183ms:
codex
现在结论趋向于“基本达标，但还有少量 P1/P2 文档口径问题”。我会补充行号证据，然后把审查结果按项目流程落成 49 号响应文档。
exec
/bin/bash -lc 'rtk nl -ba docs/plans/week-0-1-execution-plan.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# Week 0-1 执行计划
     2	
     3	**版本：** v1.0  
     4	**创建日期：** 2026-05-30  
     5	**团队规模：** 2-3人  
     6	**总工期：** 6-7个工作日
     7	
     8	---
     9	
    10	## Week 0：契约冻结（1-2工作日）
    11	
    12	### 目标
    13	冻结v0.1最小可执行契约，为Week 1纵向切片提供稳定基础。
    14	
    15	### Day 0（0.5天）
    16	
    17	**任务：**
    18	- [x] 定义核心DTO（User、Application、Approval、DormCheckoutStatus）
    19	- [x] 定义状态枚举（5个枚举类型）
    20	- [x] 定义错误码（8个核心错误码）
    21	
    22	**责任人：** 后端负责人
    23	
    24	**交付物：** contract-v0.1.md初稿
    25	
    26	### Day 1（0.5-1天）
    27	
    28	**任务：**
    29	- [ ] 创建样例请求/响应（5个核心API端点）
    30	  - POST /api/auth/login
    31	  - POST /api/applications
    32	  - GET /api/applications/{id}
    33	  - POST /api/approvals/{id}/approve
    34	  - POST /api/approvals/{id}/reject
    35	- [ ] 创建Mock响应（宿舍清退Mock + 错误Mock）
    36	- [ ] 生成seed数据（10学生 + 2辅导员 + 1学工部 + 边界样本 + 默认密码）
    37	- [ ] 前端review可消费性
    38	- [ ] 业务方确认业务假设
    39	
    40	**责任人：** 后端负责人 + 前端负责人
    41	
    42	**交付物：** contract-v0.1.md冻结版
    43	
    44	**验收标准：**
    45	- [ ] 前端可用mock跑通登录→提交→审批→查询流程
    46	- [ ] 样例数据包含至少4个边界样本
    47	
    48	**降级条件：**
    49	- 如Day 1结束未完成前端review → 冻结当前版本，Week 1开始后异步review
    50	
    51	---
    52	
    53	## Week 1：后端纵向切片（5工作日）
    54	
    55	### 目标
    56	交付可运行的后端最小闭环：薄认证 + 申请提交 + 两级审批 + 状态查询 + Dorm Mock。
    57	
    58	### Day 1-2：可运行骨架
    59	
    60	**任务：**
    61	- [ ] Django项目初始化（settings分层、数据库配置）
    62	- [ ] 基础模型迁移（User、Application、Approval）
    63	- [ ] Seed命令实现（加载contract-v0.1.md中的样例数据）
    64	- [ ] 薄认证实现（学号/工号 + 密码，JWT）
    65	
    66	**责任人：** 后端负责人
    67	
    68	**交付物：**
    69	- Django项目可运行
    70	- `python manage.py seed_users` 可用
    71	- POST /api/auth/login 可用
    72	
    73	**验收标准：**
    74	- [ ] `python manage.py runserver` 启动成功
    75	- [ ] Seed数据加载成功（10学生 + 2辅导员 + 1学工部）
    76	- [ ] 登录API返回JWT token
    77	
    78	**降级条件：**
    79	- 如Day 2结束seed命令未完成 → 手动插入测试数据，Week 2补seed命令
    80	
    81	### Day 3-4：最小流程
    82	
    83	**任务：**
    84	- [ ] 申请提交API（POST /api/applications）
    85	  - 最小角色校验：只有学生可提交
    86	  - Dorm Mock集成：检查宿舍清退状态
    87	  - 状态初始化：pending_counselor
    88	  - 创建辅导员审批记录
    89	- [ ] 辅导员审批API（POST /api/approvals/{id}/approve|reject）
    90	  - 最小角色校验：只有对应班级辅导员可审批
    91	  - 状态流转：pending_counselor → pending_dean（通过）或 rejected（驳回）
    92	  - 创建学工部审批记录（通过时）
    93	- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
    94	  - 最小角色校验：只有学工部可审批
    95	  - 状态流转：pending_dean → approved（通过）或 rejected（驳回）
    96	- [ ] 状态查询API（GET /api/applications/{id}）
    97	  - 最小角色校验：学生只能查自己，辅导员/学工部可查所有
    98	
    99	**责任人：** 后端负责人
   100	
   101	**交付物：**
   102	- 4个API端点可用
   103	- 最小角色校验实现
   104	
   105	**验收标准：**
   106	- [ ] 学生可提交申请
   107	- [ ] 辅导员可审批（通过/驳回）
   108	- [ ] 学工部可审批（通过/驳回）
   109	- [ ] 状态查询返回完整申请信息和审批记录
   110	- [ ] 角色校验生效（学生不能审批，辅导员不能跨班级审批）
   111	
   112	**降级条件：**
   113	- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批
   114	- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
   115	
   116	### Day 5：验收硬化
   117	
   118	**任务：**
   119	- [ ] 端到端自动化测试
   120	  - 测试1：学生登录 → 提交申请 → 辅导员审批通过 → 学工部审批通过 → 查询状态
   121	  - 测试2：学生登录 → 提交申请 → 辅导员审批驳回 → 查询状态
   122	  - 测试3：宿舍清退未完成 → 提交申请失败（DORM_BLOCKED）
   123	  - 测试4：角色校验（学生不能审批，辅导员不能跨班级审批）
   124	- [ ] 契约测试（API响应格式符合contract-v0.1.md）
   125	- [ ] 修复阻断bug
   126	- [ ] 输出Week 2任务清单
   127	
   128	**责任人：** 后端负责人 + QA
   129	
   130	**交付物：**
   131	- 4个自动化测试通过
   132	- Week 2任务清单
   133	
   134	**验收标准：**
   135	- [ ] 所有测试通过
   136	- [ ] 无P0/P1阻断bug
   137	- [ ] Week 2任务清单明确
   138	
   139	**降级条件：**
   140	- 如Day 5结束仍有P0 bug → 推到Week 2 Day 1修复，或砍掉触发bug的边界场景
   141	
   142	---
   143	
   144	## 并行任务
   145	
   146	### 前端准备（Week 1期间）
   147	
   148	**任务：**
   149	- [ ] 技术栈选型确认（微信小程序框架）
   150	- [ ] 项目初始化
   151	- [ ] Mock Server配置（基于contract-v0.1.md）
   152	- [ ] API Client封装
   153	
   154	**责任人：** 前端负责人
   155	
   156	**时间：** Week 1 Day 1-5（与后端并行）
   157	
   158	**交付物：**
   159	- 微信小程序项目可运行
   160	- Mock Server可用
   161	- API Client可用
   162	
   163	**验收标准：**
   164	- [ ] 可用mock跑通登录→提交→审批→查询流程
   165	
   166	---
   167	
   168	## 风险和降级
   169	
   170	### 风险1：Week 0契约定义延期
   171	
   172	**概率：** 中  
   173	**影响：** 高  
   174	**缓解措施：** 1-2工作日timebox，超时冻结当前假设进入Week 1
   175	
   176	### 风险2：Week 1 Day 3申请提交API未完成
   177	
   178	**概率：** 中  
   179	**影响：** 高  
   180	**降级方案：** 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
   181	
   182	### 风险3：Week 1 Day 4学工部审批未完成
   183	
   184	**概率：** 低  
   185	**影响：** 中  
   186	**降级方案：** 推到Week 2 Day 1，Week 1只验证辅导员审批
   187	
   188	### 风险4：Week 1 Day 5测试未通过
   189	
   190	**概率：** 中  
   191	**影响：** 高  
   192	**降级方案：** 周末加班修复，或Week 2 Day 1修复
   193	
   194	---
   195	
   196	## 验收检查清单
   197	
   198	### Week 0验收
   199	
   200	- [ ] contract-v0.1.md冻结
   201	- [ ] 前端可用mock跑通完整流程
   202	- [ ] 样例数据包含边界样本
   203	
   204	### Week 1验收
   205	
   206	- [ ] Django项目可运行
   207	- [ ] Seed数据加载成功
   208	- [ ] 4个API端点可用（登录、提交、审批、查询）
   209	- [ ] 最小角色校验实现
   210	- [ ] 4个自动化测试通过
   211	- [ ] 无P0/P1阻断bug
   212	
   213	---
   214	
   215	## 下一步（Week 2）
   216	
   217	**目标：** CSV导入v1
   218	
   219	**任务：**
   220	- Staging表设计
   221	- 校验报告
   222	- Upsert逻辑
   223	- 软停用基础
   224	- 导入审计基础
   225	
   226	**工期：** 5工作日
   227	
   228	---
   229	
   230	**计划负责人：** Claude Opus 4.7  
   231	**创建日期：** 2026-05-30  
   232	**状态：** 已批准，可执行

exec
/bin/bash -lc 'rtk nl -ba docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# Contract Fixes Review Request
     2	
     3	**日期：** 2026-05-30  
     4	**审查类型：** 契约修复验证  
     5	**审查人：** Codex  
     6	**文档编号：** 47
     7	
     8	---
     9	
    10	## 背景
    11	
    12	在上一轮审查中（文档46），Codex指出contract-v0.1.md和week-0-1-execution-plan.md存在3-4个问题，导致契约"接近可执行契约"但未达到标准。
    13	
    14	**Codex原话：**
    15	> "结论：**还没有完全达到"可执行契约"标准，不建议直接开始 Week 1 的完整实施**。可以先启动不受争议影响的 Day 1 骨架、模型、seed、认证准备，但应先用半天把下面几个契约不一致点修掉再冻结。"
    16	
    17	---
    18	
    19	## 已完成的修复
    20	
    21	### 修复1：统一API端点数量（主要阻塞点）
    22	
    23	**问题：** 契约列出6个HTTP路由，计划说"5个核心API端点"（Week 0 Day 1）和"4个API端点"（Week 1 Day 3-4），口径不一致。
    24	
    25	**修复：**
    26	- 从contract-v0.1.md移除Section 4.4 GET /api/applications（列表端点）
    27	- 统一为5个HTTP路由：
    28	  1. POST /api/auth/login
    29	  2. POST /api/applications
    30	  3. GET /api/applications/{id}
    31	  4. POST /api/approvals/{id}/approve
    32	  5. POST /api/approvals/{id}/reject
    33	
    34	**理由：** 列表端点不是最小纵向切片必需的，核心流程是"登录→提交→审批→查询单个申请"。
    35	
    36	**文件：** docs/contracts/contract-v0.1.md（Section 4.4已删除）
    37	
    38	---
    39	
    40	### 修复2：添加503 PROVIDER_UNAVAILABLE样例
    41	
    42	**问题：** Dorm Mock和错误样例缺少503 PROVIDER_UNAVAILABLE场景。
    43	
    44	**修复：**
    45	- 在contract-v0.1.md Section 6.2添加503错误样例
    46	- 样例内容：
    47	```json
    48	{
    49	  "error": {
    50	    "code": "PROVIDER_UNAVAILABLE",
    51	    "message": "宿舍清退服务暂时不可用，请稍后重试",
    52	    "details": {
    53	      "student_id": "2020503",
    54	      "provider": "dorm_checkout",
    55	      "error": "Connection timeout"
    56	    }
    57	  }
    58	}
    59	```
    60	
    61	**文件：** docs/contracts/contract-v0.1.md（Section 6.2新增503样例）
    62	
    63	---
    64	
    65	### 修复3：澄清登录响应DTO
    66	
    67	**问题：** 登录响应返回部分UserDTO（只有user_id/name/role/class_id），未说明是完整DTO还是子集。
    68	
    69	**修复：**
    70	- 在contract-v0.1.md Section 4.1 POST /api/auth/login添加说明
    71	- 说明内容：
    72	> **说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。
    73	
    74	**文件：** docs/contracts/contract-v0.1.md（Section 4.1新增说明）
    75	
    76	---
    77	
    78	### 修复4：移除矛盾的降级条件
    79	
    80	**问题：** 风险表中"申请提交API未完成 → 只做查询API"与纵向切片目标矛盾（无法先查询后提交）。
    81	
    82	**修复：**
    83	- 修改week-0-1-execution-plan.md风险2降级方案：
    84	  - 原：只做查询API，Day 4补申请提交
    85	  - 新：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
    86	- 同步修改Day 3-4降级条件，移除"列表API"引用（已从契约删除）
    87	
    88	**文件：** docs/plans/week-0-1-execution-plan.md（风险2和Day 3-4降级条件已修改）
    89	
    90	---
    91	
    92	## 审查请求
    93	
    94	请Codex批判性审查以下内容：
    95	
    96	### 1. 修复完整性
    97	- [ ] 4个修复是否完全解决了上一轮指出的问题？
    98	- [ ] 是否有遗漏的修复点？
    99	
   100	### 2. API端点统一性
   101	- [ ] 契约和计划的API端点数量现在是否一致？
   102	- [ ] 移除列表端点的决策是否合理？
   103	- [ ] 5个HTTP路由是否足以支撑最小纵向切片？
   104	
   105	### 3. 错误样例完整性
   106	- [ ] 503样例是否覆盖了PROVIDER_UNAVAILABLE场景？
   107	- [ ] 错误样例是否覆盖了所有Section 3定义的错误码？
   108	
   109	### 4. DTO一致性
   110	- [ ] AuthUserDTO说明是否清晰？
   111	- [ ] 是否需要在Section 1添加AuthUserDTO的正式定义？
   112	
   113	### 5. 降级条件合理性
   114	- [ ] 新的降级条件是否保持了纵向切片完整性？
   115	- [ ] 降级条件是否现实可行？
   116	
   117	### 6. 可执行性评估
   118	- [ ] 契约现在是否达到"可执行契约"标准？
   119	- [ ] 是否可以冻结契约并开始Week 1 Day 1工作？
   120	- [ ] 如果还有问题，优先级如何排序？
   121	
   122	---
   123	
   124	## 期望输出
   125	
   126	1. **修复验证：** 逐项确认4个修复是否解决了问题
   127	2. **剩余问题：** 如果还有问题，列出具体问题和修复建议
   128	3. **可执行性判断：** 明确回答"是否达到可执行契约标准"
   129	4. **下一步建议：** 如果达标，建议冻结契约；如果未达标，建议优先修复哪些点
   130	
   131	---
   132	
   133	**请求人：** Claude Opus 4.7  
   134	**审查协议：** docs/codex-review-protocol.md  
   135	**相关文档：**
   136	- docs/contracts/contract-v0.1.md（已修改）
   137	- docs/plans/week-0-1-execution-plan.md（已修改）
   138	- docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md（上一轮共识）

exec
/bin/bash -lc 'rtk nl -ba docs/contracts/contract-v0.1.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# 数据契约 v0.1 - 最小可执行契约
     2	
     3	**版本：** v0.1  
     4	**冻结日期：** 2026-05-30  
     5	**适用范围：** Week 1纵向切片  
     6	**下一版本：** v0.2（Week 3）
     7	
     8	---
     9	
    10	## 1. 核心DTO
    11	
    12	### 1.1 UserDTO
    13	
    14	```python
    15	@dataclass
    16	class UserDTO:
    17	    """用户数据传输对象"""
    18	    user_id: str                      # 学号/工号
    19	    name: str                         # 姓名
    20	    role: UserRole                    # 角色：student/counselor/dean
    21	    active: bool                      # 账号是否激活
    22	    class_id: Optional[str] = None    # 班级ID（学生必填，教师为None）
    23	    is_graduating: Optional[bool] = None  # 是否毕业生（仅学生）
    24	    graduation_year: Optional[int] = None # 毕业年份（仅学生）
    25	```
    26	
    27	### 1.2 ApplicationDTO
    28	
    29	```python
    30	@dataclass
    31	class ApplicationDTO:
    32	    """离校申请数据传输对象"""
    33	    application_id: str
    34	    student_id: str
    35	    student_name: str
    36	    class_id: str
    37	    reason: str                      # 申请理由
    38	    leave_date: str                  # 计划离校日期 (YYYY-MM-DD)
    39	    status: ApplicationStatus
    40	    dorm_checkout_status: DormCheckoutStatus
    41	    created_at: str                  # ISO8601
    42	    updated_at: str
    43	```
    44	
    45	### 1.3 ApprovalDTO
    46	
    47	```python
    48	@dataclass
    49	class ApprovalDTO:
    50	    """审批记录数据传输对象"""
    51	    approval_id: str
    52	    application_id: str
    53	    step: ApprovalStep           # counselor/dean
    54	    approver_id: str
    55	    approver_name: str
    56	    decision: ApprovalDecision   # approved/rejected/pending
    57	    comment: Optional[str]
    58	    decided_at: Optional[str]    # ISO8601
    59	```
    60	
    61	### 1.4 DormCheckoutStatusDTO
    62	
    63	```python
    64	@dataclass
    65	class DormCheckoutStatusDTO:
    66	    """宿舍清退状态数据传输对象"""
    67	    student_id: str
    68	    status: DormCheckoutStatus   # completed/pending/not_started/unknown
    69	    checked_at: Optional[str]    # ISO8601
    70	    blocking_reason: Optional[str]
    71	    provider_error_code: Optional[str]
    72	```
    73	
    74	---
    75	
    76	## 2. 状态枚举
    77	
    78	### 2.1 UserRole
    79	
    80	```python
    81	class UserRole(str, Enum):
    82	    STUDENT = "student"
    83	    COUNSELOR = "counselor"
    84	    DEAN = "dean"
    85	```
    86	
    87	### 2.2 ApplicationStatus
    88	
    89	```python
    90	class ApplicationStatus(str, Enum):
    91	    DRAFT = "draft"                      # 草稿
    92	    PENDING_COUNSELOR = "pending_counselor"  # 待辅导员审批
    93	    PENDING_DEAN = "pending_dean"        # 待学工部审批
    94	    APPROVED = "approved"                # 已通过
    95	    REJECTED = "rejected"                # 已驳回
    96	```
    97	
    98	### 2.3 ApprovalStep
    99	
   100	```python
   101	class ApprovalStep(str, Enum):
   102	    COUNSELOR = "counselor"
   103	    DEAN = "dean"
   104	```
   105	
   106	### 2.4 ApprovalDecision
   107	
   108	```python
   109	class ApprovalDecision(str, Enum):
   110	    PENDING = "pending"
   111	    APPROVED = "approved"
   112	    REJECTED = "rejected"
   113	```
   114	
   115	### 2.5 DormCheckoutStatus
   116	
   117	```python
   118	class DormCheckoutStatus(str, Enum):
   119	    COMPLETED = "completed"          # 已清退
   120	    PENDING = "pending"              # 清退中
   121	    NOT_STARTED = "not_started"      # 未开始
   122	    UNKNOWN = "unknown"              # 状态未知（API失败）
   123	```
   124	
   125	### 2.6 状态机契约
   126	
   127	**申请状态流转规则：**
   128	
   129	| 当前状态 | 触发动作 | 角色 | 下一状态 | 副作用 |
   130	|---------|---------|------|---------|--------|
   131	| - | 学生提交申请 | student | pending_counselor | 创建辅导员审批记录 |
   132	| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
   133	| pending_counselor | 辅导员驳回 | counselor | rejected | 无 |
   134	| pending_dean | 学工部通过 | dean | approved | 无 |
   135	| pending_dean | 学工部驳回 | dean | rejected | 无 |
   136	
   137	**宿舍清退状态处理规则：**
   138	
   139	| 宿舍状态 | 提交申请行为 | HTTP状态 | 错误码 |
   140	|---------|------------|---------|--------|
   141	| completed | 允许提交 | 201 | - |
   142	| pending | 阻断提交 | 422 | DORM_BLOCKED |
   143	| not_started | 阻断提交 | 422 | DORM_BLOCKED |
   144	| unknown | 阻断提交 | 422 | DORM_BLOCKED |
   145	| provider_unavailable | 阻断提交 | 503 | PROVIDER_UNAVAILABLE |
   146	
   147	**角色权限矩阵：**
   148	
   149	| 操作 | student | counselor | dean |
   150	|------|---------|-----------|------|
   151	| 提交申请 | ✓（仅自己） | ✗ | ✗ |
   152	| 查看申请 | ✓（仅自己） | ✓（本班级） | ✓（所有） |
   153	| 辅导员审批 | ✗ | ✓（本班级） | ✗ |
   154	| 学工部审批 | ✗ | ✗ | ✓（所有） |
   155	
   156	---
   157	
   158	## 3. 错误码
   159	
   160	### 3.1 业务错误 (4xx)
   161	
   162	| 错误码 | HTTP状态 | 说明 | 示例场景 |
   163	|--------|---------|------|---------|
   164	| VALIDATION_ERROR | 400 | 请求参数校验失败 | 必填字段缺失、格式错误 |
   165	| AUTH_REQUIRED | 401 | 未认证 | Token缺失或过期 |
   166	| FORBIDDEN | 403 | 无权限 | 学生访问他人申请 |
   167	| NOT_FOUND | 404 | 资源不存在 | 申请ID不存在 |
   168	| CONFLICT | 409 | 资源冲突 | 重复提交申请 |
   169	| DORM_BLOCKED | 422 | 宿舍清退未完成 | 提交申请时宿舍未清退 |
   170	
   171	### 3.2 系统错误 (5xx)
   172	
   173	| 错误码 | HTTP状态 | 说明 | 示例场景 |
   174	|--------|---------|------|---------|
   175	| PROVIDER_UNAVAILABLE | 503 | 外部服务不可用 | 宿舍清退API超时 |
   176	| INTERNAL_ERROR | 500 | 内部错误 | 数据库连接失败 |
   177	
   178	### 3.3 错误响应格式
   179	
   180	```json
   181	{
   182	  "error": {
   183	    "code": "DORM_BLOCKED",
   184	    "message": "宿舍清退未完成，无法提交申请",
   185	    "details": {
   186	      "student_id": "2020001",
   187	      "dorm_status": "pending"
   188	    }
   189	  }
   190	}
   191	```
   192	
   193	---
   194	
   195	## 4. API端点
   196	
   197	### 4.1 认证
   198	
   199	#### POST /api/auth/login
   200	
   201	**请求：**
   202	```json
   203	{
   204	  "user_id": "2020001",
   205	  "password": "password123"
   206	}
   207	```
   208	
   209	**响应：**
   210	```json
   211	{
   212	  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
   213	  "token_type": "Bearer",
   214	  "user": {
   215	    "user_id": "2020001",
   216	    "name": "张三",
   217	    "role": "student",
   218	    "class_id": "CS2020-01"
   219	  }
   220	}
   221	```
   222	
   223	**说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。
   224	
   225	### 4.2 申请
   226	
   227	#### POST /api/applications
   228	
   229	**请求：**
   230	```json
   231	{
   232	  "reason": "毕业离校",
   233	  "leave_date": "2024-06-30"
   234	}
   235	```
   236	
   237	**响应：**
   238	```json
   239	{
   240	  "application_id": "app_001",
   241	  "student_id": "2020001",
   242	  "student_name": "张三",
   243	  "class_id": "CS2020-01",
   244	  "reason": "毕业离校",
   245	  "leave_date": "2024-06-30",
   246	  "status": "pending_counselor",
   247	  "dorm_checkout_status": "completed",
   248	  "created_at": "2024-05-30T10:00:00Z",
   249	  "updated_at": "2024-05-30T10:00:00Z"
   250	}
   251	```
   252	
   253	#### GET /api/applications/{application_id}
   254	
   255	**响应：**
   256	```json
   257	{
   258	  "application_id": "app_001",
   259	  "student_id": "2020001",
   260	  "student_name": "张三",
   261	  "class_id": "CS2020-01",
   262	  "reason": "毕业离校",
   263	  "leave_date": "2024-06-30",
   264	  "status": "pending_counselor",
   265	  "dorm_checkout_status": "completed",
   266	  "approvals": [
   267	    {
   268	      "approval_id": "apv_001",
   269	      "step": "counselor",
   270	      "approver_id": "T001",
   271	      "approver_name": "李老师",
   272	      "decision": "pending",
   273	      "comment": null,
   274	      "decided_at": null
   275	    }
   276	  ],
   277	  "created_at": "2024-05-30T10:00:00Z",
   278	  "updated_at": "2024-05-30T10:00:00Z"
   279	}
   280	```
   281	
   282	### 4.3 审批
   283	
   284	#### POST /api/approvals/{approval_id}/approve
   285	
   286	**请求：**
   287	```json
   288	{
   289	  "comment": "同意离校"
   290	}
   291	```
   292	
   293	**响应：**
   294	```json
   295	{
   296	  "approval_id": "apv_001",
   297	  "application_id": "app_001",
   298	  "step": "counselor",
   299	  "approver_id": "T001",
   300	  "approver_name": "李老师",
   301	  "decision": "approved",
   302	  "comment": "同意离校",
   303	  "decided_at": "2024-05-30T11:00:00Z"
   304	}
   305	```
   306	
   307	#### POST /api/approvals/{approval_id}/reject
   308	
   309	**请求：**
   310	```json
   311	{
   312	  "comment": "材料不齐全"
   313	}
   314	```
   315	
   316	**响应：**
   317	```json
   318	{
   319	  "approval_id": "apv_001",
   320	  "application_id": "app_001",
   321	  "step": "counselor",
   322	  "approver_id": "T001",
   323	  "approver_name": "李老师",
   324	  "decision": "rejected",
   325	  "comment": "材料不齐全",
   326	  "decided_at": "2024-05-30T11:00:00Z"
   327	}
   328	```
   329	
   330	---
   331	
   332	## 5. 样例数据
   333	
   334	### 5.1 正常样本
   335	
   336	**默认密码：** 所有账号默认密码为 `password123`
   337	
   338	**学生（10人）：**
   339	```python
   340	students = [
   341	    {"user_id": "2020001", "name": "张三", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
   342	    {"user_id": "2020002", "name": "李四", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
   343	    {"user_id": "2020003", "name": "王五", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
   344	    {"user_id": "2020004", "name": "赵六", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
   345	    {"user_id": "2020005", "name": "钱七", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
   346	    {"user_id": "2020006", "name": "孙八", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
   347	    {"user_id": "2020007", "name": "周九", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
   348	    {"user_id": "2020008", "name": "吴十", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
   349	    {"user_id": "2020009", "name": "郑十一", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
   350	    {"user_id": "2020010", "name": "王十二", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
   351	]
   352	```
   353	
   354	**辅导员（2人）：**
   355	```python
   356	counselors = [
   357	    {"user_id": "T001", "name": "李老师", "role": "counselor", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
   358	    {"user_id": "T002", "name": "王老师", "role": "counselor", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
   359	]
   360	```
   361	
   362	**学工部（1人）：**
   363	```python
   364	deans = [
   365	    {"user_id": "D001", "name": "赵主任", "role": "dean", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
   366	]
   367	```
   368	
   369	**班级映射：**
   370	```python
   371	class_mappings = [
   372	    {"class_id": "CS2020-01", "counselor_id": "T001"},
   373	    {"class_id": "CS2020-02", "counselor_id": "T002"},
   374	]
   375	```
   376	
   377	### 5.2 边界样本
   378	
   379	**无班级映射：**
   380	```python
   381	{"user_id": "2020099", "name": "边界1", "role": "student", "class_id": "INVALID", "is_graduating": True, "graduation_year": 2024, "active": True}
   382	```
   383	
   384	**辅导员停用：**
   385	```python
   386	{"user_id": "T099", "name": "停用老师", "role": "counselor", "class_id": None, "active": False}
   387	```
   388	
   389	**非毕业生：**
   390	```python
   391	{"user_id": "2021001", "name": "边界2", "role": "student", "class_id": "CS2021-01", "is_graduating": False, "graduation_year": 2025, "active": True}
   392	```
   393	
   394	**延期毕业：**
   395	```python
   396	{"user_id": "2019001", "name": "边界3", "role": "student", "class_id": "CS2019-01", "is_graduating": True, "graduation_year": 2024, "active": True}
   397	```
   398	
   399	---
   400	
   401	## 6. Mock响应
   402	
   403	### 6.1 宿舍清退Mock
   404	
   405	**DormCheckoutProvider Mock实现：**
   406	
   407	```python
   408	class MockDormCheckoutProvider:
   409	    def check_status(self, student_id: str) -> DormCheckoutStatusDTO:
   410	        # 固定返回规则（覆盖所有状态）
   411	        mock_data = {
   412	            "2020001": DormCheckoutStatusDTO(
   413	                student_id="2020001",
   414	                status=DormCheckoutStatus.COMPLETED,
   415	                checked_at="2024-05-15T10:00:00Z",
   416	                blocking_reason=None,
   417	                provider_error_code=None
   418	            ),
   419	            "2020002": DormCheckoutStatusDTO(
   420	                student_id="2020002",
   421	                status=DormCheckoutStatus.PENDING,
   422	                checked_at=None,
   423	                blocking_reason="宿舍物品未清理",
   424	                provider_error_code=None
   425	            ),
   426	            "2020003": DormCheckoutStatusDTO(
   427	                student_id="2020003",
   428	                status=DormCheckoutStatus.NOT_STARTED,
   429	                checked_at=None,
   430	                blocking_reason="未提交清退申请",
   431	                provider_error_code=None
   432	            ),
   433	            "2020099": DormCheckoutStatusDTO(
   434	                student_id="2020099",
   435	                status=DormCheckoutStatus.UNKNOWN,
   436	                checked_at=None,
   437	                blocking_reason="学生信息不存在",
   438	                provider_error_code="STUDENT_NOT_FOUND"
   439	            ),
   440	        }
   441	        
   442	        # 默认返回NOT_STARTED（而非completed，避免掩盖失败路径）
   443	        return mock_data.get(student_id, DormCheckoutStatusDTO(
   444	            student_id=student_id,
   445	            status=DormCheckoutStatus.NOT_STARTED,
   446	            checked_at=None,
   447	            blocking_reason="未在宿舍系统中找到记录",
   448	            provider_error_code=None
   449	        ))
   450	```
   451	
   452	### 6.2 错误Mock
   453	
   454	**401 Unauthorized：**
   455	```json
   456	{
   457	  "error": {
   458	    "code": "AUTH_REQUIRED",
   459	    "message": "Token缺失或过期"
   460	  }
   461	}
   462	```
   463	
   464	**403 Forbidden：**
   465	```json
   466	{
   467	  "error": {
   468	    "code": "FORBIDDEN",
   469	    "message": "无权限访问此资源"
   470	  }
   471	}
   472	```
   473	
   474	**422 Dorm Blocked：**
   475	```json
   476	{
   477	  "error": {
   478	    "code": "DORM_BLOCKED",
   479	    "message": "宿舍清退未完成，无法提交申请",
   480	    "details": {
   481	      "student_id": "2020002",
   482	      "dorm_status": "pending",
   483	      "blocking_reason": "宿舍物品未清理"
   484	    }
   485	  }
   486	}
   487	```
   488	
   489	**503 Provider Unavailable：**
   490	```json
   491	{
   492	  "error": {
   493	    "code": "PROVIDER_UNAVAILABLE",
   494	    "message": "宿舍清退服务暂时不可用，请稍后重试",
   495	    "details": {
   496	      "student_id": "2020503",
   497	      "provider": "dorm_checkout",
   498	      "error": "Connection timeout"
   499	    }
   500	  }
   501	}
   502	```
   503	
   504	---
   505	
   506	## 7. 变更日志
   507	
   508	### v0.1 (2026-05-30)
   509	
   510	**初始版本 - 最小可执行契约**
   511	
   512	**包含内容：**
   513	- 核心DTO（User、Application、Approval、DormCheckoutStatus）
   514	- 状态枚举（UserRole、ApplicationStatus、ApprovalStep、ApprovalDecision、DormCheckoutStatus）
   515	- 错误码（8个核心错误码）
   516	- API端点（认证、申请、审批、查询）
   517	- 样例数据（正常样本 + 边界样本）
   518	- Mock响应（宿舍清退Mock + 错误Mock）
   519	
   520	**不包含内容（v0.2）：**
   521	- 附件相关DTO和API
   522	- 通知相关DTO和API
   523	- 微信OAuth相关API
   524	- 完整RBAC权限矩阵
   525	- 审批转办、撤回、驳回重提
   526	
   527	**验收标准：**
   528	- 前端可用mock跑通登录→提交→审批→查询流程
   529	- 后端可用seed数据跑通端到端测试
   530	
   531	---
   532	
   533	## 8. 使用说明
   534	
   535	### 8.1 前端使用
   536	
   537	**Mock Server配置：**
   538	```javascript
   539	// mock/handlers.js
   540	export const handlers = [
   541	  rest.post('/api/auth/login', (req, res, ctx) => {
   542	    return res(ctx.json({
   543	      access_token: 'mock_token',
   544	      token_type: 'Bearer',
   545	      user: {
   546	        user_id: '2020001',
   547	        name: '张三',
   548	        role: 'student',
   549	        class_id: 'CS2020-01'
   550	      }
   551	    }))
   552	  }),
   553	  // ... 其他端点
   554	]
   555	```
   556	
   557	### 8.2 后端使用
   558	
   559	**Seed数据加载：**
   560	```bash
   561	python manage.py seed_users
   562	python manage.py seed_class_mappings
   563	```
   564	
   565	**端到端测试：**
   566	```python
   567	def test_application_flow():
   568	    # 1. 学生登录
   569	    response = client.post('/api/auth/login', {
   570	        'user_id': '2020001',
   571	        'password': 'password123'
   572	    })
   573	    token = response.json()['access_token']
   574	    
   575	    # 2. 提交申请
   576	    response = client.post('/api/applications', 
   577	        headers={'Authorization': f'Bearer {token}'},
   578	        json={'reason': '毕业离校', 'leave_date': '2024-06-30'}
   579	    )
   580	    app_id = response.json()['application_id']
   581	    
   582	    # 3. 辅导员审批
   583	    # 4. 学工部审批
   584	    # 5. 查询状态
   585	```
   586	
   587	---
   588	
   589	**契约负责人：** Claude Opus 4.7  
   590	**前端Review：** 待确认  
   591	**业务确认：** 待确认  
   592	**冻结日期：** 2026-05-30  
   593	**下一版本：** v0.2（Week 3）

codex
我会把审查结论写入 `docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md`。核心判断会很直接：4 个修复方向正确，但仍有 3 个小范围修正，其中错误样例覆盖和降级措辞会影响“冻结前最后半天”的质量门槛。
apply patch
patch: completed
/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
diff --git a/docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md b/docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..5bf33a4f30f13985de504c9e093d98eb4652c6de
--- /dev/null
+++ b/docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
@@ -0,0 +1,190 @@
+# Contract Fixes - Codex Review Response
+
+**审查日期：** 2026-05-30  
+**审查人：** Codex  
+**针对文档：** 47-contract-fixes-review-request.md  
+**审查类型：** 契约修复验证
+
+---
+
+## 审查结论
+
+**结论：尚未完全达到可执行契约标准，但已经非常接近。**
+
+4个修复方向都正确，且主要阻塞点已经明显收敛：契约正文现在只有5个HTTP路由，列表端点已移除；503 `PROVIDER_UNAVAILABLE`样例已补；登录响应的DTO子集问题已说明；原先“申请未完成却只做查询”的降级方向已被替换。
+
+但冻结前仍建议用半天完成3个收尾修正：
+
+1. **P1：错误样例未覆盖Section 3定义的全部错误码。**
+2. **P1：降级方案仍有一句口径冲突，且Day 3提交未完成时的措辞不够可执行。**
+3. **P2：计划文档仍混用“5个HTTP路由”和“4个API端点/能力”的口径；AuthUserDTO最好正式纳入Section 1。**
+
+完成这些收尾后，可以冻结契约并开始Week 1工作。
+
+---
+
+## 逐项修复验证
+
+### 修复1：统一API端点数量
+
+**验证结果：基本解决，但计划文档仍需术语收口。**
+
+契约Section 4现在实际列出5个HTTP路由：
+
+1. `POST /api/auth/login`
+2. `POST /api/applications`
+3. `GET /api/applications/{application_id}`
+4. `POST /api/approvals/{approval_id}/approve`
+5. `POST /api/approvals/{approval_id}/reject`
+
+列表端点 `GET /api/applications` 已不在契约中。移除列表端点是合理的，因为v0.1纵向切片只需要“登录 -> 提交 -> 审批 -> 查询单个申请”，不需要审批队列或学生申请列表。
+
+剩余问题是计划文档仍写“4个API端点可用（登录、提交、审批、查询）”。这更像4个核心能力，而不是HTTP路由。建议统一术语：
+
+- HTTP路由：5个
+- 核心能力：4个，登录、提交、审批、查询
+- Day 3-4新增HTTP路由：4个，不含Day 1-2已完成的login
+
+否则后续验收时仍可能出现“到底是4个还是5个端点”的争议。
+
+### 修复2：添加503 PROVIDER_UNAVAILABLE样例
+
+**验证结果：部分解决。**
+
+契约已经新增503样例，且与宿舍清退外部服务不可用场景匹配：
+
+- `PROVIDER_UNAVAILABLE`
+- HTTP 503
+- `provider: dorm_checkout`
+- timeout细节
+
+这解决了上一轮指出的503缺口。
+
+但Section 3定义了8个错误码，而Section 6.2当前只提供了4类错误样例：401、403、422、503。缺少：
+
+- `VALIDATION_ERROR` 400
+- `NOT_FOUND` 404
+- `CONFLICT` 409
+- `INTERNAL_ERROR` 500
+
+如果v0.1目标是“前端可用mock跑通并处理错误态”，错误样例应至少覆盖Section 3列出的全部错误码。否则前端mock、契约测试和后端异常处理仍会自行发挥。
+
+### 修复3：澄清登录响应DTO
+
+**验证结果：说明清晰，但建议正式定义AuthUserDTO。**
+
+Section 4.1说明 `user` 是 `AuthUserDTO`，是 `UserDTO` 的子集，只包含 `user_id/name/role/class_id`。这解决了“登录响应到底是不是完整UserDTO”的歧义。
+
+仍建议在Section 1加入正式定义：
+
+```python
+@dataclass
+class AuthUserDTO:
+    """登录响应中的用户摘要"""
+    user_id: str
+    name: str
+    role: UserRole
+    class_id: Optional[str] = None
+```
+
+原因是契约已经命名了 `AuthUserDTO`，但核心DTO章节没有定义它。对后端实现、前端类型生成、契约测试来说，正式定义比正文说明更可靠。
+
+### 修复4：移除矛盾的降级条件
+
+**验证结果：方向正确，但风险表还需要改一句。**
+
+计划已经移除了“申请提交API未完成 -> 只做查询API”的矛盾逻辑，新的方向是优先保留“提交 -> 辅导员审批 -> 查询”最短闭环。这符合纵向切片目标。
+
+但风险表仍写：
+
+> 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
+
+这里“砍学工部审批”和“Day 4补学工部审批”同时出现，口径冲突。更合理的表达是：
+
+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
+
+这样降级条件才真正可执行：先保住最短闭环，不在同一天又承诺补回被砍范围。
+
+---
+
+## 剩余问题与修复建议
+
+### P1：错误样例覆盖不完整
+
+**位置：** `docs/contracts/contract-v0.1.md` Section 3和Section 6.2
+
+**问题：** Section 3定义8个错误码，但错误Mock只覆盖4个。
+
+**影响：** 前端mock、后端异常格式、契约测试无法完整对齐。
+
+**修复建议：** 在Section 6.2补齐400、404、409、500样例。每个样例都保持统一结构：
+
+```json
+{
+  "error": {
+    "code": "VALIDATION_ERROR",
+    "message": "请求参数校验失败",
+    "details": {
+      "field": "leave_date",
+      "reason": "must be YYYY-MM-DD"
+    }
+  }
+}
+```
+
+### P1：降级条件仍有口径冲突
+
+**位置：** `docs/plans/week-0-1-execution-plan.md` 风险2
+
+**问题：** 同一句话同时说“砍学工部审批”和“Day 4补学工部审批”。
+
+**影响：** Day 3风险触发后团队不知道是保闭环，还是继续追两级审批。
+
+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
+
+### P2：API端点术语仍不够统一
+
+**位置：** `docs/plans/week-0-1-execution-plan.md` Day 3-4交付物、Week 1验收
+
+**问题：** 计划中“4个API端点”实际指4个核心能力或Day 3-4新增HTTP路由，不等于契约的5个HTTP路由。
+
+**影响：** 不一定阻塞实现，但会继续制造验收口径争议。
+
+**修复建议：** 改为：
+
+- Week 0：5个HTTP路由样例
+- Day 3-4交付物：4个业务HTTP路由可用，不含登录
+- Week 1验收：5个HTTP路由可用，覆盖4个核心能力
+
+### P2：AuthUserDTO应正式定义
+
+**位置：** `docs/contracts/contract-v0.1.md` Section 1
+
+**问题：** Section 4.1引用了 `AuthUserDTO`，但Section 1没有该DTO定义。
+
+**影响：** 对人工阅读影响小，对类型生成和契约测试有轻微歧义。
+
+**修复建议：** 在UserDTO之后添加 `AuthUserDTO`，并调整后续编号。
+
+---
+
+## 可执行性判断
+
+**当前状态：未完全达到可执行契约标准。**
+
+不是因为方向错，而是因为仍有两个会影响执行验收的P1口径缺口：错误样例未全覆盖，降级风险表仍有冲突措辞。它们都属于半天内可以修完的收尾问题。
+
+**修完上述P1后：可以冻结contract-v0.1.md，并开始Week 1 Day 1工作。**
+
+如果团队已经要启动Week 1，也可以先启动不受这些问题影响的Day 1-2工作：Django骨架、基础模型、seed、登录认证。但不建议在P1修完前把契约标记为Final并全面进入Day 3-4业务API实现。
+
+---
+
+## 下一步建议
+
+1. 立即补齐4个缺失错误样例：400、404、409、500。
+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
+3. 将计划中的“4个API端点”改成“4个核心能力”或“4个业务HTTP路由”，避免和5个HTTP路由冲突。
+4. 在Section 1补 `AuthUserDTO` 正式定义。
+5. 完成后可直接冻结v0.1，不需要再开一轮长审查；只需做一次差异核对。
+

diff --git a/docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md b/docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..5bf33a4f30f13985de504c9e093d98eb4652c6de
--- /dev/null
+++ b/docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
@@ -0,0 +1,190 @@
+# Contract Fixes - Codex Review Response
+
+**审查日期：** 2026-05-30  
+**审查人：** Codex  
+**针对文档：** 47-contract-fixes-review-request.md  
+**审查类型：** 契约修复验证
+
+---
+
+## 审查结论
+
+**结论：尚未完全达到可执行契约标准，但已经非常接近。**
+
+4个修复方向都正确，且主要阻塞点已经明显收敛：契约正文现在只有5个HTTP路由，列表端点已移除；503 `PROVIDER_UNAVAILABLE`样例已补；登录响应的DTO子集问题已说明；原先“申请未完成却只做查询”的降级方向已被替换。
+
+但冻结前仍建议用半天完成3个收尾修正：
+
+1. **P1：错误样例未覆盖Section 3定义的全部错误码。**
+2. **P1：降级方案仍有一句口径冲突，且Day 3提交未完成时的措辞不够可执行。**
+3. **P2：计划文档仍混用“5个HTTP路由”和“4个API端点/能力”的口径；AuthUserDTO最好正式纳入Section 1。**
+
+完成这些收尾后，可以冻结契约并开始Week 1工作。
+
+---
+
+## 逐项修复验证
+
+### 修复1：统一API端点数量
+
+**验证结果：基本解决，但计划文档仍需术语收口。**
+
+契约Section 4现在实际列出5个HTTP路由：
+
+1. `POST /api/auth/login`
+2. `POST /api/applications`
+3. `GET /api/applications/{application_id}`
+4. `POST /api/approvals/{approval_id}/approve`
+5. `POST /api/approvals/{approval_id}/reject`
+
+列表端点 `GET /api/applications` 已不在契约中。移除列表端点是合理的，因为v0.1纵向切片只需要“登录 -> 提交 -> 审批 -> 查询单个申请”，不需要审批队列或学生申请列表。
+
+剩余问题是计划文档仍写“4个API端点可用（登录、提交、审批、查询）”。这更像4个核心能力，而不是HTTP路由。建议统一术语：
+
+- HTTP路由：5个
+- 核心能力：4个，登录、提交、审批、查询
+- Day 3-4新增HTTP路由：4个，不含Day 1-2已完成的login
+
+否则后续验收时仍可能出现“到底是4个还是5个端点”的争议。
+
+### 修复2：添加503 PROVIDER_UNAVAILABLE样例
+
+**验证结果：部分解决。**
+
+契约已经新增503样例，且与宿舍清退外部服务不可用场景匹配：
+
+- `PROVIDER_UNAVAILABLE`
+- HTTP 503
+- `provider: dorm_checkout`
+- timeout细节
+
+这解决了上一轮指出的503缺口。
+
+但Section 3定义了8个错误码，而Section 6.2当前只提供了4类错误样例：401、403、422、503。缺少：
+
+- `VALIDATION_ERROR` 400
+- `NOT_FOUND` 404
+- `CONFLICT` 409
+- `INTERNAL_ERROR` 500
+
+如果v0.1目标是“前端可用mock跑通并处理错误态”，错误样例应至少覆盖Section 3列出的全部错误码。否则前端mock、契约测试和后端异常处理仍会自行发挥。
+
+### 修复3：澄清登录响应DTO
+
+**验证结果：说明清晰，但建议正式定义AuthUserDTO。**
+
+Section 4.1说明 `user` 是 `AuthUserDTO`，是 `UserDTO` 的子集，只包含 `user_id/name/role/class_id`。这解决了“登录响应到底是不是完整UserDTO”的歧义。
+
+仍建议在Section 1加入正式定义：
+
+```python
+@dataclass
+class AuthUserDTO:
+    """登录响应中的用户摘要"""
+    user_id: str
+    name: str
+    role: UserRole
+    class_id: Optional[str] = None
+```
+
+原因是契约已经命名了 `AuthUserDTO`，但核心DTO章节没有定义它。对后端实现、前端类型生成、契约测试来说，正式定义比正文说明更可靠。
+
+### 修复4：移除矛盾的降级条件
+
+**验证结果：方向正确，但风险表还需要改一句。**
+
+计划已经移除了“申请提交API未完成 -> 只做查询API”的矛盾逻辑，新的方向是优先保留“提交 -> 辅导员审批 -> 查询”最短闭环。这符合纵向切片目标。
+
+但风险表仍写：
+
+> 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
+
+这里“砍学工部审批”和“Day 4补学工部审批”同时出现，口径冲突。更合理的表达是：
+
+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
+
+这样降级条件才真正可执行：先保住最短闭环，不在同一天又承诺补回被砍范围。
+
+---
+
+## 剩余问题与修复建议
+
+### P1：错误样例覆盖不完整
+
+**位置：** `docs/contracts/contract-v0.1.md` Section 3和Section 6.2
+
+**问题：** Section 3定义8个错误码，但错误Mock只覆盖4个。
+
+**影响：** 前端mock、后端异常格式、契约测试无法完整对齐。
+
+**修复建议：** 在Section 6.2补齐400、404、409、500样例。每个样例都保持统一结构：
+
+```json
+{
+  "error": {
+    "code": "VALIDATION_ERROR",
+    "message": "请求参数校验失败",
+    "details": {
+      "field": "leave_date",
+      "reason": "must be YYYY-MM-DD"
+    }
+  }
+}
+```
+
+### P1：降级条件仍有口径冲突
+
+**位置：** `docs/plans/week-0-1-execution-plan.md` 风险2
+
+**问题：** 同一句话同时说“砍学工部审批”和“Day 4补学工部审批”。
+
+**影响：** Day 3风险触发后团队不知道是保闭环，还是继续追两级审批。
+
+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
+
+### P2：API端点术语仍不够统一
+
+**位置：** `docs/plans/week-0-1-execution-plan.md` Day 3-4交付物、Week 1验收
+
+**问题：** 计划中“4个API端点”实际指4个核心能力或Day 3-4新增HTTP路由，不等于契约的5个HTTP路由。
+
+**影响：** 不一定阻塞实现，但会继续制造验收口径争议。
+
+**修复建议：** 改为：
+
+- Week 0：5个HTTP路由样例
+- Day 3-4交付物：4个业务HTTP路由可用，不含登录
+- Week 1验收：5个HTTP路由可用，覆盖4个核心能力
+
+### P2：AuthUserDTO应正式定义
+
+**位置：** `docs/contracts/contract-v0.1.md` Section 1
+
+**问题：** Section 4.1引用了 `AuthUserDTO`，但Section 1没有该DTO定义。
+
+**影响：** 对人工阅读影响小，对类型生成和契约测试有轻微歧义。
+
+**修复建议：** 在UserDTO之后添加 `AuthUserDTO`，并调整后续编号。
+
+---
+
+## 可执行性判断
+
+**当前状态：未完全达到可执行契约标准。**
+
+不是因为方向错，而是因为仍有两个会影响执行验收的P1口径缺口：错误样例未全覆盖，降级风险表仍有冲突措辞。它们都属于半天内可以修完的收尾问题。
+
+**修完上述P1后：可以冻结contract-v0.1.md，并开始Week 1 Day 1工作。**
+
+如果团队已经要启动Week 1，也可以先启动不受这些问题影响的Day 1-2工作：Django骨架、基础模型、seed、登录认证。但不建议在P1修完前把契约标记为Final并全面进入Day 3-4业务API实现。
+
+---
+
+## 下一步建议
+
+1. 立即补齐4个缺失错误样例：400、404、409、500。
+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
+3. 将计划中的“4个API端点”改成“4个核心能力”或“4个业务HTTP路由”，避免和5个HTTP路由冲突。
+4. 在Section 1补 `AuthUserDTO` 正式定义。
+5. 完成后可直接冻结v0.1，不需要再开一轮长审查；只需做一次差异核对。
+

codex
审查响应文档已生成。现在我会快速校验新文档内容，并检查工作区变更，确保只新增了预期审查文件。
exec
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system
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
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Contract Fixes - Codex Review Response

**审查日期：** 2026-05-30  
**审查人：** Codex  
**针对文档：** 47-contract-fixes-review-request.md  
**审查类型：** 契约修复验证

---

## 审查结论

**结论：尚未完全达到可执行契约标准，但已经非常接近。**

4个修复方向都正确，且主要阻塞点已经明显收敛：契约正文现在只有5个HTTP路由，列表端点已移除；503 `PROVIDER_UNAVAILABLE`样例已补；登录响应的DTO子集问题已说明；原先“申请未完成却只做查询”的降级方向已被替换。

但冻结前仍建议用半天完成3个收尾修正：

1. **P1：错误样例未覆盖Section 3定义的全部错误码。**
2. **P1：降级方案仍有一句口径冲突，且Day 3提交未完成时的措辞不够可执行。**
3. **P2：计划文档仍混用“5个HTTP路由”和“4个API端点/能力”的口径；AuthUserDTO最好正式纳入Section 1。**

完成这些收尾后，可以冻结契约并开始Week 1工作。

---

## 逐项修复验证

### 修复1：统一API端点数量

**验证结果：基本解决，但计划文档仍需术语收口。**

契约Section 4现在实际列出5个HTTP路由：

1. `POST /api/auth/login`
2. `POST /api/applications`
3. `GET /api/applications/{application_id}`
4. `POST /api/approvals/{approval_id}/approve`
5. `POST /api/approvals/{approval_id}/reject`

列表端点 `GET /api/applications` 已不在契约中。移除列表端点是合理的，因为v0.1纵向切片只需要“登录 -> 提交 -> 审批 -> 查询单个申请”，不需要审批队列或学生申请列表。

剩余问题是计划文档仍写“4个API端点可用（登录、提交、审批、查询）”。这更像4个核心能力，而不是HTTP路由。建议统一术语：

- HTTP路由：5个
- 核心能力：4个，登录、提交、审批、查询
- Day 3-4新增HTTP路由：4个，不含Day 1-2已完成的login

否则后续验收时仍可能出现“到底是4个还是5个端点”的争议。

### 修复2：添加503 PROVIDER_UNAVAILABLE样例

**验证结果：部分解决。**

契约已经新增503样例，且与宿舍清退外部服务不可用场景匹配：

- `PROVIDER_UNAVAILABLE`
- HTTP 503
- `provider: dorm_checkout`
- timeout细节

这解决了上一轮指出的503缺口。

但Section 3定义了8个错误码，而Section 6.2当前只提供了4类错误样例：401、403、422、503。缺少：

- `VALIDATION_ERROR` 400
- `NOT_FOUND` 404
- `CONFLICT` 409
- `INTERNAL_ERROR` 500

如果v0.1目标是“前端可用mock跑通并处理错误态”，错误样例应至少覆盖Section 3列出的全部错误码。否则前端mock、契约测试和后端异常处理仍会自行发挥。

### 修复3：澄清登录响应DTO

**验证结果：说明清晰，但建议正式定义AuthUserDTO。**

Section 4.1说明 `user` 是 `AuthUserDTO`，是 `UserDTO` 的子集，只包含 `user_id/name/role/class_id`。这解决了“登录响应到底是不是完整UserDTO”的歧义。

仍建议在Section 1加入正式定义：

```python
@dataclass
class AuthUserDTO:
    """登录响应中的用户摘要"""
    user_id: str
    name: str
    role: UserRole
    class_id: Optional[str] = None
```

原因是契约已经命名了 `AuthUserDTO`，但核心DTO章节没有定义它。对后端实现、前端类型生成、契约测试来说，正式定义比正文说明更可靠。

### 修复4：移除矛盾的降级条件

**验证结果：方向正确，但风险表还需要改一句。**

计划已经移除了“申请提交API未完成 -> 只做查询API”的矛盾逻辑，新的方向是优先保留“提交 -> 辅导员审批 -> 查询”最短闭环。这符合纵向切片目标。

但风险表仍写：

> 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批

这里“砍学工部审批”和“Day 4补学工部审批”同时出现，口径冲突。更合理的表达是：

> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。

这样降级条件才真正可执行：先保住最短闭环，不在同一天又承诺补回被砍范围。

---

## 剩余问题与修复建议

### P1：错误样例覆盖不完整

**位置：** `docs/contracts/contract-v0.1.md` Section 3和Section 6.2

**问题：** Section 3定义8个错误码，但错误Mock只覆盖4个。

**影响：** 前端mock、后端异常格式、契约测试无法完整对齐。

**修复建议：** 在Section 6.2补齐400、404、409、500样例。每个样例都保持统一结构：

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "请求参数校验失败",
    "details": {
      "field": "leave_date",
      "reason": "must be YYYY-MM-DD"
    }
  }
}
```

### P1：降级条件仍有口径冲突

**位置：** `docs/plans/week-0-1-execution-plan.md` 风险2

**问题：** 同一句话同时说“砍学工部审批”和“Day 4补学工部审批”。

**影响：** Day 3风险触发后团队不知道是保闭环，还是继续追两级审批。

**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。

### P2：API端点术语仍不够统一

**位置：** `docs/plans/week-0-1-execution-plan.md` Day 3-4交付物、Week 1验收

**问题：** 计划中“4个API端点”实际指4个核心能力或Day 3-4新增HTTP路由，不等于契约的5个HTTP路由。

**影响：** 不一定阻塞实现，但会继续制造验收口径争议。

**修复建议：** 改为：

- Week 0：5个HTTP路由样例
- Day 3-4交付物：4个业务HTTP路由可用，不含登录
- Week 1验收：5个HTTP路由可用，覆盖4个核心能力

### P2：AuthUserDTO应正式定义

**位置：** `docs/contracts/contract-v0.1.md` Section 1

**问题：** Section 4.1引用了 `AuthUserDTO`，但Section 1没有该DTO定义。

**影响：** 对人工阅读影响小，对类型生成和契约测试有轻微歧义。

**修复建议：** 在UserDTO之后添加 `AuthUserDTO`，并调整后续编号。

---

## 可执行性判断

**当前状态：未完全达到可执行契约标准。**

不是因为方向错，而是因为仍有两个会影响执行验收的P1口径缺口：错误样例未全覆盖，降级风险表仍有冲突措辞。它们都属于半天内可以修完的收尾问题。

**修完上述P1后：可以冻结contract-v0.1.md，并开始Week 1 Day 1工作。**

如果团队已经要启动Week 1，也可以先启动不受这些问题影响的Day 1-2工作：Django骨架、基础模型、seed、登录认证。但不建议在P1修完前把契约标记为Final并全面进入Day 3-4业务API实现。

---

## 下一步建议

1. 立即补齐4个缺失错误样例：400、404、409、500。
2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
3. 将计划中的“4个API端点”改成“4个核心能力”或“4个业务HTTP路由”，避免和5个HTTP路由冲突。
4. 在Section 1补 `AuthUserDTO` 正式定义。
5. 完成后可直接冻结v0.1，不需要再开一轮长审查；只需做一次差异核对。


diff --git a/docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md b/docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..5bf33a4f30f13985de504c9e093d98eb4652c6de
--- /dev/null
+++ b/docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
@@ -0,0 +1,190 @@
+# Contract Fixes - Codex Review Response
+
+**审查日期：** 2026-05-30  
+**审查人：** Codex  
+**针对文档：** 47-contract-fixes-review-request.md  
+**审查类型：** 契约修复验证
+
+---
+
+## 审查结论
+
+**结论：尚未完全达到可执行契约标准，但已经非常接近。**
+
+4个修复方向都正确，且主要阻塞点已经明显收敛：契约正文现在只有5个HTTP路由，列表端点已移除；503 `PROVIDER_UNAVAILABLE`样例已补；登录响应的DTO子集问题已说明；原先“申请未完成却只做查询”的降级方向已被替换。
+
+但冻结前仍建议用半天完成3个收尾修正：
+
+1. **P1：错误样例未覆盖Section 3定义的全部错误码。**
+2. **P1：降级方案仍有一句口径冲突，且Day 3提交未完成时的措辞不够可执行。**
+3. **P2：计划文档仍混用“5个HTTP路由”和“4个API端点/能力”的口径；AuthUserDTO最好正式纳入Section 1。**
+
+完成这些收尾后，可以冻结契约并开始Week 1工作。
+
+---
+
+## 逐项修复验证
+
+### 修复1：统一API端点数量
+
+**验证结果：基本解决，但计划文档仍需术语收口。**
+
+契约Section 4现在实际列出5个HTTP路由：
+
+1. `POST /api/auth/login`
+2. `POST /api/applications`
+3. `GET /api/applications/{application_id}`
+4. `POST /api/approvals/{approval_id}/approve`
+5. `POST /api/approvals/{approval_id}/reject`
+
+列表端点 `GET /api/applications` 已不在契约中。移除列表端点是合理的，因为v0.1纵向切片只需要“登录 -> 提交 -> 审批 -> 查询单个申请”，不需要审批队列或学生申请列表。
+
+剩余问题是计划文档仍写“4个API端点可用（登录、提交、审批、查询）”。这更像4个核心能力，而不是HTTP路由。建议统一术语：
+
+- HTTP路由：5个
+- 核心能力：4个，登录、提交、审批、查询
+- Day 3-4新增HTTP路由：4个，不含Day 1-2已完成的login
+
+否则后续验收时仍可能出现“到底是4个还是5个端点”的争议。
+
+### 修复2：添加503 PROVIDER_UNAVAILABLE样例
+
+**验证结果：部分解决。**
+
+契约已经新增503样例，且与宿舍清退外部服务不可用场景匹配：
+
+- `PROVIDER_UNAVAILABLE`
+- HTTP 503
+- `provider: dorm_checkout`
+- timeout细节
+
+这解决了上一轮指出的503缺口。
+
+但Section 3定义了8个错误码，而Section 6.2当前只提供了4类错误样例：401、403、422、503。缺少：
+
+- `VALIDATION_ERROR` 400
+- `NOT_FOUND` 404
+- `CONFLICT` 409
+- `INTERNAL_ERROR` 500
+
+如果v0.1目标是“前端可用mock跑通并处理错误态”，错误样例应至少覆盖Section 3列出的全部错误码。否则前端mock、契约测试和后端异常处理仍会自行发挥。
+
+### 修复3：澄清登录响应DTO
+
+**验证结果：说明清晰，但建议正式定义AuthUserDTO。**
+
+Section 4.1说明 `user` 是 `AuthUserDTO`，是 `UserDTO` 的子集，只包含 `user_id/name/role/class_id`。这解决了“登录响应到底是不是完整UserDTO”的歧义。
+
+仍建议在Section 1加入正式定义：
+
+```python
+@dataclass
+class AuthUserDTO:
+    """登录响应中的用户摘要"""
+    user_id: str
+    name: str
+    role: UserRole
+    class_id: Optional[str] = None
+```
+
+原因是契约已经命名了 `AuthUserDTO`，但核心DTO章节没有定义它。对后端实现、前端类型生成、契约测试来说，正式定义比正文说明更可靠。
+
+### 修复4：移除矛盾的降级条件
+
+**验证结果：方向正确，但风险表还需要改一句。**
+
+计划已经移除了“申请提交API未完成 -> 只做查询API”的矛盾逻辑，新的方向是优先保留“提交 -> 辅导员审批 -> 查询”最短闭环。这符合纵向切片目标。
+
+但风险表仍写：
+
+> 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
+
+这里“砍学工部审批”和“Day 4补学工部审批”同时出现，口径冲突。更合理的表达是：
+
+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
+
+这样降级条件才真正可执行：先保住最短闭环，不在同一天又承诺补回被砍范围。
+
+---
+
+## 剩余问题与修复建议
+
+### P1：错误样例覆盖不完整
+
+**位置：** `docs/contracts/contract-v0.1.md` Section 3和Section 6.2
+
+**问题：** Section 3定义8个错误码，但错误Mock只覆盖4个。
+
+**影响：** 前端mock、后端异常格式、契约测试无法完整对齐。
+
+**修复建议：** 在Section 6.2补齐400、404、409、500样例。每个样例都保持统一结构：
+
+```json
+{
+  "error": {
+    "code": "VALIDATION_ERROR",
+    "message": "请求参数校验失败",
+    "details": {
+      "field": "leave_date",
+      "reason": "must be YYYY-MM-DD"
+    }
+  }
+}
+```
+
+### P1：降级条件仍有口径冲突
+
+**位置：** `docs/plans/week-0-1-execution-plan.md` 风险2
+
+**问题：** 同一句话同时说“砍学工部审批”和“Day 4补学工部审批”。
+
+**影响：** Day 3风险触发后团队不知道是保闭环，还是继续追两级审批。
+
+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
+
+### P2：API端点术语仍不够统一
+
+**位置：** `docs/plans/week-0-1-execution-plan.md` Day 3-4交付物、Week 1验收
+
+**问题：** 计划中“4个API端点”实际指4个核心能力或Day 3-4新增HTTP路由，不等于契约的5个HTTP路由。
+
+**影响：** 不一定阻塞实现，但会继续制造验收口径争议。
+
+**修复建议：** 改为：
+
+- Week 0：5个HTTP路由样例
+- Day 3-4交付物：4个业务HTTP路由可用，不含登录
+- Week 1验收：5个HTTP路由可用，覆盖4个核心能力
+
+### P2：AuthUserDTO应正式定义
+
+**位置：** `docs/contracts/contract-v0.1.md` Section 1
+
+**问题：** Section 4.1引用了 `AuthUserDTO`，但Section 1没有该DTO定义。
+
+**影响：** 对人工阅读影响小，对类型生成和契约测试有轻微歧义。
+
+**修复建议：** 在UserDTO之后添加 `AuthUserDTO`，并调整后续编号。
+
+---
+
+## 可执行性判断
+
+**当前状态：未完全达到可执行契约标准。**
+
+不是因为方向错，而是因为仍有两个会影响执行验收的P1口径缺口：错误样例未全覆盖，降级风险表仍有冲突措辞。它们都属于半天内可以修完的收尾问题。
+
+**修完上述P1后：可以冻结contract-v0.1.md，并开始Week 1 Day 1工作。**
+
+如果团队已经要启动Week 1，也可以先启动不受这些问题影响的Day 1-2工作：Django骨架、基础模型、seed、登录认证。但不建议在P1修完前把契约标记为Final并全面进入Day 3-4业务API实现。
+
+---
+
+## 下一步建议
+
+1. 立即补齐4个缺失错误样例：400、404、409、500。
+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
+3. 将计划中的“4个API端点”改成“4个核心能力”或“4个业务HTTP路由”，避免和5个HTTP路由冲突。
+4. 在Section 1补 `AuthUserDTO` 正式定义。
+5. 完成后可直接冻结v0.1，不需要再开一轮长审查；只需做一次差异核对。
+

codex
已完成批判性审查，并按项目流程写入：

[49-contract-fixes-codex-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md)

结论：**尚未完全达到可执行契约标准，但非常接近**。4 个修复方向都正确，主要阻塞点已基本解决；但冻结前还应修 2 个 P1 和 2 个 P2：

- **P1**：错误样例未覆盖 Section 3 的全部错误码，缺 400、404、409、500。
- **P1**：风险表里仍同时写“砍学工部审批”和“Day 4补学工部审批”，降级口径冲突。
- **P2**：计划中仍混用“5个HTTP路由”和“4个API端点/能力”。
- **P2**：`AuthUserDTO` 已被引用，但未在 Section 1 正式定义。

明确回答：**现在还不建议冻结契约并全面开始 Week 1 Day 3-4 业务 API 实现**。可以先启动不受影响的 Week 1 Day 1-2：Django 骨架、模型、seed、登录认证。修完上述 P1 后，可以冻结 `contract-v0.1.md` 并开始 Week 1 工作。
diff --git a/docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md b/docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..5bf33a4f30f13985de504c9e093d98eb4652c6de
--- /dev/null
+++ b/docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
@@ -0,0 +1,190 @@
+# Contract Fixes - Codex Review Response
+
+**审查日期：** 2026-05-30  
+**审查人：** Codex  
+**针对文档：** 47-contract-fixes-review-request.md  
+**审查类型：** 契约修复验证
+
+---
+
+## 审查结论
+
+**结论：尚未完全达到可执行契约标准，但已经非常接近。**
+
+4个修复方向都正确，且主要阻塞点已经明显收敛：契约正文现在只有5个HTTP路由，列表端点已移除；503 `PROVIDER_UNAVAILABLE`样例已补；登录响应的DTO子集问题已说明；原先“申请未完成却只做查询”的降级方向已被替换。
+
+但冻结前仍建议用半天完成3个收尾修正：
+
+1. **P1：错误样例未覆盖Section 3定义的全部错误码。**
+2. **P1：降级方案仍有一句口径冲突，且Day 3提交未完成时的措辞不够可执行。**
+3. **P2：计划文档仍混用“5个HTTP路由”和“4个API端点/能力”的口径；AuthUserDTO最好正式纳入Section 1。**
+
+完成这些收尾后，可以冻结契约并开始Week 1工作。
+
+---
+
+## 逐项修复验证
+
+### 修复1：统一API端点数量
+
+**验证结果：基本解决，但计划文档仍需术语收口。**
+
+契约Section 4现在实际列出5个HTTP路由：
+
+1. `POST /api/auth/login`
+2. `POST /api/applications`
+3. `GET /api/applications/{application_id}`
+4. `POST /api/approvals/{approval_id}/approve`
+5. `POST /api/approvals/{approval_id}/reject`
+
+列表端点 `GET /api/applications` 已不在契约中。移除列表端点是合理的，因为v0.1纵向切片只需要“登录 -> 提交 -> 审批 -> 查询单个申请”，不需要审批队列或学生申请列表。
+
+剩余问题是计划文档仍写“4个API端点可用（登录、提交、审批、查询）”。这更像4个核心能力，而不是HTTP路由。建议统一术语：
+
+- HTTP路由：5个
+- 核心能力：4个，登录、提交、审批、查询
+- Day 3-4新增HTTP路由：4个，不含Day 1-2已完成的login
+
+否则后续验收时仍可能出现“到底是4个还是5个端点”的争议。
+
+### 修复2：添加503 PROVIDER_UNAVAILABLE样例
+
+**验证结果：部分解决。**
+
+契约已经新增503样例，且与宿舍清退外部服务不可用场景匹配：
+
+- `PROVIDER_UNAVAILABLE`
+- HTTP 503
+- `provider: dorm_checkout`
+- timeout细节
+
+这解决了上一轮指出的503缺口。
+
+但Section 3定义了8个错误码，而Section 6.2当前只提供了4类错误样例：401、403、422、503。缺少：
+
+- `VALIDATION_ERROR` 400
+- `NOT_FOUND` 404
+- `CONFLICT` 409
+- `INTERNAL_ERROR` 500
+
+如果v0.1目标是“前端可用mock跑通并处理错误态”，错误样例应至少覆盖Section 3列出的全部错误码。否则前端mock、契约测试和后端异常处理仍会自行发挥。
+
+### 修复3：澄清登录响应DTO
+
+**验证结果：说明清晰，但建议正式定义AuthUserDTO。**
+
+Section 4.1说明 `user` 是 `AuthUserDTO`，是 `UserDTO` 的子集，只包含 `user_id/name/role/class_id`。这解决了“登录响应到底是不是完整UserDTO”的歧义。
+
+仍建议在Section 1加入正式定义：
+
+```python
+@dataclass
+class AuthUserDTO:
+    """登录响应中的用户摘要"""
+    user_id: str
+    name: str
+    role: UserRole
+    class_id: Optional[str] = None
+```
+
+原因是契约已经命名了 `AuthUserDTO`，但核心DTO章节没有定义它。对后端实现、前端类型生成、契约测试来说，正式定义比正文说明更可靠。
+
+### 修复4：移除矛盾的降级条件
+
+**验证结果：方向正确，但风险表还需要改一句。**
+
+计划已经移除了“申请提交API未完成 -> 只做查询API”的矛盾逻辑，新的方向是优先保留“提交 -> 辅导员审批 -> 查询”最短闭环。这符合纵向切片目标。
+
+但风险表仍写：
+
+> 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
+
+这里“砍学工部审批”和“Day 4补学工部审批”同时出现，口径冲突。更合理的表达是：
+
+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
+
+这样降级条件才真正可执行：先保住最短闭环，不在同一天又承诺补回被砍范围。
+
+---
+
+## 剩余问题与修复建议
+
+### P1：错误样例覆盖不完整
+
+**位置：** `docs/contracts/contract-v0.1.md` Section 3和Section 6.2
+
+**问题：** Section 3定义8个错误码，但错误Mock只覆盖4个。
+
+**影响：** 前端mock、后端异常格式、契约测试无法完整对齐。
+
+**修复建议：** 在Section 6.2补齐400、404、409、500样例。每个样例都保持统一结构：
+
+```json
+{
+  "error": {
+    "code": "VALIDATION_ERROR",
+    "message": "请求参数校验失败",
+    "details": {
+      "field": "leave_date",
+      "reason": "must be YYYY-MM-DD"
+    }
+  }
+}
+```
+
+### P1：降级条件仍有口径冲突
+
+**位置：** `docs/plans/week-0-1-execution-plan.md` 风险2
+
+**问题：** 同一句话同时说“砍学工部审批”和“Day 4补学工部审批”。
+
+**影响：** Day 3风险触发后团队不知道是保闭环，还是继续追两级审批。
+
+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
+
+### P2：API端点术语仍不够统一
+
+**位置：** `docs/plans/week-0-1-execution-plan.md` Day 3-4交付物、Week 1验收
+
+**问题：** 计划中“4个API端点”实际指4个核心能力或Day 3-4新增HTTP路由，不等于契约的5个HTTP路由。
+
+**影响：** 不一定阻塞实现，但会继续制造验收口径争议。
+
+**修复建议：** 改为：
+
+- Week 0：5个HTTP路由样例
+- Day 3-4交付物：4个业务HTTP路由可用，不含登录
+- Week 1验收：5个HTTP路由可用，覆盖4个核心能力
+
+### P2：AuthUserDTO应正式定义
+
+**位置：** `docs/contracts/contract-v0.1.md` Section 1
+
+**问题：** Section 4.1引用了 `AuthUserDTO`，但Section 1没有该DTO定义。
+
+**影响：** 对人工阅读影响小，对类型生成和契约测试有轻微歧义。
+
+**修复建议：** 在UserDTO之后添加 `AuthUserDTO`，并调整后续编号。
+
+---
+
+## 可执行性判断
+
+**当前状态：未完全达到可执行契约标准。**
+
+不是因为方向错，而是因为仍有两个会影响执行验收的P1口径缺口：错误样例未全覆盖，降级风险表仍有冲突措辞。它们都属于半天内可以修完的收尾问题。
+
+**修完上述P1后：可以冻结contract-v0.1.md，并开始Week 1 Day 1工作。**
+
+如果团队已经要启动Week 1，也可以先启动不受这些问题影响的Day 1-2工作：Django骨架、基础模型、seed、登录认证。但不建议在P1修完前把契约标记为Final并全面进入Day 3-4业务API实现。
+
+---
+
+## 下一步建议
+
+1. 立即补齐4个缺失错误样例：400、404、409、500。
+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
+3. 将计划中的“4个API端点”改成“4个核心能力”或“4个业务HTTP路由”，避免和5个HTTP路由冲突。
+4. 在Section 1补 `AuthUserDTO` 正式定义。
+5. 完成后可直接冻结v0.1，不需要再开一轮长审查；只需做一次差异核对。
+

tokens used
58,503

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
