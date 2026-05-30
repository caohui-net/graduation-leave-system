# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-05-30T07:26:56.595Z

## Original task

请批判性审视 docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md 中提出的下一步工作方案。要求：1) 不要客气，直接指出问题和风险 2) 回答文档中的10个问题 3) 提出替代方案（如果有更好的路径）4) 质疑工期评估和任务顺序 5) 指出可能遗漏的关键点。这是多轮讨论的第一轮，鼓励质疑和反驳，不需要一次性达成共识。

## Final prompt

请批判性审视 docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md 中提出的下一步工作方案。要求：1) 不要客气，直接指出问题和风险 2) 回答文档中的10个问题 3) 提出替代方案（如果有更好的路径）4) 质疑工期评估和任务顺序 5) 指出可能遗漏的关键点。这是多轮讨论的第一轮，鼓励质疑和反驳，不需要一次性达成共识。

## Raw output

```text
**结论：方案A不应原样执行。**  
它比旧计划好，但仍然是“先后端模块、后前端、最后联调”的瀑布排期。最大风险不是数据契约，而是到 Week 8-10 才发现端到端流程、微信小程序、附件、审批权限、宿舍降级和通知串不起来。文档里把“更新实施计划”列为立即执行事项 [41-next-steps...md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:63)，这太弱了。下一步不该只是改计划，而应产出可运行的纵向切片。

**主要问题**
1. `Week 8-9 前端、Week 10 联调` 风险很高。现有计划仍把前端后置 [41-next-steps...md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:136)，而原计划还同时要求 React Native 和微信小程序 [implementation-plan.md](/home/caohui/projects/graduation-leave-system/docs/superpowers/plans/2026-05-27-implementation-plan.md:486)。2-3 人 2 周做两个端、附件、审批、认证、联调，偏乐观。
2. Week 10 不能既做联调、验收、性能、部署、文档，又兜底前面延期。原计划第10周内容明显塞爆 [implementation-plan.md](/home/caohui/projects/graduation-leave-system/docs/superpowers/plans/2026-05-27-implementation-plan.md:564)。
3. “10周演示版 + 1-2周生产集成”只有在演示范围被砍清楚时才成立。若演示还包含双端、真实微信、完整附件、通知、导入审计、宿舍降级，那不现实。
4. 方案A仍然把 CSV 导入当成前置大模块。更好的做法是先做 `seed/import minimal path`，让认证和审批用同一套落库数据跑起来，再完善 CSV 校验、staging、审计。
5. “数据契约冻结”这个词危险。契约需要版本化和变更机制，不是一次冻结后假装不会变。40号文档已有 DTO 和 ImportResult 雏形 [40-api-blocking...md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:100)，现在要做的是契约测试和样例数据包。

**10个问题回答**
1. Week 1 做数据契约太晚吗？不该等到 Week 1 结束。现在就应冻结 v0.1：字段、枚举、样例 CSV、错误码、前端 API mock。Week 1 用它跑纵向切片。
2. 是否先做 MVP？是，必须。先做“学生登录/伪登录 -> 提交申请 -> 辅导员审批 -> 学工部审批 -> 状态可查”的端到端最小流程。
3. CSV 是否更早？不应 Week 1 完整完成，但 Week 1 必须完成最小导入路径：seed/CSV 二选一落库到真实 users/class mapping 表。完整 staging、审计、软停用放 Week 2。
4. Mock 数据够吗？100学生/10辅导员只够演示，不够测试。需要 fixture matrix：无班级、重复学号、辅导员停用、多班级、非毕业生、延期、宿舍 API 401/404/429/500/timeout。
5. 抽象是否过度？方向不算过度，但实现可能过度。保留 DTO、ImportSource、DormCheckoutProvider 边界；不要一开始铺满复杂 Provider 层级和泛型框架。
6. 宿舍 API 何时集成？Mock Provider 和契约测试必须 Week 1 进入提交申请流程；真实 API 可 Week 6-7，但接口信息获取和样例响应不能等到 Week 6。
7. 10周现实吗？演示版可以，但要砍范围：优先微信小程序或一个 Web/RN 壳，不要默认双端完整交付。生产就绪不现实，尤其原计划还要求 80% 覆盖率、P95、1000并发 [implementation-plan.md](/home/caohui/projects/graduation-leave-system/docs/superpowers/plans/2026-05-27-implementation-plan.md:68)。
8. Week 1 工作量饱和吗？不是不饱和，是目标错了。Week 1 应交付可运行骨架、契约测试、seed 数据、最小审批流，而不是只交文档和接口。
9. 更好路径？有：`契约v0.1 + 纵向切片 -> CSV导入硬化 -> 核心流程扩展 -> 前端并行 -> 外部集成 -> 验收硬化`。
10. 模块顺序要调吗？要。不要“认证完整后再申请、申请完整后再审批”。改成薄认证 + 申请审批核心流优先，通知/附件/完整微信登录后补。

**替代方案**
建议改成：

- Week 0-1：契约 v0.1、fixture 数据、后端骨架、薄认证、最小申请审批闭环、Dorm Mock 接入提交校验。
- Week 2：CSV 导入 v1：staging、校验报告、upsert、软停用、审计。
- Week 3-4：申请/审批权限、附件最小可用、状态机和审计补齐。
- Week 4-6：前端并行，不等后端全完；先小程序主流程。
- Week 6-7：宿舍真实 API 适配；若 API 不到位，保留 mock + 人工证明降级。
- Week 8-9：通知、异常流、UAT 修复、导入演练。
- Week 10：只做验收、演示、缺陷修复，不再塞新功能。

遗漏的关键点：验收范围没有砍清楚，双端交付没有优先级，真实 API 信息获取没有责任人和截止日期，导入失败后的人工处理流程不明确，数据契约缺少版本管理，Week 10 没有缓冲。第一轮我的态度是：方案A可以作为底稿，但不能作为执行计划。


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
session id: 019e77c5-f5f6-7fe2-813c-5a252da5b03a
--------
user
请批判性审视 docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md 中提出的下一步工作方案。要求：1) 不要客气，直接指出问题和风险 2) 回答文档中的10个问题 3) 提出替代方案（如果有更好的路径）4) 质疑工期评估和任务顺序 5) 指出可能遗漏的关键点。这是多轮讨论的第一轮，鼓励质疑和反驳，不需要一次性达成共识。
codex
我会先读取项目里的 RTK 和 review protocol，再看这份讨论文档及必要上下文。之后按“问题回答、风险、替代路径、工期/顺序质疑、遗漏点”直接给第一轮反驳意见。
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
/bin/bash -lc "sed -n '1,260p' docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md" in /home/caohui/projects/graduation-leave-system
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
- 对于首版（CSV导入）是否过于复杂？
- 是否应该先实现CSV导入，后续再抽象？

**问题6：宿舍清退API集成时机？**
- 当前计划Week 6-7做宿舍清退API对接
- 但申请提交（Week 3）就需要校验宿舍清退状态
- 是否应该更早集成？还是先用Mock？

### 4.3 关于工期评估

**问题7：10周工期是否现实？**
- Week 1: 数据契约和接口
- Week 2-3: CSV导入
- Week 3-6: 核心业务
- Week 6-7: 宿舍清退API
- Week 8-9: 前端
- Week 10: 联调

这个节奏是否合理？哪些环节可能延期？

**问题8：Week 1的工作量是否饱和？**
- 数据契约、DTO、接口设计
- 种子数据生成
- 导入模型设计

这些工作是否足够填满一周？是否应该增加其他任务？

### 4.4 关于替代方案

**问题9：是否有更好的实施路径？**
- 当前：数据契约→CSV导入→核心业务→API集成→前端→联调
- 替代1：MVP原型→迭代完善
- 替代2：前后端并行开发
- 替代3：API集成优先（如果API信息到位）

**问题10：是否应该调整模块开发顺序？**
- 当前：认证→申请→审批→附件→通知→集成→前端
- 是否应该：申请+审批核心流程→认证→附件→通知→集成→前端？
- 哪种顺序风险更低？

---

## 五、期望的讨论输出

### 5.1 第一轮讨论

**请Codex提供：**
1. 对方案A的批判性分析（不要客气，直接指出问题）
2. 识别的风险和遗漏点
3. 替代方案建议（如果有）
4. 对10个问题的回答和反驳

### 5.2 后续轮次

**如果第一轮未达成共识：**
- Claude回应Codex的批判
- 提出修正方案或反驳
- Codex继续质疑或提出新观点
- 重复直到达成共识

### 5.3 最终输出

**达成共识后：**
- 明确的下一步行动计划
- 调整后的实施路径
- 风险缓解措施
- 关键决策记录

---

## 六、讨论范围

**本次讨论聚焦：**
1. ✓ 下一步工作的优先级和顺序
2. ✓ 实施路径的优化
3. ✓ 工期评估的合理性
4. ✓ 技术风险的识别

**不在本次讨论范围：**
1. ✗ 已达成共识的架构设计（文档40）
2. ✗ 具体代码实现细节
3. ✗ 前端UI/UX设计
4. ✗ 部署和运维方案

---

## 七、补充信息

### 7.1 项目约束

- **团队规模：** 2-3人
- **预计工期：** 10周演示版 + 1-2周生产集成
- **外部依赖：** 宿舍清退API信息待提供
- **交付要求：** Week 10可演示版本（Mock数据）

### 7.2 已有资源

- **系统设计文档：** 完整的架构、数据库、API设计
- **数据对接文档：** CSV模板、API规范
- **共识文档：** API阻塞解决方案（文档40）

### 7.3 关键假设

- CSV导入是首版主数据来源
- 宿舍清退API在Week 6-7前到位
- 微信小程序测试AppID可用
- 开发环境已就绪

---

## 八、讨论启动

**请Codex：**
1. 批判性审视方案A
2. 回答10个问题
3. 提出替代方案（如果有）
4. 指出可能遗漏的风险

**讨论原则：**
- 不要客气，直接指出问题
- 鼓励质疑和反驳
- 提出新观点和替代方案
- 多轮讨论直到达成共识

---

**讨论发起人：** Claude Opus 4.7  
**创建时间：** 2026-05-30  
**期望讨论轮次：** 2-4轮  
**优先级：** P0（决定实施路径）

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

codex
我已经看到 41 号文档本身，但它依赖 37-40 的共识和现有实施计划。为了避免只按摘要做判断，我会再快速读取相关共识文档和计划文档的目录/关键段落。
exec
/bin/bash -lc 'rtk ls -la docs/discussions/codex-review-2026-05-30' in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk rg -n \"Week|周|10周|认证|申请|审批|CSV|宿舍|ImportSource|实施|计划\" docs -g '*.md'" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk rg --files docs | rg 'docs/discussions/codex-review-2026-05-30/(3[7-9]|40)|IMPLEMENT|PLAN|SUMMARY|implementation|plan'" in /home/caohui/projects/graduation-leave-system
 succeeded in 101ms:
 succeeded in 135ms:
docs/superpowers/plans/2026-05-27-implementation-plan.md
docs/PROJECT-SUMMARY.md
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md

 succeeded in 155ms:
docs/微信小程序申请说明.md:1:# 微信小程序申请说明
docs/微信小程序申请说明.md:11:**建议使用学校主体申请小程序**
docs/微信小程序申请说明.md:15:如果使用校友会主体申请小程序，会有以下限制：
docs/微信小程序申请说明.md:21:- **影响：** 无法进行实名认证和身份验证
docs/微信小程序申请说明.md:79:3. **主体认证：** 政府主体需要提供相关证明材料
docs/codex-review-protocol.md:281:- 结果：修正staging表设计、认证约束、class_id约束等关键问题
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
docs/数据对接说明文档.md:32:- 实施周期短：无需开发API，1-2周即可上线
docs/数据对接说明文档.md:41:| 数据确认 | 第1周 | 确认数据可用性、字段定义、CSV模板 |
docs/数据对接说明文档.md:42:| CSV导入开发 | 第2-3周 | 开发CSV导入功能、校验逻辑、审计日志 |
docs/数据对接说明文档.md:43:| 宿舍清退API对接 | 第4周 | 对接宿舍清退API、测试异常场景 |
docs/数据对接说明文档.md:44:| 上线验收 | 第5周 | 全量导入演练、功能测试、正式上线 |
docs/数据对接说明文档.md:48:## 二、学生基本信息（CSV导入）
docs/数据对接说明文档.md:55:- 自动分配审批人（根据班级匹配辅导员）
docs/数据对接说明文档.md:81:- `is_graduating=true` 表示具备本批次离校申请资格
docs/数据对接说明文档.md:84:### 2.3 CSV模板
docs/数据对接说明文档.md:101:- 不要使用Excel的"另存为CSV"，建议使用专业工具导出UTF-8编码
docs/数据对接说明文档.md:105:**步骤1：准备CSV文件**
docs/数据对接说明文档.md:110:**步骤2：上传CSV文件**
docs/数据对接说明文档.md:114:- 上传CSV文件
docs/数据对接说明文档.md:125:- 如有错误，修改CSV后重新上传
docs/数据对接说明文档.md:145:- 停用账号不能创建新申请
docs/数据对接说明文档.md:146:- 停用账号可以查看历史申请记录
docs/数据对接说明文档.md:151:## 三、辅导员基本信息（CSV导入）
docs/数据对接说明文档.md:156:- 审批权限管理
docs/数据对接说明文档.md:171:- `employee_id` 必须全校唯一，与统一身份认证、人事系统工号一致
docs/数据对接说明文档.md:172:- `is_active=false` 时不能登录、不能审批，但历史记录可查询
docs/数据对接说明文档.md:174:### 3.3 CSV模板
docs/数据对接说明文档.md:191:## 四、班级-辅导员对应关系（CSV导入）
docs/数据对接说明文档.md:195:学生提交申请时，系统根据学生的 `class_id` 自动查询对应的辅导员，分配审批人。
docs/数据对接说明文档.md:210:### 4.3 CSV模板
docs/数据对接说明文档.md:243:- 无审批人的学生数：有多少学生没有对应的辅导员
docs/数据对接说明文档.md:247:## 五、宿舍清退数据（API接口）
docs/数据对接说明文档.md:251:学生提交离校申请时，系统实时查询宿舍清退状态：
docs/数据对接说明文档.md:252:- 已完成清退：允许提交申请
docs/数据对接说明文档.md:253:- 未完成清退：提示学生先完成宿舍清退手续
docs/数据对接说明文档.md:254:- 查询失败：允许学生上传宿舍清退证明截图
docs/数据对接说明文档.md:258:**接口名称：** 查询学生宿舍清退状态
docs/数据对接说明文档.md:262:**请求地址：** `http://宿舍管理系统域名/api/dorm/checkout/status`
docs/数据对接说明文档.md:264:**认证方式：** API Key + IP白名单
docs/数据对接说明文档.md:308:- `pending` - 清退中（已申请但未完成）
docs/数据对接说明文档.md:354:- 允许学生上传宿舍清退证明截图
docs/数据对接说明文档.md:361:### 6.1 CSV文件要求
docs/数据对接说明文档.md:365:- 格式：CSV或Excel（.xlsx）
docs/数据对接说明文档.md:401:### 7.1 CSV导入相关
docs/数据对接说明文档.md:403:**Q1：CSV文件中文乱码怎么办？**
docs/数据对接说明文档.md:405:A：确保文件编码为UTF-8。如果使用Excel编辑，保存时选择"CSV UTF-8（逗号分隔）"格式。
docs/数据对接说明文档.md:409:A：检查CSV文件中是否有重复的学号。系统要求学号必须唯一。
docs/数据对接说明文档.md:427:A：系统会自动重试3次。如果仍然失败，允许学生上传宿舍清退证明截图。
docs/数据对接说明文档.md:429:**Q7：API接口需要认证吗？**
docs/数据对接说明文档.md:441:A：可以通过系统管理后台手动修改，或者重新导入包含该学生的CSV文件。
docs/数据对接说明文档.md:445:A：更新班级-辅导员对应关系，重新导入CSV文件。已提交的申请不受影响，新提交的申请使用新辅导员。
docs/微信小程序备案说明.md:103:1. 申请小程序之后，访问微信公众平台
docs/微信小程序备案说明.md:132:- [微信小程序申请说明](./微信小程序申请说明.md)
docs/Codex审查流程指南.md:281:- 结果：修正staging表设计、认证约束、class_id约束等关键问题
docs/数据确认清单.md:5:**目标用户：** 宿舍管理系统管理员、数据对接负责人
docs/数据确认清单.md:27:**问题5：** 辅导员工号（`employee_id`）是否全校唯一？是否与统一身份认证、人事系统工号一致？
docs/数据确认清单.md:31:**问题6：** 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
docs/数据确认清单.md:33:**背景说明：** 系统需要明确哪些学生具备离校申请资格，通过 `is_graduating` 字段标识。
docs/数据确认清单.md:54:- A. 数据库直连（需要安全审批和网络配置）
docs/数据确认清单.md:56:- C. CSV/Excel文件导入（最快，首版推荐）
docs/数据确认清单.md:62:**问题11：** CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/数据确认清单.md:72:**背景说明：** 例如宿舍清退API查询失败时，是否允许学生上传截图证明？
docs/数据确认清单.md:74:**问题13：** 是否有统一身份认证或微信绑定前置要求？
docs/数据确认清单.md:76:**背景说明：** 系统支持密码登录和微信登录，CSV导入的账号需要首次登录设置密码。
docs/数据确认清单.md:84:### 1.6 实施保障确认
docs/数据确认清单.md:88:**背景说明：** 需要明确数据更新周期和故障联系人，确保系统稳定运行。
docs/数据确认清单.md:92:## 二、实施计划
docs/数据确认清单.md:96:首版采用**CSV/Excel导入 + 宿舍清退API**组合方案：
docs/数据确认清单.md:100:| 学生基本信息 | CSV/Excel导入 | 变更频率低（学期级），快速上线 |
docs/数据确认清单.md:101:| 辅导员基本信息 | CSV/Excel导入 | 约50人，变更频率低 |
docs/数据确认清单.md:102:| 班级-辅导员映射 | CSV/Excel导入 | 变更频率低，需强校验 |
docs/数据确认清单.md:103:| 宿舍清退数据 | API实时查询 | 需要实时校验清退状态 |
docs/数据确认清单.md:109:### 2.2 实施路径（5阶段）
docs/数据确认清单.md:111:**阶段1：数据确认（1周）**
docs/数据确认清单.md:129:**阶段2：CSV导入实现（2周）**
docs/数据确认清单.md:131:**目标：** 实现CSV批量导入功能
docs/数据确认清单.md:134:1. 设计三份CSV模板（学生、辅导员、班级映射）
docs/数据确认清单.md:135:2. 实现CSV导入功能（文件上传、解析、校验）
docs/数据确认清单.md:142:- CSV导入功能模块
docs/数据确认清单.md:143:- 三份CSV模板文件
docs/数据确认清单.md:149:**阶段3：宿舍清退API对接（1周）**
docs/数据确认清单.md:151:**目标：** 实现宿舍清退状态实时查询
docs/数据确认清单.md:154:1. 对接宿管系统宿舍清退API
docs/数据确认清单.md:155:2. 实现API调用逻辑（认证、请求、响应解析）
docs/数据确认清单.md:161:- 宿舍清退API对接模块
docs/数据确认清单.md:168:**阶段4：上线前验收（1周）**
docs/数据确认清单.md:203:- 持续优化计划
docs/数据确认清单.md:211:| 阶段1 | 第1周 | 数据确认完成 | 15个问题全部确认，获得测试数据 |
docs/数据确认清单.md:212:| 阶段2 | 第2-3周 | CSV导入功能上线 | 成功导入测试数据，校验报告无异常 |
docs/数据确认清单.md:213:| 阶段3 | 第4周 | 宿舍清退API对接完成 | API调用成功率>95%，降级流程测试通过 |
docs/数据确认清单.md:214:| 阶段4 | 第5周 | 上线前验收通过 | 全量导入成功，异常清单为空，功能测试通过 |
docs/数据确认清单.md:217:**总计时间：** 5周（约1.5个月）
docs/数据确认清单.md:227:| 宿舍清退API不稳定 | 中 | 实现降级流程，允许上传截图证明 |
docs/用户设计说明书.md:1:# 毕业生离校申请审批系统 - 用户设计说明书
docs/用户设计说明书.md:13:本系统旨在实现毕业生离校申请的在线化、规范化管理，替代传统纸质审批流程，提高审批效率，减少人工成本。
docs/用户设计说明书.md:17:- **学生端：** 在线提交离校申请、上传证明材料、查看审批进度、接收审批通知
docs/用户设计说明书.md:18:- **辅导员端：** 审批本年级学生的离校申请、查看审批历史、接收待办提醒
docs/用户设计说明书.md:19:- **学工部端：** 审批所有学生的离校申请、查看全校审批统计、导出审批数据
docs/用户设计说明书.md:32:### 2.1 申请提交流程
docs/用户设计说明书.md:35:学生登录 → 填写申请信息 → 上传证明材料 → 提交申请 → 等待审批
docs/用户设计说明书.md:40:- 计划离校日期
docs/用户设计说明书.md:44:- 宿舍清退证明（照片或PDF）
docs/用户设计说明书.md:48:### 2.2 审批流程
docs/用户设计说明书.md:51:学生提交 → 辅导员审批 → 学工部审批 → 审批完成
docs/用户设计说明书.md:56:**审批时限：**
docs/用户设计说明书.md:57:- 辅导员审批：提交后1个工作日内
docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
docs/用户设计说明书.md:61:**审批结果：**
docs/用户设计说明书.md:62:- **通过：** 进入下一审批环节或完成审批
docs/用户设计说明书.md:68:- 学生提交申请 → 通知辅导员
docs/用户设计说明书.md:69:- 辅导员审批通过 → 通知学生和学工部
docs/用户设计说明书.md:71:- 学工部审批通过 → 通知学生（审批完成）
docs/用户设计说明书.md:73:- 审批超时 → 通知审批人
docs/用户设计说明书.md:79:### 3.1 双通道认证
docs/用户设计说明书.md:94:**宿舍管理系统对接：**
docs/用户设计说明书.md:95:- 学生提交申请时，系统自动验证宿舍是否已清退
docs/用户设计说明书.md:96:- 验证失败时，提示学生先完成宿舍清退
docs/用户设计说明书.md:107:- API接口JWT Token认证
docs/用户设计说明书.md:115:- 学生只能查看自己的申请
docs/用户设计说明书.md:127:| **学生** | 本人申请 | 提交申请、查看进度、上传附件 |
docs/用户设计说明书.md:128:| **辅导员** | 本年级学生 | 审批申请、查看历史、接收通知 |
docs/用户设计说明书.md:129:| **学工部** | 全校学生 | 审批申请、查看统计、导出数据 |
docs/用户设计说明书.md:135:- ✓ 创建离校申请
docs/用户设计说明书.md:136:- ✓ 修改草稿状态的申请
docs/用户设计说明书.md:137:- ✓ 提交申请
docs/用户设计说明书.md:138:- ✓ 查看自己的申请列表和详情
docs/用户设计说明书.md:140:- ✓ 查看审批历史
docs/用户设计说明书.md:141:- ✗ 查看其他学生的申请
docs/用户设计说明书.md:144:- ✓ 查看负责班级学生的申请列表
docs/用户设计说明书.md:145:- ✓ 审批负责班级学生的申请（通过/驳回）
docs/用户设计说明书.md:146:- ✓ 填写审批意见
docs/用户设计说明书.md:147:- ✓ 查看审批历史
docs/用户设计说明书.md:148:- ✓ 接收待审批通知
docs/用户设计说明书.md:149:- ✗ 审批其他班级学生
docs/用户设计说明书.md:152:- ✓ 查看所有学生的申请列表
docs/用户设计说明书.md:153:- ✓ 审批所有学生的申请（通过/驳回）
docs/用户设计说明书.md:154:- ✓ 填写审批意见
docs/用户设计说明书.md:155:- ✓ 查看全校审批统计
docs/用户设计说明书.md:156:- ✓ 导出审批数据（Excel）
docs/用户设计说明书.md:157:- ✓ 查看审批历史
docs/用户设计说明书.md:186:- 年度申请：5,000份
docs/用户设计说明书.md:197:- 每周全量备份（周日凌晨）
docs/用户设计说明书.md:198:- 保留最近12周备份
docs/用户设计说明书.md:215:**Q4：申请被驳回后如何修改？**
docs/用户设计说明书.md:216:A：在申请详情页点击"修改"按钮，修改后重新提交。
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
docs/用户设计说明书.md:257:**工作时间：** 周一至周五 9:00-18:00
docs/用户设计说明书.md:262:- **实施计划文档：** `docs/superpowers/plans/2026-05-27-implementation-plan.md`
docs/用户设计说明书.md:284:本系统需要从宿舍管理系统获取以下数据，才能正常运行：
docs/用户设计说明书.md:287:2. **辅导员基本信息** - 创建辅导员账号，让辅导员能够审批申请
docs/用户设计说明书.md:288:3. **班级-辅导员对应关系** - 系统自动分配审批人，学生提交申请时自动找到对应的辅导员
docs/用户设计说明书.md:289:4. **宿舍清退数据** - 验证学生是否完成宿舍清退，未完成不能提交申请
docs/用户设计说明书.md:304:- 不需要技术开发，1-2周就能上线
docs/用户设计说明书.md:316:适用于：宿舍清退数据
docs/用户设计说明书.md:319:- 学生提交申请时，需要实时查询宿舍是否已清退
docs/用户设计说明书.md:320:- 如果未清退，系统会提示学生先完成宿舍清退手续
docs/用户设计说明书.md:323:- 允许学生上传宿舍清退证明截图
docs/用户设计说明书.md:324:- 管理员审核通过后，学生可以继续提交申请
docs/用户设计说明书.md:370:**4. 宿舍清退数据（实时查询）**
docs/用户设计说明书.md:397:- 登录后可以提交离校申请
docs/用户设计说明书.md:398:- 系统自动分配对应的辅导员审批
docs/用户设计说明书.md:402:- 登录后可以看到负责班级的学生申请
docs/用户设计说明书.md:403:- 可以进行审批操作
docs/用户设计说明书.md:407:- 可以看到所有学生的申请
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:20:- **位置：** 第4章 认证授权设计
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:22:- **影响：** 实施难度大、依赖外部服务、用户体验差
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:39:**API与认证（4个）：**
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:82:- 未考虑实施成本和维护成本
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:126:## 实施路线图建议
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:128:### Phase 1：简化设计，快速启动（第1-2周）
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:142:**推迟实施：**
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:148:### Phase 2：核心功能开发（第3-7周）
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:152:- 核心模块优先（认证、申请、审批）
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:160:### Phase 3：优化增强（第8-9周）
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:172:### Phase 4：测试部署（第10周）
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:188:### 立即修改（阻塞实施）
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:192:- ### 2.9 申请历史表（applications_history）
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:195:+ 说明：申请历史通过audit_logs表的字段级追踪实现
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:198:**第4章 认证授权设计：**
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:239:**第5章 审批流程：**
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:267:| **综合评分** | **6.5/10** | **可实施，但需要简化和调整** |
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:269:### 实施风险评估
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:275:| 安全措施实施困难 | 中 | 删除过度措施 |
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:281:**✓ 可以开始实施**，但需要：
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:288:**修改后可进入Phase 1实施**
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:298:5. **开始实施**：进入Phase 1开发
docs/superpowers/plans/2026-05-27-implementation-plan.md:1:# 毕业生离校申请审批系统 - 实施计划
docs/superpowers/plans/2026-05-27-implementation-plan.md:4:**计划版本：** v1.0  
docs/superpowers/plans/2026-05-27-implementation-plan.md:5:**预计工期：** 8-10周  
docs/superpowers/plans/2026-05-27-implementation-plan.md:12:实现一个完整的毕业生离校申请审批系统，支持：
docs/superpowers/plans/2026-05-27-implementation-plan.md:13:- 学生在线提交离校申请
docs/superpowers/plans/2026-05-27-implementation-plan.md:14:- 辅导员和学工部两级审批
docs/superpowers/plans/2026-05-27-implementation-plan.md:17:- 宿舍管理系统对接（API集成）
docs/superpowers/plans/2026-05-27-implementation-plan.md:26:- 认证授权系统
docs/superpowers/plans/2026-05-27-implementation-plan.md:27:- 审批流程引擎
docs/superpowers/plans/2026-05-27-implementation-plan.md:58:- 宿舍管理系统API文档和测试环境
docs/superpowers/plans/2026-05-27-implementation-plan.md:64:- ✓ 审批流程完整可用
docs/superpowers/plans/2026-05-27-implementation-plan.md:106:│   │   ├── applications/       # 离校申请模块
docs/superpowers/plans/2026-05-27-implementation-plan.md:113:│   │   ├── approvals/          # 审批管理模块
docs/superpowers/plans/2026-05-27-implementation-plan.md:171:## 实施阶段
docs/superpowers/plans/2026-05-27-implementation-plan.md:173:### 阶段1：项目初始化和基础设施（第1周）
docs/superpowers/plans/2026-05-27-implementation-plan.md:218:### 阶段2：用户认证模块（第2周）
docs/superpowers/plans/2026-05-27-implementation-plan.md:220:**目标：** 实现用户管理和认证授权系统
docs/superpowers/plans/2026-05-27-implementation-plan.md:230:2. **实现学号密码认证**
docs/superpowers/plans/2026-05-27-implementation-plan.md:235:   - 编写认证测试
docs/superpowers/plans/2026-05-27-implementation-plan.md:237:3. **实现微信OAuth2认证**
docs/superpowers/plans/2026-05-27-implementation-plan.md:241:   - 编写微信认证测试
docs/superpowers/plans/2026-05-27-implementation-plan.md:264:### 阶段3：离校申请模块（第3周）
docs/superpowers/plans/2026-05-27-implementation-plan.md:266:**目标：** 实现离校申请的创建、查询、更新、提交功能
docs/superpowers/plans/2026-05-27-implementation-plan.md:270:1. **创建申请模型**
docs/superpowers/plans/2026-05-27-implementation-plan.md:282:3. **实现申请CRUD API**
docs/superpowers/plans/2026-05-27-implementation-plan.md:283:   - 创建申请API
docs/superpowers/plans/2026-05-27-implementation-plan.md:284:   - 获取申请列表API
docs/superpowers/plans/2026-05-27-implementation-plan.md:285:   - 获取申请详情API
docs/superpowers/plans/2026-05-27-implementation-plan.md:286:   - 更新申请API
docs/superpowers/plans/2026-05-27-implementation-plan.md:287:   - 删除申请API（软删除）
docs/superpowers/plans/2026-05-27-implementation-plan.md:289:4. **实现申请提交逻辑**
docs/superpowers/plans/2026-05-27-implementation-plan.md:291:   - 实现申请编号生成
docs/superpowers/plans/2026-05-27-implementation-plan.md:295:5. **实现申请查询过滤**
docs/superpowers/plans/2026-05-27-implementation-plan.md:302:- ✓ 创建申请成功
docs/superpowers/plans/2026-05-27-implementation-plan.md:303:- ✓ 申请编号自动生成
docs/superpowers/plans/2026-05-27-implementation-plan.md:304:- ✓ 提交申请后状态变更为pending_counselor
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
docs/superpowers/plans/2026-05-27-implementation-plan.md:354:### 阶段5：附件管理模块（第5周）
docs/superpowers/plans/2026-05-27-implementation-plan.md:380:   - 权限验证（只能下载自己的或审批人的）
docs/superpowers/plans/2026-05-27-implementation-plan.md:397:### 阶段6：通知模块（第6周）
docs/superpowers/plans/2026-05-27-implementation-plan.md:427:5. **集成通知到审批流程**
docs/superpowers/plans/2026-05-27-implementation-plan.md:428:   - 申请提交时通知辅导员
docs/superpowers/plans/2026-05-27-implementation-plan.md:429:   - 审批通过时通知学生和下一审批人
docs/superpowers/plans/2026-05-27-implementation-plan.md:430:   - 审批驳回时通知学生
docs/superpowers/plans/2026-05-27-implementation-plan.md:431:   - 超时时通知审批人
docs/superpowers/plans/2026-05-27-implementation-plan.md:437:- ✓ 审批流程触发通知
docs/superpowers/plans/2026-05-27-implementation-plan.md:442:### 阶段7：外部系统集成（第7周）
docs/superpowers/plans/2026-05-27-implementation-plan.md:444:**目标：** 实现宿舍管理系统对接和重试机制
docs/superpowers/plans/2026-05-27-implementation-plan.md:454:2. **实现宿舍系统对接**
docs/superpowers/plans/2026-05-27-implementation-plan.md:457:   - 实现认证逻辑
docs/superpowers/plans/2026-05-27-implementation-plan.md:472:5. **集成到审批流程**
docs/superpowers/plans/2026-05-27-implementation-plan.md:473:   - 提交申请时验证宿舍清退
docs/superpowers/plans/2026-05-27-implementation-plan.md:478:- ✓ 宿舍系统API调用成功
docs/superpowers/plans/2026-05-27-implementation-plan.md:481:- ✓ 集成到审批流程
docs/superpowers/plans/2026-05-27-implementation-plan.md:486:### 阶段8：前端开发（第8-9周）
docs/superpowers/plans/2026-05-27-implementation-plan.md:500:2. **实现认证页面**
docs/superpowers/plans/2026-05-27-implementation-plan.md:506:3. **实现申请管理页面**
docs/superpowers/plans/2026-05-27-implementation-plan.md:507:   - 申请列表页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:508:   - 创建申请页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:509:   - 申请详情页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:510:   - 提交申请页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:512:4. **实现审批页面**
docs/superpowers/plans/2026-05-27-implementation-plan.md:513:   - 待审批列表页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:514:   - 审批详情页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:515:   - 审批操作页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:537:2. **实现认证页面**
docs/superpowers/plans/2026-05-27-implementation-plan.md:542:3. **实现申请管理页面**
docs/superpowers/plans/2026-05-27-implementation-plan.md:543:   - 申请列表页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:544:   - 创建申请页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:545:   - 申请详情页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:547:4. **实现审批页面**
docs/superpowers/plans/2026-05-27-implementation-plan.md:548:   - 待审批列表页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:549:   - 审批操作页面
docs/superpowers/plans/2026-05-27-implementation-plan.md:564:### 阶段9：测试和部署（第10周）
docs/superpowers/plans/2026-05-27-implementation-plan.md:576:   - 编写完整审批流程测试
docs/superpowers/plans/2026-05-27-implementation-plan.md:617:- 缓解：提前申请微信公众平台账号
docs/superpowers/plans/2026-05-27-implementation-plan.md:680:**计划结束**
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:1:# 混合认证方案审查 - Round 3
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:5:**审查范围：** 原设计者提出的混合认证改进方案
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:27:- 至少一种认证方式的数据库约束
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:164:改进的认证设计**从根本上是健全的**，修复了关键的账户接管漏洞。双路径方法（密码优先或微信优先）是良好的UX妥协。
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:166:**实施前必需的修改：**
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:179:    "至少一种认证方式",               # ✅ 你的方案
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:192:继续使用改进的认证设计，但在进入实施前**将上述5个强制性修改添加到设计文档**。核心架构现在是健全的。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:17:- **数据获取方式：** 通过宿管系统提供的数据库、API或CSV文件
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:24:3. **实施简化：** 避免多方对接的协调成本和技术复杂度
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:30:- ✅ **接受：** 对接方式、字段定义、实施细节的建议
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
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:115:- `pending`：清退中（已申请但未完成）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:121:### 2.4 问题4：缺实施细节
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:123:**Codex意见：** 缺少终审管理员分配规则、账号标识映射、历史审批人一致性规则、多辅导员场景处理。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:127:这些确实是实施级关键问题，需要在文档中明确。我们逐项回应：
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:131:**问题：** 学生提交申请时，系统如何确定 `admin_id`（终审管理员）？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:137:2. 所有申请提交时自动分配给默认终审人
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:142:- 按学院分配：不同学院的申请分配给不同终审人
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:174:- 学生CSV：`student_id` → `users.student_id`
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:175:- 辅导员CSV：`employee_id` → `users.employee_id`
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:176:- 班级映射CSV：`counselor_employee_id` → 查询 `users` 表中 `employee_id` 匹配的记录
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:180:#### 4.3 历史审批人一致性规则
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:182:**问题：** 班级-辅导员映射变更后，已提交申请中的 `counselor_id` 是否自动改写？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:187:这是一个重要的业务规则。如果班级映射变更后自动改写已提交申请的审批人，会导致：
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:188:1. 审批流程混乱（原审批人已审批，新审批人不知情）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:189:2. 审计追溯困难（无法还原当时的审批人是谁）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:190:3. 权限边界模糊（新审批人可能不应该看到旧申请）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:193:1. 已提交的申请保持原审批人不变
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:194:2. 新提交的申请使用新映射
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:200:1. **审批流程完整性：** 已提交申请的审批人是提交时确定的，不应因后续映射变更而改变
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:201:2. **审计追溯：** 保持历史审批人记录，便于追溯当时的审批责任
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:202:3. **权限边界：** 新辅导员不应自动获得旧申请的审批权限
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:208:| 申请提交时 | 根据当前班级-辅导员映射确定 `counselor_id` |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:209:| 映射变更后，已提交申请 | `counselor_id` **不变**，保持原审批人 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:210:| 映射变更后，新提交申请 | 使用新映射确定 `counselor_id` |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:211:| 需要改派审批人 | 管理员显式操作，记录审计日志（操作人、时间、原因） |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:215:- 审计日志表记录审批人变更操作
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:228:2. 审批流程需要确定主审批人
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:229:3. 权限边界需要明确（所有辅导员都能审批？还是只有主辅导员？）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:238:3. CSV导入时强校验：同一 `class_id` 不能出现多次
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:246:| 辅导员调岗 | 更新班级映射，新申请使用新辅导员 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:253:3. 申请提交时使用主辅导员作为 `counselor_id`
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:254:4. 所有辅导员都能查看本班申请，但只有主辅导员能审批
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:298:3. CSV需补充导入覆盖策略、重复数据处理、失败回滚
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:302:这些都是技术实施的关键细节，需要在文档中补充。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:324:- 错误码规范：200成功、400参数错误、401认证失败、500服务器错误
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:329:**CSV技术要求：**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:382:5. 辅导员工号（`employee_id`）是否全校唯一？是否与统一身份认证、人事系统工号一致？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:383:6. 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:390:9. 优先推荐的对接方式是什么？（DB直连 / API / CSV导入）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:392:11. CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:396:13. 是否有统一身份认证或微信绑定前置要求？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:399:**实施保障确认：**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:402:### 3.6 实施建议（第七章）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:404:**Codex建议：** 调整推荐方案和实施路径。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:409:Codex建议的实施路径非常合理：
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:411:2. 先落地CSV模板
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:413:4. 再对接宿舍清退API
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:419:**修改后的实施路径：**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:421:**阶段1：数据确认（1周）**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:427:**阶段2：CSV导入实现（2周）**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:428:1. 设计三份CSV模板：学生、辅导员、班级-辅导员映射
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:429:2. 实现CSV导入功能和校验逻辑
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:433:**阶段3：宿舍清退API对接（1周）**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:434:1. 对接宿管系统宿舍清退API
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:438:**阶段4：上线前验收（1周）**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:455:1. 对接方式从"DB优先"改为"CSV/Excel首版优先，API/DB增强"
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:459:5. 明确历史审批人一致性规则（不自动改写）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:461:7. 补充DB/API/CSV的技术要求细节
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:464:10. 调整实施路径（CSV优先，分阶段实施）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:479:- 调整对接方式优先级：学生/辅导员/班级映射改为"CSV/Excel首版优先"
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:483:- 补充说明：`is_graduating=true` 表示具备本批次离校申请资格
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:485:**修改3：宿舍清退数据（第三章）**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:500:- 补充DB/API/CSV的具体技术要求
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:510:**修改9：实施建议（第七章）**
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:511:- 调整推荐方案：CSV首版优先
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:512:- 补充分阶段实施路径（5个阶段）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:517:- 新增"历史审批人一致性规则"章节
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:532:5. 启动实施（按3.6节的5阶段路径）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:546:4. **实施路径：** 我们接受了CSV首版优先的建议，并补充了5阶段实施路径。Codex是否认同这个路径？是否有需要调整的地方？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:557:- **接受建议：** CSV首版优先、字段定义统一、补充实施细节
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:132:3. **关键模块强制TDD**：认证、审批、支付等
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:136:P0: 核心业务逻辑（认证、审批、状态机）
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:203:Locust测试场景只有3个任务（查看列表、查看详情、审批），权重固定（3:2:1）。
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:211:        """学生查看自己的申请"""
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:216:        """学生创建申请"""
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:227:        """辅导员查看待审批"""
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:232:        """辅导员审批"""
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:251:## 实施建议优先级
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:253:### P0 - 必须修改（阻塞实施）
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:114:2. **上传限流过严**：10次/小时意味着用户最多上传10个文件，但申请需要3个附件，如果上传失败需要重试，很容易达到限制
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:246:## 实施建议优先级
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md:248:### P0 - 必须修改（阻塞实施）
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:65:**理由：** 申请被驳回重提时，需要保留历史版本用于审计。
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:71:    snapshot = models.JSONField(help_text='申请快照')
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:88:**实施：**
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:145:1. ✅ `applications_history` - 申请历史版本
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:170:5. ✅ users表添加认证安全字段
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:171:6. ✅ 活跃申请唯一约束（Django应用层）
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:1:# 数据对接确认清单与实施计划
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:5:**目的：** 提交给宿管系统方，确认数据可用性和实施计划  
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:28:**问题5：** 辅导员工号（`employee_id`）是否全校唯一？是否与统一身份认证、人事系统工号一致？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:32:**问题6：** 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:34:**背景说明：** 系统需要明确哪些学生具备离校申请资格，通过 `is_graduating` 字段标识。
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:55:- A. 数据库直连（需要安全审批和网络配置）
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:57:- C. CSV/Excel文件导入（最快，首版推荐）
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:63:**问题11：** CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:73:**背景说明：** 例如宿舍清退API查询失败时，是否允许学生上传截图证明？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:75:**问题13：** 是否有统一身份认证或微信绑定前置要求？
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:77:**背景说明：** 系统支持密码登录和微信登录，CSV导入的账号需要首次登录设置密码。
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:85:### 1.6 实施保障确认
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:89:**背景说明：** 需要明确数据更新周期和故障联系人，确保系统稳定运行。
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:93:## 二、实施计划
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:97:首版采用**CSV/Excel导入 + 宿舍清退API**组合方案：
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:101:| 学生基本信息 | CSV/Excel导入 | 变更频率低（学期级），快速上线 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:102:| 辅导员基本信息 | CSV/Excel导入 | 约50人，变更频率低 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:103:| 班级-辅导员映射 | CSV/Excel导入 | 变更频率低，需强校验 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:104:| 宿舍清退数据 | API实时查询 | 需要实时校验清退状态 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:110:### 2.2 实施路径（5阶段）
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:112:**阶段1：数据确认（1周）**
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:130:**阶段2：CSV导入实现（2周）**
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:132:**目标：** 实现CSV批量导入功能
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:135:1. 设计三份CSV模板：
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:139:2. 实现CSV导入功能：
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:156:- CSV导入功能模块
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:157:- 三份CSV模板文件
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:163:**阶段3：宿舍清退API对接（1周）**
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:165:**目标：** 实现宿舍清退状态实时查询
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:168:1. 对接宿管系统宿舍清退API
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:170:   - 认证和鉴权
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:182:   - 学生上传宿舍清退证明截图
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:186:- 宿舍清退API对接模块
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:193:**阶段4：上线前验收（1周）**
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:200:   - 设置申请开放时间和截止时间
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:210:   - 无审批人的学生：0个
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:217:   - 辅导员登录和审批
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:219:   - 宿舍清退状态查询
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:220:   - 申请提交和审批流程
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:241:   - 如果变更频率高（每周多次），考虑升级为API实时同步
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:242:   - 如果变更频率低（每学期1-2次），保持CSV导入
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:248:   - 辅导员审批效率
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:252:   - 审批流程优化
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:259:- 持续优化计划
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:267:| 阶段1 | 第1周 | 数据确认完成 | 15个问题全部确认，获得测试数据 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:268:| 阶段2 | 第2-3周 | CSV导入功能上线 | 成功导入测试数据，校验报告无异常 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:269:| 阶段3 | 第4周 | 宿舍清退API对接完成 | API调用成功率>95%，降级流程测试通过 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:270:| 阶段4 | 第5周 | 上线前验收通过 | 全量导入成功，异常清单为空，功能测试通过 |
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:273:**总计时间：** 5周（约1.5个月）
docs/discussions/codex-review-2026-05-27/36-data-confirmation-and-implementation.md:283:| 宿舍清退API不稳定 | 中 | 实现降级流程，允许上传截图证明 |
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:16:`integrations`模块职责定义为"外部系统集成"，但实际只对接宿舍管理系统。未来如需对接图书馆系统、财务系统，是否都放在同一模块？模块划分缺乏扩展性考虑。
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:27:├── dorm/            # 宿舍系统集成
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:48:1. **Phase 1实施**：先同步实现，测量实际性能
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:89:`applications_history`表存储完整申请快照（JSON），但：
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:95:- 存储空间浪费（每个申请可能有5-10个版本）
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:107:-- 查询申请历史
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:115:- 提交申请时（version=0）
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:122:1. **并发场景罕见**：同一申请同时被两个审批人操作的概率极低
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:157:   - `idx_student_id` (学生查看自己申请)
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:209:- **需要软删除**：用户数据、申请数据、附件（合规要求）
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:210:- **不需要软删除**：审批记录、通知（历史数据，不删除）
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:229:## 实施建议优先级
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:231:### P0 - 必须修改（阻塞实施）
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:247:**下一部分：** Part 2 - API与认证设计
docs/PROJECT-SUMMARY.md:1:# 毕业生离校申请审批系统 - 项目总结
docs/PROJECT-SUMMARY.md:5:**项目名称：** 毕业生离校申请审批系统  
docs/PROJECT-SUMMARY.md:6:**项目状态：** 设计审查完成（Round 1 + Round 2），待开始实施  
docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
docs/PROJECT-SUMMARY.md:21:- **认证：** 混合认证（学号+密码 + 微信OAuth2）+ 5项安全增强
docs/PROJECT-SUMMARY.md:35:- ✓ 确认系统集成需求（宿舍管理系统）
docs/PROJECT-SUMMARY.md:41:- ✓ 完成认证授权设计（RBAC权限模型）
docs/PROJECT-SUMMARY.md:42:- ✓ 完成审批流程设计（状态机、3个审批节点）
docs/PROJECT-SUMMARY.md:49:**实施计划：**
docs/PROJECT-SUMMARY.md:50:- ✓ 完成9个阶段的实施计划
docs/PROJECT-SUMMARY.md:55:- ✓ 预计工期：8-10周
docs/PROJECT-SUMMARY.md:66:- ✓ 审查第3、5、7、8、9、10章（API、审批、部署、安全、性能、测试）
docs/PROJECT-SUMMARY.md:71:- ✓ 批次3：第5章审批流程（工作日计算、字段更新、历史审计）
docs/PROJECT-SUMMARY.md:77:- ✓ 删除多数据库残留引用（PROJECT-SUMMARY、实施计划）
docs/PROJECT-SUMMARY.md:86:- ✓ 宿舍对接添加class_name和bed_number字段
docs/PROJECT-SUMMARY.md:92:- ✓ 修正CSV模板文件扩展名（.xlsx → .csv）
docs/PROJECT-SUMMARY.md:98:- ✓ P2修复：删除Postman引用、明确认证方式、统一审批时限、修改辅导员权限范围、统一性能指标
docs/PROJECT-SUMMARY.md:104:- ✓ 更新CSV模板（学生、辅导员、班级映射）
docs/PROJECT-SUMMARY.md:110:  - 5阶段实施计划
docs/PROJECT-SUMMARY.md:113:  - 包含3个文档+4个CSV模板
docs/PROJECT-SUMMARY.md:143:- ✓ 整理微信小程序申请说明（docs/微信小程序申请说明.md）
docs/PROJECT-SUMMARY.md:159:**Phase 1 实施（进行中）：**
docs/PROJECT-SUMMARY.md:177:- ✓ 达成最终共识：Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配（文档40）
docs/PROJECT-SUMMARY.md:179:  - 用户主数据通过CSV导入到本地数据库（非运行时API查询）
docs/PROJECT-SUMMARY.md:180:  - ImportSource接口用于数据导入（非运行时查询）
docs/PROJECT-SUMMARY.md:181:  - 宿舍清退保持实时API查询（可缓存、可降级）
docs/PROJECT-SUMMARY.md:183:  - 工期调整：10周演示版 + 1-2周生产集成缓冲
docs/PROJECT-SUMMARY.md:184:  - Week 1提前做数据契约和接口设计（避免返工）
docs/PROJECT-SUMMARY.md:193:2. **实施计划文档**
docs/PROJECT-SUMMARY.md:195:   - 内容：9个阶段的详细实施计划
docs/PROJECT-SUMMARY.md:196:   - 工期：8-10周
docs/PROJECT-SUMMARY.md:209:   - 内容：宿舍管理系统对接规范，包含API接口和数据文件两种方式
docs/PROJECT-SUMMARY.md:210:   - 受众：宿舍管理系统管理员、数据对接负责人
docs/PROJECT-SUMMARY.md:211:   - 附件：`docs/templates/宿舍清退数据模板.csv`
docs/PROJECT-SUMMARY.md:221:### 2. 离校申请
docs/PROJECT-SUMMARY.md:222:- 在线填写申请表
docs/PROJECT-SUMMARY.md:223:- 上传附件（宿舍清退证明、图书馆清书证明、财务结清截图）
docs/PROJECT-SUMMARY.md:224:- 申请状态跟踪
docs/PROJECT-SUMMARY.md:225:- 申请历史查询
docs/PROJECT-SUMMARY.md:227:### 3. 审批流程
docs/PROJECT-SUMMARY.md:228:- 两级审批（辅导员→学工部）
docs/PROJECT-SUMMARY.md:229:- 审批意见记录
docs/PROJECT-SUMMARY.md:241:- 审批状态变更通知
docs/PROJECT-SUMMARY.md:246:- 宿舍管理系统对接
docs/PROJECT-SUMMARY.md:255:2. **applications** - 离校申请表
docs/PROJECT-SUMMARY.md:256:3. **approvals** - 审批记录表
docs/PROJECT-SUMMARY.md:270:## 实施阶段
docs/PROJECT-SUMMARY.md:272:### 阶段1：项目初始化和基础设施（第1周）
docs/PROJECT-SUMMARY.md:278:### 阶段2：用户认证模块（第2周）
docs/PROJECT-SUMMARY.md:280:- 学号密码认证
docs/PROJECT-SUMMARY.md:281:- 微信OAuth2认证
docs/PROJECT-SUMMARY.md:284:### 阶段3：离校申请模块（第3周）
docs/PROJECT-SUMMARY.md:285:- 申请模型
docs/PROJECT-SUMMARY.md:287:- 申请CRUD API
docs/PROJECT-SUMMARY.md:288:- 申请提交逻辑
docs/PROJECT-SUMMARY.md:290:### 阶段4：审批管理模块（第4周）
docs/PROJECT-SUMMARY.md:291:- 审批记录模型
docs/PROJECT-SUMMARY.md:292:- 审批API
docs/PROJECT-SUMMARY.md:293:- 审批流程逻辑
docs/PROJECT-SUMMARY.md:296:### 阶段5：附件管理模块（第5周）
docs/PROJECT-SUMMARY.md:301:### 阶段6：通知模块（第6周）
docs/PROJECT-SUMMARY.md:307:### 阶段7：外部系统集成（第7周）
docs/PROJECT-SUMMARY.md:309:- 宿舍系统对接
docs/PROJECT-SUMMARY.md:313:### 阶段8：前端开发（第8-9周）
docs/PROJECT-SUMMARY.md:317:### 阶段9：测试和部署（第10周）
docs/PROJECT-SUMMARY.md:326:1. **审查设计和计划**
docs/PROJECT-SUMMARY.md:328:   - 确认实施计划可行
docs/PROJECT-SUMMARY.md:333:   - 申请微信公众平台账号
docs/PROJECT-SUMMARY.md:335:3. **开始实施**
docs/PROJECT-SUMMARY.md:336:   - 按照实施计划执行
docs/PROJECT-SUMMARY.md:343:2. **微信公众平台审核延迟** - 提前申请账号
docs/PROJECT-SUMMARY.md:351:- **预计工期：** 8-10周
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:5:**分析目的：** 实施前最终审查，确保设计完整性和可实施性
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:12:- ✓ Round 1审查：架构、认证、数据库、外部集成（2 CRITICAL + 8 MAJOR）
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:13:- ✓ Round 2审查：API、审批、部署、安全、性能、测试（2 CRITICAL + 21 MAJOR + 6 MINOR）
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:18:- 实施计划：9个阶段，8-10周工期
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:60:- [ ] 认证授权机制是否完整？
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:70:### 4. 审批流程审查
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:82:- 乐观锁防止并发审批
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:83:- 审批历史追踪（applications_history表）
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:88:- [ ] 宿舍管理系统对接方案是否可行？
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:118:- [ ] 5项认证安全增强是否充分？
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:160:### 10. 实施计划审查
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:164:- [ ] 8-10周工期是否现实？
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:170:- Phase 1: 项目初始化（1周）
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:171:- Phase 2-7: 核心模块开发（6周）
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:172:- Phase 8: 前端开发（2周）
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:173:- Phase 9: 测试部署（1周）
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:207:- **CRITICAL：** 阻塞实施，必须修复
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:215:### 1. 实施可行性
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:243:5. **最终确认：** 确认设计可以开始实施
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:15:3. 实施计划文档
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:22:以下内容虽然在计划中出现，但尚未执行，因此本次不评价实现质量：
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:29:- 用户认证模块
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:30:- 申请/审批/附件/通知/集成模块
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:52:- 学生在线提交离校申请
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:53:- 辅导员一级审批
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:57:- 宿舍管理系统对接
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:65:- 认证：学号密码 + 微信 OAuth2
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:89:- 认证授权设计
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:90:- 审批流程设计
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:104:4. 审批流程具备状态机意识：草稿、待辅导员、待学工部、通过、驳回等状态明确。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:119:   例如字段声明 `NOT NULL`，外键又写 `ON DELETE SET NULL`。这在数据库层面互相冲突。审批记录、审计日志这类历史数据建议优先使用软删除或 `PROTECT/RESTRICT`，避免历史记录失真。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:131:   Access Token 设计为 7 天。对审批和个人信息系统而言，这个时长偏长。虽然尚未实现，但它属于已完成认证设计的一部分，建议在设计文档阶段调整。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:135:## 5. 实施计划文档
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:139:`docs/superpowers/plans/2026-05-27-implementation-plan.md` 已完成 9 个阶段的实施规划：
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:142:2. 用户认证模块
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:143:3. 离校申请模块
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:144:4. 审批管理模块
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:151:计划中包含任务清单、验证标准、风险和缓解措施、交付物和协作建议。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:155:实施计划的结构是完整的，能够作为项目排期和任务拆分的基础。它的优点是分阶段清楚，每阶段都有验证标准，且把测试、部署、文档和质量工具纳入计划。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:157:### 已完成计划中的问题
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:159:1. **计划仍残留“多数据库支持”**
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:161:   这与评审共识冲突。计划文档中仍写有“多数据库支持”“配置数据库连接（支持多数据库）”“配置 MySQL/PostgreSQL 服务”等内容。由于实施计划已经完成，这属于已完成计划文档的口径问题，应修正。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:165:   计划中写支持 `1000+` 并发用户，而设计文档和评审共识已经收敛为单实例峰值 500 并发用户。建议统一为 500 并发用户。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:169:   Phase 1 同时包含 Django 初始化、Docker、Celery、开发工具等任务。作为计划本身没有问题，但当前已完成部分只覆盖了目录、`.gitignore`、requirements。项目总结中已经正确标注其余任务为暂停/待继续。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:187:**Round 2：API、审批、部署、安全、性能、测试**
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:191:- 补充审批工作日计算、字段更新、历史审计
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:197:设计审查是当前已完成工作中质量最高的部分。它不仅列出了问题，还形成了回应、确认和共识摘要。这个过程已经把项目从初始设想推进到了更可实施的技术方案。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:230:目录结构与实施计划基本一致，能够承接 Django 后端、移动端、小程序、Docker 配置等后续工作。当前为空目录是正常状态，因为只完成了结构创建。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:302:4. 实施计划性能目标与设计共识不一致。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:316:其中设计审查的质量较高，已经解决了多个关键架构方向问题；但文档回填还没有完全收敛，导致项目总结、系统设计、实施计划之间仍有若干冲突。
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:329:- 权限和认证实现
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:330:- 审批状态机实现
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md:333:- 宿舍系统对接实现
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:16:- 实施计划文档
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:20:**不分析：** 未实施的代码、未完成的功能
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:24:**关注点：** 设计方案的可实施性  
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:46:| "多数据库支持"残留 | 总结、计划文档 | 口径冲突 |
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:50:| 性能目标不一致（1000+ vs 500） | 计划 vs 设计 | 口径冲突 |
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:55:这些是**设计方案本身**的实施风险：
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:60:| CRITICAL | 5项微信绑定安全措施过度 | 实施复杂、依赖外部服务 |
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:81:   - Codex: "计划1000+，设计500，应统一"
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:108:- Claude从实施角度认为该表冗余
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:121:- Claude从实施成本角度质疑
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:123:**建议：** 需要权衡安全性和实施成本
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:141:### P0 - 立即修改（阻塞实施）
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:169:18. 推迟Celery实施
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:170:19. 推迟乐观锁实施
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:199:**Claude倾向：** 简化为2项（实施成本）
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:244:- 更新实施计划
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:10:`29-data-source-analysis.md` 的方向是正确的：当前数据对接文档只覆盖宿舍清退，无法完整支撑 student、counselor、admin 三类角色的账号初始化、权限边界和自动审批分配。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:14:1. **班级-辅导员对应关系应明确列为 P0。** 这是自动分配审批人的核心数据。没有它，系统提交申请时无法稳定设置 `counselor_id` 和 `current_approver_id`，只能退化为人工逐个配置或人工改派。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:15:2. **首版不应追求所有数据源 API 化。** 对约 1000 名学生、约 50 名辅导员、约 5 名管理员的规模，CSV/Excel 批量导入加严格校验更现实；API 更适合作为后续自动化增强。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:25:| 学生基本信息 | 教务系统 | P0 | 用于创建学生账号、身份识别、展示院系专业班级、限定毕业离校申请人范围。用户设计说明书已出现“学号、姓名、专业、班级”和“批量导入学生用户”的要求，因此必须写入数据对接文档。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:26:| 辅导员基本信息 | 人事系统或人工台账 | P0 | 用于创建 counselor 账号和审批权限主体。实时同步不是 P0，但账号数据本身是 P0。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:27:| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:28:| 宿舍清退数据 | 宿管系统 | P0 | 当前业务把宿舍清退作为提交前校验项，现有对接文档已覆盖。即使保留人工证明降级，正式流程仍应具备自动校验或批量数据导入能力。 |
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
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:104:3. **账号生命周期。** 需要定义新增、更新、停用、毕业归档、辅导员离职/调岗、管理员离岗后的处理规则。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:108:5. **审批人变更后的历史一致性。** 已提交申请中的 `counselor_id` 应保持历史一致，不应因后续班级映射变更自动改写。若需改派，应由管理员显式操作并记录审计日志。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:110:6. **多辅导员和代理审批。** 现实中可能有主辅导员、代管辅导员、临时代理。首版可只要求一个主审批人，但后台应预留人工改派能力。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:112:7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:114:8. **离校批次配置。** 开放申请时间、允许离校日期范围、毕业届别可能来自业务配置，而不一定来自教务系统。应作为系统配置纳入实施计划。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:124:## 六、建议实施顺序
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:126:1. **重构数据对接说明文档目录。** 从单一“宿舍对接”扩展为“账号基础数据、审批关系数据、业务校验数据、降级与审计”四类。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:128:2. **定义学生基本信息导入模板。** 先支持 CSV/Excel 导入当届毕业生，包含毕业资格字段和班级唯一标识。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:134:5. **保留并完善宿舍清退对接。** 当前文档已较完整，下一步应把它纳入统一的校验结果、缓存、失败降级和审计机制。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:150:1. 新增“学生基本信息导入”章节，提供 CSV/Excel 模板字段。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:153:4. 将“宿舍清退数据”保留为业务校验数据，并补充与人工证明降级的关系。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:162:- **P0 数据：** 学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据、毕业资格字段。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:164:- **首版策略：** 账号和映射数据用 CSV/Excel 批量导入，宿舍清退优先 API，管理员手动维护，图书馆/财务继续截图上传。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:165:- **最高优先级行动：** 立即补充班级-辅导员映射的数据规范和导入校验，这是自动审批闭环的关键缺口。
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:5:**审查范围：** API设计、审批流程、部署架构、安全设计、性能优化、测试策略
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:17:### 1. 申请编号生成时机
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:51:- 添加审批API版本检查
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:55:### 批次3：审批流程
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:17:2. **设计层面**：部分设计过度复杂，实施风险高（微信绑定、性能目标、冗余表）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:235:-- 1. 提交申请（milestone='submitted'）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:250:**最终决策：** ✓ 渐进式实施
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:261:**Phase 1实施：**
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:295:- 过度安全措施增加实施成本
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:305:**Phase 1实施：**
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:366:    """检查审批超时（简化版）"""
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:433:+ 核心模块强制TDD：认证、审批、状态机
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:438:## 第四部分：实施路线图
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:440:### Phase 1：文档修正 + 简化设计（第1周）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:455:- ✓ 推迟Celery实施
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:460:### Phase 2：核心功能开发（第2-7周）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:473:### Phase 3：优化增强（第8-9周）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:485:### Phase 4：测试部署（第10周）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:541:| 实施复杂度 | 8/10 | 6/10 | -2（简化） |
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:551:| 实施延期 | 高 | 中 | 简化设计+渐进式 |
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:557:**✓ 可以开始实施**
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:25:- ✅ 从外部数据库读取数据（如宿舍清退状态）
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:28:- 学校A宿舍系统用MySQL
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:29:- 学校B宿舍系统用SQL Server
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:30:- 学校C宿舍系统用Oracle
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:5:**审查范围：** 系统架构、认证授权、数据库设计、外部系统集成
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:11:**所有审查部分已达成共识，可以进入实施阶段。**
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:23:- 对接外部系统的多种数据库（宿舍管理系统等）
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:53:### 1.5 审批超时监控
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:57:- 排除周末和节假日
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:70:## 第2部分：认证授权修改（5项强制性安全增强）
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:199:### 3.6 活跃申请唯一约束
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:212:            raise ValidationError("您已有进行中的申请，请等待审批完成")
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:297:## 实施优先级
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:301:- ✅ 所有认证安全增强
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:319:2. ✅ 更新实施计划（反映新的技术方案）
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:321:4. ⏸ 开始Phase 1实施
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:16:- 软删除用户后，其申请仍然存在，指向"已删除"用户 ✓
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:27:**实施细节：**
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:49:        on_delete=models.PROTECT,  # 有申请时阻止删除
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:59:            raise ValidationError("该用户有待审批申请，无法删除")
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:17:5. ✓ P2 - 明确认证方式（API Key + IP白名单）
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:18:6. ✓ P2 - 统一审批时限（1个工作日）
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:88:Postman集合文件：`docs/templates/宿舍管理系统API.postman_collection.json`
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:98:### 修复5：明确认证方式 [P2]
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:104:**认证方式：** 
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:105:- API Key认证（推荐）
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:106:- 或 Basic Auth认证
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:112:**认证方式：** API Key + IP白名单
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:124:### 修复6：统一审批时限 [P2]
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:130:- 辅导员审批：提交后24小时内
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:131:- 学工部审批：辅导员通过后24小时内
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:136:- 辅导员审批：提交后1个工作日内
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:137:- 学工部审批：辅导员通过后1个工作日内
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:151:- 查看本年级学生的申请列表
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:152:- 审批本年级学生的申请
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:153:- 审批其他年级学生
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:159:- 查看负责班级学生的申请列表
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:160:- 审批负责班级学生的申请
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:161:- 审批其他班级学生
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:190:**实施方案：**
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:205:- ✓ `docs/用户设计说明书.md` - 初始密码、审批时限、辅导员权限、性能指标
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:206:- ✓ `docs/数据对接说明文档.md` - HTTPS要求、认证方式、id_card参数、Postman引用
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:221:**可以进入实施阶段。**
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:63:    # 新增：固定审批人追踪
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:131:### 5. users表缺少认证安全字段 - **完全同意**
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:133:**立场：** 完全同意。这些字段是Round 1-3认证改进的必需部分。
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:143:    # 新增：认证安全字段
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:184:### 6. 缺少活跃申请的唯一约束 - **同意，采纳Django应用层方案**
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:188:**实施：**
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:194:        # 检查活跃申请唯一性
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:203:                raise ValidationError("您已有进行中的申请，请等待审批完成")
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:11:用户提出在宿舍管理系统数据对接中，需要补充以下字段：
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:18:   - 用途：精确定位学生宿舍床位
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:20:   - 说明：可选字段，如果宿舍管理系统有床号信息则提供
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:67:**修改位置6：CSV格式示例**
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:69:CSV添加班级和床号列：
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:71:学号,姓名,班级,宿舍楼栋,宿舍房间号,床号,是否已清退,清退日期,清退状态,备注
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:74:### 2.2 CSV模板文件（`docs/templates/宿舍清退数据模板.csv`）
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:76:更新CSV模板，添加班级和床号列，包含示例数据。
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:80:**修改位置：第6.2节 - 宿舍管理系统对接 - 接口定义（第1629-1639行）**
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:123:  - 优点：精确定位学生宿舍位置
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:124:  - 缺点：不是所有宿舍管理系统都有床号信息
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:138:- 宿舍信息：dorm_building、dorm_room、bed_number
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:159:- ✓ CSV模板文件
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:164:- [ ] 实施计划文档（可能不需要）
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:178:- API响应的class_name：宿舍管理系统返回的班级（可能不同步）
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:191:- 场景3：需要统计各宿舍楼的离校情况，需要存储
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:4:**分析范围：** 仓库全部可见文件、设计文档、实施计划、评审讨论记录、依赖文件、目录结构  
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:11:当前仓库已经完成较完整的需求、系统设计、实施计划和多轮评审共识，核心方向基本清晰：Django + DRF 单体后端、PostgreSQL 单数据库、Redis + Celery、本地文件存储、微信登录/通知、宿舍系统优先 API 对接。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:15:最大风险不是“功能缺少”，而是设计文档和实施计划中仍存在多处与既定共识冲突的细节。如果直接按当前计划开工，容易把已经达成的 PostgreSQL 单数据库、单实例部署、文件安全、工作日计算、测试目标等决策重新做偏。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:61:- 认证授权
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:62:- 审批流程
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:76:- 认证安全补充
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:82:这部分文档是当前项目最有价值的决策记录，应当作为实施基线。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:92:### 4.1 实施计划仍然残留“多数据库支持”
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:96:但实施计划仍写着：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:102:这会直接误导 Phase 1，把核心数据库支持做复杂。建议立即把实施计划改成：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:115:但实施计划仍写：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:193:- 审批记录和审计日志优先保留历史，用户删除应使用软删除或 `PROTECT`
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:226:### 6.6 “活跃申请唯一约束”没有落到设计主文档
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:228:共识文档提到“一个学生只能有一个进行中申请”。设计主文档没有在 applications 表中明确部分唯一索引，仅在流程逻辑中描述。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:240:### 6.7 审批超时动作与枚举不一致
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:242:approvals 表字段说明写 `action: approve/reject`，但超时任务会创建 `action='timeout'`。需要把 `timeout` 加入枚举，或把超时记录拆成独立 `approval_timeouts`/notification 事件，避免审批记录语义混乱。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:246:审批记录字段说明写“1个工作日(24小时)”，第 5 章又写“1个工作日 = 8小时工作时间”。建议统一为：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:278:审批 API 已有 `version` 字段和 409 响应，但更新申请、重新提交、附件变更、生成凭证等也可能改变申请状态或可审批性。建议明确所有会影响审批判断的写操作都必须纳入版本控制。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:282:RBAC 描述中学生只能“修改草稿状态的申请”，但流程允许 rejected 重新提交。需要明确：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:291:文档写“辅导员查看本年级所有申请”。实际高校场景通常按学院、专业、班级、辅导员负责范围授权，仅年级不足以防止越权。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:293:建议新增 `counselor_assignments` 或在用户/班级模型中维护负责关系，并在查询和审批时同时校验 `current_approver_id`。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:305:## 8. 认证与安全风险
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:309:设计中 Access Token 有效期为 7 天，Refresh Token 30 天。对审批、附件、个人信息系统来说，7 天 access token 偏长。建议：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:377:### 9.3 宿舍系统字段契约不足
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:384:- 人工跳过验证的审批责任归属
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:385:- 外部系统不可用时是否允许提交还是只允许审批时跳过
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:452:单实例 Gunicorn 4 workers 下，`500 并发用户` 与 `>500 QPS` 可能对只读列表接口可达，但对审批写入、附件上传、外部系统调用不现实。建议性能指标按接口分类：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:455:- 申请列表：P95/QPS
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:456:- 申请提交：P95/QPS
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:457:- 审批操作：P95/QPS
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:463:设计中缓存申请详情、申请状态、学生申请列表。对含个人信息和审批信息的数据，必须保证：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:473:设计列了很多单列索引和复合索引。实施时不建议一次性照搬所有索引，应先根据核心查询建立最小索引集：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:475:- 学生申请列表
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:476:- 审批人待办列表
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:479:- 附件按申请查询
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:494:- dev requirements 缺少 `pytest-mock`、`bandit`、`pre-commit`、`locust` 等计划中提到或实际需要的工具
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:509:当前前端仅有空目录。设计计划同时做 React Native 和微信小程序，但需求里明确“挂在微信公众号”，小程序很可能是首要交付端。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:515:3. 附件上传、微信授权、Token 刷新、审批待办这四个流程应先做端到端原型。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:516:4. React Native 与小程序不要在第 8-9 周才开始完全介入，至少要在后端 API 定稿时同步验证登录和上传能力。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:524:1. 更新实施计划，移除本项目“多数据库支持”和 MySQL/PostgreSQL 并列部署说法。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:529:6. 明确软删除 + 唯一约束 + 活跃申请唯一约束的 PostgreSQL 实现。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:539:### P2：业务模块实施前应定稿
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:543:3. 审批状态机：明确 rejected 重新提交、version 递增、附件替换规则。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:545:5. 宿舍系统集成契约：状态码、超时、降级、人工跳过责任。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:551:建议下一次实施直接按以下顺序推进：
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:553:1. 清理并更新文档漂移：实施计划、项目总结、设计第 6 章。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:573:项目方向是可行的，设计深度已经足够进入实施；但在进入编码前，需要先消除文档和计划中的旧决策残留。尤其是数据库、依赖、部署和认证安全这四类问题，如果不先统一，会在 Phase 1 产生结构性返工。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:577:> 设计评审完成，实施骨架初建；尚未达到“项目初始化完成”。
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:24:当宿舍系统不一定提供班级信息时，文件导入字段表已把 `class_name` 标为"否"（非必填），但 API 响应字段表只给 `bed_number` 标注了"可选"，会让接口实现方把 `class_name` 误认为必返字段。
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:27:接口实现方可能将class_name作为必填字段处理，导致宿舍系统无法提供班级信息时接口调用失败。
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:31:- 方案B：在所有文档中统一改为必填（需确认宿舍系统一定能提供）
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:40:在"李四"这一行，表头只有 10 列，但当前内容在 `否` 后面放了两个空单元格，导致该行变成 11 列，`未开始` 和备注列会错位；这也与下面的 CSV 示例不一致。
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:72:- **bed_number字段：** 精确定位学生宿舍床位，便于宿舍管理，添加合理
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:84:- ✓ CSV模板文件
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:111:- users表已有class_name字段，API响应中的class_name来自宿舍系统
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:119:  - 如果需要统计各宿舍楼离校情况：需要存储
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:23:- 宿舍系统可能无法提供班级信息（不同学校系统差异）
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:103:   - [ ] 检查Excel/CSV示例格式正确
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:116:| dorm_building | String | 宿舍楼栋 | 是 | "1号楼" |
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:117:| dorm_room | String | 宿舍房间号 | 是 | "101" |
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:11:发现2个CRITICAL问题和4个MAJOR问题，阻止实施。
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:34:### 2. 混合认证存在账户接管漏洞
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:39:- 允许学号+密码 AND 微信OpenID同时认证同一用户
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:80:- DoS审批队列（垃圾申请提交）
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:128:### 5. 审批超时监控不完整
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:132:- 当前实现计算周末，导致误报
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:140:    """计算截止时间，排除周末和中国节假日"""
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:168:- 无回滚计划（辅导员误批准）
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:169:- 无批量操作（辅导员审批50个申请需点击50次）
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:174:- 无申请撤回功能
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:175:- 无审批重新分配
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:13:所有CRITICAL和MAJOR问题已解决。数据库设计可以进入实施阶段。
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:29:- ✅ 覆盖审批队列、通知查询、审计追踪
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:45:- ✅ 所有认证安全字段已添加
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:49:**6. 活跃申请约束**
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:108:2. 认证/授权实现
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
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:125:- `pending`：清退中（已申请但未完成）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:143:- 系统允许学生提交申请，但需上传宿舍清退证明截图
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:151:- 审批权限管理
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:166:- `employee_id`：辅导员工号，必须全校唯一，与统一身份认证、人事系统工号一致
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:167:- `is_active`：标识是否在职，`false`时不能登录、不能审批，但历史记录可查询
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:169:**CSV模板示例：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:183:| 账号状态 | 登录 | 创建申请 | 审批 | 查看历史 | 接收通知 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:193:- 学生提交申请时自动分配辅导员审批人
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:217:**CSV模板示例：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:228:- 导入后输出校验报告：未匹配班级、未匹配辅导员、重复映射、无审批人的学生数
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:231:- 已提交申请的 `counselor_id` 不自动改写，保持历史一致性
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:232:- 新提交申请使用新映射
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:267:### 3.1 CSV/Excel导入（首版推荐）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:278:- 格式：CSV或Excel（.xlsx）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:286:1. CSV导入到临时staging表（按类型拆分）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:331:-- 2. 导入CSV到staging表
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:406:- 宿舍清退数据（实时校验）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:413:- 认证：API Key或OAuth2
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:428:- 401：认证失败
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:479:| 申请记录 | 当届申请 | 1000条/届 | 每个学生最多1个进行中申请 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:489:    application_start_date DATE,                -- 申请开放时间
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:490:    application_end_date DATE,                  -- 申请截止时间
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:521:5. 辅导员工号（`employee_id`）是否全校唯一？是否与统一身份认证、人事系统工号一致？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:522:6. 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:531:9. 优先推荐的对接方式是什么？（DB直连 / API / CSV导入）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:533:11. CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:538:13. 是否有统一身份认证或微信绑定前置要求？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:541:**实施保障确认：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:547:## 六、实施建议
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:551:首版采用**CSV/Excel导入 + 宿舍清退API**组合方案：
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:552:- 学生、辅导员、班级映射：CSV/Excel批量导入
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:553:- 宿舍清退数据：API实时查询
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:556:**实施路径（v2修订）：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:558:**阶段1：数据确认（1周）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:564:**阶段2：CSV导入实现（2周）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:565:1. 设计三份CSV模板：学生、辅导员、班级-辅导员映射
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:566:2. 实现CSV导入功能和校验逻辑
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:573:**阶段3：宿舍清退API对接（1周）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:574:1. 对接宿管系统宿舍清退API
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:578:**阶段4：上线前验收（1周）**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:722:1. ✅ CSV导入策略从"全量覆盖"改为"staging + upsert + 软停用"
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:725:4. ✅ 认证约束调整：支持CSV预导入账号（password_setup_required）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:726:5. ✅ 对接方式调整：学生/辅导员/班级映射改为CSV首版优先
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md:732:3. 启动实施（按六章节的5阶段路径）
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:15:我们认同这5个问题都是实施级关键缺陷，必须在v2文档中修正。
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:129:- 行241-243：申请提交时查询该表
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:216:### 2.3 问题3：认证约束冲突（行293-295）
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:218:**Codex意见：** 主设计中 `users` 表有 `chk_auth_method` 约束，要求 `password_hash` 或 `wechat_openid` 非空；CSV预导入账号通常还没有密码或微信绑定，会被约束挡住。
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:231:CSV导入场景：
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:232:1. 学生CSV导入：只有学号、姓名等基本信息，没有密码或微信openid
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:235:**修正方案：调整认证约束，允许预导入账号**
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:246:    -- 认证状态字段
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:259:    -- 修正后的认证约束：允许预导入账号
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:276:修正后的 `chk_auth_method` 允许三种认证状态：
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:281:**CSV导入时的处理：**
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:323:    """统一认证入口"""
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:339:    # 检查认证方式
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:384:        raise ValueError(f"CSV校验失败，共 {len(errors)} 个错误")
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:469:3. ✅ 调整认证约束，增加password_setup_required支持CSV导入
docs/discussions/codex-review-2026-05-27/35-response-to-codex-critical-issues.md:481:修正完成后，方向和实施细节都已明确，可以基于此创建v2共识文档。
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:5:**审查范围：** API设计、审批流程、部署架构、安全设计、性能优化、测试策略
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:15:- 认证增强：5项安全措施
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:39:3. **MAJOR**: 申请编号生成时机不一致：
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:44:4. **MAJOR**: 审批API（lines 907-945）缺少：
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:46:   - 当前审批人验证
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:63:- 审批/更新端点要求`version`或`If-Match`
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:64:- 文档化角色范围列表语义：学生查看自己记录，辅导员查看分配年级/当前审批人，管理员查看全部
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:68:## 第5章：审批流程设计
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:76:   - 排除周末/节假日
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:91:   - 提交/审批/驳回的审计日志
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:94:5. **MAJOR**: 提交时生成申请编号（line 1256）与API创建和数据库`NOT NULL`冲突
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:96:6. **MINOR**: 强制上传宿舍证明（line 1251）应与外部宿舍系统验证和手动降级协调（lines 1332-1333, 1512-1514）
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:99:- 按审批节点跟踪超时，不是从原始提交时间
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:101:- 每次状态转换：验证状态+角色+当前审批人，锁定或检查版本，写入approval/audit/history行，更新`current_approver_id`
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:159:3. **MAJOR**: 认证安全章节（lines 1719-1731）未包含最终确定的5项微信/认证加固措施（lines 1101-1106）
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:186:3. **MINOR**: 缓存申请状态（lines 1778-1782）可能产生过期审批视图
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:193:- 用最终确定的数据库索引替换索引列表，并将每个映射到其查询：待审批、学生列表、未读通知、审计查找
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:206:   - 实施计划要求"每个功能先写测试，再写实现"（lines 662-663）
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:211:3. **MAJOR**: 缺少5项认证加固措施的测试：
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:234:- 添加双重审批和微信绑定竞态的并发测试
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:243:- 第5章（审批流程）：REVISE - 5个MAJOR问题
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:34:3. ✅ **MAJOR - 申请编号生成时机不一致**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:40:4. ✅ **MAJOR - 审批API缺少版本检查**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:44:   - 将添加：当前审批人验证
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:56:**修改计划：**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:59:- 修改申请创建API（不返回application_no）
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:60:- 添加审批API版本检查
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:66:## 第5章：审批流程设计 - 响应
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:75:   - 将添加：工作时间9:00-17:00，排除周末/节假日
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:81:3. ✅ **MAJOR - 工作流未设置审批人字段**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:92:5. ✅ **MAJOR - 申请编号生成时机冲突**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:94:   - 将保持：提交时生成申请编号
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:96:6. ✅ **MINOR - 宿舍证明上传与外部验证协调**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:100:**修改计划：**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:132:**修改计划：**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:157:3. ✅ **MAJOR - 认证安全未包含5项加固措施**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:169:**修改计划：**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:175:- 更新认证安全章节
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:203:**修改计划：**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:225:3. ✅ **MAJOR - 缺少认证加固测试**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:241:**修改计划：**
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:244:- 添加认证安全测试用例
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:260:- 第5章审批流程（工作日、字段更新、历史、审计）
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:263:- 第8章安全设计（限流、上传、认证、审计）
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
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:114:- 学生提交申请时，系统根据班级自动找到对应辅导员
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
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:1:# Round 3 Claude分析 - Part 2: API与认证设计
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:5:**分析范围：** 第3-4章（API设计、认证授权设计）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:81:  "message": "文件已存在，已关联到申请",
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:105:## 第4章：认证授权设计
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:127:- 实施复杂度大幅增加
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:138:- ❌ 学生身份验证：Phase 1不实施，依赖管理员导入用户
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:171:1. **辅导员权限范围不明确**：能否查看其他年级申请？
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:172:2. **学工部权限过大**：admin既能审批又能管理系统配置
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:182:admin_approver   # 学工部审批员（只能审批）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:183:admin_manager    # 学工部管理员（审批+配置管理）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:192:        # 只能查看本年级学生申请
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:215:- ✓ 双通道认证设计合理
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:228:## 实施建议优先级
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:230:### P0 - 必须修改（阻塞实施）
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md:246:**下一部分：** Part 3 - 审批流程与外部集成
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:6:**审查周期：** 37 → 38 → 39 → 40
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:12:**方案名称：** Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:15:1. 用户主数据（学生、辅导员、班级映射）通过CSV导入到本地数据库
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:16:2. ImportSource接口用于数据导入，不是运行时查询
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:17:3. 宿舍清退状态通过API实时查询（可缓存、可降级）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:18:4. 本地数据库是认证、权限、审批的唯一运行时依据
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:29:外部数据源 (CSV/API/Mock)
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:31:ImportSource (数据导入源接口)
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:35:本地数据库 (认证、权限、审批的唯一运行时依据)
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:38:DormCheckoutProvider (宿舍清退实时查询)
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:45:class IUserDataImportSource(ABC):
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:62:# 2. 宿舍清退Provider（用于运行时查询）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:64:    """宿舍清退状态提供者接口"""
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:67:        """运行时查询宿舍清退状态"""
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:77:    def __init__(self, source: IUserDataImportSource):
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:149:USER_DATA_SOURCE = 'csv'  # 生产环境使用CSV导入
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:150:DORM_CHECKOUT_SOURCE = 'api'  # 宿舍清退使用API
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:178:## 四、实施计划
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:182:| 周次 | 任务 | 交付物 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:184:| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:185:| Week 2-3 | CSV导入功能、staging表、upsert逻辑、审计日志 | CSV导入模块、导入校验报告 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:186:| Week 3-6 | 申请、审批、附件、通知模块 | 核心业务功能 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:187:| Week 6-7 | 宿舍清退Provider、降级流程、缓存、错误分类 | 宿舍清退集成模块 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:188:| Week 8-9 | 前端开发 | React Native、微信小程序 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:189:| Week 10 | 联调、演示、验收清单 | 可演示版本（Mock数据） |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:192:- 宿舍清退API集成：1周
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:193:- 用户主数据API替换CSV（如需）：另计2-4周
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:195:**总工期：** 10周演示版 + 1-2周生产集成缓冲
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:199:1. **Week 1结束：** 数据契约冻结，接口定义完成
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:200:2. **Week 3结束：** CSV导入功能可用，种子数据就绪
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:201:3. **Week 6结束：** 核心业务逻辑完成
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:202:4. **Week 7结束：** 宿舍清退API对接完成
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:203:5. **Week 10结束：** 可演示版本交付
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:244:- **宿舍清退状态：** 覆盖所有枚举值（completed/pending/not_started/unknown）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:256:### 6.2 宿舍清退状态缓存
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:261:- **提交申请前：** 必须重新校验
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:269:- 认证失败（401）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:306:| RealUserDataProvider运行时查询 | CSV导入到本地数据库 | 用户主数据是基础数据，不应依赖外部API |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:308:| 10周 + 3天 | 10周演示版 + 1-2周生产集成 | 更现实的工期评估 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:309:| Week 7做接口抽象 | Week 1做数据契约和接口 | 避免后续返工 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:310:| Provider用于运行时查询 | ImportSource用于数据导入 | 明确职责边界 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:314:1. **不要偏离已达成的共识** - 原方案错误地将用户主数据API化，偏离了CSV导入的共识
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:324:### 9.1 Week 10交付物
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:328:- [ ] CSV导入功能和校验逻辑
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:329:- [ ] 宿舍清退API适配器（Mock实现）
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:351:| 真实API字段与Mock不一致 | P1 | Week 1冻结数据契约，预留扩展字段 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:354:| API认证复杂度超预期 | P2 | 预留1-2天调试时间 |
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:358:- **API延期：** 首版坚持CSV导入，不等待API
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:377:1. **立即执行：** 更新实施计划文档
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:378:2. **Week 1启动：** 数据契约和接口设计
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:379:3. **Week 2-3：** CSV导入功能开发
docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:391:- Claude Opus 4.7 - 方案设计与实施
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:16:- 准备开始Phase 1实施
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:20:- 原设计采用CSV导入用户数据（学生、辅导员、班级）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:22:- 宿舍管理系统只提供了一个第三方API文档（goliveplus租户用户查询API）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:23:- 该API字段不满足需求（缺少班级、院系、专业、宿舍清退状态等）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:26:1. 完整的API文档（学生信息、辅导员信息、宿舍清退状态）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:27:2. API认证信息（appKey、appSecret、签名算法）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:43:- Phase 2: 用户认证模块（可用Mock数据）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:44:- Phase 3: 离校申请模块
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:45:- Phase 4: 审批管理模块
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:80:    """宿舍清退状态提供者接口"""
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:83:        """查询学生宿舍清退状态"""
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:192:### 2.3 实施计划
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:194:**阶段1：不等API（10周）**
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:196:| 周次 | 任务 | 交付物 |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:198:| Week 1-2 | 基础设施 + Mock数据 | Django项目、种子数据（100学生、10辅导员） |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:199:| Week 3-6 | 核心业务逻辑 | 申请、审批、附件、通知模块 |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:200:| Week 7 | 接口抽象层 | Provider接口、MockProvider、缓存框架 |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:201:| Week 8-9 | 前端开发 | React Native、微信小程序（测试AppID） |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:202:| Week 10 | 测试 | 单元测试、集成测试（Mock数据） |
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:226:2. **分阶段交付** - 10周可交付演示版
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:238:- API认证复杂度超预期 → 可能需要额外调试时间（1-2天）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:285:**问题7：10周 + 3天工期是否合理？**
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:300:- 缓存失效处理是否考虑周全？
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:353:1. 10周 + 3天工期是否合理
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:370:3. 实施难度和工期评估
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:394:- **项目名称：** 毕业生离校申请审批系统
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:397:- **预计工期：** 8-10周（原计划）
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:398:- **当前状态：** 设计完成，准备实施
docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md:403:- Round 2: API、审批、部署、安全、性能（29个问题修复）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:6:**优先级：** P0（决定实施路径）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:17:- ✓ 达成最终共识：Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:18:- ✓ 工期调整：10周演示版 + 1-2周生产集成缓冲
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:22:外部数据源 (CSV/API/Mock)
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:24:ImportSource (数据导入源接口)
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:28:本地数据库 (认证、权限、审批的唯一运行时依据)
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:31:DormCheckoutProvider (宿舍清退实时查询)
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:37:1. 更新实施计划文档（调整Week 1-10任务分配）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:38:2. 开始Week 1工作：数据契约、DTO、ImportSource接口设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:47:3. **探索替代方案** - 寻找更好的实施路径
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:63:1. **立即执行：** 更新实施计划文档
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:64:   - 调整Week 1-10任务分配
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:65:   - 将数据契约和接口设计提前到Week 1
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:66:   - 明确每周交付物
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:68:2. **Week 1启动：** 数据契约和接口设计
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:70:   - 设计IUserDataImportSource接口
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:74:3. **Week 2-3：** CSV导入功能开发
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:88:- Week 1的工作量是否合理？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:95:### 4.1 关于实施顺序
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:97:**问题1：Week 1做数据契约是否太晚？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:98:- 数据契约影响认证、审批、前端所有模块
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:99:- 是否应该在Week 1之前（现在）就冻结数据契约？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:100:- 如果现在冻结，Week 1可以做什么？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:103:- 当前计划是按模块顺序开发（认证→申请→审批→...）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:105:- 例如：简化版申请+审批+通知，验证整体架构
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:107:**问题3：CSV导入功能是否应该更早？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:108:- 当前计划Week 2-3做CSV导入
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:109:- 但认证模块（Week 2）需要用户数据
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:110:- 是否应该Week 1就完成CSV导入？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:115:- 当前计划用种子数据（100学生、10辅导员）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:120:- ImportSource、ImportService、Provider三层抽象
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:121:- 对于首版（CSV导入）是否过于复杂？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:122:- 是否应该先实现CSV导入，后续再抽象？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:124:**问题6：宿舍清退API集成时机？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:125:- 当前计划Week 6-7做宿舍清退API对接
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:126:- 但申请提交（Week 3）就需要校验宿舍清退状态
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:131:**问题7：10周工期是否现实？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:132:- Week 1: 数据契约和接口
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:133:- Week 2-3: CSV导入
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:134:- Week 3-6: 核心业务
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:135:- Week 6-7: 宿舍清退API
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:136:- Week 8-9: 前端
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:137:- Week 10: 联调
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:141:**问题8：Week 1的工作量是否饱和？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:146:这些工作是否足够填满一周？是否应该增加其他任务？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:150:**问题9：是否有更好的实施路径？**
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:151:- 当前：数据契约→CSV导入→核心业务→API集成→前端→联调
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:157:- 当前：认证→申请→审批→附件→通知→集成→前端
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:158:- 是否应该：申请+审批核心流程→认证→附件→通知→集成→前端？
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:184:- 明确的下一步行动计划
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:185:- 调整后的实施路径
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:195:2. ✓ 实施路径的优化
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:212:- **预计工期：** 10周演示版 + 1-2周生产集成
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:213:- **外部依赖：** 宿舍清退API信息待提供
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:214:- **交付要求：** Week 10可演示版本（Mock数据）
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:219:- **数据对接文档：** CSV模板、API规范
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:224:- CSV导入是首版主数据来源
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:225:- 宿舍清退API在Week 6-7前到位
docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:250:**优先级：** P0（决定实施路径）
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:16:**核心问题：** 方案把"用户主数据 API 化"当成默认终局，偏离了此前已达成的首版共识：学生、辅导员、班级映射应优先走 CSV/Excel 导入，宿舍清退才是实时 API。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:30:`RealUserDataProvider` 不应成为认证、审批、班级映射的运行时依赖。用户、辅导员、班级映射是本系统的基础主数据，影响登录、权限、审批人分配和历史追溯。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:34:应落入本地数据库，通过 CSV/API Provider 输入到 staging，再校验、upsert、软停用。此前设计已经定义了 staging + upsert + 软停用、导入审计和校验报告：[31-data-source-requirements-consensus-v2.md](../codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md) 第282行。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:47:1. 用户主数据（学生、辅导员、班级映射）通过CSV导入到本地数据库
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:48:2. Provider只用于宿舍清退状态的实时查询
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:57:3天只适用于"API 契约已冻结、测试环境可用、认证已跑通、字段完全覆盖、只写一个薄适配器"的场景。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:63:- 认证信息
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:72:- **宿舍清退API：** 1-2周
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:73:- **用户主数据API（如果坚持）：** 2-4周（牵涉数据模型、导入/同步策略、账号状态、审批人映射和验收演练）
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:77:"10周 + 3天" → **10周演示版 + 1-2周生产集成缓冲**
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:117:当前设计用一个开关同时切用户数据和宿舍清退：[37-api-blocking-solution-review-request.md](./37-api-blocking-solution-review-request.md) 第160行。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:131:- 支持"用户主数据 CSV + 宿舍清退 API"的混合模式
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:148:- 宿舍状态：`completed/pending/not_started/unknown`
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:155:宿舍清退枚举和降级规则已有定义：[数据对接说明文档.md](../../数据对接说明文档.md) 第306行
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:163:10周做"Mock/Seed 数据可演示版本"基本可行，但 **Week 7 才做接口抽象偏晚**。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:167:Provider 契约、DTO、种子数据、导入接口应在 Week 1-2 完成，否则认证、审批、前端都会先绑定临时模型，后续返工。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:173:| 周次 | 任务 | 交付物 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:175:| Week 1 | 数据契约、DTO、Provider接口、种子数据、导入模型 | 数据契约文档、DTO定义、Provider接口 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:176:| Week 2-3 | CSV/staging/upsert/审计和核心账号数据 | CSV导入功能、staging表、审计日志 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:177:| Week 3-6 | 申请、审批、附件、通知 | 核心业务模块 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:178:| Week 6-7 | 宿舍清退Provider、降级流程、缓存、错误分类 | 宿舍清退集成模块 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:179:| Week 8-9 | 前端 | React Native、微信小程序 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:180:| Week 10 | 联调、演示、验收清单 | 演示版本 |
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:183:- 宿舍清退 API：1周
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:184:- 用户主数据 API 替换 CSV：另计 2-4周
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:188:"10周 + 3天" → **10周演示版 + 1-2周生产集成缓冲**
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:192:若外部 API 字段继续缺失，首版应坚持 CSV/Excel 主数据导入，不等待 API。
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:203:│  CSV / API / DB View / Mock                │
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:226:│  作为认证、权限、审批和历史记录的唯一运行时依据 │
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:234:│    DormCheckoutProvider（宿舍清退查询）      │
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:241:1. **外部数据源：** CSV/API/DB view/Mock
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:244:4. **本地数据库：** 作为认证、权限、审批和历史记录的唯一运行时依据
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:255:### 宿舍清退状态缓存
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:261:- **提交申请前必须重新校验**或记录"校验时间 + source_updated_at"
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:270:- 认证失败
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:287:- 认证失败次数
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:296:**"Seed/Mock + Provider 抽象 + CSV 主数据导入 + 宿舍清退 API 适配"**
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:309:### 首版实施路径
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:311:1. **Week 1-3：** CSV导入 + 种子数据
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:312:2. **Week 3-6：** 核心业务逻辑
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:313:3. **Week 6-7：** 宿舍清退API对接
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:314:4. **Week 8-9：** 前端开发
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:315:5. **Week 10：** 联调和演示
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:316:6. **API到位后：** 1-2周生产集成
docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md:320:如果数据变更频率高，可升级为API/DB同步。但首版应坚持CSV导入，快速上线。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:5:**审查范围：** 用户设计说明书、数据对接说明文档、CSV模板
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:13:发现 9 个主要问题，涉及文档一致性、安全设计、对接契约。CSV 格式本身无误。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:26:文档引用 `docs/templates/宿舍清退数据模板.xlsx`，但实际只有 `docs/templates/宿舍清退数据模板.csv`。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:41:引用 `docs/templates/宿舍管理系统API.postman_collection.json`，但 `docs/templates/` 目录中不存在此文件。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:69:### 问题4：认证方式描述不够收敛 [P2]
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:74:同时列出 API Key、Basic Auth、IP 白名单三种认证方式，未明确推荐组合。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:97:不要在宿舍清退接口中使用 `id_card`，用 `student_id + name` 足够。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:101:### 问题6：审批时限口径不一致 [P2]
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:108:用户文档与系统设计文档审批时限口径不一致。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:143:辅导员查看/审批权限按"本年级"划分过粗，实际应按学院、专业、班级或辅导员负责范围授权。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:175:## CSV 模板检查
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:177:**文件：** `docs/templates/宿舍清退数据模板.csv`
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:187:- 明确 CSV 文件名规则
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:188:- 如果实际模板是 CSV，确保文档引用一致（已修复）
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
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:118:- 认证方式：API Key + IP白名单
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
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:327:- 认证方式：API Key + IP白名单
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:331:- 参考当前数据对接文档中的宿舍清退状态查询接口
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:336:### 4.3 方式3：CSV文件导入（降级）
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:344:- 实施简单
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:353:1. 宿管系统方按模板导出CSV文件
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:360:- 文件格式：CSV
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:382:- CSV导入：建议每日更新，延迟不超过24小时
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:390:## 六、实施建议
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
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:432:2. 如果可以，开发周期大概多久？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:434:### 7.3 CSV导入情况
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:435:1. 如果使用CSV导入，是否可以按模板定期导出数据？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:436:2. 导出频率：每日 / 每周 / 按需？
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:448:1. **宿管系统方**：反馈上述问题，提供数据库/API/CSV的可行性
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:451:4. **本系统方**：更新数据对接说明文档，提供CSV模板文件
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:15:我们认同这3个问题都是实施级关键缺陷，必须在v2文档中修正，否则会导致数据一致性问题。
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:21:### 2.1 问题1：CSV导入策略错误（行329）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:36:2. 即使使用 `DELETE FROM users`，也会导致历史申请记录中的审批人引用失效
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:54:-- 2. 导入CSV到staging表
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:84:- 历史申请记录中的 `student_id`、`counselor_id`、`admin_id` 仍然有效
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:85:- 停用账号不能登录，不能创建新申请，但历史记录可查询
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:192:1. 学生提交申请时，系统需要根据 `users.class_id` 查询 `class_counselor_mapping` 确定辅导员
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:214:**CSV导入映射：**
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:216:学生CSV模板：
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:233:**申请提交时的辅导员分配：**
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:252:    # 创建申请
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:262:## 三、其他需要补充的实施细节
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:264:除了上述3个关键问题，我们还需要补充以下实施细节：
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:279:    application_start_date DATE,                -- 申请开放时间
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:280:    application_end_date DATE,                  -- 申请截止时间
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:342:| 账号状态 | 登录 | 创建申请 | 审批 | 查看历史 | 接收通知 |
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:348:- 学生：本次CSV导入中未出现
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:349:- 辅导员：本次CSV导入中未出现
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:353:- 下次CSV导入中重新出现 → 自动激活（`is_active=true`）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:376:申请提交时的终审人分配逻辑：
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:413:   - `users_staging`：CSV导入临时表
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:418:### 4.2 CSV导入策略修改（第三章3.3节）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:428:1. CSV导入到临时staging表
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:446:**CSV技术要求：**
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:451:### 4.5 实施建议修改（第七章）
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:453:**阶段2：CSV导入实现（2周）**
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:464:1. ✅ CSV导入从"全量覆盖"改为"staging + upsert + 软停用"
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:468:**额外补充的实施细节：**
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:486:- 第186-196行：历史审批人一致性规则的思考过程
docs/discussions/codex-review-2026-05-27/34-codex-second-review-response.md:490:- 第408-417行：实施建议的思考过程
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:23:**修复计划：**
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:40:### 2. 混合认证账户接管漏洞 - **部分同意，提出改进方案**
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:47:- nullable字段导致孤立认证
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:203:### 5. 审批超时监控 - **完全同意**
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:219:    """计算工作时间，排除周末、节假日、非工作时间"""
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:226:        # 跳过周末和节假日
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:254:**修复计划：**
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:262:- 毕业季2周内集中提交
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:273:**部分同意：** 1个（混合认证 - 提出改进方案）
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:276:1. 等待Codex对"混合认证改进方案"的反馈
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:14:Codex正确指出了方案的核心问题：**偏离了已达成的首版共识**。原方案错误地将用户主数据API化，而共识明确规定学生、辅导员、班级映射应采用CSV导入。
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:26:- 忽略了这些数据是系统基础主数据，影响认证、权限、审批人分配
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:29:1. 用户主数据通过CSV导入到本地数据库
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:37:class IUserDataImportSource(ABC):
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:49:# CSV实现
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:50:class CSVUserDataImportSource(IUserDataImportSource):
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:52:        # 读取CSV文件
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:56:class MockUserDataImportSource(IUserDataImportSource):
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:62:    def __init__(self, source: IUserDataImportSource):
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:76:**宿舍清退保持实时查询：**
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:79:# 宿舍清退Provider用于运行时查询
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:83:        """运行时查询宿舍清退状态"""
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:95:- 未考虑缺失信息（API文档、认证、字段映射）的影响
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:102:| 宿舍清退API集成 | 1-2周 | API契约明确、字段覆盖、认证跑通 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:103:| 用户主数据API集成（如需） | 2-4周 | 数据模型、同步策略、验收演练 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:107:"10周 + 3天" → **10周演示版 + 1-2周生产集成缓冲**
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:121:class StudentImportSource(ABC):
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:127:class CounselorImportSource(ABC):
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:132:class ClassMappingImportSource(ABC):
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:169:    def import_students(self, source: StudentImportSource):
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:209:USER_DATA_SOURCE = 'csv'  # 生产环境使用CSV导入
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:210:DORM_CHECKOUT_SOURCE = 'api'  # 宿舍清退使用API
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:273:### 修正后的实施计划
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:275:| 周次 | 任务 | 交付物 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:277:| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:278:| Week 2-3 | CSV导入功能、staging表、upsert逻辑、审计日志 | CSV导入模块、导入校验报告 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:279:| Week 3-6 | 申请、审批、附件、通知模块 | 核心业务功能 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:280:| Week 6-7 | 宿舍清退Provider、降级流程、缓存、错误分类 | 宿舍清退集成模块 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:281:| Week 8-9 | 前端开发 | React Native、微信小程序 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:282:| Week 10 | 联调、演示、验收清单 | 可演示版本（Mock数据） |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:285:- 宿舍清退API集成：1周
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:286:- 用户主数据API替换CSV（如需）：另计2-4周
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:288:**总工期：** 10周演示版 + 1-2周生产集成缓冲
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:299:外部数据源 (CSV/API/Mock)
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:301:ImportSource (数据导入源)
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:305:本地数据库 (认证、权限、审批的唯一运行时依据)
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:308:DormCheckoutProvider (宿舍清退实时查询)
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:313:1. **用户主数据落库：** 学生、辅导员、班级映射通过CSV导入到本地数据库
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:314:2. **Provider用于导入：** ImportSource接口用于数据导入，不是运行时查询
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:315:3. **宿舍清退实时查询：** DormCheckoutProvider用于运行时查询，可缓存，可降级
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:316:4. **本地数据库为准：** 认证、权限、审批以本地数据库为唯一依据
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:324:**"Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配"**
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:330:| RealUserDataProvider运行时查询 | CSV导入到本地数据库 | 用户主数据是基础数据，不应依赖外部API |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:332:| 10周 + 3天 | 10周演示版 + 1-2周生产集成 | 更现实的工期评估 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:333:| Week 7做接口抽象 | Week 1做数据契约和接口 | 避免后续返工 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:334:| Provider用于运行时查询 | ImportSource用于数据导入 | 明确职责边界 |
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:336:### 首版实施路径
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:338:1. **Week 1：** 数据契约、DTO、ImportSource接口
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:339:2. **Week 2-3：** CSV导入功能（staging + upsert + 审计）
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:340:3. **Week 3-6：** 核心业务逻辑
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:341:4. **Week 6-7：** 宿舍清退API对接
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:342:5. **Week 8-9：** 前端开发
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:343:6. **Week 10：** 联调和演示
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:344:7. **API到位后：** 1-2周生产集成
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:349:- CSV导入功能和校验逻辑
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:350:- 宿舍清退API适配器
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:370:2. 更新实施计划
docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md:371:3. 开始Week 1工作：数据契约和接口设计
docs/discussions/codex-review-2026-05-27/04-database-review.md:13:发现2个CRITICAL问题和4个MAJOR问题，需要修订后才能实施。
docs/discussions/codex-review-2026-05-27/04-database-review.md:26:- 软删除用户时，其申请仍然存在，指向"已删除"用户
docs/discussions/codex-review-2026-05-27/04-database-review.md:27:- 查询`applications WHERE is_deleted=FALSE`会返回申请，但关联的用户是已删除状态
docs/discussions/codex-review-2026-05-27/04-database-review.md:30:1. 数据不一致：活跃申请属于"已删除"用户
docs/discussions/codex-review-2026-05-27/04-database-review.md:40:        on_delete=models.PROTECT,  # 有申请时阻止删除
docs/discussions/codex-review-2026-05-27/04-database-review.md:67:**查询1：** "显示辅导员X的待审批申请"
docs/discussions/codex-review-2026-05-27/04-database-review.md:126:- "这个用户在申请#123中改了什么？" → 无before/after值
docs/discussions/codex-review-2026-05-27/04-database-review.md:127:- "安全事件期间谁批准了这个申请？" → 无会话追踪
docs/discussions/codex-review-2026-05-27/04-database-review.md:128:- "追踪这个审批工作流中的所有操作" → 无correlation_id
docs/discussions/codex-review-2026-05-27/04-database-review.md:165:- 无`admin_id`（谁做的最终审批？）
docs/discussions/codex-review-2026-05-27/04-database-review.md:170:1. 报表不可能："辅导员X本月批准了多少申请？" → 无法查询
docs/discussions/codex-review-2026-05-27/04-database-review.md:171:2. 并发bug：两个审批人同时批准 → 无乐观锁
docs/discussions/codex-review-2026-05-27/04-database-review.md:179:    -- 新增固定审批人追踪
docs/discussions/codex-review-2026-05-27/04-database-review.md:197:### 5. users表缺少认证安全字段
docs/discussions/codex-review-2026-05-27/04-database-review.md:201:**基于Round 1-3达成的认证改进，缺失字段：**
docs/discussions/codex-review-2026-05-27/04-database-review.md:213:    -- 新增认证安全字段
docs/discussions/codex-review-2026-05-27/04-database-review.md:231:### 6. 缺少活跃申请的唯一约束
docs/discussions/codex-review-2026-05-27/04-database-review.md:236:- line 532说"一个学生可以创建多个申请"
docs/discussions/codex-review-2026-05-27/04-database-review.md:237:- 但无约束防止：学生创建多个草稿、同时提交多个申请、待审批时重复提交
docs/discussions/codex-review-2026-05-27/04-database-review.md:259:                raise ValidationError("您已有进行中的申请，请等待审批完成")
docs/discussions/codex-review-2026-05-27/04-database-review.md:287:- 无`applications_history`表（申请被驳回重提时，旧数据丢失）
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:1:# Round 3 Claude分析 - Part 3: 审批流程与外部集成
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:5:**分析范围：** 第5-6章（审批流程设计、外部系统集成设计）
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:9:## 第5章：审批流程设计
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:16:`calculate_due_time()`函数实现工作日计算（9:00-17:00，排除周末和节假日），代码复杂度高：
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:24:3. **测试困难**：边界条件多（跨周末、跨节假日、跨年）
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:54:`check_approval_timeout()`每小时执行一次，扫描所有待审批申请。
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:57:- 大部分时间没有超时申请
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:72:# 方案2：定时任务只查询即将超时的申请
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:75:    # 只查询未来1小时内超时的申请
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:97:如果两个审批人同时审批同一申请，可能导致状态不一致。
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:106:    # 锁定申请记录
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:109:    # 验证审批人
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:111:        raise PermissionDenied("不是当前审批人")
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:127:- ✓ 审批历史记录完善
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:189:    # 更新申请状态
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:195:设计提到"审批人可选择'跳过验证'并备注原因"，但未说明如何审计这些操作。
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:210:    # 标记申请
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:240:## 实施建议优先级
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:242:### P0 - 必须修改（阻塞实施）
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:35:**理由：** 与文件导入字段表保持一致，宿舍系统可能无法提供班级信息。
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:116:| dorm_building | String | 宿舍楼栋 | 是 | "1号楼" |
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:117:| dorm_room | String | 宿舍房间号 | 是 | "101" |
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:124:- `class_name`：宿舍系统可能无法提供班级信息
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:125:- `bed_number`：部分宿舍系统无床号管理
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:148:- ✓ `docs/templates/宿舍清退数据模板.csv` - CSV模板
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:164:**可以进入实施阶段。**
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:16:2. 对接方式里对学生、辅导员、班级映射默认写“DB 优先”偏激进。首版更合理的路径是：账号与映射数据优先 CSV/Excel 批量导入，宿舍清退优先 API。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:17:3. 宿舍清退字段与上一轮字段共识存在轻微不一致：`checkout_status` 在本文件中标为可选，但既有字段共识中 API 响应建议必填。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:18:4. 缺少若干实施级关键问题，例如账号标识映射、终审管理员分配规则、同步覆盖策略、历史审批人不被后续映射变更自动改写等。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:33:| 宿舍清退数据 | 完整 | 支撑提交前置校验，是当前已明确需要自动校验的数据。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:34:| 辅导员基本信息 | 完整 | 支撑辅导员账号和一级审批主体。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:40:图书馆清书状态、财务结清状态、独立学籍状态没有列为 P0 是合理的。当前用户设计和系统设计仍保留截图上传、人工审核和宿舍系统异常时人工降级的方案，因此这三类不应阻塞首版上线。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:44:以下不是外部数据源，但应在文档中补充为实施前提或配置项：
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:47:2. **离校批次配置。** 包括毕业届别、开放申请时间、允许计划离校日期范围。这些可由系统后台配置，不必来自外部系统。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:69:### 3.2 宿舍清退数据
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:83:   对 API 或 CSV 数据都建议记录外部系统数据更新时间，便于区分“未完成清退”和“数据过期/未同步”。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:92:2. 缺少账号生命周期字段说明。  
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:93:   `is_active` 已有，但应补充离职、调岗、停用后如何处理其名下未完成审批，以及是否允许历史审批记录继续引用已停用账号。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:103:3. **历史一致性规则。** 班级映射变更后，不应自动改写已提交申请中的 `counselor_id`；已提交申请如需改派，应由管理员显式操作并记录审计日志。
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
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:183:4. 辅导员工号是否全校唯一？是否与统一身份认证、人事系统工号一致？
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:188:9. CSV 导入时是否采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:190:11. 是否有统一身份认证或微信绑定前置要求？是否需要导入手机号/邮箱用于找回密码或二次验证？
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:195:## 七、实施建议审查
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:203:1. 宿舍清退：优先使用宿管系统 API；若不可用，使用每日 CSV 导入；异常时保留人工证明。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:204:2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:205:3. 辅导员信息：首版优先 CSV/Excel 或后台批量维护；若有统一身份或人事 API，再对接。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:206:4. 班级-辅导员映射：首版优先 CSV/Excel 强校验，上线前必须 100% 覆盖当届学生。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:213:1. 当届所有可申请学生必须能解析到有效辅导员。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:214:2. 提交申请时必须能解析到有效终审管理员或终审组。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:216:### 7.3 更好的实施路径
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:218:建议按以下顺序实施：
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:221:2. 先落地三份基础 CSV/Excel 模板：学生、辅导员、班级-辅导员映射。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:223:4. 再对接宿舍清退 API，并把 API 失败、超时、数据过期纳入统一降级处理。
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
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:27:**Claude确认：** ✓ 已在前一轮修复（commit: docs: 修正CSV模板文件扩展名引用）
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:72:### 问题4：认证方式描述不够收敛 [P2]
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:74:**Codex指出：** 同时列出多种认证方式，未明确推荐
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:86:- 修改认证方式章节，明确推荐 API Key + IP 白名单
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:111:### 问题6：审批时限口径不一致 [P2]
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:122:3. 与审批流程设计一致
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:212:4. **实施建议：**
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:231:6. ✓ 问题4：明确认证方式
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:232:7. ✓ 问题6：统一审批时限
docs/design/2026-05-27-system-design.md:1:# 毕业生离校申请审批系统 - 系统设计文档
docs/design/2026-05-27-system-design.md:3:**项目名称：** 毕业生离校申请审批系统  
docs/design/2026-05-27-system-design.md:15:4. [认证授权设计](#4-认证授权设计)
docs/design/2026-05-27-system-design.md:16:5. [审批流程设计](#5-审批流程设计)
docs/design/2026-05-27-system-design.md:29:1. **流程发起：** 毕业生个人申请
docs/design/2026-05-27-system-design.md:31:   - 填写离校申请表，明确计划离校日期
docs/design/2026-05-27-system-design.md:32:   - 上传规定附件（宿舍清退证明、图书馆清书证明、财务结清截图）
docs/design/2026-05-27-system-design.md:33:   - 提交申请（需提前3个工作日）
docs/design/2026-05-27-system-design.md:35:2. **一级审批：** 毕业年级辅导员审核
docs/design/2026-05-27-system-design.md:51:- **认证：** 混合认证（学号+密码 + 微信OAuth2）
docs/design/2026-05-27-system-design.md:102:│ 宿舍管理系统  │  微信公众平台 │ 文件存储   │
docs/design/2026-05-27-system-design.md:121:**认证授权：**
docs/design/2026-05-27-system-design.md:123:- django-allauth（多认证方式）
docs/design/2026-05-27-system-design.md:144:│   │   └── auth.py        # 认证逻辑
docs/design/2026-05-27-system-design.md:146:│   ├── applications/      # 离校申请模块
docs/design/2026-05-27-system-design.md:147:│   │   ├── models.py      # 申请模型
docs/design/2026-05-27-system-design.md:148:│   │   ├── views.py       # 申请CRUD API
docs/design/2026-05-27-system-design.md:149:│   │   ├── workflows.py   # 审批流程
docs/design/2026-05-27-system-design.md:152:│   ├── approvals/         # 审批管理模块
docs/design/2026-05-27-system-design.md:153:│   │   ├── models.py      # 审批记录
docs/design/2026-05-27-system-design.md:154:│   │   ├── views.py       # 审批操作API
docs/design/2026-05-27-system-design.md:168:│       ├── dorm_system.py # 宿舍系统对接
docs/design/2026-05-27-system-design.md:193:2. **applications（离校申请）**
docs/design/2026-05-27-system-design.md:194:   - 申请表单创建
docs/design/2026-05-27-system-design.md:195:   - 申请信息修改
docs/design/2026-05-27-system-design.md:196:   - 申请状态查询
docs/design/2026-05-27-system-design.md:197:   - 申请历史记录
docs/design/2026-05-27-system-design.md:200:3. **approvals（审批管理）**
docs/design/2026-05-27-system-design.md:201:   - 辅导员审批操作
docs/design/2026-05-27-system-design.md:203:   - 审批意见记录
docs/design/2026-05-27-system-design.md:205:   - 审批时限监控
docs/design/2026-05-27-system-design.md:208:   - 附件上传（宿舍清退证明、图书馆清书证明、财务结清截图）
docs/design/2026-05-27-system-design.md:213:   - 附件与申请关联
docs/design/2026-05-27-system-design.md:217:   - 审批状态变更通知
docs/design/2026-05-27-system-design.md:219:   - 审批完成通知
docs/design/2026-05-27-system-design.md:224:   - 宿舍管理系统API对接
docs/design/2026-05-27-system-design.md:225:   - 宿舍清退状态查询
docs/design/2026-05-27-system-design.md:226:   - 外部系统认证
docs/design/2026-05-27-system-design.md:247:2. applications - 离校申请表
docs/design/2026-05-27-system-design.md:248:3. approvals - 审批记录表
docs/design/2026-05-27-system-design.md:253:8. applications_history - 申请历史表
docs/design/2026-05-27-system-design.md:267:    -- 认证安全字段
docs/design/2026-05-27-system-design.md:304:### 2.3 离校申请表（applications）
docs/design/2026-05-27-system-design.md:309:    application_no VARCHAR(50) UNIQUE NOT NULL COMMENT '申请编号',
docs/design/2026-05-27-system-design.md:312:    -- 固定审批人追踪
docs/design/2026-05-27-system-design.md:316:    planned_leave_date DATE NOT NULL COMMENT '计划离校日期',
docs/design/2026-05-27-system-design.md:318:    current_approver_id BIGINT COMMENT '当前审批人ID',
docs/design/2026-05-27-system-design.md:349:) COMMENT='离校申请表';
docs/design/2026-05-27-system-design.md:356:- `approved` - 审批通过
docs/design/2026-05-27-system-design.md:359:**申请编号规则：**
docs/design/2026-05-27-system-design.md:362:### 2.4 审批记录表（approvals）
docs/design/2026-05-27-system-design.md:367:    application_id BIGINT NOT NULL COMMENT '申请ID',
docs/design/2026-05-27-system-design.md:368:    approver_id BIGINT NOT NULL COMMENT '审批人ID',
docs/design/2026-05-27-system-design.md:369:    approver_role VARCHAR(20) NOT NULL COMMENT '审批人角色',
docs/design/2026-05-27-system-design.md:371:    opinion TEXT COMMENT '审批意见',
docs/design/2026-05-27-system-design.md:372:    approval_time TIMESTAMP NOT NULL COMMENT '审批时间',
docs/design/2026-05-27-system-design.md:383:) COMMENT='审批记录表';
docs/design/2026-05-27-system-design.md:397:    application_id BIGINT NOT NULL COMMENT '申请ID',
docs/design/2026-05-27-system-design.md:416:- `dorm_clearance` - 宿舍清退证明
docs/design/2026-05-27-system-design.md:432:    application_id BIGINT COMMENT '关联申请ID',
docs/design/2026-05-27-system-design.md:454:- `application_submitted` - 申请已提交
docs/design/2026-05-27-system-design.md:455:- `approval_pending` - 待审批
docs/design/2026-05-27-system-design.md:456:- `application_approved` - 申请通过
docs/design/2026-05-27-system-design.md:457:- `application_rejected` - 申请驳回
docs/design/2026-05-27-system-design.md:458:- `approval_timeout` - 审批超时提醒
docs/design/2026-05-27-system-design.md:496:- `dorm_integration_type` - 宿舍系统集成类型（api/database）
docs/design/2026-05-27-system-design.md:497:- `dorm_api_url` - 宿舍系统API地址
docs/design/2026-05-27-system-design.md:498:- `dorm_api_key` - 宿舍系统API密钥（加密存储）
docs/design/2026-05-27-system-design.md:499:- `dorm_db_config` - 宿舍系统数据库配置（加密存储，JSON格式）
docs/design/2026-05-27-system-design.md:542:- `create_application` - 创建申请
docs/design/2026-05-27-system-design.md:543:- `update_application` - 更新申请
docs/design/2026-05-27-system-design.md:544:- `approve` - 审批通过
docs/design/2026-05-27-system-design.md:545:- `reject` - 审批驳回
docs/design/2026-05-27-system-design.md:552:- `application` - 申请
docs/design/2026-05-27-system-design.md:553:- `approval` - 审批
docs/design/2026-05-27-system-design.md:557:### 2.9 申请历史表（applications_history）
docs/design/2026-05-27-system-design.md:564:    application_id BIGINT NOT NULL COMMENT '申请ID',
docs/design/2026-05-27-system-design.md:566:    snapshot JSONB NOT NULL COMMENT '申请快照(JSONB格式)',
docs/design/2026-05-27-system-design.md:575:) COMMENT='申请历史表';
docs/design/2026-05-27-system-design.md:579:- `snapshot`: JSONB格式存储申请完整数据（便于查询）
docs/design/2026-05-27-system-design.md:581:  - `submitted`: 提交申请时
docs/design/2026-05-27-system-design.md:592:  ├─1:N─→ applications (学生创建多个申请)
docs/design/2026-05-27-system-design.md:593:  ├─1:N─→ approvals (审批人审批多个申请)
docs/design/2026-05-27-system-design.md:596:applications (申请表)
docs/design/2026-05-27-system-design.md:597:  ├─N:1─→ users (申请人)
docs/design/2026-05-27-system-design.md:600:  ├─N:1─→ users (当前审批人)
docs/design/2026-05-27-system-design.md:601:  ├─1:N─→ approvals (一个申请多条审批记录)
docs/design/2026-05-27-system-design.md:602:  ├─1:N─→ attachments (一个申请多个附件)
docs/design/2026-05-27-system-design.md:603:  ├─1:N─→ notifications (一个申请多条通知)
docs/design/2026-05-27-system-design.md:604:  └─1:N─→ applications_history (一个申请多个历史版本)
docs/design/2026-05-27-system-design.md:605:  └─1:N─→ notifications (一个申请触发多个通知)
docs/design/2026-05-27-system-design.md:607:approvals (审批记录表)
docs/design/2026-05-27-system-design.md:608:  ├─N:1─→ applications (多条审批记录属于一个申请)
docs/design/2026-05-27-system-design.md:609:  └─N:1─→ users (审批人)
docs/design/2026-05-27-system-design.md:612:  └─N:1─→ applications (多个附件属于一个申请)
docs/design/2026-05-27-system-design.md:616:  └─N:1─→ applications (关联申请)
docs/design/2026-05-27-system-design.md:626:1. 一个学生可以创建多个申请（不同时间段）
docs/design/2026-05-27-system-design.md:627:2. 一个申请必须经过2级审批（辅导员→学工部）
docs/design/2026-05-27-system-design.md:628:3. 每个审批节点记录一条审批记录
docs/design/2026-05-27-system-design.md:629:4. 附件与申请强关联，申请删除时级联删除附件
docs/design/2026-05-27-system-design.md:647:**认证方式：**
docs/design/2026-05-27-system-design.md:648:- JWT Token认证
docs/design/2026-05-27-system-design.md:674:### 3.2 认证相关API
docs/design/2026-05-27-system-design.md:846:### 3.3 申请相关API
docs/design/2026-05-27-system-design.md:848:**1. 创建申请**
docs/design/2026-05-27-system-design.md:873:**2. 获取申请列表**
docs/design/2026-05-27-system-design.md:900:**3. 获取申请详情**
docs/design/2026-05-27-system-design.md:923:        "file_name": "宿舍清退证明.jpg",
docs/design/2026-05-27-system-design.md:939:**4. 更新申请**
docs/design/2026-05-27-system-design.md:957:**5. 提交申请**
docs/design/2026-05-27-system-design.md:973:### 3.4 审批相关API
docs/design/2026-05-27-system-design.md:975:**1. 获取待审批列表**
docs/design/2026-05-27-system-design.md:999:**2. 审批通过**
docs/design/2026-05-27-system-design.md:1013:  "message": "审批成功",
docs/design/2026-05-27-system-design.md:1024:  "message": "申请已被修改，请刷新后重试",
docs/design/2026-05-27-system-design.md:1031:**3. 审批驳回**
docs/design/2026-05-27-system-design.md:1038:  "opinion": "宿舍清退证明不完整，请重新提交",
docs/design/2026-05-27-system-design.md:1055:  "message": "申请已被修改，请刷新后重试",
docs/design/2026-05-27-system-design.md:1080:    "file_name": "宿舍清退证明.jpg",
docs/design/2026-05-27-system-design.md:1153:        "title": "申请已通过",
docs/design/2026-05-27-system-design.md:1154:        "content": "您的离校申请已通过辅导员审核",
docs/design/2026-05-27-system-design.md:1189:      "description": "宿舍系统集成类型（api/database）"
docs/design/2026-05-27-system-design.md:1194:      "description": "宿舍系统API地址"
docs/design/2026-05-27-system-design.md:1199:      "description": "宿舍系统API密钥（加密存储）",
docs/design/2026-05-27-system-design.md:1228:- `integration` - 外部系统集成配置（宿舍系统等）
docs/design/2026-05-27-system-design.md:1232:## 4. 认证授权设计
docs/design/2026-05-27-system-design.md:1234:### 4.1 认证方式
docs/design/2026-05-27-system-design.md:1236:**双通道认证：**
docs/design/2026-05-27-system-design.md:1237:1. **学号+密码认证**
docs/design/2026-05-27-system-design.md:1242:2. **微信OAuth2认证**
docs/design/2026-05-27-system-design.md:1248:**认证流程：**
docs/design/2026-05-27-system-design.md:1313:├─ 创建申请
docs/design/2026-05-27-system-design.md:1314:├─ 查看自己的申请
docs/design/2026-05-27-system-design.md:1315:├─ 修改草稿状态的申请
docs/design/2026-05-27-system-design.md:1320:├─ 查看本年级所有申请
docs/design/2026-05-27-system-design.md:1321:├─ 审批申请（通过/驳回）
docs/design/2026-05-27-system-design.md:1322:├─ 查看审批历史
docs/design/2026-05-27-system-design.md:1326:├─ 查看所有申请
docs/design/2026-05-27-system-design.md:1327:├─ 最终备案审批
docs/design/2026-05-27-system-design.md:1337:创建申请           | ✓       | ✗         | ✗
docs/design/2026-05-27-system-design.md:1338:查看自己申请       | ✓       | ✗         | ✗
docs/design/2026-05-27-system-design.md:1339:查看本年级申请     | ✗       | ✓         | ✗
docs/design/2026-05-27-system-design.md:1340:查看所有申请       | ✗       | ✗         | ✓
docs/design/2026-05-27-system-design.md:1341:辅导员审批         | ✗       | ✓         | ✗
docs/design/2026-05-27-system-design.md:1342:学工部审批         | ✗       | ✗         | ✓
docs/design/2026-05-27-system-design.md:1388:## 5. 审批流程设计
docs/design/2026-05-27-system-design.md:1401:approved（审批通过）
docs/design/2026-05-27-system-design.md:1408:    'pending_counselor': ['pending_admin', 'rejected'],  # 辅导员审批
docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
docs/design/2026-05-27-system-design.md:1417:**节点1：学生提交申请**
docs/design/2026-05-27-system-design.md:1420:  - 计划离校日期 ≥ 当前日期 + 3个工作日
docs/design/2026-05-27-system-design.md:1421:  - 必须上传宿舍清退证明
docs/design/2026-05-27-system-design.md:1426:  - 生成申请编号（LX{YYYYMMDD}{6位序号}）
docs/design/2026-05-27-system-design.md:1427:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
docs/design/2026-05-27-system-design.md:1428:  - 设置当前审批人：current_approver_id = counselor_id
docs/design/2026-05-27-system-design.md:1431:  - 创建历史快照：applications_history（version=0, change_reason='提交申请'）
docs/design/2026-05-27-system-design.md:1437:- 触发条件：申请状态为 pending_counselor
docs/design/2026-05-27-system-design.md:1443:    - 更新当前审批人：current_approver_id = admin_id
docs/design/2026-05-27-system-design.md:1445:    - 创建审批记录：approvals（approver_role='counselor', action='approve'）
docs/design/2026-05-27-system-design.md:1446:    - 创建历史快照：applications_history（version=N, change_reason='辅导员审批通过'）
docs/design/2026-05-27-system-design.md:1451:    - 清空当前审批人：current_approver_id = NULL
docs/design/2026-05-27-system-design.md:1453:    - 创建审批记录：approvals（approver_role='counselor', action='reject'）
docs/design/2026-05-27-system-design.md:1457:  - 记录审批意见和时间
docs/design/2026-05-27-system-design.md:1458:- 办理时限：1个工作日（按工作时间9:00-17:00计算，排除周末和节假日）
docs/design/2026-05-27-system-design.md:1462:- 触发条件：申请状态为 pending_admin
docs/design/2026-05-27-system-design.md:1468:    - 清空当前审批人：current_approver_id = NULL
docs/design/2026-05-27-system-design.md:1472:    - 创建审批记录：approvals（approver_role='admin', action='approve'）
docs/design/2026-05-27-system-design.md:1475:    - 归档申请全记录
docs/design/2026-05-27-system-design.md:1479:    - 清空当前审批人：current_approver_id = NULL
docs/design/2026-05-27-system-design.md:1481:    - 创建审批记录：approvals（approver_role='admin', action='reject'）
docs/design/2026-05-27-system-design.md:1486:- 办理时限：1个工作日（按工作时间9:00-17:00计算，排除周末和节假日）
docs/design/2026-05-27-system-design.md:1490:- 触发条件：申请状态为 rejected
docs/design/2026-05-27-system-design.md:1492:  - 学生修改申请内容
docs/design/2026-05-27-system-design.md:1507:    # 查询待审批的申请
docs/design/2026-05-27-system-design.md:1514:        # 获取最新审批记录（当前节点）
docs/design/2026-05-27-system-design.md:1520:            # 新提交的申请，从submit_time开始计算
docs/design/2026-05-27-system-design.md:1523:            # 已有审批记录，从上次审批时间开始计算
docs/design/2026-05-27-system-design.md:1530:            # 创建超时审批记录
docs/design/2026-05-27-system-design.md:1546:    排除周末和节假日
docs/design/2026-05-27-system-design.md:1583:- 第1次：办理时限到期时通知审批人
docs/design/2026-05-27-system-design.md:1584:- 第2次：超时4小时后通知审批人上级
docs/design/2026-05-27-system-design.md:1588:- 外部系统（宿舍管理系统）不可用时，允许手动上传证明文件
docs/design/2026-05-27-system-design.md:1589:- 审批人可选择"跳过验证"并备注原因
docs/design/2026-05-27-system-design.md:1605:### 6.2 宿舍管理系统对接
docs/design/2026-05-27-system-design.md:1608:验证学生宿舍清退状态，确保离校手续真实完成。
docs/design/2026-05-27-system-design.md:1615:认证方式：API Key
docs/design/2026-05-27-system-design.md:1622:# 查询宿舍清退状态
docs/design/2026-05-27-system-design.md:1692:            raise ExternalSystemTimeout("宿舍系统超时")
docs/design/2026-05-27-system-design.md:1694:            raise ExternalSystemError(f"宿舍系统错误: {str(e)}")
docs/design/2026-05-27-system-design.md:1714:    """认证失败 - 不可重试"""
docs/design/2026-05-27-system-design.md:1734:- 审批人可选择"跳过验证"并备注原因
docs/design/2026-05-27-system-design.md:1961:### 8.3 认证安全
docs/design/2026-05-27-system-design.md:1977:**Phase 1实施（2项核心措施）：**
docs/design/2026-05-27-system-design.md:2231:- 用户认证：登录、登出、密码修改、微信绑定
docs/design/2026-05-27-system-design.md:2232:- 申请操作：创建、修改、提交、删除
docs/design/2026-05-27-system-design.md:2233:- 审批操作：通过、驳回
docs/design/2026-05-27-system-design.md:2320:- `dorm_api_key` - 宿舍系统API密钥
docs/design/2026-05-27-system-design.md:2321:- `dorm_db_config` - 宿舍系统数据库配置（JSON格式）
docs/design/2026-05-27-system-design.md:2386:- `idx_approver_status`: 待审批列表查询（按审批人+状态+时间）
docs/design/2026-05-27-system-design.md:2387:- `idx_student_status`: 学生查看自己申请列表
docs/design/2026-05-27-system-design.md:2388:- `idx_status_deleted`: 按状态筛选未删除申请
docs/design/2026-05-27-system-design.md:2389:- `idx_app_time`: 申请的审批历史（按时间倒序）
docs/design/2026-05-27-system-design.md:2390:- `idx_app_type`: 申请的附件列表（按类型筛选）
docs/design/2026-05-27-system-design.md:2438:# L2: 申请状态缓存（5分钟）
docs/design/2026-05-27-system-design.md:2441:# L3: 待审批数量缓存（1分钟）
docs/design/2026-05-27-system-design.md:2454:    """申请状态变更时失效相关缓存"""
docs/design/2026-05-27-system-design.md:2458:    # 失效审批人的待审批数量缓存
docs/design/2026-05-27-system-design.md:2463:    # 失效学生的申请列表缓存
docs/design/2026-05-27-system-design.md:2481:- 审批操作（必须实时）
docs/design/2026-05-27-system-design.md:2601:# 认证安全测试（5项加固措施）
docs/design/2026-05-27-system-design.md:2649:    """测试学生无法审批"""
docs/design/2026-05-27-system-design.md:2677:    """测试审批操作记录审计日志"""
docs/design/2026-05-27-system-design.md:2684:    """测试提交申请创建历史快照"""
docs/design/2026-05-27-system-design.md:2689:    assert history.change_reason == '提交申请'
docs/design/2026-05-27-system-design.md:2695:- 完整审批流程测试
docs/design/2026-05-27-system-design.md:2711:1. 学生提交申请完整流程
docs/design/2026-05-27-system-design.md:2712:2. 辅导员审批流程
docs/design/2026-05-27-system-design.md:2779:- 业务指标：申请数量、审批时效
docs/design/2026-05-27-system-design.md:2787:- 审批超时 > 10个

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-30/38-codex-api-blocking-review.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# Codex审查：API阻塞问题解决方案

