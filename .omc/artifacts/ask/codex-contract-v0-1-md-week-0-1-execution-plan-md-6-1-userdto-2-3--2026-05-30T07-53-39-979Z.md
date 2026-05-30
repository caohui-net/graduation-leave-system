# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-05-30T07:53:39.980Z

## Original task

请确认刚修正的contract-v0.1.md和week-0-1-execution-plan.md是否已解决之前指出的6个问题：1) UserDTO字段可选性 2) 状态机契约表 3) Dorm Mock失败策略 4) seed数据完整性 5) API端点数量统一 6) 降级条件改进。修正后的文档是否达到'可执行契约'标准？是否可以立即开始Week 1实施？如果还有问题，请指出。

## Final prompt

请确认刚修正的contract-v0.1.md和week-0-1-execution-plan.md是否已解决之前指出的6个问题：1) UserDTO字段可选性 2) 状态机契约表 3) Dorm Mock失败策略 4) seed数据完整性 5) API端点数量统一 6) 降级条件改进。修正后的文档是否达到'可执行契约'标准？是否可以立即开始Week 1实施？如果还有问题，请指出。

## Raw output

```text
结论：**还没有完全达到“可执行契约”标准，不建议直接开始 Week 1 的完整实施**。可以先启动不受争议影响的 Day 1 骨架、模型、seed、认证准备，但应先用半天把下面几个契约不一致点修掉再冻结。

**6 个问题核对结果**

1. **UserDTO 字段可选性：基本已解决**
   [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:22) 已把 `class_id`、`is_graduating`、`graduation_year` 标为 Optional。  
   但登录响应里的 `user` 示例只返回 `user_id/name/role/class_id`，不包含 `active/is_graduating/graduation_year`，和 `UserDTO` 不完全一致：[contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:214)。建议明确这是 `AuthUserDTO`，或让响应严格返回 `UserDTO`。

2. **状态机契约表：已解决**
   申请状态流转、宿舍清退阻断规则、角色权限矩阵都已补上：[contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:129)。对 Week 1 最小闭环足够。

3. **Dorm Mock 失败策略：部分解决**
   已覆盖 `completed/pending/not_started/unknown`，默认返回 `NOT_STARTED` 避免误放行：[contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:430)。  
   但状态表定义了 `provider_unavailable -> 503 PROVIDER_UNAVAILABLE`：[contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:145)，Mock 实现和错误 Mock 没有可触发的 503 样本。建议加一个固定学号，如 `2020503`，返回/抛出 `PROVIDER_UNAVAILABLE`，并补 503 错误响应和测试。

4. **seed 数据完整性：基本已解决**
   有 10 学生、2 辅导员、1 学工部、班级映射、默认密码、4 个边界样本：[contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:358)。这项可以支持 Week 1。

5. **API 端点数量统一：未解决，仍是主要阻塞**
   契约实际列了 **6 个 HTTP 路由**：login、submit、detail、approve、reject、list：[contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:199)。  
   计划里又写 Day 1 是 **5 个核心 API 端点**：[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:29)，Week 1 交付和验收写 **4 个 API 端点**：[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:102)、[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:208)。  
   建议立即统一为一种口径：要么 Week 1 实施 5 个 HTTP 路由并移除 `GET /api/applications` 列表接口；要么保留列表接口并把计划全部改成 6 个 HTTP 路由。

6. **降级条件改进：部分解决，但仍有矛盾**
   Day 3-4 的降级写“保留提交→辅导员审批→查询，砍学工部审批、列表API”是合理方向：[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:112)。  
   但风险表又写“申请提交 API 未完成 → 只做查询 API，Day 4 补申请提交”：[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:176)，这和纵向切片目标冲突。Day 5 的“周末加班修复”也不是可执行的降级条件：[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:188)。

**最终判断**

当前文档是“接近可执行契约”，但还不是冻结版。阻塞点主要是 **API 路由数量不统一**、**Dorm Mock 缺 503 失败路径**、**降级规则仍有自相矛盾**。这些都是小修，不需要重新设计。

建议先修这 3 点，然后就可以开始 Week 1。若必须今天开工，可以只开 Day 1 的 Django 骨架、基础模型、seed、登录，不要先实现申请/审批路由，避免按错误端点口径返工。


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
session id: 019e77dd-cc7a-7082-bd44-c6c509a72c6c
--------
user
请确认刚修正的contract-v0.1.md和week-0-1-execution-plan.md是否已解决之前指出的6个问题：1) UserDTO字段可选性 2) 状态机契约表 3) Dorm Mock失败策略 4) seed数据完整性 5) API端点数量统一 6) 降级条件改进。修正后的文档是否达到'可执行契约'标准？是否可以立即开始Week 1实施？如果还有问题，请指出。
codex
我会按项目要求先读取本仓库的审查协议和命令规范，然后对两份文档逐项核对这 6 个问题，最后给出是否可进入 Week 1 的结论。
exec
/bin/bash -lc "sed -n '1,260p' docs/codex-review-protocol.md" in /home/caohui/projects/graduation-leave-system
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
审查协议已读取；这里属于文档/API/契约审查，我会按“问题优先、逐项定位、最后给结论”的方式处理。RTK 规则要求项目内 shell 命令加 `rtk` 前缀，后续命令我会按这个规范执行。
exec
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
 M .omc/state/hud-stdin-cache.json
?? .claude/
?? .omc/artifacts/
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
/bin/bash -lc "rtk rg --files | rtk rg 'contract-v0\\.1\\.md|week-0-1-execution-plan\\.md|codex|review|consensus|execution|contract'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md
docs/codex-review-protocol.md
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md
docs/plans/week-0-1-execution-plan.md
docs/contracts/contract-v0.1.md
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md
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
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md

codex
我已定位到两份目标文档和本轮 5/30 的审查记录。接下来先抽取目标文档的关键章节，再对照前一轮 Codex 记录里的 6 个缺口，避免只看表面关键词。
exec
/bin/bash -lc 'rtk rg -n "UserDTO|状态机|state|Dorm|Mock|seed|端点|endpoint|API|降级|fallback|degrad|optional|required|nullable|可选|失败策略|完整性|数量|Week 1|可执行契约" docs/plans/week-0-1-execution-plan.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
13:冻结v0.1最小可执行契约，为Week 1纵向切片提供稳定基础。
18:- [x] 定义核心DTO（User、Application、Approval、DormCheckoutStatus）
29:- [ ] 创建样例请求/响应（5个核心API端点）
35:- [ ] 创建Mock响应（宿舍清退Mock + 错误Mock）
36:- [ ] 生成seed数据（10学生 + 2辅导员 + 1学工部 + 边界样本 + 默认密码）
48:**降级条件：**
49:- 如Day 1结束未完成前端review → 冻结当前版本，Week 1开始后异步review
53:## Week 1：后端纵向切片（5工作日）
56:交付可运行的后端最小闭环：薄认证 + 申请提交 + 两级审批 + 状态查询 + Dorm Mock。
70:- `python manage.py seed_users` 可用
76:- [ ] 登录API返回JWT token
78:**降级条件：**
79:- 如Day 2结束seed命令未完成 → 手动插入测试数据，Week 2补seed命令
84:- [ ] 申请提交API（POST /api/applications）
86:  - Dorm Mock集成：检查宿舍清退状态
89:- [ ] 辅导员审批API（POST /api/approvals/{id}/approve|reject）
93:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
96:- [ ] 状态查询API（GET /api/applications/{id}）
102:- 4个API端点可用
112:**降级条件：**
113:- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批、列表API
114:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
124:- [ ] 契约测试（API响应格式符合contract-v0.1.md）
139:**降级条件：**
146:### 前端准备（Week 1期间）
151:- [ ] Mock Server配置（基于contract-v0.1.md）
152:- [ ] API Client封装
156:**时间：** Week 1 Day 1-5（与后端并行）
160:- Mock Server可用
161:- API Client可用
168:## 风险和降级
174:**缓解措施：** 1-2工作日timebox，超时冻结当前假设进入Week 1
176:### 风险2：Week 1 Day 3申请提交API未完成
180:**降级方案：** 只做查询API，Day 4补申请提交
182:### 风险3：Week 1 Day 4学工部审批未完成
186:**降级方案：** 推到Week 2 Day 1，Week 1只验证辅导员审批
188:### 风险4：Week 1 Day 5测试未通过
192:**降级方案：** 周末加班修复，或Week 2 Day 1修复
204:### Week 1验收
208:- [ ] 4个API端点可用（登录、提交、审批、查询）

exec
/bin/bash -lc 'rtk rg -n "UserDTO|状态机|state|Dorm|Mock|seed|端点|endpoint|API|降级|fallback|degrad|must|MUST|optional|required|nullable|可选|失败策略|完整性|数量|Week 1|可执行契约" docs/contracts/contract-v0.1.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
1:# 数据契约 v0.1 - 最小可执行契约
5:**适用范围：** Week 1纵向切片  
12:### 1.1 UserDTO
16:class UserDTO:
40:    dorm_checkout_status: DormCheckoutStatus
61:### 1.4 DormCheckoutStatusDTO
65:class DormCheckoutStatusDTO:
68:    status: DormCheckoutStatus   # completed/pending/not_started/unknown
115:### 2.5 DormCheckoutStatus
118:class DormCheckoutStatus(str, Enum):
122:    UNKNOWN = "unknown"              # 状态未知（API失败）
125:### 2.6 状态机契约
175:| PROVIDER_UNAVAILABLE | 503 | 外部服务不可用 | 宿舍清退API超时 |
195:## 4. API端点
333:- `status`: ApplicationStatus（可选）
334:- `student_id`: 学号（可选，辅导员/学工部可用）
423:## 6. Mock响应
425:### 6.1 宿舍清退Mock
427:**DormCheckoutProvider Mock实现：**
430:class MockDormCheckoutProvider:
431:    def check_status(self, student_id: str) -> DormCheckoutStatusDTO:
434:            "2020001": DormCheckoutStatusDTO(
436:                status=DormCheckoutStatus.COMPLETED,
441:            "2020002": DormCheckoutStatusDTO(
443:                status=DormCheckoutStatus.PENDING,
448:            "2020003": DormCheckoutStatusDTO(
450:                status=DormCheckoutStatus.NOT_STARTED,
455:            "2020099": DormCheckoutStatusDTO(
457:                status=DormCheckoutStatus.UNKNOWN,
465:        return mock_data.get(student_id, DormCheckoutStatusDTO(
467:            status=DormCheckoutStatus.NOT_STARTED,
474:### 6.2 错误Mock
496:**422 Dorm Blocked：**
517:**初始版本 - 最小可执行契约**
520:- 核心DTO（User、Application、Approval、DormCheckoutStatus）
521:- 状态枚举（UserRole、ApplicationStatus、ApprovalStep、ApprovalDecision、DormCheckoutStatus）
523:- API端点（认证、申请、审批、查询）
525:- Mock响应（宿舍清退Mock + 错误Mock）
528:- 附件相关DTO和API
529:- 通知相关DTO和API
530:- 微信OAuth相关API
536:- 后端可用seed数据跑通端到端测试
544:**Mock Server配置：**
560:  // ... 其他端点
568:python manage.py seed_users
569:python manage.py seed_class_mappings

exec
/bin/bash -lc 'rtk rg -n "UserDTO|状态机|Dorm Mock|seed|端点|endpoint|降级|degrad|fallback|6个|六个|可执行契约|Week 1|blocking|Critical|P0" docs/discussions/codex-review-2026-05-30' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:6:**审查对象：** 38-codex-api-blocking-review.md
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:18:## 对P0问题的响应
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:20:### P0-1：RealUserDataProvider不应成为运行时依赖
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:89:### P0-2：+3天生产就绪评估过于乐观
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:199:USER_DATA_SOURCE = env.str('USER_DATA_SOURCE', default='seed')  # seed|csv|api
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:204:USER_DATA_SOURCE = 'seed'  # 开发环境使用种子数据
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:277:| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:280:| Week 6-7 | 宿舍清退Provider、降级流程、缓存、错误分类 | 宿舍清退集成模块 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:282:| Week 10 | 联调、演示、验收清单 | 可演示版本（Mock数据） |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:315:3. **宿舍清退实时查询：** DormCheckoutProvider用于运行时查询，可缓存，可降级
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:333:| Week 7做接口抽象 | Week 1做数据契约和接口 | 避免后续返工 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:338:1. **Week 1：** 数据契约、DTO、ImportSource接口
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:343:6. **Week 10：** 联调和演示
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:351:- 降级流程
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:371:3. 开始Week 1工作：数据契约和接口设计
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:16:1. **Week 0（1-2工作日）：** 冻结v0.1最小可执行契约
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:17:2. **Week 1（5工作日）：** 后端纵向切片（保留最小权限校验）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:21:6. **Week 6-7：** 宿舍真实API或降级
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:23:8. **Week 10：** 验收演示（不新增功能）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:31:**范围：** 最小可执行契约（不是极简字段，也不是完整模型）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:47:**时间限制：** 1-2工作日完成，超时冻结当前假设进入Week 1
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:49:### 决策2：Week 1交付后端纵向切片
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:60:- Dorm Mock参与提交校验
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:98:- Mock数据（seed + fixture）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:115:| **Week 0** (1-2工作日) | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog | 前端可用mock跑通登录→提交→审批→查询流程 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:116:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:120:| **Week 6-7** | 宿舍真实API或降级方案 | 真实Provider、错误分类、缓存/降级、人工证明路径 | 真实API集成或降级方案可用 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:122:| **Week 10** | 验收演示 | 演示脚本、缺陷修复、文档 | 可演示版本交付，不新增功能 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:146:**验收标准：** 按天列出责任人、交付物、降级条件和验收测试
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:162:**修正后：** Week 1端到端最小流程 → Week 2-3扩展 → Week 4前端并行
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:168:**原方案A：** Week 8-9前端，Week 10联调
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:182:### 修正4：从Week 1数据契约到Week 0
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:184:**原方案A：** Week 1做数据契约和接口设计
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:186:**修正后：** Week 0（1-2工作日）冻结v0.1，Week 1用v0.1跑纵向切片
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:188:**原因：** 避免Week 1前半定义契约，后半只剩2-3天开发
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:192:**Claude错误建议：** Week 1"审批API无权限校验"
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:196:**原因：** 纵向切片的价值是验证角色、数据、状态机和审批链路能否串起来
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:204:**缓解措施：** 1-2工作日timebox，超时冻结当前假设进入Week 1
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:206:### 风险2：Week 1纵向切片未完成
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:208:**降级条件：**
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:216:- 如果核心端点还没有可运行实现，前端做一周mock驱动开发，Week 5切真实环境
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:219:### 风险4：Week 10过载
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:221:**缓解措施：** Week 10只做验收和演示，前面延期的任务砍掉或推迟到生产集成阶段
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:231:- Codex批判：瀑布式排期、前端后置、Week 10过载
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:235:- Claude质疑：v0.1何时冻结、Week 1工作量、前端启动条件
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:237:- Codex指出Claude方案问题：Week 0膨胀、v0.1过于字段化、Week 1砍权限校验
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:241:- 达成共识：Week 0-1拆分、v0.1最小可执行契约、保留最小权限校验、前端Week 4并行
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:248:4. **数据契约提前冻结** - 避免Week 1前半定义后半开发
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:15:它比旧计划好，但仍然是"先后端模块、后前端、最后联调"的瀑布排期。最大风险不是数据契约，而是到Week 8-10才发现端到端流程、微信小程序、附件、审批权限、宿舍降级和通知串不起来。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:26:- Week 8-9前端、Week 10联调风险很高
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:34:### 问题2：Week 10过载
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:37:Week 10不能既做联调、验收、性能、部署、文档，又兜底前面延期。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:48:若演示还包含双端、真实微信、完整附件、通知、导入审计、宿舍降级，那不现实。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:56:更好的做法是先做`seed/import minimal path`，让认证和审批用同一套落库数据跑起来，再完善CSV校验、staging、审计。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:70:### 问题1：Week 1做数据契约太晚吗？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:72:**回答：** 不该等到Week 1结束。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:75:现在就应冻结v0.1：字段、枚举、样例CSV、错误码、前端API mock。Week 1用它跑纵向切片。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:86:**回答：** 不应Week 1完整完成，但Week 1必须完成最小导入路径。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:89:seed/CSV二选一落库到真实users/class mapping表。完整staging、审计、软停用放Week 2。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:107:**回答：** Mock Provider和契约测试必须Week 1进入提交申请流程。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:119:### 问题8：Week 1的工作量是否饱和？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:124:Week 1应交付可运行骨架、契约测试、seed数据、最小审批流，而不是只交文档和接口。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:152:- Dorm Mock接入提交校验
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:164:- 状态机和审计补齐
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:173:- 若API不到位，保留mock + 人工证明降级
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:181:**Week 10：验收和演示**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:211:指定责任人，设定截止日期（Week 5前必须到位，否则启用降级方案）。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:229:### 6. Week 10没有缓冲
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:232:Week 10既要验收又要兜底延期，无缓冲空间。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:235:Week 10只做验收和演示，前面延期的任务砍掉或推迟到生产集成阶段。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:244:1. 立即冻结数据契约v0.1（现在，不是Week 1）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:245:2. Week 1交付可运行的纵向切片（不是文档）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:248:5. Week 10只做验收（不塞新功能）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:6:**优先级：** P0（决定实施路径）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:37:1. 更新实施计划文档（调整Week 1-10任务分配）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:38:2. 开始Week 1工作：数据契约、DTO、ImportSource接口设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:64:   - 调整Week 1-10任务分配
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:65:   - 将数据契约和接口设计提前到Week 1
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:68:2. **Week 1启动：** 数据契约和接口设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:88:- Week 1的工作量是否合理？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:97:**问题1：Week 1做数据契约是否太晚？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:99:- 是否应该在Week 1之前（现在）就冻结数据契约？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:100:- 如果现在冻结，Week 1可以做什么？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:110:- 是否应该Week 1就完成CSV导入？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:132:- Week 1: 数据契约和接口
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:137:- Week 10: 联调
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:141:**问题8：Week 1的工作量是否饱和？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:214:- **交付要求：** Week 10可演示版本（Mock数据）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:250:**优先级：** P0（决定实施路径）
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:12:Claude的质疑是必要的，尤其是把"Week 0准备"和"Week 1纵向切片"拆开这一点，有助于避免把契约、数据、实现全塞进同一个5天窗口。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:16:1. 把v0.1契约理解成"字段清单"，而不是可执行契约包。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:18:3. Week 1建议"审批API无权限校验"，会让纵向切片失去验证审批链路的意义。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:23:**采用Week 0-1拆分，但Week 0必须是1-2个工作日的timebox；v0.1应现在冻结最小可执行契约，不等到Week 1前半；Week 1只承诺后端端到端最小闭环；前端Week 4启动不要求后端完全稳定，只要求契约、mock和核心路径达到可消费状态。**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:27:## 一、数据契约v0.1：现在冻结还是Week 1前半？
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:31:**应现在冻结v0.1，不应拖到Week 1前半。**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:33:这里的"现在"不是指今天把完整未来模型一次性定死，而是指在正式Week 1编码前，用1-2个工作日完成一个可执行的v0.1基线：
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:38:- 样例CSV或seed fixture
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:43:如果拖到Week 1前半才冻结，Week 1后半只剩2-3天，很难完成后端骨架、认证、申请、审批、状态查询和集成测试。Claude把这个拆法描述成"Week 1前半冻结，Week 1后半纵向切片"，本质上还是把Week 1压缩成半周开发，风险比Codex原建议更高。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:50:- 选项B过大：把附件、通知、真实宿舍清退全部字段纳入v0.1，会拖慢Week 1并制造伪稳定。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:52:建议采用**最小可执行契约**：
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:60:| 宿舍清退 | provider_status、checked_at、blocking_reason、provider_error_code | 真实接口全部响应字段 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:63:| CSV/seed | 正常样本 + 边界样本 | 完整生产导入模板 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:71:- 后端负责人 owns 契约包：OpenAPI/DTO/错误码/seed schema。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:79:## 二、Week 1的7-10天工作量是否现实？
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:85:如果团队是2-3人，且Week 0已经完成v0.1契约，Week 1用5个工作日交付最小后端闭环是有机会的。但前提是严格砍范围，并且明确并行路径。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:87:Claude的拆解把工作量估成7-10天，但没有区分人日和日历天。2名后端/全栈并行时，5个工作日约等于10人日；如果只有1名有效后端，这个目标就必须降级。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:89:### Week 1应该保留什么
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:91:Week 1必须保留：
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:94:- seed/fixture落库
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:101:- Dorm Mock参与提交校验
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:104:这里需要反驳Claude的一点：**"审批API简化版，无权限校验"不应该进入Week 1目标。** 纵向切片的价值正是验证角色、数据、状态机和审批链路能否串起来。可以不做完整RBAC、组织树和复杂权限，但最小角色校验不能砍，否则Week 1只能证明CRUD能跑，不能证明毕业离校审批流程能跑。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:106:### Week 1可以推迟什么
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:108:Week 1应推迟：
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:123:- 冻结v0.1最小可执行契约
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:124:- 生成10-20条seed + 边界fixture
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:128:**Week 1 / Day 1-2：可运行骨架**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:132:- seed命令
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:135:**Week 1 / Day 3-4：最小流程**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:140:- Dorm Mock阻断/放行
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:142:**Week 1 / Day 5：验收硬化**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:149:如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:189:- 如果登录、提交、审批、查询四个核心端点还没有可运行实现，前端仍可做一周mock驱动开发，但Week 5必须切到真实开发环境联调。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:201:- Week 1做纵向切片
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:202:- Week 1不做附件、通知、微信OAuth
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:203:- Week 10只验收和修复
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:205:这比文档40的"Week 1只做数据契约、Week 8-9才做前端"更好。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:211:如果Week 0花3天定义契约，再Week 1花5天做切片，总体变成8个工作日。不是不可以，但这应被明确计入计划，而不是把"现在"当免费缓冲。建议Week 0限制为1-2个工作日，超过就冻结当前假设继续做，后续进入v0.2。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:215:Claude的Week 0列了StudentDTO、ApplicationDTO、ApprovalDTO，但缺少错误码、状态机、样例请求响应、mock、契约测试和变更规则。前端和测试真正依赖的是这些可执行产物，不只是字段名。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:217:**问题3：Week 1"无权限校验"会削弱纵向切片。**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:231:Week 1可以交Postman集合，但必须有自动化端到端测试。否则每次契约变化都靠人工点接口，后续Week 2-4会快速失控。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:241:| Week 0 / 1-2工作日 | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:242:| Week 1 | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:246:| Week 6-7 | 宿舍真实API或降级方案 | 真实Provider、错误分类、缓存/降级、人工证明路径 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:248:| Week 10 | 验收演示 | 演示脚本、缺陷修复、文档，不新增功能 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:254:1. **数据契约v0.1应该现在冻结还是Week 1前半？范围最小还是完整？**  
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:255:   现在冻结，限制在1-2个工作日内完成。范围是"最小可执行契约"，不是极简字段，也不是完整未来模型。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:257:2. **Week 1的7-10天工作量是否现实？如何调整？**  
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:258:   如果指7-10人日，在2-3人团队下现实；如果指7-10日历天，不现实。调整方式是Week 0先完成契约，Week 1只做后端最小闭环，推迟CSV完整导入、附件、通知、微信OAuth、真实宿舍API。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:264:   方向可行，但必须修正：Week 0要timebox，v0.1要可执行而非字段清单，Week 1不能砍掉最小权限校验，前端启动时间要统一，Week 2不要同时塞满CSV和主流程前端。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:270:**接受Claude的拆分方向，但不接受把契约冻结推迟到Week 1前半，也不接受Week 1无权限校验的纵向切片。**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:275:2. `week-0-1-execution-plan.md`：按天列出责任人、交付物、降级条件和验收测试。
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:17:3. 宿舍清退状态通过API实时查询（可缓存、可降级）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:139:USER_DATA_SOURCE = env.str('USER_DATA_SOURCE', default='seed')  # seed|csv|api
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:144:USER_DATA_SOURCE = 'seed'  # 开发环境使用种子数据
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:184:| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:187:| Week 6-7 | 宿舍清退Provider、降级流程、缓存、错误分类 | 宿舍清退集成模块 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:189:| Week 10 | 联调、演示、验收清单 | 可演示版本（Mock数据） |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:199:1. **Week 1结束：** 数据契约冻结，接口定义完成
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:203:5. **Week 10结束：** 可演示版本交付
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:277:### 7.2 降级策略
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:286:            # 降级到缓存
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:290:            # 降级到人工证明
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:309:| Week 7做接口抽象 | Week 1做数据契约和接口 | 避免后续返工 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:324:### 9.1 Week 10交付物
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:330:- [ ] 降级流程
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:341:- [ ] 降级流程验证通过
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:351:| 真实API字段与Mock不一致 | P1 | Week 1冻结数据契约，预留扩展字段 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:359:- **API不可用：** 降级到人工证明流程
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:366:- **审查请求：** [37-api-blocking-solution-review-request.md](./37-api-blocking-solution-review-request.md)
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:367:- **Codex审查：** [38-codex-api-blocking-review.md](./38-codex-api-blocking-review.md)
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:378:2. **Week 1启动：** 数据契约和接口设计
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:6:**审查对象：** 37-api-blocking-solution-review-request.md
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:24:## P0问题（必须修复）
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:26:### P0-1：RealUserDataProvider不应成为运行时依赖
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:53:### P0-2：+3天生产就绪评估过于乐观
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:67:参考：[37-api-blocking-solution-review-request.md](./37-api-blocking-solution-review-request.md) 第25行
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:117:当前设计用一个开关同时切用户数据和宿舍清退：[37-api-blocking-solution-review-request.md](./37-api-blocking-solution-review-request.md) 第160行。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:123:USER_DATA_SOURCE = 'seed' | 'csv' | 'api'
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:155:宿舍清退枚举和降级规则已有定义：[数据对接说明文档.md](../../数据对接说明文档.md) 第306行
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:167:Provider 契约、DTO、种子数据、导入接口应在 Week 1-2 完成，否则认证、审批、前端都会先绑定临时模型，后续返工。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:175:| Week 1 | 数据契约、DTO、Provider接口、种子数据、导入模型 | 数据契约文档、DTO定义、Provider接口 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:178:| Week 6-7 | 宿舍清退Provider、降级流程、缓存、错误分类 | 宿舍清退集成模块 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:180:| Week 10 | 联调、演示、验收清单 | 演示版本 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:235:│  运行时查询，可缓存，可降级到人工证明          │
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:245:5. **DormCheckoutProvider：** 运行时查询，可缓存，可降级到人工证明
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:280:现有设计已有重试和降级方向：[2026-05-27-system-design.md](../../design/2026-05-27-system-design.md) 第1697行
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:285:- 降级次数
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:305:   - 降级流程
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:311:1. **Week 1-3：** CSV导入 + 种子数据
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:315:5. **Week 10：** 联调和演示
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:14:Codex正确指出方案A的核心问题：瀑布式排期、前端后置、Week 10过载。纵向切片/MVP优先的方向是对的。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:18:2. Week 1交付"可运行骨架"的范围定义
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:38:- Week 10：验收演示
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:50:### 3. Week 10不能过载
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:54:Week 10应该只做验收、演示、缺陷修复，不塞新功能，不兜底延期。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:75:> 现在就应冻结v0.1：字段、枚举、样例CSV、错误码、前端API mock。Week 1用它跑纵向切片。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:90:- 如果v0.1范围太大，Week 1无法完成纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:94:- Week 1前半：冻结v0.1并生成样例数据（2-3天）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:95:- Week 1后半：用v0.1跑纵向切片（2-3天）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:98:你说的"现在"冻结，是指立即（今天）还是Week 1开始前？如果是立即，v0.1的范围应该多大？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:102:## 分歧点2：Week 1交付"可运行骨架"的范围
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:106:> Week 1应交付可运行骨架、契约测试、seed数据、最小审批流，而不是只交文档和接口。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:118:- Dorm Mock接入提交校验
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:127:5. **最小申请审批闭环**：2-3天（Application模型、Approval模型、状态机、3个API）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:128:6. **Dorm Mock**：0.5天（Mock Provider、契约测试）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:133:- 如果团队2-3人，Week 1（5个工作日）能完成吗？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:138:- Week 1目标：可运行的最小申请审批流（不含附件、通知）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:139:- Week 1交付：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:140:  - 契约v0.1 + seed数据
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:144:  - Dorm Mock（返回固定状态）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:145:- Week 1不交付：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:152:你认为Week 1的7-10天工作量是否现实？如果不现实，哪些可以推迟到Week 2？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:199:- Dorm Mock接入提交校验
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:210:**Week 1（纵向切片，5天）：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:222:- Day 5：Dorm Mock + 集成测试
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:226:**Week 1交付物：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:227:- 可运行的后端API（5个端点）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:231:**Week 1不交付：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:241:### 问题1：Week 1做数据契约太晚吗？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:244:不是太晚，而是Week 1的目标定义不清楚。应该是：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:246:- Week 1：用v0.1跑纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:254:- Mock数据（seed + fixture）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:267:### 问题8：Week 1的工作量是否饱和？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:270:Codex列出的Week 0-1工作量是7-10天，超过Week 1的5天。需要拆分：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:272:- Week 1（5天）：纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:289:### 2. Week 1纵向切片的验收标准
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:292:Week 1结束时，如何验证"纵向切片"成功？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:320:4. ✓ Week 10只做验收
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:324:2. Week 1工作量是否现实（7-10天 vs 5天）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:329:- Week 1（5天）：纵向切片（后端骨架 + 薄认证 + 最小审批流）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:335:- Week 10：验收演示
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:16:2. ✓ 定义v0.1为"最小可执行契约"（不是字段清单）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:17:3. ✓ 坚持Week 1保留最小权限校验（我的"无权限校验"建议是错误的）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:31:**v0.1范围：最小可执行契约**
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:45:**时间限制：** 1-2工作日完成，超时冻结当前假设进入Week 1
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:47:### 2. Week 1工作量：7-10人日现实，需严格砍范围
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:51:**Week 1必须保留：**
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:60:- Dorm Mock参与提交校验
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:63:**Week 1推迟：**
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:72:**我的错误：** 建议Week 1"无权限校验"是错误的。Codex正确指出：纵向切片的价值正是验证角色、数据、状态机和审批链路能否串起来。
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:101:**完全接受Codex的6个修正点。**
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:105:**修正3：** Week 1保留最小权限校验（不能砍）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:108:**修正6：** Week 1必须有自动化端到端测试（不只是Postman集合）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:116:| **Week 0** (1-2工作日) | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog | 前端可用mock跑通登录→提交→审批→查询流程 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:117:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:121:| **Week 6-7** | 宿舍真实API或降级方案 | 真实Provider、错误分类、缓存/降级、人工证明路径 | 真实API集成或降级方案可用 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:123:| **Week 10** | 验收演示 | 演示脚本、缺陷修复、文档 | 可演示版本交付，不新增功能 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:135:# 数据契约 v0.1 - 最小可执行契约
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:139:### 1.1 UserDTO
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:155:## 4. API端点
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:196:- [ ] 生成seed数据
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:204:## Week 1 (Day 1-5)
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:217:- [ ] Dorm Mock
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:225:## 降级条件
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:233:**验收标准：** 按天列出责任人、交付物、降级条件和验收测试
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:241:1. ✓ Week 0是1-2工作日timebox，冻结v0.1最小可执行契约
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:243:3. ✓ Week 1交付后端纵向切片，保留最小角色校验
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:244:4. ✓ Week 1工作量7-10人日现实（2-3人团队，5个工作日）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:247:7. ✓ Week 10只做验收演示，不新增功能
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:285:- Week 0（1-2工作日）：冻结v0.1最小可执行契约
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:286:- Week 1（5工作日）：后端纵向切片（保留最小权限校验）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:290:- Week 6-7：宿舍真实API或降级
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:292:- Week 10：验收演示
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:302:- Week 10过载风险
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:6:**优先级：** P0（阻塞开发进度）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:198:| Week 1-2 | 基础设施 + Mock数据 | Django项目、种子数据（100学生、10辅导员） |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:202:| Week 10 | 测试 | 单元测试、集成测试（Mock数据） |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:302:**问题10：错误处理和降级策略？**
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:303:- API不可用时的降级方案是否完善？
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:347:2. 风险等级评估（P0/P1/P2）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:362:3. 错误处理和降级策略改进
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:404:- Round 3: P0修复、字段补充、用户文档（20+问题修复）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:417:**优先级：** P0（阻塞开发进度）

exec
/bin/bash -lc "rtk nl -ba docs/contracts/contract-v0.1.md | rtk sed -n '150,280p'" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk nl -ba docs/contracts/contract-v0.1.md | rtk sed -n '280,410p'" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk nl -ba docs/contracts/contract-v0.1.md | rtk sed -n '1,150p'" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk nl -ba docs/contracts/contract-v0.1.md | rtk sed -n '410,590p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 130ms:
 succeeded in 329ms:
     1	# 数据契约 v0.1 - 最小可执行契约
     2	
     3	**版本：** v0.1  
     4	**冻结日期：** 2026-05-30  
     5	**适用范围：** Week 1纵向切片  
     6	**下一版本：** v0.2（Week 3）
     7	
     8	---
     9	
    10	## 1. 核心DTO
    11	
    12	### 1.1 UserDTO
    13	
    14	```python
    15	@dataclass
    16	class UserDTO:
    17	    """用户数据传输对象"""
    18	    user_id: str                      # 学号/工号
    19	    name: str                         # 姓名
    20	    role: UserRole                    # 角色：student/counselor/dean
    21	    active: bool                      # 账号是否激活
    22	    class_id: Optional[str] = None    # 班级ID（学生必填，教师为None）
    23	    is_graduating: Optional[bool] = None  # 是否毕业生（仅学生）
    24	    graduation_year: Optional[int] = None # 毕业年份（仅学生）
    25	```
    26	
    27	### 1.2 ApplicationDTO
    28	
    29	```python
    30	@dataclass
    31	class ApplicationDTO:
    32	    """离校申请数据传输对象"""
    33	    application_id: str
    34	    student_id: str
    35	    student_name: str
    36	    class_id: str
    37	    reason: str                      # 申请理由
    38	    leave_date: str                  # 计划离校日期 (YYYY-MM-DD)
    39	    status: ApplicationStatus
    40	    dorm_checkout_status: DormCheckoutStatus
    41	    created_at: str                  # ISO8601
    42	    updated_at: str
    43	```
    44	
    45	### 1.3 ApprovalDTO
    46	
    47	```python
    48	@dataclass
    49	class ApprovalDTO:
    50	    """审批记录数据传输对象"""
    51	    approval_id: str
    52	    application_id: str
    53	    step: ApprovalStep           # counselor/dean
    54	    approver_id: str
    55	    approver_name: str
    56	    decision: ApprovalDecision   # approved/rejected/pending
    57	    comment: Optional[str]
    58	    decided_at: Optional[str]    # ISO8601
    59	```
    60	
    61	### 1.4 DormCheckoutStatusDTO
    62	
    63	```python
    64	@dataclass
    65	class DormCheckoutStatusDTO:
    66	    """宿舍清退状态数据传输对象"""
    67	    student_id: str
    68	    status: DormCheckoutStatus   # completed/pending/not_started/unknown
    69	    checked_at: Optional[str]    # ISO8601
    70	    blocking_reason: Optional[str]
    71	    provider_error_code: Optional[str]
    72	```
    73	
    74	---
    75	
    76	## 2. 状态枚举
    77	
    78	### 2.1 UserRole
    79	
    80	```python
    81	class UserRole(str, Enum):
    82	    STUDENT = "student"
    83	    COUNSELOR = "counselor"
    84	    DEAN = "dean"
    85	```
    86	
    87	### 2.2 ApplicationStatus
    88	
    89	```python
    90	class ApplicationStatus(str, Enum):
    91	    DRAFT = "draft"                      # 草稿
    92	    PENDING_COUNSELOR = "pending_counselor"  # 待辅导员审批
    93	    PENDING_DEAN = "pending_dean"        # 待学工部审批
    94	    APPROVED = "approved"                # 已通过
    95	    REJECTED = "rejected"                # 已驳回
    96	```
    97	
    98	### 2.3 ApprovalStep
    99	
   100	```python
   101	class ApprovalStep(str, Enum):
   102	    COUNSELOR = "counselor"
   103	    DEAN = "dean"
   104	```
   105	
   106	### 2.4 ApprovalDecision
   107	
   108	```python
   109	class ApprovalDecision(str, Enum):
   110	    PENDING = "pending"
   111	    APPROVED = "approved"
   112	    REJECTED = "rejected"
   113	```
   114	
   115	### 2.5 DormCheckoutStatus
   116	
   117	```python
   118	class DormCheckoutStatus(str, Enum):
   119	    COMPLETED = "completed"          # 已清退
   120	    PENDING = "pending"              # 清退中
   121	    NOT_STARTED = "not_started"      # 未开始
   122	    UNKNOWN = "unknown"              # 状态未知（API失败）
   123	```
   124	
   125	### 2.6 状态机契约
   126	
   127	**申请状态流转规则：**
   128	
   129	| 当前状态 | 触发动作 | 角色 | 下一状态 | 副作用 |
   130	|---------|---------|------|---------|--------|
   131	| - | 学生提交申请 | student | pending_counselor | 创建辅导员审批记录 |
   132	| pending_counselor | 辅导员通过 | counselor | pending_dean | 创建学工部审批记录 |
   133	| pending_counselor | 辅导员驳回 | counselor | rejected | 无 |
   134	| pending_dean | 学工部通过 | dean | approved | 无 |
   135	| pending_dean | 学工部驳回 | dean | rejected | 无 |
   136	
   137	**宿舍清退状态处理规则：**
   138	
   139	| 宿舍状态 | 提交申请行为 | HTTP状态 | 错误码 |
   140	|---------|------------|---------|--------|
   141	| completed | 允许提交 | 201 | - |
   142	| pending | 阻断提交 | 422 | DORM_BLOCKED |
   143	| not_started | 阻断提交 | 422 | DORM_BLOCKED |
   144	| unknown | 阻断提交 | 422 | DORM_BLOCKED |
   145	| provider_unavailable | 阻断提交 | 503 | PROVIDER_UNAVAILABLE |
   146	
   147	**角色权限矩阵：**
   148	
   149	| 操作 | student | counselor | dean |
   150	|------|---------|-----------|------|

 succeeded in 393ms:
   280	### 4.3 审批
   281	
   282	#### POST /api/approvals/{approval_id}/approve
   283	
   284	**请求：**
   285	```json
   286	{
   287	  "comment": "同意离校"
   288	}
   289	```
   290	
   291	**响应：**
   292	```json
   293	{
   294	  "approval_id": "apv_001",
   295	  "application_id": "app_001",
   296	  "step": "counselor",
   297	  "approver_id": "T001",
   298	  "approver_name": "李老师",
   299	  "decision": "approved",
   300	  "comment": "同意离校",
   301	  "decided_at": "2024-05-30T11:00:00Z"
   302	}
   303	```
   304	
   305	#### POST /api/approvals/{approval_id}/reject
   306	
   307	**请求：**
   308	```json
   309	{
   310	  "comment": "材料不齐全"
   311	}
   312	```
   313	
   314	**响应：**
   315	```json
   316	{
   317	  "approval_id": "apv_001",
   318	  "application_id": "app_001",
   319	  "step": "counselor",
   320	  "approver_id": "T001",
   321	  "approver_name": "李老师",
   322	  "decision": "rejected",
   323	  "comment": "材料不齐全",
   324	  "decided_at": "2024-05-30T11:00:00Z"
   325	}
   326	```
   327	
   328	### 4.4 查询
   329	
   330	#### GET /api/applications
   331	
   332	**查询参数：**
   333	- `status`: ApplicationStatus（可选）
   334	- `student_id`: 学号（可选，辅导员/学工部可用）
   335	
   336	**响应：**
   337	```json
   338	{
   339	  "applications": [
   340	    {
   341	      "application_id": "app_001",
   342	      "student_id": "2020001",
   343	      "student_name": "张三",
   344	      "status": "pending_counselor",
   345	      "created_at": "2024-05-30T10:00:00Z"
   346	    }
   347	  ],
   348	  "total": 1
   349	}
   350	```
   351	
   352	---
   353	
   354	## 5. 样例数据
   355	
   356	### 5.1 正常样本
   357	
   358	**默认密码：** 所有账号默认密码为 `password123`
   359	
   360	**学生（10人）：**
   361	```python
   362	students = [
   363	    {"user_id": "2020001", "name": "张三", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
   364	    {"user_id": "2020002", "name": "李四", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
   365	    {"user_id": "2020003", "name": "王五", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
   366	    {"user_id": "2020004", "name": "赵六", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
   367	    {"user_id": "2020005", "name": "钱七", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
   368	    {"user_id": "2020006", "name": "孙八", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
   369	    {"user_id": "2020007", "name": "周九", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
   370	    {"user_id": "2020008", "name": "吴十", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
   371	    {"user_id": "2020009", "name": "郑十一", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
   372	    {"user_id": "2020010", "name": "王十二", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
   373	]
   374	```
   375	
   376	**辅导员（2人）：**
   377	```python
   378	counselors = [
   379	    {"user_id": "T001", "name": "李老师", "role": "counselor", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
   380	    {"user_id": "T002", "name": "王老师", "role": "counselor", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
   381	]
   382	```
   383	
   384	**学工部（1人）：**
   385	```python
   386	deans = [
   387	    {"user_id": "D001", "name": "赵主任", "role": "dean", "class_id": None, "is_graduating": None, "graduation_year": None, "active": True},
   388	]
   389	```
   390	
   391	**班级映射：**
   392	```python
   393	class_mappings = [
   394	    {"class_id": "CS2020-01", "counselor_id": "T001"},
   395	    {"class_id": "CS2020-02", "counselor_id": "T002"},
   396	]
   397	```
   398	
   399	### 5.2 边界样本
   400	
   401	**无班级映射：**
   402	```python
   403	{"user_id": "2020099", "name": "边界1", "role": "student", "class_id": "INVALID", "is_graduating": True, "graduation_year": 2024, "active": True}
   404	```
   405	
   406	**辅导员停用：**
   407	```python
   408	{"user_id": "T099", "name": "停用老师", "role": "counselor", "class_id": None, "active": False}
   409	```
   410	

 succeeded in 458ms:
   150	|------|---------|-----------|------|
   151	| 提交申请 | ✓（仅自己） | ✗ | ✗ |
   152	| 查看申请 | ✓（仅自己） | ✓（本班级） | ✓（所有） |
   153	| 辅导员审批 | ✗ | ✓（本班级） | ✗ |
   154	| 学工部审批 | ✗ | ✗ | ✓（所有） |
   155	
   156	---
   157	
   158	## 3. 错误码
   159	
   160	### 3.1 业务错误 (4xx)
   161	
   162	| 错误码 | HTTP状态 | 说明 | 示例场景 |
   163	|--------|---------|------|---------|
   164	| VALIDATION_ERROR | 400 | 请求参数校验失败 | 必填字段缺失、格式错误 |
   165	| AUTH_REQUIRED | 401 | 未认证 | Token缺失或过期 |
   166	| FORBIDDEN | 403 | 无权限 | 学生访问他人申请 |
   167	| NOT_FOUND | 404 | 资源不存在 | 申请ID不存在 |
   168	| CONFLICT | 409 | 资源冲突 | 重复提交申请 |
   169	| DORM_BLOCKED | 422 | 宿舍清退未完成 | 提交申请时宿舍未清退 |
   170	
   171	### 3.2 系统错误 (5xx)
   172	
   173	| 错误码 | HTTP状态 | 说明 | 示例场景 |
   174	|--------|---------|------|---------|
   175	| PROVIDER_UNAVAILABLE | 503 | 外部服务不可用 | 宿舍清退API超时 |
   176	| INTERNAL_ERROR | 500 | 内部错误 | 数据库连接失败 |
   177	
   178	### 3.3 错误响应格式
   179	
   180	```json
   181	{
   182	  "error": {
   183	    "code": "DORM_BLOCKED",
   184	    "message": "宿舍清退未完成，无法提交申请",
   185	    "details": {
   186	      "student_id": "2020001",
   187	      "dorm_status": "pending"
   188	    }
   189	  }
   190	}
   191	```
   192	
   193	---
   194	
   195	## 4. API端点
   196	
   197	### 4.1 认证
   198	
   199	#### POST /api/auth/login
   200	
   201	**请求：**
   202	```json
   203	{
   204	  "user_id": "2020001",
   205	  "password": "password123"
   206	}
   207	```
   208	
   209	**响应：**
   210	```json
   211	{
   212	  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
   213	  "token_type": "Bearer",
   214	  "user": {
   215	    "user_id": "2020001",
   216	    "name": "张三",
   217	    "role": "student",
   218	    "class_id": "CS2020-01"
   219	  }
   220	}
   221	```
   222	
   223	### 4.2 申请
   224	
   225	#### POST /api/applications
   226	
   227	**请求：**
   228	```json
   229	{
   230	  "reason": "毕业离校",
   231	  "leave_date": "2024-06-30"
   232	}
   233	```
   234	
   235	**响应：**
   236	```json
   237	{
   238	  "application_id": "app_001",
   239	  "student_id": "2020001",
   240	  "student_name": "张三",
   241	  "class_id": "CS2020-01",
   242	  "reason": "毕业离校",
   243	  "leave_date": "2024-06-30",
   244	  "status": "pending_counselor",
   245	  "dorm_checkout_status": "completed",
   246	  "created_at": "2024-05-30T10:00:00Z",
   247	  "updated_at": "2024-05-30T10:00:00Z"
   248	}
   249	```
   250	
   251	#### GET /api/applications/{application_id}
   252	
   253	**响应：**
   254	```json
   255	{
   256	  "application_id": "app_001",
   257	  "student_id": "2020001",
   258	  "student_name": "张三",
   259	  "class_id": "CS2020-01",
   260	  "reason": "毕业离校",
   261	  "leave_date": "2024-06-30",
   262	  "status": "pending_counselor",
   263	  "dorm_checkout_status": "completed",
   264	  "approvals": [
   265	    {
   266	      "approval_id": "apv_001",
   267	      "step": "counselor",
   268	      "approver_id": "T001",
   269	      "approver_name": "李老师",
   270	      "decision": "pending",
   271	      "comment": null,
   272	      "decided_at": null
   273	    }
   274	  ],
   275	  "created_at": "2024-05-30T10:00:00Z",
   276	  "updated_at": "2024-05-30T10:00:00Z"
   277	}
   278	```
   279	
   280	### 4.3 审批

exec
/bin/bash -lc "rtk nl -ba docs/contracts/contract-v0.1.md | rtk sed -n '590,680p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   590	    # 4. 学工部审批
   591	    # 5. 查询状态
   592	```
   593	
   594	---
   595	
   596	**契约负责人：** Claude Opus 4.7  
   597	**前端Review：** 待确认  
   598	**业务确认：** 待确认  
   599	**冻结日期：** 2026-05-30  
   600	**下一版本：** v0.2（Week 3）

exec
/bin/bash -lc "rtk nl -ba docs/plans/week-0-1-execution-plan.md | rtk sed -n '130,230p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   130	**交付物：**
   131	- 4个自动化测试通过
   132	- Week 2任务清单
   133	
   134	**验收标准：**
   135	- [ ] 所有测试通过
   136	- [ ] 无P0/P1阻断bug
   137	- [ ] Week 2任务清单明确
   138	
   139	**降级条件：**
   140	- 如Day 5结束仍有P0 bug → 推到Week 2 Day 1修复，或砍掉触发bug的边界场景
   141	
   142	---
   143	
   144	## 并行任务
   145	
   146	### 前端准备（Week 1期间）
   147	
   148	**任务：**
   149	- [ ] 技术栈选型确认（微信小程序框架）
   150	- [ ] 项目初始化
   151	- [ ] Mock Server配置（基于contract-v0.1.md）
   152	- [ ] API Client封装
   153	
   154	**责任人：** 前端负责人
   155	
   156	**时间：** Week 1 Day 1-5（与后端并行）
   157	
   158	**交付物：**
   159	- 微信小程序项目可运行
   160	- Mock Server可用
   161	- API Client可用
   162	
   163	**验收标准：**
   164	- [ ] 可用mock跑通登录→提交→审批→查询流程
   165	
   166	---
   167	
   168	## 风险和降级
   169	
   170	### 风险1：Week 0契约定义延期
   171	
   172	**概率：** 中  
   173	**影响：** 高  
   174	**缓解措施：** 1-2工作日timebox，超时冻结当前假设进入Week 1
   175	
   176	### 风险2：Week 1 Day 3申请提交API未完成
   177	
   178	**概率：** 中  
   179	**影响：** 高  
   180	**降级方案：** 只做查询API，Day 4补申请提交
   181	
   182	### 风险3：Week 1 Day 4学工部审批未完成
   183	
   184	**概率：** 低  
   185	**影响：** 中  
   186	**降级方案：** 推到Week 2 Day 1，Week 1只验证辅导员审批
   187	
   188	### 风险4：Week 1 Day 5测试未通过
   189	
   190	**概率：** 中  
   191	**影响：** 高  
   192	**降级方案：** 周末加班修复，或Week 2 Day 1修复
   193	
   194	---
   195	
   196	## 验收检查清单
   197	
   198	### Week 0验收
   199	
   200	- [ ] contract-v0.1.md冻结
   201	- [ ] 前端可用mock跑通完整流程
   202	- [ ] 样例数据包含边界样本
   203	
   204	### Week 1验收
   205	
   206	- [ ] Django项目可运行
   207	- [ ] Seed数据加载成功
   208	- [ ] 4个API端点可用（登录、提交、审批、查询）
   209	- [ ] 最小角色校验实现
   210	- [ ] 4个自动化测试通过
   211	- [ ] 无P0/P1阻断bug
   212	
   213	---
   214	
   215	## 下一步（Week 2）
   216	
   217	**目标：** CSV导入v1
   218	
   219	**任务：**
   220	- Staging表设计
   221	- 校验报告
   222	- Upsert逻辑
   223	- 软停用基础
   224	- 导入审计基础
   225	
   226	**工期：** 5工作日
   227	
   228	---
   229	
   230	**计划负责人：** Claude Opus 4.7  

exec
/bin/bash -lc "rtk nl -ba docs/plans/week-0-1-execution-plan.md | rtk sed -n '1,130p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# Week 0-1 执行计划
     2	
     3	**版本：** v1.0  
     4	**创建日期：** 2026-05-30  
     5	**团队规模：** 2-3人  
     6	**总工期：** 6-7个工作日
     7	
     8	---
     9	
    10	## Week 0：契约冻结（1-2工作日）
    11	
    12	### 目标
    13	冻结v0.1最小可执行契约，为Week 1纵向切片提供稳定基础。
    14	
    15	### Day 0（0.5天）
    16	
    17	**任务：**
    18	- [x] 定义核心DTO（User、Application、Approval、DormCheckoutStatus）
    19	- [x] 定义状态枚举（5个枚举类型）
    20	- [x] 定义错误码（8个核心错误码）
    21	
    22	**责任人：** 后端负责人
    23	
    24	**交付物：** contract-v0.1.md初稿
    25	
    26	### Day 1（0.5-1天）
    27	
    28	**任务：**
    29	- [ ] 创建样例请求/响应（5个核心API端点）
    30	  - POST /api/auth/login
    31	  - POST /api/applications
    32	  - GET /api/applications/{id}
    33	  - POST /api/approvals/{id}/approve
    34	  - POST /api/approvals/{id}/reject
    35	- [ ] 创建Mock响应（宿舍清退Mock + 错误Mock）
    36	- [ ] 生成seed数据（10学生 + 2辅导员 + 1学工部 + 边界样本 + 默认密码）
    37	- [ ] 前端review可消费性
    38	- [ ] 业务方确认业务假设
    39	
    40	**责任人：** 后端负责人 + 前端负责人
    41	
    42	**交付物：** contract-v0.1.md冻结版
    43	
    44	**验收标准：**
    45	- [ ] 前端可用mock跑通登录→提交→审批→查询流程
    46	- [ ] 样例数据包含至少4个边界样本
    47	
    48	**降级条件：**
    49	- 如Day 1结束未完成前端review → 冻结当前版本，Week 1开始后异步review
    50	
    51	---
    52	
    53	## Week 1：后端纵向切片（5工作日）
    54	
    55	### 目标
    56	交付可运行的后端最小闭环：薄认证 + 申请提交 + 两级审批 + 状态查询 + Dorm Mock。
    57	
    58	### Day 1-2：可运行骨架
    59	
    60	**任务：**
    61	- [ ] Django项目初始化（settings分层、数据库配置）
    62	- [ ] 基础模型迁移（User、Application、Approval）
    63	- [ ] Seed命令实现（加载contract-v0.1.md中的样例数据）
    64	- [ ] 薄认证实现（学号/工号 + 密码，JWT）
    65	
    66	**责任人：** 后端负责人
    67	
    68	**交付物：**
    69	- Django项目可运行
    70	- `python manage.py seed_users` 可用
    71	- POST /api/auth/login 可用
    72	
    73	**验收标准：**
    74	- [ ] `python manage.py runserver` 启动成功
    75	- [ ] Seed数据加载成功（10学生 + 2辅导员 + 1学工部）
    76	- [ ] 登录API返回JWT token
    77	
    78	**降级条件：**
    79	- 如Day 2结束seed命令未完成 → 手动插入测试数据，Week 2补seed命令
    80	
    81	### Day 3-4：最小流程
    82	
    83	**任务：**
    84	- [ ] 申请提交API（POST /api/applications）
    85	  - 最小角色校验：只有学生可提交
    86	  - Dorm Mock集成：检查宿舍清退状态
    87	  - 状态初始化：pending_counselor
    88	  - 创建辅导员审批记录
    89	- [ ] 辅导员审批API（POST /api/approvals/{id}/approve|reject）
    90	  - 最小角色校验：只有对应班级辅导员可审批
    91	  - 状态流转：pending_counselor → pending_dean（通过）或 rejected（驳回）
    92	  - 创建学工部审批记录（通过时）
    93	- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
    94	  - 最小角色校验：只有学工部可审批
    95	  - 状态流转：pending_dean → approved（通过）或 rejected（驳回）
    96	- [ ] 状态查询API（GET /api/applications/{id}）
    97	  - 最小角色校验：学生只能查自己，辅导员/学工部可查所有
    98	
    99	**责任人：** 后端负责人
   100	
   101	**交付物：**
   102	- 4个API端点可用
   103	- 最小角色校验实现
   104	
   105	**验收标准：**
   106	- [ ] 学生可提交申请
   107	- [ ] 辅导员可审批（通过/驳回）
   108	- [ ] 学工部可审批（通过/驳回）
   109	- [ ] 状态查询返回完整申请信息和审批记录
   110	- [ ] 角色校验生效（学生不能审批，辅导员不能跨班级审批）
   111	
   112	**降级条件：**
   113	- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批、列表API
   114	- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证"提交→辅导员审批"闭环
   115	
   116	### Day 5：验收硬化
   117	
   118	**任务：**
   119	- [ ] 端到端自动化测试
   120	  - 测试1：学生登录 → 提交申请 → 辅导员审批通过 → 学工部审批通过 → 查询状态
   121	  - 测试2：学生登录 → 提交申请 → 辅导员审批驳回 → 查询状态
   122	  - 测试3：宿舍清退未完成 → 提交申请失败（DORM_BLOCKED）
   123	  - 测试4：角色校验（学生不能审批，辅导员不能跨班级审批）
   124	- [ ] 契约测试（API响应格式符合contract-v0.1.md）
   125	- [ ] 修复阻断bug
   126	- [ ] 输出Week 2任务清单
   127	
   128	**责任人：** 后端负责人 + QA
   129	
   130	**交付物：**

codex
初步看，6 项里有几项已经补上了具体内容，但 API 数量和降级条件仍有内部不一致。我再核对端点清单和 seed/Dorm mock 的可执行细节，确认是否是阻塞 Week 1 的问题。
exec
/bin/bash -lc 'rtk rg -n "DormCheckoutProvider|provider_unavailable|PROVIDER_UNAVAILABLE|UNKNOWN|unknown|默认返回|DORM_BLOCKED|STUDENT_NOT_FOUND|API失败|超时|失败" docs/contracts/contract-v0.1.md docs/plans/week-0-1-execution-plan.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/plans/week-0-1-execution-plan.md:122:  - 测试3：宿舍清退未完成 → 提交申请失败（DORM_BLOCKED）
docs/plans/week-0-1-execution-plan.md:174:**缓解措施：** 1-2工作日timebox，超时冻结当前假设进入Week 1
docs/contracts/contract-v0.1.md:68:    status: DormCheckoutStatus   # completed/pending/not_started/unknown
docs/contracts/contract-v0.1.md:122:    UNKNOWN = "unknown"              # 状态未知（API失败）
docs/contracts/contract-v0.1.md:142:| pending | 阻断提交 | 422 | DORM_BLOCKED |
docs/contracts/contract-v0.1.md:143:| not_started | 阻断提交 | 422 | DORM_BLOCKED |
docs/contracts/contract-v0.1.md:144:| unknown | 阻断提交 | 422 | DORM_BLOCKED |
docs/contracts/contract-v0.1.md:145:| provider_unavailable | 阻断提交 | 503 | PROVIDER_UNAVAILABLE |
docs/contracts/contract-v0.1.md:164:| VALIDATION_ERROR | 400 | 请求参数校验失败 | 必填字段缺失、格式错误 |
docs/contracts/contract-v0.1.md:169:| DORM_BLOCKED | 422 | 宿舍清退未完成 | 提交申请时宿舍未清退 |
docs/contracts/contract-v0.1.md:175:| PROVIDER_UNAVAILABLE | 503 | 外部服务不可用 | 宿舍清退API超时 |
docs/contracts/contract-v0.1.md:176:| INTERNAL_ERROR | 500 | 内部错误 | 数据库连接失败 |
docs/contracts/contract-v0.1.md:183:    "code": "DORM_BLOCKED",
docs/contracts/contract-v0.1.md:427:**DormCheckoutProvider Mock实现：**
docs/contracts/contract-v0.1.md:430:class MockDormCheckoutProvider:
docs/contracts/contract-v0.1.md:457:                status=DormCheckoutStatus.UNKNOWN,
docs/contracts/contract-v0.1.md:460:                provider_error_code="STUDENT_NOT_FOUND"
docs/contracts/contract-v0.1.md:464:        # 默认返回NOT_STARTED（而非completed，避免掩盖失败路径）
docs/contracts/contract-v0.1.md:500:    "code": "DORM_BLOCKED",

exec
/bin/bash -lc 'rtk rg -n "seed|students =|counselors =|deans =|class_mappings|2020099|2021001|2019001|T099|默认密码|password" docs/contracts/contract-v0.1.md docs/plans/week-0-1-execution-plan.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/plans/week-0-1-execution-plan.md:36:- [ ] 生成seed数据（10学生 + 2辅导员 + 1学工部 + 边界样本 + 默认密码）
docs/plans/week-0-1-execution-plan.md:70:- `python manage.py seed_users` 可用
docs/plans/week-0-1-execution-plan.md:79:- 如Day 2结束seed命令未完成 → 手动插入测试数据，Week 2补seed命令
docs/contracts/contract-v0.1.md:205:  "password": "password123"
docs/contracts/contract-v0.1.md:358:**默认密码：** 所有账号默认密码为 `password123`
docs/contracts/contract-v0.1.md:362:students = [
docs/contracts/contract-v0.1.md:378:counselors = [
docs/contracts/contract-v0.1.md:386:deans = [
docs/contracts/contract-v0.1.md:393:class_mappings = [
docs/contracts/contract-v0.1.md:403:{"user_id": "2020099", "name": "边界1", "role": "student", "class_id": "INVALID", "is_graduating": True, "graduation_year": 2024, "active": True}
docs/contracts/contract-v0.1.md:408:{"user_id": "T099", "name": "停用老师", "role": "counselor", "class_id": None, "active": False}
docs/contracts/contract-v0.1.md:413:{"user_id": "2021001", "name": "边界2", "role": "student", "class_id": "CS2021-01", "is_graduating": False, "graduation_year": 2025, "active": True}
docs/contracts/contract-v0.1.md:418:{"user_id": "2019001", "name": "边界3", "role": "student", "class_id": "CS2019-01", "is_graduating": True, "graduation_year": 2024, "active": True}
docs/contracts/contract-v0.1.md:455:            "2020099": DormCheckoutStatusDTO(
docs/contracts/contract-v0.1.md:456:                student_id="2020099",
docs/contracts/contract-v0.1.md:536:- 后端可用seed数据跑通端到端测试
docs/contracts/contract-v0.1.md:568:python manage.py seed_users
docs/contracts/contract-v0.1.md:569:python manage.py seed_class_mappings
docs/contracts/contract-v0.1.md:578:        'password': 'password123'

exec
/bin/bash -lc 'rtk rg -n "''^#### (GET|POST|PUT|PATCH|DELETE) |''^### [0-9].*API|端点|4个API|5个核心API|登录、提交、审批、查询|列表API" docs/contracts/contract-v0.1.md docs/plans/week-0-1-execution-plan.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/plans/week-0-1-execution-plan.md:29:- [ ] 创建样例请求/响应（5个核心API端点）
docs/plans/week-0-1-execution-plan.md:102:- 4个API端点可用
docs/plans/week-0-1-execution-plan.md:113:- 如Day 3结束申请提交API未完成 → 保留"提交→辅导员审批→查询"最短闭环，砍学工部审批、列表API
docs/plans/week-0-1-execution-plan.md:208:- [ ] 4个API端点可用（登录、提交、审批、查询）
docs/contracts/contract-v0.1.md:195:## 4. API端点
docs/contracts/contract-v0.1.md:199:#### POST /api/auth/login
docs/contracts/contract-v0.1.md:225:#### POST /api/applications
docs/contracts/contract-v0.1.md:251:#### GET /api/applications/{application_id}
docs/contracts/contract-v0.1.md:282:#### POST /api/approvals/{approval_id}/approve
docs/contracts/contract-v0.1.md:305:#### POST /api/approvals/{approval_id}/reject
docs/contracts/contract-v0.1.md:330:#### GET /api/applications
docs/contracts/contract-v0.1.md:523:- API端点（认证、申请、审批、查询）
docs/contracts/contract-v0.1.md:560:  // ... 其他端点

codex
结论：**还没有完全达到“可执行契约”标准，不建议直接开始 Week 1 的完整实施**。可以先启动不受争议影响的 Day 1 骨架、模型、seed、认证准备，但应先用半天把下面几个契约不一致点修掉再冻结。

**6 个问题核对结果**

1. **UserDTO 字段可选性：基本已解决**
   [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:22) 已把 `class_id`、`is_graduating`、`graduation_year` 标为 Optional。  
   但登录响应里的 `user` 示例只返回 `user_id/name/role/class_id`，不包含 `active/is_graduating/graduation_year`，和 `UserDTO` 不完全一致：[contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:214)。建议明确这是 `AuthUserDTO`，或让响应严格返回 `UserDTO`。

2. **状态机契约表：已解决**
   申请状态流转、宿舍清退阻断规则、角色权限矩阵都已补上：[contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:129)。对 Week 1 最小闭环足够。

3. **Dorm Mock 失败策略：部分解决**
   已覆盖 `completed/pending/not_started/unknown`，默认返回 `NOT_STARTED` 避免误放行：[contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:430)。  
   但状态表定义了 `provider_unavailable -> 503 PROVIDER_UNAVAILABLE`：[contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:145)，Mock 实现和错误 Mock 没有可触发的 503 样本。建议加一个固定学号，如 `2020503`，返回/抛出 `PROVIDER_UNAVAILABLE`，并补 503 错误响应和测试。

4. **seed 数据完整性：基本已解决**
   有 10 学生、2 辅导员、1 学工部、班级映射、默认密码、4 个边界样本：[contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:358)。这项可以支持 Week 1。

5. **API 端点数量统一：未解决，仍是主要阻塞**
   契约实际列了 **6 个 HTTP 路由**：login、submit、detail、approve、reject、list：[contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:199)。  
   计划里又写 Day 1 是 **5 个核心 API 端点**：[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:29)，Week 1 交付和验收写 **4 个 API 端点**：[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:102)、[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:208)。  
   建议立即统一为一种口径：要么 Week 1 实施 5 个 HTTP 路由并移除 `GET /api/applications` 列表接口；要么保留列表接口并把计划全部改成 6 个 HTTP 路由。

6. **降级条件改进：部分解决，但仍有矛盾**
   Day 3-4 的降级写“保留提交→辅导员审批→查询，砍学工部审批、列表API”是合理方向：[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:112)。  
   但风险表又写“申请提交 API 未完成 → 只做查询 API，Day 4 补申请提交”：[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:176)，这和纵向切片目标冲突。Day 5 的“周末加班修复”也不是可执行的降级条件：[week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:188)。

**最终判断**

当前文档是“接近可执行契约”，但还不是冻结版。阻塞点主要是 **API 路由数量不统一**、**Dorm Mock 缺 503 失败路径**、**降级规则仍有自相矛盾**。这些都是小修，不需要重新设计。

建议先修这 3 点，然后就可以开始 Week 1。若必须今天开工，可以只开 Day 1 的 Django 骨架、基础模型、seed、登录，不要先实现申请/审批路由，避免按错误端点口径返工。
tokens used
48,791

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
