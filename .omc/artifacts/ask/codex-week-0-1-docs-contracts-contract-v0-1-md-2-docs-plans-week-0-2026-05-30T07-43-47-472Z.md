# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-05-30T07:43:47.473Z

## Original task

请审查刚创建的两个Week 0交付物：1) docs/contracts/contract-v0.1.md 2) docs/plans/week-0-1-execution-plan.md。重点评估：1) v0.1契约是否满足'最小可执行契约'标准？是否有遗漏或过度设计？ 2) Week 0-1执行计划是否可行？任务分解是否合理？降级条件是否充分？ 3) 这两个文档是否足以支撑Week 1纵向切片开发？ 4) 下一步应该做什么？是立即开始Week 1实施，还是需要补充其他准备工作？

## Final prompt

请审查刚创建的两个Week 0交付物：1) docs/contracts/contract-v0.1.md 2) docs/plans/week-0-1-execution-plan.md。重点评估：1) v0.1契约是否满足'最小可执行契约'标准？是否有遗漏或过度设计？ 2) Week 0-1执行计划是否可行？任务分解是否合理？降级条件是否充分？ 3) 这两个文档是否足以支撑Week 1纵向切片开发？ 4) 下一步应该做什么？是立即开始Week 1实施，还是需要补充其他准备工作？

## Raw output