**文档编号：** 38  
**审查日期：** 2026-05-30  
**审查人：** Codex (GPT-5.5)  
**审查对象：** 37-api-blocking-solution-review-request.md

---

## 审查结论

**评分：** 7/10

**总体评价：** Mock + 接口抽象方向是合理的，但当前方案不能按原文直接通过。

**核心问题：** 方案把"用户主数据 API 化"当成默认终局，偏离了此前已达成的首版共识：学生、辅导员、班级映射应优先走 CSV/Excel 导入，宿舍清退才是实时 API。

**共识依据：**
- [31-data-source-requirements-consensus-v2.md](../codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md) 第35行
- [数据对接说明文档.md](../../数据对接说明文档.md) 第24行

---

## P0问题（必须修复）

### P0-1：RealUserDataProvider不应成为运行时依赖

**问题描述：**

`RealUserDataProvider` 不应成为认证、审批、班级映射的运行时依赖。用户、辅导员、班级映射是本系统的基础主数据，影响登录、权限、审批人分配和历史追溯。

**应该的做法：**

应落入本地数据库，通过 CSV/API Provider 输入到 staging，再校验、upsert、软停用。此前设计已经定义了 staging + upsert + 软停用、导入审计和校验报告：[31-data-source-requirements-consensus-v2.md](../codex-review-2026-05-27/31-data-source-requirements-consensus-v2.md) 第282行。

