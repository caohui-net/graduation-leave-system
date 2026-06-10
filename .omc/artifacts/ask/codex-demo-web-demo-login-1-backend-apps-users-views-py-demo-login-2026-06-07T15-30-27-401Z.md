# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-07T15:30:27.401Z

## Original task

代码安全审计：验证demo-web登录和后端demo-login端点生产就绪

**审计文件：**
1. backend/apps/users/views.py（demo_login函数，约150-180行）
2. backend/apps/users/serializers.py（DemoLoginSerializer）
3. demo-web/index.html（apiLogin函数）

**关键问题：**
1. DEMO_AUTH_ENABLED守卫：生产环境是否可能被误启用？默认值是什么？
2. 演示账号映射：硬编码student→2020001等，是否有安全风险？
3. JWT token管理：demo-login返回的token是否安全？
4. 前端登录：明文密码传输？HTTPS必需性？
5. 生产部署检查清单：需要哪些强制配置？

**当前状态：**8/8集成测试通过，声称开发完成

请识别所有P0/P1安全问题，给出具体修复建议。

## Final prompt

代码安全审计：验证demo-web登录和后端demo-login端点生产就绪

**审计文件：**
1. backend/apps/users/views.py（demo_login函数，约150-180行）
2. backend/apps/users/serializers.py（DemoLoginSerializer）
3. demo-web/index.html（apiLogin函数）

**关键问题：**
1. DEMO_AUTH_ENABLED守卫：生产环境是否可能被误启用？默认值是什么？
2. 演示账号映射：硬编码student→2020001等，是否有安全风险？
3. JWT token管理：demo-login返回的token是否安全？
4. 前端登录：明文密码传输？HTTPS必需性？
5. 生产部署检查清单：需要哪些强制配置？

**当前状态：**8/8集成测试通过，声称开发完成

请识别所有P0/P1安全问题，给出具体修复建议。

## Raw output

