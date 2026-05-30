# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-05-30T07:17:55.096Z

## Original task

规则固化方案讨论：你说跨会话需要把规则写入项目文件。具体问题：1) 应该写入哪个文件最合适？AGENTS.md、CODEX.md、还是新建docs/codex-review-protocol.md？2) 文件内容应该如何组织才能让你每次自动读取并遵守？3) 是否需要在文件开头添加特定标记（如Load Trigger）？4) 你启动时会自动读取哪些文件？5) 如果我们现在就创建这个文件，你能确认格式是否正确、是否能在下次会话中自动生效吗？请给出具体可执行的方案。

## Final prompt

规则固化方案讨论：你说跨会话需要把规则写入项目文件。具体问题：1) 应该写入哪个文件最合适？AGENTS.md、CODEX.md、还是新建docs/codex-review-protocol.md？2) 文件内容应该如何组织才能让你每次自动读取并遵守？3) 是否需要在文件开头添加特定标记（如Load Trigger）？4) 你启动时会自动读取哪些文件？5) 如果我们现在就创建这个文件，你能确认格式是否正确、是否能在下次会话中自动生效吗？请给出具体可执行的方案。

## Raw output

```text
最稳方案：**根目录 `AGENTS.md` 做自动入口，`docs/codex-review-protocol.md` 或现有 `docs/Codex审查流程指南.md` 存放完整规则**。

当前项目根目录实际没有 `AGENTS.md`，但本次会话上下文里注入了类似 `AGENTS.md` 的项目指令，并指向 `/home/caohui/.codex/RTK.md`。这说明自动入口机制存在，但项目文件缺失或由外部配置注入。为了跨会话稳定，建议现在补一个真实的根目录 `AGENTS.md`。

**1. 应该写入哪个文件？**

推荐结构：

```text
AGENTS.md                          # 自动入口，必须简短、强制、可加载
docs/codex-review-protocol.md      # 详细审查流程
```

不要只写 `docs/codex-review-protocol.md`，因为 docs 文件通常不会被自动读取。

不建议依赖 `CODEX.md`，除非你确认当前 Codex 运行器支持它。就本项目当前表现看，**`AGENTS.md` 是更可靠的入口名**。

`CLAUDE.md` 可以保留给 Claude，但不能假设 Codex 会自动遵守它。

**2. 文件内容如何组织？**

`AGENTS.md` 只放“必须加载哪些规则”的短指令，不放长流程。示例：

```markdown
# Project Agent Instructions

## Mandatory Project Rules

- For every shell command in this project, follow `/home/caohui/.codex/RTK.md`.
- Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.
- If `docs/codex-review-protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.
- Do not treat review-protocol steps as optional when the user requests a formal review or rule-governed Codex discussion.
```

`docs/codex-review-protocol.md` 再放完整流程：

```markdown
# Codex Review Protocol

## Load Trigger

Read this file before any of the following:
- Codex review
- document review
- architecture review
- database schema review
- API design review
- data integration review
- OMC `/ask codex` review workflow

## Required Workflow

...

## Output Format

...

## Verification Checklist

...
```

你现在已有 [docs/Codex审查流程指南.md](/home/caohui/projects/graduation-leave-system/docs/Codex审查流程指南.md)，内容里已经有 `Load Trigger`。可以继续用它，但我更建议复制或重命名为 ASCII 路径 `docs/codex-review-protocol.md`，减少工具、脚本、跨平台引用问题。

**3. 是否需要 Load Trigger？**

需要，但它本身不是魔法开关。

`Load Trigger` 只有在我已经读到这个文件后才有意义。真正让它生效的是根目录 `AGENTS.md` 里的这句：

```markdown
Before performing any Codex review..., read and follow `docs/codex-review-protocol.md`.
```

所以正确组合是：

```text
AGENTS.md 负责“自动入口”
Load Trigger 负责“读到文件后判断何时适用”
```

**4. 启动时会自动读取哪些文件？**

在当前 Codex 项目环境里，可靠假设是：

```text
系统/开发者指令
当前项目的 AGENTS.md 或等价注入的项目指令
AGENTS.md 中显式引用的文件
```

不能可靠假设会自动读取：

```text
CODEX.md
CLAUDE.md
docs/*.md
README.md
.omc/*
```

除非入口文件明确要求读取，或用户当前任务触发我主动查找。

**5. 现在创建后，能否确认下次自动生效？**

我可以确认两件事：

1. **格式是否正确**：可以创建后检查 `AGENTS.md` 是否位于项目根目录，引用路径是否存在，规则是否没有歧义。
2. **在当前机制下是否具备自动生效条件**：如果 Codex 下次从 `/home/caohui/projects/graduation-leave-system` 启动，并加载根目录 `AGENTS.md`，那它会自动生效。