```text
**审查结论：暂不建议立即开始 Week 1 实施。**

两份文档方向是对的，已经接近“可执行契约”，但还差几个会直接影响 Week 1 纵向切片落地的关键点。建议先用半天把契约和计划修正到可执行状态，再进入 Week 1。

**主要问题**

1. **UserDTO 与样例数据不一致，会卡住建模和 seed。**  
   [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:16) 把 `is_graduating`、`graduation_year` 定义为所有用户必填，但辅导员/学工部样例没有这些字段 [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:338)。应改成学生专属可选字段，或拆成 `StudentDTO / StaffDTO`。

2. **缺少 Week 1 最关键的状态机契约。**  
   API 示例有提交、审批、驳回，但契约没有明确“当前状态 + 当前审批节点 + 角色 + 决策 → 下一个状态/审批记录”的表。Week 1 计划里才写了部分规则 [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:79)，应前移到契约，否则后端测试和前端 mock 会各自理解。

3. **Dorm Mock 的失败/unknown 策略不明确。**  
   契约定义了 `UNKNOWN` [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:122)，也定义了 `PROVIDER_UNAVAILABLE` [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:144)，但提交申请时遇到 `unknown` 是阻断、允许人工证明，还是 503，没有写死。更关键的是 mock 默认对未知学生返回 `completed` [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:417)，会掩盖失败路径。

4. **Seed/fixture 不满足计划自己的验收口径。**  
   计划要求 `10学生 + 2辅导员 + 1学工部 + 边界样本` [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:31)，但契约只给了 3 个正常学生和若干零散边界样本 [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:329)。还缺默认密码/密码策略，薄认证无法稳定跑 seed 登录。

5. **API 端点数量和验收表述不一致。**  
   契约实际有登录、创建、详情、审批通过、审批驳回、列表 6 类端点 [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:168)，计划有时说 5 个 API [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:29)，Week 1 又说 4 个端点 [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:97)。这会影响任务拆分和验收。

6. **执行计划的降级条件不够好。**  
   “Day 3 申请提交未完成 → 只做查询 API” [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:108) 会破坏纵向切片价值。更合理的降级是保留“提交→辅导员审批→查询”最短闭环，砍列表、学工部审批、复杂错误、完整 seed 等外围内容。  
   “周末加班” [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:135) 也不是工程降级条件，应改成明确的范围裁剪或延期规则。

**是否满足最小可执行契约？**

部分满足。DTO、枚举、错误码、样例、mock 都有了，范围也基本克制，没有把附件、通知、微信 OAuth 拉进 v0.1，这是对的 [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:480)。

但“可执行”还不够：缺状态机表、角色权限矩阵、seed 登录凭据、Dorm 异常策略、端点验收口径统一。这些不是锦上添花，是 Week 1 开发会马上碰到的决策。

**是否足以支撑 Week 1？**

还不够。现在可以支撑讨论和原型，但不够支撑 5 天内稳定交付后端纵向切片。若直接开工，最可能在模型字段、审批流转、Dorm 异常、测试数据上返工。

**下一步**

建议不要大改设计，只做一次小补丁：

1. 修正 `UserDTO` 字段可选性或拆分用户 DTO。
2. 补一张状态流转/权限矩阵。
3. 明确 Dorm `pending/not_started/unknown/provider_unavailable` 的提交行为。
4. 补齐 10 个学生、2 个辅导员、1 个学工部、默认密码、当前审批人 fixture。
5. 统一 API 数量和 Week 1 验收口径。
6. 把降级策略改成“保留最短纵向闭环，裁剪外围功能”。

这些完成后，可以立即进入 Week 1 实施；不需要再做更大的架构准备。


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
session id: 019e77d4-a50d-7911-9d50-1e03c38121df
--------
user
请审查刚创建的两个Week 0交付物：1) docs/contracts/contract-v0.1.md 2) docs/plans/week-0-1-execution-plan.md。重点评估：1) v0.1契约是否满足'最小可执行契约'标准？是否有遗漏或过度设计？ 2) Week 0-1执行计划是否可行？任务分解是否合理？降级条件是否充分？ 3) 这两个文档是否足以支撑Week 1纵向切片开发？ 4) 下一步应该做什么？是立即开始Week 1实施，还是需要补充其他准备工作？
codex
我会按项目要求先读取 RTK 和评审协议，再审查这两个文档本身；结论会按风险/遗漏优先排序，而不是只做摘要。
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
我已读取项目的审查协议。这里用户请求的是我直接做文档评审；我会遵循其中“优先列问题、给出修复建议和结论”的格式，但不额外创建 OMC 审查请求文档，除非你后续要求走完整归档流程。
exec
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
 M .omc/state/hud-stdin-cache.json
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
/bin/bash -lc 'rtk nl -ba docs/contracts/contract-v0.1.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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
    18	    user_id: str              # 学号/工号
    19	    name: str                 # 姓名
    20	    role: UserRole            # 角色：student/counselor/dean
    21	    class_id: Optional[str]   # 班级ID（学生必填）
    22	    is_graduating: bool       # 是否毕业生（学生）
    23	    graduation_year: int      # 毕业年份（学生）
    24	    active: bool              # 账号是否激活
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
   125	---
   126	
   127	## 3. 错误码
   128	
   129	### 3.1 业务错误 (4xx)
   130	
   131	| 错误码 | HTTP状态 | 说明 | 示例场景 |
   132	|--------|---------|------|---------|
   133	| VALIDATION_ERROR | 400 | 请求参数校验失败 | 必填字段缺失、格式错误 |
   134	| AUTH_REQUIRED | 401 | 未认证 | Token缺失或过期 |
   135	| FORBIDDEN | 403 | 无权限 | 学生访问他人申请 |
   136	| NOT_FOUND | 404 | 资源不存在 | 申请ID不存在 |
   137	| CONFLICT | 409 | 资源冲突 | 重复提交申请 |
   138	| DORM_BLOCKED | 422 | 宿舍清退未完成 | 提交申请时宿舍未清退 |
   139	
   140	### 3.2 系统错误 (5xx)
   141	
   142	| 错误码 | HTTP状态 | 说明 | 示例场景 |
   143	|--------|---------|------|---------|
   144	| PROVIDER_UNAVAILABLE | 503 | 外部服务不可用 | 宿舍清退API超时 |
   145	| INTERNAL_ERROR | 500 | 内部错误 | 数据库连接失败 |
   146	
   147	### 3.3 错误响应格式
   148	
   149	```json
   150	{
   151	  "error": {
   152	    "code": "DORM_BLOCKED",
   153	    "message": "宿舍清退未完成，无法提交申请",
   154	    "details": {
   155	      "student_id": "2020001",
   156	      "dorm_status": "pending"
   157	    }
   158	  }
   159	}
   160	```
   161	
   162	---
   163	
   164	## 4. API端点
   165	
   166	### 4.1 认证
   167	
   168	#### POST /api/auth/login
   169	
   170	**请求：**
   171	```json
   172	{
   173	  "user_id": "2020001",
   174	  "password": "password123"
   175	}
   176	```
   177	
   178	**响应：**
   179	```json
   180	{
   181	  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
   182	  "token_type": "Bearer",
   183	  "user": {
   184	    "user_id": "2020001",
   185	    "name": "张三",
   186	    "role": "student",
   187	    "class_id": "CS2020-01"
   188	  }
   189	}
   190	```
   191	
   192	### 4.2 申请
   193	
   194	#### POST /api/applications
   195	
   196	**请求：**
   197	```json
   198	{
   199	  "reason": "毕业离校",
   200	  "leave_date": "2024-06-30"
   201	}
   202	```
   203	
   204	**响应：**
   205	```json
   206	{
   207	  "application_id": "app_001",
   208	  "student_id": "2020001",
   209	  "student_name": "张三",
   210	  "class_id": "CS2020-01",
   211	  "reason": "毕业离校",
   212	  "leave_date": "2024-06-30",
   213	  "status": "pending_counselor",
   214	  "dorm_checkout_status": "completed",
   215	  "created_at": "2024-05-30T10:00:00Z",
   216	  "updated_at": "2024-05-30T10:00:00Z"
   217	}
   218	```
   219	
   220	#### GET /api/applications/{application_id}
   221	
   222	**响应：**
   223	```json
   224	{
   225	  "application_id": "app_001",
   226	  "student_id": "2020001",
   227	  "student_name": "张三",
   228	  "class_id": "CS2020-01",
   229	  "reason": "毕业离校",
   230	  "leave_date": "2024-06-30",
   231	  "status": "pending_counselor",
   232	  "dorm_checkout_status": "completed",
   233	  "approvals": [
   234	    {
   235	      "approval_id": "apv_001",
   236	      "step": "counselor",
   237	      "approver_id": "T001",
   238	      "approver_name": "李老师",
   239	      "decision": "pending",
   240	      "comment": null,
   241	      "decided_at": null
   242	    }
   243	  ],
   244	  "created_at": "2024-05-30T10:00:00Z",
   245	  "updated_at": "2024-05-30T10:00:00Z"
   246	}
   247	```
   248	
   249	### 4.3 审批
   250	
   251	#### POST /api/approvals/{approval_id}/approve
   252	
   253	**请求：**
   254	```json
   255	{
   256	  "comment": "同意离校"
   257	}
   258	```
   259	
   260	**响应：**
   261	```json
   262	{
   263	  "approval_id": "apv_001",
   264	  "application_id": "app_001",
   265	  "step": "counselor",
   266	  "approver_id": "T001",
   267	  "approver_name": "李老师",
   268	  "decision": "approved",
   269	  "comment": "同意离校",
   270	  "decided_at": "2024-05-30T11:00:00Z"
   271	}
   272	```
   273	
   274	#### POST /api/approvals/{approval_id}/reject
   275	
   276	**请求：**
   277	```json
   278	{
   279	  "comment": "材料不齐全"
   280	}
   281	```
   282	
   283	**响应：**
   284	```json
   285	{
   286	  "approval_id": "apv_001",
   287	  "application_id": "app_001",
   288	  "step": "counselor",
   289	  "approver_id": "T001",
   290	  "approver_name": "李老师",
   291	  "decision": "rejected",
   292	  "comment": "材料不齐全",
   293	  "decided_at": "2024-05-30T11:00:00Z"
   294	}
   295	```
   296	
   297	### 4.4 查询
   298	
   299	#### GET /api/applications
   300	
   301	**查询参数：**
   302	- `status`: ApplicationStatus（可选）
   303	- `student_id`: 学号（可选，辅导员/学工部可用）
   304	
   305	**响应：**
   306	```json
   307	{
   308	  "applications": [
   309	    {
   310	      "application_id": "app_001",
   311	      "student_id": "2020001",
   312	      "student_name": "张三",
   313	      "status": "pending_counselor",
   314	      "created_at": "2024-05-30T10:00:00Z"
   315	    }
   316	  ],
   317	  "total": 1
   318	}
   319	```
   320	
   321	---
   322	
   323	## 5. 样例数据
   324	
   325	### 5.1 正常样本
   326	
   327	**学生：**
   328	```python
   329	students = [
   330	    {"user_id": "2020001", "name": "张三", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
   331	    {"user_id": "2020002", "name": "李四", "role": "student", "class_id": "CS2020-01", "is_graduating": True, "graduation_year": 2024, "active": True},
   332	    {"user_id": "2020003", "name": "王五", "role": "student", "class_id": "CS2020-02", "is_graduating": True, "graduation_year": 2024, "active": True},
   333	]
   334	```
   335	
   336	**辅导员：**
   337	```python
   338	counselors = [
   339	    {"user_id": "T001", "name": "李老师", "role": "counselor", "class_id": None, "active": True},
   340	    {"user_id": "T002", "name": "王老师", "role": "counselor", "class_id": None, "active": True},
   341	]
   342	```
   343	
   344	**学工部：**
   345	```python
   346	deans = [
   347	    {"user_id": "D001", "name": "赵主任", "role": "dean", "class_id": None, "active": True},
   348	]
   349	```
   350	
   351	**班级映射：**
   352	```python
   353	class_mappings = [
   354	    {"class_id": "CS2020-01", "counselor_id": "T001"},
   355	    {"class_id": "CS2020-02", "counselor_id": "T002"},
   356	]
   357	```
   358	
   359	### 5.2 边界样本
   360	
   361	**无班级映射：**
   362	```python
   363	{"user_id": "2020099", "name": "边界1", "role": "student", "class_id": "INVALID", "is_graduating": True, "graduation_year": 2024, "active": True}
   364	```
   365	
   366	**辅导员停用：**
   367	```python
   368	{"user_id": "T099", "name": "停用老师", "role": "counselor", "class_id": None, "active": False}
   369	```
   370	
   371	**非毕业生：**
   372	```python
   373	{"user_id": "2021001", "name": "边界2", "role": "student", "class_id": "CS2021-01", "is_graduating": False, "graduation_year": 2025, "active": True}
   374	```
   375	
   376	**延期毕业：**
   377	```python
   378	{"user_id": "2019001", "name": "边界3", "role": "student", "class_id": "CS2019-01", "is_graduating": True, "graduation_year": 2024, "active": True}
   379	```
   380	
   381	---
   382	
   383	## 6. Mock响应
   384	
   385	### 6.1 宿舍清退Mock
   386	
   387	**DormCheckoutProvider Mock实现：**
   388	
   389	```python
   390	class MockDormCheckoutProvider:
   391	    def check_status(self, student_id: str) -> DormCheckoutStatusDTO:
   392	        # 固定返回规则
   393	        mock_data = {
   394	            "2020001": DormCheckoutStatusDTO(
   395	                student_id="2020001",
   396	                status=DormCheckoutStatus.COMPLETED,
   397	                checked_at="2024-05-15T10:00:00Z",
   398	                blocking_reason=None,
   399	                provider_error_code=None
   400	            ),
   401	            "2020002": DormCheckoutStatusDTO(
   402	                student_id="2020002",
   403	                status=DormCheckoutStatus.PENDING,
   404	                checked_at=None,
   405	                blocking_reason="宿舍物品未清理",
   406	                provider_error_code=None
   407	            ),
   408	            "2020003": DormCheckoutStatusDTO(
   409	                student_id="2020003",
   410	                status=DormCheckoutStatus.NOT_STARTED,
   411	                checked_at=None,
   412	                blocking_reason="未提交清退申请",
   413	                provider_error_code=None
   414	            ),
   415	        }
   416	        
   417	        # 默认返回completed
   418	        return mock_data.get(student_id, DormCheckoutStatusDTO(
   419	            student_id=student_id,
   420	            status=DormCheckoutStatus.COMPLETED,
   421	            checked_at="2024-05-15T10:00:00Z",
   422	            blocking_reason=None,
   423	            provider_error_code=None
   424	        ))
   425	```
   426	
   427	### 6.2 错误Mock
   428	
   429	**401 Unauthorized：**
   430	```json
   431	{
   432	  "error": {
   433	    "code": "AUTH_REQUIRED",
   434	    "message": "Token缺失或过期"
   435	  }
   436	}
   437	```
   438	
   439	**403 Forbidden：**
   440	```json
   441	{
   442	  "error": {
   443	    "code": "FORBIDDEN",
   444	    "message": "无权限访问此资源"
   445	  }
   446	}
   447	```
   448	
   449	**422 Dorm Blocked：**
   450	```json
   451	{
   452	  "error": {
   453	    "code": "DORM_BLOCKED",
   454	    "message": "宿舍清退未完成，无法提交申请",
   455	    "details": {
   456	      "student_id": "2020002",
   457	      "dorm_status": "pending",
   458	      "blocking_reason": "宿舍物品未清理"
   459	    }
   460	  }
   461	}
   462	```
   463	
   464	---
   465	
   466	## 7. 变更日志
   467	
   468	### v0.1 (2026-05-30)
   469	
   470	**初始版本 - 最小可执行契约**
   471	
   472	**包含内容：**
   473	- 核心DTO（User、Application、Approval、DormCheckoutStatus）
   474	- 状态枚举（UserRole、ApplicationStatus、ApprovalStep、ApprovalDecision、DormCheckoutStatus）
   475	- 错误码（8个核心错误码）
   476	- API端点（认证、申请、审批、查询）
   477	- 样例数据（正常样本 + 边界样本）
   478	- Mock响应（宿舍清退Mock + 错误Mock）
   479	
   480	**不包含内容（v0.2）：**
   481	- 附件相关DTO和API
   482	- 通知相关DTO和API
   483	- 微信OAuth相关API
   484	- 完整RBAC权限矩阵
   485	- 审批转办、撤回、驳回重提
   486	
   487	**验收标准：**
   488	- 前端可用mock跑通登录→提交→审批→查询流程
   489	- 后端可用seed数据跑通端到端测试
   490	
   491	---
   492	
   493	## 8. 使用说明
   494	
   495	### 8.1 前端使用
   496	
   497	**Mock Server配置：**
   498	```javascript
   499	// mock/handlers.js
   500	export const handlers = [
   501	  rest.post('/api/auth/login', (req, res, ctx) => {
   502	    return res(ctx.json({
   503	      access_token: 'mock_token',
   504	      token_type: 'Bearer',
   505	      user: {
   506	        user_id: '2020001',
   507	        name: '张三',
   508	        role: 'student',
   509	        class_id: 'CS2020-01'
   510	      }
   511	    }))
   512	  }),
   513	  // ... 其他端点
   514	]
   515	```
   516	
   517	### 8.2 后端使用
   518	
   519	**Seed数据加载：**
   520	```bash
   521	python manage.py seed_users
   522	python manage.py seed_class_mappings
   523	```
   524	
   525	**端到端测试：**
   526	```python
   527	def test_application_flow():
   528	    # 1. 学生登录
   529	    response = client.post('/api/auth/login', {
   530	        'user_id': '2020001',
   531	        'password': 'password123'
   532	    })
   533	    token = response.json()['access_token']
   534	    
   535	    # 2. 提交申请
   536	    response = client.post('/api/applications', 
   537	        headers={'Authorization': f'Bearer {token}'},
   538	        json={'reason': '毕业离校', 'leave_date': '2024-06-30'}
   539	    )
   540	    app_id = response.json()['application_id']
   541	    
   542	    # 3. 辅导员审批
   543	    # 4. 学工部审批
   544	    # 5. 查询状态
   545	```
   546	
   547	---
   548	
   549	**契约负责人：** Claude Opus 4.7  
   550	**前端Review：** 待确认  
   551	**业务确认：** 待确认  
   552	**冻结日期：** 2026-05-30  
   553	**下一版本：** v0.2（Week 3）

exec
/bin/bash -lc 'rtk nl -ba docs/plans/week-0-1-execution-plan.md' in /home/caohui/projects/graduation-leave-system
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
    29	- [ ] 创建样例请求/响应（5个API端点）
    30	- [ ] 创建Mock响应（宿舍清退Mock + 错误Mock）
    31	- [ ] 生成seed数据（10学生 + 2辅导员 + 1学工部 + 边界样本）
    32	- [ ] 前端review可消费性
    33	- [ ] 业务方确认业务假设
    34	
    35	**责任人：** 后端负责人 + 前端负责人
    36	
    37	**交付物：** contract-v0.1.md冻结版
    38	
    39	**验收标准：**
    40	- [ ] 前端可用mock跑通登录→提交→审批→查询流程
    41	- [ ] 样例数据包含至少4个边界样本
    42	
    43	**降级条件：**
    44	- 如Day 1结束未完成前端review → 冻结当前版本，Week 1开始后异步review
    45	
    46	---
    47	
    48	## Week 1：后端纵向切片（5工作日）
    49	
    50	### 目标
    51	交付可运行的后端最小闭环：薄认证 + 申请提交 + 两级审批 + 状态查询 + Dorm Mock。
    52	
    53	### Day 1-2：可运行骨架
    54	
    55	**任务：**
    56	- [ ] Django项目初始化（settings分层、数据库配置）
    57	- [ ] 基础模型迁移（User、Application、Approval）
    58	- [ ] Seed命令实现（加载contract-v0.1.md中的样例数据）
    59	- [ ] 薄认证实现（学号/工号 + 密码，JWT）
    60	
    61	**责任人：** 后端负责人
    62	
    63	**交付物：**
    64	- Django项目可运行
    65	- `python manage.py seed_users` 可用
    66	- POST /api/auth/login 可用
    67	
    68	**验收标准：**
    69	- [ ] `python manage.py runserver` 启动成功
    70	- [ ] Seed数据加载成功（10学生 + 2辅导员 + 1学工部）
    71	- [ ] 登录API返回JWT token
    72	
    73	**降级条件：**
    74	- 如Day 2结束seed命令未完成 → 手动插入测试数据，Week 2补seed命令
    75	
    76	### Day 3-4：最小流程
    77	
    78	**任务：**
    79	- [ ] 申请提交API（POST /api/applications）
    80	  - 最小角色校验：只有学生可提交
    81	  - Dorm Mock集成：检查宿舍清退状态
    82	  - 状态初始化：pending_counselor
    83	  - 创建辅导员审批记录
    84	- [ ] 辅导员审批API（POST /api/approvals/{id}/approve|reject）
    85	  - 最小角色校验：只有对应班级辅导员可审批
    86	  - 状态流转：pending_counselor → pending_dean（通过）或 rejected（驳回）
    87	  - 创建学工部审批记录（通过时）
    88	- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
    89	  - 最小角色校验：只有学工部可审批
    90	  - 状态流转：pending_dean → approved（通过）或 rejected（驳回）
    91	- [ ] 状态查询API（GET /api/applications/{id}）
    92	  - 最小角色校验：学生只能查自己，辅导员/学工部可查所有
    93	
    94	**责任人：** 后端负责人
    95	
    96	**交付物：**
    97	- 4个API端点可用
    98	- 最小角色校验实现
    99	
   100	**验收标准：**
   101	- [ ] 学生可提交申请
   102	- [ ] 辅导员可审批（通过/驳回）
   103	- [ ] 学工部可审批（通过/驳回）
   104	- [ ] 状态查询返回完整申请信息和审批记录
   105	- [ ] 角色校验生效（学生不能审批，辅导员不能跨班级审批）
   106	
   107	**降级条件：**
   108	- 如Day 3结束申请提交API未完成 → 只做查询API，Day 4补申请提交
   109	- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证辅导员审批
   110	
   111	### Day 5：验收硬化
   112	
   113	**任务：**
   114	- [ ] 端到端自动化测试
   115	  - 测试1：学生登录 → 提交申请 → 辅导员审批通过 → 学工部审批通过 → 查询状态
   116	  - 测试2：学生登录 → 提交申请 → 辅导员审批驳回 → 查询状态
   117	  - 测试3：宿舍清退未完成 → 提交申请失败（DORM_BLOCKED）
   118	  - 测试4：角色校验（学生不能审批，辅导员不能跨班级审批）
   119	- [ ] 契约测试（API响应格式符合contract-v0.1.md）
   120	- [ ] 修复阻断bug
   121	- [ ] 输出Week 2任务清单
   122	
   123	**责任人：** 后端负责人 + QA
   124	
   125	**交付物：**
   126	- 4个自动化测试通过
   127	- Week 2任务清单
   128	
   129	**验收标准：**
   130	- [ ] 所有测试通过
   131	- [ ] 无P0/P1阻断bug
   132	- [ ] Week 2任务清单明确
   133	
   134	**降级条件：**
   135	- 如Day 5结束仍有P0 bug → 周末加班修复，或Week 2 Day 1修复
   136	
   137	---
   138	
   139	## 并行任务
   140	
   141	### 前端准备（Week 1期间）
   142	
   143	**任务：**
   144	- [ ] 技术栈选型确认（微信小程序框架）
   145	- [ ] 项目初始化
   146	- [ ] Mock Server配置（基于contract-v0.1.md）
   147	- [ ] API Client封装
   148	
   149	**责任人：** 前端负责人
   150	
   151	**时间：** Week 1 Day 1-5（与后端并行）
   152	
   153	**交付物：**
   154	- 微信小程序项目可运行
   155	- Mock Server可用
   156	- API Client可用
   157	
   158	**验收标准：**
   159	- [ ] 可用mock跑通登录→提交→审批→查询流程
   160	
   161	---
   162	
   163	## 风险和降级
   164	
   165	### 风险1：Week 0契约定义延期
   166	
   167	**概率：** 中  
   168	**影响：** 高  
   169	**缓解措施：** 1-2工作日timebox，超时冻结当前假设进入Week 1
   170	
   171	### 风险2：Week 1 Day 3申请提交API未完成
   172	
   173	**概率：** 中  
   174	**影响：** 高  
   175	**降级方案：** 只做查询API，Day 4补申请提交
   176	
   177	### 风险3：Week 1 Day 4学工部审批未完成
   178	
   179	**概率：** 低  
   180	**影响：** 中  
   181	**降级方案：** 推到Week 2 Day 1，Week 1只验证辅导员审批
   182	
   183	### 风险4：Week 1 Day 5测试未通过
   184	
   185	**概率：** 中  
   186	**影响：** 高  
   187	**降级方案：** 周末加班修复，或Week 2 Day 1修复
   188	
   189	---
   190	
   191	## 验收检查清单
   192	
   193	### Week 0验收
   194	
   195	- [ ] contract-v0.1.md冻结
   196	- [ ] 前端可用mock跑通完整流程
   197	- [ ] 样例数据包含边界样本
   198	
   199	### Week 1验收
   200	
   201	- [ ] Django项目可运行
   202	- [ ] Seed数据加载成功
   203	- [ ] 4个API端点可用（登录、提交、审批、查询）
   204	- [ ] 最小角色校验实现
   205	- [ ] 4个自动化测试通过
   206	- [ ] 无P0/P1阻断bug
   207	
   208	---
   209	
   210	## 下一步（Week 2）
   211	
   212	**目标：** CSV导入v1
   213	
   214	**任务：**
   215	- Staging表设计
   216	- 校验报告
   217	- Upsert逻辑
   218	- 软停用基础
   219	- 导入审计基础
   220	
   221	**工期：** 5工作日
   222	
   223	---
   224	
   225	**计划负责人：** Claude Opus 4.7  
   226	**创建日期：** 2026-05-30  
   227	**状态：** 已批准，可执行

codex
我已经拿到两份文档的逐行内容。接下来会补一点项目背景：看现有需求/架构/数据源共识，避免只按这两份文档孤立判断。
exec
/bin/bash -lc 'rtk ls -la' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
.agents/
.claude/
.codex/
.git/
.omc/
PRD/
backend/
docker/
docs/
frontend/
plans/
.gitignore  664B
AGENTS.md  632B
CLAUDE.md  2.8K
毕业离校系统用户文档.zip  8.2K

exec
/bin/bash -lc 'rtk rg --files docs | head -80' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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
docs/用户设计说明书.md
docs/PROJECT-SUMMARY.md
docs/contracts/contract-v0.1.md
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md
docs/design/2026-05-27-system-design.md
docs/数据确认清单.md
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

exec
/bin/bash -lc "rtk rg -n \"纵向切片|Week 1|最小可执行|CSV|宿舍|微信|审批|离校\" docs -g '*.md'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/微信小程序申请说明.md:1:# 微信小程序申请说明
docs/微信小程序申请说明.md:23:#### 2. 需付费使用微信手机号快捷登录接口
docs/微信小程序申请说明.md:26:- **费用支付：** 费用支付给微信平台
docs/微信小程序申请说明.md:27:- **学校主体优势：** 学校主体的小程序使用该接口时，微信不收取费用
docs/微信小程序申请说明.md:38:### 步骤1：访问微信公众平台
docs/微信小程序申请说明.md:61:登录邮箱，点击微信发送的激活链接。
docs/微信小程序申请说明.md:77:1. **邮箱要求：** 注册邮箱不能与其他微信公众号或小程序重复使用
docs/微信小程序申请说明.md:78:2. **管理员信息：** 管理员需要进行微信扫码验证
docs/微信小程序申请说明.md:86:- [微信小程序备案说明](./微信小程序备案说明.md)
docs/微信小程序申请说明.md:87:- [微信公众平台官方文档](https://developers.weixin.qq.com/miniprogram/introduction/)
docs/用户设计说明书.md:1:# 毕业生离校申请审批系统 - 用户设计说明书
docs/用户设计说明书.md:13:本系统旨在实现毕业生离校申请的在线化、规范化管理，替代传统纸质审批流程，提高审批效率，减少人工成本。
docs/用户设计说明书.md:17:- **学生端：** 在线提交离校申请、上传证明材料、查看审批进度、接收审批通知
docs/用户设计说明书.md:18:- **辅导员端：** 审批本年级学生的离校申请、查看审批历史、接收待办提醒
docs/用户设计说明书.md:19:- **学工部端：** 审批所有学生的离校申请、查看全校审批统计、导出审批数据
docs/用户设计说明书.md:25:- **微信小程序：** 微信内使用，无需安装
docs/用户设计说明书.md:35:学生登录 → 填写申请信息 → 上传证明材料 → 提交申请 → 等待审批
docs/用户设计说明书.md:40:- 计划离校日期
docs/用户设计说明书.md:44:- 宿舍清退证明（照片或PDF）
docs/用户设计说明书.md:48:### 2.2 审批流程
docs/用户设计说明书.md:51:学生提交 → 辅导员审批 → 学工部审批 → 审批完成
docs/用户设计说明书.md:56:**审批时限：**
docs/用户设计说明书.md:57:- 辅导员审批：提交后1个工作日内
docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
docs/用户设计说明书.md:59:- 超时提醒：系统自动发送微信通知
docs/用户设计说明书.md:61:**审批结果：**
docs/用户设计说明书.md:62:- **通过：** 进入下一审批环节或完成审批
docs/用户设计说明书.md:67:**微信通知场景：**
docs/用户设计说明书.md:69:- 辅导员审批通过 → 通知学生和学工部
docs/用户设计说明书.md:71:- 学工部审批通过 → 通知学生（审批完成）
docs/用户设计说明书.md:73:- 审批超时 → 通知审批人
docs/用户设计说明书.md:87:**微信授权登录：**
docs/用户设计说明书.md:89:- 支持微信消息推送
docs/用户设计说明书.md:94:**宿舍管理系统对接：**
docs/用户设计说明书.md:95:- 学生提交申请时，系统自动验证宿舍是否已清退
docs/用户设计说明书.md:96:- 验证失败时，提示学生先完成宿舍清退
docs/用户设计说明书.md:128:| **辅导员** | 本年级学生 | 审批申请、查看历史、接收通知 |
docs/用户设计说明书.md:129:| **学工部** | 全校学生 | 审批申请、查看统计、导出数据 |
docs/用户设计说明书.md:135:- ✓ 创建离校申请
docs/用户设计说明书.md:140:- ✓ 查看审批历史
docs/用户设计说明书.md:145:- ✓ 审批负责班级学生的申请（通过/驳回）
docs/用户设计说明书.md:146:- ✓ 填写审批意见
docs/用户设计说明书.md:147:- ✓ 查看审批历史
docs/用户设计说明书.md:148:- ✓ 接收待审批通知
docs/用户设计说明书.md:149:- ✗ 审批其他班级学生
docs/用户设计说明书.md:153:- ✓ 审批所有学生的申请（通过/驳回）
docs/用户设计说明书.md:154:- ✓ 填写审批意见
docs/用户设计说明书.md:155:- ✓ 查看全校审批统计
docs/用户设计说明书.md:156:- ✓ 导出审批数据（Excel）
docs/用户设计说明书.md:157:- ✓ 查看审批历史
docs/用户设计说明书.md:209:**Q2：微信绑定失败怎么办？**
docs/用户设计说明书.md:218:**Q5：审批进度在哪里查看？**
docs/用户设计说明书.md:219:A：登录后在"我的申请"列表中查看，点击详情可查看审批历史。
docs/用户设计说明书.md:221:### 6.2 审批人常见问题
docs/用户设计说明书.md:223:**Q1：如何查看待审批申请？**
docs/用户设计说明书.md:224:A：登录后在"待审批"列表中查看，点击进入审批页面。
docs/用户设计说明书.md:226:**Q2：审批意见是否必填？**
docs/用户设计说明书.md:229:**Q3：审批后能否撤销？**
docs/用户设计说明书.md:230:A：审批后不能撤销，如需修改请联系系统管理员。
docs/用户设计说明书.md:232:**Q4：如何导出审批数据？**
docs/用户设计说明书.md:233:A：学工部用户在"审批统计"页面点击"导出Excel"按钮。
docs/用户设计说明书.md:240:**Q2：如何修改审批时限？**
docs/用户设计说明书.md:241:A：在系统配置页面修改"审批时限"参数（单位：小时）。
docs/用户设计说明书.md:246:**Q4：如何对接宿舍管理系统？**
docs/用户设计说明书.md:284:本系统需要从宿舍管理系统获取以下数据，才能正常运行：
docs/用户设计说明书.md:287:2. **辅导员基本信息** - 创建辅导员账号，让辅导员能够审批申请
docs/用户设计说明书.md:288:3. **班级-辅导员对应关系** - 系统自动分配审批人，学生提交申请时自动找到对应的辅导员
docs/用户设计说明书.md:289:4. **宿舍清退数据** - 验证学生是否完成宿舍清退，未完成不能提交申请
docs/用户设计说明书.md:316:适用于：宿舍清退数据
docs/用户设计说明书.md:319:- 学生提交申请时，需要实时查询宿舍是否已清退
docs/用户设计说明书.md:320:- 如果未清退，系统会提示学生先完成宿舍清退手续
docs/用户设计说明书.md:323:- 允许学生上传宿舍清退证明截图
docs/用户设计说明书.md:370:**4. 宿舍清退数据（实时查询）**
docs/用户设计说明书.md:397:- 登录后可以提交离校申请
docs/用户设计说明书.md:398:- 系统自动分配对应的辅导员审批
docs/用户设计说明书.md:403:- 可以进行审批操作
docs/PROJECT-SUMMARY.md:1:# 毕业生离校申请审批系统 - 项目总结
docs/PROJECT-SUMMARY.md:5:**项目名称：** 毕业生离校申请审批系统  
docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
docs/PROJECT-SUMMARY.md:17:- **平台：** iOS/Android + 微信小程序
docs/PROJECT-SUMMARY.md:21:- **认证：** 混合认证（学号+密码 + 微信OAuth2）+ 5项安全增强
docs/PROJECT-SUMMARY.md:35:- ✓ 确认系统集成需求（宿舍管理系统）
docs/PROJECT-SUMMARY.md:42:- ✓ 完成审批流程设计（状态机、3个审批节点）
docs/PROJECT-SUMMARY.md:66:- ✓ 审查第3、5、7、8、9、10章（API、审批、部署、安全、性能、测试）
docs/PROJECT-SUMMARY.md:70:- ✓ 批次2：第3章API设计（微信绑定、版本检查、上传安全）
docs/PROJECT-SUMMARY.md:71:- ✓ 批次3：第5章审批流程（工作日计算、字段更新、历史审计）
docs/PROJECT-SUMMARY.md:81:- ✓ 简化微信绑定安全措施（5项→2项核心+3项可选）
docs/PROJECT-SUMMARY.md:86:- ✓ 宿舍对接添加class_name和bed_number字段
docs/PROJECT-SUMMARY.md:92:- ✓ 修正CSV模板文件扩展名（.xlsx → .csv）
docs/PROJECT-SUMMARY.md:98:- ✓ P2修复：删除Postman引用、明确认证方式、统一审批时限、修改辅导员权限范围、统一性能指标
docs/PROJECT-SUMMARY.md:104:- ✓ 更新CSV模板（学生、辅导员、班级映射）
docs/PROJECT-SUMMARY.md:113:  - 包含3个文档+4个CSV模板
docs/PROJECT-SUMMARY.md:142:**微信小程序文档整理：**
docs/PROJECT-SUMMARY.md:143:- ✓ 整理微信小程序申请说明（docs/微信小程序申请说明.md）
docs/PROJECT-SUMMARY.md:147:- ✓ 整理微信小程序备案说明（docs/微信小程序备案说明.md）
docs/PROJECT-SUMMARY.md:177:- ✓ 达成最终共识：Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配（文档40）
docs/PROJECT-SUMMARY.md:179:  - 用户主数据通过CSV导入到本地数据库（非运行时API查询）
docs/PROJECT-SUMMARY.md:181:  - 宿舍清退保持实时API查询（可缓存、可降级）
docs/PROJECT-SUMMARY.md:184:  - Week 1提前做数据契约和接口设计（避免返工）
docs/PROJECT-SUMMARY.md:187:- ✓ Claude提出方案A：更新实施计划 + Week 1数据契约（文档41）
docs/PROJECT-SUMMARY.md:188:- ✓ Codex第一轮批判：瀑布式排期、前端后置、Week 10过载（文档42）
docs/PROJECT-SUMMARY.md:189:- ✓ Claude第一轮回应：质疑v0.1冻结时机、Week 1工作量、前端启动条件（文档43）
docs/PROJECT-SUMMARY.md:192:- ✓ 最终共识：纵向切片/MVP优先方法，Week 0-1拆分执行（文档46）
docs/PROJECT-SUMMARY.md:194:  - Week 0（1-2工作日）：冻结v0.1最小可执行契约
docs/PROJECT-SUMMARY.md:195:  - Week 1（5工作日）：后端纵向切片（保留最小权限校验）
docs/PROJECT-SUMMARY.md:196:  - Week 2：CSV导入v1
docs/PROJECT-SUMMARY.md:198:  - Week 4-6：微信小程序并行开发
docs/PROJECT-SUMMARY.md:199:  - Week 6-7：宿舍真实API或降级
docs/PROJECT-SUMMARY.md:201:  - Week 10：验收演示（不新增功能）
docs/PROJECT-SUMMARY.md:202:  - 单端交付（微信小程序优先）
docs/PROJECT-SUMMARY.md:204:  - 从瀑布式到纵向切片（避免Week 8-10才发现集成问题）
docs/PROJECT-SUMMARY.md:206:  - 从双端到单端（微信小程序优先）
docs/PROJECT-SUMMARY.md:207:  - 从Week 1数据契约到Week 0（1-2工作日timebox）
docs/PROJECT-SUMMARY.md:208:  - 保留最小权限校验（纵向切片验证完整链路）
docs/PROJECT-SUMMARY.md:233:   - 内容：宿舍管理系统对接规范，包含API接口和数据文件两种方式
docs/PROJECT-SUMMARY.md:234:   - 受众：宿舍管理系统管理员、数据对接负责人
docs/PROJECT-SUMMARY.md:235:   - 附件：`docs/templates/宿舍清退数据模板.csv`
docs/PROJECT-SUMMARY.md:242:- 微信OAuth2授权登录
docs/PROJECT-SUMMARY.md:245:### 2. 离校申请
docs/PROJECT-SUMMARY.md:247:- 上传附件（宿舍清退证明、图书馆清书证明、财务结清截图）
docs/PROJECT-SUMMARY.md:251:### 3. 审批流程
docs/PROJECT-SUMMARY.md:252:- 两级审批（辅导员→学工部）
docs/PROJECT-SUMMARY.md:253:- 审批意见记录
docs/PROJECT-SUMMARY.md:264:- 微信模板消息推送
docs/PROJECT-SUMMARY.md:265:- 审批状态变更通知
docs/PROJECT-SUMMARY.md:270:- 宿舍管理系统对接
docs/PROJECT-SUMMARY.md:279:2. **applications** - 离校申请表
docs/PROJECT-SUMMARY.md:280:3. **approvals** - 审批记录表
docs/PROJECT-SUMMARY.md:305:- 微信OAuth2认证
docs/PROJECT-SUMMARY.md:308:### 阶段3：离校申请模块（第3周）
docs/PROJECT-SUMMARY.md:314:### 阶段4：审批管理模块（第4周）
docs/PROJECT-SUMMARY.md:315:- 审批记录模型
docs/PROJECT-SUMMARY.md:316:- 审批API
docs/PROJECT-SUMMARY.md:317:- 审批流程逻辑
docs/PROJECT-SUMMARY.md:327:- 微信通知
docs/PROJECT-SUMMARY.md:333:- 宿舍系统对接
docs/PROJECT-SUMMARY.md:339:- 微信小程序
docs/PROJECT-SUMMARY.md:357:   - 申请微信公众平台账号
docs/PROJECT-SUMMARY.md:367:2. **微信公众平台审核延迟** - 提前申请账号
docs/contracts/contract-v0.1.md:1:# 数据契约 v0.1 - 最小可执行契约
docs/contracts/contract-v0.1.md:5:**适用范围：** Week 1纵向切片  
docs/contracts/contract-v0.1.md:32:    """离校申请数据传输对象"""
docs/contracts/contract-v0.1.md:38:    leave_date: str                  # 计划离校日期 (YYYY-MM-DD)
docs/contracts/contract-v0.1.md:50:    """审批记录数据传输对象"""
docs/contracts/contract-v0.1.md:66:    """宿舍清退状态数据传输对象"""
docs/contracts/contract-v0.1.md:92:    PENDING_COUNSELOR = "pending_counselor"  # 待辅导员审批
docs/contracts/contract-v0.1.md:93:    PENDING_DEAN = "pending_dean"        # 待学工部审批
docs/contracts/contract-v0.1.md:138:| DORM_BLOCKED | 422 | 宿舍清退未完成 | 提交申请时宿舍未清退 |
docs/contracts/contract-v0.1.md:144:| PROVIDER_UNAVAILABLE | 503 | 外部服务不可用 | 宿舍清退API超时 |
docs/contracts/contract-v0.1.md:153:    "message": "宿舍清退未完成，无法提交申请",
docs/contracts/contract-v0.1.md:199:  "reason": "毕业离校",
docs/contracts/contract-v0.1.md:211:  "reason": "毕业离校",
docs/contracts/contract-v0.1.md:229:  "reason": "毕业离校",
docs/contracts/contract-v0.1.md:249:### 4.3 审批
docs/contracts/contract-v0.1.md:256:  "comment": "同意离校"
docs/contracts/contract-v0.1.md:269:  "comment": "同意离校",
docs/contracts/contract-v0.1.md:385:### 6.1 宿舍清退Mock
docs/contracts/contract-v0.1.md:405:                blocking_reason="宿舍物品未清理",
docs/contracts/contract-v0.1.md:454:    "message": "宿舍清退未完成，无法提交申请",
docs/contracts/contract-v0.1.md:458:      "blocking_reason": "宿舍物品未清理"
docs/contracts/contract-v0.1.md:470:**初始版本 - 最小可执行契约**
docs/contracts/contract-v0.1.md:476:- API端点（认证、申请、审批、查询）
docs/contracts/contract-v0.1.md:478:- Mock响应（宿舍清退Mock + 错误Mock）
docs/contracts/contract-v0.1.md:483:- 微信OAuth相关API
docs/contracts/contract-v0.1.md:485:- 审批转办、撤回、驳回重提
docs/contracts/contract-v0.1.md:488:- 前端可用mock跑通登录→提交→审批→查询流程
docs/contracts/contract-v0.1.md:538:        json={'reason': '毕业离校', 'leave_date': '2024-06-30'}
docs/contracts/contract-v0.1.md:542:    # 3. 辅导员审批
docs/contracts/contract-v0.1.md:543:    # 4. 学工部审批
docs/微信小程序备案说明.md:1:# 微信小程序备案说明
docs/微信小程序备案说明.md:27:   - 可随时接听电话，用于备案期间接收微信平台的核实电话
docs/微信小程序备案说明.md:52:   - 可随时接听电话，用于备案期间接收微信平台的核实电话
docs/微信小程序备案说明.md:75:   - 可随时接听电话，用于备案期间接收微信平台的核实电话
docs/微信小程序备案说明.md:91:在填写完备案信息提交后，大约1~2个工作日，**主体负责人的常用手机号**将收到微信平台的核实电话。
docs/微信小程序备案说明.md:101:### 3.1 登录微信小程序后台
docs/微信小程序备案说明.md:103:1. 申请小程序之后，访问微信公众平台
docs/微信小程序备案说明.md:105:3. 进入微信公众平台登录页
docs/微信小程序备案说明.md:106:4. 用微信小程序管理员的微信扫码登录小程序
docs/微信小程序备案说明.md:132:- [微信小程序申请说明](./微信小程序申请说明.md)
docs/微信小程序备案说明.md:133:- [微信公众平台官方文档](https://developers.weixin.qq.com/miniprogram/introduction/)
docs/superpowers/plans/2026-05-27-implementation-plan.md:1:# 毕业生离校申请审批系统 - 实施计划
docs/superpowers/plans/2026-05-27-implementation-plan.md:12:实现一个完整的毕业生离校申请审批系统，支持：
docs/superpowers/plans/2026-05-27-implementation-plan.md:13:- 学生在线提交离校申请
docs/superpowers/plans/2026-05-27-implementation-plan.md:14:- 辅导员和学工部两级审批
docs/superpowers/plans/2026-05-27-implementation-plan.md:16:- 微信通知推送
docs/superpowers/plans/2026-05-27-implementation-plan.md:17:- 宿舍管理系统对接（API集成）
docs/superpowers/plans/2026-05-27-implementation-plan.md:24:- 前端开发（React Native + 微信小程序）
docs/superpowers/plans/2026-05-27-implementation-plan.md:27:- 审批流程引擎
docs/superpowers/plans/2026-05-27-implementation-plan.md:52:- 微信小程序开发经验
docs/superpowers/plans/2026-05-27-implementation-plan.md:57:- 微信公众平台账号
docs/superpowers/plans/2026-05-27-implementation-plan.md:58:- 宿舍管理系统API文档和测试环境
docs/superpowers/plans/2026-05-27-implementation-plan.md:64:- ✓ 审批流程完整可用
docs/superpowers/plans/2026-05-27-implementation-plan.md:106:│   │   ├── applications/       # 离校申请模块
docs/superpowers/plans/2026-05-27-implementation-plan.md:113:│   │   ├── approvals/          # 审批管理模块
docs/superpowers/plans/2026-05-27-implementation-plan.md:153:│   └── miniprogram/            # 微信小程序
docs/superpowers/plans/2026-05-27-implementation-plan.md:237:3. **实现微信OAuth2认证**
docs/superpowers/plans/2026-05-27-implementation-plan.md:239:   - 实现微信授权登录API
docs/superpowers/plans/2026-05-27-implementation-plan.md:241:   - 编写微信认证测试
docs/superpowers/plans/2026-05-27-implementation-plan.md:257:- ✓ 微信授权登录成功
docs/superpowers/plans/2026-05-27-implementation-plan.md:264:### 阶段3：离校申请模块（第3周）
docs/superpowers/plans/2026-05-27-implementation-plan.md:266:**目标：** 实现离校申请的创建、查询、更新、提交功能
docs/superpowers/plans/2026-05-27-implementation-plan.md:310:### 阶段4：审批管理模块（第4周）
docs/superpowers/plans/2026-05-27-implementation-plan.md:312:**目标：** 实现审批流程和审批记录管理
docs/superpowers/plans/2026-05-27-implementation-plan.md:316:1. **创建审批记录模型**
docs/superpowers/plans/2026-05-27-implementation-plan.md:322:2. **实现审批API**
docs/superpowers/plans/2026-05-27-implementation-plan.md:323:   - 获取待审批列表API
docs/superpowers/plans/2026-05-27-implementation-plan.md:324:   - 审批通过API
docs/superpowers/plans/2026-05-27-implementation-plan.md:325:   - 审批驳回API
docs/superpowers/plans/2026-05-27-implementation-plan.md:326:   - 获取审批历史API
docs/superpowers/plans/2026-05-27-implementation-plan.md:328:3. **实现审批流程逻辑**
docs/superpowers/plans/2026-05-27-implementation-plan.md:329:   - 辅导员审批逻辑
docs/superpowers/plans/2026-05-27-implementation-plan.md:330:   - 学工部审批逻辑
docs/superpowers/plans/2026-05-27-implementation-plan.md:331:   - 审批记录创建
docs/superpowers/plans/2026-05-27-implementation-plan.md:336:   - 检查超时审批
docs/superpowers/plans/2026-05-27-implementation-plan.md:340:5. **实现审批权限控制**
docs/superpowers/plans/2026-05-27-implementation-plan.md:341:   - 辅导员只能审批本年级
docs/superpowers/plans/2026-05-27-implementation-plan.md:342:   - 学工部可以审批所有
docs/superpowers/plans/2026-05-27-implementation-plan.md:346:- ✓ 辅导员审批通过后状态变更为pending_admin
docs/superpowers/plans/2026-05-27-implementation-plan.md:347:- ✓ 学工部审批通过后状态变更为approved
docs/superpowers/plans/2026-05-27-implementation-plan.md:380:   - 权限验证（只能下载自己的或审批人的）
docs/superpowers/plans/2026-05-27-implementation-plan.md:399:**目标：** 实现微信通知推送和通知管理
docs/superpowers/plans/2026-05-27-implementation-plan.md:409:2. **实现微信通知**
docs/superpowers/plans/2026-05-27-implementation-plan.md:410:   - 配置微信公众平台
docs/superpowers/plans/2026-05-27-implementation-plan.md:413:   - 编写微信通知测试
docs/superpowers/plans/2026-05-27-implementation-plan.md:427:5. **集成通知到审批流程**
docs/superpowers/plans/2026-05-27-implementation-plan.md:429:   - 审批通过时通知学生和下一审批人
docs/superpowers/plans/2026-05-27-implementation-plan.md:430:   - 审批驳回时通知学生
docs/superpowers/plans/2026-05-27-implementation-plan.md:431:   - 超时时通知审批人
docs/superpowers/plans/2026-05-27-implementation-plan.md:434:- ✓ 微信通知发送成功
docs/superpowers/plans/2026-05-27-implementation-plan.md:437:- ✓ 审批流程触发通知
docs/superpowers/plans/2026-05-27-implementation-plan.md:444:**目标：** 实现宿舍管理系统对接和重试机制
docs/superpowers/plans/2026-05-27-implementation-plan.md:454:2. **实现宿舍系统对接**
docs/superpowers/plans/2026-05-27-implementation-plan.md:472:5. **集成到审批流程**
docs/superpowers/plans/2026-05-27-implementation-plan.md:473:   - 提交申请时验证宿舍清退
docs/superpowers/plans/2026-05-27-implementation-plan.md:478:- ✓ 宿舍系统API调用成功
docs/superpowers/plans/2026-05-27-implementation-plan.md:481:- ✓ 集成到审批流程
docs/superpowers/plans/2026-05-27-implementation-plan.md:488:**目标：** 实现React Native应用和微信小程序
docs/superpowers/plans/2026-05-27-implementation-plan.md:502:   - 微信授权页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:512:4. **实现审批页面**
docs/superpowers/plans/2026-05-27-implementation-plan.md:513:   - 待审批列表页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:514:   - 审批详情页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:515:   - 审批操作页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:528:#### 8.2 微信小程序
docs/superpowers/plans/2026-05-27-implementation-plan.md:538:   - 微信授权登录
docs/superpowers/plans/2026-05-27-implementation-plan.md:547:4. **实现审批页面**
docs/superpowers/plans/2026-05-27-implementation-plan.md:548:   - 待审批列表页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:549:   - 审批操作页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:558:- ✓ 微信小程序运行正常
docs/superpowers/plans/2026-05-27-implementation-plan.md:576:   - 编写完整审批流程测试
docs/superpowers/plans/2026-05-27-implementation-plan.md:616:**风险2：微信公众平台审核延迟**
docs/superpowers/plans/2026-05-27-implementation-plan.md:617:- 缓解：提前申请微信公众平台账号
docs/数据确认清单.md:1:# 毕业生离校系统 - 数据确认清单
docs/数据确认清单.md:5:**目标用户：** 宿舍管理系统管理员、数据对接负责人
docs/数据确认清单.md:31:**问题6：** 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
docs/数据确认清单.md:33:**背景说明：** 系统需要明确哪些学生具备离校申请资格，通过 `is_graduating` 字段标识。
docs/数据确认清单.md:54:- A. 数据库直连（需要安全审批和网络配置）
docs/数据确认清单.md:56:- C. CSV/Excel文件导入（最快，首版推荐）
docs/数据确认清单.md:62:**问题11：** CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/数据确认清单.md:72:**背景说明：** 例如宿舍清退API查询失败时，是否允许学生上传截图证明？
docs/数据确认清单.md:74:**问题13：** 是否有统一身份认证或微信绑定前置要求？
docs/数据确认清单.md:76:**背景说明：** 系统支持密码登录和微信登录，CSV导入的账号需要首次登录设置密码。
docs/数据确认清单.md:96:首版采用**CSV/Excel导入 + 宿舍清退API**组合方案：
docs/数据确认清单.md:100:| 学生基本信息 | CSV/Excel导入 | 变更频率低（学期级），快速上线 |
docs/数据确认清单.md:101:| 辅导员基本信息 | CSV/Excel导入 | 约50人，变更频率低 |
docs/数据确认清单.md:102:| 班级-辅导员映射 | CSV/Excel导入 | 变更频率低，需强校验 |
docs/数据确认清单.md:103:| 宿舍清退数据 | API实时查询 | 需要实时校验清退状态 |
docs/数据确认清单.md:129:**阶段2：CSV导入实现（2周）**
docs/数据确认清单.md:131:**目标：** 实现CSV批量导入功能
docs/数据确认清单.md:134:1. 设计三份CSV模板（学生、辅导员、班级映射）
docs/数据确认清单.md:135:2. 实现CSV导入功能（文件上传、解析、校验）
docs/数据确认清单.md:142:- CSV导入功能模块
docs/数据确认清单.md:143:- 三份CSV模板文件
docs/数据确认清单.md:149:**阶段3：宿舍清退API对接（1周）**
docs/数据确认清单.md:151:**目标：** 实现宿舍清退状态实时查询
docs/数据确认清单.md:154:1. 对接宿管系统宿舍清退API
docs/数据确认清单.md:161:- 宿舍清退API对接模块
docs/数据确认清单.md:212:| 阶段2 | 第2-3周 | CSV导入功能上线 | 成功导入测试数据，校验报告无异常 |
docs/数据确认清单.md:213:| 阶段3 | 第4周 | 宿舍清退API对接完成 | API调用成功率>95%，降级流程测试通过 |
docs/数据确认清单.md:227:| 宿舍清退API不稳定 | 中 | 实现降级流程，允许上传截图证明 |
docs/plans/week-0-1-execution-plan.md:13:冻结v0.1最小可执行契约，为Week 1纵向切片提供稳定基础。
docs/plans/week-0-1-execution-plan.md:30:- [ ] 创建Mock响应（宿舍清退Mock + 错误Mock）
docs/plans/week-0-1-execution-plan.md:40:- [ ] 前端可用mock跑通登录→提交→审批→查询流程
docs/plans/week-0-1-execution-plan.md:44:- 如Day 1结束未完成前端review → 冻结当前版本，Week 1开始后异步review
docs/plans/week-0-1-execution-plan.md:48:## Week 1：后端纵向切片（5工作日）
docs/plans/week-0-1-execution-plan.md:51:交付可运行的后端最小闭环：薄认证 + 申请提交 + 两级审批 + 状态查询 + Dorm Mock。
docs/plans/week-0-1-execution-plan.md:81:  - Dorm Mock集成：检查宿舍清退状态
docs/plans/week-0-1-execution-plan.md:83:  - 创建辅导员审批记录
docs/plans/week-0-1-execution-plan.md:84:- [ ] 辅导员审批API（POST /api/approvals/{id}/approve|reject）
docs/plans/week-0-1-execution-plan.md:85:  - 最小角色校验：只有对应班级辅导员可审批
docs/plans/week-0-1-execution-plan.md:87:  - 创建学工部审批记录（通过时）
docs/plans/week-0-1-execution-plan.md:88:- [ ] 学工部审批API（POST /api/approvals/{id}/approve|reject）
docs/plans/week-0-1-execution-plan.md:89:  - 最小角色校验：只有学工部可审批
docs/plans/week-0-1-execution-plan.md:102:- [ ] 辅导员可审批（通过/驳回）
docs/plans/week-0-1-execution-plan.md:103:- [ ] 学工部可审批（通过/驳回）
docs/plans/week-0-1-execution-plan.md:104:- [ ] 状态查询返回完整申请信息和审批记录
docs/plans/week-0-1-execution-plan.md:105:- [ ] 角色校验生效（学生不能审批，辅导员不能跨班级审批）
docs/plans/week-0-1-execution-plan.md:109:- 如Day 4结束学工部审批未完成 → 推到Week 2 Day 1，Week 1只验证辅导员审批
docs/plans/week-0-1-execution-plan.md:115:  - 测试1：学生登录 → 提交申请 → 辅导员审批通过 → 学工部审批通过 → 查询状态
docs/plans/week-0-1-execution-plan.md:116:  - 测试2：学生登录 → 提交申请 → 辅导员审批驳回 → 查询状态
docs/plans/week-0-1-execution-plan.md:117:  - 测试3：宿舍清退未完成 → 提交申请失败（DORM_BLOCKED）
docs/plans/week-0-1-execution-plan.md:118:  - 测试4：角色校验（学生不能审批，辅导员不能跨班级审批）
docs/plans/week-0-1-execution-plan.md:141:### 前端准备（Week 1期间）
docs/plans/week-0-1-execution-plan.md:144:- [ ] 技术栈选型确认（微信小程序框架）
docs/plans/week-0-1-execution-plan.md:151:**时间：** Week 1 Day 1-5（与后端并行）
docs/plans/week-0-1-execution-plan.md:154:- 微信小程序项目可运行
docs/plans/week-0-1-execution-plan.md:159:- [ ] 可用mock跑通登录→提交→审批→查询流程
docs/plans/week-0-1-execution-plan.md:169:**缓解措施：** 1-2工作日timebox，超时冻结当前假设进入Week 1
docs/plans/week-0-1-execution-plan.md:171:### 风险2：Week 1 Day 3申请提交API未完成
docs/plans/week-0-1-execution-plan.md:177:### 风险3：Week 1 Day 4学工部审批未完成
docs/plans/week-0-1-execution-plan.md:181:**降级方案：** 推到Week 2 Day 1，Week 1只验证辅导员审批
docs/plans/week-0-1-execution-plan.md:183:### 风险4：Week 1 Day 5测试未通过
docs/plans/week-0-1-execution-plan.md:199:### Week 1验收
docs/plans/week-0-1-execution-plan.md:203:- [ ] 4个API端点可用（登录、提交、审批、查询）
docs/plans/week-0-1-execution-plan.md:212:**目标：** CSV导入v1
docs/数据对接说明文档.md:1:# 毕业生离校申请审批系统 - 数据对接说明文档
docs/数据对接说明文档.md:5:**目标用户：** 宿舍管理系统管理员、数据对接负责人
docs/数据对接说明文档.md:13:本系统需要与学校现有的**宿舍管理系统**进行数据对接，获取以下数据：
docs/数据对接说明文档.md:16:2. **辅导员基本信息** - 创建辅导员账号，用于审批管理
docs/数据对接说明文档.md:17:3. **班级-辅导员对应关系** - 自动分配审批人
docs/数据对接说明文档.md:18:4. **宿舍清退数据** - 验证学生是否完成宿舍清退
docs/数据对接说明文档.md:26:| 学生基本信息 | **CSV/Excel文件导入** | 首版推荐，快速上线 |
docs/数据对接说明文档.md:27:| 辅导员基本信息 | **CSV/Excel文件导入** | 首版推荐，快速上线 |
docs/数据对接说明文档.md:28:| 班级-辅导员对应关系 | **CSV/Excel文件导入** | 首版推荐，需强校验 |
docs/数据对接说明文档.md:29:| 宿舍清退数据 | **API接口实时查询** | 需要实时验证清退状态 |
docs/数据对接说明文档.md:31:**为什么推荐CSV/Excel导入？**
docs/数据对接说明文档.md:41:| 数据确认 | 第1周 | 确认数据可用性、字段定义、CSV模板 |
docs/数据对接说明文档.md:42:| CSV导入开发 | 第2-3周 | 开发CSV导入功能、校验逻辑、审计日志 |
docs/数据对接说明文档.md:43:| 宿舍清退API对接 | 第4周 | 对接宿舍清退API、测试异常场景 |
docs/数据对接说明文档.md:48:## 二、学生基本信息（CSV导入）
docs/数据对接说明文档.md:55:- 自动分配审批人（根据班级匹配辅导员）
docs/数据对接说明文档.md:81:- `is_graduating=true` 表示具备本批次离校申请资格
docs/数据对接说明文档.md:84:### 2.3 CSV模板
docs/数据对接说明文档.md:101:- 不要使用Excel的"另存为CSV"，建议使用专业工具导出UTF-8编码
docs/数据对接说明文档.md:105:**步骤1：准备CSV文件**
docs/数据对接说明文档.md:110:**步骤2：上传CSV文件**
docs/数据对接说明文档.md:114:- 上传CSV文件
docs/数据对接说明文档.md:125:- 如有错误，修改CSV后重新上传
docs/数据对接说明文档.md:151:## 三、辅导员基本信息（CSV导入）
docs/数据对接说明文档.md:156:- 审批权限管理
docs/数据对接说明文档.md:172:- `is_active=false` 时不能登录、不能审批，但历史记录可查询
docs/数据对接说明文档.md:174:### 3.3 CSV模板
docs/数据对接说明文档.md:191:## 四、班级-辅导员对应关系（CSV导入）
docs/数据对接说明文档.md:195:学生提交申请时，系统根据学生的 `class_id` 自动查询对应的辅导员，分配审批人。
docs/数据对接说明文档.md:210:### 4.3 CSV模板
docs/数据对接说明文档.md:243:- 无审批人的学生数：有多少学生没有对应的辅导员
docs/数据对接说明文档.md:247:## 五、宿舍清退数据（API接口）
docs/数据对接说明文档.md:251:学生提交离校申请时，系统实时查询宿舍清退状态：
docs/数据对接说明文档.md:253:- 未完成清退：提示学生先完成宿舍清退手续
docs/数据对接说明文档.md:254:- 查询失败：允许学生上传宿舍清退证明截图
docs/数据对接说明文档.md:258:**接口名称：** 查询学生宿舍清退状态
docs/数据对接说明文档.md:262:**请求地址：** `http://宿舍管理系统域名/api/dorm/checkout/status`
docs/数据对接说明文档.md:354:- 允许学生上传宿舍清退证明截图
docs/数据对接说明文档.md:361:### 6.1 CSV文件要求
docs/数据对接说明文档.md:365:- 格式：CSV或Excel（.xlsx）
docs/数据对接说明文档.md:401:### 7.1 CSV导入相关
docs/数据对接说明文档.md:403:**Q1：CSV文件中文乱码怎么办？**
docs/数据对接说明文档.md:405:A：确保文件编码为UTF-8。如果使用Excel编辑，保存时选择"CSV UTF-8（逗号分隔）"格式。
docs/数据对接说明文档.md:409:A：检查CSV文件中是否有重复的学号。系统要求学号必须唯一。
docs/数据对接说明文档.md:427:A：系统会自动重试3次。如果仍然失败，允许学生上传宿舍清退证明截图。
docs/数据对接说明文档.md:441:A：可以通过系统管理后台手动修改，或者重新导入包含该学生的CSV文件。
docs/数据对接说明文档.md:445:A：更新班级-辅导员对应关系，重新导入CSV文件。已提交的申请不受影响，新提交的申请使用新辅导员。
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:19:#### 2. 5项微信绑定安全措施过度设计
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:40:5. 微信OAuth2流程过于复杂（3种场景）
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:75:- 5项微信绑定安全措施
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:110:- 微信绑定：5项措施（过度）
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:132:2. ✓ 简化微信绑定安全措施（5项 → 2项）
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:152:- 核心模块优先（认证、申请、审批）
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:208:+ 1. 密码验证：微信绑定已有账户需要密码
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:239:**第5章 审批流程：**
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:264:| 安全设计 | 6/10 | 部分过度（微信绑定），部分不足（病毒扫描） |
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:282:1. **立即修改3个CRITICAL问题**（applications_history、微信绑定、SQLAlchemy）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:15:本毕业离校系统的数据对接范围限定为：
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:17:- **数据获取方式：** 通过宿管系统提供的数据库、API或CSV文件
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:22:1. **项目定位：** 本系统是宿管系统的配套子系统，不是全校级统一离校平台
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:67:**Codex意见：** 学生、辅导员、班级映射的"DB优先"改为"CSV/Excel优先，API/DB增强"。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:73:1. **实施周期：** CSV/Excel导入最快，DB直连需要安全审批和网络配置
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:75:3. **风险控制：** CSV导入可以先验证、再导入、可回滚；DB直连风险更高
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:76:4. **首版策略：** 先用CSV快速上线，后续根据数据变更频率决定是否升级为API/DB
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:82:| 学生基本信息 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先** / API或DB视图增强 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:83:| 辅导员基本信息 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先** / 人事或统一身份API增强 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:84:| 班级-辅导员对应关系 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:85:| 宿舍清退数据 | API优先 / DB备选 / CSV降级 | **保持不变**（API优先合理） |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:88:- 宿舍清退数据保持API优先，因为需要实时校验学生提交时的清退状态
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:89:- 账号数据采用CSV首版，上线后根据实际变更频率决定是否升级
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:123:**Codex意见：** 缺少终审管理员分配规则、账号标识映射、历史审批人一致性规则、多辅导员场景处理。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:174:- 学生CSV：`student_id` → `users.student_id`
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:175:- 辅导员CSV：`employee_id` → `users.employee_id`
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:176:- 班级映射CSV：`counselor_employee_id` → 查询 `users` 表中 `employee_id` 匹配的记录
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:180:#### 4.3 历史审批人一致性规则
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:187:这是一个重要的业务规则。如果班级映射变更后自动改写已提交申请的审批人，会导致：
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:188:1. 审批流程混乱（原审批人已审批，新审批人不知情）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:189:2. 审计追溯困难（无法还原当时的审批人是谁）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:190:3. 权限边界模糊（新审批人可能不应该看到旧申请）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:193:1. 已提交的申请保持原审批人不变
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:200:1. **审批流程完整性：** 已提交申请的审批人是提交时确定的，不应因后续映射变更而改变
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:201:2. **审计追溯：** 保持历史审批人记录，便于追溯当时的审批责任
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:202:3. **权限边界：** 新辅导员不应自动获得旧申请的审批权限
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:209:| 映射变更后，已提交申请 | `counselor_id` **不变**，保持原审批人 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:211:| 需要改派审批人 | 管理员显式操作，记录审计日志（操作人、时间、原因） |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:215:- 审计日志表记录审批人变更操作
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:228:2. 审批流程需要确定主审批人
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:229:3. 权限边界需要明确（所有辅导员都能审批？还是只有主辅导员？）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:238:3. CSV导入时强校验：同一 `class_id` 不能出现多次
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:254:4. 所有辅导员都能查看本班申请，但只有主辅导员能审批
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:278:3. `phone` 是否可选需要结合微信绑定策略确认
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:298:3. CSV需补充导入覆盖策略、重复数据处理、失败回滚
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:329:**CSV技术要求：**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:383:6. 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:390:9. 优先推荐的对接方式是什么？（DB直连 / API / CSV导入）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:392:11. CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:396:13. 是否有统一身份认证或微信绑定前置要求？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:411:2. 先落地CSV模板
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:413:4. 再对接宿舍清退API
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:427:**阶段2：CSV导入实现（2周）**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:428:1. 设计三份CSV模板：学生、辅导员、班级-辅导员映射
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:429:2. 实现CSV导入功能和校验逻辑
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:433:**阶段3：宿舍清退API对接（1周）**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:434:1. 对接宿管系统宿舍清退API
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:455:1. 对接方式从"DB优先"改为"CSV/Excel首版优先，API/DB增强"
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:459:5. 明确历史审批人一致性规则（不自动改写）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:461:7. 补充DB/API/CSV的技术要求细节
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:464:10. 调整实施路径（CSV优先，分阶段实施）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:479:- 调整对接方式优先级：学生/辅导员/班级映射改为"CSV/Excel首版优先"
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:483:- 补充说明：`is_graduating=true` 表示具备本批次离校申请资格
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:485:**修改3：宿舍清退数据（第三章）**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:500:- 补充DB/API/CSV的具体技术要求
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:511:- 调整推荐方案：CSV首版优先
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:517:- 新增"历史审批人一致性规则"章节
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:546:4. **实施路径：** 我们接受了CSV首版优先的建议，并补充了5阶段实施路径。Codex是否认同这个路径？是否有需要调整的地方？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:557:- **接受建议：** CSV首版优先、字段定义统一、补充实施细节
docs/design/2026-05-27-system-design.md:1:# 毕业生离校申请审批系统 - 系统设计文档
docs/design/2026-05-27-system-design.md:3:**项目名称：** 毕业生离校申请审批系统  
docs/design/2026-05-27-system-design.md:16:5. [审批流程设计](#5-审批流程设计)
docs/design/2026-05-27-system-design.md:30:   - 登录离校管理系统（挂在微信公众号）
docs/design/2026-05-27-system-design.md:31:   - 填写离校申请表，明确计划离校日期
docs/design/2026-05-27-system-design.md:32:   - 上传规定附件（宿舍清退证明、图书馆清书证明、财务结清截图）
docs/design/2026-05-27-system-design.md:35:2. **一级审批：** 毕业年级辅导员审核
docs/design/2026-05-27-system-design.md:36:   - 核实学生各项离校手续
docs/design/2026-05-27-system-design.md:42:   - 生成电子离校凭证
docs/design/2026-05-27-system-design.md:47:- **平台：** iOS/Android + 微信小程序
docs/design/2026-05-27-system-design.md:51:- **认证：** 混合认证（学号+密码 + 微信OAuth2）
docs/design/2026-05-27-system-design.md:64:│ React Native │ React Native │  微信小程序    │
docs/design/2026-05-27-system-design.md:102:│ 宿舍管理系统  │  微信公众平台 │ 文件存储   │
docs/design/2026-05-27-system-design.md:124:- wechatpy（微信SDK）
docs/design/2026-05-27-system-design.md:146:│   ├── applications/      # 离校申请模块
docs/design/2026-05-27-system-design.md:149:│   │   ├── workflows.py   # 审批流程
docs/design/2026-05-27-system-design.md:152:│   ├── approvals/         # 审批管理模块
docs/design/2026-05-27-system-design.md:153:│   │   ├── models.py      # 审批记录
docs/design/2026-05-27-system-design.md:154:│   │   ├── views.py       # 审批操作API
docs/design/2026-05-27-system-design.md:165:│   │   └── wechat.py      # 微信推送
docs/design/2026-05-27-system-design.md:168:│       ├── dorm_system.py # 宿舍系统对接
docs/design/2026-05-27-system-design.md:189:   - 微信OAuth2授权登录
docs/design/2026-05-27-system-design.md:193:2. **applications（离校申请）**
docs/design/2026-05-27-system-design.md:198:   - 离校日期管理
docs/design/2026-05-27-system-design.md:200:3. **approvals（审批管理）**
docs/design/2026-05-27-system-design.md:201:   - 辅导员审批操作
docs/design/2026-05-27-system-design.md:203:   - 审批意见记录
docs/design/2026-05-27-system-design.md:205:   - 审批时限监控
docs/design/2026-05-27-system-design.md:208:   - 附件上传（宿舍清退证明、图书馆清书证明、财务结清截图）
docs/design/2026-05-27-system-design.md:216:   - 微信模板消息推送
docs/design/2026-05-27-system-design.md:217:   - 审批状态变更通知
docs/design/2026-05-27-system-design.md:219:   - 审批完成通知
docs/design/2026-05-27-system-design.md:224:   - 宿舍管理系统API对接
docs/design/2026-05-27-system-design.md:225:   - 宿舍清退状态查询
docs/design/2026-05-27-system-design.md:247:2. applications - 离校申请表
docs/design/2026-05-27-system-design.md:248:3. approvals - 审批记录表
docs/design/2026-05-27-system-design.md:265:    wechat_openid VARCHAR(100) UNIQUE COMMENT '微信OpenID',
docs/design/2026-05-27-system-design.md:273:    wechat_bind_time TIMESTAMP COMMENT '微信绑定时间',
docs/design/2026-05-27-system-design.md:301:- `wechat_openid`: 微信授权登录后绑定
docs/design/2026-05-27-system-design.md:304:### 2.3 离校申请表（applications）
docs/design/2026-05-27-system-design.md:312:    -- 固定审批人追踪
docs/design/2026-05-27-system-design.md:316:    planned_leave_date DATE NOT NULL COMMENT '计划离校日期',
docs/design/2026-05-27-system-design.md:318:    current_approver_id BIGINT COMMENT '当前审批人ID',
docs/design/2026-05-27-system-design.md:325:    certificate_url VARCHAR(500) COMMENT '离校凭证URL',
docs/design/2026-05-27-system-design.md:349:) COMMENT='离校申请表';
docs/design/2026-05-27-system-design.md:356:- `approved` - 审批通过
docs/design/2026-05-27-system-design.md:362:### 2.4 审批记录表（approvals）
docs/design/2026-05-27-system-design.md:368:    approver_id BIGINT NOT NULL COMMENT '审批人ID',
docs/design/2026-05-27-system-design.md:369:    approver_role VARCHAR(20) NOT NULL COMMENT '审批人角色',
docs/design/2026-05-27-system-design.md:371:    opinion TEXT COMMENT '审批意见',
docs/design/2026-05-27-system-design.md:372:    approval_time TIMESTAMP NOT NULL COMMENT '审批时间',
docs/design/2026-05-27-system-design.md:383:) COMMENT='审批记录表';
docs/design/2026-05-27-system-design.md:416:- `dorm_clearance` - 宿舍清退证明
docs/design/2026-05-27-system-design.md:455:- `approval_pending` - 待审批
docs/design/2026-05-27-system-design.md:458:- `approval_timeout` - 审批超时提醒
docs/design/2026-05-27-system-design.md:486:- `wechat` - 微信配置
docs/design/2026-05-27-system-design.md:494:- `wechat.appid` - 微信AppID
docs/design/2026-05-27-system-design.md:495:- `wechat.secret` - 微信Secret（加密存储）
docs/design/2026-05-27-system-design.md:496:- `dorm_integration_type` - 宿舍系统集成类型（api/database）
docs/design/2026-05-27-system-design.md:497:- `dorm_api_url` - 宿舍系统API地址
docs/design/2026-05-27-system-design.md:498:- `dorm_api_key` - 宿舍系统API密钥（加密存储）
docs/design/2026-05-27-system-design.md:499:- `dorm_db_config` - 宿舍系统数据库配置（加密存储，JSON格式）
docs/design/2026-05-27-system-design.md:544:- `approve` - 审批通过
docs/design/2026-05-27-system-design.md:545:- `reject` - 审批驳回
docs/design/2026-05-27-system-design.md:553:- `approval` - 审批
docs/design/2026-05-27-system-design.md:593:  ├─1:N─→ approvals (审批人审批多个申请)
docs/design/2026-05-27-system-design.md:600:  ├─N:1─→ users (当前审批人)
docs/design/2026-05-27-system-design.md:601:  ├─1:N─→ approvals (一个申请多条审批记录)
docs/design/2026-05-27-system-design.md:607:approvals (审批记录表)
docs/design/2026-05-27-system-design.md:608:  ├─N:1─→ applications (多条审批记录属于一个申请)
docs/design/2026-05-27-system-design.md:609:  └─N:1─→ users (审批人)
docs/design/2026-05-27-system-design.md:627:2. 一个申请必须经过2级审批（辅导员→学工部）
docs/design/2026-05-27-system-design.md:628:3. 每个审批节点记录一条审批记录
docs/design/2026-05-27-system-design.md:705:**2. 微信授权登录**
docs/design/2026-05-27-system-design.md:754:**3. 微信绑定到已有账户**
docs/design/2026-05-27-system-design.md:857:  "remarks": "毕业离校"
docs/design/2026-05-27-system-design.md:923:        "file_name": "宿舍清退证明.jpg",
docs/design/2026-05-27-system-design.md:947:  "remarks": "延后离校"
docs/design/2026-05-27-system-design.md:973:### 3.4 审批相关API
docs/design/2026-05-27-system-design.md:975:**1. 获取待审批列表**
docs/design/2026-05-27-system-design.md:999:**2. 审批通过**
docs/design/2026-05-27-system-design.md:1006:  "opinion": "材料齐全，同意离校",
docs/design/2026-05-27-system-design.md:1013:  "message": "审批成功",
docs/design/2026-05-27-system-design.md:1031:**3. 审批驳回**
docs/design/2026-05-27-system-design.md:1038:  "opinion": "宿舍清退证明不完整，请重新提交",
docs/design/2026-05-27-system-design.md:1080:    "file_name": "宿舍清退证明.jpg",
docs/design/2026-05-27-system-design.md:1154:        "content": "您的离校申请已通过辅导员审核",
docs/design/2026-05-27-system-design.md:1189:      "description": "宿舍系统集成类型（api/database）"
docs/design/2026-05-27-system-design.md:1194:      "description": "宿舍系统API地址"
docs/design/2026-05-27-system-design.md:1199:      "description": "宿舍系统API密钥（加密存储）",
docs/design/2026-05-27-system-design.md:1225:- `wechat` - 微信配置
docs/design/2026-05-27-system-design.md:1228:- `integration` - 外部系统集成配置（宿舍系统等）
docs/design/2026-05-27-system-design.md:1242:2. **微信OAuth2认证**
docs/design/2026-05-27-system-design.md:1243:   - 获取微信授权code
docs/design/2026-05-27-system-design.md:1253:微信登录（安全增强）：
docs/design/2026-05-27-system-design.md:1258:   │  ├─ 已绑定其他微信：返回通用错误（防止枚举）
docs/design/2026-05-27-system-design.md:1259:   │  └─ 未绑定微信：要求密码验证 → 事务锁绑定 → 审计日志 → 生成Token
docs/design/2026-05-27-system-design.md:1267:1. **密码验证**：微信绑定已有账户时需要密码验证
docs/design/2026-05-27-system-design.md:1321:├─ 审批申请（通过/驳回）
docs/design/2026-05-27-system-design.md:1322:├─ 查看审批历史
docs/design/2026-05-27-system-design.md:1327:├─ 最终备案审批
docs/design/2026-05-27-system-design.md:1341:辅导员审批         | ✗       | ✓         | ✗
docs/design/2026-05-27-system-design.md:1342:学工部审批         | ✗       | ✗         | ✓
docs/design/2026-05-27-system-design.md:1388:## 5. 审批流程设计
docs/design/2026-05-27-system-design.md:1401:approved（审批通过）
docs/design/2026-05-27-system-design.md:1408:    'pending_counselor': ['pending_admin', 'rejected'],  # 辅导员审批
docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
docs/design/2026-05-27-system-design.md:1420:  - 计划离校日期 ≥ 当前日期 + 3个工作日
docs/design/2026-05-27-system-design.md:1421:  - 必须上传宿舍清退证明
docs/design/2026-05-27-system-design.md:1427:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
docs/design/2026-05-27-system-design.md:1428:  - 设置当前审批人：current_approver_id = counselor_id
docs/design/2026-05-27-system-design.md:1443:    - 更新当前审批人：current_approver_id = admin_id
docs/design/2026-05-27-system-design.md:1445:    - 创建审批记录：approvals（approver_role='counselor', action='approve'）
docs/design/2026-05-27-system-design.md:1446:    - 创建历史快照：applications_history（version=N, change_reason='辅导员审批通过'）
docs/design/2026-05-27-system-design.md:1451:    - 清空当前审批人：current_approver_id = NULL
docs/design/2026-05-27-system-design.md:1453:    - 创建审批记录：approvals（approver_role='counselor', action='reject'）
docs/design/2026-05-27-system-design.md:1457:  - 记录审批意见和时间
docs/design/2026-05-27-system-design.md:1468:    - 清空当前审批人：current_approver_id = NULL
docs/design/2026-05-27-system-design.md:1470:    - 生成电子离校凭证：certificate_url
docs/design/2026-05-27-system-design.md:1472:    - 创建审批记录：approvals（approver_role='admin', action='approve'）
docs/design/2026-05-27-system-design.md:1479:    - 清空当前审批人：current_approver_id = NULL
docs/design/2026-05-27-system-design.md:1481:    - 创建审批记录：approvals（approver_role='admin', action='reject'）
docs/design/2026-05-27-system-design.md:1507:    # 查询待审批的申请
docs/design/2026-05-27-system-design.md:1514:        # 获取最新审批记录（当前节点）
docs/design/2026-05-27-system-design.md:1523:            # 已有审批记录，从上次审批时间开始计算
docs/design/2026-05-27-system-design.md:1530:            # 创建超时审批记录
docs/design/2026-05-27-system-design.md:1583:- 第1次：办理时限到期时通知审批人
docs/design/2026-05-27-system-design.md:1584:- 第2次：超时4小时后通知审批人上级
docs/design/2026-05-27-system-design.md:1588:- 外部系统（宿舍管理系统）不可用时，允许手动上传证明文件
docs/design/2026-05-27-system-design.md:1589:- 审批人可选择"跳过验证"并备注原因
docs/design/2026-05-27-system-design.md:1605:### 6.2 宿舍管理系统对接
docs/design/2026-05-27-system-design.md:1608:验证学生宿舍清退状态，确保离校手续真实完成。
docs/design/2026-05-27-system-design.md:1622:# 查询宿舍清退状态
docs/design/2026-05-27-system-design.md:1692:            raise ExternalSystemTimeout("宿舍系统超时")
docs/design/2026-05-27-system-design.md:1694:            raise ExternalSystemError(f"宿舍系统错误: {str(e)}")
docs/design/2026-05-27-system-design.md:1734:- 审批人可选择"跳过验证"并备注原因
docs/design/2026-05-27-system-design.md:1915:- 微信Secret：AES-256加密存储
docs/design/2026-05-27-system-design.md:1975:**微信绑定安全措施：**
docs/design/2026-05-27-system-design.md:1983:    """微信绑定已有账户"""
docs/design/2026-05-27-system-design.md:1995:        raise ValidationError("该学号已绑定其他微信")
docs/design/2026-05-27-system-design.md:2038:    # 绑定微信
docs/design/2026-05-27-system-design.md:2062:# 不暴露具体原因：学号不存在、已绑定其他微信、密码错误等
docs/design/2026-05-27-system-design.md:2231:- 用户认证：登录、登出、密码修改、微信绑定
docs/design/2026-05-27-system-design.md:2233:- 审批操作：通过、驳回
docs/design/2026-05-27-system-design.md:2319:- `wechat_secret` - 微信Secret
docs/design/2026-05-27-system-design.md:2320:- `dorm_api_key` - 宿舍系统API密钥
docs/design/2026-05-27-system-design.md:2321:- `dorm_db_config` - 宿舍系统数据库配置（JSON格式）
docs/design/2026-05-27-system-design.md:2386:- `idx_approver_status`: 待审批列表查询（按审批人+状态+时间）
docs/design/2026-05-27-system-design.md:2389:- `idx_app_time`: 申请的审批历史（按时间倒序）
docs/design/2026-05-27-system-design.md:2441:# L3: 待审批数量缓存（1分钟）
docs/design/2026-05-27-system-design.md:2458:    # 失效审批人的待审批数量缓存
docs/design/2026-05-27-system-design.md:2481:- 审批操作（必须实时）
docs/design/2026-05-27-system-design.md:2511:    # 发送微信通知
docs/design/2026-05-27-system-design.md:2514:# 异步生成离校凭证
docs/design/2026-05-27-system-design.md:2603:    """测试微信绑定需要密码验证"""
docs/design/2026-05-27-system-design.md:2615:    """测试微信绑定事务锁（防止竞态）"""
docs/design/2026-05-27-system-design.md:2629:    """测试微信绑定记录审计日志"""
docs/design/2026-05-27-system-design.md:2641:    # 已绑定其他微信
docs/design/2026-05-27-system-design.md:2649:    """测试学生无法审批"""
docs/design/2026-05-27-system-design.md:2677:    """测试审批操作记录审计日志"""
docs/design/2026-05-27-system-design.md:2695:- 完整审批流程测试
docs/design/2026-05-27-system-design.md:2708:- 微信开发者工具（小程序测试）
docs/design/2026-05-27-system-design.md:2712:2. 辅导员审批流程
docs/design/2026-05-27-system-design.md:2772:6. 配置微信公众号
docs/design/2026-05-27-system-design.md:2779:- 业务指标：申请数量、审批时效
docs/design/2026-05-27-system-design.md:2787:- 审批超时 > 10个
docs/design/2026-05-27-system-design.md:2794:3. 微信通知依赖外部服务（需配置降级策略）
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:132:3. **关键模块强制TDD**：认证、审批、支付等
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:136:P0: 核心业务逻辑（认证、审批、状态机）
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:203:Locust测试场景只有3个任务（查看列表、查看详情、审批），权重固定（3:2:1）。
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:227:        """辅导员查看待审批"""
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:232:        """辅导员审批"""
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:24:- 绑定微信到现有账户需要密码验证
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:30:**微信新用户的密码强度验证和学生身份验证**
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:33:1. 攻击者用微信注册，使用受害者的student_id
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:57:**关键补充：** 微信新用户必须**阻止登录**直到密码设置完成且学生身份验证通过。
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:68:- "该学号已绑定其他微信账号" → student_id存在
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:69:- "该学号已注册，请输入密码" → student_id存在但无微信
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:85:#### 风险B: 微信绑定的竞态条件（MEDIUM严重性）
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:125:- 允许微信优先注册 - 减少摩擦
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:164:改进的认证设计**从根本上是健全的**，修复了关键的账户接管漏洞。双路径方法（密码优先或微信优先）是良好的UX妥协。
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:168:1. **CRITICAL**: 为微信发起的账户添加学生身份验证
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:180:    "新微信用户的学生身份验证",       # ❌ 缺失 - CRITICAL
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:32:**问题6：** 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:34:**背景说明：** 系统需要明确哪些学生具备离校申请资格，通过 `is_graduating` 字段标识。
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:55:- A. 数据库直连（需要安全审批和网络配置）
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:57:- C. CSV/Excel文件导入（最快，首版推荐）
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:63:**问题11：** CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:73:**背景说明：** 例如宿舍清退API查询失败时，是否允许学生上传截图证明？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:75:**问题13：** 是否有统一身份认证或微信绑定前置要求？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:77:**背景说明：** 系统支持密码登录和微信登录，CSV导入的账号需要首次登录设置密码。
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:97:首版采用**CSV/Excel导入 + 宿舍清退API**组合方案：
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:101:| 学生基本信息 | CSV/Excel导入 | 变更频率低（学期级），快速上线 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:102:| 辅导员基本信息 | CSV/Excel导入 | 约50人，变更频率低 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:103:| 班级-辅导员映射 | CSV/Excel导入 | 变更频率低，需强校验 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:104:| 宿舍清退数据 | API实时查询 | 需要实时校验清退状态 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:130:**阶段2：CSV导入实现（2周）**
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:132:**目标：** 实现CSV批量导入功能
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:135:1. 设计三份CSV模板：
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:139:2. 实现CSV导入功能：
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:156:- CSV导入功能模块
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:157:- 三份CSV模板文件
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:163:**阶段3：宿舍清退API对接（1周）**
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:165:**目标：** 实现宿舍清退状态实时查询
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:168:1. 对接宿管系统宿舍清退API
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:182:   - 学生上传宿舍清退证明截图
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:186:- 宿舍清退API对接模块
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:201:   - 设置允许的离校日期范围
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:210:   - 无审批人的学生：0个
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:217:   - 辅导员登录和审批
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:219:   - 宿舍清退状态查询
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:220:   - 申请提交和审批流程
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:242:   - 如果变更频率低（每学期1-2次），保持CSV导入
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:248:   - 辅导员审批效率
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:252:   - 审批流程优化
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:268:| 阶段2 | 第2-3周 | CSV导入功能上线 | 成功导入测试数据，校验报告无异常 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:269:| 阶段3 | 第4周 | 宿舍清退API对接完成 | API调用成功率>95%，降级流程测试通过 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:283:| 宿舍清退API不稳定 | 中 | 实现降级流程，允许上传截图证明 |
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:30:- 申请/审批/附件/通知/集成模块
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:52:- 学生在线提交离校申请
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:53:- 辅导员一级审批
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:56:- 微信通知
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:57:- 宿舍管理系统对接
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:65:- 认证：学号密码 + 微信 OAuth2
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:90:- 审批流程设计
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:103:3. 安全设计有明确增强项：微信绑定事务锁、通用错误、审计日志、上传 MIME 校验、API 限流等。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:104:4. 审批流程具备状态机意识：草稿、待辅导员、待学工部、通过、驳回等状态明确。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:119:   例如字段声明 `NOT NULL`，外键又写 `ON DELETE SET NULL`。这在数据库层面互相冲突。审批记录、审计日志这类历史数据建议优先使用软删除或 `PROTECT/RESTRICT`，避免历史记录失真。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:131:   Access Token 设计为 7 天。对审批和个人信息系统而言，这个时长偏长。虽然尚未实现，但它属于已完成认证设计的一部分，建议在设计文档阶段调整。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:143:3. 离校申请模块
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:144:4. 审批管理模块
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:187:**Round 2：API、审批、部署、安全、性能、测试**
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:190:- 补充微信绑定、版本检查、上传安全
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:191:- 补充审批工作日计算、字段更新、历史审计
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:330:- 审批状态机实现
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:332:- 微信通知实现
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:333:- 宿舍系统对接实现
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:16:`integrations`模块职责定义为"外部系统集成"，但实际只对接宿舍管理系统。未来如需对接图书馆系统、财务系统，是否都放在同一模块？模块划分缺乏扩展性考虑。
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:27:├── dorm/            # 宿舍系统集成
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:38:- 微信通知：HTTP请求通常<500ms，是否值得引入Celery复杂度？
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:122:1. **并发场景罕见**：同一申请同时被两个审批人操作的概率极低
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:210:- **不需要软删除**：审批记录、通知（历史数据，不删除）
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:10:`29-data-source-analysis.md` 的方向是正确的：当前数据对接文档只覆盖宿舍清退，无法完整支撑 student、counselor、admin 三类角色的账号初始化、权限边界和自动审批分配。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:14:1. **班级-辅导员对应关系应明确列为 P0。** 这是自动分配审批人的核心数据。没有它，系统提交申请时无法稳定设置 `counselor_id` 和 `current_approver_id`，只能退化为人工逐个配置或人工改派。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:15:2. **首版不应追求所有数据源 API 化。** 对约 1000 名学生、约 50 名辅导员、约 5 名管理员的规模，CSV/Excel 批量导入加严格校验更现实；API 更适合作为后续自动化增强。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:25:| 学生基本信息 | 教务系统 | P0 | 用于创建学生账号、身份识别、展示院系专业班级、限定毕业离校申请人范围。用户设计说明书已出现“学号、姓名、专业、班级”和“批量导入学生用户”的要求，因此必须写入数据对接文档。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:26:| 辅导员基本信息 | 人事系统或人工台账 | P0 | 用于创建 counselor 账号和审批权限主体。实时同步不是 P0，但账号数据本身是 P0。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:28:| 宿舍清退数据 | 宿管系统 | P0 | 当前业务把宿舍清退作为提交前校验项，现有对接文档已覆盖。即使保留人工证明降级，正式流程仍应具备自动校验或批量数据导入能力。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:29:| 毕业资格/离校资格字段 | 教务系统 | P0 字段，非 P0 独立接口 | 如果系统只导入当届毕业生，可通过导入范围满足；如果导入全量学生，则必须在学生基本信息中带 `graduation_year`、`graduation_status` 或 `eligible_for_leave`。不建议首版单独建设学籍 API。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:46:| 学生基本信息 | CSV/Excel 批量导入 | 教务系统 API | 首版按毕业届别导入更容易落地。字段建议包括 `student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:47:| 辅导员基本信息 | CSV/Excel 批量导入 | 人事系统 API 或手动创建 | 约 50 人规模下，批量导入足够。字段建议包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:48:| 班级-辅导员对应关系 | CSV/Excel 批量导入并强校验 | 教务系统 API | 必须优先支持。建议用 `class_id + counselor_employee_id + effective_term` 表达关系，不要只靠 `class_name`。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无审批人的学生数。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:49:| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入、人工证明降级 | 当前文档策略合理。提交申请时实时性较强，API 价值高；若宿管系统暂不支持 API，则每日文件导入加人工证明降级。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:50:| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:51:| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 后续对接时只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，不要引入借阅明细。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:52:| 财务结清状态 | 首版手动上传截图 | API 优先于 CSV | 后续对接时只返回是否结清和结清日期，不同步欠费明细；外部系统失败时保留人工审核通道。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:63:原因不是“方便展示”，而是学生账号、身份识别、申请资格、班级映射都依赖它。当前数据对接文档的目标用户也应从“宿舍管理系统管理员”扩展为“教务系统、人事系统、宿管系统及业务数据负责人”。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:67:首版推荐 CSV/Excel 批量导入，不推荐一开始就要求人事系统 API。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:77:- 学生提交时能否自动设置辅导员审批人；
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:78:- 辅导员是否只能查看和审批负责班级；
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:80:- 审批统计能否按院系、班级、辅导员追踪。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:82:建议数据对接文档单独增加“审批关系数据”章节，并把导入覆盖率 100% 作为上线验收条件之一。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:94:学籍状态不建议作为首版独立接口，但毕业资格字段必须进入学生基础数据。换句话说，“是否允许提交离校申请”必须有数据依据，只是不一定需要实时 API。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:108:5. **审批人变更后的历史一致性。** 已提交申请中的 `counselor_id` 应保持历史一致，不应因后续班级映射变更自动改写。若需改派，应由管理员显式操作并记录审计日志。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:110:6. **多辅导员和代理审批。** 现实中可能有主辅导员、代管辅导员、临时代理。首版可只要求一个主审批人，但后台应预留人工改派能力。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:114:8. **离校批次配置。** 开放申请时间、允许离校日期范围、毕业届别可能来自业务配置，而不一定来自教务系统。应作为系统配置纳入实施计划。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:116:9. **通知联系方式。** `phone`、`email` 对提醒和异常联系有价值；微信 `openid` 应通过用户绑定产生，不应从外部系统导入。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:126:1. **重构数据对接说明文档目录。** 从单一“宿舍对接”扩展为“账号基础数据、审批关系数据、业务校验数据、降级与审计”四类。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:128:2. **定义学生基本信息导入模板。** 先支持 CSV/Excel 导入当届毕业生，包含毕业资格字段和班级唯一标识。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:134:5. **保留并完善宿舍清退对接。** 当前文档已较完整，下一步应把它纳入统一的校验结果、缓存、失败降级和审计机制。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:150:1. 新增“学生基本信息导入”章节，提供 CSV/Excel 模板字段。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:153:4. 将“宿舍清退数据”保留为业务校验数据，并补充与人工证明降级的关系。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:162:- **P0 数据：** 学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据、毕业资格字段。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:164:- **首版策略：** 账号和映射数据用 CSV/Excel 批量导入，宿舍清退优先 API，管理员手动维护，图书馆/财务继续截图上传。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:165:- **最高优先级行动：** 立即补充班级-辅导员映射的数据规范和导入校验，这是自动审批闭环的关键缺口。
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:60:| CRITICAL | 5项微信绑定安全措施过度 | 实施复杂、依赖外部服务 |
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:112:### 2. 微信绑定5项安全措施
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:155:10. ⚠ 简化微信绑定安全措施（需讨论）
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:195:### 争议2：微信绑定安全措施保留几项？
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:237:  - 微信绑定保留几项安全措施？
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:23:- 对接外部系统的多种数据库（宿舍管理系统等）
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:53:### 1.5 审批超时监控
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:74:**新增：** 微信新用户必须验证学生身份
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:92:**新增：** 微信绑定操作使用数据库锁
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:178:- certificate_url VARCHAR(500)（离校凭证URL）
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:212:            raise ValidationError("您已有进行中的申请，请等待审批完成")
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:5:**审查范围：** API设计、审批流程、部署架构、安全设计、性能优化、测试策略
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:49:- 添加微信绑定API（/auth/wechat/bind、/auth/password/setup）
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:51:- 添加审批API版本检查
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:55:### 批次3：审批流程
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:71:- 添加微信绑定安全
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:11:当前仓库已经完成较完整的需求、系统设计、实施计划和多轮评审共识，核心方向基本清晰：Django + DRF 单体后端、PostgreSQL 单数据库、Redis + Celery、本地文件存储、微信登录/通知、宿舍系统优先 API 对接。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:62:- 审批流程
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:193:- 审批记录和审计日志优先保留历史，用户删除应使用软删除或 `PROTECT`
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:240:### 6.7 审批超时动作与枚举不一致
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:242:approvals 表字段说明写 `action: approve/reject`，但超时任务会创建 `action='timeout'`。需要把 `timeout` 加入枚举，或把超时记录拆成独立 `approval_timeouts`/notification 事件，避免审批记录语义混乱。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:246:审批记录字段说明写“1个工作日(24小时)”，第 5 章又写“1个工作日 = 8小时工作时间”。建议统一为：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:278:审批 API 已有 `version` 字段和 409 响应，但更新申请、重新提交、附件变更、生成凭证等也可能改变申请状态或可审批性。建议明确所有会影响审批判断的写操作都必须纳入版本控制。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:293:建议新增 `counselor_assignments` 或在用户/班级模型中维护负责关系，并在查询和审批时同时校验 `current_approver_id`。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:295:### 7.5 微信 openid 不应作为客户端绑定凭据
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:297:微信登录未绑定时，API 示例把 `wechat_openid` 返回给客户端。更稳妥的做法是：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:309:设计中 Access Token 有效期为 7 天，Refresh Token 30 天。对审批、附件、个人信息系统来说，7 天 access token 偏长。建议：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:318:audit_logs 设计有 `request_data` 字段。需要明确脱敏策略，否则登录密码、验证码、JWT、微信 code、API 密钥、外部数据库连接串都可能进入审计日志。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:377:### 9.3 宿舍系统字段契约不足
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:384:- 人工跳过验证的审批责任归属
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:385:- 外部系统不可用时是否允许提交还是只允许审批时跳过
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:452:单实例 Gunicorn 4 workers 下，`500 并发用户` 与 `>500 QPS` 可能对只读列表接口可达，但对审批写入、附件上传、外部系统调用不现实。建议性能指标按接口分类：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:457:- 审批操作：P95/QPS
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:463:设计中缓存申请详情、申请状态、学生申请列表。对含个人信息和审批信息的数据，必须保证：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:476:- 审批人待办列表
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:509:当前前端仅有空目录。设计计划同时做 React Native 和微信小程序，但需求里明确“挂在微信公众号”，小程序很可能是首要交付端。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:513:1. 先确认首发端：微信小程序优先，React Native 后续。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:515:3. 附件上传、微信授权、Token 刷新、审批待办这四个流程应先做端到端原型。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:543:3. 审批状态机：明确 rejected 重新提交、version 递增、附件替换规则。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:545:5. 宿舍系统集成契约：状态码、超时、降级、人工跳过责任。
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:59:            raise ValidationError("该用户有待审批申请，无法删除")
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:39:- 允许学号+密码 AND 微信OpenID同时认证同一用户
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:41:- 微信登录可以绑定到现有账户，无需密码验证（lines 1003-1006）
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:45:2. 攻击者用微信OAuth绑定到该学号（无密码验证）
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:50:# 微信绑定时必须验证现有凭证
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:53:        # 用户必须先用密码登录，然后在设置中绑定微信
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:54:        raise PermissionDenied("请先使用学号密码登录，然后在设置中绑定微信")
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:56:        raise ValidationError("该学号已绑定其他微信账号")
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:80:- DoS审批队列（垃圾申请提交）
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:128:### 5. 审批超时监控不完整
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:169:- 无批量操作（辅导员审批50个申请需点击50次）
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:173:- 无微信降级方案
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:175:- 无审批重新分配
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:185:3. **"电子离校凭证"** - PDF证书 vs 数据库状态标志？
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:191:- 为什么校园离校系统需要支持4种数据库？
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:194:- 为什么需要React Native？微信小程序不够？
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:5:**审查范围：** 用户设计说明书、数据对接说明文档、CSV模板
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:13:发现 9 个主要问题，涉及文档一致性、安全设计、对接契约。CSV 格式本身无误。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:26:文档引用 `docs/templates/宿舍清退数据模板.xlsx`，但实际只有 `docs/templates/宿舍清退数据模板.csv`。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:41:引用 `docs/templates/宿舍管理系统API.postman_collection.json`，但 `docs/templates/` 目录中不存在此文件。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:97:不要在宿舍清退接口中使用 `id_card`，用 `student_id + name` 足够。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:101:### 问题6：审批时限口径不一致 [P2]
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:108:用户文档与系统设计文档审批时限口径不一致。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:143:辅导员查看/审批权限按"本年级"划分过粗，实际应按学院、专业、班级或辅导员负责范围授权。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:175:## CSV 模板检查
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:177:**文件：** `docs/templates/宿舍清退数据模板.csv`
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:187:- 明确 CSV 文件名规则
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:188:- 如果实际模板是 CSV，确保文档引用一致（已修复）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:11:1. ✅ 学生宿舍清退数据（来源：宿管系统）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:12:   - 用途：验证学生是否完成宿舍清退
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:13:   - 对接方式：API接口 或 CSV文件导入
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:27:| 学生 | student | ~1000人/届 | 提交离校申请 | 教务系统 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:28:| 辅导员 | counselor | ~50人 | 一级审批 | 人事系统 + 教务系统 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:42:- 自动分配审批人（根据班级）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:56:- CSV文件导入（备选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:62:### 3.2 宿舍清退数据
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:67:- 验证学生是否完成宿舍清退
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:68:- 作为离校申请的前置条件
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:73:- 宿舍信息（dorm_building, dorm_room, bed_number）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:78:- CSV文件导入（备选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:90:- 分配审批权限
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:102:- CSV文件导入（备选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:113:- 自动分配审批人
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:124:- CSV文件导入（备选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:129:- 如果没有这个数据，系统无法自动分配审批人
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:151:- CSV文件导入（备选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:169:- 作为离校申请的前置条件
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:179:- CSV文件导入（备选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:195:- 作为离校申请的前置条件
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:205:- CSV文件导入（备选）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:221:- 限制只有毕业生可以提交离校申请
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:222:- 自动设置计划离校日期范围
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:248:- 宿舍清退通过外部系统API验证
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:260:| 学生基本信息 | 教务系统 | API/CSV | ❌ 缺失 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:261:| 宿舍清退数据 | 宿管系统 | API/CSV | ✅ 已有 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:262:| 辅导员基本信息 | 人事系统 | API/CSV | ❌ 缺失 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:263:| 班级-辅导员对应关系 | 教务系统 | API/CSV | ❌ 缺失 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:270:| 图书馆清书状态 | 图书馆系统 | API/CSV | 手动上传截图 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:271:| 财务结清状态 | 财务系统 | API/CSV | 手动上传截图 |
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:282:- 🔴 **影响：** 系统无法自动分配审批人
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:305:   - 当前文档只说明了宿舍清退数据
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:309:   - API接口 vs CSV文件导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:6:**目的：** 明确毕业离校系统所需的数据源，提交给宿管系统方反馈
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:14:1. **CSV导入策略**：从"全量覆盖"改为"staging表 + upsert + 软停用"
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:21:3. **认证约束调整**：增加`password_setup_required`支持CSV预导入账号
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:22:4. **对接方式调整**：学生/辅导员/班级映射改为"CSV/Excel首版优先"
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:37:| 学生基本信息 | P0 | 创建学生账号、身份识别、班级映射 | **CSV/Excel首版优先** / API或DB增强 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:38:| 宿舍清退数据 | P0 | 验证学生是否完成宿舍清退 | API优先 / DB备选 / CSV降级 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:39:| 辅导员基本信息 | P0 | 创建辅导员账号、审批权限 | **CSV/Excel首版优先** / 人事或统一身份API增强 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:40:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:44:- **CSV/Excel首版优先**：首版采用CSV/Excel批量导入，快速上线，后续根据数据变更频率决定是否升级为API/DB
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:46:- **DB备选**：直接读取宿管系统数据库（需要安全审批和网络配置）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:47:- **CSV降级**：当无法提供API或DB时，通过CSV文件导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:50:1. **实施周期**：CSV/Excel导入最快，DB直连需要安全审批和网络配置
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:52:3. **风险控制**：CSV导入可以先验证、再导入、可回滚；DB直连风险更高
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:64:- 自动分配审批人（根据班级匹配辅导员）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:90:- `is_graduating`：标识是否为当届毕业生，`true`表示具备本批次离校申请资格
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:93:**CSV模板示例：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:107:### 2.2 宿舍清退数据
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:110:- 验证学生是否完成宿舍清退（提交申请前置条件）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:143:- 系统允许学生提交申请，但需上传宿舍清退证明截图
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:151:- 审批权限管理
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:167:- `is_active`：标识是否在职，`false`时不能登录、不能审批，但历史记录可查询
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:169:**CSV模板示例：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:183:| 账号状态 | 登录 | 创建申请 | 审批 | 查看历史 | 接收通知 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:193:- 学生提交申请时自动分配辅导员审批人
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:217:**CSV模板示例：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:228:- 导入后输出校验报告：未匹配班级、未匹配辅导员、重复映射、无审批人的学生数
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:267:### 3.1 CSV/Excel导入（首版推荐）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:278:- 格式：CSV或Excel（.xlsx）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:286:1. CSV导入到临时staging表（按类型拆分）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:331:-- 2. 导入CSV到staging表
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:406:- 宿舍清退数据（实时校验）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:491:    planned_leave_date_start DATE,              -- 允许的最早离校日期
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:492:    planned_leave_date_end DATE,                -- 允许的最晚离校日期
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:522:6. 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:531:9. 优先推荐的对接方式是什么？（DB直连 / API / CSV导入）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:533:11. CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:538:13. 是否有统一身份认证或微信绑定前置要求？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:551:首版采用**CSV/Excel导入 + 宿舍清退API**组合方案：
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:552:- 学生、辅导员、班级映射：CSV/Excel批量导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:553:- 宿舍清退数据：API实时查询
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:564:**阶段2：CSV导入实现（2周）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:565:1. 设计三份CSV模板：学生、辅导员、班级-辅导员映射
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:566:2. 实现CSV导入功能和校验逻辑
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:573:**阶段3：宿舍清退API对接（1周）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:574:1. 对接宿管系统宿舍清退API
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:722:1. ✅ CSV导入策略从"全量覆盖"改为"staging + upsert + 软停用"
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:725:4. ✅ 认证约束调整：支持CSV预导入账号（password_setup_required）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:726:5. ✅ 对接方式调整：学生/辅导员/班级映射改为CSV首版优先
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:24:当宿舍系统不一定提供班级信息时，文件导入字段表已把 `class_name` 标为"否"（非必填），但 API 响应字段表只给 `bed_number` 标注了"可选"，会让接口实现方把 `class_name` 误认为必返字段。
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:27:接口实现方可能将class_name作为必填字段处理，导致宿舍系统无法提供班级信息时接口调用失败。
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:31:- 方案B：在所有文档中统一改为必填（需确认宿舍系统一定能提供）
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:40:在"李四"这一行，表头只有 10 列，但当前内容在 `否` 后面放了两个空单元格，导致该行变成 11 列，`未开始` 和备注列会错位；这也与下面的 CSV 示例不一致。
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:71:- **class_name字段：** 便于按班级统计离校情况，辅导员管理，添加合理
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:72:- **bed_number字段：** 精确定位学生宿舍床位，便于宿舍管理，添加合理
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:84:- ✓ CSV模板文件
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:111:- users表已有class_name字段，API响应中的class_name来自宿舍系统
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:118:  - 如果需要在离校凭证上显示：需要存储到applications表
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:119:  - 如果需要统计各宿舍楼离校情况：需要存储
docs/discussions/codex-review-2026-05-27/04-database-review.md:67:**查询1：** "显示辅导员X的待审批申请"
docs/discussions/codex-review-2026-05-27/04-database-review.md:128:- "追踪这个审批工作流中的所有操作" → 无correlation_id
docs/discussions/codex-review-2026-05-27/04-database-review.md:165:- 无`admin_id`（谁做的最终审批？）
docs/discussions/codex-review-2026-05-27/04-database-review.md:167:- 无`certificate_url`（line 42提到"电子离校凭证"）
docs/discussions/codex-review-2026-05-27/04-database-review.md:171:2. 并发bug：两个审批人同时批准 → 无乐观锁
docs/discussions/codex-review-2026-05-27/04-database-review.md:179:    -- 新增固定审批人追踪
docs/discussions/codex-review-2026-05-27/04-database-review.md:184:    certificate_url VARCHAR(500) COMMENT '离校凭证URL',
docs/discussions/codex-review-2026-05-27/04-database-review.md:219:    wechat_bind_time TIMESTAMP COMMENT '微信绑定时间',
docs/discussions/codex-review-2026-05-27/04-database-review.md:237:- 但无约束防止：学生创建多个草稿、同时提交多个申请、待审批时重复提交
docs/discussions/codex-review-2026-05-27/04-database-review.md:259:                raise ValidationError("您已有进行中的申请，请等待审批完成")
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:23:1. ✅ **MAJOR - 微信登录API缺少安全流程**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:27:   - 将更新：微信登录API响应格式
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:40:4. ✅ **MAJOR - 审批API缺少版本检查**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:44:   - 将添加：当前审批人验证
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:57:- 添加4个新API端点（微信绑定、密码设置、身份验证、受限Token刷新）
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:60:- 添加审批API版本检查
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:66:## 第5章：审批流程设计 - 响应
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:81:3. ✅ **MAJOR - 工作流未设置审批人字段**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:96:6. ✅ **MINOR - 宿舍证明上传与外部验证协调**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:172:- 添加微信绑定安全子章节
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:257:- 第3章API设计（微信绑定、配置、版本、上传、状态码）
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:260:- 第5章审批流程（工作日、字段更新、历史、审计）
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:218:**Codex意见：** 主设计中 `users` 表有 `chk_auth_method` 约束，要求 `password_hash` 或 `wechat_openid` 非空；CSV预导入账号通常还没有密码或微信绑定，会被约束挡住。
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:231:CSV导入场景：
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:232:1. 学生CSV导入：只有学号、姓名等基本信息，没有密码或微信openid
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:278:2. `wechat_openid IS NOT NULL`：已绑定微信
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:281:**CSV导入时的处理：**
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:384:        raise ValueError(f"CSV校验失败，共 {len(errors)} 个错误")
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:469:3. ✅ 调整认证约束，增加password_setup_required支持CSV导入
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:14:Codex正确指出了方案的核心问题：**偏离了已达成的首版共识**。原方案错误地将用户主数据API化，而共识明确规定学生、辅导员、班级映射应采用CSV导入。
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:26:- 忽略了这些数据是系统基础主数据，影响认证、权限、审批人分配
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:29:1. 用户主数据通过CSV导入到本地数据库
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:49:# CSV实现
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:50:class CSVUserDataImportSource(IUserDataImportSource):
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:52:        # 读取CSV文件
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:76:**宿舍清退保持实时查询：**
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:79:# 宿舍清退Provider用于运行时查询
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:83:        """运行时查询宿舍清退状态"""
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:102:| 宿舍清退API集成 | 1-2周 | API契约明确、字段覆盖、认证跑通 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:209:USER_DATA_SOURCE = 'csv'  # 生产环境使用CSV导入
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:210:DORM_CHECKOUT_SOURCE = 'api'  # 宿舍清退使用API
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:277:| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:278:| Week 2-3 | CSV导入功能、staging表、upsert逻辑、审计日志 | CSV导入模块、导入校验报告 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:279:| Week 3-6 | 申请、审批、附件、通知模块 | 核心业务功能 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:280:| Week 6-7 | 宿舍清退Provider、降级流程、缓存、错误分类 | 宿舍清退集成模块 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:281:| Week 8-9 | 前端开发 | React Native、微信小程序 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:282:| Week 10 | 联调、演示、验收清单 | 可演示版本（Mock数据） |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:285:- 宿舍清退API集成：1周
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:286:- 用户主数据API替换CSV（如需）：另计2-4周
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:299:外部数据源 (CSV/API/Mock)
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:305:本地数据库 (认证、权限、审批的唯一运行时依据)
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:308:DormCheckoutProvider (宿舍清退实时查询)
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:313:1. **用户主数据落库：** 学生、辅导员、班级映射通过CSV导入到本地数据库
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:315:3. **宿舍清退实时查询：** DormCheckoutProvider用于运行时查询，可缓存，可降级
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:316:4. **本地数据库为准：** 认证、权限、审批以本地数据库为唯一依据
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:324:**"Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配"**
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:330:| RealUserDataProvider运行时查询 | CSV导入到本地数据库 | 用户主数据是基础数据，不应依赖外部API |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:333:| Week 7做接口抽象 | Week 1做数据契约和接口 | 避免后续返工 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:338:1. **Week 1：** 数据契约、DTO、ImportSource接口
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:339:2. **Week 2-3：** CSV导入功能（staging + upsert + 审计）
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:341:4. **Week 6-7：** 宿舍清退API对接
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:343:6. **Week 10：** 联调和演示
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:349:- CSV导入功能和校验逻辑
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:350:- 宿舍清退API适配器
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:371:3. 开始Week 1工作：数据契约和接口设计
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:13:- ✓ Round 2审查：API、审批、部署、安全、性能、测试（2 CRITICAL + 21 MAJOR + 6 MINOR）
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:65:- 微信OAuth2流程（3步：获取code → 换取openid → 绑定/登录）
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:70:### 4. 审批流程审查
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:82:- 乐观锁防止并发审批
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:83:- 审批历史追踪（applications_history表）
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:88:- [ ] 宿舍管理系统对接方案是否可行？
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:1:# Round 3 Claude分析 - Part 3: 审批流程与外部集成
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:5:**分析范围：** 第5-6章（审批流程设计、外部系统集成设计）
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:9:## 第5章：审批流程设计
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:54:`check_approval_timeout()`每小时执行一次，扫描所有待审批申请。
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:97:如果两个审批人同时审批同一申请，可能导致状态不一致。
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:109:    # 验证审批人
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:111:        raise PermissionDenied("不是当前审批人")
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:127:- ✓ 审批历史记录完善
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:195:设计提到"审批人可选择'跳过验证'并备注原因"，但未说明如何审计这些操作。
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:35:**理由：** 与文件导入字段表保持一致，宿舍系统可能无法提供班级信息。
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:116:| dorm_building | String | 宿舍楼栋 | 是 | "1号楼" |
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:117:| dorm_room | String | 宿舍房间号 | 是 | "101" |
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:124:- `class_name`：宿舍系统可能无法提供班级信息
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:125:- `bed_number`：部分宿舍系统无床号管理
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:148:- ✓ `docs/templates/宿舍清退数据模板.csv` - CSV模板
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:46:- 微信绑定无密码验证是严重漏洞
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:51:# Codex方案：用户必须先密码登录，然后绑定微信
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:52:raise PermissionDenied("请先使用学号密码登录，然后在设置中绑定微信")
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:54:这个方案对纯微信用户不友好。场景：
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:55:- 学生首次使用，直接用微信登录（最便捷）
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:56:- 系统强制要求先设置密码，再绑定微信
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:64:   - 可选：在设置中绑定微信（需要密码验证）
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:66:2. **微信首次登录（学号不存在）：**
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:71:3. **微信登录（学号已存在）：**
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:72:   - 如果该学号已有wechat_openid → 拒绝（已绑定其他微信）
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:77:# 微信登录API
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:88:        # 已绑定其他微信
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:90:            raise ValidationError("该学号已绑定其他微信账号")
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:92:        # 未绑定微信，需要密码验证
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:97:                'message': '该学号已注册，请输入密码以绑定微信'
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:103:        # 验证通过，绑定微信
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:108:    # 场景3：新用户，微信首次登录
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:129:UNIQUE(wechat_openid)  -- 一个微信只能绑定一个学号
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:203:### 5. 审批超时监控 - **完全同意**
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:249:- 但实际上校园离校系统不需要水平扩展
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:12:**采用纵向切片/MVP优先方法，Week 0-1拆分执行。**
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:16:1. **Week 0（1-2工作日）：** 冻结v0.1最小可执行契约
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:17:2. **Week 1（5工作日）：** 后端纵向切片（保留最小权限校验）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:18:3. **Week 2：** CSV导入v1
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:20:5. **Week 4-6：** 微信小程序并行开发
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:21:6. **Week 6-7：** 宿舍真实API或降级
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:23:8. **Week 10：** 验收演示（不新增功能）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:31:**范围：** 最小可执行契约（不是极简字段，也不是完整模型）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:47:**时间限制：** 1-2工作日完成，超时冻结当前假设进入Week 1
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:49:### 决策2：Week 1交付后端纵向切片
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:57:- 辅导员审批API
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:58:- 学工部审批API
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:64:- 完整CSV导入
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:67:- 微信OAuth
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:69:- 宿舍真实API
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:70:- 复杂审批流
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:77:1. 单端范围确认（只做微信小程序）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:89:- 宿舍真实API
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:90:- 微信OAuth真实接入
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:91:- 完整CSV导入后台
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:93:### 决策4：单端交付（微信小程序优先）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:96:- 微信小程序（覆盖主要用户群）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:97:- 核心流程（申请、审批、状态查询）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:99:- 简化认证（学号+密码，无微信OAuth）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:101:- 简化通知（邮件通知，无微信推送）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:105:- 微信OAuth
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:107:- 微信模板消息
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:115:| **Week 0** (1-2工作日) | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog | 前端可用mock跑通登录→提交→审批→查询流程 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:116:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:117:| **Week 2** | CSV导入v1 | Staging表、校验报告、upsert、软停用基础、导入审计基础 | 可导入10学生+2辅导员，生成校验报告，软停用未导入账号 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:119:| **Week 4-6** | 微信小程序并行开发 | 登录、申请、审批、查询主流程 | 小程序可用mock跑通完整流程，逐步联调真实后端 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:120:| **Week 6-7** | 宿舍真实API或降级方案 | 真实Provider、错误分类、缓存/降级、人工证明路径 | 真实API集成或降级方案可用 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:122:| **Week 10** | 验收演示 | 演示脚本、缺陷修复、文档 | 可演示版本交付，不新增功能 |
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:136:**验收标准：** 前端可用mock跑通登录→提交→审批→查询流程
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:158:### 修正1：从瀑布式到纵向切片
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:160:**原方案A：** 认证→申请→审批→附件→通知→前端→联调
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:162:**修正后：** Week 1端到端最小流程 → Week 2-3扩展 → Week 4前端并行
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:168:**原方案A：** Week 8-9前端，Week 10联调
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:176:**原方案A：** React Native + 微信小程序同时开发
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:178:**修正后：** 微信小程序优先，React Native后续迭代
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:182:### 修正4：从Week 1数据契约到Week 0
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:184:**原方案A：** Week 1做数据契约和接口设计
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:186:**修正后：** Week 0（1-2工作日）冻结v0.1，Week 1用v0.1跑纵向切片
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:188:**原因：** 避免Week 1前半定义契约，后半只剩2-3天开发
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:192:**Claude错误建议：** Week 1"审批API无权限校验"
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:196:**原因：** 纵向切片的价值是验证角色、数据、状态机和审批链路能否串起来
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:204:**缓解措施：** 1-2工作日timebox，超时冻结当前假设进入Week 1
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:206:### 风险2：Week 1纵向切片未完成
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:209:- Day 3结束仍无申请提交API → 只保留"学生提交→辅导员审批→查询"
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:210:- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:219:### 风险4：Week 10过载
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:221:**缓解措施：** Week 10只做验收和演示，前面延期的任务砍掉或推迟到生产集成阶段
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:231:- Codex批判：瀑布式排期、前端后置、Week 10过载
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:232:- Codex建议：纵向切片、前端并行、砍范围
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:235:- Claude质疑：v0.1何时冻结、Week 1工作量、前端启动条件
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:237:- Codex指出Claude方案问题：Week 0膨胀、v0.1过于字段化、Week 1砍权限校验
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:241:- 达成共识：Week 0-1拆分、v0.1最小可执行契约、保留最小权限校验、前端Week 4并行
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:245:1. **纵向切片优于横向模块堆叠** - 早期验证端到端集成
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:248:4. **数据契约提前冻结** - 避免Week 1前半定义后半开发
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:249:5. **最小权限校验不能砍** - 纵向切片的价值在于验证完整链路
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:255:- CSV导入v1的详细设计（Week 2开始前）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:256:- 微信小程序技术栈选择（Week 3开始前）
docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md:257:- 宿舍真实API集成方案（Week 5开始前）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:15:它比旧计划好，但仍然是"先后端模块、后前端、最后联调"的瀑布排期。最大风险不是数据契约，而是到Week 8-10才发现端到端流程、微信小程序、附件、审批权限、宿舍降级和通知串不起来。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:17:**下一步不该只是改计划，而应产出可运行的纵向切片。**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:26:- Week 8-9前端、Week 10联调风险很高
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:28:- 原计划同时要求React Native和微信小程序
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:29:- 2-3人2周做两个端、附件、审批、认证、联调，偏乐观
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:34:### 问题2：Week 10过载
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:37:Week 10不能既做联调、验收、性能、部署、文档，又兜底前面延期。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:48:若演示还包含双端、真实微信、完整附件、通知、导入审计、宿舍降级，那不现实。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:50:### 问题4：CSV导入前置过重
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:53:方案A仍然把CSV导入当成前置大模块。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:56:更好的做法是先做`seed/import minimal path`，让认证和审批用同一套落库数据跑起来，再完善CSV校验、staging、审计。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:70:### 问题1：Week 1做数据契约太晚吗？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:72:**回答：** 不该等到Week 1结束。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:75:现在就应冻结v0.1：字段、枚举、样例CSV、错误码、前端API mock。Week 1用它跑纵向切片。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:82:先做"学生登录/伪登录 → 提交申请 → 辅导员审批 → 学工部审批 → 状态可查"的端到端最小流程。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:84:### 问题3：CSV导入是否应该更早？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:86:**回答：** 不应Week 1完整完成，但Week 1必须完成最小导入路径。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:89:seed/CSV二选一落库到真实users/class mapping表。完整staging、审计、软停用放Week 2。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:96:需要fixture matrix：无班级、重复学号、辅导员停用、多班级、非毕业生、延期、宿舍API 401/404/429/500/timeout。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:105:### 问题6：宿舍清退API集成时机？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:107:**回答：** Mock Provider和契约测试必须Week 1进入提交申请流程。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:117:优先微信小程序或一个Web/RN壳，不要默认双端完整交付。生产就绪不现实，尤其原计划还要求80%覆盖率、P95、1000并发。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:119:### 问题8：Week 1的工作量是否饱和？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:124:Week 1应交付可运行骨架、契约测试、seed数据、最小审批流，而不是只交文档和接口。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:131:契约v0.1 + 纵向切片 → CSV导入硬化 → 核心流程扩展 → 前端并行 → 外部集成 → 验收硬化
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:138:不要"认证完整后再申请、申请完整后再审批"。改成薄认证 + 申请审批核心流优先，通知/附件/完整微信登录后补。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:146:**Week 0-1：契约 + 纵向切片**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:147:- 契约v0.1（字段、枚举、样例CSV、错误码、前端API mock）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:150:- 薄认证（学号+密码，无微信）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:151:- 最小申请审批闭环（提交→辅导员审批→学工部审批→状态查询）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:154:**Week 2：CSV导入v1**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:162:- 申请/审批权限细化
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:168:- 先做微信小程序主流程
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:171:**Week 6-7：宿舍真实API适配**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:181:**Week 10：验收和演示**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:192:演示版到底包含哪些功能？双端都要吗？真实微信还是测试AppID？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:195:明确演示范围：单端（微信小程序优先）+ 核心流程 + Mock数据。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:200:React Native和微信小程序同时开发，资源不足。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:203:优先微信小程序，React Native作为可选项或后续迭代。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:208:宿舍清退API信息何时到位？谁负责跟进？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:216:CSV导入失败后，如何人工修复？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:229:### 6. Week 10没有缓冲
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:232:Week 10既要验收又要兜底延期，无缓冲空间。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:235:Week 10只做验收和演示，前面延期的任务砍掉或推迟到生产集成阶段。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:244:1. 立即冻结数据契约v0.1（现在，不是Week 1）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:245:2. Week 1交付可运行的纵向切片（不是文档）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:248:5. Week 10只做验收（不塞新功能）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:13:#### MAJOR - 微信OAuth2流程过于复杂
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:16:微信登录有3种响应场景：
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:99:1. 简化微信OAuth2流程（3种场景 → 2步流程）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:112:Round 1-3共识引入5项微信绑定安全措施：
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:134:1. **密码验证**：微信绑定已有账户时需要密码验证（已有设计）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:172:2. **学工部权限过大**：admin既能审批又能管理系统配置
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:182:admin_approver   # 学工部审批员（只能审批）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:183:admin_manager    # 学工部管理员（审批+配置管理）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:221:1. **简化微信绑定安全措施**：删除过度设计，保留核心2项
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:231:1. 简化微信绑定安全措施（删除身份验证、受限Token、事务锁）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:235:3. 简化微信OAuth2流程（3种场景 → 2步流程）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:246:**下一部分：** Part 3 - 审批流程与外部集成
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:63:    # 新增：固定审批人追踪
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:94:    certificate_url = models.CharField(max_length=500, null=True, help_text='离校凭证URL')
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:149:    wechat_bind_time = models.DateTimeField(null=True, help_text='微信绑定时间')
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:203:                raise ValidationError("您已有进行中的申请，请等待审批完成")
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:12:Claude的质疑是必要的，尤其是把"Week 0准备"和"Week 1纵向切片"拆开这一点，有助于避免把契约、数据、实现全塞进同一个5天窗口。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:18:3. Week 1建议"审批API无权限校验"，会让纵向切片失去验证审批链路的意义。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:23:**采用Week 0-1拆分，但Week 0必须是1-2个工作日的timebox；v0.1应现在冻结最小可执行契约，不等到Week 1前半；Week 1只承诺后端端到端最小闭环；前端Week 4启动不要求后端完全稳定，只要求契约、mock和核心路径达到可消费状态。**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:27:## 一、数据契约v0.1：现在冻结还是Week 1前半？
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:31:**应现在冻结v0.1，不应拖到Week 1前半。**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:33:这里的"现在"不是指今天把完整未来模型一次性定死，而是指在正式Week 1编码前，用1-2个工作日完成一个可执行的v0.1基线：
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:38:- 样例CSV或seed fixture
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:43:如果拖到Week 1前半才冻结，Week 1后半只剩2-3天，很难完成后端骨架、认证、申请、审批、状态查询和集成测试。Claude把这个拆法描述成"Week 1前半冻结，Week 1后半纵向切片"，本质上还是把Week 1压缩成半周开发，风险比Codex原建议更高。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:49:- 选项A过小：只有`student_id, name, application_id, status, approver_id`无法支撑班级映射、角色判断、审批层级、宿舍清退校验和错误处理。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:50:- 选项B过大：把附件、通知、真实宿舍清退全部字段纳入v0.1，会拖慢Week 1并制造伪稳定。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:52:建议采用**最小可执行契约**：
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:56:| 学生/用户 | student_id、name、role、class_id、is_graduating、graduation_year、active | 微信openid、手机号、完整个人档案 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:59:| 审批 | step、approver_id、decision、comment、decided_at | 会签、转办、复杂委托 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:60:| 宿舍清退 | provider_status、checked_at、blocking_reason、provider_error_code | 真实接口全部响应字段 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:61:| 认证 | login_id、role、access_token mock/JWT格式 | 微信OAuth |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:63:| CSV/seed | 正常样本 + 边界样本 | 完整生产导入模板 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:65:也就是说，v0.1的范围应是**能跑通纵向切片且为v0.2留扩展点**，不是"最小字段"和"完整模型"二选一。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:73:- 用户或业务方只确认业务假设：角色、审批链路、宿舍清退是否阻断提交。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:74:- 样例CSV/fixture先用合成数据，不等待真实样本；真实样本只用于v0.2/v1.0校准。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:79:## 二、Week 1的7-10天工作量是否现实？
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:85:如果团队是2-3人，且Week 0已经完成v0.1契约，Week 1用5个工作日交付最小后端闭环是有机会的。但前提是严格砍范围，并且明确并行路径。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:89:### Week 1应该保留什么
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:91:Week 1必须保留：
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:96:- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:98:- 辅导员审批API
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:99:- 学工部审批API
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:102:- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:104:这里需要反驳Claude的一点：**"审批API简化版，无权限校验"不应该进入Week 1目标。** 纵向切片的价值正是验证角色、数据、状态机和审批链路能否串起来。可以不做完整RBAC、组织树和复杂权限，但最小角色校验不能砍，否则Week 1只能证明CRUD能跑，不能证明毕业离校审批流程能跑。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:106:### Week 1可以推迟什么
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:108:Week 1应推迟：
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:110:- 完整CSV staging、upsert、软停用、导入审计
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:113:- 微信OAuth
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:115:- 宿舍真实API
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:116:- 审批转办、撤回、驳回后重提等复杂流
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:123:- 冻结v0.1最小可执行契约
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:125:- 确认审批链路和状态枚举
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:128:**Week 1 / Day 1-2：可运行骨架**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:135:**Week 1 / Day 3-4：最小流程**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:138:- 两级审批
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:142:**Week 1 / Day 5：验收硬化**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:149:如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:163:Week 4开始微信小程序主流程开发前，必须满足：
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:165:1. 单端范围已确认：首版只做微信小程序，不并行React Native。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:167:3. 前端mock server或mock JSON可用，覆盖登录、提交、审批、查询、错误态。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:168:4. 核心后端API在开发环境可跑通：登录、提交、审批、查询。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:169:5. 认证策略固定为"演示期学号/工号密码，微信OAuth后置"，前端只封装token机制，不等待OAuth。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:180:- 宿舍真实API
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:181:- 微信OAuth真实接入
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:182:- 完整CSV导入后台
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:189:- 如果登录、提交、审批、查询四个核心端点还没有可运行实现，前端仍可做一周mock驱动开发，但Week 5必须切到真实开发环境联调。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:201:- Week 1做纵向切片
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:202:- Week 1不做附件、通知、微信OAuth
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:203:- Week 10只验收和修复
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:205:这比文档40的"Week 1只做数据契约、Week 8-9才做前端"更好。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:211:如果Week 0花3天定义契约，再Week 1花5天做切片，总体变成8个工作日。不是不可以，但这应被明确计入计划，而不是把"现在"当免费缓冲。建议Week 0限制为1-2个工作日，超过就冻结当前假设继续做，后续进入v0.2。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:217:**问题3：Week 1"无权限校验"会削弱纵向切片。**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:219:最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:223:Claude前面说"前端Week 4并行"，后面修正建议又写"Week 2：CSV导入 + 前端开始"。这两个说法需要统一。我的建议是：Week 2可以开始前端技术预研和API client封装，但微信小程序主流程页面开发以Week 4为正式启动点。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:225:**问题5：CSV导入仍可能挤压Week 2。**
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:227:Claude建议Week 2做CSV导入并让前端开始，但CSV staging、校验报告、upsert、软停用、审计日志本身就是一周以上风险项。Week 2的目标应定义为"CSV导入v1可用"，前端只做轻量准备；不要让Week 2同时承诺完整导入和主流程前端。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:231:Week 1可以交Postman集合，但必须有自动化端到端测试。否则每次契约变化都靠人工点接口，后续Week 2-4会快速失控。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:241:| Week 0 / 1-2工作日 | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:242:| Week 1 | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:243:| Week 2 | CSV导入v1 | staging、校验报告、upsert、软停用基础、导入审计基础 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:245:| Week 4-6 | 微信小程序并行开发 | 登录、申请、审批、查询主流程，使用mock并逐步联调真实后端 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:246:| Week 6-7 | 宿舍真实API或降级方案 | 真实Provider、错误分类、缓存/降级、人工证明路径 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:248:| Week 10 | 验收演示 | 演示脚本、缺陷修复、文档，不新增功能 |
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:254:1. **数据契约v0.1应该现在冻结还是Week 1前半？范围最小还是完整？**  
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:255:   现在冻结，限制在1-2个工作日内完成。范围是"最小可执行契约"，不是极简字段，也不是完整未来模型。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:257:2. **Week 1的7-10天工作量是否现实？如何调整？**  
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:258:   如果指7-10人日，在2-3人团队下现实；如果指7-10日历天，不现实。调整方式是Week 0先完成契约，Week 1只做后端最小闭环，推迟CSV完整导入、附件、通知、微信OAuth、真实宿舍API。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:261:   v0.2可消费契约、mock可用、核心API可跑、认证策略固定为演示期薄认证、状态枚举/错误码稳定、API owner和变更机制明确。不要求附件、通知、真实OAuth、真实宿舍API完成。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:264:   方向可行，但必须修正：Week 0要timebox，v0.1要可执行而非字段清单，Week 1不能砍掉最小权限校验，前端启动时间要统一，Week 2不要同时塞满CSV和主流程前端。
docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md:270:**接受Claude的拆分方向，但不接受把契约冻结推迟到Week 1前半，也不接受Week 1无权限校验的纵向切片。**
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:25:- ✅ 从外部数据库读取数据（如宿舍清退状态）
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:28:- 学校A宿舍系统用MySQL
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:29:- 学校B宿舍系统用SQL Server
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:30:- 学校C宿舍系统用Oracle
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:5:**审查范围：** API设计、审批流程、部署架构、安全设计、性能优化、测试策略
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:26:1. **MAJOR**: 微信登录API（lines 698-723）未体现最终确定的绑定/安全流程（lines 1090-1106）：
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:44:4. **MAJOR**: 审批API（lines 907-945）缺少：
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:46:   - 当前审批人验证
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:63:- 审批/更新端点要求`version`或`If-Match`
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:64:- 文档化角色范围列表语义：学生查看自己记录，辅导员查看分配年级/当前审批人，管理员查看全部
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:68:## 第5章：审批流程设计
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:91:   - 提交/审批/驳回的审计日志
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:96:6. **MINOR**: 强制上传宿舍证明（line 1251）应与外部宿舍系统验证和手动降级协调（lines 1332-1333, 1512-1514）
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:99:- 按审批节点跟踪超时，不是从原始提交时间
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:101:- 每次状态转换：验证状态+角色+当前审批人，锁定或检查版本，写入approval/audit/history行，更新`current_approver_id`
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:159:3. **MAJOR**: 认证安全章节（lines 1719-1731）未包含最终确定的5项微信/认证加固措施（lines 1101-1106）
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:168:- 添加子章节：速率限制、上传安全、微信绑定安全、审计日志、加密`system_configs`
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:186:3. **MINOR**: 缓存申请状态（lines 1778-1782）可能产生过期审批视图
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:193:- 用最终确定的数据库索引替换索引列表，并将每个映射到其查询：待审批、学生列表、未读通知、审计查找
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:234:- 添加双重审批和微信绑定竞态的并发测试
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:243:- 第5章（审批流程）：REVISE - 5个MAJOR问题
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:16:**核心问题：** 方案把"用户主数据 API 化"当成默认终局，偏离了此前已达成的首版共识：学生、辅导员、班级映射应优先走 CSV/Excel 导入，宿舍清退才是实时 API。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:30:`RealUserDataProvider` 不应成为认证、审批、班级映射的运行时依赖。用户、辅导员、班级映射是本系统的基础主数据，影响登录、权限、审批人分配和历史追溯。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:34:应落入本地数据库，通过 CSV/API Provider 输入到 staging，再校验、upsert、软停用。此前设计已经定义了 staging + upsert + 软停用、导入审计和校验报告：[31-data-source-requirements-consensus-v2.md](../codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md) 第282行。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:47:1. 用户主数据（学生、辅导员、班级映射）通过CSV导入到本地数据库
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:48:2. Provider只用于宿舍清退状态的实时查询
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:72:- **宿舍清退API：** 1-2周
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:73:- **用户主数据API（如果坚持）：** 2-4周（牵涉数据模型、导入/同步策略、账号状态、审批人映射和验收演练）
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:117:当前设计用一个开关同时切用户数据和宿舍清退：[37-api-blocking-solution-review-request.md](./37-api-blocking-solution-review-request.md) 第160行。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:131:- 支持"用户主数据 CSV + 宿舍清退 API"的混合模式
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:148:- 宿舍状态：`completed/pending/not_started/unknown`
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:155:宿舍清退枚举和降级规则已有定义：[数据对接说明文档.md](../../数据对接说明文档.md) 第306行
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:167:Provider 契约、DTO、种子数据、导入接口应在 Week 1-2 完成，否则认证、审批、前端都会先绑定临时模型，后续返工。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:175:| Week 1 | 数据契约、DTO、Provider接口、种子数据、导入模型 | 数据契约文档、DTO定义、Provider接口 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:176:| Week 2-3 | CSV/staging/upsert/审计和核心账号数据 | CSV导入功能、staging表、审计日志 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:177:| Week 3-6 | 申请、审批、附件、通知 | 核心业务模块 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:178:| Week 6-7 | 宿舍清退Provider、降级流程、缓存、错误分类 | 宿舍清退集成模块 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:179:| Week 8-9 | 前端 | React Native、微信小程序 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:180:| Week 10 | 联调、演示、验收清单 | 演示版本 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:183:- 宿舍清退 API：1周
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:184:- 用户主数据 API 替换 CSV：另计 2-4周
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:192:若外部 API 字段继续缺失，首版应坚持 CSV/Excel 主数据导入，不等待 API。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:203:│  CSV / API / DB View / Mock                │
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:226:│  作为认证、权限、审批和历史记录的唯一运行时依据 │
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:234:│    DormCheckoutProvider（宿舍清退查询）      │
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:241:1. **外部数据源：** CSV/API/DB view/Mock
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:244:4. **本地数据库：** 作为认证、权限、审批和历史记录的唯一运行时依据
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:255:### 宿舍清退状态缓存
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:296:**"Seed/Mock + Provider 抽象 + CSV 主数据导入 + 宿舍清退 API 适配"**
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:311:1. **Week 1-3：** CSV导入 + 种子数据
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:313:3. **Week 6-7：** 宿舍清退API对接
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:315:5. **Week 10：** 联调和演示
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:320:如果数据变更频率高，可升级为API/DB同步。但首版应坚持CSV导入，快速上线。
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:21:### 2.1 问题1：CSV导入策略错误（行329）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:36:2. 即使使用 `DELETE FROM users`，也会导致历史申请记录中的审批人引用失效
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:54:-- 2. 导入CSV到staging表
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:214:**CSV导入映射：**
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:216:学生CSV模板：
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:281:    planned_leave_date_start DATE,              -- 允许的最早离校日期
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:282:    planned_leave_date_end DATE,                -- 允许的最晚离校日期
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:342:| 账号状态 | 登录 | 创建申请 | 审批 | 查看历史 | 接收通知 |
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:348:- 学生：本次CSV导入中未出现
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:349:- 辅导员：本次CSV导入中未出现
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:353:- 下次CSV导入中重新出现 → 自动激活（`is_active=true`）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:413:   - `users_staging`：CSV导入临时表
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:418:### 4.2 CSV导入策略修改（第三章3.3节）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:428:1. CSV导入到临时staging表
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:446:**CSV技术要求：**
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:453:**阶段2：CSV导入实现（2周）**
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:464:1. ✅ CSV导入从"全量覆盖"改为"staging + upsert + 软停用"
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:486:- 第186-196行：历史审批人一致性规则的思考过程
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:11:用户提出在宿舍管理系统数据对接中，需要补充以下字段：
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:18:   - 用途：精确定位学生宿舍床位
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:20:   - 说明：可选字段，如果宿舍管理系统有床号信息则提供
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:67:**修改位置6：CSV格式示例**
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:69:CSV添加班级和床号列：
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:71:学号,姓名,班级,宿舍楼栋,宿舍房间号,床号,是否已清退,清退日期,清退状态,备注
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:74:### 2.2 CSV模板文件（`docs/templates/宿舍清退数据模板.csv`）
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:76:更新CSV模板，添加班级和床号列，包含示例数据。
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:80:**修改位置：第6.2节 - 宿舍管理系统对接 - 接口定义（第1629-1639行）**
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:118:  - 优点：便于按班级统计离校情况、辅导员管理
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:123:  - 优点：精确定位学生宿舍位置
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:124:  - 缺点：不是所有宿舍管理系统都有床号信息
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:138:- 宿舍信息：dorm_building、dorm_room、bed_number
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:159:- ✓ CSV模板文件
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:178:- API响应的class_name：宿舍管理系统返回的班级（可能不同步）
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:190:- 场景2：需要在离校凭证上显示床号，需要存储
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:191:- 场景3：需要统计各宿舍楼的离校情况，需要存储
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:29:- ✅ 覆盖审批队列、通知查询、审计追踪
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:23:- 宿舍系统可能无法提供班级信息（不同学校系统差异）
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:82:- 如果后续需要在离校凭证上显示床号，再添加到applications表
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:103:   - [ ] 检查Excel/CSV示例格式正确
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:116:| dorm_building | String | 宿舍楼栋 | 是 | "1号楼" |
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:117:| dorm_room | String | 宿舍房间号 | 是 | "101" |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:16:2. ✓ 定义v0.1为"最小可执行契约"（不是字段清单）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:17:3. ✓ 坚持Week 1保留最小权限校验（我的"无权限校验"建议是错误的）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:19:5. ✓ 明确Week 2只做CSV导入v1（不塞前端主流程）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:31:**v0.1范围：最小可执行契约**
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:45:**时间限制：** 1-2工作日完成，超时冻结当前假设进入Week 1
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:47:### 2. Week 1工作量：7-10人日现实，需严格砍范围
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:51:**Week 1必须保留：**
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:57:- 辅导员审批API
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:58:- 学工部审批API
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:63:**Week 1推迟：**
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:64:- 完整CSV导入
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:67:- 微信OAuth
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:69:- 宿舍真实API
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:70:- 复杂审批流（转办、撤回、驳回重提）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:72:**我的错误：** 建议Week 1"无权限校验"是错误的。Codex正确指出：纵向切片的价值正是验证角色、数据、状态机和审批链路能否串起来。
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:79:1. 单端范围确认（只做微信小程序）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:82:4. 核心后端API可跑通（登录、提交、审批、查询）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:91:- 宿舍真实API
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:92:- 微信OAuth真实接入
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:93:- 完整CSV导入后台
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:105:**修正3：** Week 1保留最小权限校验（不能砍）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:107:**修正5：** Week 2只做CSV导入v1（不塞前端主流程）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:108:**修正6：** Week 1必须有自动化端到端测试（不只是Postman集合）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:116:| **Week 0** (1-2工作日) | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog | 前端可用mock跑通登录→提交→审批→查询流程 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:117:| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:118:| **Week 2** | CSV导入v1 | Staging表、校验报告、upsert、软停用基础、导入审计基础 | 可导入10学生+2辅导员，生成校验报告，软停用未导入账号 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:120:| **Week 4-6** | 微信小程序并行开发 | 登录、申请、审批、查询主流程 | 小程序可用mock跑通完整流程，逐步联调真实后端 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:121:| **Week 6-7** | 宿舍真实API或降级方案 | 真实Provider、错误分类、缓存/降级、人工证明路径 | 真实API集成或降级方案可用 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:123:| **Week 10** | 验收演示 | 演示脚本、缺陷修复、文档 | 可演示版本交付，不新增功能 |
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:135:# 数据契约 v0.1 - 最小可执行契约
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:159:### 4.3 审批
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:180:**验收标准：** 前端可用mock跑通登录→提交→审批→查询流程
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:204:## Week 1 (Day 1-5)
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:214:- [ ] 辅导员审批API
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:215:- [ ] 学工部审批API
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:227:- Day 3结束仍无申请提交API → 只保留"学生提交→辅导员审批→查询"
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:228:- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:241:1. ✓ Week 0是1-2工作日timebox，冻结v0.1最小可执行契约
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:243:3. ✓ Week 1交付后端纵向切片，保留最小角色校验
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:244:4. ✓ Week 1工作量7-10人日现实（2-3人团队，5个工作日）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:246:6. ✓ Week 2只做CSV导入v1，不塞前端主流程
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:247:7. ✓ Week 10只做验收演示，不新增功能
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:248:8. ✓ 单端交付（微信小程序优先）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:258:- CSV导入v1的详细设计（Week 2开始前）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:259:- 微信小程序技术栈选择（Week 3开始前）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:260:- 宿舍真实API集成方案（Week 5开始前）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:276:**Claude回应：** 完全同意。先产出可执行的Week 0-1计划，验证纵向切片可行性，再更新总实施计划。
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:285:- Week 0（1-2工作日）：冻结v0.1最小可执行契约
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:286:- Week 1（5工作日）：后端纵向切片（保留最小权限校验）
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:287:- Week 2：CSV导入v1
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:289:- Week 4-6：微信小程序并行开发
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:290:- Week 6-7：宿舍真实API或降级
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:292:- Week 10：验收演示
docs/discussions/codex-review-2026-05-30/45-next-steps-claude-response-round2.md:302:- Week 10过载风险
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:14:Codex正确指出方案A的核心问题：瀑布式排期、前端后置、Week 10过载。纵向切片/MVP优先的方向是对的。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:18:2. Week 1交付"可运行骨架"的范围定义
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:29:原方案A确实是"认证→申请→审批→附件→通知→前端→联调"的横向模块堆叠，风险在Week 8-10才暴露。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:31:**Codex的纵向切片方案更合理：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:33:- Week 2：CSV导入硬化
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:38:- Week 10：验收演示
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:44:2-3人10周同时交付React Native和微信小程序不现实。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:47:- 首版：微信小程序（覆盖主要用户群）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:50:### 3. Week 10不能过载
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:54:Week 10应该只做验收、演示、缺陷修复，不塞新功能，不兜底延期。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:67:- 宿舍API各种错误状态
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:75:> 现在就应冻结v0.1：字段、枚举、样例CSV、错误码、前端API mock。Week 1用它跑纵向切片。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:84:3. 样例CSV从哪里来？是Mock数据还是需要真实样本？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:90:- 如果v0.1范围太大，Week 1无法完成纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:94:- Week 1前半：冻结v0.1并生成样例数据（2-3天）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:95:- Week 1后半：用v0.1跑纵向切片（2-3天）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:98:你说的"现在"冻结，是指立即（今天）还是Week 1开始前？如果是立即，v0.1的范围应该多大？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:102:## 分歧点2：Week 1交付"可运行骨架"的范围
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:106:> Week 1应交付可运行骨架、契约测试、seed数据、最小审批流，而不是只交文档和接口。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:117:- 最小申请审批闭环
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:127:5. **最小申请审批闭环**：2-3天（Application模型、Approval模型、状态机、3个API）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:133:- 如果团队2-3人，Week 1（5个工作日）能完成吗？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:138:- Week 1目标：可运行的最小申请审批流（不含附件、通知）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:139:- Week 1交付：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:142:  - 申请提交API + 审批API（简化版，无权限校验）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:145:- Week 1不交付：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:152:你认为Week 1的7-10天工作量是否现实？如果不现实，哪些可以推迟到Week 2？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:160:> Week 4-6：前端并行开发，不等后端全完，先做微信小程序主流程，使用前端API mock。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:169:3. 核心流程后端API已实现（申请、审批、状态查询）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:170:4. 认证机制已确定（学号+密码还是微信OAuth？）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:178:- Week 2：后端核心API完成（申请、审批、状态查询）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:181:- Week 5-6：前端继续开发，后端做宿舍API集成
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:193:Week 0-1：契约v0.1 + 纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:198:- 最小申请审批闭环
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:210:**Week 1（纵向切片，5天）：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:216:- Day 3-4：最小申请审批流
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:220:  - 审批API（简化版）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:224:  - 端到端测试（登录→提交→审批→查询）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:226:**Week 1交付物：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:231:**Week 1不交付：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:241:### 问题1：Week 1做数据契约太晚吗？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:244:不是太晚，而是Week 1的目标定义不清楚。应该是：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:246:- Week 1：用v0.1跑纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:252:- 单端（微信小程序）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:253:- 核心流程（申请、审批、状态查询）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:255:- 简化认证（学号+密码，无微信OAuth）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:257:- 简化通知（邮件通知，无微信推送）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:261:- 微信OAuth
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:263:- 微信模板消息
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:267:### 问题8：Week 1的工作量是否饱和？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:270:Codex列出的Week 0-1工作量是7-10天，超过Week 1的5天。需要拆分：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:272:- Week 1（5天）：纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:284:- **选项A（最小）：** 只包含申请审批流需要的字段（student_id, name, application_id, status, approver_id）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:285:- **选项B（完整）：** 包含所有字段（包括附件、通知、宿舍清退相关字段）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:289:### 2. Week 1纵向切片的验收标准
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:292:Week 1结束时，如何验证"纵向切片"成功？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:295:- [ ] 可以用Postman调用5个API（登录、提交、审批、查询、Mock宿舍）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:296:- [ ] 端到端测试通过（登录→提交→审批→查询）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:317:1. ✓ 纵向切片/MVP优先
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:320:4. ✓ Week 10只做验收
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:324:2. Week 1工作量是否现实（7-10天 vs 5天）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:329:- Week 1（5天）：纵向切片（后端骨架 + 薄认证 + 最小审批流）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:330:- Week 2（5天）：CSV导入 + 前端开始
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:332:- Week 5-6：宿舍API + 前端继续
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:335:- Week 10：验收演示
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:18:6. ✓ P2 - 统一审批时限（1个工作日）
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:88:Postman集合文件：`docs/templates/宿舍管理系统API.postman_collection.json`
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:124:### 修复6：统一审批时限 [P2]
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:130:- 辅导员审批：提交后24小时内
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:131:- 学工部审批：辅导员通过后24小时内
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:136:- 辅导员审批：提交后1个工作日内
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:137:- 学工部审批：辅导员通过后1个工作日内
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:152:- 审批本年级学生的申请
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:153:- 审批其他年级学生
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:160:- 审批负责班级学生的申请
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:161:- 审批其他班级学生
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:205:- ✓ `docs/用户设计说明书.md` - 初始密码、审批时限、辅导员权限、性能指标
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:20:- 原设计采用CSV导入用户数据（学生、辅导员、班级）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:22:- 宿舍管理系统只提供了一个第三方API文档（goliveplus租户用户查询API）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:23:- 该API字段不满足需求（缺少班级、院系、专业、宿舍清退状态等）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:26:1. 完整的API文档（学生信息、辅导员信息、宿舍清退状态）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:44:- Phase 3: 离校申请模块
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:45:- Phase 4: 审批管理模块
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:47:- Phase 6: 通知模块（可Mock微信）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:80:    """宿舍清退状态提供者接口"""
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:83:        """查询学生宿舍清退状态"""
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:198:| Week 1-2 | 基础设施 + Mock数据 | Django项目、种子数据（100学生、10辅导员） |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:199:| Week 3-6 | 核心业务逻辑 | 申请、审批、附件、通知模块 |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:201:| Week 8-9 | 前端开发 | React Native、微信小程序（测试AppID） |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:202:| Week 10 | 测试 | 单元测试、集成测试（Mock数据） |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:394:- **项目名称：** 毕业生离校申请审批系统
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:395:- **技术栈：** Python Django + PostgreSQL + Redis + React Native + 微信小程序
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:403:- Round 2: API、审批、部署、安全、性能（29个问题修复）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:12:**方案名称：** Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:15:1. 用户主数据（学生、辅导员、班级映射）通过CSV导入到本地数据库
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:17:3. 宿舍清退状态通过API实时查询（可缓存、可降级）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:18:4. 本地数据库是认证、权限、审批的唯一运行时依据
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:29:外部数据源 (CSV/API/Mock)
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:35:本地数据库 (认证、权限、审批的唯一运行时依据)
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:38:DormCheckoutProvider (宿舍清退实时查询)
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:62:# 2. 宿舍清退Provider（用于运行时查询）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:64:    """宿舍清退状态提供者接口"""
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:67:        """运行时查询宿舍清退状态"""
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:149:USER_DATA_SOURCE = 'csv'  # 生产环境使用CSV导入
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:150:DORM_CHECKOUT_SOURCE = 'api'  # 宿舍清退使用API
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:184:| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:185:| Week 2-3 | CSV导入功能、staging表、upsert逻辑、审计日志 | CSV导入模块、导入校验报告 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:186:| Week 3-6 | 申请、审批、附件、通知模块 | 核心业务功能 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:187:| Week 6-7 | 宿舍清退Provider、降级流程、缓存、错误分类 | 宿舍清退集成模块 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:188:| Week 8-9 | 前端开发 | React Native、微信小程序 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:189:| Week 10 | 联调、演示、验收清单 | 可演示版本（Mock数据） |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:192:- 宿舍清退API集成：1周
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:193:- 用户主数据API替换CSV（如需）：另计2-4周
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:199:1. **Week 1结束：** 数据契约冻结，接口定义完成
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:200:2. **Week 3结束：** CSV导入功能可用，种子数据就绪
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:202:4. **Week 7结束：** 宿舍清退API对接完成
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:203:5. **Week 10结束：** 可演示版本交付
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:244:- **宿舍清退状态：** 覆盖所有枚举值（completed/pending/not_started/unknown）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:256:### 6.2 宿舍清退状态缓存
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:306:| RealUserDataProvider运行时查询 | CSV导入到本地数据库 | 用户主数据是基础数据，不应依赖外部API |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:309:| Week 7做接口抽象 | Week 1做数据契约和接口 | 避免后续返工 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:314:1. **不要偏离已达成的共识** - 原方案错误地将用户主数据API化，偏离了CSV导入的共识
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:324:### 9.1 Week 10交付物
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:328:- [ ] CSV导入功能和校验逻辑
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:329:- [ ] 宿舍清退API适配器（Mock实现）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:351:| 真实API字段与Mock不一致 | P1 | Week 1冻结数据契约，预留扩展字段 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:358:- **API延期：** 首版坚持CSV导入，不等待API
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:378:2. **Week 1启动：** 数据契约和接口设计
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:379:3. **Week 2-3：** CSV导入功能开发
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:27:**Claude确认：** ✓ 已在前一轮修复（commit: docs: 修正CSV模板文件扩展名引用）
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:111:### 问题6：审批时限口径不一致 [P2]
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:122:3. 与审批流程设计一致
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:232:7. ✓ 问题6：统一审批时限
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:17:- ✓ 达成最终共识：Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:22:外部数据源 (CSV/API/Mock)
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:28:本地数据库 (认证、权限、审批的唯一运行时依据)
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:31:DormCheckoutProvider (宿舍清退实时查询)
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:37:1. 更新实施计划文档（调整Week 1-10任务分配）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:38:2. 开始Week 1工作：数据契约、DTO、ImportSource接口设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:64:   - 调整Week 1-10任务分配
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:65:   - 将数据契约和接口设计提前到Week 1
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:68:2. **Week 1启动：** 数据契约和接口设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:74:3. **Week 2-3：** CSV导入功能开发
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:88:- Week 1的工作量是否合理？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:97:**问题1：Week 1做数据契约是否太晚？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:98:- 数据契约影响认证、审批、前端所有模块
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:99:- 是否应该在Week 1之前（现在）就冻结数据契约？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:100:- 如果现在冻结，Week 1可以做什么？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:103:- 当前计划是按模块顺序开发（认证→申请→审批→...）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:105:- 例如：简化版申请+审批+通知，验证整体架构
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:107:**问题3：CSV导入功能是否应该更早？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:108:- 当前计划Week 2-3做CSV导入
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:110:- 是否应该Week 1就完成CSV导入？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:121:- 对于首版（CSV导入）是否过于复杂？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:122:- 是否应该先实现CSV导入，后续再抽象？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:124:**问题6：宿舍清退API集成时机？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:125:- 当前计划Week 6-7做宿舍清退API对接
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:126:- 但申请提交（Week 3）就需要校验宿舍清退状态
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:132:- Week 1: 数据契约和接口
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:133:- Week 2-3: CSV导入
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:135:- Week 6-7: 宿舍清退API
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:137:- Week 10: 联调
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:141:**问题8：Week 1的工作量是否饱和？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:151:- 当前：数据契约→CSV导入→核心业务→API集成→前端→联调
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:157:- 当前：认证→申请→审批→附件→通知→集成→前端
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:158:- 是否应该：申请+审批核心流程→认证→附件→通知→集成→前端？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:213:- **外部依赖：** 宿舍清退API信息待提供
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:214:- **交付要求：** Week 10可演示版本（Mock数据）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:219:- **数据对接文档：** CSV模板、API规范
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:224:- CSV导入是首版主数据来源
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:225:- 宿舍清退API在Week 6-7前到位
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:226:- 微信小程序测试AppID可用
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:5:**目的：** 明确毕业离校系统所需的数据源，提交给宿管系统方反馈
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:15:| 学生基本信息 | P0 | 创建学生账号、身份识别、班级映射 | DB优先 / API备选 / CSV降级 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:16:| 宿舍清退数据 | P0 | 验证学生是否完成宿舍清退 | API优先 / DB备选 / CSV降级 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:17:| 辅导员基本信息 | P0 | 创建辅导员账号、审批权限 | DB优先 / API备选 / CSV降级 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:18:| 班级-辅导员对应关系 | P0 | 自动分配审批人 | DB优先 / API备选 / CSV降级 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:24:- **CSV降级**：当无法提供DB访问或API时，通过CSV文件导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:36:- 自动分配审批人（根据班级匹配辅导员）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:86:**对接方式3：CSV文件导入（降级）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:93:### 2.2 宿舍清退数据
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:96:- 验证学生是否完成宿舍清退
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:97:- 作为离校申请的前置条件
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:105:| 宿舍楼栋 | dorm_building | 文本 | 否 | 宿舍楼栋名称 | 1号楼 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:106:| 宿舍房间号 | dorm_room | 文本 | 否 | 宿舍房间号 | 101 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:137:**对接方式3：CSV文件导入（降级）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:140:- 模板文件：`docs/templates/宿舍清退数据模板.csv`（已有）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:148:- 分配审批权限
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:149:- 作为一级审批人
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:183:**对接方式3：CSV文件导入（降级）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:193:- 自动分配审批人（学生提交申请时，根据班级自动找到对应辅导员）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:194:- 辅导员权限边界（辅导员只能查看和审批负责班级的学生）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:196:- 审批统计按班级、辅导员追踪
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:199:- 如果没有这个数据，系统无法自动分配审批人
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:237:**对接方式3：CSV文件导入（降级）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:331:- 参考当前数据对接文档中的宿舍清退状态查询接口
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:336:### 4.3 方式3：CSV文件导入（降级）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:353:1. 宿管系统方按模板导出CSV文件
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:360:- 文件格式：CSV
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:382:- CSV导入：建议每日更新，延迟不超过24小时
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:400:1. 宿舍清退数据：使用现有API接口
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:401:2. 学生基本信息：数据库直连或CSV导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:402:3. 辅导员信息：CSV导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:403:4. 班级-辅导员映射：CSV导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:408:1. 宿舍清退数据：API接口（已有）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:409:2. 学生基本信息：CSV导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:410:3. 辅导员基本信息：CSV导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:411:4. 班级-辅导员对应关系：CSV导入（必须100%覆盖）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:424:   - [ ] 宿舍清退数据表
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:431:1. 除了宿舍清退状态查询接口，是否可以提供其他数据查询接口？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:434:### 7.3 CSV导入情况
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:435:1. 如果使用CSV导入，是否可以按模板定期导出数据？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:448:1. **宿管系统方**：反馈上述问题，提供数据库/API/CSV的可行性
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:451:4. **本系统方**：更新数据对接说明文档，提供CSV模板文件
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:17:2. **设计层面**：部分设计过度复杂，实施风险高（微信绑定、性能目标、冗余表）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:245:### 争议2：微信绑定安全措施
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:253:1. ✓ 密码验证：微信绑定已有账户需要密码
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:265:    """微信绑定已有账户"""
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:277:        raise ValidationError("该学号已绑定其他微信")
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:309:    """同步发送微信通知"""
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:366:    """检查审批超时（简化版）"""
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:433:+ 核心模块强制TDD：认证、审批、状态机
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:454:- ✓ 简化微信绑定措施（5项→2项）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:513:| 10 | 设计 | 简化微信绑定 | system-design.md | 1h |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:16:2. 对接方式里对学生、辅导员、班级映射默认写“DB 优先”偏激进。首版更合理的路径是：账号与映射数据优先 CSV/Excel 批量导入，宿舍清退优先 API。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:17:3. 宿舍清退字段与上一轮字段共识存在轻微不一致：`checkout_status` 在本文件中标为可选，但既有字段共识中 API 响应建议必填。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:18:4. 缺少若干实施级关键问题，例如账号标识映射、终审管理员分配规则、同步覆盖策略、历史审批人不被后续映射变更自动改写等。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:33:| 宿舍清退数据 | 完整 | 支撑提交前置校验，是当前已明确需要自动校验的数据。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:34:| 辅导员基本信息 | 完整 | 支撑辅导员账号和一级审批主体。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:40:图书馆清书状态、财务结清状态、独立学籍状态没有列为 P0 是合理的。当前用户设计和系统设计仍保留截图上传、人工审核和宿舍系统异常时人工降级的方案，因此这三类不应阻塞首版上线。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:47:2. **离校批次配置。** 包括毕业届别、开放申请时间、允许计划离校日期范围。这些可由系统后台配置，不必来自外部系统。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:61:   仅“是否毕业生”不足以表达延期毕业、结业、休学、退学、已毕业归档等异常状态。首版可以保留 `is_graduating`，但建议增加一个更直接的离校资格字段。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:66:3. `phone` 是否可选需要结合微信绑定策略确认。  
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:67:   如果登录只依赖学号密码和微信 OAuth，手机号可选合理；如果要支持短信验证、密码找回或紧急联系，手机号应至少在导入模板中强烈建议提供。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:69:### 3.2 宿舍清退数据
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:83:   对 API 或 CSV 数据都建议记录外部系统数据更新时间，便于区分“未完成清退”和“数据过期/未同步”。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:90:   如果通知主要走微信，手机号可作为推荐字段而非硬性 P0。若学校确实要求短信/电话通知，则保留必填也合理。建议在文档中说明依据。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:93:   `is_active` 已有，但应补充离职、调岗、停用后如何处理其名下未完成审批，以及是否允许历史审批记录继续引用已停用账号。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:111:3. 管理员离岗后未完成审批任务如何转交。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:121:| 学生基本信息 | DB 优先 / API 备选 / CSV 降级 | 建议改为 CSV/Excel 首版优先，DB/API 作为条件成熟后的增强。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:122:| 宿舍清退数据 | API 优先 / DB 备选 / CSV 降级 | 合理。提交前置校验对实时性要求更高，API 价值最大。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:123:| 辅导员基本信息 | DB 优先 / API 备选 / CSV 降级 | 建议改为 CSV/Excel 或手动批量维护优先，人数少且变化低频。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:124:| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:129:DB、API、CSV 三种方式的技术要求整体清晰，但建议补充：
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:134:4. CSV 需补充导入覆盖策略：全量覆盖、增量更新、软删除/停用、重复数据处理、失败回滚。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:141:2. CSV 通过 SFTP 或后台上传时应限制权限，并记录上传人、文件哈希、导入批次和导入结果。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:168:当前问题覆盖了数据库、API、CSV 和数据范围，基本可用，但建议扩展为面向多方的数据确认清单。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:181:2. 是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:188:9. CSV 导入时是否采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:190:11. 是否有统一身份认证或微信绑定前置要求？是否需要导入手机号/邮箱用于找回密码或二次验证？
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:203:1. 宿舍清退：优先使用宿管系统 API；若不可用，使用每日 CSV 导入；异常时保留人工证明。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:204:2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:205:3. 辅导员信息：首版优先 CSV/Excel 或后台批量维护；若有统一身份或人事 API，再对接。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:206:4. 班级-辅导员映射：首版优先 CSV/Excel 强校验，上线前必须 100% 覆盖当届学生。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:221:2. 先落地三份基础 CSV/Excel 模板：学生、辅导员、班级-辅导员映射。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:223:4. 再对接宿舍清退 API，并把 API 失败、超时、数据过期纳入统一降级处理。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:235:> 明确毕业离校系统所需的数据源，提交给宿管系统方反馈
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:239:> 明确毕业离校系统所需的数据源，提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人反馈。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:247:| 学生基本信息 | CSV/Excel 首版优先 / API 或 DB 视图增强 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:248:| 辅导员基本信息 | CSV/Excel 或后台批量维护首版优先 / 人事或统一身份 API 增强 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:249:| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:250:| 宿舍清退数据 | API 优先 / DB 只读视图备选 / CSV 降级 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:258:| 离校申请资格 | eligible_for_leave | 布尔 | 建议是 | 是否允许提交本批次离校申请 | true |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:261:如不新增字段，至少应说明 `is_graduating=true` 即表示具备本批次离校申请资格。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:263:### 8.4 宿舍清退字段
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:279:3. `is_active=false` 时不再分配新申请，但历史审批记录仍保留。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:287:| 是否主辅导员 | is_primary | 布尔 | 否 | 多辅导员场景下标识主审批人 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:310:2. 将学生、辅导员、班级映射的首版推荐方式从“DB 优先”调整为“CSV/Excel 优先，API/DB 增强”。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:311:3. 统一宿舍清退字段必填性，特别是 `checkout_status`。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:312:4. 补充终审管理员/终审组配置、账号标识映射、历史审批人一致性规则。

exec
/bin/bash -lc "rtk nl -ba docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md | sed -n '1,220p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# 数据源需求共识文档
     2	
     3	**文档版本：** v2.0  
     4	**创建时间：** 2026-05-27  
     5	**修订时间：** 2026-05-27  
     6	**目的：** 明确毕业离校系统所需的数据源，提交给宿管系统方反馈
     7	
     8	---
     9	
    10	## 版本变更说明（v1 → v2）
    11	
    12	**主要修正：**
    13	
    14	1. **CSV导入策略**：从"全量覆盖"改为"staging表 + upsert + 软停用"
    15	2. **数据库模型调整**：
    16	   - users表：`student_id`改为可空，新增`employee_id`和`class_id`字段
    17	   - 新增`class_counselor_mapping`表（班级-辅导员映射）
    18	   - 新增`graduation_batches`表（批次配置）
    19	   - 新增`import_logs`表（导入审计）
    20	   - 拆分staging表：`students_staging`、`counselors_staging`、`class_mapping_staging`
    21	3. **认证约束调整**：增加`password_setup_required`支持CSV预导入账号
    22	4. **对接方式调整**：学生/辅导员/班级映射改为"CSV/Excel首版优先"
    23	5. **约束增强**：学生必须有`class_id`，复用`system_configs`表
    24	
    25	**修正依据：**
    26	- Codex第二轮审查（34-codex-second-review-response.md）
    27	- Codex关键问题审查（35-response-to-codex-critical-issues.md）
    28	
    29	---
    30	
    31	## 一、数据源概述
    32	
    33	本系统需要以下数据源支持系统运行：
    34	
    35	| 数据源 | 优先级 | 用途 | 对接方式 |
    36	|--------|--------|------|----------|
    37	| 学生基本信息 | P0 | 创建学生账号、身份识别、班级映射 | **CSV/Excel首版优先** / API或DB增强 |
    38	| 宿舍清退数据 | P0 | 验证学生是否完成宿舍清退 | API优先 / DB备选 / CSV降级 |
    39	| 辅导员基本信息 | P0 | 创建辅导员账号、审批权限 | **CSV/Excel首版优先** / 人事或统一身份API增强 |
    40	| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
    41	| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |
    42	
    43	**对接方式说明：**
    44	- **CSV/Excel首版优先**：首版采用CSV/Excel批量导入，快速上线，后续根据数据变更频率决定是否升级为API/DB
    45	- **API优先**：调用宿管系统提供的API接口（实时校验场景）
    46	- **DB备选**：直接读取宿管系统数据库（需要安全审批和网络配置）
    47	- **CSV降级**：当无法提供API或DB时，通过CSV文件导入
    48	
    49	**首版策略调整理由：**
    50	1. **实施周期**：CSV/Excel导入最快，DB直连需要安全审批和网络配置
    51	2. **变更频率**：账号数据变更频率低（学期级），不需要实时同步
    52	3. **风险控制**：CSV导入可以先验证、再导入、可回滚；DB直连风险更高
    53	
    54	---
    55	
    56	## 二、P0数据源详细要求
    57	
    58	### 2.1 学生基本信息
    59	
    60	**用途：**
    61	- 创建学生账号（用于登录系统）
    62	- 身份识别和验证
    63	- 展示学生院系、专业、班级信息
    64	- 自动分配审批人（根据班级匹配辅导员）
    65	
    66	**必需字段：**
    67	
    68	| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
    69	|---------------|---------------|----------|------|------|------|
    70	| 学号 | student_id | 文本 | 是 | 学生唯一标识 | 2022001 |
    71	| 姓名 | name | 文本 | 是 | 学生姓名 | 张三 |
    72	| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
    73	| 专业 | major | 文本 | 是 | 所属专业 | 计算机科学与技术 |
    74	| 班级ID | class_id | 文本 | 是 | 班级唯一标识（核心键） | CS2022-01 |
    75	| 班级名称 | class_name | 文本 | 否 | 班级名称（用于展示） | 计算机科学与技术2022级1班 |
    76	| 年级 | grade | 整数 | 是 | 入学年份 | 2022 |
    77	| 毕业年份 | graduation_year | 整数 | 是 | 预计毕业年份 | 2026 |
    78	| 是否毕业生 | is_graduating | 布尔 | 是 | 是否为当届毕业生 | true |
    79	
    80	**可选字段：**
    81	
    82	| 字段名（中文） | 字段名（英文） | 数据类型 | 说明 | 示例 |
    83	|---------------|---------------|----------|------|------|
    84	| 手机号 | phone | 文本 | 用于找回密码或二次验证 | 13800138000 |
    85	| 邮箱 | email | 文本 | 用于通知或找回密码 | zhangsan@example.com |
    86	
    87	**字段说明：**
    88	- `class_id`：班级唯一标识，全校唯一，用于映射辅导员（**v2新增必填要求**）
    89	- `class_name`：班级显示名称，可能重复、变更或跨届复用，仅用于展示
    90	- `is_graduating`：标识是否为当届毕业生，`true`表示具备本批次离校申请资格
    91	- `graduation_year`：示例统一为2026（与当前项目日期保持一致）
    92	
    93	**CSV模板示例：**
    94	
    95	```csv
    96	student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
    97	2022001,张三,计算机学院,计算机科学与技术,CS2022-01,计算机科学与技术2022级1班,2022,2026,true,13800138000,zhangsan@example.com
    98	2022002,李四,计算机学院,软件工程,SE2022-01,软件工程2022级1班,2022,2026,true,13800138001,lisi@example.com
    99	```
   100	
   101	**数据范围：**
   102	- 只导入当届毕业生（`is_graduating=true` 且 `graduation_year=2026`）
   103	- 约1000人/届
   104	
   105	---
   106	
   107	### 2.2 宿舍清退数据
   108	
   109	**用途：**
   110	- 验证学生是否完成宿舍清退（提交申请前置条件）
   111	- 展示清退状态和完成时间
   112	
   113	**必需字段：**
   114	
   115	| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
   116	|---------------|---------------|----------|------|------|------|
   117	| 学号 | student_id | 文本 | 是 | 学生学号 | 2022001 |
   118	| 姓名 | name | 文本 | 是 | 学生姓名（用于二次验证） | 张三 |
   119	| 清退状态 | checkout_status | 枚举 | **是** | 清退状态（**v2改为必填**） | completed |
   120	| 清退完成时间 | checkout_date | 日期时间 | 条件必填 | 当status=completed时必填 | 2026-05-20 14:30:00 |
   121	| 数据更新时间 | source_updated_at | 日期时间 | 建议 | 外部系统数据更新时间（**v2新增**） | 2026-05-20 15:00:00 |
   122	
   123	**枚举值说明（v2修订）：**
   124	- `completed`：已完成清退
   125	- `pending`：清退中（已申请但未完成）
   126	- `not_started`：未开始清退
   127	- `unknown`：查询失败或数据不可用（用于API异常时的降级）
   128	
   129	**API响应示例：**
   130	
   131	```json
   132	{
   133	  "student_id": "2022001",
   134	  "name": "张三",
   135	  "checkout_status": "completed",
   136	  "checkout_date": "2026-05-20T14:30:00",
   137	  "source_updated_at": "2026-05-20T15:00:00"
   138	}
   139	```
   140	
   141	**降级处理：**
   142	- API查询失败时，返回 `checkout_status: "unknown"`
   143	- 系统允许学生提交申请，但需上传宿舍清退证明截图
   144	
   145	---
   146	
   147	### 2.3 辅导员基本信息
   148	
   149	**用途：**
   150	- 创建辅导员账号（用于登录系统）
   151	- 审批权限管理
   152	- 班级-辅导员映射
   153	
   154	**必需字段：**
   155	
   156	| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
   157	|---------------|---------------|----------|------|------|------|
   158	| 工号 | employee_id | 文本 | 是 | 辅导员唯一标识（**v2新增**） | T2022001 |
   159	| 姓名 | name | 文本 | 是 | 辅导员姓名 | 王老师 |
   160	| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
   161	| 手机号 | phone | 文本 | 否 | 联系电话 | 13900139000 |
   162	| 邮箱 | email | 文本 | 否 | 联系邮箱 | wanglaoshi@example.com |
   163	| 是否在职 | is_active | 布尔 | 是 | 是否在职（**v2新增**） | true |
   164	
   165	**字段说明：**
   166	- `employee_id`：辅导员工号，必须全校唯一，与统一身份认证、人事系统工号一致
   167	- `is_active`：标识是否在职，`false`时不能登录、不能审批，但历史记录可查询
   168	
   169	**CSV模板示例：**
   170	
   171	```csv
   172	employee_id,name,department,phone,email,is_active
   173	T2022001,王老师,计算机学院,13900139000,wanglaoshi@example.com,true
   174	T2022002,李老师,软件学院,13900139001,lililaoshi@example.com,true
   175	```
   176	
   177	**数据范围：**
   178	- 当前在职辅导员
   179	- 约50人
   180	
   181	**停用规则（v2新增）：**
   182	
   183	| 账号状态 | 登录 | 创建申请 | 审批 | 查看历史 | 接收通知 |
   184	|---------|------|---------|------|---------|---------|
   185	| `is_active=true` | ✅ | ✅ | ✅ | ✅ | ✅ |
   186	| `is_active=false` | ❌ | ❌ | ❌ | ✅（仅自己的） | ❌ |
   187	
   188	---
   189	
   190	### 2.4 班级-辅导员对应关系
   191	
   192	**用途：**
   193	- 学生提交申请时自动分配辅导员审批人
   194	- 支持辅导员变更和历史追溯
   195	
   196	**必需字段：**
   197	
   198	| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
   199	|---------------|---------------|----------|------|------|------|
   200	| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2022-01 |
   201	| 班级名称 | class_name | 文本 | 否 | 班级名称（用于展示） | 计算机科学与技术2022级1班 |
   202	| 辅导员工号 | counselor_employee_id | 文本 | 是 | 辅导员工号 | T2022001 |
   203	
   204	**可选字段（v2新增）：**
   205	
   206	| 字段名（中文） | 字段名（英文） | 数据类型 | 说明 | 示例 |
   207	|---------------|---------------|----------|------|------|
   208	| 生效日期 | effective_from | 日期 | 映射生效日期 | 2026-01-01 |
   209	| 失效日期 | effective_until | 日期 | 映射失效日期，NULL表示长期有效 | NULL |
   210	| 毕业批次ID | graduation_batch_id | 整数 | 关联毕业批次 | 1 |
   211	
   212	**字段说明：**
   213	- `class_id`：班级唯一标识，必须全校唯一，不能重复、变更或跨届复用
   214	- `counselor_employee_id`：必须在辅导员表中存在且 `is_active=true`
   215	- 首版只支持一班一主辅导员，同一 `class_id` 不能出现多次
   216	
   217	**CSV模板示例：**
   218	
   219	```csv
   220	class_id,class_name,counselor_employee_id

