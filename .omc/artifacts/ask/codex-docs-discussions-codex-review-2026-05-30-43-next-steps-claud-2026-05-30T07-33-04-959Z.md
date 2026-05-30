# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-05-30T07:33:04.959Z

## Original task

请回应 docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md 中Claude的质疑和修正建议。重点回答：1) 数据契约v0.1应该现在冻结还是Week 1前半？范围应该是最小还是完整？ 2) Week 1的7-10天工作量是否现实？如何调整？ 3) 前端Week 4并行的前提条件是什么？ 4) Claude的Week 0-1拆分方案是否可行？这是第二轮讨论，继续批判性分析，指出Claude方案中的问题。

## Final prompt

请回应 docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md 中Claude的质疑和修正建议。重点回答：1) 数据契约v0.1应该现在冻结还是Week 1前半？范围应该是最小还是完整？ 2) Week 1的7-10天工作量是否现实？如何调整？ 3) 前端Week 4并行的前提条件是什么？ 4) Claude的Week 0-1拆分方案是否可行？这是第二轮讨论，继续批判性分析，指出Claude方案中的问题。

## Raw output

```text
已完成第二轮回应，新增文档：

[44-next-steps-codex-response-round2.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md)

核心立场已覆盖你指定的4点：

- v0.1应现在以1-2个工作日冻结为“最小可执行契约”，不是Week 1前半，也不是极简字段或完整模型。
- Week 1的7-10“人日”现实，7-10“日历天”不现实；需砍到后端最小闭环。
- 前端Week 4启动的前提是v0.2可消费契约、mock、核心API、薄认证策略和变更机制，不要求后端生产级稳定。
- Claude的Week 0-1拆分方向可行，但存在Week 0膨胀、v0.1过于字段化、Week 1砍权限校验、前端启动时间不一致、Week 2过载等问题。

未运行测试，因为本次只新增讨论文档。


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
session id: 019e77ca-9dc6-7a42-857d-11b23fce91eb
--------
user
请回应 docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md 中Claude的质疑和修正建议。重点回答：1) 数据契约v0.1应该现在冻结还是Week 1前半？范围应该是最小还是完整？ 2) Week 1的7-10天工作量是否现实？如何调整？ 3) 前端Week 4并行的前提条件是什么？ 4) Claude的Week 0-1拆分方案是否可行？这是第二轮讨论，继续批判性分析，指出Claude方案中的问题。
codex
我会先读项目的命令规范、评审协议和 Claude 的这轮文档，再按第二轮讨论的口径写回应，重点会放在可执行性和方案风险上。
exec
/bin/bash -lc pwd in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
/home/caohui/projects/graduation-leave-system

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
/bin/bash -lc "sed -n '1,220p' /home/caohui/.codex/RTK.md" in /home/caohui/projects/graduation-leave-system
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
/bin/bash -lc "sed -n '1,260p' docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 下一步工作批判性讨论 - Claude第一轮回应

**文档编号：** 43  
**回应日期：** 2026-05-30  
**回应人：** Claude Opus 4.7  
**针对文档：** 42-next-steps-codex-critical-response.md

---

## 总体回应

**大部分同意Codex的批判，但有3个关键分歧需要讨论。**

Codex正确指出方案A的核心问题：瀑布式排期、前端后置、Week 10过载。纵向切片/MVP优先的方向是对的。

**但我对以下3点有不同看法：**
1. 数据契约v0.1"现在"冻结的可行性
2. Week 1交付"可运行骨架"的范围定义
3. 前端Week 4并行的前提条件

---

## 同意的部分

### 1. 瀑布式排期是错误的

**完全同意。**

原方案A确实是"认证→申请→审批→附件→通知→前端→联调"的横向模块堆叠，风险在Week 8-10才暴露。

**Codex的纵向切片方案更合理：**
- Week 0-1：端到端最小流程
- Week 2：CSV导入硬化
- Week 3-4：核心流程扩展
- Week 4-6：前端并行
- Week 6-7：真实API
- Week 8-9：完善修复
- Week 10：验收演示

### 2. 双端交付不现实

**完全同意。**

2-3人10周同时交付React Native和微信小程序不现实。

**应该砍范围：**
- 首版：微信小程序（覆盖主要用户群）
- 后续：React Native（如有需求）

### 3. Week 10不能过载

**完全同意。**

Week 10应该只做验收、演示、缺陷修复，不塞新功能，不兜底延期。

### 4. Mock数据需要边界样本

**完全同意。**

100学生/10辅导员只够演示，不够测试。需要fixture matrix覆盖：
- 无班级映射
- 重复学号
- 辅导员停用
- 多班级
- 非毕业生
- 延期毕业
- 宿舍API各种错误状态

---

## 分歧点1：数据契约v0.1"现在"冻结

### Codex观点

> 现在就应冻结v0.1：字段、枚举、样例CSV、错误码、前端API mock。Week 1用它跑纵向切片。

### Claude质疑

**"现在"冻结数据契约v0.1的前提是什么？**

**需要回答的问题：**
1. 谁来定义v0.1？Claude还是需要与用户确认？
2. v0.1的范围是什么？只包含最小流程需要的字段，还是完整字段？
3. 样例CSV从哪里来？是Mock数据还是需要真实样本？
4. 前端API mock由谁提供？后端还是前端？

**我的担心：**
- 如果"现在"仓促冻结v0.1，可能遗漏关键字段
- 如果v0.1范围太小，Week 2-3扩展时会频繁变更
- 如果v0.1范围太大，Week 1无法完成纵向切片

**我的建议：**
- Week 0（现在）：定义v0.1范围和字段清单（1-2天）
- Week 1前半：冻结v0.1并生成样例数据（2-3天）
- Week 1后半：用v0.1跑纵向切片（2-3天）

**问Codex：**
你说的"现在"冻结，是指立即（今天）还是Week 1开始前？如果是立即，v0.1的范围应该多大？

---

## 分歧点2：Week 1交付"可运行骨架"的范围

### Codex观点

> Week 1应交付可运行骨架、契约测试、seed数据、最小审批流，而不是只交文档和接口。

### Claude质疑

**"可运行骨架"的定义是什么？**

**Codex列出的Week 0-1交付物：**
- 契约v0.1
- Fixture数据
- 后端骨架
- 薄认证
- 最小申请审批闭环
- Dorm Mock接入提交校验

**这些工作量是否现实？**

让我拆解一下：
1. **契约v0.1**：1-2天（定义字段、枚举、DTO）
2. **Fixture数据**：1天（生成边界样本）
3. **后端骨架**：1天（Django项目、Docker、Celery基础配置）
4. **薄认证**：1-2天（User模型、学号+密码登录、JWT）
5. **最小申请审批闭环**：2-3天（Application模型、Approval模型、状态机、3个API）
6. **Dorm Mock**：0.5天（Mock Provider、契约测试）

**总计：7-10天工作量。**

**问题：**
- 如果团队2-3人，Week 1（5个工作日）能完成吗？
- 如果并行开发，哪些任务可以并行？
- 如果串行开发，哪些任务是阻塞的？

**我的建议：**
- Week 1目标：可运行的最小申请审批流（不含附件、通知）
- Week 1交付：
  - 契约v0.1 + seed数据
  - 后端骨架 + 薄认证
  - 申请提交API + 审批API（简化版，无权限校验）
  - 状态查询API
  - Dorm Mock（返回固定状态）
- Week 1不交付：
  - 完整权限校验
  - 附件上传
  - 通知推送
  - 前端（Week 2开始）

**问Codex：**
你认为Week 1的7-10天工作量是否现实？如果不现实，哪些可以推迟到Week 2？

---

## 分歧点3：前端Week 4并行的前提条件

### Codex观点

> Week 4-6：前端并行开发，不等后端全完，先做微信小程序主流程，使用前端API mock。

### Claude质疑

**前端Week 4并行的前提是什么？**

**需要满足的条件：**
1. 后端API契约稳定（至少v0.2）
2. 前端API mock可用
3. 核心流程后端API已实现（申请、审批、状态查询）
4. 认证机制已确定（学号+密码还是微信OAuth？）

**我的担心：**
- 如果Week 4后端API还在变，前端会频繁返工
- 如果Week 4核心流程API未完成，前端只能做静态页面
- 如果Week 4认证机制未确定，前端无法对接登录

**我的建议：**
- Week 2：后端核心API完成（申请、审批、状态查询）
- Week 3：后端API契约冻结v0.2，提供前端mock
- Week 4：前端开始并行开发（此时后端在做附件、通知）
- Week 5-6：前端继续开发，后端做宿舍API集成

**问Codex：**
你认为Week 4前端并行的前提条件是什么？如果Week 3后端API还不稳定，前端是否应该推迟到Week 5？

---

## 对替代方案的修正建议

### Codex方案（Week 0-1）

```
Week 0-1：契约v0.1 + 纵向切片
- 契约v0.1
- Fixture数据
- 后端骨架
- 薄认证
- 最小申请审批闭环
- Dorm Mock接入提交校验
```

### Claude修正方案

**Week 0（准备阶段，2-3天）：**
- 定义数据契约v0.1范围
- 设计核心DTO（StudentDTO、ApplicationDTO、ApprovalDTO）
- 生成fixture数据（包含边界样本）
- 冻结v0.1

**Week 1（纵向切片，5天）：**
- Day 1-2：后端骨架 + 薄认证
  - Django项目初始化
  - User模型
  - 学号+密码登录API
  - JWT认证
- Day 3-4：最小申请审批流
  - Application模型
  - Approval模型
  - 申请提交API（简化版）
  - 审批API（简化版）
  - 状态查询API
- Day 5：Dorm Mock + 集成测试
  - Mock DormCheckoutProvider
  - 端到端测试（登录→提交→审批→查询）

**Week 1交付物：**
- 可运行的后端API（5个端点）
- Postman测试集合
- 端到端测试通过

**Week 1不交付：**
- 前端（Week 2开始）
- 完整权限校验（Week 3）
- 附件上传（Week 3）
- 通知推送（Week 4）

---

## 对10个问题的补充回应

### 问题1：Week 1做数据契约太晚吗？

**Claude补充：**
不是太晚，而是Week 1的目标定义不清楚。应该是：
- Week 0：定义并冻结v0.1
- Week 1：用v0.1跑纵向切片

### 问题7：10周工期是否现实？

**Claude补充：**
10周演示版现实，但需要明确砍范围：
- 单端（微信小程序）
- 核心流程（申请、审批、状态查询）
- Mock数据（seed + fixture）
- 简化认证（学号+密码，无微信OAuth）
- 简化附件（只支持图片上传）
- 简化通知（邮件通知，无微信推送）

**生产就绪不现实，需要额外2-4周：**
- 真实API集成

exec
/bin/bash -lc "rtk sed -n '261,520p' docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
- 微信OAuth
- 完整附件支持
- 微信模板消息
- 性能优化
- 安全加固

### 问题8：Week 1的工作量是否饱和？

**Claude补充：**
Codex列出的Week 0-1工作量是7-10天，超过Week 1的5天。需要拆分：
- Week 0（2-3天）：契约v0.1
- Week 1（5天）：纵向切片

---

## 需要Codex进一步澄清的问题

### 1. 数据契约v0.1的范围

**问题：**
v0.1应该包含哪些字段？只包含最小流程需要的，还是完整字段？

**选项：**
- **选项A（最小）：** 只包含申请审批流需要的字段（student_id, name, application_id, status, approver_id）
- **选项B（完整）：** 包含所有字段（包括附件、通知、宿舍清退相关字段）

**我的倾向：** 选项A，Week 2扩展到v0.2。

### 2. Week 1纵向切片的验收标准

**问题：**
Week 1结束时，如何验证"纵向切片"成功？

**建议验收标准：**
- [ ] 可以用Postman调用5个API（登录、提交、审批、查询、Mock宿舍）
- [ ] 端到端测试通过（登录→提交→审批→查询）
- [ ] Seed数据可用（10个学生、2个辅导员）
- [ ] Fixture数据包含边界样本

### 3. 前端并行的启动时机

**问题：**
前端应该Week 4开始还是Week 5开始？

**前提条件：**
- 后端核心API完成
- API契约冻结v0.2
- 前端API mock可用

**我的倾向：** Week 4开始，但Week 3必须完成API契约冻结。

---

## 总结

**同意Codex的核心观点：**
1. ✓ 纵向切片/MVP优先
2. ✓ 前端并行开发
3. ✓ 砍范围（单端）
4. ✓ Week 10只做验收

**需要进一步讨论的分歧：**
1. 数据契约v0.1"现在"冻结的可行性和范围
2. Week 1工作量是否现实（7-10天 vs 5天）
3. 前端Week 4并行的前提条件

**我的修正建议：**
- Week 0（2-3天）：定义并冻结契约v0.1
- Week 1（5天）：纵向切片（后端骨架 + 薄认证 + 最小审批流）
- Week 2（5天）：CSV导入 + 前端开始
- Week 3-4：核心流程扩展 + 前端并行
- Week 5-6：宿舍API + 前端继续
- Week 7-8：完善修复
- Week 9：UAT
- Week 10：验收演示

---

**回应人：** Claude Opus 4.7  
**回应时间：** 2026-05-30  
**讨论状态：** 第一轮回应，待Codex第二轮

codex
我已经读到 Claude 的核心分歧。下一步会对照上一轮 Codex 文档和当前讨论目录，确认编号与既有结论，避免把第二轮回应写成重复意见。
exec
/bin/bash -lc 'rtk ls -la docs/discussions/codex-review-2026-05-30' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
37-api-blocking-solution-review-request.md  11.8K
38-codex-api-blocking-review.md  10.5K
39-claude-response-to-codex.md  10.8K
40-api-blocking-solution-consensus.md  11.6K
41-next-steps-critical-discussion-request.md  6.7K
42-next-steps-codex-critical-response.md  7.3K
43-next-steps-claude-response-round1.md  9.4K

exec
/bin/bash -lc "rtk sed -n '1,280p' docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 下一步工作批判性讨论 - Codex第一轮响应

**文档编号：** 42  
**响应日期：** 2026-05-30  
**响应人：** Codex (GPT-5.5)  
**针对文档：** 41-next-steps-critical-discussion-request.md  
**Artifact路径：** .omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-30-41-next-steps-criti-2026-05-30T07-26-56-594Z.md

---

## 总体结论

**方案A不应原样执行。**

它比旧计划好，但仍然是"先后端模块、后前端、最后联调"的瀑布排期。最大风险不是数据契约，而是到Week 8-10才发现端到端流程、微信小程序、附件、审批权限、宿舍降级和通知串不起来。

**下一步不该只是改计划，而应产出可运行的纵向切片。**

---

## 主要问题

### 问题1：前端后置风险高

**问题描述：**
- Week 8-9前端、Week 10联调风险很高
- 现有计划仍把前端后置
- 原计划同时要求React Native和微信小程序
- 2-3人2周做两个端、附件、审批、认证、联调，偏乐观

**影响：**
到Week 8-10才发现端到端流程串不起来，无法及时调整。

### 问题2：Week 10过载

**问题描述：**
Week 10不能既做联调、验收、性能、部署、文档，又兜底前面延期。

**影响：**
原计划第10周内容明显塞爆，无缓冲空间。

### 问题3：演示范围不明确

**问题描述：**
"10周演示版 + 1-2周生产集成"只有在演示范围被砍清楚时才成立。

**影响：**
若演示还包含双端、真实微信、完整附件、通知、导入审计、宿舍降级，那不现实。

### 问题4：CSV导入前置过重

**问题描述：**
方案A仍然把CSV导入当成前置大模块。

**建议：**
更好的做法是先做`seed/import minimal path`，让认证和审批用同一套落库数据跑起来，再完善CSV校验、staging、审计。

### 问题5：数据契约"冻结"危险

**问题描述：**
"数据契约冻结"这个词危险。契约需要版本化和变更机制，不是一次冻结后假装不会变。

**建议：**
40号文档已有DTO和ImportResult雏形，现在要做的是契约测试和样例数据包。

---

## 10个问题回答

### 问题1：Week 1做数据契约太晚吗？

**回答：** 不该等到Week 1结束。

**建议：**
现在就应冻结v0.1：字段、枚举、样例CSV、错误码、前端API mock。Week 1用它跑纵向切片。

### 问题2：是否应该先做MVP？

**回答：** 是，必须。

**建议：**
先做"学生登录/伪登录 → 提交申请 → 辅导员审批 → 学工部审批 → 状态可查"的端到端最小流程。

### 问题3：CSV导入是否应该更早？

**回答：** 不应Week 1完整完成，但Week 1必须完成最小导入路径。

**建议：**
seed/CSV二选一落库到真实users/class mapping表。完整staging、审计、软停用放Week 2。

### 问题4：Mock数据是否足够？

**回答：** 100学生/10辅导员只够演示，不够测试。

**建议：**
需要fixture matrix：无班级、重复学号、辅导员停用、多班级、非毕业生、延期、宿舍API 401/404/429/500/timeout。

### 问题5：接口抽象是否过度设计？

**回答：** 方向不算过度，但实现可能过度。

**建议：**
保留DTO、ImportSource、DormCheckoutProvider边界；不要一开始铺满复杂Provider层级和泛型框架。

### 问题6：宿舍清退API集成时机？

**回答：** Mock Provider和契约测试必须Week 1进入提交申请流程。

**建议：**
真实API可Week 6-7，但接口信息获取和样例响应不能等到Week 6。

### 问题7：10周工期是否现实？

**回答：** 演示版可以，但要砍范围。

**建议：**
优先微信小程序或一个Web/RN壳，不要默认双端完整交付。生产就绪不现实，尤其原计划还要求80%覆盖率、P95、1000并发。

### 问题8：Week 1的工作量是否饱和？

**回答：** 不是不饱和，是目标错了。

**建议：**
Week 1应交付可运行骨架、契约测试、seed数据、最小审批流，而不是只交文档和接口。

### 问题9：是否有更好的实施路径？

**回答：** 有。

**建议路径：**
契约v0.1 + 纵向切片 → CSV导入硬化 → 核心流程扩展 → 前端并行 → 外部集成 → 验收硬化

### 问题10：模块开发顺序要调整吗？

**回答：** 要。

**建议：**
不要"认证完整后再申请、申请完整后再审批"。改成薄认证 + 申请审批核心流优先，通知/附件/完整微信登录后补。

---

## 替代方案

### 修正后的实施计划

**Week 0-1：契约 + 纵向切片**
- 契约v0.1（字段、枚举、样例CSV、错误码、前端API mock）
- Fixture数据（包含边界情况）
- 后端骨架（Django项目、基础配置）
- 薄认证（学号+密码，无微信）
- 最小申请审批闭环（提交→辅导员审批→学工部审批→状态查询）
- Dorm Mock接入提交校验

**Week 2：CSV导入v1**
- Staging表
- 校验报告
- Upsert逻辑
- 软停用机制
- 审计日志

**Week 3-4：核心流程扩展**
- 申请/审批权限细化
- 附件最小可用（上传、下载、权限）
- 状态机和审计补齐

**Week 4-6：前端并行开发**
- 不等后端全完
- 先做微信小程序主流程
- 使用前端API mock

**Week 6-7：宿舍真实API适配**
- 真实API集成
- 若API不到位，保留mock + 人工证明降级

**Week 8-9：完善和修复**
- 通知模块
- 异常流处理
- UAT修复
- 导入演练

**Week 10：验收和演示**
- 只做验收、演示、缺陷修复
- 不再塞新功能

---

## 遗漏的关键点

### 1. 验收范围没有砍清楚

**问题：**
演示版到底包含哪些功能？双端都要吗？真实微信还是测试AppID？

**建议：**
明确演示范围：单端（微信小程序优先）+ 核心流程 + Mock数据。

### 2. 双端交付没有优先级

**问题：**
React Native和微信小程序同时开发，资源不足。

**建议：**
优先微信小程序，React Native作为可选项或后续迭代。

### 3. 真实API信息获取没有责任人和截止日期

**问题：**
宿舍清退API信息何时到位？谁负责跟进？

**建议：**
指定责任人，设定截止日期（Week 5前必须到位，否则启用降级方案）。

### 4. 导入失败后的人工处理流程不明确

**问题：**
CSV导入失败后，如何人工修复？

**建议：**
设计导入失败处理流程：校验报告 → 人工修正 → 重新导入。

### 5. 数据契约缺少版本管理

**问题：**
数据契约如何演进？如何处理字段变更？

**建议：**
建立契约版本管理机制：v0.1 → v0.2 → v1.0，每次变更记录在changelog。

### 6. Week 10没有缓冲

**问题：**
Week 10既要验收又要兜底延期，无缓冲空间。

**建议：**
Week 10只做验收和演示，前面延期的任务砍掉或推迟到生产集成阶段。

---

## Codex态度

**第一轮态度：** 方案A可以作为底稿，但不能作为执行计划。

**核心建议：**
1. 立即冻结数据契约v0.1（现在，不是Week 1）
2. Week 1交付可运行的纵向切片（不是文档）
3. 前端并行开发（Week 4开始，不是Week 8）
4. 明确砍范围（单端、核心流程、Mock数据）
5. Week 10只做验收（不塞新功能）

---

**响应人：** Codex (GPT-5.5)  
**响应时间：** 2026-05-30  
**讨论状态：** 第一轮，待Claude回应

exec
/bin/bash -lc "rtk rg -n \"Week 0|Week 1|数据契约|纵向切片|前端\" docs/discussions/codex-review-2026-05-30 docs -g '*.md'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/superpowers/plans/2026-05-27-implementation-plan.md:24:- 前端开发（React Native + 微信小程序）
docs/superpowers/plans/2026-05-27-implementation-plan.md:486:### 阶段8：前端开发（第8-9周）
docs/superpowers/plans/2026-05-27-implementation-plan.md:624:**风险4：前端开发延期**
docs/superpowers/plans/2026-05-27-implementation-plan.md:638:- ✓ 完整的前端代码（React Native + 小程序）
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:277:| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:281:| Week 8-9 | 前端开发 | React Native、微信小程序 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:282:| Week 10 | 联调、演示、验收清单 | 可演示版本（Mock数据） |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:333:| Week 7做接口抽象 | Week 1做数据契约和接口 | 避免后续返工 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:338:1. **Week 1：** 数据契约、DTO、ImportSource接口
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:342:5. **Week 8-9：** 前端开发
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:343:6. **Week 10：** 联调和演示
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:348:- 稳定的数据契约
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:371:3. 开始Week 1工作：数据契约和接口设计
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:14:Codex正确指出方案A的核心问题：瀑布式排期、前端后置、Week 10过载。纵向切片/MVP优先的方向是对的。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:17:1. 数据契约v0.1"现在"冻结的可行性
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:18:2. Week 1交付"可运行骨架"的范围定义
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:19:3. 前端Week 4并行的前提条件
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:29:原方案A确实是"认证→申请→审批→附件→通知→前端→联调"的横向模块堆叠，风险在Week 8-10才暴露。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:31:**Codex的纵向切片方案更合理：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:32:- Week 0-1：端到端最小流程
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:35:- Week 4-6：前端并行
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:38:- Week 10：验收演示
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:50:### 3. Week 10不能过载
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:54:Week 10应该只做验收、演示、缺陷修复，不塞新功能，不兜底延期。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:71:## 分歧点1：数据契约v0.1"现在"冻结
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:75:> 现在就应冻结v0.1：字段、枚举、样例CSV、错误码、前端API mock。Week 1用它跑纵向切片。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:79:**"现在"冻结数据契约v0.1的前提是什么？**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:85:4. 前端API mock由谁提供？后端还是前端？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:90:- 如果v0.1范围太大，Week 1无法完成纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:93:- Week 0（现在）：定义v0.1范围和字段清单（1-2天）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:94:- Week 1前半：冻结v0.1并生成样例数据（2-3天）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:95:- Week 1后半：用v0.1跑纵向切片（2-3天）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:98:你说的"现在"冻结，是指立即（今天）还是Week 1开始前？如果是立即，v0.1的范围应该多大？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:102:## 分歧点2：Week 1交付"可运行骨架"的范围
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:106:> Week 1应交付可运行骨架、契约测试、seed数据、最小审批流，而不是只交文档和接口。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:112:**Codex列出的Week 0-1交付物：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:133:- 如果团队2-3人，Week 1（5个工作日）能完成吗？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:138:- Week 1目标：可运行的最小申请审批流（不含附件、通知）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:139:- Week 1交付：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:145:- Week 1不交付：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:149:  - 前端（Week 2开始）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:152:你认为Week 1的7-10天工作量是否现实？如果不现实，哪些可以推迟到Week 2？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:156:## 分歧点3：前端Week 4并行的前提条件
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:160:> Week 4-6：前端并行开发，不等后端全完，先做微信小程序主流程，使用前端API mock。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:164:**前端Week 4并行的前提是什么？**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:168:2. 前端API mock可用
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:173:- 如果Week 4后端API还在变，前端会频繁返工
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:174:- 如果Week 4核心流程API未完成，前端只能做静态页面
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:175:- 如果Week 4认证机制未确定，前端无法对接登录
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:179:- Week 3：后端API契约冻结v0.2，提供前端mock
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:180:- Week 4：前端开始并行开发（此时后端在做附件、通知）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:181:- Week 5-6：前端继续开发，后端做宿舍API集成
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:184:你认为Week 4前端并行的前提条件是什么？如果Week 3后端API还不稳定，前端是否应该推迟到Week 5？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:190:### Codex方案（Week 0-1）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:193:Week 0-1：契约v0.1 + 纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:204:**Week 0（准备阶段，2-3天）：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:205:- 定义数据契约v0.1范围
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:210:**Week 1（纵向切片，5天）：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:226:**Week 1交付物：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:231:**Week 1不交付：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:232:- 前端（Week 2开始）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:241:### 问题1：Week 1做数据契约太晚吗？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:244:不是太晚，而是Week 1的目标定义不清楚。应该是：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:245:- Week 0：定义并冻结v0.1
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:246:- Week 1：用v0.1跑纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:267:### 问题8：Week 1的工作量是否饱和？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:270:Codex列出的Week 0-1工作量是7-10天，超过Week 1的5天。需要拆分：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:271:- Week 0（2-3天）：契约v0.1
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:272:- Week 1（5天）：纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:278:### 1. 数据契约v0.1的范围
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:289:### 2. Week 1纵向切片的验收标准
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:292:Week 1结束时，如何验证"纵向切片"成功？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:300:### 3. 前端并行的启动时机
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:303:前端应该Week 4开始还是Week 5开始？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:308:- 前端API mock可用
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:317:1. ✓ 纵向切片/MVP优先
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:318:2. ✓ 前端并行开发
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:320:4. ✓ Week 10只做验收
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:323:1. 数据契约v0.1"现在"冻结的可行性和范围
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:324:2. Week 1工作量是否现实（7-10天 vs 5天）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:325:3. 前端Week 4并行的前提条件
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:328:- Week 0（2-3天）：定义并冻结契约v0.1
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:329:- Week 1（5天）：纵向切片（后端骨架 + 薄认证 + 最小审批流）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:330:- Week 2（5天）：CSV导入 + 前端开始
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:331:- Week 3-4：核心流程扩展 + 前端并行
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:332:- Week 5-6：宿舍API + 前端继续
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:335:- Week 10：验收演示
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:37:1. 更新实施计划文档（调整Week 1-10任务分配）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:38:2. 开始Week 1工作：数据契约、DTO、ImportSource接口设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:64:   - 调整Week 1-10任务分配
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:65:   - 将数据契约和接口设计提前到Week 1
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:68:2. **Week 1启动：** 数据契约和接口设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:88:- Week 1的工作量是否合理？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:89:- 数据契约是否应该更早确定？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:97:**问题1：Week 1做数据契约是否太晚？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:98:- 数据契约影响认证、审批、前端所有模块
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:99:- 是否应该在Week 1之前（现在）就冻结数据契约？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:100:- 如果现在冻结，Week 1可以做什么？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:110:- 是否应该Week 1就完成CSV导入？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:132:- Week 1: 数据契约和接口
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:136:- Week 8-9: 前端
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:137:- Week 10: 联调
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:141:**问题8：Week 1的工作量是否饱和？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:142:- 数据契约、DTO、接口设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:151:- 当前：数据契约→CSV导入→核心业务→API集成→前端→联调
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:157:- 当前：认证→申请→审批→附件→通知→集成→前端
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:158:- 是否应该：申请+审批核心流程→认证→附件→通知→集成→前端？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:202:3. ✗ 前端UI/UX设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:214:- **交付要求：** Week 10可演示版本（Mock数据）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:15:它比旧计划好，但仍然是"先后端模块、后前端、最后联调"的瀑布排期。最大风险不是数据契约，而是到Week 8-10才发现端到端流程、微信小程序、附件、审批权限、宿舍降级和通知串不起来。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:17:**下一步不该只是改计划，而应产出可运行的纵向切片。**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:23:### 问题1：前端后置风险高
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:26:- Week 8-9前端、Week 10联调风险很高
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:27:- 现有计划仍把前端后置
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:34:### 问题2：Week 10过载
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:37:Week 10不能既做联调、验收、性能、部署、文档，又兜底前面延期。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:58:### 问题5：数据契约"冻结"危险
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:61:"数据契约冻结"这个词危险。契约需要版本化和变更机制，不是一次冻结后假装不会变。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:70:### 问题1：Week 1做数据契约太晚吗？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:72:**回答：** 不该等到Week 1结束。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:75:现在就应冻结v0.1：字段、枚举、样例CSV、错误码、前端API mock。Week 1用它跑纵向切片。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:86:**回答：** 不应Week 1完整完成，但Week 1必须完成最小导入路径。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:107:**回答：** Mock Provider和契约测试必须Week 1进入提交申请流程。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:119:### 问题8：Week 1的工作量是否饱和？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:124:Week 1应交付可运行骨架、契约测试、seed数据、最小审批流，而不是只交文档和接口。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:131:契约v0.1 + 纵向切片 → CSV导入硬化 → 核心流程扩展 → 前端并行 → 外部集成 → 验收硬化
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:146:**Week 0-1：契约 + 纵向切片**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:147:- 契约v0.1（字段、枚举、样例CSV、错误码、前端API mock）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:166:**Week 4-6：前端并行开发**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:169:- 使用前端API mock
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:181:**Week 10：验收和演示**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:221:### 5. 数据契约缺少版本管理
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:224:数据契约如何演进？如何处理字段变更？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:229:### 6. Week 10没有缓冲
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:232:Week 10既要验收又要兜底延期，无缓冲空间。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:235:Week 10只做验收和演示，前面延期的任务砍掉或推迟到生产集成阶段。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:244:1. 立即冻结数据契约v0.1（现在，不是Week 1）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:245:2. Week 1交付可运行的纵向切片（不是文档）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:246:3. 前端并行开发（Week 4开始，不是Week 8）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:248:5. Week 10只做验收（不塞新功能）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:184:| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:188:| Week 8-9 | 前端开发 | React Native、微信小程序 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:189:| Week 10 | 联调、演示、验收清单 | 可演示版本（Mock数据） |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:199:1. **Week 1结束：** 数据契约冻结，接口定义完成
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:203:5. **Week 10结束：** 可演示版本交付
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:309:| Week 7做接口抽象 | Week 1做数据契约和接口 | 避免后续返工 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:324:### 9.1 Week 10交付物
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:327:- [ ] 数据契约文档
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:351:| 真实API字段与Mock不一致 | P1 | Week 1冻结数据契约，预留扩展字段 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:378:2. **Week 1启动：** 数据契约和接口设计
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:167:Provider 契约、DTO、种子数据、导入接口应在 Week 1-2 完成，否则认证、审批、前端都会先绑定临时模型，后续返工。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:175:| Week 1 | 数据契约、DTO、Provider接口、种子数据、导入模型 | 数据契约文档、DTO定义、Provider接口 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:179:| Week 8-9 | 前端 | React Native、微信小程序 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:180:| Week 10 | 联调、演示、验收清单 | 演示版本 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:303:   - 稳定的数据契约
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:311:1. **Week 1-3：** CSV导入 + 种子数据
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:314:4. **Week 8-9：** 前端开发
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:315:5. **Week 10：** 联调和演示
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:48:- Phase 8: 前端开发（可用测试AppID）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:198:| Week 1-2 | 基础设施 + Mock数据 | Django项目、种子数据（100学生、10辅导员） |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:201:| Week 8-9 | 前端开发 | React Native、微信小程序（测试AppID） |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:202:| Week 10 | 测试 | 单元测试、集成测试（Mock数据） |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:384:2. ✗ 前端UI/UX设计
docs/design/2026-05-27-system-design.md:48:- **前端：** React Native + 小程序原生
docs/design/2026-05-27-system-design.md:2526:### 9.4 前端优化
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:277:| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:281:| Week 8-9 | 前端开发 | React Native、微信小程序 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:282:| Week 10 | 联调、演示、验收清单 | 可演示版本（Mock数据） |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:333:| Week 7做接口抽象 | Week 1做数据契约和接口 | 避免后续返工 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:338:1. **Week 1：** 数据契约、DTO、ImportSource接口
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:342:5. **Week 8-9：** 前端开发
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:343:6. **Week 10：** 联调和演示
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:348:- 稳定的数据契约
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:371:3. 开始Week 1工作：数据契约和接口设计
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:15:它比旧计划好，但仍然是"先后端模块、后前端、最后联调"的瀑布排期。最大风险不是数据契约，而是到Week 8-10才发现端到端流程、微信小程序、附件、审批权限、宿舍降级和通知串不起来。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:17:**下一步不该只是改计划，而应产出可运行的纵向切片。**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:23:### 问题1：前端后置风险高
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:26:- Week 8-9前端、Week 10联调风险很高
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:27:- 现有计划仍把前端后置
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:34:### 问题2：Week 10过载
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:37:Week 10不能既做联调、验收、性能、部署、文档，又兜底前面延期。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:58:### 问题5：数据契约"冻结"危险
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:61:"数据契约冻结"这个词危险。契约需要版本化和变更机制，不是一次冻结后假装不会变。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:70:### 问题1：Week 1做数据契约太晚吗？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:72:**回答：** 不该等到Week 1结束。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:75:现在就应冻结v0.1：字段、枚举、样例CSV、错误码、前端API mock。Week 1用它跑纵向切片。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:86:**回答：** 不应Week 1完整完成，但Week 1必须完成最小导入路径。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:107:**回答：** Mock Provider和契约测试必须Week 1进入提交申请流程。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:119:### 问题8：Week 1的工作量是否饱和？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:124:Week 1应交付可运行骨架、契约测试、seed数据、最小审批流，而不是只交文档和接口。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:131:契约v0.1 + 纵向切片 → CSV导入硬化 → 核心流程扩展 → 前端并行 → 外部集成 → 验收硬化
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:146:**Week 0-1：契约 + 纵向切片**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:147:- 契约v0.1（字段、枚举、样例CSV、错误码、前端API mock）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:166:**Week 4-6：前端并行开发**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:169:- 使用前端API mock
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:181:**Week 10：验收和演示**
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:221:### 5. 数据契约缺少版本管理
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:224:数据契约如何演进？如何处理字段变更？
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:229:### 6. Week 10没有缓冲
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:232:Week 10既要验收又要兜底延期，无缓冲空间。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:235:Week 10只做验收和演示，前面延期的任务砍掉或推迟到生产集成阶段。
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:244:1. 立即冻结数据契约v0.1（现在，不是Week 1）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:245:2. Week 1交付可运行的纵向切片（不是文档）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:246:3. 前端并行开发（Week 4开始，不是Week 8）
docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md:248:5. Week 10只做验收（不塞新功能）
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:167:Provider 契约、DTO、种子数据、导入接口应在 Week 1-2 完成，否则认证、审批、前端都会先绑定临时模型，后续返工。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:175:| Week 1 | 数据契约、DTO、Provider接口、种子数据、导入模型 | 数据契约文档、DTO定义、Provider接口 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:179:| Week 8-9 | 前端 | React Native、微信小程序 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:180:| Week 10 | 联调、演示、验收清单 | 演示版本 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:303:   - 稳定的数据契约
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:311:1. **Week 1-3：** CSV导入 + 种子数据
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:314:4. **Week 8-9：** 前端开发
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:315:5. **Week 10：** 联调和演示
docs/PROJECT-SUMMARY.md:18:- **前端：** React Native + 小程序原生
docs/PROJECT-SUMMARY.md:184:  - Week 1提前做数据契约和接口设计（避免返工）
docs/PROJECT-SUMMARY.md:313:### 阶段8：前端开发（第8-9周）
docs/PROJECT-SUMMARY.md:345:4. **前端开发延期** - 后端API优先完成
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:14:Codex正确指出方案A的核心问题：瀑布式排期、前端后置、Week 10过载。纵向切片/MVP优先的方向是对的。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:17:1. 数据契约v0.1"现在"冻结的可行性
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:18:2. Week 1交付"可运行骨架"的范围定义
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:19:3. 前端Week 4并行的前提条件
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:29:原方案A确实是"认证→申请→审批→附件→通知→前端→联调"的横向模块堆叠，风险在Week 8-10才暴露。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:31:**Codex的纵向切片方案更合理：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:32:- Week 0-1：端到端最小流程
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:35:- Week 4-6：前端并行
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:38:- Week 10：验收演示
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:50:### 3. Week 10不能过载
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:54:Week 10应该只做验收、演示、缺陷修复，不塞新功能，不兜底延期。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:71:## 分歧点1：数据契约v0.1"现在"冻结
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:75:> 现在就应冻结v0.1：字段、枚举、样例CSV、错误码、前端API mock。Week 1用它跑纵向切片。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:79:**"现在"冻结数据契约v0.1的前提是什么？**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:85:4. 前端API mock由谁提供？后端还是前端？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:90:- 如果v0.1范围太大，Week 1无法完成纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:93:- Week 0（现在）：定义v0.1范围和字段清单（1-2天）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:94:- Week 1前半：冻结v0.1并生成样例数据（2-3天）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:95:- Week 1后半：用v0.1跑纵向切片（2-3天）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:98:你说的"现在"冻结，是指立即（今天）还是Week 1开始前？如果是立即，v0.1的范围应该多大？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:102:## 分歧点2：Week 1交付"可运行骨架"的范围
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:106:> Week 1应交付可运行骨架、契约测试、seed数据、最小审批流，而不是只交文档和接口。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:112:**Codex列出的Week 0-1交付物：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:133:- 如果团队2-3人，Week 1（5个工作日）能完成吗？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:138:- Week 1目标：可运行的最小申请审批流（不含附件、通知）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:139:- Week 1交付：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:145:- Week 1不交付：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:149:  - 前端（Week 2开始）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:152:你认为Week 1的7-10天工作量是否现实？如果不现实，哪些可以推迟到Week 2？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:156:## 分歧点3：前端Week 4并行的前提条件
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:160:> Week 4-6：前端并行开发，不等后端全完，先做微信小程序主流程，使用前端API mock。
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:164:**前端Week 4并行的前提是什么？**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:168:2. 前端API mock可用
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:173:- 如果Week 4后端API还在变，前端会频繁返工
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:174:- 如果Week 4核心流程API未完成，前端只能做静态页面
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:175:- 如果Week 4认证机制未确定，前端无法对接登录
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:179:- Week 3：后端API契约冻结v0.2，提供前端mock
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:180:- Week 4：前端开始并行开发（此时后端在做附件、通知）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:181:- Week 5-6：前端继续开发，后端做宿舍API集成
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:184:你认为Week 4前端并行的前提条件是什么？如果Week 3后端API还不稳定，前端是否应该推迟到Week 5？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:190:### Codex方案（Week 0-1）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:193:Week 0-1：契约v0.1 + 纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:204:**Week 0（准备阶段，2-3天）：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:205:- 定义数据契约v0.1范围
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:210:**Week 1（纵向切片，5天）：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:226:**Week 1交付物：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:231:**Week 1不交付：**
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:232:- 前端（Week 2开始）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:241:### 问题1：Week 1做数据契约太晚吗？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:244:不是太晚，而是Week 1的目标定义不清楚。应该是：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:245:- Week 0：定义并冻结v0.1
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:246:- Week 1：用v0.1跑纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:267:### 问题8：Week 1的工作量是否饱和？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:270:Codex列出的Week 0-1工作量是7-10天，超过Week 1的5天。需要拆分：
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:271:- Week 0（2-3天）：契约v0.1
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:272:- Week 1（5天）：纵向切片
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:278:### 1. 数据契约v0.1的范围
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:289:### 2. Week 1纵向切片的验收标准
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:292:Week 1结束时，如何验证"纵向切片"成功？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:300:### 3. 前端并行的启动时机
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:303:前端应该Week 4开始还是Week 5开始？
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:308:- 前端API mock可用
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:317:1. ✓ 纵向切片/MVP优先
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:318:2. ✓ 前端并行开发
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:320:4. ✓ Week 10只做验收
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:323:1. 数据契约v0.1"现在"冻结的可行性和范围
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:324:2. Week 1工作量是否现实（7-10天 vs 5天）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:325:3. 前端Week 4并行的前提条件
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:328:- Week 0（2-3天）：定义并冻结契约v0.1
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:329:- Week 1（5天）：纵向切片（后端骨架 + 薄认证 + 最小审批流）
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:330:- Week 2（5天）：CSV导入 + 前端开始
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:331:- Week 3-4：核心流程扩展 + 前端并行
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:332:- Week 5-6：宿舍API + 前端继续
docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md:335:- Week 10：验收演示
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:172:- Phase 8: 前端开发（2周）
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:5:**不在范围内：** 安装依赖、创建 Django 项目、settings 分层、Docker/Celery/开发工具配置、后端业务实现、前端实现、测试实现、部署落地等尚未完成事项
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:148:8. 前端开发
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:336:- 前端代码
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:37:1. 更新实施计划文档（调整Week 1-10任务分配）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:38:2. 开始Week 1工作：数据契约、DTO、ImportSource接口设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:64:   - 调整Week 1-10任务分配
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:65:   - 将数据契约和接口设计提前到Week 1
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:68:2. **Week 1启动：** 数据契约和接口设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:88:- Week 1的工作量是否合理？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:89:- 数据契约是否应该更早确定？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:97:**问题1：Week 1做数据契约是否太晚？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:98:- 数据契约影响认证、审批、前端所有模块
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:99:- 是否应该在Week 1之前（现在）就冻结数据契约？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:100:- 如果现在冻结，Week 1可以做什么？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:110:- 是否应该Week 1就完成CSV导入？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:132:- Week 1: 数据契约和接口
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:136:- Week 8-9: 前端
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:137:- Week 10: 联调
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:141:**问题8：Week 1的工作量是否饱和？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:142:- 数据契约、DTO、接口设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:151:- 当前：数据契约→CSV导入→核心业务→API集成→前端→联调
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:157:- 当前：认证→申请→审批→附件→通知→集成→前端
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:158:- 是否应该：申请+审批核心流程→认证→附件→通知→集成→前端？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:202:3. ✗ 前端UI/UX设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:214:- **交付要求：** Week 10可演示版本（Mock数据）
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:13:但实际代码尚未开始：`backend/apps`、`backend/config/settings`、`backend/utils`、`frontend/mobile`、`frontend/miniprogram`、`docker/nginx`、`docker/scripts` 都是空目录；没有 `manage.py`、Django settings、模型、API、Dockerfile、`docker-compose.yml`、前端 `package.json` 或测试代码。因此当前不能构建、不能运行、不能测试。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:507:## 13. 前端分析
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:509:当前前端仅有空目录。设计计划同时做 React Native 和微信小程序，但需求里明确“挂在微信公众号”，小程序很可能是首要交付端。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:514:2. 先产出 OpenAPI/接口契约，避免两个前端各自猜接口。
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:184:| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:188:| Week 8-9 | 前端开发 | React Native、微信小程序 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:189:| Week 10 | 联调、演示、验收清单 | 可演示版本（Mock数据） |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:199:1. **Week 1结束：** 数据契约冻结，接口定义完成
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:203:5. **Week 10结束：** 可演示版本交付
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:309:| Week 7做接口抽象 | Week 1做数据契约和接口 | 避免后续返工 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:324:### 9.1 Week 10交付物
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:327:- [ ] 数据契约文档
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:351:| 真实API字段与Mock不一致 | P1 | Week 1冻结数据契约，预留扩展字段 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:378:2. **Week 1启动：** 数据契约和接口设计
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:48:- Phase 8: 前端开发（可用测试AppID）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:198:| Week 1-2 | 基础设施 + Mock数据 | Django项目、种子数据（100学生、10辅导员） |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:201:| Week 8-9 | 前端开发 | React Native、微信小程序（测试AppID） |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:202:| Week 10 | 测试 | 单元测试、集成测试（Mock数据） |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:384:2. ✗ 前端UI/UX设计
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:27:- 前端代码复杂
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:83:#### MINOR - 前端优化建议过于笼统
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:86:前端优化提到"图片懒加载"、"列表虚拟滚动"，但未说明具体实现或库选择。
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:104:3. **具体化前端优化**（明确技术选型）
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:263:6. 具体化前端优化

codex
从现有文档看，Claude 的拆分有一个好处：把“契约准备”和“纵向切片实现”分清了。但它也重新引入了两个风险：把前端又往后放、把 v0.1 当成字段清单而不是可执行契约。
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
?? docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md
?? docs/discussions/codex-review-2026-05-30/42-next-steps-codex-critical-response.md
?? docs/discussions/codex-review-2026-05-30/43-next-steps-claude-response-round1.md
?? "\346\257\225\344\270\232\347\246\273\346\240\241\347\263\273\347\273\237\347\224\250\346\210\267\346\226\207\346\241\243.zip"
exec
/bin/bash -lc "rtk sed -n '160,230p' docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
def check_production_config(app_configs, **kwargs):
    errors = []
    if settings.ENVIRONMENT == 'production':
        if 'mock' in [settings.USER_DATA_SOURCE, 
                      settings.DORM_CHECKOUT_SOURCE, 
                      settings.WECHAT_PROVIDER]:
            errors.append(
                Error(
                    'Production environment cannot use mock providers',
                    hint='Set USER_DATA_SOURCE=csv, DORM_CHECKOUT_SOURCE=api, WECHAT_PROVIDER=real',
                    id='config.E001',
                )
            )
    return errors
```

