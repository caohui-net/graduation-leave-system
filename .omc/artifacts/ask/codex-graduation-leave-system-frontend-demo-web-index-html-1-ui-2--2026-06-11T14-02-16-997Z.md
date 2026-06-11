# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-11T14:02:16.997Z

## Original task

审计graduation-leave-system最近修改：

**Frontend (demo-web/index.html):**
1. 管理员UI支持：去重逻辑、按钮隐藏、角色显示为'管理员'
2. 循环分页：while循环累积直到20条去重记录
3. Excel预览：模态框+中文状态映射+安全日期格式化
4. 安全修复：escapeHtml()防XSS、MAX_ITERATIONS防无限循环、logout清理内存

**Backend (apps/approvals/serializers.py):**
ApplicationBriefSerializer增加字段：contact_phone, building, room_number, created_at

**重点检查：**
- 逻辑正确性（去重、分页、角色判断）
- 性能问题（循环效率、内存使用）
- 安全隐患（XSS防护是否充分、注入攻击）
- 代码质量（命名、结构、可维护性）
- 最佳实践违反

请提供具体问题和修复建议。

## Final prompt

审计graduation-leave-system最近修改：

**Frontend (demo-web/index.html):**
1. 管理员UI支持：去重逻辑、按钮隐藏、角色显示为'管理员'
2. 循环分页：while循环累积直到20条去重记录
3. Excel预览：模态框+中文状态映射+安全日期格式化
4. 安全修复：escapeHtml()防XSS、MAX_ITERATIONS防无限循环、logout清理内存

**Backend (apps/approvals/serializers.py):**
ApplicationBriefSerializer增加字段：contact_phone, building, room_number, created_at

**重点检查：**
- 逻辑正确性（去重、分页、角色判断）
- 性能问题（循环效率、内存使用）
- 安全隐患（XSS防护是否充分、注入攻击）
- 代码质量（命名、结构、可维护性）
- 最佳实践违反

请提供具体问题和修复建议。

## Raw output