exec
/bin/bash -lc 'rtk nl -ba docs/discussions/codex-review-2026-05-30/46-next-steps-final-consensus.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# 下一步工作 - 最终共识
     2	
     3	**文档编号：** 46  
     4	**共识日期：** 2026-05-30  
     5	**参与方：** Claude Opus 4.7, Codex (GPT-5.5)  
     6	**讨论周期：** 41 → 42 → 43 → 44 → 45 → 46
     7	
     8	---
     9	
    10	## 一、共识结论
    11	
    12	**采用纵向切片/MVP优先方法，Week 0-1拆分执行。**
    13	
    14	经过两轮批判性讨论，达成以下核心共识：
    15	
    16	1. **Week 0（1-2工作日）：** 冻结v0.1最小可执行契约
    17	2. **Week 1（5工作日）：** 后端纵向切片（保留最小权限校验）
    18	3. **Week 2：** CSV导入v1
    19	4. **Week 3：** 核心流程补强 + v0.2契约
    20	5. **Week 4-6：** 微信小程序并行开发
    21	6. **Week 6-7：** 宿舍真实API或降级
    22	7. **Week 8-9：** UAT和完善
    23	8. **Week 10：** 验收演示（不新增功能）
    24	
    25	---
    26	
    27	## 二、核心决策
    28	
    29	### 决策1：数据契约v0.1现在冻结（1-2工作日）
    30	
    31	**范围：** 最小可执行契约（不是极简字段，也不是完整模型）
    32	
    33	**包含内容：**
    34	- OpenAPI/DTO草案
    35	- 状态枚举
    36	- 错误码
    37	- 样例请求/响应
    38	- Seed/fixture数据
    39	- Mock响应
    40	- Changelog机制
    41	
    42	**责任边界：**
    43	- 后端负责人owns契约包
    44	- 前端负责人reviews可消费性
    45	- 用户/业务方确认业务假设
    46	
    47	**时间限制：** 1-2工作日完成，超时冻结当前假设进入Week 1
    48	
    49	### 决策2：Week 1交付后端纵向切片
    50	
    51	**必须保留：**
    52	- 后端项目可运行
    53	- Seed/fixture落库
    54	- 薄认证（学号/工号+密码）
    55	- **最小角色校验**（学生/辅导员/学工部边界）
    56	- 申请提交API
    57	- 辅导员审批API
    58	- 学工部审批API
    59	- 状态查询API
    60	- Dorm Mock参与提交校验
    61	- 端到端自动化测试
    62	
    63	**推迟到Week 2+：**
    64	- 完整CSV导入
    65	- 附件上传/下载
    66	- 通知推送
    67	- 微信OAuth
    68	- 完整RBAC
    69	- 宿舍真实API
    70	- 复杂审批流
    71	
    72	**工作量：** 7-10人日（2-3人团队，5个工作日）
    73	
    74	### 决策3：前端Week 4并行启动
    75	
    76	**启动硬门槛：**
    77	1. 单端范围确认（只做微信小程序）
    78	2. OpenAPI/DTO达到v0.2（有changelog）
    79	3. 前端mock server可用
    80	4. 核心后端API可跑通
    81	5. 认证策略固定（演示期学号/工号密码）
    82	6. 状态枚举和错误码稳定
    83	7. 至少一条端到端后端测试通过
    84	8. API owner明确，破坏性变更当天通知
    85	
    86	**不应阻塞启动：**
    87	- 附件完整权限
    88	- 通知推送
    89	- 宿舍真实API
    90	- 微信OAuth真实接入
    91	- 完整CSV导入后台
    92	
    93	### 决策4：单端交付（微信小程序优先）
    94	
    95	**首版范围：**
    96	- 微信小程序（覆盖主要用户群）
    97	- 核心流程（申请、审批、状态查询）
    98	- Mock数据（seed + fixture）
    99	- 简化认证（学号+密码，无微信OAuth）
   100	- 简化附件（只支持图片上传）
   101	- 简化通知（邮件通知，无微信推送）
   102	
   103	**后续迭代：**
   104	- React Native（如有需求）
   105	- 微信OAuth
   106	- 完整附件支持
   107	- 微信模板消息
   108	
   109	---
   110	
   111	## 三、最终执行计划
   112	
   113	| 时间 | 目标 | 交付物 | 验收标准 |
   114	|------|------|--------|---------|
   115	| **Week 0** (1-2工作日) | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog | 前端可用mock跑通登录→提交→审批→查询流程 |
   116	| **Week 1** | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 | 自动化测试通过：学生登录→提交→辅导员审批→学工部审批→查询 |
   117	| **Week 2** | CSV导入v1 | Staging表、校验报告、upsert、软停用基础、导入审计基础 | 可导入10学生+2辅导员，生成校验报告，软停用未导入账号 |
   118	| **Week 3** | 核心流程补强 + v0.2契约 | 权限细化、异常流、API mock更新、前端启动检查 | v0.2契约冻结，前端mock可用，核心API稳定 |
   119	| **Week 4-6** | 微信小程序并行开发 | 登录、申请、审批、查询主流程 | 小程序可用mock跑通完整流程，逐步联调真实后端 |
   120	| **Week 6-7** | 宿舍真实API或降级方案 | 真实Provider、错误分类、缓存/降级、人工证明路径 | 真实API集成或降级方案可用 |
   121	| **Week 8-9** | UAT和完善 | 通知、附件最小可用、异常流修复、导入演练 | UAT通过，主要缺陷修复 |
   122	| **Week 10** | 验收演示 | 演示脚本、缺陷修复、文档 | 可演示版本交付，不新增功能 |
   123	
   124	---
   125	
   126	## 四、立即行动
   127	
   128	### 行动1：创建contract-v0.1.md
   129	
   130	**文件路径：** `docs/contracts/contract-v0.1.md`
   131	
   132	**责任人：** Claude（后端负责人）
   133	
   134	**时间限制：** 1-2工作日
   135	
   136	**验收标准：** 前端可用mock跑通登录→提交→审批→查询流程
   137	
   138	### 行动2：创建week-0-1-execution-plan.md
   139	
   140	**文件路径：** `docs/plans/week-0-1-execution-plan.md`
   141	
   142	**责任人：** Claude（项目负责人）
   143	
   144	**时间限制：** 与contract-v0.1.md同步完成
   145	
   146	**验收标准：** 按天列出责任人、交付物、降级条件和验收测试
   147	
   148	### 行动3：更新总实施计划
   149	
   150	**时机：** Week 0-1执行计划完成后
   151	
   152	**内容：** 基于Week 0-1执行计划更新10周总实施计划
   153	
   154	---
   155	
   156	## 五、关键修正点
   157	
   158	### 修正1：从瀑布式到纵向切片
   159	
   160	**原方案A：** 认证→申请→审批→附件→通知→前端→联调
   161	
   162	**修正后：** Week 1端到端最小流程 → Week 2-3扩展 → Week 4前端并行
   163	
   164	**原因：** 避免Week 8-10才发现集成问题
   165	
   166	### 修正2：从前端后置到并行开发
   167	
   168	**原方案A：** Week 8-9前端，Week 10联调
   169	
   170	**修正后：** Week 4前端启动，不等后端完全稳定
   171	
   172	**原因：** 降低前端集成风险，提前发现问题
   173	
   174	### 修正3：从双端到单端
   175	
   176	**原方案A：** React Native + 微信小程序同时开发
   177	
   178	**修正后：** 微信小程序优先，React Native后续迭代
   179	
   180	**原因：** 2-3人10周无法同时交付双端
   181	
   182	### 修正4：从Week 1数据契约到Week 0
   183	
   184	**原方案A：** Week 1做数据契约和接口设计
   185	
   186	**修正后：** Week 0（1-2工作日）冻结v0.1，Week 1用v0.1跑纵向切片
   187	
   188	**原因：** 避免Week 1前半定义契约，后半只剩2-3天开发
   189	
   190	### 修正5：保留最小权限校验
   191	
   192	**Claude错误建议：** Week 1"审批API无权限校验"
   193	
   194	**Codex修正：** 最小角色校验必须保留
   195	
   196	**原因：** 纵向切片的价值是验证角色、数据、状态机和审批链路能否串起来
   197	
   198	---
   199	
   200	## 六、风险缓解
   201	
   202	### 风险1：Week 0契约定义延期
   203	
   204	**缓解措施：** 1-2工作日timebox，超时冻结当前假设进入Week 1
   205	
   206	### 风险2：Week 1纵向切片未完成
   207	
   208	**降级条件：**
   209	- Day 3结束仍无申请提交API → 只保留"学生提交→辅导员审批→查询"
   210	- Day 4结束仍无两级审批 → 学工部审批推到Week 2开头
   211	
   212	### 风险3：前端Week 4启动条件不满足
   213	
   214	**应对策略：**
   215	- 如果只是字段补充、错误码补充，不推迟
   216	- 如果核心端点还没有可运行实现，前端做一周mock驱动开发，Week 5切真实环境
   217	- 如果v0.2契约仍没有确定状态枚举、角色和核心路径，先用1-2天补契约
   218	
   219	### 风险4：Week 10过载
   220	
   221	**缓解措施：** Week 10只做验收和演示，前面延期的任务砍掉或推迟到生产集成阶段
   222	
   223	---
   224	
   225	## 七、讨论总结
   226	
   227	### 讨论轮次
   228	
   229	**第一轮（文档41-42）：**
   230	- Claude提出方案A
   231	- Codex批判：瀑布式排期、前端后置、Week 10过载
   232	- Codex建议：纵向切片、前端并行、砍范围
   233	
   234	**第二轮（文档43-44）：**
   235	- Claude质疑：v0.1何时冻结、Week 1工作量、前端启动条件
   236	- Codex澄清：v0.1现在冻结、7-10人日现实、Week 4启动不要求后端完全稳定
   237	- Codex指出Claude方案问题：Week 0膨胀、v0.1过于字段化、Week 1砍权限校验
   238	
   239	**第三轮（文档45-46）：**
   240	- Claude完全接受Codex修正
   241	- 达成共识：Week 0-1拆分、v0.1最小可执行契约、保留最小权限校验、前端Week 4并行
   242	
   243	### 核心教训
   244	
   245	1. **纵向切片优于横向模块堆叠** - 早期验证端到端集成
   246	2. **前端并行优于前端后置** - 降低集成风险
   247	3. **单端优于双端** - 资源有限时聚焦核心
   248	4. **数据契约提前冻结** - 避免Week 1前半定义后半开发
   249	5. **最小权限校验不能砍** - 纵向切片的价值在于验证完整链路
   250	
   251	---
   252	
   253	## 八、后续讨论点（非阻塞）
   254	
   255	- CSV导入v1的详细设计（Week 2开始前）
   256	- 微信小程序技术栈选择（Week 3开始前）
   257	- 宿舍真实API集成方案（Week 5开始前）
   258	
   259	---
   260	
   261	**共识达成：** 2026-05-30  
   262	**状态：** 已批准，进入执行阶段  
   263	**下一步：** 创建contract-v0.1.md和week-0-1-execution-plan.md
   264	
   265	---
   266	
   267	**签署：**
   268	- Claude Opus 4.7 - 方案设计与实施
   269	- Codex (GPT-5.5) - 技术审查与验证

