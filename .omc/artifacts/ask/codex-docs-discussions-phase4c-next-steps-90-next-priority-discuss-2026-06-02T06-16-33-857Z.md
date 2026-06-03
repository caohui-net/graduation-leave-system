# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-02T06:16:33.857Z

## Original task

docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md

## Final prompt

docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md

## Raw output

```text
已完成 Codex 审查响应，产出：

[91-next-priority-codex-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md)

核心结论：推荐 **A-prime：先做 Step 2C-lite 字段映射契约**，不要直接进入写库同步命令。Step 3 应先做只读 mapper / `UserInfoProvider` 和测试；DB upsert 与 management command 放到后续 Step 4/5。

我也已按协作协议记录事件：`.omc/collaboration/events.jsonl` 新增 event `102`，`state.json` 更新为 `waiting_for_claude_response`。本次是文档审查，未 rerun 测试。


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
session id: 019e86f6-b711-7523-ad73-f98c1e59e97d
--------
user
docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md
codex
I’ll read the project command rules first, then open the discussion request so I can respond in the expected format.
exec
/bin/bash -lc "sed -n '1,220p' /home/caohui/.codex/RTK.md && sed -n '1,220p' docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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
# Phase 4C 下一步优先级讨论 - 审查请求

**日期：** 2026-06-02  
**审查人：** Codex  
**文档编号：** 90  
**前置文档：** 89 (Claude响应Codex审查，执行完成)

---

## 背景

Step 2B已完成并验证：
- XG API客户端：schema校验 + 无界循环保护 + max_pages校验
- 诊断脚本：tenant_invalid分类优化
- 测试套件：38个测试全部通过（新增9个边界测试）

**验证证据：**
```
docker compose exec -T backend python manage.py test apps.users.tests.test_xg_user_client --keepdb --noinput
Ran 38 tests in 0.072s
OK
```

**修改文件：**
1. `backend/apps/users/integrations/xg_user_client.py`
2. `backend/scripts/diagnose_xg_api.py`
3. `backend/apps/users/tests/test_xg_user_client.py`

---

## 审查问题

### 主问题：下一步优先级是什么？

根据doc 86共识，剩余工作包括：

**选项A：Step 2C - 字段覆盖报告**
- doc 86原话："Step 2C：字段覆盖报告（依赖Step 2A结果）"
- 由于Step 2A未执行（无凭证），需基于文档样例创建字段覆盖草案
- 目的：明确哪些字段必填、可选、格式要求
- 产出：字段映射表（学工→系统内部模型）

**选项B：Step 3 - 学生数据同步命令**
- 创建Django management command
- 使用XG API客户端读取学生数据
- 映射到内部Student模型并入库
- 需依赖字段覆盖规则（Step 2C）

**选项C：跳过Step 2C，直接实现Step 3**
- 理由：字段覆盖可以在实现时边做边确定
- 风险：可能需要返工调整字段映射

**选项D：其他优先级**
- 前端集成？
- 文档完善？
- 其他遗漏工作？

---

## 审查要点

请Codex评估以下问题：

1. **依赖关系分析**
   - Step 3是否强依赖Step 2C？
   - 能否在实现Step 3时增量确定字段覆盖？

2. **风险评估**
   - 直接跳到Step 3的风险有多大？
   - 缺失字段覆盖文档会导致什么问题？

3. **效率考量**
   - 先做Step 2C再做Step 3 vs 边做Step 3边确定字段
   - 哪种方式更快达到可工作状态？

4. **遗漏检查**
   - Step 2系列是否还有遗漏工作？
   - 是否需要补充其他基础设施？

---

## 期望输出

1. **推荐优先级：** 明确下一步应该做什么（A/B/C/D或其他）
2. **理由：** 为什么这是最优选择
3. **风险：** 选择该优先级的潜在风险
4. **替代方案：** 如果有更好的思路请提出

---

## 约束条件

- 无学工系统真实凭证（无法执行live测试）
- XG API客户端已完整实现且测试覆盖充分
- 用户要求持续推进直到项目完成
- 需要Claude-Codex达成共识后再执行

---

**请Codex审查并给出建议。**

codex
I have the request. Because this is a formal Codex review in the project’s collaboration flow, I’m going to read the local collaboration and review protocols before giving the recommendation.
exec
/bin/bash -lc "rtk sed -n '1,240p' .omc/collaboration/protocol.md" in /home/caohui/projects/graduation-leave-system
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

codex
I need a little more project context before I can make the priority call defensibly: the prior consensus/response docs and the current XG client/model shape.
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/phase4c-next-steps/89-*" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Phase 4C Step 2B实现审查 - Claude响应

**响应日期：** 2026-06-02  
**针对：** `88-step2b-implementation-codex-response.md`  
**文档编号：** 89

---

## 对Codex审查的总体回应

**结论：完全同意Codex的评估和修复建议。**

Codex识别的3个问题（2个P1 + 1个P2）都是真实风险，与doc 85-86共识要求完全一致：

1. ✅ **P1问题准确**：缺失`data.data`被误判为空数据，违反"schema异常显式暴露"要求
2. ✅ **P1问题关键**：无界循环风险直接违反"防无限循环保护"要求
3. ✅ **P2问题合理**：`max_pages`校验缺失导致参数语义不明确
4. ✅ **测试覆盖gap真实**：遗漏doc 85明确要求的边界场景
5. ✅ **tenant_invalid顺序风险有效**：403+tenant msg应优先识别

无分歧点，立即执行修复。

---

## 问题确认与修复方案

### P1-1：data.data缺失误判

**Codex指出：** line 138-141使用`result.get('data', {}).get('data', [])`，缺失时返回空列表，line 182返回`stopped_reason='empty'`，掩盖schema错误。

**Claude确认：** 完全同意。真实场景中，接口可能返回：
- `{'code': 200, 'data': null}` - data字段为null
- `{'code': 200, 'data': {}}` - data对象缺data字段
- `{'code': 200}` - 完全缺失data字段

当前实现会把这些schema错误误判为"0用户成功读取"，后续同步时会误认为数据源为空。

**修复方案（最小修改）：**
```python
# backend/apps/users/integrations/xg_user_client.py: fetch_users_page()
# 当前（line 135-142）：
return {
    'code': result.get('code'),
    'msg': result.get('msg', ''),
    'current_page': result.get('data', {}).get('current_page'),
    'per_page': result.get('data', {}).get('per_page'),
    'total': result.get('data', {}).get('total'),
    'users': result.get('data', {}).get('data', [])  # ← 问题：缺失返回[]
}

# 修复后：
data = result.get('data')
if data is None:
    raise ValueError("Response missing 'data' field")
if 'data' not in data:
    raise ValueError("Response data missing 'data' (user list) field")
users = data['data']
if not isinstance(users, list):
    raise ValueError(f"Response data.data must be list, got {type(users).__name__}")

return {
    'code': result.get('code'),
    'msg': result.get('msg', ''),
    'current_page': data.get('current_page'),
    'per_page': data.get('per_page'),
    'total': data.get('total'),
    'users': users
}
```

---

### P1-2：无界循环风险

**Codex指出：** line 158 `while True`缺少`current_page`前进检查和元数据校验，可能无限循环。

**Claude确认：** 完全同意。当前退出条件：
1. `max_pages`达到（可选）
2. `users`为空
3. `total/current_page/per_page`计算完成

如果接口持续返回非空users但缺失分页元数据，或`current_page`不前进，会无限循环。

**修复方案：**
```python
# backend/apps/users/integrations/xg_user_client.py: fetch_all_users()
# 在while循环开始前：
all_users = []
page = 1
total = None
prev_current_page = None  # ← 新增：跟踪上一页的current_page

while True:
    result = self.fetch_users_page(page=page, page_num=page_size, timeout=timeout, session=session)
    
    # ... 业务码检查 ...
    
    users = result['users']
    current_page = result['current_page']
    per_page = result['per_page']
    total = result['total']
    
    # ← 新增：校验current_page前进
    if current_page is not None:
        current_page_int = int(current_page) if isinstance(current_page, str) else current_page
        if prev_current_page is not None and current_page_int <= prev_current_page:
            raise ValueError(f"Pagination not advancing: current_page={current_page_int}, previous={prev_current_page}")
        prev_current_page = current_page_int
    
    # ← 新增：校验per_page有效性
    if per_page is not None:
        per_page_int = int(per_page) if isinstance(per_page, str) else per_page
        if per_page_int <= 0:
            raise ValueError(f"Invalid per_page: {per_page_int}, must be positive")
        per_page = per_page_int
    
    all_users.extend(users)
    
    # 现有终止条件...
```

---

### P2：max_pages校验缺失

**Codex指出：** line 179使用`if max_pages`，`max_pages=0`被当作无限制。

**Claude确认：** 同意。当前`if max_pages and page >= max_pages`在`max_pages=0`时不触发，`max_pages=-1`时会在第1页后返回。

**修复方案：**
```python
# backend/apps/users/integrations/xg_user_client.py: fetch_all_users()
# 在函数开始处（line 148后）：
if page_size <= 0:
    raise ValueError(f"page_size must be positive, got {page_size}")
if max_pages is not None and max_pages <= 0:  # ← 新增
    raise ValueError(f"max_pages must be positive or None, got {max_pages}")
```

---

### tenant_invalid顺序优化

**Codex指出：** 403+tenant msg应优先于通用401/403判断。

**Claude确认：** 同意。当前顺序会导致`{'code': 403, 'msg': '租户不存在'}`被归为`auth_failed`而非`tenant_invalid`。

**修复方案：**
```python
# backend/scripts/diagnose_xg_api.py: live_probe()
# 当前（line 91-98）：
elif result['code'] in (401, 403):
    return {'status': 'ERROR', 'error': 'auth_failed', ...}
elif result['code'] in (404, 40001, 40002):
    return {'status': 'ERROR', 'error': 'tenant_invalid', ...}
elif 'tenant' in result.get('msg', '').lower() or '租户' in result.get('msg', ''):
    return {'status': 'ERROR', 'error': 'tenant_invalid', ...}

# 修复后（调整顺序）：
elif 'tenant' in result.get('msg', '').lower() or '租户' in result.get('msg', ''):
    return {'status': 'ERROR', 'error': 'tenant_invalid', ...}
elif result['code'] in (401, 403):
    return {'status': 'ERROR', 'error': 'auth_failed', ...}
elif result['code'] in (404, 40001, 40002):
    return {'status': 'ERROR', 'error': 'tenant_invalid', ...}
```

---

## 修复清单

立即执行以下修复（按优先级）：

### 修复1：fetch_users_page() schema校验（P1-1）
**文件：** `backend/apps/users/integrations/xg_user_client.py:135-142`
**改动：** 显式检查`data`和`data.data`存在性，缺失抛ValueError
**预计时间：** 5分钟

### 修复2：fetch_all_users() 无界保护（P1-2）
**文件：** `backend/apps/users/integrations/xg_user_client.py:158+`
**改动：**
- 跟踪`prev_current_page`，检查前进
- 校验`per_page > 0`
**预计时间：** 10分钟

### 修复3：max_pages参数校验（P2）
**文件：** `backend/apps/users/integrations/xg_user_client.py:148`
**改动：** 增加`max_pages is not None and max_pages <= 0`检查
**预计时间：** 2分钟

### 修复4：tenant_invalid顺序（小优化）
**文件：** `backend/scripts/diagnose_xg_api.py:91-98`
**改动：** 消息检查移到401/403前
**预计时间：** 2分钟

### 修复5：补充测试（覆盖gap）
**文件：** `backend/apps/users/tests/test_xg_user_client.py`
**新增：**
- test_fetch_users_page_missing_data_field
- test_fetch_users_page_missing_data_data_field
- test_fetch_users_page_users_not_list
- test_fetch_all_users_current_page_not_advancing
- test_fetch_all_users_per_page_zero
- test_fetch_all_users_per_page_invalid_string
- test_fetch_all_users_max_pages_zero
- test_fetch_all_users_max_pages_negative
- test_fetch_all_users_page_size_one (doc 86要求)
**预计时间：** 20分钟

---

## 执行授权

根据用户指令"在得到统一可靠可行的执行方案后，无需我的干预，直接执行"：

✅ Codex与Claude达成完整共识  
✅ 5项修复明确且必要  
✅ 无分歧点  

**授权立即执行：**
1. 修复1-4（代码修正，19分钟）
2. 修复5（测试补充，20分钟）
3. 运行测试验证（预计37-41个测试）
4. 更新文档并提交

预计总耗时：40-45分钟

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/phase4c-next-steps/86-*" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Phase 4C Step 2策略 - Claude响应

**响应日期：** 2026-06-02  
**针对：** `85-post-step1-next-strategy-codex-response.md`  
**文档编号：** 86

---

## 对Codex审查的总体回应

**结论：完全同意Codex的A+B组合策略和5步路径规划。**

Codex的核心论点准确且有说服力：

1. **风险门vs硬阻塞区分清晰**：真实API测试价值高，但不应阻塞可独立验证的分页逻辑
2. **范围界定精准**：每步边界明确，避免过早引入Provider复杂度
3. **风险识别全面**：7个风险点+缓解措施实用
4. **外部依赖备选方案现实**：CSV降级路径合理

无重大分歧点，可直接执行。

---

## 问题确认与补充

### Codex识别的Gap

**Gap 1：tenant_invalid错误分类缺失**

**Codex指出：** `live_probe()` 现在只把401/403归为`auth_failed`，其他业务码统一归为`business_error`，缺少`tenant_invalid`分类。

**Claude确认：** 同意。当前实现不够细化，租户错误和其他业务错误混在一起，排障困难。

**修复方案：**
```python
# backend/scripts/diagnose_xg_api.py: live_probe()
if result['code'] in (401, 403):
    return {'status': 'ERROR', 'error': 'auth_failed', ...}
elif result['code'] in (404, 40001, 40002):  # 租户相关错误码
    return {'status': 'ERROR', 'error': 'tenant_invalid', ...}
elif 'tenant' in result.get('msg', '').lower() or '租户' in result.get('msg', ''):
    return {'status': 'ERROR', 'error': 'tenant_invalid', ...}
else:
    return {'status': 'ERROR', 'error': 'business_error', ...}
```

**执行时机：** Step 2A前修复（5分钟）

---

### Claude补充的执行细节

**细节1：Step 2A和Step 2B可以并行吗？**

**Codex建议顺序：** Step 2A → Step 2B → Step 2C

**Claude分析：**
- Step 2A（live probe）：依赖真实凭证，可能阻塞
- Step 2B（分页逻辑）：纯代码+mock，不依赖真实API

**建议：** Step 2A和Step 2B可并行开发：
1. **如果凭证可用**：先执行Step 2A（10分钟），然后Step 2B（30-40分钟）
2. **如果凭证不可用**：直接执行Step 2B，Step 2A标记为pending

**理由：** 分页逻辑的mock测试不依赖真实API，可独立验证正确性。

---

**细节2：fetch_all_users()返回格式？**

**Codex建议：** `fetch_all_users(page_size=100, max_pages=None, timeout=5, session=None)`

**Claude补充：**

返回格式建议：
```python
{
    'users': [...],  # 所有页累积的用户列表
    'total': 123,    # total字段（如果可用）
    'pages_fetched': 3,  # 实际请求的页数
    'stopped_reason': 'complete'  # complete/max_pages/empty/error
}
```

**理由：**
- `users`：调用方需要的核心数据
- `total`：用于验证数据完整性
- `pages_fetched`：调试和监控
- `stopped_reason`：区分正常结束vs被max_pages截断

---

**细节3：mock测试的page_size选择？**

**Codex建议：** `page_size=100`

**Claude补充：** mock测试应覆盖多种page_size：
- `page_size=1`：验证分页逻辑正确性（total=3，应请求3次）
- `page_size=10`：常规场景
- `page_size=100`：生产推荐值

**理由：** page_size=1时分页逻辑最容易暴露边界条件错误。

---

## 执行计划确认

### 立即执行：tenant_invalid修复（5分钟）

**文件：** `backend/scripts/diagnose_xg_api.py`

**修改：** 在`live_probe()`中增加租户错误分类逻辑

**验证：** 无需测试（纯逻辑分支，真实触发需要错误响应）

---

### 随后执行：Step 2A - 条件式live probe（10分钟，如果凭证可用）

**前提条件：**
- 真实凭证（AppId/AppKey/AppSecret）
- 本校tenantCode: S10405
- `XG_RUN_LIVE_API_TEST=1`

**执行步骤：**
1. 创建`.env`文件（从`.env.example`复制）
2. 填入真实凭证
3. 运行：`python backend/scripts/diagnose_xg_api.py --format=json`
4. 记录结果（成功：字段覆盖报告；失败：问题清单）

**输出：** 脱敏诊断报告（保存到`docs/phase4c-live-probe-result.md`）

**如果凭证不可用：** 跳过Step 2A，标记为pending，直接进入Step 2B

---

### 核心执行：Step 2B - fetch_all_users()分页（30-40分钟）

**文件：** `backend/apps/users/integrations/xg_user_client.py`

**新增方法：**
```python
def fetch_all_users(
    self, 
    page_size: int = 100, 
    max_pages: int = None, 
    timeout: int = 5, 
    session=None
) -> dict:
    """分页读取所有用户"""
    # 实现略（遵循Codex的范围界定）
