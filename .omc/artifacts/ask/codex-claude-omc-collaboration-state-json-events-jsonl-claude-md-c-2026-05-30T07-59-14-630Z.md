# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-05-30T07:59:14.631Z

## Original task

配置任务执行

我已完成Claude侧配置：
- ✓ 创建.omc/collaboration/目录结构
- ✓ 创建state.json初始文件
- ✓ 创建events.jsonl空文件
- ✓ 更新CLAUDE.md添加协作协议引用

现在请你完成Codex侧配置（按我们协商的清单）：

1. 更新AGENTS.md - 添加协作协议入口规则
2. 创建.omc/collaboration/protocol.md - 完整协议规范
3. 写ready信号 - codex_ready事件和codex-ready.md

请逐项执行并确认完成。

## Final prompt

配置任务执行

我已完成Claude侧配置：
- ✓ 创建.omc/collaboration/目录结构
- ✓ 创建state.json初始文件
- ✓ 创建events.jsonl空文件
- ✓ 更新CLAUDE.md添加协作协议引用

现在请你完成Codex侧配置（按我们协商的清单）：

1. 更新AGENTS.md - 添加协作协议入口规则
2. 创建.omc/collaboration/protocol.md - 完整协议规范
3. 写ready信号 - codex_ready事件和codex-ready.md

请逐项执行并确认完成。

## Raw output

```text
已按清单完成 Codex 侧配置：

1. 更新 [AGENTS.md](/home/caohui/projects/graduation-leave-system/AGENTS.md:6)
   已添加 Claude-Codex 协作协议入口规则，并补充协议冲突处理规则。

2. 创建 [.omc/collaboration/protocol.md](/home/caohui/projects/graduation-leave-system/.omc/collaboration/protocol.md:1)
   已写入完整协议规范，包含目录结构、共享状态、事件日志、任务、产物、锁、交接、完成和 ready 信号规则。

3. 写 ready 信号
   已创建 [.omc/collaboration/codex-ready.md](/home/caohui/projects/graduation-leave-system/.omc/collaboration/codex-ready.md:1)，并在 [.omc/collaboration/events.jsonl](/home/caohui/projects/graduation-leave-system/.omc/collaboration/events.jsonl:1) 写入 `codex_ready` 事件。  
   同时已更新 [.omc/collaboration/state.json](/home/caohui/projects/graduation-leave-system/.omc/collaboration/state.json:1)：`status` 为 `codex_ready`，`last_event_id` 为 `1`。

校验已完成：`state.json` JSON 有效，`events.jsonl` 可逐行解析。


OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019e77e2-a24e-73d1-aa54-ee022233fa59
--------
user
配置任务执行

我已完成Claude侧配置：
- ✓ 创建.omc/collaboration/目录结构
- ✓ 创建state.json初始文件
- ✓ 创建events.jsonl空文件
- ✓ 更新CLAUDE.md添加协作协议引用

现在请你完成Codex侧配置（按我们协商的清单）：

1. 更新AGENTS.md - 添加协作协议入口规则
2. 创建.omc/collaboration/protocol.md - 完整协议规范
3. 写ready信号 - codex_ready事件和codex-ready.md

请逐项执行并确认完成。
codex
我会先读取项目规则和现有协作文件，确认 Claude 侧已经放进去的结构与命名，然后再按清单落 Codex 侧配置。
exec
/bin/bash -lc "pwd && sed -n '1,220p' /home/caohui/.codex/RTK.md && sed -n '1,220p' AGENTS.md && find .omc -maxdepth 3 -type f -print | sort" in /home/caohui/projects/graduation-leave-system
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
# Project Agent Instructions

## Mandatory Project Rules

- For every shell command in this project, follow `/home/caohui/.codex/RTK.md`.
- Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.
- If `docs/codex-review-protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.
- Do not treat review-protocol steps as optional when the user requests a formal review or rule-governed Codex discussion.
.omc/artifacts/ask/codex-1-2-7-3-2026-05-30T07-12-16-863Z.md
.omc/artifacts/ask/codex-1-agents-md-codex-md-docs-codex-review-protocol-md-2-3-load--2026-05-30T07-17-55-095Z.md
.omc/artifacts/ask/codex-agents-md-docs-codex-review-protocol-md-1-agents-md-2-agents-2026-05-30T07-25-13-547Z.md
.omc/artifacts/ask/codex-claude-codex-mvp-claude-codex-orchestrator-omc-collaboration-2026-05-30T07-46-03-418Z.md
.omc/artifacts/ask/codex-claude-docs-codex-md-7-2026-05-30T07-10-12-622Z.md
.omc/artifacts/ask/codex-contract-v0-1-md-week-0-1-execution-plan-md-6-1-userdto-2-3--2026-05-30T07-53-39-979Z.md
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-31-data-source-requ-2026-05-27T03-21-37-887Z.md
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-33-response-to-code-2026-05-27T03-33-51-844Z.md
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-34-codex-second-rev-2026-05-27T08-21-47-897Z.md
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-37-api-blocking-sol-2026-05-30T07-07-49-087Z.md
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md
.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-43-next-steps-claud-2026-05-30T07-33-04-959Z.md
.omc/artifacts/ask/codex-docs-md-3-student-counselor-admin-docs-discussions-codex-rev-2026-05-27T03-07-33-566Z.md
.omc/artifacts/ask/codex-provider-claude-codex-1-2-3-omc-omc-team-provider-codex-gemi-2026-05-30T07-40-09-186Z.md
.omc/artifacts/ask/codex-week-0-1-docs-contracts-contract-v0-1-md-2-docs-plans-week-0-2026-05-30T07-43-47-472Z.md
.omc/collaboration/events.jsonl
.omc/collaboration/state.json
.omc/project-memory.json
.omc/project-state.json
.omc/session-context.json
.omc/sessions/04a41b19-6f39-4d0e-8072-0f0d097dea01.json
.omc/sessions/4aad264e-c3a4-460a-9be1-61247202bad3.json
.omc/sessions/86656873-1778-4d8a-aeee-2ff5db229c98.json
.omc/sessions/c4d9c5f4-fdb8-4176-8480-6aec0d7eaa87.json
.omc/sessions/c8f47bca-464c-4b8c-bab5-42ba59354101.json
.omc/sessions/cde0b835-f3fb-47de-af08-5d37887de1bb.json
.omc/sessions/dcf39a3e-1b72-449a-9897-852c3c7f1253.json
.omc/sessions/e2566739-aaa7-4701-9354-a710639ac308.json
.omc/sessions/f91e1567-b1b2-4cc2-bd9b-355702bc1ec4.json
.omc/state/agent-replay-7afec07d-3b40-4e4c-8f86-86e9dc0e791c.jsonl
.omc/state/agent-replay-97c93024-a4c1-4e03-93bf-7522ce3517ff.jsonl
.omc/state/checkpoints/checkpoint-2026-05-26T22-08-15-239Z.json
.omc/state/checkpoints/checkpoint-2026-05-26T22-47-05-286Z.json
.omc/state/checkpoints/checkpoint-2026-05-26T23-17-40-016Z.json
.omc/state/checkpoints/checkpoint-2026-05-27T00-56-14-420Z.json
.omc/state/checkpoints/checkpoint-2026-05-27T02-01-44-759Z.json
.omc/state/checkpoints/checkpoint-2026-05-27T02-36-09-263Z.json
.omc/state/checkpoints/checkpoint-2026-05-27T03-22-00-316Z.json
.omc/state/checkpoints/checkpoint-2026-05-27T03-22-27-490Z.json
.omc/state/checkpoints/checkpoint-2026-05-27T03-22-48-406Z.json
.omc/state/checkpoints/checkpoint-2026-05-27T08-11-32-768Z.json
.omc/state/checkpoints/checkpoint-2026-05-27T08-22-20-562Z.json
.omc/state/checkpoints/checkpoint-2026-05-27T08-57-23-348Z.json
.omc/state/checkpoints/checkpoint-2026-05-28T05-56-27-412Z.json
.omc/state/checkpoints/checkpoint-2026-05-30T07-12-05-953Z.json
.omc/state/checkpoints/checkpoint-2026-05-30T07-54-15-592Z.json
.omc/state/hud-stdin-cache.json
.omc/state/last-tool-error.json
.omc/state/mission-state.json

codex
现有项目规则要求所有项目内 shell 命令走 `rtk`。我已经看到 `.omc/collaboration` 里有 `state.json` 和 `events.jsonl`，接下来读取 Claude 侧写入的引用和状态内容，避免协议入口规则写偏。
exec
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
 M .omc/state/hud-stdin-cache.json
 M CLAUDE.md
?? .claude/
?? .omc/artifacts/
?? .omc/collaboration/
?? .omc/project-memory.json
?? .omc/sessions/
?? .omc/state/agent-replay-7afec07d-3b40-4e4c-8f86-86e9dc0e791c.jsonl
?? .omc/state/agent-replay-97c93024-a4c1-4e03-93bf-7522ce3517ff.jsonl
?? .omc/state/checkpoints/
?? .omc/state/last-tool-error.json
?? .omc/state/mission-state.json
?? .omc/state/sessions/4aad264e-c3a4-460a-9be1-61247202bad3/
?? .omc/state/sessions/7afec07d-3b40-4e4c-8f86-86e9dc0e791c/
?? .omc/state/sessions/97c93024-a4c1-4e03-93bf-7522ce3517ff/
?? .omc/state/sessions/c8f47bca-464c-4b8c-bab5-42ba59354101/
?? .omc/state/sessions/dcf39a3e-1b72-449a-9897-852c3c7f1253/
?? .omc/state/sessions/e2566739-aaa7-4701-9354-a710639ac308/
?? .omc/state/sessions/f91e1567-b1b2-4cc2-bd9b-355702bc1ec4/
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
?? "\346\257\225\344\270\232\347\246\273\346\240\241\347\263\273\347\273\237\347\224\250\346\210\267\346\226\207\346\241\243.zip"
exec
/bin/bash -lc 'rtk wc -c .omc/collaboration/events.jsonl' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
0

exec
/bin/bash -lc "rtk sed -n '1,220p' .omc/collaboration/state.json" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{
  "workflow_id": "claude-codex-collab-mvp",
  "current_task": null,
  "active_agent": "none",
  "status": "initialized",
  "last_event_id": 0,
  "updated_at": "2026-05-30T07:55:52.342Z"
}

exec
/bin/bash -lc "rtk sed -n '1,220p' CLAUDE.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 毕业生离校申请审批系统 - 项目配置

## 项目信息

**项目名称：** 毕业生离校申请审批系统  
**技术栈：** Python Flask + MySQL + 微信小程序  
**文档目录：** `docs/`  
**讨论记录：** `docs/discussions/codex-review-2026-05-27/`

---

## Claude-Codex协作机制

**协作协议：** `.omc/collaboration/protocol.md`

