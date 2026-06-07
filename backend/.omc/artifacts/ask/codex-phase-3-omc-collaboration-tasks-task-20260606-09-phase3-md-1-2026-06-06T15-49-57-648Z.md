# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-06-06T15:49:57.648Z

## Original task

审查Phase 3数据导入完成后的轻微数据差异。

**任务文档：** .omc/collaboration/tasks/TASK-20260606-09-Phase3数据导入完成-轻微差异审查.md

**核心问题：**
1. 实际导入6055用户 vs 预期6041用户（+14人差异）
2. 学生5956 vs 5946（+10），宿管75 vs 73（+2），辅导员22 vs 20（+2）
3. 可能原因：历史测试数据残留

**核心指标已达标：**
- 0个TMP ID残留 ✓
- 97%楼栋覆盖率 ✓
- 兜底宿管员已就位 ✓

**审查要点：**
1. 14人差异是否影响系统功能（审批路由/权限/统计）？
2. 是否需要调查根本原因？
3. 生产环境导入策略：append（保留历史）vs clean（删除重建）vs 手动清理？
4. 19名额外研究生如何处理（已有待确认清单）？
5. Phase 4前端工作是否有阻塞项？

**期望输出：** 结构化审查意见（影响评估+导入策略推荐+处理优先级+是否阻塞Phase 4）

## Final prompt

审查Phase 3数据导入完成后的轻微数据差异。

**任务文档：** .omc/collaboration/tasks/TASK-20260606-09-Phase3数据导入完成-轻微差异审查.md

**核心问题：**
1. 实际导入6055用户 vs 预期6041用户（+14人差异）
2. 学生5956 vs 5946（+10），宿管75 vs 73（+2），辅导员22 vs 20（+2）
3. 可能原因：历史测试数据残留

**核心指标已达标：**
- 0个TMP ID残留 ✓
- 97%楼栋覆盖率 ✓
- 兜底宿管员已就位 ✓

**审查要点：**
1. 14人差异是否影响系统功能（审批路由/权限/统计）？
2. 是否需要调查根本原因？
3. 生产环境导入策略：append（保留历史）vs clean（删除重建）vs 手动清理？
4. 19名额外研究生如何处理（已有待确认清单）？
5. Phase 4前端工作是否有阻塞项？

**期望输出：** 结构化审查意见（影响评估+导入策略推荐+处理优先级+是否阻塞Phase 4）

## Raw output