我不能 100% 从当前会话证明“下一次启动器一定读取 `AGENTS.md`”，因为那取决于 Codex CLI/运行器加载策略。但从本次上下文已经出现 “AGENTS.md instructions for 当前项目” 来看，**这是最接近可验证、可固化的方案**。

具体执行建议：

```text
1. 新建根目录 AGENTS.md
2. 将现有 docs/Codex审查流程指南.md 复制或迁移为 docs/codex-review-protocol.md
3. AGENTS.md 用强制语气引用该协议文件
4. 可选：CLAUDE.md 也加同一条引用，保证 Claude/Codex 双端一致
5. 下次新会话启动后，问我“本项目审查规则入口是什么”，验证我是否能指出 AGENTS.md 和协议文件
```

如果你要现在固化，我建议采用：

```text
AGENTS.md
docs/codex-review-protocol.md
```

而不是只依赖 `CODEX.md` 或 docs 文件。


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
session id: 019e77be-27a4-7a23-ac64-985efa2ebfdd
--------
user
规则固化方案讨论：你说跨会话需要把规则写入项目文件。具体问题：1) 应该写入哪个文件最合适？AGENTS.md、CODEX.md、还是新建docs/codex-review-protocol.md？2) 文件内容应该如何组织才能让你每次自动读取并遵守？3) 是否需要在文件开头添加特定标记（如Load Trigger）？4) 你启动时会自动读取哪些文件？5) 如果我们现在就创建这个文件，你能确认格式是否正确、是否能在下次会话中自动生效吗？请给出具体可执行的方案。
codex
我先看一下当前项目的代理入口文件，这会决定“下次会话自动生效”的最稳位置。
exec
/bin/bash -lc "ls -la && printf '\\nAGENTS.md:\\n' && sed -n '1,160p' AGENTS.md && printf '\\nRTK head:\\n' && sed -n '1,120p' /home/caohui/.codex/RTK.md" in /home/caohui/projects/graduation-leave-system
 exited 2 in 0ms:
total 72
drwxrwxr-x 13 caohui caohui 4096 May 28 11:41 .
drwxrwxr-x  8 caohui caohui 4096 May 27 05:53 ..
drwxr-xr-x  2 caohui caohui 4096 May 27 06:55 .agents
drwxrwxr-x  3 caohui caohui 4096 May 30 11:06 .claude
drwxr-xr-x  2 caohui caohui 4096 May 27 06:55 .codex
drwxrwxr-x  7 caohui caohui 4096 May 30 14:20 .git
-rw-rw-r--  1 caohui caohui  664 May 27 06:09 .gitignore
drwxrwxr-x  5 caohui caohui 4096 May 30 15:12 .omc
-rw-rw-r--  1 caohui caohui 2634 May 28 11:41 CLAUDE.md
drwxrwxr-x  2 caohui caohui 4096 May 27 05:53 PRD
drwxrwxr-x  6 caohui caohui 4096 May 27 06:09 backend
drwxrwxr-x  4 caohui caohui 4096 May 27 06:09 docker
drwxrwxr-x  6 caohui caohui 4096 May 28 17:40 docs
drwxrwxr-x  4 caohui caohui 4096 May 27 06:09 frontend
drwxrwxr-x  2 caohui caohui 4096 May 27 07:27 plans
-rw-rw-r--  1 caohui caohui 8366 May 27 10:29 毕业离校系统用户文档.zip

AGENTS.md:
sed: can't read AGENTS.md: No such file or directory

codex
这里有一个关键事实：项目根目录当前没有 `AGENTS.md`，但会话上下文里确实注入了来自 `/home/caohui/projects/graduation-leave-system/AGENTS.md` 的指令。我要再确认 `.codex`、`.agents` 里是否已有等价入口，避免建议落到不会被加载的位置。
exec
/bin/bash -lc "sed -n '1,200p' /home/caohui/.codex/RTK.md" in /home/caohui/projects/graduation-leave-system
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

