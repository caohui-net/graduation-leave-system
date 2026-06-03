# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-01T19:23:29.310Z

## Original task

docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md

## Final prompt

docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md

## Raw output

```text
Created the Codex review response at [63-phase2b-contract-decision-codex-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md).

Conclusion: recommend **Option 1** for v0.1: keep synchronous `422 DORM_BLOCKED`, do not create a notification, and remove or defer `DORM_CLEARANCE_BLOCKED` from the automatic notification contract. If persistent notification-center history becomes a product requirement later, use an independent `DormClearanceBlock` entity, not a blocked `Application` or `student_id` as a fake event entity.

I also flagged one adjacent contract mismatch: `APPLICATION_SUBMITTED` currently uses `approval` as the actual notification entity in code, while the contract says `application`; the contract should be corrected while touching this file. No tests were run because this was a document review only.


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
session id: 019e84a1-db31-7df1-b3d0-79c90724bb0d
--------
user
docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md
codex
I’ll inspect the project rules and the referenced review request first, then I’ll respond in the format the local review protocol expects.
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
/bin/bash -lc "sed -n '1,260p' docs/discussions/phase4c-next-steps/62-phase2b-contract-decision-review-request.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Phase 2B契约决策审查请求

**日期：** 2026-06-02  
**作者：** Claude  
**类型：** 契约决策审查请求  
**审查对象：** 宿舍阻断通知的实体与幂等问题

---

## 审查背景

**当前状态：**
- Track 3 Phase 2A完成（申请提交/审批通过/审批驳回通知）
- Phase 2B目标：宿舍阻断通知
- 发现契约与代码不一致问题

**问题来源：**
- Codex在60号文档中识别P1风险：宿舍阻断通知缺少可关联实体
- 契约声明关联application_id，但422时不创建Application
- 现有测试断言"宿舍阻断不创建通知"

---

## 核心问题

### 问题1：契约与实现不一致

**契约声明（notification-contract-v0.1.md）：**
```
DORM_CLEARANCE_BLOCKED:
  entity_type: application
  entity_id: application_id
  recipient: student
  message: "宿舍清退未通过，无法提交申请"
```

**实际代码（backend/apps/applications/views.py）：**
```python
# create_application视图
if not dorm_response.get('cleared'):
    return Response({
        'error': 'DORM_CLEARANCE_BLOCKED',
        'message': '宿舍清退未通过，无法提交申请'
    }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    # 直接返回422，不创建Application
```

**测试期望（test_auto_notifications_api.py）：**
```python
def test_dorm_blocked_does_not_create_notification(self):
    # 断言：宿舍阻断不创建通知
    assert Notification.objects.count() == 0
```

### 问题2：实体ID缺失

如果要创建宿舍阻断通知：
- 需要合法的entity_id用于幂等约束（recipient_id + entity_type + entity_id唯一）
- 当前422时没有Application，无法提供application_id
- 伪造entity_id会破坏通知表唯一约束的语义

---

## 决策选项

### Option 1：不为宿舍阻断创建通知

**方案：**
- 保留422错误响应
- 不创建通知
- 从契约中删除DORM_CLEARANCE_BLOCKED或标记为deferred

**优点：**
- 实现简单，无需修改代码
- 与现有测试一致
- 避免实体ID问题

**缺点：**
- 学生只能在提交时看到错误，无法通过通知中心查看
- 用户体验略差

---

### Option 2：创建blocked application或阻断记录

**方案：**
- 宿舍清退失败时创建Application（status=blocked或新状态）
- 或创建独立的DormBlockRecord表
- 使用该记录的ID作为entity_id

**优点：**
- 有合法实体ID
- 可以创建通知
- 学生可以在通知中心查看阻断原因

**缺点：**
- 需要修改Application模型（添加blocked状态）或创建新表
- 增加复杂度
- blocked application可能与审批流程状态机冲突

---

### Option 3：扩展通知实体类型

**方案：**
- 允许entity_type为dorm_clearance或student
- 使用student_id作为entity_id（宿舍阻断通知）
- 修改幂等键定义（recipient_id + entity_type + entity_id + notification_type）

**优点：**
- 不需要创建blocked application
- 可以创建通知
- 灵活性高

**缺点：**
- 打破"通知关联业务实体"的设计原则
- 幂等键变复杂（需要加notification_type）
- 可能导致重复通知（同一学生多次尝试提交）

---

## 审查要点

**请Codex审查以下问题：**

1. **推荐选项：** 三个选项中哪个最合理？为什么？
2. **实体设计：** 如果选Option 2，应该用blocked application还是独立表？
3. **幂等性：** 如果选Option 3，如何防止重复通知？
4. **测试调整：** 如果创建通知，test_dorm_blocked_does_not_create_notification需要如何修改？
5. **契约修正：** notification-contract-v0.1.md需要如何更新？
6. **影响范围：** 每个选项需要修改哪些文件？

---

## 相关文件

**契约文档：**
- docs/api/notification-contract-v0.1.md（通知契约）

**代码文件：**
- backend/apps/applications/views.py（create_application视图）
- backend/apps/applications/models.py（Application模型）
- backend/apps/notifications/models.py（Notification模型）
- backend/apps/notifications/services.py（通知服务）

**测试文件：**
- backend/apps/notifications/tests/test_auto_notifications_api.py（自动通知测试）

**讨论文档：**
- docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md（Codex识别问题）
- docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md（最终共识）

---

## 期望输出

**Codex审查应包含：**
1. 推荐选项及理由
2. 实体设计建议（如适用）
3. 幂等性方案（如适用）
4. 契约修正建议
5. 测试调整建议
6. 需要修改的文件清单
7. 实现风险评估

---

**文档编号：** 62  
**状态：** 待Codex审查

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
I found this is a formal Codex review request. I also caught that the project requires `rtk` on shell commands, so subsequent commands will follow that project rule while I inspect the contract, code, and tests behind the decision.
exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/applications/models.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from django.db import models
from django.core.exceptions import ValidationError
from apps.users.models import User


class ApplicationStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
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
        if self.status in [ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.PENDING_DEAN, ApplicationStatus.APPROVED]:
            existing = Application.objects.filter(
                student=self.student,
                status__in=[ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.PENDING_DEAN, ApplicationStatus.APPROVED]
            ).exclude(application_id=self.application_id).exists()
            if existing:
                raise ValidationError('该学生已有待审批或已通过的申请，不能重复提交')

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/api/notification-contract-v0.1.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 通知系统契约 v0.1

**版本：** v0.1  
**状态：** Draft  
**创建日期：** 2026-06-01  
**目的：** 定义通知系统最小契约，为后续实现提供设计基础

---

## 1. 概述

本契约定义毕业生离校申请审批系统的通知功能最小契约。通知系统用于向用户推送申请状态变更、审批结果、系统提醒等信息。

**设计原则：**
- 最小化：只定义核心通知读取功能
- 幂等性：同一业务事件不重复创建通知
- 权限隔离：用户只能读取自己的通知

**非目标：**
- 微信模板消息推送（推迟到生产部署）
- 小程序通知页面（推迟到DevTools可用）
- 实时推送（WebSocket/SSE）
- 消息中心运营功能

---

## 2. 通知事件类型

### 2.1 事件枚举

| 事件类型 | 枚举值 | 触发时机 | 接收者 |
|---------|--------|----------|--------|
| 申请提交 | APPLICATION_SUBMITTED | 学生提交离校申请 | 辅导员 |
| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
| 宿舍清退阻断 | DORM_CLEARANCE_BLOCKED | 宿舍清退未完成阻断申请 | 学生 |
| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |

### 2.2 事件详细说明

#### APPLICATION_SUBMITTED（申请提交）

**触发条件：** 学生成功提交离校申请

**接收者：** 该学生的辅导员

**通知内容：**
- 标题：`新的离校申请`
- 正文：`学生{student_name}（{student_id}）提交了离校申请，请及时审批。`

**关联实体：**
- entity_type: `application`
- entity_id: `{application_id}`

---

#### APPROVAL_APPROVED（审批通过）

**触发条件：** 辅导员或学工部审批通过

**接收者：** 申请学生

**通知内容：**
- 标题：`审批通过`
- 正文：`您的离校申请已通过{approver_role}审批。` （approver_role: 辅导员/学工部）

**关联实体：**
- entity_type: `approval`
- entity_id: `{approval_id}`

---

#### APPROVAL_REJECTED（审批驳回）

**触发条件：** 辅导员或学工部驳回申请

**接收者：** 申请学生

**通知内容：**
- 标题：`审批驳回`
- 正文：`您的离校申请被{approver_role}驳回。驳回原因：{comment}`

**关联实体：**
- entity_type: `approval`
- entity_id: `{approval_id}`

---

#### DORM_CLEARANCE_BLOCKED（宿舍清退阻断）

**触发条件：** 宿舍管理系统返回清退未完成

**接收者：** 申请学生

**通知内容：**
- 标题：`宿舍清退未完成`
- 正文：`您的离校申请因宿舍清退未完成而被阻断，请先完成宿舍清退手续。`

**关联实体：**
- entity_type: `application`
- entity_id: `{application_id}`

---

#### APPROVAL_TIMEOUT_WARNING（审批超时提醒）

**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理

**接收者：** 待审批的辅导员/学工部

**通知内容：**
- 标题：`审批超时提醒`
- 正文：`学生{student_name}的离校申请已超过{days}个工作日未审批，请及时处理。`

**关联实体：**
- entity_type: `approval`
- entity_id: `{approval_id}`

---

## 3. 数据模型

### 3.1 Notification字段草案

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| notification_id | String | 是 | 通知ID，格式：not_xxxxxxxx（8位随机字符） |
| recipient_id | String | 是 | 接收者用户ID（外键：User.user_id） |
| actor_id | String | 否 | 触发者用户ID（外键：User.user_id），可为空 |
| type | Enum | 是 | 通知类型（见2.1事件枚举） |
| title | String | 是 | 通知标题（最大100字符） |
| body | String | 是 | 通知正文（最大500字符） |
| entity_type | Enum | 是 | 关联实体类型：application/approval |
| entity_id | String | 是 | 关联实体ID |
| read_at | DateTime | 否 | 已读时间，未读为null |
| created_at | DateTime | 是 | 创建时间 |

### 3.2 索引建议

```sql
-- 主键索引
PRIMARY KEY (notification_id)

-- 接收者查询索引（最常用）
INDEX idx_recipient_created (recipient_id, created_at DESC)

-- 未读通知查询索引
INDEX idx_recipient_unread (recipient_id, read_at) WHERE read_at IS NULL

-- 幂等性唯一约束（防止重复通知）
UNIQUE INDEX idx_notification_idempotency (recipient_id, entity_type, entity_id, type)
```

---

## 4. API契约

### 4.1 列出通知

**端点：** `GET /api/notifications/`

**权限：** 认证用户

**查询参数：**
- `read` (可选): `true`/`false`/`all`，默认`all`
- `limit` (可选): 每页数量，默认20，最大100
- `offset` (可选): 偏移量，默认0

**请求示例：**
```http
GET /api/notifications/?read=false&limit=20&offset=0
Authorization: Bearer {access_token}
```

**响应示例（200 OK）：**
```json
{
  "count": 5,
  "results": [
    {
      "notification_id": "not_a1b2c3d4",
      "type": "APPROVAL_APPROVED",
      "title": "审批通过",
      "body": "您的离校申请已通过辅导员审批。",
      "entity_type": "approval",
      "entity_id": "apv_12345678",
      "read_at": null,
      "created_at": "2026-06-01T10:30:00Z",
      "actor": {
        "user_id": "T001",
        "name": "张老师"
      }
    }
  ]
}
```

**RBAC规则：**
- 用户只能查询自己的通知（recipient_id = request.user.user_id）
- 管理员不默认拥有跨用户读取权限

---

### 4.2 未读通知数

**端点：** `GET /api/notifications/unread_count/`

**权限：** 认证用户

**请求示例：**
```http
GET /api/notifications/unread_count/
Authorization: Bearer {access_token}
```

**响应示例（200 OK）：**
```json
{
  "unread_count": 3
}
```

---

### 4.3 标记单条已读

**端点：** `PATCH /api/notifications/{notification_id}/read/`

**权限：** 认证用户，且notification.recipient_id = request.user.user_id

**请求示例：**
```http
PATCH /api/notifications/not_a1b2c3d4/read/
Authorization: Bearer {access_token}
```

**响应示例（200 OK）：**
```json
{
  "notification_id": "not_a1b2c3d4",
  "read_at": "2026-06-01T11:00:00Z"
}
```

**错误响应（403 FORBIDDEN）：**
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "您无权标记此通知为已读"
  }
}
```

---

### 4.4 全部标记已读

**端点：** `POST /api/notifications/mark_all_read/`


exec
/bin/bash -lc "rtk sed -n '1,280p' backend/apps/notifications/models.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
import string
import random
from django.db import models
from django.conf import settings


def generate_notification_id():
    """生成格式为 not_xxxxxxxx 的通知ID"""
    chars = string.ascii_lowercase + string.digits
    random_str = ''.join(random.choices(chars, k=8))
    return f'not_{random_str}'


class NotificationType(models.TextChoices):
    APPLICATION_SUBMITTED = 'application_submitted', '申请已提交'
    APPROVAL_APPROVED = 'approval_approved', '审批通过'
    APPROVAL_REJECTED = 'approval_rejected', '审批驳回'
    DORM_CLEARANCE_BLOCKED = 'dorm_clearance_blocked', '宿舍清退阻断'
    APPROVAL_TIMEOUT_WARNING = 'approval_timeout_warning', '审批超时提醒'


class EntityType(models.TextChoices):
    APPLICATION = 'application', '离校申请'
    APPROVAL = 'approval', '审批记录'


class Notification(models.Model):
    notification_id = models.CharField(
        max_length=12,
        primary_key=True,
        default=generate_notification_id,
        editable=False,
        verbose_name='通知ID'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='notifications_received',
        verbose_name='接收者'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='notifications_triggered',
        null=True,
        blank=True,
        verbose_name='触发者'
    )
    type = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
        verbose_name='通知类型'
    )
    entity_type = models.CharField(
        max_length=50,
        choices=EntityType.choices,
        verbose_name='实体类型'
    )
    entity_id = models.CharField(
        max_length=50,
        verbose_name='实体ID'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='标题'
    )
    message = models.TextField(
        verbose_name='消息内容'
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='已读时间'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )

    class Meta:
        db_table = 'notifications'
        verbose_name = '通知'
        verbose_name_plural = '通知'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'created_at']),
            models.Index(fields=['recipient', 'read_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['recipient', 'entity_type', 'entity_id', 'type'],
                name='unique_notification_per_recipient_entity'
            )
        ]

    def __str__(self):
        return f'{self.notification_id}: {self.title}'

