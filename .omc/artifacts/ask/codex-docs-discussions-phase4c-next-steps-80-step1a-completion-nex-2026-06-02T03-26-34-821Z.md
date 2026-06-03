# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-02T03:26:34.821Z

## Original task

docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md

## Final prompt

docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md

## Raw output

```text
已完成 Codex 审查响应，写入：

[81-step1a-completion-codex-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md)

核心结论：Step 1A 作为“签名函数切片”可通过，无 P0；建议补强 MD5 固定期望值测试。下一步不建议先写孤立 Step 1C 诊断脚本，建议先做窄版 Step 1B-lite，让诊断脚本复用客户端的请求构造、签名、脱敏和错误分类逻辑。

验证结果：host 缺 Django，无法跑本地测试；Docker 中运行 `apps.users.tests.test_xg_user_client` 通过，4/4 passed。协作日志已追加 event 100，state 已更新为等待 Claude 响应。


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
session id: 019e865a-ac8c-7951-9f3f-e8aa90d46219
--------
user
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md
codex
I’ll inspect the referenced discussion file and the project protocols first, since this looks like a rule-governed review request.
exec
/bin/bash -lc "sed -n '1,240p' docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Step 1A完成审查与下一步策略讨论

**文档编号：** 80  
**创建时间：** 2026-06-02  
**审查类型：** 实现审查 + 策略讨论  
**审查者：** Codex

---

## 审查目标

1. **Step 1A实现审查**：审查签名生成函数实现质量
2. **测试覆盖评估**：评估当前测试充分性
3. **下一步策略讨论**：Step 1B（请求构建）vs Step 1C（诊断脚本）优先级
4. **优化建议**：识别潜在改进点

---

## Step 1A完成状态

### 实现文件

1. **backend/apps/users/integrations/__init__.py**
   - 导出 `generate_sign` 和 `XGUserAPIClient`

2. **backend/apps/users/integrations/xg_user_client.py**
   - `generate_sign()` 函数：支持SHA1/MD5签名生成
   - 字典排序 → 拼接 → 加密
   - `XGUserAPIClient` 类（占位符，待实现）

3. **backend/apps/users/tests/test_xg_user_client.py**
   - 官方签名样例测试（P0需求）
   - MD5加密测试
   - 非法加密类型测试
   - 测试结果：4/4 passed (0.007s)

4. **backend/.env.example**
   - 配置环境变量模板
   - 包含租户Code S10405
   - 添加测试开关 `XG_RUN_LIVE_API_TEST`

### 同步修复

修复了4个视图文件的导入错误：
- backend/apps/attachments/views.py
- backend/apps/notifications/views.py
- backend/apps/applications/views.py
- backend/apps/approvals/views.py

修改：`from backend.schema import` → `from schema import`

---

## 审查要点

### 1. 代码质量审查

**请审查以下文件：**
- backend/apps/users/integrations/xg_user_client.py
- backend/apps/users/tests/test_xg_user_client.py

**审查维度：**
- 签名算法实现是否严格遵循官方规范？
- 类型注解使用是否恰当？
- 错误处理是否充分？
- 是否存在安全隐患？

### 2. 测试充分性评估

**当前测试覆盖：**
- ✅ 官方签名样例验证
- ✅ 默认SHA1加密
- ✅ MD5加密
- ✅ 非法加密类型

**缺失测试场景（疑问）：**
- 是否需要测试空字符串参数？
- 是否需要测试特殊字符处理？
- 是否需要测试Unicode字符？

### 3. 下一步策略讨论

**Codex在doc 77中建议的分段策略：**
- ✅ **Step 1A（已完成）**：签名生成函数 + 单元测试
- ⏳ **Step 1B（待定）**：请求构建（headers + form data + fetch逻辑）+ Mock测试
- ⏳ **Step 1C（待定）**：诊断脚本（环境检查 + 实际请求日志）

**策略问题：**

1. **优先级选择：**
   - 选项A：直接进入Step 1B（请求构建），完成后再做Step 1C
   - 选项B：先做Step 1C（诊断脚本），快速验证网络连通性，再做Step 1B
   - 选项C：并行开发Step 1B和Step 1C

2. **Step 1B范围确认：**
   - 是否需要实现完整的分页逻辑？
   - 是否需要实现重试机制？
   - Mock测试应覆盖哪些场景？

3. **Step 1C诊断需求：**
   - 诊断脚本应检查哪些环境条件？
   - 是否需要记录完整的请求/响应日志？
   - 是否需要支持命令行参数？

---

## Claude的初步建议

**倾向选项B（先Step 1C后Step 1B）：**

**理由：**
1. **风险优先**：租户Code S10405是新配置，需先验证网络连通性和API可达性
2. **快速反馈**：诊断脚本可在5-10分钟内开发完成，快速暴露问题
3. **减少返工**：如果Step 1B完成后才发现网络问题，需要回退调试

**Step 1C诊断脚本建议范围：**
- 环境变量读取验证
- 签名生成测试（使用真实配置）
- 单次请求尝试（POST到真实API）
- 记录完整请求headers和响应（用于调试）
- 不需要分页逻辑，不需要数据解析

**预期输出：**
- 成功：HTTP 200 + 响应body预览
- 失败：错误代码 + 响应body + 调试建议

---

## 请Codex审查并回答

1. **Step 1A实现是否有改进空间？**
   - 代码质量问题
   - 测试缺失场景
   - 安全隐患

2. **是否同意选项B（先Step 1C后Step 1B）？**
   - 如不同意，理由是什么？
   - 是否有更优策略？

3. **Step 1C诊断脚本范围是否合理？**
   - 是否需要增加/删减功能？
   - 输出格式建议

4. **Step 1B的具体范围边界在哪里？**
   - 应包含哪些功能？
   - 应排除哪些功能（留给后续步骤）？

---

**期望输出格式：**

```markdown
## 1. Step 1A审查结果
[P0/P1/P2问题列表]

## 2. 下一步策略建议
[选项A/B/C + 理由]

## 3. Step 1C范围确认
[功能清单 + 优先级]

## 4. Step 1B范围界定
[包含功能 + 排除功能]
```

exec
/bin/bash -lc "sed -n '1,260p' docs/codex-review-protocol.md" in /home/caohui/projects/graduation-leave-system
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

codex
The request asks for a formal Codex review response. I’ve loaded the local review protocol and collaboration contract; next I’m checking the actual implementation, tests, and current shared-state expectations before writing the review artifact.
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
 M backend/apps/notifications/services.py
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
?? docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md
?? docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md
?? docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md
?? docs/discussions/phase4c-next-steps/53-codex-confirmation-option-a-corrected.md
?? docs/discussions/phase4c-next-steps/54-claude-codex-consensus-option-a-execution.md
?? docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md
?? docs/discussions/phase4c-next-steps/59-claude-codex-final-consensus-option-2.md
?? docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md
?? docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md
?? docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md
?? docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md
?? docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md
?? docs/discussions/phase4c-next-steps/69-claude-post-phase2b-step1-next-strategy.md
?? docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md
?? docs/discussions/phase4c-next-steps/71-claude-response-accept-b-mini.md
?? docs/discussions/phase4c-next-steps/72-claude-codex-consensus-phase2b-step2-strategy.md
?? docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md
?? docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md
?? docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md
?? docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md
?? docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md
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
exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/users/tests/test_xg_user_client.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
"""学工系统用户API客户端测试"""
from django.test import TestCase
from apps.users.integrations.xg_user_client import generate_sign


class GenerateSignTests(TestCase):
    """签名生成函数测试"""

    def test_official_sample_sha1(self):
        """测试官方签名样例（sha1）"""
        app_secret = '6bd1b3fb015b4e72a85769e9d64405d1'
        timestamp = '1573702840'
        rand_str = 'Gc6LGToDKy2AMhXE'

        sign = generate_sign(app_secret, timestamp, rand_str, 'sha1')

        self.assertEqual(sign, 'baeaa6693fb7b9914c9ff9e388654878b8754515')

    def test_official_sample_default_sha1(self):
        """测试官方样例（默认sha1）"""
        sign = generate_sign(
            '6bd1b3fb015b4e72a85769e9d64405d1',
            '1573702840',
            'Gc6LGToDKy2AMhXE'
        )
        self.assertEqual(sign, 'baeaa6693fb7b9914c9ff9e388654878b8754515')

    def test_md5_encryption(self):
        """测试md5加密"""
        sign = generate_sign('secret', '1234567890', 'random', 'md5')
        # 验证返回32位hex字符串
        self.assertEqual(len(sign), 32)
        self.assertTrue(all(c in '0123456789abcdef' for c in sign))

    def test_invalid_encryption_type(self):
        """测试非法加密类型"""
        with self.assertRaises(ValueError) as cm:
            generate_sign('secret', '1234567890', 'random', 'sha256')
        self.assertIn("must be 'sha1' or 'md5'", str(cm.exception))

exec
/bin/bash -lc "rtk sed -n '1,240p' backend/apps/users/integrations/xg_user_client.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
"""学工系统用户API客户端"""
import hashlib
from typing import Literal


def generate_sign(
    app_secret: str,
    timestamp: str,
    rand_str: str,
    encryption_type: Literal['sha1', 'md5'] = 'sha1'
) -> str:
    """
    生成API签名

    签名规则：
    1. 将appSecret, timestamp, randStr三个参数值进行字典排序
    2. 拼接成字符串
    3. 进行sha1或md5加密

    Args:
        app_secret: AppSecret密钥
        timestamp: Unix时间戳（字符串）
        rand_str: 随机字符串
        encryption_type: 加密类型，'sha1'或'md5'，默认'sha1'

    Returns:
        签名字符串（十六进制小写）
    """
    if encryption_type not in ('sha1', 'md5'):
        raise ValueError(f"encryption_type must be 'sha1' or 'md5', got '{encryption_type}'")

    # 1. 字典排序
    params = [app_secret, timestamp, rand_str]
    params.sort()

    # 2. 拼接
    sign_str = ''.join(params)

    # 3. 加密
    if encryption_type == 'md5':
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    else:
        return hashlib.sha1(sign_str.encode('utf-8')).hexdigest()


class XGUserAPIClient:
    """学工系统用户API客户端（待实现）"""
    pass

exec
/bin/bash -lc "rtk sed -n '260,520p' .omc/collaboration/protocol.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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

## 14. Agent Roles

This protocol supports three-agent collaboration: Claude, Codex, and Gemini. Each agent has distinct strengths and default responsibilities.

### Claude

**Primary role:** Orchestrator, synthesizer, user communication.

**Strengths:**
- Requirements clarification and user interaction
- Cross-domain synthesis and decision-making
- Documentation and narrative writing
- Coordinating multi-agent workflows

**Typical tasks:**
- Creating task specifications
- Synthesizing independent analyses from multiple agents
- Writing user-facing documentation
- Making final decisions when agents disagree
- Protocol updates and governance

### Codex

**Primary role:** Implementer, reviewer, validator.

**Strengths:**
- Code implementation and debugging
- Technical review and validation
- Protocol compliance verification
- Executable testing and mechanical validation

**Typical tasks:**
- Implementing features and fixes
- Reviewing code for correctness and security
- Validating protocol adherence
- Writing and running tests
- Mechanical backpressure (compile, lint, type-check)

### Gemini

**Primary role:** Analyst (read-only by default).

**Strengths:**
- Large-context analysis (long documents, logs, codebases)
- Multi-file scanning and pattern detection
- Third-party project analysis
- Historical data review

**Typical tasks:**
- Analyzing large log files or traces
- Scanning entire codebases for patterns
- Reviewing long documents or specifications
- Comparing multiple implementations
- Extracting insights from large datasets

**Default constraint:** Gemini operates in read-only mode unless the user explicitly authorizes write access. Gemini outputs artifacts to `.omc/collaboration/artifacts/` and does not directly modify repository files.

**Write access exception:** If the user explicitly requests Gemini to modify code, use git worktree isolation or patch artifacts to avoid conflicts with Claude/Codex work.

### Role Selection Guidelines

When a task could be handled by multiple agents:

1. **User communication or synthesis:** Claude
2. **Code implementation or review:** Codex
3. **Large-context analysis:** Gemini
4. **Ambiguous or multi-faceted:** Assign to Claude for coordination, or request independent analyses from multiple agents

Agents may delegate subtasks to other agents when appropriate. The delegating agent remains responsible for integrating the results.

## 15. Independent Analysis Protocol

When a task requires independent perspectives to avoid anchoring bias or groupthink, use this protocol.

### Triggering Independent Analysis

A task enters independent analysis mode when:

1. The task document explicitly requests "independent analysis" or "separate analyses"
2. The user requests multiple agents to analyze the same problem independently
3. The task creator marks the task with `status: open_for_collaboration`

### Independent Analysis Rules

When performing independent analysis:

1. **Do not read artifacts from other agents on the same topic.** Each agent must form their own conclusions based on source materials only.

2. **Declare independence in your artifact.** Include a clear statement: "Independent analysis - did not read [other agent names] artifacts."

3. **Create your own artifact.** Use the standard naming convention: `YYYYMMDD-HHMM-agent-topic.md`

4. **Log your completion.** Append an event indicating independent analysis completion.

### Status Extensions

The following status values support independent analysis workflows:

- `open_for_collaboration`: Task is open for multiple agents to work in parallel. No exclusive ownership.
- `waiting_synthesis`: All independent analyses are complete. Waiting for designated agent to create synthesis.

### Event Type Extensions

The following event types support independent analysis workflows:

- `collaboration_opened`: Task opened for multi-agent parallel work
- `independent_analysis_completed`: Agent completed their independent analysis
- `synthesis_requested`: Request for designated agent to synthesize multiple analyses
- `synthesis_completed`: Synthesis artifact created

### Synthesis Ownership

After all independent analyses are complete, one agent must create a synthesis or comparison document. Ownership priority:

1. **User-specified:** If the task document names a synthesis owner, that agent is responsible.
2. **Task creator:** The agent who created the task synthesizes, as they understand the original intent.
3. **Third-party agent:** If the task creator also performed independent analysis, a non-participating agent synthesizes to maintain objectivity.
4. **Fallback:** If no clear owner exists, the last completing agent creates a comparison document listing agreements and disagreements, then requests user decision.

### Synthesis Requirements

A synthesis document must:

- Reference all independent analysis artifacts
- Identify areas of agreement and disagreement
- Provide reasoning for recommended conclusions
- Highlight unresolved questions requiring user input
- Propose next steps or action items

### Example Workflow

1. Claude creates task: "Analyze approach X independently"
2. Claude appends `collaboration_opened` event, sets `status: open_for_collaboration`
3. Codex claims task, performs analysis, creates artifact, appends `independent_analysis_completed` event
4. Gemini claims task, performs analysis, creates artifact, appends `independent_analysis_completed` event
5. Claude (task creator) synthesizes both analyses, creates synthesis artifact
6. Claude appends `synthesis_completed` event, sets `status: completed`


codex
The implementation is small and the worktree is already heavily dirty with user/project changes, so I’ll keep this to review artifacts only. I’m now looking for the surrounding API notes/spec references so the review can judge the signature behavior against documented context, not just the code.
exec
/bin/bash -lc "rtk sed -n '1,220p' AGENTS.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Project Agent Instructions

## Mandatory Project Rules

- For every shell command in this project, follow `/home/caohui/.codex/RTK.md`.
- When participating in the Claude-Codex collaboration workflow, read and follow `.omc/collaboration/protocol.md` before acting. Treat it as the project-local contract for task execution, artifact generation, event logging, and shared state management.
- Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.
- If `docs/codex-review-protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.
- Do not treat review-protocol steps as optional when the user requests a formal review or rule-governed Codex discussion.
- If `.omc/collaboration/protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.

exec
/bin/bash -lc "rtk sed -n '1,220p' .omc/collaboration/state.json" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{
  "workflow_id": "claude-codex-collab-mvp",
  "current_task": "phase4c_next_steps",
  "active_agent": "claude",
  "status": "waiting_for_claude_response",
  "last_event_id": 99,
  "updated_at": "2026-06-02T03:08:57.327738096Z"
}

exec
/bin/bash -lc 'rtk tail -n 40 .omc/collaboration/events.jsonl' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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
{"id":73,"type":"review_response","agent":"codex","timestamp":"2026-06-01T04:06:28.001601Z","summary":"Codex reviewed Claude revised test coverage plan and accepted it with narrowed executable scope.","task_id":"phase4b_implementation","artifacts":[".omc/collaboration/artifacts/20260601-0405-codex-test-coverage-feedback.md"],"status":"in_progress","details":{"decision":"accept_with_scope_reductions","time_estimate":"0.6 day target, 0.7 day buffer","include_timezone":"merge two deterministic serializer boundary tests","state_machine_scope":"sequential API logic only, no real concurrency"}}
{"id":74,"type":"review_response","agent":"codex","timestamp":"2026-06-01T07:04:16.131422Z","summary":"Codex reviewed Claude Phase 4C strategy proposal and recommended contract/RBAC decision gate before tests.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md"],"status":"waiting","details":{"decision":"needs_modification_before_execution","recommended_order":["contract_skeleton","p0_implementation_fixes","focused_attachment_tests","regression","contract_v0_3_final"],"key_risks":["inconsistent_attachment_rbac","missing_file_storage_handling","missing_media_settings","validation_details_dropped"]}}
{"id":75,"type":"review_response","agent":"codex","timestamp":"2026-06-01T07:43:32.243Z","summary":"Codex reviewed Claude Phase 4C next-step options and recommended narrowed Option A-lite with DevTools as acceptance gate.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md"],"status":"waiting","details":{"decision":"proceed_with_narrowed_option_a_lite","recommendation":"detail page attachment hub, post-submit upload, dedicated upload/download API methods","completion_gate":"DevTools validation required for accepted completion","parallel_work":["dorm system discovery","frontend validation checklist"]}}
{"id":76,"type":"review_response","agent":"codex","timestamp":"2026-06-01T08:18:04.291088Z","summary":"Codex reviewed Phase 4C Phase 2 miniprogram attachment implementation and identified list response shape as a P0 blocker.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/09-codex-phase2-implementation-review-response.md"],"status":"waiting","details":{"decision":"needs_modification_before_wxss_completion","p0":"Attachment list backend returns bare array while miniprogram client expects {attachments: [...]}.","next_steps":["fix list response shape","reconcile contract/type fields","then finish WXSS and static validation"]}}
{"id":77,"type":"review_response","agent":"codex","timestamp":"2026-06-01T09:07:07.947261Z","summary":"Codex reviewed Claude Phase 4C P1 fix plan and required contract field-drift cleanup plus shared unauthorized handling.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/12-codex-p1-fixes-review-response.md"],"status":"waiting","details":{"decision":"needs_small_modification_before_execution","required_changes":["extend field drift fix to docs/api/contract-v0.3.md","make attachment error and empty states mutually exclusive","reuse ApiClient unauthorized handling for download 401","add extension precheck aligned with backend"]}}
{"id":78,"type":"review_response","agent":"codex","timestamp":"2026-06-01T09:56:55.614761Z","summary":"Codex accepted Claude Phase 4C P0 multipart parser fix; explicit attachment backend suite passes 19/19 and WXSS may continue.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md"],"status":"waiting","details":{"decision":"accepted","tests":"19/19 attachment backend tests passed","remaining_work":["WXSS styling","static validation","WeChat DevTools acceptance"]}}
{"id":79,"type":"review_response","agent":"codex","timestamp":"2026-06-01T10:16:52.564166Z","summary":"Codex reviewed Claude Phase 4C post-completion strategy and recommended a narrowed backend/ops hardening mix before new miniprogram pages.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md"],"status":"waiting","details":{"decision":"conditional_agreement_with_narrowed_mixed_strategy","priority_order":["csv_import_v1_hardening","docker_media_smoke_hardening","acceptance_evidence_pack","notification_contract_optional"],"frontend_scope":"freeze_new_miniprogram_pages_until_devtools_validation"}}
{"event_id":80,"timestamp":"2026-06-01T10:18:00Z","agent":"claude","event_type":"consensus_reached","description":"Claude完全接受Codex修正版E策略：后端/运维硬化优先的窄混合策略","details":{"strategy":"两条主线并行：CSV导入v1硬化 + Docker/media/smoke验收硬化","milestones":["M1: Backend Ops Hardening (1-2天)","M2: Phase 4C Evidence Ready (0.5-1天)","M3: Notification Contract (0.5天,可选)"],"frozen_scope":"小程序保持冻结直到DevTools验证","document":"docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md"}}
{"event_id":81,"timestamp":"2026-06-01T14:23:00Z","agent":"claude","event_type":"execution_completed","data":{"task":"backend_ops_hardening","tracks":["track1_csv_import_v1","track2_docker_media_smoke"],"milestones":["M1_backend_ops_hardening_complete","M2_phase4c_evidence_ready"],"tests_passed":"9/9 CSV import + 15-step smoke test","commits":2,"status":"ready_for_next_phase"}}
{"id":82,"type":"review_response","agent":"codex","timestamp":"2026-06-01T14:27:13.59467565Z","summary":"Codex reviewed Claude post-execution next steps and recommended a narrowed A+C evidence-closure pass followed by hard stop.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/23-codex-post-execution-next-steps-response.md"],"status":"waiting","details":{"decision":"accept_narrowed_A_plus_C","track3":"defer_unless_user_authorizes_or_devtools_remains_unavailable_after_evidence_pack","hard_stop":"after_phase4c_evidence_closure"}}
{"id":83,"type":"review_response","agent":"codex","timestamp":"2026-06-01T14:46:33.781Z","summary":"Codex reviewed Claude post-evidence next strategy and recommended a user decision gate plus contract-only Track 3 draft if authorized.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md"],"status":"waiting","details":{"decision":"do_not_start_track3_backend_implementation_without_explicit_authorization","allowed_next_internal_work":"notification_contract_draft_only","preferred_gate":["wechat_devtools_validation","dorm_system_info_collection","notification_contract_draft"]}}
{"event_id":84,"timestamp":"2026-06-01T14:55:00Z","agent":"claude","type":"consensus_reached","task":"phase4c_next_steps","description":"Claude-Codex达成共识：决策门+窄Track 3契约草案（仅文档）","artifacts":["docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md","docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md","docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md"]}
{"event_id":85,"timestamp":"2026-06-01T15:00:00Z","agent":"claude","type":"task_completed","task":"track3_phase0_notification_contract","description":"Track 3 Phase 0完成：通知契约草案v0.1（纯文档，5种事件+10字段+4 API+RBAC+幂等规则）","artifacts":["docs/api/notification-contract-v0.1.md"]}
{"id":86,"type":"review_response","agent":"codex","timestamp":"2026-06-01T15:30:00.000Z","summary":"Codex reviewed Claude post-Phase0 Track 3 strategy and rejected implicit Phase 1 authorization, recommending a contract-fix decision gate.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md"],"status":"waiting","details":{"decision":"do_not_start_phase1_without_explicit_authorization","recommended_next":"decision_gate_with_contract_fix_default","phase1_scope_if_authorized":"model_migration_read_api_rbac_tests_no_signals"}}
{"event_id":87,"timestamp":"2026-06-01T15:40:54Z","agent":"claude","type":"task_completed","task":"track3_contract_revision","description":"Track 3契约修正完成：5个P1/P2问题已修正（分页/幂等键/验收标准/错误结构/测试数据）","artifacts":["docs/api/notification-contract-v0.1.md","docs/discussions/phase4c-next-steps/28-claude-post-phase0-next-strategy.md","docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md","docs/discussions/phase4c-next-steps/30-claude-consensus-contract-revision-gate.md"],"status":"completed"}
{"id":88,"type":"review_response","agent":"codex","timestamp":"2026-06-01T15:47:10.984630Z","summary":"Codex reviewed Claude Track 3 post-contract strategy and kept Phase 1 behind explicit user authorization while approving the bounded implementation scope if authorized.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md"],"status":"waiting","details":{"decision":"do_not_start_phase1_without_explicit_authorization","phase1_scope_if_authorized":"model_migration_read_api_rbac_tests_seed_command_no_signals","recommended_gate":["authorize_phase1_backend_mvp","pause_for_external_blockers"]}}
{"event_id":89,"timestamp":"2026-06-01T15:52:00Z","agent":"claude","type":"consensus_reached","task":"phase4c_next_steps","description":"Claude完全接受Codex授权门决策：硬停止，等待用户明确授权Phase 1或选择等待外部阻塞项","artifacts":["docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md","docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md","docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md"],"details":{"decision":"accept_authorization_gate","gate_options":["authorize_phase1_backend_mvp","pause_for_external_blockers"]}}
{"id":90,"type":"review_response","agent":"codex","timestamp":"2026-06-01T15:56:00.000Z","summary":"Codex interpreted the fourth continue-and-execute instruction as not constituting explicit Track 3 Phase 1 authorization and recommended a minimal user confirmation gate.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/35-codex-authorization-interpretation-response.md"],"status":"waiting_for_user_decision","details":{"decision":"does_not_constitute_explicit_phase1_authorization","recommended_next":"ask_user_to_choose_option_1_authorize_phase1_or_option_2_wait_external_blockers","phase1_scope_if_authorized":"model_migration_read_api_rbac_tests_seed_command_no_signals"}}
{"event_id":91,"timestamp":"2026-06-01T15:57:00Z","agent":"claude","type":"consensus_reached","task":"phase4c_next_steps","description":"Claude完全接受Codex极简确认建议：不启动Phase 1，向用户呈现极简确认门（选1或选2）","artifacts":["docs/discussions/phase4c-next-steps/34-claude-authorization-interpretation-request.md","docs/discussions/phase4c-next-steps/35-codex-authorization-interpretation-response.md","docs/discussions/phase4c-next-steps/36-claude-consensus-minimal-confirmation.md"],"details":{"decision":"accept_minimal_confirmation_gate","next_action":"present_option_1_or_2_to_user"}}
{"id":92,"type":"review_response","agent":"codex","timestamp":"2026-06-01T16:48:22.187390Z","summary":"Codex reviewed Claude post-Phase2A Track 3 strategy and recommended Phase 2A stabilization plus Option E-lite, deferring Phase 2B/2C.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md"],"status":"waiting_for_claude_response","details":{"decision":"phase2a_stabilization_then_option_e_lite","defer":["phase2b_dorm_clearance_blocked_notification","phase2c_approval_timeout_reminders"],"required_first":["fix_notification_type_enum_drift","add_focused_api_notification_tests"]}}
{"id":93,"type":"review_response","agent":"codex","timestamp":"2026-06-01T17:11:07.123675Z","summary":"Codex reviewed Claude post-Phase2A stabilization Option E-lite strategy and approved execution with smoke repeatability and schema-scope constraints.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md"],"status":"waiting_for_claude_response","details":{"decision":"approve_with_constraints","required_adjustments":["move smoke precondition/reset strategy before smoke assertions","scope OpenAPI baseline to accessible schema, endpoint inventory, auth visibility, and known gaps","avoid unconditional destructive database reset","handle notification entity_id semantics before asserting in smoke"],"verification":"12 notification stabilization tests passed in Docker"}}
{"id":94,"type":"review_response","agent":"codex","timestamp":"2026-06-01T18:13:33.127210Z","summary":"Codex reviewed Claude post Option E-lite next strategy and supported B-mini plus corrected API Schema P1 work.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md"],"status":"waiting_for_claude_response","details":{"decision":"support_option_a_with_required_modifications","recommended_order":["smoke_typo_cleanup","api_schema_p1_corrected"],"adjusted_estimate":"3-4h","key_risks":["login_schema_mismatch","error_envelope_accuracy","multi_method_schema","notification_pagination_shape","attachment_module_ownership"]}}
{"id":95,"type":"review_response","agent":"codex","timestamp":"2026-06-01T18:16:41Z","summary":"Codex confirmed Claude Option A corrected response and authorized B-mini followed by API Schema P1 corrected execution.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/53-codex-confirmation-option-a-corrected.md"],"status":"waiting_for_claude_execution","details":{"decision":"confirmed","authorized_order":["smoke_typo_cleanup","api_schema_p1_corrected"],"clarification":"method-scoped extend_schema is mandatory for multi-method dispatchers; single-method function views need explicit accurate schema metadata and operationIds."}}
{"id":96,"type":"review_response","agent":"codex","timestamp":"2026-06-01T19:09:59.246622Z","summary":"Codex reviewed final Option 2 consensus and approved a narrowed A-lite path with schema-status correction first.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md"],"status":"waiting_for_claude_response","details":{"decision":"approve_option_2_with_modified_a_lite","required_first":["fix_api_schema_todo_status_to_code_complete_unaccepted","resolve_dorm_blocked_notification_contract_entity"],"defer":["phase2c_celery_beat_until_separate_decision"]}}
{"id":97,"type":"review_response","agent":"codex","timestamp":"2026-06-02T02:43:24.553780875Z","summary":"Codex reviewed Claude post Phase 2B Step 1 strategy and recommended B-mini followed by a management-command timeout warning implementation, deferring Celery beat.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md"],"status":"waiting_for_claude_response","details":{"decision":"recommend_b_mini_then_degraded_option_a","recommended_next":["decision_gate_for_timeout_warning_scope","management_command_plus_service_tests"],"defer":["celery_beat","redis_worker_services","repeat_reminders"]}}
{"id":98,"type":"review_response","agent":"codex","timestamp":"2026-06-02T02:59:39.675315935Z","summary":"Codex reviewed the API data reading test plan and required credential redaction/rotation plus official signing and tenant confirmation before live production testing.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md"],"status":"waiting_for_claude_response","details":{"decision":"needs_modification_before_live_api_test","required_first":["redact_and_rotate_exposed_credentials","obtain_official_signing_algorithm_and_tenant_code"],"recommended_scope":"diagnostic_client_plus_mock_tests_no_ci_live_calls"}}
{"id":99,"type":"review_response","agent":"codex","timestamp":"2026-06-02T03:08:57.327738096Z","summary":"Codex reviewed Claude post-Step 0 API test strategy and approved phased diagnostic-client implementation while keeping live calls gated on tenantCode.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md"],"status":"waiting_for_claude_response","details":{"decision":"approve_phased_diagnostic_client","recommended_order":["signature_and_config_tests","request_parse_mock_tests","diagnostic_probe","live_probe_after_tenant_code"],"live_gate":"XG_RUN_LIVE_API_TEST=1 plus confirmed tenantCode"}}

exec
/bin/bash -lc "rtk rg -n \"generate_sign|appSecret|randStr|encryption|学工|S10405|XG_|xg_user|签名\" backend docs .omc/collaboration .omc/artifacts/ask -g '"'!*.jsonl'"'" in /home/caohui/projects/graduation-leave-system
 succeeded in 1ms:
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-10-clau-2026-05-30T14-36-35-991Z.md:1390:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:26:4. **遗漏问题：** 列表接口真的可以推迟吗？没有列表接口，辅导员/学工部怎么知道有哪些申请需要审批？Day 2能达到可重复验收吗？
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-10-clau-2026-05-30T14-36-35-991Z.md:1393:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:60:4. **遗漏问题：** 列表接口真的可以推迟吗？没有列表接口，辅导员/学工部怎么知道有哪些申请需要审批？Day 2能达到可重复验收吗？
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-10-clau-2026-05-30T14-36-35-991Z.md:1396:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:126:4. **遗漏问题：** 列表接口真的可以推迟吗？没有列表接口，辅导员/学工部怎么知道有哪些申请需要审批？Day 2能达到可重复验收吗？
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-10-clau-2026-05-30T14-36-35-991Z.md:2681:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:2942:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:26:4. **遗漏问题：** 列表接口真的可以推迟吗？没有列表接口，辅导员/学工部怎么知道有哪些申请需要审批？Day 2能达到可重复验收吗？
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-10-clau-2026-05-30T14-36-35-991Z.md:2684:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:2945:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:60:4. **遗漏问题：** 列表接口真的可以推迟吗？没有列表接口，辅导员/学工部怎么知道有哪些申请需要审批？Day 2能达到可重复验收吗？
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-10-clau-2026-05-30T14-36-35-991Z.md:2687:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:2948:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:126:4. **遗漏问题：** 列表接口真的可以推迟吗？没有列表接口，辅导员/学工部怎么知道有哪些申请需要审批？Day 2能达到可重复验收吗？
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-10-clau-2026-05-30T14-36-35-991Z.md:3387:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-01-claude-phase4c-strate-2026-06-01T07-04-35-149Z.md:117:   - 权限测试 (学生/辅导员/学工部)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-01-claude-phase4c-strate-2026-06-01T07-04-35-149Z.md:164:   - list权限 (RBAC: 学生own/辅导员class/学工部dean)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-01-claude-phase4c-strate-2026-06-01T07-04-35-149Z.md:190:3. **RBAC复杂度:** 辅导员/学工部权限检查依赖approval scope，是否会导致N+1查询？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-01-claude-phase4c-strate-2026-06-01T07-04-35-149Z.md:1507:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-01-claude-phase4c-strate-2026-06-01T07-04-35-149Z.md:1549:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-01-claude-phase4c-strate-2026-06-01T07-04-35-149Z.md:1608:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-01-claude-phase4c-strate-2026-06-01T07-04-35-149Z.md:1612:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-01-claude-phase4c-strate-2026-06-01T07-04-35-149Z.md:1684:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-01-claude-phase4c-strate-2026-06-01T07-04-35-149Z.md:1864:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-01-claude-phase4c-strate-2026-06-01T07-04-35-149Z.md:1944:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-34-codex-second-rev-2026-05-27T08-21-47-897Z.md:688:docs/design/2026-05-27-system-design.md:1473:    - 创建历史快照：applications_history（version=N, change_reason='学工部备案通过'）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-34-codex-second-rev-2026-05-27T08-21-47-897Z.md:689:docs/design/2026-05-27-system-design.md:1482:    - 创建历史快照：applications_history（version=N, change_reason='学工部驳回'）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-34-codex-second-rev-2026-05-27T08-21-47-897Z.md:1287:   300	- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-34-codex-second-rev-2026-05-27T08-21-47-897Z.md:1301:   314	    admin_id BIGINT COMMENT '学工部管理员ID',
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-34-codex-second-rev-2026-05-27T08-21-47-897Z.md:1678:   501	- `encryption_key` - 配置加密密钥（存储在环境变量，不在数据库）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-34-implementation-o-2026-06-01T01-50-38-091Z.md:61:4. 做最小 smoke：学生登录能进申请页，教师/学工能进审批页，非法角色回登录。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-34-implementation-o-2026-06-01T01-50-38-091Z.md:1203:     9	    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-34-implementation-o-2026-06-01T01-50-38-091Z.md:2227:4. 做最小 smoke：学生登录能进申请页，教师/学工能进审批页，非法角色回登录。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-55-claude-post-api-schem-2026-06-01T18-53-35-201Z.md:1601:    description='获取当前用户的申请列表（学生/辅导员/学工部）',
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-55-claude-post-api-schem-2026-06-01T18-53-35-201Z.md:2007:    description='获取当前用户的待审批列表（辅导员或学工部）',
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-55-claude-post-api-schem-2026-06-01T18-53-35-201Z.md:2038:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-55-claude-post-api-schem-2026-06-01T18-53-35-201Z.md:2134:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1022:docs/design/2026-05-27-system-design.md:300:- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1027:docs/design/2026-05-27-system-design.md:387:- `approver_role`: counselor（辅导员）、admin（学工部）
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1167:docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:150:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1172:docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:66:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1201:docs/PROJECT-SUMMARY.md:233:  - P1-2：降级方案逻辑矛盾（风险2说"砍学工部审批"又说"Day 4补学工部审批"）
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1202:docs/PROJECT-SUMMARY.md:238:  - P1-2修复：修复风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1227:./docs/PROJECT-SUMMARY.md:233:  - P1-2：降级方案逻辑矛盾（风险2说"砍学工部审批"又说"Day 4补学工部审批"）
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1228:./docs/PROJECT-SUMMARY.md:238:  - P1-2修复：修复风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1315:backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1316:backend/apps/approvals/tests/test_list_permissions.py:29:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1395:docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:20:2. **P1-2：降级方案逻辑矛盾** - 风险2说"砍学工部审批"又说"Day 4补学工部审批"
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1498:./backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1504:./docs/design/2026-05-27-system-design.md:300:- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1509:./docs/design/2026-05-27-system-design.md:387:- `approver_role`: counselor（辅导员）、admin（学工部）
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1565:./backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1566:./backend/apps/approvals/tests/test_list_permissions.py:29:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1607:backend/apps/users/migrations/0001_initial.py:25:                ('role', models.CharField(choices=[('student', '学生'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20)),
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1694:./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:150:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1710:./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:66:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1771:./backend/apps/users/migrations/0001_initial.py:25:                ('role', models.CharField(choices=[('student', '学生'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20)),
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:1906:backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:2151:./docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:20:2. **P1-2：降级方案逻辑矛盾** - 风险2说"砍学工部审批"又说"Day 4补学工部审批"
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:2729:   123	        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:2741:   135	        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:2754:   148	        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:2815:    25	        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:2819:    29	        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:2849:    59	            approver_name='学工部1',
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:3128:    48	        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:3166:    86	        # Step 5: 学工部登录
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:3173:    93	        # Step 6: 学工部审批通过
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:3226:    30	        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:3270:    74	            approver_name='学工部',
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:3493:测试学工部驳回申请
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:3503:测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:3640:测试学工部驳回申请
.omc/artifacts/ask/codex-claude-phase-4b-docs-discussions-codex-review-2026-05-27-36--2026-06-01T02-31-23-015Z.md:3650:测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-05-claude-next-steps-str-2026-06-01T07-43-59-071Z.md:122:- 申请详情页面：附件查看组件（辅导员/学工部查看附件）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-05-claude-next-steps-str-2026-06-01T07-43-59-071Z.md:141:- 审批详情页面：辅导员/学工部审批操作
.omc/artifacts/ask/codex-claude-docs-discussions-codex-review-2026-05-27-35-claude-re-2026-06-01T01-59-52-222Z.md:1439:4. 做最小 smoke：学生登录能进申请页，教师/学工能进审批页，非法角色回登录。
.omc/artifacts/ask/codex-claude-docs-discussions-codex-review-2026-05-27-35-claude-re-2026-06-01T01-59-52-222Z.md:2818:     9	    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-claude-docs-discussions-codex-review-2026-05-27-35-claude-re-2026-06-01T01-59-52-222Z.md:2943:backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md:1383:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3146:- ✓ Seed数据导入：10学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md:1686:.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2667:- ✓ Seed数据导入：10学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md:2681:  - list_attachments：GET，RBAC（学生own/辅导员class+approval/学工部dean approval）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md:3114:- 从教务系统或学工系统导出当届毕业生数据
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md:3306:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md:3407:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md:3453:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md:3846:  - 完整流程：登录→提交→辅导员审批→学工部审批→查询
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md:3857:  - 学工部驳回：pending_dean→rejected
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md:4452:+- 定义通知事件类型：申请提交、辅导员审批、学工部审批、驳回、附件上传。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md:4675:+- 定义通知事件类型：申请提交、辅导员审批、学工部审批、驳回、附件上传。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md:4897:- 定义通知事件类型：申请提交、辅导员审批、学工部审批、驳回、附件上传。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md:5125:+- 定义通知事件类型：申请提交、辅导员审批、学工部审批、驳回、附件上传。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-15-21-048Z.md:5356:+- 定义通知事件类型：申请提交、辅导员审批、学工部审批、驳回、附件上传。
.omc/artifacts/ask/codex-phase-4a-blocked-on-phase4a-waiting-for-devtools-phase-4b-ph-2026-06-01T01-33-23-790Z.md:1059:- 核心功能：登录、学生提交、列表、详情、辅导员/学工部审批
.omc/artifacts/ask/codex-phase-4a-blocked-on-phase4a-waiting-for-devtools-phase-4b-ph-2026-06-01T01-33-23-790Z.md:1061:- 排除：独立辅导员/学工部页面集、草稿、完整附件UX、高级过滤、通知中心、审计时间线、React Native
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:25:- **P1**：风险表里仍同时写“砍学工部审批”和“Day 4补学工部审批”，降级口径冲突。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:670:  - 新：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:838:    PENDING_DEAN = "pending_dean"        # 待学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:877:| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:879:| pending_dean | 学工部通过 | dean | approved | 无 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:880:| pending_dean | 学工部驳回 | dean | rejected | 无 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:899:| 学工部审批 | ✗ | ✗ | ✓（所有） |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1105:- [ ] 生成seed数据（10学生 + 2辅导员 + 1学工部 + 边界样本 + 默认密码）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1144:- [ ] Seed数据加载成功（10学生 + 2辅导员 + 1学工部）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1161:  - 创建学工部审批记录（通过时）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1162:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1163:  - 最小角色校验：只有学工部可审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1166:  - 最小角色校验：学生只能查自己，辅导员/学工部可查所有
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1177:- [ ] 学工部可审批（通过/驳回）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1182:- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1183:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1189:  - 测试1：学生登录 → 提交申请 → 辅导员审批通过 → 学工部审批通过 → 查询状态
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1249:**降级方案：** 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1251:### 风险3：Week 1 Day 4学工部审批未完成
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1360:- **最小角色校验**（学生/辅导员/学工部边界）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1363:- 学工部审批API
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1421:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1515:- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1630:- 风险2降级方案：改为"保留提交→辅导员审批→查询闭环，砍学工部审批"
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1810:**学工部（1人）：**
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2052:docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2059:docs/plans/week-0-1-execution-plan.md:180:**降级方案：** 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2162:- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2165:- 学工部审批API
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2168:- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2215:如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2285:最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2374:    36	- [ ] 生成seed数据（10学生 + 2辅导员 + 1学工部 + 边界样本 + 默认密码）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2413:    75	- [ ] Seed数据加载成功（10学生 + 2辅导员 + 1学工部）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2430:    92	  - 创建学工部审批记录（通过时）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2431:    93	- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2432:    94	  - 最小角色校验：只有学工部可审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2435:    97	  - 最小角色校验：学生只能查自己，辅导员/学工部可查所有
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2446:   108	- [ ] 学工部可审批（通过/驳回）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2451:   113	- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2452:   114	- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2458:   120	  - 测试1：学生登录 → 提交申请 → 辅导员审批通过 → 学工部审批通过 → 查询状态
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2518:   180	**降级方案：** 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2520:   182	### 风险3：Week 1 Day 4学工部审批未完成
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2659:    85	  - 新：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2809:    93	    PENDING_DEAN = "pending_dean"        # 待学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2848:   132	| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2850:   134	| pending_dean | 学工部通过 | dean | approved | 无 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2851:   135	| pending_dean | 学工部驳回 | dean | rejected | 无 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2870:   154	| 学工部审批 | ✗ | ✗ | ✓（所有） |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3078:   362	**学工部（1人）：**
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3299:   583	    # 4. 学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3421:+> 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3423:+这里“砍学工部审批”和“Day 4补学工部审批”同时出现，口径冲突。更合理的表达是：
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3425:+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3460:+**问题：** 同一句话同时说“砍学工部审批”和“Day 4补学工部审批”。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3464:+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3507:+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3618:+> 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3620:+这里“砍学工部审批”和“Day 4补学工部审批”同时出现，口径冲突。更合理的表达是：
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3622:+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3657:+**问题：** 同一句话同时说“砍学工部审批”和“Day 4补学工部审批”。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3661:+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3704:+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3858:> 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3860:这里“砍学工部审批”和“Day 4补学工部审批”同时出现，口径冲突。更合理的表达是：
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3862:> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3897:**问题：** 同一句话同时说“砍学工部审批”和“Day 4补学工部审批”。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3901:**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3944:2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4055:+> 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4057:+这里“砍学工部审批”和“Day 4补学工部审批”同时出现，口径冲突。更合理的表达是：
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4059:+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4094:+**问题：** 同一句话同时说“砍学工部审批”和“Day 4补学工部审批”。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4098:+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4141:+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4155:- **P1**：风险表里仍同时写“砍学工部审批”和“Day 4补学工部审批”，降级口径冲突。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4265:+> 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4267:+这里“砍学工部审批”和“Day 4补学工部审批”同时出现，口径冲突。更合理的表达是：
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4269:+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4304:+**问题：** 同一句话同时说“砍学工部审批”和“Day 4补学工部审批”。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4308:+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4351:+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:13:- 权限隔离：学生/辅导员/学工部三角色完整权限校验
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:16:- 数据：seed_data支持10学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:50:- 权限隔离：学生/辅导员/学工部三角色完整权限校验
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:53:- 数据：seed_data支持10学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:92:| P1 | 小程序核心操作：学生提交申请、辅导员 approve/reject、学工部 approve/reject、错误态展示 | 1.5-2.5天 | Week 4主线 |
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:102:2. 列表现在偏“待办”：辅导员/学工部主要看 pending。那**已审批历史在哪里看**？如果小程序要“已办”，后端需要明确接口语义。
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:141:- 权限隔离：学生/辅导员/学工部三角色完整权限校验
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:144:- 数据：seed_data支持10学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:699:./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:84:| 班级-辅导员对应关系 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1042:./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:14:计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1169:./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:50:| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1199:./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:40:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1233:./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:124:| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1240:./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:204:2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1246:./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:249:| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1481:  - UserDTO字段对教师/学工部不可选
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1500:  - P1-2：降级方案逻辑矛盾（风险2说"砍学工部审批"又说"Day 4补学工部审批"）
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1505:  - P1-2修复：修复风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1526:  - 1学工部（D001，默认密码为工号）
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1548:  - 辅导员通过→pending_dean（创建学工部审批记录）
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1550:  - 学工部通过→approved
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1551:  - 学工部驳回→rejected
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1555:  - 学工部只能审批学工部步骤
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1567:  - 完整流程：登录→提交→辅导员审批→学工部审批→查询
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1578:  - 学工部驳回：pending_dean→rejected
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1608:- ✓ Seed数据需求：2学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1619:- ✓ Seed数据导入：10学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1625:  5. 学工部审批成功 - status→approved
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1727:  - Happy path: 学生→辅导员→学工部审批流程 ✓
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1753:- ✓ 学工部: approver=user + step=dean + decision=pending
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1758:- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1805:- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1923:- **学工部：** 1个
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1970:### 3. 学工部账号（Dean）
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1973:**用途：** 测试学工部审批
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1983:- 学工部能审批所有通过辅导员审批的申请
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1984:- 学工部不能直接审批pending_counselor状态的申请
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:2054:- [ ] 1个学工部账号创建成功
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:2062:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:2289:  - Happy path: 学生→辅导员→学工部审批流程 ✓
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:2330:   - 受众：学校管理人员、辅导员、学工部
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:2341:- 学生、辅导员、学工部三种角色
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:2353:- 两级审批（辅导员→学工部）
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:2828:    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:2909:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:3068:| P1 | 小程序核心操作：学生提交申请、辅导员 approve/reject、学工部 approve/reject、错误态展示 | 1.5-2.5天 | Week 4主线 |
.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:3078:2. 列表现在偏“待办”：辅导员/学工部主要看 pending。那**已审批历史在哪里看**？如果小程序要“已办”，后端需要明确接口语义。
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:32:   - 学工部审批
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:613:- ✓ 学工部: approver=user + step=dean + decision=pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:618:- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:665:- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:741:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:942:  - UserDTO字段对教师/学工部不可选
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:961:  - P1-2：降级方案逻辑矛盾（风险2说"砍学工部审批"又说"Day 4补学工部审批"）
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:966:  - P1-2修复：修复风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:987:  - 1学工部（D001，默认密码为工号）
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:997:**范围：** 登录 → 提交 → 辅导员审批 → 学工部审批 → 查询状态
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1032:- [ ] 1个学工部
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1174:### 5. 学工部能进行最终审批 ✓/✗
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1178:**Step 1: 学工部登录**
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1229:- [ ] 学工部能登录
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1235:- 检查学工部权限配置
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1488:- **学工部：** 1个
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1535:### 3. 学工部账号（Dean）
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1538:**用途：** 测试学工部审批
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1548:- 学工部能审批所有通过辅导员审批的申请
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1549:- 学工部不能直接审批pending_counselor状态的申请
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1619:- [ ] 1个学工部账号创建成功
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1627:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1696:    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1777:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2257:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2301:            approver_name='学工部',
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2367:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2371:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2401:            approver_name='学工部1',
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2758:docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:102:- 学工部: `approver=user + step=dean + decision=pending`
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2761:docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:177:    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2764:docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md:35:   - 学工部仅看 `approver=user + step=dean + decision=pending`。
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2786:backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2789:backend/apps/approvals/tests/test_list_permissions.py:29:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2809:backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2840:   116	            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2993:   - 学工部审批
.omc/collaboration/artifacts/test-coverage-claude-response.md:34:> "学工部可以看所有审批" 与代码不符
.omc/collaboration/artifacts/test-coverage-claude-response.md:39:  # 学工部: 只看自己的dean审批
.omc/collaboration/artifacts/test-coverage-claude-response.md:54:**Action:** Remove "学工部可以看所有审批" from test plan.
.omc/collaboration/artifacts/test-coverage-claude-response.md:195:   - Expected: 409 CONFLICT "学工部审批已存在，不能重复创建"
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-44-17-027Z.md:1064:契约写“辅导员3工作日，学工部2工作日”。仓库依赖里已有 `chinese-calendar`，但这会引入节假日判断、调休解释和测试固定日期选择。若没有产品要求必须精确到中国法定节假日，v0.1 可以先改为自然日；若坚持工作日，则必须把算法和测试日期固定下来。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-44-17-027Z.md:1130:docs/api/notification-contract-v0.1.md:36:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-44-17-027Z.md:1258:docs/PROJECT-SUMMARY.md:1702:  - test_approval_approved_notification_dean（学工部审批通过通知）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-44-17-027Z.md:1995:backend/apps/notifications/tests/test_auto_notifications.py:134:        self.assertIn('学工部', notification.message)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-44-17-027Z.md:2233:    52	    approver_role = "辅导员" if approval.step == "counselor" else "学工部"
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-44-17-027Z.md:2569:     8	    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:1152:docs/design/2026-05-27-system-design.md:1448:    - 通知学工部
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:1219:docs/用户设计说明书.md:69:- 辅导员审批通过 → 通知学生和学工部
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:1221:docs/用户设计说明书.md:71:- 学工部审批通过 → 通知学生（审批完成）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:1222:docs/用户设计说明书.md:72:- 学工部驳回 → 通知学生
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:1234:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:1266:docs/PROJECT-SUMMARY.md:858:- 排除：独立辅导员/学工部页面集、草稿、完整附件UX、高级过滤、通知中心、审计时间线、React Native
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:1687:docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:14:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2002:.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:1379:docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:14:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2020:.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:1455:docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:59:- 风险2降级方案：改为"保留提交→辅导员审批→查询闭环，砍学工部审批"
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2142:.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2180:docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:186:2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2350:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3555:docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:14:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2367:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3920:docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:104:> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2368:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3921:docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:143:**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2375:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3928:docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:186:2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2414:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4386:.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:494:114:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2476:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4448:.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1494:   114	- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2489:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4493:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1380:+**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2493:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4501:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1493:+**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2497:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4509:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1605:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2501:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4517:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1763:+**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2506:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4527:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1894:+**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2523:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4667:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1093:   109	- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证辅导员审批
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2538:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4682:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1603:docs/plans/week-0-1-execution-plan.md:109:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证辅导员审批
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2546:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4690:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1984:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2554:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4698:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2122:docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:40:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2592:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4736:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2940:    40	| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2623:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5277:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1183:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2660:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5314:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2452:   114	- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2679:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5333:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3425:+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2680:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5334:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3464:+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2687:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5341:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3507:+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2690:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5344:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3622:+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2691:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5345:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3661:+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2698:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5352:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3704:+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2701:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5355:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3862:> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2702:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5356:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3901:**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2709:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5363:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3944:2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2712:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5366:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4059:+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2713:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5367:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4098:+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2720:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5374:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4141:+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2724:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5378:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4269:+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2725:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5379:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4308:+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:2732:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5386:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4351:+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:3108:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:766:docs/用户设计说明书.md:69:- 辅导员审批通过 → 通知学生和学工部
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:3109:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:767:docs/用户设计说明书.md:71:- 学工部审批通过 → 通知学生（审批完成）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:3121:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1123:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:3207:.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:3002:.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1119:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:3219:.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:3026:.omc/artifacts/ask/codex-student-application-api-createdefaultapiclient-reason-leave--2026-06-01T01-42-06-938Z.md:1855:- 排除：独立辅导员/学工部页面集、草稿、完整附件UX、高级过滤、通知中心、审计时间线、React Native
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:3239:.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:3251:.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1377:./docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:3301:.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:3373:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1385:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:3340:.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:3418:.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1754:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:3369:.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:3511:.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:6216:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:3690:.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:2232:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1421:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:3854:.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3659:.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:592:docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:116:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:3866:.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3671:.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:801:docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:117:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:3906:.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:6216:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:4291:1. 通知事件枚举：申请提交、辅导员通过、学工部通过、审批驳回、宿舍清退阻断。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:4603:| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:4604:| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:4606:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:4628:**触发条件：** 辅导员或学工部审批通过
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:4634:- 正文：`您的离校申请已通过{approver_role}审批。` （approver_role: 辅导员/学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:4644:**触发条件：** 辅导员或学工部驳回申请
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:4676:**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:4678:**接收者：** 待审批的辅导员/学工部
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:4888:| 操作 | 学生 | 辅导员 | 学工部 | 说明 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:5077:backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:78:**重要说明：本项目只对接宿管系统，不直接对接教务、人事、学工等其他系统。**
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:90:2. **数据归集：** 宿管系统已从教务、人事、学工等系统归集了所需数据
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:107:**Codex意见：** 将"提交给宿管系统方"改为"提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人"。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:114:1. 本系统只对接宿管系统，不直接对接教务、人事、学工
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:128:- 在待反馈问题中增加："宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？如不包含，能否从教务/人事/学工系统归集后提供？"
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:151:| 班级-辅导员对应关系 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:507:| 学工部管理员 | 当前在职 | 5人 | 手动创建 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:527:2. 如不包含，能否从教务/人事/学工系统归集后提供？
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:618:   - 理由：项目只对接宿管系统，不直接对接教务/人事/学工
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:690:1. **项目约束确认：** 我们明确项目只对接宿管系统，不直接对接教务/人事/学工。Codex是否认同这个约束下，原文档的反馈对象（宿管系统方）是正确的？
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:734:| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:969:### 3.1 学工部管理员信息
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:972:- 创建学工部管理员账号
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1054:1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1075:| 学工部管理员信息 | P1 合理 | 人数少，手动创建比外部对接更合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1085:1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1144:### 3.5 学工部管理员信息
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1163:| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1164:| 学工部管理员信息 | 手动创建 | 合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1195:| 学工部管理员 | 约 5 人 | 合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1213:> 请教务系统、人事系统、学工部数据负责人、宿管系统方分别确认其可提供的数据范围、字段、对接方式和联系人。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1225:7. 学工部终审人是固定个人、固定角色组、轮值还是人工分配？
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1243:2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1246:5. 学工部管理员：手动创建，同时配置默认终审人或终审组。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1278:> 明确毕业离校系统所需的数据源，提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人反馈。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1288:| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1415:5. 学工部管理员：手动创建（~5人）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1478:docs/design/2026-05-27-system-design.md:314:    admin_id BIGINT COMMENT '学工部管理员ID',
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1495:docs/design/2026-05-27-system-design.md:599:  ├─N:1─→ users (学工部管理员)
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1511:docs/design/2026-05-27-system-design.md:1427:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1608:docs/discussions/codex-review-2026-05-27/04-database-review.md:181:    admin_id BIGINT COMMENT '学工部管理员ID',
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1633:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:112:7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1642:docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:176:- admin_id BIGINT（固定学工部管理员ID）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1671:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:46:1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1831:./docs/design/2026-05-27-system-design.md:314:    admin_id BIGINT COMMENT '学工部管理员ID',
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1856:./docs/design/2026-05-27-system-design.md:599:  ├─N:1─→ users (学工部管理员)
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1882:./docs/design/2026-05-27-system-design.md:1427:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1888:./docs/design/2026-05-27-system-design.md:1473:    - 创建历史快照：applications_history（version=N, change_reason='学工部备案通过'）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1889:./docs/design/2026-05-27-system-design.md:1482:    - 创建历史快照：applications_history（version=N, change_reason='学工部驳回'）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1949:./docs/discussions/codex-review-2026-05-27/04-database-review.md:181:    admin_id BIGINT COMMENT '学工部管理员ID',
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1968:./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:112:7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1976:./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:176:- admin_id BIGINT（固定学工部管理员ID）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2006:./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:46:1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2179:   300	- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2193:   314	    admin_id BIGINT COMMENT '学工部管理员ID',
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2239:    11	**重要说明：本项目只对接宿管系统，不直接对接教务、人事、学工等其他系统。**
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2251:    23	2. **数据归集：** 宿管系统已从教务、人事、学工等系统归集了所需数据
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2268:    40	**Codex意见：** 将"提交给宿管系统方"改为"提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人"。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2275:    47	1. 本系统只对接宿管系统，不直接对接教务、人事、学工
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2289:    61	- 在待反馈问题中增加："宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？如不包含，能否从教务/人事/学工系统归集后提供？"
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2312:    84	| 班级-辅导员对应关系 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2589:   357	| 学工部管理员 | 当前在职 | 5人 | 手动创建 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2609:   377	2. 如不包含，能否从教务/人事/学工系统归集后提供？
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2763:    27	| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2771:    35	| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2786:    50	| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2820:    84	### 4. 学工部管理员数据源是否需要对接？
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2848:   112	7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2872:   136	6. **手动创建学工部管理员。** 同时补充管理员账号维护和终审人分配规则。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2899:   163	- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2945:   468	   - 理由：项目只对接宿管系统，不直接对接教务/人事/学工
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:3017:   540	1. **项目约束确认：** 我们明确项目只对接宿管系统，不直接对接教务/人事/学工。Codex是否认同这个约束下，原文档的反馈对象（宿管系统方）是正确的？
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:941:.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:42:   Day 3-4 的降级写“保留提交→辅导员审批→查询，砍学工部审批、列表API”是合理方向：[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:112)。  
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:964:.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1602:   Day 3-4 的降级写“保留提交→辅导员审批→查询，砍学工部审批、列表API”是合理方向：[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:112)。  
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:1522:  - UserDTO字段对教师/学工部不可选
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:1597:- **最小角色校验**（学生/辅导员/学工部边界）
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:1600:- 学工部审批API
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:1659:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:1757:- [ ] 学工部审批API
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:1770:- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:1841:- **最小角色校验**（学生/辅导员/学工部边界）
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:1844:- 学工部审批API
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:1902:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:1996:- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:2174:   214	  - UserDTO字段对教师/学工部不可选
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:2234:    55	- **最小角色校验**（学生/辅导员/学工部边界）
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:2237:    58	- 学工部审批API
.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:2295:   116	| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:13:2. ✅ CLI兼容解析与真实签名不匹配
.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:19:- 必须读取真实旧脚本签名，不能凭空假设
.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:125:首先读取真实旧脚本签名：
.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:128:# 查看.claude/skills/claude-codex-collab/scripts/collab_event.py当前签名
.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:132:**假设真实签名确实是`<type> <agent> <task_id> <summary> [artifacts_json]`：**
.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:223:需要读取`.claude/skills/claude-codex-collab/scripts/collab_event.py`确认真实签名。如果签名不同，需要调整解析逻辑。
.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:518:2. CLI兼容解析是否匹配真实签名？（需要先读取旧脚本确认）
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:67:- **P1 权限方案回退了。** 提案让学生访问 `GET /api/approvals/` 自己申请的审批记录，并让学工部在 `GET /api/applications/` 看所有申请：[07-claude-phase1-proposal.md](</home/caohui/projects/graduation-leave-system/docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:30>)。这和 Day 3 共识冲突：审批列表学生应 403，辅导员/学工部只看自己 `pending` 审批；学工部申请列表也应是“自己待审批对应的申请”，不是全量：[04-final-consensus.md](</home/caohui/projects/graduation-leave-system/docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:37>)。
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:715:- 学工部: 返回所有申请列表
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:750:- 学工部: 返回待自己审批的记录（step='dean', decision='pending'）
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:993:docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:29:| 学工部管理员 | admin | ~5人 | 终审备案 | 人事系统 |
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:1095:docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:172:2. **学工部权限过大**：admin既能审批又能管理系统配置
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:1099:docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:182:admin_approver   # 学工部审批员（只能审批）
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:1100:docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:183:admin_manager    # 学工部管理员（审批+配置管理）
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:1327:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:1337:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:112:7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:1346:docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:176:- admin_id BIGINT（固定学工部管理员ID）
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:1394:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:46:1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:1470:docs/discussions/codex-review-2026-05-27/04-database-review.md:181:    admin_id BIGINT COMMENT '学工部管理员ID',
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:1526:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:1706:    68	            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:1787:     8	    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:1827:     8	    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:2005:     8	    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:2174:    95	    PENDING_DEAN = "pending_dean"        # 待学工部审批
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:2213:   134	| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:2215:   136	| pending_dean | 学工部通过 | dean | approved | 无 |
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:2216:   137	| pending_dean | 学工部驳回 | dean | rejected | 无 |
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:2235:   156	| 学工部审批 | ✗ | ✗ | ✓（所有） |
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:2823:   364	**学工部（1人）：**
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:3260:    84	        """测试学工部驳回申请"""
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:3362:    48	        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:3400:    86	        # Step 5: 学工部登录
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:3407:    93	        # Step 6: 学工部审批通过
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:3687:docs/PROJECT-SUMMARY.md:238:  - P1-2修复：修复风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:3852:    33	- 学工部: 返回所有申请列表
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:3887:    68	- 学工部: 返回待自己审批的记录（step='dean', decision='pending'）
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:4228:- **P1 权限方案回退了。** 提案让学生访问 `GET /api/approvals/` 自己申请的审批记录，并让学工部在 `GET /api/applications/` 看所有申请：[07-claude-phase1-proposal.md](</home/caohui/projects/graduation-leave-system/docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:30>)。这和 Day 3 共识冲突：审批列表学生应 403，辅导员/学工部只看自己 `pending` 审批；学工部申请列表也应是“自己待审批对应的申请”，不是全量：[04-final-consensus.md](</home/caohui/projects/graduation-leave-system/docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:37>)。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:772:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:844:| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:845:| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:847:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:869:**触发条件：** 辅导员或学工部审批通过
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:875:- 正文：`您的离校申请已通过{approver_role}审批。` （approver_role: 辅导员/学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:885:**触发条件：** 辅导员或学工部驳回申请
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:917:**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:919:**接收者：** 待审批的辅导员/学工部
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:1200:    description='获取当前用户的申请列表（学生/辅导员/学工部）',
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:1972:    approver_role = "辅导员" if approval.step == "counselor" else "学工部"
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:2315:    52	    approver_role = "辅导员" if approval.step == "counselor" else "学工部"
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:2387:     9	    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:2433:    34	| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:2434:    35	| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:2436:    37	| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:2458:    59	**触发条件：** 辅导员或学工部审批通过
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:2464:    65	- 正文：`您的离校申请已通过{approver_role}审批。` （approver_role: 辅导员/学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:2474:    75	**触发条件：** 辅导员或学工部驳回申请
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:2506:   107	**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:2508:   109	**接收者：** 待审批的辅导员/学工部
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-27-45-286Z.md:1810:如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-50-claude-post-option-e--2026-06-01T18-13-55-411Z.md:1674:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-50-claude-post-option-e--2026-06-01T18-13-55-411Z.md:1756:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:1157:docs/api/notification-contract-v0.1.md:36:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:1159:docs/api/notification-contract-v0.1.md:90:**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:1329:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md:1215:    36	| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:1331:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md:1269:    90	**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:1444:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md:2801:  1702	  - test_approval_approved_notification_dean（学工部审批通过通知）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:1691:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:1249:./docs/api/notification-contract-v0.1.md:35:| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:1770:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:1908:        self.assertIn('学工部', notification.message)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:2272:docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:2406:docs/PROJECT-SUMMARY.md:1702:  - test_approval_approved_notification_dean（学工部审批通过通知）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:2575:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:847:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:2577:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:917:**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:2708:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:2436:    37	| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:2710:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-62-phase2b-contract-deci-2026-06-01T19-23-29-310Z.md:2506:   107	**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:3052:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:4606:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:3054:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-37-356Z.md:4676:**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:3109:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1330:docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:3145:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2698:docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:137:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:3158:.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1141:docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:3159:.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1198:docs/design/2026-05-27-system-design.md:389:- `time_limit`: 辅导员1个工作日(24小时)，学工部1个工作日(24小时)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:3193:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:1742:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:3195:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:1812:**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:3254:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:2107:docs/PROJECT-SUMMARY.md:1702:  - test_approval_approved_notification_dean（学工部审批通过通知）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:3427:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:903:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:3429:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:957:**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:3629:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:1972:        self.assertIn('学工部', notification.message)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:3665:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:2483:    36	| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:4245:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:2934:        self.assertIn('学工部', notification.message)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:4604:backend/apps/notifications/tests/test_auto_notifications.py:134:        self.assertIn('学工部', notification.message)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:4761:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1218:docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:4762:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1370:docs/design/2026-05-27-system-design.md:389:- `time_limit`: 辅导员1个工作日(24小时)，学工部1个工作日(24小时)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:4924:.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1227:./docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:4930:.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2067:./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:137:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:5121:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:1300:docs/api/notification-contract-v0.1.md:34:| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:5122:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:1301:docs/api/notification-contract-v0.1.md:35:| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:5124:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:1303:docs/api/notification-contract-v0.1.md:37:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:5256:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:1948:    37	| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:5258:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:2018:   107	**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:5402:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:762:docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:5410:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1349:docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:137:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:5468:docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:137:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:5506:docs/design/2026-05-27-system-design.md:389:- `time_limit`: 辅导员1个工作日(24小时)，学工部1个工作日(24小时)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:5584:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:1349:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:5586:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:1419:**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:5850:    approver_role = "辅导员" if approval.step == "counselor" else "学工部"
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:6036:backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:6067:backend/apps/approvals/migrations/0001_initial.py:20:                ('step', models.CharField(choices=[('counselor', '辅导员'), ('dean', '学工部')], max_length=20)),
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:6084:backend/apps/applications/models.py:9:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:6231:**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:6233:**接收者：** 待审批的辅导员/学工部
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:6273:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:6662:    description='获取当前用户的待审批列表（辅导员或学工部）',
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:6693:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:6789:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:6906:    description='获取当前用户的申请列表（学生/辅导员/学工部）',
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:7287:    52	    approver_role = "辅导员" if approval.step == "counselor" else "学工部"
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:7750:+契约写“辅导员3工作日，学工部2工作日”。仓库依赖里已有 `chinese-calendar`，但这会引入节假日判断、调休解释和测试固定日期选择。若没有产品要求必须精确到中国法定节假日，v0.1 可以先改为自然日；若坚持工作日，则必须把算法和测试日期固定下来。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:7924:+契约写“辅导员3工作日，学工部2工作日”。仓库依赖里已有 `chinese-calendar`，但这会引入节假日判断、调休解释和测试固定日期选择。若没有产品要求必须精确到中国法定节假日，v0.1 可以先改为自然日；若坚持工作日，则必须把算法和测试日期固定下来。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:8109:契约写“辅导员3工作日，学工部2工作日”。仓库依赖里已有 `chinese-calendar`，但这会引入节假日判断、调休解释和测试固定日期选择。若没有产品要求必须精确到中国法定节假日，v0.1 可以先改为自然日；若坚持工作日，则必须把算法和测试日期固定下来。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:8283:+契约写“辅导员3工作日，学工部2工作日”。仓库依赖里已有 `chinese-calendar`，但这会引入节假日判断、调休解释和测试固定日期选择。若没有产品要求必须精确到中国法定节假日，v0.1 可以先改为自然日；若坚持工作日，则必须把算法和测试日期固定下来。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:8463:+契约写“辅导员3工作日，学工部2工作日”。仓库依赖里已有 `chinese-calendar`，但这会引入节假日判断、调休解释和测试固定日期选择。若没有产品要求必须精确到中国法定节假日，v0.1 可以先改为自然日；若坚持工作日，则必须把算法和测试日期固定下来。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:8682:+契约写“辅导员3工作日，学工部2工作日”。仓库依赖里已有 `chinese-calendar`，但这会引入节假日判断、调休解释和测试固定日期选择。若没有产品要求必须精确到中国法定节假日，v0.1 可以先改为自然日；若坚持工作日，则必须把算法和测试日期固定下来。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:8916:+契约写“辅导员3工作日，学工部2工作日”。仓库依赖里已有 `chinese-calendar`，但这会引入节假日判断、调休解释和测试固定日期选择。若没有产品要求必须精确到中国法定节假日，v0.1 可以先改为自然日；若坚持工作日，则必须把算法和测试日期固定下来。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-claude-post-phase2b-s-2026-06-02T02-43-51-045Z.md:9098:+契约写“辅导员3工作日，学工部2工作日”。仓库依赖里已有 `chinese-calendar`，但这会引入节假日判断、调休解释和测试固定日期选择。若没有产品要求必须精确到中国法定节假日，v0.1 可以先改为自然日；若坚持工作日，则必须把算法和测试日期固定下来。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:799:先做"学生登录/伪登录 → 提交申请 → 辅导员审批 → 学工部审批 → 状态可查"的端到端最小流程。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:868:- 最小申请审批闭环（提交→辅导员审批→学工部审批→状态查询）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:1667:+- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:1670:+- 学工部审批API
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:1673:+- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:1720:+如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:1790:+最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:1957:+- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:1960:+- 学工部审批API
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:1963:+- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2010:+如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2080:+最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2250:- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2253:- 学工部审批API
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2256:- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2303:如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2373:最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2544:+- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2547:+- 学工部审批API
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2550:+- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2597:+如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2667:+最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2847:+- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2850:+- 学工部审批API
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2853:+- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2900:+如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md:2970:+最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
.omc/collaboration/artifacts/20260601-0135-claude-response-phase4a-blocker-challenge.md:118:   - 辅导员/学工部 → `/pages/approvals/approvals`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:1309:docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:14:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:1331:./docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:14:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:1564:| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:1565:| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:1567:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:1589:**触发条件：** 辅导员或学工部审批通过
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:1595:- 正文：`您的离校申请已通过{approver_role}审批。` （approver_role: 辅导员/学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:1605:**触发条件：** 辅导员或学工部驳回申请
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:1637:**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:1639:**接收者：** 待审批的辅导员/学工部
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:1844:| 操作 | 学生 | 辅导员 | 学工部 | 说明 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:2012:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:2058:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:2107:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:2705:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:2785:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:2936:    68	1. 通知事件枚举：申请提交、辅导员通过、学工部通过、审批驳回、宿舍清退阻断。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:3419:   314	| 操作 | 学生 | 辅导员 | 学工部 | 说明 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:3523:+当前幂等检查只使用 `(entity_type, entity_id, type)`。这会把同一业务实体的同类通知限制为全局唯一，无法支持多个接收者。例如一个未来事件可能需要通知多个学工部账号，或者同一申请的不同待办人。即便 v0.1 当前多数事件只有单接收者，也不应把 schema 固化成全局唯一。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:3695:+当前幂等检查只使用 `(entity_type, entity_id, type)`。这会把同一业务实体的同类通知限制为全局唯一，无法支持多个接收者。例如一个未来事件可能需要通知多个学工部账号，或者同一申请的不同待办人。即便 v0.1 当前多数事件只有单接收者，也不应把 schema 固化成全局唯一。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:4011:当前幂等检查只使用 `(entity_type, entity_id, type)`。这会把同一业务实体的同类通知限制为全局唯一，无法支持多个接收者。例如一个未来事件可能需要通知多个学工部账号，或者同一申请的不同待办人。即便 v0.1 当前多数事件只有单接收者，也不应把 schema 固化成全局唯一。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:4183:+当前幂等检查只使用 `(entity_type, entity_id, type)`。这会把同一业务实体的同类通知限制为全局唯一，无法支持多个接收者。例如一个未来事件可能需要通知多个学工部账号，或者同一申请的不同待办人。即便 v0.1 当前多数事件只有单接收者，也不应把 schema 固化成全局唯一。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:4444:+当前幂等检查只使用 `(entity_type, entity_id, type)`。这会把同一业务实体的同类通知限制为全局唯一，无法支持多个接收者。例如一个未来事件可能需要通知多个学工部账号，或者同一申请的不同待办人。即便 v0.1 当前多数事件只有单接收者，也不应把 schema 固化成全局唯一。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:4646:+当前幂等检查只使用 `(entity_type, entity_id, type)`。这会把同一业务实体的同类通知限制为全局唯一，无法支持多个接收者。例如一个未来事件可能需要通知多个学工部账号，或者同一申请的不同待办人。即便 v0.1 当前多数事件只有单接收者，也不应把 schema 固化成全局唯一。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-28-claude-post-phase0-ne-2026-06-01T15-28-48-075Z.md:4828:+当前幂等检查只使用 `(entity_type, entity_id, type)`。这会把同一业务实体的同类通知限制为全局唯一，无法支持多个接收者。例如一个未来事件可能需要通知多个学工部账号，或者同一申请的不同待办人。即便 v0.1 当前多数事件只有单接收者，也不应把 schema 固化成全局唯一。
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:931:./docs/superpowers/plans/2026-05-27-implementation-plan.md:347:- ✓ 学工部审批通过后状态变更为approved
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:940:./docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:952:./docs/PROJECT-SUMMARY.md:283:  - 学工部通过→approved
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:954:./docs/PROJECT-SUMMARY.md:358:  5. 学工部审批成功 - status→approved
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:968:./docs/contracts/contract-v0.1.md:136:| pending_dean | 学工部通过 | dean | approved | 无 |
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:991:./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:26:| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:995:./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:60:- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:996:./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:63:- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:1028:./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:150:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:1035:./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:66:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:1139:./docs/design/2026-05-27-system-design.md:387:- `approver_role`: counselor（辅导员）、admin（学工部）
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:1184:./docs/design/2026-05-27-system-design.md:1016:    "next_approver": "学工部",
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:1197:./docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:1209:./docs/design/2026-05-27-system-design.md:1463:- 权限要求：学工部管理员角色 + current_approver_id匹配
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:1213:./docs/design/2026-05-27-system-design.md:1473:    - 创建历史快照：applications_history（version=N, change_reason='学工部备案通过'）
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:1217:./docs/design/2026-05-27-system-design.md:1482:    - 创建历史快照：applications_history（version=N, change_reason='学工部驳回'）
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:1263:./backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:1427:./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:182:admin_approver   # 学工部审批员（只能审批）
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:2132:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:161:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:2445:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:2479:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:31:   - 1学工部（D001）
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:38:   - 学工部D001审批 → status=approved
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:88:   - 1学工部（D001）
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:95:   - 学工部D001审批 → status=approved
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:136:5. 学工部最终审批：主路径达标，但“能看到所有待审批申请”没有接口支撑；且 dean 审批人硬编码为 `D001`：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:48)。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:156:- “辅导员能看到自己班级申请”“学工部能看到全部待审批申请”没有列表接口，验收项不可验证。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:226:   - 1学工部（D001）
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:233:   - 学工部D001审批 → status=approved
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:1390:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:1450:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:1854:        """测试学工部驳回申请"""
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:1947:        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:1985:        # Step 5: 学工部登录
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:1992:        # Step 6: 学工部审批通过
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:2069:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:2197:                ('role', models.CharField(choices=[('student', '学生'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20)),
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:2350:                ('step', models.CharField(choices=[('counselor', '辅导员'), ('dean', '学工部')], max_length=20)),
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:2593:**范围：** 登录 → 提交 → 辅导员审批 → 学工部审批 → 查询状态
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:2628:- [ ] 1个学工部
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:2770:### 5. 学工部能进行最终审批 ✓/✗
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:2774:**Step 1: 学工部登录**
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:2825:- [ ] 学工部能登录
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:2831:- 检查学工部权限配置
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:2978:- **学工部：** 1个
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3025:### 3. 学工部账号（Dean）
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3028:**用途：** 测试学工部审批
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3038:- 学工部能审批所有通过辅导员审批的申请
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3039:- 学工部不能直接审批pending_counselor状态的申请
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3109:- [ ] 1个学工部账号创建成功
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3117:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3212:### 5. 学工部能进行最终审批 ✓/✗
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3216:**Step 1: 学工部登录**
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3267:- [ ] 学工部能登录
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3273:- 检查学工部权限配置
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3384:docs/PROJECT-SUMMARY.md:238:  - P1-2修复：修复风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3542:docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:93:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3543:docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:96:**验证：** 降级方案现在明确：Day 3触发后砍学工部审批，Day 4验证辅导员闭环，学工部推Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3555:docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:14:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3557:docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:71:如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3558:docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:79:4. 顺延范围明确：学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3712:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1054:1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3730:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2763:    27	| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3769:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:1176:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3780:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:2369:    40	| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3867:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1266:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3874:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1466:docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:40:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3911:docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:51:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3912:docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:54:**验证点：** 降级逻辑现在清晰：Day 3触发→砍学工部→Day 4验证辅导员闭环→学工部推Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3920:docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:104:> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3921:docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:143:**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3928:docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:186:2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4386:.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:494:114:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4448:.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1494:   114	- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4455:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:30:   [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:180) 已明确 Day 3 触发条件、砍学工部审批、Day 4 保“提交→辅导员审批→查询”闭环、学工部审批推到 Week 2 Day 1，不再存在原先“砍掉又补回”的矛盾。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4459:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:624:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4460:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:627:**验证点：** 降级逻辑现在清晰：Day 3触发→砍学工部→Day 4验证辅导员闭环→学工部推Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4470:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:836:> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4471:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:875:**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4478:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:918:2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4479:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:982:114:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4481:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:989:180:**降级方案：** 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4484:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1090:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4485:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1093:**验证：** 降级方案现在明确：Day 3触发后砍学工部审批，Day 4验证辅导员闭环，学工部推Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4489:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1216:   114	- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4491:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1237:   180	**降级方案：** 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4493:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1380:+**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4495:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1437:+如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4496:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1445:+4. 顺延范围明确：学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4501:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1493:+**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4503:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1550:+如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4504:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1558:+4. 顺延范围明确：学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4509:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1605:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4511:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1662:如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4512:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1670:4. 顺延范围明确：学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4517:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1763:+**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4519:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1820:+如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4520:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1828:+4. 顺延范围明确：学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4525:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1870:   [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:180) 已明确 Day 3 触发条件、砍学工部审批、Day 4 保“提交→辅导员审批→查询”闭环、学工部审批推到 Week 2 Day 1，不再存在原先“砍掉又补回”的矛盾。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4527:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1894:+**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4529:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1951:+如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4530:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1959:+4. 顺延范围明确：学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4667:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1093:   109	- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证辅导员审批
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4682:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1603:docs/plans/week-0-1-execution-plan.md:109:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证辅导员审批
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4690:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1984:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4698:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2122:docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:40:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4736:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2940:    40	| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4909:.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1638:+| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4934:.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1860:+| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4953:.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2076:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:4976:.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2258:+| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5003:.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2491:+| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5240:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5277:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1183:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5314:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2452:   114	- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5333:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3425:+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5334:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3464:+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5341:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3507:+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5344:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3622:+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5345:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3661:+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5352:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3704:+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5355:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3862:> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5356:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3901:**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5363:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:3944:2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5366:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4059:+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5367:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4098:+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5374:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4141:+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5378:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4269:+> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5379:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4308:+**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5386:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:4351:+2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5393:docs/plans/week-0-1-execution-plan.md:114:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5400:docs/plans/week-0-1-execution-plan.md:180:**降级方案：** 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5440:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:536:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5457:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2003:+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5465:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2326:+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5473:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2653:1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5479:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2804:+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5488:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3141:+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5499:docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:42:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5529:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:15:1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5567:docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:40:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5623:- [ ] check_status方法签名
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5681:# 4. 学工部审批
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5692:echo "✓ 学工部审批成功"
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5726:5. 学工部登录
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5727:6. 学工部审批
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:6036:测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询 ... FAIL
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:6050:测试学工部驳回申请 ... ERROR
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:6114:测试学工部驳回申请
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:6124:测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:6251:    39	        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:6289:    77	        # Step 5: 学工部登录
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:6296:    84	        # Step 6: 学工部审批通过
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:6453:5. 学工部最终审批：主路径达标，但“能看到所有待审批申请”没有接口支撑；且 dean 审批人硬编码为 `D001`：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:48)。
.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:6473:- “辅导员能看到自己班级申请”“学工部能看到全部待审批申请”没有列表接口，验收项不可验证。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:535:设计并实现学工系统人员信息API的数据读取测试方案。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:559:- `randStr`: 随机字符串（必填）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:560:- `sign`: 认证签名（必填，算法未知）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:561:- `encryptionType`: 加密类型，sha1或md5，默认sha1（可选）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:588:### 1. 签名算法推断
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:590:文档中提到"请参见签名校验部分"但未给出具体算法。需要推断可能的签名算法：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:593:- **A. HMAC-SHA1：** `sign = HMAC-SHA1(appSecret, appKey + timestamp + randStr)`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:594:- **B. 拼接SHA1：** `sign = SHA1(appKey + timestamp + randStr + appSecret)`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:595:- **C. 参数排序SHA1：** `sign = SHA1(sorted_params + appSecret)`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:641:2. **认证测试：** 验证签名算法正确性（可能需要多次尝试）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:648:7. 错误处理测试（无效签名、无效租户等）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:679:- 签名错误（401/403）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:693:1. **签名算法推断：**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:694:   - 最可能的签名算法（基于常见开放平台实践）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1220:- 从教务系统或学工系统导出当届毕业生数据
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1395:randStr	是	string	随机字符串
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1396:sign	是	string	认证签名，请参见签名校验部分
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1397:encryptionType	否	string	加密类型 只有 sha1和md5 不传默认 sha1 方式加密
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1405:number	否	string	学工号
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1649:/bin/bash -lc 'rtk rg -n "AppId|AppKey|AppSecret|tenantCode|auth-user-info|签名|encryptionType|xuegongmj|goliveplus" docs backend .omc -S' in /home/caohui/projects/graduation-leave-system
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1652:docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:27:2. API认证信息（appKey、appSecret、签名算法）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1653:docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:153:        # 实现签名算法（待API文档提供）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1654:docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:260:- 方法签名是否合理？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1655:docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:250:**Claude签名：** 待Codex审查后达成共识
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1660:docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:36:- `sign`: 认证签名（必填，算法未知）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1661:docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:37:- `encryptionType`: 加密类型，sha1或md5，默认sha1（可选）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1663:docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:64:### 1. 签名算法推断
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1664:docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:66:文档中提到"请参见签名校验部分"但未给出具体算法。需要推断可能的签名算法：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1665:docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:117:2. **认证测试：** 验证签名算法正确性（可能需要多次尝试）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1666:docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:124:7. 错误处理测试（无效签名、无效租户等）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1668:docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:155:- 签名错误（401/403）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1669:docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:169:1. **签名算法推断：**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1670:docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:170:   - 最可能的签名算法（基于常见开放平台实践）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1671:docs/discussions/phase4c-next-steps/22-claude-post-execution-next-steps.md:193:**Claude签名**  
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1674:docs/api说明.txt:18:sign	是	string	认证签名，请参见签名校验部分
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1675:docs/api说明.txt:19:encryptionType	否	string	加密类型 只有 sha1和md5 不传默认 sha1 方式加密
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1681:docs/week3-day0-acceptance-checklist.md:393:- [ ] check_status方法签名
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1682:docs/微信小程序备案说明.md:46:   - 法人签名章或法人手写正楷签名
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1683:docs/微信小程序备案说明.md:47:   - 接受签名章，不接受连笔签
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1684:docs/微信小程序备案说明.md:70:   - 法人签名章或法人手写正楷签名
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1685:docs/微信小程序备案说明.md:71:   - 接受签名章，不接受连笔签
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1686:docs/微信小程序备案说明.md:124:3. **授权书要求：** 必须盖学校公章，法人签名（接受签名章，不接受连笔签）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1687:.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:13:2. ✅ CLI兼容解析与真实签名不匹配
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1688:.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:19:- 必须读取真实旧脚本签名，不能凭空假设
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1689:.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:125:首先读取真实旧脚本签名：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1690:.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:128:# 查看.claude/skills/claude-codex-collab/scripts/collab_event.py当前签名
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1691:.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:132:**假设真实签名确实是`<type> <agent> <task_id> <summary> [artifacts_json]`：**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1692:.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:223:需要读取`.claude/skills/claude-codex-collab/scripts/collab_event.py`确认真实签名。如果签名不同，需要调整解析逻辑。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1693:.omc/collaboration/artifacts/20260530-1725-claude-p0-fixes.md:518:2. CLI兼容解析是否匹配真实签名？（需要先读取旧脚本确认）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1694:.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:11:但方案仍有 P0/P1 级缺口。最大问题不是“还差一点实现细节”，而是若按当前文档落地，可能引入新的不可用路径：wrapper 指向错误目录、旧 CLI 兼容解析与真实调用签名不匹配、`release_lock()` owner 字段不匹配、`claim_task()` 丢失原子生命周期校验。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1695:.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:29:### P0-2：CLI 兼容解析与真实旧调用签名不匹配
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1696:.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:126:2. CLI 参数兼容：当前方案错误，未兼容真实 legacy 签名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1697:.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:127:3. `release_lock()`：方向正确，但 owner 字段和 API 签名不一致，且需要避免 finally 中 release 异常掩盖主异常。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1698:.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:154:4. wrapper 兼容旧 API 签名；核心 API 可以逐步走新签名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1699:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:5623:- [ ] check_status方法签名
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1700:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:25:2. CLI 兼容方案不匹配真实旧签名；当前真实格式是 `<type> <agent> <task_id> <summary> [artifacts_json]`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1701:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6163:对照结果显示，当前仓库里确实只有旧 `.claude` 脚本在直接写 `events.jsonl/state.json`，但 Claude 文档提出的 wrapper 路径和当前调用签名之间有几处不一致，可能会变成新的阻塞点。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1702:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6804:+但方案仍有 P0/P1 级缺口。最大问题不是“还差一点实现细节”，而是若按当前文档落地，可能引入新的不可用路径：wrapper 指向错误目录、旧 CLI 兼容解析与真实调用签名不匹配、`release_lock()` owner 字段不匹配、`claim_task()` 丢失原子生命周期校验。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1703:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6822:+### P0-2：CLI 兼容解析与真实旧调用签名不匹配
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1704:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6919:+2. CLI 参数兼容：当前方案错误，未兼容真实 legacy 签名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1705:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6920:+3. `release_lock()`：方向正确，但 owner 字段和 API 签名不一致，且需要避免 finally 中 release 异常掩盖主异常。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1706:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6947:+4. wrapper 兼容旧 API 签名；核心 API 可以逐步走新签名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1707:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6970:+但方案仍有 P0/P1 级缺口。最大问题不是“还差一点实现细节”，而是若按当前文档落地，可能引入新的不可用路径：wrapper 指向错误目录、旧 CLI 兼容解析与真实调用签名不匹配、`release_lock()` owner 字段不匹配、`claim_task()` 丢失原子生命周期校验。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1708:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6988:+### P0-2：CLI 兼容解析与真实旧调用签名不匹配
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1709:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7085:+2. CLI 参数兼容：当前方案错误，未兼容真实 legacy 签名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1710:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7086:+3. `release_lock()`：方向正确，但 owner 字段和 API 签名不一致，且需要避免 finally 中 release 异常掩盖主异常。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1711:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7113:+4. wrapper 兼容旧 API 签名；核心 API 可以逐步走新签名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1712:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7137:但方案仍有 P0/P1 级缺口。最大问题不是“还差一点实现细节”，而是若按当前文档落地，可能引入新的不可用路径：wrapper 指向错误目录、旧 CLI 兼容解析与真实调用签名不匹配、`release_lock()` owner 字段不匹配、`claim_task()` 丢失原子生命周期校验。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1713:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7155:### P0-2：CLI 兼容解析与真实旧调用签名不匹配
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1714:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7252:2. CLI 参数兼容：当前方案错误，未兼容真实 legacy 签名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1715:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7253:3. `release_lock()`：方向正确，但 owner 字段和 API 签名不一致，且需要避免 finally 中 release 异常掩盖主异常。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1716:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7280:4. wrapper 兼容旧 API 签名；核心 API 可以逐步走新签名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1717:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7303:+但方案仍有 P0/P1 级缺口。最大问题不是“还差一点实现细节”，而是若按当前文档落地，可能引入新的不可用路径：wrapper 指向错误目录、旧 CLI 兼容解析与真实调用签名不匹配、`release_lock()` owner 字段不匹配、`claim_task()` 丢失原子生命周期校验。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1718:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7321:+### P0-2：CLI 兼容解析与真实旧调用签名不匹配
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1719:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7418:+2. CLI 参数兼容：当前方案错误，未兼容真实 legacy 签名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1720:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7419:+3. `release_lock()`：方向正确，但 owner 字段和 API 签名不一致，且需要避免 finally 中 release 异常掩盖主异常。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1721:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7446:+4. wrapper 兼容旧 API 签名；核心 API 可以逐步走新签名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1722:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7461:2. CLI 兼容方案不匹配真实旧签名；当前真实格式是 `<type> <agent> <task_id> <summary> [artifacts_json]`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1723:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7484:+但方案仍有 P0/P1 级缺口。最大问题不是“还差一点实现细节”，而是若按当前文档落地，可能引入新的不可用路径：wrapper 指向错误目录、旧 CLI 兼容解析与真实调用签名不匹配、`release_lock()` owner 字段不匹配、`claim_task()` 丢失原子生命周期校验。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1724:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7502:+### P0-2：CLI 兼容解析与真实旧调用签名不匹配
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1725:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7599:+2. CLI 参数兼容：当前方案错误，未兼容真实 legacy 签名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1726:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7600:+3. `release_lock()`：方向正确，但 owner 字段和 API 签名不一致，且需要避免 finally 中 release 异常掩盖主异常。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1727:.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7627:+4. wrapper 兼容旧 API 签名；核心 API 可以逐步走新签名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1728:.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1541:- [ ] check_status方法签名
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1730:.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:1104:docs/week3-day0-acceptance-checklist.md:393:- [ ] check_status方法签名
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1732:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:128:2. API认证信息（appKey、appSecret、签名算法）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1733:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:254:        # 实现签名算法（待API文档提供）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1734:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:361:- 方法签名是否合理？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1735:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:975:- 方法签名是否合理？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1737:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:2580:    27	2. API认证信息（appKey、appSecret、签名算法）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1738:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:2706:   153	        # 实现签名算法（待API文档提供）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1739:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:3677:   260	- 方法签名是否合理？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1741:docs/design/2026-05-27-system-design.md:1970:- JWT签名算法：HS256
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1742:docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:62:3. **自签名证书**：对接方需要信任自签名证书，增加配置复杂度
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1743:docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:199:2. 如果使用自签名证书，对接方是否能接受？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1745:.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:3405:- [ ] check_status方法签名
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1746:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-22-claude-post-execution-2026-06-01T14-27-35-376Z.md:275:**Claude签名**  
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1747:.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1152:./docs/week3-day0-acceptance-checklist.md:393:- [ ] check_status方法签名
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1749:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1688:docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:27:2. API认证信息（appKey、appSecret、签名算法）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1750:.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:341:**Claude签名：** 待Codex审查后达成共识
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1751:.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:4300:docs/week3-day0-acceptance-checklist.md:393:- [ ] check_status方法签名
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1752:.omc/artifacts/ask/codex-step-2-step-1-baseline-tag-step-2-p0-step-2-enforcement-omc--2026-05-30T16-45-40-249Z.md:142:   - 保留 CLI 签名：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1753:.omc/artifacts/ask/codex-step-2-step-1-baseline-tag-step-2-p0-step-2-enforcement-omc--2026-05-30T16-45-40-249Z.md:4012:   - 保留 CLI 签名：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:1957:2. API认证信息（appKey、appSecret、签名算法）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:2069:        sign = self._generate_sign()
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:2082:    def _generate_sign(self):
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:2083:        # 实现签名算法（待API文档提供）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:2673:契约写“辅导员3工作日，学工部2工作日”。仓库依赖里已有 `chinese-calendar`，但这会引入节假日判断、调休解释和测试固定日期选择。若没有产品要求必须精确到中国法定节假日，v0.1 可以先改为自然日；若坚持工作日，则必须把算法和测试日期固定下来。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:2920:+2. **P1：签名算法不能靠猜测进入正式实现；最多允许在一次性诊断脚本中按候选算法快速验证，正式代码必须等待平台部提供签名校验文档或可确认的样例。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:2922:+另外，`docs/api说明.txt` 的官方样式文档只给出 `sign`、`timestamp`、`randStr`、`encryptionType` 字段，但缺少“签名校验部分”；`tenantCode` 也只有示例值 `C10026`。因此第一阶段的目标应调整为“受控验证接口合同”，不是直接实现生产数据同步。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:2936:+- 将文档中的凭证替换为占位符，例如 `${XG_APP_KEY}`、`${XG_APP_SECRET}`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:2941:+### P1：签名算法缺失，不能作为正式实现假设
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:2947:+当前文档明确写“请参见签名校验部分”，但仓库内文档没有该部分。候选算法 A/B/C 都只是合理猜测，不能作为生产实现依据。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:2951:+- 向平台部索要签名校验文档，至少需要：参与签名的字段、字段顺序、是否包含 form-data、secret位置、大小写、编码、输出hex/base64、时间戳单位、randStr长度、签名有效窗口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:2952:+- 同时索要一个固定样例：固定 appKey、timestamp、randStr、tenantCode、appSecret 和期望 sign。没有固定样例时，算法验证成本会显著上升。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:2979:+- 从平台部或学工系统管理员处获取本校真实 `tenantCode`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:2992:+- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:2993:+- 真实API测试必须通过显式开关启用，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:2999:+### 1. 签名算法推断
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3001:+在没有官方签名校验章节前，最可能的顺序建议如下：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3003:+1. **参数排序SHA1/MD5：** 将参与签名参数按key排序后拼接，再追加或混入 `appSecret`。很多开放平台采用这种方式，且文档提供 `encryptionType=sha1|md5` 更像普通摘要算法选择，而不是HMAC选择。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3004:+2. **拼接SHA1/MD5：** `SHA1(appKey + timestamp + randStr + appSecret)` 或 `SHA1(appSecret + appKey + timestamp + randStr)`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3005:+3. **HMAC-SHA1：** 技术上更好，但如果文档只称 `encryptionType` 为 `sha1/md5`，而不是 `hmac-sha1`，优先级略低。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3021:+backend/scripts/xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3022:+backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3023:+backend/apps/users/tests/test_xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3028:+- `xg_user_api_probe.py`：人工运行的诊断入口，读取环境变量，支持 `--algorithm`、`--page-size 1`、`--timeout`、`--dry-run`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3029:+- `xg_user_client.py`：可复用客户端，负责签名、请求构造、响应解析、错误归一化；后续可接入 `RealUserDataProvider`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3030:+- `test_xg_user_client.py`：mock HTTP响应，覆盖签名候选、字段解析、错误处理，不调用真实网络。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3039:+2. 请求构造：header/form-data完整，timestamp/randStr/sign存在。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3040:+3. 认证验证：用最小请求验证签名算法。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3049:+- 错误签名压测。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3052:+这些应等签名、租户、字段映射确认后再做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3056:+必须由平台部、学工系统管理员或接口开通记录提供真实 `tenantCode`。不要把文档样例 `C10026` 当成本校租户。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3072:+XG_USER_API_URL
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3073:+XG_USER_API_APP_KEY
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3074:+XG_USER_API_APP_SECRET
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3075:+XG_USER_API_TENANT_CODE
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3076:+XG_USER_API_ENCRYPTION_TYPE=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3077:+XG_RUN_LIVE_API_TEST=0
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3100:+- `auth_failed`：HTTP 401/403 或业务错误提示签名失败，输出当前算法名和非敏感参数。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3105:+不要对认证失败做大量重试。签名错误重试越多，越可能触发风控或污染审计。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3123:+- 获得签名校验文档或固定签名样例。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3131:+- `xg_user_client.py` 支持候选签名算法、请求构造、响应解析。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3132:+- `xg_user_api_probe.py` 可通过环境变量运行，默认只请求 `page=1&pageNum=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3147:+- 仅在 `XG_RUN_LIVE_API_TEST=1` 时执行。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3166:+- **实现可mock的客户端单元测试，覆盖签名候选和响应解析。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3168:+- **签名和租户确认前，不启动生产数据读取实现。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3195:+2. **P1：签名算法不能靠猜测进入正式实现；最多允许在一次性诊断脚本中按候选算法快速验证，正式代码必须等待平台部提供签名校验文档或可确认的样例。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3197:+另外，`docs/api说明.txt` 的官方样式文档只给出 `sign`、`timestamp`、`randStr`、`encryptionType` 字段，但缺少“签名校验部分”；`tenantCode` 也只有示例值 `C10026`。因此第一阶段的目标应调整为“受控验证接口合同”，不是直接实现生产数据同步。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3211:+- 将文档中的凭证替换为占位符，例如 `${XG_APP_KEY}`、`${XG_APP_SECRET}`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3216:+### P1：签名算法缺失，不能作为正式实现假设
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3222:+当前文档明确写“请参见签名校验部分”，但仓库内文档没有该部分。候选算法 A/B/C 都只是合理猜测，不能作为生产实现依据。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3226:+- 向平台部索要签名校验文档，至少需要：参与签名的字段、字段顺序、是否包含 form-data、secret位置、大小写、编码、输出hex/base64、时间戳单位、randStr长度、签名有效窗口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3227:+- 同时索要一个固定样例：固定 appKey、timestamp、randStr、tenantCode、appSecret 和期望 sign。没有固定样例时，算法验证成本会显著上升。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3254:+- 从平台部或学工系统管理员处获取本校真实 `tenantCode`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3267:+- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3268:+- 真实API测试必须通过显式开关启用，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3274:+### 1. 签名算法推断
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3276:+在没有官方签名校验章节前，最可能的顺序建议如下：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3278:+1. **参数排序SHA1/MD5：** 将参与签名参数按key排序后拼接，再追加或混入 `appSecret`。很多开放平台采用这种方式，且文档提供 `encryptionType=sha1|md5` 更像普通摘要算法选择，而不是HMAC选择。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3279:+2. **拼接SHA1/MD5：** `SHA1(appKey + timestamp + randStr + appSecret)` 或 `SHA1(appSecret + appKey + timestamp + randStr)`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3280:+3. **HMAC-SHA1：** 技术上更好，但如果文档只称 `encryptionType` 为 `sha1/md5`，而不是 `hmac-sha1`，优先级略低。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3296:+backend/scripts/xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3297:+backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3298:+backend/apps/users/tests/test_xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3303:+- `xg_user_api_probe.py`：人工运行的诊断入口，读取环境变量，支持 `--algorithm`、`--page-size 1`、`--timeout`、`--dry-run`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3304:+- `xg_user_client.py`：可复用客户端，负责签名、请求构造、响应解析、错误归一化；后续可接入 `RealUserDataProvider`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3305:+- `test_xg_user_client.py`：mock HTTP响应，覆盖签名候选、字段解析、错误处理，不调用真实网络。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3314:+2. 请求构造：header/form-data完整，timestamp/randStr/sign存在。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3315:+3. 认证验证：用最小请求验证签名算法。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3324:+- 错误签名压测。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3327:+这些应等签名、租户、字段映射确认后再做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3331:+必须由平台部、学工系统管理员或接口开通记录提供真实 `tenantCode`。不要把文档样例 `C10026` 当成本校租户。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3347:+XG_USER_API_URL
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3348:+XG_USER_API_APP_KEY
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3349:+XG_USER_API_APP_SECRET
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3350:+XG_USER_API_TENANT_CODE
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3351:+XG_USER_API_ENCRYPTION_TYPE=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3352:+XG_RUN_LIVE_API_TEST=0
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3375:+- `auth_failed`：HTTP 401/403 或业务错误提示签名失败，输出当前算法名和非敏感参数。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3380:+不要对认证失败做大量重试。签名错误重试越多，越可能触发风控或污染审计。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3398:+- 获得签名校验文档或固定签名样例。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3406:+- `xg_user_client.py` 支持候选签名算法、请求构造、响应解析。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3407:+- `xg_user_api_probe.py` 可通过环境变量运行，默认只请求 `page=1&pageNum=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3422:+- 仅在 `XG_RUN_LIVE_API_TEST=1` 时执行。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3441:+- **实现可mock的客户端单元测试，覆盖签名候选和响应解析。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3443:+- **签名和租户确认前，不启动生产数据读取实现。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3484:2. **P1：签名算法不能靠猜测进入正式实现；最多允许在一次性诊断脚本中按候选算法快速验证，正式代码必须等待平台部提供签名校验文档或可确认的样例。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3486:另外，`docs/api说明.txt` 的官方样式文档只给出 `sign`、`timestamp`、`randStr`、`encryptionType` 字段，但缺少“签名校验部分”；`tenantCode` 也只有示例值 `C10026`。因此第一阶段的目标应调整为“受控验证接口合同”，不是直接实现生产数据同步。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3500:- 将文档中的凭证替换为占位符，例如 `${XG_APP_KEY}`、`${XG_APP_SECRET}`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3505:### P1：签名算法缺失，不能作为正式实现假设
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3511:当前文档明确写“请参见签名校验部分”，但仓库内文档没有该部分。候选算法 A/B/C 都只是合理猜测，不能作为生产实现依据。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3515:- 向平台部索要签名校验文档，至少需要：参与签名的字段、字段顺序、是否包含 form-data、secret位置、大小写、编码、输出hex/base64、时间戳单位、randStr长度、签名有效窗口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3516:- 同时索要一个固定样例：固定 appKey、timestamp、randStr、tenantCode、appSecret 和期望 sign。没有固定样例时，算法验证成本会显著上升。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3543:- 从平台部或学工系统管理员处获取本校真实 `tenantCode`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3556:- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3557:- 真实API测试必须通过显式开关启用，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3563:### 1. 签名算法推断
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3565:在没有官方签名校验章节前，最可能的顺序建议如下：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3567:1. **参数排序SHA1/MD5：** 将参与签名参数按key排序后拼接，再追加或混入 `appSecret`。很多开放平台采用这种方式，且文档提供 `encryptionType=sha1|md5` 更像普通摘要算法选择，而不是HMAC选择。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3568:2. **拼接SHA1/MD5：** `SHA1(appKey + timestamp + randStr + appSecret)` 或 `SHA1(appSecret + appKey + timestamp + randStr)`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3569:3. **HMAC-SHA1：** 技术上更好，但如果文档只称 `encryptionType` 为 `sha1/md5`，而不是 `hmac-sha1`，优先级略低。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3585:backend/scripts/xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3586:backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3587:backend/apps/users/tests/test_xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3592:- `xg_user_api_probe.py`：人工运行的诊断入口，读取环境变量，支持 `--algorithm`、`--page-size 1`、`--timeout`、`--dry-run`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3593:- `xg_user_client.py`：可复用客户端，负责签名、请求构造、响应解析、错误归一化；后续可接入 `RealUserDataProvider`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3594:- `test_xg_user_client.py`：mock HTTP响应，覆盖签名候选、字段解析、错误处理，不调用真实网络。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3603:2. 请求构造：header/form-data完整，timestamp/randStr/sign存在。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3604:3. 认证验证：用最小请求验证签名算法。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3613:- 错误签名压测。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3616:这些应等签名、租户、字段映射确认后再做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3620:必须由平台部、学工系统管理员或接口开通记录提供真实 `tenantCode`。不要把文档样例 `C10026` 当成本校租户。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3636:XG_USER_API_URL
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3637:XG_USER_API_APP_KEY
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3638:XG_USER_API_APP_SECRET
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3639:XG_USER_API_TENANT_CODE
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3640:XG_USER_API_ENCRYPTION_TYPE=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3641:XG_RUN_LIVE_API_TEST=0
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3664:- `auth_failed`：HTTP 401/403 或业务错误提示签名失败，输出当前算法名和非敏感参数。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3669:不要对认证失败做大量重试。签名错误重试越多，越可能触发风控或污染审计。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3687:- 获得签名校验文档或固定签名样例。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3695:- `xg_user_client.py` 支持候选签名算法、请求构造、响应解析。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3696:- `xg_user_api_probe.py` 可通过环境变量运行，默认只请求 `page=1&pageNum=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3711:- 仅在 `XG_RUN_LIVE_API_TEST=1` 时执行。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3751:+2. **P1：签名算法不能靠猜测进入正式实现；最多允许在一次性诊断脚本中按候选算法快速验证，正式代码必须等待平台部提供签名校验文档或可确认的样例。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3753:+另外，`docs/api说明.txt` 的官方样式文档只给出 `sign`、`timestamp`、`randStr`、`encryptionType` 字段，但缺少“签名校验部分”；`tenantCode` 也只有示例值 `C10026`。因此第一阶段的目标应调整为“受控验证接口合同”，不是直接实现生产数据同步。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3767:+- 将文档中的凭证替换为占位符，例如 `${XG_APP_KEY}`、`${XG_APP_SECRET}`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3772:+### P1：签名算法缺失，不能作为正式实现假设
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3778:+当前文档明确写“请参见签名校验部分”，但仓库内文档没有该部分。候选算法 A/B/C 都只是合理猜测，不能作为生产实现依据。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3782:+- 向平台部索要签名校验文档，至少需要：参与签名的字段、字段顺序、是否包含 form-data、secret位置、大小写、编码、输出hex/base64、时间戳单位、randStr长度、签名有效窗口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3783:+- 同时索要一个固定样例：固定 appKey、timestamp、randStr、tenantCode、appSecret 和期望 sign。没有固定样例时，算法验证成本会显著上升。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3810:+- 从平台部或学工系统管理员处获取本校真实 `tenantCode`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3823:+- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3824:+- 真实API测试必须通过显式开关启用，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3830:+### 1. 签名算法推断
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3832:+在没有官方签名校验章节前，最可能的顺序建议如下：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3834:+1. **参数排序SHA1/MD5：** 将参与签名参数按key排序后拼接，再追加或混入 `appSecret`。很多开放平台采用这种方式，且文档提供 `encryptionType=sha1|md5` 更像普通摘要算法选择，而不是HMAC选择。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3835:+2. **拼接SHA1/MD5：** `SHA1(appKey + timestamp + randStr + appSecret)` 或 `SHA1(appSecret + appKey + timestamp + randStr)`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3836:+3. **HMAC-SHA1：** 技术上更好，但如果文档只称 `encryptionType` 为 `sha1/md5`，而不是 `hmac-sha1`，优先级略低。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3852:+backend/scripts/xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3853:+backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3854:+backend/apps/users/tests/test_xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3859:+- `xg_user_api_probe.py`：人工运行的诊断入口，读取环境变量，支持 `--algorithm`、`--page-size 1`、`--timeout`、`--dry-run`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3860:+- `xg_user_client.py`：可复用客户端，负责签名、请求构造、响应解析、错误归一化；后续可接入 `RealUserDataProvider`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3861:+- `test_xg_user_client.py`：mock HTTP响应，覆盖签名候选、字段解析、错误处理，不调用真实网络。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3870:+2. 请求构造：header/form-data完整，timestamp/randStr/sign存在。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3871:+3. 认证验证：用最小请求验证签名算法。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3880:+- 错误签名压测。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3883:+这些应等签名、租户、字段映射确认后再做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3887:+必须由平台部、学工系统管理员或接口开通记录提供真实 `tenantCode`。不要把文档样例 `C10026` 当成本校租户。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3903:+XG_USER_API_URL
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3904:+XG_USER_API_APP_KEY
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3905:+XG_USER_API_APP_SECRET
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3906:+XG_USER_API_TENANT_CODE
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3907:+XG_USER_API_ENCRYPTION_TYPE=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3908:+XG_RUN_LIVE_API_TEST=0
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3931:+- `auth_failed`：HTTP 401/403 或业务错误提示签名失败，输出当前算法名和非敏感参数。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3936:+不要对认证失败做大量重试。签名错误重试越多，越可能触发风控或污染审计。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3954:+- 获得签名校验文档或固定签名样例。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3962:+- `xg_user_client.py` 支持候选签名算法、请求构造、响应解析。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3963:+- `xg_user_api_probe.py` 可通过环境变量运行，默认只请求 `page=1&pageNum=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3978:+- 仅在 `XG_RUN_LIVE_API_TEST=1` 时执行。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3997:+- **实现可mock的客户端单元测试，覆盖签名候选和响应解析。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:3999:+- **签名和租户确认前，不启动生产数据读取实现。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4033:+2. **P1：签名算法不能靠猜测进入正式实现；最多允许在一次性诊断脚本中按候选算法快速验证，正式代码必须等待平台部提供签名校验文档或可确认的样例。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4035:+另外，`docs/api说明.txt` 的官方样式文档只给出 `sign`、`timestamp`、`randStr`、`encryptionType` 字段，但缺少“签名校验部分”；`tenantCode` 也只有示例值 `C10026`。因此第一阶段的目标应调整为“受控验证接口合同”，不是直接实现生产数据同步。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4049:+- 将文档中的凭证替换为占位符，例如 `${XG_APP_KEY}`、`${XG_APP_SECRET}`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4054:+### P1：签名算法缺失，不能作为正式实现假设
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4060:+当前文档明确写“请参见签名校验部分”，但仓库内文档没有该部分。候选算法 A/B/C 都只是合理猜测，不能作为生产实现依据。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4064:+- 向平台部索要签名校验文档，至少需要：参与签名的字段、字段顺序、是否包含 form-data、secret位置、大小写、编码、输出hex/base64、时间戳单位、randStr长度、签名有效窗口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4065:+- 同时索要一个固定样例：固定 appKey、timestamp、randStr、tenantCode、appSecret 和期望 sign。没有固定样例时，算法验证成本会显著上升。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4092:+- 从平台部或学工系统管理员处获取本校真实 `tenantCode`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4105:+- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4106:+- 真实API测试必须通过显式开关启用，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4112:+### 1. 签名算法推断
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4114:+在没有官方签名校验章节前，最可能的顺序建议如下：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4116:+1. **参数排序SHA1/MD5：** 将参与签名参数按key排序后拼接，再追加或混入 `appSecret`。很多开放平台采用这种方式，且文档提供 `encryptionType=sha1|md5` 更像普通摘要算法选择，而不是HMAC选择。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4117:+2. **拼接SHA1/MD5：** `SHA1(appKey + timestamp + randStr + appSecret)` 或 `SHA1(appSecret + appKey + timestamp + randStr)`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4118:+3. **HMAC-SHA1：** 技术上更好，但如果文档只称 `encryptionType` 为 `sha1/md5`，而不是 `hmac-sha1`，优先级略低。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4134:+backend/scripts/xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4135:+backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4136:+backend/apps/users/tests/test_xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4141:+- `xg_user_api_probe.py`：人工运行的诊断入口，读取环境变量，支持 `--algorithm`、`--page-size 1`、`--timeout`、`--dry-run`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4142:+- `xg_user_client.py`：可复用客户端，负责签名、请求构造、响应解析、错误归一化；后续可接入 `RealUserDataProvider`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4143:+- `test_xg_user_client.py`：mock HTTP响应，覆盖签名候选、字段解析、错误处理，不调用真实网络。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4152:+2. 请求构造：header/form-data完整，timestamp/randStr/sign存在。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4153:+3. 认证验证：用最小请求验证签名算法。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4162:+- 错误签名压测。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4165:+这些应等签名、租户、字段映射确认后再做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4169:+必须由平台部、学工系统管理员或接口开通记录提供真实 `tenantCode`。不要把文档样例 `C10026` 当成本校租户。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4185:+XG_USER_API_URL
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4186:+XG_USER_API_APP_KEY
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4187:+XG_USER_API_APP_SECRET
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4188:+XG_USER_API_TENANT_CODE
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4189:+XG_USER_API_ENCRYPTION_TYPE=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4190:+XG_RUN_LIVE_API_TEST=0
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4213:+- `auth_failed`：HTTP 401/403 或业务错误提示签名失败，输出当前算法名和非敏感参数。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4218:+不要对认证失败做大量重试。签名错误重试越多，越可能触发风控或污染审计。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4236:+- 获得签名校验文档或固定签名样例。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4244:+- `xg_user_client.py` 支持候选签名算法、请求构造、响应解析。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4245:+- `xg_user_api_probe.py` 可通过环境变量运行，默认只请求 `page=1&pageNum=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4260:+- 仅在 `XG_RUN_LIVE_API_TEST=1` 时执行。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4279:+- **实现可mock的客户端单元测试，覆盖签名候选和响应解析。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4281:+- **签名和租户确认前，不启动生产数据读取实现。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4343:+2. **P1：签名算法不能靠猜测进入正式实现；最多允许在一次性诊断脚本中按候选算法快速验证，正式代码必须等待平台部提供签名校验文档或可确认的样例。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4345:+另外，`docs/api说明.txt` 的官方样式文档只给出 `sign`、`timestamp`、`randStr`、`encryptionType` 字段，但缺少“签名校验部分”；`tenantCode` 也只有示例值 `C10026`。因此第一阶段的目标应调整为“受控验证接口合同”，不是直接实现生产数据同步。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4359:+- 将文档中的凭证替换为占位符，例如 `${XG_APP_KEY}`、`${XG_APP_SECRET}`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4364:+### P1：签名算法缺失，不能作为正式实现假设
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4370:+当前文档明确写“请参见签名校验部分”，但仓库内文档没有该部分。候选算法 A/B/C 都只是合理猜测，不能作为生产实现依据。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4374:+- 向平台部索要签名校验文档，至少需要：参与签名的字段、字段顺序、是否包含 form-data、secret位置、大小写、编码、输出hex/base64、时间戳单位、randStr长度、签名有效窗口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4375:+- 同时索要一个固定样例：固定 appKey、timestamp、randStr、tenantCode、appSecret 和期望 sign。没有固定样例时，算法验证成本会显著上升。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4402:+- 从平台部或学工系统管理员处获取本校真实 `tenantCode`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4415:+- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4416:+- 真实API测试必须通过显式开关启用，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4422:+### 1. 签名算法推断
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4424:+在没有官方签名校验章节前，最可能的顺序建议如下：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4426:+1. **参数排序SHA1/MD5：** 将参与签名参数按key排序后拼接，再追加或混入 `appSecret`。很多开放平台采用这种方式，且文档提供 `encryptionType=sha1|md5` 更像普通摘要算法选择，而不是HMAC选择。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4427:+2. **拼接SHA1/MD5：** `SHA1(appKey + timestamp + randStr + appSecret)` 或 `SHA1(appSecret + appKey + timestamp + randStr)`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4428:+3. **HMAC-SHA1：** 技术上更好，但如果文档只称 `encryptionType` 为 `sha1/md5`，而不是 `hmac-sha1`，优先级略低。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4444:+backend/scripts/xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4445:+backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4446:+backend/apps/users/tests/test_xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4451:+- `xg_user_api_probe.py`：人工运行的诊断入口，读取环境变量，支持 `--algorithm`、`--page-size 1`、`--timeout`、`--dry-run`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4452:+- `xg_user_client.py`：可复用客户端，负责签名、请求构造、响应解析、错误归一化；后续可接入 `RealUserDataProvider`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4453:+- `test_xg_user_client.py`：mock HTTP响应，覆盖签名候选、字段解析、错误处理，不调用真实网络。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4462:+2. 请求构造：header/form-data完整，timestamp/randStr/sign存在。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4463:+3. 认证验证：用最小请求验证签名算法。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4472:+- 错误签名压测。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4475:+这些应等签名、租户、字段映射确认后再做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4479:+必须由平台部、学工系统管理员或接口开通记录提供真实 `tenantCode`。不要把文档样例 `C10026` 当成本校租户。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4495:+XG_USER_API_URL
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4496:+XG_USER_API_APP_KEY
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4497:+XG_USER_API_APP_SECRET
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4498:+XG_USER_API_TENANT_CODE
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4499:+XG_USER_API_ENCRYPTION_TYPE=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4500:+XG_RUN_LIVE_API_TEST=0
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4523:+- `auth_failed`：HTTP 401/403 或业务错误提示签名失败，输出当前算法名和非敏感参数。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4528:+不要对认证失败做大量重试。签名错误重试越多，越可能触发风控或污染审计。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4546:+- 获得签名校验文档或固定签名样例。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4554:+- `xg_user_client.py` 支持候选签名算法、请求构造、响应解析。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4555:+- `xg_user_api_probe.py` 可通过环境变量运行，默认只请求 `page=1&pageNum=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4570:+- 仅在 `XG_RUN_LIVE_API_TEST=1` 时执行。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4589:+- **实现可mock的客户端单元测试，覆盖签名候选和响应解析。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4591:+- **签名和租户确认前，不启动生产数据读取实现。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4881:+2. **P1：签名算法不能靠猜测进入正式实现；最多允许在一次性诊断脚本中按候选算法快速验证，正式代码必须等待平台部提供签名校验文档或可确认的样例。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4883:+另外，`docs/api说明.txt` 的官方样式文档只给出 `sign`、`timestamp`、`randStr`、`encryptionType` 字段，但缺少“签名校验部分”；`tenantCode` 也只有示例值 `C10026`。因此第一阶段的目标应调整为“受控验证接口合同”，不是直接实现生产数据同步。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4897:+- 将文档中的凭证替换为占位符，例如 `${XG_APP_KEY}`、`${XG_APP_SECRET}`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4902:+### P1：签名算法缺失，不能作为正式实现假设
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4908:+当前文档明确写“请参见签名校验部分”，但仓库内文档没有该部分。候选算法 A/B/C 都只是合理猜测，不能作为生产实现依据。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4912:+- 向平台部索要签名校验文档，至少需要：参与签名的字段、字段顺序、是否包含 form-data、secret位置、大小写、编码、输出hex/base64、时间戳单位、randStr长度、签名有效窗口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4913:+- 同时索要一个固定样例：固定 appKey、timestamp、randStr、tenantCode、appSecret 和期望 sign。没有固定样例时，算法验证成本会显著上升。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4940:+- 从平台部或学工系统管理员处获取本校真实 `tenantCode`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4953:+- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4954:+- 真实API测试必须通过显式开关启用，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4960:+### 1. 签名算法推断
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4962:+在没有官方签名校验章节前，最可能的顺序建议如下：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4964:+1. **参数排序SHA1/MD5：** 将参与签名参数按key排序后拼接，再追加或混入 `appSecret`。很多开放平台采用这种方式，且文档提供 `encryptionType=sha1|md5` 更像普通摘要算法选择，而不是HMAC选择。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4965:+2. **拼接SHA1/MD5：** `SHA1(appKey + timestamp + randStr + appSecret)` 或 `SHA1(appSecret + appKey + timestamp + randStr)`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4966:+3. **HMAC-SHA1：** 技术上更好，但如果文档只称 `encryptionType` 为 `sha1/md5`，而不是 `hmac-sha1`，优先级略低。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4982:+backend/scripts/xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4983:+backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4984:+backend/apps/users/tests/test_xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4989:+- `xg_user_api_probe.py`：人工运行的诊断入口，读取环境变量，支持 `--algorithm`、`--page-size 1`、`--timeout`、`--dry-run`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4990:+- `xg_user_client.py`：可复用客户端，负责签名、请求构造、响应解析、错误归一化；后续可接入 `RealUserDataProvider`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:4991:+- `test_xg_user_client.py`：mock HTTP响应，覆盖签名候选、字段解析、错误处理，不调用真实网络。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5000:+2. 请求构造：header/form-data完整，timestamp/randStr/sign存在。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5001:+3. 认证验证：用最小请求验证签名算法。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5010:+- 错误签名压测。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5013:+这些应等签名、租户、字段映射确认后再做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5017:+必须由平台部、学工系统管理员或接口开通记录提供真实 `tenantCode`。不要把文档样例 `C10026` 当成本校租户。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5033:+XG_USER_API_URL
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5034:+XG_USER_API_APP_KEY
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5035:+XG_USER_API_APP_SECRET
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5036:+XG_USER_API_TENANT_CODE
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5037:+XG_USER_API_ENCRYPTION_TYPE=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5038:+XG_RUN_LIVE_API_TEST=0
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5061:+- `auth_failed`：HTTP 401/403 或业务错误提示签名失败，输出当前算法名和非敏感参数。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5066:+不要对认证失败做大量重试。签名错误重试越多，越可能触发风控或污染审计。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5084:+- 获得签名校验文档或固定签名样例。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5092:+- `xg_user_client.py` 支持候选签名算法、请求构造、响应解析。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5093:+- `xg_user_api_probe.py` 可通过环境变量运行，默认只请求 `page=1&pageNum=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5108:+- 仅在 `XG_RUN_LIVE_API_TEST=1` 时执行。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5127:+- **实现可mock的客户端单元测试，覆盖签名候选和响应解析。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5129:+- **签名和租户确认前，不启动生产数据读取实现。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5164:+2. **P1：签名算法不能靠猜测进入正式实现；最多允许在一次性诊断脚本中按候选算法快速验证，正式代码必须等待平台部提供签名校验文档或可确认的样例。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5166:+另外，`docs/api说明.txt` 的官方样式文档只给出 `sign`、`timestamp`、`randStr`、`encryptionType` 字段，但缺少“签名校验部分”；`tenantCode` 也只有示例值 `C10026`。因此第一阶段的目标应调整为“受控验证接口合同”，不是直接实现生产数据同步。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5180:+- 将文档中的凭证替换为占位符，例如 `${XG_APP_KEY}`、`${XG_APP_SECRET}`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5185:+### P1：签名算法缺失，不能作为正式实现假设
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5191:+当前文档明确写“请参见签名校验部分”，但仓库内文档没有该部分。候选算法 A/B/C 都只是合理猜测，不能作为生产实现依据。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5195:+- 向平台部索要签名校验文档，至少需要：参与签名的字段、字段顺序、是否包含 form-data、secret位置、大小写、编码、输出hex/base64、时间戳单位、randStr长度、签名有效窗口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5196:+- 同时索要一个固定样例：固定 appKey、timestamp、randStr、tenantCode、appSecret 和期望 sign。没有固定样例时，算法验证成本会显著上升。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5223:+- 从平台部或学工系统管理员处获取本校真实 `tenantCode`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5236:+- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5237:+- 真实API测试必须通过显式开关启用，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5243:+### 1. 签名算法推断
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5245:+在没有官方签名校验章节前，最可能的顺序建议如下：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5247:+1. **参数排序SHA1/MD5：** 将参与签名参数按key排序后拼接，再追加或混入 `appSecret`。很多开放平台采用这种方式，且文档提供 `encryptionType=sha1|md5` 更像普通摘要算法选择，而不是HMAC选择。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5248:+2. **拼接SHA1/MD5：** `SHA1(appKey + timestamp + randStr + appSecret)` 或 `SHA1(appSecret + appKey + timestamp + randStr)`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5249:+3. **HMAC-SHA1：** 技术上更好，但如果文档只称 `encryptionType` 为 `sha1/md5`，而不是 `hmac-sha1`，优先级略低。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5265:+backend/scripts/xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5266:+backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5267:+backend/apps/users/tests/test_xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5272:+- `xg_user_api_probe.py`：人工运行的诊断入口，读取环境变量，支持 `--algorithm`、`--page-size 1`、`--timeout`、`--dry-run`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5273:+- `xg_user_client.py`：可复用客户端，负责签名、请求构造、响应解析、错误归一化；后续可接入 `RealUserDataProvider`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5274:+- `test_xg_user_client.py`：mock HTTP响应，覆盖签名候选、字段解析、错误处理，不调用真实网络。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5283:+2. 请求构造：header/form-data完整，timestamp/randStr/sign存在。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5284:+3. 认证验证：用最小请求验证签名算法。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5293:+- 错误签名压测。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5296:+这些应等签名、租户、字段映射确认后再做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5300:+必须由平台部、学工系统管理员或接口开通记录提供真实 `tenantCode`。不要把文档样例 `C10026` 当成本校租户。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5316:+XG_USER_API_URL
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5317:+XG_USER_API_APP_KEY
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5318:+XG_USER_API_APP_SECRET
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5319:+XG_USER_API_TENANT_CODE
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5320:+XG_USER_API_ENCRYPTION_TYPE=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5321:+XG_RUN_LIVE_API_TEST=0
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5344:+- `auth_failed`：HTTP 401/403 或业务错误提示签名失败，输出当前算法名和非敏感参数。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5349:+不要对认证失败做大量重试。签名错误重试越多，越可能触发风控或污染审计。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5367:+- 获得签名校验文档或固定签名样例。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5375:+- `xg_user_client.py` 支持候选签名算法、请求构造、响应解析。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5376:+- `xg_user_api_probe.py` 可通过环境变量运行，默认只请求 `page=1&pageNum=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5391:+- 仅在 `XG_RUN_LIVE_API_TEST=1` 时执行。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5410:+- **实现可mock的客户端单元测试，覆盖签名候选和响应解析。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-69-api-data-reading-test-2026-06-02T03-00-05-106Z.md:5412:+- **签名和租户确认前，不启动生产数据读取实现。**
.omc/collaboration/artifacts/20260530-0959-codex-phase3-independent-review.md:190:   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:20:   - 审批权限：只校验approver_id够吗？是否需要校验class_id？学工部D001硬编码怎么办？
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:26:4. **遗漏问题：** 列表接口真的可以推迟吗？没有列表接口，辅导员/学工部怎么知道有哪些申请需要审批？Day 2能达到可重复验收吗？
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:54:   - 审批权限：只校验approver_id够吗？是否需要校验class_id？学工部D001硬编码怎么办？
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:60:4. **遗漏问题：** 列表接口真的可以推迟吗？没有列表接口，辅导员/学工部怎么知道有哪些申请需要审批？Day 2能达到可重复验收吗？
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:87:- **列表接口不应推迟**。没有列表接口，辅导员/学工部无法发现待审批申请，验收仍依赖内部ID或查库，不是可重复验收。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:88:- **只校验`approver_id`不够**：还要校验角色、辅导员班级映射、学工部审批人来源，并同步修详情查看权限。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:120:   - 审批权限：只校验approver_id够吗？是否需要校验class_id？学工部D001硬编码怎么办？
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:126:4. **遗漏问题：** 列表接口真的可以推迟吗？没有列表接口，辅导员/学工部怎么知道有哪些申请需要审批？Day 2能达到可重复验收吗？
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:958:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:1002:- 学工部审批是否也需要权限校验？（当前硬编码D001）
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:1041:- 学工部如何知道有哪些申请需要审批？
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:1141:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:1175:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:1374:        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:1412:        # Step 5: 学工部登录
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:1419:        # Step 6: 学工部审批通过
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:1605:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:1639:                ('step', models.CharField(choices=[('counselor', '辅导员'), ('dean', '学工部')], max_length=20)),
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:1767:     8	    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:1965:+计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:1977:+| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2011:+- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2013:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2014:+- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2081:+- 学工部：只看分配给自己的`pending_dean`待办。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2088:+1. **查看权限漏洞被遗漏。** `get_application`只限制学生，未限制辅导员/学工部访问范围。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2112:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2165:+计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2177:+| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2211:+- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2213:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2214:+- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2281:+- 学工部：只看分配给自己的`pending_dean`待办。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2288:+1. **查看权限漏洞被遗漏。** `get_application`只限制学生，未限制辅导员/学工部访问范围。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2312:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2428:+计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2440:+| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2474:+- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2476:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2477:+- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2544:+- 学工部：只看分配给自己的`pending_dean`待办。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2551:+1. **查看权限漏洞被遗漏。** `get_application`只限制学生，未限制辅导员/学工部访问范围。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2575:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2631:+计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2643:+| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2677:+- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2679:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2680:+- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2747:+- 学工部：只看分配给自己的`pending_dean`待办。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2754:+1. **查看权限漏洞被遗漏。** `get_application`只限制学生，未限制辅导员/学工部访问范围。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2778:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2835:计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2847:| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2881:- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2883:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2884:- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2951:- 学工部：只看分配给自己的`pending_dean`待办。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2958:1. **查看权限漏洞被遗漏。** `get_application`只限制学生，未限制辅导员/学工部访问范围。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2982:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3037:+计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3049:+| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3083:+- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3085:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3086:+- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3153:+- 学工部：只看分配给自己的`pending_dean`待办。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3160:+1. **查看权限漏洞被遗漏。** `get_application`只限制学生，未限制辅导员/学工部访问范围。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3184:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3229:- **列表接口不应推迟**。没有列表接口，辅导员/学工部无法发现待审批申请，验收仍依赖内部ID或查库，不是可重复验收。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3230:- **只校验`approver_id`不够**：还要校验角色、辅导员班级映射、学工部审批人来源，并同步修详情查看权限。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3256:+计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3268:+| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3302:+- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3304:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3305:+- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3372:+- 学工部：只看分配给自己的`pending_dean`待办。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3379:+1. **查看权限漏洞被遗漏。** `get_application`只限制学生，未限制辅导员/学工部访问范围。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3403:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:30:   [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:180) 已明确 Day 3 触发条件、砍学工部审批、Day 4 保“提交→辅导员审批→查询”闭环、学工部审批推到 Week 2 Day 1，不再存在原先“砍掉又补回”的矛盾。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:593:2. **P1-2：降级方案逻辑矛盾** - 风险2说"砍学工部审批"又说"Day 4补学工部审批"
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:619:降级方案：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:624:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:627:**验证点：** 降级逻辑现在清晰：Day 3触发→砍学工部→Day 4验证辅导员闭环→学工部推Week 2 Day 1
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:832:> 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:834:这里“砍学工部审批”和“Day 4补学工部审批”同时出现，口径冲突。更合理的表达是：
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:836:> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:871:**问题：** 同一句话同时说“砍学工部审批”和“Day 4补学工部审批”。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:875:**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:918:2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:967:/bin/bash -lc 'rtk rg -n "降级方案|学工部|Day 3|Day 4|Week 2|纵向|闭环" docs/plans/week-0-1-execution-plan.md' in /home/caohui/projects/graduation-leave-system
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:970:36:- [ ] 生成seed数据（10学生 + 2辅导员 + 1学工部 + 边界样本 + 默认密码）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:973:75:- [ ] Seed数据加载成功（10学生 + 2辅导员 + 1学工部）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:976:92:  - 创建学工部审批记录（通过时）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:977:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:978:94:  - 最小角色校验：只有学工部可审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:979:97:  - 最小角色校验：学生只能查自己，辅导员/学工部可查所有
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:980:108:- [ ] 学工部可审批（通过/驳回）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:981:113:- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:982:114:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:983:120:  - 测试1：学生登录 → 提交申请 → 辅导员审批通过 → 学工部审批通过 → 查询状态
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:989:180:**降级方案：** 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:990:182:### 风险3：Week 1 Day 4学工部审批未完成
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1079:**问题：** 风险2降级方案说"砍学工部审批，Day 4补学工部审批"，逻辑矛盾
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1085:降级方案：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1090:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1093:**验证：** 降级方案现在明确：Day 3触发后砍学工部审批，Day 4验证辅导员闭环，学工部推Week 2 Day 1
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1194:    92	  - 创建学工部审批记录（通过时）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1195:    93	- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1196:    94	  - 最小角色校验：只有学工部可审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1199:    97	  - 最小角色校验：学生只能查自己，辅导员/学工部可查所有
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1210:   108	- [ ] 学工部可审批（通过/驳回）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1215:   113	- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1216:   114	- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1222:   120	  - 测试1：学生登录 → 提交申请 → 辅导员审批通过 → 学工部审批通过 → 查询状态
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1237:   180	**降级方案：** 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1239:   182	### 风险3：Week 1 Day 4学工部审批未完成
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1380:+**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1437:+如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1443:+2. 砍范围明确：砍学工部审批。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1445:+4. 顺延范围明确：学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1493:+**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1550:+如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1556:+2. 砍范围明确：砍学工部审批。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1558:+4. 顺延范围明确：学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1605:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1662:如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1668:2. 砍范围明确：砍学工部审批。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1670:4. 顺延范围明确：学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1763:+**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1820:+如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1826:+2. 砍范围明确：砍学工部审批。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1828:+4. 顺延范围明确：学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1870:   [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:180) 已明确 Day 3 触发条件、砍学工部审批、Day 4 保“提交→辅导员审批→查询”闭环、学工部审批推到 Week 2 Day 1，不再存在原先“砍掉又补回”的矛盾。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1894:+**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1951:+如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1957:+2. 砍范围明确：砍学工部审批。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1959:+4. 顺延范围明确：学工部审批推到Week 2 Day 1。
docs/api/notification-contract-v0.1.md:34:| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
docs/api/notification-contract-v0.1.md:35:| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
docs/api/notification-contract-v0.1.md:36:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
docs/api/notification-contract-v0.1.md:58:**触发条件：** 辅导员或学工部审批通过
docs/api/notification-contract-v0.1.md:64:- 正文：`您的离校申请已通过{approver_role}审批。` （approver_role: 辅导员/学工部）
docs/api/notification-contract-v0.1.md:74:**触发条件：** 辅导员或学工部驳回申请
docs/api/notification-contract-v0.1.md:90:**触发条件：** 审批超过规定时限（辅导员3自然日，学工部2自然日）未处理
docs/api/notification-contract-v0.1.md:92:**接收者：** 待审批的辅导员/学工部
docs/api/notification-contract-v0.1.md:304:| 操作 | 学生 | 辅导员 | 学工部 | 说明 |
docs/api/contract-v0.2.md:20:| `pending_dean` | Awaiting dean approval | 待学工部审批 |
docs/api/contract-v0.2.md:41:| `dean` | Dean approval step | 学工部审批 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:22:核心结论：批准继续 Step 1，但建议改为分步实现诊断客户端：先签名与配置测试，再请求构造/响应解析 mock 测试，最后诊断脚本；真实 live call 必须等本校 `tenantCode` 且显式开启 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:106:- ✅ **签名算法已确认**（用户提供官方算法）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:118:backend/apps/users/integrations/xg_user_client.py   # 客户端
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:119:backend/scripts/xg_user_api_probe.py                # 诊断脚本
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:120:backend/apps/users/tests/test_xg_user_client.py     # Mock测试
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:124:1. 签名函数（基于确认的官方算法）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:159:### 问题2：签名算法是否需要单独验证模块？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:161:**背景：** 用户提供的签名示例使用不同的AppSecret。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:164:- appSecret: `6bd1b3fb015b4e72a85769e9d64405d1`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:166:- randStr: `Gc6LGToDKy2AMhXE`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:169:**选项A：** 客户端内置签名函数，测试时用官方样例验证
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:173:**选项B：** 先实现独立签名验证脚本，确认算法正确后再集成
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:186:1. 签名客户端（核心）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:198:  - B1: 先只实现签名函数 + 官方样例验证
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:205:  - 只实现签名验证脚本
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:254:✓ 签名生成: baea...4515
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1086:randStr	是	string	随机字符串
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1087:sign	是	string	认证签名，请参见签名校验部分
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1088:encryptionType	否	string	加密类型 只有 sha1和md5 不传默认 sha1 方式加密
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1096:number	否	string	学工号
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1294:### 1. 签名算法已确认
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1296:**Codex担心：** 签名算法缺失，不能靠猜测实现。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1298:**用户提供：** 官方签名算法（字典排序+拼接+sha1/md5）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1322:backend/scripts/xg_user_api_probe.py        # 诊断脚本
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1323:backend/apps/users/integrations/xg_user_client.py   # 客户端
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1324:backend/apps/users/tests/test_xg_user_client.py     # Mock测试
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1388:完全接受Codex审查意见，并补充一个关键进展：**用户已提供官方签名算法**。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1410:### P1：签名算法问题（已解决）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1412:**Codex指出：** 签名算法缺失，不能靠猜测实现。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1414:**Claude确认：** **问题已解决！用户在审查过程中提供了官方签名算法。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1416:**官方签名算法（已确认）：**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1419:签名规则：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1420:1. 将 appSecret, timestamp, randStr 三个参数值进行字典排序（sort）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1425:appSecret: 6bd1b3fb015b4e72a85769e9d64405d1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1427:randStr: Gc6LGToDKy2AMhXE
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1438:def generate_sign(app_secret: str, timestamp: str, rand_str: str, 
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1439:                  encryption_type: str = 'sha1') -> str:
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1441:    生成API签名
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1447:        encryption_type: 加密类型，'sha1'或'md5'，默认'sha1'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1450:        签名字符串（十六进制小写）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1460:    if encryption_type == 'md5':
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1481:3. 通过环境变量 `XG_USER_API_URL` 配置
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1494:1. 通过环境变量 `XG_USER_API_TENANT_CODE` 配置
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1509:1. 独立诊断脚本: `backend/scripts/xg_user_api_probe.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1510:2. 可Mock客户端: `backend/apps/users/integrations/xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1511:3. Mock单元测试: `backend/apps/users/tests/test_xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1512:4. 真实API测试通过 `XG_RUN_LIVE_API_TEST=1` 门禁
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1537:- AppId: ${XG_USER_API_APP_ID}
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1538:- AppKey: ${XG_USER_API_APP_KEY}
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1539:- AppSecret: ${XG_USER_API_APP_SECRET}
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1552:# 学工系统用户信息API配置
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1556:XG_USER_API_URL=https://xuegongmj.hgnu.edu.cn/api/open-api/user-center/tenant/auth-user-info
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1559:XG_USER_API_APP_ID=your_app_id_here
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1560:XG_USER_API_APP_KEY=your_app_key_here
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1561:XG_USER_API_APP_SECRET=your_app_secret_here
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1564:XG_USER_API_TENANT_CODE=your_tenant_code_here
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1567:XG_USER_API_ENCRYPTION_TYPE=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1570:XG_RUN_LIVE_API_TEST=0
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1607:1. 实现 `backend/apps/users/integrations/xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1608:   - 签名函数（已确认算法）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1613:2. 实现 `backend/scripts/xg_user_api_probe.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1620:- 签名函数通过官方样例验证
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1629:1. 实现 `backend/apps/users/tests/test_xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1636:- 测试覆盖签名生成、请求构造、响应解析
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1659:2. **P1：签名算法不能靠猜测进入正式实现；最多允许在一次性诊断脚本中按候选算法快速验证，正式代码必须等待平台部提供签名校验文档或可确认的样例。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1661:另外，`docs/api说明.txt` 的官方样式文档只给出 `sign`、`timestamp`、`randStr`、`encryptionType` 字段，但缺少“签名校验部分”；`tenantCode` 也只有示例值 `C10026`。因此第一阶段的目标应调整为“受控验证接口合同”，不是直接实现生产数据同步。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1675:- 将文档中的凭证替换为占位符，例如 `${XG_APP_KEY}`、`${XG_APP_SECRET}`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1680:### P1：签名算法缺失，不能作为正式实现假设
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1686:当前文档明确写“请参见签名校验部分”，但仓库内文档没有该部分。候选算法 A/B/C 都只是合理猜测，不能作为生产实现依据。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1690:- 向平台部索要签名校验文档，至少需要：参与签名的字段、字段顺序、是否包含 form-data、secret位置、大小写、编码、输出hex/base64、时间戳单位、randStr长度、签名有效窗口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1691:- 同时索要一个固定样例：固定 appKey、timestamp、randStr、tenantCode、appSecret 和期望 sign。没有固定样例时，算法验证成本会显著上升。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1718:- 从平台部或学工系统管理员处获取本校真实 `tenantCode`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1731:- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1732:- 真实API测试必须通过显式开关启用，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1738:### 1. 签名算法推断
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1740:在没有官方签名校验章节前，最可能的顺序建议如下：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1742:1. **参数排序SHA1/MD5：** 将参与签名参数按key排序后拼接，再追加或混入 `appSecret`。很多开放平台采用这种方式，且文档提供 `encryptionType=sha1|md5` 更像普通摘要算法选择，而不是HMAC选择。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1743:2. **拼接SHA1/MD5：** `SHA1(appKey + timestamp + randStr + appSecret)` 或 `SHA1(appSecret + appKey + timestamp + randStr)`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1744:3. **HMAC-SHA1：** 技术上更好，但如果文档只称 `encryptionType` 为 `sha1/md5`，而不是 `hmac-sha1`，优先级略低。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1760:backend/scripts/xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1761:backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1762:backend/apps/users/tests/test_xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1767:- `xg_user_api_probe.py`：人工运行的诊断入口，读取环境变量，支持 `--algorithm`、`--page-size 1`、`--timeout`、`--dry-run`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1768:- `xg_user_client.py`：可复用客户端，负责签名、请求构造、响应解析、错误归一化；后续可接入 `RealUserDataProvider`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1769:- `test_xg_user_client.py`：mock HTTP响应，覆盖签名候选、字段解析、错误处理，不调用真实网络。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1778:2. 请求构造：header/form-data完整，timestamp/randStr/sign存在。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1779:3. 认证验证：用最小请求验证签名算法。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1788:- 错误签名压测。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1791:这些应等签名、租户、字段映射确认后再做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1795:必须由平台部、学工系统管理员或接口开通记录提供真实 `tenantCode`。不要把文档样例 `C10026` 当成本校租户。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1811:XG_USER_API_URL
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1812:XG_USER_API_APP_KEY
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1813:XG_USER_API_APP_SECRET
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1814:XG_USER_API_TENANT_CODE
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1815:XG_USER_API_ENCRYPTION_TYPE=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1816:XG_RUN_LIVE_API_TEST=0
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1839:- `auth_failed`：HTTP 401/403 或业务错误提示签名失败，输出当前算法名和非敏感参数。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1844:不要对认证失败做大量重试。签名错误重试越多，越可能触发风控或污染审计。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1862:- 获得签名校验文档或固定签名样例。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1870:- `xg_user_client.py` 支持候选签名算法、请求构造、响应解析。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1871:- `xg_user_api_probe.py` 可通过环境变量运行，默认只请求 `page=1&pageNum=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1886:- 仅在 `XG_RUN_LIVE_API_TEST=1` 时执行。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1923:docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:36:backend/apps/users/integrations/xg_user_client.py   # 客户端
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1924:docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:37:backend/scripts/xg_user_api_probe.py                # 诊断脚本
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1925:docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:38:backend/apps/users/tests/test_xg_user_client.py     # Mock测试
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1926:docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:45:backend/scripts/xg_user_api_probe.py        # 诊断脚本
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1927:docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:46:backend/apps/users/integrations/xg_user_client.py   # 客户端
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1928:docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:47:backend/apps/users/tests/test_xg_user_client.py     # Mock测试
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1931:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:104:3. 通过环境变量 `XG_USER_API_URL` 配置
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1932:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:117:1. 通过环境变量 `XG_USER_API_TENANT_CODE` 配置
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1933:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:132:1. 独立诊断脚本: `backend/scripts/xg_user_api_probe.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1934:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:133:2. 可Mock客户端: `backend/apps/users/integrations/xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1935:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:134:3. Mock单元测试: `backend/apps/users/tests/test_xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1936:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:135:4. 真实API测试通过 `XG_RUN_LIVE_API_TEST=1` 门禁
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1937:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:160:- AppId: ${XG_USER_API_APP_ID}
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1938:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:161:- AppKey: ${XG_USER_API_APP_KEY}
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1939:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:162:- AppSecret: ${XG_USER_API_APP_SECRET}
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1940:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:179:XG_USER_API_URL=https://xuegongmj.hgnu.edu.cn/api/open-api/user-center/tenant/auth-user-info
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1941:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:182:XG_USER_API_APP_ID=your_app_id_here
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1942:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:183:XG_USER_API_APP_KEY=your_app_key_here
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1943:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:184:XG_USER_API_APP_SECRET=your_app_secret_here
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1944:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:187:XG_USER_API_TENANT_CODE=your_tenant_code_here
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1945:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:190:XG_USER_API_ENCRYPTION_TYPE=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1946:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:193:XG_RUN_LIVE_API_TEST=0
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1947:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:230:1. 实现 `backend/apps/users/integrations/xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1948:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:236:2. 实现 `backend/scripts/xg_user_api_probe.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1949:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:252:1. 实现 `backend/apps/users/tests/test_xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1950:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:269:2. 设置 `XG_RUN_LIVE_API_TEST=1`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1951:docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:270:3. 运行 `xg_user_api_probe.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1952:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:20:另外，`docs/api说明.txt` 的官方样式文档只给出 `sign`、`timestamp`、`randStr`、`encryptionType` 字段，但缺少“签名校验部分”；`tenantCode` 也只有示例值 `C10026`。因此第一阶段的目标应调整为“受控验证接口合同”，不是直接实现生产数据同步。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1953:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:34:- 将文档中的凭证替换为占位符，例如 `${XG_APP_KEY}`、`${XG_APP_SECRET}`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1954:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:50:- 同时索要一个固定样例：固定 appKey、timestamp、randStr、tenantCode、appSecret 和期望 sign。没有固定样例时，算法验证成本会显著上升。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1957:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:77:- 从平台部或学工系统管理员处获取本校真实 `tenantCode`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1959:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:91:- 真实API测试必须通过显式开关启用，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1960:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:119:backend/scripts/xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1961:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:120:backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1962:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:121:backend/apps/users/tests/test_xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1963:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:126:- `xg_user_api_probe.py`：人工运行的诊断入口，读取环境变量，支持 `--algorithm`、`--page-size 1`、`--timeout`、`--dry-run`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1964:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:127:- `xg_user_client.py`：可复用客户端，负责签名、请求构造、响应解析、错误归一化；后续可接入 `RealUserDataProvider`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1965:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:128:- `test_xg_user_client.py`：mock HTTP响应，覆盖签名候选、字段解析、错误处理，不调用真实网络。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1966:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:154:必须由平台部、学工系统管理员或接口开通记录提供真实 `tenantCode`。不要把文档样例 `C10026` 当成本校租户。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1968:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:170:XG_USER_API_URL
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1969:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:171:XG_USER_API_APP_KEY
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1970:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:172:XG_USER_API_APP_SECRET
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1971:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:173:XG_USER_API_TENANT_CODE
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1972:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:174:XG_USER_API_ENCRYPTION_TYPE=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1973:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:175:XG_RUN_LIVE_API_TEST=0
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1976:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:229:- `xg_user_client.py` 支持候选签名算法、请求构造、响应解析。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1977:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:230:- `xg_user_api_probe.py` 可通过环境变量运行，默认只请求 `page=1&pageNum=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1978:docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:245:- 仅在 `XG_RUN_LIVE_API_TEST=1` 时执行。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1980:docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:26:- AppId: ${XG_USER_API_APP_ID}
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1981:docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:27:- AppKey: ${XG_USER_API_APP_KEY}
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:1982:docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:28:- AppSecret: ${XG_USER_API_APP_SECRET}
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2021:# 学工系统用户信息API配置
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2025:XG_USER_API_URL=https://xuegongmj.hgnu.edu.cn/api/open-api/user-center/tenant/auth-user-info
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2028:XG_USER_API_APP_ID=your_app_id_here
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2029:XG_USER_API_APP_KEY=your_app_key_here
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2030:XG_USER_API_APP_SECRET=your_app_secret_here
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2033:XG_USER_API_TENANT_CODE=your_tenant_code_here
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2036:XG_USER_API_ENCRYPTION_TYPE=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2039:XG_RUN_LIVE_API_TEST=0
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2376:+Step 0 安全修正已经完成，签名算法也已有官方样例，可以开始写代码；但 `tenantCode` 仍未确认，真实接口字段也未验证。因此下一步的最优路径不是等待，也不是直接接入业务 Provider，而是先交付一个可离线验证、可 mock 测试、可人工 live probe 的最小诊断层。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2381:+2. **签名函数必须先用官方样例固化为单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2396:+- `generate_sign()`、请求构造、响应解析、错误归一化、mock 测试可以立即做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2397:+- `xg_user_api_probe.py` 可以立即做，但缺少 `XG_USER_API_TENANT_CODE` 时只能执行配置校验、签名样例验证、`--dry-run` 请求摘要，不能发起网络请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2398:+- live probe 必须等 `tenantCode` 到位，并且需要操作者显式确认，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2402:+### 问题2：签名算法是否需要单独验证模块？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2404:+**建议：选项 A，但把签名函数设计成独立纯函数，并把官方样例作为 P0 单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2406:+不需要额外创建一次性签名验证脚本。更好的边界是：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2409:+backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2410:+  - generate_sign(app_secret, timestamp, rand_str, encryption_type="sha1")
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2416:+- `appSecret=6bd1b3fb015b4e72a85769e9d64405d1`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2418:+- `randStr=Gc6LGToDKy2AMhXE`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2423:+- 字典排序对象是三个**参数值**：`appSecret`、`timestamp`、`randStr`，不是参数名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2426:+- 不把 `tenantCode`、`appKey`、form-data 混入签名，除非后续官方文档另行确认。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2434:+**B1：签名与配置切片**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2437:+- 实现 `generate_sign()`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2439:+- 单元测试覆盖官方签名样例、md5、非法 `encryptionType`、缺失必填环境变量。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2450:+- `backend/scripts/xg_user_api_probe.py` 作为人工诊断入口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2484:+签名样例: OK
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2485:+Live调用: skipped (missing tenantCode or XG_RUN_LIVE_API_TEST != 1)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2486:+请求摘要: POST /auth-user-info page=1 pageNum=1 encryptionType=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2499:+JSON 输出不能包含 `appSecret`、完整 `sign`、完整手机号、身份证、微信 openId。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2507:+`docs/api说明.txt` 的 header 参数是 `appKey`，没有 `appId`。`backend/.env.example` 已包含 `XG_USER_API_APP_ID`，可以保留用于记录平台凭证，但请求构造不要默认发送 `appId`。若平台部确认学校网关还要求 `appId`，再显式加入 header。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2546:+### Step 1A：签名与配置，先做
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2551:+- `backend/apps/users/integrations/xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2552:+- `backend/apps/users/tests/test_xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2556:+- 官方签名样例通过。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2557:+- 缺失 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 时有明确错误。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2558:+- `tenantCode` 缺失不影响签名样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2571:+- header 包含 `appKey/timestamp/randStr/sign/encryptionType`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2580:+- `backend/scripts/xg_user_api_probe.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2587:+- `XG_RUN_LIVE_API_TEST=1` 且配置齐全时才允许发请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2606:+  generate_sign
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2608:+  xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2627:+1. 先做 `generate_sign()` 和官方样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2655:+Step 0 安全修正已经完成，签名算法也已有官方样例，可以开始写代码；但 `tenantCode` 仍未确认，真实接口字段也未验证。因此下一步的最优路径不是等待，也不是直接接入业务 Provider，而是先交付一个可离线验证、可 mock 测试、可人工 live probe 的最小诊断层。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2660:+2. **签名函数必须先用官方样例固化为单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2675:+- `generate_sign()`、请求构造、响应解析、错误归一化、mock 测试可以立即做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2676:+- `xg_user_api_probe.py` 可以立即做，但缺少 `XG_USER_API_TENANT_CODE` 时只能执行配置校验、签名样例验证、`--dry-run` 请求摘要，不能发起网络请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2677:+- live probe 必须等 `tenantCode` 到位，并且需要操作者显式确认，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2681:+### 问题2：签名算法是否需要单独验证模块？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2683:+**建议：选项 A，但把签名函数设计成独立纯函数，并把官方样例作为 P0 单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2685:+不需要额外创建一次性签名验证脚本。更好的边界是：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2688:+backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2689:+  - generate_sign(app_secret, timestamp, rand_str, encryption_type="sha1")
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2695:+- `appSecret=6bd1b3fb015b4e72a85769e9d64405d1`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2697:+- `randStr=Gc6LGToDKy2AMhXE`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2702:+- 字典排序对象是三个**参数值**：`appSecret`、`timestamp`、`randStr`，不是参数名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2705:+- 不把 `tenantCode`、`appKey`、form-data 混入签名，除非后续官方文档另行确认。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2713:+**B1：签名与配置切片**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2716:+- 实现 `generate_sign()`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2718:+- 单元测试覆盖官方签名样例、md5、非法 `encryptionType`、缺失必填环境变量。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2729:+- `backend/scripts/xg_user_api_probe.py` 作为人工诊断入口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2763:+签名样例: OK
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2764:+Live调用: skipped (missing tenantCode or XG_RUN_LIVE_API_TEST != 1)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2765:+请求摘要: POST /auth-user-info page=1 pageNum=1 encryptionType=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2778:+JSON 输出不能包含 `appSecret`、完整 `sign`、完整手机号、身份证、微信 openId。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2786:+`docs/api说明.txt` 的 header 参数是 `appKey`，没有 `appId`。`backend/.env.example` 已包含 `XG_USER_API_APP_ID`，可以保留用于记录平台凭证，但请求构造不要默认发送 `appId`。若平台部确认学校网关还要求 `appId`，再显式加入 header。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2825:+### Step 1A：签名与配置，先做
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2830:+- `backend/apps/users/integrations/xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2831:+- `backend/apps/users/tests/test_xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2835:+- 官方签名样例通过。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2836:+- 缺失 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 时有明确错误。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2837:+- `tenantCode` 缺失不影响签名样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2850:+- header 包含 `appKey/timestamp/randStr/sign/encryptionType`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2859:+- `backend/scripts/xg_user_api_probe.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2866:+- `XG_RUN_LIVE_API_TEST=1` 且配置齐全时才允许发请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2885:+  generate_sign
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2887:+  xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:2906:+1. 先做 `generate_sign()` 和官方样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3147:Step 0 安全修正已经完成，签名算法也已有官方样例，可以开始写代码；但 `tenantCode` 仍未确认，真实接口字段也未验证。因此下一步的最优路径不是等待，也不是直接接入业务 Provider，而是先交付一个可离线验证、可 mock 测试、可人工 live probe 的最小诊断层。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3152:2. **签名函数必须先用官方样例固化为单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3167:- `generate_sign()`、请求构造、响应解析、错误归一化、mock 测试可以立即做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3168:- `xg_user_api_probe.py` 可以立即做，但缺少 `XG_USER_API_TENANT_CODE` 时只能执行配置校验、签名样例验证、`--dry-run` 请求摘要，不能发起网络请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3169:- live probe 必须等 `tenantCode` 到位，并且需要操作者显式确认，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3173:### 问题2：签名算法是否需要单独验证模块？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3175:**建议：选项 A，但把签名函数设计成独立纯函数，并把官方样例作为 P0 单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3177:不需要额外创建一次性签名验证脚本。更好的边界是：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3180:backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3181:  - generate_sign(app_secret, timestamp, rand_str, encryption_type="sha1")
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3187:- `appSecret=6bd1b3fb015b4e72a85769e9d64405d1`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3189:- `randStr=Gc6LGToDKy2AMhXE`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3194:- 字典排序对象是三个**参数值**：`appSecret`、`timestamp`、`randStr`，不是参数名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3197:- 不把 `tenantCode`、`appKey`、form-data 混入签名，除非后续官方文档另行确认。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3205:**B1：签名与配置切片**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3208:- 实现 `generate_sign()`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3210:- 单元测试覆盖官方签名样例、md5、非法 `encryptionType`、缺失必填环境变量。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3221:- `backend/scripts/xg_user_api_probe.py` 作为人工诊断入口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3255:签名样例: OK
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3256:Live调用: skipped (missing tenantCode or XG_RUN_LIVE_API_TEST != 1)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3257:请求摘要: POST /auth-user-info page=1 pageNum=1 encryptionType=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3270:JSON 输出不能包含 `appSecret`、完整 `sign`、完整手机号、身份证、微信 openId。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3278:`docs/api说明.txt` 的 header 参数是 `appKey`，没有 `appId`。`backend/.env.example` 已包含 `XG_USER_API_APP_ID`，可以保留用于记录平台凭证，但请求构造不要默认发送 `appId`。若平台部确认学校网关还要求 `appId`，再显式加入 header。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3317:### Step 1A：签名与配置，先做
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3322:- `backend/apps/users/integrations/xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3323:- `backend/apps/users/tests/test_xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3327:- 官方签名样例通过。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3328:- 缺失 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 时有明确错误。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3329:- `tenantCode` 缺失不影响签名样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3342:- header 包含 `appKey/timestamp/randStr/sign/encryptionType`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3351:- `backend/scripts/xg_user_api_probe.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3358:- `XG_RUN_LIVE_API_TEST=1` 且配置齐全时才允许发请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3377:  generate_sign
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3379:  xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3414:+Step 0 安全修正已经完成，签名算法也已有官方样例，可以开始写代码；但 `tenantCode` 仍未确认，真实接口字段也未验证。因此下一步的最优路径不是等待，也不是直接接入业务 Provider，而是先交付一个可离线验证、可 mock 测试、可人工 live probe 的最小诊断层。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3419:+2. **签名函数必须先用官方样例固化为单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3434:+- `generate_sign()`、请求构造、响应解析、错误归一化、mock 测试可以立即做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3435:+- `xg_user_api_probe.py` 可以立即做，但缺少 `XG_USER_API_TENANT_CODE` 时只能执行配置校验、签名样例验证、`--dry-run` 请求摘要，不能发起网络请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3436:+- live probe 必须等 `tenantCode` 到位，并且需要操作者显式确认，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3440:+### 问题2：签名算法是否需要单独验证模块？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3442:+**建议：选项 A，但把签名函数设计成独立纯函数，并把官方样例作为 P0 单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3444:+不需要额外创建一次性签名验证脚本。更好的边界是：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3447:+backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3448:+  - generate_sign(app_secret, timestamp, rand_str, encryption_type="sha1")
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3454:+- `appSecret=6bd1b3fb015b4e72a85769e9d64405d1`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3456:+- `randStr=Gc6LGToDKy2AMhXE`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3461:+- 字典排序对象是三个**参数值**：`appSecret`、`timestamp`、`randStr`，不是参数名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3464:+- 不把 `tenantCode`、`appKey`、form-data 混入签名，除非后续官方文档另行确认。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3472:+**B1：签名与配置切片**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3475:+- 实现 `generate_sign()`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3477:+- 单元测试覆盖官方签名样例、md5、非法 `encryptionType`、缺失必填环境变量。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3488:+- `backend/scripts/xg_user_api_probe.py` 作为人工诊断入口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3522:+签名样例: OK
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3523:+Live调用: skipped (missing tenantCode or XG_RUN_LIVE_API_TEST != 1)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3524:+请求摘要: POST /auth-user-info page=1 pageNum=1 encryptionType=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3537:+JSON 输出不能包含 `appSecret`、完整 `sign`、完整手机号、身份证、微信 openId。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3545:+`docs/api说明.txt` 的 header 参数是 `appKey`，没有 `appId`。`backend/.env.example` 已包含 `XG_USER_API_APP_ID`，可以保留用于记录平台凭证，但请求构造不要默认发送 `appId`。若平台部确认学校网关还要求 `appId`，再显式加入 header。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3584:+### Step 1A：签名与配置，先做
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3589:+- `backend/apps/users/integrations/xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3590:+- `backend/apps/users/tests/test_xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3594:+- 官方签名样例通过。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3595:+- 缺失 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 时有明确错误。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3596:+- `tenantCode` 缺失不影响签名样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3609:+- header 包含 `appKey/timestamp/randStr/sign/encryptionType`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3618:+- `backend/scripts/xg_user_api_probe.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3625:+- `XG_RUN_LIVE_API_TEST=1` 且配置齐全时才允许发请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3644:+  generate_sign
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3646:+  xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3665:+1. 先做 `generate_sign()` 和官方样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3717:+Step 0 安全修正已经完成，签名算法也已有官方样例，可以开始写代码；但 `tenantCode` 仍未确认，真实接口字段也未验证。因此下一步的最优路径不是等待，也不是直接接入业务 Provider，而是先交付一个可离线验证、可 mock 测试、可人工 live probe 的最小诊断层。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3722:+2. **签名函数必须先用官方样例固化为单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3737:+- `generate_sign()`、请求构造、响应解析、错误归一化、mock 测试可以立即做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3738:+- `xg_user_api_probe.py` 可以立即做，但缺少 `XG_USER_API_TENANT_CODE` 时只能执行配置校验、签名样例验证、`--dry-run` 请求摘要，不能发起网络请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3739:+- live probe 必须等 `tenantCode` 到位，并且需要操作者显式确认，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3743:+### 问题2：签名算法是否需要单独验证模块？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3745:+**建议：选项 A，但把签名函数设计成独立纯函数，并把官方样例作为 P0 单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3747:+不需要额外创建一次性签名验证脚本。更好的边界是：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3750:+backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3751:+  - generate_sign(app_secret, timestamp, rand_str, encryption_type="sha1")
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3757:+- `appSecret=6bd1b3fb015b4e72a85769e9d64405d1`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3759:+- `randStr=Gc6LGToDKy2AMhXE`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3764:+- 字典排序对象是三个**参数值**：`appSecret`、`timestamp`、`randStr`，不是参数名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3767:+- 不把 `tenantCode`、`appKey`、form-data 混入签名，除非后续官方文档另行确认。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3775:+**B1：签名与配置切片**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3778:+- 实现 `generate_sign()`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3780:+- 单元测试覆盖官方签名样例、md5、非法 `encryptionType`、缺失必填环境变量。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3791:+- `backend/scripts/xg_user_api_probe.py` 作为人工诊断入口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3825:+签名样例: OK
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3826:+Live调用: skipped (missing tenantCode or XG_RUN_LIVE_API_TEST != 1)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3827:+请求摘要: POST /auth-user-info page=1 pageNum=1 encryptionType=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3840:+JSON 输出不能包含 `appSecret`、完整 `sign`、完整手机号、身份证、微信 openId。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3848:+`docs/api说明.txt` 的 header 参数是 `appKey`，没有 `appId`。`backend/.env.example` 已包含 `XG_USER_API_APP_ID`，可以保留用于记录平台凭证，但请求构造不要默认发送 `appId`。若平台部确认学校网关还要求 `appId`，再显式加入 header。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3887:+### Step 1A：签名与配置，先做
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3892:+- `backend/apps/users/integrations/xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3893:+- `backend/apps/users/tests/test_xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3897:+- 官方签名样例通过。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3898:+- 缺失 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 时有明确错误。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3899:+- `tenantCode` 缺失不影响签名样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3912:+- header 包含 `appKey/timestamp/randStr/sign/encryptionType`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3921:+- `backend/scripts/xg_user_api_probe.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3928:+- `XG_RUN_LIVE_API_TEST=1` 且配置齐全时才允许发请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3947:+  generate_sign
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3949:+  xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3968:+1. 先做 `generate_sign()` 和官方样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:3992:  \"{id:\\"'$id,type:'"\\\"review_response\\\",agent:\\\"codex\\\",timestamp:\\"'$timestamp,summary:'"\\\"Codex reviewed Claude post-Step 0 API test strategy and approved phased diagnostic-client implementation while keeping live calls gated on tenantCode.\\\",task_id:\\\"phase4c_next_steps\\\",artifacts:[\\\"docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md\\\"],status:\\\"waiting_for_claude_response\\\",details:{decision:\\\"approve_phased_diagnostic_client\\\",recommended_order:[\\\"signature_and_config_tests\\\",\\\"request_parse_mock_tests\\\",\\\"diagnostic_probe\\\",\\\"live_probe_after_tenant_code\\\"],live_gate:\\\"XG_RUN_LIVE_API_TEST=1 plus confirmed tenantCode\\\"}}\")
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4029:+Step 0 安全修正已经完成，签名算法也已有官方样例，可以开始写代码；但 `tenantCode` 仍未确认，真实接口字段也未验证。因此下一步的最优路径不是等待，也不是直接接入业务 Provider，而是先交付一个可离线验证、可 mock 测试、可人工 live probe 的最小诊断层。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4034:+2. **签名函数必须先用官方样例固化为单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4049:+- `generate_sign()`、请求构造、响应解析、错误归一化、mock 测试可以立即做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4050:+- `xg_user_api_probe.py` 可以立即做，但缺少 `XG_USER_API_TENANT_CODE` 时只能执行配置校验、签名样例验证、`--dry-run` 请求摘要，不能发起网络请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4051:+- live probe 必须等 `tenantCode` 到位，并且需要操作者显式确认，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4055:+### 问题2：签名算法是否需要单独验证模块？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4057:+**建议：选项 A，但把签名函数设计成独立纯函数，并把官方样例作为 P0 单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4059:+不需要额外创建一次性签名验证脚本。更好的边界是：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4062:+backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4063:+  - generate_sign(app_secret, timestamp, rand_str, encryption_type="sha1")
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4069:+- `appSecret=6bd1b3fb015b4e72a85769e9d64405d1`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4071:+- `randStr=Gc6LGToDKy2AMhXE`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4076:+- 字典排序对象是三个**参数值**：`appSecret`、`timestamp`、`randStr`，不是参数名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4079:+- 不把 `tenantCode`、`appKey`、form-data 混入签名，除非后续官方文档另行确认。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4087:+**B1：签名与配置切片**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4090:+- 实现 `generate_sign()`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4092:+- 单元测试覆盖官方签名样例、md5、非法 `encryptionType`、缺失必填环境变量。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4103:+- `backend/scripts/xg_user_api_probe.py` 作为人工诊断入口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4137:+签名样例: OK
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4138:+Live调用: skipped (missing tenantCode or XG_RUN_LIVE_API_TEST != 1)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4139:+请求摘要: POST /auth-user-info page=1 pageNum=1 encryptionType=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4152:+JSON 输出不能包含 `appSecret`、完整 `sign`、完整手机号、身份证、微信 openId。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4160:+`docs/api说明.txt` 的 header 参数是 `appKey`，没有 `appId`。`backend/.env.example` 已包含 `XG_USER_API_APP_ID`，可以保留用于记录平台凭证，但请求构造不要默认发送 `appId`。若平台部确认学校网关还要求 `appId`，再显式加入 header。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4199:+### Step 1A：签名与配置，先做
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4204:+- `backend/apps/users/integrations/xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4205:+- `backend/apps/users/tests/test_xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4209:+- 官方签名样例通过。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4210:+- 缺失 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 时有明确错误。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4211:+- `tenantCode` 缺失不影响签名样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4224:+- header 包含 `appKey/timestamp/randStr/sign/encryptionType`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4233:+- `backend/scripts/xg_user_api_probe.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4240:+- `XG_RUN_LIVE_API_TEST=1` 且配置齐全时才允许发请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4259:+  generate_sign
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4261:+  xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4280:+1. 先做 `generate_sign()` 和官方样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4301:{"id":99,"type":"review_response","agent":"codex","timestamp":"2026-06-02T03:08:57.327738096Z","summary":"Codex reviewed Claude post-Step 0 API test strategy and approved phased diagnostic-client implementation while keeping live calls gated on tenantCode.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md"],"status":"waiting_for_claude_response","details":{"decision":"approve_phased_diagnostic_client","recommended_order":["signature_and_config_tests","request_parse_mock_tests","diagnostic_probe","live_probe_after_tenant_code"],"live_gate":"XG_RUN_LIVE_API_TEST=1 plus confirmed tenantCode"}}
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4334:+Step 0 安全修正已经完成，签名算法也已有官方样例，可以开始写代码；但 `tenantCode` 仍未确认，真实接口字段也未验证。因此下一步的最优路径不是等待，也不是直接接入业务 Provider，而是先交付一个可离线验证、可 mock 测试、可人工 live probe 的最小诊断层。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4339:+2. **签名函数必须先用官方样例固化为单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4354:+- `generate_sign()`、请求构造、响应解析、错误归一化、mock 测试可以立即做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4355:+- `xg_user_api_probe.py` 可以立即做，但缺少 `XG_USER_API_TENANT_CODE` 时只能执行配置校验、签名样例验证、`--dry-run` 请求摘要，不能发起网络请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4356:+- live probe 必须等 `tenantCode` 到位，并且需要操作者显式确认，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4360:+### 问题2：签名算法是否需要单独验证模块？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4362:+**建议：选项 A，但把签名函数设计成独立纯函数，并把官方样例作为 P0 单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4364:+不需要额外创建一次性签名验证脚本。更好的边界是：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4367:+backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4368:+  - generate_sign(app_secret, timestamp, rand_str, encryption_type="sha1")
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4374:+- `appSecret=6bd1b3fb015b4e72a85769e9d64405d1`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4376:+- `randStr=Gc6LGToDKy2AMhXE`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4381:+- 字典排序对象是三个**参数值**：`appSecret`、`timestamp`、`randStr`，不是参数名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4384:+- 不把 `tenantCode`、`appKey`、form-data 混入签名，除非后续官方文档另行确认。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4392:+**B1：签名与配置切片**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4395:+- 实现 `generate_sign()`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4397:+- 单元测试覆盖官方签名样例、md5、非法 `encryptionType`、缺失必填环境变量。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4408:+- `backend/scripts/xg_user_api_probe.py` 作为人工诊断入口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4442:+签名样例: OK
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4443:+Live调用: skipped (missing tenantCode or XG_RUN_LIVE_API_TEST != 1)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4444:+请求摘要: POST /auth-user-info page=1 pageNum=1 encryptionType=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4457:+JSON 输出不能包含 `appSecret`、完整 `sign`、完整手机号、身份证、微信 openId。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4465:+`docs/api说明.txt` 的 header 参数是 `appKey`，没有 `appId`。`backend/.env.example` 已包含 `XG_USER_API_APP_ID`，可以保留用于记录平台凭证，但请求构造不要默认发送 `appId`。若平台部确认学校网关还要求 `appId`，再显式加入 header。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4504:+### Step 1A：签名与配置，先做
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4509:+- `backend/apps/users/integrations/xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4510:+- `backend/apps/users/tests/test_xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4514:+- 官方签名样例通过。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4515:+- 缺失 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 时有明确错误。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4516:+- `tenantCode` 缺失不影响签名样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4529:+- header 包含 `appKey/timestamp/randStr/sign/encryptionType`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4538:+- `backend/scripts/xg_user_api_probe.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4545:+- `XG_RUN_LIVE_API_TEST=1` 且配置齐全时才允许发请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4564:+  generate_sign
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4566:+  xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4585:+1. 先做 `generate_sign()` 和官方样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4628:+Step 0 安全修正已经完成，签名算法也已有官方样例，可以开始写代码；但 `tenantCode` 仍未确认，真实接口字段也未验证。因此下一步的最优路径不是等待，也不是直接接入业务 Provider，而是先交付一个可离线验证、可 mock 测试、可人工 live probe 的最小诊断层。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4633:+2. **签名函数必须先用官方样例固化为单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4648:+- `generate_sign()`、请求构造、响应解析、错误归一化、mock 测试可以立即做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4649:+- `xg_user_api_probe.py` 可以立即做，但缺少 `XG_USER_API_TENANT_CODE` 时只能执行配置校验、签名样例验证、`--dry-run` 请求摘要，不能发起网络请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4650:+- live probe 必须等 `tenantCode` 到位，并且需要操作者显式确认，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4654:+### 问题2：签名算法是否需要单独验证模块？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4656:+**建议：选项 A，但把签名函数设计成独立纯函数，并把官方样例作为 P0 单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4658:+不需要额外创建一次性签名验证脚本。更好的边界是：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4661:+backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4662:+  - generate_sign(app_secret, timestamp, rand_str, encryption_type="sha1")
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4668:+- `appSecret=6bd1b3fb015b4e72a85769e9d64405d1`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4670:+- `randStr=Gc6LGToDKy2AMhXE`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4675:+- 字典排序对象是三个**参数值**：`appSecret`、`timestamp`、`randStr`，不是参数名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4678:+- 不把 `tenantCode`、`appKey`、form-data 混入签名，除非后续官方文档另行确认。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4686:+**B1：签名与配置切片**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4689:+- 实现 `generate_sign()`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4691:+- 单元测试覆盖官方签名样例、md5、非法 `encryptionType`、缺失必填环境变量。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4702:+- `backend/scripts/xg_user_api_probe.py` 作为人工诊断入口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4736:+签名样例: OK
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4737:+Live调用: skipped (missing tenantCode or XG_RUN_LIVE_API_TEST != 1)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4738:+请求摘要: POST /auth-user-info page=1 pageNum=1 encryptionType=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4751:+JSON 输出不能包含 `appSecret`、完整 `sign`、完整手机号、身份证、微信 openId。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4759:+`docs/api说明.txt` 的 header 参数是 `appKey`，没有 `appId`。`backend/.env.example` 已包含 `XG_USER_API_APP_ID`，可以保留用于记录平台凭证，但请求构造不要默认发送 `appId`。若平台部确认学校网关还要求 `appId`，再显式加入 header。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4798:+### Step 1A：签名与配置，先做
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4803:+- `backend/apps/users/integrations/xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4804:+- `backend/apps/users/tests/test_xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4808:+- 官方签名样例通过。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4809:+- 缺失 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 时有明确错误。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4810:+- `tenantCode` 缺失不影响签名样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4823:+- header 包含 `appKey/timestamp/randStr/sign/encryptionType`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4832:+- `backend/scripts/xg_user_api_probe.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4839:+- `XG_RUN_LIVE_API_TEST=1` 且配置齐全时才允许发请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4858:+  generate_sign
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4860:+  xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4879:+1. 先做 `generate_sign()` 和官方样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4892:核心结论：批准继续 Step 1，但建议改为分步实现诊断客户端：先签名与配置测试，再请求构造/响应解析 mock 测试，最后诊断脚本；真实 live call 必须等本校 `tenantCode` 且显式开启 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4915:+Step 0 安全修正已经完成，签名算法也已有官方样例，可以开始写代码；但 `tenantCode` 仍未确认，真实接口字段也未验证。因此下一步的最优路径不是等待，也不是直接接入业务 Provider，而是先交付一个可离线验证、可 mock 测试、可人工 live probe 的最小诊断层。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4920:+2. **签名函数必须先用官方样例固化为单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4935:+- `generate_sign()`、请求构造、响应解析、错误归一化、mock 测试可以立即做。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4936:+- `xg_user_api_probe.py` 可以立即做，但缺少 `XG_USER_API_TENANT_CODE` 时只能执行配置校验、签名样例验证、`--dry-run` 请求摘要，不能发起网络请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4937:+- live probe 必须等 `tenantCode` 到位，并且需要操作者显式确认，例如 `XG_RUN_LIVE_API_TEST=1`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4941:+### 问题2：签名算法是否需要单独验证模块？
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4943:+**建议：选项 A，但把签名函数设计成独立纯函数，并把官方样例作为 P0 单元测试。**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4945:+不需要额外创建一次性签名验证脚本。更好的边界是：
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4948:+backend/apps/users/integrations/xg_user_client.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4949:+  - generate_sign(app_secret, timestamp, rand_str, encryption_type="sha1")
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4955:+- `appSecret=6bd1b3fb015b4e72a85769e9d64405d1`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4957:+- `randStr=Gc6LGToDKy2AMhXE`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4962:+- 字典排序对象是三个**参数值**：`appSecret`、`timestamp`、`randStr`，不是参数名。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4965:+- 不把 `tenantCode`、`appKey`、form-data 混入签名，除非后续官方文档另行确认。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4973:+**B1：签名与配置切片**
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4976:+- 实现 `generate_sign()`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4978:+- 单元测试覆盖官方签名样例、md5、非法 `encryptionType`、缺失必填环境变量。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:4989:+- `backend/scripts/xg_user_api_probe.py` 作为人工诊断入口。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5023:+签名样例: OK
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5024:+Live调用: skipped (missing tenantCode or XG_RUN_LIVE_API_TEST != 1)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5025:+请求摘要: POST /auth-user-info page=1 pageNum=1 encryptionType=sha1
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5038:+JSON 输出不能包含 `appSecret`、完整 `sign`、完整手机号、身份证、微信 openId。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5046:+`docs/api说明.txt` 的 header 参数是 `appKey`，没有 `appId`。`backend/.env.example` 已包含 `XG_USER_API_APP_ID`，可以保留用于记录平台凭证，但请求构造不要默认发送 `appId`。若平台部确认学校网关还要求 `appId`，再显式加入 header。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5085:+### Step 1A：签名与配置，先做
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5090:+- `backend/apps/users/integrations/xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5091:+- `backend/apps/users/tests/test_xg_user_client.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5095:+- 官方签名样例通过。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5096:+- 缺失 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 时有明确错误。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5097:+- `tenantCode` 缺失不影响签名样例测试。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5110:+- header 包含 `appKey/timestamp/randStr/sign/encryptionType`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5119:+- `backend/scripts/xg_user_api_probe.py`
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5126:+- `XG_RUN_LIVE_API_TEST=1` 且配置齐全时才允许发请求。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5145:+  generate_sign
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5147:+  xg_user_api_probe.py
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-76-claude-post-step0-nex-2026-06-02T03-09-25-789Z.md:5166:+1. 先做 `generate_sign()` 和官方样例测试。
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-08-c-2026-05-30T16-49-45-184Z.md:56:- `GET /api/approvals/`：学生 403；辅导员/学工部只看 `approver=user + decision=pending + 对应 step`，正确。
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-08-c-2026-05-30T16-49-45-184Z.md:933:- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-08-c-2026-05-30T16-49-45-184Z.md:972:2. ✓ 辅导员/学工部只看自己pending审批
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-08-c-2026-05-30T16-49-45-184Z.md:1552:- 学工部: 返回所有申请列表
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-08-c-2026-05-30T16-49-45-184Z.md:1587:- 学工部: 返回待自己审批的记录（step='dean', decision='pending'）
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-08-c-2026-05-30T16-49-45-184Z.md:2348:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-08-c-2026-05-30T16-49-45-184Z.md:2495:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-08-c-2026-05-30T16-49-45-184Z.md:2590:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-08-c-2026-05-30T16-49-45-184Z.md:3084:   183	- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-08-c-2026-05-30T16-49-45-184Z.md:3223:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-08-c-2026-05-30T16-49-45-184Z.md:3271:- `GET /api/approvals/`：学生 403；辅导员/学工部只看 `approver=user + decision=pending + 对应 step`，正确。
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-10-clau-2026-05-30T14-36-08-992Z.md:1832:**范围：** 登录 → 提交 → 辅导员审批 → 学工部审批 → 查询状态
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-10-clau-2026-05-30T14-36-08-992Z.md:1867:- [ ] 1个学工部
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-10-clau-2026-05-30T14-36-08-992Z.md:2009:### 5. 学工部能进行最终审批 ✓/✗
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-10-clau-2026-05-30T14-36-08-992Z.md:2013:**Step 1: 学工部登录**
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-10-clau-2026-05-30T14-36-08-992Z.md:2064:- [ ] 学工部能登录
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-10-clau-2026-05-30T14-36-08-992Z.md:2418:- 修复：学工部从User表查询（不硬编码D001）
.omc/collaboration/artifacts/20260531-0215-phase0-fact-check-results.md:197:- `pending_dean` - 待学工部审批
.omc/collaboration/artifacts/20260531-0215-phase0-fact-check-results.md:212:- `dean` - 学工部审批
.omc/collaboration/artifacts/20260530-1005-claude-response-to-codex-phase3-review.md:227:6. Role naming: freeze terminology (dean vs admin vs 学工部管理员)
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-1-2026-05-30T14-45-24-103Z.md:1476:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-1-2026-05-30T14-45-24-103Z.md:1811:     8	    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-1-2026-05-30T14-45-24-103Z.md:2058:    DEAN = 'dean', '学工部'
.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:11:但方案仍有 P0/P1 级缺口。最大问题不是“还差一点实现细节”，而是若按当前文档落地，可能引入新的不可用路径：wrapper 指向错误目录、旧 CLI 兼容解析与真实调用签名不匹配、`release_lock()` owner 字段不匹配、`claim_task()` 丢失原子生命周期校验。
.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:29:### P0-2：CLI 兼容解析与真实旧调用签名不匹配
.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:126:2. CLI 参数兼容：当前方案错误，未兼容真实 legacy 签名。
.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:127:3. `release_lock()`：方向正确，但 owner 字段和 API 签名不一致，且需要避免 finally 中 release 异常掩盖主异常。
.omc/collaboration/artifacts/20260530-1723-codex-review-claude-blocking-issues-response.md:154:4. wrapper 兼容旧 API 签名；核心 API 可以逐步走新签名。
.omc/collaboration/artifacts/test-coverage-analysis.md:98:   - 学工部可以看所有审批
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:901:| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:902:| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:903:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:925:**触发条件：** 辅导员或学工部审批通过
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:931:- 正文：`您的离校申请已通过{approver_role}审批。` （approver_role: 辅导员/学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:941:**触发条件：** 辅导员或学工部驳回申请
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:957:**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:959:**接收者：** 待审批的辅导员/学工部
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:1396:docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:68:1. 通知事件枚举：申请提交、辅导员通过、学工部通过、审批驳回、宿舍清退阻断。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:1529:    approver_role = "辅导员" if approval.step == "counselor" else "学工部"
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:1972:        self.assertIn('学工部', notification.message)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:2227:| 操作 | 学生 | 辅导员 | 学工部 | 说明 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:2481:    34	| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:2482:    35	| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:2483:    36	| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-33-59-995Z.md:2505:    58	**触发条件：** 辅导员或学工部审批通过
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-47-claude-post-step2-nex-2026-06-01T17-57-59-267Z.md:1251:docs/PROJECT-SUMMARY.md:1124:  - list_attachments：GET，RBAC（学生own/辅导员class+approval/学工部dean approval）
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:34:   有 10 学生、2 辅导员、1 学工部、班级映射、默认密码、4 个边界样本：[contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:358)。这项可以支持 Week 1。
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:42:   Day 3-4 的降级写“保留提交→辅导员审批→查询，砍学工部审批、列表API”是合理方向：[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:112)。  
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:477:36:- [ ] 生成seed数据（10学生 + 2辅导员 + 1学工部 + 边界样本 + 默认密码）
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:489:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:493:113:- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批、列表API
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:494:114:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:507:182:### 风险3：Week 1 Day 4学工部审批未完成
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:532:334:- `student_id`: 学号（可选，辅导员/学工部可用）
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:592:docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:116:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:687:docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:149:如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:801:docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:117:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:933:    93	    PENDING_DEAN = "pending_dean"        # 待学工部审批
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:972:   132	| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:974:   134	| pending_dean | 学工部通过 | dean | approved | 无 |
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:975:   135	| pending_dean | 学工部驳回 | dean | rejected | 无 |
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1047:   334	- `student_id`: 学号（可选，辅导员/学工部可用）
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1097:   384	**学工部（1人）：**
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1130:   154	| 学工部审批 | ✗ | ✗ | ✓（所有） |
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1261:   590	    # 4. 学工部审批
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1328:   182	### 风险3：Week 1 Day 4学工部审批未完成
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1416:    36	- [ ] 生成seed数据（10学生 + 2辅导员 + 1学工部 + 边界样本 + 默认密码）
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1455:    75	- [ ] Seed数据加载成功（10学生 + 2辅导员 + 1学工部）
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1472:    92	  - 创建学工部审批记录（通过时）
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1473:    93	- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1474:    94	  - 最小角色校验：只有学工部可审批
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1477:    97	  - 最小角色校验：学生只能查自己，辅导员/学工部可查所有
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1488:   108	- [ ] 学工部可审批（通过/驳回）
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1493:   113	- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批、列表API
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1494:   114	- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1500:   120	  - 测试1：学生登录 → 提交申请 → 辅导员审批通过 → 学工部审批通过 → 查询状态
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1540:docs/plans/week-0-1-execution-plan.md:36:- [ ] 生成seed数据（10学生 + 2辅导员 + 1学工部 + 边界样本 + 默认密码）
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1565:docs/plans/week-0-1-execution-plan.md:113:- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批、列表API
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1594:   有 10 学生、2 辅导员、1 学工部、班级映射、默认密码、4 个边界样本：[contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:358)。这项可以支持 Week 1。
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1602:   Day 3-4 的降级写“保留提交→辅导员审批→查询，砍学工部审批、列表API”是合理方向：[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:112)。  
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:25:2. CLI 兼容方案不匹配真实旧签名；当前真实格式是 `<type> <agent> <task_id> <summary> [artifacts_json]`。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6163:对照结果显示，当前仓库里确实只有旧 `.claude` 脚本在直接写 `events.jsonl/state.json`，但 Claude 文档提出的 wrapper 路径和当前调用签名之间有几处不一致，可能会变成新的阻塞点。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6804:+但方案仍有 P0/P1 级缺口。最大问题不是“还差一点实现细节”，而是若按当前文档落地，可能引入新的不可用路径：wrapper 指向错误目录、旧 CLI 兼容解析与真实调用签名不匹配、`release_lock()` owner 字段不匹配、`claim_task()` 丢失原子生命周期校验。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6822:+### P0-2：CLI 兼容解析与真实旧调用签名不匹配
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6919:+2. CLI 参数兼容：当前方案错误，未兼容真实 legacy 签名。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6920:+3. `release_lock()`：方向正确，但 owner 字段和 API 签名不一致，且需要避免 finally 中 release 异常掩盖主异常。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6947:+4. wrapper 兼容旧 API 签名；核心 API 可以逐步走新签名。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6970:+但方案仍有 P0/P1 级缺口。最大问题不是“还差一点实现细节”，而是若按当前文档落地，可能引入新的不可用路径：wrapper 指向错误目录、旧 CLI 兼容解析与真实调用签名不匹配、`release_lock()` owner 字段不匹配、`claim_task()` 丢失原子生命周期校验。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:6988:+### P0-2：CLI 兼容解析与真实旧调用签名不匹配
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7085:+2. CLI 参数兼容：当前方案错误，未兼容真实 legacy 签名。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7086:+3. `release_lock()`：方向正确，但 owner 字段和 API 签名不一致，且需要避免 finally 中 release 异常掩盖主异常。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7113:+4. wrapper 兼容旧 API 签名；核心 API 可以逐步走新签名。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7137:但方案仍有 P0/P1 级缺口。最大问题不是“还差一点实现细节”，而是若按当前文档落地，可能引入新的不可用路径：wrapper 指向错误目录、旧 CLI 兼容解析与真实调用签名不匹配、`release_lock()` owner 字段不匹配、`claim_task()` 丢失原子生命周期校验。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7155:### P0-2：CLI 兼容解析与真实旧调用签名不匹配
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7252:2. CLI 参数兼容：当前方案错误，未兼容真实 legacy 签名。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7253:3. `release_lock()`：方向正确，但 owner 字段和 API 签名不一致，且需要避免 finally 中 release 异常掩盖主异常。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7280:4. wrapper 兼容旧 API 签名；核心 API 可以逐步走新签名。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7303:+但方案仍有 P0/P1 级缺口。最大问题不是“还差一点实现细节”，而是若按当前文档落地，可能引入新的不可用路径：wrapper 指向错误目录、旧 CLI 兼容解析与真实调用签名不匹配、`release_lock()` owner 字段不匹配、`claim_task()` 丢失原子生命周期校验。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7321:+### P0-2：CLI 兼容解析与真实旧调用签名不匹配
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7418:+2. CLI 参数兼容：当前方案错误，未兼容真实 legacy 签名。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7419:+3. `release_lock()`：方向正确，但 owner 字段和 API 签名不一致，且需要避免 finally 中 release 异常掩盖主异常。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7446:+4. wrapper 兼容旧 API 签名；核心 API 可以逐步走新签名。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7461:2. CLI 兼容方案不匹配真实旧签名；当前真实格式是 `<type> <agent> <task_id> <summary> [artifacts_json]`。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7484:+但方案仍有 P0/P1 级缺口。最大问题不是“还差一点实现细节”，而是若按当前文档落地，可能引入新的不可用路径：wrapper 指向错误目录、旧 CLI 兼容解析与真实调用签名不匹配、`release_lock()` owner 字段不匹配、`claim_task()` 丢失原子生命周期校验。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7502:+### P0-2：CLI 兼容解析与真实旧调用签名不匹配
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7599:+2. CLI 参数兼容：当前方案错误，未兼容真实 legacy 签名。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7600:+3. `release_lock()`：方向正确，但 owner 字段和 API 签名不一致，且需要避免 finally 中 release 异常掩盖主异常。
.omc/artifacts/ask/codex-claude-omc-collaboration-artifacts-20260530-1718-claude-bloc-2026-05-30T17-25-14-997Z.md:7627:+4. wrapper 兼容旧 API 签名；核心 API 可以逐步走新签名。
docs/plans/week-0-1-execution-plan.md:36:- [ ] 生成seed数据（10学生 + 2辅导员 + 1学工部 + 边界样本 + 默认密码）
docs/plans/week-0-1-execution-plan.md:75:- [ ] Seed数据加载成功（10学生 + 2辅导员 + 1学工部）
docs/plans/week-0-1-execution-plan.md:92:  - 创建学工部审批记录（通过时）
docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
docs/plans/week-0-1-execution-plan.md:94:  - 最小角色校验：只有学工部可审批
docs/plans/week-0-1-execution-plan.md:97:  - 最小角色校验：学生只能查自己，辅导员/学工部可查所有
docs/plans/week-0-1-execution-plan.md:108:- [ ] 学工部可审批（通过/驳回）
docs/plans/week-0-1-execution-plan.md:113:- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批
docs/plans/week-0-1-execution-plan.md:114:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
docs/plans/week-0-1-execution-plan.md:120:  - 测试1：学生登录 → 提交申请 → 辅导员审批通过 → 学工部审批通过 → 查询状态
docs/plans/week-0-1-execution-plan.md:180:**降级方案：** 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
docs/plans/week-0-1-execution-plan.md:182:### 风险3：Week 1 Day 4学工部审批未完成
docs/用户设计说明书.md:5:**目标用户：** 学校管理人员、辅导员、学工部
docs/用户设计说明书.md:19:- **学工部端：** 审批所有学生的离校申请、查看全校审批统计、导出审批数据
docs/用户设计说明书.md:51:学生提交 → 辅导员审批 → 学工部审批 → 审批完成
docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
docs/用户设计说明书.md:69:- 辅导员审批通过 → 通知学生和学工部
docs/用户设计说明书.md:71:- 学工部审批通过 → 通知学生（审批完成）
docs/用户设计说明书.md:72:- 学工部驳回 → 通知学生
docs/用户设计说明书.md:117:- 学工部可以查看所有学生
docs/用户设计说明书.md:129:| **学工部** | 全校学生 | 审批申请、查看统计、导出数据 |
docs/用户设计说明书.md:151:**学工部权限：**
docs/用户设计说明书.md:233:A：学工部用户在"审批统计"页面点击"导出Excel"按钮。
docs/用户设计说明书.md:405:**学工部端：**
docs/用户设计说明书.md:406:- 学工部管理员手动创建（约5人）
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:36:    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:85:- 学工部: approver=user + step=dean + decision=pending
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:121:    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:170:- 学工部: approver=user + step=dean + decision=pending
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:223:权限逻辑是对的：学生 403；辅导员 `approver=user + step=counselor + decision=pending`；学工部 `approver=user + step=dean + decision=pending`。这严格符合 [共识](</home/caohui/projects/graduation-leave-system/docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:19>)。
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:271:    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:320:- 学工部: approver=user + step=dean + decision=pending
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:1070:    PENDING_DEAN = "pending_dean"        # 待学工部审批
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:1109:| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:1111:| pending_dean | 学工部通过 | dean | approved | 无 |
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:1112:| pending_dean | 学工部驳回 | dean | rejected | 无 |
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:1131:| 学工部审批 | ✗ | ✗ | ✓（所有） |
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:1221:- ✓ 学工部: approver=user + step=dean + decision=pending
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:1226:- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:1273:- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:1383:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:1477:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:1569:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:2074:     8	    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:2347:    22	- ✓ 学工部: approver=user + step=dean + decision=pending
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:2352:    27	- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:2399:    74	- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:2490:权限逻辑是对的：学生 403；辅导员 `approver=user + step=counselor + decision=pending`；学工部 `approver=user + step=dean + decision=pending`。这严格符合 [共识](</home/caohui/projects/graduation-leave-system/docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:19>)。
docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
docs/PROJECT-SUMMARY.md:214:  - UserDTO字段对教师/学工部不可选
docs/PROJECT-SUMMARY.md:233:  - P1-2：降级方案逻辑矛盾（风险2说"砍学工部审批"又说"Day 4补学工部审批"）
docs/PROJECT-SUMMARY.md:238:  - P1-2修复：修复风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1
docs/PROJECT-SUMMARY.md:259:  - 1学工部（D001，默认密码为工号）
docs/PROJECT-SUMMARY.md:281:  - 辅导员通过→pending_dean（创建学工部审批记录）
docs/PROJECT-SUMMARY.md:283:  - 学工部通过→approved
docs/PROJECT-SUMMARY.md:284:  - 学工部驳回→rejected
docs/PROJECT-SUMMARY.md:288:  - 学工部只能审批学工部步骤
docs/PROJECT-SUMMARY.md:300:  - 完整流程：登录→提交→辅导员审批→学工部审批→查询
docs/PROJECT-SUMMARY.md:311:  - 学工部驳回：pending_dean→rejected
docs/PROJECT-SUMMARY.md:341:- ✓ Seed数据需求：2学生+2辅导员+1学工部+2班级映射
docs/PROJECT-SUMMARY.md:352:- ✓ Seed数据导入：10学生+2辅导员+1学工部+2班级映射
docs/PROJECT-SUMMARY.md:358:  5. 学工部审批成功 - status→approved
docs/PROJECT-SUMMARY.md:460:  - Happy path: 学生→辅导员→学工部审批流程 ✓
docs/PROJECT-SUMMARY.md:501:   - 受众：学校管理人员、辅导员、学工部
docs/PROJECT-SUMMARY.md:512:- 学生、辅导员、学工部三种角色
docs/PROJECT-SUMMARY.md:524:- 两级审批（辅导员→学工部）
docs/PROJECT-SUMMARY.md:856:- 核心功能：登录、学生提交、列表、详情、辅导员/学工部审批
docs/PROJECT-SUMMARY.md:858:- 排除：独立辅导员/学工部页面集、草稿、完整附件UX、高级过滤、通知中心、审计时间线、React Native
docs/PROJECT-SUMMARY.md:1068:1. ✓ Detail endpoint isolation: 3个测试（学生/辅导员/学工部权限隔离）
docs/PROJECT-SUMMARY.md:1124:  - list_attachments：GET，RBAC（学生own/辅导员class+approval/学工部dean approval）
docs/PROJECT-SUMMARY.md:1437:  10. 学工部审批
docs/PROJECT-SUMMARY.md:1702:  - test_approval_approved_notification_dean（学工部审批通过通知）
docs/PROJECT-SUMMARY.md:1714:  - 学工部审批后验证学生收到第二条APPROVAL_APPROVED通知
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:1739:| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:1740:| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:1742:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:1764:**触发条件：** 辅导员或学工部审批通过
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:1770:- 正文：`您的离校申请已通过{approver_role}审批。` （approver_role: 辅导员/学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:1780:**触发条件：** 辅导员或学工部驳回申请
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:1812:**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:1814:**接收者：** 待审批的辅导员/学工部
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:2029:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:2107:docs/PROJECT-SUMMARY.md:1702:  - test_approval_approved_notification_dean（学工部审批通过通知）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:2405:docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:25:- ⚠ 部分达标：4/8（Seed数据、学工部审批、负向权限、宿舍清退Mock）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:2748:backend/apps/notifications/tests/test_auto_notifications.py:134:        self.assertIn('学工部', notification.message)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:3165:    description='获取当前用户的申请列表（学生/辅导员/学工部）',
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:3399:    approver_role = "辅导员" if approval.step == "counselor" else "学工部"
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:3447:    description='获取当前用户的待审批列表（辅导员或学工部）',
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:3478:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:3574:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:4025:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:4539:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:4816:   107	**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md:4818:   109	**接收者：** 待审批的辅导员/学工部
docs/acceptance/phase4c-demo-script.md:226:### 步骤10：学工部审批
docs/acceptance/phase4c-demo-script.md:229:# 提取学工部审批ID
docs/acceptance/phase4c-demo-script.md:236:# 学工部登录
docs/acceptance/phase4c-demo-script.md:244:# 学工部审批
docs/acceptance/phase4c-demo-script.md:401:# 步骤10: 学工部审批
docs/acceptance/phase4c-demo-script.md:402:echo "--- 步骤10: 学工部审批 ---"
docs/acceptance/phase4c-demo-script.md:414:echo "✓ 学工部审批通过"
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:1407:.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:1327:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:1444:./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:15:1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:1466:./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:2102:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:1054:1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:2116:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md:2763:    27	| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:2634:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:1176:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:2639:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:2369:    40	| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:3189:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:15:1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:3222:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1880:./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:3456:docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:40:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:3489:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:536:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:3509:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2003:+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:3516:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2326:+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:3523:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2653:1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:3529:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2804:+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:3537:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3141:+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:3548:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-phase-2-p0-types-client-tests-mocks-a-skeleton-miniprogram-w-2026-05-30T19-22-05-674Z.md:3913:│   ├── approvals/          # 待审批列表（辅导员/学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-03-claude-response-to-co-2026-06-01T07-08-03-331Z.md:1139:   - 权限测试 (学生/辅导员/学工部)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-03-claude-response-to-co-2026-06-01T07-08-03-331Z.md:1186:   - list权限 (RBAC: 学生own/辅导员class/学工部dean)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-03-claude-response-to-co-2026-06-01T07-08-03-331Z.md:1212:3. **RBAC复杂度:** 辅导员/学工部权限检查依赖approval scope，是否会导致N+1查询？
docs/contracts/contract-v0.1.md:95:    PENDING_DEAN = "pending_dean"        # 待学工部审批
docs/contracts/contract-v0.1.md:134:| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
docs/contracts/contract-v0.1.md:136:| pending_dean | 学工部通过 | dean | approved | 无 |
docs/contracts/contract-v0.1.md:137:| pending_dean | 学工部驳回 | dean | rejected | 无 |
docs/contracts/contract-v0.1.md:156:| 学工部审批 | ✗ | ✗ | ✓（所有） |
docs/contracts/contract-v0.1.md:364:**学工部（1人）：**
docs/contracts/contract-v0.1.md:640:    # 4. 学工部审批
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-47-claude-post-step2-nex-2026-06-01T17-43-18-137Z.md:1680:./docs/acceptance/phase4c-evidence-index.md:66:- H1: Happy path（学生→辅导员→学工部完整审批流程）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-47-claude-post-step2-nex-2026-06-01T17-43-18-137Z.md:1796:./docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:61:当前幂等检查只使用 `(entity_type, entity_id, type)`。这会把同一业务实体的同类通知限制为全局唯一，无法支持多个接收者。例如一个未来事件可能需要通知多个学工部账号，或者同一申请的不同待办人。即便 v0.1 当前多数事件只有单接收者，也不应把 schema 固化成全局唯一。
.omc/artifacts/ask/codex-step-2-step-1-baseline-tag-step-2-p0-step-2-enforcement-omc--2026-05-30T16-45-40-249Z.md:142:   - 保留 CLI 签名：
.omc/artifacts/ask/codex-step-2-step-1-baseline-tag-step-2-p0-step-2-enforcement-omc--2026-05-30T16-45-40-249Z.md:4012:   - 保留 CLI 签名：
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:151:- 核心闭环：提交 → 辅导员通过/驳回 → 学工部通过/驳回，有正向 smoke 和关键负向测试。
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:3027:docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:14:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:3054:backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:3118:backend/apps/approvals/tests/test_list_permissions.py:59:            approver_name='学工部1',
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:3180:backend/apps/applications/tests/test_list_permissions.py:74:            approver_name='学工部',
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:3199:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:3616:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:3835:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:3920:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4197:    PENDING_DEAN = "pending_dean"        # 待学工部审批
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4236:| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4238:| pending_dean | 学工部通过 | dean | approved | 无 |
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4239:| pending_dean | 学工部驳回 | dean | rejected | 无 |
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4258:| 学工部审批 | ✗ | ✗ | ✓（所有） |
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4660:/bin/bash -lc 'rtk rg -n "reject.*comment|comment.*required|invalid state|状态.*不匹配|student.*approve|dean-level|学工部" backend/apps/*/tests' in /home/caohui/projects/graduation-leave-system
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4667:backend/apps/approvals/tests/test_rejection_flow.py:84:        """测试学工部驳回申请"""
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4668:backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4669:backend/apps/approvals/tests/test_list_permissions.py:29:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4670:backend/apps/approvals/tests/test_list_permissions.py:59:            approver_name='学工部1',
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4671:backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4672:backend/apps/applications/tests/test_list_permissions.py:74:            approver_name='学工部',
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4673:backend/apps/applications/tests/test_application_flow.py:48:        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4674:backend/apps/applications/tests/test_application_flow.py:86:        # Step 5: 学工部登录
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4675:backend/apps/applications/tests/test_application_flow.py:93:        # Step 6: 学工部审批通过
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:5026:    95	    PENDING_DEAN = "pending_dean"        # 待学工部审批
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:5065:   134	| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:5067:   136	| pending_dean | 学工部通过 | dean | approved | 无 |
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:5068:   137	| pending_dean | 学工部驳回 | dean | rejected | 无 |
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:5284:- 核心闭环：提交 → 辅导员通过/驳回 → 学工部通过/驳回，有正向 smoke 和关键负向测试。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:1312:docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:1426:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1162:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:1457:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2052:docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:1481:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:2431:    93	- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:2035:.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:67:- **P1 权限方案回退了。** 提案让学生访问 `GET /api/approvals/` 自己申请的审批记录，并让学工部在 `GET /api/applications/` 看所有申请：[07-claude-phase1-proposal.md](</home/caohui/projects/graduation-leave-system/docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:30>)。这和 Day 3 共识冲突：审批列表学生应 403，辅导员/学工部只看自己 `pending` 审批；学工部申请列表也应是“自己待审批对应的申请”，不是全量：[04-final-consensus.md](</home/caohui/projects/graduation-leave-system/docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:37>)。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:2370:.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:4228:- **P1 权限方案回退了。** 提案让学生访问 `GET /api/approvals/` 自己申请的审批记录，并让学工部在 `GET /api/applications/` 看所有申请：[07-claude-phase1-proposal.md](</home/caohui/projects/graduation-leave-system/docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:30>)。这和 Day 3 共识冲突：审批列表学生应 403，辅导员/学工部只看自己 `pending` 审批；学工部申请列表也应是“自己待审批对应的申请”，不是全量：[04-final-consensus.md](</home/caohui/projects/graduation-leave-system/docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:37>)。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:2538:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:977:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:2540:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1195:    93	- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:2709:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:60:4. 补齐 10 个学生、2 个辅导员、1 个学工部、默认密码、当前审批人 fixture。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:2727:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1072:    88	- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:2735:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1597:docs/plans/week-0-1-execution-plan.md:88:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:2796:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:4077:4. 补齐 10 个学生、2 个辅导员、1 个学工部、默认密码、当前审批人 fixture。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:2902:.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:940:./docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:2913:.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:995:./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:60:- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:3307:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1676:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:60:- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:3309:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1678:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:62:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:3795:.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:1226:- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:3917:.omc/artifacts/ask/codex-phase-1-step-2-get-api-approvals-python-api-view-get-permiss-2026-05-30T17-03-29-001Z.md:2352:    27	- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:4954:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2011:+- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:4956:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2013:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:4974:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2211:+- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:4976:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2213:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:4995:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2474:+- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:4997:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2476:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5015:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2677:+- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5017:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2679:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5037:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2881:- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5039:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2883:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5057:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3083:+- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5059:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3085:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5079:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3302:+- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5081:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3304:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5097:.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:489:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5127:.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:1473:    93	- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5474:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5723:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5808:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:6014:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:6031:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:6141:        """测试学工部驳回申请"""
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:6220:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:6224:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:6254:            approver_name='学工部1',
docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:22:- ✓ 学工部: approver=user + step=dean + decision=pending
docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:27:- ✓ 学工部: 通过自己pending dean approvals反查
docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:74:- 权限: 学生403，辅导员/学工部只看自己pending
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:33:- 学工部: 返回所有申请列表
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:68:- 学工部: 返回待自己审批的记录（step='dean', decision='pending'）
docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:183:- 权限: 学生403，辅导员/学工部只看自己pending
docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:222:2. ✓ 辅导员/学工部只看自己pending审批
docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md:35:   - 学工部仅看 `approver=user + step=dean + decision=pending`。
.omc/artifacts/ask/codex-step-2-backend-apps-approvals-pagination-py-approvallimitoff-2026-05-30T17-22-09-113Z.md:24:- 验证辅导员/学工部只看到自己的pending审批
.omc/artifacts/ask/codex-step-2-backend-apps-approvals-pagination-py-approvallimitoff-2026-05-30T17-22-09-113Z.md:57:- 验证辅导员/学工部只看到自己的pending审批
.omc/artifacts/ask/codex-step-2-backend-apps-approvals-pagination-py-approvallimitoff-2026-05-30T17-22-09-113Z.md:87:3. 修完后只做最小回归：`offset=0`、`offset=5`、学生 403、辅导员/学工部只能看到自己 pending、响应 `{count, results}`。
.omc/artifacts/ask/codex-step-2-backend-apps-approvals-pagination-py-approvallimitoff-2026-05-30T17-22-09-113Z.md:126:- 验证辅导员/学工部只看到自己的pending审批
.omc/artifacts/ask/codex-step-2-backend-apps-approvals-pagination-py-approvallimitoff-2026-05-30T17-22-09-113Z.md:1059:docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-step-2-backend-apps-approvals-pagination-py-approvallimitoff-2026-05-30T17-22-09-113Z.md:1128:docs/design/2026-05-27-system-design.md:1473:    - 创建历史快照：applications_history（version=N, change_reason='学工部备案通过'）
.omc/artifacts/ask/codex-step-2-backend-apps-approvals-pagination-py-approvallimitoff-2026-05-30T17-22-09-113Z.md:1130:docs/design/2026-05-27-system-design.md:1482:    - 创建历史快照：applications_history（version=N, change_reason='学工部驳回'）
.omc/artifacts/ask/codex-step-2-backend-apps-approvals-pagination-py-approvallimitoff-2026-05-30T17-22-09-113Z.md:1213:docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:66:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-step-2-backend-apps-approvals-pagination-py-approvallimitoff-2026-05-30T17-22-09-113Z.md:1283:docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:150:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-step-2-backend-apps-approvals-pagination-py-approvallimitoff-2026-05-30T17-22-09-113Z.md:1286:docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:27:- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-step-2-backend-apps-approvals-pagination-py-approvallimitoff-2026-05-30T17-22-09-113Z.md:1514:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:63:- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
.omc/artifacts/ask/codex-step-2-backend-apps-approvals-pagination-py-approvallimitoff-2026-05-30T17-22-09-113Z.md:1678:    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-step-2-backend-apps-approvals-pagination-py-approvallimitoff-2026-05-30T17-22-09-113Z.md:1759:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-step-2-backend-apps-approvals-pagination-py-approvallimitoff-2026-05-30T17-22-09-113Z.md:1866:3. 修完后只做最小回归：`offset=0`、`offset=5`、学生 403、辅导员/学工部只能看到自己 pending、响应 `{count, results}`。
docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:102:- 学工部: `approver=user + step=dean + decision=pending`
docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:177:    # 学工部: 只看自己的pending dean审批
docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:234:   - 权限: 学生403，辅导员/学工部只看自己pending
docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:246:   - 确认辅导员/学工部隔离
docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:260:7. ✓ 辅导员/学工部只看自己pending审批
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1153:**范围：** 登录 → 提交 → 辅导员审批 → 学工部审批 → 查询状态
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1188:- [ ] 1个学工部
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1330:### 5. 学工部能进行最终审批 ✓/✗
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1334:**Step 1: 学工部登录**
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1385:- [ ] 学工部能登录
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1391:- 检查学工部权限配置
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1541:- [ ] check_status方法签名
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1599:# 4. 学工部审批
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1610:echo "✓ 学工部审批成功"
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1644:5. 学工部登录
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1645:6. 学工部审批
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1916:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:63:- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1927:docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:150:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1934:docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:66:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:1961:docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:2060:docs/design/2026-05-27-system-design.md:1473:    - 创建历史快照：applications_history（version=N, change_reason='学工部备案通过'）
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:2062:docs/design/2026-05-27-system-design.md:1482:    - 创建历史快照：applications_history（version=N, change_reason='学工部驳回'）
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:2820:测试学工部驳回申请
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:2830:测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:3004:     8	    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-task-20260530-06-phase-3-day-0-verification-context-claude-c-2026-05-30T14-26-14-372Z.md:3038:     8	    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md:1213:    34	| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md:1214:    35	| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md:1215:    36	| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md:1237:    58	**触发条件：** 辅导员或学工部审批通过
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md:1243:    64	- 正文：`您的离校申请已通过{approver_role}审批。` （approver_role: 辅导员/学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md:1253:    74	**触发条件：** 辅导员或学工部驳回申请
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md:1269:    90	**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md:1271:    92	**接收者：** 待审批的辅导员/学工部
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md:1485:    52	    approver_role = "辅导员" if approval.step == "counselor" else "学工部"
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md:2801:  1702	  - test_approval_approved_notification_dean（学工部审批通过通知）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-65-phase2b-option1-execu-2026-06-02T02-30-46-868Z.md:2813:  1714	  - 学工部审批后验证学生收到第二条APPROVAL_APPROVED通知
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-38-45-885Z.md:935:./docs/plans/week-0-1-execution-plan.md:113:- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-38-45-885Z.md:936:./docs/plans/week-0-1-execution-plan.md:114:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-38-45-885Z.md:944:./docs/plans/week-0-1-execution-plan.md:180:**降级方案：** 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-38-45-885Z.md:945:./docs/plans/week-0-1-execution-plan.md:182:### 风险3：Week 1 Day 4学工部审批未完成
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-38-45-885Z.md:956:./docs/用户设计说明书.md:51:学生提交 → 辅导员审批 → 学工部审批 → 审批完成
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-38-45-885Z.md:958:./docs/用户设计说明书.md:71:- 学工部审批通过 → 通知学生（审批完成）
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-38-45-885Z.md:1089:./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:14:计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-38-45-885Z.md:1406:./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:93:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-38-45-885Z.md:1428:./docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:71:如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-38-45-885Z.md:1501:./docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:51:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-38-45-885Z.md:1511:./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:104:> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-38-45-885Z.md:1569:./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:42:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-38-45-885Z.md:1740:   117	| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-student-application-api-createdefaultapiclient-reason-leave--2026-06-01T01-42-06-938Z.md:1853:- 核心功能：登录、学生提交、列表、详情、辅导员/学工部审批
.omc/artifacts/ask/codex-student-application-api-createdefaultapiclient-reason-leave--2026-06-01T01-42-06-938Z.md:1855:- 排除：独立辅导员/学工部页面集、草稿、完整附件UX、高级过滤、通知中心、审计时间线、React Native
.omc/artifacts/ask/codex-student-application-api-createdefaultapiclient-reason-leave--2026-06-01T01-42-06-938Z.md:2162:docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:33:- 学工部: 返回所有申请列表
.omc/artifacts/ask/codex-student-application-api-createdefaultapiclient-reason-leave--2026-06-01T01-42-06-938Z.md:2176:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:63:- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
.omc/artifacts/ask/codex-student-application-api-createdefaultapiclient-reason-leave--2026-06-01T01-42-06-938Z.md:2184:docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:150:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-student-application-api-createdefaultapiclient-reason-leave--2026-06-01T01-42-06-938Z.md:2188:docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:66:- 学工部列表：GET /api/applications/?role=dean
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:14:计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:26:| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:60:- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:62:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:63:- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:130:- 学工部：只看分配给自己的`pending_dean`待办。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:137:1. **查看权限漏洞被遗漏。** `get_application`只限制学生，未限制辅导员/学工部访问范围。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:161:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:34:4. 学工部管理员数据源
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:79:4. 学工部管理员数据源
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:107:- P1：学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:149:4. 学工部管理员数据源
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:186:- ❌ 管理员数据（辅导员、学工部管理员）
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:199:| 学工部管理员 | admin | ~5人 | 终审备案 | 人事系统 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:304:### 3.5 学工部管理员信息
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:309:- 创建学工部管理员账号
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:439:| 学工部管理员信息 | 人事系统 | 手动创建 | 数量少，可手动 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:486:4. **学工部管理员是否需要数据对接？**
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1045:| 学工部管理员信息 | P1 | 不建议做系统级数据对接 | `29-data-source-analysis.md` 第三章 3.5 和第六章均说明管理员约 5 人，可手动创建。这里是账号初始化问题，不是高频数据同步问题。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1059:| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 约 5 人，不建议接 HR API。需要在文档中明确由系统管理员维护，并保留角色授权、停用、重置密码流程。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1078:6. **组织架构与权限边界。** 学工部可看全校，辅导员只能看负责班级。除班级映射外，还需要院系、专业、年级等维度用于筛选、统计和异常排查。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1102:6. **手动创建学工部管理员账号。** 同时补充后台维护流程，包括新增、停用、密码重置、角色授权审计。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1117:/bin/bash -lc 'rtk rg -n "student|counselor|admin|辅导员|学工|班级|教务|人事|图书|财务|宿舍|清退|审批人" docs/design docs/用户设计说明书.md docs/PROJECT-SUMMARY.md' in /home/caohui/projects/graduation-leave-system
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1119:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1123:docs/PROJECT-SUMMARY.md:132:   - 受众：学校管理人员、辅导员、学工部
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1127:docs/PROJECT-SUMMARY.md:143:- 学生、辅导员、学工部三种角色
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1129:docs/PROJECT-SUMMARY.md:155:- 两级审批（辅导员→学工部）
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1132:docs/用户设计说明书.md:5:**目标用户：** 学校管理人员、辅导员、学工部
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1134:docs/用户设计说明书.md:19:- **学工部端：** 审批所有学生的离校申请、查看全校审批统计、导出审批数据
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1139:docs/用户设计说明书.md:51:学生提交 → 辅导员审批 → 学工部审批 → 审批完成
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1141:docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1143:docs/用户设计说明书.md:69:- 辅导员审批通过 → 通知学生和学工部
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1145:docs/用户设计说明书.md:71:- 学工部审批通过 → 通知学生（审批完成）
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1146:docs/用户设计说明书.md:72:- 学工部驳回 → 通知学生
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1152:docs/用户设计说明书.md:117:- 学工部可以查看所有学生
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1154:docs/用户设计说明书.md:129:| **学工部** | 全校学生 | 审批申请、查看统计、导出数据 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1159:docs/用户设计说明书.md:151:**学工部权限：**
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1162:docs/用户设计说明书.md:233:A：学工部用户在"审批统计"页面点击"导出Excel"按钮。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1167:docs/design/2026-05-27-system-design.md:40:3. **终端备案：** 学工部管理科负责人终审
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1170:docs/design/2026-05-27-system-design.md:187:   - 学生/辅导员/学工部用户管理
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1172:docs/design/2026-05-27-system-design.md:202:   - 学工部备案操作
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1180:docs/design/2026-05-27-system-design.md:300:- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1184:docs/design/2026-05-27-system-design.md:314:    admin_id BIGINT COMMENT '学工部管理员ID',
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1194:docs/design/2026-05-27-system-design.md:355:- `pending_admin` - 待学工部备案
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1197:docs/design/2026-05-27-system-design.md:387:- `approver_role`: counselor（辅导员）、admin（学工部）
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1198:docs/design/2026-05-27-system-design.md:389:- `time_limit`: 辅导员1个工作日(24小时)，学工部1个工作日(24小时)
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1208:docs/design/2026-05-27-system-design.md:599:  ├─N:1─→ users (学工部管理员)
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1211:docs/design/2026-05-27-system-design.md:627:2. 一个申请必须经过2级审批（辅导员→学工部）
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1231:docs/design/2026-05-27-system-design.md:1016:    "next_approver": "学工部",
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1245:docs/design/2026-05-27-system-design.md:1325:admin（学工部管理员）
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1248:docs/design/2026-05-27-system-design.md:1342:学工部审批         | ✗       | ✗         | ✓
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1255:docs/design/2026-05-27-system-design.md:1399:（待学工部备案）
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1258:docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1264:docs/design/2026-05-27-system-design.md:1427:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1274:docs/design/2026-05-27-system-design.md:1448:    - 通知学工部
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1278:docs/design/2026-05-27-system-design.md:1461:**节点3：学工部备案**
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1280:docs/design/2026-05-27-system-design.md:1463:- 权限要求：学工部管理员角色 + current_approver_id匹配
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1283:docs/design/2026-05-27-system-design.md:1473:    - 创建历史快照：applications_history（version=N, change_reason='学工部备案通过'）
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1286:docs/design/2026-05-27-system-design.md:1482:    - 创建历史快照：applications_history（version=N, change_reason='学工部驳回'）
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1335:docs/design/2026-05-27-system-design.md:2713:3. 学工部备案流程
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1409:（待学工部备案）
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1419:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1437:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1458:    - 通知学工部
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1535:- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1549:    admin_id BIGINT COMMENT '学工部管理员ID',
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1571:A：学工部用户在"审批统计"页面点击"导出Excel"按钮。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1638:+| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1647:-| 学工部管理员信息 | P1 | 不建议做系统级数据对接 | `29-data-source-analysis.md` 第三章 3.5 和第六章均说明管理员约 5 人，可手动创建。这里是账号初始化问题，不是高频数据同步问题。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1652:+| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1668:-| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 约 5 人，不建议接 HR API。需要在文档中明确由系统管理员维护，并保留角色授权、停用、重置密码流程。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1678:+| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1703:-6. **组织架构与权限边界。** 学工部可看全校，辅导员只能看负责班级。除班级映射外，还需要院系、专业、年级等维度用于筛选、统计和异常排查。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1722:+### 4. 学工部管理员数据源是否需要对接？
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1750:+7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1781:-6. **手动创建学工部管理员账号。** 同时补充后台维护流程，包括新增、停用、密码重置、角色授权审计。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1782:+6. **手动创建学工部管理员。** 同时补充管理员账号维护和终审人分配规则。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1814:+- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1860:+| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1869:-| 学工部管理员信息 | P1 | 不建议做系统级数据对接 | `29-data-source-analysis.md` 第三章 3.5 和第六章均说明管理员约 5 人，可手动创建。这里是账号初始化问题，不是高频数据同步问题。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1874:+| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1890:-| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 约 5 人，不建议接 HR API。需要在文档中明确由系统管理员维护，并保留角色授权、停用、重置密码流程。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1900:+| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1925:-6. **组织架构与权限边界。** 学工部可看全校，辅导员只能看负责班级。除班级映射外，还需要院系、专业、年级等维度用于筛选、统计和异常排查。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1944:+### 4. 学工部管理员数据源是否需要对接？
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1972:+7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2003:-6. **手动创建学工部管理员账号。** 同时补充后台维护流程，包括新增、停用、密码重置、角色授权审计。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2004:+6. **手动创建学工部管理员。** 同时补充管理员账号维护和终审人分配规则。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2036:+- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2076:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2084:| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2099:| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2133:### 4. 学工部管理员数据源是否需要对接？
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2161:7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2185:6. **手动创建学工部管理员。** 同时补充管理员账号维护和终审人分配规则。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2212:- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2258:+| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2267:-| 学工部管理员信息 | P1 | 不建议做系统级数据对接 | `29-data-source-analysis.md` 第三章 3.5 和第六章均说明管理员约 5 人，可手动创建。这里是账号初始化问题，不是高频数据同步问题。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2272:+| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2288:-| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 约 5 人，不建议接 HR API。需要在文档中明确由系统管理员维护，并保留角色授权、停用、重置密码流程。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2298:+| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2323:-6. **组织架构与权限边界。** 学工部可看全校，辅导员只能看负责班级。除班级映射外，还需要院系、专业、年级等维度用于筛选、统计和异常排查。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2342:+### 4. 学工部管理员数据源是否需要对接？
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2370:+7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2401:-6. **手动创建学工部管理员账号。** 同时补充后台维护流程，包括新增、停用、密码重置、角色授权审计。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2402:+6. **手动创建学工部管理员。** 同时补充管理员账号维护和终审人分配规则。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2434:+- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2447:- P1：学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2491:+| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2500:-| 学工部管理员信息 | P1 | 不建议做系统级数据对接 | `29-data-source-analysis.md` 第三章 3.5 和第六章均说明管理员约 5 人，可手动创建。这里是账号初始化问题，不是高频数据同步问题。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2505:+| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2521:-| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 约 5 人，不建议接 HR API。需要在文档中明确由系统管理员维护，并保留角色授权、停用、重置密码流程。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2531:+| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2556:-6. **组织架构与权限边界。** 学工部可看全校，辅导员只能看负责班级。除班级映射外，还需要院系、专业、年级等维度用于筛选、统计和异常排查。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2575:+### 4. 学工部管理员数据源是否需要对接？
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2603:+7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2634:-6. **手动创建学工部管理员账号。** 同时补充后台维护流程，包括新增、停用、密码重置、角色授权审计。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2635:+6. **手动创建学工部管理员。** 同时补充管理员账号维护和终审人分配规则。
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:2667:+- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-08-claude-phase2-impleme-2026-06-01T08-18-49-202Z.md:2180:docs/PROJECT-SUMMARY.md:1124:  - list_attachments：GET，RBAC（学生own/辅导员class+approval/学工部dean approval）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-08-claude-phase2-impleme-2026-06-01T08-18-49-202Z.md:2867:docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:14:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:826:c/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1528:**问题：** "辅导员能看到自己班级申请""学工部能看到全部待审批申请"没有列表接口  
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:838:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1648:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:1093:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:2942:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:26:4. **遗漏问题：** 列表接口真的可以推迟吗？没有列表接口，辅导员/学工部怎么知道有哪些申请需要审批？Day 2能达到可重复验收吗？
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:1096:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:2945:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:60:4. **遗漏问题：** 列表接口真的可以推迟吗？没有列表接口，辅导员/学工部怎么知道有哪些申请需要审批？Day 2能达到可重复验收吗？
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:1099:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:2948:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:126:4. **遗漏问题：** 列表接口真的可以推迟吗？没有列表接口，辅导员/学工部怎么知道有哪些申请需要审批？Day 2能达到可重复验收吗？
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:1736:    68	            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:1895:     8	    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:1929:     8	    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:2125:     8	    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:2204:    39	        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:2242:    77	        # Step 5: 学工部登录
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:2249:    84	        # Step 6: 学工部审批通过
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:2743:    75	        """测试学工部驳回申请"""
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:2879:**问题：** 风险2降级方案说"砍学工部审批，Day 4补学工部审批"，逻辑矛盾
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:2885:降级方案：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:2890:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:2893:**验证：** 降级方案现在明确：Day 3触发后砍学工部审批，Day 4验证辅导员闭环，学工部推Week 2 Day 1
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:2975:**问题：** 风险2说"砍学工部审批"又说"Day 4补学工部审批"
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:2979:降级方案：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:2984:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3019:- 样例数据（10学生 + 2辅导员 + 1学工部 + 边界样本）
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3212:计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3224:| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3258:- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3260:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3261:- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3328:- 学工部：只看分配给自己的`pending_dean`待办。
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3335:1. **查看权限漏洞被遗漏。** `get_application`只限制学生，未限制辅导员/学工部访问范围。
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3359:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3466:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:4300:docs/week3-day0-acceptance-checklist.md:393:- [ ] check_status方法签名
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:4816:    71	- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:5143:测试学工部驳回申请
.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:5153:测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:25:- ⚠ 部分达标：4/8（Seed数据、学工部审批、负向权限、宿舍清退Mock）
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:64:**7. 缺少列表接口**：辅导员/学工部看不到待审批列表
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:150:- 学工部列表：GET /api/applications/?role=dean
backend/apps/approvals/migrations/0001_initial.py:20:                ('step', models.CharField(choices=[('counselor', '辅导员'), ('dean', '学工部')], max_length=20)),
docs/acceptance/phase4c-evidence-index.md:66:- H1: Happy path（学生→辅导员→学工部完整审批流程）
docs/acceptance/phase4c-acceptance-checklist.md:56:| RBAC权限（学生/辅导员/学工部） | ✅ 通过 | `test_list.py` 6个测试 |
docs/acceptance/phase4c-acceptance-checklist.md:146:| 学工部登录 | ✅ 通过 | 步骤9 |
docs/acceptance/phase4c-acceptance-checklist.md:147:| 学工部审批 | ✅ 通过 | 步骤10 |
backend/apps/approvals/tests/test_rejection_flow.py:86:        """测试学工部驳回申请"""
backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
backend/apps/approvals/tests/test_list_permissions.py:29:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
backend/apps/approvals/tests/test_list_permissions.py:59:            approver_name='学工部1',
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:1104:docs/week3-day0-acceptance-checklist.md:393:- [ ] check_status方法签名
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:1190:docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:1220:docs/PROJECT-SUMMARY.md:283:  - 学工部通过→approved
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:1221:docs/PROJECT-SUMMARY.md:284:  - 学工部驳回→rejected
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:1226:docs/PROJECT-SUMMARY.md:311:  - 学工部驳回：pending_dean→rejected
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:1229:docs/PROJECT-SUMMARY.md:358:  5. 学工部审批成功 - status→approved
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:1297:docs/superpowers/plans/2026-05-27-implementation-plan.md:347:- ✓ 学工部审批通过后状态变更为approved
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:1318:docs/contracts/contract-v0.1.md:136:| pending_dean | 学工部通过 | dean | approved | 无 |
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:1319:docs/contracts/contract-v0.1.md:137:| pending_dean | 学工部驳回 | dean | rejected | 无 |
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:1458:docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:22:- ✓ 学工部: approver=user + step=dean + decision=pending
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:1691:.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:1099:docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:182:admin_approver   # 学工部审批员（只能审批）
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:1894:.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:2215:   136	| pending_dean | 学工部通过 | dean | approved | 无 |
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:1895:.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:2216:   137	| pending_dean | 学工部驳回 | dean | rejected | 无 |
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:2109:docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md:35:   - 学工部仅看 `approver=user + step=dean + decision=pending`。
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:2156:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:977:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:2160:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-51-p1-fixes-confirm-2026-05-30T08-18-41-431Z.md:1195:    93	- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:2312:docs/design/2026-05-27-system-design.md:387:- `approver_role`: counselor（辅导员）、admin（学工部）
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:2348:docs/design/2026-05-27-system-design.md:1016:    "next_approver": "学工部",
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:2368:docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:2381:docs/design/2026-05-27-system-design.md:1463:- 权限要求：学工部管理员角色 + current_approver_id匹配
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:2451:docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:102:- 学工部: `approver=user + step=dean + decision=pending`
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:2731:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:26:| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:2735:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:60:- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3461:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1072:    88	- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3463:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1525:docs/superpowers/plans/2026-05-27-implementation-plan.md:347:- ✓ 学工部审批通过后状态变更为approved
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3465:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1597:docs/plans/week-0-1-execution-plan.md:88:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3475:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1843:docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3491:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2395:docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:182:admin_approver   # 学工部审批员（只能审批）
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3744:.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1197:docs/design/2026-05-27-system-design.md:387:- `approver_role`: counselor（辅导员）、admin（学工部）
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3751:.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1231:docs/design/2026-05-27-system-design.md:1016:    "next_approver": "学工部",
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3755:.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1258:docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3764:.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1280:docs/design/2026-05-27-system-design.md:1463:- 权限要求：学工部管理员角色 + current_approver_id匹配
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3793:.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1419:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3832:.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:92:| P1 | 小程序核心操作：学生提交申请、辅导员 approve/reject、学工部 approve/reject、错误态展示 | 1.5-2.5天 | Week 4主线 |
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3854:.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1550:  - 学工部通过→approved
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3855:.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1551:  - 学工部驳回→rejected
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3860:.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1578:  - 学工部驳回：pending_dean→rejected
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3863:.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1625:  5. 学工部审批成功 - status→approved
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:3871:.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1753:- ✓ 学工部: approver=user + step=dean + decision=pending
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4007:.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:3068:| P1 | 小程序核心操作：学生提交申请、辅导员 approve/reject、学工部 approve/reject、错误态展示 | 1.5-2.5天 | Week 4主线 |
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4011:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:907:docs/superpowers/plans/2026-05-27-implementation-plan.md:347:- ✓ 学工部审批通过后状态变更为approved
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4018:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1624:docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:182:admin_approver   # 学工部审批员（只能审批）
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4032:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:2228:docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4083:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:4443:   347	- ✓ 学工部审批通过后状态变更为approved
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4085:.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:14:3. ✓ 学工部看到1条pending审批（approver=D001, decision=pending）
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4088:.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:37:3. ✓ 学工部看到1条pending审批（approver=D001, decision=pending）
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4092:.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:86:3. ✓ 学工部看到1条pending审批（approver=D001, decision=pending）
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4172:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1465:docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4223:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1676:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:60:- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4879:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4992:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:5077:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:6211:34:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:6296:119:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:7012:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:7056:            approver_name='学工部',
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:7206:**学工部（1人）：**
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:7491:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:7495:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:7525:            approver_name='学工部1',
backend/apps/approvals/tests/test_permissions.py:123:        """学工部不能处理辅导员审批步骤"""
backend/apps/approvals/tests/test_permissions.py:135:        """辅导员不能处理学工部审批步骤"""
backend/apps/approvals/tests/test_permissions.py:148:        """同角色但非指定学工部审批人不能处理审批"""
backend/apps/approvals/tests/test_state_machine.py:127:        """测试学工部审批步骤与申请状态不匹配时返回409"""
backend/apps/approvals/views.py:23:    description='获取当前用户的待审批列表（辅导员或学工部）',
backend/apps/approvals/views.py:54:    # 学工部: 只看自己的dean审批
backend/apps/approvals/views.py:150:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
backend/apps/approvals/models.py:8:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:1222:3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:1249:./docs/api/notification-contract-v0.1.md:35:| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:1463:./docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:156:- 辅导员/学工部驳回后创建 `APPROVAL_REJECTED` 给学生；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:1485:./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:215:3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:1908:        self.assertIn('学工部', notification.message)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:2481:    approver_role = "辅导员" if approval.step == "counselor" else "学工部"
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:3016:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:3098:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:3261:backend/apps/applications/tests/test_list_permissions.py:74:            approver_name='学工部',
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:3311:backend/apps/approvals/tests/test_list_permissions.py:59:            approver_name='学工部1',
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:5410:+- 学生审批通过通知：`type=approval_approved`、`entity_type=approval`、`message`包含`辅导员`或`学工部`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:5598:+- 学生审批通过通知：`type=approval_approved`、`entity_type=approval`、`message`包含`辅导员`或`学工部`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:5862:+- 学生审批通过通知：`type=approval_approved`、`entity_type=approval`、`message`包含`辅导员`或`学工部`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:6068:- 学生审批通过通知：`type=approval_approved`、`entity_type=approval`、`message`包含`辅导员`或`学工部`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:6265:+- 学生审批通过通知：`type=approval_approved`、`entity_type=approval`、`message`包含`辅导员`或`学工部`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-43-claude-post-phase2a-s-2026-06-01T17-11-31-800Z.md:6467:+- 学生审批通过通知：`type=approval_approved`、`entity_type=approval`、`message`包含`辅导员`或`学工部`。
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:25:   [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:16) 把 `is_graduating`、`graduation_year` 定义为所有用户必填，但辅导员/学工部样例没有这些字段 [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:338)。应改成学生专属可选字段，或拆成 `StudentDTO / StaffDTO`。
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:34:   计划要求 `10学生 + 2辅导员 + 1学工部 + 边界样本` [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:31)，但契约只给了 3 个正常学生和若干零散边界样本 [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:329)。还缺默认密码/密码策略，薄认证无法稳定跑 seed 登录。
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:40:   “Day 3 申请提交未完成 → 只做查询 API” [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:108) 会破坏纵向切片价值。更合理的降级是保留“提交→辅导员审批→查询”最短闭环，砍列表、学工部审批、复杂错误、完整 seed 等外围内容。  
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:60:4. 补齐 10 个学生、2 个辅导员、1 个学工部、默认密码、当前审批人 fixture。
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:520:    93	    PENDING_DEAN = "pending_dean"        # 待学工部审批
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:730:   303	- `student_id`: 学号（可选，辅导员/学工部可用）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:771:   344	**学工部：**
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:970:   543	    # 4. 学工部审批
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1015:    31	- [ ] 生成seed数据（10学生 + 2辅导员 + 1学工部 + 边界样本）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1054:    70	- [ ] Seed数据加载成功（10学生 + 2辅导员 + 1学工部）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1071:    87	  - 创建学工部审批记录（通过时）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1072:    88	- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1073:    89	  - 最小角色校验：只有学工部可审批
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1076:    92	  - 最小角色校验：学生只能查自己，辅导员/学工部可查所有
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1087:   103	- [ ] 学工部可审批（通过/驳回）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1093:   109	- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证辅导员审批
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1099:   115	  - 测试1：学生登录 → 提交申请 → 辅导员审批通过 → 学工部审批通过 → 查询状态
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1161:   177	### 风险3：Week 1 Day 4学工部审批未完成
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1321:docs/用户设计说明书.md:19:- **学工部端：** 审批所有学生的离校申请、查看全校审批统计、导出审批数据
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1327:docs/用户设计说明书.md:51:学生提交 → 辅导员审批 → 学工部审批 → 审批完成
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1330:docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1335:docs/用户设计说明书.md:69:- 辅导员审批通过 → 通知学生和学工部
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1336:docs/用户设计说明书.md:71:- 学工部审批通过 → 通知学生（审批完成）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1344:docs/用户设计说明书.md:129:| **学工部** | 全校学生 | 审批申请、查看统计、导出数据 |
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1367:docs/用户设计说明书.md:233:A：学工部用户在"审批统计"页面点击"导出Excel"按钮。
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1385:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1428:docs/PROJECT-SUMMARY.md:252:- 两级审批（辅导员→学工部）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1453:docs/contracts/contract-v0.1.md:93:    PENDING_DEAN = "pending_dean"        # 待学工部审批
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1475:docs/contracts/contract-v0.1.md:543:    # 4. 学工部审批
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1490:docs/superpowers/plans/2026-05-27-implementation-plan.md:14:- 辅导员和学工部两级审批
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1518:docs/superpowers/plans/2026-05-27-implementation-plan.md:330:   - 学工部审批逻辑
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1523:docs/superpowers/plans/2026-05-27-implementation-plan.md:342:   - 学工部可以审批所有
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1525:docs/superpowers/plans/2026-05-27-implementation-plan.md:347:- ✓ 学工部审批通过后状态变更为approved
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1596:docs/plans/week-0-1-execution-plan.md:87:  - 创建学工部审批记录（通过时）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1597:docs/plans/week-0-1-execution-plan.md:88:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1598:docs/plans/week-0-1-execution-plan.md:89:  - 最小角色校验：只有学工部可审批
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1600:docs/plans/week-0-1-execution-plan.md:103:- [ ] 学工部可审批（通过/驳回）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1603:docs/plans/week-0-1-execution-plan.md:109:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证辅导员审批
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1604:docs/plans/week-0-1-execution-plan.md:115:  - 测试1：学生登录 → 提交申请 → 辅导员审批通过 → 学工部审批通过 → 查询状态
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1615:docs/plans/week-0-1-execution-plan.md:177:### 风险3：Week 1 Day 4学工部审批未完成
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1687:docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:84:| 班级-辅导员对应关系 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1808:docs/design/2026-05-27-system-design.md:627:2. 一个申请必须经过2级审批（辅导员→学工部）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1839:docs/design/2026-05-27-system-design.md:1342:学工部审批         | ✗       | ✗         | ✓
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1843:docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1846:docs/design/2026-05-27-system-design.md:1427:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1963:docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:104:4. 审批流程具备状态机意识：草稿、待辅导员、待学工部、通过、驳回等状态明确。
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1984:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1991:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:50:| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2122:docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:40:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2290:docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:58:- 学工部审批API
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2307:docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:116:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2328:docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:210:- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2356:docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:82:先做"学生登录/伪登录 → 提交申请 → 辅导员审批 → 学工部审批 → 状态可查"的端到端最小流程。
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2371:docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:151:- 最小申请审批闭环（提交→辅导员审批→学工部审批→状态查询）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2394:docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:172:2. **学工部权限过大**：admin既能审批又能管理系统配置
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2395:docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:182:admin_approver   # 学工部审批员（只能审批）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2396:docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:183:admin_manager    # 学工部管理员（审批+配置管理）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2428:docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:96:- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2430:docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:99:- 学工部审批API
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2431:docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:102:- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2445:docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:149:如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2461:docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:219:最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2581:docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:58:- 学工部审批API
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2597:docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:117:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2607:docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:215:- [ ] 学工部审批API
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2609:docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:228:- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2696:docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:131:- 学工部审批：辅导员通过后24小时内
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2698:docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:137:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2869:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:124:| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2878:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:204:2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2884:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:239:> 明确毕业离校系统所需的数据源，提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人反馈。
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2887:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:249:| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2940:    40	| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:2941:    41	| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:3179:    55	- **最小角色校验**（学生/辅导员/学工部边界）
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:3182:    58	- 学工部审批API
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:3240:   116	| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:3334:   210	- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:3811:   237	### 2.5 学工部管理员信息
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:3823:   249	| 部门 | department | 文本 | 是 | 所属部门 | 学工部 |
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:4042:   [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:16) 把 `is_graduating`、`graduation_year` 定义为所有用户必填，但辅导员/学工部样例没有这些字段 [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:338)。应改成学生专属可选字段，或拆成 `StudentDTO / StaffDTO`。
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:4051:   计划要求 `10学生 + 2辅导员 + 1学工部 + 边界样本` [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:31)，但契约只给了 3 个正常学生和若干零散边界样本 [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:329)。还缺默认密码/密码策略，薄认证无法稳定跑 seed 登录。
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:4057:   “Day 3 申请提交未完成 → 只做查询 API” [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:108) 会破坏纵向切片价值。更合理的降级是保留“提交→辅导员审批→查询”最短闭环，砍列表、学工部审批、复杂错误、完整 seed 等外围内容。  
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:4077:4. 补齐 10 个学生、2 个辅导员、1 个学工部、默认密码、当前审批人 fixture。
docs/api说明.txt:17:randStr	是	string	随机字符串
docs/api说明.txt:18:sign	是	string	认证签名，请参见签名校验部分
docs/api说明.txt:19:encryptionType	否	string	加密类型 只有 sha1和md5 不传默认 sha1 方式加密
docs/api说明.txt:27:number	否	string	学工号
.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:14:3. ✓ 学工部看到1条pending审批（approver=D001, decision=pending）
.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:19:- 角色权限过滤正确（学生403，辅导员/学工部只看自己的）
.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:37:3. ✓ 学工部看到1条pending审批（approver=D001, decision=pending）
.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:42:- 角色权限过滤正确（学生403，辅导员/学工部只看自己的）
.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:63:- 学工部只看到流转到自己名下的 pending approval
.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:86:3. ✓ 学工部看到1条pending审批（approver=D001, decision=pending）
.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:91:- 角色权限过滤正确（学生403，辅导员/学工部只看自己的）
.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:109:- 学工部只看到流转到自己名下的 pending approval
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md:1289:7. 学工部审批（API调用示例）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md:1489:- 学工部审批；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md:1640:- H1: Happy path（学生→辅导员→学工部完整审批流程）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md:1854:| RBAC权限（学生/辅导员/学工部） | ✅ 通过 | `test_list.py` 6个测试 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md:1944:| 学工部登录 | ✅ 通过 | 步骤9 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md:1945:| 学工部审批 | ✅ 通过 | 步骤10 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md:2262:+1. 通知事件枚举：申请提交、辅导员通过、学工部通过、审批驳回、宿舍清退阻断。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md:2430:+1. 通知事件枚举：申请提交、辅导员通过、学工部通过、审批驳回、宿舍清退阻断。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md:2602:1. 通知事件枚举：申请提交、辅导员通过、学工部通过、审批驳回、宿舍清退阻断。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md:2770:+1. 通知事件枚举：申请提交、辅导员通过、学工部通过、审批驳回、宿舍清退阻断。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md:3017:+1. 通知事件枚举：申请提交、辅导员通过、学工部通过、审批驳回、宿舍清退阻断。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md:3211:+1. 通知事件枚举：申请提交、辅导员通过、学工部通过、审批驳回、宿舍清退阻断。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md:3454:+1. 通知事件枚举：申请提交、辅导员通过、学工部通过、审批驳回、宿舍清退阻断。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md:3655:+1. 通知事件枚举：申请提交、辅导员通过、学工部通过、审批驳回、宿舍清退阻断。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-25-claude-post-evidence--2026-06-01T14-46-53-399Z.md:3831:+1. 通知事件枚举：申请提交、辅导员通过、学工部通过、审批驳回、宿舍清退阻断。
docs/week3-day0-seed-data-requirements.md:13:- **学工部：** 1个
docs/week3-day0-seed-data-requirements.md:60:### 3. 学工部账号（Dean）
docs/week3-day0-seed-data-requirements.md:63:**用途：** 测试学工部审批
docs/week3-day0-seed-data-requirements.md:73:- 学工部能审批所有通过辅导员审批的申请
docs/week3-day0-seed-data-requirements.md:74:- 学工部不能直接审批pending_counselor状态的申请
docs/week3-day0-seed-data-requirements.md:144:- [ ] 1个学工部账号创建成功
docs/week3-day0-seed-data-requirements.md:152:- [ ] 学工部可以登录（D001/D001）
docs/week3-day0-acceptance-checklist.md:5:**范围：** 登录 → 提交 → 辅导员审批 → 学工部审批 → 查询状态
docs/week3-day0-acceptance-checklist.md:40:- [ ] 1个学工部
docs/week3-day0-acceptance-checklist.md:182:### 5. 学工部能进行最终审批 ✓/✗
docs/week3-day0-acceptance-checklist.md:186:**Step 1: 学工部登录**
docs/week3-day0-acceptance-checklist.md:237:- [ ] 学工部能登录
docs/week3-day0-acceptance-checklist.md:243:- 检查学工部权限配置
docs/week3-day0-acceptance-checklist.md:393:- [ ] check_status方法签名
docs/week3-day0-acceptance-checklist.md:451:# 4. 学工部审批
docs/week3-day0-acceptance-checklist.md:462:echo "✓ 学工部审批成功"
docs/week3-day0-acceptance-checklist.md:496:5. 学工部登录
docs/week3-day0-acceptance-checklist.md:497:6. 学工部审批
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:341:**Claude签名：** 待Codex审查后达成共识
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:1300:docs/api/notification-contract-v0.1.md:34:| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:1301:docs/api/notification-contract-v0.1.md:35:| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:1303:docs/api/notification-contract-v0.1.md:37:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:1570:backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:1945:    34	| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:1946:    35	| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:1948:    37	| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:1970:    59	**触发条件：** 辅导员或学工部审批通过
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:1976:    65	- 正文：`您的离校申请已通过{approver_role}审批。` （approver_role: 辅导员/学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:1986:    75	**触发条件：** 辅导员或学工部驳回申请
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:2018:   107	**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:2020:   109	**接收者：** 待审批的辅导员/学工部
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:2090:    35	    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:2170:   115	            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:2325:     9	    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:2367:     8	    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:2401:     8	    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3375:+契约允许辅导员和学工部审批通过都通知学生。现有唯一键使用 `entity_type=approval`、`entity_id=approval_id` 时，两个审批步骤会产生两条不同通知，这是合理的。实现文档应明确这一点，避免误以为“申请最终通过”才通知。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3413:+4. 步骤语义：辅导员通过与学工部通过分别产生不同 `approval_id` 的通过通知。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3447:+- 辅导员/学工部通过后创建 `APPROVAL_APPROVED` 给学生；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3448:+- 辅导员/学工部驳回后创建 `APPROVAL_REJECTED` 给学生；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3467:+3. 学工部通过后，学生收到一条 `APPROVAL_APPROVED` 通知，关联 dean approval。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3577:+契约允许辅导员和学工部审批通过都通知学生。现有唯一键使用 `entity_type=approval`、`entity_id=approval_id` 时，两个审批步骤会产生两条不同通知，这是合理的。实现文档应明确这一点，避免误以为“申请最终通过”才通知。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3615:+4. 步骤语义：辅导员通过与学工部通过分别产生不同 `approval_id` 的通过通知。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3649:+- 辅导员/学工部通过后创建 `APPROVAL_APPROVED` 给学生；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3650:+- 辅导员/学工部驳回后创建 `APPROVAL_REJECTED` 给学生；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3669:+3. 学工部通过后，学生收到一条 `APPROVAL_APPROVED` 通知，关联 dean approval。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3783:契约允许辅导员和学工部审批通过都通知学生。现有唯一键使用 `entity_type=approval`、`entity_id=approval_id` 时，两个审批步骤会产生两条不同通知，这是合理的。实现文档应明确这一点，避免误以为“申请最终通过”才通知。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3821:4. 步骤语义：辅导员通过与学工部通过分别产生不同 `approval_id` 的通过通知。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3855:- 辅导员/学工部通过后创建 `APPROVAL_APPROVED` 给学生；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3856:- 辅导员/学工部驳回后创建 `APPROVAL_REJECTED` 给学生；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3875:3. 学工部通过后，学生收到一条 `APPROVAL_APPROVED` 通知，关联 dean approval。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:3985:+契约允许辅导员和学工部审批通过都通知学生。现有唯一键使用 `entity_type=approval`、`entity_id=approval_id` 时，两个审批步骤会产生两条不同通知，这是合理的。实现文档应明确这一点，避免误以为“申请最终通过”才通知。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:4023:+4. 步骤语义：辅导员通过与学工部通过分别产生不同 `approval_id` 的通过通知。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:4057:+- 辅导员/学工部通过后创建 `APPROVAL_APPROVED` 给学生；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:4058:+- 辅导员/学工部驳回后创建 `APPROVAL_REJECTED` 给学生；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:4077:+3. 学工部通过后，学生收到一条 `APPROVAL_APPROVED` 通知，关联 dean approval。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:4204:+契约允许辅导员和学工部审批通过都通知学生。现有唯一键使用 `entity_type=approval`、`entity_id=approval_id` 时，两个审批步骤会产生两条不同通知，这是合理的。实现文档应明确这一点，避免误以为“申请最终通过”才通知。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:4242:+4. 步骤语义：辅导员通过与学工部通过分别产生不同 `approval_id` 的通过通知。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:4276:+- 辅导员/学工部通过后创建 `APPROVAL_APPROVED` 给学生；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:4277:+- 辅导员/学工部驳回后创建 `APPROVAL_REJECTED` 给学生；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-37-claude-post-phase1-ne-2026-06-01T16-19-58-609Z.md:4296:+3. 学工部通过后，学生收到一条 `APPROVAL_APPROVED` 通知，关联 dean approval。
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:66:- 学工部列表：GET /api/applications/?role=dean
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:110:- 学工部审批是否也需要权限校验？（当前硬编码D001）
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:149:- 学工部如何知道有哪些申请需要审批？
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:888:docs/week3-day0-seed-data-requirements.md:152:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:947:backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:991:docs/PROJECT-SUMMARY.md:259:  - 1学工部（D001，默认密码为工号）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1095:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:62:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1103:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:161:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1187:docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:110:- 学工部审批是否也需要权限校验？（当前硬编码D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1207:docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:182:3. 学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1222:docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:118:- 学工部D001硬编码应该修复（从User表查询唯一dean）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1231:docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:329:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1241:docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:71:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1339:docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:116:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1402:backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1859:docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:117:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1918:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:987:  - 1学工部（D001，默认密码为工号）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1940:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1627:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1968:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2257:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1972:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2367:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1984:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2786:backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:1988:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2809:backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:2007:.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:1659:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:2012:.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:1902:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:2014:.omc/artifacts/ask/codex-docs-discussions-week3-direction-2026-05-30-01-claude-propos-2026-05-30T09-05-06-225Z.md:2295:   116	| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:2232:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-47-contract-fixes-r-2026-05-30T08-09-47-792Z.md:1421:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:2759:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:31:   - 1学工部（D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:2763:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:38:   - 学工部D001审批 → status=approved
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:2766:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:88:   - 1学工部（D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:2770:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:95:   - 学工部D001审批 → status=approved
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:2773:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:136:5. 学工部最终审批：主路径达标，但“能看到所有待审批申请”没有接口支撑；且 dean 审批人硬编码为 `D001`：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:48)。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:2780:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:226:   - 1学工部（D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:2784:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:233:   - 学工部D001审批 → status=approved
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:2862:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3117:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:2942:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:6453:5. 学工部最终审批：主路径达标，但“能看到所有待审批申请”没有接口支撑；且 dean 审批人硬编码为 `D001`：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:48)。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3430:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:20:   - 审批权限：只校验approver_id够吗？是否需要校验class_id？学工部D001硬编码怎么办？
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3432:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:54:   - 审批权限：只校验approver_id够吗？是否需要校验class_id？学工部D001硬编码怎么办？
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3434:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:120:   - 审批权限：只校验approver_id够吗？是否需要校验class_id？学工部D001硬编码怎么办？
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3440:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:1002:- 学工部审批是否也需要权限校验？（当前硬编码D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3487:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2013:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3495:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2112:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3498:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2213:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3506:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2312:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3509:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2476:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3517:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2575:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3520:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2679:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3528:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2778:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3531:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2883:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3539:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2982:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3542:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3085:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3550:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3184:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3553:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3304:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3561:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3403:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3659:.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:592:docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:116:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3671:.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md:801:docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:117:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3685:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4418:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:613:3. 学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:3696:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4456:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1678:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:62:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4009:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4853:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1632:./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:110:- 学工部审批是否也需要权限校验？（当前硬编码D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4014:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4869:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2247:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4018:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4877:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2355:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4046:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4921:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4711:backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4048:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4923:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4735:backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4088:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4971:.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4085:.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:14:3. ✓ 学工部看到1条pending审批（approver=D001, decision=pending）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4090:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4973:.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4088:.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:37:3. ✓ 学工部看到1条pending审批（approver=D001, decision=pending）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4092:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4975:.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4092:.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:86:3. ✓ 学工部看到1条pending审批（approver=D001, decision=pending）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4124:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5030:.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:7012:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4135:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5044:.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:7491:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4153:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5115:.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:2808:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4253:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5257:.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:2132:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:161:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4594:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5748:.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:1080:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4601:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5758:.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:2061:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4620:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5784:.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:3003:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4629:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5821:.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2000:  - 1学工部（D001，默认密码为工号）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4647:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5847:.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:3053:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4684:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5914:.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:4809:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4705:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5990:.omc/artifacts/ask/codex-docs-discussions-week3-day1-review-2026-05-30-17-claude-next-2026-05-30T15-17-01-336Z.md:1195:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:161:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4936:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6360:.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:27589:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:4940:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6366:.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:27703:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5119:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6624:.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:838:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1648:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5157:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6690:.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3260:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5163:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6699:.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3359:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5164:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6702:.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3466:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5187:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6739:.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:4816:    71	- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5194:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6748:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:853:- 学工部D001硬编码应该修复（从User表查询唯一dean）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5200:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6758:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1070:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5204:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6762:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1254:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:161:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5214:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6774:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1648:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5218:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6786:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:3233:   118	- 学工部D001硬编码应该修复（从User表查询唯一dean）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5221:.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6792:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:3351:   329	- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5238:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:853:- 学工部D001硬编码应该修复（从User表查询唯一dean）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5247:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1070:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5254:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1254:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:161:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5268:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1648:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5284:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:3233:   118	- 学工部D001硬编码应该修复（从User表查询唯一dean）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:5288:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:3351:   329	- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:6216:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:6229:docs/PROJECT-SUMMARY.md:341:- ✓ Seed数据需求：2学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:6230:docs/PROJECT-SUMMARY.md:352:- ✓ Seed数据导入：10学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:6234:docs/PROJECT-SUMMARY.md:460:  - Happy path: 学生→辅导员→学工部审批流程 ✓
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:6236:docs/PROJECT-SUMMARY.md:512:- 学生、辅导员、学工部三种角色
.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:6243:docs/PROJECT-SUMMARY.md:856:- 核心功能：登录、学生提交、列表、详情、辅导员/学工部审批
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:182:3. 学工部从User表查询（不硬编码D001）
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:196:- 学工部ID从User表动态查询
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:309:2. 根据角色自动过滤（学生看自己，辅导员看待审批，学工部看待审批）
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:613:3. 学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:627:- 学工部ID从User表动态查询
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1215:2. 根据角色自动过滤（学生看自己，辅导员看待审批，学工部看待审批）
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1465:docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1534:docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:150:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1544:docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:66:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1676:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:60:- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1678:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:62:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1679:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:63:- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1900:docs/design/2026-05-27-system-design.md:1473:    - 创建历史快照：applications_history（version=N, change_reason='学工部备案通过'）
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1902:docs/design/2026-05-27-system-design.md:1482:    - 创建历史快照：applications_history（version=N, change_reason='学工部驳回'）
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:2161:docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:117:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:2187:docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:116:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:2574:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:2928:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:3041:        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:3079:        # Step 5: 学工部登录
.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:3086:        # Step 6: 学工部审批通过
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:94:- ✗ 学工部从User表动态读取
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:118:- 学工部D001硬编码应该修复（从User表查询唯一dean）
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:329:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:910:./docs/week3-day0-acceptance-checklist.md:243:- 检查学工部权限配置
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:939:./docs/用户设计说明书.md:151:**学工部权限：**
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:947:./docs/PROJECT-SUMMARY.md:238:  - P1-2修复：修复风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1001:./docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1003:./docs/plans/week-0-1-execution-plan.md:113:- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1005:./docs/plans/week-0-1-execution-plan.md:180:**降级方案：** 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1035:./docs/design/2026-05-27-system-design.md:389:- `time_limit`: 辅导员1个工作日(24小时)，学工部1个工作日(24小时)
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1083:./docs/design/2026-05-27-system-design.md:1463:- 权限要求：学工部管理员角色 + current_approver_id匹配
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1085:./docs/design/2026-05-27-system-design.md:1473:    - 创建历史快照：applications_history（version=N, change_reason='学工部备案通过'）
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1087:./docs/design/2026-05-27-system-design.md:1482:    - 创建历史快照：applications_history（version=N, change_reason='学工部驳回'）
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1208:./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:27:- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1218:./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:74:- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1319:./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:183:- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1489:./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:234:   - 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1568:./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:26:| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1575:./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:63:- 同步修复`GET /api/applications/{id}/`查看权限。当前只限制学生，任何辅导员/学工部都可查看任意申请，这是同类权限漏洞。
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1577:./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:137:1. **查看权限漏洞被遗漏。** `get_application`只限制学生，未限制辅导员/学工部访问范围。
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1628:./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:66:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1632:./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:110:- 学工部审批是否也需要权限校验？（当前硬编码D001）
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1880:./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2038:./docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:51:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2039:./docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:54:**验证点：** 降级逻辑现在清晰：Day 3触发→砍学工部→Day 4验证辅导员闭环→学工部推Week 2 Day 1
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2078:./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:104:> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2080:./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:143:**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2085:./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:186:2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2092:./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:172:2. **学工部权限过大**：admin既能审批又能管理系统配置
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2130:./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:42:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2143:./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:149:如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2148:./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:219:最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2168:./docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:71:如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2190:./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:25:- ⚠ 部分达标：4/8（Seed数据、学工部审批、负向权限、宿舍清退Mock）
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2200:./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:150:- 学工部列表：GET /api/applications/?role=dean
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2211:./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:93:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2212:./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:96:**验证：** 降级方案现在明确：Day 3触发后砍学工部审批，Day 4验证辅导员闭环，学工部推Week 2 Day 1
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2247:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2251:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2281:            approver_name='学工部1',
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2355:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2399:            approver_name='学工部',
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2479:    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2560:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2829:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2871:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2964:- ✓ 学工部: approver=user + step=dean + decision=pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2969:- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3016:- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3099:   - 学工部仅看 `approver=user + step=dean + decision=pending`。
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3135:- ✓ Seed数据需求：2学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3146:- ✓ Seed数据导入：10学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3152:  5. 学工部审批成功 - status→approved
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3493:docs/contracts/contract-v0.1.md:95:    PENDING_DEAN = "pending_dean"        # 待学工部审批
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3497:docs/contracts/contract-v0.1.md:134:| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3499:docs/contracts/contract-v0.1.md:136:| pending_dean | 学工部通过 | dean | approved | 无 |
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3500:docs/contracts/contract-v0.1.md:137:| pending_dean | 学工部驳回 | dean | rejected | 无 |
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3527:docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:22:- ✓ 学工部: approver=user + step=dean + decision=pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3528:docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:27:- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3534:docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:74:- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3546:docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:33:- 学工部: 返回所有申请列表
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3549:docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:68:- 学工部: 返回待自己审批的记录（step='dean', decision='pending'）
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3568:docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:183:- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3576:docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:222:2. ✓ 辅导员/学工部只看自己pending审批
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3609:docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md:35:   - 学工部仅看 `approver=user + step=dean + decision=pending`。
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3619:docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:102:- 学工部: `approver=user + step=dean + decision=pending`
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3625:docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:177:    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3627:docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:234:   - 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3630:docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:260:7. ✓ 辅导员/学工部只看自己pending审批
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3641:backend/apps/applications/models.py:8:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3651:backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:3660:backend/apps/approvals/views.py:35:    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4339:    35	    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4420:   116	            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4623:    27	- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4670:    74	- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4694:还有一个比分页更关键的遗漏：`GET /api/applications/{id}/` 现在只限制学生和辅导员，学工部角色没有对象级限制；这和 Phase 1 共识里的“Dean detail endpoint 同步修正”相冲突。这个应该作为前端对接前的 P1 处理。
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4706:/bin/bash -lc "rtk rg -n \"Dean|dean|学工部|detail|applications/.*/|get_application|D002|403\" backend/apps/*/tests docs/discussions/week3-day3-planning-2026-05-30 -g '"'!**/__pycache__/**'"'" in /home/caohui/projects/graduation-leave-system
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4711:backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4715:backend/apps/applications/tests/test_list_permissions.py:74:            approver_name='学工部',
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4719:backend/apps/applications/tests/test_application_flow.py:48:        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4720:backend/apps/applications/tests/test_application_flow.py:86:        # Step 5: 学工部登录
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4722:backend/apps/applications/tests/test_application_flow.py:93:        # Step 6: 学工部审批通过
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4729:backend/apps/approvals/tests/test_rejection_flow.py:84:        """测试学工部驳回申请"""
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4735:backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4738:backend/apps/approvals/tests/test_list_permissions.py:29:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4742:backend/apps/approvals/tests/test_list_permissions.py:59:            approver_name='学工部1',
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4789:docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:22:- ✓ 学工部: approver=user + step=dean + decision=pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4790:docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:27:- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4794:docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:74:- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4801:docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md:35:   - 学工部仅看 `approver=user + step=dean + decision=pending`。
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4802:docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:33:- 学工部: 返回所有申请列表
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4803:docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:68:- 学工部: 返回待自己审批的记录（step='dean', decision='pending'）
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4808:docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:102:- 学工部: `approver=user + step=dean + decision=pending`
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4810:docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:177:    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4812:docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:234:   - 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4814:docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:246:   - 确认辅导员/学工部隔离
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4816:docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:260:7. ✓ 辅导员/学工部只看自己pending审批
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4834:docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:183:- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4839:docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:222:2. ✓ 辅导员/学工部只看自己pending审批
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:71:- 修复：学工部从User表查询（不硬编码D001）
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:33:| 5. 学工部最终审批 | ⚠ 部分达标 | 主路径达标，但缺列表接口，dean硬编码 |
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:72:**问题：** "辅导员能看到自己班级申请""学工部能看到全部待审批申请"没有列表接口  
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:128:2. API认证信息（appKey、appSecret、签名算法）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:240:        sign = self._generate_sign()
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:253:    def _generate_sign(self):
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:254:        # 实现签名算法（待API文档提供）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:361:- 方法签名是否合理？
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:572:- 从教务系统或学工系统导出当届毕业生数据
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:750:3. **终端备案：** 学工部管理科负责人终审
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:897:   - 学生/辅导员/学工部用户管理
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:912:   - 学工部备案操作
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:975:- 方法签名是否合理？
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:1176:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:1177:| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:1373:### 2.5 学工部管理员信息
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:1385:| 部门 | department | 文本 | 是 | 所属部门 | 学工部 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:1635:**问题2：** 如不包含，能否从教务/人事/学工系统归集后提供？
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:2181:| 学工部管理员 | 当前在职 | 5人 | 手动创建 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:2218:2. 如不包含，能否从教务/人事/学工系统归集后提供？
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:2369:    40	| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:2370:    41	| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:2580:    27	2. API认证信息（appKey、appSecret、签名算法）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:2692:   139	        sign = self._generate_sign()
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:2705:   152	    def _generate_sign(self):
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:2706:   153	        # 实现签名算法（待API文档提供）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:2996:   478	| 学工部管理员 | 当前在职 | 5人 | 手动创建 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:3033:   515	2. 如不包含，能否从教务/人事/学工系统归集后提供？
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:3388:   106	- 从教务系统或学工系统导出当届毕业生数据
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md:3677:   260	- 方法签名是否合理？
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:829:- ✗ 学工部从User表动态读取
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:853:- 学工部D001硬编码应该修复（从User表查询唯一dean）
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1070:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1225:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:14:计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1254:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:161:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1269:docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:64:**7. 缺少列表接口**：辅导员/学工部看不到待审批列表
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1441:docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:33:| 5. 学工部最终审批 | ⚠ 部分达标 | 主路径达标，但缺列表接口，dean硬编码 |
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1445:docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:72:**问题：** "辅导员能看到自己班级申请""学工部能看到全部待审批申请"没有列表接口  
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1489:| 5. 学工部最终审批 | ⚠ 部分达标 | 主路径达标，但缺列表接口，dean硬编码 |
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1528:**问题：** "辅导员能看到自己班级申请""学工部能看到全部待审批申请"没有列表接口  
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1617:- 学工部：只看分配给自己的`pending_dean`待办。
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1624:1. **查看权限漏洞被遗漏。** `get_application`只限制学生，未限制辅导员/学工部访问范围。
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1648:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1905:.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:4033:+   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1915:.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:4266:+   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1925:.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:4552:   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1935:.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:4785:+   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1945:.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:5083:+   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1955:.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:5331:+   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1965:.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:5575:+   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:2640:.omc/collaboration/artifacts/20260530-0959-codex-phase3-independent-review.md:190:   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:2942:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:26:4. **遗漏问题：** 列表接口真的可以推迟吗？没有列表接口，辅导员/学工部怎么知道有哪些申请需要审批？Day 2能达到可重复验收吗？
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:2945:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:60:4. **遗漏问题：** 列表接口真的可以推迟吗？没有列表接口，辅导员/学工部怎么知道有哪些申请需要审批？Day 2能达到可重复验收吗？
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:2948:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:126:4. **遗漏问题：** 列表接口真的可以推迟吗？没有列表接口，辅导员/学工部怎么知道有哪些申请需要审批？Day 2能达到可重复验收吗？
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:3209:    94	- ✗ 学工部从User表动态读取
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:3233:   118	- 学工部D001硬编码应该修复（从User表查询唯一dean）
.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:3351:   329	- 修复：学工部从User表查询（不硬编码D001）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:55:- **最小角色校验**（学生/辅导员/学工部边界）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:58:- 学工部审批API
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:116:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:210:- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:30:2. 是否先做 MVP？是，必须。先做“学生登录/伪登录 -> 提交申请 -> 辅导员审批 -> 学工部审批 -> 状态可查”的端到端最小流程。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:753:docs/用户设计说明书.md:19:- **学工部端：** 审批所有学生的离校申请、查看全校审批统计、导出审批数据
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:759:docs/用户设计说明书.md:51:学生提交 → 辅导员审批 → 学工部审批 → 审批完成
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:762:docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:766:docs/用户设计说明书.md:69:- 辅导员审批通过 → 通知学生和学工部
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:767:docs/用户设计说明书.md:71:- 学工部审批通过 → 通知学生（审批完成）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:777:docs/用户设计说明书.md:129:| **学工部** | 全校学生 | 审批申请、查看统计、导出数据 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:810:docs/用户设计说明书.md:233:A：学工部用户在"审批统计"页面点击"导出Excel"按钮。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:859:docs/superpowers/plans/2026-05-27-implementation-plan.md:14:- 辅导员和学工部两级审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:900:docs/superpowers/plans/2026-05-27-implementation-plan.md:330:   - 学工部审批逻辑
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:905:docs/superpowers/plans/2026-05-27-implementation-plan.md:342:   - 学工部可以审批所有
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:907:docs/superpowers/plans/2026-05-27-implementation-plan.md:347:- ✓ 学工部审批通过后状态变更为approved
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:964:docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:84:| 班级-辅导员对应关系 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1123:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1160:docs/PROJECT-SUMMARY.md:228:- 两级审批（辅导员→学工部）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1221:docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:104:4. 审批流程具备状态机意识：草稿、待辅导员、待学工部、通过、驳回等状态明确。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1266:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1272:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:50:| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1285:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:112:7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1347:docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:131:- 学工部审批：辅导员通过后24小时内
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1349:docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:137:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1466:docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:40:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1623:docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:172:2. **学工部权限过大**：admin既能审批又能管理系统配置
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1624:docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:182:admin_approver   # 学工部审批员（只能审批）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1625:docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:183:admin_manager    # 学工部管理员（审批+配置管理）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1688:docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:27:2. API认证信息（appKey、appSecret、签名算法）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:2039:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:124:| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:2050:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:204:2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:2061:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:249:| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:2177:docs/design/2026-05-27-system-design.md:627:2. 一个申请必须经过2级审批（辅导员→学工部）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:2224:docs/design/2026-05-27-system-design.md:1342:学工部审批         | ✗       | ✗         | ✓
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:2228:docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:2233:docs/design/2026-05-27-system-design.md:1427:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:2844:- 辅导员和学工部两级审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:4110:    14	- 辅导员和学工部两级审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:4426:   330	   - 学工部审批逻辑
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:4438:   342	   - 学工部可以审批所有
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:4443:   347	- ✓ 学工部审批通过后状态变更为approved
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:4791:2. 是否先做 MVP？是，必须。先做“学生登录/伪登录 -> 提交申请 -> 辅导员审批 -> 学工部审批 -> 状态可查”的端到端最小流程。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:82:先做"学生登录/伪登录 → 提交申请 → 辅导员审批 → 学工部审批 → 状态可查"的端到端最小流程。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:151:- 最小申请审批闭环（提交→辅导员审批→学工部审批→状态查询）
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:96:- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:99:- 学工部审批API
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:102:- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:149:如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:219:最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:82:**问题：** 风险2降级方案说"砍学工部审批，Day 4补学工部审批"，逻辑矛盾
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:88:降级方案：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:93:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:96:**验证：** 降级方案现在明确：Day 3触发后砍学工部审批，Day 4验证辅导员闭环，学工部推Week 2 Day 1
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:1014:- 学工部: `approver=user + step=dean + decision=pending`
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:1089:    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:1146:   - 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:1158:   - 确认辅导员/学工部隔离
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:1172:7. ✓ 辅导员/学工部只看自己pending审批
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:1211:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:1305:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:1493:docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:1710:- ✓ 学工部: approver=user + step=dean + decision=pending
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:1715:- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:1762:- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:1871:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:1920:    22	- ✓ 学工部: approver=user + step=dean + decision=pending
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:1925:    27	- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:1972:    74	- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:2039:   177	    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:2081:   234	   - 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:2093:   246	   - 确认辅导员/学工部隔离
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:2107:   260	7. ✓ 辅导员/学工部只看自己pending审批
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:2156:+   - 学工部仅看 `approver=user + step=dean + decision=pending`。
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:2208:+   - 学工部仅看 `approver=user + step=dean + decision=pending`。
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:2263:+   - 学工部仅看 `approver=user + step=dean + decision=pending`。
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:2392:+   - 学工部仅看 `approver=user + step=dean + decision=pending`。
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:2450:+   - 学工部仅看 `approver=user + step=dean + decision=pending`。
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:2518:   - 学工部仅看 `approver=user + step=dean + decision=pending`。
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:2570:+   - 学工部仅看 `approver=user + step=dean + decision=pending`。
.omc/artifacts/ask/codex-step-2-docs-discussions-week3-day3-planning-2026-05-30-10-cl-2026-05-30T17-08-12-927Z.md:2636:+   - 学工部仅看 `approver=user + step=dean + decision=pending`。
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:85:  - 新：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:14:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:71:如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:77:2. 砍范围明确：砍学工部审批。
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:79:4. 顺延范围明确：学工部审批推到Week 2 Day 1。
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:20:2. **P1-2：降级方案逻辑矛盾** - 风险2说"砍学工部审批"又说"Day 4补学工部审批"
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:46:降级方案：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:51:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:54:**验证点：** 降级逻辑现在清晰：Day 3触发→砍学工部→Day 4验证辅导员闭环→学工部推Week 2 Day 1
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:100:> 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:102:这里“砍学工部审批”和“Day 4补学工部审批”同时出现，口径冲突。更合理的表达是：
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:104:> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:139:**问题：** 同一句话同时说“砍学工部审批”和“Day 4补学工部审批”。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:143:**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:186:2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:137:- ✅ 申请提交流程（学生 → 辅导员 → 学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:138:- ✅ 两级审批流程（辅导员 → 学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:190:- 审批列表页（辅导员/学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:1177:契约允许辅导员和学工部审批通过都通知学生。现有唯一键使用 `entity_type=approval`、`entity_id=approval_id` 时，两个审批步骤会产生两条不同通知，这是合理的。实现文档应明确这一点，避免误以为“申请最终通过”才通知。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:1215:4. 步骤语义：辅导员通过与学工部通过分别产生不同 `approval_id` 的通过通知。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:1249:- 辅导员/学工部通过后创建 `APPROVAL_APPROVED` 给学生；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:1250:- 辅导员/学工部驳回后创建 `APPROVAL_REJECTED` 给学生；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:1269:3. 学工部通过后，学生收到一条 `APPROVAL_APPROVED` 通知，关联 dean approval。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:1376:./docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:61:当前幂等检查只使用 `(entity_type, entity_id, type)`。这会把同一业务实体的同类通知限制为全局唯一，无法支持多个接收者。例如一个未来事件可能需要通知多个学工部账号，或者同一申请的不同待办人。即便 v0.1 当前多数事件只有单接收者，也不应把 schema 固化成全局唯一。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:1543:3. 学工部通过后，学生收到一条`APPROVAL_APPROVED`通知，关联dean approval
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:1609:approver_role = "辅导员" if approval.step == "counselor" else "学工部"
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:1614:approver_role = "辅导员" if approval.step == "counselor" else "学工部"
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:1763:docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:83:契约允许辅导员和学工部审批通过都通知学生。现有唯一键使用 `entity_type=approval`、`entity_id=approval_id` 时，两个审批步骤会产生两条不同通知，这是合理的。实现文档应明确这一点，避免误以为“申请最终通过”才通知。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:1777:docs/contracts/contract-v0.1.md:136:| pending_dean | 学工部通过 | dean | approved | 无 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:1778:docs/contracts/contract-v0.1.md:137:| pending_dean | 学工部驳回 | dean | rejected | 无 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:1787:docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:61:当前幂等检查只使用 `(entity_type, entity_id, type)`。这会把同一业务实体的同类通知限制为全局唯一，无法支持多个接收者。例如一个未来事件可能需要通知多个学工部账号，或者同一申请的不同待办人。即便 v0.1 当前多数事件只有单接收者，也不应把 schema 固化成全局唯一。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:1814:backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:2233:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:2315:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:2741:    approver_role = "辅导员" if approval.step == "counselor" else "学工部"
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:2934:        self.assertIn('学工部', notification.message)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:3592:    52	    approver_role = "辅导员" if approval.step == "counselor" else "学工部"
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:3648:   118	            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:4156:+3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:4400:+3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:4647:3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:4891:+3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-46-58-260Z.md:5141:+3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:59:- 风险2降级方案：改为"保留提交→辅导员审批→查询闭环，砍学工部审批"
.omc/artifacts/ask/codex-week-3-complete-need-next-phase-strategy-discussion-complete-2026-05-30T20-23-08-920Z.md:1146:backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:1262:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:1448:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:2059:        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:2097:        # Step 5: 学工部登录
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:2104:        # Step 6: 学工部审批通过
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:3575:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:3716:        """测试学工部驳回申请"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:4675:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:4687:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:4700:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:4763:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:5115:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:5127:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:5140:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:5203:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:5560:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:5572:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:5585:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:5648:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:6004:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:6016:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:6029:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:6092:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:6447:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:6459:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:6472:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:6535:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:6944:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:6956:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:6969:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:7032:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:7389:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:7401:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:7414:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:7477:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:7976:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:7988:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:8001:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:8064:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:8464:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:8476:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:8489:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:8552:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:8914:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:8926:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:8939:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:9002:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:9435:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:9447:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:9460:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:9523:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:9878:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:9890:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:9903:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:9966:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:10347:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:10359:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:10372:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:10435:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:10954:    PENDING_DEAN = "pending_dean"        # 待学工部审批
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:10993:| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:10995:| pending_dean | 学工部通过 | dean | approved | 无 |
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:10996:| pending_dean | 学工部驳回 | dean | rejected | 无 |
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:11015:| 学工部审批 | ✗ | ✗ | ✓（所有） |
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:11365:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:11377:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:11390:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:11453:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:11763:**学工部（1人）：**
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:12500:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:12512:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:12525:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:12588:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:13047:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:13059:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:13072:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:13135:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:13502:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:13514:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:13527:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:13590:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:13964:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:13976:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:13989:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:14052:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:14471:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:14483:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:14496:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:14559:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:15167:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:15179:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:15192:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:15255:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:15652:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:15664:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:15677:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:15740:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:16144:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:16156:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:16169:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:16232:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:16594:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:16606:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:16619:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:16682:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:17175:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:17187:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:17200:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:17263:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:17758:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:17770:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:17783:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:17846:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:18361:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:18373:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:18386:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:18449:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:19195:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:19207:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:19220:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:19283:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:20055:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:20067:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:20080:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:20143:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:20893:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:20905:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:20918:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:20981:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:21766:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:21778:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:21791:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:21854:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:22604:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:22616:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:22629:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:22692:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:23438:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:23450:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:23463:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:23526:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:24272:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:24284:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:24297:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:24360:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:25106:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:25118:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:25131:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:25194:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:25954:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:25966:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:25979:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:26042:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:26792:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:26804:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:26817:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:26880:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:27589:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:27633:            approver_name='学工部',
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:27703:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:27707:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:27737:            approver_name='学工部1',
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:27932:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:27944:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:27957:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:28020:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:28770:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:28782:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:28795:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:28858:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:29650:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:29662:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:29675:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:29738:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:30441:  +        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:30453:  +        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:30466:  +        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:30525:  +        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:30824:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:30836:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:30849:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:30912:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:31707:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:31719:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:31732:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:31795:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:32613:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:32625:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:32638:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:32701:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:33524:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:33536:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:33549:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:33612:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:34434:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:34446:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:34459:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:34522:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:35348:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:35360:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:35373:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:35436:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:36377:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:36389:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:36402:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:36465:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:37351:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:37363:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:37376:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:37439:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:38320:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:38332:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:38345:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:38408:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:39293:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:39305:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:39318:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:39381:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:40263:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:40275:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:40288:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:40351:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:41321:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:41333:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:41346:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:41409:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:42299:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:42311:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:42324:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:42387:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:43273:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:43285:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:43298:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:43361:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:44244:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:44256:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:44269:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:44332:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:45276:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:45288:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:45301:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:45364:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:46095:   115	            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:46683:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:46695:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:46708:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:46771:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:47492:   123	        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:47504:   135	        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:47517:   148	        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:47757:   127	        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:47992:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:48004:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:48017:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:48080:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:48987:+        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:48999:+        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:49012:+        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:49075:+        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:67:2. **“学工部可以看所有审批”与当前实现冲突**
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:68:   文档建议 [test-coverage-analysis.md](/home/caohui/projects/graduation-leave-system/.omc/collaboration/artifacts/test-coverage-analysis.md:98) 写“学工部可以看所有审批”，但代码是学工部只看自己的 dean 审批：[approvals/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:35)，申请列表也是只看自己的 pending dean 审批：[applications/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/views.py:41)。这里必须先确认产品规则。若当前设计是“指定审批人可见”，测试应改成“学工部只能看自己 assigned 的审批”。
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:82:   覆盖学生详情 403、辅导员详情跨班级 403、学工部非 assigned dean 详情 403、`/api/approvals/?decision=all` 不泄露其他审批人记录。
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:93:2. 有遗漏：详情接口隔离、`decision=all` 历史审批隔离、学工部“全部可见 vs 指定可见”的规则确认、辅导员通过后 dean 审批创建唯一性、API 层驳回后重新提交。
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:904:        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:963:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:1007:            approver_name='学工部',
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:1077:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:1081:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:1111:            approver_name='学工部1',
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:1190:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:1270:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:1624:        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:1662:        # Step 5: 学工部登录
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:1669:        # Step 6: 学工部审批通过
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:2055:        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:2067:        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:2080:        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:2142:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:2177:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:2366:        """测试学工部驳回申请"""
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:2846:    98	   - 学工部可以看所有审批
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:2908:    35	    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:2988:   115	            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:3263:    30	        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:3307:    74	            approver_name='学工部',
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:3610:   127	        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:3647:2. **“学工部可以看所有审批”与当前实现冲突**
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:3648:   文档建议 [test-coverage-analysis.md](/home/caohui/projects/graduation-leave-system/.omc/collaboration/artifacts/test-coverage-analysis.md:98) 写“学工部可以看所有审批”，但代码是学工部只看自己的 dean 审批：[approvals/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:35)，申请列表也是只看自己的 pending dean 审批：[applications/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/views.py:41)。这里必须先确认产品规则。若当前设计是“指定审批人可见”，测试应改成“学工部只能看自己 assigned 的审批”。
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:3662:   覆盖学生详情 403、辅导员详情跨班级 403、学工部非 assigned dean 详情 403、`/api/approvals/?decision=all` 不泄露其他审批人记录。
.omc/artifacts/ask/codex-omc-collaboration-artifacts-test-coverage-analysis-md-gap-1--2026-06-01T03-36-40-648Z.md:3673:2. 有遗漏：详情接口隔离、`decision=all` 历史审批隔离、学工部“全部可见 vs 指定可见”的规则确认、辅导员通过后 dean 审批创建唯一性、API 层驳回后重新提交。
.omc/artifacts/ask/codex-phase-4b-student-application-miniprogram-pages-student-appli-2026-06-01T02-23-37-379Z.md:1730:    35	    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-phase-4b-student-application-miniprogram-pages-student-appli-2026-06-01T02-23-37-379Z.md:1810:   115	            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-phase-4b-student-application-miniprogram-pages-student-appli-2026-06-01T02-23-37-379Z.md:1950:    48	        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-phase-4b-student-application-miniprogram-pages-student-appli-2026-06-01T02-23-37-379Z.md:1988:    86	        # Step 5: 学工部登录
.omc/artifacts/ask/codex-phase-4b-student-application-miniprogram-pages-student-appli-2026-06-01T02-23-37-379Z.md:1995:    93	        # Step 6: 学工部审批通过
.omc/artifacts/ask/codex-phase-4b-student-application-miniprogram-pages-student-appli-2026-06-01T02-23-37-379Z.md:2458:测试学工部驳回申请
.omc/artifacts/ask/codex-phase-4b-student-application-miniprogram-pages-student-appli-2026-06-01T02-23-37-379Z.md:2468:测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询
.omc/artifacts/ask/codex-phase-4b-student-application-miniprogram-pages-student-appli-2026-06-01T02-23-37-379Z.md:2643:backend/apps/approvals/tests/test_list_permissions.py:59:            approver_name='学工部1',
.omc/artifacts/ask/codex-phase-4b-student-application-miniprogram-pages-student-appli-2026-06-01T02-23-37-379Z.md:2697:backend/apps/applications/tests/test_list_permissions.py:74:            approver_name='学工部',
.omc/artifacts/ask/codex-phase-4b-student-application-miniprogram-pages-student-appli-2026-06-01T02-23-37-379Z.md:2891:     9	    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:88:  - 学生本人、负责辅导员、当前/相关学工部可看
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:97:- 学工部：只能查看自己相关 dean approval 的申请附件
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:98:- 无关学生、无关辅导员、无关学工部：403
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:2014:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:2023:docs/PROJECT-SUMMARY.md:858:- 排除：独立辅导员/学工部页面集、草稿、完整附件UX、高级过滤、通知中心、审计时间线、React Native
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:2122:.omc/artifacts/ask/codex-phase-4a-blocked-on-phase4a-waiting-for-devtools-phase-4b-ph-2026-06-01T01-33-23-790Z.md:1061:- 排除：独立辅导员/学工部页面集、草稿、完整附件UX、高级过滤、通知中心、审计时间线、React Native
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:2217:.omc/artifacts/ask/codex-phase-1-docs-discussions-week3-day3-planning-2026-05-30-07-c-2026-05-30T16-44-42-656Z.md:1526:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:2481:.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md:1123:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:2748:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:741:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:3002:.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md:1119:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:3026:.omc/artifacts/ask/codex-student-application-api-createdefaultapiclient-reason-leave--2026-06-01T01-42-06-938Z.md:1855:- 排除：独立辅导员/学工部页面集、草稿、完整附件UX、高级过滤、通知中心、审计时间线、React Native
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:3251:.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1377:./docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:3373:.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md:1385:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:3418:.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1754:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:3511:.omc/artifacts/ask/codex-phase-4a-readiness-repair-complete-fixed-all-4-issues-stale--2026-05-31T03-30-57-980Z.md:6216:docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:3888:    35	    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:3968:   115	            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:4236:     9	    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:4295:  - 学生本人、负责辅导员、当前/相关学工部可看
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:4304:- 学工部：只能查看自己相关 dean approval 的申请附件
.omc/artifacts/ask/codex-6-48-phase-4b-role-guard-ts-date-ts-p0-ui-detail-approval-le-2026-06-01T04-18-35-149Z.md:4305:- 无关学生、无关辅导员、无关学工部：403
backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:55:- **最小角色校验**（学生/辅导员/学工部边界）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:58:- 学工部审批API
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:117:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:215:- [ ] 学工部审批API
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:228:- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头
.omc/artifacts/ask/codex-docs-discussions-week3-day1-review-2026-05-30-17-claude-next-2026-05-30T15-17-01-336Z.md:1195:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:161:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:106:- `backend/apps/applications/views.py:85` 只限制学生访问他人申请，辅导员/学工部查询范围还没收紧。
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:133:   - 学工部：看全部或待学工部审批
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:137:   smoke 应该走真实使用路径：登录 → 学生提交 → 辅导员从待办列表拿到申请/审批 ID → 审批 → 学工部从待办列表拿到审批 ID → 审批 → 学生查询最终状态。
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1089:    PENDING_DEAN = "pending_dean"        # 待学工部审批
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1128:| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1130:| pending_dean | 学工部通过 | dean | approved | 无 |
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1131:| pending_dean | 学工部驳回 | dean | rejected | 无 |
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1150:| 学工部审批 | ✗ | ✗ | ✓（所有） |
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1263:**目标用户：** 学校管理人员、辅导员、学工部
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1277:- **学工部端：** 审批所有学生的离校申请、查看全校审批统计、导出审批数据
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1309:学生提交 → 辅导员审批 → 学工部审批 → 审批完成
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1316:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1327:- 辅导员审批通过 → 通知学生和学工部
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1329:- 学工部审批通过 → 通知学生（审批完成）
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1330:- 学工部驳回 → 通知学生
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1375:- 学工部可以查看所有学生
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1387:| **学工部** | 全校学生 | 审批申请、查看统计、导出数据 |
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1409:**学工部权限：**
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1491:A：学工部用户在"审批统计"页面点击"导出Excel"按钮。
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1754:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1955:  - UserDTO字段对教师/学工部不可选
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1974:  - P1-2：降级方案逻辑矛盾（风险2说"砍学工部审批"又说"Day 4补学工部审批"）
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:1979:  - P1-2修复：修复风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2000:  - 1学工部（D001，默认密码为工号）
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2010:**范围：** 登录 → 提交 → 辅导员审批 → 学工部审批 → 查询状态
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2045:- [ ] 1个学工部
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2187:### 5. 学工部能进行最终审批 ✓/✗
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2191:**Step 1: 学工部登录**
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2242:- [ ] 学工部能登录
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2248:- 检查学工部权限配置
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2414:**学工部（1人）：**
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2596:  - 辅导员通过→pending_dean（创建学工部审批记录）
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2598:  - 学工部通过→approved
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2599:  - 学工部驳回→rejected
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2603:  - 学工部只能审批学工部步骤
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2615:  - 完整流程：登录→提交→辅导员审批→学工部审批→查询
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2626:  - 学工部驳回：pending_dean→rejected
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2656:- ✓ Seed数据需求：2学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2667:- ✓ Seed数据导入：10学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2673:  5. 学工部审批成功 - status→approved
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2736:   - 受众：学校管理人员、辅导员、学工部
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2747:- 学生、辅导员、学工部三种角色
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2759:- 两级审批（辅导员→学工部）
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2914:- **学工部：** 1个
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2961:### 3. 学工部账号（Dean）
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2964:**用途：** 测试学工部审批
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2974:- 学工部能审批所有通过辅导员审批的申请
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2975:- 学工部不能直接审批pending_counselor状态的申请
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:3045:- [ ] 1个学工部账号创建成功
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:3053:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:3187:     8	    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:3334:     8	    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:3379:     8	    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:3593:    75	        """测试学工部驳回申请"""
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:3894:    39	        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:3932:    77	        # Step 5: 学工部登录
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:3939:    84	        # Step 6: 学工部审批通过
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:4243:测试学工部驳回申请
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:4253:测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:4809:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:4998:- `backend/apps/applications/views.py:85` 只限制学生访问他人申请，辅导员/学工部查询范围还没收紧。
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:5025:   - 学工部：看全部或待学工部审批
.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:5029:   smoke 应该走真实使用路径：登录 → 学生提交 → 辅导员从待办列表拿到申请/审批 ID → 审批 → 学工部从待办列表拿到审批 ID → 审批 → 学生查询最终状态。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:11:**重要说明：本项目只对接宿管系统，不直接对接教务、人事、学工等其他系统。**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:23:2. **数据归集：** 宿管系统已从教务、人事、学工等系统归集了所需数据
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:40:**Codex意见：** 将"提交给宿管系统方"改为"提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人"。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:47:1. 本系统只对接宿管系统，不直接对接教务、人事、学工
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:61:- 在待反馈问题中增加："宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？如不包含，能否从教务/人事/学工系统归集后提供？"
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:84:| 班级-辅导员对应关系 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:357:| 学工部管理员 | 当前在职 | 5人 | 手动创建 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:377:2. 如不包含，能否从教务/人事/学工系统归集后提供？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:468:   - 理由：项目只对接宿管系统，不直接对接教务/人事/学工
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:540:1. **项目约束确认：** 我们明确项目只对接宿管系统，不直接对接教务/人事/学工。Codex是否认同这个约束下，原文档的反馈对象（宿管系统方）是正确的？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:16:**问题2：** 如不包含，能否从教务/人事/学工系统归集后提供？
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:674:> "学工部可以看所有审批" 与代码不符
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:679:  # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:694:**Action:** Remove "学工部可以看所有审批" from test plan.
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:835:   - Expected: 409 CONFLICT "学工部审批已存在，不能重复创建"
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:993:./docs/api/contract-v0.2.md:20:| `pending_dean` | Awaiting dean approval | 待学工部审批 |
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:998:./docs/api/contract-v0.2.md:41:| `dean` | Dean approval step | 学工部审批 |
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1095:./docs/week3-day0-seed-data-requirements.md:63:**用途：** 测试学工部审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1096:./docs/week3-day0-seed-data-requirements.md:73:- 学工部能审批所有通过辅导员审批的申请
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1097:./docs/week3-day0-seed-data-requirements.md:74:- 学工部不能直接审批pending_counselor状态的申请
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1108:./docs/week3-day0-acceptance-checklist.md:5:**范围：** 登录 → 提交 → 辅导员审批 → 学工部审批 → 查询状态
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1127:./docs/week3-day0-acceptance-checklist.md:182:### 5. 学工部能进行最终审批 ✓/✗
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1152:./docs/week3-day0-acceptance-checklist.md:393:- [ ] check_status方法签名
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1158:./docs/week3-day0-acceptance-checklist.md:451:# 4. 学工部审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1160:./docs/week3-day0-acceptance-checklist.md:462:echo "✓ 学工部审批成功"
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1166:./docs/week3-day0-acceptance-checklist.md:497:6. 学工部审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1221:./docs/用户设计说明书.md:19:- **学工部端：** 审批所有学生的离校申请、查看全校审批统计、导出审批数据
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1224:./docs/用户设计说明书.md:51:学生提交 → 辅导员审批 → 学工部审批 → 审批完成
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1227:./docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1230:./docs/用户设计说明书.md:69:- 辅导员审批通过 → 通知学生和学工部
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1231:./docs/用户设计说明书.md:71:- 学工部审批通过 → 通知学生（审批完成）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1234:./docs/用户设计说明书.md:129:| **学工部** | 全校学生 | 审批申请、查看统计、导出数据 |
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1256:./docs/用户设计说明书.md:233:A：学工部用户在"审批统计"页面点击"导出Excel"按钮。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1329:./docs/contracts/contract-v0.1.md:95:    PENDING_DEAN = "pending_dean"        # 待学工部审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1335:./docs/contracts/contract-v0.1.md:134:| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1339:./docs/contracts/contract-v0.1.md:156:| 学工部审批 | ✗ | ✗ | ✓（所有） |
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1372:./docs/contracts/contract-v0.1.md:640:    # 4. 学工部审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1377:./docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1386:./docs/PROJECT-SUMMARY.md:233:  - P1-2：降级方案逻辑矛盾（风险2说"砍学工部审批"又说"Day 4补学工部审批"）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1387:./docs/PROJECT-SUMMARY.md:238:  - P1-2修复：修复风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1396:./docs/PROJECT-SUMMARY.md:281:  - 辅导员通过→pending_dean（创建学工部审批记录）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1398:./docs/PROJECT-SUMMARY.md:288:  - 学工部只能审批学工部步骤
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1399:./docs/PROJECT-SUMMARY.md:300:  - 完整流程：登录→提交→辅导员审批→学工部审批→查询
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1406:./docs/PROJECT-SUMMARY.md:358:  5. 学工部审批成功 - status→approved
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1425:./docs/PROJECT-SUMMARY.md:460:  - Happy path: 学生→辅导员→学工部审批流程 ✓
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1432:./docs/PROJECT-SUMMARY.md:524:- 两级审批（辅导员→学工部）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1469:./docs/PROJECT-SUMMARY.md:856:- 核心功能：登录、学生提交、列表、详情、辅导员/学工部审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1491:./docs/superpowers/plans/2026-05-27-implementation-plan.md:14:- 辅导员和学工部两级审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1515:./docs/superpowers/plans/2026-05-27-implementation-plan.md:330:   - 学工部审批逻辑
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1522:./docs/superpowers/plans/2026-05-27-implementation-plan.md:342:   - 学工部可以审批所有
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1524:./docs/superpowers/plans/2026-05-27-implementation-plan.md:347:- ✓ 学工部审批通过后状态变更为approved
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1564:./docs/plans/week-0-1-execution-plan.md:92:  - 创建学工部审批记录（通过时）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1565:./docs/plans/week-0-1-execution-plan.md:93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1566:./docs/plans/week-0-1-execution-plan.md:94:  - 最小角色校验：只有学工部可审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1570:./docs/plans/week-0-1-execution-plan.md:108:- [ ] 学工部可审批（通过/驳回）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1573:./docs/plans/week-0-1-execution-plan.md:113:- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1574:./docs/plans/week-0-1-execution-plan.md:114:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1575:./docs/plans/week-0-1-execution-plan.md:120:  - 测试1：学生登录 → 提交申请 → 辅导员审批通过 → 学工部审批通过 → 查询状态
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1579:./docs/plans/week-0-1-execution-plan.md:180:**降级方案：** 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1580:./docs/plans/week-0-1-execution-plan.md:182:### 风险3：Week 1 Day 4学工部审批未完成
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1608:./docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:27:- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1647:./docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:68:- 学工部: 返回待自己审批的记录（step='dean', decision='pending'）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1715:./docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:104:4. 审批流程具备状态机意识：草稿、待辅导员、待学工部、通过、驳回等状态明确。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1730:./backend/apps/approvals/views.py:35:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1759:./backend/apps/approvals/views.py:115:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1824:./docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:222:2. ✓ 辅导员/学工部只看自己pending审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1893:./backend/apps/approvals/tests/test_permissions.py:123:        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1896:./backend/apps/approvals/tests/test_permissions.py:135:        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1900:./backend/apps/approvals/tests/test_permissions.py:148:        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1913:./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1933:./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:163:- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:1999:./backend/apps/approvals/tests/test_state_machine.py:127:        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2065:./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:131:- 学工部审批：辅导员通过后24小时内
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2067:./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:137:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2153:./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:40:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2326:./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:172:2. **学工部权限过大**：admin既能审批又能管理系统配置
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2327:./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:182:admin_approver   # 学工部审批员（只能审批）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2328:./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:183:admin_manager    # 学工部管理员（审批+配置管理）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2438:./docs/design/2026-05-27-system-design.md:627:2. 一个申请必须经过2级审批（辅导员→学工部）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2470:./docs/design/2026-05-27-system-design.md:1342:学工部审批         | ✗       | ✗         | ✓
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2477:./docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2479:./docs/design/2026-05-27-system-design.md:1427:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2575:./backend/apps/applications/migrations/0001_initial.py:22:                ('status', models.CharField(choices=[('draft', '草稿'), ('pending_counselor', '待辅导员审批'), ('pending_dean', '待学工部审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='draft', max_length=20)),
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2602:./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:177:    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2615:./docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md:260:7. ✓ 辅导员/学工部只看自己pending审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2655:./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:110:- 学工部审批是否也需要权限校验？（当前硬编码D001）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2662:./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:149:- 学工部如何知道有哪些申请需要审批？
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2673:./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:14:计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2674:./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:26:| 审批权限 | 0.5h | 1-1.5h | approve/reject都要改；需要覆盖辅导员、学工部、查看权限 |
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2683:./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:60:- `approval.approver_id == user.user_id`，对辅导员和学工部都适用。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2685:./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:62:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2868:./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:309:2. 根据角色自动过滤（学生看自己，辅导员看待审批，学工部看待审批）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:2999:./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:25:- ⚠ 部分达标：4/8（Seed数据、学工部审批、负向权限、宿舍清退Mock）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3005:./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:64:**7. 缺少列表接口**：辅导员/学工部看不到待审批列表
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3023:./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:33:| 5. 学工部最终审批 | ⚠ 部分达标 | 主路径达标，但缺列表接口，dean硬编码 |
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3032:./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:72:**问题：** "辅导员能看到自己班级申请""学工部能看到全部待审批申请"没有列表接口  
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3046:./backend/apps/applications/models.py:9:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3113:./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:58:- 学工部审批API
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3119:./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:116:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3126:./docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:210:- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3170:./backend/apps/applications/tests/test_application_flow.py:50:        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3179:./backend/apps/applications/tests/test_application_flow.py:95:        # Step 6: 学工部审批通过
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3192:./docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:85:  - 新：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3226:./docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:14:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3228:./docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:71:如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3229:./docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:77:2. 砍范围明确：砍学工部审批。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3231:./docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:79:4. 顺延范围明确：学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3241:./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:82:**问题：** 风险2降级方案说"砍学工部审批，Day 4补学工部审批"，逻辑矛盾
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3242:./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:88:降级方案：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3243:./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:93:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3244:./docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:96:**验证：** 降级方案现在明确：Day 3触发后砍学工部审批，Day 4验证辅导员闭环，学工部推Week 2 Day 1
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3256:./docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:20:2. **P1-2：降级方案逻辑矛盾** - 风险2说"砍学工部审批"又说"Day 4补学工部审批"
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3257:./docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:46:降级方案：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3258:./docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:51:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3261:./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:58:- 学工部审批API
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3268:./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:117:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3275:./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:215:- [ ] 学工部审批API
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3278:./docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:228:- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3290:./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:96:- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3292:./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:99:- 学工部审批API
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3294:./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:102:- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3300:./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:149:如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3307:./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:219:最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3329:./docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:59:- 风险2降级方案：改为"保留提交→辅导员审批→查询闭环，砍学工部审批"
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3334:./docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:82:先做"学生登录/伪登录 → 提交申请 → 辅导员审批 → 学工部审批 → 状态可查"的端到端最小流程。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3337:./docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:151:- 最小申请审批闭环（提交→辅导员审批→学工部审批→状态查询）
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3384:./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:100:> 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3385:./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:102:这里“砍学工部审批”和“Day 4补学工部审批”同时出现，口径冲突。更合理的表达是：
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3386:./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:104:> 如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证“提交 -> 辅导员审批 -> 查询”闭环；学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3388:./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:139:**问题：** 同一句话同时说“砍学工部审批”和“Day 4补学工部审批”。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3390:./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:143:**修复建议：** 明确Day 3触发后只保“提交 -> 辅导员审批 -> 查询”，学工部审批统一推到Week 2 Day 1。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3392:./docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:186:2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3394:./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:33:**问题：** 风险2说"砍学工部审批"又说"Day 4补学工部审批"
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3395:./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:37:降级方案：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3396:./docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:42:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3606:        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3758:        """学工部不能处理辅导员审批步骤"""
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3770:        """辅导员不能处理学工部审批步骤"""
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3783:        """同角色但非指定学工部审批人不能处理审批"""
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3830:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:3956:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:4036:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:4112:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:4365:        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:4403:        # Step 5: 学工部登录
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:4410:        # Step 6: 学工部审批通过
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:4537:        """测试学工部驳回申请"""
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:4621:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:4665:            approver_name='学工部',
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:4735:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:4739:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:4769:            approver_name='学工部1',
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:4831:    35	    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:4911:   115	            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:5071:     9	    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-4-omc-collaboration-artifacts-test-coverage-claude-response--2026-06-01T04-07-17-714Z.md:5236:   127	        """测试学工部审批步骤与申请状态不匹配时返回409"""
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:199:2. 如果使用自签名证书，对接方是否能接受？
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:16:- ❌ 管理员数据（辅导员、学工部管理员）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:29:| 学工部管理员 | admin | ~5人 | 终审备案 | 人事系统 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:134:### 3.5 学工部管理员信息
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:139:- 创建学工部管理员账号
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:269:| 学工部管理员信息 | 人事系统 | 手动创建 | 数量少，可手动 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:316:4. **学工部管理员是否需要数据对接？**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:19:| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:254:### 3.1 学工部管理员信息
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:257:- 创建学工部管理员账号
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:412:5. 学工部管理员：手动创建（~5人）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:172:2. **学工部权限过大**：admin既能审批又能管理系统配置
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:182:admin_approver   # 学工部审批员（只能审批）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:183:admin_manager    # 学工部管理员（审批+配置管理）
docs/discussions/codex-review-2026-05-27/04-database-review.md:181:    admin_id BIGINT COMMENT '学工部管理员ID',
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:15:1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:36:| 学工部管理员信息 | P1 合理 | 人数少，手动创建比外部对接更合理。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:46:1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:105:### 3.5 学工部管理员信息
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:124:| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:125:| 学工部管理员信息 | 手动创建 | 合理。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:156:| 学工部管理员 | 约 5 人 | 合理。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:174:> 请教务系统、人事系统、学工部数据负责人、宿管系统方分别确认其可提供的数据范围、字段、对接方式和联系人。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:186:7. 学工部终审人是固定个人、固定角色组、轮值还是人工分配？
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:204:2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:207:5. 学工部管理员：手动创建，同时配置默认终审人或终审组。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:239:> 明确毕业离校系统所需的数据源，提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人反馈。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:249:| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:309:1. 将反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:62:3. **自签名证书**：对接方需要信任自签名证书，增加配置复杂度
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:54:- 学工部终审备案
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:104:4. 审批流程具备状态机意识：草稿、待辅导员、待学工部、通过、驳回等状态明确。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:35:| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:50:| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:84:### 4. 学工部管理员数据源是否需要对接？
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:112:7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:136:6. **手动创建学工部管理员。** 同时补充管理员账号维护和终审人分配规则。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:163:- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:176:- admin_id BIGINT（固定学工部管理员ID）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:40:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:41:| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:237:### 2.5 学工部管理员信息
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:249:| 部门 | department | 文本 | 是 | 所属部门 | 学工部 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:478:| 学工部管理员 | 当前在职 | 5人 | 手动创建 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:515:2. 如不包含，能否从教务/人事/学工系统归集后提供？
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:1948:backend/apps/approvals/tests/test_state_machine.py:127:        """测试学工部审批步骤与申请状态不匹配时返回409"""
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3070:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:20:   - 审批权限：只校验approver_id够吗？是否需要校验class_id？学工部D001硬编码怎么办？
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3071:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:54:   - 审批权限：只校验approver_id够吗？是否需要校验class_id？学工部D001硬编码怎么办？
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3072:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:120:   - 审批权限：只校验approver_id够吗？是否需要校验class_id？学工部D001硬编码怎么办？
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3074:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:1002:- 学工部审批是否也需要权限校验？（当前硬编码D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3096:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2013:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3105:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2112:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3107:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2213:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3116:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2312:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3118:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2476:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3127:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2575:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3129:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2679:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3138:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2778:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3140:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2883:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3149:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2982:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3151:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3085:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3160:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3184:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3162:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3304:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3171:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3403:+- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3263:docs/PROJECT-SUMMARY.md:259:  - 1学工部（D001，默认密码为工号）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3322:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-10-clau-2026-05-30T14-36-35-991Z.md:3387:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3370:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:62:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3379:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:161:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3511:backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3533:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:31:   - 1学工部（D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3536:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:38:   - 学工部D001审批 → status=approved
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3538:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:88:   - 1学工部（D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3541:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:95:   - 学工部D001审批 → status=approved
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3543:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:136:5. 学工部最终审批：主路径达标，但“能看到所有待审批申请”没有接口支撑；且 dean 审批人硬编码为 `D001`：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:48)。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3547:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:226:   - 1学工部（D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3550:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:233:   - 学工部D001审批 → status=approved
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3611:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:3117:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3649:.omc/artifacts/ask/codex-week-3-day-1-week-3-plan-d-2-timebox-day-1-day-1-8-4-p0-day--2026-05-30T09-57-40-097Z.md:6453:5. 学工部最终审批：主路径达标，但“能看到所有待审批申请”没有接口支撑；且 dean 审批人硬编码为 `D001`：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:48)。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3687:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:987:  - 1学工部（D001，默认密码为工号）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3702:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:1627:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3723:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2257:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3729:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2367:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3742:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2786:backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3745:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-22-35-514Z.md:2809:backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3765:docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:110:- 学工部审批是否也需要权限校验？（当前硬编码D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3775:docs/week3-day0-seed-data-requirements.md:152:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3791:docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:182:3. 学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3796:docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:118:- 学工部D001硬编码应该修复（从User表查询唯一dean）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3806:docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:329:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3899:docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:71:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3955:.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:16:- 数据：seed_data支持10学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3957:.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:53:- 数据：seed_data支持10学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3960:.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:144:- 数据：seed_data支持10学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3972:.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:1526:  - 1学工部（D001，默认密码为工号）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:3991:.omc/artifacts/ask/codex-phase-1-3-dean-status-smoke-test-smoke-test-api-approve-reje-2026-05-30T18-34-32-995Z.md:2062:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4055:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-10-clau-2026-05-30T14-36-08-992Z.md:2418:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4159:.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:3309:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1678:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:62:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4242:.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:4956:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2013:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4245:.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:4976:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2213:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4248:.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:4997:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2476:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4251:.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5017:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2679:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4254:.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5039:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:2883:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4257:.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5059:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3085:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4260:.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:5081:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T10-09-06-045Z.md:3304:+- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4287:.omc/artifacts/ask/codex-phase-2a-2b-p0-resubmission-approval-filter-typescript-types-2026-05-30T19-10-22-093Z.md:6220:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4311:backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4326:.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:14:3. ✓ 学工部看到1条pending审批（approver=D001, decision=pending）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4328:.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:37:3. ✓ 学工部看到1条pending审批（approver=D001, decision=pending）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4330:.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:86:3. ✓ 学工部看到1条pending审批（approver=D001, decision=pending）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4384:.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4668:backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4385:.omc/artifacts/ask/codex-phase-2-p0-typescript-types-api-client-mock-fixtures-phase-a-2026-05-30T19-53-48-774Z.md:4671:backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4418:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:613:3. 学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4456:.omc/artifacts/ask/codex-claude-day-2-docs-discussions-week3-day1-review-2026-05-30-0-2026-05-30T14-29-49-229Z.md:1678:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:62:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4853:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:1632:./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:110:- 学工部审批是否也需要权限校验？（当前硬编码D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4869:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2247:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4877:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:2355:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4921:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4711:backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4923:.omc/artifacts/ask/codex-phase-1-day-3-get-api-approvals-get-api-applications-12-24-2-2026-05-30T18-20-58-931Z.md:4735:backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4971:.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4085:.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:14:3. ✓ 学工部看到1条pending审批（approver=D001, decision=pending）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4973:.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4088:.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:37:3. ✓ 学工部看到1条pending审批（approver=D001, decision=pending）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:4975:.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:4092:.omc/artifacts/ask/codex-step-2-1-get-api-approvals-403-2-count-results-next-previous-2026-05-30T17-53-21-975Z.md:86:3. ✓ 学工部看到1条pending审批（approver=D001, decision=pending）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5030:.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:7012:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5044:.omc/artifacts/ask/codex-week-3-phase-2-p0-resubmission-approval-filter-phase-a-skele-2026-05-30T19-58-57-411Z.md:7491:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5115:.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:2808:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5257:.omc/artifacts/ask/codex-task-20260530-06-re-verification-after-blocker-fix-context-c-2026-05-30T14-31-47-231Z.md:2132:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:161:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5748:.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:1080:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5758:.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:2061:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5784:.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:3003:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5821:.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:2000:  - 1学工部（D001，默认密码为工号）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5847:.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:3053:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5914:.omc/artifacts/ask/codex-day-0-4-1-week-3-day-1-2-3-vs-1-2-3-4-2026-05-30T14-38-15-508Z.md:4809:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:5990:.omc/artifacts/ask/codex-docs-discussions-week3-day1-review-2026-05-30-17-claude-next-2026-05-30T15-17-01-336Z.md:1195:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:161:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6360:.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:27589:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6366:.omc/artifacts/ask/codex-review-claude-s-response-at-omc-collaboration-artifacts-2026-2026-05-30T20-16-52-737Z.md:27703:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6624:.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:838:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1648:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6690:.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3260:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6699:.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3359:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6702:.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:3466:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6739:.omc/artifacts/ask/codex-day-3-docs-discussions-week3-day3-planning-2026-05-30-01-cla-2026-05-30T16-00-18-381Z.md:4816:    71	- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6748:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:853:- 学工部D001硬编码应该修复（从User表查询唯一dean）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6758:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1070:- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6762:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1254:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:161:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6774:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:1648:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6786:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:3233:   118	- 学工部D001硬编码应该修复（从User表查询唯一dean）
.omc/artifacts/ask/codex-week-4-prep-bundle-complete-event-66-created-3-focused-docs--2026-05-31T03-10-06-623Z.md:6792:.omc/artifacts/ask/codex-claude-docs-discussions-week3-day1-review-2026-05-30-05-clau-2026-05-30T10-19-43-667Z.md:3351:   329	- 修复：学工部从User表查询（不硬编码D001）
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:83:我会把首个可验收目标定为：辅导员或学工部登录后，能从待审批列表进入详情并完成通过操作，状态刷新正确。
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:588:docs/plans/week-0-1-execution-plan.md:182:### 风险3：Week 1 Day 4学工部审批未完成
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:644:docs/PROJECT-SUMMARY.md:233:  - P1-2：降级方案逻辑矛盾（风险2说"砍学工部审批"又说"Day 4补学工部审批"）
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:649:docs/PROJECT-SUMMARY.md:238:  - P1-2修复：修复风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:660:docs/PROJECT-SUMMARY.md:352:- ✓ Seed数据导入：10学生+2辅导员+1学工部+2班级映射
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:728:docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:14:计划抓住了主要P1方向，但还停留在“列出修复点”的层面，没有把修复间依赖、测试基线、迁移成本、并发验证、数据重置和列表发现能力纳入执行设计。4小时估算明显过乐观；把列表接口降为可选也不成立，因为没有列表接口，辅导员/学工部无法从产品流程中发现待审批申请，验收仍依赖数据库或前一步响应里的内部ID。
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:1278:docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:82:**问题：** 风险2降级方案说"砍学工部审批，Day 4补学工部审批"，逻辑矛盾
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:1379:docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md:14:**理由：** 上一轮指出的2个P1阻塞问题已经解决。`contract-v0.1.md` Section 3定义的8个错误码在Section 6.2均有错误Mock样例；`week-0-1-execution-plan.md` 风险2不再同时承诺“砍学工部审批”和“Day 4补学工部审批”，降级路径已经改为先保最短闭环，学工部审批顺延到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:1455:docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:59:- 风险2降级方案：改为"保留提交→辅导员审批→查询闭环，砍学工部审批"
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:1556:docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:33:**问题：** 风险2说"砍学工部审批"又说"Day 4补学工部审批"
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:1608:docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md:20:2. **P1-2：降级方案逻辑矛盾** - 风险2说"砍学工部审批"又说"Day 4补学工部审批"
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:1655:docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:40:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:1656:docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:41:| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:1737:docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:84:| 班级-辅导员对应关系 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:1921:docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:19:| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2033:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:15:1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2037:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:36:| 学工部管理员信息 | P1 合理 | 人数少，手动创建比外部对接更合理。 |
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2048:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:124:| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2058:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:204:2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2066:docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:249:| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2076:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2081:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:35:| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2089:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:50:| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2111:docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:163:- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2180:docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:186:2. 修改风险2降级方案，明确Day 3触发后学工部审批推到Week 2 Day 1。
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2313:    PENDING_DEAN = "pending_dean"        # 待学工部审批
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2352:| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2354:| pending_dean | 学工部通过 | dean | approved | 无 |
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2355:| pending_dean | 学工部驳回 | dean | rejected | 无 |
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2374:| 学工部审批 | ✗ | ✗ | ✓（所有） |
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2588:**学工部（1人）：**
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:2998:    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:3079:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:3273:    # 4. 学工部审批
.omc/artifacts/ask/codex-week-3-closure-gate-smoke-test-api-10-p0-p1-p2-v0-2-csv-1-sk-2026-05-30T18-51-57-674Z.md:4075:我会把首个可验收目标定为：辅导员或学工部登录后，能从待审批列表进入详情并完成通过操作，状态刷新正确。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:98:1. 反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:216:| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:451:### 3.1 学工部管理员信息
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:454:- 创建学工部管理员账号
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:536:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:544:| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:559:| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:593:### 4. 学工部管理员数据源是否需要对接？
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:621:7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:645:6. **手动创建学工部管理员。** 同时补充管理员账号维护和终审人分配规则。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:672:- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:695:- ❌ 管理员数据（辅导员、学工部管理员）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:708:| 学工部管理员 | admin | ~5人 | 终审备案 | 人事系统 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:813:### 3.5 学工部管理员信息
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:818:- 创建学工部管理员账号
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1095:5. 学工部管理员：手动创建（~5人）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1200:docs/用户设计说明书.md:5:**目标用户：** 学校管理人员、辅导员、学工部
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1204:docs/用户设计说明书.md:19:- **学工部端：** 审批所有学生的离校申请、查看全校审批统计、导出审批数据
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1214:docs/用户设计说明书.md:51:学生提交 → 辅导员审批 → 学工部审批 → 审批完成
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1218:docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1225:docs/用户设计说明书.md:69:- 辅导员审批通过 → 通知学生和学工部
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1227:docs/用户设计说明书.md:71:- 学工部审批通过 → 通知学生（审批完成）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1228:docs/用户设计说明书.md:72:- 学工部驳回 → 通知学生
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1240:docs/用户设计说明书.md:117:- 学工部可以查看所有学生
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1243:docs/用户设计说明书.md:129:| **学工部** | 全校学生 | 审批申请、查看统计、导出数据 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1278:docs/用户设计说明书.md:233:A：学工部用户在"审批统计"页面点击"导出Excel"按钮。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1309:docs/design/2026-05-27-system-design.md:187:   - 学生/辅导员/学工部用户管理
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1341:docs/design/2026-05-27-system-design.md:300:- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1348:docs/design/2026-05-27-system-design.md:314:    admin_id BIGINT COMMENT '学工部管理员ID',
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1369:docs/design/2026-05-27-system-design.md:387:- `approver_role`: counselor（辅导员）、admin（学工部）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1370:docs/design/2026-05-27-system-design.md:389:- `time_limit`: 辅导员1个工作日(24小时)，学工部1个工作日(24小时)
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1406:docs/design/2026-05-27-system-design.md:599:  ├─N:1─→ users (学工部管理员)
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1419:docs/design/2026-05-27-system-design.md:627:2. 一个申请必须经过2级审批（辅导员→学工部）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1479:docs/design/2026-05-27-system-design.md:1325:admin（学工部管理员）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1483:docs/design/2026-05-27-system-design.md:1342:学工部审批         | ✗       | ✗         | ✓
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1491:docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1498:docs/design/2026-05-27-system-design.md:1427:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1512:docs/design/2026-05-27-system-design.md:1463:- 权限要求：学工部管理员角色 + current_approver_id匹配
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1516:docs/design/2026-05-27-system-design.md:1473:    - 创建历史快照：applications_history（version=N, change_reason='学工部备案通过'）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1520:docs/design/2026-05-27-system-design.md:1482:    - 创建历史快照：applications_history（version=N, change_reason='学工部驳回'）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1880:- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1894:    admin_id BIGINT COMMENT '学工部管理员ID',
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1935:- `pending_admin` - 待学工部备案
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:1956:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2003:+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2024:+| 学工部管理员信息 | P1 合理 | 人数少，手动创建比外部对接更合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2034:+1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2093:+### 3.5 学工部管理员信息
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2112:+| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2113:+| 学工部管理员信息 | 手动创建 | 合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2144:+| 学工部管理员 | 约 5 人 | 合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2162:+> 请教务系统、人事系统、学工部数据负责人、宿管系统方分别确认其可提供的数据范围、字段、对接方式和联系人。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2174:+7. 学工部终审人是固定个人、固定角色组、轮值还是人工分配？
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2192:+2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2195:+5. 学工部管理员：手动创建，同时配置默认终审人或终审组。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2227:+> 明确毕业离校系统所需的数据源，提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人反馈。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2237:+| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2297:+1. 将反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2326:+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2347:+| 学工部管理员信息 | P1 合理 | 人数少，手动创建比外部对接更合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2357:+1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2416:+### 3.5 学工部管理员信息
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2435:+| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2436:+| 学工部管理员信息 | 手动创建 | 合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2467:+| 学工部管理员 | 约 5 人 | 合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2485:+> 请教务系统、人事系统、学工部数据负责人、宿管系统方分别确认其可提供的数据范围、字段、对接方式和联系人。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2497:+7. 学工部终审人是固定个人、固定角色组、轮值还是人工分配？
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2515:+2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2518:+5. 学工部管理员：手动创建，同时配置默认终审人或终审组。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2550:+> 明确毕业离校系统所需的数据源，提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人反馈。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2560:+| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2620:+1. 将反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2653:1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2674:| 学工部管理员信息 | P1 合理 | 人数少，手动创建比外部对接更合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2684:1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2775:1. 将反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2804:+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2825:+| 学工部管理员信息 | P1 合理 | 人数少，手动创建比外部对接更合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2835:+1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2894:+### 3.5 学工部管理员信息
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2913:+| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2914:+| 学工部管理员信息 | 手动创建 | 合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2945:+| 学工部管理员 | 约 5 人 | 合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2963:+> 请教务系统、人事系统、学工部数据负责人、宿管系统方分别确认其可提供的数据范围、字段、对接方式和联系人。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2975:+7. 学工部终审人是固定个人、固定角色组、轮值还是人工分配？
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2993:+2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:2996:+5. 学工部管理员：手动创建，同时配置默认终审人或终审组。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3028:+> 明确毕业离校系统所需的数据源，提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人反馈。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3038:+| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3098:+1. 将反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3114:1. 反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3141:+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3162:+| 学工部管理员信息 | P1 合理 | 人数少，手动创建比外部对接更合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3172:+1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3231:+### 3.5 学工部管理员信息
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3250:+| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3251:+| 学工部管理员信息 | 手动创建 | 合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3282:+| 学工部管理员 | 约 5 人 | 合理。 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3300:+> 请教务系统、人事系统、学工部数据负责人、宿管系统方分别确认其可提供的数据范围、字段、对接方式和联系人。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3312:+7. 学工部终审人是固定个人、固定角色组、轮值还是人工分配？
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3330:+2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3333:+5. 学工部管理员：手动创建，同时配置默认终审人或终审组。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3365:+> 明确毕业离校系统所需的数据源，提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人反馈。
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3375:+| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md:3435:+1. 将反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-22-claude-post-execution-2026-06-01T14-27-35-376Z.md:275:**Claude签名**  
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-22-claude-post-execution-2026-06-01T14-27-35-376Z.md:1169:- 定义通知事件类型：申请提交、辅导员审批、学工部审批、驳回、附件上传。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-22-claude-post-execution-2026-06-01T14-27-35-376Z.md:1364:- 定义通知事件类型：申请提交、辅导员审批、学工部审批、驳回、附件上传
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-22-claude-post-execution-2026-06-01T14-27-35-376Z.md:1575:+- 学工部审批；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-22-claude-post-execution-2026-06-01T14-27-35-376Z.md:1768:+- 学工部审批；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-22-claude-post-execution-2026-06-01T14-27-35-376Z.md:1971:+- 学工部审批；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-22-claude-post-execution-2026-06-01T14-27-35-376Z.md:2187:+- 学工部审批；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-22-claude-post-execution-2026-06-01T14-27-35-376Z.md:2380:- 学工部审批；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-22-claude-post-execution-2026-06-01T14-27-35-376Z.md:2598:+- 学工部审批；
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-22-claude-post-execution-2026-06-01T14-27-35-376Z.md:2799:+- 学工部审批；
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:1080:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:1124:            approver_name='学工部',
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:1586:测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询 ... ok
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:1618:测试学工部驳回申请 ... ok
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:1933:  +    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:2061:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:2065:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:2095:            approver_name='学工部1',
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:2287:        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:2325:        # Step 5: 学工部登录
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:2332:        # Step 6: 学工部审批通过
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:2446:- ✓ 学工部: approver=user + step=dean + decision=pending
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:2451:- ✓ 学工部: 通过自己pending dean approvals反查
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:2498:- 权限: 学生403，辅导员/学工部只看自己pending
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:2819:    # 学工部: 只看自己的pending dean审批
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:2900:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:3003:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:3047:            approver_name='学工部',
.omc/artifacts/ask/codex-step-4-12-8-7-application-list-6-tests-1-student-2-student-3-2026-05-30T18-14-22-783Z.md:3285:   - 学工部仅看 `approver=user + step=dean + decision=pending`。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-48-37-499Z.md:144:- ✅ 申请提交流程（学生 → 辅导员 → 学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-48-37-499Z.md:145:- ✅ 两级审批流程（辅导员 → 学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-48-37-499Z.md:197:- 审批列表页（辅导员/学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-40-claude-post-phase2a-n-2026-06-01T16-48-37-499Z.md:1585:3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:33:**问题：** 风险2说"砍学工部审批"又说"Day 4补学工部审批"
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:37:降级方案：保留"提交→辅导员审批→查询"最短闭环，砍学工部审批，Day 4补学工部审批
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:42:降级方案：如Day 3结束申请提交API仍未完成或不稳定，则立即砍学工部审批，Day 4集中完成并验证"提交→辅导员审批→查询"闭环；学工部审批推到Week 2 Day 1
docs/discussions/codex-review-2026-05-30/53-p1-fixes-final-consensus.md:77:- 样例数据（10学生 + 2辅导员 + 1学工部 + 边界样本）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:27:2. API认证信息（appKey、appSecret、签名算法）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:139:        sign = self._generate_sign()
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:152:    def _generate_sign(self):
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:153:        # 实现签名算法（待API文档提供）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:260:- 方法签名是否合理？
backend/apps/applications/tests/test_detail_permissions.py:33:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
backend/apps/applications/tests/test_detail_permissions.py:37:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:1266:3. **终端备案：** 学工部管理科负责人终审
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:1413:   - 学生/辅导员/学工部用户管理
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:1428:   - 学工部备案操作
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:1526:- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:1540:    admin_id BIGINT COMMENT '学工部管理员ID',
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:2274:./docs/plans/week-0-1-execution-plan.md:36:- [ ] 生成seed数据（10学生 + 2辅导员 + 1学工部 + 边界样本 + 默认密码）
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:2669:- **学工部：** 1个
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:2716:### 3. 学工部账号（Dean）
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:2719:**用途：** 测试学工部审批
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:2729:- 学工部能审批所有通过辅导员审批的申请
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:2730:- 学工部不能直接审批pending_counselor状态的申请
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:2800:- [ ] 1个学工部账号创建成功
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:2808:- [ ] 学工部可以登录（D001/D001）
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:2848:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:3018:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:3194:### 5. 学工部能进行最终审批 ✓/✗
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:3198:**Step 1: 学工部登录**
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:3249:- [ ] 学工部能登录
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:3255:- 检查学工部权限配置
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:3405:- [ ] check_status方法签名
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:4033:+   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:4266:+   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:4552:   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:4785:+   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:5083:+   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:5331:+   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
.omc/artifacts/ask/codex-task-20260530-06-phase-3-independent-review-request-context--2026-05-30T10-02-12-891Z.md:5575:+   System design uses `admin` / 学工部管理员, code uses `dean`, Claude uses "dean". Day 0 must freeze terminology for Week 3.
docs/superpowers/plans/2026-05-27-implementation-plan.md:14:- 辅导员和学工部两级审批
docs/superpowers/plans/2026-05-27-implementation-plan.md:330:   - 学工部审批逻辑
docs/superpowers/plans/2026-05-27-implementation-plan.md:342:   - 学工部可以审批所有
docs/superpowers/plans/2026-05-27-implementation-plan.md:347:- ✓ 学工部审批通过后状态变更为approved
backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
backend/apps/applications/tests/test_list_permissions.py:74:            approver_name='学工部',
backend/apps/applications/tests/test_application_flow.py:50:        """测试完整的申请流程：登录→提交→辅导员审批→学工部审批→查询"""
backend/apps/applications/tests/test_application_flow.py:88:        # Step 5: 学工部登录
backend/apps/applications/tests/test_application_flow.py:95:        # Step 6: 学工部审批通过
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:131:- 学工部审批：辅导员通过后24小时内
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:137:- 学工部审批：辅导员通过后1个工作日内
docs/数据对接说明文档.md:106:- 从教务系统或学工系统导出当届毕业生数据
backend/apps/applications/views.py:25:    description='获取当前用户的申请列表（学生/辅导员/学工部）',
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:76:        help_text='学工部管理员ID'
backend/apps/applications/models.py:9:    PENDING_DEAN = 'pending_dean', '待学工部审批'
.omc/artifacts/ask/codex-final-wording-fixes-complete-and-pushed-phase-4a-prep-docs-f-2026-05-31T03-34-09-147Z.md:2090:backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-final-wording-fixes-complete-and-pushed-phase-4a-prep-docs-f-2026-05-31T03-34-09-147Z.md:2157:backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
docs/微信小程序备案说明.md:46:   - 法人签名章或法人手写正楷签名
docs/微信小程序备案说明.md:47:   - 接受签名章，不接受连笔签
docs/微信小程序备案说明.md:70:   - 法人签名章或法人手写正楷签名
docs/微信小程序备案说明.md:71:   - 接受签名章，不接受连笔签
docs/微信小程序备案说明.md:124:3. **授权书要求：** 必须盖学校公章，法人签名（接受签名章，不接受连笔签）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-19-claude-next-phase-str-2026-06-01T10-17-18-356Z.md:1391:- 定义通知事件类型：申请提交、辅导员审批、学工部审批、驳回、附件上传。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:1346:| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:1347:| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:1349:| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:1371:**触发条件：** 辅导员或学工部审批通过
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:1377:- 正文：`您的离校申请已通过{approver_role}审批。` （approver_role: 辅导员/学工部）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:1387:**触发条件：** 辅导员或学工部驳回申请
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:1419:**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:1421:**接收者：** 待审批的辅导员/学工部
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:1628:| 操作 | 学生 | 辅导员 | 学工部 | 说明 |
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:1712:**理由：** 未来可能需要通知多个接收者（如多个学工部账号）
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:1890:当前幂等检查只使用 `(entity_type, entity_id, type)`。这会把同一业务实体的同类通知限制为全局唯一，无法支持多个接收者。例如一个未来事件可能需要通知多个学工部账号，或者同一申请的不同待办人。即便 v0.1 当前多数事件只有单接收者，也不应把 schema 固化成全局唯一。
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:2439:backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:2440:backend/apps/approvals/tests/test_list_permissions.py:29:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:2546:backend/apps/applications/tests/test_detail_permissions.py:33:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:2547:backend/apps/applications/tests/test_detail_permissions.py:37:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:2549:backend/apps/users/migrations/0001_initial.py:25:                ('role', models.CharField(choices=[('student', '学生'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20)),
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:2555:backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:2716:backend/apps/approvals/views.py:115:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:2929:    DEAN = 'dean', '学工部'
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:3027:    # 学工部: 只看自己的dean审批
.omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-31-claude-post-contract--2026-06-01T15-47-30-046Z.md:3107:            return Response({'error': {'code': 'CONFLICT', 'message': '学工部审批已存在，不能重复创建'}},
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:11:完全接受Codex审查意见，并补充一个关键进展：**用户已提供官方签名算法**。
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:33:### P1：签名算法问题（已解决）
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:35:**Codex指出：** 签名算法缺失，不能靠猜测实现。
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:37:**Claude确认：** **问题已解决！用户在审查过程中提供了官方签名算法。**
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:39:**官方签名算法（已确认）：**
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:42:签名规则：
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:43:1. 将 appSecret, timestamp, randStr 三个参数值进行字典排序（sort）
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:48:appSecret: 6bd1b3fb015b4e72a85769e9d64405d1
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:50:randStr: Gc6LGToDKy2AMhXE
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:61:def generate_sign(app_secret: str, timestamp: str, rand_str: str, 
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:62:                  encryption_type: str = 'sha1') -> str:
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:64:    生成API签名
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:70:        encryption_type: 加密类型，'sha1'或'md5'，默认'sha1'
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:73:        签名字符串（十六进制小写）
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:83:    if encryption_type == 'md5':
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:104:3. 通过环境变量 `XG_USER_API_URL` 配置
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:117:1. 通过环境变量 `XG_USER_API_TENANT_CODE` 配置
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:132:1. 独立诊断脚本: `backend/scripts/xg_user_api_probe.py`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:133:2. 可Mock客户端: `backend/apps/users/integrations/xg_user_client.py`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:134:3. Mock单元测试: `backend/apps/users/tests/test_xg_user_client.py`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:135:4. 真实API测试通过 `XG_RUN_LIVE_API_TEST=1` 门禁
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:160:- AppId: ${XG_USER_API_APP_ID}
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:161:- AppKey: ${XG_USER_API_APP_KEY}
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:162:- AppSecret: ${XG_USER_API_APP_SECRET}
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:175:# 学工系统用户信息API配置
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:179:XG_USER_API_URL=https://xuegongmj.hgnu.edu.cn/api/open-api/user-center/tenant/auth-user-info
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:182:XG_USER_API_APP_ID=your_app_id_here
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:183:XG_USER_API_APP_KEY=your_app_key_here
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:184:XG_USER_API_APP_SECRET=your_app_secret_here
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:187:XG_USER_API_TENANT_CODE=your_tenant_code_here
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:190:XG_USER_API_ENCRYPTION_TYPE=sha1
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:193:XG_RUN_LIVE_API_TEST=0
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:230:1. 实现 `backend/apps/users/integrations/xg_user_client.py`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:231:   - 签名函数（已确认算法）
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:236:2. 实现 `backend/scripts/xg_user_api_probe.py`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:243:- 签名函数通过官方样例验证
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:252:1. 实现 `backend/apps/users/tests/test_xg_user_client.py`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:259:- 测试覆盖签名生成、请求构造、响应解析
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:269:2. 设置 `XG_RUN_LIVE_API_TEST=1`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:270:3. 运行 `xg_user_api_probe.py`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:297:2. ✅ 签名算法已确认（用户提供官方算法）
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:308:1. **签名算法已确认** - 不再是猜测，可以直接实现
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:320:3. 实现签名客户端和诊断脚本
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:327:**Claude签名：** 完全接受Codex审查意见，基于确认的签名算法开始实现。
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:250:**Claude签名：** 待Codex审查后达成共识
docs/discussions/phase4c-next-steps/23-codex-post-execution-next-steps-response.md:148:- 学工部审批；
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:83:契约允许辅导员和学工部审批通过都通知学生。现有唯一键使用 `entity_type=approval`、`entity_id=approval_id` 时，两个审批步骤会产生两条不同通知，这是合理的。实现文档应明确这一点，避免误以为“申请最终通过”才通知。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:121:4. 步骤语义：辅导员通过与学工部通过分别产生不同 `approval_id` 的通过通知。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:155:- 辅导员/学工部通过后创建 `APPROVAL_APPROVED` 给学生；
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:156:- 辅导员/学工部驳回后创建 `APPROVAL_REJECTED` 给学生；
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:175:3. 学工部通过后，学生收到一条 `APPROVAL_APPROVED` 通知，关联 dean approval。
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:28:### 问题2：签名算法验证
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:33:- `generate_sign()` 作为独立纯函数
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:44:- **Step 1A:** 签名与配置（立即执行）
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:80:- `.env.example` 保留 `XG_USER_API_APP_ID` 用于记录
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:111:### Step 1A：签名与配置（立即执行）
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:116:backend/apps/users/integrations/xg_user_client.py
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:117:backend/apps/users/tests/test_xg_user_client.py
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:121:- ✅ `generate_sign()` 实现正确
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:122:- ✅ 官方签名样例测试通过
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:124:- ✅ 非法encryptionType抛错
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:144:backend/scripts/xg_user_api_probe.py
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:157:2. ✅ 签名函数优先，官方样例P0测试
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:107:契约写“辅导员3工作日，学工部2工作日”。仓库依赖里已有 `chinese-calendar`，但这会引入节假日判断、调休解释和测试固定日期选择。若没有产品要求必须精确到中国法定节假日，v0.1 可以先改为自然日；若坚持工作日，则必须把算法和测试日期固定下来。
docs/数据确认清单.md:15:**问题2：** 如不包含,能否从教务/人事/学工系统归集后提供？
docs/discussions/phase4c-next-steps/22-claude-post-execution-next-steps.md:193:**Claude签名**  
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:11:**状态：** 达成共识，执行Step 1A（签名与配置切片）
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:24:- Step 1A: 签名与配置
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:39:### 3. 签名验证
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:42:- `generate_sign()` 纯函数
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:63:backend/apps/users/integrations/xg_user_client.py
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:64:backend/apps/users/tests/test_xg_user_client.py
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:69:- [ ] `generate_sign()` 实现
docs/design/2026-05-27-system-design.md:40:3. **终端备案：** 学工部管理科负责人终审
docs/design/2026-05-27-system-design.md:187:   - 学生/辅导员/学工部用户管理
docs/design/2026-05-27-system-design.md:202:   - 学工部备案操作
docs/design/2026-05-27-system-design.md:300:- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
docs/design/2026-05-27-system-design.md:314:    admin_id BIGINT COMMENT '学工部管理员ID',
docs/design/2026-05-27-system-design.md:355:- `pending_admin` - 待学工部备案
docs/design/2026-05-27-system-design.md:387:- `approver_role`: counselor（辅导员）、admin（学工部）
docs/design/2026-05-27-system-design.md:389:- `time_limit`: 辅导员1个工作日(24小时)，学工部1个工作日(24小时)
docs/design/2026-05-27-system-design.md:501:- `encryption_key` - 配置加密密钥（存储在环境变量，不在数据库）
docs/design/2026-05-27-system-design.md:599:  ├─N:1─→ users (学工部管理员)
docs/design/2026-05-27-system-design.md:627:2. 一个申请必须经过2级审批（辅导员→学工部）
docs/design/2026-05-27-system-design.md:1016:    "next_approver": "学工部",
docs/design/2026-05-27-system-design.md:1325:admin（学工部管理员）
docs/design/2026-05-27-system-design.md:1342:学工部审批         | ✗       | ✗         | ✓
docs/design/2026-05-27-system-design.md:1399:（待学工部备案）
docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
docs/design/2026-05-27-system-design.md:1427:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
docs/design/2026-05-27-system-design.md:1448:    - 通知学工部
docs/design/2026-05-27-system-design.md:1461:**节点3：学工部备案**
docs/design/2026-05-27-system-design.md:1463:- 权限要求：学工部管理员角色 + current_approver_id匹配
docs/design/2026-05-27-system-design.md:1473:    - 创建历史快照：applications_history（version=N, change_reason='学工部备案通过'）
docs/design/2026-05-27-system-design.md:1482:    - 创建历史快照：applications_history（version=N, change_reason='学工部驳回'）
docs/design/2026-05-27-system-design.md:1970:- JWT签名算法：HS256
docs/design/2026-05-27-system-design.md:2713:3. 学工部备案流程
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:47:3. 学工部通过后，学生收到一条`APPROVAL_APPROVED`通知，关联dean approval
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:113:approver_role = "辅导员" if approval.step == "counselor" else "学工部"
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:118:approver_role = "辅导员" if approval.step == "counselor" else "学工部"
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:12:1. **Step 1A实现审查**：审查签名生成函数实现质量
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:24:   - 导出 `generate_sign` 和 `XGUserAPIClient`
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:26:2. **backend/apps/users/integrations/xg_user_client.py**
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:27:   - `generate_sign()` 函数：支持SHA1/MD5签名生成
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:31:3. **backend/apps/users/tests/test_xg_user_client.py**
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:32:   - 官方签名样例测试（P0需求）
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:39:   - 包含租户Code S10405
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:40:   - 添加测试开关 `XG_RUN_LIVE_API_TEST`
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:59:- backend/apps/users/integrations/xg_user_client.py
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:60:- backend/apps/users/tests/test_xg_user_client.py
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:63:- 签名算法实现是否严格遵循官方规范？
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:71:- ✅ 官方签名样例验证
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:84:- ✅ **Step 1A（已完成）**：签名生成函数 + 单元测试
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:112:1. **风险优先**：租户Code S10405是新配置，需先验证网络连通性和API可达性
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:118:- 签名生成测试（使用真实配置）
docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:31:   - 权限测试 (学生/辅导员/学工部)
docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:78:   - list权限 (RBAC: 学生own/辅导员class/学工部dean)
docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:104:3. **RBAC复杂度:** 辅导员/学工部权限检查依赖approval scope，是否会导致N+1查询？
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:131:- 定义通知事件类型：申请提交、辅导员审批、学工部审批、驳回、附件上传。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:61:当前幂等检查只使用 `(entity_type, entity_id, type)`。这会把同一业务实体的同类通知限制为全局唯一，无法支持多个接收者。例如一个未来事件可能需要通知多个学工部账号，或者同一申请的不同待办人。即便 v0.1 当前多数事件只有单接收者，也不应把 schema 固化成全局唯一。
docs/discussions/phase4c-next-steps/24-claude-consensus-evidence-closure.md:61:7. 学工部审批（API调用示例）
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:11:设计并实现学工系统人员信息API的数据读取测试方案。
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:26:- AppId: ${XG_USER_API_APP_ID}
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:27:- AppKey: ${XG_USER_API_APP_KEY}
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:28:- AppSecret: ${XG_USER_API_APP_SECRET}
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:37:- `randStr`: 随机字符串（必填）
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:38:- `sign`: 认证签名（必填，算法未知）
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:39:- `encryptionType`: 加密类型，sha1或md5，默认sha1（可选）
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:66:### 1. 签名算法推断
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:68:文档中提到"请参见签名校验部分"但未给出具体算法。需要推断可能的签名算法：
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:71:- **A. HMAC-SHA1：** `sign = HMAC-SHA1(appSecret, appKey + timestamp + randStr)`
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:72:- **B. 拼接SHA1：** `sign = SHA1(appKey + timestamp + randStr + appSecret)`
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:73:- **C. 参数排序SHA1：** `sign = SHA1(sorted_params + appSecret)`
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:119:2. **认证测试：** 验证签名算法正确性（可能需要多次尝试）
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:126:7. 错误处理测试（无效签名、无效租户等）
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:157:- 签名错误（401/403）
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:171:1. **签名算法推断：**
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:172:   - 最可能的签名算法（基于常见开放平台实践）
backend/apps/users/tests/test_xg_user_client.py:1:"""学工系统用户API客户端测试"""
backend/apps/users/tests/test_xg_user_client.py:3:from apps.users.integrations.xg_user_client import generate_sign
backend/apps/users/tests/test_xg_user_client.py:7:    """签名生成函数测试"""
backend/apps/users/tests/test_xg_user_client.py:10:        """测试官方签名样例（sha1）"""
backend/apps/users/tests/test_xg_user_client.py:15:        sign = generate_sign(app_secret, timestamp, rand_str, 'sha1')
backend/apps/users/tests/test_xg_user_client.py:21:        sign = generate_sign(
backend/apps/users/tests/test_xg_user_client.py:28:    def test_md5_encryption(self):
backend/apps/users/tests/test_xg_user_client.py:30:        sign = generate_sign('secret', '1234567890', 'random', 'md5')
backend/apps/users/tests/test_xg_user_client.py:35:    def test_invalid_encryption_type(self):
backend/apps/users/tests/test_xg_user_client.py:38:            generate_sign('secret', '1234567890', 'random', 'sha256')
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:15:Step 0 安全修正已经完成，签名算法也已有官方样例，可以开始写代码；但 `tenantCode` 仍未确认，真实接口字段也未验证。因此下一步的最优路径不是等待，也不是直接接入业务 Provider，而是先交付一个可离线验证、可 mock 测试、可人工 live probe 的最小诊断层。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:20:2. **签名函数必须先用官方样例固化为单元测试。**
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:35:- `generate_sign()`、请求构造、响应解析、错误归一化、mock 测试可以立即做。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:36:- `xg_user_api_probe.py` 可以立即做，但缺少 `XG_USER_API_TENANT_CODE` 时只能执行配置校验、签名样例验证、`--dry-run` 请求摘要，不能发起网络请求。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:37:- live probe 必须等 `tenantCode` 到位，并且需要操作者显式确认，例如 `XG_RUN_LIVE_API_TEST=1`。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:41:### 问题2：签名算法是否需要单独验证模块？
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:43:**建议：选项 A，但把签名函数设计成独立纯函数，并把官方样例作为 P0 单元测试。**
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:45:不需要额外创建一次性签名验证脚本。更好的边界是：
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:48:backend/apps/users/integrations/xg_user_client.py
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:49:  - generate_sign(app_secret, timestamp, rand_str, encryption_type="sha1")
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:55:- `appSecret=6bd1b3fb015b4e72a85769e9d64405d1`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:57:- `randStr=Gc6LGToDKy2AMhXE`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:62:- 字典排序对象是三个**参数值**：`appSecret`、`timestamp`、`randStr`，不是参数名。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:65:- 不把 `tenantCode`、`appKey`、form-data 混入签名，除非后续官方文档另行确认。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:73:**B1：签名与配置切片**
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:76:- 实现 `generate_sign()`。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:78:- 单元测试覆盖官方签名样例、md5、非法 `encryptionType`、缺失必填环境变量。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:89:- `backend/scripts/xg_user_api_probe.py` 作为人工诊断入口。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:123:签名样例: OK
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:124:Live调用: skipped (missing tenantCode or XG_RUN_LIVE_API_TEST != 1)
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:125:请求摘要: POST /auth-user-info page=1 pageNum=1 encryptionType=sha1
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:138:JSON 输出不能包含 `appSecret`、完整 `sign`、完整手机号、身份证、微信 openId。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:146:`docs/api说明.txt` 的 header 参数是 `appKey`，没有 `appId`。`backend/.env.example` 已包含 `XG_USER_API_APP_ID`，可以保留用于记录平台凭证，但请求构造不要默认发送 `appId`。若平台部确认学校网关还要求 `appId`，再显式加入 header。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:185:### Step 1A：签名与配置，先做
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:190:- `backend/apps/users/integrations/xg_user_client.py`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:191:- `backend/apps/users/tests/test_xg_user_client.py`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:195:- 官方签名样例通过。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:196:- 缺失 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 时有明确错误。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:197:- `tenantCode` 缺失不影响签名样例测试。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:210:- header 包含 `appKey/timestamp/randStr/sign/encryptionType`。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:219:- `backend/scripts/xg_user_api_probe.py`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:226:- `XG_RUN_LIVE_API_TEST=1` 且配置齐全时才允许发请求。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:245:  generate_sign
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:247:  xg_user_api_probe.py
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:266:1. 先做 `generate_sign()` 和官方样例测试。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:215:3. 提交申请、辅导员通过、学工部通过、任一驳回均有focused测试或smoke覆盖。
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:24:- ✅ **签名算法已确认**（用户提供官方算法）
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:36:backend/apps/users/integrations/xg_user_client.py   # 客户端
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:37:backend/scripts/xg_user_api_probe.py                # 诊断脚本
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:38:backend/apps/users/tests/test_xg_user_client.py     # Mock测试
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:42:1. 签名函数（基于确认的官方算法）
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:77:### 问题2：签名算法是否需要单独验证模块？
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:79:**背景：** 用户提供的签名示例使用不同的AppSecret。
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:82:- appSecret: `6bd1b3fb015b4e72a85769e9d64405d1`
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:84:- randStr: `Gc6LGToDKy2AMhXE`
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:87:**选项A：** 客户端内置签名函数，测试时用官方样例验证
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:91:**选项B：** 先实现独立签名验证脚本，确认算法正确后再集成
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:104:1. 签名客户端（核心）
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:116:  - B1: 先只实现签名函数 + 官方样例验证
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:123:  - 只实现签名验证脚本
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:172:✓ 签名生成: baea...4515
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:87:- 学生审批通过通知：`type=approval_approved`、`entity_type=approval`、`message`包含`辅导员`或`学工部`。
docs/discussions/phase4c-next-steps/30-claude-consensus-contract-revision-gate.md:76:**理由：** 未来可能需要通知多个接收者（如多个学工部账号）
backend/apps/users/models.py:8:    DEAN = 'dean', '学工部'
backend/apps/users/integrations/__init__.py:1:"""学工系统API集成模块"""
backend/apps/users/integrations/__init__.py:2:from .xg_user_client import generate_sign, XGUserAPIClient
backend/apps/users/integrations/__init__.py:4:__all__ = ['generate_sign', 'XGUserAPIClient']
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:58:- ✅ 申请提交流程（学生 → 辅导员 → 学工部）
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:59:- ✅ 两级审批流程（辅导员 → 学工部）
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:111:- 审批列表页（辅导员/学工部）
docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:17:### 1. 签名算法已确认
docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:19:**Codex担心：** 签名算法缺失，不能靠猜测实现。
docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:21:**用户提供：** 官方签名算法（字典排序+拼接+sha1/md5）
docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:45:backend/scripts/xg_user_api_probe.py        # 诊断脚本
docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:46:backend/apps/users/integrations/xg_user_client.py   # 客户端
docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:47:backend/apps/users/tests/test_xg_user_client.py     # Mock测试
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:18:2. **P1：签名算法不能靠猜测进入正式实现；最多允许在一次性诊断脚本中按候选算法快速验证，正式代码必须等待平台部提供签名校验文档或可确认的样例。**
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:20:另外，`docs/api说明.txt` 的官方样式文档只给出 `sign`、`timestamp`、`randStr`、`encryptionType` 字段，但缺少“签名校验部分”；`tenantCode` 也只有示例值 `C10026`。因此第一阶段的目标应调整为“受控验证接口合同”，不是直接实现生产数据同步。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:34:- 将文档中的凭证替换为占位符，例如 `${XG_APP_KEY}`、`${XG_APP_SECRET}`。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:39:### P1：签名算法缺失，不能作为正式实现假设
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:45:当前文档明确写“请参见签名校验部分”，但仓库内文档没有该部分。候选算法 A/B/C 都只是合理猜测，不能作为生产实现依据。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:49:- 向平台部索要签名校验文档，至少需要：参与签名的字段、字段顺序、是否包含 form-data、secret位置、大小写、编码、输出hex/base64、时间戳单位、randStr长度、签名有效窗口。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:50:- 同时索要一个固定样例：固定 appKey、timestamp、randStr、tenantCode、appSecret 和期望 sign。没有固定样例时，算法验证成本会显著上升。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:77:- 从平台部或学工系统管理员处获取本校真实 `tenantCode`。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:90:- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:91:- 真实API测试必须通过显式开关启用，例如 `XG_RUN_LIVE_API_TEST=1`。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:97:### 1. 签名算法推断
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:99:在没有官方签名校验章节前，最可能的顺序建议如下：
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:101:1. **参数排序SHA1/MD5：** 将参与签名参数按key排序后拼接，再追加或混入 `appSecret`。很多开放平台采用这种方式，且文档提供 `encryptionType=sha1|md5` 更像普通摘要算法选择，而不是HMAC选择。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:102:2. **拼接SHA1/MD5：** `SHA1(appKey + timestamp + randStr + appSecret)` 或 `SHA1(appSecret + appKey + timestamp + randStr)`。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:103:3. **HMAC-SHA1：** 技术上更好，但如果文档只称 `encryptionType` 为 `sha1/md5`，而不是 `hmac-sha1`，优先级略低。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:119:backend/scripts/xg_user_api_probe.py
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:120:backend/apps/users/integrations/xg_user_client.py
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:121:backend/apps/users/tests/test_xg_user_client.py
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:126:- `xg_user_api_probe.py`：人工运行的诊断入口，读取环境变量，支持 `--algorithm`、`--page-size 1`、`--timeout`、`--dry-run`。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:127:- `xg_user_client.py`：可复用客户端，负责签名、请求构造、响应解析、错误归一化；后续可接入 `RealUserDataProvider`。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:128:- `test_xg_user_client.py`：mock HTTP响应，覆盖签名候选、字段解析、错误处理，不调用真实网络。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:137:2. 请求构造：header/form-data完整，timestamp/randStr/sign存在。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:138:3. 认证验证：用最小请求验证签名算法。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:147:- 错误签名压测。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:150:这些应等签名、租户、字段映射确认后再做。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:154:必须由平台部、学工系统管理员或接口开通记录提供真实 `tenantCode`。不要把文档样例 `C10026` 当成本校租户。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:170:XG_USER_API_URL
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:171:XG_USER_API_APP_KEY
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:172:XG_USER_API_APP_SECRET
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:173:XG_USER_API_TENANT_CODE
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:174:XG_USER_API_ENCRYPTION_TYPE=sha1
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:175:XG_RUN_LIVE_API_TEST=0
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:198:- `auth_failed`：HTTP 401/403 或业务错误提示签名失败，输出当前算法名和非敏感参数。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:203:不要对认证失败做大量重试。签名错误重试越多，越可能触发风控或污染审计。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:221:- 获得签名校验文档或固定签名样例。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:229:- `xg_user_client.py` 支持候选签名算法、请求构造、响应解析。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:230:- `xg_user_api_probe.py` 可通过环境变量运行，默认只请求 `page=1&pageNum=1`。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:245:- 仅在 `XG_RUN_LIVE_API_TEST=1` 时执行。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:264:- **实现可mock的客户端单元测试，覆盖签名候选和响应解析。**
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:266:- **签名和租户确认前，不启动生产数据读取实现。**
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:106:- 定义通知事件类型：申请提交、辅导员审批、学工部审批、驳回、附件上传
docs/discussions/phase4c-next-steps/05-claude-next-steps-strategy-request.md:40:- 申请详情页面：附件查看组件（辅导员/学工部查看附件）
docs/discussions/phase4c-next-steps/05-claude-next-steps-strategy-request.md:59:- 审批详情页面：辅导员/学工部审批操作
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:68:1. 通知事件枚举：申请提交、辅导员通过、学工部通过、审批驳回、宿舍清退阻断。
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:59:- 辅导员/学工部可根据backend RBAC查看/下载
backend/apps/notifications/services.py:54:    approver_role = "辅导员" if approval.step == "counselor" else "学工部"
backend/apps/users/integrations/xg_user_client.py:1:"""学工系统用户API客户端"""
backend/apps/users/integrations/xg_user_client.py:6:def generate_sign(
backend/apps/users/integrations/xg_user_client.py:10:    encryption_type: Literal['sha1', 'md5'] = 'sha1'
backend/apps/users/integrations/xg_user_client.py:13:    生成API签名
backend/apps/users/integrations/xg_user_client.py:15:    签名规则：
backend/apps/users/integrations/xg_user_client.py:16:    1. 将appSecret, timestamp, randStr三个参数值进行字典排序
backend/apps/users/integrations/xg_user_client.py:24:        encryption_type: 加密类型，'sha1'或'md5'，默认'sha1'
backend/apps/users/integrations/xg_user_client.py:27:        签名字符串（十六进制小写）
backend/apps/users/integrations/xg_user_client.py:29:    if encryption_type not in ('sha1', 'md5'):
backend/apps/users/integrations/xg_user_client.py:30:        raise ValueError(f"encryption_type must be 'sha1' or 'md5', got '{encryption_type}'")
backend/apps/users/integrations/xg_user_client.py:40:    if encryption_type == 'md5':
backend/apps/users/integrations/xg_user_client.py:47:    """学工系统用户API客户端（待实现）"""
backend/apps/users/migrations/0001_initial.py:25:                ('role', models.CharField(choices=[('student', '学生'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20)),
backend/apps/notifications/tests/test_timeout_warnings.py:29:            name='测试学工部',
backend/apps/notifications/tests/test_auto_notifications.py:134:        self.assertIn('学工部', notification.message)

codex
The prior Codex guidance already set a useful boundary: live calls stay gated, request construction is mockable, and probe output must redact secrets. I’m going to run the narrow test file now and collect line numbers for precise findings.
exec
/bin/bash -lc "rtk ls -la backend && rtk find backend -maxdepth 2 -type f \\( -name 'manage.py' -o -name 'pytest.ini' -o -name 'pyproject.toml' -o -name 'requirements*.txt' \\) -print" in /home/caohui/projects/graduation-leave-system
 exited 1 in 0ms:
.omc/
__pycache__/
apps/
config/
data/
docs/
media/
requirements/
utils/
.env  269B
.env.example  648B
Dockerfile  493B
app -> /app  4B
manage.py  666B
schema.py  739B
rtk: rtk find does not support compound predicates or actions (e.g. -not, -exec). Use `find` directly.

exec
/bin/bash -lc "rtk sed -n '1,280p' docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# API测试Step 0后下一步策略 - Codex审查响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**审查类型：** 执行策略  
**针对：** `76-claude-post-step0-next-strategy-request.md`  
**文档编号：** 77

---

## 审查结论

**结论：批准继续 Step 1，但需要把原计划改成“分步实现的诊断客户端”，而不是一次性完整封装。**

Step 0 安全修正已经完成，签名算法也已有官方样例，可以开始写代码；但 `tenantCode` 仍未确认，真实接口字段也未验证。因此下一步的最优路径不是等待，也不是直接接入业务 Provider，而是先交付一个可离线验证、可 mock 测试、可人工 live probe 的最小诊断层。

推荐决策：

1. **租户Code未拿到前不阻塞代码实现，但阻塞真实API调用。**
2. **签名函数必须先用官方样例固化为单元测试。**
3. **实现范围采用 B 分步方案，不采用一次性大包方案。**
4. **响应字段解析先宽松，业务映射决策延后。**
5. **诊断脚本默认文本输出，追加 `--format=json` 支持。**

---

## 对5个问题的明确建议

### 问题1：是否应该先获取租户Code？

**建议：选项 A + C 的组合。**

继续实现客户端代码和 mock 测试，`tenantCode` 使用环境变量占位；但真实API验证必须硬性等待平台部提供本校 `tenantCode`。也就是说：

- `generate_sign()`、请求构造、响应解析、错误归一化、mock 测试可以立即做。
- `xg_user_api_probe.py` 可以立即做，但缺少 `XG_USER_API_TENANT_CODE` 时只能执行配置校验、签名样例验证、`--dry-run` 请求摘要，不能发起网络请求。
- live probe 必须等 `tenantCode` 到位，并且需要操作者显式确认，例如 `XG_RUN_LIVE_API_TEST=1`。

不建议选项 B。等待租户Code会阻塞低风险、可离线验证的工作。

### 问题2：签名算法是否需要单独验证模块？

**建议：选项 A，但把签名函数设计成独立纯函数，并把官方样例作为 P0 单元测试。**

不需要额外创建一次性签名验证脚本。更好的边界是：

```text
backend/apps/users/integrations/xg_user_client.py
  - generate_sign(app_secret, timestamp, rand_str, encryption_type="sha1")
  - XGUserAPIClient
```

测试必须包含官方样例：

- `appSecret=6bd1b3fb015b4e72a85769e9d64405d1`
- `timestamp=1573702840`
- `randStr=Gc6LGToDKy2AMhXE`
- `sha1=baeaa6693fb7b9914c9ff9e388654878b8754515`

实现注意点：

- 字典排序对象是三个**参数值**：`appSecret`、`timestamp`、`randStr`，不是参数名。
- 默认 `sha1`，仅允许 `sha1` / `md5`，其他值直接抛配置错误。
- 输出小写 hex。
- 不把 `tenantCode`、`appKey`、form-data 混入签名，除非后续官方文档另行确认。

### 问题3：实现范围是否过大？

**建议：选项 B，分步实现。**

Claude 的原计划方向正确，但作为下一步一次性打包偏大。建议拆成三个可验收切片：

**B1：签名与配置切片**

- 新建 `backend/apps/users/integrations/` 包。
- 实现 `generate_sign()`。
- 实现配置读取/校验对象。
- 单元测试覆盖官方签名样例、md5、非法 `encryptionType`、缺失必填环境变量。

**B2：请求构造与响应解析切片**

- 实现 header/form-data 构造。
- 使用 `requests`，设置短超时，默认 `page=1&pageNum=1`。
- 解析 `code/msg/data/current_page/data/total/per_page`。
- 对成功响应、业务错误、schema 异常做 mock 测试。

**B3：诊断脚本与错误归一化切片**

- `backend/scripts/xg_user_api_probe.py` 作为人工诊断入口。
- 默认不进行 live call，必须环境变量或参数显式开启。
- 输出脱敏文本；需要自动化时支持 JSON。

这个拆法能在没有 `tenantCode` 的情况下完成 70%-80% 的确定性工作，同时把真实接口风险留在最后一个人工门。

### 问题4：是否需要先确认响应字段？

**建议：选项 A，但字段解析必须“宽松采样 + 不承诺业务可用”。**

API文档里的返回字段足以做诊断客户端，不足以证明它能替代当前 CSV/Mock 数据源。当前文档没有明确给出：

- 班级 `class_id`
- 辅导员映射
- 院系/专业标准字段
- 宿舍清退状态

因此客户端解析应分两层：

1. **接口结构层：** 严格校验 `code/msg/data/data/total` 这类协议字段。
2. **业务字段层：** 宽松采样，记录 `name/number/phone/identity_id/department/user_identity/user_auth_extra_field` 是否出现，不因业务字段缺失直接失败。

live probe 成功后，应输出“字段覆盖报告”，再决定是否接入 Provider。没有班级/辅导员/宿舍字段前，不应把该接口宣称为完整业务数据源。

### 问题5：诊断脚本的输出格式？

**建议：选项 C，但默认选项 A。**

默认人类可读文本最适合人工诊断；同时提供 `--format=json`，方便后续把结果贴入验收文档或自动化脚本。

默认文本建议包含：

```text
配置: OK
签名样例: OK
Live调用: skipped (missing tenantCode or XG_RUN_LIVE_API_TEST != 1)
请求摘要: POST /auth-user-info page=1 pageNum=1 encryptionType=sha1
```

live 成功时只输出摘要：

```text
HTTP状态: 200
业务码: 200
分页: current_page=1 per_page=1 total=4311
字段: name=yes number=yes phone=yes department=yes user_identity=yes
样本: name=张* number=17 phone=186****9896
```

JSON 输出不能包含 `appSecret`、完整 `sign`、完整手机号、身份证、微信 openId。

---

## 其他风险与遗漏

### P1：`AppId` 与接口文档字段可能不一致

`docs/api说明.txt` 的 header 参数是 `appKey`，没有 `appId`。`backend/.env.example` 已包含 `XG_USER_API_APP_ID`，可以保留用于记录平台凭证，但请求构造不要默认发送 `appId`。若平台部确认学校网关还要求 `appId`，再显式加入 header。

### P1：生产URL必须作为配置，不要写死

用户确认的学校域名可作为 `.env.example` 默认值，但客户端必须只从配置读取 URL。后续如果平台部要求改用 `saas.api.goliveplus.cn` 或测试环境，不能改代码。

### P1：真实调用要限制半径

第一次 live probe 固定：

- `page=1`
- `pageNum=1`
- 不带姓名、手机号、学号过滤
- 不做分页循环
- 不保存原始响应文件，除非已脱敏

### P2：测试不要新增第三方 mock 依赖

当前依赖已有 `requests`，测试可以直接用 `unittest.mock.patch` mock `requests.Session.post`。除非后续 HTTP 客户端测试明显膨胀，否则不必引入 `responses` 或 `requests-mock`。

### P2：错误分类要面向排障

建议定义少量稳定错误类型：

- `config_error`
- `sign_error`
- `network_error`
- `http_error`
- `auth_failed`
- `tenant_invalid`
- `business_error`
- `unexpected_schema`

诊断脚本输出错误类型和非敏感上下文即可，不打印完整 header。

---

## 推荐执行优先级

### Step 1A：签名与配置，先做

交付：

- `backend/apps/users/integrations/__init__.py`
- `backend/apps/users/integrations/xg_user_client.py`
- `backend/apps/users/tests/test_xg_user_client.py`

验收：

- 官方签名样例通过。
- 缺失 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 时有明确错误。
- `tenantCode` 缺失不影响签名样例测试。

### Step 1B：请求构造与解析，再做

交付：

- `XGUserAPIClient.build_headers()`
- `XGUserAPIClient.build_form_data()`
- `XGUserAPIClient.fetch_users_page()`
- 响应解析 DTO 或普通 dict 规范化函数

验收：

- header 包含 `appKey/timestamp/randStr/sign/encryptionType`。
- form-data 包含 `tenantCode/page/pageNum`。
- mock 成功响应能解析分页和人员列表。
- mock 错误响应能归一化为稳定错误类型。

### Step 1C：诊断脚本，最后做

交付：

- `backend/scripts/xg_user_api_probe.py`

验收：

- 默认不调用真实API。
- `--dry-run` 打印请求摘要。
- `--format=text|json` 均可用。
- `XG_RUN_LIVE_API_TEST=1` 且配置齐全时才允许发请求。

### Step 2：live probe，等租户Code

验收：

- 使用本校真实 `tenantCode`。
- 只请求一页一条。
- 产出脱敏字段覆盖报告。
- 根据字段覆盖再开“是否接入 Provider”的新决策门。

---

## 更优化的替代方案

推荐采用 **“诊断客户端先行，业务 Provider 后置”**：

```text
现在实现：
  generate_sign
  XGUserAPIClient
  xg_user_api_probe.py
  mock tests

暂不实现：
  RealUserDataProvider
  数据同步入库
  全量分页
  班级/辅导员自动映射
  宿舍清退状态接入
```

这样做的理由是：当前已知信息足够验证认证和接口结构，但不足以证明业务字段完整。把业务 Provider 后置，可以避免把一个“能读人员列表”的接口过早包装成“能支撑毕业离校业务”的数据源。

---

## 最终建议

Codex 建议 Claude 继续执行 Step 1，但按以下边界落地：

1. 先做 `generate_sign()` 和官方样例测试。
2. 再做请求构造、响应解析、mock 错误测试。
3. 最后做诊断脚本，默认 dry-run/text 输出，支持 JSON。
4. 没有本校 `tenantCode` 前，不做真实 API 请求。
5. live probe 只产出字段覆盖报告，不直接触发 Provider 接入。

**批准状态：** 可以开始 Step 1A / Step 1B；Step 1C 可实现但 live 调用必须等待 `tenantCode`。

exec
/bin/bash -lc "rtk sed -n '1,220p' backend/.env.example" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 学工系统用户信息API配置
# 联系平台部获取真实凭证后填入 .env 文件（不要提交.env）

# API地址（学校网关）
XG_USER_API_URL=https://xuegongmj.hgnu.edu.cn/api/open-api/user-center/tenant/auth-user-info

# API认证凭证（必填）
XG_USER_API_APP_ID=your_app_id_here
XG_USER_API_APP_KEY=your_app_key_here
XG_USER_API_APP_SECRET=your_app_secret_here

# 租户Code（必填）
# 本校租户Code: S10405
XG_USER_API_TENANT_CODE=S10405

# 加密类型（可选，默认sha1）
XG_USER_API_ENCRYPTION_TYPE=sha1

# 真实API测试开关（默认0=跳过，设置为1启用真实API调用）
XG_RUN_LIVE_API_TEST=0

exec
/bin/bash -lc 'rtk nl -ba backend/apps/users/tests/test_xg_user_client.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	"""学工系统用户API客户端测试"""
     2	from django.test import TestCase
     3	from apps.users.integrations.xg_user_client import generate_sign
     4	
     5	
     6	class GenerateSignTests(TestCase):
     7	    """签名生成函数测试"""
     8	
     9	    def test_official_sample_sha1(self):
    10	        """测试官方签名样例（sha1）"""
    11	        app_secret = '6bd1b3fb015b4e72a85769e9d64405d1'
    12	        timestamp = '1573702840'
    13	        rand_str = 'Gc6LGToDKy2AMhXE'
    14	
    15	        sign = generate_sign(app_secret, timestamp, rand_str, 'sha1')
    16	
    17	        self.assertEqual(sign, 'baeaa6693fb7b9914c9ff9e388654878b8754515')
    18	
    19	    def test_official_sample_default_sha1(self):
    20	        """测试官方样例（默认sha1）"""
    21	        sign = generate_sign(
    22	            '6bd1b3fb015b4e72a85769e9d64405d1',
    23	            '1573702840',
    24	            'Gc6LGToDKy2AMhXE'
    25	        )
    26	        self.assertEqual(sign, 'baeaa6693fb7b9914c9ff9e388654878b8754515')
    27	
    28	    def test_md5_encryption(self):
    29	        """测试md5加密"""
    30	        sign = generate_sign('secret', '1234567890', 'random', 'md5')
    31	        # 验证返回32位hex字符串
    32	        self.assertEqual(len(sign), 32)
    33	        self.assertTrue(all(c in '0123456789abcdef' for c in sign))
    34	
    35	    def test_invalid_encryption_type(self):
    36	        """测试非法加密类型"""
    37	        with self.assertRaises(ValueError) as cm:
    38	            generate_sign('secret', '1234567890', 'random', 'sha256')
    39	        self.assertIn("must be 'sha1' or 'md5'", str(cm.exception))

exec
/bin/bash -lc 'rtk nl -ba backend/apps/users/integrations/xg_user_client.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	"""学工系统用户API客户端"""
     2	import hashlib
     3	from typing import Literal
     4	
     5	
     6	def generate_sign(
     7	    app_secret: str,
     8	    timestamp: str,
     9	    rand_str: str,
    10	    encryption_type: Literal['sha1', 'md5'] = 'sha1'
    11	) -> str:
    12	    """
    13	    生成API签名
    14	
    15	    签名规则：
    16	    1. 将appSecret, timestamp, randStr三个参数值进行字典排序
    17	    2. 拼接成字符串
    18	    3. 进行sha1或md5加密
    19	
    20	    Args:
    21	        app_secret: AppSecret密钥
    22	        timestamp: Unix时间戳（字符串）
    23	        rand_str: 随机字符串
    24	        encryption_type: 加密类型，'sha1'或'md5'，默认'sha1'
    25	
    26	    Returns:
    27	        签名字符串（十六进制小写）
    28	    """
    29	    if encryption_type not in ('sha1', 'md5'):
    30	        raise ValueError(f"encryption_type must be 'sha1' or 'md5', got '{encryption_type}'")
    31	
    32	    # 1. 字典排序
    33	    params = [app_secret, timestamp, rand_str]
    34	    params.sort()
    35	
    36	    # 2. 拼接
    37	    sign_str = ''.join(params)
    38	
    39	    # 3. 加密
    40	    if encryption_type == 'md5':
    41	        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    42	    else:
    43	        return hashlib.sha1(sign_str.encode('utf-8')).hexdigest()
    44	
    45	
    46	class XGUserAPIClient:
    47	    """学工系统用户API客户端（待实现）"""
    48	    pass

codex
One checklist item exposed a minor tooling issue: `rtk find` rejected compound predicates, so I’ll avoid that pattern. I have enough file context; the remaining verification is the focused Django test command.
exec
/bin/bash -lc "rtk sed -n '1,220p' manage.py" in /home/caohui/projects/graduation-leave-system/backend
exec
/bin/bash -lc 'rtk ls requirements' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
base.txt  615B
dev.txt  232B
prod.txt  98B

exec
/bin/bash -lc 'rtk python -c "import django; print(django.get_version())"' in /home/caohui/projects/graduation-leave-system/backend
 exited 127 in 0ms:
[rtk: No such file or directory (os error 2)]

 succeeded in 104ms:
codex
Host Python is not exposed as `python` in this environment, so I’m switching to `python3` for the narrow test. If Django is not installed on the host, I’ll report that and rely on the existing documented 4/4 run rather than broadening scope.
exec
/bin/bash -lc 'rtk python3 manage.py test apps.users.tests.test_xg_user_client -v 2' in /home/caohui/projects/graduation-leave-system/backend
exec
/bin/bash -lc 'rtk python3 -c "import django; print(django.get_version())"' in /home/caohui/projects/graduation-leave-system/backend
 exited 1 in 231ms:
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/manage.py", line 11, in main
    from django.core.management import execute_from_command_line
ModuleNotFoundError: No module named 'django'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/manage.py", line 22, in <module>
    main()
    ~~~~^^
  File "/home/caohui/projects/graduation-leave-system/backend/manage.py", line 13, in main
    raise ImportError(
    ...<3 lines>...
    ) from exc
ImportError: Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?

 exited 1 in 238ms:
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import django; print(django.get_version())
    ^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'django'

codex
The focused test cannot run on the host because Django is not installed there. I’ll check whether the repo has an existing Docker test path before deciding whether to run it that way.
exec
/bin/bash -lc "rtk rg --files -g '*compose*' -g 'Dockerfile' -g 'Makefile'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/Dockerfile
docker-compose.yml

exec
/bin/bash -lc "rtk rg -n \"docker compose|compose|manage.py test|pytest|apps.users.tests\" README.md docs backend .omc/collaboration/artifacts -g '"'!*.jsonl'"'" in /home/caohui/projects/graduation-leave-system
 exited 2 in 0ms:
rg: README.md: No such file or directory (os error 2)
.omc/collaboration/artifacts/20260530-1005-claude-response-to-codex-phase3-review.md:15:1. Compose-first strategy is correct (verified: docker-compose.yml exists)
.omc/collaboration/artifacts/20260530-1005-claude-response-to-codex-phase3-review.md:29:$ ls -la docker-compose.yml backend/Dockerfile .env.docker
.omc/collaboration/artifacts/20260530-1005-claude-response-to-codex-phase3-review.md:30:docker-compose.yml  712B
.omc/collaboration/artifacts/20260530-1005-claude-response-to-codex-phase3-review.md:86:- `docker compose config` (Compose validity)
.omc/collaboration/artifacts/20260530-1005-claude-response-to-codex-phase3-review.md:100:- Product verification: separate commands (docker compose config, migrate, seed_data, API smoke)
.omc/collaboration/artifacts/20260530-1005-claude-response-to-codex-phase3-review.md:122:1. Verify Compose validity: `docker compose config`
.omc/collaboration/artifacts/20260530-1005-claude-response-to-codex-phase3-review.md:212:- Compose: `docker compose config`
.omc/collaboration/artifacts/20260530-1005-claude-response-to-codex-phase3-review.md:213:- Migration: `docker compose exec backend python manage.py showmigrations`
.omc/collaboration/artifacts/20260530-1005-claude-response-to-codex-phase3-review.md:214:- Seed: `docker compose exec backend python manage.py seed_data` (verify idempotent)
.omc/collaboration/artifacts/20260530-1008-codex-phase3-consensus.md:97:1. Run `docker compose config`.
.omc/collaboration/artifacts/20260530-1008-codex-phase3-consensus.md:100:4. Use full Compose as the Day 1 baseline because `docker-compose.yml`, `backend/Dockerfile`, and `.env.docker` already exist.
.omc/collaboration/artifacts/20260530-1008-codex-phase3-consensus.md:142:- `docker-compose.yml` and `.env.docker`
backend/requirements/dev.txt:4:pytest==8.1.1
backend/requirements/dev.txt:5:pytest-django==4.8.0
backend/requirements/dev.txt:6:pytest-cov==5.0.0
.omc/collaboration/artifacts/20260530-0959-codex-phase3-independent-review.md:37:- `docker-compose.yml`
.omc/collaboration/artifacts/20260530-0959-codex-phase3-independent-review.md:42:The current `docker-compose.yml` runs PostgreSQL 15 and maps backend `8001:8000`. Claude's proposal says to create Compose only if local Python dependencies are missing, and suggests a raw `postgres:14` container for Priority 2. That risks introducing a second, divergent environment path and port/version drift.
.omc/collaboration/artifacts/20260530-0959-codex-phase3-independent-review.md:53:- whether `docker compose config` succeeds
.omc/collaboration/artifacts/20260530-0959-codex-phase3-independent-review.md:109:The collaboration journal does not change merely because a product doc section was edited unless an event/state update happens. Running validation after every product substep can burn the Day 0 timebox and gives false confidence about product runtime correctness. Product runtime needs separate checks: `docker compose config`, `migrate`, `seed_data`, API login/submit/approve/query.
.omc/collaboration/artifacts/20260530-0959-codex-phase3-independent-review.md:121:1. Run `docker compose config`.
.omc/collaboration/artifacts/20260530-0959-codex-phase3-independent-review.md:204:2. **Update environment checks:** add `docker compose config`, `.env.docker` presence, `backend/manage.py check`, port `8001`, dependency file checks, and DB readiness checks.
.omc/collaboration/artifacts/20260530-2225-codex-day0-verification.md:36:- Existing test modules are stale against current routes. `python manage.py test apps.applications.tests.test_application_flow apps.applications.tests.test_error_cases apps.approvals.tests.test_rejection_flow` finds 8 tests but fails because tests call `/api/auth/login/` while the current route is `/api/auth/login`.
.omc/collaboration/artifacts/20260531-0325-step1-verification-results.md:106:docker compose exec backend python manage.py seed_data
.omc/collaboration/artifacts/20260531-0325-step1-verification-results.md:111:docker compose exec backend python manage.py seed_data --reset
.omc/collaboration/artifacts/phase4a-validation-checklist.md:29:docker compose exec backend python manage.py seed_data
.omc/collaboration/artifacts/phase4a-validation-checklist.md:34:docker compose exec backend python manage.py seed_data --reset
.omc/collaboration/artifacts/20260530-2251-codex-four-project-pattern-analysis.md:34:Dev Buddy is the most engineered system in the set. Its Ralph loop decomposes work into discovery, requirements/UAT, decomposition, plan linting, build, code review, and UAT. The important detail is not the exact stage list. The important detail is that state transitions, executor selection, retry handling, and mechanical failure context are file-backed and script-visible.
.omc/collaboration/artifacts/20260531-0415-codex-week3-execution-summary.md:37:- `docker compose exec backend python manage.py test apps.approvals.tests.test_permissions apps.approvals.tests.test_state_machine --keepdb`
.omc/collaboration/artifacts/20260531-0415-codex-week3-execution-summary.md:39:- `docker compose exec backend python manage.py test apps.approvals.tests.test_permissions apps.approvals.tests.test_state_machine apps.approvals.tests.test_rejection_flow apps.approvals.tests.test_list_permissions apps.applications.tests.test_application_flow apps.applications.tests.test_error_cases apps.applications.tests.test_list_permissions apps.applications.tests.test_p0_fixes apps.applications.tests.test_constraints --keepdb`
.omc/collaboration/artifacts/20260531-0415-codex-week3-execution-summary.md:41:- `docker compose exec backend python manage.py check`
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:112:docker exec backend python manage.py test apps.applications.tests.test_application_flow apps.applications.tests.test_error_cases apps.approvals.tests.test_rejection_flow --keepdb
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:74:docker exec graduation-leave-system-backend-1 python manage.py test \
.omc/collaboration/artifacts/20260530-1654-codex-github-projects-analysis.md:46:- **P1 借鉴：阶段化 gate**。Discovery、Requirements、Decompose 后设置用户/对方 agent checkpoint；我们不必全量照搬 Ralph，但可以给“需求/设计/实现/审查/验收”定义可选状态。
docs/acceptance/phase4c-demo-script.md:22:docker compose version
docs/acceptance/phase4c-demo-script.md:42:docker compose up -d
docs/acceptance/phase4c-demo-script.md:48:docker compose ps
docs/acceptance/phase4c-demo-script.md:59:docker compose exec backend python manage.py migrate
docs/acceptance/phase4c-demo-script.md:62:docker compose exec backend python manage.py showmigrations
docs/acceptance/phase4c-demo-script.md:73:docker compose exec backend python manage.py seed_data
docs/acceptance/phase4c-demo-script.md:76:docker compose exec backend python manage.py shell -c "
docs/acceptance/phase4c-demo-script.md:323:docker compose down
docs/acceptance/phase4c-demo-script.md:352:docker compose up -d
docs/acceptance/phase4c-demo-script.md:354:docker compose exec backend python manage.py migrate
docs/acceptance/phase4c-demo-script.md:355:docker compose exec backend python manage.py seed_data
docs/PROJECT-SUMMARY.md:349:- ✓ Docker配置：Dockerfile（Python 3.11）+ docker-compose.yml（PostgreSQL + Django）
docs/PROJECT-SUMMARY.md:774:- `docker compose exec backend python manage.py test apps.approvals.tests.test_permissions apps.approvals.tests.test_state_machine --keepdb`：10 tests OK
docs/PROJECT-SUMMARY.md:775:- `docker compose exec backend python manage.py test [explicit approvals/applications test modules] --keepdb`：37 tests OK
docs/PROJECT-SUMMARY.md:776:- `docker compose exec backend python manage.py check`：通过
docs/PROJECT-SUMMARY.md:1304:- backend/apps/users/tests/test_import_csv.py（9个测试）
docs/PROJECT-SUMMARY.md:1315:- ✓ 添加media_data volume到docker-compose.yml
docs/PROJECT-SUMMARY.md:1333:  2. 启动服务（docker compose up -d）
docs/PROJECT-SUMMARY.md:1357:- docker-compose.yml（添加media_data volume）
docs/PROJECT-SUMMARY.md:1428:  1. Docker启动（docker compose up -d）
docs/acceptance/phase4c-evidence-index.md:15:docker compose exec backend python manage.py test --keepdb
docs/acceptance/phase4c-evidence-index.md:18:docker compose exec backend python manage.py test apps.applications.tests --keepdb
docs/acceptance/phase4c-evidence-index.md:19:docker compose exec backend python manage.py test apps.approvals.tests --keepdb
docs/acceptance/phase4c-evidence-index.md:20:docker compose exec backend python manage.py test apps.attachments.tests --keepdb
docs/acceptance/phase4c-evidence-index.md:21:docker compose exec backend python manage.py test apps.users.tests --keepdb
docs/acceptance/phase4c-evidence-index.md:24:docker compose exec backend python manage.py test apps.users.tests.test_import_csv --keepdb
docs/acceptance/phase4c-evidence-index.md:56:| CSV导入测试 | 9个 | `backend/apps/users/tests/test_import_csv.py` |
docs/acceptance/phase4c-evidence-index.md:83:docker compose exec backend python manage.py import_csv \
docs/acceptance/phase4c-evidence-index.md:87:docker compose exec backend python manage.py import_csv \
docs/acceptance/phase4c-evidence-index.md:89:docker compose exec backend python manage.py import_csv \
docs/acceptance/phase4c-evidence-index.md:91:docker compose exec backend python manage.py import_csv \
docs/acceptance/phase4c-evidence-index.md:115:2. 启动服务：`docker compose up -d`
docs/acceptance/phase4c-evidence-index.md:116:3. 数据库迁移：`docker compose exec backend python manage.py migrate`
docs/acceptance/phase4c-evidence-index.md:117:4. 加载数据：`docker compose exec backend python manage.py seed_data`
docs/acceptance/phase4c-evidence-index.md:135:**路径：** `docker-compose.yml`
docs/acceptance/phase4c-acceptance-checklist.md:94:| **总计测试数** | ✅ 9/9 | `backend/apps/users/tests/test_import_csv.py` |
docs/acceptance/phase4c-acceptance-checklist.md:104:| PostgreSQL容器 | ✅ 通过 | `docker-compose.yml:db` |
docs/acceptance/phase4c-acceptance-checklist.md:105:| Backend容器 | ✅ 通过 | `docker-compose.yml:backend` |
docs/week3-day0-seed-data-requirements.md:117:docker compose exec backend python manage.py seed_data
docs/week3-day0-seed-data-requirements.md:128:1. 创建超级用户：`docker compose exec backend python manage.py createsuperuser`
docs/week3-day0-acceptance-checklist.md:15:docker compose exec backend python manage.py migrate
docs/week3-day0-acceptance-checklist.md:34:docker compose exec backend python manage.py seed_data
docs/week3-day0-environment-strategy.md:13:- docker compose 2.40.3: ✓
docs/week3-day0-environment-strategy.md:35:   - docker compose 2.40.3已安装
docs/week3-day0-environment-strategy.md:54:2. **docker-compose.yml**
docs/week3-day0-environment-strategy.md:69:docker compose build
docs/week3-day0-environment-strategy.md:72:docker compose up -d
docs/week3-day0-environment-strategy.md:75:docker compose exec backend python manage.py migrate
docs/week3-day0-environment-strategy.md:78:docker compose exec backend python manage.py seed_data
docs/week3-day0-environment-strategy.md:103:- **缓解：** docker-compose.yml配置depends_on，确保PostgreSQL先启动
.omc/collaboration/artifacts/20260530-1025-phase4-operator-checklist.md:25:- ✓ Environment strategy: Compose-first (docker-compose.yml exists)
docs/superpowers/plans/2026-05-27-implementation-plan.md:164:├── docker-compose.yml
docs/superpowers/plans/2026-05-27-implementation-plan.md:192:   - 编写docker-compose.yml
docs/superpowers/plans/2026-05-27-implementation-plan.md:204:   - 配置pytest
docs/superpowers/plans/2026-05-27-implementation-plan.md:210:- ✓ `docker-compose up` 成功启动所有服务
docs/superpowers/plans/2026-05-27-implementation-plan.md:591:   - 完善docker-compose.yml
.omc/collaboration/artifacts/20260530-0955-claude-phase3-initial-analysis.md:54:- Action: Create `docker-compose.yml` with app + db
docs/design/2026-05-27-system-design.md:1772:### 7.2 docker-compose.yml示例
docs/design/2026-05-27-system-design.md:2552:- pytest + pytest-django
docs/design/2026-05-27-system-design.md:2571:# pytest tests/test_application.py::test_application_submit_generates_number
docs/design/2026-05-27-system-design.md:2701:- pytest-mock（模拟外部系统）
docs/design/2026-05-27-system-design.md:2769:3. 运行 `docker-compose up -d`
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:210:- 不支持reset（手工docker compose down -v）
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:271:- docker compose up后可执行迁移和seed
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:132:docker exec backend python manage.py test apps.approvals.tests apps.applications.tests
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:74:1. docker-compose.yml暴露5432端口
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:155:1. docker-compose.yml不暴露5432
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:216:- Codex提到"修测试发现和测试数据，让`manage.py test`默认能发现并通过核心测试"
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:218:- 建议：Day 2至少修复测试发现问题，让`manage.py test`能找到测试
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:70:2. **High - T0校验命令应使用 `docker compose exec backend` 优先于裸 `docker exec backend`。**
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:71:   `docker-compose.yml` 定义的是 compose service `backend`，裸 `docker exec backend` 依赖容器名刚好叫 backend，不如 compose 命令稳定。文档12已有裸命令，可以执行中改成 compose 等价命令。
docs/discussions/week3-direction-2026-05-30/01-claude-proposal.md:97:2. 创建Docker Compose配置（docker-compose.yml）
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:153:# pytest.ini
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:154:[pytest]
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:188:    run: pytest tests/unit/
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:197:    run: pytest tests/integration/
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:238:- ✓ 测试框架选择合理（pytest）
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:151:docker exec backend python manage.py test --help
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:152:docker exec backend python manage.py test apps.users.tests.test_models -v 2
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:255:`.gitignore` 覆盖面合理，适合当前技术栈。尤其是 `.env`、`node_modules/`、`.pytest_cache/`、`staticfiles/`、`db.sqlite3` 等常见噪声和敏感文件都已排除。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:139:3. **host测试环境不可用。** 当前直接运行`python3 backend/manage.py test`失败：未安装Django。若验收依赖Docker，计划需明确Docker命令。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:156:- `docker compose up`后可执行迁移和seed。
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:71:1. docker-compose.yml不暴露5432
docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md:48:- `docker compose exec backend` vs `docker exec backend`
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:126:   - 将修改：MinIO仅作为未来扩展选项，不在基线compose中
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:133:- 完全重写docker-compose.yml（postgres、单实例django-app、redis、celery）
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:156:- pytest + pytest-django + factory_boy
docs/discussions/phase4c-next-steps/19-claude-next-phase-strategy-request.md:119:- D3: 部署脚本（Docker compose、环境配置、数据库初始化）
docs/discussions/phase4c-next-steps/19-claude-next-phase-strategy-request.md:179:2. 部署脚本（Docker compose、环境配置）
docs/discussions/phase4c-next-steps/19-claude-next-phase-strategy-request.md:200:2. 部署脚本优化（Docker compose、环境配置、数据库初始化）
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:33:- 移除docker-compose中的`deploy.replicas: 3`
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:64:backend/apps/users/tests/test_xg_user_client.py
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:29:python manage.py test apps.attachments.tests.test_upload apps.attachments.tests.test_list apps.attachments.tests.test_download apps.attachments.tests.test_delete -v 2
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:96:rtk docker compose exec -T backend python manage.py test apps.attachments.tests.test_list -v 2
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:102:rtk docker compose exec -T backend python manage.py test apps.attachments.tests.test_upload apps.attachments.tests.test_list apps.attachments.tests.test_download apps.attachments.tests.test_delete -v 2
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:110:rtk docker compose exec -T backend python manage.py test apps.attachments.tests -v 2
docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md:91:- 需要Celery beat配置（docker-compose服务、settings、broker）
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:79:1. **docker-compose.yml暴露宿主5432**：容易和本机PostgreSQL冲突
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:116:4. **修测试发现和测试数据**：让`manage.py test`默认能发现并通过核心测试
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:31:3. **backend/apps/users/tests/test_xg_user_client.py**
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:60:- backend/apps/users/tests/test_xg_user_client.py
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:57:docker compose exec -T backend python manage.py test \
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:117:backend/apps/users/tests/test_xg_user_client.py
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:30:docker compose exec backend python manage.py test apps.notifications.tests.test_auto_notifications apps.notifications.tests.test_auto_notifications_api
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:71:   在`tests/smoke_test.sh`头部和`DEPLOYMENT.md`说明：必须在`docker compose down -v`、`migrate`、`seed_data`之后运行。
docs/discussions/phase4c-next-steps/10-claude-response-to-codex-phase2-review.md:214:**验证：** 运行 `pytest backend/apps/attachments/tests/test_list.py -v`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:191:- `backend/apps/users/tests/test_xg_user_client.py`
docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:47:backend/apps/users/tests/test_xg_user_client.py     # Mock测试
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:147:docker compose exec -T backend python manage.py test \
docs/discussions/phase4c-next-steps/24-claude-consensus-evidence-closure.md:41:- 测试命令：`docker compose exec backend python manage.py test`
docs/discussions/phase4c-next-steps/24-claude-consensus-evidence-closure.md:55:1. Docker启动：`docker compose up -d`
docs/discussions/phase4c-next-steps/24-claude-consensus-evidence-closure.md:56:2. 数据库迁移：`docker compose exec backend python manage.py migrate`
docs/discussions/phase4c-next-steps/24-claude-consensus-evidence-closure.md:57:3. 加载数据：`docker compose exec backend python manage.py seed_data`
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:44:**Codex正确。** `docker-compose.yml:25-26`仅挂载`./backend:/app`，未为`MEDIA_ROOT`配置独立volume。Phase 4C附件功能在容器重启后会丢失文件，影响验收可信度。
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:90:- 明确`docker compose up`、`migrate`、`seed_data`、`import_csv`、smoke测试顺序
docs/discussions/week3-direction-2026-05-30/02-codex-review.md:42:- 一键启动脚本（docker-compose up）
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:253:**命令：** `docker compose exec -T backend python manage.py test apps.attachments.tests.test_list -v 2`
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:235:- 尝试运行通知测试：`python3 manage.py test apps.notifications...`，本地环境缺少Django依赖，未能执行。
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:65:docker-compose.yml中服务没有健康检查配置，容器启动不代表服务就绪。
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:220:# docker-compose.yml
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:13:但实际代码尚未开始：`backend/apps`、`backend/config/settings`、`backend/utils`、`frontend/mobile`、`frontend/miniprogram`、`docker/nginx`、`docker/scripts` 都是空目录；没有 `manage.py`、Django settings、模型、API、Dockerfile、`docker-compose.yml`、前端 `package.json` 或测试代码。因此当前不能构建、不能运行、不能测试。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:396:- `docker-compose.yml`
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:403:### 10.2 compose 示例路径不一致
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:405:设计文档中 compose 示例使用：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:426:compose 示例只有 `depends_on`，不能保证 Postgres/Redis 已可用。建议添加：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:440:- 使用 compose service 名称，而不是假设容器名 `postgres`
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:487:测试策略方向正确：pytest、PostgreSQL、TDD、覆盖率 80%+、并发测试、文件安全测试、限流测试、审计测试。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:491:- 没有 pytest 配置
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:493:- 没有 PostgreSQL 测试 compose
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:494:- dev requirements 缺少 `pytest-mock`、`bandit`、`pre-commit`、`locust` 等计划中提到或实际需要的工具
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:499:- `pytest.ini`
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:501:- Docker/compose test database
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:534:2. 创建 Dockerfile、docker-compose、nginx.conf、`.env.example`。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:535:3. 建立 pytest + PostgreSQL 测试基线。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:556:   - dev：pytest 工具、pre-commit、安全扫描、压测工具
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:559:4. 写 docker-compose 最小可运行环境：Django + Postgres + Redis。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:581:> 本地 Docker 可启动，Django 可访问，PostgreSQL/Redis 可连接，pytest 可运行。
docs/discussions/phase4c-next-steps/67-claude-response-accept-codex-fixes.md:29:- 命令：`rtk docker compose exec -T backend python manage.py makemigrations notifications`
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:90:- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:121:backend/apps/users/tests/test_xg_user_client.py
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:130:不建议把真实API调用写进Django常规测试套件。若确实需要live测试，使用 pytest marker 或环境变量硬门禁，并默认跳过。
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:163:**命令：** `docker compose exec -T backend python manage.py test apps.attachments.tests.test_list -v 2`
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:47:rtk docker compose exec -T backend python manage.py test \
docs/discussions/phase4c-next-steps/66-phase2b-option1-execution-codex-response.md:169:PYTHONPATH=. python backend/manage.py test apps.notifications.tests.test_auto_notifications apps.notifications.tests.test_auto_notifications_api --keepdb --noinput
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:102:- Docker 容器启动失败：查看 `docker compose ps`、`docker compose logs backend/db`。
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:48:Phase 2C不建议现在合并执行。当前 `requirements` 有Celery/Redis依赖，但项目设置和 `docker-compose.yml` 尚未配置Celery worker/beat。审批超时提醒还需要工作日算法、扫描窗口、重复提醒策略、幂等键和调度验收，这不是2B旁边的小补丁。
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:71:- 如果引入Celery beat，必须同时补配置、docker-compose服务、任务幂等测试和调度验收说明。
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:121:项目依赖中已有Celery/Redis，但settings和docker-compose尚未配置broker、worker、beat服务。直接实现定时提醒会把任务代码、运行方式和验收证据拆散。
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:135:- MinIO仅作为可选的未来存储模式，不是基线compose的一部分
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:134:3. Mock单元测试: `backend/apps/users/tests/test_xg_user_client.py`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:252:1. 实现 `backend/apps/users/tests/test_xg_user_client.py`
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:50:仓库已有 `docker-compose.yml` 和 `backend/Dockerfile`。当前Compose能启动PostgreSQL和Django开发服务，但仍缺少Phase 4C之后最关键的附件持久化闭环：
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:52:- `docker-compose.yml:25-26`只挂载了 `./backend:/app`，没有为 `MEDIA_ROOT` 配置独立volume。
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:106:- 明确 `docker compose up`、`migrate`、`seed_data`、`import_csv`、smoke测试顺序。
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:255:1. docker-compose.yml移除`deploy.replicas: 3`
docs/discussions/phase4c-next-steps/72-claude-codex-consensus-phase2b-step2-strategy.md:140:- Redis服务（docker-compose）
docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md:34:- `docker-compose.yml:3-34` 只有 `db` 和 `backend` 服务，没有 Redis、worker、beat。
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:92:  - `docker compose down -v`
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:93:  - `docker compose up -d --wait`
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:94:  - `docker compose exec backend python manage.py migrate`
docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:95:  - `docker compose exec backend python manage.py seed_data`
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:96:- 不在pytest测试套件中
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:38:backend/apps/users/tests/test_xg_user_client.py     # Mock测试

codex
The repo’s established verification path is Docker Compose. I’ll use the targeted `docker compose exec -T backend ...` form if the services are already running; otherwise I’ll avoid starting the stack just for a review unless needed.
exec
/bin/bash -lc "rtk sed -n '1,120p' docker-compose.yml" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: graduation_leave
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/app
      - media_data:/app/media
    ports:
      - "8001:8000"
    env_file:
      - .env.docker
    depends_on:
      db:
        condition: service_healthy

volumes:
  postgres_data:
  media_data:

exec
/bin/bash -lc 'rtk docker compose ps' in /home/caohui/projects/graduation-leave-system
 succeeded in 165ms:
[compose] 2 services:
  graduation-leave-system-backend-1 (graduation-leave-system-backend) Up 10 hours [8001, 8001]
  graduation-leave-system-db-1 (postgres:15-alpine) Up 10 hours (healthy) [5432, 5432]

codex
The backend and database containers are already up and healthy, so I’m running only the focused Step 1A test module in the container.
exec
/bin/bash -lc 'rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client -v 2' in /home/caohui/projects/graduation-leave-system
 exited 1 in 473ms:
Creating test database for alias 'default' ('test_graduation_leave')...
Found 4 test(s).
Type 'yes' if you would like to try deleting the test database 'test_graduation_leave', or 'no' to cancel: Got an error creating the test database: database "test_graduation_leave" already exists

Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 87, in _execute
    return self.cursor.execute(sql)
           ^^^^^^^^^^^^^^^^^^^^^^^^
psycopg2.errors.DuplicateDatabase: database "test_graduation_leave" already exists


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/creation.py", line 201, in _create_test_db
    self._execute_create_test_db(cursor, test_db_params, keepdb)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/postgresql/creation.py", line 46, in _execute_create_test_db
    super()._execute_create_test_db(cursor, parameters, keepdb)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/creation.py", line 187, in _execute_create_test_db
    cursor.execute("CREATE DATABASE %(dbname)s %(suffix)s" % parameters)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 67, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 80, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 87, in _execute
    return self.cursor.execute(sql)
           ^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: database "test_graduation_leave" already exists


During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/app/manage.py", line 22, in <module>
    main()
  File "/app/manage.py", line 18, in main
    execute_from_command_line(sys.argv)
  File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
    utility.execute()
  File "/usr/local/lib/python3.11/site-packages/django/core/management/__init__.py", line 436, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/usr/local/lib/python3.11/site-packages/django/core/management/commands/test.py", line 24, in run_from_argv
    super().run_from_argv(argv)
  File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 412, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/usr/local/lib/python3.11/site-packages/django/core/management/base.py", line 458, in execute
    output = self.handle(*args, **options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/core/management/commands/test.py", line 68, in handle
    failures = test_runner.run_tests(test_labels)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/test/runner.py", line 1054, in run_tests
    old_config = self.setup_databases(
                 ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/test/runner.py", line 950, in setup_databases
    return _setup_databases(
           ^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/django/test/utils.py", line 221, in setup_databases
    connection.creation.create_test_db(
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/creation.py", line 62, in create_test_db
    self._create_test_db(verbosity, autoclobber, keepdb)
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/base/creation.py", line 210, in _create_test_db
    confirm = input(
              ^^^^^^
EOFError: EOF when reading a line

codex
The first container test hit an existing test database and Django tried to prompt, which fails in noninteractive mode. I’m rerunning with `--keepdb --noinput`, matching the project’s existing pattern.
exec
/bin/bash -lc 'rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client -v 2 --keepdb --noinput' in /home/caohui/projects/graduation-leave-system
 succeeded in 679ms:
Using existing test database for alias 'default' ('test_graduation_leave')...
Found 4 test(s).
Operations to perform:
  Synchronize unmigrated apps: corsheaders, django_filters, drf_spectacular, messages, rest_framework, rest_framework_simplejwt, staticfiles
  Apply all migrations: admin, applications, approvals, attachments, auth, contenttypes, notifications, sessions, users
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  No migrations to apply.
System check identified no issues (0 silenced).
test_invalid_encryption_type (apps.users.tests.test_xg_user_client.GenerateSignTests.test_invalid_encryption_type)
测试非法加密类型 ... ok
test_md5_encryption (apps.users.tests.test_xg_user_client.GenerateSignTests.test_md5_encryption)
测试md5加密 ... ok
test_official_sample_default_sha1 (apps.users.tests.test_xg_user_client.GenerateSignTests.test_official_sample_default_sha1)
测试官方样例（默认sha1） ... ok
test_official_sample_sha1 (apps.users.tests.test_xg_user_client.GenerateSignTests.test_official_sample_sha1)
测试官方签名样例（sha1） ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.005s

OK
Preserving test database for alias 'default' ('test_graduation_leave')...

exec
/bin/bash -lc "rtk python3 - <<'PY'
import hashlib
print(hashlib.md5('1234567890randomsecret'.encode()).hexdigest())
print(hashlib.sha1('1234567890randomsecret'.encode()).hexdigest())
PY" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
2a471e23465cf11561ef7455fff00a86
a80f0218d36a2d363403cbb7eb0384d2aafe2b31

codex
I’ve finished the technical review and focused verification. I’m going to write the Codex response as the next numbered discussion document, then update the collaboration journal with a single review-response event.
apply patch
patch: completed
/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
diff --git a/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md b/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..05489a45877a612064fcbe7cacb8b5dd61370ea0
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
@@ -0,0 +1,162 @@
+# Step 1A完成审查与下一步策略 - Codex响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**审查类型：** 实现审查 + 策略建议  
+**针对：** `80-step1a-completion-next-review-request.md`  
+**文档编号：** 81
+
+---
+
+## 1. Step 1A审查结果
+
+**结论：Step 1A签名纯函数可以通过，但建议在进入真实诊断前补两个小修正。**
+
+已验证：
+
+- `backend/apps/users/integrations/xg_user_client.py` 的 `generate_sign()` 按三个参数值排序后拼接，再做 `sha1/md5` 小写 hex，符合当前官方样例约束。
+- 官方样例测试覆盖了显式 `sha1` 和默认 `sha1`。
+- 非法 `encryption_type` 会失败，不会静默降级。
+- 聚焦测试在 Docker 环境通过：`rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client -v 2 --keepdb --noinput`，4/4 passed。
+
+### P0问题
+
+无。
+
+当前代码没有发现会导致官方签名样例失败、密钥泄露或错误参与字段签名的 P0 问题。
+
+### P1问题
+
+1. **MD5测试断言过弱。**  
+   位置：`backend/apps/users/tests/test_xg_user_client.py:28`  
+   现在只检查长度和 hex 字符集，即使拼接顺序错误也可能通过。建议改成固定期望值，例如 `generate_sign('secret', '1234567890', 'random', 'md5')` 应等于 `2a471e23465cf11561ef7455fff00a86`。
+
+2. **Step 1A相对 doc 77 的“配置切片”尚未完成。**  
+   位置：`backend/apps/users/integrations/xg_user_client.py:46`  
+   当前只交付签名函数，`XGUserAPIClient` 仍是占位类，尚无配置读取/校验对象。若把 Step 1A 定义为“签名函数切片”，可以接受；若沿用 doc 77 验收标准，则还缺少 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 的明确错误测试。
+
+### P2问题
+
+1. **空字符串策略需要在边界上明确。**  
+   `generate_sign()` 作为纯函数可以允许空字符串，但请求构建/配置层必须拒绝空 `appSecret/timestamp/randStr`。建议不要在签名函数里混入环境语义，在 Step 1B 的 config/header 构造处校验。
+
+2. **特殊字符与 Unicode 不需要作为 P0，但可补一个文档化测试。**  
+   当前实现使用 UTF-8 编码，行为确定。实际 header 中的 `randStr` 应限制为 ASCII 随机串；如果平台文档没有要求 Unicode，测试不必扩大为必选项。
+
+3. **大小写/空白归一化应放在配置层。**  
+   `generate_sign()` 严格接受 `sha1/md5` 是合理的；环境变量读取时可以对 `XG_USER_API_ENCRYPTION_TYPE` 做 `strip().lower()`，再传入纯函数。
+
+### 安全评价
+
+- 当前签名函数不会记录或返回密钥，仅返回摘要，安全面较小。
+- `md5` 只因官方接口兼容而保留，不应作为默认值。
+- 后续诊断脚本不得打印完整 `appSecret`、完整 `sign`、手机号、身份证号、openId 或完整原始响应。
+
+---
+
+## 2. 下一步策略建议
+
+**建议选择“修正后的选项A”：先做 Step 1B-lite，再做 Step 1C。**
+
+不建议纯选项B先写诊断脚本。诊断脚本也必须构造 headers/form-data、生成 timestamp/randStr/sign、处理超时和脱敏输出；如果没有可复用客户端层，脚本会复制 Step 1B 逻辑，后续再迁回客户端时容易产生签名字段、日志脱敏、错误分类不一致。
+
+推荐顺序：
+
+1. **立即补 Step 1A 小修正。**  
+   固定 MD5 期望值；如坚持 doc 77 的 Step 1A 验收，再补配置校验对象与缺失配置测试。
+
+2. **执行 Step 1B-lite。**  
+   只实现配置读取、headers 构造、form-data 构造、单页请求、基础响应解析和 mock 测试。不做分页循环、不做重试、不接入业务 Provider。
+
+3. **随后执行 Step 1C。**  
+   诊断脚本调用 Step 1B-lite 的客户端能力，默认 dry-run；只有 `XG_RUN_LIVE_API_TEST=1` 且配置齐全时做一次 `page=1/pageNum=1` live probe。
+
+这样仍然能快速验证网络/API可达性，但不会牺牲可测试性和脱敏一致性。
+
+---
+
+## 3. Step 1C范围确认
+
+Step 1C范围基本合理，但需要改成“安全诊断入口”，不是完整请求/响应日志收集器。
+
+### 必须包含
+
+- 环境变量读取与校验：URL、appKey、appSecret、tenantCode、encryptionType、live开关。
+- 官方签名样例自检。
+- 默认 dry-run，请求摘要不发网络请求。
+- live probe 硬门禁：`XG_RUN_LIVE_API_TEST=1`，配置齐全，固定 `page=1/pageNum=1`。
+- 输出格式：默认 text，支持 `--format=json`。
+- 超时参数：默认短超时，例如 5 秒，可用 `--timeout` 调整。
+- 错误分类：`config_error`、`sign_error`、`network_error`、`http_error`、`auth_failed`、`tenant_invalid`、`business_error`、`unexpected_schema`。
+- 脱敏输出：只显示 header/form-data 的非敏感摘要；响应 body 只允许脱敏预览。
+
+### 应删除或限制
+
+- 不记录完整请求 headers，因为其中包含完整 `sign`。
+- 不保存完整响应 body，除非先脱敏并明确标注。
+- 不做分页循环、批量读取、落库、字段映射结论。
+- 不在常规 Django/pytest 测试套件里触发 live API。
+
+### 建议输出
+
+文本输出保持短摘要：
+
+```text
+配置: OK
+签名样例: OK
+Live调用: skipped (XG_RUN_LIVE_API_TEST != 1)
+请求摘要: POST auth-user-info page=1 pageNum=1 encryptionType=sha1 sign=present
+```
+
+live 成功时输出：
+
+```text
+HTTP状态: 200
+业务码: 200
+分页: current_page=1 per_page=1 total=...
+字段覆盖: name=yes number=yes phone=yes department=yes user_identity=yes
+样本: name=张* number=17**** phone=186****9896
+```
+
+---
+
+## 4. Step 1B范围界定
+
+### 应包含
+
+- `XGUserAPIConfig` 或等价配置对象：从环境读取、校验必填项、归一化 encryptionType。
+- `XGUserAPIClient.build_headers()`：
+  - 包含 `appKey/timestamp/randStr/sign/encryptionType`。
+  - 默认不发送 `appId`，除非平台部确认接口要求。
+  - timestamp/randStr 可注入或可 patch，方便确定性测试。
+- `XGUserAPIClient.build_form_data()`：
+  - 包含 `tenantCode/page/pageNum`。
+  - 默认 `page=1/pageNum=1`。
+- `XGUserAPIClient.fetch_users_page()`：
+  - 使用短超时。
+  - 支持注入 session，便于 mock `post`。
+  - 只请求单页。
+- 响应解析：
+  - 协议层解析 `code/msg/data/current_page/data/total/per_page`。
+  - 人员字段先宽松采样，不做业务字段强承诺。
+- Mock测试：
+  - header字段完整、签名确定性。
+  - form-data字段完整。
+  - 成功响应解析分页和人员列表。
+  - HTTP错误、网络异常、业务错误、schema异常。
+  - 缺失配置和非法 encryptionType。
+
+### 应排除
+
+- 全量分页循环。
+- 重试机制，尤其是认证失败重试。
+- Provider接入、数据库写入、CSV替换。
+- 班级/辅导员/宿舍字段业务映射。
+- 真实API测试进入 CI 或常规测试。
+- 完整原始响应日志。
+
+---
+
+## 最终建议
+
+Step 1A可以作为“签名函数切片”通过；进入下一步前建议补 MD5 固定值测试。下一步不要先写孤立诊断脚本，而是先做一个很窄的 Step 1B-lite，让 Step 1C 复用同一套请求构造、签名和脱敏逻辑。真实 live probe 仍必须保持单页一条、显式开关、脱敏输出。

diff --git a/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md b/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..05489a45877a612064fcbe7cacb8b5dd61370ea0
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
@@ -0,0 +1,162 @@
+# Step 1A完成审查与下一步策略 - Codex响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**审查类型：** 实现审查 + 策略建议  
+**针对：** `80-step1a-completion-next-review-request.md`  
+**文档编号：** 81
+
+---
+
+## 1. Step 1A审查结果
+
+**结论：Step 1A签名纯函数可以通过，但建议在进入真实诊断前补两个小修正。**
+
+已验证：
+
+- `backend/apps/users/integrations/xg_user_client.py` 的 `generate_sign()` 按三个参数值排序后拼接，再做 `sha1/md5` 小写 hex，符合当前官方样例约束。
+- 官方样例测试覆盖了显式 `sha1` 和默认 `sha1`。
+- 非法 `encryption_type` 会失败，不会静默降级。
+- 聚焦测试在 Docker 环境通过：`rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client -v 2 --keepdb --noinput`，4/4 passed。
+
+### P0问题
+
+无。
+
+当前代码没有发现会导致官方签名样例失败、密钥泄露或错误参与字段签名的 P0 问题。
+
+### P1问题
+
+1. **MD5测试断言过弱。**  
+   位置：`backend/apps/users/tests/test_xg_user_client.py:28`  
+   现在只检查长度和 hex 字符集，即使拼接顺序错误也可能通过。建议改成固定期望值，例如 `generate_sign('secret', '1234567890', 'random', 'md5')` 应等于 `2a471e23465cf11561ef7455fff00a86`。
+
+2. **Step 1A相对 doc 77 的“配置切片”尚未完成。**  
+   位置：`backend/apps/users/integrations/xg_user_client.py:46`  
+   当前只交付签名函数，`XGUserAPIClient` 仍是占位类，尚无配置读取/校验对象。若把 Step 1A 定义为“签名函数切片”，可以接受；若沿用 doc 77 验收标准，则还缺少 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 的明确错误测试。
+
+### P2问题
+
+1. **空字符串策略需要在边界上明确。**  
+   `generate_sign()` 作为纯函数可以允许空字符串，但请求构建/配置层必须拒绝空 `appSecret/timestamp/randStr`。建议不要在签名函数里混入环境语义，在 Step 1B 的 config/header 构造处校验。
+
+2. **特殊字符与 Unicode 不需要作为 P0，但可补一个文档化测试。**  
+   当前实现使用 UTF-8 编码，行为确定。实际 header 中的 `randStr` 应限制为 ASCII 随机串；如果平台文档没有要求 Unicode，测试不必扩大为必选项。
+
+3. **大小写/空白归一化应放在配置层。**  
+   `generate_sign()` 严格接受 `sha1/md5` 是合理的；环境变量读取时可以对 `XG_USER_API_ENCRYPTION_TYPE` 做 `strip().lower()`，再传入纯函数。
+
+### 安全评价
+
+- 当前签名函数不会记录或返回密钥，仅返回摘要，安全面较小。
+- `md5` 只因官方接口兼容而保留，不应作为默认值。
+- 后续诊断脚本不得打印完整 `appSecret`、完整 `sign`、手机号、身份证号、openId 或完整原始响应。
+
+---
+
+## 2. 下一步策略建议
+
+**建议选择“修正后的选项A”：先做 Step 1B-lite，再做 Step 1C。**
+
+不建议纯选项B先写诊断脚本。诊断脚本也必须构造 headers/form-data、生成 timestamp/randStr/sign、处理超时和脱敏输出；如果没有可复用客户端层，脚本会复制 Step 1B 逻辑，后续再迁回客户端时容易产生签名字段、日志脱敏、错误分类不一致。
+
+推荐顺序：
+
+1. **立即补 Step 1A 小修正。**  
+   固定 MD5 期望值；如坚持 doc 77 的 Step 1A 验收，再补配置校验对象与缺失配置测试。
+
+2. **执行 Step 1B-lite。**  
+   只实现配置读取、headers 构造、form-data 构造、单页请求、基础响应解析和 mock 测试。不做分页循环、不做重试、不接入业务 Provider。
+
+3. **随后执行 Step 1C。**  
+   诊断脚本调用 Step 1B-lite 的客户端能力，默认 dry-run；只有 `XG_RUN_LIVE_API_TEST=1` 且配置齐全时做一次 `page=1/pageNum=1` live probe。
+
+这样仍然能快速验证网络/API可达性，但不会牺牲可测试性和脱敏一致性。
+
+---
+
+## 3. Step 1C范围确认
+
+Step 1C范围基本合理，但需要改成“安全诊断入口”，不是完整请求/响应日志收集器。
+
+### 必须包含
+
+- 环境变量读取与校验：URL、appKey、appSecret、tenantCode、encryptionType、live开关。
+- 官方签名样例自检。
+- 默认 dry-run，请求摘要不发网络请求。
+- live probe 硬门禁：`XG_RUN_LIVE_API_TEST=1`，配置齐全，固定 `page=1/pageNum=1`。
+- 输出格式：默认 text，支持 `--format=json`。
+- 超时参数：默认短超时，例如 5 秒，可用 `--timeout` 调整。
+- 错误分类：`config_error`、`sign_error`、`network_error`、`http_error`、`auth_failed`、`tenant_invalid`、`business_error`、`unexpected_schema`。
+- 脱敏输出：只显示 header/form-data 的非敏感摘要；响应 body 只允许脱敏预览。
+
+### 应删除或限制
+
+- 不记录完整请求 headers，因为其中包含完整 `sign`。
+- 不保存完整响应 body，除非先脱敏并明确标注。
+- 不做分页循环、批量读取、落库、字段映射结论。
+- 不在常规 Django/pytest 测试套件里触发 live API。
+
+### 建议输出
+
+文本输出保持短摘要：
+
+```text
+配置: OK
+签名样例: OK
+Live调用: skipped (XG_RUN_LIVE_API_TEST != 1)
+请求摘要: POST auth-user-info page=1 pageNum=1 encryptionType=sha1 sign=present
+```
+
+live 成功时输出：
+
+```text
+HTTP状态: 200
+业务码: 200
+分页: current_page=1 per_page=1 total=...
+字段覆盖: name=yes number=yes phone=yes department=yes user_identity=yes
+样本: name=张* number=17**** phone=186****9896
+```
+
+---
+
+## 4. Step 1B范围界定
+
+### 应包含
+
+- `XGUserAPIConfig` 或等价配置对象：从环境读取、校验必填项、归一化 encryptionType。
+- `XGUserAPIClient.build_headers()`：
+  - 包含 `appKey/timestamp/randStr/sign/encryptionType`。
+  - 默认不发送 `appId`，除非平台部确认接口要求。
+  - timestamp/randStr 可注入或可 patch，方便确定性测试。
+- `XGUserAPIClient.build_form_data()`：
+  - 包含 `tenantCode/page/pageNum`。
+  - 默认 `page=1/pageNum=1`。
+- `XGUserAPIClient.fetch_users_page()`：
+  - 使用短超时。
+  - 支持注入 session，便于 mock `post`。
+  - 只请求单页。
+- 响应解析：
+  - 协议层解析 `code/msg/data/current_page/data/total/per_page`。
+  - 人员字段先宽松采样，不做业务字段强承诺。
+- Mock测试：
+  - header字段完整、签名确定性。
+  - form-data字段完整。
+  - 成功响应解析分页和人员列表。
+  - HTTP错误、网络异常、业务错误、schema异常。
+  - 缺失配置和非法 encryptionType。
+
+### 应排除
+
+- 全量分页循环。
+- 重试机制，尤其是认证失败重试。
+- Provider接入、数据库写入、CSV替换。
+- 班级/辅导员/宿舍字段业务映射。
+- 真实API测试进入 CI 或常规测试。
+- 完整原始响应日志。
+
+---
+
+## 最终建议
+
+Step 1A可以作为“签名函数切片”通过；进入下一步前建议补 MD5 固定值测试。下一步不要先写孤立诊断脚本，而是先做一个很窄的 Step 1B-lite，让 Step 1C 复用同一套请求构造、签名和脱敏逻辑。真实 live probe 仍必须保持单页一条、显式开关、脱敏输出。

codex
The review document is written at `docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md`. I’m checking the collaboration lock area before appending the review event and updating state.
exec
/bin/bash -lc 'rtk ls -la .omc/collaboration/locks' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
(empty)

exec
/bin/bash -lc 'rtk tail -n 8 .omc/collaboration/events.jsonl' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{"id":92,"type":"review_response","agent":"codex","timestamp":"2026-06-01T16:48:22.187390Z","summary":"Codex reviewed Claude post-Phase2A Track 3 strategy and recommended Phase 2A stabilization plus Option E-lite, deferring Phase 2B/2C.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md"],"status":"waiting_for_claude_response","details":{"decision":"phase2a_stabilization_then_option_e_lite","defer":["phase2b_dorm_clearance_blocked_notification","phase2c_approval_timeout_reminders"],"required_first":["fix_notification_type_enum_drift","add_focused_api_notification_tests"]}}
{"id":93,"type":"review_response","agent":"codex","timestamp":"2026-06-01T17:11:07.123675Z","summary":"Codex reviewed Claude post-Phase2A stabilization Option E-lite strategy and approved execution with smoke repeatability and schema-scope constraints.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md"],"status":"waiting_for_claude_response","details":{"decision":"approve_with_constraints","required_adjustments":["move smoke precondition/reset strategy before smoke assertions","scope OpenAPI baseline to accessible schema, endpoint inventory, auth visibility, and known gaps","avoid unconditional destructive database reset","handle notification entity_id semantics before asserting in smoke"],"verification":"12 notification stabilization tests passed in Docker"}}
{"id":94,"type":"review_response","agent":"codex","timestamp":"2026-06-01T18:13:33.127210Z","summary":"Codex reviewed Claude post Option E-lite next strategy and supported B-mini plus corrected API Schema P1 work.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md"],"status":"waiting_for_claude_response","details":{"decision":"support_option_a_with_required_modifications","recommended_order":["smoke_typo_cleanup","api_schema_p1_corrected"],"adjusted_estimate":"3-4h","key_risks":["login_schema_mismatch","error_envelope_accuracy","multi_method_schema","notification_pagination_shape","attachment_module_ownership"]}}
{"id":95,"type":"review_response","agent":"codex","timestamp":"2026-06-01T18:16:41Z","summary":"Codex confirmed Claude Option A corrected response and authorized B-mini followed by API Schema P1 corrected execution.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/53-codex-confirmation-option-a-corrected.md"],"status":"waiting_for_claude_execution","details":{"decision":"confirmed","authorized_order":["smoke_typo_cleanup","api_schema_p1_corrected"],"clarification":"method-scoped extend_schema is mandatory for multi-method dispatchers; single-method function views need explicit accurate schema metadata and operationIds."}}
{"id":96,"type":"review_response","agent":"codex","timestamp":"2026-06-01T19:09:59.246622Z","summary":"Codex reviewed final Option 2 consensus and approved a narrowed A-lite path with schema-status correction first.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md"],"status":"waiting_for_claude_response","details":{"decision":"approve_option_2_with_modified_a_lite","required_first":["fix_api_schema_todo_status_to_code_complete_unaccepted","resolve_dorm_blocked_notification_contract_entity"],"defer":["phase2c_celery_beat_until_separate_decision"]}}
{"id":97,"type":"review_response","agent":"codex","timestamp":"2026-06-02T02:43:24.553780875Z","summary":"Codex reviewed Claude post Phase 2B Step 1 strategy and recommended B-mini followed by a management-command timeout warning implementation, deferring Celery beat.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/70-codex-post-phase2b-step1-next-strategy-response.md"],"status":"waiting_for_claude_response","details":{"decision":"recommend_b_mini_then_degraded_option_a","recommended_next":["decision_gate_for_timeout_warning_scope","management_command_plus_service_tests"],"defer":["celery_beat","redis_worker_services","repeat_reminders"]}}
{"id":98,"type":"review_response","agent":"codex","timestamp":"2026-06-02T02:59:39.675315935Z","summary":"Codex reviewed the API data reading test plan and required credential redaction/rotation plus official signing and tenant confirmation before live production testing.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md"],"status":"waiting_for_claude_response","details":{"decision":"needs_modification_before_live_api_test","required_first":["redact_and_rotate_exposed_credentials","obtain_official_signing_algorithm_and_tenant_code"],"recommended_scope":"diagnostic_client_plus_mock_tests_no_ci_live_calls"}}
{"id":99,"type":"review_response","agent":"codex","timestamp":"2026-06-02T03:08:57.327738096Z","summary":"Codex reviewed Claude post-Step 0 API test strategy and approved phased diagnostic-client implementation while keeping live calls gated on tenantCode.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md"],"status":"waiting_for_claude_response","details":{"decision":"approve_phased_diagnostic_client","recommended_order":["signature_and_config_tests","request_parse_mock_tests","diagnostic_probe","live_probe_after_tenant_code"],"live_gate":"XG_RUN_LIVE_API_TEST=1 plus confirmed tenantCode"}}

diff --git a/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md b/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..05489a45877a612064fcbe7cacb8b5dd61370ea0
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
@@ -0,0 +1,162 @@
+# Step 1A完成审查与下一步策略 - Codex响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**审查类型：** 实现审查 + 策略建议  
+**针对：** `80-step1a-completion-next-review-request.md`  
+**文档编号：** 81
+
+---
+
+## 1. Step 1A审查结果
+
+**结论：Step 1A签名纯函数可以通过，但建议在进入真实诊断前补两个小修正。**
+
+已验证：
+
+- `backend/apps/users/integrations/xg_user_client.py` 的 `generate_sign()` 按三个参数值排序后拼接，再做 `sha1/md5` 小写 hex，符合当前官方样例约束。
+- 官方样例测试覆盖了显式 `sha1` 和默认 `sha1`。
+- 非法 `encryption_type` 会失败，不会静默降级。
+- 聚焦测试在 Docker 环境通过：`rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client -v 2 --keepdb --noinput`，4/4 passed。
+
+### P0问题
+
+无。
+
+当前代码没有发现会导致官方签名样例失败、密钥泄露或错误参与字段签名的 P0 问题。
+
+### P1问题
+
+1. **MD5测试断言过弱。**  
+   位置：`backend/apps/users/tests/test_xg_user_client.py:28`  
+   现在只检查长度和 hex 字符集，即使拼接顺序错误也可能通过。建议改成固定期望值，例如 `generate_sign('secret', '1234567890', 'random', 'md5')` 应等于 `2a471e23465cf11561ef7455fff00a86`。
+
+2. **Step 1A相对 doc 77 的“配置切片”尚未完成。**  
+   位置：`backend/apps/users/integrations/xg_user_client.py:46`  
+   当前只交付签名函数，`XGUserAPIClient` 仍是占位类，尚无配置读取/校验对象。若把 Step 1A 定义为“签名函数切片”，可以接受；若沿用 doc 77 验收标准，则还缺少 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 的明确错误测试。
+
+### P2问题
+
+1. **空字符串策略需要在边界上明确。**  
+   `generate_sign()` 作为纯函数可以允许空字符串，但请求构建/配置层必须拒绝空 `appSecret/timestamp/randStr`。建议不要在签名函数里混入环境语义，在 Step 1B 的 config/header 构造处校验。
+
+2. **特殊字符与 Unicode 不需要作为 P0，但可补一个文档化测试。**  
+   当前实现使用 UTF-8 编码，行为确定。实际 header 中的 `randStr` 应限制为 ASCII 随机串；如果平台文档没有要求 Unicode，测试不必扩大为必选项。
+
+3. **大小写/空白归一化应放在配置层。**  
+   `generate_sign()` 严格接受 `sha1/md5` 是合理的；环境变量读取时可以对 `XG_USER_API_ENCRYPTION_TYPE` 做 `strip().lower()`，再传入纯函数。
+
+### 安全评价
+
+- 当前签名函数不会记录或返回密钥，仅返回摘要，安全面较小。
+- `md5` 只因官方接口兼容而保留，不应作为默认值。
+- 后续诊断脚本不得打印完整 `appSecret`、完整 `sign`、手机号、身份证号、openId 或完整原始响应。
+
+---
+
+## 2. 下一步策略建议
+
+**建议选择“修正后的选项A”：先做 Step 1B-lite，再做 Step 1C。**
+
+不建议纯选项B先写诊断脚本。诊断脚本也必须构造 headers/form-data、生成 timestamp/randStr/sign、处理超时和脱敏输出；如果没有可复用客户端层，脚本会复制 Step 1B 逻辑，后续再迁回客户端时容易产生签名字段、日志脱敏、错误分类不一致。
+
+推荐顺序：
+
+1. **立即补 Step 1A 小修正。**  
+   固定 MD5 期望值；如坚持 doc 77 的 Step 1A 验收，再补配置校验对象与缺失配置测试。
+
+2. **执行 Step 1B-lite。**  
+   只实现配置读取、headers 构造、form-data 构造、单页请求、基础响应解析和 mock 测试。不做分页循环、不做重试、不接入业务 Provider。
+
+3. **随后执行 Step 1C。**  
+   诊断脚本调用 Step 1B-lite 的客户端能力，默认 dry-run；只有 `XG_RUN_LIVE_API_TEST=1` 且配置齐全时做一次 `page=1/pageNum=1` live probe。
+
+这样仍然能快速验证网络/API可达性，但不会牺牲可测试性和脱敏一致性。
+
+---
+
+## 3. Step 1C范围确认
+
+Step 1C范围基本合理，但需要改成“安全诊断入口”，不是完整请求/响应日志收集器。
+
+### 必须包含
+
+- 环境变量读取与校验：URL、appKey、appSecret、tenantCode、encryptionType、live开关。
+- 官方签名样例自检。
+- 默认 dry-run，请求摘要不发网络请求。
+- live probe 硬门禁：`XG_RUN_LIVE_API_TEST=1`，配置齐全，固定 `page=1/pageNum=1`。
+- 输出格式：默认 text，支持 `--format=json`。
+- 超时参数：默认短超时，例如 5 秒，可用 `--timeout` 调整。
+- 错误分类：`config_error`、`sign_error`、`network_error`、`http_error`、`auth_failed`、`tenant_invalid`、`business_error`、`unexpected_schema`。
+- 脱敏输出：只显示 header/form-data 的非敏感摘要；响应 body 只允许脱敏预览。
+
+### 应删除或限制
+
+- 不记录完整请求 headers，因为其中包含完整 `sign`。
+- 不保存完整响应 body，除非先脱敏并明确标注。
+- 不做分页循环、批量读取、落库、字段映射结论。
+- 不在常规 Django/pytest 测试套件里触发 live API。
+
+### 建议输出
+
+文本输出保持短摘要：
+
+```text
+配置: OK
+签名样例: OK
+Live调用: skipped (XG_RUN_LIVE_API_TEST != 1)
+请求摘要: POST auth-user-info page=1 pageNum=1 encryptionType=sha1 sign=present
+```
+
+live 成功时输出：
+
+```text
+HTTP状态: 200
+业务码: 200
+分页: current_page=1 per_page=1 total=...
+字段覆盖: name=yes number=yes phone=yes department=yes user_identity=yes
+样本: name=张* number=17**** phone=186****9896
+```
+
+---
+
+## 4. Step 1B范围界定
+
+### 应包含
+
+- `XGUserAPIConfig` 或等价配置对象：从环境读取、校验必填项、归一化 encryptionType。
+- `XGUserAPIClient.build_headers()`：
+  - 包含 `appKey/timestamp/randStr/sign/encryptionType`。
+  - 默认不发送 `appId`，除非平台部确认接口要求。
+  - timestamp/randStr 可注入或可 patch，方便确定性测试。
+- `XGUserAPIClient.build_form_data()`：
+  - 包含 `tenantCode/page/pageNum`。
+  - 默认 `page=1/pageNum=1`。
+- `XGUserAPIClient.fetch_users_page()`：
+  - 使用短超时。
+  - 支持注入 session，便于 mock `post`。
+  - 只请求单页。
+- 响应解析：
+  - 协议层解析 `code/msg/data/current_page/data/total/per_page`。
+  - 人员字段先宽松采样，不做业务字段强承诺。
+- Mock测试：
+  - header字段完整、签名确定性。
+  - form-data字段完整。
+  - 成功响应解析分页和人员列表。
+  - HTTP错误、网络异常、业务错误、schema异常。
+  - 缺失配置和非法 encryptionType。
+
+### 应排除
+
+- 全量分页循环。
+- 重试机制，尤其是认证失败重试。
+- Provider接入、数据库写入、CSV替换。
+- 班级/辅导员/宿舍字段业务映射。
+- 真实API测试进入 CI 或常规测试。
+- 完整原始响应日志。
+
+---
+
+## 最终建议
+
+Step 1A可以作为“签名函数切片”通过；进入下一步前建议补 MD5 固定值测试。下一步不要先写孤立诊断脚本，而是先做一个很窄的 Step 1B-lite，让 Step 1C 复用同一套请求构造、签名和脱敏逻辑。真实 live probe 仍必须保持单页一条、显式开关、脱敏输出。

codex
The lock directory is clear and the last event is 99. I’m appending event 100 under the required journal lock and keeping the workflow state pointed back to Claude for response.
exec
/bin/bash -lc "rtk bash -lc '
set -euo pipefail
lock=.omc/collaboration/locks/journal.lock
mkdir \""'$lock"
cleanup() { rm -rf "$lock"; }
trap cleanup EXIT
now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
printf "{'"\\\"agent\\\":\\\"codex\\\",\\\"task_id\\\":\\\"phase4c_next_steps\\\",\\\"created_at\\\":\\\"%s\\\",\\\"heartbeat_at\\\":\\\"%s\\\",\\\"reason\\\":\\\"append Step 1A review response event and update state\\\"}\\n\" \""'$now" "$now" > "$lock/owner.json"
python3 - <<PY
import json
from pathlib import Path
from datetime import datetime, timezone

events_path = Path(".omc/collaboration/events.jsonl")
state_path = Path(".omc/collaboration/state.json")
ids = []
with events_path.open("r", encoding="utf-8") as f:
    for line_no, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Malformed JSONL line {line_no}: {exc}")
        event_id = event.get("id", event.get("event_id"))
        if isinstance(event_id, int):
            ids.append(event_id)
if len(ids) != len(set(ids)):
    seen = set()
    dupes = []
    for event_id in ids:
        if event_id in seen and event_id not in dupes:
            dupes.append(event_id)
        seen.add(event_id)
    raise SystemExit(f"Duplicate event ids: {dupes}")
next_id = max(ids, default=0) + 1
now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
event = {
    "id": next_id,
    "type": "review_response",
    "agent": "codex",
    "timestamp": now,
    "summary": "Codex reviewed Step 1A signature implementation and recommended Step 1B-lite before diagnostic script.",
    "task_id": "phase4c_next_steps",
    "artifacts": ["docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md"],
    "status": "waiting_for_claude_response",
    "details": {
        "decision": "step1a_passes_signature_slice_with_p1_test_improvement",
        "recommended_next": ["fix_md5_expected_value_test", "step1b_lite_request_build_mock_tests", "step1c_probe_reusing_client"],
        "verification": "4/4 xg_user_client tests passed in Docker with --keepdb --noinput"
    }
}
with events_path.open("a", encoding="utf-8") as f:
    f.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "'"\\n\")
state = json.loads(state_path.read_text(encoding=\"utf-8\"))
state.update({
    \"current_task\": \"phase4c_next_steps\",
    \"active_agent\": \"claude\",
    \"status\": \"waiting_for_claude_response\",
    \"last_event_id\": next_id,
    \"updated_at\": now,
})
tmp_path = state_path.with_name(state_path.name + \".tmp.codex\")
tmp_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + \"\\n\", encoding=\"utf-8\")
json.loads(tmp_path.read_text(encoding=\"utf-8\"))
tmp_path.replace(state_path)
print(f\"appended event {next_id}\")
PY
python3 - <<PY
import json
from pathlib import Path
for path in [Path(\".omc/collaboration/events.jsonl\"), Path(\".omc/collaboration/state.json\")]:
    if path.name.endswith(\"jsonl\"):
        for line_no, line in enumerate(path.read_text(encoding=\"utf-8\").splitlines(), 1):
            if line.strip():
                json.loads(line)
    else:
        json.loads(path.read_text(encoding=\"utf-8\"))
print(\"collaboration files valid\")
PY
'" in /home/caohui/projects/graduation-leave-system
diff --git a/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md b/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..05489a45877a612064fcbe7cacb8b5dd61370ea0
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
@@ -0,0 +1,162 @@
+# Step 1A完成审查与下一步策略 - Codex响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**审查类型：** 实现审查 + 策略建议  
+**针对：** `80-step1a-completion-next-review-request.md`  
+**文档编号：** 81
+
+---
+
+## 1. Step 1A审查结果
+
+**结论：Step 1A签名纯函数可以通过，但建议在进入真实诊断前补两个小修正。**
+
+已验证：
+
+- `backend/apps/users/integrations/xg_user_client.py` 的 `generate_sign()` 按三个参数值排序后拼接，再做 `sha1/md5` 小写 hex，符合当前官方样例约束。
+- 官方样例测试覆盖了显式 `sha1` 和默认 `sha1`。
+- 非法 `encryption_type` 会失败，不会静默降级。
+- 聚焦测试在 Docker 环境通过：`rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client -v 2 --keepdb --noinput`，4/4 passed。
+
+### P0问题
+
+无。
+
+当前代码没有发现会导致官方签名样例失败、密钥泄露或错误参与字段签名的 P0 问题。
+
+### P1问题
+
+1. **MD5测试断言过弱。**  
+   位置：`backend/apps/users/tests/test_xg_user_client.py:28`  
+   现在只检查长度和 hex 字符集，即使拼接顺序错误也可能通过。建议改成固定期望值，例如 `generate_sign('secret', '1234567890', 'random', 'md5')` 应等于 `2a471e23465cf11561ef7455fff00a86`。
+
+2. **Step 1A相对 doc 77 的“配置切片”尚未完成。**  
+   位置：`backend/apps/users/integrations/xg_user_client.py:46`  
+   当前只交付签名函数，`XGUserAPIClient` 仍是占位类，尚无配置读取/校验对象。若把 Step 1A 定义为“签名函数切片”，可以接受；若沿用 doc 77 验收标准，则还缺少 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 的明确错误测试。
+
+### P2问题
+
+1. **空字符串策略需要在边界上明确。**  
+   `generate_sign()` 作为纯函数可以允许空字符串，但请求构建/配置层必须拒绝空 `appSecret/timestamp/randStr`。建议不要在签名函数里混入环境语义，在 Step 1B 的 config/header 构造处校验。
+
+2. **特殊字符与 Unicode 不需要作为 P0，但可补一个文档化测试。**  
+   当前实现使用 UTF-8 编码，行为确定。实际 header 中的 `randStr` 应限制为 ASCII 随机串；如果平台文档没有要求 Unicode，测试不必扩大为必选项。
+
+3. **大小写/空白归一化应放在配置层。**  
+   `generate_sign()` 严格接受 `sha1/md5` 是合理的；环境变量读取时可以对 `XG_USER_API_ENCRYPTION_TYPE` 做 `strip().lower()`，再传入纯函数。
+
+### 安全评价
+
+- 当前签名函数不会记录或返回密钥，仅返回摘要，安全面较小。
+- `md5` 只因官方接口兼容而保留，不应作为默认值。
+- 后续诊断脚本不得打印完整 `appSecret`、完整 `sign`、手机号、身份证号、openId 或完整原始响应。
+
+---
+
+## 2. 下一步策略建议
+
+**建议选择“修正后的选项A”：先做 Step 1B-lite，再做 Step 1C。**
+
+不建议纯选项B先写诊断脚本。诊断脚本也必须构造 headers/form-data、生成 timestamp/randStr/sign、处理超时和脱敏输出；如果没有可复用客户端层，脚本会复制 Step 1B 逻辑，后续再迁回客户端时容易产生签名字段、日志脱敏、错误分类不一致。
+
+推荐顺序：
+
+1. **立即补 Step 1A 小修正。**  
+   固定 MD5 期望值；如坚持 doc 77 的 Step 1A 验收，再补配置校验对象与缺失配置测试。
+
+2. **执行 Step 1B-lite。**  
+   只实现配置读取、headers 构造、form-data 构造、单页请求、基础响应解析和 mock 测试。不做分页循环、不做重试、不接入业务 Provider。
+
+3. **随后执行 Step 1C。**  
+   诊断脚本调用 Step 1B-lite 的客户端能力，默认 dry-run；只有 `XG_RUN_LIVE_API_TEST=1` 且配置齐全时做一次 `page=1/pageNum=1` live probe。
+
+这样仍然能快速验证网络/API可达性，但不会牺牲可测试性和脱敏一致性。
+
+---
+
+## 3. Step 1C范围确认
+
+Step 1C范围基本合理，但需要改成“安全诊断入口”，不是完整请求/响应日志收集器。
+
+### 必须包含
+
+- 环境变量读取与校验：URL、appKey、appSecret、tenantCode、encryptionType、live开关。
+- 官方签名样例自检。
+- 默认 dry-run，请求摘要不发网络请求。
+- live probe 硬门禁：`XG_RUN_LIVE_API_TEST=1`，配置齐全，固定 `page=1/pageNum=1`。
+- 输出格式：默认 text，支持 `--format=json`。
+- 超时参数：默认短超时，例如 5 秒，可用 `--timeout` 调整。
+- 错误分类：`config_error`、`sign_error`、`network_error`、`http_error`、`auth_failed`、`tenant_invalid`、`business_error`、`unexpected_schema`。
+- 脱敏输出：只显示 header/form-data 的非敏感摘要；响应 body 只允许脱敏预览。
+
+### 应删除或限制
+
+- 不记录完整请求 headers，因为其中包含完整 `sign`。
+- 不保存完整响应 body，除非先脱敏并明确标注。
+- 不做分页循环、批量读取、落库、字段映射结论。
+- 不在常规 Django/pytest 测试套件里触发 live API。
+
+### 建议输出
+
+文本输出保持短摘要：
+
+```text
+配置: OK
+签名样例: OK
+Live调用: skipped (XG_RUN_LIVE_API_TEST != 1)
+请求摘要: POST auth-user-info page=1 pageNum=1 encryptionType=sha1 sign=present
+```
+
+live 成功时输出：
+
+```text
+HTTP状态: 200
+业务码: 200
+分页: current_page=1 per_page=1 total=...
+字段覆盖: name=yes number=yes phone=yes department=yes user_identity=yes
+样本: name=张* number=17**** phone=186****9896
+```
+
+---
+
+## 4. Step 1B范围界定
+
+### 应包含
+
+- `XGUserAPIConfig` 或等价配置对象：从环境读取、校验必填项、归一化 encryptionType。
+- `XGUserAPIClient.build_headers()`：
+  - 包含 `appKey/timestamp/randStr/sign/encryptionType`。
+  - 默认不发送 `appId`，除非平台部确认接口要求。
+  - timestamp/randStr 可注入或可 patch，方便确定性测试。
+- `XGUserAPIClient.build_form_data()`：
+  - 包含 `tenantCode/page/pageNum`。
+  - 默认 `page=1/pageNum=1`。
+- `XGUserAPIClient.fetch_users_page()`：
+  - 使用短超时。
+  - 支持注入 session，便于 mock `post`。
+  - 只请求单页。
+- 响应解析：
+  - 协议层解析 `code/msg/data/current_page/data/total/per_page`。
+  - 人员字段先宽松采样，不做业务字段强承诺。
+- Mock测试：
+  - header字段完整、签名确定性。
+  - form-data字段完整。
+  - 成功响应解析分页和人员列表。
+  - HTTP错误、网络异常、业务错误、schema异常。
+  - 缺失配置和非法 encryptionType。
+
+### 应排除
+
+- 全量分页循环。
+- 重试机制，尤其是认证失败重试。
+- Provider接入、数据库写入、CSV替换。
+- 班级/辅导员/宿舍字段业务映射。
+- 真实API测试进入 CI 或常规测试。
+- 完整原始响应日志。
+
+---
+
+## 最终建议
+
+Step 1A可以作为“签名函数切片”通过；进入下一步前建议补 MD5 固定值测试。下一步不要先写孤立诊断脚本，而是先做一个很窄的 Step 1B-lite，让 Step 1C 复用同一套请求构造、签名和脱敏逻辑。真实 live probe 仍必须保持单页一条、显式开关、脱敏输出。

 succeeded in 180ms:
appended event 100
collaboration files valid

codex
The collaboration event and state update succeeded and validated. I’m doing one final diff/status check limited to the files I touched so the close-out is accurate.
exec
/bin/bash -lc 'rtk git status --short docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md .omc/collaboration/events.jsonl .omc/collaboration/state.json' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
 M .omc/collaboration/events.jsonl
 M .omc/collaboration/state.json
?? docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Step 1A完成审查与下一步策略 - Codex响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**审查类型：** 实现审查 + 策略建议  
**针对：** `80-step1a-completion-next-review-request.md`  
**文档编号：** 81

---

## 1. Step 1A审查结果

**结论：Step 1A签名纯函数可以通过，但建议在进入真实诊断前补两个小修正。**

已验证：

- `backend/apps/users/integrations/xg_user_client.py` 的 `generate_sign()` 按三个参数值排序后拼接，再做 `sha1/md5` 小写 hex，符合当前官方样例约束。
- 官方样例测试覆盖了显式 `sha1` 和默认 `sha1`。
- 非法 `encryption_type` 会失败，不会静默降级。
- 聚焦测试在 Docker 环境通过：`rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client -v 2 --keepdb --noinput`，4/4 passed。

### P0问题

无。

当前代码没有发现会导致官方签名样例失败、密钥泄露或错误参与字段签名的 P0 问题。

### P1问题

1. **MD5测试断言过弱。**  
   位置：`backend/apps/users/tests/test_xg_user_client.py:28`  
   现在只检查长度和 hex 字符集，即使拼接顺序错误也可能通过。建议改成固定期望值，例如 `generate_sign('secret', '1234567890', 'random', 'md5')` 应等于 `2a471e23465cf11561ef7455fff00a86`。

2. **Step 1A相对 doc 77 的“配置切片”尚未完成。**  
   位置：`backend/apps/users/integrations/xg_user_client.py:46`  
   当前只交付签名函数，`XGUserAPIClient` 仍是占位类，尚无配置读取/校验对象。若把 Step 1A 定义为“签名函数切片”，可以接受；若沿用 doc 77 验收标准，则还缺少 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 的明确错误测试。

### P2问题

1. **空字符串策略需要在边界上明确。**  
   `generate_sign()` 作为纯函数可以允许空字符串，但请求构建/配置层必须拒绝空 `appSecret/timestamp/randStr`。建议不要在签名函数里混入环境语义，在 Step 1B 的 config/header 构造处校验。

2. **特殊字符与 Unicode 不需要作为 P0，但可补一个文档化测试。**  
   当前实现使用 UTF-8 编码，行为确定。实际 header 中的 `randStr` 应限制为 ASCII 随机串；如果平台文档没有要求 Unicode，测试不必扩大为必选项。

3. **大小写/空白归一化应放在配置层。**  
   `generate_sign()` 严格接受 `sha1/md5` 是合理的；环境变量读取时可以对 `XG_USER_API_ENCRYPTION_TYPE` 做 `strip().lower()`，再传入纯函数。

### 安全评价

- 当前签名函数不会记录或返回密钥，仅返回摘要，安全面较小。
- `md5` 只因官方接口兼容而保留，不应作为默认值。
- 后续诊断脚本不得打印完整 `appSecret`、完整 `sign`、手机号、身份证号、openId 或完整原始响应。

---

## 2. 下一步策略建议

**建议选择“修正后的选项A”：先做 Step 1B-lite，再做 Step 1C。**

不建议纯选项B先写诊断脚本。诊断脚本也必须构造 headers/form-data、生成 timestamp/randStr/sign、处理超时和脱敏输出；如果没有可复用客户端层，脚本会复制 Step 1B 逻辑，后续再迁回客户端时容易产生签名字段、日志脱敏、错误分类不一致。

推荐顺序：

1. **立即补 Step 1A 小修正。**  
   固定 MD5 期望值；如坚持 doc 77 的 Step 1A 验收，再补配置校验对象与缺失配置测试。

2. **执行 Step 1B-lite。**  
   只实现配置读取、headers 构造、form-data 构造、单页请求、基础响应解析和 mock 测试。不做分页循环、不做重试、不接入业务 Provider。

3. **随后执行 Step 1C。**  
   诊断脚本调用 Step 1B-lite 的客户端能力，默认 dry-run；只有 `XG_RUN_LIVE_API_TEST=1` 且配置齐全时做一次 `page=1/pageNum=1` live probe。

这样仍然能快速验证网络/API可达性，但不会牺牲可测试性和脱敏一致性。

---

## 3. Step 1C范围确认

Step 1C范围基本合理，但需要改成“安全诊断入口”，不是完整请求/响应日志收集器。

### 必须包含

- 环境变量读取与校验：URL、appKey、appSecret、tenantCode、encryptionType、live开关。
- 官方签名样例自检。
- 默认 dry-run，请求摘要不发网络请求。
- live probe 硬门禁：`XG_RUN_LIVE_API_TEST=1`，配置齐全，固定 `page=1/pageNum=1`。
- 输出格式：默认 text，支持 `--format=json`。
- 超时参数：默认短超时，例如 5 秒，可用 `--timeout` 调整。
- 错误分类：`config_error`、`sign_error`、`network_error`、`http_error`、`auth_failed`、`tenant_invalid`、`business_error`、`unexpected_schema`。
- 脱敏输出：只显示 header/form-data 的非敏感摘要；响应 body 只允许脱敏预览。

### 应删除或限制

- 不记录完整请求 headers，因为其中包含完整 `sign`。
- 不保存完整响应 body，除非先脱敏并明确标注。
- 不做分页循环、批量读取、落库、字段映射结论。
- 不在常规 Django/pytest 测试套件里触发 live API。

### 建议输出

文本输出保持短摘要：

```text
配置: OK
签名样例: OK
Live调用: skipped (XG_RUN_LIVE_API_TEST != 1)
请求摘要: POST auth-user-info page=1 pageNum=1 encryptionType=sha1 sign=present
```

live 成功时输出：

```text
HTTP状态: 200
业务码: 200
分页: current_page=1 per_page=1 total=...
字段覆盖: name=yes number=yes phone=yes department=yes user_identity=yes
样本: name=张* number=17**** phone=186****9896
```

---

## 4. Step 1B范围界定

### 应包含

- `XGUserAPIConfig` 或等价配置对象：从环境读取、校验必填项、归一化 encryptionType。
- `XGUserAPIClient.build_headers()`：
  - 包含 `appKey/timestamp/randStr/sign/encryptionType`。
  - 默认不发送 `appId`，除非平台部确认接口要求。
  - timestamp/randStr 可注入或可 patch，方便确定性测试。
- `XGUserAPIClient.build_form_data()`：
  - 包含 `tenantCode/page/pageNum`。
  - 默认 `page=1/pageNum=1`。
- `XGUserAPIClient.fetch_users_page()`：
  - 使用短超时。
  - 支持注入 session，便于 mock `post`。
  - 只请求单页。
- 响应解析：
  - 协议层解析 `code/msg/data/current_page/data/total/per_page`。
  - 人员字段先宽松采样，不做业务字段强承诺。
- Mock测试：
  - header字段完整、签名确定性。
  - form-data字段完整。
  - 成功响应解析分页和人员列表。
  - HTTP错误、网络异常、业务错误、schema异常。
  - 缺失配置和非法 encryptionType。

### 应排除

- 全量分页循环。
- 重试机制，尤其是认证失败重试。
- Provider接入、数据库写入、CSV替换。
- 班级/辅导员/宿舍字段业务映射。
- 真实API测试进入 CI 或常规测试。
- 完整原始响应日志。

---

## 最终建议

Step 1A可以作为“签名函数切片”通过；进入下一步前建议补 MD5 固定值测试。下一步不要先写孤立诊断脚本，而是先做一个很窄的 Step 1B-lite，让 Step 1C 复用同一套请求构造、签名和脱敏逻辑。真实 live probe 仍必须保持单页一条、显式开关、脱敏输出。

exec
/bin/bash -lc 'rtk tail -n 2 .omc/collaboration/events.jsonl' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{"id":99,"type":"review_response","agent":"codex","timestamp":"2026-06-02T03:08:57.327738096Z","summary":"Codex reviewed Claude post-Step 0 API test strategy and approved phased diagnostic-client implementation while keeping live calls gated on tenantCode.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md"],"status":"waiting_for_claude_response","details":{"decision":"approve_phased_diagnostic_client","recommended_order":["signature_and_config_tests","request_parse_mock_tests","diagnostic_probe","live_probe_after_tenant_code"],"live_gate":"XG_RUN_LIVE_API_TEST=1 plus confirmed tenantCode"}}
{"id":100,"type":"review_response","agent":"codex","timestamp":"2026-06-02T03:26:08.406715Z","summary":"Codex reviewed Step 1A signature implementation and recommended Step 1B-lite before diagnostic script.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md"],"status":"waiting_for_claude_response","details":{"decision":"step1a_passes_signature_slice_with_p1_test_improvement","recommended_next":["fix_md5_expected_value_test","step1b_lite_request_build_mock_tests","step1c_probe_reusing_client"],"verification":"4/4 xg_user_client tests passed in Docker with --keepdb --noinput"}}

exec
/bin/bash -lc "rtk sed -n '1,80p' .omc/collaboration/state.json" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{
  "workflow_id": "claude-codex-collab-mvp",
  "current_task": "phase4c_next_steps",
  "active_agent": "claude",
  "status": "waiting_for_claude_response",
  "last_event_id": 100,
  "updated_at": "2026-06-02T03:26:08.406715Z"
}

diff --git a/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md b/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..05489a45877a612064fcbe7cacb8b5dd61370ea0
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
@@ -0,0 +1,162 @@
+# Step 1A完成审查与下一步策略 - Codex响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**审查类型：** 实现审查 + 策略建议  
+**针对：** `80-step1a-completion-next-review-request.md`  
+**文档编号：** 81
+
+---
+
+## 1. Step 1A审查结果
+
+**结论：Step 1A签名纯函数可以通过，但建议在进入真实诊断前补两个小修正。**
+
+已验证：
+
+- `backend/apps/users/integrations/xg_user_client.py` 的 `generate_sign()` 按三个参数值排序后拼接，再做 `sha1/md5` 小写 hex，符合当前官方样例约束。
+- 官方样例测试覆盖了显式 `sha1` 和默认 `sha1`。
+- 非法 `encryption_type` 会失败，不会静默降级。
+- 聚焦测试在 Docker 环境通过：`rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client -v 2 --keepdb --noinput`，4/4 passed。
+
+### P0问题
+
+无。
+
+当前代码没有发现会导致官方签名样例失败、密钥泄露或错误参与字段签名的 P0 问题。
+
+### P1问题
+
+1. **MD5测试断言过弱。**  
+   位置：`backend/apps/users/tests/test_xg_user_client.py:28`  
+   现在只检查长度和 hex 字符集，即使拼接顺序错误也可能通过。建议改成固定期望值，例如 `generate_sign('secret', '1234567890', 'random', 'md5')` 应等于 `2a471e23465cf11561ef7455fff00a86`。
+
+2. **Step 1A相对 doc 77 的“配置切片”尚未完成。**  
+   位置：`backend/apps/users/integrations/xg_user_client.py:46`  
+   当前只交付签名函数，`XGUserAPIClient` 仍是占位类，尚无配置读取/校验对象。若把 Step 1A 定义为“签名函数切片”，可以接受；若沿用 doc 77 验收标准，则还缺少 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 的明确错误测试。
+
+### P2问题
+
+1. **空字符串策略需要在边界上明确。**  
+   `generate_sign()` 作为纯函数可以允许空字符串，但请求构建/配置层必须拒绝空 `appSecret/timestamp/randStr`。建议不要在签名函数里混入环境语义，在 Step 1B 的 config/header 构造处校验。
+
+2. **特殊字符与 Unicode 不需要作为 P0，但可补一个文档化测试。**  
+   当前实现使用 UTF-8 编码，行为确定。实际 header 中的 `randStr` 应限制为 ASCII 随机串；如果平台文档没有要求 Unicode，测试不必扩大为必选项。
+
+3. **大小写/空白归一化应放在配置层。**  
+   `generate_sign()` 严格接受 `sha1/md5` 是合理的；环境变量读取时可以对 `XG_USER_API_ENCRYPTION_TYPE` 做 `strip().lower()`，再传入纯函数。
+
+### 安全评价
+
+- 当前签名函数不会记录或返回密钥，仅返回摘要，安全面较小。
+- `md5` 只因官方接口兼容而保留，不应作为默认值。
+- 后续诊断脚本不得打印完整 `appSecret`、完整 `sign`、手机号、身份证号、openId 或完整原始响应。
+
+---
+
+## 2. 下一步策略建议
+
+**建议选择“修正后的选项A”：先做 Step 1B-lite，再做 Step 1C。**
+
+不建议纯选项B先写诊断脚本。诊断脚本也必须构造 headers/form-data、生成 timestamp/randStr/sign、处理超时和脱敏输出；如果没有可复用客户端层，脚本会复制 Step 1B 逻辑，后续再迁回客户端时容易产生签名字段、日志脱敏、错误分类不一致。
+
+推荐顺序：
+
+1. **立即补 Step 1A 小修正。**  
+   固定 MD5 期望值；如坚持 doc 77 的 Step 1A 验收，再补配置校验对象与缺失配置测试。
+
+2. **执行 Step 1B-lite。**  
+   只实现配置读取、headers 构造、form-data 构造、单页请求、基础响应解析和 mock 测试。不做分页循环、不做重试、不接入业务 Provider。
+
+3. **随后执行 Step 1C。**  
+   诊断脚本调用 Step 1B-lite 的客户端能力，默认 dry-run；只有 `XG_RUN_LIVE_API_TEST=1` 且配置齐全时做一次 `page=1/pageNum=1` live probe。
+
+这样仍然能快速验证网络/API可达性，但不会牺牲可测试性和脱敏一致性。
+
+---
+
+## 3. Step 1C范围确认
+
+Step 1C范围基本合理，但需要改成“安全诊断入口”，不是完整请求/响应日志收集器。
+
+### 必须包含
+
+- 环境变量读取与校验：URL、appKey、appSecret、tenantCode、encryptionType、live开关。
+- 官方签名样例自检。
+- 默认 dry-run，请求摘要不发网络请求。
+- live probe 硬门禁：`XG_RUN_LIVE_API_TEST=1`，配置齐全，固定 `page=1/pageNum=1`。
+- 输出格式：默认 text，支持 `--format=json`。
+- 超时参数：默认短超时，例如 5 秒，可用 `--timeout` 调整。
+- 错误分类：`config_error`、`sign_error`、`network_error`、`http_error`、`auth_failed`、`tenant_invalid`、`business_error`、`unexpected_schema`。
+- 脱敏输出：只显示 header/form-data 的非敏感摘要；响应 body 只允许脱敏预览。
+
+### 应删除或限制
+
+- 不记录完整请求 headers，因为其中包含完整 `sign`。
+- 不保存完整响应 body，除非先脱敏并明确标注。
+- 不做分页循环、批量读取、落库、字段映射结论。
+- 不在常规 Django/pytest 测试套件里触发 live API。
+
+### 建议输出
+
+文本输出保持短摘要：
+
+```text
+配置: OK
+签名样例: OK
+Live调用: skipped (XG_RUN_LIVE_API_TEST != 1)
+请求摘要: POST auth-user-info page=1 pageNum=1 encryptionType=sha1 sign=present
+```
+
+live 成功时输出：
+
+```text
+HTTP状态: 200
+业务码: 200
+分页: current_page=1 per_page=1 total=...
+字段覆盖: name=yes number=yes phone=yes department=yes user_identity=yes
+样本: name=张* number=17**** phone=186****9896
+```
+
+---
+
+## 4. Step 1B范围界定
+
+### 应包含
+
+- `XGUserAPIConfig` 或等价配置对象：从环境读取、校验必填项、归一化 encryptionType。
+- `XGUserAPIClient.build_headers()`：
+  - 包含 `appKey/timestamp/randStr/sign/encryptionType`。
+  - 默认不发送 `appId`，除非平台部确认接口要求。
+  - timestamp/randStr 可注入或可 patch，方便确定性测试。
+- `XGUserAPIClient.build_form_data()`：
+  - 包含 `tenantCode/page/pageNum`。
+  - 默认 `page=1/pageNum=1`。
+- `XGUserAPIClient.fetch_users_page()`：
+  - 使用短超时。
+  - 支持注入 session，便于 mock `post`。
+  - 只请求单页。
+- 响应解析：
+  - 协议层解析 `code/msg/data/current_page/data/total/per_page`。
+  - 人员字段先宽松采样，不做业务字段强承诺。
+- Mock测试：
+  - header字段完整、签名确定性。
+  - form-data字段完整。
+  - 成功响应解析分页和人员列表。
+  - HTTP错误、网络异常、业务错误、schema异常。
+  - 缺失配置和非法 encryptionType。
+
+### 应排除
+
+- 全量分页循环。
+- 重试机制，尤其是认证失败重试。
+- Provider接入、数据库写入、CSV替换。
+- 班级/辅导员/宿舍字段业务映射。
+- 真实API测试进入 CI 或常规测试。
+- 完整原始响应日志。
+
+---
+
+## 最终建议
+
+Step 1A可以作为“签名函数切片”通过；进入下一步前建议补 MD5 固定值测试。下一步不要先写孤立诊断脚本，而是先做一个很窄的 Step 1B-lite，让 Step 1C 复用同一套请求构造、签名和脱敏逻辑。真实 live probe 仍必须保持单页一条、显式开关、脱敏输出。

codex
已完成 Codex 审查响应，写入：

[81-step1a-completion-codex-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md)

核心结论：Step 1A 作为“签名函数切片”可通过，无 P0；建议补强 MD5 固定期望值测试。下一步不建议先写孤立 Step 1C 诊断脚本，建议先做窄版 Step 1B-lite，让诊断脚本复用客户端的请求构造、签名、脱敏和错误分类逻辑。

验证结果：host 缺 Django，无法跑本地测试；Docker 中运行 `apps.users.tests.test_xg_user_client` 通过，4/4 passed。协作日志已追加 event 100，state 已更新为等待 Claude 响应。
diff --git a/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md b/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..05489a45877a612064fcbe7cacb8b5dd61370ea0
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
@@ -0,0 +1,162 @@
+# Step 1A完成审查与下一步策略 - Codex响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**审查类型：** 实现审查 + 策略建议  
+**针对：** `80-step1a-completion-next-review-request.md`  
+**文档编号：** 81
+
+---
+
+## 1. Step 1A审查结果
+
+**结论：Step 1A签名纯函数可以通过，但建议在进入真实诊断前补两个小修正。**
+
+已验证：
+
+- `backend/apps/users/integrations/xg_user_client.py` 的 `generate_sign()` 按三个参数值排序后拼接，再做 `sha1/md5` 小写 hex，符合当前官方样例约束。
+- 官方样例测试覆盖了显式 `sha1` 和默认 `sha1`。
+- 非法 `encryption_type` 会失败，不会静默降级。
+- 聚焦测试在 Docker 环境通过：`rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client -v 2 --keepdb --noinput`，4/4 passed。
+
+### P0问题
+
+无。
+
+当前代码没有发现会导致官方签名样例失败、密钥泄露或错误参与字段签名的 P0 问题。
+
+### P1问题
+
+1. **MD5测试断言过弱。**  
+   位置：`backend/apps/users/tests/test_xg_user_client.py:28`  
+   现在只检查长度和 hex 字符集，即使拼接顺序错误也可能通过。建议改成固定期望值，例如 `generate_sign('secret', '1234567890', 'random', 'md5')` 应等于 `2a471e23465cf11561ef7455fff00a86`。
+
+2. **Step 1A相对 doc 77 的“配置切片”尚未完成。**  
+   位置：`backend/apps/users/integrations/xg_user_client.py:46`  
+   当前只交付签名函数，`XGUserAPIClient` 仍是占位类，尚无配置读取/校验对象。若把 Step 1A 定义为“签名函数切片”，可以接受；若沿用 doc 77 验收标准，则还缺少 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 的明确错误测试。
+
+### P2问题
+
+1. **空字符串策略需要在边界上明确。**  
+   `generate_sign()` 作为纯函数可以允许空字符串，但请求构建/配置层必须拒绝空 `appSecret/timestamp/randStr`。建议不要在签名函数里混入环境语义，在 Step 1B 的 config/header 构造处校验。
+
+2. **特殊字符与 Unicode 不需要作为 P0，但可补一个文档化测试。**  
+   当前实现使用 UTF-8 编码，行为确定。实际 header 中的 `randStr` 应限制为 ASCII 随机串；如果平台文档没有要求 Unicode，测试不必扩大为必选项。
+
+3. **大小写/空白归一化应放在配置层。**  
+   `generate_sign()` 严格接受 `sha1/md5` 是合理的；环境变量读取时可以对 `XG_USER_API_ENCRYPTION_TYPE` 做 `strip().lower()`，再传入纯函数。
+
+### 安全评价
+
+- 当前签名函数不会记录或返回密钥，仅返回摘要，安全面较小。
+- `md5` 只因官方接口兼容而保留，不应作为默认值。
+- 后续诊断脚本不得打印完整 `appSecret`、完整 `sign`、手机号、身份证号、openId 或完整原始响应。
+
+---
+
+## 2. 下一步策略建议
+
+**建议选择“修正后的选项A”：先做 Step 1B-lite，再做 Step 1C。**
+
+不建议纯选项B先写诊断脚本。诊断脚本也必须构造 headers/form-data、生成 timestamp/randStr/sign、处理超时和脱敏输出；如果没有可复用客户端层，脚本会复制 Step 1B 逻辑，后续再迁回客户端时容易产生签名字段、日志脱敏、错误分类不一致。
+
+推荐顺序：
+
+1. **立即补 Step 1A 小修正。**  
+   固定 MD5 期望值；如坚持 doc 77 的 Step 1A 验收，再补配置校验对象与缺失配置测试。
+
+2. **执行 Step 1B-lite。**  
+   只实现配置读取、headers 构造、form-data 构造、单页请求、基础响应解析和 mock 测试。不做分页循环、不做重试、不接入业务 Provider。
+
+3. **随后执行 Step 1C。**  
+   诊断脚本调用 Step 1B-lite 的客户端能力，默认 dry-run；只有 `XG_RUN_LIVE_API_TEST=1` 且配置齐全时做一次 `page=1/pageNum=1` live probe。
+
+这样仍然能快速验证网络/API可达性，但不会牺牲可测试性和脱敏一致性。
+
+---
+
+## 3. Step 1C范围确认
+
+Step 1C范围基本合理，但需要改成“安全诊断入口”，不是完整请求/响应日志收集器。
+
+### 必须包含
+
+- 环境变量读取与校验：URL、appKey、appSecret、tenantCode、encryptionType、live开关。
+- 官方签名样例自检。
+- 默认 dry-run，请求摘要不发网络请求。
+- live probe 硬门禁：`XG_RUN_LIVE_API_TEST=1`，配置齐全，固定 `page=1/pageNum=1`。
+- 输出格式：默认 text，支持 `--format=json`。
+- 超时参数：默认短超时，例如 5 秒，可用 `--timeout` 调整。
+- 错误分类：`config_error`、`sign_error`、`network_error`、`http_error`、`auth_failed`、`tenant_invalid`、`business_error`、`unexpected_schema`。
+- 脱敏输出：只显示 header/form-data 的非敏感摘要；响应 body 只允许脱敏预览。
+
+### 应删除或限制
+
+- 不记录完整请求 headers，因为其中包含完整 `sign`。
+- 不保存完整响应 body，除非先脱敏并明确标注。
+- 不做分页循环、批量读取、落库、字段映射结论。
+- 不在常规 Django/pytest 测试套件里触发 live API。
+
+### 建议输出
+
+文本输出保持短摘要：
+
+```text
+配置: OK
+签名样例: OK
+Live调用: skipped (XG_RUN_LIVE_API_TEST != 1)
+请求摘要: POST auth-user-info page=1 pageNum=1 encryptionType=sha1 sign=present
+```
+
+live 成功时输出：
+
+```text
+HTTP状态: 200
+业务码: 200
+分页: current_page=1 per_page=1 total=...
+字段覆盖: name=yes number=yes phone=yes department=yes user_identity=yes
+样本: name=张* number=17**** phone=186****9896
+```
+
+---
+
+## 4. Step 1B范围界定
+
+### 应包含
+
+- `XGUserAPIConfig` 或等价配置对象：从环境读取、校验必填项、归一化 encryptionType。
+- `XGUserAPIClient.build_headers()`：
+  - 包含 `appKey/timestamp/randStr/sign/encryptionType`。
+  - 默认不发送 `appId`，除非平台部确认接口要求。
+  - timestamp/randStr 可注入或可 patch，方便确定性测试。
+- `XGUserAPIClient.build_form_data()`：
+  - 包含 `tenantCode/page/pageNum`。
+  - 默认 `page=1/pageNum=1`。
+- `XGUserAPIClient.fetch_users_page()`：
+  - 使用短超时。
+  - 支持注入 session，便于 mock `post`。
+  - 只请求单页。
+- 响应解析：
+  - 协议层解析 `code/msg/data/current_page/data/total/per_page`。
+  - 人员字段先宽松采样，不做业务字段强承诺。
+- Mock测试：
+  - header字段完整、签名确定性。
+  - form-data字段完整。
+  - 成功响应解析分页和人员列表。
+  - HTTP错误、网络异常、业务错误、schema异常。
+  - 缺失配置和非法 encryptionType。
+
+### 应排除
+
+- 全量分页循环。
+- 重试机制，尤其是认证失败重试。
+- Provider接入、数据库写入、CSV替换。
+- 班级/辅导员/宿舍字段业务映射。
+- 真实API测试进入 CI 或常规测试。
+- 完整原始响应日志。
+
+---
+
+## 最终建议
+
+Step 1A可以作为“签名函数切片”通过；进入下一步前建议补 MD5 固定值测试。下一步不要先写孤立诊断脚本，而是先做一个很窄的 Step 1B-lite，让 Step 1C 复用同一套请求构造、签名和脱敏逻辑。真实 live probe 仍必须保持单页一条、显式开关、脱敏输出。

tokens used
79,870

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