exec
/bin/bash -lc "find . -maxdepth 3 -type f | sort | sed -n '1,200p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
./.claude/settings.local.json
./.git/COMMIT_EDITMSG
./.git/HEAD
./.git/config
./.git/description
./.git/hooks/applypatch-msg.sample
./.git/hooks/commit-msg.sample
./.git/hooks/fsmonitor-watchman.sample
./.git/hooks/post-update.sample
./.git/hooks/pre-applypatch.sample
./.git/hooks/pre-commit.sample
./.git/hooks/pre-merge-commit.sample
./.git/hooks/pre-push.sample
./.git/hooks/pre-rebase.sample
./.git/hooks/pre-receive.sample
./.git/hooks/prepare-commit-msg.sample
./.git/hooks/push-to-checkout.sample
./.git/hooks/sendemail-validate.sample
./.git/hooks/update.sample
./.git/index
./.git/info/exclude
./.git/logs/HEAD
./.gitignore
./.omc/project-memory.json
./.omc/project-state.json
./.omc/session-context.json
./.omc/sessions/04a41b19-6f39-4d0e-8072-0f0d097dea01.json
./.omc/sessions/4aad264e-c3a4-460a-9be1-61247202bad3.json
./.omc/sessions/86656873-1778-4d8a-aeee-2ff5db229c98.json
./.omc/sessions/c4d9c5f4-fdb8-4176-8480-6aec0d7eaa87.json
./.omc/sessions/c8f47bca-464c-4b8c-bab5-42ba59354101.json
./.omc/sessions/cde0b835-f3fb-47de-af08-5d37887de1bb.json
./.omc/sessions/dcf39a3e-1b72-449a-9897-852c3c7f1253.json
./.omc/sessions/e2566739-aaa7-4701-9354-a710639ac308.json
./.omc/sessions/f91e1567-b1b2-4cc2-bd9b-355702bc1ec4.json
./.omc/state/agent-replay-7afec07d-3b40-4e4c-8f86-86e9dc0e791c.jsonl
./.omc/state/agent-replay-97c93024-a4c1-4e03-93bf-7522ce3517ff.jsonl
./.omc/state/hud-stdin-cache.json
./.omc/state/mission-state.json
./CLAUDE.md
./backend/requirements/base.txt
./backend/requirements/dev.txt
./backend/requirements/prod.txt
./docs/Codex审查流程指南.md
./docs/PROJECT-SUMMARY.md
./docs/design/2026-05-27-system-design.md
./docs/templates/学生基本信息导入模板.csv
./docs/templates/宿舍清退数据模板.csv
./docs/templates/班级辅导员对应关系导入模板.csv
./docs/templates/辅导员基本信息导入模板.csv
./docs/微信小程序备案说明.md
./docs/微信小程序申请说明.md
./docs/数据对接说明文档.md
./docs/数据对接说明文档.md.backup
./docs/数据确认清单.md
./docs/用户设计说明书.md
./毕业离校系统用户文档.zip

exec
/bin/bash -lc "find .codex .agents .claude -maxdepth 3 -type f -print -exec sed -n '1,80p' {} \\;" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
.claude/settings.local.json
{
  "permissions": {
    "allow": [
      "Bash(rtk wc *)",
      "Skill(codex:setup)",
      "Bash(rtk grep *)",
      "Bash(gh *)",
      "Bash(rtk git *)",
      "Bash(codex review *)",
      "Bash(rtk ls *)",
      "Bash(rtk read *)",
      "Bash(zip *)",
      "Bash(dufs *)",
      "Skill(codex:rescue)",
      "Bash(rtk ps *)",
      "Bash(omc ask *)",
      "Read(//tmp/**)",
      "Bash(rm -rf graduation-docs)",
      "Bash(mkdir -p graduation-docs/templates)",
      "Bash(cp \"docs/数据对接说明文档.md\" \"docs/用户设计说明书.md\" \"docs/数据确认清单.md\" /tmp/graduation-docs/)",
      "Bash(cp docs/templates/*.csv /tmp/graduation-docs/templates/)",
      "Bash(kill 1229060)",
      "Bash(codex --version)",
      "mcp__plugin_oh-my-claudecode_t__project_memory_add_directive",
      "Bash(lightpanda fetch *)",
      "Bash(node *)",
      "Bash(awk '{print $NF}')",
      "Bash(env)",
      "WebFetch(domain:interface-doc.goliveplus.cn)"
    ]
  }
}

codex
项目里已经有 `docs/Codex审查流程指南.md`，这可能正是你说的“审查规则”。我会读一下它的结构，再给出是否需要搬到入口文件、如何链接的建议。
exec
/bin/bash -lc "sed -n '1,240p' docs/Codex审查流程指南.md" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'git status --short' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
 M .omc/state/hud-stdin-cache.json
?? .omc/artifacts/
?? .omc/project-memory.json
?? .omc/sessions/
?? .omc/state/agent-replay-7afec07d-3b40-4e4c-8f86-86e9dc0e791c.jsonl
?? .omc/state/agent-replay-97c93024-a4c1-4e03-93bf-7522ce3517ff.jsonl
?? .omc/state/checkpoints/
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
?? docs/discussions/codex-review-2026-05-30/
?? "\346\257\225\344\270\232\347\246\273\346\240\241\347\263\273\347\273\237\347\224\250\346\210\267\346\226\207\346\241\243.zip"

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
最稳方案：**根目录 `AGENTS.md` 做自动入口，`docs/codex-review-protocol.md` 或现有 `docs/Codex审查流程指南.md` 存放完整规则**。