exec
/bin/bash -lc 'rtk nl -ba docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# API阻塞问题解决方案 - 最终共识
     2	
     3	**文档编号：** 40  
     4	**共识日期：** 2026-05-30  
     5	**参与方：** Claude Opus 4.7, Codex (GPT-5.5)  
     6	**审查周期：** 37 → 38 → 39 → 40
     7	
     8	---
     9	
    10	## 一、共识结论
    11	
    12	**方案名称：** Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配
    13	
    14	**核心原则：**
    15	1. 用户主数据（学生、辅导员、班级映射）通过CSV导入到本地数据库
    16	2. ImportSource接口用于数据导入，不是运行时查询
    17	3. 宿舍清退状态通过API实时查询（可缓存、可降级）
    18	4. 本地数据库是认证、权限、审批的唯一运行时依据
    19	
    20	**评分：** 9/10（Codex原评分7/10，修正后提升至9/10）
    21	
    22	---
    23	
    24	## 二、架构设计
    25	
    26	### 2.1 数据流架构
    27	
    28	```
    29	外部数据源 (CSV/API/Mock)
    30	    ↓
    31	ImportSource (数据导入源接口)
    32	    ↓
    33	ImportService (导入服务：校验、staging、upsert、软停用)
    34	    ↓
    35	本地数据库 (认证、权限、审批的唯一运行时依据)
    36	    ↑
    37	    │ (运行时查询)
    38	DormCheckoutProvider (宿舍清退实时查询)
    39	```
    40	
    41	### 2.2 核心接口设计
    42	
    43	```python
    44	# 1. 数据导入源接口（用于导入，非运行时查询）
    45	class IUserDataImportSource(ABC):
    46	    """用户数据导入源接口"""
    47	    @abstractmethod
    48	    def fetch_students(self) -> ImportResult[StudentDTO]:
    49	        """获取学生数据用于导入"""
    50	        pass
    51	    
    52	    @abstractmethod
    53	    def fetch_counselors(self) -> ImportResult[CounselorDTO]:
    54	        """获取辅导员数据用于导入"""
    55	        pass
    56	    
    57	    @abstractmethod
    58	    def fetch_class_mapping(self) -> ImportResult[ClassMappingDTO]:
    59	        """获取班级映射数据用于导入"""
    60	        pass
    61	
    62	# 2. 宿舍清退Provider（用于运行时查询）
    63	class IDormCheckoutProvider(ABC):
    64	    """宿舍清退状态提供者接口"""
    65	    @abstractmethod
    66	    def check_status(self, student_id: str) -> CheckoutResult:
    67	        """运行时查询宿舍清退状态"""
    68	        pass
    69	    
    70	    @abstractmethod
    71	    def health_check(self) -> HealthStatus:
    72	        """健康检查"""
    73	        pass
    74	
    75	# 3. 导入服务
    76	class UserDataImportService:
    77	    def __init__(self, source: IUserDataImportSource):
    78	        self.source = source
    79	    
    80	    def import_data(self):
    81	        # 1. 从source获取数据
    82	        result = self.source.fetch_students()
    83	        
    84	        # 2. 导入到staging表
    85	        self.load_to_staging(result.data)
    86	        
    87	        # 3. 校验（必填字段、唯一性、班级覆盖率）
    88	        errors = self.validate(result.data)
    89	        
    90	        # 4. Upsert到users表
    91	        self.upsert_to_users()
    92	        
    93	        # 5. 软停用未导入的账号
    94	        self.soft_delete_missing()
    95	        
    96	        # 6. 生成审计日志
    97	        self.create_audit_log(result, errors)
    98	```
    99	
   100	### 2.3 DTO设计
   101	
   102	```python
   103	@dataclass
   104	class StudentDTO:
   105	    student_id: str
   106	    name: str
   107	    department: str
   108	    major: str
   109	    class_id: str
   110	    grade: int
   111	    graduation_year: int
   112	    is_graduating: bool
   113	    phone: Optional[str] = None
   114	    email: Optional[str] = None
   115	
   116	@dataclass
   117	class ImportResult[T]:
   118	    data: List[T]
   119	    total_count: int
   120	    source_updated_at: datetime
   121	    metadata: Dict[str, Any]
   122	
   123	@dataclass
   124	class CheckoutResult:
   125	    student_id: str
   126	    status: CheckoutStatus  # completed/pending/not_started/unknown
   127	    checkout_date: Optional[datetime]
   128	    error: Optional[str]
   129	```
   130	
   131	---
   132	
   133	## 三、配置管理
   134	
   135	### 3.1 细粒度配置
   136	
   137	```python
   138	# settings/base.py
   139	USER_DATA_SOURCE = env.str('USER_DATA_SOURCE', default='seed')  # seed|csv|api
   140	DORM_CHECKOUT_SOURCE = env.str('DORM_CHECKOUT_SOURCE', default='mock')  # mock|api|csv
   141	WECHAT_PROVIDER = env.str('WECHAT_PROVIDER', default='mock')  # mock|real
   142	
   143	# settings/dev.py
   144	USER_DATA_SOURCE = 'seed'  # 开发环境使用种子数据
   145	DORM_CHECKOUT_SOURCE = 'mock'
   146	WECHAT_PROVIDER = 'mock'
   147	
   148	# settings/prod.py
   149	USER_DATA_SOURCE = 'csv'  # 生产环境使用CSV导入
   150	DORM_CHECKOUT_SOURCE = 'api'  # 宿舍清退使用API
   151	WECHAT_PROVIDER = 'real'
   152	```
   153	
   154	### 3.2 安全检查
   155	
   156	```python
   157	from django.core.checks import Error, register
   158	
   159	@register()
   160	def check_production_config(app_configs, **kwargs):
   161	    errors = []
   162	    if settings.ENVIRONMENT == 'production':
   163	        if 'mock' in [settings.USER_DATA_SOURCE, 
   164	                      settings.DORM_CHECKOUT_SOURCE, 
   165	                      settings.WECHAT_PROVIDER]:
   166	            errors.append(
   167	                Error(
   168	                    'Production environment cannot use mock providers',
   169	                    hint='Set USER_DATA_SOURCE=csv, DORM_CHECKOUT_SOURCE=api, WECHAT_PROVIDER=real',
   170	                    id='config.E001',
   171	                )
   172	            )
   173	    return errors
   174	```
   175	
   176	---
   177	
   178	## 四、实施计划
   179	
   180	### 4.1 修正后的工期
   181	
   182	| 周次 | 任务 | 交付物 |
   183	|------|------|--------|
   184	| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
   185	| Week 2-3 | CSV导入功能、staging表、upsert逻辑、审计日志 | CSV导入模块、导入校验报告 |
   186	| Week 3-6 | 申请、审批、附件、通知模块 | 核心业务功能 |
   187	| Week 6-7 | 宿舍清退Provider、降级流程、缓存、错误分类 | 宿舍清退集成模块 |
   188	| Week 8-9 | 前端开发 | React Native、微信小程序 |
   189	| Week 10 | 联调、演示、验收清单 | 可演示版本（Mock数据） |
   190	
   191	**API到位后：**
   192	- 宿舍清退API集成：1周
   193	- 用户主数据API替换CSV（如需）：另计2-4周
   194	
   195	**总工期：** 10周演示版 + 1-2周生产集成缓冲
   196	
   197	### 4.2 关键里程碑
   198	
   199	1. **Week 1结束：** 数据契约冻结，接口定义完成
   200	2. **Week 3结束：** CSV导入功能可用，种子数据就绪
   201	3. **Week 6结束：** 核心业务逻辑完成
   202	4. **Week 7结束：** 宿舍清退API对接完成
   203	5. **Week 10结束：** 可演示版本交付
   204	
   205	---
   206	
   207	## 五、Mock数据设计
   208	
   209	### 5.1 边界样本
   210	
   211	```python
   212	def generate_comprehensive_mock_data():
   213	    students = [
   214	        # 正常学生
   215	        Student(student_id="2020001", name="张三", class_id="CS2020-01", is_graduating=True),
   216	        
   217	        # 边界情况
   218	        Student(student_id="2020002", name="李四", class_id="INVALID", is_graduating=True),  # 无班级映射
   219	        Student(student_id="2020003", name="王五", class_id="CS2020-99", is_graduating=True),  # 辅导员停用
   220	        Student(student_id="2020004", name="赵六", class_id="CS2020-01", is_graduating=False),  # 非毕业生
   221	        Student(student_id="2020005", name="钱七", class_id="CS2020-01", is_graduating=True, graduation_year=2027),  # 延期毕业
   222	    ]
   223	    
   224	    counselors = [
   225	        Counselor(employee_id="T001", name="李老师", is_active=True),
   226	        Counselor(employee_id="T002", name="王老师", is_active=False),  # 停用辅导员
   227	    ]
   228	    
   229	    dorm_statuses = {
   230	        "2020001": CheckoutStatus(status="completed", date="2024-06-15"),
   231	        "2020002": CheckoutStatus(status="pending", date=None),
   232	        "2020003": CheckoutStatus(status="not_started", date=None),
   233	        "2020004": CheckoutStatus(status="unknown", date=None),  # API失败
   234	    }
   235	    
   236	    return students, counselors, dorm_statuses
   237	```
   238	
   239	### 5.2 数据规模
   240	
   241	- **学生：** 100人（覆盖5个院系、10个班级）
   242	- **辅导员：** 10人（包含停用账号）
   243	- **班级映射：** 10个班级
   244	- **宿舍清退状态：** 覆盖所有枚举值（completed/pending/not_started/unknown）
   245	
   246	---
   247	
   248	## 六、缓存策略
   249	
   250	### 6.1 用户信息缓存
   251	
   252	- **TTL：** 30分钟
   253	- **缓存键：** `user:{user_id}`
   254	- **更新策略：** 导入后清空缓存
   255	
   256	### 6.2 宿舍清退状态缓存
   257	
   258	- **completed：** 10-30分钟
   259	- **pending/not_started：** 1-5分钟
   260	- **unknown/error：** 30-60秒
   261	- **提交申请前：** 必须重新校验
   262	
   263	---
   264	
   265	## 七、错误处理
   266	
   267	### 7.1 错误分类
   268	
   269	- 认证失败（401）
   270	- 字段缺失（400）
   271	- 学生不存在（404）
   272	- 限流（429）
   273	- 超时（504）
   274	- 服务不可用（503）
   275	- 数据不一致（422）
   276	
   277	### 7.2 降级策略
   278	
   279	```python
   280	class DormCheckoutProvider:
   281	    def check_status(self, student_id: str) -> CheckoutResult:
   282	        try:
   283	            # 尝试API查询
   284	            return self._query_api(student_id)
   285	        except APIUnavailableError:
   286	            # 降级到缓存
   287	            cached = self._get_cached_status(student_id)
   288	            if cached:
   289	                return cached
   290	            # 降级到人工证明
   291	            return CheckoutResult(
   292	                student_id=student_id,
   293	                status=CheckoutStatus.MANUAL_PROOF_REQUIRED,
   294	                error="API不可用，需提供人工证明"
   295	            )
   296	```
   297	
   298	---
   299	
   300	## 八、关键变更
   301	
   302	### 8.1 与原方案的差异
   303	
   304	| 原方案 | 修正后方案 | 原因 |
   305	|--------|-----------|------|
   306	| RealUserDataProvider运行时查询 | CSV导入到本地数据库 | 用户主数据是基础数据，不应依赖外部API |
   307	| USE_MOCK_DATA单一开关 | 细粒度配置（USER_DATA_SOURCE/DORM_CHECKOUT_SOURCE/WECHAT_PROVIDER） | 支持混合模式，生产环境安全 |
   308	| 10周 + 3天 | 10周演示版 + 1-2周生产集成 | 更现实的工期评估 |
   309	| Week 7做接口抽象 | Week 1做数据契约和接口 | 避免后续返工 |
   310	| Provider用于运行时查询 | ImportSource用于数据导入 | 明确职责边界 |
   311	
   312	### 8.2 核心教训
   313	
   314	1. **不要偏离已达成的共识** - 原方案错误地将用户主数据API化，偏离了CSV导入的共识
   315	2. **用户主数据应落入本地数据库** - 不应依赖外部API
   316	3. **Provider抽象层的用途是数据导入** - 不是运行时查询
   317	4. **工期评估要现实** - 考虑缺失信息的影响
   318	5. **配置要细粒度** - 支持混合模式
   319	
   320	---
   321	
   322	## 九、验收标准
   323	
   324	### 9.1 Week 10交付物
   325	
   326	- [ ] 可演示版本（使用Mock/Seed数据）
   327	- [ ] 数据契约文档
   328	- [ ] CSV导入功能和校验逻辑
   329	- [ ] 宿舍清退API适配器（Mock实现）
   330	- [ ] 降级流程
   331	- [ ] 契约测试
   332	- [ ] 上线验收清单
   333	
   334	### 9.2 生产就绪标准
   335	
   336	- [ ] 真实API集成完成
   337	- [ ] 性能测试通过（P95 < 500ms）
   338	- [ ] 错误处理覆盖所有场景
   339	- [ ] 监控和告警配置完成
   340	- [ ] 数据导入审计日志完整
   341	- [ ] 降级流程验证通过
   342	
   343	---
   344	
   345	## 十、风险管理
   346	
   347	### 10.1 已识别风险
   348	
   349	| 风险 | 等级 | 缓解措施 |
   350	|------|------|---------|
   351	| 真实API字段与Mock不一致 | P1 | Week 1冻结数据契约，预留扩展字段 |
   352	| 真实API性能问题 | P1 | 缓存和重试机制 |
   353	| 真实API数据结构差异大 | P2 | DTO适配层，预留2-3天调整时间 |
   354	| API认证复杂度超预期 | P2 | 预留1-2天调试时间 |
   355	
   356	### 10.2 应急预案
   357	
   358	- **API延期：** 首版坚持CSV导入，不等待API
   359	- **API不可用：** 降级到人工证明流程
   360	- **数据质量问题：** 导入校验报告，人工审核
   361	
   362	---
   363	
   364	## 十一、参考文档
   365	
   366	- **审查请求：** [37-api-blocking-solution-review-request.md](./37-api-blocking-solution-review-request.md)
   367	- **Codex审查：** [38-codex-api-blocking-review.md](./38-codex-api-blocking-review.md)
   368	- **Claude响应：** [39-claude-response-to-codex.md](./39-claude-response-to-codex.md)
   369	- **系统设计：** [../../design/2026-05-27-system-design.md](../../design/2026-05-27-system-design.md)
   370	- **数据对接：** [../../数据对接说明文档.md](../../数据对接说明文档.md)
   371	- **共识v2：** [../codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md](../codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md)
   372	
   373	---
   374	
   375	## 十二、下一步行动
   376	
   377	1. **立即执行：** 更新实施计划文档
   378	2. **Week 1启动：** 数据契约和接口设计
   379	3. **Week 2-3：** CSV导入功能开发
   380	4. **持续跟进：** 外部API信息获取进度
   381	
   382	---
   383	
   384	**共识达成：** 2026-05-30  
   385	**状态：** 已批准，可执行  
   386	**有效期：** 至项目首版交付
   387	
   388	---
   389	
   390	**签署：**
   391	- Claude Opus 4.7 - 方案设计与实施
   392	- Codex (GPT-5.5) - 技术审查与验证