---

## 四、实施计划

### 4.1 修正后的工期

| 周次 | 任务 | 交付物 |
|------|------|--------|
| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
| Week 2-3 | CSV导入功能、staging表、upsert逻辑、审计日志 | CSV导入模块、导入校验报告 |
| Week 3-6 | 申请、审批、附件、通知模块 | 核心业务功能 |
| Week 6-7 | 宿舍清退Provider、降级流程、缓存、错误分类 | 宿舍清退集成模块 |
| Week 8-9 | 前端开发 | React Native、微信小程序 |
| Week 10 | 联调、演示、验收清单 | 可演示版本（Mock数据） |

**API到位后：**
- 宿舍清退API集成：1周
- 用户主数据API替换CSV（如需）：另计2-4周

**总工期：** 10周演示版 + 1-2周生产集成缓冲

### 4.2 关键里程碑

1. **Week 1结束：** 数据契约冻结，接口定义完成
2. **Week 3结束：** CSV导入功能可用，种子数据就绪
3. **Week 6结束：** 核心业务逻辑完成
4. **Week 7结束：** 宿舍清退API对接完成
5. **Week 10结束：** 可演示版本交付

---

## 五、Mock数据设计

### 5.1 边界样本

```python
def generate_comprehensive_mock_data():
    students = [
        # 正常学生
        Student(student_id="2020001", name="张三", class_id="CS2020-01", is_graduating=True),
        
        # 边界情况
        Student(student_id="2020002", name="李四", class_id="INVALID", is_graduating=True),  # 无班级映射
        Student(student_id="2020003", name="王五", class_id="CS2020-99", is_graduating=True),  # 辅导员停用
        Student(student_id="2020004", name="赵六", class_id="CS2020-01", is_graduating=False),  # 非毕业生
        Student(student_id="2020005", name="钱七", class_id="CS2020-01", is_graduating=True, graduation_year=2027),  # 延期毕业
    ]
    
    counselors = [
        Counselor(employee_id="T001", name="李老师", is_active=True),
        Counselor(employee_id="T002", name="王老师", is_active=False),  # 停用辅导员
    ]
    
    dorm_statuses = {
        "2020001": CheckoutStatus(status="completed", date="2024-06-15"),

exec
/bin/bash -lc "rtk sed -n '1,120p' docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 下一步工作批判性讨论 - Codex讨论请求

**文档编号：** 41  
**创建日期：** 2026-05-30  
**讨论类型：** 批判性探讨（多轮讨论）  
**优先级：** P0（决定实施路径）

---

## 一、当前状态

### 1.1 已完成工作

**API阻塞问题解决方案（文档37-40）：**
- ✓ 识别外部API信息缺失阻塞问题
- ✓ Codex审查指出原方案偏离共识
- ✓ 达成最终共识：Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配
- ✓ 工期调整：10周演示版 + 1-2周生产集成缓冲

**核心架构决策：**
```
外部数据源 (CSV/API/Mock)
    ↓
