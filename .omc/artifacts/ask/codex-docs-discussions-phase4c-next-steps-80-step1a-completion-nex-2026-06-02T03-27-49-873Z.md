# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-02T03:27:49.873Z

## Original task

docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md

## Final prompt

docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md

## Raw output

```text
## 1. Step 1A审查结果

结论：签名纯函数可以通过，当前无 P0。

P1 问题：

1. MD5 测试断言过弱  
   [test_xg_user_client.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/tests/test_xg_user_client.py:28) 只校验长度和 hex 字符集，不能证明排序/拼接正确。建议改成固定值断言：`generate_sign('secret', '1234567890', 'random', 'md5') == '2a471e23465cf11561ef7455fff00a86'`。

2. 如果 Step 1A 仍定义为“签名与配置切片”，配置校验尚未完成  
   [xg_user_client.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/integrations/xg_user_client.py:46) 的 `XGUserAPIClient` 仍是占位类。若 Step 1A 只验收签名函数，可通过；若按 doc 79 的“配置校验”验收，还需要配置对象和缺失配置测试。

P2 建议：

- 空字符串校验放在配置/请求构建层，不要污染 `generate_sign()` 纯函数。
- 特殊字符/Unicode 不是 P0；当前 UTF-8 行为确定。`randStr` 后续建议限制为 ASCII。
- `XG_USER_API_ENCRYPTION_TYPE` 的 `strip().lower()` 归一化应放在配置层。

验证：已运行 `rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client -v 2 --keepdb --noinput`，4/4 passed。

## 2. 下一步策略建议

建议采用“修正后的选项A”：先补 Step 1A 小修正，再做 Step 1B-lite，然后做 Step 1C。

不建议纯选项B先写孤立诊断脚本。诊断脚本本身也要构造 headers/form-data、签名、超时、错误分类和脱敏输出；如果不先有可复用客户端层，后续容易重复实现并产生不一致。

## 3. Step 1C范围确认

Step 1C 应是安全诊断入口：

- 必须包含：环境变量校验、官方签名样例自检、默认 dry-run、`XG_RUN_LIVE_API_TEST=1` 才允许 live probe、固定 `page=1/pageNum=1`、短超时、错误分类、脱敏输出。
- 可支持：`--format=json`、`--timeout`。
- 应避免：完整 headers、完整 `sign`、完整响应 body、分页循环、落库、Provider 接入、CI 中默认 live 调用。

## 4. Step 1B范围界定

Step 1B-lite 应包含：

- `XGUserAPIConfig` 或等价配置对象。
- `build_headers()`：`appKey/timestamp/randStr/sign/encryptionType`，timestamp/randStr 可注入便于测试。
- `build_form_data()`：`tenantCode/page/pageNum`，默认单页一条。
- `fetch_users_page()`：单页请求、短超时、可注入 session。
- 基础响应解析和 mock 测试：成功、HTTP错误、网络异常、业务错误、schema异常、缺失配置、非法加密类型。

应排除：全量分页、重试机制、Provider 接入、数据库写入、字段业务映射、真实API进入常规测试。


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
session id: 019e865d-ef56-7be3-9268-6aa4efbc8424
--------
user
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md
codex
I’ll inspect the project instructions and the referenced review request, then follow the local review protocol before giving findings.
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

codex
The project requires `rtk` on shell commands, and the review protocol is active for this request. I’m loading the collaboration contract and the requested document next so the response matches the repo’s workflow.
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md" in /home/caohui/projects/graduation-leave-system
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

 succeeded in 3040ms:
exec
/bin/bash -lc "rtk sed -n '241,520p' docs/codex-review-protocol.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:

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
- 修复后要验证一致性
- 必要时进行多轮讨论

### ✗ 常见错误
- 不要直接调用`codex`命令（使用`/ask`）
- 不要跳过Claude响应步骤
- 不要盲目接受所有Codex建议
- 不要只修改部分文档
- 不要忘记更新项目文档
- 不要一次审查过大篇幅内容

---

## 七、成功案例

**案例1：数据源需求v2共识**
- 请求：34-codex-second-review-response.md
- Codex：通过`/ask codex`调用，artifact保存
- Claude：35-response-to-codex-critical-issues.md（修正5个关键问题）
- 共识：31-data-source-requirements-consensus-v2.md
- 结果：修正staging表设计、认证约束、class_id约束等关键问题

---

## 八、与旧方式的区别

**旧方式（已废弃）：**
```bash
codex review "$(cat [文档路径])"
```

**新方式（推荐）：**
```
/oh-my-claudecode:ask codex "审查 [文档路径] - [审查要求]"
```

**优势：**
- 统一的调用接口
- 自动artifact管理
- 更好的错误处理
- 与OMC生态集成

---

**流程版本：** v2.0  
**创建日期：** 2026-05-27  
**更新日期：** 2026-05-28  
**变更说明：** 从自定义skill迁移到使用`/oh-my-claudecode:ask`

codex
The request is a formal Codex review of Step 1A and next-step strategy. I’m reading the implementation and tests now, plus enough surrounding context to verify whether the request’s completion claims match the code.
exec
/bin/bash -lc "rtk sed -n '1,180p' backend/apps/users/integrations/__init__.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
"""学工系统API集成模块"""
from .xg_user_client import generate_sign, XGUserAPIClient

__all__ = ['generate_sign', 'XGUserAPIClient']

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
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/users/integrations/xg_user_client.py" in /home/caohui/projects/graduation-leave-system
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
/bin/bash -lc "rtk rg -n \"generate_sign|XGUserAPIClient|XG_|xg_user|签名|sign\" backend docs/discussions/phase4c-next-steps -g '"'!**/.venv/**'"'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/discussions/phase4c-next-steps/35-codex-authorization-interpretation-response.md:79:   范围：Django Notification模型、迁移、4个读取/已读API、RBAC测试、seed命令；不含 signals、Celery、小程序通知页、微信模板。
docs/discussions/phase4c-next-steps/35-codex-authorization-interpretation-response.md:109:- signals；
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:45:> - 不包含：signals、小程序通知页、微信模板消息
docs/discussions/phase4c-next-steps/33-claude-consensus-authorization-gate.md:70:- signals触发逻辑（推迟到Phase 2）
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:11:完全接受Codex审查意见，并补充一个关键进展：**用户已提供官方签名算法**。
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:33:### P1：签名算法问题（已解决）
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:35:**Codex指出：** 签名算法缺失，不能靠猜测实现。
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:37:**Claude确认：** **问题已解决！用户在审查过程中提供了官方签名算法。**
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:39:**官方签名算法（已确认）：**
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:42:签名规则：
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:61:def generate_sign(app_secret: str, timestamp: str, rand_str: str, 
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:64:    生成API签名
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:73:        签名字符串（十六进制小写）
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:80:    sign_str = ''.join(params)
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:84:        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:86:        return hashlib.sha1(sign_str.encode('utf-8')).hexdigest()
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:104:3. 通过环境变量 `XG_USER_API_URL` 配置
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:117:1. 通过环境变量 `XG_USER_API_TENANT_CODE` 配置
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:132:1. 独立诊断脚本: `backend/scripts/xg_user_api_probe.py`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:133:2. 可Mock客户端: `backend/apps/users/integrations/xg_user_client.py`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:134:3. Mock单元测试: `backend/apps/users/tests/test_xg_user_client.py`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:135:4. 真实API测试通过 `XG_RUN_LIVE_API_TEST=1` 门禁
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:160:- AppId: ${XG_USER_API_APP_ID}
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:161:- AppKey: ${XG_USER_API_APP_KEY}
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:162:- AppSecret: ${XG_USER_API_APP_SECRET}
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
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:245:- 日志不打印secret/完整sign
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:252:1. 实现 `backend/apps/users/tests/test_xg_user_client.py`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:259:- 测试覆盖签名生成、请求构造、响应解析
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:269:2. 设置 `XG_RUN_LIVE_API_TEST=1`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:270:3. 运行 `xg_user_api_probe.py`
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:297:2. ✅ 签名算法已确认（用户提供官方算法）
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:308:1. **签名算法已确认** - 不再是猜测，可以直接实现
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:320:3. 实现签名客户端和诊断脚本
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:327:**Claude签名：** 完全接受Codex审查意见，基于确认的签名算法开始实现。
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:11:**状态：** 达成共识，执行Step 1A（签名与配置切片）
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:24:- Step 1A: 签名与配置
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:39:### 3. 签名验证
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:42:- `generate_sign()` 纯函数
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:63:backend/apps/users/integrations/xg_user_client.py
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:64:backend/apps/users/tests/test_xg_user_client.py
docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md:69:- [ ] `generate_sign()` 实现
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:34:- ⏸ Phase 2：signals自动触发通知创建
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:47:### Option A：Track 3 Phase 2（signals自动触发）
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:50:- 实现Django signals监听Application/Approval状态变更
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:60:- 增加系统复杂度（signals耦合）
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:65:- signals实现：2-3小时
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:86:- 无signals时通知列表为空（需要手工创建测试数据）
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:102:- Phase 2：signals自动触发
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:192:### 推荐：Option A（Track 3 Phase 2 - signals自动触发）
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:204:- 使用Django signals（post_save）监听Application/Approval变更
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:205:- 补充signals单元测试和集成测试
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:213:5. 所有signals测试通过
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:218:- 无signals时前端通知列表为空（用户体验差）
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:236:1. **策略选择：** Option A（Phase 2 signals）是否合理？是否有更优方案？
docs/discussions/phase4c-next-steps/37-claude-post-phase1-next-strategy.md:250:**Claude签名：** 待Codex审查后达成共识
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:33:**接受：** 先创建`backend/apps/notifications/services.py`，提供幂等创建函数，而不是直接在signals receiver中实现业务逻辑。
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:68:- Django signals实现（可选，视服务层验证结果决定）
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:146:- 纯signals实现（改为服务层+业务视图调用）
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:24:- ✅ **签名算法已确认**（用户提供官方算法）
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:36:backend/apps/users/integrations/xg_user_client.py   # 客户端
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:37:backend/scripts/xg_user_api_probe.py                # 诊断脚本
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:38:backend/apps/users/tests/test_xg_user_client.py     # Mock测试
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:42:1. 签名函数（基于确认的官方算法）
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:77:### 问题2：签名算法是否需要单独验证模块？
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:79:**背景：** 用户提供的签名示例使用不同的AppSecret。
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:87:**选项A：** 客户端内置签名函数，测试时用官方样例验证
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:91:**选项B：** 先实现独立签名验证脚本，确认算法正确后再集成
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:104:1. 签名客户端（核心）
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:116:  - B1: 先只实现签名函数 + 官方样例验证
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:123:  - 只实现签名验证脚本
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:172:✓ 签名生成: baea...4515
docs/discussions/phase4c-next-steps/27-claude-consensus-decision-gate.md:33:- 不包含：Django model/migration/serializer/viewset/signals
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:170:- `test_list_assigned_counselor_positive` ✅
docs/discussions/phase4c-next-steps/30-claude-consensus-contract-revision-gate.md:84:**理由：** 没有signals就没有真实的业务幂等验收对象
docs/discussions/phase4c-next-steps/30-claude-consensus-contract-revision-gate.md:111:- 描述：实现Django model + migration + API + 测试（不含signals）
docs/discussions/phase4c-next-steps/30-claude-consensus-contract-revision-gate.md:170:- ❌ 不实现signals触发逻辑（Phase 2才考虑）
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:79:- signals；
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:112:如果 0.5 天内开始写 model、migration、signals 和 API，范围会快速超过「最小契约」。
docs/discussions/phase4c-next-steps/26-codex-post-evidence-strategy-review.md:150:- **只新增文档**：不新增 model、migration、serializer、viewset、URL、signals、tests。
docs/discussions/phase4c-next-steps/36-claude-consensus-minimal-confirmation.md:54:- signals、Celery、审批挂钩、超时提醒
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:18:> 是否授权启动 Track 3 Phase 1 后端通知 MVP（Django model + migration + read APIs + tests，不含 signals/小程序/微信模板消息）？
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:63:- `post_save` signals。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:132:5. 将 signal 示例从 Phase 1 相关实现建议中移到 Phase 2，避免误导实现范围。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-review.md:138:**推荐路线：短决策门 -> 用户授权 -> Phase 1 后端 MVP 一次性完成 -> 再停下审查 Phase 2 signals。**
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:115:Fix `STUDENT_NOTIF_COUNT` in `tests/smoke_test.sh`. Either assign it before line 255 or remove that echo if the final unread-count assertion is the real check. Run the smoke test once with the existing reset strategy if the environment is available.
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:120:- assigned counselor allowed
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:13:**结论：Step 1A签名纯函数可以通过，但建议在进入真实诊断前补两个小修正。**
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:17:- `backend/apps/users/integrations/xg_user_client.py` 的 `generate_sign()` 按三个参数值排序后拼接，再做 `sha1/md5` 小写 hex，符合当前官方样例约束。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:20:- 聚焦测试在 Docker 环境通过：`rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client -v 2 --keepdb --noinput`，4/4 passed。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:26:当前代码没有发现会导致官方签名样例失败、密钥泄露或错误参与字段签名的 P0 问题。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:31:   位置：`backend/apps/users/tests/test_xg_user_client.py:28`  
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:32:   现在只检查长度和 hex 字符集，即使拼接顺序错误也可能通过。建议改成固定期望值，例如 `generate_sign('secret', '1234567890', 'random', 'md5')` 应等于 `2a471e23465cf11561ef7455fff00a86`。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:35:   位置：`backend/apps/users/integrations/xg_user_client.py:46`  
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:36:   当前只交付签名函数，`XGUserAPIClient` 仍是占位类，尚无配置读取/校验对象。若把 Step 1A 定义为“签名函数切片”，可以接受；若沿用 doc 77 验收标准，则还缺少 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 的明确错误测试。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:41:   `generate_sign()` 作为纯函数可以允许空字符串，但请求构建/配置层必须拒绝空 `appSecret/timestamp/randStr`。建议不要在签名函数里混入环境语义，在 Step 1B 的 config/header 构造处校验。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:47:   `generate_sign()` 严格接受 `sha1/md5` 是合理的；环境变量读取时可以对 `XG_USER_API_ENCRYPTION_TYPE` 做 `strip().lower()`，再传入纯函数。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:51:- 当前签名函数不会记录或返回密钥，仅返回摘要，安全面较小。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:53:- 后续诊断脚本不得打印完整 `appSecret`、完整 `sign`、手机号、身份证号、openId 或完整原始响应。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:61:不建议纯选项B先写诊断脚本。诊断脚本也必须构造 headers/form-data、生成 timestamp/randStr/sign、处理超时和脱敏输出；如果没有可复用客户端层，脚本会复制 Step 1B 逻辑，后续再迁回客户端时容易产生签名字段、日志脱敏、错误分类不一致。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:72:   诊断脚本调用 Step 1B-lite 的客户端能力，默认 dry-run；只有 `XG_RUN_LIVE_API_TEST=1` 且配置齐全时做一次 `page=1/pageNum=1` live probe。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:85:- 官方签名样例自检。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:87:- live probe 硬门禁：`XG_RUN_LIVE_API_TEST=1`，配置齐全，固定 `page=1/pageNum=1`。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:90:- 错误分类：`config_error`、`sign_error`、`network_error`、`http_error`、`auth_failed`、`tenant_invalid`、`business_error`、`unexpected_schema`。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:95:- 不记录完整请求 headers，因为其中包含完整 `sign`。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:106:签名样例: OK
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:107:Live调用: skipped (XG_RUN_LIVE_API_TEST != 1)
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:108:请求摘要: POST auth-user-info page=1 pageNum=1 encryptionType=sha1 sign=present
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:128:- `XGUserAPIClient.build_headers()`：
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:129:  - 包含 `appKey/timestamp/randStr/sign/encryptionType`。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:132:- `XGUserAPIClient.build_form_data()`：
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:135:- `XGUserAPIClient.fetch_users_page()`：
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:143:  - header字段完整、签名确定性。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:162:Step 1A可以作为“签名函数切片”通过；进入下一步前建议补 MD5 固定值测试。下一步不要先写孤立诊断脚本，而是先做一个很窄的 Step 1B-lite，让 Step 1C 复用同一套请求构造、签名和脱敏逻辑。真实 live probe 仍必须保持单页一条、显式开关、脱敏输出。
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:28:### 问题2：签名算法验证
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:33:- `generate_sign()` 作为独立纯函数
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:44:- **Step 1A:** 签名与配置（立即执行）
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:80:- `.env.example` 保留 `XG_USER_API_APP_ID` 用于记录
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:111:### Step 1A：签名与配置（立即执行）
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:116:backend/apps/users/integrations/xg_user_client.py
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:117:backend/apps/users/tests/test_xg_user_client.py
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:121:- ✅ `generate_sign()` 实现正确
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:122:- ✅ 官方签名样例测试通过
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:132:- `XGUserAPIClient.build_headers()`
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:133:- `XGUserAPIClient.build_form_data()`
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:134:- `XGUserAPIClient.fetch_users_page()`
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:144:backend/scripts/xg_user_api_probe.py
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:157:2. ✅ 签名函数优先，官方样例P0测试
docs/discussions/phase4c-next-steps/22-claude-post-execution-next-steps.md:193:**Claude签名**  
docs/discussions/phase4c-next-steps/34-claude-authorization-interpretation-request.md:35:- 排除：signals、Celery、小程序页、微信模板
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:35:| Phase 1是否包含 signals | 不包含 | 信号触发应作为 Phase 2 单独审查 |
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:73:如果 Phase 1 只做读取 API 和已读 API，不做创建路径和 signals，就没有真实的“同一业务状态变更不重复创建通知”验收对象。把幂等性测试列为 Phase 1 必过项会迫使实现临时创建入口或测试内部方法，范围会变形。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:75:**建议：** Phase 1只验收模型约束、读取/已读 API、RBAC。业务事件幂等测试挪到 Phase 2 signals 任务；Phase 1最多测试数据库唯一约束。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:119:signals、`transaction.on_commit()`、审批状态机挂钩、宿舍阻断通知、超时提醒都放到 Phase 2。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:136:- **实现范围膨胀：** Phase 1禁止 signals 和 Celery。
docs/discussions/phase4c-next-steps/29-codex-post-phase0-next-strategy-response.md:163:5. 如果用户选 A，再执行 Phase 1A/1B/1C，但不包含 signals。
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
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:50:  - XGUserAPIClient
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:65:- 不把 `tenantCode`、`appKey`、form-data 混入签名，除非后续官方文档另行确认。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:73:**B1：签名与配置切片**
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:76:- 实现 `generate_sign()`。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:78:- 单元测试覆盖官方签名样例、md5、非法 `encryptionType`、缺失必填环境变量。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:89:- `backend/scripts/xg_user_api_probe.py` 作为人工诊断入口。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:123:签名样例: OK
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:124:Live调用: skipped (missing tenantCode or XG_RUN_LIVE_API_TEST != 1)
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:138:JSON 输出不能包含 `appSecret`、完整 `sign`、完整手机号、身份证、微信 openId。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:146:`docs/api说明.txt` 的 header 参数是 `appKey`，没有 `appId`。`backend/.env.example` 已包含 `XG_USER_API_APP_ID`，可以保留用于记录平台凭证，但请求构造不要默认发送 `appId`。若平台部确认学校网关还要求 `appId`，再显式加入 header。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:171:- `sign_error`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:185:### Step 1A：签名与配置，先做
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:190:- `backend/apps/users/integrations/xg_user_client.py`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:191:- `backend/apps/users/tests/test_xg_user_client.py`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:195:- 官方签名样例通过。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:196:- 缺失 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 时有明确错误。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:197:- `tenantCode` 缺失不影响签名样例测试。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:203:- `XGUserAPIClient.build_headers()`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:204:- `XGUserAPIClient.build_form_data()`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:205:- `XGUserAPIClient.fetch_users_page()`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:210:- header 包含 `appKey/timestamp/randStr/sign/encryptionType`。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:219:- `backend/scripts/xg_user_api_probe.py`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:226:- `XG_RUN_LIVE_API_TEST=1` 且配置齐全时才允许发请求。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:245:  generate_sign
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:246:  XGUserAPIClient
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:247:  xg_user_api_probe.py
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:266:1. 先做 `generate_sign()` 和官方样例测试。
docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:17:### 1. 签名算法已确认
docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:19:**Codex担心：** 签名算法缺失，不能靠猜测实现。
docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:21:**用户提供：** 官方签名算法（字典排序+拼接+sha1/md5）
docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:45:backend/scripts/xg_user_api_probe.py        # 诊断脚本
docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:46:backend/apps/users/integrations/xg_user_client.py   # 客户端
docs/discussions/phase4c-next-steps/75-claude-codex-consensus-api-test-step0.md:47:backend/apps/users/tests/test_xg_user_client.py     # Mock测试
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:26:- AppId: ${XG_USER_API_APP_ID}
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:27:- AppKey: ${XG_USER_API_APP_KEY}
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:28:- AppSecret: ${XG_USER_API_APP_SECRET}
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:38:- `sign`: 认证签名（必填，算法未知）
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
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:75:- List visibility: student own positive, student other negative, assigned counselor positive, cross-counselor negative, assigned dean positive or negative according to the final RBAC decision.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:95:Do not run the full 48-test suite after every small edit. It wastes time without improving signal.
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:21:4. **Phase 1不得包含 signals、Celery、小程序通知页、微信模板消息。**
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:37:| Phase 1是否包含 signals | 不同意 | signals 属于 Phase 2 |
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:71:signals、`transaction.on_commit()`、审批状态机挂钩、超时提醒、宿舍阻断触发都放到 Phase 2 单独审查。
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:119:   范围：Notification model/migration/API/tests/seed command，不含 signals、小程序通知页、微信模板消息。
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:148:- signals；
docs/discussions/phase4c-next-steps/32-codex-post-contract-revision-next-strategy-response.md:164:> 通知契约已经修正到可实现状态。建议授权启动 Track 3 Phase 1 后端MVP实现，范围仅限 Django Notification模型、迁移、读取/已读API、RBAC测试和测试造数命令；不包含 signals、小程序通知页、微信模板消息。请确认是否授权启动 Phase 1。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:18:2. **P1：签名算法不能靠猜测进入正式实现；最多允许在一次性诊断脚本中按候选算法快速验证，正式代码必须等待平台部提供签名校验文档或可确认的样例。**
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:20:另外，`docs/api说明.txt` 的官方样式文档只给出 `sign`、`timestamp`、`randStr`、`encryptionType` 字段，但缺少“签名校验部分”；`tenantCode` 也只有示例值 `C10026`。因此第一阶段的目标应调整为“受控验证接口合同”，不是直接实现生产数据同步。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:34:- 将文档中的凭证替换为占位符，例如 `${XG_APP_KEY}`、`${XG_APP_SECRET}`。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:37:- 不在日志中打印完整 header、secret、sign 原文；最多打印尾部4位或哈希摘要。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:39:### P1：签名算法缺失，不能作为正式实现假设
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:45:当前文档明确写“请参见签名校验部分”，但仓库内文档没有该部分。候选算法 A/B/C 都只是合理猜测，不能作为生产实现依据。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:49:- 向平台部索要签名校验文档，至少需要：参与签名的字段、字段顺序、是否包含 form-data、secret位置、大小写、编码、输出hex/base64、时间戳单位、randStr长度、签名有效窗口。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:50:- 同时索要一个固定样例：固定 appKey、timestamp、randStr、tenantCode、appSecret 和期望 sign。没有固定样例时，算法验证成本会显著上升。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:90:- pytest/Django测试只覆盖签名函数、请求构造、响应解析、错误处理，并使用 mock/responses。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:91:- 真实API测试必须通过显式开关启用，例如 `XG_RUN_LIVE_API_TEST=1`。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:97:### 1. 签名算法推断
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:99:在没有官方签名校验章节前，最可能的顺序建议如下：
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:101:1. **参数排序SHA1/MD5：** 将参与签名参数按key排序后拼接，再追加或混入 `appSecret`。很多开放平台采用这种方式，且文档提供 `encryptionType=sha1|md5` 更像普通摘要算法选择，而不是HMAC选择。
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
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:170:XG_USER_API_URL
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:171:XG_USER_API_APP_KEY
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:172:XG_USER_API_APP_SECRET
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:173:XG_USER_API_TENANT_CODE
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:174:XG_USER_API_ENCRYPTION_TYPE=sha1
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:175:XG_RUN_LIVE_API_TEST=0
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:189:- 不打印完整 sign。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:198:- `auth_failed`：HTTP 401/403 或业务错误提示签名失败，输出当前算法名和非敏感参数。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:203:不要对认证失败做大量重试。签名错误重试越多，越可能触发风控或污染审计。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:221:- 获得签名校验文档或固定签名样例。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:229:- `xg_user_client.py` 支持候选签名算法、请求构造、响应解析。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:230:- `xg_user_api_probe.py` 可通过环境变量运行，默认只请求 `page=1&pageNum=1`。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:245:- 仅在 `XG_RUN_LIVE_API_TEST=1` 时执行。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:264:- **实现可mock的客户端单元测试，覆盖签名候选和响应解析。**
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:266:- **签名和租户确认前，不启动生产数据读取实现。**
backend/apps/users/integrations/__init__.py:2:from .xg_user_client import generate_sign, XGUserAPIClient
backend/apps/users/integrations/__init__.py:4:__all__ = ['generate_sign', 'XGUserAPIClient']
backend/apps/attachments/tests/test_download.py:89:        """Assigned counselor can download attachment"""
backend/apps/approvals/tests/test_permissions.py:147:    def test_non_assigned_dean_forbidden(self):
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:12:1. **Step 1A实现审查**：审查签名生成函数实现质量
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:24:   - 导出 `generate_sign` 和 `XGUserAPIClient`
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:26:2. **backend/apps/users/integrations/xg_user_client.py**
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:27:   - `generate_sign()` 函数：支持SHA1/MD5签名生成
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:29:   - `XGUserAPIClient` 类（占位符，待实现）
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:31:3. **backend/apps/users/tests/test_xg_user_client.py**
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:32:   - 官方签名样例测试（P0需求）
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:40:   - 添加测试开关 `XG_RUN_LIVE_API_TEST`
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:59:- backend/apps/users/integrations/xg_user_client.py
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:60:- backend/apps/users/tests/test_xg_user_client.py
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:63:- 签名算法实现是否严格遵循官方规范？
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:71:- ✅ 官方签名样例验证
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:84:- ✅ **Step 1A（已完成）**：签名生成函数 + 单元测试
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:118:- 签名生成测试（使用真实配置）
backend/apps/users/tests/test_xg_user_client.py:3:from apps.users.integrations.xg_user_client import generate_sign
backend/apps/users/tests/test_xg_user_client.py:7:    """签名生成函数测试"""
backend/apps/users/tests/test_xg_user_client.py:10:        """测试官方签名样例（sha1）"""
backend/apps/users/tests/test_xg_user_client.py:15:        sign = generate_sign(app_secret, timestamp, rand_str, 'sha1')
backend/apps/users/tests/test_xg_user_client.py:17:        self.assertEqual(sign, 'baeaa6693fb7b9914c9ff9e388654878b8754515')
backend/apps/users/tests/test_xg_user_client.py:21:        sign = generate_sign(
backend/apps/users/tests/test_xg_user_client.py:26:        self.assertEqual(sign, 'baeaa6693fb7b9914c9ff9e388654878b8754515')
backend/apps/users/tests/test_xg_user_client.py:30:        sign = generate_sign('secret', '1234567890', 'random', 'md5')
backend/apps/users/tests/test_xg_user_client.py:32:        self.assertEqual(len(sign), 32)
backend/apps/users/tests/test_xg_user_client.py:33:        self.assertTrue(all(c in '0123456789abcdef' for c in sign))
backend/apps/users/tests/test_xg_user_client.py:38:            generate_sign('secret', '1234567890', 'random', 'sha256')
backend/apps/applications/tests/test_detail_permissions.py:71:        # Counselor T002 (assigned to CS2020-02) tries to access
backend/apps/applications/tests/test_detail_permissions.py:77:    def test_dean_cannot_access_non_assigned_application(self):
backend/apps/users/migrations/0001_initial.py:22:                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
backend/apps/attachments/tests/test_list.py:131:    def test_list_assigned_counselor_positive(self):
backend/apps/attachments/tests/test_list.py:132:        """Assigned counselor can list application attachments"""
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:12:**结论：有条件同意 Option A，但不同意按当前文档写法直接实现“4种通知类型 + 纯 signals”。**
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:14:Codex建议的下一步是 **Option A-lite：先完成后端自动通知闭环，但把范围收窄为 3 个可由现有持久化模型可靠触发的事件，并先抽出通知创建服务，再选择性接入 signals 或业务视图钩子**。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:27:原因是当前代码里宿舍阻断发生在申请创建之前，接口直接返回 `422`，没有 `Application` 实体可作为通知关联对象；超时提醒仍需要定时扫描/任务调度，不属于 signals 立即触发范围。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:33:### P1：`DORM_CLEARANCE_BLOCKED` 不能由当前模型 signals 可靠触发
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:44:**裁决：** 本轮不要把 `DORM_CLEARANCE_BLOCKED` 纳入 signals Phase 2验收标准。可作为后续独立小任务处理：要么调整契约允许 `entity_type=student/application_attempt`，要么在阻断时创建可追踪的申请尝试记录。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:46:### P1：纯 signals 会把业务错误隐藏到模型保存副作用里
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:53:- 测试或管理命令直接创建模型时，signals 可能因缺少 `ClassMapping` 而让原本合法的模型保存失败；
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:57:**裁决：** 先建立 `apps.notifications.services`，提供幂等创建函数；业务入口或 signals 都调用该服务。不要把拼装和幂等逻辑散落在 receiver 里。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:75:成功提交路径依赖 `ClassMapping` 找到辅导员。当前 API 已在创建申请前校验映射存在，因此在 API 路径中安全；但 signals 会对所有 `Application.objects.create` 生效，包括测试、管理命令、shell脚本。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:77:**建议：** 若保留 signals，receiver 只在能解析出接收者时创建通知；解析失败应记录日志并跳过，不能破坏模型保存。更好的实现是由 `create_application` 在成功创建 `Approval` 后调用通知服务，因为此时接收者就是 `approval.approver`。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:93:不依赖 WeChat DevTools，能继续提高后端闭环价值；但不应写成“4种立即触发 + 纯 signals”。建议改为：
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:128:1. signals receiver 未在 `NotificationsConfig.ready()` 中加载，Django 不会自动注册。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:129:2. Django 4下 `default_app_config` 不可靠，当前 `INSTALLED_APPS` 使用的是 `'apps.notifications'`，若要在 notifications app 注册 signals，应改用 `'apps.notifications.apps.NotificationsConfig'` 或确认自动 config 发现行为。
backend/apps/users/integrations/xg_user_client.py:6:def generate_sign(
backend/apps/users/integrations/xg_user_client.py:13:    生成API签名
backend/apps/users/integrations/xg_user_client.py:15:    签名规则：
backend/apps/users/integrations/xg_user_client.py:27:        签名字符串（十六进制小写）
backend/apps/users/integrations/xg_user_client.py:37:    sign_str = ''.join(params)
backend/apps/users/integrations/xg_user_client.py:41:        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()
backend/apps/users/integrations/xg_user_client.py:43:        return hashlib.sha1(sign_str.encode('utf-8')).hexdigest()
backend/apps/users/integrations/xg_user_client.py:46:class XGUserAPIClient:

exec
/bin/bash -lc "rtk sed -n '1,180p' backend/.env.example" in /home/caohui/projects/graduation-leave-system
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

codex
I found an existing `81-step1a-completion-codex-response.md` in the discussion folder that appears to answer this same request. I’m still verifying the code and tests directly, because the final review should be grounded in current files rather than only copying that artifact.
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
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-80-step1a-completion-nex-2026-06-02T03-26-34-821Z.md
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
?? docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md
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
/bin/bash -lc "rtk sed -n '230,285p' docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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
/bin/bash -lc "rtk sed -n '35,110p' docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
**Codex指出：** 签名算法缺失，不能靠猜测实现。

**Claude确认：** **问题已解决！用户在审查过程中提供了官方签名算法。**

**官方签名算法（已确认）：**

```
签名规则：
1. 将 appSecret, timestamp, randStr 三个参数值进行字典排序（sort）
2. 拼接成字符串
3. 进行 sha1 或 md5 加密（默认sha1）