```

**测试文件：** `backend/apps/users/tests/test_xg_user_client.py`

**新增测试场景（8个）：**
1. 单页成功（total=5, page_size=10）
2. 多页成功（total=25, page_size=10，应请求3页）
3. 空数据（total=0, users=[]）
4. 最后一页不足page_size（total=25, page_size=10，第3页只有5条）
5. per_page字符串兼容（per_page="10"）
6. 中间页HTTP错误（第2页500错误，应抛异常）
7. 中间页业务错误（第2页code=500，应抛异常）
8. max_pages限制（total=100, page_size=10, max_pages=3，应停在第3页）

**验证：** 测试通过（预计21+8=29测试）

---

### 待定执行：Step 2C - 字段覆盖报告（依赖Step 2A结果）

**前提条件：** Step 2A成功获取真实响应

**输出文件：** `docs/phase4c-field-coverage-report.md`

**内容：**
- 学工API提供的字段清单
- 本系统User model需要的字段清单
- 覆盖情况（完全覆盖/部分覆盖/缺失）
- 缺失字段的备选方案（CSV/手工维护/默认值）

**如果Step 2A未执行：** 基于文档样例创建字段覆盖草案

---

## 共识确认

**与Codex达成以下共识：**

1. ✅ 真实API测试作"早期风险门"，不阻塞分页实现
2. ✅ Step 2顺序：2A（条件式live probe）+ 2B（分页mock）+ 2C（字段覆盖）
3. ✅ 分页逻辑严格限制在客户端层，不接Provider/DB
4. ✅ Phase 4C完整路径：5步清晰界定
5. ✅ 外部依赖阻塞时CSV降级合理
6. ✅ 需修复tenant_invalid分类缺失

**补充共识：**

7. ✅ Step 2A和2B可并行（如果凭证不可用，2A可跳过）
8. ✅ fetch_all_users()返回格式包含users/total/pages_fetched/stopped_reason
9. ✅ mock测试覆盖page_size=1场景（暴露边界条件）
10. ✅ 立即修复tenant_invalid分类gap

**无分歧点，可直接执行。**

---

## 执行授权

根据用户指令"在得到统一可靠可行的执行方案后，无需我的干预，直接执行"：

✅ Codex与Claude已达成完整共识  
✅ 执行方案明确且可行  
✅ 无分歧点  

**授权立即执行：**
1. tenant_invalid修复（5分钟）
2. Step 2A条件式live probe（10分钟，如果凭证可用）
3. Step 2B fetch_all_users()分页（30-40分钟）
4. Step 2C字段覆盖报告（依赖2A结果）

预计总耗时：45-55分钟（如果凭证可用）/ 35-45分钟（如果凭证不可用）

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


class XGUserAPIConfig:
    """学工系统API配置"""

    def __init__(self):
        import os
        self.url = os.getenv('XG_USER_API_URL', '').strip()
        self.app_id = os.getenv('XG_USER_API_APP_ID', '').strip()
        self.app_key = os.getenv('XG_USER_API_APP_KEY', '').strip()
        self.app_secret = os.getenv('XG_USER_API_APP_SECRET', '').strip()
        self.tenant_code = os.getenv('XG_USER_API_TENANT_CODE', '').strip()
        encryption_type = os.getenv('XG_USER_API_ENCRYPTION_TYPE', 'sha1').strip().lower()

        if encryption_type not in ('sha1', 'md5'):
            raise ValueError(f"XG_USER_API_ENCRYPTION_TYPE must be 'sha1' or 'md5', got '{encryption_type}'")
        self.encryption_type = encryption_type

        self._validate()

    def _validate(self):
        """校验必填配置项"""
        if not self.url:
            raise ValueError("XG_USER_API_URL is required")
        if not self.app_key:
            raise ValueError("XG_USER_API_APP_KEY is required")
        if not self.app_secret:
            raise ValueError("XG_USER_API_APP_SECRET is required")
        if not self.tenant_code:
            raise ValueError("XG_USER_API_TENANT_CODE is required")

    def is_live_test_enabled(self) -> bool:
        """检查是否启用真实API测试"""
        import os
        return os.getenv('XG_RUN_LIVE_API_TEST', '0').strip() == '1'


class XGUserAPIClient:
    """学工系统用户API客户端"""

    def __init__(self, config: XGUserAPIConfig):
        self.config = config

    def build_headers(self, timestamp: str = None, rand_str: str = None) -> dict:
        """构造请求headers"""
        import time
        import random
        import string

        if timestamp is None:
            timestamp = str(int(time.time()))
        if rand_str is None:
            rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

        sign = generate_sign(self.config.app_secret, timestamp, rand_str, self.config.encryption_type)

        return {
            'appKey': self.config.app_key,
            'timestamp': timestamp,
            'randStr': rand_str,
            'sign': sign,
            'encryptionType': self.config.encryption_type
        }

    def build_form_data(self, page: int = 1, page_num: int = 1) -> dict:
        """构造form-data"""
        return {
            'tenantCode': self.config.tenant_code,
            'page': str(page),
            'pageNum': str(page_num)
        }

    def fetch_users_page(self, page: int = 1, page_num: int = 1, timeout: int = 5, session=None) -> dict:
        """请求单页用户数据"""
        import requests

        if session is None:
            session = requests.Session()

        headers = self.build_headers()
        data = self.build_form_data(page, page_num)

        response = session.post(self.config.url, headers=headers, data=data, timeout=timeout)
        response.raise_for_status()

        result = response.json()

        # 协议层解析
        if 'code' not in result:
            raise ValueError("Response missing 'code' field")

        data = result.get('data')
        if data is None:
            raise ValueError("Response missing 'data' field")
        if 'data' not in data:
            raise ValueError("Response data missing 'data' (user list) field")
        users = data['data']
        if not isinstance(users, list):
            raise ValueError(f"Response data.data must be list, got {type(users).__name__}")

        return {
            'code': result.get('code'),
            'msg': result.get('msg', ''),
            'current_page': data.get('current_page'),
            'per_page': data.get('per_page'),
            'total': data.get('total'),
            'users': users
        }

    def fetch_all_users(self, page_size: int = 100, max_pages: int = None, timeout: int = 5, session=None) -> dict:
        """分页读取所有用户"""
        import requests

        if page_size <= 0:
            raise ValueError(f"page_size must be positive, got {page_size}")
        if max_pages is not None and max_pages <= 0:
            raise ValueError(f"max_pages must be positive or None, got {max_pages}")

        if session is None:
            session = requests.Session()

        all_users = []
        page = 1
        total = None
        prev_current_page = None

        while True:
            result = self.fetch_users_page(page=page, page_num=page_size, timeout=timeout, session=session)

            if result['code'] != 200:
                raise ValueError(f"Business error: code={result['code']}, msg={result['msg']}")

            users = result['users']
            if not isinstance(users, list):
                raise ValueError(f"users must be list, got {type(users).__name__}")

            all_users.extend(users)

            current_page = result['current_page']
            per_page = result['per_page']
            total = result['total']

            # 转换per_page为整数并校验
            if per_page is not None:
                per_page = int(per_page) if isinstance(per_page, str) else per_page
                if per_page <= 0:
                    raise ValueError(f"Invalid per_page: {per_page}, must be positive")

            # 校验current_page前进
            if current_page is not None:
                current_page_int = int(current_page) if isinstance(current_page, str) else current_page
                if prev_current_page is not None and current_page_int <= prev_current_page:
                    raise ValueError(f"Pagination not advancing: current_page={current_page_int}, previous={prev_current_page}")
                prev_current_page = current_page_int

            # 判断是否结束
            if max_pages and page >= max_pages:
                return {'users': all_users, 'total': total, 'pages_fetched': page, 'stopped_reason': 'max_pages'}

            if not users:
                return {'users': all_users, 'total': total, 'pages_fetched': page, 'stopped_reason': 'empty'}

            if total is not None and current_page is not None and per_page is not None:
                total_pages = (int(total) + per_page - 1) // per_page
                if int(current_page) >= total_pages:
                    return {'users': all_users, 'total': total, 'pages_fetched': page, 'stopped_reason': 'complete'}

            page += 1

exec
/bin/bash -lc "rtk rg -n \"class Student|Student\\(\" backend/apps -g '*.py'" in /home/caohui/projects/graduation-leave-system
 exited 1 in 0ms:
codex
The client now has the pagination and schema guardrails from the previous review, so the remaining question is less about client correctness and more about synchronization contract risk. I’m checking the internal user/student model and any existing Phase 4C docs so the recommendation maps to actual fields rather than abstract process.
exec
/bin/bash -lc 'rtk ls -la docs/discussions/phase4c-next-steps' in /home/caohui/projects/graduation-leave-system
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

exec
/bin/bash -lc "rtk sed -n '1,240p' backend/apps/users/models.py" in /home/caohui/projects/graduation-leave-system
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
/bin/bash -lc "rtk rg -n \"student|Student|stu|学号|姓名|college|major|grade|class|phone|email|User\" backend/apps docs/discussions/phase4c-next-steps -g '*.py' -g '*.md'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:58:- 新增断言1：`Application.objects.filter(student=blocked_student).count() == 0`
docs/discussions/phase4c-next-steps/65-phase2b-option1-execution-review-request.md:60:- 新增断言2：`Notification.objects.filter(recipient=blocked_student).count() == 0`
docs/discussions/phase4c-next-steps/42-claude-consensus-phase2a-stabilization.md:39:- `entity_type=student`引入语义债务（无法表达多次尝试上下文）
docs/discussions/phase4c-next-steps/58-claude-codex-consensus-option-a-prime-partial.md:31:   - 字段：access_token, token_type, user（AuthUserSerializer）
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:18:4. ✅ student_id作实体会让幂等粒度过粗
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:69:- 添加断言：Application.objects.filter(student=blocked_student).count() == 0
docs/discussions/phase4c-next-steps/64-claude-response-accept-option-1.md:70:- 添加断言：Notification.objects.filter(recipient=blocked_student).count() == 0
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:132:- `XGUserAPIClient.build_headers()`
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:133:- `XGUserAPIClient.build_form_data()`
docs/discussions/phase4c-next-steps/78-claude-response-accept-step1-segmented.md:134:- `XGUserAPIClient.fetch_users_page()`
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:35:- Counselor access checks `application.class_id == user.class_id` or matching approval.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:36:- Application detail checks `ClassMapping(counselor=user, class_id=application.class_id, active=True)`.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:72:- Upload success: student uploads to own application.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:73:- Upload forbidden: student cannot upload to another student's application; counselor/dean cannot upload.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:75:- List visibility: student own positive, student other negative, assigned counselor positive, cross-counselor negative, assigned dean positive or negative according to the final RBAC decision.
docs/discussions/phase4c-next-steps/02-codex-phase4c-strategy-review.md:77:- Delete: owner student soft-deletes; non-owner student and staff are forbidden; list/download exclude deleted attachments.
docs/discussions/phase4c-next-steps/44-codex-post-phase2a-stabilization-next-strategy-response.md:86:- 辅导员通知：`type=application_submitted`、`entity_type=approval`、`message`包含学生姓名或学号。
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:24:   - 导出 `generate_sign` 和 `XGUserAPIClient`
docs/discussions/phase4c-next-steps/80-step1a-completion-next-review-request.md:29:   - `XGUserAPIClient` 类（占位符，待实现）
docs/discussions/phase4c-next-steps/84-post-step1-next-strategy-request.md:21:  - XGUserAPIConfig：环境读取+校验+归一化
docs/discussions/phase4c-next-steps/84-post-step1-next-strategy-request.md:22:  - XGUserAPIClient：build_headers() + build_form_data() + fetch_users_page()
docs/discussions/phase4c-next-steps/84-post-step1-next-strategy-request.md:40:- Provider接入（UserInfoProvider）
docs/discussions/phase4c-next-steps/84-post-step1-next-strategy-request.md:93:- 创建 `UserInfoProvider`
docs/discussions/phase4c-next-steps/84-post-step1-next-strategy-request.md:95:- 调用 `XGUserAPIClient` 获取数据
docs/discussions/phase4c-next-steps/84-post-step1-next-strategy-request.md:96:- 写入数据库（User model）
docs/discussions/phase4c-next-steps/84-post-step1-next-strategy-request.md:139:   - `XGUserAPIClient.fetch_all_users()` 方法
docs/discussions/phase4c-next-steps/07-claude-response-to-codex-strategy-review.md:39:4. 不在`student-application`页面添加上传功能
docs/discussions/phase4c-next-steps/01-claude-phase4c-strategy-proposal.md:78:   - list权限 (RBAC: 学生own/辅导员class/学工部dean)
docs/discussions/phase4c-next-steps/74-claude-response-accept-codex-with-algo.md:285:- 可以考虑接入 `RealUserDataProvider`
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:13:**根因：** `@parser_classes([MultiPartParser, FormParser])` 装饰器位置错误
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:28:@permission_classes([IsAuthenticated])
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:32:@parser_classes([MultiPartParser, FormParser])
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:40:@permission_classes([IsAuthenticated])
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:41:@parser_classes([MultiPartParser, FormParser])  # 移到这里
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:49:**修改内容：** 将 `@parser_classes` 装饰器从 `upload_attachment()` 移到 `attachments_view()`
docs/discussions/phase4c-next-steps/17-claude-p0-fix-verification-summary.md:73:  - test_upload_forbidden_other_student ✅
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:60:    if user.role == UserRole.STUDENT:
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:61:        return application.student_id == user.user_id
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:63:    if user.role == UserRole.COUNSELOR:
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:66:            class_id=application.class_id,
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:70:    if user.role == UserRole.DEAN:
docs/discussions/phase4c-next-steps/04-codex-response-to-claude.md:98:- upload/delete limited to owning student
docs/discussions/phase4c-next-steps/83-consensus-step1b-lite-first.md:58:- `XGUserAPIConfig`：环境读取+校验+归一化
docs/discussions/phase4c-next-steps/83-consensus-step1b-lite-first.md:59:- `XGUserAPIClient`：headers构造+form-data构造+单页请求
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:127:- `xg_user_client.py`：可复用客户端，负责签名、请求构造、响应解析、错误归一化；后续可接入 `RealUserDataProvider`。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:140:5. 字段采样：仅检查人员记录是否包含 `name/number/phone/identity_id/department/user_identity/updated_at` 等文档字段。
docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md:146:- 按姓名/手机号过滤的生产验证。
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:41:- Attachment: `application.class_id == user.class_id` OR matching approval
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:42:- Application detail: `ClassMapping(counselor=user, class_id=application.class_id, active=True)`
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:56:    if user.role == UserRole.STUDENT:
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:57:        return application.student_id == user.user_id
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:59:    elif user.role == UserRole.COUNSELOR:
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:60:        # Must have active class mapping
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:63:            class_id=application.class_id,
docs/discussions/phase4c-next-steps/03-claude-response-to-codex-review.md:67:    elif user.role == UserRole.DEAN:
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:23:   - 在 `XGUserAPIClient` 内实现 `fetch_all_users()` 或同等迭代能力。
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:128:- 确定学工字段到本系统 `User`/班级/角色/辅导员关系的映射。
docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md:130:- 设计 `UserInfoProvider` 接口和降级策略。
docs/discussions/phase4c-next-steps/54-claude-codex-consensus-option-a-execution.md:63:✓ 不重构为class-based views  
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:46:Apply `@parser_classes([MultiPartParser, FormParser])` to the DRF entrypoint, or split the upload/list handlers into separately decorated DRF views routed by method/path. After the fix, rerun the 19 explicit attachment tests.
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:64:Either fix the upload parser issue and rerun all 19 tests, or downgrade the implementation status to reflect that only list tests are currently passing.
docs/discussions/phase4c-next-steps/15-codex-p1-implementation-review-response.md:74:The new attachment elements use classes such as `attachment-error`, `empty-attachments`, `attachment-list`, `attachment-item`, `attachment-info`, `attachment-actions`, `btn-small`, and `btn-upload`, but `detail.wxss` does not define them.
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:44:**裁决：** 本轮不要把 `DORM_CLEARANCE_BLOCKED` 纳入 signals Phase 2验收标准。可作为后续独立小任务处理：要么调整契约允许 `entity_type=student/application_attempt`，要么在阻断时创建可追踪的申请尝试记录。
docs/discussions/phase4c-next-steps/38-codex-post-phase1-next-strategy-response.md:73:**位置：** `backend/apps/users/class_mapping.py:5-9`、`backend/apps/applications/views.py:107-132`
docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.md:98:1. **配置对象**：`XGUserAPIConfig`
docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.md:104:2. **请求构造**：`XGUserAPIClient`
docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.md:137:- Provider接入（`UserInfoProvider`）
docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.md:138:- 数据库写入（`User.objects.create`）
docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.md:154:   - 调用 `XGUserAPIConfig` 校验
docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.md:168:   - 调用 `XGUserAPIClient.fetch_users_page()`
docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.md:187:   - 响应：姓名显示首字+星，手机号显示前3后4，学号显示前2后4
docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.md:206:  - 新增 `XGUserAPIConfig` 类
docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.md:207:  - 扩展 `XGUserAPIClient` 类
docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md:61:- **Option 3：** 扩展通知实体类型（dorm_clearance或student），定义幂等键
docs/discussions/phase4c-next-steps/53-codex-confirmation-option-a-corrected.md:14:Claude在52号文档中已经接受51号审查的关键修正：先执行B-mini smoke typo清理，再执行A-corrected API Schema P1；采用文档化方式保持schema与当前运行时行为一致；不在本阶段引入全局错误包装、class-based view重构、通知分页行为修改或Track 3 Phase 2B/2C。
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:140:- `name` - 姓名
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:141:- `number` - 工号/学号
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:142:- `phone` - 手机号
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:149:- 是否包含班级信息？（需要class_id映射辅导员）
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:176:✓ 字段采样: name, number, phone存在
docs/discussions/phase4c-next-steps/76-claude-post-step0-next-strategy-request.md:188:    "fields_present": ["name", "number", "phone"]
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:113:const isOwner = userInfo.role === 'student' && detail.student_id === userInfo.user_id;
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:144:<view class="section">
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:145:  <text class="section-title">附件</text>
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:146:  <view class="attachment-list" wx:if="{{attachments.length > 0}}">
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:147:    <view class="attachment-item" wx:for="{{attachments}}" wx:key="attachment_id">
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:148:      <view class="attachment-info">
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:149:        <text class="file-name">{{item.file_name}}</text>
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:150:        <text class="file-size">{{item.file_size / 1024}} KB</text>
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:152:      <view class="attachment-actions">
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:153:        <button class="btn-small download" bindtap="onDownloadAttachment" data-attachment="{{item}}">下载</button>
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:154:        <button class="btn-small delete" wx:if="{{isOwner}}" bindtap="onDeleteAttachment" data-id="{{item.attachment_id}}">删除</button>
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:158:  <view class="empty-attachments" wx:if="{{attachments.length === 0}}">
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:161:  <button class="btn-upload" wx:if="{{isOwner}}" bindtap="onChooseFile" disabled="{{uploading}}">
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:164:  <view class="attachment-error" wx:if="{{attachmentError}}">
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:205:1. **验证范围：** 是否需要检查与其他页面的集成？（如student-application页面提交后跳转到detail页面）
docs/discussions/phase4c-next-steps/08-claude-phase2-implementation-review-request.md:307:const isOwner = userInfo.role === 'student' && detail.student_id === userInfo.user_id;
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:45:- 其他过滤参数（name, number, phone等）可选
docs/discussions/phase4c-next-steps/69-api-data-reading-test-review-request.md:125:6. 过滤参数测试（按学号、姓名等）
docs/discussions/phase4c-next-steps/52-claude-response-option-a-corrected.md:87:- 不重构为class-based views（保持行为不变）
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:16:如果产品明确要求“通知中心可回看宿舍阻断原因”，再采用 Option 2 的独立 `DormClearanceBlock` / `DormBlockRecord` 表。不要优先使用 blocked application，也不建议使用 `student_id` 伪装业务事件实体。
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:45:### 问题3：使用 `student_id` 作为通知实体会让幂等语义过粗 [P1]
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:50:当前唯一约束是 `(recipient, entity_type, entity_id, type)`。如果 `entity_type=student` 且 `entity_id=student_id`，同一个学生未来所有宿舍阻断都会折叠成同一条通知，无法表达不同阻断记录、不同原因或清退后再次阻断。
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:86:- student: FK(User)
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:102:recipient = student
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:111:更好的折中不是扩大幂等键，而是新增阻断记录实体。把 `student_id + dorm_status + blocking_reason + unresolved` 归并到一个 open block record，再由通知引用该 record。
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:119:- 断言 `Application.objects.filter(student=blocked_student).count() == 0`。
docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md:120:- 断言 `Notification.objects.filter(recipient=blocked_student).count() == 0`。
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:28:@permission_classes([IsAuthenticated])
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:37:@parser_classes([MultiPartParser, FormParser])
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:45:2. `@parser_classes([MultiPartParser, FormParser])` 装饰在 `upload_attachment()` 辅助函数上
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:71:@permission_classes([IsAuthenticated])
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:72:@parser_classes([MultiPartParser, FormParser])  # 移到这里
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:81:# 从这里移除 @parser_classes 装饰器
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:88:1. DRF只在 `@api_view` 装饰的函数上处理 `@parser_classes`
docs/discussions/phase4c-next-steps/16-claude-response-to-codex-p1-verification.md:141:- 将 `@parser_classes([MultiPartParser, FormParser])` 从 `upload_attachment()` 移到 `attachments_view()`
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:18:3. Add upload UI to the student application flow only after deciding the UX boundary.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:69:4. Add delete affordance only for the owning student where possible; still rely on backend RBAC.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:70:5. Add upload entry from `student-application` only if the product decision is clear:
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:107:- Student can choose and upload an allowed file after an application exists.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:108:- Student owner can delete.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:118:- Student cannot delete someone else's attachment.
docs/discussions/phase4c-next-steps/06-codex-next-steps-strategy-review.md:147:Claude's initial Option A recommendation is mostly right, but it is too broad in one place: uploading directly on the student application page assumes pre-existing `application_id` semantics that the backend does not provide.
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:50:  - XGUserAPIClient
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:101:- 班级 `class_id`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:109:2. **业务字段层：** 宽松采样，记录 `name/number/phone/identity_id/department/user_identity/user_auth_extra_field` 是否出现，不因业务字段缺失直接失败。
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:134:字段: name=yes number=yes phone=yes department=yes user_identity=yes
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:135:样本: name=张* number=17 phone=186****9896
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:158:- 不带姓名、手机号、学号过滤
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:203:- `XGUserAPIClient.build_headers()`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:204:- `XGUserAPIClient.build_form_data()`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:205:- `XGUserAPIClient.fetch_users_page()`
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:246:  XGUserAPIClient
docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md:251:  RealUserDataProvider
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:109:message = f"学生{application.student_name}（{application.student.user_id}）提交了离校申请，请及时审批。"
docs/discussions/phase4c-next-steps/39-claude-consensus-option-a-lite.md:155:- 调整契约允许`entity_type=student`或`entity_type=application_attempt`
docs/discussions/phase4c-next-steps/51-codex-option-e-lite-next-strategy-review.md:66:**Required adjustment:** use method-scoped decorators, for example stacked `@extend_schema(methods=['GET'], ...)` and `@extend_schema(methods=['POST'], ...)`, or refactor to class-based/generic views only if that remains tightly scoped. Keep behavior unchanged unless tests cover the refactor.
docs/discussions/phase4c-next-steps/22-claude-post-execution-next-steps.md:37:- 小程序骨架完成（login/student-application/approvals/detail）
docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md:46:- 映射到内部Student模型并入库
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:40:仓库已经有基础命令 `backend/apps/users/management/commands/import_csv.py`，支持students、counselors、mappings三类CSV导入。但它目前仍是开发辅助级别，不是可验收的数据导入工具：
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:85:- 统一CSV字段名：students、counselors、class mappings与 `docs/数据对接说明文档.md` 一致。
docs/discussions/phase4c-next-steps/20-codex-next-phase-strategy-response.md:88:- 增加强校验：必填字段、重复主键、班级映射引用辅导员存在、学生class_id有映射。
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:28:The attachment markup has classes for error, empty, list, item, actions, small buttons, and upload button. `detail.wxss` still has no corresponding attachment-specific styles. This matches the planned Step 6 and is not a backend or contract blocker.
docs/discussions/phase4c-next-steps/18-codex-p0-fix-verification-response.md:34:1. **P0 parser bug fix correctness:** Yes. `@parser_classes([MultiPartParser, FormParser])` is now on `attachments_view()`, which is the DRF `@api_view` entrypoint. Removing it from the plain helper `upload_attachment()` is correct.
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:76:<view wx:if="{{attachmentError}}" class="error-message">{{attachmentError}}</view>
docs/discussions/phase4c-next-steps/11-claude-p1-fixes-review-request.md:77:<view wx:elif="{{attachments.length === 0}}" class="empty-message">暂无附件</view>
docs/discussions/phase4c-next-steps/57-claude-response-accept-option-a-prime.md:38:- `user: AuthUserSerializer`（嵌套）
docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md:44:- 扩展通知实体类型，例如 `dorm_clearance` 或 `student`，并定义幂等键。
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:38:- 需要契约修正：允许`entity_type=student`或创建申请尝试记录
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:246:- 契约修正：允许`entity_type=student`，`entity_id=student.id`
docs/discussions/phase4c-next-steps/40-claude-post-phase2a-next-strategy.md:247:- 实现`notify_dorm_clearance_blocked(student, dorm_status)`
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:36:   当前只交付签名函数，`XGUserAPIClient` 仍是占位类，尚无配置读取/校验对象。若把 Step 1A 定义为“签名函数切片”，可以接受；若沿用 doc 77 验收标准，则还缺少 `XG_USER_API_URL`、`XG_USER_API_APP_KEY`、`XG_USER_API_APP_SECRET`、`XG_USER_API_TENANT_CODE` 的明确错误测试。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:117:字段覆盖: name=yes number=yes phone=yes department=yes user_identity=yes
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:118:样本: name=张* number=17**** phone=186****9896
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:127:- `XGUserAPIConfig` 或等价配置对象：从环境读取、校验必填项、归一化 encryptionType。
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:128:- `XGUserAPIClient.build_headers()`：
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:132:- `XGUserAPIClient.build_form_data()`：
docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md:135:- `XGUserAPIClient.fetch_users_page()`：
backend/apps/approvals/admin.py:6:class ApprovalAdmin(admin.ModelAdmin):
docs/discussions/phase4c-next-steps/87-step2b-implementation-review-request.md:43:**新增方法：** XGUserAPIClient.fetch_all_users()
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:33:  recipient: student
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:106:- 允许entity_type为dorm_clearance或student
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md:107:- 使用student_id作为entity_id（宿舍阻断通知）
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:70:<view class="attachment-error" wx:if="{{attachmentError}}">
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:73:<view class="empty-attachments" wx:elif="{{attachments.length === 0}}">
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:76:<view class="attachment-list" wx:else>
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:168:- `test_list_student_own_positive` ✅
docs/discussions/phase4c-next-steps/14-claude-p1-implementation-summary.md:169:- `test_list_student_other_negative` ✅
backend/apps/attachments/migrations/0001_initial.py:8:class Migration(migrations.Migration):
backend/apps/attachments/migrations/0001_initial.py:13:        ('applications', '0004_remove_unique_student_constraint'),
backend/apps/approvals/serializers.py:5:class ApprovalListSerializer(serializers.ModelSerializer):
backend/apps/approvals/serializers.py:10:    class Meta:
backend/apps/approvals/serializers.py:18:class ApprovalSerializer(serializers.ModelSerializer):
backend/apps/approvals/serializers.py:22:    class Meta:
backend/apps/approvals/serializers.py:30:class ApprovalActionSerializer(serializers.Serializer):
backend/apps/approvals/serializers.py:34:class ApprovalListResponseSerializer(serializers.Serializer):
backend/apps/approvals/models.py:2:from apps.users.models import User
backend/apps/approvals/models.py:6:class ApprovalStep(models.TextChoices):
backend/apps/approvals/models.py:11:class ApprovalDecision(models.TextChoices):
backend/apps/approvals/models.py:17:class Approval(models.Model):
backend/apps/approvals/models.py:21:    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approvals')
backend/apps/approvals/models.py:29:    class Meta:
backend/apps/attachments/tests/test_list.py:5:from apps.users.models import User, UserRole
backend/apps/attachments/tests/test_list.py:6:from apps.users.class_mapping import ClassMapping
backend/apps/attachments/tests/test_list.py:12:class AttachmentListTestCase(TestCase):
backend/apps/attachments/tests/test_list.py:16:        # Create students
backend/apps/attachments/tests/test_list.py:17:        self.student = User.objects.create_user(
backend/apps/attachments/tests/test_list.py:21:            role=UserRole.STUDENT,
backend/apps/attachments/tests/test_list.py:22:            class_id='CS2020-01',
backend/apps/attachments/tests/test_list.py:27:        self.other_student = User.objects.create_user(
backend/apps/attachments/tests/test_list.py:31:            role=UserRole.STUDENT,
backend/apps/attachments/tests/test_list.py:32:            class_id='CS2020-02',
backend/apps/attachments/tests/test_list.py:38:        self.counselor = User.objects.create_user(
backend/apps/attachments/tests/test_list.py:42:            role=UserRole.COUNSELOR
backend/apps/attachments/tests/test_list.py:45:        self.other_counselor = User.objects.create_user(
backend/apps/attachments/tests/test_list.py:49:            role=UserRole.COUNSELOR
backend/apps/attachments/tests/test_list.py:53:        self.dean = User.objects.create_user(
backend/apps/attachments/tests/test_list.py:57:            role=UserRole.DEAN
backend/apps/attachments/tests/test_list.py:60:        # Create class mappings
backend/apps/attachments/tests/test_list.py:62:            class_id='CS2020-01',
backend/apps/attachments/tests/test_list.py:69:            class_id='CS2020-02',
backend/apps/attachments/tests/test_list.py:75:        # Create application for student
backend/apps/attachments/tests/test_list.py:78:            student=self.student,
backend/apps/attachments/tests/test_list.py:79:            student_name='张三',
backend/apps/attachments/tests/test_list.py:80:            class_id='CS2020-01',
backend/apps/attachments/tests/test_list.py:90:            uploaded_by=self.student,
backend/apps/attachments/tests/test_list.py:108:    def test_list_student_own_positive(self):
backend/apps/attachments/tests/test_list.py:109:        """Student can list own application attachments"""
backend/apps/attachments/tests/test_list.py:110:        self.client.force_authenticate(user=self.student)
backend/apps/attachments/tests/test_list.py:120:    def test_list_student_other_negative(self):
backend/apps/attachments/tests/test_list.py:121:        """Student cannot list another student's attachments"""
backend/apps/attachments/tests/test_list.py:122:        self.client.force_authenticate(user=self.other_student)
backend/apps/attachments/tests/test_list.py:170:        self.client.force_authenticate(user=self.student)
backend/apps/attachments/tests/test_delete.py:5:from apps.users.models import User, UserRole
backend/apps/attachments/tests/test_delete.py:6:from apps.users.class_mapping import ClassMapping
backend/apps/attachments/tests/test_delete.py:11:class AttachmentDeleteTestCase(TestCase):
backend/apps/attachments/tests/test_delete.py:15:        # Create students
backend/apps/attachments/tests/test_delete.py:16:        self.student = User.objects.create_user(
backend/apps/attachments/tests/test_delete.py:20:            role=UserRole.STUDENT,
backend/apps/attachments/tests/test_delete.py:21:            class_id='CS2020-01',
backend/apps/attachments/tests/test_delete.py:26:        self.other_student = User.objects.create_user(
backend/apps/attachments/tests/test_delete.py:30:            role=UserRole.STUDENT,
backend/apps/attachments/tests/test_delete.py:31:            class_id='CS2020-02',
backend/apps/attachments/tests/test_delete.py:37:        self.counselor = User.objects.create_user(
backend/apps/attachments/tests/test_delete.py:41:            role=UserRole.COUNSELOR
backend/apps/attachments/tests/test_delete.py:44:        # Create class mapping
backend/apps/attachments/tests/test_delete.py:46:            class_id='CS2020-01',
backend/apps/attachments/tests/test_delete.py:55:            student=self.student,
backend/apps/attachments/tests/test_delete.py:56:            student_name='张三',
backend/apps/attachments/tests/test_delete.py:57:            class_id='CS2020-01',
backend/apps/attachments/tests/test_delete.py:68:            uploaded_by=self.student,
backend/apps/attachments/tests/test_delete.py:77:        """Owner student can soft-delete attachment"""
backend/apps/attachments/tests/test_delete.py:78:        self.client.force_authenticate(user=self.student)
backend/apps/attachments/tests/test_delete.py:91:    def test_delete_non_owner_student_forbidden(self):
backend/apps/attachments/tests/test_delete.py:92:        """Non-owner student cannot delete attachment"""
backend/apps/attachments/tests/test_delete.py:93:        self.client.force_authenticate(user=self.other_student)
backend/apps/attachments/tests/test_delete.py:122:        self.client.force_authenticate(user=self.student)
backend/apps/attachments/tests/test_upload.py:5:from apps.users.models import User, UserRole
backend/apps/attachments/tests/test_upload.py:6:from apps.users.class_mapping import ClassMapping
backend/apps/attachments/tests/test_upload.py:11:class AttachmentUploadTestCase(TestCase):
backend/apps/attachments/tests/test_upload.py:15:        # Create student
backend/apps/attachments/tests/test_upload.py:16:        self.student = User.objects.create_user(
backend/apps/attachments/tests/test_upload.py:20:            role=UserRole.STUDENT,
backend/apps/attachments/tests/test_upload.py:21:            class_id='CS2020-01',
backend/apps/attachments/tests/test_upload.py:26:        # Create another student
backend/apps/attachments/tests/test_upload.py:27:        self.other_student = User.objects.create_user(
backend/apps/attachments/tests/test_upload.py:31:            role=UserRole.STUDENT,
backend/apps/attachments/tests/test_upload.py:32:            class_id='CS2020-01',
backend/apps/attachments/tests/test_upload.py:38:        self.counselor = User.objects.create_user(
backend/apps/attachments/tests/test_upload.py:42:            role=UserRole.COUNSELOR
backend/apps/attachments/tests/test_upload.py:45:        # Create class mapping
backend/apps/attachments/tests/test_upload.py:47:            class_id='CS2020-01',
backend/apps/attachments/tests/test_upload.py:53:        # Create application for student
backend/apps/attachments/tests/test_upload.py:56:            student=self.student,
backend/apps/attachments/tests/test_upload.py:57:            student_name='张三',
backend/apps/attachments/tests/test_upload.py:58:            class_id='CS2020-01',
backend/apps/attachments/tests/test_upload.py:64:        # Create application for other student
backend/apps/attachments/tests/test_upload.py:67:            student=self.other_student,
backend/apps/attachments/tests/test_upload.py:68:            student_name='李四',
backend/apps/attachments/tests/test_upload.py:69:            class_id='CS2020-01',
backend/apps/attachments/tests/test_upload.py:76:        """Student can upload attachment to own application"""
backend/apps/attachments/tests/test_upload.py:77:        self.client.force_authenticate(user=self.student)
backend/apps/attachments/tests/test_upload.py:97:    def test_upload_forbidden_other_student(self):
backend/apps/attachments/tests/test_upload.py:98:        """Student cannot upload to another student's application"""
backend/apps/attachments/tests/test_upload.py:99:        self.client.force_authenticate(user=self.student)
backend/apps/attachments/tests/test_upload.py:133:        self.client.force_authenticate(user=self.student)
backend/apps/attachments/tests/test_upload.py:150:        self.client.force_authenticate(user=self.student)
backend/apps/attachments/tests/test_download.py:5:from apps.users.models import User, UserRole
backend/apps/attachments/tests/test_download.py:6:from apps.users.class_mapping import ClassMapping
backend/apps/attachments/tests/test_download.py:12:class AttachmentDownloadTestCase(TestCase):
backend/apps/attachments/tests/test_download.py:16:        # Create students
backend/apps/attachments/tests/test_download.py:17:        self.student = User.objects.create_user(
backend/apps/attachments/tests/test_download.py:21:            role=UserRole.STUDENT,
backend/apps/attachments/tests/test_download.py:22:            class_id='CS2020-01',
backend/apps/attachments/tests/test_download.py:27:        self.other_student = User.objects.create_user(
backend/apps/attachments/tests/test_download.py:31:            role=UserRole.STUDENT,
backend/apps/attachments/tests/test_download.py:32:            class_id='CS2020-02',
backend/apps/attachments/tests/test_download.py:38:        self.counselor = User.objects.create_user(
backend/apps/attachments/tests/test_download.py:42:            role=UserRole.COUNSELOR
backend/apps/attachments/tests/test_download.py:45:        # Create class mapping
backend/apps/attachments/tests/test_download.py:47:            class_id='CS2020-01',
backend/apps/attachments/tests/test_download.py:56:            student=self.student,
backend/apps/attachments/tests/test_download.py:57:            student_name='张三',
backend/apps/attachments/tests/test_download.py:58:            class_id='CS2020-01',
backend/apps/attachments/tests/test_download.py:69:            uploaded_by=self.student,
backend/apps/attachments/tests/test_download.py:77:    def test_download_positive_student(self):
backend/apps/attachments/tests/test_download.py:78:        """Student can download own application attachment"""
backend/apps/attachments/tests/test_download.py:79:        self.client.force_authenticate(user=self.student)
backend/apps/attachments/tests/test_download.py:99:        """Unauthorized student cannot download attachment"""
backend/apps/attachments/tests/test_download.py:100:        self.client.force_authenticate(user=self.other_student)
backend/apps/attachments/tests/test_download.py:114:        self.client.force_authenticate(user=self.student)
backend/apps/attachments/views.py:2:from rest_framework.decorators import api_view, permission_classes, parser_classes
backend/apps/attachments/views.py:10:from apps.users.models import UserRole
backend/apps/attachments/views.py:47:@permission_classes([IsAuthenticated])
backend/apps/attachments/views.py:48:@parser_classes([MultiPartParser, FormParser])
backend/apps/attachments/views.py:67:    # Permission: only student who owns the application
backend/apps/attachments/views.py:68:    if user.role != UserRole.STUDENT or application.student_id != user.user_id:
backend/apps/attachments/views.py:128:@permission_classes([IsAuthenticated])
backend/apps/attachments/views.py:171:@permission_classes([IsAuthenticated])
backend/apps/attachments/views.py:187:    # Permission: only student who owns the application
backend/apps/attachments/views.py:188:    if user.role != UserRole.STUDENT or attachment.application.student_id != user.user_id:
backend/apps/attachments/serializers.py:5:class AttachmentUploadSerializer(serializers.Serializer):
backend/apps/attachments/serializers.py:23:class AttachmentSerializer(serializers.ModelSerializer):
backend/apps/attachments/serializers.py:24:    class Meta:
backend/apps/attachments/serializers.py:30:class AttachmentListResponseSerializer(serializers.Serializer):
backend/apps/attachments/models.py:3:from apps.users.models import User
backend/apps/attachments/models.py:6:class AttachmentType(models.TextChoices):
backend/apps/attachments/models.py:13:class Attachment(models.Model):
backend/apps/attachments/models.py:16:    uploaded_by = models.ForeignKey(User, on_delete=models.PROTECT)
backend/apps/attachments/models.py:26:    class Meta:
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:91:### P2：Phase 2B不是简单契约修正，`entity_type=student`会引入新语义债务
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:95:宿舍阻断发生在`Application.objects.create()`之前，这一点判断正确。但直接允许`entity_type=student`并不只是简单改枚举：
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:100:- 如果未来要审计“申请尝试”，`student`实体无法表达每次尝试的上下文。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:104:本轮不要实现Phase 2B。若未来确实需要，应优先设计`application_attempt`或显式`dedupe_key`/`occurred_at`语义，而不是直接复用`student`作为实体。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:146:宿舍阻断通知确实能增加一点用户体验，但同步422已经给了学生明确反馈。为这点价值引入`student`实体通知、迁移、幂等语义和契约版本变更，投入产出比不高。
docs/discussions/phase4c-next-steps/41-codex-post-phase2a-next-strategy-response.md:150:> Phase 2B只有在需要审计阻断历史或产品明确要求站内留痕时才启动；届时优先设计`application_attempt`，不要只把`entity_type=student`作为快捷方案。
backend/apps/approvals/tests/test_rejection_flow.py:6:from apps.users.models import User, UserRole
backend/apps/approvals/tests/test_rejection_flow.py:7:from apps.users.class_mapping import ClassMapping
backend/apps/approvals/tests/test_rejection_flow.py:12:class RejectionFlowTestCase(TestCase):
backend/apps/approvals/tests/test_rejection_flow.py:16:        self.student = User.objects.create_user(
backend/apps/approvals/tests/test_rejection_flow.py:20:            role=UserRole.STUDENT,
backend/apps/approvals/tests/test_rejection_flow.py:21:            class_id='CS2020-01',
backend/apps/approvals/tests/test_rejection_flow.py:26:        self.counselor = User.objects.create_user(
backend/apps/approvals/tests/test_rejection_flow.py:30:            role=UserRole.COUNSELOR
backend/apps/approvals/tests/test_rejection_flow.py:33:        self.dean = User.objects.create_user(
backend/apps/approvals/tests/test_rejection_flow.py:37:            role=UserRole.DEAN
backend/apps/approvals/tests/test_rejection_flow.py:40:        # Create class mapping
backend/apps/approvals/tests/test_rejection_flow.py:42:            class_id='CS2020-01',
backend/apps/approvals/tests/test_rejection_flow.py:50:        # Student login and submit
backend/apps/approvals/tests/test_rejection_flow.py:55:        student_token = response.data['access_token']
backend/apps/approvals/tests/test_rejection_flow.py:57:        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
backend/apps/approvals/tests/test_rejection_flow.py:87:        # Student login and submit
backend/apps/approvals/tests/test_rejection_flow.py:92:        student_token = response.data['access_token']
backend/apps/approvals/tests/test_rejection_flow.py:94:        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
backend/apps/approvals/tests/test_list_permissions.py:3:from apps.users.models import User, UserRole
backend/apps/approvals/tests/test_list_permissions.py:8:class ApprovalListPermissionTest(TestCase):
backend/apps/approvals/tests/test_list_permissions.py:13:        self.student = User.objects.create(user_id='S001', name='学生', role=UserRole.STUDENT, class_id='CS2020-01')
backend/apps/approvals/tests/test_list_permissions.py:14:        self.student.set_password('S001')
backend/apps/approvals/tests/test_list_permissions.py:15:        self.student.save()
backend/apps/approvals/tests/test_list_permissions.py:17:        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
backend/apps/approvals/tests/test_list_permissions.py:21:        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
backend/apps/approvals/tests/test_list_permissions.py:25:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
backend/apps/approvals/tests/test_list_permissions.py:29:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
backend/apps/approvals/tests/test_list_permissions.py:36:            student=self.student,
backend/apps/approvals/tests/test_list_permissions.py:37:            student_name='学生',
backend/apps/approvals/tests/test_list_permissions.py:38:            class_id='CS2020-01',
backend/apps/approvals/tests/test_list_permissions.py:63:    def test_student_403_on_approval_list(self):
backend/apps/approvals/tests/test_list_permissions.py:64:        self.client.force_authenticate(user=self.student)
backend/apps/approvals/tests/test_list_permissions.py:105:            student=self.student,
backend/apps/approvals/tests/test_list_permissions.py:106:            student_name='学生',
backend/apps/approvals/tests/test_list_permissions.py:107:            class_id='CS2020-01',
backend/apps/approvals/tests/test_list_permissions.py:124:            student=self.student,
backend/apps/approvals/tests/test_list_permissions.py:125:            student_name='学生',
backend/apps/approvals/tests/test_list_permissions.py:126:            class_id='CS2020-01',
backend/apps/applications/admin.py:6:class ApplicationAdmin(admin.ModelAdmin):
backend/apps/applications/admin.py:7:    list_display = ['application_id', 'student', 'student_name', 'class_id', 'status', 'created_at']
backend/apps/applications/admin.py:9:    search_fields = ['application_id', 'student__user_id', 'student_name', 'class_id']
backend/apps/approvals/tests/test_permissions.py:4:from apps.users.models import User, UserRole
backend/apps/approvals/tests/test_permissions.py:7:from apps.users.class_mapping import ClassMapping
backend/apps/approvals/tests/test_permissions.py:11:class ApprovalPermissionsTestCase(TestCase):
backend/apps/approvals/tests/test_permissions.py:13:        # Create students
backend/apps/approvals/tests/test_permissions.py:14:        self.student1 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:17:            role=UserRole.STUDENT,
backend/apps/approvals/tests/test_permissions.py:18:            class_id='CS2020-01',
backend/apps/approvals/tests/test_permissions.py:21:        self.student2 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:24:            role=UserRole.STUDENT,
backend/apps/approvals/tests/test_permissions.py:25:            class_id='CS2020-02',
backend/apps/approvals/tests/test_permissions.py:30:        self.counselor1 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:33:            role=UserRole.COUNSELOR,
backend/apps/approvals/tests/test_permissions.py:36:        self.counselor2 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:39:            role=UserRole.COUNSELOR,
backend/apps/approvals/tests/test_permissions.py:42:        self.dean1 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:45:            role=UserRole.DEAN,
backend/apps/approvals/tests/test_permissions.py:48:        self.dean2 = User.objects.create_user(
backend/apps/approvals/tests/test_permissions.py:51:            role=UserRole.DEAN,
backend/apps/approvals/tests/test_permissions.py:55:        # Create class mappings
backend/apps/approvals/tests/test_permissions.py:57:            class_id='CS2020-01',
backend/apps/approvals/tests/test_permissions.py:63:            class_id='CS2020-02',
backend/apps/approvals/tests/test_permissions.py:69:        # Create application for student1
backend/apps/approvals/tests/test_permissions.py:72:            student=self.student1,
backend/apps/approvals/tests/test_permissions.py:73:            student_name='张三',
backend/apps/approvals/tests/test_permissions.py:74:            class_id='CS2020-01',
backend/apps/approvals/tests/test_permissions.py:104:    def test_student_cannot_approve_or_reject(self):
backend/apps/approvals/tests/test_permissions.py:106:        self.client.force_authenticate(user=self.student1)
backend/apps/approvals/tests/test_state_machine.py:4:from apps.users.models import User, UserRole
backend/apps/approvals/tests/test_state_machine.py:7:from apps.users.class_mapping import ClassMapping
backend/apps/approvals/tests/test_state_machine.py:10:class ApprovalStateMachineTestCase(TestCase):
backend/apps/approvals/tests/test_state_machine.py:12:        # Create student
backend/apps/approvals/tests/test_state_machine.py:13:        self.student = User.objects.create_user(
backend/apps/approvals/tests/test_state_machine.py:16:            role=UserRole.STUDENT,
backend/apps/approvals/tests/test_state_machine.py:17:            class_id='CS2020-01',
backend/apps/approvals/tests/test_state_machine.py:22:        self.counselor = User.objects.create_user(
backend/apps/approvals/tests/test_state_machine.py:25:            role=UserRole.COUNSELOR,
backend/apps/approvals/tests/test_state_machine.py:30:        self.dean = User.objects.create_user(
backend/apps/approvals/tests/test_state_machine.py:33:            role=UserRole.DEAN,
backend/apps/approvals/tests/test_state_machine.py:37:        # Create class mapping
backend/apps/approvals/tests/test_state_machine.py:39:            class_id='CS2020-01',
backend/apps/approvals/tests/test_state_machine.py:48:            student=self.student,
backend/apps/approvals/tests/test_state_machine.py:49:            student_name='张三',
backend/apps/approvals/tests/test_state_machine.py:50:            class_id='CS2020-01',
backend/apps/applications/providers.py:1:from dataclasses import dataclass
backend/apps/applications/providers.py:6:@dataclass
backend/apps/applications/providers.py:7:class DormCheckoutStatusDTO:
backend/apps/applications/providers.py:8:    student_id: str
backend/apps/applications/providers.py:15:class MockDormCheckoutProvider:
backend/apps/applications/providers.py:16:    def check_status(self, student_id: str) -> DormCheckoutStatusDTO:
backend/apps/applications/providers.py:19:                student_id="2020001",
backend/apps/applications/providers.py:26:                student_id="2020002",
backend/apps/applications/providers.py:33:                student_id="2020003",
backend/apps/applications/providers.py:40:                student_id="2020006",
backend/apps/applications/providers.py:47:                student_id="2020099",
backend/apps/applications/providers.py:55:        return mock_data.get(student_id, DormCheckoutStatusDTO(
backend/apps/applications/providers.py:56:            student_id=student_id,
backend/apps/approvals/views.py:2:from rest_framework.decorators import api_view, permission_classes
backend/apps/approvals/views.py:14:from apps.users.models import UserRole
backend/apps/approvals/views.py:36:@permission_classes([IsAuthenticated])
backend/apps/approvals/views.py:41:    if user.role == UserRole.STUDENT:
backend/apps/approvals/views.py:48:    if user.role == UserRole.COUNSELOR:
backend/apps/approvals/views.py:55:    elif user.role == UserRole.DEAN:
backend/apps/approvals/views.py:100:@permission_classes([IsAuthenticated])
backend/apps/approvals/views.py:110:    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
backend/apps/approvals/views.py:113:    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
backend/apps/approvals/views.py:185:@permission_classes([IsAuthenticated])
backend/apps/approvals/views.py:195:    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
backend/apps/approvals/views.py:198:    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
backend/apps/applications/pagination.py:5:class ApplicationLimitOffsetPagination(LimitOffsetPagination):
backend/apps/applications/views.py:2:from rest_framework.decorators import api_view, permission_classes
backend/apps/applications/views.py:14:from apps.users.models import UserRole
backend/apps/applications/views.py:15:from apps.users.class_mapping import ClassMapping
backend/apps/applications/views.py:54:@permission_classes([IsAuthenticated])
backend/apps/applications/views.py:65:    # Student: own applications only
backend/apps/applications/views.py:66:    if user.role == UserRole.STUDENT:
backend/apps/applications/views.py:67:        queryset = Application.objects.filter(student=user)
backend/apps/applications/views.py:70:    elif user.role == UserRole.COUNSELOR:
backend/apps/applications/views.py:79:    elif user.role == UserRole.DEAN:
backend/apps/applications/views.py:114:    if user.role != UserRole.STUDENT:
backend/apps/applications/views.py:120:        student=user,
backend/apps/applications/views.py:125:                                    'details': {'student_id': user.user_id, 'existing_application_id': existing.application_id, 'status': existing.status}}},
backend/apps/applications/views.py:139:                                    'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
backend/apps/applications/views.py:144:        class_mapping = ClassMapping.objects.get(class_id=user.class_id, active=True)
backend/apps/applications/views.py:147:                                    'details': {'class_id': user.class_id}}},
backend/apps/applications/views.py:152:        student=user,
backend/apps/applications/views.py:153:        student_name=user.name,
backend/apps/applications/views.py:154:        class_id=user.class_id,
backend/apps/applications/views.py:165:        approver=class_mapping.counselor,
backend/apps/applications/views.py:166:        approver_name=class_mapping.counselor_name,
backend/apps/applications/views.py:187:@permission_classes([IsAuthenticated])
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:31:**Codex正确。** `backend/apps/users/management/commands/import_csv.py`已存在，支持students/counselors/mappings导入。但当前实现缺少：
docs/discussions/phase4c-next-steps/21-claude-consensus-narrowed-strategy.md:74:- 增加强校验：必填字段、重复主键、班级映射引用辅导员存在、学生class_id有映射
docs/discussions/phase4c-next-steps/13-claude-response-to-codex-p1-review.md:88:class ApiClient {
backend/apps/approvals/pagination.py:5:class ApprovalLimitOffsetPagination(LimitOffsetPagination):
docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md:178:- 本系统User model需要的字段清单
backend/apps/applications/migrations/0003_application_unique_student_application.py:6:class Migration(migrations.Migration):
backend/apps/applications/migrations/0003_application_unique_student_application.py:15:            constraint=models.UniqueConstraint(fields=('student',), name='unique_student_application'),
backend/apps/users/class_mapping.py:2:from apps.users.models import User
backend/apps/users/class_mapping.py:5:class ClassMapping(models.Model):
backend/apps/users/class_mapping.py:6:    class_id = models.CharField(max_length=50, primary_key=True)
backend/apps/users/class_mapping.py:7:    counselor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='managed_classes')
backend/apps/users/class_mapping.py:13:    class Meta:
backend/apps/users/class_mapping.py:14:        db_table = 'class_mappings'
backend/apps/applications/migrations/0002_initial.py:8:class Migration(migrations.Migration):
backend/apps/applications/migrations/0002_initial.py:20:            name='student',
backend/apps/users/models.py:1:from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
backend/apps/users/models.py:5:class UserRole(models.TextChoices):
backend/apps/users/models.py:6:    STUDENT = 'student', '学生'
backend/apps/users/models.py:11:class UserManager(BaseUserManager):
backend/apps/users/models.py:27:class User(AbstractBaseUser, PermissionsMixin):
backend/apps/users/models.py:30:    role = models.CharField(max_length=20, choices=UserRole.choices)
backend/apps/users/models.py:32:    class_id = models.CharField(max_length=50, null=True, blank=True)
backend/apps/users/models.py:40:    objects = UserManager()
backend/apps/users/models.py:45:    class Meta:
backend/apps/applications/migrations/0001_initial.py:6:class Migration(migrations.Migration):
backend/apps/applications/migrations/0001_initial.py:18:                ('student_name', models.CharField(max_length=100)),
backend/apps/applications/migrations/0001_initial.py:19:                ('class_id', models.CharField(max_length=50)),
backend/apps/applications/migrations/0004_remove_unique_student_constraint.py:6:class Migration(migrations.Migration):
backend/apps/applications/migrations/0004_remove_unique_student_constraint.py:9:        ('applications', '0003_application_unique_student_application'),
backend/apps/applications/migrations/0004_remove_unique_student_constraint.py:15:            name='unique_student_application',
backend/apps/approvals/migrations/0002_initial.py:8:class Migration(migrations.Migration):
backend/apps/approvals/migrations/0001_initial.py:7:class Migration(migrations.Migration):
backend/apps/applications/tests/test_p0_fixes.py:5:from apps.users.models import UserRole
backend/apps/applications/tests/test_p0_fixes.py:6:from apps.users.class_mapping import ClassMapping
backend/apps/applications/tests/test_p0_fixes.py:8:User = get_user_model()
backend/apps/applications/tests/test_p0_fixes.py:11:class ResubmissionAfterRejectionTest(TestCase):
backend/apps/applications/tests/test_p0_fixes.py:13:        self.student = User.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:15:            name='Test Student',
backend/apps/applications/tests/test_p0_fixes.py:16:            role=UserRole.STUDENT,
backend/apps/applications/tests/test_p0_fixes.py:17:            class_id='CS2020-01'
backend/apps/applications/tests/test_p0_fixes.py:19:        self.counselor = User.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:22:            role=UserRole.COUNSELOR
backend/apps/applications/tests/test_p0_fixes.py:25:            class_id='CS2020-01',
backend/apps/applications/tests/test_p0_fixes.py:34:            student=self.student,
backend/apps/applications/tests/test_p0_fixes.py:35:            student_name=self.student.name,
backend/apps/applications/tests/test_p0_fixes.py:36:            class_id=self.student.class_id,
backend/apps/applications/tests/test_p0_fixes.py:45:            student=self.student,
backend/apps/applications/tests/test_p0_fixes.py:46:            student_name=self.student.name,
backend/apps/applications/tests/test_p0_fixes.py:47:            class_id=self.student.class_id,
backend/apps/applications/tests/test_p0_fixes.py:53:        self.assertEqual(Application.objects.filter(student=self.student).count(), 2)
backend/apps/applications/tests/test_p0_fixes.py:60:            student=self.student,
backend/apps/applications/tests/test_p0_fixes.py:61:            student_name=self.student.name,
backend/apps/applications/tests/test_p0_fixes.py:62:            class_id=self.student.class_id,
backend/apps/applications/tests/test_p0_fixes.py:71:            student=self.student,
backend/apps/applications/tests/test_p0_fixes.py:72:            student_name=self.student.name,
backend/apps/applications/tests/test_p0_fixes.py:73:            class_id=self.student.class_id,
backend/apps/applications/tests/test_p0_fixes.py:84:class ApprovalDecisionFilterTest(TestCase):
backend/apps/applications/tests/test_p0_fixes.py:86:        self.student = User.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:88:            name='Test Student',
backend/apps/applications/tests/test_p0_fixes.py:89:            role=UserRole.STUDENT,
backend/apps/applications/tests/test_p0_fixes.py:90:            class_id='CS2020-01'
backend/apps/applications/tests/test_p0_fixes.py:92:        self.counselor = User.objects.create(
backend/apps/applications/tests/test_p0_fixes.py:95:            role=UserRole.COUNSELOR
backend/apps/applications/tests/test_p0_fixes.py:101:            student=self.student,
backend/apps/applications/tests/test_p0_fixes.py:102:            student_name=self.student.name,
backend/apps/applications/tests/test_p0_fixes.py:103:            class_id=self.student.class_id,
backend/apps/applications/tests/test_p0_fixes.py:111:            student=self.student,
backend/apps/applications/tests/test_p0_fixes.py:112:            student_name=self.student.name,
backend/apps/applications/tests/test_p0_fixes.py:113:            class_id=self.student.class_id,
backend/apps/applications/tests/test_p0_fixes.py:121:            student=self.student,
backend/apps/applications/tests/test_p0_fixes.py:122:            student_name=self.student.name,
backend/apps/applications/tests/test_p0_fixes.py:123:            class_id=self.student.class_id,
backend/apps/users/views.py:2:from rest_framework.decorators import api_view, permission_classes
backend/apps/users/views.py:26:@permission_classes([AllowAny])
backend/apps/applications/tests/test_error_cases.py:6:from apps.users.models import User, UserRole
backend/apps/applications/tests/test_error_cases.py:7:from apps.users.class_mapping import ClassMapping
backend/apps/applications/tests/test_error_cases.py:11:class ErrorCasesTestCase(TestCase):
backend/apps/applications/tests/test_error_cases.py:16:        self.student1 = User.objects.create_user(
backend/apps/applications/tests/test_error_cases.py:20:            role=UserRole.STUDENT,
backend/apps/applications/tests/test_error_cases.py:21:            class_id='CS2020-01',
backend/apps/applications/tests/test_error_cases.py:26:        self.student2 = User.objects.create_user(
backend/apps/applications/tests/test_error_cases.py:30:            role=UserRole.STUDENT,
backend/apps/applications/tests/test_error_cases.py:31:            class_id='CS2020-01',
backend/apps/applications/tests/test_error_cases.py:36:        self.student3 = User.objects.create_user(
backend/apps/applications/tests/test_error_cases.py:40:            role=UserRole.STUDENT,
backend/apps/applications/tests/test_error_cases.py:41:            class_id='CS2020-01',
backend/apps/applications/tests/test_error_cases.py:46:        self.counselor = User.objects.create_user(
backend/apps/applications/tests/test_error_cases.py:50:            role=UserRole.COUNSELOR
backend/apps/applications/tests/test_error_cases.py:53:        # Create class mapping
backend/apps/applications/tests/test_error_cases.py:55:            class_id='CS2020-01',
backend/apps/applications/tests/test_error_cases.py:102:    def test_forbidden_access_other_student_application(self):
backend/apps/applications/tests/test_error_cases.py:104:        # Student1 creates application
backend/apps/applications/tests/test_error_cases.py:118:        # Student2 tries to access Student1's application
backend/apps/users/serializers.py:3:from .models import User
backend/apps/users/serializers.py:6:class UserSerializer(serializers.ModelSerializer):
backend/apps/users/serializers.py:7:    class Meta:
backend/apps/users/serializers.py:8:        model = User
backend/apps/users/serializers.py:9:        fields = ['user_id', 'name', 'role', 'class_id', 'active', 'is_graduating', 'graduation_year']
backend/apps/users/serializers.py:13:class AuthUserSerializer(serializers.ModelSerializer):
backend/apps/users/serializers.py:14:    """登录响应中的用户摘要（UserDTO子集）"""
backend/apps/users/serializers.py:15:    class Meta:
backend/apps/users/serializers.py:16:        model = User
backend/apps/users/serializers.py:17:        fields = ['user_id', 'name', 'role', 'class_id']
backend/apps/users/serializers.py:20:class LoginSerializer(serializers.Serializer):
backend/apps/users/serializers.py:29:            user = User.objects.get(user_id=user_id)
backend/apps/users/serializers.py:30:        except User.DoesNotExist:
backend/apps/users/serializers.py:44:            'user': AuthUserSerializer(user).data
backend/apps/users/serializers.py:48:class LoginResponseSerializer(serializers.Serializer):
backend/apps/users/serializers.py:52:    user = AuthUserSerializer(help_text="用户信息")
backend/apps/users/integrations/__init__.py:2:from .xg_user_client import generate_sign, XGUserAPIClient
backend/apps/users/integrations/__init__.py:4:__all__ = ['generate_sign', 'XGUserAPIClient']
backend/apps/applications/permissions.py:1:from apps.users.models import UserRole
backend/apps/applications/permissions.py:2:from apps.users.class_mapping import ClassMapping
backend/apps/applications/permissions.py:8:    if user.role == UserRole.STUDENT:
backend/apps/applications/permissions.py:9:        return application.student_id == user.user_id
backend/apps/applications/permissions.py:11:    if user.role == UserRole.COUNSELOR:
backend/apps/applications/permissions.py:14:            class_id=application.class_id,
backend/apps/applications/permissions.py:18:    if user.role == UserRole.DEAN:
backend/apps/applications/tests/test_detail_permissions.py:3:from apps.users.models import User, UserRole
backend/apps/applications/tests/test_detail_permissions.py:4:from apps.users.class_mapping import ClassMapping
backend/apps/applications/tests/test_detail_permissions.py:10:class ApplicationDetailPermissionTest(TestCase):
backend/apps/applications/tests/test_detail_permissions.py:14:        # Students (use IDs that mock provider recognizes as COMPLETED)
backend/apps/applications/tests/test_detail_permissions.py:15:        self.student1 = User.objects.create(user_id='2020001', name='学生1', role=UserRole.STUDENT, class_id='CS2020-01')
backend/apps/applications/tests/test_detail_permissions.py:16:        self.student1.set_password('2020001')
backend/apps/applications/tests/test_detail_permissions.py:17:        self.student1.save()
backend/apps/applications/tests/test_detail_permissions.py:19:        self.student2 = User.objects.create(user_id='2020002', name='学生2', role=UserRole.STUDENT, class_id='CS2020-02')
backend/apps/applications/tests/test_detail_permissions.py:20:        self.student2.set_password('2020002')
backend/apps/applications/tests/test_detail_permissions.py:21:        self.student2.save()
backend/apps/applications/tests/test_detail_permissions.py:24:        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
backend/apps/applications/tests/test_detail_permissions.py:28:        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
backend/apps/applications/tests/test_detail_permissions.py:33:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
backend/apps/applications/tests/test_detail_permissions.py:37:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
backend/apps/applications/tests/test_detail_permissions.py:42:        ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
backend/apps/applications/tests/test_detail_permissions.py:43:        ClassMapping.objects.create(class_id='CS2020-02', counselor=self.counselor2, counselor_name='辅导员2', active=True)
backend/apps/applications/tests/test_detail_permissions.py:45:    def test_student_cannot_access_other_student_application(self):
backend/apps/applications/tests/test_detail_permissions.py:46:        # Student1 creates application
backend/apps/applications/tests/test_detail_permissions.py:47:        self.client.force_authenticate(user=self.student1)
backend/apps/applications/tests/test_detail_permissions.py:55:        # Student2 tries to access Student1's application
backend/apps/applications/tests/test_detail_permissions.py:56:        self.client.force_authenticate(user=self.student2)
backend/apps/applications/tests/test_detail_permissions.py:61:    def test_counselor_cannot_access_cross_class_application(self):
backend/apps/applications/tests/test_detail_permissions.py:62:        # Student from CS2020-01 creates application
backend/apps/applications/tests/test_detail_permissions.py:63:        self.client.force_authenticate(user=self.student1)
backend/apps/applications/tests/test_detail_permissions.py:78:        # Student creates application
backend/apps/applications/tests/test_detail_permissions.py:79:        self.client.force_authenticate(user=self.student1)
backend/apps/applications/serializers.py:5:class ApplicationListSerializer(serializers.ModelSerializer):
backend/apps/applications/serializers.py:7:    student_id = serializers.CharField(source='student.user_id', read_only=True)
backend/apps/applications/serializers.py:9:    class Meta:
backend/apps/applications/serializers.py:11:        fields = ['application_id', 'student_id', 'student_name', 'class_id',
backend/apps/applications/serializers.py:13:        read_only_fields = ['application_id', 'student_id', 'student_name',
backend/apps/applications/serializers.py:14:                            'class_id', 'status', 'created_at', 'updated_at']
backend/apps/applications/serializers.py:17:class ApplicationSerializer(serializers.ModelSerializer):
backend/apps/applications/serializers.py:18:    student_id = serializers.CharField(source='student.user_id', read_only=True)
backend/apps/applications/serializers.py:21:    class Meta:
backend/apps/applications/serializers.py:23:        fields = ['application_id', 'student_id', 'student_name', 'class_id',
backend/apps/applications/serializers.py:26:        read_only_fields = ['application_id', 'student_id', 'student_name',
backend/apps/applications/serializers.py:27:                            'class_id', 'status', 'dorm_checkout_status',
backend/apps/applications/serializers.py:35:class ApplicationCreateSerializer(serializers.Serializer):
backend/apps/applications/serializers.py:52:class ApplicationListResponseSerializer(serializers.Serializer):
backend/apps/users/tests/test_import_csv.py:7:from apps.users.models import User, UserRole
backend/apps/users/tests/test_import_csv.py:8:from apps.users.class_mapping import ClassMapping
backend/apps/users/tests/test_import_csv.py:11:class ImportCSVCommandTest(TestCase):
backend/apps/users/tests/test_import_csv.py:14:        User.objects.create_user(user_id='T001', name='李老师', role=UserRole.COUNSELOR, password='T001')
backend/apps/users/tests/test_import_csv.py:15:        User.objects.create_user(user_id='T002', name='王老师', role=UserRole.COUNSELOR, password='T002')
backend/apps/users/tests/test_import_csv.py:33:            self.assertEqual(User.objects.filter(role=UserRole.COUNSELOR).count(), 4)
backend/apps/users/tests/test_import_csv.py:34:            self.assertTrue(User.objects.filter(user_id='T003', name='张老师').exists())
backend/apps/users/tests/test_import_csv.py:68:        csv_content = "class_id,counselor_employee_id\nCS2020-01,T001\nCS2020-02,T002"
backend/apps/users/tests/test_import_csv.py:76:            mapping = ClassMapping.objects.get(class_id='CS2020-01')
backend/apps/users/tests/test_import_csv.py:83:        csv_content = "class_id,counselor_employee_id\nCS2020-01,T999"
backend/apps/users/tests/test_import_csv.py:97:    def test_import_students_success(self):
backend/apps/users/tests/test_import_csv.py:98:        """Test successful student import"""
backend/apps/users/tests/test_import_csv.py:99:        counselor = User.objects.get(user_id='T001')
backend/apps/users/tests/test_import_csv.py:100:        ClassMapping.objects.create(class_id='CS2020-01', counselor=counselor, counselor_name='李老师')
backend/apps/users/tests/test_import_csv.py:102:        csv_content = "student_id,name,class_id,is_graduating,graduation_year\n2020001,张三,CS2020-01,true,2024"
backend/apps/users/tests/test_import_csv.py:107:            call_command('import_csv', '--students', filepath, stdout=out)
backend/apps/users/tests/test_import_csv.py:109:            self.assertEqual(User.objects.filter(role=UserRole.STUDENT).count(), 1)
backend/apps/users/tests/test_import_csv.py:110:            student = User.objects.get(user_id='2020001')
backend/apps/users/tests/test_import_csv.py:111:            self.assertEqual(student.name, '张三')
backend/apps/users/tests/test_import_csv.py:112:            self.assertEqual(student.class_id, 'CS2020-01')
backend/apps/users/tests/test_import_csv.py:113:            self.assertTrue(student.is_graduating)
backend/apps/users/tests/test_import_csv.py:117:    def test_import_students_class_mapping_missing(self):
backend/apps/users/tests/test_import_csv.py:118:        """Test student import with missing class mapping"""
backend/apps/users/tests/test_import_csv.py:119:        csv_content = "student_id,name,class_id,is_graduating,graduation_year\n2020001,张三,CS2020-99,true,2024"
backend/apps/users/tests/test_import_csv.py:124:            call_command('import_csv', '--students', filepath, stdout=out)
backend/apps/users/tests/test_import_csv.py:129:            self.assertEqual(User.objects.filter(role=UserRole.STUDENT).count(), 0)
backend/apps/users/tests/test_import_csv.py:145:            self.assertFalse(User.objects.filter(user_id='T005').exists())
backend/apps/users/tests/test_import_csv.py:155:            initial_count = User.objects.filter(role=UserRole.COUNSELOR).count()
backend/apps/users/tests/test_import_csv.py:161:            final_count = User.objects.filter(role=UserRole.COUNSELOR).count()
backend/apps/applications/tests/test_serializer_validation.py:8:class ApplicationCreateSerializerTest(TestCase):
backend/apps/applications/models.py:3:from apps.users.models import User
backend/apps/applications/models.py:6:class ApplicationStatus(models.TextChoices):
backend/apps/applications/models.py:14:class DormCheckoutStatus(models.TextChoices):
backend/apps/applications/models.py:21:class Application(models.Model):
backend/apps/applications/models.py:23:    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='applications')
backend/apps/applications/models.py:24:    student_name = models.CharField(max_length=100)
backend/apps/applications/models.py:25:    class_id = models.CharField(max_length=50)
backend/apps/applications/models.py:33:    class Meta:
backend/apps/applications/models.py:39:                student=self.student,
backend/apps/applications/tests/test_list_permissions.py:3:from apps.users.models import User, UserRole
backend/apps/applications/tests/test_list_permissions.py:4:from apps.users.class_mapping import ClassMapping
backend/apps/applications/tests/test_list_permissions.py:9:class ApplicationListPermissionTest(TestCase):
backend/apps/applications/tests/test_list_permissions.py:14:        self.student1 = User.objects.create(user_id='S001', name='学生1', role=UserRole.STUDENT, class_id='CS2020-01')
backend/apps/applications/tests/test_list_permissions.py:15:        self.student1.set_password('S001')
backend/apps/applications/tests/test_list_permissions.py:16:        self.student1.save()
backend/apps/applications/tests/test_list_permissions.py:18:        self.student2 = User.objects.create(user_id='S002', name='学生2', role=UserRole.STUDENT, class_id='CS2020-02')
backend/apps/applications/tests/test_list_permissions.py:19:        self.student2.set_password('S002')
backend/apps/applications/tests/test_list_permissions.py:20:        self.student2.save()
backend/apps/applications/tests/test_list_permissions.py:22:        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
backend/apps/applications/tests/test_list_permissions.py:26:        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
backend/apps/applications/tests/test_list_permissions.py:30:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
backend/apps/applications/tests/test_list_permissions.py:34:        # Create class mappings
backend/apps/applications/tests/test_list_permissions.py:35:        ClassMapping.objects.create(class_id='CS2020-01', counselor=self.counselor1, counselor_name='辅导员1', active=True)
backend/apps/applications/tests/test_list_permissions.py:36:        ClassMapping.objects.create(class_id='CS2020-02', counselor=self.counselor2, counselor_name='辅导员2', active=True)
backend/apps/applications/tests/test_list_permissions.py:41:            student=self.student1,
backend/apps/applications/tests/test_list_permissions.py:42:            student_name='学生1',
backend/apps/applications/tests/test_list_permissions.py:43:            class_id='CS2020-01',
backend/apps/applications/tests/test_list_permissions.py:51:            student=self.student2,
backend/apps/applications/tests/test_list_permissions.py:52:            student_name='学生2',
backend/apps/applications/tests/test_list_permissions.py:53:            class_id='CS2020-02',
backend/apps/applications/tests/test_list_permissions.py:78:    def test_student_sees_only_own_applications(self):
backend/apps/applications/tests/test_list_permissions.py:79:        self.client.force_authenticate(user=self.student1)
backend/apps/applications/tests/test_list_permissions.py:85:    def test_student_cannot_see_other_student_applications(self):
backend/apps/applications/tests/test_list_permissions.py:86:        self.client.force_authenticate(user=self.student1)
backend/apps/applications/tests/test_list_permissions.py:111:        self.client.force_authenticate(user=self.student1)
backend/apps/applications/tests/test_constraints.py:6:from apps.users.models import User, UserRole
backend/apps/applications/tests/test_constraints.py:8:from apps.users.class_mapping import ClassMapping
backend/apps/applications/tests/test_constraints.py:11:class ApplicationConstraintsTestCase(TestCase):
backend/apps/applications/tests/test_constraints.py:13:        # Create student
backend/apps/applications/tests/test_constraints.py:14:        self.student = User.objects.create_user(
backend/apps/applications/tests/test_constraints.py:17:            role=UserRole.STUDENT,
backend/apps/applications/tests/test_constraints.py:18:            class_id='CS2020-01',
backend/apps/applications/tests/test_constraints.py:25:        self.counselor = User.objects.create_user(
backend/apps/applications/tests/test_constraints.py:28:            role=UserRole.COUNSELOR,
backend/apps/applications/tests/test_constraints.py:32:        # Create class mapping
backend/apps/applications/tests/test_constraints.py:34:            class_id='CS2020-01',
backend/apps/applications/tests/test_constraints.py:44:        self.client.force_authenticate(user=self.student)
backend/apps/applications/tests/test_application_flow.py:6:from apps.users.models import User, UserRole
backend/apps/applications/tests/test_application_flow.py:7:from apps.users.class_mapping import ClassMapping
backend/apps/applications/tests/test_application_flow.py:12:class ApplicationFlowTestCase(TestCase):
backend/apps/applications/tests/test_application_flow.py:17:        self.student = User.objects.create_user(
backend/apps/applications/tests/test_application_flow.py:21:            role=UserRole.STUDENT,
backend/apps/applications/tests/test_application_flow.py:22:            class_id='CS2020-01',
backend/apps/applications/tests/test_application_flow.py:27:        self.counselor = User.objects.create_user(
backend/apps/applications/tests/test_application_flow.py:31:            role=UserRole.COUNSELOR
backend/apps/applications/tests/test_application_flow.py:34:        self.dean = User.objects.create_user(
backend/apps/applications/tests/test_application_flow.py:38:            role=UserRole.DEAN
backend/apps/applications/tests/test_application_flow.py:41:        # Create class mapping
backend/apps/applications/tests/test_application_flow.py:43:            class_id='CS2020-01',
backend/apps/applications/tests/test_application_flow.py:58:        student_token = response.data['access_token']
backend/apps/applications/tests/test_application_flow.py:61:        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
backend/apps/applications/tests/test_application_flow.py:110:        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {student_token}')
backend/apps/users/migrations/0001_initial.py:8:class Migration(migrations.Migration):
backend/apps/users/migrations/0001_initial.py:18:            name='User',
backend/apps/users/migrations/0001_initial.py:25:                ('role', models.CharField(choices=[('student', '学生'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20)),
backend/apps/users/migrations/0001_initial.py:27:                ('class_id', models.CharField(blank=True, max_length=50, null=True)),
backend/apps/users/migrations/0001_initial.py:43:                ('class_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
backend/apps/users/migrations/0001_initial.py:48:                ('counselor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='managed_classes', to=settings.AUTH_USER_MODEL)),
backend/apps/users/migrations/0001_initial.py:51:                'db_table': 'class_mappings',
backend/apps/users/apps.py:4:class UsersConfig(AppConfig):
backend/apps/notifications/views.py:3:from rest_framework.decorators import api_view, permission_classes
backend/apps/notifications/views.py:28:@permission_classes([IsAuthenticated])
backend/apps/notifications/views.py:73:@permission_classes([IsAuthenticated])
backend/apps/notifications/views.py:96:@permission_classes([IsAuthenticated])
backend/apps/notifications/views.py:140:@permission_classes([IsAuthenticated])
backend/apps/users/__init__.py:1:# Users app
backend/apps/notifications/serializers.py:5:class NotificationSerializer(serializers.ModelSerializer):
backend/apps/notifications/serializers.py:6:    class Meta:
backend/apps/notifications/serializers.py:26:class NotificationListResponseSerializer(serializers.Serializer):
backend/apps/users/admin.py:2:from .models import User
backend/apps/users/admin.py:3:from .class_mapping import ClassMapping
backend/apps/users/admin.py:6:@admin.register(User)
backend/apps/users/admin.py:7:class UserAdmin(admin.ModelAdmin):
backend/apps/users/admin.py:8:    list_display = ['user_id', 'name', 'role', 'class_id', 'active']
backend/apps/users/admin.py:10:    search_fields = ['user_id', 'name', 'class_id']
backend/apps/users/admin.py:15:class ClassMappingAdmin(admin.ModelAdmin):
backend/apps/users/admin.py:16:    list_display = ['class_id', 'counselor', 'counselor_name', 'active']
backend/apps/users/admin.py:18:    search_fields = ['class_id', 'counselor__user_id', 'counselor_name']
backend/apps/users/admin.py:19:    ordering = ['class_id']
backend/apps/notifications/services.py:14:User = get_user_model()
backend/apps/notifications/services.py:19:    Create notification for counselor when student submits application.
backend/apps/notifications/services.py:29:    message = f"学生{application.student_name}（{application.student.user_id}）提交了离校申请，请及时审批。"
backend/apps/notifications/services.py:37:            'actor': application.student,
backend/apps/notifications/services.py:46:    Create notification for student when approval is approved or rejected.
backend/apps/notifications/services.py:66:        recipient=approval.application.student,
backend/apps/notifications/services.py:99:    ).select_related('approver', 'application__student')
backend/apps/notifications/services.py:113:        message = f"学生{approval.application.student_name}的离校申请已超过{days}天未审批，请及时处理。"
backend/apps/notifications/models.py:14:class NotificationType(models.TextChoices):
backend/apps/notifications/models.py:21:class EntityType(models.TextChoices):
backend/apps/notifications/models.py:26:class Notification(models.Model):
backend/apps/notifications/models.py:79:    class Meta:
backend/apps/notifications/admin.py:6:class NotificationAdmin(admin.ModelAdmin):
backend/apps/users/integrations/xg_user_client.py:46:class XGUserAPIConfig:
backend/apps/users/integrations/xg_user_client.py:81:class XGUserAPIClient:
backend/apps/users/integrations/xg_user_client.py:84:    def __init__(self, config: XGUserAPIConfig):
backend/apps/notifications/migrations/0001_initial.py:9:class Migration(migrations.Migration):
backend/apps/notifications/migrations/0002_alter_notification_type.py:6:class Migration(migrations.Migration):
backend/apps/notifications/tests/test_models.py:3:from apps.users.models import User
backend/apps/notifications/tests/test_models.py:7:class NotificationModelTest(TestCase):
backend/apps/notifications/tests/test_models.py:9:        self.student = User.objects.create(
backend/apps/notifications/tests/test_models.py:12:            role='student',
backend/apps/notifications/tests/test_models.py:13:            class_id='CS2020-01'
backend/apps/notifications/tests/test_models.py:15:        self.counselor = User.objects.create(
backend/apps/notifications/tests/test_models.py:24:            recipient=self.student,
backend/apps/notifications/tests/test_models.py:35:        self.assertEqual(notification.recipient, self.student)
backend/apps/notifications/tests/test_models.py:41:            recipient=self.student,
backend/apps/notifications/tests/test_models.py:49:            recipient=self.student,
backend/apps/notifications/tests/test_models.py:61:            recipient=self.student,
backend/apps/notifications/tests/test_models.py:70:                recipient=self.student,
backend/apps/notifications/tests/test_models.py:80:        student2 = User.objects.create(
backend/apps/notifications/tests/test_models.py:83:            role='student',
backend/apps/notifications/tests/test_models.py:84:            class_id='CS2020-01'
backend/apps/notifications/tests/test_models.py:87:            recipient=self.student,
backend/apps/notifications/tests/test_models.py:95:            recipient=student2,
backend/apps/notifications/tests/test_models.py:107:            recipient=self.student,
backend/apps/notifications/tests/test_models.py:115:            recipient=self.student,
backend/apps/notifications/apps.py:4:class NotificationsConfig(AppConfig):
backend/apps/notifications/tests/test_timeout_warnings.py:10:User = get_user_model()
backend/apps/notifications/tests/test_timeout_warnings.py:13:class ApprovalTimeoutWarningTests(TestCase):
backend/apps/notifications/tests/test_timeout_warnings.py:15:        self.student = User.objects.create_user(
backend/apps/notifications/tests/test_timeout_warnings.py:18:            role='student',
backend/apps/notifications/tests/test_timeout_warnings.py:19:            class_id='CS2020-1'
backend/apps/notifications/tests/test_timeout_warnings.py:21:        self.counselor = User.objects.create_user(
backend/apps/notifications/tests/test_timeout_warnings.py:25:            class_id='CS2020-1'
backend/apps/notifications/tests/test_timeout_warnings.py:27:        self.dean = User.objects.create_user(
backend/apps/notifications/tests/test_timeout_warnings.py:36:            student=self.student,
backend/apps/notifications/tests/test_timeout_warnings.py:59:            student=self.student,
backend/apps/notifications/tests/test_timeout_warnings.py:82:            student=self.student,
backend/apps/notifications/tests/test_timeout_warnings.py:100:            student=self.student,
backend/apps/notifications/tests/test_timeout_warnings.py:121:            student=self.student,
backend/apps/notifications/tests/test_timeout_warnings.py:144:            student=self.student,
backend/apps/notifications/tests/test_auto_notifications.py:5:- Student submits application (APPLICATION_SUBMITTED)
backend/apps/notifications/tests/test_auto_notifications.py:19:User = get_user_model()
backend/apps/notifications/tests/test_auto_notifications.py:22:class AutoNotificationTest(TestCase):
backend/apps/notifications/tests/test_auto_notifications.py:27:        self.student = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications.py:30:            role='student',
backend/apps/notifications/tests/test_auto_notifications.py:31:            class_id='CS2021-1'
backend/apps/notifications/tests/test_auto_notifications.py:33:        self.counselor = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications.py:38:        self.dean = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications.py:48:            student=self.student,
backend/apps/notifications/tests/test_auto_notifications.py:49:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications.py:50:            class_id=self.student.class_id,
backend/apps/notifications/tests/test_auto_notifications.py:69:        self.assertEqual(notification.actor, self.student)
backend/apps/notifications/tests/test_auto_notifications.py:80:            student=self.student,
backend/apps/notifications/tests/test_auto_notifications.py:81:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications.py:82:            class_id=self.student.class_id,
backend/apps/notifications/tests/test_auto_notifications.py:100:        self.assertEqual(notification.recipient, self.student)
backend/apps/notifications/tests/test_auto_notifications.py:111:            student=self.student,
backend/apps/notifications/tests/test_auto_notifications.py:112:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications.py:113:            class_id=self.student.class_id,
backend/apps/notifications/tests/test_auto_notifications.py:131:        self.assertEqual(notification.recipient, self.student)
backend/apps/notifications/tests/test_auto_notifications.py:140:            student=self.student,
backend/apps/notifications/tests/test_auto_notifications.py:141:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications.py:142:            class_id=self.student.class_id,
backend/apps/notifications/tests/test_auto_notifications.py:161:        self.assertEqual(notification.recipient, self.student)
backend/apps/notifications/tests/test_auto_notifications.py:171:            student=self.student,
backend/apps/notifications/tests/test_auto_notifications.py:172:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications.py:173:            class_id=self.student.class_id,
backend/apps/notifications/tests/test_auto_notifications.py:206:            student=self.student,
backend/apps/notifications/tests/test_auto_notifications.py:207:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications.py:208:            class_id=self.student.class_id,
backend/apps/notifications/tests/test_auto_notifications.py:231:            recipient=self.student,
backend/apps/users/tests/test_xg_user_client.py:4:from apps.users.integrations.xg_user_client import generate_sign, XGUserAPIConfig, XGUserAPIClient
backend/apps/users/tests/test_xg_user_client.py:7:class GenerateSignTests(TestCase):
backend/apps/users/tests/test_xg_user_client.py:49:class XGUserAPIConfigTests(TestCase):
backend/apps/users/tests/test_xg_user_client.py:54:        config = XGUserAPIConfig()
backend/apps/users/tests/test_xg_user_client.py:65:            XGUserAPIConfig()
backend/apps/users/tests/test_xg_user_client.py:72:            XGUserAPIConfig()
backend/apps/users/tests/test_xg_user_client.py:79:            XGUserAPIConfig()
backend/apps/users/tests/test_xg_user_client.py:86:            XGUserAPIConfig()
backend/apps/users/tests/test_xg_user_client.py:93:            XGUserAPIConfig()
backend/apps/users/tests/test_xg_user_client.py:99:        config = XGUserAPIConfig()
backend/apps/users/tests/test_xg_user_client.py:105:        config = XGUserAPIConfig()
backend/apps/users/tests/test_xg_user_client.py:111:        config = XGUserAPIConfig()
backend/apps/users/tests/test_xg_user_client.py:115:class XGUserAPIClientTests(TestCase):
backend/apps/users/tests/test_xg_user_client.py:127:        self.config = XGUserAPIConfig()
backend/apps/users/tests/test_xg_user_client.py:128:        self.client = XGUserAPIClient(self.config)
backend/apps/users/tests/test_xg_user_client.py:248:                'data': [{'name': f'User{i}', 'number': f'202100{i}'} for i in range(1, 6)]
backend/apps/users/management/commands/seed_data.py:2:from apps.users.models import User, UserRole
backend/apps/users/management/commands/seed_data.py:3:from apps.users.class_mapping import ClassMapping
backend/apps/users/management/commands/seed_data.py:6:class Command(BaseCommand):
backend/apps/users/management/commands/seed_data.py:27:        # Students (10)
backend/apps/users/management/commands/seed_data.py:28:        students = [
backend/apps/users/management/commands/seed_data.py:29:            {'user_id': '2020001', 'name': '张三', 'class_id': 'CS2020-01'},
backend/apps/users/management/commands/seed_data.py:30:            {'user_id': '2020002', 'name': '李四', 'class_id': 'CS2020-02'},
backend/apps/users/management/commands/seed_data.py:31:            {'user_id': '2020003', 'name': '王五', 'class_id': 'CS2020-01'},
backend/apps/users/management/commands/seed_data.py:32:            {'user_id': '2020004', 'name': '赵六', 'class_id': 'CS2020-01'},
backend/apps/users/management/commands/seed_data.py:33:            {'user_id': '2020005', 'name': '孙七', 'class_id': 'CS2020-01'},
backend/apps/users/management/commands/seed_data.py:34:            {'user_id': '2020006', 'name': '周八', 'class_id': 'CS2020-02'},
backend/apps/users/management/commands/seed_data.py:35:            {'user_id': '2020007', 'name': '吴九', 'class_id': 'CS2020-02'},
backend/apps/users/management/commands/seed_data.py:36:            {'user_id': '2020008', 'name': '郑十', 'class_id': 'CS2020-02'},
backend/apps/users/management/commands/seed_data.py:37:            {'user_id': '2020009', 'name': '王十一', 'class_id': 'CS2020-02'},
backend/apps/users/management/commands/seed_data.py:38:            {'user_id': '2020010', 'name': '王十二', 'class_id': 'CS2020-02'},
backend/apps/users/management/commands/seed_data.py:41:        for student_data in students:
backend/apps/users/management/commands/seed_data.py:42:            user, created = User.objects.update_or_create(
backend/apps/users/management/commands/seed_data.py:43:                user_id=student_data['user_id'],
backend/apps/users/management/commands/seed_data.py:45:                    'name': student_data['name'],
backend/apps/users/management/commands/seed_data.py:46:                    'role': UserRole.STUDENT,
backend/apps/users/management/commands/seed_data.py:47:                    'class_id': student_data['class_id'],
backend/apps/users/management/commands/seed_data.py:54:                user.set_password(student_data['user_id'])
backend/apps/users/management/commands/seed_data.py:56:            self.stdout.write(f'{"Created" if created else "Updated"} student: {user.user_id}')
backend/apps/users/management/commands/seed_data.py:65:            user, created = User.objects.get_or_create(
backend/apps/users/management/commands/seed_data.py:69:                    'role': UserRole.COUNSELOR,
backend/apps/users/management/commands/seed_data.py:79:        user, created = User.objects.get_or_create(
backend/apps/users/management/commands/seed_data.py:83:                'role': UserRole.DEAN,
backend/apps/users/management/commands/seed_data.py:94:            {'class_id': 'CS2020-01', 'counselor_id': 'T001'},
backend/apps/users/management/commands/seed_data.py:95:            {'class_id': 'CS2020-02', 'counselor_id': 'T002'},
backend/apps/users/management/commands/seed_data.py:99:            counselor = User.objects.get(user_id=mapping_data['counselor_id'])
backend/apps/users/management/commands/seed_data.py:101:                class_id=mapping_data['class_id'],
backend/apps/users/management/commands/seed_data.py:109:                self.stdout.write(f'Created mapping: {mapping.class_id} -> {counselor.user_id}')
backend/apps/notifications/management/commands/seed_notifications.py:3:from apps.users.models import User
backend/apps/notifications/management/commands/seed_notifications.py:7:class Command(BaseCommand):
backend/apps/notifications/management/commands/seed_notifications.py:11:        students = User.objects.filter(role='student')[:3]
backend/apps/notifications/management/commands/seed_notifications.py:13:        if not students:
backend/apps/notifications/management/commands/seed_notifications.py:19:        for i, student in enumerate(students):
backend/apps/notifications/management/commands/seed_notifications.py:21:                recipient=student,
backend/apps/notifications/management/commands/seed_notifications.py:32:                    recipient=student,
backend/apps/users/management/commands/import_csv.py:4:from apps.users.models import User, UserRole
backend/apps/users/management/commands/import_csv.py:5:from apps.users.class_mapping import ClassMapping
backend/apps/users/management/commands/import_csv.py:8:class Command(BaseCommand):
backend/apps/users/management/commands/import_csv.py:9:    help = 'Import users and class mappings from CSV files'
backend/apps/users/management/commands/import_csv.py:12:        parser.add_argument('--students', type=str, help='Path to students CSV file')
backend/apps/users/management/commands/import_csv.py:14:        parser.add_argument('--mappings', type=str, help='Path to class mappings CSV file')
backend/apps/users/management/commands/import_csv.py:24:            'students': {'created': 0, 'updated': 0, 'failed': 0, 'errors': []},
backend/apps/users/management/commands/import_csv.py:29:        if options['students']:
backend/apps/users/management/commands/import_csv.py:30:            self.import_students(options['students'], dry_run, summary['students'])
backend/apps/users/management/commands/import_csv.py:49:    def import_students(self, filepath, dry_run, summary):
backend/apps/users/management/commands/import_csv.py:50:        """Import students from CSV with validation"""
backend/apps/users/management/commands/import_csv.py:51:        required_fields = ['student_id', 'name', 'class_id', 'is_graduating', 'graduation_year']
backend/apps/users/management/commands/import_csv.py:72:                    student_id = row['student_id'].strip()
backend/apps/users/management/commands/import_csv.py:73:                    if student_id in seen_ids:
backend/apps/users/management/commands/import_csv.py:74:                        summary['errors'].append(f"Row {row_num}: Duplicate student_id '{student_id}'")
backend/apps/users/management/commands/import_csv.py:77:                    seen_ids.add(student_id)
backend/apps/users/management/commands/import_csv.py:79:                    # Validate class_id has mapping
backend/apps/users/management/commands/import_csv.py:80:                    class_id = row['class_id'].strip()
backend/apps/users/management/commands/import_csv.py:81:                    if not dry_run and not ClassMapping.objects.filter(class_id=class_id).exists():
backend/apps/users/management/commands/import_csv.py:82:                        summary['errors'].append(f"Row {row_num}: class_id '{class_id}' has no counselor mapping")
backend/apps/users/management/commands/import_csv.py:87:                        exists = User.objects.filter(user_id=student_id).exists()
backend/apps/users/management/commands/import_csv.py:93:                        user, created = User.objects.update_or_create(
backend/apps/users/management/commands/import_csv.py:94:                            user_id=student_id,
backend/apps/users/management/commands/import_csv.py:97:                                'role': UserRole.STUDENT,
backend/apps/users/management/commands/import_csv.py:98:                                'class_id': class_id,
backend/apps/users/management/commands/import_csv.py:104:                            user.set_password(row.get('password', student_id))
backend/apps/users/management/commands/import_csv.py:110:                        self.stdout.write(f'{"Created" if created else "Updated"} student: {user.user_id}')
backend/apps/users/management/commands/import_csv.py:115:            raise CommandError(f"Error importing students: {str(e)}")
backend/apps/users/management/commands/import_csv.py:149:                        exists = User.objects.filter(user_id=employee_id).exists()
backend/apps/users/management/commands/import_csv.py:155:                        user, created = User.objects.update_or_create(
backend/apps/users/management/commands/import_csv.py:159:                                'role': UserRole.COUNSELOR,
backend/apps/users/management/commands/import_csv.py:178:        """Import class mappings from CSV with validation"""
backend/apps/users/management/commands/import_csv.py:179:        required_fields = ['class_id', 'counselor_employee_id']
backend/apps/users/management/commands/import_csv.py:200:                    class_id = row['class_id'].strip()
backend/apps/users/management/commands/import_csv.py:201:                    if class_id in seen_ids:
backend/apps/users/management/commands/import_csv.py:202:                        summary['errors'].append(f"Row {row_num}: Duplicate class_id '{class_id}'")
backend/apps/users/management/commands/import_csv.py:205:                    seen_ids.add(class_id)
backend/apps/users/management/commands/import_csv.py:211:                            counselor = User.objects.get(user_id=counselor_id, role=UserRole.COUNSELOR)
backend/apps/users/management/commands/import_csv.py:212:                        except User.DoesNotExist:
backend/apps/users/management/commands/import_csv.py:218:                        exists = ClassMapping.objects.filter(class_id=class_id).exists()
backend/apps/users/management/commands/import_csv.py:225:                            class_id=class_id,
backend/apps/users/management/commands/import_csv.py:236:                        self.stdout.write(f'{"Created" if created else "Updated"} mapping: {mapping.class_id} -> {counselor.user_id}')
backend/apps/notifications/management/commands/send_approval_timeout_warnings.py:5:class Command(BaseCommand):
backend/apps/notifications/tests/test_api.py:4:from apps.users.models import User
backend/apps/notifications/tests/test_api.py:8:class NotificationAPITest(TestCase):
backend/apps/notifications/tests/test_api.py:11:        self.student1 = User.objects.create(
backend/apps/notifications/tests/test_api.py:14:            role='student',
backend/apps/notifications/tests/test_api.py:15:            class_id='CS2020-01'
backend/apps/notifications/tests/test_api.py:17:        self.student2 = User.objects.create(
backend/apps/notifications/tests/test_api.py:20:            role='student',
backend/apps/notifications/tests/test_api.py:21:            class_id='CS2020-02'
backend/apps/notifications/tests/test_api.py:23:        self.counselor = User.objects.create(
backend/apps/notifications/tests/test_api.py:32:            recipient=self.student1,
backend/apps/notifications/tests/test_api.py:40:            recipient=self.student1,
backend/apps/notifications/tests/test_api.py:48:        self.client.force_authenticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:58:            recipient=self.student1,
backend/apps/notifications/tests/test_api.py:66:            recipient=self.student1,
backend/apps/notifications/tests/test_api.py:75:        self.client.force_authenticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:90:                recipient=self.student1,
backend/apps/notifications/tests/test_api.py:98:        self.client.force_authenticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:110:            recipient=self.student1,
backend/apps/notifications/tests/test_api.py:118:            recipient=self.student2,
backend/apps/notifications/tests/test_api.py:126:        self.client.force_authenticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:133:            recipient=self.student1,
backend/apps/notifications/tests/test_api.py:141:            recipient=self.student1,
backend/apps/notifications/tests/test_api.py:150:        self.client.force_authenticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:159:            recipient=self.student1,
backend/apps/notifications/tests/test_api.py:167:        self.client.force_authenticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:179:            recipient=self.student1,
backend/apps/notifications/tests/test_api.py:187:        self.client.force_authenticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:200:            recipient=self.student1,
backend/apps/notifications/tests/test_api.py:208:        self.client.force_authenticate(user=self.student2)
backend/apps/notifications/tests/test_api.py:216:        self.client.force_authenticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:225:            recipient=self.student1,
backend/apps/notifications/tests/test_api.py:233:            recipient=self.student1,
backend/apps/notifications/tests/test_api.py:241:        self.client.force_authenticate(user=self.student1)
backend/apps/notifications/tests/test_api.py:248:            recipient=self.student1,
backend/apps/notifications/tests/test_auto_notifications_api.py:14:from apps.users.class_mapping import ClassMapping
backend/apps/notifications/tests/test_auto_notifications_api.py:16:User = get_user_model()
backend/apps/notifications/tests/test_auto_notifications_api.py:19:class AutoNotificationAPITest(TestCase):
backend/apps/notifications/tests/test_auto_notifications_api.py:23:        """Create test users and class mapping."""
backend/apps/notifications/tests/test_auto_notifications_api.py:26:        self.student = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications_api.py:29:            role='student',
backend/apps/notifications/tests/test_auto_notifications_api.py:30:            class_id='CS2021-1'
backend/apps/notifications/tests/test_auto_notifications_api.py:32:        self.counselor = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications_api.py:37:        self.dean = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications_api.py:44:            class_id='CS2021-1',
backend/apps/notifications/tests/test_auto_notifications_api.py:51:        """Test counselor can see APPLICATION_SUBMITTED notification via API after student submits."""
backend/apps/notifications/tests/test_auto_notifications_api.py:52:        # Student submits application (triggers notification)
backend/apps/notifications/tests/test_auto_notifications_api.py:53:        self.client.force_authenticate(user=self.student)
backend/apps/notifications/tests/test_auto_notifications_api.py:72:        """Test student can see APPROVAL_APPROVED notification via API after counselor approves."""
backend/apps/notifications/tests/test_auto_notifications_api.py:76:            student=self.student,
backend/apps/notifications/tests/test_auto_notifications_api.py:77:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:78:            class_id=self.student.class_id,
backend/apps/notifications/tests/test_auto_notifications_api.py:100:        # Student checks notifications via API
backend/apps/notifications/tests/test_auto_notifications_api.py:101:        self.client.force_authenticate(user=self.student)
backend/apps/notifications/tests/test_auto_notifications_api.py:118:            student=self.student,
backend/apps/notifications/tests/test_auto_notifications_api.py:119:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:120:            class_id=self.student.class_id,
backend/apps/notifications/tests/test_auto_notifications_api.py:142:        # Student checks notification
backend/apps/notifications/tests/test_auto_notifications_api.py:143:        self.client.force_authenticate(user=self.student)
backend/apps/notifications/tests/test_auto_notifications_api.py:153:        # Create application for student1
backend/apps/notifications/tests/test_auto_notifications_api.py:154:        student2 = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications_api.py:157:            role='student',
backend/apps/notifications/tests/test_auto_notifications_api.py:158:            class_id='CS2021-2'
backend/apps/notifications/tests/test_auto_notifications_api.py:163:            student=self.student,
backend/apps/notifications/tests/test_auto_notifications_api.py:164:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:165:            class_id=self.student.class_id,
backend/apps/notifications/tests/test_auto_notifications_api.py:180:        # Student2 tries to approve (should fail with permission denied)
backend/apps/notifications/tests/test_auto_notifications_api.py:181:        self.client.force_authenticate(user=student2)
backend/apps/notifications/tests/test_auto_notifications_api.py:198:            student=self.student,
backend/apps/notifications/tests/test_auto_notifications_api.py:199:            student_name=self.student.name,
backend/apps/notifications/tests/test_auto_notifications_api.py:200:            class_id=self.student.class_id,
backend/apps/notifications/tests/test_auto_notifications_api.py:224:            recipient=self.student,
backend/apps/notifications/tests/test_auto_notifications_api.py:231:        # Create student with non-completed dorm status (use ID not in mock data)
backend/apps/notifications/tests/test_auto_notifications_api.py:232:        blocked_student = User.objects.create_user(
backend/apps/notifications/tests/test_auto_notifications_api.py:235:            role='student',
backend/apps/notifications/tests/test_auto_notifications_api.py:236:            class_id='CS2021-1'
backend/apps/notifications/tests/test_auto_notifications_api.py:239:        # Student tries to submit application (should fail with 422 dorm blocked)
backend/apps/notifications/tests/test_auto_notifications_api.py:240:        self.client.force_authenticate(user=blocked_student)
backend/apps/notifications/tests/test_auto_notifications_api.py:248:        self.assertEqual(Application.objects.filter(student=blocked_student).count(), 0)
backend/apps/notifications/tests/test_auto_notifications_api.py:250:        # Verify no notification was created for the blocked student
backend/apps/notifications/tests/test_auto_notifications_api.py:251:        self.assertEqual(Notification.objects.filter(recipient=blocked_student).count(), 0)

exec
/bin/bash -lc "rtk rg --files backend/apps | rtk rg 'models.py|serializers.py|management|users|graduation|students'" in /home/caohui/projects/graduation-leave-system
 succeeded in 184ms:
backend/apps/approvals/serializers.py
backend/apps/approvals/models.py
backend/apps/applications/serializers.py
backend/apps/applications/models.py
backend/apps/users/integrations/__init__.py
backend/apps/users/class_mapping.py
backend/apps/users/integrations/xg_user_client.py
backend/apps/users/__init__.py
backend/apps/users/admin.py
backend/apps/users/urls.py
backend/apps/users/migrations/__init__.py
backend/apps/users/migrations/0001_initial.py
backend/apps/users/apps.py
backend/apps/users/models.py
backend/apps/users/management/__init__.py
backend/apps/attachments/serializers.py
backend/apps/attachments/models.py
backend/apps/users/management/commands/__init__.py
backend/apps/users/management/commands/import_csv.py
backend/apps/users/management/commands/seed_data.py
backend/apps/users/serializers.py
backend/apps/users/views.py
backend/apps/notifications/serializers.py
backend/apps/notifications/models.py
backend/apps/notifications/management/__init__.py
backend/apps/notifications/management/commands/__init__.py
backend/apps/users/tests/__init__.py
backend/apps/users/tests/test_xg_user_client.py
backend/apps/users/tests/test_import_csv.py
backend/apps/notifications/management/commands/send_approval_timeout_warnings.py
backend/apps/notifications/management/commands/seed_notifications.py
backend/apps/notifications/tests/test_models.py

codex
The internal `User` table is small but the CSV importer already treats several fields as operational requirements: `student_id`, `name`, `class_id`, `is_graduating`, and `graduation_year`, with class-mapping validation. That makes a pure “just code Step 3” path riskier than it first looks.
exec
/bin/bash -lc "rtk sed -n '110,170p' docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
- live probe 能力存在，但是否已跑真实接口取决于凭证和 `tenantCode`。

**Step 2：分页读取与真实结构验证（下一步）**

范围：
- Step 2A：有凭证则执行一次 live probe，产出脱敏结果。
- Step 2B：实现 `fetch_all_users()`，mock 测试覆盖分页边界。
- Step 2C：整理字段覆盖清单，判断能否支撑用户同步。

验收标准：
- 分页 mock 测试通过。
- 不发生无限循环。
- 能处理 `per_page` 字符串/整数两种形态。
- live 成功时有脱敏字段覆盖报告；live 失败时有明确错误分类和外部问题清单。

**Step 3：字段映射与 Provider 设计**

范围：
- 确定学工字段到本系统 `User`/班级/角色/辅导员关系的映射。
- 明确哪些字段由学工API提供，哪些继续由 CSV/手工配置提供。
- 设计 `UserInfoProvider` 接口和降级策略。

验收标准：
- 有字段映射表。
- 有缺失字段处理规则。
- 有 CSV 与 API 并存策略。
- Provider 只读转换测试通过。

**Step 4：同步服务与数据库写入**

范围：
- 实现幂等 upsert。
- 明确用户停用/缺失策略。
- 增加事务边界、审计摘要、冲突报告。

验收标准：
- 重复同步不产生重复用户。
- 字段冲突可报告。
- 不会误删或误停用本地手工账号。

**Step 5：运维化与验收**

范围：
- 管理命令或后台任务入口。
- dry-run / live-run / summary 输出。
- 运行手册与回滚方案。

验收标准：
- dry-run 可查看变更摘要。
- live-run 有明确确认门。
- 生产凭证不进入仓库、日志和测试输出。

外部依赖阻塞时的备选方案：

- 无凭证：继续完成 Step 2B mock 分页和 Step 3 字段映射草案，但不声明生产可用。
- API不可达：保留 CSV 导入作为主路径，API 对接降级为待外部修复。
- 字段不足：仅使用 API 补充可确定字段，班级/辅导员映射继续由 CSV/Excel 或手工维护提供。

---

## 5. 风险识别

exec
/bin/bash -lc "rtk sed -n '90,150p' docs/discussions/phase4c-next-steps/77-codex-post-step0-strategy-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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

exec
/bin/bash -lc "rtk sed -n '110,180p' docs/discussions/phase4c-next-steps/73-api-data-reading-test-codex-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
- 记录响应状态码、业务 `code/msg`、响应耗时，但不记录敏感header。

必须联系平台部获取准确算法文档。靠猜测可以帮助定位问题，但不能作为交付方案。

### 2. 测试脚本组织建议

推荐采用 **A为主，B为辅**：

```text
backend/scripts/xg_user_api_probe.py
backend/apps/users/integrations/xg_user_client.py
backend/apps/users/tests/test_xg_user_client.py
```

职责划分：

- `xg_user_api_probe.py`：人工运行的诊断入口，读取环境变量，支持 `--algorithm`、`--page-size 1`、`--timeout`、`--dry-run`。
- `xg_user_client.py`：可复用客户端，负责签名、请求构造、响应解析、错误归一化；后续可接入 `RealUserDataProvider`。
- `test_xg_user_client.py`：mock HTTP响应，覆盖签名候选、字段解析、错误处理，不调用真实网络。

不建议把真实API调用写进Django常规测试套件。若确实需要live测试，使用 pytest marker 或环境变量硬门禁，并默认跳过。

### 3. MVP测试范围

第一阶段只做以下5项：

1. 配置校验：必填环境变量齐全，缺失即退出。
2. 请求构造：header/form-data完整，timestamp/randStr/sign存在。
3. 认证验证：用最小请求验证签名算法。
4. 数据结构验证：确认 `code/msg/data/current_page/data/total/per_page` 存在，`data.data` 是列表。
5. 字段采样：仅检查人员记录是否包含 `name/number/phone/identity_id/department/user_identity/updated_at` 等文档字段。

暂不做：

- 全量分页拉取。
- 性能测试。
- 按姓名/手机号过滤的生产验证。
- 错误签名压测。
- 数据入库同步。

这些应等签名、租户、字段映射确认后再做。

### 4. 租户信息获取策略

必须由平台部、学工系统管理员或接口开通记录提供真实 `tenantCode`。不要把文档样例 `C10026` 当成本校租户。

建议向平台部一次性确认：

- 正式环境URL和测试环境URL。
- 本校 `tenantCode`。
- 凭证对应的租户和权限范围。
- 是否限制来源IP。
- 是否有测试租户和测试人员数据。
- 分页最大 `pageNum`、限流策略、时间戳有效窗口。

### 5. 安全性最佳实践

建议新增或使用以下环境变量：

```text
XG_USER_API_URL
XG_USER_API_APP_KEY
XG_USER_API_APP_SECRET
XG_USER_API_TENANT_CODE
XG_USER_API_ENCRYPTION_TYPE=sha1
XG_RUN_LIVE_API_TEST=0
```

当前 `.gitignore` 已覆盖 `.env`、`.env.local`、`.env.*.local`，方向正确。但建议增加一个可提交的示例文件：

```text

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

