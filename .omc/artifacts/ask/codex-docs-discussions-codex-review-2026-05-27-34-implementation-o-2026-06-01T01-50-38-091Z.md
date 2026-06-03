# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-01T01:50:38.091Z

## Original task

审查实施顺序和策略

请批判性审查 docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md 中提出的5个问题：

1. **实施顺序：** 先页面后路由 vs 先路由后页面 vs 骨架优先
2. **角色保护：** 防御性保护 vs 依赖路由 vs 混合策略
3. **错误处理：** 页面内实现 vs 提取到api.ts vs 延迟重构
4. **表单验证：** 仅非空 vs 添加长度/日期验证
5. **成功跳转：** 延迟时间、跳转方式、交互保护

**要求：**
- 不要接受当前方案，指出所有风险
- 引用微信小程序最佳实践
- 对每个问题给出明确推荐
- 发现文档中未提到的新问题

按照期望输出格式返回分析结果。

## Final prompt

审查实施顺序和策略

请批判性审查 docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md 中提出的5个问题：

1. **实施顺序：** 先页面后路由 vs 先路由后页面 vs 骨架优先
2. **角色保护：** 防御性保护 vs 依赖路由 vs 混合策略
3. **错误处理：** 页面内实现 vs 提取到api.ts vs 延迟重构
4. **表单验证：** 仅非空 vs 添加长度/日期验证
5. **成功跳转：** 延迟时间、跳转方式、交互保护

**要求：**
- 不要接受当前方案，指出所有风险
- 引用微信小程序最佳实践
- 对每个问题给出明确推荐
- 发现文档中未提到的新问题

按照期望输出格式返回分析结果。

## Raw output

```text
# 问题1：实施顺序

**风险分析：** 当前“完整页面先做完，最后接路由”的顺序不建议接受。它会让学生主流程在一段时间内不可验证，且现有 `login.ts` 仍把所有角色跳到审批列表：[login.ts](/home/caohui/projects/graduation-leave-system/miniprogram/pages/login/login.ts:40)。`approvals` 页也只校验登录，不校验角色：[approvals.ts](/home/caohui/projects/graduation-leave-system/miniprogram/pages/approvals/approvals.ts:16)。

微信官方 `app.json` 文档要求新增页面必须修改 `pages` 数组，且未指定 `entryPagePath` 时 `pages` 第一项是首页；所以注册顺序也有风险，不能误把新页放到第一项。

**推荐方案：** 采用“骨架优先 + 纵向切片”：

1. 创建最小 `student-application` 四件套，`Page({ onLoad/onShow guard })` 可运行。
2. 追加注册到 `app.json`，保持 `pages/login/login` 第一项不变。
3. 立即修改 `login.ts` 角色路由：`student -> student-application`，`counselor/dean -> approvals`。
4. 做最小 smoke：学生登录能进申请页，教师/学工能进审批页，非法角色回登录。
5. 再填充表单、提交、错误处理和成功跳转。

**理由：** 这比“先页面后路由”更早暴露集成问题，也比“先路由后页面”避免跳不存在页面。替代方案 A 的“先写注释路由”是坏味道，未执行代码不会被验证；替代方案 C 只测 404 不够，不能验证登录、权限、页面生命周期和 API 链路。

# 问题2：角色保护

**必要性分析：** 角色保护不能只依赖 `login.ts`。小程序页面可能通过重启恢复、分享、开发者工具路径、历史页面栈等方式进入；微信页面路由文档也明确 `reLaunch` 不是重启 AppService，全局 JS 状态不会因此重置。前端保护不是安全边界，后端才是安全边界，但页面级保护是必要的 UX 和防误入防线。

**推荐时机：** 从骨架页第一版就实现混合策略：

- `login.ts` 做正确角色分流。
- `student-application` 在 `onLoad` 和 `onShow` 都做 `requireRole('student')`。
- 后端继续保留权威角色校验，现有 `create_application` 已限制学生提交：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/views.py:77)。
- 测试要单独覆盖“学生登录路由正确”和“非学生直接访问被拦截”，不要让页面守卫掩盖路由 bug。

**理由：** 仅防御性保护会掩盖登录路由缺陷；仅依赖路由会漏掉直接进入页面；混合策略是正确分层。`console.warn` 可以保留给开发诊断，但不能代替用户可见提示和跳转处理。

# 问题3：错误处理

**YAGNI vs DRY权衡：** 当前已经不是 YAGNI。现有登录页、详情页、审批列表都在重复 `err.error?.message || err.message`，例如：[detail.ts](/home/caohui/projects/graduation-leave-system/miniprogram/pages/detail/detail.ts:66)。新页面再写一套会扩大不一致。

文档里的示例还有实际 bug：后端 `DORM_BLOCKED` 的 `blocking_reason` 位于 `err.error.details.blocking_reason`，不是 `err.error.blocking_reason`：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/views.py:101)。

**推荐策略：** 提取一个轻量通用函数到 `miniprogram/services/api.ts` 或 `miniprogram/services/errors.ts`，例如 `formatApiError(err, fallback, codeMessages?)`。通用层处理 `ApiError`、`Error`、网络失败、401；页面传入领域映射，如 `DORM_BLOCKED`、`CONFLICT`。

**理由：** 不建议做成 `ApiClient` 静态方法，错误格式化不是请求能力本身。也不建议只加 TODO，重复已经存在。重点是正确处理 `details` 可能为对象、数组或字符串，避免页面显示 `[object Object]`。

# 问题4：表单验证

**前端验证边界：** 前端验证用于即时反馈和减少无效请求，不能替代后端。微信 `picker mode=date` 支持 `start/end`，但客户端日期和页面数据都不可信；后端仍必须校验。微信 `textarea` 默认 `maxlength` 是 140，如果业务想要 500 字，必须显式设置。

**推荐范围：** 采用替代方案 C，但不要做特殊字符黑名单：

- `reason.trim()` 非空。
- `reason` 显式长度上限，建议先定为 500 字，并同步后端 serializer/契约。
- `leave_date` 必填、格式为 `YYYY-MM-DD`、不早于今天。
- WXML `picker` 设置 `start="{{today}}"`，提交前再校验一次。
- 不做“特殊字符禁止”，允许正常标点；XSS/SQL 注入由渲染转义、ORM、后端输出策略处理。

**理由：** 只做非空太弱，会把明显错误推给后端。只做前端长度/日期也不够，因为后端当前 `ApplicationCreateSerializer` 没有长度和最小日期约束：[serializers.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/serializers.py:35)。必须同时更新契约和后端，否则前后端行为会漂移。

# 问题5：成功跳转

**UX影响分析：** 当前 1500ms 是微信 `showToast` 默认时长，但提交成功后固定等待 1.5 秒偏慢；延迟期间如果不禁用交互，会出现重复提交、二次跳转、用户返回等竞态。微信官方 `showToast` 支持 `mask` 防止触摸穿透，`redirectTo` 是关闭当前页并跳新页，语义上适合“提交成功后不回到表单”。

**推荐方案：** 使用 `redirectTo`，延迟缩短到 800-1000ms，并加交互保护：

- 提交开始设置 `submitting: true`，按钮 disabled。
- 请求期间 `wx.showLoading({ title: '提交中', mask: true })`，完成后 `wx.hideLoading()`。
- 成功后 `wx.showToast({ title: '提交成功', icon: 'success', duration: 800, mask: true })`。
- `setTimeout` 后 `wx.redirectTo({ url: '/pages/detail/detail?id=' + encodeURIComponent(application_id) })`。
- 失败时恢复 `submitting: false`。
- 跳转失败要兜底提示或回退到申请列表。

**理由：** `navigateTo` 会保留表单页，用户返回后容易看到已提交的旧表单；且小程序 `navigateTo` 页面栈最多十层，不适合作为提交完成后的默认路径。`reLaunch` 太重，会清空所有页面。`redirectTo` 最符合“表单提交完成，当前页失效”的语义。

# 新发现的问题

**问题描述：** 文档没有提到“已有申请”的前置体验。后端 `CONFLICT` 返回 `existing_application_id`：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/views.py:87)。学生进入申请页时可以先查自己的申请，如果已有待审批/已通过，直接跳详情或提示，而不是等提交失败。

**影响范围：** 学生重复提交体验、错误处理、成功/冲突跳转。

**推荐方案：** 页面 `onLoad` 可先 `listApplications` 判断已有有效申请；若不做预查，也必须在 `CONFLICT` 中读取 `details.existing_application_id` 并引导到详情页。

**问题描述：** API 错误结构和类型定义太宽。`ApiError.details?: any` 会让页面随意读取字段，文档示例已经读错字段。

**影响范围：** 所有页面错误展示。

**推荐方案：** 定义类型守卫和错误 formatter，至少覆盖 `VALIDATION_ERROR`、`FORBIDDEN`、`CONFLICT`、`DORM_BLOCKED`、`NOT_FOUND`、401/network fail。

**问题描述：** 当前登录成功路由缺少角色矩阵。`login.ts` 现在所有角色都进审批页，这和新增学生申请页直接冲突。

**影响范围：** 学生登录后的首屏、审批列表权限、端到端验收。

**推荐方案：** 在实现前先写清路由矩阵，并用 smoke 测试锁定：`student -> /pages/student-application/student-application`，`counselor/dean -> /pages/approvals/approvals`，未知角色清 token 并回登录。

**微信官方依据：**  
`app.json pages`、页面路由、`wx.navigateTo`、`wx.redirectTo`、`wx.reLaunch`、`wx.showToast`、`wx.showLoading`、`picker`、`textarea`：  
https://developers.weixin.qq.com/miniprogram/dev/reference/configuration/app.html  
https://developers.weixin.qq.com/miniprogram/dev/framework/app-service/route.html  
https://developers.weixin.qq.com/miniprogram/dev/api/route/wx.navigateTo.html  
https://developers.weixin.qq.com/miniprogram/dev/api/route/wx.redirectTo.html  
https://developers.weixin.qq.com/miniprogram/dev/api/route/wx.reLaunch.html  
https://developers.weixin.qq.com/miniprogram/dev/api/ui/interaction/wx.showToast.html  
https://developers.weixin.qq.com/miniprogram/dev/api/ui/interaction/wx.showLoading.html  
https://developers.weixin.qq.com/miniprogram/dev/component/picker.html  
https://developers.weixin.qq.com/miniprogram/dev/component/textarea.html


OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019e80dc-99aa-78c2-9110-c349e3579def
--------
user
审查实施顺序和策略

请批判性审查 docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md 中提出的5个问题：

1. **实施顺序：** 先页面后路由 vs 先路由后页面 vs 骨架优先
2. **角色保护：** 防御性保护 vs 依赖路由 vs 混合策略
3. **错误处理：** 页面内实现 vs 提取到api.ts vs 延迟重构
4. **表单验证：** 仅非空 vs 添加长度/日期验证
5. **成功跳转：** 延迟时间、跳转方式、交互保护

**要求：**
- 不要接受当前方案，指出所有风险
- 引用微信小程序最佳实践
- 对每个问题给出明确推荐
- 发现文档中未提到的新问题

按照期望输出格式返回分析结果。
codex
我会先读取项目里的协作与审查规则，再打开目标讨论文档，按项目约定输出审查结论。
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

codex
项目规则要求 shell 命令都经 `rtk` 代理；我刚才为了读取规则先直接执行了一次，后续命令会按规则加 `rtk`。现在我会读取目标文档和相关前端实现上下文，避免只凭文档表面判断。
exec
/bin/bash -lc "rtk rg -n \"wx\\.navigate|wx\\.redirect|wx\\.reLaunch|wx\\.showToast|Page\\(|Component\\(|role|角色|pages/|app\\.json|permission|auth|login\" -S ." in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 实施顺序挑战 - Codex审查请求

**创建时间：** 2026-06-01T01:45  
**审查类型：** 实施策略审查  
**审查人：** Codex

---

## 审查背景

Codex已完成student-application页面方案审查，给出"需要小幅调整后再实施"结论。

**当前计划的实施顺序：**
1. 创建student-application.ts（表单逻辑+角色保护+错误格式化）
2. 创建student-application.wxml（表单UI）
3. 创建student-application.wxss（样式）
4. 创建student-application.json（页面配置）
5. 注册页面到app.json
6. 修改login.ts添加角色路由

---

## 需要你批判性审查的问题

### 问题1：实施顺序是否合理？

**当前方案：** 先完整实现student-application页面（4个文件），最后修改login.ts路由

**潜在问题：**
- 如果先实现页面但不修改路由，学生登录后无法访问新页面
- 如果先修改路由但页面不存在，会导致404错误
- 4个文件一次性创建，如果中途发现问题，回滚成本高

**替代方案A：** 先修改login.ts路由（添加条件判断但暂时注释），再实现页面，最后取消注释
**替代方案B：** 先创建空页面骨架（4个文件最小化内容），注册+路由，再逐步填充逻辑
**替代方案C：** 保持当前顺序，但在app.json注册后立即测试404，确认路由前页面可访问

**你的任务：** 批判当前顺序，指出风险，推荐最优方案

---

### 问题2：角色保护的实施时机？

**当前方案：** 在student-application.ts的onLoad中检查角色

```typescript
onLoad() {
  const userInfo = app.globalData.userInfo;
  if (!userInfo || userInfo.role !== 'student') {
    wx.reLaunch({ url: '/pages/login/login' });
    return;
  }
  // ...
}
```

**潜在问题：**
- 如果login.ts路由已正确实现，角色保护是否冗余？
- 如果用户直接输入URL或通过其他方式访问，角色保护是必要的
- 但如果login.ts路由有bug，角色保护会掩盖路由问题

**替代方案A：** 先不实现角色保护，依赖login.ts路由，测试通过后再添加防御性保护
**替代方案B：** 先实现角色保护，即使login.ts路由有bug也能防御
**替代方案C：** 实现角色保护，但添加console.warn提示"不应通过此路径访问"

**你的任务：** 分析角色保护的必要性和实施时机

---

### 问题3：错误处理的实施优先级？

**当前方案：** 在student-application.ts中实现错误格式化函数

```typescript
function formatError(err: any): string {
  if (err.error?.code === 'DORM_BLOCKED') {
    return `宿舍清退未完成：${err.error.blocking_reason || '请联系宿管'}`;
  }
  if (err.error?.code === 'CONFLICT') {
    return '您已有待审批或已通过的申请';
  }
  if (err.error?.code === 'VALIDATION_ERROR') {
    return err.error.details || '表单验证失败';
  }
  return err.error?.message || err.message || '操作失败';
}
```

**潜在问题：**
- 这个函数只在student-application页面使用，是否应该提取到services/api.ts作为通用工具？
- 如果未来其他页面也需要类似错误处理，会导致代码重复
- 但如果现在提取，可能过度设计（YAGNI原则）

**替代方案A：** 先在页面内实现，等第二个页面需要时再提取
**替代方案B：** 现在就提取到api.ts，作为ApiClient的静态方法或独立函数
**替代方案C：** 实现为页面内函数，但添加TODO注释标记未来重构点

**你的任务：** 权衡YAGNI vs DRY，推荐错误处理的实施策略

---

### 问题4：表单验证的实施范围？

**当前方案：** 提交时验证reason非空且trim后非空，leave_date非空

**潜在问题：**
- 是否需要验证leave_date不早于今天？（虽然picker设置了start=today，但用户可能修改系统时间）
- 是否需要验证reason长度上限？（避免超长文本导致UI问题或数据库截断）
- 是否需要验证reason不包含特殊字符？（防止XSS或SQL注入，虽然后端应该处理）

**替代方案A：** 只验证非空，其他交给后端
**替代方案B：** 添加长度验证（如reason最多500字）
**替代方案C：** 添加日期验证（不早于今天）+ 长度验证

**你的任务：** 确定前端验证的合理边界

---

### 问题5：成功后跳转的实施细节？

**当前方案：** 成功后showToast，然后redirectTo到详情页

```typescript
wx.showToast({ title: '提交成功', icon: 'success' });
setTimeout(() => {
  wx.redirectTo({ url: `/pages/detail/detail?id=${res.application_id}` });
}, 1500);
```

**潜在问题：**
- 1500ms延迟是否合理？用户可能觉得慢
- 使用redirectTo会清空页面栈，用户无法返回表单页（但这可能是期望行为）
- 如果用户在延迟期间点击其他按钮，可能导致竞态条件

**替代方案A：** 缩短延迟到500ms
**替代方案B：** 不延迟，直接跳转（toast可能看不到）
**替代方案C：** 使用navigateTo而非redirectTo，允许用户返回
**替代方案D：** 在跳转前禁用所有交互（添加全屏遮罩）

**你的任务：** 评估跳转时机和方式的用户体验影响

---

## 审查要求

1. **批判性思考：** 不要接受当前方案，指出所有潜在问题
2. **提供证据：** 引用微信小程序最佳实践、常见坑点、性能考虑
3. **权衡分析：** 对每个问题的替代方案进行利弊分析
4. **明确推荐：** 给出你认为最优的实施策略，并说明理由
5. **发现新问题：** 如果发现我没有提到的问题，请指出

---

## 期望输出

```markdown
# 问题1：实施顺序
**风险分析：** ...
**推荐方案：** ...
**理由：** ...

# 问题2：角色保护
**必要性分析：** ...
**推荐时机：** ...
**理由：** ...

# 问题3：错误处理
**YAGNI vs DRY权衡：** ...
**推荐策略：** ...
**理由：** ...

# 问题4：表单验证
**前端验证边界：** ...
**推荐范围：** ...
**理由：** ...

# 问题5：成功跳转
**UX影响分析：** ...
**推荐方案：** ...
**理由：** ...