exec
/bin/bash -lc "rtk sed -n '1,260p' backend/apps/applications/views.py" in /home/caohui/projects/graduation-leave-system
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
from backend.schema import ErrorResponseSerializer
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

    # Counselor: applications with own pending counselor approvals
    elif user.role == UserRole.COUNSELOR:
        pending_approvals = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.COUNSELOR,
            decision=ApprovalDecision.PENDING
        ).values_list('application', flat=True)
        queryset = Application.objects.filter(pk__in=pending_approvals)

    # Dean: applications with own pending dean approvals
    elif user.role == UserRole.DEAN:
        pending_approvals = Approval.objects.filter(
            approver=user,
            step=ApprovalStep.DEAN,
            decision=ApprovalDecision.PENDING
        ).values_list('application', flat=True)
        queryset = Application.objects.filter(pk__in=pending_approvals)

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
        status__in=[ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.PENDING_DEAN, ApplicationStatus.APPROVED]
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

    application = Application.objects.create(
        application_id=f'app_{uuid.uuid4().hex[:8]}',
        student=user,
        student_name=user.name,
        class_id=user.class_id,
        reason=serializer.validated_data['reason'],
        leave_date=serializer.validated_data['leave_date'],
        status=ApplicationStatus.PENDING_COUNSELOR,
        dorm_checkout_status=dorm_status.status
    )

    counselor_approval = Approval.objects.create(
        approval_id=f'apv_{uuid.uuid4().hex[:8]}',
        application=application,
        step=ApprovalStep.COUNSELOR,
        approver=class_mapping.counselor,
        approver_name=class_mapping.counselor_name,
        decision=ApprovalDecision.PENDING
    )

    notify_application_submitted(application, counselor_approval)

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
/bin/bash -lc "rtk sed -n '1,360p' backend/apps/notifications/tests/test_auto_notifications_api.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
"""
API-level tests for automatic notification creation.

Verifies that notifications created by business logic are visible through the API
and that negative paths (permission denied, status conflicts) don't create notifications.
"""

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.applications.models import Application, ApplicationStatus
from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
from apps.notifications.models import Notification
from apps.users.class_mapping import ClassMapping

User = get_user_model()


class AutoNotificationAPITest(TestCase):
    """Test automatic notifications are visible through API."""

    def setUp(self):
        """Create test users and class mapping."""
        self.client = APIClient()

        self.student = User.objects.create_user(
            user_id='2020001',
            name='测试学生',
            role='student',
            class_id='CS2021-1'
        )
        self.counselor = User.objects.create_user(
            user_id='T001',
            name='张老师',
            role='counselor'
        )
        self.dean = User.objects.create_user(
            user_id='D001',
            name='赵主任',
            role='dean'
        )

        ClassMapping.objects.create(
            class_id='CS2021-1',
            counselor=self.counselor,
            counselor_name=self.counselor.name,
            active=True
        )

    def test_application_submitted_notification_visible_via_api(self):
        """Test counselor can see APPLICATION_SUBMITTED notification via API after student submits."""
        # Student submits application (triggers notification)
        self.client.force_authenticate(user=self.student)
        response = self.client.post('/api/applications/', {
            'reason': '毕业离校',
            'leave_date': '2026-07-01'
        })
        self.assertEqual(response.status_code, 201)

        # Counselor checks notifications via API
        self.client.force_authenticate(user=self.counselor)
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, 200)

        notifications = response.json()['results']
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0]['type'], 'application_submitted')
        self.assertEqual(notifications[0]['entity_type'], 'approval')
        self.assertIn('测试学生', notifications[0]['message'])

    def test_approval_approved_notification_visible_via_api(self):
        """Test student can see APPROVAL_APPROVED notification via API after counselor approves."""
        # Create application and approval
        application = Application.objects.create(
            application_id='app_test001',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2026-07-01',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        approval = Approval.objects.create(
            approval_id='apv_test001',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.PENDING
        )

        # Counselor approves (triggers notification)
        self.client.force_authenticate(user=self.counselor)
        response = self.client.post(f'/api/approvals/{approval.approval_id}/approve/', {
            'comment': '同意'
        })
        self.assertEqual(response.status_code, 200)

        # Student checks notifications via API
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, 200)

        notifications = response.json()['results']
        self.assertGreaterEqual(len(notifications), 1)

        # Find the approval notification
        approval_notif = [n for n in notifications if n['type'] == 'approval_approved'][0]
        self.assertEqual(approval_notif['entity_type'], 'approval')
        self.assertIn('辅导员', approval_notif['message'])

    def test_approval_rejected_notification_includes_reason(self):
        """Test APPROVAL_REJECTED notification includes rejection reason in message."""
        # Create application and approval
        application = Application.objects.create(
            application_id='app_test002',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2026-07-01',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        approval = Approval.objects.create(
            approval_id='apv_test002',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.PENDING
        )

        # Counselor rejects with reason
        self.client.force_authenticate(user=self.counselor)
        response = self.client.post(f'/api/approvals/{approval.approval_id}/reject/', {
            'comment': '材料不齐全，请补充'
        })
        self.assertEqual(response.status_code, 200)

        # Student checks notification
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, 200)

        notifications = response.json()['results']
        reject_notif = [n for n in notifications if n['type'] == 'approval_rejected'][0]
        self.assertIn('材料不齐全，请补充', reject_notif['message'])

    def test_permission_denied_does_not_create_notification(self):
        """Test that permission denied does not create spurious notifications."""
        # Create application for student1
        student2 = User.objects.create_user(
            user_id='2021002',
            name='其他学生',
            role='student',
            class_id='CS2021-2'
        )

        application = Application.objects.create(
            application_id='app_test003',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2026-07-01',
            status=ApplicationStatus.PENDING_COUNSELOR
        )

        approval = Approval.objects.create(
            approval_id='apv_test003',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.PENDING
        )

        # Student2 tries to approve (should fail with permission denied)
        self.client.force_authenticate(user=student2)
        response = self.client.post(f'/api/approvals/{approval.approval_id}/approve/', {
            'comment': '同意'
        })
        self.assertIn(response.status_code, [403, 404])

        # Verify no notification was created
        self.assertEqual(Notification.objects.filter(
            entity_type='approval',
            entity_id=approval.pk
        ).count(), 0)

    def test_status_conflict_does_not_create_notification(self):
        """Test that status conflict (e.g., re-approving) does not create duplicate notifications."""
        # Create application and approval
        application = Application.objects.create(
            application_id='app_test004',
            student=self.student,
            student_name=self.student.name,
            class_id=self.student.class_id,
            reason='毕业离校',
            leave_date='2026-07-01',
            status=ApplicationStatus.PENDING_DEAN  # Already past counselor
        )

        approval = Approval.objects.create(
            approval_id='apv_test004',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=self.counselor,
            approver_name=self.counselor.name,
            decision=ApprovalDecision.APPROVED  # Already approved
        )

        # Counselor tries to approve again (should fail with conflict)
        self.client.force_authenticate(user=self.counselor)
        response = self.client.post(f'/api/approvals/{approval.approval_id}/approve/', {
            'comment': '再次同意'
        })
        self.assertEqual(response.status_code, 409)

        # Verify only one notification exists (from initial approval, not from failed re-approval)
        self.assertEqual(Notification.objects.filter(
            recipient=self.student,
            entity_type='approval',
            entity_id=approval.pk
        ).count(), 0)  # No notification because we created approval directly, not through API

    def test_dorm_blocked_does_not_create_notification(self):
        """Test that dorm checkout blockage does not create notifications."""
        # Create student with non-completed dorm status (use ID not in mock data)
        blocked_student = User.objects.create_user(
            user_id='2021999',
            name='被阻断学生',
            role='student',
            class_id='CS2021-1'
        )

        # Student tries to submit application (should fail with 422 dorm blocked)
        self.client.force_authenticate(user=blocked_student)
        response = self.client.post('/api/applications/', {
            'reason': '毕业离校',
            'leave_date': '2026-07-01'
        })
        self.assertEqual(response.status_code, 422)

        # Verify no notification was created for counselor
        self.assertEqual(Notification.objects.filter(
            recipient=self.counselor,
            type='application_submitted'
        ).count(), 0)

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/phase4c-next-steps/61-claude-codex-final-consensus-d0-a-lite.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Claude-Codex最终共识 - 执行D0 + A-lite

**日期：** 2026-06-02  
**作者：** Claude + Codex  
**类型：** 最终共识  
**状态：** 达成共识，立即执行

---

## 共识内容

**执行Option 2 + D0 + A-lite方案。**

**核心决策：**
1. ✅ 接受API Schema P1"代码完成，未验收"状态
2. ✅ 执行D0：API Schema文档一致性修正（15-30分钟）
3. ✅ 执行A-lite：Track 3 Phase 2B契约修正优先（30-60分钟 + 1-2小时实现）
4. ⏸ Phase 2C单独立项（不与2B捆绑执行）

---

## Claude完全接受Codex建议

**Codex的关键洞察：**
1. API Schema TODO文档状态自相矛盾（顶部"P1完成"，后文"待验证"）
2. 宿舍阻断通知缺少可关联实体（契约声明application_id，但422时不创建Application）
3. 现有测试与Phase 2B目标相反（断言"不创建通知"）
4. Phase 2C基础设施未就绪（Celery/Redis依赖存在，但未配置）

**Claude认同：**
- 59号文档的方向A（2B+2C合并执行）跨度偏大
- 必须先修正文档一致性
- 必须先解决2B契约冲突
- Phase 2C不能作为4-6小时的顺手收尾任务

---

## 执行计划

### D0：API Schema文档一致性修正（15-30分钟）

**目标：** 修正`docs/api/api-schema-todo.md`状态表述

**修改内容：**
1. 顶部状态：从"P1完成"改为"P1代码完成，验收阻塞"
2. 基线验收状态：改为"待可用环境复验"
3. 删除已通过检查的误导表述（HTTP 200、operation统计）
4. 保留login响应schema修复为已完成代码项

**产出：** api-schema-todo.md v2.2

---

### A-lite Step 1：Phase 2B契约修正（30-60分钟）

**目标：** 解决宿舍阻断通知的实体与幂等问题

**决策选项：**
- **Option 1：** 不为宿舍阻断创建通知，保留422错误响应
- **Option 2：** 创建blocked application或阻断记录，作为通知实体
- **Option 3：** 扩展通知实体类型（dorm_clearance或student），定义幂等键

**执行：**
1. 分析当前代码和测试
2. 选择最合理的契约方案
3. 更新`notification-contract-v0.1.md`
4. 更新测试期望

**产出：** notification-contract-v0.1.md修订 + 契约决策文档

---

### A-lite Step 2：Phase 2B实现（1-2小时）

**前置条件：** Step 1契约明确后执行

**范围：**
1. 根据契约决策实现通知逻辑
2. 添加服务函数
3. 添加API级测试
4. 调整现有测试（test_dorm_blocked_does_not_create_notification）
5. 验证只对学生本人创建通知

**产出：** 代码实现 + 测试 + smoke验证

---

### Phase 2C：单独立项（不在本次执行）

**原因：**
- 需要Celery beat配置（docker-compose服务、settings、broker）
- 需要工作日算法、扫描窗口、重复提醒策略
- 需要幂等键和调度验收
- 时间估算：2-7小时（取决于Celery vs 同步方案）

**下一步：** 2B完成后单独评审

---

## 执行顺序

1. **立即执行D0**（15-30分钟）
2. **立即执行A-lite Step 1**（30-60分钟）
3. **根据契约决策执行A-lite Step 2**（1-2小时）
4. **Phase 2C单独讨论**（2B完成后）

---

## 时间估算

**D0 + A-lite总计：** 2-3.5小时
- D0：15-30分钟
- A-lite Step 1：30-60分钟
- A-lite Step 2：1-2小时

**Phase 2C（单独）：** 2-7小时（取决于方案）

---

## 产出物

**D0：**
- docs/api/api-schema-todo.md v2.2

**A-lite Step 1：**
- docs/api/notification-contract-v0.1.md（修订）
- docs/discussions/phase4c-next-steps/XX-phase2b-contract-decision.md

**A-lite Step 2：**
- backend/apps/notifications/services.py（修改）
- backend/apps/notifications/tests/（修改）
- tests/smoke_test.sh（可能修改）

---

## 最终共识

> 执行Option 2 + D0 + A-lite方案。立即修正API Schema文档状态，然后执行Phase 2B契约修正和实现。Phase 2C单独立项，不与2B捆绑执行。

---

**文档编号：** 61  
**状态：** 共识达成，立即执行

exec
/bin/bash -lc "rtk sed -n '1,240p' docs/discussions/phase4c-next-steps/60-codex-final-consensus-option-2-review-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Codex审查响应 - 最终共识Option 2与下一步方向

**日期：** 2026-06-02  
**作者：** Codex  
**类型：** 策略审查响应  
**针对：** 59-claude-codex-final-consensus-option-2.md

---

## 审查结论

**同意执行Option 2，但不同意直接按59号文档的完整方向A（Track 3 Phase 2B-2C）开工。**

更稳妥的下一步是：

1. 先做一个很小的文档一致性修正：把 `docs/api/api-schema-todo.md` 的状态改成“代码完成，未验收”，不要继续写“P1完成”。
2. 然后执行 **Direction A-lite：Track 3 Phase 2B契约修正优先**。
3. Phase 2C（审批超时提醒）暂不和2B捆绑执行，先单独立项并明确Celery/调度策略。

理由是：Option 2本身合理，但59号文档把“继续其他工作”直接落到2B-2C完整实现，跨度偏大。当前代码和契约对2B仍有实质冲突，2C还会引入调度基础设施，不能作为一个4-6小时的顺手收尾任务处理。

---

## 对5个问题的回答

### 1. 是否同意执行Option 2？

**同意。**

P1 Schema当前只能标记为“代码完成，未验收”。在依赖安装失败、schema生成不可运行、operationId唯一性无法验证的情况下，继续P2示例会固化潜在错误契约。接受未验收状态并切换到不依赖该schema验收的工作，是合理选择。