**强制规则：** When participating in Claude-Codex collaboration workflow, read and follow `.omc/collaboration/protocol.md` for task execution, artifact generation, and state management.

---

## Codex审查流程（强制要求）

**流程文档：** `docs/codex-review-protocol.md`

**强制规则：** Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.

### 核心要求

1. **统一调用方式**
   - 使用 `/oh-my-claudecode:ask codex` 进行所有审查
   - 不直接调用 `codex` CLI命令

2. **结构化审查请求**
   - 创建审查请求文档（XX-[主题]-review-request.md）
   - 明确审查范围、要点、期望输出

3. **批判性分析**
   - 不盲目接受Codex建议
   - 在Claude响应文档中说明理由
   - 深入分析根本原因和影响范围

4. **完整流程（7步）**
   - 第1步：创建审查请求文档
   - 第2步：调用 `/oh-my-claudecode:ask codex`
   - 第3步：保存Codex审查结果
   - 第4步：Claude响应Codex审查
   - 第5步：执行修复
   - 第6步：创建共识文档
   - 第7步：归档到项目文档

5. **文档一致性**
   - 修复后验证所有相关文档
   - 确保字段命名、类型、必填性统一
   - 更新PROJECT-SUMMARY.md和session-context.json

---

## 文档审查触发条件

当满足以下任一条件时，必须使用Codex审查流程：

- 创建或修改技术设计文档
- 数据库模型变更
- API接口设计
- 数据对接方案
- 系统架构调整
- 关键业务流程变更

---

## 项目约定

### 文档编号规则

**讨论文档：** `docs/discussions/codex-review-YYYY-MM-DD/XX-[主题].md`

**审查文档编号：**
- XX号：审查请求
- XX+1号：Codex响应
- XX+2号：Claude响应
- XX+3号：最终共识

### 提交规范

**Commit格式：**
```
<type>: <description>

<body>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**Type类型：**
- `docs`: 文档更新
- `feat`: 新功能
- `fix`: 修复
- `refactor`: 重构
- `chore`: 杂项

---

## 变更管理（强制）

**每次修改后必须：**
1. 检查所有关联文件是否需要同步修改
2. 用Read工具验证修改内容正确
3. 更新PROJECT-SUMMARY.md或CHANGELOG.md
4. 更新.omc/session-context.json
5. git add + commit + push（一次性包含所有变更）

---

## 参考文档

- **系统设计：** `docs/design/2026-05-27-system-design.md`
- **数据对接：** `docs/数据对接说明文档.md`
- **用户文档：** `docs/用户设计说明书.md`
- **审查流程：** `docs/codex-review-protocol.md`
- **项目总结：** `docs/PROJECT-SUMMARY.md`

codex
`CLAUDE.md` 已经指向 `.omc/collaboration/protocol.md`，状态文件当前是 initialized、事件流为空。下一步我会补齐 `AGENTS.md` 的同等入口规则，并写入协议正文和 ready 信号文件。
exec
/bin/bash -lc "rtk find .omc/collaboration -maxdepth 2 -type f -print -exec wc -c {} \\;" in /home/caohui/projects/graduation-leave-system
 exited 1 in 0ms:
rtk: rtk find does not support compound predicates or actions (e.g. -not, -exec). Use `find` directly.

exec
/bin/bash -lc "rtk rg -n \"Claude-Codex|collaboration|protocol.md|codex_ready|codex-ready\" -S . -g '"'!node_modules'"' -g '"'!venv'"'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
./CLAUDE.md:12:## Claude-Codex协作机制
./CLAUDE.md:14:**协作协议：** `.omc/collaboration/protocol.md`
./CLAUDE.md:16:**强制规则：** When participating in Claude-Codex collaboration workflow, read and follow `.omc/collaboration/protocol.md` for task execution, artifact generation, and state management.
./CLAUDE.md:22:**流程文档：** `docs/codex-review-protocol.md`
./CLAUDE.md:24:**强制规则：** Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.
./CLAUDE.md:118:- **审查流程：** `docs/codex-review-protocol.md`
./AGENTS.md:6:- Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.
./AGENTS.md:7:- If `docs/codex-review-protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.

exec
/bin/bash -lc 'rtk ls -la .omc/collaboration' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
artifacts/
locks/
tasks/
events.jsonl  0B
state.json  190B

exec
/bin/bash -lc 'rtk date -u +%Y-%m-%dT%H:%M:%SZ' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
2026-05-30T07:57:25Z

codex
我现在会做实际文件变更：`AGENTS.md` 增加 Codex 侧入口规则；`.omc/collaboration/protocol.md` 定义共享状态、事件、任务、产物、锁和交接流程；最后写入 `codex_ready` 事件、ready 文档，并同步 `state.json` 的事件序号与状态。
apply patch
patch: completed
/home/caohui/projects/graduation-leave-system/.omc/collaboration/codex-ready.md
/home/caohui/projects/graduation-leave-system/.omc/collaboration/events.jsonl
/home/caohui/projects/graduation-leave-system/.omc/collaboration/protocol.md
/home/caohui/projects/graduation-leave-system/.omc/collaboration/state.json
/home/caohui/projects/graduation-leave-system/AGENTS.md
diff --git a/.omc/collaboration/codex-ready.md b/.omc/collaboration/codex-ready.md
new file mode 100644
index 0000000000000000000000000000000000000000..3d85f283fdaeb2d363aecc01ea11addd758d58e4
--- /dev/null
+++ b/.omc/collaboration/codex-ready.md
@@ -0,0 +1,16 @@
+# Codex Ready
+
+Status: ready
+Agent: codex
+Timestamp: 2026-05-30T07:57:25.000Z
+Event: codex_ready
+Event ID: 1
+
+Codex-side collaboration configuration is complete.
+
+Completed items:
+
+- Updated `AGENTS.md` with the collaboration protocol entry rule.
+- Created `.omc/collaboration/protocol.md` with the shared protocol specification.
+- Wrote the `codex_ready` event to `.omc/collaboration/events.jsonl`.
+- Updated `.omc/collaboration/state.json` to reflect `codex_ready`.
diff --git a/.omc/collaboration/events.jsonl b/.omc/collaboration/events.jsonl
index e69de29bb2d1d6434b8b29ae775ad8c2e48c5391..d2f79e2115e8e4718cb7eb731b4a8308dd20e965
--- a/.omc/collaboration/events.jsonl
+++ b/.omc/collaboration/events.jsonl
@@ -0,0 +1 @@
+{"id":1,"type":"codex_ready","agent":"codex","timestamp":"2026-05-30T07:57:25.000Z","summary":"Codex collaboration configuration completed and ready for Claude-Codex workflow.","artifacts":["AGENTS.md",".omc/collaboration/protocol.md",".omc/collaboration/codex-ready.md"],"status":"codex_ready"}
diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
new file mode 100644
index 0000000000000000000000000000000000000000..a831acc3f4534a3d2c3a48ce4720292ccf968809
--- /dev/null
+++ b/.omc/collaboration/protocol.md
@@ -0,0 +1,212 @@
+# Claude-Codex Collaboration Protocol
+
+Version: 0.1
+Status: active
+Owner: Claude + Codex
+
+## 1. Purpose
+
+This protocol defines the shared operating contract for Claude-Codex collaboration in this repository. It covers task handoff, shared state, event logging, artifact creation, lock usage, and completion signaling.
+
+Agents must read this file before participating in the collaboration workflow.
+
+## 2. Directory Layout
+
+All collaboration files live under `.omc/collaboration/`.
+
+- `protocol.md`: this protocol.
+- `state.json`: current shared workflow state.
+- `events.jsonl`: append-only event log.
+- `tasks/`: task specifications and task handoff documents.
+- `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
+- `locks/`: advisory lock files for serialized work.
+- `codex-ready.md`: Codex readiness signal.
+
+## 3. Authority And Conflicts
+
+This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
+
+If a conflict is encountered, the active agent must follow the higher-priority instruction and record the conflict in its response or task artifact when material to the collaboration.
+
+Codex-specific repository rules in `AGENTS.md` remain mandatory. Claude-specific repository rules in `CLAUDE.md` remain mandatory.
+
+## 4. Shared State
+
+`state.json` is the latest compact state snapshot. It must remain valid JSON.
+
+Recommended schema:
+
+```json
+{
+  "workflow_id": "claude-codex-collab-mvp",
+  "current_task": null,
+  "active_agent": "none",
+  "status": "initialized",
+  "last_event_id": 0,
+  "updated_at": "2026-05-30T00:00:00.000Z"
+}
+```
+
+Field meanings:
+
+- `workflow_id`: stable collaboration workflow identifier.
+- `current_task`: active task id or `null`.
+- `active_agent`: `claude`, `codex`, or `none`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `last_event_id`: numeric id of the last event written to `events.jsonl`.
+- `updated_at`: UTC ISO-8601 timestamp for the state update.
+
+State updates should be minimal and should not replace durable task or artifact content.
+
+## 5. Event Log
+
+`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+
+Required event fields:
+
+```json
+{
+  "id": 1,
+  "type": "codex_ready",
+  "agent": "codex",
+  "timestamp": "2026-05-30T00:00:00.000Z",
+  "summary": "Short event summary."
+}
+```
+
+Recommended optional fields:
+
+- `task_id`: related task id.
+- `artifacts`: array of artifact paths.
+- `status`: resulting workflow status.
+- `details`: compact structured metadata.
+
+Event id rules:
+
+- Start at `1`.
+- Increment by `1` for every new event.
+- After writing an event, update `state.json.last_event_id` to the new id.
+
+Common event types:
+
+- `claude_ready`
+- `codex_ready`
+- `task_created`
+- `task_claimed`
+- `artifact_created`
+- `handoff_requested`
+- `review_requested`
+- `blocked`
+- `completed`
+
+## 6. Tasks
+
+Task documents belong in `.omc/collaboration/tasks/`.
+
+Recommended task filename:
+
+```text
+TASK-YYYYMMDD-NN-short-name.md
+```
+
+Recommended task content:
+
+- Task id.
+- Owner or requesting agent.
+- Objective.
+- Scope.
+- Inputs and relevant files.
+- Expected outputs.
+- Constraints and mandatory rules.
+- Acceptance criteria.
+- Current status.
+
+When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+
+## 7. Artifacts
+
+Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
+
+Artifacts should be durable and self-contained enough for the other agent to continue work without relying on chat history.
+
+Recommended artifact filenames:
+
+```text
+YYYYMMDD-HHMM-agent-topic.md
+```
+
+For formal Codex review or OMC `/ask codex` workflows, the repository's `docs/codex-review-protocol.md` remains mandatory and takes precedence over this generic artifact convention.
+
+## 8. Locks
+
+Locks are advisory files under `.omc/collaboration/locks/`.
+
+Use a lock when two agents might modify the same shared collaboration file at the same time.
+
+Recommended lock filename:
+
+```text
+resource-name.lock
+```
+
+Recommended lock content:
+
+```json
+{
+  "agent": "codex",
+  "resource": "state.json",
+  "created_at": "2026-05-30T00:00:00.000Z",
+  "reason": "Updating state after event append."
+}
+```
+
+Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
+
+## 9. Handoff Rules
+
+When handing work to the other agent:
+
+1. Write or update the task document.
+2. Write any supporting artifact needed for context.
+3. Append a `handoff_requested` event.
+4. Update `state.json` with the current task, status, active agent, and last event id.
+5. State the handoff clearly in the user-facing response when applicable.
+
+Handoffs should include concrete next actions, relevant file paths, and any known blockers.
+
+## 10. Completion Rules
+
+A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
+
+Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
+
+## 11. Readiness Signal
+
+Codex readiness is represented by both:
+
+- A `codex_ready` event in `events.jsonl`.
+- `.omc/collaboration/codex-ready.md`.
+
+Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
+
+## 12. Minimal Operating Checklist
+
+Before collaboration work:
+
+- Read `AGENTS.md` or `CLAUDE.md`, as applicable.
+- Read `.omc/collaboration/protocol.md`.
+- Inspect `state.json` and recent `events.jsonl` entries.
+
+During collaboration work:
+
+- Keep edits scoped to the task.
+- Preserve append-only event history.
+- Keep shared JSON valid.
+- Create durable artifacts for decisions that must survive chat context.
+
+After collaboration work:
+
+- Append the relevant event.
+- Update `state.json`.
+- Verify changed files.
+- Report completed items and any remaining risk.
diff --git a/.omc/collaboration/state.json b/.omc/collaboration/state.json
index 8bb3c6cdb1f9fa26ff0bf1461955b09fa865fcd8..cd54728b42f70c14c107993b869b9af2fdf5da79
--- a/.omc/collaboration/state.json
+++ b/.omc/collaboration/state.json
@@ -2,7 +2,7 @@
   "workflow_id": "claude-codex-collab-mvp",
   "current_task": null,
   "active_agent": "none",