示例：
appSecret: 6bd1b3fb015b4e72a85769e9d64405d1
timestamp: 1573702840
randStr: Gc6LGToDKy2AMhXE

排序后拼接: 15737028406bd1b3fb015b4e72a85769e9d64405d1Gc6LGToDKy2AMhXE
sha1结果: baeaa6693fb7b9914c9ff9e388654878b8754515
```

**Python实现参考：**

```python
import hashlib

def generate_sign(app_secret: str, timestamp: str, rand_str: str, 
                  encryption_type: str = 'sha1') -> str:
    """
    生成API签名
    
    Args:
        app_secret: AppSecret密钥
        timestamp: Unix时间戳（字符串）
        rand_str: 随机字符串
        encryption_type: 加密类型，'sha1'或'md5'，默认'sha1'
    
    Returns:
        签名字符串（十六进制小写）
    """
    # 1. 将三个参数值进行字典排序
    params = [app_secret, timestamp, rand_str]
    params.sort()
    
    # 2. 拼接成字符串
    sign_str = ''.join(params)
    
    # 3. 进行加密
    if encryption_type == 'md5':
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    else:  # 默认sha1
        return hashlib.sha1(sign_str.encode('utf-8')).hexdigest()
```

**执行优先级：** 可以开始实现（阻塞已解除）

---

### P1：URL来源不一致（需要确认）

**Codex指出：** 
- 参考文档: `dev-saas-api.goliveplus.cn` 和 `saas.api.goliveplus.cn`
- 审查请求: `xuegongmj.hgnu.edu.cn`

**Claude确认：** 用户提供的URL是学校域名，应该是学校部署的网关或反向代理。

**修复方案：**
1. 使用用户提供的生产URL: `https://xuegongmj.hgnu.edu.cn/api/open-api/user-center/tenant/auth-user-info`
2. 在 `.env.example` 中注释说明测试/生产URL的区别
3. 通过环境变量 `XG_USER_API_URL` 配置