codex
I’ve got enough to answer now. I’m going to write the Codex response as the next numbered discussion document so Claude has a durable artifact to consume, then I’ll summarize the recommendation here.
codex
I’m creating `91-next-priority-codex-response.md` with the review conclusion. The key decision is to keep Step 2C, but make it a short “mapping contract” gate rather than a broad documentation exercise.
apply patch
patch: completed
/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
diff --git a/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md b/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..b42293300cba0dfed225b660b8a7647b719805e2
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
@@ -0,0 +1,205 @@
+# Phase 4C 下一步优先级讨论 - Codex响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**针对：** `90-next-priority-discussion-request.md`  
+**文档编号：** 91
+
+---
+
+## 审查结论
+
+**推荐优先级：选择 A，但收窄为“Step 2C-lite 字段映射契约”，随后进入 Step 3 的只读 Provider/映射测试。**
+
+不建议直接执行选项 B 或 C 中的“学生数据同步命令并入库”。当前 `fetch_all_users()` 已经解决分页读取问题，但数据库写入不是下一个最低风险动作。下一步应先把学工字段、内部 `User` 字段、CSV补充字段、缺失字段处理规则固定下来。
+
+建议顺序：
+
+1. **Step 2C-lite：字段覆盖与映射契约**
+2. **Step 3：只读 mapper / `UserInfoProvider` 设计与测试**
+3. **Step 4：同步服务与幂等 upsert**
+4. **Step 5：management command 运维入口**
+
+这也与 doc 85 的阶段划分一致：doc 85 中 Step 3 是“字段映射与 Provider 设计”，Step 4 才是“同步服务与数据库写入”，Step 5 才是“管理命令或后台任务入口”。本次请求中的选项 B 实际上把 Step 3、Step 4、Step 5 合并了，风险偏高。
+
+---
+
+## 依赖关系分析
+
+### Step 3是否强依赖Step 2C？
+
+**强依赖，但不是依赖真实凭证；依赖的是字段映射决策。**
+
+没有真实凭证时，仍然可以基于以下材料完成 Step 2C-lite：
+
+- 学工文档样例字段：`name`、`number`、`phone`、`identity_id`、`department`、`user_identity`、`updated_at` 等
+- 当前内部 `User` 模型字段：`user_id`、`name`、`role`、`active`、`class_id`、`is_graduating`、`graduation_year`
+- 当前 CSV 导入命令的业务要求：学生导入要求 `student_id`、`name`、`class_id`、`is_graduating`、`graduation_year`
+- 现有 `ClassMapping` 约束：学生 `class_id` 需要能匹配辅导员映射
+
+因此 Step 2C 不是“等 live probe 才能做”的硬阻塞项，而是一个必须先落地的同步契约。
+
+### 能否在实现Step 3时增量确定字段覆盖？
+
+可以增量修正字段覆盖，但不应在入库同步命令里首次确定字段覆盖。
+
+合理边界是：
+
+- mapper / provider 测试阶段可以增量调整字段映射；
+- DB upsert 阶段不应再临时决定必填字段、默认值、缺失字段策略；
+- management command 阶段只负责执行已确认的同步计划，不应承载字段决策。
+
+---
+
+## 风险评估
+
+### 直接跳到Step 3/同步命令的主要风险
+
+1. **误写入风险**
+   - 如果 `number` 是否等同 `student_id` 未确认，可能把错误字段作为 `User.user_id` 主键。
+   - 主键一旦写错，后续修复会涉及用户、申请、审批、通知等关联数据。
+
+2. **权限链风险**
+   - 当前业务依赖 `class_id` 和 `ClassMapping` 做辅导员可见性控制。
+   - 学工API文档样例没有明确稳定的 `class_id` 字段；如果用院系/专业/班级名称临时拼接，可能导致辅导员看不到学生或看到错误班级。
+
+3. **毕业生范围风险**
+   - CSV 导入要求 `is_graduating` 和 `graduation_year`。
+   - 学工API样例字段未证明能提供这两个字段。若默认所有学生都是毕业生，会扩大系统范围；若默认否，会导致毕业生缺失。
+
+4. **角色识别风险**
+   - `user_identity` 可能能区分学生/老师，但值域未确认。
+   - 未定义值域映射前，直接入库可能把辅导员、学生或其他人员角色写错。
+
+5. **回滚成本风险**
+   - 只读 mapper 的错误可通过测试修正。
+   - 入库命令的错误需要数据清理、关联检查和审计摘要，成本更高。
+
+### 缺失字段覆盖文档会导致什么问题？
+
+最直接的问题是同步命令无法判断“成功”是什么意思。它只能证明 API 返回了用户列表，不能证明这些用户足以支撑本系统的毕业离校业务。
+
+尤其需要提前写清：
+
+- `number -> User.user_id` 是否成立；
+- `name -> User.name` 是否必填；
+- `user_identity -> User.role` 的值域；
+- `class_id` 从哪里来，学工API没有时是否继续依赖 CSV；
+- `is_graduating`、`graduation_year` 从哪里来，缺失时是否禁止入库；
+- API 缺失用户时是否停用本地用户，还是仅报告差异。
+
+---
+
+## 效率考量
+
+**最快达到可工作状态的方式不是直接写同步命令，而是先做一个短平快的字段契约。**
+
+推荐 Step 2C-lite 控制在一个小交付内：
+
+1. 创建字段覆盖表，不追求真实字段全集，只覆盖“同步写库必需字段”。
+2. 把字段分为四类：
+   - API可直接提供
+   - API可能提供但需 live probe 确认
+   - 必须由 CSV/手工配置提供
+   - 暂不支持或禁止默认推断
+3. 明确同步门槛：
+   - 没有 `number/name`：不可创建用户
+   - 没有 `class_id`：不可替代当前学生 CSV 主路径
+   - 没有 `is_graduating/graduation_year`：不可声明毕业生筛选可用
+   - 没有辅导员映射：不可自动创建 `ClassMapping`
+4. 产出 mapper 测试用例输入/输出样例。
+
+完成这个文档后，Step 3 的 mapper/provider 可以很快实现，而且测试目标明确。反过来，如果直接写 DB 同步命令，测试会被迫同时覆盖字段猜测、数据转换、幂等 upsert、事务和命令输出，反馈周期会变慢。
+
+---
+
+## 遗漏检查
+
+Step 2系列还有一个关键遗漏：**字段覆盖报告不能只列 API 字段，还必须列内部写库字段和缺失字段策略。**
+
+建议 Step 2C-lite 至少包含以下表：
+
+| 内部目标 | 来源字段 | 状态 | 处理规则 |
+| --- | --- | --- | --- |
+| `User.user_id` | `number` | 文档样例可用，需 live 确认 | 必填；缺失则跳过并报告 |
+| `User.name` | `name` | 文档样例可用，需 live 确认 | 必填；缺失则跳过并报告 |
+| `User.role` | `user_identity` | 值域未知 | 只接受明确学生值；未知值跳过并报告 |
+| `User.class_id` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `User.is_graduating` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `User.graduation_year` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `ClassMapping` | 未确认 | 缺失 | 不由学工用户API自动生成 |
+
+还建议补充两个基础设施决策，放入 Step 2C 或 Step 3：
+
+1. **API 与 CSV 并存策略**
+   - 在字段未完全覆盖前，API 只能补充或更新可确定字段，不能替代 CSV 导入。
+
+2. **缺失/停用策略**
+   - 初期不要因为 API 本次未返回某用户就自动停用本地用户；先输出差异报告，等 live 数据稳定后再决定停用规则。
+
+---
+
+## 推荐执行方案
+
+### 下一步：Step 2C-lite
+
+产出文件建议：
+
+`docs/phase4c-xg-field-coverage.md`
+
+内容建议：
+
+1. 学工API文档样例字段清单
+2. 内部 `User` / `ClassMapping` 写库字段清单
+3. 字段映射表
+4. 缺失字段处理规则
+5. API/CSV 并存策略
+6. Step 3 mapper 测试样例
+
+验收标准：
+
+- 能明确哪些字段允许 API 写入，哪些字段仍由 CSV/手工来源维护；
+- 能明确什么情况下跳过记录、报告错误、禁止同步；
+- 能为下一步 mapper/provider 测试提供固定输入输出。
+
+### 随后：Step 3
+
+实现范围建议收窄为：
+
+- 新增纯转换函数或 `UserInfoProvider`；
+- 输入为 `fetch_all_users()` 返回的用户列表；
+- 输出为内部标准化用户 DTO / dict；
+- 不写数据库；
+- 单元测试覆盖字段缺失、角色未知、班级缺失、毕业字段缺失等场景。
+
+### 再后：Step 4/5
+
+等 mapper 通过测试后再做：
+
+- 幂等 upsert；
+- dry-run 变更摘要；
+- 冲突报告；
+- 不自动停用本地缺失用户；
+- management command 入口。
+
+---
+
+## 替代方案
+
+如果团队非常希望马上看到可执行命令，可以采用折中方案：
+
+**创建 `sync_xg_users --dry-run`，但只做读取和映射报告，不写数据库。**
+
+这本质上仍然是 Step 2C-lite + Step 3 的组合，不是完整同步命令。它可以提高可见性，同时避免未确认字段导致误写库。
+
+---
+
+## 最终建议
+
+**不要跳过 Step 2C。**
+
+但 Step 2C 不应拖成大文档任务，而应作为一个短周期、可执行的字段映射契约。完成后进入只读 mapper/provider；再进入 DB upsert；最后再封装 management command。
+
+本轮推荐决策：
+
+**A-prime：Step 2C-lite 字段映射契约优先，禁止直接实现写库同步命令。**