但需要补一个前置动作：`docs/api/api-schema-todo.md` 顶部和基线验收区仍写着“P1完成”和多项已通过检查，后文又写环境不可用、验证待完成。这个文档应先修成一致状态，否则后续讨论会继续误读P1边界。

### 2. 是否同意方向A作为下一步？

**只同意收窄后的方向A-lite，不同意一次性执行2B+2C。**

Phase 2B可以作为下一步，但必须先修契约。当前 `DORM_CLEARANCE_BLOCKED` 契约声明关联 `application_id`，而实际 `create_application` 在宿舍清退失败时直接返回422，根本不会创建Application。现有测试也明确断言宿舍阻断不创建通知。

因此2B不能直接“实现通知逻辑”。必须先决定以下契约之一：

- 继续不为宿舍阻断创建通知，只保留422错误响应。
- 创建一种可持久化的阻断记录或blocked application，再用它作为通知实体。
- 扩展通知实体类型，例如 `dorm_clearance` 或 `student`，并定义幂等键。

没有这个决定，2B实现会在实体ID、幂等约束和测试期望上不一致。

Phase 2C不建议现在合并执行。当前 `requirements` 有Celery/Redis依赖，但项目设置和 `docker-compose.yml` 尚未配置Celery worker/beat。审批超时提醒还需要工作日算法、扫描窗口、重复提醒策略、幂等键和调度验收，这不是2B旁边的小补丁。

### 3. 是否有更优方向？

**建议方向：D0 + A-lite。**

**D0：API Schema状态文档一致性修正（15-30分钟）**
- 把 `docs/api/api-schema-todo.md` 状态从“P1完成”改为“P1代码完成，验收阻塞”。
- 将基线验收状态改成“待可用环境复验”，不要保留HTTP 200/operation统计的通过表述。
- 保留login响应schema修复为已完成代码项。

**A-lite Step 1：Phase 2B契约修正（30-60分钟）**
- 明确宿舍阻断是否产生通知。
- 如果产生通知，先补实体类型/幂等规则/测试期望。
- 如果不产生通知，把契约中的 `DORM_CLEARANCE_BLOCKED` 标记为 deferred 或删除自动通知承诺。

**A-lite Step 2：只在契约明确后实现Phase 2B（1-2小时）**
- 添加服务函数和API级测试。
- 调整当前 `test_dorm_blocked_does_not_create_notification`。
- 验证只对学生本人创建通知，不向辅导员创建误通知。

**Phase 2C：单独立项**
- 先写Celery/无Celery两种实现决策。
- 如果引入Celery beat，必须同时补配置、docker-compose服务、任务幂等测试和调度验收说明。

### 4. 时间估算是否合理？

**59号文档的4-6小时对“完整2B+2C”偏乐观。**

更合理估算：

- D0文档一致性：15-30分钟
- Phase 2B契约修正：30-60分钟
- Phase 2B实现与测试：1-2小时
- Phase 2C最小同步/management command方案：2-3小时
- Phase 2C Celery beat完整方案：4-7小时

如果坚持完整2B+2C并包含Celery配置、Docker服务、幂等、防重复和测试，建议按 **5.5-8小时** 估算，而不是4-6小时。

### 5. 执行顺序是否合理？

**建议调整执行顺序。**

推荐顺序：

1. 修正 `docs/api/api-schema-todo.md` 的P1状态表述。
2. 创建或更新2B契约修正文档，先解决宿舍阻断通知的实体与幂等问题。
3. 执行Phase 2B实现和测试。
4. 再决定Phase 2C是否采用Celery beat；不要默认引入。
5. Phase 2C执行前补验收清单，包括重复运行不重复通知、只提醒pending审批、已处理审批不会提醒。

---

## 关键风险

### P1：API Schema TODO状态仍自相矛盾

`docs/api/api-schema-todo.md` 顶部写“P1完成”，基线验收也列出 `/api/schema/` 和 Swagger UI 可访问；但同一文件后文又说明由于环境限制，schema生成、schema端点、Swagger UI、operationId唯一性和后端测试均待验证。

这会直接违背58/59号文档已经达成的“代码完成，未验收”共识。建议立刻修正。

### P1：宿舍阻断通知缺少可关联实体

`docs/api/notification-contract-v0.1.md` 声明宿舍阻断通知关联 `application_id`，但 `backend/apps/applications/views.py` 在宿舍清退失败时直接返回422，不创建Application。当前Application状态也没有blocked状态。

如果直接创建通知，要么没有合法 `entity_id`，要么需要临时伪造实体ID，都会破坏通知表唯一约束的语义。

### P1：现有测试与Phase 2B目标相反

`backend/apps/notifications/tests/test_auto_notifications_api.py` 中当前测试名和断言是“宿舍阻断不创建通知”。如果2B目标是创建宿舍阻断通知，必须先更新测试意图，并确认这是产品/契约层面的正式变更。

### P2：Phase 2C基础设施未就绪

项目依赖中已有Celery/Redis，但settings和docker-compose尚未配置broker、worker、beat服务。直接实现定时提醒会把任务代码、运行方式和验收证据拆散。

---

## 最终建议

**批准Option 2；批准继续Track 3，但要求收窄为A-lite。**

不要现在执行完整Phase 2B-2C。先做API Schema文档状态修正，再做Phase 2B契约决策与实现。Phase 2C等2B完成后单独评审，特别是先决定是否真的引入Celery beat。

**文档编号：** 60  
**状态：** Codex建议修改后执行

exec
/bin/bash -lc "rtk sed -n '1,320p' backend/apps/notifications/services.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
"""
Notification service layer for idempotent notification creation.

This module provides business logic for creating notifications automatically
when key events occur (application submission, approval decisions).
"""

from django.contrib.auth import get_user_model
from .models import Notification, NotificationType
from apps.approvals.models import ApprovalDecision

User = get_user_model()


def notify_application_submitted(application, approval):
    """
    Create notification for counselor when student submits application.

    Args:
        application: Application instance
        approval: Counselor approval instance

    Returns:
        tuple: (Notification instance, created boolean)
    """
    title = "新的离校申请"
    message = f"学生{application.student_name}（{application.student.user_id}）提交了离校申请，请及时审批。"

    return Notification.objects.get_or_create(
        recipient=approval.approver,
        entity_type='approval',
        entity_id=approval.pk,
        type=NotificationType.APPLICATION_SUBMITTED,
        defaults={
            'actor': application.student,
            'title': title,
            'message': message
        }
    )


def notify_approval_decided(approval):
    """
    Create notification for student when approval is approved or rejected.

    Args:
        approval: Approval instance with decision

    Returns:
        tuple: (Notification instance, created boolean)
    """
    approver_role = "辅导员" if approval.step == "counselor" else "学工部"

    if approval.decision == ApprovalDecision.APPROVED:
        title = "审批通过"
        message = f"您的离校申请已通过{approver_role}审批。"
        notification_type = NotificationType.APPROVAL_APPROVED
    else:  # rejected
        title = "审批驳回"
        message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
        notification_type = NotificationType.APPROVAL_REJECTED

    return Notification.objects.get_or_create(
        recipient=approval.application.student,
        entity_type='approval',
        entity_id=approval.pk,
        type=notification_type,
        defaults={
            'actor': approval.approver,
            'title': title,
            'message': message
        }
    )

codex
The current implementation confirms the mismatch: the blocked path returns `422` before creating an `Application`, while the notification model’s idempotency constraint is tied to a concrete `(recipient, entity_type, entity_id, type)` event. I’m checking provider behavior and line numbers now so the review can be specific.
exec
/bin/bash -lc "rtk nl -ba backend/apps/notifications/models.py | sed -n '1,140p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	import string
     2	import random
     3	from django.db import models
     4	from django.conf import settings
     5	
     6	
     7	def generate_notification_id():
     8	    """生成格式为 not_xxxxxxxx 的通知ID"""
     9	    chars = string.ascii_lowercase + string.digits
    10	    random_str = ''.join(random.choices(chars, k=8))
    11	    return f'not_{random_str}'
    12	
    13	
    14	class NotificationType(models.TextChoices):
    15	    APPLICATION_SUBMITTED = 'application_submitted', '申请已提交'
    16	    APPROVAL_APPROVED = 'approval_approved', '审批通过'
    17	    APPROVAL_REJECTED = 'approval_rejected', '审批驳回'
    18	    DORM_CLEARANCE_BLOCKED = 'dorm_clearance_blocked', '宿舍清退阻断'
    19	    APPROVAL_TIMEOUT_WARNING = 'approval_timeout_warning', '审批超时提醒'
    20	
    21	
    22	class EntityType(models.TextChoices):
    23	    APPLICATION = 'application', '离校申请'
    24	    APPROVAL = 'approval', '审批记录'
    25	
    26	
    27	class Notification(models.Model):
    28	    notification_id = models.CharField(
    29	        max_length=12,
    30	        primary_key=True,
    31	        default=generate_notification_id,
    32	        editable=False,
    33	        verbose_name='通知ID'
    34	    )
    35	    recipient = models.ForeignKey(
    36	        settings.AUTH_USER_MODEL,
    37	        on_delete=models.PROTECT,
    38	        related_name='notifications_received',
    39	        verbose_name='接收者'
    40	    )
    41	    actor = models.ForeignKey(
    42	        settings.AUTH_USER_MODEL,
    43	        on_delete=models.PROTECT,
    44	        related_name='notifications_triggered',
    45	        null=True,
    46	        blank=True,
    47	        verbose_name='触发者'
    48	    )
    49	    type = models.CharField(
    50	        max_length=50,
    51	        choices=NotificationType.choices,
    52	        verbose_name='通知类型'
    53	    )
    54	    entity_type = models.CharField(
    55	        max_length=50,
    56	        choices=EntityType.choices,
    57	        verbose_name='实体类型'
    58	    )
    59	    entity_id = models.CharField(
    60	        max_length=50,
    61	        verbose_name='实体ID'
    62	    )
    63	    title = models.CharField(
    64	        max_length=200,
    65	        verbose_name='标题'
    66	    )
    67	    message = models.TextField(
    68	        verbose_name='消息内容'
    69	    )
    70	    read_at = models.DateTimeField(
    71	        null=True,
    72	        blank=True,
    73	        verbose_name='已读时间'
    74	    )
    75	    created_at = models.DateTimeField(
    76	        auto_now_add=True,
    77	        verbose_name='创建时间'
    78	    )
    79	
    80	    class Meta:
    81	        db_table = 'notifications'
    82	        verbose_name = '通知'
    83	        verbose_name_plural = '通知'
    84	        ordering = ['-created_at']
    85	        indexes = [
    86	            models.Index(fields=['recipient', 'created_at']),
    87	            models.Index(fields=['recipient', 'read_at']),
    88	        ]
    89	        constraints = [
    90	            models.UniqueConstraint(
    91	                fields=['recipient', 'entity_type', 'entity_id', 'type'],
    92	                name='unique_notification_per_recipient_entity'
    93	            )
    94	        ]
    95	
    96	    def __str__(self):
    97	        return f'{self.notification_id}: {self.title}'