**执行优先级：** 实现时注意（环境变量配置）

---

### P1：租户Code获取（待确认）

exec
/bin/bash -lc "rtk sed -n '1,220p' docs/discussions/phase4c-next-steps/79-claude-codex-consensus-step1a.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# API测试Step 1分步实现 - Claude-Codex共识

**日期：** 2026-06-02  
**参与方：** Codex + Claude  
**文档编号：** 79

---

## 共识结论

**状态：** 达成共识，执行Step 1A（签名与配置切片）

---

## 关键共识

### 1. 实现策略

**Codex建议：** 分步实现（B方案）

**Claude接受：** ✅ 完全同意

**共识方案：**
- Step 1A: 签名与配置
- Step 1B: 请求构造与响应解析
- Step 1C: 诊断脚本

---

### 2. 租户Code策略

**共识：** A+C组合
- 代码实现不等待
- Mock测试立即做
- 真实API调用等待租户Code

---

### 3. 签名验证

**共识：** 官方样例作为P0单元测试
- `generate_sign()` 纯函数
- 必须通过官方样例验证
- 支持sha1/md5

---

### 4. 字段处理

**共识：** 宽松采样策略
- 接口结构严格
- 业务字段宽松
- Live后输出覆盖报告

---

## Step 1A 执行计划