diff --git a/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md b/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..b42293300cba0dfed225b660b8a7647b719805e2
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
@@ -0,0 +1,205 @@
+# Phase 4C 下一步优先级讨论 - Codex响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**针对：** `90-next-priority-discussion-request.md`  
+**文档编号：** 91
+
+---
+
+## 审查结论
+
+**推荐优先级：选择 A，但收窄为“Step 2C-lite 字段映射契约”，随后进入 Step 3 的只读 Provider/映射测试。**
+
+不建议直接执行选项 B 或 C 中的“学生数据同步命令并入库”。当前 `fetch_all_users()` 已经解决分页读取问题，但数据库写入不是下一个最低风险动作。下一步应先把学工字段、内部 `User` 字段、CSV补充字段、缺失字段处理规则固定下来。
+
+建议顺序：
+
+1. **Step 2C-lite：字段覆盖与映射契约**
+2. **Step 3：只读 mapper / `UserInfoProvider` 设计与测试**
+3. **Step 4：同步服务与幂等 upsert**
+4. **Step 5：management command 运维入口**
+
+这也与 doc 85 的阶段划分一致：doc 85 中 Step 3 是“字段映射与 Provider 设计”，Step 4 才是“同步服务与数据库写入”，Step 5 才是“管理命令或后台任务入口”。本次请求中的选项 B 实际上把 Step 3、Step 4、Step 5 合并了，风险偏高。
+
+---
+
+## 依赖关系分析
+
+### Step 3是否强依赖Step 2C？
+
+**强依赖，但不是依赖真实凭证；依赖的是字段映射决策。**
+
+没有真实凭证时，仍然可以基于以下材料完成 Step 2C-lite：
+
+- 学工文档样例字段：`name`、`number`、`phone`、`identity_id`、`department`、`user_identity`、`updated_at` 等
+- 当前内部 `User` 模型字段：`user_id`、`name`、`role`、`active`、`class_id`、`is_graduating`、`graduation_year`
+- 当前 CSV 导入命令的业务要求：学生导入要求 `student_id`、`name`、`class_id`、`is_graduating`、`graduation_year`
+- 现有 `ClassMapping` 约束：学生 `class_id` 需要能匹配辅导员映射
+
+因此 Step 2C 不是“等 live probe 才能做”的硬阻塞项，而是一个必须先落地的同步契约。
+
+### 能否在实现Step 3时增量确定字段覆盖？
+
+可以增量修正字段覆盖，但不应在入库同步命令里首次确定字段覆盖。
+
+合理边界是：
+
+- mapper / provider 测试阶段可以增量调整字段映射；
+- DB upsert 阶段不应再临时决定必填字段、默认值、缺失字段策略；
+- management command 阶段只负责执行已确认的同步计划，不应承载字段决策。
+
+---
+
+## 风险评估
+
+### 直接跳到Step 3/同步命令的主要风险
+
+1. **误写入风险**
+   - 如果 `number` 是否等同 `student_id` 未确认，可能把错误字段作为 `User.user_id` 主键。
+   - 主键一旦写错，后续修复会涉及用户、申请、审批、通知等关联数据。
+
+2. **权限链风险**
+   - 当前业务依赖 `class_id` 和 `ClassMapping` 做辅导员可见性控制。
+   - 学工API文档样例没有明确稳定的 `class_id` 字段；如果用院系/专业/班级名称临时拼接，可能导致辅导员看不到学生或看到错误班级。
+
+3. **毕业生范围风险**
+   - CSV 导入要求 `is_graduating` 和 `graduation_year`。
+   - 学工API样例字段未证明能提供这两个字段。若默认所有学生都是毕业生，会扩大系统范围；若默认否，会导致毕业生缺失。
+
+4. **角色识别风险**
+   - `user_identity` 可能能区分学生/老师，但值域未确认。
+   - 未定义值域映射前，直接入库可能把辅导员、学生或其他人员角色写错。
+
+5. **回滚成本风险**
+   - 只读 mapper 的错误可通过测试修正。
+   - 入库命令的错误需要数据清理、关联检查和审计摘要，成本更高。
+
+### 缺失字段覆盖文档会导致什么问题？
+
+最直接的问题是同步命令无法判断“成功”是什么意思。它只能证明 API 返回了用户列表，不能证明这些用户足以支撑本系统的毕业离校业务。
+
+尤其需要提前写清：
+
+- `number -> User.user_id` 是否成立；
+- `name -> User.name` 是否必填；
+- `user_identity -> User.role` 的值域；
+- `class_id` 从哪里来，学工API没有时是否继续依赖 CSV；
+- `is_graduating`、`graduation_year` 从哪里来，缺失时是否禁止入库；
+- API 缺失用户时是否停用本地用户，还是仅报告差异。
+
+---
+
+## 效率考量
+
+**最快达到可工作状态的方式不是直接写同步命令，而是先做一个短平快的字段契约。**
+
+推荐 Step 2C-lite 控制在一个小交付内：
+
+1. 创建字段覆盖表，不追求真实字段全集，只覆盖“同步写库必需字段”。
+2. 把字段分为四类：
+   - API可直接提供
+   - API可能提供但需 live probe 确认
+   - 必须由 CSV/手工配置提供
+   - 暂不支持或禁止默认推断
+3. 明确同步门槛：
+   - 没有 `number/name`：不可创建用户
+   - 没有 `class_id`：不可替代当前学生 CSV 主路径
+   - 没有 `is_graduating/graduation_year`：不可声明毕业生筛选可用
+   - 没有辅导员映射：不可自动创建 `ClassMapping`
+4. 产出 mapper 测试用例输入/输出样例。
+
+完成这个文档后，Step 3 的 mapper/provider 可以很快实现，而且测试目标明确。反过来，如果直接写 DB 同步命令，测试会被迫同时覆盖字段猜测、数据转换、幂等 upsert、事务和命令输出，反馈周期会变慢。
+
+---
+
+## 遗漏检查
+
+Step 2系列还有一个关键遗漏：**字段覆盖报告不能只列 API 字段，还必须列内部写库字段和缺失字段策略。**
+
+建议 Step 2C-lite 至少包含以下表：
+
+| 内部目标 | 来源字段 | 状态 | 处理规则 |
+| --- | --- | --- | --- |
+| `User.user_id` | `number` | 文档样例可用，需 live 确认 | 必填；缺失则跳过并报告 |
+| `User.name` | `name` | 文档样例可用，需 live 确认 | 必填；缺失则跳过并报告 |
+| `User.role` | `user_identity` | 值域未知 | 只接受明确学生值；未知值跳过并报告 |
+| `User.class_id` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `User.is_graduating` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `User.graduation_year` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `ClassMapping` | 未确认 | 缺失 | 不由学工用户API自动生成 |
+
+还建议补充两个基础设施决策，放入 Step 2C 或 Step 3：
+
+1. **API 与 CSV 并存策略**
+   - 在字段未完全覆盖前，API 只能补充或更新可确定字段，不能替代 CSV 导入。
+
+2. **缺失/停用策略**
+   - 初期不要因为 API 本次未返回某用户就自动停用本地用户；先输出差异报告，等 live 数据稳定后再决定停用规则。
+
+---
+
+## 推荐执行方案
+
+### 下一步：Step 2C-lite
+
+产出文件建议：
+
+`docs/phase4c-xg-field-coverage.md`
+
+内容建议：
+
+1. 学工API文档样例字段清单
+2. 内部 `User` / `ClassMapping` 写库字段清单
+3. 字段映射表
+4. 缺失字段处理规则
+5. API/CSV 并存策略
+6. Step 3 mapper 测试样例
+
+验收标准：
+
+- 能明确哪些字段允许 API 写入，哪些字段仍由 CSV/手工来源维护；
+- 能明确什么情况下跳过记录、报告错误、禁止同步；
+- 能为下一步 mapper/provider 测试提供固定输入输出。
+
+### 随后：Step 3
+
+实现范围建议收窄为：
+
+- 新增纯转换函数或 `UserInfoProvider`；
+- 输入为 `fetch_all_users()` 返回的用户列表；
+- 输出为内部标准化用户 DTO / dict；
+- 不写数据库；
+- 单元测试覆盖字段缺失、角色未知、班级缺失、毕业字段缺失等场景。
+
+### 再后：Step 4/5
+
+等 mapper 通过测试后再做：
+
+- 幂等 upsert；
+- dry-run 变更摘要；
+- 冲突报告；
+- 不自动停用本地缺失用户；
+- management command 入口。
+
+---
+
+## 替代方案
+
+如果团队非常希望马上看到可执行命令，可以采用折中方案：
+
+**创建 `sync_xg_users --dry-run`，但只做读取和映射报告，不写数据库。**
+
+这本质上仍然是 Step 2C-lite + Step 3 的组合，不是完整同步命令。它可以提高可见性，同时避免未确认字段导致误写库。
+
+---
+
+## 最终建议
+
+**不要跳过 Step 2C。**
+
+但 Step 2C 不应拖成大文档任务，而应作为一个短周期、可执行的字段映射契约。完成后进入只读 mapper/provider；再进入 DB upsert；最后再封装 management command。
+
+本轮推荐决策：
+
+**A-prime：Step 2C-lite 字段映射契约优先，禁止直接实现写库同步命令。**