**风险：**

如果直接在业务中查询 Provider，会引入：
- 外部 API 可用性风险
- 分页问题
- 延迟问题
- 字段缺失
- 历史变更不可追溯

**修复建议：**

1. 用户主数据（学生、辅导员、班级映射）通过CSV导入到本地数据库
2. Provider只用于宿舍清退状态的实时查询
3. 保留Provider抽象层，但明确其用途：数据导入（非运行时查询）

---

### P0-2：+3天生产就绪评估过于乐观

**问题描述：**

3天只适用于"API 契约已冻结、测试环境可用、认证已跑通、字段完全覆盖、只写一个薄适配器"的场景。

**当前现状：**

文档明确缺少：
- 完整 API 文档
- 认证信息
- 字段映射
- 交付时间

参考：[37-api-blocking-solution-review-request.md](./37-api-blocking-solution-review-request.md) 第25行

**修复建议：**

真实集成应预留：
- **宿舍清退API：** 1-2周
- **用户主数据API（如果坚持）：** 2-4周（牵涉数据模型、导入/同步策略、账号状态、审批人映射和验收演练）

**推荐工期：**

"10周 + 3天" → **10周演示版 + 1-2周生产集成缓冲**

---

## P1问题（重要改进）

### P1-1：接口设计粒度不够