-  "status": "initialized",
-  "last_event_id": 0,
-  "updated_at": "2026-05-30T07:55:52.342Z"
+  "status": "codex_ready",
+  "last_event_id": 1,
+  "updated_at": "2026-05-30T07:57:25.000Z"
 }
diff --git a/AGENTS.md b/AGENTS.md
index dff45f359d65fc63ff972d7f5caf24b6070a0dac..72a8b712798d84d6e47fb68909cbe2d595d68ebf
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -3,6 +3,8 @@
 ## Mandatory Project Rules
 
 - For every shell command in this project, follow `/home/caohui/.codex/RTK.md`.
+- When participating in the Claude-Codex collaboration workflow, read and follow `.omc/collaboration/protocol.md` before acting. Treat it as the project-local contract for task execution, artifact generation, event logging, and shared state management.
 - Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.
 - If `docs/codex-review-protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.
 - Do not treat review-protocol steps as optional when the user requests a formal review or rule-governed Codex discussion.
+- If `.omc/collaboration/protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.

diff --git a/.omc/collaboration/codex-ready.md b/.omc/collaboration/codex-ready.md
new file mode 100644
index 0000000000000000000000000000000000000000..3d85f283fdaeb2d363aecc01ea11addd758d58e4
--- /dev/null
+++ b/.omc/collaboration/codex-ready.md
@@ -0,0 +1,16 @@
+# Codex Ready
+
+Status: ready
+Agent: codex
+Timestamp: 2026-05-30T07:57:25.000Z
+Event: codex_ready
+Event ID: 1
+
+Codex-side collaboration configuration is complete.
+
+Completed items:
+
+- Updated `AGENTS.md` with the collaboration protocol entry rule.
+- Created `.omc/collaboration/protocol.md` with the shared protocol specification.
+- Wrote the `codex_ready` event to `.omc/collaboration/events.jsonl`.
+- Updated `.omc/collaboration/state.json` to reflect `codex_ready`.
diff --git a/.omc/collaboration/events.jsonl b/.omc/collaboration/events.jsonl
index e69de29bb2d1d6434b8b29ae775ad8c2e48c5391..d2f79e2115e8e4718cb7eb731b4a8308dd20e965
--- a/.omc/collaboration/events.jsonl
+++ b/.omc/collaboration/events.jsonl
@@ -0,0 +1 @@
+{"id":1,"type":"codex_ready","agent":"codex","timestamp":"2026-05-30T07:57:25.000Z","summary":"Codex collaboration configuration completed and ready for Claude-Codex workflow.","artifacts":["AGENTS.md",".omc/collaboration/protocol.md",".omc/collaboration/codex-ready.md"],"status":"codex_ready"}
diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
new file mode 100644
index 0000000000000000000000000000000000000000..a831acc3f4534a3d2c3a48ce4720292ccf968809
--- /dev/null
+++ b/.omc/collaboration/protocol.md
@@ -0,0 +1,212 @@
+# Claude-Codex Collaboration Protocol
+
+Version: 0.1
+Status: active
+Owner: Claude + Codex
+
+## 1. Purpose
+
+This protocol defines the shared operating contract for Claude-Codex collaboration in this repository. It covers task handoff, shared state, event logging, artifact creation, lock usage, and completion signaling.
+
+Agents must read this file before participating in the collaboration workflow.
+
+## 2. Directory Layout
+
+All collaboration files live under `.omc/collaboration/`.
+
+- `protocol.md`: this protocol.
+- `state.json`: current shared workflow state.
+- `events.jsonl`: append-only event log.
+- `tasks/`: task specifications and task handoff documents.
+- `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
+- `locks/`: advisory lock files for serialized work.
+- `codex-ready.md`: Codex readiness signal.
+
+## 3. Authority And Conflicts
+
+This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
+
+If a conflict is encountered, the active agent must follow the higher-priority instruction and record the conflict in its response or task artifact when material to the collaboration.
+
+Codex-specific repository rules in `AGENTS.md` remain mandatory. Claude-specific repository rules in `CLAUDE.md` remain mandatory.
+
+## 4. Shared State
+
+`state.json` is the latest compact state snapshot. It must remain valid JSON.
+
+Recommended schema:
+
+```json
+{
+  "workflow_id": "claude-codex-collab-mvp",
+  "current_task": null,
+  "active_agent": "none",
+  "status": "initialized",
+  "last_event_id": 0,
+  "updated_at": "2026-05-30T00:00:00.000Z"
+}
+```
+
+Field meanings:
+
+- `workflow_id`: stable collaboration workflow identifier.
+- `current_task`: active task id or `null`.
+- `active_agent`: `claude`, `codex`, or `none`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `last_event_id`: numeric id of the last event written to `events.jsonl`.
+- `updated_at`: UTC ISO-8601 timestamp for the state update.
+
+State updates should be minimal and should not replace durable task or artifact content.
+
+## 5. Event Log
+
+`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+
+Required event fields:
+
+```json
+{
+  "id": 1,
+  "type": "codex_ready",
+  "agent": "codex",
+  "timestamp": "2026-05-30T00:00:00.000Z",
+  "summary": "Short event summary."
+}
+```
+
+Recommended optional fields:
+
+- `task_id`: related task id.
+- `artifacts`: array of artifact paths.
+- `status`: resulting workflow status.
+- `details`: compact structured metadata.
+
+Event id rules:
+
+- Start at `1`.
+- Increment by `1` for every new event.
+- After writing an event, update `state.json.last_event_id` to the new id.
+
+Common event types:
+
+- `claude_ready`
+- `codex_ready`
+- `task_created`
+- `task_claimed`
+- `artifact_created`
+- `handoff_requested`
+- `review_requested`
+- `blocked`
+- `completed`
+
+## 6. Tasks
+
+Task documents belong in `.omc/collaboration/tasks/`.
+
+Recommended task filename:
+
+```text
+TASK-YYYYMMDD-NN-short-name.md
+```
+
+Recommended task content:
+
+- Task id.
+- Owner or requesting agent.
+- Objective.
+- Scope.
+- Inputs and relevant files.
+- Expected outputs.
+- Constraints and mandatory rules.
+- Acceptance criteria.
+- Current status.
+
+When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+
+## 7. Artifacts
+
+Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
+
+Artifacts should be durable and self-contained enough for the other agent to continue work without relying on chat history.
+
+Recommended artifact filenames:
+
+```text
+YYYYMMDD-HHMM-agent-topic.md
+```
+
+For formal Codex review or OMC `/ask codex` workflows, the repository's `docs/codex-review-protocol.md` remains mandatory and takes precedence over this generic artifact convention.
+
+## 8. Locks
+
+Locks are advisory files under `.omc/collaboration/locks/`.
+
+Use a lock when two agents might modify the same shared collaboration file at the same time.
+
+Recommended lock filename:
+
+```text
+resource-name.lock
+```
+
+Recommended lock content:
+
+```json
+{
+  "agent": "codex",
+  "resource": "state.json",
+  "created_at": "2026-05-30T00:00:00.000Z",
+  "reason": "Updating state after event append."
+}
+```
+
+Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
+
+## 9. Handoff Rules
+
+When handing work to the other agent:
+
+1. Write or update the task document.
+2. Write any supporting artifact needed for context.
+3. Append a `handoff_requested` event.
+4. Update `state.json` with the current task, status, active agent, and last event id.
+5. State the handoff clearly in the user-facing response when applicable.
+
+Handoffs should include concrete next actions, relevant file paths, and any known blockers.
+
+## 10. Completion Rules
+
+A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
+
+Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
+
+## 11. Readiness Signal
+
+Codex readiness is represented by both:
+
+- A `codex_ready` event in `events.jsonl`.
+- `.omc/collaboration/codex-ready.md`.
+
+Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
+
+## 12. Minimal Operating Checklist
+
+Before collaboration work:
+
+- Read `AGENTS.md` or `CLAUDE.md`, as applicable.
+- Read `.omc/collaboration/protocol.md`.
+- Inspect `state.json` and recent `events.jsonl` entries.
+
+During collaboration work:
+
+- Keep edits scoped to the task.
+- Preserve append-only event history.
+- Keep shared JSON valid.
+- Create durable artifacts for decisions that must survive chat context.
+
+After collaboration work:
+
+- Append the relevant event.
+- Update `state.json`.
+- Verify changed files.
+- Report completed items and any remaining risk.
diff --git a/.omc/collaboration/state.json b/.omc/collaboration/state.json
index 8bb3c6cdb1f9fa26ff0bf1461955b09fa865fcd8..cd54728b42f70c14c107993b869b9af2fdf5da79
--- a/.omc/collaboration/state.json
+++ b/.omc/collaboration/state.json
@@ -2,7 +2,7 @@
   "workflow_id": "claude-codex-collab-mvp",
   "current_task": null,
   "active_agent": "none",