```text
**审计结论：需要修改。** 主要风险集中在前端：XSS 修复覆盖不完整、分页去重会丢数据、Excel 预览与实际导出不一致。后端新增 serializer 字段本身没有明显 N+1 问题，因为列表查询已 `select_related('application', 'application__student', 'approver')`。

**发现的问题**

1. **高危：XSS 修复不完整，多个新增/相关 UI 仍直接拼接 `innerHTML`**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:290)、[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:770)、[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:425)、[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:1442)

   `escapeHtml()` 只用于审批列表的少数字段。学生详情、审批详情、Excel 预览、上传文件列表仍拼接 `student_name`、`reason`、`comment`、`approver_name`、`file_name`、`building`、`room_number` 等用户/外部输入。文件名还被拼进 `onclick` 属性，单引号可打断 JS 字符串。

   修复建议：不要用字符串拼 HTML。优先用 `document.createElement()` + `textContent` + `addEventListener()`；若短期修复，所有文本字段统一 `escapeHtml()`，所有 URL/ID 参数用 `encodeURIComponent()`，事件参数用 `JSON.stringify()` 或改为 `data-*` 绑定。

2. **高危：循环分页去重会永久丢记录**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:111)、[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:134)、[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:144)

   当前先把本轮抓到的全部唯一 `application.id` 加入 `deanDisplayedApps`，再 `slice(0, 20)` 展示。若累积到 21 条，第 21 条已经进了去重 Set，但不会显示；下一次加载从新的 `offset` 继续，导致这条记录永久消失。

   修复建议：只在实际渲染后再加入 displayed Set；或者维护 `pendingApprovalBuffer`，把超过 20 条的记录缓存给下一页；更好的方案是在后端提供按申请去重的分页接口，前端不要对审批记录做跨页去重。

3. **高危：Excel 预览最多只有 100 条审批记录，且可能缺列，和实际导出不一致**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:693)、[backend/apps/approvals/pagination.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/pagination.py:7)、[backend/apps/approvals/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:380)

   前端请求 `limit=1000`，但后端 `max_limit = 100`，所以预览最多拿 100 条 approval，不是 1000。实际下载接口导出的是最多 1000 个 application，并预取审批记录。预览按 approval 分组，若同一申请的宿管/辅导员记录不在前 100 条内，预览会显示不完整。

   修复建议：新增 `/approvals/export/preview/`，复用导出接口的 application 查询和组装逻辑；或前端按分页循环拉满到 1000，但仍建议以后端 application 为单位生成预览。

4. **中高：`MAX_ITERATIONS` 会在有更多数据时隐藏“加载更多”并显示空数据**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:92)、[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:233)

   如果前 10 页都被前端过滤/去重掉，`displayRecords.length === 0` 会进入空态并隐藏按钮，即使 `currentOffset < totalCount`。`decided` 过滤尤其容易触发，因为前端用 `decision=all` 拉数据后本地过滤。

   修复建议：后端支持 `decision=decided` 或 `decision__in=approved,rejected`；前端在达到迭代上限且 `currentOffset < totalCount` 时不能隐藏加载更多，也不能显示“暂无数据”。

5. **中危：登出没有清理持久化登录态**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:1367)、[demo-web/js/api.js](/home/caohui/projects/graduation-leave-system/demo-web/js/api.js:9)

   `logout()` 只清内存变量，但 `api.js` 会从 `localStorage.auth_token` / `user_info` 恢复登录。SSO callback 会写这些值。用户点退出后刷新页面可能又自动登录。

   修复建议：`logout()` 中同时执行：
   ```js
   localStorage.removeItem('auth_token');
   localStorage.removeItem('user_info');
   uploadedFiles = [];
   renderFileList();
   ```

6. **中危：admin “隐藏审批按钮”只是 UI 控制，后端仍允许 admin 审批/驳回**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:1354)、[backend/apps/approvals/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:162)、[backend/apps/approvals/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:302)

   如果管理员定位为“仅查询”，隐藏按钮不构成权限控制，直接调用 API 仍可审批。测试里还明确断言 admin 可审批。

   修复建议：明确产品语义。若 admin 只读，移除后端 admin bypass，并改测试；若 admin 可代审批，则前端不应隐藏按钮，或至少展示“代审批”权限。

7. **中危：新增学生详情页审批记录接口实际拿不到数据**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:282)、[backend/apps/approvals/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:54)

   学生调用 `/approvals/?application_id=...` 会被 403；后端也没有处理 `application_id` 过滤。结果学生详情审批进度基本只能靠 `app.status` 猜，审批人、时间、驳回原因拿不到。

   修复建议：直接使用 `/applications/{id}/` 返回的 `approvals` 字段；或者新增学生可访问的 application approval history endpoint。

8. **低到中：管理员角色显示修复不完整**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:1279)、[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:1352)

   列表右侧 `role-display` 会显示“管理员”，但登录后顶部 `currentUserRole` 的 `roleMap` 缺少 `admin`，普通登录路径会显示 `(admin)`。

   修复建议：两个 role map 合并成一个全局 `ROLE_LABELS`，避免显示不一致。

**补充检查**

`ApplicationBriefSerializer` 新增 `contact_phone/building/room_number/created_at` 本身可用，且 approvals 列表查询已做 `select_related`，没有看到新增字段导致的明显 N+1。但这些字段会出现在所有审批列表角色响应中，若宿管/辅导员列表不需要全部宿舍信息，建议按角色或接口用途收敛字段。


OpenAI Codex v0.138.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019eb6fa-7177-75f3-95c8-7c1eb0a3ec20
--------
user
审计graduation-leave-system最近修改：

**Frontend (demo-web/index.html):**
1. 管理员UI支持：去重逻辑、按钮隐藏、角色显示为'管理员'
2. 循环分页：while循环累积直到20条去重记录
3. Excel预览：模态框+中文状态映射+安全日期格式化
4. 安全修复：escapeHtml()防XSS、MAX_ITERATIONS防无限循环、logout清理内存

**Backend (apps/approvals/serializers.py):**
ApplicationBriefSerializer增加字段：contact_phone, building, room_number, created_at

**重点检查：**
- 逻辑正确性（去重、分页、角色判断）
- 性能问题（循环效率、内存使用）
- 安全隐患（XSS防护是否充分、注入攻击）
- 代码质量（命名、结构、可维护性）
- 最佳实践违反

请提供具体问题和修复建议。
codex
我会按项目的审计协议先读取本地规则，然后检查相关 diff 和实现细节，重点按你列的逻辑、性能、安全和维护性维度给出问题。
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
已读取项目规则。后续命令我会按仓库要求用 `rtk` 前缀；现在先看最近变更和两个目标文件的上下文，再定位具体风险点。
exec
/bin/bash -lc 'rtk git log --oneline -5 -- demo-web/index.html apps/approvals/serializers.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
7b2fce6 fix(security): 修复XSS漏洞、无限循环风险、内存泄漏
68d5ea0 fix(demo-web): 修复Excel预览日期显示Invalid Date问题
afd6d9f fix(demo-web): Excel预览状态字段中文化
f532f03 feat(demo-web): 添加Excel导出预览功能
097e0f7 refactor(demo-web): 重构分页逻辑，固定显示20条去重后的记录

exec
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
 M .omc/project-memory.json
 M .omc/session-context.json
 M .omc/state/agent-replay-d6e66725-4b67-4dd4-a5e4-db4b7079be97.jsonl
 M .omc/state/hud-stdin-cache.json
 M .omc/state/last-tool-error.json
 M .omc/state/sessions/d6e66725-4b67-4dd4-a5e4-db4b7079be97/session-started.json
 M .wolf/anatomy.md
 M .wolf/hooks/_session.json
 M .wolf/memory.md
 M .wolf/token-ledger.json
 M backend/.omc/state/last-tool-error.json
 M backend/.omc/state/subagent-tracking.json
 M backend/apps/users/serializers.py
 M backend/backend/.omc/state/last-tool-error.json
 M demo-web/index.html
 M demo-web/mobile-sso-callback.html
?? .omc/state/agent-replay-3d083cc4-a44f-4127-9dca-94c726dcd3d9.jsonl
?? .omc/state/checkpoints/checkpoint-2026-06-11T05-13-54-689Z.json
?? .omc/state/checkpoints/checkpoint-2026-06-11T06-14-59-392Z.json
?? .omc/state/checkpoints/checkpoint-2026-06-11T10-37-16-941Z.json
?? .omc/state/sessions/3d083cc4-a44f-4127-9dca-94c726dcd3d9/
?? .omc/state/sessions/c412db69-4e34-4904-969a-9c87d1bf29c1/
?? backend/.omc/state/agent-replay-3d083cc4-a44f-4127-9dca-94c726dcd3d9.jsonl
?? backend/.omc/state/agent-replay-c412db69-4e34-4904-969a-9c87d1bf29c1.jsonl
?? backend/check_approvals.py
?? backend/test_api_response.py
?? backend/test_student_interface.py
?? backend/test_student_room_info.py
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260611144228_1159_47.jpg"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260611180317_25_1707.jpg"
?? "docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260611182142_639_2.jpg"
exec
/bin/bash -lc 'rtk git diff -- demo-web/index.html apps/approvals/serializers.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
demo-web/index.html | 177 ++++++++++++++++++++++++++++++++++++++++++++++++++--
 1 file changed, 173 insertions(+), 4 deletions(-)

--- Changes ---

demo-web/index.html
  @@ -39,7 +39,7 @@
  -                htmlStr += '<div class="card" style="cursor: pointer;">' +
  +                htmlStr += '<div class="card" style="cursor: pointer;" onclick="showApplicationDetail(\'' + app.application_id + '\')">' +
                     '<div class="flex-row justify-between align-center" style="margin-bottom: 8px;">' +
                       '<span style="font-size: 16px; font-weight: bold;">申请 ' + appIdDisplay + '</span>' +
                       '<span class="tag ' + statusDisplay.class + '">' + statusDisplay.text + '</span>' +
  @@ -263,6 +263,141 @@
  +    async function showApplicationDetail(applicationId) {
  +        // Student view: show application detail with approval history
  +        showScreen(2);
  +
  +        const appRes = await fetch(API_BASE_URL + '/applications/' + applicationId + '/', {
  +            headers: getAuthHeaders()
  +        });
  +
  +        if (!appRes.ok) {
  +            document.querySelector('#screen-2').innerHTML = '<div class="card"><p style="color: #ff4d4f;">加载失败</p></div>';
  +            return;
  +        }
  +
  +        const appData = await appRes.json();
  +        const attachments = await apiGetAttachments(applicationId);
  +
  +        // Fetch approval records
  +        const approvalsRes = await fetch(API_BASE_URL + '/approvals/?application_id=' + applicationId, {
  +            headers: getAuthHeaders()
  +        });
  +        const approvalsData = approvalsRes.ok ? await approvalsRes.json() : { results: [] };
  +
  +        const container = document.querySelector('#screen-2');
  +
  +        const basicInfoHtml = '<div class="card">' +
  +            '<div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">基本信息</div>' +
  +            '<div style="display: flex; margin-bottom: 8px;">' +
  +              '<span style="font-size: 14px; color: #999; width: 80px;">申请ID:</span>' +
  +              '<span style="font-size: 14px; color: #333;">' + (appData.application_id || '-') + '</span>' +
  +            '</div>' +
  +            '<div style="display: flex; margin-bottom: 8px;">' +
  +              '<span style="font-size: 14px; color: #999; width: 80px;">学生姓名:</span>' +
  +              '<span style="font-size: 14px; color: #333;">' + (appData.student_name || '-') + '</span>' +
  +            '</div>' +
  +            '<div style="display: flex; margin-bottom: 8px;">' +
  +              '<span style="font-size: 14px; color: #999; width: 80px;">联系电话:</span>' +
  +              '<span style="font-size: 14px; color: #333;">' + (appData.contact_phone || '-') + '</span>' +
  +            '</div>' +
  +            '<div style="display: flex; margin-bottom: 8px;">' +
  +              '<span style="font-size: 14px; color: #999; width: 80px;">离校日期:</span>' +
  +              '<span style="font-size: 14px; color: #333;">' + (appData.leave_date || '-') + '</span>' +
  +            '</div>' +
  +            '<div style="display: flex; margin-bottom: 8px;">' +
  +              '<span style="font-size: 14px; color: #999; width: 80px;">离校原因:</span>' +
  +              '<span style="font-size: 14px; color: #333;">' + (appData.reason || '-') + '</span>' +
  +            '</div>' +
  +          '</div>';
  +
  +        const attachmentsHtml = '<div class="card">' +
  +            '<div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">附件材料</div>' +
  +            (attachments && attachments.length > 0
  +                ? attachments.map(att =>
  +                    '<div style="display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid #f0f0f0;">' +
  +                      '<span style="flex: 1; font-size: 14px; color: #333;">' + att.filename + '</span>' +
  +                      '<button class="btn-outline" style="padding: 4px 12px; font-size: 13px;" onclick="previewAttachment(\'' + att.attachment_id + '\')">预览</button>' +
  +                    '</div>'
  +                  ).join('')
  +                : '<div style="color: #999; font-size: 14px;">无附件</div>') +
  +          '</div>';
  +
  +        const approvalProgressHtml = renderStudentApprovalProgress(appData, approvalsData.results);
  +
  +        container.innerHTML = basicInfoHtml + attachmentsHtml + approvalProgressHtml +
  +            '<div style="padding: 20px;"><button class="btn-outline" onclick="showScreen(1); loadMyApplications();" style="width: 100%;">返回</button></div>';
  +    }
  +
  +    function renderStudentApprovalProgress(appData, approvals) {
  +        const stepNames = {
  +            'dorm_manager': '宿管员审批',
  +            'counselor': '辅导员审批',
  +            'dean': '学工部审批'
  +        };
  +
  +        const workflow = ['dorm_manager', 'counselor', 'dean'];
  +        const appStatus = appData.status;
  +
  +        let html = '<div class="card"><div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">审批进度</div>';
  +
  +        for (let i = workflow.length - 1; i >= 0; i--) {
  +            const step = workflow[i];
  +            const stepName = stepNames[step];
  +            const approval = approvals.find(a => a.step === step);
  +
  +            let state, tagText, tagCls, dotBg, dotBorder;
  +
  +            if (appStatus === 'rejected' && approval && approval.decision === 'rejected') {
  +                state = 'rejected';
  +                tagText = '已驳回';
  +                tagCls = 'tag-rejected';
  +                dotBg = 'var(--status-error)';
  +                dotBorder = 'var(--status-error)';
  +            } else if (approval && approval.decision === 'approved') {
  +                state = 'approved';
  +                tagText = '已通过';
  +                tagCls = 'tag-approved';
  +                dotBg = 'var(--status-success)';
  +                dotBorder = 'var(--status-success)';
  +            } else if (appStatus === 'pending_' + step) {
  +                state = 'pending';
  +                tagText = '待审批';
  ... (35 lines truncated)
  @@ -688,6 +823,31 @@
  +    function showRejectedApplicationBanner() {
  +        const existingBanner = document.getElementById('rejected-banner');
  +        if (existingBanner) return;
  +
  +        const banner = document.createElement('div');
  +        banner.id = 'rejected-banner';
  +        banner.className = 'card';
  +        banner.style.cssText = 'margin: 20px; margin-bottom: 20px; padding: 16px; background: #fffbe6; border-left: 4px solid #faad14;';
  +        banner.innerHTML = `
  +          <div style="display: flex; align-items: center; gap: 12px;">
  +            <span style="font-size: 20px;">⚠️</span>
  +            <div style="flex: 1;">
  +              <div style="font-size: 14px; font-weight: 600; color: #333; margin-bottom: 4px;">您的申请已被驳回</div>
  +              <div style="font-size: 13px; color: #666;">请查看驳回原因后重新提交申请</div>
  +            </div>
  +            <button class="btn-outline" onclick="showScreen(1); loadMyApplications();" style="padding: 8px 16px; font-size: 13px;">查看驳回原因</button>
  +          </div>
  +        `;
  +        const screen0 = document.getElementById('screen-0');
  +        const firstChild = screen0.querySelector('div[style*="padding: 20px"]');
  +        if (firstChild) {
  +            firstChild.insertBefore(banner, firstChild.firstChild);
  +        }
  +    }
  +
       async function doSubmitApplication() {
           const phone = document.getElementById('contactPhone').value;
           const reason = document.getElementById('applicationReason').value;
  @@ -896,7 +1056,7 @@
  -          <input id="loginPassword" type="password" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入密码" required>
  +          <input id="loginPassword" type="password" autocomplete="new-password" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入密码" required>
           </div>
           <div id="loginError" style="display: none; padding: 10px; background: #fff2f0; border: 1px solid #ffccc7; border-radius: 4px; color: #cf1322; font-size: 14px; margin-bottom: 16px;"></div>
           <button class="btn-primary" onclick="doLogin()">登录</button>
  @@ -1144,11 +1304,20 @@
  -            if (applications.results && applications.results.length > 0) {
  +            const hasApplications = applications.results && applications.results.length > 0;
  +            const hasActiveApplication = hasApplications && applications.results.some(app =>
  +              app.status.startsWith('pending_') || app.status === 'approved'
  +            );
  +
  +            if (hasActiveApplication) {
                 showScreen(1); // Show application progress
                 loadMyApplications();
               } else {
  -              showScreen(0); // Show application form
  +              showScreen(0); // Show application form (allow submit if no active application)
  +              if (hasApplications) {
  +                // Show info banner if has rejected applications
  +                showRejectedApplicationBanner();
  +              }
               }
             } else {
               showScreen(1); // Approval list screen
  +173 -4
[full diff: rtk git diff --no-compact]

codex
当前工作区里 `demo-web/index.html` 有未提交变更；`apps/approvals/serializers.py` 没出现在未提交 diff 里，可能已经在最近提交中。我会同时审查工作区版本和最近提交中的相关改动。
exec
/bin/bash -lc 'rtk git diff --no-compact -- demo-web/index.html' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
diff --git a/demo-web/index.html b/demo-web/index.html
index d47ba18..4318f16 100644
--- a/demo-web/index.html
+++ b/demo-web/index.html
@@ -39,7 +39,7 @@
             filtered.forEach(app => {
                 const statusDisplay = getStatusDisplay(app.status);
                 const appIdDisplay = app.application_id ? app.application_id.substring(0,8) : '未知';
-                htmlStr += '<div class="card" style="cursor: pointer;">' +
+                htmlStr += '<div class="card" style="cursor: pointer;" onclick="showApplicationDetail(\'' + app.application_id + '\')">' +
                   '<div class="flex-row justify-between align-center" style="margin-bottom: 8px;">' +
                     '<span style="font-size: 16px; font-weight: bold;">申请 ' + appIdDisplay + '</span>' +
                     '<span class="tag ' + statusDisplay.class + '">' + statusDisplay.text + '</span>' +
@@ -263,6 +263,141 @@
     }
 
     let currentApprovalId = null;
+    async function showApplicationDetail(applicationId) {
+        // Student view: show application detail with approval history
+        showScreen(2);
+
+        const appRes = await fetch(API_BASE_URL + '/applications/' + applicationId + '/', {
+            headers: getAuthHeaders()
+        });
+
+        if (!appRes.ok) {
+            document.querySelector('#screen-2').innerHTML = '<div class="card"><p style="color: #ff4d4f;">加载失败</p></div>';
+            return;
+        }
+
+        const appData = await appRes.json();
+        const attachments = await apiGetAttachments(applicationId);
+
+        // Fetch approval records
+        const approvalsRes = await fetch(API_BASE_URL + '/approvals/?application_id=' + applicationId, {
+            headers: getAuthHeaders()
+        });
+        const approvalsData = approvalsRes.ok ? await approvalsRes.json() : { results: [] };
+
+        const container = document.querySelector('#screen-2');
+
+        const basicInfoHtml = '<div class="card">' +
+            '<div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">基本信息</div>' +
+            '<div style="display: flex; margin-bottom: 8px;">' +
+              '<span style="font-size: 14px; color: #999; width: 80px;">申请ID:</span>' +
+              '<span style="font-size: 14px; color: #333;">' + (appData.application_id || '-') + '</span>' +
+            '</div>' +
+            '<div style="display: flex; margin-bottom: 8px;">' +
+              '<span style="font-size: 14px; color: #999; width: 80px;">学生姓名:</span>' +
+              '<span style="font-size: 14px; color: #333;">' + (appData.student_name || '-') + '</span>' +
+            '</div>' +
+            '<div style="display: flex; margin-bottom: 8px;">' +
+              '<span style="font-size: 14px; color: #999; width: 80px;">联系电话:</span>' +
+              '<span style="font-size: 14px; color: #333;">' + (appData.contact_phone || '-') + '</span>' +
+            '</div>' +
+            '<div style="display: flex; margin-bottom: 8px;">' +
+              '<span style="font-size: 14px; color: #999; width: 80px;">离校日期:</span>' +
+              '<span style="font-size: 14px; color: #333;">' + (appData.leave_date || '-') + '</span>' +
+            '</div>' +
+            '<div style="display: flex; margin-bottom: 8px;">' +
+              '<span style="font-size: 14px; color: #999; width: 80px;">离校原因:</span>' +
+              '<span style="font-size: 14px; color: #333;">' + (appData.reason || '-') + '</span>' +
+            '</div>' +
+          '</div>';
+
+        const attachmentsHtml = '<div class="card">' +
+            '<div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">附件材料</div>' +
+            (attachments && attachments.length > 0
+                ? attachments.map(att =>
+                    '<div style="display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid #f0f0f0;">' +
+                      '<span style="flex: 1; font-size: 14px; color: #333;">' + att.filename + '</span>' +
+                      '<button class="btn-outline" style="padding: 4px 12px; font-size: 13px;" onclick="previewAttachment(\'' + att.attachment_id + '\')">预览</button>' +
+                    '</div>'
+                  ).join('')
+                : '<div style="color: #999; font-size: 14px;">无附件</div>') +
+          '</div>';
+
+        const approvalProgressHtml = renderStudentApprovalProgress(appData, approvalsData.results);
+
+        container.innerHTML = basicInfoHtml + attachmentsHtml + approvalProgressHtml +
+            '<div style="padding: 20px;"><button class="btn-outline" onclick="showScreen(1); loadMyApplications();" style="width: 100%;">返回</button></div>';
+    }
+
+    function renderStudentApprovalProgress(appData, approvals) {
+        const stepNames = {
+            'dorm_manager': '宿管员审批',
+            'counselor': '辅导员审批',
+            'dean': '学工部审批'
+        };
+
+        const workflow = ['dorm_manager', 'counselor', 'dean'];
+        const appStatus = appData.status;
+
+        let html = '<div class="card"><div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">审批进度</div>';
+
+        for (let i = workflow.length - 1; i >= 0; i--) {
+            const step = workflow[i];
+            const stepName = stepNames[step];
+            const approval = approvals.find(a => a.step === step);
+
+            let state, tagText, tagCls, dotBg, dotBorder;
+
+            if (appStatus === 'rejected' && approval && approval.decision === 'rejected') {
+                state = 'rejected';
+                tagText = '已驳回';
+                tagCls = 'tag-rejected';
+                dotBg = 'var(--status-error)';
+                dotBorder = 'var(--status-error)';
+            } else if (approval && approval.decision === 'approved') {
+                state = 'approved';
+                tagText = '已通过';
+                tagCls = 'tag-approved';
+                dotBg = 'var(--status-success)';
+                dotBorder = 'var(--status-success)';
+            } else if (appStatus === 'pending_' + step) {
+                state = 'pending';
+                tagText = '待审批';
+                tagCls = 'tag-pending';
+                dotBg = 'white';
+                dotBorder = 'var(--primary-color)';
+            } else {
+                state = 'future';
+                tagText = '未开始';
+                tagCls = 'tag';
+                dotBg = '#e8e8e8';
+                dotBorder = '#e8e8e8';
+            }
+
+            html += '<div style="position: relative; padding-left: 30px; margin-bottom: 20px;">' +
+                '<div style="position: absolute; left: 10px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: ' + dotBg + '; border: 2px solid ' + dotBorder + ';"></div>' +
+                '<div style="margin-bottom: 6px;"><span style="font-size: 15px; font-weight: 600;">' + stepName + '</span> <span class="tag ' + tagCls + '">' + tagText + '</span></div>';
+
+            if (approval) {
+                html += '<div style="font-size: 13px; color: #666;">审批人: ' + (approval.approver_name || '待分配') + '</div>';
+                if (approval.decided_at) {
+                    html += '<div style="font-size: 13px; color: #666;">时间: ' + new Date(approval.decided_at).toLocaleString() + '</div>';
+                }
+                if (state === 'rejected') {
+                    const comment = approval.comment && approval.comment.trim() ? approval.comment : '审批人未填写驳回原因';
+                    html += '<div style="font-size: 13px; color: #ff4d4f; margin-top: 4px; font-weight: 600;">驳回原因: ' + comment + '</div>';
+                } else if (approval.comment && approval.comment.trim()) {
+                    html += '<div style="font-size: 13px; color: #666; margin-top: 4px;">意见: ' + approval.comment + '</div>';
+                }
+            }
+
+            html += '</div>';
+        }
+
+        html += '</div>';
+        return html;
+    }
+
     async function openApproval(id) {
         currentApprovalId = id;
         showScreen(2);
@@ -688,6 +823,31 @@
         }
     }
 
+    function showRejectedApplicationBanner() {
+        const existingBanner = document.getElementById('rejected-banner');
+        if (existingBanner) return;
+
+        const banner = document.createElement('div');
+        banner.id = 'rejected-banner';
+        banner.className = 'card';
+        banner.style.cssText = 'margin: 20px; margin-bottom: 20px; padding: 16px; background: #fffbe6; border-left: 4px solid #faad14;';
+        banner.innerHTML = `
+          <div style="display: flex; align-items: center; gap: 12px;">
+            <span style="font-size: 20px;">⚠️</span>
+            <div style="flex: 1;">
+              <div style="font-size: 14px; font-weight: 600; color: #333; margin-bottom: 4px;">您的申请已被驳回</div>
+              <div style="font-size: 13px; color: #666;">请查看驳回原因后重新提交申请</div>
+            </div>
+            <button class="btn-outline" onclick="showScreen(1); loadMyApplications();" style="padding: 8px 16px; font-size: 13px;">查看驳回原因</button>
+          </div>
+        `;
+        const screen0 = document.getElementById('screen-0');
+        const firstChild = screen0.querySelector('div[style*="padding: 20px"]');
+        if (firstChild) {
+            firstChild.insertBefore(banner, firstChild.firstChild);
+        }
+    }
+
     async function doSubmitApplication() {
         const phone = document.getElementById('contactPhone').value;
         const reason = document.getElementById('applicationReason').value;
@@ -896,7 +1056,7 @@
         </div>
         <div style="margin-bottom: 24px;">
           <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">密码</label>
-          <input id="loginPassword" type="password" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入密码" required>
+          <input id="loginPassword" type="password" autocomplete="new-password" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入密码" required>
         </div>
         <div id="loginError" style="display: none; padding: 10px; background: #fff2f0; border: 1px solid #ffccc7; border-radius: 4px; color: #cf1322; font-size: 14px; margin-bottom: 16px;"></div>
         <button class="btn-primary" onclick="doLogin()">登录</button>
@@ -1144,11 +1304,20 @@
 
             // Check if student has applications
             const applications = await apiGetApplications();
-            if (applications.results && applications.results.length > 0) {
+            const hasApplications = applications.results && applications.results.length > 0;
+            const hasActiveApplication = hasApplications && applications.results.some(app =>
+              app.status.startsWith('pending_') || app.status === 'approved'
+            );
+
+            if (hasActiveApplication) {
               showScreen(1); // Show application progress
               loadMyApplications();
             } else {
-              showScreen(0); // Show application form
+              showScreen(0); // Show application form (allow submit if no active application)
+              if (hasApplications) {
+                // Show info banner if has rejected applications
+                showRejectedApplicationBanner();
+              }
             }
           } else {
             showScreen(1); // Approval list screen

exec
/bin/bash -lc "rtk nl -ba demo-web/index.html | sed -n '220,520p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   220	                listContainer.innerHTML = htmlStr;
   221	            }
   222	
   223	            // Update offset to current position
   224	            approvalOffset = currentOffset;
   225	
   226	            // Check if there's more data to load
   227	            // Has more if: we haven't displayed all accumulated results, or there's more data in API
   228	            approvalHasMore = (accumulatedResults.length > TARGET_COUNT) || (currentOffset < totalCount);
   229	
   230	            if (loadMoreBtn) {
   231	                loadMoreBtn.style.display = approvalHasMore ? 'block' : 'none';
   232	            }
   233	        } else {
   234	            if (!append) {
   235	                listContainer.innerHTML = '<div style="text-align:center; padding: 20px; color:#999;">暂无数据</div>';
   236	            }
   237	            if (loadMoreBtn) {
   238	                loadMoreBtn.style.display = 'none';
   239	            }
   240	        }
   241	    }
   242	
   243	    function filterApprovals(filter) {
   244	        currentFilter = filter;
   245	
   246	        // Update tab active state
   247	        const tabs = document.querySelectorAll('#approval-tabs .nav-tab');
   248	        tabs.forEach((tab, index) => {
   249	            tab.classList.remove('active');
   250	            if ((filter === 'all' && index === 0) ||
   251	                (filter === 'pending' && index === 1) ||
   252	                (filter === 'decided' && index === 2)) {
   253	                tab.classList.add('active');
   254	            }
   255	        });
   256	
   257	        // Reload list with filter
   258	        if (currentUser && currentUser.role === 'student') {
   259	            loadMyApplications();
   260	        } else {
   261	            loadApprovals();
   262	        }
   263	    }
   264	
   265	    let currentApprovalId = null;
   266	    async function showApplicationDetail(applicationId) {
   267	        // Student view: show application detail with approval history
   268	        showScreen(2);
   269	
   270	        const appRes = await fetch(API_BASE_URL + '/applications/' + applicationId + '/', {
   271	            headers: getAuthHeaders()
   272	        });
   273	
   274	        if (!appRes.ok) {
   275	            document.querySelector('#screen-2').innerHTML = '<div class="card"><p style="color: #ff4d4f;">加载失败</p></div>';
   276	            return;
   277	        }
   278	
   279	        const appData = await appRes.json();
   280	        const attachments = await apiGetAttachments(applicationId);
   281	
   282	        // Fetch approval records
   283	        const approvalsRes = await fetch(API_BASE_URL + '/approvals/?application_id=' + applicationId, {
   284	            headers: getAuthHeaders()
   285	        });
   286	        const approvalsData = approvalsRes.ok ? await approvalsRes.json() : { results: [] };
   287	
   288	        const container = document.querySelector('#screen-2');
   289	
   290	        const basicInfoHtml = '<div class="card">' +
   291	            '<div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">基本信息</div>' +
   292	            '<div style="display: flex; margin-bottom: 8px;">' +
   293	              '<span style="font-size: 14px; color: #999; width: 80px;">申请ID:</span>' +
   294	              '<span style="font-size: 14px; color: #333;">' + (appData.application_id || '-') + '</span>' +
   295	            '</div>' +
   296	            '<div style="display: flex; margin-bottom: 8px;">' +
   297	              '<span style="font-size: 14px; color: #999; width: 80px;">学生姓名:</span>' +
   298	              '<span style="font-size: 14px; color: #333;">' + (appData.student_name || '-') + '</span>' +
   299	            '</div>' +
   300	            '<div style="display: flex; margin-bottom: 8px;">' +
   301	              '<span style="font-size: 14px; color: #999; width: 80px;">联系电话:</span>' +
   302	              '<span style="font-size: 14px; color: #333;">' + (appData.contact_phone || '-') + '</span>' +
   303	            '</div>' +
   304	            '<div style="display: flex; margin-bottom: 8px;">' +
   305	              '<span style="font-size: 14px; color: #999; width: 80px;">离校日期:</span>' +
   306	              '<span style="font-size: 14px; color: #333;">' + (appData.leave_date || '-') + '</span>' +
   307	            '</div>' +
   308	            '<div style="display: flex; margin-bottom: 8px;">' +
   309	              '<span style="font-size: 14px; color: #999; width: 80px;">离校原因:</span>' +
   310	              '<span style="font-size: 14px; color: #333;">' + (appData.reason || '-') + '</span>' +
   311	            '</div>' +
   312	          '</div>';
   313	
   314	        const attachmentsHtml = '<div class="card">' +
   315	            '<div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">附件材料</div>' +
   316	            (attachments && attachments.length > 0
   317	                ? attachments.map(att =>
   318	                    '<div style="display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid #f0f0f0;">' +
   319	                      '<span style="flex: 1; font-size: 14px; color: #333;">' + att.filename + '</span>' +
   320	                      '<button class="btn-outline" style="padding: 4px 12px; font-size: 13px;" onclick="previewAttachment(\'' + att.attachment_id + '\')">预览</button>' +
   321	                    '</div>'
   322	                  ).join('')
   323	                : '<div style="color: #999; font-size: 14px;">无附件</div>') +
   324	          '</div>';
   325	
   326	        const approvalProgressHtml = renderStudentApprovalProgress(appData, approvalsData.results);
   327	
   328	        container.innerHTML = basicInfoHtml + attachmentsHtml + approvalProgressHtml +
   329	            '<div style="padding: 20px;"><button class="btn-outline" onclick="showScreen(1); loadMyApplications();" style="width: 100%;">返回</button></div>';
   330	    }
   331	
   332	    function renderStudentApprovalProgress(appData, approvals) {
   333	        const stepNames = {
   334	            'dorm_manager': '宿管员审批',
   335	            'counselor': '辅导员审批',
   336	            'dean': '学工部审批'
   337	        };
   338	
   339	        const workflow = ['dorm_manager', 'counselor', 'dean'];
   340	        const appStatus = appData.status;
   341	
   342	        let html = '<div class="card"><div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">审批进度</div>';
   343	
   344	        for (let i = workflow.length - 1; i >= 0; i--) {
   345	            const step = workflow[i];
   346	            const stepName = stepNames[step];
   347	            const approval = approvals.find(a => a.step === step);
   348	
   349	            let state, tagText, tagCls, dotBg, dotBorder;
   350	
   351	            if (appStatus === 'rejected' && approval && approval.decision === 'rejected') {
   352	                state = 'rejected';
   353	                tagText = '已驳回';
   354	                tagCls = 'tag-rejected';
   355	                dotBg = 'var(--status-error)';
   356	                dotBorder = 'var(--status-error)';
   357	            } else if (approval && approval.decision === 'approved') {
   358	                state = 'approved';
   359	                tagText = '已通过';
   360	                tagCls = 'tag-approved';
   361	                dotBg = 'var(--status-success)';
   362	                dotBorder = 'var(--status-success)';
   363	            } else if (appStatus === 'pending_' + step) {
   364	                state = 'pending';
   365	                tagText = '待审批';
   366	                tagCls = 'tag-pending';
   367	                dotBg = 'white';
   368	                dotBorder = 'var(--primary-color)';
   369	            } else {
   370	                state = 'future';
   371	                tagText = '未开始';
   372	                tagCls = 'tag';
   373	                dotBg = '#e8e8e8';
   374	                dotBorder = '#e8e8e8';
   375	            }
   376	
   377	            html += '<div style="position: relative; padding-left: 30px; margin-bottom: 20px;">' +
   378	                '<div style="position: absolute; left: 10px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: ' + dotBg + '; border: 2px solid ' + dotBorder + ';"></div>' +
   379	                '<div style="margin-bottom: 6px;"><span style="font-size: 15px; font-weight: 600;">' + stepName + '</span> <span class="tag ' + tagCls + '">' + tagText + '</span></div>';
   380	
   381	            if (approval) {
   382	                html += '<div style="font-size: 13px; color: #666;">审批人: ' + (approval.approver_name || '待分配') + '</div>';
   383	                if (approval.decided_at) {
   384	                    html += '<div style="font-size: 13px; color: #666;">时间: ' + new Date(approval.decided_at).toLocaleString() + '</div>';
   385	                }
   386	                if (state === 'rejected') {
   387	                    const comment = approval.comment && approval.comment.trim() ? approval.comment : '审批人未填写驳回原因';
   388	                    html += '<div style="font-size: 13px; color: #ff4d4f; margin-top: 4px; font-weight: 600;">驳回原因: ' + comment + '</div>';
   389	                } else if (approval.comment && approval.comment.trim()) {
   390	                    html += '<div style="font-size: 13px; color: #666; margin-top: 4px;">意见: ' + approval.comment + '</div>';
   391	                }
   392	            }
   393	
   394	            html += '</div>';
   395	        }
   396	
   397	        html += '</div>';
   398	        return html;
   399	    }
   400	
   401	    async function openApproval(id) {
   402	        currentApprovalId = id;
   403	        showScreen(2);
   404	
   405	        const res = await fetch(API_BASE_URL + '/approvals/' + id + '/', {
   406	            headers: getAuthHeaders()
   407	        });
   408	        if (res.ok) {
   409	            const detail = await res.json();
   410	
   411	            const appRes = await fetch(API_BASE_URL + '/applications/' + detail.application_id + '/', {
   412	                headers: getAuthHeaders()
   413	            });
   414	            const appData = appRes.ok ? await appRes.json() : null;
   415	
   416	            // Fetch attachments
   417	            const attachments = await apiGetAttachments(detail.application_id);
   418	
   419	            const container = document.querySelector('#screen-2');
   420	
   421	            const basicInfoHtml = '<div class="card">' +
   422	                '<div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">基本信息</div>' +
   423	                '<div style="display: flex; margin-bottom: 8px;">' +
   424	                  '<span style="font-size: 14px; color: #999; width: 80px;">申请ID:</span>' +
   425	                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.application_id || detail.id.substring(0,8)) + '</span>' +
   426	                '</div>' +
   427	                '<div style="display: flex; margin-bottom: 8px;">' +
   428	                  '<span style="font-size: 14px; color: #999; width: 80px;">学生:</span>' +
   429	                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.student_name || '-') + ' (' + (detail.student_id || '-') + ')</span>' +
   430	                '</div>' +
   431	                '<div style="display: flex; margin-bottom: 8px;">' +
   432	                  '<span style="font-size: 14px; color: #999; width: 80px;">联系电话:</span>' +
   433	                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.contact_phone || '-') + '</span>' +
   434	                '</div>' +
   435	                '<div style="display: flex; margin-bottom: 8px;">' +
   436	                  '<span style="font-size: 14px; color: #999; width: 80px;">离校日期:</span>' +
   437	                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.leave_date || '-') + '</span>' +
   438	                '</div>' +
   439	                '<div style="display: flex; margin-bottom: 8px;">' +
   440	                  '<span style="font-size: 14px; color: #999; width: 80px;">楼栋号:</span>' +
   441	                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.building || '-') + '</span>' +
   442	                '</div>' +
   443	                '<div style="display: flex; margin-bottom: 8px;">' +
   444	                  '<span style="font-size: 14px; color: #999; width: 80px;">房间号:</span>' +
   445	                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.room_number || '-') + '</span>' +
   446	                '</div>' +
   447	                '<div style="display: flex; margin-bottom: 8px;">' +
   448	                  '<span style="font-size: 14px; color: #999; width: 80px;">申请原因:</span>' +
   449	                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.reason || '无') + '</span>' +
   450	                '</div>' +
   451	              '</div>';
   452	
   453	            // Generate attachment HTML - hide download for counselor/dorm_manager
   454	            let attachmentHtml = '';
   455	            if (attachments && attachments.length > 0) {
   456	                const showDownload = currentUser && (currentUser.role === 'dean' || currentUser.role === 'admin');
   457	                attachmentHtml = '<div class="card"><div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">附件材料</div>';
   458	                attachments.forEach(att => {
   459	                    attachmentHtml += '<div style="display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid #f0f0f0;">' +
   460	                        '<span style="font-size: 14px; color: #333; flex: 1;">' + att.file_name + ' (' + (att.file_size / 1024).toFixed(2) + ' KB)</span>' +
   461	                        '<button onclick="handleAttachmentPreview(\'' + att.attachment_id + '\')" style="font-size: 14px; color: var(--primary-color); background: none; border: none; cursor: pointer; margin-right: 12px;">预览</button>' +
   462	                        (showDownload ? '<button onclick="handleAttachmentDownload(\'' + att.attachment_id + '\', \'' + att.file_name + '\')" style="font-size: 14px; color: var(--primary-color); background: none; border: none; cursor: pointer;">下载</button>' : '') +
   463	                    '</div>';
   464	                });
   465	                attachmentHtml += '</div>';
   466	            }
   467	
   468	            // 动态生成审批时间轴
   469	            const timelineHtml = generateTimeline(detail, appData);
   470	
   471	            const cards = container.querySelectorAll('.card');
   472	            if (cards.length > 0) {
   473	                cards[0].outerHTML = basicInfoHtml;
   474	            }
   475	            if (cards.length > 1) {
   476	                if (attachmentHtml) {
   477	                    cards[1].outerHTML = attachmentHtml + timelineHtml;
   478	                } else {
   479	                    cards[1].outerHTML = timelineHtml;
   480	                }
   481	            }
   482	        }
   483	    }
   484	
   485	    function generateTimeline(detail, appData) {
   486	        const stepNames = {
   487	            'dorm_manager': '宿管员审批',
   488	            'counselor': '辅导员审批',
   489	            'dean': '学工部审批'
   490	        };
   491	
   492	        const appStatus = appData ? appData.status : detail.step;
   493	
   494	        // Filter workflow based on current user role
   495	        let workflow = ['dorm_manager', 'counselor', 'dean'];
   496	        if (currentUser && currentUser.role === 'dorm_manager') {
   497	            workflow = ['dorm_manager'];
   498	        } else if (currentUser && currentUser.role === 'counselor') {
   499	            workflow = ['dorm_manager', 'counselor'];
   500	        }
   501	        // dean/admin sees all steps (default)
   502	
   503	        // Calculate current level index
   504	        let currentLevel;
   505	        if (appStatus === 'approved') {
   506	            currentLevel = workflow.length;
   507	        } else if (appStatus === 'rejected') {
   508	            currentLevel = workflow.indexOf(detail.step);
   509	        } else if (appStatus.startsWith('pending_')) {
   510	            const pendingStep = appStatus.replace('pending_', '');
   511	            currentLevel = workflow.indexOf(pendingStep);
   512	        } else {
   513	            currentLevel = -1;
   514	        }
   515	
   516	        let html = '<div class="card"><div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">审批记录</div>';
   517	
   518	        for (let i = workflow.length - 1; i >= 0; i--) {
   519	            const step = workflow[i];
   520	            const stepName = stepNames[step];

exec
/bin/bash -lc "rtk nl -ba apps/approvals/serializers.py | sed -n '1,260p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
nl: apps/approvals/serializers.py: No such file or directory

exec
/bin/bash -lc "rtk nl -ba demo-web/index.html | sed -n '1,220p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	<!DOCTYPE html>
     2	<html lang="zh-CN">
     3	<head>
     4	  <meta charset="UTF-8">
     5	  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
     6	  <title>毕业离校申请系统 - UI Demo</title>
     7	  <link rel="stylesheet" href="css/global.css">
     8	  <script src="js/api.js?v=20260610-1650"></script>
     9	<script>
    10	    let currentFilter = 'all';
    11	    let approvalOffset = 0;
    12	    let approvalHasMore = true;
    13	    let deanDisplayedApps = new Set(); // Track displayed application IDs for dean deduplication
    14	    // currentUser is declared in api.js
    15	
    16	    // HTML escape helper to prevent XSS
    17	    function escapeHtml(text) {
    18	        if (!text) return '';
    19	        const div = document.createElement('div');
    20	        div.textContent = text;
    21	        return div.innerHTML;
    22	    }
    23	
    24	    async function loadMyApplications() {
    25	        if (!currentToken) return;
    26	        const data = await apiGetApplications();
    27	        const listContainer = document.getElementById('approval-list-container');
    28	
    29	        if (data.results && data.results.length > 0) {
    30	            // Apply filter
    31	            let filtered = data.results;
    32	            if (currentFilter === 'pending') {
    33	                filtered = data.results.filter(a => a.status && a.status.startsWith('pending_'));
    34	            } else if (currentFilter === 'decided') {
    35	                filtered = data.results.filter(a => a.status === 'approved' || a.status === 'rejected');
    36	            }
    37	
    38	            let htmlStr = '';
    39	            filtered.forEach(app => {
    40	                const statusDisplay = getStatusDisplay(app.status);
    41	                const appIdDisplay = app.application_id ? app.application_id.substring(0,8) : '未知';
    42	                htmlStr += '<div class="card" style="cursor: pointer;" onclick="showApplicationDetail(\'' + app.application_id + '\')">' +
    43	                  '<div class="flex-row justify-between align-center" style="margin-bottom: 8px;">' +
    44	                    '<span style="font-size: 16px; font-weight: bold;">申请 ' + appIdDisplay + '</span>' +
    45	                    '<span class="tag ' + statusDisplay.class + '">' + statusDisplay.text + '</span>' +
    46	                  '</div>' +
    47	                  '<div style="margin-bottom: 4px;">' +
    48	                    '<span style="font-size: 14px; color: #999; margin-right: 8px;">离校日期:</span>' +
    49	                    '<span style="font-size: 14px; color: #333;">' + (app.leave_date || '-') + '</span>' +
    50	                  '</div>' +
    51	                  '<div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #f0f0f0;">' +
    52	                    '<span style="font-size: 12px; color: #999;">' + new Date(app.created_at).toLocaleString() + '</span>' +
    53	                  '</div>' +
    54	                '</div>';
    55	            });
    56	            listContainer.innerHTML = htmlStr;
    57	        } else {
    58	            listContainer.innerHTML = '<div style="text-align:center; padding: 20px; color:#999;">暂无申请记录</div>';
    59	        }
    60	    }
    61	
    62	    async function loadApprovals(append = false) {
    63	        console.log('[DEBUG] loadApprovals called, append=', append, 'currentToken=', currentToken);
    64	        if (!currentToken) return;
    65	
    66	        if (!append) {
    67	            approvalOffset = 0;
    68	            approvalHasMore = true;
    69	            deanDisplayedApps.clear(); // Clear deduplication set on fresh load
    70	        }
    71	
    72	        // Map currentFilter to API decision parameter
    73	        let decision = 'pending';
    74	        if (currentFilter === 'all') {
    75	            decision = 'all';
    76	        } else if (currentFilter === 'decided') {
    77	            decision = 'all'; // Get all, then filter for approved/rejected
    78	        }
    79	
    80	        const listContainer = document.getElementById('approval-list-container');
    81	        const loadMoreBtn = document.getElementById('load-more-approvals');
    82	
    83	        const TARGET_COUNT = 20; // Target number of deduplicated records to display
    84	        const BATCH_SIZE = 20;   // API request batch size
    85	        const MAX_ITERATIONS = 10; // Safety limit to prevent infinite loops
    86	        let accumulatedResults = [];
    87	        let currentOffset = approvalOffset;
    88	        let totalCount = 0;
    89	        let iterations = 0;
    90	
    91	        // Loop until we have TARGET_COUNT deduplicated records or no more data
    92	        while (accumulatedResults.length < TARGET_COUNT && iterations < MAX_ITERATIONS) {
    93	            iterations++;
    94	            const data = await apiGetApprovals(decision, BATCH_SIZE, currentOffset);
    95	            console.log('[DEBUG] apiGetApprovals returned:', data, 'offset:', currentOffset);
    96	
    97	            if (!data || !data.results || data.results.length === 0) {
    98	                // No more data from API
    99	                break;
   100	            }
   101	
   102	            totalCount = data.count;
   103	
   104	            // Apply front-end filter only for 'decided' (approved or rejected)
   105	            let filtered = data.results;
   106	            if (currentFilter === 'decided') {
   107	                filtered = data.results.filter(a => a.decision === 'approved' || a.decision === 'rejected');
   108	                console.log('[DEBUG] Filtered decided count:', filtered.length);
   109	            }
   110	
   111	            // For dean/admin: deduplicate by application_id
   112	            if (currentUser && (currentUser.role === 'dean' || currentUser.role === 'admin')) {
   113	                const beforeCount = filtered.length;
   114	                const newUniqueRecords = [];
   115	                const orphanApprovals = [];
   116	
   117	                filtered.forEach(approval => {
   118	                    const appId = approval.application?.id;
   119	                    if (appId) {
   120	                        if (!deanDisplayedApps.has(appId)) {
   121	                            newUniqueRecords.push(approval);
   122	                            deanDisplayedApps.add(appId); // Track globally across pages
   123	                        }
   124	                    } else {
   125	                        // Keep approvals without application link
   126	                        orphanApprovals.push(approval);
   127	                    }
   128	                });
   129	
   130	                filtered = newUniqueRecords.concat(orphanApprovals);
   131	                console.log('[DEBUG] Dedup: before', beforeCount, '→ after', filtered.length, 'deanDisplayedApps size:', deanDisplayedApps.size);
   132	            }
   133	
   134	            accumulatedResults = accumulatedResults.concat(filtered);
   135	            currentOffset += BATCH_SIZE;
   136	
   137	            // Stop if we've reached the end of available data
   138	            if (currentOffset >= totalCount) {
   139	                break;
   140	            }
   141	        }
   142	
   143	        // Render accumulated results (up to TARGET_COUNT)
   144	        const displayRecords = accumulatedResults.slice(0, TARGET_COUNT);
   145	        console.log('[DEBUG] Displaying', displayRecords.length, 'records, accumulated', accumulatedResults.length);
   146	
   147	        // Status map based on backend expectations
   148	        const statusMap = {
   149	            'pending_dorm_manager': { text: '待宿管审批', cls: 'tag-pending' },
   150	            'pending_counselor': { text: '待辅导员审批', cls: 'tag-pending' },
   151	            'pending_dean': { text: '待学工部审批', cls: 'tag-pending' },
   152	            'approved': { text: '已通过', cls: 'tag-approved' },
   153	            'rejected': { text: '已拒绝', cls: 'tag-rejected' }
   154	        };
   155	
   156	        const decisionMap = {
   157	            'pending': { text: '待审批', cls: 'tag-pending' },
   158	            'approved': { text: '已通过', cls: 'tag-approved' },
   159	            'rejected': { text: '已拒绝', cls: 'tag-rejected' }
   160	        };
   161	
   162	        if (displayRecords.length > 0) {
   163	            let htmlStr = '';
   164	
   165	            displayRecords.forEach(approval => {
   166	                const application = approval.application || {};
   167	
   168	                // Use approval decision for status tag (more accurate for dean/approval views)
   169	                const decision = approval.decision || 'pending';
   170	                const step = decisionMap[decision] ? decisionMap[decision].text : decision;
   171	                const tagCls = decisionMap[decision] ? decisionMap[decision].cls : 'tag-pending';
   172	
   173	                const safeAppId = escapeHtml(application.id || approval.id).substring(0,8);
   174	                const safeStudentName = escapeHtml(application.student_name || '-');
   175	                const safeStudentId = escapeHtml(application.student_id || '-');
   176	
   177	                htmlStr += '<div class="card" onclick="openApproval(\'' + approval.id + '\')" style="cursor: pointer;">' +
   178	                  '<div class="flex-row justify-between align-center" style="margin-bottom: 8px;">' +
   179	                    '<span style="font-size: 16px; font-weight: bold;">申请 ' + safeAppId + '</span>' +
   180	                    '<span class="tag ' + tagCls + '">' + step + '</span>' +
   181	                  '</div>' +
   182	                  '<div style="margin-bottom: 4px;">' +
   183	                    '<span style="font-size: 14px; color: #999; margin-right: 8px;">学生:</span>' +
   184	                    '<span style="font-size: 14px; color: #333;">' + safeStudentName + ' (' + safeStudentId + ')</span>' +
   185	                  '</div>';
   186	
   187	                // Show approver and decision time for decided approvals
   188	                if (approval.decision === 'approved' || approval.decision === 'rejected') {
   189	                    // Extract real approver name from comment if auto-completed
   190	                    let realApprover = approval.approver_name || '-';
   191	                    if (approval.comment && approval.comment.includes('已由')) {
   192	                        const match = approval.comment.match(/已由(.+?)完成审批/);
   193	                        if (match) {
   194	                            realApprover = match[1];
   195	                        }
   196	                    }
   197	                    const safeApprover = escapeHtml(realApprover);
   198	
   199	                    htmlStr += '<div style="margin-bottom: 4px;">' +
   200	                      '<span style="font-size: 14px; color: #999; margin-right: 8px;">审批人:</span>' +
   201	                      '<span style="font-size: 14px; color: #333;">' + safeApprover + '</span>' +
   202	                    '</div>';
   203	                    if (approval.decided_at) {
   204	                        htmlStr += '<div style="margin-bottom: 4px;">' +
   205	                          '<span style="font-size: 14px; color: #999; margin-right: 8px;">审批时间:</span>' +
   206	                          '<span style="font-size: 14px; color: #333;">' + new Date(approval.decided_at).toLocaleString() + '</span>' +
   207	                        '</div>';
   208	                    }
   209	                }
   210	
   211	                htmlStr += '<div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #f0f0f0;">' +
   212	                    '<span style="font-size: 12px; color: #999;">创建: ' + new Date(approval.created_at || application.created_at).toLocaleString() + '</span>' +
   213	                  '</div>' +
   214	                '</div>';
   215	            });
   216	
   217	            if (append) {
   218	                listContainer.innerHTML += htmlStr;
   219	            } else {
   220	                listContainer.innerHTML = htmlStr;

codex
目标后端文件实际在 `backend/apps/approvals/serializers.py`，不是仓库根的 `apps/...`。前端新增的学生详情路径里已经暴露出多处未转义拼接，我会继续把管理员列表、Excel 预览和登出逻辑完整扫完，避免只看新增段落。
exec
/bin/bash -lc 'rtk git log --oneline -8 -- backend/apps/approvals/serializers.py demo-web/index.html' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
7b2fce6 fix(security): 修复XSS漏洞、无限循环风险、内存泄漏
ee5667a fix(backend): ApplicationBriefSerializer添加缺失字段
68d5ea0 fix(demo-web): 修复Excel预览日期显示Invalid Date问题
afd6d9f fix(demo-web): Excel预览状态字段中文化
f532f03 feat(demo-web): 添加Excel导出预览功能
097e0f7 refactor(demo-web): 重构分页逻辑，固定显示20条去重后的记录
ce19e4e fix(demo-web): 修复admin角色审批列表显示问题
99a9173 fix: 修复管理员附件预览按钮不显示问题

exec
/bin/bash -lc "rtk nl -ba demo-web/index.html | sed -n '920,1340p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   920	      display: flex;
   921	      border-bottom: 1px solid #f0f0f0;
   922	      position: sticky;
   923	      top: 0;
   924	      z-index: 10;
   925	    }
   926	    .nav-tab {
   927	      flex: 1;
   928	      text-align: center;
   929	      padding: 12px 0;
   930	      font-size: 14px;
   931	      color: #666;
   932	      cursor: pointer;
   933	      position: relative;
   934	      border: none;
   935	      background: none;
   936	    }
   937	    .nav-tab.active {
   938	      color: var(--primary-color);
   939	      font-weight: 600;
   940	    }
   941	    .nav-tab.active::after {
   942	      content: '';
   943	      position: absolute;
   944	      bottom: 0;
   945	      left: 50%;
   946	      transform: translateX(-50%);
   947	      width: 30px;
   948	      height: 2px;
   949	      background: var(--primary-color);
   950	      border-radius: 1px;
   951	    }
   952	
   953	    /* 响应式：桌面端Tab导航优化 */
   954	    @media (min-width: 1024px) {
   955	      .nav-tabs {
   956	        padding: 0 40px;
   957	      }
   958	      .nav-tab {
   959	        padding: 16px 24px;
   960	        font-size: 16px;
   961	      }
   962	      .nav-tab.active::after {
   963	        width: 50px;
   964	        height: 3px;
   965	      }
   966	    }
   967	
   968	    /* 附件上传区域样式 */
   969	    .upload-area {
   970	      border: 2px dashed #d9d9d9;
   971	      border-radius: 8px;
   972	      padding: 30px;
   973	      text-align: center;
   974	      cursor: pointer;
   975	      transition: all 0.3s;
   976	    }
   977	    .upload-area:hover {
   978	      border-color: var(--primary-color);
   979	      background: #fafafa;
   980	    }
   981	    .file-item {
   982	      display: flex;
   983	      align-items: center;
   984	      justify-content: space-between;
   985	      padding: 10px;
   986	      background: #fafafa;
   987	      border-radius: 4px;
   988	      margin-bottom: 8px;
   989	    }
   990	    .file-info {
   991	      flex: 1;
   992	      margin-left: 8px;
   993	    }
   994	    .file-name {
   995	      font-size: 14px;
   996	      color: #333;
   997	    }
   998	    .file-size {
   999	      font-size: 12px;
  1000	      color: #999;
  1001	    }
  1002	    .btn-delete {
  1003	      background: none;
  1004	      border: none;
  1005	      color: var(--status-error);
  1006	      font-size: 20px;
  1007	      cursor: pointer;
  1008	      padding: 0 8px;
  1009	    }
  1010	
  1011	    .screen {
  1012	      display: none;
  1013	      min-height: calc(100vh - 45px);
  1014	    }
  1015	    .screen.active {
  1016	      display: block;
  1017	    }
  1018	    .login-screen {
  1019	      display: none;
  1020	      min-height: calc(100vh - 45px);
  1021	    }
  1022	    .login-screen.active {
  1023	      display: block;
  1024	    }
  1025	  </style>
  1026	</head>
  1027	<body>
  1028	  <!-- 顶部导航 -->
  1029	  <div class="nav-tabs" id="navTabs" style="display: none;">
  1030	    <button class="nav-tab active" onclick="showScreen(0)">学生申请</button>
  1031	    <button class="nav-tab" onclick="showScreen(1)"><span id="nav-approval-text">审批列表</span></button>
  1032	    <button class="nav-tab" onclick="showScreen(2)" style="display: none;">申请详情</button>
  1033	  </div>
  1034	
  1035	  <!-- 登录状态栏 -->
  1036	  <div id="userBar" style="background: white; padding: 8px 16px; border-bottom: 1px solid #f0f0f0; display: none; align-items: center; justify-content: space-between;">
  1037	    <div>
  1038	      <span style="font-size: 14px; color: #666;">当前用户:</span>
  1039	      <span id="currentUserName" style="font-size: 14px; font-weight: 500; margin-left: 8px;"></span>
  1040	      <span id="currentUserRole" style="font-size: 12px; color: #999; margin-left: 8px;"></span>
  1041	    </div>
  1042	    <button onclick="logout()" style="padding: 4px 12px; border: 1px solid #d9d9d9; border-radius: 4px; background: white; cursor: pointer;">退出登录</button>
  1043	  </div>
  1044	
  1045	  <!-- 登录屏幕 -->
  1046	  <div class="login-screen active" id="screen-login">
  1047	    <div style="padding: 40px 20px; max-width: 400px; margin: 0 auto;">
  1048	      <div class="card">
  1049	        <div style="text-align: center; margin-bottom: 30px;">
  1050	          <h2 style="color: var(--primary-color); margin-bottom: 8px;">毕业离校申请系统</h2>
  1051	          <p style="color: #666; font-size: 14px;">请登录以继续</p>
  1052	        </div>
  1053	        <div style="margin-bottom: 20px;">
  1054	          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">用户ID</label>
  1055	          <input id="loginUserId" type="text" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入用户ID（如 2020001）" required>
  1056	        </div>
  1057	        <div style="margin-bottom: 24px;">
  1058	          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">密码</label>
  1059	          <input id="loginPassword" type="password" autocomplete="new-password" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入密码" required>
  1060	        </div>
  1061	        <div id="loginError" style="display: none; padding: 10px; background: #fff2f0; border: 1px solid #ffccc7; border-radius: 4px; color: #cf1322; font-size: 14px; margin-bottom: 16px;"></div>
  1062	        <button class="btn-primary" onclick="doLogin()">登录</button>
  1063	      </div>
  1064	    </div>
  1065	  </div>
  1066	
  1067	  <div class="screen" id="screen-0">
  1068	    <div style="padding: 20px;">
  1069	      <!-- 用户信息卡片 -->
  1070	      <div class="card" style="margin-bottom: 20px;">
  1071	        <div style="font-size: 16px; font-weight: 600; color: var(--primary-color); margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #f0f0f0;">
  1072	          申请人信息
  1073	        </div>
  1074	        <div style="display: flex; align-items: center; padding: 10px 0;">
  1075	          <span style="font-size: 14px; color: #666; width: 80px;">姓名</span>
  1076	          <span id="studentName" style="font-size: 14px; color: #333;">-</span>
  1077	        </div>
  1078	        <div style="display: flex; align-items: center; padding: 10px 0;">
  1079	          <span style="font-size: 14px; color: #666; width: 80px;">学号</span>
  1080	          <span id="studentId" style="font-size: 14px; color: #333;">-</span>
  1081	        </div>
  1082	        <div style="display: flex; align-items: center; padding: 10px 0;">
  1083	          <span style="font-size: 14px; color: #666; width: 80px;">楼栋号</span>
  1084	          <span id="studentBuilding" style="font-size: 14px; color: #333;">-</span>
  1085	        </div>
  1086	        <div style="display: flex; align-items: center; padding: 10px 0;">
  1087	          <span style="font-size: 14px; color: #666; width: 80px;">房间号</span>
  1088	          <span id="studentRoom" style="font-size: 14px; color: #333;">-</span>
  1089	        </div>
  1090	      </div>
  1091	
  1092	      <!-- 表单卡片 -->
  1093	      <div class="card">
  1094	        <div style="margin-bottom: 20px;">
  1095	          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">联系电话</label>
  1096	          <input id="contactPhone" type="tel" name="contact_phone" maxlength="20" inputmode="numeric" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入联系电话" required>
  1097	        </div>
  1098	        <div style="margin-bottom: 20px;">
  1099	          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">离校原因</label>
  1100	          <textarea id="applicationReason" style="width: 100%; min-height: 120px; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入离校原因"></textarea>
  1101	          <span style="display: block; text-align: right; font-size: 12px; color: #999; margin-top: 4px;">0/500</span>
  1102	        </div>
  1103	        <div style="margin-bottom: 20px;">
  1104	          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">离校日期</label>
  1105	          <input id="leaveDate" type="date" name="leave_date" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" required>
  1106	        </div>
  1107	
  1108	        <!-- 附件上传区域 -->
  1109	        <div style="margin-bottom: 20px;">
  1110	          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">附件材料（必需）</label>
  1111	          <div class="upload-zone">
  1112	            <input type="file" id="fileInput" multiple accept=".jpg,.jpeg,.png,.pdf,.doc,.docx" style="display: none;">
  1113	            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
  1114	              <div style="font-size: 40px; color: #999; margin-bottom: 8px;">📎</div>
  1115	              <div style="font-size: 14px; color: #666;">点击或拖拽文件到此处上传</div>
  1116	              <div style="font-size: 12px; color: #999; margin-top: 4px;">支持jpg/png/pdf/doc/docx，单文件不超过10MB</div>
  1117	            </div>
  1118	          </div>
  1119	          <!-- 文件列表 -->
  1120	          <div id="fileList" style="margin-top: 12px;"></div>
  1121	        </div>
  1122	
  1123	        <button class="btn-primary" onclick="doSubmitApplication()">提交申请</button>
  1124	      </div>
  1125	    </div>
  1126	  </div>
  1127	
  1128	  <!-- 屏幕2: 审批列表页 -->
  1129	  <div class="screen" id="screen-1">
  1130	    <div style="background: white; padding: 16px; display: flex; justify-content: space-between; align-items: center;">
  1131	      <div style="font-size: 18px; font-weight: bold;" id="list-title">审批列表</div>
  1132	      <div style="display: flex; align-items: center; gap: 12px;">
  1133	        <button id="export-btn" onclick="exportApprovals()" style="display: none; padding: 8px 16px; background: var(--primary-color); color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px;">导出Excel</button>
  1134	        <div style="font-size: 12px; color: #999;" id="role-display">宿管员</div>
  1135	      </div>
  1136	    </div>
  1137	
  1138	    <!-- Tab切换 -->
  1139	    <div style="background: white; display: flex; border-bottom: 1px solid #f0f0f0;" id="approval-tabs">
  1140	      <div class="nav-tab active" style="flex: 1;" onclick="filterApprovals('all')">全部</div>
  1141	      <div class="nav-tab" style="flex: 1;" onclick="filterApprovals('pending')">待审批</div>
  1142	      <div class="nav-tab" style="flex: 1;" onclick="filterApprovals('decided')">已审批</div>
  1143	    </div>
  1144	
  1145	    <div style="padding: 10px;" id="approval-list-container">
  1146	      <!-- 列表项 -->
  1147	      <div style="text-align:center; padding: 20px; color:#999;">加载中...</div>
  1148	    </div>
  1149	    <div style="padding: 10px; text-align: center;">
  1150	      <button id="load-more-approvals" onclick="loadApprovals(true)" style="display: none; padding: 10px 20px; border: 1px solid var(--primary-color); background: white; color: var(--primary-color); border-radius: 4px; cursor: pointer;">加载更多</button>
  1151	    </div>
  1152	  </div>
  1153	
  1154	  <!-- 屏幕3: 申请详情页 -->
  1155	  <div class="screen" id="screen-2">
  1156	    <div style="background: white; padding: 16px; display: flex; align-items: center; gap: 12px;">
  1157	      <button onclick="showScreen(1)" style="border: none; background: none; font-size: 20px; cursor: pointer; color: var(--primary-color); padding: 0;">←</button>
  1158	      <div style="font-size: 18px; font-weight: bold;">申请详情</div>
  1159	    </div>
  1160	
  1161	    <div style="padding: 10px;">
  1162	      <!-- 基本信息 -->
  1163	      <div class="card">
  1164	        <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">基本信息</div>
  1165	        <div style="display: flex; margin-bottom: 8px;">
  1166	          <span style="font-size: 14px; color: #999; width: 80px;">申请ID:</span>
  1167	          <span style="font-size: 14px; color: #333; flex: 1;">-</span>
  1168	        </div>
  1169	        <div style="display: flex; margin-bottom: 8px;">
  1170	          <span style="font-size: 14px; color: #999; width: 80px;">学生:</span>
  1171	          <span style="font-size: 14px; color: #333; flex: 1;">-</span>
  1172	        </div>
  1173	        <div style="display: flex; margin-bottom: 8px;">
  1174	          <span style="font-size: 14px; color: #999; width: 80px;">离校日期:</span>
  1175	          <span style="font-size: 14px; color: #333; flex: 1;">-</span>
  1176	        </div>
  1177	        <div style="display: flex; margin-bottom: 8px;">
  1178	          <span style="font-size: 14px; color: #999; width: 80px;">申请原因:</span>
  1179	          <span style="font-size: 14px; color: #333; flex: 1;">-</span>
  1180	        </div>
  1181	      </div>
  1182	
  1183	      <!-- 审批记录时间轴 -->
  1184	      <div class="card">
  1185	        <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">审批记录</div>
  1186	
  1187	        <!-- 时间轴项 -->
  1188	        <div style="position: relative; padding-left: 30px; margin-bottom: 20px;">
  1189	          <div style="position: absolute; left: 10px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: white; border: 2px solid var(--primary-color);"></div>
  1190	          <div style="position: absolute; left: 14px; top: 16px; bottom: -20px; width: 1px; background: #e8e8e8;"></div>
  1191	          <div class="flex-row justify-between align-center" style="margin-bottom: 6px;">
  1192	            <span style="font-size: 15px; font-weight: 600;">宿管员审批</span>
  1193	            <span class="tag tag-pending">待审批</span>
  1194	          </div>
  1195	          <div style="font-size: 13px; color: #666;">审批人: 李老师</div>
  1196	        </div>
  1197	
  1198	        <div style="position: relative; padding-left: 30px; margin-bottom: 20px;">
  1199	          <div style="position: absolute; left: 10px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--status-success); border: 2px solid var(--status-success);"></div>
  1200	          <div class="flex-row justify-between align-center" style="margin-bottom: 6px;">
  1201	            <span style="font-size: 15px; font-weight: 600;">提交申请</span>
  1202	            <span class="tag tag-approved">已完成</span>
  1203	          </div>
  1204	          <div style="font-size: 13px; color: #666;">提交时间: 2024-06-01 10:30</div>
  1205	        </div>
  1206	      </div>
  1207	
  1208	      <!-- 审批操作 -->
  1209	      <div id="approval-section" style="padding: 10px;">
  1210	        <div class="card" style="margin-bottom: 10px;">
  1211	          <label style="display: block; font-size: 14px; color: #333; margin-bottom: 6px; font-weight: 500;">审批意见（可选）</label>
  1212	          <textarea id="approvalComment" style="width: 100%; min-height: 60px; padding: 8px; border: 1px solid #e8e8e8; border-radius: 4px; font-size: 14px;" placeholder="请输入审批意见"></textarea>
  1213	          <span style="display: block; text-align: right; font-size: 12px; color: #999; margin-top: 4px;">0/200</span>
  1214	        </div>
  1215	        <div style="display: flex; gap: 10px;" id="approval-actions">
  1216	          <button class="btn-primary" style="flex: 1;" onclick="doApprove()">通过</button>
  1217	          <button class="btn-outline" style="flex: 1;" onclick="doReject()">拒绝</button>
  1218	        </div>
  1219	      </div>
  1220	    </div>
  1221	  </div>
  1222	
  1223	  <script>
  1224	    // Status mapping
  1225	    const statusMap = {
  1226	      'pending_dorm_manager': { text: '待宿管审批', class: 'tag-pending' },
  1227	      'pending_counselor': { text: '待辅导员审批', class: 'tag-pending' },
  1228	      'pending_dean': { text: '待学工部审批', class: 'tag-pending' },
  1229	      'approved': { text: '已通过', class: 'tag-approved' },
  1230	      'rejected': { text: '已拒绝', class: 'tag-rejected' }
  1231	    };
  1232	
  1233	    function getStatusDisplay(status) {
  1234	      return statusMap[status] || { text: status, class: 'tag' };
  1235	    }
  1236	
  1237	    function showScreen(index) {
  1238	      document.querySelectorAll('.screen').forEach((s, i) => {
  1239	        s.classList.toggle('active', i === index);
  1240	      });
  1241	      document.querySelectorAll('.nav-tabs .nav-tab').forEach((t, i) => {
  1242	        t.classList.toggle('active', i === index);
  1243	      });
  1244	    }
  1245	
  1246	    async function doLogin() {
  1247	      const userId = document.getElementById('loginUserId').value.trim();
  1248	      const password = document.getElementById('loginPassword').value.trim();
  1249	      const errorEl = document.getElementById('loginError');
  1250	      const btn = event?.target || document.querySelector('#screen-login .btn-primary');
  1251	
  1252	      if (!userId || !password) {
  1253	        errorEl.textContent = '请输入用户ID和密码';
  1254	        errorEl.style.display = 'block';
  1255	        return;
  1256	      }
  1257	
  1258	      // Loading state
  1259	      const originalText = btn.textContent;
  1260	      btn.disabled = true;
  1261	      btn.textContent = '登录中...';
  1262	
  1263	      try {
  1264	        const result = await apiLogin(userId, password);
  1265	
  1266	        if (result.success) {
  1267	          errorEl.style.display = 'none';
  1268	          document.getElementById('loginUserId').value = '';
  1269	          document.getElementById('loginPassword').value = '';
  1270	
  1271	          // Show nav tabs and user bar
  1272	          document.getElementById('navTabs').style.display = 'flex';
  1273	          document.getElementById('userBar').style.display = 'flex';
  1274	          document.getElementById('currentUserName').textContent = result.user.name;
  1275	
  1276	          // Store current user for role-based UI control
  1277	          currentUser = result.user;
  1278	
  1279	          const roleMap = {
  1280	            'student': '学生',
  1281	            'dorm_manager': '宿管员',
  1282	            'counselor': '辅导员',
  1283	            'dean': '学工部'
  1284	          };
  1285	          document.getElementById('currentUserRole').textContent = '(' + (roleMap[result.user.role] || result.user.role) + ')';
  1286	
  1287	          // Update UI based on role
  1288	          updateUIForRole(result.user.role);
  1289	
  1290	          // Hide login screen
  1291	          document.getElementById('screen-login').classList.remove('active');
  1292	
  1293	          // Route based on role and application status
  1294	          if (result.user.role === 'student') {
  1295	            document.getElementById('studentName').textContent = result.user.name;
  1296	            document.getElementById('studentId').textContent = result.user.user_id;
  1297	            document.getElementById('studentBuilding').textContent = result.user.building || '-';
  1298	            document.getElementById('studentRoom').textContent = result.user.room_number || '-';
  1299	
  1300	            // Pre-fill phone if available
  1301	            if (result.user.phone) {
  1302	              document.getElementById('contactPhone').value = result.user.phone;
  1303	            }
  1304	
  1305	            // Check if student has applications
  1306	            const applications = await apiGetApplications();
  1307	            const hasApplications = applications.results && applications.results.length > 0;
  1308	            const hasActiveApplication = hasApplications && applications.results.some(app =>
  1309	              app.status.startsWith('pending_') || app.status === 'approved'
  1310	            );
  1311	
  1312	            if (hasActiveApplication) {
  1313	              showScreen(1); // Show application progress
  1314	              loadMyApplications();
  1315	            } else {
  1316	              showScreen(0); // Show application form (allow submit if no active application)
  1317	              if (hasApplications) {
  1318	                // Show info banner if has rejected applications
  1319	                showRejectedApplicationBanner();
  1320	              }
  1321	            }
  1322	          } else {
  1323	            showScreen(1); // Approval list screen
  1324	            loadApprovals();
  1325	          }
  1326	        } else {
  1327	          errorEl.textContent = result.error.error || '登录失败，请检查用户ID和密码';
  1328	          errorEl.style.display = 'block';
  1329	        }
  1330	      } finally {
  1331	        btn.disabled = false;
  1332	        btn.textContent = originalText;
  1333	      }
  1334	    }
  1335	
  1336	    function updateUIForRole(role) {
  1337	      const isStudent = role === 'student';
  1338	      const isDean = role === 'dean';
  1339	      const isAdmin = role === 'admin';
  1340	

exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/serializers.py | sed -n '1,320p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import serializers
     2	from .models import Approval
     3	
     4	
     5	class ApplicationBriefSerializer(serializers.Serializer):
     6	    """Brief application info for approval list"""
     7	    id = serializers.CharField(source='application_id')
     8	    status = serializers.CharField()
     9	    student_name = serializers.CharField(source='student.name')
    10	    student_id = serializers.CharField(source='student.user_id')
    11	    contact_phone = serializers.CharField(allow_null=True)
    12	    leave_date = serializers.DateField()
    13	    building = serializers.CharField(source='student.building', allow_null=True)
    14	    room_number = serializers.CharField(source='student.room_number', allow_null=True)
    15	    created_at = serializers.DateTimeField()
    16	
    17	
    18	class ApprovalListSerializer(serializers.ModelSerializer):
    19	    """Lean serializer for approval lists - nested application structure"""
    20	    id = serializers.CharField(source='approval_id', read_only=True)
    21	    application = ApplicationBriefSerializer(read_only=True)
    22	    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
    23	
    24	    class Meta:
    25	        model = Approval
    26	        fields = ['id', 'application', 'step', 'approver_id',
    27	                  'approver_name', 'decision', 'comment', 'decided_at', 'created_at']
    28	        read_only_fields = ['id', 'step', 'approver_id',
    29	                            'approver_name', 'decision', 'comment', 'decided_at', 'created_at']
    30	
    31	
    32	class ApprovalBriefSerializer(serializers.ModelSerializer):
    33	    """Brief approval info without attachments - for nested use in ApplicationSerializer"""
    34	    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
    35	    decided_by_id = serializers.CharField(source='decided_by.user_id', read_only=True, allow_null=True)
    36	    decided_by_name = serializers.CharField(source='decided_by.name', read_only=True, allow_null=True)
    37	
    38	    class Meta:
    39	        model = Approval
    40	        fields = ['approval_id', 'step', 'approver_id', 'approver_name',
    41	                  'decided_by_id', 'decided_by_name', 'decision', 'comment', 'decided_at']
    42	        read_only_fields = fields
    43	
    44	
    45	class ApprovalSerializer(serializers.ModelSerializer):
    46	    """Full approval detail with nested application info"""
    47	    application_id = serializers.CharField(source='application.application_id', read_only=True)
    48	    student_name = serializers.CharField(source='application.student.name', read_only=True)
    49	    student_id = serializers.CharField(source='application.student.user_id', read_only=True)
    50	    contact_phone = serializers.CharField(source='application.contact_phone', read_only=True)
    51	    reason = serializers.CharField(source='application.reason', read_only=True)
    52	    leave_date = serializers.DateField(source='application.leave_date', read_only=True)
    53	    building = serializers.CharField(source='application.student.building', read_only=True, allow_null=True)
    54	    room_number = serializers.CharField(source='application.student.room_number', read_only=True, allow_null=True)
    55	    attachments = serializers.SerializerMethodField()
    56	    approver_id = serializers.CharField(source='approver.user_id', read_only=True)
    57	    decided_by_id = serializers.CharField(source='decided_by.user_id', read_only=True, allow_null=True)
    58	    decided_by_name = serializers.CharField(source='decided_by.name', read_only=True, allow_null=True)
    59	
    60	    class Meta:
    61	        model = Approval
    62	        fields = ['approval_id', 'application_id', 'student_name', 'student_id',
    63	                  'contact_phone', 'reason', 'leave_date', 'building', 'room_number',
    64	                  'attachments', 'step', 'approver_id',
    65	                  'approver_name', 'decided_by_id', 'decided_by_name', 'decision', 'comment', 'decided_at']
    66	        read_only_fields = ['approval_id', 'application_id', 'student_name', 'student_id',
    67	                            'contact_phone', 'reason', 'leave_date', 'building', 'room_number',
    68	                            'attachments', 'step',
    69	                            'approver_id', 'approver_name', 'decided_by_id', 'decided_by_name', 'decision', 'decided_at']
    70	
    71	    def get_attachments(self, obj):
    72	        from apps.attachments.serializers import AttachmentSerializer
    73	        return AttachmentSerializer(
    74	            obj.application.attachments.filter(is_deleted=False),
    75	            many=True
    76	        ).data
    77	
    78	
    79	class ApprovalActionSerializer(serializers.Serializer):
    80	    comment = serializers.CharField(required=False, allow_blank=True)
    81	
    82	
    83	class ApprovalListResponseSerializer(serializers.Serializer):
    84	    """Schema-only: approval list response with pagination"""
    85	    count = serializers.IntegerField()
    86	    results = ApprovalListSerializer(many=True)

exec
/bin/bash -lc "rtk nl -ba demo-web/index.html | sed -n '520,920p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   520	            const stepName = stepNames[step];
   521	            const isLast = i === 0;
   522	
   523	            let state, tagText, tagCls, dotBg, dotBorder, showConnector;
   524	
   525	            // Check if this is the current approval's step
   526	            if (step === detail.step) {
   527	                if (detail.decision === 'approved') {
   528	                    state = 'approved';
   529	                    tagText = '已通过';
   530	                    tagCls = 'tag-approved';
   531	                    dotBg = 'var(--status-success)';
   532	                    dotBorder = 'var(--status-success)';
   533	                } else if (detail.decision === 'rejected') {
   534	                    state = 'rejected';
   535	                    tagText = '已驳回';
   536	                    tagCls = 'tag-rejected';
   537	                    dotBg = 'var(--status-error)';
   538	                    dotBorder = 'var(--status-error)';
   539	                } else {
   540	                    state = 'pending';
   541	                    tagText = '待审批';
   542	                    tagCls = 'tag-pending';
   543	                    dotBg = 'white';
   544	                    dotBorder = 'var(--primary-color)';
   545	                }
   546	                showConnector = !isLast;
   547	            } else if (i < currentLevel || appStatus === 'approved') {
   548	                state = 'approved';
   549	                tagText = '已通过';
   550	                tagCls = 'tag-approved';
   551	                dotBg = 'var(--status-success)';
   552	                dotBorder = 'var(--status-success)';
   553	                showConnector = !isLast;
   554	            } else if (i === currentLevel && appStatus !== 'rejected') {
   555	                state = 'pending';
   556	                tagText = '待审批';
   557	                tagCls = 'tag-pending';
   558	                dotBg = 'white';
   559	                dotBorder = 'var(--primary-color)';
   560	                showConnector = !isLast;
   561	            } else {
   562	                state = 'future';
   563	                tagText = '未开始';
   564	                tagCls = 'tag';
   565	                dotBg = '#e8e8e8';
   566	                dotBorder = '#e8e8e8';
   567	                showConnector = !isLast;
   568	            }
   569	
   570	            html += '<div style="position: relative; padding-left: 30px;' + (isLast ? '' : ' margin-bottom: 20px;') + '">' +
   571	              '<div style="position: absolute; left: 10px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: ' + dotBg + '; border: 2px solid ' + dotBorder + ';"></div>';
   572	
   573	            if (showConnector) {
   574	                html += '<div style="position: absolute; left: 14px; top: 16px; bottom: -20px; width: 1px; background: #e8e8e8;"></div>';
   575	            }
   576	
   577	            html += '<div class="flex-row justify-between align-center" style="margin-bottom: 6px;">' +
   578	                '<span style="font-size: 15px; font-weight: 600;">' + stepName + '</span>' +
   579	                '<span class="tag ' + tagCls + '">' + tagText + '</span>' +
   580	              '</div>';
   581	
   582	            if (state === 'approved' || state === 'pending' || state === 'rejected') {
   583	                if (detail.step === step) {
   584	                    html += '<div style="font-size: 13px; color: #666;">审批人: ' + (detail.approver_name || '待分配') + '</div>';
   585	                    if (detail.decided_at) {
   586	                        html += '<div style="font-size: 13px; color: #666;">时间: ' + detail.decided_at + '</div>';
   587	                    }
   588	                    if (detail.comment) {
   589	                        html += '<div style="font-size: 13px; color: #666; margin-top: 4px;">意见: ' + detail.comment + '</div>';
   590	                    }
   591	                }
   592	            }
   593	
   594	            html += '</div>';
   595	        }
   596	
   597	        html += '<div style="position: relative; padding-left: 30px; margin-top: 20px;">' +
   598	          '<div style="position: absolute; left: 10px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--status-success); border: 2px solid var(--status-success);"></div>' +
   599	          '<div class="flex-row justify-between align-center" style="margin-bottom: 6px;">' +
   600	            '<span style="font-size: 15px; font-weight: 600;">提交申请</span>' +
   601	            '<span class="tag tag-approved">已完成</span>' +
   602	          '</div>' +
   603	          '<div style="font-size: 13px; color: #666;">学生已提交</div>' +
   604	        '</div></div>';
   605	
   606	        return html;
   607	    }
   608	    
   609	    async function doApprove() {
   610	        if(!currentApprovalId) return;
   611	        const comment = document.getElementById('approvalComment').value;
   612	        const btn = event?.target || document.querySelector('#approval-actions .btn-primary');
   613	
   614	        const originalText = btn.textContent;
   615	        btn.disabled = true;
   616	        btn.textContent = '处理中...';
   617	
   618	        try {
   619	            const ok = await apiApprove(currentApprovalId, comment);
   620	            if(ok) { showToast('审批通过', 'success'); showScreen(1); loadApprovals(); }
   621	            else { showToast('审批失败', 'error'); }
   622	        } finally {
   623	            btn.disabled = false;
   624	            btn.textContent = originalText;
   625	        }
   626	    }
   627	
   628	    async function doReject() {
   629	        if(!currentApprovalId) return;
   630	        const comment = document.getElementById('approvalComment').value;
   631	        const btn = event?.target || document.querySelector('#approval-actions .btn-outline');
   632	
   633	        const originalText = btn.textContent;
   634	        btn.disabled = true;
   635	        btn.textContent = '处理中...';
   636	
   637	        try {
   638	            const ok = await apiReject(currentApprovalId, comment);
   639	            if(ok) { showToast('审批拒绝', 'success'); showScreen(1); loadApprovals(); }
   640	            else { showToast('审批失败', 'error'); }
   641	        } finally {
   642	            btn.disabled = false;
   643	            btn.textContent = originalText;
   644	        }
   645	    }
   646	
   647	    async function handleAttachmentPreview(attachmentId) {
   648	        try {
   649	            const url = API_BASE_URL + '/api/attachments/' + attachmentId + '/download/?preview=true';
   650	            const response = await fetch(url, {
   651	                headers: { 'Authorization': 'Bearer ' + currentToken }
   652	            });
   653	            if (!response.ok) throw new Error('预览失败');
   654	            const blob = await response.blob();
   655	            const blobUrl = URL.createObjectURL(blob);
   656	            window.open(blobUrl, '_blank');
   657	            setTimeout(() => URL.revokeObjectURL(blobUrl), 100);
   658	        } catch (error) {
   659	            showToast('预览失败: ' + error.message, 'error');
   660	        }
   661	    }
   662	
   663	    async function handleAttachmentDownload(attachmentId, fileName) {
   664	        try {
   665	            const url = API_BASE_URL + '/api/attachments/' + attachmentId + '/download/';
   666	            const response = await fetch(url, {
   667	                headers: { 'Authorization': 'Bearer ' + currentToken }
   668	            });
   669	            if (!response.ok) throw new Error('下载失败');
   670	            const blob = await response.blob();
   671	            const blobUrl = URL.createObjectURL(blob);
   672	            const a = document.createElement('a');
   673	            a.href = blobUrl;
   674	            a.download = fileName;
   675	            document.body.appendChild(a);
   676	            a.click();
   677	            document.body.removeChild(a);
   678	            URL.revokeObjectURL(blobUrl);
   679	            showToast('下载成功', 'success');
   680	        } catch (error) {
   681	            showToast('下载失败: ' + error.message, 'error');
   682	        }
   683	    }
   684	
   685	    async function exportApprovals() {
   686	        const btn = document.getElementById('export-btn');
   687	        const originalText = btn.textContent;
   688	        btn.disabled = true;
   689	        btn.textContent = '加载中...';
   690	
   691	        try {
   692	            // Fetch preview data (JSON format)
   693	            const res = await fetch(API_BASE_URL + '/approvals/?decision=all&limit=1000', {
   694	                headers: getAuthHeaders()
   695	            });
   696	
   697	            if (res.ok) {
   698	                const data = await res.json();
   699	                showExcelPreview(data.results);
   700	            } else {
   701	                showToast('加载数据失败', 'error');
   702	            }
   703	        } catch (err) {
   704	            console.error('Export preview failed:', err);
   705	            showToast('加载失败', 'error');
   706	        } finally {
   707	            btn.disabled = false;
   708	            btn.textContent = originalText;
   709	        }
   710	    }
   711	
   712	    function showExcelPreview(approvals) {
   713	        // Status mapping to Chinese
   714	        const statusMap = {
   715	            'pending_dorm_manager': '待宿管审批',
   716	            'pending_counselor': '待辅导员审批',
   717	            'pending_dean': '待学工部审批',
   718	            'approved': '已通过',
   719	            'rejected': '已拒绝',
   720	            'draft': '草稿'
   721	        };
   722	
   723	        const decisionMap = {
   724	            'pending': '待审批',
   725	            'approved': '已通过',
   726	            'rejected': '已拒绝'
   727	        };
   728	
   729	        // Build table header
   730	        const headers = ['申请ID', '提交人', '学号', '手机号', '离校日期', '楼栋号', '房间号', '提交时间', '审批状态',
   731	                        '宿管员', '宿管审批时间', '宿管审批结果', '辅导员', '辅导员审批时间', '辅导员审批结果'];
   732	
   733	        const headerHTML = '<tr>' + headers.map(h => `<th style="padding: 8px; border: 1px solid #ddd; text-align: left; white-space: nowrap;">${h}</th>`).join('') + '</tr>';
   734	        document.getElementById('excelPreviewHeader').innerHTML = headerHTML;
   735	
   736	        // Build table body - group approvals by application
   737	        const appMap = new Map();
   738	        approvals.forEach(approval => {
   739	            const appId = approval.application?.id;
   740	            if (appId && !appMap.has(appId)) {
   741	                appMap.set(appId, {
   742	                    application: approval.application,
   743	                    dormApproval: null,
   744	                    counselorApproval: null
   745	                });
   746	            }
   747	
   748	            if (appId) {
   749	                const record = appMap.get(appId);
   750	                if (approval.step === 'dorm_manager') {
   751	                    record.dormApproval = approval;
   752	                } else if (approval.step === 'counselor') {
   753	                    record.counselorApproval = approval;
   754	                }
   755	            }
   756	        });
   757	
   758	        const rows = Array.from(appMap.values()).map(record => {
   759	            const app = record.application;
   760	            const dorm = record.dormApproval;
   761	            const counselor = record.counselorApproval;
   762	
   763	            // Helper function to format date safely
   764	            const formatDate = (dateStr) => {
   765	                if (!dateStr) return '-';
   766	                const date = new Date(dateStr);
   767	                return isNaN(date.getTime()) ? '-' : date.toLocaleString();
   768	            };
   769	
   770	            return `<tr>
   771	                <td style="padding: 8px; border: 1px solid #ddd;">${app.id?.substring(0,8) || '-'}</td>
   772	                <td style="padding: 8px; border: 1px solid #ddd;">${app.student_name || '-'}</td>
   773	                <td style="padding: 8px; border: 1px solid #ddd;">${app.student_id || '-'}</td>
   774	                <td style="padding: 8px; border: 1px solid #ddd;">${app.contact_phone || '-'}</td>
   775	                <td style="padding: 8px; border: 1px solid #ddd;">${app.leave_date || '-'}</td>
   776	                <td style="padding: 8px; border: 1px solid #ddd;">${app.building || '-'}</td>
   777	                <td style="padding: 8px; border: 1px solid #ddd;">${app.room_number || '-'}</td>
   778	                <td style="padding: 8px; border: 1px solid #ddd;">${formatDate(app.created_at)}</td>
   779	                <td style="padding: 8px; border: 1px solid #ddd;">${statusMap[app.status] || app.status || '-'}</td>
   780	                <td style="padding: 8px; border: 1px solid #ddd;">${dorm?.approver_name || '-'}</td>
   781	                <td style="padding: 8px; border: 1px solid #ddd;">${formatDate(dorm?.decided_at)}</td>
   782	                <td style="padding: 8px; border: 1px solid #ddd;">${dorm?.decision ? decisionMap[dorm.decision] || dorm.decision : '-'}</td>
   783	                <td style="padding: 8px; border: 1px solid #ddd;">${counselor?.approver_name || '-'}</td>
   784	                <td style="padding: 8px; border: 1px solid #ddd;">${formatDate(counselor?.decided_at)}</td>
   785	                <td style="padding: 8px; border: 1px solid #ddd;">${counselor?.decision ? decisionMap[counselor.decision] || counselor.decision : '-'}</td>
   786	            </tr>`;
   787	        }).join('');
   788	
   789	        document.getElementById('excelPreviewBody').innerHTML = rows;
   790	        document.getElementById('excelPreviewModal').style.display = 'block';
   791	    }
   792	
   793	    function closeExcelPreview() {
   794	        document.getElementById('excelPreviewModal').style.display = 'none';
   795	    }
   796	
   797	    async function confirmExcelDownload() {
   798	        closeExcelPreview();
   799	
   800	        try {
   801	            const res = await fetch(API_BASE_URL + '/approvals/export/', {
   802	                method: 'GET',
   803	                headers: getAuthHeaders()
   804	            });
   805	
   806	            if (res.ok) {
   807	                const blob = await res.blob();
   808	                const url = window.URL.createObjectURL(blob);
   809	                const a = document.createElement('a');
   810	                a.href = url;
   811	                a.download = '审批数据_' + new Date().toISOString().split('T')[0] + '.xlsx';
   812	                document.body.appendChild(a);
   813	                a.click();
   814	                document.body.removeChild(a);
   815	                window.URL.revokeObjectURL(url);
   816	                showToast('导出成功', 'success');
   817	            } else {
   818	                showToast('导出失败', 'error');
   819	            }
   820	        } catch (err) {
   821	            console.error('Download failed:', err);
   822	            showToast('下载失败', 'error');
   823	        }
   824	    }
   825	
   826	    function showRejectedApplicationBanner() {
   827	        const existingBanner = document.getElementById('rejected-banner');
   828	        if (existingBanner) return;
   829	
   830	        const banner = document.createElement('div');
   831	        banner.id = 'rejected-banner';
   832	        banner.className = 'card';
   833	        banner.style.cssText = 'margin: 20px; margin-bottom: 20px; padding: 16px; background: #fffbe6; border-left: 4px solid #faad14;';
   834	        banner.innerHTML = `
   835	          <div style="display: flex; align-items: center; gap: 12px;">
   836	            <span style="font-size: 20px;">⚠️</span>
   837	            <div style="flex: 1;">
   838	              <div style="font-size: 14px; font-weight: 600; color: #333; margin-bottom: 4px;">您的申请已被驳回</div>
   839	              <div style="font-size: 13px; color: #666;">请查看驳回原因后重新提交申请</div>
   840	            </div>
   841	            <button class="btn-outline" onclick="showScreen(1); loadMyApplications();" style="padding: 8px 16px; font-size: 13px;">查看驳回原因</button>
   842	          </div>
   843	        `;
   844	        const screen0 = document.getElementById('screen-0');
   845	        const firstChild = screen0.querySelector('div[style*="padding: 20px"]');
   846	        if (firstChild) {
   847	            firstChild.insertBefore(banner, firstChild.firstChild);
   848	        }
   849	    }
   850	
   851	    async function doSubmitApplication() {
   852	        const phone = document.getElementById('contactPhone').value;
   853	        const reason = document.getElementById('applicationReason').value;
   854	        const leaveDate = document.getElementById('leaveDate').value;
   855	
   856	        // 验证必填字段
   857	        if (!phone || !leaveDate) {
   858	             showToast('请输入联系电话和离校日期', 'error');
   859	             return;
   860	        }
   861	
   862	        // 验证附件（必需）
   863	        if (!uploadedFiles || uploadedFiles.length === 0) {
   864	             showToast('请上传附件材料', 'error');
   865	             return;
   866	        }
   867	
   868	        // 验证手机号格式（11位，1开头）
   869	        if (!/^1\d{10}$/.test(phone)) {
   870	             showToast('请输入有效的11位手机号码', 'error');
   871	             return;
   872	        }
   873	
   874	        // 验证原因长度（最多500字符）
   875	        if (reason && reason.length > 500) {
   876	             showToast('离校原因不能超过500字', 'error');
   877	             return;
   878	        }
   879	
   880	        // 验证离校日期（不能早于今天）
   881	        const today = new Date();
   882	        today.setHours(0, 0, 0, 0);
   883	        const selectedDate = new Date(leaveDate);
   884	        if (selectedDate < today) {
   885	             showToast('离校日期不能早于今天', 'error');
   886	             return;
   887	        }
   888	
   889	        const btn = event?.target || document.querySelector('#screen-0 .btn-primary');
   890	        const originalText = btn.textContent;
   891	        btn.disabled = true;
   892	        btn.textContent = '提交中...';
   893	
   894	        try {
   895	            const result = await apiSubmitApplication(phone, reason, leaveDate, uploadedFiles);
   896	            if (result.success) {
   897	                showToast('申请提交成功', 'success');
   898	                document.getElementById('contactPhone').value = '';
   899	                document.getElementById('applicationReason').value = '';
   900	                document.getElementById('leaveDate').value = '';
   901	                uploadedFiles = [];
   902	                renderFileList();
   903	
   904	                // Switch to progress view
   905	                showScreen(1);
   906	                loadMyApplications();
   907	            } else {
   908	                showToast(result.error.message || '申请提交失败', 'error');
   909	            }
   910	        } finally {
   911	            btn.disabled = false;
   912	            btn.textContent = originalText;
   913	        }
   914	    }
   915	</script>
   916	  <style>
   917	    /* 导航标签 */
   918	    .nav-tabs {
   919	      background: white;
   920	      display: flex;

exec
/bin/bash -lc 'rtk git show --stat --patch --find-renames --no-compact 7b2fce6 -- demo-web/index.html' in /home/caohui/projects/graduation-leave-system
 exited 128 in 0ms:
fatal: unrecognized argument: --no-compact


exec
/bin/bash -lc 'rtk git show --stat --patch --no-compact ee5667a -- backend/apps/approvals/serializers.py' in /home/caohui/projects/graduation-leave-system
 exited 128 in 0ms:
fatal: unrecognized argument: --no-compact


exec
/bin/bash -lc "rtk nl -ba demo-web/index.html | sed -n '1336,1460p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
  1336	    function updateUIForRole(role) {
  1337	      const isStudent = role === 'student';
  1338	      const isDean = role === 'dean';
  1339	      const isAdmin = role === 'admin';
  1340	
  1341	      // Hide "学生申请" tab for non-students
  1342	      const navTabs = document.querySelectorAll('#navTabs .nav-tab');
  1343	      if (navTabs[0]) {
  1344	        navTabs[0].style.display = isStudent ? 'block' : 'none';
  1345	      }
  1346	
  1347	      // Update nav tab text
  1348	      document.getElementById('nav-approval-text').textContent = isStudent ? '我的申请' : (isDean || isAdmin ? '审批查询' : '审批列表');
  1349	
  1350	      // Update list page title and role display
  1351	      document.getElementById('list-title').textContent = isStudent ? '我的申请' : (isDean || isAdmin ? '审批查询' : '审批列表');
  1352	      document.getElementById('role-display').textContent = (isStudent ? '学生' : isDean ? '学工部' : isAdmin ? '管理员' : role === 'counselor' ? '辅导员' : '宿管员');
  1353	
  1354	      // Show/hide approval section for student/dean/admin
  1355	      const approvalSection = document.getElementById('approval-section');
  1356	      if (approvalSection) {
  1357	        approvalSection.style.display = (isStudent || isDean || isAdmin) ? 'none' : 'block';
  1358	      }
  1359	
  1360	      // Show export button for dean and admin roles
  1361	      const exportBtn = document.getElementById('export-btn');
  1362	      if (exportBtn) {
  1363	        exportBtn.style.display = (isDean || isAdmin) ? 'block' : 'none';
  1364	      }
  1365	    }
  1366	
  1367	    function logout() {
  1368	      currentToken = null;
  1369	      currentUser = null;
  1370	      deanDisplayedApps.clear(); // Clear deduplication memory on logout
  1371	      approvalOffset = 0;
  1372	      approvalHasMore = true;
  1373	      document.getElementById('navTabs').style.display = 'none';
  1374	      document.getElementById('userBar').style.display = 'none';
  1375	      document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  1376	      document.getElementById('screen-login').classList.add('active');
  1377	    }
  1378	
  1379	    // File upload management
  1380	    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
  1381	    const ALLOWED_TYPES = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx'];
  1382	    let uploadedFiles = [];
  1383	
  1384	    const fileInput = document.getElementById('fileInput');
  1385	    const fileList = document.getElementById('fileList');
  1386	    const uploadArea = document.querySelector('.upload-area');
  1387	
  1388	    // File selection handler
  1389	    fileInput.addEventListener('change', (e) => {
  1390	      handleFiles(e.target.files);
  1391	    });
  1392	
  1393	    // Drag and drop handlers
  1394	    uploadArea.addEventListener('dragover', (e) => {
  1395	      e.preventDefault();
  1396	      uploadArea.style.borderColor = 'var(--primary-color)';
  1397	      uploadArea.style.background = '#fafafa';
  1398	    });
  1399	
  1400	    uploadArea.addEventListener('dragleave', () => {
  1401	      uploadArea.style.borderColor = '#d9d9d9';
  1402	      uploadArea.style.background = 'white';
  1403	    });
  1404	
  1405	    uploadArea.addEventListener('drop', (e) => {
  1406	      e.preventDefault();
  1407	      uploadArea.style.borderColor = '#d9d9d9';
  1408	      uploadArea.style.background = 'white';
  1409	      handleFiles(e.dataTransfer.files);
  1410	    });
  1411	
  1412	    function handleFiles(files) {
  1413	      const validFiles = [];
  1414	      const errors = [];
  1415	
  1416	      Array.from(files).forEach(file => {
  1417	        const ext = '.' + file.name.split('.').pop().toLowerCase();
  1418	
  1419	        if (!ALLOWED_TYPES.includes(ext)) {
  1420	          errors.push(`${file.name}: 不支持的文件格式`);
  1421	          return;
  1422	        }
  1423	
  1424	        if (file.size > MAX_FILE_SIZE) {
  1425	          errors.push(`${file.name}: 文件大小超过10MB`);
  1426	          return;
  1427	        }
  1428	
  1429	        validFiles.push(file);
  1430	      });
  1431	
  1432	      if (errors.length > 0) {
  1433	        errors.forEach(err => showToast(err, 'error'));
  1434	      }
  1435	
  1436	      uploadedFiles = uploadedFiles.concat(validFiles);
  1437	      renderFileList();
  1438	      fileInput.value = ''; // Reset input
  1439	    }
  1440	
  1441	    function renderFileList() {
  1442	      fileList.innerHTML = uploadedFiles.map((file, index) => `
  1443	        <div class="file-item">
  1444	          <span style="font-size: 20px;">📄</span>
  1445	          <div class="file-info">
  1446	            <div class="file-name">${file.name}</div>
  1447	            <div class="file-size">${formatFileSize(file.size)}</div>
  1448	          </div>
  1449	          <button class="btn-delete" onclick="removeFile(${index})" type="button">×</button>
  1450	        </div>
  1451	      `).join('');
  1452	    }
  1453	
  1454	    function removeFile(index) {
  1455	      uploadedFiles.splice(index, 1);
  1456	      renderFileList();
  1457	    }
  1458	
  1459	    function formatFileSize(bytes) {
  1460	      if (bytes < 1024) return bytes + ' B';

exec
/bin/bash -lc "rtk nl -ba demo-web/js/api.js | sed -n '1,260p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	// API Integration Layer
     2	const API_BASE_URL = `http://${window.location.hostname}:7787/api`;
     3	
     4	let currentToken = null;
     5	let currentUser = null;
     6	
     7	// 页面加载时自动恢复登录状态
     8	function restoreAuthState() {
     9	    const savedToken = localStorage.getItem('auth_token');
    10	    const savedUser = localStorage.getItem('user_info');
    11	
    12	    if (savedToken) {
    13	        currentToken = savedToken;
    14	        if (savedUser) {
    15	            try {
    16	                currentUser = JSON.parse(savedUser);
    17	                console.log('Auth state restored from localStorage', currentUser);
    18	            } catch (e) {
    19	                console.error('Failed to parse user info:', e);
    20	            }
    21	        }
    22	    }
    23	}
    24	
    25	// 恢复登录后初始化UI
    26	function initializeUIAfterRestore(user) {
    27	    // 隐藏登录界面
    28	    const loginScreen = document.getElementById('screen-login');
    29	    if (loginScreen && loginScreen.classList.contains('active')) {
    30	        loginScreen.classList.remove('active');
    31	
    32	        // 显示导航栏和用户栏
    33	        const navTabs = document.getElementById('navTabs');
    34	        const userBar = document.getElementById('userBar');
    35	        if (navTabs) navTabs.style.display = 'flex';
    36	        if (userBar) userBar.style.display = 'flex';
    37	
    38	        // 显示用户信息
    39	        const userNameEl = document.getElementById('currentUserName');
    40	        const userRoleEl = document.getElementById('currentUserRole');
    41	        if (userNameEl && user.real_name) userNameEl.textContent = user.real_name;
    42	        if (userRoleEl && user.role) {
    43	            const roleMap = { 'student': '学生', 'dorm_manager': '宿管', 'counselor': '辅导员', 'dean': '学工部', 'admin': '管理员' };
    44	            userRoleEl.textContent = '(' + (roleMap[user.role] || user.role) + ')';
    45	        }
    46	
    47	        // 根据角色显示对应界面
    48	        if (user.role === 'student') {
    49	            if (typeof showScreen === 'function') showScreen(0);
    50	        } else {
    51	            if (typeof showScreen === 'function') showScreen(1); // 审批列表
    52	        }
    53	
    54	        console.log('UI initialized for user:', user.username);
    55	    }
    56	}
    57	
    58	// 页面加载时立即执行
    59	restoreAuthState();
    60	
    61	async function apiLogin(userId, password) {
    62	    try {
    63	        const response = await fetch(API_BASE_URL + '/auth/login', {
    64	            method: 'POST',
    65	            headers: { 'Content-Type': 'application/json' },
    66	            body: JSON.stringify({
    67	                user_id: userId,
    68	                password: password
    69	            })
    70	        });
    71	
    72	        if (response.ok) {
    73	            const data = await response.json();
    74	            currentToken = data.access_token;
    75	            currentUser = data.user;
    76	            return { success: true, user: data.user };
    77	        } else {
    78	            currentToken = null;
    79	            currentUser = null;
    80	            const error = await response.json().catch(() => ({ error: 'Login failed' }));
    81	            return { success: false, error: error };
    82	        }
    83	    } catch (e) {
    84	        console.error("Login failed:", e);
    85	        currentToken = null;
    86	        currentUser = null;
    87	        return { success: false, error: 'Network error' };
    88	    }
    89	}
    90	
    91	function getAuthHeaders() {
    92	    return {
    93	        'Authorization': 'Bearer ' + currentToken
    94	    };
    95	}
    96	
    97	async function apiSubmitApplication(phone, reason, leaveDate, files) {
    98	    const formData = new FormData();
    99	    formData.append('contact_phone', phone);
   100	    formData.append('reason', reason);
   101	    formData.append('leave_date', leaveDate);
   102	    files.forEach(f => formData.append('attachments', f));
   103	
   104	    try {
   105	        const response = await fetch(API_BASE_URL + '/applications/', {
   106	            method: 'POST',
   107	            headers: { 'Authorization': 'Bearer ' + currentToken },
   108	            body: formData
   109	        });
   110	        if (response.ok) {
   111	            return { success: true, data: await response.json() };
   112	        } else {
   113	            const error = await response.json().catch(() => ({ error: { message: '提交失败' } }));
   114	            return { success: false, error: error.error || { message: '提交失败' } };
   115	        }
   116	    } catch (e) {
   117	        console.error("Submit application failed:", e);
   118	        return { success: false, error: { message: '网络错误，请检查连接' } };
   119	    }
   120	}
   121	
   122	async function apiGetApplications() {
   123	    try {
   124	        const response = await fetch(API_BASE_URL + '/applications/', {
   125	            headers: getAuthHeaders()
   126	        });
   127	        if (response.ok) {
   128	            return await response.json();
   129	        }
   130	    } catch (e) {
   131	        console.error("Get applications failed:", e);
   132	    }
   133	    return { results: [] };
   134	}
   135	
   136	async function apiGetApprovals(decision = 'pending', limit = 20, offset = 0) {
   137	    try {
   138	        const url = API_BASE_URL + '/approvals/?decision=' + decision + '&limit=' + limit + '&offset=' + offset;
   139	        const response = await fetch(url, {
   140	            headers: getAuthHeaders()
   141	        });
   142	        if (response.ok) {
   143	            return await response.json();
   144	        }
   145	    } catch (e) {
   146	        console.error("Get approvals failed:", e);
   147	    }
   148	    return { results: [], count: 0 };
   149	}
   150	
   151	async function apiApprove(approvalId, comment) {
   152	    try {
   153	        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId + '/approve/', {
   154	            method: 'POST',
   155	            headers: Object.assign({}, getAuthHeaders(), { 'Content-Type': 'application/json' }),
   156	            body: JSON.stringify({ comment: comment })
   157	        });
   158	        return response.ok;
   159	    } catch (e) {
   160	        console.error("Approve failed:", e);
   161	        return false;
   162	    }
   163	}
   164	
   165	async function apiReject(approvalId, comment) {
   166	    try {
   167	        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId + '/reject/', {
   168	            method: 'POST',
   169	            headers: Object.assign({}, getAuthHeaders(), { 'Content-Type': 'application/json' }),
   170	            body: JSON.stringify({ comment: comment })
   171	        });
   172	        return response.ok;
   173	    } catch (e) {
   174	        console.error("Reject failed:", e);
   175	        return false;
   176	    }
   177	}
   178	
   179	async function apiUploadAttachment(applicationId, file, attachmentType = 'other') {
   180	    const formData = new FormData();
   181	    formData.append('file', file);
   182	    formData.append('attachment_type', attachmentType);
   183	
   184	    try {
   185	        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/', {
   186	            method: 'POST',
   187	            headers: getAuthHeaders(),
   188	            body: formData
   189	        });
   190	        if (response.ok) {
   191	            return await response.json();
   192	        }
   193	    } catch (e) {
   194	        console.error("Upload attachment failed:", e);
   195	    }
   196	    return null;
   197	}
   198	
   199	async function apiGetAttachments(applicationId) {
   200	    try {
   201	        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/', {
   202	            headers: getAuthHeaders()
   203	        });
   204	        if (response.ok) {
   205	            return await response.json();
   206	        }
   207	    } catch (e) {
   208	        console.error("Get attachments failed:", e);
   209	    }
   210	    return [];
   211	}
   212	
   213	async function apiDeleteAttachment(applicationId, attachmentId) {
   214	    try {
   215	        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/' + attachmentId + '/', {
   216	            method: 'DELETE',
   217	            headers: getAuthHeaders()
   218	        });
   219	        return response.ok;
   220	    } catch (e) {
   221	        console.error("Delete attachment failed:", e);
   222	        return false;
   223	    }
   224	}
   225	
   226	// DOM加载完成后，如果有token则自动初始化UI
   227	if (typeof document !== 'undefined') {
   228	    document.addEventListener('DOMContentLoaded', function() {
   229	        if (currentToken && currentUser) {
   230	            console.log('Initializing UI after token restore');
   231	            initializeUIAfterRestore(currentUser);
   232	        }
   233	    });
   234	}