### 交付文件

```
backend/apps/users/integrations/__init__.py
backend/apps/users/integrations/xg_user_client.py
backend/apps/users/tests/test_xg_user_client.py
```

### 验收标准

- [ ] `generate_sign()` 实现
- [ ] 官方样例测试通过
- [ ] md5支持
- [ ] 错误处理
- [ ] 配置校验

---

**下一步：** 执行Step 1A实现

exec
/bin/bash -lc "rtk sed -n '1,220p' docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md" in /home/caohui/projects/graduation-leave-system
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

codex
The implementation matches the confirmed official SHA1 sample. The main gap I see so far is test strength and the earlier Step 1A “配置校验” acceptance item, because the client class is still a placeholder.
exec
/bin/bash -lc "rtk python - <<'PY'
import hashlib
s=''.join(sorted(['secret','1234567890','random']))
print(s)
print(hashlib.md5(s.encode()).hexdigest())
PY" in /home/caohui/projects/graduation-leave-system
 exited 127 in 0ms:
[rtk: No such file or directory (os error 2)]

exec
/bin/bash -lc "rtk nl -ba backend/apps/users/tests/test_xg_user_client.py | sed -n '1,120p'" in /home/caohui/projects/graduation-leave-system
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
/bin/bash -lc "rtk nl -ba backend/apps/users/integrations/xg_user_client.py | sed -n '1,120p'" in /home/caohui/projects/graduation-leave-system
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