codex
The response document is in place. I’m checking the collaboration state briefly so I don’t miss a required handoff/event record for this review artifact.
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
 M backend/apps/users/integrations/xg_user_client.py
 M backend/apps/users/tests/test_xg_user_client.py
 M backend/scripts/diagnose_xg_api.py
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
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-80-step1a-completion-nex-2026-06-02T03-27-49-873Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-84-post-step1-next-strat-2026-06-02T03-46-46-328Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-87-step2b-implementation-2026-06-02T03-59-39-871Z.md
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
?? docs/discussions/phase4c-next-steps/82-claude-response-agree-step1b-lite-first.md
?? docs/discussions/phase4c-next-steps/83-consensus-step1b-lite-first.md
?? docs/discussions/phase4c-next-steps/84-post-step1-next-strategy-request.md
?? docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md
?? docs/discussions/phase4c-next-steps/86-claude-response-agree-step2-strategy.md
?? docs/discussions/phase4c-next-steps/87-step2b-implementation-review-request.md
?? docs/discussions/phase4c-next-steps/88-step2b-implementation-codex-response.md
?? docs/discussions/phase4c-next-steps/89-claude-response-agree-fixes.md
?? docs/discussions/phase4c-next-steps/90-next-priority-discussion-request.md
?? docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
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
/bin/bash -lc "rtk sed -n '1,220p' .omc/collaboration/state.json" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{
  "workflow_id": "claude-codex-collab-mvp",
  "current_task": "phase4c_next_steps",
  "active_agent": "claude",
  "status": "waiting_for_claude_response",
  "last_event_id": 101,
  "updated_at": "2026-06-02T03:46:24.955536Z"
}