-  "status": "initialized",
-  "last_event_id": 0,
-  "updated_at": "2026-05-30T07:55:52.342Z"
+  "status": "codex_ready",
+  "last_event_id": 1,
+  "updated_at": "2026-05-30T07:57:25.000Z"
 }
diff --git a/AGENTS.md b/AGENTS.md
index dff45f359d65fc63ff972d7f5caf24b6070a0dac..72a8b712798d84d6e47fb68909cbe2d595d68ebf
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -3,6 +3,8 @@
 ## Mandatory Project Rules
 
 - For every shell command in this project, follow `/home/caohui/.codex/RTK.md`.
+- When participating in the Claude-Codex collaboration workflow, read and follow `.omc/collaboration/protocol.md` before acting. Treat it as the project-local contract for task execution, artifact generation, event logging, and shared state management.
 - Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.
 - If `docs/codex-review-protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.
 - Do not treat review-protocol steps as optional when the user requests a formal review or rule-governed Codex discussion.
+- If `.omc/collaboration/protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.

codex
文件已经写入。现在我会做一次校验：检查 JSON 是否有效、事件日志是否可逐行解析，并复读关键文件确认内容落盘。
exec
/bin/bash -lc 'rtk python -m json.tool .omc/collaboration/state.json' in /home/caohui/projects/graduation-leave-system
 exited 127 in 0ms:
[rtk: No such file or directory (os error 2)]

exec
/bin/bash -lc "rtk python -c \"import json,pathlib; [json.loads(line) for line in pathlib.Path('.omc/collaboration/events.jsonl').read_text().splitlines() if line.strip()]; print('events.jsonl ok')\"" in /home/caohui/projects/graduation-leave-system
 exited 127 in 0ms:
[rtk: No such file or directory (os error 2)]

exec
/bin/bash -lc "rtk sed -n '1,40p' AGENTS.md" in /home/caohui/projects/graduation-leave-system
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
/bin/bash -lc "rtk sed -n '1,20p' .omc/collaboration/events.jsonl" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{"id":1,"type":"codex_ready","agent":"codex","timestamp":"2026-05-30T07:57:25.000Z","summary":"Codex collaboration configuration completed and ready for Claude-Codex workflow.","artifacts":["AGENTS.md",".omc/collaboration/protocol.md",".omc/collaboration/codex-ready.md"],"status":"codex_ready"}

exec
/bin/bash -lc "rtk sed -n '1,220p' .omc/collaboration/protocol.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Claude-Codex Collaboration Protocol

Version: 0.1
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
- `locks/`: advisory lock files for serialized work.
- `codex-ready.md`: Codex readiness signal.

## 3. Authority And Conflicts

This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.

If a conflict is encountered, the active agent must follow the higher-priority instruction and record the conflict in its response or task artifact when material to the collaboration.

Codex-specific repository rules in `AGENTS.md` remain mandatory. Claude-specific repository rules in `CLAUDE.md` remain mandatory.

## 4. Shared State

`state.json` is the latest compact state snapshot. It must remain valid JSON.

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
- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
- `last_event_id`: numeric id of the last event written to `events.jsonl`.
- `updated_at`: UTC ISO-8601 timestamp for the state update.

State updates should be minimal and should not replace durable task or artifact content.

## 5. Event Log

`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.

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

- Start at `1`.
- Increment by `1` for every new event.
- After writing an event, update `state.json.last_event_id` to the new id.

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

When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.

## 7. Artifacts

Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.

Artifacts should be durable and self-contained enough for the other agent to continue work without relying on chat history.

Recommended artifact filenames:

```text
YYYYMMDD-HHMM-agent-topic.md
```

For formal Codex review or OMC `/ask codex` workflows, the repository's `docs/codex-review-protocol.md` remains mandatory and takes precedence over this generic artifact convention.

## 8. Locks

Locks are advisory files under `.omc/collaboration/locks/`.

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

## 9. Handoff Rules

When handing work to the other agent:

1. Write or update the task document.
2. Write any supporting artifact needed for context.
3. Append a `handoff_requested` event.
4. Update `state.json` with the current task, status, active agent, and last event id.
5. State the handoff clearly in the user-facing response when applicable.

Handoffs should include concrete next actions, relevant file paths, and any known blockers.

## 10. Completion Rules

A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.

Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.

## 11. Readiness Signal

Codex readiness is represented by both:

- A `codex_ready` event in `events.jsonl`.
- `.omc/collaboration/codex-ready.md`.

Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.

## 12. Minimal Operating Checklist

Before collaboration work:

- Read `AGENTS.md` or `CLAUDE.md`, as applicable.
- Read `.omc/collaboration/protocol.md`.
- Inspect `state.json` and recent `events.jsonl` entries.

During collaboration work:

- Keep edits scoped to the task.
- Preserve append-only event history.
- Keep shared JSON valid.
- Create durable artifacts for decisions that must survive chat context.

After collaboration work:

- Append the relevant event.
- Update `state.json`.
- Verify changed files.
- Report completed items and any remaining risk.

exec
/bin/bash -lc "rtk sed -n '1,80p' .omc/collaboration/codex-ready.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Codex Ready

Status: ready
Agent: codex
Timestamp: 2026-05-30T07:57:25.000Z
Event: codex_ready
Event ID: 1

Codex-side collaboration configuration is complete.

Completed items:

- Updated `AGENTS.md` with the collaboration protocol entry rule.
- Created `.omc/collaboration/protocol.md` with the shared protocol specification.
- Wrote the `codex_ready` event to `.omc/collaboration/events.jsonl`.
- Updated `.omc/collaboration/state.json` to reflect `codex_ready`.

diff --git a/.omc/collaboration/codex-ready.md b/.omc/collaboration/codex-ready.md
new file mode 100644
index 0000000000000000000000000000000000000000..3d85f283fdaeb2d363aecc01ea11addd758d58e4
--- /dev/null
+++ b/.omc/collaboration/codex-ready.md
@@ -0,0 +1,16 @@
+# Codex Ready
+
+Status: ready
+Agent: codex
+Timestamp: 2026-05-30T07:57:25.000Z
+Event: codex_ready
+Event ID: 1
+
+Codex-side collaboration configuration is complete.
+
+Completed items:
+
+- Updated `AGENTS.md` with the collaboration protocol entry rule.
+- Created `.omc/collaboration/protocol.md` with the shared protocol specification.
+- Wrote the `codex_ready` event to `.omc/collaboration/events.jsonl`.
+- Updated `.omc/collaboration/state.json` to reflect `codex_ready`.
diff --git a/.omc/collaboration/events.jsonl b/.omc/collaboration/events.jsonl
index e69de29bb2d1d6434b8b29ae775ad8c2e48c5391..d2f79e2115e8e4718cb7eb731b4a8308dd20e965
--- a/.omc/collaboration/events.jsonl
+++ b/.omc/collaboration/events.jsonl
@@ -0,0 +1 @@
+{"id":1,"type":"codex_ready","agent":"codex","timestamp":"2026-05-30T07:57:25.000Z","summary":"Codex collaboration configuration completed and ready for Claude-Codex workflow.","artifacts":["AGENTS.md",".omc/collaboration/protocol.md",".omc/collaboration/codex-ready.md"],"status":"codex_ready"}
diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
new file mode 100644
index 0000000000000000000000000000000000000000..a831acc3f4534a3d2c3a48ce4720292ccf968809
--- /dev/null
+++ b/.omc/collaboration/protocol.md
@@ -0,0 +1,212 @@
+# Claude-Codex Collaboration Protocol
+
+Version: 0.1
+Status: active
+Owner: Claude + Codex
+
+## 1. Purpose
+
+This protocol defines the shared operating contract for Claude-Codex collaboration in this repository. It covers task handoff, shared state, event logging, artifact creation, lock usage, and completion signaling.
+
+Agents must read this file before participating in the collaboration workflow.
+
+## 2. Directory Layout
+
+All collaboration files live under `.omc/collaboration/`.
+
+- `protocol.md`: this protocol.
+- `state.json`: current shared workflow state.
+- `events.jsonl`: append-only event log.
+- `tasks/`: task specifications and task handoff documents.
+- `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
+- `locks/`: advisory lock files for serialized work.
+- `codex-ready.md`: Codex readiness signal.
+
+## 3. Authority And Conflicts
+
+This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
+
+If a conflict is encountered, the active agent must follow the higher-priority instruction and record the conflict in its response or task artifact when material to the collaboration.
+
+Codex-specific repository rules in `AGENTS.md` remain mandatory. Claude-specific repository rules in `CLAUDE.md` remain mandatory.
+
+## 4. Shared State
+
+`state.json` is the latest compact state snapshot. It must remain valid JSON.
+
+Recommended schema:
+
+```json
+{
+  "workflow_id": "claude-codex-collab-mvp",
+  "current_task": null,
+  "active_agent": "none",
+  "status": "initialized",
+  "last_event_id": 0,
+  "updated_at": "2026-05-30T00:00:00.000Z"
+}
+```
+
+Field meanings:
+
+- `workflow_id`: stable collaboration workflow identifier.
+- `current_task`: active task id or `null`.
+- `active_agent`: `claude`, `codex`, or `none`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `last_event_id`: numeric id of the last event written to `events.jsonl`.
+- `updated_at`: UTC ISO-8601 timestamp for the state update.
+
+State updates should be minimal and should not replace durable task or artifact content.
+
+## 5. Event Log
+
+`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+
+Required event fields:
+
+```json
+{
+  "id": 1,
+  "type": "codex_ready",
+  "agent": "codex",
+  "timestamp": "2026-05-30T00:00:00.000Z",
+  "summary": "Short event summary."
+}
+```
+
+Recommended optional fields:
+
+- `task_id`: related task id.
+- `artifacts`: array of artifact paths.
+- `status`: resulting workflow status.
+- `details`: compact structured metadata.
+
+Event id rules:
+
+- Start at `1`.
+- Increment by `1` for every new event.
+- After writing an event, update `state.json.last_event_id` to the new id.
+
+Common event types:
+
+- `claude_ready`
+- `codex_ready`
+- `task_created`
+- `task_claimed`
+- `artifact_created`
+- `handoff_requested`
+- `review_requested`
+- `blocked`
+- `completed`
+
+## 6. Tasks
+
+Task documents belong in `.omc/collaboration/tasks/`.
+
+Recommended task filename:
+
+```text
+TASK-YYYYMMDD-NN-short-name.md
+```
+
+Recommended task content:
+
+- Task id.
+- Owner or requesting agent.
+- Objective.
+- Scope.
+- Inputs and relevant files.
+- Expected outputs.
+- Constraints and mandatory rules.
+- Acceptance criteria.
+- Current status.
+
+When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+
+## 7. Artifacts
+
+Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
+
+Artifacts should be durable and self-contained enough for the other agent to continue work without relying on chat history.
+
+Recommended artifact filenames:
+
+```text
+YYYYMMDD-HHMM-agent-topic.md
+```
+
+For formal Codex review or OMC `/ask codex` workflows, the repository's `docs/codex-review-protocol.md` remains mandatory and takes precedence over this generic artifact convention.
+
+## 8. Locks
+
+Locks are advisory files under `.omc/collaboration/locks/`.
+
+Use a lock when two agents might modify the same shared collaboration file at the same time.
+
+Recommended lock filename:
+
+```text
+resource-name.lock
+```
+
+Recommended lock content:
+
+```json
+{
+  "agent": "codex",
+  "resource": "state.json",
+  "created_at": "2026-05-30T00:00:00.000Z",
+  "reason": "Updating state after event append."
+}
+```
+
+Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
+
+## 9. Handoff Rules
+
+When handing work to the other agent:
+
+1. Write or update the task document.
+2. Write any supporting artifact needed for context.
+3. Append a `handoff_requested` event.
+4. Update `state.json` with the current task, status, active agent, and last event id.
+5. State the handoff clearly in the user-facing response when applicable.
+
+Handoffs should include concrete next actions, relevant file paths, and any known blockers.
+
+## 10. Completion Rules
+
+A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
+
+Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
+
+## 11. Readiness Signal
+
+Codex readiness is represented by both:
+
+- A `codex_ready` event in `events.jsonl`.
+- `.omc/collaboration/codex-ready.md`.
+
+Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
+
+## 12. Minimal Operating Checklist
+
+Before collaboration work:
+
+- Read `AGENTS.md` or `CLAUDE.md`, as applicable.
+- Read `.omc/collaboration/protocol.md`.
+- Inspect `state.json` and recent `events.jsonl` entries.
+
+During collaboration work:
+
+- Keep edits scoped to the task.
+- Preserve append-only event history.
+- Keep shared JSON valid.
+- Create durable artifacts for decisions that must survive chat context.
+
+After collaboration work:
+
+- Append the relevant event.
+- Update `state.json`.
+- Verify changed files.
+- Report completed items and any remaining risk.
diff --git a/.omc/collaboration/state.json b/.omc/collaboration/state.json
index 8bb3c6cdb1f9fa26ff0bf1461955b09fa865fcd8..cd54728b42f70c14c107993b869b9af2fdf5da79
--- a/.omc/collaboration/state.json
+++ b/.omc/collaboration/state.json
@@ -2,7 +2,7 @@
   "workflow_id": "claude-codex-collab-mvp",
   "current_task": null,
   "active_agent": "none",
-  "status": "initialized",
-  "last_event_id": 0,
-  "updated_at": "2026-05-30T07:55:52.342Z"
+  "status": "codex_ready",
+  "last_event_id": 1,
+  "updated_at": "2026-05-30T07:57:25.000Z"
 }
diff --git a/AGENTS.md b/AGENTS.md
index dff45f359d65fc63ff972d7f5caf24b6070a0dac..72a8b712798d84d6e47fb68909cbe2d595d68ebf
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -3,6 +3,8 @@
 ## Mandatory Project Rules
 
 - For every shell command in this project, follow `/home/caohui/.codex/RTK.md`.
+- When participating in the Claude-Codex collaboration workflow, read and follow `.omc/collaboration/protocol.md` before acting. Treat it as the project-local contract for task execution, artifact generation, event logging, and shared state management.
 - Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.
 - If `docs/codex-review-protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.
 - Do not treat review-protocol steps as optional when the user requests a formal review or rule-governed Codex discussion.