**问题描述：**

`get_students(filters) -> List[Student]`、`get_counselors()`、`get_class_mapping() -> Dict[str, str]` 太粗，缺少：
- 分页
- 增量同步
- 源数据更新时间
- 数据质量报告
- 批次标识
- 字段映射版本
- 错误分类
- 健康检查

**修复建议：**

拆分为：
- `StudentSourceProvider` / `CounselorSourceProvider` / `ClassMappingSourceProvider`
- `DormCheckoutProvider`
- `ProviderHealthCheck`
- `ImportAdapter` 或 `SyncService`

**返回值设计：**

返回值应是 DTO，不是 Django ORM Model。
- Provider 负责：取数和标准化
- Import/Sync 层负责：校验、落库、审计、软停用

---

### P1-2：USE_MOCK_DATA太粗且有生产风险

**问题描述：**

当前设计用一个开关同时切用户数据和宿舍清退：[37-api-blocking-solution-review-request.md](./37-api-blocking-solution-review-request.md) 第160行。

**修复建议：**

改为细粒度配置：
```python
USER_DATA_SOURCE = 'seed' | 'csv' | 'api'
DORM_CHECKOUT_SOURCE = 'mock' | 'api' | 'csv'
WECHAT_PROVIDER = 'mock' | 'real'
```