当前项目根目录实际没有 `AGENTS.md`，但本次会话上下文里注入了类似 `AGENTS.md` 的项目指令，并指向 `/home/caohui/.codex/RTK.md`。这说明自动入口机制存在，但项目文件缺失或由外部配置注入。为了跨会话稳定，建议现在补一个真实的根目录 `AGENTS.md`。

**1. 应该写入哪个文件？**

推荐结构：

```text
AGENTS.md                          # 自动入口，必须简短、强制、可加载
docs/codex-review-protocol.md      # 详细审查流程
```

不要只写 `docs/codex-review-protocol.md`，因为 docs 文件通常不会被自动读取。

不建议依赖 `CODEX.md`，除非你确认当前 Codex 运行器支持它。就本项目当前表现看，**`AGENTS.md` 是更可靠的入口名**。

`CLAUDE.md` 可以保留给 Claude，但不能假设 Codex 会自动遵守它。

**2. 文件内容如何组织？**

`AGENTS.md` 只放“必须加载哪些规则”的短指令，不放长流程。示例：

```markdown
# Project Agent Instructions

## Mandatory Project Rules

- For every shell command in this project, follow `/home/caohui/.codex/RTK.md`.
- Before performing any Codex review, document review, architecture review, API review, database review, data integration review, or OMC `/ask codex` workflow, read and follow `docs/codex-review-protocol.md`.
- If `docs/codex-review-protocol.md` conflicts with higher-priority system/developer instructions, follow the higher-priority instruction and state the conflict.
- Do not treat review-protocol steps as optional when the user requests a formal review or rule-governed Codex discussion.
```

`docs/codex-review-protocol.md` 再放完整流程：

```markdown
# Codex Review Protocol

## Load Trigger

Read this file before any of the following:
- Codex review
- document review
- architecture review
- database schema review
- API design review
- data integration review
- OMC `/ask codex` review workflow

## Required Workflow

...

## Output Format

...

## Verification Checklist

...
```

你现在已有 [docs/Codex审查流程指南.md](/home/caohui/projects/graduation-leave-system/docs/Codex审查流程指南.md)，内容里已经有 `Load Trigger`。可以继续用它，但我更建议复制或重命名为 ASCII 路径 `docs/codex-review-protocol.md`，减少工具、脚本、跨平台引用问题。

**3. 是否需要 Load Trigger？**

需要，但它本身不是魔法开关。

`Load Trigger` 只有在我已经读到这个文件后才有意义。真正让它生效的是根目录 `AGENTS.md` 里的这句：

```markdown
Before performing any Codex review..., read and follow `docs/codex-review-protocol.md`.
```

所以正确组合是：

```text
AGENTS.md 负责“自动入口”
Load Trigger 负责“读到文件后判断何时适用”
```

**4. 启动时会自动读取哪些文件？**

在当前 Codex 项目环境里，可靠假设是：

```text
系统/开发者指令
当前项目的 AGENTS.md 或等价注入的项目指令
AGENTS.md 中显式引用的文件
```

不能可靠假设会自动读取：

```text
CODEX.md
CLAUDE.md
docs/*.md
README.md
.omc/*
```

除非入口文件明确要求读取，或用户当前任务触发我主动查找。

**5. 现在创建后，能否确认下次自动生效？**

我可以确认两件事：

1. **格式是否正确**：可以创建后检查 `AGENTS.md` 是否位于项目根目录，引用路径是否存在，规则是否没有歧义。
2. **在当前机制下是否具备自动生效条件**：如果 Codex 下次从 `/home/caohui/projects/graduation-leave-system` 启动，并加载根目录 `AGENTS.md`，那它会自动生效。

我不能 100% 从当前会话证明“下一次启动器一定读取 `AGENTS.md`”，因为那取决于 Codex CLI/运行器加载策略。但从本次上下文已经出现 “AGENTS.md instructions for 当前项目” 来看，**这是最接近可验证、可固化的方案**。

具体执行建议：

```text
1. 新建根目录 AGENTS.md
2. 将现有 docs/Codex审查流程指南.md 复制或迁移为 docs/codex-review-protocol.md
3. AGENTS.md 用强制语气引用该协议文件
4. 可选：CLAUDE.md 也加同一条引用，保证 Claude/Codex 双端一致
5. 下次新会话启动后，问我“本项目审查规则入口是什么”，验证我是否能指出 AGENTS.md 和协议文件
```

如果你要现在固化，我建议采用：

```text
AGENTS.md
docs/codex-review-protocol.md
```

而不是只依赖 `CODEX.md` 或 docs 文件。
tokens used
13,933

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