exec
/bin/bash -lc 'rtk tail -n 20 .omc/collaboration/events.jsonl' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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
{"id":100,"type":"review_response","agent":"codex","timestamp":"2026-06-02T03:26:08.406715Z","summary":"Codex reviewed Step 1A signature implementation and recommended Step 1B-lite before diagnostic script.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md"],"status":"waiting_for_claude_response","details":{"decision":"step1a_passes_signature_slice_with_p1_test_improvement","recommended_next":["fix_md5_expected_value_test","step1b_lite_request_build_mock_tests","step1c_probe_reusing_client"],"verification":"4/4 xg_user_client tests passed in Docker with --keepdb --noinput"}}
{"id":101,"type":"review_response","agent":"codex","timestamp":"2026-06-02T03:46:24.955536Z","summary":"Codex reviewed post-Step 1 Phase 4C strategy and approved conditional live probe plus pagination-first Step 2, deferring Provider/DB writes.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md"],"status":"waiting_for_claude_response","details":{"decision":"approve_A_plus_B_with_live_nonblocking","recommended_next":["conditional_page1_live_probe","fetch_all_users_pagination_with_mock_tests","field_coverage_before_provider"],"defer":["provider_integration","database_write","csv_replacement","retry_and_resume"],"key_risks":["pageNum_is_page_size","per_page_string_type","tenant_invalid_classification_missing","field_coverage_may_not_replace_csv"]}}