**安全措施：**
- 生产环境禁止 `mock`
- 启动时 system check 直接失败
- 支持"用户主数据 CSV + 宿舍清退 API"的混合模式

---

### P1-3：Mock数据真实性不足

**问题描述：**

100学生、10辅导员可以支撑演示，但不足以覆盖风险。

**必须包含边界样本：**
- 无班级映射
- 辅导员停用
- 重复 class_id
- 多辅导员
- 延期毕业/非毕业生
- 姓名不一致
- 宿舍状态：`completed/pending/not_started/unknown`
- API错误：404/401/429/500
- 超时
- 数据过期

**参考：**

宿舍清退枚举和降级规则已有定义：[数据对接说明文档.md](../../数据对接说明文档.md) 第306行

---

## 工期评估

### 当前方案评估

10周做"Mock/Seed 数据可演示版本"基本可行，但 **Week 7 才做接口抽象偏晚**。

**问题：**

Provider 契约、DTO、种子数据、导入接口应在 Week 1-2 完成，否则认证、审批、前端都会先绑定临时模型，后续返工。

### 调整后的工期

**建议调整为：**

| 周次 | 任务 | 交付物 |
|------|------|--------|
| Week 1 | 数据契约、DTO、Provider接口、种子数据、导入模型 | 数据契约文档、DTO定义、Provider接口 |
| Week 2-3 | CSV/staging/upsert/审计和核心账号数据 | CSV导入功能、staging表、审计日志 |
| Week 3-6 | 申请、审批、附件、通知 | 核心业务模块 |
| Week 6-7 | 宿舍清退Provider、降级流程、缓存、错误分类 | 宿舍清退集成模块 |
| Week 8-9 | 前端 | React Native、微信小程序 |
| Week 10 | 联调、演示、验收清单 | 演示版本 |