exec
/bin/bash -lc 'rtk rg -n "class MockDorm|DORM|dorm|DormCheckout" backend/apps docs/api tests -S' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/applications/admin.py:8:    list_filter = ['status', 'dorm_checkout_status']
backend/apps/applications/providers.py:3:from .models import DormCheckoutStatus
backend/apps/applications/providers.py:7:class DormCheckoutStatusDTO:
backend/apps/applications/providers.py:15:class MockDormCheckoutProvider:
backend/apps/applications/providers.py:16:    def check_status(self, student_id: str) -> DormCheckoutStatusDTO:
backend/apps/applications/providers.py:18:            "2020001": DormCheckoutStatusDTO(
backend/apps/applications/providers.py:20:                status=DormCheckoutStatus.COMPLETED,
backend/apps/applications/providers.py:25:            "2020002": DormCheckoutStatusDTO(
backend/apps/applications/providers.py:27:                status=DormCheckoutStatus.COMPLETED,
backend/apps/applications/providers.py:32:            "2020003": DormCheckoutStatusDTO(
backend/apps/applications/providers.py:34:                status=DormCheckoutStatus.NOT_STARTED,
backend/apps/applications/providers.py:39:            "2020006": DormCheckoutStatusDTO(
backend/apps/applications/providers.py:41:                status=DormCheckoutStatus.COMPLETED,
backend/apps/applications/providers.py:46:            "2020099": DormCheckoutStatusDTO(
backend/apps/applications/providers.py:48:                status=DormCheckoutStatus.UNKNOWN,
backend/apps/applications/providers.py:55:        return mock_data.get(student_id, DormCheckoutStatusDTO(
backend/apps/applications/providers.py:57:            status=DormCheckoutStatus.NOT_STARTED,
docs/api/notification-contract-v0.1.md:36:| 宿舍清退阻断 | DORM_CLEARANCE_BLOCKED | 宿舍清退未完成阻断申请 | 学生 |
docs/api/notification-contract-v0.1.md:89:#### DORM_CLEARANCE_BLOCKED（宿舍清退阻断）
docs/api/contract-v0.2.md:43:### 1.4 DormCheckoutStatus
docs/api/contract-v0.2.md:188:| `DORM_BLOCKED` | 422 | Dorm checkout incomplete | Blocking condition |
docs/api/contract-v0.2.md:376:### 6.5 DORM_BLOCKED (422)
docs/api/contract-v0.2.md:396:    "code": "DORM_BLOCKED",
docs/api/contract-v0.2.md:400:      "dorm_status": "pending",
docs/api/contract-v0.2.md:435:  "dorm_checkout_status": "completed",
docs/api/contract-v0.2.md:471:  "dorm_checkout_status": "completed",
docs/api/contract-v0.3.md:22:  - `attachment_type`: String (required) - one of: `dorm_checkout`, `library_clearance`, `finance_clearance`, `other`
docs/api/contract-v0.3.md:28:  "attachment_type": "dorm_checkout",
docs/api/contract-v0.3.md:56:      "attachment_type": "dorm_checkout",
backend/apps/attachments/migrations/0001_initial.py:23:                ('attachment_type', models.CharField(choices=[('dorm_checkout', '宿舍清退证明'), ('library_clearance', '图书馆清书证明'), ('finance_clearance', '财务结清证明'), ('other', '其他')], max_length=50)),
backend/apps/applications/migrations/0001_initial.py:23:                ('dorm_checkout_status', models.CharField(choices=[('completed', '已清退'), ('pending', '清退中'), ('not_started', '未开始'), ('unknown', '状态未知')], default='not_started', max_length=20)),
docs/api/contract-v0.3-skeleton.md:21:  - `attachment_type`: String (required) - one of: `dorm_checkout`, `library_clearance`, `finance_clearance`, `other`
docs/api/contract-v0.3-skeleton.md:29:  "attachment_type": "dorm_checkout",
docs/api/contract-v0.3-skeleton.md:59:      "attachment_type": "dorm_checkout",
backend/apps/applications/serializers.py:24:                  'reason', 'leave_date', 'status', 'dorm_checkout_status',
backend/apps/applications/serializers.py:27:                            'class_id', 'status', 'dorm_checkout_status',
backend/apps/applications/models.py:14:class DormCheckoutStatus(models.TextChoices):
backend/apps/applications/models.py:29:    dorm_checkout_status = models.CharField(max_length=20, choices=DormCheckoutStatus.choices, default=DormCheckoutStatus.NOT_STARTED)
backend/apps/applications/tests/test_error_cases.py:61:    def test_dorm_blocked_error(self):
backend/apps/applications/tests/test_error_cases.py:75:        self.assertEqual(response.data['error']['code'], 'DORM_BLOCKED')
backend/apps/applications/views.py:8:from .models import Application, ApplicationStatus, DormCheckoutStatus
backend/apps/applications/views.py:11:from .providers import MockDormCheckoutProvider
backend/apps/applications/views.py:134:    provider = MockDormCheckoutProvider()
backend/apps/applications/views.py:135:    dorm_status = provider.check_status(user.user_id)
backend/apps/applications/views.py:137:    if dorm_status.status != DormCheckoutStatus.COMPLETED:
backend/apps/applications/views.py:138:        return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
backend/apps/applications/views.py:139:                                    'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
backend/apps/applications/views.py:140:                                                'blocking_reason': dorm_status.blocking_reason}}},
backend/apps/applications/views.py:158:        dorm_checkout_status=dorm_status.status
backend/apps/attachments/models.py:7:    DORM_CHECKOUT = 'dorm_checkout', '宿舍清退证明'
backend/apps/attachments/tests/test_download.py:71:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_upload.py:84:                'attachment_type': AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_upload.py:94:        self.assertEqual(response.data['attachment_type'], AttachmentType.DORM_CHECKOUT)
backend/apps/attachments/tests/test_upload.py:106:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:123:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_upload.py:138:                'attachment_type': AttachmentType.DORM_CHECKOUT
backend/apps/attachments/tests/test_delete.py:70:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/attachments/tests/test_list.py:92:            attachment_type=AttachmentType.DORM_CHECKOUT,
backend/apps/notifications/models.py:18:    DORM_CLEARANCE_BLOCKED = 'dorm_clearance_blocked', '宿舍清退阻断'
backend/apps/notifications/tests/test_auto_notifications_api.py:229:    def test_dorm_blocked_does_not_create_notification(self):
backend/apps/notifications/tests/test_auto_notifications_api.py:230:        """Test that dorm checkout blockage does not create notifications."""
backend/apps/notifications/tests/test_auto_notifications_api.py:231:        # Create student with non-completed dorm status (use ID not in mock data)
backend/apps/notifications/tests/test_auto_notifications_api.py:239:        # Student tries to submit application (should fail with 422 dorm blocked)
backend/apps/notifications/migrations/0001_initial.py:22:                ('type', models.CharField(choices=[('application_submitted', '申请已提交'), ('approval_approved', '审批通过'), ('approval_rejected', '审批驳回'), ('dorm_clearance_blocked', '宿舍清退阻断'), ('approval_timeout_warning', '审批超时提醒')], max_length=50, verbose_name='通知类型')),

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/views.py | sed -n '80,170p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
    80	        pending_approvals = Approval.objects.filter(
    81	            approver=user,
    82	            step=ApprovalStep.DEAN,
    83	            decision=ApprovalDecision.PENDING
    84	        ).values_list('application', flat=True)
    85	        queryset = Application.objects.filter(pk__in=pending_approvals)
    86	
    87	    else:
    88	        return Response(
    89	            {'error': {'code': 'FORBIDDEN', 'message': '无效的用户角色'}},
    90	            status=status.HTTP_403_FORBIDDEN
    91	        )
    92	
    93	    # Status filtering
    94	    status_param = request.query_params.get('status')
    95	    if status_param:
    96	        queryset = queryset.filter(status=status_param)
    97	
    98	    # Sort by created_at DESC
    99	    queryset = queryset.order_by('-created_at', '-application_id')
   100	
   101	    # Paginate
   102	    paginator = ApplicationLimitOffsetPagination()
   103	    page = paginator.paginate_queryset(queryset, request)
   104	
   105	    # Serialize
   106	    serializer = ApplicationListSerializer(page, many=True)
   107	
   108	    return paginator.get_paginated_response(serializer.data)
   109	
   110	
   111	def create_application(request):
   112	    user = request.user
   113	
   114	    if user.role != UserRole.STUDENT:
   115	        return Response({'error': {'code': 'FORBIDDEN', 'message': '只有学生可以提交申请'}},
   116	                        status=status.HTTP_403_FORBIDDEN)
   117	
   118	    # Check for existing pending/approved applications
   119	    existing = Application.objects.filter(
   120	        student=user,
   121	        status__in=[ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.PENDING_DEAN, ApplicationStatus.APPROVED]
   122	    ).first()
   123	    if existing:
   124	        return Response({'error': {'code': 'CONFLICT', 'message': '已有待审批或已通过的申请，不能重复提交',
   125	                                    'details': {'student_id': user.user_id, 'existing_application_id': existing.application_id, 'status': existing.status}}},
   126	                        status=status.HTTP_409_CONFLICT)
   127	
   128	    serializer = ApplicationCreateSerializer(data=request.data)
   129	    if not serializer.is_valid():
   130	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
   131	                                    'details': serializer.errors}},
   132	                        status=status.HTTP_400_BAD_REQUEST)
   133	
   134	    provider = MockDormCheckoutProvider()
   135	    dorm_status = provider.check_status(user.user_id)
   136	
   137	    if dorm_status.status != DormCheckoutStatus.COMPLETED:
   138	        return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
   139	                                    'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
   140	                                                'blocking_reason': dorm_status.blocking_reason}}},
   141	                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
   142	
   143	    try:
   144	        class_mapping = ClassMapping.objects.get(class_id=user.class_id, active=True)
   145	    except ClassMapping.DoesNotExist:
   146	        return Response({'error': {'code': 'NOT_FOUND', 'message': '班级映射不存在',
   147	                                    'details': {'class_id': user.class_id}}},
   148	                        status=status.HTTP_404_NOT_FOUND)
   149	
   150	    application = Application.objects.create(
   151	        application_id=f'app_{uuid.uuid4().hex[:8]}',
   152	        student=user,
   153	        student_name=user.name,
   154	        class_id=user.class_id,
   155	        reason=serializer.validated_data['reason'],
   156	        leave_date=serializer.validated_data['leave_date'],
   157	        status=ApplicationStatus.PENDING_COUNSELOR,
   158	        dorm_checkout_status=dorm_status.status
   159	    )
   160	
   161	    counselor_approval = Approval.objects.create(
   162	        approval_id=f'apv_{uuid.uuid4().hex[:8]}',
   163	        application=application,
   164	        step=ApprovalStep.COUNSELOR,
   165	        approver=class_mapping.counselor,
   166	        approver_name=class_mapping.counselor_name,
   167	        decision=ApprovalDecision.PENDING
   168	    )
   169	
   170	    notify_application_submitted(application, counselor_approval)