exec
/bin/bash -lc 'rtk git show --stat --patch ce19e4e -- demo-web/index.html' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
commit ce19e4e7659c7da55e899ac1ac6db51676a1f1be
Author: caohui-net <13307411234@189.cn>
Date:   Thu Jun 11 13:43:39 2026 +0800

    fix(demo-web): 修复admin角色审批列表显示问题
    
    - 删除重复的currentUser声明（已在api.js中声明）
    - 添加admin角色完整UI支持（显示为'管理员'而非'宿管员'）
    - 修复admin角色去重逻辑（之前仅对dean生效）
    - 保留无application关联的Approval记录（孤儿记录）
    - 添加调试日志用于排查数据显示问题
    - 隐藏admin角色的审批操作按钮（仅查看，不审批）
    
    Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
---
 demo-web/index.html | 38 +++++++++++++++++++++++++-------------
 1 file changed, 25 insertions(+), 13 deletions(-)

diff --git a/demo-web/index.html b/demo-web/index.html
index 909e952..3834135 100644
--- a/demo-web/index.html
+++ b/demo-web/index.html
@@ -11,7 +11,7 @@
     let approvalOffset = 0;
     let approvalHasMore = true;
     let deanDisplayedApps = new Set(); // Track displayed application IDs for dean deduplication