```text
**审计结论：不建议宣称生产就绪。** 8/8 集成测试通过只能说明流程可用，当前仍有生产阻断级安全风险。

**P0 / 生产阻断**

1. [backend/apps/users/views.py:58](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:58) `DEMO_AUTH_ENABLED` 默认值是 `false`，这一点正确；但 [.env.docker:28](/home/caohui/projects/graduation-leave-system/.env.docker:28) 设置为 `true`，且 [docker-compose.yml:24](/home/caohui/projects/graduation-leave-system/docker-compose.yml:24) 用 `runserver`，会走 [backend/manage.py:9](/home/caohui/projects/graduation-leave-system/backend/manage.py:9) 的 `config.settings.dev`。如果这套 compose 被误用于公网，任何人都能按角色直接领取学生、宿管、辅导员、学工部 JWT。

2. [demo-web/js/api.js:7](/home/caohui/projects/graduation-leave-system/demo-web/js/api.js:7) 当前 `apiLogin` 实际调用的是 `/api/auth/login`，不是 `/api/auth/demo-login`；[demo-web/index.html:398](/home/caohui/projects/graduation-leave-system/demo-web/index.html:398) 仍公开展示演示账号和弱口令。如果这些账号存在于生产库且密码未改，这就是公开后门。

3. JWT 使用 [backend/config/settings/base.py:146](/home/caohui/projects/graduation-leave-system/backend/config/settings/base.py:146) 的 `SECRET_KEY` 签名，而默认值是 [backend/config/settings/base.py:11](/home/caohui/projects/graduation-leave-system/backend/config/settings/base.py:11) 的固定开发密钥，`.env.docker` 也使用固定弱密钥。生产若未强制替换，JWT 可被伪造。

4. HTTPS 不是强制项：[backend/config/settings/prod.py:7](/home/caohui/projects/graduation-leave-system/backend/config/settings/prod.py:7) `SECURE_SSL_REDIRECT` 默认 `false`。当前登录会发送密码，后续请求会发送 Bearer token；生产 HTTP 下等同明文暴露凭证和 token。

**P1 / 高风险**

1. [backend/apps/users/serializers.py:60](/home/caohui/projects/graduation-leave-system/backend/apps/users/serializers.py:60) 硬编码 `student -> 2020001` 等不是秘密本身，但风险在于它把公开 role 映射到真实高权限账号。建议增加 `is_demo` 标记或独立 demo 用户表，并校验 `user.is_demo=True`，禁止映射到真实业务账号。

2. [backend/apps/users/views.py:55](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:55) `demo_login` 是 `AllowAny` 且无 throttle/audit。即使只在演示环境，也应限制频率、记录 role/IP/User-Agent，并在启用时明确打启动告警。

3. [backend/config/settings/base.py:141](/home/caohui/projects/graduation-leave-system/backend/config/settings/base.py:141) access token 24 小时偏长，且前端没有刷新/失效处理。demo-login 返回的是标准 access token，本身生成方式可接受，但生产建议 15-60 分钟、强密钥、必要时启用 token blacklist 或短会话策略。

4. `demo-web/index.html` 多处把后端字段拼接进 `innerHTML`，例如申请人、原因、意见等。如果后端数据可被用户提交，会形成存储型 XSS；因为 token 在 JS 内存变量 `currentToken` 中，XSS 可直接发起已认证请求。应统一使用 `textContent` 或 HTML escaping。

**必须修复建议**

- 生产启动时强制断言：`DEBUG=False`、`DEMO_AUTH_ENABLED != true`、`SECRET_KEY` 非默认、`ALLOWED_HOSTS` 非通配、HTTPS 开关启用。
- 将 `DEMO_AUTH_ENABLED` 移入 Django settings，并在 `prod.py` 中硬禁止：生产环境检测到 true 直接启动失败。
- 删除生产包中的 demo-web 演示账号提示，或只在明确 demo build 中展示。
- 演示账号与真实账号隔离，增加 `is_demo` 校验；高权限 demo 账号不得存在于生产库。
- 生产启用 HTTPS/HSTS/secure cookies/proxy SSL header，反向代理只暴露 HTTPS。
- 给 `/api/auth/login` 和 `/api/auth/demo-login` 配置 throttling、审计日志和异常告警。

当前状态可以说“开发/演示环境可用”，不能说“生产就绪”。


OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019ea2b2-f56b-7aa3-8478-fb4530b409c7
--------
user
代码安全审计：验证demo-web登录和后端demo-login端点生产就绪

**审计文件：**
1. backend/apps/users/views.py（demo_login函数，约150-180行）
2. backend/apps/users/serializers.py（DemoLoginSerializer）
3. demo-web/index.html（apiLogin函数）

**关键问题：**
1. DEMO_AUTH_ENABLED守卫：生产环境是否可能被误启用？默认值是什么？
2. 演示账号映射：硬编码student→2020001等，是否有安全风险？
3. JWT token管理：demo-login返回的token是否安全？
4. 前端登录：明文密码传输？HTTPS必需性？
5. 生产部署检查清单：需要哪些强制配置？

**当前状态：**8/8集成测试通过，声称开发完成

请识别所有P0/P1安全问题，给出具体修复建议。
codex
我会按项目的审计协议先读取本地规则，再查看指定代码和相关配置，最后按 P0/P1 风险给出结论和修复建议。
exec
/bin/bash -lc "sed -n '1,240p' docs/codex-review-protocol.md" in /home/caohui/projects/graduation-leave-system
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
规则已读取。接下来我只做审计，不改代码；重点会核对配置默认值、调用链和 token 生成方式，而不是只看这三个函数的表面实现。
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
/bin/bash -lc 'rtk rg -n "DEMO_AUTH_ENABLED|demo_login|demo-login|DemoLoginSerializer|SIMPLE_JWT|JWT|DEBUG|SECURE_SSL|SESSION_COOKIE_SECURE|CSRF_COOKIE_SECURE|CORS|ALLOWED_HOSTS" -S .' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
./DEPLOYMENT.md:94:| `DEBUG` | Enable debug mode | `True` | **No** - Set to `False` in production |
./DEPLOYMENT.md:95:| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `localhost,127.0.0.1` | **Yes** - Set to your domain(s) |
./DEPLOYMENT.md:107:### CORS Settings
./DEPLOYMENT.md:111:| `CORS_ALLOWED_ORIGINS` | Comma-separated list of allowed origins | `http://localhost:3000,http://127.0.0.1:3000` | **Yes** - Set to your frontend URL(s) |
./DEPLOYMENT.md:115:- **JWT Settings:** JWT tokens use `SECRET_KEY` for signing (no separate `JWT_SECRET_KEY` needed)
./DEPLOYMENT.md:117:- **Unused Variables:** `.env.example` may reference `JWT_SECRET_KEY`, `REDIS_URL`, `CELERY_BROKER_URL` - these are not currently read by the application
./DEPLOYMENT.md:174:**401 Unauthorized - JWT Expired**
./DEPLOYMENT.md:178:**Cause:** JWT access token expired (default lifetime: 24 hours)
./backend/requirements.txt:12:# CORS
./demo-web/IMPLEMENTATION_NOTES.md:6:   - Handled JWT token acquisition on role switch.
./docs/api/api-schema-todo.md:15:- JWT Bearer认证配置
./backend/config/settings/base.py:13:DEBUG = config('DEBUG', default=True, cast=bool)
./backend/config/settings/base.py:15:ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])
./backend/config/settings/base.py:115:        'rest_framework_simplejwt.authentication.JWTAuthentication',
./backend/config/settings/base.py:139:# JWT Settings
./backend/config/settings/base.py:140:SIMPLE_JWT = {
./backend/config/settings/base.py:152:# CORS Settings
./backend/config/settings/base.py:153:CORS_ALLOWED_ORIGINS = config(
./backend/config/settings/base.py:154:    'CORS_ALLOWED_ORIGINS',
./backend/config/settings/prod.py:4:DEBUG = False
./backend/config/settings/prod.py:7:SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
./backend/config/settings/prod.py:8:SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
./backend/config/settings/prod.py:9:CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
./backend/config/settings/dev.py:4:DEBUG = True
./backend/config/settings/dev.py:6:ALLOWED_HOSTS = ['*']
./backend/config/settings/dev.py:11:# Disable CORS restrictions in development
./backend/config/settings/dev.py:12:CORS_ALLOW_ALL_ORIGINS = True
./docs/acceptance/phase4c-known-issues.md:93:| 未配置CORS白名单 | 安全风险 | 当前允许所有来源 | 生产环境需限制ALLOWED_HOSTS |
./docs/acceptance/phase4c-known-issues.md:101:1. **立即处理（生产部署前）：** HTTPS、CORS白名单、数据库备份
./docs/用户设计说明书.md:107:- API接口JWT Token认证
./docs/acceptance/phase4c-evidence-index.md:128:- `JWT_SECRET_KEY`：JWT密钥
./docs/acceptance/phase4c-evidence-index.md:129:- `ALLOWED_HOSTS`：允许的域名
./docs/acceptance/phase4c-acceptance-checklist.md:16:| JWT认证 | ✅ 通过 | `backend/apps/users/views.py:login` |
./docs/acceptance/phase4c-acceptance-checklist.md:116:| Django配置 | ✅ 通过 | SECRET_KEY/DEBUG/ALLOWED_HOSTS |
./docs/acceptance/phase4c-acceptance-checklist.md:118:| JWT配置 | ✅ 通过 | JWT_SECRET_KEY/LIFETIME |
./docs/acceptance/phase4c-acceptance-checklist.md:182:| JWT token注入 | ✅ 通过 | Authorization header |
./docs/week3-day0-acceptance-checklist.md:106:- [ ] 登录返回JWT token
./docs/week3-day0-acceptance-checklist.md:112:- 401错误：检查JWT配置
./backend/apps/users/urls.py:6:    path('demo-login', views.demo_login, name='demo_login'),
./docs/PROJECT-SUMMARY.md:254:  - JWT认证系统（login API）
./docs/PROJECT-SUMMARY.md:679:- ✓ JWT token注入 + 401处理
./docs/PROJECT-SUMMARY.md:712:  - JWT token注入 + 401处理
./docs/PROJECT-SUMMARY.md:1323:  - Django配置（SECRET_KEY, DEBUG, ALLOWED_HOSTS）
./docs/PROJECT-SUMMARY.md:1325:  - JWT配置（JWT_SECRET_KEY, JWT_ACCESS_TOKEN_LIFETIME, JWT_REFRESH_TOKEN_LIFETIME）
./docs/PROJECT-SUMMARY.md:1450:  4. Known Residual Risks（8项：并发压测/对象存储/连接池/HTTPS/CORS/日志轮转/数据库备份/监控告警）
./docs/PROJECT-SUMMARY.md:1928:- ✓ 验证JWT Bearer认证可见
./docs/PROJECT-SUMMARY.md:1941:- JWT认证: Bearer JWT ✓
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
./docs/操作说明书-待改进事项.md:78:- 补充日志级别说明（DEBUG/INFO/WARNING/ERROR）
./docs/SYSTEM-OPERATIONS-GUIDE.md:23:- 认证：JWT (SimpleJWT)
./docs/SYSTEM-OPERATIONS-GUIDE.md:65:# 预期返回：JWT token
./docs/SYSTEM-OPERATIONS-GUIDE.md:307:DEBUG=True
./docs/SYSTEM-OPERATIONS-GUIDE.md:308:ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
./docs/SYSTEM-OPERATIONS-GUIDE.md:310:# JWT配置
./docs/SYSTEM-OPERATIONS-GUIDE.md:311:JWT_SECRET_KEY=<生产环境需更换>
./docs/SYSTEM-OPERATIONS-GUIDE.md:312:JWT_ACCESS_TOKEN_LIFETIME=3600
./docs/SYSTEM-OPERATIONS-GUIDE.md:313:JWT_REFRESH_TOKEN_LIFETIME=86400
./docs/SYSTEM-OPERATIONS-GUIDE.md:319:1. 更换SECRET_KEY和JWT_SECRET_KEY为随机字符串
./docs/SYSTEM-OPERATIONS-GUIDE.md:320:2. 设置DEBUG=False
./docs/SYSTEM-OPERATIONS-GUIDE.md:321:3. 配置ALLOWED_HOSTS为实际域名
./docs/SYSTEM-OPERATIONS-GUIDE.md:373:**问题：** JWT认证失败
./backend/apps/users/views.py:7:from .serializers import LoginSerializer, LoginResponseSerializer, DemoLoginSerializer
./backend/apps/users/views.py:13:    description='使用用户ID和密码登录，返回JWT access token',
./backend/apps/users/views.py:36:    operation_id='auth_demo_login',
./backend/apps/users/views.py:38:    description='按角色快速登录演示账号。生产环境必须禁用（DEMO_AUTH_ENABLED=false）。',
./backend/apps/users/views.py:39:    request=DemoLoginSerializer,
./backend/apps/users/views.py:56:def demo_login(request):
./backend/apps/users/views.py:58:    if os.environ.get('DEMO_AUTH_ENABLED', 'false').lower() != 'true':
./backend/apps/users/views.py:61:    serializer = DemoLoginSerializer(data=request.data)
./docs/COMPLETION-STATUS.md:41:- **认证授权：** JWT + RBAC权限模型完成
./docs/COMPLETION-STATUS.md:73:- W008: SECURE_SSL_REDIRECT 未启用
./docs/COMPLETION-STATUS.md:75:- W012: SESSION_COOKIE_SECURE 未启用
./docs/COMPLETION-STATUS.md:76:- W016: CSRF_COOKIE_SECURE 未启用
./docs/design/2026-05-27-system-design.md:122:- djangorestframework-simplejwt（JWT令牌）
./docs/design/2026-05-27-system-design.md:190:   - JWT令牌生成和验证
./docs/design/2026-05-27-system-design.md:648:- JWT Token认证
./docs/design/2026-05-27-system-design.md:1251:用户输入学号+密码 → 后端验证 → 生成JWT Token → 返回Token
./docs/design/2026-05-27-system-design.md:1277:### 4.2 JWT Token设计
./docs/design/2026-05-27-system-design.md:1284:    "typ": "JWT"
./docs/design/2026-05-27-system-design.md:1930:- API使用JWT Token，豁免CSRF
./docs/design/2026-05-27-system-design.md:1954:SECURE_SSL_REDIRECT = True
./docs/design/2026-05-27-system-design.md:1955:SESSION_COOKIE_SECURE = True
./docs/design/2026-05-27-system-design.md:1956:CSRF_COOKIE_SECURE = True
./docs/design/2026-05-27-system-design.md:1970:- JWT签名算法：HS256
./docs/superpowers/plans/2026-05-27-implementation-plan.md:256:- ✓ 学号密码登录成功，返回JWT Token
./docs/week3-day0-environment-strategy.md:63:   - DEBUG模式配置
./docs/test-reports/comprehensive-test-2026-06-07.md:81:- ✅ 用户身份认证（JWT令牌生成）
./docs/test-reports/comprehensive-test-2026-06-07.md:140:- ✅ JWT令牌生成（5/5）
./docs/test-reports/comprehensive-test-corrected-2026-06-07.md:57:- ✅ 用户身份认证（JWT令牌生成）
./docs/plans/week-0-1-execution-plan.md:64:- [ ] 薄认证实现（学号/工号 + 密码，JWT）
./docs/plans/week-0-1-execution-plan.md:76:- [ ] 登录API返回JWT token
./docs/test-reports/multi-role-test-2026-06-07.md:47:- **预期结果:** 返回200状态码和JWT访问令牌
./docs/test-reports/multi-role-test-2026-06-07.md:106:- [x] JWT令牌生成 (5/5)
./docs/test-reports/multi-role-test-2026-06-07.md:174:本次测试成功验证了系统支持多种用户角色的身份认证功能，包括学生、辅导员、宿管和管理员4种角色。所有用户均能成功登录并获取JWT令牌。
./docs/test-reports/workflow-test-2026-06-07.md:51:- **预期结果:** 返回200状态码和JWT访问令牌
./docs/test-reports/workflow-test-2026-06-07.md:87:1. **身份认证:** 5名学生均成功登录，获取有效JWT令牌
./docs/test-reports/workflow-test-2026-06-07.md:116:- [x] 用户身份认证 (JWT令牌生成)
./backend/apps/users/serializers.py:50:    access_token = serializers.CharField(help_text="JWT access token")
./backend/apps/users/serializers.py:55:class DemoLoginSerializer(serializers.Serializer):
./backend/apps/users/serializers.py:56:    """演示登录（仅在DEMO_AUTH_ENABLED=true时启用）"""
./docs/discussions/week3-direction-2026-05-30/04-codex-review-of-claude-response.md:41:- JWT认证或项目当前实际使用的认证方式。
./docs/API测试流程演示.md:34:    "access_token": "eyJhbGci...(JWT Token)",
./docs/API测试流程演示.md:45:**说明：** 学生使用学号和密码登录，获取JWT访问令牌用于后续API调用。
./docs/API测试流程演示.md:125:    "access_token": "eyJhbGci...(JWT Token)",
./docs/API测试流程演示.md:210:    "access_token": "eyJhbGci...(JWT Token)",
./docs/API测试流程演示.md:398:| 登录 | POST | /api/auth/login | 获取JWT令牌 |
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:131:- JWT Bearer认证可见
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:148:- 重复申请409、宿舍阻断422、JWT过期、media权限
./docs/discussions/phase4c-next-steps/45-claude-response-to-codex-option-e-lite-review.md:169:4. JWT Bearer认证可见
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:96:引入`drf-spectacular`本身风险可控，但当前项目大量使用function-based views和手写`Response`错误结构。文件上传虽然有`MultiPartParser`，但OpenAPI对multipart字段、错误envelope、下载文件响应、分页结构和JWT认证的生成结果仍需要人工校准。
./docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:103:- JWT Bearer认证在schema中可见。
./docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:97:- ALLOWED_HOSTS/CORS/DEBUG 安全检查；
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:43:- schema 中 JWT Bearer 可见：`type: http`、`scheme: bearer`、`bearerFormat: JWT`。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:76:- `DEBUG`
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:77:- `ALLOWED_HOSTS`
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:83:- `CORS_ALLOWED_ORIGINS`
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:84:- `SECURE_SSL_REDIRECT`
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:85:- `SESSION_COOKIE_SECURE`
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:86:- `CSRF_COOKIE_SECURE`
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:88:注意：`.env.example` 中包含 `JWT_SECRET_KEY`、`JWT_ACCESS_TOKEN_LIFETIME`、`JWT_REFRESH_TOKEN_LIFETIME`、`MEDIA_ROOT`、`MEDIA_URL`、`REDIS_*`、`CELERY_*`，但当前 settings 没有实际读取这些变量。Step 3 不要把它们写成“生产必填”。更好的处理是：
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:99:- JWT 过期或缺失：表现为 401，重新登录获取 token。
./docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:134:- JWT Bearer schema：可见
./docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md:25:- JWT Bearer认证可见
./docs/discussions/phase4c-next-steps/25-claude-post-evidence-next-strategy.md:85:- CORS白名单配置
./docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:61:| 认证 | login_id、role、access_token mock/JWT格式 | 微信OAuth |
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:39:- JWT Bearer认证可见 ✓
./docs/discussions/phase4c-next-steps/47-claude-post-step2-next-strategy.md:164:  - JWT过期401
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:126:4. **薄认证**：1-2天（User模型、学号+密码登录、JWT）
./docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:215:  - JWT认证
./docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:143:- 重复申请409、宿舍阻断422、JWT过期、media权限
./docs/discussions/week3-direction-2026-05-30/06-consensus.md:100:   - JWT认证或项目实际使用的认证方式
./docs/discussions/week3-direction-2026-05-30/03-claude-response.md:47:- 是否包括JWT认证？
./docs/discussions/week3-direction-2026-05-30/03-claude-response.md:128:- **必须包括**：JWT认证、提交申请、两级审批、状态查询
./docs/discussions/phase4c-next-steps/49-claude-consensus-option-e-lite-complete.md:79:- ✓ JWT Bearer认证可见
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:80:- 权限与JWT认证说明准确。
./docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:207:- 补常见失败：重复申请导致409、宿舍阻断422、JWT过期、media权限。
./docs/discussions/phase4c-next-steps/43-claude-post-phase2a-stabilization-next-strategy.md:78:- 重复申请409、宿舍阻断422、JWT过期、media权限
./docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:134:- 用户有有效的JWT token
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:165:5. ✅ **MINOR - SECURE_SSL_REDIRECT生产环境限制**
./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:139:- ❌ 受限Token：统一使用标准JWT Token
./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:148:#### MAJOR - JWT Token 7天有效期过长
./docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:216:- ✓ JWT Token机制标准
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:66:- JWT Token + Refresh Token机制
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:138:- Django/DRF/SimpleJWT/CORS/filter
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:318:audit_logs 设计有 `request_data` 字段。需要明确脱敏策略，否则登录密码、验证码、JWT、微信 code、API 密钥、外部数据库连接串都可能进入审计日志。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:555:   - base：Django/DRF/PostgreSQL/Redis/Celery/SimpleJWT/requests/python-magic/chinese-calendar/cryptography/django-redis
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:164:5. **MINOR**: `SECURE_SSL_REDIRECT=True`（line 1712）应仅用于生产环境
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:42:7. JWT Token 7天有效期过长
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:139:- JWT Token有效期：7天 → 1小时
./docs/discussions/completion-review-2026-06-03/01-codex-final-assessment.md:45:- DEBUG=False
./docs/discussions/completion-review-2026-06-03/01-codex-final-assessment.md:46:- ALLOWED_HOSTS
./docs/discussions/completion-review-2026-06-03/01-codex-final-assessment.md:50:- CORS/CSRF白名单
./docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:77:   - Claude: "JWT Token 7天有效期过长，建议1小时"
./docs/discussions/phase4c-next-steps/46-claude-codex-consensus-option-e-lite.md:75:4. JWT Bearer认证可见

exec
/bin/bash -lc "rtk sed -n '1,260p' demo-web/index.html" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>毕业离校申请系统 - UI Demo</title>
  <link rel="stylesheet" href="css/global.css">
  <script src="js/api.js"></script>
<script>
    async function loadApprovals() {
        if (!currentToken) return;
        const data = await apiGetApprovals();
        const listContainer = document.querySelector('#screen-1 .card').parentNode;
        
        // Status map based on backend expectations
        const statusMap = {
            'pending_dorm_manager': { text: '待宿管审批', cls: 'tag-pending' },
            'pending_counselor': { text: '待辅导员审批', cls: 'tag-pending' },
            'pending_dean': { text: '待学工部审批', cls: 'tag-pending' },
            'approved': { text: '已通过', cls: 'tag-approved' },
            'rejected': { text: '已拒绝', cls: 'tag-rejected' }
        };

        if (data.results && data.results.length > 0) {
            let htmlStr = '';
            data.results.forEach(approval => {
                const application = approval.application || {};
                const appStatus = application.status || 'unknown';
                const step = statusMap[appStatus] ? statusMap[appStatus].text : appStatus;
                const tagCls = statusMap[appStatus] ? statusMap[appStatus].cls : 'tag-pending';

                htmlStr += '<div class="card" onclick="openApproval(\'' + approval.id + '\')" style="cursor: pointer;">' +
                  '<div class="flex-row justify-between align-center" style="margin-bottom: 8px;">' +
                    '<span style="font-size: 16px; font-weight: bold;">申请 ' + (application.id ? application.id.substring(0,8) : approval.id.substring(0,8)) + '</span>' +
                    '<span class="tag ' + tagCls + '">' + step + '</span>' +
                  '</div>' +
                  '<div style="margin-bottom: 4px;">' +
                    '<span style="font-size: 14px; color: #999; margin-right: 8px;">学生:</span>' +
                    '<span style="font-size: 14px; color: #333;">' + (application.student_name || '-') + ' (' + (application.student_id || '-') + ')</span>' +
                  '</div>' +
                  '<div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #f0f0f0;">' +
                    '<span style="font-size: 12px; color: #999;">' + new Date(approval.created_at || application.created_at).toLocaleString() + '</span>' +
                  '</div>' +
                '</div>';
            });
            listContainer.innerHTML = htmlStr;
        } else {
             listContainer.innerHTML = '<div style="text-align:center; padding: 20px; color:#999;">暂无数据</div>';
        }
    }
    
    let currentApprovalId = null;
    async function openApproval(id) {
        currentApprovalId = id;
        showScreen(2);

        const res = await fetch(API_BASE_URL + '/approvals/' + id + '/', {
            headers: getAuthHeaders()
        });
        if (res.ok) {
            const detail = await res.json();

            const appRes = await fetch(API_BASE_URL + '/applications/' + detail.application_id + '/', {
                headers: getAuthHeaders()
            });
            const appData = appRes.ok ? await appRes.json() : null;

            const container = document.querySelector('#screen-2');

            const basicInfoHtml = '<div class="card">' +
                '<div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">基本信息</div>' +
                '<div style="display: flex; margin-bottom: 8px;">' +
                  '<span style="font-size: 14px; color: #999; width: 80px;">申请ID:</span>' +
                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.application_id || detail.id.substring(0,8)) + '</span>' +
                '</div>' +
                '<div style="display: flex; margin-bottom: 8px;">' +
                  '<span style="font-size: 14px; color: #999; width: 80px;">学生:</span>' +
                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.student_name || '-') + ' (' + (detail.student_id || '-') + ')</span>' +
                '</div>' +
                '<div style="display: flex; margin-bottom: 8px;">' +
                  '<span style="font-size: 14px; color: #999; width: 80px;">联系电话:</span>' +
                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.contact_phone || '-') + '</span>' +
                '</div>' +
                '<div style="display: flex; margin-bottom: 8px;">' +
                  '<span style="font-size: 14px; color: #999; width: 80px;">申请原因:</span>' +
                  '<span style="font-size: 14px; color: #333; flex: 1;">' + (detail.reason || '无') + '</span>' +
                '</div>' +
              '</div>';

            // 动态生成审批时间轴
            const timelineHtml = generateTimeline(detail, appData);

            const cards = container.querySelectorAll('.card');
            if (cards.length > 0) {
                cards[0].outerHTML = basicInfoHtml;
            }
            if (cards.length > 1) {
                cards[1].outerHTML = timelineHtml;
            }
        }
    }

    function generateTimeline(detail, appData) {
        const stepNames = {
            'dorm_manager': '宿管员审批',
            'counselor': '辅导员审批',
            'dean': '学工部审批'
        };

        const appStatus = appData ? appData.status : detail.step;
        const workflow = ['dorm_manager', 'counselor', 'dean'];

        let html = '<div class="card"><div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">审批记录</div>';

        for (let i = workflow.length - 1; i >= 0; i--) {
            const step = workflow[i];
            const stepName = stepNames[step];
            const isLast = i === 0;

            let state, tagText, tagCls, dotBg, dotBorder, showConnector;
            if (appStatus === 'approved' || appStatus === 'pending_' + workflow[i+1] || (i === workflow.length - 1 && appStatus === 'approved')) {
                state = 'approved';
                tagText = '已通过';
                tagCls = 'tag-approved';
                dotBg = 'var(--status-success)';
                dotBorder = 'var(--status-success)';
                showConnector = !isLast;
            } else if (appStatus === 'pending_' + step) {
                state = 'pending';
                tagText = '待审批';
                tagCls = 'tag-pending';
                dotBg = 'white';
                dotBorder = 'var(--primary-color)';
                showConnector = !isLast;
            } else if (appStatus === 'rejected' && detail.step === step) {
                state = 'rejected';
                tagText = '已驳回';
                tagCls = 'tag-rejected';
                dotBg = 'var(--status-error)';
                dotBorder = 'var(--status-error)';
                showConnector = !isLast;
            } else {
                state = 'future';
                tagText = '未开始';
                tagCls = 'tag';
                dotBg = '#e8e8e8';
                dotBorder = '#e8e8e8';
                showConnector = !isLast;
            }

            html += '<div style="position: relative; padding-left: 30px;' + (isLast ? '' : ' margin-bottom: 20px;') + '">' +
              '<div style="position: absolute; left: 10px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: ' + dotBg + '; border: 2px solid ' + dotBorder + ';"></div>';

            if (showConnector) {
                html += '<div style="position: absolute; left: 14px; top: 16px; bottom: -20px; width: 1px; background: #e8e8e8;"></div>';
            }

            html += '<div class="flex-row justify-between align-center" style="margin-bottom: 6px;">' +
                '<span style="font-size: 15px; font-weight: 600;">' + stepName + '</span>' +
                '<span class="tag ' + tagCls + '">' + tagText + '</span>' +
              '</div>';

            if (state === 'approved' || state === 'pending' || state === 'rejected') {
                if (detail.step === step) {
                    html += '<div style="font-size: 13px; color: #666;">审批人: ' + (detail.approver_name || '待分配') + '</div>';
                    if (detail.decided_at) {
                        html += '<div style="font-size: 13px; color: #666;">时间: ' + detail.decided_at + '</div>';
                    }
                    if (detail.comment) {
                        html += '<div style="font-size: 13px; color: #666; margin-top: 4px;">意见: ' + detail.comment + '</div>';
                    }
                }
            }

            html += '</div>';
        }

        html += '<div style="position: relative; padding-left: 30px; margin-top: 20px;">' +
          '<div style="position: absolute; left: 10px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--status-success); border: 2px solid var(--status-success);"></div>' +
          '<div class="flex-row justify-between align-center" style="margin-bottom: 6px;">' +
            '<span style="font-size: 15px; font-weight: 600;">提交申请</span>' +
            '<span class="tag tag-approved">已完成</span>' +
          '</div>' +
          '<div style="font-size: 13px; color: #666;">学生已提交</div>' +
        '</div></div>';

        return html;
    }
    
    async function doApprove() {
        if(!currentApprovalId) return;
        const comment = document.getElementById('approvalComment').value;
        const ok = await apiApprove(currentApprovalId, comment);
        if(ok) { showToast('审批通过', 'success'); showScreen(1); loadApprovals(); }
        else { showToast('审批失败', 'error'); }
    }

    async function doReject() {
        if(!currentApprovalId) return;
        const comment = document.getElementById('approvalComment').value;
        const ok = await apiReject(currentApprovalId, comment);
        if(ok) { showToast('审批拒绝', 'success'); showScreen(1); loadApprovals(); }
        else { showToast('审批失败', 'error'); }
    }
    
    async function doSubmitApplication() {
        const phone = document.getElementById('contactPhone').value;
        const reason = document.getElementById('applicationReason').value;
        const leaveDate = document.getElementById('leaveDate').value;

        // 验证必填字段
        if (!phone || !leaveDate) {
             showToast('请输入联系电话和离校日期', 'error');
             return;
        }

        // 验证手机号格式（11位，1开头）
        if (!/^1\d{10}$/.test(phone)) {
             showToast('请输入有效的11位手机号码', 'error');
             return;
        }

        // 验证原因长度（最多500字符）
        if (reason && reason.length > 500) {
             showToast('离校原因不能超过500字', 'error');
             return;
        }

        // 验证离校日期（不能早于今天）
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const selectedDate = new Date(leaveDate);
        if (selectedDate < today) {
             showToast('离校日期不能早于今天', 'error');
             return;
        }

        const ok = await apiSubmitApplication(phone, reason, leaveDate, uploadedFiles);
        if (ok) {
            showToast('申请提交成功', 'success');
            document.getElementById('contactPhone').value = '';
            document.getElementById('applicationReason').value = '';
            document.getElementById('leaveDate').value = '';
            uploadedFiles = [];
            renderFileList();
        } else {
            showToast('申请提交失败', 'error');
        }
    }
