# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-07T15:24:33.810Z

## Original task

代码安全性和架构审计：

**审计文件：**
- backend/apps/users/views.py（demo-login端点实现）
- backend/apps/users/serializers.py（DemoLoginSerializer）
- backend/apps/users/urls.py（路由配置）

**审计重点：**
1. demo-login端点安全性：
   - DEMO_AUTH_ENABLED环境变量守卫是否足够？
   - 生产环境是否可能被误启用？
   - 是否有其他安全漏洞（认证绕过、token泄露）？

2. 认证机制：
   - JWT token生成和管理是否安全？
   - 会话管理是否有漏洞？
   - 密码处理是否安全（虽然是演示账号）？

3. 后端数据契约：
   - 序列化器是否完整？
   - 与前端期望是否一致？
   - 错误响应格式是否标准？

4. 生产环境风险：
   - 是否有阻塞生产部署的安全问题？
   - 需要哪些额外的安全加固？

**当前状态：**
- 8/8自动化测试通过
- 声称开发完成

请识别所有P0/P1安全和架构问题。

## Final prompt

代码安全性和架构审计：

**审计文件：**
- backend/apps/users/views.py（demo-login端点实现）
- backend/apps/users/serializers.py（DemoLoginSerializer）
- backend/apps/users/urls.py（路由配置）

**审计重点：**
1. demo-login端点安全性：
   - DEMO_AUTH_ENABLED环境变量守卫是否足够？
   - 生产环境是否可能被误启用？
   - 是否有其他安全漏洞（认证绕过、token泄露）？

2. 认证机制：
   - JWT token生成和管理是否安全？
   - 会话管理是否有漏洞？
   - 密码处理是否安全（虽然是演示账号）？

3. 后端数据契约：
   - 序列化器是否完整？
   - 与前端期望是否一致？
   - 错误响应格式是否标准？

4. 生产环境风险：
   - 是否有阻塞生产部署的安全问题？
   - 需要哪些额外的安全加固？

**当前状态：**
- 8/8自动化测试通过
- 声称开发完成

请识别所有P0/P1安全和架构问题。

## Raw output