+- If `.omc/collaboration/protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.

codex
内容复读正常；刚才 JSON 校验命令里环境没有 `python` 可执行名，我会用 `python3` 重新跑校验。
exec
/bin/bash -lc 'rtk git diff -- AGENTS.md .omc/collaboration/protocol.md .omc/collaboration/state.json .omc/collaboration/events.jsonl .omc/collaboration/codex-ready.md' in /home/caohui/projects/graduation-leave-system
 exited 128 in 0ms:
fatal: bad revision 'AGENTS.md'

exec
/bin/bash -lc "rtk python3 -c \"import json,pathlib; [json.loads(line) for line in pathlib.Path('.omc/collaboration/events.jsonl').read_text().splitlines() if line.strip()]; print('events.jsonl ok')\"" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
events.jsonl ok

exec
/bin/bash -lc 'rtk python3 -m json.tool .omc/collaboration/state.json' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
{
    "workflow_id": "claude-codex-collab-mvp",
    "current_task": null,
    "active_agent": "none",
    "status": "codex_ready",
    "last_event_id": 1,
    "updated_at": "2026-05-30T07:57:25.000Z"
}

diff --git a/.omc/collaboration/codex-ready.md b/.omc/collaboration/codex-ready.md
new file mode 100644
index 0000000000000000000000000000000000000000..3d85f283fdaeb2d363aecc01ea11addd758d58e4
--- /dev/null
+++ b/.omc/collaboration/codex-ready.md
@@ -0,0 +1,16 @@
+# Codex Ready
+
+Status: ready
+Agent: codex
+Timestamp: 2026-05-30T07:57:25.000Z
+Event: codex_ready
+Event ID: 1
+
+Codex-side collaboration configuration is complete.
+
+Completed items:
+
+- Updated `AGENTS.md` with the collaboration protocol entry rule.
+- Created `.omc/collaboration/protocol.md` with the shared protocol specification.
+- Wrote the `codex_ready` event to `.omc/collaboration/events.jsonl`.
+- Updated `.omc/collaboration/state.json` to reflect `codex_ready`.
diff --git a/.omc/collaboration/events.jsonl b/.omc/collaboration/events.jsonl
index e69de29bb2d1d6434b8b29ae775ad8c2e48c5391..d2f79e2115e8e4718cb7eb731b4a8308dd20e965
--- a/.omc/collaboration/events.jsonl
+++ b/.omc/collaboration/events.jsonl
@@ -0,0 +1 @@
+{"id":1,"type":"codex_ready","agent":"codex","timestamp":"2026-05-30T07:57:25.000Z","summary":"Codex collaboration configuration completed and ready for Claude-Codex workflow.","artifacts":["AGENTS.md",".omc/collaboration/protocol.md",".omc/collaboration/codex-ready.md"],"status":"codex_ready"}
diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
new file mode 100644
index 0000000000000000000000000000000000000000..a831acc3f4534a3d2c3a48ce4720292ccf968809
--- /dev/null
+++ b/.omc/collaboration/protocol.md
@@ -0,0 +1,212 @@
+# Claude-Codex Collaboration Protocol
+
+Version: 0.1
+Status: active
+Owner: Claude + Codex
+
+## 1. Purpose
+
+This protocol defines the shared operating contract for Claude-Codex collaboration in this repository. It covers task handoff, shared state, event logging, artifact creation, lock usage, and completion signaling.
+
+Agents must read this file before participating in the collaboration workflow.
+
+## 2. Directory Layout
+
+All collaboration files live under `.omc/collaboration/`.
+
+- `protocol.md`: this protocol.
+- `state.json`: current shared workflow state.
+- `events.jsonl`: append-only event log.
+- `tasks/`: task specifications and task handoff documents.
+- `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
+- `locks/`: advisory lock files for serialized work.
+- `codex-ready.md`: Codex readiness signal.
+
+## 3. Authority And Conflicts
+
+This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
+
+If a conflict is encountered, the active agent must follow the higher-priority instruction and record the conflict in its response or task artifact when material to the collaboration.
+
+Codex-specific repository rules in `AGENTS.md` remain mandatory. Claude-specific repository rules in `CLAUDE.md` remain mandatory.
+
+## 4. Shared State
+
+`state.json` is the latest compact state snapshot. It must remain valid JSON.
+
+Recommended schema:
+
+```json
+{
+  "workflow_id": "claude-codex-collab-mvp",
+  "current_task": null,
+  "active_agent": "none",
+  "status": "initialized",
+  "last_event_id": 0,
+  "updated_at": "2026-05-30T00:00:00.000Z"
+}
+```
+
+Field meanings:
+
+- `workflow_id`: stable collaboration workflow identifier.
+- `current_task`: active task id or `null`.
+- `active_agent`: `claude`, `codex`, or `none`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `last_event_id`: numeric id of the last event written to `events.jsonl`.
+- `updated_at`: UTC ISO-8601 timestamp for the state update.
+
+State updates should be minimal and should not replace durable task or artifact content.
+
+## 5. Event Log
+
+`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+
+Required event fields:
+
+```json
+{
+  "id": 1,
+  "type": "codex_ready",
+  "agent": "codex",
+  "timestamp": "2026-05-30T00:00:00.000Z",
+  "summary": "Short event summary."
+}
+```
+
+Recommended optional fields:
+
+- `task_id`: related task id.
+- `artifacts`: array of artifact paths.
+- `status`: resulting workflow status.
+- `details`: compact structured metadata.
+
+Event id rules:
+
+- Start at `1`.
+- Increment by `1` for every new event.
+- After writing an event, update `state.json.last_event_id` to the new id.
+
+Common event types:
+
+- `claude_ready`
+- `codex_ready`
+- `task_created`
+- `task_claimed`
+- `artifact_created`
+- `handoff_requested`
+- `review_requested`
+- `blocked`
+- `completed`
+
+## 6. Tasks
+
+Task documents belong in `.omc/collaboration/tasks/`.
+
+Recommended task filename:
+
+```text
+TASK-YYYYMMDD-NN-short-name.md
+```
+
+Recommended task content:
+
+- Task id.
+- Owner or requesting agent.
+- Objective.
+- Scope.
+- Inputs and relevant files.
+- Expected outputs.
+- Constraints and mandatory rules.
+- Acceptance criteria.
+- Current status.
+
+When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+
+## 7. Artifacts
+
+Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
+
+Artifacts should be durable and self-contained enough for the other agent to continue work without relying on chat history.
+
+Recommended artifact filenames:
+
+```text
+YYYYMMDD-HHMM-agent-topic.md
+```
+
+For formal Codex review or OMC `/ask codex` workflows, the repository's `docs/codex-review-protocol.md` remains mandatory and takes precedence over this generic artifact convention.
+
+## 8. Locks
+
+Locks are advisory files under `.omc/collaboration/locks/`.
+
+Use a lock when two agents might modify the same shared collaboration file at the same time.
+
+Recommended lock filename:
+
+```text
+resource-name.lock
+```
+
+Recommended lock content:
+
+```json
+{
+  "agent": "codex",
+  "resource": "state.json",
+  "created_at": "2026-05-30T00:00:00.000Z",
+  "reason": "Updating state after event append."
+}
+```
+
+Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
+
+## 9. Handoff Rules
+
+When handing work to the other agent:
+
+1. Write or update the task document.
+2. Write any supporting artifact needed for context.
+3. Append a `handoff_requested` event.
+4. Update `state.json` with the current task, status, active agent, and last event id.
+5. State the handoff clearly in the user-facing response when applicable.
+
+Handoffs should include concrete next actions, relevant file paths, and any known blockers.
+
+## 10. Completion Rules
+
+A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
+
+Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
+
+## 11. Readiness Signal
+
+Codex readiness is represented by both:
+
+- A `codex_ready` event in `events.jsonl`.
+- `.omc/collaboration/codex-ready.md`.
+
+Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
+
+## 12. Minimal Operating Checklist
+
+Before collaboration work:
+
+- Read `AGENTS.md` or `CLAUDE.md`, as applicable.
+- Read `.omc/collaboration/protocol.md`.
+- Inspect `state.json` and recent `events.jsonl` entries.
+
+During collaboration work:
+
+- Keep edits scoped to the task.
+- Preserve append-only event history.
+- Keep shared JSON valid.
+- Create durable artifacts for decisions that must survive chat context.
+
+After collaboration work:
+
+- Append the relevant event.
+- Update `state.json`.
+- Verify changed files.
+- Report completed items and any remaining risk.
diff --git a/.omc/collaboration/state.json b/.omc/collaboration/state.json
index 8bb3c6cdb1f9fa26ff0bf1461955b09fa865fcd8..cd54728b42f70c14c107993b869b9af2fdf5da79
--- a/.omc/collaboration/state.json
+++ b/.omc/collaboration/state.json
@@ -2,7 +2,7 @@
   "workflow_id": "claude-codex-collab-mvp",
   "current_task": null,
   "active_agent": "none",
-  "status": "initialized",
-  "last_event_id": 0,
-  "updated_at": "2026-05-30T07:55:52.342Z"
+  "status": "codex_ready",
+  "last_event_id": 1,
+  "updated_at": "2026-05-30T07:57:25.000Z"
 }
diff --git a/AGENTS.md b/AGENTS.md
index dff45f359d65fc63ff972d7f5caf24b6070a0dac..72a8b712798d84d6e47fb68909cbe2d595d68ebf
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -3,6 +3,8 @@
 ## Mandatory Project Rules
 
 - For every shell command in this project, follow `/home/caohui/.codex/RTK.md`.
+- When participating in the Claude-Codex collaboration workflow, read and follow `.omc/collaboration/protocol.md` before acting. Treat it as the project-local contract for task execution, artifact generation, event logging, and shared state management.
 - Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.
 - If `docs/codex-review-protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.
 - Do not treat review-protocol steps as optional when the user requests a formal review or rule-governed Codex discussion.
