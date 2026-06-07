# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-05T05:14:23.459Z

## Original task

审查 docs/用户需求最终确认与实施方案.md

审查要点（详见 .omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md）:
1. 业务逻辑完整性 - 5项决策一致性，2级审批可行性
2. 技术可行性 - 变更工作量，路由改造风险  
3. 数据一致性 - File1-5关联，名称规范化
4. 实施风险 - Phase顺序，回滚策略

输出格式：
- 评分（满分40）
- P0/P1/P2问题清单
- 修正建议

## Final prompt

审查 docs/用户需求最终确认与实施方案.md

审查要点（详见 .omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md）:
1. 业务逻辑完整性 - 5项决策一致性，2级审批可行性
2. 技术可行性 - 变更工作量，路由改造风险  
3. 数据一致性 - File1-5关联，名称规范化
4. 实施风险 - Phase顺序，回滚策略

输出格式：
- 评分（满分40）
- P0/P1/P2问题清单
- 修正建议

## Raw output

```text
已完成审查，并写入 artifact：[20260605-codex-implementation-plan-review.md](/home/caohui/projects/graduation-leave-system/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md)。协作任务状态已置为 `completed`。

**评分**
| 维度 | 分数 |
|---|---:|
| 业务逻辑完整性 | 7/10 |
| 技术可行性 | 5/10 |
| 数据一致性 | 6/10 |
| 实施风险控制 | 4/10 |
| **总分** | **22/40** |

**结论：需要修改后再实施。** 方案方向正确，但不能按“所有 P0 已解除、2.5-3 天完成”直接推进。

**P0 问题**
1. 空学号学生无法导入：方案允许 `user_id` 为空，但现有 `User.user_id` 是主键且创建用户要求非空。
2. “任一宿管员可审批”与当前单审批人 `Approval.approver` 模型冲突，必须先定义唯一主责人或改造为多人待办模型。
3. `ClassMapping` 移除范围被低估；提交申请、审批流转、详情权限都直接依赖它。

**P1 问题**
1. File1/File2 差异口径不一致：`155`、`271研究生`、`116 File2独有` 的关系需要重新写清。
2. 状态机名称与现有代码不一致，现有是 `pending_dorm_manager/pending_counselor/pending_dean/approved`。
3. 新 `admin` 与既有 `dean` 角色关系未定义。
4. 路由键缺少申请时快照，后续学院/楼栋/人员变更会影响历史审计。
5. 学院和楼栋规范化只有示例，没有完整字典、冲突规则和阻断标准。
6. 数据导入命令与现有 `import_csv` 不一致，现有命令仍要求 `class_id` 和 `ClassMapping`。
7. 2.5-3 天估算偏乐观。
8. 风险章节缺少备份、dry-run、导入批次回滚和迁移失败回滚方案。

**P2 建议**
1. 明确 frontend、miniprogram、demo-web 是否都要同步。
2. 增加负向权限测试：跨楼栋、跨学院、管理员不可审批、学生不可看审批列表。
3. 寝室号精确路由建议用独立映射表，不建议长期使用 JSONField。
4. 通知文案同步移除“学工部审批”。
5. API 文档和 TypeScript 类型应列入交付物。

**修正建议**
先增加 Phase 0：数据画像和路由门禁。必须输出 File1/File2 匹配报告、完整学院/楼栋规范化字典、缺学号账号生成策略、5830 人逐条宿管和辅导员路由结果。

MVP 建议把楼栋多宿管员收敛为“每栋楼唯一主责宿管员”，后续再做代理或多人队列。然后重排实施为：数据门禁 → 后端模型/路由/权限 → 导入 dry-run/真实导入 → 前端和 API 类型同步 → 端到端权限回归 → 备份与回滚演练。


OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019e9630-67b7-7b43-9c9b-d61999620dfe
--------
user
审查 docs/用户需求最终确认与实施方案.md

审查要点（详见 .omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md）:
1. 业务逻辑完整性 - 5项决策一致性，2级审批可行性
2. 技术可行性 - 变更工作量，路由改造风险  
3. 数据一致性 - File1-5关联，名称规范化
4. 实施风险 - Phase顺序，回滚策略

输出格式：
- 评分（满分40）
- P0/P1/P2问题清单
- 修正建议
codex
我会先读取项目规则和评审协议，再打开实施方案与任务说明，按指定四个审查维度给出问题分级和评分。
exec
/bin/bash -lc "sed -n '1,260p' docs/codex-review-protocol.md" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "sed -n '1,240p' .omc/collaboration/protocol.md" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "pwd && sed -n '1,220p' /home/caohui/.codex/RTK.md" in /home/caohui/projects/graduation-leave-system
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

codex
规则里要求本项目所有 shell 命令通过 `rtk` 执行。我刚才读规则前的初始探测没有加前缀；后续命令会按项目规则走，并按协作协议先检查任务与日志状态。
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/用户需求最终确认与实施方案.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 用户需求最终确认与实施方案

**确认日期：** 2026-06-05  
**文档类型：** 业务需求最终确认  
**背景：** Excel数据源关联策略协作完成后，用户提供关键业务决策  
**状态：** 所有P0阻塞已解除，可开始实施

---

## 数据文件映射说明

本文档中引用的文件编号与实际文件对应关系：

| 文件编号 | 实际文件名 | 内容说明 | 行数/记录数 |
|---------|-----------|---------|-----------|
| **File 1** | `1-5830名毕业生（含研究生）.xls` | 学生基准数据（含研究生） | 5830行 |
| **File 2** | `2026届预计毕业生5675人.xlsx` | 学生补充数据（含学号） | 5675行 |
| **File 3** | `2026年社区辅导员信息统计表.xls` | 宿管员数据（按楼栋） | 33楼栋 |
| **File 4** | `2026年学院辅导员信息统计表.xls` | 辅导员数据（按学院） | 19学院 |
| **File 5** | `file5_students_5830.csv` | 合并输出文件（File1+File2） | 5830行 |

**说明：** File 5 是数据处理脚本的输出结果，不是原始输入文件。

---

## 一、用户确认的5项关键决策

### 决策1: 数据合并策略

**用户原文：**
> "以文件1学生数据为基准，文件2学生数据作为字段补充，文件2中没有的数据，在文件1中暂时设定为空"

**解读：**
- File1 (5830行) 作为基准数据
- File2 (5675行) 补充学号(XH)、班号(BH)等字段
- File2没有的155行学生（差异部分）：补充字段留空
- 271行研究生：补充字段留空（File2无研究生数据）

**影响：**
- ✓ 解决了"271研究生+116 File2独有学生"问题
- ✓ 全部5830行学生可导入
- ✓ 无需纠结匹配失败记录处理

### 决策2: 班级字段处理

**用户原文：**
> "班级数据先设置为空"

**解读：**
- `class_id` 字段可为空
- 不需要立即解决班级映射问题
- 审批流程不依赖班级字段

**影响：**
- ✓ 移除ClassMapping复杂度
- ✓ 简化数据导入流程
- ✓ 避免班级辅导员映射争议

### 决策3: 审批流程调整（重大变更）

**用户原文：**
> "第一次审批按楼栋数据向宿管员申请，第一次审批通过后，再按学院向辅导员发起第二次审批"

**当前系统设计：**
```
学生提交 → 宿管员审批(by class_id) → 辅导员审批(by class_id) → 学工部审批 → 完成
```

**新需求：**
```
学生提交 → 宿管员审批(by 楼栋) → 辅导员审批(by 学院) → 完成（保存结果）
```

**关键变更：**
- 移除学工部（dean）审批环节
- 路由方式从 `class_id` 改为 `building` + `college`
- 审批级数：3级 → 2级

**影响：**
- ⚠️ 需要修改审批流程状态机
- ⚠️ 需要修改路由逻辑
- ✓ 简化审批流程
- ✓ 解决"楼栋跨班级"问题

### 决策4: 数据持久化要求

**用户原文：**
> "二次审批完成后，将流程与审批结果数据进行保存"

**解读：**
- 保存完整审批流程记录
- 保存每次审批结果（通过/驳回/意见）
- 支持审批历史查询

**影响：**
- ✓ 当前系统已支持（Application + Approval模型）

### 决策5: 新增学工管理员角色

**用户原文：**
> "学工管理员数据没有添加，但要保留。学工管理员不做审批，但要能查看学生离校审批的整体情况"

**4类用户定义：**

| 角色 | 职责 | 权限范围 |
|------|------|----------|
| 学生 (student) | 提交离校申请 | 查看自己的申请 |
| 宿管员 (dorm_manager) | 第一次审批（按楼栋） | 只看自己负责楼栋的申请 |
| 辅导员 (counselor) | 第二次审批（按学院） | 只看自己负责学院的申请 |
| 学工管理员 (admin) | 查看全局数据 | 查看所有申请，但无审批权限 |

**影响：**
- 需要新增 `admin` 角色
- 需要全局视图界面
- 学工管理员数据后续提供（Excel/CSV格式）

---

## 二、补充确认：寝室号字段

### 确认1: 楼栋审批关系

**用户原文：**
> "楼栋按文件5与文件3中共同的楼栋字段为审批关系设定"

**解读：**
- File5 (学生).楼栋名称 ↔ File3 (宿管员).楼栋号
- 匹配规则：字符串精确匹配或规范化后匹配
- 一个楼栋对应多个宿管员：任一人可审批（待确认）

### 确认2: 寝室号未来补充

**用户原文：**
> "文件5的数据中应该有寝室号字段，文件3中没有，后面会再确认提交文件3的寝室号字段数据，以形成单一对应关系"

**当前情况：**
- File5 (学生) 有：楼栋名称 + 寝室号 ✓
- File3 (宿管员) 有：楼栋号 ✓，无寝室号 ✗

**未来升级：**
- File3 补充寝室号字段
- 路由升级：楼栋级（一对多）→ 楼栋+寝室号级（一对一）

**实施策略：**
- **Phase 1（当前）：** 按楼栋路由（building-level）
- **Phase 2（File3补充后）：** 按楼栋+寝室号路由（room-level，精确一对一）

---

## 三、P0阻塞问题解决情况

### Codex审查识别的P0问题

| 问题 | Codex评估 | 用户决策 | 解决状态 |
|------|-----------|----------|----------|
| 学生数据无法关联 | ⚠️ 需增强匹配规则 | 决策1：File1为基准 | ✅ 已解除 |
| 研究生缺学号/班级 | ❌ 271行缺失 | 决策1：字段留空 | ✅ 已解除 |
| 班级字段缺失 | ⚠️ File1有，File2格式不同 | 决策2：暂时为空 | ✅ 已解除 |
| ClassMapping缺失 | ❌ 辅导员无班级映射 | 决策3：改为学院级 | ✅ 已解除 |
| 楼栋→宿管员一对多 | ⚠️ 无法确定选主规则 | 决策3：楼栋级路由 | ✅ 已解除 |
| 辅导员学院级降级 | ⚠️ 需业务确认 | 决策3：确认接受 | ✅ 已解除 |

**结论：所有P0阻塞已通过用户业务决策解除。**

---

## 四、系统设计变更需求

### 4.1 数据模型调整

**Student (用户表 - 学生角色)：**
```python
# 必填字段
user_id        # 学号（File2补充，可能为空）
name           # 姓名（File1）
role = 'student'

# 核心字段
building_name  # 楼栋名称（File1） - 第一次审批路由键
room_number    # 寝室号（File1） - 未来精确路由键
department     # 学院名称（File1规范化） - 第二次审批路由键
class_id       # 班级（可为空） - 不用于路由

# 补充字段（可空）
major          # 专业（File1）
grade          # 年级（File1）
phone          # 手机号（File2补充）
email          # 邮箱（File2补充）
```

**DormManager (用户表 - 宿管员角色)：**
```python
user_id        # 工号（File3）
name           # 姓名（File3）
role = 'dorm_manager'
building       # 负责楼栋（File3）
room_numbers   # 负责寝室号列表（未来File3补充）
phone          # 手机号（File3）
```

**Counselor (用户表 - 辅导员角色)：**
```python
user_id        # 工号（File4）
name           # 姓名（File4）
role = 'counselor'
department     # 负责学院（File4）
phone          # 手机号（File4）
```

**Admin (用户表 - 学工管理员角色)：**
```python
user_id        # 工号（未来提供）
name           # 姓名（未来提供）
role = 'admin'
# 无业务范围限制，可查看全部
```

### 4.2 审批流程变更

**当前流程（3级）：**
```python
PENDING → DORM_MANAGER_APPROVED → COUNSELOR_APPROVED → DEAN_APPROVED → COMPLETED
```

**新流程（2级）：**
```python
PENDING → DORM_MANAGER_APPROVED → COUNSELOR_APPROVED → COMPLETED
```

**状态定义：**
- `PENDING`: 学生已提交，等待宿管员审批
- `DORM_MANAGER_APPROVED`: 宿管员已通过，等待辅导员审批
- `COUNSELOR_APPROVED`: 辅导员已通过，流程完成
- `REJECTED`: 任一环节驳回

### 4.3 路由逻辑变更

**当前路由（基于ClassMapping）：**
```python
def get_approver(application):
    class_mapping = ClassMapping.objects.get(class_id=application.student.class_id)
    if application.status == 'PENDING':
        return class_mapping.dorm_manager
    elif application.status == 'DORM_MANAGER_APPROVED':
        return class_mapping.counselor
```

**新路由（基于Building + Department）：**
```python
def get_approver(application):
    if application.status == 'PENDING':
        # 第一次审批：按楼栋查宿管员
        building = application.student.building_name
        dorm_managers = DormManager.objects.filter(building=building)
        return dorm_managers  # 任一可审批，或按选主规则
    
    elif application.status == 'DORM_MANAGER_APPROVED':
        # 第二次审批：按学院查辅导员
        department = application.student.department
        counselor = Counselor.objects.get(department=department)

exec
/bin/bash -lc 'rtk tail -n 80 .omc/collaboration/events.jsonl' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{"id":1,"type":"workflow_initialized","agent":"claude","timestamp":"2026-06-05T05:10:00.000Z","summary":"Initialize implementation-plan-review workflow","status":"initialized"}
{"id":2,"type":"task_created","agent":"claude","timestamp":"2026-06-05T05:10:10.000Z","task_id":"TASK-20260605-03","summary":"Review implementation plan document","artifacts":["tasks/TASK-20260605-03-implementation-plan-review.md"]}
{"id":3,"type":"handoff_requested","agent":"claude","timestamp":"2026-06-05T05:10:20.000Z","task_id":"TASK-20260605-03","target_agent":"codex","summary":"Request Codex review of implementation plan"}

exec
/bin/bash -lc "rtk sed -n '1,200p' .omc/collaboration/state.json" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{
  "workflow_id": "implementation-plan-review",
  "current_task": "TASK-20260605-03",
  "active_agent": "codex",
  "status": "handoff_pending",
  "last_event_id": 3,
  "updated_at": "2026-06-05T05:10:20.000Z"
}

exec
/bin/bash -lc "rtk sed -n '1,260p' .omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 实施方案审查请求

**任务ID:** TASK-20260605-03  
**创建时间:** 2026-06-05T05:05:00Z  
**审查对象:** 用户需求最终确认与实施方案文档  
**审查目标:** 验证业务逻辑完整性、技术可行性、数据一致性

---

## 审查范围

**文档路径:** `docs/用户需求最终确认与实施方案.md`

**文档内容概述:**
- 用户5项关键业务决策（数据合并、班级字段、审批流程、管理员角色、寝室号）
- 系统设计变更需求（数据模型、审批流程、路由逻辑、权限控制）
- 5阶段实施方案（数据准备、系统调整、数据导入、前端调整、测试验证）
- 风险与缓解措施
- 未来升级路径（寝室号精确路由）

---

## 审查要点

### 1. 业务逻辑完整性

**核心问题:**
- 用户5项决策是否相互一致？是否存在矛盾？
- 2级审批流程（楼栋→学院）是否满足实际业务需求？
- 4类用户角色（学生/宿管员/辅导员/管理员）权限划分是否合理？
- ClassMapping移除后的路由方案（Building + Department）是否可行？

**具体检查项:**
- [ ] File1+File2合并策略：5830行基准是否覆盖所有必需学生？
- [ ] 楼栋路由：一对多问题（一个楼栋多个宿管员）是否有明确规则？
- [ ] 学院路由：辅导员按学院级审批（非班级级）是否符合业务预期？
- [ ] 管理员角色：只读全局权限定义是否完整？

### 2. 技术可行性

**核心问题:**
- 审批流程从3级改为2级的系统变更工作量是否合理？
- 路由逻辑从ClassMapping改为Building+Department是否存在技术风险？
- class_id字段从必填改为可选是否会影响现有代码？
- 2.5-3天实施时间是否现实？

**具体检查项:**
- [ ] 数据模型调整：Student/DormManager/Counselor/Admin字段定义是否完整？
- [ ] 状态机修改：PENDING→DORM_MANAGER_APPROVED→COUNSELOR_APPROVED是否遗漏边界状态？
- [ ] 前端界面区分：4类用户界面是否需要新增大量页面？
- [ ] 权限控制：现有RBAC系统是否需要重构？

### 3. 数据一致性

**核心问题:**
- File1、File2、File3、File4之间的数据关联是否清晰？
- 学院名称规范化映射是否会遗漏或冲突？
- 楼栋名称匹配（File1 vs File3）是否存在格式不一致风险？
- 5830行学生是否都能成功路由到宿管员和辅导员？

**具体检查项:**
- [ ] 文件映射表：File 1-5的实际文件名和内容说明是否准确？
- [ ] 字段覆盖：File1+File2合并后所有必需字段是否完整？
- [ ] 路由验证：导入前门禁（每个学生必须能找到宿管员+辅导员）是否充分？
- [ ] 数据质量：271行研究生、155行差异学生的处理是否会导致业务中断？

### 4. 实施风险

**核心问题:**
- Phase 1-5的实施顺序是否合理？是否存在前后依赖未明确的风险？
- 风险缓解措施（楼栋名称不匹配、多宿管员选择、管理员界面延后）是否充分？
- 未来升级路径（寝室号精确路由）与当前实施是否存在架构冲突？

**具体检查项:**
- [ ] Phase顺序：数据准备→系统调整→数据导入的顺序是否会导致测试困难？
- [ ] 回滚策略：如果实施失败，是否有回滚方案？
- [ ] 增量部署：是否可以分阶段部署而非一次性全量变更？

---

## 期望输出

### 评估格式

**评分维度（满分10分）:**
- 业务逻辑完整性: _/10
- 技术可行性: _/10
- 数据一致性: _/10
- 实施风险控制: _/10
- **总分:** _/40

### 问题分级

- **P0（阻塞性）:** 不解决无法开始实施，必须立即修正
- **P1（主要）:** 实施前必须解决，否则高概率失败
- **P2（改进）:** 建议优化，但不阻塞实施

### 审查输出结构

```markdown
## 审查结论

【总体评分】

## P0问题清单

1. 【问题描述】
   - 影响范围：
   - 建议修正：

## P1问题清单

## P2建议清单

## 补充建议

【针对实施方案的优化建议】
```

---

## 后续行动

**审查通过后:**
1. Claude根据Codex反馈修正文档和实施方案
2. 创建Phase 1数据准备脚本（学院规范化+文件合并）
3. 执行数据准备并生成File 5
4. 开始Phase 2系统代码调整

**审查未通过（存在P0问题）:**
1. 与用户确认P0问题的业务决策
2. 根据用户反馈修正方案
3. 重新提交审查

---

**请Codex审查上述文档，识别所有P0/P1/P2问题，提供评分和修正建议。**

codex
任务日志当前是 Claude 发起并交给 Codex，状态为 `handoff_pending`。我会按协议原子认领任务并更新协作状态，然后继续做文档审查。
exec
/bin/bash -lc "rtk node -e \"const fs=require('fs'); const path='.omc/collaboration'; const lock=path+'/locks/journal.lock'; const task='TASK-20260605-03'; const now=new Date().toISOString(); fs.mkdirSync(lock); let done=false; try { fs.writeFileSync(lock+'/owner.json', JSON.stringify({agent:'codex',task_id:task,created_at:now,heartbeat_at:now,reason:'claim implementation plan review'}, null, 2)); const eventsPath=path+'/events.jsonl'; const raw=fs.existsSync(eventsPath)?fs.readFileSync(eventsPath,'utf8').trim():''; const events=raw?raw.split(/\\n/).map((line,i)=>{try{return JSON.parse(line)}catch(e){throw new Error('Malformed events.jsonl line '+(i+1)+': '+e.message)}}):[]; const ids=new Set(); for (const e of events) { if (ids.has(e.id)) throw new Error('Duplicate event id '+e.id); ids.add(e.id); } const activeStates=new Set(['claimed','in_progress','waiting','blocked','timeout_candidate']); const active=events.filter(e=>e.task_id===task && activeStates.has(e.status)).at(-1); if (active) throw new Error('Task already active: '+JSON.stringify(active)); const id=events.reduce((m,e)=>Math.max(m, Number(e.id)||0),0)+1; const ev={id,type:'task_claimed',agent:'codex',timestamp:now,task_id:task,summary:'Codex claimed implementation plan review task',status:'in_progress'}; fs.appendFileSync(eventsPath, JSON.stringify(ev)+'\\n'); const state={workflow_id:'implementation-plan-review',current_task:task,active_agent:'codex',status:'in_progress',last_event_id:id,updated_at:now}; const tmp=path+'/state.json.tmp.codex'; fs.writeFileSync(tmp, JSON.stringify(state,null,2)+'\\n'); JSON.parse(fs.readFileSync(tmp,'utf8')); fs.renameSync(tmp,path+'/state.json'); const checkRaw=fs.readFileSync(eventsPath,'utf8').trim(); const checkEvents=checkRaw?checkRaw.split(/\\n/).map(JSON.parse):[]; const maxId=checkEvents.reduce((m,e)=>Math.max(m, Number(e.id)||0),0); const st=JSON.parse(fs.readFileSync(path+'/state.json','utf8')); if (st.last_event_id"'!==maxId) throw new Error('"'state last_event_id mismatch'); done=true; } finally { try { fs.rmSync(lock,{recursive:true,force:true}); } catch(e) {} }\"" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
codex
任务已认领。现在我会补齐实施方案全文，并快速查看现有后端模型、审批状态和前端路由相关代码，这样评分不会只停留在文档表面。
exec
/bin/bash -lc "rtk sed -n '180,420p' docs/用户需求最终确认与实施方案.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
room_number    # 寝室号（File1） - 未来精确路由键
department     # 学院名称（File1规范化） - 第二次审批路由键
class_id       # 班级（可为空） - 不用于路由

# 补充字段（可空）
major          # 专业（File1）
grade          # 年级（File1）
phone          # 手机号（File2补充）
email          # 邮箱（File2补充）
```

**DormManager (用户表 - 宿管员角色)：**
```python
user_id        # 工号（File3）
name           # 姓名（File3）
role = 'dorm_manager'
building       # 负责楼栋（File3）
room_numbers   # 负责寝室号列表（未来File3补充）
phone          # 手机号（File3）
```

**Counselor (用户表 - 辅导员角色)：**
```python
user_id        # 工号（File4）
name           # 姓名（File4）
role = 'counselor'
department     # 负责学院（File4）
phone          # 手机号（File4）
```

**Admin (用户表 - 学工管理员角色)：**
```python
user_id        # 工号（未来提供）
name           # 姓名（未来提供）
role = 'admin'
# 无业务范围限制，可查看全部
```

### 4.2 审批流程变更

**当前流程（3级）：**
```python
PENDING → DORM_MANAGER_APPROVED → COUNSELOR_APPROVED → DEAN_APPROVED → COMPLETED
```

**新流程（2级）：**
```python
PENDING → DORM_MANAGER_APPROVED → COUNSELOR_APPROVED → COMPLETED
```

**状态定义：**
- `PENDING`: 学生已提交，等待宿管员审批
- `DORM_MANAGER_APPROVED`: 宿管员已通过，等待辅导员审批
- `COUNSELOR_APPROVED`: 辅导员已通过，流程完成
- `REJECTED`: 任一环节驳回

### 4.3 路由逻辑变更

**当前路由（基于ClassMapping）：**
```python
def get_approver(application):
    class_mapping = ClassMapping.objects.get(class_id=application.student.class_id)
    if application.status == 'PENDING':
        return class_mapping.dorm_manager
    elif application.status == 'DORM_MANAGER_APPROVED':
        return class_mapping.counselor
```

**新路由（基于Building + Department）：**
```python
def get_approver(application):
    if application.status == 'PENDING':
        # 第一次审批：按楼栋查宿管员
        building = application.student.building_name
        dorm_managers = DormManager.objects.filter(building=building)
        return dorm_managers  # 任一可审批，或按选主规则
    
    elif application.status == 'DORM_MANAGER_APPROVED':
        # 第二次审批：按学院查辅导员
        department = application.student.department
        counselor = Counselor.objects.get(department=department)
        return counselor
```

### 4.4 权限控制调整

**角色权限矩阵：**

| 操作 | 学生 | 宿管员 | 辅导员 | 学工管理员 |
|------|------|--------|--------|------------|
| 提交申请 | ✓ | ✗ | ✗ | ✗ |
| 查看自己的申请 | ✓ | ✗ | ✗ | ✗ |
| 第一次审批（楼栋） | ✗ | ✓ | ✗ | ✗ |
| 查看楼栋范围申请 | ✗ | ✓ | ✗ | ✗ |
| 第二次审批（学院） | ✗ | ✗ | ✓ | ✗ |
| 查看学院范围申请 | ✗ | ✗ | ✓ | ✗ |
| 查看所有申请 | ✗ | ✗ | ✗ | ✓ |
| 查看统计报表 | ✗ | ✗ | ✗ | ✓ |

---

## 五、实施方案（最终版）

### Phase 1: 数据准备与合并（0.5天）

**任务1.1：学院名称规范化**
```python
# scripts/normalize_colleges.py
COLLEGE_MAP = {
    "文学院（苏东坡书院）": "文学院(苏东坡书院)",
    "政法学院、纪检监察学院、知识产权学院": "政法学院",
    "计算机学院": "计算机学院",  # 与File4"计算机与人工智能学院"对应
    # ... 19个学院完整映射
}
```

**任务1.2：File1 + File2合并脚本**
```python
# scripts/merge_student_data.py
def merge_files():
    # 1. 读取File1 (5830行) 作为基准
    # 2. 读取File2 (5675行) 作为补充
    # 3. 按"姓名+规范化学院+班级/BH"匹配（Codex推荐规则）
    # 4. File2有的：补充学号、专业、班号等字段
    # 5. File2没有的：对应字段留空
    # 6. 输出File5 (5830行)
    pass
```

**输出：**
- `file5_students_5830.csv` - 完整学生数据
- `file3_dorm_managers.csv` - 宿管员数据（33楼栋）
- `file4_counselors.csv` - 辅导员数据（19学院）

### Phase 2: 系统代码调整（1-1.5天）

**任务2.1：审批流程修改**
- 移除 `DEAN_APPROVED` 状态
- 修改状态转换规则
- 更新 `Application.get_next_status()` 方法

**任务2.2：路由逻辑重构**
- 创建 `BuildingApprovalRouter` - 楼栋→宿管员路由
- 创建 `DepartmentApprovalRouter` - 学院→辅导员路由
- 移除 `ClassMapping` 依赖

**任务2.3：权限控制扩展**
- 新增 `admin` 角色
- 实现全局查看权限（无业务范围限制）
- 更新权限装饰器

**任务2.4：数据模型微调**
- `Student.class_id` 改为可空
- 确保 `Student.building_name` 和 `Student.department` 非空
- 预留 `DormManager.room_numbers` 字段（未来使用）

### Phase 3: 数据导入（0.5天）

**导入脚本：**
```bash
# Step 1: 导入学生（5830行）
python manage.py import_students file5_students_5830.csv \
  --set-graduating=true \
  --set-year=2026 \
  --allow-empty-class-id

# Step 2: 导入辅导员（19学院）
python manage.py import_counselors file4_counselors.csv

# Step 3: 导入宿管员（33楼栋）
python manage.py import_dorm_managers file3_dorm_managers.csv

# Step 4: 验证路由
python manage.py validate_building_routing
python manage.py validate_department_routing
```

**前置门禁：**
- ✓ File5学生数 = 5830
- ✓ 每个学生的楼栋能找到至少1个宿管员
- ✓ 每个学生的学院能找到1个辅导员
- ✓ 抽样100条验证数据一致性

### Phase 4: 前端调整（0.5天）

**任务4.1：用户界面区分**
- 学生界面：提交申请+查看自己申请
- 宿管员界面：查看楼栋范围申请+第一次审批
- 辅导员界面：查看学院范围申请+第二次审批
- 学工管理员界面：全局数据视图+统计报表（预留）

**任务4.2：审批流程UI更新**
- 移除学工部审批步骤展示
- 更新进度条：2级审批
- 更新审批记录显示

### Phase 5: 测试验证（0.5天）

**测试用例：**
1. 学生提交申请
2. 按楼栋路由到正确宿管员
3. 宿管员审批通过
4. 按学院路由到正确辅导员
5. 辅导员审批通过
6. 状态变为COMPLETED
7. 审批记录完整保存
8. 权限隔离验证（学生/宿管/辅导/管理员）

**总时间：** 2.5-3天

---

## 六、未来升级路径（Phase 2可选）

### 寝室号精确路由升级

**前提：** File3补充寝室号字段后

**数据模型扩展：**
```python
# DormManager model
room_numbers = models.JSONField()  # 负责寝室号列表，如["201","202","203"]

# 或创建新的映射表
class DormManagerRoomMapping(models.Model):
    building = models.CharField(max_length=50)
    room_number = models.CharField(max_length=20)
    dorm_manager = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['building', 'room_number']
```

**路由逻辑升级：**
```python
def get_dorm_manager(application):
    building = application.student.building_name
    room = application.student.room_number
    
    # 精确匹配：楼栋+寝室号 → 唯一宿管员
    mapping = DormManagerRoomMapping.objects.get(

exec
/bin/bash -lc 'rtk rg --files' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
task_plan.md
progress.md
scripts/analyze_excel_data.py
CLAUDE.md
AGENTS.md
tests/test_p0_fixes.sh
tests/smoke_test.sh
DEPLOYMENT.md
tests/api_data_samples.sh
毕业离校系统用户文档.zip
docker-compose.yml
findings.md
backend/Dockerfile
backend/data/templates/counselors_template.csv
backend/data/templates/class_mappings_template.csv
backend/data/templates/students_template.csv
backend/requirements/base.txt
backend/requirements/dev.txt
backend/requirements/prod.txt
backend/schema.py
backend/config/__init__.py
backend/config/urls.py
backend/config/settings/__init__.py
backend/config/settings/base.py
backend/config/settings/prod.py
backend/config/settings/test.py
backend/config/settings/dev.py
backend/config/wsgi.py
backend/scripts/diagnose_xg_api.py
backend/scripts/xg_api_collection_test.py
backend/apps/approvals/validators.py
backend/apps/approvals/__init__.py
backend/apps/approvals/admin.py
backend/apps/approvals/pagination.py
backend/apps/approvals/urls.py
backend/apps/approvals/migrations/__init__.py
backend/apps/approvals/migrations/0003_alter_approval_step.py
backend/apps/approvals/migrations/0002_initial.py
backend/apps/approvals/migrations/0001_initial.py
backend/apps/approvals/tests/__init__.py
backend/apps/approvals/tests/test_rejection_flow.py
backend/apps/approvals/tests/test_list_permissions.py
backend/apps/approvals/tests/test_permissions.py
backend/apps/approvals/tests/test_state_machine.py
backend/apps/approvals/views.py
backend/apps/approvals/serializers.py
backend/apps/approvals/models.py
backend/reports/xg_collection_test_20260603_033437.json
backend/reports/xg_collection_test_20260603_033223.json
backend/reports/xg_collection_test_20260603_033038.json
backend/apps/notifications/services.py
backend/apps/notifications/__init__.py
backend/apps/notifications/admin.py
backend/apps/notifications/urls.py
frontend/types/api.ts
backend/apps/notifications/migrations/__init__.py
backend/apps/notifications/migrations/0001_initial.py
backend/apps/notifications/migrations/0002_alter_notification_type.py
backend/apps/notifications/apps.py
frontend/services/mock.ts
frontend/services/api.ts
demo-web/css/global.css
demo-web/index.html
backend/apps/notifications/tests/__init__.py
backend/apps/notifications/tests/test_auto_notifications_api.py
backend/apps/notifications/tests/test_timeout_warnings.py
backend/apps/notifications/tests/test_models.py
backend/apps/notifications/tests/test_api.py
backend/apps/notifications/tests/test_auto_notifications.py
backend/apps/notifications/views.py
backend/apps/notifications/serializers.py
backend/apps/notifications/models.py
backend/manage.py
backend/apps/notifications/management/__init__.py
backend/apps/attachments/__init__.py
backend/apps/attachments/urls.py
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md
backend/apps/__init__.py
backend/apps/users/integrations/__init__.py
backend/apps/users/integrations/xg_user_client.py
backend/apps/users/integrations/xg_user_mapper.py
backend/apps/users/services/xg_user_sync.py
backend/apps/users/__init__.py
backend/apps/users/admin.py
backend/apps/users/urls.py
backend/apps/users/migrations/__init__.py
backend/apps/users/migrations/0001_initial.py
backend/apps/users/migrations/0002_user_department_user_email_user_phone.py
backend/apps/users/migrations/0004_backfill_dorm_manager.py
backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py
backend/apps/users/apps.py
backend/apps/users/class_mapping.py
backend/apps/users/tests/__init__.py
backend/apps/users/tests/test_xg_user_mapper.py
backend/apps/users/tests/test_xg_user_client.py
backend/apps/users/tests/test_xg_user_sync.py
backend/apps/users/tests/test_import_csv.py
backend/apps/users/views.py
backend/apps/users/serializers.py
backend/apps/users/models.py
backend/apps/users/management/__init__.py
backend/apps/attachments/migrations/__init__.py
backend/apps/attachments/migrations/0001_initial.py
backend/apps/users/management/commands/__init__.py
backend/apps/users/management/commands/import_csv.py
backend/apps/users/management/commands/sync_xg_users.py
backend/apps/users/management/commands/seed_data.py
backend/apps/attachments/tests/__init__.py
backend/apps/attachments/tests/test_list.py
backend/apps/attachments/tests/test_delete.py
backend/apps/attachments/tests/test_upload.py
backend/apps/attachments/tests/test_download.py
backend/apps/attachments/views.py
backend/apps/attachments/serializers.py
backend/apps/attachments/models.py
backend/apps/applications/models.py
docs/plans/week-0-1-execution-plan.md
docs/codex-review-protocol.md
docs/2026年社区辅导员信息统计表.xls
docs/API-DATA-EXAMPLES.md
docs/XG-API与项目数据表对比分析.md
docs/1-5830名毕业生（含研究生）.xls
docs/week3-day0-environment-strategy.md
docs/COMPLETION-STATUS.md
docs/2026届预计毕业生5675人.xlsx
docs/XG-API-DATA-EXAMPLES.md
docs/用户设计说明书.md
docs/外部系统数据接口确认清单.md
docs/PROJECT-SUMMARY.md
docs/Excel数据源实际分析结果.md
docs/微信图片_20260528210619_555_47.jpg
docs/微信图片_20260528210617_553_47.jpg
docs/XG-API-DATA-SAMPLES.md
docs/XG-API-ACTUAL-DATA-SAMPLES.md
docs/微信小程序申请说明.md
docs/XG-API-数据源全面分析报告.md
docs/contracts/contract-v0.2.md
docs/contracts/contract-v0.1.md
docs/Excel数据源分析与需求对比.md
docs/PROJECT-COMPLETION-DECLARATION.md
docs/superpowers/plans/2026-05-27-implementation-plan.md
docs/XG-API-COLLECTION-TEST-GUIDE.md
docs/用户需求最终确认与实施方案.md
docs/数据对接说明文档.md
docs/phase4c-xg-field-coverage.md
docs/操作说明书-待改进事项.md
docs/微信小程序备案说明.md
docs/Codex审查流程指南.md
docs/2026年学院辅导员信息统计表.xls
docs/project-completion-status-2026-06-02.md
docs/api说明.txt
docs/XG-API数据不足解决方案讨论.md
docs/week3-day0-seed-data-requirements.md
docs/week3-day0-acceptance-checklist.md
docs/api-samples/notifications_unread_count.json
docs/api-samples/approvals_list_counselor.json
docs/api-samples/notifications_list.json
docs/api-samples/application_detail.json
docs/api-samples/applications_list.json
docs/templates/宿舍清退数据模板.csv
docs/templates/学生基本信息导入模板.csv
docs/templates/班级辅导员对应关系导入模板.csv
docs/templates/辅导员基本信息导入模板.csv
docs/api/contract-v0.3-skeleton.md
docs/ui-design-proposals/01-analysis-and-responsive-plan.md
docs/acceptance/phase4c-demo-script.md
docs/acceptance/phase4c-known-issues.md
docs/acceptance/phase4c-evidence-index.md
docs/acceptance/phase4c-acceptance-checklist.md
docs/api/api-schema-todo.md
docs/api/contract-v0.3.md
docs/api/contract-v0.2.md
docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md
docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decision.md
docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md
docs/discussions/ui-design-2026-06-02/01-ui-requirements-analysis.md
docs/discussions/ui-design-2026-06-02/02-gemini-review-request.md
docs/discussions/ui-design-2026-06-02/10-final-consensus-dean-filing-ui.md
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md
docs/discussions/ui-design-2026-06-02/02-gemini-review-response.md
docs/discussions/ui-design-2026-06-02/07-claude-response-to-gemini-ui-proposal.md
docs/discussions/ui-design-2026-06-02/04-complete-ui-coverage-analysis.md
docs/discussions/ui-design-2026-06-02/03-claude-response-to-gemini.md
docs/discussions/ui-design-2026-06-02/05-ui-enhancement-color-responsive.md
docs/操作说明书.md
docs/数据确认清单.md
docs/微信图片_20260528210618_554_47.jpg
backend/apps/notifications/management/commands/__init__.py
backend/apps/notifications/management/commands/seed_notifications.py
backend/apps/notifications/management/commands/send_approval_timeout_warnings.py
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md
docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md
docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md
docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md
docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md
docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md
docs/discussions/week3-day1-review-2026-05-30/16-codex-authorization-ruling.md
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md
docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md
miniprogram/services/api.ts
miniprogram/project.config.json
miniprogram/app.wxss
miniprogram/utils/role-guard.ts
miniprogram/utils/date.ts
miniprogram/pages/approvals/approvals.ts
miniprogram/pages/approvals/approvals.wxml
miniprogram/pages/approvals/approvals.wxss
miniprogram/pages/login/login.wxml
miniprogram/pages/login/login.wxss
miniprogram/pages/login/login.ts
miniprogram/pages/student-application/student-application.wxml
miniprogram/pages/student-application/student-application.json
miniprogram/pages/student-application/student-application.wxss
miniprogram/pages/student-application/student-application.ts
miniprogram/pages/detail/detail.ts
miniprogram/pages/detail/detail.wxml
miniprogram/pages/detail/detail.wxss
miniprogram/app.json
miniprogram/app.ts
miniprogram/sitemap.json
miniprogram/types/api.ts
docs/discussions/phase4c-next-steps/34-claude-authorization-interpretation-request.md
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md
docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md
docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md
docs/discussions/phase4c-next-steps/54-claude-codex-consensus-option-a-execution.md
docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md
docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md
docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md
docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md
docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md
docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md
docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md
docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md
docs/discussions/phase4c-next-steps/59-claude-codex-final-consensus-option-2.md
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md
docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md
docs/discussions/completion-review-2026-06-03/02-claude-response.md
docs/discussions/phase4c-next-steps/35-codex-authorization-interpretation-response.md
docs/discussions/completion-review-2026-06-03/01-codex-final-assessment.md
docs/design/2026-05-27-system-design.md
docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md
backend/apps/applications/__init__.py
backend/apps/applications/admin.py
backend/apps/applications/providers.py
backend/apps/applications/pagination.py
backend/apps/applications/urls.py
docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md
docs/discussions/week3-direction-2026-05-30/06-consensus.md
docs/discussions/week3-direction-2026-05-30/01-claude-proposal.md
docs/discussions/week3-direction-2026-05-30/03-claude-response.md
docs/discussions/week3-direction-2026-05-30/02-codex-review.md
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md
docs/discussions/week3-day1-review-2026-05-30/09-codex-execution-review.md
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md
docs/discussions/week3-day1-review-2026-05-30/19-claude-deadlock-analysis.md
docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md
docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md
backend/apps/applications/migrations/0003_application_unique_student_application.py
backend/apps/applications/migrations/__init__.py
backend/apps/applications/migrations/0002_initial.py
backend/apps/applications/migrations/0001_initial.py
backend/apps/applications/migrations/0005_alter_application_status.py
backend/apps/applications/migrations/0004_remove_unique_student_constraint.py
docs/discussions/codex-review-2026-06-02/02-claude-response-migration-strategy.md
docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md
docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md
docs/discussions/codex-review-2026-05-27/01-architecture-review.md
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md
docs/discussions/codex-review-2026-05-27/21-final-consensus.md
docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md
docs/discussions/codex-review-2026-05-27/04-database-review.md
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md
docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md
docs/discussions/codex-review-2026-05-27/02-architecture-response.md
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md
docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md
docs/discussions/phase4c-next-steps/88-step2b-implementation-codex-response.md
docs/discussions/phase4c-next-steps/05-claude-next-steps-strategy-request.md
docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md
docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md
docs/discussions/phase4c-next-steps/58-claude-codex-consensus-option-a-prime-partial.md
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md
docs/discussions/phase4c-next-steps/84-post-step1-next-strategy-request.md
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md
docs/discussions/phase4c-next-steps/55-claude-post-api-schema-p1-next-strategy.md
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md
docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md
docs/discussions/phase4c-next-steps/83-consensus-step1b-lite-first.md
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md
docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md
docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md
docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md
docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md
docs/discussions/phase4c-next-steps/24-claude-consensus-evidence-closure.md
docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md
docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md
docs/discussions/phase4c-next-steps/22-claude-post-execution-next-steps.md
docs/discussions/phase4c-next-steps/30-claude-consensus-contract-revision-gate.md
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md
docs/discussions/phase4c-next-steps/87-step2b-implementation-review-request.md
docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md
docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md
docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md
docs/discussions/phase4c-next-steps/36-claude-consensus-minimal-confirmation.md
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md
docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md
docs/discussions/phase4c-next-steps/49-claude-consensus-option-e-lite-complete.md
docs/discussions/phase4c-next-steps/67-claude-response-accept-codex-fixes.md
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md
docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.md
docs/discussions/phase4c-next-steps/72-claude-codex-consensus-phase2b-step2-strategy.md
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md
docs/discussions/phase4c-next-steps/68-claude-codex-consensus-phase2b-option1.md
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md
docs/discussions/phase4c-next-steps/23-codex-post-execution-next-steps-response.md
docs/discussions/phase4c-next-steps/53-codex-confirmation-option-a-corrected.md
docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md
docs/discussions/phase4c-next-steps/43-claude-post-phase2a-stabilization-next-strategy.md
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md
docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md
docs/discussions/phase4c-next-steps/71-claude-response-accept-b-mini.md
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md
docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md
docs/discussions/phase4c-next-steps/94-post-step3-next-priority-request.md
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md
docs/discussions/phase4c-next-steps/19-claude-next-phase-strategy-request.md
docs/discussions/phase4c-next-steps/89-claude-response-agree-fixes.md
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md
docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md
backend/apps/applications/tests/test_constraints.py
backend/apps/applications/tests/test_application_flow.py
backend/apps/applications/views.py
backend/apps/applications/permissions.py
backend/apps/applications/serializers.py
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md
docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md
backend/apps/applications/tests/test_detail_permissions.py
backend/apps/applications/tests/test_serializer_validation.py
backend/apps/applications/tests/test_list_permissions.py
backend/apps/applications/tests/test_p0_fixes.py
backend/apps/applications/tests/test_error_cases.py
backend/apps/applications/tests/__init__.py
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md
docs/api/notification-contract-v0.1.md

exec
/bin/bash -lc 'rtk rg -n "ClassMapping|DORM_MANAGER_APPROVED|COUNSELOR_APPROVED|DEAN|dean|role|class_id|building|department" -S .' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
./task_plan.md:9:- Negative permission tests are P0, with a minimal role/assignment suite now and exhaustive permutations deferred to Week 4.
./scripts/analyze_excel_data.py:16:    '学生': ['user_id(学号)', 'name(姓名)', 'class_id(班级ID)', 'is_graduating(毕业生标识)',
./scripts/analyze_excel_data.py:17:             'graduation_year(毕业年份)', 'department(院系)', 'phone(手机号)'],
./scripts/analyze_excel_data.py:18:    '辅导员': ['employee_id(工号)', 'name(姓名)', 'department(院系)'],
./scripts/analyze_excel_data.py:20:    'ClassMapping': ['class_id(班级ID)', 'counselor_id(辅导员工号)']
./tests/smoke_test.sh:288:if [ "$APP_STATUS_AFTER" != "pending_dean" ]; then
./tests/smoke_test.sh:289:  echo "✗ Application status not updated: $APP_STATUS_AFTER (expected: pending_dean)"
./tests/smoke_test.sh:295:# Extract dean approval ID
./tests/smoke_test.sh:296:DEAN_APPROVAL_ID=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
./tests/smoke_test.sh:298:  | jq -r '.approvals[] | select(.step=="dean") | .approval_id')
./tests/smoke_test.sh:300:if [ -z "$DEAN_APPROVAL_ID" ] || [ "$DEAN_APPROVAL_ID" = "null" ]; then
./tests/smoke_test.sh:305:echo "  Dean approval: $DEAN_APPROVAL_ID"
./tests/smoke_test.sh:309:DEAN_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
./tests/smoke_test.sh:314:if [ -z "$DEAN_TOKEN" ] || [ "$DEAN_TOKEN" = "null" ]; then
./tests/smoke_test.sh:322:DEAN_APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$DEAN_APPROVAL_ID/approve/" \
./tests/smoke_test.sh:323:  -H "Authorization: Bearer $DEAN_TOKEN" \
./tests/smoke_test.sh:327:DEAN_DECISION=$(echo "$DEAN_APPROVE_RESPONSE" | jq -r '.decision')
./tests/smoke_test.sh:329:if [ "$DEAN_DECISION" != "approved" ]; then
./tests/smoke_test.sh:331:  echo "$DEAN_APPROVE_RESPONSE" | jq '.'
./backend/data/templates/counselors_template.csv:1:employee_id,name,department,is_active,password
./backend/data/templates/class_mappings_template.csv:1:class_id,counselor_employee_id
./backend/data/templates/students_template.csv:1:student_id,name,department,major,class_id,grade,graduation_year,is_graduating,password
./backend/scripts/xg_api_collection_test.py:135:                'department': 0,
./backend/scripts/xg_api_collection_test.py:143:                if user.get('department') and len(user['department']) > 0:
./backend/scripts/xg_api_collection_test.py:144:                    related_stats['department'] += 1
./backend/apps/approvals/validators.py:7:    'dean': ApplicationStatus.PENDING_DEAN,
./miniprogram/utils/role-guard.ts:17:  if (!allowedRoles.includes(userInfo.role)) {
./miniprogram/utils/role-guard.ts:19:    const targetUrl = userInfo.role === 'student'
./backend/apps/approvals/migrations/0003_alter_approval_step.py:16:            field=models.CharField(choices=[('dorm_manager', '宿管员'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20),
./backend/apps/approvals/migrations/0001_initial.py:20:                ('step', models.CharField(choices=[('counselor', '辅导员'), ('dean', '学工部')], max_length=20)),
./miniprogram/pages/approvals/approvals.ts:3:import { checkRoleAndRedirect } from '../../utils/role-guard';
./miniprogram/pages/approvals/approvals.ts:13:    userInfo: { name: '', role: '' },
./miniprogram/pages/approvals/approvals.ts:14:    roleText: '',
./miniprogram/pages/approvals/approvals.ts:19:    if (checkRoleAndRedirect(app.globalData.userInfo, ['counselor', 'dean'])) return;
./miniprogram/pages/approvals/approvals.ts:22:    const roleMap: Record<string, string> = {
./miniprogram/pages/approvals/approvals.ts:26:      dean: '学工部',
./miniprogram/pages/approvals/approvals.ts:31:      roleText: roleMap[userInfo.role] || userInfo.role,
./miniprogram/pages/approvals/approvals.ts:38:    if (checkRoleAndRedirect(app.globalData.userInfo, ['counselor', 'dean'])) return;
./miniprogram/pages/approvals/approvals.wxml:3:    <text class="title">{{userInfo.role === 'dean' ? '备案查询' : '审批列表'}}</text>
./miniprogram/pages/approvals/approvals.wxml:4:    <text class="user-info">{{userInfo.name}} ({{roleText}})</text>
./miniprogram/pages/approvals/approvals.wxml:41:    <text>{{userInfo.role === 'dean' ? '暂无已通过备案申请' : '暂无待审批项'}}</text>
./backend/apps/approvals/tests/test_rejection_flow.py:7:from apps.users.class_mapping import ClassMapping
./backend/apps/approvals/tests/test_rejection_flow.py:20:            role=UserRole.STUDENT,
./backend/apps/approvals/tests/test_rejection_flow.py:21:            class_id='CS2020-01',
./backend/apps/approvals/tests/test_rejection_flow.py:30:            role=UserRole.COUNSELOR
./backend/apps/approvals/tests/test_rejection_flow.py:37:            role=UserRole.DORM_MANAGER
./backend/apps/approvals/tests/test_rejection_flow.py:41:        ClassMapping.objects.create(
./backend/apps/approvals/tests/test_rejection_flow.py:42:            class_id='CS2020-01',
./backend/apps/approvals/tests/test_list_permissions.py:13:        self.student = User.objects.create(user_id='S001', name='学生', role=UserRole.STUDENT, class_id='CS2020-01')
./backend/apps/approvals/tests/test_list_permissions.py:17:        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
./backend/apps/approvals/tests/test_list_permissions.py:21:        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
./backend/apps/approvals/tests/test_list_permissions.py:25:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
./backend/apps/approvals/tests/test_list_permissions.py:29:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
./backend/apps/approvals/tests/test_list_permissions.py:33:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
./backend/apps/approvals/tests/test_list_permissions.py:34:        self.dean1.set_password('D001')
./backend/apps/approvals/tests/test_list_permissions.py:35:        self.dean1.save()
./backend/apps/approvals/tests/test_list_permissions.py:37:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
./backend/apps/approvals/tests/test_list_permissions.py:38:        self.dean2.set_password('D002')
./backend/apps/approvals/tests/test_list_permissions.py:39:        self.dean2.save()
./backend/apps/approvals/tests/test_list_permissions.py:46:            class_id='CS2020-01',
./backend/apps/approvals/tests/test_list_permissions.py:101:    def test_dean_sees_all_approvals_for_archive(self):
./backend/apps/approvals/tests/test_list_permissions.py:102:        self.client.force_authenticate(user=self.dean1)
./backend/apps/approvals/tests/test_list_permissions.py:121:            class_id='CS2020-01',
./backend/apps/approvals/tests/test_list_permissions.py:140:            class_id='CS2020-01',
./backend/apps/approvals/tests/test_permissions.py:7:from apps.users.class_mapping import ClassMapping
./backend/apps/approvals/tests/test_permissions.py:16:            role=UserRole.STUDENT,
./backend/apps/approvals/tests/test_permissions.py:17:            class_id='CS2020-01',
./backend/apps/approvals/tests/test_permissions.py:23:            role=UserRole.STUDENT,
./backend/apps/approvals/tests/test_permissions.py:24:            class_id='CS2020-02',
./backend/apps/approvals/tests/test_permissions.py:32:            role=UserRole.COUNSELOR,
./backend/apps/approvals/tests/test_permissions.py:38:            role=UserRole.COUNSELOR,
./backend/apps/approvals/tests/test_permissions.py:44:            role=UserRole.DORM_MANAGER,
./backend/apps/approvals/tests/test_permissions.py:50:            role=UserRole.DORM_MANAGER,
./backend/apps/approvals/tests/test_permissions.py:53:        self.dean1 = User.objects.create_user(
./backend/apps/approvals/tests/test_permissions.py:56:            role=UserRole.DEAN,
./backend/apps/approvals/tests/test_permissions.py:59:        self.dean2 = User.objects.create_user(
./backend/apps/approvals/tests/test_permissions.py:62:            role=UserRole.DEAN,
./backend/apps/approvals/tests/test_permissions.py:67:        ClassMapping.objects.create(
./backend/apps/approvals/tests/test_permissions.py:68:            class_id='CS2020-01',
./backend/apps/approvals/tests/test_permissions.py:75:        ClassMapping.objects.create(
./backend/apps/approvals/tests/test_permissions.py:76:            class_id='CS2020-02',
./backend/apps/approvals/tests/test_permissions.py:89:            class_id='CS2020-01',
./backend/apps/approvals/tests/test_permissions.py:137:    def test_dean_cannot_act_on_counselor_step(self):
./backend/apps/approvals/tests/test_permissions.py:139:        self.client.force_authenticate(user=self.dean1)
./miniprogram/pages/login/login.ts:40:      if (res.user.role === 'student') {
./miniprogram/pages/login/login.ts:42:      } else if (res.user.role === 'counselor' || res.user.role === 'dean') {
./DEPLOYMENT.md:126:- department (optional)
./DEPLOYMENT.md:129:- class_id (required)
./DEPLOYMENT.md:135:- class_id (required)
./DEPLOYMENT.md:162:**Cause:** Student already has an active application (status: pending_counselor, pending_dean, or approved)
./DEPLOYMENT.md:191:**Solution:** Verify user role and permissions. Check that counselor is assigned to the student's class via class mappings.
./DEPLOYMENT.md:202:- Deans can access attachments for applications with pending dean approval
./frontend/services/mock.ts:18:    role: 'student',
./frontend/services/mock.ts:19:    class_id: 'CS2020-01',
./frontend/services/mock.ts:29:    role: 'counselor',
./frontend/services/mock.ts:30:    class_id: null,
./frontend/services/mock.ts:41:      class_id: 'CS2020-01',
./frontend/services/mock.ts:55:  class_id: 'CS2020-01',
./demo-web/index.html:123:    <select id="roleSelector" onchange="switchRole(this.value)" style="padding: 4px 8px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;">
./demo-web/index.html:126:      <option value="dean">学工部</option>
./demo-web/index.html:184:      <div style="font-size: 12px; color: #999;" id="role-display">宿管员</div>
./demo-web/index.html:314:    function switchRole(role) {
./demo-web/index.html:315:      currentRole = role;
./demo-web/index.html:316:      const roleMap = {
./demo-web/index.html:319:        'dean': '学工部'
./demo-web/index.html:321:      const isDean = role === 'dean';
./demo-web/index.html:326:      // Update list page title and role display
./demo-web/index.html:328:      document.getElementById('role-display').textContent = roleMap[role];
./frontend/types/api.ts:4:export type UserRole = 'student' | 'counselor' | 'dean';
./frontend/types/api.ts:9:  | 'pending_dean'
./frontend/types/api.ts:15:export type ApprovalStep = 'counselor' | 'dean';
./frontend/types/api.ts:26:  role: UserRole;
./frontend/types/api.ts:27:  class_id?: string | null;
./frontend/types/api.ts:46:  class_id: string;
./backend/apps/approvals/tests/test_state_machine.py:7:from apps.users.class_mapping import ClassMapping
./backend/apps/approvals/tests/test_state_machine.py:16:            role=UserRole.STUDENT,
./backend/apps/approvals/tests/test_state_machine.py:17:            class_id='CS2020-01',
./backend/apps/approvals/tests/test_state_machine.py:25:            role=UserRole.COUNSELOR,
./backend/apps/approvals/tests/test_state_machine.py:33:            role=UserRole.DORM_MANAGER,
./backend/apps/approvals/tests/test_state_machine.py:37:        # Create dean
./backend/apps/approvals/tests/test_state_machine.py:38:        self.dean = User.objects.create_user(
./backend/apps/approvals/tests/test_state_machine.py:41:            role=UserRole.DEAN,
./backend/apps/approvals/tests/test_state_machine.py:46:        ClassMapping.objects.create(
./backend/apps/approvals/tests/test_state_machine.py:47:            class_id='CS2020-01',
./backend/apps/approvals/tests/test_state_machine.py:60:            class_id='CS2020-01',
./backend/apps/approvals/views.py:41:    if user.role == UserRole.STUDENT:
./backend/apps/approvals/views.py:48:    if user.role == UserRole.DORM_MANAGER:
./backend/apps/approvals/views.py:55:    elif user.role == UserRole.COUNSELOR:
./backend/apps/approvals/views.py:62:    elif user.role == UserRole.DEAN:
./backend/apps/approvals/views.py:114:    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
./backend/apps/approvals/views.py:117:    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
./backend/apps/approvals/views.py:120:    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
./backend/apps/approvals/views.py:164:        from apps.users.class_mapping import ClassMapping
./backend/apps/approvals/views.py:165:        class_mapping = ClassMapping.objects.get(class_id=application.class_id, active=True)
./backend/apps/approvals/views.py:176:        # Check for existing dean approval to prevent duplicates
./backend/apps/approvals/views.py:177:        existing_dean_approval = Approval.objects.filter(
./backend/apps/approvals/views.py:179:            step=ApprovalStep.DEAN
./backend/apps/approvals/views.py:182:        if existing_dean_approval:
./backend/apps/approvals/views.py:186:        application.status = ApplicationStatus.PENDING_DEAN
./backend/apps/approvals/views.py:189:        # Get first available dean user
./backend/apps/approvals/views.py:191:        dean_user = User.objects.filter(role=UserRole.DEAN, active=True).first()
./backend/apps/approvals/views.py:193:        if not dean_user:
./backend/apps/approvals/views.py:200:            step=ApprovalStep.DEAN,
./backend/apps/approvals/views.py:201:            approver=dean_user,
./backend/apps/approvals/views.py:202:            approver_name=dean_user.name,
./backend/apps/approvals/views.py:205:    elif approval.step == ApprovalStep.DEAN:
./backend/apps/approvals/views.py:237:    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
./backend/apps/approvals/views.py:240:    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
./backend/apps/approvals/views.py:243:    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
./backend/apps/approvals/models.py:9:    DEAN = 'dean', '学工部'
./docs/Codex审查流程指南.md:281:- 结果：修正staging表设计、认证约束、class_id约束等关键问题
./findings.md:17:- `backend/apps/approvals/views.py` has role checks, assigned approver check, duplicate-decision check, and inline status/step matching for both approve and reject.
./backend/apps/applications/admin.py:7:    list_display = ['application_id', 'student', 'student_name', 'class_id', 'status', 'created_at']
./backend/apps/applications/admin.py:9:    search_fields = ['application_id', 'student__user_id', 'student_name', 'class_id']
./backend/apps/notifications/services.py:54:    approver_role_map = {
./backend/apps/notifications/services.py:58:    approver_role = approver_role_map.get(approval.step, "审批人")
./backend/apps/notifications/services.py:62:        message = f"您的离校申请已通过{approver_role}审批。"
./backend/apps/notifications/services.py:66:        message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
./miniprogram/app.ts:4:    userInfo: null as { user_id: string; name: string; role: string } | null,
./docs/plans/week-0-1-execution-plan.md:91:  - 状态流转：pending_counselor → pending_dean（通过）或 rejected（驳回）
./docs/plans/week-0-1-execution-plan.md:95:  - 状态流转：pending_dean → approved（通过）或 rejected（驳回）
./docs/codex-review-protocol.md:281:- 结果：修正staging表设计、认证约束、class_id约束等关键问题
./docs/API-DATA-EXAMPLES.md:17:  "class_id": "CS2020-01",
./docs/API-DATA-EXAMPLES.md:35:| class_id | string | 班级代码 | CS2020-01 |
./docs/API-DATA-EXAMPLES.md:38:| status | string | 申请状态 | pending_dorm_manager / pending_counselor / pending_dean / approved / rejected |
./docs/API-DATA-EXAMPLES.md:69:| step | string | 审批步骤 | dorm_manager / counselor / dean |
./docs/API-DATA-EXAMPLES.md:91:      "class_id": "CS2020-01",
./docs/API-DATA-EXAMPLES.md:171:      "class_id": "CS2020-01",
./docs/API-DATA-EXAMPLES.md:189:- `pending_dean`: 待学工部审批
./docs/API-DATA-EXAMPLES.md:196:- `dean`: 学工部审批
./backend/apps/applications/migrations/0001_initial.py:19:                ('class_id', models.CharField(max_length=50)),
./backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
./docs/XG-API与项目数据表对比分析.md:18:    role = models.CharField(max_length=20)                       # student
./docs/XG-API与项目数据表对比分析.md:19:    department = models.CharField(max_length=100)                # 院系
./docs/XG-API与项目数据表对比分析.md:20:    class_id = models.CharField(max_length=50)                   # 班级ID ⚠️
./docs/XG-API与项目数据表对比分析.md:38:  "department": [{"name": "计算机学院", "level": 2}],
./docs/XG-API与项目数据表对比分析.md:49:| role | ✓ | user_identity.name | "学生" | ⚠️ 需适配 | 实际为对象，mapper假设为字符串 |
./docs/XG-API与项目数据表对比分析.md:50:| department | ✓ | department[0].name | "计算机学院" | ⚠️ 需适配 | 实际为数组，mapper未取[0] |
./docs/XG-API与项目数据表对比分析.md:51:| **class_id** | **✓** | **缺失** | **无** | **❌ 无法映射** | **XG API未提供班级ID** |
./docs/XG-API与项目数据表对比分析.md:62:1. **class_id（班级ID）**
./docs/XG-API与项目数据表对比分析.md:64:   - **业务依赖：** `Student.class_id → ClassMapping.class_id → Counselor`
./docs/XG-API与项目数据表对比分析.md:82:4. **role (user_identity)**
./docs/XG-API与项目数据表对比分析.md:88:5. **department**
./docs/XG-API与项目数据表对比分析.md:92:   - **需要：** 取 `department[0].name`
./docs/XG-API与项目数据表对比分析.md:96:## 二、ClassMapping（班级-辅导员映射表）对比
./docs/XG-API与项目数据表对比分析.md:101:# backend/apps/users/models.py - ClassMapping模型
./docs/XG-API与项目数据表对比分析.md:102:class ClassMapping(models.Model):
./docs/XG-API与项目数据表对比分析.md:103:    class_id = models.CharField(max_length=50, primary_key=True)  # 班级ID
./docs/XG-API与项目数据表对比分析.md:110:ClassMapping(
./docs/XG-API与项目数据表对比分析.md:111:    class_id="CS2022-01",
./docs/XG-API与项目数据表对比分析.md:129:- **缺失影响：** 即使有class_id也无法分配辅导员
./docs/XG-API与项目数据表对比分析.md:133:| class_id | class_name | counselor_employee_id |
./docs/XG-API与项目数据表对比分析.md:148:  "role": "student",
./docs/XG-API与项目数据表对比分析.md:149:  "department": "计算机学院",
./docs/XG-API与项目数据表对比分析.md:150:  "class_id": "CS2022-01",           // ⚠️ 关键字段
./docs/XG-API与项目数据表对比分析.md:165:  "user_identity": {"name": "学生"}, // ⚠️ 需适配到role
./docs/XG-API与项目数据表对比分析.md:166:  "department": [{"name": "计算机学院"}], // ⚠️ 需适配
./docs/XG-API与项目数据表对比分析.md:167:  // class_id: 缺失              // ❌ 无法提供
./docs/XG-API与项目数据表对比分析.md:199:| 🔴 P0 | class_id | 完全缺失 | "CS2022-01" | 无 | 审批人分配失败 |
./docs/XG-API与项目数据表对比分析.md:202:| 🔴 P0 | ClassMapping全表 | 完全缺失 | {"CS2022-01":"T2022001"} | 无 | 审批链路中断 |
./docs/XG-API与项目数据表对比分析.md:205:| 🟡 P1 | department | 结构不匹配 | "计算机学院" | [{"name":"计算机学院"}] | mapper需适配 |
./docs/XG-API与项目数据表对比分析.md:215:- ❌ 完全缺失：5个（class_id, is_graduating, graduation_year, email, major, grade, class_name中5个必填/重要）
./docs/XG-API与项目数据表对比分析.md:216:- ⚠️ 结构不匹配：2个（user_identity, department）
./docs/XG-API与项目数据表对比分析.md:220:**ClassMapping表：**
./docs/XG-API与项目数据表对比分析.md:232:#### class_id（班级ID）
./docs/XG-API与项目数据表对比分析.md:243:- 用于ClassMapping表主键
./docs/XG-API与项目数据表对比分析.md:244:- 一个class_id对应一个辅导员
./docs/XG-API与项目数据表对比分析.md:245:- 学生提交申请时通过class_id查找审批人
./docs/XG-API与项目数据表对比分析.md:293:#### ClassMapping（班级-辅导员映射）
./docs/XG-API与项目数据表对比分析.md:297:class_id: 班级ID（主键）
./docs/XG-API与项目数据表对比分析.md:303:- 必须覆盖所有学生的class_id
./docs/XG-API与项目数据表对比分析.md:305:- 辅导员必须在User表中存在且role=counselor
./docs/XG-API与项目数据表对比分析.md:308:- 学生提交申请时查询 `Student.class_id → ClassMapping → Counselor`
./docs/XG-API与项目数据表对比分析.md:354:- ⚠️ 部分满足/需适配：3个（role, department, phone）
./docs/XG-API与项目数据表对比分析.md:355:- ❌ 完全不满足：4个（class_id, is_graduating, graduation_year, ClassMapping）
./backend/apps/applications/migrations/0005_alter_application_status.py:16:            field=models.CharField(choices=[('draft', '草稿'), ('pending_dorm_manager', '待宿管员审批'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20),
./docs/COMPLETION-STATUS.md:39:- **3步审批流程：** dorm_manager → counselor → dean 完整实现
./miniprogram/types/api.ts:4:export type UserRole = 'student' | 'dorm_manager' | 'counselor' | 'dean';
./miniprogram/types/api.ts:26:  role: UserRole;
./miniprogram/types/api.ts:27:  class_id?: string | null;
./miniprogram/types/api.ts:46:  class_id: string;
./backend/apps/notifications/tests/test_auto_notifications_api.py:14:from apps.users.class_mapping import ClassMapping
./backend/apps/notifications/tests/test_auto_notifications_api.py:29:            role='student',
./backend/apps/notifications/tests/test_auto_notifications_api.py:30:            class_id='CS2021-1'
./backend/apps/notifications/tests/test_auto_notifications_api.py:35:            role='counselor'
./backend/apps/notifications/tests/test_auto_notifications_api.py:40:            role='dorm_manager'
./backend/apps/notifications/tests/test_auto_notifications_api.py:42:        self.dean = User.objects.create_user(
./backend/apps/notifications/tests/test_auto_notifications_api.py:45:            role='dean'
./backend/apps/notifications/tests/test_auto_notifications_api.py:48:        ClassMapping.objects.create(
./backend/apps/notifications/tests/test_auto_notifications_api.py:49:            class_id='CS2021-1',
./backend/apps/notifications/tests/test_auto_notifications_api.py:85:            class_id=self.student.class_id,
./backend/apps/notifications/tests/test_auto_notifications_api.py:127:            class_id=self.student.class_id,
./backend/apps/notifications/tests/test_auto_notifications_api.py:164:            role='student',
./backend/apps/notifications/tests/test_auto_notifications_api.py:165:            class_id='CS2021-2'
./backend/apps/notifications/tests/test_auto_notifications_api.py:172:            class_id=self.student.class_id,
./backend/apps/notifications/tests/test_auto_notifications_api.py:207:            class_id=self.student.class_id,
./backend/apps/notifications/tests/test_auto_notifications_api.py:242:            role='student',
./backend/apps/notifications/tests/test_auto_notifications_api.py:243:            class_id='CS2021-1'
./docs/XG-API-DATA-EXAMPLES.md:41:| departmentId | 否 | string | 部门ID（逗号分隔） | 203,204 |
./docs/XG-API-DATA-EXAMPLES.md:42:| departmentCode | 否 | string | 部门code（逗号分隔） | - |
./docs/XG-API-DATA-EXAMPLES.md:141:### 部门信息（department数组）
./docs/XG-API-DATA-EXAMPLES.md:150:  "department_code": "C100261159409057535680",
./docs/XG-API-DATA-EXAMPLES.md:163:| name | string | 部门名称 | User.department |
./docs/XG-API-DATA-EXAMPLES.md:164:| department_code | string | 部门唯一Code | - |
./docs/XG-API-DATA-EXAMPLES.md:236:| `department[0].name` | `department` | 取第一个部门名称 |
./docs/XG-API-DATA-EXAMPLES.md:238:| `user_identity.name` | `role` | 需要映射规则（学生/教师→对应角色） |
./docs/XG-API-DATA-EXAMPLES.md:245:4. **部门提取：** `department[0].name` （取第一个部门）
./docs/XG-API-DATA-EXAMPLES.md:258:- ✓ `department` 数组至少有一个元素
./docs/XG-API-DATA-EXAMPLES.md:264:- `department` 为空 → department字段为null
./backend/apps/notifications/tests/test_timeout_warnings.py:18:            role='student',
./backend/apps/notifications/tests/test_timeout_warnings.py:19:            class_id='CS2020-1'
./backend/apps/notifications/tests/test_timeout_warnings.py:24:            role='counselor',
./backend/apps/notifications/tests/test_timeout_warnings.py:25:            class_id='CS2020-1'
./backend/apps/notifications/tests/test_timeout_warnings.py:30:            role='dorm_manager'
./backend/apps/notifications/tests/test_models.py:12:            role='student',
./backend/apps/notifications/tests/test_models.py:13:            class_id='CS2020-01'
./backend/apps/notifications/tests/test_models.py:18:            role='counselor'
./backend/apps/notifications/tests/test_models.py:83:            role='student',
./backend/apps/notifications/tests/test_models.py:84:            class_id='CS2020-01'
./backend/apps/applications/tests/test_p0_fixes.py:6:from apps.users.class_mapping import ClassMapping
./backend/apps/applications/tests/test_p0_fixes.py:16:            role=UserRole.STUDENT,
./backend/apps/applications/tests/test_p0_fixes.py:17:            class_id='CS2020-01'
./backend/apps/applications/tests/test_p0_fixes.py:22:            role=UserRole.COUNSELOR
./backend/apps/applications/tests/test_p0_fixes.py:24:        ClassMapping.objects.create(
./backend/apps/applications/tests/test_p0_fixes.py:25:            class_id='CS2020-01',
./backend/apps/applications/tests/test_p0_fixes.py:36:            class_id=self.student.class_id,
./backend/apps/applications/tests/test_p0_fixes.py:47:            class_id=self.student.class_id,
./backend/apps/applications/tests/test_p0_fixes.py:62:            class_id=self.student.class_id,
./backend/apps/applications/tests/test_p0_fixes.py:73:            class_id=self.student.class_id,
./backend/apps/applications/tests/test_p0_fixes.py:89:            role=UserRole.STUDENT,
./backend/apps/applications/tests/test_p0_fixes.py:90:            class_id='CS2020-01'
./backend/apps/applications/tests/test_p0_fixes.py:95:            role=UserRole.COUNSELOR
./backend/apps/applications/tests/test_p0_fixes.py:103:            class_id=self.student.class_id,
./backend/apps/applications/tests/test_p0_fixes.py:113:            class_id=self.student.class_id,
./backend/apps/applications/tests/test_p0_fixes.py:123:            class_id=self.student.class_id,
./docs/外部系统数据接口确认清单.md:14:**核心问题：** XG API缺失class_id、is_graduating、graduation_year等关键字段
./docs/外部系统数据接口确认清单.md:32:| class_id | 班级ID，用于辅导员分配 | ❌ 缺失 | 字符串，如"CS2022-01" |
./docs/外部系统数据接口确认清单.md:38:- 格式：class_id → counselor_employee_id映射
./docs/外部系统数据接口确认清单.md:56:- 班级ID（class_id）- 唯一标识班级
./docs/外部系统数据接口确认清单.md:88:  "class_id": "CS2022-01",
./docs/外部系统数据接口确认清单.md:93:    "department": "计算机学院"
./miniprogram/pages/detail/detail.ts:64:      const isOwner = userInfo.role === 'student' && detail.student_id === userInfo.user_id;
./backend/apps/notifications/tests/test_api.py:14:            role='student',
./backend/apps/notifications/tests/test_api.py:15:            class_id='CS2020-01'
./backend/apps/notifications/tests/test_api.py:20:            role='student',
./backend/apps/notifications/tests/test_api.py:21:            class_id='CS2020-02'
./backend/apps/notifications/tests/test_api.py:26:            role='counselor'
./backend/apps/applications/tests/test_error_cases.py:7:from apps.users.class_mapping import ClassMapping
./backend/apps/applications/tests/test_error_cases.py:20:            role=UserRole.STUDENT,
./backend/apps/applications/tests/test_error_cases.py:21:            class_id='CS2020-01',
./backend/apps/applications/tests/test_error_cases.py:30:            role=UserRole.STUDENT,
./backend/apps/applications/tests/test_error_cases.py:31:            class_id='CS2020-01',
./backend/apps/applications/tests/test_error_cases.py:40:            role=UserRole.STUDENT,
./backend/apps/applications/tests/test_error_cases.py:41:            class_id='CS2020-01',
./backend/apps/applications/tests/test_error_cases.py:50:            role=UserRole.COUNSELOR
./backend/apps/applications/tests/test_error_cases.py:56:            role=UserRole.DORM_MANAGER
./backend/apps/applications/tests/test_error_cases.py:59:        self.dean = User.objects.create_user(
./backend/apps/applications/tests/test_error_cases.py:63:            role=UserRole.DEAN
./backend/apps/applications/tests/test_error_cases.py:67:        ClassMapping.objects.create(
./backend/apps/applications/tests/test_error_cases.py:68:            class_id='CS2020-01',
./backend/apps/notifications/tests/test_auto_notifications.py:30:            role='student',
./backend/apps/notifications/tests/test_auto_notifications.py:31:            class_id='CS2021-1'
./backend/apps/notifications/tests/test_auto_notifications.py:36:            role='counselor'
./backend/apps/notifications/tests/test_auto_notifications.py:41:            role='dorm_manager'
./backend/apps/notifications/tests/test_auto_notifications.py:50:            class_id=self.student.class_id,
./backend/apps/notifications/tests/test_auto_notifications.py:82:            class_id=self.student.class_id,
./backend/apps/notifications/tests/test_auto_notifications.py:113:            class_id=self.student.class_id,
./backend/apps/notifications/tests/test_auto_notifications.py:142:            class_id=self.student.class_id,
./backend/apps/notifications/tests/test_auto_notifications.py:173:            class_id=self.student.class_id,
./backend/apps/notifications/tests/test_auto_notifications.py:208:            class_id=self.student.class_id,
./backend/apps/applications/tests/test_detail_permissions.py:4:from apps.users.class_mapping import ClassMapping
./backend/apps/applications/tests/test_detail_permissions.py:15:        self.student1 = User.objects.create(user_id='2020001', name='学生1', role=UserRole.STUDENT, class_id='CS2020-01')
./backend/apps/applications/tests/test_detail_permissions.py:19:        self.student2 = User.objects.create(user_id='2020002', name='学生2', role=UserRole.STUDENT, class_id='CS2020-02')
./backend/apps/applications/tests/test_detail_permissions.py:24:        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
./backend/apps/applications/tests/test_detail_permissions.py:28:        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
./backend/apps/applications/tests/test_detail_permissions.py:32:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
./backend/apps/applications/tests/test_detail_permissions.py:36:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
./backend/apps/applications/tests/test_detail_permissions.py:41:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
./backend/apps/applications/tests/test_detail_permissions.py:42:        self.dean1.set_password('D001')
./backend/apps/applications/tests/test_detail_permissions.py:43:        self.dean1.save()
./backend/apps/applications/tests/test_detail_permissions.py:45:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
./backend/apps/applications/tests/test_detail_permissions.py:46:        self.dean2.set_password('D002')
./backend/apps/applications/tests/test_detail_permissions.py:47:        self.dean2.save()
./backend/apps/applications/tests/test_detail_permissions.py:50:        ClassMapping.objects.create(class_id='CS2020-01', dorm_manager=self.dorm_manager1, dorm_manager_name='宿管员1', counselor=self.counselor1, counselor_name='辅导员1', active=True)
./backend/apps/applications/tests/test_detail_permissions.py:51:        ClassMapping.objects.create(class_id='CS2020-02', dorm_manager=self.dorm_manager2, dorm_manager_name='宿管员2', counselor=self.counselor2, counselor_name='辅导员2', active=True)
./backend/apps/applications/tests/test_detail_permissions.py:85:    def test_dean_cannot_access_in_progress_application(self):
./backend/apps/applications/tests/test_detail_permissions.py:95:        # Dean archive role cannot access in-progress applications
./backend/apps/applications/tests/test_detail_permissions.py:96:        self.client.force_authenticate(user=self.dean2)
./miniprogram/pages/detail/detail.wxml:19:        <text class="value">{{detail.class_id}}</text>
./miniprogram/pages/detail/detail.wxml:74:    <view class="actions" wx:if="{{canApprove && userInfo.role !== 'dean'}}">
./docs/PROJECT-SUMMARY.md:90:- ✓ 统一系统设计文档字段命名（is_checked_out、checkout_date、dorm_building/dorm_room）
./docs/PROJECT-SUMMARY.md:105:  - 统一使用英文字段名（student_id, employee_id, class_id等）
./docs/PROJECT-SUMMARY.md:252:  - User模型（user_id、name、role、class_id、is_graduating、graduation_year）
./docs/PROJECT-SUMMARY.md:253:  - UserRole枚举（student、counselor、dean）
./docs/PROJECT-SUMMARY.md:266:  - ApplicationStatus枚举（draft、pending_counselor、pending_dean、approved、rejected）
./docs/PROJECT-SUMMARY.md:272:  - ApprovalStep枚举（counselor、dean）
./docs/PROJECT-SUMMARY.md:281:  - 辅导员通过→pending_dean（创建学工部审批记录）
./docs/PROJECT-SUMMARY.md:301:  - 验证状态流转：pending_counselor→pending_dean→approved
./docs/PROJECT-SUMMARY.md:311:  - 学工部驳回：pending_dean→rejected
./docs/PROJECT-SUMMARY.md:315:- ✓ ClassMapping模型
./docs/PROJECT-SUMMARY.md:316:  - class_id、counselor、counselor_name、active
./docs/PROJECT-SUMMARY.md:319:  - 支持导入students CSV（student_id、name、class_id等）
./docs/PROJECT-SUMMARY.md:321:  - 支持导入mappings CSV（class_id、counselor_id）
./docs/PROJECT-SUMMARY.md:324:  - 根据学生class_id查找ClassMapping
./docs/PROJECT-SUMMARY.md:329:  - ClassMapping管理界面
./docs/PROJECT-SUMMARY.md:357:  4. 辅导员审批成功 - status→pending_dean
./docs/PROJECT-SUMMARY.md:384:  - 工程完整性：Codex建议ClassMapping校验、并发测试，Claude认为过度工程
./docs/PROJECT-SUMMARY.md:389:  - ClassMapping校验推到Day 3或Week 3
./docs/PROJECT-SUMMARY.md:427:  - 添加重复dean审批检查（防止重复创建）
./docs/PROJECT-SUMMARY.md:433:  - 修复测试问题（添加format='json'，添加D001 dean用户）
./docs/PROJECT-SUMMARY.md:456:  - 添加Dean detail endpoint权限检查（只能查看有pending dean approval的申请）
./docs/PROJECT-SUMMARY.md:743:  - 完整审批流程验证（student→counselor→dean）
./docs/PROJECT-SUMMARY.md:769:- ✓ 新增状态机覆盖：重复驳回冲突、counselor/dean步骤状态不匹配返回409
./docs/PROJECT-SUMMARY.md:771:- ✓ 前端/小程序类型对齐：登录`token_type`、用户`class_id`、申请列表字段、分页去除`next/previous`
./docs/PROJECT-SUMMARY.md:982:  - miniprogram/pages/login/login.ts（student→student-application, counselor/dean→approvals, 未知角色清理会话）
./docs/PROJECT-SUMMARY.md:1034:  - miniprogram/utils/role-guard.ts（防止重复跳转的角色保护）
./docs/PROJECT-SUMMARY.md:1037:  - miniprogram/pages/student-application/student-application.ts（使用role-guard + date工具，onShow刷新today）
./docs/PROJECT-SUMMARY.md:1038:  - miniprogram/pages/approvals/approvals.ts（使用role-guard）
./docs/PROJECT-SUMMARY.md:1077:  - test_dean_cannot_access_non_assigned_application
./docs/PROJECT-SUMMARY.md:1124:  - list_attachments：GET，RBAC（学生own/辅导员class+approval/学工部dean approval）
./docs/PROJECT-SUMMARY.md:1257:  - counselors.csv: active → is_active, 添加department字段
./docs/PROJECT-SUMMARY.md:1259:  - students.csv: 移除active字段, 添加department/major/grade字段
./docs/PROJECT-SUMMARY.md:1274:- ✓ 必填字段验证（student_id, name, class_id等）
./docs/PROJECT-SUMMARY.md:1702:  - test_approval_approved_notification_dean（学工部审批通过通知）
./docs/PROJECT-SUMMARY.md:1853:   - 扫描pending审批，判断超时（counselor 3天，dean 2天）
./docs/PROJECT-SUMMARY.md:1864:   - 6个测试：counselor/dean超时、未超时、已审批、幂等性、dry_run
./docs/PROJECT-SUMMARY.md:2233:- ✅ API初期只补充phone/email/department，不创建新用户
./docs/PROJECT-SUMMARY.md:2234:- ✅ class_id/is_graduating/graduation_year继续由CSV维护
./docs/PROJECT-SUMMARY.md:2289:1. User模型缺失phone/email/department字段
./docs/PROJECT-SUMMARY.md:2307:- 待讨论：User模型扩展策略（增加phone/email/department）
./docs/PROJECT-SUMMARY.md:2370:- 场景覆盖：skip透传/existing候选/missing不创建/role冲突/只读保证/字段gap warning/空输入/混合场景
./docs/PROJECT-SUMMARY.md:2381:- ⏭ 下一步：User模型扩展决策（增加phone/email/department字段）
./docs/PROJECT-SUMMARY.md:2398:- 扩展User模型：新增phone/email/department三个nullable字段
./docs/PROJECT-SUMMARY.md:2399:- 字段权威性划分：CSV主导核心字段（user_id/name/role/class_id/is_graduating/graduation_year），API补充联系方式（phone/email/department）
./docs/PROJECT-SUMMARY.md:2405:  - 新增3个API补充字段（phone/email/department）
./docs/PROJECT-SUMMARY.md:2408:  - apps/users/migrations/0002_user_department_user_email_user_phone.py
./docs/PROJECT-SUMMARY.md:2425:- backend/apps/users/migrations/0002_user_department_user_email_user_phone.py（新建）
./docs/PROJECT-SUMMARY.md:2472:  - statusMap更新：pending_counselor→pending_dorm_manager, pending_dean→pending_counselor
./docs/PROJECT-SUMMARY.md:2483:  - roleMap新增：dorm_manager: '宿管员'
./docs/PROJECT-SUMMARY.md:2484:  - roleMap修正：dean: '学工部'（原'院长'）
./docs/PROJECT-SUMMARY.md:2510:  - 动态标题：`{{userInfo.role === 'dean' ? '备案查询' : '审批列表'}}`
./docs/PROJECT-SUMMARY.md:2513:  - 审批按钮条件：`wx:if="{{canApprove && userInfo.role !== 'dean'}}"`
./docs/PROJECT-SUMMARY.md:2516:- docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md
./docs/PROJECT-SUMMARY.md:2518:- docs/discussions/ui-design-2026-06-02/10-final-consensus-dean-filing-ui.md
./docs/PROJECT-SUMMARY.md:2540:- ✓ **小程序角色守卫冲突**：文档说宿管员可进审批列表，实际小程序只允许counselor/dean；添加警告说明
./docs/PROJECT-SUMMARY.md:2585:- class_id（班级ID）→ 审批人分配失败
./docs/PROJECT-SUMMARY.md:2588:- ClassMapping表（班级-辅导员映射）→ 审批链路中断
./docs/PROJECT-SUMMARY.md:2593:- department实际为数组 `[{"name": "计算机学院"}]` 而非字符串
./docs/PROJECT-SUMMARY.md:2599:  - 数据流：CSV创建用户+核心字段 → XG API更新phone/department/active
./docs/PROJECT-SUMMARY.md:2642:- ✓ department数组格式支持：`[{"name": "计算机学院"}]`
./docs/PROJECT-SUMMARY.md:2707:- ❌ 缺：负责班级清单（P0关键字段，无法生成ClassMapping）
./docs/PROJECT-SUMMARY.md:2718:- 无法生成ClassMapping表
./docs/PROJECT-SUMMARY.md:2732:| ClassMapping | 0% | ❌ 完全不满足 | 无负责班级信息 |
./docs/PROJECT-SUMMARY.md:2825:2. **班级字段处理** - class_id暂时为空，不用于路由
./docs/PROJECT-SUMMARY.md:2836:| ClassMapping缺失 | 决策3：改为楼栋+学院路由 | ✅ 已解除 |
./docs/PROJECT-SUMMARY.md:2845:| 路由方式 | ClassMapping(class_id) | Building+College | 重大 |
./backend/apps/applications/tests/test_list_permissions.py:4:from apps.users.class_mapping import ClassMapping
./backend/apps/applications/tests/test_list_permissions.py:14:        self.student1 = User.objects.create(user_id='S001', name='学生1', role=UserRole.STUDENT, class_id='CS2020-01')
./backend/apps/applications/tests/test_list_permissions.py:18:        self.student2 = User.objects.create(user_id='S002', name='学生2', role=UserRole.STUDENT, class_id='CS2020-02')
./backend/apps/applications/tests/test_list_permissions.py:22:        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
./backend/apps/applications/tests/test_list_permissions.py:26:        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
./backend/apps/applications/tests/test_list_permissions.py:30:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
./backend/apps/applications/tests/test_list_permissions.py:34:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
./backend/apps/applications/tests/test_list_permissions.py:38:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
./backend/apps/applications/tests/test_list_permissions.py:39:        self.dean.set_password('D001')
./backend/apps/applications/tests/test_list_permissions.py:40:        self.dean.save()
./backend/apps/applications/tests/test_list_permissions.py:43:        ClassMapping.objects.create(class_id='CS2020-01', dorm_manager=self.dorm_manager1, dorm_manager_name='宿管员1', counselor=self.counselor1, counselor_name='辅导员1', active=True)
./backend/apps/applications/tests/test_list_permissions.py:44:        ClassMapping.objects.create(class_id='CS2020-02', dorm_manager=self.dorm_manager2, dorm_manager_name='宿管员2', counselor=self.counselor2, counselor_name='辅导员2', active=True)
./backend/apps/applications/tests/test_list_permissions.py:51:            class_id='CS2020-01',
./backend/apps/applications/tests/test_list_permissions.py:61:            class_id='CS2020-02',
./backend/apps/applications/tests/test_list_permissions.py:102:    def test_dean_sees_only_approved_applications_for_archive(self):
./backend/apps/applications/tests/test_list_permissions.py:103:        self.client.force_authenticate(user=self.dean)
./docs/Excel数据源实际分析结果.md:30:| class_id (班级ID) | 班级 | ✅ 满足 | 格式：电信(专升本)202403 |
./docs/Excel数据源实际分析结果.md:31:| department (院系) | 学院名称 | ✅ 满足 | 如：物理与电信学院 |
./docs/Excel数据源实际分析结果.md:67:| class_id (班级ID) | BH | ✅ 满足 | 格式：环境202201 |
./docs/Excel数据源实际分析结果.md:68:| department (院系) | ❌ 缺失 | **P0缺陷** | YXMC仅为校名，无学院信息 |
./docs/Excel数据源实际分析结果.md:87:| role | - | 需手工标记 | 固定为dorm_manager |
./docs/Excel数据源实际分析结果.md:104:| department (院系) | 学院 | ✅ 满足 | |
./docs/Excel数据源实际分析结果.md:106:| role | - | 需手工标记 | 固定为counselor |
./docs/Excel数据源实际分析结果.md:108:**ClassMapping关键缺陷：**
./docs/Excel数据源实际分析结果.md:111:| class_id (负责班级) | ❌ 完全缺失 | **P0缺陷** | 无法建立辅导员-班级映射 |
./docs/Excel数据源实际分析结果.md:151:- 无法生成ClassMapping表
./docs/Excel数据源实际分析结果.md:170:### 3.1 学生表（User - role=student）
./docs/Excel数据源实际分析结果.md:179:### 3.2 辅导员表（User - role=counselor）
./docs/Excel数据源实际分析结果.md:187:### 3.3 宿管员表（User - role=dorm_manager）
./docs/Excel数据源实际分析结果.md:195:### 3.4 班级-辅导员映射表（ClassMapping）
./docs/Excel数据源实际分析结果.md:222:class_id,counselor_id
./docs/Excel数据源实际分析结果.md:337:| ClassMapping | ❌ 0% | 完全缺失 | 必须补充 |
./docs/api-samples/application_detail.json:5:  "class_id": "CS2020-01",
./docs/api-samples/application_detail.json:34:      "step": "dean",
./docs/contracts/contract-v0.2.md:12:UserRole: student | counselor | dean
./docs/contracts/contract-v0.2.md:13:ApplicationStatus: draft | pending_counselor | pending_dean | approved | rejected
./docs/contracts/contract-v0.2.md:14:ApprovalStep: counselor | dean
./docs/contracts/contract-v0.2.md:27:  "role": "student",
./docs/contracts/contract-v0.2.md:28:  "class_id": "CS2020-01"
./docs/contracts/contract-v0.2.md:32:`class_id` 对教师角色为 `null`。
./docs/contracts/contract-v0.2.md:41:  "class_id": "CS2020-01",
./docs/contracts/contract-v0.2.md:119:| pending_counselor | 通过 | counselor | counselor | pending_dean | 创建 dean 审批 |
./docs/contracts/contract-v0.2.md:121:| pending_dean | 通过 | dean | dean | approved | 无 |
./docs/contracts/contract-v0.2.md:122:| pending_dean | 驳回 | dean | dean | rejected | 无 |
./docs/contracts/contract-v0.2.md:128:- `dean` 审批只能处理 `pending_dean` 申请。
./docs/contracts/contract-v0.2.md:130:- 已处于 `pending_counselor`、`pending_dean`、`approved` 的申请会阻断重复提交。
./docs/contracts/contract-v0.2.md:134:| 操作 | student | counselor | dean |
./docs/contracts/contract-v0.2.md:138:| 申请列表 | 仅本人申请 | 仅本人待处理 counselor 审批对应申请 | 仅本人待处理 dean 审批对应申请 |
./docs/contracts/contract-v0.2.md:139:| 申请详情 | 仅本人申请 | 仅负责班级申请 | 仅本人待处理 dean 审批对应申请 |
./docs/contracts/contract-v0.2.md:140:| 审批列表 | 禁止 | 仅本人 counselor 审批 | 仅本人 dean 审批 |
./docs/contracts/contract-v0.2.md:142:| dean 审批动作 | 禁止 | 禁止 | 仅指定 approver |
./docs/contracts/contract-v0.2.md:163:    "role": "student",
./docs/contracts/contract-v0.2.md:164:    "class_id": "CS2020-01"
./docs/api-samples/applications_list.json:8:      "class_id": "CS2020-01",
./docs/contracts/contract-v0.1.md:22:    role: UserRole                    # 角色：student/counselor/dean
./docs/contracts/contract-v0.1.md:24:    class_id: Optional[str] = None    # 班级ID（学生必填，教师为None）
./docs/contracts/contract-v0.1.md:38:    class_id: str
./docs/contracts/contract-v0.1.md:55:    step: ApprovalStep           # counselor/dean
./docs/contracts/contract-v0.1.md:86:    DEAN = "dean"
./docs/contracts/contract-v0.1.md:95:    PENDING_DEAN = "pending_dean"        # 待学工部审批
./docs/contracts/contract-v0.1.md:105:    DEAN = "dean"
./docs/contracts/contract-v0.1.md:134:| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
./docs/contracts/contract-v0.1.md:136:| pending_dean | 学工部通过 | dean | approved | 无 |
./docs/contracts/contract-v0.1.md:137:| pending_dean | 学工部驳回 | dean | rejected | 无 |
./docs/contracts/contract-v0.1.md:151:| 操作 | student | counselor | dean |
./docs/contracts/contract-v0.1.md:219:    "role": "student",
./docs/contracts/contract-v0.1.md:220:    "class_id": "CS2020-01"
./docs/contracts/contract-v0.1.md:225:**说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。
./docs/contracts/contract-v0.1.md:245:  "class_id": "CS2020-01",
./docs/contracts/contract-v0.1.md:263:  "class_id": "CS2020-01",
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
./docs/contracts/contract-v0.1.md:366:deans = [
./docs/contracts/contract-v0.1.md:367:    {"user_id": "D001", "name": "赵主任", "role": "dean", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
./docs/contracts/contract-v0.1.md:374:    {"class_id": "CS2020-01", "counselor_id": "T001"},
./docs/contracts/contract-v0.1.md:375:    {"class_id": "CS2020-02", "counselor_id": "T002"},
./docs/contracts/contract-v0.1.md:383:{"user_id": "2020099", "name": "边界1", "role": "student", "class_id": "INVALID", "is_graduating": True, "graduation_year": 2024, "active": True}
./docs/contracts/contract-v0.1.md:388:{"user_id": "T099", "name": "停用老师", "role": "counselor", "class_id": None, "active": False}
./docs/contracts/contract-v0.1.md:393:{"user_id": "2021001", "name": "边界2", "role": "student", "class_id": "CS2021-01", "is_graduating": False, "graduation_year": 2025, "active": True}
./docs/contracts/contract-v0.1.md:398:{"user_id": "2019001", "name": "边界3", "role": "student", "class_id": "CS2019-01", "is_graduating": True, "graduation_year": 2024, "active": True}
./docs/contracts/contract-v0.1.md:605:        role: 'student',
./docs/contracts/contract-v0.1.md:606:        class_id: 'CS2020-01'
./docs/Excel数据源分析与需求对比.md:22:### 2.1 学生表（User - role=student）
./docs/Excel数据源分析与需求对比.md:28:| **class_id** | **班级ID** | string | ✓ | **审批路由关键字段** | **文件1或文件2** |
./docs/Excel数据源分析与需求对比.md:31:| department | 院系 | string | ✓ | 所属学院 | 文件1或文件2 |
./docs/Excel数据源分析与需求对比.md:37:- ✅ 如无class_id，是否包含"专业+年级+班号"可组合生成？
./docs/Excel数据源分析与需求对比.md:40:### 2.2 辅导员表（User - role=counselor）
./docs/Excel数据源分析与需求对比.md:46:| department | 院系 | string | ✓ | 所属学院 | 文件4 |
./docs/Excel数据源分析与需求对比.md:48:| role | 角色 | string | ✓ | 固定"counselor" | 手工标记 |
./docs/Excel数据源分析与需求对比.md:54:### 2.3 宿管员表（User - role=dorm_manager）
./docs/Excel数据源分析与需求对比.md:61:| role | 角色 | string | ✓ | 固定"dorm_manager" | 手工标记 |
./docs/Excel数据源分析与需求对比.md:66:### 2.4 班级-辅导员映射表（ClassMapping）
./docs/Excel数据源分析与需求对比.md:70:| **class_id** | **班级ID** | string | ✓ | **主键** | **与学生表一致** |
./docs/Excel数据源分析与需求对比.md:89:- [ ] **班级ID或班级名称**（class_id / class / 班级 / 班号）
./docs/Excel数据源分析与需求对比.md:90:- [ ] 院系/学院（department / 院系 / 学院）
./docs/Excel数据源分析与需求对比.md:108:- [ ] 所属学院（department / 学院 / 院系）
./docs/Excel数据源分析与需求对比.md:142:**缺class_id但有班级名称：**
./docs/Excel数据源分析与需求对比.md:143:- 需要：创建class_id规则（如"学院缩写+年级+班号"）
./docs/Excel数据源分析与需求对比.md:158:1. ❌ 完全没有班级信息（无class_id也无班级名称）
./docs/Excel数据源分析与需求对比.md:171:**步骤1：统一class_id格式**
./docs/Excel数据源分析与需求对比.md:173:# 如果只有班级名称，生成class_id
./docs/Excel数据源分析与需求对比.md:181:role = 'student'  # 学生角色
./docs/Excel数据源分析与需求对比.md:184:**步骤3：生成ClassMapping**
./docs/Excel数据源分析与需求对比.md:186:class_id,counselor_id
./docs/Excel数据源分析与需求对比.md:202:user_id,name,role,department,class_id,is_graduating,graduation_year,phone,email
./docs/week3-day0-acceptance-checklist.md:46:SELECT role, COUNT(*) FROM users GROUP BY role;
./docs/week3-day0-acceptance-checklist.md:47:-- 预期：student=2, counselor=2, dean=1
./docs/week3-day0-acceptance-checklist.md:79:    "role": "student"
./docs/week3-day0-acceptance-checklist.md:158:  "status": "pending_dean",
./docs/week3-day0-acceptance-checklist.md:172:- [ ] 申请状态从pending_counselor变为pending_dean
./docs/week3-day0-acceptance-checklist.md:206:  "step": "dean",
./docs/week3-day0-acceptance-checklist.md:229:      "step": "dean",
./docs/week3-day0-acceptance-checklist.md:239:- [ ] 申请状态从pending_dean变为approved
./docs/week3-day0-acceptance-checklist.md:274:      "step": "dean",
./docs/week3-day0-acceptance-checklist.md:452:DEAN_TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
./docs/week3-day0-acceptance-checklist.md:458:  -H "Authorization: Bearer $DEAN_TOKEN" \
./backend/apps/applications/tests/test_constraints.py:8:from apps.users.class_mapping import ClassMapping
./backend/apps/applications/tests/test_constraints.py:17:            role=UserRole.STUDENT,
./backend/apps/applications/tests/test_constraints.py:18:            class_id='CS2020-01',
./backend/apps/applications/tests/test_constraints.py:28:            role=UserRole.COUNSELOR,
./backend/apps/applications/tests/test_constraints.py:34:            role=UserRole.DORM_MANAGER,
./backend/apps/applications/tests/test_constraints.py:39:        ClassMapping.objects.create(
./backend/apps/applications/tests/test_constraints.py:40:            class_id='CS2020-01',
./backend/apps/applications/tests/test_application_flow.py:7:from apps.users.class_mapping import ClassMapping
./backend/apps/applications/tests/test_application_flow.py:21:            role=UserRole.STUDENT,
./backend/apps/applications/tests/test_application_flow.py:22:            class_id='CS2020-01',
./backend/apps/applications/tests/test_application_flow.py:31:            role=UserRole.COUNSELOR
./backend/apps/applications/tests/test_application_flow.py:38:            role=UserRole.DORM_MANAGER
./backend/apps/applications/tests/test_application_flow.py:41:        self.dean = User.objects.create_user(
./backend/apps/applications/tests/test_application_flow.py:45:            role=UserRole.DEAN
./backend/apps/applications/tests/test_application_flow.py:49:        ClassMapping.objects.create(
./backend/apps/applications/tests/test_application_flow.py:50:            class_id='CS2020-01',
./backend/apps/applications/tests/test_application_flow.py:119:        self.assertEqual(application.status, ApplicationStatus.PENDING_DEAN)
./backend/apps/applications/tests/test_application_flow.py:126:        dean_token = response.data['access_token']
./backend/apps/applications/tests/test_application_flow.py:129:        dean_approval = application.approvals.get(step=ApprovalStep.DEAN)
./backend/apps/applications/tests/test_application_flow.py:131:        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dean_token}')
./backend/apps/applications/tests/test_application_flow.py:132:        response = self.client.post(f'/api/approvals/{dean_approval.approval_id}/approve/', {
./backend/apps/applications/tests/test_application_flow.py:149:        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {dean_token}')
./docs/templates/学生基本信息导入模板.csv:1:student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
./docs/templates/班级辅导员对应关系导入模板.csv:1:class_id,class_name,counselor_employee_id
./docs/templates/辅导员基本信息导入模板.csv:1:employee_id,name,department,phone,email,is_active
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:38:    PENDING_DEAN = 'pending_dean', '待学工部审批'
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:57:    DEAN = 'dean', '学工部'
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:87:- 所有测试中的 `self.dean` → `self.counselor`（第二审批人）
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:89:- 状态断言从 `pending_dean` → `pending_counselor`
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:106:- 如果数据库中已有 `pending_counselor` 或 `pending_dean` 状态的申请，需要数据迁移脚本
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:148:- 先检查数据库中是否有 `pending_counselor` 或 `pending_dean` 记录
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:157:- 全局搜索所有 `PENDING_COUNSELOR` 和 `PENDING_DEAN` 引用
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:166:- 检查 `User.role` 是否支持 `dorm_manager` 角色
./docs/discussions/ui-design-2026-06-02/06-approval-workflow-change-requirement.md:194:- 实施时需要确认 `User.role` 是否支持 `dorm_manager` 角色
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decision.md:6:**回应：** 08-codex-dean-filing-ui-decision
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decision.md:59:- 列表页标题：`role === 'dean' ? '备案查询' : '审批列表'`
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decision.md:60:- 空状态文案：`role === 'dean' ? '暂无已通过备案申请' : '暂无待审批申请'`
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decision.md:61:- 详情页操作区：`if (role === 'dean') { hide approval buttons }`
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decision.md:64:- 页面标题：`{{roleText === '学工部' ? '备案查询' : '审批列表'}}`
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decision.md:68:- 审批按钮显示逻辑：`canApprove && userInfo.role !== 'dean'`
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decision.md:73:- `backend/apps/applications/views.py:list_applications` - dean 返回 `status=approved` 申请
./docs/discussions/ui-design-2026-06-02/09-claude-response-to-codex-filing-decision.md:74:- `backend/apps/approvals/views.py:list_approvals` - dean 返回所有审批记录
./docs/XG-API-DATA-SAMPLES.md:76:  "department_code": "C100260159402712838523",
./docs/XG-API-DATA-SAMPLES.md:82:#### 二级部门（parent_dep[1] / department[0]）
./docs/XG-API-DATA-SAMPLES.md:88:  "department_code": "C100261159409057535680",
./docs/XG-API-DATA-SAMPLES.md:102:**映射规则：** 取 `department[0].name` → `User.department = "产品测试"`
./docs/XG-API-DATA-SAMPLES.md:171:| department[0].name | "产品测试" | User.department | "产品测试" | 取第一个部门 |
./docs/XG-API-DATA-SAMPLES.md:173:| user_identity.name | "来宾" | User.role | - | 需要身份映射规则 |
./docs/XG-API-DATA-SAMPLES.md:193:| department | 至少1个 | [{"id": 47, ...}] | ✓ |
./docs/XG-API-DATA-SAMPLES.md:214:### 情况2：department数组为空
./docs/XG-API-DATA-SAMPLES.md:219:  "department": []
./docs/XG-API-DATA-SAMPLES.md:223:**处理：** `User.department = None`
./docs/XG-API-ACTUAL-DATA-SAMPLES.md:66:| department（部门） | 20 | 0 | 100% | ✓ 优秀 |
./docs/XG-API-ACTUAL-DATA-SAMPLES.md:93:      "department": [{"name": "计算机学院", "level": 2}],
./docs/XG-API-ACTUAL-DATA-SAMPLES.md:108:| department[0].name | "计算机学院" | User.department | "计算机学院" | ✓ 取第一个 |
./docs/XG-API-ACTUAL-DATA-SAMPLES.md:116:### 样例3：部门层级（department / parent_dep）
./docs/XG-API-ACTUAL-DATA-SAMPLES.md:145:### 情况2：department数组为空
./docs/XG-API-ACTUAL-DATA-SAMPLES.md:193:| `department[0].name` | [待采集] | `User.department` | 取第一个部门 | [待采集] | [待验证] |
./docs/XG-API-ACTUAL-DATA-SAMPLES.md:195:| `user_identity.name` | [待采集] | `User.role` | 身份映射规则 | [待采集] | [待验证] |
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:3:**文档编号：** 08-codex-dean-filing-ui-decision  
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:17:- 数据仍使用后端已支持的 dean 角色查询逻辑，只展示 `status=approved` 的申请。
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:36:- **选项 B**通过“备案查询”Tab 明确语义，但 dean 角色天然只看 approved 数据时，“全部 / 待审批 / 已审批 / 备案查询”这些 Tab 对学工部并没有真实业务意义，反而暗示还有审批过滤。
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:48:   - 后端已支持 dean 查看 approved 申请。
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:93:> 复用现有审批列表和详情页，按 dean/学工部角色把页面语义改为“备案查询”，列表只展示已通过申请，详情页保持只读。
./docs/discussions/ui-design-2026-06-02/08-codex-dean-filing-ui-decision.md:125:   - 当前 dean API 已固定返回 approved。
./backend/apps/applications/views.py:15:from apps.users.class_mapping import ClassMapping
./backend/apps/applications/views.py:66:    if user.role == UserRole.STUDENT:
./backend/apps/applications/views.py:70:    elif user.role == UserRole.DORM_MANAGER:
./backend/apps/applications/views.py:79:    elif user.role == UserRole.COUNSELOR:
./backend/apps/applications/views.py:87:    # Dean: view all approved applications (archiving role)
./backend/apps/applications/views.py:88:    elif user.role == UserRole.DEAN:
./backend/apps/applications/views.py:118:    if user.role != UserRole.STUDENT:
./backend/apps/applications/views.py:148:        class_mapping = ClassMapping.objects.get(class_id=user.class_id, active=True)
./backend/apps/applications/views.py:149:    except ClassMapping.DoesNotExist:
./backend/apps/applications/views.py:151:                                    'details': {'class_id': user.class_id}}},
./backend/apps/applications/views.py:156:                                    'details': {'class_id': user.class_id}}},
./backend/apps/applications/views.py:165:        class_id=user.class_id,
./backend/apps/notifications/management/commands/seed_notifications.py:11:        students = User.objects.filter(role='student')[:3]
./docs/XG-API-数据源全面分析报告.md:49:| 3 | department | ✓ 必填 | department[0].name | ✅ 满足 | 100% | - |
./docs/XG-API-数据源全面分析报告.md:51:| 5 | **class_id** | **✓ 必填** | **缺失** | **❌ 不满足** | **0%** | **API未提供班级ID** |
./docs/XG-API-数据源全面分析报告.md:76:| 3 | department | ✓ 必填 | department | ✅ 满足 | - |
./docs/XG-API-数据源全面分析报告.md:88:| 1 | **class_id** | **✓ 必填** | **缺失** | **❌ 不满足** | **API未提供班级ID** |
./docs/XG-API-数据源全面分析报告.md:112:#### P0-1: class_id（班级ID）缺失
./docs/XG-API-数据源全面分析报告.md:115:- XG API实际采样20条记录，均无class_id或等价字段
./docs/XG-API-数据源全面分析报告.md:116:- 无法从department、parent_dep、或其他关联对象推导唯一班级标识
./docs/XG-API-数据源全面分析报告.md:121:   - 系统依赖 `Student.class_id → ClassMapping.class_id → ClassMapping.counselor_id → Counselor`
./docs/XG-API-数据源全面分析报告.md:122:   - 缺失class_id导致审批链路首个分派点无法落地
./docs/XG-API-数据源全面分析报告.md:126:   - ClassMapping表以class_id为主键
./docs/XG-API-数据源全面分析报告.md:131:   - User模型要求学生必填class_id
./docs/XG-API-数据源全面分析报告.md:140:- ✓ 已实施：CSV导入维护class_id
./docs/XG-API-数据源全面分析报告.md:141:- ✓ 已实施：API同步时不覆盖class_id字段
./docs/XG-API-数据源全面分析报告.md:218:- XG用户API不提供class_id到counselor_employee_id的映射
./docs/XG-API-数据源全面分析报告.md:220:- 需要独立数据源维护ClassMapping表
./docs/XG-API-数据源全面分析报告.md:224:   - 即使有class_id，也无法查找对应辅导员
./docs/XG-API-数据源全面分析报告.md:225:   - `class_id → counselor_id` 映射查询失败
./docs/XG-API-数据源全面分析报告.md:238:- ✓ 已实施：CSV导入ClassMapping表
./docs/XG-API-数据源全面分析报告.md:295:#### P1-2: mapper不支持department数组结构
./docs/XG-API-数据源全面分析报告.md:299:- 当前mapper：直接赋值 `department = xg_user.get('department')`
./docs/XG-API-数据源全面分析报告.md:307:- department字段值错误（显示为"[{'name':...}]"）
./docs/XG-API-数据源全面分析报告.md:310:- 取 `department[0].name`
./docs/XG-API-数据源全面分析报告.md:430:| department | 20 | 20 | 0 | 0 | 100% | ✓ 优秀 |
./docs/XG-API-数据源全面分析报告.md:493:  ↓ 包含：student_id, name, class_id, is_graduating, graduation_year
./docs/XG-API-数据源全面分析报告.md:499:  ↓ 更新字段：phone, department, active/status
./docs/XG-API-数据源全面分析报告.md:501:  ↓ 不覆盖：class_id, is_graduating, graduation_year
./docs/XG-API-数据源全面分析报告.md:508:- ✓ CSV维护ClassMapping班级-辅导员映射
./docs/XG-API-数据源全面分析报告.md:510:- ✓ XG API更新phone/department/active
./docs/XG-API-数据源全面分析报告.md:516:- ✗ XG API覆盖class_id/is_graduating/graduation_year
./docs/XG-API-数据源全面分析报告.md:518:- ✗ 用部门名/班级名推导class_id
./docs/XG-API-数据源全面分析报告.md:529:- ⚠️ 时效性（phone/department变更需等API同步周期）
./docs/XG-API-数据源全面分析报告.md:534:1. ✗ XG提供稳定唯一class_id，能与ClassMapping对齐
./docs/XG-API-数据源全面分析报告.md:556:**问题2：** mapper不支持department数组
./docs/XG-API-数据源全面分析报告.md:558:- 修复：取 `department[0].name`
./docs/XG-API-数据源全面分析报告.md:608:   - class_id - 审批人分配失败
./backend/apps/applications/permissions.py:2:from apps.users.class_mapping import ClassMapping
./backend/apps/applications/permissions.py:8:    if user.role == UserRole.STUDENT:
./backend/apps/applications/permissions.py:11:    if user.role == UserRole.DORM_MANAGER:
./backend/apps/applications/permissions.py:12:        return ClassMapping.objects.filter(
./backend/apps/applications/permissions.py:14:            class_id=application.class_id,
./backend/apps/applications/permissions.py:18:    if user.role == UserRole.COUNSELOR:
./backend/apps/applications/permissions.py:19:        return ClassMapping.objects.filter(
./backend/apps/applications/permissions.py:21:            class_id=application.class_id,
./backend/apps/applications/permissions.py:25:    if user.role == UserRole.DEAN:
./backend/apps/applications/serializers.py:11:        fields = ['application_id', 'student_id', 'student_name', 'class_id',
./backend/apps/applications/serializers.py:14:                            'class_id', 'status', 'created_at', 'updated_at']
./backend/apps/applications/serializers.py:23:        fields = ['application_id', 'student_id', 'student_name', 'class_id',
./backend/apps/applications/serializers.py:27:                            'class_id', 'status', 'dorm_checkout_status',
./backend/apps/applications/models.py:10:    PENDING_DEAN = 'pending_dean', '待学工部审批'
./backend/apps/applications/models.py:26:    class_id = models.CharField(max_length=50)
./backend/apps/applications/models.py:41:            ApplicationStatus.PENDING_DEAN,
./docs/discussions/ui-design-2026-06-02/10-final-consensus-dean-filing-ui.md:3:**文档编号：** 10-final-consensus-dean-filing-ui  
./docs/discussions/ui-design-2026-06-02/10-final-consensus-dean-filing-ui.md:42:**后端改动：** 无（已支持 dean 查看 status=approved）
./miniprogram/pages/student-application/student-application.ts:2:import { checkRoleAndRedirect } from '../../utils/role-guard';
./docs/数据对接说明文档.md:63:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
./docs/数据对接说明文档.md:65:| 班级ID | class_id | 文本 | 是 | 班级唯一标识（重要） | CS2022-01 |
./docs/数据对接说明文档.md:79:- `class_id` 必须全校唯一，用于映射辅导员，不能重复、变更或跨届复用
./docs/数据对接说明文档.md:92:student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
./docs/数据对接说明文档.md:108:- 确保 `class_id` 字段填写正确（后续用于匹配辅导员）
./docs/数据对接说明文档.md:165:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
./docs/数据对接说明文档.md:180:employee_id,name,department,phone,email,is_active
./docs/数据对接说明文档.md:195:学生提交申请时，系统根据学生的 `class_id` 自动查询对应的辅导员，分配审批人。
./docs/数据对接说明文档.md:201:| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2022-01 |
./docs/数据对接说明文档.md:206:- `class_id` 必须全校唯一，不能重复
./docs/数据对接说明文档.md:208:- 首版只支持一班一主辅导员，同一 `class_id` 不能出现多次
./docs/数据对接说明文档.md:216:class_id,class_name,counselor_employee_id
./docs/数据对接说明文档.md:237:- 班级映射覆盖率（所有学生的class_id都有对应辅导员）
./docs/数据对接说明文档.md:240:- 未匹配班级：学生表中的class_id在映射表中不存在
./docs/数据对接说明文档.md:242:- 重复映射：同一class_id出现多次
./docs/phase4c-xg-field-coverage.md:19:**核心结论：** XG API无法独立支持项目需求（缺失class_id/is_graduating/graduation_year等关键业务字段），只能作为补充信息源。推荐策略：CSV主导 + XG API补充。
./docs/phase4c-xg-field-coverage.md:34:| `department` | array | 100% | `[{"name": "计算机学院", "level": 2}]` | 院系（数组非字符串） |
./docs/phase4c-xg-field-coverage.md:42:- ❌ `class_id`：班级ID（审批人分配必需）
./docs/phase4c-xg-field-coverage.md:60:| `role` | string | 必填，枚举值 | student/counselor/advisor/dean/admin |
./docs/phase4c-xg-field-coverage.md:66:| `class_id` | string | 学生必填 | 班级ID，用于辅导员映射（ClassMapping） |
./docs/phase4c-xg-field-coverage.md:76:| `department` | string | 院系/部门（用于展示） |
./docs/phase4c-xg-field-coverage.md:81:**ClassMapping约束：**
./docs/phase4c-xg-field-coverage.md:82:- 学生的`class_id`必须能匹配`ClassMapping`表中的记录
./docs/phase4c-xg-field-coverage.md:83:- `ClassMapping.class_id` → `ClassMapping.counselor_id` → `User.user_id`（辅导员）
./docs/phase4c-xg-field-coverage.md:84:- 如果`class_id`缺失或无法匹配，学生申请将无法自动分配辅导员审批人
./docs/phase4c-xg-field-coverage.md:97:| `User.department` | `department` | 🟡 待确认 | **可选**。缺失则置为NULL。 |
./docs/phase4c-xg-field-coverage.md:103:| `User.role` | `user_identity` | 🔴 未确认 | **必填，高风险**。<br>- 需live确认`user_identity`值域（可能是1/2/3或student/teacher/staff）<br>- **初期策略：只接受明确的"学生"值，其他值一律跳过**<br>- 跳过原因：`unknown_user_identity: {value}` |
./docs/phase4c-xg-field-coverage.md:119:| `User.class_id` | 未知 | 🔴 缺失 | **学生必填，API无法提供**。<br>- 继续由CSV/手工维护<br>- API同步时不覆盖此字段<br>- 新用户如果缺失`class_id`，标记为`skip_reason: missing_class_id` |
./docs/phase4c-xg-field-coverage.md:146:| `department`缺失 | 置为NULL（新用户）或保持原值（已存在用户） |
./docs/phase4c-xg-field-coverage.md:147:| `class_id`缺失 | 保持原值（不覆盖），新用户跳过并标记`missing_class_id` |
./docs/phase4c-xg-field-coverage.md:161:      "skip_reason": "missing_class_id",
./docs/phase4c-xg-field-coverage.md:171:    "missing_class_id": 1
./docs/phase4c-xg-field-coverage.md:188:| **CSV导入（主）** | `user_id`, `name`, `role`, `class_id`, `is_graduating`, `graduation_year` | 学生创建和核心业务字段由CSV维护 |
./docs/phase4c-xg-field-coverage.md:189:| **学工API（补充）** | `phone`, `email`, `department`, `updated_at` | API仅补充或更新非核心字段 |
./docs/phase4c-xg-field-coverage.md:194:- CSV导入创建所有学生用户（包含`class_id`/`is_graduating`/`graduation_year`）
./docs/phase4c-xg-field-coverage.md:195:- 学工API同步仅更新已存在用户的`phone`/`email`/`department`
./docs/phase4c-xg-field-coverage.md:196:- 学工API **不创建新用户**（因为缺少`class_id`等必填字段）
./docs/phase4c-xg-field-coverage.md:199:- 前提：live测试确认学工API能提供`class_id`/`is_graduating`/`graduation_year`
./docs/phase4c-xg-field-coverage.md:227:    "department": "计算机学院",
./docs/phase4c-xg-field-coverage.md:253:    "role": "student",
./docs/phase4c-xg-field-coverage.md:255:    "department": "计算机学院",
./docs/phase4c-xg-field-coverage.md:256:    "class_id": None,  # API不提供
./docs/phase4c-xg-field-coverage.md:266:    "role": None,
./docs/phase4c-xg-field-coverage.md:268:    "department": None,
./docs/phase4c-xg-field-coverage.md:269:    "class_id": None,
./docs/phase4c-xg-field-coverage.md:279:    "role": None,
./docs/phase4c-xg-field-coverage.md:281:    "department": None,
./docs/phase4c-xg-field-coverage.md:282:    "class_id": None,
./docs/phase4c-xg-field-coverage.md:314:3. 是否提供`class_id`/`is_graduating`/`graduation_year`
./docs/XG-API-COLLECTION-TEST-GUIDE.md:78:- **关联对象：** user_identity, department, parent_dep, user
./docs/用户需求最终确认与实施方案.md:50:- `class_id` 字段可为空
./docs/用户需求最终确认与实施方案.md:55:- ✓ 移除ClassMapping复杂度
./docs/用户需求最终确认与实施方案.md:66:学生提交 → 宿管员审批(by class_id) → 辅导员审批(by class_id) → 学工部审批 → 完成
./docs/用户需求最终确认与实施方案.md:75:- 移除学工部（dean）审批环节
./docs/用户需求最终确认与实施方案.md:76:- 路由方式从 `class_id` 改为 `building` + `college`
./docs/用户需求最终确认与实施方案.md:145:- **Phase 1（当前）：** 按楼栋路由（building-level）
./docs/用户需求最终确认与实施方案.md:159:| ClassMapping缺失 | ❌ 辅导员无班级映射 | 决策3：改为学院级 | ✅ 已解除 |
./docs/用户需求最终确认与实施方案.md:176:role = 'student'
./docs/用户需求最终确认与实施方案.md:179:building_name  # 楼栋名称（File1） - 第一次审批路由键
./docs/用户需求最终确认与实施方案.md:181:department     # 学院名称（File1规范化） - 第二次审批路由键
./docs/用户需求最终确认与实施方案.md:182:class_id       # 班级（可为空） - 不用于路由
./docs/用户需求最终确认与实施方案.md:195:role = 'dorm_manager'
./docs/用户需求最终确认与实施方案.md:196:building       # 负责楼栋（File3）
./docs/用户需求最终确认与实施方案.md:205:role = 'counselor'
./docs/用户需求最终确认与实施方案.md:206:department     # 负责学院（File4）
./docs/用户需求最终确认与实施方案.md:214:role = 'admin'
./docs/用户需求最终确认与实施方案.md:222:PENDING → DORM_MANAGER_APPROVED → COUNSELOR_APPROVED → DEAN_APPROVED → COMPLETED
./docs/用户需求最终确认与实施方案.md:227:PENDING → DORM_MANAGER_APPROVED → COUNSELOR_APPROVED → COMPLETED
./docs/用户需求最终确认与实施方案.md:232:- `DORM_MANAGER_APPROVED`: 宿管员已通过，等待辅导员审批
./docs/用户需求最终确认与实施方案.md:233:- `COUNSELOR_APPROVED`: 辅导员已通过，流程完成
./docs/用户需求最终确认与实施方案.md:238:**当前路由（基于ClassMapping）：**
./docs/用户需求最终确认与实施方案.md:241:    class_mapping = ClassMapping.objects.get(class_id=application.student.class_id)
./docs/用户需求最终确认与实施方案.md:244:    elif application.status == 'DORM_MANAGER_APPROVED':
./docs/用户需求最终确认与实施方案.md:253:        building = application.student.building_name
./docs/用户需求最终确认与实施方案.md:254:        dorm_managers = DormManager.objects.filter(building=building)
./docs/用户需求最终确认与实施方案.md:257:    elif application.status == 'DORM_MANAGER_APPROVED':
./docs/用户需求最终确认与实施方案.md:259:        department = application.student.department
./docs/用户需求最终确认与实施方案.md:260:        counselor = Counselor.objects.get(department=department)
./docs/用户需求最终确认与实施方案.md:317:- 移除 `DEAN_APPROVED` 状态
./docs/用户需求最终确认与实施方案.md:324:- 移除 `ClassMapping` 依赖
./docs/用户需求最终确认与实施方案.md:332:- `Student.class_id` 改为可空
./docs/用户需求最终确认与实施方案.md:333:- 确保 `Student.building_name` 和 `Student.department` 非空
./docs/用户需求最终确认与实施方案.md:353:python manage.py validate_building_routing
./docs/用户需求最终确认与实施方案.md:354:python manage.py validate_department_routing
./docs/用户需求最终确认与实施方案.md:405:    building = models.CharField(max_length=50)
./docs/用户需求最终确认与实施方案.md:410:        unique_together = ['building', 'room_number']
./docs/用户需求最终确认与实施方案.md:416:    building = application.student.building_name
./docs/用户需求最终确认与实施方案.md:421:        building=building,
./docs/用户需求最终确认与实施方案.md:489:- ⏳ `scripts/validate_building_routing.py` - 楼栋路由验证
./docs/用户需求最终确认与实施方案.md:490:- ⏳ `scripts/validate_department_routing.py` - 学院路由验证
./docs/superpowers/plans/2026-05-27-implementation-plan.md:226:   - 添加字段：student_id、role、wechat_openid等
./docs/project-completion-status-2026-06-02.md:15:- 数据库模型完整 (User, ClassMapping, Application, Approval)
./docs/project-completion-status-2026-06-02.md:30:**根本原因**: 测试setUp未创建dean用户
./docs/project-completion-status-2026-06-02.md:35:3. `test_dean_cannot_act_on_counselor_step` - dean权限测试
./docs/project-completion-status-2026-06-02.md:38:6. `test_dean_rejection` - dean驳回流程
./docs/project-completion-status-2026-06-02.md:42:**修复方案**: 在测试setUp中创建dean用户并关联到应用
./docs/project-completion-status-2026-06-02.md:51:4. `test_dean_cannot_access_non_assigned_application` - dean权限
./docs/project-completion-status-2026-06-02.md:54:7. `test_dean_sees_only_pending_dean_approvals` - dean列表过滤
./docs/project-completion-status-2026-06-02.md:55:8. `test_dean_cannot_see_other_dean_approvals` - dean权限隔离
./docs/project-completion-status-2026-06-02.md:56:9. `test_dean_sees_only_own_pending_approvals` - dean自己的审批
./docs/project-completion-status-2026-06-02.md:67:1. 批量更新测试fixture - 在所有test_*.py的setUp添加dean用户创建
./docs/project-completion-status-2026-06-02.md:115:1. **阶段1** (30分钟): 批量修复fixture问题 - 在8个测试文件添加dean用户创建
./docs/acceptance/phase4c-demo-script.md:79:print(f'Students: {User.objects.filter(role=\"student\").count()}')
./docs/acceptance/phase4c-demo-script.md:80:print(f'Counselors: {User.objects.filter(role=\"counselor\").count()}')
./docs/acceptance/phase4c-demo-script.md:81:print(f'Deans: {User.objects.filter(role=\"dean\").count()}')
./docs/acceptance/phase4c-demo-script.md:222:**预期输出：** Application status after counselor approval: pending_dean
./docs/acceptance/phase4c-demo-script.md:230:DEAN_APPROVAL_ID=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
./docs/acceptance/phase4c-demo-script.md:232:  | jq -r '.approvals[] | select(.step=="dean") | .approval_id')
./docs/acceptance/phase4c-demo-script.md:234:echo "Dean approval ID: $DEAN_APPROVAL_ID"
./docs/acceptance/phase4c-demo-script.md:237:DEAN_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
./docs/acceptance/phase4c-demo-script.md:242:echo "Dean token: ${DEAN_TOKEN:0:20}..."
./docs/acceptance/phase4c-demo-script.md:245:DEAN_APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$DEAN_APPROVAL_ID/approve/" \
./docs/acceptance/phase4c-demo-script.md:246:  -H "Authorization: Bearer $DEAN_TOKEN" \
./docs/acceptance/phase4c-demo-script.md:250:DEAN_DECISION=$(echo "$DEAN_APPROVE_RESPONSE" | jq -r '.decision')
./docs/acceptance/phase4c-demo-script.md:252:echo "Dean decision: $DEAN_DECISION"
./docs/acceptance/phase4c-demo-script.md:403:DEAN_APPROVAL_ID=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
./docs/acceptance/phase4c-demo-script.md:405:  | jq -r '.approvals[] | select(.step=="dean") | .approval_id')
./docs/acceptance/phase4c-demo-script.md:406:DEAN_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
./docs/acceptance/phase4c-demo-script.md:410:curl -s -X POST "$BASE_URL/api/approvals/$DEAN_APPROVAL_ID/approve/" \
./docs/acceptance/phase4c-demo-script.md:411:  -H "Authorization: Bearer $DEAN_TOKEN" \
./docs/acceptance/phase4c-known-issues.md:20:| 角色路由跳转 | 未验证 | 无法确认role-guard实际生效 | 模拟器/真机测试登录流程 |
./docs/api说明.txt:31:departmentId	否	string	部门Id ,查询多个用半角逗号分隔例如: 203,204
./docs/api说明.txt:32:departmentCode	否	string	部门code ,查询多个用半角逗号分隔例如: 203,204
./docs/api说明.txt:69:                        "department_code": "C100260159402712838523",
./docs/api说明.txt:84:                        "department_code": "C100261159409057535680",
./docs/api说明.txt:112:                "department": [
./docs/api说明.txt:119:                        "department_code": "C100261159409057535680",
./docs/api说明.txt:129:                            "department_id": 47
./docs/api说明.txt:185:department.name	部门名称 name
./docs/api说明.txt:186:department.third_code	部门的在对接系统中的标识/来源可能为学校自建/钉钉接入/企业微信接入
./docs/api说明.txt:187:department.department_code	当前部门的在青橄榄系统中对外提供的唯一Code
./docs/api说明.txt:188:department.level	当前部门级别
./docs/api说明.txt:189:department.parent_id	父级主键ID
./docs/api说明.txt:190:department.key	该层级所对应的路由
./docs/acceptance/phase4c-evidence-index.md:102:| `class_mappings_template.csv` | class_id, counselor_employee_id |
./docs/acceptance/phase4c-evidence-index.md:103:| `students_template.csv` | student_id, name, class_id, is_graduating, graduation_year |
./docs/XG-API数据不足解决方案讨论.md:3:**问题：** XG API缺失class_id/is_graduating/graduation_year等关键字段  
./docs/XG-API数据不足解决方案讨论.md:16:| class_id | 审批人分配失败 | ❌ 不可绕过 |
./docs/XG-API数据不足解决方案讨论.md:19:| ClassMapping | 审批链路中断 | ❌ 不可绕过 |
./docs/XG-API数据不足解决方案讨论.md:40:         → 创建ClassMapping
./docs/XG-API数据不足解决方案讨论.md:41:XG API  → 仅更新已存在用户的phone/department
./docs/XG-API数据不足解决方案讨论.md:73:- 增加`class_id`字段
./docs/XG-API数据不足解决方案讨论.md:109:- 学生学籍信息（含class_id/grade/major）
./docs/XG-API数据不足解决方案讨论.md:111:- 班级管理信息（ClassMapping）
./docs/XG-API数据不足解决方案讨论.md:184:CSV        → class_id, is_graduating, graduation_year（核心必填）
./docs/XG-API数据不足解决方案讨论.md:185:XG API     → phone, department, active（补充信息）
./docs/XG-API数据不足解决方案讨论.md:270:- [ ] 修复P1 mapper问题（user_identity/department）
./docs/XG-API数据不足解决方案讨论.md:277:- [ ] 验证ClassMapping覆盖率
./docs/XG-API数据不足解决方案讨论.md:282:- [ ] 启用API补充模式（仅更新phone/department）
./docs/XG-API数据不足解决方案讨论.md:287:- ✓ 所有学生class_id有对应ClassMapping
./docs/XG-API数据不足解决方案讨论.md:301:  - 需求：class_id, is_graduating, graduation_year
./docs/XG-API数据不足解决方案讨论.md:321:1. ✓ XG或教务API提供class_id（稳定唯一）
./docs/XG-API数据不足解决方案讨论.md:354:- **表现：** class_id填写错误、重复、格式不一致
./docs/XG-API数据不足解决方案讨论.md:389:| Week 3 | 全量数据导入 | 1000名学生账号 + ClassMapping |
./docs/XG-API数据不足解决方案讨论.md:397:- ✓ ClassMapping覆盖率 100%
./docs/acceptance/phase4c-acceptance-checklist.md:17:| 角色枚举（student/counselor/dean） | ✅ 通过 | `backend/apps/users/models.py:UserRole` |
./docs/acceptance/phase4c-acceptance-checklist.md:37:| 审批步骤（counselor/dean） | ✅ 通过 | `ApprovalStep` |
./docs/acceptance/phase4c-acceptance-checklist.md:78:| counselors.csv字段统一 | ✅ 通过 | `employee_id, name, department, is_active` |
./docs/acceptance/phase4c-acceptance-checklist.md:79:| mappings.csv字段统一 | ✅ 通过 | `class_id, counselor_employee_id` |
./docs/acceptance/phase4c-acceptance-checklist.md:80:| students.csv字段统一 | ✅ 通过 | `student_id, name, class_id, is_graduating, graduation_year` |
./docs/acceptance/phase4c-acceptance-checklist.md:190:| role-guard工具 | ✅ 通过 | `utils/role-guard.ts` |
./docs/acceptance/phase4c-acceptance-checklist.md:191:| 登录路由矩阵 | ✅ 通过 | student→student-application, counselor/dean→approvals |
./backend/apps/users/integrations/xg_user_mapper.py:15:            'role': str | None,
./backend/apps/users/integrations/xg_user_mapper.py:18:            'department': str | None,
./backend/apps/users/integrations/xg_user_mapper.py:19:            'class_id': None,  # API不提供
./backend/apps/users/integrations/xg_user_mapper.py:28:        'role': None,
./backend/apps/users/integrations/xg_user_mapper.py:31:        'department': None,
./backend/apps/users/integrations/xg_user_mapper.py:32:        'class_id': None,
./backend/apps/users/integrations/xg_user_mapper.py:44:    department_raw = xg_user.get('department')
./backend/apps/users/integrations/xg_user_mapper.py:46:    # 处理department数组: [{"name": "计算机学院", "level": 2}]
./backend/apps/users/integrations/xg_user_mapper.py:47:    department = None
./backend/apps/users/integrations/xg_user_mapper.py:48:    if isinstance(department_raw, list) and len(department_raw) > 0:
./backend/apps/users/integrations/xg_user_mapper.py:49:        if isinstance(department_raw[0], dict):
./backend/apps/users/integrations/xg_user_mapper.py:50:            department = department_raw[0].get('name')
./backend/apps/users/integrations/xg_user_mapper.py:51:    elif isinstance(department_raw, str):
./backend/apps/users/integrations/xg_user_mapper.py:53:        department = department_raw
./backend/apps/users/integrations/xg_user_mapper.py:70:    role = None
./backend/apps/users/integrations/xg_user_mapper.py:77:                role = 'student'
./backend/apps/users/integrations/xg_user_mapper.py:87:                role = 'student'
./backend/apps/users/integrations/xg_user_mapper.py:102:    result['role'] = role
./backend/apps/users/integrations/xg_user_mapper.py:105:    result['department'] = department
./docs/week3-day0-seed-data-requirements.md:29:| class_id | CS2020-01 | CS2020-02 |
./docs/week3-day0-seed-data-requirements.md:50:| role | counselor | counselor |
./docs/week3-day0-seed-data-requirements.md:69:| role | dean |
./docs/week3-day0-seed-data-requirements.md:78:### 4. 班级映射（ClassMapping）
./docs/week3-day0-seed-data-requirements.md:83:| class_id | counselor_id | counselor_name | active |
./docs/week3-day0-seed-data-requirements.md:155:- [ ] 学生1的class_id为CS2020-01
./docs/week3-day0-seed-data-requirements.md:156:- [ ] 学生2的class_id为CS2020-02
./docs/api/contract-v0.2.md:20:| `pending_dean` | Awaiting dean approval | 待学工部审批 |
./docs/api/contract-v0.2.md:41:| `dean` | Dean approval step | 学工部审批 |
./docs/api/contract-v0.2.md:65:pending_counselor ──approve──→ pending_dean ──approve──→ approved (terminal)
./docs/api/contract-v0.2.md:81:| `pending_counselor` | `pending_dean` | Counselor approves | Creates dean approval |
./docs/api/contract-v0.2.md:83:| `pending_dean` | `approved` | Dean approves | Terminal state |
./docs/api/contract-v0.2.md:84:| `pending_dean` | `rejected` | Dean rejects | Terminal state |
./docs/api/contract-v0.2.md:100:- Dean approval requires `application.status == pending_dean`
./docs/api/contract-v0.2.md:108:- Counselor approval must complete before dean approval
./docs/api/contract-v0.2.md:124:| Approve dean step | ❌ | ❌ | ✅ | Must be assigned dean |
./docs/api/contract-v0.2.md:125:| Reject dean step | ❌ | ❌ | ✅ | Must be assigned dean |
./docs/api/contract-v0.2.md:130:- Counselor operations require `user.role == COUNSELOR`
./docs/api/contract-v0.2.md:131:- Dean operations require `user.role == DEAN`
./docs/api/contract-v0.2.md:140:- Dean can only act on `step == dean`
./docs/api/contract-v0.2.md:431:  "class_id": "CS2020-01",
./docs/api/contract-v0.2.md:467:  "class_id": "CS2020-01",
./docs/api/contract-v0.2.md:470:  "status": "pending_dean",
./docs/api/contract-v0.2.md:486:      "step": "dean",
./backend/apps/users/services/xg_user_sync.py:62:            if local_user.role != 'student':
./backend/apps/users/services/xg_user_sync.py:65:                    'reason': 'role_mismatch',
./backend/apps/users/services/xg_user_sync.py:66:                    'local_role': local_user.role,
./backend/apps/users/services/xg_user_sync.py:67:                    'api_role': mapped['role']
./backend/apps/users/services/xg_user_sync.py:77:            result['warnings'].append(f"would_create_but_blocked: {user_id} (lacks class_id/is_graduating/graduation_year)")
./backend/apps/users/services/xg_user_sync.py:83:            "until User model adds phone/email/department or name overwrite policy is approved"
./backend/apps/users/services/xg_user_sync.py:138:            if local_user.role != 'student':
./backend/apps/users/services/xg_user_sync.py:141:                    'reason': 'role_mismatch',
./backend/apps/users/services/xg_user_sync.py:142:                    'local_role': local_user.role,
./backend/apps/users/services/xg_user_sync.py:143:                    'api_role': mapped['role']
./backend/apps/users/services/xg_user_sync.py:150:                local_user.department = mapped.get('department', '')
./docs/api/notification-contract-v0.1.md:64:- 正文：`您的离校申请已通过{approver_role}审批。` （approver_role: 辅导员/学工部）
./docs/api/notification-contract-v0.1.md:80:- 正文：`您的离校申请被{approver_role}驳回。驳回原因：{comment}`
./backend/apps/users/admin.py:3:from .class_mapping import ClassMapping
./backend/apps/users/admin.py:8:    list_display = ['user_id', 'name', 'role', 'class_id', 'active']
./backend/apps/users/admin.py:9:    list_filter = ['role', 'active', 'is_graduating']
./backend/apps/users/admin.py:10:    search_fields = ['user_id', 'name', 'class_id']
./backend/apps/users/admin.py:14:@admin.register(ClassMapping)
./backend/apps/users/admin.py:15:class ClassMappingAdmin(admin.ModelAdmin):
./backend/apps/users/admin.py:16:    list_display = ['class_id', 'counselor', 'counselor_name', 'active']
./backend/apps/users/admin.py:18:    search_fields = ['class_id', 'counselor__user_id', 'counselor_name']
./backend/apps/users/admin.py:19:    ordering = ['class_id']
./docs/api/contract-v0.3.md:117:- **Counselor:** Can view if active class mapping exists (`ClassMapping.objects.filter(counselor=user, class_id=application.class_id, active=True).exists()`)
./docs/api/contract-v0.3.md:118:- **Dean:** Can view if has pending dean approval (`Approval.objects.filter(application=application, approver=user, step=ApprovalStep.DEAN, decision=ApprovalDecision.PENDING).exists()`)
./docs/api/contract-v0.3-skeleton.md:122:- **Counselor:** Can view if active class mapping exists (`ClassMapping.objects.filter(counselor=user, class_id=application.class_id, active=True).exists()`)
./docs/api/contract-v0.3-skeleton.md:123:- **Dean:** Can view if has pending dean approval (`Approval.objects.filter(application=application, approver=user, step=ApprovalStep.DEAN, decision=ApprovalDecision.PENDING).exists()`)
./backend/apps/users/migrations/0001_initial.py:25:                ('role', models.CharField(choices=[('student', '学生'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20)),
./backend/apps/users/migrations/0001_initial.py:27:                ('class_id', models.CharField(blank=True, max_length=50, null=True)),
./backend/apps/users/migrations/0001_initial.py:41:            name='ClassMapping',
./backend/apps/users/migrations/0001_initial.py:43:                ('class_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
./backend/apps/users/migrations/0002_user_department_user_email_user_phone.py:15:            name='department',
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:35:### 修复2: 添加ClassMapping fixtures ✓
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:43:1. 添加import: `from apps.users.class_mapping import ClassMapping`
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:44:2. 在setUp中创建ClassMapping:
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:46:ClassMapping.objects.create(
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:47:    class_id='CS2020-01',
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:54:**效果:** 修复404错误（create_application需要ClassMapping才能正常工作）
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:103:**根因:** create_application视图需要ClassMapping，测试未创建  
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:104:**修复:** 在3个测试文件的setUp中添加ClassMapping fixture  
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:118:3. **404根因诊断:** 通过运行测试发现ClassMapping缺失导致404
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:132:- 添加ClassMapping fixtures
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:152:2. `apps/applications/tests/test_application_flow.py` - 添加ClassMapping
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:153:3. `apps/applications/tests/test_error_cases.py` - 添加ClassMapping + 修复test_dorm_blocked_error
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:154:4. `apps/approvals/tests/test_rejection_flow.py` - 添加ClassMapping
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:163:2. **测试隔离很重要:** ClassMapping缺失导致测试间相互影响
./backend/apps/users/migrations/0004_backfill_dorm_manager.py:7:    ClassMapping = apps.get_model("users", "ClassMapping")
./backend/apps/users/migrations/0004_backfill_dorm_manager.py:8:    for mapping in ClassMapping.objects.filter(dorm_manager__isnull=True):
./backend/apps/users/migrations/0004_backfill_dorm_manager.py:15:    ClassMapping = apps.get_model("users", "ClassMapping")
./backend/apps/users/migrations/0004_backfill_dorm_manager.py:16:    ClassMapping.objects.all().update(dorm_manager=None, dorm_manager_name=None)
./backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:11:        ('users', '0002_user_department_user_email_user_phone'),
./backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:27:            name='role',
./backend/apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:28:            field=models.CharField(choices=[('student', '学生'), ('dorm_manager', '宿管员'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20),
./backend/apps/users/serializers.py:9:        fields = ['user_id', 'name', 'role', 'class_id', 'active', 'is_graduating', 'graduation_year']
./backend/apps/users/serializers.py:17:        fields = ['user_id', 'name', 'role', 'class_id']
./backend/apps/users/class_mapping.py:5:class ClassMapping(models.Model):
./backend/apps/users/class_mapping.py:6:    class_id = models.CharField(max_length=50, primary_key=True)
./backend/apps/users/models.py:9:    DEAN = 'dean', '学工部'
./backend/apps/users/models.py:31:    role = models.CharField(max_length=20, choices=UserRole.choices)
./backend/apps/users/models.py:33:    class_id = models.CharField(max_length=50, null=True, blank=True)
./backend/apps/users/models.py:40:    department = models.CharField(max_length=100, null=True, blank=True)
./backend/apps/users/models.py:49:    REQUIRED_FIELDS = ['name', 'role']
./backend/apps/users/tests/test_xg_user_mapper.py:16:            'department': '计算机学院',
./backend/apps/users/tests/test_xg_user_mapper.py:24:        self.assertEqual(result['role'], 'student')
./backend/apps/users/tests/test_xg_user_mapper.py:27:        self.assertEqual(result['department'], '计算机学院')
./backend/apps/users/tests/test_xg_user_mapper.py:28:        self.assertIsNone(result['class_id'])
./backend/apps/users/tests/test_xg_user_mapper.py:43:        self.assertEqual(result['role'], 'student')
./backend/apps/users/tests/test_xg_user_mapper.py:84:        self.assertIsNone(result['role'])
./backend/apps/users/tests/test_xg_user_mapper.py:98:        self.assertIsNone(result['role'])
./backend/apps/users/tests/test_xg_user_mapper.py:113:        self.assertEqual(result['role'], 'student')
./backend/apps/users/tests/test_xg_user_mapper.py:115:        self.assertIsNone(result['department'])
./backend/apps/users/tests/test_xg_user_mapper.py:134:            'department': [{'name': '计算机学院', 'level': 2}]
./backend/apps/users/tests/test_xg_user_mapper.py:141:        self.assertEqual(result['role'], 'student')
./backend/apps/users/tests/test_xg_user_mapper.py:143:        self.assertEqual(result['department'], '计算机学院')
./backend/apps/users/tests/test_xg_user_mapper.py:146:    def test_department_array_format(self):
./backend/apps/users/tests/test_xg_user_mapper.py:147:        """测试department数组格式"""
./backend/apps/users/tests/test_xg_user_mapper.py:152:            'department': [
./backend/apps/users/tests/test_xg_user_mapper.py:161:        self.assertEqual(result['department'], '计算机学院')
./backend/apps/users/tests/test_xg_user_mapper.py:178:    def test_department_empty_array(self):
./backend/apps/users/tests/test_xg_user_mapper.py:179:        """测试department空数组"""
./backend/apps/users/tests/test_xg_user_mapper.py:184:            'department': []
./backend/apps/users/tests/test_xg_user_mapper.py:189:        self.assertIsNone(result['department'])
./backend/apps/users/tests/test_xg_user_sync.py:18:            role='student',
./backend/apps/users/tests/test_xg_user_sync.py:20:            class_id='CS2021-1',
./backend/apps/users/tests/test_xg_user_sync.py:29:            role='counselor',
./backend/apps/users/tests/test_xg_user_sync.py:59:                'department': '计算机学院'
./backend/apps/users/tests/test_xg_user_sync.py:99:    def test_local_role_conflict(self):
./backend/apps/users/tests/test_xg_user_sync.py:119:        self.assertEqual(conflict['reason'], 'role_mismatch')
./backend/apps/users/tests/test_xg_user_sync.py:120:        self.assertEqual(conflict['local_role'], 'counselor')
./backend/apps/users/tests/test_xg_user_sync.py:121:        self.assertEqual(conflict['api_role'], 'student')
./backend/apps/users/tests/test_xg_user_sync.py:127:        original_class_id = original_user.class_id
./backend/apps/users/tests/test_xg_user_sync.py:143:        self.assertEqual(user_after.class_id, original_class_id)
./backend/apps/users/tests/test_xg_user_sync.py:156:                'department': '计算机学院'
./backend/apps/users/tests/test_xg_user_sync.py:169:        self.assertIn('phone/email/department', warning_text)
./backend/apps/users/tests/test_xg_user_sync.py:234:            role='student',
./backend/apps/users/tests/test_xg_user_sync.py:236:            class_id='CS2021-1',
./backend/apps/users/tests/test_xg_user_sync.py:241:            department=''
./backend/apps/users/tests/test_xg_user_sync.py:246:            role='counselor',
./backend/apps/users/tests/test_xg_user_sync.py:258:            'department': '计算机学院'
./backend/apps/users/tests/test_xg_user_sync.py:267:        self.assertEqual(user.department, '计算机学院')
./backend/apps/users/tests/test_xg_user_sync.py:282:    def test_scenario3_skip_role_conflict(self):
./backend/apps/users/tests/test_xg_user_sync.py:283:        """场景3：检测并跳过role冲突(local非student)"""
./backend/apps/users/tests/test_xg_user_sync.py:290:        self.assertEqual(result['conflicts'][0]['reason'], 'role_mismatch')
./backend/apps/users/tests/test_xg_user_sync.py:310:            'department': '计算机学院'
./backend/apps/users/tests/test_xg_user_sync.py:319:        self.assertEqual(user.department, '')
./backend/apps/users/tests/test_xg_user_sync.py:326:            role='student',
./backend/apps/users/tests/test_xg_user_sync.py:328:            class_id='CS2021-1',
./backend/apps/users/tests/test_xg_user_sync.py:370:            role='student',
./backend/apps/users/tests/test_xg_user_sync.py:372:            class_id='CS2021-2',
./backend/apps/users/tests/test_xg_user_sync.py:383:        self.assertEqual(counselor.role, 'counselor')
./backend/apps/users/management/commands/import_csv.py:5:from apps.users.class_mapping import ClassMapping
./backend/apps/users/management/commands/import_csv.py:51:        required_fields = ['student_id', 'name', 'class_id', 'is_graduating', 'graduation_year']
./backend/apps/users/management/commands/import_csv.py:79:                    # Validate class_id has mapping
./backend/apps/users/management/commands/import_csv.py:80:                    class_id = row['class_id'].strip()
./backend/apps/users/management/commands/import_csv.py:81:                    if not dry_run and not ClassMapping.objects.filter(class_id=class_id).exists():
./backend/apps/users/management/commands/import_csv.py:82:                        summary['errors'].append(f"Row {row_num}: class_id '{class_id}' has no counselor mapping")
./backend/apps/users/management/commands/import_csv.py:97:                                'role': UserRole.STUDENT,
./backend/apps/users/management/commands/import_csv.py:98:                                'class_id': class_id,
./backend/apps/users/management/commands/import_csv.py:159:                                'role': UserRole.COUNSELOR,
./backend/apps/users/management/commands/import_csv.py:179:        required_fields = ['class_id', 'counselor_employee_id']
./backend/apps/users/management/commands/import_csv.py:200:                    class_id = row['class_id'].strip()
./backend/apps/users/management/commands/import_csv.py:201:                    if class_id in seen_ids:
./backend/apps/users/management/commands/import_csv.py:202:                        summary['errors'].append(f"Row {row_num}: Duplicate class_id '{class_id}'")
./backend/apps/users/management/commands/import_csv.py:205:                    seen_ids.add(class_id)
./backend/apps/users/management/commands/import_csv.py:211:                            counselor = User.objects.get(user_id=counselor_id, role=UserRole.COUNSELOR)
./backend/apps/users/management/commands/import_csv.py:218:                        exists = ClassMapping.objects.filter(class_id=class_id).exists()
./backend/apps/users/management/commands/import_csv.py:224:                        mapping, created = ClassMapping.objects.update_or_create(
./backend/apps/users/management/commands/import_csv.py:225:                            class_id=class_id,
./backend/apps/users/management/commands/import_csv.py:236:                        self.stdout.write(f'{"Created" if created else "Updated"} mapping: {mapping.class_id} -> {counselor.user_id}')
./backend/apps/users/tests/test_import_csv.py:8:from apps.users.class_mapping import ClassMapping
./backend/apps/users/tests/test_import_csv.py:14:        User.objects.create_user(user_id='T001', name='李老师', role=UserRole.COUNSELOR, password='T001')
./backend/apps/users/tests/test_import_csv.py:15:        User.objects.create_user(user_id='T002', name='王老师', role=UserRole.COUNSELOR, password='T002')
./backend/apps/users/tests/test_import_csv.py:26:        csv_content = "employee_id,name,department\nT003,张老师,计算机学院\nT004,赵老师,软件学院"
./backend/apps/users/tests/test_import_csv.py:33:            self.assertEqual(User.objects.filter(role=UserRole.COUNSELOR).count(), 4)
./backend/apps/users/tests/test_import_csv.py:68:        csv_content = "class_id,counselor_employee_id\nCS2020-01,T001\nCS2020-02,T002"
./backend/apps/users/tests/test_import_csv.py:75:            self.assertEqual(ClassMapping.objects.count(), 2)
./backend/apps/users/tests/test_import_csv.py:76:            mapping = ClassMapping.objects.get(class_id='CS2020-01')
./backend/apps/users/tests/test_import_csv.py:83:        csv_content = "class_id,counselor_employee_id\nCS2020-01,T999"
./backend/apps/users/tests/test_import_csv.py:93:            self.assertEqual(ClassMapping.objects.count(), 0)
./backend/apps/users/tests/test_import_csv.py:100:        ClassMapping.objects.create(class_id='CS2020-01', counselor=counselor, counselor_name='李老师')
./backend/apps/users/tests/test_import_csv.py:102:        csv_content = "student_id,name,class_id,is_graduating,graduation_year\n2020001,张三,CS2020-01,true,2024"
./backend/apps/users/tests/test_import_csv.py:109:            self.assertEqual(User.objects.filter(role=UserRole.STUDENT).count(), 1)
./backend/apps/users/tests/test_import_csv.py:112:            self.assertEqual(student.class_id, 'CS2020-01')
./backend/apps/users/tests/test_import_csv.py:119:        csv_content = "student_id,name,class_id,is_graduating,graduation_year\n2020001,张三,CS2020-99,true,2024"
./backend/apps/users/tests/test_import_csv.py:129:            self.assertEqual(User.objects.filter(role=UserRole.STUDENT).count(), 0)
./backend/apps/users/tests/test_import_csv.py:155:            initial_count = User.objects.filter(role=UserRole.COUNSELOR).count()
./backend/apps/users/tests/test_import_csv.py:161:            final_count = User.objects.filter(role=UserRole.COUNSELOR).count()
./backend/apps/users/management/commands/seed_data.py:3:from apps.users.class_mapping import ClassMapping
./backend/apps/users/management/commands/seed_data.py:29:            {'user_id': '2020001', 'name': '张三', 'class_id': 'CS2020-01'},
./backend/apps/users/management/commands/seed_data.py:30:            {'user_id': '2020002', 'name': '李四', 'class_id': 'CS2020-02'},
./backend/apps/users/management/commands/seed_data.py:31:            {'user_id': '2020003', 'name': '王五', 'class_id': 'CS2020-01'},
./backend/apps/users/management/commands/seed_data.py:32:            {'user_id': '2020004', 'name': '赵六', 'class_id': 'CS2020-01'},
./backend/apps/users/management/commands/seed_data.py:33:            {'user_id': '2020005', 'name': '孙七', 'class_id': 'CS2020-01'},
./backend/apps/users/management/commands/seed_data.py:34:            {'user_id': '2020006', 'name': '周八', 'class_id': 'CS2020-02'},
./backend/apps/users/management/commands/seed_data.py:35:            {'user_id': '2020007', 'name': '吴九', 'class_id': 'CS2020-02'},
./backend/apps/users/management/commands/seed_data.py:36:            {'user_id': '2020008', 'name': '郑十', 'class_id': 'CS2020-02'},
./backend/apps/users/management/commands/seed_data.py:37:            {'user_id': '2020009', 'name': '王十一', 'class_id': 'CS2020-02'},
./backend/apps/users/management/commands/seed_data.py:38:            {'user_id': '2020010', 'name': '王十二', 'class_id': 'CS2020-02'},
./backend/apps/users/management/commands/seed_data.py:46:                    'role': UserRole.STUDENT,
./backend/apps/users/management/commands/seed_data.py:47:                    'class_id': student_data['class_id'],
./backend/apps/users/management/commands/seed_data.py:69:                    'role': UserRole.COUNSELOR,
./backend/apps/users/management/commands/seed_data.py:89:                    'role': UserRole.DORM_MANAGER,
./backend/apps/users/management/commands/seed_data.py:103:                'role': UserRole.DEAN,
./backend/apps/users/management/commands/seed_data.py:110:            self.stdout.write(f'Created dean: {user.user_id}')
./backend/apps/users/management/commands/seed_data.py:114:            {'class_id': 'CS2020-01', 'dorm_manager_id': 'M001', 'counselor_id': 'T001'},
./backend/apps/users/management/commands/seed_data.py:115:            {'class_id': 'CS2020-02', 'dorm_manager_id': 'M002', 'counselor_id': 'T002'},
./backend/apps/users/management/commands/seed_data.py:121:            mapping, created = ClassMapping.objects.get_or_create(
./backend/apps/users/management/commands/seed_data.py:122:                class_id=mapping_data['class_id'],
./backend/apps/users/management/commands/seed_data.py:132:                self.stdout.write(f'Created mapping: {mapping.class_id} -> M:{dorm_manager.user_id}/C:{counselor.user_id}')
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:15:Step 4B应该新增并持久化`phone`、`email`、`department`三个API补充字段，但继续保持`name`、`class_id`、`is_graduating`、`graduation_year`由CSV/手工维护。这个方案与既有Phase 1策略一致：CSV负责用户创建和核心业务字段，学工API只补充联系方式/院系等非核心字段。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:25:当前`User`模型只包含`user_id/name/role/active/class_id/is_graduating/graduation_year`，mapper输出的`phone/department`无处落库。若选择“不扩展模型”，Step 4B不应改为`name`覆盖或其他轻量写入；应明确标记为跳过，保留Step 4A只读报告，并将后续Step 5命令限定为dry-run/plan命令。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:29:字段覆盖契约已经定义CSV负责`user_id/name/role/class_id/is_graduating/graduation_year`，API负责`phone/email/department`。`name`虽然来自API，但它是核心身份展示字段，且CSV导入当前会更新`name`。允许API覆盖会造成数据源权威性不清晰。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:35:字段契约包含`email`，但当前`map_xg_user_to_internal()`只提取`phone`和`department`。如果模型新增`email`，Step 4B应同步补充mapper提取和测试；否则会出现模型有字段但服务永远无法更新的半成品状态。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:50:department = models.CharField(max_length=100, null=True, blank=True)
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:77:| 角色/权限 | `role` | CSV/本地 | 只验证学生身份，冲突则跳过 |
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:78:| 业务核心 | `class_id/is_graduating/graduation_year` | CSV | 不修改 |
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:79:| 补充资料 | `phone/email/department` | 学工API | 仅更新已存在学生 |
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:89:1. User模型新增`phone/email/department`并生成migration。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:92:4. 仅对本地已存在且`role='student'`的用户更新补充字段。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:95:7. 不更新`name/class_id/is_graduating/graduation_year/role/active`。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:102:- 不扩展CSV导入器读取`phone/email/department`，除非另开CSV契约修订。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:121:1. `makemigrations`生成只包含`phone/email/department`的users migration。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:123:3. 服务测试覆盖已存在学生更新`phone/email/department`。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:128:8. 服务测试覆盖`name/class_id/is_graduating/graduation_year`不被API覆盖。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:137:当前系统未证明页面或业务流程立即需要`phone/email/department`，但字段契约和Phase 1策略已经把它们定义为API补充字段；同时这三个字段是通知、联系、展示和院系统计的自然基础字段。考虑到nullable migration风险低，且Step 4B需要真实写入目标，现在扩展是合理的。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:164:最小范围应包含`phone/email/department`三字段的真实持久化。若担心email数据源不确定，也仍建议模型包含email，mapper先按直接`email`字段提取，服务自然只在API提供非空email时更新。
./docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md:174:1. 新增`User.phone`、`User.email`、`User.department`。
./docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:113:const isOwner = userInfo.role === 'student' && detail.student_id === userInfo.user_id;
./docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:307:const isOwner = userInfo.role === 'student' && detail.student_id === userInfo.user_id;
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:35:- 阻塞解除条件：增加`phone/email/department`或批准`name`覆盖策略
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:66:4. `test_local_role_conflict`：覆盖`user_id/reason/local_role/api_role`结构，通过。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:67:5. `test_core_fields_readonly`：覆盖`class_id/is_graduating/graduation_year/name`不变，通过。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:84:完整。当前断言覆盖不创建、计数和`would_create_but_blocked`。服务warning已包含`class_id/is_graduating/graduation_year`，如需更强锁定可增加断言，但现有测试已经足够支撑Step 4A。
./docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md:142:Step 4B前置建议：优先决策User模型是否新增`phone/email/department`，以及`name`是否允许由学工API覆盖；在该决策完成前，不应把Step 4A的`would_update_count`解释为真实可写更新数。
./docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:53:- 测试或管理命令直接创建模型时，signals 可能因缺少 `ClassMapping` 而让原本合法的模型保存失败；
./docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:75:成功提交路径依赖 `ClassMapping` 找到辅导员。当前 API 已在创建申请前校验映射存在，因此在 API 路径中安全；但 signals 会对所有 `Application.objects.create` 生效，包括测试、管理命令、shell脚本。
./docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:130:3. 直接在 receiver 中导入 `Application/Approval/ClassMapping` 容易形成循环导入；应在函数内部延迟导入或把业务函数放在服务层。
./docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:175:3. 学工部通过后，学生收到一条 `APPROVAL_APPROVED` 通知，关联 dean approval。
./docs/discussions/week3-direction-2026-05-30/01-claude-proposal.md:14:- Week 2: ClassMapping模型、CSV导入命令、动态辅导员分配、CSV模板
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:15:- mapper输出phone/department
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:16:- 字段契约定义phone/email/department为API补充字段
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:26:### 问题1：是否新增phone/email/department字段？
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:29:- 新增字段：phone, email, department
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:34:- 保持当前7字段（user_id/name/role/active/class_id/is_graduating/graduation_year）
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:60:- phone/email/department可持久化
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:72:- Step 4B可持久化phone/email/department
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:74:- 核心字段（name/class_id/毕业信息）仍由CSV控制
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:100:### phone/email/department字段价值
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:108:- CSV：不包含phone/email/department
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:109:- 学工API：包含phone/department，email需补充提取
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:138:        migrations.AddField('User', 'department', CharField(max_length=100, null=True, blank=True)),
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:152:- CSV主导：user_id/name/role/class_id/is_graduating/graduation_year
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:153:- API补充：phone/email/department
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:187:### 审查要点2：phone/email/department必要性
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:214:字段契约定义phone/email/department为API补充字段，但当前系统明确需要这些字段吗？
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:240:- 只更新phone/department？
./docs/discussions/phase4c-next-steps/105-step4b-model-extension-strategy-request.md:255:   - 是否新增phone/email/department
./docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:41:- Attachment: `application.class_id == user.class_id` OR matching approval
./docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:42:- Application detail: `ClassMapping(counselor=user, class_id=application.class_id, active=True)`
./docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:56:    if user.role == UserRole.STUDENT:
./docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:59:    elif user.role == UserRole.COUNSELOR:
./docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:61:        return ClassMapping.objects.filter(
./docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:63:            class_id=application.class_id,
./docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:67:    elif user.role == UserRole.DEAN:
./docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:68:        # Must have pending dean approval
./docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:72:            step=ApprovalStep.DEAN,
./docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:22:- department: CharField(max_length=100, null=True, blank=True)
./docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:30:| 角色权限 | role | CSV/本地 | 只验证 |
./docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:31:| 业务核心 | class_id/is_graduating/graduation_year | CSV | 不修改 |
./docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:32:| 补充资料 | phone/email/department | 学工API | 仅更新已存在学生 |
./docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md:69:1. ✅ migration只包含phone/email/department
./docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:78:   - list权限 (RBAC: 学生own/辅导员class/学工部dean)
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:38:**影响范围：** 主键错误会波及`Application`、`Approval`、`Notification`、`ClassMapping`全部关联表。
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:44:**Codex指出：** 业务依赖`class_id`和`ClassMapping`做辅导员可见性控制，学工API样例未明确稳定的`class_id`字段。
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:47:- `Application.student_id` → `User.user_id` + `User.class_id` → `ClassMapping.class_id` → `User.user_id` (辅导员)
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:48:- 如果`class_id`缺失或用院系/专业/班级名称临时拼接，辅导员会看不到学生或看到错误班级
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:51:**必要动作：** 在字段契约中明确`class_id`来源，缺失时继续依赖CSV。
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:72:- `User.role`有明确值域：`student`/`counselor`/`advisor`/`dean`/`admin`
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:110:- role (必填)
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:111:- class_id (学生必填，辅导员可选)
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:115:### ClassMapping关联约束
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:116:[说明class_id必须能匹配ClassMapping]
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:123:| User.role | user_identity | 值域未知 | 只接受明确学生值；未知值跳过并报告 |
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:124:| User.class_id | 未确认 | 缺失 | 继续由CSV/手工维护，API不覆盖 |
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:163:            'role': str,
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:164:            'class_id': str | None,
./docs/discussions/phase4c-next-steps/92-claude-response-agree-step2c-lite.md:180:5. class_id缺失返回None（不阻止创建，由CSV补充）
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:34:- mapper输出phone/department/email
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:36:- 缺失：phone, email, department字段
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:42:- role
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:44:- class_id
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:51:- department（mapper输出，字段契约定义为API补充）
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:58:- Phase 1：API不创建新用户（缺class_id/is_graduating/graduation_year）
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:70:3. **角色冲突：** 本地存在但role≠student → 计入conflicts
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:72:5. **核心字段保护：** 不覆盖class_id/is_graduating/graduation_year
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:73:6. **补充字段警告：** phone/department无模型字段 → 输出warnings
./docs/discussions/phase4c-next-steps/97-consensus-step4a-first.md:101:- 给User增加phone/email/department
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:60:    if user.role == UserRole.STUDENT:
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:63:    if user.role == UserRole.COUNSELOR:
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:64:        return ClassMapping.objects.filter(
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:66:            class_id=application.class_id,
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:70:    if user.role == UserRole.DEAN:
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:74:            step=ApprovalStep.DEAN,
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:81:This must include `ApprovalDecision.PENDING` for dean access, matching current application detail behavior. A dean with historical non-pending approval should not gain attachment visibility unless Contract v0.3 deliberately changes the application-detail contract too.
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:122:- dean with pending approval allowed
./docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:123:- dean with non-pending or unrelated approval forbidden
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:24:- 当前计数：本地存在且role='student' → +1
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:25:- 问题：User模型无phone/email/department，name覆盖未决
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:99:result['warnings'].append("User model lacks phone/email/department fields - cannot persist API supplemental data")
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:106:    "until User model adds phone/email/department or name overwrite policy is approved"
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:129:   - 本地存在且role='student' → existing_count=1, would_update_count=1
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:136:4. `test_local_role_conflict`
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:137:   - 本地存在但role≠'student' → conflicts
./docs/discussions/phase4c-next-steps/100-claude-response-agree-modification.md:141:   - 服务执行后DB中class_id/is_graduating/graduation_year不变
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:14:但有一个必须先澄清并落地的小问题：`would_update_count`现在按"本地存在且role=student"计数。若该字段表示"真实可写更新数"，当前User模型没有`phone/email/department`，`name`是否允许API覆盖也未决，因此真实可更新字段数应为0。若该字段表示"未来可更新候选数"，则字段名有误导性，测试必须明确锁定这个语义。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:24:**问题描述：** 当前实现只要本地用户存在且角色为`student`，就执行`would_update_count += 1`。这符合文档97第4条"已存在学生计入would_update_count"，但与字段覆盖文档的Phase 1事实存在张力：User模型当前没有`phone/email/department`字段，`name`是否允许由API覆盖仍未决。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:30:- 保留当前计数也可以，但warning文本应更强：`would_update_count` candidates exist, but no supplemental API fields can be persisted until User model adds phone/email/department or name overwrite policy is approved。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:37:**问题描述：** 当前只有`would_update_count > 0`时才输出模型字段gap warning。若输入中只有missing_local用户，但mapper已经产出`phone/department`，仍然存在同一个字段gap和Phase 1创建阻塞问题，只是现在只有逐用户`would_create_but_blocked` warning。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:42:- 至少在`mapped_count > 0`且任一mapped结果包含`phone`或`department`时输出字段gap warning。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:63:5. 本地存在但`role != 'student'`进入`conflicts`，结构包含`user_id`、`reason`、`local_role`、`api_role`，足够支撑后续报告。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:65:7. 服务没有写DB，不会覆盖`class_id/is_graduating/graduation_year`。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:77:如果`would_update_count`表示"现有学生同步候选"，当前实现正确。如果表示"当前真实可写更新"，当前实现不准确，因为可安全写入字段未成立：`phone/email/department`不存在，`name`覆盖策略未决。建议在Step 4A把它定义为候选数，并用warning明确真实写入仍不可执行。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:81:当前结构足够：`user_id`、`reason='role_mismatch'`、`local_role`、`api_role`。可选增强是加入`name`，便于人工排查，但不应作为Step 4A阻塞项。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:91:- 服务执行后本地User的`class_id/is_graduating/graduation_year`保持不变；
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:100:2. "不覆盖class_id/is_graduating/graduation_year"：断言服务只读后DB原值不变，不要模拟Step 4B写入行为。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:101:3. "phone/department无模型字段warning"：断言warning文本明确说明不能持久化补充字段，并且不会影响`existing_count`。
./docs/discussions/phase4c-next-steps/99-step4a-implementation-codex-response.md:102:4. "混合场景"：应包含至少一个skip、一个missing_local、一个role conflict、一个existing student，并断言所有计数互不串类。
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:33:3. 本地存在但role≠student → 计入conflicts
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:35:5. phone/department无模型字段 → 输出warning
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:75:5. 不覆盖class_id/is_graduating/graduation_year
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:76:6. phone/department无模型字段warning
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:90:- API不创建新用户（缺class_id/is_graduating/graduation_year）
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:91:- mapper返回class_id=None但skip_reason=None的情况必须处理
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:102:- mapper输出phone/department
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:126:当本地用户存在且role='student'时，计入would_update。
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:135:- phone/department（模型无字段，不能写）
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:141:当本地role≠student时，计入conflicts。
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:145:- 是否包含reason（'role_mismatch'）
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:146:- 是否包含local_role和api_role用于对比
./docs/discussions/phase4c-next-steps/98-step4a-implementation-review-request.md:162:文档97要求测试"不覆盖class_id/is_graduating/graduation_year"。
./docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:35:- Counselor access checks `application.class_id == user.class_id` or matching approval.
./docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:36:- Application detail checks `ClassMapping(counselor=user, class_id=application.class_id, active=True)`.
./docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:37:- Dean attachment access allows any matching dean approval.
./docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:38:- Application detail currently allows only own pending dean approval.
./docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:68:Do not build a full role x operation matrix. It is too much for Phase 4C, and most combinations duplicate permission logic.
./docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:73:- Upload forbidden: student cannot upload to another student's application; counselor/dean cannot upload.
./docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:75:- List visibility: student own positive, student other negative, assigned counselor positive, cross-counselor negative, assigned dean positive or negative according to the final RBAC decision.
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:38:4. ✅ role conflict结构完整性
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:95:**问题1：是否新增phone/email/department字段？**
./docs/discussions/phase4c-next-steps/104-step4a-final-consensus.md:115:1. 评估phone/email/department字段业务价值
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:42:4. ✅ test_local_role_conflict - 角色冲突检测
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:67:- test_local_role_conflict通过
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:68:- conflicts结构包含user_id/reason/local_role/api_role
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:72:- class_id/is_graduating/graduation_year不变
./docs/discussions/phase4c-next-steps/102-implementation-complete-summary.md:103:- ✅ 场景4：role conflict结构
./docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:41:2. **权限链风险**：`class_id`缺失导致辅导员可见性断裂
./docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:64:| User.role | user_identity | 值域未知 | 只接受学生值；未知跳过 |
./docs/discussions/phase4c-next-steps/93-consensus-step2c-lite-first.md:65:| User.class_id | 未确认 | 缺失 | CSV维护，API不覆盖 |
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:15:1. ✅ **P1准确**：User模型缺失phone/email/department字段，mapper输出无法安全持久化
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:28:**Codex指出：** mapper输出phone/department，但User模型只到graduation_year，缺这些字段。
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:37:    role = CharField(max_length=20)
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:39:    class_id = CharField(max_length=50, null=True, blank=True)
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:42:    # 缺失: phone, email, department
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:46:- 字段契约定义phone/email/department为"API补充字段"
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:57:**Codex指出：** 字段契约说Phase 1不创建新用户，但mapper对合法学生返回class_id=None且skip_reason=None。
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:61:- 但class_id/is_graduating/graduation_year都是None
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:71:        result['warnings'].append('would_create_but_blocked: API lacks class_id')
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:110:3. 本地存在但role不是student → 计入conflicts
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:112:5. phone/department无模型字段 → 输出warning
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:121:5. 不覆盖class_id/is_graduating/graduation_year
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:122:6. phone/department无模型字段warning
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:135:- 给User增加phone/email/department字段
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:145:- 字段契约已定义phone/email/department为API补充字段
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:184:- 当前提取：number, name, user_identity, phone, department
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:201:5. ✅ 识别User模型缺phone/email/department
./docs/discussions/phase4c-next-steps/96-claude-response-agree-step4a.md:214:- 选项1：增加phone/email/department字段（推荐）
./docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:144:- `department` - 部门（数组）
./docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:149:- 是否包含班级信息？（需要class_id映射辅导员）
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:24:- department: CharField(max_length=100, null=True, blank=True)
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:31:- CSV主导：user_id/name/role/class_id/is_graduating/graduation_year
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:32:- API补充：phone/email/department
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:38:**当前状态：** mapper只提取phone/department，缺email
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:72:- 只更新已存在学生的phone/email/department
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:91:1. ✅ migration只包含phone/email/department
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:97:7. ✅ 服务测试覆盖role冲突不更新
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:165:    if local_user.role != 'student':
./docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md:171:    for field in ['phone', 'email', 'department']:
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:18:2. 字段gap warning已强化，包含候选数量、`sync candidates exist`、`no API supplemental fields can be persisted`、`phone/email/department`以及name覆盖策略未批准的阻塞说明。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:51:`plan_xg_user_sync()`当前warning已经包含`lacks class_id/is_graduating/graduation_year`，符合Phase 1不创建边界。测试目前只断言`would_create_but_blocked`。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:56:self.assertIn('class_id', warning_text)
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:87:- 缺失字段：`phone/email/department`
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:105:4. `test_local_role_conflict`：覆盖`user_id/reason/local_role/api_role`冲突结构。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:106:5. `test_core_fields_readonly`：覆盖服务执行后`class_id/is_graduating/graduation_year/name`不变。
./docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md:128:服务实现完整，测试基本完整。建议补充断言`class_id/is_graduating/graduation_year`出现在warning中，以锁定"为什么不创建"的核心字段gap。
./docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:117:字段覆盖: name=yes number=yes phone=yes department=yes user_identity=yes
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:237:2. 班级-辅导员映射表中，`class_id` 必须唯一
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:238:3. CSV导入时强校验：同一 `class_id` 不能出现多次
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:252:2. 允许同一 `class_id` 有多条记录，但只能有一个 `is_primary=true`
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:381:4. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:496:- 补充说明：`class_id` 必须唯一，不允许重复
./docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:101:- 班级 `class_id`
./docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:109:2. **业务字段层：** 宽松采样，记录 `name/number/phone/identity_id/department/user_identity/user_auth_extra_field` 是否出现，不因业务字段缺失直接失败。
./docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:134:字段: name=yes number=yes phone=yes department=yes user_identity=yes
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:24:**问题4：** `class_id`（班级ID）是否全校唯一？班级名称是否可能重复、变更或跨届复用？
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:26:**背景说明：** 系统需要用 `class_id` 作为核心键映射辅导员，如果只有班级名称，可能导致映射错误。
./docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:151:   - 班级映射覆盖率（所有学生的class_id都有对应辅导员）
./docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:73:- counselor 阶段阈值为 3 天，dean 阶段阈值为 2 天。
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:71:  if (userInfo.role !== 'student') {
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:157:if (res.user.role === 'student') {
./docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md:159:} else if (res.user.role === 'counselor' || res.user.role === 'dean') {
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:20:**Codex指出：** 文档写 `password123/counselor/dean/dorm_manager`，实际学生密码=学号，辅导员=`T001/T002`，学工部=`D001`，宿管员账号未创建
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:86:**Codex指出：** 文档说宿管员登录后进入审批列表，但 approvals.ts:19 只允许 `['counselor', 'dean']`
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:89:- miniprogram/pages/approvals/approvals.ts:19 `checkRoleAndRedirect(app.globalData.userInfo, ['counselor', 'dean'])`
./docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:109:if (checkRoleAndRedirect(app.globalData.userInfo, ['counselor', 'dean', 'dorm_manager'])) return;
./backend/reports/xg_collection_test_20260603_033437.json:67:        "department": 20,
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:47:3. 学工部通过后，学生收到一条`APPROVAL_APPROVED`通知，关联dean approval
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:113:approver_role = "辅导员" if approval.step == "counselor" else "学工部"
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:114:message = f"您的离校申请已通过{approver_role}审批。"
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:118:approver_role = "辅导员" if approval.step == "counselor" else "学工部"
./docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:119:message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:47:- 院系（department）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:73:- 宿舍信息（dorm_building, dorm_room, bed_number）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:97:- 院系（department，可选）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:119:- 院系（department）
./docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:88:- 增加强校验：必填字段、重复主键、班级映射引用辅导员存在、学生class_id有映射。
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:50:// miniprogram/utils/role-guard.ts (新建)
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:66:  if (!allowedRoles.includes(userInfo.role)) {
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:68:    const targetUrl = userInfo.role === 'student' 
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:83:import { checkRoleAndRedirect } from '../../utils/role-guard';
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:167:1. **miniprogram/utils/role-guard.ts** - 新建角色守卫函数
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:169:3. miniprogram/pages/student-application/student-application.ts - 使用role-guard + date helper
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:170:4. miniprogram/pages/approvals/approvals.ts - 使用role-guard
./docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md:171:5. miniprogram/pages/detail/detail.ts - 使用role-guard（如需要）
./docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:87:    "dorm_building": "1号楼",
./docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:100:- `room_no` → `dorm_building` + `dorm_room`
./docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:116:| dorm_building | String | 宿舍楼栋 | 是 | "1号楼" |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:44:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:46:| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2020-01 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:67:    department,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:69:    class_id,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:105:| 宿舍楼栋 | dorm_building | 文本 | 否 | 宿舍楼栋名称 | 1号楼 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:126:    dorm_building,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:159:| 院系 | department | 文本 | 否 | 所属院系 | 计算机学院 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:172:    department,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:207:| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2020-01 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:211:| 院系 | department | 文本 | 否 | 所属院系 | 计算机学院 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:221:    class_id,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:225:    department,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:385:- 学生表中的class_id必须在班级-辅导员映射表中存在
./docs/discussions/phase4c-next-steps/71-claude-response-accept-b-mini.md:38:- 阈值：counselor 3天，dean 2天
./docs/discussions/phase4c-next-steps/71-claude-response-accept-b-mini.md:87:- dean超时2天触发提醒
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:56:字段整体合理，能支撑首版业务。`student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`is_graduating` 作为必填基本可接受。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:80:3. `dorm_building`、`dorm_room`、`bed_number` 可选是可接受的，但应说明这些字段仅用于展示、核对和异常排查，业务判定不得依赖床位文本匹配。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:97:该章节是文档中最关键、也最合理的部分。`class_id` 作为必填是正确的，避免只靠班级名称匹配。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:182:3. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
./docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:172:- `test_list_dean_pending_approval_positive` ✅
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:49:    role ENUM('student', 'counselor', 'admin') NOT NULL,
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:51:    PRIMARY KEY (student_id, employee_id, role)
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:58:INSERT INTO users (student_id, name, department, ...)
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:59:SELECT student_id, name, department, ...
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:63:    department = VALUES(department),
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:70:WHERE role = 'student'
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:120:    role ENUM('student', 'counselor', 'admin') NOT NULL,
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:121:    department VARCHAR(100),
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:123:    class_id VARCHAR(50),        -- 新增（见问题3）
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:137:        (role = 'student' AND student_id IS NOT NULL AND employee_id IS NULL) OR
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:138:        (role IN ('counselor', 'admin') AND employee_id IS NOT NULL AND student_id IS NULL)
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:152:def authenticate(username, password, role):
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:153:    if role == 'student':
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:154:        user = User.query.filter_by(student_id=username, role='student').first()
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:156:        user = User.query.filter_by(employee_id=username, role=role).first()
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:165:### 2.3 问题3：class_id缺失（行381）
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:167:**Codex意见：** 班级-辅导员映射需要 `class_id` 作为核心键，但当前users表只有 `class_name`。
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:182:班级-辅导员映射表使用 `class_id`：
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:185:    class_id VARCHAR(50) PRIMARY KEY,
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:192:1. 学生提交申请时，系统需要根据 `users.class_id` 查询 `class_counselor_mapping` 确定辅导员
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:193:2. 但当前 `users` 表没有 `class_id` 字段
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:198:在 `users` 表中新增 `class_id` 字段：
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:202:ADD COLUMN class_id VARCHAR(50) AFTER major;
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:204:-- 为学生账号添加索引（辅导员/管理员的class_id为空）
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:205:CREATE INDEX idx_class_id ON users(class_id);
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:209:- `class_id`：班级唯一标识（如 `CS2022-01`），全校唯一
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:211:- 学生账号：`class_id` 必填，`class_name` 可选
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:212:- 辅导员/管理员账号：`class_id` 和 `class_name` 都为空
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:218:student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:227:    class_id=row['class_id'],      # 核心键
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:229:    role='student'
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:236:    student = User.query.filter_by(student_id=student_id, role='student').first()
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:237:    if not student or not student.class_id:
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:240:    # 根据class_id查询辅导员
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:241:    mapping = ClassCounselorMapping.query.filter_by(class_id=student.class_id).first()
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:243:        raise ValueError(f"班级 {student.class_id} 未配置辅导员")
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:247:        role='counselor'
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:328:    {"row": 12, "field": "class_id", "error": "班级ID不存在"}
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:385:        User.role == 'admin',
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:409:   - 新增 `class_id` 字段
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:437:- 新增 `class_id` 字段（必填）
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:438:- 说明 `class_id` 是班级唯一标识，用于映射辅导员
./docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:466:3. ✅ 新增 `class_id` 字段到users表
./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:195:            student__department=request.user.department
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:28:当前 `map_xg_user_to_internal()` 输出 `phone` 和 `department`，字段覆盖契约也把 `phone`、`email`、`department`定义为 API 补充字段。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:34:- `role`
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:36:- `class_id`
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:40:没有 `phone`、`email`、`department` 持久化字段。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:42:这意味着如果 Step 4 现在直接做“幂等 upsert 并写库”，实际可安全写入的 API 字段非常有限。`class_id`、`is_graduating`、`graduation_year`按共识不由 API 覆盖；`role`仅用于过滤学生；`user_id`是主键；剩下只有 `name` 可能可更新，但它属于 CSV 主导核心字段，不应在没有明确策略时被 API 静默覆盖。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:48:字段契约明确 Phase 1 中学工 API 不创建新学生，因为缺少 `class_id`、`is_graduating`、`graduation_year`。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:52:- `class_id=None`
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:90:3. 写入字段范围清晰：**目前不满足**，因为模型缺少 `phone`/`department`/`email`。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:129:- 当前没有模型字段承接 `phone`/`department`：输出 warning，不能声明可写入。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:137:- 不覆盖 `class_id`、`is_graduating`、`graduation_year`
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:138:- 无 phone/department 模型字段时输出明确 warning
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:144:1. **模型扩展路线**：给 `User` 增加 `phone`、`email`、`department` 等 API 补充字段，再实现幂等更新。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:177:   - 当前模型与字段契约不一致，不能假装 `phone`/`department` 可 upsert。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:183:   - `name`、`class_id`、毕业字段由 CSV 主导，API 覆盖必须有明确规则。
./docs/discussions/phase4c-next-steps/95-post-step3-next-priority-codex-response.md:197:1. mapper 返回 `phone`/`department` 是合理的，但 Step 4 不能把它们视为可持久化字段，除非模型扩展。
./docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:74:- 增加强校验：必填字段、重复主键、班级映射引用辅导员存在、学生class_id有映射
./docs/discussions/phase4c-next-steps/72-claude-codex-consensus-phase2b-step2-strategy.md:77:- 阈值：counselor 3天，dean 2天
./docs/discussions/phase4c-next-steps/72-claude-codex-consensus-phase2b-step2-strategy.md:106:- 覆盖：counselor/dean超时场景
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:35:- 学工文档样例字段：`name`、`number`、`phone`、`identity_id`、`department`、`user_identity`、`updated_at` 等
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:36:- 当前内部 `User` 模型字段：`user_id`、`name`、`role`、`active`、`class_id`、`is_graduating`、`graduation_year`
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:37:- 当前 CSV 导入命令的业务要求：学生导入要求 `student_id`、`name`、`class_id`、`is_graduating`、`graduation_year`
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:38:- 现有 `ClassMapping` 约束：学生 `class_id` 需要能匹配辅导员映射
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:63:   - 当前业务依赖 `class_id` 和 `ClassMapping` 做辅导员可见性控制。
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:64:   - 学工API文档样例没有明确稳定的 `class_id` 字段；如果用院系/专业/班级名称临时拼接，可能导致辅导员看不到学生或看到错误班级。
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:86:- `user_identity -> User.role` 的值域；
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:87:- `class_id` 从哪里来，学工API没有时是否继续依赖 CSV；
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:107:   - 没有 `class_id`：不可替代当前学生 CSV 主路径
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:109:   - 没有辅导员映射：不可自动创建 `ClassMapping`
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:126:| `User.role` | `user_identity` | 值域未知 | 只接受明确学生值；未知值跳过并报告 |
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:127:| `User.class_id` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:130:| `ClassMapping` | 未确认 | 缺失 | 不由学工用户API自动生成 |
./docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md:153:2. 内部 `User` / `ClassMapping` 写库字段清单
./docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:27:3. Add permission checks (role-based filtering)
./docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:41:2. Counselor attempts dean approval (403)
./docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md:50:### Tertiary: ClassMapping校验 (if time permits)
./docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:40:**Technical risk: medium.** These pages are less exposed to file API quirks, but they still depend on unverified navigation, role routing, WXML binding, and approval action behavior.
./docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:119:- Counselor/dean can view/download according to backend RBAC.
./docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md:35:   - 学工部仅看 `approver=user + step=dean + decision=pending`。
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:72:**场景4：test_local_role_conflict**
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:73:- 验证conflicts结构包含user_id/reason/local_role/api_role
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:76:- 验证服务执行后DB中class_id/is_graduating/graduation_year不变
./docs/discussions/phase4c-next-steps/101-implementation-review-and-test-request.md:124:**质疑：** 是否需要验证warning提示缺少class_id等核心字段？
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:75:if user.role == UserRole.STUDENT:
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:102:- 学工部: `approver=user + step=dean + decision=pending`
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:163:    if user.role == UserRole.STUDENT:
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:170:    if user.role == UserRole.COUNSELOR:
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:177:    # 学工部: 只看自己的pending dean审批
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:178:    elif user.role == UserRole.DEAN:
./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:181:            step=ApprovalStep.DEAN,
./docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:140:5. 字段采样：仅检查人员记录是否包含 `name/number/phone/identity_id/department/user_identity/updated_at` 等文档字段。
./backend/apps/attachments/tests/test_list.py:6:from apps.users.class_mapping import ClassMapping
./backend/apps/attachments/tests/test_list.py:20:            role=UserRole.STUDENT,
./backend/apps/attachments/tests/test_list.py:21:            class_id='CS2020-01',
./backend/apps/attachments/tests/test_list.py:30:            role=UserRole.STUDENT,
./backend/apps/attachments/tests/test_list.py:31:            class_id='CS2020-02',
./backend/apps/attachments/tests/test_list.py:41:            role=UserRole.COUNSELOR
./backend/apps/attachments/tests/test_list.py:48:            role=UserRole.COUNSELOR
./backend/apps/attachments/tests/test_list.py:51:        # Create dean
./backend/apps/attachments/tests/test_list.py:52:        self.dean = User.objects.create_user(
./backend/apps/attachments/tests/test_list.py:56:            role=UserRole.DEAN
./backend/apps/attachments/tests/test_list.py:60:        ClassMapping.objects.create(
./backend/apps/attachments/tests/test_list.py:61:            class_id='CS2020-01',
./backend/apps/attachments/tests/test_list.py:67:        ClassMapping.objects.create(
./backend/apps/attachments/tests/test_list.py:68:            class_id='CS2020-02',
./backend/apps/attachments/tests/test_list.py:79:            class_id='CS2020-01',
./backend/apps/attachments/tests/test_list.py:142:    def test_list_dean_archive_positive(self):
./backend/apps/attachments/tests/test_list.py:144:        self.client.force_authenticate(user=self.dean)
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:60:if user.role == UserRole.STUDENT:
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:62:elif user.role == UserRole.COUNSELOR:
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:68:elif user.role == UserRole.DEAN:
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:71:        step=ApprovalStep.DEAN,
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:111:if user.role == UserRole.STUDENT:
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:113:elif user.role == UserRole.COUNSELOR:
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:114:    class_ids = ClassMapping.objects.filter(
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:116:    ).values_list('class_id', flat=True)
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:117:    queryset = Application.objects.filter(class_id__in=class_ids)
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:118:elif user.role == UserRole.DEAN:
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:122:        step=ApprovalStep.DEAN,
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:132:- `?status=pending_dean`
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:143:            'class_id', 'reason', 'leave_date', 'status',
./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:157:      "class_id": "CS2020-01",
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:44:   - Counselor: filter by `class_id` via ClassMapping
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:50:- **[Codex constraint]** Define `?status=pending` to map to both `pending_counselor` AND `pending_dean`
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:51:- Or use real enum values: `pending_counselor`, `pending_dean`, `approved`, `rejected`
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:80:4. Dean cannot list other deans' approvals
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:81:5. List endpoints respect role-based filtering
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:107:- Document remaining work: ClassMapping validation, advanced filtering, cursor pagination
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:141:**Issue:** `Application.status` values are `pending_counselor`/`pending_dean`/`approved`/`rejected`, not single `pending`.
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:144:- Option A: Map `?status=pending` to both `pending_counselor` AND `pending_dean`
./docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:194:2. Explicit role checks (no default "show all")
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:57:- ClassMapping validation
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:73:**Impact:** Risk of implementing wrong scope for Dean role.
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:101:**With full scope (pagination, filtering, ClassMapping):** 5-6 hours
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:153:- Document remaining work (ClassMapping, advanced filtering, pagination)
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:161:List endpoints are new data exposure surface. If using `Application.objects.all()` then filtering by parameters, easy for counselor/dean to see applications they shouldn't.
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:163:**Mitigation:** Start with role-based queryset filtering, not parameter filtering.
./docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:177:ClassMapping: not in main path
./backend/apps/attachments/tests/test_delete.py:6:from apps.users.class_mapping import ClassMapping
./backend/apps/attachments/tests/test_delete.py:20:            role=UserRole.STUDENT,
./backend/apps/attachments/tests/test_delete.py:21:            class_id='CS2020-01',
./backend/apps/attachments/tests/test_delete.py:30:            role=UserRole.STUDENT,
./backend/apps/attachments/tests/test_delete.py:31:            class_id='CS2020-02',
./backend/apps/attachments/tests/test_delete.py:41:            role=UserRole.COUNSELOR
./backend/apps/attachments/tests/test_delete.py:45:        ClassMapping.objects.create(
./backend/apps/attachments/tests/test_delete.py:46:            class_id='CS2020-01',
./backend/apps/attachments/tests/test_delete.py:57:            class_id='CS2020-01',
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:22:- ✓ 学工部: approver=user + step=dean + decision=pending
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:26:- ✓ 辅导员: class_id via ClassMapping
./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:27:- ✓ 学工部: 通过自己pending dean approvals反查
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:120:   - Counselor: assigned classes only (filter by class_id via ClassMapping)
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:151:4. Dean cannot list other deans' approvals
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:152:5. List endpoints respect role-based filtering
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:181:- Document remaining work: ClassMapping validation, advanced filtering, cursor pagination
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:213:**YES.** No date range filtering, no advanced pagination, no ClassMapping validation in Day 3.
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:222:1. Start with role-based queryset filtering (not parameter filtering)
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:224:3. Add explicit permission tests for each role
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:230:if user.role == UserRole.COUNSELOR:
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:232:elif user.role == UserRole.DEAN:
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:246:2. **Explicit role checks** - No default "show all" behavior
./docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:247:3. **Permission tests** - Test each role's isolation
./backend/apps/attachments/tests/test_upload.py:6:from apps.users.class_mapping import ClassMapping
./backend/apps/attachments/tests/test_upload.py:20:            role=UserRole.STUDENT,
./backend/apps/attachments/tests/test_upload.py:21:            class_id='CS2020-01',
./backend/apps/attachments/tests/test_upload.py:31:            role=UserRole.STUDENT,
./backend/apps/attachments/tests/test_upload.py:32:            class_id='CS2020-01',
./backend/apps/attachments/tests/test_upload.py:42:            role=UserRole.COUNSELOR
./backend/apps/attachments/tests/test_upload.py:46:        ClassMapping.objects.create(
./backend/apps/attachments/tests/test_upload.py:47:            class_id='CS2020-01',
./backend/apps/attachments/tests/test_upload.py:58:            class_id='CS2020-01',
./backend/apps/attachments/tests/test_upload.py:69:            class_id='CS2020-01',
./docs/discussions/ui-design-2026-06-02/03-claude-response-to-gemini.md:93:- 当前 `app.globalData.userInfo` 结构：`{user_id, name, role}`
./docs/discussions/ui-design-2026-06-02/03-claude-response-to-gemini.md:97:  - `department: str | None`
./docs/discussions/ui-design-2026-06-02/03-claude-response-to-gemini.md:103:  1. 后端 `/auth/me` 接口补充phone/email/department字段
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:43:      "class_id": "CS2020-01",
./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:68:- 学工部: 返回待自己审批的记录（step='dean', decision='pending'）
./backend/apps/attachments/tests/test_download.py:6:from apps.users.class_mapping import ClassMapping
./backend/apps/attachments/tests/test_download.py:21:            role=UserRole.STUDENT,
./backend/apps/attachments/tests/test_download.py:22:            class_id='CS2020-01',
./backend/apps/attachments/tests/test_download.py:31:            role=UserRole.STUDENT,
./backend/apps/attachments/tests/test_download.py:32:            class_id='CS2020-02',
./backend/apps/attachments/tests/test_download.py:42:            role=UserRole.COUNSELOR
./backend/apps/attachments/tests/test_download.py:46:        ClassMapping.objects.create(
./backend/apps/attachments/tests/test_download.py:47:            class_id='CS2020-01',
./backend/apps/attachments/tests/test_download.py:58:            class_id='CS2020-01',
./backend/apps/attachments/views.py:68:    if user.role != UserRole.STUDENT or application.student_id != user.user_id:
./backend/apps/attachments/views.py:188:    if user.role != UserRole.STUDENT or attachment.application.student_id != user.user_id:
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:154:    role = models.CharField(max_length=20)
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:155:    department = models.CharField(max_length=100, null=True)
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:168:            models.Index(fields=['role']),
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:46:| 学生基本信息 | CSV/Excel 批量导入 | 教务系统 API | 首版按毕业届别导入更容易落地。字段建议包括 `student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:47:| 辅导员基本信息 | CSV/Excel 批量导入 | 人事系统 API 或手动创建 | 约 50 人规模下，批量导入足够。字段建议包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:48:| 班级-辅导员对应关系 | CSV/Excel 批量导入并强校验 | 教务系统 API | 必须优先支持。建议用 `class_id + counselor_employee_id + effective_term` 表达关系，不要只靠 `class_name`。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无审批人的学生数。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:100:1. **班级唯一标识。** 当前分析偏向 `class_name`，但班级名称可能重复、改名或跨届复用。应要求 `class_id`，`class_name` 只用于展示。
./docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md:49:  if (!userInfo || userInfo.role !== 'student') {
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:43:  "dorm_building": "1号楼",
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:133:student_id → name → class_name → dorm_building → dorm_room → bed_number → is_checked_out → ...
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:138:- 宿舍信息：dorm_building、dorm_room、bed_number
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:204:- class_name vs class_id
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:55:- 实际影响：counselor/dean访问学生申请页被踢回登录
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:67:  if (userInfo.role === 'counselor' || userInfo.role === 'dean') {
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:83:- 缺失保护：未检查`userInfo.role`
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:97:  if (userInfo.role === 'student') {
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:103:  // counselor/dean继续加载
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:104:  const roleMap: Record<string, string> = {
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:107:    dean: '院长',
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:112:    roleText: roleMap[userInfo.role] || userInfo.role,
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:125:  if (userInfo.role === 'student') {
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:192:- 扩展ApprovalListSerializer添加student_name/class_id/leave_date
./docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md:213:   - 手工验证角色保护：student不能进approvals，counselor/dean不能停留student-application
./docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:48:**Codex指出：** 系统设计文档使用is_cleared/clearance_date/room_no，数据对接文档使用is_checked_out/checkout_date/dorm_building/dorm_room。
./docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:60:  - `dorm_building` + `dorm_room`（而非room_no）
./docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:98:   - [ ] 第1638行：room_no → dorm_building（或拆分为dorm_building + dorm_room）
./docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:116:| dorm_building | String | 宿舍楼栋 | 是 | "1号楼" |
./docs/discussions/codex-review-2026-06-02/02-claude-response-migration-strategy.md:4:**Context:** Phase 4 regression testing blocker - missing dorm_manager fields in ClassMapping migration
./docs/discussions/codex-review-2026-06-02/02-claude-response-migration-strategy.md:47:   - `docker compose exec backend python manage.py shell -c "from apps.users.models import ClassMapping; print(ClassMapping.objects.count())"`
./docs/discussions/codex-review-2026-06-02/02-claude-response-migration-strategy.md:61:- Test fixtures will provide complete ClassMapping objects
./docs/discussions/codex-review-2026-06-02/02-claude-response-migration-strategy.md:91:1. Check ClassMapping table row count in Docker database
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:22:- Generated migration 0003 - added nullable dorm_manager fields to ClassMapping
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:26:- Added `ApprovalStep.DEAN` to match UserRole.DEAN
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:27:- Added `ApplicationStatus.PENDING_DEAN` for dean approval state
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:28:- Updated `Application.clean()` to include PENDING_DEAN in duplicate checks
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:31:- Added dean approval creation when counselor approves
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:42:- Tests not creating dean users in setUp()
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:49:- `test_dean_rejection` - likely missing dean user fixture
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:52:Tests checking dean-specific permissions fail, likely due to:
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:53:- Test fixtures not creating dean approval records
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:58:- `test_dean_sees_only_pending_dean_approvals`
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:59:- `test_dean_cannot_access_non_assigned_application`
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:66:**Original design:** 2-step (counselor → admin/dean)  
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:68:**Current state:** 3-step workflow implemented (dorm_manager → counselor → dean)  
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:72:1. Update test fixtures to create dean users
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:75:4. Update permission checks for dean role
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:85:5. `backend/apps/approvals/models.py` (added ApprovalStep.DEAN)
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:86:6. `backend/apps/applications/models.py` (added PENDING_DEAN, updated clean())
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:87:7. `backend/apps/approvals/views.py` (added dean approval creation)
./docs/discussions/codex-review-2026-06-02/04-phase4-progress-summary.md:94:1. Update test fixtures to create dean users
./docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:11:Phase 4 regression tests revealed **breaking changes** from adding dorm_manager step to approval workflow. The 3-step workflow (counselor → dean) was expanded to 4-step (counselor → dorm_manager → dean), but enum definitions and approval creation logic were not updated consistently.
./docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:46:self.application.status = ApplicationStatus.PENDING_DEAN
./docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:48:AttributeError: PENDING_DEAN
./docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:53:step=ApprovalStep.DEAN
./docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:55:AttributeError: DEAN
./docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:59:- `ApplicationStatus` enum missing `PENDING_DEAN` value
./docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:60:- `ApprovalStep` enum missing `DEAN` value
./docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:61:- Tests assume 3-step workflow (counselor → dean) but code now has 4-step workflow
./docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:80:1. ✓ Added `dorm_manager` fields to ClassMapping model
./docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:87:2. ✗ `ApplicationStatus` enum still has `PENDING_DEAN` instead of `PENDING_DORM_MANAGER` + `PENDING_DEAN`
./docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:96:   - Should we keep 3-step workflow (counselor → dean) and make dorm_manager optional?
./docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:97:   - Or fully implement 4-step workflow (counselor → dorm_manager → dean)?
./docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:102:   - Should we keep `PENDING_DEAN` or is it redundant with `PENDING_DORM_MANAGER`?
./docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:103:   - How should `ApprovalStep.DEAN` be handled if dorm_manager comes before dean?
./docs/discussions/codex-review-2026-06-02/03-phase4-regression-findings.md:107:   - Should we derive it from `approver.name` or from `ClassMapping.dorm_manager_name`?
./docs/操作说明书.md:22:| 学工部 (dean) | 备案查询 | 查看已通过申请，用于存档和统计 |
./docs/操作说明书.md:233:1. 输入账号：dean，密码：password123
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:88:**部分接受Codex建议，但认为Day 2不应包含ClassMapping校验。**
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:91:- ✓ `approval.step`与`user.role`匹配
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:93:- ✗ 辅导员额外校验`ClassMapping`当前映射
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:99:ClassMapping校验是**过度工程**：
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:102:- ClassMapping校验防御的是"历史/篡改approval"场景
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:115:ClassMapping校验推迟到Week 3或Day 3（如果有）。
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:118:- 学工部D001硬编码应该修复（从User表查询唯一dean）
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:395:**Codex：** ClassMapping校验、并发测试、完整smoke test  
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:415:2. **ClassMapping校验是否Day 2必须？**
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:446:2. **ClassMapping校验** - Day 2过度工程
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:466:2. ClassMapping校验是否Day 2必须？
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:53:- 未完成项只剩列表接口、完整负向smoke、ClassMapping、并发压力和清理类任务
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:57:- 重复审批仍能改变状态或重复创建dean approval
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:104:docker exec backend python manage.py shell -c "from apps.users.models import User; print(User.objects.get(user_id='2020002').class_id)"
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:115:- 防重复dean approval
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:179:- Conditional Go：Day 3只做列表接口、完整负向smoke、ClassMapping/并发/清理
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:189:3. `get_application`不再让任意counselor/dean查看所有申请
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:190:4. 审批状态机保护覆盖approve/reject，且不会重复生成dean approval
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:198:3. ClassMapping二次校验
./docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:246:- ⚠ ClassMapping二次校验
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:25:### 2. ClassMapping校验是否Day 2必须？
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:31:- ClassMapping防的是更弱、更后置的场景
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:130:3. **ClassMapping校验（可选）** - 如果业务需要
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:151:- ⚠ ClassMapping校验
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:190:- ClassMapping校验、并发测试、完整smoke test是工程完整性要求
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:197:- ClassMapping、并发测试推到Day 3或Week 3
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:206:- 接受ClassMapping推迟到Day 3/Week 3
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:23:**Codex意见：** `PRIMARY KEY (student_id, employee_id, role)` 会让可空字段隐式非空，学生没有employee_id、辅导员没有student_id，导入会冲突。
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:35:    role ENUM('student', 'counselor', 'admin') NOT NULL,
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:36:    PRIMARY KEY (student_id, employee_id, role)  -- 问题：复合主键让可空字段隐式非空
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:41:1. 学生导入：`student_id='2022001', employee_id=NULL, role='student'` → 主键包含NULL，插入失败
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:42:2. 辅导员导入：`student_id=NULL, employee_id='T001', role='counselor'` → 主键包含NULL，插入失败
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:51:    department VARCHAR(100),
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:53:    class_id VARCHAR(50),
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:66:    department VARCHAR(100),
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:73:    class_id VARCHAR(50) PRIMARY KEY,
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:86:INSERT INTO users (student_id, name, department, major, class_id, role, is_active, ...)
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:87:SELECT student_id, name, department, major, class_id, 'student', true, ...
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:91:    department = VALUES(department),
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:92:    class_id = VALUES(class_id),
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:99:WHERE role = 'student'
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:110:WHERE u.role = 'student'
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:137:    class_id VARCHAR(50) NOT NULL COMMENT '班级唯一标识',
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:152:    UNIQUE KEY uk_class_active (class_id, is_active),
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:160:    INDEX idx_class_id (class_id),
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:170:| class_id | VARCHAR(50) | 班级唯一标识，如 `CS2022-01` |
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:179:`UNIQUE KEY uk_class_active (class_id, is_active)` 确保：
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:186:def get_counselor_for_class(class_id, graduation_batch_id=None):
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:189:        class_id=class_id,
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:202:        raise ValueError(f"班级 {class_id} 未配置辅导员")
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:207:        raise ValueError(f"班级 {class_id} 的辅导员映射尚未生效")
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:209:        raise ValueError(f"班级 {class_id} 的辅导员映射已失效")
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:250:    role ENUM('student', 'counselor', 'admin') NOT NULL,
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:268:        (role = 'student' AND student_id IS NOT NULL AND employee_id IS NULL) OR
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:269:        (role IN ('counselor', 'admin') AND employee_id IS NOT NULL AND student_id IS NULL)
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:289:            role='student',
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:304:        role='student',
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:322:def authenticate(username, password, role):
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:325:    if role == 'student':
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:326:        user = User.query.filter_by(student_id=username, role='student').first()
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:328:        user = User.query.filter_by(employee_id=username, role=role).first()
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:352:### 2.4 问题4：class_id约束不完整（行135-139）
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:354:**Codex意见：** 检查约束只检查学生/员工标识互斥，没有检查学生必须有 `class_id`。
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:360:当前约束只检查 `student_id` 和 `employee_id` 互斥，未检查学生必须有 `class_id`。
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:365:-- 增强的检查约束：学生必须有student_id和class_id
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:367:    (role = 'student' AND student_id IS NOT NULL AND employee_id IS NULL AND class_id IS NOT NULL) OR
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:368:    (role IN ('counselor', 'admin') AND employee_id IS NOT NULL AND student_id IS NULL AND class_id IS NULL)
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:380:        if not row.get('class_id'):
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:381:            errors.append({"row": row_num, "field": "class_id", "error": "班级ID不能为空"})
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:418:        User.role == 'admin',
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:441:- 新增 `class_id` 字段（可空）
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:443:- 修改 `chk_user_identity` 约束：增加 `class_id` 必填检查
./docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:470:4. ✅ 增强class_id约束，确保学生必须有class_id
./docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:56:系统设计文档中的响应仍使用 `is_cleared`、`clearance_date`、`room_no`，而数据对接文档定义的是 `is_checked_out`、`checkout_date`、`dorm_building`、`dorm_room` 等字段；在补充 `class_name` 和 `bed_number` 后仍保留两套命名，会让实现方按不同文档接出不兼容的 payload。
./docs/design/2026-05-27-system-design.md:278:    role VARCHAR(20) NOT NULL COMMENT '角色: student/counselor/admin',
./docs/design/2026-05-27-system-design.md:279:    department VARCHAR(100) COMMENT '院系',
./docs/design/2026-05-27-system-design.md:289:    INDEX idx_role (role),
./docs/design/2026-05-27-system-design.md:300:- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
./docs/design/2026-05-27-system-design.md:369:    approver_role VARCHAR(20) NOT NULL COMMENT '审批人角色',
./docs/design/2026-05-27-system-design.md:387:- `approver_role`: counselor（辅导员）、admin（学工部）
./docs/design/2026-05-27-system-design.md:699:      "role": "student"
./docs/design/2026-05-27-system-design.md:915:      "department": "计算机学院"
./docs/design/2026-05-27-system-design.md:930:        "approver_role": "counselor",
./docs/design/2026-05-27-system-design.md:1289:    "role": "student",
./docs/design/2026-05-27-system-design.md:1353:def role_required(*roles):
./docs/design/2026-05-27-system-design.md:1357:            if request.user.role not in roles:
./docs/design/2026-05-27-system-design.md:1364:@role_required('counselor', 'admin')
./docs/design/2026-05-27-system-design.md:1375:        return request.user.role == 'student'
./docs/design/2026-05-27-system-design.md:1379:        return request.user.role == 'counselor'
./docs/design/2026-05-27-system-design.md:1445:    - 创建审批记录：approvals（approver_role='counselor', action='approve'）
./docs/design/2026-05-27-system-design.md:1453:    - 创建审批记录：approvals（approver_role='counselor', action='reject'）
./docs/design/2026-05-27-system-design.md:1472:    - 创建审批记录：approvals（approver_role='admin', action='approve'）
./docs/design/2026-05-27-system-design.md:1481:    - 创建审批记录：approvals（approver_role='admin', action='reject'）
./docs/design/2026-05-27-system-design.md:1534:                approver_role=app.status.replace('pending_', ''),
./docs/design/2026-05-27-system-design.md:1636:    "dorm_building": "1号楼",
./docs/design/2026-05-27-system-design.md:2339:CREATE INDEX idx_role ON users(role);
./docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:69:   - 定义StudentDTO、CounselorDTO、ClassMappingDTO
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:76:Section 4.1说明 `user` 是 `AuthUserDTO`，是 `UserDTO` 的子集，只包含 `user_id/name/role/class_id`。这解决了“登录响应到底是不是完整UserDTO”的歧义。
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:86:    role: UserRole
./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:87:    class_id: Optional[str] = None
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:58:    def fetch_class_mapping(self) -> ImportResult[ClassMappingDTO]:
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:107:    department: str
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:109:    class_id: str
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:215:        Student(student_id="2020001", name="张三", class_id="CS2020-01", is_graduating=True),
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:218:        Student(student_id="2020002", name="李四", class_id="INVALID", is_graduating=True),  # 无班级映射
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:219:        Student(student_id="2020003", name="王五", class_id="CS2020-99", is_graduating=True),  # 辅导员停用
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:220:        Student(student_id="2020004", name="赵六", class_id="CS2020-01", is_graduating=False),  # 非毕业生
./docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:221:        Student(student_id="2020005", name="钱七", class_id="CS2020-01", is_graduating=True, graduation_year=2027),  # 延期毕业
./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:33:- 状态枚举（draft/pending_counselor/pending_dean/approved/rejected）
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:99:                department="计算机学院",
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:101:                class_id="CS2020-01",
./docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:126:            dorm_building="1号楼",
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:100:- `StudentSourceProvider` / `CounselorSourceProvider` / `ClassMappingSourceProvider`
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:144:- 重复 class_id
./docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:211:│  - ClassMappingSourceProvider               │
./docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:67:**问题：** 登录响应返回部分UserDTO（只有user_id/name/role/class_id），未说明是完整DTO还是子集。
./docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:72:> **说明：** 响应中的 `user` 对象为 AuthUserDTO（UserDTO的子集），仅包含认证后必需的字段（user_id、name、role、class_id），不包含 active、is_graduating、graduation_year 等完整字段。
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:56:| 学生/用户 | student_id、name、role、class_id、is_graduating、graduation_year、active | 微信openid、手机号、完整个人档案 |
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:57:| 班级/辅导员 | class_id、counselor_id、counselor_active | 组织树、多辅导员复杂分配 |
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:61:| 认证 | login_id、role、access_token mock/JWT格式 | 微信OAuth |
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:159:1. 2020002的class_id改为CS2020-02（当前是CS2020-01）
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:167:docker exec backend python manage.py shell -c "from apps.users.models import User; print(User.objects.get(user_id='2020002').class_id)"
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:172:- 2020002的class_id为CS2020-02
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:361:- 先修复2020002的class_id（5分钟）
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:65:- 辅导员列表：GET /api/applications/?role=counselor
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:66:- 学工部列表：GET /api/applications/?role=dean
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:109:- 是否需要同时校验`class_id`？（辅导员只能审批自己班级）
./docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md:28:### 2. ClassMapping校验是否Day 2必须？
./docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md:30:**ClassMapping校验不是Day 2必须。**
./docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md:34:ClassMapping防的是更弱、更后置的场景，而且当前没有approval修改接口，Day 2不该把它当阻塞项。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:80:   - 未完成项只剩列表接口、完整负向smoke、ClassMapping、并发压力和清理类任务。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:84:   - 重复审批仍能改变状态或重复创建dean approval；
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:145:权限、`get_application`、dynamic dean、approve/reject状态机、事务、重复dean防护、唯一约束、IntegrityError处理放在1.5小时内，只有在代码结构非常顺、migration无历史数据问题、测试暂不跟进时才可能完成。更现实是2小时左右。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:201:- 防重复dean approval。
./docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:231:- 满足不可跳过项：Conditional Go，Day 3只做列表接口、完整负向smoke、ClassMapping/并发/清理。
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:124:- 辅导员通过只能创建一个dean approval
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:132:- ClassMapping二次防御
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:159:7. **dynamic dean语义风险** - 接受，必须定义多记录/缺失规则
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:191:- 可以Day 3：列表接口、完整负向场景、ClassMapping、并发测试、代码清理
./docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:202:2. **审批权限修复** - 接受，重点转为reject复核、get_application权限、dynamic dean
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:149:- 辅导员列表：GET /api/applications/?role=counselor
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:150:- 学工部列表：GET /api/applications/?role=dean
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:17:- 当前代码基线与提案一致。现有代码里 `approval.approver_id` 校验和 `approval.decision != pending` 已经存在，但事务、锁、动态 dean、数据库唯一约束仍缺失。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:42:- 重复审批返回 409，且不会重复创建 dean approval。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:56:- 权限 + get_application + dynamic dean：45-75分钟。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:57:- 状态机事务/锁/重复 dean 防护：90-120分钟。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:63:因此，4小时只能争取"核心止血 + 最低证据"；6小时更接近完成 Conditional Go。若坚持4小时，必须把列表接口、完整负向 smoke、ClassMapping防御、并发压力验证推到 Day 3。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:73:- 辅导员通过只能创建一个 dean approval。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:81:- ClassMapping二次防御校验。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:97:1. **测试基线风险。** 仓库已有 Django 测试，但现有测试数据没有明显创建 `ClassMapping`，而提交申请依赖班级映射；需要先确认测试能否通过并修正 fixture。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:98:2. **reset语义风险。** `seed_data` 当前使用 `get_or_create`，不会更新既有用户的 `class_id`；即使改成 `update_or_create`，也不一定清理 applications/approvals。重复 smoke 会被唯一约束挡住。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:100:4. **事务验证风险。** `select_for_update()` 需要在真实数据库事务中验证；如果只用普通 curl 串行验证，无法证明并发下不会重复创建 dean approval。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:103:7. **dynamic dean语义风险。** "从 User 表查询 dean"需要定义 active 条件、多个 dean 的选择规则、没有 dean 时的错误码。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:109:- **状态机保护 1小时偏乐观。** 事务、锁、状态匹配、重复 dean 防护、approve/reject 两条路径和测试至少需要 1.5-2小时。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:121:- 阶段2：assigned approver 权限覆盖 approve/reject；`get_application` 不再让任意 counselor/dean 查看所有申请。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:122:- 阶段3：审批状态机保护覆盖 approve/reject，且不会重复生成 dean approval。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:130:- ClassMapping二次校验。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:139:2. **审批权限修复：** 方向正确，但现有代码已部分实现 assigned approver 检查；剩余重点应转为 reject 复核、`get_application` 角色权限、dynamic dean 和测试。`get_application` 现在只限制学生，counselor/dean 仍可看任意申请。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:140:3. **状态机保护：** 必须覆盖 approve 和 reject。只校验重复审批不够，还要校验 step/status 匹配，例如 dean approval 不能在 `pending_counselor` 状态下被操作。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:151:- 状态机风险不只是语法不熟，而是事务边界、锁顺序、状态匹配和重复 dean 创建需要一起成立。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:154:建议新增风险：测试基线不可用、migration失败、列表接口契约冲突、动态 dean 多记录/缺失、手工验证无法证明并发正确性。
./docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:164:3. **1:15-3:15 核心一致性修复：** 权限、状态机、动态 dean、唯一约束、事务。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:24:| 测试/数据基线修复 | 未单列 | 0.5-1h | 当前测试依赖`ClassMapping`，但部分测试setUp未创建映射；host环境也未安装Django，验证入口未稳定 |
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:59:- `approval.step`与`user.role`匹配。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:61:- 对辅导员，额外校验申请班级当前仍映射给该辅导员：`ClassMapping(class_id=application.class_id, counselor=user, active=True)`。这能防止历史/篡改approval把错误辅导员写进去。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:62:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:72:- 再验证状态机：`counselor`只能处理`pending_counselor`；`dean`只能处理`pending_dean`。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:85:- **若允许驳回后重新提交：** 应使用条件唯一约束，只限制`draft/pending_counselor/pending_dean/approved`等活跃或终态成功申请；`rejected`可再次提交。或者不新建申请，而是允许在原申请上“重新提交/更新材料”。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:127:- `GET /api/applications/`根据当前登录用户角色自动过滤，不依赖`role`查询参数授权。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:130:- 学工部：只看分配给自己的`pending_dean`待办。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:131:- 返回字段包含`application_id`、`student_id/name`、`class_id`、`status`、当前待办`approval_id`。
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:138:2. **现有测试fixtures不完整。** 创建申请依赖`ClassMapping`，但部分测试未创建映射；Day 2新增测试前应先修基线。
./docs/数据确认清单.md:23:**问题4：** `class_id`（班级ID）是否全校唯一？班级名称是否可能重复、变更或跨届复用？
./docs/数据确认清单.md:25:**背景说明：** 系统需要用 `class_id` 作为核心键映射辅导员，如果只有班级名称，可能导致映射错误。
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:16:   - users表：`student_id`改为可空，新增`employee_id`和`class_id`字段
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:23:5. **约束增强**：学生必须有`class_id`，复用`system_configs`表
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:72:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:74:| 班级ID | class_id | 文本 | 是 | 班级唯一标识（核心键） | CS2022-01 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:88:- `class_id`：班级唯一标识，全校唯一，用于映射辅导员（**v2新增必填要求**）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:96:student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:160:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:172:employee_id,name,department,phone,email,is_active
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:200:| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2022-01 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:213:- `class_id`：班级唯一标识，必须全校唯一，不能重复、变更或跨届复用
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:215:- 首版只支持一班一主辅导员，同一 `class_id` 不能出现多次
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:220:class_id,class_name,counselor_employee_id
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:226:- 学生表中的 `class_id` 必须在班级映射表中存在
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:249:| 部门 | department | 文本 | 是 | 所属部门 | 学工部 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:298:    department VARCHAR(100),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:300:    class_id VARCHAR(50),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:313:    department VARCHAR(100),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:320:    class_id VARCHAR(50) PRIMARY KEY,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:335:INSERT INTO users (student_id, name, department, class_id, role, is_active, password_setup_required, ...)
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:336:SELECT student_id, name, department, class_id, 'student', true, true, ...
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:340:    department = VALUES(department),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:341:    class_id = VALUES(class_id),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:348:WHERE u.role = 'student'
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:393:    {"row": 12, "field": "class_id", "error": "班级ID不存在"}
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:520:4. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:597:- 新增 `class_id VARCHAR(50)` 字段（可空）
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:602:      (role = 'student' AND student_id IS NOT NULL AND employee_id IS NULL AND class_id IS NOT NULL) OR
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:603:      (role IN ('counselor', 'admin') AND employee_id IS NOT NULL AND student_id IS NULL AND class_id IS NULL)
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:617:    department VARCHAR(100),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:619:    class_id VARCHAR(50),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:634:    department VARCHAR(100),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:643:    class_id VARCHAR(50) PRIMARY KEY,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:652:    class_id VARCHAR(50) NOT NULL COMMENT '班级唯一标识',
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:662:    UNIQUE KEY uk_class_active (class_id, is_active),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:666:    INDEX idx_class_id (class_id),
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:723:2. ✅ 数据库模型调整：users表增加employee_id和class_id，调整约束
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:727:6. ✅ 约束增强：学生必须有class_id，复用system_configs表
./docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:167:6. **Dynamic dean查询**（最低优先级，可选优化）
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:132:class ClassMappingImportSource(ABC):
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:134:    def fetch(self) -> ImportResult[ClassMappingDTO]:
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:151:    department: str
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:153:    class_id: str
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:243:        Student(student_id="2020001", name="张三", class_id="CS2020-01", is_graduating=True),
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:246:        Student(student_id="2020002", name="李四", class_id="INVALID", is_graduating=True),  # 无班级映射
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:247:        Student(student_id="2020003", name="王五", class_id="CS2020-99", is_graduating=True),  # 辅导员停用
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:248:        Student(student_id="2020004", name="赵六", class_id="CS2020-01", is_graduating=False),  # 非毕业生
./docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:249:        Student(student_id="2020005", name="钱七", class_id="CS2020-01", is_graduating=True, graduation_year=2027),  # 延期毕业
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:57:3. **dean选择方式。** 短期可保留 `D001`，但如果实现动态查询成本很低，可以顺手修；不应阻塞核心安全项。
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:80:   approve/reject 已有 approver 和 pending 检查，但没有 `transaction.atomic()`、`select_for_update()`、application.status 与 approval.step 匹配校验，也没有防重复 dean approval 的唯一约束或查询保护。
./docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:83:   counselor/dean 仍可读取任意申请，和不可跳过项冲突。该项应保留在核心修复内，不可降级为清理项。
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:33:| 5. 学工部最终审批 | ⚠ 部分达标 | 主路径达标，但缺列表接口，dean硬编码 |
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:46:**问题：** 只按role放行，不按`approval.approver_id == request.user.user_id`校验  

codex
从代码搜索结果看，现有系统仍大量依赖 `class_id`、`ClassMapping`、`dean` 和 `pending_dean`，而方案文档把这些改造压到 1-1.5 天。这个会影响技术可行性和实施风险评分。
exec
/bin/bash -lc "rtk sed -n '1,280p' backend/apps/users/models.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserRole(models.TextChoices):
    STUDENT = 'student', '学生'
    DORM_MANAGER = 'dorm_manager', '宿管员'
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

    # API补充字段（学工系统）
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)

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
/bin/bash -lc "rtk sed -n '420,760p' docs/用户需求最终确认与实施方案.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
    mapping = DormManagerRoomMapping.objects.get(
        building=building,
        room_number=room
    )
    return mapping.dorm_manager
```

**优势：**
- 解决一对多问题
- 精确责任到人
- 避免审批冲突

**实施时间：** +1天（File3补充数据到达后）

---

## 七、风险与缓解

### 风险1: 楼栋名称不匹配

**风险描述：**
- File5楼栋名："荷园2栋"
- File3楼栋号："荷园二栋"
- 字符串不匹配导致路由失败

**缓解措施：**
- 建立楼栋名称规范化表（类似学院规范化）
- 导入前验证：所有File5楼栋能在File3中找到对应
- 提供手工映射工具

### 风险2: 多宿管员选择规则未定

**风险描述：**
- 一个楼栋有3个宿管员
- 系统不知道应该派给谁

**缓解措施（3选1）：**
- 方案A：任一人可审批（先到先得）
- 方案B：指定主责宿管员（File3补充主责标记）
- 方案C：轮值制（按时间/日期轮换）

**推荐：** 方案A（最简单）

### 风险3: 学工管理员界面开发延后

**风险描述：**
- 学工管理员数据未提供
- 全局视图界面开发滞后

**缓解措施：**
- 预留admin角色和权限
- 先开发其他3类用户界面
- 学工管理员数据到达后快速集成（+0.5天）

---

## 八、交付物清单

### 8.1 文档交付

- ✓ 本文档：用户需求最终确认与实施方案
- ⏳ 数据导入手册
- ⏳ 系统变更说明（给开发团队）
- ⏳ 测试用例文档

### 8.2 脚本交付

- ⏳ `scripts/normalize_colleges.py` - 学院规范化
- ⏳ `scripts/merge_student_data.py` - File1+File2合并
- ⏳ `scripts/validate_building_routing.py` - 楼栋路由验证
- ⏳ `scripts/validate_department_routing.py` - 学院路由验证

### 8.3 数据交付

- ⏳ `file5_students_5830.csv` - 完整学生数据
- ⏳ `file3_dorm_managers.csv` - 宿管员数据
- ⏳ `file4_counselors.csv` - 辅导员数据
- ⏳ `college_normalization_map.json` - 学院规范化映射

### 8.4 代码交付

- ⏳ 审批流程状态机修改
- ⏳ 楼栋路由器实现
- ⏳ 学院路由器实现
- ⏳ Admin角色权限实现
- ⏳ 4类用户界面实现
- ⏳ 单元测试+集成测试

---

## 九、决策记录

| 决策编号 | 决策内容 | 决策人 | 日期 | 理由 |
|---------|---------|-------|------|------|
| DEC-001 | File1为基准合并File2 | 用户 | 2026-06-05 | 保留全部5830学生 |
| DEC-002 | 班级字段暂时为空 | 用户 | 2026-06-05 | 简化导入流程 |
| DEC-003 | 2级审批（楼栋→学院） | 用户 | 2026-06-05 | 移除学工部审批 |
| DEC-004 | 新增学工管理员角色 | 用户 | 2026-06-05 | 全局数据查看需求 |
| DEC-005 | 寝室号未来补充 | 用户 | 2026-06-05 | 精确路由需求 |

---

**文档状态：** ✅ 已完成  
**下一步：** 等待用户确认是否立即开始实施  
**预期完成时间：** 2.5-3天


exec
/bin/bash -lc "rtk sed -n '1,340p' backend/apps/approvals/models.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.db import models
from apps.users.models import User
from apps.applications.models import Application


class ApprovalStep(models.TextChoices):
    DORM_MANAGER = 'dorm_manager', '宿管员'
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
/bin/bash -lc "rtk sed -n '1,320p' backend/apps/applications/models.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.db import models
from django.core.exceptions import ValidationError
from apps.users.models import User


class ApplicationStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    PENDING_DORM_MANAGER = 'pending_dorm_manager', '待宿管员审批'
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
        active_statuses = [
            ApplicationStatus.PENDING_DORM_MANAGER,
            ApplicationStatus.PENDING_COUNSELOR,
            ApplicationStatus.PENDING_DEAN,
            ApplicationStatus.APPROVED,
        ]
        if self.status in active_statuses:
            existing = Application.objects.filter(
                student=self.student,
                status__in=active_statuses
            ).exclude(application_id=self.application_id).exists()
            if existing:
                raise ValidationError('该学生已有待审批或已通过的申请，不能重复提交')

codex
后端当前模型已经有 `User.class_id` 可空，但 `Application.class_id` 仍是必填，审批步骤里也仍保留 `DEAN`。接下来我会定位创建申请、审批流转和列表权限的具体实现，用来判断方案遗漏点。
exec
/bin/bash -lc "rtk sed -n '1,340p' backend/apps/applications/views.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Application, ApplicationStatus, DormCheckoutStatus
from .serializers import ApplicationSerializer, ApplicationCreateSerializer, ApplicationListSerializer, ApplicationListResponseSerializer
from .pagination import ApplicationLimitOffsetPagination
from .providers import MockDormCheckoutProvider
from .permissions import can_view_application
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.users.models import UserRole
from apps.users.class_mapping import ClassMapping
from apps.notifications.services import notify_application_submitted
from schema import ErrorResponseSerializer
import uuid


@extend_schema(
    methods=['GET'],
    operation_id='applications_list',
    summary='获取申请列表',
    description='获取当前用户的申请列表（学生/辅导员/学工部）',
    parameters=[
        OpenApiParameter('status', OpenApiTypes.STR, description='状态过滤'),
        OpenApiParameter('limit', OpenApiTypes.INT, description='每页数量（默认20）'),
        OpenApiParameter('offset', OpenApiTypes.INT, description='偏移量（默认0）'),
    ],
    responses={
        200: ApplicationListResponseSerializer,
        403: ErrorResponseSerializer,
    },
    tags=['申请']
)
@extend_schema(
    methods=['POST'],
    operation_id='applications_create',
    summary='提交离校申请',
    description='学生提交新的离校申请',
    request=ApplicationCreateSerializer,
    responses={
        201: ApplicationSerializer,
        400: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
        409: ErrorResponseSerializer,
        422: ErrorResponseSerializer,
    },
    tags=['申请']
)
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

    # Dorm Manager: applications with own pending dorm manager approvals
    elif user.role == UserRole.DORM_MANAGER:
        pending_approvals = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.DORM_MANAGER,
            decision=ApprovalDecision.PENDING
        ).values_list('application', flat=True)
        queryset = Application.objects.filter(pk__in=pending_approvals)

    # Counselor: applications with own pending counselor approvals
    elif user.role == UserRole.COUNSELOR:
        pending_approvals = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.COUNSELOR,
            decision=ApprovalDecision.PENDING
        ).values_list('application', flat=True)
        queryset = Application.objects.filter(pk__in=pending_approvals)

    # Dean: view all approved applications (archiving role)
    elif user.role == UserRole.DEAN:
        queryset = Application.objects.filter(status=ApplicationStatus.APPROVED)

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
        status__in=[ApplicationStatus.PENDING_DORM_MANAGER, ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.APPROVED]
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

    if class_mapping.dorm_manager is None:
        return Response({'error': {'code': 'NOT_FOUND', 'message': '班级宿管员映射不存在',
                                    'details': {'class_id': user.class_id}}},
                        status=status.HTTP_404_NOT_FOUND)

    dorm_manager_name = class_mapping.dorm_manager_name or class_mapping.dorm_manager.name

    application = Application.objects.create(
        application_id=f'app_{uuid.uuid4().hex[:8]}',
        student=user,
        student_name=user.name,
        class_id=user.class_id,
        reason=serializer.validated_data['reason'],
        leave_date=serializer.validated_data['leave_date'],
        status=ApplicationStatus.PENDING_DORM_MANAGER,
        dorm_checkout_status=dorm_status.status
    )

    dorm_manager_approval = Approval.objects.create(
        approval_id=f'apv_{uuid.uuid4().hex[:8]}',
        application=application,
        step=ApprovalStep.DORM_MANAGER,
        approver=class_mapping.dorm_manager,
        approver_name=dorm_manager_name,
        decision=ApprovalDecision.PENDING
    )

    notify_application_submitted(application, dorm_manager_approval)

    return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)


@extend_schema(
    operation_id='applications_get',
    summary='获取申请详情',
    description='获取指定申请的详细信息（包括审批记录）',
    responses={
        200: ApplicationSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
    },
    tags=['申请']
)
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

    # Check permission using shared helper
    if not can_view_application(user, application):
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
                        status=status.HTTP_403_FORBIDDEN)

    return Response(ApplicationSerializer(application).data)

exec
/bin/bash -lc "rtk sed -n '1,220p' backend/apps/approvals/validators.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from apps.applications.models import ApplicationStatus


EXPECTED_STATUS_BY_STEP = {
    'dorm_manager': ApplicationStatus.PENDING_DORM_MANAGER,
    'counselor': ApplicationStatus.PENDING_COUNSELOR,
    'dean': ApplicationStatus.PENDING_DEAN,
}


def approval_step_matches_application_status(approval):
    expected_status = EXPECTED_STATUS_BY_STEP.get(approval.step)
    if expected_status is None:
        return False
    return approval.application.status == expected_status

exec
/bin/bash -lc "rtk sed -n '1,360p' backend/apps/approvals/views.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from drf_spectacular.types import OpenApiTypes as Types
from .models import Approval, ApprovalDecision, ApprovalStep
from .serializers import ApprovalSerializer, ApprovalActionSerializer, ApprovalListSerializer, ApprovalListResponseSerializer
from .pagination import ApprovalLimitOffsetPagination
from .validators import approval_step_matches_application_status
from apps.applications.models import Application, ApplicationStatus
from apps.users.models import UserRole
from apps.notifications.services import notify_approval_decided
from schema import ErrorResponseSerializer
import uuid


@extend_schema(
    operation_id='approvals_list',
    summary='获取审批列表',
    description='获取当前用户的待审批列表（辅导员或学工部）',
    parameters=[
        OpenApiParameter('decision', Types.STR, description='决策过滤：pending/approved/rejected/all（默认pending）'),
        OpenApiParameter('limit', Types.INT, description='每页数量（默认20）'),
        OpenApiParameter('offset', Types.INT, description='偏移量（默认0）'),
    ],
    responses={
        200: ApprovalListResponseSerializer,
        403: ErrorResponseSerializer,
    },
    tags=['审批']
)
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

    # 宿管员: 只看自己的dorm_manager审批
    if user.role == UserRole.DORM_MANAGER:
        queryset = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.DORM_MANAGER
        ).select_related('application', 'approver')

    # 辅导员: 只看自己的counselor审批
    elif user.role == UserRole.COUNSELOR:
        queryset = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.COUNSELOR
        ).select_related('application', 'approver')

    # 学工部: 查看所有审批（存档用）
    elif user.role == UserRole.DEAN:
        queryset = Approval.objects.all().select_related('application', 'approver')

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


@extend_schema(
    operation_id='approvals_approve',
    summary='通过审批',
    description='审批人通过指定的审批申请',
    request=ApprovalActionSerializer,
    responses={
        200: ApprovalSerializer,
        400: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
        409: ErrorResponseSerializer,
    },
    tags=['审批']
)
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
    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
                        status=status.HTTP_403_FORBIDDEN)
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

    notify_approval_decided(approval)

    application = approval.application
    if approval.step == ApprovalStep.DORM_MANAGER:
        # Check for existing counselor approval to prevent duplicates
        existing_counselor_approval = Approval.objects.filter(
            application=application,
            step=ApprovalStep.COUNSELOR
        ).exists()

        if existing_counselor_approval:
            return Response({'error': {'code': 'CONFLICT', 'message': '辅导员审批已存在，不能重复创建'}},
                            status=status.HTTP_409_CONFLICT)

        application.status = ApplicationStatus.PENDING_COUNSELOR
        application.save()

        # Get counselor from class mapping
        from apps.users.class_mapping import ClassMapping
        class_mapping = ClassMapping.objects.get(class_id=application.class_id, active=True)

        Approval.objects.create(
            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=class_mapping.counselor,
            approver_name=class_mapping.counselor_name,
            decision=ApprovalDecision.PENDING
        )
    elif approval.step == ApprovalStep.COUNSELOR:
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

        # Get first available dean user
        from apps.users.models import User
        dean_user = User.objects.filter(role=UserRole.DEAN, active=True).first()

        if not dean_user:
            return Response({'error': {'code': 'NOT_FOUND', 'message': '学工部审批人不存在'}},
                            status=status.HTTP_404_NOT_FOUND)

        Approval.objects.create(
            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
            application=application,
            step=ApprovalStep.DEAN,
            approver=dean_user,
            approver_name=dean_user.name,
            decision=ApprovalDecision.PENDING
        )
    elif approval.step == ApprovalStep.DEAN:
        application.status = ApplicationStatus.APPROVED
        application.save()

    return Response(ApprovalSerializer(approval).data)


@extend_schema(
    operation_id='approvals_reject',
    summary='驳回审批',
    description='审批人驳回指定的审批申请',
    request=ApprovalActionSerializer,
    responses={
        200: ApprovalSerializer,
        400: ErrorResponseSerializer,
        403: ErrorResponseSerializer,
        404: ErrorResponseSerializer,
        409: ErrorResponseSerializer,
    },
    tags=['审批']
)
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
    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
                        status=status.HTTP_403_FORBIDDEN)
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

    notify_approval_decided(approval)

    application = approval.application
    application.status = ApplicationStatus.REJECTED
    application.save()

    return Response(ApprovalSerializer(approval).data)

exec
/bin/bash -lc "rtk sed -n '1,320p' backend/apps/applications/serializers.py" in /home/caohui/projects/graduation-leave-system
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


class ApplicationListResponseSerializer(serializers.Serializer):
    """Schema-only: application list response with pagination"""
    count = serializers.IntegerField()
    results = ApplicationListSerializer(many=True)

codex
现有创建申请在提交时直接查 `ClassMapping` 并写入 `Application.class_id`，宿管审批通过后也从 `ClassMapping` 找辅导员；这意味着“移除 ClassMapping”不是替换一处路由函数，而是提交、流转、权限、测试和接口契约都要一起改。
exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/applications/permissions.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from apps.users.models import UserRole
from apps.users.class_mapping import ClassMapping
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision


def can_view_application(user, application):
    """Check if user can view application and its attachments."""
    if user.role == UserRole.STUDENT:
        return application.student_id == user.user_id

    if user.role == UserRole.DORM_MANAGER:
        return ClassMapping.objects.filter(
            dorm_manager=user,
            class_id=application.class_id,
            active=True
        ).exists()

    if user.role == UserRole.COUNSELOR:
        return ClassMapping.objects.filter(
            counselor=user,
            class_id=application.class_id,
            active=True
        ).exists()

    if user.role == UserRole.DEAN:
        # Dean archives completed applications and does not participate in approval.
        return application.status == 'approved'

    return False

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/users/management/commands/import_csv.py" in /home/caohui/projects/graduation-leave-system
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
                    class_id = row['class_id'].strip()
                    if class_id in seen_ids:
                        summary['errors'].append(f"Row {row_num}: Duplicate class_id '{class_id}'")
                        summary['failed'] += 1
                        continue
                    seen_ids.add(class_id)

                    # Validate counselor exists
                    counselor_id = row['counselor_employee_id'].strip()
                    if not dry_run:
                        try:
                            counselor = User.objects.get(user_id=counselor_id, role=UserRole.COUNSELOR)
                        except User.DoesNotExist:
                            summary['errors'].append(f"Row {row_num}: counselor_employee_id '{counselor_id}' not found")
                            summary['failed'] += 1
                            continue

                    if dry_run:
                        exists = ClassMapping.objects.filter(class_id=class_id).exists()
                        if exists:
                            summary['updated'] += 1
                        else:
                            summary['created'] += 1
                    else:
                        mapping, created = ClassMapping.objects.update_or_create(
                            class_id=class_id,
                            defaults={
                                'counselor': counselor,
                                'counselor_name': counselor.name,
                            }
                        )
                        if created:
                            summary['created'] += 1
                        else:
                            summary['updated'] += 1

                        self.stdout.write(f'{"Created" if created else "Updated"} mapping: {mapping.class_id} -> {counselor.user_id}')

        except FileNotFoundError:
            raise CommandError(f"File not found: {filepath}")
        except Exception as e:
            raise CommandError(f"Error importing mappings: {str(e)}")

    def print_summary(self, summary, dry_run):
        """Print import summary"""
        self.stdout.write('\n' + '='*60)
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN SUMMARY (no changes applied)'))
        else:
            self.stdout.write(self.style.SUCCESS('IMPORT SUMMARY'))
        self.stdout.write('='*60)

        for entity_type, stats in summary.items():
            if stats['created'] + stats['updated'] + stats['failed'] > 0:
                self.stdout.write(f'\n{entity_type.upper()}:')
                self.stdout.write(f'  Created: {stats["created"]}')
                self.stdout.write(f'  Updated: {stats["updated"]}')
                self.stdout.write(f'  Failed:  {stats["failed"]}')

                if stats['errors']:
                    self.stdout.write(f'\n  Errors:')

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/users/class_mapping.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.db import models
from apps.users.models import User


class ClassMapping(models.Model):
    class_id = models.CharField(max_length=50, primary_key=True)
    dorm_manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='managed_dorms', null=True, blank=True)
    dorm_manager_name = models.CharField(max_length=100, null=True, blank=True)
    counselor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='managed_classes')
    counselor_name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'class_mappings'

exec
/bin/bash -lc "rtk sed -n '1,220p' frontend/types/api.ts" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
// API Types based on v0.2 Contract
// Generated: 2026-05-31

export type UserRole = 'student' | 'counselor' | 'dean';

export type ApplicationStatus =
  | 'draft'
  | 'pending_counselor'
  | 'pending_dean'
  | 'approved'
  | 'rejected';

export type ApprovalDecision = 'pending' | 'approved' | 'rejected';

export type ApprovalStep = 'counselor' | 'dean';

// Auth
export interface LoginRequest {
  user_id: string;
  password: string;
}

export interface User {
  user_id: string;
  name: string;
  role: UserRole;
  class_id?: string | null;
}

export interface LoginResponse {
  access_token: string;
  token_type: 'Bearer';
  user: User;
}

// Applications
export interface ApplicationCreateRequest {
  reason: string;
  leave_date: string; // YYYY-MM-DD
}

export interface Application {
  application_id: string;
  student_id: string;
  student_name: string;
  class_id: string;
  reason: string;
  leave_date: string;
  status: ApplicationStatus;
  created_at: string;
  updated_at: string;
}

export interface ApplicationDetail extends Application {
  dorm_checkout_status: string;
  approvals: ApprovalDetail[];
}

// Approvals
export interface ApprovalDetail {
  approval_id: string;
  application_id: string;
  step: ApprovalStep;
  approver_id: string;
  approver_name: string;
  decision: ApprovalDecision;
  comment: string | null;
  decided_at: string | null;
}

export interface ApprovalListItem {
  approval_id: string;
  application_id: string;
  step: ApprovalStep;
  approver_id: string;
  approver_name: string;
  decision: ApprovalDecision;
  created_at: string;
}

export interface ApprovalActionRequest {
  comment?: string;
}

export interface ApprovalActionResponse {
  approval_id: string;
  decision: ApprovalDecision;
  comment: string | null;
  decided_at: string;
}

// Pagination
export interface PaginatedResponse<T> {
  count: number;
  results: T[];
}

// Errors
export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: any;
  };
}

codex
数据一致性方面，方案里的“导入前门禁”方向是对的，但它仍把 5830 全量成功路由写成假设，没有把失败阈值、规范化字典来源、重复学院/楼栋负责人规则固化为阻断条件。我会再核对已有 Excel 分析文档中的记录数和差异描述。
exec
/bin/bash -lc 'rtk nl -ba docs/用户需求最终确认与实施方案.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# 用户需求最终确认与实施方案
     2	
     3	**确认日期：** 2026-06-05  
     4	**文档类型：** 业务需求最终确认  
     5	**背景：** Excel数据源关联策略协作完成后，用户提供关键业务决策  
     6	**状态：** 所有P0阻塞已解除，可开始实施
     7	
     8	---
     9	
    10	## 数据文件映射说明
    11	
    12	本文档中引用的文件编号与实际文件对应关系：
    13	
    14	| 文件编号 | 实际文件名 | 内容说明 | 行数/记录数 |
    15	|---------|-----------|---------|-----------|
    16	| **File 1** | `1-5830名毕业生（含研究生）.xls` | 学生基准数据（含研究生） | 5830行 |
    17	| **File 2** | `2026届预计毕业生5675人.xlsx` | 学生补充数据（含学号） | 5675行 |
    18	| **File 3** | `2026年社区辅导员信息统计表.xls` | 宿管员数据（按楼栋） | 33楼栋 |
    19	| **File 4** | `2026年学院辅导员信息统计表.xls` | 辅导员数据（按学院） | 19学院 |
    20	| **File 5** | `file5_students_5830.csv` | 合并输出文件（File1+File2） | 5830行 |
    21	
    22	**说明：** File 5 是数据处理脚本的输出结果，不是原始输入文件。
    23	
    24	---
    25	
    26	## 一、用户确认的5项关键决策
    27	
    28	### 决策1: 数据合并策略
    29	
    30	**用户原文：**
    31	> "以文件1学生数据为基准，文件2学生数据作为字段补充，文件2中没有的数据，在文件1中暂时设定为空"
    32	
    33	**解读：**
    34	- File1 (5830行) 作为基准数据
    35	- File2 (5675行) 补充学号(XH)、班号(BH)等字段
    36	- File2没有的155行学生（差异部分）：补充字段留空
    37	- 271行研究生：补充字段留空（File2无研究生数据）
    38	
    39	**影响：**
    40	- ✓ 解决了"271研究生+116 File2独有学生"问题
    41	- ✓ 全部5830行学生可导入
    42	- ✓ 无需纠结匹配失败记录处理
    43	
    44	### 决策2: 班级字段处理
    45	
    46	**用户原文：**
    47	> "班级数据先设置为空"
    48	
    49	**解读：**
    50	- `class_id` 字段可为空
    51	- 不需要立即解决班级映射问题
    52	- 审批流程不依赖班级字段
    53	
    54	**影响：**
    55	- ✓ 移除ClassMapping复杂度
    56	- ✓ 简化数据导入流程
    57	- ✓ 避免班级辅导员映射争议
    58	
    59	### 决策3: 审批流程调整（重大变更）
    60	
    61	**用户原文：**
    62	> "第一次审批按楼栋数据向宿管员申请，第一次审批通过后，再按学院向辅导员发起第二次审批"
    63	
    64	**当前系统设计：**
    65	```
    66	学生提交 → 宿管员审批(by class_id) → 辅导员审批(by class_id) → 学工部审批 → 完成
    67	```
    68	
    69	**新需求：**
    70	```
    71	学生提交 → 宿管员审批(by 楼栋) → 辅导员审批(by 学院) → 完成（保存结果）
    72	```
    73	
    74	**关键变更：**
    75	- 移除学工部（dean）审批环节
    76	- 路由方式从 `class_id` 改为 `building` + `college`
    77	- 审批级数：3级 → 2级
    78	
    79	**影响：**
    80	- ⚠️ 需要修改审批流程状态机
    81	- ⚠️ 需要修改路由逻辑
    82	- ✓ 简化审批流程
    83	- ✓ 解决"楼栋跨班级"问题
    84	
    85	### 决策4: 数据持久化要求
    86	
    87	**用户原文：**
    88	> "二次审批完成后，将流程与审批结果数据进行保存"
    89	
    90	**解读：**
    91	- 保存完整审批流程记录
    92	- 保存每次审批结果（通过/驳回/意见）
    93	- 支持审批历史查询
    94	
    95	**影响：**
    96	- ✓ 当前系统已支持（Application + Approval模型）
    97	
    98	### 决策5: 新增学工管理员角色
    99	
   100	**用户原文：**
   101	> "学工管理员数据没有添加，但要保留。学工管理员不做审批，但要能查看学生离校审批的整体情况"
   102	
   103	**4类用户定义：**
   104	
   105	| 角色 | 职责 | 权限范围 |
   106	|------|------|----------|
   107	| 学生 (student) | 提交离校申请 | 查看自己的申请 |
   108	| 宿管员 (dorm_manager) | 第一次审批（按楼栋） | 只看自己负责楼栋的申请 |
   109	| 辅导员 (counselor) | 第二次审批（按学院） | 只看自己负责学院的申请 |
   110	| 学工管理员 (admin) | 查看全局数据 | 查看所有申请，但无审批权限 |
   111	
   112	**影响：**
   113	- 需要新增 `admin` 角色
   114	- 需要全局视图界面
   115	- 学工管理员数据后续提供（Excel/CSV格式）
   116	
   117	---
   118	
   119	## 二、补充确认：寝室号字段
   120	
   121	### 确认1: 楼栋审批关系
   122	
   123	**用户原文：**
   124	> "楼栋按文件5与文件3中共同的楼栋字段为审批关系设定"
   125	
   126	**解读：**
   127	- File5 (学生).楼栋名称 ↔ File3 (宿管员).楼栋号
   128	- 匹配规则：字符串精确匹配或规范化后匹配
   129	- 一个楼栋对应多个宿管员：任一人可审批（待确认）
   130	
   131	### 确认2: 寝室号未来补充
   132	
   133	**用户原文：**
   134	> "文件5的数据中应该有寝室号字段，文件3中没有，后面会再确认提交文件3的寝室号字段数据，以形成单一对应关系"
   135	
   136	**当前情况：**
   137	- File5 (学生) 有：楼栋名称 + 寝室号 ✓
   138	- File3 (宿管员) 有：楼栋号 ✓，无寝室号 ✗
   139	
   140	**未来升级：**
   141	- File3 补充寝室号字段
   142	- 路由升级：楼栋级（一对多）→ 楼栋+寝室号级（一对一）
   143	
   144	**实施策略：**
   145	- **Phase 1（当前）：** 按楼栋路由（building-level）
   146	- **Phase 2（File3补充后）：** 按楼栋+寝室号路由（room-level，精确一对一）
   147	
   148	---
   149	
   150	## 三、P0阻塞问题解决情况
   151	
   152	### Codex审查识别的P0问题
   153	
   154	| 问题 | Codex评估 | 用户决策 | 解决状态 |
   155	|------|-----------|----------|----------|
   156	| 学生数据无法关联 | ⚠️ 需增强匹配规则 | 决策1：File1为基准 | ✅ 已解除 |
   157	| 研究生缺学号/班级 | ❌ 271行缺失 | 决策1：字段留空 | ✅ 已解除 |
   158	| 班级字段缺失 | ⚠️ File1有，File2格式不同 | 决策2：暂时为空 | ✅ 已解除 |
   159	| ClassMapping缺失 | ❌ 辅导员无班级映射 | 决策3：改为学院级 | ✅ 已解除 |
   160	| 楼栋→宿管员一对多 | ⚠️ 无法确定选主规则 | 决策3：楼栋级路由 | ✅ 已解除 |
   161	| 辅导员学院级降级 | ⚠️ 需业务确认 | 决策3：确认接受 | ✅ 已解除 |
   162	
   163	**结论：所有P0阻塞已通过用户业务决策解除。**
   164	
   165	---
   166	
   167	## 四、系统设计变更需求
   168	
   169	### 4.1 数据模型调整
   170	
   171	**Student (用户表 - 学生角色)：**
   172	```python
   173	# 必填字段
   174	user_id        # 学号（File2补充，可能为空）
   175	name           # 姓名（File1）
   176	role = 'student'
   177	
   178	# 核心字段
   179	building_name  # 楼栋名称（File1） - 第一次审批路由键
   180	room_number    # 寝室号（File1） - 未来精确路由键
   181	department     # 学院名称（File1规范化） - 第二次审批路由键
   182	class_id       # 班级（可为空） - 不用于路由
   183	
   184	# 补充字段（可空）
   185	major          # 专业（File1）
   186	grade          # 年级（File1）
   187	phone          # 手机号（File2补充）
   188	email          # 邮箱（File2补充）
   189	```
   190	
   191	**DormManager (用户表 - 宿管员角色)：**
   192	```python
   193	user_id        # 工号（File3）
   194	name           # 姓名（File3）
   195	role = 'dorm_manager'
   196	building       # 负责楼栋（File3）
   197	room_numbers   # 负责寝室号列表（未来File3补充）
   198	phone          # 手机号（File3）
   199	```
   200	
   201	**Counselor (用户表 - 辅导员角色)：**
   202	```python
   203	user_id        # 工号（File4）
   204	name           # 姓名（File4）
   205	role = 'counselor'
   206	department     # 负责学院（File4）
   207	phone          # 手机号（File4）
   208	```
   209	
   210	**Admin (用户表 - 学工管理员角色)：**
   211	```python
   212	user_id        # 工号（未来提供）
   213	name           # 姓名（未来提供）
   214	role = 'admin'
   215	# 无业务范围限制，可查看全部
   216	```
   217	
   218	### 4.2 审批流程变更
   219	
   220	**当前流程（3级）：**
   221	```python
   222	PENDING → DORM_MANAGER_APPROVED → COUNSELOR_APPROVED → DEAN_APPROVED → COMPLETED
   223	```
   224	
   225	**新流程（2级）：**
   226	```python
   227	PENDING → DORM_MANAGER_APPROVED → COUNSELOR_APPROVED → COMPLETED
   228	```
   229	
   230	**状态定义：**
   231	- `PENDING`: 学生已提交，等待宿管员审批
   232	- `DORM_MANAGER_APPROVED`: 宿管员已通过，等待辅导员审批
   233	- `COUNSELOR_APPROVED`: 辅导员已通过，流程完成
   234	- `REJECTED`: 任一环节驳回
   235	
   236	### 4.3 路由逻辑变更
   237	
   238	**当前路由（基于ClassMapping）：**
   239	```python
   240	def get_approver(application):
   241	    class_mapping = ClassMapping.objects.get(class_id=application.student.class_id)
   242	    if application.status == 'PENDING':
   243	        return class_mapping.dorm_manager
   244	    elif application.status == 'DORM_MANAGER_APPROVED':
   245	        return class_mapping.counselor
   246	```
   247	
   248	**新路由（基于Building + Department）：**
   249	```python
   250	def get_approver(application):
   251	    if application.status == 'PENDING':
   252	        # 第一次审批：按楼栋查宿管员
   253	        building = application.student.building_name
   254	        dorm_managers = DormManager.objects.filter(building=building)
   255	        return dorm_managers  # 任一可审批，或按选主规则
   256	    
   257	    elif application.status == 'DORM_MANAGER_APPROVED':
   258	        # 第二次审批：按学院查辅导员
   259	        department = application.student.department
   260	        counselor = Counselor.objects.get(department=department)
   261	        return counselor
   262	```
   263	
   264	### 4.4 权限控制调整
   265	
   266	**角色权限矩阵：**
   267	
   268	| 操作 | 学生 | 宿管员 | 辅导员 | 学工管理员 |
   269	|------|------|--------|--------|------------|
   270	| 提交申请 | ✓ | ✗ | ✗ | ✗ |
   271	| 查看自己的申请 | ✓ | ✗ | ✗ | ✗ |
   272	| 第一次审批（楼栋） | ✗ | ✓ | ✗ | ✗ |
   273	| 查看楼栋范围申请 | ✗ | ✓ | ✗ | ✗ |
   274	| 第二次审批（学院） | ✗ | ✗ | ✓ | ✗ |
   275	| 查看学院范围申请 | ✗ | ✗ | ✓ | ✗ |
   276	| 查看所有申请 | ✗ | ✗ | ✗ | ✓ |
   277	| 查看统计报表 | ✗ | ✗ | ✗ | ✓ |
   278	
   279	---
   280	
   281	## 五、实施方案（最终版）
   282	
   283	### Phase 1: 数据准备与合并（0.5天）
   284	
   285	**任务1.1：学院名称规范化**
   286	```python
   287	# scripts/normalize_colleges.py
   288	COLLEGE_MAP = {
   289	    "文学院（苏东坡书院）": "文学院(苏东坡书院)",
   290	    "政法学院、纪检监察学院、知识产权学院": "政法学院",
   291	    "计算机学院": "计算机学院",  # 与File4"计算机与人工智能学院"对应
   292	    # ... 19个学院完整映射
   293	}
   294	```
   295	
   296	**任务1.2：File1 + File2合并脚本**
   297	```python
   298	# scripts/merge_student_data.py
   299	def merge_files():
   300	    # 1. 读取File1 (5830行) 作为基准
   301	    # 2. 读取File2 (5675行) 作为补充
   302	    # 3. 按"姓名+规范化学院+班级/BH"匹配（Codex推荐规则）
   303	    # 4. File2有的：补充学号、专业、班号等字段
   304	    # 5. File2没有的：对应字段留空
   305	    # 6. 输出File5 (5830行)
   306	    pass
   307	```
   308	
   309	**输出：**
   310	- `file5_students_5830.csv` - 完整学生数据
   311	- `file3_dorm_managers.csv` - 宿管员数据（33楼栋）
   312	- `file4_counselors.csv` - 辅导员数据（19学院）
   313	
   314	### Phase 2: 系统代码调整（1-1.5天）
   315	
   316	**任务2.1：审批流程修改**
   317	- 移除 `DEAN_APPROVED` 状态
   318	- 修改状态转换规则
   319	- 更新 `Application.get_next_status()` 方法
   320	
   321	**任务2.2：路由逻辑重构**
   322	- 创建 `BuildingApprovalRouter` - 楼栋→宿管员路由
   323	- 创建 `DepartmentApprovalRouter` - 学院→辅导员路由
   324	- 移除 `ClassMapping` 依赖
   325	
   326	**任务2.3：权限控制扩展**
   327	- 新增 `admin` 角色
   328	- 实现全局查看权限（无业务范围限制）
   329	- 更新权限装饰器
   330	
   331	**任务2.4：数据模型微调**
   332	- `Student.class_id` 改为可空
   333	- 确保 `Student.building_name` 和 `Student.department` 非空
   334	- 预留 `DormManager.room_numbers` 字段（未来使用）
   335	
   336	### Phase 3: 数据导入（0.5天）
   337	
   338	**导入脚本：**
   339	```bash
   340	# Step 1: 导入学生（5830行）
   341	python manage.py import_students file5_students_5830.csv \
   342	  --set-graduating=true \
   343	  --set-year=2026 \
   344	  --allow-empty-class-id
   345	
   346	# Step 2: 导入辅导员（19学院）
   347	python manage.py import_counselors file4_counselors.csv
   348	
   349	# Step 3: 导入宿管员（33楼栋）
   350	python manage.py import_dorm_managers file3_dorm_managers.csv
   351	
   352	# Step 4: 验证路由
   353	python manage.py validate_building_routing
   354	python manage.py validate_department_routing
   355	```
   356	
   357	**前置门禁：**
   358	- ✓ File5学生数 = 5830
   359	- ✓ 每个学生的楼栋能找到至少1个宿管员
   360	- ✓ 每个学生的学院能找到1个辅导员
   361	- ✓ 抽样100条验证数据一致性
   362	
   363	### Phase 4: 前端调整（0.5天）
   364	
   365	**任务4.1：用户界面区分**
   366	- 学生界面：提交申请+查看自己申请
   367	- 宿管员界面：查看楼栋范围申请+第一次审批
   368	- 辅导员界面：查看学院范围申请+第二次审批
   369	- 学工管理员界面：全局数据视图+统计报表（预留）
   370	
   371	**任务4.2：审批流程UI更新**
   372	- 移除学工部审批步骤展示
   373	- 更新进度条：2级审批
   374	- 更新审批记录显示
   375	
   376	### Phase 5: 测试验证（0.5天）
   377	
   378	**测试用例：**
   379	1. 学生提交申请
   380	2. 按楼栋路由到正确宿管员
   381	3. 宿管员审批通过
   382	4. 按学院路由到正确辅导员
   383	5. 辅导员审批通过
   384	6. 状态变为COMPLETED
   385	7. 审批记录完整保存
   386	8. 权限隔离验证（学生/宿管/辅导/管理员）
   387	
   388	**总时间：** 2.5-3天
   389	
   390	---
   391	
   392	## 六、未来升级路径（Phase 2可选）
   393	
   394	### 寝室号精确路由升级
   395	
   396	**前提：** File3补充寝室号字段后
   397	
   398	**数据模型扩展：**
   399	```python
   400	# DormManager model
   401	room_numbers = models.JSONField()  # 负责寝室号列表，如["201","202","203"]
   402	
   403	# 或创建新的映射表
   404	class DormManagerRoomMapping(models.Model):
   405	    building = models.CharField(max_length=50)
   406	    room_number = models.CharField(max_length=20)
   407	    dorm_manager = models.ForeignKey(User, on_delete=models.CASCADE)
   408	    
   409	    class Meta:
   410	        unique_together = ['building', 'room_number']
   411	```
   412	
   413	**路由逻辑升级：**
   414	```python
   415	def get_dorm_manager(application):
   416	    building = application.student.building_name
   417	    room = application.student.room_number
   418	    
   419	    # 精确匹配：楼栋+寝室号 → 唯一宿管员
   420	    mapping = DormManagerRoomMapping.objects.get(
   421	        building=building,
   422	        room_number=room
   423	    )
   424	    return mapping.dorm_manager
   425	```
   426	
   427	**优势：**
   428	- 解决一对多问题
   429	- 精确责任到人
   430	- 避免审批冲突
   431	
   432	**实施时间：** +1天（File3补充数据到达后）
   433	
   434	---
   435	
   436	## 七、风险与缓解
   437	
   438	### 风险1: 楼栋名称不匹配
   439	
   440	**风险描述：**
   441	- File5楼栋名："荷园2栋"
   442	- File3楼栋号："荷园二栋"
   443	- 字符串不匹配导致路由失败
   444	
   445	**缓解措施：**
   446	- 建立楼栋名称规范化表（类似学院规范化）
   447	- 导入前验证：所有File5楼栋能在File3中找到对应
   448	- 提供手工映射工具
   449	
   450	### 风险2: 多宿管员选择规则未定
   451	
   452	**风险描述：**
   453	- 一个楼栋有3个宿管员
   454	- 系统不知道应该派给谁
   455	
   456	**缓解措施（3选1）：**
   457	- 方案A：任一人可审批（先到先得）
   458	- 方案B：指定主责宿管员（File3补充主责标记）
   459	- 方案C：轮值制（按时间/日期轮换）
   460	
   461	**推荐：** 方案A（最简单）
   462	
   463	### 风险3: 学工管理员界面开发延后
   464	
   465	**风险描述：**
   466	- 学工管理员数据未提供
   467	- 全局视图界面开发滞后
   468	
   469	**缓解措施：**
   470	- 预留admin角色和权限
   471	- 先开发其他3类用户界面
   472	- 学工管理员数据到达后快速集成（+0.5天）
   473	
   474	---
   475	
   476	## 八、交付物清单
   477	
   478	### 8.1 文档交付
   479	
   480	- ✓ 本文档：用户需求最终确认与实施方案
   481	- ⏳ 数据导入手册
   482	- ⏳ 系统变更说明（给开发团队）
   483	- ⏳ 测试用例文档
   484	
   485	### 8.2 脚本交付
   486	
   487	- ⏳ `scripts/normalize_colleges.py` - 学院规范化
   488	- ⏳ `scripts/merge_student_data.py` - File1+File2合并
   489	- ⏳ `scripts/validate_building_routing.py` - 楼栋路由验证
   490	- ⏳ `scripts/validate_department_routing.py` - 学院路由验证
   491	
   492	### 8.3 数据交付
   493	
   494	- ⏳ `file5_students_5830.csv` - 完整学生数据
   495	- ⏳ `file3_dorm_managers.csv` - 宿管员数据
   496	- ⏳ `file4_counselors.csv` - 辅导员数据
   497	- ⏳ `college_normalization_map.json` - 学院规范化映射
   498	
   499	### 8.4 代码交付
   500	
   501	- ⏳ 审批流程状态机修改
   502	- ⏳ 楼栋路由器实现
   503	- ⏳ 学院路由器实现
   504	- ⏳ Admin角色权限实现
   505	- ⏳ 4类用户界面实现
   506	- ⏳ 单元测试+集成测试
   507	
   508	---
   509	
   510	## 九、决策记录
   511	
   512	| 决策编号 | 决策内容 | 决策人 | 日期 | 理由 |
   513	|---------|---------|-------|------|------|
   514	| DEC-001 | File1为基准合并File2 | 用户 | 2026-06-05 | 保留全部5830学生 |
   515	| DEC-002 | 班级字段暂时为空 | 用户 | 2026-06-05 | 简化导入流程 |
   516	| DEC-003 | 2级审批（楼栋→学院） | 用户 | 2026-06-05 | 移除学工部审批 |
   517	| DEC-004 | 新增学工管理员角色 | 用户 | 2026-06-05 | 全局数据查看需求 |
   518	| DEC-005 | 寝室号未来补充 | 用户 | 2026-06-05 | 精确路由需求 |
   519	
   520	---
   521	
   522	**文档状态：** ✅ 已完成  
   523	**下一步：** 等待用户确认是否立即开始实施  
   524	**预期完成时间：** 2.5-3天
   525	

exec
/bin/bash -lc 'rtk rg -n "5830|5675|271|155|116|File 1|File1|File 2|File2|楼栋|学院|宿管|辅导员" docs/Excel数据源实际分析结果.md docs/Excel数据源分析与需求对比.md docs/数据对接说明文档.md docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:14:1. **班级-辅导员对应关系应明确列为 P0。** 这是自动分配审批人的核心数据。没有它，系统提交申请时无法稳定设置 `counselor_id` 和 `current_approver_id`，只能退化为人工逐个配置或人工改派。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:15:2. **首版不应追求所有数据源 API 化。** 对约 1000 名学生、约 50 名辅导员、约 5 名管理员的规模，CSV/Excel 批量导入加严格校验更现实；API 更适合作为后续自动化增强。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:26:| 辅导员基本信息 | 人事系统或人工台账 | P0 | 用于创建 counselor 账号和审批权限主体。实时同步不是 P0，但账号数据本身是 P0。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:28:| 宿舍清退数据 | 宿管系统 | P0 | 当前业务把宿舍清退作为提交前校验项，现有对接文档已覆盖。即使保留人工证明降级，正式流程仍应具备自动校验或批量数据导入能力。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:47:| 辅导员基本信息 | CSV/Excel 批量导入 | 人事系统 API 或手动创建 | 约 50 人规模下，批量导入足够。字段建议包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:48:| 班级-辅导员对应关系 | CSV/Excel 批量导入并强校验 | 教务系统 API | 必须优先支持。建议用 `class_id + counselor_employee_id + effective_term` 表达关系，不要只靠 `class_name`。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无审批人的学生数。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:49:| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入、人工证明降级 | 当前文档策略合理。提交申请时实时性较强，API 价值高；若宿管系统暂不支持 API，则每日文件导入加人工证明降级。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:63:原因不是“方便展示”，而是学生账号、身份识别、申请资格、班级映射都依赖它。当前数据对接文档的目标用户也应从“宿舍管理系统管理员”扩展为“教务系统、人事系统、宿管系统及业务数据负责人”。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:65:### 2. 辅导员数据源如何对接？
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:69:理由是辅导员规模约 50 人，变化频率低，API 改造投入可能高于收益。但数据结构必须标准化，尤其是 `employee_id` 要能被班级-辅导员映射引用。若学校已有成熟 HR API 或统一身份平台，可在后续升级为 API 同步。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:71:### 3. 班级-辅导员对应关系是否应为 P0？
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:77:- 学生提交时能否自动设置辅导员审批人；
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:78:- 辅导员是否只能查看和审批负责班级；
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:80:- 审批统计能否按院系、班级、辅导员追踪。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:102:2. **组织架构数据。** 院系、专业、年级不仅用于展示，也用于权限过滤、统计导出、异常排查。首版可随学生和辅导员数据导入，不必单独做组织架构接口。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:104:3. **账号生命周期。** 需要定义新增、更新、停用、毕业归档、辅导员离职/调岗、管理员离岗后的处理规则。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:110:6. **多辅导员和代理审批。** 现实中可能有主辅导员、代管辅导员、临时代理。首版可只要求一个主审批人，但后台应预留人工改派能力。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:130:3. **定义辅导员基本信息导入模板。** 先确保 counselor 账号存在，且 `employee_id` 可被映射数据引用。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:132:4. **实现班级-辅导员映射导入。** 这是最关键步骤。上线前必须校验当届学生 100% 能解析到有效辅导员，否则不应开放提交。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:151:2. 新增“辅导员基本信息导入”章节，明确 `employee_id`、联系方式和账号状态。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:152:3. 新增“班级-辅导员对应关系导入”章节，列为 P0，并写明覆盖率和异常报告要求。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:154:5. 在附录中增加三份模板：学生基础数据、辅导员基础数据、班级-辅导员映射。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:162:- **P0 数据：** 学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据、毕业资格字段。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:165:- **最高优先级行动：** 立即补充班级-辅导员映射的数据规范和导入校验，这是自动审批闭环的关键缺口。
docs/数据对接说明文档.md:16:2. **辅导员基本信息** - 创建辅导员账号，用于审批管理
docs/数据对接说明文档.md:17:3. **班级-辅导员对应关系** - 自动分配审批人
docs/数据对接说明文档.md:27:| 辅导员基本信息 | **CSV/Excel文件导入** | 首版推荐，快速上线 |
docs/数据对接说明文档.md:28:| 班级-辅导员对应关系 | **CSV/Excel文件导入** | 首版推荐，需强校验 |
docs/数据对接说明文档.md:34:- 变更频率低：学生和辅导员信息每学期更新1-2次
docs/数据对接说明文档.md:55:- 自动分配审批人（根据班级匹配辅导员）
docs/数据对接说明文档.md:63:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
docs/数据对接说明文档.md:79:- `class_id` 必须全校唯一，用于映射辅导员，不能重复、变更或跨届复用
docs/数据对接说明文档.md:93:2022001,张三,计算机学院,计算机科学与技术,CS2022-01,计算机科学与技术2022级1班,2022,2026,true,13800138000,zhangsan@example.com
docs/数据对接说明文档.md:94:2022002,李四,计算机学院,软件工程,SE2022-01,软件工程2022级1班,2022,2026,true,13800138001,lisi@example.com
docs/数据对接说明文档.md:108:- 确保 `class_id` 字段填写正确（后续用于匹配辅导员）
docs/数据对接说明文档.md:151:## 三、辅导员基本信息（CSV导入）
docs/数据对接说明文档.md:155:- 创建辅导员账号（用于登录系统）
docs/数据对接说明文档.md:157:- 班级-辅导员映射
docs/数据对接说明文档.md:163:| 工号 | employee_id | 文本 | 是 | 辅导员唯一标识 | T2022001 |
docs/数据对接说明文档.md:164:| 姓名 | name | 文本 | 是 | 辅导员姓名 | 王老师 |
docs/数据对接说明文档.md:165:| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
docs/数据对接说明文档.md:176:**文件名：** `辅导员基本信息导入模板.csv`
docs/数据对接说明文档.md:181:T2022001,王老师,计算机学院,13900139000,wanglaoshi@example.com,true
docs/数据对接说明文档.md:182:T2022002,李老师,软件学院,13900139001,lililaoshi@example.com,true
docs/数据对接说明文档.md:191:## 四、班级-辅导员对应关系（CSV导入）
docs/数据对接说明文档.md:195:学生提交申请时，系统根据学生的 `class_id` 自动查询对应的辅导员，分配审批人。
docs/数据对接说明文档.md:203:| 辅导员工号 | counselor_employee_id | 文本 | 是 | 辅导员工号 | T2022001 |
docs/数据对接说明文档.md:207:- `counselor_employee_id` 必须在辅导员表中存在
docs/数据对接说明文档.md:208:- 首版只支持一班一主辅导员，同一 `class_id` 不能出现多次
docs/数据对接说明文档.md:212:**文件名：** `班级辅导员对应关系导入模板.csv`
docs/数据对接说明文档.md:224:1. 先导入辅导员基本信息
docs/数据对接说明文档.md:225:2. 再导入班级-辅导员对应关系
docs/数据对接说明文档.md:229:- 班级映射需要验证辅导员工号是否存在
docs/数据对接说明文档.md:230:- 学生导入需要验证班级ID是否有对应的辅导员
docs/数据对接说明文档.md:236:- 辅导员工号存在性（必须在辅导员表中）
docs/数据对接说明文档.md:237:- 班级映射覆盖率（所有学生的class_id都有对应辅导员）
docs/数据对接说明文档.md:241:- 未匹配辅导员：映射表中的工号在辅导员表中不存在
docs/数据对接说明文档.md:243:- 无审批人的学生数：有多少学生没有对应的辅导员
docs/数据对接说明文档.md:379:- 导入类型（学生/辅导员/班级映射）
docs/数据对接说明文档.md:413:A：需要先导入班级-辅导员对应关系，再导入学生信息。
docs/数据对接说明文档.md:443:**Q10：辅导员调岗后如何处理？**
docs/数据对接说明文档.md:445:A：更新班级-辅导员对应关系，重新导入CSV文件。已提交的申请不受影响，新提交的申请使用新辅导员。
docs/Excel数据源实际分析结果.md:12:### 文件1：1-5830名毕业生（含研究生）.xls
docs/Excel数据源实际分析结果.md:17:校区, 楼栋名称, 寝室号, 学生姓名, 性别, 专业, 学院名称, 班级, 层次, 年级
docs/Excel数据源实际分析结果.md:22:北区, 荷园2栋, 206, 孙芮, 女, 电子信息工程（专升本）, 物理与电信学院, 电信(专升本)202403, 专升本, 2024
docs/Excel数据源实际分析结果.md:31:| department (院系) | 学院名称 | ✅ 满足 | 如：物理与电信学院 |
docs/Excel数据源实际分析结果.md:37:### 文件2：2026届预计毕业生5675人.xlsx
docs/Excel数据源实际分析结果.md:49:- YXMC = 院校名称（值：黄冈师范学院）
docs/Excel数据源实际分析结果.md:57:YXMC: 黄冈师范学院
docs/Excel数据源实际分析结果.md:68:| department (院系) | ❌ 缺失 | **P0缺陷** | YXMC仅为校名，无学院信息 |
docs/Excel数据源实际分析结果.md:73:### 文件3：2026年社区辅导员信息统计表.xls
docs/Excel数据源实际分析结果.md:77:Row 1 (header): 序号, 楼栋号, 职工号, 姓名, 电话
docs/Excel数据源实际分析结果.md:91:### 文件4：2026年学院辅导员信息统计表.xls
docs/Excel数据源实际分析结果.md:95:Row 1 (header): 序号, 学院, 职工号, 毕业班辅导员, 电话
docs/Excel数据源实际分析结果.md:96:Row 2 (sample): 1, 马克思主义学院, 20250015, 胡晓炀, 17386282440
docs/Excel数据源实际分析结果.md:103:| name (姓名) | 毕业班辅导员 | ✅ 满足 | |
docs/Excel数据源实际分析结果.md:104:| department (院系) | 学院 | ✅ 满足 | |
docs/Excel数据源实际分析结果.md:111:| class_id (负责班级) | ❌ 完全缺失 | **P0缺陷** | 无法建立辅导员-班级映射 |
docs/Excel数据源实际分析结果.md:120:- 文件1有：学院名称、班级 ✓
docs/Excel数据源实际分析结果.md:130:- 无法生成完整的学生表（同时包含学号+学院+班级）
docs/Excel数据源实际分析结果.md:132:  - 选文件1 → 有学院，但无学号（无法唯一标识）
docs/Excel数据源实际分析结果.md:133:  - 选文件2 → 有学号，但无学院（审批路由失效）
docs/Excel数据源实际分析结果.md:137:### 缺陷2：辅导员文件缺少负责班级清单
docs/Excel数据源实际分析结果.md:142:学院, 职工号, 姓名, 电话
docs/Excel数据源实际分析结果.md:143:马克思主义学院, 20250015, 胡晓炀, 17386282440
docs/Excel数据源实际分析结果.md:147:- 该辅导员负责哪些班级？
docs/Excel数据源实际分析结果.md:148:- 班级与辅导员的对应关系？
docs/Excel数据源实际分析结果.md:152:- 无法实现"辅导员只能审批自己负责班级的申请"
docs/Excel数据源实际分析结果.md:157:### 缺陷3：部分宿管员无工号
docs/Excel数据源实际分析结果.md:163:- 这些宿管员无法导入系统（user_id必填）
docs/Excel数据源实际分析结果.md:174:| 字段完整性 | 40% | 缺学号或缺学院（二选一缺陷）|
docs/Excel数据源实际分析结果.md:176:| 数据量 | 100% | 5675-5830人符合预期 |
docs/Excel数据源实际分析结果.md:179:### 3.2 辅导员表（User - role=counselor）
docs/Excel数据源实际分析结果.md:187:### 3.3 宿管员表（User - role=dorm_manager）
docs/Excel数据源实际分析结果.md:195:### 3.4 班级-辅导员映射表（ClassMapping）
docs/Excel数据源实际分析结果.md:211:# 生成完整学生表：学号 + 姓名 + 学院 + 班级
docs/Excel数据源实际分析结果.md:215:- 逐行核对文件1和文件2的匹配关系（约5675条）
docs/Excel数据源实际分析结果.md:219:**步骤2：补充辅导员-班级映射**
docs/Excel数据源实际分析结果.md:221:# 从学院获取每个辅导员负责的班级清单
docs/Excel数据源实际分析结果.md:228:- 联系各学院确认辅导员负责班级
docs/Excel数据源实际分析结果.md:231:**步骤3：补充宿管员工号**
docs/Excel数据源实际分析结果.md:246:- 劣势：无学院信息
docs/Excel数据源实际分析结果.md:249:1. 从班号推导学院（如"环境202201" → 环境学院）
docs/Excel数据源实际分析结果.md:250:2. 建立专业→学院映射表
docs/Excel数据源实际分析结果.md:267:- 学院名称（新增）
docs/Excel数据源实际分析结果.md:272:**辅导员文件必需列：**
docs/Excel数据源实际分析结果.md:275:- 学院
docs/Excel数据源实际分析结果.md:278:**宿管员文件必需列：**
docs/Excel数据源实际分析结果.md:334:| 学生表 | ❌ 60% | 学号与学院分离 | 方案C > 方案A |
docs/Excel数据源实际分析结果.md:335:| 辅导员表 | ✅ 100% | 无 | 可直接使用 |
docs/Excel数据源实际分析结果.md:336:| 宿管员表 | ⚠️ 75% | 部分工号缺失 | 补充工号 |
docs/Excel数据源实际分析结果.md:345:2. 辅导员-班级映射完全缺失
docs/Excel数据源分析与需求对比.md:13:| 文件1 | 1-5830名毕业生（含研究生）.xls | 1002.5K | 学生基准文件 |
docs/Excel数据源分析与需求对比.md:14:| 文件2 | 2026届预计毕业生5675人.xlsx | 900.7K | 学生补充文件（含学号） |
docs/Excel数据源分析与需求对比.md:15:| 文件3 | 2026年社区辅导员信息统计表.xls | 30.0K | 宿管员信息 |
docs/Excel数据源分析与需求对比.md:16:| 文件4 | 2026年学院辅导员信息统计表.xls | 23.5K | 辅导员信息 |
docs/Excel数据源分析与需求对比.md:31:| department | 院系 | string | ✓ | 所属学院 | 文件1或文件2 |
docs/Excel数据源分析与需求对比.md:40:### 2.2 辅导员表（User - role=counselor）
docs/Excel数据源分析与需求对比.md:45:| name | 姓名 | string | ✓ | 辅导员姓名 | 文件4 |
docs/Excel数据源分析与需求对比.md:46:| department | 院系 | string | ✓ | 所属学院 | 文件4 |
docs/Excel数据源分析与需求对比.md:52:- ✅ 是否包含所属学院信息？
docs/Excel数据源分析与需求对比.md:54:### 2.3 宿管员表（User - role=dorm_manager）
docs/Excel数据源分析与需求对比.md:59:| name | 姓名 | string | ✓ | 宿管员姓名 | 文件3 |
docs/Excel数据源分析与需求对比.md:66:### 2.4 班级-辅导员映射表（ClassMapping）
docs/Excel数据源分析与需求对比.md:72:| **counselor_id** | **辅导员工号** | string | ✓ | **外键** | **文件4** |
docs/Excel数据源分析与需求对比.md:75:- ✅ 文件4是否包含**辅导员负责的班级清单**？
docs/Excel数据源分析与需求对比.md:76:- ✅ 或能否从学生表和辅导员表推导映射关系？
docs/Excel数据源分析与需求对比.md:90:- [ ] 院系/学院（department / 院系 / 学院）
docs/Excel数据源分析与需求对比.md:103:### 3.2 辅导员文件检查（文件4）
docs/Excel数据源分析与需求对比.md:108:- [ ] 所属学院（department / 学院 / 院系）
docs/Excel数据源分析与需求对比.md:116:### 3.3 宿管员文件检查（文件3）
docs/Excel数据源分析与需求对比.md:131:3. ✅ 文件4包含辅导员工号、姓名、院系、负责班级
docs/Excel数据源分析与需求对比.md:132:4. ✅ 辅导员负责班级与学生班级ID匹配
docs/Excel数据源分析与需求对比.md:133:5. ✅ 文件3包含宿管员工号、姓名
docs/Excel数据源分析与需求对比.md:134:6. ✅ 学生总数接近5675-5830人
docs/Excel数据源分析与需求对比.md:143:- 需要：创建class_id规则（如"学院缩写+年级+班号"）
docs/Excel数据源分析与需求对比.md:144:- 示例：计算机学院2022级1班 → CS2022-01
docs/Excel数据源分析与需求对比.md:146:**缺辅导员-班级映射：**
docs/Excel数据源分析与需求对比.md:148:- 格式：每个班级对应一个辅导员工号
docs/Excel数据源分析与需求对比.md:160:3. ❌ 辅导员文件无法与学生班级建立映射
docs/Excel数据源分析与需求对比.md:174:# 示例：计算机学院2022级1班 → CS2022-01
docs/Excel数据源分析与需求对比.md:195:1. `students.csv` - 学生数据（5675-5830行）
docs/Excel数据源分析与需求对比.md:196:2. `counselors.csv` - 辅导员数据
docs/Excel数据源分析与需求对比.md:197:3. `dorm_managers.csv` - 宿管员数据
docs/Excel数据源分析与需求对比.md:203:2022001,张三,student,计算机学院,CS2022-01,true,2026,13800138000,
docs/Excel数据源分析与需求对比.md:204:2022002,李四,student,计算机学院,CS2022-01,true,2026,13800138001,
docs/Excel数据源分析与需求对比.md:227:   - 文件4是否包含辅导员负责的班级清单？

exec
/bin/bash -lc 'rtk nl -ba backend/apps/applications/views.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import status
     2	from rest_framework.decorators import api_view, permission_classes
     3	from rest_framework.permissions import IsAuthenticated
     4	from rest_framework.response import Response
     5	from django.utils import timezone
     6	from drf_spectacular.utils import extend_schema, OpenApiParameter
     7	from drf_spectacular.types import OpenApiTypes
     8	from .models import Application, ApplicationStatus, DormCheckoutStatus
     9	from .serializers import ApplicationSerializer, ApplicationCreateSerializer, ApplicationListSerializer, ApplicationListResponseSerializer
    10	from .pagination import ApplicationLimitOffsetPagination
    11	from .providers import MockDormCheckoutProvider
    12	from .permissions import can_view_application
    13	from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
    14	from apps.users.models import UserRole
    15	from apps.users.class_mapping import ClassMapping
    16	from apps.notifications.services import notify_application_submitted
    17	from schema import ErrorResponseSerializer
    18	import uuid
    19	
    20	
    21	@extend_schema(
    22	    methods=['GET'],
    23	    operation_id='applications_list',
    24	    summary='获取申请列表',
    25	    description='获取当前用户的申请列表（学生/辅导员/学工部）',
    26	    parameters=[
    27	        OpenApiParameter('status', OpenApiTypes.STR, description='状态过滤'),
    28	        OpenApiParameter('limit', OpenApiTypes.INT, description='每页数量（默认20）'),
    29	        OpenApiParameter('offset', OpenApiTypes.INT, description='偏移量（默认0）'),
    30	    ],
    31	    responses={
    32	        200: ApplicationListResponseSerializer,
    33	        403: ErrorResponseSerializer,
    34	    },
    35	    tags=['申请']
    36	)
    37	@extend_schema(
    38	    methods=['POST'],
    39	    operation_id='applications_create',
    40	    summary='提交离校申请',
    41	    description='学生提交新的离校申请',
    42	    request=ApplicationCreateSerializer,
    43	    responses={
    44	        201: ApplicationSerializer,
    45	        400: ErrorResponseSerializer,
    46	        403: ErrorResponseSerializer,
    47	        404: ErrorResponseSerializer,
    48	        409: ErrorResponseSerializer,
    49	        422: ErrorResponseSerializer,
    50	    },
    51	    tags=['申请']
    52	)
    53	@api_view(['GET', 'POST'])
    54	@permission_classes([IsAuthenticated])
    55	def applications_view(request):
    56	    if request.method == 'GET':
    57	        return list_applications(request)
    58	    else:
    59	        return create_application(request)
    60	
    61	
    62	def list_applications(request):
    63	    user = request.user
    64	
    65	    # Student: own applications only
    66	    if user.role == UserRole.STUDENT:
    67	        queryset = Application.objects.filter(student=user)
    68	
    69	    # Dorm Manager: applications with own pending dorm manager approvals
    70	    elif user.role == UserRole.DORM_MANAGER:
    71	        pending_approvals = Approval.objects.filter(
    72	            approver=user,
    73	            step=ApprovalStep.DORM_MANAGER,
    74	            decision=ApprovalDecision.PENDING
    75	        ).values_list('application', flat=True)
    76	        queryset = Application.objects.filter(pk__in=pending_approvals)
    77	
    78	    # Counselor: applications with own pending counselor approvals
    79	    elif user.role == UserRole.COUNSELOR:
    80	        pending_approvals = Approval.objects.filter(
    81	            approver=user,
    82	            step=ApprovalStep.COUNSELOR,
    83	            decision=ApprovalDecision.PENDING
    84	        ).values_list('application', flat=True)
    85	        queryset = Application.objects.filter(pk__in=pending_approvals)
    86	
    87	    # Dean: view all approved applications (archiving role)
    88	    elif user.role == UserRole.DEAN:
    89	        queryset = Application.objects.filter(status=ApplicationStatus.APPROVED)
    90	
    91	    else:
    92	        return Response(
    93	            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
    94	            status=status.HTTP_403_FORBIDDEN
    95	        )
    96	
    97	    # Status filtering
    98	    status_param = request.query_params.get('status')
    99	    if status_param:
   100	        queryset = queryset.filter(status=status_param)
   101	
   102	    # Sort by created_at DESC
   103	    queryset = queryset.order_by('-created_at', '-application_id')
   104	
   105	    # Paginate
   106	    paginator = ApplicationLimitOffsetPagination()
   107	    page = paginator.paginate_queryset(queryset, request)
   108	
   109	    # Serialize
   110	    serializer = ApplicationListSerializer(page, many=True)
   111	
   112	    return paginator.get_paginated_response(serializer.data)
   113	
   114	
   115	def create_application(request):
   116	    user = request.user
   117	
   118	    if user.role != UserRole.STUDENT:
   119	        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以提交申请'}},
   120	                        status=status.HTTP_403_FORBIDDEN)
   121	
   122	    # Check for existing pending/approved applications
   123	    existing = Application.objects.filter(
   124	        student=user,
   125	        status__in=[ApplicationStatus.PENDING_DORM_MANAGER, ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.APPROVED]
   126	    ).first()
   127	    if existing:
   128	        return Response({'error': {'code': 'CONFLICT', 'message': '已有待审批或已通过的申请，不能重复提交',
   129	                                    'details': {'student_id': user.user_id, 'existing_application_id': existing.application_id, 'status': existing.status}}},
   130	                        status=status.HTTP_409_CONFLICT)
   131	
   132	    serializer = ApplicationCreateSerializer(data=request.data)
   133	    if not serializer.is_valid():
   134	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
   135	                                    'details': serializer.errors}},
   136	                        status=status.HTTP_400_BAD_REQUEST)
   137	
   138	    provider = MockDormCheckoutProvider()
   139	    dorm_status = provider.check_status(user.user_id)
   140	
   141	    if dorm_status.status != DormCheckoutStatus.COMPLETED:
   142	        return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
   143	                                    'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
   144	                                                'blocking_reason': dorm_status.blocking_reason}}},
   145	                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
   146	
   147	    try:
   148	        class_mapping = ClassMapping.objects.get(class_id=user.class_id, active=True)
   149	    except ClassMapping.DoesNotExist:
   150	        return Response({'error': {'code': 'NOT_FOUND', 'message': '班级映射不存在',
   151	                                    'details': {'class_id': user.class_id}}},
   152	                        status=status.HTTP_404_NOT_FOUND)
   153	
   154	    if class_mapping.dorm_manager is None:
   155	        return Response({'error': {'code': 'NOT_FOUND', 'message': '班级宿管员映射不存在',
   156	                                    'details': {'class_id': user.class_id}}},
   157	                        status=status.HTTP_404_NOT_FOUND)
   158	
   159	    dorm_manager_name = class_mapping.dorm_manager_name or class_mapping.dorm_manager.name
   160	
   161	    application = Application.objects.create(
   162	        application_id=f'app_{uuid.uuid4().hex[:8]}',
   163	        student=user,
   164	        student_name=user.name,
   165	        class_id=user.class_id,
   166	        reason=serializer.validated_data['reason'],
   167	        leave_date=serializer.validated_data['leave_date'],
   168	        status=ApplicationStatus.PENDING_DORM_MANAGER,
   169	        dorm_checkout_status=dorm_status.status
   170	    )
   171	
   172	    dorm_manager_approval = Approval.objects.create(
   173	        approval_id=f'apv_{uuid.uuid4().hex[:8]}',
   174	        application=application,
   175	        step=ApprovalStep.DORM_MANAGER,
   176	        approver=class_mapping.dorm_manager,
   177	        approver_name=dorm_manager_name,
   178	        decision=ApprovalDecision.PENDING
   179	    )
   180	
   181	    notify_application_submitted(application, dorm_manager_approval)
   182	
   183	    return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
   184	
   185	
   186	@extend_schema(
   187	    operation_id='applications_get',
   188	    summary='获取申请详情',
   189	    description='获取指定申请的详细信息（包括审批记录）',
   190	    responses={
   191	        200: ApplicationSerializer,
   192	        403: ErrorResponseSerializer,
   193	        404: ErrorResponseSerializer,
   194	    },
   195	    tags=['申请']
   196	)
   197	@api_view(['GET'])
   198	@permission_classes([IsAuthenticated])
   199	def get_application(request, application_id):
   200	    try:
   201	        application = Application.objects.get(application_id=application_id)
   202	    except Application.DoesNotExist:
   203	        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在',
   204	                                    'details': {'application_id': application_id}}},
   205	                        status=status.HTTP_404_NOT_FOUND)
   206	
   207	    user = request.user
   208	
   209	    # Check permission using shared helper
   210	    if not can_view_application(user, application):
   211	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
   212	                        status=status.HTTP_403_FORBIDDEN)
   213	
   214	    return Response(ApplicationSerializer(application).data)

exec
/bin/bash -lc 'rtk nl -ba backend/apps/applications/permissions.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from apps.users.models import UserRole
     2	from apps.users.class_mapping import ClassMapping
     3	from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
     4	
     5	
     6	def can_view_application(user, application):
     7	    """Check if user can view application and its attachments."""
     8	    if user.role == UserRole.STUDENT:
     9	        return application.student_id == user.user_id
    10	
    11	    if user.role == UserRole.DORM_MANAGER:
    12	        return ClassMapping.objects.filter(
    13	            dorm_manager=user,
    14	            class_id=application.class_id,
    15	            active=True
    16	        ).exists()
    17	
    18	    if user.role == UserRole.COUNSELOR:
    19	        return ClassMapping.objects.filter(
    20	            counselor=user,
    21	            class_id=application.class_id,
    22	            active=True
    23	        ).exists()
    24	
    25	    if user.role == UserRole.DEAN:
    26	        # Dean archives completed applications and does not participate in approval.
    27	        return application.status == 'approved'
    28	
    29	    return False

exec
/bin/bash -lc 'rtk nl -ba frontend/types/api.ts' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	// API Types based on v0.2 Contract
     2	// Generated: 2026-05-31
     3	
     4	export type UserRole = 'student' | 'counselor' | 'dean';
     5	
     6	export type ApplicationStatus =
     7	  | 'draft'
     8	  | 'pending_counselor'
     9	  | 'pending_dean'
    10	  | 'approved'
    11	  | 'rejected';
    12	
    13	export type ApprovalDecision = 'pending' | 'approved' | 'rejected';
    14	
    15	export type ApprovalStep = 'counselor' | 'dean';
    16	
    17	// Auth
    18	export interface LoginRequest {
    19	  user_id: string;
    20	  password: string;
    21	}
    22	
    23	export interface User {
    24	  user_id: string;
    25	  name: string;
    26	  role: UserRole;
    27	  class_id?: string | null;
    28	}
    29	
    30	export interface LoginResponse {
    31	  access_token: string;
    32	  token_type: 'Bearer';
    33	  user: User;
    34	}
    35	
    36	// Applications
    37	export interface ApplicationCreateRequest {
    38	  reason: string;
    39	  leave_date: string; // YYYY-MM-DD
    40	}
    41	
    42	export interface Application {
    43	  application_id: string;
    44	  student_id: string;
    45	  student_name: string;
    46	  class_id: string;
    47	  reason: string;
    48	  leave_date: string;
    49	  status: ApplicationStatus;
    50	  created_at: string;
    51	  updated_at: string;
    52	}
    53	
    54	export interface ApplicationDetail extends Application {
    55	  dorm_checkout_status: string;
    56	  approvals: ApprovalDetail[];
    57	}
    58	
    59	// Approvals
    60	export interface ApprovalDetail {
    61	  approval_id: string;
    62	  application_id: string;
    63	  step: ApprovalStep;
    64	  approver_id: string;
    65	  approver_name: string;
    66	  decision: ApprovalDecision;
    67	  comment: string | null;
    68	  decided_at: string | null;
    69	}
    70	
    71	export interface ApprovalListItem {
    72	  approval_id: string;
    73	  application_id: string;
    74	  step: ApprovalStep;
    75	  approver_id: string;
    76	  approver_name: string;
    77	  decision: ApprovalDecision;
    78	  created_at: string;
    79	}
    80	
    81	export interface ApprovalActionRequest {
    82	  comment?: string;
    83	}
    84	
    85	export interface ApprovalActionResponse {
    86	  approval_id: string;
    87	  decision: ApprovalDecision;
    88	  comment: string | null;
    89	  decided_at: string;
    90	}
    91	
    92	// Pagination
    93	export interface PaginatedResponse<T> {
    94	  count: number;
    95	  results: T[];
    96	}
    97	
    98	// Errors
    99	export interface ApiError {
   100	  error: {
   101	    code: string;
   102	    message: string;
   103	    details?: any;
   104	  };
   105	}

exec
/bin/bash -lc 'rtk nl -ba backend/apps/approvals/views.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import status
     2	from rest_framework.decorators import api_view, permission_classes
     3	from rest_framework.permissions import IsAuthenticated
     4	from rest_framework.response import Response
     5	from django.utils import timezone
     6	from django.db import transaction
     7	from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
     8	from drf_spectacular.types import OpenApiTypes as Types
     9	from .models import Approval, ApprovalDecision, ApprovalStep
    10	from .serializers import ApprovalSerializer, ApprovalActionSerializer, ApprovalListSerializer, ApprovalListResponseSerializer
    11	from .pagination import ApprovalLimitOffsetPagination
    12	from .validators import approval_step_matches_application_status
    13	from apps.applications.models import Application, ApplicationStatus
    14	from apps.users.models import UserRole
    15	from apps.notifications.services import notify_approval_decided
    16	from schema import ErrorResponseSerializer
    17	import uuid
    18	
    19	
    20	@extend_schema(
    21	    operation_id='approvals_list',
    22	    summary='获取审批列表',
    23	    description='获取当前用户的待审批列表（辅导员或学工部）',
    24	    parameters=[
    25	        OpenApiParameter('decision', Types.STR, description='决策过滤：pending/approved/rejected/all（默认pending）'),
    26	        OpenApiParameter('limit', Types.INT, description='每页数量（默认20）'),
    27	        OpenApiParameter('offset', Types.INT, description='偏移量（默认0）'),
    28	    ],
    29	    responses={
    30	        200: ApprovalListResponseSerializer,
    31	        403: ErrorResponseSerializer,
    32	    },
    33	    tags=['审批']
    34	)
    35	@api_view(['GET'])
    36	@permission_classes([IsAuthenticated])
    37	def list_approvals(request):
    38	    user = request.user
    39	
    40	    # 学生禁止访问
    41	    if user.role == UserRole.STUDENT:
    42	        return Response(
    43	            {'error': {'code': 'FORBIDDEN', 'message': '学生不能访问审批列表'}},
    44	            status=status.HTTP_403_FORBIDDEN
    45	        )
    46	
    47	    # 宿管员: 只看自己的dorm_manager审批
    48	    if user.role == UserRole.DORM_MANAGER:
    49	        queryset = Approval.objects.filter(
    50	            approver=user,
    51	            step=ApprovalStep.DORM_MANAGER
    52	        ).select_related('application', 'approver')
    53	
    54	    # 辅导员: 只看自己的counselor审批
    55	    elif user.role == UserRole.COUNSELOR:
    56	        queryset = Approval.objects.filter(
    57	            approver=user,
    58	            step=ApprovalStep.COUNSELOR
    59	        ).select_related('application', 'approver')
    60	
    61	    # 学工部: 查看所有审批（存档用）
    62	    elif user.role == UserRole.DEAN:
    63	        queryset = Approval.objects.all().select_related('application', 'approver')
    64	
    65	    else:
    66	        return Response(
    67	            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
    68	            status=status.HTTP_403_FORBIDDEN
    69	        )
    70	
    71	    # Decision filtering (default: pending)
    72	    decision_param = request.query_params.get('decision', 'pending')
    73	    if decision_param != 'all':
    74	        queryset = queryset.filter(decision=decision_param)
    75	
    76	    # 排序
    77	    queryset = queryset.order_by('-created_at', '-approval_id')
    78	
    79	    # 分页
    80	    paginator = ApprovalLimitOffsetPagination()
    81	    page = paginator.paginate_queryset(queryset, request)
    82	
    83	    # 序列化
    84	    serializer = ApprovalListSerializer(page, many=True)
    85	
    86	    return paginator.get_paginated_response(serializer.data)
    87	
    88	
    89	@extend_schema(
    90	    operation_id='approvals_approve',
    91	    summary='通过审批',
    92	    description='审批人通过指定的审批申请',
    93	    request=ApprovalActionSerializer,
    94	    responses={
    95	        200: ApprovalSerializer,
    96	        400: ErrorResponseSerializer,
    97	        403: ErrorResponseSerializer,
    98	        404: ErrorResponseSerializer,
    99	        409: ErrorResponseSerializer,
   100	    },
   101	    tags=['审批']
   102	)
   103	@api_view(['POST'])
   104	@permission_classes([IsAuthenticated])
   105	@transaction.atomic
   106	def approve_approval(request, approval_id):
   107	    try:
   108	        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
   109	    except Approval.DoesNotExist:
   110	        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
   111	                        status=status.HTTP_404_NOT_FOUND)
   112	
   113	    user = request.user
   114	    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
   115	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   116	                        status=status.HTTP_403_FORBIDDEN)
   117	    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
   118	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   119	                        status=status.HTTP_403_FORBIDDEN)
   120	    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
   121	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   122	                        status=status.HTTP_403_FORBIDDEN)
   123	
   124	    if approval.approver_id != user.user_id:
   125	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   126	                        status=status.HTTP_403_FORBIDDEN)
   127	
   128	    if approval.decision != ApprovalDecision.PENDING:
   129	        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
   130	                        status=status.HTTP_409_CONFLICT)
   131	
   132	    if not approval_step_matches_application_status(approval):
   133	        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
   134	                        status=status.HTTP_409_CONFLICT)
   135	
   136	    serializer = ApprovalActionSerializer(data=request.data)
   137	    if not serializer.is_valid():
   138	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败'}},
   139	                        status=status.HTTP_400_BAD_REQUEST)
   140	
   141	    approval.decision = ApprovalDecision.APPROVED
   142	    approval.comment = serializer.validated_data.get('comment', '')
   143	    approval.decided_at = timezone.now()
   144	    approval.save()
   145	
   146	    notify_approval_decided(approval)
   147	
   148	    application = approval.application
   149	    if approval.step == ApprovalStep.DORM_MANAGER:
   150	        # Check for existing counselor approval to prevent duplicates
   151	        existing_counselor_approval = Approval.objects.filter(
   152	            application=application,
   153	            step=ApprovalStep.COUNSELOR
   154	        ).exists()
   155	
   156	        if existing_counselor_approval:
   157	            return Response({'error': {'code': 'CONFLICT', 'message': '辅导员审批已存在，不能重复创建'}},
   158	                            status=status.HTTP_409_CONFLICT)
   159	
   160	        application.status = ApplicationStatus.PENDING_COUNSELOR
   161	        application.save()
   162	
   163	        # Get counselor from class mapping
   164	        from apps.users.class_mapping import ClassMapping
   165	        class_mapping = ClassMapping.objects.get(class_id=application.class_id, active=True)
   166	
   167	        Approval.objects.create(
   168	            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
   169	            application=application,
   170	            step=ApprovalStep.COUNSELOR,
   171	            approver=class_mapping.counselor,
   172	            approver_name=class_mapping.counselor_name,
   173	            decision=ApprovalDecision.PENDING
   174	        )
   175	    elif approval.step == ApprovalStep.COUNSELOR:
   176	        # Check for existing dean approval to prevent duplicates
   177	        existing_dean_approval = Approval.objects.filter(
   178	            application=application,
   179	            step=ApprovalStep.DEAN
   180	        ).exists()
   181	
   182	        if existing_dean_approval:
   183	            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
   184	                            status=status.HTTP_409_CONFLICT)
   185	
   186	        application.status = ApplicationStatus.PENDING_DEAN
   187	        application.save()
   188	
   189	        # Get first available dean user
   190	        from apps.users.models import User
   191	        dean_user = User.objects.filter(role=UserRole.DEAN, active=True).first()
   192	
   193	        if not dean_user:
   194	            return Response({'error': {'code': 'NOT_FOUND', 'message': '学工部审批人不存在'}},
   195	                            status=status.HTTP_404_NOT_FOUND)
   196	
   197	        Approval.objects.create(
   198	            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
   199	            application=application,
   200	            step=ApprovalStep.DEAN,
   201	            approver=dean_user,
   202	            approver_name=dean_user.name,
   203	            decision=ApprovalDecision.PENDING
   204	        )
   205	    elif approval.step == ApprovalStep.DEAN:
   206	        application.status = ApplicationStatus.APPROVED
   207	        application.save()
   208	
   209	    return Response(ApprovalSerializer(approval).data)
   210	
   211	
   212	@extend_schema(
   213	    operation_id='approvals_reject',
   214	    summary='驳回审批',
   215	    description='审批人驳回指定的审批申请',
   216	    request=ApprovalActionSerializer,
   217	    responses={
   218	        200: ApprovalSerializer,
   219	        400: ErrorResponseSerializer,
   220	        403: ErrorResponseSerializer,
   221	        404: ErrorResponseSerializer,
   222	        409: ErrorResponseSerializer,
   223	    },
   224	    tags=['审批']
   225	)
   226	@api_view(['POST'])
   227	@permission_classes([IsAuthenticated])
   228	@transaction.atomic
   229	def reject_approval(request, approval_id):
   230	    try:
   231	        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
   232	    except Approval.DoesNotExist:
   233	        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
   234	                        status=status.HTTP_404_NOT_FOUND)
   235	
   236	    user = request.user
   237	    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
   238	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   239	                        status=status.HTTP_403_FORBIDDEN)
   240	    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
   241	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   242	                        status=status.HTTP_403_FORBIDDEN)
   243	    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
   244	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   245	                        status=status.HTTP_403_FORBIDDEN)
   246	
   247	    if approval.approver_id != user.user_id:
   248	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   249	                        status=status.HTTP_403_FORBIDDEN)
   250	
   251	    if approval.decision != ApprovalDecision.PENDING:
   252	        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
   253	                        status=status.HTTP_409_CONFLICT)
   254	
   255	    if not approval_step_matches_application_status(approval):
   256	        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
   257	                        status=status.HTTP_409_CONFLICT)
   258	
   259	    serializer = ApprovalActionSerializer(data=request.data)
   260	    if not serializer.is_valid():
   261	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败'}},
   262	                        status=status.HTTP_400_BAD_REQUEST)
   263	
   264	    approval.decision = ApprovalDecision.REJECTED
   265	    approval.comment = serializer.validated_data.get('comment', '')
   266	    approval.decided_at = timezone.now()
   267	    approval.save()
   268	
   269	    notify_approval_decided(approval)
   270	
   271	    application = approval.application
   272	    application.status = ApplicationStatus.REJECTED
   273	    application.save()
   274	
   275	    return Response(ApprovalSerializer(approval).data)

exec
/bin/bash -lc 'rtk nl -ba backend/apps/applications/models.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.db import models
     2	from django.core.exceptions import ValidationError
     3	from apps.users.models import User
     4	
     5	
     6	class ApplicationStatus(models.TextChoices):
     7	    DRAFT = 'draft', '草稿'
     8	    PENDING_DORM_MANAGER = 'pending_dorm_manager', '待宿管员审批'
     9	    PENDING_COUNSELOR = 'pending_counselor', '待辅导员审批'
    10	    PENDING_DEAN = 'pending_dean', '待学工部审批'
    11	    APPROVED = 'approved', '已通过'
    12	    REJECTED = 'rejected', '已驳回'
    13	
    14	
    15	class DormCheckoutStatus(models.TextChoices):
    16	    COMPLETED = 'completed', '已清退'
    17	    PENDING = 'pending', '清退中'
    18	    NOT_STARTED = 'not_started', '未开始'
    19	    UNKNOWN = 'unknown', '状态未知'
    20	
    21	
    22	class Application(models.Model):
    23	    application_id = models.CharField(max_length=50, primary_key=True)
    24	    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='applications')
    25	    student_name = models.CharField(max_length=100)
    26	    class_id = models.CharField(max_length=50)
    27	    reason = models.TextField()
    28	    leave_date = models.DateField()
    29	    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.DRAFT)
    30	    dorm_checkout_status = models.CharField(max_length=20, choices=DormCheckoutStatus.choices, default=DormCheckoutStatus.NOT_STARTED)
    31	    created_at = models.DateTimeField(auto_now_add=True)
    32	    updated_at = models.DateTimeField(auto_now=True)
    33	
    34	    class Meta:
    35	        db_table = 'applications'
    36	
    37	    def clean(self):
    38	        active_statuses = [
    39	            ApplicationStatus.PENDING_DORM_MANAGER,
    40	            ApplicationStatus.PENDING_COUNSELOR,
    41	            ApplicationStatus.PENDING_DEAN,
    42	            ApplicationStatus.APPROVED,
    43	        ]
    44	        if self.status in active_statuses:
    45	            existing = Application.objects.filter(
    46	                student=self.student,
    47	                status__in=active_statuses
    48	            ).exclude(application_id=self.application_id).exists()
    49	            if existing:
    50	                raise ValidationError('该学生已有待审批或已通过的申请，不能重复提交')

exec
/bin/bash -lc 'rtk nl -ba backend/apps/users/models.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
     2	from django.db import models
     3	
     4	
     5	class UserRole(models.TextChoices):
     6	    STUDENT = 'student', '学生'
     7	    DORM_MANAGER = 'dorm_manager', '宿管员'
     8	    COUNSELOR = 'counselor', '辅导员'
     9	    DEAN = 'dean', '学工部'
    10	
    11	
    12	class UserManager(BaseUserManager):
    13	    def create_user(self, user_id, password=None, **extra_fields):
    14	        if not user_id:
    15	            raise ValueError('user_id is required')
    16	        user = self.model(user_id=user_id, **extra_fields)
    17	        user.set_password(password)
    18	        user.save(using=self._db)
    19	        return user
    20	
    21	    def create_superuser(self, user_id, password=None, **extra_fields):
    22	        extra_fields.setdefault('is_staff', True)
    23	        extra_fields.setdefault('is_superuser', True)
    24	        extra_fields.setdefault('active', True)
    25	        return self.create_user(user_id, password, **extra_fields)
    26	
    27	
    28	class User(AbstractBaseUser, PermissionsMixin):
    29	    user_id = models.CharField(max_length=50, unique=True, primary_key=True)
    30	    name = models.CharField(max_length=100)
    31	    role = models.CharField(max_length=20, choices=UserRole.choices)
    32	    active = models.BooleanField(default=True)
    33	    class_id = models.CharField(max_length=50, null=True, blank=True)
    34	    is_graduating = models.BooleanField(null=True, blank=True)
    35	    graduation_year = models.IntegerField(null=True, blank=True)
    36	
    37	    # API补充字段（学工系统）
    38	    phone = models.CharField(max_length=20, null=True, blank=True)
    39	    email = models.EmailField(null=True, blank=True)
    40	    department = models.CharField(max_length=100, null=True, blank=True)
    41	
    42	    is_staff = models.BooleanField(default=False)
    43	    created_at = models.DateTimeField(auto_now_add=True)
    44	    updated_at = models.DateTimeField(auto_now=True)
    45	
    46	    objects = UserManager()
    47	
    48	    USERNAME_FIELD = 'user_id'
    49	    REQUIRED_FIELDS = ['name', 'role']
    50	
    51	    class Meta:
    52	        db_table = 'users'
    53	
    54	    def __str__(self):
    55	        return f"{self.user_id} - {self.name}"

codex
我已形成主要结论：方案方向可以落地，但不能按“所有 P0 已解除、2.5-3 天可完成”直接进入实施。关键阻塞是空学号导入、楼栋多宿管员与当前单审批人模型冲突、以及 `ClassMapping/dean/class_id` 在现有代码中是横跨后端、前端和测试的契约。接下来我会把审查结果写成协作 artifact，并完成任务日志。
apply patch
patch: completed
/home/caohui/projects/graduation-leave-system/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md
diff --git a/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md b/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md
new file mode 100644
index 0000000000000000000000000000000000000000..55cb8e2beb37fa6a4a2b80a2807dfe11504911ba
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md
@@ -0,0 +1,129 @@
+# Codex Implementation Plan Review
+
+**Task ID:** TASK-20260605-03
+**Review target:** `docs/用户需求最终确认与实施方案.md`
+**Reviewer:** Codex
+**Date:** 2026-06-05
+
+## 审查结论
+
+当前方案的业务方向基本正确：用 File1 作为学生基准、改为“楼栋宿管员 -> 学院辅导员”的 2 级审批、把学工管理员定位为只读角色，整体符合用户最新决策。
+
+但文档不能按“所有 P0 已解除，可开始实施”执行。至少 3 个阻塞点仍未闭合：空学号/空 `user_id` 无法导入、楼栋多宿管员与当前单审批人模型冲突、`ClassMapping`/`dean`/`class_id` 的代码契约改造范围被明显低估。
+
+评分：
+
+| 维度 | 分数 |
+|---|---:|
+| 业务逻辑完整性 | 7/10 |
+| 技术可行性 | 5/10 |
+| 数据一致性 | 6/10 |
+| 实施风险控制 | 4/10 |
+| **总分** | **22/40** |
+
+结论：需要修改后再实施。
+
+## P0 问题清单
+
+1. 空学号学生无法导入，与“全部 5830 行可导入”矛盾
+   - 位置：`docs/用户需求最终确认与实施方案.md:33-42`, `docs/用户需求最终确认与实施方案.md:171-175`
+   - 证据：现有 `User.user_id` 是主键且唯一；`UserManager.create_user()` 明确要求 `user_id` 非空。见 `backend/apps/users/models.py:12-17`, `backend/apps/users/models.py:28-31`。
+   - 影响范围：File2 未匹配学生、研究生、登录账号、审批记录外键、通知和导入脚本。
+   - 建议修正：实施前必须定义缺学号学生的稳定主键策略。推荐使用可追溯的临时账号，如 `TMP2026_{file1_row_no}` 或 `GRAD2026_{hash(name+college+building+room)}`，并在 File5 中增加 `source_row_id`、`user_id_source`、`student_no` 三类字段，避免把“登录账号主键”和“真实学号”混为一个字段。
+
+2. “任一宿管员可审批”与当前审批模型不兼容
+   - 位置：`docs/用户需求最终确认与实施方案.md:126-130`, `docs/用户需求最终确认与实施方案.md:248-255`, `docs/用户需求最终确认与实施方案.md:450-461`
+   - 证据：当前 `Approval.approver` 是单个用户外键；创建申请时只创建一个宿管审批记录。见 `backend/apps/approvals/models.py:14-22`, `backend/apps/applications/views.py:172-179`。方案中的 `return dorm_managers` 没有定义如何落到审批记录、权限过滤、重复审批和通知。
+   - 影响范围：提交申请、审批列表、详情权限、并发审批、通知、审计。
+   - 建议修正：MVP 不要实现“任一人可审批”的组任务，除非增加 group approval 模型。更现实的 P0 修正是要求 File3 或映射表生成一个 `primary_dorm_manager_user_id`，每栋楼唯一主责宿管员；其他宿管员作为后续代理/备份扩展。
+
+3. `ClassMapping` 移除工作量被低估，当前方案遗漏提交和流转入口
+   - 位置：`docs/用户需求最终确认与实施方案.md:321-324`
+   - 证据：现有提交申请直接查 `ClassMapping` 并用它创建宿管审批，见 `backend/apps/applications/views.py:147-179`；宿管审批通过后仍用 `ClassMapping` 创建辅导员审批，见 `backend/apps/approvals/views.py:149-174`；详情权限也按 `ClassMapping` 判断，见 `backend/apps/applications/permissions.py:11-23`。
+   - 影响范围：后端接口、权限、数据库迁移、导入命令、前端类型、测试套件和文档契约。
+   - 建议修正：把 Phase 2 拆成明确的改造清单：数据模型、提交路由、审批通过路由、列表过滤、详情权限、附件权限、导入命令、API schema、前端/miniprogram 类型、测试 fixture。未完成前不能导入真实数据并开放提交。
+
+## P1 问题清单
+
+1. 数据差异口径不一致
+   - 位置：`docs/用户需求最终确认与实施方案.md:33-40`
+   - 问题：文档同时写“File2 没有的 155 行”和“271 研究生 + 116 File2 独有”。这两个口径不能同时成立。按 5830 和 5675 的净差是 155，但若存在 271 个 File1 独有和 116 个 File2 独有，交集应为 5559。
+   - 建议修正：File5 生成报告必须输出 `file1_only_count`、`file2_only_count`、`matched_count`、`ambiguous_match_count`、`duplicate_key_count`，并把 File2 独有 116 行明确列为“不导入但归档报告”或“追加导入”。
+
+2. 状态机名称与现有代码不一致，迁移边界不清
+   - 位置：`docs/用户需求最终确认与实施方案.md:218-234`, `docs/用户需求最终确认与实施方案.md:316-319`
+   - 证据：现有状态是 `pending_dorm_manager / pending_counselor / pending_dean / approved / rejected`，不是文档里的 `PENDING / DORM_MANAGER_APPROVED / COUNSELOR_APPROVED / COMPLETED`。见 `backend/apps/applications/models.py:6-12`。
+   - 建议修正：最终状态应继续使用 API 现有风格，例如 `pending_dorm_manager -> pending_counselor -> approved`。删除或迁移 `pending_dean`，并补充历史数据迁移规则。
+
+3. 学工管理员与既有 `dean` 角色关系未定义
+   - 位置：`docs/用户需求最终确认与实施方案.md:98-115`, `docs/用户需求最终确认与实施方案.md:326-329`
+   - 证据：后端已有 `UserRole.DEAN`，前端类型也只有 `student | counselor | dean`，见 `backend/apps/users/models.py:5-9`, `frontend/types/api.ts:4-15`。
+   - 建议修正：明确是复用并重命名 `dean` 为只读管理员，还是新增 `admin` 并迁移/废弃 `dean`。推荐短期复用 `dean` 的只读语义，文案改为“学工管理员(dean/admin display name)”，代码层是否改枚举放到单独 migration。
+
+4. 路由键没有做申请时快照，后续人员/学院/楼栋变更会破坏审计
+   - 位置：`docs/用户需求最终确认与实施方案.md:85-96`, `docs/用户需求最终确认与实施方案.md:178-182`
+   - 问题：如果只从 `User.department/building_name` 动态读取，学生学院或宿管映射更新后，历史申请的可见范围和审批追溯会变化。
+   - 建议修正：`Application` 增加申请时快照字段：`student_building_name`、`student_room_number`、`student_department`、可选 `route_version`。`Approval` 已保存审批人和姓名，可保留。
+
+5. 学院/楼栋规范化缺少完整字典和阻断标准
+   - 位置：`docs/用户需求最终确认与实施方案.md:285-293`, `docs/用户需求最终确认与实施方案.md:357-361`, `docs/用户需求最终确认与实施方案.md:438-448`
+   - 问题：只给示例，没有说明 19 个学院、33 个楼栋的完整映射来源、冲突处理和失败阈值。
+   - 建议修正：将 `college_normalization_map.json` 和 `building_normalization_map.json` 列为 Phase 1 必交付；导入门禁应是 100% 路由覆盖，任何未匹配、重复唯一键、空路由键都阻断。
+
+6. 数据导入 Phase 缺少对现有导入命令的替换范围
+   - 位置：`docs/用户需求最终确认与实施方案.md:336-355`
+   - 证据：现有 `import_csv` 仍要求学生 `class_id`，并校验 `ClassMapping` 存在。见 `backend/apps/users/management/commands/import_csv.py`。
+   - 建议修正：新增或重写导入命令，不要在文档里直接使用不存在的 `import_students/import_counselors/import_dorm_managers` 命令名，除非 Phase 2 明确包含这些命令实现。
+
+7. 2.5-3 天估算偏乐观
+   - 位置：`docs/用户需求最终确认与实施方案.md:314-388`
+   - 问题：现有后端、前端、miniprogram、测试和 API 契约都依赖原 3 级/班级模型。1-1.5 天系统调整加 0.5 天前端不足以覆盖迁移、测试修复和回归。
+   - 建议修正：按 4-6 天估算更现实；或切分为“后端闭环 MVP”和“前端/管理员视图完善”两个里程碑。
+
+8. 缺少回滚策略
+   - 位置：`docs/用户需求最终确认与实施方案.md:436-472`
+   - 问题：风险章节只有缓解，没有数据库迁移失败、导入失败、上线后路由错误的回滚路径。
+   - 建议修正：补充上线前备份、迁移可逆性、导入 dry-run、导入批次号、删除/回滚本批数据脚本、功能开关或维护窗口方案。
+
+## P2 建议清单
+
+1. 前端调整不要只写“4 类用户界面”，应明确小程序、frontend、demo-web 是否都要同步。
+2. 测试用例应增加负向权限：宿管员不能看其他楼栋、辅导员不能看其他学院、管理员不能审批、学生不能访问审批列表。
+3. 寝室号未来升级建议优先建独立映射表，不建议把 `room_numbers` JSONField 作为长期方案；独立表更容易做唯一约束和导入差异报告。
+4. 通知文案需要随审批步骤更新，避免继续提示“学工部审批”。
+5. API 文档和 TypeScript 类型应列入交付物，否则前后端状态枚举会漂移。
+
+## 修正建议
+
+1. 先把文档状态从“所有 P0 阻塞已解除”改为“业务方向确认，实施前仍需关闭 P0 技术/数据门禁”。
+2. 增加 Phase 0：数据画像和路由门禁。
+   - 输出 File1/File2 匹配报告。
+   - 输出完整学院/楼栋规范化字典。
+   - 输出缺学号学生账号生成策略。
+   - 输出每名学生的宿管和辅导员路由结果。
+3. 把楼栋多宿管员规则收敛为一个 MVP 决策。
+   - 推荐：每栋楼唯一主责宿管员。
+   - 后续再做多人队列或代理审批。
+4. 重新设计数据模型变更。
+   - `User` 增加学生楼栋、寝室、专业、年级字段。
+   - `Application.class_id` 改可空或废弃展示依赖，并新增申请时路由快照字段。
+   - 明确 `dean` 到 `admin` 的迁移或复用策略。
+5. 重排实施顺序。
+   - Phase 0 数据门禁。
+   - Phase 1 后端模型和路由，带单元测试。
+   - Phase 2 导入命令 dry-run 和真实导入。
+   - Phase 3 前端/小程序/API 类型同步。
+   - Phase 4 端到端和权限回归。
+   - Phase 5 备份、上线、回滚演练。
+
+## 最低通过条件
+
+实施前至少满足以下条件：
+
+1. 5830 行学生均有非空稳定 `user_id`。
+2. 每个学生都能唯一确定一个宿管审批主体，或系统模型已支持多人待办。
+3. 每个学生都能唯一确定一个学院辅导员。
+4. `ClassMapping` 依赖清单已全部替换或兼容。
+5. `pending_dean/dean` 的迁移策略明确。
+6. 导入脚本支持 dry-run，并输出 100% 路由覆盖报告。
+7. 有数据库备份和导入批次回滚方案。

diff --git a/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md b/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md
new file mode 100644
index 0000000000000000000000000000000000000000..55cb8e2beb37fa6a4a2b80a2807dfe11504911ba
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md
@@ -0,0 +1,129 @@
+# Codex Implementation Plan Review
+
+**Task ID:** TASK-20260605-03
+**Review target:** `docs/用户需求最终确认与实施方案.md`
+**Reviewer:** Codex
+**Date:** 2026-06-05
+
+## 审查结论
+
+当前方案的业务方向基本正确：用 File1 作为学生基准、改为“楼栋宿管员 -> 学院辅导员”的 2 级审批、把学工管理员定位为只读角色，整体符合用户最新决策。
+
+但文档不能按“所有 P0 已解除，可开始实施”执行。至少 3 个阻塞点仍未闭合：空学号/空 `user_id` 无法导入、楼栋多宿管员与当前单审批人模型冲突、`ClassMapping`/`dean`/`class_id` 的代码契约改造范围被明显低估。
+
+评分：
+
+| 维度 | 分数 |
+|---|---:|
+| 业务逻辑完整性 | 7/10 |
+| 技术可行性 | 5/10 |
+| 数据一致性 | 6/10 |
+| 实施风险控制 | 4/10 |
+| **总分** | **22/40** |
+
+结论：需要修改后再实施。
+
+## P0 问题清单
+
+1. 空学号学生无法导入，与“全部 5830 行可导入”矛盾
+   - 位置：`docs/用户需求最终确认与实施方案.md:33-42`, `docs/用户需求最终确认与实施方案.md:171-175`
+   - 证据：现有 `User.user_id` 是主键且唯一；`UserManager.create_user()` 明确要求 `user_id` 非空。见 `backend/apps/users/models.py:12-17`, `backend/apps/users/models.py:28-31`。
+   - 影响范围：File2 未匹配学生、研究生、登录账号、审批记录外键、通知和导入脚本。
+   - 建议修正：实施前必须定义缺学号学生的稳定主键策略。推荐使用可追溯的临时账号，如 `TMP2026_{file1_row_no}` 或 `GRAD2026_{hash(name+college+building+room)}`，并在 File5 中增加 `source_row_id`、`user_id_source`、`student_no` 三类字段，避免把“登录账号主键”和“真实学号”混为一个字段。
+
+2. “任一宿管员可审批”与当前审批模型不兼容
+   - 位置：`docs/用户需求最终确认与实施方案.md:126-130`, `docs/用户需求最终确认与实施方案.md:248-255`, `docs/用户需求最终确认与实施方案.md:450-461`
+   - 证据：当前 `Approval.approver` 是单个用户外键；创建申请时只创建一个宿管审批记录。见 `backend/apps/approvals/models.py:14-22`, `backend/apps/applications/views.py:172-179`。方案中的 `return dorm_managers` 没有定义如何落到审批记录、权限过滤、重复审批和通知。
+   - 影响范围：提交申请、审批列表、详情权限、并发审批、通知、审计。
+   - 建议修正：MVP 不要实现“任一人可审批”的组任务，除非增加 group approval 模型。更现实的 P0 修正是要求 File3 或映射表生成一个 `primary_dorm_manager_user_id`，每栋楼唯一主责宿管员；其他宿管员作为后续代理/备份扩展。
+
+3. `ClassMapping` 移除工作量被低估，当前方案遗漏提交和流转入口
+   - 位置：`docs/用户需求最终确认与实施方案.md:321-324`
+   - 证据：现有提交申请直接查 `ClassMapping` 并用它创建宿管审批，见 `backend/apps/applications/views.py:147-179`；宿管审批通过后仍用 `ClassMapping` 创建辅导员审批，见 `backend/apps/approvals/views.py:149-174`；详情权限也按 `ClassMapping` 判断，见 `backend/apps/applications/permissions.py:11-23`。
+   - 影响范围：后端接口、权限、数据库迁移、导入命令、前端类型、测试套件和文档契约。
+   - 建议修正：把 Phase 2 拆成明确的改造清单：数据模型、提交路由、审批通过路由、列表过滤、详情权限、附件权限、导入命令、API schema、前端/miniprogram 类型、测试 fixture。未完成前不能导入真实数据并开放提交。
+
+## P1 问题清单
+
+1. 数据差异口径不一致
+   - 位置：`docs/用户需求最终确认与实施方案.md:33-40`
+   - 问题：文档同时写“File2 没有的 155 行”和“271 研究生 + 116 File2 独有”。这两个口径不能同时成立。按 5830 和 5675 的净差是 155，但若存在 271 个 File1 独有和 116 个 File2 独有，交集应为 5559。
+   - 建议修正：File5 生成报告必须输出 `file1_only_count`、`file2_only_count`、`matched_count`、`ambiguous_match_count`、`duplicate_key_count`，并把 File2 独有 116 行明确列为“不导入但归档报告”或“追加导入”。
+
+2. 状态机名称与现有代码不一致，迁移边界不清
+   - 位置：`docs/用户需求最终确认与实施方案.md:218-234`, `docs/用户需求最终确认与实施方案.md:316-319`
+   - 证据：现有状态是 `pending_dorm_manager / pending_counselor / pending_dean / approved / rejected`，不是文档里的 `PENDING / DORM_MANAGER_APPROVED / COUNSELOR_APPROVED / COMPLETED`。见 `backend/apps/applications/models.py:6-12`。
+   - 建议修正：最终状态应继续使用 API 现有风格，例如 `pending_dorm_manager -> pending_counselor -> approved`。删除或迁移 `pending_dean`，并补充历史数据迁移规则。
+
+3. 学工管理员与既有 `dean` 角色关系未定义
+   - 位置：`docs/用户需求最终确认与实施方案.md:98-115`, `docs/用户需求最终确认与实施方案.md:326-329`
+   - 证据：后端已有 `UserRole.DEAN`，前端类型也只有 `student | counselor | dean`，见 `backend/apps/users/models.py:5-9`, `frontend/types/api.ts:4-15`。
+   - 建议修正：明确是复用并重命名 `dean` 为只读管理员，还是新增 `admin` 并迁移/废弃 `dean`。推荐短期复用 `dean` 的只读语义，文案改为“学工管理员(dean/admin display name)”，代码层是否改枚举放到单独 migration。
+
+4. 路由键没有做申请时快照，后续人员/学院/楼栋变更会破坏审计
+   - 位置：`docs/用户需求最终确认与实施方案.md:85-96`, `docs/用户需求最终确认与实施方案.md:178-182`
+   - 问题：如果只从 `User.department/building_name` 动态读取，学生学院或宿管映射更新后，历史申请的可见范围和审批追溯会变化。
+   - 建议修正：`Application` 增加申请时快照字段：`student_building_name`、`student_room_number`、`student_department`、可选 `route_version`。`Approval` 已保存审批人和姓名，可保留。
+
+5. 学院/楼栋规范化缺少完整字典和阻断标准
+   - 位置：`docs/用户需求最终确认与实施方案.md:285-293`, `docs/用户需求最终确认与实施方案.md:357-361`, `docs/用户需求最终确认与实施方案.md:438-448`
+   - 问题：只给示例，没有说明 19 个学院、33 个楼栋的完整映射来源、冲突处理和失败阈值。
+   - 建议修正：将 `college_normalization_map.json` 和 `building_normalization_map.json` 列为 Phase 1 必交付；导入门禁应是 100% 路由覆盖，任何未匹配、重复唯一键、空路由键都阻断。
+
+6. 数据导入 Phase 缺少对现有导入命令的替换范围
+   - 位置：`docs/用户需求最终确认与实施方案.md:336-355`
+   - 证据：现有 `import_csv` 仍要求学生 `class_id`，并校验 `ClassMapping` 存在。见 `backend/apps/users/management/commands/import_csv.py`。
+   - 建议修正：新增或重写导入命令，不要在文档里直接使用不存在的 `import_students/import_counselors/import_dorm_managers` 命令名，除非 Phase 2 明确包含这些命令实现。
+
+7. 2.5-3 天估算偏乐观
+   - 位置：`docs/用户需求最终确认与实施方案.md:314-388`
+   - 问题：现有后端、前端、miniprogram、测试和 API 契约都依赖原 3 级/班级模型。1-1.5 天系统调整加 0.5 天前端不足以覆盖迁移、测试修复和回归。
+   - 建议修正：按 4-6 天估算更现实；或切分为“后端闭环 MVP”和“前端/管理员视图完善”两个里程碑。
+
+8. 缺少回滚策略
+   - 位置：`docs/用户需求最终确认与实施方案.md:436-472`
+   - 问题：风险章节只有缓解，没有数据库迁移失败、导入失败、上线后路由错误的回滚路径。
+   - 建议修正：补充上线前备份、迁移可逆性、导入 dry-run、导入批次号、删除/回滚本批数据脚本、功能开关或维护窗口方案。
+
+## P2 建议清单
+
+1. 前端调整不要只写“4 类用户界面”，应明确小程序、frontend、demo-web 是否都要同步。
+2. 测试用例应增加负向权限：宿管员不能看其他楼栋、辅导员不能看其他学院、管理员不能审批、学生不能访问审批列表。
+3. 寝室号未来升级建议优先建独立映射表，不建议把 `room_numbers` JSONField 作为长期方案；独立表更容易做唯一约束和导入差异报告。
+4. 通知文案需要随审批步骤更新，避免继续提示“学工部审批”。
+5. API 文档和 TypeScript 类型应列入交付物，否则前后端状态枚举会漂移。
+
+## 修正建议
+
+1. 先把文档状态从“所有 P0 阻塞已解除”改为“业务方向确认，实施前仍需关闭 P0 技术/数据门禁”。
+2. 增加 Phase 0：数据画像和路由门禁。
+   - 输出 File1/File2 匹配报告。
+   - 输出完整学院/楼栋规范化字典。
+   - 输出缺学号学生账号生成策略。
+   - 输出每名学生的宿管和辅导员路由结果。
+3. 把楼栋多宿管员规则收敛为一个 MVP 决策。
+   - 推荐：每栋楼唯一主责宿管员。
+   - 后续再做多人队列或代理审批。
+4. 重新设计数据模型变更。
+   - `User` 增加学生楼栋、寝室、专业、年级字段。
+   - `Application.class_id` 改可空或废弃展示依赖，并新增申请时路由快照字段。
+   - 明确 `dean` 到 `admin` 的迁移或复用策略。
+5. 重排实施顺序。
+   - Phase 0 数据门禁。
+   - Phase 1 后端模型和路由，带单元测试。
+   - Phase 2 导入命令 dry-run 和真实导入。
+   - Phase 3 前端/小程序/API 类型同步。
+   - Phase 4 端到端和权限回归。
+   - Phase 5 备份、上线、回滚演练。
+
+## 最低通过条件
+
+实施前至少满足以下条件：
+
+1. 5830 行学生均有非空稳定 `user_id`。
+2. 每个学生都能唯一确定一个宿管审批主体，或系统模型已支持多人待办。
+3. 每个学生都能唯一确定一个学院辅导员。
+4. `ClassMapping` 依赖清单已全部替换或兼容。
+5. `pending_dean/dean` 的迁移策略明确。
+6. 导入脚本支持 dry-run，并输出 100% 路由覆盖报告。
+7. 有数据库备份和导入批次回滚方案。

codex
审查 artifact 已写入协作目录。最后我会按协议记录 `artifact_created` 和 `completed` 事件，把共享状态置为完成。
exec
/bin/bash -lc "rtk node -e \"const fs=require('fs'); const path='.omc/collaboration'; const lock=path+'/locks/journal.lock'; const task='TASK-20260605-03'; const artifact='.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md'; const now=new Date().toISOString(); fs.mkdirSync(lock); try { fs.writeFileSync(lock+'/owner.json', JSON.stringify({agent:'codex',task_id:task,created_at:now,heartbeat_at:now,reason:'record review artifact and complete task'}, null, 2)); const eventsPath=path+'/events.jsonl'; const raw=fs.existsSync(eventsPath)?fs.readFileSync(eventsPath,'utf8').trim():''; const events=raw?raw.split(/\\n/).map((line,i)=>{try{return JSON.parse(line)}catch(e){throw new Error('Malformed events.jsonl line '+(i+1)+': '+e.message)}}):[]; const ids=new Set(); for (const e of events) { if (ids.has(e.id)) throw new Error('Duplicate event id '+e.id); ids.add(e.id); } let nextId=events.reduce((m,e)=>Math.max(m, Number(e.id)||0),0)+1; const ev1={id:nextId++,type:'artifact_created',agent:'codex',timestamp:now,task_id:task,summary:'Codex implementation plan review artifact created',artifacts:[artifact],status:'in_progress'}; const ev2={id:nextId++,type:'completed',agent:'codex',timestamp:now,task_id:task,summary:'Codex completed implementation plan review',artifacts:[artifact],status:'completed'}; fs.appendFileSync(eventsPath, JSON.stringify(ev1)+'\\n'+JSON.stringify(ev2)+'\\n'); const state={workflow_id:'implementation-plan-review',current_task:task,active_agent:'none',status:'completed',last_event_id:ev2.id,updated_at:now}; const tmp=path+'/state.json.tmp.codex'; fs.writeFileSync(tmp, JSON.stringify(state,null,2)+'\\n'); JSON.parse(fs.readFileSync(tmp,'utf8')); fs.renameSync(tmp,path+'/state.json'); const checkEvents=fs.readFileSync(eventsPath,'utf8').trim().split(/\\n/).map(JSON.parse); const maxId=checkEvents.reduce((m,e)=>Math.max(m, Number(e.id)||0),0); const st=JSON.parse(fs.readFileSync(path+'/state.json','utf8')); if (st.last_event_id"'!==maxId) throw new Error('"'state last_event_id mismatch'); } finally { try { fs.rmSync(lock,{recursive:true,force:true}); } catch(e) {} }\"" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
diff --git a/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md b/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md
new file mode 100644
index 0000000000000000000000000000000000000000..55cb8e2beb37fa6a4a2b80a2807dfe11504911ba
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md
@@ -0,0 +1,129 @@
+# Codex Implementation Plan Review
+
+**Task ID:** TASK-20260605-03
+**Review target:** `docs/用户需求最终确认与实施方案.md`
+**Reviewer:** Codex
+**Date:** 2026-06-05
+
+## 审查结论
+
+当前方案的业务方向基本正确：用 File1 作为学生基准、改为“楼栋宿管员 -> 学院辅导员”的 2 级审批、把学工管理员定位为只读角色，整体符合用户最新决策。
+
+但文档不能按“所有 P0 已解除，可开始实施”执行。至少 3 个阻塞点仍未闭合：空学号/空 `user_id` 无法导入、楼栋多宿管员与当前单审批人模型冲突、`ClassMapping`/`dean`/`class_id` 的代码契约改造范围被明显低估。
+
+评分：
+
+| 维度 | 分数 |
+|---|---:|
+| 业务逻辑完整性 | 7/10 |
+| 技术可行性 | 5/10 |
+| 数据一致性 | 6/10 |
+| 实施风险控制 | 4/10 |
+| **总分** | **22/40** |
+
+结论：需要修改后再实施。
+
+## P0 问题清单
+
+1. 空学号学生无法导入，与“全部 5830 行可导入”矛盾
+   - 位置：`docs/用户需求最终确认与实施方案.md:33-42`, `docs/用户需求最终确认与实施方案.md:171-175`
+   - 证据：现有 `User.user_id` 是主键且唯一；`UserManager.create_user()` 明确要求 `user_id` 非空。见 `backend/apps/users/models.py:12-17`, `backend/apps/users/models.py:28-31`。
+   - 影响范围：File2 未匹配学生、研究生、登录账号、审批记录外键、通知和导入脚本。
+   - 建议修正：实施前必须定义缺学号学生的稳定主键策略。推荐使用可追溯的临时账号，如 `TMP2026_{file1_row_no}` 或 `GRAD2026_{hash(name+college+building+room)}`，并在 File5 中增加 `source_row_id`、`user_id_source`、`student_no` 三类字段，避免把“登录账号主键”和“真实学号”混为一个字段。
+
+2. “任一宿管员可审批”与当前审批模型不兼容
+   - 位置：`docs/用户需求最终确认与实施方案.md:126-130`, `docs/用户需求最终确认与实施方案.md:248-255`, `docs/用户需求最终确认与实施方案.md:450-461`
+   - 证据：当前 `Approval.approver` 是单个用户外键；创建申请时只创建一个宿管审批记录。见 `backend/apps/approvals/models.py:14-22`, `backend/apps/applications/views.py:172-179`。方案中的 `return dorm_managers` 没有定义如何落到审批记录、权限过滤、重复审批和通知。
+   - 影响范围：提交申请、审批列表、详情权限、并发审批、通知、审计。
+   - 建议修正：MVP 不要实现“任一人可审批”的组任务，除非增加 group approval 模型。更现实的 P0 修正是要求 File3 或映射表生成一个 `primary_dorm_manager_user_id`，每栋楼唯一主责宿管员；其他宿管员作为后续代理/备份扩展。
+
+3. `ClassMapping` 移除工作量被低估，当前方案遗漏提交和流转入口
+   - 位置：`docs/用户需求最终确认与实施方案.md:321-324`
+   - 证据：现有提交申请直接查 `ClassMapping` 并用它创建宿管审批，见 `backend/apps/applications/views.py:147-179`；宿管审批通过后仍用 `ClassMapping` 创建辅导员审批，见 `backend/apps/approvals/views.py:149-174`；详情权限也按 `ClassMapping` 判断，见 `backend/apps/applications/permissions.py:11-23`。
+   - 影响范围：后端接口、权限、数据库迁移、导入命令、前端类型、测试套件和文档契约。
+   - 建议修正：把 Phase 2 拆成明确的改造清单：数据模型、提交路由、审批通过路由、列表过滤、详情权限、附件权限、导入命令、API schema、前端/miniprogram 类型、测试 fixture。未完成前不能导入真实数据并开放提交。
+
+## P1 问题清单
+
+1. 数据差异口径不一致
+   - 位置：`docs/用户需求最终确认与实施方案.md:33-40`
+   - 问题：文档同时写“File2 没有的 155 行”和“271 研究生 + 116 File2 独有”。这两个口径不能同时成立。按 5830 和 5675 的净差是 155，但若存在 271 个 File1 独有和 116 个 File2 独有，交集应为 5559。
+   - 建议修正：File5 生成报告必须输出 `file1_only_count`、`file2_only_count`、`matched_count`、`ambiguous_match_count`、`duplicate_key_count`，并把 File2 独有 116 行明确列为“不导入但归档报告”或“追加导入”。
+
+2. 状态机名称与现有代码不一致，迁移边界不清
+   - 位置：`docs/用户需求最终确认与实施方案.md:218-234`, `docs/用户需求最终确认与实施方案.md:316-319`
+   - 证据：现有状态是 `pending_dorm_manager / pending_counselor / pending_dean / approved / rejected`，不是文档里的 `PENDING / DORM_MANAGER_APPROVED / COUNSELOR_APPROVED / COMPLETED`。见 `backend/apps/applications/models.py:6-12`。
+   - 建议修正：最终状态应继续使用 API 现有风格，例如 `pending_dorm_manager -> pending_counselor -> approved`。删除或迁移 `pending_dean`，并补充历史数据迁移规则。
+
+3. 学工管理员与既有 `dean` 角色关系未定义
+   - 位置：`docs/用户需求最终确认与实施方案.md:98-115`, `docs/用户需求最终确认与实施方案.md:326-329`
+   - 证据：后端已有 `UserRole.DEAN`，前端类型也只有 `student | counselor | dean`，见 `backend/apps/users/models.py:5-9`, `frontend/types/api.ts:4-15`。
+   - 建议修正：明确是复用并重命名 `dean` 为只读管理员，还是新增 `admin` 并迁移/废弃 `dean`。推荐短期复用 `dean` 的只读语义，文案改为“学工管理员(dean/admin display name)”，代码层是否改枚举放到单独 migration。
+
+4. 路由键没有做申请时快照，后续人员/学院/楼栋变更会破坏审计
+   - 位置：`docs/用户需求最终确认与实施方案.md:85-96`, `docs/用户需求最终确认与实施方案.md:178-182`
+   - 问题：如果只从 `User.department/building_name` 动态读取，学生学院或宿管映射更新后，历史申请的可见范围和审批追溯会变化。
+   - 建议修正：`Application` 增加申请时快照字段：`student_building_name`、`student_room_number`、`student_department`、可选 `route_version`。`Approval` 已保存审批人和姓名，可保留。
+
+5. 学院/楼栋规范化缺少完整字典和阻断标准
+   - 位置：`docs/用户需求最终确认与实施方案.md:285-293`, `docs/用户需求最终确认与实施方案.md:357-361`, `docs/用户需求最终确认与实施方案.md:438-448`
+   - 问题：只给示例，没有说明 19 个学院、33 个楼栋的完整映射来源、冲突处理和失败阈值。
+   - 建议修正：将 `college_normalization_map.json` 和 `building_normalization_map.json` 列为 Phase 1 必交付；导入门禁应是 100% 路由覆盖，任何未匹配、重复唯一键、空路由键都阻断。
+
+6. 数据导入 Phase 缺少对现有导入命令的替换范围
+   - 位置：`docs/用户需求最终确认与实施方案.md:336-355`
+   - 证据：现有 `import_csv` 仍要求学生 `class_id`，并校验 `ClassMapping` 存在。见 `backend/apps/users/management/commands/import_csv.py`。
+   - 建议修正：新增或重写导入命令，不要在文档里直接使用不存在的 `import_students/import_counselors/import_dorm_managers` 命令名，除非 Phase 2 明确包含这些命令实现。
+
+7. 2.5-3 天估算偏乐观
+   - 位置：`docs/用户需求最终确认与实施方案.md:314-388`
+   - 问题：现有后端、前端、miniprogram、测试和 API 契约都依赖原 3 级/班级模型。1-1.5 天系统调整加 0.5 天前端不足以覆盖迁移、测试修复和回归。
+   - 建议修正：按 4-6 天估算更现实；或切分为“后端闭环 MVP”和“前端/管理员视图完善”两个里程碑。
+
+8. 缺少回滚策略
+   - 位置：`docs/用户需求最终确认与实施方案.md:436-472`
+   - 问题：风险章节只有缓解，没有数据库迁移失败、导入失败、上线后路由错误的回滚路径。
+   - 建议修正：补充上线前备份、迁移可逆性、导入 dry-run、导入批次号、删除/回滚本批数据脚本、功能开关或维护窗口方案。
+
+## P2 建议清单
+
+1. 前端调整不要只写“4 类用户界面”，应明确小程序、frontend、demo-web 是否都要同步。
+2. 测试用例应增加负向权限：宿管员不能看其他楼栋、辅导员不能看其他学院、管理员不能审批、学生不能访问审批列表。
+3. 寝室号未来升级建议优先建独立映射表，不建议把 `room_numbers` JSONField 作为长期方案；独立表更容易做唯一约束和导入差异报告。
+4. 通知文案需要随审批步骤更新，避免继续提示“学工部审批”。
+5. API 文档和 TypeScript 类型应列入交付物，否则前后端状态枚举会漂移。
+
+## 修正建议
+
+1. 先把文档状态从“所有 P0 阻塞已解除”改为“业务方向确认，实施前仍需关闭 P0 技术/数据门禁”。
+2. 增加 Phase 0：数据画像和路由门禁。
+   - 输出 File1/File2 匹配报告。
+   - 输出完整学院/楼栋规范化字典。
+   - 输出缺学号学生账号生成策略。
+   - 输出每名学生的宿管和辅导员路由结果。
+3. 把楼栋多宿管员规则收敛为一个 MVP 决策。
+   - 推荐：每栋楼唯一主责宿管员。
+   - 后续再做多人队列或代理审批。
+4. 重新设计数据模型变更。
+   - `User` 增加学生楼栋、寝室、专业、年级字段。
+   - `Application.class_id` 改可空或废弃展示依赖，并新增申请时路由快照字段。
+   - 明确 `dean` 到 `admin` 的迁移或复用策略。
+5. 重排实施顺序。
+   - Phase 0 数据门禁。
+   - Phase 1 后端模型和路由，带单元测试。
+   - Phase 2 导入命令 dry-run 和真实导入。
+   - Phase 3 前端/小程序/API 类型同步。
+   - Phase 4 端到端和权限回归。
+   - Phase 5 备份、上线、回滚演练。
+
+## 最低通过条件
+
+实施前至少满足以下条件：
+
+1. 5830 行学生均有非空稳定 `user_id`。
+2. 每个学生都能唯一确定一个宿管审批主体，或系统模型已支持多人待办。
+3. 每个学生都能唯一确定一个学院辅导员。
+4. `ClassMapping` 依赖清单已全部替换或兼容。
+5. `pending_dean/dean` 的迁移策略明确。
+6. 导入脚本支持 dry-run，并输出 100% 路由覆盖报告。
+7. 有数据库备份和导入批次回滚方案。

exec
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
 M .omc/collaboration/events.jsonl
 M .omc/collaboration/state.json
 M .omc/state/hud-stdin-cache.json
 M backend/apps/applications/permissions.py
 M backend/apps/applications/providers.py
 M backend/apps/applications/tests/test_constraints.py
 M backend/apps/applications/tests/test_detail_permissions.py
 M backend/apps/applications/tests/test_error_cases.py
 M backend/apps/applications/tests/test_list_permissions.py
 M backend/apps/applications/views.py
 M backend/apps/approvals/tests/test_list_permissions.py
 M backend/apps/approvals/tests/test_permissions.py
 M backend/apps/approvals/tests/test_rejection_flow.py
 M backend/apps/attachments/tests/test_list.py
 M backend/apps/notifications/services.py
 M backend/apps/notifications/tests/test_auto_notifications.py
 M backend/apps/users/integrations/xg_user_client.py
 M backend/apps/users/management/commands/seed_data.py
 M backend/apps/users/models.py
 M backend/apps/users/tests/test_xg_user_client.py
 M backend/scripts/diagnose_xg_api.py
 M docs/api/notification-contract-v0.1.md
 M frontend/services/api.ts
 M frontend/services/mock.ts
 M frontend/types/api.ts
 M tests/test_p0_fixes.sh
?? .claude/scheduled_tasks.json
?? .omc/artifacts/ask/codex-omc-collaboration-tasks-task-20260605-01-excel-association-r-2026-06-05T00-55-29-654Z.md
?? .omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md
?? .omc/collaboration/tasks/TASK-20260605-03-implementation-plan-review.md
?? .omc/project-memory.json
?? .omc/sessions/
?? .omc/state/agent-replay-f5a217eb-15dd-46c8-bdf3-d9e12d88125b.jsonl
?? .omc/state/checkpoints/
?? .omc/state/last-tool-error.json
?? .omc/state/mission-state.json
?? .omc/state/sessions/1975d66f-d9f9-404a-aee5-c702658630c2/
?? .omc/state/sessions/4aad264e-c3a4-460a-9be1-61247202bad3/
?? .omc/state/sessions/7afec07d-3b40-4e4c-8f86-86e9dc0e791c/
?? .omc/state/sessions/83935a94-dc9d-4f47-83f5-bad88cc99fad/
?? .omc/state/sessions/97c93024-a4c1-4e03-93bf-7522ce3517ff/
?? .omc/state/sessions/9bdcb1fe-5a48-4133-8a75-ba525f0229cb/
?? .omc/state/sessions/c8f47bca-464c-4b8c-bab5-42ba59354101/
?? .omc/state/sessions/dcf39a3e-1b72-449a-9897-852c3c7f1253/
?? .omc/state/sessions/e2566739-aaa7-4701-9354-a710639ac308/
?? .omc/state/sessions/f5a217eb-15dd-46c8-bdf3-d9e12d88125b/
?? .omc/state/sessions/f91e1567-b1b2-4cc2-bd9b-355702bc1ec4/
?? .planning/
?? backend/.omc/
?? backend/app
?? backend/apps/notifications/management/commands/send_approval_timeout_warnings.py
?? backend/apps/notifications/tests/test_timeout_warnings.py
?? backend/apps/users/migrations/0002_user_department_user_email_user_phone.py
?? backend/config/settings/test.py
?? backend/docs/
?? backend/reports/
?? backend/scripts/normalize_colleges.py
?? "docs/1-5830\345\220\215\346\257\225\344\270\232\347\224\237\357\274\210\345\220\253\347\240\224\347\251\266\347\224\237\357\274\211.xls"
?? "docs/2026\345\261\212\351\242\204\350\256\241\346\257\225\344\270\232\347\224\2375675\344\272\272.xlsx"
?? "docs/2026\345\271\264\345\255\246\351\231\242\350\276\205\345\257\274\345\221\230\344\277\241\346\201\257\347\273\237\350\256\241\350\241\250.xls"
?? "docs/2026\345\271\264\347\244\276\345\214\272\350\276\205\345\257\274\345\221\230\344\277\241\346\201\257\347\273\237\350\256\241\350\241\250.xls"
?? "docs/Excel\346\225\260\346\215\256\346\272\220\345\210\206\346\236\220\344\270\216\351\234\200\346\261\202\345\257\271\346\257\224.md"
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
?? docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md
?? docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md
?? docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md
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
?? docs/project-completion-status-2026-06-02.md
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260528210617_553_47.jpg"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260528210618_554_47.jpg"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260528210619_555_47.jpg"
?? findings.md
?? miniprogram/.omc/
?? progress.md
?? scripts/
?? task_plan.md
?? "\346\257\225\344\270\232\347\246\273\346\240\241\347\263\273\347\273\237\347\224\250\346\210\267\346\226\207\346\241\243.zip"
exec
/bin/bash -lc 'rtk tail -n 6 .omc/collaboration/events.jsonl' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{"id":1,"type":"workflow_initialized","agent":"claude","timestamp":"2026-06-05T05:10:00.000Z","summary":"Initialize implementation-plan-review workflow","status":"initialized"}
{"id":2,"type":"task_created","agent":"claude","timestamp":"2026-06-05T05:10:10.000Z","task_id":"TASK-20260605-03","summary":"Review implementation plan document","artifacts":["tasks/TASK-20260605-03-implementation-plan-review.md"]}
{"id":3,"type":"handoff_requested","agent":"claude","timestamp":"2026-06-05T05:10:20.000Z","task_id":"TASK-20260605-03","target_agent":"codex","summary":"Request Codex review of implementation plan"}
{"id":4,"type":"task_claimed","agent":"codex","timestamp":"2026-06-05T05:11:07.039Z","task_id":"TASK-20260605-03","summary":"Codex claimed implementation plan review task","status":"in_progress"}
{"id":5,"type":"artifact_created","agent":"codex","timestamp":"2026-06-05T05:13:50.860Z","task_id":"TASK-20260605-03","summary":"Codex implementation plan review artifact created","artifacts":[".omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md"],"status":"in_progress"}
{"id":6,"type":"completed","agent":"codex","timestamp":"2026-06-05T05:13:50.860Z","task_id":"TASK-20260605-03","summary":"Codex completed implementation plan review","artifacts":[".omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md"],"status":"completed"}

exec
/bin/bash -lc "rtk sed -n '1,220p' .omc/collaboration/state.json" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{
  "workflow_id": "implementation-plan-review",
  "current_task": "TASK-20260605-03",
  "active_agent": "none",
  "status": "completed",
  "last_event_id": 6,
  "updated_at": "2026-06-05T05:13:50.860Z"
}

diff --git a/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md b/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md
new file mode 100644
index 0000000000000000000000000000000000000000..55cb8e2beb37fa6a4a2b80a2807dfe11504911ba
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md
@@ -0,0 +1,129 @@
+# Codex Implementation Plan Review
+
+**Task ID:** TASK-20260605-03
+**Review target:** `docs/用户需求最终确认与实施方案.md`
+**Reviewer:** Codex
+**Date:** 2026-06-05
+
+## 审查结论
+
+当前方案的业务方向基本正确：用 File1 作为学生基准、改为“楼栋宿管员 -> 学院辅导员”的 2 级审批、把学工管理员定位为只读角色，整体符合用户最新决策。
+
+但文档不能按“所有 P0 已解除，可开始实施”执行。至少 3 个阻塞点仍未闭合：空学号/空 `user_id` 无法导入、楼栋多宿管员与当前单审批人模型冲突、`ClassMapping`/`dean`/`class_id` 的代码契约改造范围被明显低估。
+
+评分：
+
+| 维度 | 分数 |
+|---|---:|
+| 业务逻辑完整性 | 7/10 |
+| 技术可行性 | 5/10 |
+| 数据一致性 | 6/10 |
+| 实施风险控制 | 4/10 |
+| **总分** | **22/40** |
+
+结论：需要修改后再实施。
+
+## P0 问题清单
+
+1. 空学号学生无法导入，与“全部 5830 行可导入”矛盾
+   - 位置：`docs/用户需求最终确认与实施方案.md:33-42`, `docs/用户需求最终确认与实施方案.md:171-175`
+   - 证据：现有 `User.user_id` 是主键且唯一；`UserManager.create_user()` 明确要求 `user_id` 非空。见 `backend/apps/users/models.py:12-17`, `backend/apps/users/models.py:28-31`。
+   - 影响范围：File2 未匹配学生、研究生、登录账号、审批记录外键、通知和导入脚本。
+   - 建议修正：实施前必须定义缺学号学生的稳定主键策略。推荐使用可追溯的临时账号，如 `TMP2026_{file1_row_no}` 或 `GRAD2026_{hash(name+college+building+room)}`，并在 File5 中增加 `source_row_id`、`user_id_source`、`student_no` 三类字段，避免把“登录账号主键”和“真实学号”混为一个字段。
+
+2. “任一宿管员可审批”与当前审批模型不兼容
+   - 位置：`docs/用户需求最终确认与实施方案.md:126-130`, `docs/用户需求最终确认与实施方案.md:248-255`, `docs/用户需求最终确认与实施方案.md:450-461`
+   - 证据：当前 `Approval.approver` 是单个用户外键；创建申请时只创建一个宿管审批记录。见 `backend/apps/approvals/models.py:14-22`, `backend/apps/applications/views.py:172-179`。方案中的 `return dorm_managers` 没有定义如何落到审批记录、权限过滤、重复审批和通知。
+   - 影响范围：提交申请、审批列表、详情权限、并发审批、通知、审计。
+   - 建议修正：MVP 不要实现“任一人可审批”的组任务，除非增加 group approval 模型。更现实的 P0 修正是要求 File3 或映射表生成一个 `primary_dorm_manager_user_id`，每栋楼唯一主责宿管员；其他宿管员作为后续代理/备份扩展。
+
+3. `ClassMapping` 移除工作量被低估，当前方案遗漏提交和流转入口
+   - 位置：`docs/用户需求最终确认与实施方案.md:321-324`
+   - 证据：现有提交申请直接查 `ClassMapping` 并用它创建宿管审批，见 `backend/apps/applications/views.py:147-179`；宿管审批通过后仍用 `ClassMapping` 创建辅导员审批，见 `backend/apps/approvals/views.py:149-174`；详情权限也按 `ClassMapping` 判断，见 `backend/apps/applications/permissions.py:11-23`。
+   - 影响范围：后端接口、权限、数据库迁移、导入命令、前端类型、测试套件和文档契约。
+   - 建议修正：把 Phase 2 拆成明确的改造清单：数据模型、提交路由、审批通过路由、列表过滤、详情权限、附件权限、导入命令、API schema、前端/miniprogram 类型、测试 fixture。未完成前不能导入真实数据并开放提交。
+
+## P1 问题清单
+
+1. 数据差异口径不一致
+   - 位置：`docs/用户需求最终确认与实施方案.md:33-40`
+   - 问题：文档同时写“File2 没有的 155 行”和“271 研究生 + 116 File2 独有”。这两个口径不能同时成立。按 5830 和 5675 的净差是 155，但若存在 271 个 File1 独有和 116 个 File2 独有，交集应为 5559。
+   - 建议修正：File5 生成报告必须输出 `file1_only_count`、`file2_only_count`、`matched_count`、`ambiguous_match_count`、`duplicate_key_count`，并把 File2 独有 116 行明确列为“不导入但归档报告”或“追加导入”。
+
+2. 状态机名称与现有代码不一致，迁移边界不清
+   - 位置：`docs/用户需求最终确认与实施方案.md:218-234`, `docs/用户需求最终确认与实施方案.md:316-319`
+   - 证据：现有状态是 `pending_dorm_manager / pending_counselor / pending_dean / approved / rejected`，不是文档里的 `PENDING / DORM_MANAGER_APPROVED / COUNSELOR_APPROVED / COMPLETED`。见 `backend/apps/applications/models.py:6-12`。
+   - 建议修正：最终状态应继续使用 API 现有风格，例如 `pending_dorm_manager -> pending_counselor -> approved`。删除或迁移 `pending_dean`，并补充历史数据迁移规则。
+
+3. 学工管理员与既有 `dean` 角色关系未定义
+   - 位置：`docs/用户需求最终确认与实施方案.md:98-115`, `docs/用户需求最终确认与实施方案.md:326-329`
+   - 证据：后端已有 `UserRole.DEAN`，前端类型也只有 `student | counselor | dean`，见 `backend/apps/users/models.py:5-9`, `frontend/types/api.ts:4-15`。
+   - 建议修正：明确是复用并重命名 `dean` 为只读管理员，还是新增 `admin` 并迁移/废弃 `dean`。推荐短期复用 `dean` 的只读语义，文案改为“学工管理员(dean/admin display name)”，代码层是否改枚举放到单独 migration。
+
+4. 路由键没有做申请时快照，后续人员/学院/楼栋变更会破坏审计
+   - 位置：`docs/用户需求最终确认与实施方案.md:85-96`, `docs/用户需求最终确认与实施方案.md:178-182`
+   - 问题：如果只从 `User.department/building_name` 动态读取，学生学院或宿管映射更新后，历史申请的可见范围和审批追溯会变化。
+   - 建议修正：`Application` 增加申请时快照字段：`student_building_name`、`student_room_number`、`student_department`、可选 `route_version`。`Approval` 已保存审批人和姓名，可保留。
+
+5. 学院/楼栋规范化缺少完整字典和阻断标准
+   - 位置：`docs/用户需求最终确认与实施方案.md:285-293`, `docs/用户需求最终确认与实施方案.md:357-361`, `docs/用户需求最终确认与实施方案.md:438-448`
+   - 问题：只给示例，没有说明 19 个学院、33 个楼栋的完整映射来源、冲突处理和失败阈值。
+   - 建议修正：将 `college_normalization_map.json` 和 `building_normalization_map.json` 列为 Phase 1 必交付；导入门禁应是 100% 路由覆盖，任何未匹配、重复唯一键、空路由键都阻断。
+
+6. 数据导入 Phase 缺少对现有导入命令的替换范围
+   - 位置：`docs/用户需求最终确认与实施方案.md:336-355`
+   - 证据：现有 `import_csv` 仍要求学生 `class_id`，并校验 `ClassMapping` 存在。见 `backend/apps/users/management/commands/import_csv.py`。
+   - 建议修正：新增或重写导入命令，不要在文档里直接使用不存在的 `import_students/import_counselors/import_dorm_managers` 命令名，除非 Phase 2 明确包含这些命令实现。
+
+7. 2.5-3 天估算偏乐观
+   - 位置：`docs/用户需求最终确认与实施方案.md:314-388`
+   - 问题：现有后端、前端、miniprogram、测试和 API 契约都依赖原 3 级/班级模型。1-1.5 天系统调整加 0.5 天前端不足以覆盖迁移、测试修复和回归。
+   - 建议修正：按 4-6 天估算更现实；或切分为“后端闭环 MVP”和“前端/管理员视图完善”两个里程碑。
+
+8. 缺少回滚策略
+   - 位置：`docs/用户需求最终确认与实施方案.md:436-472`
+   - 问题：风险章节只有缓解，没有数据库迁移失败、导入失败、上线后路由错误的回滚路径。
+   - 建议修正：补充上线前备份、迁移可逆性、导入 dry-run、导入批次号、删除/回滚本批数据脚本、功能开关或维护窗口方案。
+
+## P2 建议清单
+
+1. 前端调整不要只写“4 类用户界面”，应明确小程序、frontend、demo-web 是否都要同步。
+2. 测试用例应增加负向权限：宿管员不能看其他楼栋、辅导员不能看其他学院、管理员不能审批、学生不能访问审批列表。
+3. 寝室号未来升级建议优先建独立映射表，不建议把 `room_numbers` JSONField 作为长期方案；独立表更容易做唯一约束和导入差异报告。
+4. 通知文案需要随审批步骤更新，避免继续提示“学工部审批”。
+5. API 文档和 TypeScript 类型应列入交付物，否则前后端状态枚举会漂移。
+
+## 修正建议
+
+1. 先把文档状态从“所有 P0 阻塞已解除”改为“业务方向确认，实施前仍需关闭 P0 技术/数据门禁”。
+2. 增加 Phase 0：数据画像和路由门禁。
+   - 输出 File1/File2 匹配报告。
+   - 输出完整学院/楼栋规范化字典。
+   - 输出缺学号学生账号生成策略。
+   - 输出每名学生的宿管和辅导员路由结果。
+3. 把楼栋多宿管员规则收敛为一个 MVP 决策。
+   - 推荐：每栋楼唯一主责宿管员。
+   - 后续再做多人队列或代理审批。
+4. 重新设计数据模型变更。
+   - `User` 增加学生楼栋、寝室、专业、年级字段。
+   - `Application.class_id` 改可空或废弃展示依赖，并新增申请时路由快照字段。
+   - 明确 `dean` 到 `admin` 的迁移或复用策略。
+5. 重排实施顺序。
+   - Phase 0 数据门禁。
+   - Phase 1 后端模型和路由，带单元测试。
+   - Phase 2 导入命令 dry-run 和真实导入。
+   - Phase 3 前端/小程序/API 类型同步。
+   - Phase 4 端到端和权限回归。
+   - Phase 5 备份、上线、回滚演练。
+
+## 最低通过条件
+
+实施前至少满足以下条件：
+
+1. 5830 行学生均有非空稳定 `user_id`。
+2. 每个学生都能唯一确定一个宿管审批主体，或系统模型已支持多人待办。
+3. 每个学生都能唯一确定一个学院辅导员。
+4. `ClassMapping` 依赖清单已全部替换或兼容。
+5. `pending_dean/dean` 的迁移策略明确。
+6. 导入脚本支持 dry-run，并输出 100% 路由覆盖报告。
+7. 有数据库备份和导入批次回滚方案。

codex
已完成审查，并写入 artifact：[20260605-codex-implementation-plan-review.md](/home/caohui/projects/graduation-leave-system/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md)。协作任务状态已置为 `completed`。

**评分**
| 维度 | 分数 |
|---|---:|
| 业务逻辑完整性 | 7/10 |
| 技术可行性 | 5/10 |
| 数据一致性 | 6/10 |
| 实施风险控制 | 4/10 |
| **总分** | **22/40** |

**结论：需要修改后再实施。** 方案方向正确，但不能按“所有 P0 已解除、2.5-3 天完成”直接推进。

**P0 问题**
1. 空学号学生无法导入：方案允许 `user_id` 为空，但现有 `User.user_id` 是主键且创建用户要求非空。
2. “任一宿管员可审批”与当前单审批人 `Approval.approver` 模型冲突，必须先定义唯一主责人或改造为多人待办模型。
3. `ClassMapping` 移除范围被低估；提交申请、审批流转、详情权限都直接依赖它。

**P1 问题**
1. File1/File2 差异口径不一致：`155`、`271研究生`、`116 File2独有` 的关系需要重新写清。
2. 状态机名称与现有代码不一致，现有是 `pending_dorm_manager/pending_counselor/pending_dean/approved`。
3. 新 `admin` 与既有 `dean` 角色关系未定义。
4. 路由键缺少申请时快照，后续学院/楼栋/人员变更会影响历史审计。
5. 学院和楼栋规范化只有示例，没有完整字典、冲突规则和阻断标准。
6. 数据导入命令与现有 `import_csv` 不一致，现有命令仍要求 `class_id` 和 `ClassMapping`。
7. 2.5-3 天估算偏乐观。
8. 风险章节缺少备份、dry-run、导入批次回滚和迁移失败回滚方案。

**P2 建议**
1. 明确 frontend、miniprogram、demo-web 是否都要同步。
2. 增加负向权限测试：跨楼栋、跨学院、管理员不可审批、学生不可看审批列表。
3. 寝室号精确路由建议用独立映射表，不建议长期使用 JSONField。
4. 通知文案同步移除“学工部审批”。
5. API 文档和 TypeScript 类型应列入交付物。

**修正建议**
先增加 Phase 0：数据画像和路由门禁。必须输出 File1/File2 匹配报告、完整学院/楼栋规范化字典、缺学号账号生成策略、5830 人逐条宿管和辅导员路由结果。

MVP 建议把楼栋多宿管员收敛为“每栋楼唯一主责宿管员”，后续再做代理或多人队列。然后重排实施为：数据门禁 → 后端模型/路由/权限 → 导入 dry-run/真实导入 → 前端和 API 类型同步 → 端到端权限回归 → 备份与回滚演练。
diff --git a/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md b/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md
new file mode 100644
index 0000000000000000000000000000000000000000..55cb8e2beb37fa6a4a2b80a2807dfe11504911ba
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md
@@ -0,0 +1,129 @@
+# Codex Implementation Plan Review
+
+**Task ID:** TASK-20260605-03
+**Review target:** `docs/用户需求最终确认与实施方案.md`
+**Reviewer:** Codex
+**Date:** 2026-06-05
+
+## 审查结论
+
+当前方案的业务方向基本正确：用 File1 作为学生基准、改为“楼栋宿管员 -> 学院辅导员”的 2 级审批、把学工管理员定位为只读角色，整体符合用户最新决策。
+
+但文档不能按“所有 P0 已解除，可开始实施”执行。至少 3 个阻塞点仍未闭合：空学号/空 `user_id` 无法导入、楼栋多宿管员与当前单审批人模型冲突、`ClassMapping`/`dean`/`class_id` 的代码契约改造范围被明显低估。
+
+评分：
+
+| 维度 | 分数 |
+|---|---:|
+| 业务逻辑完整性 | 7/10 |
+| 技术可行性 | 5/10 |
+| 数据一致性 | 6/10 |
+| 实施风险控制 | 4/10 |
+| **总分** | **22/40** |
+
+结论：需要修改后再实施。
+
+## P0 问题清单
+
+1. 空学号学生无法导入，与“全部 5830 行可导入”矛盾
+   - 位置：`docs/用户需求最终确认与实施方案.md:33-42`, `docs/用户需求最终确认与实施方案.md:171-175`
+   - 证据：现有 `User.user_id` 是主键且唯一；`UserManager.create_user()` 明确要求 `user_id` 非空。见 `backend/apps/users/models.py:12-17`, `backend/apps/users/models.py:28-31`。
+   - 影响范围：File2 未匹配学生、研究生、登录账号、审批记录外键、通知和导入脚本。
+   - 建议修正：实施前必须定义缺学号学生的稳定主键策略。推荐使用可追溯的临时账号，如 `TMP2026_{file1_row_no}` 或 `GRAD2026_{hash(name+college+building+room)}`，并在 File5 中增加 `source_row_id`、`user_id_source`、`student_no` 三类字段，避免把“登录账号主键”和“真实学号”混为一个字段。
+
+2. “任一宿管员可审批”与当前审批模型不兼容
+   - 位置：`docs/用户需求最终确认与实施方案.md:126-130`, `docs/用户需求最终确认与实施方案.md:248-255`, `docs/用户需求最终确认与实施方案.md:450-461`
+   - 证据：当前 `Approval.approver` 是单个用户外键；创建申请时只创建一个宿管审批记录。见 `backend/apps/approvals/models.py:14-22`, `backend/apps/applications/views.py:172-179`。方案中的 `return dorm_managers` 没有定义如何落到审批记录、权限过滤、重复审批和通知。
+   - 影响范围：提交申请、审批列表、详情权限、并发审批、通知、审计。
+   - 建议修正：MVP 不要实现“任一人可审批”的组任务，除非增加 group approval 模型。更现实的 P0 修正是要求 File3 或映射表生成一个 `primary_dorm_manager_user_id`，每栋楼唯一主责宿管员；其他宿管员作为后续代理/备份扩展。
+
+3. `ClassMapping` 移除工作量被低估，当前方案遗漏提交和流转入口
+   - 位置：`docs/用户需求最终确认与实施方案.md:321-324`
+   - 证据：现有提交申请直接查 `ClassMapping` 并用它创建宿管审批，见 `backend/apps/applications/views.py:147-179`；宿管审批通过后仍用 `ClassMapping` 创建辅导员审批，见 `backend/apps/approvals/views.py:149-174`；详情权限也按 `ClassMapping` 判断，见 `backend/apps/applications/permissions.py:11-23`。
+   - 影响范围：后端接口、权限、数据库迁移、导入命令、前端类型、测试套件和文档契约。
+   - 建议修正：把 Phase 2 拆成明确的改造清单：数据模型、提交路由、审批通过路由、列表过滤、详情权限、附件权限、导入命令、API schema、前端/miniprogram 类型、测试 fixture。未完成前不能导入真实数据并开放提交。
+
+## P1 问题清单
+
+1. 数据差异口径不一致
+   - 位置：`docs/用户需求最终确认与实施方案.md:33-40`
+   - 问题：文档同时写“File2 没有的 155 行”和“271 研究生 + 116 File2 独有”。这两个口径不能同时成立。按 5830 和 5675 的净差是 155，但若存在 271 个 File1 独有和 116 个 File2 独有，交集应为 5559。
+   - 建议修正：File5 生成报告必须输出 `file1_only_count`、`file2_only_count`、`matched_count`、`ambiguous_match_count`、`duplicate_key_count`，并把 File2 独有 116 行明确列为“不导入但归档报告”或“追加导入”。
+
+2. 状态机名称与现有代码不一致，迁移边界不清
+   - 位置：`docs/用户需求最终确认与实施方案.md:218-234`, `docs/用户需求最终确认与实施方案.md:316-319`
+   - 证据：现有状态是 `pending_dorm_manager / pending_counselor / pending_dean / approved / rejected`，不是文档里的 `PENDING / DORM_MANAGER_APPROVED / COUNSELOR_APPROVED / COMPLETED`。见 `backend/apps/applications/models.py:6-12`。
+   - 建议修正：最终状态应继续使用 API 现有风格，例如 `pending_dorm_manager -> pending_counselor -> approved`。删除或迁移 `pending_dean`，并补充历史数据迁移规则。
+
+3. 学工管理员与既有 `dean` 角色关系未定义
+   - 位置：`docs/用户需求最终确认与实施方案.md:98-115`, `docs/用户需求最终确认与实施方案.md:326-329`
+   - 证据：后端已有 `UserRole.DEAN`，前端类型也只有 `student | counselor | dean`，见 `backend/apps/users/models.py:5-9`, `frontend/types/api.ts:4-15`。
+   - 建议修正：明确是复用并重命名 `dean` 为只读管理员，还是新增 `admin` 并迁移/废弃 `dean`。推荐短期复用 `dean` 的只读语义，文案改为“学工管理员(dean/admin display name)”，代码层是否改枚举放到单独 migration。
+
+4. 路由键没有做申请时快照，后续人员/学院/楼栋变更会破坏审计
+   - 位置：`docs/用户需求最终确认与实施方案.md:85-96`, `docs/用户需求最终确认与实施方案.md:178-182`
+   - 问题：如果只从 `User.department/building_name` 动态读取，学生学院或宿管映射更新后，历史申请的可见范围和审批追溯会变化。
+   - 建议修正：`Application` 增加申请时快照字段：`student_building_name`、`student_room_number`、`student_department`、可选 `route_version`。`Approval` 已保存审批人和姓名，可保留。
+
+5. 学院/楼栋规范化缺少完整字典和阻断标准
+   - 位置：`docs/用户需求最终确认与实施方案.md:285-293`, `docs/用户需求最终确认与实施方案.md:357-361`, `docs/用户需求最终确认与实施方案.md:438-448`
+   - 问题：只给示例，没有说明 19 个学院、33 个楼栋的完整映射来源、冲突处理和失败阈值。
+   - 建议修正：将 `college_normalization_map.json` 和 `building_normalization_map.json` 列为 Phase 1 必交付；导入门禁应是 100% 路由覆盖，任何未匹配、重复唯一键、空路由键都阻断。
+
+6. 数据导入 Phase 缺少对现有导入命令的替换范围
+   - 位置：`docs/用户需求最终确认与实施方案.md:336-355`
+   - 证据：现有 `import_csv` 仍要求学生 `class_id`，并校验 `ClassMapping` 存在。见 `backend/apps/users/management/commands/import_csv.py`。
+   - 建议修正：新增或重写导入命令，不要在文档里直接使用不存在的 `import_students/import_counselors/import_dorm_managers` 命令名，除非 Phase 2 明确包含这些命令实现。
+
+7. 2.5-3 天估算偏乐观
+   - 位置：`docs/用户需求最终确认与实施方案.md:314-388`
+   - 问题：现有后端、前端、miniprogram、测试和 API 契约都依赖原 3 级/班级模型。1-1.5 天系统调整加 0.5 天前端不足以覆盖迁移、测试修复和回归。
+   - 建议修正：按 4-6 天估算更现实；或切分为“后端闭环 MVP”和“前端/管理员视图完善”两个里程碑。
+
+8. 缺少回滚策略
+   - 位置：`docs/用户需求最终确认与实施方案.md:436-472`
+   - 问题：风险章节只有缓解，没有数据库迁移失败、导入失败、上线后路由错误的回滚路径。
+   - 建议修正：补充上线前备份、迁移可逆性、导入 dry-run、导入批次号、删除/回滚本批数据脚本、功能开关或维护窗口方案。
+
+## P2 建议清单
+
+1. 前端调整不要只写“4 类用户界面”，应明确小程序、frontend、demo-web 是否都要同步。
+2. 测试用例应增加负向权限：宿管员不能看其他楼栋、辅导员不能看其他学院、管理员不能审批、学生不能访问审批列表。
+3. 寝室号未来升级建议优先建独立映射表，不建议把 `room_numbers` JSONField 作为长期方案；独立表更容易做唯一约束和导入差异报告。
+4. 通知文案需要随审批步骤更新，避免继续提示“学工部审批”。
+5. API 文档和 TypeScript 类型应列入交付物，否则前后端状态枚举会漂移。
+
+## 修正建议
+
+1. 先把文档状态从“所有 P0 阻塞已解除”改为“业务方向确认，实施前仍需关闭 P0 技术/数据门禁”。
+2. 增加 Phase 0：数据画像和路由门禁。
+   - 输出 File1/File2 匹配报告。
+   - 输出完整学院/楼栋规范化字典。
+   - 输出缺学号学生账号生成策略。
+   - 输出每名学生的宿管和辅导员路由结果。
+3. 把楼栋多宿管员规则收敛为一个 MVP 决策。
+   - 推荐：每栋楼唯一主责宿管员。
+   - 后续再做多人队列或代理审批。
+4. 重新设计数据模型变更。
+   - `User` 增加学生楼栋、寝室、专业、年级字段。
+   - `Application.class_id` 改可空或废弃展示依赖，并新增申请时路由快照字段。
+   - 明确 `dean` 到 `admin` 的迁移或复用策略。
+5. 重排实施顺序。
+   - Phase 0 数据门禁。
+   - Phase 1 后端模型和路由，带单元测试。
+   - Phase 2 导入命令 dry-run 和真实导入。
+   - Phase 3 前端/小程序/API 类型同步。
+   - Phase 4 端到端和权限回归。
+   - Phase 5 备份、上线、回滚演练。
+
+## 最低通过条件
+
+实施前至少满足以下条件：
+
+1. 5830 行学生均有非空稳定 `user_id`。
+2. 每个学生都能唯一确定一个宿管审批主体，或系统模型已支持多人待办。
+3. 每个学生都能唯一确定一个学院辅导员。
+4. `ClassMapping` 依赖清单已全部替换或兼容。
+5. `pending_dean/dean` 的迁移策略明确。
+6. 导入脚本支持 dry-run，并输出 100% 路由覆盖报告。
+7. 有数据库备份和导入批次回滚方案。

tokens used
172,435

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