```text
已完成审查，并写入 artifact：

[20260606-1548-codex-phase3-data-discrepancy-review.md](/home/caohui/projects/graduation-leave-system/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md)

核心结论：

- 14人差异本身不阻塞系统功能，已基本确认是历史测试/种子数据残留：
  - 学生：`2020001`-`2020010`
  - 宿管：`M001/M002`
  - 辅导员：`T001/T002`
- 不建议继续大范围根因调查；当前证据足够，保留一次性审计记录即可。
- 生产首次导入推荐 `clean/rebuild` 基线，不推荐 `append`。现有 `import_students --mode clean` 只清学生，不能清理残留 staff，因此生产最好空库迁移后导入，或先显式清理目标角色数据。
- 19名额外研究生暂不纳入主批次，作为 Phase 3.5 等业务确认后补充处理。
- Phase 4 页面开发不阻塞；但真实端到端联调阻塞。

额外发现两个更重要的 Phase 4 联调风险：

- 当前库有1个非 `rejected` 申请，会阻止 `import_students --mode clean`。
- 辅导员路由当前不可用：22名辅导员 `department` 均为空，且 [apps/approvals/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:14) 未导入 `User` 但后面使用了 `User.objects`。

协作日志已更新到 `TASK-20260606-09` completed，`state.json.last_event_id=15`。未修改业务代码；只写入审查 artifact 和协作事件/state。


OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system/backend
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019e9d9a-9a2d-7df2-9eab-44585a14cc2a
--------
user
审查Phase 3数据导入完成后的轻微数据差异。

**任务文档：** .omc/collaboration/tasks/TASK-20260606-09-Phase3数据导入完成-轻微差异审查.md

**核心问题：**
1. 实际导入6055用户 vs 预期6041用户（+14人差异）
2. 学生5956 vs 5946（+10），宿管75 vs 73（+2），辅导员22 vs 20（+2）
3. 可能原因：历史测试数据残留

**核心指标已达标：**
- 0个TMP ID残留 ✓
- 97%楼栋覆盖率 ✓
- 兜底宿管员已就位 ✓

**审查要点：**
1. 14人差异是否影响系统功能（审批路由/权限/统计）？
2. 是否需要调查根本原因？
3. 生产环境导入策略：append（保留历史）vs clean（删除重建）vs 手动清理？
4. 19名额外研究生如何处理（已有待确认清单）？
5. Phase 4前端工作是否有阻塞项？

**期望输出：** 结构化审查意见（影响评估+导入策略推荐+处理优先级+是否阻塞Phase 4）
codex
我会先读取项目要求和审查协议，再看任务文档与相关证据，之后按影响、策略、优先级和阻塞判断输出审查意见。
exec
/bin/bash -lc "pwd && sed -n '1,220p' /home/caohui/.codex/RTK.md" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
/home/caohui/projects/graduation-leave-system/backend
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
RTK要求所有项目内 shell 命令加 `rtk` 前缀。接下来我会按这个约束读取协作协议、审查协议和任务文档。
exec
/bin/bash -lc "rtk sed -n '1,240p' .omc/collaboration/protocol.md" in /home/caohui/projects/graduation-leave-system/backend
 exited 2 in 0ms:
/usr/bin/sed: can't read .omc/collaboration/protocol.md: No such file or directory

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/codex-review-protocol.md" in /home/caohui/projects/graduation-leave-system/backend
 exited 2 in 0ms:
/usr/bin/sed: can't read docs/codex-review-protocol.md: No such file or directory

exec
/bin/bash -lc "rtk sed -n '1,260p' .omc/collaboration/tasks/TASK-20260606-09-Phase3数据导入完成-轻微差异审查.md" in /home/caohui/projects/graduation-leave-system/backend
 exited 2 in 0ms:
/usr/bin/sed: can't read .omc/collaboration/tasks/TASK-20260606-09-Phase3数据导入完成-轻微差异审查.md: No such file or directory

codex
这些路径在当前 `backend` 目录下不存在，我会向上检查仓库结构，定位项目根目录里的 `.omc` 和 `docs`。
exec
/bin/bash -lc "rtk find .. -maxdepth 4 \\( -path '*/.omc/collaboration/protocol.md' -o -path '*/docs/codex-review-protocol.md' -o -path '*/TASK-20260606-09-Phase3数据导入完成-轻微差异审查.md' \\) -print" in /home/caohui/projects/graduation-leave-system/backend
 exited 1 in 0ms:
rtk: rtk find does not support compound predicates or actions (e.g. -not, -exec). Use `find` directly.

exec
/bin/bash -lc 'rtk ls -la ..' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
.agents/
.claude/
.codex/
.git/
.omc/
.planning/
.pytest_cache/
PRD/
backend/
demo-web/
docker/
docs/
frontend/
miniprogram/
plans/
scripts/
tests/
.env.docker  598B
.env.example  683B
.gitignore  664B
AGENTS.md  1.0K
CLAUDE.md  3.1K
DEPLOYMENT.md  8.0K
docker-compose.yml  756B
findings.md  1.8K
progress.md  1.3K
task_plan.md  2.4K
毕业离校系统用户文档.zip  8.2K

exec
/bin/bash -lc 'rtk ls -la' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
.omc/
.pytest_cache/
__pycache__/
apps/
config/
data/
docs/
media/
reports/
requirements/
scripts/
utils/
venv/
.env  269B
.env.example  648B
Dockerfile  493B
app -> /app  4B
manage.py  666B
requirements.txt  333B
schema.py  739B

codex
当前目录本身有 `.omc` 和 `docs`，但协议文件不在预期位置。我会用 `rg --files` 定位同名文件和任务文档。
exec
/bin/bash -lc 'rtk ls -la .omc .omc/collaboration docs' in /home/caohui/projects/graduation-leave-system/backend
 exited 2 in 0ms:
.omc:
total 28
drwxrwxr-x  4 caohui caohui 4096 Jun  6 23:38 .
drwxrwxr-x 15 caohui caohui 4096 Jun  6 18:39 ..
drwxrwxr-x  3 caohui caohui 4096 May 31 00:08 artifacts
-rw-rw-r--  1 caohui caohui 8496 Jun  6 23:38 session-context.json
drwxrwxr-x  4 caohui caohui 4096 Jun  6 23:41 state

docs:
total 12
drwxrwxr-x  3 caohui caohui 4096 May 31 00:26 .
drwxrwxr-x 15 caohui caohui 4096 Jun  6 18:39 ..
drwxrwxr-x  3 caohui caohui 4096 May 31 00:26 discussions
ls: cannot access '.omc/collaboration': No such file or directory

exec
/bin/bash -lc 'rtk ls -la ../.omc ../.omc/collaboration ../docs' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
artifacts/
collaboration/
plans/
sessions/
state/
.omc/
artifacts/
backup-20260530-084231/
backup-20260602-091926/
backup-20260602-101257/
backup-20260603-101421/
locks/
scripts/
tasks/
acceptance/
api/
api-samples/
contracts/
design/
discussions/
plans/
superpowers/
templates/
ui-design-proposals/
project-memory.json  14.0K
project-state.json  1.7K
session-context.json  7.8K
codex-ready.md  468B
events.jsonl  4.5K
events_backup.jsonl  51.5K
phase1b-implementation-consensus.md  12.5K
protocol.md  15.8K
state.json  214B
task-1-consensus.md  5.0K
task-2-consensus.md  5.9K
task-3-consensus.md  6.0K
task-4-consensus.md  4.8K
1-5830名毕业生（含研究生）.xls  1002.5K
1-无入住信息.xls  45.0K
19名额外研究生待确认清单.md  3.3K
20260606-毕业生入住基本信息.xls  1.3M
2026届预计毕业生5675人.xlsx  900.7K
2026年学院辅导员信息统计表.xls  23.5K
2026年社区辅导员信息统计表.xls  30.0K
271名研究生学号比对分析报告.md  5.0K
271名研究生学号补充请求.csv  26.6K
API-DATA-EXAMPLES.md  5.1K
COMPLETION-STATUS.md  4.1K
Codex审查流程指南.md  7.0K
Excel数据源分析与需求对比.md  8.0K
Excel数据源实际分析结果.md  9.7K
PROJECT-COMPLETION-DECLARATION.md  2.9K
PROJECT-SUMMARY.md  129.4K
Phase0数据验证后执行逻辑调整总结.md  6.7K
XG-API-ACTUAL-DATA-SAMPLES.md  6.2K
XG-API-COLLECTION-TEST-GUIDE.md  4.1K
XG-API-DATA-EXAMPLES.md  6.7K
XG-API-DATA-SAMPLES.md  5.5K
XG-API-数据源全面分析报告.md  19.0K
XG-API与项目数据表对比分析.md  12.0K
XG-API数据不足解决方案讨论.md  11.2K
api说明.txt  7.5K
codex-review-protocol.md  7.0K
missing_building_data_discrepancy_analysis.md  4.7K
phase4c-xg-field-coverage.md  10.9K
project-completion-status-2026-06-02.md  4.1K
week3-day0-acceptance-checklist.md  11.7K
week3-day0-environment-strategy.md  2.2K
week3-day0-seed-data-requirements.md  4.1K
兜底宿管员路由逻辑方案.md  6.2K
外部系统数据接口确认清单.md  5.6K
微信图片_20260528210617_553_47.jpg  85.9K
微信图片_20260528210618_554_47.jpg  192.1K
微信图片_20260528210619_555_47.jpg  121.0K
微信小程序备案说明.md  4.3K
微信小程序申请说明.md  2.4K
操作说明书-待改进事项.md  3.8K
操作说明书.md  10.7K
数据对接说明文档.md  13.8K
数据对接说明文档.md.backup  11.5K
数据确认清单.md  7.3K
数据补充请求-116名学生楼栋信息.md  3.8K
数据补充请求-271名研究生学号信息.md  4.2K
新增审核人员.txt  302B
无楼栋信息学生对比表.csv  9.0K
用户设计说明书.md  12.2K
用户需求最终确认与实施方案.md  21.7K
硕士研究生-毕业生290人.xls  50.0K

exec
/bin/bash -lc "rtk rg --files -g 'protocol.md' -g 'codex-review-protocol.md' -g '*Phase3*差异审查*.md' . .." in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
../docs/codex-review-protocol.md

codex
协议文件在仓库根目录；任务文档可能也在根 `.omc/collaboration/tasks`，我会读取协议并列出任务目录确认文件名。
exec
/bin/bash -lc 'rtk ls -la ../.omc/collaboration/tasks' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
TASK-20260530-01-protocol-critical-review.md  2.2K
TASK-20260530-02-implement-p0-amendments.md  3.2K
TASK-20260530-03-分析4个github项目并评估可借鉴内容（含gemini集成.md  473B
TASK-20260530-04-实施p0优先级项：角色路由+独立分析协议+journal校验.md  2.4K
TASK-20260530-05-next-steps-critical-discussion.md  2.6K
TASK-20260530-06-readiness-gate-canary-pilot.md  7.0K
TASK-20260602-01-ui-design-miniprogram.md  3.7K
TASK-20260602-02-step-4b-phase-3:-xg用户同步服务apply.md  1.8K
TASK-20260602-03-step-4b-phase-4:-回归验证---运行完整测试.md  1.3K
TASK-20260602-04-step-5:-xg用户同步管理命令---sync_xg_u.md  1.6K
TASK-20260603-01-xg-data-coverage-analysis.md  3.0K
TASK-20260603-02-xg-data-review-request.md  3.4K
TASK-20260605-01-excel-association-review-request.md  8.0K
TASK-20260605-01-excel数据源关联策略讨论---file1+file2通过.md  724B
TASK-20260605-03-implementation-plan-review.md  4.4K
TASK-20260605-04-phase-0-p0阻塞：116个file2独有学生缺少楼栋.md  1.0K
TASK-20260606-08-审查请求.md  6.7K
TASK-20260606-08-数据验证完成：271名研究生学号已找到（100%匹配），发现.md  970B
TASK-20260606-09-Phase3数据导入完成-轻微差异审查.md  5.2K

exec
/bin/bash -lc "rtk sed -n '1,260p' ../.omc/collaboration/protocol.md" in /home/caohui/projects/graduation-leave-system/backend
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
/bin/bash -lc "rtk sed -n '1,260p' ../docs/codex-review-protocol.md" in /home/caohui/projects/graduation-leave-system/backend
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
/bin/bash -lc "rtk sed -n '261,520p' ../.omc/collaboration/protocol.md" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:

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
审查流程要求查看共享状态和事件日志；我会先确认当前任务状态，再读取这次 Phase 3 任务文档的完整内容。
exec
/bin/bash -lc "rtk sed -n '1,260p' ../.omc/collaboration/tasks/TASK-20260606-09-Phase3数据导入完成-轻微差异审查.md" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
# Phase 3数据导入完成 - 轻微数据差异审查请求

**任务ID:** TASK-20260606-09  
**日期:** 2026-06-06  
**审查类型:** Phase 3数据导入验证结果分析  
**审查范围:** 数据差异影响评估与处理建议

---

## 审查背景

Phase 3数据导入已完成（Phase 3.1-3.4），所有预期数据已成功导入数据库。但验证过程中发现实际导入数据量与预期存在轻微差异，需审查差异原因、影响范围及处理建议。

**核心指标均已达标：**
- ✅ 0个TMP ID残留
- ✅ 97%楼栋覆盖率（5830/5956）
- ✅ 兜底宿管员92008149已就位

---

## 数据导入实际结果

### Phase 3.1 - 学生导入
- **文件：** file5_students_merged_v2.csv
- **预期：** 5946人
- **实际：** 5956人 (+10)
- **结果：** 导入成功，0个TMP ID残留

### Phase 3.2 - 宿管员导入
- **文件：** dorm_managers_processed.csv（预处理自File3）
- **预期：** 72人 + 1兜底宿管员 = 73人
- **实际：** 75人 (+2)
- **结果：** 导入成功，兜底宿管员92008149已就位

### Phase 3.3 - 辅导员导入
- **文件：** counselors_processed.csv（预处理自File4）
- **预期：** 20人
- **实际：** 22人 (+2)
- **结果：** 导入成功

### Phase 3.4 - 学工管理员导入
- **文件：** additional_staff.csv
- **预期：** 2学工管理员 + 1兜底宿管员 = 3人
- **实际：** 2学工管理员 + 1兜底宿管员 = 3人（与Phase 3.2重复导入兜底宿管员）
- **结果：** 导入成功

### 汇总
- **总用户数：** 6055人
- **预期：** 5946 + 73 + 20 + 2 = 6041人
- **差异：** +14人

---

## 差异分析

### 可能原因
1. **历史测试数据残留：** 数据库可能包含之前测试导入的历史数据（最可能）
2. **重复导入：** update_or_create可能更新了已存在记录而非创建新记录
3. **数据源文件差异：** 预处理过程中可能有额外数据被纳入

### 差异分布
- 学生：+10人（0.17%偏差）
- 宿管员：+2人（2.7%偏差）
- 辅导员：+2人（10%偏差）
- 学工管理员：符合预期

### 功能影响评估（初步）
- **审批路由：** 不受影响（路由基于building和department字段，非用户总数）
- **权限控制：** 不受影响（基于role字段）
- **兜底宿管员：** 已验证存在且配置正确
- **楼栋覆盖率：** 97%（5830/5956），略低于预期98%（5830/5946），但仍在可接受范围

---

## 待审查问题

### 1. 差异是否影响系统功能？
- 多出的14个用户是否会导致审批流程、权限控制或数据统计异常？
- 楼栋覆盖率从98%降至97%是否可接受？

### 2. 是否需要调查根本原因？
- 是否需要识别多出的14个用户具体是谁？
- 是否需要验证这些用户是历史数据还是重复导入？

### 3. 生产环境导入策略
- **方案A：** 使用append模式（当前）- 保留历史数据，快速部署
- **方案B：** 使用clean模式 - 删除所有学生后重新导入，确保数据纯净
- **方案C：** 手动清理差异用户 - 识别并删除多余记录

**约束条件：**
- import_students --mode clean 要求数据库无active applications（当前满足）
- clean模式会删除所有role=STUDENT的用户

### 4. 19名额外研究生处理
- 已创建待确认清单：`docs/19名额外研究生待确认清单.md`
- 这19人在系统中但不在源数据中，是否应纳入主批次？
- 建议作为Phase 3.5单独处理，等待用户确认

---

## 技术实施记录

### Bug修复
- **问题：** import_students.py和import_staff.py的dry-run模式raise Exception导致统计无法打印
- **修复：** Line 76-78（import_students）和Line 55-56（import_staff）改用transaction.set_rollback(True)
- **结果：** 干运行正常显示统计，事务仍正确回滚

### 数据预处理
- **File3预处理：** 跳过标题行，添加"角色"列（宿管员），楼栋号→楼栋
- **File4预处理：** 跳过标题行，添加"角色"列（辅导员），无需楼栋字段
- **输出文件：** dorm_managers_processed.csv（72行）, counselors_processed.csv（20行）

---

## 审查请求

**请Codex审查：**
1. 14人数据差异的功能影响评估是否准确？
2. 生产环境应选择哪种导入策略（方案A/B/C）？
3. 19名额外研究生的处理优先级（Phase 3.5 vs 忽略）？
4. 是否需要在Phase 4前端工作前先解决这些差异？

**期望输出：**
- 差异影响评估（功能/性能/数据一致性）
- 推荐的生产环境导入策略（含理由）
- 19名额外研究生处理建议
- Phase 4启动前是否有阻塞项

---

**相关文档：**
- `.omc/session-context.json` - Phase 3完成状态
- `docs/PROJECT-SUMMARY.md` - Phase 3数据导入执行记录
- `docs/19名额外研究生待确认清单.md` - 额外研究生详情
- `backend/data/file5_students_merged_v2.csv` - 学生源数据（5946行）
- `backend/data/dorm_managers_processed.csv` - 宿管员源数据（72行）
- `backend/data/counselors_processed.csv` - 辅导员源数据（20行）
- `backend/data/additional_staff.csv` - 管理员源数据（3行）

**Claude初步判断：** 差异轻微，不阻塞Phase 4前端工作，建议生产环境使用clean模式确保数据纯净。

exec
/bin/bash -lc 'rtk tail -n 40 ../.omc/collaboration/events.jsonl' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
{"id":1,"type":"workflow_initialized","agent":"claude","timestamp":"2026-06-05T05:10:00.000Z","summary":"Initialize implementation-plan-review workflow","status":"initialized"}
{"id":2,"type":"task_created","agent":"claude","timestamp":"2026-06-05T05:10:10.000Z","task_id":"TASK-20260605-03","summary":"Review implementation plan document","artifacts":["tasks/TASK-20260605-03-implementation-plan-review.md"]}
{"id":3,"type":"handoff_requested","agent":"claude","timestamp":"2026-06-05T05:10:20.000Z","task_id":"TASK-20260605-03","target_agent":"codex","summary":"Request Codex review of implementation plan"}
{"id":4,"type":"task_claimed","agent":"codex","timestamp":"2026-06-05T05:11:07.039Z","task_id":"TASK-20260605-03","summary":"Codex claimed implementation plan review task","status":"in_progress"}
{"id":5,"type":"artifact_created","agent":"codex","timestamp":"2026-06-05T05:13:50.860Z","task_id":"TASK-20260605-03","summary":"Codex implementation plan review artifact created","artifacts":[".omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md"],"status":"in_progress"}
{"id":6,"type":"completed","agent":"codex","timestamp":"2026-06-05T05:13:50.860Z","task_id":"TASK-20260605-03","summary":"Codex completed implementation plan review","artifacts":[".omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md"],"status":"completed"}
{"id": 7, "type": "task_created", "agent": "claude", "timestamp": "2026-06-05T19:55:07.600892+00:00", "summary": "Created task: Phase 0 P0\u963b\u585e\uff1a116\u4e2aFile2\u72ec\u6709\u5b66\u751f\u7f3a\u5c11\u697c\u680b\u6570\u636e\uff0c\u5bfc\u81f4\u5bbf\u7ba1\u5458\u8def\u7531\u5931\u8d25\uff0898.0% vs 100%\u95e8\u7981\u8981\u6c42\uff09\u3002\u9700\u8981\u4e1a\u52a1\u51b3\u7b56\uff1a1)\u63a5\u53d798%\u8986\u76d6\u7387\u4f5c\u4e3a\u53ef\u63a5\u53d7\u6807\u51c6 2)\u6392\u9664\u8fd9116\u540d\u5b66\u751f\u76f4\u5230\u8865\u5145\u697c\u680b\u6570\u636e 3)\u8981\u6c42\u7528\u6237\u7acb\u5373\u63d0\u4f9b\u697c\u680b\u6570\u636e\u3002\u8f85\u5bfc\u5458\u8def\u7531\u5df2100%\u8986\u76d6\u3002\u6b64\u95ee\u9898\u963b\u585ePhase 0\u9a8c\u8bc1\u901a\u8fc7\u53caPhase 1-5\u5b9e\u65bd\u3002", "task_id": "TASK-20260605-04", "artifacts": ["/home/caohui/projects/graduation-leave-system/.omc/collaboration/tasks/TASK-20260605-04-phase-0-p0\u963b\u585e\uff1a116\u4e2afile2\u72ec\u6709\u5b66\u751f\u7f3a\u5c11\u697c\u680b.md"], "status": "task_open"}
{"id": 8, "type": "task_created", "agent": "claude", "timestamp": "2026-06-06T10:08:47.638971+00:00", "summary": "Created task: \u6570\u636e\u9a8c\u8bc1\u5b8c\u6210\uff1a271\u540d\u7814\u7a76\u751f\u5b66\u53f7\u5df2\u627e\u5230\uff08100%\u5339\u914d\uff09\uff0c\u53d1\u73b019\u540d\u989d\u5916\u7814\u7a76\u751f\uff0c\u65b0\u589e3\u540d\u7ba1\u7406\u5458\uff08\u542b\u515c\u5e95\u5bbf\u7ba1\u5458\uff09\uff0c\u9700\u5ba1\u67e5\u5bf9Phase 2-3\u6267\u884c\u903b\u8f91\u7684\u5f71\u54cd\uff1a1)\u515c\u5e95\u5bbf\u7ba1\u5458\u8def\u7531\u5b9e\u73b0\u65b9\u6848\u9009\u62e9 2)271\u4eba\u5b66\u53f7\u66f4\u65b0\u7b56\u7565 3)19\u540d\u989d\u5916\u7814\u7a76\u751f\u5904\u7406\u65b9\u5f0f 4)Phase 3\u6570\u636e\u5bfc\u5165\u4efb\u52a1\u8c03\u6574", "task_id": "TASK-20260606-08", "artifacts": ["/home/caohui/projects/graduation-leave-system/.omc/collaboration/tasks/TASK-20260606-08-\u6570\u636e\u9a8c\u8bc1\u5b8c\u6210\uff1a271\u540d\u7814\u7a76\u751f\u5b66\u53f7\u5df2\u627e\u5230\uff08100%\u5339\u914d\uff09\uff0c\u53d1\u73b0.md"], "status": "task_open"}
{"id": 9, "type": "handoff_requested", "agent": "claude", "timestamp": "2026-06-06T10:10:03.804457+00:00", "summary": "handoff to codex for execution logic adjustment review", "task_id": "TASK-20260606-08", "status": "waiting"}
{"id": 10, "type": "task_claimed", "agent": "codex", "timestamp": "2026-06-06T10:16:51.870139+00:00", "task_id": "TASK-20260606-08", "summary": "Codex claimed Phase 0 execution logic adjustment review", "status": "in_progress"}
{"id": 11, "type": "artifact_created", "agent": "codex", "timestamp": "2026-06-06T10:20:50.992679+00:00", "task_id": "TASK-20260606-08", "summary": "Codex Phase 0 execution logic adjustment review artifact created", "artifacts": [".omc/collaboration/artifacts/20260606-1019-codex-phase0-execution-logic-review.md"], "status": "in_progress"}
{"id": 12, "type": "completed", "agent": "codex", "timestamp": "2026-06-06T10:20:50.992679+00:00", "task_id": "TASK-20260606-08", "summary": "Codex completed Phase 0 execution logic adjustment review", "artifacts": [".omc/collaboration/artifacts/20260606-1019-codex-phase0-execution-logic-review.md"], "status": "completed"}

exec
/bin/bash -lc 'rtk cat ../.omc/collaboration/state.json' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
{
  "workflow_id": "implementation-plan-review",
  "current_task": "TASK-20260606-08",
  "active_agent": "none",
  "status": "completed",
  "last_event_id": 12,
  "updated_at": "2026-06-06T10:20:50.992679+00:00"
}

codex
我还会抽查导入命令、用户模型和当前数据库计数，避免只根据任务描述做判断。重点是确认这些“额外用户”是否可进入路由、权限和统计路径。
exec
/bin/bash -lc "rtk sed -n '1,220p' ../docs/19名额外研究生待确认清单.md" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
# 19名额外研究生待确认清单

**日期：** 2026-06-06  
**来源：** 290人研究生文件 + "无入住信息"文件  
**状态：** 待用户确认

---

## 基本情况

**发现：** 19名研究生出现在290人研究生文件和"无入住信息"文件中，但不在File1/File2/File5（5946人主批次）中。

**学号特征：** 2021045xxx, 2022045xxx, 2023045xxx（非2026届特征）

---

## 数据来源

1. **290人研究生文件：** `docs/硕士研究生-毕业生290人.xls`
   - 包含这19人的姓名和学号

2. **无入住信息文件：** `docs/1-无入住信息.xls`
   - 包含这19人的记录（标记为无入住信息）

3. **主批次数据：** `backend/data/file5_students_merged.csv`
   - **不包含**这19人

---

## 需要用户确认的问题

### 1. 是否属于2026届毕业离校范围？

**疑点：**
- 学号前缀为2021/2022/2023，可能是往届生
- 不在主批次File1/File2中
- 标记为"无入住信息"

**请确认：**
- [ ] 这19人是否属于2026届毕业生？
- [ ] 是否需要办理2026年离校手续？
- [ ] 还是已在往年批次处理？

### 2. 是否应进入本系统主批次？

**当前主批次口径：** 5946人（File1 5830 + File2独有116 + File2临时ID271）

**选项：**
- [ ] 纳入主批次（需重新定义口径为5965人）
- [ ] 作为单独补充批次
- [ ] 不纳入系统

### 3. 缺失的关键字段

如需纳入系统，以下字段需要补充：

| 字段 | 当前状态 | 用途 |
|------|----------|------|
| 学院/班级 | ❓ 未知 | 辅导员路由 |
| 楼栋信息 | ❌ 无 | 宿管员路由 |
| 辅导员映射 | ❓ 未知 | 审批流程 |
| 毕业状态 | ❓ 未知 | 是否符合离校条件 |

### 4. 路由策略

**宿管员审批：**
- [ ] 无楼栋信息，是否走兜底宿管员程婷（92008149）审批？
- [ ] 还是需要补充楼栋信息？

**辅导员审批：**
- [ ] 是否有明确的学院/辅导员映射？
- [ ] 辅导员是否已在File4中？

---

## 19人清单

**数据文件：**
- 对比分析：`docs/无楼栋信息学生对比表.csv`（第118-136行）
- 研究生分析：`docs/271名研究生学号比对分析报告.md`

**关键信息：**
- 总人数：19人
- 来源一致性：290人文件和无入住信息文件100%重合
- 与主批次关系：完全不在File1/File2/File5中

---

## 建议处理方案

### 方案A：暂不纳入（推荐）

**理由：**
- 学号特征显示可能非2026届
- 缺少关键字段，无法立即路由
- 不影响5946人主批次验收

**后续：**
- 用户确认属于2026届后，作为Phase 3.5补充批次
- 补齐字段后单独导入

### 方案B：立即纳入

**前提条件：**
- 用户书面确认属于2026届
- 补充学院/班级/辅导员映射
- 确定宿管员路由策略（无楼栋走兜底 or 补充楼栋）

**影响：**
- 主批次口径变为5965人
- 需要验证新增19人的路由覆盖率

---

## 决策记录

**决策人：** _____________  
**决策日期：** _____________  
**决策结果：** 

- [ ] 方案A：暂不纳入，等待进一步确认
- [ ] 方案B：立即纳入，已补充字段（附件：___________）

**补充说明：**

---

---

**参考文档：**
- `docs/missing_building_data_discrepancy_analysis.md`
- `docs/271名研究生学号比对分析报告.md`
- `.omc/collaboration/artifacts/20260606-consensus-phase0-execution-logic-adjustment.md`

exec
/bin/bash -lc "rtk rg --files apps scripts data | rtk rg 'import_(students|staff)|models.py|serializers.py|views.py|urls.py|csv"'$|xlsx?$'"'" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
data/templates/counselors_template.csv
data/templates/class_mappings_template.csv
data/templates/students_template.csv
data/file5_students_merged_v2.csv
data/counselors_processed.csv
data/2026届预计毕业生5675人.csv
data/missing_building_data_request.csv
data/missing_student_no_request.csv
data/file5_students_merged.csv
data/dorm_managers_processed.csv
data/2026年学院辅导员信息统计表.csv
data/1-5830名毕业生（含研究生）.csv
data/2026年社区辅导员信息统计表.csv
data/additional_staff.csv
data/missing_student_no_filled.csv
apps/approvals/urls.py
apps/approvals/views.py
apps/approvals/serializers.py
apps/approvals/models.py
apps/applications/urls.py
apps/applications/serializers.py
apps/applications/models.py
apps/applications/views.py
apps/notifications/urls.py
apps/attachments/urls.py
apps/notifications/tests/test_models.py
apps/notifications/views.py
apps/notifications/serializers.py
apps/notifications/models.py
apps/attachments/views.py
apps/attachments/serializers.py
apps/attachments/models.py
apps/users/management/commands/import_students.py
apps/users/management/commands/import_staff.py
apps/users/urls.py
apps/users/views.py
apps/users/serializers.py
apps/users/models.py

exec
/bin/bash -lc "rtk rg -n \"class User|role|building|department|import_students|import_staff|Leave|Application|approval|route|routing|STUDENT|COUNSELOR|DORM\" apps scripts config data docs -g '*.py' -g '*.md'" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
config/urls.py:11:    path('api/approvals/', include('apps.approvals.urls')),
config/settings/base.py:17:# Application definition
config/settings/base.py:36:    'apps.approvals',
config/settings/base.py:159:# Fallback dorm manager for students without building assignment
config/settings/base.py:160:FALLBACK_DORM_MANAGER_USER_ID = '92008149'
apps/approvals/validators.py:1:from apps.applications.models import ApplicationStatus
apps/approvals/validators.py:5:    'dorm_manager': ApplicationStatus.PENDING_DORM_MANAGER,
apps/approvals/validators.py:6:    'counselor': ApplicationStatus.PENDING_COUNSELOR,
apps/approvals/validators.py:10:def approval_step_matches_application_status(approval):
apps/approvals/validators.py:11:    expected_status = EXPECTED_STATUS_BY_STEP.get(approval.step)
apps/approvals/validators.py:14:    return approval.application.status == expected_status
apps/approvals/admin.py:7:    list_display = ['approval_id', 'application', 'step', 'approver', 'decision', 'decided_at']
apps/approvals/admin.py:9:    search_fields = ['approval_id', 'application__application_id', 'approver__user_id']
apps/approvals/urls.py:5:    path('', views.list_approvals, name='list_approvals'),
apps/approvals/urls.py:6:    path('<str:approval_id>/approve/', views.approve_approval, name='approve_approval'),
apps/approvals/urls.py:7:    path('<str:approval_id>/reject/', views.reject_approval, name='reject_approval'),
apps/approvals/models.py:3:from apps.applications.models import Application
apps/approvals/models.py:7:    DORM_MANAGER = 'dorm_manager', '宿管员'
apps/approvals/models.py:8:    COUNSELOR = 'counselor', '辅导员'
apps/approvals/models.py:19:    approval_id = models.CharField(max_length=50, primary_key=True)
apps/approvals/models.py:20:    application = models.ForeignKey(Application, on_delete=models.PROTECT, related_name='approvals')
apps/approvals/models.py:22:    approver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='approvals')
apps/approvals/models.py:31:        db_table = 'approvals'
apps/approvals/migrations/0003_alter_approval_step.py:9:        ('approvals', '0002_initial'),
apps/approvals/migrations/0003_alter_approval_step.py:14:            model_name='approval',
apps/approvals/migrations/0002_initial.py:14:        ('approvals', '0001_initial'),
apps/approvals/migrations/0002_initial.py:19:            model_name='approval',
apps/approvals/migrations/0002_initial.py:21:            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='approvals', to=settings.AUTH_USER_MODEL),
apps/approvals/migrations/0001_initial.py:19:                ('approval_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
apps/approvals/migrations/0001_initial.py:27:                ('application', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='approvals', to='applications.application')),
apps/approvals/migrations/0001_initial.py:30:                'db_table': 'approvals',
scripts/merge_student_data.py:71:            building = row['楼栋名称'].strip()
scripts/merge_student_data.py:108:                building=building,
scripts/merge_student_data.py:131:                'department': college_norm,
scripts/merge_student_data.py:136:                'building_name': building,
scripts/merge_student_data.py:162:                'department': college_norm,
scripts/merge_student_data.py:167:                'building_name': '',  # Not in File2
apps/applications/admin.py:2:from .models import Application
apps/applications/admin.py:5:@admin.register(Application)
apps/applications/admin.py:6:class ApplicationAdmin(admin.ModelAdmin):
scripts/validate_routing_coverage.py:3:Validate routing coverage for all students.
scripts/validate_routing_coverage.py:4:Ensures every student can be routed to dorm manager and counselor.
scripts/validate_routing_coverage.py:30:    Returns: {building_name: [manager_ids]}
scripts/validate_routing_coverage.py:32:    building_managers = defaultdict(list)
scripts/validate_routing_coverage.py:38:            building = row['楼栋号'].strip()
scripts/validate_routing_coverage.py:42:                building_managers[building].append(manager_id)
scripts/validate_routing_coverage.py:44:    return dict(building_managers)
scripts/validate_routing_coverage.py:50:    Returns: {department: counselor_id}
scripts/validate_routing_coverage.py:58:            department_raw = row['学院'].strip()
scripts/validate_routing_coverage.py:63:                    # Normalize department name to match File5
scripts/validate_routing_coverage.py:64:                    department_norm = normalize_college_name(department_raw)
scripts/validate_routing_coverage.py:65:                    dept_counselors[department_norm] = counselor_id
scripts/validate_routing_coverage.py:67:                    # Skip departments that can't be normalized
scripts/validate_routing_coverage.py:73:def validate_routing(file5_path: str, file3_path: str, file4_path: str) -> dict:
scripts/validate_routing_coverage.py:75:    Validate that all students can be routed to approvers.
scripts/validate_routing_coverage.py:80:    building_managers = load_dorm_managers(file3_path)
scripts/validate_routing_coverage.py:96:        building = student['building_name']
scripts/validate_routing_coverage.py:97:        department = student['department']
scripts/validate_routing_coverage.py:99:        # Check dorm manager routing
scripts/validate_routing_coverage.py:100:        has_dorm_manager = building in building_managers
scripts/validate_routing_coverage.py:107:                'building': building
scripts/validate_routing_coverage.py:110:        # Check counselor routing
scripts/validate_routing_coverage.py:111:        has_counselor = department in dept_counselors
scripts/validate_routing_coverage.py:118:                'department': department
scripts/validate_routing_coverage.py:121:        # Check full routing
scripts/validate_routing_coverage.py:128:                'building': building,
scripts/validate_routing_coverage.py:129:                'department': department,
scripts/validate_routing_coverage.py:148:    parser = argparse.ArgumentParser(description='Validate routing coverage')
scripts/validate_routing_coverage.py:156:    print("Validating routing coverage...")
scripts/validate_routing_coverage.py:157:    report = validate_routing(args.file5, args.file3, args.file4)
scripts/validate_routing_coverage.py:167:        print("\n✓ PASS: 100% routing coverage achieved")
scripts/validate_routing_coverage.py:170:        print(f"\n✗ FAIL: {len(report['unroutable_students'])} students cannot be routed")
scripts/validate_routing_coverage.py:171:        print("\nMissing dorm managers for buildings:")
scripts/validate_routing_coverage.py:172:        missing_buildings = set(s['building'] for s in report['missing_dorm_manager'])
scripts/validate_routing_coverage.py:173:        for building in sorted(missing_buildings):
scripts/validate_routing_coverage.py:174:            count = sum(1 for s in report['missing_dorm_manager'] if s['building'] == building)
scripts/validate_routing_coverage.py:175:            print(f"  - {building}: {count} students")
scripts/validate_routing_coverage.py:177:        print("\nMissing counselors for departments:")
scripts/validate_routing_coverage.py:178:        missing_depts = set(s['department'] for s in report['missing_counselor'])
scripts/validate_routing_coverage.py:180:            count = sum(1 for s in report['missing_counselor'] if s['department'] == dept)
scripts/xg_api_collection_test.py:135:                'department': 0,
scripts/xg_api_collection_test.py:143:                if user.get('department') and len(user['department']) > 0:
scripts/xg_api_collection_test.py:144:                    related_stats['department'] += 1
apps/applications/providers.py:51:                provider_error_code="STUDENT_NOT_FOUND"
apps/applications/pagination.py:5:class ApplicationLimitOffsetPagination(LimitOffsetPagination):
scripts/normalize_colleges.py:4:Maps File1 college names to File4 counselor department names.
scripts/generate_temp_user_ids.py:10:def generate_grad_user_id(name: str, college: str, building: str, room: str) -> str:
scripts/generate_temp_user_ids.py:16:    data = f"{name}|{college}|{building}|{room}".encode('utf-8')
scripts/generate_temp_user_ids.py:33:    building: str,
scripts/generate_temp_user_ids.py:45:        building: Building name
scripts/generate_temp_user_ids.py:60:        grad_id = generate_grad_user_id(name, college, building, room)
apps/approvals/serializers.py:6:    """Lean serializer for approval lists - includes created_at"""
apps/approvals/serializers.py:12:        fields = ['approval_id', 'application_id', 'step', 'approver_id',
apps/approvals/serializers.py:14:        read_only_fields = ['approval_id', 'application_id', 'step',
apps/approvals/serializers.py:24:        fields = ['approval_id', 'application_id', 'step', 'approver_id',
apps/approvals/serializers.py:26:        read_only_fields = ['approval_id', 'application_id', 'step',
apps/approvals/serializers.py:35:    """Schema-only: approval list response with pagination"""
apps/approvals/views.py:12:from .validators import approval_step_matches_application_status
apps/approvals/views.py:13:from apps.applications.models import Application, ApplicationStatus
apps/approvals/views.py:15:from apps.notifications.services import notify_approval_decided
apps/approvals/views.py:21:    operation_id='approvals_list',
apps/approvals/views.py:37:def list_approvals(request):
apps/approvals/views.py:41:    if user.role == UserRole.STUDENT:
apps/approvals/views.py:48:    if user.role == UserRole.DORM_MANAGER:
apps/approvals/views.py:51:            step=ApprovalStep.DORM_MANAGER
apps/approvals/views.py:55:    elif user.role == UserRole.COUNSELOR:
apps/approvals/views.py:58:            step=ApprovalStep.COUNSELOR
apps/approvals/views.py:62:    elif user.role == UserRole.DEAN:
apps/approvals/views.py:77:    queryset = queryset.order_by('-created_at', '-approval_id')
apps/approvals/views.py:90:    operation_id='approvals_approve',
apps/approvals/views.py:106:def approve_approval(request, approval_id):
apps/approvals/views.py:108:        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
apps/approvals/views.py:114:    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
apps/approvals/views.py:117:    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
apps/approvals/views.py:120:    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
apps/approvals/views.py:124:    if approval.approver_id != user.user_id:
apps/approvals/views.py:128:    if approval.decision != ApprovalDecision.PENDING:
apps/approvals/views.py:132:    if not approval_step_matches_application_status(approval):
apps/approvals/views.py:141:    approval.decision = ApprovalDecision.APPROVED
apps/approvals/views.py:142:    approval.comment = serializer.validated_data.get('comment', '')
apps/approvals/views.py:143:    approval.decided_at = timezone.now()
apps/approvals/views.py:144:    approval.save()
apps/approvals/views.py:146:    notify_approval_decided(approval)
apps/approvals/views.py:148:    application = approval.application
apps/approvals/views.py:149:    if approval.step == ApprovalStep.DORM_MANAGER:
apps/approvals/views.py:150:        # Check for existing counselor approval to prevent duplicates
apps/approvals/views.py:151:        existing_counselor_approval = Approval.objects.filter(
apps/approvals/views.py:153:            step=ApprovalStep.COUNSELOR
apps/approvals/views.py:156:        if existing_counselor_approval:
apps/approvals/views.py:160:        application.status = ApplicationStatus.PENDING_COUNSELOR
apps/approvals/views.py:163:        # Get counselor by department
apps/approvals/views.py:165:            counselor = User.objects.get(role=UserRole.COUNSELOR, department=application.student.department, active=True)
apps/approvals/views.py:168:                                        'details': {'department': application.student.department}}},
apps/approvals/views.py:172:            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
apps/approvals/views.py:174:            step=ApprovalStep.COUNSELOR,
apps/approvals/views.py:179:    elif approval.step == ApprovalStep.COUNSELOR:
apps/approvals/views.py:180:        # Counselor approval completes the process (2-level approval)
apps/approvals/views.py:181:        application.status = ApplicationStatus.APPROVED
apps/approvals/views.py:184:    return Response(ApprovalSerializer(approval).data)
apps/approvals/views.py:188:    operation_id='approvals_reject',
apps/approvals/views.py:204:def reject_approval(request, approval_id):
apps/approvals/views.py:206:        approval = Approval.objects.select_for_update().get(approval_id=approval_id)
apps/approvals/views.py:212:    if approval.step == ApprovalStep.DORM_MANAGER and user.role != UserRole.DORM_MANAGER:
apps/approvals/views.py:215:    if approval.step == ApprovalStep.COUNSELOR and user.role != UserRole.COUNSELOR:
apps/approvals/views.py:218:    if approval.step == ApprovalStep.DEAN and user.role != UserRole.DEAN:
apps/approvals/views.py:222:    if approval.approver_id != user.user_id:
apps/approvals/views.py:226:    if approval.decision != ApprovalDecision.PENDING:
apps/approvals/views.py:230:    if not approval_step_matches_application_status(approval):
apps/approvals/views.py:239:    approval.decision = ApprovalDecision.REJECTED
apps/approvals/views.py:240:    approval.comment = serializer.validated_data.get('comment', '')
apps/approvals/views.py:241:    approval.decided_at = timezone.now()
apps/approvals/views.py:242:    approval.save()
apps/approvals/views.py:244:    notify_approval_decided(approval)
apps/approvals/views.py:246:    application = approval.application
apps/approvals/views.py:247:    application.status = ApplicationStatus.REJECTED
apps/approvals/views.py:250:    return Response(ApprovalSerializer(approval).data)
docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:40:- `apps/approvals/tests/test_rejection_flow.py`
docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:77:  apps.approvals.tests.test_rejection_flow
docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensus.md:154:4. `apps/approvals/tests/test_rejection_flow.py` - 添加ClassMapping
apps/applications/migrations/0001_initial.py:15:            name='Application',
apps/approvals/tests/test_state_machine.py:5:from apps.applications.models import Application, ApplicationStatus
apps/approvals/tests/test_state_machine.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
apps/approvals/tests/test_state_machine.py:16:            role=UserRole.STUDENT,
apps/approvals/tests/test_state_machine.py:25:            role=UserRole.COUNSELOR,
apps/approvals/tests/test_state_machine.py:33:            role=UserRole.DORM_MANAGER,
apps/approvals/tests/test_state_machine.py:41:            role=UserRole.DEAN,
apps/approvals/tests/test_state_machine.py:56:        self.application = Application.objects.create(
apps/approvals/tests/test_state_machine.py:63:            status=ApplicationStatus.PENDING_COUNSELOR
apps/approvals/tests/test_state_machine.py:66:        # Create counselor approval
apps/approvals/tests/test_state_machine.py:67:        self.approval = Approval.objects.create(
apps/approvals/tests/test_state_machine.py:68:            approval_id='apv_test001',
apps/approvals/tests/test_state_machine.py:70:            step=ApprovalStep.COUNSELOR,
apps/approvals/tests/test_state_machine.py:78:    def test_duplicate_approval_conflict(self):
apps/approvals/tests/test_state_machine.py:82:        # First approval
apps/approvals/tests/test_state_machine.py:84:            f'/api/approvals/{self.approval.approval_id}/approve/',
apps/approvals/tests/test_state_machine.py:90:        # Second approval attempt
apps/approvals/tests/test_state_machine.py:92:            f'/api/approvals/{self.approval.approval_id}/approve/',
apps/approvals/tests/test_state_machine.py:103:            f'/api/approvals/{self.approval.approval_id}/reject/',
apps/approvals/tests/test_state_machine.py:110:            f'/api/approvals/{self.approval.approval_id}/reject/',
apps/approvals/tests/test_state_machine.py:118:        self.application.status = ApplicationStatus.PENDING_DORM_MANAGER
apps/approvals/tests/test_state_machine.py:123:            f'/api/approvals/{self.approval.approval_id}/approve/',
apps/approvals/tests/test_state_machine.py:128:            f'/api/approvals/{self.approval.approval_id}/reject/',
apps/approvals/tests/test_state_machine.py:138:        self.application.status = ApplicationStatus.APPROVED
apps/approvals/tests/test_state_machine.py:140:        dorm_manager_approval = Approval.objects.create(
apps/approvals/tests/test_state_machine.py:141:            approval_id='apv_test002',
apps/approvals/tests/test_state_machine.py:143:            step=ApprovalStep.DORM_MANAGER,
apps/approvals/tests/test_state_machine.py:151:            f'/api/approvals/{dorm_manager_approval.approval_id}/approve/',
apps/approvals/tests/test_state_machine.py:156:            f'/api/approvals/{dorm_manager_approval.approval_id}/reject/',
apps/approvals/tests/test_permissions.py:5:from apps.applications.models import Application, ApplicationStatus
apps/approvals/tests/test_permissions.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
apps/approvals/tests/test_permissions.py:16:            role=UserRole.STUDENT,
apps/approvals/tests/test_permissions.py:23:            role=UserRole.STUDENT,
apps/approvals/tests/test_permissions.py:32:            role=UserRole.COUNSELOR,
apps/approvals/tests/test_permissions.py:38:            role=UserRole.COUNSELOR,
apps/approvals/tests/test_permissions.py:44:            role=UserRole.DORM_MANAGER,
apps/approvals/tests/test_permissions.py:50:            role=UserRole.DORM_MANAGER,
apps/approvals/tests/test_permissions.py:56:            role=UserRole.DEAN,
apps/approvals/tests/test_permissions.py:62:            role=UserRole.DEAN,
apps/approvals/tests/test_permissions.py:85:        self.application1 = Application.objects.create(
apps/approvals/tests/test_permissions.py:92:            status=ApplicationStatus.PENDING_COUNSELOR
apps/approvals/tests/test_permissions.py:95:        # Create counselor approval for application1
apps/approvals/tests/test_permissions.py:96:        self.approval1 = Approval.objects.create(
apps/approvals/tests/test_permissions.py:97:            approval_id='apv_test001',
apps/approvals/tests/test_permissions.py:99:            step=ApprovalStep.COUNSELOR,
apps/approvals/tests/test_permissions.py:107:    def _create_dorm_manager_approval(self):
apps/approvals/tests/test_permissions.py:108:        self.application1.status = ApplicationStatus.PENDING_DORM_MANAGER
apps/approvals/tests/test_permissions.py:111:            approval_id='apv_test002',
apps/approvals/tests/test_permissions.py:113:            step=ApprovalStep.DORM_MANAGER,
apps/approvals/tests/test_permissions.py:124:            f'/api/approvals/{self.approval1.approval_id}/approve/',
apps/approvals/tests/test_permissions.py:129:            f'/api/approvals/{self.approval1.approval_id}/reject/',
apps/approvals/tests/test_permissions.py:142:            f'/api/approvals/{self.approval1.approval_id}/approve/',
apps/approvals/tests/test_permissions.py:151:        dorm_manager_approval = self._create_dorm_manager_approval()
apps/approvals/tests/test_permissions.py:155:            f'/api/approvals/{dorm_manager_approval.approval_id}/approve/',
apps/approvals/tests/test_permissions.py:164:        dorm_manager_approval = self._create_dorm_manager_approval()
apps/approvals/tests/test_permissions.py:168:            f'/api/approvals/{dorm_manager_approval.approval_id}/reject/',
apps/approvals/tests/test_permissions.py:180:            f'/api/approvals/{self.approval1.approval_id}/approve/',
apps/approvals/tests/test_permissions.py:191:            f'/api/approvals/{self.approval1.approval_id}/reject/',
apps/approvals/tests/test_rejection_flow.py:8:from apps.applications.models import Application, ApplicationStatus
apps/approvals/tests/test_rejection_flow.py:9:from apps.approvals.models import ApprovalDecision, ApprovalStep
apps/approvals/tests/test_rejection_flow.py:20:            role=UserRole.STUDENT,
apps/approvals/tests/test_rejection_flow.py:30:            role=UserRole.COUNSELOR
apps/approvals/tests/test_rejection_flow.py:37:            role=UserRole.DORM_MANAGER
apps/approvals/tests/test_rejection_flow.py:73:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
apps/approvals/tests/test_rejection_flow.py:76:        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/approve/', {
apps/approvals/tests/test_rejection_flow.py:91:        application = Application.objects.get(application_id=application_id)
apps/approvals/tests/test_rejection_flow.py:92:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
apps/approvals/tests/test_rejection_flow.py:95:        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/reject/', {
apps/approvals/tests/test_rejection_flow.py:102:        self.assertEqual(application.status, ApplicationStatus.REJECTED)
apps/approvals/tests/test_rejection_flow.py:107:        application = Application.objects.get(application_id=application_id)
apps/approvals/tests/test_rejection_flow.py:118:        counselor_approval = application.approvals.get(step=ApprovalStep.COUNSELOR)
apps/approvals/tests/test_rejection_flow.py:121:        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/reject/', {
apps/approvals/tests/test_rejection_flow.py:129:        self.assertEqual(application.status, ApplicationStatus.REJECTED)
docs/discussions/week3-day3-planning-2026-05-30/05-claude-response-to-phase0-review.md:112:docker exec backend python manage.py test apps.applications.tests.test_application_flow apps.applications.tests.test_error_cases apps.approvals.tests.test_rejection_flow --keepdb
scripts/supplement_building_data.py:10:def update_file5_with_building_data(filled_csv_path: str, file5_path: str, output_path: str):
scripts/supplement_building_data.py:15:        filled_csv_path: 用户填写的CSV（backend/data/missing_building_data_request.csv）
scripts/supplement_building_data.py:19:    # Load filled building data
scripts/supplement_building_data.py:20:    building_data = {}
scripts/supplement_building_data.py:25:            building = row['楼栋名称（待补充）'].strip()
scripts/supplement_building_data.py:27:            if building:  # Only update if filled
scripts/supplement_building_data.py:28:                building_data[user_id] = {'building': building, 'room': room}
scripts/supplement_building_data.py:36:            if user_id in building_data:
scripts/supplement_building_data.py:37:                row['building_name'] = building_data[user_id]['building']
scripts/supplement_building_data.py:38:                row['room_number'] = building_data[user_id]['room']
scripts/supplement_building_data.py:49:    print(f"✓ Updated {len(building_data)} students with building data")
scripts/supplement_building_data.py:51:    return len(building_data)
scripts/supplement_building_data.py:55:    parser = argparse.ArgumentParser(description='Update File5 with building data from filled CSV')
scripts/supplement_building_data.py:56:    parser.add_argument('--filled-csv', required=True, help='User-filled CSV with building data')
scripts/supplement_building_data.py:62:    updated_count = update_file5_with_building_data(args.filled_csv, args.file5, args.output)
scripts/supplement_building_data.py:67:    print(f"  python3 manage.py import_students --file {args.output}")
apps/applications/permissions.py:3:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
apps/applications/permissions.py:8:    if user.role == UserRole.STUDENT:
apps/applications/permissions.py:11:    if user.role == UserRole.DORM_MANAGER:
apps/applications/permissions.py:18:    if user.role == UserRole.COUNSELOR:
apps/applications/permissions.py:25:    if user.role == UserRole.DEAN:
apps/applications/permissions.py:26:        # Dean archives completed applications and does not participate in approval.
apps/applications/views.py:8:from .models import Application, ApplicationStatus, DormCheckoutStatus
apps/applications/views.py:9:from .serializers import ApplicationSerializer, ApplicationCreateSerializer, ApplicationListSerializer, ApplicationListResponseSerializer
apps/applications/views.py:10:from .pagination import ApplicationLimitOffsetPagination
apps/applications/views.py:13:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
apps/applications/views.py:31:        200: ApplicationListResponseSerializer,
apps/applications/views.py:41:    request=ApplicationCreateSerializer,
apps/applications/views.py:43:        201: ApplicationSerializer,
apps/applications/views.py:65:    if user.role == UserRole.STUDENT:
apps/applications/views.py:66:        queryset = Application.objects.filter(student=user)
apps/applications/views.py:68:    # Dorm Manager: applications with own pending dorm manager approvals
apps/applications/views.py:69:    elif user.role == UserRole.DORM_MANAGER:
apps/applications/views.py:70:        pending_approvals = Approval.objects.filter(
apps/applications/views.py:72:            step=ApprovalStep.DORM_MANAGER,
apps/applications/views.py:75:        queryset = Application.objects.filter(pk__in=pending_approvals)
apps/applications/views.py:77:    # Counselor: applications with own pending counselor approvals
apps/applications/views.py:78:    elif user.role == UserRole.COUNSELOR:
apps/applications/views.py:79:        pending_approvals = Approval.objects.filter(
apps/applications/views.py:81:            step=ApprovalStep.COUNSELOR,
apps/applications/views.py:84:        queryset = Application.objects.filter(pk__in=pending_approvals)
apps/applications/views.py:86:    # Dean: view all approved applications (archiving role)
apps/applications/views.py:87:    elif user.role == UserRole.DEAN:
apps/applications/views.py:88:        queryset = Application.objects.filter(status=ApplicationStatus.APPROVED)
apps/applications/views.py:105:    paginator = ApplicationLimitOffsetPagination()
apps/applications/views.py:109:    serializer = ApplicationListSerializer(page, many=True)
apps/applications/views.py:117:    if user.role != UserRole.STUDENT:
apps/applications/views.py:122:    existing = Application.objects.filter(
apps/applications/views.py:124:        status__in=[ApplicationStatus.PENDING_DORM_MANAGER, ApplicationStatus.PENDING_COUNSELOR, ApplicationStatus.APPROVED]
apps/applications/views.py:131:    serializer = ApplicationCreateSerializer(data=request.data)
apps/applications/views.py:141:        return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
apps/applications/views.py:148:    building = user.building
apps/applications/views.py:150:    # Try to find dorm manager by building
apps/applications/views.py:151:    if building and building.strip():
apps/applications/views.py:153:            dorm_manager = User.objects.get(role=UserRole.DORM_MANAGER, building=building, active=True)
apps/applications/views.py:157:            dorm_manager = User.objects.filter(role=UserRole.DORM_MANAGER, building=building, active=True).first()
apps/applications/views.py:159:    # Fallback: use default dorm manager for students without building
apps/applications/views.py:162:        fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')
apps/applications/views.py:164:            dorm_manager = User.objects.get(role=UserRole.DORM_MANAGER, user_id=fallback_id, active=True)
apps/applications/views.py:167:                                        'details': {'building': building or '未分配', 'fallback_id': fallback_id}}},
apps/applications/views.py:172:    application = Application.objects.create(
apps/applications/views.py:179:        status=ApplicationStatus.PENDING_DORM_MANAGER,
apps/applications/views.py:183:    dorm_manager_approval = Approval.objects.create(
apps/applications/views.py:184:        approval_id=f'apv_{uuid.uuid4().hex[:8]}',
apps/applications/views.py:186:        step=ApprovalStep.DORM_MANAGER,
apps/applications/views.py:192:    notify_application_submitted(application, dorm_manager_approval)
apps/applications/views.py:194:    return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
apps/applications/views.py:202:        200: ApplicationSerializer,
apps/applications/views.py:212:        application = Application.objects.get(application_id=application_id)
apps/applications/views.py:213:    except Application.DoesNotExist:
apps/applications/views.py:225:    return Response(ApplicationSerializer(application).data)
apps/applications/models.py:6:class ApplicationStatus(models.TextChoices):
apps/applications/models.py:8:    PENDING_DORM_MANAGER = 'pending_dorm_manager', '待宿管员审批'
apps/applications/models.py:9:    PENDING_COUNSELOR = 'pending_counselor', '待辅导员审批'
apps/applications/models.py:21:class Application(models.Model):
apps/applications/models.py:28:    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.DRAFT)
apps/applications/models.py:38:            ApplicationStatus.PENDING_DORM_MANAGER,
apps/applications/models.py:39:            ApplicationStatus.PENDING_COUNSELOR,
apps/applications/models.py:40:            ApplicationStatus.APPROVED,
apps/applications/models.py:43:            existing = Application.objects.filter(
apps/applications/serializers.py:2:from .models import Application
apps/applications/serializers.py:5:class ApplicationListSerializer(serializers.ModelSerializer):
apps/applications/serializers.py:6:    """Lean serializer for application lists - no nested approvals"""
apps/applications/serializers.py:10:        model = Application
apps/applications/serializers.py:17:class ApplicationSerializer(serializers.ModelSerializer):
apps/applications/serializers.py:19:    approvals = serializers.SerializerMethodField()
apps/applications/serializers.py:22:        model = Application
apps/applications/serializers.py:25:                  'approvals', 'created_at', 'updated_at']
apps/applications/serializers.py:30:    def get_approvals(self, obj):
apps/applications/serializers.py:31:        from apps.approvals.serializers import ApprovalSerializer
apps/applications/serializers.py:32:        return ApprovalSerializer(obj.approvals.all(), many=True).data
apps/applications/serializers.py:35:class ApplicationCreateSerializer(serializers.Serializer):
apps/applications/serializers.py:52:class ApplicationListResponseSerializer(serializers.Serializer):
apps/applications/serializers.py:55:    results = ApplicationListSerializer(many=True)
apps/users/serializers.py:6:class UserSerializer(serializers.ModelSerializer):
apps/users/serializers.py:9:        fields = ['user_id', 'name', 'role', 'class_id', 'active', 'is_graduating', 'graduation_year']
apps/users/serializers.py:17:        fields = ['user_id', 'name', 'role', 'class_id']
apps/users/models.py:5:class UserRole(models.TextChoices):
apps/users/models.py:6:    STUDENT = 'student', '学生'
apps/users/models.py:7:    DORM_MANAGER = 'dorm_manager', '宿管员'
apps/users/models.py:8:    COUNSELOR = 'counselor', '辅导员'
apps/users/models.py:13:class UserManager(BaseUserManager):
apps/users/models.py:29:class User(AbstractBaseUser, PermissionsMixin):
apps/users/models.py:32:    role = models.CharField(max_length=20, choices=UserRole.choices)
apps/users/models.py:41:    department = models.CharField(max_length=100, null=True, blank=True)
apps/users/models.py:42:    building = models.CharField(max_length=100, null=True, blank=True)
apps/users/models.py:51:    REQUIRED_FIELDS = ['name', 'role']
apps/users/integrations/xg_user_mapper.py:15:            'role': str | None,
apps/users/integrations/xg_user_mapper.py:18:            'department': str | None,
apps/users/integrations/xg_user_mapper.py:28:        'role': None,
apps/users/integrations/xg_user_mapper.py:31:        'department': None,
apps/users/integrations/xg_user_mapper.py:44:    department_raw = xg_user.get('department')
apps/users/integrations/xg_user_mapper.py:46:    # 处理department数组: [{"name": "计算机学院", "level": 2}]
apps/users/integrations/xg_user_mapper.py:47:    department = None
apps/users/integrations/xg_user_mapper.py:48:    if isinstance(department_raw, list) and len(department_raw) > 0:
apps/users/integrations/xg_user_mapper.py:49:        if isinstance(department_raw[0], dict):
apps/users/integrations/xg_user_mapper.py:50:            department = department_raw[0].get('name')
apps/users/integrations/xg_user_mapper.py:51:    elif isinstance(department_raw, str):
apps/users/integrations/xg_user_mapper.py:53:        department = department_raw
apps/users/integrations/xg_user_mapper.py:70:    role = None
apps/users/integrations/xg_user_mapper.py:77:                role = 'student'
apps/users/integrations/xg_user_mapper.py:87:                role = 'student'
apps/users/integrations/xg_user_mapper.py:102:    result['role'] = role
apps/users/integrations/xg_user_mapper.py:105:    result['department'] = department
apps/approvals/tests/test_list_permissions.py:4:from apps.applications.models import Application, ApplicationStatus
apps/approvals/tests/test_list_permissions.py:5:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
apps/approvals/tests/test_list_permissions.py:13:        self.student = User.objects.create(user_id='S001', name='学生', role=UserRole.STUDENT, class_id='CS2020-01')
apps/approvals/tests/test_list_permissions.py:17:        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
apps/approvals/tests/test_list_permissions.py:21:        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
apps/approvals/tests/test_list_permissions.py:25:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
apps/approvals/tests/test_list_permissions.py:29:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
apps/approvals/tests/test_list_permissions.py:33:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
apps/approvals/tests/test_list_permissions.py:37:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
apps/approvals/tests/test_list_permissions.py:42:        self.app = Application.objects.create(
apps/approvals/tests/test_list_permissions.py:49:            status=ApplicationStatus.PENDING_COUNSELOR
apps/approvals/tests/test_list_permissions.py:52:        # Create approvals
apps/approvals/tests/test_list_permissions.py:53:        self.approval_c1 = Approval.objects.create(
apps/approvals/tests/test_list_permissions.py:54:            approval_id='apv_c1',
apps/approvals/tests/test_list_permissions.py:56:            step=ApprovalStep.COUNSELOR,
apps/approvals/tests/test_list_permissions.py:62:        self.approval_m1 = Approval.objects.create(
apps/approvals/tests/test_list_permissions.py:63:            approval_id='apv_m1',
apps/approvals/tests/test_list_permissions.py:65:            step=ApprovalStep.DORM_MANAGER,
apps/approvals/tests/test_list_permissions.py:71:    def test_student_403_on_approval_list(self):
apps/approvals/tests/test_list_permissions.py:73:        response = self.client.get('/api/approvals/')
apps/approvals/tests/test_list_permissions.py:77:    def test_counselor_sees_only_own_pending_approvals(self):
apps/approvals/tests/test_list_permissions.py:79:        response = self.client.get('/api/approvals/')
apps/approvals/tests/test_list_permissions.py:82:        self.assertEqual(response.data['results'][0]['approval_id'], 'apv_c1')
apps/approvals/tests/test_list_permissions.py:84:    def test_counselor_cannot_see_other_counselor_approvals(self):
apps/approvals/tests/test_list_permissions.py:86:        response = self.client.get('/api/approvals/')
apps/approvals/tests/test_list_permissions.py:89:    def test_dorm_manager_sees_only_own_pending_approvals(self):
apps/approvals/tests/test_list_permissions.py:91:        response = self.client.get('/api/approvals/')
apps/approvals/tests/test_list_permissions.py:94:        self.assertEqual(response.data['results'][0]['approval_id'], 'apv_m1')
apps/approvals/tests/test_list_permissions.py:96:    def test_dorm_manager_cannot_see_other_dorm_manager_approvals(self):
apps/approvals/tests/test_list_permissions.py:98:        response = self.client.get('/api/approvals/')
apps/approvals/tests/test_list_permissions.py:101:    def test_dean_sees_all_approvals_for_archive(self):
apps/approvals/tests/test_list_permissions.py:103:        response = self.client.get('/api/approvals/')
apps/approvals/tests/test_list_permissions.py:109:        response = self.client.get('/api/approvals/')
apps/approvals/tests/test_list_permissions.py:116:        # Create second application and approval for counselor1 (approved)
apps/approvals/tests/test_list_permissions.py:117:        app2 = Application.objects.create(
apps/approvals/tests/test_list_permissions.py:124:            status=ApplicationStatus.APPROVED
apps/approvals/tests/test_list_permissions.py:126:        approval_c1_approved = Approval.objects.create(
apps/approvals/tests/test_list_permissions.py:127:            approval_id='apv_c1_approved',
apps/approvals/tests/test_list_permissions.py:129:            step=ApprovalStep.COUNSELOR,
apps/approvals/tests/test_list_permissions.py:135:        # Create approval for counselor2
apps/approvals/tests/test_list_permissions.py:136:        app3 = Application.objects.create(
apps/approvals/tests/test_list_permissions.py:143:            status=ApplicationStatus.PENDING_COUNSELOR
apps/approvals/tests/test_list_permissions.py:145:        approval_c2 = Approval.objects.create(
apps/approvals/tests/test_list_permissions.py:146:            approval_id='apv_c2',
apps/approvals/tests/test_list_permissions.py:148:            step=ApprovalStep.COUNSELOR,
apps/approvals/tests/test_list_permissions.py:156:        response = self.client.get('/api/approvals/?decision=all')
apps/approvals/tests/test_list_permissions.py:160:        # Verify only counselor1's approvals returned
apps/approvals/tests/test_list_permissions.py:161:        approval_ids = [a['approval_id'] for a in response.data['results']]
apps/approvals/tests/test_list_permissions.py:162:        self.assertIn('apv_c1', approval_ids)
apps/approvals/tests/test_list_permissions.py:163:        self.assertIn('apv_c1_approved', approval_ids)
apps/approvals/tests/test_list_permissions.py:164:        self.assertNotIn('apv_c2', approval_ids)
apps/applications/tests/test_p0_fixes.py:3:from apps.applications.models import Application, ApplicationStatus
apps/applications/tests/test_p0_fixes.py:4:from apps.approvals.models import Approval, ApprovalDecision, ApprovalStep
apps/applications/tests/test_p0_fixes.py:16:            role=UserRole.STUDENT,
apps/applications/tests/test_p0_fixes.py:22:            role=UserRole.COUNSELOR
apps/applications/tests/test_p0_fixes.py:32:        app1 = Application.objects.create(
apps/applications/tests/test_p0_fixes.py:39:            status=ApplicationStatus.REJECTED
apps/applications/tests/test_p0_fixes.py:43:        app2 = Application.objects.create(
apps/applications/tests/test_p0_fixes.py:50:            status=ApplicationStatus.PENDING_COUNSELOR
apps/applications/tests/test_p0_fixes.py:53:        self.assertEqual(Application.objects.filter(student=self.student).count(), 2)
apps/applications/tests/test_p0_fixes.py:54:        self.assertEqual(app2.status, ApplicationStatus.PENDING_COUNSELOR)
apps/applications/tests/test_p0_fixes.py:58:        app1 = Application.objects.create(
apps/applications/tests/test_p0_fixes.py:65:            status=ApplicationStatus.PENDING_COUNSELOR
apps/applications/tests/test_p0_fixes.py:69:        app2 = Application(
apps/applications/tests/test_p0_fixes.py:76:            status=ApplicationStatus.PENDING_COUNSELOR
apps/applications/tests/test_p0_fixes.py:89:            role=UserRole.STUDENT,
apps/applications/tests/test_p0_fixes.py:95:            role=UserRole.COUNSELOR
apps/applications/tests/test_p0_fixes.py:98:        # Create applications with different approval states
apps/applications/tests/test_p0_fixes.py:99:        self.app_pending = Application.objects.create(
apps/applications/tests/test_p0_fixes.py:106:            status=ApplicationStatus.PENDING_COUNSELOR
apps/applications/tests/test_p0_fixes.py:109:        self.app_approved = Application.objects.create(
apps/applications/tests/test_p0_fixes.py:116:            status=ApplicationStatus.APPROVED
apps/applications/tests/test_p0_fixes.py:119:        self.app_rejected = Application.objects.create(
apps/applications/tests/test_p0_fixes.py:126:            status=ApplicationStatus.REJECTED
apps/applications/tests/test_p0_fixes.py:129:        # Create approvals
apps/applications/tests/test_p0_fixes.py:130:        self.approval_pending = Approval.objects.create(
apps/applications/tests/test_p0_fixes.py:131:            approval_id='apv_pending',
apps/applications/tests/test_p0_fixes.py:133:            step=ApprovalStep.COUNSELOR,
apps/applications/tests/test_p0_fixes.py:139:        self.approval_approved = Approval.objects.create(
apps/applications/tests/test_p0_fixes.py:140:            approval_id='apv_approved',
apps/applications/tests/test_p0_fixes.py:142:            step=ApprovalStep.COUNSELOR,
apps/applications/tests/test_p0_fixes.py:148:        self.approval_rejected = Approval.objects.create(
apps/applications/tests/test_p0_fixes.py:149:            approval_id='apv_rejected',
apps/applications/tests/test_p0_fixes.py:151:            step=ApprovalStep.COUNSELOR,
apps/applications/tests/test_p0_fixes.py:157:    def test_filter_pending_approvals(self):
apps/applications/tests/test_p0_fixes.py:158:        approvals = Approval.objects.filter(
apps/applications/tests/test_p0_fixes.py:162:        self.assertEqual(approvals.count(), 1)
apps/applications/tests/test_p0_fixes.py:163:        self.assertEqual(approvals.first().approval_id, 'apv_pending')
apps/applications/tests/test_p0_fixes.py:165:    def test_filter_approved_approvals(self):
apps/applications/tests/test_p0_fixes.py:166:        approvals = Approval.objects.filter(
apps/applications/tests/test_p0_fixes.py:170:        self.assertEqual(approvals.count(), 1)
apps/applications/tests/test_p0_fixes.py:171:        self.assertEqual(approvals.first().approval_id, 'apv_approved')
apps/applications/tests/test_p0_fixes.py:173:    def test_filter_rejected_approvals(self):
apps/applications/tests/test_p0_fixes.py:174:        approvals = Approval.objects.filter(
apps/applications/tests/test_p0_fixes.py:178:        self.assertEqual(approvals.count(), 1)
apps/applications/tests/test_p0_fixes.py:179:        self.assertEqual(approvals.first().approval_id, 'apv_rejected')
apps/applications/tests/test_p0_fixes.py:181:    def test_filter_all_approvals(self):
apps/applications/tests/test_p0_fixes.py:182:        approvals = Approval.objects.filter(approver=self.counselor)
apps/applications/tests/test_p0_fixes.py:183:        self.assertEqual(approvals.count(), 3)
apps/users/tests/test_xg_user_mapper.py:16:            'department': '计算机学院',
apps/users/tests/test_xg_user_mapper.py:24:        self.assertEqual(result['role'], 'student')
apps/users/tests/test_xg_user_mapper.py:27:        self.assertEqual(result['department'], '计算机学院')
apps/users/tests/test_xg_user_mapper.py:43:        self.assertEqual(result['role'], 'student')
apps/users/tests/test_xg_user_mapper.py:84:        self.assertIsNone(result['role'])
apps/users/tests/test_xg_user_mapper.py:98:        self.assertIsNone(result['role'])
apps/users/tests/test_xg_user_mapper.py:113:        self.assertEqual(result['role'], 'student')
apps/users/tests/test_xg_user_mapper.py:115:        self.assertIsNone(result['department'])
apps/users/tests/test_xg_user_mapper.py:134:            'department': [{'name': '计算机学院', 'level': 2}]
apps/users/tests/test_xg_user_mapper.py:141:        self.assertEqual(result['role'], 'student')
apps/users/tests/test_xg_user_mapper.py:143:        self.assertEqual(result['department'], '计算机学院')
apps/users/tests/test_xg_user_mapper.py:146:    def test_department_array_format(self):
apps/users/tests/test_xg_user_mapper.py:147:        """测试department数组格式"""
apps/users/tests/test_xg_user_mapper.py:152:            'department': [
apps/users/tests/test_xg_user_mapper.py:161:        self.assertEqual(result['department'], '计算机学院')
apps/users/tests/test_xg_user_mapper.py:178:    def test_department_empty_array(self):
apps/users/tests/test_xg_user_mapper.py:179:        """测试department空数组"""
apps/users/tests/test_xg_user_mapper.py:184:            'department': []
apps/users/tests/test_xg_user_mapper.py:189:        self.assertIsNone(result['department'])
apps/applications/tests/test_error_cases.py:8:from apps.applications.models import Application, ApplicationStatus
apps/applications/tests/test_error_cases.py:20:            role=UserRole.STUDENT,
apps/applications/tests/test_error_cases.py:30:            role=UserRole.STUDENT,
apps/applications/tests/test_error_cases.py:40:            role=UserRole.STUDENT,
apps/applications/tests/test_error_cases.py:50:            role=UserRole.COUNSELOR
apps/applications/tests/test_error_cases.py:56:            role=UserRole.DORM_MANAGER
apps/applications/tests/test_error_cases.py:63:            role=UserRole.DEAN
apps/applications/tests/test_error_cases.py:90:        self.assertEqual(response.data['error']['code'], 'DORM_BLOCKED')
apps/users/migrations/0001_initial.py:25:                ('role', models.CharField(choices=[('student', '学生'), ('counselor', '辅导员'), ('dean', '学工部')], max_length=20)),
apps/users/tests/test_xg_user_sync.py:18:            role='student',
apps/users/tests/test_xg_user_sync.py:29:            role='counselor',
apps/users/tests/test_xg_user_sync.py:59:                'department': '计算机学院'
apps/users/tests/test_xg_user_sync.py:99:    def test_local_role_conflict(self):
apps/users/tests/test_xg_user_sync.py:119:        self.assertEqual(conflict['reason'], 'role_mismatch')
apps/users/tests/test_xg_user_sync.py:120:        self.assertEqual(conflict['local_role'], 'counselor')
apps/users/tests/test_xg_user_sync.py:121:        self.assertEqual(conflict['api_role'], 'student')
apps/users/tests/test_xg_user_sync.py:156:                'department': '计算机学院'
apps/users/tests/test_xg_user_sync.py:169:        self.assertIn('phone/email/department', warning_text)
apps/users/tests/test_xg_user_sync.py:234:            role='student',
apps/users/tests/test_xg_user_sync.py:241:            department=''
apps/users/tests/test_xg_user_sync.py:246:            role='counselor',
apps/users/tests/test_xg_user_sync.py:258:            'department': '计算机学院'
apps/users/tests/test_xg_user_sync.py:267:        self.assertEqual(user.department, '计算机学院')
apps/users/tests/test_xg_user_sync.py:282:    def test_scenario3_skip_role_conflict(self):
apps/users/tests/test_xg_user_sync.py:283:        """场景3：检测并跳过role冲突(local非student)"""
apps/users/tests/test_xg_user_sync.py:290:        self.assertEqual(result['conflicts'][0]['reason'], 'role_mismatch')
apps/users/tests/test_xg_user_sync.py:310:            'department': '计算机学院'
apps/users/tests/test_xg_user_sync.py:319:        self.assertEqual(user.department, '')
apps/users/tests/test_xg_user_sync.py:326:            role='student',
apps/users/tests/test_xg_user_sync.py:370:            role='student',
apps/users/tests/test_xg_user_sync.py:383:        self.assertEqual(counselor.role, 'counselor')
apps/applications/tests/test_detail_permissions.py:5:from apps.applications.models import Application, ApplicationStatus
apps/applications/tests/test_detail_permissions.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
apps/applications/tests/test_detail_permissions.py:10:class ApplicationDetailPermissionTest(TestCase):
apps/applications/tests/test_detail_permissions.py:15:        self.student1 = User.objects.create(user_id='2020001', name='学生1', role=UserRole.STUDENT, class_id='CS2020-01')
apps/applications/tests/test_detail_permissions.py:19:        self.student2 = User.objects.create(user_id='2020002', name='学生2', role=UserRole.STUDENT, class_id='CS2020-02')
apps/applications/tests/test_detail_permissions.py:24:        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
apps/applications/tests/test_detail_permissions.py:28:        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
apps/applications/tests/test_detail_permissions.py:32:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
apps/applications/tests/test_detail_permissions.py:36:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
apps/applications/tests/test_detail_permissions.py:41:        self.dean1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
apps/applications/tests/test_detail_permissions.py:45:        self.dean2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
apps/applications/tests/test_detail_permissions.py:95:        # Dean archive role cannot access in-progress applications
apps/notifications/services.py:5:when key events occur (application submission, approval decisions).
apps/notifications/services.py:12:from apps.approvals.models import ApprovalDecision
apps/notifications/services.py:17:def notify_application_submitted(application, approval):
apps/notifications/services.py:22:        application: Application instance
apps/notifications/services.py:23:        approval: Counselor approval instance
apps/notifications/services.py:32:        recipient=approval.approver,
apps/notifications/services.py:33:        entity_type='approval',
apps/notifications/services.py:34:        entity_id=approval.pk,
apps/notifications/services.py:44:def notify_approval_decided(approval):
apps/notifications/services.py:46:    Create notification for student when approval is approved or rejected.
apps/notifications/services.py:49:        approval: Approval instance with decision
apps/notifications/services.py:54:    approver_role_map = {
apps/notifications/services.py:58:    approver_role = approver_role_map.get(approval.step, "审批人")
apps/notifications/services.py:60:    if approval.decision == ApprovalDecision.APPROVED:
apps/notifications/services.py:62:        message = f"您的离校申请已通过{approver_role}审批。"
apps/notifications/services.py:66:        message = f"您的离校申请被{approver_role}驳回。驳回原因：{approval.comment}"
apps/notifications/services.py:70:        recipient=approval.application.student,
apps/notifications/services.py:71:        entity_type='approval',
apps/notifications/services.py:72:        entity_id=approval.pk,
apps/notifications/services.py:75:            'actor': approval.approver,
apps/notifications/services.py:82:def create_approval_timeout_warnings(now=None, dry_run=False):
apps/notifications/services.py:84:    Create timeout warning notifications for pending approvals.
apps/notifications/services.py:93:    from apps.approvals.models import Approval
apps/notifications/services.py:101:    pending_approvals = Approval.objects.filter(
apps/notifications/services.py:109:    for approval in pending_approvals:
apps/notifications/services.py:110:        threshold = counselor_threshold if approval.step == 'counselor' else dorm_manager_threshold
apps/notifications/services.py:112:        if approval.created_at > threshold:
apps/notifications/services.py:115:        days = (now - approval.created_at).days
apps/notifications/services.py:117:        message = f"学生{approval.application.student_name}的离校申请已超过{days}天未审批，请及时处理。"
apps/notifications/services.py:121:                'approval_id': approval.pk,
apps/notifications/services.py:122:                'approver': approval.approver.name,
apps/notifications/services.py:128:                recipient=approval.approver,
apps/notifications/services.py:129:                entity_type='approval',
apps/notifications/services.py:130:                entity_id=approval.pk,
apps/notifications/services.py:142:                    'approval_id': approval.pk,
apps/notifications/services.py:143:                    'approver': approval.approver.name,
apps/users/admin.py:7:class UserAdmin(admin.ModelAdmin):
apps/users/admin.py:8:    list_display = ['user_id', 'name', 'role', 'class_id', 'active']
apps/users/admin.py:9:    list_filter = ['role', 'active', 'is_graduating']
apps/users/tests/test_import_csv.py:14:        User.objects.create_user(user_id='T001', name='李老师', role=UserRole.COUNSELOR, password='T001')
apps/users/tests/test_import_csv.py:15:        User.objects.create_user(user_id='T002', name='王老师', role=UserRole.COUNSELOR, password='T002')
apps/users/tests/test_import_csv.py:26:        csv_content = "employee_id,name,department\nT003,张老师,计算机学院\nT004,赵老师,软件学院"
apps/users/tests/test_import_csv.py:33:            self.assertEqual(User.objects.filter(role=UserRole.COUNSELOR).count(), 4)
apps/users/tests/test_import_csv.py:97:    def test_import_students_success(self):
apps/users/tests/test_import_csv.py:109:            self.assertEqual(User.objects.filter(role=UserRole.STUDENT).count(), 1)
apps/users/tests/test_import_csv.py:117:    def test_import_students_class_mapping_missing(self):
apps/users/tests/test_import_csv.py:129:            self.assertEqual(User.objects.filter(role=UserRole.STUDENT).count(), 0)
apps/users/tests/test_import_csv.py:155:            initial_count = User.objects.filter(role=UserRole.COUNSELOR).count()
apps/users/tests/test_import_csv.py:161:            final_count = User.objects.filter(role=UserRole.COUNSELOR).count()
apps/applications/tests/test_serializer_validation.py:5:from apps.applications.serializers import ApplicationCreateSerializer
apps/applications/tests/test_serializer_validation.py:8:class ApplicationCreateSerializerTest(TestCase):
apps/applications/tests/test_serializer_validation.py:15:        serializer = ApplicationCreateSerializer(data=data)
apps/applications/tests/test_serializer_validation.py:25:        serializer = ApplicationCreateSerializer(data=data)
apps/applications/tests/test_serializer_validation.py:35:        serializer = ApplicationCreateSerializer(data=data)
apps/applications/tests/test_serializer_validation.py:45:        serializer = ApplicationCreateSerializer(data=data)
apps/applications/tests/test_serializer_validation.py:54:        serializer = ApplicationCreateSerializer(data=data)
apps/applications/tests/test_serializer_validation.py:72:        serializer = ApplicationCreateSerializer(data=data)
apps/applications/tests/test_serializer_validation.py:89:        serializer = ApplicationCreateSerializer(data=data)
apps/users/management/commands/import_csv.py:30:            self.import_students(options['students'], dry_run, summary['students'])
apps/users/management/commands/import_csv.py:49:    def import_students(self, filepath, dry_run, summary):
apps/users/management/commands/import_csv.py:97:                                'role': UserRole.STUDENT,
apps/users/management/commands/import_csv.py:159:                                'role': UserRole.COUNSELOR,
apps/users/management/commands/import_csv.py:211:                            counselor = User.objects.get(user_id=counselor_id, role=UserRole.COUNSELOR)
apps/users/management/commands/seed_data.py:13:            help='Clear applications and approvals before loading seed data',
apps/users/management/commands/seed_data.py:18:            self.stdout.write('Resetting applications and approvals...')
apps/users/management/commands/seed_data.py:19:            from apps.applications.models import Application
apps/users/management/commands/seed_data.py:20:            from apps.approvals.models import Approval
apps/users/management/commands/seed_data.py:22:            Application.objects.all().delete()
apps/users/management/commands/seed_data.py:46:                    'role': UserRole.STUDENT,
apps/users/management/commands/seed_data.py:69:                    'role': UserRole.COUNSELOR,
apps/users/management/commands/seed_data.py:89:                    'role': UserRole.DORM_MANAGER,
apps/users/management/commands/seed_data.py:103:                'role': UserRole.DEAN,
apps/applications/tests/test_list_permissions.py:5:from apps.applications.models import Application, ApplicationStatus
apps/applications/tests/test_list_permissions.py:6:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
apps/applications/tests/test_list_permissions.py:9:class ApplicationListPermissionTest(TestCase):
apps/applications/tests/test_list_permissions.py:14:        self.student1 = User.objects.create(user_id='S001', name='学生1', role=UserRole.STUDENT, class_id='CS2020-01')
apps/applications/tests/test_list_permissions.py:18:        self.student2 = User.objects.create(user_id='S002', name='学生2', role=UserRole.STUDENT, class_id='CS2020-02')
apps/applications/tests/test_list_permissions.py:22:        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
apps/applications/tests/test_list_permissions.py:26:        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
apps/applications/tests/test_list_permissions.py:30:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
apps/applications/tests/test_list_permissions.py:34:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
apps/applications/tests/test_list_permissions.py:38:        self.dean = User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
apps/applications/tests/test_list_permissions.py:47:        self.app1 = Application.objects.create(
apps/applications/tests/test_list_permissions.py:54:            status=ApplicationStatus.PENDING_COUNSELOR
apps/applications/tests/test_list_permissions.py:57:        self.app2 = Application.objects.create(
apps/applications/tests/test_list_permissions.py:64:            status=ApplicationStatus.APPROVED
apps/applications/tests/test_list_permissions.py:67:        # Create approvals
apps/applications/tests/test_list_permissions.py:69:            approval_id='apv_001',
apps/applications/tests/test_list_permissions.py:71:            step=ApprovalStep.COUNSELOR,
apps/applications/tests/test_list_permissions.py:90:    def test_counselor_sees_only_pending_counselor_approvals(self):
apps/applications/tests/test_list_permissions.py:109:    def test_response_format_no_nested_approvals(self):
apps/applications/tests/test_list_permissions.py:114:        self.assertNotIn('approvals', response.data['results'][0])
apps/users/management/commands/import_staff.py:4:Supports staff types: DORM_MANAGER, COUNSELOR, ADMIN.
apps/users/management/commands/import_staff.py:28:        stats = self._import_staff(file_path, dry_run)
apps/users/management/commands/import_staff.py:31:    def _import_staff(self, file_path, dry_run):
apps/users/management/commands/import_staff.py:38:            'by_role': {}
apps/users/management/commands/import_staff.py:64:        role_str = (row.get('角色') or row.get('role') or '').strip()
apps/users/management/commands/import_staff.py:66:        building = (row.get('楼栋') or row.get('building') or '').strip()
apps/users/management/commands/import_staff.py:68:        if not user_id or not name or not role_str:
apps/users/management/commands/import_staff.py:70:            stats['errors'].append(f'Missing required fields: user_id={user_id}, name={name}, role={role_str}')
apps/users/management/commands/import_staff.py:73:        # Map role string to UserRole
apps/users/management/commands/import_staff.py:74:        role_map = {
apps/users/management/commands/import_staff.py:75:            '宿管员': UserRole.DORM_MANAGER,
apps/users/management/commands/import_staff.py:76:            'DORM_MANAGER': UserRole.DORM_MANAGER,
apps/users/management/commands/import_staff.py:77:            '辅导员': UserRole.COUNSELOR,
apps/users/management/commands/import_staff.py:78:            'COUNSELOR': UserRole.COUNSELOR,
apps/users/management/commands/import_staff.py:83:        role = role_map.get(role_str)
apps/users/management/commands/import_staff.py:84:        if not role:
apps/users/management/commands/import_staff.py:86:            stats['errors'].append(f'{user_id}: Unknown role "{role_str}"')
apps/users/management/commands/import_staff.py:89:        # Validate building requirement
apps/users/management/commands/import_staff.py:90:        if role == UserRole.DORM_MANAGER and not building:
apps/users/management/commands/import_staff.py:91:            # Allow empty building for fallback dorm manager
apps/users/management/commands/import_staff.py:93:            fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')
apps/users/management/commands/import_staff.py:97:                        f'{user_id} ({name}): DORM_MANAGER without building (not fallback manager)'
apps/users/management/commands/import_staff.py:107:            stats['by_role'][role] = stats['by_role'].get(role, 0) + 1
apps/users/management/commands/import_staff.py:113:                    'role': role,
apps/users/management/commands/import_staff.py:115:                    'building': building if building else None,
apps/users/management/commands/import_staff.py:125:            stats['by_role'][role] = stats['by_role'].get(role, 0) + 1
apps/users/management/commands/import_staff.py:135:        if stats['by_role']:
apps/users/management/commands/import_staff.py:136:            self.stdout.write('\nBy role:')
apps/users/management/commands/import_staff.py:137:            for role, count in stats['by_role'].items():
apps/users/management/commands/import_staff.py:138:                self.stdout.write(f'  {role}: {count}')
apps/notifications/models.py:16:    APPROVAL_APPROVED = 'approval_approved', '审批通过'
apps/notifications/models.py:17:    APPROVAL_REJECTED = 'approval_rejected', '审批驳回'
apps/notifications/models.py:18:    APPROVAL_TIMEOUT_WARNING = 'approval_timeout_warning', '审批超时提醒'
apps/notifications/models.py:23:    APPROVAL = 'approval', '审批记录'
apps/users/migrations/0006_add_admin_role.py:1:# Generated migration to add ADMIN role to User.role choices
apps/users/migrations/0006_add_admin_role.py:9:        ('users', '0005_user_building'),
apps/users/migrations/0006_add_admin_role.py:15:            name='role',
apps/users/migrations/0002_user_department_user_email_user_phone.py:15:            name='department',
apps/users/migrations/0005_user_building.py:13:            name='building',
apps/users/services/xg_user_sync.py:62:            if local_user.role != 'student':
apps/users/services/xg_user_sync.py:65:                    'reason': 'role_mismatch',
apps/users/services/xg_user_sync.py:66:                    'local_role': local_user.role,
apps/users/services/xg_user_sync.py:67:                    'api_role': mapped['role']
apps/users/services/xg_user_sync.py:83:            "until User model adds phone/email/department or name overwrite policy is approved"
apps/users/services/xg_user_sync.py:138:            if local_user.role != 'student':
apps/users/services/xg_user_sync.py:141:                    'reason': 'role_mismatch',
apps/users/services/xg_user_sync.py:142:                    'local_role': local_user.role,
apps/users/services/xg_user_sync.py:143:                    'api_role': mapped['role']
apps/users/services/xg_user_sync.py:150:                local_user.department = mapped.get('department', '')
apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:11:        ('users', '0002_user_department_user_email_user_phone'),
apps/users/migrations/0003_classmapping_dorm_manager_and_more.py:27:            name='role',
apps/notifications/tests/test_models.py:12:            role='student',
apps/notifications/tests/test_models.py:18:            role='counselor'
apps/notifications/tests/test_models.py:83:            role='student',
apps/users/apps.py:4:class UsersConfig(AppConfig):
apps/notifications/tests/test_api.py:14:            role='student',
apps/notifications/tests/test_api.py:20:            role='student',
apps/notifications/tests/test_api.py:26:            role='counselor'
apps/applications/tests/test_application_flow.py:8:from apps.applications.models import Application, ApplicationStatus
apps/applications/tests/test_application_flow.py:9:from apps.approvals.models import ApprovalDecision, ApprovalStep
apps/applications/tests/test_application_flow.py:12:class ApplicationFlowTestCase(TestCase):
apps/applications/tests/test_application_flow.py:21:            role=UserRole.STUDENT,
apps/applications/tests/test_application_flow.py:31:            role=UserRole.COUNSELOR
apps/applications/tests/test_application_flow.py:38:            role=UserRole.DORM_MANAGER
apps/applications/tests/test_application_flow.py:45:            role=UserRole.DEAN
apps/applications/tests/test_application_flow.py:76:        self.assertEqual(response.data['status'], ApplicationStatus.PENDING_DORM_MANAGER)
apps/applications/tests/test_application_flow.py:87:        application = Application.objects.get(application_id=application_id)
apps/applications/tests/test_application_flow.py:88:        dorm_manager_approval = application.approvals.get(step=ApprovalStep.DORM_MANAGER)
apps/applications/tests/test_application_flow.py:91:        response = self.client.post(f'/api/approvals/{dorm_manager_approval.approval_id}/approve/', {
apps/applications/tests/test_application_flow.py:98:        self.assertEqual(application.status, ApplicationStatus.PENDING_COUNSELOR)
apps/applications/tests/test_application_flow.py:108:        counselor_approval = application.approvals.get(step=ApprovalStep.COUNSELOR)
apps/applications/tests/test_application_flow.py:111:        response = self.client.post(f'/api/approvals/{counselor_approval.approval_id}/approve/', {
apps/applications/tests/test_application_flow.py:119:        self.assertEqual(application.status, ApplicationStatus.APPROVED)
apps/applications/tests/test_application_flow.py:125:        self.assertEqual(response.data['status'], ApplicationStatus.APPROVED)
apps/applications/tests/test_application_flow.py:126:        self.assertEqual(len(response.data['approvals']), 2)  # 2-level approval
apps/notifications/tests/test_auto_notifications_api.py:11:from apps.applications.models import Application, ApplicationStatus
apps/notifications/tests/test_auto_notifications_api.py:12:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
apps/notifications/tests/test_auto_notifications_api.py:29:            role='student',
apps/notifications/tests/test_auto_notifications_api.py:35:            role='counselor'
apps/notifications/tests/test_auto_notifications_api.py:40:            role='dorm_manager'
apps/notifications/tests/test_auto_notifications_api.py:45:            role='dean'
apps/notifications/tests/test_auto_notifications_api.py:75:        self.assertEqual(notifications[0]['entity_type'], 'approval')
apps/notifications/tests/test_auto_notifications_api.py:78:    def test_approval_approved_notification_visible_via_api(self):
apps/notifications/tests/test_auto_notifications_api.py:80:        # Create application and approval
apps/notifications/tests/test_auto_notifications_api.py:81:        application = Application.objects.create(
apps/notifications/tests/test_auto_notifications_api.py:88:            status=ApplicationStatus.PENDING_COUNSELOR
apps/notifications/tests/test_auto_notifications_api.py:91:        approval = Approval.objects.create(
apps/notifications/tests/test_auto_notifications_api.py:92:            approval_id='apv_test001',
apps/notifications/tests/test_auto_notifications_api.py:94:            step=ApprovalStep.COUNSELOR,
apps/notifications/tests/test_auto_notifications_api.py:102:        response = self.client.post(f'/api/approvals/{approval.approval_id}/approve/', {
apps/notifications/tests/test_auto_notifications_api.py:115:        # Find the approval notification
apps/notifications/tests/test_auto_notifications_api.py:116:        approval_notif = [n for n in notifications if n['type'] == 'approval_approved'][0]
apps/notifications/tests/test_auto_notifications_api.py:117:        self.assertEqual(approval_notif['entity_type'], 'approval')
apps/notifications/tests/test_auto_notifications_api.py:118:        self.assertIn('辅导员', approval_notif['message'])
apps/notifications/tests/test_auto_notifications_api.py:120:    def test_approval_rejected_notification_includes_reason(self):
apps/notifications/tests/test_auto_notifications_api.py:122:        # Create application and approval
apps/notifications/tests/test_auto_notifications_api.py:123:        application = Application.objects.create(
apps/notifications/tests/test_auto_notifications_api.py:130:            status=ApplicationStatus.PENDING_COUNSELOR
apps/notifications/tests/test_auto_notifications_api.py:133:        approval = Approval.objects.create(
apps/notifications/tests/test_auto_notifications_api.py:134:            approval_id='apv_test002',
apps/notifications/tests/test_auto_notifications_api.py:136:            step=ApprovalStep.COUNSELOR,
apps/notifications/tests/test_auto_notifications_api.py:144:        response = self.client.post(f'/api/approvals/{approval.approval_id}/reject/', {
apps/notifications/tests/test_auto_notifications_api.py:155:        reject_notif = [n for n in notifications if n['type'] == 'approval_rejected'][0]
apps/notifications/tests/test_auto_notifications_api.py:164:            role='student',
apps/notifications/tests/test_auto_notifications_api.py:168:        application = Application.objects.create(
apps/notifications/tests/test_auto_notifications_api.py:175:            status=ApplicationStatus.PENDING_COUNSELOR
apps/notifications/tests/test_auto_notifications_api.py:178:        approval = Approval.objects.create(
apps/notifications/tests/test_auto_notifications_api.py:179:            approval_id='apv_test003',
apps/notifications/tests/test_auto_notifications_api.py:181:            step=ApprovalStep.COUNSELOR,
apps/notifications/tests/test_auto_notifications_api.py:189:        response = self.client.post(f'/api/approvals/{approval.approval_id}/approve/', {
apps/notifications/tests/test_auto_notifications_api.py:196:            entity_type='approval',
apps/notifications/tests/test_auto_notifications_api.py:197:            entity_id=approval.pk
apps/notifications/tests/test_auto_notifications_api.py:202:        # Create application and approval
apps/notifications/tests/test_auto_notifications_api.py:203:        application = Application.objects.create(
apps/notifications/tests/test_auto_notifications_api.py:210:            status=ApplicationStatus.APPROVED
apps/notifications/tests/test_auto_notifications_api.py:213:        approval = Approval.objects.create(
apps/notifications/tests/test_auto_notifications_api.py:214:            approval_id='apv_test004',
apps/notifications/tests/test_auto_notifications_api.py:216:            step=ApprovalStep.COUNSELOR,
apps/notifications/tests/test_auto_notifications_api.py:224:        response = self.client.post(f'/api/approvals/{approval.approval_id}/approve/', {
apps/notifications/tests/test_auto_notifications_api.py:229:        # Verify only one notification exists (from initial approval, not from failed re-approval)
apps/notifications/tests/test_auto_notifications_api.py:232:            entity_type='approval',
apps/notifications/tests/test_auto_notifications_api.py:233:            entity_id=approval.pk
apps/notifications/tests/test_auto_notifications_api.py:234:        ).count(), 0)  # No notification because we created approval directly, not through API
apps/notifications/tests/test_auto_notifications_api.py:242:            role='student',
apps/notifications/tests/test_auto_notifications_api.py:254:        # Verify no Application was created (422 is synchronous validation failure)
apps/notifications/tests/test_auto_notifications_api.py:255:        self.assertEqual(Application.objects.filter(student=blocked_student).count(), 0)
apps/notifications/management/commands/seed_notifications.py:11:        students = User.objects.filter(role='student')[:3]
apps/notifications/tests/test_timeout_warnings.py:5:from apps.notifications.services import create_approval_timeout_warnings
apps/notifications/tests/test_timeout_warnings.py:7:from apps.applications.models import Application
apps/notifications/tests/test_timeout_warnings.py:8:from apps.approvals.models import Approval, ApprovalDecision
apps/notifications/tests/test_timeout_warnings.py:18:            role='student',
apps/notifications/tests/test_timeout_warnings.py:24:            role='counselor',
apps/notifications/tests/test_timeout_warnings.py:30:            role='dorm_manager'
apps/notifications/tests/test_timeout_warnings.py:34:        """Test counselor approval timeout after 3 days"""
apps/notifications/tests/test_timeout_warnings.py:35:        app = Application.objects.create(
apps/notifications/tests/test_timeout_warnings.py:40:        approval = Approval.objects.create(
apps/notifications/tests/test_timeout_warnings.py:45:        approval.created_at = timezone.now() - timedelta(days=4)
apps/notifications/tests/test_timeout_warnings.py:46:        approval.save()
apps/notifications/tests/test_timeout_warnings.py:48:        result = create_approval_timeout_warnings()
apps/notifications/tests/test_timeout_warnings.py:57:        """Test dorm manager approval timeout after 2 days"""
apps/notifications/tests/test_timeout_warnings.py:58:        app = Application.objects.create(
apps/notifications/tests/test_timeout_warnings.py:63:        approval = Approval.objects.create(
apps/notifications/tests/test_timeout_warnings.py:68:        approval.created_at = timezone.now() - timedelta(days=3)
apps/notifications/tests/test_timeout_warnings.py:69:        approval.save()
apps/notifications/tests/test_timeout_warnings.py:71:        result = create_approval_timeout_warnings()
apps/notifications/tests/test_timeout_warnings.py:80:        """Test that approvals within threshold are not notified"""
apps/notifications/tests/test_timeout_warnings.py:81:        app = Application.objects.create(
apps/notifications/tests/test_timeout_warnings.py:92:        result = create_approval_timeout_warnings()
apps/notifications/tests/test_timeout_warnings.py:98:        """Test that approved/rejected approvals are not notified"""
apps/notifications/tests/test_timeout_warnings.py:99:        app = Application.objects.create(
apps/notifications/tests/test_timeout_warnings.py:104:        approval = Approval.objects.create(
apps/notifications/tests/test_timeout_warnings.py:110:        approval.created_at = timezone.now() - timedelta(days=4)
apps/notifications/tests/test_timeout_warnings.py:111:        approval.save()
apps/notifications/tests/test_timeout_warnings.py:113:        result = create_approval_timeout_warnings()
apps/notifications/tests/test_timeout_warnings.py:120:        app = Application.objects.create(
apps/notifications/tests/test_timeout_warnings.py:125:        approval = Approval.objects.create(
apps/notifications/tests/test_timeout_warnings.py:130:        approval.created_at = timezone.now() - timedelta(days=4)
apps/notifications/tests/test_timeout_warnings.py:131:        approval.save()
apps/notifications/tests/test_timeout_warnings.py:133:        result1 = create_approval_timeout_warnings()
apps/notifications/tests/test_timeout_warnings.py:136:        result2 = create_approval_timeout_warnings()
apps/notifications/tests/test_timeout_warnings.py:143:        app = Application.objects.create(
apps/notifications/tests/test_timeout_warnings.py:148:        approval = Approval.objects.create(
apps/notifications/tests/test_timeout_warnings.py:153:        approval.created_at = timezone.now() - timedelta(days=4)
apps/notifications/tests/test_timeout_warnings.py:154:        approval.save()
apps/notifications/tests/test_timeout_warnings.py:156:        result = create_approval_timeout_warnings(dry_run=True)
apps/notifications/tests/test_timeout_warnings.py:160:        self.assertIn('approval_id', result['warnings'][0])
apps/notifications/management/commands/send_approval_timeout_warnings.py:2:from apps.notifications.services import create_approval_timeout_warnings
apps/notifications/management/commands/send_approval_timeout_warnings.py:6:    help = 'Send approval timeout warning notifications'
apps/notifications/management/commands/send_approval_timeout_warnings.py:21:        result = create_approval_timeout_warnings(dry_run=dry_run)
apps/notifications/management/commands/send_approval_timeout_warnings.py:31:                    f"  - Approval {warning['approval_id']}: "
apps/attachments/views.py:11:from apps.applications.models import Application
apps/attachments/views.py:13:from apps.approvals.models import Approval, ApprovalStep
apps/attachments/views.py:62:        application = Application.objects.get(application_id=application_id)
apps/attachments/views.py:63:    except Application.DoesNotExist:
apps/attachments/views.py:68:    if user.role != UserRole.STUDENT or application.student_id != user.user_id:
apps/attachments/views.py:100:        application = Application.objects.get(application_id=application_id)
apps/attachments/views.py:101:    except Application.DoesNotExist:
apps/attachments/views.py:188:    if user.role != UserRole.STUDENT or attachment.application.student_id != user.user_id:
apps/notifications/migrations/0002_alter_notification_type.py:16:            field=models.CharField(choices=[('application_submitted', '申请已提交'), ('approval_approved', '审批通过'), ('approval_rejected', '审批驳回'), ('approval_timeout_warning', '审批超时提醒')], max_length=50, verbose_name='通知类型'),
apps/attachments/models.py:2:from apps.applications.models import Application
apps/attachments/models.py:7:    DORM_CHECKOUT = 'dorm_checkout', '宿舍清退证明'
apps/attachments/models.py:15:    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='attachments')
apps/notifications/tests/test_auto_notifications.py:14:from apps.applications.models import Application, ApplicationStatus
apps/notifications/tests/test_auto_notifications.py:15:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
apps/notifications/tests/test_auto_notifications.py:17:from apps.notifications.services import notify_application_submitted, notify_approval_decided
apps/notifications/tests/test_auto_notifications.py:30:            role='student',
apps/notifications/tests/test_auto_notifications.py:36:            role='counselor'
apps/notifications/tests/test_auto_notifications.py:41:            role='dorm_manager'
apps/notifications/tests/test_auto_notifications.py:46:        application = Application.objects.create(
apps/notifications/tests/test_auto_notifications.py:53:            status=ApplicationStatus.PENDING_COUNSELOR
apps/notifications/tests/test_auto_notifications.py:56:        approval = Approval.objects.create(
apps/notifications/tests/test_auto_notifications.py:57:            approval_id='apv_test001',
apps/notifications/tests/test_auto_notifications.py:59:            step=ApprovalStep.COUNSELOR,
apps/notifications/tests/test_auto_notifications.py:65:        notification, created = notify_application_submitted(application, approval)
apps/notifications/tests/test_auto_notifications.py:71:        self.assertEqual(notification.entity_type, 'approval')
apps/notifications/tests/test_auto_notifications.py:72:        self.assertEqual(notification.entity_id, approval.pk)
apps/notifications/tests/test_auto_notifications.py:76:    def test_approval_approved_notification_counselor(self):
apps/notifications/tests/test_auto_notifications.py:77:        """Test APPROVAL_APPROVED notification for counselor approval."""
apps/notifications/tests/test_auto_notifications.py:78:        application = Application.objects.create(
apps/notifications/tests/test_auto_notifications.py:85:            status=ApplicationStatus.PENDING_COUNSELOR
apps/notifications/tests/test_auto_notifications.py:88:        approval = Approval.objects.create(
apps/notifications/tests/test_auto_notifications.py:89:            approval_id='apv_test002',
apps/notifications/tests/test_auto_notifications.py:91:            step=ApprovalStep.COUNSELOR,
apps/notifications/tests/test_auto_notifications.py:97:        notification, created = notify_approval_decided(approval)
apps/notifications/tests/test_auto_notifications.py:102:        self.assertEqual(notification.type, 'approval_approved')
apps/notifications/tests/test_auto_notifications.py:103:        self.assertEqual(notification.entity_type, 'approval')
apps/notifications/tests/test_auto_notifications.py:104:        self.assertEqual(notification.entity_id, approval.pk)
apps/notifications/tests/test_auto_notifications.py:107:    def test_approval_approved_notification_dorm_manager(self):
apps/notifications/tests/test_auto_notifications.py:108:        """Test APPROVAL_APPROVED notification for dorm manager approval."""
apps/notifications/tests/test_auto_notifications.py:109:        application = Application.objects.create(
apps/notifications/tests/test_auto_notifications.py:116:            status=ApplicationStatus.PENDING_DORM_MANAGER
apps/notifications/tests/test_auto_notifications.py:119:        approval = Approval.objects.create(
apps/notifications/tests/test_auto_notifications.py:120:            approval_id='apv_test003',
apps/notifications/tests/test_auto_notifications.py:122:            step=ApprovalStep.DORM_MANAGER,
apps/notifications/tests/test_auto_notifications.py:128:        notification, created = notify_approval_decided(approval)
apps/notifications/tests/test_auto_notifications.py:133:        self.assertEqual(notification.type, 'approval_approved')
apps/notifications/tests/test_auto_notifications.py:136:    def test_approval_rejected_notification(self):
apps/notifications/tests/test_auto_notifications.py:138:        application = Application.objects.create(
apps/notifications/tests/test_auto_notifications.py:145:            status=ApplicationStatus.PENDING_COUNSELOR
apps/notifications/tests/test_auto_notifications.py:148:        approval = Approval.objects.create(
apps/notifications/tests/test_auto_notifications.py:149:            approval_id='apv_test004',
apps/notifications/tests/test_auto_notifications.py:151:            step=ApprovalStep.COUNSELOR,
apps/notifications/tests/test_auto_notifications.py:158:        notification, created = notify_approval_decided(approval)
apps/notifications/tests/test_auto_notifications.py:163:        self.assertEqual(notification.type, 'approval_rejected')
apps/notifications/tests/test_auto_notifications.py:169:        application = Application.objects.create(
apps/notifications/tests/test_auto_notifications.py:176:            status=ApplicationStatus.PENDING_COUNSELOR
apps/notifications/tests/test_auto_notifications.py:179:        approval = Approval.objects.create(
apps/notifications/tests/test_auto_notifications.py:180:            approval_id='apv_test005',
apps/notifications/tests/test_auto_notifications.py:182:            step=ApprovalStep.COUNSELOR,
apps/notifications/tests/test_auto_notifications.py:188:        notification1, created1 = notify_application_submitted(application, approval)
apps/notifications/tests/test_auto_notifications.py:191:        notification2, created2 = notify_application_submitted(application, approval)
apps/notifications/tests/test_auto_notifications.py:197:            entity_type='approval',
apps/notifications/tests/test_auto_notifications.py:198:            entity_id=approval.pk,
apps/notifications/tests/test_auto_notifications.py:202:    def test_idempotency_approval_decided(self):
apps/notifications/tests/test_auto_notifications.py:203:        """Test that repeated approval decisions don't create duplicate notifications."""
apps/notifications/tests/test_auto_notifications.py:204:        application = Application.objects.create(
apps/notifications/tests/test_auto_notifications.py:211:            status=ApplicationStatus.PENDING_COUNSELOR
apps/notifications/tests/test_auto_notifications.py:214:        approval = Approval.objects.create(
apps/notifications/tests/test_auto_notifications.py:215:            approval_id='apv_test006',
apps/notifications/tests/test_auto_notifications.py:217:            step=ApprovalStep.COUNSELOR,
apps/notifications/tests/test_auto_notifications.py:223:        notification1, created1 = notify_approval_decided(approval)
apps/notifications/tests/test_auto_notifications.py:226:        notification2, created2 = notify_approval_decided(approval)
apps/notifications/tests/test_auto_notifications.py:232:            entity_type='approval',
apps/notifications/tests/test_auto_notifications.py:233:            entity_id=approval.pk,
apps/notifications/tests/test_auto_notifications.py:234:            type='approval_approved'
apps/notifications/migrations/0001_initial.py:22:                ('type', models.CharField(choices=[('application_submitted', '申请已提交'), ('approval_approved', '审批通过'), ('approval_rejected', '审批驳回'), ('dorm_clearance_blocked', '宿舍清退阻断'), ('approval_timeout_warning', '审批超时提醒')], max_length=50, verbose_name='通知类型')),
apps/notifications/migrations/0001_initial.py:23:                ('entity_type', models.CharField(choices=[('application', '离校申请'), ('approval', '审批记录')], max_length=50, verbose_name='实体类型')),
apps/applications/tests/test_constraints.py:7:from apps.applications.models import Application, ApplicationStatus
apps/applications/tests/test_constraints.py:11:class ApplicationConstraintsTestCase(TestCase):
apps/applications/tests/test_constraints.py:17:            role=UserRole.STUDENT,
apps/applications/tests/test_constraints.py:28:            role=UserRole.COUNSELOR,
apps/applications/tests/test_constraints.py:34:            role=UserRole.DORM_MANAGER,
apps/attachments/tests/test_download.py:7:from apps.applications.models import Application, ApplicationStatus
apps/attachments/tests/test_download.py:8:from apps.approvals.models import Approval, ApprovalStep, ApprovalDecision
apps/attachments/tests/test_download.py:21:            role=UserRole.STUDENT,
apps/attachments/tests/test_download.py:31:            role=UserRole.STUDENT,
apps/attachments/tests/test_download.py:42:            role=UserRole.COUNSELOR
apps/attachments/tests/test_download.py:54:        self.application = Application.objects.create(
apps/attachments/tests/test_download.py:61:            status=ApplicationStatus.PENDING_COUNSELOR
apps/attachments/tests/test_download.py:71:            attachment_type=AttachmentType.DORM_CHECKOUT,
apps/users/management/commands/import_students.py:4:Supports File5 format with building_name field.
apps/users/management/commands/import_students.py:33:            from apps.applications.models import Application
apps/users/management/commands/import_students.py:34:            active_apps = Application.objects.exclude(status='rejected').count()
apps/users/management/commands/import_students.py:41:        stats = self._import_students(file_path, dry_run, mode)
apps/users/management/commands/import_students.py:44:    def _import_students(self, file_path, dry_run, mode):
apps/users/management/commands/import_students.py:63:                deleted = User.objects.filter(role=UserRole.STUDENT).delete()
apps/users/management/commands/import_students.py:84:        department = row.get('department', '').strip()
apps/users/management/commands/import_students.py:86:        building = row.get('building_name', '').strip()
apps/users/management/commands/import_students.py:110:                    'department': department,
apps/users/management/commands/import_students.py:112:                    'building': building if building else None,
apps/users/management/commands/import_students.py:115:                    'role': UserRole.STUDENT,
apps/attachments/tests/test_delete.py:7:from apps.applications.models import Application, ApplicationStatus
apps/attachments/tests/test_delete.py:20:            role=UserRole.STUDENT,
apps/attachments/tests/test_delete.py:30:            role=UserRole.STUDENT,
apps/attachments/tests/test_delete.py:41:            role=UserRole.COUNSELOR
apps/attachments/tests/test_delete.py:53:        self.application = Application.objects.create(
apps/attachments/tests/test_delete.py:60:            status=ApplicationStatus.PENDING_COUNSELOR
apps/attachments/tests/test_delete.py:70:            attachment_type=AttachmentType.DORM_CHECKOUT,
apps/attachments/tests/test_list.py:7:from apps.applications.models import Application, ApplicationStatus
apps/attachments/tests/test_list.py:20:            role=UserRole.STUDENT,
apps/attachments/tests/test_list.py:30:            role=UserRole.STUDENT,
apps/attachments/tests/test_list.py:41:            role=UserRole.COUNSELOR
apps/attachments/tests/test_list.py:48:            role=UserRole.COUNSELOR
apps/attachments/tests/test_list.py:56:            role=UserRole.DEAN
apps/attachments/tests/test_list.py:75:        self.application = Application.objects.create(
apps/attachments/tests/test_list.py:82:            status=ApplicationStatus.APPROVED
apps/attachments/tests/test_list.py:91:            attachment_type=AttachmentType.DORM_CHECKOUT,
apps/attachments/tests/test_upload.py:7:from apps.applications.models import Application, ApplicationStatus
apps/attachments/tests/test_upload.py:20:            role=UserRole.STUDENT,
apps/attachments/tests/test_upload.py:31:            role=UserRole.STUDENT,
apps/attachments/tests/test_upload.py:42:            role=UserRole.COUNSELOR
apps/attachments/tests/test_upload.py:54:        self.application = Application.objects.create(
apps/attachments/tests/test_upload.py:61:            status=ApplicationStatus.PENDING_COUNSELOR
apps/attachments/tests/test_upload.py:65:        self.other_application = Application.objects.create(
apps/attachments/tests/test_upload.py:72:            status=ApplicationStatus.PENDING_COUNSELOR
apps/attachments/tests/test_upload.py:84:                'attachment_type': AttachmentType.DORM_CHECKOUT,
apps/attachments/tests/test_upload.py:94:        self.assertEqual(response.data['attachment_type'], AttachmentType.DORM_CHECKOUT)
apps/attachments/tests/test_upload.py:106:                'attachment_type': AttachmentType.DORM_CHECKOUT
apps/attachments/tests/test_upload.py:123:                'attachment_type': AttachmentType.DORM_CHECKOUT
apps/attachments/tests/test_upload.py:138:                'attachment_type': AttachmentType.DORM_CHECKOUT

codex
从任务文档看，19名额外研究生本身缺少路由字段且不在主批次，不能直接并入口径。下一步我会读取模型、导入脚本和申请创建逻辑，判断额外用户会不会真实触发流程问题。
exec
/bin/bash -lc "rtk sed -n '1,220p' apps/users/management/commands/import_students.py" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
"""
Django management command to import students from File5 CSV.

Supports File5 format with building_name field.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.users.models import User, UserRole
import csv
from pathlib import Path


class Command(BaseCommand):
    help = 'Import students from File5 CSV (v2 format with real student numbers)'

    def add_arguments(self, parser):
        parser.add_argument('--file', required=True, help='Input CSV file path')
        parser.add_argument('--dry-run', action='store_true', help='Dry run without writing to DB')
        parser.add_argument('--mode', choices=['append', 'clean'], default='append',
                            help='Import mode: append (default) or clean (delete all students first)')

    def handle(self, *args, **options):
        file_path = options['file']
        dry_run = options['dry_run']
        mode = options['mode']

        if not Path(file_path).exists():
            raise CommandError(f'File not found: {file_path}')

        # Safety check for clean mode
        if mode == 'clean' and not dry_run:
            from apps.applications.models import Application
            active_apps = Application.objects.exclude(status='rejected').count()
            if active_apps > 0:
                raise CommandError(
                    f'Cannot clean import: {active_apps} active applications exist. '
                    'Use append mode or manually clear applications first.'
                )

        stats = self._import_students(file_path, dry_run, mode)
        self._print_results(stats, dry_run)

    def _import_students(self, file_path, dry_run, mode):
        stats = {
            'total': 0,
            'created': 0,
            'updated': 0,
            'skipped': 0,
            'errors': []
        }

        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)

            # Validate required columns
            required = ['user_id', 'name', 'class_id']
            missing = [col for col in required if col not in reader.fieldnames]
            if missing:
                raise CommandError(f'Missing required columns: {", ".join(missing)}')

            if mode == 'clean' and not dry_run:
                deleted = User.objects.filter(role=UserRole.STUDENT).delete()
                self.stdout.write(f'Deleted {deleted[0]} existing students')

            rows = list(reader)
            stats['total'] = len(rows)

            with transaction.atomic():
                for row in rows:
                    try:
                        self._process_row(row, stats, dry_run)
                    except Exception as e:
                        stats['errors'].append(f"Row {stats['total']}: {str(e)}")

                if dry_run:
                    transaction.set_rollback(True)

        return stats

    def _process_row(self, row, stats, dry_run):
        user_id = row['user_id'].strip()
        name = row['name'].strip()
        department = row.get('department', '').strip()
        class_id = row.get('class_id', '').strip()
        building = row.get('building_name', '').strip()
        phone = row.get('phone', '').strip()
        email = row.get('email', '').strip()
        graduation_year = int(row.get('graduation_year', 2026))

        # Skip TMP IDs
        if user_id.startswith('TMP2026_'):
            stats['skipped'] += 1
            stats['errors'].append(f'{user_id}: TMP ID not allowed in import')
            return

        if dry_run:
            # Dry run: just count
            exists = User.objects.filter(user_id=user_id).exists()
            if exists:
                stats['updated'] += 1
            else:
                stats['created'] += 1
        else:
            # Real import
            user, created = User.objects.update_or_create(
                user_id=user_id,
                defaults={
                    'name': name,
                    'department': department,
                    'class_id': class_id,
                    'building': building if building else None,
                    'phone': phone if phone else None,
                    'email': email if email else None,
                    'role': UserRole.STUDENT,
                    'graduation_year': graduation_year,
                    'is_graduating': True,
                    'active': True,
                }
            )

            if created:
                stats['created'] += 1
            else:
                stats['updated'] += 1

    def _print_results(self, stats, dry_run):
        mode_label = 'DRY RUN' if dry_run else 'IMPORT'
        self.stdout.write(f'\n=== {mode_label} RESULTS ===')
        self.stdout.write(f'Total rows: {stats["total"]}')
        self.stdout.write(f'Created: {stats["created"]}')
        self.stdout.write(f'Updated: {stats["updated"]}')
        self.stdout.write(f'Skipped: {stats["skipped"]}')

        if stats['errors']:
            self.stdout.write(self.style.WARNING(f'\nErrors ({len(stats["errors"])}):'))
            for err in stats['errors'][:10]:
                self.stdout.write(f'  - {err}')
            if len(stats['errors']) > 10:
                self.stdout.write(f'  ... and {len(stats["errors"]) - 10} more')

        if not dry_run and len(stats['errors']) == 0:
            self.stdout.write(self.style.SUCCESS(f'\n✓ Import successful'))

exec
/bin/bash -lc "rtk sed -n '1,240p' apps/users/models.py" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserRole(models.TextChoices):
    STUDENT = 'student', '学生'
    DORM_MANAGER = 'dorm_manager', '宿管员'
    COUNSELOR = 'counselor', '辅导员'
    DEAN = 'dean', '学工部'
    ADMIN = 'admin', '学工管理员'


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
    building = models.CharField(max_length=100, null=True, blank=True)

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
/bin/bash -lc "rtk sed -n '1,240p' apps/users/management/commands/import_staff.py" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
"""
Django management command to import staff from CSV.

Supports staff types: DORM_MANAGER, COUNSELOR, ADMIN.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.users.models import User, UserRole
import csv
from pathlib import Path


class Command(BaseCommand):
    help = 'Import staff (dorm managers, counselors, admins) from CSV'

    def add_arguments(self, parser):
        parser.add_argument('--file', required=True, help='Input CSV file path')
        parser.add_argument('--dry-run', action='store_true', help='Dry run without writing to DB')

    def handle(self, *args, **options):
        file_path = options['file']
        dry_run = options['dry_run']

        if not Path(file_path).exists():
            raise CommandError(f'File not found: {file_path}')

        stats = self._import_staff(file_path, dry_run)
        self._print_results(stats, dry_run)

    def _import_staff(self, file_path, dry_run):
        stats = {
            'total': 0,
            'created': 0,
            'updated': 0,
            'skipped': 0,
            'errors': [],
            'by_role': {}
        }

        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)

            # Support both Chinese and English column names
            rows = list(reader)
            stats['total'] = len(rows)

            with transaction.atomic():
                for row in rows:
                    try:
                        self._process_row(row, stats, dry_run)
                    except Exception as e:
                        stats['errors'].append(f"Row {stats['total']}: {str(e)}")

                if dry_run:
                    transaction.set_rollback(True)

        return stats

    def _process_row(self, row, stats, dry_run):
        # Support both Chinese and English column names
        user_id = (row.get('职工号') or row.get('user_id') or '').strip()
        name = (row.get('姓名') or row.get('name') or '').strip()
        role_str = (row.get('角色') or row.get('role') or '').strip()
        phone = (row.get('手机') or row.get('phone') or '').strip()
        building = (row.get('楼栋') or row.get('building') or '').strip()

        if not user_id or not name or not role_str:
            stats['skipped'] += 1
            stats['errors'].append(f'Missing required fields: user_id={user_id}, name={name}, role={role_str}')
            return

        # Map role string to UserRole
        role_map = {
            '宿管员': UserRole.DORM_MANAGER,
            'DORM_MANAGER': UserRole.DORM_MANAGER,
            '辅导员': UserRole.COUNSELOR,
            'COUNSELOR': UserRole.COUNSELOR,
            '学工管理员': UserRole.ADMIN,
            'ADMIN': UserRole.ADMIN,
        }

        role = role_map.get(role_str)
        if not role:
            stats['skipped'] += 1
            stats['errors'].append(f'{user_id}: Unknown role "{role_str}"')
            return

        # Validate building requirement
        if role == UserRole.DORM_MANAGER and not building:
            # Allow empty building for fallback dorm manager
            from django.conf import settings
            fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')
            if user_id != fallback_id:
                self.stdout.write(
                    self.style.WARNING(
                        f'{user_id} ({name}): DORM_MANAGER without building (not fallback manager)'
                    )
                )

        if dry_run:
            exists = User.objects.filter(user_id=user_id).exists()
            if exists:
                stats['updated'] += 1
            else:
                stats['created'] += 1
            stats['by_role'][role] = stats['by_role'].get(role, 0) + 1
        else:
            user, created = User.objects.update_or_create(
                user_id=user_id,
                defaults={
                    'name': name,
                    'role': role,
                    'phone': phone if phone else None,
                    'building': building if building else None,
                    'active': True,
                }
            )

            if created:
                stats['created'] += 1
            else:
                stats['updated'] += 1

            stats['by_role'][role] = stats['by_role'].get(role, 0) + 1

    def _print_results(self, stats, dry_run):
        mode_label = 'DRY RUN' if dry_run else 'IMPORT'
        self.stdout.write(f'\n=== {mode_label} RESULTS ===')
        self.stdout.write(f'Total rows: {stats["total"]}')
        self.stdout.write(f'Created: {stats["created"]}')
        self.stdout.write(f'Updated: {stats["updated"]}')
        self.stdout.write(f'Skipped: {stats["skipped"]}')

        if stats['by_role']:
            self.stdout.write('\nBy role:')
            for role, count in stats['by_role'].items():
                self.stdout.write(f'  {role}: {count}')

        if stats['errors']:
            self.stdout.write(self.style.WARNING(f'\nErrors ({len(stats["errors"])}):'))
            for err in stats['errors'][:10]:
                self.stdout.write(f'  - {err}')
            if len(stats['errors']) > 10:
                self.stdout.write(f'  ... and {len(stats['errors']) - 10} more')

        if not dry_run and len(stats['errors']) == 0:
            self.stdout.write(self.style.SUCCESS(f'\n✓ Import successful'))

exec
/bin/bash -lc "rtk sed -n '1,260p' apps/applications/views.py" in /home/caohui/projects/graduation-leave-system/backend
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
from apps.users.models import UserRole, User
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

    # Find dorm manager with fallback mechanism
    dorm_manager = None
    building = user.building

    # Try to find dorm manager by building
    if building and building.strip():
        try:
            dorm_manager = User.objects.get(role=UserRole.DORM_MANAGER, building=building, active=True)
        except User.DoesNotExist:
            pass  # Will try fallback
        except User.MultipleObjectsReturned:
            dorm_manager = User.objects.filter(role=UserRole.DORM_MANAGER, building=building, active=True).first()

    # Fallback: use default dorm manager for students without building
    if not dorm_manager:
        from django.conf import settings
        fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')
        try:
            dorm_manager = User.objects.get(role=UserRole.DORM_MANAGER, user_id=fallback_id, active=True)
        except User.DoesNotExist:
            return Response({'error': {'code': 'NOT_FOUND', 'message': '无可用宿管员',
                                        'details': {'building': building or '未分配', 'fallback_id': fallback_id}}},
                            status=status.HTTP_404_NOT_FOUND)

    dorm_manager_name = dorm_manager.name

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
        approver=dorm_manager,
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

codex
申请提交逻辑确认了：宿管路由会按楼栋找人，找不到则走兜底；辅导员是在宿管通过时按学生学院查找，若同学院多名辅导员会产生风险。我会继续查当前数据是否存在“多名同楼栋/同学院”的额外记录风险。
exec
/bin/bash -lc "rtk sed -n '1,280p' apps/approvals/views.py" in /home/caohui/projects/graduation-leave-system/backend
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

        # Get counselor by department
        try:
            counselor = User.objects.get(role=UserRole.COUNSELOR, department=application.student.department, active=True)
        except User.DoesNotExist:
            return Response({'error': {'code': 'NOT_FOUND', 'message': '该学院辅导员不存在',
                                        'details': {'department': application.student.department}}},
                            status=status.HTTP_404_NOT_FOUND)

        Approval.objects.create(
            approval_id=f'apv_{uuid.uuid4().hex[:8]}',
            application=application,
            step=ApprovalStep.COUNSELOR,
            approver=counselor,
            approver_name=counselor.name,
            decision=ApprovalDecision.PENDING
        )
    elif approval.step == ApprovalStep.COUNSELOR:
        # Counselor approval completes the process (2-level approval)
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
/bin/bash -lc "rtk sed -n '1,220p' apps/users/views.py" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import LoginSerializer, LoginResponseSerializer


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

exec
/bin/bash -lc "rtk sed -n '1,220p' apps/applications/serializers.py" in /home/caohui/projects/graduation-leave-system/backend
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

exec
/bin/bash -lc "rtk sed -n '1,220p' apps/users/serializers.py" in /home/caohui/projects/graduation-leave-system/backend
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

codex
另一个独立风险出现了：`apps/approvals/views.py` 在宿管通过后使用 `User.objects`，但当前文件只导入了 `UserRole`，这会让辅导员审批创建路径直接报错。这个风险与14人差异无关，但可能会影响 Phase 4 联调。
exec
/bin/bash -lc "rtk python manage.py shell -c \"from apps.users.models import User,UserRole; from apps.applications.models import Application; from collections import Counter; print('users', User.objects.count()); print('by_role', dict(Counter(User.objects.values_list('role', flat=True)))); print('students', User.objects.filter(role=UserRole.STUDENT).count()); print('staff active by_role', dict(Counter(User.objects.exclude(role=UserRole.STUDENT).values_list('role', flat=True)))); print('applications', Application.objects.count()); print('active_apps', Application.objects.exclude(status='rejected').count()); print('tmp', User.objects.filter(user_id__startswith='TMP2026_').count()); print('student_no_building', User.objects.filter(role=UserRole.STUDENT, building__isnull=True).count()+User.objects.filter(role=UserRole.STUDENT, building='').count())\"" in /home/caohui/projects/graduation-leave-system/backend
 exited 127 in 0ms:
[rtk: No such file or directory (os error 2)]

codex
本地没有 `python` 命令别名，我会改用 `python3` 执行同样的 Django 查询。
exec
/bin/bash -lc "rtk python3 manage.py shell -c \"from apps.users.models import User,UserRole; from apps.applications.models import Application; from collections import Counter; print('users', User.objects.count()); print('by_role', dict(Counter(User.objects.values_list('role', flat=True)))); print('students', User.objects.filter(role=UserRole.STUDENT).count()); print('staff_by_role', dict(Counter(User.objects.exclude(role=UserRole.STUDENT).values_list('role', flat=True)))); print('applications', Application.objects.count()); print('active_apps', Application.objects.exclude(status='rejected').count()); print('tmp', User.objects.filter(user_id__startswith='TMP2026_').count()); print('student_no_building', User.objects.filter(role=UserRole.STUDENT, building__isnull=True).count()+User.objects.filter(role=UserRole.STUDENT, building='').count())\"" in /home/caohui/projects/graduation-leave-system/backend
 exited 1 in 0ms:
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
Django 依赖在当前 shell 环境未激活；项目有 `venv`，我会用虚拟环境里的 Python 查询数据库。
exec
/bin/bash -lc "rtk ./venv/bin/python manage.py shell -c \"from apps.users.models import User,UserRole; from apps.applications.models import Application; from collections import Counter; print('users', User.objects.count()); print('by_role', dict(Counter(User.objects.values_list('role', flat=True)))); print('students', User.objects.filter(role=UserRole.STUDENT).count()); print('staff_by_role', dict(Counter(User.objects.exclude(role=UserRole.STUDENT).values_list('role', flat=True)))); print('applications', Application.objects.count()); print('active_apps', Application.objects.exclude(status='rejected').count()); print('tmp', User.objects.filter(user_id__startswith='TMP2026_').count()); print('student_no_building', User.objects.filter(role=UserRole.STUDENT, building__isnull=True).count()+User.objects.filter(role=UserRole.STUDENT, building='').count())\"" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 408ms:
users 6056
by_role {'student': 5956, 'counselor': 22, 'dorm_manager': 75, 'dean': 1, 'admin': 2}
students 5956
staff_by_role {'counselor': 22, 'dorm_manager': 75, 'dean': 1, 'admin': 2}
applications 2
active_apps 1
tmp 0
student_no_building 126

codex
数据库现状比任务文档多一个 `dean` 角色用户：总用户 6056，若排除 `dean` 才是6055。还发现当前有1个非 rejected 申请，因此现在直接执行学生 `clean` 导入会被命令拦截。
exec
/bin/bash -lc "rtk ./venv/bin/python manage.py shell -c \"import csv; from collections import Counter,defaultdict; from pathlib import Path; from apps.users.models import User,UserRole; from apps.applications.models import Application; base=Path('data'); sources={}; sources['students']={r['user_id'].strip() for r in csv.DictReader(open(base/'file5_students_merged_v2.csv', encoding='utf-8-sig'))}; def staff_ids(path):\\n    ids=[]\\n    for r in csv.DictReader(open(base/path, encoding='utf-8-sig')):\\n        uid=(r.get('职工号') or r.get('user_id') or '').strip();\\n        if uid: ids.append(uid)\\n    return set(ids)\\nsources['dorm']=staff_ids('dorm_managers_processed.csv'); sources['counselor']=staff_ids('counselors_processed.csv'); sources['additional']=staff_ids('additional_staff.csv'); print('source_counts', {k:len(v) for k,v in sources.items()}); print('source_union', len(set().union(*sources.values()))); print('db_by_role', dict(Counter(User.objects.values_list('role', flat=True)))); role_sources={UserRole.STUDENT:sources['students'], UserRole.DORM_MANAGER:sources['dorm']|sources['additional'], UserRole.COUNSELOR:sources['counselor'], UserRole.ADMIN:sources['additional']};\\nfor role, ids in role_sources.items():\\n    db=set(User.objects.filter(role=role).values_list('user_id', flat=True));\\n    extra=sorted(db-ids); missing=sorted(ids-db);\\n    print('ROLE', role, 'db', len(db), 'src', len(ids), 'extra', len(extra), extra[:50], 'missing', len(missing), missing[:20]);\\nprint('apps_by_status', dict(Counter(Application.objects.values_list('status', flat=True)))); print('active_app_rows', list(Application.objects.exclude(status='rejected').values_list('application_id','student_id','status')[:10]))\"" in /home/caohui/projects/graduation-leave-system/backend
 exited 1 in 416ms:
Traceback (most recent call last):
  File "/home/caohui/projects/graduation-leave-system/backend/manage.py", line 22, in <module>
    main()
    ~~~~^^
  File "/home/caohui/projects/graduation-leave-system/backend/manage.py", line 18, in main
    execute_from_command_line(sys.argv)
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
    utility.execute()
    ~~~~~~~~~~~~~~~^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/core/management/__init__.py", line 436, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/core/management/base.py", line 412, in run_from_argv
    self.execute(*args, **cmd_options)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/core/management/base.py", line 458, in execute
    output = self.handle(*args, **options)
  File "/home/caohui/projects/graduation-leave-system/backend/venv/lib/python3.14/site-packages/django/core/management/commands/shell.py", line 117, in handle
    exec(options["command"], globals())
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<string>", line 1
    import csv; from collections import Counter,defaultdict; from pathlib import Path; from apps.users.models import User,UserRole; from apps.applications.models import Application; base=Path('data'); sources={}; sources['students']={r['user_id'].strip() for r in csv.DictReader(open(base/'file5_students_merged_v2.csv', encoding='utf-8-sig'))}; def staff_ids(path):\n    ids=[]\n    for r in csv.DictReader(open(base/path, encoding='utf-8-sig')):\n        uid=(r.get('职工号') or r.get('user_id') or '').strip();\n        if uid: ids.append(uid)\n    return set(ids)\nsources['dorm']=staff_ids('dorm_managers_processed.csv'); sources['counselor']=staff_ids('counselors_processed.csv'); sources['additional']=staff_ids('additional_staff.csv'); print('source_counts', {k:len(v) for k,v in sources.items()}); print('source_union', len(set().union(*sources.values()))); print('db_by_role', dict(Counter(User.objects.values_list('role', flat=True)))); role_sources={UserRole.STUDENT:sources['students'], UserRole.DORM_MANAGER:sources['dorm']|sources['additional'], UserRole.COUNSELOR:sources['counselor'], UserRole.ADMIN:sources['additional']};\nfor role, ids in role_sources.items():\n    db=set(User.objects.filter(role=role).values_list('user_id', flat=True));\n    extra=sorted(db-ids); missing=sorted(ids-db);\n    print('ROLE', role, 'db', len(db), 'src', len(ids), 'extra', len(extra), extra[:50], 'missing', len(missing), missing[:20]);\nprint('apps_by_status', dict(Counter(Application.objects.values_list('status', flat=True)))); print('active_app_rows', list(Application.objects.exclude(status='rejected').values_list('application_id','student_id','status')[:10]))
                                                                                                                                                                                                                                                                                                                                                          ^^^
SyntaxError: invalid syntax

codex
上一条内联脚本因为 shell `-c` 不适合定义多行函数失败了；我会用 stdin 方式运行同一段只读查询。
exec
/bin/bash -lc "rtk ./venv/bin/python manage.py shell <<'PY'
import csv
from collections import Counter
from pathlib import Path
from apps.users.models import User, UserRole
from apps.applications.models import Application

base = Path('data')

def read_ids(path, *cols):
    ids = []
    with open(base / path, encoding='utf-8-sig') as f:
        for row in csv.DictReader(f):
            uid = ''
            for col in cols:
                uid = (row.get(col) or '').strip()
                if uid:
                    break
            if uid:
                ids.append(uid)
    return set(ids)

sources = {
    'students': read_ids('file5_students_merged_v2.csv', 'user_id'),
    'dorm': read_ids('dorm_managers_processed.csv', '职工号', 'user_id'),
    'counselor': read_ids('counselors_processed.csv', '职工号', 'user_id'),
    'additional': read_ids('additional_staff.csv', '职工号', 'user_id'),
}
print('source_counts', {k: len(v) for k, v in sources.items()})
print('source_union', len(set().union(*sources.values())))
print('db_by_role', dict(Counter(User.objects.values_list('role', flat=True))))
role_sources = {
    UserRole.STUDENT: sources['students'],
    UserRole.DORM_MANAGER: sources['dorm'] | sources['additional'],
    UserRole.COUNSELOR: sources['counselor'],
    UserRole.ADMIN: sources['additional'],
}
for role, ids in role_sources.items():
    db = set(User.objects.filter(role=role).values_list('user_id', flat=True))
    extra = sorted(db - ids)
    missing = sorted(ids - db)
    print('ROLE', role, 'db', len(db), 'src', len(ids), 'extra', len(extra), extra[:80], 'missing', len(missing), missing[:20])
print('apps_by_status', dict(Counter(Application.objects.values_list('status', flat=True))))
print('active_app_rows', list(Application.objects.exclude(status='rejected').values_list('application_id','student_id','status')[:20]))
PY" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 326ms:
source_counts {'students': 5946, 'dorm': 72, 'counselor': 20, 'additional': 3}
source_union 6041
db_by_role {'student': 5956, 'counselor': 22, 'dorm_manager': 75, 'dean': 1, 'admin': 2}
ROLE student db 5956 src 5946 extra 10 ['2020001', '2020002', '2020003', '2020004', '2020005', '2020006', '2020007', '2020008', '2020009', '2020010'] missing 0 []
ROLE dorm_manager db 75 src 75 extra 2 ['M001', 'M002'] missing 2 ['19970545', '20144020']
ROLE counselor db 22 src 20 extra 2 ['T001', 'T002'] missing 0 []
ROLE admin db 2 src 3 extra 0 [] missing 1 ['92008149']
apps_by_status {'approved': 1, 'rejected': 1}
active_app_rows [('app_4ae6dd14', '2020001', 'approved')]

codex
只读比对已基本确认根因是残留测试数据：10个学生是 `2020001`-`2020010`，2个辅导员是 `T001/T002`。宿管差异里也有 `M001/M002` 测试账号；另有2个源宿管被后续管理员文件覆盖成 `admin`，需要单独说明。
exec
/bin/bash -lc 'rtk cat data/additional_staff.csv' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
职工号,姓名,角色,手机,楼栋,备注
20144020,肖延量,学工管理员,13636001781,,学生管理科科长
19970545,李桃花,学工管理员,15907258727,,学生事务管理科长
92008149,程婷,宿管员,13476778525,,"负责无楼栋学生审批（兜底宿管员）"

exec
/bin/bash -lc "rtk rg -n \"19970545|20144020|92008149|M001|M002|T001|T002\" data docs apps -g '*.csv' -g '*.md' -g '*.py'" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
apps/approvals/tests/test_rejection_flow.py:27:            user_id='T001',
apps/approvals/tests/test_rejection_flow.py:28:            password='T001',
apps/approvals/tests/test_rejection_flow.py:34:            user_id='M001',
apps/approvals/tests/test_rejection_flow.py:35:            password='M001',
apps/approvals/tests/test_rejection_flow.py:68:            'user_id': 'M001',
apps/approvals/tests/test_rejection_flow.py:69:            'password': 'M001'
apps/approvals/tests/test_rejection_flow.py:86:            'user_id': 'M001',
apps/approvals/tests/test_rejection_flow.py:87:            'password': 'M001'
apps/approvals/tests/test_rejection_flow.py:112:            'user_id': 'T001',
apps/approvals/tests/test_rejection_flow.py:113:            'password': 'T001'
apps/approvals/tests/test_list_permissions.py:17:        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
apps/approvals/tests/test_list_permissions.py:18:        self.counselor1.set_password('T001')
apps/approvals/tests/test_list_permissions.py:21:        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
apps/approvals/tests/test_list_permissions.py:22:        self.counselor2.set_password('T002')
apps/approvals/tests/test_list_permissions.py:25:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
apps/approvals/tests/test_list_permissions.py:26:        self.dorm_manager1.set_password('M001')
apps/approvals/tests/test_list_permissions.py:29:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
apps/approvals/tests/test_list_permissions.py:30:        self.dorm_manager2.set_password('M002')
apps/approvals/tests/test_permissions.py:30:            user_id='T001',
apps/approvals/tests/test_permissions.py:33:            password='T001'
apps/approvals/tests/test_permissions.py:36:            user_id='T002',
apps/approvals/tests/test_permissions.py:39:            password='T002'
apps/approvals/tests/test_permissions.py:42:            user_id='M001',
apps/approvals/tests/test_permissions.py:45:            password='M001'
apps/approvals/tests/test_permissions.py:48:            user_id='M002',
apps/approvals/tests/test_permissions.py:51:            password='M002'
apps/approvals/tests/test_permissions.py:177:        # T002 tries to approve T001's application
apps/approvals/tests/test_permissions.py:188:        # T002 tries to reject T001's application
apps/approvals/tests/test_state_machine.py:23:            user_id='T001',
apps/approvals/tests/test_state_machine.py:26:            password='T001'
apps/approvals/tests/test_state_machine.py:31:            user_id='M001',
apps/approvals/tests/test_state_machine.py:34:            password='M001'
data/templates/counselors_template.csv:2:T001,李老师,计算机学院,true,T001
data/templates/counselors_template.csv:3:T002,王老师,软件学院,true,T002
data/templates/class_mappings_template.csv:2:CS2020-01,T001
data/templates/class_mappings_template.csv:3:CS2020-02,T002
apps/notifications/tests/test_auto_notifications_api.py:33:            user_id='T001',
apps/notifications/tests/test_auto_notifications_api.py:38:            user_id='M001',
apps/notifications/tests/test_timeout_warnings.py:22:            user_id='T001',
apps/notifications/tests/test_timeout_warnings.py:28:            user_id='M001',
apps/notifications/tests/test_models.py:16:            user_id='T001',
apps/notifications/tests/test_api.py:24:            user_id='T001',
apps/notifications/tests/test_auto_notifications.py:34:            user_id='T001',
apps/notifications/tests/test_auto_notifications.py:39:            user_id='M001',
data/additional_staff.csv:2:20144020,肖延量,学工管理员,13636001781,,学生管理科科长
data/additional_staff.csv:3:19970545,李桃花,学工管理员,15907258727,,学生事务管理科长
data/additional_staff.csv:4:92008149,程婷,宿管员,13476778525,,"负责无楼栋学生审批（兜底宿管员）"
apps/applications/views.py:162:        fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')
apps/applications/tests/test_error_cases.py:47:            user_id='T001',
apps/applications/tests/test_error_cases.py:48:            password='T001',
apps/applications/tests/test_error_cases.py:53:            user_id='M001',
apps/applications/tests/test_error_cases.py:54:            password='M001',
apps/applications/tests/test_detail_permissions.py:24:        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
apps/applications/tests/test_detail_permissions.py:25:        self.counselor1.set_password('T001')
apps/applications/tests/test_detail_permissions.py:28:        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
apps/applications/tests/test_detail_permissions.py:29:        self.counselor2.set_password('T002')
apps/applications/tests/test_detail_permissions.py:32:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
apps/applications/tests/test_detail_permissions.py:33:        self.dorm_manager1.set_password('M001')
apps/applications/tests/test_detail_permissions.py:36:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
apps/applications/tests/test_detail_permissions.py:37:        self.dorm_manager2.set_password('M002')
apps/applications/tests/test_detail_permissions.py:79:        # Counselor T002 (assigned to CS2020-02) tries to access
apps/applications/tests/test_list_permissions.py:22:        self.counselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR)
apps/applications/tests/test_list_permissions.py:23:        self.counselor1.set_password('T001')
apps/applications/tests/test_list_permissions.py:26:        self.counselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR)
apps/applications/tests/test_list_permissions.py:27:        self.counselor2.set_password('T002')
apps/applications/tests/test_list_permissions.py:30:        self.dorm_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_MANAGER)
apps/applications/tests/test_list_permissions.py:31:        self.dorm_manager1.set_password('M001')
apps/applications/tests/test_list_permissions.py:34:        self.dorm_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_MANAGER)
apps/applications/tests/test_list_permissions.py:35:        self.dorm_manager2.set_password('M002')
apps/applications/tests/test_application_flow.py:28:            user_id='T001',
apps/applications/tests/test_application_flow.py:29:            password='T001',
apps/applications/tests/test_application_flow.py:35:            user_id='M001',
apps/applications/tests/test_application_flow.py:36:            password='M001',
apps/applications/tests/test_application_flow.py:81:            'user_id': 'M001',
apps/applications/tests/test_application_flow.py:82:            'password': 'M001'
apps/applications/tests/test_application_flow.py:102:            'user_id': 'T001',
apps/applications/tests/test_application_flow.py:103:            'password': 'T001'
apps/attachments/tests/test_upload.py:39:            user_id='T001',
apps/attachments/tests/test_upload.py:40:            password='T001',
apps/attachments/tests/test_download.py:39:            user_id='T001',
apps/attachments/tests/test_download.py:40:            password='T001',
apps/applications/tests/test_constraints.py:26:            user_id='T001',
apps/applications/tests/test_constraints.py:29:            password='T001'
apps/applications/tests/test_constraints.py:32:            user_id='M001',
apps/applications/tests/test_constraints.py:35:            password='M001'
apps/attachments/tests/test_delete.py:38:            user_id='T001',
apps/attachments/tests/test_delete.py:39:            password='T001',
apps/users/tests/test_import_csv.py:14:        User.objects.create_user(user_id='T001', name='李老师', role=UserRole.COUNSELOR, password='T001')
apps/users/tests/test_import_csv.py:15:        User.objects.create_user(user_id='T002', name='王老师', role=UserRole.COUNSELOR, password='T002')
apps/users/tests/test_import_csv.py:68:        csv_content = "class_id,counselor_employee_id\nCS2020-01,T001\nCS2020-02,T002"
apps/users/tests/test_import_csv.py:77:            self.assertEqual(mapping.counselor.user_id, 'T001')
apps/users/tests/test_import_csv.py:99:        counselor = User.objects.get(user_id='T001')
apps/attachments/tests/test_list.py:38:            user_id='T001',
apps/attachments/tests/test_list.py:39:            password='T001',
apps/attachments/tests/test_list.py:45:            user_id='T002',
apps/attachments/tests/test_list.py:46:            password='T002',
apps/users/tests/test_xg_user_sync.py:27:            user_id='T001',
apps/users/tests/test_xg_user_sync.py:103:                'number': 'T001',
apps/users/tests/test_xg_user_sync.py:118:        self.assertEqual(conflict['user_id'], 'T001')
apps/users/tests/test_xg_user_sync.py:197:            {'number': 'T001', 'name': '李老师', 'user_identity': '1'},
apps/users/tests/test_xg_user_sync.py:208:        self.assertEqual(result['existing_count'], 2)  # T001和2021001都存在
apps/users/tests/test_xg_user_sync.py:244:            user_id='T001',
apps/users/tests/test_xg_user_sync.py:284:        xg_users = [{'number': 'T001', 'name': '李老师', 'user_identity': '1'}]
apps/users/tests/test_xg_user_sync.py:349:            {'number': 'T001', 'name': '李老师', 'user_identity': '1'},
apps/users/tests/test_xg_user_sync.py:382:        counselor = User.objects.get(user_id='T001')
apps/users/management/commands/seed_data.py:60:            {'user_id': 'T001', 'name': '李老师'},
apps/users/management/commands/seed_data.py:61:            {'user_id': 'T002', 'name': '王老师'},
apps/users/management/commands/seed_data.py:80:            {'user_id': 'M001', 'name': '宿管员1'},
apps/users/management/commands/seed_data.py:81:            {'user_id': 'M002', 'name': '宿管员2'},
apps/users/management/commands/seed_data.py:114:            {'class_id': 'CS2020-01', 'dorm_manager_id': 'M001', 'counselor_id': 'T001'},
apps/users/management/commands/seed_data.py:115:            {'class_id': 'CS2020-02', 'dorm_manager_id': 'M002', 'counselor_id': 'T002'},
apps/users/management/commands/import_staff.py:93:            fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')

exec
/bin/bash -lc "rtk ./venv/bin/python manage.py shell <<'PY'
from apps.users.models import User
ids = ['M001','M002','T001','T002','2020001','2020002','19970545','20144020','92008149']
for u in User.objects.filter(user_id__in=ids).order_by('user_id'):
    print(u.user_id, u.name, u.role, u.department, u.building, u.active, u.created_at, u.updated_at)
PY" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 321ms:
19970545 李桃花 admin None None True 2026-06-06 15:24:08.386406+00:00 2026-06-06 15:24:08.386416+00:00
20144020 肖延量 admin None None True 2026-06-06 15:24:08.381332+00:00 2026-06-06 15:24:08.381358+00:00
2020001 张三 student None None True 2026-06-03 09:06:38.048173+00:00 2026-06-03 09:06:38.121384+00:00
2020002 李四 student None None True 2026-06-03 09:06:38.131009+00:00 2026-06-03 09:06:38.207350+00:00
92008149 程婷 dorm_manager None None True 2026-06-06 15:24:08.391454+00:00 2026-06-06 15:24:08.391462+00:00
M001 宿管员1 dorm_manager None None True 2026-06-03 09:06:38.991226+00:00 2026-06-03 09:06:39.066382+00:00
M002 宿管员2 dorm_manager None None True 2026-06-03 09:06:39.068519+00:00 2026-06-03 09:06:39.144708+00:00
T001 李老师 counselor None None True 2026-06-03 09:06:38.823620+00:00 2026-06-03 09:06:38.904156+00:00
T002 王老师 counselor None None True 2026-06-03 09:06:38.907129+00:00 2026-06-03 09:06:38.988743+00:00

codex
这里还有一个数据口径细节：两个学工管理员 `19970545/20144020` 也在宿管源文件中出现过，后续 `additional_staff.csv` 把他们覆盖为 `admin`，所以“宿管75 vs 73”的表象不是单纯 +2，还包含“+2测试宿管、-2被改角色、+1兜底、源文件实际72”的混合效果。
exec
/bin/bash -lc 'rtk head -n 8 data/dorm_managers_processed.csv' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
职工号,姓名,角色,手机,楼栋
92024022,冯慧芬,宿管员,15672450463,紫园1栋
92023036,孙亮亮,宿管员,18986517220,紫园2栋
92022013,方华英,宿管员,15072783987,紫园2栋
92025051,赵馨,宿管员,18871117105,紫园3栋
92021006,王旺萍,宿管员,13477663215,紫园3栋
92020060,陈细婷,宿管员,15271627693,紫园4栋
92024013,华娟,宿管员,18062222746,紫园4栋

exec
/bin/bash -lc 'rtk rg -n "19970545|20144020" data/dorm_managers_processed.csv data/2026年社区辅导员信息统计表.csv ../docs/2026年社区辅导员信息统计表.xls' in /home/caohui/projects/graduation-leave-system/backend
 exited 1 in 0ms:
exec
/bin/bash -lc "rtk ./venv/bin/python manage.py shell <<'PY'
from collections import Counter,defaultdict
from apps.users.models import User, UserRole
for role, key in [(UserRole.DORM_MANAGER, 'building'), (UserRole.COUNSELOR, 'department')]:
    vals = list(User.objects.filter(role=role, active=True).values_list(key, flat=True))
    c = Counter(vals)
    dups = {k:v for k,v in c.items() if k and v > 1}
    blanks = c.get(None, 0) + c.get('', 0)
    print(role, 'active', len(vals), 'duplicate_keys', dups, 'blank_or_null', blanks)
PY" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 380ms:
dorm_manager active 75 duplicate_keys {'紫园2栋': 2, '紫园3栋': 2, '紫园4栋': 2, '紫园5栋': 2, '紫园6栋': 2, '紫园7栋': 2, '紫园8栋': 2, '紫园9栋': 2, '紫园10栋': 2, '柳园1栋': 2, '柳园2栋': 2, '柳园3栋': 2, '柳园4栋': 2, '柳园5栋': 2, '柳园6栋': 2, '柳园7栋': 2, '柳园8栋': 2, '柳园9栋': 2, '柳园10栋': 2, '荷园1栋': 2, '荷园3栋': 2, '荷园5栋': 2, '荷园6栋': 2, '兰园1栋': 2, '兰园2栋': 2, '兰园3栋': 2, '兰园4栋': 2, '兰园5栋': 2, '兰园6栋': 2, '兰园7栋': 2, '兰园8栋': 2, '兰园9栋': 2, '兰园10栋': 2, '兰园12栋': 4} blank_or_null 3
counselor active 22 duplicate_keys {} blank_or_null 22

codex
更关键的联调风险已经确认：当前22个辅导员的 `department` 全为空，而审批代码按 `department` 精确查辅导员。这意味着学生能提交到宿管，但宿管通过后无法生成辅导员审批。这个是 Phase 4 前必须修正或至少导入前修正的数据/脚本问题。
exec
/bin/bash -lc 'rtk head -n 3 data/file5_students_merged_v2.csv' in /home/caohui/projects/graduation-leave-system/backend
exec
/bin/bash -lc 'rtk head -n 8 data/counselors_processed.csv' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 193ms:
 succeeded in 176ms:
exec
/bin/bash -lc "rtk ./venv/bin/python manage.py shell <<'PY'
from collections import Counter
from apps.users.models import User, UserRole
print('student departments sample', list(User.objects.filter(role=UserRole.STUDENT).exclude(department__isnull=True).values_list('department', flat=True).distinct()[:30]))
print('counselors', list(User.objects.filter(role=UserRole.COUNSELOR).values_list('user_id','name','department')[:30]))
PY" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 557ms:
student departments sample ['体育学院', '教育学院', '机电与智能制造学院', '数学与统计学院', '旅游文化与地理科学学院', '化学化工学院', '计算机与人工智能学院', '外国语学院', '政法学院', '新闻与传播学院', '建筑与工程学院', '物理与电信学院', '马克思主义学院', '商学院', '音乐与戏剧学院', '李时珍中医药学院', '文学院(苏东坡书院)', '美术学院', '生命科学学院']
counselors [('T001', '李老师', None), ('T002', '王老师', None), ('20250015', '胡晓炀', None), ('92005340', '钟秀娟', None), ('20220048', '吴灿', None), ('20210044', '张小东', None), ('20210021', '杨丽媛', None), ('20148522', '侯晓文', None), ('20200106', '张兴', None), ('20148523', '陈劲松', None), ('20148396', '程文学', None), ('20220052', '胡乐', None), ('20210063', '龚文朋', None), ('20210054', '郑红妍', None), ('20020559', '张宏洋', None), ('20240020', '王娜娜', None), ('20108090', '袁婷', None), ('20230039', '方皓正', None), ('20148444', '邱锐', None), ('20230044', '吴勇', None), ('20250016', '罗真', None), ('20210066', '金玲', None)]

codex
数据差异本身可以解释为测试残留，但我不会把“Phase 4无阻塞”直接判通过：当前辅导员导入缺少学院字段，属于比14人差异更实质的流程阻塞。接下来我会整理成正式审查 artifact，并记录协作事件。
codex
我会按协作协议先声明 Codex 已接手这个审查任务，然后写入审查 artifact，最后追加完成事件。共享状态写入会通过 journal lock 保护。
exec
/bin/bash -lc "rtk ./venv/bin/python - <<'PY'
import json, os, shutil
from pathlib import Path
from datetime import datetime, timezone
base = Path('../.omc/collaboration')
lock = base / 'locks' / 'journal.lock'
task_id = 'TASK-20260606-09'
now = datetime.now(timezone.utc).isoformat()
os.mkdir(lock)
try:
    (lock / 'owner.json').write_text(json.dumps({
        'agent': 'codex', 'task_id': task_id, 'created_at': now,
        'heartbeat_at': now, 'reason': 'claim Phase 3 data discrepancy review'
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    events_path = base / 'events.jsonl'
    events = []
    with events_path.open(encoding='utf-8') as f:
        for lineno, line in enumerate(f, 1):
            if line.strip():
                event = json.loads(line)
                events.append(event)
    ids = [e['id'] for e in events]
    if len(ids) "'!= len(set(ids)):
        raise RuntimeError('"'duplicate event ids')
    next_id = max(ids, default=0) + 1
    event = {
        'id': next_id,
        'type': 'task_claimed',
        'agent': 'codex',
        'timestamp': now,
        'task_id': task_id,
        'summary': 'Codex claimed Phase 3 data discrepancy review',
        'status': 'in_progress'
    }
    with events_path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(event, ensure_ascii=False, separators=(',', ':')) + '\\n')
    state = {
        'workflow_id': 'implementation-plan-review',
        'current_task': task_id,
        'active_agent': 'codex',
        'status': 'in_progress',
        'last_event_id': next_id,
        'updated_at': now
    }
    tmp = base / 'state.json.tmp.codex'
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\\n', encoding='utf-8')
    json.loads(tmp.read_text(encoding='utf-8'))
    os.replace(tmp, base / 'state.json')
finally:
    shutil.rmtree(lock)
PY" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
codex
任务已在协作日志中标记为 Codex 接手。我会取关键代码行号，确保审查意见能落到具体证据，而不是只给结论。
exec
/bin/bash -lc "rtk nl -ba apps/applications/views.py | rtk sed -n '125,180p'" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
   125	    ).first()
   126	    if existing:
   127	        return Response({'error': {'code': 'CONFLICT', 'message': '已有待审批或已通过的申请，不能重复提交',
   128	                                    'details': {'student_id': user.user_id, 'existing_application_id': existing.application_id, 'status': existing.status}}},
   129	                        status=status.HTTP_409_CONFLICT)
   130	
   131	    serializer = ApplicationCreateSerializer(data=request.data)
   132	    if not serializer.is_valid():
   133	        return Response({'error': {'code': 'VALIDATION_ERROR', 'message': '请求参数验证失败',
   134	                                    'details': serializer.errors}},
   135	                        status=status.HTTP_400_BAD_REQUEST)
   136	
   137	    provider = MockDormCheckoutProvider()
   138	    dorm_status = provider.check_status(user.user_id)
   139	
   140	    if dorm_status.status != DormCheckoutStatus.COMPLETED:
   141	        return Response({'error': {'code': 'DORM_BLOCKED', 'message': '宿舍清退未完成，无法提交申请',
   142	                                    'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
   143	                                                'blocking_reason': dorm_status.blocking_reason}}},
   144	                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
   145	
   146	    # Find dorm manager with fallback mechanism
   147	    dorm_manager = None
   148	    building = user.building
   149	
   150	    # Try to find dorm manager by building
   151	    if building and building.strip():
   152	        try:
   153	            dorm_manager = User.objects.get(role=UserRole.DORM_MANAGER, building=building, active=True)
   154	        except User.DoesNotExist:
   155	            pass  # Will try fallback
   156	        except User.MultipleObjectsReturned:
   157	            dorm_manager = User.objects.filter(role=UserRole.DORM_MANAGER, building=building, active=True).first()
   158	
   159	    # Fallback: use default dorm manager for students without building
   160	    if not dorm_manager:
   161	        from django.conf import settings
   162	        fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')
   163	        try:
   164	            dorm_manager = User.objects.get(role=UserRole.DORM_MANAGER, user_id=fallback_id, active=True)
   165	        except User.DoesNotExist:
   166	            return Response({'error': {'code': 'NOT_FOUND', 'message': '无可用宿管员',
   167	                                        'details': {'building': building or '未分配', 'fallback_id': fallback_id}}},
   168	                            status=status.HTTP_404_NOT_FOUND)
   169	
   170	    dorm_manager_name = dorm_manager.name
   171	
   172	    application = Application.objects.create(
   173	        application_id=f'app_{uuid.uuid4().hex[:8]}',
   174	        student=user,
   175	        student_name=user.name,
   176	        class_id=user.class_id,
   177	        reason=serializer.validated_data['reason'],
   178	        leave_date=serializer.validated_data['leave_date'],
   179	        status=ApplicationStatus.PENDING_DORM_MANAGER,
   180	        dorm_checkout_status=dorm_status.status

exec
/bin/bash -lc "rtk nl -ba apps/users/management/commands/import_students.py | rtk sed -n '25,72p'" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
    25	        dry_run = options['dry_run']
    26	        mode = options['mode']
    27	
    28	        if not Path(file_path).exists():
    29	            raise CommandError(f'File not found: {file_path}')
    30	
    31	        # Safety check for clean mode
    32	        if mode == 'clean' and not dry_run:
    33	            from apps.applications.models import Application
    34	            active_apps = Application.objects.exclude(status='rejected').count()
    35	            if active_apps > 0:
    36	                raise CommandError(
    37	                    f'Cannot clean import: {active_apps} active applications exist. '
    38	                    'Use append mode or manually clear applications first.'
    39	                )
    40	
    41	        stats = self._import_students(file_path, dry_run, mode)
    42	        self._print_results(stats, dry_run)
    43	
    44	    def _import_students(self, file_path, dry_run, mode):
    45	        stats = {
    46	            'total': 0,
    47	            'created': 0,
    48	            'updated': 0,
    49	            'skipped': 0,
    50	            'errors': []
    51	        }
    52	
    53	        with open(file_path, 'r', encoding='utf-8-sig') as f:
    54	            reader = csv.DictReader(f)
    55	
    56	            # Validate required columns
    57	            required = ['user_id', 'name', 'class_id']
    58	            missing = [col for col in required if col not in reader.fieldnames]
    59	            if missing:
    60	                raise CommandError(f'Missing required columns: {", ".join(missing)}')
    61	
    62	            if mode == 'clean' and not dry_run:
    63	                deleted = User.objects.filter(role=UserRole.STUDENT).delete()
    64	                self.stdout.write(f'Deleted {deleted[0]} existing students')
    65	
    66	            rows = list(reader)
    67	            stats['total'] = len(rows)
    68	
    69	            with transaction.atomic():
    70	                for row in rows:
    71	                    try:
    72	                        self._process_row(row, stats, dry_run)

exec
/bin/bash -lc "rtk nl -ba apps/users/management/commands/import_staff.py | rtk sed -n '60,122p'" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
    60	    def _process_row(self, row, stats, dry_run):
    61	        # Support both Chinese and English column names
    62	        user_id = (row.get('职工号') or row.get('user_id') or '').strip()
    63	        name = (row.get('姓名') or row.get('name') or '').strip()
    64	        role_str = (row.get('角色') or row.get('role') or '').strip()
    65	        phone = (row.get('手机') or row.get('phone') or '').strip()
    66	        building = (row.get('楼栋') or row.get('building') or '').strip()
    67	
    68	        if not user_id or not name or not role_str:
    69	            stats['skipped'] += 1
    70	            stats['errors'].append(f'Missing required fields: user_id={user_id}, name={name}, role={role_str}')
    71	            return
    72	
    73	        # Map role string to UserRole
    74	        role_map = {
    75	            '宿管员': UserRole.DORM_MANAGER,
    76	            'DORM_MANAGER': UserRole.DORM_MANAGER,
    77	            '辅导员': UserRole.COUNSELOR,
    78	            'COUNSELOR': UserRole.COUNSELOR,
    79	            '学工管理员': UserRole.ADMIN,
    80	            'ADMIN': UserRole.ADMIN,
    81	        }
    82	
    83	        role = role_map.get(role_str)
    84	        if not role:
    85	            stats['skipped'] += 1
    86	            stats['errors'].append(f'{user_id}: Unknown role "{role_str}"')
    87	            return
    88	
    89	        # Validate building requirement
    90	        if role == UserRole.DORM_MANAGER and not building:
    91	            # Allow empty building for fallback dorm manager
    92	            from django.conf import settings
    93	            fallback_id = getattr(settings, 'FALLBACK_DORM_MANAGER_USER_ID', '92008149')
    94	            if user_id != fallback_id:
    95	                self.stdout.write(
    96	                    self.style.WARNING(
    97	                        f'{user_id} ({name}): DORM_MANAGER without building (not fallback manager)'
    98	                    )
    99	                )
   100	
   101	        if dry_run:
   102	            exists = User.objects.filter(user_id=user_id).exists()
   103	            if exists:
   104	                stats['updated'] += 1
   105	            else:
   106	                stats['created'] += 1
   107	            stats['by_role'][role] = stats['by_role'].get(role, 0) + 1
   108	        else:
   109	            user, created = User.objects.update_or_create(
   110	                user_id=user_id,
   111	                defaults={
   112	                    'name': name,
   113	                    'role': role,
   114	                    'phone': phone if phone else None,
   115	                    'building': building if building else None,
   116	                    'active': True,
   117	                }
   118	            )
   119	
   120	            if created:
   121	                stats['created'] += 1
   122	            else:

exec
/bin/bash -lc "rtk nl -ba apps/approvals/views.py | rtk sed -n '1,18p;145,171p'" in /home/caohui/projects/graduation-leave-system/backend
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
   163	        # Get counselor by department
   164	        try:
   165	            counselor = User.objects.get(role=UserRole.COUNSELOR, department=application.student.department, active=True)
   166	        except User.DoesNotExist:
   167	            return Response({'error': {'code': 'NOT_FOUND', 'message': '该学院辅导员不存在',
   168	                                        'details': {'department': application.student.department}}},
   169	                            status=status.HTTP_404_NOT_FOUND)
   170	
   171	        Approval.objects.create(

exec
/bin/bash -lc 'rtk date -u +%Y%m%d-%H%M' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
20260606-1548

codex
我需要更正刚才的一个中间判断：`19970545/20144020` 是 `additional_staff.csv` 中的学工管理员，不在已处理宿管 CSV 中；宿管 +2 可以直接归因为 `M001/M002` 测试账号残留。正式审查会按这个修正后的结论写入。
apply patch
patch: completed
/home/caohui/projects/graduation-leave-system/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md
diff --git a/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md b/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md
new file mode 100644
index 0000000000000000000000000000000000000000..f4f206976f9830a6f43ce74344fc1b89013d12c3
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md
@@ -0,0 +1,133 @@
+# Phase 3数据导入轻微差异 - Codex审查意见
+
+**任务ID:** TASK-20260606-09  
+**审查日期:** 2026-06-06  
+**审查人:** Codex  
+**审查范围:** Phase 3导入后用户数量差异、功能影响、生产导入策略、Phase 4阻塞判断
+
+## 审查结论
+
+14人差异本身不构成审批路由、权限控制或前端页面开发的直接阻塞；根因已可定位为历史测试/种子数据残留，且不是TMP ID问题。
+
+但当前环境存在两个比14人差异更实质的Phase 4联调阻塞：
+
+1. 当前数据库有1个非rejected申请，`import_students --mode clean` 会被安全检查拦截。
+2. 辅导员审批路由当前不可用：导入脚本未写入辅导员 `department`，当前22名辅导员 `department` 均为空；同时 `apps/approvals/views.py` 使用 `User.objects` 但未导入 `User`。
+
+因此：前端静态页面/接口契约开发不阻塞；完整端到端申请-宿管-辅导员审批联调在Phase 4前应先修正。
+
+## 证据摘要
+
+只读数据库比对结果：
+
+- 源数据并集：6041人，包含学生5946、宿管72、辅导员20、additional_staff 3。
+- 当前数据库：6056人；若排除既有 `dean` 角色，为6055人，与任务文档口径一致。
+- 分角色：学生5956、宿管75、辅导员22、admin 2、dean 1。
+- TMP ID：0。
+- 当前非rejected申请：1个，`app_4ae6dd14 / 2020001 / approved`。
+
+差异身份：
+
+- 额外学生10人：`2020001` 到 `2020010`，均为测试学生。
+- 额外宿管2人：`M001`、`M002`，均为测试宿管。
+- 额外辅导员2人：`T001`、`T002`，均为测试辅导员。
+
+相关代码依据：
+
+- `import_students --mode clean` 在存在非rejected申请时拒绝执行：`apps/users/management/commands/import_students.py:31`。
+- `clean` 只删除 `role=student` 用户，不清理宿管/辅导员/admin：`apps/users/management/commands/import_students.py:62`。
+- `import_staff` 当前只读取 `phone/building`，没有读取或写入 `department`：`apps/users/management/commands/import_staff.py:62`。
+- 学生提交申请时宿管按 `building` 查找，找不到走兜底：`apps/applications/views.py:151`。
+- 宿管通过后辅导员按学生 `department` 精确查找：`apps/approvals/views.py:163`。
+- `apps/approvals/views.py` 只导入 `UserRole`，未导入 `User`，但后续使用 `User.objects`：`apps/approvals/views.py:14`。
+
+## 影响评估
+
+### 功能影响
+
+14个历史测试账号对主流程没有直接破坏性影响：
+
+- 宿管路由基于学生 `building`，并且有兜底宿管；额外测试宿管 `M001/M002` 的 `building` 为空，不会按楼栋承接真实学生。
+- 权限控制基于 `role` 和当前登录用户，额外账号不会提升真实用户权限。
+- 额外测试学生不会影响真实学生提交申请，除非被用于登录和操作。
+
+但会造成环境数据污染：
+
+- 用户统计、覆盖率、角色人数会偏离源数据口径。
+- `2020001` 已有关联approved申请，会阻塞 `clean` 导入。
+- 测试账号如保留在生产，会带来审计、误登录和数据可信度风险。
+
+### 数据一致性影响
+
+当前差异不影响“TMP清零”和“兜底宿管存在”这两个硬指标，但会降低验收口径的可解释性。生产验收不应接受“已知测试账号残留”的用户基线。
+
+辅导员 `department` 缺失是独立的一致性问题，影响实际审批流，不应被14人差异掩盖。
+
+### 性能影响
+
+14条额外用户记录对性能无实际影响。
+
+## 根因调查建议
+
+不需要继续做大范围根因调查；当前已足够定位：
+
+- 10个学生、2个宿管、2个辅导员均符合项目测试/种子数据命名模式。
+- 创建时间集中在2026-06-03，早于Phase 3导入。
+- 源数据对比没有缺失主批次用户。
+
+建议保留一次性审计记录即可：列出额外账号、关联申请、清理方式和清理时间。
+
+## 生产导入策略推荐
+
+推荐：生产使用 clean/rebuild 基线，不使用 append 作为首次上线导入策略。
+
+具体建议：
+
+1. 新生产库优先从空库迁移后导入。保留必要系统账号或超级管理员，批量导入学生、宿管、辅导员、学工管理员、兜底宿管。
+2. 如果不是空库，先确认没有有效业务申请；否则不得直接删除学生。
+3. 不建议只运行现有 `import_students --mode clean` 后继续 append staff，因为该命令只清学生，无法清掉 `M001/M002/T001/T002` 这类历史 staff。
+4. 对当前开发/测试库，建议手动清理已知测试账号及其测试申请，或重建库；清理后重新执行 dry-run 和正式导入。
+5. append 模式仅适合后续增量补录，前提是输入文件经过白名单比对，且导入后运行“DB用户集合 - 源数据集合 = 0”的校验。
+
+不推荐方案A append：会保留污染数据，生产验收口径不干净。
+
+不推荐单纯方案C手动清理作为生产主策略：适合修复当前环境，不适合作为可复现上线流程。
+
+## 19名额外研究生处理建议
+
+建议暂不纳入主批次，不阻塞Phase 4。
+
+理由：
+
+- 这19人不在File1/File2/File5主批次。
+- 学号特征为2021/2022/2023，不足以证明属于2026届主批次。
+- 当前缺少学院/班级/楼栋/辅导员映射等路由关键字段。
+
+处理优先级：Phase 3.5补充批次，等待业务确认。确认属于2026届后，再按补充批次导入，并明确无楼栋是否走兜底宿管、学院如何映射辅导员。
+
+## Phase 4阻塞判断
+
+不阻塞：
+
+- 前端页面开发。
+- 登录、列表、表单、状态展示等基于现有API契约的开发。
+- 使用mock或固定测试账号做非端到端页面验收。
+
+阻塞：
+
+- 真实数据端到端联调。
+- 宿管通过后创建辅导员审批。
+- 生产导入验收。
+
+Phase 4前建议先完成以下P0/P1：
+
+- P0：修复 `apps/approvals/views.py` 缺少 `User` 导入。
+- P0：补齐辅导员 `department` 导入字段，或调整路由模型为明确的学院-辅导员映射。
+- P1：清理当前环境测试账号 `2020001-2020010/M001/M002/T001/T002` 及测试申请，或重建库。
+- P1：为生产导入增加导后校验脚本，至少校验角色人数、源数据缺失、DB额外用户、TMP ID、兜底宿管、学生无楼栋数量、辅导员department覆盖。
+
+## 最终建议
+
+接受Phase 3“主批次数据已导入、TMP已清零、兜底宿管已就位”的阶段性结论，但不要把当前数据库作为生产基线。
+
+生产上线采用可复现的clean/rebuild导入；19名额外研究生进入Phase 3.5待业务确认；Phase 4页面开发可以继续，但端到端审批联调前必须修正辅导员路由字段和 `User` 导入问题。

diff --git a/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md b/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md
new file mode 100644
index 0000000000000000000000000000000000000000..f4f206976f9830a6f43ce74344fc1b89013d12c3
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md
@@ -0,0 +1,133 @@
+# Phase 3数据导入轻微差异 - Codex审查意见
+
+**任务ID:** TASK-20260606-09  
+**审查日期:** 2026-06-06  
+**审查人:** Codex  
+**审查范围:** Phase 3导入后用户数量差异、功能影响、生产导入策略、Phase 4阻塞判断
+
+## 审查结论
+
+14人差异本身不构成审批路由、权限控制或前端页面开发的直接阻塞；根因已可定位为历史测试/种子数据残留，且不是TMP ID问题。
+
+但当前环境存在两个比14人差异更实质的Phase 4联调阻塞：
+
+1. 当前数据库有1个非rejected申请，`import_students --mode clean` 会被安全检查拦截。
+2. 辅导员审批路由当前不可用：导入脚本未写入辅导员 `department`，当前22名辅导员 `department` 均为空；同时 `apps/approvals/views.py` 使用 `User.objects` 但未导入 `User`。
+
+因此：前端静态页面/接口契约开发不阻塞；完整端到端申请-宿管-辅导员审批联调在Phase 4前应先修正。
+
+## 证据摘要
+
+只读数据库比对结果：
+
+- 源数据并集：6041人，包含学生5946、宿管72、辅导员20、additional_staff 3。
+- 当前数据库：6056人；若排除既有 `dean` 角色，为6055人，与任务文档口径一致。
+- 分角色：学生5956、宿管75、辅导员22、admin 2、dean 1。
+- TMP ID：0。
+- 当前非rejected申请：1个，`app_4ae6dd14 / 2020001 / approved`。
+
+差异身份：
+
+- 额外学生10人：`2020001` 到 `2020010`，均为测试学生。
+- 额外宿管2人：`M001`、`M002`，均为测试宿管。
+- 额外辅导员2人：`T001`、`T002`，均为测试辅导员。
+
+相关代码依据：
+
+- `import_students --mode clean` 在存在非rejected申请时拒绝执行：`apps/users/management/commands/import_students.py:31`。
+- `clean` 只删除 `role=student` 用户，不清理宿管/辅导员/admin：`apps/users/management/commands/import_students.py:62`。
+- `import_staff` 当前只读取 `phone/building`，没有读取或写入 `department`：`apps/users/management/commands/import_staff.py:62`。
+- 学生提交申请时宿管按 `building` 查找，找不到走兜底：`apps/applications/views.py:151`。
+- 宿管通过后辅导员按学生 `department` 精确查找：`apps/approvals/views.py:163`。
+- `apps/approvals/views.py` 只导入 `UserRole`，未导入 `User`，但后续使用 `User.objects`：`apps/approvals/views.py:14`。
+
+## 影响评估
+
+### 功能影响
+
+14个历史测试账号对主流程没有直接破坏性影响：
+
+- 宿管路由基于学生 `building`，并且有兜底宿管；额外测试宿管 `M001/M002` 的 `building` 为空，不会按楼栋承接真实学生。
+- 权限控制基于 `role` 和当前登录用户，额外账号不会提升真实用户权限。
+- 额外测试学生不会影响真实学生提交申请，除非被用于登录和操作。
+
+但会造成环境数据污染：
+
+- 用户统计、覆盖率、角色人数会偏离源数据口径。
+- `2020001` 已有关联approved申请，会阻塞 `clean` 导入。
+- 测试账号如保留在生产，会带来审计、误登录和数据可信度风险。
+
+### 数据一致性影响
+
+当前差异不影响“TMP清零”和“兜底宿管存在”这两个硬指标，但会降低验收口径的可解释性。生产验收不应接受“已知测试账号残留”的用户基线。
+
+辅导员 `department` 缺失是独立的一致性问题，影响实际审批流，不应被14人差异掩盖。
+
+### 性能影响
+
+14条额外用户记录对性能无实际影响。
+
+## 根因调查建议
+
+不需要继续做大范围根因调查；当前已足够定位：
+
+- 10个学生、2个宿管、2个辅导员均符合项目测试/种子数据命名模式。
+- 创建时间集中在2026-06-03，早于Phase 3导入。
+- 源数据对比没有缺失主批次用户。
+
+建议保留一次性审计记录即可：列出额外账号、关联申请、清理方式和清理时间。
+
+## 生产导入策略推荐
+
+推荐：生产使用 clean/rebuild 基线，不使用 append 作为首次上线导入策略。
+
+具体建议：
+
+1. 新生产库优先从空库迁移后导入。保留必要系统账号或超级管理员，批量导入学生、宿管、辅导员、学工管理员、兜底宿管。
+2. 如果不是空库，先确认没有有效业务申请；否则不得直接删除学生。
+3. 不建议只运行现有 `import_students --mode clean` 后继续 append staff，因为该命令只清学生，无法清掉 `M001/M002/T001/T002` 这类历史 staff。
+4. 对当前开发/测试库，建议手动清理已知测试账号及其测试申请，或重建库；清理后重新执行 dry-run 和正式导入。
+5. append 模式仅适合后续增量补录，前提是输入文件经过白名单比对，且导入后运行“DB用户集合 - 源数据集合 = 0”的校验。
+
+不推荐方案A append：会保留污染数据，生产验收口径不干净。
+
+不推荐单纯方案C手动清理作为生产主策略：适合修复当前环境，不适合作为可复现上线流程。
+
+## 19名额外研究生处理建议
+
+建议暂不纳入主批次，不阻塞Phase 4。
+
+理由：
+
+- 这19人不在File1/File2/File5主批次。
+- 学号特征为2021/2022/2023，不足以证明属于2026届主批次。
+- 当前缺少学院/班级/楼栋/辅导员映射等路由关键字段。
+
+处理优先级：Phase 3.5补充批次，等待业务确认。确认属于2026届后，再按补充批次导入，并明确无楼栋是否走兜底宿管、学院如何映射辅导员。
+
+## Phase 4阻塞判断
+
+不阻塞：
+
+- 前端页面开发。
+- 登录、列表、表单、状态展示等基于现有API契约的开发。
+- 使用mock或固定测试账号做非端到端页面验收。
+
+阻塞：
+
+- 真实数据端到端联调。
+- 宿管通过后创建辅导员审批。
+- 生产导入验收。
+
+Phase 4前建议先完成以下P0/P1：
+
+- P0：修复 `apps/approvals/views.py` 缺少 `User` 导入。
+- P0：补齐辅导员 `department` 导入字段，或调整路由模型为明确的学院-辅导员映射。
+- P1：清理当前环境测试账号 `2020001-2020010/M001/M002/T001/T002` 及测试申请，或重建库。
+- P1：为生产导入增加导后校验脚本，至少校验角色人数、源数据缺失、DB额外用户、TMP ID、兜底宿管、学生无楼栋数量、辅导员department覆盖。
+
+## 最终建议
+
+接受Phase 3“主批次数据已导入、TMP已清零、兜底宿管已就位”的阶段性结论，但不要把当前数据库作为生产基线。
+
+生产上线采用可复现的clean/rebuild导入；19名额外研究生进入Phase 3.5待业务确认；Phase 4页面开发可以继续，但端到端审批联调前必须修正辅导员路由字段和 `User` 导入问题。

codex
审查 artifact 已写入。我会验证文件内容并把 artifact_created/completed 事件追加到协作日志。
exec
/bin/bash -lc "rtk sed -n '1,260p' ../.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
# Phase 3数据导入轻微差异 - Codex审查意见

**任务ID:** TASK-20260606-09  
**审查日期:** 2026-06-06  
**审查人:** Codex  
**审查范围:** Phase 3导入后用户数量差异、功能影响、生产导入策略、Phase 4阻塞判断

## 审查结论

14人差异本身不构成审批路由、权限控制或前端页面开发的直接阻塞；根因已可定位为历史测试/种子数据残留，且不是TMP ID问题。

但当前环境存在两个比14人差异更实质的Phase 4联调阻塞：

1. 当前数据库有1个非rejected申请，`import_students --mode clean` 会被安全检查拦截。
2. 辅导员审批路由当前不可用：导入脚本未写入辅导员 `department`，当前22名辅导员 `department` 均为空；同时 `apps/approvals/views.py` 使用 `User.objects` 但未导入 `User`。

因此：前端静态页面/接口契约开发不阻塞；完整端到端申请-宿管-辅导员审批联调在Phase 4前应先修正。

## 证据摘要

只读数据库比对结果：

- 源数据并集：6041人，包含学生5946、宿管72、辅导员20、additional_staff 3。
- 当前数据库：6056人；若排除既有 `dean` 角色，为6055人，与任务文档口径一致。
- 分角色：学生5956、宿管75、辅导员22、admin 2、dean 1。
- TMP ID：0。
- 当前非rejected申请：1个，`app_4ae6dd14 / 2020001 / approved`。

差异身份：

- 额外学生10人：`2020001` 到 `2020010`，均为测试学生。
- 额外宿管2人：`M001`、`M002`，均为测试宿管。
- 额外辅导员2人：`T001`、`T002`，均为测试辅导员。

相关代码依据：

- `import_students --mode clean` 在存在非rejected申请时拒绝执行：`apps/users/management/commands/import_students.py:31`。
- `clean` 只删除 `role=student` 用户，不清理宿管/辅导员/admin：`apps/users/management/commands/import_students.py:62`。
- `import_staff` 当前只读取 `phone/building`，没有读取或写入 `department`：`apps/users/management/commands/import_staff.py:62`。
- 学生提交申请时宿管按 `building` 查找，找不到走兜底：`apps/applications/views.py:151`。
- 宿管通过后辅导员按学生 `department` 精确查找：`apps/approvals/views.py:163`。
- `apps/approvals/views.py` 只导入 `UserRole`，未导入 `User`，但后续使用 `User.objects`：`apps/approvals/views.py:14`。

## 影响评估

### 功能影响

14个历史测试账号对主流程没有直接破坏性影响：

- 宿管路由基于学生 `building`，并且有兜底宿管；额外测试宿管 `M001/M002` 的 `building` 为空，不会按楼栋承接真实学生。
- 权限控制基于 `role` 和当前登录用户，额外账号不会提升真实用户权限。
- 额外测试学生不会影响真实学生提交申请，除非被用于登录和操作。

但会造成环境数据污染：

- 用户统计、覆盖率、角色人数会偏离源数据口径。
- `2020001` 已有关联approved申请，会阻塞 `clean` 导入。
- 测试账号如保留在生产，会带来审计、误登录和数据可信度风险。

### 数据一致性影响

当前差异不影响“TMP清零”和“兜底宿管存在”这两个硬指标，但会降低验收口径的可解释性。生产验收不应接受“已知测试账号残留”的用户基线。

辅导员 `department` 缺失是独立的一致性问题，影响实际审批流，不应被14人差异掩盖。

### 性能影响

14条额外用户记录对性能无实际影响。

## 根因调查建议

不需要继续做大范围根因调查；当前已足够定位：

- 10个学生、2个宿管、2个辅导员均符合项目测试/种子数据命名模式。
- 创建时间集中在2026-06-03，早于Phase 3导入。
- 源数据对比没有缺失主批次用户。

建议保留一次性审计记录即可：列出额外账号、关联申请、清理方式和清理时间。

## 生产导入策略推荐

推荐：生产使用 clean/rebuild 基线，不使用 append 作为首次上线导入策略。

具体建议：

1. 新生产库优先从空库迁移后导入。保留必要系统账号或超级管理员，批量导入学生、宿管、辅导员、学工管理员、兜底宿管。
2. 如果不是空库，先确认没有有效业务申请；否则不得直接删除学生。
3. 不建议只运行现有 `import_students --mode clean` 后继续 append staff，因为该命令只清学生，无法清掉 `M001/M002/T001/T002` 这类历史 staff。
4. 对当前开发/测试库，建议手动清理已知测试账号及其测试申请，或重建库；清理后重新执行 dry-run 和正式导入。
5. append 模式仅适合后续增量补录，前提是输入文件经过白名单比对，且导入后运行“DB用户集合 - 源数据集合 = 0”的校验。

不推荐方案A append：会保留污染数据，生产验收口径不干净。

不推荐单纯方案C手动清理作为生产主策略：适合修复当前环境，不适合作为可复现上线流程。

## 19名额外研究生处理建议

建议暂不纳入主批次，不阻塞Phase 4。

理由：

- 这19人不在File1/File2/File5主批次。
- 学号特征为2021/2022/2023，不足以证明属于2026届主批次。
- 当前缺少学院/班级/楼栋/辅导员映射等路由关键字段。

处理优先级：Phase 3.5补充批次，等待业务确认。确认属于2026届后，再按补充批次导入，并明确无楼栋是否走兜底宿管、学院如何映射辅导员。

## Phase 4阻塞判断

不阻塞：

- 前端页面开发。
- 登录、列表、表单、状态展示等基于现有API契约的开发。
- 使用mock或固定测试账号做非端到端页面验收。

阻塞：

- 真实数据端到端联调。
- 宿管通过后创建辅导员审批。
- 生产导入验收。

Phase 4前建议先完成以下P0/P1：

- P0：修复 `apps/approvals/views.py` 缺少 `User` 导入。
- P0：补齐辅导员 `department` 导入字段，或调整路由模型为明确的学院-辅导员映射。
- P1：清理当前环境测试账号 `2020001-2020010/M001/M002/T001/T002` 及测试申请，或重建库。
- P1：为生产导入增加导后校验脚本，至少校验角色人数、源数据缺失、DB额外用户、TMP ID、兜底宿管、学生无楼栋数量、辅导员department覆盖。

## 最终建议

接受Phase 3“主批次数据已导入、TMP已清零、兜底宿管已就位”的阶段性结论，但不要把当前数据库作为生产基线。

生产上线采用可复现的clean/rebuild导入；19名额外研究生进入Phase 3.5待业务确认；Phase 4页面开发可以继续，但端到端审批联调前必须修正辅导员路由字段和 `User` 导入问题。

exec
/bin/bash -lc 'rtk cat ../.omc/collaboration/state.json' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
{
  "workflow_id": "implementation-plan-review",
  "current_task": "TASK-20260606-09",
  "active_agent": "codex",
  "status": "in_progress",
  "last_event_id": 13,
  "updated_at": "2026-06-06T15:47:41.175851+00:00"
}

exec
/bin/bash -lc 'rtk tail -n 8 ../.omc/collaboration/events.jsonl' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
{"id":6,"type":"completed","agent":"codex","timestamp":"2026-06-05T05:13:50.860Z","task_id":"TASK-20260605-03","summary":"Codex completed implementation plan review","artifacts":[".omc/collaboration/artifacts/20260605-codex-implementation-plan-review.md"],"status":"completed"}
{"id": 7, "type": "task_created", "agent": "claude", "timestamp": "2026-06-05T19:55:07.600892+00:00", "summary": "Created task: Phase 0 P0\u963b\u585e\uff1a116\u4e2aFile2\u72ec\u6709\u5b66\u751f\u7f3a\u5c11\u697c\u680b\u6570\u636e\uff0c\u5bfc\u81f4\u5bbf\u7ba1\u5458\u8def\u7531\u5931\u8d25\uff0898.0% vs 100%\u95e8\u7981\u8981\u6c42\uff09\u3002\u9700\u8981\u4e1a\u52a1\u51b3\u7b56\uff1a1)\u63a5\u53d798%\u8986\u76d6\u7387\u4f5c\u4e3a\u53ef\u63a5\u53d7\u6807\u51c6 2)\u6392\u9664\u8fd9116\u540d\u5b66\u751f\u76f4\u5230\u8865\u5145\u697c\u680b\u6570\u636e 3)\u8981\u6c42\u7528\u6237\u7acb\u5373\u63d0\u4f9b\u697c\u680b\u6570\u636e\u3002\u8f85\u5bfc\u5458\u8def\u7531\u5df2100%\u8986\u76d6\u3002\u6b64\u95ee\u9898\u963b\u585ePhase 0\u9a8c\u8bc1\u901a\u8fc7\u53caPhase 1-5\u5b9e\u65bd\u3002", "task_id": "TASK-20260605-04", "artifacts": ["/home/caohui/projects/graduation-leave-system/.omc/collaboration/tasks/TASK-20260605-04-phase-0-p0\u963b\u585e\uff1a116\u4e2afile2\u72ec\u6709\u5b66\u751f\u7f3a\u5c11\u697c\u680b.md"], "status": "task_open"}
{"id": 8, "type": "task_created", "agent": "claude", "timestamp": "2026-06-06T10:08:47.638971+00:00", "summary": "Created task: \u6570\u636e\u9a8c\u8bc1\u5b8c\u6210\uff1a271\u540d\u7814\u7a76\u751f\u5b66\u53f7\u5df2\u627e\u5230\uff08100%\u5339\u914d\uff09\uff0c\u53d1\u73b019\u540d\u989d\u5916\u7814\u7a76\u751f\uff0c\u65b0\u589e3\u540d\u7ba1\u7406\u5458\uff08\u542b\u515c\u5e95\u5bbf\u7ba1\u5458\uff09\uff0c\u9700\u5ba1\u67e5\u5bf9Phase 2-3\u6267\u884c\u903b\u8f91\u7684\u5f71\u54cd\uff1a1)\u515c\u5e95\u5bbf\u7ba1\u5458\u8def\u7531\u5b9e\u73b0\u65b9\u6848\u9009\u62e9 2)271\u4eba\u5b66\u53f7\u66f4\u65b0\u7b56\u7565 3)19\u540d\u989d\u5916\u7814\u7a76\u751f\u5904\u7406\u65b9\u5f0f 4)Phase 3\u6570\u636e\u5bfc\u5165\u4efb\u52a1\u8c03\u6574", "task_id": "TASK-20260606-08", "artifacts": ["/home/caohui/projects/graduation-leave-system/.omc/collaboration/tasks/TASK-20260606-08-\u6570\u636e\u9a8c\u8bc1\u5b8c\u6210\uff1a271\u540d\u7814\u7a76\u751f\u5b66\u53f7\u5df2\u627e\u5230\uff08100%\u5339\u914d\uff09\uff0c\u53d1\u73b0.md"], "status": "task_open"}
{"id": 9, "type": "handoff_requested", "agent": "claude", "timestamp": "2026-06-06T10:10:03.804457+00:00", "summary": "handoff to codex for execution logic adjustment review", "task_id": "TASK-20260606-08", "status": "waiting"}
{"id": 10, "type": "task_claimed", "agent": "codex", "timestamp": "2026-06-06T10:16:51.870139+00:00", "task_id": "TASK-20260606-08", "summary": "Codex claimed Phase 0 execution logic adjustment review", "status": "in_progress"}
{"id": 11, "type": "artifact_created", "agent": "codex", "timestamp": "2026-06-06T10:20:50.992679+00:00", "task_id": "TASK-20260606-08", "summary": "Codex Phase 0 execution logic adjustment review artifact created", "artifacts": [".omc/collaboration/artifacts/20260606-1019-codex-phase0-execution-logic-review.md"], "status": "in_progress"}
{"id": 12, "type": "completed", "agent": "codex", "timestamp": "2026-06-06T10:20:50.992679+00:00", "task_id": "TASK-20260606-08", "summary": "Codex completed Phase 0 execution logic adjustment review", "artifacts": [".omc/collaboration/artifacts/20260606-1019-codex-phase0-execution-logic-review.md"], "status": "completed"}
{"id":13,"type":"task_claimed","agent":"codex","timestamp":"2026-06-06T15:47:41.175851+00:00","task_id":"TASK-20260606-09","summary":"Codex claimed Phase 3 data discrepancy review","status":"in_progress"}

diff --git a/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md b/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md
new file mode 100644
index 0000000000000000000000000000000000000000..f4f206976f9830a6f43ce74344fc1b89013d12c3
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md
@@ -0,0 +1,133 @@
+# Phase 3数据导入轻微差异 - Codex审查意见
+
+**任务ID:** TASK-20260606-09  
+**审查日期:** 2026-06-06  
+**审查人:** Codex  
+**审查范围:** Phase 3导入后用户数量差异、功能影响、生产导入策略、Phase 4阻塞判断
+
+## 审查结论
+
+14人差异本身不构成审批路由、权限控制或前端页面开发的直接阻塞；根因已可定位为历史测试/种子数据残留，且不是TMP ID问题。
+
+但当前环境存在两个比14人差异更实质的Phase 4联调阻塞：
+
+1. 当前数据库有1个非rejected申请，`import_students --mode clean` 会被安全检查拦截。
+2. 辅导员审批路由当前不可用：导入脚本未写入辅导员 `department`，当前22名辅导员 `department` 均为空；同时 `apps/approvals/views.py` 使用 `User.objects` 但未导入 `User`。
+
+因此：前端静态页面/接口契约开发不阻塞；完整端到端申请-宿管-辅导员审批联调在Phase 4前应先修正。
+
+## 证据摘要
+
+只读数据库比对结果：
+
+- 源数据并集：6041人，包含学生5946、宿管72、辅导员20、additional_staff 3。
+- 当前数据库：6056人；若排除既有 `dean` 角色，为6055人，与任务文档口径一致。
+- 分角色：学生5956、宿管75、辅导员22、admin 2、dean 1。
+- TMP ID：0。
+- 当前非rejected申请：1个，`app_4ae6dd14 / 2020001 / approved`。
+
+差异身份：
+
+- 额外学生10人：`2020001` 到 `2020010`，均为测试学生。
+- 额外宿管2人：`M001`、`M002`，均为测试宿管。
+- 额外辅导员2人：`T001`、`T002`，均为测试辅导员。
+
+相关代码依据：
+
+- `import_students --mode clean` 在存在非rejected申请时拒绝执行：`apps/users/management/commands/import_students.py:31`。
+- `clean` 只删除 `role=student` 用户，不清理宿管/辅导员/admin：`apps/users/management/commands/import_students.py:62`。
+- `import_staff` 当前只读取 `phone/building`，没有读取或写入 `department`：`apps/users/management/commands/import_staff.py:62`。
+- 学生提交申请时宿管按 `building` 查找，找不到走兜底：`apps/applications/views.py:151`。
+- 宿管通过后辅导员按学生 `department` 精确查找：`apps/approvals/views.py:163`。
+- `apps/approvals/views.py` 只导入 `UserRole`，未导入 `User`，但后续使用 `User.objects`：`apps/approvals/views.py:14`。
+
+## 影响评估
+
+### 功能影响
+
+14个历史测试账号对主流程没有直接破坏性影响：
+
+- 宿管路由基于学生 `building`，并且有兜底宿管；额外测试宿管 `M001/M002` 的 `building` 为空，不会按楼栋承接真实学生。
+- 权限控制基于 `role` 和当前登录用户，额外账号不会提升真实用户权限。
+- 额外测试学生不会影响真实学生提交申请，除非被用于登录和操作。
+
+但会造成环境数据污染：
+
+- 用户统计、覆盖率、角色人数会偏离源数据口径。
+- `2020001` 已有关联approved申请，会阻塞 `clean` 导入。
+- 测试账号如保留在生产，会带来审计、误登录和数据可信度风险。
+
+### 数据一致性影响
+
+当前差异不影响“TMP清零”和“兜底宿管存在”这两个硬指标，但会降低验收口径的可解释性。生产验收不应接受“已知测试账号残留”的用户基线。
+
+辅导员 `department` 缺失是独立的一致性问题，影响实际审批流，不应被14人差异掩盖。
+
+### 性能影响
+
+14条额外用户记录对性能无实际影响。
+
+## 根因调查建议
+
+不需要继续做大范围根因调查；当前已足够定位：
+
+- 10个学生、2个宿管、2个辅导员均符合项目测试/种子数据命名模式。
+- 创建时间集中在2026-06-03，早于Phase 3导入。
+- 源数据对比没有缺失主批次用户。
+
+建议保留一次性审计记录即可：列出额外账号、关联申请、清理方式和清理时间。
+
+## 生产导入策略推荐
+
+推荐：生产使用 clean/rebuild 基线，不使用 append 作为首次上线导入策略。
+
+具体建议：
+
+1. 新生产库优先从空库迁移后导入。保留必要系统账号或超级管理员，批量导入学生、宿管、辅导员、学工管理员、兜底宿管。
+2. 如果不是空库，先确认没有有效业务申请；否则不得直接删除学生。
+3. 不建议只运行现有 `import_students --mode clean` 后继续 append staff，因为该命令只清学生，无法清掉 `M001/M002/T001/T002` 这类历史 staff。
+4. 对当前开发/测试库，建议手动清理已知测试账号及其测试申请，或重建库；清理后重新执行 dry-run 和正式导入。
+5. append 模式仅适合后续增量补录，前提是输入文件经过白名单比对，且导入后运行“DB用户集合 - 源数据集合 = 0”的校验。
+
+不推荐方案A append：会保留污染数据，生产验收口径不干净。
+
+不推荐单纯方案C手动清理作为生产主策略：适合修复当前环境，不适合作为可复现上线流程。
+
+## 19名额外研究生处理建议
+
+建议暂不纳入主批次，不阻塞Phase 4。
+
+理由：
+
+- 这19人不在File1/File2/File5主批次。
+- 学号特征为2021/2022/2023，不足以证明属于2026届主批次。
+- 当前缺少学院/班级/楼栋/辅导员映射等路由关键字段。
+
+处理优先级：Phase 3.5补充批次，等待业务确认。确认属于2026届后，再按补充批次导入，并明确无楼栋是否走兜底宿管、学院如何映射辅导员。
+
+## Phase 4阻塞判断
+
+不阻塞：
+
+- 前端页面开发。
+- 登录、列表、表单、状态展示等基于现有API契约的开发。
+- 使用mock或固定测试账号做非端到端页面验收。
+
+阻塞：
+
+- 真实数据端到端联调。
+- 宿管通过后创建辅导员审批。
+- 生产导入验收。
+
+Phase 4前建议先完成以下P0/P1：
+
+- P0：修复 `apps/approvals/views.py` 缺少 `User` 导入。
+- P0：补齐辅导员 `department` 导入字段，或调整路由模型为明确的学院-辅导员映射。
+- P1：清理当前环境测试账号 `2020001-2020010/M001/M002/T001/T002` 及测试申请，或重建库。
+- P1：为生产导入增加导后校验脚本，至少校验角色人数、源数据缺失、DB额外用户、TMP ID、兜底宿管、学生无楼栋数量、辅导员department覆盖。
+
+## 最终建议
+
+接受Phase 3“主批次数据已导入、TMP已清零、兜底宿管已就位”的阶段性结论，但不要把当前数据库作为生产基线。
+
+生产上线采用可复现的clean/rebuild导入；19名额外研究生进入Phase 3.5待业务确认；Phase 4页面开发可以继续，但端到端审批联调前必须修正辅导员路由字段和 `User` 导入问题。

exec
/bin/bash -lc "rtk ./venv/bin/python - <<'PY'
import json, os, shutil
from pathlib import Path
from datetime import datetime, timezone
base = Path('../.omc/collaboration')
lock = base / 'locks' / 'journal.lock'
task_id = 'TASK-20260606-09'
artifact = '.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md'
now = datetime.now(timezone.utc).isoformat()
os.mkdir(lock)
try:
    (lock / 'owner.json').write_text(json.dumps({
        'agent': 'codex', 'task_id': task_id, 'created_at': now,
        'heartbeat_at': now, 'reason': 'record Phase 3 data discrepancy review completion'
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    events_path = base / 'events.jsonl'
    events = []
    with events_path.open(encoding='utf-8') as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    ids = [e['id'] for e in events]
    if len(ids) "'!= len(set(ids)):
        raise RuntimeError('"'duplicate event ids')
    next_id = max(ids, default=0) + 1
    new_events = [
        {
            'id': next_id,
            'type': 'artifact_created',
            'agent': 'codex',
            'timestamp': now,
            'task_id': task_id,
            'summary': 'Codex Phase 3 data discrepancy review artifact created',
            'artifacts': [artifact],
            'status': 'in_progress'
        },
        {
            'id': next_id + 1,
            'type': 'completed',
            'agent': 'codex',
            'timestamp': now,
            'task_id': task_id,
            'summary': 'Codex completed Phase 3 data discrepancy review',
            'artifacts': [artifact],
            'status': 'completed'
        }
    ]
    with events_path.open('a', encoding='utf-8') as f:
        for event in new_events:
            f.write(json.dumps(event, ensure_ascii=False, separators=(',', ':')) + '\\n')
    state = {
        'workflow_id': 'implementation-plan-review',
        'current_task': task_id,
        'active_agent': 'none',
        'status': 'completed',
        'last_event_id': next_id + 1,
        'updated_at': now
    }
    tmp = base / 'state.json.tmp.codex'
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\\n', encoding='utf-8')
    json.loads(tmp.read_text(encoding='utf-8'))
    os.replace(tmp, base / 'state.json')
finally:
    shutil.rmtree(lock)
PY" in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
diff --git a/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md b/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md
new file mode 100644
index 0000000000000000000000000000000000000000..f4f206976f9830a6f43ce74344fc1b89013d12c3
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md
@@ -0,0 +1,133 @@
+# Phase 3数据导入轻微差异 - Codex审查意见
+
+**任务ID:** TASK-20260606-09  
+**审查日期:** 2026-06-06  
+**审查人:** Codex  
+**审查范围:** Phase 3导入后用户数量差异、功能影响、生产导入策略、Phase 4阻塞判断
+
+## 审查结论
+
+14人差异本身不构成审批路由、权限控制或前端页面开发的直接阻塞；根因已可定位为历史测试/种子数据残留，且不是TMP ID问题。
+
+但当前环境存在两个比14人差异更实质的Phase 4联调阻塞：
+
+1. 当前数据库有1个非rejected申请，`import_students --mode clean` 会被安全检查拦截。
+2. 辅导员审批路由当前不可用：导入脚本未写入辅导员 `department`，当前22名辅导员 `department` 均为空；同时 `apps/approvals/views.py` 使用 `User.objects` 但未导入 `User`。
+
+因此：前端静态页面/接口契约开发不阻塞；完整端到端申请-宿管-辅导员审批联调在Phase 4前应先修正。
+
+## 证据摘要
+
+只读数据库比对结果：
+
+- 源数据并集：6041人，包含学生5946、宿管72、辅导员20、additional_staff 3。
+- 当前数据库：6056人；若排除既有 `dean` 角色，为6055人，与任务文档口径一致。
+- 分角色：学生5956、宿管75、辅导员22、admin 2、dean 1。
+- TMP ID：0。
+- 当前非rejected申请：1个，`app_4ae6dd14 / 2020001 / approved`。
+
+差异身份：
+
+- 额外学生10人：`2020001` 到 `2020010`，均为测试学生。
+- 额外宿管2人：`M001`、`M002`，均为测试宿管。
+- 额外辅导员2人：`T001`、`T002`，均为测试辅导员。
+
+相关代码依据：
+
+- `import_students --mode clean` 在存在非rejected申请时拒绝执行：`apps/users/management/commands/import_students.py:31`。
+- `clean` 只删除 `role=student` 用户，不清理宿管/辅导员/admin：`apps/users/management/commands/import_students.py:62`。
+- `import_staff` 当前只读取 `phone/building`，没有读取或写入 `department`：`apps/users/management/commands/import_staff.py:62`。
+- 学生提交申请时宿管按 `building` 查找，找不到走兜底：`apps/applications/views.py:151`。
+- 宿管通过后辅导员按学生 `department` 精确查找：`apps/approvals/views.py:163`。
+- `apps/approvals/views.py` 只导入 `UserRole`，未导入 `User`，但后续使用 `User.objects`：`apps/approvals/views.py:14`。
+
+## 影响评估
+
+### 功能影响
+
+14个历史测试账号对主流程没有直接破坏性影响：
+
+- 宿管路由基于学生 `building`，并且有兜底宿管；额外测试宿管 `M001/M002` 的 `building` 为空，不会按楼栋承接真实学生。
+- 权限控制基于 `role` 和当前登录用户，额外账号不会提升真实用户权限。
+- 额外测试学生不会影响真实学生提交申请，除非被用于登录和操作。
+
+但会造成环境数据污染：
+
+- 用户统计、覆盖率、角色人数会偏离源数据口径。
+- `2020001` 已有关联approved申请，会阻塞 `clean` 导入。
+- 测试账号如保留在生产，会带来审计、误登录和数据可信度风险。
+
+### 数据一致性影响
+
+当前差异不影响“TMP清零”和“兜底宿管存在”这两个硬指标，但会降低验收口径的可解释性。生产验收不应接受“已知测试账号残留”的用户基线。
+
+辅导员 `department` 缺失是独立的一致性问题，影响实际审批流，不应被14人差异掩盖。
+
+### 性能影响
+
+14条额外用户记录对性能无实际影响。
+
+## 根因调查建议
+
+不需要继续做大范围根因调查；当前已足够定位：
+
+- 10个学生、2个宿管、2个辅导员均符合项目测试/种子数据命名模式。
+- 创建时间集中在2026-06-03，早于Phase 3导入。
+- 源数据对比没有缺失主批次用户。
+
+建议保留一次性审计记录即可：列出额外账号、关联申请、清理方式和清理时间。
+
+## 生产导入策略推荐
+
+推荐：生产使用 clean/rebuild 基线，不使用 append 作为首次上线导入策略。
+
+具体建议：
+
+1. 新生产库优先从空库迁移后导入。保留必要系统账号或超级管理员，批量导入学生、宿管、辅导员、学工管理员、兜底宿管。
+2. 如果不是空库，先确认没有有效业务申请；否则不得直接删除学生。
+3. 不建议只运行现有 `import_students --mode clean` 后继续 append staff，因为该命令只清学生，无法清掉 `M001/M002/T001/T002` 这类历史 staff。
+4. 对当前开发/测试库，建议手动清理已知测试账号及其测试申请，或重建库；清理后重新执行 dry-run 和正式导入。
+5. append 模式仅适合后续增量补录，前提是输入文件经过白名单比对，且导入后运行“DB用户集合 - 源数据集合 = 0”的校验。
+
+不推荐方案A append：会保留污染数据，生产验收口径不干净。
+
+不推荐单纯方案C手动清理作为生产主策略：适合修复当前环境，不适合作为可复现上线流程。
+
+## 19名额外研究生处理建议
+
+建议暂不纳入主批次，不阻塞Phase 4。
+
+理由：
+
+- 这19人不在File1/File2/File5主批次。
+- 学号特征为2021/2022/2023，不足以证明属于2026届主批次。
+- 当前缺少学院/班级/楼栋/辅导员映射等路由关键字段。
+
+处理优先级：Phase 3.5补充批次，等待业务确认。确认属于2026届后，再按补充批次导入，并明确无楼栋是否走兜底宿管、学院如何映射辅导员。
+
+## Phase 4阻塞判断
+
+不阻塞：
+
+- 前端页面开发。
+- 登录、列表、表单、状态展示等基于现有API契约的开发。
+- 使用mock或固定测试账号做非端到端页面验收。
+
+阻塞：
+
+- 真实数据端到端联调。
+- 宿管通过后创建辅导员审批。
+- 生产导入验收。
+
+Phase 4前建议先完成以下P0/P1：
+
+- P0：修复 `apps/approvals/views.py` 缺少 `User` 导入。
+- P0：补齐辅导员 `department` 导入字段，或调整路由模型为明确的学院-辅导员映射。
+- P1：清理当前环境测试账号 `2020001-2020010/M001/M002/T001/T002` 及测试申请，或重建库。
+- P1：为生产导入增加导后校验脚本，至少校验角色人数、源数据缺失、DB额外用户、TMP ID、兜底宿管、学生无楼栋数量、辅导员department覆盖。
+
+## 最终建议
+
+接受Phase 3“主批次数据已导入、TMP已清零、兜底宿管已就位”的阶段性结论，但不要把当前数据库作为生产基线。
+
+生产上线采用可复现的clean/rebuild导入；19名额外研究生进入Phase 3.5待业务确认；Phase 4页面开发可以继续，但端到端审批联调前必须修正辅导员路由字段和 `User` 导入问题。

codex
协作完成事件已写入。我会最后核对状态文件和事件尾部，确认日志一致。
exec
/bin/bash -lc 'rtk cat ../.omc/collaboration/state.json' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
{
  "workflow_id": "implementation-plan-review",
  "current_task": "TASK-20260606-09",
  "active_agent": "none",
  "status": "completed",
  "last_event_id": 15,
  "updated_at": "2026-06-06T15:49:30.744215+00:00"
}

exec
/bin/bash -lc 'rtk tail -n 6 ../.omc/collaboration/events.jsonl' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
{"id": 10, "type": "task_claimed", "agent": "codex", "timestamp": "2026-06-06T10:16:51.870139+00:00", "task_id": "TASK-20260606-08", "summary": "Codex claimed Phase 0 execution logic adjustment review", "status": "in_progress"}
{"id": 11, "type": "artifact_created", "agent": "codex", "timestamp": "2026-06-06T10:20:50.992679+00:00", "task_id": "TASK-20260606-08", "summary": "Codex Phase 0 execution logic adjustment review artifact created", "artifacts": [".omc/collaboration/artifacts/20260606-1019-codex-phase0-execution-logic-review.md"], "status": "in_progress"}
{"id": 12, "type": "completed", "agent": "codex", "timestamp": "2026-06-06T10:20:50.992679+00:00", "task_id": "TASK-20260606-08", "summary": "Codex completed Phase 0 execution logic adjustment review", "artifacts": [".omc/collaboration/artifacts/20260606-1019-codex-phase0-execution-logic-review.md"], "status": "completed"}
{"id":13,"type":"task_claimed","agent":"codex","timestamp":"2026-06-06T15:47:41.175851+00:00","task_id":"TASK-20260606-09","summary":"Codex claimed Phase 3 data discrepancy review","status":"in_progress"}
{"id":14,"type":"artifact_created","agent":"codex","timestamp":"2026-06-06T15:49:30.744215+00:00","task_id":"TASK-20260606-09","summary":"Codex Phase 3 data discrepancy review artifact created","artifacts":[".omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md"],"status":"in_progress"}
{"id":15,"type":"completed","agent":"codex","timestamp":"2026-06-06T15:49:30.744215+00:00","task_id":"TASK-20260606-09","summary":"Codex completed Phase 3 data discrepancy review","artifacts":[".omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md"],"status":"completed"}

exec
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system/backend
 succeeded in 0ms:
 M ../.omc/collaboration/events.jsonl
 M ../.omc/collaboration/state.json
 M ../.omc/session-context.json
 M ../.omc/state/hud-stdin-cache.json
 M apps/applications/permissions.py
 M apps/applications/providers.py
 M apps/applications/tests/test_constraints.py
 M apps/applications/tests/test_detail_permissions.py
 M apps/applications/tests/test_error_cases.py
 M apps/applications/tests/test_list_permissions.py
 M apps/approvals/tests/test_list_permissions.py
 M apps/approvals/tests/test_permissions.py
 M apps/approvals/tests/test_rejection_flow.py
 M apps/attachments/tests/test_list.py
 M apps/notifications/services.py
 M apps/notifications/tests/test_auto_notifications.py
 M apps/users/integrations/xg_user_client.py
 M apps/users/management/commands/seed_data.py
 M apps/users/tests/test_xg_user_client.py
 M scripts/merge_student_data.py
 M scripts/normalize_colleges.py
 M ../docs/api/notification-contract-v0.1.md
 M ../frontend/services/api.ts
 M ../frontend/services/mock.ts
 M ../frontend/types/api.ts
 M ../tests/test_p0_fixes.sh
?? ../.claude/scheduled_tasks.json
?? ../.omc/artifacts/ask/codex-docs-md-omc-collaboration-tasks-task-20260605-03-implementat-2026-06-05T05-14-23-458Z.md
?? ../.omc/artifacts/ask/codex-omc-collaboration-tasks-task-20260605-01-excel-association-r-2026-06-05T00-55-29-654Z.md
?? ../.omc/artifacts/ask/codex-phase-0-omc-collaboration-tasks-task-20260606-08-md-1-b-2-27-2026-06-06T10-21-25-940Z.md
?? ../.omc/artifacts/ask/codex-phase-0-p0-omc-collaboration-artifacts-20260605-phase0-routi-2026-06-05T20-00-13-603Z.md
?? ../.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md
?? "../.omc/collaboration/tasks/TASK-20260606-08-\345\256\241\346\237\245\350\257\267\346\261\202.md"
?? "../.omc/collaboration/tasks/TASK-20260606-08-\346\225\260\346\215\256\351\252\214\350\257\201\345\256\214\346\210\220\357\274\232271\345\220\215\347\240\224\347\251\266\347\224\237\345\255\246\345\217\267\345\267\262\346\211\276\345\210\260\357\274\210100%\345\214\271\351\205\215\357\274\211\357\274\214\345\217\221\347\216\260.md"
?? "../.omc/collaboration/tasks/TASK-20260606-09-Phase3\346\225\260\346\215\256\345\257\274\345\205\245\345\256\214\346\210\220-\350\275\273\345\276\256\345\267\256\345\274\202\345\256\241\346\237\245.md"
?? ../.omc/project-memory.json
?? ../.omc/sessions/
?? ../.omc/state/agent-replay-f5a217eb-15dd-46c8-bdf3-d9e12d88125b.jsonl
?? ../.omc/state/checkpoints/
?? ../.omc/state/last-tool-error.json
?? ../.omc/state/mission-state.json
?? ../.omc/state/sessions/1975d66f-d9f9-404a-aee5-c702658630c2/
?? ../.omc/state/sessions/4aad264e-c3a4-460a-9be1-61247202bad3/
?? ../.omc/state/sessions/7afec07d-3b40-4e4c-8f86-86e9dc0e791c/
?? ../.omc/state/sessions/83935a94-dc9d-4f47-83f5-bad88cc99fad/
?? ../.omc/state/sessions/97c93024-a4c1-4e03-93bf-7522ce3517ff/
?? ../.omc/state/sessions/9bdcb1fe-5a48-4133-8a75-ba525f0229cb/
?? ../.omc/state/sessions/c8f47bca-464c-4b8c-bab5-42ba59354101/
?? ../.omc/state/sessions/dcf39a3e-1b72-449a-9897-852c3c7f1253/
?? ../.omc/state/sessions/e2566739-aaa7-4701-9354-a710639ac308/
?? ../.omc/state/sessions/f5a217eb-15dd-46c8-bdf3-d9e12d88125b/
?? ../.omc/state/sessions/f91e1567-b1b2-4cc2-bd9b-355702bc1ec4/
?? ../.omc/state/subagent-tracking.json
?? ../.planning/
?? .omc/artifacts/
?? .omc/state/
?? app
?? apps/notifications/management/commands/send_approval_timeout_warnings.py
?? apps/notifications/tests/test_timeout_warnings.py
?? apps/users/migrations/0002_user_department_user_email_user_phone.py
?? config/settings/test.py
?? "data/1-5830\345\220\215\346\257\225\344\270\232\347\224\237\357\274\210\345\220\253\347\240\224\347\251\266\347\224\237\357\274\211.csv"
?? "data/2026\345\261\212\351\242\204\350\256\241\346\257\225\344\270\232\347\224\2375675\344\272\272.csv"
?? "data/2026\345\271\264\345\255\246\351\231\242\350\276\205\345\257\274\345\221\230\344\277\241\346\201\257\347\273\237\350\256\241\350\241\250.csv"
?? "data/2026\345\271\264\347\244\276\345\214\272\350\276\205\345\257\274\345\221\230\344\277\241\346\201\257\347\273\237\350\256\241\350\241\250.csv"
?? data/file5_students_merged.csv
?? data/merge_report.json
?? data/routing_coverage_report.json
?? docs/
?? reports/
?? requirements.txt
?? "../docs/1-5830\345\220\215\346\257\225\344\270\232\347\224\237\357\274\210\345\220\253\347\240\224\347\251\266\347\224\237\357\274\211.xls"
?? "../docs/1-\346\227\240\345\205\245\344\275\217\344\277\241\346\201\257.xls"
?? "../docs/20260606-\346\257\225\344\270\232\347\224\237\345\205\245\344\275\217\345\237\272\346\234\254\344\277\241\346\201\257.xls"
?? "../docs/2026\345\261\212\351\242\204\350\256\241\346\257\225\344\270\232\347\224\2375675\344\272\272.xlsx"
?? "../docs/2026\345\271\264\345\255\246\351\231\242\350\276\205\345\257\274\345\221\230\344\277\241\346\201\257\347\273\237\350\256\241\350\241\250.xls"
?? "../docs/2026\345\271\264\347\244\276\345\214\272\350\276\205\345\257\274\345\221\230\344\277\241\346\201\257\347\273\237\350\256\241\350\241\250.xls"
?? "../docs/Excel\346\225\260\346\215\256\346\272\220\345\210\206\346\236\220\344\270\216\351\234\200\346\261\202\345\257\271\346\257\224.md"
?? "../docs/api\350\257\264\346\230\216.txt"
?? ../docs/contracts/contract-v0.2.md
?? ../docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md
?? ../docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md
?? ../docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md
?? ../docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md
?? ../docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md
?? ../docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md
?? ../docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md
?? ../docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md
?? ../docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md
?? ../docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md
?? ../docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md
?? ../docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md
?? ../docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md
?? ../docs/discussions/codex-review-2026-05-27/21-final-consensus.md
?? ../docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md
?? ../docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
?? ../docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md
?? ../docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
?? ../docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md
?? ../docs/discussions/codex-review-2026-05-27/34-implementation-order-challenge.md
?? ../docs/discussions/codex-review-2026-05-27/35-claude-response-implementation-strategy.md
?? ../docs/discussions/codex-review-2026-05-27/36-claude-response-phase4b-review.md
?? ../docs/discussions/codex-review-2026-05-27/37-phase4b-fix-consensus.md
?? ../docs/discussions/codex-review-2026-05-30/49-contract-fixes-codex-response.md
?? ../docs/discussions/phase4c-next-steps/102-implementation-review-and-test-codex-response.md
?? ../docs/discussions/phase4c-next-steps/103-step4a-implementation-final-codex-response.md
?? ../docs/discussions/phase4c-next-steps/106-step4b-model-extension-strategy-codex-response.md
?? ../docs/discussions/phase4c-next-steps/107-claude-response-agree-step4b.md
?? ../docs/discussions/phase4c-next-steps/108-step4b-strategy-final-consensus.md
?? ../docs/discussions/week3-day1-review-2026-05-30/01-codex-review.md
?? ../docs/discussions/week3-day1-review-2026-05-30/02-claude-response.md
?? ../docs/discussions/week3-day1-review-2026-05-30/03-day2-plan-review-request.md
?? ../docs/discussions/week3-day1-review-2026-05-30/04-codex-day2-plan-review.md
?? ../docs/discussions/week3-day1-review-2026-05-30/05-claude-response-to-codex-review.md
?? ../docs/discussions/week3-day1-review-2026-05-30/06-codex-counter-response.md
?? ../docs/discussions/week3-day1-review-2026-05-30/08-claude-day2-execution-proposal.md
?? ../docs/discussions/week3-day1-review-2026-05-30/09-codex-day2-execution-review.md
?? ../docs/discussions/week3-day1-review-2026-05-30/09-codex-execution-review.md
?? ../docs/discussions/week3-day1-review-2026-05-30/10-claude-response-to-codex-execution-review.md
?? ../docs/discussions/week3-day1-review-2026-05-30/11-codex-response-to-claude-execution-review.md
?? ../docs/discussions/week3-day1-review-2026-05-30/13-claude-day2-launch-proposal.md
?? ../docs/discussions/week3-day1-review-2026-05-30/14-codex-day2-launch-review.md
?? ../docs/discussions/week3-day1-review-2026-05-30/15-claude-authorization-question.md
?? ../docs/discussions/week3-day1-review-2026-05-30/16-codex-authorization-ruling.md
?? ../docs/discussions/week3-day1-review-2026-05-30/17-claude-next-steps-analysis.md
?? ../docs/discussions/week3-day1-review-2026-05-30/18-codex-next-steps-review.md
?? ../docs/discussions/week3-day1-review-2026-05-30/19-claude-deadlock-analysis.md
?? ../docs/discussions/week3-day1-review-2026-05-30/20-codex-deadlock-ruling.md
?? ../docs/discussions/week3-day3-planning-2026-05-30/07-claude-phase1-proposal.md
?? ../docs/discussions/week3-day3-planning-2026-05-30/08-claude-phase1-revised.md
?? ../docs/discussions/week3-day3-planning-2026-05-30/09-phase1-final-consensus.md
?? ../docs/discussions/week3-day3-planning-2026-05-30/10-claude-response-step2-review.md
?? ../docs/discussions/week3-day3-planning-2026-05-30/11-codex-step2-final-review.md
?? ../docs/project-completion-status-2026-06-02.md
?? "../docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260528210617_553_47.jpg"
?? "../docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260528210618_554_47.jpg"
?? "../docs/\345\276\256\344\277\241\345\233\276\347\211\207_20260528210619_555_47.jpg"
?? "../docs/\346\226\260\345\242\236\345\256\241\346\240\270\344\272\272\345\221\230.txt"
?? "../docs/\347\241\225\345\243\253\347\240\224\347\251\266\347\224\237-\346\257\225\344\270\232\347\224\237290\344\272\272.xls"
?? ../findings.md
?? ../miniprogram/.omc/
?? ../progress.md
?? ../scripts/
?? ../task_plan.md
?? "../\346\257\225\344\270\232\347\246\273\346\240\241\347\263\273\347\273\237\347\224\250\346\210\267\346\226\207\346\241\243.zip"
diff --git a/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md b/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md
new file mode 100644
index 0000000000000000000000000000000000000000..f4f206976f9830a6f43ce74344fc1b89013d12c3
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md
@@ -0,0 +1,133 @@
+# Phase 3数据导入轻微差异 - Codex审查意见
+
+**任务ID:** TASK-20260606-09  
+**审查日期:** 2026-06-06  
+**审查人:** Codex  
+**审查范围:** Phase 3导入后用户数量差异、功能影响、生产导入策略、Phase 4阻塞判断
+
+## 审查结论
+
+14人差异本身不构成审批路由、权限控制或前端页面开发的直接阻塞；根因已可定位为历史测试/种子数据残留，且不是TMP ID问题。
+
+但当前环境存在两个比14人差异更实质的Phase 4联调阻塞：
+
+1. 当前数据库有1个非rejected申请，`import_students --mode clean` 会被安全检查拦截。
+2. 辅导员审批路由当前不可用：导入脚本未写入辅导员 `department`，当前22名辅导员 `department` 均为空；同时 `apps/approvals/views.py` 使用 `User.objects` 但未导入 `User`。
+
+因此：前端静态页面/接口契约开发不阻塞；完整端到端申请-宿管-辅导员审批联调在Phase 4前应先修正。
+
+## 证据摘要
+
+只读数据库比对结果：
+
+- 源数据并集：6041人，包含学生5946、宿管72、辅导员20、additional_staff 3。
+- 当前数据库：6056人；若排除既有 `dean` 角色，为6055人，与任务文档口径一致。
+- 分角色：学生5956、宿管75、辅导员22、admin 2、dean 1。
+- TMP ID：0。
+- 当前非rejected申请：1个，`app_4ae6dd14 / 2020001 / approved`。
+
+差异身份：
+
+- 额外学生10人：`2020001` 到 `2020010`，均为测试学生。
+- 额外宿管2人：`M001`、`M002`，均为测试宿管。
+- 额外辅导员2人：`T001`、`T002`，均为测试辅导员。
+
+相关代码依据：
+
+- `import_students --mode clean` 在存在非rejected申请时拒绝执行：`apps/users/management/commands/import_students.py:31`。
+- `clean` 只删除 `role=student` 用户，不清理宿管/辅导员/admin：`apps/users/management/commands/import_students.py:62`。
+- `import_staff` 当前只读取 `phone/building`，没有读取或写入 `department`：`apps/users/management/commands/import_staff.py:62`。
+- 学生提交申请时宿管按 `building` 查找，找不到走兜底：`apps/applications/views.py:151`。
+- 宿管通过后辅导员按学生 `department` 精确查找：`apps/approvals/views.py:163`。
+- `apps/approvals/views.py` 只导入 `UserRole`，未导入 `User`，但后续使用 `User.objects`：`apps/approvals/views.py:14`。
+
+## 影响评估
+
+### 功能影响
+
+14个历史测试账号对主流程没有直接破坏性影响：
+
+- 宿管路由基于学生 `building`，并且有兜底宿管；额外测试宿管 `M001/M002` 的 `building` 为空，不会按楼栋承接真实学生。
+- 权限控制基于 `role` 和当前登录用户，额外账号不会提升真实用户权限。
+- 额外测试学生不会影响真实学生提交申请，除非被用于登录和操作。
+
+但会造成环境数据污染：
+
+- 用户统计、覆盖率、角色人数会偏离源数据口径。
+- `2020001` 已有关联approved申请，会阻塞 `clean` 导入。
+- 测试账号如保留在生产，会带来审计、误登录和数据可信度风险。
+
+### 数据一致性影响
+
+当前差异不影响“TMP清零”和“兜底宿管存在”这两个硬指标，但会降低验收口径的可解释性。生产验收不应接受“已知测试账号残留”的用户基线。
+
+辅导员 `department` 缺失是独立的一致性问题，影响实际审批流，不应被14人差异掩盖。
+
+### 性能影响
+
+14条额外用户记录对性能无实际影响。
+
+## 根因调查建议
+
+不需要继续做大范围根因调查；当前已足够定位：
+
+- 10个学生、2个宿管、2个辅导员均符合项目测试/种子数据命名模式。
+- 创建时间集中在2026-06-03，早于Phase 3导入。
+- 源数据对比没有缺失主批次用户。
+
+建议保留一次性审计记录即可：列出额外账号、关联申请、清理方式和清理时间。
+
+## 生产导入策略推荐
+
+推荐：生产使用 clean/rebuild 基线，不使用 append 作为首次上线导入策略。
+
+具体建议：
+
+1. 新生产库优先从空库迁移后导入。保留必要系统账号或超级管理员，批量导入学生、宿管、辅导员、学工管理员、兜底宿管。
+2. 如果不是空库，先确认没有有效业务申请；否则不得直接删除学生。
+3. 不建议只运行现有 `import_students --mode clean` 后继续 append staff，因为该命令只清学生，无法清掉 `M001/M002/T001/T002` 这类历史 staff。
+4. 对当前开发/测试库，建议手动清理已知测试账号及其测试申请，或重建库；清理后重新执行 dry-run 和正式导入。
+5. append 模式仅适合后续增量补录，前提是输入文件经过白名单比对，且导入后运行“DB用户集合 - 源数据集合 = 0”的校验。
+
+不推荐方案A append：会保留污染数据，生产验收口径不干净。
+
+不推荐单纯方案C手动清理作为生产主策略：适合修复当前环境，不适合作为可复现上线流程。
+
+## 19名额外研究生处理建议
+
+建议暂不纳入主批次，不阻塞Phase 4。
+
+理由：
+
+- 这19人不在File1/File2/File5主批次。
+- 学号特征为2021/2022/2023，不足以证明属于2026届主批次。
+- 当前缺少学院/班级/楼栋/辅导员映射等路由关键字段。
+
+处理优先级：Phase 3.5补充批次，等待业务确认。确认属于2026届后，再按补充批次导入，并明确无楼栋是否走兜底宿管、学院如何映射辅导员。
+
+## Phase 4阻塞判断
+
+不阻塞：
+
+- 前端页面开发。
+- 登录、列表、表单、状态展示等基于现有API契约的开发。
+- 使用mock或固定测试账号做非端到端页面验收。
+
+阻塞：
+
+- 真实数据端到端联调。
+- 宿管通过后创建辅导员审批。
+- 生产导入验收。
+
+Phase 4前建议先完成以下P0/P1：
+
+- P0：修复 `apps/approvals/views.py` 缺少 `User` 导入。
+- P0：补齐辅导员 `department` 导入字段，或调整路由模型为明确的学院-辅导员映射。
+- P1：清理当前环境测试账号 `2020001-2020010/M001/M002/T001/T002` 及测试申请，或重建库。
+- P1：为生产导入增加导后校验脚本，至少校验角色人数、源数据缺失、DB额外用户、TMP ID、兜底宿管、学生无楼栋数量、辅导员department覆盖。
+
+## 最终建议
+
+接受Phase 3“主批次数据已导入、TMP已清零、兜底宿管已就位”的阶段性结论，但不要把当前数据库作为生产基线。
+
+生产上线采用可复现的clean/rebuild导入；19名额外研究生进入Phase 3.5待业务确认；Phase 4页面开发可以继续，但端到端审批联调前必须修正辅导员路由字段和 `User` 导入问题。

codex
已完成审查，并写入 artifact：

[20260606-1548-codex-phase3-data-discrepancy-review.md](/home/caohui/projects/graduation-leave-system/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md)

核心结论：

- 14人差异本身不阻塞系统功能，已基本确认是历史测试/种子数据残留：
  - 学生：`2020001`-`2020010`
  - 宿管：`M001/M002`
  - 辅导员：`T001/T002`
- 不建议继续大范围根因调查；当前证据足够，保留一次性审计记录即可。
- 生产首次导入推荐 `clean/rebuild` 基线，不推荐 `append`。现有 `import_students --mode clean` 只清学生，不能清理残留 staff，因此生产最好空库迁移后导入，或先显式清理目标角色数据。
- 19名额外研究生暂不纳入主批次，作为 Phase 3.5 等业务确认后补充处理。
- Phase 4 页面开发不阻塞；但真实端到端联调阻塞。

额外发现两个更重要的 Phase 4 联调风险：

- 当前库有1个非 `rejected` 申请，会阻止 `import_students --mode clean`。
- 辅导员路由当前不可用：22名辅导员 `department` 均为空，且 [apps/approvals/views.py](/home/caohui/projects/graduation-leave-system/backend/apps/approvals/views.py:14) 未导入 `User` 但后面使用了 `User.objects`。

协作日志已更新到 `TASK-20260606-09` completed，`state.json.last_event_id=15`。未修改业务代码；只写入审查 artifact 和协作事件/state。
diff --git a/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md b/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md
new file mode 100644
index 0000000000000000000000000000000000000000..f4f206976f9830a6f43ce74344fc1b89013d12c3
--- /dev/null
+++ b/.omc/collaboration/artifacts/20260606-1548-codex-phase3-data-discrepancy-review.md
@@ -0,0 +1,133 @@
+# Phase 3数据导入轻微差异 - Codex审查意见
+
+**任务ID:** TASK-20260606-09  
+**审查日期:** 2026-06-06  
+**审查人:** Codex  
+**审查范围:** Phase 3导入后用户数量差异、功能影响、生产导入策略、Phase 4阻塞判断
+
+## 审查结论
+
+14人差异本身不构成审批路由、权限控制或前端页面开发的直接阻塞；根因已可定位为历史测试/种子数据残留，且不是TMP ID问题。
+
+但当前环境存在两个比14人差异更实质的Phase 4联调阻塞：
+
+1. 当前数据库有1个非rejected申请，`import_students --mode clean` 会被安全检查拦截。
+2. 辅导员审批路由当前不可用：导入脚本未写入辅导员 `department`，当前22名辅导员 `department` 均为空；同时 `apps/approvals/views.py` 使用 `User.objects` 但未导入 `User`。
+
+因此：前端静态页面/接口契约开发不阻塞；完整端到端申请-宿管-辅导员审批联调在Phase 4前应先修正。
+
+## 证据摘要
+
+只读数据库比对结果：
+
+- 源数据并集：6041人，包含学生5946、宿管72、辅导员20、additional_staff 3。
+- 当前数据库：6056人；若排除既有 `dean` 角色，为6055人，与任务文档口径一致。
+- 分角色：学生5956、宿管75、辅导员22、admin 2、dean 1。
+- TMP ID：0。
+- 当前非rejected申请：1个，`app_4ae6dd14 / 2020001 / approved`。
+
+差异身份：
+
+- 额外学生10人：`2020001` 到 `2020010`，均为测试学生。
+- 额外宿管2人：`M001`、`M002`，均为测试宿管。
+- 额外辅导员2人：`T001`、`T002`，均为测试辅导员。
+
+相关代码依据：
+
+- `import_students --mode clean` 在存在非rejected申请时拒绝执行：`apps/users/management/commands/import_students.py:31`。
+- `clean` 只删除 `role=student` 用户，不清理宿管/辅导员/admin：`apps/users/management/commands/import_students.py:62`。
+- `import_staff` 当前只读取 `phone/building`，没有读取或写入 `department`：`apps/users/management/commands/import_staff.py:62`。
+- 学生提交申请时宿管按 `building` 查找，找不到走兜底：`apps/applications/views.py:151`。
+- 宿管通过后辅导员按学生 `department` 精确查找：`apps/approvals/views.py:163`。
+- `apps/approvals/views.py` 只导入 `UserRole`，未导入 `User`，但后续使用 `User.objects`：`apps/approvals/views.py:14`。
+
+## 影响评估
+
+### 功能影响
+
+14个历史测试账号对主流程没有直接破坏性影响：
+
+- 宿管路由基于学生 `building`，并且有兜底宿管；额外测试宿管 `M001/M002` 的 `building` 为空，不会按楼栋承接真实学生。
+- 权限控制基于 `role` 和当前登录用户，额外账号不会提升真实用户权限。
+- 额外测试学生不会影响真实学生提交申请，除非被用于登录和操作。
+
+但会造成环境数据污染：
+
+- 用户统计、覆盖率、角色人数会偏离源数据口径。
+- `2020001` 已有关联approved申请，会阻塞 `clean` 导入。
+- 测试账号如保留在生产，会带来审计、误登录和数据可信度风险。
+
+### 数据一致性影响
+
+当前差异不影响“TMP清零”和“兜底宿管存在”这两个硬指标，但会降低验收口径的可解释性。生产验收不应接受“已知测试账号残留”的用户基线。
+
+辅导员 `department` 缺失是独立的一致性问题，影响实际审批流，不应被14人差异掩盖。
+
+### 性能影响
+
+14条额外用户记录对性能无实际影响。
+
+## 根因调查建议
+
+不需要继续做大范围根因调查；当前已足够定位：
+
+- 10个学生、2个宿管、2个辅导员均符合项目测试/种子数据命名模式。
+- 创建时间集中在2026-06-03，早于Phase 3导入。
+- 源数据对比没有缺失主批次用户。
+
+建议保留一次性审计记录即可：列出额外账号、关联申请、清理方式和清理时间。
+
+## 生产导入策略推荐
+
+推荐：生产使用 clean/rebuild 基线，不使用 append 作为首次上线导入策略。
+
+具体建议：
+
+1. 新生产库优先从空库迁移后导入。保留必要系统账号或超级管理员，批量导入学生、宿管、辅导员、学工管理员、兜底宿管。
+2. 如果不是空库，先确认没有有效业务申请；否则不得直接删除学生。
+3. 不建议只运行现有 `import_students --mode clean` 后继续 append staff，因为该命令只清学生，无法清掉 `M001/M002/T001/T002` 这类历史 staff。
+4. 对当前开发/测试库，建议手动清理已知测试账号及其测试申请，或重建库；清理后重新执行 dry-run 和正式导入。
+5. append 模式仅适合后续增量补录，前提是输入文件经过白名单比对，且导入后运行“DB用户集合 - 源数据集合 = 0”的校验。
+
+不推荐方案A append：会保留污染数据，生产验收口径不干净。
+
+不推荐单纯方案C手动清理作为生产主策略：适合修复当前环境，不适合作为可复现上线流程。
+
+## 19名额外研究生处理建议
+
+建议暂不纳入主批次，不阻塞Phase 4。
+
+理由：
+
+- 这19人不在File1/File2/File5主批次。
+- 学号特征为2021/2022/2023，不足以证明属于2026届主批次。
+- 当前缺少学院/班级/楼栋/辅导员映射等路由关键字段。
+
+处理优先级：Phase 3.5补充批次，等待业务确认。确认属于2026届后，再按补充批次导入，并明确无楼栋是否走兜底宿管、学院如何映射辅导员。
+
+## Phase 4阻塞判断
+
+不阻塞：
+
+- 前端页面开发。
+- 登录、列表、表单、状态展示等基于现有API契约的开发。
+- 使用mock或固定测试账号做非端到端页面验收。
+
+阻塞：
+
+- 真实数据端到端联调。
+- 宿管通过后创建辅导员审批。
+- 生产导入验收。
+
+Phase 4前建议先完成以下P0/P1：
+
+- P0：修复 `apps/approvals/views.py` 缺少 `User` 导入。
+- P0：补齐辅导员 `department` 导入字段，或调整路由模型为明确的学院-辅导员映射。
+- P1：清理当前环境测试账号 `2020001-2020010/M001/M002/T001/T002` 及测试申请，或重建库。
+- P1：为生产导入增加导后校验脚本，至少校验角色人数、源数据缺失、DB额外用户、TMP ID、兜底宿管、学生无楼栋数量、辅导员department覆盖。
+
+## 最终建议
+
+接受Phase 3“主批次数据已导入、TMP已清零、兜底宿管已就位”的阶段性结论，但不要把当前数据库作为生产基线。
+
+生产上线采用可复现的clean/rebuild导入；19名额外研究生进入Phase 3.5待业务确认；Phase 4页面开发可以继续，但端到端审批联调前必须修正辅导员路由字段和 `User` 导入问题。

tokens used
88,269

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