+- If `.omc/collaboration/protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.

codex
JSON 校验已经通过。`rtk git diff -- ...` 这条被代理解析成了错误参数形式，我会改用单文件状态和普通 diff 方式确认变更清单。
exec
/bin/bash -lc 'rtk git diff AGENTS.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
AGENTS.md | 2 ++
 1 file changed, 2 insertions(+)

--- Changes ---

AGENTS.md
  @@ -3,6 +3,8 @@
  +- When participating in the Claude-Codex collaboration workflow, read and follow `.omc/collaboration/protocol.md` before acting. Treat it as the project-local contract for task execution, artifact generation, event logging, and shared state management.
   - Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.
   - If `docs/codex-review-protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.
   - Do not treat review-protocol steps as optional when the user requests a formal review or rule-governed Codex discussion.
  +- If `.omc/collaboration/protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.
  +2 -0

exec
/bin/bash -lc 'rtk git status --short AGENTS.md .omc/collaboration' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
 M AGENTS.md
?? .omc/collaboration/
diff --git a/.omc/collaboration/codex-ready.md b/.omc/collaboration/codex-ready.md
new file mode 100644
index 0000000000000000000000000000000000000000..3d85f283fdaeb2d363aecc01ea11addd758d58e4
--- /dev/null
+++ b/.omc/collaboration/codex-ready.md
@@ -0,0 +1,16 @@
+# Codex Ready
+
+Status: ready
+Agent: codex
+Timestamp: 2026-05-30T07:57:25.000Z
+Event: codex_ready
+Event ID: 1
+
+Codex-side collaboration configuration is complete.
+
+Completed items:
+
+- Updated `AGENTS.md` with the collaboration protocol entry rule.
+- Created `.omc/collaboration/protocol.md` with the shared protocol specification.
+- Wrote the `codex_ready` event to `.omc/collaboration/events.jsonl`.
+- Updated `.omc/collaboration/state.json` to reflect `codex_ready`.
diff --git a/.omc/collaboration/events.jsonl b/.omc/collaboration/events.jsonl
index e69de29bb2d1d6434b8b29ae775ad8c2e48c5391..d2f79e2115e8e4718cb7eb731b4a8308dd20e965
--- a/.omc/collaboration/events.jsonl
+++ b/.omc/collaboration/events.jsonl
@@ -0,0 +1 @@
+{"id":1,"type":"codex_ready","agent":"codex","timestamp":"2026-05-30T07:57:25.000Z","summary":"Codex collaboration configuration completed and ready for Claude-Codex workflow.","artifacts":["AGENTS.md",".omc/collaboration/protocol.md",".omc/collaboration/codex-ready.md"],"status":"codex_ready"}
diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
new file mode 100644
index 0000000000000000000000000000000000000000..a831acc3f4534a3d2c3a48ce4720292ccf968809
--- /dev/null
+++ b/.omc/collaboration/protocol.md
@@ -0,0 +1,212 @@
+# Claude-Codex Collaboration Protocol
+
+Version: 0.1
+Status: active
+Owner: Claude + Codex
+
+## 1. Purpose
+
+This protocol defines the shared operating contract for Claude-Codex collaboration in this repository. It covers task handoff, shared state, event logging, artifact creation, lock usage, and completion signaling.
+
+Agents must read this file before participating in the collaboration workflow.
+
+## 2. Directory Layout
+
+All collaboration files live under `.omc/collaboration/`.
+
+- `protocol.md`: this protocol.
+- `state.json`: current shared workflow state.
+- `events.jsonl`: append-only event log.
+- `tasks/`: task specifications and task handoff documents.
+- `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
+- `locks/`: advisory lock files for serialized work.
+- `codex-ready.md`: Codex readiness signal.
+
+## 3. Authority And Conflicts
+
+This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
+
+If a conflict is encountered, the active agent must follow the higher-priority instruction and record the conflict in its response or task artifact when material to the collaboration.
+
+Codex-specific repository rules in `AGENTS.md` remain mandatory. Claude-specific repository rules in `CLAUDE.md` remain mandatory.
+
+## 4. Shared State
+
+`state.json` is the latest compact state snapshot. It must remain valid JSON.
+
+Recommended schema:
+
+```json
+{
+  "workflow_id": "claude-codex-collab-mvp",
+  "current_task": null,
+  "active_agent": "none",
+  "status": "initialized",
+  "last_event_id": 0,
+  "updated_at": "2026-05-30T00:00:00.000Z"
+}
+```
+
+Field meanings:
+
+- `workflow_id`: stable collaboration workflow identifier.
+- `current_task`: active task id or `null`.
+- `active_agent`: `claude`, `codex`, or `none`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `last_event_id`: numeric id of the last event written to `events.jsonl`.
+- `updated_at`: UTC ISO-8601 timestamp for the state update.
+
+State updates should be minimal and should not replace durable task or artifact content.
+
+## 5. Event Log
+
+`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+
+Required event fields:
+
+```json
+{
+  "id": 1,
+  "type": "codex_ready",
+  "agent": "codex",
+  "timestamp": "2026-05-30T00:00:00.000Z",
+  "summary": "Short event summary."
+}
+```
+
+Recommended optional fields:
+
+- `task_id`: related task id.
+- `artifacts`: array of artifact paths.
+- `status`: resulting workflow status.
+- `details`: compact structured metadata.
+
+Event id rules:
+
+- Start at `1`.
+- Increment by `1` for every new event.
+- After writing an event, update `state.json.last_event_id` to the new id.
+
+Common event types:
+
+- `claude_ready`
+- `codex_ready`
+- `task_created`
+- `task_claimed`
+- `artifact_created`
+- `handoff_requested`
+- `review_requested`
+- `blocked`
+- `completed`
+
+## 6. Tasks
+
+Task documents belong in `.omc/collaboration/tasks/`.
+
+Recommended task filename:
+
+```text
+TASK-YYYYMMDD-NN-short-name.md
+```
+
+Recommended task content:
+
+- Task id.
+- Owner or requesting agent.
+- Objective.
+- Scope.
+- Inputs and relevant files.
+- Expected outputs.
+- Constraints and mandatory rules.
+- Acceptance criteria.
+- Current status.
+
+When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+
+## 7. Artifacts
+
+Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
+
+Artifacts should be durable and self-contained enough for the other agent to continue work without relying on chat history.
+
+Recommended artifact filenames:
+
+```text
+YYYYMMDD-HHMM-agent-topic.md
+```
+
+For formal Codex review or OMC `/ask codex` workflows, the repository's `docs/codex-review-protocol.md` remains mandatory and takes precedence over this generic artifact convention.
+
+## 8. Locks
+
+Locks are advisory files under `.omc/collaboration/locks/`.
+
+Use a lock when two agents might modify the same shared collaboration file at the same time.
+
+Recommended lock filename:
+
+```text
+resource-name.lock
+```
+
+Recommended lock content:
+
+```json
+{
+  "agent": "codex",
+  "resource": "state.json",
+  "created_at": "2026-05-30T00:00:00.000Z",
+  "reason": "Updating state after event append."
+}
+```
+
+Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
+
+## 9. Handoff Rules
+
+When handing work to the other agent:
+
+1. Write or update the task document.
+2. Write any supporting artifact needed for context.
+3. Append a `handoff_requested` event.
+4. Update `state.json` with the current task, status, active agent, and last event id.
+5. State the handoff clearly in the user-facing response when applicable.
+
+Handoffs should include concrete next actions, relevant file paths, and any known blockers.
+
+## 10. Completion Rules
+
+A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
+
+Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
+
+## 11. Readiness Signal
+
+Codex readiness is represented by both:
+
+- A `codex_ready` event in `events.jsonl`.
+- `.omc/collaboration/codex-ready.md`.
+
+Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
+
+## 12. Minimal Operating Checklist
+
+Before collaboration work:
+
+- Read `AGENTS.md` or `CLAUDE.md`, as applicable.
+- Read `.omc/collaboration/protocol.md`.
+- Inspect `state.json` and recent `events.jsonl` entries.
+
+During collaboration work:
+
+- Keep edits scoped to the task.
+- Preserve append-only event history.
+- Keep shared JSON valid.
+- Create durable artifacts for decisions that must survive chat context.
+
+After collaboration work:
+
+- Append the relevant event.
+- Update `state.json`.
+- Verify changed files.
+- Report completed items and any remaining risk.
diff --git a/.omc/collaboration/state.json b/.omc/collaboration/state.json
index 8bb3c6cdb1f9fa26ff0bf1461955b09fa865fcd8..cd54728b42f70c14c107993b869b9af2fdf5da79
--- a/.omc/collaboration/state.json
+++ b/.omc/collaboration/state.json
@@ -2,7 +2,7 @@
   "workflow_id": "claude-codex-collab-mvp",
   "current_task": null,
   "active_agent": "none",
-  "status": "initialized",
-  "last_event_id": 0,
-  "updated_at": "2026-05-30T07:55:52.342Z"
+  "status": "codex_ready",
+  "last_event_id": 1,
+  "updated_at": "2026-05-30T07:57:25.000Z"
 }
diff --git a/AGENTS.md b/AGENTS.md
index dff45f359d65fc63ff972d7f5caf24b6070a0dac..72a8b712798d84d6e47fb68909cbe2d595d68ebf
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -3,6 +3,8 @@
 ## Mandatory Project Rules
 
 - For every shell command in this project, follow `/home/caohui/.codex/RTK.md`.
+- When participating in the Claude-Codex collaboration workflow, read and follow `.omc/collaboration/protocol.md` before acting. Treat it as the project-local contract for task execution, artifact generation, event logging, and shared state management.
 - Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.
 - If `docs/codex-review-protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.
 - Do not treat review-protocol steps as optional when the user requests a formal review or rule-governed Codex discussion.