```text
**Findings**
P0 - demo-login 可在生产被一个环境变量直接打开，属于生产阻塞  
位置：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:54)、[prod.py](/home/caohui/projects/graduation-leave-system/backend/config/settings/prod.py:4)、[urls.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/urls.py:6)  
`demo_login` 是 `AllowAny`，路由在所有环境无条件挂载，只检查 `os.environ.get('DEMO_AUTH_ENABLED') == 'true'`。`prod.py` 没有强制覆盖或启动失败保护；如果生产环境、容器镜像或 `.env` 中误设为 true，任何人可无密码获取 student/dorm_manager/counselor/dean JWT。当前本地 `backend/.env` 也存在 `DEMO_AUTH_ENABLED=true`，说明误带配置的风险不是理论问题。  
修复：生产 settings 中强制 `DEMO_AUTH_ENABLED = False`，并在启动时加 fail-fast：`if not DEBUG and DEMO_AUTH_ENABLED: raise ImproperlyConfigured(...)`。更好的是生产 URLconf 不挂载该路由，或返回 404。

P0 - JWT 签名密钥允许使用弱默认值，生产可启动  
位置：[base.py](/home/caohui/projects/graduation-leave-system/backend/config/settings/base.py:11)、[base.py](/home/caohui/projects/graduation-leave-system/backend/config/settings/base.py:146)  
`SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY`，但 `SECRET_KEY` 有可用默认值，`prod.py` 未强制要求真实密钥。`manage.py check --deploy --settings=config.settings.prod` 已提示 SECRET_KEY 弱值风险。若生产使用默认/开发密钥，攻击者可伪造 JWT，影响高于 demo-login。  
修复：生产环境必须缺失即失败，不允许默认 SECRET_KEY；JWT 签名密钥建议独立配置为 `JWT_SIGNING_KEY`，并强制长度/随机性校验。

P1 - demo-login 绑定真实固定账号，没有 demo-only 边界  
位置：[serializers.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/serializers.py:55)、[seed_data.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/management/commands/seed_data.py:40)  
`DemoLoginSerializer` 直接把 role 映射到真实 `User` 表里的固定 ID：`2020001/M001/T001/D001`。这些账号也是 seed/test 文档中的真实工作流账号，且默认密码等于 ID。只要这些账号进入生产库，demo-login 一旦开启就是对真实权限账号的无密码接管。  
修复：增加 `is_demo_account` 或单独 demo 用户表/租户；serializer 必须校验 `user.role == requested_role` 且 `user.is_demo_account is True`；生产导入脚本不得创建这些 demo 账号为 active。

P1 - 认证端点无节流/审计，普通登录可被暴力尝试  
位置：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:26)、[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:54)、[base.py](/home/caohui/projects/graduation-leave-system/backend/config/settings/base.py:113)  
`login` 和 `demo_login` 都是 `AllowAny`，REST_FRAMEWORK 未配置 throttle。普通登录没有账号/IP 级限速；demo-login 一旦开启也没有审计记录。  
修复：配置 DRF throttle，至少对 auth endpoints 使用 stricter scope；记录 demo-login 使用日志，包括 role、IP、UA、时间。

P1 - access token 生命周期过长且无撤销能力  
位置：[base.py](/home/caohui/projects/graduation-leave-system/backend/config/settings/base.py:140)、[serializers.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/serializers.py:39)  
access token 有效期 24 小时，响应只返回 access token，没有 refresh/logout/blacklist 机制。泄露后 24 小时内无法服务端撤销。对 dean/counselor 这类权限账号不合适。  
修复：生产 access token 缩短到 5-15 分钟；引入 refresh token rotation/blacklist 或明确无状态 JWT 风险接受；必要时增加 token version/jti denylist。

P1 - 错误响应契约不一致，前后端和 OpenAPI 易漂移  
位置：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:20)、[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:58)、[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:64)  
其他业务接口使用 `{'error': {'code', 'message', 'details'}}`，但登录失败返回 DRF serializer errors，demo-login 禁用返回 `{'error': 'Demo login is disabled'}`。这会让前端错误处理和 API schema 不稳定。  
修复：统一 auth 错误 envelope，例如 `DEMO_LOGIN_DISABLED`、`VALIDATION_ERROR`、`INVALID_CREDENTIALS`。

P1 - 当前 demo-web 与声称契约不一致  
位置：[api.js](/home/caohui/projects/graduation-leave-system/demo-web/js/api.js:7)、[index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:608)  
项目总结声称前端调用 `/api/auth/demo-login` 并只传 role，但当前代码仍读取 `user_id/password` 并调用 `/api/auth/login`。这不是后端三文件自身漏洞，但说明“开发完成/8 个测试通过”没有覆盖真实集成契约。  
修复：要么前端改为 role -> demo-login，要么撤销 demo-login 方案，继续普通登录；两者不能同时声称完成。

**结论**
当前不能认为生产就绪。阻塞项是：demo-login 生产 fail-fast 缺失、JWT/SECRET_KEY 生产基线缺失。8/8 自动化测试没有覆盖这些安全路径。

我执行了 `venv/bin/python manage.py check --deploy --settings=config.settings.prod`，结果有 8 个 warning，包括弱 SECRET_KEY、HTTPS redirect/cookie secure 未启用。建议先补生产安全测试，再谈发布。


OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019ea2ac-ad2b-7772-bb80-9266d3e9de91
--------
user
代码安全性和架构审计：

**审计文件：**
- backend/apps/users/views.py（demo-login端点实现）
- backend/apps/users/serializers.py（DemoLoginSerializer）
- backend/apps/users/urls.py（路由配置）

**审计重点：**
1. demo-login端点安全性：
   - DEMO_AUTH_ENABLED环境变量守卫是否足够？
   - 生产环境是否可能被误启用？
   - 是否有其他安全漏洞（认证绕过、token泄露）？

2. 认证机制：
   - JWT token生成和管理是否安全？
   - 会话管理是否有漏洞？
   - 密码处理是否安全（虽然是演示账号）？

3. 后端数据契约：
   - 序列化器是否完整？
   - 与前端期望是否一致？
   - 错误响应格式是否标准？

4. 生产环境风险：
   - 是否有阻塞生产部署的安全问题？
   - 需要哪些额外的安全加固？

**当前状态：**
- 8/8自动化测试通过
- 声称开发完成

请识别所有P0/P1安全和架构问题。
codex
我会按项目的审计协议先读取本地规则，然后只围绕这三个文件和相关认证配置做代码审查，重点找 P0/P1 风险并给出可落地的证据。
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
规则里要求所有 shell 命令经 `rtk`。我刚才先读规则时还没应用该前缀；后续命令会按项目要求统一使用 `rtk`。
codex
接下来我会读取三个目标文件、相关 settings/JWT 配置和现有测试。安全审计需要看调用链，不只看端点函数本身。
exec
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
 M .claude/skills/claude-codex-collab/SKILL.md
 M .omc/collaboration/events.jsonl
 M .omc/collaboration/state.json
 M .omc/project-memory.json
 M .omc/state/hud-stdin-cache.json
 D .omc/state/last-tool-error.json
 M .omc/state/mission-state.json
 D .omc/state/sessions/94aed496-0d75-412d-acc0-6f4d0f9e1c6e/session-started.json
 M .wolf/anatomy.md
 M .wolf/buglog.json
 M .wolf/cerebrum.md
 M .wolf/hooks/_session.json
 M .wolf/identity.md
 M .wolf/memory.md
 M .wolf/token-ledger.json
 M CLAUDE.md
 M backend/.omc/state/last-tool-error.json
 D backend/.omc/state/sessions/1975d66f-d9f9-404a-aee5-c702658630c2/session-started.json
 D backend/.omc/state/sessions/2d0f3e4b-af19-4432-9d9e-b2d773c8d64d/session-started.json
 D backend/.omc/state/sessions/f5a217eb-15dd-46c8-bdf3-d9e12d88125b/session-started.json
 M tests/.omc/state/last-tool-error.json
?? .omc/artifacts/ask/codex-demo-web-index-html-ui-docs-design-2026-05-27-system-design--2026-06-07T11-48-29-324Z.md
?? .omc/artifacts/ask/codex-demo-web-ui-omc-collaboration-tasks-task-20260607-demo-web-u-2026-06-07T12-00-48-030Z.md
?? .omc/artifacts/ask/codex-demo-web-ui-omc-collaboration-tasks-task-20260607-demo-web-v-2026-06-07T12-14-39-818Z.md
?? .omc/artifacts/ask/gemini-demo-web-ui-omc-collaboration-tasks-task-20260607-demo-web-u-2026-06-07T12-05-00-744Z.md
?? .omc/artifacts/final-testing-report-2026-06-07.md
?? .omc/artifacts/login-design-fix-summary-2026-06-07.md
?? .omc/collaboration/artifacts/20260607-claude-fix-complete-report.md
?? .omc/collaboration/artifacts/20260607-claude-p1-fix-status-report.md
?? .omc/collaboration/artifacts/20260607-claude-response-demo-web-ui-fix-review.md
?? .omc/collaboration/artifacts/20260607-claude-response-p0-fix-plan.md
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB-UI\344\274\230\345\214\226\344\270\216\347\224\237\344\272\247\345\260\261\347\273\252\350\257\204\344\274\260-1780837217-discuss-r0-claude-20260607-130017.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB-UI\344\274\230\345\214\226\344\270\216\347\224\237\344\272\247\345\260\261\347\273\252\350\257\204\344\274\260-1780837217-discuss-r1-codex-20260607-130207.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB-UI\344\274\230\345\214\226\344\270\216\347\224\237\344\272\247\345\260\261\347\273\252\350\257\204\344\274\260-1780837217-discuss-r1-gemini-20260607-130132.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB-UI\344\274\230\345\214\226\344\270\216\347\224\237\344\272\247\345\260\261\347\273\252\350\257\204\344\274\260-1780837217-discuss-r2-codex-20260607-130354.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB-UI\344\274\230\345\214\226\344\270\216\347\224\237\344\272\247\345\260\261\347\273\252\350\257\204\344\274\260-1780837217-discuss-r2-gemini-20260607-130246.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB-UI\344\274\230\345\214\226\344\270\216\347\224\237\344\272\247\345\260\261\347\273\252\350\257\204\344\274\260-1780837217-discuss-r3-codex-20260607-130603.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB-UI\344\274\230\345\214\226\344\270\216\347\224\237\344\272\247\345\260\261\347\273\252\350\257\204\344\274\260-1780837217-discuss-r4-codex-20260607-130755.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB-UI\344\274\230\345\214\226\344\270\216\347\224\237\344\272\247\345\260\261\347\273\252\350\257\204\344\274\260-1780837217-discuss-r4-gemini-20260607-130729.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB-UI\344\274\230\345\214\226\344\270\216\347\224\237\344\272\247\345\260\261\347\273\252\350\257\204\344\274\260-1780837217-discuss-r5-codex-20260607-131024.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\344\273\243\347\240\201\345\256\241\350\256\241-\351\252\214\350\257\2018\344\270\252\344\277\256\345\244\215\347\232\204\346\255\243\347\241\256\346\200\247-1780839567-discuss-r0-claude-20260607-133927.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\344\273\243\347\240\201\345\256\241\350\256\241-\351\252\214\350\257\2018\344\270\252\344\277\256\345\244\215\347\232\204\346\255\243\347\241\256\346\200\247-1780839567-discuss-r1-codex-20260607-134124.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\344\273\243\347\240\201\345\256\241\350\256\241-\351\252\214\350\257\2018\344\270\252\344\277\256\345\244\215\347\232\204\346\255\243\347\241\256\346\200\247-1780839567-discuss-r2-gemini-20260607-134211.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\344\273\243\347\240\201\345\256\241\350\256\241-\351\252\214\350\257\2018\344\270\252\344\277\256\345\244\215\347\232\204\346\255\243\347\241\256\346\200\247-1780839567-discuss-r3-codex-20260607-134635.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\344\273\243\347\240\201\345\256\241\350\256\241-\351\252\214\350\257\2018\344\270\252\344\277\256\345\244\215\347\232\204\346\255\243\347\241\256\346\200\247-1780839567-discuss-r3-gemini-20260607-134500.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\344\273\243\347\240\201\345\256\241\350\256\241-\351\252\214\350\257\2018\344\270\252\344\277\256\345\244\215\347\232\204\346\255\243\347\241\256\346\200\247-1780839567-discuss-r4-codex-20260607-134827.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\344\273\243\347\240\201\345\256\241\350\256\241-\351\252\214\350\257\2018\344\270\252\344\277\256\345\244\215\347\232\204\346\255\243\347\241\256\346\200\247-1780839567-discuss-r4-gemini-20260607-134712.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\344\273\243\347\240\201\345\256\241\350\256\241-\351\252\214\350\257\2018\344\270\252\344\277\256\345\244\215\347\232\204\346\255\243\347\241\256\346\200\247-1780839567-discuss-r5-codex-20260607-135002.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\344\273\243\347\240\201\345\256\241\350\256\241-\351\252\214\350\257\2018\344\270\252\344\277\256\345\244\215\347\232\204\346\255\243\347\241\256\346\200\247-1780839567-discuss-r5-gemini-20260607-134901.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\344\277\256\345\244\215\345\220\216\347\273\255\351\227\256\351\242\230-\345\275\223\345\211\215\344\273\243\347\240\201\347\212\266\346\200\201\344\270\216CODEX\345\256\241\346\237\245\345\267\256\345\274\202-1780836426-discuss-r0-claude-20260607-124706.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\344\277\256\345\244\215\345\220\216\347\273\255\351\227\256\351\242\230-\345\275\223\345\211\215\344\273\243\347\240\201\347\212\266\346\200\201\344\270\216CODEX\345\256\241\346\237\245\345\267\256\345\274\202-1780836426-discuss-r1-codex-20260607-124859.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\344\277\256\345\244\215\345\220\216\347\273\255\351\227\256\351\242\230-\345\275\223\345\211\215\344\273\243\347\240\201\347\212\266\346\200\201\344\270\216CODEX\345\256\241\346\237\245\345\267\256\345\274\202-1780836426-discuss-r2-codex-20260607-125158.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\344\277\256\345\244\215\345\220\216\347\273\255\351\227\256\351\242\230-\345\275\223\345\211\215\344\273\243\347\240\201\347\212\266\346\200\201\344\270\216CODEX\345\256\241\346\237\245\345\267\256\345\274\202-1780836426-discuss-r2-gemini-20260607-125051.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\344\277\256\345\244\215\345\220\216\347\273\255\351\227\256\351\242\230-\345\275\223\345\211\215\344\273\243\347\240\201\347\212\266\346\200\201\344\270\216CODEX\345\256\241\346\237\245\345\267\256\345\274\202-1780836426-discuss-r3-codex-20260607-125352.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\344\277\256\345\244\215\345\220\216\347\273\255\351\227\256\351\242\230-\345\275\223\345\211\215\344\273\243\347\240\201\347\212\266\346\200\201\344\270\216CODEX\345\256\241\346\237\245\345\267\256\345\274\202-1780836426-discuss-r3-gemini-20260607.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\347\231\273\345\275\225\350\256\276\350\256\241\347\274\272\351\231\267\344\277\256\345\244\215-\345\275\223\345\211\215\346\211\213\345\212\250\351\200\211\346\213\251\350\247\222\350\211\262\347\232\204\346\226\271\345\274\217\344\270\215\347\254\246\345\220\210\347\234\237\345\256\236\347\231\273\345\275\225\346\265\201\347\250\213-1780841849-discuss-r0-claude-20260607-141729.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\347\231\273\345\275\225\350\256\276\350\256\241\347\274\272\351\231\267\344\277\256\345\244\215-\345\275\223\345\211\215\346\211\213\345\212\250\351\200\211\346\213\251\350\247\222\350\211\262\347\232\204\346\226\271\345\274\217\344\270\215\347\254\246\345\220\210\347\234\237\345\256\236\347\231\273\345\275\225\346\265\201\347\250\213-1780841849-discuss-r1-codex-20260607-141908.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\347\231\273\345\275\225\350\256\276\350\256\241\347\274\272\351\231\267\344\277\256\345\244\215-\345\275\223\345\211\215\346\211\213\345\212\250\351\200\211\346\213\251\350\247\222\350\211\262\347\232\204\346\226\271\345\274\217\344\270\215\347\254\246\345\220\210\347\234\237\345\256\236\347\231\273\345\275\225\346\265\201\347\250\213-1780841849-discuss-r1-gemini-20260607-141855.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\347\231\273\345\275\225\350\256\276\350\256\241\347\274\272\351\231\267\344\277\256\345\244\215-\345\275\223\345\211\215\346\211\213\345\212\250\351\200\211\346\213\251\350\247\222\350\211\262\347\232\204\346\226\271\345\274\217\344\270\215\347\254\246\345\220\210\347\234\237\345\256\236\347\231\273\345\275\225\346\265\201\347\250\213-1780841849-discuss-r2-codex-20260607-142044.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\347\231\273\345\275\225\350\256\276\350\256\241\347\274\272\351\231\267\344\277\256\345\244\215-\345\275\223\345\211\215\346\211\213\345\212\250\351\200\211\346\213\251\350\247\222\350\211\262\347\232\204\346\226\271\345\274\217\344\270\215\347\254\246\345\220\210\347\234\237\345\256\236\347\231\273\345\275\225\346\265\201\347\250\213-1780841849-discuss-r2-gemini-20260607-142003.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\347\231\273\345\275\225\350\256\276\350\256\241\347\274\272\351\231\267\344\277\256\345\244\215-\345\275\223\345\211\215\346\211\213\345\212\250\351\200\211\346\213\251\350\247\222\350\211\262\347\232\204\346\226\271\345\274\217\344\270\215\347\254\246\345\220\210\347\234\237\345\256\236\347\231\273\345\275\225\346\265\201\347\250\213-1780841849-discuss-r3-codex-20260607-142254.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\347\231\273\345\275\225\350\256\276\350\256\241\347\274\272\351\231\267\344\277\256\345\244\215-\345\275\223\345\211\215\346\211\213\345\212\250\351\200\211\346\213\251\350\247\222\350\211\262\347\232\204\346\226\271\345\274\217\344\270\215\347\254\246\345\220\210\347\234\237\345\256\236\347\231\273\345\275\225\346\265\201\347\250\213-1780841849-discuss-r3-gemini-20260607-142200.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\350\256\244\350\257\201\346\226\271\346\241\210-\345\246\202\344\275\225\347\247\273\351\231\244TESTACCOUNTS\346\230\216\346\226\207\345\207\255\350\257\201-1780838572-discuss-r0-claude-20260607-132252.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\350\256\244\350\257\201\346\226\271\346\241\210-\345\246\202\344\275\225\347\247\273\351\231\244TESTACCOUNTS\346\230\216\346\226\207\345\207\255\350\257\201-1780838572-discuss-r1-codex-20260607-132446.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\350\256\244\350\257\201\346\226\271\346\241\210-\345\246\202\344\275\225\347\247\273\351\231\244TESTACCOUNTS\346\230\216\346\226\207\345\207\255\350\257\201-1780838572-discuss-r1-gemini-20260607-132524.md"
?? ".omc/collaboration/artifacts/DISCUSS-DEMO-WEB\350\256\244\350\257\201\346\226\271\346\241\210-\345\246\202\344\275\225\347\247\273\351\231\244TESTACCOUNTS\346\230\216\346\226\207\345\207\255\350\257\201-1780838572-discuss-r2-codex-20260607-132719.md"
?? ".omc/collaboration/artifacts/DISCUSS-\345\256\241\350\256\241\347\231\273\345\275\225\350\256\276\350\256\241\344\277\256\345\244\215\344\273\243\347\240\201-\351\252\214\350\257\201DEMO-WEB-1780842596-discuss-r0-claude-20260607-142956.md"
?? ".omc/collaboration/artifacts/DISCUSS-\345\256\241\350\256\241\347\231\273\345\275\225\350\256\276\350\256\241\344\277\256\345\244\215\344\273\243\347\240\201-\351\252\214\350\257\201DEMO-WEB-1780842596-discuss-r1-codex-20260607-143215.md"
?? ".omc/collaboration/artifacts/DISCUSS-\345\256\241\350\256\241\347\231\273\345\275\225\350\256\276\350\256\241\344\277\256\345\244\215\344\273\243\347\240\201-\351\252\214\350\257\201DEMO-WEB-1780842596-discuss-r1-gemini-20260607-143037.md"
?? ".omc/collaboration/artifacts/DISCUSS-\345\256\241\350\256\241\347\231\273\345\275\225\350\256\276\350\256\241\344\277\256\345\244\215\344\273\243\347\240\201-\351\252\214\350\257\201DEMO-WEB-1780842596-discuss-r2-codex-20260607-143353.md"
?? ".omc/collaboration/artifacts/DISCUSS-\345\256\241\350\256\241\347\231\273\345\275\225\350\256\276\350\256\241\344\277\256\345\244\215\344\273\243\347\240\201-\351\252\214\350\257\201DEMO-WEB-1780842596-discuss-r2-gemini-20260607-143255.md"
?? ".omc/collaboration/artifacts/DISCUSS-\345\256\241\350\256\241\347\231\273\345\275\225\350\256\276\350\256\241\344\277\256\345\244\215\344\273\243\347\240\201-\351\252\214\350\257\201DEMO-WEB-1780842596-discuss-r3-codex-20260607-143642.md"
?? ".omc/collaboration/artifacts/DISCUSS-\345\256\241\350\256\241\347\231\273\345\275\225\350\256\276\350\256\241\344\277\256\345\244\215\344\273\243\347\240\201-\351\252\214\350\257\201DEMO-WEB-1780842596-discuss-r3-gemini-20260607-143500.md"
?? ".omc/collaboration/artifacts/DISCUSS-\345\256\241\350\256\241\351\233\206\346\210\220\346\265\213\350\257\225\350\204\232\346\234\254\346\233\264\346\226\260-\351\252\214\350\257\201DEMO-WEB-1780844953-discuss-r0-claude-20260607-150913.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB-UI\344\274\230\345\214\226\344\270\216\347\224\237\344\272\247\345\260\261\347\273\252\350\257\204\344\274\260-1780837217-r1-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB-UI\344\274\230\345\214\226\344\270\216\347\224\237\344\272\247\345\260\261\347\273\252\350\257\204\344\274\260-1780837217-r2-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB-UI\344\274\230\345\214\226\344\270\216\347\224\237\344\272\247\345\260\261\347\273\252\350\257\204\344\274\260-1780837217-r3-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB-UI\344\274\230\345\214\226\344\270\216\347\224\237\344\272\247\345\260\261\347\273\252\350\257\204\344\274\260-1780837217-r4-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB-UI\344\274\230\345\214\226\344\270\216\347\224\237\344\272\247\345\260\261\347\273\252\350\257\204\344\274\260-1780837217-r5-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB\344\273\243\347\240\201\345\256\241\350\256\241-\351\252\214\350\257\2018\344\270\252\344\277\256\345\244\215\347\232\204\346\255\243\347\241\256\346\200\247-1780839567-r1-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB\344\273\243\347\240\201\345\256\241\350\256\241-\351\252\214\350\257\2018\344\270\252\344\277\256\345\244\215\347\232\204\346\255\243\347\241\256\346\200\247-1780839567-r2-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB\344\273\243\347\240\201\345\256\241\350\256\241-\351\252\214\350\257\2018\344\270\252\344\277\256\345\244\215\347\232\204\346\255\243\347\241\256\346\200\247-1780839567-r3-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB\344\273\243\347\240\201\345\256\241\350\256\241-\351\252\214\350\257\2018\344\270\252\344\277\256\345\244\215\347\232\204\346\255\243\347\241\256\346\200\247-1780839567-r4-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB\344\273\243\347\240\201\345\256\241\350\256\241-\351\252\214\350\257\2018\344\270\252\344\277\256\345\244\215\347\232\204\346\255\243\347\241\256\346\200\247-1780839567-r5-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB\344\277\256\345\244\215\345\220\216\347\273\255\351\227\256\351\242\230-\345\275\223\345\211\215\344\273\243\347\240\201\347\212\266\346\200\201\344\270\216CODEX\345\256\241\346\237\245\345\267\256\345\274\202-1780836426-r1-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB\344\277\256\345\244\215\345\220\216\347\273\255\351\227\256\351\242\230-\345\275\223\345\211\215\344\273\243\347\240\201\347\212\266\346\200\201\344\270\216CODEX\345\256\241\346\237\245\345\267\256\345\274\202-1780836426-r2-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB\344\277\256\345\244\215\345\220\216\347\273\255\351\227\256\351\242\230-\345\275\223\345\211\215\344\273\243\347\240\201\347\212\266\346\200\201\344\270\216CODEX\345\256\241\346\237\245\345\267\256\345\274\202-1780836426-r3-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB\347\231\273\345\275\225\350\256\276\350\256\241\347\274\272\351\231\267\344\277\256\345\244\215-\345\275\223\345\211\215\346\211\213\345\212\250\351\200\211\346\213\251\350\247\222\350\211\262\347\232\204\346\226\271\345\274\217\344\270\215\347\254\246\345\220\210\347\234\237\345\256\236\347\231\273\345\275\225\346\265\201\347\250\213-1780841849-r1-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB\347\231\273\345\275\225\350\256\276\350\256\241\347\274\272\351\231\267\344\277\256\345\244\215-\345\275\223\345\211\215\346\211\213\345\212\250\351\200\211\346\213\251\350\247\222\350\211\262\347\232\204\346\226\271\345\274\217\344\270\215\347\254\246\345\220\210\347\234\237\345\256\236\347\231\273\345\275\225\346\265\201\347\250\213-1780841849-r2-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB\347\231\273\345\275\225\350\256\276\350\256\241\347\274\272\351\231\267\344\277\256\345\244\215-\345\275\223\345\211\215\346\211\213\345\212\250\351\200\211\346\213\251\350\247\222\350\211\262\347\232\204\346\226\271\345\274\217\344\270\215\347\254\246\345\220\210\347\234\237\345\256\236\347\231\273\345\275\225\346\265\201\347\250\213-1780841849-r3-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB\350\256\244\350\257\201\346\226\271\346\241\210-\345\246\202\344\275\225\347\247\273\351\231\244TESTACCOUNTS\346\230\216\346\226\207\345\207\255\350\257\201-1780838572-r1-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB\350\256\244\350\257\201\346\226\271\346\241\210-\345\246\202\344\275\225\347\247\273\351\231\244TESTACCOUNTS\346\230\216\346\226\207\345\207\255\350\257\201-1780838572-r2-context.md"
?? ".omc/collaboration/context/DISCUSS-DEMO-WEB\350\256\244\350\257\201\346\226\271\346\241\210-\345\246\202\344\275\225\347\247\273\351\231\244TESTACCOUNTS\346\230\216\346\226\207\345\207\255\350\257\201-1780838572-r3-context.md"
?? ".omc/collaboration/context/DISCUSS-\345\256\241\350\256\241\347\231\273\345\275\225\350\256\276\350\256\241\344\277\256\345\244\215\344\273\243\347\240\201-\351\252\214\350\257\201DEMO-WEB-1780842596-r1-context.md"
?? ".omc/collaboration/context/DISCUSS-\345\256\241\350\256\241\347\231\273\345\275\225\350\256\276\350\256\241\344\277\256\345\244\215\344\273\243\347\240\201-\351\252\214\350\257\201DEMO-WEB-1780842596-r2-context.md"
?? ".omc/collaboration/context/DISCUSS-\345\256\241\350\256\241\347\231\273\345\275\225\350\256\276\350\256\241\344\277\256\345\244\215\344\273\243\347\240\201-\351\252\214\350\257\201DEMO-WEB-1780842596-r3-context.md"
?? ".omc/collaboration/context/DISCUSS-\345\256\241\350\256\241\351\233\206\346\210\220\346\265\213\350\257\225\350\204\232\346\234\254\346\233\264\346\226\260-\351\252\214\350\257\201DEMO-WEB-1780844953-r1-context.md"
?? ".omc/collaboration/state/DISCUSS-DEMO-WEB-UI\344\274\230\345\214\226\344\270\216\347\224\237\344\272\247\345\260\261\347\273\252\350\257\204\344\274\260-1780837217.json"
?? ".omc/collaboration/state/DISCUSS-DEMO-WEB\344\273\243\347\240\201\345\256\241\350\256\241-\351\252\214\350\257\2018\344\270\252\344\277\256\345\244\215\347\232\204\346\255\243\347\241\256\346\200\247-1780839567.json"
?? ".omc/collaboration/state/DISCUSS-DEMO-WEB\344\277\256\345\244\215\345\220\216\347\273\255\351\227\256\351\242\230-\345\275\223\345\211\215\344\273\243\347\240\201\347\212\266\346\200\201\344\270\216CODEX\345\256\241\346\237\245\345\267\256\345\274\202-1780836426.json"
?? ".omc/collaboration/state/DISCUSS-DEMO-WEB\347\231\273\345\275\225\350\256\276\350\256\241\347\274\272\351\231\267\344\277\256\345\244\215-\345\275\223\345\211\215\346\211\213\345\212\250\351\200\211\346\213\251\350\247\222\350\211\262\347\232\204\346\226\271\345\274\217\344\270\215\347\254\246\345\220\210\347\234\237\345\256\236\347\231\273\345\275\225\346\265\201\347\250\213-1780841849.json"
?? ".omc/collaboration/state/DISCUSS-DEMO-WEB\350\256\244\350\257\201\346\226\271\346\241\210-\345\246\202\344\275\225\347\247\273\351\231\244TESTACCOUNTS\346\230\216\346\226\207\345\207\255\350\257\201-1780838572.json"
?? ".omc/collaboration/state/DISCUSS-\345\256\241\350\256\241\347\231\273\345\275\225\350\256\276\350\256\241\344\277\256\345\244\215\344\273\243\347\240\201-\351\252\214\350\257\201DEMO-WEB-1780842596.json"
?? ".omc/collaboration/state/DISCUSS-\345\256\241\350\256\241\351\233\206\346\210\220\346\265\213\350\257\225\350\204\232\346\234\254\346\233\264\346\226\260-\351\252\214\350\257\201DEMO-WEB-1780844953.json"
?? .omc/collaboration/tasks/task-20260607-demo-web-validation.md
?? .omc/sessions/328d9a42-f2e5-452e-9255-3eabda324325.json
?? .omc/sessions/94aed496-0d75-412d-acc0-6f4d0f9e1c6e.json
?? .omc/state/agent-replay-a3a2658d-f0b7-4369-a779-8d2c41b2c4bf.jsonl
?? .omc/state/checkpoints/checkpoint-2026-06-07T11-27-25-848Z.json
?? .omc/state/checkpoints/checkpoint-2026-06-07T12-00-59-580Z.json
?? .omc/state/checkpoints/checkpoint-2026-06-07T12-45-42-951Z.json
?? .omc/state/checkpoints/checkpoint-2026-06-07T12-57-30-302Z.json
?? .omc/state/checkpoints/checkpoint-2026-06-07T13-32-56-721Z.json
?? .omc/state/checkpoints/checkpoint-2026-06-07T14-37-13-894Z.json
?? .omc/state/checkpoints/checkpoint-2026-06-07T14-37-23-069Z.json
?? .omc/state/checkpoints/checkpoint-2026-06-07T15-03-52-970Z.json
?? .omc/state/sessions/328d9a42-f2e5-452e-9255-3eabda324325/
?? .omc/state/sessions/9e78d64d-daa5-4814-8e83-8d5cf583c34a/
?? .omc/state/sessions/a3a2658d-f0b7-4369-a779-8d2c41b2c4bf/
?? backend/.omc/state/checkpoints/checkpoint-2026-06-07T14-05-18-375Z.json
?? backend/.omc/state/sessions/328d9a42-f2e5-452e-9255-3eabda324325/
?? demo-web/.omc/
?? replace_script.js
?? replace_script2.js
?? replace_script3.js
?? replace_script4.js
exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/users/serializers.py" in /home/caohui/projects/graduation-leave-system
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


class DemoLoginSerializer(serializers.Serializer):
    """演示登录（仅在DEMO_AUTH_ENABLED=true时启用）"""
    role = serializers.ChoiceField(choices=['student', 'dorm_manager', 'counselor', 'dean'])

    # 角色到演示用户映射
    DEMO_USERS = {
        'student': '2020001',
        'dorm_manager': 'M001',
        'counselor': 'T001',
        'dean': 'D001',
    }

    def validate(self, attrs):
        role = attrs.get('role')
        user_id = self.DEMO_USERS.get(role)

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError(f'Demo user for role {role} not found')

        if not user.active:
            raise serializers.ValidationError('Demo account is inactive')

        refresh = RefreshToken.for_user(user)

        return {
            'access_token': str(refresh.access_token),
            'token_type': 'Bearer',
            'user': AuthUserSerializer(user).data
        }

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/users/views.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
import os
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import LoginSerializer, LoginResponseSerializer, DemoLoginSerializer


@extend_schema(
    operation_id='auth_login',
    summary='用户登录',
    description='使用用户ID和密码登录，返回JWT access token',
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            response=LoginResponseSerializer,
            description='登录成功，返回access token和用户信息'
        ),
        400: OpenApiResponse(
            description='登录失败：DRF默认ValidationError格式（非项目envelope）'
        ),
    },
    tags=['认证']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    operation_id='auth_demo_login',
    summary='演示登录（仅开发/演示环境）',
    description='按角色快速登录演示账号。生产环境必须禁用（DEMO_AUTH_ENABLED=false）。',
    request=DemoLoginSerializer,
    responses={
        200: OpenApiResponse(
            response=LoginResponseSerializer,
            description='登录成功，返回access token和用户信息'
        ),
        403: OpenApiResponse(
            description='演示登录已禁用'
        ),
        400: OpenApiResponse(
            description='无效的角色或演示用户不存在'
        ),
    },
    tags=['认证']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def demo_login(request):
    # 生产环境守卫
    if os.environ.get('DEMO_AUTH_ENABLED', 'false').lower() != 'true':
        return Response({'error': 'Demo login is disabled'}, status=status.HTTP_403_FORBIDDEN)

    serializer = DemoLoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

exec
/bin/bash -lc "rtk sed -n '1,220p' backend/apps/users/urls.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('demo-login', views.demo_login, name='demo_login'),
]

codex
目标实现很短；主要风险会落在环境守卫是否和部署环境绑定、JWT 生命周期、以及响应契约是否和项目其他 API 一致。我现在补充检查配置和测试覆盖。
exec
/bin/bash -lc 'rtk rg -n "DEMO_AUTH_ENABLED|SIMPLE_JWT|JWT|ACCESS_TOKEN|REFRESH|AUTHENTICATION|DEFAULT_AUTHENTICATION|REST_FRAMEWORK|DEBUG|ALLOWED_HOSTS|ENV|DJANGO_ENV|SECRET_KEY" backend -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/config/settings/base.py:11:SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')
backend/config/settings/base.py:13:DEBUG = config('DEBUG', default=True, cast=bool)
backend/config/settings/base.py:15:ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])
backend/config/settings/base.py:113:REST_FRAMEWORK = {
backend/config/settings/base.py:114:    'DEFAULT_AUTHENTICATION_CLASSES': (
backend/config/settings/base.py:115:        'rest_framework_simplejwt.authentication.JWTAuthentication',
backend/config/settings/base.py:139:# JWT Settings
backend/config/settings/base.py:140:SIMPLE_JWT = {
backend/config/settings/base.py:141:    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
backend/config/settings/base.py:142:    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
backend/config/settings/base.py:143:    'ROTATE_REFRESH_TOKENS': False,
backend/config/settings/base.py:146:    'SIGNING_KEY': SECRET_KEY,
backend/config/settings/prod.py:4:DEBUG = False
backend/config/settings/dev.py:4:DEBUG = True
backend/config/settings/dev.py:6:ALLOWED_HOSTS = ['*']
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:24:REST_FRAMEWORK = {
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:25:    'DEFAULT_AUTHENTICATION_CLASSES': (...),
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:58:REST_FRAMEWORK = {
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:59:    'DEFAULT_AUTHENTICATION_CLASSES': (...),
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:101:- 位置：REST_FRAMEWORK字典内
backend/apps/users/serializers.py:50:    access_token = serializers.CharField(help_text="JWT access token")
backend/apps/users/serializers.py:56:    """演示登录（仅在DEMO_AUTH_ENABLED=true时启用）"""
backend/apps/users/views.py:13:    description='使用用户ID和密码登录，返回JWT access token',
backend/apps/users/views.py:38:    description='按角色快速登录演示账号。生产环境必须禁用（DEMO_AUTH_ENABLED=false）。',
backend/apps/users/views.py:58:    if os.environ.get('DEMO_AUTH_ENABLED', 'false').lower() != 'true':

exec
/bin/bash -lc 'rtk rg --files backend | rtk rg "(settings|urls|models|tests|permissions|auth|middleware|serializers|views)"' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/config/urls.py
backend/config/settings/dev.py
backend/apps/approvals/urls.py
backend/apps/approvals/tests/__init__.py
backend/apps/approvals/tests/test_rejection_flow.py
backend/apps/approvals/tests/test_list_permissions.py
backend/apps/approvals/tests/test_permissions.py
backend/apps/approvals/tests/test_state_machine.py
backend/apps/approvals/views.py
backend/apps/approvals/serializers.py
backend/apps/approvals/models.py
backend/config/settings/prod.py
backend/config/settings/test.py
backend/config/settings/base.py
backend/apps/applications/urls.py
backend/apps/attachments/urls.py
backend/apps/applications/tests/__init__.py
backend/apps/applications/tests/test_p0_fixes.py
backend/apps/applications/tests/test_error_cases.py
backend/apps/applications/tests/test_detail_permissions.py
backend/apps/applications/tests/test_serializer_validation.py
backend/apps/applications/tests/test_list_permissions.py
backend/apps/applications/tests/test_constraints.py
backend/apps/applications/tests/test_application_flow.py
backend/apps/applications/views.py
backend/apps/applications/permissions.py
backend/apps/applications/serializers.py
backend/apps/applications/models.py
backend/apps/attachments/tests/__init__.py
backend/apps/attachments/tests/test_list.py
backend/apps/attachments/tests/test_delete.py
backend/apps/attachments/tests/test_upload.py
backend/apps/attachments/tests/test_download.py
backend/apps/attachments/views.py
backend/apps/attachments/serializers.py
backend/apps/attachments/models.py
backend/apps/notifications/urls.py
backend/apps/notifications/tests/__init__.py
backend/apps/notifications/tests/test_auto_notifications_api.py
backend/apps/notifications/tests/test_timeout_warnings.py
backend/apps/notifications/tests/test_models.py
backend/apps/notifications/tests/test_api.py
backend/apps/notifications/tests/test_auto_notifications.py
backend/apps/notifications/views.py
backend/apps/notifications/serializers.py
backend/apps/notifications/models.py
backend/apps/users/tests/__init__.py
backend/apps/users/tests/test_xg_user_mapper.py
backend/apps/users/tests/test_xg_user_client.py
backend/apps/users/tests/test_xg_user_sync.py
backend/apps/users/tests/test_import_csv.py
backend/apps/users/views.py
backend/apps/users/serializers.py
backend/apps/users/models.py
backend/apps/users/urls.py
backend/config/settings/__init__.py

exec
/bin/bash -lc 'rtk rg -n "demo-login|demo_login|DemoLogin|DEMO_AUTH|auth_login|access_token|token_type|Invalid credentials|Account is inactive" -S .' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
./frontend/services/mock.ts:13:  access_token: 'mock_token_student',
./frontend/services/mock.ts:14:  token_type: 'Bearer',
./frontend/services/mock.ts:24:  access_token: 'mock_token_counselor',
./frontend/services/mock.ts:25:  token_type: 'Bearer',
./demo-web/js/api.js:20:            currentToken = data.access_token;
./demo-web/test-integration.sh:17:  | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
./demo-web/test-integration.sh:31:  | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
./demo-web/test-integration.sh:45:  | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
./demo-web/test-integration.sh:59:  | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
./frontend/types/api.ts:31:  access_token: string;
./frontend/types/api.ts:32:  token_type: 'Bearer';
./docs/PROJECT-SUMMARY.md:771:- ✓ 前端/小程序类型对齐：登录`token_type`、用户`class_id`、申请列表字段、分页去除`next/previous`
./docs/PROJECT-SUMMARY.md:2030:- 运行时返回{access_token, token_type, user}
./docs/PROJECT-SUMMARY.md:2034:  - 字段：access_token, token_type, user（AuthUserSerializer）
./docs/PROJECT-SUMMARY.md:4071:2. ✓ Blocking-2: TestAccounts明文凭证 - 移除前端密码，切换到后端demo-login端点
./docs/PROJECT-SUMMARY.md:4080:- apiLogin仅传递role到/api/auth/demo-login
./docs/PROJECT-SUMMARY.md:4081:- 后端按DEMO_AUTH_ENABLED控制演示登录
./docs/PROJECT-SUMMARY.md:4082:- 生产环境必须禁用demo-login（返回404/403）
./docs/PROJECT-SUMMARY.md:4123:1. ❌ **后端缺失demo-login端点** - 前端调用但后端未实现，认证流程完全中断
./docs/PROJECT-SUMMARY.md:4136:*Task #15: 实现demo-login端点*
./docs/PROJECT-SUMMARY.md:4137:- ✓ 后端新增POST /api/auth/demo-login
./docs/PROJECT-SUMMARY.md:4138:- ✓ DemoLoginSerializer接收role，返回对应演示用户token
./docs/PROJECT-SUMMARY.md:4139:- ✓ DEMO_AUTH_ENABLED环境变量守卫（生产环境=false）
./docs/PROJECT-SUMMARY.md:4152:- ✓ 认证流程已打通（demo-login端点实现）
./docs/design/2026-05-27-system-design.md:692:    "access_token": "eyJhbGc...",
./docs/design/2026-05-27-system-design.md:720:    "access_token": "eyJhbGc...",
./docs/design/2026-05-27-system-design.md:771:    "access_token": "eyJhbGc...",
./docs/design/2026-05-27-system-design.md:807:    "access_token": "eyJhbGc...",
./docs/design/2026-05-27-system-design.md:828:    "access_token": "eyJhbGc...",
./docs/design/2026-05-27-system-design.md:837:Authorization: Bearer {access_token}
./docs/design/2026-05-27-system-design.md:851:Authorization: Bearer {access_token}
./docs/design/2026-05-27-system-design.md:876:Authorization: Bearer {access_token}
./docs/design/2026-05-27-system-design.md:903:Authorization: Bearer {access_token}
./docs/design/2026-05-27-system-design.md:942:Authorization: Bearer {access_token}
./docs/design/2026-05-27-system-design.md:960:Authorization: Bearer {access_token}
./docs/design/2026-05-27-system-design.md:978:Authorization: Bearer {access_token}
./docs/design/2026-05-27-system-design.md:1002:Authorization: Bearer {access_token}
./docs/design/2026-05-27-system-design.md:1034:Authorization: Bearer {access_token}
./docs/design/2026-05-27-system-design.md:1067:Authorization: Bearer {access_token}
./docs/design/2026-05-27-system-design.md:1121:Authorization: Bearer {access_token}
./docs/design/2026-05-27-system-design.md:1129:Authorization: Bearer {access_token}
./docs/design/2026-05-27-system-design.md:1143:Authorization: Bearer {access_token}
./docs/design/2026-05-27-system-design.md:1166:Authorization: Bearer {access_token}
./docs/testing-guide.md:110:  -H "Authorization: Bearer <access_token>"
./docs/testing-guide.md:116:  -H "Authorization: Bearer <access_token>" \
./docs/testing-guide.md:145:  -H "Authorization: Bearer <access_token>"
./docs/SYSTEM-OPERATIONS-GUIDE.md:122:Authorization: Bearer <access_token>
./docs/SYSTEM-OPERATIONS-GUIDE.md:132:Authorization: Bearer <access_token>
./docs/SYSTEM-OPERATIONS-GUIDE.md:138:Authorization: Bearer <access_token>
./docs/SYSTEM-OPERATIONS-GUIDE.md:155:Authorization: Bearer <access_token>
./docs/SYSTEM-OPERATIONS-GUIDE.md:161:Authorization: Bearer <access_token>
./docs/SYSTEM-OPERATIONS-GUIDE.md:170:Authorization: Bearer <access_token>
./docs/SYSTEM-OPERATIONS-GUIDE.md:190:Authorization: Bearer <access_token>
./docs/SYSTEM-OPERATIONS-GUIDE.md:197:Authorization: Bearer <access_token>
./docs/SYSTEM-OPERATIONS-GUIDE.md:204:Authorization: Bearer <access_token>
./docs/SYSTEM-OPERATIONS-GUIDE.md:219:- **响应：** `{"access_token": "string", "refresh_token": "string", "user": {...}}`
./docs/SYSTEM-OPERATIONS-GUIDE.md:389:Authorization: Bearer <access_token>
./docs/API测试流程演示.md:34:    "access_token": "eyJhbGci...(JWT Token)",
./docs/API测试流程演示.md:35:    "token_type": "Bearer",
./docs/API测试流程演示.md:55:  -H "Authorization: Bearer {access_token}" \
./docs/API测试流程演示.md:85:  -H "Authorization: Bearer {access_token}"
./docs/API测试流程演示.md:125:    "access_token": "eyJhbGci...(JWT Token)",
./docs/API测试流程演示.md:126:    "token_type": "Bearer",
./docs/API测试流程演示.md:145:  -H "Authorization: Bearer {access_token}"
./docs/API测试流程演示.md:176:  -H "Authorization: Bearer {access_token}" \
./docs/API测试流程演示.md:210:    "access_token": "eyJhbGci...(JWT Token)",
./docs/API测试流程演示.md:211:    "token_type": "Bearer",
./docs/API测试流程演示.md:230:  -H "Authorization: Bearer {access_token}"
./docs/API测试流程演示.md:262:  -H "Authorization: Bearer {access_token}" \
./docs/API测试流程演示.md:289:  -H "Authorization: Bearer {access_token}"
./docs/API测试流程演示.md:340:  -H "Authorization: Bearer {access_token}" \
./docs/contracts/contract-v0.2.md:158:  "access_token": "<jwt>",
./docs/contracts/contract-v0.2.md:159:  "token_type": "Bearer",
./docs/contracts/contract-v0.1.md:214:  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
./docs/contracts/contract-v0.1.md:215:  "token_type": "Bearer",
./docs/contracts/contract-v0.1.md:600:      access_token: 'mock_token',
./docs/contracts/contract-v0.1.md:601:      token_type: 'Bearer',
./docs/contracts/contract-v0.1.md:630:    token = response.json()['access_token']
./docs/api/notification-contract-v0.1.md:160:Authorization: Bearer {access_token}
./docs/api/notification-contract-v0.1.md:201:Authorization: Bearer {access_token}
./docs/api/notification-contract-v0.1.md:222:Authorization: Bearer {access_token}
./docs/api/notification-contract-v0.1.md:254:Authorization: Bearer {access_token}
./docs/api/api-schema-todo.md:68:- 修复auth_login的200响应schema不匹配问题
./docs/api/api-schema-todo.md:69:- 原问题：@extend_schema使用LoginSerializer（字段：user_id, password），但运行时返回{access_token, token_type, user}
./tests/multi_role_test.py:45:        token = login_resp.json()["access_token"]
./docs/acceptance/phase4c-demo-script.md:102:  | jq -r '.access_token')
./docs/acceptance/phase4c-demo-script.md:192:  | jq -r '.access_token')
./docs/acceptance/phase4c-demo-script.md:240:  | jq -r '.access_token')
./docs/acceptance/phase4c-demo-script.md:286:  | jq -r '.access_token')
./docs/acceptance/phase4c-demo-script.md:364:  | jq -r '.access_token')
./docs/acceptance/phase4c-demo-script.md:393:  | jq -r '.access_token')
./docs/acceptance/phase4c-demo-script.md:409:  | jq -r '.access_token')
./docs/acceptance/phase4c-demo-script.md:430:  | jq -r '.access_token')
./tests/test_p0_fixes.sh:18:  -d '{"user_id":"2020001","password":"2020001"}' | jq -r '.access_token')
./tests/test_p0_fixes.sh:40:  -d '{"user_id":"T001","password":"T001"}' | jq -r '.access_token')
./tests/smoke_test.sh:53:  | jq -r '.access_token')
./tests/smoke_test.sh:100:  | jq -r '.access_token')
./tests/smoke_test.sh:226:  | jq -r '.access_token')
./tests/smoke_test.sh:329:  | jq -r '.access_token')
./tests/smoke_test.sh:360:  | jq -r '.access_token')
./tests/smoke_test.sh:399:  | jq -r '.access_token')
./tests/test_multi_dorm_manager.sh:16:  | jq -r '.access_token')
./tests/test_multi_dorm_manager.sh:62:  | jq -r '.access_token')
./tests/test_multi_dorm_manager.sh:84:  | jq -r '.access_token')
./tests/api_data_samples.sh:21:  | jq -r '.access_token')
./tests/api_data_samples.sh:65:  | jq -r '.access_token')
./tests/approval_workflow_test.py:54:        return resp.json()["access_token"]
./tests/full_workflow_test.py:42:        token = login_resp.json()["access_token"]
./miniprogram/types/api.ts:31:  access_token: string;
./miniprogram/types/api.ts:32:  token_type: 'Bearer';
./miniprogram/pages/login/login.ts:35:      wx.setStorageSync('token', res.access_token);
./miniprogram/pages/login/login.ts:37:      app.globalData.token = res.access_token;
./docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:31:The plan describes `/api/auth/login/` and a token response containing a refresh token. The current route is `path('login', ...)`, so the canonical route is `/api/auth/login` without a trailing slash. The current login serializer returns `access_token`, `token_type`, and `user`; it does not return `refresh_token`.
./docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:32:- 实际运行时返回：`{'access_token': ..., 'token_type': 'Bearer', 'user': {...}}`
./docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:36:- `access_token: str`
./docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:37:- `token_type: str`（default='Bearer'）
./backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:97:### 问题1: KeyError: 'access_token'
./docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:16:另外，静态检查已经发现一个P1级schema fidelity风险：`backend/apps/users/views.py` 的登录成功响应使用 `LoginSerializer` 作为200响应schema，但运行时返回的是 `access_token`、`token_type`、`user`，不是 `LoginSerializer` 声明的 `user_id`/`password` 字段形状。这个问题属于P1准确性，不应推迟到P2示例阶段。
./docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:94:  - `access_token`
./docs/discussions/phase4c-next-steps/56-codex-post-api-schema-p1-next-strategy-response.md:95:  - `token_type`
./docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:283:2. token字段改为access_token
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:194:- ✓ 解析access_token
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:221:- access_token字段
./docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:359:- 修复：端口8001、access_token、UUID ID、URL斜杠
./docs/discussions/phase4c-next-steps/58-claude-codex-consensus-option-a-prime-partial.md:27:- 运行时：返回`{access_token, token_type, user}`
./docs/discussions/phase4c-next-steps/58-claude-codex-consensus-option-a-prime-partial.md:31:   - 字段：access_token, token_type, user（AuthUserSerializer）
./docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:101:- 修复：端口8001、access_token、UUID ID、URL斜杠
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:68:**问题：** 文档用`token`、数字ID、端口8000；实际是`access_token`、`app_xxx/apv_xxx`、端口8001  
./docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:117:5. **写真实smoke脚本**：动态读取`access_token`、`application_id`、`approval_id`，不要写死`1/2`
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:61:| 认证 | login_id、role、access_token mock/JWT格式 | 微信OAuth |
./backend/apps/applications/tests/test_error_cases.py:90:        token = response.data['access_token']
./backend/apps/applications/tests/test_error_cases.py:107:        token = response.data['access_token']
./backend/apps/applications/tests/test_error_cases.py:135:        token1 = response.data['access_token']
./backend/apps/applications/tests/test_error_cases.py:151:        token2 = response.data['access_token']
./backend/apps/applications/tests/test_error_cases.py:164:        token = response.data['access_token']
./backend/apps/applications/tests/test_error_cases.py:177:        token = response.data['access_token']
./backend/apps/approvals/tests/test_rejection_flow.py:60:        student_token = response.data['access_token']
./backend/apps/approvals/tests/test_rejection_flow.py:76:        dorm_manager_token = response.data['access_token']
./backend/apps/approvals/tests/test_rejection_flow.py:94:        dorm_manager_token = response.data['access_token']
./backend/apps/approvals/tests/test_rejection_flow.py:120:        counselor_token = response.data['access_token']
./backend/apps/applications/tests/test_application_flow.py:71:        student_token = response.data['access_token']
./backend/apps/applications/tests/test_application_flow.py:89:        dorm_manager_token = response.data['access_token']
./backend/apps/applications/tests/test_application_flow.py:110:        counselor_token = response.data['access_token']
./docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:143:- 修复：端口8001、access_token字段、UUID格式ID、URL斜杠
./docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:57:- 修复：端口8001、access_token字段、UUID格式ID、URL斜杠
./backend/apps/users/serializers.py:31:            raise serializers.ValidationError('Invalid credentials')
./backend/apps/users/serializers.py:34:            raise serializers.ValidationError('Invalid credentials')
./backend/apps/users/serializers.py:37:            raise serializers.ValidationError('Account is inactive')
./backend/apps/users/serializers.py:42:            'access_token': str(refresh.access_token),
./backend/apps/users/serializers.py:43:            'token_type': 'Bearer',
./backend/apps/users/serializers.py:50:    access_token = serializers.CharField(help_text="JWT access token")
./backend/apps/users/serializers.py:51:    token_type = serializers.CharField(default='Bearer', help_text="Token type")
./backend/apps/users/serializers.py:55:class DemoLoginSerializer(serializers.Serializer):
./backend/apps/users/serializers.py:56:    """演示登录（仅在DEMO_AUTH_ENABLED=true时启用）"""
./backend/apps/users/serializers.py:82:            'access_token': str(refresh.access_token),
./backend/apps/users/serializers.py:83:            'token_type': 'Bearer',
./docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:105:- 解析`access_token`，不要假设`token`字段。
./backend/apps/users/views.py:7:from .serializers import LoginSerializer, LoginResponseSerializer, DemoLoginSerializer
./backend/apps/users/views.py:11:    operation_id='auth_login',
./backend/apps/users/views.py:36:    operation_id='auth_demo_login',
./backend/apps/users/views.py:38:    description='按角色快速登录演示账号。生产环境必须禁用（DEMO_AUTH_ENABLED=false）。',
./backend/apps/users/views.py:39:    request=DemoLoginSerializer,
./backend/apps/users/views.py:56:def demo_login(request):
./backend/apps/users/views.py:58:    if os.environ.get('DEMO_AUTH_ENABLED', 'false').lower() != 'true':
./backend/apps/users/views.py:61:    serializer = DemoLoginSerializer(data=request.data)
./backend/apps/users/urls.py:6:    path('demo-login', views.demo_login, name='demo_login'),

codex
初步看到 demo-login 默认关闭，但它只受一个独立环境变量控制，没有和生产 settings 形成硬绑定。我要看 `prod.py`、JWT 配置和用户模型，确认这是不是阻塞生产的安全问题。
exec
/bin/bash -lc "rtk nl -ba backend/apps/users/models.py | rtk sed -n '1,240p'" in /home/caohui/projects/graduation-leave-system
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
    10	    ADMIN = 'admin', '学工管理员'
    11	
    12	
    13	class UserManager(BaseUserManager):
    14	    def create_user(self, user_id, password=None, **extra_fields):
    15	        if not user_id:
    16	            raise ValueError('user_id is required')
    17	        user = self.model(user_id=user_id, **extra_fields)
    18	        user.set_password(password)
    19	        user.save(using=self._db)
    20	        return user
    21	
    22	    def create_superuser(self, user_id, password=None, **extra_fields):
    23	        extra_fields.setdefault('is_staff', True)
    24	        extra_fields.setdefault('is_superuser', True)
    25	        extra_fields.setdefault('active', True)
    26	        return self.create_user(user_id, password, **extra_fields)
    27	
    28	
    29	class User(AbstractBaseUser, PermissionsMixin):
    30	    user_id = models.CharField(max_length=50, unique=True, primary_key=True)
    31	    name = models.CharField(max_length=100)
    32	    role = models.CharField(max_length=20, choices=UserRole.choices)
    33	    active = models.BooleanField(default=True)
    34	    class_id = models.CharField(max_length=50, null=True, blank=True)
    35	    is_graduating = models.BooleanField(null=True, blank=True)
    36	    graduation_year = models.IntegerField(null=True, blank=True)
    37	
    38	    # API补充字段（学工系统）
    39	    phone = models.CharField(max_length=20, null=True, blank=True)
    40	    email = models.EmailField(null=True, blank=True)
    41	    department = models.CharField(max_length=100, null=True, blank=True)
    42	    building = models.CharField(max_length=100, null=True, blank=True)
    43	
    44	    is_staff = models.BooleanField(default=False)
    45	    created_at = models.DateTimeField(auto_now_add=True)
    46	    updated_at = models.DateTimeField(auto_now=True)
    47	
    48	    objects = UserManager()
    49	
    50	    USERNAME_FIELD = 'user_id'
    51	    REQUIRED_FIELDS = ['name', 'role']
    52	
    53	    class Meta:
    54	        db_table = 'users'
    55	
    56	    def __str__(self):
    57	        return f"{self.user_id} - {self.name}"

exec
/bin/bash -lc "rtk nl -ba backend/config/settings/dev.py | rtk sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	"""Development settings."""
     2	from .base import *
     3	
     4	DEBUG = True
     5	
     6	ALLOWED_HOSTS = ['*']
     7	
     8	# Console email backend for development
     9	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    10	
    11	# Disable CORS restrictions in development
    12	CORS_ALLOW_ALL_ORIGINS = True

exec
/bin/bash -lc "rtk nl -ba backend/config/settings/test.py | rtk sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	"""Test settings - use SQLite instead of PostgreSQL"""
     2	from .base import *
     3	import tempfile
     4	
     5	# Use SQLite for testing (no PostgreSQL client libraries required)
     6	DATABASES = {
     7	    'default': {
     8	        'ENGINE': 'django.db.backends.sqlite3',
     9	        'NAME': BASE_DIR / 'test_db.sqlite3',
    10	    }
    11	}
    12	
    13	# Speed up tests
    14	PASSWORD_HASHERS = [
    15	    'django.contrib.auth.hashers.MD5PasswordHasher',
    16	]
    17	
    18	MEDIA_ROOT = tempfile.mkdtemp(prefix='graduation_leave_test_media_')

exec
/bin/bash -lc "rtk nl -ba backend/config/settings/base.py | rtk sed -n '1,210p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	"""
     2	Django settings for graduation leave system project.
     3	Base settings shared across all environments.
     4	"""
     5	from pathlib import Path
     6	from decouple import config
     7	from datetime import timedelta
     8	
     9	BASE_DIR = Path(__file__).resolve().parent.parent.parent
    10	
    11	SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')
    12	
    13	DEBUG = config('DEBUG', default=True, cast=bool)
    14	
    15	ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])
    16	
    17	# Application definition
    18	INSTALLED_APPS = [
    19	    'django.contrib.admin',
    20	    'django.contrib.auth',
    21	    'django.contrib.contenttypes',
    22	    'django.contrib.sessions',
    23	    'django.contrib.messages',
    24	    'django.contrib.staticfiles',
    25	
    26	    # Third party
    27	    'rest_framework',
    28	    'rest_framework_simplejwt',
    29	    'corsheaders',
    30	    'django_filters',
    31	    'drf_spectacular',
    32	
    33	    # Local apps
    34	    'apps.users',
    35	    'apps.applications',
    36	    'apps.approvals',
    37	    'apps.attachments',
    38	    'apps.notifications',
    39	]
    40	
    41	MIDDLEWARE = [
    42	    'django.middleware.security.SecurityMiddleware',
    43	    'corsheaders.middleware.CorsMiddleware',
    44	    'django.contrib.sessions.middleware.SessionMiddleware',
    45	    'django.middleware.common.CommonMiddleware',
    46	    'django.middleware.csrf.CsrfViewMiddleware',
    47	    'django.contrib.auth.middleware.AuthenticationMiddleware',
    48	    'django.contrib.messages.middleware.MessageMiddleware',
    49	    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    50	]
    51	
    52	ROOT_URLCONF = 'config.urls'
    53	
    54	TEMPLATES = [
    55	    {
    56	        'BACKEND': 'django.template.backends.django.DjangoTemplates',
    57	        'DIRS': [],
    58	        'APP_DIRS': True,
    59	        'OPTIONS': {
    60	            'context_processors': [
    61	                'django.template.context_processors.debug',
    62	                'django.template.context_processors.request',
    63	                'django.contrib.auth.context_processors.auth',
    64	                'django.contrib.messages.context_processors.messages',
    65	            ],
    66	        },
    67	    },
    68	]
    69	
    70	WSGI_APPLICATION = 'config.wsgi.application'
    71	
    72	# Database
    73	DATABASES = {
    74	    'default': {
    75	        'ENGINE': 'django.db.backends.postgresql',
    76	        'NAME': config('DB_NAME', default='graduation_leave'),
    77	        'USER': config('DB_USER', default='postgres'),
    78	        'PASSWORD': config('DB_PASSWORD', default='postgres'),
    79	        'HOST': config('DB_HOST', default='localhost'),
    80	        'PORT': config('DB_PORT', default='5432'),
    81	    }
    82	}
    83	
    84	# Custom user model
    85	AUTH_USER_MODEL = 'users.User'
    86	
    87	# Password validation
    88	AUTH_PASSWORD_VALIDATORS = [
    89	    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    90	    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    91	    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    92	    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    93	]
    94	
    95	# Internationalization
    96	LANGUAGE_CODE = 'zh-hans'
    97	TIME_ZONE = 'Asia/Shanghai'
    98	USE_I18N = True
    99	USE_TZ = True
   100	
   101	# Static files
   102	STATIC_URL = 'static/'
   103	STATIC_ROOT = BASE_DIR / 'staticfiles'
   104	
   105	# Media files
   106	MEDIA_URL = '/media/'
   107	MEDIA_ROOT = BASE_DIR / 'media'
   108	
   109	# Default primary key field type
   110	DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
   111	
   112	# REST Framework
   113	REST_FRAMEWORK = {
   114	    'DEFAULT_AUTHENTICATION_CLASSES': (
   115	        'rest_framework_simplejwt.authentication.JWTAuthentication',
   116	    ),
   117	    'DEFAULT_PERMISSION_CLASSES': (
   118	        'rest_framework.permissions.IsAuthenticated',
   119	    ),
   120	    'DEFAULT_RENDERER_CLASSES': (
   121	        'rest_framework.renderers.JSONRenderer',
   122	    ),
   123	    'DEFAULT_PARSER_CLASSES': (
   124	        'rest_framework.parsers.JSONParser',
   125	    ),
   126	    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
   127	    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
   128	}
   129	
   130	# API Documentation
   131	SPECTACULAR_SETTINGS = {
   132	    'TITLE': '毕业生离校申请审批系统 API',
   133	    'DESCRIPTION': '毕业生离校申请审批系统后端API文档',
   134	    'VERSION': '1.0.0',
   135	    'SERVE_INCLUDE_SCHEMA': False,
   136	    'COMPONENT_SPLIT_REQUEST': True,
   137	}
   138	
   139	# JWT Settings
   140	SIMPLE_JWT = {
   141	    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
   142	    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
   143	    'ROTATE_REFRESH_TOKENS': False,
   144	    'BLACKLIST_AFTER_ROTATION': False,
   145	    'ALGORITHM': 'HS256',
   146	    'SIGNING_KEY': SECRET_KEY,
   147	    'AUTH_HEADER_TYPES': ('Bearer',),
   148	    'USER_ID_FIELD': 'user_id',
   149	    'USER_ID_CLAIM': 'user_id',
   150	}
   151	
   152	# CORS Settings
   153	CORS_ALLOWED_ORIGINS = config(
   154	    'CORS_ALLOWED_ORIGINS',
   155	    default='http://localhost:3000,http://127.0.0.1:3000',
   156	    cast=lambda v: [s.strip() for s in v.split(',')]
   157	)
   158	
   159	# Fallback dorm manager for students without building assignment
   160	FALLBACK_DORM_MANAGER_USER_ID = '92008149'

exec
/bin/bash -lc "rtk nl -ba backend/config/settings/prod.py | rtk sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	"""Production settings."""
     2	from .base import *
     3	
     4	DEBUG = False
     5	
     6	# Security settings
     7	SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
     8	SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
     9	CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)

exec
/bin/bash -lc "rtk nl -ba backend/config/urls.py | rtk sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	"""URL Configuration"""
     2	from django.contrib import admin
     3	from django.urls import path, include
     4	from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
     5	
     6	urlpatterns = [
     7	    path('admin/', admin.site.urls),
     8	    path('api/auth/', include('apps.users.urls')),
     9	    path('api/', include('apps.attachments.urls')),
    10	    path('api/applications/', include('apps.applications.urls')),
    11	    path('api/approvals/', include('apps.approvals.urls')),
    12	    path('api/notifications/', include('apps.notifications.urls')),
    13	
    14	    # API Documentation
    15	    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    16	    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    17	]

codex
配置层面确认了几个需要严肃处理的点：生产 settings 没有强制禁止 demo auth，JWT access token 是 24 小时，且签名默认值可用。现在我再查演示账号数据来源和测试是否覆盖“生产误启用”。
exec
/bin/bash -lc 'rtk rg -n "class .*Login|demo-login|DEMO_AUTH_ENABLED|auth/demo-login|auth/login" backend/apps/users/tests backend/apps/*/tests tests demo-web -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
tests/multi_role_test.py:35:        login_resp = requests.post(f"{BASE_URL}/api/auth/login", json={
tests/test_p0_fixes.sh:16:TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/test_p0_fixes.sh:38:COUNSELOR_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/smoke_test.sh:50:STUDENT_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/smoke_test.sh:97:M001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/smoke_test.sh:223:T001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/smoke_test.sh:326:STUDENT2_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/smoke_test.sh:357:M002_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/smoke_test.sh:396:T002_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
demo-web/js/api.js:9:        const response = await fetch(API_BASE_URL + '/auth/login', {
demo-web/test-integration.sh:14:STUDENT_TOKEN=$(curl -s -X POST "$API_BASE/auth/login" \
demo-web/test-integration.sh:28:DM_TOKEN=$(curl -s -X POST "$API_BASE/auth/login" \
demo-web/test-integration.sh:42:COUNSELOR_TOKEN=$(curl -s -X POST "$API_BASE/auth/login" \
demo-web/test-integration.sh:56:ADMIN_TOKEN=$(curl -s -X POST "$API_BASE/auth/login" \
tests/test_multi_dorm_manager.sh:13:STUDENT_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/test_multi_dorm_manager.sh:59:M001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/test_multi_dorm_manager.sh:81:M003_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/api_data_samples.sh:18:STUDENT_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/api_data_samples.sh:62:COUNSELOR_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/approval_workflow_test.py:49:    resp = requests.post(f"{BASE_URL}/api/auth/login", json={
backend/apps/applications/tests/test_error_cases.py:86:        response = self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:103:        response = self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:131:        response = self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:147:        response = self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:160:        response = self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:173:        response = self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_application_flow.py:66:        response = self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_application_flow.py:85:        response = self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_application_flow.py:106:        response = self.client.post('/api/auth/login', {
backend/apps/approvals/tests/test_rejection_flow.py:56:        response = self.client.post('/api/auth/login', {
backend/apps/approvals/tests/test_rejection_flow.py:72:        response = self.client.post('/api/auth/login', {
backend/apps/approvals/tests/test_rejection_flow.py:90:        response = self.client.post('/api/auth/login', {
backend/apps/approvals/tests/test_rejection_flow.py:116:        response = self.client.post('/api/auth/login', {
tests/full_workflow_test.py:32:        login_resp = requests.post(f"{BASE_URL}/api/auth/login", json={

exec
/bin/bash -lc "rtk rg -n \"success|code|message|error|detail|exception|custom_exception|EXCEPTION_HANDLER|Response\\(|ValidationError\" backend/apps backend/config -S" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/config/settings/base.py:23:    'django.contrib.messages',
backend/config/settings/base.py:48:    'django.contrib.messages.middleware.MessageMiddleware',
backend/config/settings/base.py:64:                'django.contrib.messages.context_processors.messages',
backend/apps/approvals/pagination.py:11:        return Response({
backend/apps/approvals/tests/test_rejection_flow.py:68:        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
backend/apps/approvals/tests/test_rejection_flow.py:84:        self.assertEqual(response.status_code, status.HTTP_200_OK)
backend/apps/approvals/tests/test_rejection_flow.py:103:        self.assertEqual(response.status_code, status.HTTP_200_OK)
backend/apps/approvals/tests/test_rejection_flow.py:129:        self.assertEqual(response.status_code, status.HTTP_200_OK)
backend/apps/approvals/tests/test_list_permissions.py:74:        self.assertEqual(response.status_code, 403)
backend/apps/approvals/tests/test_list_permissions.py:75:        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
backend/apps/approvals/tests/test_list_permissions.py:80:        self.assertEqual(response.status_code, 200)
backend/apps/approvals/tests/test_list_permissions.py:92:        self.assertEqual(response.status_code, 200)
backend/apps/approvals/tests/test_list_permissions.py:104:        self.assertEqual(response.status_code, 200)
backend/apps/approvals/tests/test_list_permissions.py:157:        self.assertEqual(response.status_code, 200)
backend/apps/approvals/tests/test_permissions.py:142:        self.assertEqual(approve_response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/approvals/tests/test_permissions.py:143:        self.assertEqual(reject_response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/approvals/tests/test_permissions.py:155:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/approvals/tests/test_permissions.py:168:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/approvals/tests/test_permissions.py:181:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/approvals/tests/test_permissions.py:192:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/approvals/tests/test_permissions.py:203:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/approvals/tests/test_state_machine.py:92:        self.assertEqual(response1.status_code, status.HTTP_200_OK)
backend/apps/approvals/tests/test_state_machine.py:100:        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/tests/test_state_machine.py:111:        self.assertEqual(response1.status_code, status.HTTP_200_OK)
backend/apps/approvals/tests/test_state_machine.py:118:        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/tests/test_state_machine.py:137:        self.assertEqual(approve_response.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/tests/test_state_machine.py:138:        self.assertEqual(reject_response.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/tests/test_state_machine.py:165:        self.assertEqual(approve_response.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/tests/test_state_machine.py:166:        self.assertEqual(reject_response.status_code, status.HTTP_409_CONFLICT)
backend/apps/approvals/views.py:42:        return Response(
backend/apps/approvals/views.py:43:            {'error': {'code': 'FORBIDDEN', 'message': '学生不能访问审批列表'}},
backend/apps/approvals/views.py:66:        return Response(
backend/apps/approvals/views.py:67:            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
backend/apps/approvals/views.py:106:        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
backend/apps/approvals/views.py:113:        return Response(ApprovalSerializer(approval).data)
backend/apps/approvals/views.py:115:    return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
backend/apps/approvals/views.py:140:        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
backend/apps/approvals/views.py:145:        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
backend/apps/approvals/views.py:148:        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
backend/apps/approvals/views.py:151:        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
backend/apps/approvals/views.py:155:        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
backend/apps/approvals/views.py:159:        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
backend/apps/approvals/views.py:163:        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
backend/apps/approvals/views.py:168:        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败'}},
backend/apps/approvals/views.py:206:            return Response({'error': {'code': 'CONFLICT', 'message': '辅导员审批已存在，不能重复创建'}},
backend/apps/approvals/views.py:232:            return Response({'error': {'code': 'NOT_FOUND', 'message': '该学院辅导员不存在',
backend/apps/approvals/views.py:233:                                        'details': {'department': application.student.department}}},
backend/apps/approvals/views.py:249:    return Response(ApprovalSerializer(approval).data)
backend/apps/approvals/views.py:273:        return Response({'error': {'code': 'NOT_FOUND', 'message': '审批记录不存在'}},
backend/apps/approvals/views.py:278:        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
backend/apps/approvals/views.py:281:        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
backend/apps/approvals/views.py:284:        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
backend/apps/approvals/views.py:288:        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限执行此操作'}},
backend/apps/approvals/views.py:292:        return Response({'error': {'code': 'CONFLICT', 'message': '审批已完成，不能重复操作'}},
backend/apps/approvals/views.py:296:        return Response({'error': {'code': 'CONFLICT', 'message': '申请状态与审批步骤不匹配'}},
backend/apps/approvals/views.py:301:        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败'}},
backend/apps/approvals/views.py:315:    return Response(ApprovalSerializer(approval).data)
backend/apps/approvals/serializers.py:26:    """Full approval detail with nested application info"""
backend/apps/applications/providers.py:12:    provider_error_code: Optional[str]
backend/apps/applications/providers.py:23:                provider_error_code=None
backend/apps/applications/providers.py:30:                provider_error_code=None
backend/apps/applications/providers.py:37:                provider_error_code=None
backend/apps/applications/providers.py:44:                provider_error_code=None
backend/apps/applications/providers.py:51:                provider_error_code="STUDENT_NOT_FOUND"
backend/apps/applications/providers.py:58:                provider_error_code=None
backend/apps/applications/providers.py:65:                provider_error_code=None
backend/apps/applications/providers.py:72:                provider_error_code=None
backend/apps/applications/providers.py:79:                provider_error_code=None
backend/apps/applications/providers.py:86:                provider_error_code=None
backend/apps/applications/providers.py:93:                provider_error_code=None
backend/apps/applications/providers.py:100:                provider_error_code=None
backend/apps/applications/providers.py:109:            provider_error_code=None
backend/apps/applications/pagination.py:11:        return Response({
backend/apps/applications/serializers.py:44:            raise serializers.ValidationError('离校日期不能早于今天')
backend/apps/applications/tests/test_p0_fixes.py:79:        # Should raise validation error
backend/apps/applications/models.py:2:from django.core.exceptions import ValidationError
backend/apps/applications/models.py:49:                raise ValidationError('该学生已有待审批或已通过的申请，不能重复提交')
backend/apps/applications/tests/test_error_cases.py:84:    def test_dorm_blocked_error(self):
backend/apps/applications/tests/test_error_cases.py:98:        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
backend/apps/applications/tests/test_error_cases.py:99:        self.assertEqual(response.data['error']['code'], 'DORM_BLOCKED')
backend/apps/applications/tests/test_error_cases.py:117:        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
backend/apps/applications/tests/test_error_cases.py:125:        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
backend/apps/applications/tests/test_error_cases.py:126:        self.assertEqual(response.data['error']['code'], 'CONFLICT')
backend/apps/applications/tests/test_error_cases.py:143:        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
backend/apps/applications/tests/test_error_cases.py:155:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/applications/tests/test_error_cases.py:156:        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
backend/apps/applications/tests/test_error_cases.py:168:        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
backend/apps/applications/tests/test_error_cases.py:169:        self.assertEqual(response.data['error']['code'], 'NOT_FOUND')
backend/apps/applications/tests/test_error_cases.py:171:    def test_validation_error_missing_fields(self):
backend/apps/applications/tests/test_error_cases.py:184:        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
backend/apps/applications/tests/test_error_cases.py:185:        self.assertEqual(response.data['error']['code'], 'VALIDATION_ERROR')
backend/apps/applications/tests/test_detail_permissions.py:61:        self.assertEqual(response.status_code, 201)
backend/apps/applications/tests/test_detail_permissions.py:67:        self.assertEqual(response.status_code, 403)
backend/apps/applications/tests/test_detail_permissions.py:68:        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
backend/apps/applications/tests/test_detail_permissions.py:78:        self.assertEqual(response.status_code, 201)
backend/apps/applications/tests/test_detail_permissions.py:84:        self.assertEqual(response.status_code, 403)
backend/apps/applications/tests/test_detail_permissions.py:85:        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
backend/apps/applications/tests/test_detail_permissions.py:95:        self.assertEqual(response.status_code, 201)
backend/apps/applications/tests/test_detail_permissions.py:101:        self.assertEqual(response.status_code, 403)
backend/apps/applications/tests/test_detail_permissions.py:102:        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
backend/apps/applications/tests/test_serializer_validation.py:18:        self.assertIn('reason', serializer.errors)
backend/apps/applications/tests/test_serializer_validation.py:40:        self.assertIn('leave_date', serializer.errors)
backend/apps/applications/tests/test_serializer_validation.py:98:        self.assertIn('leave_date', serializer.errors)
backend/apps/applications/tests/test_list_permissions.py:80:        self.assertEqual(response.status_code, 200)
backend/apps/applications/tests/test_list_permissions.py:93:        self.assertEqual(response.status_code, 200)
backend/apps/applications/tests/test_list_permissions.py:105:        self.assertEqual(response.status_code, 200)
backend/apps/applications/tests/test_constraints.py:68:        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
backend/apps/applications/tests/test_constraints.py:80:        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
backend/apps/applications/tests/test_application_flow.py:70:        self.assertEqual(response.status_code, status.HTTP_200_OK)
backend/apps/applications/tests/test_application_flow.py:80:        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
backend/apps/applications/tests/test_application_flow.py:99:        self.assertEqual(response.status_code, status.HTTP_200_OK)
backend/apps/applications/tests/test_application_flow.py:119:        self.assertEqual(response.status_code, status.HTTP_200_OK)
backend/apps/applications/tests/test_application_flow.py:129:        self.assertEqual(response.status_code, status.HTTP_200_OK)
backend/apps/users/management/commands/import_csv.py:24:            'students': {'created': 0, 'updated': 0, 'failed': 0, 'errors': []},
backend/apps/users/management/commands/import_csv.py:25:            'counselors': {'created': 0, 'updated': 0, 'failed': 0, 'errors': []},
backend/apps/users/management/commands/import_csv.py:26:            'mappings': {'created': 0, 'updated': 0, 'failed': 0, 'errors': []},
backend/apps/users/management/commands/import_csv.py:42:        errors = []
backend/apps/users/management/commands/import_csv.py:45:                errors.append(f"Row {row_num}: Missing required field '{field}'")
backend/apps/users/management/commands/import_csv.py:46:        return errors
backend/apps/users/management/commands/import_csv.py:65:                    errors = self.validate_required_fields(row, required_fields, row_num)
backend/apps/users/management/commands/import_csv.py:66:                    if errors:
backend/apps/users/management/commands/import_csv.py:67:                        summary['errors'].extend(errors)
backend/apps/users/management/commands/import_csv.py:74:                        summary['errors'].append(f"Row {row_num}: Duplicate student_id '{student_id}'")
backend/apps/users/management/commands/import_csv.py:82:                        summary['errors'].append(f"Row {row_num}: class_id '{class_id}' has no counselor mapping")
backend/apps/users/management/commands/import_csv.py:134:                    errors = self.validate_required_fields(row, required_fields, row_num)
backend/apps/users/management/commands/import_csv.py:135:                    if errors:
backend/apps/users/management/commands/import_csv.py:136:                        summary['errors'].extend(errors)
backend/apps/users/management/commands/import_csv.py:143:                        summary['errors'].append(f"Row {row_num}: Duplicate employee_id '{employee_id}'")
backend/apps/users/management/commands/import_csv.py:193:                    errors = self.validate_required_fields(row, required_fields, row_num)
backend/apps/users/management/commands/import_csv.py:194:                    if errors:
backend/apps/users/management/commands/import_csv.py:195:                        summary['errors'].extend(errors)
backend/apps/users/management/commands/import_csv.py:202:                        summary['errors'].append(f"Row {row_num}: Duplicate class_id '{class_id}'")
backend/apps/users/management/commands/import_csv.py:213:                            summary['errors'].append(f"Row {row_num}: counselor_employee_id '{counselor_id}' not found")
backend/apps/users/management/commands/import_csv.py:259:                if stats['errors']:
backend/apps/users/management/commands/import_csv.py:261:                    for error in stats['errors'][:10]:  # Show first 10 errors
backend/apps/users/management/commands/import_csv.py:262:                        self.stdout.write(f'    - {error}')
backend/apps/users/management/commands/import_csv.py:263:                    if len(stats['errors']) > 10:
backend/apps/users/management/commands/import_csv.py:264:                        self.stdout.write(f'    ... and {len(stats["errors"]) - 10} more errors')
backend/apps/applications/views.py:95:        return Response(
backend/apps/applications/views.py:96:            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
backend/apps/applications/views.py:124:        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以提交申请'}},
backend/apps/applications/views.py:129:        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
backend/apps/applications/views.py:130:                                    'details': serializer.errors}},
backend/apps/applications/views.py:140:            return Response({'error': {'code': 'CONFLICT', 'message': '已有待审批或已通过的申请，不能重复提交',
backend/apps/applications/views.py:141:                                        'details': {'student_id': user.user_id, 'existing_application_id': existing.application_id, 'status': existing.status}}},
backend/apps/applications/views.py:148:            return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
backend/apps/applications/views.py:149:                                        'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
backend/apps/applications/views.py:171:                return Response({'error': {'code': 'NOT_FOUND', 'message': '无可用宿管员',
backend/apps/applications/views.py:172:                                            'details': {'building': building or '未分配', 'fallback_id': fallback_id}}},
backend/apps/applications/views.py:218:    return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
backend/apps/applications/views.py:238:        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在',
backend/apps/applications/views.py:239:                                    'details': {'application_id': application_id}}},
backend/apps/applications/views.py:246:        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限访问此资源'}},
backend/apps/applications/views.py:249:    return Response(ApplicationSerializer(application).data)
backend/apps/applications/views.py:271:        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以创建草稿'}},
backend/apps/applications/views.py:279:        return Response(ApplicationSerializer(draft).data, status=status.HTTP_200_OK)
backend/apps/applications/views.py:290:    return Response(ApplicationSerializer(draft).data, status=status.HTTP_201_CREATED)
backend/apps/users/management/commands/import_students.py:50:            'errors': []
backend/apps/users/management/commands/import_students.py:74:                        stats['errors'].append(f"Row {stats['total']}: {str(e)}")
backend/apps/users/management/commands/import_students.py:94:            stats['errors'].append(f'{user_id}: TMP ID not allowed in import')
backend/apps/users/management/commands/import_students.py:135:        if stats['errors']:
backend/apps/users/management/commands/import_students.py:136:            self.stdout.write(self.style.WARNING(f'\nErrors ({len(stats["errors"])}):'))
backend/apps/users/management/commands/import_students.py:137:            for err in stats['errors'][:10]:
backend/apps/users/management/commands/import_students.py:139:            if len(stats['errors']) > 10:
backend/apps/users/management/commands/import_students.py:140:                self.stdout.write(f'  ... and {len(stats["errors"]) - 10} more')
backend/apps/users/management/commands/import_students.py:142:        if not dry_run and len(stats['errors']) == 0:
backend/apps/users/management/commands/import_students.py:143:            self.stdout.write(self.style.SUCCESS(f'\n✓ Import successful'))
backend/apps/attachments/tests/test_list.py:111:        self.assertEqual(response.status_code, status.HTTP_200_OK)
backend/apps/attachments/tests/test_list.py:123:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/attachments/tests/test_list.py:124:        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
backend/apps/attachments/tests/test_list.py:134:        self.assertEqual(response.status_code, status.HTTP_200_OK)
backend/apps/attachments/tests/test_list.py:145:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/attachments/tests/test_list.py:146:        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
backend/apps/attachments/tests/test_list.py:156:        self.assertEqual(response.status_code, status.HTTP_200_OK)
backend/apps/attachments/tests/test_list.py:171:        self.assertEqual(response.status_code, status.HTTP_200_OK)
backend/apps/users/management/commands/seed_data.py:116:        self.stdout.write(self.style.SUCCESS('Seed data loaded successfully'))
backend/apps/attachments/tests/test_delete.py:81:    def test_delete_owner_success(self):
backend/apps/attachments/tests/test_delete.py:89:        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
backend/apps/attachments/tests/test_delete.py:104:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/attachments/tests/test_delete.py:105:        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
backend/apps/attachments/tests/test_delete.py:119:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/attachments/tests/test_delete.py:120:        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
backend/apps/attachments/tests/test_delete.py:133:        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
backend/apps/attachments/tests/test_delete.py:134:        self.assertEqual(response.data['error']['code'], 'NOT_FOUND')
backend/apps/users/management/commands/import_staff.py:40:            'errors': [],
backend/apps/users/management/commands/import_staff.py:56:                        stats['errors'].append(f"Row {stats['total']}: {str(e)}")
backend/apps/users/management/commands/import_staff.py:74:            stats['errors'].append(f'Missing required fields: user_id={user_id}, name={name}, role={role_str}')
backend/apps/users/management/commands/import_staff.py:90:            stats['errors'].append(f'{user_id}: Unknown role "{role_str}"')
backend/apps/users/management/commands/import_staff.py:156:        if stats['errors']:
backend/apps/users/management/commands/import_staff.py:157:            self.stdout.write(self.style.WARNING(f'\nErrors ({len(stats["errors"])}):'))
backend/apps/users/management/commands/import_staff.py:158:            for err in stats['errors'][:10]:
backend/apps/users/management/commands/import_staff.py:160:            if len(stats['errors']) > 10:
backend/apps/users/management/commands/import_staff.py:161:                self.stdout.write(f'  ... and {len(stats["errors"]) - 10} more')
backend/apps/users/management/commands/import_staff.py:163:        if not dry_run and len(stats['errors']) == 0:
backend/apps/users/management/commands/import_staff.py:164:            self.stdout.write(self.style.SUCCESS(f'\n✓ Import successful'))
backend/apps/attachments/tests/test_upload.py:80:    def test_upload_success(self):
backend/apps/attachments/tests/test_upload.py:95:        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
backend/apps/attachments/tests/test_upload.py:116:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/attachments/tests/test_upload.py:117:        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
backend/apps/attachments/tests/test_upload.py:133:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/attachments/tests/test_upload.py:134:        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
backend/apps/attachments/tests/test_upload.py:148:        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
backend/apps/attachments/tests/test_upload.py:149:        self.assertEqual(response.data['error']['code'], 'VALIDATION_ERROR')
backend/apps/attachments/tests/test_upload.py:150:        self.assertIn('details', response.data['error'])
backend/apps/attachments/tests/test_upload.py:151:        self.assertIn('file', response.data['error']['details'])
backend/apps/attachments/tests/test_upload.py:166:        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
backend/apps/attachments/tests/test_upload.py:167:        self.assertEqual(response.data['error']['code'], 'VALIDATION_ERROR')
backend/apps/attachments/tests/test_upload.py:168:        self.assertIn('details', response.data['error'])
backend/apps/attachments/tests/test_upload.py:169:        self.assertIn('attachment_type', response.data['error']['details'])
backend/apps/attachments/tests/test_download.py:90:        self.assertEqual(response.status_code, status.HTTP_200_OK)
backend/apps/attachments/tests/test_download.py:101:        self.assertEqual(response.status_code, status.HTTP_200_OK)
backend/apps/attachments/tests/test_download.py:111:        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
backend/apps/attachments/tests/test_download.py:112:        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
backend/apps/attachments/tests/test_download.py:125:        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
backend/apps/attachments/tests/test_download.py:126:        self.assertEqual(response.data['error']['code'], 'NOT_FOUND')
backend/apps/attachments/views.py:63:        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在'}},
backend/apps/attachments/views.py:68:        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限上传附件'}},
backend/apps/attachments/views.py:74:        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
backend/apps/attachments/views.py:75:                                    'details': serializer.errors}},
backend/apps/attachments/views.py:91:    return Response(AttachmentSerializer(attachment).data, status=status.HTTP_201_CREATED)
backend/apps/attachments/views.py:101:        return Response({'error': {'code': 'NOT_FOUND', 'message': '申请不存在'}},
backend/apps/attachments/views.py:106:        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限查看附件'}},
backend/apps/attachments/views.py:112:    return Response({'attachments': serializer.data})
backend/apps/attachments/views.py:120:        200: OpenApiResponse(description='附件文件内容'),
backend/apps/attachments/views.py:135:        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
backend/apps/attachments/views.py:140:        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
backend/apps/attachments/views.py:146:        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限下载附件'}},
backend/apps/attachments/views.py:151:        return FileResponse(attachment.file.open('rb'), as_attachment=True, filename=attachment.file_name, content_type=attachment.content_type)
backend/apps/attachments/views.py:153:        return Response({'error': {'code': 'NOT_FOUND', 'message': '文件不存在'}},
backend/apps/attachments/views.py:163:        204: OpenApiResponse(description='删除成功'),
backend/apps/attachments/views.py:178:        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
backend/apps/attachments/views.py:183:        return Response({'error': {'code': 'NOT_FOUND', 'message': '附件不存在'}},
backend/apps/attachments/views.py:188:        return Response({'error': {'code': 'FORBIDDEN', 'message': '无权限删除附件'}},
backend/apps/attachments/views.py:196:    return Response(status=status.HTTP_204_NO_CONTENT)
backend/apps/notifications/services.py:29:    message = f"学生{application.student_name}（{application.student.user_id}）提交了离校申请，请及时审批。"
backend/apps/notifications/services.py:39:            'message': message
backend/apps/notifications/services.py:62:        message = f"您的离校申请已通过{approver_role}审批。"
backend/apps/notifications/services.py:66:        message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
backend/apps/notifications/services.py:77:            'message': message
backend/apps/notifications/services.py:117:        message = f"学生{approval.application.student_name}的离校申请已超过{days}天未审批，请及时处理。"
backend/apps/notifications/services.py:135:                    'message': message
backend/apps/attachments/serializers.py:12:            raise serializers.ValidationError('文件大小不能超过10MB')
backend/apps/attachments/serializers.py:18:            raise serializers.ValidationError(f'不支持的文件类型，仅支持：{", ".join(allowed_extensions)}')
backend/apps/notifications/admin.py:9:    search_fields = ['notification_id', 'title', 'message', 'recipient__user_id']
backend/apps/users/tests/test_xg_user_mapper.py:9:    def test_complete_fields_success(self):
backend/apps/users/views.py:16:        200: OpenApiResponse(
backend/apps/users/views.py:20:        400: OpenApiResponse(
backend/apps/users/views.py:21:            description='登录失败：DRF默认ValidationError格式（非项目envelope）'
backend/apps/users/views.py:31:        return Response(serializer.validated_data, status=status.HTTP_200_OK)
backend/apps/users/views.py:32:    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
backend/apps/users/views.py:41:        200: OpenApiResponse(
backend/apps/users/views.py:45:        403: OpenApiResponse(
backend/apps/users/views.py:48:        400: OpenApiResponse(
backend/apps/users/views.py:59:        return Response({'error': 'Demo login is disabled'}, status=status.HTTP_403_FORBIDDEN)
backend/apps/users/views.py:63:        return Response(serializer.validated_data, status=status.HTTP_200_OK)
backend/apps/users/views.py:64:    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
backend/apps/notifications/migrations/0001_initial.py:26:                ('message', models.TextField(verbose_name='消息内容')),
backend/apps/users/tests/test_xg_user_client.py:39:        self.assertIn("must be 'sha1' or 'md5'", str(cm.exception))
backend/apps/users/tests/test_xg_user_client.py:58:        self.assertEqual(config.tenant_code, 'S10405')
backend/apps/users/tests/test_xg_user_client.py:66:        self.assertIn('XG_USER_API_URL is required', str(cm.exception))
backend/apps/users/tests/test_xg_user_client.py:73:        self.assertIn('XG_USER_API_APP_KEY is required', str(cm.exception))
backend/apps/users/tests/test_xg_user_client.py:80:        self.assertIn('XG_USER_API_APP_SECRET is required', str(cm.exception))
backend/apps/users/tests/test_xg_user_client.py:83:    def test_missing_tenant_code(self):
backend/apps/users/tests/test_xg_user_client.py:87:        self.assertIn('XG_USER_API_TENANT_CODE is required', str(cm.exception))
backend/apps/users/tests/test_xg_user_client.py:94:        self.assertIn("must be 'sha1' or 'md5'", str(cm.exception))
backend/apps/users/tests/test_xg_user_client.py:172:    def test_fetch_users_page_success(self):
backend/apps/users/tests/test_xg_user_client.py:177:            'code': 200,
backend/apps/users/tests/test_xg_user_client.py:178:            'msg': 'success',
backend/apps/users/tests/test_xg_user_client.py:193:        self.assertEqual(result['code'], 200)
backend/apps/users/tests/test_xg_user_client.py:194:        self.assertEqual(result['msg'], 'success')
backend/apps/users/tests/test_xg_user_client.py:200:    def test_fetch_users_page_http_error(self):
backend/apps/users/tests/test_xg_user_client.py:210:    def test_fetch_users_page_missing_code(self):
backend/apps/users/tests/test_xg_user_client.py:211:        """测试响应缺失code字段"""
backend/apps/users/tests/test_xg_user_client.py:214:        mock_response.json.return_value = {'msg': 'no code'}
backend/apps/users/tests/test_xg_user_client.py:219:        self.assertIn("missing 'code'", str(cm.exception))
backend/apps/users/tests/test_xg_user_client.py:221:    def test_fetch_users_page_business_error(self):
backend/apps/users/tests/test_xg_user_client.py:226:            'code': 401,
backend/apps/users/tests/test_xg_user_client.py:234:        self.assertEqual(result['code'], 401)
backend/apps/users/tests/test_xg_user_client.py:242:            'code': 200,
backend/apps/users/tests/test_xg_user_client.py:243:            'msg': 'success',
backend/apps/users/tests/test_xg_user_client.py:264:            {'code': 200, 'msg': 'success', 'data': {
backend/apps/users/tests/test_xg_user_client.py:268:            {'code': 200, 'msg': 'success', 'data': {
backend/apps/users/tests/test_xg_user_client.py:272:            {'code': 200, 'msg': 'success', 'data': {
backend/apps/users/tests/test_xg_user_client.py:291:            'code': 200,
backend/apps/users/tests/test_xg_user_client.py:292:            'msg': 'success',
backend/apps/users/tests/test_xg_user_client.py:308:            {'code': 200, 'msg': 'success', 'data': {
backend/apps/users/tests/test_xg_user_client.py:312:            {'code': 200, 'msg': 'success', 'data': {
backend/apps/users/tests/test_xg_user_client.py:316:            {'code': 200, 'msg': 'success', 'data': {
backend/apps/users/tests/test_xg_user_client.py:333:            'code': 200,
backend/apps/users/tests/test_xg_user_client.py:334:            'msg': 'success',
backend/apps/users/tests/test_xg_user_client.py:349:    def test_fetch_all_users_http_error_middle_page(self):
backend/apps/users/tests/test_xg_user_client.py:353:            Mock(json=lambda: {'code': 200, 'msg': 'success', 'data': {
backend/apps/users/tests/test_xg_user_client.py:364:    def test_fetch_all_users_business_error_middle_page(self):
backend/apps/users/tests/test_xg_user_client.py:368:            {'code': 200, 'msg': 'success', 'data': {
backend/apps/users/tests/test_xg_user_client.py:372:            {'code': 500, 'msg': 'internal error', 'data': {'data': []}}
backend/apps/users/tests/test_xg_user_client.py:378:        self.assertIn('Business error', str(cm.exception))
backend/apps/users/tests/test_xg_user_client.py:384:            {'code': 200, 'msg': 'success', 'data': {
backend/apps/users/tests/test_xg_user_client.py:401:        mock_response.json.return_value = {'code': 200, 'msg': 'success'}
backend/apps/users/tests/test_xg_user_client.py:406:        self.assertIn("missing 'data' field", str(cm.exception))
backend/apps/users/tests/test_xg_user_client.py:413:            'code': 200,
backend/apps/users/tests/test_xg_user_client.py:414:            'msg': 'success',
backend/apps/users/tests/test_xg_user_client.py:421:        self.assertIn("missing 'data' (user list) field", str(cm.exception))
backend/apps/users/tests/test_xg_user_client.py:428:            'code': 200,
backend/apps/users/tests/test_xg_user_client.py:429:            'msg': 'success',
backend/apps/users/tests/test_xg_user_client.py:436:        self.assertIn("must be list", str(cm.exception))
backend/apps/users/tests/test_xg_user_client.py:442:            {'code': 200, 'msg': 'success', 'data': {
backend/apps/users/tests/test_xg_user_client.py:446:            {'code': 200, 'msg': 'success', 'data': {
backend/apps/users/tests/test_xg_user_client.py:455:        self.assertIn("not advancing", str(cm.exception))
backend/apps/users/tests/test_xg_user_client.py:462:            'code': 200,
backend/apps/users/tests/test_xg_user_client.py:463:            'msg': 'success',
backend/apps/users/tests/test_xg_user_client.py:470:        self.assertIn("Invalid per_page", str(cm.exception))
backend/apps/users/tests/test_xg_user_client.py:477:            'code': 200,
backend/apps/users/tests/test_xg_user_client.py:478:            'msg': 'success',
backend/apps/users/tests/test_xg_user_client.py:490:        self.assertIn("max_pages must be positive", str(cm.exception))
backend/apps/users/tests/test_xg_user_client.py:496:        self.assertIn("max_pages must be positive", str(cm.exception))
backend/apps/users/tests/test_xg_user_client.py:502:            {'code': 200, 'msg': 'success', 'data': {
backend/apps/users/tests/test_xg_user_client.py:506:            {'code': 200, 'msg': 'success', 'data': {
backend/apps/users/tests/test_xg_user_client.py:510:            {'code': 200, 'msg': 'success', 'data': {
backend/apps/users/tests/test_import_csv.py:24:    def test_import_counselors_success(self):
backend/apps/users/tests/test_import_csv.py:25:        """Test successful counselor import"""
backend/apps/users/tests/test_import_csv.py:47:            self.assertIn('missing required columns', str(cm.exception).lower())
backend/apps/users/tests/test_import_csv.py:66:    def test_import_mappings_success(self):
backend/apps/users/tests/test_import_csv.py:67:        """Test successful mapping import"""
backend/apps/users/tests/test_import_csv.py:97:    def test_import_students_success(self):
backend/apps/users/tests/test_import_csv.py:98:        """Test successful student import"""
backend/apps/users/tests/test_import_csv.py:149:    def test_validation_error_skips_invalid_rows(self):
backend/apps/users/tests/test_import_csv.py:150:        """Test that validation errors skip invalid rows but import valid ones"""
backend/apps/users/tests/test_xg_user_sync.py:344:    def test_scenario7_detailed_statistics(self):
backend/apps/notifications/models.py:66:    message = models.TextField(
backend/apps/notifications/serializers.py:16:            'message',
backend/apps/notifications/views.py:53:    return Response({
backend/apps/notifications/views.py:64:        200: OpenApiResponse(
backend/apps/notifications/views.py:79:    return Response({'unread_count': count})
backend/apps/notifications/views.py:105:        return Response(
backend/apps/notifications/views.py:106:            {'error': {'code': 'NOT_FOUND', 'message': '通知不存在'}},
backend/apps/notifications/views.py:111:        return Response(
backend/apps/notifications/views.py:112:            {'error': {'code': 'FORBIDDEN', 'message': '无权访问此通知'}},
backend/apps/notifications/views.py:121:    return Response(serializer.data)
backend/apps/notifications/views.py:130:        200: OpenApiResponse(
backend/apps/notifications/views.py:150:    return Response({'marked_count': updated_count})
backend/apps/users/serializers.py:31:            raise serializers.ValidationError('Invalid credentials')
backend/apps/users/serializers.py:34:            raise serializers.ValidationError('Invalid credentials')
backend/apps/users/serializers.py:37:            raise serializers.ValidationError('Account is inactive')
backend/apps/users/serializers.py:74:            raise serializers.ValidationError(f'Demo user for role {role} not found')
backend/apps/users/serializers.py:77:            raise serializers.ValidationError('Demo account is inactive')
backend/apps/notifications/tests/test_auto_notifications_api.py:70:        self.assertEqual(response.status_code, 201)
backend/apps/notifications/tests/test_auto_notifications_api.py:75:        self.assertEqual(response.status_code, 200)
backend/apps/notifications/tests/test_auto_notifications_api.py:81:        self.assertIn('测试学生', notifications[0]['message'])
backend/apps/notifications/tests/test_auto_notifications_api.py:110:        self.assertEqual(response.status_code, 200)
backend/apps/notifications/tests/test_auto_notifications_api.py:115:        self.assertEqual(response.status_code, 200)
backend/apps/notifications/tests/test_auto_notifications_api.py:123:        self.assertIn('辅导员', approval_notif['message'])
backend/apps/notifications/tests/test_auto_notifications_api.py:126:        """Test APPROVAL_REJECTED notification includes rejection reason in message."""
backend/apps/notifications/tests/test_auto_notifications_api.py:152:        self.assertEqual(response.status_code, 200)
backend/apps/notifications/tests/test_auto_notifications_api.py:157:        self.assertEqual(response.status_code, 200)
backend/apps/notifications/tests/test_auto_notifications_api.py:161:        self.assertIn('材料不齐全，请补充', reject_notif['message'])
backend/apps/notifications/tests/test_auto_notifications_api.py:199:        self.assertIn(response.status_code, [403, 404])
backend/apps/notifications/tests/test_auto_notifications_api.py:234:        self.assertEqual(response.status_code, 409)
backend/apps/notifications/tests/test_auto_notifications_api.py:262:        self.assertEqual(response.status_code, 422)
backend/apps/notifications/management/commands/seed_notifications.py:26:                message=f'您的离校申请已提交，等待审批'
backend/apps/notifications/management/commands/seed_notifications.py:37:                    message='您的离校申请已通过审批',
backend/apps/notifications/tests/test_models.py:30:            message='您的离校申请已通过辅导员审批'
backend/apps/notifications/tests/test_models.py:46:            message='您的离校申请已提交'
backend/apps/notifications/tests/test_models.py:54:            message='您的离校申请已提交'
backend/apps/notifications/tests/test_models.py:66:            message='您的离校申请已通过审批'
backend/apps/notifications/tests/test_models.py:75:                message='重复通知'
backend/apps/notifications/tests/test_models.py:92:            message='通知1'
backend/apps/notifications/tests/test_models.py:100:            message='通知2'
backend/apps/notifications/tests/test_models.py:112:            message='消息1'
backend/apps/notifications/tests/test_models.py:120:            message='消息2'
backend/apps/notifications/tests/test_api.py:37:            message='消息1'
backend/apps/notifications/tests/test_api.py:45:            message='消息2'
backend/apps/notifications/tests/test_api.py:51:        self.assertEqual(response.status_code, 200)
backend/apps/notifications/tests/test_api.py:63:            message='消息1'
backend/apps/notifications/tests/test_api.py:71:            message='消息2',
backend/apps/notifications/tests/test_api.py:95:                message=f'消息{i}'
backend/apps/notifications/tests/test_api.py:115:            message='消息1'
backend/apps/notifications/tests/test_api.py:123:            message='消息2'
backend/apps/notifications/tests/test_api.py:138:            message='消息1'
backend/apps/notifications/tests/test_api.py:146:            message='消息2',
backend/apps/notifications/tests/test_api.py:153:        self.assertEqual(response.status_code, 200)
backend/apps/notifications/tests/test_api.py:164:            message='消息'
backend/apps/notifications/tests/test_api.py:170:        self.assertEqual(response.status_code, 200)
backend/apps/notifications/tests/test_api.py:184:            message='消息'
backend/apps/notifications/tests/test_api.py:190:        self.assertEqual(response1.status_code, 200)
backend/apps/notifications/tests/test_api.py:194:        self.assertEqual(response2.status_code, 200)
backend/apps/notifications/tests/test_api.py:205:            message='消息'
backend/apps/notifications/tests/test_api.py:211:        self.assertEqual(response.status_code, 403)
backend/apps/notifications/tests/test_api.py:212:        self.assertEqual(response.data['error']['code'], 'FORBIDDEN')
backend/apps/notifications/tests/test_api.py:219:        self.assertEqual(response.status_code, 404)
backend/apps/notifications/tests/test_api.py:220:        self.assertEqual(response.data['error']['code'], 'NOT_FOUND')
backend/apps/notifications/tests/test_api.py:230:            message='消息1'
backend/apps/notifications/tests/test_api.py:238:            message='消息2'
backend/apps/notifications/tests/test_api.py:244:        self.assertEqual(response.status_code, 200)
backend/apps/users/integrations/xg_user_client.py:41:        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()
backend/apps/users/integrations/xg_user_client.py:43:        return hashlib.sha1(sign_str.encode('utf-8')).hexdigest()
backend/apps/users/integrations/xg_user_client.py:55:        self.tenant_code = os.getenv('XG_USER_API_TENANT_CODE', '').strip()
backend/apps/users/integrations/xg_user_client.py:72:        if not self.tenant_code:
backend/apps/users/integrations/xg_user_client.py:111:            'tenantCode': self.config.tenant_code,
backend/apps/users/integrations/xg_user_client.py:131:        if 'code' not in result:
backend/apps/users/integrations/xg_user_client.py:132:            raise ValueError("Response missing 'code' field")
backend/apps/users/integrations/xg_user_client.py:144:            'code': result.get('code'),
backend/apps/users/integrations/xg_user_client.py:171:            if result['code'] != 200:
backend/apps/users/integrations/xg_user_client.py:172:                raise ValueError(f"Business error: code={result['code']}, msg={result['msg']}")
backend/apps/notifications/tests/test_auto_notifications.py:77:        self.assertIn('测试学生', notification.message)
backend/apps/notifications/tests/test_auto_notifications.py:78:        self.assertIn('2021001', notification.message)
backend/apps/notifications/tests/test_auto_notifications.py:109:        self.assertIn('辅导员', notification.message)
backend/apps/notifications/tests/test_auto_notifications.py:138:        self.assertIn('宿管员', notification.message)
backend/apps/notifications/tests/test_auto_notifications.py:168:        self.assertIn('驳回', notification.message)
backend/apps/notifications/tests/test_auto_notifications.py:169:        self.assertIn('材料不齐全', notification.message)

exec
/bin/bash -lc 'rtk rg -n "2020001|M001|T001|D001|92008149|create_user|set_password|password=|DEMO_USERS" backend tests docs demo-web frontend miniprogram -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
frontend/services/mock.ts:16:    user_id: '2020001',
frontend/services/mock.ts:27:    user_id: 'T001',
frontend/services/mock.ts:39:      student_id: '2020001',
frontend/services/mock.ts:53:  student_id: '2020001',
frontend/services/mock.ts:65:      approver_id: 'T001',
frontend/services/mock.ts:83:      approver_id: 'T001',
tests/test_p0_fixes.sh:18:  -d '{"user_id":"2020001","password":"2020001"}' | jq -r '.access_token')
tests/test_p0_fixes.sh:40:  -d '{"user_id":"T001","password":"T001"}' | jq -r '.access_token')
tests/smoke_test.sh:46:echo "--- H1: Happy Path (2020001 → M001 → T001) ---"
tests/smoke_test.sh:49:echo "1. Student 2020001 login..."
tests/smoke_test.sh:52:  -d '{"user_id":"2020001","password":"2020001"}' \
tests/smoke_test.sh:96:echo "3. Dorm manager M001 login..."
tests/smoke_test.sh:97:M001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/smoke_test.sh:99:  -d '{"user_id":"M001","password":"M001"}' \
tests/smoke_test.sh:102:if [ -z "$M001_TOKEN" ] || [ "$M001_TOKEN" = "null" ]; then
tests/smoke_test.sh:111:  -H "Authorization: Bearer $M001_TOKEN" \
tests/smoke_test.sh:222:echo "7. Counselor T001 login..."
tests/smoke_test.sh:223:T001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/smoke_test.sh:225:  -d '{"user_id":"T001","password":"T001"}' \
tests/smoke_test.sh:228:if [ -z "$T001_TOKEN" ] || [ "$T001_TOKEN" = "null" ]; then
tests/smoke_test.sh:240:  -H "Authorization: Bearer $T001_TOKEN" \
tests/smoke_test.sh:462:# N2: T002 tries to approve T001's approval (should fail)
tests/smoke_test.sh:464:echo "18. T002 tries to approve T001's approval (should fail)..."
tests/test_multi_dorm_manager.sh:3:# Scenario: Student in 1号楼 submits application, both M001 and M003 receive approval tasks
tests/test_multi_dorm_manager.sh:12:echo "1. Student 2020001 login..."
tests/test_multi_dorm_manager.sh:15:  -d '{"user_id":"2020001","password":"2020001"}' \
tests/test_multi_dorm_manager.sh:45:  echo "✗ Expected 2 approvals (M001 and M003), got $APPROVALS_COUNT"
tests/test_multi_dorm_manager.sh:48:echo "✓ Both M001 and M003 received approval tasks"
tests/test_multi_dorm_manager.sh:51:M001_APPROVAL_ID=$(echo "$APP_RESPONSE" | jq -r '.approvals[] | select(.approver_name=="宿管员1") | .approval_id')
tests/test_multi_dorm_manager.sh:54:echo "  M001 approval: $M001_APPROVAL_ID"
tests/test_multi_dorm_manager.sh:57:# 4. M001 login
tests/test_multi_dorm_manager.sh:58:echo "4. M001 login..."
tests/test_multi_dorm_manager.sh:59:M001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/test_multi_dorm_manager.sh:61:  -d '{"user_id":"M001","password":"M001"}' \
tests/test_multi_dorm_manager.sh:63:echo "✓ M001 login success"
tests/test_multi_dorm_manager.sh:65:# 5. M001 approve
tests/test_multi_dorm_manager.sh:66:echo "5. M001 approve..."
tests/test_multi_dorm_manager.sh:67:M001_APPROVE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/approvals/$M001_APPROVAL_ID/approve/" \
tests/test_multi_dorm_manager.sh:68:  -H "Authorization: Bearer $M001_TOKEN" \
tests/test_multi_dorm_manager.sh:72:M001_DECISION=$(echo "$M001_APPROVE_RESPONSE" | jq -r '.decision')
tests/test_multi_dorm_manager.sh:73:if [ "$M001_DECISION" != "approved" ]; then
tests/test_multi_dorm_manager.sh:74:  echo "✗ M001 approve failed"
tests/test_multi_dorm_manager.sh:77:echo "✓ M001 approved"
tests/api_data_samples.sh:20:  -d '{"user_id":"2020001","password":"2020001"}' \
tests/api_data_samples.sh:64:  -d '{"user_id":"T001","password":"T001"}' \
docs/19名额外研究生待确认清单.md:67:- [ ] 无楼栋信息，是否走兜底宿管员程婷（92008149）审批？
docs/数据库数据分析报告.md:73:| 2020001 | 张三 | 计算机学院 | CS2020-01 | 1号楼 | 活跃 |
docs/数据库数据分析报告.md:100:| M001 | 宿管员1 | 1号楼 | 活跃 |
docs/数据库数据分析报告.md:104:**说明：** 1号楼有2个宿管员（M001、M003），支持多宿管员协同审批功能测试。
docs/数据库数据分析报告.md:110:| T001 | 李老师 | 计算机学院 | 活跃 |
docs/数据库数据分析报告.md:117:| D001 | 赵主任 | 学工部主任 | 活跃 |
docs/数据库数据分析报告.md:129:| app_43d97aed | 张三(2020001) | 测试多宿管员审批 | 2026-06-08 | approved | 2026-06-06 19:37:04 |
docs/数据库数据分析报告.md:156:| apv_7ae34163 | app_43d97aed | dorm_manager | M001(宿管员1) | approved | 同意 | 2026-06-06 19:37:05 |
docs/数据库数据分析报告.md:158:| apv_c174232a | app_43d97aed | counselor | T001(李老师) | approved | 档案已办理，同意离校 | 2026-06-07 03:00:05 |
docs/数据库数据分析报告.md:170:**测试场景：** 学生张三(2020001)住在1号楼，该楼有2个宿管员（M001、M003）
docs/数据库数据分析报告.md:173:1. 系统自动为M001和M003创建审批任务
docs/数据库数据分析报告.md:174:2. M001首先审批通过（19:37:05.061）
docs/数据库数据分析报告.md:184:| 宿管员审批 | M001 | 2026-06-06 19:37:05 | 1秒 |
docs/数据库数据分析报告.md:185:| 辅导员审批 | T001 | 2026-06-07 03:00:05 | 7小时23分 |
docs/数据库数据分析报告.md:210:- 6条通知可能包括：宿管员（M001、M003）和辅导员（T001）收到的多次通知
docs/数据库数据分析报告.md:265:- 学生张三(2020001)住1号楼，宿管员M001和M003负责1号楼
docs/数据库数据分析报告.md:266:- 学生张三属于计算机学院，辅导员T001负责计算机学院
docs/PROJECT-SUMMARY.md:257:  - 10学生（2020001-2020010，默认密码为学号）
docs/PROJECT-SUMMARY.md:258:  - 2辅导员（T001、T002，默认密码为工号）
docs/PROJECT-SUMMARY.md:259:  - 1学工部（D001，默认密码为工号）
docs/PROJECT-SUMMARY.md:323:  - 移除硬编码辅导员ID（T001）
docs/PROJECT-SUMMARY.md:327:  - 创建2个班级映射（CS2020-01→T001, CS2020-02→T002）
docs/PROJECT-SUMMARY.md:405:  2. Seed/mock/reset（45分钟）：T001/T002两条链路可重复生成
docs/PROJECT-SUMMARY.md:433:  - 修复测试问题（添加format='json'，添加D001 dean用户）
docs/PROJECT-SUMMARY.md:453:  - Gap 3: smoke test负向测试逻辑错误（测试T002审批自己的approval而非T001的）
docs/PROJECT-SUMMARY.md:2538:- ✓ **测试账号错误**：文档写password123，实际学生密码=学号，辅导员=T001/T002，学工部=D001，宿管员未实现
docs/PROJECT-SUMMARY.md:2962:3. settings/base.py：新增FALLBACK_DORM_MANAGER_USER_ID = '92008149'
docs/PROJECT-SUMMARY.md:3001:   - 兜底宿管员空building字段处理（职工号92008149）
docs/PROJECT-SUMMARY.md:3085:- 兜底宿管员：92008149 ✅ 已就位
docs/PROJECT-SUMMARY.md:3109:- 14人差异为历史测试数据（学生2020001-2020010, 宿管M001/M002, 辅导员T001/T002），不阻塞功能
docs/PROJECT-SUMMARY.md:3255:   - 旧：`--- H1: Happy Path (2020001 → T001 → D001) ---`
docs/PROJECT-SUMMARY.md:3256:   - 新：`--- H1: Happy Path (2020001 → M001 → T001) ---`
docs/PROJECT-SUMMARY.md:3272:- ✓ H1测试完全通过（student 2020001→M001 approve→T001 approve→status:approved）
docs/PROJECT-SUMMARY.md:3305:   - 验证2个审批创建 → M001审批 → M003自动完成
docs/PROJECT-SUMMARY.md:3308:- ✓ Student 2020001提交申请 → 2个审批创建(M001, M003)
docs/PROJECT-SUMMARY.md:3309:- ✓ M001审批通过
docs/PROJECT-SUMMARY.md:3363:- 学生: 2020001, 2020002（密码同学号）
docs/PROJECT-SUMMARY.md:3364:- 宿管员: M001, M002, M003（密码同工号）
docs/PROJECT-SUMMARY.md:3365:- 辅导员: T001, T002（密码同工号）
docs/PROJECT-SUMMARY.md:3366:- 学工部: D001（密码同工号）
docs/PROJECT-SUMMARY.md:3501:- ✓ 路由覆盖分析：100%完整（98.05%直接 + 116人fallback至宿管#92008149）
docs/PROJECT-SUMMARY.md:4140:- ✓ 角色映射：student→2020001, dorm_manager→M001, counselor→T001, dean→D001
docs/PROJECT-SUMMARY.md:4193:- 学生: 2020001 / 2020001
docs/PROJECT-SUMMARY.md:4194:- 宿管员: M001 / M001
docs/PROJECT-SUMMARY.md:4195:- 辅导员: T001 / T001
docs/PROJECT-SUMMARY.md:4196:- 学工部: D001 / D001
docs/PROJECT-SUMMARY.md:4221:**背景**：原集成测试使用演示数据账号（2020001, M001, T001, D001），需更新为真实生产测试账号以准确验证系统功能。
docs/api-samples/notifications_list.json:6:      "recipient_id": "2020001",
docs/api-samples/notifications_list.json:7:      "actor_id": "D001",
docs/api-samples/notifications_list.json:18:      "recipient_id": "2020001",
docs/api-samples/notifications_list.json:19:      "actor_id": "T001",
docs/api-samples/notifications_list.json:30:      "recipient_id": "2020001",
docs/api-samples/notifications_list.json:31:      "actor_id": "M001",
docs/api/notification-contract-v0.1.md:178:        "user_id": "T001",
docs/api/notification-contract-v0.1.md:378:       recipient_id="2020001",
demo-web/index.html:390:          <input id="loginUserId" type="text" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入用户ID（如 2020001）" required>
demo-web/index.html:400:          <div style="font-size: 12px; color: #999;">学生: 2020001 / 2020001</div>
demo-web/index.html:401:          <div style="font-size: 12px; color: #999;">宿管员: M001 / M001</div>
demo-web/index.html:402:          <div style="font-size: 12px; color: #999;">辅导员: T001 / T001</div>
demo-web/index.html:403:          <div style="font-size: 12px; color: #999;">学工部: D001 / D001</div>
demo-web/index.html:422:          <span style="font-size: 14px; color: #333;">2020001</span>
demo-web/index.html:532:          <span style="font-size: 14px; color: #333; flex: 1;">张三 (2020001)</span>
docs/api/contract-v0.2.md:322:      "student_id": "2020001",
docs/api/contract-v0.2.md:399:      "student_id": "2020001",
docs/api/contract-v0.2.md:429:  "student_id": "2020001",
docs/api/contract-v0.2.md:441:      "approver_id": "T001",
docs/api/contract-v0.2.md:465:  "student_id": "2020001",
docs/api/contract-v0.2.md:477:      "approver_id": "T001",
docs/api/contract-v0.2.md:487:      "approver_id": "D001",
docs/api/contract-v0.2.md:516:      "approver_id": "T001",
docs/api/contract-v0.2.md:525:      "approver_id": "T001",
docs/api/contract-v0.2.md:558:  "approver_id": "T001",
docs/api/contract-v0.2.md:585:  "approver_id": "T001",
docs/管理员操作指南和流程图补充.md:221:2. 输入工号（如：D001）
docs/acceptance/phase4c-demo-script.md:101:  -d '{"user_id":"2020001","password":"2020001"}' \
docs/acceptance/phase4c-demo-script.md:189:T001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:191:  -d '{"user_id":"T001","password":"T001"}' \
docs/acceptance/phase4c-demo-script.md:194:echo "Counselor token: ${T001_TOKEN:0:20}..."
docs/acceptance/phase4c-demo-script.md:198:  -H "Authorization: Bearer $T001_TOKEN" \
docs/acceptance/phase4c-demo-script.md:239:  -d '{"user_id":"D001","password":"D001"}' \
docs/acceptance/phase4c-demo-script.md:288:# T002尝试审批T001的审批（应该失败）
docs/acceptance/phase4c-demo-script.md:363:  -d '{"user_id":"2020001","password":"2020001"}' \
docs/acceptance/phase4c-demo-script.md:390:T001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:392:  -d '{"user_id":"T001","password":"T001"}' \
docs/acceptance/phase4c-demo-script.md:395:  -H "Authorization: Bearer $T001_TOKEN" \
docs/acceptance/phase4c-demo-script.md:408:  -d '{"user_id":"D001","password":"D001"}' \
docs/contracts/contract-v0.2.md:25:  "user_id": "2020001",
docs/contracts/contract-v0.2.md:39:  "student_id": "2020001",
docs/contracts/contract-v0.2.md:62:      "approver_id": "T001",
docs/contracts/contract-v0.2.md:79:  "approver_id": "T001",
docs/contracts/contract-v0.2.md:93:  "approver_id": "T001",
docs/contracts/contract-v0.2.md:151:{"user_id":"2020001","password":"2020001"}
docs/contracts/contract-v0.2.md:161:    "user_id": "2020001",
docs/contracts/contract-v0.2.md:223:      "student_id": "2020001",
docs/contracts/contract-v0.1.md:188:      "student_id": "2020001",
docs/contracts/contract-v0.1.md:206:  "user_id": "2020001",
docs/contracts/contract-v0.1.md:217:    "user_id": "2020001",
docs/contracts/contract-v0.1.md:243:  "student_id": "2020001",
docs/contracts/contract-v0.1.md:261:  "student_id": "2020001",
docs/contracts/contract-v0.1.md:272:      "approver_id": "T001",
docs/contracts/contract-v0.1.md:301:  "approver_id": "T001",
docs/contracts/contract-v0.1.md:324:  "approver_id": "T001",
docs/contracts/contract-v0.1.md:343:    {"user_id": "2020001", "name": "张三", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
docs/contracts/contract-v0.1.md:359:    {"user_id": "T001", "name": "李老师", "role": "counselor", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
docs/contracts/contract-v0.1.md:367:    {"user_id": "D001", "name": "赵主任", "role": "dean", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
docs/contracts/contract-v0.1.md:374:    {"class_id": "CS2020-01", "counselor_id": "T001"},
docs/contracts/contract-v0.1.md:414:            "2020001": DormCheckoutStatusDTO(
docs/contracts/contract-v0.1.md:415:                student_id="2020001",
docs/contracts/contract-v0.1.md:510:      "student_id": "2020001",
docs/contracts/contract-v0.1.md:603:        user_id: '2020001',
docs/contracts/contract-v0.1.md:627:        'user_id': '2020001',
docs/api-samples/application_detail.json:3:  "student_id": "2020001",
docs/api-samples/application_detail.json:15:      "approver_id": "M001",
docs/api-samples/application_detail.json:25:      "approver_id": "T001",
docs/api-samples/application_detail.json:35:      "approver_id": "D001",
docs/Excel数据源分析与需求对比.md:187:CS2022-01,T001
docs/Excel数据源分析与需求对比.md:188:CS2022-02,T001
docs/api-samples/applications_list.json:6:      "student_id": "2020001",
docs/week3-day0-seed-data-requirements.md:27:| student_id | 2020001 | 2020002 |
docs/week3-day0-seed-data-requirements.md:32:| password | 2020001 | 2020002 |
docs/week3-day0-seed-data-requirements.md:48:| employee_id | T001 | T002 |
docs/week3-day0-seed-data-requirements.md:51:| password | T001 | T002 |
docs/week3-day0-seed-data-requirements.md:67:| employee_id | D001 |
docs/week3-day0-seed-data-requirements.md:70:| password | D001 |
docs/week3-day0-seed-data-requirements.md:85:| CS2020-01 | T001 | 王老师 | true |
docs/week3-day0-seed-data-requirements.md:102:| 2020001 | completed | 正常流程测试 |
docs/week3-day0-seed-data-requirements.md:108:**Day 1-2验证：** 只需2020001和2020002返回completed
docs/week3-day0-seed-data-requirements.md:148:- [ ] 学生1可以登录（2020001/2020001）
docs/week3-day0-seed-data-requirements.md:150:- [ ] 辅导员1可以登录（T001/T001）
docs/week3-day0-seed-data-requirements.md:152:- [ ] 学工部可以登录（D001/D001）
docs/SYSTEM-OPERATIONS-GUIDE.md:63:  -d '{"user_id":"2020001","password":"2020001"}'
docs/SYSTEM-OPERATIONS-GUIDE.md:89:- 2020001 / 2020001（张三，1号楼，计算机学院）
docs/SYSTEM-OPERATIONS-GUIDE.md:93:- M001 / M001（宿管员1，1号楼）
docs/SYSTEM-OPERATIONS-GUIDE.md:98:- T001 / T001（李老师，计算机学院）
docs/SYSTEM-OPERATIONS-GUIDE.md:102:- D001 / D001（赵主任）
docs/SYSTEM-OPERATIONS-GUIDE.md:114:  "user_id": "2020001",
docs/SYSTEM-OPERATIONS-GUIDE.md:115:  "password": "2020001"
docs/SYSTEM-OPERATIONS-GUIDE.md:147:  "user_id": "M001",
docs/SYSTEM-OPERATIONS-GUIDE.md:148:  "password": "M001"
docs/SYSTEM-OPERATIONS-GUIDE.md:182:  "user_id": "T001",
docs/SYSTEM-OPERATIONS-GUIDE.md:183:  "password": "T001"
docs/SYSTEM-OPERATIONS-GUIDE.md:386:  -d '{"user_id":"2020001","password":"2020001"}'
docs/week3-day0-acceptance-checklist.md:69:  -d '{"user_id": "2020001", "password": "2020001"}'
docs/week3-day0-acceptance-checklist.md:77:    "user_id": "2020001",
docs/week3-day0-acceptance-checklist.md:99:  "student_id": "2020001",
docs/week3-day0-acceptance-checklist.md:126:  -d '{"user_id": "T001", "password": "T001"}'
docs/week3-day0-acceptance-checklist.md:190:  -d '{"user_id": "D001", "password": "D001"}'
docs/week3-day0-acceptance-checklist.md:260:  "student_id": "2020001",
docs/week3-day0-acceptance-checklist.md:363:- [ ] 返回completed状态（对于2020001、2020002）
docs/week3-day0-acceptance-checklist.md:424:  -d '{"user_id": "2020001", "password": "2020001"}' \
docs/week3-day0-acceptance-checklist.md:441:  -d '{"user_id": "T001", "password": "T001"}' \
docs/week3-day0-acceptance-checklist.md:454:  -d '{"user_id": "D001", "password": "D001"}' \
docs/新增审核人员.txt:3:132名未入住宿舍的毕业生申请离校，楼栋宿管员审批人基本信息：92008149 程婷  13476778525
docs/design/2026-05-27-system-design.md:683:  "student_id": "2020001",
docs/design/2026-05-27-system-design.md:697:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:724:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:762:  "student_id": "2020001",
docs/design/2026-05-27-system-design.md:775:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:797:  "student_id": "2020001",
docs/design/2026-05-27-system-design.md:811:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:913:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:1288:    "student_id": "2020001",
docs/design/2026-05-27-system-design.md:1627:  student_id: 2020001
docs/design/2026-05-27-system-design.md:1633:    "student_id": "2020001",
docs/design/2026-05-27-system-design.md:2604:    response = bind_wechat(student_id='2020001', openid='oXXX', password='wrong')
docs/design/2026-05-27-system-design.md:2619:            executor.submit(bind_wechat, '2020001', 'oXXX1', 'pass'),
docs/design/2026-05-27-system-design.md:2620:            executor.submit(bind_wechat, '2020001', 'oXXX2', 'pass')
docs/design/2026-05-27-system-design.md:2630:    bind_wechat(student_id='2020001', openid='oXXX', password='pass')
docs/design/2026-05-27-system-design.md:2638:    r1 = bind_wechat(student_id='9999999', openid='oXXX', password='pass')
docs/design/2026-05-27-system-design.md:2640:    r2 = bind_wechat(student_id='2020001', openid='oXXX', password='wrong')
docs/design/2026-05-27-system-design.md:2642:    r3 = bind_wechat(student_id='2020002', openid='oXXX', password='pass')
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:20:**Codex指出：** 文档写 `password123/counselor/dean/dorm_manager`，实际学生密码=学号，辅导员=`T001/T002`，学工部=`D001`，宿管员账号未创建
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:23:- seed_data.py:54 学生密码为 `user.set_password(student_data['user_id'])`
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:24:- seed_data.py:60 辅导员账号为 `T001/T002`
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:25:- seed_data.py:80 学工部账号为 `D001`
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:33:| 学生 | 2020001 | 2020001 | 密码等于学号 |
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:34:| 辅导员 | T001 | T001 | 第二级审批 |
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:35:| 学工部 | D001 | D001 | 备案查询 |
docs/Phase0数据验证后执行逻辑调整总结.md:34:2. 如果building为空或找不到，使用兜底宿管员(职工号92008149)
docs/Phase0数据验证后执行逻辑调整总结.md:82:| 92008149 | 程婷 | 宿管员(DORM_MANAGER) | 兜底宿管员（无building）|
docs/Phase0数据验证后执行逻辑调整总结.md:92:- 兜底宿管员路由逻辑已实现（依赖职工号92008149）
docs/Phase0数据验证后执行逻辑调整总结.md:153:- 无楼栋学生：路由到兜底宿管员（职工号92008149）
docs/Phase0数据验证后执行逻辑调整总结.md:202:**风险：** 职工号92008149的程婷未导入数据库  
docs/API测试流程演示.md:14:  - 学生：2020001 / 2020001（张三）
docs/API测试流程演示.md:15:  - 宿管员：M001 / M001（宿管员1）
docs/API测试流程演示.md:16:  - 辅导员：T001 / T001（李老师）
docs/API测试流程演示.md:28:  -d '{"user_id":"2020001","password":"2020001"}'
docs/API测试流程演示.md:37:        "user_id": "2020001",
docs/API测试流程演示.md:66:    "student_id": "2020001",
docs/API测试流程演示.md:92:    "student_id": "2020001",
docs/API测试流程演示.md:99:            "approver_id": "M001",
docs/API测试流程演示.md:119:  -d '{"user_id":"M001","password":"M001"}'
docs/API测试流程演示.md:128:        "user_id": "M001",
docs/API测试流程演示.md:186:    "approver_id": "M001",
docs/API测试流程演示.md:204:  -d '{"user_id":"T001","password":"T001"}'
docs/API测试流程演示.md:213:        "user_id": "T001",
docs/API测试流程演示.md:272:    "approver_id": "T001",
docs/API测试流程演示.md:296:    "student_id": "2020001",
docs/API测试流程演示.md:307:            "approver_id": "M001",
docs/API测试流程演示.md:316:            "approver_id": "T001",
docs/API测试流程演示.md:371:            "approver_id": "M001",
docs/用户操作手册.md:270:2. 输入学号（如：2020001）
docs/用户操作手册.md:394:2. 输入工号（如：M001）
docs/用户操作手册.md:506:2. 输入工号（如：T001）
docs/用户操作手册.md:597:2. 输入工号（如：D001）
docs/截图获取说明.md:36:**学生角色（2020001）：**
docs/截图获取说明.md:43:**宿管员角色（M001）：**
docs/截图获取说明.md:50:**辅导员角色（T001）：**
docs/UAT-CHECKLIST.md:12:- [x] 学生登录API (2020001/2020001) - 集成测试通过
docs/UAT-CHECKLIST.md:13:- [x] 宿管员登录API (M001/M001) - 集成测试通过
docs/UAT-CHECKLIST.md:14:- [x] 辅导员登录API (T001/T001) - 集成测试通过
docs/UAT-CHECKLIST.md:15:- [x] 学工部登录API (D001/D001) - 集成测试通过
docs/UAT-CHECKLIST.md:41:3. 输入用户ID: `2020001`，密码: `2020001`
docs/UAT-CHECKLIST.md:58:2. 输入用户ID: `M001`，密码: `M001`
docs/UAT-CHECKLIST.md:75:2. 输入用户ID: `T001`，密码: `T001`
docs/UAT-CHECKLIST.md:89:2. 输入用户ID: `D001`，密码: `D001`
docs/UAT-CHECKLIST.md:104:2. 输入用户ID: `2020001`，密码: `wrongpassword`
docs/UAT-CHECKLIST.md:117:**前置条件**: 以宿管员身份登录 (M001/M001)
docs/UAT-CHECKLIST.md:154:1. 学生登录 (2020001) → 提交新申请
docs/UAT-CHECKLIST.md:155:2. 退出，宿管员登录 (M001) → 审批通过
docs/UAT-CHECKLIST.md:156:3. 退出，辅导员登录 (T001) → 查看审批列表
docs/UAT-CHECKLIST.md:191:  - 学生: 2020001 / 2020001
docs/UAT-CHECKLIST.md:192:  - 宿管员: M001 / M001
docs/UAT-CHECKLIST.md:193:  - 辅导员: T001 / T001
docs/UAT-CHECKLIST.md:194:  - 学工部: D001 / D001
docs/兜底宿管员路由逻辑方案.md:16:- 新增宿管员程婷（职工号：92008149）
docs/兜底宿管员路由逻辑方案.md:112:                user_id='92008149',  # 程婷职工号
docs/兜底宿管员路由逻辑方案.md:245:92008149,程婷,宿管员,13476778525,,"负责无楼栋学生审批（兜底宿管员）"
backend/config/settings/base.py:160:FALLBACK_DORM_MANAGER_USER_ID = '92008149'
backend/data/templates/counselors_template.csv:2:T001,李老师,计算机学院,true,T001
backend/data/templates/class_mappings_template.csv:2:CS2020-01,T001
backend/data/templates/students_template.csv:2:2020001,张三,计算机学院,计算机科学与技术,CS2020-01,2020,2024,true,2020001
backend/backend/apps/users/management/commands/cleanup_test_data.py:26:            '2020001', '2020002', '2020003', '2020004', '2020005',
backend/backend/apps/users/management/commands/cleanup_test_data.py:28:            'M001', 'M002', 'M003', 'T001', 'T002', 'D001'
backend/scripts/generate_temp_user_ids.py:71:    uid, source = determine_user_id("2020001", "张三", "计算机学院", "荷园1栋", "101", 1)
backend/scripts/generate_temp_user_ids.py:73:    assert uid == "2020001"
backend/data/additional_staff.csv:4:92008149,程婷,宿管员,13476778525,,"负责无楼栋学生审批（兜底宿管员）"
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:87:    "student_id": "2020001",
docs/API-DATA-EXAMPLES.md:15:  "student_id": "2020001",
docs/API-DATA-EXAMPLES.md:33:| student_id | string | 学号 | 2020001 |
docs/API-DATA-EXAMPLES.md:55:  "approver_id": "M001",
docs/API-DATA-EXAMPLES.md:70:| approver_id | string | 审批人ID | M001 |
docs/操作说明书.md:132:3. 输入学号：2020001，密码：password123
docs/操作说明书.md:319:| 学生 | 2020001 | 2020001 | 密码等于学号，可提交申请 |
docs/操作说明书.md:320:| 辅导员 | T001 | T001 | 第二级审批（李老师） |
docs/操作说明书.md:322:| 学工部 | D001 | D001 | 备案查询（赵主任） |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:155:| 工号 | employee_id | 文本 | 是 | 辅导员唯一标识 | T2020001 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:209:| 辅导员工号 | counselor_employee_id | 文本 | 是 | 辅导员工号 | T2020001 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:270:| 工号 | employee_id | 文本 | 是 | 管理员唯一标识 | A2020001 |
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:53:    user.set_password(password)
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:42:2. 辅导员导入：`student_id=NULL, employee_id='T001', role='counselor'` → 主键包含NULL，插入失败
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:68:    "student_id": "2020001",
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:84:    "student_id": "2020001",
docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:155:      "student_id": "2020001",
docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md:196:- T002看不到T001的approvals
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:42:**Problem:** smoke_test.sh line 175 tries to create second application with same student `2020001`.
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:144:3. T002 cannot see T001 approvals
backend/apps/applications/providers.py:18:            "2020001": DormCheckoutStatusDTO(
backend/apps/applications/providers.py:19:                student_id="2020001",
docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md:198:- ✓ Seed/reset可以稳定生成T001/T002两条链路
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:197:5. Smoke test verification (T002 cannot see T001 data)
docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md:89:- T002看不到T001的approvals
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:41:      "student_id": "2020001",
docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md:78:      "approver_id": "T001",
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:43:1. **先恢复测试与数据基线。** 修`2020002`、Mock、CSV模板、测试fixtures，让T001/T002两条链路可构造。否则后续权限和smoke都没有可靠样本。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:62:- 对学工部，不要在业务逻辑里散落硬编码`D001`。MVP可以用`DEFAULT_DEAN_USER_ID=D001`或“唯一active dean”解析，但创建Dean approval时应从`User`表读取真实用户和姓名。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:94:- `2020001 -> CS2020-01 -> T001 -> completed`
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:108:- 验证正向链路：`2020002`提交后由`T002`审批，再由`D001`审批，最终状态`approved`。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:109:- 验证负向链路：`T001`不能审批`2020002`的approval；重复审批返回409；重复提交返回409；错误step/status返回409。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:143:7. **D001硬编码没有治理方案。** 可以作为seed常量，但不应成为业务逻辑长期事实。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:157:- `seed_data --reset`或等价流程能稳定生成T001/T002/D001和正负样本。
docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md:161:- 列表接口能让T002发现`2020002`的待办，D001发现学工部待办。
backend/apps/users/serializers.py:60:    DEMO_USERS = {
backend/apps/users/serializers.py:61:        'student': '2020001',
backend/apps/users/serializers.py:62:        'dorm_manager': 'M001',
backend/apps/users/serializers.py:63:        'counselor': 'T001',
backend/apps/users/serializers.py:64:        'dean': 'D001',
backend/apps/users/serializers.py:69:        user_id = self.DEMO_USERS.get(role)
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:249:5. **Smoke test verification** - Verify T002 cannot see T001's data
docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md:70:- Seed/mock/reset 能稳定生成 T001/T002 两条链路。
backend/apps/applications/tests/test_application_flow.py:17:        self.student = User.objects.create_user(
backend/apps/applications/tests/test_application_flow.py:18:            user_id='2020001',
backend/apps/applications/tests/test_application_flow.py:19:            password='2020001',
backend/apps/applications/tests/test_application_flow.py:29:        self.counselor = User.objects.create_user(
backend/apps/applications/tests/test_application_flow.py:30:            user_id='T001',
backend/apps/applications/tests/test_application_flow.py:31:            password='T001',
backend/apps/applications/tests/test_application_flow.py:37:        self.dorm_manager = User.objects.create_user(
backend/apps/applications/tests/test_application_flow.py:38:            user_id='M001',
backend/apps/applications/tests/test_application_flow.py:39:            password='M001',
backend/apps/applications/tests/test_application_flow.py:45:        self.dean = User.objects.create_user(
backend/apps/applications/tests/test_application_flow.py:46:            user_id='D001',
backend/apps/applications/tests/test_application_flow.py:47:            password='D001',
backend/apps/applications/tests/test_application_flow.py:67:            'user_id': '2020001',
backend/apps/applications/tests/test_application_flow.py:68:            'password': '2020001'
backend/apps/applications/tests/test_application_flow.py:86:            'user_id': 'M001',
backend/apps/applications/tests/test_application_flow.py:87:            'password': 'M001'
backend/apps/applications/tests/test_application_flow.py:107:            'user_id': 'T001',
backend/apps/applications/tests/test_application_flow.py:108:            'password': 'T001'
backend/apps/applications/tests/test_error_cases.py:16:        self.student1 = User.objects.create_user(
backend/apps/applications/tests/test_error_cases.py:17:            user_id='2020001',
backend/apps/applications/tests/test_error_cases.py:18:            password='2020001',
backend/apps/applications/tests/test_error_cases.py:28:        self.student2 = User.objects.create_user(
backend/apps/applications/tests/test_error_cases.py:30:            password='2020002',
backend/apps/applications/tests/test_error_cases.py:40:        self.student3 = User.objects.create_user(
backend/apps/applications/tests/test_error_cases.py:42:            password='2020003',
backend/apps/applications/tests/test_error_cases.py:52:        self.counselor = User.objects.create_user(
backend/apps/applications/tests/test_error_cases.py:53:            user_id='T001',
backend/apps/applications/tests/test_error_cases.py:54:            password='T001',
backend/apps/applications/tests/test_error_cases.py:59:        self.dorm_manager = User.objects.create_user(
backend/apps/applications/tests/test_error_cases.py:60:            user_id='M001',
backend/apps/applications/tests/test_error_cases.py:61:            password='M001',
backend/apps/applications/tests/test_error_cases.py:67:        self.dean = User.objects.create_user(
backend/apps/applications/tests/test_error_cases.py:68:            user_id='D001',
backend/apps/applications/tests/test_error_cases.py:69:            password='D001',
backend/apps/applications/tests/test_error_cases.py:104:            'user_id': '2020001',
backend/apps/applications/tests/test_error_cases.py:105:            'password': '2020001'
backend/apps/applications/tests/test_error_cases.py:132:            'user_id': '2020001',
backend/apps/applications/tests/test_error_cases.py:133:            'password': '2020001'
backend/apps/applications/tests/test_error_cases.py:161:            'user_id': '2020001',
backend/apps/applications/tests/test_error_cases.py:162:            'password': '2020001'
backend/apps/applications/tests/test_error_cases.py:174:            'user_id': '2020001',
backend/apps/applications/tests/test_error_cases.py:175:            'password': '2020001'
backend/apps/users/models.py:14:    def create_user(self, user_id, password=None, **extra_fields):
backend/apps/users/models.py:18:        user.set_password(password)
backend/apps/users/models.py:22:    def create_superuser(self, user_id, password=None, **extra_fields):
backend/apps/users/models.py:26:        return self.create_user(user_id, password, **extra_fields)
backend/apps/applications/tests/test_detail_permissions.py:15:        self.student1 = User.objects.create(user_id='2020001', name='学生1', role=UserRole.STUDENT, class_id='CS2020-01', building='1号楼', department='计算机学院')
backend/apps/applications/tests/test_detail_permissions.py:16:        self.student1.set_password('2020001')
backend/apps/applications/tests/test_detail_permissions.py:20:        self.student2.set_password('2020002')
backend/apps/applications/tests/test_detail_permissions.py:24:        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR, department='计算机学院')
backend/apps/applications/tests/test_detail_permissions.py:25:        self.counselor1.set_password('T001')
backend/apps/applications/tests/test_detail_permissions.py:29:        self.counselor2.set_password('T002')
backend/apps/applications/tests/test_detail_permissions.py:32:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER, building='1号楼')
backend/apps/applications/tests/test_detail_permissions.py:33:        self.dorm_manager1.set_password('M001')
backend/apps/applications/tests/test_detail_permissions.py:37:        self.dorm_manager2.set_password('M002')
backend/apps/applications/tests/test_detail_permissions.py:41:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
backend/apps/applications/tests/test_detail_permissions.py:42:        self.dean1.set_password('D001')
backend/apps/applications/tests/test_detail_permissions.py:46:        self.dean2.set_password('D002')
backend/apps/applications/views.py:166:            fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')
backend/apps/users/tests/test_xg_user_sync.py:27:            user_id='T001',
backend/apps/users/tests/test_xg_user_sync.py:103:                'number': 'T001',
backend/apps/users/tests/test_xg_user_sync.py:118:        self.assertEqual(conflict['user_id'], 'T001')
backend/apps/users/tests/test_xg_user_sync.py:197:            {'number': 'T001', 'name': '李老师', 'user_identity': '1'},
backend/apps/users/tests/test_xg_user_sync.py:208:        self.assertEqual(result['existing_count'], 2)  # T001和2021001都存在
backend/apps/users/tests/test_xg_user_sync.py:244:            user_id='T001',
backend/apps/users/tests/test_xg_user_sync.py:284:        xg_users = [{'number': 'T001', 'name': '李老师', 'user_identity': '1'}]
backend/apps/users/tests/test_xg_user_sync.py:349:            {'number': 'T001', 'name': '李老师', 'user_identity': '1'},
backend/apps/users/tests/test_xg_user_sync.py:382:        counselor = User.objects.get(user_id='T001')
backend/apps/applications/tests/test_list_permissions.py:15:        self.student1.set_password('S001')
backend/apps/applications/tests/test_list_permissions.py:19:        self.student2.set_password('S002')
backend/apps/applications/tests/test_list_permissions.py:22:        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
backend/apps/applications/tests/test_list_permissions.py:23:        self.counselor1.set_password('T001')
backend/apps/applications/tests/test_list_permissions.py:27:        self.counselor2.set_password('T002')
backend/apps/applications/tests/test_list_permissions.py:30:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
backend/apps/applications/tests/test_list_permissions.py:31:        self.dorm_manager1.set_password('M001')
backend/apps/applications/tests/test_list_permissions.py:35:        self.dorm_manager2.set_password('M002')
backend/apps/applications/tests/test_list_permissions.py:38:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
backend/apps/applications/tests/test_list_permissions.py:39:        self.dean.set_password('D001')
backend/apps/applications/tests/test_constraints.py:14:        self.student = User.objects.create_user(
backend/apps/applications/tests/test_constraints.py:15:            user_id='2020001',
backend/apps/applications/tests/test_constraints.py:21:            password='2020001',
backend/apps/applications/tests/test_constraints.py:27:        self.counselor = User.objects.create_user(
backend/apps/applications/tests/test_constraints.py:28:            user_id='T001',
backend/apps/applications/tests/test_constraints.py:31:            password='T001',
backend/apps/applications/tests/test_constraints.py:34:        self.dorm_manager = User.objects.create_user(
backend/apps/applications/tests/test_constraints.py:35:            user_id='M001',
backend/apps/applications/tests/test_constraints.py:38:            password='M001',
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:34:- 46 号共识中的验收项写了“通知断言按本次实体过滤，不受旧数据干扰”。当前 smoke 主要通过 message 内容过滤通知，例如包含 `2020001`、`辅导员`、`材料不齐全`，不是通过当前 `approval_id` 或 `application_id` 过滤。由于推荐运行方式是 `SMOKE_RESET=1`，这不是本轮阻塞项，但应避免在总结中声称已经完全实现“按实体 id 过滤”。
backend/apps/approvals/tests/test_list_permissions.py:14:        self.student.set_password('S001')
backend/apps/approvals/tests/test_list_permissions.py:17:        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
backend/apps/approvals/tests/test_list_permissions.py:18:        self.counselor1.set_password('T001')
backend/apps/approvals/tests/test_list_permissions.py:22:        self.counselor2.set_password('T002')
backend/apps/approvals/tests/test_list_permissions.py:25:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
backend/apps/approvals/tests/test_list_permissions.py:26:        self.dorm_manager1.set_password('M001')
backend/apps/approvals/tests/test_list_permissions.py:30:        self.dorm_manager2.set_password('M002')
backend/apps/approvals/tests/test_list_permissions.py:33:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
backend/apps/approvals/tests/test_list_permissions.py:34:        self.dean1.set_password('D001')
backend/apps/approvals/tests/test_list_permissions.py:38:        self.dean2.set_password('D002')
backend/apps/approvals/tests/test_permissions.py:13:        self.student1 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:14:            user_id='2020001',
backend/apps/approvals/tests/test_permissions.py:18:            password='2020001',
backend/apps/approvals/tests/test_permissions.py:22:        self.student2 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:27:            password='2020002',
backend/apps/approvals/tests/test_permissions.py:33:        self.counselor1 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:34:            user_id='T001',
backend/apps/approvals/tests/test_permissions.py:37:            password='T001',
backend/apps/approvals/tests/test_permissions.py:40:        self.counselor2 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:44:            password='T002',
backend/apps/approvals/tests/test_permissions.py:47:        self.dorm_manager1 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:48:            user_id='M001',
backend/apps/approvals/tests/test_permissions.py:51:            password='M001',
backend/apps/approvals/tests/test_permissions.py:54:        self.dorm_manager2 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:58:            password='M002',
backend/apps/approvals/tests/test_permissions.py:61:        self.dean1 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:62:            user_id='D001',
backend/apps/approvals/tests/test_permissions.py:65:            password='D001'
backend/apps/approvals/tests/test_permissions.py:67:        self.dean2 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:71:            password='D002'
backend/apps/approvals/tests/test_permissions.py:185:        # T002 tries to approve T001's application
backend/apps/approvals/tests/test_permissions.py:196:        # T002 tries to reject T001's application
backend/apps/notifications/tests/test_auto_notifications_api.py:26:        self.student = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications_api.py:27:            user_id='2020001',
backend/apps/notifications/tests/test_auto_notifications_api.py:34:        self.counselor = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications_api.py:35:            user_id='T001',
backend/apps/notifications/tests/test_auto_notifications_api.py:40:        self.dorm_manager = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications_api.py:41:            user_id='M001',
backend/apps/notifications/tests/test_auto_notifications_api.py:46:        self.dean = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications_api.py:47:            user_id='D001',
backend/apps/notifications/tests/test_auto_notifications_api.py:166:        student2 = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications_api.py:246:        blocked_student = User.objects.create_user(
backend/apps/approvals/tests/test_state_machine.py:13:        self.student = User.objects.create_user(
backend/apps/approvals/tests/test_state_machine.py:14:            user_id='2020001',
backend/apps/approvals/tests/test_state_machine.py:18:            password='2020001',
backend/apps/approvals/tests/test_state_machine.py:24:        self.counselor = User.objects.create_user(
backend/apps/approvals/tests/test_state_machine.py:25:            user_id='T001',
backend/apps/approvals/tests/test_state_machine.py:28:            password='T001',
backend/apps/approvals/tests/test_state_machine.py:33:        self.dorm_manager = User.objects.create_user(
backend/apps/approvals/tests/test_state_machine.py:34:            user_id='M001',
backend/apps/approvals/tests/test_state_machine.py:37:            password='M001',
backend/apps/approvals/tests/test_state_machine.py:42:        self.dean = User.objects.create_user(
backend/apps/approvals/tests/test_state_machine.py:43:            user_id='D001',
backend/apps/approvals/tests/test_state_machine.py:46:            password='D001'
backend/apps/notifications/tests/test_timeout_warnings.py:15:        self.student = User.objects.create_user(
backend/apps/notifications/tests/test_timeout_warnings.py:16:            user_id='2020001',
backend/apps/notifications/tests/test_timeout_warnings.py:23:        self.counselor = User.objects.create_user(
backend/apps/notifications/tests/test_timeout_warnings.py:24:            user_id='T001',
backend/apps/notifications/tests/test_timeout_warnings.py:30:        self.dorm_manager = User.objects.create_user(
backend/apps/notifications/tests/test_timeout_warnings.py:31:            user_id='M001',
backend/apps/users/tests/test_import_csv.py:14:        User.objects.create_user(user_id='T001', name='李老师', role=UserRole.COUNSELOR, password='T001', department='计算机学院')
backend/apps/users/tests/test_import_csv.py:15:        User.objects.create_user(user_id='T002', name='王老师', role=UserRole.COUNSELOR, password='T002', department='软件学院')
backend/apps/users/tests/test_import_csv.py:68:        csv_content = "class_id,counselor_employee_id\nCS2020-01,T001\nCS2020-02,T002"
backend/apps/users/tests/test_import_csv.py:77:            self.assertEqual(mapping.counselor.user_id, 'T001')
backend/apps/users/tests/test_import_csv.py:99:        counselor = User.objects.get(user_id='T001')
backend/apps/users/tests/test_import_csv.py:102:        csv_content = "student_id,name,class_id,is_graduating,graduation_year\n2020001,张三,CS2020-01,true,2024"
backend/apps/users/tests/test_import_csv.py:110:            student = User.objects.get(user_id='2020001')
backend/apps/users/tests/test_import_csv.py:119:        csv_content = "student_id,name,class_id,is_graduating,graduation_year\n2020001,张三,CS2020-99,true,2024"
backend/apps/notifications/tests/test_models.py:10:            user_id='2020001',
backend/apps/notifications/tests/test_models.py:16:            user_id='T001',
backend/apps/notifications/tests/test_api.py:12:            user_id='2020001',
backend/apps/notifications/tests/test_api.py:24:            user_id='T001',
backend/apps/notifications/tests/test_auto_notifications.py:27:        self.student = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications.py:35:        self.counselor = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications.py:36:            user_id='T001',
backend/apps/notifications/tests/test_auto_notifications.py:41:        self.dorm_manager = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications.py:42:            user_id='M001',
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:58:当前smoke直接用固定账号提交申请，并且脚本没有清理数据库。只要环境中已经存在学生`2020001`或`2020002`的待审批/已通过申请，提交步骤就会被409挡住。当前通知检查也只验证未读数量，既有未读通知会掩盖本次流程是否真的创建了正确通知。
docs/discussions/phase4c-next-steps/31-claude-post-contract-revision-next-strategy.md:242:python manage.py seed_notifications --user 2020001 --count 10
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:19:- `2020001 -> T001 -> D001` 这一条链路在当前数据库状态下成功
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:31:| 3. 学生登录提交 | ✓ 达标 | 2020001达标 |
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:36:| 8. 宿舍清退Mock | ⚠ 部分达标 | 只对2020001达标，缺抽象接口 |
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:113:1. **修正seed/mock**：让两个不同班级学生都能正向提交，分别验证T001/T002
docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md:114:2. **修审批权限**：必须校验审批人就是当前用户；补T002不能审批T001班级的负向测试
docs/discussions/week3-day1-review-2026-05-30/12-final-consensus-execution-plan.md:98:- T001/T002两条链路必须可重复生成
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:57:3. **dean选择方式。** 短期可保留 `D001`，但如果实现动态查询成本很低，可以顺手修；不应阻塞核心安全项。
docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md:73:3. **High - `seed_data --reset` 当前不存在，且样本数据不满足 T001/T002 双链路。**
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:243:        Student(student_id="2020001", name="张三", class_id="CS2020-01", is_graduating=True),
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:253:        Counselor(employee_id="T001", name="李老师", is_active=True),
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:258:        "2020001": CheckoutStatus(status="completed", date="2024-06-15"),
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:71:- 修复：学工部从User表查询（不硬编码D001）
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:73:- 验证：T002不能审批T001的申请（403）
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:94:- 实现：正向路径（2020002 → T002 → D001 → approved）
docs/discussions/week3-day1-review-2026-05-30/07-consensus-day2-plan.md:144:- ✓ Seed/mock数据正确（T001/T002两条链路）
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:32:- 测试：T002不能审批T001班级的申请
docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md:110:- 学工部审批是否也需要权限校验？（当前硬编码D001）
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:52:- T001/T002双链路数据生成可能有bug
docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md:86:- Phase 2（15分钟）：生成T001链路数据
backend/apps/attachments/tests/test_list.py:16:        self.student = User.objects.create_user(
backend/apps/attachments/tests/test_list.py:17:            user_id='2020001',
backend/apps/attachments/tests/test_list.py:18:            password='2020001',
backend/apps/attachments/tests/test_list.py:28:        self.other_student = User.objects.create_user(
backend/apps/attachments/tests/test_list.py:30:            password='2020002',
backend/apps/attachments/tests/test_list.py:41:        self.counselor = User.objects.create_user(
backend/apps/attachments/tests/test_list.py:42:            user_id='T001',
backend/apps/attachments/tests/test_list.py:43:            password='T001',
backend/apps/attachments/tests/test_list.py:49:        self.other_counselor = User.objects.create_user(
backend/apps/attachments/tests/test_list.py:51:            password='T002',
backend/apps/attachments/tests/test_list.py:58:        self.dean = User.objects.create_user(
backend/apps/attachments/tests/test_list.py:59:            user_id='D001',
backend/apps/attachments/tests/test_list.py:60:            password='D001',
backend/apps/attachments/tests/test_delete.py:16:        self.student = User.objects.create_user(
backend/apps/attachments/tests/test_delete.py:17:            user_id='2020001',
backend/apps/attachments/tests/test_delete.py:18:            password='2020001',
backend/apps/attachments/tests/test_delete.py:28:        self.other_student = User.objects.create_user(
backend/apps/attachments/tests/test_delete.py:30:            password='2020002',
backend/apps/attachments/tests/test_delete.py:41:        self.counselor = User.objects.create_user(
backend/apps/attachments/tests/test_delete.py:42:            user_id='T001',
backend/apps/attachments/tests/test_delete.py:43:            password='T001',
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:29:1. 只测试了一条路径（2020001 → T001 → D001）
docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md:118:- 测试：T002不能审批T001班级的申请
backend/apps/attachments/tests/test_upload.py:16:        self.student = User.objects.create_user(
backend/apps/attachments/tests/test_upload.py:17:            user_id='2020001',
backend/apps/attachments/tests/test_upload.py:18:            password='2020001',
backend/apps/attachments/tests/test_upload.py:29:        self.other_student = User.objects.create_user(
backend/apps/attachments/tests/test_upload.py:31:            password='2020002',
backend/apps/attachments/tests/test_upload.py:42:        self.counselor = User.objects.create_user(
backend/apps/attachments/tests/test_upload.py:43:            user_id='T001',
backend/apps/attachments/tests/test_upload.py:44:            password='T001',
docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md:121:- Seed/mock/reset能稳定生成T001/T002两条链路
docs/discussions/codex-review-2026-05-30/50-p1-fixes-summary.md:55:      "student_id": "2020001",
docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md:192:- T001/T002两条链路必须可重复生成。
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:97:                student_id="2020001",
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:112:                employee_id="T001",
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:118:- 学工部D001硬编码应该修复（从User表查询唯一dean）
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:179:- 2020001 → CS2020-01 → T001 → completed
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:207:- 正向路径：2020002 → T002 → D001 → approved
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:258:7. **D001硬编码无治理方案** - ✓ 接受，Day 2从User表查询
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:276:- 列表接口能让T002/D001发现待办
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:294:- ✓ Seed/mock数据正确（T001/T002两条链路）
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:329:- 修复：学工部从User表查询（不硬编码D001）
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:331:- 验证：T002不能审批T001的申请（403）
docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md:352:- 实现：正向路径（2020002 → T002 → D001 → approved）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:215:        Student(student_id="2020001", name="张三", class_id="CS2020-01", is_graduating=True),
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:225:        Counselor(employee_id="T001", name="李老师", is_active=True),
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:230:        "2020001": CheckoutStatus(status="completed", date="2024-06-15"),
backend/apps/attachments/tests/test_download.py:17:        self.student = User.objects.create_user(
backend/apps/attachments/tests/test_download.py:18:            user_id='2020001',
backend/apps/attachments/tests/test_download.py:19:            password='2020001',
backend/apps/attachments/tests/test_download.py:29:        self.other_student = User.objects.create_user(
backend/apps/attachments/tests/test_download.py:31:            password='2020002',
backend/apps/attachments/tests/test_download.py:42:        self.counselor = User.objects.create_user(
backend/apps/attachments/tests/test_download.py:43:            user_id='T001',
backend/apps/attachments/tests/test_download.py:44:            password='T001',
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:182:3. 学工部从User表查询（不硬编码D001）
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:187:# T002尝试审批T001的申请，期望403
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:188:curl -X POST http://localhost:8001/api/approvals/{T001的approval_id}/approve \
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:260:1. 正向路径：2020002 → T002 → D001 → approved
docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md:336:- ✓ Seed/mock数据正确（T001/T002两条链路）
backend/apps/approvals/tests/test_rejection_flow.py:16:        self.student = User.objects.create_user(
backend/apps/approvals/tests/test_rejection_flow.py:17:            user_id='2020001',
backend/apps/approvals/tests/test_rejection_flow.py:18:            password='2020001',
backend/apps/approvals/tests/test_rejection_flow.py:28:        self.counselor = User.objects.create_user(
backend/apps/approvals/tests/test_rejection_flow.py:29:            user_id='T001',
backend/apps/approvals/tests/test_rejection_flow.py:30:            password='T001',
backend/apps/approvals/tests/test_rejection_flow.py:36:        self.dorm_manager = User.objects.create_user(
backend/apps/approvals/tests/test_rejection_flow.py:37:            user_id='M001',
backend/apps/approvals/tests/test_rejection_flow.py:38:            password='M001',
backend/apps/approvals/tests/test_rejection_flow.py:57:            'user_id': '2020001',
backend/apps/approvals/tests/test_rejection_flow.py:58:            'password': '2020001'
backend/apps/approvals/tests/test_rejection_flow.py:73:            'user_id': 'M001',
backend/apps/approvals/tests/test_rejection_flow.py:74:            'password': 'M001'
backend/apps/approvals/tests/test_rejection_flow.py:91:            'user_id': 'M001',
backend/apps/approvals/tests/test_rejection_flow.py:92:            'password': 'M001'
backend/apps/approvals/tests/test_rejection_flow.py:117:            'user_id': 'T001',
backend/apps/approvals/tests/test_rejection_flow.py:118:            'password': 'T001'
backend/apps/users/management/commands/import_csv.py:104:                            user.set_password(row.get('password', student_id))
backend/apps/users/management/commands/import_csv.py:163:                            user.set_password(row.get('password', employee_id))
backend/apps/users/management/commands/seed_data.py:28:            {'user_id': '2020001', 'name': '张三', 'class_id': 'CS2020-01', 'building': '1号楼', 'department': '计算机学院'},
backend/apps/users/management/commands/seed_data.py:55:                user.set_password(student_data['user_id'])
backend/apps/users/management/commands/seed_data.py:61:            {'user_id': 'T001', 'name': '李老师', 'department': '计算机学院'},
backend/apps/users/management/commands/seed_data.py:76:                user.set_password(counselor_data['user_id'])
backend/apps/users/management/commands/seed_data.py:82:            {'user_id': 'M001', 'name': '宿管员1', 'building': '1号楼'},
backend/apps/users/management/commands/seed_data.py:98:                user.set_password(dm_data['user_id'])
backend/apps/users/management/commands/seed_data.py:104:            user_id='D001',
backend/apps/users/management/commands/seed_data.py:112:            user.set_password('D001')
backend/apps/users/management/commands/import_staff.py:108:            fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')

codex
前端搜索结果显示 demo-web 当前仍在调用普通 `/auth/login`，不是这个新增 `/auth/demo-login`；这属于契约/集成风险。为避免误报，我会打开相关前端接口文件和最新项目记录确认“期望”是什么。
exec
/bin/bash -lc "rtk nl -ba frontend/types/api.ts | rtk sed -n '1,90p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	// API Types based on v0.2 Contract
     2	// Generated: 2026-05-31
     3	
     4	export type UserRole = 'student' | 'dorm_manager' | 'counselor' | 'dean' | 'admin';
     5	
     6	export type ApplicationStatus =
     7	  | 'draft'
     8	  | 'pending_dorm_manager'
     9	  | 'pending_counselor'
    10	  | 'approved'
    11	  | 'rejected';
    12	
    13	export type ApprovalDecision = 'pending' | 'approved' | 'rejected';
    14	
    15	export type ApprovalStep = 'dorm_manager' | 'counselor';
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
    38	  contact_phone: string;
    39	  reason?: string;
    40	  leave_date: string; // YYYY-MM-DD
    41	}
    42	
    43	export interface Application {
    44	  application_id: string;
    45	  student_id: string;
    46	  student_name: string;
    47	  class_id: string;
    48	  contact_phone?: string | null;
    49	  reason: string;
    50	  leave_date: string;
    51	  status: ApplicationStatus;
    52	  created_at: string;
    53	  updated_at: string;
    54	}
    55	
    56	export interface ApplicationDetail extends Application {
    57	  dorm_checkout_status: string;
    58	  approvals: ApprovalDetail[];
    59	}
    60	
    61	// Approvals
    62	export interface ApprovalDetail {
    63	  approval_id: string;
    64	  application_id: string;
    65	  step: ApprovalStep;
    66	  approver_id: string;
    67	  approver_name: string;
    68	  decision: ApprovalDecision;
    69	  comment: string | null;
    70	  decided_at: string | null;
    71	}
    72	
    73	export interface ApprovalListItem {
    74	  approval_id: string;
    75	  application_id: string;
    76	  step: ApprovalStep;
    77	  approver_id: string;
    78	  approver_name: string;
    79	  decision: ApprovalDecision;
    80	  created_at: string;
    81	}
    82	
    83	export interface ApprovalActionRequest {
    84	  comment?: string;
    85	}
    86	
    87	export interface ApprovalActionResponse {
    88	  approval_id: string;
    89	  decision: ApprovalDecision;
    90	  comment: string | null;

exec
/bin/bash -lc "rtk nl -ba demo-web/js/api.js | rtk sed -n '1,160p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	// API Integration Layer
     2	const API_BASE_URL = '/api';
     3	
     4	let currentToken = null;
     5	let currentUser = null;
     6	
     7	async function apiLogin(userId, password) {
     8	    try {
     9	        const response = await fetch(API_BASE_URL + '/auth/login', {
    10	            method: 'POST',
    11	            headers: { 'Content-Type': 'application/json' },
    12	            body: JSON.stringify({
    13	                user_id: userId,
    14	                password: password
    15	            })
    16	        });
    17	
    18	        if (response.ok) {
    19	            const data = await response.json();
    20	            currentToken = data.access_token;
    21	            currentUser = data.user;
    22	            return { success: true, user: data.user };
    23	        } else {
    24	            currentToken = null;
    25	            currentUser = null;
    26	            const error = await response.json().catch(() => ({ error: 'Login failed' }));
    27	            return { success: false, error: error };
    28	        }
    29	    } catch (e) {
    30	        console.error("Login failed:", e);
    31	        currentToken = null;
    32	        currentUser = null;
    33	        return { success: false, error: 'Network error' };
    34	    }
    35	}
    36	
    37	function getAuthHeaders() {
    38	    return {
    39	        'Authorization': 'Bearer ' + currentToken
    40	    };
    41	}
    42	
    43	async function apiSubmitApplication(phone, reason, leaveDate, files) {
    44	    const formData = new FormData();
    45	    formData.append('contact_phone', phone);
    46	    formData.append('reason', reason);
    47	    formData.append('leave_date', leaveDate);
    48	    files.forEach(f => formData.append('attachments', f));
    49	    
    50	    try {
    51	        const response = await fetch(API_BASE_URL + '/applications/', {
    52	            method: 'POST',
    53	            headers: { 'Authorization': 'Bearer ' + currentToken },
    54	            body: formData
    55	        });
    56	        return response.ok;
    57	    } catch (e) {
    58	        console.error("Submit application failed:", e);
    59	        return false;
    60	    }
    61	}
    62	
    63	async function apiGetApprovals() {
    64	    try {
    65	        const response = await fetch(API_BASE_URL + '/approvals/', {
    66	            headers: getAuthHeaders()
    67	        });
    68	        if (response.ok) {
    69	            return await response.json();
    70	        }
    71	    } catch (e) {
    72	        console.error("Get approvals failed:", e);
    73	    }
    74	    return [];
    75	}
    76	
    77	async function apiApprove(approvalId, comment) {
    78	    try {
    79	        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId + '/approve/', {
    80	            method: 'POST',
    81	            headers: Object.assign({}, getAuthHeaders(), { 'Content-Type': 'application/json' }),
    82	            body: JSON.stringify({ comment: comment })
    83	        });
    84	        return response.ok;
    85	    } catch (e) {
    86	        console.error("Approve failed:", e);
    87	        return false;
    88	    }
    89	}
    90	
    91	async function apiReject(approvalId, comment) {
    92	    try {
    93	        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId + '/reject/', {
    94	            method: 'POST',
    95	            headers: Object.assign({}, getAuthHeaders(), { 'Content-Type': 'application/json' }),
    96	            body: JSON.stringify({ comment: comment })
    97	        });
    98	        return response.ok;
    99	    } catch (e) {
   100	        console.error("Reject failed:", e);
   101	        return false;
   102	    }
   103	}
   104	
   105	async function apiUploadAttachment(applicationId, file, attachmentType = 'other') {
   106	    const formData = new FormData();
   107	    formData.append('file', file);
   108	    formData.append('attachment_type', attachmentType);
   109	
   110	    try {
   111	        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/', {
   112	            method: 'POST',
   113	            headers: getAuthHeaders(),
   114	            body: formData
   115	        });
   116	        if (response.ok) {
   117	            return await response.json();
   118	        }
   119	    } catch (e) {
   120	        console.error("Upload attachment failed:", e);
   121	    }
   122	    return null;
   123	}
   124	
   125	async function apiGetAttachments(applicationId) {
   126	    try {
   127	        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/', {
   128	            headers: getAuthHeaders()
   129	        });
   130	        if (response.ok) {
   131	            return await response.json();
   132	        }
   133	    } catch (e) {
   134	        console.error("Get attachments failed:", e);
   135	    }
   136	    return [];
   137	}
   138	
   139	async function apiDeleteAttachment(applicationId, attachmentId) {
   140	    try {
   141	        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/' + attachmentId + '/', {
   142	            method: 'DELETE',
   143	            headers: getAuthHeaders()
   144	        });
   145	        return response.ok;
   146	    } catch (e) {
   147	        console.error("Delete attachment failed:", e);
   148	        return false;
   149	    }
   150	}

exec
/bin/bash -lc "rtk nl -ba miniprogram/types/api.ts | rtk sed -n '1,90p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	// API Types based on v0.2 Contract
     2	// Generated: 2026-05-31
     3	
     4	export type UserRole = 'student' | 'dorm_manager' | 'counselor' | 'dean' | 'admin';
     5	
     6	export type ApplicationStatus =
     7	  | 'draft'
     8	  | 'pending_dorm_manager'
     9	  | 'pending_counselor'
    10	  | 'approved'
    11	  | 'rejected';
    12	
    13	export type ApprovalDecision = 'pending' | 'approved' | 'rejected';
    14	
    15	export type ApprovalStep = 'dorm_manager' | 'counselor';
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

exec
/bin/bash -lc "rtk nl -ba docs/PROJECT-SUMMARY.md | rtk sed -n '4060,4165p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
  4060	- ✓ 5轮讨论达成共识（部分轮次Gemini超时，但Codex响应完整）
  4061	- ✓ 识别8个问题（3个P1 + 5个Blocking）
  4062	- ✓ 优先级排序：Blocking问题优先于P1问题
  4063	
  4064	**P1问题修复（非阻塞性）:**
  4065	1. ✓ P1-1: 时间线结构完整性 - 验证通过，无需修改
  4066	2. ✓ P1-2: 角色选择器初始化不一致 - 调整selector顺序，dorm_manager置顶
  4067	3. ✓ P1-3: Dean角色标签一致性 - 验证通过，已正确显示"备案查询"
  4068	
  4069	**Blocking问题修复（生产阻塞）:**
  4070	1. ✓ Blocking-1: 硬编码API_BASE_URL - 改为相对路径'/api'，支持部署灵活性
  4071	2. ✓ Blocking-2: TestAccounts明文凭证 - 移除前端密码，切换到后端demo-login端点
  4072	3. ✓ Blocking-3: 阻塞式alert() - 替换为非阻塞Toast通知组件
  4073	4. ✓ Blocking-4: 表单验证不足 - 增强手机号/原因/日期验证
  4074	5. ✓ Blocking-5: 375px宽度限制 - 改为width:100%，支持现代大屏设备
  4075	
  4076	**技术实现:**
  4077	
  4078	*认证重构（Blocking-2）:*
  4079	- 移除TestAccounts对象（含明文密码）
  4080	- apiLogin仅传递role到/api/auth/demo-login
  4081	- 后端按DEMO_AUTH_ENABLED控制演示登录
  4082	- 生产环境必须禁用demo-login（返回404/403）
  4083	
  4084	*Toast通知系统（Blocking-3）:*
  4085	```css
  4086	.toast-container { position: fixed; top: 20px; z-index: 9999; }
  4087	.toast.success { background: var(--status-success); }
  4088	.toast.error { background: var(--status-error); }
  4089	```
  4090	
  4091	*表单验证增强（Blocking-4）:*
  4092	- 手机号格式验证（11位，1开头）
  4093	- 原因长度限制（≤500字）
  4094	- 离校日期验证（≥今天）
  4095	
  4096	*响应式布局修复（Blocking-5）:*
  4097	- 从max-width:375px改为width:100%
  4098	- 支持现代大屏手机（iPhone 15 Pro Max等）
  4099	
  4100	**提交记录:**
  4101	1. feat(demo-web): P1-2和Blocking-5修复 (角色选择器+响应式宽度)
  4102	2. fix(demo-web): Blocking-1和Blocking-4修复 (API路径+表单验证)
  4103	3. feat(demo-web): Blocking-3修复-Toast通知系统 (替换alert)
  4104	4. fix(demo-web): Blocking-2修复-移除TestAccounts (认证重构)
  4105	
  4106	**协作产物:**
  4107	- .omc/collaboration/artifacts/DISCUSS-DEMO-WEB-UI优化-* (8个artifacts)
  4108	- .omc/collaboration/artifacts/DISCUSS-DEMO-WEB认证方案-* (4个artifacts)
  4109	
  4110	**初始验证状态（审计前）:**
  4111	- ✓ 8个UI问题已修复并提交
  4112	- ✓ 代码已推送到远程仓库
  4113	- ⚠️ 声称"生产就绪"但未验证后端集成
  4114	
  4115	### Demo-Web代码审计（2026-06-07下午，三方协作）
  4116	
  4117	**审计背景:**
  4118	- 使用Claude-Codex-Gemini三方协作对8个修复进行验证
  4119	- 5轮讨论，Codex和Gemini达成共识
  4120	- 目标：验证修复的正确性，确认无遗漏问题
  4121	
  4122	**审计发现（5个阻塞问题）:**
  4123	1. ❌ **后端缺失demo-login端点** - 前端调用但后端未实现，认证流程完全中断
  4124	2. ❌ **审批列表数据契约不匹配** - 前端期望嵌套结构，后端返回扁平结构
  4125	3. ❌ **审批详情数据契约不匹配** - 前端期望student_name等字段，后端未提供
  4126	4. ❌ **时间线硬编码HTML** - 未使用API数据动态渲染
  4127	5. ❌ **文档过早宣称就绪** - 声称生产就绪但存在阻塞问题
  4128	
  4129	**审计结论:**
  4130	- UI修复已实现（Toast、表单验证、响应式布局等）
  4131	- 但后端集成问题导致demo-web**无法实际工作**
  4132	- 8个UI修复无法被验证，因为系统根本跑不起来
  4133	
  4134	**集成修复（2026-06-07晚）:**
  4135	
  4136	*Task #15: 实现demo-login端点*
  4137	- ✓ 后端新增POST /api/auth/demo-login
  4138	- ✓ DemoLoginSerializer接收role，返回对应演示用户token
  4139	- ✓ DEMO_AUTH_ENABLED环境变量守卫（生产环境=false）
  4140	- ✓ 角色映射：student→2020001, dorm_manager→M001, counselor→T001, dean→D001
  4141	
  4142	*Task #16: 修复审批列表数据契约*
  4143	- ✓ 新增ApplicationBriefSerializer提供嵌套application对象
  4144	- ✓ ApprovalListSerializer返回{id, application:{id, status}, ...}
  4145	- ✓ 前端`approval.application.status`现在可正常访问
  4146	
  4147	*Task #17: 修复审批详情数据契约*
  4148	- ✓ ApprovalSerializer新增student_name, student_id, contact_phone, reason字段
  4149	- ✓ 前端详情页面现在可正确显示学生信息
  4150	
  4151	**当前状态:**
  4152	- ✓ 认证流程已打通（demo-login端点实现）
  4153	- ✓ 审批列表可正确渲染（数据契约修复）
  4154	- ✓ 审批详情可正确显示（数据契约修复）
  4155	- ⏳ 时间线仍为硬编码HTML（待实现动态渲染）
  4156	- ⏳ 需端到端测试验证完整流程
  4157	
  4158	**下一步:**
  4159	- [ ] Task #18: 实现动态时间线渲染
  4160	- [ ] 端到端集成测试
  4161	- [ ] 用户验收测试（UAT）
  4162	
  4163	
  4164	### 登录设计修复及审计（2026-06-07下午）
  4165	

codex
这里有一个明显不一致：项目总结声称前端只传 role 到 `/api/auth/demo-login`，但当前 `demo-web/js/api.js` 仍传 `user_id/password` 到 `/api/auth/login`。我会把它作为架构/契约发现，但安全结论仍以这次审计的三个后端文件为主。
exec
/bin/bash -lc "rtk rg -n \"apiLogin\\(|role|loginRole|demo-login|TestAccounts|loginUserId|loginPassword\" demo-web/index.html demo-web/js -S" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
demo-web/index.html:390:          <input id="loginUserId" type="text" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入用户ID（如 2020001）" required>
demo-web/index.html:394:          <input id="loginPassword" type="password" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入密码" required>
demo-web/index.html:466:      <div style="font-size: 12px; color: #999;" id="role-display">宿管员</div>
demo-web/index.html:608:      const userId = document.getElementById('loginUserId').value.trim();
demo-web/index.html:609:      const password = document.getElementById('loginPassword').value.trim();
demo-web/index.html:618:      const result = await apiLogin(userId, password);
demo-web/index.html:622:        document.getElementById('loginUserId').value = '';
demo-web/index.html:623:        document.getElementById('loginPassword').value = '';
demo-web/index.html:628:        const roleMap = {
demo-web/index.html:634:        document.getElementById('currentUserRole').textContent = '(' + (roleMap[result.user.role] || result.user.role) + ')';
demo-web/index.html:636:        // Update UI based on role
demo-web/index.html:637:        updateUIForRole(result.user.role);
demo-web/index.html:641:        if (result.user.role === 'student') {
demo-web/index.html:653:    function updateUIForRole(role) {
demo-web/index.html:654:      const isStudent = role === 'student';
demo-web/index.html:655:      const isDean = role === 'dean';
demo-web/index.html:660:      // Update list page title and role display
demo-web/index.html:662:      document.getElementById('role-display').textContent = (isStudent ? '学生' : isDean ? '学工部' : role === 'counselor' ? '辅导员' : '宿管员');
demo-web/js/api.js:7:async function apiLogin(userId, password) {

exec
/bin/bash -lc "rtk nl -ba backend/apps/users/views.py | rtk sed -n '1,120p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	import os
     2	from rest_framework import status
     3	from rest_framework.decorators import api_view, permission_classes
     4	from rest_framework.permissions import AllowAny
     5	from rest_framework.response import Response
     6	from drf_spectacular.utils import extend_schema, OpenApiResponse
     7	from .serializers import LoginSerializer, LoginResponseSerializer, DemoLoginSerializer
     8	
     9	
    10	@extend_schema(
    11	    operation_id='auth_login',
    12	    summary='用户登录',
    13	    description='使用用户ID和密码登录，返回JWT access token',
    14	    request=LoginSerializer,
    15	    responses={
    16	        200: OpenApiResponse(
    17	            response=LoginResponseSerializer,
    18	            description='登录成功，返回access token和用户信息'
    19	        ),
    20	        400: OpenApiResponse(
    21	            description='登录失败：DRF默认ValidationError格式（非项目envelope）'
    22	        ),
    23	    },
    24	    tags=['认证']
    25	)
    26	@api_view(['POST'])
    27	@permission_classes([AllowAny])
    28	def login(request):
    29	    serializer = LoginSerializer(data=request.data)
    30	    if serializer.is_valid():
    31	        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    32	    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    33	
    34	
    35	@extend_schema(
    36	    operation_id='auth_demo_login',
    37	    summary='演示登录（仅开发/演示环境）',
    38	    description='按角色快速登录演示账号。生产环境必须禁用（DEMO_AUTH_ENABLED=false）。',
    39	    request=DemoLoginSerializer,
    40	    responses={
    41	        200: OpenApiResponse(
    42	            response=LoginResponseSerializer,
    43	            description='登录成功，返回access token和用户信息'
    44	        ),
    45	        403: OpenApiResponse(
    46	            description='演示登录已禁用'
    47	        ),
    48	        400: OpenApiResponse(
    49	            description='无效的角色或演示用户不存在'
    50	        ),
    51	    },
    52	    tags=['认证']
    53	)
    54	@api_view(['POST'])
    55	@permission_classes([AllowAny])
    56	def demo_login(request):
    57	    # 生产环境守卫
    58	    if os.environ.get('DEMO_AUTH_ENABLED', 'false').lower() != 'true':
    59	        return Response({'error': 'Demo login is disabled'}, status=status.HTTP_403_FORBIDDEN)
    60	
    61	    serializer = DemoLoginSerializer(data=request.data)
    62	    if serializer.is_valid():
    63	        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    64	    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

exec
/bin/bash -lc "rtk nl -ba backend/apps/users/urls.py | rtk sed -n '1,80p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.urls import path
     2	from . import views
     3	
     4	urlpatterns = [
     5	    path('login', views.login, name='login'),
     6	    path('demo-login', views.demo_login, name='demo_login'),
     7	]

exec
/bin/bash -lc "rtk nl -ba backend/apps/users/serializers.py | rtk sed -n '1,120p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from rest_framework import serializers
     2	from rest_framework_simplejwt.tokens import RefreshToken
     3	from .models import User
     4	
     5	
     6	class UserSerializer(serializers.ModelSerializer):
     7	    class Meta:
     8	        model = User
     9	        fields = ['user_id', 'name', 'role', 'class_id', 'active', 'is_graduating', 'graduation_year']
    10	        read_only_fields = ['user_id']
    11	
    12	
    13	class AuthUserSerializer(serializers.ModelSerializer):
    14	    """登录响应中的用户摘要（UserDTO子集）"""
    15	    class Meta:
    16	        model = User
    17	        fields = ['user_id', 'name', 'role', 'class_id']
    18	
    19	
    20	class LoginSerializer(serializers.Serializer):
    21	    user_id = serializers.CharField()
    22	    password = serializers.CharField(write_only=True)
    23	
    24	    def validate(self, attrs):
    25	        user_id = attrs.get('user_id')
    26	        password = attrs.get('password')
    27	
    28	        try:
    29	            user = User.objects.get(user_id=user_id)
    30	        except User.DoesNotExist:
    31	            raise serializers.ValidationError('Invalid credentials')
    32	
    33	        if not user.check_password(password):
    34	            raise serializers.ValidationError('Invalid credentials')
    35	
    36	        if not user.active:
    37	            raise serializers.ValidationError('Account is inactive')
    38	
    39	        refresh = RefreshToken.for_user(user)
    40	
    41	        return {
    42	            'access_token': str(refresh.access_token),
    43	            'token_type': 'Bearer',
    44	            'user': AuthUserSerializer(user).data
    45	        }
    46	
    47	
    48	class LoginResponseSerializer(serializers.Serializer):
    49	    """登录成功响应（schema-only，用于OpenAPI文档）"""
    50	    access_token = serializers.CharField(help_text="JWT access token")
    51	    token_type = serializers.CharField(default='Bearer', help_text="Token type")
    52	    user = AuthUserSerializer(help_text="用户信息")
    53	
    54	
    55	class DemoLoginSerializer(serializers.Serializer):
    56	    """演示登录（仅在DEMO_AUTH_ENABLED=true时启用）"""
    57	    role = serializers.ChoiceField(choices=['student', 'dorm_manager', 'counselor', 'dean'])
    58	
    59	    # 角色到演示用户映射
    60	    DEMO_USERS = {
    61	        'student': '2020001',
    62	        'dorm_manager': 'M001',
    63	        'counselor': 'T001',
    64	        'dean': 'D001',
    65	    }
    66	
    67	    def validate(self, attrs):
    68	        role = attrs.get('role')
    69	        user_id = self.DEMO_USERS.get(role)
    70	
    71	        try:
    72	            user = User.objects.get(user_id=user_id)
    73	        except User.DoesNotExist:
    74	            raise serializers.ValidationError(f'Demo user for role {role} not found')
    75	
    76	        if not user.active:
    77	            raise serializers.ValidationError('Demo account is inactive')
    78	
    79	        refresh = RefreshToken.for_user(user)
    80	
    81	        return {
    82	            'access_token': str(refresh.access_token),
    83	            'token_type': 'Bearer',
    84	            'user': AuthUserSerializer(user).data
    85	        }

codex
我已经有足够证据做审查结论。最后做一次 Django 配置检查和 demo-login 相关测试搜索，确认没有已有测试把生产误启用挡住。
exec
/bin/bash -lc 'rtk find backend/apps/users/tests -maxdepth 2 -type f -print' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
rtk find: unknown flag '-print', ignored
5F 1D:

./ __init__.py test_import_csv.py test_xg_user_client.py test_xg_user_mapper.py test_xg_user_sync.py

exec
/bin/bash -lc 'rtk python backend/manage.py check --deploy --settings=config.settings.prod' in /home/caohui/projects/graduation-leave-system
 exited 127 in 0ms:
[rtk: No such file or directory (os error 2)]

exec
/bin/bash -lc "rtk sed -n '1,80p' backend/config/settings/__init__.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Settings package

codex
配置检查命令第一次因为工作目录/解释器路径没有跑起来；我会从 `backend` 目录用项目可用的 Python 再执行一次。
exec
/bin/bash -lc 'rtk ls -la backend' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
.omc/
.pytest_cache/
__pycache__/
apps/
backend/
config/
data/
docs/
media/
plans/
reports/
requirements/
scripts/
utils/
venv/
.env  374B
.env.example  761B
Dockerfile  493B
app -> /app  4B
manage.py  666B
requirements.txt  333B
schema.py  739B

exec
/bin/bash -lc 'rtk which python3' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
/usr/bin/python3

exec
/bin/bash -lc 'rtk python3 manage.py check --deploy --settings=config.settings.prod' in /home/caohui/projects/graduation-leave-system/backend
 exited 1 in 204ms:
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

codex
系统 Python 没装 Django；仓库有 `backend/venv`，我用这个环境跑部署检查。
exec
/bin/bash -lc 'rtk venv/bin/python manage.py check --deploy --settings=config.settings.prod' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 425ms:
System check identified some issues:

WARNINGS:
?: (drf_spectacular.W001) /home/caohui/projects/graduation-leave-system/backend/apps/applications/serializers.py: Warning [applications_view > ApplicationSerializer]: unable to resolve type hint for function "get_approvals". Consider using a type hint or @extend_schema_field. Defaulting to string.
?: (drf_spectacular.W002) /home/caohui/projects/graduation-leave-system/backend/apps/applications/views.py: Error [get_or_create_draft]: unable to guess serializer. This is graceful fallback handling for APIViews. Consider using GenericAPIView as view base class, if view is under your control. Either way you may want to add a serializer_class (or method). Ignoring view for now.
?: (drf_spectacular.W002) /home/caohui/projects/graduation-leave-system/backend/apps/notifications/views.py: Error [mark_as_read]: unable to guess serializer. This is graceful fallback handling for APIViews. Consider using GenericAPIView as view base class, if view is under your control. Either way you may want to add a serializer_class (or method). Ignoring view for now.
?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting. If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security. Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.
?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
?: (security.W009) Your SECRET_KEY has less than 50 characters, less than 5 unique characters, or it's prefixed with 'django-insecure-' indicating that it was generated automatically by Django. Please generate a long and random value, otherwise many of Django's security-critical features will be vulnerable to attack.
?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.

System check identified 8 issues (0 silenced).

codex
部署检查也暴露了生产安全基线缺口，特别是 `SECRET_KEY` 默认弱值和 HTTPS cookie 设置默认关闭。这些不是 demo-login 文件本身，但会影响 JWT 安全结论。
exec
/bin/bash -lc 'rtk git diff -- backend/apps/users/views.py backend/apps/users/serializers.py backend/apps/users/urls.py backend/config/settings/base.py backend/config/settings/prod.py demo-web/js/api.js demo-web/index.html' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
exec
/bin/bash -lc "rtk nl -ba backend/apps/users/management/commands/seed_data.py | rtk sed -n '1,130p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	from django.core.management.base import BaseCommand
     2	from apps.users.models import User, UserRole
     3	
     4	
     5	class Command(BaseCommand):
     6	    help = 'Load seed data for users'
     7	
     8	    def add_arguments(self, parser):
     9	        parser.add_argument(
    10	            '--reset',
    11	            action='store_true',
    12	            help='Clear applications and approvals before loading seed data',
    13	        )
    14	
    15	    def handle(self, *args, **options):
    16	        if options['reset']:
    17	            self.stdout.write('Resetting applications and approvals...')
    18	            from apps.applications.models import Application
    19	            from apps.approvals.models import Approval
    20	            Approval.objects.all().delete()
    21	            Application.objects.all().delete()
    22	            self.stdout.write(self.style.SUCCESS('Reset complete'))
    23	
    24	        self.stdout.write('Loading seed data...')
    25	
    26	        # Students (10)
    27	        students = [
    28	            {'user_id': '2020001', 'name': '张三', 'class_id': 'CS2020-01', 'building': '1号楼', 'department': '计算机学院'},
    29	            {'user_id': '2020002', 'name': '李四', 'class_id': 'CS2020-02', 'building': '2号楼', 'department': '软件学院'},
    30	            {'user_id': '2020003', 'name': '王五', 'class_id': 'CS2020-01', 'building': '1号楼', 'department': '计算机学院'},
    31	            {'user_id': '2020004', 'name': '赵六', 'class_id': 'CS2020-01', 'building': '1号楼', 'department': '计算机学院'},
    32	            {'user_id': '2020005', 'name': '孙七', 'class_id': 'CS2020-01', 'building': '1号楼', 'department': '计算机学院'},
    33	            {'user_id': '2020006', 'name': '周八', 'class_id': 'CS2020-02', 'building': '2号楼', 'department': '软件学院'},
    34	            {'user_id': '2020007', 'name': '吴九', 'class_id': 'CS2020-02', 'building': '2号楼', 'department': '软件学院'},
    35	            {'user_id': '2020008', 'name': '郑十', 'class_id': 'CS2020-02', 'building': '2号楼', 'department': '软件学院'},
    36	            {'user_id': '2020009', 'name': '王十一', 'class_id': 'CS2020-02', 'building': '2号楼', 'department': '软件学院'},
    37	            {'user_id': '2020010', 'name': '王十二', 'class_id': 'CS2020-02', 'building': '2号楼', 'department': '软件学院'},
    38	        ]
    39	
    40	        for student_data in students:
    41	            user, created = User.objects.update_or_create(
    42	                user_id=student_data['user_id'],
    43	                defaults={
    44	                    'name': student_data['name'],
    45	                    'role': UserRole.STUDENT,
    46	                    'class_id': student_data['class_id'],
    47	                    'building': student_data.get('building'),
    48	                    'department': student_data.get('department'),
    49	                    'is_graduating': True,
    50	                    'graduation_year': 2024,
    51	                    'active': True,
    52	                }
    53	            )
    54	            if created:
    55	                user.set_password(student_data['user_id'])
    56	                user.save()
    57	            self.stdout.write(f'{"Created" if created else "Updated"} student: {user.user_id}')
    58	
    59	        # Counselors (2)
    60	        counselors = [
    61	            {'user_id': 'T001', 'name': '李老师', 'department': '计算机学院'},
    62	            {'user_id': 'T002', 'name': '王老师', 'department': '软件学院'},
    63	        ]
    64	
    65	        for counselor_data in counselors:
    66	            user, created = User.objects.get_or_create(
    67	                user_id=counselor_data['user_id'],
    68	                defaults={
    69	                    'name': counselor_data['name'],
    70	                    'role': UserRole.COUNSELOR,
    71	                    'department': counselor_data.get('department'),
    72	                    'active': True,
    73	                }
    74	            )
    75	            if created:
    76	                user.set_password(counselor_data['user_id'])
    77	                user.save()
    78	                self.stdout.write(f'Created counselor: {user.user_id}')
    79	
    80	        # Dorm managers (3)
    81	        dorm_managers = [
    82	            {'user_id': 'M001', 'name': '宿管员1', 'building': '1号楼'},
    83	            {'user_id': 'M002', 'name': '宿管员2', 'building': '2号楼'},
    84	            {'user_id': 'M003', 'name': '宿管员3', 'building': '1号楼'},
    85	        ]
    86	
    87	        for dm_data in dorm_managers:
    88	            user, created = User.objects.update_or_create(
    89	                user_id=dm_data['user_id'],
    90	                defaults={
    91	                    'name': dm_data['name'],
    92	                    'role': UserRole.DORM_MANAGER,
    93	                    'building': dm_data.get('building'),
    94	                    'active': True,
    95	                }
    96	            )
    97	            if created:
    98	                user.set_password(dm_data['user_id'])
    99	                user.save()
   100	                self.stdout.write(f'Created dorm_manager: {user.user_id}')
   101	
   102	        # Dean (1)
   103	        user, created = User.objects.get_or_create(
   104	            user_id='D001',
   105	            defaults={
   106	                'name': '赵主任',
   107	                'role': UserRole.DEAN,
   108	                'active': True,
   109	            }
   110	        )
   111	        if created:
   112	            user.set_password('D001')
   113	            user.save()
   114	            self.stdout.write(f'Created dean: {user.user_id}')
   115	
   116	        self.stdout.write(self.style.SUCCESS('Seed data loaded successfully'))

exec
/bin/bash -lc 'rtk rg -n "''^DEMO_AUTH_ENABLED|''^DJANGO_SETTINGS_MODULE|''^DEBUG|''^SECRET_KEY|''^SECURE_SSL_REDIRECT|''^SESSION_COOKIE_SECURE|''^CSRF_COOKIE_SECURE" backend/.env backend/.env.example -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/.env:1:SECRET_KEY=django-insecure-dev-key-please-change-in-production
backend/.env:2:DEBUG=True
backend/.env:14:DEMO_AUTH_ENABLED=true
backend/.env.example:23:DEMO_AUTH_ENABLED=false

codex
**Findings**
P0 - demo-login 可在生产被一个环境变量直接打开，属于生产阻塞  
位置：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:54)、[prod.py](/home/caohui/projects/graduation-leave-system/backend/config/settings/prod.py:4)、[urls.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/urls.py:6)  
`demo_login` 是 `AllowAny`，路由在所有环境无条件挂载，只检查 `os.environ.get('DEMO_AUTH_ENABLED') == 'true'`。`prod.py` 没有强制覆盖或启动失败保护；如果生产环境、容器镜像或 `.env` 中误设为 true，任何人可无密码获取 student/dorm_manager/counselor/dean JWT。当前本地 `backend/.env` 也存在 `DEMO_AUTH_ENABLED=true`，说明误带配置的风险不是理论问题。  
修复：生产 settings 中强制 `DEMO_AUTH_ENABLED = False`，并在启动时加 fail-fast：`if not DEBUG and DEMO_AUTH_ENABLED: raise ImproperlyConfigured(...)`。更好的是生产 URLconf 不挂载该路由，或返回 404。

P0 - JWT 签名密钥允许使用弱默认值，生产可启动  
位置：[base.py](/home/caohui/projects/graduation-leave-system/backend/config/settings/base.py:11)、[base.py](/home/caohui/projects/graduation-leave-system/backend/config/settings/base.py:146)  
`SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY`，但 `SECRET_KEY` 有可用默认值，`prod.py` 未强制要求真实密钥。`manage.py check --deploy --settings=config.settings.prod` 已提示 SECRET_KEY 弱值风险。若生产使用默认/开发密钥，攻击者可伪造 JWT，影响高于 demo-login。  
修复：生产环境必须缺失即失败，不允许默认 SECRET_KEY；JWT 签名密钥建议独立配置为 `JWT_SIGNING_KEY`，并强制长度/随机性校验。

P1 - demo-login 绑定真实固定账号，没有 demo-only 边界  
位置：[serializers.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/serializers.py:55)、[seed_data.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/management/commands/seed_data.py:40)  
`DemoLoginSerializer` 直接把 role 映射到真实 `User` 表里的固定 ID：`2020001/M001/T001/D001`。这些账号也是 seed/test 文档中的真实工作流账号，且默认密码等于 ID。只要这些账号进入生产库，demo-login 一旦开启就是对真实权限账号的无密码接管。  
修复：增加 `is_demo_account` 或单独 demo 用户表/租户；serializer 必须校验 `user.role == requested_role` 且 `user.is_demo_account is True`；生产导入脚本不得创建这些 demo 账号为 active。

P1 - 认证端点无节流/审计，普通登录可被暴力尝试  
位置：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:26)、[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:54)、[base.py](/home/caohui/projects/graduation-leave-system/backend/config/settings/base.py:113)  
`login` 和 `demo_login` 都是 `AllowAny`，REST_FRAMEWORK 未配置 throttle。普通登录没有账号/IP 级限速；demo-login 一旦开启也没有审计记录。  
修复：配置 DRF throttle，至少对 auth endpoints 使用 stricter scope；记录 demo-login 使用日志，包括 role、IP、UA、时间。

P1 - access token 生命周期过长且无撤销能力  
位置：[base.py](/home/caohui/projects/graduation-leave-system/backend/config/settings/base.py:140)、[serializers.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/serializers.py:39)  
access token 有效期 24 小时，响应只返回 access token，没有 refresh/logout/blacklist 机制。泄露后 24 小时内无法服务端撤销。对 dean/counselor 这类权限账号不合适。  
修复：生产 access token 缩短到 5-15 分钟；引入 refresh token rotation/blacklist 或明确无状态 JWT 风险接受；必要时增加 token version/jti denylist。

P1 - 错误响应契约不一致，前后端和 OpenAPI 易漂移  
位置：[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:20)、[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:58)、[views.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:64)  
其他业务接口使用 `{'error': {'code', 'message', 'details'}}`，但登录失败返回 DRF serializer errors，demo-login 禁用返回 `{'error': 'Demo login is disabled'}`。这会让前端错误处理和 API schema 不稳定。  
修复：统一 auth 错误 envelope，例如 `DEMO_LOGIN_DISABLED`、`VALIDATION_ERROR`、`INVALID_CREDENTIALS`。

P1 - 当前 demo-web 与声称契约不一致  
位置：[api.js](/home/caohui/projects/graduation-leave-system/demo-web/js/api.js:7)、[index.html](/home/caohui/projects/graduation-leave-system/demo-web/index.html:608)  
项目总结声称前端调用 `/api/auth/demo-login` 并只传 role，但当前代码仍读取 `user_id/password` 并调用 `/api/auth/login`。这不是后端三文件自身漏洞，但说明“开发完成/8 个测试通过”没有覆盖真实集成契约。  
修复：要么前端改为 role -> demo-login，要么撤销 demo-login 方案，继续普通登录；两者不能同时声称完成。

**结论**
当前不能认为生产就绪。阻塞项是：demo-login 生产 fail-fast 缺失、JWT/SECRET_KEY 生产基线缺失。8/8 自动化测试没有覆盖这些安全路径。

我执行了 `venv/bin/python manage.py check --deploy --settings=config.settings.prod`，结果有 8 个 warning，包括弱 SECRET_KEY、HTTPS redirect/cookie secure 未启用。建议先补生产安全测试，再谈发布。
tokens used
153,965

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