diff --git a/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md b/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..b42293300cba0dfed225b660b8a7647b719805e2
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
@@ -0,0 +1,205 @@
+# Phase 4C 下一步优先级讨论 - Codex响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**针对：** `90-next-priority-discussion-request.md`  
+**文档编号：** 91
+
+---
+
+## 审查结论
+
+**推荐优先级：选择 A，但收窄为“Step 2C-lite 字段映射契约”，随后进入 Step 3 的只读 Provider/映射测试。**
+
+不建议直接执行选项 B 或 C 中的“学生数据同步命令并入库”。当前 `fetch_all_users()` 已经解决分页读取问题，但数据库写入不是下一个最低风险动作。下一步应先把学工字段、内部 `User` 字段、CSV补充字段、缺失字段处理规则固定下来。
+
+建议顺序：
+
+1. **Step 2C-lite：字段覆盖与映射契约**
+2. **Step 3：只读 mapper / `UserInfoProvider` 设计与测试**
+3. **Step 4：同步服务与幂等 upsert**
+4. **Step 5：management command 运维入口**
+
+这也与 doc 85 的阶段划分一致：doc 85 中 Step 3 是“字段映射与 Provider 设计”，Step 4 才是“同步服务与数据库写入”，Step 5 才是“管理命令或后台任务入口”。本次请求中的选项 B 实际上把 Step 3、Step 4、Step 5 合并了，风险偏高。
+
+---
+
+## 依赖关系分析
+
+### Step 3是否强依赖Step 2C？
+
+**强依赖，但不是依赖真实凭证；依赖的是字段映射决策。**
+
+没有真实凭证时，仍然可以基于以下材料完成 Step 2C-lite：
+
+- 学工文档样例字段：`name`、`number`、`phone`、`identity_id`、`department`、`user_identity`、`updated_at` 等
+- 当前内部 `User` 模型字段：`user_id`、`name`、`role`、`active`、`class_id`、`is_graduating`、`graduation_year`
+- 当前 CSV 导入命令的业务要求：学生导入要求 `student_id`、`name`、`class_id`、`is_graduating`、`graduation_year`
+- 现有 `ClassMapping` 约束：学生 `class_id` 需要能匹配辅导员映射
+
+因此 Step 2C 不是“等 live probe 才能做”的硬阻塞项，而是一个必须先落地的同步契约。
+
+### 能否在实现Step 3时增量确定字段覆盖？
+
+可以增量修正字段覆盖，但不应在入库同步命令里首次确定字段覆盖。
+
+合理边界是：
+
+- mapper / provider 测试阶段可以增量调整字段映射；
+- DB upsert 阶段不应再临时决定必填字段、默认值、缺失字段策略；
+- management command 阶段只负责执行已确认的同步计划，不应承载字段决策。
+
+---
+
+## 风险评估
+
+### 直接跳到Step 3/同步命令的主要风险
+
+1. **误写入风险**
+   - 如果 `number` 是否等同 `student_id` 未确认，可能把错误字段作为 `User.user_id` 主键。
+   - 主键一旦写错，后续修复会涉及用户、申请、审批、通知等关联数据。
+
+2. **权限链风险**
+   - 当前业务依赖 `class_id` 和 `ClassMapping` 做辅导员可见性控制。
+   - 学工API文档样例没有明确稳定的 `class_id` 字段；如果用院系/专业/班级名称临时拼接，可能导致辅导员看不到学生或看到错误班级。
+
+3. **毕业生范围风险**
+   - CSV 导入要求 `is_graduating` 和 `graduation_year`。
+   - 学工API样例字段未证明能提供这两个字段。若默认所有学生都是毕业生，会扩大系统范围；若默认否，会导致毕业生缺失。
+
+4. **角色识别风险**
+   - `user_identity` 可能能区分学生/老师，但值域未确认。
+   - 未定义值域映射前，直接入库可能把辅导员、学生或其他人员角色写错。
+
+5. **回滚成本风险**
+   - 只读 mapper 的错误可通过测试修正。
+   - 入库命令的错误需要数据清理、关联检查和审计摘要，成本更高。
+
+### 缺失字段覆盖文档会导致什么问题？
+
+最直接的问题是同步命令无法判断“成功”是什么意思。它只能证明 API 返回了用户列表，不能证明这些用户足以支撑本系统的毕业离校业务。
+
+尤其需要提前写清：
+
+- `number -> User.user_id` 是否成立；
+- `name -> User.name` 是否必填；
+- `user_identity -> User.role` 的值域；
+- `class_id` 从哪里来，学工API没有时是否继续依赖 CSV；
+- `is_graduating`、`graduation_year` 从哪里来，缺失时是否禁止入库；
+- API 缺失用户时是否停用本地用户，还是仅报告差异。
+
+---
+
+## 效率考量
+
+**最快达到可工作状态的方式不是直接写同步命令，而是先做一个短平快的字段契约。**
+
+推荐 Step 2C-lite 控制在一个小交付内：
+
+1. 创建字段覆盖表，不追求真实字段全集，只覆盖“同步写库必需字段”。
+2. 把字段分为四类：
+   - API可直接提供
+   - API可能提供但需 live probe 确认
+   - 必须由 CSV/手工配置提供
+   - 暂不支持或禁止默认推断
+3. 明确同步门槛：
+   - 没有 `number/name`：不可创建用户
+   - 没有 `class_id`：不可替代当前学生 CSV 主路径
+   - 没有 `is_graduating/graduation_year`：不可声明毕业生筛选可用
+   - 没有辅导员映射：不可自动创建 `ClassMapping`
+4. 产出 mapper 测试用例输入/输出样例。
+
+完成这个文档后，Step 3 的 mapper/provider 可以很快实现，而且测试目标明确。反过来，如果直接写 DB 同步命令，测试会被迫同时覆盖字段猜测、数据转换、幂等 upsert、事务和命令输出，反馈周期会变慢。
+
+---
+
+## 遗漏检查
+
+Step 2系列还有一个关键遗漏：**字段覆盖报告不能只列 API 字段，还必须列内部写库字段和缺失字段策略。**
+
+建议 Step 2C-lite 至少包含以下表：
+
+| 内部目标 | 来源字段 | 状态 | 处理规则 |
+| --- | --- | --- | --- |
+| `User.user_id` | `number` | 文档样例可用，需 live 确认 | 必填；缺失则跳过并报告 |
+| `User.name` | `name` | 文档样例可用，需 live 确认 | 必填；缺失则跳过并报告 |
+| `User.role` | `user_identity` | 值域未知 | 只接受明确学生值；未知值跳过并报告 |
+| `User.class_id` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `User.is_graduating` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `User.graduation_year` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `ClassMapping` | 未确认 | 缺失 | 不由学工用户API自动生成 |
+
+还建议补充两个基础设施决策，放入 Step 2C 或 Step 3：
+
+1. **API 与 CSV 并存策略**
+   - 在字段未完全覆盖前，API 只能补充或更新可确定字段，不能替代 CSV 导入。
+
+2. **缺失/停用策略**
+   - 初期不要因为 API 本次未返回某用户就自动停用本地用户；先输出差异报告，等 live 数据稳定后再决定停用规则。
+
+---
+
+## 推荐执行方案
+
+### 下一步：Step 2C-lite
+
+产出文件建议：
+
+`docs/phase4c-xg-field-coverage.md`
+
+内容建议：
+
+1. 学工API文档样例字段清单
+2. 内部 `User` / `ClassMapping` 写库字段清单
+3. 字段映射表
+4. 缺失字段处理规则
+5. API/CSV 并存策略
+6. Step 3 mapper 测试样例
+
+验收标准：
+
+- 能明确哪些字段允许 API 写入，哪些字段仍由 CSV/手工来源维护；
+- 能明确什么情况下跳过记录、报告错误、禁止同步；
+- 能为下一步 mapper/provider 测试提供固定输入输出。
+
+### 随后：Step 3
+
+实现范围建议收窄为：
+
+- 新增纯转换函数或 `UserInfoProvider`；
+- 输入为 `fetch_all_users()` 返回的用户列表；
+- 输出为内部标准化用户 DTO / dict；
+- 不写数据库；
+- 单元测试覆盖字段缺失、角色未知、班级缺失、毕业字段缺失等场景。
+
+### 再后：Step 4/5
+
+等 mapper 通过测试后再做：
+
+- 幂等 upsert；
+- dry-run 变更摘要；
+- 冲突报告；
+- 不自动停用本地缺失用户；
+- management command 入口。
+
+---
+
+## 替代方案
+
+如果团队非常希望马上看到可执行命令，可以采用折中方案：
+
+**创建 `sync_xg_users --dry-run`，但只做读取和映射报告，不写数据库。**
+
+这本质上仍然是 Step 2C-lite + Step 3 的组合，不是完整同步命令。它可以提高可见性，同时避免未确认字段导致误写库。
+
+---
+
+## 最终建议
+
+**不要跳过 Step 2C。**
+
+但 Step 2C 不应拖成大文档任务，而应作为一个短周期、可执行的字段映射契约。完成后进入只读 mapper/provider；再进入 DB upsert；最后再封装 management command。
+
+本轮推荐决策：
+
+**A-prime：Step 2C-lite 字段映射契约优先，禁止直接实现写库同步命令。**

codex
The collaboration state is active and waiting for Claude, so I’m appending a review-response event and updating `state.json` under the required journal lock.
exec
/bin/bash -lc "rtk bash -lc 'set -euo pipefail
lock=.omc/collaboration/locks/journal.lock
mkdir \""'$lock"
cleanup() { rm -rf "$lock"; }
trap cleanup EXIT
python3 - <<'"'\"'\"'PY'\"'\"'
import json
from datetime import datetime, timezone
from pathlib import Path