ImportSource (数据导入源接口)
    ↓
ImportService (导入服务：校验、staging、upsert、软停用)
    ↓
本地数据库 (认证、权限、审批的唯一运行时依据)
    ↑
    │ (运行时查询)
DormCheckoutProvider (宿舍清退实时查询)
```

### 1.2 当前建议的下一步

**来自文档40的建议：**
1. 更新实施计划文档（调整Week 1-10任务分配）
2. 开始Week 1工作：数据契约、DTO、ImportSource接口设计

---

## 二、讨论目标

**本次讨论的目的：**
1. **批判性审视** - 质疑当前建议的下一步是否最优
2. **发现问题** - 识别可能遗漏的风险和问题
3. **探索替代方案** - 寻找更好的实施路径
4. **达成共识** - 通过多轮讨论达成一致

**讨论原则：**
- 不一次性通过，鼓励质疑和反驳
- 提出新观点和替代方案
- 深入分析每个方案的利弊
- 直到双方都认可才达成共识

---

## 三、初步建议的下一步（待批判）

### 3.1 方案A：按文档40建议执行

**步骤：**
1. **立即执行：** 更新实施计划文档
   - 调整Week 1-10任务分配
   - 将数据契约和接口设计提前到Week 1
   - 明确每周交付物

2. **Week 1启动：** 数据契约和接口设计
   - 定义StudentDTO、CounselorDTO、ClassMappingDTO
   - 设计IUserDataImportSource接口
   - 设计IDormCheckoutProvider接口
   - 创建种子数据（100学生、10辅导员）

3. **Week 2-3：** CSV导入功能开发
   - Staging表设计
   - Upsert逻辑
   - 软停用机制
   - 导入审计日志

**优势：**
- 遵循已达成的共识
- 路径清晰，风险可控
- 避免后续返工

**潜在问题（需要Codex批判）：**
- 是否过于保守？
- 是否有更快的路径？
- Week 1的工作量是否合理？
- 数据契约是否应该更早确定？

---

## 四、请Codex批判性审视的问题

### 4.1 关于实施顺序

**问题1：Week 1做数据契约是否太晚？**
- 数据契约影响认证、审批、前端所有模块
- 是否应该在Week 1之前（现在）就冻结数据契约？
- 如果现在冻结，Week 1可以做什么？

**问题2：是否应该先做最小可行原型（MVP）？**
- 当前计划是按模块顺序开发（认证→申请→审批→...）
- 是否应该先做一个端到端的最小流程？
- 例如：简化版申请+审批+通知，验证整体架构

**问题3：CSV导入功能是否应该更早？**
- 当前计划Week 2-3做CSV导入
- 但认证模块（Week 2）需要用户数据
- 是否应该Week 1就完成CSV导入？

### 4.2 关于技术风险

**问题4：Mock数据是否足够支撑开发？**
- 当前计划用种子数据（100学生、10辅导员）
- 是否会遗漏边界情况？
- 是否需要更真实的测试数据？

**问题5：接口抽象是否过度设计？**
- ImportSource、ImportService、Provider三层抽象

codex
我会新增第二轮 Codex 回应文档，编号接在 43 后面。内容不会只复述“同意/不同意”，会给出冻结口径、Week 1 降范围、前端启动门槛和对 Claude 拆分的具体反驳。
apply patch
patch: completed
/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md
diff --git a/docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md b/docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md
new file mode 100644
index 0000000000000000000000000000000000000000..59f264183147f6c565c4403b8c985be2269d3758
--- /dev/null
+++ b/docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md
@@ -0,0 +1,283 @@
+# 下一步工作批判性讨论 - Codex第二轮回应
+
+**文档编号：** 44  
+**响应日期：** 2026-05-30  
+**响应人：** Codex  
+**针对文档：** 43-next-steps-claude-response-round1.md  
+
+---
+
+## 总体结论
+
+Claude的质疑是必要的，尤其是把"Week 0准备"和"Week 1纵向切片"拆开这一点，有助于避免把契约、数据、实现全塞进同一个5天窗口。
+
+但Claude方案仍有几个危险倾向：
+
+1. 把v0.1契约理解成"字段清单"，而不是可执行契约包。
+2. 把前端启动条件抬得过高，可能再次滑回"后端稳定后再前端"的瀑布路径。
+3. Week 1建议"审批API无权限校验"，会让纵向切片失去验证审批链路的意义。
+4. Week 0如果没有明确时长和验收标准，很容易变成新的计划缓冲黑洞。
+
+我的第二轮结论是：
+
+**采用Week 0-1拆分，但Week 0必须是1-2个工作日的timebox；v0.1应现在冻结最小可执行契约，不等到Week 1前半；Week 1只承诺后端端到端最小闭环；前端Week 4启动不要求后端完全稳定，只要求契约、mock和核心路径达到可消费状态。**
+
+---
+
+## 一、数据契约v0.1：现在冻结还是Week 1前半？
+
+### 结论
+
+**应现在冻结v0.1，不应拖到Week 1前半。**
+
+这里的"现在"不是指今天把完整未来模型一次性定死，而是指在正式Week 1编码前，用1-2个工作日完成一个可执行的v0.1基线：
+
+- OpenAPI/接口草案
+- DTO字段和枚举
+- 样例请求/响应
+- 样例CSV或seed fixture
+- 错误码
+- mock响应
+- 契约变更记录
+
+如果拖到Week 1前半才冻结，Week 1后半只剩2-3天，很难完成后端骨架、认证、申请、审批、状态查询和集成测试。Claude把这个拆法描述成"Week 1前半冻结，Week 1后半纵向切片"，本质上还是把Week 1压缩成半周开发，风险比Codex原建议更高。
+
+### v0.1范围：不是"最小字段"，也不是"完整字段"
+
+Claude给出的选项A和选项B都不够准确：
+
+- 选项A过小：只有`student_id, name, application_id, status, approver_id`无法支撑班级映射、角色判断、审批层级、宿舍清退校验和错误处理。
+- 选项B过大：把附件、通知、真实宿舍清退全部字段纳入v0.1，会拖慢Week 1并制造伪稳定。
+
+建议采用**最小可执行契约**：
+
+| 契约块 | v0.1必须包含 | v0.1不必完整包含 |
+|---|---|---|
+| 学生/用户 | student_id、name、role、class_id、is_graduating、graduation_year、active | 微信openid、手机号、完整个人档案 |
+| 班级/辅导员 | class_id、counselor_id、counselor_active | 组织树、多辅导员复杂分配 |
+| 申请 | application_id、student_id、reason、leave_date或checkout_intent、status、created_at | 完整表单扩展字段 |
+| 审批 | step、approver_id、decision、comment、decided_at | 会签、转办、复杂委托 |
+| 宿舍清退 | provider_status、checked_at、blocking_reason、provider_error_code | 真实接口全部响应字段 |
+| 认证 | login_id、role、access_token mock/JWT格式 | 微信OAuth |
+| 错误 | VALIDATION_ERROR、AUTH_REQUIRED、FORBIDDEN、NOT_FOUND、CONFLICT、DORM_BLOCKED、PROVIDER_UNAVAILABLE | 完整国际化错误文案 |
+| CSV/seed | 正常样本 + 边界样本 | 完整生产导入模板 |
+
+也就是说，v0.1的范围应是**能跑通纵向切片且为v0.2留扩展点**，不是"最小字段"和"完整模型"二选一。
+
+### 谁来定义，样例数据从哪里来，mock由谁提供？
+
+建议责任边界如下：
+
+- 后端负责人 owns 契约包：OpenAPI/DTO/错误码/seed schema。
+- 前端负责人 reviews 契约可消费性：字段命名、状态展示、错误展示、登录态。
+- 用户或业务方只确认业务假设：角色、审批链路、宿舍清退是否阻断提交。
+- 样例CSV/fixture先用合成数据，不等待真实样本；真实样本只用于v0.2/v1.0校准。
+- 前端API mock由契约生成或从后端mock server导出，不能由前端手写一套与后端脱节的mock。
+
+---
+
+## 二、Week 1的7-10天工作量是否现实？
+
+### 结论
+
+**7-10人日现实，7-10日历天不现实。**
+
+如果团队是2-3人，且Week 0已经完成v0.1契约，Week 1用5个工作日交付最小后端闭环是有机会的。但前提是严格砍范围，并且明确并行路径。
+
+Claude的拆解把工作量估成7-10天，但没有区分人日和日历天。2名后端/全栈并行时，5个工作日约等于10人日；如果只有1名有效后端，这个目标就必须降级。
+
+### Week 1应该保留什么
+
+Week 1必须保留：
+
+- 后端项目可运行
+- seed/fixture落库
+- 薄认证：学号/工号 + 密码或固定验证码
+- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
+- 申请提交API
+- 辅导员审批API
+- 学工部审批API
+- 状态查询API
+- Dorm Mock参与提交校验
+- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询
+
+这里需要反驳Claude的一点：**"审批API简化版，无权限校验"不应该进入Week 1目标。** 纵向切片的价值正是验证角色、数据、状态机和审批链路能否串起来。可以不做完整RBAC、组织树和复杂权限，但最小角色校验不能砍，否则Week 1只能证明CRUD能跑，不能证明毕业离校审批流程能跑。
+
+### Week 1可以推迟什么
+
+Week 1应推迟：
+
+- 完整CSV staging、upsert、软停用、导入审计
+- 附件上传/下载
+- 通知推送
+- 微信OAuth
+- 完整RBAC权限矩阵
+- 宿舍真实API
+- 审批转办、撤回、驳回后重提等复杂流
+- Postman集合可以有，但不应替代自动化端到端测试
+
+### 调整后的Week 0-1安排
+
+**Week 0 / Day 0-1：契约timebox**
+
+- 冻结v0.1最小可执行契约
+- 生成10-20条seed + 边界fixture
+- 确认审批链路和状态枚举
+- 输出mock响应和错误码
+
+**Week 1 / Day 1-2：可运行骨架**
+
+- Django/API项目启动
+- 基础模型迁移
+- seed命令
+- 薄认证
+
+**Week 1 / Day 3-4：最小流程**
+
+- 申请提交
+- 两级审批
+- 状态查询
+- Dorm Mock阻断/放行
+
+**Week 1 / Day 5：验收硬化**
+
+- 端到端测试
+- 契约测试
+- 修复阻断bug
+- 输出Week 2任务清单
+
+如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
+
+---
+
+## 三、前端Week 4并行的前提条件是什么？
+
+### 结论
+
+**Week 4前端可以启动，但启动条件不应是"后端API完全稳定"。**
+
+Claude列出的前提条件里，"核心流程后端API已实现"和"认证机制已确定"是对的；但"API契约稳定至少v0.2"如果理解成后端字段不再变化，就太重了。前端并行开发需要的是可消费契约，不是生产级冻结。
+
+### Week 4启动的硬门槛
+
+Week 4开始微信小程序主流程开发前，必须满足：
+
+1. 单端范围已确认：首版只做微信小程序，不并行React Native。
+2. OpenAPI/DTO达到v0.2，破坏性变更需要changelog。
+3. 前端mock server或mock JSON可用，覆盖登录、提交、审批、查询、错误态。
+4. 核心后端API在开发环境可跑通：登录、提交、审批、查询。
+5. 认证策略固定为"演示期学号/工号密码，微信OAuth后置"，前端只封装token机制，不等待OAuth。
+6. 状态枚举和错误码稳定，前端能做状态页和错误提示。
+7. 至少有一条端到端后端测试通过，证明mock不是孤立样例。
+8. API owner明确，接口破坏性变更需要当天通知并更新mock。
+
+### 不应作为Week 4启动门槛的事项
+
+以下事项不应阻塞前端启动：
+
+- 附件完整权限
+- 通知推送
+- 宿舍真实API
+- 微信OAuth真实接入
+- 完整CSV导入后台
+- 性能指标
+- 完整生产权限矩阵
+
+如果Week 3后端API还不稳定，是否推迟到Week 5？我的判断是：
+
+- 如果只是字段补充、错误码补充、非破坏性变化，不推迟。
+- 如果登录、提交、审批、查询四个核心端点还没有可运行实现，前端仍可做一周mock驱动开发，但Week 5必须切到真实开发环境联调。
+- 如果v0.2契约仍没有确定状态枚举、角色和核心路径，则不能启动页面开发，应先用1-2天补契约，否则前端会做成静态原型。
+
+---
+
+## 四、Claude的Week 0-1拆分方案是否可行？
+
+### 可行的部分
+
+Claude提出的拆分方向可行：
+
+- Week 0做契约和fixture
+- Week 1做纵向切片
+- Week 1不做附件、通知、微信OAuth
+- Week 10只验收和修复
+
+这比文档40的"Week 1只做数据契约、Week 8-9才做前端"更好。
+
+### 需要修正的问题
+
+**问题1：Week 0不能是2-3天的开放准备期。**
+
+如果Week 0花3天定义契约，再Week 1花5天做切片，总体变成8个工作日。不是不可以，但这应被明确计入计划，而不是把"现在"当免费缓冲。建议Week 0限制为1-2个工作日，超过就冻结当前假设继续做，后续进入v0.2。
+
+**问题2：v0.1不能只定义DTO。**
+
+Claude的Week 0列了StudentDTO、ApplicationDTO、ApprovalDTO，但缺少错误码、状态机、样例请求响应、mock、契约测试和变更规则。前端和测试真正依赖的是这些可执行产物，不只是字段名。
+
+**问题3：Week 1"无权限校验"会削弱纵向切片。**
+
+最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
+
+**问题4：前端启动时间在文档内不一致。**
+
+Claude前面说"前端Week 4并行"，后面修正建议又写"Week 2：CSV导入 + 前端开始"。这两个说法需要统一。我的建议是：Week 2可以开始前端技术预研和API client封装，但微信小程序主流程页面开发以Week 4为正式启动点。
+
+**问题5：CSV导入仍可能挤压Week 2。**
+
+Claude建议Week 2做CSV导入并让前端开始，但CSV staging、校验报告、upsert、软停用、审计日志本身就是一周以上风险项。Week 2的目标应定义为"CSV导入v1可用"，前端只做轻量准备；不要让Week 2同时承诺完整导入和主流程前端。
+
+**问题6：Postman集合不是足够验收标准。**
+
+Week 1可以交Postman集合，但必须有自动化端到端测试。否则每次契约变化都靠人工点接口，后续Week 2-4会快速失控。
+
+---
+
+## 五、建议形成第二轮共识
+
+建议将执行计划修正为：
+
+| 时间 | 目标 | 交付物 |
+|---|---|---|
+| Week 0 / 1-2工作日 | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog |
+| Week 1 | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 |
+| Week 2 | CSV导入v1 | staging、校验报告、upsert、软停用基础、导入审计基础 |
+| Week 3 | 核心流程补强 + v0.2契约 | 权限细化、异常流、API mock更新、前端启动检查 |
+| Week 4-6 | 微信小程序并行开发 | 登录、申请、审批、查询主流程，使用mock并逐步联调真实后端 |
+| Week 6-7 | 宿舍真实API或降级方案 | 真实Provider、错误分类、缓存/降级、人工证明路径 |
+| Week 8-9 | UAT和完善 | 通知、附件最小可用、异常流修复、导入演练 |
+| Week 10 | 验收演示 | 演示脚本、缺陷修复、文档，不新增功能 |
+
+---
+
+## 直接回答Claude的4个问题
+
+1. **数据契约v0.1应该现在冻结还是Week 1前半？范围最小还是完整？**  
+   现在冻结，限制在1-2个工作日内完成。范围是"最小可执行契约"，不是极简字段，也不是完整未来模型。
+
+2. **Week 1的7-10天工作量是否现实？如何调整？**  
+   如果指7-10人日，在2-3人团队下现实；如果指7-10日历天，不现实。调整方式是Week 0先完成契约，Week 1只做后端最小闭环，推迟CSV完整导入、附件、通知、微信OAuth、真实宿舍API。
+
+3. **前端Week 4并行的前提条件是什么？**  
+   v0.2可消费契约、mock可用、核心API可跑、认证策略固定为演示期薄认证、状态枚举/错误码稳定、API owner和变更机制明确。不要求附件、通知、真实OAuth、真实宿舍API完成。
+
+4. **Claude的Week 0-1拆分方案是否可行？**  
+   方向可行，但必须修正：Week 0要timebox，v0.1要可执行而非字段清单，Week 1不能砍掉最小权限校验，前端启动时间要统一，Week 2不要同时塞满CSV和主流程前端。
+
+---
+
+## Codex第二轮态度
+
+**接受Claude的拆分方向，但不接受把契约冻结推迟到Week 1前半，也不接受Week 1无权限校验的纵向切片。**
+
+下一步不应继续抽象讨论，而应产出两个落地文件：
+
+1. `contract-v0.1.md`或OpenAPI草案：字段、状态、错误码、样例、mock、changelog。
+2. `week-0-1-execution-plan.md`：按天列出责任人、交付物、降级条件和验收测试。
+
+这两个文件完成后，再更新总实施计划。否则直接改10周排期仍然会停留在计划层，不能降低真正的集成风险。
+
+---
+
+**响应人：** Codex  
+**响应时间：** 2026-05-30  
+**讨论状态：** 第二轮回应，建议进入Week 0-1执行共识

diff --git a/docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md b/docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md
new file mode 100644
index 0000000000000000000000000000000000000000..59f264183147f6c565c4403b8c985be2269d3758
--- /dev/null
+++ b/docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md
@@ -0,0 +1,283 @@
+# 下一步工作批判性讨论 - Codex第二轮回应
+
+**文档编号：** 44  
+**响应日期：** 2026-05-30  
+**响应人：** Codex  
+**针对文档：** 43-next-steps-claude-response-round1.md  
+
+---
+
+## 总体结论
+
+Claude的质疑是必要的，尤其是把"Week 0准备"和"Week 1纵向切片"拆开这一点，有助于避免把契约、数据、实现全塞进同一个5天窗口。
+
+但Claude方案仍有几个危险倾向：
+
+1. 把v0.1契约理解成"字段清单"，而不是可执行契约包。
+2. 把前端启动条件抬得过高，可能再次滑回"后端稳定后再前端"的瀑布路径。
+3. Week 1建议"审批API无权限校验"，会让纵向切片失去验证审批链路的意义。
+4. Week 0如果没有明确时长和验收标准，很容易变成新的计划缓冲黑洞。
+
+我的第二轮结论是：
+
+**采用Week 0-1拆分，但Week 0必须是1-2个工作日的timebox；v0.1应现在冻结最小可执行契约，不等到Week 1前半；Week 1只承诺后端端到端最小闭环；前端Week 4启动不要求后端完全稳定，只要求契约、mock和核心路径达到可消费状态。**
+
+---
+
+## 一、数据契约v0.1：现在冻结还是Week 1前半？
+
+### 结论
+
+**应现在冻结v0.1，不应拖到Week 1前半。**
+
+这里的"现在"不是指今天把完整未来模型一次性定死，而是指在正式Week 1编码前，用1-2个工作日完成一个可执行的v0.1基线：
+
+- OpenAPI/接口草案
+- DTO字段和枚举
+- 样例请求/响应
+- 样例CSV或seed fixture
+- 错误码
+- mock响应
+- 契约变更记录
+
+如果拖到Week 1前半才冻结，Week 1后半只剩2-3天，很难完成后端骨架、认证、申请、审批、状态查询和集成测试。Claude把这个拆法描述成"Week 1前半冻结，Week 1后半纵向切片"，本质上还是把Week 1压缩成半周开发，风险比Codex原建议更高。
+
+### v0.1范围：不是"最小字段"，也不是"完整字段"
+
+Claude给出的选项A和选项B都不够准确：
+
+- 选项A过小：只有`student_id, name, application_id, status, approver_id`无法支撑班级映射、角色判断、审批层级、宿舍清退校验和错误处理。
+- 选项B过大：把附件、通知、真实宿舍清退全部字段纳入v0.1，会拖慢Week 1并制造伪稳定。
+
+建议采用**最小可执行契约**：
+
+| 契约块 | v0.1必须包含 | v0.1不必完整包含 |
+|---|---|---|
+| 学生/用户 | student_id、name、role、class_id、is_graduating、graduation_year、active | 微信openid、手机号、完整个人档案 |
+| 班级/辅导员 | class_id、counselor_id、counselor_active | 组织树、多辅导员复杂分配 |
+| 申请 | application_id、student_id、reason、leave_date或checkout_intent、status、created_at | 完整表单扩展字段 |
+| 审批 | step、approver_id、decision、comment、decided_at | 会签、转办、复杂委托 |
+| 宿舍清退 | provider_status、checked_at、blocking_reason、provider_error_code | 真实接口全部响应字段 |
+| 认证 | login_id、role、access_token mock/JWT格式 | 微信OAuth |
+| 错误 | VALIDATION_ERROR、AUTH_REQUIRED、FORBIDDEN、NOT_FOUND、CONFLICT、DORM_BLOCKED、PROVIDER_UNAVAILABLE | 完整国际化错误文案 |
+| CSV/seed | 正常样本 + 边界样本 | 完整生产导入模板 |
+
+也就是说，v0.1的范围应是**能跑通纵向切片且为v0.2留扩展点**，不是"最小字段"和"完整模型"二选一。
+
+### 谁来定义，样例数据从哪里来，mock由谁提供？
+
+建议责任边界如下：
+
+- 后端负责人 owns 契约包：OpenAPI/DTO/错误码/seed schema。
+- 前端负责人 reviews 契约可消费性：字段命名、状态展示、错误展示、登录态。
+- 用户或业务方只确认业务假设：角色、审批链路、宿舍清退是否阻断提交。
+- 样例CSV/fixture先用合成数据，不等待真实样本；真实样本只用于v0.2/v1.0校准。
+- 前端API mock由契约生成或从后端mock server导出，不能由前端手写一套与后端脱节的mock。
+
+---
+
+## 二、Week 1的7-10天工作量是否现实？
+
+### 结论
+
+**7-10人日现实，7-10日历天不现实。**
+
+如果团队是2-3人，且Week 0已经完成v0.1契约，Week 1用5个工作日交付最小后端闭环是有机会的。但前提是严格砍范围，并且明确并行路径。
+
+Claude的拆解把工作量估成7-10天，但没有区分人日和日历天。2名后端/全栈并行时，5个工作日约等于10人日；如果只有1名有效后端，这个目标就必须降级。
+
+### Week 1应该保留什么
+
+Week 1必须保留：
+
+- 后端项目可运行
+- seed/fixture落库
+- 薄认证：学号/工号 + 密码或固定验证码
+- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
+- 申请提交API
+- 辅导员审批API
+- 学工部审批API
+- 状态查询API
+- Dorm Mock参与提交校验
+- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询
+
+这里需要反驳Claude的一点：**"审批API简化版，无权限校验"不应该进入Week 1目标。** 纵向切片的价值正是验证角色、数据、状态机和审批链路能否串起来。可以不做完整RBAC、组织树和复杂权限，但最小角色校验不能砍，否则Week 1只能证明CRUD能跑，不能证明毕业离校审批流程能跑。
+
+### Week 1可以推迟什么
+
+Week 1应推迟：
+
+- 完整CSV staging、upsert、软停用、导入审计
+- 附件上传/下载
+- 通知推送
+- 微信OAuth
+- 完整RBAC权限矩阵
+- 宿舍真实API
+- 审批转办、撤回、驳回后重提等复杂流
+- Postman集合可以有，但不应替代自动化端到端测试
+
+### 调整后的Week 0-1安排
+
+**Week 0 / Day 0-1：契约timebox**
+
+- 冻结v0.1最小可执行契约
+- 生成10-20条seed + 边界fixture
+- 确认审批链路和状态枚举
+- 输出mock响应和错误码
+
+**Week 1 / Day 1-2：可运行骨架**
+
+- Django/API项目启动
+- 基础模型迁移
+- seed命令
+- 薄认证
+
+**Week 1 / Day 3-4：最小流程**
+
+- 申请提交
+- 两级审批
+- 状态查询
+- Dorm Mock阻断/放行
+
+**Week 1 / Day 5：验收硬化**
+
+- 端到端测试
+- 契约测试
+- 修复阻断bug
+- 输出Week 2任务清单
+
+如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
+
+---
+
+## 三、前端Week 4并行的前提条件是什么？
+
+### 结论
+
+**Week 4前端可以启动，但启动条件不应是"后端API完全稳定"。**
+
+Claude列出的前提条件里，"核心流程后端API已实现"和"认证机制已确定"是对的；但"API契约稳定至少v0.2"如果理解成后端字段不再变化，就太重了。前端并行开发需要的是可消费契约，不是生产级冻结。
+
+### Week 4启动的硬门槛
+
+Week 4开始微信小程序主流程开发前，必须满足：
+
+1. 单端范围已确认：首版只做微信小程序，不并行React Native。
+2. OpenAPI/DTO达到v0.2，破坏性变更需要changelog。
+3. 前端mock server或mock JSON可用，覆盖登录、提交、审批、查询、错误态。
+4. 核心后端API在开发环境可跑通：登录、提交、审批、查询。
+5. 认证策略固定为"演示期学号/工号密码，微信OAuth后置"，前端只封装token机制，不等待OAuth。
+6. 状态枚举和错误码稳定，前端能做状态页和错误提示。
+7. 至少有一条端到端后端测试通过，证明mock不是孤立样例。
+8. API owner明确，接口破坏性变更需要当天通知并更新mock。
+
+### 不应作为Week 4启动门槛的事项
+
+以下事项不应阻塞前端启动：
+
+- 附件完整权限
+- 通知推送
+- 宿舍真实API
+- 微信OAuth真实接入
+- 完整CSV导入后台
+- 性能指标
+- 完整生产权限矩阵
+
+如果Week 3后端API还不稳定，是否推迟到Week 5？我的判断是：
+
+- 如果只是字段补充、错误码补充、非破坏性变化，不推迟。
+- 如果登录、提交、审批、查询四个核心端点还没有可运行实现，前端仍可做一周mock驱动开发，但Week 5必须切到真实开发环境联调。
+- 如果v0.2契约仍没有确定状态枚举、角色和核心路径，则不能启动页面开发，应先用1-2天补契约，否则前端会做成静态原型。
+
+---
+
+## 四、Claude的Week 0-1拆分方案是否可行？
+
+### 可行的部分
+
+Claude提出的拆分方向可行：
+
+- Week 0做契约和fixture
+- Week 1做纵向切片
+- Week 1不做附件、通知、微信OAuth
+- Week 10只验收和修复
+
+这比文档40的"Week 1只做数据契约、Week 8-9才做前端"更好。
+
+### 需要修正的问题
+
+**问题1：Week 0不能是2-3天的开放准备期。**
+
+如果Week 0花3天定义契约，再Week 1花5天做切片，总体变成8个工作日。不是不可以，但这应被明确计入计划，而不是把"现在"当免费缓冲。建议Week 0限制为1-2个工作日，超过就冻结当前假设继续做，后续进入v0.2。
+
+**问题2：v0.1不能只定义DTO。**
+
+Claude的Week 0列了StudentDTO、ApplicationDTO、ApprovalDTO，但缺少错误码、状态机、样例请求响应、mock、契约测试和变更规则。前端和测试真正依赖的是这些可执行产物，不只是字段名。
+
+**问题3：Week 1"无权限校验"会削弱纵向切片。**
+
+最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
+
+**问题4：前端启动时间在文档内不一致。**
+
+Claude前面说"前端Week 4并行"，后面修正建议又写"Week 2：CSV导入 + 前端开始"。这两个说法需要统一。我的建议是：Week 2可以开始前端技术预研和API client封装，但微信小程序主流程页面开发以Week 4为正式启动点。
+
+**问题5：CSV导入仍可能挤压Week 2。**
+
+Claude建议Week 2做CSV导入并让前端开始，但CSV staging、校验报告、upsert、软停用、审计日志本身就是一周以上风险项。Week 2的目标应定义为"CSV导入v1可用"，前端只做轻量准备；不要让Week 2同时承诺完整导入和主流程前端。
+
+**问题6：Postman集合不是足够验收标准。**
+
+Week 1可以交Postman集合，但必须有自动化端到端测试。否则每次契约变化都靠人工点接口，后续Week 2-4会快速失控。
+
+---
+
+## 五、建议形成第二轮共识
+
+建议将执行计划修正为：
+
+| 时间 | 目标 | 交付物 |
+|---|---|---|
+| Week 0 / 1-2工作日 | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog |
+| Week 1 | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 |
+| Week 2 | CSV导入v1 | staging、校验报告、upsert、软停用基础、导入审计基础 |
+| Week 3 | 核心流程补强 + v0.2契约 | 权限细化、异常流、API mock更新、前端启动检查 |
+| Week 4-6 | 微信小程序并行开发 | 登录、申请、审批、查询主流程，使用mock并逐步联调真实后端 |
+| Week 6-7 | 宿舍真实API或降级方案 | 真实Provider、错误分类、缓存/降级、人工证明路径 |
+| Week 8-9 | UAT和完善 | 通知、附件最小可用、异常流修复、导入演练 |
+| Week 10 | 验收演示 | 演示脚本、缺陷修复、文档，不新增功能 |
+
+---
+
+## 直接回答Claude的4个问题
+
+1. **数据契约v0.1应该现在冻结还是Week 1前半？范围最小还是完整？**  
+   现在冻结，限制在1-2个工作日内完成。范围是"最小可执行契约"，不是极简字段，也不是完整未来模型。
+
+2. **Week 1的7-10天工作量是否现实？如何调整？**  
+   如果指7-10人日，在2-3人团队下现实；如果指7-10日历天，不现实。调整方式是Week 0先完成契约，Week 1只做后端最小闭环，推迟CSV完整导入、附件、通知、微信OAuth、真实宿舍API。
+
+3. **前端Week 4并行的前提条件是什么？**  
+   v0.2可消费契约、mock可用、核心API可跑、认证策略固定为演示期薄认证、状态枚举/错误码稳定、API owner和变更机制明确。不要求附件、通知、真实OAuth、真实宿舍API完成。
+
+4. **Claude的Week 0-1拆分方案是否可行？**  
+   方向可行，但必须修正：Week 0要timebox，v0.1要可执行而非字段清单，Week 1不能砍掉最小权限校验，前端启动时间要统一，Week 2不要同时塞满CSV和主流程前端。
+
+---
+
+## Codex第二轮态度
+
+**接受Claude的拆分方向，但不接受把契约冻结推迟到Week 1前半，也不接受Week 1无权限校验的纵向切片。**
+
+下一步不应继续抽象讨论，而应产出两个落地文件：
+
+1. `contract-v0.1.md`或OpenAPI草案：字段、状态、错误码、样例、mock、changelog。
+2. `week-0-1-execution-plan.md`：按天列出责任人、交付物、降级条件和验收测试。
+
+这两个文件完成后，再更新总实施计划。否则直接改10周排期仍然会停留在计划层，不能降低真正的集成风险。
+
+---
+
+**响应人：** Codex  
+**响应时间：** 2026-05-30  
+**讨论状态：** 第二轮回应，建议进入Week 0-1执行共识

codex
第二轮回应文档已经写入。现在我会快速校验文件内容和工作区状态，确保编号、标题和重点问题都覆盖到了。
exec
/bin/bash -lc 'rtk git status --short docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
?? docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md
exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 下一步工作批判性讨论 - Codex第二轮回应

**文档编号：** 44  
**响应日期：** 2026-05-30  
**响应人：** Codex  
**针对文档：** 43-next-steps-claude-response-round1.md  

---

## 总体结论

Claude的质疑是必要的，尤其是把"Week 0准备"和"Week 1纵向切片"拆开这一点，有助于避免把契约、数据、实现全塞进同一个5天窗口。

但Claude方案仍有几个危险倾向：

1. 把v0.1契约理解成"字段清单"，而不是可执行契约包。
2. 把前端启动条件抬得过高，可能再次滑回"后端稳定后再前端"的瀑布路径。
3. Week 1建议"审批API无权限校验"，会让纵向切片失去验证审批链路的意义。
4. Week 0如果没有明确时长和验收标准，很容易变成新的计划缓冲黑洞。

我的第二轮结论是：

**采用Week 0-1拆分，但Week 0必须是1-2个工作日的timebox；v0.1应现在冻结最小可执行契约，不等到Week 1前半；Week 1只承诺后端端到端最小闭环；前端Week 4启动不要求后端完全稳定，只要求契约、mock和核心路径达到可消费状态。**

---

## 一、数据契约v0.1：现在冻结还是Week 1前半？

### 结论

**应现在冻结v0.1，不应拖到Week 1前半。**

这里的"现在"不是指今天把完整未来模型一次性定死，而是指在正式Week 1编码前，用1-2个工作日完成一个可执行的v0.1基线：

- OpenAPI/接口草案
- DTO字段和枚举
- 样例请求/响应
- 样例CSV或seed fixture
- 错误码
- mock响应
- 契约变更记录

如果拖到Week 1前半才冻结，Week 1后半只剩2-3天，很难完成后端骨架、认证、申请、审批、状态查询和集成测试。Claude把这个拆法描述成"Week 1前半冻结，Week 1后半纵向切片"，本质上还是把Week 1压缩成半周开发，风险比Codex原建议更高。

### v0.1范围：不是"最小字段"，也不是"完整字段"

Claude给出的选项A和选项B都不够准确：

- 选项A过小：只有`student_id, name, application_id, status, approver_id`无法支撑班级映射、角色判断、审批层级、宿舍清退校验和错误处理。
- 选项B过大：把附件、通知、真实宿舍清退全部字段纳入v0.1，会拖慢Week 1并制造伪稳定。

建议采用**最小可执行契约**：

| 契约块 | v0.1必须包含 | v0.1不必完整包含 |
|---|---|---|
| 学生/用户 | student_id、name、role、class_id、is_graduating、graduation_year、active | 微信openid、手机号、完整个人档案 |
| 班级/辅导员 | class_id、counselor_id、counselor_active | 组织树、多辅导员复杂分配 |
| 申请 | application_id、student_id、reason、leave_date或checkout_intent、status、created_at | 完整表单扩展字段 |
| 审批 | step、approver_id、decision、comment、decided_at | 会签、转办、复杂委托 |
| 宿舍清退 | provider_status、checked_at、blocking_reason、provider_error_code | 真实接口全部响应字段 |
| 认证 | login_id、role、access_token mock/JWT格式 | 微信OAuth |
| 错误 | VALIDATION_ERROR、AUTH_REQUIRED、FORBIDDEN、NOT_FOUND、CONFLICT、DORM_BLOCKED、PROVIDER_UNAVAILABLE | 完整国际化错误文案 |
| CSV/seed | 正常样本 + 边界样本 | 完整生产导入模板 |

也就是说，v0.1的范围应是**能跑通纵向切片且为v0.2留扩展点**，不是"最小字段"和"完整模型"二选一。

### 谁来定义，样例数据从哪里来，mock由谁提供？

建议责任边界如下：

- 后端负责人 owns 契约包：OpenAPI/DTO/错误码/seed schema。
- 前端负责人 reviews 契约可消费性：字段命名、状态展示、错误展示、登录态。
- 用户或业务方只确认业务假设：角色、审批链路、宿舍清退是否阻断提交。
- 样例CSV/fixture先用合成数据，不等待真实样本；真实样本只用于v0.2/v1.0校准。
- 前端API mock由契约生成或从后端mock server导出，不能由前端手写一套与后端脱节的mock。

---

## 二、Week 1的7-10天工作量是否现实？

### 结论

**7-10人日现实，7-10日历天不现实。**

如果团队是2-3人，且Week 0已经完成v0.1契约，Week 1用5个工作日交付最小后端闭环是有机会的。但前提是严格砍范围，并且明确并行路径。

Claude的拆解把工作量估成7-10天，但没有区分人日和日历天。2名后端/全栈并行时，5个工作日约等于10人日；如果只有1名有效后端，这个目标就必须降级。

### Week 1应该保留什么

Week 1必须保留：

- 后端项目可运行
- seed/fixture落库
- 薄认证：学号/工号 + 密码或固定验证码
- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
- 申请提交API
- 辅导员审批API
- 学工部审批API
- 状态查询API
- Dorm Mock参与提交校验
- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询

这里需要反驳Claude的一点：**"审批API简化版，无权限校验"不应该进入Week 1目标。** 纵向切片的价值正是验证角色、数据、状态机和审批链路能否串起来。可以不做完整RBAC、组织树和复杂权限，但最小角色校验不能砍，否则Week 1只能证明CRUD能跑，不能证明毕业离校审批流程能跑。

### Week 1可以推迟什么

Week 1应推迟：

- 完整CSV staging、upsert、软停用、导入审计
- 附件上传/下载
- 通知推送
- 微信OAuth
- 完整RBAC权限矩阵
- 宿舍真实API
- 审批转办、撤回、驳回后重提等复杂流
- Postman集合可以有，但不应替代自动化端到端测试

### 调整后的Week 0-1安排

**Week 0 / Day 0-1：契约timebox**

- 冻结v0.1最小可执行契约
- 生成10-20条seed + 边界fixture
- 确认审批链路和状态枚举
- 输出mock响应和错误码

**Week 1 / Day 1-2：可运行骨架**

- Django/API项目启动
- 基础模型迁移
- seed命令
- 薄认证

**Week 1 / Day 3-4：最小流程**

- 申请提交
- 两级审批
- 状态查询
- Dorm Mock阻断/放行

**Week 1 / Day 5：验收硬化**

- 端到端测试
- 契约测试
- 修复阻断bug
- 输出Week 2任务清单

如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。

---

## 三、前端Week 4并行的前提条件是什么？

### 结论

**Week 4前端可以启动，但启动条件不应是"后端API完全稳定"。**

Claude列出的前提条件里，"核心流程后端API已实现"和"认证机制已确定"是对的；但"API契约稳定至少v0.2"如果理解成后端字段不再变化，就太重了。前端并行开发需要的是可消费契约，不是生产级冻结。

### Week 4启动的硬门槛

Week 4开始微信小程序主流程开发前，必须满足：

1. 单端范围已确认：首版只做微信小程序，不并行React Native。
2. OpenAPI/DTO达到v0.2，破坏性变更需要changelog。
3. 前端mock server或mock JSON可用，覆盖登录、提交、审批、查询、错误态。
4. 核心后端API在开发环境可跑通：登录、提交、审批、查询。
5. 认证策略固定为"演示期学号/工号密码，微信OAuth后置"，前端只封装token机制，不等待OAuth。
6. 状态枚举和错误码稳定，前端能做状态页和错误提示。
7. 至少有一条端到端后端测试通过，证明mock不是孤立样例。
8. API owner明确，接口破坏性变更需要当天通知并更新mock。

### 不应作为Week 4启动门槛的事项

以下事项不应阻塞前端启动：

- 附件完整权限
- 通知推送
- 宿舍真实API
- 微信OAuth真实接入
- 完整CSV导入后台
- 性能指标
- 完整生产权限矩阵

如果Week 3后端API还不稳定，是否推迟到Week 5？我的判断是：

- 如果只是字段补充、错误码补充、非破坏性变化，不推迟。
- 如果登录、提交、审批、查询四个核心端点还没有可运行实现，前端仍可做一周mock驱动开发，但Week 5必须切到真实开发环境联调。
- 如果v0.2契约仍没有确定状态枚举、角色和核心路径，则不能启动页面开发，应先用1-2天补契约，否则前端会做成静态原型。

---

## 四、Claude的Week 0-1拆分方案是否可行？

### 可行的部分

Claude提出的拆分方向可行：

- Week 0做契约和fixture
- Week 1做纵向切片
- Week 1不做附件、通知、微信OAuth
- Week 10只验收和修复

这比文档40的"Week 1只做数据契约、Week 8-9才做前端"更好。

### 需要修正的问题

**问题1：Week 0不能是2-3天的开放准备期。**

如果Week 0花3天定义契约，再Week 1花5天做切片，总体变成8个工作日。不是不可以，但这应被明确计入计划，而不是把"现在"当免费缓冲。建议Week 0限制为1-2个工作日，超过就冻结当前假设继续做，后续进入v0.2。

**问题2：v0.1不能只定义DTO。**

Claude的Week 0列了StudentDTO、ApplicationDTO、ApprovalDTO，但缺少错误码、状态机、样例请求响应、mock、契约测试和变更规则。前端和测试真正依赖的是这些可执行产物，不只是字段名。

**问题3：Week 1"无权限校验"会削弱纵向切片。**

最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。

**问题4：前端启动时间在文档内不一致。**

Claude前面说"前端Week 4并行"，后面修正建议又写"Week 2：CSV导入 + 前端开始"。这两个说法需要统一。我的建议是：Week 2可以开始前端技术预研和API client封装，但微信小程序主流程页面开发以Week 4为正式启动点。

**问题5：CSV导入仍可能挤压Week 2。**

Claude建议Week 2做CSV导入并让前端开始，但CSV staging、校验报告、upsert、软停用、审计日志本身就是一周以上风险项。Week 2的目标应定义为"CSV导入v1可用"，前端只做轻量准备；不要让Week 2同时承诺完整导入和主流程前端。

**问题6：Postman集合不是足够验收标准。**

Week 1可以交Postman集合，但必须有自动化端到端测试。否则每次契约变化都靠人工点接口，后续Week 2-4会快速失控。

---

## 五、建议形成第二轮共识

建议将执行计划修正为：

| 时间 | 目标 | 交付物 |
|---|---|---|
| Week 0 / 1-2工作日 | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog |
| Week 1 | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 |
| Week 2 | CSV导入v1 | staging、校验报告、upsert、软停用基础、导入审计基础 |
| Week 3 | 核心流程补强 + v0.2契约 | 权限细化、异常流、API mock更新、前端启动检查 |
| Week 4-6 | 微信小程序并行开发 | 登录、申请、审批、查询主流程，使用mock并逐步联调真实后端 |
| Week 6-7 | 宿舍真实API或降级方案 | 真实Provider、错误分类、缓存/降级、人工证明路径 |
| Week 8-9 | UAT和完善 | 通知、附件最小可用、异常流修复、导入演练 |
| Week 10 | 验收演示 | 演示脚本、缺陷修复、文档，不新增功能 |

---

## 直接回答Claude的4个问题

1. **数据契约v0.1应该现在冻结还是Week 1前半？范围最小还是完整？**  
   现在冻结，限制在1-2个工作日内完成。范围是"最小可执行契约"，不是极简字段，也不是完整未来模型。

2. **Week 1的7-10天工作量是否现实？如何调整？**  
   如果指7-10人日，在2-3人团队下现实；如果指7-10日历天，不现实。调整方式是Week 0先完成契约，Week 1只做后端最小闭环，推迟CSV完整导入、附件、通知、微信OAuth、真实宿舍API。

3. **前端Week 4并行的前提条件是什么？**  

exec
/bin/bash -lc "rtk sed -n '261,520p' docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   v0.2可消费契约、mock可用、核心API可跑、认证策略固定为演示期薄认证、状态枚举/错误码稳定、API owner和变更机制明确。不要求附件、通知、真实OAuth、真实宿舍API完成。

4. **Claude的Week 0-1拆分方案是否可行？**  
   方向可行，但必须修正：Week 0要timebox，v0.1要可执行而非字段清单，Week 1不能砍掉最小权限校验，前端启动时间要统一，Week 2不要同时塞满CSV和主流程前端。

---

## Codex第二轮态度

**接受Claude的拆分方向，但不接受把契约冻结推迟到Week 1前半，也不接受Week 1无权限校验的纵向切片。**

下一步不应继续抽象讨论，而应产出两个落地文件：

1. `contract-v0.1.md`或OpenAPI草案：字段、状态、错误码、样例、mock、changelog。
2. `week-0-1-execution-plan.md`：按天列出责任人、交付物、降级条件和验收测试。

这两个文件完成后，再更新总实施计划。否则直接改10周排期仍然会停留在计划层，不能降低真正的集成风险。

---

**响应人：** Codex  
**响应时间：** 2026-05-30  
**讨论状态：** 第二轮回应，建议进入Week 0-1执行共识

diff --git a/docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md b/docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md
new file mode 100644
index 0000000000000000000000000000000000000000..59f264183147f6c565c4403b8c985be2269d3758
--- /dev/null
+++ b/docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md
@@ -0,0 +1,283 @@
+# 下一步工作批判性讨论 - Codex第二轮回应
+
+**文档编号：** 44  
+**响应日期：** 2026-05-30  
+**响应人：** Codex  
+**针对文档：** 43-next-steps-claude-response-round1.md  
+
+---
+
+## 总体结论
+
+Claude的质疑是必要的，尤其是把"Week 0准备"和"Week 1纵向切片"拆开这一点，有助于避免把契约、数据、实现全塞进同一个5天窗口。
+
+但Claude方案仍有几个危险倾向：
+
+1. 把v0.1契约理解成"字段清单"，而不是可执行契约包。
+2. 把前端启动条件抬得过高，可能再次滑回"后端稳定后再前端"的瀑布路径。
+3. Week 1建议"审批API无权限校验"，会让纵向切片失去验证审批链路的意义。
+4. Week 0如果没有明确时长和验收标准，很容易变成新的计划缓冲黑洞。
+
+我的第二轮结论是：
+
+**采用Week 0-1拆分，但Week 0必须是1-2个工作日的timebox；v0.1应现在冻结最小可执行契约，不等到Week 1前半；Week 1只承诺后端端到端最小闭环；前端Week 4启动不要求后端完全稳定，只要求契约、mock和核心路径达到可消费状态。**
+
+---
+
+## 一、数据契约v0.1：现在冻结还是Week 1前半？
+
+### 结论
+
+**应现在冻结v0.1，不应拖到Week 1前半。**
+
+这里的"现在"不是指今天把完整未来模型一次性定死，而是指在正式Week 1编码前，用1-2个工作日完成一个可执行的v0.1基线：
+
+- OpenAPI/接口草案
+- DTO字段和枚举
+- 样例请求/响应
+- 样例CSV或seed fixture
+- 错误码
+- mock响应
+- 契约变更记录
+
+如果拖到Week 1前半才冻结，Week 1后半只剩2-3天，很难完成后端骨架、认证、申请、审批、状态查询和集成测试。Claude把这个拆法描述成"Week 1前半冻结，Week 1后半纵向切片"，本质上还是把Week 1压缩成半周开发，风险比Codex原建议更高。
+
+### v0.1范围：不是"最小字段"，也不是"完整字段"
+
+Claude给出的选项A和选项B都不够准确：
+
+- 选项A过小：只有`student_id, name, application_id, status, approver_id`无法支撑班级映射、角色判断、审批层级、宿舍清退校验和错误处理。
+- 选项B过大：把附件、通知、真实宿舍清退全部字段纳入v0.1，会拖慢Week 1并制造伪稳定。
+
+建议采用**最小可执行契约**：
+
+| 契约块 | v0.1必须包含 | v0.1不必完整包含 |
+|---|---|---|
+| 学生/用户 | student_id、name、role、class_id、is_graduating、graduation_year、active | 微信openid、手机号、完整个人档案 |
+| 班级/辅导员 | class_id、counselor_id、counselor_active | 组织树、多辅导员复杂分配 |
+| 申请 | application_id、student_id、reason、leave_date或checkout_intent、status、created_at | 完整表单扩展字段 |
+| 审批 | step、approver_id、decision、comment、decided_at | 会签、转办、复杂委托 |
+| 宿舍清退 | provider_status、checked_at、blocking_reason、provider_error_code | 真实接口全部响应字段 |
+| 认证 | login_id、role、access_token mock/JWT格式 | 微信OAuth |
+| 错误 | VALIDATION_ERROR、AUTH_REQUIRED、FORBIDDEN、NOT_FOUND、CONFLICT、DORM_BLOCKED、PROVIDER_UNAVAILABLE | 完整国际化错误文案 |
+| CSV/seed | 正常样本 + 边界样本 | 完整生产导入模板 |
+
+也就是说，v0.1的范围应是**能跑通纵向切片且为v0.2留扩展点**，不是"最小字段"和"完整模型"二选一。
+
+### 谁来定义，样例数据从哪里来，mock由谁提供？
+
+建议责任边界如下：
+
+- 后端负责人 owns 契约包：OpenAPI/DTO/错误码/seed schema。
+- 前端负责人 reviews 契约可消费性：字段命名、状态展示、错误展示、登录态。
+- 用户或业务方只确认业务假设：角色、审批链路、宿舍清退是否阻断提交。
+- 样例CSV/fixture先用合成数据，不等待真实样本；真实样本只用于v0.2/v1.0校准。
+- 前端API mock由契约生成或从后端mock server导出，不能由前端手写一套与后端脱节的mock。
+
+---
+
+## 二、Week 1的7-10天工作量是否现实？
+
+### 结论
+
+**7-10人日现实，7-10日历天不现实。**
+
+如果团队是2-3人，且Week 0已经完成v0.1契约，Week 1用5个工作日交付最小后端闭环是有机会的。但前提是严格砍范围，并且明确并行路径。
+
+Claude的拆解把工作量估成7-10天，但没有区分人日和日历天。2名后端/全栈并行时，5个工作日约等于10人日；如果只有1名有效后端，这个目标就必须降级。
+
+### Week 1应该保留什么
+
+Week 1必须保留：
+
+- 后端项目可运行
+- seed/fixture落库
+- 薄认证：学号/工号 + 密码或固定验证码
+- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
+- 申请提交API
+- 辅导员审批API
+- 学工部审批API
+- 状态查询API
+- Dorm Mock参与提交校验
+- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询
+
+这里需要反驳Claude的一点：**"审批API简化版，无权限校验"不应该进入Week 1目标。** 纵向切片的价值正是验证角色、数据、状态机和审批链路能否串起来。可以不做完整RBAC、组织树和复杂权限，但最小角色校验不能砍，否则Week 1只能证明CRUD能跑，不能证明毕业离校审批流程能跑。
+
+### Week 1可以推迟什么
+
+Week 1应推迟：
+
+- 完整CSV staging、upsert、软停用、导入审计
+- 附件上传/下载
+- 通知推送
+- 微信OAuth
+- 完整RBAC权限矩阵
+- 宿舍真实API
+- 审批转办、撤回、驳回后重提等复杂流
+- Postman集合可以有，但不应替代自动化端到端测试
+
+### 调整后的Week 0-1安排
+
+**Week 0 / Day 0-1：契约timebox**
+
+- 冻结v0.1最小可执行契约
+- 生成10-20条seed + 边界fixture
+- 确认审批链路和状态枚举
+- 输出mock响应和错误码
+
+**Week 1 / Day 1-2：可运行骨架**
+
+- Django/API项目启动
+- 基础模型迁移
+- seed命令
+- 薄认证
+
+**Week 1 / Day 3-4：最小流程**
+
+- 申请提交
+- 两级审批
+- 状态查询
+- Dorm Mock阻断/放行
+
+**Week 1 / Day 5：验收硬化**
+
+- 端到端测试
+- 契约测试
+- 修复阻断bug
+- 输出Week 2任务清单
+
+如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
+
+---
+
+## 三、前端Week 4并行的前提条件是什么？
+
+### 结论
+
+**Week 4前端可以启动，但启动条件不应是"后端API完全稳定"。**
+
+Claude列出的前提条件里，"核心流程后端API已实现"和"认证机制已确定"是对的；但"API契约稳定至少v0.2"如果理解成后端字段不再变化，就太重了。前端并行开发需要的是可消费契约，不是生产级冻结。
+
+### Week 4启动的硬门槛
+
+Week 4开始微信小程序主流程开发前，必须满足：
+
+1. 单端范围已确认：首版只做微信小程序，不并行React Native。
+2. OpenAPI/DTO达到v0.2，破坏性变更需要changelog。
+3. 前端mock server或mock JSON可用，覆盖登录、提交、审批、查询、错误态。
+4. 核心后端API在开发环境可跑通：登录、提交、审批、查询。
+5. 认证策略固定为"演示期学号/工号密码，微信OAuth后置"，前端只封装token机制，不等待OAuth。
+6. 状态枚举和错误码稳定，前端能做状态页和错误提示。
+7. 至少有一条端到端后端测试通过，证明mock不是孤立样例。
+8. API owner明确，接口破坏性变更需要当天通知并更新mock。
+
+### 不应作为Week 4启动门槛的事项
+
+以下事项不应阻塞前端启动：
+
+- 附件完整权限
+- 通知推送
+- 宿舍真实API
+- 微信OAuth真实接入
+- 完整CSV导入后台
+- 性能指标
+- 完整生产权限矩阵
+
+如果Week 3后端API还不稳定，是否推迟到Week 5？我的判断是：
+
+- 如果只是字段补充、错误码补充、非破坏性变化，不推迟。
+- 如果登录、提交、审批、查询四个核心端点还没有可运行实现，前端仍可做一周mock驱动开发，但Week 5必须切到真实开发环境联调。
+- 如果v0.2契约仍没有确定状态枚举、角色和核心路径，则不能启动页面开发，应先用1-2天补契约，否则前端会做成静态原型。
+
+---
+
+## 四、Claude的Week 0-1拆分方案是否可行？
+
+### 可行的部分
+
+Claude提出的拆分方向可行：
+
+- Week 0做契约和fixture
+- Week 1做纵向切片
+- Week 1不做附件、通知、微信OAuth
+- Week 10只验收和修复
+
+这比文档40的"Week 1只做数据契约、Week 8-9才做前端"更好。
+
+### 需要修正的问题
+
+**问题1：Week 0不能是2-3天的开放准备期。**
+
+如果Week 0花3天定义契约，再Week 1花5天做切片，总体变成8个工作日。不是不可以，但这应被明确计入计划，而不是把"现在"当免费缓冲。建议Week 0限制为1-2个工作日，超过就冻结当前假设继续做，后续进入v0.2。
+
+**问题2：v0.1不能只定义DTO。**
+
+Claude的Week 0列了StudentDTO、ApplicationDTO、ApprovalDTO，但缺少错误码、状态机、样例请求响应、mock、契约测试和变更规则。前端和测试真正依赖的是这些可执行产物，不只是字段名。
+
+**问题3：Week 1"无权限校验"会削弱纵向切片。**
+
+最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
+
+**问题4：前端启动时间在文档内不一致。**
+
+Claude前面说"前端Week 4并行"，后面修正建议又写"Week 2：CSV导入 + 前端开始"。这两个说法需要统一。我的建议是：Week 2可以开始前端技术预研和API client封装，但微信小程序主流程页面开发以Week 4为正式启动点。
+
+**问题5：CSV导入仍可能挤压Week 2。**
+
+Claude建议Week 2做CSV导入并让前端开始，但CSV staging、校验报告、upsert、软停用、审计日志本身就是一周以上风险项。Week 2的目标应定义为"CSV导入v1可用"，前端只做轻量准备；不要让Week 2同时承诺完整导入和主流程前端。
+
+**问题6：Postman集合不是足够验收标准。**
+
+Week 1可以交Postman集合，但必须有自动化端到端测试。否则每次契约变化都靠人工点接口，后续Week 2-4会快速失控。
+
+---
+
+## 五、建议形成第二轮共识
+
+建议将执行计划修正为：
+
+| 时间 | 目标 | 交付物 |
+|---|---|---|
+| Week 0 / 1-2工作日 | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog |
+| Week 1 | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 |
+| Week 2 | CSV导入v1 | staging、校验报告、upsert、软停用基础、导入审计基础 |
+| Week 3 | 核心流程补强 + v0.2契约 | 权限细化、异常流、API mock更新、前端启动检查 |
+| Week 4-6 | 微信小程序并行开发 | 登录、申请、审批、查询主流程，使用mock并逐步联调真实后端 |
+| Week 6-7 | 宿舍真实API或降级方案 | 真实Provider、错误分类、缓存/降级、人工证明路径 |
+| Week 8-9 | UAT和完善 | 通知、附件最小可用、异常流修复、导入演练 |
+| Week 10 | 验收演示 | 演示脚本、缺陷修复、文档，不新增功能 |
+
+---
+
+## 直接回答Claude的4个问题
+
+1. **数据契约v0.1应该现在冻结还是Week 1前半？范围最小还是完整？**  
+   现在冻结，限制在1-2个工作日内完成。范围是"最小可执行契约"，不是极简字段，也不是完整未来模型。
+
+2. **Week 1的7-10天工作量是否现实？如何调整？**  
+   如果指7-10人日，在2-3人团队下现实；如果指7-10日历天，不现实。调整方式是Week 0先完成契约，Week 1只做后端最小闭环，推迟CSV完整导入、附件、通知、微信OAuth、真实宿舍API。
+
+3. **前端Week 4并行的前提条件是什么？**  
+   v0.2可消费契约、mock可用、核心API可跑、认证策略固定为演示期薄认证、状态枚举/错误码稳定、API owner和变更机制明确。不要求附件、通知、真实OAuth、真实宿舍API完成。
+
+4. **Claude的Week 0-1拆分方案是否可行？**  
+   方向可行，但必须修正：Week 0要timebox，v0.1要可执行而非字段清单，Week 1不能砍掉最小权限校验，前端启动时间要统一，Week 2不要同时塞满CSV和主流程前端。
+
+---
+
+## Codex第二轮态度
+
+**接受Claude的拆分方向，但不接受把契约冻结推迟到Week 1前半，也不接受Week 1无权限校验的纵向切片。**
+
+下一步不应继续抽象讨论，而应产出两个落地文件：
+
+1. `contract-v0.1.md`或OpenAPI草案：字段、状态、错误码、样例、mock、changelog。
+2. `week-0-1-execution-plan.md`：按天列出责任人、交付物、降级条件和验收测试。
+
+这两个文件完成后，再更新总实施计划。否则直接改10周排期仍然会停留在计划层，不能降低真正的集成风险。
+
+---
+
+**响应人：** Codex  
+**响应时间：** 2026-05-30  
+**讨论状态：** 第二轮回应，建议进入Week 0-1执行共识

codex
已完成第二轮回应，新增文档：

[44-next-steps-codex-response-round2.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md)

核心立场已覆盖你指定的4点：

- v0.1应现在以1-2个工作日冻结为“最小可执行契约”，不是Week 1前半，也不是极简字段或完整模型。
- Week 1的7-10“人日”现实，7-10“日历天”不现实；需砍到后端最小闭环。
- 前端Week 4启动的前提是v0.2可消费契约、mock、核心API、薄认证策略和变更机制，不要求后端生产级稳定。
- Claude的Week 0-1拆分方向可行，但存在Week 0膨胀、v0.1过于字段化、Week 1砍权限校验、前端启动时间不一致、Week 2过载等问题。

未运行测试，因为本次只新增讨论文档。
diff --git a/docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md b/docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md
new file mode 100644
index 0000000000000000000000000000000000000000..59f264183147f6c565c4403b8c985be2269d3758
--- /dev/null
+++ b/docs/discussions/codex-review-2026-05-30/44-next-steps-codex-response-round2.md
@@ -0,0 +1,283 @@
+# 下一步工作批判性讨论 - Codex第二轮回应
+
+**文档编号：** 44  
+**响应日期：** 2026-05-30  
+**响应人：** Codex  
+**针对文档：** 43-next-steps-claude-response-round1.md  
+
+---
+
+## 总体结论
+
+Claude的质疑是必要的，尤其是把"Week 0准备"和"Week 1纵向切片"拆开这一点，有助于避免把契约、数据、实现全塞进同一个5天窗口。
+
+但Claude方案仍有几个危险倾向：
+
+1. 把v0.1契约理解成"字段清单"，而不是可执行契约包。
+2. 把前端启动条件抬得过高，可能再次滑回"后端稳定后再前端"的瀑布路径。
+3. Week 1建议"审批API无权限校验"，会让纵向切片失去验证审批链路的意义。
+4. Week 0如果没有明确时长和验收标准，很容易变成新的计划缓冲黑洞。
+
+我的第二轮结论是：
+
+**采用Week 0-1拆分，但Week 0必须是1-2个工作日的timebox；v0.1应现在冻结最小可执行契约，不等到Week 1前半；Week 1只承诺后端端到端最小闭环；前端Week 4启动不要求后端完全稳定，只要求契约、mock和核心路径达到可消费状态。**
+
+---
+
+## 一、数据契约v0.1：现在冻结还是Week 1前半？
+
+### 结论
+
+**应现在冻结v0.1，不应拖到Week 1前半。**
+
+这里的"现在"不是指今天把完整未来模型一次性定死，而是指在正式Week 1编码前，用1-2个工作日完成一个可执行的v0.1基线：
+
+- OpenAPI/接口草案
+- DTO字段和枚举
+- 样例请求/响应
+- 样例CSV或seed fixture
+- 错误码
+- mock响应
+- 契约变更记录
+
+如果拖到Week 1前半才冻结，Week 1后半只剩2-3天，很难完成后端骨架、认证、申请、审批、状态查询和集成测试。Claude把这个拆法描述成"Week 1前半冻结，Week 1后半纵向切片"，本质上还是把Week 1压缩成半周开发，风险比Codex原建议更高。
+
+### v0.1范围：不是"最小字段"，也不是"完整字段"
+
+Claude给出的选项A和选项B都不够准确：
+
+- 选项A过小：只有`student_id, name, application_id, status, approver_id`无法支撑班级映射、角色判断、审批层级、宿舍清退校验和错误处理。
+- 选项B过大：把附件、通知、真实宿舍清退全部字段纳入v0.1，会拖慢Week 1并制造伪稳定。
+
+建议采用**最小可执行契约**：
+
+| 契约块 | v0.1必须包含 | v0.1不必完整包含 |
+|---|---|---|
+| 学生/用户 | student_id、name、role、class_id、is_graduating、graduation_year、active | 微信openid、手机号、完整个人档案 |
+| 班级/辅导员 | class_id、counselor_id、counselor_active | 组织树、多辅导员复杂分配 |
+| 申请 | application_id、student_id、reason、leave_date或checkout_intent、status、created_at | 完整表单扩展字段 |
+| 审批 | step、approver_id、decision、comment、decided_at | 会签、转办、复杂委托 |
+| 宿舍清退 | provider_status、checked_at、blocking_reason、provider_error_code | 真实接口全部响应字段 |
+| 认证 | login_id、role、access_token mock/JWT格式 | 微信OAuth |
+| 错误 | VALIDATION_ERROR、AUTH_REQUIRED、FORBIDDEN、NOT_FOUND、CONFLICT、DORM_BLOCKED、PROVIDER_UNAVAILABLE | 完整国际化错误文案 |
+| CSV/seed | 正常样本 + 边界样本 | 完整生产导入模板 |
+
+也就是说，v0.1的范围应是**能跑通纵向切片且为v0.2留扩展点**，不是"最小字段"和"完整模型"二选一。
+
+### 谁来定义，样例数据从哪里来，mock由谁提供？
+
+建议责任边界如下：
+
+- 后端负责人 owns 契约包：OpenAPI/DTO/错误码/seed schema。
+- 前端负责人 reviews 契约可消费性：字段命名、状态展示、错误展示、登录态。
+- 用户或业务方只确认业务假设：角色、审批链路、宿舍清退是否阻断提交。
+- 样例CSV/fixture先用合成数据，不等待真实样本；真实样本只用于v0.2/v1.0校准。
+- 前端API mock由契约生成或从后端mock server导出，不能由前端手写一套与后端脱节的mock。
+
+---
+
+## 二、Week 1的7-10天工作量是否现实？
+
+### 结论
+
+**7-10人日现实，7-10日历天不现实。**
+
+如果团队是2-3人，且Week 0已经完成v0.1契约，Week 1用5个工作日交付最小后端闭环是有机会的。但前提是严格砍范围，并且明确并行路径。
+
+Claude的拆解把工作量估成7-10天，但没有区分人日和日历天。2名后端/全栈并行时，5个工作日约等于10人日；如果只有1名有效后端，这个目标就必须降级。
+
+### Week 1应该保留什么
+
+Week 1必须保留：
+
+- 后端项目可运行
+- seed/fixture落库
+- 薄认证：学号/工号 + 密码或固定验证码
+- 最小角色校验：学生只能提交和查看自己的申请，辅导员/学工部只能执行对应审批动作
+- 申请提交API
+- 辅导员审批API
+- 学工部审批API
+- 状态查询API
+- Dorm Mock参与提交校验
+- 一条端到端测试：登录 -> 提交 -> 辅导员审批 -> 学工部审批 -> 查询
+
+这里需要反驳Claude的一点：**"审批API简化版，无权限校验"不应该进入Week 1目标。** 纵向切片的价值正是验证角色、数据、状态机和审批链路能否串起来。可以不做完整RBAC、组织树和复杂权限，但最小角色校验不能砍，否则Week 1只能证明CRUD能跑，不能证明毕业离校审批流程能跑。
+
+### Week 1可以推迟什么
+
+Week 1应推迟：
+
+- 完整CSV staging、upsert、软停用、导入审计
+- 附件上传/下载
+- 通知推送
+- 微信OAuth
+- 完整RBAC权限矩阵
+- 宿舍真实API
+- 审批转办、撤回、驳回后重提等复杂流
+- Postman集合可以有，但不应替代自动化端到端测试
+
+### 调整后的Week 0-1安排
+
+**Week 0 / Day 0-1：契约timebox**
+
+- 冻结v0.1最小可执行契约
+- 生成10-20条seed + 边界fixture
+- 确认审批链路和状态枚举
+- 输出mock响应和错误码
+
+**Week 1 / Day 1-2：可运行骨架**
+
+- Django/API项目启动
+- 基础模型迁移
+- seed命令
+- 薄认证
+
+**Week 1 / Day 3-4：最小流程**
+
+- 申请提交
+- 两级审批
+- 状态查询
+- Dorm Mock阻断/放行
+
+**Week 1 / Day 5：验收硬化**
+
+- 端到端测试
+- 契约测试
+- 修复阻断bug
+- 输出Week 2任务清单
+
+如果Day 3结束仍没有申请提交API和状态查询API，应立即降级：只保留"学生提交 -> 辅导员审批 -> 查询"，把学工部审批推到Week 2开头。但这个降级必须显式记录，不能静默延期。
+
+---
+
+## 三、前端Week 4并行的前提条件是什么？
+
+### 结论
+
+**Week 4前端可以启动，但启动条件不应是"后端API完全稳定"。**
+
+Claude列出的前提条件里，"核心流程后端API已实现"和"认证机制已确定"是对的；但"API契约稳定至少v0.2"如果理解成后端字段不再变化，就太重了。前端并行开发需要的是可消费契约，不是生产级冻结。
+
+### Week 4启动的硬门槛
+
+Week 4开始微信小程序主流程开发前，必须满足：
+
+1. 单端范围已确认：首版只做微信小程序，不并行React Native。
+2. OpenAPI/DTO达到v0.2，破坏性变更需要changelog。
+3. 前端mock server或mock JSON可用，覆盖登录、提交、审批、查询、错误态。
+4. 核心后端API在开发环境可跑通：登录、提交、审批、查询。
+5. 认证策略固定为"演示期学号/工号密码，微信OAuth后置"，前端只封装token机制，不等待OAuth。
+6. 状态枚举和错误码稳定，前端能做状态页和错误提示。
+7. 至少有一条端到端后端测试通过，证明mock不是孤立样例。
+8. API owner明确，接口破坏性变更需要当天通知并更新mock。
+
+### 不应作为Week 4启动门槛的事项
+
+以下事项不应阻塞前端启动：
+
+- 附件完整权限
+- 通知推送
+- 宿舍真实API
+- 微信OAuth真实接入
+- 完整CSV导入后台
+- 性能指标
+- 完整生产权限矩阵
+
+如果Week 3后端API还不稳定，是否推迟到Week 5？我的判断是：
+
+- 如果只是字段补充、错误码补充、非破坏性变化，不推迟。
+- 如果登录、提交、审批、查询四个核心端点还没有可运行实现，前端仍可做一周mock驱动开发，但Week 5必须切到真实开发环境联调。
+- 如果v0.2契约仍没有确定状态枚举、角色和核心路径，则不能启动页面开发，应先用1-2天补契约，否则前端会做成静态原型。
+
+---
+
+## 四、Claude的Week 0-1拆分方案是否可行？
+
+### 可行的部分
+
+Claude提出的拆分方向可行：
+
+- Week 0做契约和fixture
+- Week 1做纵向切片
+- Week 1不做附件、通知、微信OAuth
+- Week 10只验收和修复
+
+这比文档40的"Week 1只做数据契约、Week 8-9才做前端"更好。
+
+### 需要修正的问题
+
+**问题1：Week 0不能是2-3天的开放准备期。**
+
+如果Week 0花3天定义契约，再Week 1花5天做切片，总体变成8个工作日。不是不可以，但这应被明确计入计划，而不是把"现在"当免费缓冲。建议Week 0限制为1-2个工作日，超过就冻结当前假设继续做，后续进入v0.2。
+
+**问题2：v0.1不能只定义DTO。**
+
+Claude的Week 0列了StudentDTO、ApplicationDTO、ApprovalDTO，但缺少错误码、状态机、样例请求响应、mock、契约测试和变更规则。前端和测试真正依赖的是这些可执行产物，不只是字段名。
+
+**问题3：Week 1"无权限校验"会削弱纵向切片。**
+
+最小权限校验必须保留。否则审批API无法验证学生、辅导员、学工部三个角色的边界，后续权限返工会冲击核心流程。
+
+**问题4：前端启动时间在文档内不一致。**
+
+Claude前面说"前端Week 4并行"，后面修正建议又写"Week 2：CSV导入 + 前端开始"。这两个说法需要统一。我的建议是：Week 2可以开始前端技术预研和API client封装，但微信小程序主流程页面开发以Week 4为正式启动点。
+
+**问题5：CSV导入仍可能挤压Week 2。**
+
+Claude建议Week 2做CSV导入并让前端开始，但CSV staging、校验报告、upsert、软停用、审计日志本身就是一周以上风险项。Week 2的目标应定义为"CSV导入v1可用"，前端只做轻量准备；不要让Week 2同时承诺完整导入和主流程前端。
+
+**问题6：Postman集合不是足够验收标准。**
+
+Week 1可以交Postman集合，但必须有自动化端到端测试。否则每次契约变化都靠人工点接口，后续Week 2-4会快速失控。
+
+---
+
+## 五、建议形成第二轮共识
+
+建议将执行计划修正为：
+
+| 时间 | 目标 | 交付物 |
+|---|---|---|
+| Week 0 / 1-2工作日 | v0.1最小可执行契约 | OpenAPI/DTO、状态枚举、错误码、seed/fixture、mock响应、changelog |
+| Week 1 | 后端纵向切片 | 薄认证、最小角色校验、提交、两级审批、查询、Dorm Mock、端到端测试 |
+| Week 2 | CSV导入v1 | staging、校验报告、upsert、软停用基础、导入审计基础 |
+| Week 3 | 核心流程补强 + v0.2契约 | 权限细化、异常流、API mock更新、前端启动检查 |
+| Week 4-6 | 微信小程序并行开发 | 登录、申请、审批、查询主流程，使用mock并逐步联调真实后端 |
+| Week 6-7 | 宿舍真实API或降级方案 | 真实Provider、错误分类、缓存/降级、人工证明路径 |
+| Week 8-9 | UAT和完善 | 通知、附件最小可用、异常流修复、导入演练 |
+| Week 10 | 验收演示 | 演示脚本、缺陷修复、文档，不新增功能 |
+
+---
+
+## 直接回答Claude的4个问题
+
+1. **数据契约v0.1应该现在冻结还是Week 1前半？范围最小还是完整？**  
+   现在冻结，限制在1-2个工作日内完成。范围是"最小可执行契约"，不是极简字段，也不是完整未来模型。
+
+2. **Week 1的7-10天工作量是否现实？如何调整？**  
+   如果指7-10人日，在2-3人团队下现实；如果指7-10日历天，不现实。调整方式是Week 0先完成契约，Week 1只做后端最小闭环，推迟CSV完整导入、附件、通知、微信OAuth、真实宿舍API。
+
+3. **前端Week 4并行的前提条件是什么？**  
+   v0.2可消费契约、mock可用、核心API可跑、认证策略固定为演示期薄认证、状态枚举/错误码稳定、API owner和变更机制明确。不要求附件、通知、真实OAuth、真实宿舍API完成。
+
+4. **Claude的Week 0-1拆分方案是否可行？**  
+   方向可行，但必须修正：Week 0要timebox，v0.1要可执行而非字段清单，Week 1不能砍掉最小权限校验，前端启动时间要统一，Week 2不要同时塞满CSV和主流程前端。
+
+---
+
+## Codex第二轮态度
+
+**接受Claude的拆分方向，但不接受把契约冻结推迟到Week 1前半，也不接受Week 1无权限校验的纵向切片。**
+
+下一步不应继续抽象讨论，而应产出两个落地文件：
+
+1. `contract-v0.1.md`或OpenAPI草案：字段、状态、错误码、样例、mock、changelog。
+2. `week-0-1-execution-plan.md`：按天列出责任人、交付物、降级条件和验收测试。
+
+这两个文件完成后，再更新总实施计划。否则直接改10周排期仍然会停留在计划层，不能降低真正的集成风险。
+
+---
+
+**响应人：** Codex  
+**响应时间：** 2026-05-30  
+**讨论状态：** 第二轮回应，建议进入Week 0-1执行共识

tokens used
57,603

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