# 新发现的问题
**问题描述：** ...
**影响范围：** ...
**推荐方案：** ...
```

exec
/bin/bash -lc 'rtk rg --files | head -200' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
task_plan.md
progress.md
CLAUDE.md
AGENTS.md
docs/api/contract-v0.2.md
docs/week3-day0-seed-data-requirements.md
docs/week3-day0-acceptance-checklist.md
docs/templates/宿舍清退数据模板.csv
docs/templates/学生基本信息导入模板.csv
docs/templates/班级辅导员对应关系导入模板.csv
docs/templates/辅导员基本信息导入模板.csv
docs/微信小程序申请说明.md
docs/superpowers/plans/2026-05-27-implementation-plan.md
docs/数据对接说明文档.md
docs/微信小程序备案说明.md
docs/Codex审查流程指南.md
docs/plans/week-0-1-execution-plan.md
docs/codex-review-protocol.md
docs/week3-day0-environment-strategy.md
docs/用户设计说明书.md
docs/PROJECT-SUMMARY.md
docs/contracts/contract-v0.2.md
docs/contracts/contract-v0.1.md
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md
docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md
docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md
docs/discussions/week3-day3-planning-2026-05-30/01-claude-day3-proposal.md
docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md
docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md
docs/discussions/week3-day1-review-2026-05-30/19-claude-deadlock-analysis.md
docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md
docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md
docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md
docs/discussions/week3-day1-review-2026-05-30/09-codex-execution-review.md
tests/test_p0_fixes.sh
tests/smoke_test.sh
backend/data/templates/counselors_template.csv
backend/data/templates/class_mappings_template.csv
backend/data/templates/students_template.csv
backend/requirements/base.txt
backend/requirements/dev.txt
backend/requirements/prod.txt
backend/config/__init__.py
backend/config/urls.py
backend/config/settings/__init__.py
backend/config/settings/base.py
backend/config/settings/prod.py
backend/config/settings/dev.py
backend/config/wsgi.py
backend/apps/approvals/validators.py
backend/apps/approvals/__init__.py
backend/apps/approvals/admin.py
backend/apps/approvals/pagination.py
backend/apps/approvals/urls.py
backend/apps/approvals/migrations/__init__.py
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
miniprogram/app.json
miniprogram/app.ts
miniprogram/sitemap.json
backend/apps/applications/__init__.py
backend/apps/applications/admin.py
backend/apps/applications/providers.py
backend/apps/applications/pagination.py
backend/apps/applications/urls.py
backend/apps/applications/migrations/0003_application_unique_student_application.py
backend/apps/applications/migrations/__init__.py
backend/apps/applications/migrations/0002_initial.py
backend/apps/applications/migrations/0001_initial.py
backend/apps/applications/migrations/0004_remove_unique_student_constraint.py
backend/apps/applications/tests/__init__.py
backend/apps/applications/tests/test_p0_fixes.py
backend/apps/applications/tests/test_error_cases.py
backend/apps/applications/tests/test_list_permissions.py
backend/apps/applications/tests/test_constraints.py
backend/apps/applications/tests/test_application_flow.py
backend/apps/applications/views.py
backend/apps/applications/serializers.py
backend/apps/applications/models.py
backend/apps/users/__init__.py
backend/apps/users/admin.py
backend/apps/users/urls.py
backend/apps/users/migrations/__init__.py
backend/apps/users/migrations/0001_initial.py
backend/apps/users/apps.py
backend/apps/users/class_mapping.py
backend/apps/users/views.py
backend/apps/users/serializers.py
backend/apps/users/models.py
backend/apps/users/management/__init__.py
backend/apps/users/management/commands/__init__.py
backend/apps/users/management/commands/import_csv.py
backend/apps/users/management/commands/seed_data.py
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md
backend/manage.py
backend/Dockerfile
毕业离校系统用户文档.zip
docker-compose.yml
findings.md
frontend/services/mock.ts
frontend/services/api.ts
frontend/types/api.ts
miniprogram/pages/approvals/approvals.ts
miniprogram/pages/approvals/approvals.wxml
miniprogram/pages/approvals/approvals.wxss
miniprogram/pages/login/login.wxml
miniprogram/pages/login/login.wxss
miniprogram/pages/login/login.ts
miniprogram/pages/detail/detail.ts
miniprogram/pages/detail/detail.wxml
miniprogram/pages/detail/detail.wxss
miniprogram/project.config.json
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md
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
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md
docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md
docs/数据确认清单.md
docs/design/2026-05-27-system-design.md
docs/discussions/codex-review-2026-05-27/02-architecture-response.md
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md
docs/discussions/codex-review-2026-05-27/04-database-review.md
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md
docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md
docs/discussions/week3-day1-review-2026-05-30/16-codex-authorization-ruling.md
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md
docs/discussions/codex-review-2026-05-30/51-p1-fixes-confirmation-request.md
docs/discussions/week3-direction-2026-05-30/05-claude-final-response.md
docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md
docs/discussions/week3-direction-2026-05-30/06-consensus.md
docs/discussions/week3-direction-2026-05-30/01-claude-proposal.md
docs/discussions/week3-direction-2026-05-30/03-claude-response.md
docs/discussions/week3-direction-2026-05-30/02-codex-review.md
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md
docs/discussions/codex-review-2026-05-30/52-p1-fixes-codex-confirmation-response.md
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md

 succeeded in 177ms:
codex
目标文档的“期望输出”已经明确，我会按它的章节结构返回。接下来只补充关键代码上下文：当前路由注册、登录跳转、API 客户端和详情页的既有模式。
exec
/bin/bash -lc 'rtk nl -ba miniprogram/pages/detail/detail.ts' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk nl -ba miniprogram/pages/login/login.ts' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk nl -ba miniprogram/app.ts' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk nl -ba miniprogram/pages/approvals/approvals.ts' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk nl -ba miniprogram/services/api.ts' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk nl -ba miniprogram/app.json' in /home/caohui/projects/graduation-leave-system
 succeeded in 230ms:
 succeeded in 354ms:
 succeeded in 319ms:
 succeeded in 375ms:
     1	import { createDefaultApiClient } from '../../services/api';
     2	
     3	const app = getApp<IAppOption>();
     4	const apiClient = createDefaultApiClient();
     5	
     6	Page({
     7	  data: {
     8	    userId: '',
     9	    password: '',
    10	    loading: false,
    11	    error: '',
    12	  },
    13	
    14	  onUserIdInput(e: any) {
    15	    this.setData({ userId: e.detail.value });
    16	  },
    17	
    18	  onPasswordInput(e: any) {
    19	    this.setData({ password: e.detail.value });
    20	  },
    21	
    22	  async onLogin() {
    23	    const { userId, password } = this.data;
    24	
    25	    if (!userId || !password) {
    26	      this.setData({ error: '请输入用户ID和密码' });
    27	      return;
    28	    }
    29	
    30	    this.setData({ loading: true, error: '' });
    31	
    32	    try {
    33	      const res = await apiClient.login({ user_id: userId, password });
    34	
    35	      wx.setStorageSync('token', res.access_token);
    36	      wx.setStorageSync('userInfo', res.user);
    37	      app.globalData.token = res.access_token;
    38	      app.globalData.userInfo = res.user;
    39	
    40	      wx.redirectTo({ url: '/pages/approvals/approvals' });
    41	    } catch (err: any) {
    42	      this.setData({
    43	        error: err.error?.message || err.message || '登录失败',
    44	        loading: false,
    45	      });
    46	    }
    47	  },
    48	});

 succeeded in 354ms:
     1	{
     2	  "pages": [
     3	    "pages/login/login",
     4	    "pages/approvals/approvals",
     5	    "pages/detail/detail"
     6	  ],
     7	  "window": {
     8	    "navigationBarTitleText": "毕业离校申请系统",
     9	    "navigationBarBackgroundColor": "#1890ff",
    10	    "navigationBarTextStyle": "white",
    11	    "backgroundColor": "#f5f5f5"
    12	  },
    13	  "sitemapLocation": "sitemap.json"
    14	}

 succeeded in 517ms:
codex
已有代码显示学生登录目前会统一跳到审批列表，详情页和审批列表只做了“已登录”检查，没有统一的角色守卫或错误格式化。为了判断验证边界，我再看一下 API 类型和后端当前约束。
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
/bin/bash -lc 'rtk nl -ba backend/apps/applications/serializers.py' in /home/caohui/projects/graduation-leave-system
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
    12	                  'reason', 'leave_date', 'status', 'created_at', 'updated_at']
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
    24	                  'reason', 'leave_date', 'status', 'dorm_checkout_status',
    25	                  'approvals', 'created_at', 'updated_at']
    26	        read_only_fields = ['application_id', 'student_id', 'student_name',
    27	                            'class_id', 'status', 'dorm_checkout_status',
    28	                            'created_at', 'updated_at']
    29	
    30	    def get_approvals(self, obj):
    31	        from apps.approvals.serializers import ApprovalSerializer
    32	        return ApprovalSerializer(obj.approvals.all(), many=True).data
    33	
    34	
    35	class ApplicationCreateSerializer(serializers.Serializer):
    36	    reason = serializers.CharField()
    37	    leave_date = serializers.DateField()

exec
/bin/bash -lc 'rtk nl -ba miniprogram/types/api.ts' in /home/caohui/projects/graduation-leave-system
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
/bin/bash -lc 'rtk rg -n "ApplicationCreateRequest|reason|leave_date|VALIDATION_ERROR|DORM_BLOCKED|CONFLICT|FORBIDDEN" docs/contracts docs/api backend/apps/applications miniprogram -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/applications/providers.py:11:    blocking_reason: Optional[str]
backend/apps/applications/providers.py:22:                blocking_reason=None,
backend/apps/applications/providers.py:29:                blocking_reason=None,
backend/apps/applications/providers.py:36:                blocking_reason="未提交清退申请",
backend/apps/applications/providers.py:43:                blocking_reason=None,
backend/apps/applications/providers.py:50:                blocking_reason="学生信息不存在",
backend/apps/applications/providers.py:59:            blocking_reason="未在宿舍系统中找到记录",
backend/apps/applications/migrations/0001_initial.py:20:                ('reason', models.TextField()),
backend/apps/applications/migrations/0001_initial.py:21:                ('leave_date', models.DateField()),
backend/apps/applications/tests/test_p0_fixes.py:37:            reason='First attempt',
backend/apps/applications/tests/test_p0_fixes.py:38:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:48:            reason='Second attempt',
backend/apps/applications/tests/test_p0_fixes.py:49:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:63:            reason='First attempt',
backend/apps/applications/tests/test_p0_fixes.py:64:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:74:            reason='Second attempt',
backend/apps/applications/tests/test_p0_fixes.py:75:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:104:            reason='Pending',
backend/apps/applications/tests/test_p0_fixes.py:105:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:114:            reason='Approved',
backend/apps/applications/tests/test_p0_fixes.py:115:            leave_date='2024-06-30',
backend/apps/applications/tests/test_p0_fixes.py:124:            reason='Rejected',
backend/apps/applications/tests/test_p0_fixes.py:125:            leave_date='2024-06-30',
backend/apps/applications/tests/test_error_cases.py:69:            'reason': '毕业离校',
backend/apps/applications/tests/test_error_cases.py:70:            'leave_date': '2024-06-30'
backend/apps/applications/tests/test_error_cases.py:73:        self.assertEqual(response.data['error']['code'], 'DORM_BLOCKED')
backend/apps/applications/tests/test_error_cases.py:87:            'reason': '毕业离校',
backend/apps/applications/tests/test_error_cases.py:88:            'leave_date': '2024-06-30'
backend/apps/applications/tests/test_error_cases.py:94:            'reason': '毕业离校',
backend/apps/applications/tests/test_error_cases.py:95:            'leave_date': '2024-06-30'
backend/apps/applications/tests/test_error_cases.py:97:        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
backend/apps/applications/tests/test_error_cases.py:98:        self.assertEqual(response.data['error']['code'], 'CONFLICT')
backend/apps/applications/tests/test_error_cases.py:111:            'reason': '毕业离校',
backend/apps/applications/tests/test_error_cases.py:112:            'leave_date': '2024-06-30'
backend/apps/applications/tests/test_error_cases.py:125:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/applications/tests/test_error_cases.py:126:        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
backend/apps/applications/tests/test_error_cases.py:151:            'reason': '毕业离校'
backend/apps/applications/tests/test_error_cases.py:152:            # Missing leave_date
backend/apps/applications/tests/test_error_cases.py:155:        self.assertEqual(response.data['error']['code'], 'VALIDATION_ERROR')
backend/apps/applications/tests/test_list_permissions.py:44:            reason='测试',
backend/apps/applications/tests/test_list_permissions.py:45:            leave_date='2024-07-01',
backend/apps/applications/tests/test_list_permissions.py:54:            reason='测试',
backend/apps/applications/tests/test_list_permissions.py:55:            leave_date='2024-07-01',
backend/apps/applications/tests/test_constraints.py:48:                'reason': '毕业离校',
backend/apps/applications/tests/test_constraints.py:49:                'leave_date': '2024-06-30'
backend/apps/applications/tests/test_constraints.py:59:                'reason': '再次提交',
backend/apps/applications/tests/test_constraints.py:60:                'leave_date': '2024-07-01'
backend/apps/applications/tests/test_constraints.py:64:        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
backend/apps/applications/tests/test_application_flow.py:61:            'reason': '毕业离校',
backend/apps/applications/tests/test_application_flow.py:62:            'leave_date': '2024-06-30'
backend/apps/applications/views.py:52:            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
backend/apps/applications/views.py:53:            status=status.HTTP_403_FORBIDDEN
backend/apps/applications/views.py:78:        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以提交申请'}},
backend/apps/applications/views.py:79:                        status=status.HTTP_403_FORBIDDEN)
backend/apps/applications/views.py:87:        return Response({'error': {'code': 'CONFLICT', 'message': '已有待审批或已通过的申请，不能重复提交',
backend/apps/applications/views.py:89:                        status=status.HTTP_409_CONFLICT)
backend/apps/applications/views.py:93:        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
backend/apps/applications/views.py:101:        return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
backend/apps/applications/views.py:103:                                                'blocking_reason': dorm_status.blocking_reason}}},
backend/apps/applications/views.py:118:        reason=serializer.validated_data['reason'],
backend/apps/applications/views.py:119:        leave_date=serializer.validated_data['leave_date'],
backend/apps/applications/views.py:150:        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
backend/apps/applications/views.py:151:                        status=status.HTTP_403_FORBIDDEN)
backend/apps/applications/views.py:158:            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
backend/apps/applications/views.py:159:                            status=status.HTTP_403_FORBIDDEN)
backend/apps/applications/views.py:170:            return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
backend/apps/applications/views.py:171:                            status=status.HTTP_403_FORBIDDEN)
backend/apps/applications/serializers.py:12:                  'reason', 'leave_date', 'status', 'created_at', 'updated_at']
backend/apps/applications/serializers.py:24:                  'reason', 'leave_date', 'status', 'dorm_checkout_status',
backend/apps/applications/serializers.py:36:    reason = serializers.CharField()
backend/apps/applications/serializers.py:37:    leave_date = serializers.DateField()
backend/apps/applications/models.py:26:    reason = models.TextField()
backend/apps/applications/models.py:27:    leave_date = models.DateField()
miniprogram/services/api.ts:5:  ApplicationCreateRequest,
miniprogram/services/api.ts:75:  async createApplication(req: ApplicationCreateRequest): Promise<ApplicationDetail> {
docs/api/contract-v0.2.md:93:- Attempting operations on terminal states returns `409 CONFLICT`
docs/api/contract-v0.2.md:101:- Mismatch returns `409 CONFLICT`
docs/api/contract-v0.2.md:105:- Attempting repeat operations returns `409 CONFLICT`
docs/api/contract-v0.2.md:132:- Violation returns `403 FORBIDDEN`
docs/api/contract-v0.2.md:136:- Violation returns `403 FORBIDDEN`
docs/api/contract-v0.2.md:141:- Violation returns `403 FORBIDDEN`
docs/api/contract-v0.2.md:184:| `VALIDATION_ERROR` | 400 | Request validation failed | Missing/invalid fields |
docs/api/contract-v0.2.md:185:| `FORBIDDEN` | 403 | Permission denied | Role/approver mismatch |
docs/api/contract-v0.2.md:187:| `CONFLICT` | 409 | State conflict | Duplicate/invalid operation |
docs/api/contract-v0.2.md:188:| `DORM_BLOCKED` | 422 | Dorm checkout incomplete | Blocking condition |
docs/api/contract-v0.2.md:203:### 6.1 VALIDATION_ERROR (400)
docs/api/contract-v0.2.md:213:  "reason": ""
docs/api/contract-v0.2.md:221:    "code": "VALIDATION_ERROR",
docs/api/contract-v0.2.md:224:      "reason": ["This field may not be blank."],
docs/api/contract-v0.2.md:225:      "leave_date": ["This field is required."]
docs/api/contract-v0.2.md:231:### 6.2 FORBIDDEN (403)
docs/api/contract-v0.2.md:250:    "code": "FORBIDDEN",
docs/api/contract-v0.2.md:273:    "code": "FORBIDDEN",
docs/api/contract-v0.2.md:299:### 6.4 CONFLICT (409)
docs/api/contract-v0.2.md:310:  "reason": "毕业离校",
docs/api/contract-v0.2.md:311:  "leave_date": "2024-06-30"
docs/api/contract-v0.2.md:319:    "code": "CONFLICT",
docs/api/contract-v0.2.md:347:    "code": "CONFLICT",
docs/api/contract-v0.2.md:370:    "code": "CONFLICT",
docs/api/contract-v0.2.md:376:### 6.5 DORM_BLOCKED (422)
docs/api/contract-v0.2.md:387:  "reason": "毕业离校",
docs/api/contract-v0.2.md:388:  "leave_date": "2024-06-30"
docs/api/contract-v0.2.md:396:    "code": "DORM_BLOCKED",
docs/api/contract-v0.2.md:401:      "blocking_reason": "物品未清空"
docs/api/contract-v0.2.md:420:  "reason": "毕业离校",
docs/api/contract-v0.2.md:421:  "leave_date": "2024-06-30"
docs/api/contract-v0.2.md:432:  "reason": "毕业离校",
docs/api/contract-v0.2.md:433:  "leave_date": "2024-06-30",
docs/api/contract-v0.2.md:468:  "reason": "毕业离校",
docs/api/contract-v0.2.md:469:  "leave_date": "2024-06-30",
miniprogram/pages/detail/detail.wxml:23:        <text class="value">{{detail.leave_date}}</text>
miniprogram/pages/detail/detail.wxml:27:        <text class="value">{{detail.reason}}</text>
miniprogram/types/api.ts:37:export interface ApplicationCreateRequest {
miniprogram/types/api.ts:38:  reason: string;
miniprogram/types/api.ts:39:  leave_date: string; // YYYY-MM-DD
miniprogram/types/api.ts:47:  reason: string;
miniprogram/types/api.ts:48:  leave_date: string;
docs/contracts/contract-v0.2.md:42:  "reason": "毕业离校",
docs/contracts/contract-v0.2.md:43:  "leave_date": "2024-06-30",
docs/contracts/contract-v0.2.md:126:- 审批记录必须仍为 `pending`，否则返回 `409 CONFLICT`。
docs/contracts/contract-v0.2.md:174:{"reason":"毕业离校","leave_date":"2024-06-30"}
docs/contracts/contract-v0.2.md:220:    "code": "CONFLICT",
docs/contracts/contract-v0.2.md:234:| VALIDATION_ERROR | 400 | 申请提交字段缺失或格式错误 |
docs/contracts/contract-v0.2.md:235:| FORBIDDEN | 403 | 角色不符、非指定审批人、越权访问 |
docs/contracts/contract-v0.2.md:237:| CONFLICT | 409 | 重复提交、重复审批、状态与审批步骤不匹配 |
docs/contracts/contract-v0.2.md:238:| DORM_BLOCKED | 422 | 宿舍清退未完成 |
docs/contracts/contract-v0.1.md:39:    reason: str                      # 申请理由
docs/contracts/contract-v0.1.md:40:    leave_date: str                  # 计划离校日期 (YYYY-MM-DD)
docs/contracts/contract-v0.1.md:72:    blocking_reason: Optional[str]
docs/contracts/contract-v0.1.md:144:| pending | 阻断提交 | 422 | DORM_BLOCKED |
docs/contracts/contract-v0.1.md:145:| not_started | 阻断提交 | 422 | DORM_BLOCKED |
docs/contracts/contract-v0.1.md:146:| unknown | 阻断提交 | 422 | DORM_BLOCKED |
docs/contracts/contract-v0.1.md:166:| VALIDATION_ERROR | 400 | 请求参数校验失败 | 必填字段缺失、格式错误 |
docs/contracts/contract-v0.1.md:168:| FORBIDDEN | 403 | 无权限 | 学生访问他人申请 |
docs/contracts/contract-v0.1.md:170:| CONFLICT | 409 | 资源冲突 | 重复提交申请 |
docs/contracts/contract-v0.1.md:171:| DORM_BLOCKED | 422 | 宿舍清退未完成 | 提交申请时宿舍未清退 |
docs/contracts/contract-v0.1.md:185:    "code": "DORM_BLOCKED",
docs/contracts/contract-v0.1.md:234:  "reason": "毕业离校",
docs/contracts/contract-v0.1.md:235:  "leave_date": "2024-06-30"
docs/contracts/contract-v0.1.md:246:  "reason": "毕业离校",
docs/contracts/contract-v0.1.md:247:  "leave_date": "2024-06-30",
docs/contracts/contract-v0.1.md:264:  "reason": "毕业离校",
docs/contracts/contract-v0.1.md:265:  "leave_date": "2024-06-30",
docs/contracts/contract-v0.1.md:418:                blocking_reason=None,
docs/contracts/contract-v0.1.md:425:                blocking_reason="宿舍物品未清理",
docs/contracts/contract-v0.1.md:432:                blocking_reason="未提交清退申请",
docs/contracts/contract-v0.1.md:439:                blocking_reason="学生信息不存在",
docs/contracts/contract-v0.1.md:449:            blocking_reason="未在宿舍系统中找到记录",
docs/contracts/contract-v0.1.md:460:    "code": "VALIDATION_ERROR",
docs/contracts/contract-v0.1.md:463:      "field": "leave_date",
docs/contracts/contract-v0.1.md:464:      "reason": "离校日期不能早于今天"
docs/contracts/contract-v0.1.md:484:    "code": "FORBIDDEN",
docs/contracts/contract-v0.1.md:507:    "code": "CONFLICT",
docs/contracts/contract-v0.1.md:521:    "code": "DORM_BLOCKED",
docs/contracts/contract-v0.1.md:526:      "blocking_reason": "宿舍物品未清理"
docs/contracts/contract-v0.1.md:635:        json={'reason': '毕业离校', 'leave_date': '2024-06-30'}

exec
/bin/bash -lc 'rtk nl -ba backend/apps/applications/views.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import status
     2	from rest_framework.decorators import api_view, permission_classes
     3	from rest_framework.permissions import IsAuthenticated
     4	from rest_framework.response import Response
     5	from django.utils import timezone
     6	from .models import Application, ApplicationStatus, DormCheckoutStatus
     7	from .serializers import ApplicationSerializer, ApplicationCreateSerializer, ApplicationListSerializer
     8	from .pagination import ApplicationLimitOffsetPagination
     9	from .providers import MockDormCheckoutProvider
    10	from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
    11	from apps.users.models import UserRole
    12	from apps.users.class_mapping import ClassMapping
    13	import uuid
    14	
    15	
    16	@api_view(['GET', 'POST'])
    17	@permission_classes([IsAuthenticated])
    18	def applications_view(request):
    19	    if request.method == 'GET':
    20	        return list_applications(request)
    21	    else:
    22	        return create_application(request)
    23	
    24	
    25	def list_applications(request):
    26	    user = request.user
    27	
    28	    # Student: own applications only
    29	    if user.role == UserRole.STUDENT:
    30	        queryset = Application.objects.filter(student=user)
    31	
    32	    # Counselor: applications with own pending counselor approvals
    33	    elif user.role == UserRole.COUNSELOR:
    34	        pending_approvals = Approval.objects.filter(
    35	            approver=user,
    36	            step=ApprovalStep.COUNSELOR,
    37	            decision=ApprovalDecision.PENDING
    38	        ).values_list('application', flat=True)
    39	        queryset = Application.objects.filter(pk__in=pending_approvals)
    40	
    41	    # Dean: applications with own pending dean approvals
    42	    elif user.role == UserRole.DEAN:
    43	        pending_approvals = Approval.objects.filter(
    44	            approver=user,
    45	            step=ApprovalStep.DEAN,
    46	            decision=ApprovalDecision.PENDING
    47	        ).values_list('application', flat=True)
    48	        queryset = Application.objects.filter(pk__in=pending_approvals)
    49	
    50	    else:
    51	        return Response(
    52	            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
    53	            status=status.HTTP_403_FORBIDDEN
    54	        )
    55	
    56	    # Status filtering
    57	    status_param = request.query_params.get('status')
    58	    if status_param:
    59	        queryset = queryset.filter(status=status_param)
    60	
    61	    # Sort by created_at DESC
    62	    queryset = queryset.order_by('-created_at', '-application_id')
    63	
    64	    # Paginate
    65	    paginator = ApplicationLimitOffsetPagination()
    66	    page = paginator.paginate_queryset(queryset, request)
    67	
    68	    # Serialize
    69	    serializer = ApplicationListSerializer(page, many=True)
    70	
    71	    return paginator.get_paginated_response(serializer.data)
    72	
    73	
    74	def create_application(request):
    75	    user = request.user
    76	
    77	    if user.role != UserRole.STUDENT:
    78	        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以提交申请'}},
    79	                        status=status.HTTP_403_FORBIDDEN)
    80	
    81	    # Check for existing pending/approved applications
    82	    existing = Application.objects.filter(
    83	        student=user,
    84	        status__in=[ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.PENDING_DEAN, ApplicationStatus.APPROVED]
    85	    ).first()
    86	    if existing:
    87	        return Response({'error': {'code': 'CONFLICT', 'message': '已有待审批或已通过的申请，不能重复提交',
    88	                                    'details': {'student_id': user.user_id, 'existing_application_id': existing.application_id, 'status': existing.status}}},
    89	                        status=status.HTTP_409_CONFLICT)
    90	
    91	    serializer = ApplicationCreateSerializer(data=request.data)
    92	    if not serializer.is_valid():
    93	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
    94	                                    'details': serializer.errors}},
    95	                        status=status.HTTP_400_BAD_REQUEST)
    96	
    97	    provider = MockDormCheckoutProvider()
    98	    dorm_status = provider.check_status(user.user_id)
    99	
   100	    if dorm_status.status != DormCheckoutStatus.COMPLETED:
   101	        return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
   102	                                    'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
   103	                                                'blocking_reason': dorm_status.blocking_reason}}},
   104	                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
   105	
   106	    try:
   107	        class_mapping = ClassMapping.objects.get(class_id=user.class_id, active=True)
   108	    except ClassMapping.DoesNotExist:
   109	        return Response({'error': {'code': 'NOT_FOUND', 'message': '班级映射不存在',
   110	                                    'details': {'class_id': user.class_id}}},
   111	                        status=status.HTTP_404_NOT_FOUND)
   112	
   113	    application = Application.objects.create(
   114	        application_id=f'app_{uuid.uuid4().hex[:8]}',
   115	        student=user,
   116	        student_name=user.name,
   117	        class_id=user.class_id,
   118	        reason=serializer.validated_data['reason'],
   119	        leave_date=serializer.validated_data['leave_date'],
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

web search: 
web search: site:developers.weixin.qq.com miniprogram wx.redirectTo navigateTo reLaunch showToast showLoading API 官方 文档
web search: 
web search: 
web search: 
web search: wx.navigateTo 保留当前页面 跳转 微信小程序 文档
web search: 
web search: developers.weixin.qq.com miniprogram component textarea maxlength default 140
codex
微信官方文档页面在浏览工具里无法直接展开，我会用官方文档 URL 和可验证的 API 语义作为依据，同时以项目里的实际代码行作为本次审查的主要证据。
exec
/bin/bash -lc 'rtk curl -L --max-time 20 -s https://developers.weixin.qq.com/miniprogram/dev/component/textarea.html | head -80' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk curl -L --max-time 20 -s https://developers.weixin.qq.com/miniprogram/dev/component/picker.html | head -80' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk curl -L --max-time 20 -s https://developers.weixin.qq.com/miniprogram/dev/api/route/wx.navigateTo.html | head -60' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk curl -L --max-time 20 -s https://developers.weixin.qq.com/miniprogram/dev/api/ui/interaction/wx.showToast.html | head -80' in /home/caohui/projects/graduation-leave-system
 succeeded in 380ms:
<!DOCTYPE html>
<html lang="cn">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>picker | 微信开放文档</title>
    <meta name="description" content="微信开发者平台文档">
    <meta name="msapplication-TileColor" content="#ffffff">
  <meta name="theme-color" content="#ffffff">
  <meta name="keywords" content="微信官方文档">
  <link rel="shortcut icon" type="image/x-icon" href="https://res.wx.qq.com/a/wx_fed/assets/res/NTI4MWU5.ico">
  <link rel="mask-icon" color="#4C4C4C" href="https://res.wx.qq.com/a/wx_fed/assets/res/MjliNWVm.svg">
  <link rel="apple-touch-icon-precomposed" href="https://res.wx.qq.com/a/wx_fed/assets/res/OTE0YTAw.png">
  <script>
(function () {
  'use strict';

  const SCRIPT_URLs = [
      'https://dldir1.qq.com/WechatWebDev/devPlatform/px.min.js',
      'https://dev.weixin.qq.com/platform-console/proxy/assets/tel/px.min.js',
  ];
  const param = {
      maskMode: 'no-mask', // 隐私策略, all-mask 或 no-mask, 详见：https://dev.weixin.qq.com/docs/analysis/sdk/docs.html
      recordCanvas: false,  // 若要采集canvas, 设为true
      projectId: 'wxef34f91ddab0c534-0HLdQNKAk-dzsFsA', // 项目 ID，需替换为体验分析项目 ID
      iframe: false, // 是否采集 iframe 页面
      console: true, // 是否采集 console 输出的错误日志
      network: true, // 是否采集网络错误
  };
  function loadScript(url) {
      return new Promise((resolve, reject) => {
          const scriptEle = document.createElement('script');
          scriptEle.type = 'text/javascript';
          scriptEle.async = true;
          scriptEle.src = url;
          scriptEle.onload = () => {
              resolve(url);
          };
          scriptEle.onerror = () => {
              reject(new Error('Script load error'));
          };
          document.head.appendChild(scriptEle);
      });
  }
  async function main() {
      try {
          sessionStorage.setItem('wxobs_start_timestamp', String(Date.now()));
          const fastestUrl = await Promise.race(SCRIPT_URLs.map(url => loadScript(url)));
          window.__startPX && window.__startPX(param);
      }
      catch (error) {
          console.error('Error loading scripts:', error);
      }
  }
  main();

})();
        </script>
    
    <link rel="preload" href="https://res.wx.qq.com/wxdoc/dist/assets/css/0.styles.ec574a5b.css" as="style"><link rel="preload" href="https://res.wx.qq.com/wxdoc/dist/assets/js/app.556b7a0e.js" as="script"><link rel="preload" href="https://res.wx.qq.com/wxdoc/dist/assets/js/695.314d3e5f.js" as="script">
    <link rel="stylesheet" href="https://res.wx.qq.com/wxdoc/dist/assets/css/0.styles.ec574a5b.css">
  </head>
  <body>
    <div id="app" data-server-rendered="true"><div class="theme-container"><div class="theme-container"><header class="navbar navbar_with-link"><div class="navbar__left"><a href="/doc/" class="home-link"><div class="logo__wrp"><span class="logo__icon"></span></div></a> <span class="dot"></span> <div class="dropdown-wrapper"><a class="dropdown-title"><span class="title">小程序</span> <span class="arrow right"></span></a> <ul class="nav-dropdown" style="display:none;"><li class="dropdown-item selected"><!----> <a href="/miniprogram/dev/framework/" class="nav-link external">
  小程序
</a></li><li class="dropdown-item"><!----> <a href="/minigame/introduction/" class="nav-link external">
  小游戏
</a></li><li class="dropdown-item"><!----> <a href="/doc/subscription/guide/" class="nav-link external">
  公众号
</a></li><li class="dropdown-item"><!----> <a href="/doc/service/guide/" class="nav-link external">
  服务号
</a></li><li class="dropdown-item"><!----> <a href="/doc/oplatform/open/intro.html" class="nav-link external">
  开放平台
</a></li><li class="dropdown-item"><!----> <a href="https://work.weixin.qq.com/api/doc" class="nav-link external">
  企业微信
</a></li><li class="dropdown-item"><!----> <a href="https://pay.weixin.qq.com/doc/v3/merchant/4012062524" class="nav-link external">
  微信支付
</a></li><li class="dropdown-item"><!----> <a href="/doc/channels/" class="nav-link external">
  视频号
</a></li><li class="dropdown-item"><!----> <a href="/doc/store/shop/" class="nav-link external">

 succeeded in 679ms:
<!DOCTYPE html>
<html lang="cn">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>textarea | 微信开放文档</title>
    <meta name="description" content="微信开发者平台文档">
    <meta name="msapplication-TileColor" content="#ffffff">
  <meta name="theme-color" content="#ffffff">
  <meta name="keywords" content="微信官方文档">
  <link rel="shortcut icon" type="image/x-icon" href="https://res.wx.qq.com/a/wx_fed/assets/res/NTI4MWU5.ico">
  <link rel="mask-icon" color="#4C4C4C" href="https://res.wx.qq.com/a/wx_fed/assets/res/MjliNWVm.svg">
  <link rel="apple-touch-icon-precomposed" href="https://res.wx.qq.com/a/wx_fed/assets/res/OTE0YTAw.png">
  <script>
(function () {
  'use strict';

  const SCRIPT_URLs = [
      'https://dldir1.qq.com/WechatWebDev/devPlatform/px.min.js',
      'https://dev.weixin.qq.com/platform-console/proxy/assets/tel/px.min.js',
  ];
  const param = {
      maskMode: 'no-mask', // 隐私策略, all-mask 或 no-mask, 详见：https://dev.weixin.qq.com/docs/analysis/sdk/docs.html
      recordCanvas: false,  // 若要采集canvas, 设为true
      projectId: 'wxef34f91ddab0c534-0HLdQNKAk-dzsFsA', // 项目 ID，需替换为体验分析项目 ID
      iframe: false, // 是否采集 iframe 页面
      console: true, // 是否采集 console 输出的错误日志
      network: true, // 是否采集网络错误
  };
  function loadScript(url) {
      return new Promise((resolve, reject) => {
          const scriptEle = document.createElement('script');
          scriptEle.type = 'text/javascript';
          scriptEle.async = true;
          scriptEle.src = url;
          scriptEle.onload = () => {
              resolve(url);
          };
          scriptEle.onerror = () => {
              reject(new Error('Script load error'));
          };
          document.head.appendChild(scriptEle);
      });
  }
  async function main() {
      try {
          sessionStorage.setItem('wxobs_start_timestamp', String(Date.now()));
          const fastestUrl = await Promise.race(SCRIPT_URLs.map(url => loadScript(url)));
          window.__startPX && window.__startPX(param);
      }
      catch (error) {
          console.error('Error loading scripts:', error);
      }
  }
  main();

})();
        </script>
    
    <link rel="preload" href="https://res.wx.qq.com/wxdoc/dist/assets/css/0.styles.ec574a5b.css" as="style"><link rel="preload" href="https://res.wx.qq.com/wxdoc/dist/assets/js/app.556b7a0e.js" as="script"><link rel="preload" href="https://res.wx.qq.com/wxdoc/dist/assets/js/2266.4d3dd484.js" as="script">
    <link rel="stylesheet" href="https://res.wx.qq.com/wxdoc/dist/assets/css/0.styles.ec574a5b.css">
  </head>
  <body>
    <div id="app" data-server-rendered="true"><div class="theme-container"><div class="theme-container"><header class="navbar navbar_with-link"><div class="navbar__left"><a href="/doc/" class="home-link"><div class="logo__wrp"><span class="logo__icon"></span></div></a> <span class="dot"></span> <div class="dropdown-wrapper"><a class="dropdown-title"><span class="title">小程序</span> <span class="arrow right"></span></a> <ul class="nav-dropdown" style="display:none;"><li class="dropdown-item selected"><!----> <a href="/miniprogram/dev/framework/" class="nav-link external">
  小程序
</a></li><li class="dropdown-item"><!----> <a href="/minigame/introduction/" class="nav-link external">
  小游戏
</a></li><li class="dropdown-item"><!----> <a href="/doc/subscription/guide/" class="nav-link external">
  公众号
</a></li><li class="dropdown-item"><!----> <a href="/doc/service/guide/" class="nav-link external">
  服务号
</a></li><li class="dropdown-item"><!----> <a href="/doc/oplatform/open/intro.html" class="nav-link external">
  开放平台
</a></li><li class="dropdown-item"><!----> <a href="https://work.weixin.qq.com/api/doc" class="nav-link external">
  企业微信
</a></li><li class="dropdown-item"><!----> <a href="https://pay.weixin.qq.com/doc/v3/merchant/4012062524" class="nav-link external">
  微信支付
</a></li><li class="dropdown-item"><!----> <a href="/doc/channels/" class="nav-link external">
  视频号
</a></li><li class="dropdown-item"><!----> <a href="/doc/store/shop/" class="nav-link external">

 succeeded in 1624ms:
<!DOCTYPE html>
<html lang="cn">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>wx.navigateTo(Object object) | 微信开放文档</title>
    <meta name="description" content="微信开发者平台文档">
    <meta name="msapplication-TileColor" content="#ffffff">
  <meta name="theme-color" content="#ffffff">
  <meta name="keywords" content="微信官方文档">
  <link rel="shortcut icon" type="image/x-icon" href="https://res.wx.qq.com/a/wx_fed/assets/res/NTI4MWU5.ico">
  <link rel="mask-icon" color="#4C4C4C" href="https://res.wx.qq.com/a/wx_fed/assets/res/MjliNWVm.svg">
  <link rel="apple-touch-icon-precomposed" href="https://res.wx.qq.com/a/wx_fed/assets/res/OTE0YTAw.png">
  <script>
(function () {
  'use strict';

  const SCRIPT_URLs = [
      'https://dldir1.qq.com/WechatWebDev/devPlatform/px.min.js',
      'https://dev.weixin.qq.com/platform-console/proxy/assets/tel/px.min.js',
  ];
  const param = {
      maskMode: 'no-mask', // 隐私策略, all-mask 或 no-mask, 详见：https://dev.weixin.qq.com/docs/analysis/sdk/docs.html
      recordCanvas: false,  // 若要采集canvas, 设为true
      projectId: 'wxef34f91ddab0c534-0HLdQNKAk-dzsFsA', // 项目 ID，需替换为体验分析项目 ID
      iframe: false, // 是否采集 iframe 页面
      console: true, // 是否采集 console 输出的错误日志
      network: true, // 是否采集网络错误
  };
  function loadScript(url) {
      return new Promise((resolve, reject) => {
          const scriptEle = document.createElement('script');
          scriptEle.type = 'text/javascript';
          scriptEle.async = true;
          scriptEle.src = url;
          scriptEle.onload = () => {
              resolve(url);
          };
          scriptEle.onerror = () => {
              reject(new Error('Script load error'));
          };
          document.head.appendChild(scriptEle);
      });
  }
  async function main() {
      try {
          sessionStorage.setItem('wxobs_start_timestamp', String(Date.now()));
          const fastestUrl = await Promise.race(SCRIPT_URLs.map(url => loadScript(url)));
          window.__startPX && window.__startPX(param);
      }
      catch (error) {
          console.error('Error loading scripts:', error);
      }
  }
  main();

})();
        </script>
    
    <link rel="preload" href="https://res.wx.qq.com/wxdoc/dist/assets/css/0.styles.ec574a5b.css" as="style"><link rel="preload" href="https://res.wx.qq.com/wxdoc/dist/assets/js/app.556b7a0e.js" as="script"><link rel="preload" href="https://res.wx.qq.com/wxdoc/dist/assets/js/1788.819007d0.js" as="script">

thread 'main' (701614) panicked at /rustc/59807616e1fa2540724bfbac14d7976d7e4a3860/library/std/src/io/stdio.rs:1165:9:
failed printing to stdout: Broken pipe (os error 32)
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace

 succeeded in 2730ms:
<!DOCTYPE html>
<html lang="cn">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>wx.showToast(Object object) | 微信开放文档</title>
    <meta name="description" content="微信开发者平台文档">
    <meta name="msapplication-TileColor" content="#ffffff">
  <meta name="theme-color" content="#ffffff">
  <meta name="keywords" content="微信官方文档">
  <link rel="shortcut icon" type="image/x-icon" href="https://res.wx.qq.com/a/wx_fed/assets/res/NTI4MWU5.ico">
  <link rel="mask-icon" color="#4C4C4C" href="https://res.wx.qq.com/a/wx_fed/assets/res/MjliNWVm.svg">
  <link rel="apple-touch-icon-precomposed" href="https://res.wx.qq.com/a/wx_fed/assets/res/OTE0YTAw.png">
  <script>
(function () {
  'use strict';

  const SCRIPT_URLs = [
      'https://dldir1.qq.com/WechatWebDev/devPlatform/px.min.js',
      'https://dev.weixin.qq.com/platform-console/proxy/assets/tel/px.min.js',
  ];
  const param = {
      maskMode: 'no-mask', // 隐私策略, all-mask 或 no-mask, 详见：https://dev.weixin.qq.com/docs/analysis/sdk/docs.html
      recordCanvas: false,  // 若要采集canvas, 设为true
      projectId: 'wxef34f91ddab0c534-0HLdQNKAk-dzsFsA', // 项目 ID，需替换为体验分析项目 ID
      iframe: false, // 是否采集 iframe 页面
      console: true, // 是否采集 console 输出的错误日志
      network: true, // 是否采集网络错误
  };
  function loadScript(url) {
      return new Promise((resolve, reject) => {
          const scriptEle = document.createElement('script');
          scriptEle.type = 'text/javascript';
          scriptEle.async = true;
          scriptEle.src = url;
          scriptEle.onload = () => {
              resolve(url);
          };
          scriptEle.onerror = () => {
              reject(new Error('Script load error'));
          };
          document.head.appendChild(scriptEle);
      });
  }
  async function main() {
      try {
          sessionStorage.setItem('wxobs_start_timestamp', String(Date.now()));
          const fastestUrl = await Promise.race(SCRIPT_URLs.map(url => loadScript(url)));
          window.__startPX && window.__startPX(param);
      }
      catch (error) {
          console.error('Error loading scripts:', error);
      }
  }
  main();

})();
        </script>
    
    <link rel="preload" href="https://res.wx.qq.com/wxdoc/dist/assets/css/0.styles.ec574a5b.css" as="style"><link rel="preload" href="https://res.wx.qq.com/wxdoc/dist/assets/js/app.556b7a0e.js" as="script"><link rel="preload" href="https://res.wx.qq.com/wxdoc/dist/assets/js/1888.5d55ce2a.js" as="script">
    <link rel="stylesheet" href="https://res.wx.qq.com/wxdoc/dist/assets/css/0.styles.ec574a5b.css">
  </head>
  <body>
    <div id="app" data-server-rendered="true"><div class="theme-container"><div class="theme-container"><header class="navbar navbar_with-link"><div class="navbar__left"><a href="/doc/" class="home-link"><div class="logo__wrp"><span class="logo__icon"></span></div></a> <span class="dot"></span> <div class="dropdown-wrapper"><a class="dropdown-title"><span class="title">小程序</span> <span class="arrow right"></span></a> <ul class="nav-dropdown" style="display:none;"><li class="dropdown-item selected"><!----> <a href="/miniprogram/dev/framework/" class="nav-link external">
  小程序
</a></li><li class="dropdown-item"><!----> <a href="/minigame/introduction/" class="nav-link external">
  小游戏
</a></li><li class="dropdown-item"><!----> <a href="/doc/subscription/guide/" class="nav-link external">
  公众号
</a></li><li class="dropdown-item"><!----> <a href="/doc/service/guide/" class="nav-link external">
  服务号
</a></li><li class="dropdown-item"><!----> <a href="/doc/oplatform/open/intro.html" class="nav-link external">
  开放平台
</a></li><li class="dropdown-item"><!----> <a href="https://work.weixin.qq.com/api/doc" class="nav-link external">
  企业微信
</a></li><li class="dropdown-item"><!----> <a href="https://pay.weixin.qq.com/doc/v3/merchant/4012062524" class="nav-link external">
  微信支付
</a></li><li class="dropdown-item"><!----> <a href="/doc/channels/" class="nav-link external">
  视频号
</a></li><li class="dropdown-item"><!----> <a href="/doc/store/shop/" class="nav-link external">

thread 'main' (701619) panicked at /rustc/59807616e1fa2540724bfbac14d7976d7e4a3860/library/std/src/io/stdio.rs:1165:9:
failed printing to stdout: Broken pipe (os error 32)
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace

exec
/bin/bash -lc "rtk bash -lc \"curl -L --max-time 20 -s https://developers.weixin.qq.com/miniprogram/dev/api/route/wx.redirectTo.html | rg -n '关闭当前页面|跳转到|tabBar|页面栈' | head -30\"" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk bash -lc \"curl -L --max-time 20 -s https://developers.weixin.qq.com/miniprogram/dev/api/route/wx.navigateTo.html | rg -n '保留当前页面|页面栈|十层|跳转到|tabBar|关闭' | head -30\"" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk bash -lc \"curl -L --max-time 20 -s https://developers.weixin.qq.com/miniprogram/dev/component/textarea.html | rg -n 'maxlength|最大输入长度|默认|字数|长度' | head -40\"" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk bash -lc \"curl -L --max-time 20 -s https://developers.weixin.qq.com/miniprogram/dev/api/ui/interaction/wx.showToast.html | rg -n 'duration|mask|默认|提示' | head -40\"" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk bash -lc \"curl -L --max-time 20 -s https://developers.weixin.qq.com/miniprogram/dev/component/picker.html | rg -n 'start|end|mode|date|日期|有效值' | head -60\"" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk bash -lc \"curl -L --max-time 20 -s https://developers.weixin.qq.com/miniprogram/dev/api/route/wx.reLaunch.html | rg -n '关闭所有页面|打开到|路径' | head -30\"" in /home/caohui/projects/graduation-leave-system
 succeeded in 671ms:
530:    <!----></a> <!----> <!----></span></li></ul></div></li></ul></div></li></ul></div></div> </aside></div> <div class="page__wrp"><main class="page"><div class="page-inner" style="min-height:0px;"> <div id="docContent"><div class="Breadcrumb"></div> <div class="content custom"><h1 id="textarea"><a href="#textarea" class="header-anchor">#</a> textarea</h1> <blockquote><p>基础库 1.0.0 开始支持，低版本需做<a href="../framework/compatibility.html">兼容处理</a>。</p></blockquote> <blockquote><p><strong>微信 Windows 版</strong>：支持</p> <p><strong>微信 Mac 版</strong>：支持</p> <p><strong>微信 鸿蒙 OS 版</strong>：支持</p></blockquote> <p class="wedoc-support-tips">渲染框架支持情况：Skyline （使用最新 <a href="/miniprogram/dev/devtools/nightly.html">Nightly</a> 工具调试）、WebView</p> <h2 id="功能描述"><a href="#功能描述" class="header-anchor">#</a> 功能描述</h2> <p>多行输入框。该组件是<a href="native-component.html">原生组件</a>，使用时请注意相关限制。</p> <h2 id="通用属性"><a href="#通用属性" class="header-anchor">#</a> 通用属性</h2> <div class="table-wrp"><table class="have-children-table"><thead><tr><th></th> <th>属性</th> <th>类型</th> <th>默认值</th> <th>必填</th> <th>说明</th> <th>最低版本</th></tr></thead> <tbody><tr><td><i class="toggle-children-table"></i></td> <td>value</td> <td>string</td> <td></td> <td>否</td> <td>输入框的内容</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>placeholder</td> <td>string</td> <td></td> <td>否</td> <td>输入框为空时占位符</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>placeholder-style</td> <td>string</td> <td></td> <td>否</td> <td>指定 placeholder 的样式，目前仅支持color,font-size,font-weight,line-height</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>disabled</td> <td>boolean</td> <td>false</td> <td>否</td> <td>是否禁用</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>maxlength</td> <td>number</td> <td>140</td> <td>否</td> <td>最大输入长度，设置为 -1 的时候不限制最大长度</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>auto-focus</td> <td>boolean</td> <td>false</td> <td>否</td> <td>自动聚焦，拉起键盘。</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>focus</td> <td>boolean</td> <td>false</td> <td>否</td> <td>获取焦点</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>auto-height</td> <td>boolean</td> <td>false</td> <td>否</td> <td>是否自动增高，设置auto-height时，style.height不生效</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>cursor-spacing</td> <td>number</td> <td>0</td> <td>否</td> <td>指定光标与键盘的距离。取<code>textarea</code>距离底部的距离和<code>cursor-spacing</code>指定的距离的最小值作为光标与键盘的距离</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>cursor</td> <td>number</td> <td>-1</td> <td>否</td> <td>指定focus时的光标位置</td> <td><a href="../framework/compatibility.html">1.5.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>selection-start</td> <td>number</td> <td>-1</td> <td>否</td> <td>光标起始位置，自动聚集时有效，需与<code>selection-end</code>搭配使用</td> <td><a href="../framework/compatibility.html">1.9.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>selection-end</td> <td>number</td> <td>-1</td> <td>否</td> <td>光标结束位置，自动聚集时有效，需与<code>selection-start</code>搭配使用</td> <td><a href="../framework/compatibility.html">1.9.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>adjust-position</td> <td>boolean</td> <td>true</td> <td>否</td> <td>键盘弹起时，是否自动上推页面</td> <td><a href="../framework/compatibility.html">1.9.90</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>hold-keyboard</td> <td>boolean</td> <td>false</td> <td>否</td> <td>focus时，点击页面的时候不收起键盘</td> <td><a href="../framework/compatibility.html">2.8.2</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>disable-default-padding</td> <td>boolean</td> <td>false</td> <td>否</td> <td>是否去掉 iOS 下的默认内边距</td> <td><a href="../framework/compatibility.html">2.10.0</a></td></tr> <tr class="have-children-tr show-children"><td><i class="toggle-children-table"></i></td> <td>confirm-type</td> <td>string</td> <td>return</td> <td>否</td> <td>设置键盘右下角按钮的文字</td> <td><a href="../framework/compatibility.html">2.13.0</a></td></tr> <tr class="children-table"><td><i class="toggle-children-table"></i></td> <td colspan="6"><table><thead><tr><th style="width: 20%;">合法值</th> <th>说明</th></tr></thead> <tbody><tr><td>send</td> <td>右下角按钮为“发送”</td></tr> <tr><td>search</td> <td>右下角按钮为“搜索”</td></tr> <tr><td>next</td> <td>右下角按钮为“下一个”</td></tr> <tr><td>go</td> <td>右下角按钮为“前往”</td></tr> <tr><td>done</td> <td>右下角按钮为“完成”</td></tr> <tr><td>return</td> <td>右下角按钮为“换行”</td></tr></tbody></table></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>confirm-hold</td> <td>boolean</td> <td>false</td> <td>否</td> <td>点击键盘右下角按钮时是否保持键盘不收起</td> <td><a href="../framework/compatibility.html">2.16.0</a></td></tr> <tr class="have-children-tr show-children"><td><i class="toggle-children-table"></i></td> <td>adjust-keyboard-to</td> <td>boolean</td> <td>cursor</td> <td>否</td> <td>键盘对齐位置。</td> <td><a href="../framework/compatibility.html">2.16.1</a></td></tr> <tr class="children-table"><td><i class="toggle-children-table"></i></td> <td colspan="6"><table><thead><tr><th style="width: 20%;">合法值</th> <th>说明</th></tr></thead> <tbody><tr><td>cursor</td> <td>对齐光标位置</td></tr> <tr><td>bottom</td> <td>对齐输入框底部</td></tr></tbody></table></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>bindfocus</td> <td>eventhandle</td> <td></td> <td>否</td> <td>输入框聚焦时触发，event.detail = { value, height }，height 为键盘高度，在基础库 1.9.90 起支持</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>bindblur</td> <td>eventhandle</td> <td></td> <td>否</td> <td>输入框失去焦点时触发，event.detail = {value, cursor}</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>bindlinechange</td> <td>eventhandle</td> <td></td> <td>否</td> <td>输入框行数变化时调用，event.detail = {height: 0, heightRpx: 0, lineCount: 0}</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>bindinput</td> <td>eventhandle</td> <td></td> <td>否</td> <td>当键盘输入时，触发 input 事件，event.detail = {value, cursor, keyCode}，keyCode 为键值，目前工具还不支持返回keyCode参数。**bindinput 处理函数的返回值并不会反映到 textarea 上**</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>bindconfirm</td> <td>eventhandle</td> <td></td> <td>否</td> <td>点击完成时， 触发 confirm 事件，event.detail = {value: value}</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>bindkeyboardheightchange</td> <td>eventhandle</td> <td></td> <td>否</td> <td>键盘高度发生变化的时候触发此事件，event.detail = {height: height, duration: duration}</td> <td><a href="../framework/compatibility.html">2.7.0</a></td></tr></tbody></table></div> <h2 id="Skyline-特有属性"><a href="#Skyline-特有属性" class="header-anchor">#</a> Skyline 特有属性</h2> <div class="table-wrp"><table class="have-children-table"><thead><tr><th></th> <th>属性</th> <th>类型</th> <th>默认值</th> <th>必填</th> <th>说明</th> <th>最低版本</th></tr></thead> <tbody><tr><td><i class="toggle-children-table"></i></td> <td>placeholder-style</td> <td>string</td> <td></td> <td>否</td> <td>需传入对象，格式为 <code>{ fontSize: number, fontWeight: string, color: string }</code></td> <td></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>bind:selectionchange</td> <td>eventhandle</td> <td></td> <td>否</td> <td>选区改变事件, {selectionStart, selectionEnd}</td> <td><a href="../framework/compatibility.html">3.2.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>bind:keyboardcompositionstart</td> <td>eventhandle</td> <td></td> <td>否</td> <td>输入法开始新的输入时触发 （仅当输入法支持时触发）</td> <td><a href="../framework/compatibility.html">3.2.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>bind:keyboardcompositionupdate</td> <td>eventhandle</td> <td></td> <td>否</td> <td>输入法输入字符时触发（仅当输入法支持时触发）</td> <td><a href="../framework/compatibility.html">3.2.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>bind:keyboardcompositionend</td> <td>eventhandle</td> <td></td> <td>否</td> <td>输入法输入结束时触发（仅当输入法支持时触发）</td> <td><a href="../framework/compatibility.html">3.2.0</a></td></tr></tbody></table></div> <h2 id="WebView-特有属性"><a href="#WebView-特有属性" class="header-anchor">#</a> WebView 特有属性</h2> <div class="table-wrp"><table class="have-children-table"><thead><tr><th></th> <th>属性</th> <th>类型</th> <th>默认值</th> <th>必填</th> <th>说明</th> <th>最低版本</th></tr></thead> <tbody><tr><td><i class="toggle-children-table"></i></td> <td>placeholder-class</td> <td>string</td> <td>textarea-placeholder</td> <td>否</td> <td>指定 placeholder 的样式类，目前仅支持color,font-size和font-weight</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>fixed</td> <td>boolean</td> <td>false</td> <td>否</td> <td>如果 textarea 是在一个 <code>position:fixed</code> 的区域，需要显示指定属性 fixed 为 true</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>show-confirm-bar</td> <td>boolean</td> <td>true</td> <td>否</td> <td>是否显示键盘上方带有”完成“按钮那一栏</td> <td><a href="../framework/compatibility.html">1.6.0</a></td></tr></tbody></table></div> <h2 id="Bug-Tip"><a href="#Bug-Tip" class="header-anchor">#</a> Bug &amp; Tip</h2> <ol><li><code>tip</code>: <code>textarea</code> 的 <code>blur</code> 事件会晚于页面上的 <code>tap</code> 事件，如果需要在 <code>button</code> 的点击事件获取 <code>textarea</code>，可以使用 <code>form</code> 的 <code>bindsubmit</code>。</li> <li><code>tip</code>: 不建议在多行文本上对用户的输入进行修改，所以 <code>textarea</code> 的 <code>bindinput</code> 处理函数并不会将返回值反映到 <code>textarea</code> 上。</li> <li><code>tip</code> : 键盘高度发生变化，keyboardheightchange事件可能会多次触发，开发者对于相同的height值应该忽略掉</li> <li><code>bug</code>: 微信版本 <code>6.3.30</code>，<code>textarea</code> 在列表渲染时，新增加的 <code>textarea</code> 在自动聚焦时的位置计算错误。</li></ol> <h2 id="示例代码"><a href="#示例代码" class="header-anchor">#</a> 示例代码</h2> <p><a href="https://developers.weixin.qq.com/s/QAwRn6m86tYu" title="在开发者工具中预览效果" target="_blank" rel="noopener noreferrer">在开发者工具中预览效果<span></span></a></p> <div class="language-html extra-class"><pre class="language-html"><code><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>view</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>section<span class="token punctuation">&quot;</span></span><span class="token punctuation">&gt;</span></span>

 succeeded in 706ms:
3498:    <!----></a> <!----> <!----></span></li></ul></div></li></ul></div></li></ul></div></div> </aside></div> <div class="page__wrp"><main class="page"><div class="page-inner" style="min-height:0px;"> <div id="docContent"><div class="Breadcrumb"></div> <div class="content custom"><h1 id="wx-navigateTo-Object-object"><a href="#wx-navigateTo-Object-object" class="header-anchor">#</a> wx.navigateTo(Object object)</h1> <blockquote><p><strong>以 <a href="../../framework/app-service/api.html#%E5%BC%82%E6%AD%A5-API-%E8%BF%94%E5%9B%9E-Promise">Promise 风格</a> 调用</strong>：支持</p> <p><strong>需要页面权限</strong>：当前是插件页面时，宿主小程序不能调用该接口，反之亦然</p> <p><strong>小程序插件</strong>：支持，需要小程序基础库版本不低于 <a href="../../framework/compatibility.html">2.2.2</a></p> <p>在小程序插件中使用时，只能在当前插件的页面中调用</p> <p><strong>微信 Windows 版</strong>：支持</p> <p><strong>微信 Mac 版</strong>：支持</p> <p><strong>微信 鸿蒙 OS 版</strong>：支持</p></blockquote> <h2 id="功能描述"><a href="#功能描述" class="header-anchor">#</a> 功能描述</h2> <p>保留当前页面，跳转到应用内的某个页面。但是不能跳到 tabbar 页面。使用 <a href="wx.navigateBack.html">wx.navigateBack</a> 可以返回到原页面。小程序中页面栈最多十层。</p> <h2 id="参数"><a href="#参数" class="header-anchor">#</a> 参数</h2> <h3 id="Object-object"><a href="#Object-object" class="header-anchor">#</a> Object object</h3> <div class="table-wrp"><table><thead><tr><th>属性</th> <th>类型</th> <th>默认值</th> <th>必填</th> <th>说明</th></tr></thead> <tbody><tr><td>url</td> <td>string</td> <td></td> <td>是</td> <td>需要跳转的应用内非 tabBar 的页面的路径 (代码包路径), 路径后可以带参数。参数与路径之间使用 <code>?</code> 分隔，参数键与参数值用 <code>=</code> 相连，不同参数用 <code>&amp;</code> 分隔；如 'path?key=value&amp;key2=value2'</td></tr> <tr><td>events</td> <td>Object</td> <td></td> <td>否</td> <td>页面间通信接口，用于监听被打开页面发送到当前页面的数据。基础库 2.7.3 开始支持。</td></tr> <tr><td>routeType</td> <td>string</td> <td></td> <td>否</td> <td>2.29.2 自定义路由类型，相关文档 <a href="../../framework/runtime/skyline/custom-route.html">自定义路由</a></td></tr> <tr><td>routeConfig</td> <td>Object</td> <td></td> <td>否</td> <td>3.4.0 自定义路由配置，相关文档 <a href="../../framework/runtime/skyline/custom-route.html">自定义路由</a></td></tr> <tr><td>routeOptions</td> <td>Object</td> <td></td> <td>否</td> <td>3.4.0 自定义路由参数，相关文档 <a href="../../framework/runtime/skyline/custom-route.html">自定义路由</a></td></tr> <tr><td>withOpenContainer</td> <td>Object</td> <td></td> <td>否</td> <td>3.12.2 skyline 下指定路由动画所用OpenContainerContext，相关文档 <a href="../../framework/custom-component/glass-easel/skyline.html">OpenContainerContext</a></td></tr> <tr><td>success</td> <td>function</td> <td></td> <td>否</td> <td>接口调用成功的回调函数</td></tr> <tr><td>fail</td> <td>function</td> <td></td> <td>否</td> <td>接口调用失败的回调函数</td></tr> <tr><td>complete</td> <td>function</td> <td></td> <td>否</td> <td>接口调用结束的回调函数（调用成功、失败都会执行）</td></tr></tbody></table></div><h4 id="object-success-回调函数"><a href="#object-success-回调函数" class="header-anchor">#</a> object.success 回调函数</h4> <h5 id="参数-2"><a href="#参数-2" class="header-anchor">#</a> 参数</h5> <h6 id="Object-res"><a href="#Object-res" class="header-anchor">#</a> Object res</h6> <div class="table-wrp"><table><thead><tr><th>属性</th> <th>类型</th> <th>说明</th></tr></thead> <tbody><tr><td>eventChannel</td> <td><a href="EventChannel.html">EventChannel</a></td> <td>和被打开页面进行通信</td></tr></tbody></table></div><h2 id="示例代码"><a href="#示例代码" class="header-anchor">#</a> 示例代码</h2> <div class="language-js extra-class"><pre class="language-js"><code>wx<span class="token punctuation">.</span><span class="token function">navigateTo</span><span class="token punctuation">(</span><span class="token punctuation">{</span>

 succeeded in 771ms:
3498:    <!----></a> <!----> <!----></span></li></ul></div></li></ul></div></li></ul></div></div> </aside></div> <div class="page__wrp"><main class="page"><div class="page-inner" style="min-height:0px;"> <div id="docContent"><div class="Breadcrumb"></div> <div class="content custom"><h1 id="wx-redirectTo-Object-object"><a href="#wx-redirectTo-Object-object" class="header-anchor">#</a> wx.redirectTo(Object object)</h1> <blockquote><p><strong>以 <a href="../../framework/app-service/api.html#%E5%BC%82%E6%AD%A5-API-%E8%BF%94%E5%9B%9E-Promise">Promise 风格</a> 调用</strong>：支持</p> <p><strong>需要页面权限</strong>：当前是插件页面时，宿主小程序不能调用该接口，反之亦然</p> <p><strong>小程序插件</strong>：支持，需要小程序基础库版本不低于 <a href="../../framework/compatibility.html">2.2.2</a></p> <p>在小程序插件中使用时，只能在当前插件的页面中调用</p> <p><strong>微信 Windows 版</strong>：支持</p> <p><strong>微信 Mac 版</strong>：支持</p> <p><strong>微信 鸿蒙 OS 版</strong>：支持</p></blockquote> <h2 id="功能描述"><a href="#功能描述" class="header-anchor">#</a> 功能描述</h2> <p>关闭当前页面，跳转到应用内的某个页面。但是不允许跳转到 tabbar 页面。</p> <h2 id="参数"><a href="#参数" class="header-anchor">#</a> 参数</h2> <h3 id="Object-object"><a href="#Object-object" class="header-anchor">#</a> Object object</h3> <div class="table-wrp"><table><thead><tr><th>属性</th> <th>类型</th> <th>默认值</th> <th>必填</th> <th>说明</th></tr></thead> <tbody><tr><td>url</td> <td>string</td> <td></td> <td>是</td> <td>需要跳转的应用内非 tabBar 的页面的路径 (代码包路径), 路径后可以带参数。参数与路径之间使用 <code>?</code> 分隔，参数键与参数值用 <code>=</code> 相连，不同参数用 <code>&amp;</code> 分隔；如 'path?key=value&amp;key2=value2'</td></tr> <tr><td>success</td> <td>function</td> <td></td> <td>否</td> <td>接口调用成功的回调函数</td></tr> <tr><td>fail</td> <td>function</td> <td></td> <td>否</td> <td>接口调用失败的回调函数</td></tr> <tr><td>complete</td> <td>function</td> <td></td> <td>否</td> <td>接口调用结束的回调函数（调用成功、失败都会执行）</td></tr></tbody></table></div><h2 id="示例代码"><a href="#示例代码" class="header-anchor">#</a> 示例代码</h2> <div class="language-js extra-class"><pre class="language-js"><code>wx<span class="token punctuation">.</span><span class="token function">redirectTo</span><span class="token punctuation">(</span><span class="token punctuation">{</span>

 succeeded in 734ms:
42:          document.head.appendChild(scriptEle);
47:          sessionStorage.setItem('wxobs_start_timestamp', String(Date.now()));
49:          window.__startPX && window.__startPX(param);
64:    <div id="app" data-server-rendered="true"><div class="theme-container"><div class="theme-container"><header class="navbar navbar_with-link"><div class="navbar__left"><a href="/doc/" class="home-link"><div class="logo__wrp"><span class="logo__icon"></span></div></a> <span class="dot"></span> <div class="dropdown-wrapper"><a class="dropdown-title"><span class="title">小程序</span> <span class="arrow right"></span></a> <ul class="nav-dropdown" style="display:none;"><li class="dropdown-item selected"><!----> <a href="/miniprogram/dev/framework/" class="nav-link external">
126:          </a></li><li class="dropdown-item" style="display:;"><a href="/miniprogram/dev/platform-capabilities/extended/" target="_self" class="nav-link external">
130:          </a> <!----></div> <!----></li><li class="subnavbar__item dropdown-subnavbar" style="display:;"><div class="dropdown-subnavbar-title"><a>云服务</a> <span class="arrow right dropdown-subnavbar-select"></span></div> <ul class="dropdown-subnavbar-ul"><li class="dropdown-item" style="display:;"><a href="/miniprogram/dev/wxcloudservice/wxcloud/basis/getting-started" target="_self" class="nav-link external">
384:    <!----></a> <!----> <!----></span></li></ul></div></li><li><div class="NavigationLevel NavigationLevel--closed NavigationLevel--level-2"><div class="NavigationLevel__parent"><span class="NavigationToggle NavigationToggle--closed"><span class="NavigationToggle__icon NavigationToggle__icon--closed"></span></span> <span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/" class="NavigationItem__router-link">
386:    <!----></a> <!----> <!----></span></div> <ul class="NavigationLevel__children"><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/" class="NavigationItem__router-link">
387:      渲染系统(RenderSystem)
388:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/#画布透明配置" class="NavigationItem__router-link">
390:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/geometry.html" class="NavigationItem__router-link">
392:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/effect.html" class="NavigationItem__router-link">
394:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/material.html" class="NavigationItem__router-link">
396:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/mesh.html" class="NavigationItem__router-link">
398:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/texture.html" class="NavigationItem__router-link">
400:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/texture.html#立方体纹理" class="NavigationItem__router-link">
402:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/texture.html#视频纹理" class="NavigationItem__router-link">
404:    <span class="wedoc-beta-tag" style="margin-left:0;">Beta</span></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/texture.html#使用纹理" class="NavigationItem__router-link">
406:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/camera.html" class="NavigationItem__router-link">
408:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/render-texture.html" class="NavigationItem__router-link">
409:      渲染到纹理(RenderTexture)
410:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/atlas.html" class="NavigationItem__router-link">
412:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/env.html" class="NavigationItem__router-link">
414:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/env.html#天空盒" class="NavigationItem__router-link">
416:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/light.html" class="NavigationItem__router-link">
418:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/light.html#阴影" class="NavigationItem__router-link">
420:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/component/xr-frame/render/post-process.html" class="NavigationItem__router-link">
530:    <!----></a> <!----> <!----></span></li></ul></div></li></ul></div></li></ul></div></div> </aside></div> <div class="page__wrp"><main class="page"><div class="page-inner" style="min-height:0px;"> <div id="docContent"><div class="Breadcrumb"></div> <div class="content custom"><h1 id="picker"><a href="#picker" class="header-anchor">#</a> picker</h1> <blockquote><p>基础库 1.0.0 开始支持，低版本需做<a href="../framework/compatibility.html">兼容处理</a>。</p></blockquote> <blockquote><p><strong>微信 Windows 版</strong>：支持</p> <p><strong>微信 Mac 版</strong>：支持</p> <p><strong>微信 鸿蒙 OS 版</strong>：支持</p></blockquote> <p class="wedoc-support-tips">渲染框架支持情况：Skyline （使用最新 <a href="/miniprogram/dev/devtools/nightly.html">Nightly</a> 工具调试）、WebView</p> <h2 id="功能描述"><a href="#功能描述" class="header-anchor">#</a> 功能描述</h2> <p>从底部弹起的滚动选择器。</p> <h2 id="通用属性"><a href="#通用属性" class="header-anchor">#</a> 通用属性</h2> <div class="table-wrp"><table class="have-children-table"><thead><tr><th></th> <th>属性</th> <th>类型</th> <th>默认值</th> <th>必填</th> <th>说明</th> <th>最低版本</th></tr></thead> <tbody><tr><td><i class="toggle-children-table"></i></td> <td>header-text</td> <td>string</td> <td></td> <td>否</td> <td>选择器的标题，仅安卓可用</td> <td><a href="../framework/compatibility.html">2.11.0</a></td></tr> <tr class="have-children-tr show-children"><td><i class="toggle-children-table"></i></td> <td>mode</td> <td>string</td> <td>selector</td> <td>否</td> <td>选择器类型</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr class="children-table"><td><i class="toggle-children-table"></i></td> <td colspan="6"><table><thead><tr><th style="width: 20%;">合法值</th> <th>说明</th></tr></thead> <tbody><tr><td>selector</td> <td>普通选择器</td></tr> <tr><td>multiSelector</td> <td>多列选择器</td></tr> <tr><td>time</td> <td>时间选择器</td></tr> <tr><td>date</td> <td>日期选择器</td></tr> <tr><td>region</td> <td>省市区选择器</td></tr></tbody></table></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>disabled</td> <td>boolean</td> <td>false</td> <td>否</td> <td>是否禁用</td> <td><a href="../framework/compatibility.html">1.0.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>bindcancel</td> <td>eventhandle</td> <td></td> <td>否</td> <td>取消选择时触发</td> <td><a href="../framework/compatibility.html">1.9.90</a></td></tr></tbody></table></div> <p>除了上述通用的属性，对于不同的mode，<code>picker</code>拥有不同的属性。</p> <h2 id="普通选择器：mode-selector"><a href="#普通选择器：mode-selector" class="header-anchor">#</a> 普通选择器：mode = selector</h2> <div class="table-wrp"><table><thead><tr><th>属性名</th> <th>类型</th> <th>默认值</th> <th>说明</th> <th>最低版本</th></tr></thead> <tbody><tr><td>range</td> <td>array/object array</td> <td>[]</td> <td>mode 为 selector 或 multiSelector 时，range 有效</td> <td></td></tr> <tr><td>range-key</td> <td>string</td> <td></td> <td>当 range 是一个 Object Array 时，通过 range-key 来指定 Object 中 key 的值作为选择器显示内容</td> <td></td></tr> <tr><td>value</td> <td>number</td> <td>0</td> <td>表示选择了 range 中的第几个（下标从 0 开始）</td> <td></td></tr> <tr><td>bindchange</td> <td>eventhandle</td> <td></td> <td>value 改变时触发 change 事件，event.detail = {value}</td> <td></td></tr></tbody></table></div><h2 id="多列选择器：mode-multiSelector"><a href="#多列选择器：mode-multiSelector" class="header-anchor">#</a> 多列选择器：mode = multiSelector</h2> <div class="table-wrp"><table><thead><tr><th>属性名</th> <th>类型</th> <th>默认值</th> <th>说明</th> <th>最低版本</th></tr></thead> <tbody><tr><td>range</td> <td>array/object array</td> <td>[]</td> <td>mode 为 selector 或 multiSelector 时，range 有效</td> <td></td></tr> <tr><td>range-key</td> <td>string</td> <td></td> <td>当 range 是一个 Object Array 时，通过 range-key 来指定 Object 中 key 的值作为选择器显示内容</td> <td></td></tr> <tr><td>value</td> <td>array</td> <td>[]</td> <td>表示选择了 range 中的第几个（下标从 0 开始）</td> <td></td></tr> <tr><td>bindchange</td> <td>eventhandle</td> <td></td> <td>value 改变时触发 change 事件，event.detail = {value}</td> <td></td></tr> <tr><td>bindcolumnchange</td> <td>eventhandle</td> <td></td> <td>列改变时触发</td> <td></td></tr></tbody></table></div><h2 id="时间选择器：mode-time"><a href="#时间选择器：mode-time" class="header-anchor">#</a> 时间选择器：mode = time</h2> <div class="table-wrp"><table><thead><tr><th>属性名</th> <th>类型</th> <th>默认值</th> <th>说明</th> <th>最低版本</th></tr></thead> <tbody><tr><td>value</td> <td>string</td> <td></td> <td>表示选中的时间，格式为&quot;hh:mm&quot;</td> <td></td></tr> <tr><td>start</td> <td>string</td> <td></td> <td>表示有效时间范围的开始，字符串格式为&quot;hh:mm&quot;</td> <td></td></tr> <tr><td>end</td> <td>string</td> <td></td> <td>表示有效时间范围的结束，字符串格式为&quot;hh:mm&quot;</td> <td></td></tr> <tr><td>bindchange</td> <td>eventhandle</td> <td></td> <td>value 改变时触发 change 事件，event.detail = {value}</td> <td></td></tr></tbody></table></div><h2 id="日期选择器：mode-date"><a href="#日期选择器：mode-date" class="header-anchor">#</a> 日期选择器：mode = date</h2> <div class="table-wrp"><table><thead><tr><th>属性名</th> <th>类型</th> <th>默认值</th> <th>说明</th> <th>最低版本</th></tr></thead> <tbody><tr><td>value</td> <td>string</td> <td>当天</td> <td>表示选中的日期，格式为&quot;YYYY-MM-DD&quot;</td> <td></td></tr> <tr><td>start</td> <td>string</td> <td></td> <td>表示有效日期范围的开始，字符串格式为&quot;YYYY-MM-DD&quot;</td> <td></td></tr> <tr><td>end</td> <td>string</td> <td></td> <td>表示有效日期范围的结束，字符串格式为&quot;YYYY-MM-DD&quot;</td> <td></td></tr> <tr><td>fields</td> <td>string</td> <td>day</td> <td>有效值 year,month,day，表示选择器的粒度</td> <td></td></tr> <tr><td>bindchange</td> <td>eventhandle</td> <td></td> <td>value 改变时触发 change 事件，event.detail = {value}</td> <td></td></tr></tbody></table></div><p><strong>fields 有效值：</strong></p> <div class="table-wrp"><table><thead><tr><th>值</th> <th>说明</th></tr></thead> <tbody><tr><td>year</td> <td>选择器粒度为年</td></tr> <tr><td>month</td> <td>选择器粒度为月份</td></tr> <tr><td>day</td> <td>选择器粒度为天</td></tr></tbody></table></div><h2 id="省市区选择器：mode-region-1-4-0"><a href="#省市区选择器：mode-region-1-4-0" class="header-anchor">#</a> 省市区选择器：mode = region <a href="../framework/compatibility.html">1.4.0</a></h2> <div class="table-wrp"><table><thead><tr><th>属性名</th> <th>类型</th> <th>默认值</th> <th>说明</th> <th>最低版本</th></tr></thead> <tbody><tr><td>value</td> <td>array</td> <td>[]</td> <td>表示选中的省市区，默认选中每一列的第一个值</td> <td></td></tr> <tr><td>custom-item</td> <td>string</td> <td></td> <td>可为每一列的顶部添加一个自定义的项</td> <td><a href="../framework/compatibility.html">1.5.0</a></td></tr> <tr><td>level</td> <td>string</td> <td>region</td> <td>选择器层级</td> <td><a href="../framework/compatibility.html">2.21.1</a></td></tr> <tr><td>bindchange</td> <td>eventhandle</td> <td></td> <td>value 改变时触发 change 事件，event.detail = {value, code, postcode}，其中字段 code 是统计用区划代码，postcode 是邮政编码</td> <td></td></tr></tbody></table></div><p>level 的有效值</p> <div class="table-wrp"><table><thead><tr><th>值</th> <th>说明</th></tr></thead> <tbody><tr><td>province</td> <td>省级选择器</td></tr> <tr><td>city</td> <td>市级选择器</td></tr> <tr><td>region</td> <td>区级选择器</td></tr> <tr><td>sub-district</td> <td>街道选择器</td></tr></tbody></table></div><h2 id="示例代码"><a href="#示例代码" class="header-anchor">#</a> 示例代码</h2> <p><a href="https://developers.weixin.qq.com/s/D22Y9SmR7fJK" title="在开发者工具中预览效果" target="_blank" rel="noopener noreferrer">在开发者工具中预览效果<span></span></a></p> <div class="language-html extra-class"><pre class="language-html"><code><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>view</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>section<span class="token punctuation">&quot;</span></span><span class="token punctuation">&gt;</span></span>
540:  <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>picker</span> <span class="token attr-name">mode</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>multiSelector<span class="token punctuation">&quot;</span></span> <span class="token attr-name">bindchange</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>bindMultiPickerChange<span class="token punctuation">&quot;</span></span> <span class="token attr-name">bindcolumnchange</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>bindMultiPickerColumnChange<span class="token punctuation">&quot;</span></span> <span class="token attr-name">value</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>{{multiIndex}}<span class="token punctuation">&quot;</span></span> <span class="token attr-name">range</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>{{multiArray}}<span class="token punctuation">&quot;</span></span><span class="token punctuation">&gt;</span></span>
548:  <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>picker</span> <span class="token attr-name">mode</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>time<span class="token punctuation">&quot;</span></span> <span class="token attr-name">value</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>{{time}}<span class="token punctuation">&quot;</span></span> <span class="token attr-name">start</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>09:01<span class="token punctuation">&quot;</span></span> <span class="token attr-name">end</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>21:01<span class="token punctuation">&quot;</span></span> <span class="token attr-name">bindchange</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>bindTimeChange<span class="token punctuation">&quot;</span></span><span class="token punctuation">&gt;</span></span>
556:  <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>view</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>section__title<span class="token punctuation">&quot;</span></span><span class="token punctuation">&gt;</span></span>日期选择器<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>view</span><span class="token punctuation">&gt;</span></span>
557:  <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>picker</span> <span class="token attr-name">mode</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>date<span class="token punctuation">&quot;</span></span> <span class="token attr-name">value</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>{{date}}<span class="token punctuation">&quot;</span></span> <span class="token attr-name">start</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>2015-09-01<span class="token punctuation">&quot;</span></span> <span class="token attr-name">end</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>2017-09-01<span class="token punctuation">&quot;</span></span> <span class="token attr-name">bindchange</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>bindDateChange<span class="token punctuation">&quot;</span></span><span class="token punctuation">&gt;</span></span>
559:      当前选择: {{date}}
565:  <span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>picker</span> <span class="token attr-name">mode</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>region<span class="token punctuation">&quot;</span></span> <span class="token attr-name">bindchange</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>bindRegionChange<span class="token punctuation">&quot;</span></span> <span class="token attr-name">value</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>{{region}}<span class="token punctuation">&quot;</span></span> <span class="token attr-name">custom-item</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">&quot;</span>{{customItem}}<span class="token punctuation">&quot;</span></span><span class="token punctuation">&gt;</span></span>
637:    <span class="token literal-property property">date</span><span class="token operator">:</span> <span class="token string">'2016-09-01'</span><span class="token punctuation">,</span>
720:      <span class="token literal-property property">date</span><span class="token operator">:</span> e<span class="token punctuation">.</span>detail<span class="token punctuation">.</span>value

 succeeded in 805ms:
12:  <link rel="mask-icon" color="#4C4C4C" href="https://res.wx.qq.com/a/wx_fed/assets/res/MjliNWVm.svg">
23:      maskMode: 'no-mask', // 隐私策略, all-mask 或 no-mask, 详见：https://dev.weixin.qq.com/docs/analysis/sdk/docs.html
148:</a></div></nav></div> <div class="links-panel__ft"><ul class="lang-tab"><li class="lang-tab__icon"><img src="https://res.wx.qq.com/t/components/icons/base/translate_regular.svg"></li></ul></div></div> <div><div class="weui-mask" style="display:none;"></div> <div class="weui-actionsheet "><!----> <div class="weui-actionsheet__menu"><div class="weui-actionsheet__cell">中文</div><div class="weui-actionsheet__cell">EN</div></div> <div class="weui-actionsheet__action"><div class="weui-actionsheet__cell">取消</div></div></div></div></div> <a href="javascript:;" class="mobile-search-btn"></a> <div class="main-container" style="margin-top:144px;"><div class="main-contontaier__bd" style="min-height:0px;"><div class="sidebar__wrp"><div class="sidebar-cell_mobile"><li class="subnavbar__item selected"><a href="javascript:;" target="_self">API</a></li></div> <aside class="sidebar" style="top:144px;"> <div class="TreeNavigation"><div class="NavigationLevel NavigationLevel--level-0"><ul><li><div class="NavigationLevel NavigationLevel--closed NavigationLevel--level-1"><div class="NavigationLevel__parent"><span class="NavigationToggle NavigationToggle--closed"><span class="NavigationToggle__icon NavigationToggle__icon--closed"></span></span> <span class="NavigationItem"><!----> <a href="/miniprogram/dev/api/base/wx.env.html" class="NavigationItem__router-link">
3498:    <!----></a> <!----> <!----></span></li></ul></div></li></ul></div></li></ul></div></div> </aside></div> <div class="page__wrp"><main class="page"><div class="page-inner" style="min-height:0px;"> <div id="docContent"><div class="Breadcrumb"></div> <div class="content custom"><h1 id="wx-showToast-Object-object"><a href="#wx-showToast-Object-object" class="header-anchor">#</a> wx.showToast(Object object)</h1> <blockquote><p><strong>以 <a href="../../../framework/app-service/api.html#异步-API-返回-Promise">Promise 风格</a> 调用</strong>：支持</p> <p><strong>小程序插件</strong>：支持，需要小程序基础库版本不低于 <a href="../../../framework/compatibility.html">1.9.6</a></p> <p><strong>微信 Windows 版</strong>：支持</p> <p><strong>微信 Mac 版</strong>：支持</p> <p><strong>微信 鸿蒙 OS 版</strong>：支持</p></blockquote> <h2 id="功能描述"><a href="#功能描述" class="header-anchor">#</a> 功能描述</h2> <p>显示消息提示框</p> <h2 id="参数"><a href="#参数" class="header-anchor">#</a> 参数</h2> <h3 id="Object-object"><a href="#Object-object" class="header-anchor">#</a> Object object</h3> <div class="table-wrp"><table class="have-children-table"><thead><tr><th></th> <th>属性</th> <th>类型</th> <th>默认值</th> <th>必填</th> <th>说明</th> <th>最低版本</th></tr></thead> <tbody><tr><td><i class="toggle-children-table"></i></td> <td>title</td> <td>string</td> <td></td> <td>是</td> <td>提示的内容</td> <td></td></tr> <tr class="have-children-tr show-children"><td><i class="toggle-children-table"></i></td> <td>icon</td> <td>string</td> <td>success</td> <td>否</td> <td>图标</td> <td></td></tr> <tr class="children-table"><td><i class="toggle-children-table"></i></td> <td colspan="6"><table><thead><tr><th style="width: 20%;">合法值</th> <th>说明</th> <th style="width: 20%;">最低版本</th></tr></thead> <tbody><tr><td>success</td> <td>显示成功图标，此时 title 文本最多显示 7 个汉字长度</td> <td></td></tr> <tr><td>error</td> <td>显示失败图标，此时 title 文本最多显示 7 个汉字长度</td> <td><a href="../../../framework/compatibility.html">2.14.1</a></td></tr> <tr><td>loading</td> <td>显示加载图标，此时 title 文本最多显示 7 个汉字长度</td> <td></td></tr> <tr><td>none</td> <td>不显示图标，此时 title 文本最多可显示两行，<a href="../../../framework/compatibility.html">1.9.0</a>及以上版本支持</td> <td></td></tr></tbody></table></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>image</td> <td>string</td> <td></td> <td>否</td> <td>自定义图标的本地路径，image 的优先级高于 icon</td> <td><a href="../../../framework/compatibility.html">1.1.0</a></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>duration</td> <td>number</td> <td>1500</td> <td>否</td> <td>提示的延迟时间</td> <td></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>mask</td> <td>boolean</td> <td>false</td> <td>否</td> <td>是否显示透明蒙层，防止触摸穿透</td> <td></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>success</td> <td>function</td> <td></td> <td>否</td> <td>接口调用成功的回调函数</td> <td></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>fail</td> <td>function</td> <td></td> <td>否</td> <td>接口调用失败的回调函数</td> <td></td></tr> <tr><td><i class="toggle-children-table"></i></td> <td>complete</td> <td>function</td> <td></td> <td>否</td> <td>接口调用结束的回调函数（调用成功、失败都会执行）</td> <td></td></tr></tbody></table></div> <h2 id="示例代码"><a href="#示例代码" class="header-anchor">#</a> 示例代码</h2> <div class="language-js extra-class"><pre class="language-js"><code>wx<span class="token punctuation">.</span><span class="token function">showToast</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
3501:  <span class="token literal-property property">duration</span><span class="token operator">:</span> <span class="token number">2000</span>

 succeeded in 995ms:
3498:    <!----></a> <!----> <!----></span></li></ul></div></li></ul></div></li></ul></div></div> </aside></div> <div class="page__wrp"><main class="page"><div class="page-inner" style="min-height:0px;"> <div id="docContent"><div class="Breadcrumb"></div> <div class="content custom"><h1 id="wx-reLaunch-Object-object"><a href="#wx-reLaunch-Object-object" class="header-anchor">#</a> wx.reLaunch(Object object)</h1> <blockquote><p>基础库 1.1.0 开始支持，低版本需做<a href="../../framework/compatibility.html">兼容处理</a>。</p></blockquote> <blockquote><p><strong>以 <a href="../../framework/app-service/api.html#%E5%BC%82%E6%AD%A5-API-%E8%BF%94%E5%9B%9E-Promise">Promise 风格</a> 调用</strong>：支持</p> <p><strong>需要页面权限</strong>：当前是插件页面时，宿主小程序不能调用该接口，反之亦然</p> <p><strong>小程序插件</strong>：支持，需要小程序基础库版本不低于 <a href="../../framework/compatibility.html">2.3.1</a></p> <p>在小程序插件中使用时，只能在当前插件的页面中调用</p> <p><strong>微信 Windows 版</strong>：支持</p> <p><strong>微信 Mac 版</strong>：支持</p> <p><strong>微信 鸿蒙 OS 版</strong>：支持</p></blockquote> <h2 id="功能描述"><a href="#功能描述" class="header-anchor">#</a> 功能描述</h2> <p>关闭所有页面，打开到应用内的某个页面</p> <h2 id="参数"><a href="#参数" class="header-anchor">#</a> 参数</h2> <h3 id="Object-object"><a href="#Object-object" class="header-anchor">#</a> Object object</h3> <div class="table-wrp"><table><thead><tr><th>属性</th> <th>类型</th> <th>默认值</th> <th>必填</th> <th>说明</th></tr></thead> <tbody><tr><td>url</td> <td>string</td> <td></td> <td>是</td> <td>需要跳转的应用内页面路径 (代码包路径)，路径后可以带参数。参数与路径之间使用?分隔，参数键与参数值用=相连，不同参数用&amp;分隔；如 'path?key=value&amp;key2=value2'</td></tr> <tr><td>success</td> <td>function</td> <td></td> <td>否</td> <td>接口调用成功的回调函数</td></tr> <tr><td>fail</td> <td>function</td> <td></td> <td>否</td> <td>接口调用失败的回调函数</td></tr> <tr><td>complete</td> <td>function</td> <td></td> <td>否</td> <td>接口调用结束的回调函数（调用成功、失败都会执行）</td></tr></tbody></table></div><h2 id="示例代码"><a href="#示例代码" class="header-anchor">#</a> 示例代码</h2> <div class="language-js extra-class"><pre class="language-js"><code>wx<span class="token punctuation">.</span><span class="token function">reLaunch</span><span class="token punctuation">(</span><span class="token punctuation">{</span>

exec
/bin/bash -lc "rtk bash -lc \"curl -L --max-time 20 -s https://developers.weixin.qq.com/miniprogram/dev/reference/configuration/app.html | rg -n 'pages|第一项|页面路径|初始页面|首页|新增/减少页面' | head -60\"" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk bash -lc \"curl -L --max-time 20 -s https://developers.weixin.qq.com/miniprogram/dev/framework/app-service/route.html | rg -n '页面栈|路由|navigateTo|redirectTo|reLaunch|生命周期|onLoad|onUnload' | head -80\"" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk bash -lc \"curl -L --max-time 20 -s https://developers.weixin.qq.com/miniprogram/dev/api/ui/interaction/wx.showLoading.html | rg -n 'mask|防止触摸穿透|loading|hideLoading|显示 loading' | head -60\"" in /home/caohui/projects/graduation-leave-system
 succeeded in 646ms:
6:    <title>页面路由 | 微信开放文档</title>
221:      页面生命周期
223:      页面路由
227:      页面路由监听
229:      路由事件重写
303:      自定义路由
305:      预设路由效果
373:      组件生命周期
974:    <!----></a> <!----> <!----></span></li></ul></div></li></ul></div></div> </aside></div> <div class="page__wrp"><main class="page"><div class="page-inner" style="min-height:0px;"> <div id="docContent"><div class="Breadcrumb"></div> <div class="content custom"><h1 id="页面路由"><a href="#页面路由" class="header-anchor">#</a> 页面路由</h1> <p>在小程序中，所有页面的创建、销毁及状态转换都由页面路由来表达和进行控制。以下内容会简单介绍小程序的页面路由相关逻辑。</p> <h2 id="路由的时机"><a href="#路由的时机" class="header-anchor">#</a> 路由的时机</h2> <p>路由会以事件形式表示，由微信客户端下发给小程序基础库，下发后客户端和基础库将分别同时处理这一次路由事件。路由事件的发起可以大致分为以下两类：</p> <ol><li><p>通过用户的操作（如按下返回按钮）发起。通过这种方式发起时，路由事件将直接由客户端下发到基础库执行；</p></li> <li><p>由开发者通过 API（如 <code>wx.navigateTo</code>）或者组件（如 <code>&lt;navigator&gt;</code>）发起。通过这种方式发起时，基础库将首先向客户端发起路由请求，客户端确认路由可以被执行后，再将路由事件下发到基础库。其中，如果路由被确定执行，API 的 <code>success</code> 回调函数或组件的 <code>success</code> 事件将被触发，否则将触发 <code>fail</code>。</p></li></ol> <p>当一次路由被确定执行（API 或组件通知 <code>success</code>）时，没有操作可以取消这一次路由。</p> <p>当多次路由被连续发起时，如果当前的路由事件还未处理完毕，后续的路由事件将等待当前路由处理，并排队依次执行，直到所有待处理的路由都被执行完毕。</p> <blockquote><p>一个简单的例子：用户点击返回按钮触发了 <code>navigateBack</code>，小程序在页面栈当前栈顶页的 <code>onUnload</code> 中调用 <code>wx.redirectTo</code>，<strong>并不能</strong> 将当前正在被销毁的页面重定向为一个新页面，而是会先完成页面返回，再将页面返回后的新栈顶页重定向到新的页面。</p></blockquote> <h2 id="页面栈"><a href="#页面栈" class="header-anchor">#</a> 页面栈</h2> <p>目前，小程序的页面会被组织为一个页面栈加若干不在栈中的悬垂页面的组合形式。其中，页面栈按顺序存放了通过跳转依次打开的页面，而当前已经创建但非活跃的 tabBar 页面及处于画中画模式（如 <a href="../../component/video.html#%E5%B0%8F%E7%AA%97%E7%89%B9%E6%80%A7%E8%AF%B4%E6%98%8E"><code>video</code></a>、<a href="../../component/live-player.html#%E5%B0%8F%E7%AA%97%E7%89%B9%E6%80%A7%E8%AF%B4%E6%98%8E"><code>live-player</code></a> 等）中的页面将以悬垂页面的形式存在。</p> <p>全局接口 <a href="../../reference/api/getCurrentPages.html"><code>getCurrentPages</code></a> 可以用来获取当前页面栈。</p> <p>小程序冷启动完成后，在整个小程序存活过程中（除去某次路由执行到一半的中间状态外），页面栈中都将存在至少一个页面。</p> <p>页面栈的具体行为可以参见下面具体路由行为中的详细描述。</p> <h2 id="路由的监听及响应"><a href="#路由的监听及响应" class="header-anchor">#</a> 路由的监听及响应</h2> <h3 id="页面生命周期函数"><a href="#页面生命周期函数" class="header-anchor">#</a> 页面生命周期函数</h3> <p>每个小程序页面都有若干生命周期函数，如 <code>onLoad</code>, <code>onShow</code>, <code>onRouteDone</code>, <code>onHide</code>, <code>onUnload</code> 等。它们可以在页面注册时定义，并会在相应的时机触发。所有生命周期函数及它们各自的含义和触发时机可以参见 <a href="../../reference/api/Page.html#%E7%94%9F%E5%91%BD%E5%91%A8%E6%9C%9F%E5%9B%9E%E8%B0%83%E5%87%BD%E6%95%B0">Page 接口</a>，下面的内容也将详细说明每个路由将如何触发页面的生命周期函数。</p> <h3 id="页面路由监听"><a href="#页面路由监听" class="header-anchor">#</a> 页面路由监听</h3> <p>从基础库版本 <a href="../compatibility.html">3.5.5</a> 开始，基础库提供了一组针对路由事件的监听函数。相比页面生命周期函数，它们能更好地针对某次路由进行响应。详见 <a href="./route-event-listener">页面路由监听</a>。</p> <h2 id="路由类型"><a href="#路由类型" class="header-anchor">#</a> 路由类型</h2> <p>小程序目前的路由类型可以大致分为以下七种：</p> <h3 id="_1-小程序启动"><a href="#_1-小程序启动" class="header-anchor">#</a> 1. 小程序启动</h3> <ul><li>openType: <code>appLaunch</code></li></ul> <p>小程序启动路由 <code>appLaunch</code> 表示一个新的小程序启动，并加载第一个页面。<code>appLaunch</code> 在每个小程序实例中会且仅会出现一次，且每个小程序实例启动时的第一个路由事件必定为 <code>appLaunch</code>。</p> <p><strong>触发方式</strong></p> <p><code>appLaunch</code> 仅能由小程序冷启动被动触发，不能由开发者主动触发，启动后也不能通过其他用户操作触发。</p> <p><strong>页面栈及生命周期处理</strong></p> <p>由于 <code>appLaunch</code> 必定是启动时的第一个路由，而路由前没有任何页面存在，此时页面栈必定为空。<code>appLaunch</code> 会创建路由事件指定的页面，并将其推入页面栈作为栈中唯一的页面。在这个过程中，这个页面的 <code>onLoad</code>, <code>onShow</code> 两个生命周期将依次被触发。</p> <h3 id="_2-打开新页面"><a href="#_2-打开新页面" class="header-anchor">#</a> 2. 打开新页面</h3> <ul><li>openType: <code>navigateTo</code></li></ul> <p>打开新页面路由 <code>navigateTo</code> 表示打开一个新的页面，并将其推入页面栈。</p> <p><strong>触发方式</strong></p> <ol><li>调用 API <a href="../../api/route/wx.navigateTo.html"><code>wx.navigateTo</code></a>, <a href="../../reference/api/Router.html"><code>Router.navigateTo</code></a></li> <li>使用组件 <a href="../../component/navigator.html"><code>&lt;navigator open-type=&quot;navigateTo&quot;/&gt;</code></a></li> <li>用户点击一个视频小窗（如 <a href="../../component/video.html#%E5%B0%8F%E7%AA%97%E7%89%B9%E6%80%A7%E8%AF%B4%E6%98%8E"><code>video</code></a>）</li></ol> <p><code>navigateTo</code> 的目标必须为非 tabBar 页面。</p> <p><strong>页面栈及生命周期处理</strong></p> <p><code>navigateTo</code> 事件发生时，页面栈当前的栈顶页面将首先被隐藏，触发 <code>onHide</code> 生命周期；之后框架将创建路由事件指定的页面，并将其推入页面栈作为新的栈顶。在这个过程中，这个新页面的 <code>onLoad</code>, <code>onShow</code> 两个生命周期将依次被触发。</p> <p>作为一种特殊情况，如果 <code>navigateTo</code> 事件发生时，页面栈当前的栈顶页面满足小窗模式逻辑，或事件由用户点击视频小窗发起，那么页面栈及生命周期的的处理会有所不同。</p> <h3 id="_3-页面重定向"><a href="#_3-页面重定向" class="header-anchor">#</a> 3. 页面重定向</h3> <ul><li>openType: <code>redirectTo</code></li></ul> <p>页面重定向路由 <code>redirectTo</code> 表示将页面栈当前的栈顶页面替换为一个新的页面。</p> <p><strong>触发方式</strong></p> <ol><li>调用 API <a href="../../api/route/wx.redirectTo.html"><code>wx.redirectTo</code></a>, <a href="../../reference/api/Router.html"><code>Router.redirectTo</code></a></li> <li>使用组件 <a href="../../component/navigator.html"><code>&lt;navigator open-type=&quot;redirectTo&quot;/&gt;</code></a></li></ol> <p><code>redirectTo</code> 的目标必须为非 tabBar 页面。</p> <p><strong>页面栈及生命周期处理</strong></p> <p><code>redirectTo</code> 事件发生时，页面栈当前的栈顶页面将首先被弹出并销毁，在此过程中，这个栈顶页面的 <code>onUnload</code> 生命周期将被触发；之后框架将创建路由事件指定的页面，并将其推入页面栈作为新的栈顶。在这个过程中，这个新页面的 <code>onLoad</code>, <code>onShow</code> 两个生命周期将依次被触发。</p> <h3 id="_4-页面返回"><a href="#_4-页面返回" class="header-anchor">#</a> 4. 页面返回</h3> <ul><li>openType: <code>navigateBack</code></li></ul> <p>页面返回路由 <code>navigateBack</code> 表示将页面栈当前的栈顶的若干个页面依次弹出并销毁。</p> <p><strong>触发方式</strong></p> <ol><li>调用 API <a href="../../api/route/wx.navigateBack.html"><code>wx.navigateBack</code></a>, <a href="../../reference/api/Router.html"><code>Router.navigateBack</code></a></li> <li>使用组件 <a href="../../component/navigator.html"><code>&lt;navigator open-type=&quot;navigateBack&quot;/&gt;</code></a></li> <li>用户按左上角返回按钮，或触发操作系统返回的动作（如按下系统返回键、屏幕边缘向内滑动等）</li> <li>用户点击一个视频小窗（如 <a href="../../component/video.html#%E5%B0%8F%E7%AA%97%E7%89%B9%E6%80%A7%E8%AF%B4%E6%98%8E"><code>video</code></a>）</li></ol> <p>如果页面栈中当前只有一个页面，<code>navigateBack</code> 调用请求将失败（无论指定的 <code>delta</code> 是多少）；</p> <p>如果页面栈中当前的页面数量少于调用时指定的 <code>delta</code> + 1（即调用后页面数量将少于一个），<code>navigateBack</code> 将弹出到只剩页面栈当前的页面栈底的页面为止（即至少保留一个页面）。</p> <p><strong>页面栈及生命周期处理</strong></p> <p><code>navigateBack</code> 事件发生时，页面栈当前的栈顶页面将被弹出并销毁，并触发这个页面的 <code>onUnload</code> 生命周期；以上操作将被重复执行多次，直到弹出的页面数量等于指定的页面数量，或当前页面栈中只剩下一个页面。之后，页面栈新的栈顶页面的 <code>onShow</code> 生命周期将被触发。</p> <p>一种特殊情况是，如果 <code>navigateBack</code> 发生时，页面栈当前的栈顶页面满足小窗模式逻辑，或事件由用户点击视频小窗发起，那么页面栈及生命周期的的处理会有所不同。</p> <h3 id="_5-Tab-切换"><a href="#_5-Tab-切换" class="header-anchor">#</a> 5. Tab 切换</h3> <ul><li>openType: <code>switchTab</code></li></ul> <p>Tab 切换路由 <code>switchTab</code> 表示切换到指定的 tab 页面。</p> <p><strong>触发方式</strong></p> <ol><li>调用 API <a href="../../api/route/wx.switchTab.html"><code>wx.switchTab</code></a>, <a href="../../reference/api/Router.html"><code>Router.switchTab</code></a></li> <li>使用组件 <a href="../../component/navigator.html"><code>&lt;navigator open-type=&quot;switchTab&quot;/&gt;</code></a></li> <li>用户点击 Tab Bar 中的 Tab 按钮</li></ol> <p><code>switchTab</code> 的目标必须为 tabBar 页面。</p> <p><strong>页面栈及生命周期处理</strong></p> <p>由于 <code>navigateTo</code> 和 <code>redirectTo</code> 不能指定 tabBar 页面作为目标，因此当一个 tabBar 页面出现在页面栈中时，它必定为页面栈的第一个页面（即栈底页面）；同时，框架会保证任一 tabBar 页面在小程序中最多同时存在一个页面实例。<code>switchTab</code> 的行为主要基于这两点进行。</p> <p><code>switchTab</code> 事件发生时，如果当前页面栈中存在多于一个页面，页面栈当前的栈顶页面将被弹出并销毁，并触发这个页面的 <code>onUnload</code> 生命周期；以上操作将被重复执行多次，直到页面栈中只剩下一个页面。之后，根据页面栈中仅剩的页面进行不同的处理：</p> <ul><li style="list-style: disc">
976:    <ul><li style="list-style: circle">如果路由事件开始时页面栈中存在多于一个页面（即目标 tabBar 页面不是栈顶页面），触发目标 tabBar 页面的 <code>onShow</code> 生命周期；</li> <li style="list-style: circle">否则（路由事件开始时目标 tabBar 页面是栈顶页面），不触发任何生命周期，直接结束；</li></ul></li> <li style="list-style: disc">
978:    <ol><li style="list-style: decimal">将这个页面从页面栈中弹出；</li> <li style="list-style: decimal"><ul><li style="list-style: disc">
980:            <ul><li style="list-style: circle">如果路由事件开始时页面栈中只有一个页面（即该 tabBar 页面是栈顶页面），触发它的 <code>onHide</code> 生命周期；</li> <li style="list-style: circle">否则（路由事件开始时该 tabBar 页面不是栈顶页面），不触发它的任何生命周期；</li></ul></li> <li style="list-style: disc">否则（这个页面为非 tabBar 页面时），销毁该页面，触发 <code>onUnload</code> 生命周期；</li></ul></li> <li style="list-style: decimal"><ul><li style="list-style: disc">如果目标 tabBar 页之前已经被创建过（现在是一个悬垂页面），将其推入页面栈，触发 <code>onShow</code> 生命周期；</li> <li style="list-style: disc">否则（目标 tabBar 页不存在实例），创建目标 tabBar 页并推入页面栈，依次触发 <code>onLoad</code>, <code>onShow</code> 生命周期。</li></ul></li></ol></li></ul> <h3 id="_6-重加载"><a href="#_6-重加载" class="header-anchor">#</a> 6. 重加载</h3> <ul><li>openType: <code>reLaunch</code>, <code>autoReLaunch</code></li></ul> <p>重加载路由 <code>reLaunch</code> 或 <code>autoReLaunch</code> 表示销毁当前所有的页面，并载入一个新页面。</p> <p>重加载路由的两种 openType 的区别主要为是否由开发者主动触发（或是由用户触发），这两种 openType 的路由逻辑基本一致。</p> <p><strong>触发方式</strong></p> <ol><li>（<code>reLaunch</code>）调用 API <a href="../../api/route/wx.reLaunch.html"><code>wx.reLaunch</code></a>, <a href="../../reference/api/Router.html"><code>Router.reLaunch</code></a></li> <li>（<code>reLaunch</code>）使用组件 <a href="../../component/navigator.html"><code>&lt;navigator open-type=&quot;reLaunch&quot;/&gt;</code></a></li> <li>（<code>autoReLaunch</code>）小程序处于后台时，用户从扫码或分享等场景重新进入小程序</li></ol> <p><code>reLaunch</code> 可以指定任意页面作为目标页面，无论它是否是小程序的首页或是否 tabBar 页。</p> <p>请注意：<code>reLaunch</code> 及 <code>autoReLaunch</code> 仅代表一种路由，<strong>并不等于小程序重启，小程序会在当前的 AppService 上继续运行</strong>，既不会重新启动 AppService 的 JavaScript 运行环境，也不会重新注入小程序代码或触发 <code>App.onLaunch</code> 生命周期，各种 JS 的全局变量或全局状态也不会被重置。</p> <p><strong>页面栈及生命周期处理</strong></p> <p><code>reLaunch</code> 或 <code>autoReLaunch</code> 事件发生时，页面栈中的所有页面将由顶至底依次被弹出并销毁，触发 <code>onUnload</code> 生命周期；之后所有悬垂页面将以不确定的顺序逐个被销毁，触发 <code>onUnload</code> 生命周期。所有页面都被销毁后，目标页面将被创建，并推入页面栈成为栈中唯一的页面，依次触发 <code>onLoad</code> 和 <code>onShow</code> 两个生命周期。</p> <h3 id="_7-关闭小窗页面"><a href="#_7-关闭小窗页面" class="header-anchor">#</a> 7. 关闭小窗页面</h3> <ul><li>openType: <code>dismissPip</code></li></ul> <p>关闭小窗页面路由 <code>dismissPip</code> 表示关闭一个正处于小窗模式的页面。</p> <h2 id="附注"><a href="#附注" class="header-anchor">#</a> 附注</h2> <p><code>switchTab</code> 事件的处理逻辑较为复杂，下面的表格用以展示在各种情况下进行 <code>switchTab</code> 时生命周期的触发情况，作为辅助说明。在这个表格中，我们假设：</p> <ul><li><code>tabA</code>, <code>tabB</code> 为 tabBar 页面</li> <li><code>C</code> 是一个非 tabBar 页面，并且我们只会从 <code>tabA</code> 页面打开它</li> <li><code>D</code> 是一个非 tabBar 页面，并且我们只会从 <code>tabB</code> 页面打开它</li></ul> <div class="table-wrp"><table><thead><tr><th>当前页面</th> <th><code>switchTab</code> 目标页面</th> <th>触发的生命周期（按顺序）</th></tr></thead> <tbody><tr><td><code>tabA</code></td> <td><code>tabA</code></td> <td>Nothing happened</td></tr> <tr><td><code>tabA</code></td> <td><code>tabB</code></td> <td><code>tabA.onHide()</code>, <code>tabB.onLoad()</code>, <code>tabB.onShow()</code></td></tr> <tr><td><code>tabA</code></td> <td><code>tabB</code>（再次打开）</td> <td><code>tabA.onHide()</code>, <code>tabB.onShow()</code></td></tr> <tr><td><code>C</code></td> <td><code>tabA</code></td> <td><code>C.onUnload()</code>, <code>tabA.onShow()</code></td></tr> <tr><td><code>C</code></td> <td><code>tabB</code></td> <td><code>C.onUnload()</code>, <code>tabB.onLoad()</code>, <code>tabB.onShow()</code></td></tr> <tr><td><code>D</code></td> <td><code>tabB</code></td> <td><code>D.onUnload()</code>, <code>tabB.onShow()</code></td></tr> <tr><td><code>D</code>（从转发进入）</td> <td><code>tabA</code></td> <td><code>D.onUnload()</code>, <code>tabA.onLoad()</code>, <code>tabA.onShow()</code></td></tr> <tr><td><code>D</code>（从转发进入）</td> <td><code>tabB</code></td> <td><code>D.onUnload()</code>, <code>tabB.onLoad()</code>, <code>tabB.onShow()</code></td></tr></tbody></table></div></div> <div class="fixed-translate" style="display:none;"><span>The translations are provided by WeChat Translation and are for reference only. In case of any inconsistency and discrepancy between the Chinese version and the English version, the Chinese version shall prevail.Incorrect translation. <a href="javascript:;" class="fixed-translate-btn">Tap to report.</a></span></div></div> <!----> <div class="related"><!----> <!----></div> <footer class="page-edit"><!----></footer>  <footer class="footer"><ul class="footer-links"><li class="footer-link"><a href="http://www.tencent.com/zh-cn/index.shtml" target="_blank">关于腾讯</a></li> <li class="footer-link"><a href="https://mp.weixin.qq.com/debug/wxadoc/introduction/index.html?t=1484641676" target="_blank">文档中心</a></li> <li class="footer-link"><a href="https://kf.qq.com/faq/17030722muuu170307MFBny2.html" target="_blank">辟谣中心</a></li> <li class="footer-link"><a href="http://kf.qq.com/faq/120911VrYVrA1509086vyumm.html" target="_blank">客服中心</a></li></ul> <p class="copyright">Copyright © 2012-<span>2026</span> Tencent. All Rights Reserved.</p></footer></div></main></div> <!----></div></div> <div id="popoverWrapId" class="pop-links__wrp popover_hide"><ul class="pop-links__list"><li class="pop-links__item"><button class="pop-link">复制</button></li> <li class="pop-links__item"><button class="pop-link">问题反馈</button></li></ul></div> <div class="fixed-btns"><a href="javascript:;" class="fixed-btn fixed-btn__feedback"><div class="fixed-btn__inner"><span class="fixed-btn__icon"></span> <span class="fixed-btn__text">反馈</span></div></a> <a href="javascript:;" class="fixed-btn fixed-btn__top" style="display:none;"><div class="fixed-btn__inner"><span class="fixed-btn__icon"></span></div></a></div></div></div></div>

 succeeded in 673ms:
252:    <!----></a> <!----> <!----></span></li></ul></div></li></ul></div></div> </aside></div> <div class="page__wrp"><main class="page"><div class="page-inner" style="min-height:0px;"> <div id="docContent"><div class="Breadcrumb"></div> <div class="content custom"><h1 id="全局配置"><a href="#全局配置" class="header-anchor">#</a> 全局配置</h1> <p>小程序根目录下的 <code>app.json</code> 文件用来对微信小程序进行全局配置。文件内容为一个 JSON 对象，有以下属性：</p> <h2 id="配置项"><a href="#配置项" class="header-anchor">#</a> 配置项</h2> <div class="table-wrp"><table><thead><tr><th>属性</th> <th>类型</th> <th>必填</th> <th>描述</th> <th>最低版本</th></tr></thead> <tbody><tr><td><a href="#entryPagePath">entryPagePath</a></td> <td>string</td> <td>否</td> <td>小程序默认启动首页</td> <td></td></tr> <tr><td><a href="#pages">pages</a></td> <td>string[]</td> <td>是</td> <td>页面路径列表</td> <td></td></tr> <tr><td><a href="#window">window</a></td> <td>Object</td> <td>否</td> <td>全局的默认窗口表现</td> <td></td></tr> <tr><td><a href="#tabBar">tabBar</a></td> <td>Object</td> <td>否</td> <td>底部 <code>tab</code> 栏的表现</td> <td></td></tr> <tr><td><a href="#networkTimeout">networkTimeout</a></td> <td>Object</td> <td>否</td> <td>网络超时时间</td> <td></td></tr> <tr><td><a href="#debug">debug</a></td> <td>boolean</td> <td>否</td> <td>是否开启 debug 模式，默认关闭</td> <td></td></tr> <tr><td><a href="#functionalPages">functionalPages</a></td> <td>boolean</td> <td>否</td> <td>是否启用插件功能页，默认关闭</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.1.0'</a></td></tr> <tr><td><a href="#subpackages">subpackages</a></td> <td>Object[]</td> <td>否</td> <td>分包结构配置</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'1.7.3'</a></td></tr> <tr><td><a href="#workers">workers</a></td> <td>string</td> <td>否</td> <td><code>Worker</code> 代码放置的目录</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'1.9.90'</a></td></tr> <tr><td><a href="#requiredBackgroundModes">requiredBackgroundModes</a></td> <td>string[]</td> <td>否</td> <td>需要在后台使用的能力，如「音乐播放」</td> <td></td></tr> <tr><td><a href="#requiredPrivateInfos">requiredPrivateInfos</a></td> <td>string[]</td> <td>否</td> <td>调用的地理位置相关隐私接口</td> <td></td></tr> <tr><td><a href="#plugins">plugins</a></td> <td>Object</td> <td>否</td> <td>使用到的插件</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'1.9.6'</a></td></tr> <tr><td><a href="#preloadRule">preloadRule</a></td> <td>Object</td> <td>否</td> <td>分包预下载规则</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.3.0'</a></td></tr> <tr><td><a href="#resizable">resizable</a></td> <td>boolean</td> <td>否</td> <td>PC 小程序是否支持用户任意改变窗口大小（包括最大化窗口）；iPad 小程序是否支持屏幕旋转。默认关闭</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.3.0'</a></td></tr> <tr><td><a href="#usingComponents">usingComponents</a></td> <td>Object</td> <td>否</td> <td>全局<a href="/miniprogram/dev/framework/custom-component/" target="_blank">自定义组件</a>配置</td> <td>开发者工具 1.02.1810190</td></tr> <tr><td><a href="#permission">permission</a></td> <td>Object</td> <td>否</td> <td>小程序接口权限相关设置</td> <td>微信客户端 7.0.0</td></tr> <tr><td><a href="#sitemapLocation">sitemapLocation</a></td> <td>string</td> <td>是</td> <td>指明 sitemap.json 的位置</td> <td></td></tr> <tr><td><a href="#style">style</a></td> <td>string</td> <td>否</td> <td>指定使用升级后的weui样式</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.8.0'</a></td></tr> <tr><td><a href="#useextendedlib">useExtendedLib</a></td> <td>Object</td> <td>否</td> <td>指定需要引用的扩展库</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.2.1'</a></td></tr> <tr><td><a href="#entranceDeclare">entranceDeclare</a></td> <td>Object</td> <td>否</td> <td>微信消息用小程序打开</td> <td>微信客户端 7.0.9</td></tr> <tr><td><a href="#darkmode">darkmode</a></td> <td>boolean</td> <td>否</td> <td>小程序支持 DarkMode</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.11.0'</a></td></tr> <tr><td><a href="#themeLocation">themeLocation</a></td> <td>string</td> <td>否</td> <td>指明 theme.json 的位置，darkmode为true为必填</td> <td>开发者工具 1.03.2004271</td></tr> <tr><td><a href="#lazyCodeLoading">lazyCodeLoading</a></td> <td>string</td> <td>否</td> <td>配置自定义组件代码按需注入</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.11.1'</a></td></tr> <tr><td><a href="#singlePage">singlePage</a></td> <td>Object</td> <td>否</td> <td>单页模式相关配置</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.12.0'</a></td></tr> <tr><td>supportedMaterials</td> <td>Object</td> <td>否</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/material/support_material.html" target="_blank">聊天素材小程序打开</a>相关配置</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.14.3'</a></td></tr> <tr><td>serviceProviderTicket</td> <td>string</td> <td>否</td> <td><a href="https://developers.weixin.qq.com/doc/oplatform/Third-party_Platforms/2.0/operation/thirdparty/customized_service_platform_guidelines" target="_blank">定制化型服务商</a>票据</td> <td></td></tr> <tr><td><a href="#embeddedAppIdList">embeddedAppIdList</a></td> <td>string[]</td> <td>否</td> <td>半屏小程序 appId</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.20.1'</a></td></tr> <tr><td><a href="#halfPage">halfPage</a></td> <td>Object</td> <td>否</td> <td>视频号直播半屏场景设置</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.18.0'</a></td></tr> <tr><td><a href="#debugOptions">debugOptions</a></td> <td>Object</td> <td>否</td> <td>调试相关配置</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.22.1'</a></td></tr> <tr><td><a href="#enablePassiveEvent">enablePassiveEvent</a></td> <td>Object或boolean</td> <td>否</td> <td>touch 事件监听是否为 passive</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.24.1'</a></td></tr> <tr><td><a href="#resolveAlias">resolveAlias</a></td> <td>Object</td> <td>否</td> <td>自定义模块映射规则</td> <td></td></tr> <tr><td><a href="#renderer">renderer</a></td> <td>string</td> <td>否</td> <td>全局默认的渲染后端</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.30.4'</a></td></tr> <tr><td><a href="#rendererOptions">rendererOptions</a></td> <td>Object</td> <td>否</td> <td>渲染后端选项</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.31.1'</a></td></tr> <tr><td>componentFramework</td> <td>string</td> <td>否</td> <td>组件框架，详见<a href="https://developers.weixin.qq.com/miniprogram/dev/framework/custom-component/glass-easel/migration.html" target="_blank">相关文档</a></td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.30.4'</a></td></tr> <tr><td>miniApp</td> <td>Object</td> <td>否</td> <td>多端模式场景接入身份管理服务时开启小程序授权页相关配置，详见<a href="https://developers.weixin.qq.com/miniprogram/dev/platform-capabilities/miniapp/quickstart/auth" target="_blank">相关文档</a></td> <td></td></tr> <tr><td>static</td> <td>Object</td> <td>否</td> <td>正常情况下默认所有资源文件都被打包发布到所有平台，可以通过 static 字段配置特定每个目录/文件只能发布到特定的平台(多端场景) <a href="https://developers.weixin.qq.com/miniprogram/dev/platform-capabilities/miniapp/pre-read/condition-compile" target="_blank">相关文档</a></td> <td></td></tr> <tr><td>convertRpxToVw</td> <td>boolean</td> <td>否</td> <td>配置是否将 rpx 单位转换为 vw 单位，开启后能修复某些 rpx 下的精度问题</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'3.3.0'</a></td></tr> <tr><td><a href="#chatTools">chatTools</a></td> <td>Object</td> <td>否</td> <td>聊天工具分包配置</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'3.7.8'</a></td></tr></tbody></table></div><h3 id="entryPagePath"><a href="#entryPagePath" class="header-anchor">#</a> entryPagePath</h3> <p>指定小程序的默认启动路径（首页），常见情景是从微信聊天列表页下拉启动、小程序列表启动等。如果不填，将默认为 <code>pages</code> 列表的第一项。不支持带页面路径参数。</p> <div class="language-json extra-class"><pre class="language-json"><code><span class="token punctuation">{</span>
253:  <span class="token property">&quot;entryPagePath&quot;</span><span class="token operator">:</span> <span class="token string">&quot;pages/index/index&quot;</span>
255:</code></pre></div><h3 id="pages"><a href="#pages" class="header-anchor">#</a> pages</h3> <p>用于指定小程序由哪些页面组成，每一项都对应一个页面的 路径（含文件名） 信息。文件名不需要写文件后缀，框架会自动去寻找对应位置的 <code>.json</code>, <code>.js</code>, <code>.wxml</code>, <code>.wxss</code> 四个文件进行处理。</p> <p>未指定 <code>entryPagePath</code> 时，数组的第一项代表小程序的初始页面（首页）。</p> <p><strong>小程序中新增/减少页面，都需要对 pages 数组进行修改。</strong></p> <p>如开发目录为：</p> <div class="language- extra-class"><pre class="language-text"><code>├── app.js
258:├── pages
269:  <span class="token property">&quot;pages&quot;</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">&quot;pages/index/index&quot;</span><span class="token punctuation">,</span> <span class="token string">&quot;pages/logs/logs&quot;</span><span class="token punctuation">]</span>
271:</code></pre></div><h3 id="window"><a href="#window" class="header-anchor">#</a> window</h3> <p>用于设置小程序的状态栏、导航条、标题、窗口背景色。</p> <div class="table-wrp"><table><thead><tr><th>属性</th> <th>类型</th> <th>默认值</th> <th>描述</th> <th>最低版本</th></tr></thead> <tbody><tr><td>navigationBarBackgroundColor</td> <td>HexColor</td> <td>#000000</td> <td>导航栏背景颜色，如 <code>#000000</code></td> <td></td></tr> <tr><td>navigationBarTextStyle</td> <td>string</td> <td>white</td> <td>导航栏标题、状态栏颜色，仅支持 <code>black</code> / <code>white</code></td> <td></td></tr> <tr><td>navigationBarTitleText</td> <td>string</td> <td></td> <td>导航栏标题文字内容</td> <td></td></tr> <tr><td>navigationStyle</td> <td>string</td> <td>default</td> <td>导航栏样式，仅支持以下值：<br><code>default</code> 默认样式<br> <code>custom</code> 自定义导航栏，只保留右上角胶囊按钮。参见注 2。</td> <td>iOS/Android 微信客户端 6.6.0，Windows/Mac 微信基础库 3.6.1</td></tr> <tr><td>homeButton</td> <td>boolean</td> <td>false</td> <td>在非首页、非页面栈最底层页面或非tabbar内页面中的导航栏展示home键</td> <td>微信客户端 8.0.24</td></tr> <tr><td>backgroundColor</td> <td>HexColor</td> <td>#ffffff</td> <td>窗口的背景色</td> <td></td></tr> <tr><td>backgroundTextStyle</td> <td>string</td> <td>dark</td> <td>下拉 loading 的样式，仅支持 <code>dark</code> / <code>light</code></td> <td></td></tr> <tr><td>backgroundColorTop</td> <td>string</td> <td>#ffffff</td> <td>顶部窗口的背景色，仅 iOS 支持</td> <td>微信客户端 6.5.16</td></tr> <tr><td>backgroundColorBottom</td> <td>string</td> <td>#ffffff</td> <td>底部窗口的背景色，仅 iOS 支持</td> <td>微信客户端 6.5.16</td></tr> <tr><td>enablePullDownRefresh</td> <td>boolean</td> <td>false</td> <td>是否开启全局的下拉刷新。<br>详见 <a href="../api/Page#onpulldownrefresh" target="_blank">Page.onPullDownRefresh</a></td> <td></td></tr> <tr><td>onReachBottomDistance</td> <td>number</td> <td>50</td> <td>页面上拉触底事件触发时距页面底部距离，单位为 px。<br>详见 <a href="../api/Page#onreachbottom" target="_blank">Page.onReachBottom</a></td> <td></td></tr> <tr><td>pageOrientation</td> <td>string</td> <td>portrait</td> <td>屏幕旋转设置，支持 <code>auto</code> / <code>portrait</code> / <code>landscape</code> <br>详见 <a href="https://developers.weixin.qq.com/miniprogram/dev/framework/view/resizable.html" target="_blank">响应显示区域变化</a></td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.4.0'</a> (auto) / <a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.5.0'</a> (landscape)</td></tr> <tr><td><a href="#restartStrategy">restartStrategy</a></td> <td>string</td> <td>homePage</td> <td>重新启动策略配置</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.8.0'</a></td></tr> <tr><td>initialRenderingCache</td> <td>string</td> <td></td> <td>页面<a href="https://developers.weixin.qq.com/miniprogram/dev/framework/view/initial-rendering-cache.html" target="_blank">初始渲染缓存</a>配置，支持 <code>static</code> / <code>dynamic</code></td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.11.1'</a></td></tr> <tr><td>visualEffectInBackground</td> <td>string</td> <td>none</td> <td>切入系统后台时，隐藏页面内容，保护用户隐私。支持 <code>hidden</code> / <code>none</code></td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.15.0'</a></td></tr> <tr><td>handleWebviewPreload</td> <td>string</td> <td>static</td> <td>控制<a href="https://developers.weixin.qq.com/miniprogram/dev/framework/performance/tips/runtime_nav.html#_2-4-%E6%8E%A7%E5%88%B6%E9%A2%84%E5%8A%A0%E8%BD%BD%E4%B8%8B%E4%B8%AA%E9%A1%B5%E9%9D%A2%E7%9A%84%E6%97%B6%E6%9C%BA" target="_blank">预加载下个页面的时机</a>。支持 <code>static</code> / <code>manual</code> / <code>auto</code></td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.15.0'</a></td></tr></tbody></table></div><ul><li>注 1：HexColor（十六进制颜色值），如&quot;#ff00ff&quot;</li> <li>注 2：关于<code>navigationStyle</code> <ul><li>iOS/Android 客户端 7.0.0 以下版本，<code>navigationStyle</code> 只在 <code>app.json</code> 中生效。</li> <li>iOS/Android 客户端 6.7.2 版本开始，<code>navigationStyle: custom</code> 对 <a href="https://developers.weixin.qq.com/miniprogram/dev/component/web-view.html" target="_blank">web-view</a> 组件无效</li> <li>开启 custom 后，低版本客户端需要做好兼容。开发者工具基础库版本切到 1.7.0（不代表最低版本，只供调试用）可方便切到旧视觉</li></ul></li></ul> <h4 id="restartStrategy"><a href="#restartStrategy" class="header-anchor">#</a> restartStrategy</h4> <blockquote><p>基础库 '2.8.0' 开始支持，低版本需做<a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank" rel="noopener noreferrer">兼容处理<span></span></a>。</p></blockquote> <p><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/runtime/operating-mechanism.html#_2-1-%E9%87%8D%E6%96%B0%E5%90%AF%E5%8A%A8%E7%AD%96%E7%95%A5" target="_blank">重新启动策略</a>配置</p> <div class="table-wrp"><table><thead><tr><th>可选值</th> <th>含义</th></tr></thead> <tbody><tr><td>homePage</td> <td>（默认值）如果从这个页面退出小程序，下次将从首页冷启动</td></tr> <tr><td>homePageAndLatestPage</td> <td>如果从这个页面退出小程序，下次冷启动后立刻加载这个页面，页面的参数保持不变（不可用于 tab 页）</td></tr></tbody></table></div><p>如：</p> <div class="language-json extra-class"><pre class="language-json"><code><span class="token punctuation">{</span>
280:</code></pre></div><img src="https://res8.wxqcloud.qq.com.cn/wxdoc/a0be6d67-aa37-43d0-849e-d1f047504fe3.jpg" width="600px"> <h3 id="tabBar"><a href="#tabBar" class="header-anchor">#</a> tabBar</h3> <p>如果小程序是一个多 tab 应用（客户端窗口的底部或顶部有 tab 栏可以切换页面），可以通过 tabBar 配置项指定 tab 栏的表现，以及 tab 切换时显示的对应页面。</p> <div class="table-wrp"><table><thead><tr><th>属性</th> <th>类型</th> <th>必填</th> <th>默认值</th> <th>描述</th> <th>最低版本</th></tr></thead> <tbody><tr><td>color</td> <td>HexColor</td> <td>是</td> <td></td> <td>tab 上的文字默认颜色，仅支持十六进制颜色</td> <td></td></tr> <tr><td>selectedColor</td> <td>HexColor</td> <td>是</td> <td></td> <td>tab 上的文字选中时的颜色，仅支持十六进制颜色</td> <td></td></tr> <tr><td>backgroundColor</td> <td>HexColor</td> <td>是</td> <td></td> <td>tab 的背景色，仅支持十六进制颜色</td> <td></td></tr> <tr><td>borderStyle</td> <td>string</td> <td>否</td> <td>black</td> <td>tabbar 上边框的颜色， 仅支持 <code>black</code> / <code>white</code></td> <td></td></tr> <tr><td>list</td> <td>Array</td> <td>是</td> <td></td> <td>tab 的列表，详见 <code>list</code> 属性说明，最少 2 个、最多 5 个 tab</td> <td></td></tr> <tr><td>position</td> <td>string</td> <td>否</td> <td>bottom</td> <td>tabBar 的位置，仅支持 <code>bottom</code> / <code>top</code></td> <td></td></tr> <tr><td>custom</td> <td>boolean</td> <td>否</td> <td>false</td> <td>自定义 tabBar，见<a href="https://developers.weixin.qq.com/miniprogram/dev/framework/ability/custom-tabbar.html" target="_blank">详情</a></td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank">'2.5.0'</a></td></tr></tbody></table></div><p>其中 list 接受一个数组，<strong>只能配置最少 2 个、最多 5 个 tab</strong>。tab 按数组的顺序排序，每个项都是一个对象，其属性值如下：</p> <div class="table-wrp"><table><thead><tr><th>属性</th> <th>类型</th> <th>必填</th> <th>说明</th></tr></thead> <tbody><tr><td>pagePath</td> <td>string</td> <td>是</td> <td>页面路径，必须在 pages 中先定义</td></tr> <tr><td>text</td> <td>string</td> <td>是</td> <td>tab 上按钮文字</td></tr> <tr><td>iconPath</td> <td>string</td> <td>否</td> <td>图片路径，icon 大小限制为 40kb，建议尺寸为 81px * 81px，不支持网络图片。<br><strong>当 <code>position</code> 为 <code>top</code> 时，不显示 icon。</strong></td></tr> <tr><td>selectedIconPath</td> <td>string</td> <td>否</td> <td>选中时的图片路径，icon 大小限制为 40kb，建议尺寸为 81px * 81px，不支持网络图片。<br><strong>当 <code>position</code> 为 <code>top</code> 时，不显示 icon。</strong></td></tr></tbody></table></div><img src="https://res8.wxqcloud.qq.com.cn/wxdoc/6a5ada5f-f394-469c-b686-ad2a8951baa6.png"> <h3 id="networkTimeout"><a href="#networkTimeout" class="header-anchor">#</a> networkTimeout</h3> <p>各类网络请求的超时时间，单位均为毫秒。</p> <div class="table-wrp"><table><thead><tr><th>属性</th> <th>类型</th> <th>必填</th> <th>默认值</th> <th>说明</th></tr></thead> <tbody><tr><td>request</td> <td>number</td> <td>否</td> <td>60000</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/api/network/request/wx.request.html" target="_blank">wx.request</a> 的超时时间，单位：毫秒。</td></tr> <tr><td>connectSocket</td> <td>number</td> <td>否</td> <td>60000</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/api/network/websocket/SocketTask.html" target="_blank">wx.connectSocket</a> 的超时时间，单位：毫秒。</td></tr> <tr><td>uploadFile</td> <td>number</td> <td>否</td> <td>60000</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/api/network/upload/wx.uploadFile.html" target="_blank">wx.uploadFile</a> 的超时时间，单位：毫秒。</td></tr> <tr><td>downloadFile</td> <td>number</td> <td>否</td> <td>60000</td> <td><a href="https://developers.weixin.qq.com/miniprogram/dev/api/network/download/wx.downloadFile.html" target="_blank">wx.downloadFile</a> 的超时时间，单位：毫秒。</td></tr></tbody></table></div><h3 id="debug"><a href="#debug" class="header-anchor">#</a> debug</h3> <p>可以在开发者工具中开启 <code>debug</code> 模式，在开发者工具的控制台面板，调试信息以 <code>info</code> 的形式给出，其信息有 Page 的注册，页面路由，数据更新，事件触发等。可以帮助开发者快速定位一些常见的问题。</p> <h3 id="functionalPages"><a href="#functionalPages" class="header-anchor">#</a> functionalPages</h3> <blockquote><p>基础库 '2.1.0' 开始支持，低版本需做<a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank" rel="noopener noreferrer">兼容处理<span></span></a>。</p></blockquote> <p>插件所有者小程序需要设置这一项来启用<a href="https://developers.weixin.qq.com/miniprogram/dev/framework/plugin/functional-pages" target="_blank">插件功能页</a>。</p> <h3 id="subpackages"><a href="#subpackages" class="header-anchor">#</a> subpackages</h3> <blockquote><p>微信客户端 6.6.0 ，基础库 1.7.3 及以上版本支持</p></blockquote> <p>启用<a href="https://developers.weixin.qq.com/miniprogram/dev/framework/subpackages" target="_blank">分包加载</a>时，声明项目分包结构。</p> <blockquote><p>写成 subPackages 也支持。</p></blockquote> <h3 id="workers"><a href="#workers" class="header-anchor">#</a> workers</h3> <blockquote><p>基础库 '1.9.90' 开始支持，低版本需做<a href="https://developers.weixin.qq.com/miniprogram/dev/framework/compatibility.html" target="_blank" rel="noopener noreferrer">兼容处理<span></span></a>。</p></blockquote> <p>使用 <a href="https://developers.weixin.qq.com/miniprogram/dev/framework/workers" target="_blank">Worker</a> 处理多线程任务时，设置 <code>Worker</code> 代码放置的目录</p> <h3 id="requiredBackgroundModes"><a href="#requiredBackgroundModes" class="header-anchor">#</a> requiredBackgroundModes</h3> <blockquote><p>微信客户端 6.7.2 及以上版本支持</p></blockquote> <p>申明需要后台运行的能力，类型为数组。目前支持以下项目：</p> <ul><li><code>audio</code>: 后台音乐播放</li> <li><code>location</code>: 后台定位</li></ul> <p>如：</p> <div class="language-json extra-class"><pre class="language-json"><code><span class="token punctuation">{</span>
281:  <span class="token property">&quot;pages&quot;</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">&quot;pages/index/index&quot;</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
285:  <span class="token property">&quot;pages&quot;</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">&quot;pages/index/index&quot;</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
294:  <span class="token property">&quot;pages&quot;</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">&quot;pages/index/index&quot;</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
309:        <span class="token property">&quot;path&quot;</span><span class="token operator">:</span> <span class="token string">&quot;pages/index/index&quot;</span><span class="token punctuation">,</span>
384:      <span class="token property">&quot;entryPagePath&quot;</span><span class="token operator">:</span> <span class="token string">&quot;pages/activity_create/index&quot;</span><span class="token punctuation">,</span>
393:  <span class="token property">&quot;pages&quot;</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">&quot;pages/index/index&quot;</span><span class="token punctuation">,</span> <span class="token string">&quot;pages/logs/index&quot;</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
400:        <span class="token property">&quot;pagePath&quot;</span><span class="token operator">:</span> <span class="token string">&quot;pages/index/index&quot;</span><span class="token punctuation">,</span>
401:        <span class="token property">&quot;text&quot;</span><span class="token operator">:</span> <span class="token string">&quot;首页&quot;</span>
404:        <span class="token property">&quot;pagePath&quot;</span><span class="token operator">:</span> <span class="token string">&quot;pages/logs/logs&quot;</span><span class="token punctuation">,</span>

 succeeded in 718ms:
12:  <link rel="mask-icon" color="#4C4C4C" href="https://res.wx.qq.com/a/wx_fed/assets/res/MjliNWVm.svg">
23:      maskMode: 'no-mask', // 隐私策略, all-mask 或 no-mask, 详见：https://dev.weixin.qq.com/docs/analysis/sdk/docs.html
52:          console.error('Error loading scripts:', error);
148:</a></div></nav></div> <div class="links-panel__ft"><ul class="lang-tab"><li class="lang-tab__icon"><img src="https://res.wx.qq.com/t/components/icons/base/translate_regular.svg"></li></ul></div></div> <div><div class="weui-mask" style="display:none;"></div> <div class="weui-actionsheet "><!----> <div class="weui-actionsheet__menu"><div class="weui-actionsheet__cell">中文</div><div class="weui-actionsheet__cell">EN</div></div> <div class="weui-actionsheet__action"><div class="weui-actionsheet__cell">取消</div></div></div></div></div> <a href="javascript:;" class="mobile-search-btn"></a> <div class="main-container" style="margin-top:144px;"><div class="main-contontaier__bd" style="min-height:0px;"><div class="sidebar__wrp"><div class="sidebar-cell_mobile"><li class="subnavbar__item selected"><a href="javascript:;" target="_self">API</a></li></div> <aside class="sidebar" style="top:144px;"> <div class="TreeNavigation"><div class="NavigationLevel NavigationLevel--level-0"><ul><li><div class="NavigationLevel NavigationLevel--closed NavigationLevel--level-1"><div class="NavigationLevel__parent"><span class="NavigationToggle NavigationToggle--closed"><span class="NavigationToggle__icon NavigationToggle__icon--closed"></span></span> <span class="NavigationItem"><!----> <a href="/miniprogram/dev/api/base/wx.env.html" class="NavigationItem__router-link">
536:    <!----></a> <!----> <!----></span></li><li><span class="NavigationItem"><!----> <a href="/miniprogram/dev/api/ui/interaction/wx.hideLoading.html" class="NavigationItem__router-link">
537:      wx.hideLoading
3498:    <!----></a> <!----> <!----></span></li></ul></div></li></ul></div></li></ul></div></div> </aside></div> <div class="page__wrp"><main class="page"><div class="page-inner" style="min-height:0px;"> <div id="docContent"><div class="Breadcrumb"></div> <div class="content custom"><h1 id="wx-showLoading-Object-object"><a href="#wx-showLoading-Object-object" class="header-anchor">#</a> wx.showLoading(Object object)</h1> <blockquote><p>基础库 1.1.0 开始支持，低版本需做<a href="../../../framework/compatibility.html">兼容处理</a>。</p></blockquote> <blockquote><p><strong>以 <a href="../../../framework/app-service/api.html#%E5%BC%82%E6%AD%A5-API-%E8%BF%94%E5%9B%9E-Promise">Promise 风格</a> 调用</strong>：支持</p> <p><strong>小程序插件</strong>：支持，需要小程序基础库版本不低于 <a href="../../../framework/compatibility.html">1.9.6</a></p> <p><strong>微信 Windows 版</strong>：支持</p> <p><strong>微信 Mac 版</strong>：支持</p> <p><strong>微信 鸿蒙 OS 版</strong>：支持</p></blockquote> <h2 id="功能描述"><a href="#功能描述" class="header-anchor">#</a> 功能描述</h2> <p>显示 loading 提示框。需主动调用 wx.hideLoading 才能关闭提示框</p> <h2 id="参数"><a href="#参数" class="header-anchor">#</a> 参数</h2> <h3 id="Object-object"><a href="#Object-object" class="header-anchor">#</a> Object object</h3> <div class="table-wrp"><table><thead><tr><th>属性</th> <th>类型</th> <th>默认值</th> <th>必填</th> <th>说明</th></tr></thead> <tbody><tr><td>title</td> <td>string</td> <td></td> <td>是</td> <td>提示的内容</td></tr> <tr><td>mask</td> <td>boolean</td> <td>false</td> <td>否</td> <td>是否显示透明蒙层，防止触摸穿透</td></tr> <tr><td>success</td> <td>function</td> <td></td> <td>否</td> <td>接口调用成功的回调函数</td></tr> <tr><td>fail</td> <td>function</td> <td></td> <td>否</td> <td>接口调用失败的回调函数</td></tr> <tr><td>complete</td> <td>function</td> <td></td> <td>否</td> <td>接口调用结束的回调函数（调用成功、失败都会执行）</td></tr></tbody></table></div><h2 id="示例代码"><a href="#示例代码" class="header-anchor">#</a> 示例代码</h2> <div class="language-js extra-class"><pre class="language-js"><code>wx<span class="token punctuation">.</span><span class="token function">showLoading</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
3503:  wx<span class="token punctuation">.</span><span class="token function">hideLoading</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
3505:</code></pre></div><h2 id="注意"><a href="#注意" class="header-anchor">#</a> 注意</h2> <ul><li><a href="wx.showLoading.html">wx.showLoading</a> 和 <a href="wx.showToast.html">wx.showToast</a> 同时只能显示一个</li> <li><a href="wx.showLoading.html">wx.showLoading</a> 应与 <a href="wx.hideLoading.html">wx.hideLoading</a> 配对使用</li></ul></div> <div class="fixed-translate" style="display:none;"><span>The translations are provided by WeChat Translation and are for reference only. In case of any inconsistency and discrepancy between the Chinese version and the English version, the Chinese version shall prevail.Incorrect translation. <a href="javascript:;" class="fixed-translate-btn">Tap to report.</a></span></div></div> <!----> <div class="related"><!----> <!----></div> <footer class="page-edit"><!----></footer>  <footer class="footer"><ul class="footer-links"><li class="footer-link"><a href="http://www.tencent.com/zh-cn/index.shtml" target="_blank">关于腾讯</a></li> <li class="footer-link"><a href="https://mp.weixin.qq.com/debug/wxadoc/introduction/index.html?t=1484641676" target="_blank">文档中心</a></li> <li class="footer-link"><a href="https://kf.qq.com/faq/17030722muuu170307MFBny2.html" target="_blank">辟谣中心</a></li> <li class="footer-link"><a href="http://kf.qq.com/faq/120911VrYVrA1509086vyumm.html" target="_blank">客服中心</a></li></ul> <p class="copyright">Copyright © 2012-<span>2026</span> Tencent. All Rights Reserved.</p></footer></div></main></div> <!----></div></div> <div id="popoverWrapId" class="pop-links__wrp popover_hide"><ul class="pop-links__list"><li class="pop-links__item"><button class="pop-link">复制</button></li> <li class="pop-links__item"><button class="pop-link">问题反馈</button></li></ul></div> <div class="fixed-btns"><a href="javascript:;" class="fixed-btn fixed-btn__feedback"><div class="fixed-btn__inner"><span class="fixed-btn__icon"></span> <span class="fixed-btn__text">反馈</span></div></a> <a href="javascript:;" class="fixed-btn fixed-btn__top" style="display:none;"><div class="fixed-btn__inner"><span class="fixed-btn__icon"></span></div></a></div></div></div></div>

exec
/bin/bash -lc 'rtk nl -ba backend/apps/approvals/urls.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.urls import path
     2	from . import views
     3	
     4	urlpatterns = [
     5	    path('', views.list_approvals, name='list_approvals'),
     6	    path('<str:approval_id>/approve/', views.approve_approval, name='approve_approval'),
     7	    path('<str:approval_id>/reject/', views.reject_approval, name='reject_approval'),
     8	]

exec
/bin/bash -lc 'rtk nl -ba backend/apps/applications/urls.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.urls import path
     2	from . import views
     3	
     4	urlpatterns = [
     5	    path('', views.applications_view, name='applications'),
     6	    path('<str:application_id>/', views.get_application, name='get_application'),
     7	]

exec
/bin/bash -lc 'rtk nl -ba backend/config/urls.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	"""URL Configuration"""
     2	from django.contrib import admin
     3	from django.urls import path, include
     4	
     5	urlpatterns = [
     6	    path('admin/', admin.site.urls),
     7	    path('api/auth/', include('apps.users.urls')),
     8	    path('api/applications/', include('apps.applications.urls')),
     9	    path('api/approvals/', include('apps.approvals.urls')),
    10	]

codex
# 问题1：实施顺序

**风险分析：** 当前“完整页面先做完，最后接路由”的顺序不建议接受。它会让学生主流程在一段时间内不可验证，且现有 `login.ts` 仍把所有角色跳到审批列表：[login.ts](/home/caohui/projects/graduation-leave-system/miniprogram/pages/login/login.ts:40)。`approvals` 页也只校验登录，不校验角色：[approvals.ts](/home/caohui/projects/graduation-leave-system/miniprogram/pages/approvals/approvals.ts:16)。

微信官方 `app.json` 文档要求新增页面必须修改 `pages` 数组，且未指定 `entryPagePath` 时 `pages` 第一项是首页；所以注册顺序也有风险，不能误把新页放到第一项。

**推荐方案：** 采用“骨架优先 + 纵向切片”：

1. 创建最小 `student-application` 四件套，`Page({ onLoad/onShow guard })` 可运行。
2. 追加注册到 `app.json`，保持 `pages/login/login` 第一项不变。
3. 立即修改 `login.ts` 角色路由：`student -> student-application`，`counselor/dean -> approvals`。
4. 做最小 smoke：学生登录能进申请页，教师/学工能进审批页，非法角色回登录。
5. 再填充表单、提交、错误处理和成功跳转。

**理由：** 这比“先页面后路由”更早暴露集成问题，也比“先路由后页面”避免跳不存在页面。替代方案 A 的“先写注释路由”是坏味道，未执行代码不会被验证；替代方案 C 只测 404 不够，不能验证登录、权限、页面生命周期和 API 链路。

# 问题2：角色保护

**必要性分析：** 角色保护不能只依赖 `login.ts`。小程序页面可能通过重启恢复、分享、开发者工具路径、历史页面栈等方式进入；微信页面路由文档也明确 `reLaunch` 不是重启 AppService，全局 JS 状态不会因此重置。前端保护不是安全边界，后端才是安全边界，但页面级保护是必要的 UX 和防误入防线。

**推荐时机：** 从骨架页第一版就实现混合策略：

- `login.ts` 做正确角色分流。
- `student-application` 在 `onLoad` 和 `onShow` 都做 `requireRole('student')`。
- 后端继续保留权威角色校验，现有 `create_application` 已限制学生提交：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/views.py:77)。
- 测试要单独覆盖“学生登录路由正确”和“非学生直接访问被拦截”，不要让页面守卫掩盖路由 bug。

**理由：** 仅防御性保护会掩盖登录路由缺陷；仅依赖路由会漏掉直接进入页面；混合策略是正确分层。`console.warn` 可以保留给开发诊断，但不能代替用户可见提示和跳转处理。

# 问题3：错误处理

**YAGNI vs DRY权衡：** 当前已经不是 YAGNI。现有登录页、详情页、审批列表都在重复 `err.error?.message || err.message`，例如：[detail.ts](/home/caohui/projects/graduation-leave-system/miniprogram/pages/detail/detail.ts:66)。新页面再写一套会扩大不一致。

文档里的示例还有实际 bug：后端 `DORM_BLOCKED` 的 `blocking_reason` 位于 `err.error.details.blocking_reason`，不是 `err.error.blocking_reason`：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/views.py:101)。

**推荐策略：** 提取一个轻量通用函数到 `miniprogram/services/api.ts` 或 `miniprogram/services/errors.ts`，例如 `formatApiError(err, fallback, codeMessages?)`。通用层处理 `ApiError`、`Error`、网络失败、401；页面传入领域映射，如 `DORM_BLOCKED`、`CONFLICT`。

**理由：** 不建议做成 `ApiClient` 静态方法，错误格式化不是请求能力本身。也不建议只加 TODO，重复已经存在。重点是正确处理 `details` 可能为对象、数组或字符串，避免页面显示 `[object Object]`。

# 问题4：表单验证

**前端验证边界：** 前端验证用于即时反馈和减少无效请求，不能替代后端。微信 `picker mode=date` 支持 `start/end`，但客户端日期和页面数据都不可信；后端仍必须校验。微信 `textarea` 默认 `maxlength` 是 140，如果业务想要 500 字，必须显式设置。

**推荐范围：** 采用替代方案 C，但不要做特殊字符黑名单：

- `reason.trim()` 非空。
- `reason` 显式长度上限，建议先定为 500 字，并同步后端 serializer/契约。
- `leave_date` 必填、格式为 `YYYY-MM-DD`、不早于今天。
- WXML `picker` 设置 `start="{{today}}"`，提交前再校验一次。
- 不做“特殊字符禁止”，允许正常标点；XSS/SQL 注入由渲染转义、ORM、后端输出策略处理。

**理由：** 只做非空太弱，会把明显错误推给后端。只做前端长度/日期也不够，因为后端当前 `ApplicationCreateSerializer` 没有长度和最小日期约束：[serializers.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/serializers.py:35)。必须同时更新契约和后端，否则前后端行为会漂移。

# 问题5：成功跳转

**UX影响分析：** 当前 1500ms 是微信 `showToast` 默认时长，但提交成功后固定等待 1.5 秒偏慢；延迟期间如果不禁用交互，会出现重复提交、二次跳转、用户返回等竞态。微信官方 `showToast` 支持 `mask` 防止触摸穿透，`redirectTo` 是关闭当前页并跳新页，语义上适合“提交成功后不回到表单”。

**推荐方案：** 使用 `redirectTo`，延迟缩短到 800-1000ms，并加交互保护：

- 提交开始设置 `submitting: true`，按钮 disabled。
- 请求期间 `wx.showLoading({ title: '提交中', mask: true })`，完成后 `wx.hideLoading()`。
- 成功后 `wx.showToast({ title: '提交成功', icon: 'success', duration: 800, mask: true })`。
- `setTimeout` 后 `wx.redirectTo({ url: '/pages/detail/detail?id=' + encodeURIComponent(application_id) })`。
- 失败时恢复 `submitting: false`。
- 跳转失败要兜底提示或回退到申请列表。

**理由：** `navigateTo` 会保留表单页，用户返回后容易看到已提交的旧表单；且小程序 `navigateTo` 页面栈最多十层，不适合作为提交完成后的默认路径。`reLaunch` 太重，会清空所有页面。`redirectTo` 最符合“表单提交完成，当前页失效”的语义。

# 新发现的问题

**问题描述：** 文档没有提到“已有申请”的前置体验。后端 `CONFLICT` 返回 `existing_application_id`：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/applications/views.py:87)。学生进入申请页时可以先查自己的申请，如果已有待审批/已通过，直接跳详情或提示，而不是等提交失败。

**影响范围：** 学生重复提交体验、错误处理、成功/冲突跳转。

**推荐方案：** 页面 `onLoad` 可先 `listApplications` 判断已有有效申请；若不做预查，也必须在 `CONFLICT` 中读取 `details.existing_application_id` 并引导到详情页。

**问题描述：** API 错误结构和类型定义太宽。`ApiError.details?: any` 会让页面随意读取字段，文档示例已经读错字段。

**影响范围：** 所有页面错误展示。

**推荐方案：** 定义类型守卫和错误 formatter，至少覆盖 `VALIDATION_ERROR`、`FORBIDDEN`、`CONFLICT`、`DORM_BLOCKED`、`NOT_FOUND`、401/network fail。

**问题描述：** 当前登录成功路由缺少角色矩阵。`login.ts` 现在所有角色都进审批页，这和新增学生申请页直接冲突。

**影响范围：** 学生登录后的首屏、审批列表权限、端到端验收。

**推荐方案：** 在实现前先写清路由矩阵，并用 smoke 测试锁定：`student -> /pages/student-application/student-application`，`counselor/dean -> /pages/approvals/approvals`，未知角色清 token 并回登录。

**微信官方依据：**  
`app.json pages`、页面路由、`wx.navigateTo`、`wx.redirectTo`、`wx.reLaunch`、`wx.showToast`、`wx.showLoading`、`picker`、`textarea`：  
https://developers.weixin.qq.com/miniprogram/dev/reference/configuration/app.html  
https://developers.weixin.qq.com/miniprogram/dev/framework/app-service/route.html  
https://developers.weixin.qq.com/miniprogram/dev/api/route/wx.navigateTo.html  
https://developers.weixin.qq.com/miniprogram/dev/api/route/wx.redirectTo.html  
https://developers.weixin.qq.com/miniprogram/dev/api/route/wx.reLaunch.html  
https://developers.weixin.qq.com/miniprogram/dev/api/ui/interaction/wx.showToast.html  
https://developers.weixin.qq.com/miniprogram/dev/api/ui/interaction/wx.showLoading.html  
https://developers.weixin.qq.com/miniprogram/dev/component/picker.html  
https://developers.weixin.qq.com/miniprogram/dev/component/textarea.html
tokens used
118,237

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