+- If `.omc/collaboration/protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.

exec
/bin/bash -lc 'rtk ls -la .omc/collaboration' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
artifacts/
locks/
tasks/
codex-ready.md  468B
events.jsonl  296B
protocol.md  6.1K
state.json  190B

diff --git a/.omc/collaboration/codex-ready.md b/.omc/collaboration/codex-ready.md
new file mode 100644
index 0000000000000000000000000000000000000000..3d85f283fdaeb2d363aecc01ea11addd758d58e4
--- /dev/null
+++ b/.omc/collaboration/codex-ready.md
@@ -0,0 +1,16 @@
+# Codex Ready
+
+Status: ready
+Agent: codex
+Timestamp: 2026-05-30T07:57:25.000Z
+Event: codex_ready
+Event ID: 1
+
+Codex-side collaboration configuration is complete.
+
+Completed items:
+
+- Updated `AGENTS.md` with the collaboration protocol entry rule.
+- Created `.omc/collaboration/protocol.md` with the shared protocol specification.
+- Wrote the `codex_ready` event to `.omc/collaboration/events.jsonl`.
+- Updated `.omc/collaboration/state.json` to reflect `codex_ready`.
diff --git a/.omc/collaboration/events.jsonl b/.omc/collaboration/events.jsonl
index e69de29bb2d1d6434b8b29ae775ad8c2e48c5391..d2f79e2115e8e4718cb7eb731b4a8308dd20e965
--- a/.omc/collaboration/events.jsonl
+++ b/.omc/collaboration/events.jsonl
@@ -0,0 +1 @@
+{"id":1,"type":"codex_ready","agent":"codex","timestamp":"2026-05-30T07:57:25.000Z","summary":"Codex collaboration configuration completed and ready for Claude-Codex workflow.","artifacts":["AGENTS.md",".omc/collaboration/protocol.md",".omc/collaboration/codex-ready.md"],"status":"codex_ready"}
diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
new file mode 100644
index 0000000000000000000000000000000000000000..a831acc3f4534a3d2c3a48ce4720292ccf968809
--- /dev/null
+++ b/.omc/collaboration/protocol.md
@@ -0,0 +1,212 @@
+# Claude-Codex Collaboration Protocol
+
+Version: 0.1
+Status: active
+Owner: Claude + Codex
+
+## 1. Purpose
+
+This protocol defines the shared operating contract for Claude-Codex collaboration in this repository. It covers task handoff, shared state, event logging, artifact creation, lock usage, and completion signaling.
+
+Agents must read this file before participating in the collaboration workflow.
+
+## 2. Directory Layout
+
+All collaboration files live under `.omc/collaboration/`.
+
+- `protocol.md`: this protocol.
+- `state.json`: current shared workflow state.
+- `events.jsonl`: append-only event log.
+- `tasks/`: task specifications and task handoff documents.
+- `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
+- `locks/`: advisory lock files for serialized work.
+- `codex-ready.md`: Codex readiness signal.
+
+## 3. Authority And Conflicts
+
+This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
+
+If a conflict is encountered, the active agent must follow the higher-priority instruction and record the conflict in its response or task artifact when material to the collaboration.
+
+Codex-specific repository rules in `AGENTS.md` remain mandatory. Claude-specific repository rules in `CLAUDE.md` remain mandatory.
+
+## 4. Shared State
+
+`state.json` is the latest compact state snapshot. It must remain valid JSON.
+
+Recommended schema:
+
+```json
+{
+  "workflow_id": "claude-codex-collab-mvp",
+  "current_task": null,
+  "active_agent": "none",
+  "status": "initialized",
+  "last_event_id": 0,
+  "updated_at": "2026-05-30T00:00:00.000Z"
+}
+```
+
+Field meanings:
+
+- `workflow_id`: stable collaboration workflow identifier.
+- `current_task`: active task id or `null`.
+- `active_agent`: `claude`, `codex`, or `none`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `last_event_id`: numeric id of the last event written to `events.jsonl`.
+- `updated_at`: UTC ISO-8601 timestamp for the state update.
+
+State updates should be minimal and should not replace durable task or artifact content.
+
+## 5. Event Log
+
+`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+
+Required event fields:
+
+```json
+{
+  "id": 1,
+  "type": "codex_ready",
+  "agent": "codex",
+  "timestamp": "2026-05-30T00:00:00.000Z",
+  "summary": "Short event summary."
+}
+```
+
+Recommended optional fields:
+
+- `task_id`: related task id.
+- `artifacts`: array of artifact paths.
+- `status`: resulting workflow status.
+- `details`: compact structured metadata.
+
+Event id rules:
+
+- Start at `1`.
+- Increment by `1` for every new event.
+- After writing an event, update `state.json.last_event_id` to the new id.
+
+Common event types:
+
+- `claude_ready`
+- `codex_ready`
+- `task_created`
+- `task_claimed`
+- `artifact_created`
+- `handoff_requested`
+- `review_requested`
+- `blocked`
+- `completed`
+
+## 6. Tasks
+
+Task documents belong in `.omc/collaboration/tasks/`.
+
+Recommended task filename:
+
+```text
+TASK-YYYYMMDD-NN-short-name.md
+```
+
+Recommended task content:
+
+- Task id.
+- Owner or requesting agent.
+- Objective.
+- Scope.
+- Inputs and relevant files.
+- Expected outputs.
+- Constraints and mandatory rules.
+- Acceptance criteria.
+- Current status.
+
+When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+
+## 7. Artifacts
+
+Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
+
+Artifacts should be durable and self-contained enough for the other agent to continue work without relying on chat history.
+
+Recommended artifact filenames:
+
+```text
+YYYYMMDD-HHMM-agent-topic.md
+```
+
+For formal Codex review or OMC `/ask codex` workflows, the repository's `docs/codex-review-protocol.md` remains mandatory and takes precedence over this generic artifact convention.
+
+## 8. Locks
+
+Locks are advisory files under `.omc/collaboration/locks/`.
+
+Use a lock when two agents might modify the same shared collaboration file at the same time.
+
+Recommended lock filename:
+
+```text
+resource-name.lock
+```
+
+Recommended lock content:
+
+```json
+{
+  "agent": "codex",
+  "resource": "state.json",
+  "created_at": "2026-05-30T00:00:00.000Z",
+  "reason": "Updating state after event append."
+}
+```
+
+Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
+
+## 9. Handoff Rules
+
+When handing work to the other agent:
+
+1. Write or update the task document.
+2. Write any supporting artifact needed for context.
+3. Append a `handoff_requested` event.
+4. Update `state.json` with the current task, status, active agent, and last event id.
+5. State the handoff clearly in the user-facing response when applicable.
+
+Handoffs should include concrete next actions, relevant file paths, and any known blockers.
+
+## 10. Completion Rules
+
+A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
+
+Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
+
+## 11. Readiness Signal
+
+Codex readiness is represented by both:
+
+- A `codex_ready` event in `events.jsonl`.
+- `.omc/collaboration/codex-ready.md`.
+
+Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
+
+## 12. Minimal Operating Checklist
+
+Before collaboration work:
+
+- Read `AGENTS.md` or `CLAUDE.md`, as applicable.
+- Read `.omc/collaboration/protocol.md`.
+- Inspect `state.json` and recent `events.jsonl` entries.
+
+During collaboration work:
+
+- Keep edits scoped to the task.
+- Preserve append-only event history.
+- Keep shared JSON valid.
+- Create durable artifacts for decisions that must survive chat context.
+
+After collaboration work:
+
+- Append the relevant event.
+- Update `state.json`.
+- Verify changed files.
+- Report completed items and any remaining risk.
diff --git a/.omc/collaboration/state.json b/.omc/collaboration/state.json
index 8bb3c6cdb1f9fa26ff0bf1461955b09fa865fcd8..cd54728b42f70c14c107993b869b9af2fdf5da79
--- a/.omc/collaboration/state.json
+++ b/.omc/collaboration/state.json
@@ -2,7 +2,7 @@
   "workflow_id": "claude-codex-collab-mvp",
   "current_task": null,
   "active_agent": "none",
-  "status": "initialized",
-  "last_event_id": 0,
-  "updated_at": "2026-05-30T07:55:52.342Z"
+  "status": "codex_ready",
+  "last_event_id": 1,
+  "updated_at": "2026-05-30T07:57:25.000Z"
 }
diff --git a/AGENTS.md b/AGENTS.md
index dff45f359d65fc63ff972d7f5caf24b6070a0dac..72a8b712798d84d6e47fb68909cbe2d595d68ebf
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -3,6 +3,8 @@
 ## Mandatory Project Rules
 
 - For every shell command in this project, follow `/home/caohui/.codex/RTK.md`.
+- When participating in the Claude-Codex collaboration workflow, read and follow `.omc/collaboration/protocol.md` before acting. Treat it as the project-local contract for task execution, artifact generation, event logging, and shared state management.
 - Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.
 - If `docs/codex-review-protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.
 - Do not treat review-protocol steps as optional when the user requests a formal review or rule-governed Codex discussion.