-    let currentUser = null; // Current logged-in user
+    // currentUser is declared in api.js
 
     async function loadMyApplications() {
         if (!currentToken) return;
@@ -71,6 +71,8 @@
 
         const data = await apiGetApprovals(decision, 20, approvalOffset);
         console.log('[DEBUG] apiGetApprovals returned:', data);
+        console.log('[DEBUG] currentUser:', currentUser);
+        console.log('[DEBUG] currentFilter:', currentFilter, 'decision:', decision);
         const listContainer = document.getElementById('approval-list-container');
         const loadMoreBtn = document.getElementById('load-more-approvals');
 
@@ -97,21 +99,30 @@
             let filtered = data.results;
             if (currentFilter === 'decided') {
                 filtered = data.results.filter(a => a.decision === 'approved' || a.decision === 'rejected');
+                console.log('[DEBUG] Filtered decided count:', filtered.length);
             }
 
             let htmlStr = '';
 
-            // For dean: group by application_id to avoid duplicates (cross-page deduplication)
-            if (currentUser && currentUser.role === 'dean') {
+            // For dean/admin: group by application_id to avoid duplicates (cross-page deduplication)
+            if (currentUser && (currentUser.role === 'dean' || currentUser.role === 'admin')) {
+                console.log('[DEBUG] Before dedup:', filtered.length, 'deanDisplayedApps size:', deanDisplayedApps.size);
                 const appMap = new Map();
+                const orphanApprovals = []; // Approvals without application link
                 filtered.forEach(approval => {
                     const appId = approval.application?.id;
-                    if (appId && !deanDisplayedApps.has(appId) && !appMap.has(appId)) {
-                        appMap.set(appId, approval);
-                        deanDisplayedApps.add(appId); // Track globally
+                    if (appId) {
+                        if (!deanDisplayedApps.has(appId) && !appMap.has(appId)) {
+                            appMap.set(appId, approval);
+                            deanDisplayedApps.add(appId); // Track globally
+                        }
+                    } else {
+                        // Keep approvals without application link
+                        orphanApprovals.push(approval);
                     }
                 });
-                filtered = Array.from(appMap.values());
+                filtered = Array.from(appMap.values()).concat(orphanApprovals);
+                console.log('[DEBUG] After dedup:', filtered.length, 'unique apps:', appMap.size, 'orphans:', orphanApprovals.length);
             }
 
             filtered.forEach(approval => {
@@ -1005,6 +1016,7 @@
     function updateUIForRole(role) {
       const isStudent = role === 'student';
       const isDean = role === 'dean';
+      const isAdmin = role === 'admin';
 
       // Hide "学生申请" tab for non-students
       const navTabs = document.querySelectorAll('#navTabs .nav-tab');
@@ -1013,22 +1025,22 @@
       }
 
       // Update nav tab text
-      document.getElementById('nav-approval-text').textContent = isStudent ? '我的申请' : (isDean ? '审批查询' : '审批列表');
+      document.getElementById('nav-approval-text').textContent = isStudent ? '我的申请' : (isDean || isAdmin ? '审批查询' : '审批列表');
 
       // Update list page title and role display
-      document.getElementById('list-title').textContent = isStudent ? '我的申请' : (isDean ? '审批查询' : '审批列表');
-      document.getElementById('role-display').textContent = (isStudent ? '学生' : isDean ? '学工部' : role === 'counselor' ? '辅导员' : '宿管员');
+      document.getElementById('list-title').textContent = isStudent ? '我的申请' : (isDean || isAdmin ? '审批查询' : '审批列表');
+      document.getElementById('role-display').textContent = (isStudent ? '学生' : isDean ? '学工部' : isAdmin ? '管理员' : role === 'counselor' ? '辅导员' : '宿管员');
 
-      // Show/hide approval section for student/dean
+      // Show/hide approval section for student/dean/admin
       const approvalSection = document.getElementById('approval-section');
       if (approvalSection) {
-        approvalSection.style.display = (isStudent || isDean) ? 'none' : 'block';
+        approvalSection.style.display = (isStudent || isDean || isAdmin) ? 'none' : 'block';
       }
 
       // Show export button for dean and admin roles
       const exportBtn = document.getElementById('export-btn');
       if (exportBtn) {
-        exportBtn.style.display = (isDean || role === 'admin') ? 'block' : 'none';
+        exportBtn.style.display = (isDean || isAdmin) ? 'block' : 'none';
       }
     }

exec
/bin/bash -lc 'rtk git show --stat --patch 7b2fce6 -- demo-web/index.html' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
commit 7b2fce6866d278127b71fb6d60cdf1d63e8d76ee
Author: caohui-net <13307411234@189.cn>
Date:   Thu Jun 11 18:23:29 2026 +0800

    fix(security): 修复XSS漏洞、无限循环风险、内存泄漏
    
    - 添加escapeHtml()防止XSS注入(student_name/approver_name等用户输入)
    - loadApprovals循环增加MAX_ITERATIONS=10上限防止挂起
    - logout()清理deanDisplayedApps Set避免跨session内存累积
---
 demo-web/index.html | 27 +++++++++++++++++++++++----
 1 file changed, 23 insertions(+), 4 deletions(-)

diff --git a/demo-web/index.html b/demo-web/index.html
index 0333676..d47ba18 100644
--- a/demo-web/index.html
+++ b/demo-web/index.html
@@ -13,6 +13,14 @@
     let deanDisplayedApps = new Set(); // Track displayed application IDs for dean deduplication
     // currentUser is declared in api.js
 
+    // HTML escape helper to prevent XSS
+    function escapeHtml(text) {
+        if (!text) return '';
+        const div = document.createElement('div');
+        div.textContent = text;
+        return div.innerHTML;
+    }
+
     async function loadMyApplications() {
         if (!currentToken) return;
         const data = await apiGetApplications();
@@ -74,12 +82,15 @@
 
         const TARGET_COUNT = 20; // Target number of deduplicated records to display
         const BATCH_SIZE = 20;   // API request batch size
+        const MAX_ITERATIONS = 10; // Safety limit to prevent infinite loops
         let accumulatedResults = [];
         let currentOffset = approvalOffset;
         let totalCount = 0;
+        let iterations = 0;
 
         // Loop until we have TARGET_COUNT deduplicated records or no more data
-        while (accumulatedResults.length < TARGET_COUNT) {
+        while (accumulatedResults.length < TARGET_COUNT && iterations < MAX_ITERATIONS) {
+            iterations++;
             const data = await apiGetApprovals(decision, BATCH_SIZE, currentOffset);
             console.log('[DEBUG] apiGetApprovals returned:', data, 'offset:', currentOffset);
 
@@ -159,14 +170,18 @@
                 const step = decisionMap[decision] ? decisionMap[decision].text : decision;
                 const tagCls = decisionMap[decision] ? decisionMap[decision].cls : 'tag-pending';
 
+                const safeAppId = escapeHtml(application.id || approval.id).substring(0,8);
+                const safeStudentName = escapeHtml(application.student_name || '-');
+                const safeStudentId = escapeHtml(application.student_id || '-');
+
                 htmlStr += '<div class="card" onclick="openApproval(\'' + approval.id + '\')" style="cursor: pointer;">' +
                   '<div class="flex-row justify-between align-center" style="margin-bottom: 8px;">' +
-                    '<span style="font-size: 16px; font-weight: bold;">申请 ' + (application.id ? application.id.substring(0,8) : approval.id.substring(0,8)) + '</span>' +
+                    '<span style="font-size: 16px; font-weight: bold;">申请 ' + safeAppId + '</span>' +
                     '<span class="tag ' + tagCls + '">' + step + '</span>' +
                   '</div>' +
                   '<div style="margin-bottom: 4px;">' +
                     '<span style="font-size: 14px; color: #999; margin-right: 8px;">学生:</span>' +
-                    '<span style="font-size: 14px; color: #333;">' + (application.student_name || '-') + ' (' + (application.student_id || '-') + ')</span>' +
+                    '<span style="font-size: 14px; color: #333;">' + safeStudentName + ' (' + safeStudentId + ')</span>' +
                   '</div>';
 
                 // Show approver and decision time for decided approvals
@@ -179,10 +194,11 @@
                             realApprover = match[1];
                         }
                     }
+                    const safeApprover = escapeHtml(realApprover);
 
                     htmlStr += '<div style="margin-bottom: 4px;">' +
                       '<span style="font-size: 14px; color: #999; margin-right: 8px;">审批人:</span>' +
-                      '<span style="font-size: 14px; color: #333;">' + realApprover + '</span>' +
+                      '<span style="font-size: 14px; color: #333;">' + safeApprover + '</span>' +
                     '</div>';
                     if (approval.decided_at) {
                         htmlStr += '<div style="margin-bottom: 4px;">' +
@@ -1182,6 +1198,9 @@
     function logout() {
       currentToken = null;
       currentUser = null;
+      deanDisplayedApps.clear(); // Clear deduplication memory on logout
+      approvalOffset = 0;
+      approvalHasMore = true;
       document.getElementById('navTabs').style.display = 'none';
       document.getElementById('userBar').style.display = 'none';
       document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));

exec
/bin/bash -lc 'rtk git show --stat --patch ee5667a -- backend/apps/approvals/serializers.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
commit ee5667a7e72ece271111f8ba096af7e2b2e82e70
Author: caohui-net <13307411234@189.cn>
Date:   Thu Jun 11 14:14:02 2026 +0800

    fix(backend): ApplicationBriefSerializer添加缺失字段
    
    - 添加contact_phone（联系电话）
    - 添加building和room_number（宿舍信息）
    - 添加created_at（提交时间）
    - 修复Excel预览数据不完整问题
    
    Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
---
 backend/apps/approvals/serializers.py | 4 ++++
 1 file changed, 4 insertions(+)

diff --git a/backend/apps/approvals/serializers.py b/backend/apps/approvals/serializers.py
index 243fcde..db544eb 100644
--- a/backend/apps/approvals/serializers.py
+++ b/backend/apps/approvals/serializers.py
@@ -8,7 +8,11 @@ class ApplicationBriefSerializer(serializers.Serializer):
     status = serializers.CharField()
     student_name = serializers.CharField(source='student.name')
     student_id = serializers.CharField(source='student.user_id')
+    contact_phone = serializers.CharField(allow_null=True)
     leave_date = serializers.DateField()
+    building = serializers.CharField(source='student.building', allow_null=True)
+    room_number = serializers.CharField(source='student.room_number', allow_null=True)
+    created_at = serializers.DateTimeField()
 
 
 class ApprovalListSerializer(serializers.ModelSerializer):

exec
/bin/bash -lc 'rtk git show --stat --patch 097e0f7 -- demo-web/index.html' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
commit 097e0f7a78611c5ad379d3b360bc7a7b83c8cd4d
Author: caohui-net <13307411234@189.cn>
Date:   Thu Jun 11 13:57:07 2026 +0800

    refactor(demo-web): 重构分页逻辑，固定显示20条去重后的记录
    
    - 改变分页策略：循环请求API直到凑够20条去重后的记录
    - 修复显示数量不固定问题（之前每页显示5-15条不等）
    - 优化加载更多：每次加载20条去重后的记录
    - 保持跨页去重逻辑（deanDisplayedApps全局追踪）
    
    Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
---
 demo-web/index.html | 98 ++++++++++++++++++++++++++++++++++-------------------
 1 file changed, 64 insertions(+), 34 deletions(-)

diff --git a/demo-web/index.html b/demo-web/index.html
index 3834135..7816d22 100644
--- a/demo-web/index.html
+++ b/demo-web/index.html
@@ -69,31 +69,26 @@
             decision = 'all'; // Get all, then filter for approved/rejected
         }
 
-        const data = await apiGetApprovals(decision, 20, approvalOffset);
-        console.log('[DEBUG] apiGetApprovals returned:', data);
-        console.log('[DEBUG] currentUser:', currentUser);
-        console.log('[DEBUG] currentFilter:', currentFilter, 'decision:', decision);
         const listContainer = document.getElementById('approval-list-container');
         const loadMoreBtn = document.getElementById('load-more-approvals');
 
-        // Status map based on backend expectations
-        const statusMap = {
-            'pending_dorm_manager': { text: '待宿管审批', cls: 'tag-pending' },
-            'pending_counselor': { text: '待辅导员审批', cls: 'tag-pending' },
-            'pending_dean': { text: '待学工部审批', cls: 'tag-pending' },
-            'approved': { text: '已通过', cls: 'tag-approved' },
-            'rejected': { text: '已拒绝', cls: 'tag-rejected' }
-        };
+        const TARGET_COUNT = 20; // Target number of deduplicated records to display
+        const BATCH_SIZE = 20;   // API request batch size
+        let accumulatedResults = [];
+        let currentOffset = approvalOffset;
+        let totalCount = 0;
 
-        const decisionMap = {
-            'pending': { text: '待审批', cls: 'tag-pending' },
-            'approved': { text: '已通过', cls: 'tag-approved' },
-            'rejected': { text: '已拒绝', cls: 'tag-rejected' }
-        };
+        // Loop until we have TARGET_COUNT deduplicated records or no more data
+        while (accumulatedResults.length < TARGET_COUNT) {
+            const data = await apiGetApprovals(decision, BATCH_SIZE, currentOffset);
+            console.log('[DEBUG] apiGetApprovals returned:', data, 'offset:', currentOffset);
 
-        if (data.results && data.results.length > 0) {
-            // Save raw page size before filtering for pagination offset
-            const rawResultsLength = data.results.length;
+            if (!data || !data.results || data.results.length === 0) {
+                // No more data from API
+                break;
+            }
+
+            totalCount = data.count;
 
             // Apply front-end filter only for 'decided' (approved or rejected)
             let filtered = data.results;
@@ -102,30 +97,61 @@
                 console.log('[DEBUG] Filtered decided count:', filtered.length);
             }
 
-            let htmlStr = '';
-
-            // For dean/admin: group by application_id to avoid duplicates (cross-page deduplication)
+            // For dean/admin: deduplicate by application_id
             if (currentUser && (currentUser.role === 'dean' || currentUser.role === 'admin')) {
-                console.log('[DEBUG] Before dedup:', filtered.length, 'deanDisplayedApps size:', deanDisplayedApps.size);
-                const appMap = new Map();
-                const orphanApprovals = []; // Approvals without application link
+                const beforeCount = filtered.length;
+                const newUniqueRecords = [];
+                const orphanApprovals = [];
+
                 filtered.forEach(approval => {
                     const appId = approval.application?.id;
                     if (appId) {
-                        if (!deanDisplayedApps.has(appId) && !appMap.has(appId)) {
-                            appMap.set(appId, approval);
-                            deanDisplayedApps.add(appId); // Track globally
+                        if (!deanDisplayedApps.has(appId)) {
+                            newUniqueRecords.push(approval);
+                            deanDisplayedApps.add(appId); // Track globally across pages
                         }
                     } else {
                         // Keep approvals without application link
                         orphanApprovals.push(approval);
                     }
                 });
-                filtered = Array.from(appMap.values()).concat(orphanApprovals);
-                console.log('[DEBUG] After dedup:', filtered.length, 'unique apps:', appMap.size, 'orphans:', orphanApprovals.length);
+
+                filtered = newUniqueRecords.concat(orphanApprovals);
+                console.log('[DEBUG] Dedup: before', beforeCount, '→ after', filtered.length, 'deanDisplayedApps size:', deanDisplayedApps.size);
             }
 
-            filtered.forEach(approval => {
+            accumulatedResults = accumulatedResults.concat(filtered);
+            currentOffset += BATCH_SIZE;
+
+            // Stop if we've reached the end of available data
+            if (currentOffset >= totalCount) {
+                break;
+            }
+        }
+
+        // Render accumulated results (up to TARGET_COUNT)
+        const displayRecords = accumulatedResults.slice(0, TARGET_COUNT);
+        console.log('[DEBUG] Displaying', displayRecords.length, 'records, accumulated', accumulatedResults.length);
+
+        // Status map based on backend expectations
+        const statusMap = {
+            'pending_dorm_manager': { text: '待宿管审批', cls: 'tag-pending' },
+            'pending_counselor': { text: '待辅导员审批', cls: 'tag-pending' },
+            'pending_dean': { text: '待学工部审批', cls: 'tag-pending' },
+            'approved': { text: '已通过', cls: 'tag-approved' },
+            'rejected': { text: '已拒绝', cls: 'tag-rejected' }
+        };
+
+        const decisionMap = {
+            'pending': { text: '待审批', cls: 'tag-pending' },
+            'approved': { text: '已通过', cls: 'tag-approved' },
+            'rejected': { text: '已拒绝', cls: 'tag-rejected' }
+        };
+
+        if (displayRecords.length > 0) {
+            let htmlStr = '';
+
+            displayRecords.forEach(approval => {
                 const application = approval.application || {};
 
                 // Use approval decision for status tag (more accurate for dean/approval views)
@@ -178,8 +204,12 @@
                 listContainer.innerHTML = htmlStr;
             }
 
-            approvalOffset += rawResultsLength;
-            approvalHasMore = data.count > approvalOffset;
+            // Update offset to current position
+            approvalOffset = currentOffset;
+
+            // Check if there's more data to load
+            // Has more if: we haven't displayed all accumulated results, or there's more data in API
+            approvalHasMore = (accumulatedResults.length > TARGET_COUNT) || (currentOffset < totalCount);
 
             if (loadMoreBtn) {
                 loadMoreBtn.style.display = approvalHasMore ? 'block' : 'none';

codex
分页改动的核心问题开始清晰：当前用全局去重集配合“多抓几页再截断 20 条”，但被截断掉的记录也已经加入去重集，后续“加载更多”会永久跳过这些记录。接下来我再核对 Excel 预览和后端序列化字段是否有同类数据完整性或安全问题。
exec
/bin/bash -lc 'rtk git show --stat --patch f532f03 -- demo-web/index.html' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
commit f532f03c6a17e8ce1f4816404c5ac3c0d3745d37
Author: caohui-net <13307411234@189.cn>
Date:   Thu Jun 11 14:03:18 2026 +0800

    feat(demo-web): 添加Excel导出预览功能
    
    - 点击导出按钮先显示数据表格预览
    - 预览模态框展示所有导出字段（申请信息+审批记录）
    - 预览后确认才下载Excel文件
    - 优化用户体验：避免直接下载未知内容
    
    Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
---
 demo-web/index.html | 118 ++++++++++++++++++++++++++++++++++++++++++++++++----
 1 file changed, 110 insertions(+), 8 deletions(-)

diff --git a/demo-web/index.html b/demo-web/index.html
index 7816d22..7f01b50 100644
--- a/demo-web/index.html
+++ b/demo-web/index.html
@@ -535,7 +535,93 @@
         const btn = document.getElementById('export-btn');
         const originalText = btn.textContent;
         btn.disabled = true;
-        btn.textContent = '导出中...';
+        btn.textContent = '加载中...';
+
+        try {
+            // Fetch preview data (JSON format)
+            const res = await fetch(API_BASE_URL + '/approvals/?decision=all&limit=1000', {
+                headers: getAuthHeaders()
+            });
+
+            if (res.ok) {
+                const data = await res.json();
+                showExcelPreview(data.results);
+            } else {
+                showToast('加载数据失败', 'error');
+            }
+        } catch (err) {
+            console.error('Export preview failed:', err);
+            showToast('加载失败', 'error');
+        } finally {
+            btn.disabled = false;
+            btn.textContent = originalText;
+        }
+    }
+
+    function showExcelPreview(approvals) {
+        // Build table header
+        const headers = ['申请ID', '提交人', '学号', '手机号', '离校日期', '楼栋号', '房间号', '提交时间', '审批状态',
+                        '宿管员', '宿管审批时间', '宿管审批结果', '辅导员', '辅导员审批时间', '辅导员审批结果'];
+
+        const headerHTML = '<tr>' + headers.map(h => `<th style="padding: 8px; border: 1px solid #ddd; text-align: left; white-space: nowrap;">${h}</th>`).join('') + '</tr>';
+        document.getElementById('excelPreviewHeader').innerHTML = headerHTML;
+
+        // Build table body - group approvals by application
+        const appMap = new Map();
+        approvals.forEach(approval => {
+            const appId = approval.application?.id;
+            if (appId && !appMap.has(appId)) {
+                appMap.set(appId, {
+                    application: approval.application,
+                    dormApproval: null,
+                    counselorApproval: null
+                });
+            }
+
+            if (appId) {
+                const record = appMap.get(appId);
+                if (approval.step === 'dorm_manager') {
+                    record.dormApproval = approval;
+                } else if (approval.step === 'counselor') {
+                    record.counselorApproval = approval;
+                }
+            }
+        });
+
+        const rows = Array.from(appMap.values()).map(record => {
+            const app = record.application;
+            const dorm = record.dormApproval;
+            const counselor = record.counselorApproval;
+
+            return `<tr>
+                <td style="padding: 8px; border: 1px solid #ddd;">${app.id?.substring(0,8) || '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${app.student_name || '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${app.student_id || '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${app.contact_phone || '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${app.leave_date || '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${app.building || '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${app.room_number || '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${new Date(app.created_at).toLocaleString()}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${app.status || '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${dorm?.approver_name || '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${dorm?.decided_at ? new Date(dorm.decided_at).toLocaleString() : '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${dorm?.decision || '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${counselor?.approver_name || '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${counselor?.decided_at ? new Date(counselor.decided_at).toLocaleString() : '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${counselor?.decision || '-'}</td>
+            </tr>`;
+        }).join('');
+
+        document.getElementById('excelPreviewBody').innerHTML = rows;
+        document.getElementById('excelPreviewModal').style.display = 'block';
+    }
+
+    function closeExcelPreview() {
+        document.getElementById('excelPreviewModal').style.display = 'none';
+    }
+
+    async function confirmExcelDownload() {
+        closeExcelPreview();
 
         try {
             const res = await fetch(API_BASE_URL + '/approvals/export/', {
@@ -555,15 +641,11 @@
                 window.URL.revokeObjectURL(url);
                 showToast('导出成功', 'success');
             } else {
-                const error = await res.json();
-                showToast(error.error?.message || '导出失败', 'error');
+                showToast('导出失败', 'error');
             }
         } catch (err) {
-            console.error('Export failed:', err);
-            showToast('导出失败', 'error');
-        } finally {
-            btn.disabled = false;
-            btn.textContent = originalText;
+            console.error('Download failed:', err);
+            showToast('下载失败', 'error');
         }
     }
 
@@ -1170,6 +1252,26 @@
     }
   </script>
 
+<!-- Excel预览模态框 -->
+<div id="excelPreviewModal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 1000; overflow: auto;">
+  <div style="background: white; margin: 20px auto; max-width: 95%; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
+    <div style="padding: 20px; border-bottom: 1px solid #f0f0f0; display: flex; justify-content: space-between; align-items: center;">
+      <h3 style="margin: 0;">审批数据预览</h3>
+      <button onclick="closeExcelPreview()" style="border: none; background: none; font-size: 24px; cursor: pointer; color: #999;">&times;</button>
+    </div>
+    <div style="padding: 20px; overflow-x: auto; max-height: 60vh;">
+      <table id="excelPreviewTable" style="width: 100%; border-collapse: collapse; font-size: 13px;">
+        <thead id="excelPreviewHeader" style="background: #f5f5f5; position: sticky; top: 0;"></thead>
+        <tbody id="excelPreviewBody"></tbody>
+      </table>
+    </div>
+    <div style="padding: 20px; border-top: 1px solid #f0f0f0; display: flex; gap: 12px; justify-content: flex-end;">
+      <button onclick="closeExcelPreview()" class="btn-outline" style="flex: 0;">取消</button>
+      <button onclick="confirmExcelDownload()" class="btn-primary" style="flex: 0;">下载Excel</button>
+    </div>
+  </div>
+</div>
+
 <!-- Toast容器 -->
 <div class="toast-container" id="toastContainer"></div>

exec
/bin/bash -lc 'rtk git show --stat --patch 68d5ea0 -- demo-web/index.html' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
commit 68d5ea09923cc007464ef3d6d7ad0c8c29f5fc5d
Author: caohui-net <13307411234@189.cn>
Date:   Thu Jun 11 14:12:05 2026 +0800

    fix(demo-web): 修复Excel预览日期显示Invalid Date问题
    
    - 添加formatDate辅助函数安全处理日期
    - 检查日期有效性，无效时显示"-"
    - 修复提交时间和审批时间显示问题
    
    Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
---
 demo-web/index.html | 13 ++++++++++---
 1 file changed, 10 insertions(+), 3 deletions(-)

diff --git a/demo-web/index.html b/demo-web/index.html
index bfff14e..0333676 100644
--- a/demo-web/index.html
+++ b/demo-web/index.html
@@ -609,6 +609,13 @@
             const dorm = record.dormApproval;
             const counselor = record.counselorApproval;
 
+            // Helper function to format date safely
+            const formatDate = (dateStr) => {
+                if (!dateStr) return '-';
+                const date = new Date(dateStr);
+                return isNaN(date.getTime()) ? '-' : date.toLocaleString();
+            };
+
             return `<tr>
                 <td style="padding: 8px; border: 1px solid #ddd;">${app.id?.substring(0,8) || '-'}</td>
                 <td style="padding: 8px; border: 1px solid #ddd;">${app.student_name || '-'}</td>
@@ -617,13 +624,13 @@
                 <td style="padding: 8px; border: 1px solid #ddd;">${app.leave_date || '-'}</td>
                 <td style="padding: 8px; border: 1px solid #ddd;">${app.building || '-'}</td>
                 <td style="padding: 8px; border: 1px solid #ddd;">${app.room_number || '-'}</td>
-                <td style="padding: 8px; border: 1px solid #ddd;">${new Date(app.created_at).toLocaleString()}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${formatDate(app.created_at)}</td>
                 <td style="padding: 8px; border: 1px solid #ddd;">${statusMap[app.status] || app.status || '-'}</td>
                 <td style="padding: 8px; border: 1px solid #ddd;">${dorm?.approver_name || '-'}</td>
-                <td style="padding: 8px; border: 1px solid #ddd;">${dorm?.decided_at ? new Date(dorm.decided_at).toLocaleString() : '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${formatDate(dorm?.decided_at)}</td>
                 <td style="padding: 8px; border: 1px solid #ddd;">${dorm?.decision ? decisionMap[dorm.decision] || dorm.decision : '-'}</td>
                 <td style="padding: 8px; border: 1px solid #ddd;">${counselor?.approver_name || '-'}</td>
-                <td style="padding: 8px; border: 1px solid #ddd;">${counselor?.decided_at ? new Date(counselor.decided_at).toLocaleString() : '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${formatDate(counselor?.decided_at)}</td>
                 <td style="padding: 8px; border: 1px solid #ddd;">${counselor?.decision ? decisionMap[counselor.decision] || counselor.decision : '-'}</td>
             </tr>`;
         }).join('');

exec
/bin/bash -lc 'rtk git show --stat --patch afd6d9f -- demo-web/index.html' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
commit afd6d9ffcfdfcd30e3561c57aa42e50f1ffa6de0
Author: caohui-net <13307411234@189.cn>
Date:   Thu Jun 11 14:09:01 2026 +0800

    fix(demo-web): Excel预览状态字段中文化
    
    - 添加statusMap和decisionMap映射表
    - 申请状态显示中文（已通过/待宿管审批等）
    - 审批结果显示中文（已通过/已拒绝/待审批）
    
    Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
---
 demo-web/index.html | 22 +++++++++++++++++++---
 1 file changed, 19 insertions(+), 3 deletions(-)

diff --git a/demo-web/index.html b/demo-web/index.html
index 7f01b50..bfff14e 100644
--- a/demo-web/index.html
+++ b/demo-web/index.html
@@ -559,6 +559,22 @@
     }
 
     function showExcelPreview(approvals) {
+        // Status mapping to Chinese
+        const statusMap = {
+            'pending_dorm_manager': '待宿管审批',
+            'pending_counselor': '待辅导员审批',
+            'pending_dean': '待学工部审批',
+            'approved': '已通过',
+            'rejected': '已拒绝',
+            'draft': '草稿'
+        };
+
+        const decisionMap = {
+            'pending': '待审批',
+            'approved': '已通过',
+            'rejected': '已拒绝'
+        };
+
         // Build table header
         const headers = ['申请ID', '提交人', '学号', '手机号', '离校日期', '楼栋号', '房间号', '提交时间', '审批状态',
                         '宿管员', '宿管审批时间', '宿管审批结果', '辅导员', '辅导员审批时间', '辅导员审批结果'];
@@ -602,13 +618,13 @@
                 <td style="padding: 8px; border: 1px solid #ddd;">${app.building || '-'}</td>
                 <td style="padding: 8px; border: 1px solid #ddd;">${app.room_number || '-'}</td>
                 <td style="padding: 8px; border: 1px solid #ddd;">${new Date(app.created_at).toLocaleString()}</td>
-                <td style="padding: 8px; border: 1px solid #ddd;">${app.status || '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${statusMap[app.status] || app.status || '-'}</td>
                 <td style="padding: 8px; border: 1px solid #ddd;">${dorm?.approver_name || '-'}</td>
                 <td style="padding: 8px; border: 1px solid #ddd;">${dorm?.decided_at ? new Date(dorm.decided_at).toLocaleString() : '-'}</td>
-                <td style="padding: 8px; border: 1px solid #ddd;">${dorm?.decision || '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${dorm?.decision ? decisionMap[dorm.decision] || dorm.decision : '-'}</td>
                 <td style="padding: 8px; border: 1px solid #ddd;">${counselor?.approver_name || '-'}</td>
                 <td style="padding: 8px; border: 1px solid #ddd;">${counselor?.decided_at ? new Date(counselor.decided_at).toLocaleString() : '-'}</td>
-                <td style="padding: 8px; border: 1px solid #ddd;">${counselor?.decision || '-'}</td>
+                <td style="padding: 8px; border: 1px solid #ddd;">${counselor?.decision ? decisionMap[counselor.decision] || counselor.decision : '-'}</td>
             </tr>`;
         }).join('');

exec
/bin/bash -lc 'rtk rg -n "localStorage|auth_token|user_info|logout|escapeHtml|innerHTML|onclick=|application_id|attachment_id|file_name|filename|student_name|comment|approver_name|showExcelPreview|loadApprovals|deanDisplayedApps" demo-web backend/apps -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/approvals/admin.py:9:    search_fields = ['approval_id', 'application__application_id', 'approver__user_id']
backend/apps/approvals/models.py:23:    approver_name = models.CharField(max_length=100)
backend/apps/approvals/models.py:26:    comment = models.TextField(null=True, blank=True)
demo-web/admin/dashboard.html:128:      <button class="btn btn-primary" onclick="testAPI()">测试API调用</button>
demo-web/admin/dashboard.html:129:      <button class="btn btn-danger" onclick="logout()">退出登录</button>
demo-web/admin/dashboard.html:136:      const token = localStorage.getItem('auth_token');
demo-web/admin/dashboard.html:137:      const userInfo = JSON.parse(localStorage.getItem('user_info') || '{}');
demo-web/admin/dashboard.html:159:      const token = localStorage.getItem('auth_token');
demo-web/admin/dashboard.html:164:    function logout() {
demo-web/admin/dashboard.html:165:      localStorage.removeItem('auth_token');
demo-web/admin/dashboard.html:166:      localStorage.removeItem('user_info');
backend/apps/approvals/tests/test_admin_and_export.py:28:            application_id='app_test001',
backend/apps/approvals/tests/test_admin_and_export.py:30:            student_name=self.student.name,
backend/apps/approvals/tests/test_admin_and_export.py:42:            approver_name=self.dorm_manager.name,
backend/apps/approvals/tests/test_admin_and_export.py:51:            {'comment': 'ADMIN代审批'}
backend/apps/approvals/tests/test_admin_and_export.py:63:            {'comment': 'ADMIN驳回'}
backend/apps/approvals/tests/test_rejection_flow.py:69:        return response.data['application_id']
backend/apps/approvals/tests/test_rejection_flow.py:82:            'comment': '宿舍清退通过'
backend/apps/approvals/tests/test_rejection_flow.py:88:        application_id = self._submit_application()
backend/apps/approvals/tests/test_rejection_flow.py:96:        application = Application.objects.get(application_id=application_id)
backend/apps/approvals/tests/test_rejection_flow.py:101:            'comment': '宿舍清退未完成'
backend/apps/approvals/tests/test_rejection_flow.py:111:        application_id = self._submit_application()
backend/apps/approvals/tests/test_rejection_flow.py:112:        application = Application.objects.get(application_id=application_id)
backend/apps/approvals/tests/test_rejection_flow.py:127:            'comment': '材料不齐全'
backend/apps/approvals/migrations/0001_initial.py:21:                ('approver_name', models.CharField(max_length=100)),
backend/apps/approvals/migrations/0001_initial.py:23:                ('comment', models.TextField(blank=True, null=True)),
backend/apps/approvals/tests/test_list_permissions.py:43:            application_id='app_001',
backend/apps/approvals/tests/test_list_permissions.py:45:            student_name='学生',
backend/apps/approvals/tests/test_list_permissions.py:58:            approver_name='辅导员1',
backend/apps/approvals/tests/test_list_permissions.py:67:            approver_name='宿管员1',
backend/apps/approvals/tests/test_list_permissions.py:118:            application_id='app_002',
backend/apps/approvals/tests/test_list_permissions.py:120:            student_name='学生',
backend/apps/approvals/tests/test_list_permissions.py:131:            approver_name='辅导员1',
backend/apps/approvals/tests/test_list_permissions.py:137:            application_id='app_003',
backend/apps/approvals/tests/test_list_permissions.py:139:            student_name='学生',
backend/apps/approvals/tests/test_list_permissions.py:150:            approver_name='辅导员2',
backend/apps/applications/admin.py:7:    list_display = ['application_id', 'student', 'student_name', 'class_id', 'status', 'created_at']
backend/apps/applications/admin.py:9:    search_fields = ['application_id', 'student__user_id', 'student_name', 'class_id']
backend/apps/approvals/tests/test_permissions.py:94:            application_id='app_test001',
backend/apps/approvals/tests/test_permissions.py:96:            student_name='张三',
backend/apps/approvals/tests/test_permissions.py:109:            approver_name='李老师',
backend/apps/approvals/tests/test_permissions.py:123:            approver_name='宿管员1',
backend/apps/approvals/tests/test_permissions.py:133:            {'comment': '同意'},
backend/apps/approvals/tests/test_permissions.py:138:            {'comment': '不同意'},
backend/apps/approvals/tests/test_permissions.py:151:            {'comment': '同意'},
backend/apps/approvals/tests/test_permissions.py:164:            {'comment': '同意'},
backend/apps/approvals/tests/test_permissions.py:177:            {'comment': '不同意'},
backend/apps/approvals/tests/test_permissions.py:189:            {'comment': '同意'},
backend/apps/approvals/tests/test_permissions.py:200:            {'comment': '不同意'},
backend/apps/applications/urls.py:7:    path('<str:application_id>/', views.get_application, name='get_application'),
backend/apps/sso_qingganlian/tests/test_providers.py:24:        self.mock_client.get_user_info.return_value = {
backend/apps/sso_qingganlian/tests/test_providers.py:44:        self.mock_client.get_user_info.assert_called_once()
demo-web/js/api.js:9:    const savedToken = localStorage.getItem('auth_token');
demo-web/js/api.js:10:    const savedUser = localStorage.getItem('user_info');
demo-web/js/api.js:17:                console.log('Auth state restored from localStorage', currentUser);
demo-web/js/api.js:151:async function apiApprove(approvalId, comment) {
demo-web/js/api.js:156:            body: JSON.stringify({ comment: comment })
demo-web/js/api.js:165:async function apiReject(approvalId, comment) {
demo-web/js/api.js:170:            body: JSON.stringify({ comment: comment })
demo-web/index.html:13:    let deanDisplayedApps = new Set(); // Track displayed application IDs for dean deduplication
demo-web/index.html:17:    function escapeHtml(text) {
demo-web/index.html:21:        return div.innerHTML;
demo-web/index.html:41:                const appIdDisplay = app.application_id ? app.application_id.substring(0,8) : '未知';
demo-web/index.html:42:                htmlStr += '<div class="card" style="cursor: pointer;" onclick="showApplicationDetail(\'' + app.application_id + '\')">' +
demo-web/index.html:56:            listContainer.innerHTML = htmlStr;
demo-web/index.html:58:            listContainer.innerHTML = '<div style="text-align:center; padding: 20px; color:#999;">暂无申请记录</div>';
demo-web/index.html:62:    async function loadApprovals(append = false) {
demo-web/index.html:63:        console.log('[DEBUG] loadApprovals called, append=', append, 'currentToken=', currentToken);
demo-web/index.html:69:            deanDisplayedApps.clear(); // Clear deduplication set on fresh load
demo-web/index.html:111:            // For dean/admin: deduplicate by application_id
demo-web/index.html:120:                        if (!deanDisplayedApps.has(appId)) {
demo-web/index.html:122:                            deanDisplayedApps.add(appId); // Track globally across pages
demo-web/index.html:131:                console.log('[DEBUG] Dedup: before', beforeCount, '→ after', filtered.length, 'deanDisplayedApps size:', deanDisplayedApps.size);
demo-web/index.html:173:                const safeAppId = escapeHtml(application.id || approval.id).substring(0,8);
demo-web/index.html:174:                const safeStudentName = escapeHtml(application.student_name || '-');
demo-web/index.html:175:                const safeStudentId = escapeHtml(application.student_id || '-');
demo-web/index.html:177:                htmlStr += '<div class="card" onclick="openApproval(\'' + approval.id + '\')" style="cursor: pointer;">' +
demo-web/index.html:189:                    // Extract real approver name from comment if auto-completed
demo-web/index.html:190:                    let realApprover = approval.approver_name || '-';
demo-web/index.html:191:                    if (approval.comment && approval.comment.includes('已由')) {
demo-web/index.html:192:                        const match = approval.comment.match(/已由(.+?)完成审批/);
demo-web/index.html:197:                    const safeApprover = escapeHtml(realApprover);
demo-web/index.html:218:                listContainer.innerHTML += htmlStr;
demo-web/index.html:220:                listContainer.innerHTML = htmlStr;
demo-web/index.html:235:                listContainer.innerHTML = '<div style="text-align:center; padding: 20px; color:#999;">暂无数据</div>';
demo-web/index.html:261:            loadApprovals();
demo-web/index.html:275:            document.querySelector('#screen-2').innerHTML = '<div class="card"><p style="color: #ff4d4f;">加载失败</p></div>';
demo-web/index.html:283:        const approvalsRes = await fetch(API_BASE_URL + '/approvals/?application_id=' + applicationId, {
demo-web/index.html:294:              '<span style="font-size: 14px; color: #333;">' + (appData.application_id || '-') + '</span>' +
demo-web/index.html:298:              '<span style="font-size: 14px; color: #333;">' + (appData.student_name || '-') + '</span>' +
demo-web/index.html:319:                      '<span style="flex: 1; font-size: 14px; color: #333;">' + att.filename + '</span>' +
demo-web/index.html:320:                      '<button class="btn-outline" style="padding: 4px 12px; font-size: 13px;" onclick="previewAttachment(\'' + att.attachment_id + '\')">预览</button>' +
demo-web/index.html:328:        container.innerHTML = basicInfoHtml + attachmentsHtml + approvalProgressHtml +
demo-web/index.html:329:            '<div style="padding: 20px;"><button class="btn-outline" onclick="showScreen(1); loadMyApplications();" style="width: 100%;">返回</button></div>';
demo-web/index.html:382:                html += '<div style="font-size: 13px; color: #666;">审批人: ' + (approval.approver_name || '待分配') + '</div>';
demo-web/index.html:387:                    const comment = approval.comment && approval.comment.trim() ? approval.comment : '审批人未填写驳回原因';
demo-web/index.html:388:                    html += '<div style="font-size: 13px; color: #ff4d4f; margin-top: 4px; font-weight: 600;">驳回原因: ' + comment + '</div>';
demo-web/index.html:389:                } else if (approval.comment && approval.comment.trim()) {
demo-web/index.html:390:                    html += '<div style="font-size: 13px; color: #666; margin-top: 4px;">意见: ' + approval.comment + '</div>';
demo-web/index.html:411:            const appRes = await fetch(API_BASE_URL + '/applications/' + detail.application_id + '/', {
demo-web/index.html:417:            const attachments = await apiGetAttachments(detail.application_id);
demo-web/index.html:425:                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.application_id || detail.id.substring(0,8)) + '</span>' +
demo-web/index.html:429:                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.student_name || '-') + ' (' + (detail.student_id || '-') + ')</span>' +
demo-web/index.html:460:                        '<span style="font-size: 14px; color: #333; flex: 1;">' + att.file_name + ' (' + (att.file_size / 1024).toFixed(2) + ' KB)</span>' +
demo-web/index.html:461:                        '<button onclick="handleAttachmentPreview(\'' + att.attachment_id + '\')" style="font-size: 14px; color: var(--primary-color); background: none; border: none; cursor: pointer; margin-right: 12px;">预览</button>' +
demo-web/index.html:462:                        (showDownload ? '<button onclick="handleAttachmentDownload(\'' + att.attachment_id + '\', \'' + att.file_name + '\')" style="font-size: 14px; color: var(--primary-color); background: none; border: none; cursor: pointer;">下载</button>' : '') +
demo-web/index.html:584:                    html += '<div style="font-size: 13px; color: #666;">审批人: ' + (detail.approver_name || '待分配') + '</div>';
demo-web/index.html:588:                    if (detail.comment) {
demo-web/index.html:589:                        html += '<div style="font-size: 13px; color: #666; margin-top: 4px;">意见: ' + detail.comment + '</div>';
demo-web/index.html:611:        const comment = document.getElementById('approvalComment').value;
demo-web/index.html:619:            const ok = await apiApprove(currentApprovalId, comment);
demo-web/index.html:620:            if(ok) { showToast('审批通过', 'success'); showScreen(1); loadApprovals(); }
demo-web/index.html:630:        const comment = document.getElementById('approvalComment').value;
demo-web/index.html:638:            const ok = await apiReject(currentApprovalId, comment);
demo-web/index.html:639:            if(ok) { showToast('审批拒绝', 'success'); showScreen(1); loadApprovals(); }
demo-web/index.html:699:                showExcelPreview(data.results);
demo-web/index.html:712:    function showExcelPreview(approvals) {
demo-web/index.html:734:        document.getElementById('excelPreviewHeader').innerHTML = headerHTML;
demo-web/index.html:772:                <td style="padding: 8px; border: 1px solid #ddd;">${app.student_name || '-'}</td>
demo-web/index.html:780:                <td style="padding: 8px; border: 1px solid #ddd;">${dorm?.approver_name || '-'}</td>
demo-web/index.html:783:                <td style="padding: 8px; border: 1px solid #ddd;">${counselor?.approver_name || '-'}</td>
demo-web/index.html:789:        document.getElementById('excelPreviewBody').innerHTML = rows;
demo-web/index.html:834:        banner.innerHTML = `
demo-web/index.html:841:            <button class="btn-outline" onclick="showScreen(1); loadMyApplications();" style="padding: 8px 16px; font-size: 13px;">查看驳回原因</button>
demo-web/index.html:1030:    <button class="nav-tab active" onclick="showScreen(0)">学生申请</button>
demo-web/index.html:1031:    <button class="nav-tab" onclick="showScreen(1)"><span id="nav-approval-text">审批列表</span></button>
demo-web/index.html:1032:    <button class="nav-tab" onclick="showScreen(2)" style="display: none;">申请详情</button>
demo-web/index.html:1042:    <button onclick="logout()" style="padding: 4px 12px; border: 1px solid #d9d9d9; border-radius: 4px; background: white; cursor: pointer;">退出登录</button>
demo-web/index.html:1062:        <button class="btn-primary" onclick="doLogin()">登录</button>
demo-web/index.html:1113:            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
demo-web/index.html:1123:        <button class="btn-primary" onclick="doSubmitApplication()">提交申请</button>
demo-web/index.html:1133:        <button id="export-btn" onclick="exportApprovals()" style="display: none; padding: 8px 16px; background: var(--primary-color); color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px;">导出Excel</button>
demo-web/index.html:1140:      <div class="nav-tab active" style="flex: 1;" onclick="filterApprovals('all')">全部</div>
demo-web/index.html:1141:      <div class="nav-tab" style="flex: 1;" onclick="filterApprovals('pending')">待审批</div>
demo-web/index.html:1142:      <div class="nav-tab" style="flex: 1;" onclick="filterApprovals('decided')">已审批</div>
demo-web/index.html:1150:      <button id="load-more-approvals" onclick="loadApprovals(true)" style="display: none; padding: 10px 20px; border: 1px solid var(--primary-color); background: white; color: var(--primary-color); border-radius: 4px; cursor: pointer;">加载更多</button>
demo-web/index.html:1157:      <button onclick="showScreen(1)" style="border: none; background: none; font-size: 20px; cursor: pointer; color: var(--primary-color); padding: 0;">←</button>
demo-web/index.html:1216:          <button class="btn-primary" style="flex: 1;" onclick="doApprove()">通过</button>
demo-web/index.html:1217:          <button class="btn-outline" style="flex: 1;" onclick="doReject()">拒绝</button>
demo-web/index.html:1324:            loadApprovals();
demo-web/index.html:1367:    function logout() {
demo-web/index.html:1370:      deanDisplayedApps.clear(); // Clear deduplication memory on logout
demo-web/index.html:1442:      fileList.innerHTML = uploadedFiles.map((file, index) => `
demo-web/index.html:1449:          <button class="btn-delete" onclick="removeFile(${index})" type="button">×</button>
demo-web/index.html:1471:      <button onclick="closeExcelPreview()" style="border: none; background: none; font-size: 24px; cursor: pointer; color: #999;">&times;</button>
demo-web/index.html:1480:      <button onclick="closeExcelPreview()" class="btn-outline" style="flex: 0;">取消</button>
demo-web/index.html:1481:      <button onclick="confirmExcelDownload()" class="btn-primary" style="flex: 0;">下载Excel</button>
demo-web/mobile-sso-callback.html:82:          localStorage.setItem('auth_token', data.token);
demo-web/mobile-sso-callback.html:83:          localStorage.setItem('user_info', JSON.stringify(data.user));
demo-web/mobile-sso-callback.html:112:          localStorage.setItem('auth_token', data.token);
demo-web/mobile-sso-callback.html:113:          localStorage.setItem('user_info', JSON.stringify(data.user));
demo-web/mobile-sso-callback.html:141:        document.querySelector('.loading').innerHTML =
demo-web/mobile-sso-callback.html:145:            <button onclick="window.location.href='/'">返回首页</button>
backend/apps/applications/migrations/0001_initial.py:17:                ('application_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
backend/apps/applications/migrations/0001_initial.py:18:                ('student_name', models.CharField(max_length=100)),
demo-web/IMPLEMENTATION_NOTES.md:15:   - Created loadApprovals() to fetch real approval data from /api/v1/approvals/.
backend/apps/approvals/tests/test_state_machine.py:61:            application_id='app_test001',
backend/apps/approvals/tests/test_state_machine.py:63:            student_name='张三',
backend/apps/approvals/tests/test_state_machine.py:76:            approver_name='李老师',
backend/apps/approvals/tests/test_state_machine.py:89:            {'comment': '同意'},
backend/apps/approvals/tests/test_state_machine.py:97:            {'comment': '再次同意'},
backend/apps/approvals/tests/test_state_machine.py:108:            {'comment': '不同意'},
backend/apps/approvals/tests/test_state_machine.py:115:            {'comment': '再次不同意'},
backend/apps/approvals/tests/test_state_machine.py:128:            {'comment': '同意'},
backend/apps/approvals/tests/test_state_machine.py:133:            {'comment': '不同意'},
backend/apps/approvals/tests/test_state_machine.py:149:            approver_name='宿管员',
backend/apps/approvals/tests/test_state_machine.py:156:            {'comment': '同意'},
backend/apps/approvals/tests/test_state_machine.py:161:            {'comment': '不同意'},
backend/apps/sso_qingganlian/providers/qingganlian.py:65:        # Step 2: user_code → user_info
backend/apps/sso_qingganlian/providers/qingganlian.py:66:        user_info_result = self.client.get_user_info(
backend/apps/sso_qingganlian/providers/qingganlian.py:69:        user_data = user_info_result['data']
demo-web/test-integration.sh:89:  if echo "$APPROVAL_DETAIL" | grep -q "student_name"; then
demo-web/test-integration.sh:90:    echo "✓ Approval detail retrieved with student_name"
demo-web/test-integration.sh:93:    echo "✗ Approval detail missing student_name"
demo-web/test-integration.sh:117:  | grep -o '"application_id":"[^"]*"' | head -1 | cut -d'"' -f4)
backend/apps/approvals/views.py:192:    approval.comment = serializer.validated_data.get('comment', '')
backend/apps/approvals/views.py:215:                other_approval.comment = f'已由{approval.approver_name}完成审批，无需重复操作'
backend/apps/approvals/views.py:221:                f"for application {application.application_id} after approval by {actual_approver.user_id}"
backend/apps/approvals/views.py:266:            approver_name=counselor.name,
backend/apps/approvals/views.py:332:    approval.comment = serializer.validated_data.get('comment', '')
backend/apps/approvals/views.py:402:            sanitize_excel_formula(app.application_id),
backend/apps/approvals/views.py:403:            sanitize_excel_formula(app.student_name),
backend/apps/approvals/views.py:411:            sanitize_excel_formula(dorm_approval.approver_name if dorm_approval else ''),
backend/apps/approvals/views.py:414:            sanitize_excel_formula(counselor_approval.approver_name if counselor_approval else ''),
backend/apps/approvals/views.py:431:    response['Content-Disposition'] = f'attachment; filename="approvals_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
backend/apps/sso_qingganlian/views.py:68:        user_info_response = client.get_user_info(tenant_code, user_code, user_type)
backend/apps/sso_qingganlian/views.py:69:        user_info = user_info_response.get('data', {})
backend/apps/sso_qingganlian/views.py:71:        real_name = user_info.get('real_name', '')
backend/apps/sso_qingganlian/views.py:72:        identity_name = user_info.get('identity_name', '学生')
backend/apps/sso_qingganlian/views.py:73:        phone = user_info.get('phone', '')
backend/apps/sso_qingganlian/views.py:74:        user_id_str = user_info.get('number', user_code)
demo-web/admin-sso-callback.html:73:          // 保存JWT token到localStorage
demo-web/admin-sso-callback.html:74:          localStorage.setItem('auth_token', data.token);
demo-web/admin-sso-callback.html:75:          localStorage.setItem('user_info', JSON.stringify(data.user));
demo-web/admin-sso-callback.html:86:        document.querySelector('.loading').innerHTML =
demo-web/admin-sso-callback.html:90:            <button onclick="window.location.href='/'">返回首页</button>
demo-web/admin-sso-callback.html:100:        document.querySelector('.loading').innerHTML =
demo-web/admin-sso-callback.html:104:            <button onclick="window.location.href='/'">返回首页</button>
backend/apps/approvals/serializers.py:7:    id = serializers.CharField(source='application_id')
backend/apps/approvals/serializers.py:9:    student_name = serializers.CharField(source='student.name')
backend/apps/approvals/serializers.py:27:                  'approver_name', 'decision', 'comment', 'decided_at', 'created_at']
backend/apps/approvals/serializers.py:29:                            'approver_name', 'decision', 'comment', 'decided_at', 'created_at']
backend/apps/approvals/serializers.py:40:        fields = ['approval_id', 'step', 'approver_id', 'approver_name',
backend/apps/approvals/serializers.py:41:                  'decided_by_id', 'decided_by_name', 'decision', 'comment', 'decided_at']
backend/apps/approvals/serializers.py:47:    application_id = serializers.CharField(source='application.application_id', read_only=True)
backend/apps/approvals/serializers.py:48:    student_name = serializers.CharField(source='application.student.name', read_only=True)
backend/apps/approvals/serializers.py:62:        fields = ['approval_id', 'application_id', 'student_name', 'student_id',
backend/apps/approvals/serializers.py:65:                  'approver_name', 'decided_by_id', 'decided_by_name', 'decision', 'comment', 'decided_at']
backend/apps/approvals/serializers.py:66:        read_only_fields = ['approval_id', 'application_id', 'student_name', 'student_id',
backend/apps/approvals/serializers.py:69:                            'approver_id', 'approver_name', 'decided_by_id', 'decided_by_name', 'decision', 'decided_at']
backend/apps/approvals/serializers.py:80:    comment = serializers.CharField(required=False, allow_blank=True)
backend/apps/applications/tests/test_p0_fixes.py:33:            application_id='app_001',
backend/apps/applications/tests/test_p0_fixes.py:35:            student_name=self.student.name,
backend/apps/applications/tests/test_p0_fixes.py:44:            application_id='app_002',
backend/apps/applications/tests/test_p0_fixes.py:46:            student_name=self.student.name,
backend/apps/applications/tests/test_p0_fixes.py:59:            application_id='app_001',
backend/apps/applications/tests/test_p0_fixes.py:61:            student_name=self.student.name,
backend/apps/applications/tests/test_p0_fixes.py:70:            application_id='app_002',
backend/apps/applications/tests/test_p0_fixes.py:72:            student_name=self.student.name,
backend/apps/applications/tests/test_p0_fixes.py:100:            application_id='app_pending',
backend/apps/applications/tests/test_p0_fixes.py:102:            student_name=self.student.name,
backend/apps/applications/tests/test_p0_fixes.py:110:            application_id='app_approved',
backend/apps/applications/tests/test_p0_fixes.py:112:            student_name=self.student.name,
backend/apps/applications/tests/test_p0_fixes.py:120:            application_id='app_rejected',
backend/apps/applications/tests/test_p0_fixes.py:122:            student_name=self.student.name,
backend/apps/applications/tests/test_p0_fixes.py:135:            approver_name=self.counselor.name,
backend/apps/applications/tests/test_p0_fixes.py:144:            approver_name=self.counselor.name,
backend/apps/applications/tests/test_p0_fixes.py:153:            approver_name=self.counselor.name,
backend/apps/sso_qingganlian/client.py:128:    def get_user_info(self, tenant_code, user_code, user_type):
backend/apps/applications/tests/test_error_cases.py:144:        application_id = response.data['application_id']
backend/apps/applications/tests/test_error_cases.py:154:        response = self.client.get(f'/api/applications/{application_id}/')
backend/apps/applications/models.py:22:    application_id = models.CharField(max_length=50, primary_key=True)
backend/apps/applications/models.py:24:    student_name = models.CharField(max_length=100)
backend/apps/applications/models.py:47:            ).exclude(application_id=self.application_id).exists()
backend/apps/applications/tests/test_detail_permissions.py:62:        app_id = response.data['application_id']
backend/apps/applications/tests/test_detail_permissions.py:79:        app_id = response.data['application_id']
backend/apps/applications/tests/test_detail_permissions.py:96:        app_id = response.data['application_id']
backend/apps/notifications/services.py:29:    message = f"学生{application.student_name}（{application.student.user_id}）提交了离校申请，请及时审批。"
backend/apps/notifications/services.py:66:        message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
backend/apps/notifications/services.py:117:        message = f"学生{approval.application.student_name}的离校申请已超过{days}天未审批，请及时处理。"
backend/apps/applications/tests/test_list_permissions.py:48:            application_id='app_001',
backend/apps/applications/tests/test_list_permissions.py:50:            student_name='学生1',
backend/apps/applications/tests/test_list_permissions.py:58:            application_id='app_002',
backend/apps/applications/tests/test_list_permissions.py:60:            student_name='学生2',
backend/apps/applications/tests/test_list_permissions.py:73:            approver_name='辅导员1',
backend/apps/applications/tests/test_list_permissions.py:82:        self.assertEqual(response.data['results'][0]['application_id'], 'app_001')
backend/apps/applications/tests/test_list_permissions.py:87:        app_ids = [app['application_id'] for app in response.data['results']]
backend/apps/applications/tests/test_list_permissions.py:95:        self.assertEqual(response.data['results'][0]['application_id'], 'app_001')
backend/apps/applications/tests/test_list_permissions.py:107:        self.assertEqual(response.data['results'][0]['application_id'], 'app_002')
backend/apps/applications/tests/test_application_flow.py:82:        application_id = response.data['application_id']
backend/apps/applications/tests/test_application_flow.py:92:        application = Application.objects.get(application_id=application_id)
backend/apps/applications/tests/test_application_flow.py:97:            'comment': '宿舍清退通过'
backend/apps/applications/tests/test_application_flow.py:117:            'comment': '同意离校'
backend/apps/applications/tests/test_application_flow.py:128:        response = self.client.get(f'/api/applications/{application_id}/')
backend/apps/applications/serializers.py:11:        fields = ['application_id', 'student_id', 'student_name', 'class_id',
backend/apps/applications/serializers.py:13:        read_only_fields = ['application_id', 'student_id', 'student_name',
backend/apps/applications/serializers.py:23:        fields = ['application_id', 'student_id', 'student_name', 'class_id',
backend/apps/applications/serializers.py:26:        read_only_fields = ['application_id', 'student_id', 'student_name',
backend/apps/attachments/serializers.py:16:        file_name = value.name.lower()
backend/apps/attachments/serializers.py:17:        if not any(file_name.endswith(ext) for ext in allowed_extensions):
backend/apps/attachments/serializers.py:26:        fields = ['attachment_id', 'file_name', 'file_size', 'content_type', 'attachment_type', 'uploaded_at']
backend/apps/attachments/serializers.py:27:        read_only_fields = ['attachment_id', 'file_name', 'file_size', 'content_type', 'uploaded_at']
backend/apps/attachments/urls.py:5:    path('applications/<str:application_id>/attachments/', views.attachments_view, name='attachments'),
backend/apps/attachments/urls.py:6:    path('attachments/<str:attachment_id>/download/', views.download_attachment, name='download_attachment'),
backend/apps/attachments/urls.py:7:    path('attachments/<str:attachment_id>/', views.delete_attachment, name='delete_attachment'),
backend/apps/notifications/tests/test_auto_notifications_api.py:87:            application_id='app_test001',
backend/apps/notifications/tests/test_auto_notifications_api.py:89:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:101:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:108:            'comment': '同意'
backend/apps/notifications/tests/test_auto_notifications_api.py:129:            application_id='app_test002',
backend/apps/notifications/tests/test_auto_notifications_api.py:131:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:143:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:150:            'comment': '材料不齐全，请补充'
backend/apps/notifications/tests/test_auto_notifications_api.py:176:            application_id='app_test003',
backend/apps/notifications/tests/test_auto_notifications_api.py:178:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:190:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:197:            'comment': '同意'
backend/apps/notifications/tests/test_auto_notifications_api.py:211:            application_id='app_test004',
backend/apps/notifications/tests/test_auto_notifications_api.py:213:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:225:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:232:            'comment': '再次同意'
backend/apps/attachments/models.py:14:    attachment_id = models.CharField(max_length=50, primary_key=True)
backend/apps/attachments/models.py:19:    file_name = models.CharField(max_length=255)
backend/apps/attachments/models.py:31:        return f"{self.attachment_id} - {self.file_name}"
backend/apps/attachments/migrations/0001_initial.py:21:                ('attachment_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
backend/apps/attachments/migrations/0001_initial.py:24:                ('file_name', models.CharField(max_length=255)),
backend/apps/attachments/views.py:48:def attachments_view(request, application_id):
backend/apps/attachments/views.py:51:        return list_attachments(request, application_id)
backend/apps/attachments/views.py:53:        return upload_attachment(request, application_id)
backend/apps/attachments/views.py:56:def upload_attachment(request, application_id):
backend/apps/attachments/views.py:61:        application = Application.objects.get(application_id=application_id)
backend/apps/attachments/views.py:81:        attachment_id=f'att_{uuid.uuid4().hex[:12]}',
backend/apps/attachments/views.py:86:        file_name=file.name,
backend/apps/attachments/views.py:94:def list_attachments(request, application_id):
backend/apps/attachments/views.py:99:        application = Application.objects.get(application_id=application_id)
backend/apps/attachments/views.py:128:def download_attachment(request, attachment_id):
backend/apps/attachments/views.py:133:        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
backend/apps/attachments/views.py:162:            filename=attachment.file_name,
backend/apps/attachments/views.py:184:def delete_attachment(request, attachment_id):
backend/apps/attachments/views.py:189:        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
backend/apps/notifications/tests/test_auto_notifications.py:51:            application_id='app_test001',
backend/apps/notifications/tests/test_auto_notifications.py:53:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications.py:65:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:83:            application_id='app_test002',
backend/apps/notifications/tests/test_auto_notifications.py:85:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications.py:97:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:114:            application_id='app_test003',
backend/apps/notifications/tests/test_auto_notifications.py:116:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications.py:128:            approver_name=self.dorm_manager.name,
backend/apps/notifications/tests/test_auto_notifications.py:143:            application_id='app_test004',
backend/apps/notifications/tests/test_auto_notifications.py:145:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications.py:157:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:159:            comment='材料不齐全'
backend/apps/notifications/tests/test_auto_notifications.py:174:            application_id='app_test005',
backend/apps/notifications/tests/test_auto_notifications.py:176:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications.py:188:            approver_name=self.counselor.name,
backend/apps/notifications/tests/test_auto_notifications.py:209:            application_id='app_test006',
backend/apps/notifications/tests/test_auto_notifications.py:211:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications.py:223:            approver_name=self.counselor.name,
backend/apps/attachments/tests/test_list.py:82:            application_id='app_test001',
backend/apps/attachments/tests/test_list.py:84:            student_name='张三',
backend/apps/attachments/tests/test_list.py:93:            attachment_id='att_test001',
backend/apps/attachments/tests/test_list.py:98:            file_name='test.pdf',
backend/apps/attachments/tests/test_list.py:108:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:113:        self.assertEqual(response.data['attachments'][0]['attachment_id'], 'att_test001')
backend/apps/attachments/tests/test_list.py:120:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:131:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:142:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:153:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_list.py:168:            f'/api/applications/{self.application.application_id}/attachments/'
backend/apps/attachments/tests/test_upload.py:60:            application_id='app_test001',
backend/apps/attachments/tests/test_upload.py:62:            student_name='张三',
backend/apps/attachments/tests/test_upload.py:71:            application_id='app_test002',
backend/apps/attachments/tests/test_upload.py:73:            student_name='李四',
backend/apps/attachments/tests/test_upload.py:86:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:96:        self.assertIn('attachment_id', response.data)
backend/apps/attachments/tests/test_upload.py:97:        self.assertTrue(response.data['attachment_id'].startswith('att_'))
backend/apps/attachments/tests/test_upload.py:98:        self.assertEqual(len(response.data['attachment_id']), 16)  # att_ + 12 hex chars
backend/apps/attachments/tests/test_upload.py:100:        self.assertEqual(response.data['file_name'], 'test.pdf')
backend/apps/attachments/tests/test_upload.py:108:            f'/api/applications/{self.other_application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:125:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:141:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_upload.py:159:            f'/api/applications/{self.application.application_id}/attachments/',
backend/apps/attachments/tests/test_download.py:60:            application_id='app_test001',
backend/apps/attachments/tests/test_download.py:62:            student_name='张三',
backend/apps/attachments/tests/test_download.py:72:            attachment_id='att_test001',
backend/apps/attachments/tests/test_download.py:77:            file_name='test.pdf',
backend/apps/attachments/tests/test_download.py:87:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_download.py:98:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_download.py:108:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_download.py:122:            f'/api/attachments/{self.attachment.attachment_id}/download/'
backend/apps/attachments/tests/test_delete.py:59:            application_id='app_test001',
backend/apps/attachments/tests/test_delete.py:61:            student_name='张三',
backend/apps/attachments/tests/test_delete.py:71:            attachment_id='att_test001',
backend/apps/attachments/tests/test_delete.py:76:            file_name='test.pdf',
backend/apps/attachments/tests/test_delete.py:86:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_delete.py:101:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_delete.py:116:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/attachments/tests/test_delete.py:130:            f'/api/attachments/{self.attachment.attachment_id}/'
backend/apps/applications/views.py:104:    queryset = queryset.order_by('-created_at', '-application_id')
backend/apps/applications/views.py:139:                                        'details': {'student_id': user.user_id, 'existing_application_id': existing.application_id, 'status': existing.status}}},
backend/apps/applications/views.py:188:                application_id=f'app_{uuid.uuid4().hex[:8]}',
backend/apps/applications/views.py:190:                student_name=user.name,
backend/apps/applications/views.py:206:                approver_name=dorm_manager.name,
backend/apps/applications/views.py:232:def get_application(request, application_id):
backend/apps/applications/views.py:234:        application = Application.objects.get(application_id=application_id)
backend/apps/applications/views.py:237:                                    'details': {'application_id': application_id}}},
backend/apps/applications/views.py:281:        application_id=f'app_{uuid.uuid4().hex[:8]}',
backend/apps/applications/views.py:283:        student_name=user.name,

codex
Excel 预览当前仍用 `innerHTML` 拼接未转义的学生、楼栋、房间和审批人字段，安全修复只覆盖了审批列表的少数列，没有覆盖新增预览、详情页和文件列表。后端字段添加本身较小，但可能增加列表查询的关联访问成本，我会看一下 approvals 视图是否已经 `select_related`。
exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/views.py | sed -n '1,340p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import status
     2	from rest_framework.decorators import api_view, permission_classes, parser_classes
     3	from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
     4	from rest_framework.permissions import IsAuthenticated
     5	from rest_framework.response import Response
     6	from django.utils import timezone
     7	from drf_spectacular.utils import extend_schema, OpenApiParameter
     8	from .models import Application, ApplicationStatus, DormCheckoutStatus
     9	from .serializers import ApplicationSerializer, ApplicationCreateSerializer, ApplicationListSerializer, ApplicationListResponseSerializer
    10	from .pagination import ApplicationLimitOffsetPagination
    11	from .providers import MockDormCheckoutProvider
    12	from .permissions import can_view_application
    13	from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
    14	from apps.users.models import UserRole, User
    15	from apps.notifications.services import notify_application_submitted
    16	from schema import ErrorResponseSerializer
    17	import uuid
    18	import logging
    19	
    20	
    21	@extend_schema(
    22	    methods=['GET'],
    23	    operation_id='applications_list',
    24	    summary='获取申请列表',
    25	    description='获取当前用户的申请列表（学生/辅导员/学工部）',
    26	    parameters=[
    27	        OpenApiParameter('status', str, description='状态过滤'),
    28	        OpenApiParameter('limit', int, description='每页数量（默认20）'),
    29	        OpenApiParameter('offset', int, description='偏移量（默认0）'),
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
    55	@parser_classes([JSONParser, MultiPartParser, FormParser])
    56	def applications_view(request):
    57	    if request.method == 'GET':
    58	        return list_applications(request)
    59	    else:
    60	        return create_application(request)
    61	
    62	
    63	def list_applications(request):
    64	    user = request.user
    65	
    66	    # Student: own applications only
    67	    if user.role == UserRole.STUDENT:
    68	        queryset = Application.objects.filter(student=user)
    69	
    70	    # Dorm Manager: applications with own pending dorm manager approvals
    71	    elif user.role == UserRole.DORM_MANAGER:
    72	        pending_approvals = Approval.objects.filter(
    73	            approver=user,
    74	            step=ApprovalStep.DORM_MANAGER,
    75	            decision=ApprovalDecision.PENDING
    76	        ).values_list('application', flat=True)
    77	        queryset = Application.objects.filter(pk__in=pending_approvals)
    78	
    79	    # Counselor: applications with own pending counselor approvals
    80	    elif user.role == UserRole.COUNSELOR:
    81	        pending_approvals = Approval.objects.filter(
    82	            approver=user,
    83	            step=ApprovalStep.COUNSELOR,
    84	            decision=ApprovalDecision.PENDING
    85	        ).values_list('application', flat=True)
    86	        queryset = Application.objects.filter(pk__in=pending_approvals)
    87	
    88	    # Dean/Admin: view all applications
    89	    elif user.role in [UserRole.DEAN, UserRole.ADMIN]:
    90	        queryset = Application.objects.all()
    91	
    92	    else:
    93	        return Response(
    94	            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
    95	            status=status.HTTP_403_FORBIDDEN
    96	        )
    97	
    98	    # Status filtering
    99	    status_param = request.query_params.get('status')
   100	    if status_param:
   101	        queryset = queryset.filter(status=status_param)
   102	
   103	    # Sort by created_at DESC
   104	    queryset = queryset.order_by('-created_at', '-application_id')
   105	
   106	    # Paginate
   107	    paginator = ApplicationLimitOffsetPagination()
   108	    page = paginator.paginate_queryset(queryset, request)
   109	
   110	    # Serialize
   111	    serializer = ApplicationListSerializer(page, many=True)
   112	
   113	    return paginator.get_paginated_response(serializer.data)
   114	
   115	
   116	def create_application(request):
   117	    from django.db import transaction
   118	
   119	    user = request.user
   120	
   121	    if user.role != UserRole.STUDENT:
   122	        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以提交申请'}},
   123	                        status=status.HTTP_403_FORBIDDEN)
   124	
   125	    serializer = ApplicationCreateSerializer(data=request.data)
   126	    if not serializer.is_valid():
   127	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
   128	                                    'details': serializer.errors}},
   129	                        status=status.HTTP_400_BAD_REQUEST)
   130	
   131	    with transaction.atomic():
   132	        # Check for existing pending/approved applications
   133	        existing = Application.objects.select_for_update().filter(
   134	            student=user,
   135	            status__in=[ApplicationStatus.PENDING_DORM_MANAGER, ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.APPROVED]
   136	        ).first()
   137	        if existing:
   138	            return Response({'error': {'code': 'CONFLICT', 'message': '已有待审批或已通过的申请，不能重复提交',
   139	                                        'details': {'student_id': user.user_id, 'existing_application_id': existing.application_id, 'status': existing.status}}},
   140	                            status=status.HTTP_409_CONFLICT)
   141	
   142	        provider = MockDormCheckoutProvider()
   143	        dorm_status = provider.check_status(user.user_id)
   144	
   145	        if dorm_status.status != DormCheckoutStatus.COMPLETED:
   146	            return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
   147	                                        'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
   148	                                                    'blocking_reason': dorm_status.blocking_reason}}},
   149	                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
   150	
   151	        # Find dorm managers
   152	        dorm_managers = []
   153	        building = user.building
   154	
   155	        if building and building.strip():
   156	            dorm_managers = list(User.objects.filter(
   157	                role=UserRole.DORM_MANAGER,
   158	                building=building,
   159	                active=True
   160	            ).order_by('user_id'))
   161	
   162	        if not dorm_managers:
   163	            from django.conf import settings
   164	            fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')
   165	            try:
   166	                fallback_manager = User.objects.get(role=UserRole.DORM_MANAGER, user_id=fallback_id, active=True)
   167	                dorm_managers = [fallback_manager]
   168	            except User.DoesNotExist:
   169	                return Response({'error': {'code': 'NOT_FOUND', 'message': '无可用宿管员',
   170	                                            'details': {'building': building or '未分配', 'fallback_id': fallback_id}}},
   171	                                status=status.HTTP_404_NOT_FOUND)
   172	
   173	        # Check for existing draft, convert if exists
   174	        draft = Application.objects.select_for_update().filter(student=user, status=ApplicationStatus.DRAFT).first()
   175	
   176	        if draft:
   177	            # Update draft to submitted application
   178	            draft.contact_phone = serializer.validated_data['contact_phone']
   179	            draft.reason = serializer.validated_data.get('reason', '')
   180	            draft.leave_date = serializer.validated_data['leave_date']
   181	            draft.status = ApplicationStatus.PENDING_DORM_MANAGER
   182	            draft.dorm_checkout_status = dorm_status.status
   183	            draft.save()
   184	            application = draft
   185	        else:
   186	            # Create new application
   187	            application = Application.objects.create(
   188	                application_id=f'app_{uuid.uuid4().hex[:8]}',
   189	                student=user,
   190	                student_name=user.name,
   191	                class_id=user.class_id,
   192	                contact_phone=serializer.validated_data['contact_phone'],
   193	                reason=serializer.validated_data.get('reason', ''),
   194	                leave_date=serializer.validated_data['leave_date'],
   195	                status=ApplicationStatus.PENDING_DORM_MANAGER,
   196	                dorm_checkout_status=dorm_status.status
   197	            )
   198	
   199	        # Create approvals
   200	        for dorm_manager in dorm_managers:
   201	            dorm_manager_approval = Approval.objects.create(
   202	                approval_id=f'apv_{uuid.uuid4().hex[:8]}',
   203	                application=application,
   204	                step=ApprovalStep.DORM_MANAGER,
   205	                approver=dorm_manager,
   206	                approver_name=dorm_manager.name,
   207	                decision=ApprovalDecision.PENDING
   208	            )
   209	            notify_application_submitted(application, dorm_manager_approval)
   210	
   211	        # Sync phone to User table
   212	        if not user.phone:
   213	            user.phone = serializer.validated_data['contact_phone']
   214	            user.save()
   215	
   216	    return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
   217	
   218	
   219	@extend_schema(
   220	    operation_id='applications_get',
   221	    summary='获取申请详情',
   222	    description='获取指定申请的详细信息（包括审批记录）',
   223	    responses={
   224	        200: ApplicationSerializer,
   225	        403: ErrorResponseSerializer,
   226	        404: ErrorResponseSerializer,
   227	    },
   228	    tags=['申请']
   229	)
   230	@api_view(['GET'])
   231	@permission_classes([IsAuthenticated])
   232	def get_application(request, application_id):
   233	    try:
   234	        application = Application.objects.get(application_id=application_id)
   235	    except Application.DoesNotExist:
   236	        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在',
   237	                                    'details': {'application_id': application_id}}},
   238	                        status=status.HTTP_404_NOT_FOUND)
   239	
   240	    user = request.user
   241	
   242	    # Check permission using shared helper
   243	    if not can_view_application(user, application):
   244	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
   245	                        status=status.HTTP_403_FORBIDDEN)
   246	
   247	    return Response(ApplicationSerializer(application).data)
   248	
   249	
   250	@extend_schema(
   251	    operation_id='applications_draft',
   252	    summary='获取或创建草稿申请',
   253	    description='学生获取或创建草稿申请，用于附件上传前置',
   254	    responses={
   255	        200: ApplicationSerializer,
   256	        201: ApplicationSerializer,
   257	        403: ErrorResponseSerializer,
   258	    },
   259	    tags=['申请']
   260	)
   261	@api_view(['POST'])
   262	@permission_classes([IsAuthenticated])
   263	def get_or_create_draft(request):
   264	    from django.db import transaction
   265	
   266	    user = request.user
   267	
   268	    if user.role != UserRole.STUDENT:
   269	        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以创建草稿'}},
   270	                        status=status.HTTP_403_FORBIDDEN)
   271	
   272	    with transaction.atomic():
   273	        # Get existing draft or create new one
   274	        draft = Application.objects.select_for_update().filter(student=user, status=ApplicationStatus.DRAFT).first()
   275	
   276	    if draft:
   277	        return Response(ApplicationSerializer(draft).data, status=status.HTTP_200_OK)
   278	
   279	    # Create new draft
   280	    draft = Application.objects.create(
   281	        application_id=f'app_{uuid.uuid4().hex[:8]}',
   282	        student=user,
   283	        student_name=user.name,
   284	        class_id=user.class_id,
   285	        status=ApplicationStatus.DRAFT
   286	    )
   287	
   288	    return Response(ApplicationSerializer(draft).data, status=status.HTTP_201_CREATED)

exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/views.py | sed -n '1,290p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import status
     2	from rest_framework.decorators import api_view, permission_classes
     3	from rest_framework.permissions import IsAuthenticated
     4	from rest_framework.response import Response
     5	from django.utils import timezone
     6	from django.db import transaction
     7	from django.http import HttpResponse
     8	from django.db.models import Prefetch
     9	import logging
    10	from drf_spectacular.utils import extend_schema, OpenApiParameter
    11	from openpyxl import Workbook
    12	from openpyxl.styles import Font, Alignment
    13	from .models import Approval, ApprovalDecision, ApprovalStep
    14	from .serializers import ApprovalSerializer, ApprovalActionSerializer, ApprovalListSerializer, ApprovalListResponseSerializer
    15	from .pagination import ApprovalLimitOffsetPagination
    16	from .validators import approval_step_matches_application_status
    17	from apps.applications.models import Application, ApplicationStatus
    18	from apps.users.models import User, UserRole
    19	from apps.notifications.services import notify_approval_decided
    20	from schema import ErrorResponseSerializer
    21	import uuid
    22	
    23	
    24	def sanitize_excel_formula(value):
    25	    """Sanitize text to prevent Excel formula injection."""
    26	    if not value:
    27	        return value
    28	    value_str = str(value)
    29	    if value_str and value_str[0] in ('=', '+', '-', '@'):
    30	        return "'" + value_str
    31	    return value_str
    32	
    33	
    34	@extend_schema(
    35	    operation_id='approvals_list',
    36	    summary='获取审批列表',
    37	    description='获取当前用户的待审批列表（辅导员或学工部）',
    38	    parameters=[
    39	        OpenApiParameter('decision', str, description='决策过滤：pending/approved/rejected/all（默认pending）'),
    40	        OpenApiParameter('limit', int, description='每页数量（默认20）'),
    41	        OpenApiParameter('offset', int, description='偏移量（默认0）'),
    42	    ],
    43	    responses={
    44	        200: ApprovalListResponseSerializer,
    45	        403: ErrorResponseSerializer,
    46	    },
    47	    tags=['审批']
    48	)
    49	@api_view(['GET'])
    50	@permission_classes([IsAuthenticated])
    51	def list_approvals(request):
    52	    user = request.user
    53	
    54	    # 学生禁止访问
    55	    if user.role == UserRole.STUDENT:
    56	        return Response(
    57	            {'error': {'code': 'FORBIDDEN', 'message': '学生不能访问审批列表'}},
    58	            status=status.HTTP_403_FORBIDDEN
    59	        )
    60	
    61	    # 宿管员: 只看自己的dorm_manager审批
    62	    if user.role == UserRole.DORM_MANAGER:
    63	        queryset = Approval.objects.filter(
    64	            approver=user,
    65	            step=ApprovalStep.DORM_MANAGER
    66	        ).select_related('application', 'application__student', 'approver')
    67	
    68	    # 辅导员: 只看自己的counselor审批
    69	    elif user.role == UserRole.COUNSELOR:
    70	        queryset = Approval.objects.filter(
    71	            approver=user,
    72	            step=ApprovalStep.COUNSELOR
    73	        ).select_related('application', 'application__student', 'approver')
    74	
    75	    # 学工部: 查看所有审批（存档用）
    76	    elif user.role == UserRole.DEAN:
    77	        queryset = Approval.objects.all().select_related('application', 'application__student', 'approver')
    78	
    79	    # 学工管理员: 查看所有审批（管理用）
    80	    elif user.role == UserRole.ADMIN:
    81	        queryset = Approval.objects.all().select_related('application', 'application__student', 'approver')
    82	
    83	    else:
    84	        return Response(
    85	            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
    86	            status=status.HTTP_403_FORBIDDEN
    87	        )
    88	
    89	    # Decision filtering (default: pending)
    90	    decision_param = request.query_params.get('decision', 'pending')
    91	    if decision_param != 'all':
    92	        queryset = queryset.filter(decision=decision_param)
    93	
    94	    # 排序
    95	    queryset = queryset.order_by('-created_at', '-approval_id')
    96	
    97	    # 分页
    98	    paginator = ApprovalLimitOffsetPagination()
    99	    page = paginator.paginate_queryset(queryset, request)
   100	
   101	    # 序列化
   102	    serializer = ApprovalListSerializer(page, many=True)
   103	
   104	    return paginator.get_paginated_response(serializer.data)
   105	
   106	
   107	@extend_schema(
   108	    operation_id='approvals_get',
   109	    summary='获取审批详情',
   110	    description='获取指定审批的详细信息',
   111	    responses={
   112	        200: ApprovalSerializer,
   113	        403: ErrorResponseSerializer,
   114	        404: ErrorResponseSerializer,
   115	    },
   116	    tags=['审批']
   117	)
   118	@api_view(['GET'])
   119	@permission_classes([IsAuthenticated])
   120	def get_approval(request, approval_id):
   121	    try:
   122	        approval = Approval.objects.select_related('application', 'approver').get(approval_id=approval_id)
   123	    except Approval.DoesNotExist:
   124	        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
   125	                        status=status.HTTP_404_NOT_FOUND)
   126	
   127	    user = request.user
   128	
   129	    # Permission check: only the approver or dean/admin can view this approval
   130	    if user.role in [UserRole.DEAN, UserRole.ADMIN] or approval.approver_id == user.user_id:
   131	        return Response(ApprovalSerializer(approval).data)
   132	
   133	    return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
   134	                    status=status.HTTP_403_FORBIDDEN)
   135	
   136	
   137	@extend_schema(
   138	    operation_id='approvals_approve',
   139	    summary='通过审批',
   140	    description='审批人通过指定的审批申请',
   141	    request=ApprovalActionSerializer,
   142	    responses={
   143	        200: ApprovalSerializer,
   144	        400: ErrorResponseSerializer,
   145	        403: ErrorResponseSerializer,
   146	        404: ErrorResponseSerializer,
   147	        409: ErrorResponseSerializer,
   148	    },
   149	    tags=['审批']
   150	)
   151	@api_view(['POST'])
   152	@permission_classes([IsAuthenticated])
   153	@transaction.atomic
   154	def approve_approval(request, approval_id):
   155	    try:
   156	        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
   157	    except Approval.DoesNotExist:
   158	        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
   159	                        status=status.HTTP_404_NOT_FOUND)
   160	
   161	    user = request.user
   162	    # Admin can approve/reject any step
   163	    if user.role != UserRole.ADMIN:
   164	        if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
   165	            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   166	                            status=status.HTTP_403_FORBIDDEN)
   167	        if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
   168	            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   169	                            status=status.HTTP_403_FORBIDDEN)
   170	        if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
   171	            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   172	                            status=status.HTTP_403_FORBIDDEN)
   173	
   174	        if approval.approver_id != user.user_id:
   175	            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   176	                            status=status.HTTP_403_FORBIDDEN)
   177	
   178	    if approval.decision != ApprovalDecision.PENDING:
   179	        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
   180	                        status=status.HTTP_409_CONFLICT)
   181	
   182	    if not approval_step_matches_application_status(approval):
   183	        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
   184	                        status=status.HTTP_409_CONFLICT)
   185	
   186	    serializer = ApprovalActionSerializer(data=request.data)
   187	    if not serializer.is_valid():
   188	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败'}},
   189	                        status=status.HTTP_400_BAD_REQUEST)
   190	
   191	    approval.decision = ApprovalDecision.APPROVED
   192	    approval.comment = serializer.validated_data.get('comment', '')
   193	    approval.decided_at = timezone.now()
   194	    approval.decided_by = user
   195	    approval.save()
   196	
   197	    notify_approval_decided(approval)
   198	
   199	    application = approval.application
   200	    if approval.step == ApprovalStep.DORM_MANAGER:
   201	        # Auto-complete other pending dorm manager approvals for the same building
   202	        # (New requirement: any dorm manager in the building can approve, others see "already approved")
   203	        other_dorm_approvals = Approval.objects.filter(
   204	            application=application,
   205	            step=ApprovalStep.DORM_MANAGER,
   206	            decision=ApprovalDecision.PENDING
   207	        ).exclude(approval_id=approval.approval_id)
   208	
   209	        if other_dorm_approvals.exists():
   210	            now = timezone.now()
   211	            actual_approver = approval.decided_by or approval.approver
   212	            count = other_dorm_approvals.count()
   213	            for other_approval in other_dorm_approvals:
   214	                other_approval.decision = ApprovalDecision.APPROVED
   215	                other_approval.comment = f'已由{approval.approver_name}完成审批，无需重复操作'
   216	                other_approval.decided_at = now
   217	                other_approval.decided_by = actual_approver
   218	                other_approval.save()
   219	            logging.info(
   220	                f"Auto-completed {count} other dorm manager approvals "
   221	                f"for application {application.application_id} after approval by {actual_approver.user_id}"
   222	            )
   223	
   224	        # Check for existing counselor approval to prevent duplicates
   225	        existing_counselor_approval = Approval.objects.filter(
   226	            application=application,
   227	            step=ApprovalStep.COUNSELOR
   228	        ).exists()
   229	
   230	        if existing_counselor_approval:
   231	            return Response({'error': {'code': 'CONFLICT', 'message': '辅导员审批已存在，不能重复创建'}},
   232	                            status=status.HTTP_409_CONFLICT)
   233	
   234	        application.status = ApplicationStatus.PENDING_COUNSELOR
   235	        application.save()
   236	
   237	        # Get counselor by department (Phase 3 design: department-based routing)
   238	        # Note: Original design used ClassMapping (class_id), but Phase 3 user requirements
   239	        # changed to "按学院向辅导员审批" (approval by department/college).
   240	        # Multiple counselors per department are allowed (different classes within department).
   241	        # Selection: order_by('user_id') picks lowest ID for deterministic routing.
   242	        counselors = User.objects.filter(
   243	            role=UserRole.COUNSELOR,
   244	            department=application.student.department,
   245	            active=True
   246	        ).order_by('user_id')
   247	
   248	        if counselors.count() > 1:
   249	            logging.warning(
   250	                f"Multiple counselors found for department {application.student.department}: "
   251	                f"{counselors.count()} matches. Selected {counselors.first().user_id} via order_by('user_id')"
   252	            )
   253	
   254	        counselor = counselors.first()
   255	
   256	        if not counselor:
   257	            return Response({'error': {'code': 'NOT_FOUND', 'message': '该学院辅导员不存在',
   258	                                        'details': {'department': application.student.department}}},
   259	                            status=status.HTTP_404_NOT_FOUND)
   260	
   261	        Approval.objects.create(
   262	            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
   263	            application=application,
   264	            step=ApprovalStep.COUNSELOR,
   265	            approver=counselor,
   266	            approver_name=counselor.name,
   267	            decision=ApprovalDecision.PENDING
   268	        )
   269	    elif approval.step == ApprovalStep.COUNSELOR:
   270	        # Counselor approval completes the process (2-level approval)
   271	        application.status = ApplicationStatus.APPROVED
   272	        application.save()
   273	
   274	    return Response(ApprovalSerializer(approval).data)
   275	
   276	
   277	@extend_schema(
   278	    operation_id='approvals_reject',
   279	    summary='驳回审批',
   280	    description='审批人驳回指定的审批申请',
   281	    request=ApprovalActionSerializer,
   282	    responses={
   283	        200: ApprovalSerializer,
   284	        400: ErrorResponseSerializer,
   285	        403: ErrorResponseSerializer,
   286	        404: ErrorResponseSerializer,
   287	        409: ErrorResponseSerializer,
   288	    },
   289	    tags=['审批']
   290	)

exec
/bin/bash -lc "rtk nl -ba backend/apps/attachments/views.py | sed -n '1,230p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import status
     2	from rest_framework.decorators import api_view, permission_classes, parser_classes
     3	from rest_framework.permissions import IsAuthenticated
     4	from rest_framework.parsers import MultiPartParser, FormParser
     5	from rest_framework.response import Response
     6	from django.http import FileResponse, Http404
     7	from django.utils import timezone
     8	from drf_spectacular.utils import extend_schema, OpenApiResponse
     9	from apps.users.models import UserRole
    10	from apps.applications.models import Application
    11	from apps.applications.permissions import can_view_application
    12	from apps.approvals.models import Approval, ApprovalStep
    13	from .models import Attachment
    14	from .serializers import AttachmentUploadSerializer, AttachmentSerializer, AttachmentListResponseSerializer
    15	from schema import ErrorResponseSerializer
    16	import uuid
    17	
    18	
    19	@extend_schema(
    20	    methods=['GET'],
    21	    operation_id='attachments_list',
    22	    summary='获取附件列表',
    23	    description='获取指定申请的附件列表',
    24	    responses={
    25	        200: AttachmentListResponseSerializer,
    26	        403: ErrorResponseSerializer,
    27	        404: ErrorResponseSerializer,
    28	    },
    29	    tags=['附件']
    30	)
    31	@extend_schema(
    32	    methods=['POST'],
    33	    operation_id='attachments_upload',
    34	    summary='上传附件',
    35	    description='为指定申请上传附件（仅申请所有者可上传）',
    36	    request=AttachmentUploadSerializer,
    37	    responses={
    38	        201: AttachmentSerializer,
    39	        400: ErrorResponseSerializer,
    40	        403: ErrorResponseSerializer,
    41	        404: ErrorResponseSerializer,
    42	    },
    43	    tags=['附件']
    44	)
    45	@api_view(['GET', 'POST'])
    46	@permission_classes([IsAuthenticated])
    47	@parser_classes([MultiPartParser, FormParser])
    48	def attachments_view(request, application_id):
    49	    """Dispatcher for attachment list (GET) and upload (POST)"""
    50	    if request.method == 'GET':
    51	        return list_attachments(request, application_id)
    52	    else:
    53	        return upload_attachment(request, application_id)
    54	
    55	
    56	def upload_attachment(request, application_id):
    57	    user = request.user
    58	
    59	    # Get application
    60	    try:
    61	        application = Application.objects.get(application_id=application_id)
    62	    except Application.DoesNotExist:
    63	        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在'}},
    64	                        status=status.HTTP_404_NOT_FOUND)
    65	
    66	    # Permission: only student who owns the application
    67	    if user.role != UserRole.STUDENT or application.student_id != user.user_id:
    68	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限上传附件'}},
    69	                        status=status.HTTP_403_FORBIDDEN)
    70	
    71	    # Validate
    72	    serializer = AttachmentUploadSerializer(data=request.data)
    73	    if not serializer.is_valid():
    74	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
    75	                                    'details': serializer.errors}},
    76	                        status=status.HTTP_400_BAD_REQUEST)
    77	
    78	    # Create attachment
    79	    file = serializer.validated_data['file']
    80	    attachment = Attachment.objects.create(
    81	        attachment_id=f'att_{uuid.uuid4().hex[:12]}',
    82	        application=application,
    83	        uploaded_by=user,
    84	        file=file,
    85	        attachment_type=serializer.validated_data['attachment_type'],
    86	        file_name=file.name,
    87	        file_size=file.size,
    88	        content_type=file.content_type or 'application/octet-stream'
    89	    )
    90	
    91	    return Response(AttachmentSerializer(attachment).data, status=status.HTTP_201_CREATED)
    92	
    93	
    94	def list_attachments(request, application_id):
    95	    user = request.user
    96	
    97	    # Get application
    98	    try:
    99	        application = Application.objects.get(application_id=application_id)
   100	    except Application.DoesNotExist:
   101	        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在'}},
   102	                        status=status.HTTP_404_NOT_FOUND)
   103	
   104	    # Permission check using shared helper
   105	    if not can_view_application(user, application):
   106	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限查看附件'}},
   107	                        status=status.HTTP_403_FORBIDDEN)
   108	
   109	    # List attachments (exclude soft-deleted)
   110	    attachments = Attachment.objects.filter(application=application, is_deleted=False)
   111	    serializer = AttachmentSerializer(attachments, many=True)
   112	    return Response({'attachments': serializer.data})
   113	
   114	
   115	@extend_schema(
   116	    operation_id='attachments_download',
   117	    summary='下载附件',
   118	    description='下载指定附件文件',
   119	    responses={
   120	        200: OpenApiResponse(description='附件文件内容'),
   121	        403: ErrorResponseSerializer,
   122	        404: ErrorResponseSerializer,
   123	    },
   124	    tags=['附件']
   125	)
   126	@api_view(['GET'])
   127	@permission_classes([IsAuthenticated])
   128	def download_attachment(request, attachment_id):
   129	    user = request.user
   130	
   131	    # Get attachment
   132	    try:
   133	        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
   134	    except Attachment.DoesNotExist:
   135	        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
   136	                        status=status.HTTP_404_NOT_FOUND)
   137	
   138	    # Check if soft-deleted
   139	    if attachment.is_deleted:
   140	        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
   141	                        status=status.HTTP_404_NOT_FOUND)
   142	
   143	    # Permission check using shared helper
   144	    application = attachment.application
   145	    if not can_view_application(user, application):
   146	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限下载附件'}},
   147	                        status=status.HTTP_403_FORBIDDEN)
   148	
   149	    # Return file
   150	    try:
   151	        # Check if preview mode (query param: ?preview=true)
   152	        preview_mode = request.GET.get('preview', 'false').lower() == 'true'
   153	
   154	        # Restrict preview to safe MIME types
   155	        ALLOWED_PREVIEW_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
   156	        if preview_mode and attachment.content_type not in ALLOWED_PREVIEW_TYPES:
   157	            preview_mode = False
   158	
   159	        return FileResponse(
   160	            attachment.file.open('rb'),
   161	            as_attachment=not preview_mode,
   162	            filename=attachment.file_name,
   163	            content_type=attachment.content_type
   164	        )
   165	    except FileNotFoundError:
   166	        return Response({'error': {'code': 'NOT_FOUND', 'message': '文件不存在'}},
   167	                        status=status.HTTP_404_NOT_FOUND)
   168	
   169	
   170	@extend_schema(
   171	    operation_id='attachments_delete',
   172	    summary='删除附件',
   173	    description='软删除指定附件（仅申请所有者可删除）',
   174	    request=None,
   175	    responses={
   176	        204: OpenApiResponse(description='删除成功'),
   177	        403: ErrorResponseSerializer,
   178	        404: ErrorResponseSerializer,
   179	    },
   180	    tags=['附件']
   181	)
   182	@api_view(['DELETE'])
   183	@permission_classes([IsAuthenticated])
   184	def delete_attachment(request, attachment_id):
   185	    user = request.user
   186	
   187	    # Get attachment
   188	    try:
   189	        attachment = Attachment.objects.select_related('application').get(attachment_id=attachment_id)
   190	    except Attachment.DoesNotExist:
   191	        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
   192	                        status=status.HTTP_404_NOT_FOUND)
   193	
   194	    # Check if already deleted
   195	    if attachment.is_deleted:
   196	        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
   197	                        status=status.HTTP_404_NOT_FOUND)
   198	
   199	    # Permission: only student who owns the application
   200	    if user.role != UserRole.STUDENT or attachment.application.student_id != user.user_id:
   201	        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限删除附件'}},
   202	                        status=status.HTTP_403_FORBIDDEN)
   203	
   204	    # Soft delete
   205	    attachment.is_deleted = True
   206	    attachment.deleted_at = timezone.now()
   207	    attachment.save()
   208	
   209	    return Response(status=status.HTTP_204_NO_CONTENT)

exec
/bin/bash -lc 'rtk rg -n "select_related|prefetch_related|ApprovalListSerializer|ApprovalSerializer|paginate|LimitOffset|PageNumber|limit|offset|decision|application_id" backend/apps/approvals backend/backend -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/approvals/admin.py:7:    list_display = ['approval_id', 'application', 'step', 'approver', 'decision', 'decided_at']
backend/apps/approvals/admin.py:8:    list_filter = ['step', 'decision']
backend/apps/approvals/admin.py:9:    search_fields = ['approval_id', 'application__application_id', 'approver__user_id']
backend/apps/approvals/pagination.py:1:from rest_framework.pagination import LimitOffsetPagination
backend/apps/approvals/pagination.py:5:class ApprovalLimitOffsetPagination(LimitOffsetPagination):
backend/apps/approvals/pagination.py:7:    default_limit = 20
backend/apps/approvals/pagination.py:8:    max_limit = 100
backend/apps/approvals/pagination.py:10:    def get_paginated_response(self, data):
backend/apps/approvals/migrations/0001_initial.py:22:                ('decision', models.CharField(choices=[('pending', '待审批'), ('approved', '已通过'), ('rejected', '已驳回')], default='pending', max_length=20)),
backend/apps/approvals/tests/test_state_machine.py:61:            application_id='app_test001',
backend/apps/approvals/tests/test_state_machine.py:77:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_state_machine.py:150:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_admin_and_export.py:28:            application_id='app_test001',
backend/apps/approvals/tests/test_admin_and_export.py:43:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_admin_and_export.py:55:        self.assertEqual(self.approval.decision, ApprovalDecision.APPROVED)
backend/apps/approvals/tests/test_admin_and_export.py:67:        self.assertEqual(self.approval.decision, ApprovalDecision.REJECTED)
backend/apps/approvals/tests/test_rejection_flow.py:69:        return response.data['application_id']
backend/apps/approvals/tests/test_rejection_flow.py:88:        application_id = self._submit_application()
backend/apps/approvals/tests/test_rejection_flow.py:96:        application = Application.objects.get(application_id=application_id)
backend/apps/approvals/tests/test_rejection_flow.py:104:        self.assertEqual(response.data['decision'], ApprovalDecision.REJECTED)
backend/apps/approvals/tests/test_rejection_flow.py:111:        application_id = self._submit_application()
backend/apps/approvals/tests/test_rejection_flow.py:112:        application = Application.objects.get(application_id=application_id)
backend/apps/approvals/tests/test_rejection_flow.py:130:        self.assertEqual(response.data['decision'], ApprovalDecision.REJECTED)
backend/apps/approvals/tests/test_list_permissions.py:43:            application_id='app_001',
backend/apps/approvals/tests/test_list_permissions.py:59:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_list_permissions.py:68:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_list_permissions.py:115:    def test_decision_all_does_not_leak_cross_approver_data(self):
backend/apps/approvals/tests/test_list_permissions.py:118:            application_id='app_002',
backend/apps/approvals/tests/test_list_permissions.py:132:            decision=ApprovalDecision.APPROVED
backend/apps/approvals/tests/test_list_permissions.py:137:            application_id='app_003',
backend/apps/approvals/tests/test_list_permissions.py:151:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_list_permissions.py:154:        # Counselor1 calls decision=all
backend/apps/approvals/tests/test_list_permissions.py:156:        response = self.client.get('/api/approvals/?decision=all')
backend/apps/approvals/views.py:14:from .serializers import ApprovalSerializer, ApprovalActionSerializer, ApprovalListSerializer, ApprovalListResponseSerializer
backend/apps/approvals/views.py:15:from .pagination import ApprovalLimitOffsetPagination
backend/apps/approvals/views.py:39:        OpenApiParameter('decision', str, description='决策过滤：pending/approved/rejected/all（默认pending）'),
backend/apps/approvals/views.py:40:        OpenApiParameter('limit', int, description='每页数量（默认20）'),
backend/apps/approvals/views.py:41:        OpenApiParameter('offset', int, description='偏移量（默认0）'),
backend/apps/approvals/views.py:66:        ).select_related('application', 'application__student', 'approver')
backend/apps/approvals/views.py:73:        ).select_related('application', 'application__student', 'approver')
backend/apps/approvals/views.py:77:        queryset = Approval.objects.all().select_related('application', 'application__student', 'approver')
backend/apps/approvals/views.py:81:        queryset = Approval.objects.all().select_related('application', 'application__student', 'approver')
backend/apps/approvals/views.py:90:    decision_param = request.query_params.get('decision', 'pending')
backend/apps/approvals/views.py:91:    if decision_param != 'all':
backend/apps/approvals/views.py:92:        queryset = queryset.filter(decision=decision_param)
backend/apps/approvals/views.py:98:    paginator = ApprovalLimitOffsetPagination()
backend/apps/approvals/views.py:99:    page = paginator.paginate_queryset(queryset, request)
backend/apps/approvals/views.py:102:    serializer = ApprovalListSerializer(page, many=True)
backend/apps/approvals/views.py:104:    return paginator.get_paginated_response(serializer.data)
backend/apps/approvals/views.py:112:        200: ApprovalSerializer,
backend/apps/approvals/views.py:122:        approval = Approval.objects.select_related('application', 'approver').get(approval_id=approval_id)
backend/apps/approvals/views.py:131:        return Response(ApprovalSerializer(approval).data)
backend/apps/approvals/views.py:143:        200: ApprovalSerializer,
backend/apps/approvals/views.py:178:    if approval.decision != ApprovalDecision.PENDING:
backend/apps/approvals/views.py:191:    approval.decision = ApprovalDecision.APPROVED
backend/apps/approvals/views.py:206:            decision=ApprovalDecision.PENDING
backend/apps/approvals/views.py:214:                other_approval.decision = ApprovalDecision.APPROVED
backend/apps/approvals/views.py:221:                f"for application {application.application_id} after approval by {actual_approver.user_id}"
backend/apps/approvals/views.py:267:            decision=ApprovalDecision.PENDING
backend/apps/approvals/views.py:274:    return Response(ApprovalSerializer(approval).data)
backend/apps/approvals/views.py:283:        200: ApprovalSerializer,
backend/apps/approvals/views.py:318:    if approval.decision != ApprovalDecision.PENDING:
backend/apps/approvals/views.py:331:    approval.decision = ApprovalDecision.REJECTED
backend/apps/approvals/views.py:343:    return Response(ApprovalSerializer(approval).data)
backend/apps/approvals/views.py:380:    applications = Application.objects.select_related('student').prefetch_related(
backend/apps/approvals/views.py:402:            sanitize_excel_formula(app.application_id),
backend/apps/approvals/views.py:413:            dorm_approval.get_decision_display() if dorm_approval else '',
backend/apps/approvals/views.py:416:            counselor_approval.get_decision_display() if counselor_approval else '',
backend/apps/approvals/serializers.py:7:    id = serializers.CharField(source='application_id')
backend/apps/approvals/serializers.py:18:class ApprovalListSerializer(serializers.ModelSerializer):
backend/apps/approvals/serializers.py:27:                  'approver_name', 'decision', 'comment', 'decided_at', 'created_at']
backend/apps/approvals/serializers.py:29:                            'approver_name', 'decision', 'comment', 'decided_at', 'created_at']
backend/apps/approvals/serializers.py:41:                  'decided_by_id', 'decided_by_name', 'decision', 'comment', 'decided_at']
backend/apps/approvals/serializers.py:45:class ApprovalSerializer(serializers.ModelSerializer):
backend/apps/approvals/serializers.py:47:    application_id = serializers.CharField(source='application.application_id', read_only=True)
backend/apps/approvals/serializers.py:62:        fields = ['approval_id', 'application_id', 'student_name', 'student_id',
backend/apps/approvals/serializers.py:65:                  'approver_name', 'decided_by_id', 'decided_by_name', 'decision', 'comment', 'decided_at']
backend/apps/approvals/serializers.py:66:        read_only_fields = ['approval_id', 'application_id', 'student_name', 'student_id',
backend/apps/approvals/serializers.py:69:                            'approver_id', 'approver_name', 'decided_by_id', 'decided_by_name', 'decision', 'decided_at']
backend/apps/approvals/serializers.py:86:    results = ApprovalListSerializer(many=True)
backend/apps/approvals/models.py:25:    decision = models.CharField(max_length=20, choices=ApprovalDecision.choices, default=ApprovalDecision.PENDING)
backend/apps/approvals/tests/test_permissions.py:94:            application_id='app_test001',
backend/apps/approvals/tests/test_permissions.py:110:            decision=ApprovalDecision.PENDING
backend/apps/approvals/tests/test_permissions.py:124:            decision=ApprovalDecision.PENDING

exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/views.py | sed -n '290,450p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   290	)
   291	@api_view(['POST'])
   292	@permission_classes([IsAuthenticated])
   293	@transaction.atomic
   294	def reject_approval(request, approval_id):
   295	    try:
   296	        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
   297	    except Approval.DoesNotExist:
   298	        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
   299	                        status=status.HTTP_404_NOT_FOUND)
   300	
   301	    user = request.user
   302	    # Admin can approve/reject any step
   303	    if user.role != UserRole.ADMIN:
   304	        if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
   305	            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   306	                            status=status.HTTP_403_FORBIDDEN)
   307	        if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
   308	            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   309	                            status=status.HTTP_403_FORBIDDEN)
   310	        if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
   311	            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   312	                            status=status.HTTP_403_FORBIDDEN)
   313	
   314	        if approval.approver_id != user.user_id:
   315	            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
   316	                            status=status.HTTP_403_FORBIDDEN)
   317	
   318	    if approval.decision != ApprovalDecision.PENDING:
   319	        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
   320	                        status=status.HTTP_409_CONFLICT)
   321	
   322	    if not approval_step_matches_application_status(approval):
   323	        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
   324	                        status=status.HTTP_409_CONFLICT)
   325	
   326	    serializer = ApprovalActionSerializer(data=request.data)
   327	    if not serializer.is_valid():
   328	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败'}},
   329	                        status=status.HTTP_400_BAD_REQUEST)
   330	
   331	    approval.decision = ApprovalDecision.REJECTED
   332	    approval.comment = serializer.validated_data.get('comment', '')
   333	    approval.decided_at = timezone.now()
   334	    approval.decided_by = user
   335	    approval.save()
   336	
   337	    notify_approval_decided(approval)
   338	
   339	    application = approval.application
   340	    application.status = ApplicationStatus.REJECTED
   341	    application.save()
   342	
   343	    return Response(ApprovalSerializer(approval).data)
   344	
   345	
   346	@extend_schema(
   347	    operation_id='approvals_export',
   348	    summary='导出审批数据',
   349	    description='导出所有审批数据到Excel（仅学工部）',
   350	    responses={
   351	        200: {'description': 'Excel文件'},
   352	        403: ErrorResponseSerializer,
   353	    },
   354	    tags=['审批']
   355	)
   356	@api_view(['GET'])
   357	@permission_classes([IsAuthenticated])
   358	def export_approvals(request):
   359	    if request.user.role not in [UserRole.DEAN, UserRole.ADMIN]:
   360	        return Response(
   361	            {'error': {'code': 'FORBIDDEN', 'message': '仅学工部/管理员可导出数据'}},
   362	            status=status.HTTP_403_FORBIDDEN
   363	        )
   364	
   365	    # Limit export to 1000 rows max to prevent memory issues
   366	    MAX_EXPORT_ROWS = 1000
   367	
   368	    # Optimize query with Prefetch to avoid N+1
   369	    dorm_prefetch = Prefetch(
   370	        'approvals',
   371	        queryset=Approval.objects.filter(step=ApprovalStep.DORM_MANAGER),
   372	        to_attr='dorm_approvals_list'
   373	    )
   374	    counselor_prefetch = Prefetch(
   375	        'approvals',
   376	        queryset=Approval.objects.filter(step=ApprovalStep.COUNSELOR),
   377	        to_attr='counselor_approvals_list'
   378	    )
   379	
   380	    applications = Application.objects.select_related('student').prefetch_related(
   381	        dorm_prefetch, counselor_prefetch
   382	    ).order_by('-created_at')[:MAX_EXPORT_ROWS]
   383	
   384	    wb = Workbook()
   385	    ws = wb.active
   386	    ws.title = '审批数据'
   387	
   388	    headers = ['申请ID', '提交人', '学号', '手机号', '离校日期', '楼栋号', '房间号', '提交时间', '审批状态',
   389	               '宿管员', '宿管审批时间', '宿管审批结果',
   390	               '辅导员', '辅导员审批时间', '辅导员审批结果']
   391	    ws.append(headers)
   392	
   393	    for cell in ws[1]:
   394	        cell.font = Font(bold=True)
   395	        cell.alignment = Alignment(horizontal='center')
   396	
   397	    for app in applications:
   398	        dorm_approval = app.dorm_approvals_list[0] if app.dorm_approvals_list else None
   399	        counselor_approval = app.counselor_approvals_list[0] if app.counselor_approvals_list else None
   400	
   401	        row = [
   402	            sanitize_excel_formula(app.application_id),
   403	            sanitize_excel_formula(app.student_name),
   404	            sanitize_excel_formula(app.student.user_id if app.student else ''),
   405	            sanitize_excel_formula(app.contact_phone or ''),
   406	            app.leave_date.strftime('%Y-%m-%d') if app.leave_date else '',
   407	            sanitize_excel_formula(app.student.building or '') if app.student else '',
   408	            sanitize_excel_formula(app.student.room_number or '') if app.student else '',
   409	            app.created_at.strftime('%Y-%m-%d %H:%M:%S'),
   410	            app.get_status_display(),
   411	            sanitize_excel_formula(dorm_approval.approver_name if dorm_approval else ''),
   412	            dorm_approval.decided_at.strftime('%Y-%m-%d %H:%M:%S') if dorm_approval and dorm_approval.decided_at else '',
   413	            dorm_approval.get_decision_display() if dorm_approval else '',
   414	            sanitize_excel_formula(counselor_approval.approver_name if counselor_approval else ''),
   415	            counselor_approval.decided_at.strftime('%Y-%m-%d %H:%M:%S') if counselor_approval and counselor_approval.decided_at else '',
   416	            counselor_approval.get_decision_display() if counselor_approval else '',
   417	        ]
   418	        ws.append(row)
   419	
   420	    for column in ws.columns:
   421	        max_length = 0
   422	        column_letter = column[0].column_letter
   423	        for cell in column:
   424	            if cell.value:
   425	                max_length = max(max_length, len(str(cell.value)))
   426	        ws.column_dimensions[column_letter].width = min(max_length + 2, 50)
   427	
   428	    response = HttpResponse(
   429	        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
   430	    )
   431	    response['Content-Disposition'] = f'attachment; filename="approvals_{timezone.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
   432	    wb.save(response)
   433	
   434	    return response

exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/tests/test_admin_and_export.py | sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework.test import APITestCase
     2	from django.contrib.auth import get_user_model
     3	from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
     4	from apps.applications.models import Application, ApplicationStatus
     5	from apps.approvals.views import sanitize_excel_formula
     6	
     7	User = get_user_model()
     8	
     9	
    10	class AdminSuperuserTest(APITestCase):
    11	    """Test ADMIN role can approve/reject any step and decided_by is recorded."""
    12	
    13	    def setUp(self):
    14	        self.student = User.objects.create_user(
    15	            user_id='20200001', name='测试学生',
    16	            role='student', department='计算机学院', building='1号楼'
    17	        )
    18	        self.dorm_manager = User.objects.create_user(
    19	            user_id='M001', name='宿管员1',
    20	            role='dorm_manager', building='1号楼'
    21	        )
    22	        self.admin = User.objects.create_user(
    23	            user_id='A001', name='管理员',
    24	            role='admin'
    25	        )
    26	
    27	        self.application = Application.objects.create(
    28	            application_id='app_test001',
    29	            student=self.student,
    30	            student_name=self.student.name,
    31	            class_id='CS2020',
    32	            contact_phone='13800138000',
    33	            leave_date='2026-07-01',
    34	            status=ApplicationStatus.PENDING_DORM_MANAGER
    35	        )
    36	
    37	        self.approval = Approval.objects.create(
    38	            approval_id='apv_test001',
    39	            application=self.application,
    40	            step=ApprovalStep.DORM_MANAGER,
    41	            approver=self.dorm_manager,
    42	            approver_name=self.dorm_manager.name,
    43	            decision=ApprovalDecision.PENDING
    44	        )
    45	
    46	    def test_admin_can_approve_dorm_manager_step(self):
    47	        """ADMIN can approve dorm manager step."""
    48	        self.client.force_authenticate(user=self.admin)
    49	        response = self.client.post(
    50	            f'/api/approvals/{self.approval.approval_id}/approve/',
    51	            {'comment': 'ADMIN代审批'}
    52	        )
    53	        self.assertEqual(response.status_code, 200)
    54	        self.approval.refresh_from_db()
    55	        self.assertEqual(self.approval.decision, ApprovalDecision.APPROVED)
    56	        self.assertEqual(self.approval.decided_by, self.admin)
    57	
    58	    def test_admin_can_reject_any_step(self):
    59	        """ADMIN can reject any step."""
    60	        self.client.force_authenticate(user=self.admin)
    61	        response = self.client.post(
    62	            f'/api/approvals/{self.approval.approval_id}/reject/',
    63	            {'comment': 'ADMIN驳回'}
    64	        )
    65	        self.assertEqual(response.status_code, 200)
    66	        self.approval.refresh_from_db()
    67	        self.assertEqual(self.approval.decision, ApprovalDecision.REJECTED)
    68	        self.assertEqual(self.approval.decided_by, self.admin)
    69	
    70	
    71	class ExcelExportTest(APITestCase):
    72	    """Test Excel export permissions and formula injection prevention."""
    73	
    74	    def setUp(self):
    75	        self.student = User.objects.create_user(
    76	            user_id='20200002', name='学生',
    77	            role='student'
    78	        )
    79	        self.dean = User.objects.create_user(
    80	            user_id='D001', name='学工部',
    81	            role='dean'
    82	        )
    83	        self.admin = User.objects.create_user(
    84	            user_id='A002', name='管理员',
    85	            role='admin'
    86	        )
    87	
    88	    def test_student_cannot_export(self):
    89	        """Student cannot export."""
    90	        self.client.force_authenticate(user=self.student)
    91	        response = self.client.get('/api/approvals/export/')
    92	        self.assertEqual(response.status_code, 403)
    93	
    94	    def test_dean_can_export(self):
    95	        """DEAN can export."""
    96	        self.client.force_authenticate(user=self.dean)
    97	        response = self.client.get('/api/approvals/export/')
    98	        self.assertEqual(response.status_code, 200)
    99	        self.assertEqual(
   100	            response['Content-Type'],
   101	            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
   102	        )
   103	
   104	    def test_admin_can_export(self):
   105	        """ADMIN can export."""
   106	        self.client.force_authenticate(user=self.admin)
   107	        response = self.client.get('/api/approvals/export/')
   108	        self.assertEqual(response.status_code, 200)
   109	
   110	    def test_sanitize_excel_formula(self):
   111	        """Test formula injection prevention."""
   112	        self.assertEqual(sanitize_excel_formula('=SUM(A1:A10)'), "'=SUM(A1:A10)")
   113	        self.assertEqual(sanitize_excel_formula('+1234'), "'+1234")
   114	        self.assertEqual(sanitize_excel_formula('-cmd'), "'-cmd")
   115	        self.assertEqual(sanitize_excel_formula('@remote'), "'@remote")
   116	        self.assertEqual(sanitize_excel_formula('normal text'), 'normal text')
   117	        self.assertEqual(sanitize_excel_formula(''), '')
   118	        self.assertEqual(sanitize_excel_formula(None), None)

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/serializers.py | sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import serializers
     2	from .models import Application
     3	
     4	
     5	class ApplicationListSerializer(serializers.ModelSerializer):
     6	    """Lean serializer for application lists - no nested approvals"""
     7	    student_id = serializers.CharField(source='student.user_id', read_only=True)
     8	
     9	    class Meta:
    10	        model = Application
    11	        fields = ['application_id', 'student_id', 'student_name', 'class_id',
    12	                  'contact_phone', 'reason', 'leave_date', 'status', 'created_at', 'updated_at']
    13	        read_only_fields = ['application_id', 'student_id', 'student_name',
    14	                            'class_id', 'status', 'created_at', 'updated_at']
    15	
    16	
    17	class ApplicationSerializer(serializers.ModelSerializer):
    18	    student_id = serializers.CharField(source='student.user_id', read_only=True)
    19	    approvals = serializers.SerializerMethodField()
    20	
    21	    class Meta:
    22	        model = Application
    23	        fields = ['application_id', 'student_id', 'student_name', 'class_id',
    24	                  'contact_phone', 'reason', 'leave_date', 'status', 'dorm_checkout_status',
    25	                  'approvals', 'created_at', 'updated_at']
    26	        read_only_fields = ['application_id', 'student_id', 'student_name',
    27	                            'class_id', 'status', 'dorm_checkout_status',
    28	                            'created_at', 'updated_at']
    29	
    30	    def get_approvals(self, obj):
    31	        from apps.approvals.serializers import ApprovalBriefSerializer
    32	        return ApprovalBriefSerializer(obj.approvals.all(), many=True).data
    33	
    34	
    35	class ApplicationCreateSerializer(serializers.Serializer):
    36	    contact_phone = serializers.CharField(max_length=20, required=True)
    37	    reason = serializers.CharField(max_length=500, required=False, allow_blank=True, default='')
    38	    leave_date = serializers.DateField()
    39	
    40	    def validate_leave_date(self, value):
    41	        from django.utils import timezone
    42	        today = timezone.now().date()
    43	        if value < today:
    44	            raise serializers.ValidationError('离校日期不能早于今天')
    45	        return value
    46	
    47	
    48	class ApplicationListResponseSerializer(serializers.Serializer):
    49	    """Schema-only: application list response with pagination"""
    50	    count = serializers.IntegerField()
    51	    results = ApplicationListSerializer(many=True)

exec
/bin/bash -lc "rtk nl -ba backend/apps/approvals/pagination.py | sed -n '1,80p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework.pagination import LimitOffsetPagination
     2	from rest_framework.response import Response
     3	
     4	
     5	class ApprovalLimitOffsetPagination(LimitOffsetPagination):
     6	    """自定义分页器 - 只返回count和results"""
     7	    default_limit = 20
     8	    max_limit = 100
     9	
    10	    def get_paginated_response(self, data):
    11	        return Response({
    12	            'count': self.count,
    13	            'results': data,
    14	        })

exec
/bin/bash -lc 'rtk git diff --check -- demo-web/index.html backend/apps/approvals/serializers.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
exec
/bin/bash -lc "rtk rg -n \"function previewAttachment|previewAttachment\\(|handleAttachmentPreview|apiGetAttachments\" demo-web/index.html demo-web/js/api.js" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
demo-web/js/api.js:199:async function apiGetAttachments(applicationId) {
demo-web/index.html:280:        const attachments = await apiGetAttachments(applicationId);
demo-web/index.html:320:                      '<button class="btn-outline" style="padding: 4px 12px; font-size: 13px;" onclick="previewAttachment(\'' + att.attachment_id + '\')">预览</button>' +
demo-web/index.html:417:            const attachments = await apiGetAttachments(detail.application_id);
demo-web/index.html:461:                        '<button onclick="handleAttachmentPreview(\'' + att.attachment_id + '\')" style="font-size: 14px; color: var(--primary-color); background: none; border: none; cursor: pointer; margin-right: 12px;">预览</button>' +
demo-web/index.html:647:    async function handleAttachmentPreview(attachmentId) {

exec
/bin/bash -lc 'rtk rg -n "application_id" backend/apps/approvals/views.py backend/apps/approvals/tests -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/approvals/views.py:221:                f"for application {application.application_id} after approval by {actual_approver.user_id}"
backend/apps/approvals/views.py:402:            sanitize_excel_formula(app.application_id),
backend/apps/approvals/tests/test_admin_and_export.py:28:            application_id='app_test001',
backend/apps/approvals/tests/test_rejection_flow.py:69:        return response.data['application_id']
backend/apps/approvals/tests/test_rejection_flow.py:88:        application_id = self._submit_application()
backend/apps/approvals/tests/test_rejection_flow.py:96:        application = Application.objects.get(application_id=application_id)
backend/apps/approvals/tests/test_rejection_flow.py:111:        application_id = self._submit_application()
backend/apps/approvals/tests/test_rejection_flow.py:112:        application = Application.objects.get(application_id=application_id)
backend/apps/approvals/tests/test_list_permissions.py:43:            application_id='app_001',
backend/apps/approvals/tests/test_list_permissions.py:118:            application_id='app_002',
backend/apps/approvals/tests/test_list_permissions.py:137:            application_id='app_003',
backend/apps/approvals/tests/test_permissions.py:94:            application_id='app_test001',
backend/apps/approvals/tests/test_state_machine.py:61:            application_id='app_test001',

codex
**审计结论：需要修改。** 主要风险集中在前端：XSS 修复覆盖不完整、分页去重会丢数据、Excel 预览与实际导出不一致。后端新增 serializer 字段本身没有明显 N+1 问题，因为列表查询已 `select_related('application', 'application__student', 'approver')`。

**发现的问题**

1. **高危：XSS 修复不完整，多个新增/相关 UI 仍直接拼接 `innerHTML`**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:290)、[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:770)、[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:425)、[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:1442)

   `escapeHtml()` 只用于审批列表的少数字段。学生详情、审批详情、Excel 预览、上传文件列表仍拼接 `student_name`、`reason`、`comment`、`approver_name`、`file_name`、`building`、`room_number` 等用户/外部输入。文件名还被拼进 `onclick` 属性，单引号可打断 JS 字符串。

   修复建议：不要用字符串拼 HTML。优先用 `document.createElement()` + `textContent` + `addEventListener()`；若短期修复，所有文本字段统一 `escapeHtml()`，所有 URL/ID 参数用 `encodeURIComponent()`，事件参数用 `JSON.stringify()` 或改为 `data-*` 绑定。

2. **高危：循环分页去重会永久丢记录**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:111)、[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:134)、[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:144)

   当前先把本轮抓到的全部唯一 `application.id` 加入 `deanDisplayedApps`，再 `slice(0, 20)` 展示。若累积到 21 条，第 21 条已经进了去重 Set，但不会显示；下一次加载从新的 `offset` 继续，导致这条记录永久消失。

   修复建议：只在实际渲染后再加入 displayed Set；或者维护 `pendingApprovalBuffer`，把超过 20 条的记录缓存给下一页；更好的方案是在后端提供按申请去重的分页接口，前端不要对审批记录做跨页去重。

3. **高危：Excel 预览最多只有 100 条审批记录，且可能缺列，和实际导出不一致**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:693)、[backend/apps/approvals/pagination.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/pagination.py:7)、[backend/apps/approvals/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:380)

   前端请求 `limit=1000`，但后端 `max_limit = 100`，所以预览最多拿 100 条 approval，不是 1000。实际下载接口导出的是最多 1000 个 application，并预取审批记录。预览按 approval 分组，若同一申请的宿管/辅导员记录不在前 100 条内，预览会显示不完整。

   修复建议：新增 `/approvals/export/preview/`，复用导出接口的 application 查询和组装逻辑；或前端按分页循环拉满到 1000，但仍建议以后端 application 为单位生成预览。

4. **中高：`MAX_ITERATIONS` 会在有更多数据时隐藏“加载更多”并显示空数据**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:92)、[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:233)

   如果前 10 页都被前端过滤/去重掉，`displayRecords.length === 0` 会进入空态并隐藏按钮，即使 `currentOffset < totalCount`。`decided` 过滤尤其容易触发，因为前端用 `decision=all` 拉数据后本地过滤。

   修复建议：后端支持 `decision=decided` 或 `decision__in=approved,rejected`；前端在达到迭代上限且 `currentOffset < totalCount` 时不能隐藏加载更多，也不能显示“暂无数据”。

5. **中危：登出没有清理持久化登录态**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:1367)、[demo-web/js/api.js](/home/caohui/projects/graduation-leave-system/demo-web/js/api.js:9)

   `logout()` 只清内存变量，但 `api.js` 会从 `localStorage.auth_token` / `user_info` 恢复登录。SSO callback 会写这些值。用户点退出后刷新页面可能又自动登录。

   修复建议：`logout()` 中同时执行：
   ```js
   localStorage.removeItem('auth_token');
   localStorage.removeItem('user_info');
   uploadedFiles = [];
   renderFileList();
   ```

6. **中危：admin “隐藏审批按钮”只是 UI 控制，后端仍允许 admin 审批/驳回**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:1354)、[backend/apps/approvals/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:162)、[backend/apps/approvals/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:302)

   如果管理员定位为“仅查询”，隐藏按钮不构成权限控制，直接调用 API 仍可审批。测试里还明确断言 admin 可审批。

   修复建议：明确产品语义。若 admin 只读，移除后端 admin bypass，并改测试；若 admin 可代审批，则前端不应隐藏按钮，或至少展示“代审批”权限。

7. **中危：新增学生详情页审批记录接口实际拿不到数据**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:282)、[backend/apps/approvals/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:54)

   学生调用 `/approvals/?application_id=...` 会被 403；后端也没有处理 `application_id` 过滤。结果学生详情审批进度基本只能靠 `app.status` 猜，审批人、时间、驳回原因拿不到。

   修复建议：直接使用 `/applications/{id}/` 返回的 `approvals` 字段；或者新增学生可访问的 application approval history endpoint。

8. **低到中：管理员角色显示修复不完整**
   位置：[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:1279)、[demo-web/index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:1352)

   列表右侧 `role-display` 会显示“管理员”，但登录后顶部 `currentUserRole` 的 `roleMap` 缺少 `admin`，普通登录路径会显示 `(admin)`。

   修复建议：两个 role map 合并成一个全局 `ROLE_LABELS`，避免显示不一致。

**补充检查**

`ApplicationBriefSerializer` 新增 `contact_phone/building/room_number/created_at` 本身可用，且 approvals 列表查询已做 `select_related`，没有看到新增字段导致的明显 N+1。但这些字段会出现在所有审批列表角色响应中，若宿管/辅导员列表不需要全部宿舍信息，建议按角色或接口用途收敛字段。
tokens used
97,159

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