exec
/bin/bash -lc "rtk nl -ba docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md | sed -n '220,360p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   220	class_id,class_name,counselor_employee_id
   221	CS2022-01,计算机科学与技术2022级1班,T2022001
   222	SE2022-01,软件工程2022级1班,T2022002
   223	```
   224	
   225	**校验要求：**
   226	- 学生表中的 `class_id` 必须在班级映射表中存在
   227	- 班级映射表中的 `counselor_employee_id` 必须在辅导员表中存在
   228	- 导入后输出校验报告：未匹配班级、未匹配辅导员、重复映射、无审批人的学生数
   229	
   230	**历史一致性规则（v2新增）：**
   231	- 已提交申请的 `counselor_id` 不自动改写，保持历史一致性
   232	- 新提交申请使用新映射
   233	- 如需改派，由管理员显式操作并记录审计日志
   234	
   235	---
   236	
   237	### 2.5 学工部管理员信息
   238	
   239	**用途：**
   240	- 创建管理员账号（终审权限）
   241	- 系统配置和管理
   242	
   243	**必需字段：**
   244	
   245	| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
   246	|---------------|---------------|----------|------|------|------|
   247	| 工号 | employee_id | 文本 | 是 | 管理员唯一标识 | A2022001 |
   248	| 姓名 | name | 文本 | 是 | 管理员姓名 | 赵主任 |
   249	| 部门 | department | 文本 | 是 | 所属部门 | 学工部 |
   250	| 手机号 | phone | 文本 | 否 | 联系电话 | 13700137000 |
   251	| 邮箱 | email | 文本 | 否 | 联系邮箱 | zhaozr@example.com |
   252	
   253	**数据范围：**
   254	- 约5人
   255	- 首版采用手动创建，不参与批量导入
   256	
   257	**默认终审人配置（v2新增）：**
   258	- 系统配置表（`system_configs`）存储默认终审人列表
   259	- 配置项：`default_admin_ids`（如 `3,5,7`）
   260	- 分配模式：`admin_assignment_mode`（fixed/round_robin/load_balance）
   261	- 首版采用固定分配（fixed），使用第一个可用管理员
   262	
   263	---
   264	
   265	## 三、数据对接方式详细说明
   266	
   267	### 3.1 CSV/Excel导入（首版推荐）
   268	
   269	**适用场景：**
   270	- 学生基本信息
   271	- 辅导员基本信息
   272	- 班级-辅导员对应关系
   273	
   274	**技术要求：**
   275	
   276	**文件格式：**
   277	- 编码：UTF-8（避免中文乱码）
   278	- 格式：CSV或Excel（.xlsx）
   279	- 大小限制：单文件不超过10MB
   280	- 行数限制：单文件不超过10000行
   281	
   282	**导入策略（v2修订）：**
   283	
   284	采用**staging表 + upsert + 软停用**模式：
   285	
   286	1. CSV导入到临时staging表（按类型拆分）
   287	2. 存在则更新，不存在则插入（upsert）
   288	3. 本次未导入的账号标记为 `is_active=false`
   289	4. 下次导入重新出现时自动激活
   290	
   291	**Staging表设计（v2新增）：**
   292	
   293	```sql
   294	-- 学生导入staging表
   295	CREATE TABLE students_staging (
   296	    student_id VARCHAR(50) PRIMARY KEY,
   297	    name VARCHAR(100) NOT NULL,
   298	    department VARCHAR(100),
   299	    major VARCHAR(100),
   300	    class_id VARCHAR(50),
   301	    class_name VARCHAR(100),
   302	    grade INT,
   303	    graduation_year INT,
   304	    is_graduating BOOLEAN,
   305	    phone VARCHAR(20),
   306	    email VARCHAR(100)
   307	);
   308	
   309	-- 辅导员导入staging表
   310	CREATE TABLE counselors_staging (
   311	    employee_id VARCHAR(50) PRIMARY KEY,
   312	    name VARCHAR(100) NOT NULL,
   313	    department VARCHAR(100),
   314	    phone VARCHAR(20),
   315	    email VARCHAR(100)
   316	);
   317	
   318	-- 班级映射导入staging表
   319	CREATE TABLE class_mapping_staging (
   320	    class_id VARCHAR(50) PRIMARY KEY,
   321	    counselor_employee_id VARCHAR(50) NOT NULL
   322	);
   323	```
   324	
   325	**导入流程：**
   326	
   327	```sql
   328	-- 1. 清空staging表
   329	TRUNCATE students_staging;
   330	
   331	-- 2. 导入CSV到staging表
   332	LOAD DATA INFILE 'students.csv' INTO TABLE students_staging;
   333	
   334	-- 3. Upsert到users表
   335	INSERT INTO users (student_id, name, department, class_id, role, is_active, password_setup_required, ...)
   336	SELECT student_id, name, department, class_id, 'student', true, true, ...
   337	FROM students_staging
   338	ON DUPLICATE KEY UPDATE
   339	    name = VALUES(name),
   340	    department = VALUES(department),
   341	    class_id = VALUES(class_id),
   342	    is_active = true,
   343	    updated_at = NOW();
   344	
   345	-- 4. 软停用：本次未导入的学生（使用NOT EXISTS避免NULL问题）
   346	UPDATE users u
   347	SET is_active = false, updated_at = NOW()
   348	WHERE u.role = 'student'
   349	  AND NOT EXISTS (
   350	      SELECT 1 FROM students_staging s
   351	      WHERE s.student_id = u.student_id
   352	  );
   353	```
   354	
   355	**校验要求：**
   356	- 必填字段非空校验
   357	- 学号/工号唯一性校验
   358	- 班级ID存在性校验
   359	- 辅导员工号存在性校验
   360	- 重复数据校验

codex
从共识文档看，Week 0 的目标是“可执行契约”，不是完整模型；同时已有共识要求用户主数据最终落本地库、宿舍清退运行时查询、Week 1 保留最小权限校验。这会影响我对遗漏和过度设计的判断。
exec
/bin/bash -lc "rtk find . -maxdepth 3 -name 'manage.py' -o -name 'pyproject.toml' -o -name 'requirements*.txt' -o -name 'package.json'" in /home/caohui/projects/graduation-leave-system
 exited 1 in 0ms:
rtk: rtk find does not support compound predicates or actions (e.g. -not, -exec). Use `find` directly.

exec
/bin/bash -lc 'rtk rg --files frontend | head -120' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
exec
/bin/bash -lc 'rtk rg --files backend | head -120' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/requirements/base.txt
backend/requirements/dev.txt
backend/requirements/prod.txt

exec
/bin/bash -lc "rtk proxy find . -maxdepth 3 \\( -name manage.py -o -name pyproject.toml -o -name 'requirements*.txt' -o -name package.json \\)" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
exec
/bin/bash -lc 'rtk nl -ba backend/requirements/base.txt' in /home/caohui/projects/graduation-leave-system
 succeeded in 1ms:
     1	# Django Core
     2	Django==4.2.13
     3	djangorestframework==3.14.0
     4	djangorestframework-simplejwt==5.3.1
     5	django-cors-headers==4.3.1
     6	django-filter==23.5
     7	
     8	# Database
     9	psycopg2-binary==2.9.9
    10	
    11	# State Machine
    12	django-fsm==2.8.1
    13	
    14	# Celery
    15	celery==5.3.6
    16	redis==5.0.3
    17	
    18	# WeChat
    19	wechatpy==1.8.18
    20	
    21	# Retry
    22	tenacity==8.2.3
    23	
    24	# Password
    25	bcrypt==4.1.2
    26	
    27	# Environment
    28	python-decouple==3.8
    29	
    30	# Utils
    31	python-dateutil==2.9.0
    32	pytz==2024.1
    33	
    34	# File Processing
    35	python-magic==0.4.27
    36	
    37	# Work Day Calculation
    38	chinese-calendar==1.9.0
    39	
    40	# HTTP Client
    41	requests==2.31.0
    42	
    43	# Encryption
    44	cryptography==42.0.5
    45	
    46	# Cache
    47	django-redis==5.4.0

exec
/bin/bash -lc 'rtk nl -ba backend/requirements/prod.txt' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk nl -ba backend/requirements/dev.txt' in /home/caohui/projects/graduation-leave-system
 succeeded in 101ms:
 succeeded in 294ms:
exec
/bin/bash -lc 'rtk head -20 docs/templates/班级辅导员对应关系导入模板.csv' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk head -20 docs/templates/辅导员基本信息导入模板.csv' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk head -20 docs/templates/学生基本信息导入模板.csv' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk head -20 docs/templates/宿舍清退数据模板.csv' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
学号,姓名,班级,宿舍楼栋,宿舍房间号,床号,是否已清退,清退日期,清退状态,备注
2020010101,张三,计算机2020级1班,1号楼,101,1,是,2026-05-20,已完成,已完成清退，物品已搬离
2020010102,李四,计算机2020级1班,1号楼,102,2,否,,未开始,尚未办理清退手续
2020010103,王五,计算机2020级2班,2号楼,201,1,是,2026-05-21,已完成,已完成清退

 succeeded in 109ms:
 succeeded in 124ms:
 succeeded in 136ms:
class_id,class_name,counselor_employee_id
CS2022-01,计算机科学与技术2022级1班,T2022001
SE2022-01,软件工程2022级1班,T2022002

codex
**审查结论：暂不建议立即开始 Week 1 实施。**

两份文档方向是对的，已经接近“可执行契约”，但还差几个会直接影响 Week 1 纵向切片落地的关键点。建议先用半天把契约和计划修正到可执行状态，再进入 Week 1。

**主要问题**

1. **UserDTO 与样例数据不一致，会卡住建模和 seed。**  
   [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:16) 把 `is_graduating`、`graduation_year` 定义为所有用户必填，但辅导员/学工部样例没有这些字段 [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:338)。应改成学生专属可选字段，或拆成 `StudentDTO / StaffDTO`。

2. **缺少 Week 1 最关键的状态机契约。**  
   API 示例有提交、审批、驳回，但契约没有明确“当前状态 + 当前审批节点 + 角色 + 决策 → 下一个状态/审批记录”的表。Week 1 计划里才写了部分规则 [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:79)，应前移到契约，否则后端测试和前端 mock 会各自理解。

3. **Dorm Mock 的失败/unknown 策略不明确。**  
   契约定义了 `UNKNOWN` [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:122)，也定义了 `PROVIDER_UNAVAILABLE` [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:144)，但提交申请时遇到 `unknown` 是阻断、允许人工证明，还是 503，没有写死。更关键的是 mock 默认对未知学生返回 `completed` [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:417)，会掩盖失败路径。

4. **Seed/fixture 不满足计划自己的验收口径。**  
   计划要求 `10学生 + 2辅导员 + 1学工部 + 边界样本` [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:31)，但契约只给了 3 个正常学生和若干零散边界样本 [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:329)。还缺默认密码/密码策略，薄认证无法稳定跑 seed 登录。

5. **API 端点数量和验收表述不一致。**  
   契约实际有登录、创建、详情、审批通过、审批驳回、列表 6 类端点 [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:168)，计划有时说 5 个 API [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:29)，Week 1 又说 4 个端点 [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:97)。这会影响任务拆分和验收。

6. **执行计划的降级条件不够好。**  
   “Day 3 申请提交未完成 → 只做查询 API” [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:108) 会破坏纵向切片价值。更合理的降级是保留“提交→辅导员审批→查询”最短闭环，砍列表、学工部审批、复杂错误、完整 seed 等外围内容。  
   “周末加班” [week-0-1-execution-plan.md](/home/caohui/projects/graduation-leave-system/docs/plans/week-0-1-execution-plan.md:135) 也不是工程降级条件，应改成明确的范围裁剪或延期规则。

**是否满足最小可执行契约？**

部分满足。DTO、枚举、错误码、样例、mock 都有了，范围也基本克制，没有把附件、通知、微信 OAuth 拉进 v0.1，这是对的 [contract-v0.1.md](/home/caohui/projects/graduation-leave-system/docs/contracts/contract-v0.1.md:480)。

但“可执行”还不够：缺状态机表、角色权限矩阵、seed 登录凭据、Dorm 异常策略、端点验收口径统一。这些不是锦上添花，是 Week 1 开发会马上碰到的决策。

**是否足以支撑 Week 1？**

还不够。现在可以支撑讨论和原型，但不够支撑 5 天内稳定交付后端纵向切片。若直接开工，最可能在模型字段、审批流转、Dorm 异常、测试数据上返工。

**下一步**

建议不要大改设计，只做一次小补丁：

1. 修正 `UserDTO` 字段可选性或拆分用户 DTO。
2. 补一张状态流转/权限矩阵。
3. 明确 Dorm `pending/not_started/unknown/provider_unavailable` 的提交行为。
4. 补齐 10 个学生、2 个辅导员、1 个学工部、默认密码、当前审批人 fixture。
5. 统一 API 数量和 Week 1 验收口径。
6. 把降级策略改成“保留最短纵向闭环，裁剪外围功能”。

这些完成后，可以立即进入 Week 1 实施；不需要再做更大的架构准备。
tokens used
55,493

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