**API到位后：**
- 宿舍清退 API：1周
- 用户主数据 API 替换 CSV：另计 2-4周

**总工期：**

"10周 + 3天" → **10周演示版 + 1-2周生产集成缓冲**

**重要提示：**

若外部 API 字段继续缺失，首版应坚持 CSV/Excel 主数据导入，不等待 API。

---

## 架构建议

### 推荐架构：反腐层 + 本地主数据

```
┌─────────────────────────────────────────────┐
│         外部数据源（External Sources）        │
│  CSV / API / DB View / Mock                │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         Provider层（Data Providers）         │
│  只负责读取外部数据并转换为标准 DTO           │
│  - StudentSourceProvider                    │
│  - CounselorSourceProvider                  │
│  - ClassMappingSourceProvider               │
│  - DormCheckoutProvider                     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│    Import/Sync Service（导入/同步服务）      │
│  校验必填字段、唯一性、班级覆盖率、辅导员有效性 │
│  - Staging表                                │
│  - Upsert逻辑                               │
│  - 软停用                                   │
│  - 导入审计                                 │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│      本地数据库（Local Database）            │
│  作为认证、权限、审批和历史记录的唯一运行时依据 │
│  - users表                                  │
│  - applications表                           │
│  - approvals表                              │
└─────────────────────────────────────────────┘
                    ↑
                    │ (运行时查询)
┌─────────────────────────────────────────────┐
│    DormCheckoutProvider（宿舍清退查询）      │
│  运行时查询，可缓存，可降级到人工证明          │
└─────────────────────────────────────────────┘
```

### 关键设计原则

1. **外部数据源：** CSV/API/DB view/Mock
2. **Provider：** 只负责读取外部数据并转换为标准 DTO
3. **Import/Sync Service：** 校验必填字段、唯一性、班级覆盖率、辅导员有效性
4. **本地数据库：** 作为认证、权限、审批和历史记录的唯一运行时依据
5. **DormCheckoutProvider：** 运行时查询，可缓存，可降级到人工证明

---

## 缓存策略

### 用户信息缓存

按现有设计 30分钟左右缓存：[2026-05-27-system-design.md](../../design/2026-05-27-system-design.md) 第2433行

### 宿舍清退状态缓存

**建议：**
- `completed`：可缓存 10-30分钟
- `pending/not_started`：缓存 1-5分钟
- `unknown/error`：只短缓存 30-60秒，避免故障恢复后仍误判

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# API阻塞问题解决方案 - 最终共识

**文档编号：** 40  
**共识日期：** 2026-05-30  
**参与方：** Claude Opus 4.7, Codex (GPT-5.5)  
**审查周期：** 37 → 38 → 39 → 40

---

## 一、共识结论

**方案名称：** Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配

**核心原则：**
1. 用户主数据（学生、辅导员、班级映射）通过CSV导入到本地数据库
2. ImportSource接口用于数据导入，不是运行时查询
3. 宿舍清退状态通过API实时查询（可缓存、可降级）
4. 本地数据库是认证、权限、审批的唯一运行时依据

**评分：** 9/10（Codex原评分7/10，修正后提升至9/10）

---

## 二、架构设计

### 2.1 数据流架构

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

### 2.2 核心接口设计

```python
# 1. 数据导入源接口（用于导入，非运行时查询）
class IUserDataImportSource(ABC):
    """用户数据导入源接口"""
    @abstractmethod
    def fetch_students(self) -> ImportResult[StudentDTO]:
        """获取学生数据用于导入"""
        pass
    
    @abstractmethod
    def fetch_counselors(self) -> ImportResult[CounselorDTO]:
        """获取辅导员数据用于导入"""
        pass
    
    @abstractmethod
    def fetch_class_mapping(self) -> ImportResult[ClassMappingDTO]:
        """获取班级映射数据用于导入"""
        pass

# 2. 宿舍清退Provider（用于运行时查询）
class IDormCheckoutProvider(ABC):
    """宿舍清退状态提供者接口"""
    @abstractmethod
    def check_status(self, student_id: str) -> CheckoutResult:
        """运行时查询宿舍清退状态"""
        pass
    
    @abstractmethod
    def health_check(self) -> HealthStatus:
        """健康检查"""
        pass

# 3. 导入服务
class UserDataImportService:
    def __init__(self, source: IUserDataImportSource):
        self.source = source
    
    def import_data(self):
        # 1. 从source获取数据
        result = self.source.fetch_students()
        
        # 2. 导入到staging表
        self.load_to_staging(result.data)
        
        # 3. 校验（必填字段、唯一性、班级覆盖率）
        errors = self.validate(result.data)
        
        # 4. Upsert到users表
        self.upsert_to_users()
        
        # 5. 软停用未导入的账号
        self.soft_delete_missing()
        
        # 6. 生成审计日志
        self.create_audit_log(result, errors)
```

### 2.3 DTO设计

```python
@dataclass
class StudentDTO:
    student_id: str
    name: str
    department: str
    major: str
    class_id: str
    grade: int
    graduation_year: int
    is_graduating: bool
    phone: Optional[str] = None
    email: Optional[str] = None

@dataclass
class ImportResult[T]:
    data: List[T]
    total_count: int
    source_updated_at: datetime
    metadata: Dict[str, Any]

@dataclass
class CheckoutResult:
    student_id: str
    status: CheckoutStatus  # completed/pending/not_started/unknown
    checkout_date: Optional[datetime]
    error: Optional[str]
```

---

## 三、配置管理

### 3.1 细粒度配置

```python
# settings/base.py
USER_DATA_SOURCE = env.str('USER_DATA_SOURCE', default='seed')  # seed|csv|api
DORM_CHECKOUT_SOURCE = env.str('DORM_CHECKOUT_SOURCE', default='mock')  # mock|api|csv
WECHAT_PROVIDER = env.str('WECHAT_PROVIDER', default='mock')  # mock|real

# settings/dev.py
USER_DATA_SOURCE = 'seed'  # 开发环境使用种子数据
DORM_CHECKOUT_SOURCE = 'mock'
WECHAT_PROVIDER = 'mock'

# settings/prod.py
USER_DATA_SOURCE = 'csv'  # 生产环境使用CSV导入
DORM_CHECKOUT_SOURCE = 'api'  # 宿舍清退使用API
WECHAT_PROVIDER = 'real'
```

### 3.2 安全检查

```python
from django.core.checks import Error, register

@register()
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
        "2020002": CheckoutStatus(status="pending", date=None),
        "2020003": CheckoutStatus(status="not_started", date=None),
        "2020004": CheckoutStatus(status="unknown", date=None),  # API失败
    }
    
    return students, counselors, dorm_statuses
```

### 5.2 数据规模

- **学生：** 100人（覆盖5个院系、10个班级）
- **辅导员：** 10人（包含停用账号）
- **班级映射：** 10个班级
- **宿舍清退状态：** 覆盖所有枚举值（completed/pending/not_started/unknown）

---

## 六、缓存策略

### 6.1 用户信息缓存

- **TTL：** 30分钟
- **缓存键：** `user:{user_id}`
- **更新策略：** 导入后清空缓存

### 6.2 宿舍清退状态缓存

- **completed：** 10-30分钟
- **pending/not_started：** 1-5分钟
- **unknown/error：** 30-60秒

exec
/bin/bash -lc "rtk sed -n '1,320p' docs/superpowers/plans/2026-05-27-implementation-plan.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 毕业生离校申请审批系统 - 实施计划

**创建日期：** 2026-05-27  
**计划版本：** v1.0  
**预计工期：** 8-10周  
**开发人员：** 2-3人

---

## 目标

实现一个完整的毕业生离校申请审批系统，支持：
- 学生在线提交离校申请
- 辅导员和学工部两级审批
- 附件上传和管理
- 微信通知推送
- 宿舍管理系统对接（API集成）
- Docker容器化部署

## 范围

**包含：**
- 后端API开发（Django + DRF）
- 前端开发（React Native + 微信小程序）
- 数据库设计和实现
- 认证授权系统
- 审批流程引擎
- 文件存储系统
- 通知系统
- 外部系统集成
- Docker部署配置
- 单元测试和集成测试

**不包含：**
- 生产环境运维
- 用户培训
- 数据迁移
- 性能调优（初期）

## 前置条件

**开发环境：**
- Python 3.10+
- Node.js 18+
- Docker 20.10+
- Docker Compose 2.0+
- Git

**技能要求：**
- Python/Django开发经验
- React Native开发经验
- 微信小程序开发经验
- Docker使用经验
- RESTful API设计经验

**外部依赖：**
- 微信公众平台账号
- 宿舍管理系统API文档和测试环境

## 成功标准

**功能完整性：**
- ✓ 所有核心功能实现并通过测试
- ✓ 审批流程完整可用
- ✓ 通知系统正常工作
- ✓ 外部系统对接成功

**质量标准：**
- ✓ 单元测试覆盖率 > 80%
- ✓ 所有API通过集成测试
- ✓ 端到端测试通过
- ✓ 无严重安全漏洞