</script>
  <style>
    /* 导航标签 */
    .nav-tabs {
      background: white;
      display: flex;
      border-bottom: 1px solid #f0f0f0;
      position: sticky;
      top: 0;
      z-index: 10;
    }

codex
我已经看到后端 demo-login 的开关默认是 `false`，但还需要确认生产 settings、前端 API 基址和 token 保存位置；这些决定它是不是“可部署安全”，而不是单点函数是否能跑通。
exec
/bin/bash -lc "rtk nl -ba backend/config/settings/prod.py | rtk sed -n '1,120p'" in /home/caohui/projects/graduation-leave-system
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
/bin/bash -lc "rtk rg -n \"function apiLogin|async function apiLogin|apiLogin|currentToken|localStorage|sessionStorage|Authorization|API_BASE_URL|demo-login|password|fetch\\(\" demo-web/index.html demo-web/js -S" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
demo-web/index.html:11:        if (!currentToken) return;
demo-web/index.html:57:        const res = await fetch(API_BASE_URL + '/approvals/' + id + '/', {
demo-web/index.html:63:            const appRes = await fetch(API_BASE_URL + '/applications/' + detail.application_id + '/', {
demo-web/index.html:394:          <input id="loginPassword" type="password" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入密码" required>
demo-web/index.html:609:      const password = document.getElementById('loginPassword').value.trim();
demo-web/index.html:612:      if (!userId || !password) {
demo-web/index.html:618:      const result = await apiLogin(userId, password);
demo-web/index.html:672:      currentToken = null;
demo-web/js/api.js:2:const API_BASE_URL = '/api';
demo-web/js/api.js:4:let currentToken = null;
demo-web/js/api.js:7:async function apiLogin(userId, password) {
demo-web/js/api.js:9:        const response = await fetch(API_BASE_URL + '/auth/login', {
demo-web/js/api.js:14:                password: password
demo-web/js/api.js:20:            currentToken = data.access_token;
demo-web/js/api.js:24:            currentToken = null;
demo-web/js/api.js:31:        currentToken = null;
demo-web/js/api.js:39:        'Authorization': 'Bearer ' + currentToken
demo-web/js/api.js:51:        const response = await fetch(API_BASE_URL + '/applications/', {
demo-web/js/api.js:53:            headers: { 'Authorization': 'Bearer ' + currentToken },
demo-web/js/api.js:65:        const response = await fetch(API_BASE_URL + '/approvals/', {
demo-web/js/api.js:79:        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId + '/approve/', {
demo-web/js/api.js:93:        const response = await fetch(API_BASE_URL + '/approvals/' + approvalId + '/reject/', {
demo-web/js/api.js:111:        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/', {
demo-web/js/api.js:127:        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/', {
demo-web/js/api.js:141:        const response = await fetch(API_BASE_URL + '/applications/' + applicationId + '/attachments/' + attachmentId + '/', {

exec
/bin/bash -lc "rtk nl -ba backend/config/settings/base.py | rtk sed -n '1,190p'" in /home/caohui/projects/graduation-leave-system
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

exec
/bin/bash -lc 'rtk rg -n "DEMO_AUTH_ENABLED|demo-login|auth/login|currentToken|localStorage|SESSION_COOKIE_SECURE|SECURE_SSL_REDIRECT|JWT_ACCESS_TOKEN_LIFETIME|ACCESS_TOKEN_LIFETIME" backend demo-web docs tests .env* -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
.env.example:20:JWT_ACCESS_TOKEN_LIFETIME=3600
.env.docker:16:JWT_ACCESS_TOKEN_LIFETIME=3600
.env.docker:28:DEMO_AUTH_ENABLED=true
tests/multi_role_test.py:35:        login_resp = requests.post(f"{BASE_URL}/api/auth/login", json={
tests/test_p0_fixes.sh:16:TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/test_p0_fixes.sh:38:COUNSELOR_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/smoke_test.sh:50:STUDENT_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/smoke_test.sh:97:M001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/smoke_test.sh:223:T001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/smoke_test.sh:326:STUDENT2_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/smoke_test.sh:357:M002_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/smoke_test.sh:396:T002_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/test_multi_dorm_manager.sh:13:STUDENT_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/test_multi_dorm_manager.sh:59:M001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/test_multi_dorm_manager.sh:81:M003_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/full_workflow_test.py:32:        login_resp = requests.post(f"{BASE_URL}/api/auth/login", json={
tests/approval_workflow_test.py:49:    resp = requests.post(f"{BASE_URL}/api/auth/login", json={
tests/api_data_samples.sh:18:STUDENT_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
tests/api_data_samples.sh:62:COUNSELOR_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
docs/API测试流程演示.md:26:curl -X POST http://localhost:8001/api/auth/login \
docs/API测试流程演示.md:117:curl -X POST http://localhost:8001/api/auth/login \
docs/API测试流程演示.md:202:curl -X POST http://localhost:8001/api/auth/login \
docs/API测试流程演示.md:398:| 登录 | POST | /api/auth/login | 获取JWT令牌 |
demo-web/js/api.js:4:let currentToken = null;
demo-web/js/api.js:9:        const response = await fetch(API_BASE_URL + '/auth/login', {
demo-web/js/api.js:20:            currentToken = data.access_token;
demo-web/js/api.js:24:            currentToken = null;
demo-web/js/api.js:31:        currentToken = null;
demo-web/js/api.js:39:        'Authorization': 'Bearer ' + currentToken
demo-web/js/api.js:53:            headers: { 'Authorization': 'Bearer ' + currentToken },
demo-web/test-integration.sh:14:STUDENT_TOKEN=$(curl -s -X POST "$API_BASE/auth/login" \
demo-web/test-integration.sh:28:DM_TOKEN=$(curl -s -X POST "$API_BASE/auth/login" \
demo-web/test-integration.sh:42:COUNSELOR_TOKEN=$(curl -s -X POST "$API_BASE/auth/login" \
demo-web/test-integration.sh:56:ADMIN_TOKEN=$(curl -s -X POST "$API_BASE/auth/login" \
docs/design/2026-05-27-system-design.md:678:POST /api/v1/auth/login
docs/design/2026-05-27-system-design.md:1954:SECURE_SSL_REDIRECT = True
docs/design/2026-05-27-system-design.md:1955:SESSION_COOKIE_SECURE = True
docs/design/2026-05-27-system-design.md:2102:        location /api/v1/auth/login {
docs/design/2026-05-27-system-design.md:2658:        response = client.post('/api/v1/auth/login', data)
docs/SYSTEM-OPERATIONS-GUIDE.md:60:curl http://localhost:8001/api/auth/login \
docs/SYSTEM-OPERATIONS-GUIDE.md:112:POST /api/auth/login
docs/SYSTEM-OPERATIONS-GUIDE.md:145:POST /api/auth/login
docs/SYSTEM-OPERATIONS-GUIDE.md:180:POST /api/auth/login
docs/SYSTEM-OPERATIONS-GUIDE.md:217:- **端点：** `POST /api/auth/login`
docs/SYSTEM-OPERATIONS-GUIDE.md:312:JWT_ACCESS_TOKEN_LIFETIME=3600
docs/SYSTEM-OPERATIONS-GUIDE.md:383:curl http://localhost:8001/api/auth/login \
docs/week3-day0-acceptance-checklist.md:67:curl -X POST http://localhost:8000/api/auth/login \
docs/week3-day0-acceptance-checklist.md:124:curl -X POST http://localhost:8000/api/auth/login \
docs/week3-day0-acceptance-checklist.md:188:curl -X POST http://localhost:8000/api/auth/login \
docs/week3-day0-acceptance-checklist.md:302:curl -X POST http://localhost:8000/api/auth/login \
docs/week3-day0-acceptance-checklist.md:422:STUDENT_TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
docs/week3-day0-acceptance-checklist.md:439:COUNSELOR_TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
docs/week3-day0-acceptance-checklist.md:452:DEAN_TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
docs/plans/week-0-1-execution-plan.md:30:  - POST /api/auth/login
docs/plans/week-0-1-execution-plan.md:71:- POST /api/auth/login 可用
backend/config/settings/base.py:141:    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
backend/config/settings/prod.py:7:SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
backend/config/settings/prod.py:8:SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
docs/contracts/contract-v0.2.md:146:### POST `/api/auth/login`
docs/contracts/contract-v0.1.md:201:#### POST /api/auth/login
docs/contracts/contract-v0.1.md:598:  rest.post('/api/auth/login', (req, res, ctx) => {
docs/contracts/contract-v0.1.md:626:    response = client.post('/api/auth/login', {
docs/PROJECT-SUMMARY.md:1325:  - JWT配置（JWT_SECRET_KEY, JWT_ACCESS_TOKEN_LIFETIME, JWT_REFRESH_TOKEN_LIFETIME）
docs/PROJECT-SUMMARY.md:4071:2. ✓ Blocking-2: TestAccounts明文凭证 - 移除前端密码，切换到后端demo-login端点
docs/PROJECT-SUMMARY.md:4080:- apiLogin仅传递role到/api/auth/demo-login
docs/PROJECT-SUMMARY.md:4081:- 后端按DEMO_AUTH_ENABLED控制演示登录
docs/PROJECT-SUMMARY.md:4082:- 生产环境必须禁用demo-login（返回404/403）
docs/PROJECT-SUMMARY.md:4123:1. ❌ **后端缺失demo-login端点** - 前端调用但后端未实现，认证流程完全中断
docs/PROJECT-SUMMARY.md:4136:*Task #15: 实现demo-login端点*
docs/PROJECT-SUMMARY.md:4137:- ✓ 后端新增POST /api/auth/demo-login
docs/PROJECT-SUMMARY.md:4139:- ✓ DEMO_AUTH_ENABLED环境变量守卫（生产环境=false）
docs/PROJECT-SUMMARY.md:4152:- ✓ 认证流程已打通（demo-login端点实现）
docs/PROJECT-SUMMARY.md:4173:- ✓ apiLogin改为调用POST /api/auth/login（真实认证端点）
docs/PROJECT-SUMMARY.md:4184:2. ❌ **登录失败状态未清理** - apiLogin失败时未清除currentToken/currentUser
docs/testing-guide.md:34:- 登录: `POST /api/auth/login/`
docs/testing-guide.md:85:curl -X POST http://localhost:8001/api/auth/login/ \
docs/testing-guide.md:165:curl -X POST http://localhost:8001/api/auth/login/ \
docs/testing-guide.md:220:curl -X POST http://localhost:8001/api/auth/login/ \
docs/testing-guide.md:431:- [ ] POST /api/auth/login/ - 登录
backend/apps/users/urls.py:6:    path('demo-login', views.demo_login, name='demo_login'),
docs/test-reports/comprehensive-test-2026-06-07.md:40:1. 用户登录（POST /api/auth/login）
docs/test-reports/comprehensive-test-2026-06-07.md:68:- 原因: 测试脚本使用 `/api/auth/login/` (带尾部斜杠)
docs/test-reports/comprehensive-test-2026-06-07.md:69:- 修复: 改为 `/api/auth/login` (无尾部斜杠)
backend/apps/users/views.py:38:    description='按角色快速登录演示账号。生产环境必须禁用（DEMO_AUTH_ENABLED=false）。',
backend/apps/users/views.py:58:    if os.environ.get('DEMO_AUTH_ENABLED', 'false').lower() != 'true':
docs/test-reports/multi-role-test-2026-06-07.md:45:- **接口:** `POST /api/auth/login`
docs/test-reports/workflow-test-2026-06-07.md:49:- **接口:** `POST /api/auth/login`
docs/test-reports/workflow-test-2026-06-07.md:97:- **现象:** 测试脚本初始使用 `/api/auth/login/` (带尾部斜杠) 导致404错误
docs/test-reports/workflow-test-2026-06-07.md:99:- **修复:** 修改测试脚本使用 `/api/auth/login` (无尾部斜杠)
docs/COMPLETION-STATUS.md:73:- W008: SECURE_SSL_REDIRECT 未启用
docs/COMPLETION-STATUS.md:75:- W012: SESSION_COOKIE_SECURE 未启用
backend/apps/applications/tests/test_error_cases.py:86:        response = self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:103:        response = self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:131:        response = self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:147:        response = self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:160:        response = self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:173:        response = self.client.post('/api/auth/login', {
demo-web/index.html:11:        if (!currentToken) return;
demo-web/index.html:672:      currentToken = null;
backend/apps/applications/tests/test_application_flow.py:66:        response = self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_application_flow.py:85:        response = self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_application_flow.py:106:        response = self.client.post('/api/auth/login', {
docs/acceptance/phase4c-demo-script.md:99:STUDENT_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:189:T001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:237:DEAN_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:283:T002_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:361:STUDENT_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:390:T001_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:406:DEAN_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
docs/acceptance/phase4c-demo-script.md:427:T002_TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
backend/apps/users/serializers.py:56:    """演示登录（仅在DEMO_AUTH_ENABLED=true时启用）"""
docs/acceptance/phase4c-acceptance-checklist.md:18:| 登录API（POST /api/auth/login） | ✅ 通过 | 测试通过 + smoke test步骤1 |
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:47:**Codex指出：** 文档写 `/api/v1/...`、`logout`、`PUT /applications/{id}/`，实际是 `/api/auth/login`、`/api/applications/`、无logout、无PUT
docs/discussions/ui-design-2026-06-02/11-claude-response-operations-manual-review.md:59:- POST /api/auth/login - 用户登录
backend/apps/approvals/tests/test_rejection_flow.py:56:        response = self.client.post('/api/auth/login', {
backend/apps/approvals/tests/test_rejection_flow.py:72:        response = self.client.post('/api/auth/login', {
backend/apps/approvals/tests/test_rejection_flow.py:90:        response = self.client.post('/api/auth/login', {
backend/apps/approvals/tests/test_rejection_flow.py:116:        response = self.client.post('/api/auth/login', {
docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md:34:1. `POST /api/auth/login`
docs/discussions/codex-review-2026-05-30/48-contract-fixes-summary.md:46:- Section 4.1 POST /api/auth/login添加说明
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:28:  1. POST /api/auth/login
docs/discussions/codex-review-2026-05-30/47-contract-fixes-review-request.md:70:- 在contract-v0.1.md Section 4.1 POST /api/auth/login添加说明
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:32:**Root Cause:** Tests use `/api/auth/login/` but route is `/api/auth/login` (no trailing slash)
docs/discussions/week3-day3-planning-2026-05-30/03-claude-response-to-codex.md:98:   - Change `/api/auth/login/` to `/api/auth/login`
docs/discussions/week3-day3-planning-2026-05-30/02-codex-critical-review.md:23:- Root cause: Tests use `/api/auth/login/` but route is `/api/auth/login` (no trailing slash)
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:23:   - Change `/api/auth/login/` to `/api/auth/login` (remove trailing slash)
docs/discussions/week3-day3-planning-2026-05-30/04-final-consensus.md:183:- Root cause: Tests use `/api/auth/login/` but route is `/api/auth/login`
docs/操作说明书.md:378:- POST /api/auth/login - 用户登录
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:78:- 暴力破解密码（/api/v1/auth/login无速率限制）
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:165:5. ✅ **MINOR - SECURE_SSL_REDIRECT生产环境限制**
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:164:5. **MINOR**: `SECURE_SSL_REDIRECT=True`（line 1712）应仅用于生产环境
docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md:49:- 当前路由是`/api/auth/login`（无尾斜杠）
docs/discussions/phase4c-next-steps/50-claude-post-option-e-lite-next-strategy.md:175:- /api/auth/login/ - 添加@extend_schema
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:84:- `SECURE_SSL_REDIRECT`
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:85:- `SESSION_COOKIE_SECURE`
docs/discussions/phase4c-next-steps/48-codex-post-step2-next-strategy-response.md:88:注意：`.env.example` 中包含 `JWT_SECRET_KEY`、`JWT_ACCESS_TOKEN_LIFETIME`、`JWT_REFRESH_TOKEN_LIFETIME`、`MEDIA_ROOT`、`MEDIA_URL`、`REDIS_*`、`CELERY_*`，但当前 settings 没有实际读取这些变量。Step 3 不要把它们写成“生产必填”。更好的处理是：
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:31:The plan describes `/api/auth/login/` and a token response containing a refresh token. The current route is `path('login', ...)`, so the canonical route is `/api/auth/login` without a trailing slash. The current login serializer returns `access_token`, `token_type`, and `user`; it does not return `refresh_token`.
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:198:- Document auth/login and notification pagination accurately.

exec
/bin/bash -lc "rtk nl -ba demo-web/js/api.js | rtk sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
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
/bin/bash -lc "rtk nl -ba demo-web/index.html | rtk sed -n '360,700p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   360	  </style>
   361	</head>
   362	<body>
   363	  <!-- 顶部导航 -->
   364	  <div class="nav-tabs">
   365	    <button class="nav-tab active" onclick="showScreen(0)">学生申请</button>
   366	    <button class="nav-tab" onclick="showScreen(1)"><span id="nav-approval-text">审批列表</span></button>
   367	    <button class="nav-tab" onclick="showScreen(2)">申请详情</button>
   368	  </div>
   369	
   370	  <!-- 登录状态栏 -->
   371	  <div id="userBar" style="background: white; padding: 8px 16px; border-bottom: 1px solid #f0f0f0; display: none; align-items: center; justify-content: space-between;">
   372	    <div>
   373	      <span style="font-size: 14px; color: #666;">当前用户:</span>
   374	      <span id="currentUserName" style="font-size: 14px; font-weight: 500; margin-left: 8px;"></span>
   375	      <span id="currentUserRole" style="font-size: 12px; color: #999; margin-left: 8px;"></span>
   376	    </div>
   377	    <button onclick="logout()" style="padding: 4px 12px; border: 1px solid #d9d9d9; border-radius: 4px; background: white; cursor: pointer;">退出登录</button>
   378	  </div>
   379	
   380	  <!-- 登录屏幕 -->
   381	  <div class="login-screen active" id="screen-login">
   382	    <div style="padding: 40px 20px; max-width: 400px; margin: 0 auto;">
   383	      <div class="card">
   384	        <div style="text-align: center; margin-bottom: 30px;">
   385	          <h2 style="color: var(--primary-color); margin-bottom: 8px;">毕业离校申请系统</h2>
   386	          <p style="color: #666; font-size: 14px;">请登录以继续</p>
   387	        </div>
   388	        <div style="margin-bottom: 20px;">
   389	          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">用户ID</label>
   390	          <input id="loginUserId" type="text" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入用户ID（如 2020001）" required>
   391	        </div>
   392	        <div style="margin-bottom: 24px;">
   393	          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">密码</label>
   394	          <input id="loginPassword" type="password" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入密码" required>
   395	        </div>
   396	        <div id="loginError" style="display: none; padding: 10px; background: #fff2f0; border: 1px solid #ffccc7; border-radius: 4px; color: #cf1322; font-size: 14px; margin-bottom: 16px;"></div>
   397	        <button class="btn-primary" onclick="doLogin()">登录</button>
   398	        <div style="margin-top: 16px; padding: 12px; background: #f6f6f6; border-radius: 4px;">
   399	          <div style="font-size: 12px; color: #666; margin-bottom: 4px;">演示账号：</div>
   400	          <div style="font-size: 12px; color: #999;">学生: 2020001 / 2020001</div>
   401	          <div style="font-size: 12px; color: #999;">宿管员: M001 / M001</div>
   402	          <div style="font-size: 12px; color: #999;">辅导员: T001 / T001</div>
   403	          <div style="font-size: 12px; color: #999;">学工部: D001 / D001</div>
   404	        </div>
   405	      </div>
   406	    </div>
   407	  </div>
   408	
   409	  <div class="screen" id="screen-0">
   410	    <div style="padding: 20px;">
   411	      <!-- 用户信息卡片 -->
   412	      <div class="card" style="margin-bottom: 20px;">
   413	        <div style="font-size: 16px; font-weight: 600; color: var(--primary-color); margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #f0f0f0;">
   414	          申请人信息
   415	        </div>
   416	        <div style="display: flex; align-items: center; padding: 10px 0;">
   417	          <span style="font-size: 14px; color: #666; width: 80px;">姓名</span>
   418	          <span style="font-size: 14px; color: #333;">张三</span>
   419	        </div>
   420	        <div style="display: flex; align-items: center; padding: 10px 0;">
   421	          <span style="font-size: 14px; color: #666; width: 80px;">学号</span>
   422	          <span style="font-size: 14px; color: #333;">2020001</span>
   423	        </div>
   424	      </div>
   425	
   426	      <!-- 表单卡片 -->
   427	      <div class="card">
   428	        <div style="margin-bottom: 20px;">
   429	          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">联系电话</label>
   430	          <input id="contactPhone" type="tel" name="contact_phone" maxlength="20" inputmode="numeric" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入联系电话" required>
   431	        </div>
   432	        <div style="margin-bottom: 20px;">
   433	          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">离校原因</label>
   434	          <textarea id="applicationReason" style="width: 100%; min-height: 120px; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="请输入离校原因"></textarea>
   435	          <span style="display: block; text-align: right; font-size: 12px; color: #999; margin-top: 4px;">0/500</span>
   436	        </div>
   437	        <div style="margin-bottom: 20px;">
   438	          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">离校日期</label>
   439	          <input id="leaveDate" type="date" name="leave_date" style="width: 100%; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" required>
   440	        </div>
   441	
   442	        <!-- 附件上传区域 -->
   443	        <div style="margin-bottom: 20px;">
   444	          <label style="display: block; font-size: 14px; margin-bottom: 8px; font-weight: 500;">附件材料（可选）</label>
   445	          <div class="upload-zone">
   446	            <input type="file" id="fileInput" multiple accept=".jpg,.jpeg,.png,.pdf,.doc,.docx" style="display: none;">
   447	            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
   448	              <div style="font-size: 40px; color: #999; margin-bottom: 8px;">📎</div>
   449	              <div style="font-size: 14px; color: #666;">点击或拖拽文件到此处上传</div>
   450	              <div style="font-size: 12px; color: #999; margin-top: 4px;">支持jpg/png/pdf/doc/docx，单文件不超过10MB</div>
   451	            </div>
   452	          </div>
   453	          <!-- 文件列表 -->
   454	          <div id="fileList" style="margin-top: 12px;"></div>
   455	        </div>
   456	
   457	        <button class="btn-primary" onclick="doSubmitApplication()">提交申请</button>
   458	      </div>
   459	    </div>
   460	  </div>
   461	
   462	  <!-- 屏幕2: 审批列表页 -->
   463	  <div class="screen" id="screen-1">
   464	    <div style="background: white; padding: 16px; display: flex; justify-content: space-between; align-items: center;">
   465	      <div style="font-size: 18px; font-weight: bold;" id="list-title">审批列表</div>
   466	      <div style="font-size: 12px; color: #999;" id="role-display">宿管员</div>
   467	    </div>
   468	
   469	    <!-- Tab切换 -->
   470	    <div style="background: white; display: flex; border-bottom: 1px solid #f0f0f0;">
   471	      <div class="nav-tab active" style="flex: 1;">全部</div>
   472	      <div class="nav-tab" style="flex: 1;">待审批</div>
   473	      <div class="nav-tab" style="flex: 1;">已审批</div>
   474	    </div>
   475	
   476	    <div style="padding: 10px;">
   477	      <!-- 列表项 -->
   478	      <div class="card">
   479	        <div class="flex-row justify-between align-center" style="margin-bottom: 8px;">
   480	          <span style="font-size: 16px; font-weight: bold;">申请 APP-001</span>
   481	          <span class="tag tag-pending">待审批</span>
   482	        </div>
   483	        <div style="margin-bottom: 4px;">
   484	          <span style="font-size: 14px; color: #999; margin-right: 8px;">申请ID:</span>
   485	          <span style="font-size: 14px; color: #333;">APP-001</span>
   486	        </div>
   487	        <div style="margin-bottom: 4px;">
   488	          <span style="font-size: 14px; color: #999; margin-right: 8px;">审批步骤:</span>
   489	          <span style="font-size: 14px; color: #333;">宿管员审批</span>
   490	        </div>
   491	        <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #f0f0f0;">
   492	          <span style="font-size: 12px; color: #999;">2024-06-01 10:30</span>
   493	        </div>
   494	      </div>
   495	
   496	      <div class="card">
   497	        <div class="flex-row justify-between align-center" style="margin-bottom: 8px;">
   498	          <span style="font-size: 16px; font-weight: bold;">申请 APP-002</span>
   499	          <span class="tag tag-approved">已通过</span>
   500	        </div>
   501	        <div style="margin-bottom: 4px;">
   502	          <span style="font-size: 14px; color: #999; margin-right: 8px;">申请ID:</span>
   503	          <span style="font-size: 14px; color: #333;">APP-002</span>
   504	        </div>
   505	        <div style="margin-bottom: 4px;">
   506	          <span style="font-size: 14px; color: #999; margin-right: 8px;">审批步骤:</span>
   507	          <span style="font-size: 14px; color: #333;">辅导员审批</span>
   508	        </div>
   509	        <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #f0f0f0;">
   510	          <span style="font-size: 12px; color: #999;">2024-05-30 14:20</span>
   511	        </div>
   512	      </div>
   513	    </div>
   514	  </div>
   515	
   516	  <!-- 屏幕3: 申请详情页 -->
   517	  <div class="screen" id="screen-2">
   518	    <div style="background: white; padding: 16px;">
   519	      <div style="font-size: 18px; font-weight: bold;">申请详情</div>
   520	    </div>
   521	
   522	    <div style="padding: 10px;">
   523	      <!-- 基本信息 -->
   524	      <div class="card">
   525	        <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">基本信息</div>
   526	        <div style="display: flex; margin-bottom: 8px;">
   527	          <span style="font-size: 14px; color: #999; width: 80px;">申请ID:</span>
   528	          <span style="font-size: 14px; color: #333; flex: 1;">APP-001</span>
   529	        </div>
   530	        <div style="display: flex; margin-bottom: 8px;">
   531	          <span style="font-size: 14px; color: #999; width: 80px;">学生:</span>
   532	          <span style="font-size: 14px; color: #333; flex: 1;">张三 (2020001)</span>
   533	        </div>
   534	        <div style="display: flex; margin-bottom: 8px;">
   535	          <span style="font-size: 14px; color: #999; width: 80px;">离校日期:</span>
   536	          <span style="font-size: 14px; color: #333; flex: 1;">2024-06-15</span>
   537	        </div>
   538	        <div style="display: flex; margin-bottom: 8px;">
   539	          <span style="font-size: 14px; color: #999; width: 80px;">申请原因:</span>
   540	          <span style="font-size: 14px; color: #333; flex: 1;">毕业实习，需要提前离校</span>
   541	        </div>
   542	      </div>
   543	
   544	      <!-- 审批记录时间轴 -->
   545	      <div class="card">
   546	        <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">审批记录</div>
   547	
   548	        <!-- 时间轴项 -->
   549	        <div style="position: relative; padding-left: 30px; margin-bottom: 20px;">
   550	          <div style="position: absolute; left: 10px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: white; border: 2px solid var(--primary-color);"></div>
   551	          <div style="position: absolute; left: 14px; top: 16px; bottom: -20px; width: 1px; background: #e8e8e8;"></div>
   552	          <div class="flex-row justify-between align-center" style="margin-bottom: 6px;">
   553	            <span style="font-size: 15px; font-weight: 600;">宿管员审批</span>
   554	            <span class="tag tag-pending">待审批</span>
   555	          </div>
   556	          <div style="font-size: 13px; color: #666;">审批人: 李老师</div>
   557	        </div>
   558	
   559	        <div style="position: relative; padding-left: 30px; margin-bottom: 20px;">
   560	          <div style="position: absolute; left: 10px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: var(--status-success); border: 2px solid var(--status-success);"></div>
   561	          <div class="flex-row justify-between align-center" style="margin-bottom: 6px;">
   562	            <span style="font-size: 15px; font-weight: 600;">提交申请</span>
   563	            <span class="tag tag-approved">已完成</span>
   564	          </div>
   565	          <div style="font-size: 13px; color: #666;">提交时间: 2024-06-01 10:30</div>
   566	        </div>
   567	      </div>
   568	
   569	      <!-- 审批操作 -->
   570	      <div id="approval-section" style="padding: 10px;">
   571	        <div class="card" style="margin-bottom: 10px;">
   572	          <label style="display: block; font-size: 14px; color: #333; margin-bottom: 6px; font-weight: 500;">审批意见（可选）</label>
   573	          <textarea id="approvalComment" style="width: 100%; min-height: 60px; padding: 8px; border: 1px solid #e8e8e8; border-radius: 4px; font-size: 14px;" placeholder="请输入审批意见"></textarea>
   574	          <span style="display: block; text-align: right; font-size: 12px; color: #999; margin-top: 4px;">0/200</span>
   575	        </div>
   576	        <div style="display: flex; gap: 10px;" id="approval-actions">
   577	          <button class="btn-primary" style="flex: 1;" onclick="doApprove()">通过</button>
   578	          <button class="btn-outline" style="flex: 1;" onclick="doReject()">拒绝</button>
   579	        </div>
   580	      </div>
   581	    </div>
   582	  </div>
   583	
   584	  <script>
   585	    // Status mapping
   586	    const statusMap = {
   587	      'pending_dorm_manager': { text: '待宿管审批', class: 'tag-pending' },
   588	      'pending_counselor': { text: '待辅导员审批', class: 'tag-pending' },
   589	      'pending_dean': { text: '待学工部审批', class: 'tag-pending' },
   590	      'approved': { text: '已通过', class: 'tag-approved' },
   591	      'rejected': { text: '已拒绝', class: 'tag-rejected' }
   592	    };
   593	
   594	    function getStatusDisplay(status) {
   595	      return statusMap[status] || { text: status, class: 'tag' };
   596	    }
   597	
   598	    function showScreen(index) {
   599	      document.querySelectorAll('.screen').forEach((s, i) => {
   600	        s.classList.toggle('active', i === index);
   601	      });
   602	      document.querySelectorAll('.nav-tabs .nav-tab').forEach((t, i) => {
   603	        t.classList.toggle('active', i === index);
   604	      });
   605	    }
   606	
   607	    async function doLogin() {
   608	      const userId = document.getElementById('loginUserId').value.trim();
   609	      const password = document.getElementById('loginPassword').value.trim();
   610	      const errorEl = document.getElementById('loginError');
   611	
   612	      if (!userId || !password) {
   613	        errorEl.textContent = '请输入用户ID和密码';
   614	        errorEl.style.display = 'block';
   615	        return;
   616	      }
   617	
   618	      const result = await apiLogin(userId, password);
   619	
   620	      if (result.success) {
   621	        errorEl.style.display = 'none';
   622	        document.getElementById('loginUserId').value = '';
   623	        document.getElementById('loginPassword').value = '';
   624	
   625	        // Show user bar
   626	        document.getElementById('userBar').style.display = 'flex';
   627	        document.getElementById('currentUserName').textContent = result.user.name;
   628	        const roleMap = {
   629	          'student': '学生',
   630	          'dorm_manager': '宿管员',
   631	          'counselor': '辅导员',
   632	          'dean': '学工部'
   633	        };
   634	        document.getElementById('currentUserRole').textContent = '(' + (roleMap[result.user.role] || result.user.role) + ')';
   635	
   636	        // Update UI based on role
   637	        updateUIForRole(result.user.role);
   638	
   639	        // Hide login screen, show appropriate screen
   640	        document.getElementById('screen-login').classList.remove('active');
   641	        if (result.user.role === 'student') {
   642	          showScreen(0); // Student application screen
   643	        } else {
   644	          showScreen(1); // Approval list screen
   645	          loadApprovals();
   646	        }
   647	      } else {
   648	        errorEl.textContent = result.error.error || '登录失败，请检查用户ID和密码';
   649	        errorEl.style.display = 'block';
   650	      }
   651	    }
   652	
   653	    function updateUIForRole(role) {
   654	      const isStudent = role === 'student';
   655	      const isDean = role === 'dean';
   656	
   657	      // Update nav tab text
   658	      document.getElementById('nav-approval-text').textContent = isStudent ? '我的申请' : (isDean ? '备案查询' : '审批列表');
   659	
   660	      // Update list page title and role display
   661	      document.getElementById('list-title').textContent = isStudent ? '我的申请' : (isDean ? '备案查询' : '审批列表');
   662	      document.getElementById('role-display').textContent = (isStudent ? '学生' : isDean ? '学工部' : role === 'counselor' ? '辅导员' : '宿管员');
   663	
   664	      // Show/hide approval section for student/dean
   665	      const approvalSection = document.getElementById('approval-section');
   666	      if (approvalSection) {
   667	        approvalSection.style.display = (isStudent || isDean) ? 'none' : 'block';
   668	      }
   669	    }
   670	
   671	    function logout() {
   672	      currentToken = null;
   673	      currentUser = null;
   674	      document.getElementById('userBar').style.display = 'none';
   675	      document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
   676	      document.getElementById('screen-login').classList.add('active');
   677	    }
   678	
   679	    // File upload management
   680	    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
   681	    const ALLOWED_TYPES = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx'];
   682	    let uploadedFiles = [];
   683	
   684	    const fileInput = document.getElementById('fileInput');
   685	    const fileList = document.getElementById('fileList');
   686	    const uploadArea = document.querySelector('.upload-area');
   687	
   688	    // File selection handler
   689	    fileInput.addEventListener('change', (e) => {
   690	      handleFiles(e.target.files);
   691	    });
   692	
   693	    // Drag and drop handlers
   694	    uploadArea.addEventListener('dragover', (e) => {
   695	      e.preventDefault();
   696	      uploadArea.style.borderColor = 'var(--primary-color)';
   697	      uploadArea.style.background = '#fafafa';
   698	    });
   699	
   700	    uploadArea.addEventListener('dragleave', () => {

exec
/bin/bash -lc "rtk sed -n '80,130p' DEPLOYMENT.md && rtk sed -n '160,190p' DEPLOYMENT.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:

### 6. Access Application

- Backend API: http://localhost:8001
- Admin: http://localhost:8001/admin
- API Schema: http://localhost:8001/api/schema/swagger-ui/

## Environment Variables

### Core Settings

| Variable | Purpose | Default | Production Required |
|----------|---------|---------|---------------------|
| `SECRET_KEY` | Django secret key for cryptographic signing | `django-insecure-dev-key-change-in-production` | **Yes** - Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | Enable debug mode | `True` | **No** - Set to `False` in production |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `localhost,127.0.0.1` | **Yes** - Set to your domain(s) |

### Database Settings

| Variable | Purpose | Default | Production Required |
|----------|---------|---------|---------------------|
| `DB_NAME` | PostgreSQL database name | `graduation_leave` | **No** - Default is fine |
| `DB_USER` | PostgreSQL username | `postgres` | **Yes** - Use dedicated user |
| `DB_PASSWORD` | PostgreSQL password | `postgres` | **Yes** - Use secure password |
| `DB_HOST` | PostgreSQL host | `localhost` | **No** - Use `db` for Docker |
| `DB_PORT` | PostgreSQL port | `5432` | **No** - Default is fine |

### CORS Settings

| Variable | Purpose | Default | Production Required |
|----------|---------|---------|---------------------|
| `CORS_ALLOWED_ORIGINS` | Comma-separated list of allowed origins | `http://localhost:3000,http://127.0.0.1:3000` | **Yes** - Set to your frontend URL(s) |

### Notes

- **JWT Settings:** JWT tokens use `SECRET_KEY` for signing (no separate `JWT_SECRET_KEY` needed)
- **Media Files:** `MEDIA_URL=/media/` and `MEDIA_ROOT=/app/media` are hardcoded (not configurable via env vars)
- **Unused Variables:** `.env.example` may reference `JWT_SECRET_KEY`, `REDIS_URL`, `CELERY_BROKER_URL` - these are not currently read by the application

## Data Import

### CSV Field Requirements

**counselors.csv:**
- employee_id (required)
- name (required)
- department (optional)

**mappings.csv:**
- class_id (required)
- counselor_employee_id (required)
{"error": {"code": "CONFLICT", "message": "You already have a pending or approved application"}}
```
**Cause:** Student already has an active application (status: pending_counselor, pending_dean, or approved)

**Solution:** Student must wait for current application to be rejected before submitting a new one, or contact administrator to check application status.

**422 Unprocessable Entity - Dorm Clearance Blocked**
```json
{"error": {"code": "DORM_BLOCKED", "message": "Cannot submit application: dorm clearance not completed"}}
```
**Cause:** Student's dorm checkout status is not `completed` (checked via mock provider or real dorm system API)

**Solution:** Student must complete dorm clearance first. Check dorm system status or contact dorm administrator.

**401 Unauthorized - JWT Expired**
```json
{"detail": "Given token not valid for any token type"}
```
**Cause:** JWT access token expired (default lifetime: 24 hours)

**Solution:** Re-login to get new token. Frontend should implement automatic token refresh or redirect to login page.

**403 Forbidden - Cross-Role Access**
```json
{"error": {"code": "FORBIDDEN", "message": "You do not have permission to perform this action"}}
```
**Common scenarios:**
- Student trying to access another student's application
- Counselor trying to approve application from different class
- Dean trying to approve counselor-step approval


codex
这里出现一个事实偏差：当前 `demo-web/js/api.js` 的 `apiLogin` 调的是 `/api/auth/login` 并发送 `user_id/password`，不是 `/api/auth/demo-login`。我会把这个作为审计发现处理，因为它影响“明文密码”和演示账号暴露的风险判断。
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
/bin/bash -lc 'rtk rg -n "demo-login|DemoLoginSerializer|DEMO_AUTH_ENABLED" backend/apps/users backend/apps -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/users/urls.py:6:    path('demo-login', views.demo_login, name='demo_login'),
backend/apps/users/views.py:7:from .serializers import LoginSerializer, LoginResponseSerializer, DemoLoginSerializer
backend/apps/users/views.py:38:    description='按角色快速登录演示账号。生产环境必须禁用（DEMO_AUTH_ENABLED=false）。',
backend/apps/users/views.py:39:    request=DemoLoginSerializer,
backend/apps/users/views.py:58:    if os.environ.get('DEMO_AUTH_ENABLED', 'false').lower() != 'true':
backend/apps/users/views.py:61:    serializer = DemoLoginSerializer(data=request.data)
backend/apps/users/serializers.py:55:class DemoLoginSerializer(serializers.Serializer):
backend/apps/users/serializers.py:56:    """演示登录（仅在DEMO_AUTH_ENABLED=true时启用）"""
backend/apps/users/urls.py:6:    path('demo-login', views.demo_login, name='demo_login'),
backend/apps/users/serializers.py:55:class DemoLoginSerializer(serializers.Serializer):
backend/apps/users/serializers.py:56:    """演示登录（仅在DEMO_AUTH_ENABLED=true时启用）"""
backend/apps/users/views.py:7:from .serializers import LoginSerializer, LoginResponseSerializer, DemoLoginSerializer
backend/apps/users/views.py:38:    description='按角色快速登录演示账号。生产环境必须禁用（DEMO_AUTH_ENABLED=false）。',
backend/apps/users/views.py:39:    request=DemoLoginSerializer,
backend/apps/users/views.py:58:    if os.environ.get('DEMO_AUTH_ENABLED', 'false').lower() != 'true':
backend/apps/users/views.py:61:    serializer = DemoLoginSerializer(data=request.data)

exec
/bin/bash -lc 'rtk rg -n "DEMO_AUTH_ENABLED|DJANGO_SETTINGS_MODULE|config.settings|SECURE_SSL_REDIRECT|SESSION_COOKIE_SECURE|CSRF_COOKIE_SECURE|SECRET_KEY|DEBUG|ALLOWED_HOSTS|CORS_ALLOWED_ORIGINS" docker-compose*.yml Dockerfile backend manage.py .env.example .env.docker -S' in /home/caohui/projects/graduation-leave-system
 exited 2 in 0ms:
rg: Dockerfile: No such file or directory (os error 2)
rg: manage.py: No such file or directory (os error 2)
.env.docker:10:SECRET_KEY=django-insecure-docker-dev-key-change-in-production
.env.docker:11:DEBUG=True
.env.docker:12:ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
.env.docker:15:JWT_SECRET_KEY=jwt-secret-key-change-in-production
.env.docker:28:DEMO_AUTH_ENABLED=true
.env.example:10:SECRET_KEY=your-secret-key-here-generate-with-django-get-secret-key
.env.example:11:DEBUG=False
.env.example:12:ALLOWED_HOSTS=your-domain.com,localhost
.env.example:19:JWT_SECRET_KEY=your-jwt-secret-key-here
backend/config/settings/base.py:11:SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')
backend/config/settings/base.py:13:DEBUG = config('DEBUG', default=True, cast=bool)
backend/config/settings/base.py:15:ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])
backend/config/settings/base.py:146:    'SIGNING_KEY': SECRET_KEY,
backend/config/settings/base.py:153:CORS_ALLOWED_ORIGINS = config(
backend/config/settings/base.py:154:    'CORS_ALLOWED_ORIGINS',
backend/manage.py:9:    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/normalize_department_names.py:10:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/export_blocked_students.py:11:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/config/settings/dev.py:4:DEBUG = True
backend/config/settings/dev.py:6:ALLOWED_HOSTS = ['*']
backend/scripts/normalize_building_null.py:10:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/update_offcampus_graduates.py:11:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/import_graduates.py:13:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/import_missing_counselors.py:10:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/config/wsgi.py:5:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
backend/scripts/analyze_department_values.py:11:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/verify_system_readiness.py:10:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/analyze_graduate_data.py:11:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/verify_db_status.py:10:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/xg_api_collection_test.py:22:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
backend/scripts/validate_import.py:13:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/diagnose_xg_api.py:10:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:57:# config/settings/base.py
backend/docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:100:- 文件：config/settings/base.py
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:21:**文件:** `config/settings/base.py`  
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:151:1. `config/settings/base.py` - 添加TEST_REQUEST_DEFAULT_FORMAT
backend/scripts/comprehensive_db_analysis.py:13:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/verify_import_integrity.py:11:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/config/settings/prod.py:4:DEBUG = False
backend/config/settings/prod.py:7:SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
backend/config/settings/prod.py:8:SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
backend/config/settings/prod.py:9:CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
backend/scripts/backup_database.py:9:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/apps/users/views.py:38:    description='按角色快速登录演示账号。生产环境必须禁用（DEMO_AUTH_ENABLED=false）。',
backend/apps/users/views.py:58:    if os.environ.get('DEMO_AUTH_ENABLED', 'false').lower() != 'true':
backend/apps/users/serializers.py:56:    """演示登录（仅在DEMO_AUTH_ENABLED=true时启用）"""

exec
/bin/bash -lc 'rtk rg -n "X_FRAME_OPTIONS|SECURE_HSTS|SECURE_PROXY_SSL_HEADER|SECURE_REFERRER_POLICY|CSRF_TRUSTED_ORIGINS|CORS_ALLOW_ALL_ORIGINS" backend/config/settings -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/config/settings/dev.py:12:CORS_ALLOW_ALL_ORIGINS = True

codex
配置里还有一个部署层面的高风险点：`.env.docker` 明确把 `DEMO_AUTH_ENABLED=true`，而 `backend/manage.py` 默认使用 dev settings。只靠“生产时记得别这样配”不够，需要部署前置校验。
exec
/bin/bash -lc "rtk nl -ba backend/manage.py | rtk sed -n '1,60p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	#!/usr/bin/env python
     2	"""Django's command-line utility for administrative tasks."""
     3	import os
     4	import sys
     5	
     6	
     7	def main():
     8	    """Run administrative tasks."""
     9	    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
    10	    try:
    11	        from django.core.management import execute_from_command_line
    12	    except ImportError as exc:
    13	        raise ImportError(
    14	            "Couldn't import Django. Are you sure it's installed and "
    15	            "available on your PYTHONPATH environment variable? Did you "
    16	            "forget to activate a virtual environment?"
    17	        ) from exc
    18	    execute_from_command_line(sys.argv)
    19	
    20	
    21	if __name__ == '__main__':
    22	    main()

exec
/bin/bash -lc "rtk nl -ba .env.example | rtk sed -n '1,80p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# Database Configuration
     2	DB_ENGINE=django.db.backends.postgresql
     3	DB_NAME=graduation_leave
     4	DB_USER=postgres
     5	DB_PASSWORD=your_secure_password_here
     6	DB_HOST=db
     7	DB_PORT=5432
     8	
     9	# Django Settings
    10	SECRET_KEY=your-secret-key-here-generate-with-django-get-secret-key
    11	DEBUG=False
    12	ALLOWED_HOSTS=your-domain.com,localhost
    13	
    14	# Media Files
    15	MEDIA_ROOT=/app/media
    16	MEDIA_URL=/media/
    17	
    18	# JWT Settings
    19	JWT_SECRET_KEY=your-jwt-secret-key-here
    20	JWT_ACCESS_TOKEN_LIFETIME=3600
    21	JWT_REFRESH_TOKEN_LIFETIME=86400
    22	
    23	# Redis (optional, for future use)
    24	REDIS_HOST=localhost
    25	REDIS_PORT=6379
    26	
    27	# Celery (optional, for future use)
    28	CELERY_BROKER_URL=redis://localhost:6379/0
    29	CELERY_RESULT_BACKEND=redis://localhost:6379/0

exec
/bin/bash -lc "rtk nl -ba .env.docker | rtk sed -n '1,80p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# Database Configuration
     2	DB_ENGINE=django.db.backends.postgresql
     3	DB_NAME=graduation_leave
     4	DB_USER=postgres
     5	DB_PASSWORD=postgres
     6	DB_HOST=db
     7	DB_PORT=5432
     8	
     9	# Django Settings
    10	SECRET_KEY=django-insecure-docker-dev-key-change-in-production
    11	DEBUG=True
    12	ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
    13	
    14	# JWT Settings
    15	JWT_SECRET_KEY=jwt-secret-key-change-in-production
    16	JWT_ACCESS_TOKEN_LIFETIME=3600
    17	JWT_REFRESH_TOKEN_LIFETIME=86400
    18	
    19	# Redis (for future use)
    20	REDIS_HOST=localhost
    21	REDIS_PORT=6379
    22	
    23	# Celery (for future use)
    24	CELERY_BROKER_URL=redis://localhost:6379/0
    25	CELERY_RESULT_BACKEND=redis://localhost:6379/0
    26	
    27	# Demo Authentication (演示环境快速登录，生产环境必须设为false)
    28	DEMO_AUTH_ENABLED=true

exec
/bin/bash -lc "rtk rg --files | rtk rg '("'^|/)(docker-compose.*'"\\.ya?ml|Dockerfile|manage.py|\\.env.*|settings/.*\\.py)"'$'"'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docker-compose.yml
backend/config/settings/__init__.py
backend/config/settings/base.py
backend/config/settings/prod.py
backend/config/settings/test.py
backend/config/settings/dev.py
backend/manage.py
backend/Dockerfile

exec
/bin/bash -lc "rtk nl -ba backend/config/settings/dev.py | rtk sed -n '1,60p'" in /home/caohui/projects/graduation-leave-system
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

codex
我还会看 Docker 启动命令，确认容器到底用 dev 还是 prod settings；这会影响我是否把误启用 demo-login 判为 P0。
exec
/bin/bash -lc "rtk nl -ba docker-compose.yml | rtk sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	version: '3.8'
     2	
     3	services:
     4	  db:
     5	    image: postgres:15-alpine
     6	    environment:
     7	      POSTGRES_DB: graduation_leave
     8	      POSTGRES_USER: postgres
     9	      POSTGRES_PASSWORD: postgres
    10	    ports:
    11	      - "5432:5432"
    12	    volumes:
    13	      - postgres_data:/var/lib/postgresql/data
    14	    healthcheck:
    15	      test: ["CMD-SHELL", "pg_isready -U postgres"]
    16	      interval: 5s
    17	      timeout: 5s
    18	      retries: 5
    19	
    20	  backend:
    21	    build:
    22	      context: ./backend
    23	      dockerfile: Dockerfile
    24	    command: python manage.py runserver 0.0.0.0:8000
    25	    volumes:
    26	      - ./backend:/app
    27	      - media_data:/app/media
    28	    ports:
    29	      - "8001:8000"
    30	    env_file:
    31	      - .env.docker
    32	    depends_on:
    33	      db:
    34	        condition: service_healthy
    35	
    36	volumes:
    37	  postgres_data:
    38	  media_data:

exec
/bin/bash -lc "rtk nl -ba backend/Dockerfile | rtk sed -n '1,160p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	FROM python:3.11-slim
     2	
     3	WORKDIR /app
     4	
     5	# Install system dependencies
     6	RUN apt-get update && apt-get install -y \
     7	    gcc \
     8	    postgresql-client \
     9	    libpq-dev \
    10	    libmagic1 \
    11	    && rm -rf /var/lib/apt/lists/*
    12	
    13	# Copy requirements
    14	COPY requirements/ /app/requirements/
    15	
    16	# Install Python dependencies
    17	RUN pip install --no-cache-dir -r requirements/base.txt
    18	
    19	# Copy application code
    20	COPY . /app/
    21	
    22	# Expose port
    23	EXPOSE 8000
    24	
    25	# Run Django
    26	CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

exec
/bin/bash -lc "rtk rg -n \"gunicorn|runserver|DJANGO_SETTINGS_MODULE|config.settings.dev|config.settings.prod|env_file|\\.env.docker\" -S docker-compose.yml backend/Dockerfile scripts backend" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/requirements/prod.txt:4:gunicorn==21.2.0
backend/config/wsgi.py:5:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
backend/Dockerfile:26:CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
backend/scripts/normalize_department_names.py:10:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/export_blocked_students.py:11:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/normalize_building_null.py:10:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/update_offcampus_graduates.py:11:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/import_graduates.py:13:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/import_missing_counselors.py:10:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/analyze_department_values.py:11:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/verify_system_readiness.py:10:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/analyze_graduate_data.py:11:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/verify_db_status.py:10:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/verify_import_integrity.py:11:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/comprehensive_db_analysis.py:13:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
docker-compose.yml:24:    command: python manage.py runserver 0.0.0.0:8000
docker-compose.yml:30:    env_file:
docker-compose.yml:31:      - .env.docker
backend/scripts/backup_database.py:9:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/xg_api_collection_test.py:22:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
backend/scripts/validate_import.py:13:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/Dockerfile:26:CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
backend/manage.py:9:    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
backend/scripts/diagnose_xg_api.py:10:os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

exec
/bin/bash -lc "rtk nl -ba backend/config/wsgi.py | rtk sed -n '1,60p' && rtk nl -ba backend/config/asgi.py | rtk sed -n '1,60p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	"""WSGI config for graduation leave system project."""
     2	import os
     3	from django.core.wsgi import get_wsgi_application
     4	
     5	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
     6	
     7	application = get_wsgi_application()
nl: backend/config/asgi.py: No such file or directory

codex
**审计结论：不建议宣称生产就绪。** 8/8 集成测试通过只能说明流程可用，当前仍有生产阻断级安全风险。

**P0 / 生产阻断**

1. [backend/apps/users/views.py:58](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:58) `DEMO_AUTH_ENABLED` 默认值是 `false`，这一点正确；但 [.env.docker:28](/home/caohui/projects/graduation-leave-system/.env.docker:28) 设置为 `true`，且 [docker-compose.yml:24](/home/caohui/projects/graduation-leave-system/docker-compose.yml:24) 用 `runserver`，会走 [backend/manage.py:9](/home/caohui/projects/graduation-leave-system/backend/manage.py:9) 的 `config.settings.dev`。如果这套 compose 被误用于公网，任何人都能按角色直接领取学生、宿管、辅导员、学工部 JWT。

2. [demo-web/js/api.js:7](/home/caohui/projects/graduation-leave-system/demo-web/js/api.js:7) 当前 `apiLogin` 实际调用的是 `/api/auth/login`，不是 `/api/auth/demo-login`；[demo-web/index.html:398](/home/caohui/projects/graduation-leave-system/demo-web/index.html:398) 仍公开展示演示账号和弱口令。如果这些账号存在于生产库且密码未改，这就是公开后门。

3. JWT 使用 [backend/config/settings/base.py:146](/home/caohui/projects/graduation-leave-system/backend/config/settings/base.py:146) 的 `SECRET_KEY` 签名，而默认值是 [backend/config/settings/base.py:11](/home/caohui/projects/graduation-leave-system/backend/config/settings/base.py:11) 的固定开发密钥，`.env.docker` 也使用固定弱密钥。生产若未强制替换，JWT 可被伪造。

4. HTTPS 不是强制项：[backend/config/settings/prod.py:7](/home/caohui/projects/graduation-leave-system/backend/config/settings/prod.py:7) `SECURE_SSL_REDIRECT` 默认 `false`。当前登录会发送密码，后续请求会发送 Bearer token；生产 HTTP 下等同明文暴露凭证和 token。

**P1 / 高风险**

1. [backend/apps/users/serializers.py:60](/home/caohui/projects/graduation-leave-system/backend/apps/users/serializers.py:60) 硬编码 `student -> 2020001` 等不是秘密本身，但风险在于它把公开 role 映射到真实高权限账号。建议增加 `is_demo` 标记或独立 demo 用户表，并校验 `user.is_demo=True`，禁止映射到真实业务账号。

2. [backend/apps/users/views.py:55](/home/caohui/projects/graduation-leave-system/backend/apps/users/views.py:55) `demo_login` 是 `AllowAny` 且无 throttle/audit。即使只在演示环境，也应限制频率、记录 role/IP/User-Agent，并在启用时明确打启动告警。

3. [backend/config/settings/base.py:141](/home/caohui/projects/graduation-leave-system/backend/config/settings/base.py:141) access token 24 小时偏长，且前端没有刷新/失效处理。demo-login 返回的是标准 access token，本身生成方式可接受，但生产建议 15-60 分钟、强密钥、必要时启用 token blacklist 或短会话策略。

4. `demo-web/index.html` 多处把后端字段拼接进 `innerHTML`，例如申请人、原因、意见等。如果后端数据可被用户提交，会形成存储型 XSS；因为 token 在 JS 内存变量 `currentToken` 中，XSS 可直接发起已认证请求。应统一使用 `textContent` 或 HTML escaping。

**必须修复建议**

- 生产启动时强制断言：`DEBUG=False`、`DEMO_AUTH_ENABLED != true`、`SECRET_KEY` 非默认、`ALLOWED_HOSTS` 非通配、HTTPS 开关启用。
- 将 `DEMO_AUTH_ENABLED` 移入 Django settings，并在 `prod.py` 中硬禁止：生产环境检测到 true 直接启动失败。
- 删除生产包中的 demo-web 演示账号提示，或只在明确 demo build 中展示。
- 演示账号与真实账号隔离，增加 `is_demo` 校验；高权限 demo 账号不得存在于生产库。
- 生产启用 HTTPS/HSTS/secure cookies/proxy SSL header，反向代理只暴露 HTTPS。
- 给 `/api/auth/login` 和 `/api/auth/demo-login` 配置 throttling、审计日志和异常告警。

当前状态可以说“开发/演示环境可用”，不能说“生产就绪”。
tokens used
95,764

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