lock = Path(\".omc/collaboration/locks/journal.lock\")
events_path = Path(\".omc/collaboration/events.jsonl\")
state_path = Path(\".omc/collaboration/state.json\")

now = datetime.now(timezone.utc).isoformat().replace(\"+00:00\", \"Z\")
(lock / \"owner.json\").write_text(json.dumps({
    \"agent\": \"codex\",
    \"task_id\": \"phase4c_next_steps\",
    \"created_at\": now,
    \"heartbeat_at\": now,
    \"reason\": \"append Codex review response event and update state\"
}, ensure_ascii=False, indent=2), encoding=\"utf-8\")

max_id = 0
with events_path.open(\"r\", encoding=\"utf-8\") as f:
    for line_no, line in enumerate(f, start=1):
        if not line.strip():
            continue
        event = json.loads(line)
        event_id = event.get(\"id\", event.get(\"event_id\"))
        if isinstance(event_id, int) and event_id > max_id:
            max_id = event_id

next_id = max_id + 1
event = {
    \"id\": next_id,
    \"type\": \"review_response\",
    \"agent\": \"codex\",
    \"timestamp\": now,
    \"summary\": \"Codex reviewed Phase 4C next priority and recommended Step 2C-lite field mapping before read-only Provider and DB sync.\",
    \"task_id\": \"phase4c_next_steps\",
    \"artifacts\": [\"docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md\"],
    \"status\": \"waiting_for_claude_response\",
    \"details\": {
        \"decision\": \"step2c_lite_before_provider_or_db_sync\",
        \"recommended_next\": [
            \"field_coverage_mapping_contract\",
            \"readonly_mapper_provider_tests\",
            \"idempotent_upsert_service\",
            \"management_command_entry\"
        ],
        \"defer\": [\"database_write\", \"csv_replacement\", \"automatic_deactivation\"]
    }
}

with events_path.open(\"a\", encoding=\"utf-8\") as f:
    f.write(json.dumps(event, ensure_ascii=False, separators=(\",\", \":\")) + \"\\n\")

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

# Validate appended event and state after write.
seen_max = 0
with events_path.open(\"r\", encoding=\"utf-8\") as f:
    for line in f:
        if line.strip():
            e = json.loads(line)
            eid = e.get(\"id\", e.get(\"event_id\"))
            if isinstance(eid, int):
                seen_max = max(seen_max, eid)
new_state = json.loads(state_path.read_text(encoding=\"utf-8\"))
assert new_state[\"last_event_id\"] == seen_max == next_id
print(f\"appended event {next_id}\")
PY'" in /home/caohui/projects/graduation-leave-system
 succeeded in 129ms:
appended event 102

diff --git a/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md b/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..b42293300cba0dfed225b660b8a7647b719805e2
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
@@ -0,0 +1,205 @@
+# Phase 4C 下一步优先级讨论 - Codex响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**针对：** `90-next-priority-discussion-request.md`  
+**文档编号：** 91
+
+---
+
+## 审查结论
+
+**推荐优先级：选择 A，但收窄为“Step 2C-lite 字段映射契约”，随后进入 Step 3 的只读 Provider/映射测试。**
+
+不建议直接执行选项 B 或 C 中的“学生数据同步命令并入库”。当前 `fetch_all_users()` 已经解决分页读取问题，但数据库写入不是下一个最低风险动作。下一步应先把学工字段、内部 `User` 字段、CSV补充字段、缺失字段处理规则固定下来。
+
+建议顺序：
+
+1. **Step 2C-lite：字段覆盖与映射契约**
+2. **Step 3：只读 mapper / `UserInfoProvider` 设计与测试**
+3. **Step 4：同步服务与幂等 upsert**
+4. **Step 5：management command 运维入口**
+
+这也与 doc 85 的阶段划分一致：doc 85 中 Step 3 是“字段映射与 Provider 设计”，Step 4 才是“同步服务与数据库写入”，Step 5 才是“管理命令或后台任务入口”。本次请求中的选项 B 实际上把 Step 3、Step 4、Step 5 合并了，风险偏高。
+
+---
+
+## 依赖关系分析
+
+### Step 3是否强依赖Step 2C？
+
+**强依赖，但不是依赖真实凭证；依赖的是字段映射决策。**
+
+没有真实凭证时，仍然可以基于以下材料完成 Step 2C-lite：
+
+- 学工文档样例字段：`name`、`number`、`phone`、`identity_id`、`department`、`user_identity`、`updated_at` 等
+- 当前内部 `User` 模型字段：`user_id`、`name`、`role`、`active`、`class_id`、`is_graduating`、`graduation_year`
+- 当前 CSV 导入命令的业务要求：学生导入要求 `student_id`、`name`、`class_id`、`is_graduating`、`graduation_year`
+- 现有 `ClassMapping` 约束：学生 `class_id` 需要能匹配辅导员映射
+
+因此 Step 2C 不是“等 live probe 才能做”的硬阻塞项，而是一个必须先落地的同步契约。
+
+### 能否在实现Step 3时增量确定字段覆盖？
+
+可以增量修正字段覆盖，但不应在入库同步命令里首次确定字段覆盖。
+
+合理边界是：
+
+- mapper / provider 测试阶段可以增量调整字段映射；
+- DB upsert 阶段不应再临时决定必填字段、默认值、缺失字段策略；
+- management command 阶段只负责执行已确认的同步计划，不应承载字段决策。
+
+---
+
+## 风险评估
+
+### 直接跳到Step 3/同步命令的主要风险
+
+1. **误写入风险**
+   - 如果 `number` 是否等同 `student_id` 未确认，可能把错误字段作为 `User.user_id` 主键。
+   - 主键一旦写错，后续修复会涉及用户、申请、审批、通知等关联数据。
+
+2. **权限链风险**
+   - 当前业务依赖 `class_id` 和 `ClassMapping` 做辅导员可见性控制。
+   - 学工API文档样例没有明确稳定的 `class_id` 字段；如果用院系/专业/班级名称临时拼接，可能导致辅导员看不到学生或看到错误班级。
+
+3. **毕业生范围风险**
+   - CSV 导入要求 `is_graduating` 和 `graduation_year`。
+   - 学工API样例字段未证明能提供这两个字段。若默认所有学生都是毕业生，会扩大系统范围；若默认否，会导致毕业生缺失。
+
+4. **角色识别风险**
+   - `user_identity` 可能能区分学生/老师，但值域未确认。
+   - 未定义值域映射前，直接入库可能把辅导员、学生或其他人员角色写错。
+
+5. **回滚成本风险**
+   - 只读 mapper 的错误可通过测试修正。
+   - 入库命令的错误需要数据清理、关联检查和审计摘要，成本更高。
+
+### 缺失字段覆盖文档会导致什么问题？
+
+最直接的问题是同步命令无法判断“成功”是什么意思。它只能证明 API 返回了用户列表，不能证明这些用户足以支撑本系统的毕业离校业务。
+
+尤其需要提前写清：
+
+- `number -> User.user_id` 是否成立；
+- `name -> User.name` 是否必填；
+- `user_identity -> User.role` 的值域；
+- `class_id` 从哪里来，学工API没有时是否继续依赖 CSV；
+- `is_graduating`、`graduation_year` 从哪里来，缺失时是否禁止入库；
+- API 缺失用户时是否停用本地用户，还是仅报告差异。
+
+---
+
+## 效率考量
+
+**最快达到可工作状态的方式不是直接写同步命令，而是先做一个短平快的字段契约。**
+
+推荐 Step 2C-lite 控制在一个小交付内：
+
+1. 创建字段覆盖表，不追求真实字段全集，只覆盖“同步写库必需字段”。
+2. 把字段分为四类：
+   - API可直接提供
+   - API可能提供但需 live probe 确认
+   - 必须由 CSV/手工配置提供
+   - 暂不支持或禁止默认推断
+3. 明确同步门槛：
+   - 没有 `number/name`：不可创建用户
+   - 没有 `class_id`：不可替代当前学生 CSV 主路径
+   - 没有 `is_graduating/graduation_year`：不可声明毕业生筛选可用
+   - 没有辅导员映射：不可自动创建 `ClassMapping`
+4. 产出 mapper 测试用例输入/输出样例。
+
+完成这个文档后，Step 3 的 mapper/provider 可以很快实现，而且测试目标明确。反过来，如果直接写 DB 同步命令，测试会被迫同时覆盖字段猜测、数据转换、幂等 upsert、事务和命令输出，反馈周期会变慢。
+
+---
+
+## 遗漏检查
+
+Step 2系列还有一个关键遗漏：**字段覆盖报告不能只列 API 字段，还必须列内部写库字段和缺失字段策略。**
+
+建议 Step 2C-lite 至少包含以下表：
+
+| 内部目标 | 来源字段 | 状态 | 处理规则 |
+| --- | --- | --- | --- |
+| `User.user_id` | `number` | 文档样例可用，需 live 确认 | 必填；缺失则跳过并报告 |
+| `User.name` | `name` | 文档样例可用，需 live 确认 | 必填；缺失则跳过并报告 |
+| `User.role` | `user_identity` | 值域未知 | 只接受明确学生值；未知值跳过并报告 |
+| `User.class_id` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `User.is_graduating` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `User.graduation_year` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `ClassMapping` | 未确认 | 缺失 | 不由学工用户API自动生成 |
+
+还建议补充两个基础设施决策，放入 Step 2C 或 Step 3：
+
+1. **API 与 CSV 并存策略**
+   - 在字段未完全覆盖前，API 只能补充或更新可确定字段，不能替代 CSV 导入。
+
+2. **缺失/停用策略**
+   - 初期不要因为 API 本次未返回某用户就自动停用本地用户；先输出差异报告，等 live 数据稳定后再决定停用规则。
+
+---
+
+## 推荐执行方案
+
+### 下一步：Step 2C-lite
+
+产出文件建议：
+
+`docs/phase4c-xg-field-coverage.md`
+
+内容建议：
+
+1. 学工API文档样例字段清单
+2. 内部 `User` / `ClassMapping` 写库字段清单
+3. 字段映射表
+4. 缺失字段处理规则
+5. API/CSV 并存策略
+6. Step 3 mapper 测试样例
+
+验收标准：
+
+- 能明确哪些字段允许 API 写入，哪些字段仍由 CSV/手工来源维护；
+- 能明确什么情况下跳过记录、报告错误、禁止同步；
+- 能为下一步 mapper/provider 测试提供固定输入输出。
+
+### 随后：Step 3
+
+实现范围建议收窄为：
+
+- 新增纯转换函数或 `UserInfoProvider`；
+- 输入为 `fetch_all_users()` 返回的用户列表；
+- 输出为内部标准化用户 DTO / dict；
+- 不写数据库；
+- 单元测试覆盖字段缺失、角色未知、班级缺失、毕业字段缺失等场景。
+
+### 再后：Step 4/5
+
+等 mapper 通过测试后再做：
+
+- 幂等 upsert；
+- dry-run 变更摘要；
+- 冲突报告；
+- 不自动停用本地缺失用户；
+- management command 入口。
+
+---
+
+## 替代方案
+
+如果团队非常希望马上看到可执行命令，可以采用折中方案：
+
+**创建 `sync_xg_users --dry-run`，但只做读取和映射报告，不写数据库。**
+
+这本质上仍然是 Step 2C-lite + Step 3 的组合，不是完整同步命令。它可以提高可见性，同时避免未确认字段导致误写库。
+
+---
+
+## 最终建议
+
+**不要跳过 Step 2C。**
+
+但 Step 2C 不应拖成大文档任务，而应作为一个短周期、可执行的字段映射契约。完成后进入只读 mapper/provider；再进入 DB upsert；最后再封装 management command。
+
+本轮推荐决策：
+
+**A-prime：Step 2C-lite 字段映射契约优先，禁止直接实现写库同步命令。**

codex
The collaboration event is recorded as event 102. I’m doing one last read of the new response file and status so the final note can point to the exact artifact and avoid implying tests were rerun.
exec
/bin/bash -lc 'rtk git status --short docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md .omc/collaboration/events.jsonl .omc/collaboration/state.json' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
 M .omc/collaboration/events.jsonl
 M .omc/collaboration/state.json
?? docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
exec
/bin/bash -lc "rtk sed -n '1,80p' docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Phase 4C 下一步优先级讨论 - Codex响应

**审查日期：** 2026-06-02  
**审查人：** Codex  
**针对：** `90-next-priority-discussion-request.md`  
**文档编号：** 91

---

## 审查结论

**推荐优先级：选择 A，但收窄为“Step 2C-lite 字段映射契约”，随后进入 Step 3 的只读 Provider/映射测试。**

不建议直接执行选项 B 或 C 中的“学生数据同步命令并入库”。当前 `fetch_all_users()` 已经解决分页读取问题，但数据库写入不是下一个最低风险动作。下一步应先把学工字段、内部 `User` 字段、CSV补充字段、缺失字段处理规则固定下来。

建议顺序：

1. **Step 2C-lite：字段覆盖与映射契约**
2. **Step 3：只读 mapper / `UserInfoProvider` 设计与测试**
3. **Step 4：同步服务与幂等 upsert**
4. **Step 5：management command 运维入口**

这也与 doc 85 的阶段划分一致：doc 85 中 Step 3 是“字段映射与 Provider 设计”，Step 4 才是“同步服务与数据库写入”，Step 5 才是“管理命令或后台任务入口”。本次请求中的选项 B 实际上把 Step 3、Step 4、Step 5 合并了，风险偏高。

---

## 依赖关系分析

### Step 3是否强依赖Step 2C？

**强依赖，但不是依赖真实凭证；依赖的是字段映射决策。**

没有真实凭证时，仍然可以基于以下材料完成 Step 2C-lite：

- 学工文档样例字段：`name`、`number`、`phone`、`identity_id`、`department`、`user_identity`、`updated_at` 等
- 当前内部 `User` 模型字段：`user_id`、`name`、`role`、`active`、`class_id`、`is_graduating`、`graduation_year`
- 当前 CSV 导入命令的业务要求：学生导入要求 `student_id`、`name`、`class_id`、`is_graduating`、`graduation_year`
- 现有 `ClassMapping` 约束：学生 `class_id` 需要能匹配辅导员映射

因此 Step 2C 不是“等 live probe 才能做”的硬阻塞项，而是一个必须先落地的同步契约。

### 能否在实现Step 3时增量确定字段覆盖？

可以增量修正字段覆盖，但不应在入库同步命令里首次确定字段覆盖。

合理边界是：

- mapper / provider 测试阶段可以增量调整字段映射；
- DB upsert 阶段不应再临时决定必填字段、默认值、缺失字段策略；
- management command 阶段只负责执行已确认的同步计划，不应承载字段决策。

---

## 风险评估

### 直接跳到Step 3/同步命令的主要风险

1. **误写入风险**
   - 如果 `number` 是否等同 `student_id` 未确认，可能把错误字段作为 `User.user_id` 主键。
   - 主键一旦写错，后续修复会涉及用户、申请、审批、通知等关联数据。

2. **权限链风险**
   - 当前业务依赖 `class_id` 和 `ClassMapping` 做辅导员可见性控制。
   - 学工API文档样例没有明确稳定的 `class_id` 字段；如果用院系/专业/班级名称临时拼接，可能导致辅导员看不到学生或看到错误班级。

3. **毕业生范围风险**
   - CSV 导入要求 `is_graduating` 和 `graduation_year`。
   - 学工API样例字段未证明能提供这两个字段。若默认所有学生都是毕业生，会扩大系统范围；若默认否，会导致毕业生缺失。

4. **角色识别风险**
   - `user_identity` 可能能区分学生/老师，但值域未确认。
   - 未定义值域映射前，直接入库可能把辅导员、学生或其他人员角色写错。

5. **回滚成本风险**
   - 只读 mapper 的错误可通过测试修正。
   - 入库命令的错误需要数据清理、关联检查和审计摘要，成本更高。

### 缺失字段覆盖文档会导致什么问题？

最直接的问题是同步命令无法判断“成功”是什么意思。它只能证明 API 返回了用户列表，不能证明这些用户足以支撑本系统的毕业离校业务。

exec
/bin/bash -lc 'rtk tail -n 3 .omc/collaboration/events.jsonl' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{"id":100,"type":"review_response","agent":"codex","timestamp":"2026-06-02T03:26:08.406715Z","summary":"Codex reviewed Step 1A signature implementation and recommended Step 1B-lite before diagnostic script.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/81-step1a-completion-codex-response.md"],"status":"waiting_for_claude_response","details":{"decision":"step1a_passes_signature_slice_with_p1_test_improvement","recommended_next":["fix_md5_expected_value_test","step1b_lite_request_build_mock_tests","step1c_probe_reusing_client"],"verification":"4/4 xg_user_client tests passed in Docker with --keepdb --noinput"}}
{"id":101,"type":"review_response","agent":"codex","timestamp":"2026-06-02T03:46:24.955536Z","summary":"Codex reviewed post-Step 1 Phase 4C strategy and approved conditional live probe plus pagination-first Step 2, deferring Provider/DB writes.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/85-post-step1-next-strategy-codex-response.md"],"status":"waiting_for_claude_response","details":{"decision":"approve_A_plus_B_with_live_nonblocking","recommended_next":["conditional_page1_live_probe","fetch_all_users_pagination_with_mock_tests","field_coverage_before_provider"],"defer":["provider_integration","database_write","csv_replacement","retry_and_resume"],"key_risks":["pageNum_is_page_size","per_page_string_type","tenant_invalid_classification_missing","field_coverage_may_not_replace_csv"]}}
{"id":102,"type":"review_response","agent":"codex","timestamp":"2026-06-02T06:15:46.167218Z","summary":"Codex reviewed Phase 4C next priority and recommended Step 2C-lite field mapping before read-only Provider and DB sync.","task_id":"phase4c_next_steps","artifacts":["docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md"],"status":"waiting_for_claude_response","details":{"decision":"step2c_lite_before_provider_or_db_sync","recommended_next":["field_coverage_mapping_contract","readonly_mapper_provider_tests","idempotent_upsert_service","management_command_entry"],"defer":["database_write","csv_replacement","automatic_deactivation"]}}

diff --git a/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md b/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..b42293300cba0dfed225b660b8a7647b719805e2
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
@@ -0,0 +1,205 @@
+# Phase 4C 下一步优先级讨论 - Codex响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**针对：** `90-next-priority-discussion-request.md`  
+**文档编号：** 91
+
+---
+
+## 审查结论
+
+**推荐优先级：选择 A，但收窄为“Step 2C-lite 字段映射契约”，随后进入 Step 3 的只读 Provider/映射测试。**
+
+不建议直接执行选项 B 或 C 中的“学生数据同步命令并入库”。当前 `fetch_all_users()` 已经解决分页读取问题，但数据库写入不是下一个最低风险动作。下一步应先把学工字段、内部 `User` 字段、CSV补充字段、缺失字段处理规则固定下来。
+
+建议顺序：
+
+1. **Step 2C-lite：字段覆盖与映射契约**
+2. **Step 3：只读 mapper / `UserInfoProvider` 设计与测试**
+3. **Step 4：同步服务与幂等 upsert**
+4. **Step 5：management command 运维入口**
+
+这也与 doc 85 的阶段划分一致：doc 85 中 Step 3 是“字段映射与 Provider 设计”，Step 4 才是“同步服务与数据库写入”，Step 5 才是“管理命令或后台任务入口”。本次请求中的选项 B 实际上把 Step 3、Step 4、Step 5 合并了，风险偏高。
+
+---
+
+## 依赖关系分析
+
+### Step 3是否强依赖Step 2C？
+
+**强依赖，但不是依赖真实凭证；依赖的是字段映射决策。**
+
+没有真实凭证时，仍然可以基于以下材料完成 Step 2C-lite：
+
+- 学工文档样例字段：`name`、`number`、`phone`、`identity_id`、`department`、`user_identity`、`updated_at` 等
+- 当前内部 `User` 模型字段：`user_id`、`name`、`role`、`active`、`class_id`、`is_graduating`、`graduation_year`
+- 当前 CSV 导入命令的业务要求：学生导入要求 `student_id`、`name`、`class_id`、`is_graduating`、`graduation_year`
+- 现有 `ClassMapping` 约束：学生 `class_id` 需要能匹配辅导员映射
+
+因此 Step 2C 不是“等 live probe 才能做”的硬阻塞项，而是一个必须先落地的同步契约。
+
+### 能否在实现Step 3时增量确定字段覆盖？
+
+可以增量修正字段覆盖，但不应在入库同步命令里首次确定字段覆盖。
+
+合理边界是：
+
+- mapper / provider 测试阶段可以增量调整字段映射；
+- DB upsert 阶段不应再临时决定必填字段、默认值、缺失字段策略；
+- management command 阶段只负责执行已确认的同步计划，不应承载字段决策。
+
+---
+
+## 风险评估
+
+### 直接跳到Step 3/同步命令的主要风险
+
+1. **误写入风险**
+   - 如果 `number` 是否等同 `student_id` 未确认，可能把错误字段作为 `User.user_id` 主键。
+   - 主键一旦写错，后续修复会涉及用户、申请、审批、通知等关联数据。
+
+2. **权限链风险**
+   - 当前业务依赖 `class_id` 和 `ClassMapping` 做辅导员可见性控制。
+   - 学工API文档样例没有明确稳定的 `class_id` 字段；如果用院系/专业/班级名称临时拼接，可能导致辅导员看不到学生或看到错误班级。
+
+3. **毕业生范围风险**
+   - CSV 导入要求 `is_graduating` 和 `graduation_year`。
+   - 学工API样例字段未证明能提供这两个字段。若默认所有学生都是毕业生，会扩大系统范围；若默认否，会导致毕业生缺失。
+
+4. **角色识别风险**
+   - `user_identity` 可能能区分学生/老师，但值域未确认。
+   - 未定义值域映射前，直接入库可能把辅导员、学生或其他人员角色写错。
+
+5. **回滚成本风险**
+   - 只读 mapper 的错误可通过测试修正。
+   - 入库命令的错误需要数据清理、关联检查和审计摘要，成本更高。
+
+### 缺失字段覆盖文档会导致什么问题？
+
+最直接的问题是同步命令无法判断“成功”是什么意思。它只能证明 API 返回了用户列表，不能证明这些用户足以支撑本系统的毕业离校业务。
+
+尤其需要提前写清：
+
+- `number -> User.user_id` 是否成立；
+- `name -> User.name` 是否必填；
+- `user_identity -> User.role` 的值域；
+- `class_id` 从哪里来，学工API没有时是否继续依赖 CSV；
+- `is_graduating`、`graduation_year` 从哪里来，缺失时是否禁止入库；
+- API 缺失用户时是否停用本地用户，还是仅报告差异。
+
+---
+
+## 效率考量
+
+**最快达到可工作状态的方式不是直接写同步命令，而是先做一个短平快的字段契约。**
+
+推荐 Step 2C-lite 控制在一个小交付内：
+
+1. 创建字段覆盖表，不追求真实字段全集，只覆盖“同步写库必需字段”。
+2. 把字段分为四类：
+   - API可直接提供
+   - API可能提供但需 live probe 确认
+   - 必须由 CSV/手工配置提供
+   - 暂不支持或禁止默认推断
+3. 明确同步门槛：
+   - 没有 `number/name`：不可创建用户
+   - 没有 `class_id`：不可替代当前学生 CSV 主路径
+   - 没有 `is_graduating/graduation_year`：不可声明毕业生筛选可用
+   - 没有辅导员映射：不可自动创建 `ClassMapping`
+4. 产出 mapper 测试用例输入/输出样例。
+
+完成这个文档后，Step 3 的 mapper/provider 可以很快实现，而且测试目标明确。反过来，如果直接写 DB 同步命令，测试会被迫同时覆盖字段猜测、数据转换、幂等 upsert、事务和命令输出，反馈周期会变慢。
+
+---
+
+## 遗漏检查
+
+Step 2系列还有一个关键遗漏：**字段覆盖报告不能只列 API 字段，还必须列内部写库字段和缺失字段策略。**
+
+建议 Step 2C-lite 至少包含以下表：
+
+| 内部目标 | 来源字段 | 状态 | 处理规则 |
+| --- | --- | --- | --- |
+| `User.user_id` | `number` | 文档样例可用，需 live 确认 | 必填；缺失则跳过并报告 |
+| `User.name` | `name` | 文档样例可用，需 live 确认 | 必填；缺失则跳过并报告 |
+| `User.role` | `user_identity` | 值域未知 | 只接受明确学生值；未知值跳过并报告 |
+| `User.class_id` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `User.is_graduating` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `User.graduation_year` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `ClassMapping` | 未确认 | 缺失 | 不由学工用户API自动生成 |
+
+还建议补充两个基础设施决策，放入 Step 2C 或 Step 3：
+
+1. **API 与 CSV 并存策略**
+   - 在字段未完全覆盖前，API 只能补充或更新可确定字段，不能替代 CSV 导入。
+
+2. **缺失/停用策略**
+   - 初期不要因为 API 本次未返回某用户就自动停用本地用户；先输出差异报告，等 live 数据稳定后再决定停用规则。
+
+---
+
+## 推荐执行方案
+
+### 下一步：Step 2C-lite
+
+产出文件建议：
+
+`docs/phase4c-xg-field-coverage.md`
+
+内容建议：
+
+1. 学工API文档样例字段清单
+2. 内部 `User` / `ClassMapping` 写库字段清单
+3. 字段映射表
+4. 缺失字段处理规则
+5. API/CSV 并存策略
+6. Step 3 mapper 测试样例
+
+验收标准：
+
+- 能明确哪些字段允许 API 写入，哪些字段仍由 CSV/手工来源维护；
+- 能明确什么情况下跳过记录、报告错误、禁止同步；
+- 能为下一步 mapper/provider 测试提供固定输入输出。
+
+### 随后：Step 3
+
+实现范围建议收窄为：
+
+- 新增纯转换函数或 `UserInfoProvider`；
+- 输入为 `fetch_all_users()` 返回的用户列表；
+- 输出为内部标准化用户 DTO / dict；
+- 不写数据库；
+- 单元测试覆盖字段缺失、角色未知、班级缺失、毕业字段缺失等场景。
+
+### 再后：Step 4/5
+
+等 mapper 通过测试后再做：
+
+- 幂等 upsert；
+- dry-run 变更摘要；
+- 冲突报告；
+- 不自动停用本地缺失用户；
+- management command 入口。
+
+---
+
+## 替代方案
+
+如果团队非常希望马上看到可执行命令，可以采用折中方案：
+
+**创建 `sync_xg_users --dry-run`，但只做读取和映射报告，不写数据库。**
+
+这本质上仍然是 Step 2C-lite + Step 3 的组合，不是完整同步命令。它可以提高可见性，同时避免未确认字段导致误写库。
+
+---
+
+## 最终建议
+
+**不要跳过 Step 2C。**
+
+但 Step 2C 不应拖成大文档任务，而应作为一个短周期、可执行的字段映射契约。完成后进入只读 mapper/provider；再进入 DB upsert；最后再封装 management command。
+
+本轮推荐决策：
+
+**A-prime：Step 2C-lite 字段映射契约优先，禁止直接实现写库同步命令。**

codex
已完成 Codex 审查响应，产出：

[91-next-priority-codex-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md)

核心结论：推荐 **A-prime：先做 Step 2C-lite 字段映射契约**，不要直接进入写库同步命令。Step 3 应先做只读 mapper / `UserInfoProvider` 和测试；DB upsert 与 management command 放到后续 Step 4/5。

我也已按协作协议记录事件：`.omc/collaboration/events.jsonl` 新增 event `102`，`state.json` 更新为 `waiting_for_claude_response`。本次是文档审查，未 rerun 测试。
diff --git a/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md b/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..b42293300cba0dfed225b660b8a7647b719805e2
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/91-next-priority-codex-response.md
@@ -0,0 +1,205 @@
+# Phase 4C 下一步优先级讨论 - Codex响应
+
+**审查日期：** 2026-06-02  
+**审查人：** Codex  
+**针对：** `90-next-priority-discussion-request.md`  
+**文档编号：** 91
+
+---
+
+## 审查结论
+
+**推荐优先级：选择 A，但收窄为“Step 2C-lite 字段映射契约”，随后进入 Step 3 的只读 Provider/映射测试。**
+
+不建议直接执行选项 B 或 C 中的“学生数据同步命令并入库”。当前 `fetch_all_users()` 已经解决分页读取问题，但数据库写入不是下一个最低风险动作。下一步应先把学工字段、内部 `User` 字段、CSV补充字段、缺失字段处理规则固定下来。
+
+建议顺序：
+
+1. **Step 2C-lite：字段覆盖与映射契约**
+2. **Step 3：只读 mapper / `UserInfoProvider` 设计与测试**
+3. **Step 4：同步服务与幂等 upsert**
+4. **Step 5：management command 运维入口**
+
+这也与 doc 85 的阶段划分一致：doc 85 中 Step 3 是“字段映射与 Provider 设计”，Step 4 才是“同步服务与数据库写入”，Step 5 才是“管理命令或后台任务入口”。本次请求中的选项 B 实际上把 Step 3、Step 4、Step 5 合并了，风险偏高。
+
+---
+
+## 依赖关系分析
+
+### Step 3是否强依赖Step 2C？
+
+**强依赖，但不是依赖真实凭证；依赖的是字段映射决策。**
+
+没有真实凭证时，仍然可以基于以下材料完成 Step 2C-lite：
+
+- 学工文档样例字段：`name`、`number`、`phone`、`identity_id`、`department`、`user_identity`、`updated_at` 等
+- 当前内部 `User` 模型字段：`user_id`、`name`、`role`、`active`、`class_id`、`is_graduating`、`graduation_year`
+- 当前 CSV 导入命令的业务要求：学生导入要求 `student_id`、`name`、`class_id`、`is_graduating`、`graduation_year`
+- 现有 `ClassMapping` 约束：学生 `class_id` 需要能匹配辅导员映射
+
+因此 Step 2C 不是“等 live probe 才能做”的硬阻塞项，而是一个必须先落地的同步契约。
+
+### 能否在实现Step 3时增量确定字段覆盖？
+
+可以增量修正字段覆盖，但不应在入库同步命令里首次确定字段覆盖。
+
+合理边界是：
+
+- mapper / provider 测试阶段可以增量调整字段映射；
+- DB upsert 阶段不应再临时决定必填字段、默认值、缺失字段策略；
+- management command 阶段只负责执行已确认的同步计划，不应承载字段决策。
+
+---
+
+## 风险评估
+
+### 直接跳到Step 3/同步命令的主要风险
+
+1. **误写入风险**
+   - 如果 `number` 是否等同 `student_id` 未确认，可能把错误字段作为 `User.user_id` 主键。
+   - 主键一旦写错，后续修复会涉及用户、申请、审批、通知等关联数据。
+
+2. **权限链风险**
+   - 当前业务依赖 `class_id` 和 `ClassMapping` 做辅导员可见性控制。
+   - 学工API文档样例没有明确稳定的 `class_id` 字段；如果用院系/专业/班级名称临时拼接，可能导致辅导员看不到学生或看到错误班级。
+
+3. **毕业生范围风险**
+   - CSV 导入要求 `is_graduating` 和 `graduation_year`。
+   - 学工API样例字段未证明能提供这两个字段。若默认所有学生都是毕业生，会扩大系统范围；若默认否，会导致毕业生缺失。
+
+4. **角色识别风险**
+   - `user_identity` 可能能区分学生/老师，但值域未确认。
+   - 未定义值域映射前，直接入库可能把辅导员、学生或其他人员角色写错。
+
+5. **回滚成本风险**
+   - 只读 mapper 的错误可通过测试修正。
+   - 入库命令的错误需要数据清理、关联检查和审计摘要，成本更高。
+
+### 缺失字段覆盖文档会导致什么问题？
+
+最直接的问题是同步命令无法判断“成功”是什么意思。它只能证明 API 返回了用户列表，不能证明这些用户足以支撑本系统的毕业离校业务。
+
+尤其需要提前写清：
+
+- `number -> User.user_id` 是否成立；
+- `name -> User.name` 是否必填；
+- `user_identity -> User.role` 的值域；
+- `class_id` 从哪里来，学工API没有时是否继续依赖 CSV；
+- `is_graduating`、`graduation_year` 从哪里来，缺失时是否禁止入库；
+- API 缺失用户时是否停用本地用户，还是仅报告差异。
+
+---
+
+## 效率考量
+
+**最快达到可工作状态的方式不是直接写同步命令，而是先做一个短平快的字段契约。**
+
+推荐 Step 2C-lite 控制在一个小交付内：
+
+1. 创建字段覆盖表，不追求真实字段全集，只覆盖“同步写库必需字段”。
+2. 把字段分为四类：
+   - API可直接提供
+   - API可能提供但需 live probe 确认
+   - 必须由 CSV/手工配置提供
+   - 暂不支持或禁止默认推断
+3. 明确同步门槛：
+   - 没有 `number/name`：不可创建用户
+   - 没有 `class_id`：不可替代当前学生 CSV 主路径
+   - 没有 `is_graduating/graduation_year`：不可声明毕业生筛选可用
+   - 没有辅导员映射：不可自动创建 `ClassMapping`
+4. 产出 mapper 测试用例输入/输出样例。
+
+完成这个文档后，Step 3 的 mapper/provider 可以很快实现，而且测试目标明确。反过来，如果直接写 DB 同步命令，测试会被迫同时覆盖字段猜测、数据转换、幂等 upsert、事务和命令输出，反馈周期会变慢。
+
+---
+
+## 遗漏检查
+
+Step 2系列还有一个关键遗漏：**字段覆盖报告不能只列 API 字段，还必须列内部写库字段和缺失字段策略。**
+
+建议 Step 2C-lite 至少包含以下表：
+
+| 内部目标 | 来源字段 | 状态 | 处理规则 |
+| --- | --- | --- | --- |
+| `User.user_id` | `number` | 文档样例可用，需 live 确认 | 必填；缺失则跳过并报告 |
+| `User.name` | `name` | 文档样例可用，需 live 确认 | 必填；缺失则跳过并报告 |
+| `User.role` | `user_identity` | 值域未知 | 只接受明确学生值；未知值跳过并报告 |
+| `User.class_id` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `User.is_graduating` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `User.graduation_year` | 未确认 | 缺失 | 继续由 CSV/手工维护，API 不覆盖 |
+| `ClassMapping` | 未确认 | 缺失 | 不由学工用户API自动生成 |
+
+还建议补充两个基础设施决策，放入 Step 2C 或 Step 3：
+
+1. **API 与 CSV 并存策略**
+   - 在字段未完全覆盖前，API 只能补充或更新可确定字段，不能替代 CSV 导入。
+
+2. **缺失/停用策略**
+   - 初期不要因为 API 本次未返回某用户就自动停用本地用户；先输出差异报告，等 live 数据稳定后再决定停用规则。
+
+---
+
+## 推荐执行方案
+
+### 下一步：Step 2C-lite
+
+产出文件建议：
+
+`docs/phase4c-xg-field-coverage.md`
+
+内容建议：
+
+1. 学工API文档样例字段清单
+2. 内部 `User` / `ClassMapping` 写库字段清单
+3. 字段映射表
+4. 缺失字段处理规则
+5. API/CSV 并存策略
+6. Step 3 mapper 测试样例
+
+验收标准：
+
+- 能明确哪些字段允许 API 写入，哪些字段仍由 CSV/手工来源维护；
+- 能明确什么情况下跳过记录、报告错误、禁止同步；
+- 能为下一步 mapper/provider 测试提供固定输入输出。
+
+### 随后：Step 3
+
+实现范围建议收窄为：
+
+- 新增纯转换函数或 `UserInfoProvider`；
+- 输入为 `fetch_all_users()` 返回的用户列表；
+- 输出为内部标准化用户 DTO / dict；
+- 不写数据库；
+- 单元测试覆盖字段缺失、角色未知、班级缺失、毕业字段缺失等场景。
+
+### 再后：Step 4/5
+
+等 mapper 通过测试后再做：
+
+- 幂等 upsert；
+- dry-run 变更摘要；
+- 冲突报告；
+- 不自动停用本地缺失用户；
+- management command 入口。
+
+---
+
+## 替代方案
+
+如果团队非常希望马上看到可执行命令，可以采用折中方案：
+
+**创建 `sync_xg_users --dry-run`，但只做读取和映射报告，不写数据库。**
+
+这本质上仍然是 Step 2C-lite + Step 3 的组合，不是完整同步命令。它可以提高可见性，同时避免未确认字段导致误写库。
+
+---
+
+## 最终建议
+
+**不要跳过 Step 2C。**
+
+但 Step 2C 不应拖成大文档任务，而应作为一个短周期、可执行的字段映射契约。完成后进入只读 mapper/provider；再进入 DB upsert；最后再封装 management command。
+
+本轮推荐决策：
+
+**A-prime：Step 2C-lite 字段映射契约优先，禁止直接实现写库同步命令。**

tokens used
59,549

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