**性能标准：**
- ✓ API响应时间 < 200ms（P95）
- ✓ 支持1000+并发用户
- ✓ 文件上传成功率 > 99%

**部署标准：**
- ✓ Docker一键部署成功
- ✓ 数据库迁移脚本完整
- ✓ 备份恢复流程验证通过

---

## 文件结构规划

```
graduation-leave-system/
├── backend/                    # Django后端
│   ├── config/                 # 项目配置
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── dev.py
│   │   │   └── prod.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── celery.py
│   ├── apps/
│   │   ├── accounts/           # 用户账户模块
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   ├── permissions.py
│   │   │   └── tests/
│   │   ├── applications/       # 离校申请模块
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   ├── workflows.py
│   │   │   ├── states.py
│   │   │   └── tests/
│   │   ├── approvals/          # 审批管理模块
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   └── tests/
│   │   ├── attachments/        # 附件管理模块
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   ├── storage.py
│   │   │   └── tests/
│   │   ├── notifications/      # 通知模块
│   │   │   ├── models.py
│   │   │   ├── tasks.py
│   │   │   ├── wechat.py
│   │   │   └── tests/
│   │   └── integrations/       # 外部系统集成
│   │       ├── base.py
│   │       ├── dorm_system.py
│   │       └── tests/
│   ├── utils/                  # 工具模块
│   │   ├── validators.py
│   │   ├── exceptions.py
│   │   └── responses.py
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── dev.txt
│   │   └── prod.txt
│   ├── Dockerfile
│   └── manage.py
├── frontend/
│   ├── mobile/                 # React Native应用
│   │   ├── src/
│   │   │   ├── screens/
│   │   │   ├── components/
│   │   │   ├── services/
│   │   │   ├── utils/
│   │   │   └── App.js
│   │   ├── package.json
│   │   └── README.md
│   └── miniprogram/            # 微信小程序
│       ├── pages/
│       ├── components/
│       ├── utils/
│       ├── app.js
│       └── app.json
├── docker/
│   ├── nginx/
│   │   └── nginx.conf
│   └── scripts/
│       └── backup.sh
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 实施阶段

### 阶段1：项目初始化和基础设施（第1周）

**目标：** 搭建项目基础框架和开发环境

**任务清单：**

1. **创建项目目录结构**
   - 创建backend、frontend、docker目录
   - 初始化Git仓库
   - 创建.gitignore文件

2. **初始化Django项目**
   - 安装Django 4.2
   - 创建Django项目
   - 配置settings分层（base/dev/prod）
   - 配置PostgreSQL数据库连接

3. **配置Docker环境**
   - 编写Dockerfile（Django应用）
   - 编写docker-compose.yml
   - 配置Nginx服务
   - 配置MySQL/PostgreSQL服务
   - 配置Redis服务

4. **配置Celery**
   - 安装Celery
   - 配置Celery应用
   - 配置Celery worker
   - 配置Celery beat

5. **配置开发工具**
   - 配置pytest
   - 配置代码格式化工具（black、isort）
   - 配置代码检查工具（flake8、pylint）
   - 配置pre-commit hooks

**验证标准：**
- ✓ `docker-compose up` 成功启动所有服务
- ✓ Django开发服务器可访问
- ✓ 数据库连接成功
- ✓ Redis连接成功
- ✓ Celery worker正常运行

---

### 阶段2：用户认证模块（第2周）

**目标：** 实现用户管理和认证授权系统

**任务清单：**

1. **创建用户模型**
   - 定义User模型（继承AbstractUser）
   - 添加字段：student_id、role、wechat_openid等
   - 创建数据库迁移
   - 编写模型测试

2. **实现学号密码认证**
   - 安装djangorestframework-simplejwt
   - 实现登录API
   - 实现Token刷新API
   - 实现登出API
   - 编写认证测试

3. **实现微信OAuth2认证**
   - 安装wechatpy
   - 实现微信授权登录API
   - 实现openid绑定逻辑
   - 编写微信认证测试

4. **实现权限系统**
   - 定义角色权限（student/counselor/admin）
   - 实现RBAC权限类
   - 实现权限装饰器
   - 编写权限测试

5. **实现用户管理API**
   - 用户列表API
   - 用户详情API
   - 用户更新API
   - 密码修改API

**验证标准：**
- ✓ 学号密码登录成功，返回JWT Token
- ✓ 微信授权登录成功
- ✓ Token刷新成功
- ✓ 权限控制正常工作
- ✓ 所有测试通过

---

### 阶段3：离校申请模块（第3周）

**目标：** 实现离校申请的创建、查询、更新、提交功能

**任务清单：**

1. **创建申请模型**
   - 定义Application模型
   - 添加字段：application_no、status、planned_leave_date等
   - 创建数据库迁移
   - 编写模型测试

2. **实现状态机**
   - 安装django-fsm
   - 定义状态转换规则
   - 实现状态转换方法
   - 编写状态机测试

3. **实现申请CRUD API**
   - 创建申请API
   - 获取申请列表API
   - 获取申请详情API
   - 更新申请API
   - 删除申请API（软删除）

4. **实现申请提交逻辑**
   - 实现提交前校验
   - 实现申请编号生成
   - 实现状态变更
   - 触发通知发送

5. **实现申请查询过滤**
   - 按状态过滤
   - 按日期范围过滤
   - 按学生过滤
   - 分页查询

**验证标准：**
- ✓ 创建申请成功
- ✓ 申请编号自动生成
- ✓ 提交申请后状态变更为pending_counselor
- ✓ 查询过滤正常工作
- ✓ 所有测试通过

---

### 阶段4：审批管理模块（第4周）

**目标：** 实现审批流程和审批记录管理

**任务清单：**

1. **创建审批记录模型**
   - 定义Approval模型
   - 添加字段：approver_id、action、opinion等
   - 创建数据库迁移
   - 编写模型测试

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-30/37-api-blocking-solution-review-request.md" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '321,700p' docs/superpowers/plans/2026-05-27-implementation-plan.md" in /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk sed -n '1,280p' docs/discussions/codex-review-2026-05-30/39-claude-response-to-codex.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 125ms:
# Claude响应Codex审查：API阻塞问题解决方案

**文档编号：** 39  
**响应日期：** 2026-05-30  
**响应人：** Claude Opus 4.7  
**审查对象：** 38-codex-api-blocking-review.md

---

## 总体响应

**完全接受Codex的审查意见。**

Codex正确指出了方案的核心问题：**偏离了已达成的首版共识**。原方案错误地将用户主数据API化，而共识明确规定学生、辅导员、班级映射应采用CSV导入。

---

## 对P0问题的响应

### P0-1：RealUserDataProvider不应成为运行时依赖

**完全同意。**

**错误认识：**
- 原方案将用户主数据（学生、辅导员、班级映射）视为可通过Provider实时查询的数据
- 忽略了这些数据是系统基础主数据，影响认证、权限、审批人分配

**正确做法：**
1. 用户主数据通过CSV导入到本地数据库
2. 使用staging表 + upsert + 软停用模式（已在v2共识中定义）
3. Provider抽象层保留，但用途改为：**数据导入的输入源**，而非运行时查询

**修正后的架构：**

```python
# Provider用于数据导入（非运行时查询）
class IUserDataImportSource(ABC):
    """用户数据导入源接口"""
    @abstractmethod
    def fetch_students(self) -> List[StudentDTO]:
        """获取学生数据用于导入"""
        pass
    
    @abstractmethod
    def fetch_counselors(self) -> List[CounselorDTO]:
        """获取辅导员数据用于导入"""
        pass

# CSV实现
class CSVUserDataImportSource(IUserDataImportSource):
    def fetch_students(self):
        # 读取CSV文件
        return parse_csv_to_dto('students.csv')

# Mock实现（开发阶段）
class MockUserDataImportSource(IUserDataImportSource):
    def fetch_students(self):
        return generate_mock_students(100)

# 导入服务
class UserDataImportService:
    def __init__(self, source: IUserDataImportSource):
        self.source = source
    
    def import_data(self):
        # 1. 从source获取数据
        students = self.source.fetch_students()
        
        # 2. 导入到staging表
        # 3. 校验
        # 4. Upsert到users表
        # 5. 软停用未导入的账号
        # 6. 生成审计日志
```

**宿舍清退保持实时查询：**

```python
# 宿舍清退Provider用于运行时查询
class IDormCheckoutProvider(ABC):
    @abstractmethod
    def check_status(self, student_id: str) -> CheckoutStatus:
        """运行时查询宿舍清退状态"""
        pass
```

---

### P0-2：+3天生产就绪评估过于乐观

**完全同意。**

**错误评估原因：**
- 低估了API集成的复杂度
- 未考虑缺失信息（API文档、认证、字段映射）的影响
- 未考虑数据模型调整、验收演练的时间

**修正后的工期：**

| 场景 | 工期 | 说明 |
|------|------|------|
| 宿舍清退API集成 | 1-2周 | API契约明确、字段覆盖、认证跑通 |
| 用户主数据API集成（如需） | 2-4周 | 数据模型、同步策略、验收演练 |

**总工期调整：**

"10周 + 3天" → **10周演示版 + 1-2周生产集成缓冲**

---

## 对P1问题的响应

### P1-1：接口设计粒度不够

**完全同意。**

**修正后的接口设计：**

```python
# 1. 拆分Provider
class StudentImportSource(ABC):
    @abstractmethod
    def fetch(self, batch_id: int) -> ImportResult[StudentDTO]:
        """获取学生数据"""
        pass

class CounselorImportSource(ABC):
    @abstractmethod
    def fetch(self) -> ImportResult[CounselorDTO]:
        pass

class ClassMappingImportSource(ABC):
    @abstractmethod
    def fetch(self) -> ImportResult[ClassMappingDTO]:
        pass

class DormCheckoutProvider(ABC):
    @abstractmethod
    def check_status(self, student_id: str) -> CheckoutResult:
        pass
    
    @abstractmethod
    def health_check(self) -> HealthStatus:
        pass

# 2. 返回DTO而非ORM Model
@dataclass
class StudentDTO:
    student_id: str
    name: str
    department: str
    major: str
    class_id: str
    grade: int
    graduation_year: int
    is_graduating: bool
    phone: Optional[str] = None
    email: Optional[str] = None

@dataclass
class ImportResult[T]:
    data: List[T]
    total_count: int
    source_updated_at: datetime
    metadata: Dict[str, Any]

# 3. Import/Sync Service
class ImportService:
    def import_students(self, source: StudentImportSource):
        # 1. Fetch from source
        result = source.fetch(batch_id=current_batch_id)
        
        # 2. Validate
        errors = self.validate(result.data)
        
        # 3. Load to staging
        self.load_to_staging(result.data)
        
        # 4. Upsert
        self.upsert_to_users()
        
        # 5. Soft delete
        self.soft_delete_missing()
        
        # 6. Audit log
        self.create_audit_log(result, errors)
```

---

### P1-2：USE_MOCK_DATA太粗且有生产风险

**完全同意。**

**修正后的配置：**

```python
# settings/base.py
USER_DATA_SOURCE = env.str('USER_DATA_SOURCE', default='seed')  # seed|csv|api
DORM_CHECKOUT_SOURCE = env.str('DORM_CHECKOUT_SOURCE', default='mock')  # mock|api|csv
WECHAT_PROVIDER = env.str('WECHAT_PROVIDER', default='mock')  # mock|real

# settings/dev.py
USER_DATA_SOURCE = 'seed'  # 开发环境使用种子数据
DORM_CHECKOUT_SOURCE = 'mock'
WECHAT_PROVIDER = 'mock'

# settings/prod.py
USER_DATA_SOURCE = 'csv'  # 生产环境使用CSV导入
DORM_CHECKOUT_SOURCE = 'api'  # 宿舍清退使用API
WECHAT_PROVIDER = 'real'

# 安全检查
from django.core.checks import Error, register

@register()
def check_production_config(app_configs, **kwargs):
    errors = []
    if settings.ENVIRONMENT == 'production':
        if 'mock' in [settings.USER_DATA_SOURCE, settings.DORM_CHECKOUT_SOURCE, settings.WECHAT_PROVIDER]:
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

### P1-3：Mock数据真实性不足

**完全同意。**

**补充边界样本：**

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
        "2020002": CheckoutStatus(status="pending", date=None),
        "2020003": CheckoutStatus(status="not_started", date=None),
        "2020004": CheckoutStatus(status="unknown", date=None),  # API失败
    }
    
    return students, counselors, dorm_statuses