exec
/bin/bash -lc 'rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client -v 2 --keepdb --noinput' in /home/caohui/projects/graduation-leave-system
 succeeded in 716ms:
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
test_invalid_encryption_type (apps.users.tests.test_xg_user_client.GenerateSignTests.test_invalid_encryption_type)
测试非法加密类型 ... ok
System check identified no issues (0 silenced).
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

codex
The focused Django tests pass: 4 tests in 0.005s. One local `rtk python` helper command failed because of how `rtk` parsed the heredoc, so I’m using a simpler form for the checksum sanity check.
exec
/bin/bash -lc "rtk find backend -maxdepth 2 -type f -name 'manage.py' -o -name 'requirements.txt' -o -name 'pyproject.toml'" in /home/caohui/projects/graduation-leave-system
 exited 1 in 0ms:
rtk: rtk find does not support compound predicates or actions (e.g. -not, -exec). Use `find` directly.

exec
/bin/bash -lc "rtk python -c \"import hashlib; s=''.join(sorted(['secret','1234567890','random'])); print(s); print(hashlib.md5(s.encode()).hexdigest())\"" in /home/caohui/projects/graduation-leave-system
 exited 127 in 0ms:
[rtk: No such file or directory (os error 2)]

codex
The `rtk` wrapper is intentionally restrictive for some command forms; it does not affect the review result. I have enough evidence from the code, consensus docs, and Django test run to produce the review.
codex
I’m doing one last checksum verification inside the backend container, then I’ll give the review in the requested four-part format.
exec
/bin/bash -lc "rtk docker compose exec -T backend python -c \"import hashlib; s=''.join(sorted(['secret','1234567890','random'])); print(s); print(hashlib.md5(s.encode()).hexdigest())\"" in /home/caohui/projects/graduation-leave-system
 succeeded in 161ms:
1234567890randomsecret
2a471e23465cf11561ef7455fff00a86

codex
## 1. Step 1A审查结果

结论：签名纯函数可以通过，当前无 P0。

P1 问题：

1. MD5 测试断言过弱  
   [test_xg_user_client.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/tests/test_xg_user_client.py:28) 只校验长度和 hex 字符集，不能证明排序/拼接正确。建议改成固定值断言：`generate_sign('secret', '1234567890', 'random', 'md5') == '2a471e23465cf11561ef7455fff00a86'`。

2. 如果 Step 1A 仍定义为“签名与配置切片”，配置校验尚未完成  
   [xg_user_client.py](/home/caohui/projects/graduation-leave-system/backend/apps/users/integrations/xg_user_client.py:46) 的 `XGUserAPIClient` 仍是占位类。若 Step 1A 只验收签名函数，可通过；若按 doc 79 的“配置校验”验收，还需要配置对象和缺失配置测试。

P2 建议：

- 空字符串校验放在配置/请求构建层，不要污染 `generate_sign()` 纯函数。
- 特殊字符/Unicode 不是 P0；当前 UTF-8 行为确定。`randStr` 后续建议限制为 ASCII。
- `XG_USER_API_ENCRYPTION_TYPE` 的 `strip().lower()` 归一化应放在配置层。