+- If `.omc/collaboration/protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.

codex
已按清单完成 Codex 侧配置：

1. 更新 [AGENTS.md](/home/caohui/projects/graduation-leave-system/AGENTS.md:6)
   已添加 Claude-Codex 协作协议入口规则，并补充协议冲突处理规则。

2. 创建 [.omc/collaboration/protocol.md](/home/caohui/projects/graduation-leave-system/.omc/collaboration/protocol.md:1)
   已写入完整协议规范，包含目录结构、共享状态、事件日志、任务、产物、锁、交接、完成和 ready 信号规则。

3. 写 ready 信号
   已创建 [.omc/collaboration/codex-ready.md](/home/caohui/projects/graduation-leave-system/.omc/collaboration/codex-ready.md:1)，并在 [.omc/collaboration/events.jsonl](/home/caohui/projects/graduation-leave-system/.omc/collaboration/events.jsonl:1) 写入 `codex_ready` 事件。  
   同时已更新 [.omc/collaboration/state.json](/home/caohui/projects/graduation-leave-system/.omc/collaboration/state.json:1)：`status` 为 `codex_ready`，`last_event_id` 为 `1`。

校验已完成：`state.json` JSON 有效，`events.jsonl` 可逐行解析。
diff --git a/.omc/collaboration/codex-ready.md b/.omc/collaboration/codex-ready.md
new file mode 100644
index 0000000000000000000000000000000000000000..3d85f283fdaeb2d363aecc01ea11addd758d58e4
--- /dev/null
+++ b/.omc/collaboration/codex-ready.md
@@ -0,0 +1,16 @@
+# Codex Ready
+
+Status: ready
+Agent: codex
+Timestamp: 2026-05-30T07:57:25.000Z
+Event: codex_ready
+Event ID: 1
+
+Codex-side collaboration configuration is complete.
+
+Completed items:
+
+- Updated `AGENTS.md` with the collaboration protocol entry rule.
+- Created `.omc/collaboration/protocol.md` with the shared protocol specification.
+- Wrote the `codex_ready` event to `.omc/collaboration/events.jsonl`.
+- Updated `.omc/collaboration/state.json` to reflect `codex_ready`.
diff --git a/.omc/collaboration/events.jsonl b/.omc/collaboration/events.jsonl
index e69de29bb2d1d6434b8b29ae775ad8c2e48c5391..d2f79e2115e8e4718cb7eb731b4a8308dd20e965
--- a/.omc/collaboration/events.jsonl
+++ b/.omc/collaboration/events.jsonl
@@ -0,0 +1 @@
+{"id":1,"type":"codex_ready","agent":"codex","timestamp":"2026-05-30T07:57:25.000Z","summary":"Codex collaboration configuration completed and ready for Claude-Codex workflow.","artifacts":["AGENTS.md",".omc/collaboration/protocol.md",".omc/collaboration/codex-ready.md"],"status":"codex_ready"}
diff --git a/.omc/collaboration/protocol.md b/.omc/collaboration/protocol.md
new file mode 100644
index 0000000000000000000000000000000000000000..a831acc3f4534a3d2c3a48ce4720292ccf968809
--- /dev/null
+++ b/.omc/collaboration/protocol.md
@@ -0,0 +1,212 @@
+# Claude-Codex Collaboration Protocol
+
+Version: 0.1
+Status: active
+Owner: Claude + Codex
+
+## 1. Purpose
+
+This protocol defines the shared operating contract for Claude-Codex collaboration in this repository. It covers task handoff, shared state, event logging, artifact creation, lock usage, and completion signaling.
+
+Agents must read this file before participating in the collaboration workflow.
+
+## 2. Directory Layout
+
+All collaboration files live under `.omc/collaboration/`.
+
+- `protocol.md`: this protocol.
+- `state.json`: current shared workflow state.
+- `events.jsonl`: append-only event log.
+- `tasks/`: task specifications and task handoff documents.
+- `artifacts/`: generated outputs, reviews, summaries, and other durable work products.
+- `locks/`: advisory lock files for serialized work.
+- `codex-ready.md`: Codex readiness signal.
+
+## 3. Authority And Conflicts
+
+This protocol is project-local. Higher-priority system, developer, repository, and direct user instructions override it.
+
+If a conflict is encountered, the active agent must follow the higher-priority instruction and record the conflict in its response or task artifact when material to the collaboration.
+
+Codex-specific repository rules in `AGENTS.md` remain mandatory. Claude-specific repository rules in `CLAUDE.md` remain mandatory.
+
+## 4. Shared State
+
+`state.json` is the latest compact state snapshot. It must remain valid JSON.
+
+Recommended schema:
+
+```json
+{
+  "workflow_id": "claude-codex-collab-mvp",
+  "current_task": null,
+  "active_agent": "none",
+  "status": "initialized",
+  "last_event_id": 0,
+  "updated_at": "2026-05-30T00:00:00.000Z"
+}
+```
+
+Field meanings:
+
+- `workflow_id`: stable collaboration workflow identifier.
+- `current_task`: active task id or `null`.
+- `active_agent`: `claude`, `codex`, or `none`.
+- `status`: compact workflow status such as `initialized`, `codex_ready`, `task_open`, `in_progress`, `blocked`, `completed`.
+- `last_event_id`: numeric id of the last event written to `events.jsonl`.
+- `updated_at`: UTC ISO-8601 timestamp for the state update.
+
+State updates should be minimal and should not replace durable task or artifact content.
+
+## 5. Event Log
+
+`events.jsonl` is append-only. Each line is one valid JSON object. Do not rewrite previous events unless the user explicitly requests repair of a malformed log.
+
+Required event fields:
+
+```json
+{
+  "id": 1,
+  "type": "codex_ready",
+  "agent": "codex",
+  "timestamp": "2026-05-30T00:00:00.000Z",
+  "summary": "Short event summary."
+}
+```
+
+Recommended optional fields:
+
+- `task_id`: related task id.
+- `artifacts`: array of artifact paths.
+- `status`: resulting workflow status.
+- `details`: compact structured metadata.
+
+Event id rules:
+
+- Start at `1`.
+- Increment by `1` for every new event.
+- After writing an event, update `state.json.last_event_id` to the new id.
+
+Common event types:
+
+- `claude_ready`
+- `codex_ready`
+- `task_created`
+- `task_claimed`
+- `artifact_created`
+- `handoff_requested`
+- `review_requested`
+- `blocked`
+- `completed`
+
+## 6. Tasks
+
+Task documents belong in `.omc/collaboration/tasks/`.
+
+Recommended task filename:
+
+```text
+TASK-YYYYMMDD-NN-short-name.md
+```
+
+Recommended task content:
+
+- Task id.
+- Owner or requesting agent.
+- Objective.
+- Scope.
+- Inputs and relevant files.
+- Expected outputs.
+- Constraints and mandatory rules.
+- Acceptance criteria.
+- Current status.
+
+When claiming a task, the agent should write a `task_claimed` event and set `state.json.active_agent` and `state.json.current_task`.
+
+## 7. Artifacts
+
+Artifacts belong in `.omc/collaboration/artifacts/` unless another project rule requires a different path.
+
+Artifacts should be durable and self-contained enough for the other agent to continue work without relying on chat history.
+
+Recommended artifact filenames:
+
+```text
+YYYYMMDD-HHMM-agent-topic.md
+```
+
+For formal Codex review or OMC `/ask codex` workflows, the repository's `docs/codex-review-protocol.md` remains mandatory and takes precedence over this generic artifact convention.
+
+## 8. Locks
+
+Locks are advisory files under `.omc/collaboration/locks/`.
+
+Use a lock when two agents might modify the same shared collaboration file at the same time.
+
+Recommended lock filename:
+
+```text
+resource-name.lock
+```
+
+Recommended lock content:
+
+```json
+{
+  "agent": "codex",
+  "resource": "state.json",
+  "created_at": "2026-05-30T00:00:00.000Z",
+  "reason": "Updating state after event append."
+}
+```
+
+Remove locks after the protected write completes. If a stale lock is suspected, inspect its timestamp and coordinate through an event or user-visible response before overriding it.
+
+## 9. Handoff Rules
+
+When handing work to the other agent:
+
+1. Write or update the task document.
+2. Write any supporting artifact needed for context.
+3. Append a `handoff_requested` event.
+4. Update `state.json` with the current task, status, active agent, and last event id.
+5. State the handoff clearly in the user-facing response when applicable.
+
+Handoffs should include concrete next actions, relevant file paths, and any known blockers.
+
+## 10. Completion Rules
+
+A task is complete only when the requested files are written, verification appropriate to the change has been performed, and completion is reflected in the collaboration log when the task is part of this workflow.
+
+Completion should write a `completed` event and update `state.json.status` to `completed` unless the workflow remains open for the other agent.
+
+## 11. Readiness Signal
+
+Codex readiness is represented by both:
+
+- A `codex_ready` event in `events.jsonl`.
+- `.omc/collaboration/codex-ready.md`.
+
+Claude readiness may be represented similarly with `claude_ready` and a corresponding readiness artifact.
+
+## 12. Minimal Operating Checklist
+
+Before collaboration work:
+
+- Read `AGENTS.md` or `CLAUDE.md`, as applicable.
+- Read `.omc/collaboration/protocol.md`.
+- Inspect `state.json` and recent `events.jsonl` entries.
+
+During collaboration work:
+
+- Keep edits scoped to the task.
+- Preserve append-only event history.
+- Keep shared JSON valid.
+- Create durable artifacts for decisions that must survive chat context.
+
+After collaboration work:
+
+- Append the relevant event.
+- Update `state.json`.
+- Verify changed files.
+- Report completed items and any remaining risk.
diff --git a/.omc/collaboration/state.json b/.omc/collaboration/state.json
index 8bb3c6cdb1f9fa26ff0bf1461955b09fa865fcd8..cd54728b42f70c14c107993b869b9af2fdf5da79
--- a/.omc/collaboration/state.json
+++ b/.omc/collaboration/state.json
@@ -2,7 +2,7 @@
   "workflow_id": "claude-codex-collab-mvp",
   "current_task": null,
   "active_agent": "none",
-  "status": "initialized",
-  "last_event_id": 0,
-  "updated_at": "2026-05-30T07:55:52.342Z"
+  "status": "codex_ready",
+  "last_event_id": 1,
+  "updated_at": "2026-05-30T07:57:25.000Z"
 }
diff --git a/AGENTS.md b/AGENTS.md
index dff45f359d65fc63ff972d7f5caf24b6070a0dac..72a8b712798d84d6e47fb68909cbe2d595d68ebf
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -3,6 +3,8 @@
 ## Mandatory Project Rules
 
 - For every shell command in this project, follow `/home/caohui/.codex/RTK.md`.
+- When participating in the Claude-Codex collaboration workflow, read and follow `.omc/collaboration/protocol.md` before acting. Treat it as the project-local contract for task execution, artifact generation, event logging, and shared state management.
 - Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.
 - If `docs/codex-review-protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.
 - Do not treat review-protocol steps as optional when the user requests a formal review or rule-governed Codex discussion.
+- If `.omc/collaboration/protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.

tokens used
43,556

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