```

---

## 工期调整响应

**完全接受Codex的工期建议。**

### 修正后的实施计划

| 周次 | 任务 | 交付物 |
|------|------|--------|
| Week 1 | 数据契约、DTO、ImportSource接口、种子数据、导入模型 | 数据契约文档、DTO定义、ImportSource接口 |
| Week 2-3 | CSV导入功能、staging表、upsert逻辑、审计日志 | CSV导入模块、导入校验报告 |
| Week 3-6 | 申请、审批、附件、通知模块 | 核心业务功能 |
| Week 6-7 | 宿舍清退Provider、降级流程、缓存、错误分类 | 宿舍清退集成模块 |

 succeeded in 136ms:
 succeeded in 156ms:
codex
初步判断：41 号文档把“按 40 更新计划”当成低风险动作，但真正的问题是它仍然按传统模块瀑布排期，且把前端、验收、外部依赖和导入治理压到后面。下面我会补几处行号，方便最终意见能落到具体文档位置。
exec
/bin/bash -lc 'rtk nl -ba docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# 下一步工作批判性讨论 - Codex讨论请求
     2	
     3	**文档编号：** 41  
     4	**创建日期：** 2026-05-30  
     5	**讨论类型：** 批判性探讨（多轮讨论）  
     6	**优先级：** P0（决定实施路径）
     7	
     8	---
     9	
    10	## 一、当前状态
    11	
    12	### 1.1 已完成工作
    13	
    14	**API阻塞问题解决方案（文档37-40）：**
    15	- ✓ 识别外部API信息缺失阻塞问题
    16	- ✓ Codex审查指出原方案偏离共识
    17	- ✓ 达成最终共识：Seed/Mock + ImportSource抽象 + CSV主数据导入 + 宿舍清退API适配
    18	- ✓ 工期调整：10周演示版 + 1-2周生产集成缓冲
    19	
    20	**核心架构决策：**
    21	```
    22	外部数据源 (CSV/API/Mock)
    23	    ↓
    24	ImportSource (数据导入源接口)
    25	    ↓
    26	ImportService (导入服务：校验、staging、upsert、软停用)
    27	    ↓
    28	本地数据库 (认证、权限、审批的唯一运行时依据)
    29	    ↑
    30	    │ (运行时查询)
    31	DormCheckoutProvider (宿舍清退实时查询)
    32	```
    33	
    34	### 1.2 当前建议的下一步
    35	
    36	**来自文档40的建议：**
    37	1. 更新实施计划文档（调整Week 1-10任务分配）
    38	2. 开始Week 1工作：数据契约、DTO、ImportSource接口设计
    39	
    40	---
    41	
    42	## 二、讨论目标
    43	
    44	**本次讨论的目的：**
    45	1. **批判性审视** - 质疑当前建议的下一步是否最优
    46	2. **发现问题** - 识别可能遗漏的风险和问题
    47	3. **探索替代方案** - 寻找更好的实施路径
    48	4. **达成共识** - 通过多轮讨论达成一致
    49	
    50	**讨论原则：**
    51	- 不一次性通过，鼓励质疑和反驳
    52	- 提出新观点和替代方案
    53	- 深入分析每个方案的利弊
    54	- 直到双方都认可才达成共识
    55	
    56	---
    57	
    58	## 三、初步建议的下一步（待批判）
    59	
    60	### 3.1 方案A：按文档40建议执行
    61	
    62	**步骤：**
    63	1. **立即执行：** 更新实施计划文档
    64	   - 调整Week 1-10任务分配
    65	   - 将数据契约和接口设计提前到Week 1
    66	   - 明确每周交付物
    67	
    68	2. **Week 1启动：** 数据契约和接口设计
    69	   - 定义StudentDTO、CounselorDTO、ClassMappingDTO
    70	   - 设计IUserDataImportSource接口
    71	   - 设计IDormCheckoutProvider接口
    72	   - 创建种子数据（100学生、10辅导员）
    73	
    74	3. **Week 2-3：** CSV导入功能开发
    75	   - Staging表设计
    76	   - Upsert逻辑
    77	   - 软停用机制
    78	   - 导入审计日志
    79	
    80	**优势：**
    81	- 遵循已达成的共识
    82	- 路径清晰，风险可控
    83	- 避免后续返工
    84	
    85	**潜在问题（需要Codex批判）：**
    86	- 是否过于保守？
    87	- 是否有更快的路径？
    88	- Week 1的工作量是否合理？
    89	- 数据契约是否应该更早确定？
    90	
    91	---
    92	
    93	## 四、请Codex批判性审视的问题
    94	
    95	### 4.1 关于实施顺序
    96	
    97	**问题1：Week 1做数据契约是否太晚？**
    98	- 数据契约影响认证、审批、前端所有模块
    99	- 是否应该在Week 1之前（现在）就冻结数据契约？
   100	- 如果现在冻结，Week 1可以做什么？
   101	
   102	**问题2：是否应该先做最小可行原型（MVP）？**
   103	- 当前计划是按模块顺序开发（认证→申请→审批→...）
   104	- 是否应该先做一个端到端的最小流程？
   105	- 例如：简化版申请+审批+通知，验证整体架构
   106	
   107	**问题3：CSV导入功能是否应该更早？**
   108	- 当前计划Week 2-3做CSV导入
   109	- 但认证模块（Week 2）需要用户数据
   110	- 是否应该Week 1就完成CSV导入？
   111	
   112	### 4.2 关于技术风险
   113	
   114	**问题4：Mock数据是否足够支撑开发？**
   115	- 当前计划用种子数据（100学生、10辅导员）
   116	- 是否会遗漏边界情况？
   117	- 是否需要更真实的测试数据？
   118	
   119	**问题5：接口抽象是否过度设计？**
   120	- ImportSource、ImportService、Provider三层抽象
   121	- 对于首版（CSV导入）是否过于复杂？
   122	- 是否应该先实现CSV导入，后续再抽象？
   123	
   124	**问题6：宿舍清退API集成时机？**
   125	- 当前计划Week 6-7做宿舍清退API对接
   126	- 但申请提交（Week 3）就需要校验宿舍清退状态
   127	- 是否应该更早集成？还是先用Mock？
   128	
   129	### 4.3 关于工期评估
   130	
   131	**问题7：10周工期是否现实？**
   132	- Week 1: 数据契约和接口
   133	- Week 2-3: CSV导入
   134	- Week 3-6: 核心业务
   135	- Week 6-7: 宿舍清退API
   136	- Week 8-9: 前端
   137	- Week 10: 联调
   138	
   139	这个节奏是否合理？哪些环节可能延期？
   140	
   141	**问题8：Week 1的工作量是否饱和？**
   142	- 数据契约、DTO、接口设计
   143	- 种子数据生成
   144	- 导入模型设计
   145	
   146	这些工作是否足够填满一周？是否应该增加其他任务？
   147	
   148	### 4.4 关于替代方案
   149	
   150	**问题9：是否有更好的实施路径？**
   151	- 当前：数据契约→CSV导入→核心业务→API集成→前端→联调
   152	- 替代1：MVP原型→迭代完善
   153	- 替代2：前后端并行开发
   154	- 替代3：API集成优先（如果API信息到位）
   155	
   156	**问题10：是否应该调整模块开发顺序？**
   157	- 当前：认证→申请→审批→附件→通知→集成→前端
   158	- 是否应该：申请+审批核心流程→认证→附件→通知→集成→前端？
   159	- 哪种顺序风险更低？
   160	
   161	---
   162	
   163	## 五、期望的讨论输出
   164	
   165	### 5.1 第一轮讨论
   166	
   167	**请Codex提供：**
   168	1. 对方案A的批判性分析（不要客气，直接指出问题）
   169	2. 识别的风险和遗漏点
   170	3. 替代方案建议（如果有）
   171	4. 对10个问题的回答和反驳
   172	
   173	### 5.2 后续轮次
   174	
   175	**如果第一轮未达成共识：**
   176	- Claude回应Codex的批判
   177	- 提出修正方案或反驳
   178	- Codex继续质疑或提出新观点
   179	- 重复直到达成共识
   180	
   181	### 5.3 最终输出
   182	
   183	**达成共识后：**
   184	- 明确的下一步行动计划
   185	- 调整后的实施路径
   186	- 风险缓解措施
   187	- 关键决策记录
   188	
   189	---
   190	
   191	## 六、讨论范围
   192	
   193	**本次讨论聚焦：**
   194	1. ✓ 下一步工作的优先级和顺序
   195	2. ✓ 实施路径的优化
   196	3. ✓ 工期评估的合理性
   197	4. ✓ 技术风险的识别
   198	
   199	**不在本次讨论范围：**
   200	1. ✗ 已达成共识的架构设计（文档40）
   201	2. ✗ 具体代码实现细节
   202	3. ✗ 前端UI/UX设计
   203	4. ✗ 部署和运维方案
   204	
   205	---
   206	
   207	## 七、补充信息
   208	
   209	### 7.1 项目约束
   210	
   211	- **团队规模：** 2-3人
   212	- **预计工期：** 10周演示版 + 1-2周生产集成
   213	- **外部依赖：** 宿舍清退API信息待提供
   214	- **交付要求：** Week 10可演示版本（Mock数据）
   215	
   216	### 7.2 已有资源
   217	
   218	- **系统设计文档：** 完整的架构、数据库、API设计
   219	- **数据对接文档：** CSV模板、API规范
   220	- **共识文档：** API阻塞解决方案（文档40）
   221	
   222	### 7.3 关键假设
   223	
   224	- CSV导入是首版主数据来源
   225	- 宿舍清退API在Week 6-7前到位
   226	- 微信小程序测试AppID可用
   227	- 开发环境已就绪
   228	
   229	---
   230	
   231	## 八、讨论启动
   232	
   233	**请Codex：**
   234	1. 批判性审视方案A
   235	2. 回答10个问题
   236	3. 提出替代方案（如果有）
   237	4. 指出可能遗漏的风险
   238	
   239	**讨论原则：**
   240	- 不要客气，直接指出问题
   241	- 鼓励质疑和反驳
   242	- 提出新观点和替代方案
   243	- 多轮讨论直到达成共识
   244	
   245	---
   246	
   247	**讨论发起人：** Claude Opus 4.7  
   248	**创建时间：** 2026-05-30  
   249	**期望讨论轮次：** 2-4轮  
   250	**优先级：** P0（决定实施路径）

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
/bin/bash -lc 'rtk nl -ba docs/superpowers/plans/2026-05-27-implementation-plan.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# 毕业生离校申请审批系统 - 实施计划
     2	
     3	**创建日期：** 2026-05-27  
     4	**计划版本：** v1.0  
     5	**预计工期：** 8-10周  
     6	**开发人员：** 2-3人
     7	
     8	---
     9	
    10	## 目标
    11	
    12	实现一个完整的毕业生离校申请审批系统，支持：
    13	- 学生在线提交离校申请
    14	- 辅导员和学工部两级审批
    15	- 附件上传和管理
    16	- 微信通知推送
    17	- 宿舍管理系统对接（API集成）
    18	- Docker容器化部署
    19	
    20	## 范围
    21	
    22	**包含：**
    23	- 后端API开发（Django + DRF）
    24	- 前端开发（React Native + 微信小程序）
    25	- 数据库设计和实现
    26	- 认证授权系统
    27	- 审批流程引擎
    28	- 文件存储系统
    29	- 通知系统
    30	- 外部系统集成
    31	- Docker部署配置
    32	- 单元测试和集成测试
    33	
    34	**不包含：**
    35	- 生产环境运维
    36	- 用户培训
    37	- 数据迁移
    38	- 性能调优（初期）
    39	
    40	## 前置条件
    41	
    42	**开发环境：**
    43	- Python 3.10+
    44	- Node.js 18+
    45	- Docker 20.10+
    46	- Docker Compose 2.0+
    47	- Git
    48	
    49	**技能要求：**
    50	- Python/Django开发经验
    51	- React Native开发经验
    52	- 微信小程序开发经验
    53	- Docker使用经验
    54	- RESTful API设计经验
    55	
    56	**外部依赖：**
    57	- 微信公众平台账号
    58	- 宿舍管理系统API文档和测试环境
    59	
    60	## 成功标准
    61	
    62	**功能完整性：**
    63	- ✓ 所有核心功能实现并通过测试
    64	- ✓ 审批流程完整可用
    65	- ✓ 通知系统正常工作
    66	- ✓ 外部系统对接成功
    67	
    68	**质量标准：**
    69	- ✓ 单元测试覆盖率 > 80%
    70	- ✓ 所有API通过集成测试
    71	- ✓ 端到端测试通过
    72	- ✓ 无严重安全漏洞
    73	
    74	**性能标准：**
    75	- ✓ API响应时间 < 200ms（P95）
    76	- ✓ 支持1000+并发用户
    77	- ✓ 文件上传成功率 > 99%
    78	
    79	**部署标准：**
    80	- ✓ Docker一键部署成功
    81	- ✓ 数据库迁移脚本完整
    82	- ✓ 备份恢复流程验证通过
    83	
    84	---
    85	
    86	## 文件结构规划
    87	
    88	```
    89	graduation-leave-system/
    90	├── backend/                    # Django后端
    91	│   ├── config/                 # 项目配置
    92	│   │   ├── settings/
    93	│   │   │   ├── base.py
    94	│   │   │   ├── dev.py
    95	│   │   │   └── prod.py
    96	│   │   ├── urls.py
    97	│   │   ├── wsgi.py
    98	│   │   └── celery.py
    99	│   ├── apps/
   100	│   │   ├── accounts/           # 用户账户模块
   101	│   │   │   ├── models.py
   102	│   │   │   ├── views.py
   103	│   │   │   ├── serializers.py
   104	│   │   │   ├── permissions.py
   105	│   │   │   └── tests/
   106	│   │   ├── applications/       # 离校申请模块
   107	│   │   │   ├── models.py
   108	│   │   │   ├── views.py
   109	│   │   │   ├── serializers.py
   110	│   │   │   ├── workflows.py
   111	│   │   │   ├── states.py
   112	│   │   │   └── tests/
   113	│   │   ├── approvals/          # 审批管理模块
   114	│   │   │   ├── models.py
   115	│   │   │   ├── views.py
   116	│   │   │   ├── serializers.py
   117	│   │   │   └── tests/
   118	│   │   ├── attachments/        # 附件管理模块
   119	│   │   │   ├── models.py
   120	│   │   │   ├── views.py
   121	│   │   │   ├── serializers.py
   122	│   │   │   ├── storage.py
   123	│   │   │   └── tests/
   124	│   │   ├── notifications/      # 通知模块
   125	│   │   │   ├── models.py
   126	│   │   │   ├── tasks.py
   127	│   │   │   ├── wechat.py
   128	│   │   │   └── tests/
   129	│   │   └── integrations/       # 外部系统集成
   130	│   │       ├── base.py
   131	│   │       ├── dorm_system.py
   132	│   │       └── tests/
   133	│   ├── utils/                  # 工具模块
   134	│   │   ├── validators.py
   135	│   │   ├── exceptions.py
   136	│   │   └── responses.py
   137	│   ├── requirements/
   138	│   │   ├── base.txt
   139	│   │   ├── dev.txt
   140	│   │   └── prod.txt
   141	│   ├── Dockerfile
   142	│   └── manage.py
   143	├── frontend/
   144	│   ├── mobile/                 # React Native应用
   145	│   │   ├── src/
   146	│   │   │   ├── screens/
   147	│   │   │   ├── components/
   148	│   │   │   ├── services/
   149	│   │   │   ├── utils/
   150	│   │   │   └── App.js
   151	│   │   ├── package.json
   152	│   │   └── README.md
   153	│   └── miniprogram/            # 微信小程序
   154	│       ├── pages/
   155	│       ├── components/
   156	│       ├── utils/
   157	│       ├── app.js
   158	│       └── app.json
   159	├── docker/
   160	│   ├── nginx/
   161	│   │   └── nginx.conf
   162	│   └── scripts/
   163	│       └── backup.sh
   164	├── docker-compose.yml
   165	├── .env.example
   166	└── README.md
   167	```
   168	
   169	---
   170	
   171	## 实施阶段
   172	
   173	### 阶段1：项目初始化和基础设施（第1周）
   174	
   175	**目标：** 搭建项目基础框架和开发环境
   176	
   177	**任务清单：**
   178	
   179	1. **创建项目目录结构**
   180	   - 创建backend、frontend、docker目录
   181	   - 初始化Git仓库
   182	   - 创建.gitignore文件
   183	
   184	2. **初始化Django项目**
   185	   - 安装Django 4.2
   186	   - 创建Django项目
   187	   - 配置settings分层（base/dev/prod）
   188	   - 配置PostgreSQL数据库连接
   189	
   190	3. **配置Docker环境**
   191	   - 编写Dockerfile（Django应用）
   192	   - 编写docker-compose.yml
   193	   - 配置Nginx服务
   194	   - 配置MySQL/PostgreSQL服务
   195	   - 配置Redis服务
   196	
   197	4. **配置Celery**
   198	   - 安装Celery
   199	   - 配置Celery应用
   200	   - 配置Celery worker
   201	   - 配置Celery beat
   202	
   203	5. **配置开发工具**
   204	   - 配置pytest
   205	   - 配置代码格式化工具（black、isort）
   206	   - 配置代码检查工具（flake8、pylint）
   207	   - 配置pre-commit hooks
   208	
   209	**验证标准：**
   210	- ✓ `docker-compose up` 成功启动所有服务
   211	- ✓ Django开发服务器可访问
   212	- ✓ 数据库连接成功
   213	- ✓ Redis连接成功
   214	- ✓ Celery worker正常运行
   215	
   216	---
   217	
   218	### 阶段2：用户认证模块（第2周）
   219	
   220	**目标：** 实现用户管理和认证授权系统
   221	
   222	**任务清单：**
   223	
   224	1. **创建用户模型**
   225	   - 定义User模型（继承AbstractUser）
   226	   - 添加字段：student_id、role、wechat_openid等
   227	   - 创建数据库迁移
   228	   - 编写模型测试
   229	
   230	2. **实现学号密码认证**
   231	   - 安装djangorestframework-simplejwt
   232	   - 实现登录API
   233	   - 实现Token刷新API
   234	   - 实现登出API
   235	   - 编写认证测试
   236	
   237	3. **实现微信OAuth2认证**
   238	   - 安装wechatpy
   239	   - 实现微信授权登录API
   240	   - 实现openid绑定逻辑
   241	   - 编写微信认证测试
   242	
   243	4. **实现权限系统**
   244	   - 定义角色权限（student/counselor/admin）
   245	   - 实现RBAC权限类
   246	   - 实现权限装饰器
   247	   - 编写权限测试
   248	
   249	5. **实现用户管理API**
   250	   - 用户列表API
   251	   - 用户详情API
   252	   - 用户更新API
   253	   - 密码修改API
   254	
   255	**验证标准：**
   256	- ✓ 学号密码登录成功，返回JWT Token
   257	- ✓ 微信授权登录成功
   258	- ✓ Token刷新成功
   259	- ✓ 权限控制正常工作
   260	- ✓ 所有测试通过
   261	
   262	---
   263	
   264	### 阶段3：离校申请模块（第3周）
   265	
   266	**目标：** 实现离校申请的创建、查询、更新、提交功能
   267	
   268	**任务清单：**
   269	
   270	1. **创建申请模型**
   271	   - 定义Application模型
   272	   - 添加字段：application_no、status、planned_leave_date等
   273	   - 创建数据库迁移
   274	   - 编写模型测试
   275	
   276	2. **实现状态机**
   277	   - 安装django-fsm
   278	   - 定义状态转换规则
   279	   - 实现状态转换方法
   280	   - 编写状态机测试
   281	
   282	3. **实现申请CRUD API**
   283	   - 创建申请API
   284	   - 获取申请列表API
   285	   - 获取申请详情API
   286	   - 更新申请API
   287	   - 删除申请API（软删除）
   288	
   289	4. **实现申请提交逻辑**
   290	   - 实现提交前校验
   291	   - 实现申请编号生成
   292	   - 实现状态变更
   293	   - 触发通知发送
   294	
   295	5. **实现申请查询过滤**
   296	   - 按状态过滤
   297	   - 按日期范围过滤
   298	   - 按学生过滤
   299	   - 分页查询
   300	
   301	**验证标准：**
   302	- ✓ 创建申请成功
   303	- ✓ 申请编号自动生成
   304	- ✓ 提交申请后状态变更为pending_counselor
   305	- ✓ 查询过滤正常工作
   306	- ✓ 所有测试通过
   307	
   308	---
   309	
   310	### 阶段4：审批管理模块（第4周）
   311	
   312	**目标：** 实现审批流程和审批记录管理
   313	
   314	**任务清单：**
   315	
   316	1. **创建审批记录模型**
   317	   - 定义Approval模型
   318	   - 添加字段：approver_id、action、opinion等
   319	   - 创建数据库迁移
   320	   - 编写模型测试
   321	
   322	2. **实现审批API**
   323	   - 获取待审批列表API
   324	   - 审批通过API
   325	   - 审批驳回API
   326	   - 获取审批历史API
   327	
   328	3. **实现审批流程逻辑**
   329	   - 辅导员审批逻辑
   330	   - 学工部审批逻辑
   331	   - 审批记录创建
   332	   - 状态变更触发
   333	
   334	4. **实现超时监控**
   335	   - 创建Celery定时任务
   336	   - 检查超时审批
   337	   - 发送超时提醒
   338	   - 标记超时状态
   339	
   340	5. **实现审批权限控制**
   341	   - 辅导员只能审批本年级
   342	   - 学工部可以审批所有
   343	   - 权限验证测试
   344	
   345	**验证标准：**
   346	- ✓ 辅导员审批通过后状态变更为pending_admin
   347	- ✓ 学工部审批通过后状态变更为approved
   348	- ✓ 驳回后状态变更为rejected
   349	- ✓ 超时监控正常工作
   350	- ✓ 所有测试通过
   351	
   352	---
   353	
   354	### 阶段5：附件管理模块（第5周）
   355	
   356	**目标：** 实现文件上传、下载、存储管理
   357	
   358	**任务清单：**
   359	
   360	1. **创建附件模型**
   361	   - 定义Attachment模型
   362	   - 添加字段：file_name、file_path、file_size等
   363	   - 创建数据库迁移
   364	   - 编写模型测试
   365	
   366	2. **配置文件存储**
   367	   - 配置本地文件存储
   368	   - 配置MinIO存储（可选）
   369	   - 实现存储抽象层
   370	   - 编写存储测试
   371	
   372	3. **实现附件上传API**
   373	   - 文件上传接口
   374	   - 文件大小验证（最大10MB）
   375	   - 文件类型验证（jpg/png/pdf/doc/docx）
   376	   - 文件路径生成
   377	
   378	4. **实现附件下载API**
   379	   - 文件下载接口
   380	   - 权限验证（只能下载自己的或审批人的）
   381	   - 文件流式传输
   382	
   383	5. **实现附件删除API**
   384	   - 软删除附件记录
   385	   - 物理删除文件（可选）
   386	   - 权限验证
   387	
   388	**验证标准：**
   389	- ✓ 文件上传成功
   390	- ✓ 文件大小和类型验证正常
   391	- ✓ 文件下载成功
   392	- ✓ 权限控制正常
   393	- ✓ 所有测试通过
   394	
   395	---
   396	
   397	### 阶段6：通知模块（第6周）
   398	
   399	**目标：** 实现微信通知推送和通知管理
   400	
   401	**任务清单：**
   402	
   403	1. **创建通知模型**
   404	   - 定义Notification模型
   405	   - 添加字段：title、content、is_read等
   406	   - 创建数据库迁移
   407	   - 编写模型测试
   408	
   409	2. **实现微信通知**
   410	   - 配置微信公众平台
   411	   - 实现模板消息发送
   412	   - 实现通知重试机制
   413	   - 编写微信通知测试
   414	
   415	3. **实现Celery异步任务**
   416	   - 创建发送通知任务
   417	   - 创建批量发送任务
   418	   - 配置任务优先级
   419	   - 编写任务测试
   420	
   421	4. **实现通知API**
   422	   - 获取通知列表API
   423	   - 标记已读API
   424	   - 获取未读数量API
   425	   - 删除通知API
   426	
   427	5. **集成通知到审批流程**
   428	   - 申请提交时通知辅导员
   429	   - 审批通过时通知学生和下一审批人
   430	   - 审批驳回时通知学生
   431	   - 超时时通知审批人
   432	
   433	**验证标准：**
   434	- ✓ 微信通知发送成功
   435	- ✓ 异步任务正常执行
   436	- ✓ 通知API正常工作
   437	- ✓ 审批流程触发通知
   438	- ✓ 所有测试通过
   439	
   440	---
   441	
   442	### 阶段7：外部系统集成（第7周）
   443	
   444	**目标：** 实现宿舍管理系统对接和重试机制
   445	
   446	**任务清单：**
   447	
   448	1. **设计集成接口**
   449	   - 定义ExternalSystemPlugin基类
   450	   - 定义接口规范
   451	   - 定义异常类型
   452	   - 编写接口文档
   453	
   454	2. **实现宿舍系统对接**
   455	   - 实现DormSystemPlugin
   456	   - 实现API调用
   457	   - 实现认证逻辑
   458	   - 编写对接测试
   459	
   460	3. **实现重试机制**
   461	   - 安装tenacity
   462	   - 配置重试策略
   463	   - 实现指数退避
   464	   - 编写重试测试
   465	
   466	4. **实现降级策略**
   467	   - 实现手动上传证明
   468	   - 实现跳过验证选项
   469	   - 记录降级日志
   470	   - 编写降级测试
   471	
   472	5. **集成到审批流程**
   473	   - 提交申请时验证宿舍清退
   474	   - 验证失败时提示用户
   475	   - 验证成功时记录结果
   476	
   477	**验证标准：**
   478	- ✓ 宿舍系统API调用成功
   479	- ✓ 重试机制正常工作
   480	- ✓ 降级策略正常工作
   481	- ✓ 集成到审批流程
   482	- ✓ 所有测试通过
   483	
   484	---
   485	
   486	### 阶段8：前端开发（第8-9周）
   487	
   488	**目标：** 实现React Native应用和微信小程序
   489	
   490	#### 8.1 React Native应用
   491	
   492	**任务清单：**
   493	
   494	1. **项目初始化**
   495	   - 创建React Native项目
   496	   - 配置导航（React Navigation）
   497	   - 配置状态管理（Redux/Context）
   498	   - 配置API客户端（Axios）
   499	
   500	2. **实现认证页面**
   501	   - 登录页面
   502	   - 微信授权页面
   503	   - Token存储和管理
   504	   - 自动登录
   505	
   506	3. **实现申请管理页面**
   507	   - 申请列表页面
   508	   - 创建申请页面
   509	   - 申请详情页面
   510	   - 提交申请页面
   511	
   512	4. **实现审批页面**
   513	   - 待审批列表页面
   514	   - 审批详情页面
   515	   - 审批操作页面
   516	
   517	5. **实现附件上传**
   518	   - 图片选择
   519	   - 文件上传
   520	   - 上传进度显示
   521	   - 附件预览
   522	
   523	6. **实现通知页面**
   524	   - 通知列表页面
   525	   - 通知详情页面
   526	   - 未读标记
   527	
   528	#### 8.2 微信小程序
   529	
   530	**任务清单：**
   531	
   532	1. **项目初始化**
   533	   - 创建小程序项目
   534	   - 配置页面路由
   535	   - 配置API客户端
   536	
   537	2. **实现认证页面**
   538	   - 微信授权登录
   539	   - Token存储
   540	   - 自动登录
   541	
   542	3. **实现申请管理页面**
   543	   - 申请列表页面
   544	   - 创建申请页面
   545	   - 申请详情页面
   546	
   547	4. **实现审批页面**
   548	   - 待审批列表页面
   549	   - 审批操作页面
   550	
   551	5. **实现附件上传**
   552	   - 图片选择
   553	   - 文件上传
   554	   - 附件预览
   555	
   556	**验证标准：**
   557	- ✓ React Native应用在iOS和Android上运行正常
   558	- ✓ 微信小程序运行正常
   559	- ✓ 所有功能正常工作
   560	- ✓ UI/UX符合设计要求
   561	
   562	---
   563	
   564	### 阶段9：测试和部署（第10周）
   565	
   566	**目标：** 完成测试和部署配置
   567	
   568	**任务清单：**
   569	
   570	1. **单元测试**
   571	   - 补充缺失的单元测试
   572	   - 确保覆盖率 > 80%
   573	   - 修复失败的测试
   574	
   575	2. **集成测试**
   576	   - 编写完整审批流程测试
   577	   - 编写外部系统对接测试
   578	   - 编写文件上传下载测试
   579	
   580	3. **端到端测试**
   581	   - 编写移动端自动化测试
   582	   - 编写小程序测试用例
   583	   - 执行手动测试
   584	
   585	4. **性能测试**
   586	   - 使用Locust进行压力测试
   587	   - 测试并发性能
   588	   - 优化性能瓶颈
   589	
   590	5. **部署配置**
   591	   - 完善docker-compose.yml
   592	   - 编写部署文档
   593	   - 编写备份脚本
   594	   - 编写恢复脚本
   595	
   596	6. **文档编写**
   597	   - API文档
   598	   - 部署文档
   599	   - 用户手册
   600	   - 运维手册
   601	
   602	**验证标准：**
   603	- ✓ 所有测试通过
   604	- ✓ 性能测试达标
   605	- ✓ Docker一键部署成功
   606	- ✓ 文档完整
   607	
   608	---
   609	
   610	## 风险和缓解措施
   611	
   612	**风险1：外部系统API不稳定**
   613	- 缓解：实现重试机制和降级策略
   614	- 缓解：提供手动上传证明的备选方案
   615	
   616	**风险2：微信公众平台审核延迟**
   617	- 缓解：提前申请微信公众平台账号
   618	- 缓解：准备测试账号用于开发
   619	
   620	**风险3：数据库性能问题**
   621	- 缓解：提前进行性能测试
   622	- 缓解：优化索引和查询
   623	
   624	**风险4：前端开发延期**
   625	- 缓解：后端API优先完成
   626	- 缓解：前后端并行开发
   627	
   628	**风险5：测试覆盖不足**
   629	- 缓解：TDD开发模式
   630	- 缓解：代码审查机制
   631	
   632	---
   633	
   634	## 交付物
   635	
   636	**代码交付：**
   637	- ✓ 完整的后端代码（Django）
   638	- ✓ 完整的前端代码（React Native + 小程序）
   639	- ✓ Docker部署配置
   640	- ✓ 数据库迁移脚本
   641	- ✓ 测试代码
   642	
   643	**文档交付：**
   644	- ✓ 系统设计文档
   645	- ✓ API文档
   646	- ✓ 部署文档
   647	- ✓ 用户手册
   648	- ✓ 运维手册
   649	
   650	**测试交付：**
   651	- ✓ 单元测试报告
   652	- ✓ 集成测试报告
   653	- ✓ 性能测试报告
   654	- ✓ 端到端测试报告
   655	
   656	---
   657	
   658	## 执行建议
   659	
   660	**开发模式：**
   661	- 采用TDD（测试驱动开发）
   662	- 每个功能先写测试，再写实现
   663	- 频繁提交代码（每完成一个小任务就提交）
   664	- 代码审查（至少一人审查）
   665	
   666	**协作方式：**
   667	- 使用Git Flow工作流
   668	- 主分支：main（生产）、develop（开发）
   669	- 功能分支：feature/xxx
   670	- 修复分支：bugfix/xxx
   671	
   672	**质量保证：**
   673	- 代码格式化（black、isort）
   674	- 代码检查（flake8、pylint）
   675	- 类型检查（mypy）
   676	- 安全检查（bandit）
   677	
   678	---
   679	
   680	**计划结束**

codex
**结论：方案A不应原样执行。**  
它比旧计划好，但仍然是“先后端模块、后前端、最后联调”的瀑布排期。最大风险不是数据契约，而是到 Week 8-10 才发现端到端流程、微信小程序、附件、审批权限、宿舍降级和通知串不起来。文档里把“更新实施计划”列为立即执行事项 [41-next-steps...md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:63)，这太弱了。下一步不该只是改计划，而应产出可运行的纵向切片。

**主要问题**
1. `Week 8-9 前端、Week 10 联调` 风险很高。现有计划仍把前端后置 [41-next-steps...md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/41-next-steps-critical-discussion-request.md:136)，而原计划还同时要求 React Native 和微信小程序 [implementation-plan.md](/home/caohui/projects/graduation-leave-system/docs/superpowers/plans/2026-05-27-implementation-plan.md:486)。2-3 人 2 周做两个端、附件、审批、认证、联调，偏乐观。
2. Week 10 不能既做联调、验收、性能、部署、文档，又兜底前面延期。原计划第10周内容明显塞爆 [implementation-plan.md](/home/caohui/projects/graduation-leave-system/docs/superpowers/plans/2026-05-27-implementation-plan.md:564)。
3. “10周演示版 + 1-2周生产集成”只有在演示范围被砍清楚时才成立。若演示还包含双端、真实微信、完整附件、通知、导入审计、宿舍降级，那不现实。
4. 方案A仍然把 CSV 导入当成前置大模块。更好的做法是先做 `seed/import minimal path`，让认证和审批用同一套落库数据跑起来，再完善 CSV 校验、staging、审计。
5. “数据契约冻结”这个词危险。契约需要版本化和变更机制，不是一次冻结后假装不会变。40号文档已有 DTO 和 ImportResult 雏形 [40-api-blocking...md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-30/40-api-blocking-solution-consensus.md:100)，现在要做的是契约测试和样例数据包。

**10个问题回答**
1. Week 1 做数据契约太晚吗？不该等到 Week 1 结束。现在就应冻结 v0.1：字段、枚举、样例 CSV、错误码、前端 API mock。Week 1 用它跑纵向切片。
2. 是否先做 MVP？是，必须。先做“学生登录/伪登录 -> 提交申请 -> 辅导员审批 -> 学工部审批 -> 状态可查”的端到端最小流程。
3. CSV 是否更早？不应 Week 1 完整完成，但 Week 1 必须完成最小导入路径：seed/CSV 二选一落库到真实 users/class mapping 表。完整 staging、审计、软停用放 Week 2。
4. Mock 数据够吗？100学生/10辅导员只够演示，不够测试。需要 fixture matrix：无班级、重复学号、辅导员停用、多班级、非毕业生、延期、宿舍 API 401/404/429/500/timeout。
5. 抽象是否过度？方向不算过度，但实现可能过度。保留 DTO、ImportSource、DormCheckoutProvider 边界；不要一开始铺满复杂 Provider 层级和泛型框架。
6. 宿舍 API 何时集成？Mock Provider 和契约测试必须 Week 1 进入提交申请流程；真实 API 可 Week 6-7，但接口信息获取和样例响应不能等到 Week 6。
7. 10周现实吗？演示版可以，但要砍范围：优先微信小程序或一个 Web/RN 壳，不要默认双端完整交付。生产就绪不现实，尤其原计划还要求 80% 覆盖率、P95、1000并发 [implementation-plan.md](/home/caohui/projects/graduation-leave-system/docs/superpowers/plans/2026-05-27-implementation-plan.md:68)。
8. Week 1 工作量饱和吗？不是不饱和，是目标错了。Week 1 应交付可运行骨架、契约测试、seed 数据、最小审批流，而不是只交文档和接口。
9. 更好路径？有：`契约v0.1 + 纵向切片 -> CSV导入硬化 -> 核心流程扩展 -> 前端并行 -> 外部集成 -> 验收硬化`。
10. 模块顺序要调吗？要。不要“认证完整后再申请、申请完整后再审批”。改成薄认证 + 申请审批核心流优先，通知/附件/完整微信登录后补。

**替代方案**
建议改成：

- Week 0-1：契约 v0.1、fixture 数据、后端骨架、薄认证、最小申请审批闭环、Dorm Mock 接入提交校验。
- Week 2：CSV 导入 v1：staging、校验报告、upsert、软停用、审计。
- Week 3-4：申请/审批权限、附件最小可用、状态机和审计补齐。
- Week 4-6：前端并行，不等后端全完；先小程序主流程。
- Week 6-7：宿舍真实 API 适配；若 API 不到位，保留 mock + 人工证明降级。
- Week 8-9：通知、异常流、UAT 修复、导入演练。
- Week 10：只做验收、演示、缺陷修复，不再塞新功能。

遗漏的关键点：验收范围没有砍清楚，双端交付没有优先级，真实 API 信息获取没有责任人和截止日期，导入失败后的人工处理流程不明确，数据契约缺少版本管理，Week 10 没有缓冲。第一轮我的态度是：方案A可以作为底稿，但不能作为执行计划。
tokens used
61,165

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