验证：已运行 `rtk docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client -v 2 --keepdb --noinput`，4/4 passed。

## 2. 下一步策略建议

建议采用“修正后的选项A”：先补 Step 1A 小修正，再做 Step 1B-lite，然后做 Step 1C。

不建议纯选项B先写孤立诊断脚本。诊断脚本本身也要构造 headers/form-data、签名、超时、错误分类和脱敏输出；如果不先有可复用客户端层，后续容易重复实现并产生不一致。

## 3. Step 1C范围确认

Step 1C 应是安全诊断入口：

- 必须包含：环境变量校验、官方签名样例自检、默认 dry-run、`XG_RUN_LIVE_API_TEST=1` 才允许 live probe、固定 `page=1/pageNum=1`、短超时、错误分类、脱敏输出。
- 可支持：`--format=json`、`--timeout`。
- 应避免：完整 headers、完整 `sign`、完整响应 body、分页循环、落库、Provider 接入、CI 中默认 live 调用。

## 4. Step 1B范围界定

Step 1B-lite 应包含：

- `XGUserAPIConfig` 或等价配置对象。
- `build_headers()`：`appKey/timestamp/randStr/sign/encryptionType`，timestamp/randStr 可注入便于测试。
- `build_form_data()`：`tenantCode/page/pageNum`，默认单页一条。
- `fetch_users_page()`：单页请求、短超时、可注入 session。
- 基础响应解析和 mock 测试：成功、HTTP错误、网络异常、业务错误、schema异常、缺失配置、非法加密类型。

应排除：全量分页、重试机制、Provider 接入、数据库写入、字段业务映射、真实API进入常规测试。
tokens used
56,693

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
