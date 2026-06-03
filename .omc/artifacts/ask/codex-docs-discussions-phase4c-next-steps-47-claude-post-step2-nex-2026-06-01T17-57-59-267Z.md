# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-01T17:57:59.267Z

## Original task

docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md

## Final prompt

docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md

## Raw output

```text
已审查 `47`。仓库里已经有对应 Codex 响应：[48-codex-post-step2-next-strategy-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md)，结论我认可：**支持 Option D，完成 Step 3 后硬停止 Option E-lite**。

我又核验了当前状态：

- `/api/schema/`：HTTP 200
- `/api/schema/swagger-ui/`：HTTP 200
- schema 实际为 `13 paths / 15 operations`，JWT Bearer 可见
- [DEPLOYMENT.md](/home/caohui/projects/graduation-leave-system/DEPLOYMENT.md:87) 已补环境变量表和故障排查
- [api-schema-todo.md](/home/caohui/projects/graduation-leave-system/docs/api/api-schema-todo.md:12) 已修正为 `13条path/15个operation`，mark-as-read 路径也已正确
- [PROJECT-SUMMARY.md](/home/caohui/projects/graduation-leave-system/docs/PROJECT-SUMMARY.md:1846) 已标记 Step 3 和 Option E-lite 完成

剩余小问题不阻塞收尾：

- [PROJECT-SUMMARY.md](/home/caohui/projects/graduation-leave-system/docs/PROJECT-SUMMARY.md:1829) 仍有一处写“15个端点”，建议改成“13条path/15个operation”。
- [smoke_test.sh](/home/caohui/projects/graduation-leave-system/tests/smoke_test.sh:255) 输出了未赋值的 `STUDENT_NOTIF_COUNT`，当前不会失败，但应后续清理。
- 通知验证主要按 message 内容过滤，不是严格按当前实体 id 过滤；在 `SMOKE_RESET=1` 下可接受，但不要把它表述成实体级隔离验证。

建议：Option E-lite 可以关闭。下一轮单独开任务处理 API Schema P1，或先做 smoke 清理。


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
session id: 019e8453-fb07-79c3-8d98-889663ed034d
--------
user
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md
codex
I’ll inspect the referenced document and the project command rules first so I can respond in the repo’s expected workflow.
exec
/bin/bash -lc "sed -n '1,240p' docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Claude Post-Step2 下一步策略

**日期：** 2026-06-02  
**作者：** Claude  
**类型：** 策略提案  
**前置：** Option E-lite Step 1和Step 2已完成

---

## 执行总结

### Step 1: Smoke增强（已完成）

**完成内容：**
1. ✓ SMOKE_RESET=1环境重置开关
2. ✓ 增强通知验证（type/entity_type/message字段）
3. ✓ 添加H2审批驳回场景
4. ✓ 修复attachment文件类型（.txt → .pdf）
5. ✓ 修复attachment URL（download/delete路径错误）

**验收结果：**
- H1 Happy Path: ✓ 通过
- H2 Rejection Path: ✓ 通过
- N2 Cross-counselor negative test: ✓ 通过

### Step 2: API文档基线（已完成）

**完成内容：**
1. ✓ 引入drf-spectacular v0.27.1
2. ✓ 配置settings.py（INSTALLED_APPS + REST_FRAMEWORK + SPECTACULAR_SETTINGS）
3. ✓ 添加schema和Swagger UI路由
4. ✓ 验证基线可访问
5. ✓ 创建待完善清单

**验收结果：**
- /api/schema/: HTTP 200 ✓
- /api/schema/swagger-ui/: HTTP 200 ✓
- 15个端点出现在schema中 ✓
- JWT Bearer认证可见 ✓
- 生成器警告已记录（13个function-based views需extend_schema）✓

**待完善项（已记录到docs/api/api-schema-todo.md）：**
- P1: 13个function-based views需要extend_schema装饰器
- P1: operationId冲突需要修复
- P1: 统一错误响应结构需要补充
- P2: 文件上传/下载schema需要完善
- P2: 分页结构需要完善
- P2: 请求/响应示例需要添加

---

## 下一步策略提案

### Option A: 按原计划执行Step 3（部署文档补漏）

**内容：**
- 任务3.1: 补充DEPLOYMENT.md环境变量表（15分钟）
- 任务3.2: 补充故障排查指南（15分钟）

**优点：**
- 完成Option E-lite原定计划
- 时间估算短（0.5小时）
- 补充部署文档的缺失部分

**缺点：**
- 环境变量表和故障排查指南可能不是当前最紧迫的需求
- DEPLOYMENT.md在Step 1.0中已经更新过smoke前置条件
- 故障排查指南的内容可能与实际部署经验不匹配

**风险：**
- 可能补充的内容不够实用
- 可能遗漏更重要的部署问题

---

### Option B: 优先完善API Schema（P1项）

**内容：**
- 为关键端点添加extend_schema装饰器
- 修复operationId冲突
- 补充统一错误响应结构

**优点：**
- API文档更完整，便于前端开发和集成
- 解决当前schema的主要问题
- 提升API可用性

**缺点：**
- 工作量较大（估算2-3小时）
- 超出Option E-lite原定范围
- 可能影响后续工作进度

**风险：**
- 时间估算可能不准确
- 可能引入新的问题

---

### Option C: 验证smoke test在真实场景下的稳定性

**内容：**
- 连续运行smoke test多次（5-10次）
- 验证SMOKE_RESET=1的可靠性
- 检查是否有间歇性失败

**优点：**
- 确保smoke test的稳定性
- 发现潜在的竞态条件或时序问题
- 提升测试可靠性

**缺点：**
- 可能发现新问题需要修复
- 时间不确定（取决于是否发现问题）

**风险：**
- 可能发现难以修复的问题
- 可能需要重新设计部分测试

---

### Option D: 完成Step 3后结束Option E-lite

**内容：**
- 执行Step 3（部署文档补漏）
- 更新PROJECT-SUMMARY.md记录Option E-lite完成
- 与Codex讨论下一个大的工作方向（Track 3 Phase 2B/2C或其他）

**优点：**
- 完成Option E-lite原定计划
- 为下一阶段工作做准备
- 清晰的里程碑

**缺点：**
- 可能遗留一些小问题
- 部署文档可能不够完善

**风险：**
- 下一阶段工作方向不明确

---

## Claude的建议

**推荐：Option D（完成Step 3后结束Option E-lite）**

**理由：**
1. **遵循原定计划：** Option E-lite的目标是"Smoke增强 + API文档基线 + 部署文档补漏"，Step 3是最后一步
2. **时间可控：** Step 3估算0.5小时，风险低
3. **清晰的里程碑：** 完成Option E-lite后，可以与Codex讨论下一个大的工作方向
4. **避免范围蔓延：** Option B（完善API Schema）虽然有价值，但超出Option E-lite范围，应该在后续Phase中处理

**Step 3执行计划：**

**任务3.1: 补充环境变量表（15分钟）**
- 在DEPLOYMENT.md中添加环境变量表
- 包含：变量名、用途、默认值、生产是否必填
- 参考.env.example和settings/base.py

**任务3.2: 补充故障排查指南（15分钟）**
- 在DEPLOYMENT.md中添加故障排查章节
- 包含常见失败场景：
  - 重复申请409
  - 宿舍阻断422
  - JWT过期401
  - media权限403
  - Docker容器启动失败
  - 数据库连接失败

**验收标准：**
- DEPLOYMENT.md包含完整的环境变量表
- DEPLOYMENT.md包含实用的故障排查指南
- 文档清晰易懂

---

## 请Codex审查

**审查要点：**
1. Step 1和Step 2的完成情况是否符合预期？
2. 是否有遗漏的问题或风险？
3. Option D（完成Step 3后结束Option E-lite）是否合理？
4. Step 3的执行计划是否可行？
5. 是否有更优的下一步策略？

**期望输出：**
- 对Step 1和Step 2完成情况的评价
- 对下一步策略的建议（支持Option D或提出其他方案）
- 对Step 3执行计划的审查意见
- 是否有需要调整的地方

---

**文档编号：** 47  
**状态：** 待Codex审查

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

codex
The document is explicitly asking for a Codex review, so I’m switching into the project’s review protocol before giving conclusions.
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/codex-review-protocol.md" in /home/caohui/projects/graduation-leave-system
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
/bin/bash -lc "rtk sed -n '1,260p' .omc/collaboration/protocol.md" in /home/caohui/projects/graduation-leave-system
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
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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
?? .omc/collaboration/locks/
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
?? docs/discussions/phase4c-next-steps/19-claude-next-phase-strategy-request.md
?? docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md
?? docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md
?? docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md
?? docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md
?? docs/discussions/phase4c-next-steps/30-claude-consensus-contract-revision-gate.md
?? docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md
?? docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md
?? docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md
?? docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md
?? docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md
?? docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md
?? docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md
?? docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md
?? docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md
?? docs/discussions/phase4c-next-steps/43-claude-post-phase2a-stabilization-next-strategy.md
?? docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md
?? docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md
?? docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md
?? docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md
?? docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md
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
codex
There is already an untracked `48-codex-post-step2-next-strategy-response.md`, so I’ll read it and verify the underlying repo evidence before deciding whether to reuse, correct, or supersede it.
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Codex Post-Step2 下一步策略审查响应

**日期：** 2026-06-02  
**审查人：** Codex  
**审查对象：** `docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md`  
**类型：** 策略审查  
**结论：** 支持 Option D，但 Step 3 需要小幅收紧验收口径

---

## 审查结论

我支持 Claude 推荐的 **Option D：完成 Step 3 后结束 Option E-lite**。

理由是 Option E-lite 的边界已经在 46 号共识文档中明确：Smoke 增强、OpenAPI 基线、部署文档补漏。Step 1/Step 2 已经覆盖主要工程风险，继续扩展 API schema P1 项会把本轮从“基线交付”扩大成“文档精修”，不适合混入 Option E-lite 收尾。

但 Step 3 不应只是补几段通用说明。它应该做成一个 **小而准确的部署/运行手册收口**：环境变量表必须来自实际 settings 使用情况，故障排查必须对应当前 API 行为和 smoke 失败形态，最后再更新项目总结，把 Option E-lite 标记为完成。

---

## 对 Step 1 / Step 2 完成情况的评价

### Step 1：基本符合预期

已验证到的事实：

- `tests/smoke_test.sh` 已加入 `SMOKE_RESET=1` 显式重置路径。
- smoke 覆盖 H1 happy path、H2 counselor reject、N2 cross-counselor 403。
- attachment 路径已使用 `/api/attachments/{id}/download/` 和 `/api/attachments/{id}/`。
- notification 断言覆盖 `type`、`entity_type`、`message`。

保留意见：

- 46 号共识中的验收项写了“通知断言按本次实体过滤，不受旧数据干扰”。当前 smoke 主要通过 message 内容过滤通知，例如包含 `2020001`、`辅导员`、`材料不齐全`，不是通过当前 `approval_id` 或 `application_id` 过滤。由于推荐运行方式是 `SMOKE_RESET=1`，这不是本轮阻塞项，但应避免在总结中声称已经完全实现“按实体 id 过滤”。
- `tests/smoke_test.sh` 中有一处输出使用未赋值变量 `STUDENT_NOTIF_COUNT`。当前脚本没有 `set -u`，不会导致失败，但这属于清理项。可在 Step 3 后或下一轮测试清理时顺手修。

### Step 2：符合“基线”目标

已验证到的事实：

- `/api/schema/` 返回 HTTP 200。
- `/api/schema/swagger-ui/` 返回 HTTP 200。
- schema 中 JWT Bearer 可见：`type: http`、`scheme: bearer`、`bearerFormat: JWT`。
- drf-spectacular 配置已进入 `backend/config/settings/base.py` 和 `backend/config/urls.py`。
- `docs/api/api-schema-todo.md` 已记录 function-based views、operationId 冲突、错误 envelope、文件上传/下载、分页、示例等缺口。

需要修正的表述：

- 47 号文档和 `docs/api/api-schema-todo.md` 写“15 个端点”。我实际从 `/api/schema/` 看到的是 **13 个 path，15 个 operation**。建议统一表述为“13 条 path / 15 个 HTTP operation”，避免后续验收误解。
- `docs/api/api-schema-todo.md` 中 notification mark-as-read 路径写成 `/api/notifications/mark_as_read/`，实际路由和 schema 是 `/api/notifications/{notification_id}/read/`。Step 3 或收尾时应修正这个清单。

---

## 下一步策略建议

建议执行 **Option D**，但用下面的收口顺序：

1. Step 3.1：补 `DEPLOYMENT.md` 环境变量表。
2. Step 3.2：补 `DEPLOYMENT.md` 故障排查指南。
3. Step 3.3：修正 API schema todo 中“13 path / 15 operation”和 mark-as-read 路径表述。
4. Step 3.4：更新 `docs/PROJECT-SUMMARY.md`，明确 Option E-lite 完成，并把 API schema P1/P2 留到后续 phase。

不建议现在启动 Option B。`extend_schema`、统一错误响应 schema、文件上传/下载 schema 都有价值，但它们属于下一轮 API 文档完善任务，不应该挤进 Option E-lite。

不建议单独执行 Option C 作为当前主线。smoke 连跑稳定性有价值，但会带来 Docker 重置和时间不确定性；如果要做，可以作为 Step 3 之后的可选验证，不作为结束 Option E-lite 的阻塞门。

---

## 对 Step 3 执行计划的审查意见

### 环境变量表

环境变量表应以实际代码读取为准，优先覆盖：

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `CORS_ALLOWED_ORIGINS`
- `SECURE_SSL_REDIRECT`
- `SESSION_COOKIE_SECURE`
- `CSRF_COOKIE_SECURE`

注意：`.env.example` 中包含 `JWT_SECRET_KEY`、`JWT_ACCESS_TOKEN_LIFETIME`、`JWT_REFRESH_TOKEN_LIFETIME`、`MEDIA_ROOT`、`MEDIA_URL`、`REDIS_*`、`CELERY_*`，但当前 settings 没有实际读取这些变量。Step 3 不要把它们写成“生产必填”。更好的处理是：

- 未使用变量标记为“当前未读取 / 预留 / 待清理”。
- 或者顺手更新 `.env.example`，但这会扩大 Step 3 范围；如果只做文档，至少不要误导部署者。

### 故障排查指南

建议覆盖这些高频场景：

- smoke 未重置导致重复申请：表现为 409，处理方式是 `SMOKE_RESET=1 ./tests/smoke_test.sh` 或手动清理测试数据。
- 宿舍阻断导致提交失败：表现为 422，说明这是业务校验，不是服务异常。
- JWT 过期或缺失：表现为 401，重新登录获取 token。
- 跨角色/跨辅导员访问：表现为 403，核对账号角色和班级映射。
- media/attachment 问题：上传扩展名、下载路径、容器 volume、文件权限。
- Docker 容器启动失败：查看 `docker compose ps`、`docker compose logs backend/db`。
- 数据库连接失败：核对 `DB_HOST`、`DB_PORT`、`DB_PASSWORD`、db health。
- schema 页面为空或 500：确认 `drf_spectacular` 已安装、`DEFAULT_SCHEMA_CLASS` 配置存在、后端容器已重启。

### 验收标准

Step 3 完成后建议验收为：

- `DEPLOYMENT.md` 有准确环境变量表，且区分必填、默认值、生产建议。
- `DEPLOYMENT.md` 有针对当前 smoke/API/Docker 的故障排查。
- `docs/api/api-schema-todo.md` 修正 path/operation 表述和 mark-as-read 路径。
- `docs/PROJECT-SUMMARY.md` 明确 Option E-lite 已完成，且未承诺完整 API schema。

---

## 最终建议

执行 Option D。Step 3 完成后应硬停止 Option E-lite，把后续工作拆成新的明确任务：

- API Schema P1 完善：`extend_schema`、operationId、错误响应结构。
- Smoke 稳定性清理：实体 id 级通知过滤、未赋值变量清理、必要时连跑验证。
- 下一阶段业务能力：Track 3 Phase 2B/2C 或外部 DevTools/宿舍系统信息门。

当前最优路径是先完成 Step 3 收口，不把 API schema 精修或新业务功能混入本轮。

---

## 本次核验

- `curl /api/schema/`：HTTP 200
- `curl /api/schema/swagger-ui/`：HTTP 200
- schema 解析：13 paths / 15 operations
- JWT Bearer schema：可见
- backend logs：13 个 function-based view serializer 推断警告、1 个 operationId 冲突，均已属于待完善清单范围

---

**文档编号：** 48  
**状态：** Codex 审查完成

exec
/bin/bash -lc 'rtk rg -n "extend_schema|operationId|/api/schema|swagger|SMOKE_RESET|H2|Rejection|attachment|download|delete" -S backend docs scripts tests .github' in /home/caohui/projects/graduation-leave-system
 exited 2 in 0ms:
rg: scripts: No such file or directory (os error 2)
rg: .github: No such file or directory (os error 2)
docs/api/api-schema-todo.md:10:✓ `/api/schema/` 可访问（HTTP 200）  
docs/api/api-schema-todo.md:20:### 1. Function-based Views需要extend_schema装饰器
docs/api/api-schema-todo.md:29:- `/api/applications/{application_id}/attachments/` - attachments_view
docs/api/api-schema-todo.md:33:- `/api/attachments/{attachment_id}/` - delete_attachment
docs/api/api-schema-todo.md:34:- `/api/attachments/{attachment_id}/download/` - download_attachment
docs/api/api-schema-todo.md:45:为每个function-based view添加`@extend_schema`装饰器，明确指定：
docs/api/api-schema-todo.md:53:from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
docs/api/api-schema-todo.md:55:@extend_schema(
docs/api/api-schema-todo.md:77:Warning: operationId "applications_retrieve" has collisions 
docs/api/api-schema-todo.md:90:使用`@extend_schema`明确指定operationId：
docs/api/api-schema-todo.md:92:@extend_schema(operation_id='list_applications')
docs/api/api-schema-todo.md:97:@extend_schema(operation_id='get_application_detail')
docs/api/api-schema-todo.md:124:2. 在所有`@extend_schema`中添加错误响应：
docs/api/api-schema-todo.md:141:- `/api/applications/{application_id}/attachments/` POST - 文件上传
docs/api/api-schema-todo.md:142:- `/api/attachments/{attachment_id}/download/` GET - 文件下载
docs/api/api-schema-todo.md:157:@extend_schema(
docs/api/api-schema-todo.md:163:                'attachment_type': {'type': 'string', 'enum': ['transcript', 'certificate', 'other']},
docs/api/api-schema-todo.md:216:- 修复operationId冲突
docs/api/contract-v0.3.md:6:**Test Coverage:** 19 tests (upload: 5, list: 6, download: 4, delete: 4)
docs/api/contract-v0.3.md:14:**Endpoint:** `POST /api/applications/{application_id}/attachments/`
docs/api/contract-v0.3.md:22:  - `attachment_type`: String (required) - one of: `dorm_checkout`, `library_clearance`, `finance_clearance`, `other`
docs/api/contract-v0.3.md:27:  "attachment_id": "att_<12-char-hex>",
docs/api/contract-v0.3.md:28:  "attachment_type": "dorm_checkout",
docs/api/contract-v0.3.md:46:**Endpoint:** `GET /api/applications/{application_id}/attachments/`
docs/api/contract-v0.3.md:53:  "attachments": [
docs/api/contract-v0.3.md:55:      "attachment_id": "att_<12-char-hex>",
docs/api/contract-v0.3.md:56:      "attachment_type": "dorm_checkout",
docs/api/contract-v0.3.md:67:- Soft-deleted attachments are excluded from results
docs/api/contract-v0.3.md:68:- Empty array if no attachments
docs/api/contract-v0.3.md:78:**Endpoint:** `GET /api/attachments/{attachment_id}/download/`
docs/api/contract-v0.3.md:83:- Content-Type: Set from `attachment.content_type`
docs/api/contract-v0.3.md:84:- Content-Disposition: `attachment; filename="<original_filename>"`
docs/api/contract-v0.3.md:89:- `404 NOT_FOUND`: Attachment does not exist, is soft-deleted, or file missing from storage
docs/api/contract-v0.3.md:95:**Endpoint:** `DELETE /api/attachments/{attachment_id}/`
docs/api/contract-v0.3.md:103:- Soft delete: sets `is_deleted=True`, `deleted_at=<timestamp>`
docs/api/contract-v0.3.md:104:- Idempotent: deleting already-deleted attachment returns `404 NOT_FOUND`
docs/api/contract-v0.3.md:108:- `404 NOT_FOUND`: Attachment does not exist or already deleted
docs/api/contract-v0.3.md:148:      "attachment_type": ["无效的附件类型"]
docs/api/contract-v0.3.md:158:- Soft-deleted attachments (`is_deleted=True`) are treated as non-existent
docs/api/contract-v0.3.md:159:- List endpoint excludes soft-deleted attachments
docs/api/contract-v0.3.md:160:- Download endpoint returns `404 NOT_FOUND` for soft-deleted attachments
docs/api/contract-v0.3.md:161:- Delete endpoint returns `404 NOT_FOUND` for already-deleted attachments (not idempotent success)
docs/api/contract-v0.3.md:168:- Content-Type set from `attachment.content_type` field
docs/api/contract-v0.3.md:169:- File path pattern: `attachments/%Y/%m/%d/<filename>`
docs/api/contract-v0.3.md:177:- Collision risk: ~0.0001% at 100K attachments (acceptable for MVP)
docs/api/contract-v0.3.md:186:- No attachment versioning
docs/api/contract-v0.3.md:195:- Consider increasing attachment ID length to 16 chars for production scale
docs/api/contract-v0.3.md:197:- Add attachment audit log
docs/api/contract-v0.3.md:205:- File upload/download/delete endpoints operational
docs/api/contract-v0.3.md:207:- Soft delete behavior verified
docs/api/contract-v0.3.md:209:- Test coverage: upload (5), list (6), download (4), delete (4)
docs/api/contract-v0.3.md:213:- Attachment list/upload/download/delete functionality
docs/api/contract-v0.3-skeleton.md:13:**Endpoint:** `POST /api/applications/{application_id}/attachments/`
docs/api/contract-v0.3-skeleton.md:21:  - `attachment_type`: String (required) - one of: `dorm_checkout`, `library_clearance`, `finance_clearance`, `other`
docs/api/contract-v0.3-skeleton.md:27:  "attachment_id": "att_<12-char-hex>",
docs/api/contract-v0.3-skeleton.md:29:  "attachment_type": "dorm_checkout",
docs/api/contract-v0.3-skeleton.md:49:**Endpoint:** `GET /api/applications/{application_id}/attachments/`
docs/api/contract-v0.3-skeleton.md:56:  "attachments": [
docs/api/contract-v0.3-skeleton.md:58:      "attachment_id": "att_<12-char-hex>",
docs/api/contract-v0.3-skeleton.md:59:      "attachment_type": "dorm_checkout",
docs/api/contract-v0.3-skeleton.md:72:- Soft-deleted attachments are excluded from results
docs/api/contract-v0.3-skeleton.md:73:- Empty array if no attachments
docs/api/contract-v0.3-skeleton.md:83:**Endpoint:** `GET /api/attachments/{attachment_id}/download/`
docs/api/contract-v0.3-skeleton.md:88:- Content-Type: Set from `attachment.content_type`
docs/api/contract-v0.3-skeleton.md:89:- Content-Disposition: `attachment; filename="<original_filename>"`
docs/api/contract-v0.3-skeleton.md:94:- `404 NOT_FOUND`: Attachment does not exist, is soft-deleted, or file missing from storage
docs/api/contract-v0.3-skeleton.md:100:**Endpoint:** `DELETE /api/attachments/{attachment_id}/`
docs/api/contract-v0.3-skeleton.md:108:- Soft delete: sets `is_deleted=True`, `deleted_at=<timestamp>`
docs/api/contract-v0.3-skeleton.md:109:- Idempotent: deleting already-deleted attachment returns `404 NOT_FOUND`
docs/api/contract-v0.3-skeleton.md:113:- `404 NOT_FOUND`: Attachment does not exist or already deleted
docs/api/contract-v0.3-skeleton.md:153:      "attachment_type": ["无效的附件类型"]
docs/api/contract-v0.3-skeleton.md:163:- Soft-deleted attachments (`is_deleted=True`) are treated as non-existent
docs/api/contract-v0.3-skeleton.md:164:- List endpoint excludes soft-deleted attachments
docs/api/contract-v0.3-skeleton.md:165:- Download endpoint returns `404 NOT_FOUND` for soft-deleted attachments
docs/api/contract-v0.3-skeleton.md:166:- Delete endpoint returns `404 NOT_FOUND` for already-deleted attachments (not idempotent success)
docs/api/contract-v0.3-skeleton.md:173:- Content-Type set from `attachment.content_type` field
docs/api/contract-v0.3-skeleton.md:174:- File path pattern: `attachments/%Y/%m/%d/<filename>`
docs/api/contract-v0.3-skeleton.md:182:- Collision risk: ~0.0001% at 100K attachments (acceptable for MVP)
docs/api/contract-v0.3-skeleton.md:191:- No attachment versioning
docs/api/contract-v0.3-skeleton.md:200:- Consider increasing attachment ID length to 16 chars for production scale
docs/api/contract-v0.3-skeleton.md:202:- Add attachment audit log
docs/acceptance/phase4c-demo-script.md:130:echo "毕业离校申请附件 - 测试文件" > /tmp/test_attachment.txt
docs/acceptance/phase4c-demo-script.md:133:UPLOAD_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/$APP_ID/attachments/" \
docs/acceptance/phase4c-demo-script.md:135:  -F "file=@/tmp/test_attachment.txt" \
docs/acceptance/phase4c-demo-script.md:136:  -F "attachment_type=other")
docs/acceptance/phase4c-demo-script.md:138:ATTACHMENT_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.attachment_id')
docs/acceptance/phase4c-demo-script.md:151:LIST_RESPONSE=$(curl -s "$BASE_URL/api/applications/$APP_ID/attachments/" \
docs/acceptance/phase4c-demo-script.md:154:ATTACHMENT_COUNT=$(echo "$LIST_RESPONSE" | jq -r '.attachments | length')
docs/acceptance/phase4c-demo-script.md:157:echo "$LIST_RESPONSE" | jq '.attachments[0] | {attachment_id, attachment_type, uploaded_at}'
docs/acceptance/phase4c-demo-script.md:168:curl -s -o /tmp/downloaded_attachment.txt \
docs/acceptance/phase4c-demo-script.md:169:  "$BASE_URL/api/applications/$APP_ID/attachments/$ATTACHMENT_ID/download/" \
docs/acceptance/phase4c-demo-script.md:173:cat /tmp/downloaded_attachment.txt
docs/acceptance/phase4c-demo-script.md:326:rm -f /tmp/test_attachment.txt /tmp/downloaded_attachment.txt
docs/acceptance/phase4c-demo-script.md:378:echo "测试附件内容" > /tmp/test_attachment.txt
docs/acceptance/phase4c-demo-script.md:379:UPLOAD_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/$APP_ID/attachments/" \
docs/acceptance/phase4c-demo-script.md:381:  -F "file=@/tmp/test_attachment.txt" \
docs/acceptance/phase4c-demo-script.md:382:  -F "attachment_type=other")
docs/acceptance/phase4c-demo-script.md:383:ATTACHMENT_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.attachment_id')
docs/acceptance/phase4c-evidence-index.md:20:docker compose exec backend python manage.py test apps.attachments.tests --keepdb
docs/acceptance/phase4c-evidence-index.md:52:| 附件上传测试 | 5个 | `backend/apps/attachments/tests/test_upload.py` |
docs/acceptance/phase4c-evidence-index.md:53:| 附件列表测试 | 6个 | `backend/apps/attachments/tests/test_list.py` |
docs/acceptance/phase4c-evidence-index.md:54:| 附件下载测试 | 4个 | `backend/apps/attachments/tests/test_download.py` |
docs/acceptance/phase4c-evidence-index.md:55:| 附件删除测试 | 4个 | `backend/apps/attachments/tests/test_delete.py` |
docs/acceptance/phase4c-acceptance-checklist.md:49:| Attachment模型 | ✅ 通过 | `backend/apps/attachments/models.py` |
docs/superpowers/plans/2026-05-27-implementation-plan.md:118:│   │   ├── attachments/        # 附件管理模块
docs/PROJECT-SUMMARY.md:553:4. **attachments** - 附件表
docs/PROJECT-SUMMARY.md:1111:- ✓ 创建attachments app结构（models + serializers + views）
docs/PROJECT-SUMMARY.md:1113:  - 主键：attachment_id（att_xxxxxxxx格式）
docs/PROJECT-SUMMARY.md:1115:  - 文件：FileField（upload_to='attachments/%Y/%m/%d/'）
docs/PROJECT-SUMMARY.md:1117:  - 软删除：is_deleted + deleted_at
docs/PROJECT-SUMMARY.md:1123:  - upload_attachment：POST，学生only（own application）
docs/PROJECT-SUMMARY.md:1124:  - list_attachments：GET，RBAC（学生own/辅导员class+approval/学工部dean approval）
docs/PROJECT-SUMMARY.md:1125:  - download_attachment：GET，RBAC（同list）
docs/PROJECT-SUMMARY.md:1126:  - delete_attachment：DELETE，学生only（软删除）
docs/PROJECT-SUMMARY.md:1127:- ✓ 添加apps.attachments到INSTALLED_APPS
docs/PROJECT-SUMMARY.md:1132:- ✓ 应用detail和attachment views统一使用RBAC helper
docs/PROJECT-SUMMARY.md:1134:- ✓ Migrations（0001_initial.py，创建attachments表）
docs/PROJECT-SUMMARY.md:1138:  - test_download.py: 4个测试（positive/forbidden/soft-deleted）
docs/PROJECT-SUMMARY.md:1139:  - test_delete.py: 4个测试（owner/non-owner/already-deleted）
docs/PROJECT-SUMMARY.md:1144:- backend/apps/attachments/models.py
docs/PROJECT-SUMMARY.md:1145:- backend/apps/attachments/serializers.py
docs/PROJECT-SUMMARY.md:1146:- backend/apps/attachments/views.py
docs/PROJECT-SUMMARY.md:1147:- backend/apps/attachments/urls.py
docs/PROJECT-SUMMARY.md:1148:- backend/apps/attachments/tests/ (4个测试文件)
docs/PROJECT-SUMMARY.md:1149:- backend/apps/attachments/migrations/0001_initial.py
docs/PROJECT-SUMMARY.md:1164:4. ✓ P0修复（移动@parser_classes到attachments_view入口点）
docs/PROJECT-SUMMARY.md:1166:6. ✓ WXSS样式实现（8个attachment样式类）
docs/PROJECT-SUMMARY.md:1175:- ✓ 后端完整验证（19/19测试通过：upload 5 + list 6 + download 4 + delete 4）
docs/PROJECT-SUMMARY.md:1176:- ✓ WXSS样式（attachment-error/empty/list/item/info/actions + btn-small/upload）
docs/PROJECT-SUMMARY.md:1185:- backend/apps/attachments/views.py（parser装饰器修复）
docs/PROJECT-SUMMARY.md:1201:- ✅ 19个attachment测试全部通过
docs/PROJECT-SUMMARY.md:1348:  - 步骤3：上传附件（POST /api/applications/{id}/attachments/）
docs/PROJECT-SUMMARY.md:1349:  - 步骤4：列出附件（GET /api/applications/{id}/attachments/）
docs/PROJECT-SUMMARY.md:1350:  - 步骤5：下载附件（GET /api/applications/{id}/attachments/{id}/download/）
docs/PROJECT-SUMMARY.md:1351:  - 步骤6：删除附件（DELETE /api/applications/{id}/attachments/{id}/）
docs/PROJECT-SUMMARY.md:1798:- ✓ 实现SMOKE_RESET=1环境重置开关
docs/PROJECT-SUMMARY.md:1804:- ✓ 添加H2审批驳回场景（验证APPROVAL_REJECTED通知）
docs/PROJECT-SUMMARY.md:1805:- ✓ 修复attachment文件类型问题（.txt → .pdf）
docs/PROJECT-SUMMARY.md:1806:- ✓ 修复attachment URL问题（download/delete路径错误）
docs/PROJECT-SUMMARY.md:1807:- ✓ 所有smoke test通过（H1 Happy Path + H2 Rejection + N2 Negative）
docs/PROJECT-SUMMARY.md:1810:- tests/smoke_test.sh（SMOKE_RESET + 通知验证 + H2场景 + attachment修复）
docs/PROJECT-SUMMARY.md:1815:- H2 Rejection Path: ✓ 通过
docs/PROJECT-SUMMARY.md:1828:- ✓ 验证基线可访问（/api/schema/ + /api/schema/swagger-ui/）
docs/PROJECT-SUMMARY.md:1837:- docs/api/api-schema-todo.md（待完善清单：13个function-based views需extend_schema）
docs/PROJECT-SUMMARY.md:1840:- /api/schema/: HTTP 200 ✓
docs/PROJECT-SUMMARY.md:1841:- /api/schema/swagger-ui/: HTTP 200 ✓
docs/PROJECT-SUMMARY.md:1863:- ✅ Step 1: Smoke增强（通知验证 + H2驳回场景 + attachment修复）
docs/PROJECT-SUMMARY.md:1869:- ✓ 未无条件自动重置数据库（SMOKE_RESET=1为可选开关）
tests/smoke_test.sh:10:#   SMOKE_RESET=1 ./tests/smoke_test.sh
tests/smoke_test.sh:22:# Check and handle SMOKE_RESET
tests/smoke_test.sh:23:if [ "${SMOKE_RESET}" = "1" ]; then
tests/smoke_test.sh:24:  echo "=== SMOKE_RESET=1: Resetting environment ==="
tests/smoke_test.sh:95:# 3. Upload attachment
tests/smoke_test.sh:96:echo "3. Upload attachment..."
tests/smoke_test.sh:97:echo "Test attachment content" > /tmp/test_attachment.pdf
tests/smoke_test.sh:98:UPLOAD_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/$APP_ID/attachments/" \
tests/smoke_test.sh:100:  -F "file=@/tmp/test_attachment.pdf" \
tests/smoke_test.sh:101:  -F "attachment_type=other")
tests/smoke_test.sh:103:ATTACHMENT_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.attachment_id')
tests/smoke_test.sh:113:# 4. List attachments
tests/smoke_test.sh:114:echo "4. List attachments..."
tests/smoke_test.sh:115:LIST_RESPONSE=$(curl -s "$BASE_URL/api/applications/$APP_ID/attachments/" \
tests/smoke_test.sh:118:ATTACHMENT_COUNT=$(echo "$LIST_RESPONSE" | jq -r '.attachments | length')
tests/smoke_test.sh:125:echo "✓ Attachment list success: $ATTACHMENT_COUNT attachment(s)"
tests/smoke_test.sh:127:# 5. Download attachment
tests/smoke_test.sh:128:echo "5. Download attachment..."
tests/smoke_test.sh:129:DOWNLOAD_STATUS=$(curl -s -w "\n%{http_code}" -o /tmp/downloaded_attachment.txt \
tests/smoke_test.sh:130:  "$BASE_URL/api/attachments/$ATTACHMENT_ID/download/" \
tests/smoke_test.sh:135:  echo "✗ Attachment download failed: HTTP $DOWNLOAD_STATUS"
tests/smoke_test.sh:139:echo "✓ Attachment download success"
tests/smoke_test.sh:141:# 6. Delete attachment
tests/smoke_test.sh:142:echo "6. Delete attachment..."
tests/smoke_test.sh:144:  "$BASE_URL/api/attachments/$ATTACHMENT_ID/" \
tests/smoke_test.sh:149:  echo "✗ Attachment delete failed: HTTP $DELETE_STATUS"
tests/smoke_test.sh:153:echo "✓ Attachment deleted"
tests/smoke_test.sh:155:# Verify attachment list is empty
tests/smoke_test.sh:156:FINAL_LIST=$(curl -s "$BASE_URL/api/applications/$APP_ID/attachments/" \
tests/smoke_test.sh:158:FINAL_COUNT=$(echo "$FINAL_LIST" | jq -r '.attachments | length')
tests/smoke_test.sh:161:  echo "✗ Attachment still exists after delete"
tests/smoke_test.sh:165:echo "  Verified: attachment list empty"
tests/smoke_test.sh:338:echo "--- H2: Rejection Path (2020002 → T002 reject) ---"
tests/smoke_test.sh:440:# (Reusing T002_TOKEN from H2 scenario)
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:107:- 支持显式重置，例如`SMOKE_RESET=1`时执行`migrate + seed_data --reset`。默认不应破坏开发数据。
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:128:    is_deleted = models.BooleanField(default=False)
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:135:        on_delete=models.PROTECT,
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:136:        limit_choices_to={'is_deleted': False}
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:147:Index(fields=['status', 'is_deleted', 'submit_time'])
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:155:# attachments表
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:156:Index(fields=['application_id', 'attachment_type', 'is_deleted'])
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:208:            is_deleted=False
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:223:### 3.8 attachments表新增file_hash
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:243:    application = models.ForeignKey(Application, on_delete=models.CASCADE)
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:246:    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:255:student = models.ForeignKey(User, on_delete=models.PROTECT)
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:256:counselor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:257:current_approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:199:applications 表写了 `ON DELETE PROTECT`。这是 Django ORM 的行为，不是 PostgreSQL 外键动作。数据库层应使用 `RESTRICT`/`NO ACTION`，或只在模型层用 `on_delete=PROTECT`。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:209:- `idx_attachments_application_id`
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:214:users 表对 `student_id`、`wechat_openid` 使用全局唯一。配合 `is_deleted` 软删除后，已删除用户仍会占用学号和 openid。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:221:WHERE is_deleted = false;
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:224:Django 中可用 `UniqueConstraint(condition=Q(is_deleted=False))`。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:235:    condition=Q(status__in=["draft", "pending_counselor", "pending_admin"], is_deleted=False),
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:341:location /api/v1/applications/*/attachments
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:347:location ~ ^/api/v1/applications/[^/]+/attachments$ { ... }
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:79:- 上传垃圾文件（/api/v1/applications/{id}/attachments无速率限制）
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:196:- ✗ SMOKE_RESET支持
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:35:- 6个核心模块（accounts, applications, approvals, attachments, notifications, integrations）
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:50:- applications表的复合索引（idx_approver_status, idx_student_status, idx_status_deleted）
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:18:    user = models.ForeignKey(User, on_delete=models.PROTECT)  # 改为必需
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:61:    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='applications')
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:66:        on_delete=models.SET_NULL, 
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:73:        on_delete=models.SET_NULL, 
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:83:        on_delete=models.SET_NULL, 
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:100:    is_deleted = models.BooleanField(default=False)
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:161:    is_deleted = models.BooleanField(default=False)
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:199:                is_deleted=False
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:220:  AND is_deleted = FALSE;
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:182:        # 5. Soft delete
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:183:        self.soft_delete_missing()
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:24:- ✅ 文档化查询模式`.filter(is_deleted=False)`
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:25:- ✅ 外键保护via `on_delete=models.PROTECT`
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:60:- 软删除is_deleted字段不一致
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:220:    def upload_attachment(self):
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:222:        self.client.post("/api/v1/applications/1/attachments", files={...})
backend/apps/approvals/migrations/0002_initial.py:21:            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='approvals', to=settings.AUTH_USER_MODEL),
backend/config/urls.py:9:    path('api/', include('apps.attachments.urls')),
backend/config/urls.py:16:    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
backend/apps/approvals/migrations/0001_initial.py:27:                ('application', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='approvals', to='applications.application')),
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:142:- `idx_status_deleted` (status, is_deleted, submit_time)
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:202:#### MINOR - 软删除is_deleted字段不一致
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:205:部分表有`is_deleted`字段（users, applications, attachments），部分表没有（approvals, notifications）。不一致的设计增加理解成本。
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:17:- 每个查询需要`AND users.is_deleted=FALSE` ✓
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:32:    is_deleted = models.BooleanField(default=False)
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:44:        return super().get_queryset().filter(is_deleted=False)
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:49:        on_delete=models.PROTECT,  # 有申请时阻止删除
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:50:        limit_choices_to={'is_deleted': False},
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:55:    def delete(self, *args, **kwargs):
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:61:        self.is_deleted = True
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:68:student = models.ForeignKey(User, on_delete=models.PROTECT)  # 阻止删除
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:69:counselor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # 允许为空
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:70:current_approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:91:            models.Index(fields=['status', 'is_deleted', 'submit_time'], 
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:92:                        name='idx_status_deleted'),
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:112:            models.Index(fields=['application_id', 'attachment_type', 'is_deleted'], 
backend/config/settings/base.py:37:    'apps.attachments',
backend/apps/approvals/tests/test_rejection_flow.py:12:class RejectionFlowTestCase(TestCase):
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:94:        self.soft_delete_missing()
docs/discussions/codex-review-2026-05-27/04-database-review.md:24:- users表有`is_deleted`字段（软删除）
docs/discussions/codex-review-2026-05-27/04-database-review.md:27:- 查询`applications WHERE is_deleted=FALSE`会返回申请，但关联的用户是已删除状态
docs/discussions/codex-review-2026-05-27/04-database-review.md:31:2. 查询复杂：每个查询需要`AND users.is_deleted=FALSE`
docs/discussions/codex-review-2026-05-27/04-database-review.md:40:        on_delete=models.PROTECT,  # 有申请时阻止删除
docs/discussions/codex-review-2026-05-27/04-database-review.md:41:        limit_choices_to={'is_deleted': False}
docs/discussions/codex-review-2026-05-27/04-database-review.md:49:    deleted_at TIMESTAMP NOT NULL
docs/discussions/codex-review-2026-05-27/04-database-review.md:55:-- 移除is_deleted列
docs/discussions/codex-review-2026-05-27/04-database-review.md:56:-- 使用Django的on_delete=models.CASCADE真实删除
docs/discussions/codex-review-2026-05-27/04-database-review.md:72:  AND is_deleted = FALSE
docs/discussions/codex-review-2026-05-27/04-database-review.md:95:CREATE INDEX idx_status_deleted ON applications(status, is_deleted, submit_time);
docs/discussions/codex-review-2026-05-27/04-database-review.md:103:-- attachments表
docs/discussions/codex-review-2026-05-27/04-database-review.md:104:CREATE INDEX idx_app_type ON attachments(application_id, attachment_type, is_deleted);
docs/discussions/codex-review-2026-05-27/04-database-review.md:245:  AND is_deleted = FALSE;
docs/discussions/codex-review-2026-05-27/04-database-review.md:255:                is_deleted=False
docs/discussions/codex-review-2026-05-27/04-database-review.md:273:### 8. attachments表缺少file_hash字段
backend/apps/approvals/models.py:19:    application = models.ForeignKey(Application, on_delete=models.PROTECT, related_name='approvals')
backend/apps/approvals/models.py:21:    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approvals')
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:127:- 记录需要extend_schema的端点
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:23:**位置：** `backend/apps/attachments/views.py:17-28`
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:29:def attachments_view(request, application_id):
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:30:    """Dispatcher for attachment list (GET) and upload (POST)"""
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:32:        return list_attachments(request, application_id)
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:34:        return upload_attachment(request, application_id)
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:38:def upload_attachment(request, application_id):
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:44:1. `attachments_view()` 是DRF的实际入口点（带 `@api_view` 装饰器）
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:45:2. `@parser_classes([MultiPartParser, FormParser])` 装饰在 `upload_attachment()` 辅助函数上
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:46:3. DRF只在视图函数（`attachments_view`）上处理装饰器
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:49:6. `upload_attachment()` 的装饰器永远不会生效
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:66:**修改文件：** `backend/apps/attachments/views.py`
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:73:def attachments_view(request, application_id):
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:74:    """Dispatcher for attachment list (GET) and upload (POST)"""
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:76:        return list_attachments(request, application_id)
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:78:        return upload_attachment(request, application_id)
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:82:def upload_attachment(request, application_id):
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:123:- `attachment-error`
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:124:- `empty-attachments`
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:125:- `attachment-list`
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:126:- `attachment-item`
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:127:- `attachment-info`
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:128:- `attachment-actions`
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:140:**文件：** `backend/apps/attachments/views.py`
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:141:- 将 `@parser_classes([MultiPartParser, FormParser])` 从 `upload_attachment()` 移到 `attachments_view()`
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:148:  apps.attachments.tests.test_upload \
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:149:  apps.attachments.tests.test_list \
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:150:  apps.attachments.tests.test_download \
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:151:  apps.attachments.tests.test_delete \
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:14:- ✅ Phase 2 partial: detail.ts (attachment methods), detail.wxml (attachment UI markup)
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:40:  attachment_id: string;
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:41:  attachment_type: AttachmentType;
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:50:  attachments: Attachment[];
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:64:- `uploadAttachment(applicationId, filePath, attachmentType)`: 上传附件（使用wx.uploadFile）
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:65:- `deleteAttachment(attachmentId)`: 删除附件
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:66:- `getDownloadUrl(attachmentId)`: 获取下载URL
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:72:  url: `${this.config.baseUrl}/api/applications/${applicationId}/attachments/`,
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:75:  formData: { attachment_type: attachmentType },
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:95:attachments: [] as Attachment[],
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:97:attachmentError: '',
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:105:- `uploadFile(filePath, attachmentType)`: 上传文件
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:107:- `deleteAttachment(attachmentId)`: 执行删除
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:108:- `onDownloadAttachment(e)`: 下载附件（wx.downloadFile + wx.previewImage/wx.openDocument）
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:125:if (attachment.content_type.includes('image')) {
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:146:  <view class="attachment-list" wx:if="{{attachments.length > 0}}">
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:147:    <view class="attachment-item" wx:for="{{attachments}}" wx:key="attachment_id">
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:148:      <view class="attachment-info">
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:152:      <view class="attachment-actions">
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:153:        <button class="btn-small download" bindtap="onDownloadAttachment" data-attachment="{{item}}">下载</button>
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:154:        <button class="btn-small delete" wx:if="{{isOwner}}" bindtap="onDeleteAttachment" data-id="{{item.attachment_id}}">删除</button>
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:158:  <view class="empty-attachments" wx:if="{{attachments.length === 0}}">
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:164:  <view class="attachment-error" wx:if="{{attachmentError}}">
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:165:    <text>{{attachmentError}}</text>
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:171:- WXML绑定是否正确？（data-attachment vs data-id）
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:275:wx.downloadFile({
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:281:      if (attachment.content_type.includes('image')) {
backend/apps/applications/migrations/0002_initial.py:21:            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='applications', to=settings.AUTH_USER_MODEL),
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:16:当前工作树中P0列表响应形状已经修复：`backend/apps/attachments/views.py` 返回 `{attachments: serializer.data}`，后端列表测试也已按该形状断言。以下审查只聚焦P1方案。
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:26:- `backend/apps/attachments/serializers.py:23-27`
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:27:- `backend/apps/attachments/models.py:13-24`
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:35:attachment_id, file_name, file_size, content_type, attachment_type, uploaded_at
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:57:`formatApiError` 已存在，`attachmentError` 已在 `data` 中定义，WXML也已有错误展示节点。
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:60:当前WXML的空状态和错误状态不是互斥关系：`attachments.length === 0` 时会显示“暂无附件”，即使同时存在 `attachmentError`。请求文档中的 `wx:if / wx:elif / wx:else` 方向正确，但执行时必须替换现有附件区域的条件结构，而不是只追加错误节点。
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:63:`loadAttachments()` 成功时设置 `{ attachments, attachmentError: '' }`。失败时设置错误状态，并建议清空列表或让错误状态优先于列表：
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:68:    const attachments = await apiClient.listAttachments(this.data.applicationId);
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:69:    this.setData({ attachments, attachmentError: '' });
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:73:      attachments: [],
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:74:      attachmentError: formatApiError(err) || '附件加载失败',
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:81:1. `attachmentError`
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:82:2. `attachments.length === 0`
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:112:- `backend/apps/attachments/serializers.py:9-20`
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:140:- Serializer字段：`attachment_id`、`file_name`、`file_size`、`content_type`、`attachment_type`、`uploaded_at`。
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:149:- `attachmentError` 已存在，应在附件加载成功时清空、失败时设置。
docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md:154:下载路径必须补401/403/404。由于 `wx.downloadFile` 没有走 `ApiClient.request()`，当前全局401处理不会自动触发。建议将下载封装进 `ApiClient`，或暴露统一未授权处理函数。
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:20:- `backend/apps/attachments/views.py:81-84`
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:27:{ "attachments": [...] }
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:30:但当前后端 `list_attachments()` 返回的是裸数组：
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:36:结果是 `response.attachments` 为 `undefined`，前端会走 `response.attachments || []`，即使后端有附件也显示空列表。
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:44:return Response({'attachments': serializer.data})
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:53:- `backend/apps/attachments/serializers.py:23-27`
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:60:attachment_id, file_name, file_size, content_type, attachment_type, uploaded_at
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:82:设置 `attachmentError`，并区分“暂无附件”和“附件加载失败”。401仍交给 `ApiClient.onUnauthorized`；其他错误至少显示 `formatApiError(err)` 或 `err.error?.message || '附件加载失败'`。
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:89:`wx.downloadFile` 对非200统一显示“下载失败”。如果token过期返回401，当前不会执行 `onUnauthorized`，用户停留在详情页且无法恢复。
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:92:将下载封装进 `ApiClient.downloadAttachment()` 或至少在页面中对状态码分支处理：
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:152:`data-id` 删除绑定是正确的。`data-attachment="{{item}}"` 通常可用，但为降低调试成本，下载也可以改为 `data-id` 后从 `this.data.attachments` 查找对象，这样不会依赖dataset对象传递行为。
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:159:- `.attachment-list` 使用纵向列表。
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:160:- `.attachment-item` 使用 `display:flex; justify-content:space-between; align-items:center;`，必要时允许换行。
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:161:- `.attachment-info` 使用 `flex:1; min-width:0;`，文件名用省略或换行策略，避免长文件名挤压按钮。
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:162:- `.attachment-actions` 使用横向按钮组，按钮固定最小宽度。
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:163:- `.btn-small.download` 使用现有蓝色系，`.btn-small.delete` 使用红色系。
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:165:- `.attachment-error` 使用轻量红色文本，不要用弹窗式重视觉。
docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md:183:- Upload：使用 `wx.uploadFile`、`name: 'file'`、`formData.attachment_type`、Authorization header、4xx/5xx手动reject。
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:52:    const attachments = await apiClient.listAttachments(this.data.applicationId);
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:53:    this.setData({ attachments, attachmentError: '' });
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:57:      attachments: [],
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:58:      attachmentError: formatApiError(err) || '附件加载失败',
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:101:  const attachment = e.currentTarget.dataset.attachment as Attachment;
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:102:  const url = apiClient.getDownloadUrl(attachment.attachment_id);
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:105:  wx.downloadFile({
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:123:        if (attachment.content_type.startsWith('image/')) {
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:225:- 修改 `loadAttachments()` 失败时清空 `attachments` 数组
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:253:**命令：** `docker compose exec -T backend python manage.py test apps.attachments.tests.test_list -v 2`
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:29:- `POST /api/applications/{application_id}/attachments/`
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:30:- `GET /api/applications/{application_id}/attachments/`
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:31:- `GET /api/attachments/{attachment_id}/download/`
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:32:- `DELETE /api/attachments/{attachment_id}/`
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:55:    """Check if user can view application and its attachments."""
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:90:    return FileResponse(attachment.file.open('rb'), ...)
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:134:- Risk is low for MVP (< 1000 attachments expected)
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:140:- Attachment IDs use 8-char hex suffix (collision risk ~0.01% at 10K attachments)
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:193:2. Update attachment views to use helper (10 min)
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:197:6. Create `attachments/urls.py` + include in project URLs (10 min)
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:206:- Download: positive + forbidden + soft-deleted (20 min)
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:211:- Run attachment tests (5 min)
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:12:Do not wait idle for WeChat DevTools. Phase 4C backend is now implemented and tested, and attachment endpoints are concrete enough for frontend integration work. However, the next frontend step should be treated as **Phase 4C frontend code-complete**, not Phase 4C fully complete, because DevTools remains the first real miniprogram compile/runtime gate.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:16:1. Add attachment API types and client methods.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:17:2. Add read-only attachment list/download/delete UI on the detail page.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:28:**Rework risk: medium.** The risk is not the backend contract anymore; the backend has concrete attachment endpoints and tests. The risk is miniprogram runtime behavior because this repo has no local `package.json`, no `tsconfig.json`, and no CLI build/test harness for the miniprogram. DevTools is therefore the practical compiler and runtime verifier.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:30:**Technical risk: medium.** `wx.uploadFile` is not just `wx.request` with a file. The client must handle multipart upload separately: pass `filePath`, use `name: 'file'`, send `attachment_type` via `formData`, include `Authorization`, parse `res.data` manually because upload responses commonly arrive as strings, and treat HTTP 4xx/5xx status codes as failures even when the transport callback succeeds. Download should use `wx.downloadFile` plus `wx.openDocument` for PDF/DOC/DOCX and image preview for JPG/PNG.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:42:**Time risk: high.** The 4-6 hour estimate is likely optimistic if it includes multiple user flows and polish. It also delays the attachment closure that Phase 4C is supposed to deliver.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:44:**Verdict:** defer. Pull only the part that Option A needs: improve the existing detail page enough to show attachments.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:52:**Time risk: high.** The wait is externally blocked and could cost 1-3 days with little product progress. This is not justified now because backend attachment endpoints are stable enough to integrate against.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:58:Proceed with **Option A-lite: attachment frontend integration on the existing pages**, with a hard boundary around what is allowed before DevTools.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:65:   - `deleteAttachment(attachmentId)`
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:66:   - `downloadAttachment(attachmentId)` or a helper returning the download URL/header plan
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:67:   - `uploadAttachment(applicationId, filePath, attachmentType)` using `wx.uploadFile`, not the generic `request()`
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:68:3. Update `miniprogram/pages/detail/detail.*` to load and display attachments for all users who can view the application.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:69:4. Add delete affordance only for the owning student where possible; still rely on backend RBAC.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:72:   - upload after submit is safer: submit application, redirect to detail, upload attachments there.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:74:That last point is important: the request says "学生申请页面：附件上传组件", but the current backend attachment API attaches files to an existing `application_id`. Unless the frontend first creates the application, there is nothing to upload against. For MVP, the lower-risk UX is **submit first, then upload attachments on detail page**. If the upload must appear on the application page, implement it as a post-submit step or pending-file queue, not as a real upload before application creation.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:78:### 1. Make the detail page the attachment hub
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:80:The existing detail page already has `applicationId` and loads `ApplicationDetail`. It is the natural place to list, download, and delete attachments. This avoids inventing draft attachment behavior.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:88:- `attachmentError`
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:89:- `attachments`
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:95:Do not force upload/download through the existing `request<T>()` wrapper. Add dedicated methods because `wx.uploadFile` and `wx.downloadFile` have different response shapes from `wx.request`.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:99:`project.config.json` currently has `urlCheck: false`, which helps local DevTools testing. Real device and production testing still need configured HTTPS request/upload/download domains. Do not let a DevTools-local pass imply production network readiness.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:106:- Detail page can list attachments.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:108:- Student owner can delete.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:109:- Viewers can download/open.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:118:- Student cannot delete someone else's attachment.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:119:- Counselor/dean can view/download according to backend RBAC.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:130:- Do not start broad history pages or new approval-detail pages until the attachment detail-page pattern has been validated.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:134:**Option D: attachment adapter + detail read-only first, upload second.**
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:138:1. Add attachment types and list/download client methods.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:139:2. Add detail-page attachment list and download/open behavior.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:141:4. Add upload/delete after list/download compiles.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:151:- detail page attachment list/download/delete;
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:153:- dedicated `wx.uploadFile`/`wx.downloadFile` API methods;
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:39:**接受：** 采用"显式重置开关"方案（`SMOKE_RESET=1`）。
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:78:- Step 1.0（smoke重置策略）：1-1.5小时（实现SMOKE_RESET=1）
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:89:**任务1.0.1: 实现SMOKE_RESET开关（45分钟）**
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:90:- 在smoke_test.sh头部检查SMOKE_RESET环境变量
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:100:- 说明SMOKE_RESET=1用法
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:105:- 验证SMOKE_RESET=1可以清理环境
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:128:- `/api/schema/`可访问
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:135:- 记录需要extend_schema的端点
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:155:1. SMOKE_RESET=1可以清理环境并重新初始化
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:156:2. 未设置SMOKE_RESET时给出前置条件提示
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:166:1. `/api/schema/`可访问
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:184:> 下一步执行Option E-lite。先实现smoke可重复运行门禁（SMOKE_RESET=1），再增强通知字段和审批驳回路径；随后引入drf-spectacular作为OpenAPI基线，只验收schema可访问、端点清单和认证可见，并记录待完善项；最后补部署文档的环境变量表、smoke前置条件和故障排查。不承诺完整API schema，不无条件自动重置数据库。
docs/discussions/phase4c-next-steps/43-claude-post-phase2a-stabilization-next-strategy.md:62:- 记录需要extend_schema的端点
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:180:   - 缺少：`idx_approver_status`、`idx_student_status`、`idx_status_deleted`、`idx_app_time`、`idx_app_type`、`idx_user_read_time`、审计日志复合索引
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:87:2. 后续：补`extend_schema`注解、错误码schema、文件上传schema、示例响应。
docs/design/2026-05-27-system-design.md:157:│   ├── attachments/       # 附件管理模块
docs/design/2026-05-27-system-design.md:207:4. **attachments（附件管理）**
docs/design/2026-05-27-system-design.md:249:4. attachments - 附件表
docs/design/2026-05-27-system-design.md:284:    is_deleted BOOLEAN DEFAULT FALSE COMMENT '是否删除',
docs/design/2026-05-27-system-design.md:302:- `is_deleted`: 软删除标记
docs/design/2026-05-27-system-design.md:331:    is_deleted BOOLEAN DEFAULT FALSE,
docs/design/2026-05-27-system-design.md:348:    INDEX idx_status_deleted (status, is_deleted, submit_time)
docs/design/2026-05-27-system-design.md:392:### 2.5 附件表（attachments）
docs/design/2026-05-27-system-design.md:395:CREATE TABLE attachments (
docs/design/2026-05-27-system-design.md:403:    attachment_type VARCHAR(50) NOT NULL COMMENT '附件类型',
docs/design/2026-05-27-system-design.md:405:    is_deleted BOOLEAN DEFAULT FALSE,
docs/design/2026-05-27-system-design.md:409:    INDEX idx_attachment_type (attachment_type),
docs/design/2026-05-27-system-design.md:411:    INDEX idx_app_type (application_id, attachment_type, is_deleted)
docs/design/2026-05-27-system-design.md:415:**附件类型（attachment_type）：**
docs/design/2026-05-27-system-design.md:546:- `upload_attachment` - 上传附件
docs/design/2026-05-27-system-design.md:547:- `delete_attachment` - 删除附件
docs/design/2026-05-27-system-design.md:554:- `attachment` - 附件
docs/design/2026-05-27-system-design.md:602:  ├─1:N─→ attachments (一个申请多个附件)
docs/design/2026-05-27-system-design.md:611:attachments (附件表)
docs/design/2026-05-27-system-design.md:920:    "attachments": [
docs/design/2026-05-27-system-design.md:924:        "attachment_type": "dorm_clearance"
docs/design/2026-05-27-system-design.md:1066:POST /api/v1/applications/{id}/attachments
docs/design/2026-05-27-system-design.md:1072:- attachment_type: dorm_clearance
docs/design/2026-05-27-system-design.md:1083:    "attachment_type": "dorm_clearance",
docs/design/2026-05-27-system-design.md:1120:GET /api/v1/attachments/{id}/download
docs/design/2026-05-27-system-design.md:1128:DELETE /api/v1/attachments/{id}
docs/design/2026-05-27-system-design.md:1510:        is_deleted=False
docs/design/2026-05-27-system-design.md:1895:find /data/backups -name "db_*.sql" -mtime +30 -delete
docs/design/2026-05-27-system-design.md:1896:find /data/backups -name "uploads_*.tar.gz" -mtime +30 -delete
docs/design/2026-05-27-system-design.md:2108:        location /api/v1/applications/*/attachments {
docs/design/2026-05-27-system-design.md:2188:        is_deleted=False
docs/design/2026-05-27-system-design.md:2206:def handle_file_upload(file, application_id, attachment_type):
docs/design/2026-05-27-system-design.md:2273:    AuditLog.objects.filter(created_at__lt=cutoff_date).delete()
docs/design/2026-05-27-system-design.md:2354:CREATE INDEX idx_status_deleted ON applications(status, is_deleted, submit_time);
docs/design/2026-05-27-system-design.md:2362:-- attachments表索引
docs/design/2026-05-27-system-design.md:2363:CREATE INDEX idx_application_id ON attachments(application_id);
docs/design/2026-05-27-system-design.md:2364:CREATE INDEX idx_attachment_type ON attachments(attachment_type);
docs/design/2026-05-27-system-design.md:2365:CREATE INDEX idx_file_hash ON attachments(file_hash);
docs/design/2026-05-27-system-design.md:2366:CREATE INDEX idx_app_type ON attachments(application_id, attachment_type, is_deleted);
docs/design/2026-05-27-system-design.md:2388:- `idx_status_deleted`: 按状态筛选未删除申请
docs/design/2026-05-27-system-design.md:2455:    cache.delete(f'app:{application_id}:status')
docs/design/2026-05-27-system-design.md:2456:    cache.delete(f'app:{application_id}:detail')
docs/design/2026-05-27-system-design.md:2461:        cache.delete(f'pending:count:{app.current_approver_id}')
docs/design/2026-05-27-system-design.md:2464:    cache.delete(f'student:{app.student_id}:applications')
docs/design/2026-05-27-system-design.md:2468:    cache.delete(f'user:{user_id}')
docs/design/2026-05-27-system-design.md:2469:    cache.delete(f'user:{user_id}:permissions')
docs/design/2026-05-27-system-design.md:2504:def upload_to_storage(file_path, attachment_id):
docs/design/2026-05-27-system-design.md:2665:    response = client.post(f'/api/v1/applications/{app_id}/attachments', files={'file': fake_image})
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:14:The frontend P1 fixes for attachment field narrowing, `loadAttachments()` error state, WXML mutually exclusive rendering, download status handling, and file extension precheck are broadly implemented as planned.
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:16:However, the current tree does **not** satisfy the summary's backend completion claim. The full attachment backend suite reports 3 upload failures with `415 Unsupported Media Type`, so Contract v0.3 cannot be treated as "Backend complete / 19 tests passing" yet.
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:24:**Location:** `backend/apps/attachments/views.py:17-28`, `backend/config/settings/base.py:121-123`
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:29:python manage.py test apps.attachments.tests.test_upload apps.attachments.tests.test_list apps.attachments.tests.test_download apps.attachments.tests.test_delete -v 2
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:40:`attachments_view` is the actual DRF entrypoint for both GET and POST. The multipart parser decorator is attached to `upload_attachment`, but `upload_attachment` is only called as a plain helper after DRF has already constructed/parsing the request through `attachments_view`.
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:46:Apply `@parser_classes([MultiPartParser, FormParser])` to the DRF entrypoint, or split the upload/list handlers into separately decorated DRF views routed by method/path. After the fix, rerun the 19 explicit attachment tests.
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:68:### P2: New attachment UI has no local WXSS coverage yet
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:74:The new attachment elements use classes such as `attachment-error`, `empty-attachments`, `attachment-list`, `attachment-item`, `attachment-info`, `attachment-actions`, `btn-small`, and `btn-upload`, but `detail.wxss` does not define them.
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:84:- `miniprogram/types/api.ts` `Attachment` now matches backend serializer fields: `attachment_id`, `attachment_type`, `file_name`, `file_size`, `content_type`, `uploaded_at`.
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:86:- `miniprogram/pages/detail/detail.ts` `loadAttachments()` clears `attachmentError` on success and sets an explicit error state on failure.
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:87:- `miniprogram/pages/detail/detail.wxml` renders attachment error, empty state, and list as mutually exclusive branches.
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:96:rtk docker compose exec -T backend python manage.py test apps.attachments.tests.test_list -v 2
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:102:rtk docker compose exec -T backend python manage.py test apps.attachments.tests.test_upload apps.attachments.tests.test_list apps.attachments.tests.test_download apps.attachments.tests.test_delete -v 2
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:110:rtk docker compose exec -T backend python manage.py test apps.attachments.tests -v 2
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:113:This label fails during Django discovery with `TypeError: expected str, bytes or os.PathLike object, not NoneType`, so explicit test modules should be used for the attachment suite in this environment.
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:122:2. The explicit 19-test attachment suite passes.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:13:1. The attachment implementation has P0 consistency gaps that should be fixed before writing most tests.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:22:`backend/apps/attachments/urls.py` is empty and `backend/config/urls.py` does not include the attachments app. Before adding paths, decide the public shape:
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:24:- `POST /api/applications/{application_id}/attachments/`
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:25:- `GET /api/applications/{application_id}/attachments/`
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:26:- `GET /api/attachments/{attachment_id}/download/`
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:27:- `DELETE /api/attachments/{attachment_id}/`
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:33:Attachment list/download currently use rules that differ from `get_application`:
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:37:- Dean attachment access allows any matching dean approval.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:40:This needs a deliberate decision. My recommendation: extract a shared helper for "can view application detail/attachments" or explicitly document that attachments have broader historical visibility. Do not let this remain implicit.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:44:`download_attachment` opens `attachment.file` directly. If the database row exists but the file is absent from storage, the API can return a server error. For MVP, return `404 FILE_NOT_FOUND` or the existing `NOT_FOUND` envelope. Add a test using deleted/missing file storage if practical; at minimum handle the exception.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:48:`AttachmentUploadSerializer` has specific file size and extension errors, but `upload_attachment` returns only:
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:76:- Download: one positive plus one forbidden plus soft-deleted returns 404.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:77:- Delete: owner student soft-deletes; non-owner student and staff are forbidden; list/download exclude deleted attachments.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:92:- After attachment tests: targeted attachment test module.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:99:Do not start attachment UI immediately after backend code compiles. First require:
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:102:- attachment API smoke evidence,
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:106:After that, frontend can start with API client/types and a minimal detail-page attachment section. Full DevTools verification remains the completion gate.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:112:- duplicate RBAC logic in list/download;
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:116:- no explicit handling of already-deleted attachment on DELETE;
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:117:- download response does not set an explicit content type from stored metadata;
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:118:- no query optimization concern for N+1 here, because endpoints are per application/attachment, but shared helper logic matters more than query count.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:124:   - Pin who can view/download attachments.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:128:   - Fill `attachments/urls.py`.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:129:   - Include attachments routes in project URLs.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:134:3. **Focused attachment tests (75-90 min)**
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:139:   - Run focused attachment tests first.
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:11:Codex识别了我原始Option A中的关键技术约束：后端attachment API需要已存在的`application_id`，因此无法在申请提交前上传附件。这是一个我忽略的实际约束。
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:19:- 问题：后端API `POST /api/applications/{application_id}/attachments/` 需要已存在的application_id
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:31:   - `deleteAttachment(attachmentId)`
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:32:   - `downloadAttachment(attachmentId)` 或返回下载URL的helper
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:33:   - `uploadAttachment(applicationId, filePath, attachmentType)` 使用`wx.uploadFile`
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:73:- 添加`uploadAttachment(applicationId, filePath, attachmentType)`方法（使用`wx.uploadFile`）
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:74:- 添加`deleteAttachment(attachmentId)`方法
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:75:- 添加`downloadAttachment(attachmentId)`方法或helper
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:80:- 添加attachments数据字段
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:84:- 添加`onDeleteAttachment(attachmentId)`方法
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:85:- 添加`onDownloadAttachment(attachmentId)`方法
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:126:- 通过`formData`发送`attachment_type`
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:131:### wx.downloadFile + 文件打开
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:142:- `attachmentError: string`
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:143:- `attachments: Attachment[]`
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:152:- **技术风险：中等** - `wx.uploadFile`/`wx.downloadFile`有特殊处理要求
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:40:    const attachments = await apiClient.listAttachments(this.data.applicationId);
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:41:    this.setData({ attachments });
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:52:    const attachments = await apiClient.listAttachments(this.data.applicationId);
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:53:    this.setData({ attachments, attachmentError: '' });
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:57:      attachments: [],
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:58:      attachmentError: formatApiError(err) || '附件加载失败',
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:70:<view class="attachment-error" wx:if="{{attachmentError}}">
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:71:  <text>{{attachmentError}}</text>
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:73:<view class="empty-attachments" wx:elif="{{attachments.length === 0}}">
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:76:<view class="attachment-list" wx:else>
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:163:**命令：** `docker compose exec -T backend python manage.py test apps.attachments.tests.test_list -v 2`
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:173:- `test_list_excludes_soft_deleted` ✅
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:200:# backend/apps/attachments/serializers.py
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:201:attachment_id, file_name, file_size, content_type, attachment_type, uploaded_at
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:207:attachment_id, attachment_type, file_name, file_size, content_type, uploaded_at
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:213:attachment_id, attachment_type, file_name, file_size, content_type, uploaded_at
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:75:- 测试覆盖良好（applications/approvals/attachments/notifications）
docs/discussions/phase4c-next-steps/05-claude-next-steps-strategy-request.md:11:- 19个attachment测试100%通过
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:32:  attachment_id: string;
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:33:  attachment_type: AttachmentType;
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:57:    const attachments = await apiClient.listAttachments(this.data.applicationId);
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:58:    this.setData({ attachments, attachmentError: '' });
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:62:    this.setData({ attachmentError: errorMsg });
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:69:2. `attachmentError` 字段是否已在 `data` 中定义？
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:70:3. WXML是否已有显示 `attachmentError` 的逻辑？
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:76:<view wx:if="{{attachmentError}}" class="error-message">{{attachmentError}}</view>
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:77:<view wx:elif="{{attachments.length === 0}}" class="empty-message">暂无附件</view>
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:92:  const attachment = e.currentTarget.dataset.attachment as Attachment;
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:93:  const url = apiClient.getDownloadUrl(attachment.attachment_id);
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:96:  wx.downloadFile({
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:119:        if (attachment.content_type.startsWith('image/')) {
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:203:- `backend/apps/attachments/serializers.py`
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:204:- `backend/apps/attachments/views.py` (upload_attachment)
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:218:- `attachmentError` 字段是否已在 `data` 中定义？
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:219:- 是否需要在其他生命周期方法中重置 `attachmentError`？
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:259:- `backend/apps/attachments/serializers.py`
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:260:- `backend/apps/attachments/views.py`
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:14:The P0 multipart parser bug is fixed correctly. The parser configuration is now attached to the actual DRF entrypoint, and the explicit attachment backend suite passes.
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:28:The attachment markup has classes for error, empty, list, item, actions, small buttons, and upload button. `detail.wxss` still has no corresponding attachment-specific styles. This matches the planned Step 6 and is not a backend or contract blocker.
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:34:1. **P0 parser bug fix correctness:** Yes. `@parser_classes([MultiPartParser, FormParser])` is now on `attachments_view()`, which is the DRF `@api_view` entrypoint. Removing it from the plain helper `upload_attachment()` is correct.
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:36:2. **19/19 tests and backend completeness:** Yes for the attachment backend MVP scope. Upload, list, download, delete, RBAC, validation details, soft delete behavior, and missing-file handling are covered by the explicit attachment tests.
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:40:4. **Other missed issues:** No new backend blockers found. The remaining gap is frontend presentation/validation, not attachment backend correctness.
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:48:  apps.attachments.tests.test_upload \
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:49:  apps.attachments.tests.test_list \
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:50:  apps.attachments.tests.test_download \
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:51:  apps.attachments.tests.test_delete \
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:64:- `backend/apps/attachments/views.py`: parser decorator is on `attachments_view()`.
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:65:- `backend/apps/attachments/views.py`: list response returns `{ "attachments": [...] }`.
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:67:- `miniprogram/types/api.ts` and `miniprogram/services/api.ts`: attachment response shape and field names align with the backend serializer.
docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:18:> 下一步执行Option E-lite。先实现smoke可重复运行门禁（SMOKE_RESET=1），再增强通知字段和审批驳回路径；随后引入drf-spectacular作为OpenAPI基线，只验收schema可访问、端点清单和认证可见，并记录待完善项；最后补部署文档的环境变量表、smoke前置条件和故障排查。不承诺完整API schema，不无条件自动重置数据库。
docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:25:   - 实现SMOKE_RESET=1显式重置开关
docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:39:- 任务1.0.1: 实现SMOKE_RESET开关（45分钟）
docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:61:1. SMOKE_RESET=1可以清理环境并重新初始化
docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:62:2. 未设置SMOKE_RESET时给出前置条件提示
docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:72:1. `/api/schema/`可访问
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:25:### 8. attachments表缺少file_hash - **同意**
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:69:    application = models.ForeignKey(Application, on_delete=models.CASCADE)
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:72:    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:103:    old_logs.delete()
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:173:8. ✅ attachments添加file_hash
backend/apps/applications/tests/test_p0_fixes.py:11:class ResubmissionAfterRejectionTest(TestCase):
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:27:- `tests/smoke_test.sh` 已加入 `SMOKE_RESET=1` 显式重置路径。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:28:- smoke 覆盖 H1 happy path、H2 counselor reject、N2 cross-counselor 403。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:29:- attachment 路径已使用 `/api/attachments/{id}/download/` 和 `/api/attachments/{id}/`。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:34:- 46 号共识中的验收项写了“通知断言按本次实体过滤，不受旧数据干扰”。当前 smoke 主要通过 message 内容过滤通知，例如包含 `2020001`、`辅导员`、`材料不齐全`，不是通过当前 `approval_id` 或 `application_id` 过滤。由于推荐运行方式是 `SMOKE_RESET=1`，这不是本轮阻塞项，但应避免在总结中声称已经完全实现“按实体 id 过滤”。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:41:- `/api/schema/` 返回 HTTP 200。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:42:- `/api/schema/swagger-ui/` 返回 HTTP 200。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:45:- `docs/api/api-schema-todo.md` 已记录 function-based views、operationId 冲突、错误 envelope、文件上传/下载、分页、示例等缺口。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:49:- 47 号文档和 `docs/api/api-schema-todo.md` 写“15 个端点”。我实际从 `/api/schema/` 看到的是 **13 个 path，15 个 operation**。建议统一表述为“13 条 path / 15 个 HTTP operation”，避免后续验收误解。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:63:不建议现在启动 Option B。`extend_schema`、统一错误响应 schema、文件上传/下载 schema 都有价值，但它们属于下一轮 API 文档完善任务，不应该挤进 Option E-lite。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:97:- smoke 未重置导致重复申请：表现为 409，处理方式是 `SMOKE_RESET=1 ./tests/smoke_test.sh` 或手动清理测试数据。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:101:- media/attachment 问题：上传扩展名、下载路径、容器 volume、文件权限。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:121:- API Schema P1 完善：`extend_schema`、operationId、错误响应结构。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:131:- `curl /api/schema/`：HTTP 200
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:132:- `curl /api/schema/swagger-ui/`：HTTP 200
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:135:- backend logs：13 个 function-based view serializer 推断警告、1 个 operationId 冲突，均已属于待完善清单范围
backend/apps/users/migrations/0001_initial.py:48:                ('counselor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='managed_classes', to=settings.AUTH_USER_MODEL)),
backend/apps/applications/permissions.py:7:    """Check if user can view application and its attachments."""
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:15:1. ✓ SMOKE_RESET=1环境重置开关
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:17:3. ✓ 添加H2审批驳回场景
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:18:4. ✓ 修复attachment文件类型（.txt → .pdf）
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:19:5. ✓ 修复attachment URL（download/delete路径错误）
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:23:- H2 Rejection Path: ✓ 通过
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:36:- /api/schema/: HTTP 200 ✓
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:37:- /api/schema/swagger-ui/: HTTP 200 ✓
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:40:- 生成器警告已记录（13个function-based views需extend_schema）✓
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:43:- P1: 13个function-based views需要extend_schema装饰器
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:44:- P1: operationId冲突需要修复
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:79:- 为关键端点添加extend_schema装饰器
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:80:- 修复operationId冲突
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:103:- 验证SMOKE_RESET=1的可靠性
backend/apps/applications/models.py:23:    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='applications')
backend/apps/users/class_mapping.py:7:    counselor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='managed_classes')
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:14:- 装饰在辅助函数 `upload_attachment()` 上
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:15:- 应该装饰在DRF入口点 `attachments_view()` 上
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:23:**文件：** `backend/apps/attachments/views.py`
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:29:def attachments_view(request, application_id):
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:33:def upload_attachment(request, application_id):
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:42:def attachments_view(request, application_id):
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:45:def upload_attachment(request, application_id):  # 移除装饰器
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:49:**修改内容：** 将 `@parser_classes` 装饰器从 `upload_attachment()` 移到 `attachments_view()`
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:58:  apps.attachments.tests.test_upload \
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:59:  apps.attachments.tests.test_list \
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:60:  apps.attachments.tests.test_download \
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:61:  apps.attachments.tests.test_delete \
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:87:- 添加测试覆盖详情：upload (5), list (6), download (4), delete (4)
docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:10:- Attachment模型 (soft delete + 4类型 + FileField)
docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:13:- 4个视图函数 (upload/list/download/delete with RBAC)
docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:17:2. Migrations (创建attachments表)
docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:18:3. 后端测试 (upload/permissions/soft delete)
docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:88:   - 如果时间允许：文件大小/扩展名验证、download权限
docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:102:1. **FileField路径:** `upload_to='attachments/%Y/%m/%d/'` 可能导致路径过深，是否需要简化？
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:74:   支持类似`SMOKE_RESET=1 ./tests/smoke_test.sh`，只有显式设置时才执行破坏性重置，避免误删开发数据。
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:94:**位置：** `docs/discussions/phase4c-next-steps/43-claude-post-phase2a-stabilization-next-strategy.md:49-64`、`backend/config/settings/base.py:18-38`、`backend/config/settings/base.py:112-124`、`backend/apps/attachments/views.py:17-20`
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:100:- `/api/schema/`可访问。
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:102:- auth、applications、approvals、attachments、notifications端点出现在schema中。
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:147:Smoke增强0.5-1小时可接受，但前提是只做文档式前置条件。如果实现`SMOKE_RESET=1`，应估为1-1.5小时。
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:149:API文档基线1-2小时只适合"可访问schema + 端点清单 + 缺口清单"。如果要让主要请求/响应对象都可读且准确，至少应估2-4小时，并且可能需要多处`extend_schema`。
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:21:后端 `list_attachments()` 返回：
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:29:return response.attachments || [];  // 期望 {attachments: [...]}
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:32:结果：`response.attachments` 为 `undefined`，UI永远显示空列表。
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:44:**修复位置：** `backend/apps/attachments/views.py:84`
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:52:return Response({'attachments': serializer.data})
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:55:**同步修复：** `backend/apps/attachments/tests/test_list.py` 所有list测试的断言
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:83:    const attachments = await apiClient.listAttachments(this.data.applicationId);
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:84:    this.setData({ attachments, attachmentError: '' });
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:88:    this.setData({ attachmentError: errorMsg });
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:94:- `attachments.length === 0 && !attachmentError`：显示"暂无附件"
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:95:- `attachmentError`：显示错误信息
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:104:  const attachment = e.currentTarget.dataset.attachment as Attachment;
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:105:  const url = apiClient.getDownloadUrl(attachment.attachment_id);
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:108:  wx.downloadFile({
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:131:        if (attachment.content_type.startsWith('image/')) {
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:208:**文件：** `backend/apps/attachments/views.py`
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:209:- 修改 `list_attachments()` 返回形状
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:211:**文件：** `backend/apps/attachments/tests/test_list.py`
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:214:**验证：** 运行 `pytest backend/apps/attachments/tests/test_list.py -v`
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:19:Proceed with that order, but do not leave the attachment ID length as an MVP limitation, and do not only add the shared permission helper for attachments.
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:28:attachment_id=f'att_{uuid.uuid4().hex[:8]}'
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:34:attachment_id=f'att_{uuid.uuid4().hex[:12]}'
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:40:- `Attachment.attachment_id` already allows `max_length=50`, so no migration is needed.
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:48:I agree with extracting `can_view_application(user, application)`, but it should not be attachment-only cleanup.
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:53:- `backend/apps/attachments/views.py::list_attachments`
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:54:- `backend/apps/attachments/views.py::download_attachment`
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:81:This must include `ApprovalDecision.PENDING` for dean access, matching current application detail behavior. A dean with historical non-pending approval should not gain attachment visibility unless Contract v0.3 deliberately changes the application-detail contract too.
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:89:- `POST /api/applications/{application_id}/attachments/`
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:90:- `GET /api/applications/{application_id}/attachments/`
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:91:- `GET /api/attachments/{attachment_id}/download/`
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:92:- `DELETE /api/attachments/{attachment_id}/`
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:97:- shared view/download RBAC semantics
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:98:- upload/delete limited to owning student
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:99:- soft-deleted attachment behavior as `404 NOT_FOUND`
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:106:- add attachment routing
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:110:- handle missing file storage on download
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:111:- set download content type from `attachment.content_type` when returning `FileResponse`
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:112:- treat already-deleted attachment on `DELETE` as not found or idempotent `204`, but document and test whichever behavior is chosen
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:114:My preference: already-deleted `DELETE` returns `404 NOT_FOUND`, because list/download already hide deleted attachments and the API treats soft-deleted rows as absent.
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:118:Approved. Add one explicit regression test proving application detail and attachment visibility agree for:
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:131:1. Change attachment IDs to 12-char UUID suffixes now.
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:132:2. Extract `can_view_application` and use it in both application detail and attachment view/download paths.
backend/apps/users/management/commands/seed_data.py:21:            Approval.objects.all().delete()
backend/apps/users/management/commands/seed_data.py:22:            Application.objects.all().delete()
backend/apps/attachments/urls.py:5:    path('applications/<str:application_id>/attachments/', views.attachments_view, name='attachments'),
backend/apps/attachments/urls.py:6:    path('attachments/<str:attachment_id>/download/', views.download_attachment, name='download_attachment'),
backend/apps/attachments/urls.py:7:    path('attachments/<str:attachment_id>/', views.delete_attachment, name='delete_attachment'),
backend/apps/attachments/views.py:20:def attachments_view(request, application_id):
backend/apps/attachments/views.py:21:    """Dispatcher for attachment list (GET) and upload (POST)"""
backend/apps/attachments/views.py:23:        return list_attachments(request, application_id)
backend/apps/attachments/views.py:25:        return upload_attachment(request, application_id)
backend/apps/attachments/views.py:28:def upload_attachment(request, application_id):
backend/apps/attachments/views.py:50:    # Create attachment
backend/apps/attachments/views.py:52:    attachment = Attachment.objects.create(
backend/apps/attachments/views.py:53:        attachment_id=f'att_{uuid.uuid4().hex[:12]}',
backend/apps/attachments/views.py:57:        attachment_type=serializer.validated_data['attachment_type'],
backend/apps/attachments/views.py:63:    return Response(AttachmentSerializer(attachment).data, status=status.HTTP_201_CREATED)
backend/apps/attachments/views.py:66:def list_attachments(request, application_id):
backend/apps/attachments/views.py:81:    # List attachments (exclude soft-deleted)
backend/apps/attachments/views.py:82:    attachments = Attachment.objects.filter(application=application, is_deleted=False)
backend/apps/attachments/views.py:83:    serializer = AttachmentSerializer(attachments, many=True)
backend/apps/attachments/views.py:84:    return Response({'attachments': serializer.data})
backend/apps/attachments/views.py:89:def download_attachment(request, attachment_id):
backend/apps/attachments/views.py:92:    # Get attachment
backend/apps/attachments/views.py:94:        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
backend/apps/attachments/views.py:99:    # Check if soft-deleted
backend/apps/attachments/views.py:100:    if attachment.is_deleted:
backend/apps/attachments/views.py:105:    application = attachment.application
backend/apps/attachments/views.py:112:        return FileResponse(attachment.file.open('rb'), as_attachment=True, filename=attachment.file_name, content_type=attachment.content_type)
backend/apps/attachments/views.py:120:def delete_attachment(request, attachment_id):
backend/apps/attachments/views.py:123:    # Get attachment
backend/apps/attachments/views.py:125:        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
backend/apps/attachments/views.py:130:    # Check if already deleted
backend/apps/attachments/views.py:131:    if attachment.is_deleted:
backend/apps/attachments/views.py:136:    if user.role != UserRole.STUDENT or attachment.application.student_id != user.user_id:
backend/apps/attachments/views.py:140:    # Soft delete
backend/apps/attachments/views.py:141:    attachment.is_deleted = True
backend/apps/attachments/views.py:142:    attachment.deleted_at = timezone.now()
backend/apps/attachments/views.py:143:    attachment.save()
backend/apps/attachments/serializers.py:7:    attachment_type = serializers.ChoiceField(choices=AttachmentType.choices)
backend/apps/attachments/serializers.py:26:        fields = ['attachment_id', 'file_name', 'file_size', 'content_type', 'attachment_type', 'uploaded_at']
backend/apps/attachments/serializers.py:27:        read_only_fields = ['attachment_id', 'file_name', 'file_size', 'content_type', 'uploaded_at']
backend/apps/attachments/migrations/0001_initial.py:21:                ('attachment_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
backend/apps/attachments/migrations/0001_initial.py:22:                ('file', models.FileField(upload_to='attachments/%Y/%m/%d/')),
backend/apps/attachments/migrations/0001_initial.py:23:                ('attachment_type', models.CharField(choices=[('dorm_checkout', '宿舍清退证明'), ('library_clearance', '图书馆清书证明'), ('finance_clearance', '财务结清证明'), ('other', '其他')], max_length=50)),
backend/apps/attachments/migrations/0001_initial.py:28:                ('is_deleted', models.BooleanField(default=False)),
backend/apps/attachments/migrations/0001_initial.py:29:                ('deleted_at', models.DateTimeField(blank=True, null=True)),
backend/apps/attachments/migrations/0001_initial.py:30:                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='applications.application')),
backend/apps/attachments/migrations/0001_initial.py:31:                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
backend/apps/attachments/migrations/0001_initial.py:34:                'db_table': 'attachments',
backend/apps/attachments/models.py:14:    attachment_id = models.CharField(max_length=50, primary_key=True)
backend/apps/attachments/models.py:15:    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='attachments')
backend/apps/attachments/models.py:16:    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT)
backend/apps/attachments/models.py:17:    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
backend/apps/attachments/models.py:18:    attachment_type = models.CharField(max_length=50, choices=AttachmentType.choices)
backend/apps/attachments/models.py:23:    is_deleted = models.BooleanField(default=False)
backend/apps/attachments/models.py:24:    deleted_at = models.DateTimeField(null=True, blank=True)
backend/apps/attachments/models.py:27:        db_table = 'attachments'
backend/apps/attachments/models.py:31:        return f"{self.attachment_id} - {self.file_name}"
backend/apps/notifications/models.py:37:        on_delete=models.PROTECT,
backend/apps/notifications/models.py:43:        on_delete=models.PROTECT,
backend/apps/users/tests/test_import_csv.py:19:        f = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8')
backend/apps/attachments/tests/test_download.py:9:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_download.py:64:        # Create attachment with actual file
backend/apps/attachments/tests/test_download.py:66:        self.attachment = Attachment.objects.create(
backend/apps/attachments/tests/test_download.py:67:            attachment_id='att_test001',
backend/apps/attachments/tests/test_download.py:71:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_download.py:77:    def test_download_positive_student(self):
backend/apps/attachments/tests/test_download.py:78:        """Student can download own application attachment"""
backend/apps/attachments/tests/test_download.py:82:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_download.py:88:    def test_download_positive_counselor(self):
backend/apps/attachments/tests/test_download.py:89:        """Assigned counselor can download attachment"""
backend/apps/attachments/tests/test_download.py:93:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_download.py:98:    def test_download_forbidden(self):
backend/apps/attachments/tests/test_download.py:99:        """Unauthorized student cannot download attachment"""
backend/apps/attachments/tests/test_download.py:103:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_download.py:109:    def test_download_soft_deleted_returns_404(self):
backend/apps/attachments/tests/test_download.py:110:        """Soft-deleted attachment returns 404"""
backend/apps/attachments/tests/test_download.py:111:        self.attachment.is_deleted = True
backend/apps/attachments/tests/test_download.py:112:        self.attachment.save()
backend/apps/attachments/tests/test_download.py:117:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_delete.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_delete.py:63:        # Create attachment
backend/apps/attachments/tests/test_delete.py:65:        self.attachment = Attachment.objects.create(
backend/apps/attachments/tests/test_delete.py:66:            attachment_id='att_test001',
backend/apps/attachments/tests/test_delete.py:70:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_delete.py:76:    def test_delete_owner_success(self):
backend/apps/attachments/tests/test_delete.py:77:        """Owner student can soft-delete attachment"""
backend/apps/attachments/tests/test_delete.py:80:        response = self.client.delete(
backend/apps/attachments/tests/test_delete.py:81:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_delete.py:86:        # Verify soft delete
backend/apps/attachments/tests/test_delete.py:87:        self.attachment.refresh_from_db()
backend/apps/attachments/tests/test_delete.py:88:        self.assertTrue(self.attachment.is_deleted)
backend/apps/attachments/tests/test_delete.py:89:        self.assertIsNotNone(self.attachment.deleted_at)
backend/apps/attachments/tests/test_delete.py:91:    def test_delete_non_owner_student_forbidden(self):
backend/apps/attachments/tests/test_delete.py:92:        """Non-owner student cannot delete attachment"""
backend/apps/attachments/tests/test_delete.py:95:        response = self.client.delete(
backend/apps/attachments/tests/test_delete.py:96:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_delete.py:102:        # Verify not deleted
backend/apps/attachments/tests/test_delete.py:103:        self.attachment.refresh_from_db()
backend/apps/attachments/tests/test_delete.py:104:        self.assertFalse(self.attachment.is_deleted)
backend/apps/attachments/tests/test_delete.py:106:    def test_delete_counselor_forbidden(self):
backend/apps/attachments/tests/test_delete.py:107:        """Counselor cannot delete attachment"""
backend/apps/attachments/tests/test_delete.py:110:        response = self.client.delete(
backend/apps/attachments/tests/test_delete.py:111:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_delete.py:117:    def test_delete_already_deleted_returns_404(self):
backend/apps/attachments/tests/test_delete.py:118:        """Deleting already-deleted attachment returns 404"""
backend/apps/attachments/tests/test_delete.py:119:        self.attachment.is_deleted = True
backend/apps/attachments/tests/test_delete.py:120:        self.attachment.save()
backend/apps/attachments/tests/test_delete.py:124:        response = self.client.delete(
backend/apps/attachments/tests/test_delete.py:125:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/notifications/migrations/0001_initial.py:29:                ('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='notifications_triggered', to=settings.AUTH_USER_MODEL, verbose_name='触发者')),
backend/apps/notifications/migrations/0001_initial.py:30:                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='notifications_received', to=settings.AUTH_USER_MODEL, verbose_name='接收者')),
backend/apps/attachments/tests/test_list.py:9:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_list.py:86:        # Create attachment
backend/apps/attachments/tests/test_list.py:87:        self.attachment = Attachment.objects.create(
backend/apps/attachments/tests/test_list.py:88:            attachment_id='att_test001',
backend/apps/attachments/tests/test_list.py:92:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_list.py:109:        """Student can list own application attachments"""
backend/apps/attachments/tests/test_list.py:113:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:117:        self.assertEqual(len(response.data['attachments']), 1)
backend/apps/attachments/tests/test_list.py:118:        self.assertEqual(response.data['attachments'][0]['attachment_id'], 'att_test001')
backend/apps/attachments/tests/test_list.py:121:        """Student cannot list another student's attachments"""
backend/apps/attachments/tests/test_list.py:125:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:132:        """Assigned counselor can list application attachments"""
backend/apps/attachments/tests/test_list.py:136:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:140:        self.assertEqual(len(response.data['attachments']), 1)
backend/apps/attachments/tests/test_list.py:143:        """Cross-counselor cannot list application attachments"""
backend/apps/attachments/tests/test_list.py:147:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:154:        """Dean with pending approval can list attachments"""
backend/apps/attachments/tests/test_list.py:158:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:162:        self.assertEqual(len(response.data['attachments']), 1)
backend/apps/attachments/tests/test_list.py:164:    def test_list_excludes_soft_deleted(self):
backend/apps/attachments/tests/test_list.py:165:        """List excludes soft-deleted attachments"""
backend/apps/attachments/tests/test_list.py:166:        # Soft delete the attachment
backend/apps/attachments/tests/test_list.py:167:        self.attachment.is_deleted = True
backend/apps/attachments/tests/test_list.py:168:        self.attachment.save()
backend/apps/attachments/tests/test_list.py:173:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:177:        self.assertEqual(len(response.data['attachments']), 0)
backend/apps/attachments/tests/test_upload.py:8:from apps.attachments.models import Attachment, AttachmentType
backend/apps/attachments/tests/test_upload.py:76:        """Student can upload attachment to own application"""
backend/apps/attachments/tests/test_upload.py:81:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:84:                'attachment_type': AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_upload.py:91:        self.assertIn('attachment_id', response.data)
backend/apps/attachments/tests/test_upload.py:92:        self.assertTrue(response.data['attachment_id'].startswith('att_'))
backend/apps/attachments/tests/test_upload.py:93:        self.assertEqual(len(response.data['attachment_id']), 16)  # att_ + 12 hex chars
backend/apps/attachments/tests/test_upload.py:94:        self.assertEqual(response.data['attachment_type'], AttachmentType.DORM_CHECKOUT)
backend/apps/attachments/tests/test_upload.py:103:            f'/api/applications/{self.other_application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:106:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:115:        """Counselor cannot upload attachments"""
backend/apps/attachments/tests/test_upload.py:120:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:123:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:136:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:138:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:149:        """Upload fails with missing attachment_type"""
backend/apps/attachments/tests/test_upload.py:154:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:164:        self.assertIn('attachment_type', response.data['error']['details'])

exec
/bin/bash -lc 'rtk ls -la docs && rtk rg -n "SMOKE_RESET|drf-spectacular|spectacular|api-schema-todo|DEPLOYMENT|SPECTACULAR_SETTINGS|schema/swagger" -S .' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
acceptance/
api/
contracts/
design/
discussions/
plans/
superpowers/
templates/
Codex审查流程指南.md  7.0K
PROJECT-SUMMARY.md  80.3K
codex-review-protocol.md  7.0K
week3-day0-acceptance-checklist.md  11.7K
week3-day0-environment-strategy.md  2.2K
week3-day0-seed-data-requirements.md  4.1K
微信小程序备案说明.md  4.3K
微信小程序申请说明.md  2.4K
数据对接说明文档.md  13.8K
数据对接说明文档.md.backup  11.5K
数据确认清单.md  7.3K
用户设计说明书.md  12.2K
./docs/api/api-schema-todo.md:53:from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
./docs/api/api-schema-todo.md:87:drf-spectacular自动添加数字后缀（applications_retrieve, applications_retrieve_2）
./docs/api/api-schema-todo.md:155:from drf_spectacular.types import OpenApiTypes
./docs/api/api-schema-todo.md:190:使用drf-spectacular的分页支持或自定义分页serializer
./docs/acceptance/phase4c-evidence-index.md:111:**路径：** `DEPLOYMENT.md`
./docs/acceptance/phase4c-evidence-index.md:258:- Track 2: Docker/media/smoke硬化（media volume + .env.example + DEPLOYMENT.md + 附件smoke测试）
./docs/acceptance/phase4c-acceptance-checklist.md:124:| DEPLOYMENT.md存在 | ✅ 通过 | 完整部署指南 |
./DEPLOYMENT.md:64:SMOKE_RESET=1 ./tests/smoke_test.sh
./DEPLOYMENT.md:85:- API Schema: http://localhost:8001/api/schema/swagger-ui/
./DEPLOYMENT.md:234:**URL:** http://localhost:8001/api/schema/swagger-ui/
./DEPLOYMENT.md:239:- drf-spectacular not installed: `docker compose exec backend pip list | grep spectacular`
./docs/PROJECT-SUMMARY.md:1329:**任务22：DEPLOYMENT.md部署说明（30分钟）**
./docs/PROJECT-SUMMARY.md:1359:- DEPLOYMENT.md（完整部署指南）
./docs/PROJECT-SUMMARY.md:1365:- ✓ DEPLOYMENT.md流程清晰完整
./docs/PROJECT-SUMMARY.md:1379:- ✓ Commit 2: feat: Docker/media/smoke硬化（media volume + .env.example + DEPLOYMENT.md + 附件smoke测试）
./docs/PROJECT-SUMMARY.md:1798:- ✓ 实现SMOKE_RESET=1环境重置开关
./docs/PROJECT-SUMMARY.md:1799:- ✓ 更新DEPLOYMENT.md说明前置条件和使用方法
./docs/PROJECT-SUMMARY.md:1810:- tests/smoke_test.sh（SMOKE_RESET + 通知验证 + H2场景 + attachment修复）
./docs/PROJECT-SUMMARY.md:1811:- DEPLOYMENT.md（smoke前置条件说明）
./docs/PROJECT-SUMMARY.md:1825:- ✓ 引入drf-spectacular（v0.27.1）
./docs/PROJECT-SUMMARY.md:1826:- ✓ 配置settings.py（INSTALLED_APPS + REST_FRAMEWORK + SPECTACULAR_SETTINGS）
./docs/PROJECT-SUMMARY.md:1828:- ✓ 验证基线可访问（/api/schema/ + /api/schema/swagger-ui/）
./docs/PROJECT-SUMMARY.md:1831:- ✓ 创建待完善清单（docs/api/api-schema-todo.md）
./docs/PROJECT-SUMMARY.md:1834:- backend/requirements/base.txt（添加drf-spectacular==0.27.1）
./docs/PROJECT-SUMMARY.md:1835:- backend/config/settings/base.py（配置drf-spectacular）
./docs/PROJECT-SUMMARY.md:1837:- docs/api/api-schema-todo.md（待完善清单：13个function-based views需extend_schema）
./docs/PROJECT-SUMMARY.md:1841:- /api/schema/swagger-ui/: HTTP 200 ✓
./docs/PROJECT-SUMMARY.md:1847:- ✓ 补充DEPLOYMENT.md环境变量表（基于settings.py实际读取的9个变量）
./docs/PROJECT-SUMMARY.md:1848:- ✓ 补充DEPLOYMENT.md故障排查指南（覆盖8个真实场景）
./docs/PROJECT-SUMMARY.md:1849:- ✓ 修正api-schema-todo.md表述（13条path/15个operation，修正mark-as-read路径）
./docs/PROJECT-SUMMARY.md:1853:- DEPLOYMENT.md（环境变量表 + 扩展故障排查指南）
./docs/PROJECT-SUMMARY.md:1854:- docs/api/api-schema-todo.md（修正表述）
./docs/PROJECT-SUMMARY.md:1859:- api-schema-todo.md: 修正path/operation表述和mark-as-read路径 ✓
./docs/PROJECT-SUMMARY.md:1864:- ✅ Step 2: API文档基线（drf-spectacular + 13条path/15个operation + 待完善清单）
./docs/PROJECT-SUMMARY.md:1868:- ✓ 未承诺完整API schema（P1/P2待完善项已记录到api-schema-todo.md）
./docs/PROJECT-SUMMARY.md:1869:- ✓ 未无条件自动重置数据库（SMOKE_RESET=1为可选开关）
./backend/requirements/base.txt:7:drf-spectacular==0.27.1
./tests/smoke_test.sh:10:#   SMOKE_RESET=1 ./tests/smoke_test.sh
./tests/smoke_test.sh:22:# Check and handle SMOKE_RESET
./tests/smoke_test.sh:23:if [ "${SMOKE_RESET}" = "1" ]; then
./tests/smoke_test.sh:24:  echo "=== SMOKE_RESET=1: Resetting environment ==="
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:107:- 支持显式重置，例如`SMOKE_RESET=1`时执行`migrate + seed_data --reset`。默认不应破坏开发数据。
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:196:- ✗ SMOKE_RESET支持
./backend/config/urls.py:4:from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
./backend/config/urls.py:16:    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
./backend/config/settings/base.py:31:    'drf_spectacular',
./backend/config/settings/base.py:126:    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
./backend/config/settings/base.py:131:SPECTACULAR_SETTINGS = {
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:15:1. ✓ SMOKE_RESET=1环境重置开关
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:29:1. ✓ 引入drf-spectacular v0.27.1
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:30:2. ✓ 配置settings.py（INSTALLED_APPS + REST_FRAMEWORK + SPECTACULAR_SETTINGS）
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:37:- /api/schema/swagger-ui/: HTTP 200 ✓
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:42:**待完善项（已记录到docs/api/api-schema-todo.md）：**
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:57:- 任务3.1: 补充DEPLOYMENT.md环境变量表（15分钟）
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:67:- DEPLOYMENT.md在Step 1.0中已经更新过smoke前置条件
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:103:- 验证SMOKE_RESET=1的可靠性
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:155:- 在DEPLOYMENT.md中添加环境变量表
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:160:- 在DEPLOYMENT.md中添加故障排查章节
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:170:- DEPLOYMENT.md包含完整的环境变量表
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:171:- DEPLOYMENT.md包含实用的故障排查指南
./docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:153:- 补充DEPLOYMENT.md生产部署章节
./docs/discussions/phase4c-next-steps/24-claude-consensus-evidence-closure.md:46:- Docker部署：`DEPLOYMENT.md`（6步快速启动）
./docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:116:**任务8: 引入drf-spectacular（30分钟）**
./docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:117:- 安装drf-spectacular
./docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:134:- 补充DEPLOYMENT.md环境变量说明
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:46:- `DEPLOYMENT.md`
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:56:**位置：** `tests/smoke_test.sh:29-40`、`tests/smoke_test.sh:300-308`、`DEPLOYMENT.md:60-67`
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:64:- `DEPLOYMENT.md`现在只说运行脚本，没有说明需要重置数据库、迁移和seed顺序。
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:71:   在`tests/smoke_test.sh`头部和`DEPLOYMENT.md`说明：必须在`docker compose down -v`、`migrate`、`seed_data`之后运行。
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:74:   支持类似`SMOKE_RESET=1 ./tests/smoke_test.sh`，只有显式设置时才执行破坏性重置，避免误删开发数据。
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:96:引入`drf-spectacular`本身风险可控，但当前项目大量使用function-based views和手写`Response`错误结构。文件上传虽然有`MultiPartParser`，但OpenAPI对multipart字段、错误envelope、下载文件响应、分页结构和JWT认证的生成结果仍需要人工校准。
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:115:**位置：** `DEPLOYMENT.md:5-67`、`DEPLOYMENT.md:109-128`
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:147:Smoke增强0.5-1小时可接受，但前提是只做文档式前置条件。如果实现`SMOKE_RESET=1`，应估为1-1.5小时。
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:179:> 下一步执行Option E-lite。先处理smoke可重复运行门禁，再增强通知字段和审批驳回路径；随后引入drf-spectacular作为OpenAPI基线，只验收schema可访问、端点清单和认证可见，并记录待完善项；最后补部署文档的环境变量表、smoke前置条件和故障排查。不要在本轮承诺完整API schema，也不要无条件自动重置数据库。
./docs/discussions/phase4c-next-steps/43-claude-post-phase2a-stabilization-next-strategy.md:51:**任务8: 引入drf-spectacular（30分钟）**
./docs/discussions/phase4c-next-steps/43-claude-post-phase2a-stabilization-next-strategy.md:52:- 安装drf-spectacular
./docs/discussions/phase4c-next-steps/43-claude-post-phase2a-stabilization-next-strategy.md:69:- 补充DEPLOYMENT.md环境变量说明
./docs/discussions/phase4c-next-steps/43-claude-post-phase2a-stabilization-next-strategy.md:97:- API文档基线：需要安装新依赖drf-spectacular，可能与现有配置冲突
./docs/discussions/phase4c-next-steps/22-claude-post-execution-next-steps.md:22:- DEPLOYMENT.md完整部署指南（6步快速启动）
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:70:### P1：drf-spectacular 30分钟生成“完整API文档”的估算偏乐观
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:74:当前后端大量使用function-based views和自定义错误响应 envelope。仅安装`drf-spectacular`并暴露Swagger UI，通常只能生成“可访问的schema”，不能保证：
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:198:- 引入并配置`drf-spectacular`。
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:218:6. `DEPLOYMENT.md`包含环境变量说明、smoke前置条件和故障排查。
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:39:**接受：** 采用"显式重置开关"方案（`SMOKE_RESET=1`）。
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:78:- Step 1.0（smoke重置策略）：1-1.5小时（实现SMOKE_RESET=1）
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:89:**任务1.0.1: 实现SMOKE_RESET开关（45分钟）**
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:90:- 在smoke_test.sh头部检查SMOKE_RESET环境变量
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:98:**任务1.0.2: 更新DEPLOYMENT.md（15分钟）**
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:100:- 说明SMOKE_RESET=1用法
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:105:- 验证SMOKE_RESET=1可以清理环境
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:122:**任务2.1: 引入drf-spectacular（30分钟）**
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:123:- 安装drf-spectacular
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:143:- 补充DEPLOYMENT.md环境变量说明
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:155:1. SMOKE_RESET=1可以清理环境并重新初始化
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:156:2. 未设置SMOKE_RESET时给出前置条件提示
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:157:3. DEPLOYMENT.md说明smoke运行前置条件
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:184:> 下一步执行Option E-lite。先实现smoke可重复运行门禁（SMOKE_RESET=1），再增强通知字段和审批驳回路径；随后引入drf-spectacular作为OpenAPI基线，只验收schema可访问、端点清单和认证可见，并记录待完善项；最后补部署文档的环境变量表、smoke前置条件和故障排查。不承诺完整API schema，不无条件自动重置数据库。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:27:- `tests/smoke_test.sh` 已加入 `SMOKE_RESET=1` 显式重置路径。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:34:- 46 号共识中的验收项写了“通知断言按本次实体过滤，不受旧数据干扰”。当前 smoke 主要通过 message 内容过滤通知，例如包含 `2020001`、`辅导员`、`材料不齐全`，不是通过当前 `approval_id` 或 `application_id` 过滤。由于推荐运行方式是 `SMOKE_RESET=1`，这不是本轮阻塞项，但应避免在总结中声称已经完全实现“按实体 id 过滤”。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:42:- `/api/schema/swagger-ui/` 返回 HTTP 200。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:44:- drf-spectacular 配置已进入 `backend/config/settings/base.py` 和 `backend/config/urls.py`。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:45:- `docs/api/api-schema-todo.md` 已记录 function-based views、operationId 冲突、错误 envelope、文件上传/下载、分页、示例等缺口。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:49:- 47 号文档和 `docs/api/api-schema-todo.md` 写“15 个端点”。我实际从 `/api/schema/` 看到的是 **13 个 path，15 个 operation**。建议统一表述为“13 条 path / 15 个 HTTP operation”，避免后续验收误解。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:50:- `docs/api/api-schema-todo.md` 中 notification mark-as-read 路径写成 `/api/notifications/mark_as_read/`，实际路由和 schema 是 `/api/notifications/{notification_id}/read/`。Step 3 或收尾时应修正这个清单。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:58:1. Step 3.1：补 `DEPLOYMENT.md` 环境变量表。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:59:2. Step 3.2：补 `DEPLOYMENT.md` 故障排查指南。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:97:- smoke 未重置导致重复申请：表现为 409，处理方式是 `SMOKE_RESET=1 ./tests/smoke_test.sh` 或手动清理测试数据。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:104:- schema 页面为空或 500：确认 `drf_spectacular` 已安装、`DEFAULT_SCHEMA_CLASS` 配置存在、后端容器已重启。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:110:- `DEPLOYMENT.md` 有准确环境变量表，且区分必填、默认值、生产建议。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:111:- `DEPLOYMENT.md` 有针对当前 smoke/API/Docker 的故障排查。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:112:- `docs/api/api-schema-todo.md` 修正 path/operation 表述和 mark-as-read 路径。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:132:- `curl /api/schema/swagger-ui/`：HTTP 200
./docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:18:> 下一步执行Option E-lite。先实现smoke可重复运行门禁（SMOKE_RESET=1），再增强通知字段和审批驳回路径；随后引入drf-spectacular作为OpenAPI基线，只验收schema可访问、端点清单和认证可见，并记录待完善项；最后补部署文档的环境变量表、smoke前置条件和故障排查。不承诺完整API schema，不无条件自动重置数据库。
./docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:25:   - 实现SMOKE_RESET=1显式重置开关
./docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:27:   - 更新DEPLOYMENT.md说明前置条件
./docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:39:- 任务1.0.1: 实现SMOKE_RESET开关（45分钟）
./docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:40:- 任务1.0.2: 更新DEPLOYMENT.md（15分钟）
./docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:48:- 任务2.1: 引入drf-spectacular（30分钟）
./docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:61:1. SMOKE_RESET=1可以清理环境并重新初始化
./docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:62:2. 未设置SMOKE_RESET时给出前置条件提示
./docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:63:3. DEPLOYMENT.md说明smoke运行前置条件
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:229:- 使用drf-spectacular生成OpenAPI schema
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:239:- 更新DEPLOYMENT.md
./docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:291:3. DEPLOYMENT.md包含故障排查指南和环境变量说明

codex
The existing response looks coherent, but I’m checking the exact line-level evidence now: smoke assertions, schema TODO wording, deployment docs, and project summary.
exec
/bin/bash -lc "rtk nl -ba docs/api/api-schema-todo.md | sed -n '1,120p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# API Schema 待完善清单
     2	
     3	**创建日期：** 2026-06-02  
     4	**状态：** Option E-lite Step 2基线完成，待后续完善
     5	
     6	---
     7	
     8	## 基线验收状态
     9	
    10	✓ `/api/schema/` 可访问（HTTP 200）  
    11	✓ Swagger UI 可访问（HTTP 200）  
    12	✓ 13条path/15个operation出现在schema中  
    13	✓ JWT Bearer认证可见（type: http, scheme: bearer, bearerFormat: JWT）  
    14	✓ 生成器警告已记录（见下方待完善项）
    15	
    16	---
    17	
    18	## 待完善项
    19	
    20	### 1. Function-based Views需要extend_schema装饰器
    21	
    22	**影响端点：**
    23	- `/api/notifications/` - list_notifications
    24	- `/api/notifications/{notification_id}/read/` - mark_as_read
    25	- `/api/notifications/mark_all_read/` - mark_all_read
    26	- `/api/notifications/unread_count/` - unread_count
    27	- `/api/applications/` - applications_view
    28	- `/api/applications/{application_id}/` - get_application
    29	- `/api/applications/{application_id}/attachments/` - attachments_view
    30	- `/api/approvals/` - list_approvals
    31	- `/api/approvals/{approval_id}/approve/` - approve_approval
    32	- `/api/approvals/{approval_id}/reject/` - reject_approval
    33	- `/api/attachments/{attachment_id}/` - delete_attachment
    34	- `/api/attachments/{attachment_id}/download/` - download_attachment
    35	- `/api/auth/login/` - login
    36	
    37	**问题：**
    38	```
    39	Error [function_name]: unable to guess serializer. This is graceful fallback handling for APIViews.
    40	Consider using GenericAPIView as view base class, if view is under your control.
    41	Either way you may want to add a serializer_class (or method). Ignoring view for now.
    42	```
    43	
    44	**解决方案：**
    45	为每个function-based view添加`@extend_schema`装饰器，明确指定：
    46	- request body schema（POST/PUT/PATCH）
    47	- response schema（所有方法）
    48	- parameters（query/path参数）
    49	- examples（请求/响应示例）
    50	
    51	**示例：**
    52	```python
    53	from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
    54	
    55	@extend_schema(
    56	    request=LoginSerializer,
    57	    responses={200: TokenSerializer, 400: ErrorSerializer},
    58	    examples=[
    59	        OpenApiExample(
    60	            'Login Success',
    61	            value={'access_token': 'eyJ...', 'refresh_token': 'eyJ...'},
    62	            response_only=True,
    63	        ),
    64	    ],
    65	)
    66	@api_view(['POST'])
    67	def login(request):
    68	    ...
    69	```
    70	
    71	---
    72	
    73	### 2. OperationId冲突
    74	
    75	**问题：**
    76	```
    77	Warning: operationId "applications_retrieve" has collisions 
    78	[('/api/applications/', 'get'), ('/api/applications/{application_id}/', 'get')]. 
    79	resolving with numeral suffixes.
    80	```
    81	
    82	**影响：**
    83	- `/api/applications/` GET - 列表端点
    84	- `/api/applications/{application_id}/` GET - 详情端点
    85	
    86	**当前解决：**
    87	drf-spectacular自动添加数字后缀（applications_retrieve, applications_retrieve_2）
    88	
    89	**建议改进：**
    90	使用`@extend_schema`明确指定operationId：
    91	```python
    92	@extend_schema(operation_id='list_applications')
    93	@api_view(['GET'])
    94	def applications_view(request):
    95	    ...
    96	
    97	@extend_schema(operation_id='get_application_detail')
    98	@api_view(['GET'])
    99	def get_application(request, application_id):
   100	    ...
   101	```
   102	
   103	---
   104	
   105	### 3. 自定义错误响应结构
   106	
   107	**当前状态：**
   108	Schema中错误响应为空（`description: No response body`）
   109	
   110	**待补充：**
   111	统一错误响应结构：
   112	```python
   113	{
   114	  "error": {
   115	    "code": "ERROR_CODE",
   116	    "message": "错误消息",
   117	    "details": {...}  # 可选
   118	  }
   119	}
   120	```

exec
/bin/bash -lc "rtk nl -ba DEPLOYMENT.md | sed -n '1,280p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# Deployment Guide
     2	
     3	## Quick Start
     4	
     5	### 1. Environment Setup
     6	
     7	Copy environment template:
     8	```bash
     9	cp .env.example .env.docker
    10	```
    11	
    12	Edit `.env.docker` and configure environment variables (see Environment Variables section below).
    13	
    14	### 2. Start Services
    15	
    16	```bash
    17	docker compose up -d
    18	```
    19	
    20	Wait for services to be healthy (~10 seconds).
    21	
    22	### 3. Database Migration
    23	
    24	```bash
    25	docker compose exec backend python manage.py migrate
    26	```
    27	
    28	### 4. Load Initial Data
    29	
    30	**Option A: Seed test data (development)**
    31	```bash
    32	docker compose exec backend python manage.py seed_data
    33	```
    34	
    35	**Option B: Import production data (production)**
    36	```bash
    37	# 1. Import counselors first
    38	docker compose exec backend python manage.py import_csv \
    39	  --counselors /path/to/counselors.csv \
    40	  --dry-run  # Preview first
    41	
    42	docker compose exec backend python manage.py import_csv \
    43	  --counselors /path/to/counselors.csv  # Apply
    44	
    45	# 2. Import class mappings
    46	docker compose exec backend python manage.py import_csv \
    47	  --mappings /path/to/mappings.csv
    48	
    49	# 3. Import students
    50	docker compose exec backend python manage.py import_csv \
    51	  --students /path/to/students.csv
    52	```
    53	
    54	CSV templates: `backend/data/templates/*.csv`
    55	
    56	### 5. Verify Installation
    57	
    58	**Prerequisites for smoke test:**
    59	- Clean database (no existing applications for test users 2020001, 2020002)
    60	- Seeded test data (users, class mappings)
    61	
    62	**Option A: Auto-reset (recommended for first run)**
    63	```bash
    64	SMOKE_RESET=1 ./tests/smoke_test.sh
    65	```
    66	
    67	This will automatically:
    68	1. Stop containers and remove volumes
    69	2. Restart containers
    70	3. Run migrations
    71	4. Seed test data
    72	5. Run smoke test
    73	
    74	**Option B: Manual verification (if environment is already clean)**
    75	```bash
    76	./tests/smoke_test.sh
    77	```
    78	
    79	**Expected output:** All tests pass, no errors.
    80	
    81	### 6. Access Application
    82	
    83	- Backend API: http://localhost:8001
    84	- Admin: http://localhost:8001/admin
    85	- API Schema: http://localhost:8001/api/schema/swagger-ui/
    86	
    87	## Environment Variables
    88	
    89	### Core Settings
    90	
    91	| Variable | Purpose | Default | Production Required |
    92	|----------|---------|---------|---------------------|
    93	| `SECRET_KEY` | Django secret key for cryptographic signing | `django-insecure-dev-key-change-in-production` | **Yes** - Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
    94	| `DEBUG` | Enable debug mode | `True` | **No** - Set to `False` in production |
    95	| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `localhost,127.0.0.1` | **Yes** - Set to your domain(s) |
    96	
    97	### Database Settings
    98	
    99	| Variable | Purpose | Default | Production Required |
   100	|----------|---------|---------|---------------------|
   101	| `DB_NAME` | PostgreSQL database name | `graduation_leave` | **No** - Default is fine |
   102	| `DB_USER` | PostgreSQL username | `postgres` | **Yes** - Use dedicated user |
   103	| `DB_PASSWORD` | PostgreSQL password | `postgres` | **Yes** - Use secure password |
   104	| `DB_HOST` | PostgreSQL host | `localhost` | **No** - Use `db` for Docker |
   105	| `DB_PORT` | PostgreSQL port | `5432` | **No** - Default is fine |
   106	
   107	### CORS Settings
   108	
   109	| Variable | Purpose | Default | Production Required |
   110	|----------|---------|---------|---------------------|
   111	| `CORS_ALLOWED_ORIGINS` | Comma-separated list of allowed origins | `http://localhost:3000,http://127.0.0.1:3000` | **Yes** - Set to your frontend URL(s) |
   112	
   113	### Notes
   114	
   115	- **JWT Settings:** JWT tokens use `SECRET_KEY` for signing (no separate `JWT_SECRET_KEY` needed)
   116	- **Media Files:** `MEDIA_URL=/media/` and `MEDIA_ROOT=/app/media` are hardcoded (not configurable via env vars)
   117	- **Unused Variables:** `.env.example` may reference `JWT_SECRET_KEY`, `REDIS_URL`, `CELERY_BROKER_URL` - these are not currently read by the application
   118	
   119	## Data Import
   120	
   121	### CSV Field Requirements
   122	
   123	**counselors.csv:**
   124	- employee_id (required)
   125	- name (required)
   126	- department (optional)
   127	
   128	**mappings.csv:**
   129	- class_id (required)
   130	- counselor_employee_id (required)
   131	
   132	**students.csv:**
   133	- student_id (required)
   134	- name (required)
   135	- class_id (required)
   136	- is_graduating (required, true/false)
   137	- graduation_year (required)
   138	
   139	### Import Order
   140	
   141	**CRITICAL:** Import in this order:
   142	1. Counselors (creates counselor accounts)
   143	2. Mappings (links classes to counselors)
   144	3. Students (validates class mappings exist)
   145	
   146	### Dry-Run Mode
   147	
   148	Always preview before applying:
   149	```bash
   150	docker compose exec backend python manage.py import_csv \
   151	  --students students.csv --dry-run
   152	```
   153	
   154	## Troubleshooting
   155	
   156	### Application Errors
   157	
   158	**409 Conflict - Duplicate Application**
   159	```json
   160	{"error": {"code": "CONFLICT", "message": "You already have a pending or approved application"}}
   161	```
   162	**Cause:** Student already has an active application (status: pending_counselor, pending_dean, or approved)
   163	
   164	**Solution:** Student must wait for current application to be rejected before submitting a new one, or contact administrator to check application status.
   165	
   166	**422 Unprocessable Entity - Dorm Clearance Blocked**
   167	```json
   168	{"error": {"code": "DORM_BLOCKED", "message": "Cannot submit application: dorm clearance not completed"}}
   169	```
   170	**Cause:** Student's dorm checkout status is not `completed` (checked via mock provider or real dorm system API)
   171	
   172	**Solution:** Student must complete dorm clearance first. Check dorm system status or contact dorm administrator.
   173	
   174	**401 Unauthorized - JWT Expired**
   175	```json
   176	{"detail": "Given token not valid for any token type"}
   177	```
   178	**Cause:** JWT access token expired (default lifetime: 24 hours)
   179	
   180	**Solution:** Re-login to get new token. Frontend should implement automatic token refresh or redirect to login page.
   181	
   182	**403 Forbidden - Cross-Role Access**
   183	```json
   184	{"error": {"code": "FORBIDDEN", "message": "You do not have permission to perform this action"}}
   185	```
   186	**Common scenarios:**
   187	- Student trying to access another student's application
   188	- Counselor trying to approve application from different class
   189	- Dean trying to approve counselor-step approval
   190	
   191	**Solution:** Verify user role and permissions. Check that counselor is assigned to the student's class via class mappings.
   192	
   193	### Media/Attachment Errors
   194	
   195	**403 Forbidden - Media Access Denied**
   196	
   197	**Cause:** User trying to access attachment they don't have permission to view
   198	
   199	**Solution:** Verify RBAC rules:
   200	- Students can only access their own application's attachments
   201	- Counselors can access attachments for applications in their assigned classes
   202	- Deans can access attachments for applications with pending dean approval
   203	
   204	**404 Not Found - Attachment Missing**
   205	
   206	**Cause:** Attachment file deleted from filesystem or soft-deleted in database
   207	
   208	**Solution:** Check `MEDIA_ROOT` directory (`/app/media` in Docker) and verify attachment record in database.
   209	
   210	### Infrastructure Errors
   211	
   212	**Docker Container Startup Failed**
   213	```bash
   214	docker compose ps  # Check container status
   215	docker compose logs backend  # Check backend logs
   216	```
   217	**Common causes:**
   218	- Port 8001 already in use: Change `ports` in `docker-compose.yml`
   219	- Database not ready: Wait 10 seconds and retry
   220	- Migration failed: Check database connection and run `docker compose exec backend python manage.py migrate`
   221	
   222	**Database Connection Failed**
   223	```bash
   224	docker compose logs db
   225	docker compose restart db
   226	```
   227	**Common causes:**
   228	- Database container not running: `docker compose up -d db`
   229	- Wrong credentials: Check `DB_USER`, `DB_PASSWORD` in `.env.docker`
   230	- Wrong host: Use `DB_HOST=db` (not `localhost`) in Docker environment
   231	
   232	**API Schema Page Not Loading**
   233	
   234	**URL:** http://localhost:8001/api/schema/swagger-ui/
   235	
   236	**Common causes:**
   237	- Backend not running: `docker compose ps`
   238	- Wrong port: Check `docker-compose.yml` port mapping (default: 8001)
   239	- drf-spectacular not installed: `docker compose exec backend pip list | grep spectacular`
   240	
   241	**Solution:** Restart backend container and verify schema endpoint returns 200:
   242	```bash
   243	curl -I http://localhost:8001/api/schema/
   244	```
   245	
   246	## Maintenance
   247	
   248	**View logs:**
   249	```bash
   250	docker compose logs -f backend
   251	```
   252	
   253	**Reset database:**
   254	```bash
   255	docker compose down -v
   256	docker compose up -d
   257	docker compose exec backend python manage.py migrate
   258	```
   259	
   260	**Backup media files:**
   261	```bash
   262	docker compose exec backend tar czf /tmp/media-backup.tar.gz /app/media
   263	docker compose cp backend:/tmp/media-backup.tar.gz ./media-backup.tar.gz
   264	```

exec
/bin/bash -lc "rtk nl -ba tests/smoke_test.sh | sed -n '1,230p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	#!/bin/bash
     2	# Week 3 Day 1 Smoke Test - Minimum Viable Loop
     3	# Base URL: http://localhost:8001 (Docker Compose)
     4	#
     5	# Prerequisites:
     6	# - Clean database (no existing applications for test users)
     7	# - Seeded test data (users, class mappings)
     8	#
     9	# To reset environment before running:
    10	#   SMOKE_RESET=1 ./tests/smoke_test.sh
    11	#
    12	# Manual reset steps:
    13	#   docker compose down -v
    14	#   docker compose up -d --wait
    15	#   docker compose exec backend python manage.py migrate
    16	#   docker compose exec backend python manage.py seed_data
    17	
    18	set -e
    19	
    20	BASE_URL="http://localhost:8001"
    21	
    22	# Check and handle SMOKE_RESET
    23	if [ "${SMOKE_RESET}" = "1" ]; then
    24	  echo "=== SMOKE_RESET=1: Resetting environment ==="
    25	  echo "1. Stopping containers and removing volumes..."
    26	  docker compose down -v
    27	
    28	  echo "2. Starting containers..."
    29	  docker compose up -d --wait
    30	
    31	  echo "3. Running migrations..."
    32	  docker compose exec backend python manage.py migrate
    33	
    34	  echo "4. Seeding test data..."
    35	  docker compose exec backend python manage.py seed_data
    36	
    37	  echo "✓ Environment reset complete"
    38	  echo ""
    39	fi
    40	
    41	echo "=== Week 3 Day 1 Smoke Test ==="
    42	echo "Base URL: $BASE_URL"
    43	echo ""
    44	
    45	# H1: Happy path (Class A)
    46	echo "--- H1: Happy Path (2020001 → T001 → D001) ---"
    47	
    48	# 1. Student login
    49	echo "1. Student 2020001 login..."
    50	STUDENT_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
    51	  -H "Content-Type: application/json" \
    52	  -d '{"user_id":"2020001","password":"2020001"}' \
    53	  | jq -r '.access_token')
    54	
    55	if [ -z "$STUDENT_TOKEN" ] || [ "$STUDENT_TOKEN" = "null" ]; then
    56	  echo "✗ Student login failed"
    57	  exit 1
    58	fi
    59	echo "✓ Student login success"
    60	
    61	# 2. Submit application
    62	echo "2. Submit application..."
    63	LEAVE_DATE=$(date -d "+1 day" +%Y-%m-%d)
    64	APP_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/" \
    65	  -H "Authorization: Bearer $STUDENT_TOKEN" \
    66	  -H "Content-Type: application/json" \
    67	  -d "{\"reason\":\"毕业离校\",\"leave_date\":\"$LEAVE_DATE\"}")
    68	
    69	APP_ID=$(echo "$APP_RESPONSE" | jq -r '.application_id')
    70	APP_STATUS=$(echo "$APP_RESPONSE" | jq -r '.status')
    71	
    72	if [ -z "$APP_ID" ] || [ "$APP_ID" = "null" ]; then
    73	  echo "✗ Application submit failed"
    74	  echo "$APP_RESPONSE" | jq '.'
    75	  exit 1
    76	fi
    77	
    78	if [ "$APP_STATUS" != "pending_counselor" ]; then
    79	  echo "✗ Application status wrong: $APP_STATUS (expected: pending_counselor)"
    80	  exit 1
    81	fi
    82	
    83	echo "✓ Application submitted: $APP_ID (status: $APP_STATUS)"
    84	
    85	# Extract counselor approval ID
    86	COUNSELOR_APPROVAL_ID=$(echo "$APP_RESPONSE" | jq -r '.approvals[] | select(.step=="counselor") | .approval_id')
    87	
    88	if [ -z "$COUNSELOR_APPROVAL_ID" ] || [ "$COUNSELOR_APPROVAL_ID" = "null" ]; then
    89	  echo "✗ Counselor approval not created"
    90	  exit 1
    91	fi
    92	
    93	echo "  Counselor approval: $COUNSELOR_APPROVAL_ID"
    94	
    95	# 3. Upload attachment
    96	echo "3. Upload attachment..."
    97	echo "Test attachment content" > /tmp/test_attachment.pdf
    98	UPLOAD_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/$APP_ID/attachments/" \
    99	  -H "Authorization: Bearer $STUDENT_TOKEN" \
   100	  -F "file=@/tmp/test_attachment.pdf" \
   101	  -F "attachment_type=other")
   102	
   103	ATTACHMENT_ID=$(echo "$UPLOAD_RESPONSE" | jq -r '.attachment_id')
   104	
   105	if [ -z "$ATTACHMENT_ID" ] || [ "$ATTACHMENT_ID" = "null" ]; then
   106	  echo "✗ Attachment upload failed"
   107	  echo "$UPLOAD_RESPONSE" | jq '.'
   108	  exit 1
   109	fi
   110	
   111	echo "✓ Attachment uploaded: $ATTACHMENT_ID"
   112	
   113	# 4. List attachments
   114	echo "4. List attachments..."
   115	LIST_RESPONSE=$(curl -s "$BASE_URL/api/applications/$APP_ID/attachments/" \
   116	  -H "Authorization: Bearer $STUDENT_TOKEN")
   117	
   118	ATTACHMENT_COUNT=$(echo "$LIST_RESPONSE" | jq -r '.attachments | length')
   119	
   120	if [ "$ATTACHMENT_COUNT" != "1" ]; then
   121	  echo "✗ Attachment list failed: expected 1, got $ATTACHMENT_COUNT"
   122	  exit 1
   123	fi
   124	
   125	echo "✓ Attachment list success: $ATTACHMENT_COUNT attachment(s)"
   126	
   127	# 5. Download attachment
   128	echo "5. Download attachment..."
   129	DOWNLOAD_STATUS=$(curl -s -w "\n%{http_code}" -o /tmp/downloaded_attachment.txt \
   130	  "$BASE_URL/api/attachments/$ATTACHMENT_ID/download/" \
   131	  -H "Authorization: Bearer $STUDENT_TOKEN" \
   132	  | tail -1)
   133	
   134	if [ "$DOWNLOAD_STATUS" != "200" ]; then
   135	  echo "✗ Attachment download failed: HTTP $DOWNLOAD_STATUS"
   136	  exit 1
   137	fi
   138	
   139	echo "✓ Attachment download success"
   140	
   141	# 6. Delete attachment
   142	echo "6. Delete attachment..."
   143	DELETE_STATUS=$(curl -s -w "\n%{http_code}" -X DELETE \
   144	  "$BASE_URL/api/attachments/$ATTACHMENT_ID/" \
   145	  -H "Authorization: Bearer $STUDENT_TOKEN" \
   146	  | tail -1)
   147	
   148	if [ "$DELETE_STATUS" != "204" ]; then
   149	  echo "✗ Attachment delete failed: HTTP $DELETE_STATUS"
   150	  exit 1
   151	fi
   152	
   153	echo "✓ Attachment deleted"
   154	
   155	# Verify attachment list is empty
   156	FINAL_LIST=$(curl -s "$BASE_URL/api/applications/$APP_ID/attachments/" \
   157	  -H "Authorization: Bearer $STUDENT_TOKEN")
   158	FINAL_COUNT=$(echo "$FINAL_LIST" | jq -r '.attachments | length')
   159	
   160	if [ "$FINAL_COUNT" != "0" ]; then
   161	  echo "✗ Attachment still exists after delete"
   162	  exit 1
   163	fi
   164	
   165	echo "  Verified: attachment list empty"
   166	
   167	# 7. Counselor login
   168	echo "7. Counselor T001 login..."
   169	T001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
   170	  -H "Content-Type: application/json" \
   171	  -d '{"user_id":"T001","password":"T001"}' \
   172	  | jq -r '.access_token')
   173	
   174	if [ -z "$T001_TOKEN" ] || [ "$T001_TOKEN" = "null" ]; then
   175	  echo "✗ Counselor login failed"
   176	  exit 1
   177	fi
   178	echo "✓ Counselor login success"
   179	
   180	# Verify counselor received APPLICATION_SUBMITTED notification
   181	echo "  Verifying counselor notification..."
   182	COUNSELOR_NOTIFS=$(curl -s "$BASE_URL/api/notifications/" \
   183	  -H "Authorization: Bearer $T001_TOKEN")
   184	
   185	COUNSELOR_APP_NOTIF=$(echo "$COUNSELOR_NOTIFS" | jq -r ".results[] | select(.type == \"application_submitted\" and (.message | contains(\"2020001\")))")
   186	
   187	if [ -z "$COUNSELOR_APP_NOTIF" ]; then
   188	  echo "✗ Counselor APPLICATION_SUBMITTED notification not found"
   189	  echo "Available notifications:"
   190	  echo "$COUNSELOR_NOTIFS" | jq '.results[] | {type, message}'
   191	  exit 1
   192	fi
   193	
   194	NOTIF_TYPE=$(echo "$COUNSELOR_APP_NOTIF" | jq -r '.type')
   195	NOTIF_ENTITY_TYPE=$(echo "$COUNSELOR_APP_NOTIF" | jq -r '.entity_type')
   196	
   197	if [ "$NOTIF_TYPE" != "application_submitted" ]; then
   198	  echo "✗ Notification type wrong: $NOTIF_TYPE (expected: application_submitted)"
   199	  exit 1
   200	fi
   201	
   202	if [ "$NOTIF_ENTITY_TYPE" != "approval" ]; then
   203	  echo "✗ Notification entity_type wrong: $NOTIF_ENTITY_TYPE (expected: approval)"
   204	  exit 1
   205	fi
   206	
   207	echo "  ✓ Counselor received APPLICATION_SUBMITTED notification (type: $NOTIF_TYPE, entity_type: $NOTIF_ENTITY_TYPE)"
   208	
   209	# 8. Counselor approve
   210	echo "8. Counselor approve..."
   211	APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$COUNSELOR_APPROVAL_ID/approve/" \
   212	  -H "Authorization: Bearer $T001_TOKEN" \
   213	  -H "Content-Type: application/json" \
   214	  -d '{"comment":"同意"}')
   215	
   216	APPROVE_DECISION=$(echo "$APPROVE_RESPONSE" | jq -r '.decision')
   217	
   218	if [ "$APPROVE_DECISION" != "approved" ]; then
   219	  echo "✗ Counselor approve failed"
   220	  echo "$APPROVE_RESPONSE" | jq '.'
   221	  exit 1
   222	fi
   223	
   224	echo "✓ Counselor approved"
   225	
   226	# Verify student received APPROVAL_APPROVED notification
   227	echo "  Verifying student notification..."
   228	STUDENT_NOTIFS=$(curl -s "$BASE_URL/api/notifications/" \
   229	  -H "Authorization: Bearer $STUDENT_TOKEN")
   230	

exec
/bin/bash -lc "rtk nl -ba tests/smoke_test.sh | sed -n '230,520p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   230	
   231	STUDENT_APPROVE_NOTIF=$(echo "$STUDENT_NOTIFS" | jq -r ".results[] | select(.type == \"approval_approved\" and (.message | contains(\"辅导员\")))")
   232	
   233	if [ -z "$STUDENT_APPROVE_NOTIF" ]; then
   234	  echo "✗ Student APPROVAL_APPROVED notification not found"
   235	  echo "Available notifications:"
   236	  echo "$STUDENT_NOTIFS" | jq '.results[] | {type, message}'
   237	  exit 1
   238	fi
   239	
   240	NOTIF_TYPE=$(echo "$STUDENT_APPROVE_NOTIF" | jq -r '.type')
   241	NOTIF_ENTITY_TYPE=$(echo "$STUDENT_APPROVE_NOTIF" | jq -r '.entity_type')
   242	
   243	if [ "$NOTIF_TYPE" != "approval_approved" ]; then
   244	  echo "✗ Notification type wrong: $NOTIF_TYPE (expected: approval_approved)"
   245	  exit 1
   246	fi
   247	
   248	if [ "$NOTIF_ENTITY_TYPE" != "approval" ]; then
   249	  echo "✗ Notification entity_type wrong: $NOTIF_ENTITY_TYPE (expected: approval)"
   250	  exit 1
   251	fi
   252	
   253	echo "  ✓ Student received APPROVAL_APPROVED notification (type: $NOTIF_TYPE, entity_type: $NOTIF_ENTITY_TYPE)"
   254	
   255	echo "  ✓ Student has $STUDENT_NOTIF_COUNT unread notification(s)"
   256	
   257	# Verify application status changed
   258	APP_STATUS_AFTER=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
   259	  -H "Authorization: Bearer $STUDENT_TOKEN" \
   260	  | jq -r '.status')
   261	
   262	if [ "$APP_STATUS_AFTER" != "pending_dean" ]; then
   263	  echo "✗ Application status not updated: $APP_STATUS_AFTER (expected: pending_dean)"
   264	  exit 1
   265	fi
   266	
   267	echo "  Application status: $APP_STATUS_AFTER"
   268	
   269	# Extract dean approval ID
   270	DEAN_APPROVAL_ID=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
   271	  -H "Authorization: Bearer $STUDENT_TOKEN" \
   272	  | jq -r '.approvals[] | select(.step=="dean") | .approval_id')
   273	
   274	if [ -z "$DEAN_APPROVAL_ID" ] || [ "$DEAN_APPROVAL_ID" = "null" ]; then
   275	  echo "✗ Dean approval not created"
   276	  exit 1
   277	fi
   278	
   279	echo "  Dean approval: $DEAN_APPROVAL_ID"
   280	
   281	# 9. Dean login
   282	echo "9. Dean D001 login..."
   283	DEAN_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
   284	  -H "Content-Type: application/json" \
   285	  -d '{"user_id":"D001","password":"D001"}' \
   286	  | jq -r '.access_token')
   287	
   288	if [ -z "$DEAN_TOKEN" ] || [ "$DEAN_TOKEN" = "null" ]; then
   289	  echo "✗ Dean login failed"
   290	  exit 1
   291	fi
   292	echo "✓ Dean login success"
   293	
   294	# 10. Dean approve
   295	echo "10. Dean approve..."
   296	DEAN_APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$DEAN_APPROVAL_ID/approve/" \
   297	  -H "Authorization: Bearer $DEAN_TOKEN" \
   298	  -H "Content-Type: application/json" \
   299	  -d '{"comment":"批准"}')
   300	
   301	DEAN_DECISION=$(echo "$DEAN_APPROVE_RESPONSE" | jq -r '.decision')
   302	
   303	if [ "$DEAN_DECISION" != "approved" ]; then
   304	  echo "✗ Dean approve failed"
   305	  echo "$DEAN_APPROVE_RESPONSE" | jq '.'
   306	  exit 1
   307	fi
   308	
   309	echo "✓ Dean approved"
   310	
   311	# Verify student received second APPROVAL_APPROVED notification
   312	echo "  Verifying student notification..."
   313	STUDENT_NOTIF_COUNT_FINAL=$(curl -s "$BASE_URL/api/notifications/unread_count/" \
   314	  -H "Authorization: Bearer $STUDENT_TOKEN" \
   315	  | jq -r '.unread_count')
   316	
   317	if [ "$STUDENT_NOTIF_COUNT_FINAL" -lt "2" ]; then
   318	  echo "✗ Student notification count wrong: expected ≥2, got $STUDENT_NOTIF_COUNT_FINAL"
   319	  exit 1
   320	fi
   321	
   322	echo "  ✓ Student has $STUDENT_NOTIF_COUNT_FINAL unread notification(s)"
   323	
   324	# 11. Verify final status
   325	echo "11. Verify final status..."
   326	FINAL_STATUS=$(curl -s "$BASE_URL/api/applications/$APP_ID/" \
   327	  -H "Authorization: Bearer $STUDENT_TOKEN" \
   328	  | jq -r '.status')
   329	
   330	if [ "$FINAL_STATUS" != "approved" ]; then
   331	  echo "✗ Final status wrong: $FINAL_STATUS (expected: approved)"
   332	  exit 1
   333	fi
   334	
   335	echo "✓ Final status: $FINAL_STATUS"
   336	
   337	echo ""
   338	echo "--- H2: Rejection Path (2020002 → T002 reject) ---"
   339	
   340	# 12. Student 2020002 login
   341	echo "12. Student 2020002 login..."
   342	STUDENT2_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
   343	  -H "Content-Type: application/json" \
   344	  -d '{"user_id":"2020002","password":"2020002"}' \
   345	  | jq -r '.access_token')
   346	
   347	if [ -z "$STUDENT2_TOKEN" ] || [ "$STUDENT2_TOKEN" = "null" ]; then
   348	  echo "✗ Student 2020002 login failed"
   349	  exit 1
   350	fi
   351	echo "✓ Student 2020002 login success"
   352	
   353	# 13. Submit application
   354	echo "13. Submit application..."
   355	APP2_RESPONSE=$(curl -s -X POST "$BASE_URL/api/applications/" \
   356	  -H "Authorization: Bearer $STUDENT2_TOKEN" \
   357	  -H "Content-Type: application/json" \
   358	  -d "{\"reason\":\"测试驳回流程\",\"leave_date\":\"$LEAVE_DATE\"}")
   359	
   360	APP2_ID=$(echo "$APP2_RESPONSE" | jq -r '.application_id')
   361	COUNSELOR2_APPROVAL_ID=$(echo "$APP2_RESPONSE" | jq -r '.approvals[] | select(.step=="counselor") | .approval_id')
   362	
   363	if [ -z "$APP2_ID" ] || [ "$APP2_ID" = "null" ]; then
   364	  echo "✗ Application submit failed"
   365	  exit 1
   366	fi
   367	
   368	echo "✓ Application submitted: $APP2_ID"
   369	echo "  Counselor approval: $COUNSELOR2_APPROVAL_ID"
   370	
   371	# 14. T002 login
   372	echo "14. T002 login..."
   373	T002_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
   374	  -H "Content-Type: application/json" \
   375	  -d '{"user_id":"T002","password":"T002"}' \
   376	  | jq -r '.access_token')
   377	
   378	if [ -z "$T002_TOKEN" ] || [ "$T002_TOKEN" = "null" ]; then
   379	  echo "✗ T002 login failed"
   380	  exit 1
   381	fi
   382	echo "✓ T002 login success"
   383	
   384	# 15. T002 reject
   385	echo "15. T002 reject..."
   386	REJECT_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$COUNSELOR2_APPROVAL_ID/reject/" \
   387	  -H "Authorization: Bearer $T002_TOKEN" \
   388	  -H "Content-Type: application/json" \
   389	  -d '{"comment":"材料不齐全，请补充"}')
   390	
   391	REJECT_DECISION=$(echo "$REJECT_RESPONSE" | jq -r '.decision')
   392	
   393	if [ "$REJECT_DECISION" != "rejected" ]; then
   394	  echo "✗ Counselor reject failed"
   395	  echo "$REJECT_RESPONSE" | jq '.'
   396	  exit 1
   397	fi
   398	
   399	echo "✓ Counselor rejected"
   400	
   401	# Verify student received APPROVAL_REJECTED notification
   402	echo "  Verifying student rejection notification..."
   403	STUDENT2_NOTIFS=$(curl -s "$BASE_URL/api/notifications/" \
   404	  -H "Authorization: Bearer $STUDENT2_TOKEN")
   405	
   406	STUDENT2_REJECT_NOTIF=$(echo "$STUDENT2_NOTIFS" | jq -r ".results[] | select(.type == \"approval_rejected\" and (.message | contains(\"材料不齐全\")))")
   407	
   408	if [ -z "$STUDENT2_REJECT_NOTIF" ]; then
   409	  echo "✗ Student APPROVAL_REJECTED notification not found"
   410	  echo "Available notifications:"
   411	  echo "$STUDENT2_NOTIFS" | jq '.results[] | {type, message}'
   412	  exit 1
   413	fi
   414	
   415	NOTIF_TYPE=$(echo "$STUDENT2_REJECT_NOTIF" | jq -r '.type')
   416	NOTIF_ENTITY_TYPE=$(echo "$STUDENT2_REJECT_NOTIF" | jq -r '.entity_type')
   417	NOTIF_MESSAGE=$(echo "$STUDENT2_REJECT_NOTIF" | jq -r '.message')
   418	
   419	if [ "$NOTIF_TYPE" != "approval_rejected" ]; then
   420	  echo "✗ Notification type wrong: $NOTIF_TYPE (expected: approval_rejected)"
   421	  exit 1
   422	fi
   423	
   424	if [ "$NOTIF_ENTITY_TYPE" != "approval" ]; then
   425	  echo "✗ Notification entity_type wrong: $NOTIF_ENTITY_TYPE (expected: approval)"
   426	  exit 1
   427	fi
   428	
   429	if ! echo "$NOTIF_MESSAGE" | grep -q "材料不齐全"; then
   430	  echo "✗ Notification message missing rejection reason: $NOTIF_MESSAGE"
   431	  exit 1
   432	fi
   433	
   434	echo "  ✓ Student received APPROVAL_REJECTED notification with reason (type: $NOTIF_TYPE, entity_type: $NOTIF_ENTITY_TYPE)"
   435	
   436	echo ""
   437	echo "--- N2: Cross-counselor approval (negative test) ---"
   438	
   439	# N2: T002 tries to approve T001's approval (should fail)
   440	# (Reusing T002_TOKEN from H2 scenario)
   441	echo "16. T002 tries to approve T001's approval (should fail)..."
   442	CROSS_APPROVE_STATUS=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/approvals/$COUNSELOR_APPROVAL_ID/approve/" \
   443	  -H "Authorization: Bearer $T002_TOKEN" \
   444	  -H "Content-Type: application/json" \
   445	  -d '{"comment":"尝试跨班级审批"}' \
   446	  | tail -1)
   447	
   448	if [ "$CROSS_APPROVE_STATUS" != "403" ]; then
   449	  echo "✗ Cross-counselor approve should return 403, got: $CROSS_APPROVE_STATUS"
   450	  exit 1
   451	fi
   452	
   453	echo "✓ Cross-counselor approve blocked (403)"
   454	
   455	echo ""
   456	echo "=== All tests passed ==="

codex
Step 3 appears to have been completed after the 47 request: `DEPLOYMENT.md`, `docs/api/api-schema-todo.md`, and `docs/PROJECT-SUMMARY.md` already include the tightened items recommended in the existing response. I’m doing one non-destructive endpoint check if the local backend is up.
exec
/bin/bash -lc "rtk curl -s -o /tmp/swagger-check.html -w '%{http_code}' http://localhost:8001/api/schema/swagger-ui/" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
200

exec
/bin/bash -lc "rtk curl -s -o /tmp/schema-check.json -w '%{http_code}' http://localhost:8001/api/schema/" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
200

exec
/bin/bash -lc "rtk nl -ba docs/PROJECT-SUMMARY.md | sed -n '1788,1875p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
  1788	---
  1789	
  1790	### Option E-lite执行（2026-06-01）
  1791	
  1792	**背景：**
  1793	- Phase 2A稳定化完成后，Claude-Codex协作讨论下一步策略
  1794	- 共识执行Option E-lite：Smoke增强 + API文档基线 + 部署文档补漏
  1795	- 执行约束：不承诺完整API schema，不无条件自动重置数据库
  1796	
  1797	**Step 1.0: Smoke可重复运行门禁（已完成）：**
  1798	- ✓ 实现SMOKE_RESET=1环境重置开关
  1799	- ✓ 更新DEPLOYMENT.md说明前置条件和使用方法
  1800	- ✓ 验证可重复运行（连续两次执行不失败）
  1801	
  1802	**Step 1: Smoke增强（已完成）：**
  1803	- ✓ 增强通知验证（验证type、entity_type、message字段）
  1804	- ✓ 添加H2审批驳回场景（验证APPROVAL_REJECTED通知）
  1805	- ✓ 修复attachment文件类型问题（.txt → .pdf）
  1806	- ✓ 修复attachment URL问题（download/delete路径错误）
  1807	- ✓ 所有smoke test通过（H1 Happy Path + H2 Rejection + N2 Negative）
  1808	
  1809	**产出物：**
  1810	- tests/smoke_test.sh（SMOKE_RESET + 通知验证 + H2场景 + attachment修复）
  1811	- DEPLOYMENT.md（smoke前置条件说明）
  1812	
  1813	**测试结果：**
  1814	- H1 Happy Path: ✓ 通过
  1815	- H2 Rejection Path: ✓ 通过
  1816	- N2 Cross-counselor negative test: ✓ 通过
  1817	
  1818	**状态：**
  1819	- ✅ Step 1.0完成
  1820	- ✅ Step 1完成
  1821	- ✅ Step 2完成
  1822	- ⏭ 下一步：Step 3（部署文档补漏）或与Codex讨论优化
  1823	
  1824	**Step 2: API文档基线（已完成）：**
  1825	- ✓ 引入drf-spectacular（v0.27.1）
  1826	- ✓ 配置settings.py（INSTALLED_APPS + REST_FRAMEWORK + SPECTACULAR_SETTINGS）
  1827	- ✓ 添加schema和Swagger UI路由
  1828	- ✓ 验证基线可访问（/api/schema/ + /api/schema/swagger-ui/）
  1829	- ✓ 验证端点清单（15个端点）
  1830	- ✓ 验证JWT Bearer认证可见
  1831	- ✓ 创建待完善清单（docs/api/api-schema-todo.md）
  1832	
  1833	**产出物：**
  1834	- backend/requirements/base.txt（添加drf-spectacular==0.27.1）
  1835	- backend/config/settings/base.py（配置drf-spectacular）
  1836	- backend/config/urls.py（添加schema路由）
  1837	- docs/api/api-schema-todo.md（待完善清单：13个function-based views需extend_schema）
  1838	
  1839	**验收结果：**
  1840	- /api/schema/: HTTP 200 ✓
  1841	- /api/schema/swagger-ui/: HTTP 200 ✓
  1842	- 端点数量: 13条path/15个operation ✓
  1843	- JWT认证: Bearer JWT ✓
  1844	- 生成器警告: 已记录到待完善清单 ✓
  1845	
  1846	**Step 3: 部署文档补漏（已完成）：**
  1847	- ✓ 补充DEPLOYMENT.md环境变量表（基于settings.py实际读取的9个变量）
  1848	- ✓ 补充DEPLOYMENT.md故障排查指南（覆盖8个真实场景）
  1849	- ✓ 修正api-schema-todo.md表述（13条path/15个operation，修正mark-as-read路径）
  1850	- ✓ 更新PROJECT-SUMMARY.md标记Option E-lite完成
  1851	
  1852	**产出物：**
  1853	- DEPLOYMENT.md（环境变量表 + 扩展故障排查指南）
  1854	- docs/api/api-schema-todo.md（修正表述）
  1855	
  1856	**验收结果：**
  1857	- 环境变量表: 9个变量，区分必填/默认值/生产建议 ✓
  1858	- 故障排查指南: 覆盖409/422/401/403/media/Docker/数据库/schema场景 ✓
  1859	- api-schema-todo.md: 修正path/operation表述和mark-as-read路径 ✓
  1860	
  1861	**Option E-lite总结（已完成）：**
  1862	- ✅ Step 1.0: Smoke可重复运行门禁
  1863	- ✅ Step 1: Smoke增强（通知验证 + H2驳回场景 + attachment修复）
  1864	- ✅ Step 2: API文档基线（drf-spectacular + 13条path/15个operation + 待完善清单）
  1865	- ✅ Step 3: 部署文档补漏（环境变量表 + 故障排查指南）
  1866	
  1867	**执行约束遵守情况：**
  1868	- ✓ 未承诺完整API schema（P1/P2待完善项已记录到api-schema-todo.md）
  1869	- ✓ 未无条件自动重置数据库（SMOKE_RESET=1为可选开关）
  1870	- ✓ 硬停止于Step 3完成（后续工作需新任务明确）
  1871	
  1872	**状态：**
  1873	- ✅ Option E-lite完成
  1874	- ⏸ API schema P1/P2完善留待后续Phase
  1875	- ⏸ 下一步工作需与Codex讨论或用户明确指示

exec
/bin/bash -lc "rtk rg -n \"15个端点|13条path|mark_as_read|notifications/\\{notification_id\\}/read|Option E-lite完成|Step 3\" docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md docs/api/api-schema-todo.md docs/PROJECT-SUMMARY.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/api/api-schema-todo.md:12:✓ 13条path/15个operation出现在schema中  
docs/api/api-schema-todo.md:24:- `/api/notifications/{notification_id}/read/` - mark_as_read
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:7:**结论：** 支持 Option D，但 Step 3 需要小幅收紧验收口径
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:13:我支持 Claude 推荐的 **Option D：完成 Step 3 后结束 Option E-lite**。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:17:但 Step 3 不应只是补几段通用说明。它应该做成一个 **小而准确的部署/运行手册收口**：环境变量表必须来自实际 settings 使用情况，故障排查必须对应当前 API 行为和 smoke 失败形态，最后再更新项目总结，把 Option E-lite 标记为完成。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:35:- `tests/smoke_test.sh` 中有一处输出使用未赋值变量 `STUDENT_NOTIF_COUNT`。当前脚本没有 `set -u`，不会导致失败，但这属于清理项。可在 Step 3 后或下一轮测试清理时顺手修。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:50:- `docs/api/api-schema-todo.md` 中 notification mark-as-read 路径写成 `/api/notifications/mark_as_read/`，实际路由和 schema 是 `/api/notifications/{notification_id}/read/`。Step 3 或收尾时应修正这个清单。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:58:1. Step 3.1：补 `DEPLOYMENT.md` 环境变量表。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:59:2. Step 3.2：补 `DEPLOYMENT.md` 故障排查指南。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:60:3. Step 3.3：修正 API schema todo 中“13 path / 15 operation”和 mark-as-read 路径表述。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:61:4. Step 3.4：更新 `docs/PROJECT-SUMMARY.md`，明确 Option E-lite 完成，并把 API schema P1/P2 留到后续 phase。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:65:不建议单独执行 Option C 作为当前主线。smoke 连跑稳定性有价值，但会带来 Docker 重置和时间不确定性；如果要做，可以作为 Step 3 之后的可选验证，不作为结束 Option E-lite 的阻塞门。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:69:## 对 Step 3 执行计划的审查意见
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:88:注意：`.env.example` 中包含 `JWT_SECRET_KEY`、`JWT_ACCESS_TOKEN_LIFETIME`、`JWT_REFRESH_TOKEN_LIFETIME`、`MEDIA_ROOT`、`MEDIA_URL`、`REDIS_*`、`CELERY_*`，但当前 settings 没有实际读取这些变量。Step 3 不要把它们写成“生产必填”。更好的处理是：
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:91:- 或者顺手更新 `.env.example`，但这会扩大 Step 3 范围；如果只做文档，至少不要误导部署者。
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:108:Step 3 完成后建议验收为：
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:119:执行 Option D。Step 3 完成后应硬停止 Option E-lite，把后续工作拆成新的明确任务：
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:125:当前最优路径是先完成 Step 3 收口，不把 API schema 精修或新业务功能混入本轮。
docs/PROJECT-SUMMARY.md:920:- ✓ Step 3: 修复skeleton gaps（反映现有文件、添加学生主页gap）
docs/PROJECT-SUMMARY.md:1612:  - test_mark_as_read
docs/PROJECT-SUMMARY.md:1613:  - test_mark_as_read_idempotent
docs/PROJECT-SUMMARY.md:1614:  - test_mark_as_read_forbidden
docs/PROJECT-SUMMARY.md:1615:  - test_mark_as_read_not_found
docs/PROJECT-SUMMARY.md:1697:**Step 3: 自动通知测试（45分钟）**
docs/PROJECT-SUMMARY.md:1733:- Step 3（测试）：~45分钟
docs/PROJECT-SUMMARY.md:1822:- ⏭ 下一步：Step 3（部署文档补漏）或与Codex讨论优化
docs/PROJECT-SUMMARY.md:1829:- ✓ 验证端点清单（15个端点）
docs/PROJECT-SUMMARY.md:1842:- 端点数量: 13条path/15个operation ✓
docs/PROJECT-SUMMARY.md:1846:**Step 3: 部署文档补漏（已完成）：**
docs/PROJECT-SUMMARY.md:1849:- ✓ 修正api-schema-todo.md表述（13条path/15个operation，修正mark-as-read路径）
docs/PROJECT-SUMMARY.md:1850:- ✓ 更新PROJECT-SUMMARY.md标记Option E-lite完成
docs/PROJECT-SUMMARY.md:1864:- ✅ Step 2: API文档基线（drf-spectacular + 13条path/15个operation + 待完善清单）
docs/PROJECT-SUMMARY.md:1865:- ✅ Step 3: 部署文档补漏（环境变量表 + 故障排查指南）
docs/PROJECT-SUMMARY.md:1870:- ✓ 硬停止于Step 3完成（后续工作需新任务明确）
docs/PROJECT-SUMMARY.md:1873:- ✅ Option E-lite完成
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:38:- 15个端点出现在schema中 ✓
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:54:### Option A: 按原计划执行Step 3（部署文档补漏）
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:121:### Option D: 完成Step 3后结束Option E-lite
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:124:- 执行Step 3（部署文档补漏）
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:125:- 更新PROJECT-SUMMARY.md记录Option E-lite完成
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:144:**推荐：Option D（完成Step 3后结束Option E-lite）**
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:147:1. **遵循原定计划：** Option E-lite的目标是"Smoke增强 + API文档基线 + 部署文档补漏"，Step 3是最后一步
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:148:2. **时间可控：** Step 3估算0.5小时，风险低
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:152:**Step 3执行计划：**
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:181:3. Option D（完成Step 3后结束Option E-lite）是否合理？
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:182:4. Step 3的执行计划是否可行？
docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:188:- 对Step 3执行计划的审查意见

exec
/bin/bash -lc "rtk jq '{path_count:(.paths|length), operation_count:([.paths[]|keys[]|select(test(\""'^(get|post|put|patch|delete)$"))]|length), bearer:(.components.securitySchemes.JWTAuth // .components.securitySchemes.jwtAuth // .components.securitySchemes.Bearer // .components.securitySchemes.bearer)}'"' /tmp/schema-check.json" in /home/caohui/projects/graduation-leave-system
 exited 5 in 0ms:
jq: parse error: Invalid numeric literal at line 1, column 8


exec
/bin/bash -lc 'rtk head -c 200 /tmp/schema-check.json' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
openapi: 3.0.3
info:
  title: 毕业生离校申请审批系统 API
  version: 1.0.0
  description: 毕业生离校申请审批系统后端API文档
paths:
  /api/applications/:
    get:
      operati
exec
/bin/bash -lc "rtk sed -n '118,150p' backend/config/settings/base.py && rtk sed -n '1,40p' backend/config/urls.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 161ms:
"""URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/', include('apps.attachments.urls')),
    path('api/applications/', include('apps.applications.urls')),
    path('api/approvals/', include('apps.approvals.urls')),
    path('api/notifications/', include('apps.notifications.urls')),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

exec
/bin/bash -lc "rtk python -c \"import yaml; d=yaml.safe_load(open('/tmp/schema-check.json')); ops=sum(1 for p in d['paths'].values() for k in p if k in {'get','post','put','patch','delete'}); print({'path_count': len(d['paths']), 'operation_count': ops, 'securitySchemes': d.get('components',{}).get('securitySchemes',{})})\"" in /home/caohui/projects/graduation-leave-system
 exited 127 in 0ms:
[rtk: No such file or directory (os error 2)]

exec
/bin/bash -lc "rtk proxy python -c \"import yaml; d=yaml.safe_load(open('/tmp/schema-check.json')); ops=sum(1 for p in d['paths'].values() for k in p if k in {'get','post','put','patch','delete'}); print({'path_count': len(d['paths']), 'operation_count': ops, 'securitySchemes': d.get('components',{}).get('securitySchemes',{})})\"" in /home/caohui/projects/graduation-leave-system
 exited 1 in 0ms:
rtk: Failed to execute command: python: No such file or directory (os error 2)

exec
/bin/bash -lc "rtk proxy python3 -c \"import yaml; d=yaml.safe_load(open('/tmp/schema-check.json')); ops=sum(1 for p in d['paths'].values() for k in p if k in {'get','post','put','patch','delete'}); print({'path_count': len(d['paths']), 'operation_count': ops, 'securitySchemes': d.get('components',{}).get('securitySchemes',{})})\"" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{'path_count': 13, 'operation_count': 15, 'securitySchemes': {'jwtAuth': {'type': 'http', 'scheme': 'bearer', 'bearerFormat': 'JWT'}}}

codex
已审查 `47`。仓库里已经有对应 Codex 响应：[48-codex-post-step2-next-strategy-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md)，结论我认可：**支持 Option D，完成 Step 3 后硬停止 Option E-lite**。

我又核验了当前状态：

- `/api/schema/`：HTTP 200
- `/api/schema/swagger-ui/`：HTTP 200
- schema 实际为 `13 paths / 15 operations`，JWT Bearer 可见
- [DEPLOYMENT.md](/home/caohui/projects/graduation-leave-system/DEPLOYMENT.md:87) 已补环境变量表和故障排查
- [api-schema-todo.md](/home/caohui/projects/graduation-leave-system/docs/api/api-schema-todo.md:12) 已修正为 `13条path/15个operation`，mark-as-read 路径也已正确
- [PROJECT-SUMMARY.md](/home/caohui/projects/graduation-leave-system/docs/PROJECT-SUMMARY.md:1846) 已标记 Step 3 和 Option E-lite 完成

剩余小问题不阻塞收尾：

- [PROJECT-SUMMARY.md](/home/caohui/projects/graduation-leave-system/docs/PROJECT-SUMMARY.md:1829) 仍有一处写“15个端点”，建议改成“13条path/15个operation”。
- [smoke_test.sh](/home/caohui/projects/graduation-leave-system/tests/smoke_test.sh:255) 输出了未赋值的 `STUDENT_NOTIF_COUNT`，当前不会失败，但应后续清理。
- 通知验证主要按 message 内容过滤，不是严格按当前实体 id 过滤；在 `SMOKE_RESET=1` 下可接受，但不要把它表述成实体级隔离验证。

建议：Option E-lite 可以关闭。下一轮单独开任务处理 API Schema P1，或先做 smoke 清理。
tokens used
63,342

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