exec
/bin/bash -lc "rtk nl -ba backend/apps/notifications/services.py | sed -n '1,180p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	"""
     2	Notification service layer for idempotent notification creation.
     3	
     4	This module provides business logic for creating notifications automatically
     5	when key events occur (application submission, approval decisions).
     6	"""
     7	
     8	from django.contrib.auth import get_user_model
     9	from .models import Notification, NotificationType
    10	from apps.approvals.models import ApprovalDecision
    11	
    12	User = get_user_model()
    13	
    14	
    15	def notify_application_submitted(application, approval):
    16	    """
    17	    Create notification for counselor when student submits application.
    18	
    19	    Args:
    20	        application: Application instance
    21	        approval: Counselor approval instance
    22	
    23	    Returns:
    24	        tuple: (Notification instance, created boolean)
    25	    """
    26	    title = "新的离校申请"
    27	    message = f"学生{application.student_name}（{application.student.user_id}）提交了离校申请，请及时审批。"
    28	
    29	    return Notification.objects.get_or_create(
    30	        recipient=approval.approver,
    31	        entity_type='approval',
    32	        entity_id=approval.pk,
    33	        type=NotificationType.APPLICATION_SUBMITTED,
    34	        defaults={
    35	            'actor': application.student,
    36	            'title': title,
    37	            'message': message
    38	        }
    39	    )
    40	
    41	
    42	def notify_approval_decided(approval):
    43	    """
    44	    Create notification for student when approval is approved or rejected.
    45	
    46	    Args:
    47	        approval: Approval instance with decision
    48	
    49	    Returns:
    50	        tuple: (Notification instance, created boolean)
    51	    """
    52	    approver_role = "辅导员" if approval.step == "counselor" else "学工部"
    53	
    54	    if approval.decision == ApprovalDecision.APPROVED:
    55	        title = "审批通过"
    56	        message = f"您的离校申请已通过{approver_role}审批。"
    57	        notification_type = NotificationType.APPROVAL_APPROVED
    58	    else:  # rejected
    59	        title = "审批驳回"
    60	        message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
    61	        notification_type = NotificationType.APPROVAL_REJECTED
    62	
    63	    return Notification.objects.get_or_create(
    64	        recipient=approval.application.student,
    65	        entity_type='approval',
    66	        entity_id=approval.pk,
    67	        type=notification_type,
    68	        defaults={
    69	            'actor': approval.approver,
    70	            'title': title,
    71	            'message': message
    72	        }
    73	    )

exec
/bin/bash -lc "rtk nl -ba backend/apps/applications/models.py | sed -n '1,90p'" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk nl -ba backend/apps/notifications/tests/test_auto_notifications_api.py | sed -n '220,260p'" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk nl -ba docs/api/notification-contract-v0.1.md | sed -n '25,120p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   220	        self.assertEqual(response.status_code, 409)
   221	
   222	        # Verify only one notification exists (from initial approval, not from failed re-approval)
   223	        self.assertEqual(Notification.objects.filter(
   224	            recipient=self.student,
   225	            entity_type='approval',
   226	            entity_id=approval.pk
   227	        ).count(), 0)  # No notification because we created approval directly, not through API
   228	
   229	    def test_dorm_blocked_does_not_create_notification(self):
   230	        """Test that dorm checkout blockage does not create notifications."""
   231	        # Create student with non-completed dorm status (use ID not in mock data)
   232	        blocked_student = User.objects.create_user(
   233	            user_id='2021999',
   234	            name='被阻断学生',
   235	            role='student',
   236	            class_id='CS2021-1'
   237	        )
   238	
   239	        # Student tries to submit application (should fail with 422 dorm blocked)
   240	        self.client.force_authenticate(user=blocked_student)
   241	        response = self.client.post('/api/applications/', {
   242	            'reason': '毕业离校',
   243	            'leave_date': '2026-07-01'
   244	        })
   245	        self.assertEqual(response.status_code, 422)
   246	
   247	        # Verify no notification was created for counselor
   248	        self.assertEqual(Notification.objects.filter(
   249	            recipient=self.counselor,
   250	            type='application_submitted'
   251	        ).count(), 0)

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

 succeeded in 0ms:
    25	---
    26	
    27	## 2. 通知事件类型
    28	
    29	### 2.1 事件枚举
    30	
    31	| 事件类型 | 枚举值 | 触发时机 | 接收者 |
    32	|---------|--------|----------|--------|
    33	| 申请提交 | APPLICATION_SUBMITTED | 学生提交离校申请 | 辅导员 |
    34	| 审批通过 | APPROVAL_APPROVED | 辅导员/学工部审批通过 | 学生 |
    35	| 审批驳回 | APPROVAL_REJECTED | 辅导员/学工部驳回申请 | 学生 |
    36	| 宿舍清退阻断 | DORM_CLEARANCE_BLOCKED | 宿舍清退未完成阻断申请 | 学生 |
    37	| 审批超时提醒 | APPROVAL_TIMEOUT_WARNING | 审批超过时限未处理 | 辅导员/学工部 |
    38	
    39	### 2.2 事件详细说明
    40	
    41	#### APPLICATION_SUBMITTED（申请提交）
    42	
    43	**触发条件：** 学生成功提交离校申请
    44	
    45	**接收者：** 该学生的辅导员
    46	
    47	**通知内容：**
    48	- 标题：`新的离校申请`
    49	- 正文：`学生{student_name}（{student_id}）提交了离校申请，请及时审批。`
    50	
    51	**关联实体：**
    52	- entity_type: `application`
    53	- entity_id: `{application_id}`
    54	
    55	---
    56	
    57	#### APPROVAL_APPROVED（审批通过）
    58	
    59	**触发条件：** 辅导员或学工部审批通过
    60	
    61	**接收者：** 申请学生
    62	
    63	**通知内容：**
    64	- 标题：`审批通过`
    65	- 正文：`您的离校申请已通过{approver_role}审批。` （approver_role: 辅导员/学工部）
    66	
    67	**关联实体：**
    68	- entity_type: `approval`
    69	- entity_id: `{approval_id}`
    70	
    71	---
    72	
    73	#### APPROVAL_REJECTED（审批驳回）
    74	
    75	**触发条件：** 辅导员或学工部驳回申请
    76	
    77	**接收者：** 申请学生
    78	
    79	**通知内容：**
    80	- 标题：`审批驳回`
    81	- 正文：`您的离校申请被{approver_role}驳回。驳回原因：{comment}`
    82	
    83	**关联实体：**
    84	- entity_type: `approval`
    85	- entity_id: `{approval_id}`
    86	
    87	---
    88	
    89	#### DORM_CLEARANCE_BLOCKED（宿舍清退阻断）
    90	
    91	**触发条件：** 宿舍管理系统返回清退未完成
    92	
    93	**接收者：** 申请学生
    94	
    95	**通知内容：**
    96	- 标题：`宿舍清退未完成`
    97	- 正文：`您的离校申请因宿舍清退未完成而被阻断，请先完成宿舍清退手续。`
    98	
    99	**关联实体：**
   100	- entity_type: `application`
   101	- entity_id: `{application_id}`
   102	
   103	---
   104	
   105	#### APPROVAL_TIMEOUT_WARNING（审批超时提醒）
   106	
   107	**触发条件：** 审批超过规定时限（辅导员3工作日，学工部2工作日）未处理
   108	
   109	**接收者：** 待审批的辅导员/学工部
   110	
   111	**通知内容：**
   112	- 标题：`审批超时提醒`
   113	- 正文：`学生{student_name}的离校申请已超过{days}个工作日未审批，请及时处理。`
   114	
   115	**关联实体：**
   116	- entity_type: `approval`
   117	- entity_id: `{approval_id}`
   118	
   119	---
   120	

exec
/bin/bash -lc "rtk sed -n '1,120p' backend/apps/applications/providers.py" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
from dataclasses import dataclass
from typing import Optional
from .models import DormCheckoutStatus


@dataclass
class DormCheckoutStatusDTO:
    student_id: str
    status: str
    checked_at: Optional[str]
    blocking_reason: Optional[str]
    provider_error_code: Optional[str]


class MockDormCheckoutProvider:
    def check_status(self, student_id: str) -> DormCheckoutStatusDTO:
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
                status=DormCheckoutStatus.COMPLETED,
                checked_at="2024-05-15T10:15:00Z",
                blocking_reason=None,
                provider_error_code=None
            ),
            "2020003": DormCheckoutStatusDTO(
                student_id="2020003",
                status=DormCheckoutStatus.NOT_STARTED,
                checked_at=None,
                blocking_reason="未提交清退申请",
                provider_error_code=None
            ),
            "2020006": DormCheckoutStatusDTO(
                student_id="2020006",
                status=DormCheckoutStatus.COMPLETED,
                checked_at="2024-05-15T10:30:00Z",
                blocking_reason=None,
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

        return mock_data.get(student_id, DormCheckoutStatusDTO(
            student_id=student_id,
            status=DormCheckoutStatus.NOT_STARTED,
            checked_at=None,
            blocking_reason="未在宿舍系统中找到记录",
            provider_error_code=None
        ))

exec
/bin/bash -lc 'rtk ls -1 docs/discussions/phase4c-next-steps | tail -n 20' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-47-claude-post-step2-nex-2026-06-01T17-57-59-267Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-47-claude-post-step2-nex-2026-06-01T18-03-30-703Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-50-claude-post-option-e--2026-06-01T18-13-55-411Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-52-claude-response-optio-2026-06-01T18-20-09-573Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-55-claude-post-api-schem-2026-06-01T18-53-35-201Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-58-claude-codex-consensu-2026-06-01T19-03-31-790Z.md
?? .omc/artifacts/ask/codex-docs-discussions-phase4c-next-steps-59-claude-codex-final-co-2026-06-01T19-10-22-958Z.md
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
?? backend/apps/approvals/validators.py
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
codex
I’m going to save the review as the next numbered discussion document. The key decision I’m leaning to is: keep the current synchronous `422` behavior for v0.1, remove/defer this notification from the automatic notification contract, and only create a separate dorm block record later if product requires persistent notification history.
apply patch
patch: completed
/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md
diff --git a/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md b/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..20cd44f26a573c989807c24d9bc7453deb177957
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md
@@ -0,0 +1,183 @@
+# Phase 2B契约决策 - Codex审查响应
+
+**日期：** 2026-06-02  
+**审查人：** Codex  
+**类型：** 契约决策审查响应  
+**针对：** 62-phase2b-contract-decision-review-request.md
+
+---
+
+## 审查结论
+
+**建议当前采用 Option 1：不为宿舍阻断创建通知，将 `DORM_CLEARANCE_BLOCKED` 从 v0.1 自动通知契约中删除或标记为 deferred。**
+
+理由：当前宿舍阻断是申请提交接口的同步校验失败，而不是已创建业务实体上的状态变更。`create_application` 在宿舍未清退时直接返回 `422`，不会创建 `Application`；通知模型又要求幂等键绑定明确实体。因此在不新增实体的前提下创建通知，会破坏 `entity_id` 语义。
+
+如果产品明确要求“通知中心可回看宿舍阻断原因”，再采用 Option 2 的独立 `DormClearanceBlock` / `DormBlockRecord` 表。不要优先使用 blocked application，也不建议使用 `student_id` 伪装业务事件实体。
+
+---
+
+## 发现的问题
+
+### 问题1：当前不能按契约创建宿舍阻断通知 [P1]
+
+**位置：**
+- `docs/api/notification-contract-v0.1.md:89`
+- `docs/api/notification-contract-v0.1.md:99`
+- `backend/apps/applications/views.py:137`
+- `backend/apps/applications/views.py:150`
+
+契约要求 `DORM_CLEARANCE_BLOCKED` 关联 `application_id`，但代码在宿舍状态非 `completed` 时直接返回 `422`，`Application.objects.create(...)` 在后续分支才执行。也就是说阻断路径没有合法 `application_id`。
+
+**建议：** v0.1中删除该自动通知承诺，或在事件表中标记为 deferred：当前仅通过 `POST /api/applications/` 的 `422 DORM_BLOCKED` 响应告知学生。
+
+### 问题2：blocked application会污染申请状态机 [P1]
+
+**位置：**
+- `backend/apps/applications/models.py:6`
+- `backend/apps/applications/models.py:21`
+- `backend/apps/applications/views.py:118`
+
+如果为阻断创建 `Application(status=blocked)`，需要重新定义列表展示、重复提交限制、审批流创建条件、可见性、统计口径和清退后重提行为。它不是单纯新增一个状态，会让“申请”同时表达“已提交审批对象”和“提交失败尝试”两种语义。
+
+**建议：** 如果必须持久化阻断事件，优先新建独立表，不要把阻断塞进 `Application`。
+
+### 问题3：使用 `student_id` 作为通知实体会让幂等语义过粗 [P1]
+
+**位置：**
+- `backend/apps/notifications/models.py:89`
+
+当前唯一约束是 `(recipient, entity_type, entity_id, type)`。如果 `entity_type=student` 且 `entity_id=student_id`，同一个学生未来所有宿舍阻断都会折叠成同一条通知，无法表达不同阻断记录、不同原因或清退后再次阻断。
+
+**建议：** 不选 Option 3。除非引入真正的 `DormClearanceBlock` 记录，否则不要创建该通知。
+
+### 问题4：通知契约还有一个相邻不一致点，应一并修正 [P2]
+
+**位置：**
+- `docs/api/notification-contract-v0.1.md:51`
+- `backend/apps/notifications/services.py:29`
+
+契约写 `APPLICATION_SUBMITTED` 关联 `application`，但服务实际用 `entity_type='approval'`、`entity_id=approval.pk` 创建通知。考虑接收者是辅导员，通知入口要处理的是待审批记录，当前实现使用 `approval` 更合理。
+
+**建议：** 本次修订 `notification-contract-v0.1.md` 时一并把 `APPLICATION_SUBMITTED` 的关联实体改为 `approval/{approval_id}`，避免后续 Phase 2B 文档只修宿舍阻断而留下旧冲突。
+
+---
+
+## 对审查要点的回答
+
+### 1. 推荐选项
+
+推荐 **Option 1** 作为当前 v0.1 / A-lite 决策：
+
+- 保留 `422 DORM_BLOCKED` 同步响应。
+- 不创建通知。
+- `notification-contract-v0.1.md` 删除 `DORM_CLEARANCE_BLOCKED`，或保留在“Deferred / 后续版本”章节。
+- 当前测试 `test_dorm_blocked_does_not_create_notification` 的方向保持正确，但断言应强化为“学生和辅导员都没有宿舍阻断/申请提交通知”。
+
+### 2. 如果选 Option 2，实体设计怎么做
+
+如果产品必须要通知中心留痕，建议独立表，不建议 blocked application。
+
+建议表意：
+
+```text
+DormClearanceBlock
+- block_id: blk_xxxxxxxx, primary key
+- student: FK(User)
+- dorm_status
+- blocking_reason
+- provider_error_code
+- checked_at
+- last_attempt_at
+- resolved_at nullable
+- created_at
+```
+
+通知使用：
+
+```text
+type = dorm_clearance_blocked
+entity_type = dorm_clearance_block
+entity_id = block_id
+recipient = student
+```
+
+这样通知有合法业务实体，且不会污染申请审批状态机。
+
+### 3. 如果选 Option 3，如何防重复
+
+不推荐 Option 3。若临时采用，至少不要修改唯一约束；当前唯一约束已包含 `type`。但必须接受一个后果：同一学生的宿舍阻断通知会长期只有一条。
+
+更好的折中不是扩大幂等键，而是新增阻断记录实体。把 `student_id + dorm_status + blocking_reason + unresolved` 归并到一个 open block record，再由通知引用该 record。
+
+### 4. 测试如何调整
+
+采用 Option 1：
+
+- 保留并改名为 `test_dorm_blocked_returns_422_without_notification`。
+- 断言响应 `error.code == DORM_BLOCKED`。
+- 断言 `Application.objects.filter(student=blocked_student).count() == 0`。
+- 断言 `Notification.objects.filter(recipient=blocked_student).count() == 0`。
+- 保留辅导员没有 `application_submitted` 通知的断言。
+
+采用 Option 2：
+
+- 将原测试改为断言创建 `DormClearanceBlock` 和一条学生通知。
+- 断言不创建 `Application` 和 `Approval`。
+- 连续提交两次时，通知数量仍为1，阻断记录可更新 `last_attempt_at`。
+- 断言辅导员不收到通知。
+
+### 5. 契约如何修正
+
+采用 Option 1 时，建议修订：
+
+- 事件枚举移除 `DORM_CLEARANCE_BLOCKED`，或移动到 `Deferred events`。
+- 删除详细事件说明中的 `entity_type: application / entity_id: application_id`。
+- 在非目标或说明中写明：宿舍阻断当前是申请提交接口的同步错误响应，不进入通知中心。
+- 同步修正 `APPLICATION_SUBMITTED` 的实体为 `approval/{approval_id}`，匹配现有服务实现。
+
+### 6. 影响文件清单
+
+Option 1 最小修改：
+
+- `docs/api/notification-contract-v0.1.md`
+- `backend/apps/notifications/tests/test_auto_notifications_api.py`
+
+Option 2 独立表修改：
+
+- `backend/apps/applications/models.py` 或新增 `backend/apps/dormitory/models.py`
+- 对应 migration
+- `backend/apps/applications/views.py`
+- `backend/apps/notifications/models.py`
+- `backend/apps/notifications/services.py`
+- `backend/apps/notifications/tests/test_auto_notifications_api.py`
+- `docs/api/notification-contract-v0.1.md`
+- 如暴露阻断记录 API，再更新 schema/serializer/urls
+
+Option 3 修改：
+
+- `backend/apps/notifications/models.py`
+- migration
+- `backend/apps/notifications/services.py`
+- `backend/apps/applications/views.py`
+- `backend/apps/notifications/tests/test_auto_notifications_api.py`
+- `docs/api/notification-contract-v0.1.md`
+
+### 7. 实现风险评估
+
+Option 1风险最低。主要风险是产品体验较弱，但当前用户已经在提交动作中即时收到明确错误，且该事件不是异步通知的强需求。
+
+Option 2风险中等。独立表方案语义清楚，但会增加数据模型、迁移、测试和后续清退状态同步问题。只有在“通知中心留痕”是明确产品需求时才值得做。
+
+Option 3风险最高。实现看似简单，但实体语义弱，幂等粒度粗，会给后续审计、重复阻断、原因变化和数据解释留下债务。
+
+---
+
+## 最终建议
+
+Phase 2B不要直接实现宿舍阻断通知。当前应把 Phase 2B 定义为“契约修正优先”：从 v0.1 自动通知范围中移除或 defer `DORM_CLEARANCE_BLOCKED`，保持同步 `422` 阻断行为，并加强现有负路径测试。
+
+如果后续要做“宿舍阻断通知中心留痕”，先单独立项 `DormClearanceBlock` 实体，再基于该实体创建通知。
+
+**文档编号：** 63  
+**状态：** Codex建议采用 Option 1；Option 2仅作为后续产品需求成立时的扩展方案

diff --git a/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md b/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..20cd44f26a573c989807c24d9bc7453deb177957
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md
@@ -0,0 +1,183 @@
+# Phase 2B契约决策 - Codex审查响应
+
+**日期：** 2026-06-02  
+**审查人：** Codex  
+**类型：** 契约决策审查响应  
+**针对：** 62-phase2b-contract-decision-review-request.md
+
+---
+
+## 审查结论
+
+**建议当前采用 Option 1：不为宿舍阻断创建通知，将 `DORM_CLEARANCE_BLOCKED` 从 v0.1 自动通知契约中删除或标记为 deferred。**
+
+理由：当前宿舍阻断是申请提交接口的同步校验失败，而不是已创建业务实体上的状态变更。`create_application` 在宿舍未清退时直接返回 `422`，不会创建 `Application`；通知模型又要求幂等键绑定明确实体。因此在不新增实体的前提下创建通知，会破坏 `entity_id` 语义。
+
+如果产品明确要求“通知中心可回看宿舍阻断原因”，再采用 Option 2 的独立 `DormClearanceBlock` / `DormBlockRecord` 表。不要优先使用 blocked application，也不建议使用 `student_id` 伪装业务事件实体。
+
+---
+
+## 发现的问题
+
+### 问题1：当前不能按契约创建宿舍阻断通知 [P1]
+
+**位置：**
+- `docs/api/notification-contract-v0.1.md:89`
+- `docs/api/notification-contract-v0.1.md:99`
+- `backend/apps/applications/views.py:137`
+- `backend/apps/applications/views.py:150`
+
+契约要求 `DORM_CLEARANCE_BLOCKED` 关联 `application_id`，但代码在宿舍状态非 `completed` 时直接返回 `422`，`Application.objects.create(...)` 在后续分支才执行。也就是说阻断路径没有合法 `application_id`。
+
+**建议：** v0.1中删除该自动通知承诺，或在事件表中标记为 deferred：当前仅通过 `POST /api/applications/` 的 `422 DORM_BLOCKED` 响应告知学生。
+
+### 问题2：blocked application会污染申请状态机 [P1]
+
+**位置：**
+- `backend/apps/applications/models.py:6`
+- `backend/apps/applications/models.py:21`
+- `backend/apps/applications/views.py:118`
+
+如果为阻断创建 `Application(status=blocked)`，需要重新定义列表展示、重复提交限制、审批流创建条件、可见性、统计口径和清退后重提行为。它不是单纯新增一个状态，会让“申请”同时表达“已提交审批对象”和“提交失败尝试”两种语义。
+
+**建议：** 如果必须持久化阻断事件，优先新建独立表，不要把阻断塞进 `Application`。
+
+### 问题3：使用 `student_id` 作为通知实体会让幂等语义过粗 [P1]
+
+**位置：**
+- `backend/apps/notifications/models.py:89`
+
+当前唯一约束是 `(recipient, entity_type, entity_id, type)`。如果 `entity_type=student` 且 `entity_id=student_id`，同一个学生未来所有宿舍阻断都会折叠成同一条通知，无法表达不同阻断记录、不同原因或清退后再次阻断。
+
+**建议：** 不选 Option 3。除非引入真正的 `DormClearanceBlock` 记录，否则不要创建该通知。
+
+### 问题4：通知契约还有一个相邻不一致点，应一并修正 [P2]
+
+**位置：**
+- `docs/api/notification-contract-v0.1.md:51`
+- `backend/apps/notifications/services.py:29`
+
+契约写 `APPLICATION_SUBMITTED` 关联 `application`，但服务实际用 `entity_type='approval'`、`entity_id=approval.pk` 创建通知。考虑接收者是辅导员，通知入口要处理的是待审批记录，当前实现使用 `approval` 更合理。
+
+**建议：** 本次修订 `notification-contract-v0.1.md` 时一并把 `APPLICATION_SUBMITTED` 的关联实体改为 `approval/{approval_id}`，避免后续 Phase 2B 文档只修宿舍阻断而留下旧冲突。
+
+---
+
+## 对审查要点的回答
+
+### 1. 推荐选项
+
+推荐 **Option 1** 作为当前 v0.1 / A-lite 决策：
+
+- 保留 `422 DORM_BLOCKED` 同步响应。
+- 不创建通知。
+- `notification-contract-v0.1.md` 删除 `DORM_CLEARANCE_BLOCKED`，或保留在“Deferred / 后续版本”章节。
+- 当前测试 `test_dorm_blocked_does_not_create_notification` 的方向保持正确，但断言应强化为“学生和辅导员都没有宿舍阻断/申请提交通知”。
+
+### 2. 如果选 Option 2，实体设计怎么做
+
+如果产品必须要通知中心留痕，建议独立表，不建议 blocked application。
+
+建议表意：
+
+```text
+DormClearanceBlock
+- block_id: blk_xxxxxxxx, primary key
+- student: FK(User)
+- dorm_status
+- blocking_reason
+- provider_error_code
+- checked_at
+- last_attempt_at
+- resolved_at nullable
+- created_at
+```
+
+通知使用：
+
+```text
+type = dorm_clearance_blocked
+entity_type = dorm_clearance_block
+entity_id = block_id
+recipient = student
+```
+
+这样通知有合法业务实体，且不会污染申请审批状态机。
+
+### 3. 如果选 Option 3，如何防重复
+
+不推荐 Option 3。若临时采用，至少不要修改唯一约束；当前唯一约束已包含 `type`。但必须接受一个后果：同一学生的宿舍阻断通知会长期只有一条。
+
+更好的折中不是扩大幂等键，而是新增阻断记录实体。把 `student_id + dorm_status + blocking_reason + unresolved` 归并到一个 open block record，再由通知引用该 record。
+
+### 4. 测试如何调整
+
+采用 Option 1：
+
+- 保留并改名为 `test_dorm_blocked_returns_422_without_notification`。
+- 断言响应 `error.code == DORM_BLOCKED`。
+- 断言 `Application.objects.filter(student=blocked_student).count() == 0`。
+- 断言 `Notification.objects.filter(recipient=blocked_student).count() == 0`。
+- 保留辅导员没有 `application_submitted` 通知的断言。
+
+采用 Option 2：
+
+- 将原测试改为断言创建 `DormClearanceBlock` 和一条学生通知。
+- 断言不创建 `Application` 和 `Approval`。
+- 连续提交两次时，通知数量仍为1，阻断记录可更新 `last_attempt_at`。
+- 断言辅导员不收到通知。
+
+### 5. 契约如何修正
+
+采用 Option 1 时，建议修订：
+
+- 事件枚举移除 `DORM_CLEARANCE_BLOCKED`，或移动到 `Deferred events`。
+- 删除详细事件说明中的 `entity_type: application / entity_id: application_id`。
+- 在非目标或说明中写明：宿舍阻断当前是申请提交接口的同步错误响应，不进入通知中心。
+- 同步修正 `APPLICATION_SUBMITTED` 的实体为 `approval/{approval_id}`，匹配现有服务实现。
+
+### 6. 影响文件清单
+
+Option 1 最小修改：
+
+- `docs/api/notification-contract-v0.1.md`
+- `backend/apps/notifications/tests/test_auto_notifications_api.py`
+
+Option 2 独立表修改：
+
+- `backend/apps/applications/models.py` 或新增 `backend/apps/dormitory/models.py`
+- 对应 migration
+- `backend/apps/applications/views.py`
+- `backend/apps/notifications/models.py`
+- `backend/apps/notifications/services.py`
+- `backend/apps/notifications/tests/test_auto_notifications_api.py`
+- `docs/api/notification-contract-v0.1.md`
+- 如暴露阻断记录 API，再更新 schema/serializer/urls
+
+Option 3 修改：
+
+- `backend/apps/notifications/models.py`
+- migration
+- `backend/apps/notifications/services.py`
+- `backend/apps/applications/views.py`
+- `backend/apps/notifications/tests/test_auto_notifications_api.py`
+- `docs/api/notification-contract-v0.1.md`
+
+### 7. 实现风险评估
+
+Option 1风险最低。主要风险是产品体验较弱，但当前用户已经在提交动作中即时收到明确错误，且该事件不是异步通知的强需求。
+
+Option 2风险中等。独立表方案语义清楚，但会增加数据模型、迁移、测试和后续清退状态同步问题。只有在“通知中心留痕”是明确产品需求时才值得做。
+
+Option 3风险最高。实现看似简单，但实体语义弱，幂等粒度粗，会给后续审计、重复阻断、原因变化和数据解释留下债务。
+
+---
+
+## 最终建议
+
+Phase 2B不要直接实现宿舍阻断通知。当前应把 Phase 2B 定义为“契约修正优先”：从 v0.1 自动通知范围中移除或 defer `DORM_CLEARANCE_BLOCKED`，保持同步 `422` 阻断行为，并加强现有负路径测试。
+
+如果后续要做“宿舍阻断通知中心留痕”，先单独立项 `DormClearanceBlock` 实体，再基于该实体创建通知。
+
+**文档编号：** 63  
+**状态：** Codex建议采用 Option 1；Option 2仅作为后续产品需求成立时的扩展方案

codex
The response document is written. I’m doing a quick sanity pass over the saved artifact and the diff so I can report exactly what changed.
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Phase 2B契约决策 - Codex审查响应

**日期：** 2026-06-02  
**审查人：** Codex  
**类型：** 契约决策审查响应  
**针对：** 62-phase2b-contract-decision-review-request.md

---

## 审查结论

**建议当前采用 Option 1：不为宿舍阻断创建通知，将 `DORM_CLEARANCE_BLOCKED` 从 v0.1 自动通知契约中删除或标记为 deferred。**

理由：当前宿舍阻断是申请提交接口的同步校验失败，而不是已创建业务实体上的状态变更。`create_application` 在宿舍未清退时直接返回 `422`，不会创建 `Application`；通知模型又要求幂等键绑定明确实体。因此在不新增实体的前提下创建通知，会破坏 `entity_id` 语义。

如果产品明确要求“通知中心可回看宿舍阻断原因”，再采用 Option 2 的独立 `DormClearanceBlock` / `DormBlockRecord` 表。不要优先使用 blocked application，也不建议使用 `student_id` 伪装业务事件实体。

---

## 发现的问题

### 问题1：当前不能按契约创建宿舍阻断通知 [P1]

**位置：**
- `docs/api/notification-contract-v0.1.md:89`
- `docs/api/notification-contract-v0.1.md:99`
- `backend/apps/applications/views.py:137`
- `backend/apps/applications/views.py:150`

契约要求 `DORM_CLEARANCE_BLOCKED` 关联 `application_id`，但代码在宿舍状态非 `completed` 时直接返回 `422`，`Application.objects.create(...)` 在后续分支才执行。也就是说阻断路径没有合法 `application_id`。

**建议：** v0.1中删除该自动通知承诺，或在事件表中标记为 deferred：当前仅通过 `POST /api/applications/` 的 `422 DORM_BLOCKED` 响应告知学生。

### 问题2：blocked application会污染申请状态机 [P1]

**位置：**
- `backend/apps/applications/models.py:6`
- `backend/apps/applications/models.py:21`
- `backend/apps/applications/views.py:118`

如果为阻断创建 `Application(status=blocked)`，需要重新定义列表展示、重复提交限制、审批流创建条件、可见性、统计口径和清退后重提行为。它不是单纯新增一个状态，会让“申请”同时表达“已提交审批对象”和“提交失败尝试”两种语义。

**建议：** 如果必须持久化阻断事件，优先新建独立表，不要把阻断塞进 `Application`。

### 问题3：使用 `student_id` 作为通知实体会让幂等语义过粗 [P1]

**位置：**
- `backend/apps/notifications/models.py:89`

当前唯一约束是 `(recipient, entity_type, entity_id, type)`。如果 `entity_type=student` 且 `entity_id=student_id`，同一个学生未来所有宿舍阻断都会折叠成同一条通知，无法表达不同阻断记录、不同原因或清退后再次阻断。

**建议：** 不选 Option 3。除非引入真正的 `DormClearanceBlock` 记录，否则不要创建该通知。

### 问题4：通知契约还有一个相邻不一致点，应一并修正 [P2]

**位置：**
- `docs/api/notification-contract-v0.1.md:51`
- `backend/apps/notifications/services.py:29`

契约写 `APPLICATION_SUBMITTED` 关联 `application`，但服务实际用 `entity_type='approval'`、`entity_id=approval.pk` 创建通知。考虑接收者是辅导员，通知入口要处理的是待审批记录，当前实现使用 `approval` 更合理。

**建议：** 本次修订 `notification-contract-v0.1.md` 时一并把 `APPLICATION_SUBMITTED` 的关联实体改为 `approval/{approval_id}`，避免后续 Phase 2B 文档只修宿舍阻断而留下旧冲突。

---

## 对审查要点的回答

### 1. 推荐选项

推荐 **Option 1** 作为当前 v0.1 / A-lite 决策：

- 保留 `422 DORM_BLOCKED` 同步响应。
- 不创建通知。
- `notification-contract-v0.1.md` 删除 `DORM_CLEARANCE_BLOCKED`，或保留在“Deferred / 后续版本”章节。
- 当前测试 `test_dorm_blocked_does_not_create_notification` 的方向保持正确，但断言应强化为“学生和辅导员都没有宿舍阻断/申请提交通知”。

### 2. 如果选 Option 2，实体设计怎么做

如果产品必须要通知中心留痕，建议独立表，不建议 blocked application。

建议表意：

```text
DormClearanceBlock
- block_id: blk_xxxxxxxx, primary key
- student: FK(User)
- dorm_status
- blocking_reason
- provider_error_code
- checked_at
- last_attempt_at
- resolved_at nullable
- created_at
```

通知使用：

```text
type = dorm_clearance_blocked
entity_type = dorm_clearance_block
entity_id = block_id
recipient = student
```

这样通知有合法业务实体，且不会污染申请审批状态机。

### 3. 如果选 Option 3，如何防重复

不推荐 Option 3。若临时采用，至少不要修改唯一约束；当前唯一约束已包含 `type`。但必须接受一个后果：同一学生的宿舍阻断通知会长期只有一条。

更好的折中不是扩大幂等键，而是新增阻断记录实体。把 `student_id + dorm_status + blocking_reason + unresolved` 归并到一个 open block record，再由通知引用该 record。

### 4. 测试如何调整

采用 Option 1：

- 保留并改名为 `test_dorm_blocked_returns_422_without_notification`。
- 断言响应 `error.code == DORM_BLOCKED`。
- 断言 `Application.objects.filter(student=blocked_student).count() == 0`。
- 断言 `Notification.objects.filter(recipient=blocked_student).count() == 0`。
- 保留辅导员没有 `application_submitted` 通知的断言。

采用 Option 2：

- 将原测试改为断言创建 `DormClearanceBlock` 和一条学生通知。
- 断言不创建 `Application` 和 `Approval`。
- 连续提交两次时，通知数量仍为1，阻断记录可更新 `last_attempt_at`。
- 断言辅导员不收到通知。

### 5. 契约如何修正

采用 Option 1 时，建议修订：

- 事件枚举移除 `DORM_CLEARANCE_BLOCKED`，或移动到 `Deferred events`。
- 删除详细事件说明中的 `entity_type: application / entity_id: application_id`。
- 在非目标或说明中写明：宿舍阻断当前是申请提交接口的同步错误响应，不进入通知中心。
- 同步修正 `APPLICATION_SUBMITTED` 的实体为 `approval/{approval_id}`，匹配现有服务实现。

### 6. 影响文件清单

Option 1 最小修改：

- `docs/api/notification-contract-v0.1.md`
- `backend/apps/notifications/tests/test_auto_notifications_api.py`

Option 2 独立表修改：

- `backend/apps/applications/models.py` 或新增 `backend/apps/dormitory/models.py`
- 对应 migration
- `backend/apps/applications/views.py`
- `backend/apps/notifications/models.py`
- `backend/apps/notifications/services.py`
- `backend/apps/notifications/tests/test_auto_notifications_api.py`
- `docs/api/notification-contract-v0.1.md`
- 如暴露阻断记录 API，再更新 schema/serializer/urls

Option 3 修改：

- `backend/apps/notifications/models.py`
- migration
- `backend/apps/notifications/services.py`
- `backend/apps/applications/views.py`
- `backend/apps/notifications/tests/test_auto_notifications_api.py`
- `docs/api/notification-contract-v0.1.md`

### 7. 实现风险评估

Option 1风险最低。主要风险是产品体验较弱，但当前用户已经在提交动作中即时收到明确错误，且该事件不是异步通知的强需求。

Option 2风险中等。独立表方案语义清楚，但会增加数据模型、迁移、测试和后续清退状态同步问题。只有在“通知中心留痕”是明确产品需求时才值得做。

Option 3风险最高。实现看似简单，但实体语义弱，幂等粒度粗，会给后续审计、重复阻断、原因变化和数据解释留下债务。

---

## 最终建议

Phase 2B不要直接实现宿舍阻断通知。当前应把 Phase 2B 定义为“契约修正优先”：从 v0.1 自动通知范围中移除或 defer `DORM_CLEARANCE_BLOCKED`，保持同步 `422` 阻断行为，并加强现有负路径测试。

如果后续要做“宿舍阻断通知中心留痕”，先单独立项 `DormClearanceBlock` 实体，再基于该实体创建通知。

**文档编号：** 63  
**状态：** Codex建议采用 Option 1；Option 2仅作为后续产品需求成立时的扩展方案

exec
/bin/bash -lc 'rtk git diff -- docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
diff --git a/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md b/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..20cd44f26a573c989807c24d9bc7453deb177957
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md
@@ -0,0 +1,183 @@
+# Phase 2B契约决策 - Codex审查响应
+
+**日期：** 2026-06-02  
+**审查人：** Codex  
+**类型：** 契约决策审查响应  
+**针对：** 62-phase2b-contract-decision-review-request.md
+
+---
+
+## 审查结论
+
+**建议当前采用 Option 1：不为宿舍阻断创建通知，将 `DORM_CLEARANCE_BLOCKED` 从 v0.1 自动通知契约中删除或标记为 deferred。**
+
+理由：当前宿舍阻断是申请提交接口的同步校验失败，而不是已创建业务实体上的状态变更。`create_application` 在宿舍未清退时直接返回 `422`，不会创建 `Application`；通知模型又要求幂等键绑定明确实体。因此在不新增实体的前提下创建通知，会破坏 `entity_id` 语义。
+
+如果产品明确要求“通知中心可回看宿舍阻断原因”，再采用 Option 2 的独立 `DormClearanceBlock` / `DormBlockRecord` 表。不要优先使用 blocked application，也不建议使用 `student_id` 伪装业务事件实体。
+
+---
+
+## 发现的问题
+
+### 问题1：当前不能按契约创建宿舍阻断通知 [P1]
+
+**位置：**
+- `docs/api/notification-contract-v0.1.md:89`
+- `docs/api/notification-contract-v0.1.md:99`
+- `backend/apps/applications/views.py:137`
+- `backend/apps/applications/views.py:150`
+
+契约要求 `DORM_CLEARANCE_BLOCKED` 关联 `application_id`，但代码在宿舍状态非 `completed` 时直接返回 `422`，`Application.objects.create(...)` 在后续分支才执行。也就是说阻断路径没有合法 `application_id`。
+
+**建议：** v0.1中删除该自动通知承诺，或在事件表中标记为 deferred：当前仅通过 `POST /api/applications/` 的 `422 DORM_BLOCKED` 响应告知学生。
+
+### 问题2：blocked application会污染申请状态机 [P1]
+
+**位置：**
+- `backend/apps/applications/models.py:6`
+- `backend/apps/applications/models.py:21`
+- `backend/apps/applications/views.py:118`
+
+如果为阻断创建 `Application(status=blocked)`，需要重新定义列表展示、重复提交限制、审批流创建条件、可见性、统计口径和清退后重提行为。它不是单纯新增一个状态，会让“申请”同时表达“已提交审批对象”和“提交失败尝试”两种语义。
+
+**建议：** 如果必须持久化阻断事件，优先新建独立表，不要把阻断塞进 `Application`。
+
+### 问题3：使用 `student_id` 作为通知实体会让幂等语义过粗 [P1]
+
+**位置：**
+- `backend/apps/notifications/models.py:89`
+
+当前唯一约束是 `(recipient, entity_type, entity_id, type)`。如果 `entity_type=student` 且 `entity_id=student_id`，同一个学生未来所有宿舍阻断都会折叠成同一条通知，无法表达不同阻断记录、不同原因或清退后再次阻断。
+
+**建议：** 不选 Option 3。除非引入真正的 `DormClearanceBlock` 记录，否则不要创建该通知。
+
+### 问题4：通知契约还有一个相邻不一致点，应一并修正 [P2]
+
+**位置：**
+- `docs/api/notification-contract-v0.1.md:51`
+- `backend/apps/notifications/services.py:29`
+
+契约写 `APPLICATION_SUBMITTED` 关联 `application`，但服务实际用 `entity_type='approval'`、`entity_id=approval.pk` 创建通知。考虑接收者是辅导员，通知入口要处理的是待审批记录，当前实现使用 `approval` 更合理。
+
+**建议：** 本次修订 `notification-contract-v0.1.md` 时一并把 `APPLICATION_SUBMITTED` 的关联实体改为 `approval/{approval_id}`，避免后续 Phase 2B 文档只修宿舍阻断而留下旧冲突。
+
+---
+
+## 对审查要点的回答
+
+### 1. 推荐选项
+
+推荐 **Option 1** 作为当前 v0.1 / A-lite 决策：
+
+- 保留 `422 DORM_BLOCKED` 同步响应。
+- 不创建通知。
+- `notification-contract-v0.1.md` 删除 `DORM_CLEARANCE_BLOCKED`，或保留在“Deferred / 后续版本”章节。
+- 当前测试 `test_dorm_blocked_does_not_create_notification` 的方向保持正确，但断言应强化为“学生和辅导员都没有宿舍阻断/申请提交通知”。
+
+### 2. 如果选 Option 2，实体设计怎么做
+
+如果产品必须要通知中心留痕，建议独立表，不建议 blocked application。
+
+建议表意：
+
+```text
+DormClearanceBlock
+- block_id: blk_xxxxxxxx, primary key
+- student: FK(User)
+- dorm_status
+- blocking_reason
+- provider_error_code
+- checked_at
+- last_attempt_at
+- resolved_at nullable
+- created_at
+```
+
+通知使用：
+
+```text
+type = dorm_clearance_blocked
+entity_type = dorm_clearance_block
+entity_id = block_id
+recipient = student
+```
+
+这样通知有合法业务实体，且不会污染申请审批状态机。
+
+### 3. 如果选 Option 3，如何防重复
+
+不推荐 Option 3。若临时采用，至少不要修改唯一约束；当前唯一约束已包含 `type`。但必须接受一个后果：同一学生的宿舍阻断通知会长期只有一条。
+
+更好的折中不是扩大幂等键，而是新增阻断记录实体。把 `student_id + dorm_status + blocking_reason + unresolved` 归并到一个 open block record，再由通知引用该 record。
+
+### 4. 测试如何调整
+
+采用 Option 1：
+
+- 保留并改名为 `test_dorm_blocked_returns_422_without_notification`。
+- 断言响应 `error.code == DORM_BLOCKED`。
+- 断言 `Application.objects.filter(student=blocked_student).count() == 0`。
+- 断言 `Notification.objects.filter(recipient=blocked_student).count() == 0`。
+- 保留辅导员没有 `application_submitted` 通知的断言。
+
+采用 Option 2：
+
+- 将原测试改为断言创建 `DormClearanceBlock` 和一条学生通知。
+- 断言不创建 `Application` 和 `Approval`。
+- 连续提交两次时，通知数量仍为1，阻断记录可更新 `last_attempt_at`。
+- 断言辅导员不收到通知。
+
+### 5. 契约如何修正
+
+采用 Option 1 时，建议修订：
+
+- 事件枚举移除 `DORM_CLEARANCE_BLOCKED`，或移动到 `Deferred events`。
+- 删除详细事件说明中的 `entity_type: application / entity_id: application_id`。
+- 在非目标或说明中写明：宿舍阻断当前是申请提交接口的同步错误响应，不进入通知中心。
+- 同步修正 `APPLICATION_SUBMITTED` 的实体为 `approval/{approval_id}`，匹配现有服务实现。
+
+### 6. 影响文件清单
+
+Option 1 最小修改：
+
+- `docs/api/notification-contract-v0.1.md`
+- `backend/apps/notifications/tests/test_auto_notifications_api.py`
+
+Option 2 独立表修改：
+
+- `backend/apps/applications/models.py` 或新增 `backend/apps/dormitory/models.py`
+- 对应 migration
+- `backend/apps/applications/views.py`
+- `backend/apps/notifications/models.py`
+- `backend/apps/notifications/services.py`
+- `backend/apps/notifications/tests/test_auto_notifications_api.py`
+- `docs/api/notification-contract-v0.1.md`
+- 如暴露阻断记录 API，再更新 schema/serializer/urls
+
+Option 3 修改：
+
+- `backend/apps/notifications/models.py`
+- migration
+- `backend/apps/notifications/services.py`
+- `backend/apps/applications/views.py`
+- `backend/apps/notifications/tests/test_auto_notifications_api.py`
+- `docs/api/notification-contract-v0.1.md`
+
+### 7. 实现风险评估
+
+Option 1风险最低。主要风险是产品体验较弱，但当前用户已经在提交动作中即时收到明确错误，且该事件不是异步通知的强需求。
+
+Option 2风险中等。独立表方案语义清楚，但会增加数据模型、迁移、测试和后续清退状态同步问题。只有在“通知中心留痕”是明确产品需求时才值得做。
+
+Option 3风险最高。实现看似简单，但实体语义弱，幂等粒度粗，会给后续审计、重复阻断、原因变化和数据解释留下债务。
+
+---
+
+## 最终建议
+
+Phase 2B不要直接实现宿舍阻断通知。当前应把 Phase 2B 定义为“契约修正优先”：从 v0.1 自动通知范围中移除或 defer `DORM_CLEARANCE_BLOCKED`，保持同步 `422` 阻断行为，并加强现有负路径测试。
+
+如果后续要做“宿舍阻断通知中心留痕”，先单独立项 `DormClearanceBlock` 实体，再基于该实体创建通知。
+
+**文档编号：** 63  
+**状态：** Codex建议采用 Option 1；Option 2仅作为后续产品需求成立时的扩展方案

exec
/bin/bash -lc 'rtk git status --short docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
?? docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md
diff --git a/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md b/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..20cd44f26a573c989807c24d9bc7453deb177957
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md
@@ -0,0 +1,183 @@
+# Phase 2B契约决策 - Codex审查响应
+
+**日期：** 2026-06-02  
+**审查人：** Codex  
+**类型：** 契约决策审查响应  
+**针对：** 62-phase2b-contract-decision-review-request.md
+
+---
+
+## 审查结论
+
+**建议当前采用 Option 1：不为宿舍阻断创建通知，将 `DORM_CLEARANCE_BLOCKED` 从 v0.1 自动通知契约中删除或标记为 deferred。**
+
+理由：当前宿舍阻断是申请提交接口的同步校验失败，而不是已创建业务实体上的状态变更。`create_application` 在宿舍未清退时直接返回 `422`，不会创建 `Application`；通知模型又要求幂等键绑定明确实体。因此在不新增实体的前提下创建通知，会破坏 `entity_id` 语义。
+
+如果产品明确要求“通知中心可回看宿舍阻断原因”，再采用 Option 2 的独立 `DormClearanceBlock` / `DormBlockRecord` 表。不要优先使用 blocked application，也不建议使用 `student_id` 伪装业务事件实体。
+
+---
+
+## 发现的问题
+
+### 问题1：当前不能按契约创建宿舍阻断通知 [P1]
+
+**位置：**
+- `docs/api/notification-contract-v0.1.md:89`
+- `docs/api/notification-contract-v0.1.md:99`
+- `backend/apps/applications/views.py:137`
+- `backend/apps/applications/views.py:150`
+
+契约要求 `DORM_CLEARANCE_BLOCKED` 关联 `application_id`，但代码在宿舍状态非 `completed` 时直接返回 `422`，`Application.objects.create(...)` 在后续分支才执行。也就是说阻断路径没有合法 `application_id`。
+
+**建议：** v0.1中删除该自动通知承诺，或在事件表中标记为 deferred：当前仅通过 `POST /api/applications/` 的 `422 DORM_BLOCKED` 响应告知学生。
+
+### 问题2：blocked application会污染申请状态机 [P1]
+
+**位置：**
+- `backend/apps/applications/models.py:6`
+- `backend/apps/applications/models.py:21`
+- `backend/apps/applications/views.py:118`
+
+如果为阻断创建 `Application(status=blocked)`，需要重新定义列表展示、重复提交限制、审批流创建条件、可见性、统计口径和清退后重提行为。它不是单纯新增一个状态，会让“申请”同时表达“已提交审批对象”和“提交失败尝试”两种语义。
+
+**建议：** 如果必须持久化阻断事件，优先新建独立表，不要把阻断塞进 `Application`。
+
+### 问题3：使用 `student_id` 作为通知实体会让幂等语义过粗 [P1]
+
+**位置：**
+- `backend/apps/notifications/models.py:89`
+
+当前唯一约束是 `(recipient, entity_type, entity_id, type)`。如果 `entity_type=student` 且 `entity_id=student_id`，同一个学生未来所有宿舍阻断都会折叠成同一条通知，无法表达不同阻断记录、不同原因或清退后再次阻断。
+
+**建议：** 不选 Option 3。除非引入真正的 `DormClearanceBlock` 记录，否则不要创建该通知。
+
+### 问题4：通知契约还有一个相邻不一致点，应一并修正 [P2]
+
+**位置：**
+- `docs/api/notification-contract-v0.1.md:51`
+- `backend/apps/notifications/services.py:29`
+
+契约写 `APPLICATION_SUBMITTED` 关联 `application`，但服务实际用 `entity_type='approval'`、`entity_id=approval.pk` 创建通知。考虑接收者是辅导员，通知入口要处理的是待审批记录，当前实现使用 `approval` 更合理。
+
+**建议：** 本次修订 `notification-contract-v0.1.md` 时一并把 `APPLICATION_SUBMITTED` 的关联实体改为 `approval/{approval_id}`，避免后续 Phase 2B 文档只修宿舍阻断而留下旧冲突。
+
+---
+
+## 对审查要点的回答
+
+### 1. 推荐选项
+
+推荐 **Option 1** 作为当前 v0.1 / A-lite 决策：
+
+- 保留 `422 DORM_BLOCKED` 同步响应。
+- 不创建通知。
+- `notification-contract-v0.1.md` 删除 `DORM_CLEARANCE_BLOCKED`，或保留在“Deferred / 后续版本”章节。
+- 当前测试 `test_dorm_blocked_does_not_create_notification` 的方向保持正确，但断言应强化为“学生和辅导员都没有宿舍阻断/申请提交通知”。
+
+### 2. 如果选 Option 2，实体设计怎么做
+
+如果产品必须要通知中心留痕，建议独立表，不建议 blocked application。
+
+建议表意：
+
+```text
+DormClearanceBlock
+- block_id: blk_xxxxxxxx, primary key
+- student: FK(User)
+- dorm_status
+- blocking_reason
+- provider_error_code
+- checked_at
+- last_attempt_at
+- resolved_at nullable
+- created_at
+```
+
+通知使用：
+
+```text
+type = dorm_clearance_blocked
+entity_type = dorm_clearance_block
+entity_id = block_id
+recipient = student
+```
+
+这样通知有合法业务实体，且不会污染申请审批状态机。
+
+### 3. 如果选 Option 3，如何防重复
+
+不推荐 Option 3。若临时采用，至少不要修改唯一约束；当前唯一约束已包含 `type`。但必须接受一个后果：同一学生的宿舍阻断通知会长期只有一条。
+
+更好的折中不是扩大幂等键，而是新增阻断记录实体。把 `student_id + dorm_status + blocking_reason + unresolved` 归并到一个 open block record，再由通知引用该 record。
+
+### 4. 测试如何调整
+
+采用 Option 1：
+
+- 保留并改名为 `test_dorm_blocked_returns_422_without_notification`。
+- 断言响应 `error.code == DORM_BLOCKED`。
+- 断言 `Application.objects.filter(student=blocked_student).count() == 0`。
+- 断言 `Notification.objects.filter(recipient=blocked_student).count() == 0`。
+- 保留辅导员没有 `application_submitted` 通知的断言。
+
+采用 Option 2：
+
+- 将原测试改为断言创建 `DormClearanceBlock` 和一条学生通知。
+- 断言不创建 `Application` 和 `Approval`。
+- 连续提交两次时，通知数量仍为1，阻断记录可更新 `last_attempt_at`。
+- 断言辅导员不收到通知。
+
+### 5. 契约如何修正
+
+采用 Option 1 时，建议修订：
+
+- 事件枚举移除 `DORM_CLEARANCE_BLOCKED`，或移动到 `Deferred events`。
+- 删除详细事件说明中的 `entity_type: application / entity_id: application_id`。
+- 在非目标或说明中写明：宿舍阻断当前是申请提交接口的同步错误响应，不进入通知中心。
+- 同步修正 `APPLICATION_SUBMITTED` 的实体为 `approval/{approval_id}`，匹配现有服务实现。
+
+### 6. 影响文件清单
+
+Option 1 最小修改：
+
+- `docs/api/notification-contract-v0.1.md`
+- `backend/apps/notifications/tests/test_auto_notifications_api.py`
+
+Option 2 独立表修改：
+
+- `backend/apps/applications/models.py` 或新增 `backend/apps/dormitory/models.py`
+- 对应 migration
+- `backend/apps/applications/views.py`
+- `backend/apps/notifications/models.py`
+- `backend/apps/notifications/services.py`
+- `backend/apps/notifications/tests/test_auto_notifications_api.py`
+- `docs/api/notification-contract-v0.1.md`
+- 如暴露阻断记录 API，再更新 schema/serializer/urls
+
+Option 3 修改：
+
+- `backend/apps/notifications/models.py`
+- migration
+- `backend/apps/notifications/services.py`
+- `backend/apps/applications/views.py`
+- `backend/apps/notifications/tests/test_auto_notifications_api.py`
+- `docs/api/notification-contract-v0.1.md`
+
+### 7. 实现风险评估
+
+Option 1风险最低。主要风险是产品体验较弱，但当前用户已经在提交动作中即时收到明确错误，且该事件不是异步通知的强需求。
+
+Option 2风险中等。独立表方案语义清楚，但会增加数据模型、迁移、测试和后续清退状态同步问题。只有在“通知中心留痕”是明确产品需求时才值得做。
+
+Option 3风险最高。实现看似简单，但实体语义弱，幂等粒度粗，会给后续审计、重复阻断、原因变化和数据解释留下债务。
+
+---
+
+## 最终建议
+
+Phase 2B不要直接实现宿舍阻断通知。当前应把 Phase 2B 定义为“契约修正优先”：从 v0.1 自动通知范围中移除或 defer `DORM_CLEARANCE_BLOCKED`，保持同步 `422` 阻断行为，并加强现有负路径测试。
+
+如果后续要做“宿舍阻断通知中心留痕”，先单独立项 `DormClearanceBlock` 实体，再基于该实体创建通知。
+
+**文档编号：** 63  
+**状态：** Codex建议采用 Option 1；Option 2仅作为后续产品需求成立时的扩展方案

codex
Created the Codex review response at [63-phase2b-contract-decision-codex-response.md](/home/caohui/projects/graduation-leave-system/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md).

Conclusion: recommend **Option 1** for v0.1: keep synchronous `422 DORM_BLOCKED`, do not create a notification, and remove or defer `DORM_CLEARANCE_BLOCKED` from the automatic notification contract. If persistent notification-center history becomes a product requirement later, use an independent `DormClearanceBlock` entity, not a blocked `Application` or `student_id` as a fake event entity.

I also flagged one adjacent contract mismatch: `APPLICATION_SUBMITTED` currently uses `approval` as the actual notification entity in code, while the contract says `application`; the contract should be corrected while touching this file. No tests were run because this was a document review only.
diff --git a/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md b/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md
new file mode 100644
index 0000000000000000000000000000000000000000..20cd44f26a573c989807c24d9bc7453deb177957
--- /dev/null
+++ b/docs/discussions/phase4c-next-steps/63-phase2b-contract-decision-codex-response.md
@@ -0,0 +1,183 @@
+# Phase 2B契约决策 - Codex审查响应
+
+**日期：** 2026-06-02  
+**审查人：** Codex  
+**类型：** 契约决策审查响应  
+**针对：** 62-phase2b-contract-decision-review-request.md
+
+---
+
+## 审查结论
+
+**建议当前采用 Option 1：不为宿舍阻断创建通知，将 `DORM_CLEARANCE_BLOCKED` 从 v0.1 自动通知契约中删除或标记为 deferred。**
+
+理由：当前宿舍阻断是申请提交接口的同步校验失败，而不是已创建业务实体上的状态变更。`create_application` 在宿舍未清退时直接返回 `422`，不会创建 `Application`；通知模型又要求幂等键绑定明确实体。因此在不新增实体的前提下创建通知，会破坏 `entity_id` 语义。
+
+如果产品明确要求“通知中心可回看宿舍阻断原因”，再采用 Option 2 的独立 `DormClearanceBlock` / `DormBlockRecord` 表。不要优先使用 blocked application，也不建议使用 `student_id` 伪装业务事件实体。
+
+---
+
+## 发现的问题
+
+### 问题1：当前不能按契约创建宿舍阻断通知 [P1]
+
+**位置：**
+- `docs/api/notification-contract-v0.1.md:89`
+- `docs/api/notification-contract-v0.1.md:99`
+- `backend/apps/applications/views.py:137`
+- `backend/apps/applications/views.py:150`
+
+契约要求 `DORM_CLEARANCE_BLOCKED` 关联 `application_id`，但代码在宿舍状态非 `completed` 时直接返回 `422`，`Application.objects.create(...)` 在后续分支才执行。也就是说阻断路径没有合法 `application_id`。
+
+**建议：** v0.1中删除该自动通知承诺，或在事件表中标记为 deferred：当前仅通过 `POST /api/applications/` 的 `422 DORM_BLOCKED` 响应告知学生。
+
+### 问题2：blocked application会污染申请状态机 [P1]
+
+**位置：**
+- `backend/apps/applications/models.py:6`
+- `backend/apps/applications/models.py:21`
+- `backend/apps/applications/views.py:118`
+
+如果为阻断创建 `Application(status=blocked)`，需要重新定义列表展示、重复提交限制、审批流创建条件、可见性、统计口径和清退后重提行为。它不是单纯新增一个状态，会让“申请”同时表达“已提交审批对象”和“提交失败尝试”两种语义。
+
+**建议：** 如果必须持久化阻断事件，优先新建独立表，不要把阻断塞进 `Application`。
+
+### 问题3：使用 `student_id` 作为通知实体会让幂等语义过粗 [P1]
+
+**位置：**
+- `backend/apps/notifications/models.py:89`
+
+当前唯一约束是 `(recipient, entity_type, entity_id, type)`。如果 `entity_type=student` 且 `entity_id=student_id`，同一个学生未来所有宿舍阻断都会折叠成同一条通知，无法表达不同阻断记录、不同原因或清退后再次阻断。
+
+**建议：** 不选 Option 3。除非引入真正的 `DormClearanceBlock` 记录，否则不要创建该通知。
+
+### 问题4：通知契约还有一个相邻不一致点，应一并修正 [P2]
+
+**位置：**
+- `docs/api/notification-contract-v0.1.md:51`
+- `backend/apps/notifications/services.py:29`
+
+契约写 `APPLICATION_SUBMITTED` 关联 `application`，但服务实际用 `entity_type='approval'`、`entity_id=approval.pk` 创建通知。考虑接收者是辅导员，通知入口要处理的是待审批记录，当前实现使用 `approval` 更合理。
+
+**建议：** 本次修订 `notification-contract-v0.1.md` 时一并把 `APPLICATION_SUBMITTED` 的关联实体改为 `approval/{approval_id}`，避免后续 Phase 2B 文档只修宿舍阻断而留下旧冲突。
+
+---
+
+## 对审查要点的回答
+
+### 1. 推荐选项
+
+推荐 **Option 1** 作为当前 v0.1 / A-lite 决策：
+
+- 保留 `422 DORM_BLOCKED` 同步响应。
+- 不创建通知。
+- `notification-contract-v0.1.md` 删除 `DORM_CLEARANCE_BLOCKED`，或保留在“Deferred / 后续版本”章节。
+- 当前测试 `test_dorm_blocked_does_not_create_notification` 的方向保持正确，但断言应强化为“学生和辅导员都没有宿舍阻断/申请提交通知”。
+
+### 2. 如果选 Option 2，实体设计怎么做
+
+如果产品必须要通知中心留痕，建议独立表，不建议 blocked application。
+
+建议表意：
+
+```text
+DormClearanceBlock
+- block_id: blk_xxxxxxxx, primary key
+- student: FK(User)
+- dorm_status
+- blocking_reason
+- provider_error_code
+- checked_at
+- last_attempt_at
+- resolved_at nullable
+- created_at
+```
+
+通知使用：
+
+```text
+type = dorm_clearance_blocked
+entity_type = dorm_clearance_block
+entity_id = block_id
+recipient = student
+```
+
+这样通知有合法业务实体，且不会污染申请审批状态机。
+
+### 3. 如果选 Option 3，如何防重复
+
+不推荐 Option 3。若临时采用，至少不要修改唯一约束；当前唯一约束已包含 `type`。但必须接受一个后果：同一学生的宿舍阻断通知会长期只有一条。
+
+更好的折中不是扩大幂等键，而是新增阻断记录实体。把 `student_id + dorm_status + blocking_reason + unresolved` 归并到一个 open block record，再由通知引用该 record。
+
+### 4. 测试如何调整
+
+采用 Option 1：
+
+- 保留并改名为 `test_dorm_blocked_returns_422_without_notification`。
+- 断言响应 `error.code == DORM_BLOCKED`。
+- 断言 `Application.objects.filter(student=blocked_student).count() == 0`。
+- 断言 `Notification.objects.filter(recipient=blocked_student).count() == 0`。
+- 保留辅导员没有 `application_submitted` 通知的断言。
+
+采用 Option 2：
+
+- 将原测试改为断言创建 `DormClearanceBlock` 和一条学生通知。
+- 断言不创建 `Application` 和 `Approval`。
+- 连续提交两次时，通知数量仍为1，阻断记录可更新 `last_attempt_at`。
+- 断言辅导员不收到通知。
+
+### 5. 契约如何修正
+
+采用 Option 1 时，建议修订：
+
+- 事件枚举移除 `DORM_CLEARANCE_BLOCKED`，或移动到 `Deferred events`。
+- 删除详细事件说明中的 `entity_type: application / entity_id: application_id`。
+- 在非目标或说明中写明：宿舍阻断当前是申请提交接口的同步错误响应，不进入通知中心。
+- 同步修正 `APPLICATION_SUBMITTED` 的实体为 `approval/{approval_id}`，匹配现有服务实现。
+
+### 6. 影响文件清单
+
+Option 1 最小修改：
+
+- `docs/api/notification-contract-v0.1.md`
+- `backend/apps/notifications/tests/test_auto_notifications_api.py`
+
+Option 2 独立表修改：
+
+- `backend/apps/applications/models.py` 或新增 `backend/apps/dormitory/models.py`
+- 对应 migration
+- `backend/apps/applications/views.py`
+- `backend/apps/notifications/models.py`
+- `backend/apps/notifications/services.py`
+- `backend/apps/notifications/tests/test_auto_notifications_api.py`
+- `docs/api/notification-contract-v0.1.md`
+- 如暴露阻断记录 API，再更新 schema/serializer/urls
+
+Option 3 修改：
+
+- `backend/apps/notifications/models.py`
+- migration
+- `backend/apps/notifications/services.py`
+- `backend/apps/applications/views.py`
+- `backend/apps/notifications/tests/test_auto_notifications_api.py`
+- `docs/api/notification-contract-v0.1.md`
+
+### 7. 实现风险评估
+
+Option 1风险最低。主要风险是产品体验较弱，但当前用户已经在提交动作中即时收到明确错误，且该事件不是异步通知的强需求。
+
+Option 2风险中等。独立表方案语义清楚，但会增加数据模型、迁移、测试和后续清退状态同步问题。只有在“通知中心留痕”是明确产品需求时才值得做。
+
+Option 3风险最高。实现看似简单，但实体语义弱，幂等粒度粗，会给后续审计、重复阻断、原因变化和数据解释留下债务。
+
+---
+
+## 最终建议
+
+Phase 2B不要直接实现宿舍阻断通知。当前应把 Phase 2B 定义为“契约修正优先”：从 v0.1 自动通知范围中移除或 defer `DORM_CLEARANCE_BLOCKED`，保持同步 `422` 阻断行为，并加强现有负路径测试。
+
+如果后续要做“宿舍阻断通知中心留痕”，先单独立项 `DormClearanceBlock` 实体，再基于该实体创建通知。
+
+**文档编号：** 63  
+**状态：** Codex建议采用 Option 1；Option 2仅作为后续产品需求成立时的扩展方案

tokens used
48,484

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
