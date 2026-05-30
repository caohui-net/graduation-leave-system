# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-05-27T03:33:51.845Z

## Original task

审查 docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md - 这是我们对你之前审查意见的回应。请确认：1) 我们对项目约束（只对接宿管系统）的理解是否合理 2) 我们接受/不接受的建议是否有问题 3) 账号标识映射方案是否可行 4) 实施路径是否合理 5) 是否还有遗漏的关键问题

## Final prompt

审查 docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md - 这是我们对你之前审查意见的回应。请确认：1) 我们对项目约束（只对接宿管系统）的理解是否合理 2) 我们接受/不接受的建议是否有问题 3) 账号标识映射方案是否可行 4) 实施路径是否合理 5) 是否还有遗漏的关键问题

## Raw output

```text
**结论：方向基本可以接受，但不建议原样进入 v2。主要还有 3 个需要修正的点。**

**发现**
1. [33-response-to-codex-data-review.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:329) 里的 CSV “全量覆盖（清空后重新导入）”有风险。`users` 会被 `applications.student_id/counselor_id/admin_id` 外键引用，不能清空重建。应改为：导入到 staging 表、校验通过后按主键 upsert、缺失记录软停用、保留导入批次和回滚点。
2. [33-response-to-codex-data-review.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:168) 新增 `employee_id` 方案可行，但当前系统设计里 `users.student_id` 是 `UNIQUE NOT NULL`，见 [system-design.md](/home/caohui/projects/graduation-leave-system/docs/design/2026-05-27-system-design.md:262)。若辅导员/管理员 `student_id` 为空，必须同步修改模型约束：`student_id` 可空且仅学生唯一，`employee_id` 可空且仅教职工唯一，并明确 `username`/登录账号如何生成。
3. [33-response-to-codex-data-review.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:381) 你们要求 `class_id` 作为核心映射键是对的，但当前用户表设计只有 `class_name`，没有 `class_id`，见 [system-design.md](/home/caohui/projects/graduation-leave-system/docs/design/2026-05-27-system-design.md:279)。需要把 `class_id` 加入学生用户或学生档案，否则班级-辅导员映射无法稳定落地。

**逐项确认**
1. 项目约束“只对接宿管系统”作为系统集成边界是合理的。  
但文档不要写成“学生、辅导员、班级映射天然由宿管系统负责”。更准确的表述是：本系统只向宿管系统取数；宿管系统需作为数据归集和交付责任方，确认其是否能提供上游数据、字段字典、更新时间、联系人和故障响应。

2. 接受/不接受建议基本合理。  
不接受“直接面向多方反馈”可以成立；接受 CSV 优先、`checkout_status` 必填、历史审批人不自动改写都合理。`is_graduating` 首版保留也可以，但建议至少补一个业务语义说明：`is_graduating=true` 等同于“具备本批次离校申请资格”；更稳的是新增 `eligible_for_leave`。

3. 账号标识映射方案可行，但要补约束。  
推荐保留 `student_id` 和 `employee_id` 两列，不复用字段。需要明确：
`student_id` 仅学生必填；`employee_id` 仅 counselor/admin 必填；分别建条件唯一索引；班级映射只引用 counselor 的 `employee_id`；管理员也用 `employee_id` 但不参与班级映射。

4. 实施路径总体合理。  
建议在阶段 2 前增加“数据模型修订”：`employee_id`、`class_id`、导入批次表、默认终审人配置。CSV 导入阶段不能做物理清空，应做 staging + 校验 + upsert + 软停用。上线前验收还应加两条：所有可申请学生 100% 解析到有效辅导员；提交申请时 100% 能解析到有效终审人。

5. 仍遗漏的关键问题：
- 离校批次配置：毕业届别、开放时间、允许计划离校日期范围。
- 导入审计：上传人、文件哈希、批次号、差异报告、失败明细。
- 停用规则：学生毕业归档、辅导员离职/调岗、管理员离岗后的未完成任务处理。
- 默认终审人失效兜底：默认管理员被停用时禁止上线或阻断提交。
- 正式文档需删除所有 `<thinking>` 段落。

总体判断：可以基于这份回应形成共识，但 v2 修改时先修正“全量覆盖清空”、`employee_id` 约束、`class_id` 落库这三处，否则实施时会撞到数据一致性问题。


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
session id: 019e677d-7bd7-73a3-8142-3544cf3beae7
--------
user
审查 docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md - 这是我们对你之前审查意见的回应。请确认：1) 我们对项目约束（只对接宿管系统）的理解是否合理 2) 我们接受/不接受的建议是否有问题 3) 账号标识映射方案是否可行 4) 实施路径是否合理 5) 是否还有遗漏的关键问题
codex
我会先读取项目指令和这份回应文档，再对照相关上下文文件确认约束与实施方案是否自洽。
exec
/bin/bash -lc "sed -n '1,260p' docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 对Codex数据需求审查的回应

**回应时间：** 2026-05-27  
**回应对象：** `32-codex-data-requirements-review.md`  
**原始文档：** `31-data-source-requirements-consensus.md`

---

## 一、核心项目约束澄清

**重要说明：本项目只对接宿管系统，不直接对接教务、人事、学工等其他系统。**

### 1.1 项目边界

本毕业离校系统的数据对接范围限定为：
- **唯一数据源：** 宿管系统
- **数据获取方式：** 通过宿管系统提供的数据库、API或CSV文件
- **数据责任方：** 宿管系统负责人

### 1.2 为什么只对接宿管系统

1. **项目定位：** 本系统是宿管系统的配套子系统，不是全校级统一离校平台
2. **数据归集：** 宿管系统已从教务、人事、学工等系统归集了所需数据
3. **实施简化：** 避免多方对接的协调成本和技术复杂度
4. **权责清晰：** 数据质量、更新时效由宿管系统统一负责

### 1.3 对Codex审查的影响

基于上述约束，Codex审查中的部分建议需要重新评估：
- ✅ **接受：** 对接方式、字段定义、实施细节的建议
- ❌ **不接受：** 将反馈对象从"宿管系统"改为"多方数据负责人"
- 🔄 **调整：** 待反馈问题需明确"宿管系统能否提供这些数据"

---

## 二、对Codex四大核心问题的逐项回应

### 2.1 问题1：反馈对象错误

**Codex意见：** 将"提交给宿管系统方"改为"提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人"。

**我们的回应：** ❌ **不接受此建议**

**理由：**

基于项目约束（只对接宿管系统），原文档的反馈对象是正确的：
1. 本系统只对接宿管系统，不直接对接教务、人事、学工
2. 学生、辅导员、班级映射等数据由宿管系统负责提供
3. 宿管系统如何获取这些数据（是否从教务/人事归集）是宿管系统的内部实现
4. 我们的职责是明确需求，由宿管系统确认能否提供

**但我们接受Codex的隐含提醒：**

需要在待反馈问题中明确询问宿管系统：
- 这些数据是否在宿管系统数据库中？
- 如果不在，宿管系统能否从其他系统归集后提供？
- 如果无法提供，是否需要调整项目对接范围？

**修改方案：**
- 保持反馈对象为"宿管系统方"
- 在待反馈问题中增加："宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？如不包含，能否从教务/人事/学工系统归集后提供？"

---

### 2.2 问题2：对接方式过激

**Codex意见：** 学生、辅导员、班级映射的"DB优先"改为"CSV/Excel优先，API/DB增强"。

**我们的回应：** ✅ **完全接受**

**理由：**

1. **实施周期：** CSV/Excel导入最快，DB直连需要安全审批和网络配置
2. **变更频率：** 账号数据变更频率低（学期级），不需要实时同步
3. **风险控制：** CSV导入可以先验证、再导入、可回滚；DB直连风险更高
4. **首版策略：** 先用CSV快速上线，后续根据数据变更频率决定是否升级为API/DB

**修改方案：**

| 数据源 | 原方案 | 修改后方案 |
|--------|--------|-----------|
| 学生基本信息 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先** / API或DB视图增强 |
| 辅导员基本信息 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先** / 人事或统一身份API增强 |
| 班级-辅导员对应关系 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
| 宿舍清退数据 | API优先 / DB备选 / CSV降级 | **保持不变**（API优先合理） |

**特别说明：**
- 宿舍清退数据保持API优先，因为需要实时校验学生提交时的清退状态
- 账号数据采用CSV首版，上线后根据实际变更频率决定是否升级

---

### 2.3 问题3：字段定义不一致

**Codex意见：** `checkout_status` 在本文档中标为可选，但既有字段共识中API响应建议必填。

**我们的回应：** ✅ **完全接受**

**理由：**

1. **业务必要性：** 清退状态是提交前置校验的核心字段，必须明确
2. **一致性：** 应与之前的字段共识保持一致
3. **降级处理：** 即使API查询失败，也应返回 `unknown` 而非空值

**修改方案：**

| 字段 | 原定义 | 修改后定义 |
|------|--------|-----------|
| `checkout_status` | 可选 | **必填**，枚举：`completed`/`pending`/`not_started`/`unknown` |
| `checkout_date` | 可选 | **条件必填**：当 `checkout_status = completed` 时必填 |
| `source_updated_at` | 未列出 | **建议新增**：记录外部系统数据更新时间 |

**枚举值说明：**
- `completed`：已完成清退
- `pending`：清退中（已申请但未完成）
- `not_started`：未开始清退
- `unknown`：查询失败或数据不可用（用于API异常时的降级）

---

### 2.4 问题4：缺实施细节

**Codex意见：** 缺少终审管理员分配规则、账号标识映射、历史审批人一致性规则、多辅导员场景处理。

**我们的回应：** ✅ **完全接受，需要补充**

这些确实是实施级关键问题，需要在文档中明确。我们逐项回应：

#### 4.1 终审管理员分配规则

**问题：** 学生提交申请时，系统如何确定 `admin_id`（终审管理员）？

**我们的方案：**

首版采用**固定终审人**方案：
1. 系统配置表中设置默认终审管理员（1-2人）
2. 所有申请提交时自动分配给默认终审人
3. 管理员可以在后台手动转交给其他管理员

**后续增强方案（P1）：**
- 轮转分配：按提交顺序轮流分配给管理员组
- 按学院分配：不同学院的申请分配给不同终审人
- 负载均衡：根据管理员当前待审数量智能分配

**修改方案：** 在文档中增加"终审管理员配置"章节，说明首版采用固定终审人。

---

#### 4.2 账号标识映射

**问题：** 辅导员和管理员使用 `employee_id`，但系统数据库模型中如何存储和映射？

**我们的方案：**

当前数据库设计：
- `users` 表有 `student_id` 字段（学生学号）
- 辅导员和管理员账号需要统一标识字段

**两种方案对比：**

| 方案 | 优点 | 缺点 | 我们的选择 |
|------|------|------|-----------|
| 复用 `student_id` 字段存储 `employee_id` | 不需要改表结构 | 字段名语义不清 | ❌ |
| 新增 `employee_id` 字段 | 语义清晰，扩展性好 | 需要修改表结构 | ✅ |

**修改方案：**

1. `users` 表增加 `employee_id` 字段（可空）
2. 学生账号：`student_id` 必填，`employee_id` 为空
3. 辅导员/管理员账号：`employee_id` 必填，`student_id` 为空
4. 登录时根据账号类型判断使用哪个字段

**数据导入映射：**
- 学生CSV：`student_id` → `users.student_id`
- 辅导员CSV：`employee_id` → `users.employee_id`
- 班级映射CSV：`counselor_employee_id` → 查询 `users` 表中 `employee_id` 匹配的记录

---

#### 4.3 历史审批人一致性规则

**问题：** 班级-辅导员映射变更后，已提交申请中的 `counselor_id` 是否自动改写？

**我们的方案：** ✅ **不自动改写，保持历史一致性**

<thinking>
这是一个重要的业务规则。如果班级映射变更后自动改写已提交申请的审批人，会导致：
1. 审批流程混乱（原审批人已审批，新审批人不知情）
2. 审计追溯困难（无法还原当时的审批人是谁）
3. 权限边界模糊（新审批人可能不应该看到旧申请）

正确的做法是：
1. 已提交的申请保持原审批人不变
2. 新提交的申请使用新映射
3. 如需改派，由管理员显式操作并记录审计日志
</thinking>

**理由：**

1. **审批流程完整性：** 已提交申请的审批人是提交时确定的，不应因后续映射变更而改变
2. **审计追溯：** 保持历史审批人记录，便于追溯当时的审批责任
3. **权限边界：** 新辅导员不应自动获得旧申请的审批权限

**具体规则：**

| 场景 | 处理方式 |
|------|----------|
| 申请提交时 | 根据当前班级-辅导员映射确定 `counselor_id` |
| 映射变更后，已提交申请 | `counselor_id` **不变**，保持原审批人 |
| 映射变更后，新提交申请 | 使用新映射确定 `counselor_id` |
| 需要改派审批人 | 管理员显式操作，记录审计日志（操作人、时间、原因） |

**数据库设计支持：**
- `applications` 表的 `counselor_id` 是快照字段，不关联外键级联更新
- 审计日志表记录审批人变更操作

---

#### 4.4 多辅导员场景处理

**问题：** 一个班级是否可能有多个辅导员？如何处理主辅导员、代理辅导员、临时负责人？

**我们的方案：** 首版**不支持**多辅导员，后续根据实际需求扩展

<thinking>
多辅导员场景会增加系统复杂度：
1. 数据模型需要支持一对多关系
2. 审批流程需要确定主审批人
3. 权限边界需要明确（所有辅导员都能审批？还是只有主辅导员？）
4. 通知逻辑需要调整（通知所有辅导员？还是只通知主辅导员？）

首版应该简化，采用一班一主辅导员的模型。如果实际运行中发现确实需要多辅导员支持，再扩展。
</thinking>

**首版限制：**
1. 一个班级只能映射一个辅导员（主辅导员）
2. 班级-辅导员映射表中，`class_id` 必须唯一
3. CSV导入时强校验：同一 `class_id` 不能出现多次

**如果实际存在多辅导员场景：**

| 场景 | 首版处理方式 |
|------|-------------|
| 一班多辅导员 | 只导入主辅导员，其他辅导员不导入 |
| 代理辅导员 | 临时修改班级映射，指向代理辅导员 |
| 辅导员调岗 | 更新班级映射，新申请使用新辅导员 |

**后续扩展方案（P1）：**

如果实际需求强烈，可以扩展为：
1. 班级-辅导员映射表增加 `is_primary` 字段（标识主辅导员）
2. 允许同一 `class_id` 有多条记录，但只能有一个 `is_primary=true`
3. 申请提交时使用主辅导员作为 `counselor_id`
4. 所有辅导员都能查看本班申请，但只有主辅导员能审批

**修改方案：** 在文档中明确说明首版只支持一班一主辅导员，并在待反馈问题中询问宿管系统是否存在多辅导员场景。

---

## 三、对其他审查意见的回应

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
/bin/bash -lc "pwd && rg --files -g 'AGENTS.md' -g 'docs/discussions/codex-review-2026-05-27/**' -g '"'!node_modules'"'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
/home/caohui/projects/graduation-leave-system
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md
docs/discussions/codex-review-2026-05-27/17-claude-analysis-part4-deployment-security.md
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md
docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md
docs/discussions/codex-review-2026-05-27/02-architecture-response.md
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md
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
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md
docs/discussions/codex-review-2026-05-27/21-final-consensus.md
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md

codex
我已经看到回应文档的主体，里面还包含一些 `<thinking>` 残留，这本身会影响正式文档质量。接下来我会读完后半部分，并回看前置共识与我之前的审查意见，避免只按单篇文档判断。
exec
/bin/bash -lc "rtk sed -n '261,620p' docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:

### 3.1 数据源完整性（第二章）

**Codex结论：** P0数据源覆盖完整，未遗漏关键数据。

**我们的回应：** ✅ **认同**

同意以下判断：
- 图书馆清书、财务结清、学籍状态不列为P0是合理的
- 当前保留截图上传和人工审核的降级方案
- 这些数据不应阻塞首版上线

### 3.2 字段定义合理性（第三章）

**Codex建议：**
1. `is_graduating` 建议改名或补充为 `eligible_for_leave`
2. `graduation_year` 示例应与当前项目日期保持一致（2026）
3. `phone` 是否可选需要结合微信绑定策略确认

**我们的回应：** 🔄 **部分接受**

| 建议 | 我们的回应 |
|------|-----------|
| `is_graduating` 改名 | ❌ 首版保持不变，字段含义已明确 |
| `graduation_year` 示例改为2026 | ✅ 接受，统一为2026 |
| `phone` 可选性确认 | ✅ 接受，需要在待反馈问题中询问宿管系统 |

**理由：**
- `is_graduating` 字段名虽不完美，但首版已足够表达"是否为当届毕业生"
- 延期毕业、结业等异常状态可以通过 `is_graduating=false` 排除
- 如果后续需要更细粒度的状态，再扩展为 `graduation_status` 枚举

### 3.3 对接方式可行性（第四章）

**Codex建议：**
1. DB直连需要安全边界清晰、只读视图
2. API需补充分页、增量同步、错误码、限流、重试、幂等
3. CSV需补充导入覆盖策略、重复数据处理、失败回滚

**我们的回应：** ✅ **完全接受**

这些都是技术实施的关键细节，需要在文档中补充。

<thinking>
Codex提出的这些技术要求都很合理，是实际对接时必须考虑的问题。我需要在回应中明确：
1. 我们接受这些建议
2. 说明如何在文档中补充这些内容
3. 给出具体的补充方案
</thinking>

**补充方案：**

在文档"三、数据源详细说明"的每个数据源章节中，增加"技术要求"小节：

**DB直连技术要求：**
- 只读账号，不得有写权限
- 使用只读视图或同步库，不直接访问生产业务表
- IP白名单限制，只允许应用服务器访问
- 连接池配置：最大连接数、超时时间、重试策略

**API技术要求：**
- 分页支持：每页最多100条，支持 `page`/`page_size` 参数
- 增量同步：支持 `updated_after` 参数，只返回指定时间后更新的数据
- 错误码规范：200成功、400参数错误、401认证失败、500服务器错误
- 限流策略：每分钟最多60次请求
- 重试机制：失败后指数退避重试，最多3次
- 幂等性：同一请求多次调用结果一致

**CSV技术要求：**
- 导入策略：首版采用**全量覆盖**（清空后重新导入）
- 重复数据：按主键（学号/工号/班级ID）去重，保留最后一条
- 失败处理：导入前备份，失败后回滚到备份
- 校验报告：导入后生成校验报告（成功数、失败数、错误明细）

### 3.4 数据量估算（第五章）

**Codex意见：** 当前估算基本合理，但需要明确是"当届毕业生"还是"全部学生"。

**我们的回应：** ✅ **接受，需要明确**

<thinking>
数据量估算需要明确两个问题：
1. 系统是只服务当届毕业生（约1000人），还是保留多届历史数据（约10000人）？
2. 班级映射数量是否考虑了历史有效期和多辅导员场景？

这会影响数据库容量设计和性能优化策略。
</thinking>

**明确说明：**

| 数据项 | 首版范围 | 容量设计 | 说明 |
|--------|----------|----------|------|
| 学生账号 | 当届毕业生 | 1000人/届 | 只导入当届，历史届别不保留 |
| 系统容量 | 支持多届历史 | 10000人 | 数据库设计按10000人容量 |
| 辅导员账号 | 当前在职 | 50人 | 离职辅导员标记 `is_active=false` |
| 班级映射 | 当届有效映射 | 50-100条 | 首版不考虑历史有效期 |
| 学工部管理员 | 当前在职 | 5人 | 手动创建 |

**待反馈问题补充：**
- 宿管系统能否只提供当届毕业生数据？
- 是否需要保留历史届别数据用于查询和统计？

### 3.5 待反馈问题（第六章）

**Codex建议：** 扩展为面向多方的数据确认清单，新增12个问题。

**我们的回应：** 🔄 **部分接受，需要调整**

基于项目约束（只对接宿管系统），我们接受Codex建议的问题方向，但需要调整提问对象和表述。

**修改方案：**

将Codex建议的12个问题调整为"向宿管系统确认的问题清单"：

**数据可用性确认：**
1. 宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？
2. 如不包含，能否从教务/人事/学工系统归集后提供？
3. 能否只提供当届毕业生数据（约1000人），还是必须提供全部学生数据？

**字段和标识确认：**
4. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
5. 辅导员工号（`employee_id`）是否全校唯一？是否与统一身份认证、人事系统工号一致？
6. 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？

**多辅导员场景确认：**
7. 是否存在一个班级多个辅导员、代理辅导员、临时负责人或辅导员调岗场景？
8. 班级-辅导员映射变更频率如何？是否能提供当前有效映射和历史有效期？

**对接方式确认：**
9. 优先推荐的对接方式是什么？（DB直连 / API / CSV导入）
10. 各数据源能否提供测试数据、测试环境和字段字典？
11. CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？

**异常处理确认：**
12. 外部系统不可用、数据延迟或查询失败时，业务上允许怎样的人工降级？
13. 是否有统一身份认证或微信绑定前置要求？
14. 是否需要导入手机号/邮箱用于找回密码或二次验证？

**实施保障确认：**
15. 数据提供方能否承诺导出频率、数据更新时间、联系人和故障响应时间？

### 3.6 实施建议（第七章）

**Codex建议：** 调整推荐方案和实施路径。

**我们的回应：** ✅ **完全接受**

<thinking>
Codex建议的实施路径非常合理：
1. 先确认数据权责方和联系人
2. 先落地CSV模板
3. 实现导入校验报告
4. 再对接宿舍清退API
5. 上线前冻结数据批次

这个路径符合敏捷开发的原则：先简单后复杂，先验证后扩展。
</thinking>

**修改后的实施路径：**

**阶段1：数据确认（1周）**
1. 向宿管系统提交本需求文档
2. 确认数据可用性、字段定义、对接方式
3. 获取测试数据和字段字典
4. 明确联系人和故障响应方式

**阶段2：CSV导入实现（2周）**
1. 设计三份CSV模板：学生、辅导员、班级-辅导员映射
2. 实现CSV导入功能和校验逻辑
3. 生成导入校验报告（成功数、失败数、错误明细）
4. 重点校验：学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射

**阶段3：宿舍清退API对接（1周）**
1. 对接宿管系统宿舍清退API
2. 实现API失败、超时、数据过期的降级处理
3. 测试API异常场景和人工证明流程

**阶段4：上线前验收（1周）**
1. 冻结当届数据批次
2. 完成一次全量导入演练
3. 清零异常清单（无效学号、无效工号、未映射班级）
4. 确认终审管理员配置

**阶段5：上线后优化（按需）**
1. 根据数据变更频率决定是否升级为API/DB同步
2. 根据实际需求决定是否支持多辅导员场景

---

## 四、总结和下一步行动

### 4.1 回应总结

**完全接受的建议（✅）：**
1. 对接方式从"DB优先"改为"CSV/Excel首版优先，API/DB增强"
2. `checkout_status` 改为必填，增加枚举值
3. 补充终审管理员分配规则
4. 补充账号标识映射方案（新增 `employee_id` 字段）
5. 明确历史审批人一致性规则（不自动改写）
6. 明确首版不支持多辅导员场景
7. 补充DB/API/CSV的技术要求细节
8. 明确数据量估算范围（当届毕业生）
9. 扩展待反馈问题清单
10. 调整实施路径（CSV优先，分阶段实施）

**不接受的建议（❌）：**
1. 将反馈对象从"宿管系统"改为"多方数据负责人"
   - 理由：项目只对接宿管系统，不直接对接教务/人事/学工

**部分接受的建议（🔄）：**
1. `is_graduating` 改名：首版保持不变，后续根据需要扩展
2. 待反馈问题：接受问题方向，但调整为"向宿管系统确认"

### 4.2 需要修改的具体内容

基于上述回应，我们需要对 `31-data-source-requirements-consensus.md` 进行以下修改：

**修改1：数据源概述表（第二章）**
- 调整对接方式优先级：学生/辅导员/班级映射改为"CSV/Excel首版优先"

**修改2：学生基本信息（第三章）**
- `graduation_year` 示例从2024改为2026
- 补充说明：`is_graduating=true` 表示具备本批次离校申请资格

**修改3：宿舍清退数据（第三章）**
- `checkout_status` 改为必填，增加枚举值说明
- `checkout_date` 改为条件必填
- 新增 `source_updated_at` 字段（建议）

**修改4：辅导员基本信息（第三章）**
- 补充说明：`employee_id` 必须全校唯一
- 补充说明：`is_active=false` 时的处理规则

**修改5：班级-辅导员对应关系（第三章）**
- 补充说明：首版只支持一班一主辅导员
- 补充说明：`class_id` 必须唯一，不允许重复

**修改6：对接方式（第四章）**
- 每个数据源增加"技术要求"小节
- 补充DB/API/CSV的具体技术要求

**修改7：数据量估算（第五章）**
- 明确说明：学生数据只包含当届毕业生（约1000人）
- 明确说明：系统容量设计按10000人

**修改8：待反馈问题（第七章）**
- 扩展为15个问题的确认清单
- 增加"数据可用性确认"、"字段和标识确认"、"多辅导员场景确认"等分类

**修改9：实施建议（第七章）**
- 调整推荐方案：CSV首版优先
- 补充分阶段实施路径（5个阶段）

**修改10：新增章节**
- 新增"终审管理员配置"章节
- 新增"账号标识映射方案"章节
- 新增"历史审批人一致性规则"章节
- 新增"多辅导员场景说明"章节

### 4.3 下一步行动

**立即行动（本次讨论）：**
1. ✅ 已完成：生成本回应文档（33-response-to-codex-data-review.md）
2. 待Codex确认：Codex审查本回应文档，确认我们的理解和方案是否合理
3. 达成共识：基于Codex反馈，形成最终共识

**后续行动（共识达成后）：**
1. 创建修订版文档：`31-data-source-requirements-consensus-v2.md`
2. 按照4.2节的修改清单逐项修改
3. 提交给宿管系统方反馈
4. 根据宿管系统反馈调整方案
5. 启动实施（按3.6节的5阶段路径）

### 4.4 需要Codex进一步确认的问题

<thinking>
我需要列出一些需要Codex进一步确认的问题，特别是我们不接受或部分接受的建议，需要Codex的反馈。
</thinking>

1. **项目约束确认：** 我们明确项目只对接宿管系统，不直接对接教务/人事/学工。Codex是否认同这个约束下，原文档的反馈对象（宿管系统方）是正确的？

2. **账号标识映射方案：** 我们提出新增 `employee_id` 字段的方案。Codex是否认同这个方案？是否有更好的替代方案？

3. **多辅导员场景：** 我们提出首版不支持多辅导员，后续根据需求扩展。Codex是否认同这个策略？是否建议首版就支持？

4. **实施路径：** 我们接受了CSV首版优先的建议，并补充了5阶段实施路径。Codex是否认同这个路径？是否有需要调整的地方？

5. **字段定义：** 我们保持 `is_graduating` 字段名不变。Codex是否认同首版保持不变的策略？

---

## 五、结语

感谢Codex的详细审查和建设性建议。本回应文档明确了我们的立场：

- **核心约束：** 项目只对接宿管系统
- **接受建议：** CSV首版优先、字段定义统一、补充实施细节
- **保持立场：** 反馈对象为宿管系统方

期待Codex对本回应文档的反馈，以便我们达成最终共识，推进数据对接工作。


exec
/bin/bash -lc "rtk sed -n '1,320p' docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 数据源需求共识文档

**文档版本：** v1.0  
**创建时间：** 2026-05-27  
**目的：** 明确毕业离校系统所需的数据源，提交给宿管系统方反馈

---

## 一、数据源概述

本系统需要以下数据源支持系统运行：

| 数据源 | 优先级 | 用途 | 对接方式 |
|--------|--------|------|----------|
| 学生基本信息 | P0 | 创建学生账号、身份识别、班级映射 | DB优先 / API备选 / CSV降级 |
| 宿舍清退数据 | P0 | 验证学生是否完成宿舍清退 | API优先 / DB备选 / CSV降级 |
| 辅导员基本信息 | P0 | 创建辅导员账号、审批权限 | DB优先 / API备选 / CSV降级 |
| 班级-辅导员对应关系 | P0 | 自动分配审批人 | DB优先 / API备选 / CSV降级 |
| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |

**对接方式说明：**
- **DB优先**：直接读取宿管系统数据库（推荐，支持MySQL/SQL Server/Oracle）
- **API备选**：调用宿管系统提供的API接口
- **CSV降级**：当无法提供DB访问或API时，通过CSV文件导入

---

## 二、P0数据源详细要求

### 2.1 学生基本信息

**用途：**
- 创建学生账号（用于登录系统）
- 身份识别和验证
- 展示学生院系、专业、班级信息
- 自动分配审批人（根据班级匹配辅导员）

**必需字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 学号 | student_id | 文本 | 是 | 学生唯一标识 | 2020010101 |
| 姓名 | name | 文本 | 是 | 学生姓名 | 张三 |
| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
| 专业 | major | 文本 | 是 | 所属专业 | 计算机科学与技术 |
| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2020-01 |
| 班级名称 | class_name | 文本 | 是 | 班级名称（用于展示） | 计算机2020级1班 |
| 年级 | grade | 整数 | 是 | 入学年份 | 2020 |
| 毕业年份 | graduation_year | 整数 | 是 | 预计毕业年份 | 2024 |
| 是否毕业生 | is_graduating | 布尔 | 是 | 是否为当届毕业生 | true |

**可选字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 手机号 | phone | 文本 | 否 | 用于通知 | 13800138000 |
| 邮箱 | email | 文本 | 否 | 用于通知 | student@example.com |

**数据量：** 约1000人/届

**对接方式1：数据库直连（推荐）**
```sql
-- 示例查询（假设宿管系统有学生表）
SELECT 
    student_id,
    name,
    department,
    major,
    class_id,
    class_name,
    grade,
    graduation_year,
    is_graduating,
    phone,
    email
FROM students
WHERE is_graduating = true
  AND graduation_year = 2024;
```

**对接方式2：API接口（备选）**
```
GET /api/students?graduation_year=2024&is_graduating=true
```

**对接方式3：CSV文件导入（降级）**
- 文件名：`students_YYYYMMDD.csv`
- 字符编码：UTF-8
- 模板文件：`docs/templates/学生基本信息导入模板.csv`

---

### 2.2 宿舍清退数据

**用途：**
- 验证学生是否完成宿舍清退
- 作为离校申请的前置条件

**必需字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 学号 | student_id | 文本 | 是 | 学生学号 | 2020010101 |
| 姓名 | name | 文本 | 是 | 学生姓名 | 张三 |
| 宿舍楼栋 | dorm_building | 文本 | 否 | 宿舍楼栋名称 | 1号楼 |
| 宿舍房间号 | dorm_room | 文本 | 否 | 宿舍房间号 | 101 |
| 床号 | bed_number | 文本 | 否 | 床位号 | 1 |
| 是否已清退 | is_checked_out | 布尔 | 是 | 是否已完成清退 | true |
| 清退日期 | checkout_date | 日期时间 | 否 | 清退完成日期 | 2026-05-20 10:30:00 |
| 清退状态 | checkout_status | 文本 | 否 | completed/pending/not_started | completed |
| 备注 | remarks | 文本 | 否 | 备注信息 | 已完成清退 |

**数据量：** 约1000人/届

**对接方式1：API接口（推荐，已有）**
- 当前数据对接文档已详细说明
- 接口地址：`/api/dorm/checkout/status`
- 认证方式：API Key + IP白名单

**对接方式2：数据库直连（备选）**
```sql
-- 示例查询
SELECT 
    student_id,
    name,
    dorm_building,
    dorm_room,
    bed_number,
    is_checked_out,
    checkout_date,
    checkout_status,
    remarks
FROM dorm_checkout
WHERE graduation_year = 2024;
```

**对接方式3：CSV文件导入（降级）**
- 文件名：`dorm_checkout_YYYYMMDD.csv`
- 字符编码：UTF-8
- 模板文件：`docs/templates/宿舍清退数据模板.csv`（已有）

---

### 2.3 辅导员基本信息

**用途：**
- 创建辅导员账号（用于登录系统）
- 分配审批权限
- 作为一级审批人

**必需字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 工号 | employee_id | 文本 | 是 | 辅导员唯一标识 | T2020001 |
| 姓名 | name | 文本 | 是 | 辅导员姓名 | 李老师 |
| 手机号 | phone | 文本 | 是 | 用于通知 | 13900139000 |
| 邮箱 | email | 文本 | 否 | 用于通知 | teacher@example.com |
| 院系 | department | 文本 | 否 | 所属院系 | 计算机学院 |
| 是否在职 | is_active | 布尔 | 是 | 是否在职 | true |

**数据量：** 约50人

**对接方式1：数据库直连（推荐）**
```sql
-- 示例查询（假设宿管系统有辅导员表）
SELECT 
    employee_id,
    name,
    phone,
    email,
    department,
    is_active
FROM counselors
WHERE is_active = true;
```

**对接方式2：API接口（备选）**
```
GET /api/counselors?is_active=true
```

**对接方式3：CSV文件导入（降级）**
- 文件名：`counselors_YYYYMMDD.csv`
- 字符编码：UTF-8
- 模板文件：`docs/templates/辅导员基本信息导入模板.csv`

---

### 2.4 班级-辅导员对应关系

**用途：**
- 自动分配审批人（学生提交申请时，根据班级自动找到对应辅导员）
- 辅导员权限边界（辅导员只能查看和审批负责班级的学生）
- 待办通知准确发送
- 审批统计按班级、辅导员追踪

**重要性：** 🔴 最高优先级缺口
- 如果没有这个数据，系统无法自动分配审批人
- 需要手动配置每个学生的辅导员（~1000人/届）
- 上线前必须达到100%覆盖率

**必需字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2020-01 |
| 班级名称 | class_name | 文本 | 是 | 班级名称（用于展示） | 计算机2020级1班 |
| 辅导员工号 | counselor_employee_id | 文本 | 是 | 辅导员工号 | T2020001 |
| 辅导员姓名 | counselor_name | 文本 | 否 | 辅导员姓名（用于展示） | 李老师 |
| 院系 | department | 文本 | 否 | 所属院系 | 计算机学院 |
| 年级 | grade | 整数 | 否 | 年级 | 2020 |
| 生效学期 | effective_term | 文本 | 否 | 生效学期 | 2023-2024-2 |

**数据量：** 约50条映射关系

**对接方式1：数据库直连（推荐）**
```sql
-- 示例查询
SELECT 
    class_id,
    class_name,
    counselor_employee_id,
    counselor_name,
    department,
    grade,
    effective_term
FROM class_counselor_mapping
WHERE grade = 2020;
```

**对接方式2：API接口（备选）**
```
GET /api/class-counselor-mapping?grade=2020
```

**对接方式3：CSV文件导入（降级）**
- 文件名：`class_counselor_mapping_YYYYMMDD.csv`
- 字符编码：UTF-8
- 模板文件：`docs/templates/班级辅导员对应关系导入模板.csv`

**校验要求：**
- 导入后必须输出校验报告：
  - 未匹配班级数量
  - 未匹配辅导员数量
  - 重复映射数量
  - 无负责人的学生数量
- 上线前必须达到100%当届学生可解析到有效辅导员

---

## 三、P1数据源（可选）

### 3.1 学工部管理员信息

**用途：**
- 创建学工部管理员账号
- 终审备案权限

**数据量：** 约5人

**建议方式：** 手动创建
- 数量少，手动创建成本低
- 不建议做系统级数据对接

**如需导入，字段要求：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 工号 | employee_id | 文本 | 是 | 管理员唯一标识 | A2020001 |
| 姓名 | name | 文本 | 是 | 管理员姓名 | 王主任 |
| 手机号 | phone | 文本 | 是 | 用于通知 | 13700137000 |
| 邮箱 | email | 文本 | 否 | 用于通知 | admin@example.com |

---

## 四、对接方式详细说明

### 4.1 方式1：数据库直连（推荐）

**优点：**
- 实时性高
- 自动化程度高
- 无需开发API
- 支持复杂查询

**技术要求：**
- 提供数据库只读账号
- 支持的数据库类型：MySQL / SQL Server / Oracle / PostgreSQL
- 网络连通性：本系统服务器能访问宿管系统数据库

**安全措施：**
- 只读权限
- IP白名单
- 专用账号
- 定期更换密码

**配置信息（需提供）：**
```json
{
  "db_type": "mysql",
  "host": "dorm-db.example.com",
  "port": 3306,
  "database": "dorm_system",
  "username": "readonly_user",
  "password": "***",
  "charset": "utf8mb4"
}
```

---

### 4.2 方式2：API接口（备选）

**优点：**
- 安全性高（不暴露数据库）
- 可控性强
- 支持复杂业务逻辑

**缺点：**

exec
/bin/bash -lc "rtk sed -n '1,280p' docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 数据源需求共识文档审查结果

**审查时间：** 2026-05-27  
**审查对象：** `31-data-source-requirements-consensus.md`  
**参考材料：** `30-codex-data-source-review.md`、`25-class-bed-field-consensus.md`、`docs/用户设计说明书.md`、`docs/design/2026-05-27-system-design.md`、`docs/数据对接说明文档.md`、`docs/templates/*.csv`

---

## 一、总体结论

**结论：文档方向正确，P0 数据源基本完整；但不建议原样提交给用户。**

建议先做一轮小范围修订后再提交，主要原因是：

1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
2. 对接方式里对学生、辅导员、班级映射默认写“DB 优先”偏激进。首版更合理的路径是：账号与映射数据优先 CSV/Excel 批量导入，宿舍清退优先 API。
3. 宿舍清退字段与上一轮字段共识存在轻微不一致：`checkout_status` 在本文件中标为可选，但既有字段共识中 API 响应建议必填。
4. 缺少若干实施级关键问题，例如账号标识映射、终审管理员分配规则、同步覆盖策略、历史审批人不被后续映射变更自动改写等。

修订上述问题后，文档可以作为数据对接需求初稿提交。

---

## 二、数据源完整性审查

### 2.1 P0 数据源覆盖情况

当前 P0 数据源覆盖了系统运行所需的核心闭环：

| 数据源 | 审查结论 | 说明 |
|--------|----------|------|
| 学生基本信息 | 完整 | 支撑学生账号、身份识别、班级映射、毕业届别筛选。 |
| 宿舍清退数据 | 完整 | 支撑提交前置校验，是当前已明确需要自动校验的数据。 |
| 辅导员基本信息 | 完整 | 支撑辅导员账号和一级审批主体。 |
| 班级-辅导员对应关系 | 完整且必要 | 是自动分配 `counselor_id` 和权限边界的关键数据。 |
| 学工部管理员信息 | P1 合理 | 人数少，手动创建比外部对接更合理。 |

### 2.2 未遗漏的部分

图书馆清书状态、财务结清状态、独立学籍状态没有列为 P0 是合理的。当前用户设计和系统设计仍保留截图上传、人工审核和宿舍系统异常时人工降级的方案，因此这三类不应阻塞首版上线。

### 2.3 建议补充的“非数据源但上线必需项”

以下不是外部数据源，但应在文档中补充为实施前提或配置项：

1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
2. **离校批次配置。** 包括毕业届别、开放申请时间、允许计划离校日期范围。这些可由系统后台配置，不必来自外部系统。
3. **账号标识映射。** 当前系统设计中的 `users.student_id` 被用作唯一登录标识，但共识文档给辅导员和管理员使用 `employee_id`。需要明确导入时 `employee_id` 映射到哪个内部字段，或后续模型是否新增统一的 `external_id/employee_id`。

---

## 三、字段定义合理性审查

### 3.1 学生基本信息

字段整体合理，能支撑首版业务。`student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`is_graduating` 作为必填基本可接受。

建议调整：

1. `is_graduating` 建议改名或补充为 `eligible_for_leave` / `graduation_status`。  
   仅“是否毕业生”不足以表达延期毕业、结业、休学、退学、已毕业归档等异常状态。首版可以保留 `is_graduating`，但建议增加一个更直接的离校资格字段。

2. `graduation_year` 示例应与当前项目日期保持一致。  
   文档创建时间为 2026-05-27，但 SQL 示例使用 `graduation_year = 2024`。建议统一为 `2026` 或说明“示例年份按实际毕业届别替换”。

3. `phone` 是否可选需要结合微信绑定策略确认。  
   如果登录只依赖学号密码和微信 OAuth，手机号可选合理；如果要支持短信验证、密码找回或紧急联系，手机号应至少在导入模板中强烈建议提供。

### 3.2 宿舍清退数据

核心字段完整，但必填性需要和既有共识统一。

建议调整：

1. `checkout_status` 建议改为必填，且给出枚举：`completed`、`pending`、`not_started`、`unknown`。  
   既有字段共识已将 `checkout_status` 作为 API 响应必填字段，本文件标为可选会造成实现歧义。

2. `checkout_date` 应明确条件必填：当 `is_checked_out = true` 或 `checkout_status = completed` 时必填，未清退时允许为空。

3. `dorm_building`、`dorm_room`、`bed_number` 可选是可接受的，但应说明这些字段仅用于展示、核对和异常排查，业务判定不得依赖床位文本匹配。

4. 应补充 `source_updated_at`。  
   对 API 或 CSV 数据都建议记录外部系统数据更新时间，便于区分“未完成清退”和“数据过期/未同步”。

### 3.3 辅导员基本信息

字段基本可用，但有两个风险点：

1. `phone` 标为必填偏强。  
   如果通知主要走微信，手机号可作为推荐字段而非硬性 P0。若学校确实要求短信/电话通知，则保留必填也合理。建议在文档中说明依据。

2. 缺少账号生命周期字段说明。  
   `is_active` 已有，但应补充离职、调岗、停用后如何处理其名下未完成审批，以及是否允许历史审批记录继续引用已停用账号。

### 3.4 班级-辅导员对应关系

该章节是文档中最关键、也最合理的部分。`class_id` 作为必填是正确的，避免只靠班级名称匹配。

建议补充：

1. **一班多辅导员场景。** 首版可以要求一个主辅导员，但应明确是否允许同一班级多名辅导员、代理辅导员或临时改派。
2. **有效期字段。** `effective_term` 可选略弱，建议至少支持 `effective_start_date` / `effective_end_date` 或说明同一届首版只按当前有效映射导入。
3. **历史一致性规则。** 班级映射变更后，不应自动改写已提交申请中的 `counselor_id`；已提交申请如需改派，应由管理员显式操作并记录审计日志。

### 3.5 学工部管理员信息

手动创建是合理方案。建议补充：

1. 管理员账号创建、停用、重置密码、角色授权和审计要求。
2. 默认终审人或终审组配置规则。
3. 管理员离岗后未完成审批任务如何转交。

---

## 四、对接方式可行性审查

### 4.1 当前优先级评价

| 数据源 | 当前写法 | 审查意见 |
|--------|----------|----------|
| 学生基本信息 | DB 优先 / API 备选 / CSV 降级 | 建议改为 CSV/Excel 首版优先，DB/API 作为条件成熟后的增强。 |
| 宿舍清退数据 | API 优先 / DB 备选 / CSV 降级 | 合理。提交前置校验对实时性要求更高，API 价值最大。 |
| 辅导员基本信息 | DB 优先 / API 备选 / CSV 降级 | 建议改为 CSV/Excel 或手动批量维护优先，人数少且变化低频。 |
| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
| 学工部管理员信息 | 手动创建 | 合理。 |

### 4.2 技术要求清晰度

DB、API、CSV 三种方式的技术要求整体清晰，但建议补充：

1. DB 直连只建议在同一内网、安全边界清晰、能提供只读视图的情况下使用。
2. DB 直连不要直接暴露生产业务表，建议由数据源系统提供只读视图或同步库。
3. API 需补充分页、增量同步、错误码、限流、重试、幂等和测试环境要求。
4. CSV 需补充导入覆盖策略：全量覆盖、增量更新、软删除/停用、重复数据处理、失败回滚。

### 4.3 安全措施充分性

已有只读账号、IP 白名单、专用账号、定期换密等措施，方向正确。建议增加：

1. 密钥、数据库密码必须加密存储，不得写入代码仓库或明文配置。
2. CSV 通过 SFTP 或后台上传时应限制权限，并记录上传人、文件哈希、导入批次和导入结果。
3. 数据最小化：不采集身份证号、家庭住址、欠费明细、图书借阅明细等高敏字段。
4. 外部系统异常时要区分“未完成”“查询失败”“数据过期”“人工证明待审”，不能统一判定为不通过。

---

## 五、数据量估算审查

### 5.1 当前估算是否合理

| 数据项 | 当前估算 | 审查结论 |
|--------|----------|----------|
| 学生 | 约 1000 人/届 | 合理，但需注明是“当届毕业生”。用户设计说明书中另有“学生用户 10,000 人”的容量指标，二者不冲突。 |
| 辅导员 | 约 50 人 | 合理。 |
| 班级映射 | 约 50 条 | 基本合理，但取决于班级粒度和是否存在多辅导员/代理关系。 |
| 学工部管理员 | 约 5 人 | 合理。 |

### 5.2 建议补充说明

1. 若系统只导入当届毕业生，1000 人规模合理。
2. 若系统保留多届历史或提前导入低年级学生，容量应按 10,000 学生账号设计。
3. 班级映射数量不应只按班级数估算；若一个班有主辅导员、代理辅导员、历史有效期，则映射记录可能多于 50 条。

---

## 六、待反馈问题审查

当前问题覆盖了数据库、API、CSV 和数据范围，基本可用，但建议扩展为面向多方的数据确认清单。

### 6.1 建议修改提问对象

将“请宿管系统方反馈以下问题”改为：

> 请教务系统、人事系统、学工部数据负责人、宿管系统方分别确认其可提供的数据范围、字段、对接方式和联系人。

原因：学生、辅导员、班级映射通常不是宿管系统的权责数据。

### 6.2 建议新增问题

1. 学生数据来源是否为教务系统？是否能只提供当届毕业生名单？
2. 是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
3. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
4. 辅导员工号是否全校唯一？是否与统一身份认证、人事系统工号一致？
5. 是否存在一个班级多个辅导员、代理辅导员、临时负责人或辅导员调岗场景？
6. 班级-辅导员映射变更频率如何？是否能提供当前有效映射和历史有效期？
7. 学工部终审人是固定个人、固定角色组、轮值还是人工分配？
8. 各数据源能否提供测试数据、测试环境和字段字典？
9. CSV 导入时是否采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
10. 外部系统不可用、数据延迟或查询失败时，业务上允许怎样的人工降级？
11. 是否有统一身份认证或微信绑定前置要求？是否需要导入手机号/邮箱用于找回密码或二次验证？
12. 数据提供方能否承诺导出频率、数据更新时间、联系人和故障响应时间？

---

## 七、实施建议审查

### 7.1 推荐方案

共识文档中的推荐方案整体合理，但“如果宿管系统数据库包含所有数据”这个前提不够现实。学生、辅导员、班级映射不应假设都在宿管系统数据库中。

建议改为：

1. 宿舍清退：优先使用宿管系统 API；若不可用，使用每日 CSV 导入；异常时保留人工证明。
2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
3. 辅导员信息：首版优先 CSV/Excel 或后台批量维护；若有统一身份或人事 API，再对接。
4. 班级-辅导员映射：首版优先 CSV/Excel 强校验，上线前必须 100% 覆盖当届学生。
5. 学工部管理员：手动创建，同时配置默认终审人或终审组。

### 7.2 最小可行方案

共识文档的最小可行方案合理，可以保留。建议补充两个验收条件：

1. 当届所有可申请学生必须能解析到有效辅导员。
2. 提交申请时必须能解析到有效终审管理员或终审组。

### 7.3 更好的实施路径

建议按以下顺序实施：

1. 先确认数据权责方和联系人，不把所有问题都压给宿管系统。
2. 先落地三份基础 CSV/Excel 模板：学生、辅导员、班级-辅导员映射。
3. 实现导入校验报告，重点校验学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射。
4. 再对接宿舍清退 API，并把 API 失败、超时、数据过期纳入统一降级处理。
5. 上线前冻结当届数据批次，完成一次全量导入演练和异常清单清零。
6. 上线后根据数据变更频率决定是否将学生、辅导员、映射数据升级为 API 或 DB 同步。

---

## 八、具体修改建议

### 8.1 文档目的

建议将：

> 明确毕业离校系统所需的数据源，提交给宿管系统方反馈

修改为：

> 明确毕业离校系统所需的数据源，提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人反馈。

### 8.2 数据源概述表

建议将学生、辅导员、班级映射的对接方式调整为：

| 数据源 | 建议对接方式 |
|--------|--------------|
| 学生基本信息 | CSV/Excel 首版优先 / API 或 DB 视图增强 |
| 辅导员基本信息 | CSV/Excel 或后台批量维护首版优先 / 人事或统一身份 API 增强 |
| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
| 宿舍清退数据 | API 优先 / DB 只读视图备选 / CSV 降级 |

### 8.3 学生字段

建议在学生基本信息中增加：

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 离校申请资格 | eligible_for_leave | 布尔 | 建议是 | 是否允许提交本批次离校申请 | true |
| 学籍/毕业状态 | graduation_status | 文本 | 否 | graduating/delayed/graduated/suspended/withdrawn | graduating |

如不新增字段，至少应说明 `is_graduating=true` 即表示具备本批次离校申请资格。

### 8.4 宿舍清退字段

建议将：

| 字段 | 当前 | 建议 |
|------|------|------|
| checkout_status | 可选 | 必填，枚举：completed/pending/not_started/unknown |
| checkout_date | 可选 | 条件必填：completed 时必填 |
| source_updated_at | 未列出 | 建议新增，记录外部系统数据更新时间 |

### 8.5 辅导员字段

建议补充说明：

1. `employee_id` 必须全校唯一，并与班级映射中的 `counselor_employee_id` 完全一致。
2. `phone` 是否必填取决于通知和找回密码方案；如果不依赖短信，可改为建议字段。
3. `is_active=false` 时不再分配新申请，但历史审批记录仍保留。


exec
/bin/bash -lc "rtk sed -n '321,760p' docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
- 需要开发API接口
- 维护成本较高

**技术要求：**
- REST API
- JSON格式
- 认证方式：API Key + IP白名单
- 响应时间：< 500ms（P95）

**接口规范：**
- 参考当前数据对接文档中的宿舍清退状态查询接口
- 需要为每个数据源提供对应的查询接口

---

### 4.3 方式3：CSV文件导入（降级）

**适用场景：**
- 无法提供数据库访问权限
- 无法开发API接口
- 临时应急方案

**优点：**
- 实施简单
- 无需技术对接

**缺点：**
- 数据有延迟
- 需要人工操作
- 容易出错

**操作流程：**
1. 宿管系统方按模板导出CSV文件
2. 通过SFTP上传或管理后台上传
3. 本系统导入并校验
4. 生成导入报告

**文件要求：**
- 字符编码：UTF-8
- 文件格式：CSV
- 导出频率：每日一次（建议凌晨1点）
- 文件命名：`{数据源}_{YYYYMMDD}.csv`

---

## 五、数据质量要求

### 5.1 数据完整性
- 必填字段不能为空
- 学号、工号必须唯一
- 日期格式必须正确

### 5.2 数据准确性
- 学号必须与实际一致
- 姓名必须与实际一致
- 清退状态必须真实准确
- 班级-辅导员映射必须准确

### 5.3 数据时效性
- 数据库直连：实时
- API接口：实时
- CSV导入：建议每日更新，延迟不超过24小时

### 5.4 数据一致性
- 学生表中的class_id必须在班级-辅导员映射表中存在
- 班级-辅导员映射表中的counselor_employee_id必须在辅导员表中存在

---

## 六、实施建议

### 6.1 推荐方案

**如果宿管系统数据库包含所有数据：**
1. 使用数据库直连方式
2. 提供只读账号
3. 本系统定时同步数据

**如果宿管系统数据库只包含部分数据：**
1. 宿舍清退数据：使用现有API接口
2. 学生基本信息：数据库直连或CSV导入
3. 辅导员信息：CSV导入
4. 班级-辅导员映射：CSV导入

### 6.2 最小可行方案

**首版上线最低要求：**
1. 宿舍清退数据：API接口（已有）
2. 学生基本信息：CSV导入
3. 辅导员基本信息：CSV导入
4. 班级-辅导员对应关系：CSV导入（必须100%覆盖）
5. 学工部管理员：手动创建（~5人）

---

## 七、待反馈问题

请宿管系统方反馈以下问题：

### 7.1 数据库情况
1. 宿管系统使用的数据库类型？（MySQL / SQL Server / Oracle / PostgreSQL / 其他）
2. 数据库中是否包含以下数据表？
   - [ ] 学生基本信息表
   - [ ] 宿舍清退数据表
   - [ ] 辅导员信息表
   - [ ] 班级-辅导员对应关系表
3. 是否可以提供数据库只读账号？
4. 如果可以，能否提供表结构说明？

### 7.2 API接口情况
1. 除了宿舍清退状态查询接口，是否可以提供其他数据查询接口？
2. 如果可以，开发周期大概多久？

### 7.3 CSV导入情况
1. 如果使用CSV导入，是否可以按模板定期导出数据？
2. 导出频率：每日 / 每周 / 按需？
3. 传输方式：SFTP / 共享文件夹 / 手动上传？

### 7.4 数据范围
1. 学生数据是否只包含当届毕业生，还是包含全校学生？
2. 辅导员数据是否只包含负责毕业班的辅导员，还是全部辅导员？
3. 班级-辅导员对应关系是否稳定，还是会频繁变动？

---

## 八、下一步行动

1. **宿管系统方**：反馈上述问题，提供数据库/API/CSV的可行性
2. **本系统方**：根据反馈，确定最终对接方案
3. **双方**：联调测试，确保数据准确性和完整性
4. **本系统方**：更新数据对接说明文档，提供CSV模板文件

---

**文档结束**

exec
/bin/bash -lc "rtk rg -n \"employee_id|student_id|class_counselor|counselor_id|admin_id|users|User\" docs src app server prisma database migrations -g '"'!node_modules'"'" in /home/caohui/projects/graduation-leave-system
 exited 2 in 0ms:
rg: src: No such file or directory (os error 2)
rg: app: No such file or directory (os error 2)
rg: server: No such file or directory (os error 2)
rg: prisma: No such file or directory (os error 2)
rg: database: No such file or directory (os error 2)
rg: migrations: No such file or directory (os error 2)
docs/superpowers/plans/2026-05-27-implementation-plan.md:225:   - 定义User模型（继承AbstractUser）
docs/superpowers/plans/2026-05-27-implementation-plan.md:226:   - 添加字段：student_id、role、wechat_openid等
docs/design/2026-05-27-system-design.md:246:1. users - 用户表
docs/design/2026-05-27-system-design.md:255:### 2.2 用户表（users）
docs/design/2026-05-27-system-design.md:260:CREATE TABLE users (
docs/design/2026-05-27-system-design.md:262:    student_id VARCHAR(20) UNIQUE NOT NULL COMMENT '学号',
docs/design/2026-05-27-system-design.md:288:    INDEX idx_student_id (student_id),
docs/design/2026-05-27-system-design.md:310:    student_id BIGINT NOT NULL COMMENT '学生ID',
docs/design/2026-05-27-system-design.md:313:    counselor_id BIGINT COMMENT '辅导员ID',
docs/design/2026-05-27-system-design.md:314:    admin_id BIGINT COMMENT '学工部管理员ID',
docs/design/2026-05-27-system-design.md:335:    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:336:    FOREIGN KEY (counselor_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:337:    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:338:    FOREIGN KEY (current_approver_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:340:    INDEX idx_student_id (student_id),
docs/design/2026-05-27-system-design.md:341:    INDEX idx_counselor_id (counselor_id),
docs/design/2026-05-27-system-design.md:342:    INDEX idx_admin_id (admin_id),
docs/design/2026-05-27-system-design.md:347:    INDEX idx_student_status (student_id, status, created_at),
docs/design/2026-05-27-system-design.md:378:    FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:444:    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
docs/design/2026-05-27-system-design.md:480:    FOREIGN KEY (updated_by) REFERENCES users(id)
docs/design/2026-05-27-system-design.md:527:    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:572:    FOREIGN KEY (changed_by) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:591:users (用户表)
docs/design/2026-05-27-system-design.md:597:  ├─N:1─→ users (申请人)
docs/design/2026-05-27-system-design.md:598:  ├─N:1─→ users (辅导员)
docs/design/2026-05-27-system-design.md:599:  ├─N:1─→ users (学工部管理员)
docs/design/2026-05-27-system-design.md:600:  ├─N:1─→ users (当前审批人)
docs/design/2026-05-27-system-design.md:609:  └─N:1─→ users (审批人)
docs/design/2026-05-27-system-design.md:615:  ├─N:1─→ users (接收人)
docs/design/2026-05-27-system-design.md:619:  └─N:1─→ users (操作人)
docs/design/2026-05-27-system-design.md:622:  └─N:1─→ users (更新人)
docs/design/2026-05-27-system-design.md:683:  "student_id": "2020001",
docs/design/2026-05-27-system-design.md:697:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:724:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:762:  "student_id": "2020001",
docs/design/2026-05-27-system-design.md:775:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:797:  "student_id": "2020001",
docs/design/2026-05-27-system-design.md:811:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:913:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:1288:    "student_id": "2020001",
docs/design/2026-05-27-system-design.md:1383:        return obj.student_id == request.user.id
docs/design/2026-05-27-system-design.md:1427:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
docs/design/2026-05-27-system-design.md:1428:  - 设置当前审批人：current_approver_id = counselor_id
docs/design/2026-05-27-system-design.md:1443:    - 更新当前审批人：current_approver_id = admin_id
docs/design/2026-05-27-system-design.md:1627:  student_id: 2020001
docs/design/2026-05-27-system-design.md:1633:    "student_id": "2020001",
docs/design/2026-05-27-system-design.md:1657:    def get_checkout_status(self, student_id):
docs/design/2026-05-27-system-design.md:1659:            f'{self.base_url}/api/students/{student_id}/checkout',
docs/design/2026-05-27-system-design.md:1679:    def verify_clearance(self, student_id):
docs/design/2026-05-27-system-design.md:1683:                params={"student_id": student_id},
docs/design/2026-05-27-system-design.md:1727:def verify_dorm_clearance(student_id):
docs/design/2026-05-27-system-design.md:1729:    return plugin.verify_clearance(student_id)
docs/design/2026-05-27-system-design.md:1982:def bind_wechat_to_account(student_id, wechat_openid, password):
docs/design/2026-05-27-system-design.md:1984:    user = User.objects.filter(student_id=student_id).first()
docs/design/2026-05-27-system-design.md:1990:            request_data={'student_id': student_id}
docs/design/2026-05-27-system-design.md:2072:        'rest_framework.throttling.UserRateThrottle',
docs/design/2026-05-27-system-design.md:2083:from rest_framework.throttling import UserRateThrottle
docs/design/2026-05-27-system-design.md:2085:class LoginRateThrottle(UserRateThrottle):
docs/design/2026-05-27-system-design.md:2088:class UploadRateThrottle(UserRateThrottle):
docs/design/2026-05-27-system-design.md:2337:-- users表索引
docs/design/2026-05-27-system-design.md:2338:CREATE INDEX idx_student_id ON users(student_id);
docs/design/2026-05-27-system-design.md:2339:CREATE INDEX idx_role ON users(role);
docs/design/2026-05-27-system-design.md:2340:CREATE INDEX idx_wechat_openid ON users(wechat_openid);
docs/design/2026-05-27-system-design.md:2341:CREATE INDEX idx_account_locked ON users(account_locked);
docs/design/2026-05-27-system-design.md:2344:CREATE INDEX idx_student_id ON applications(student_id);
docs/design/2026-05-27-system-design.md:2345:CREATE INDEX idx_counselor_id ON applications(counselor_id);
docs/design/2026-05-27-system-design.md:2346:CREATE INDEX idx_admin_id ON applications(admin_id);
docs/design/2026-05-27-system-design.md:2353:CREATE INDEX idx_student_status ON applications(student_id, status, created_at);
docs/design/2026-05-27-system-design.md:2464:    cache.delete(f'student:{app.student_id}:applications')
docs/design/2026-05-27-system-design.md:2593:    result = approve_application(app_id, counselor_id, 'approve')
docs/design/2026-05-27-system-design.md:2604:    response = bind_wechat(student_id='2020001', openid='oXXX', password='wrong')
docs/design/2026-05-27-system-design.md:2630:    bind_wechat(student_id='2020001', openid='oXXX', password='pass')
docs/design/2026-05-27-system-design.md:2638:    r1 = bind_wechat(student_id='9999999', openid='oXXX', password='pass')
docs/design/2026-05-27-system-design.md:2640:    r2 = bind_wechat(student_id='2020001', openid='oXXX', password='wrong')
docs/design/2026-05-27-system-design.md:2642:    r3 = bind_wechat(student_id='2020002', openid='oXXX', password='pass')
docs/design/2026-05-27-system-design.md:2678:    approve_application(app_id, counselor_id, 'approve')
docs/design/2026-05-27-system-design.md:2730:from locust import HttpUser, task, between
docs/design/2026-05-27-system-design.md:2732:class GraduationLeaveUser(HttpUser):
docs/数据对接说明文档.md:67:| student_id | String | 是 | 学号 | "2020010101" |
docs/数据对接说明文档.md:72:GET /api/dorm/checkout/status?student_id=2020010101&name=张三
docs/数据对接说明文档.md:85:  "student_id": "2020010101",
docs/数据对接说明文档.md:104:| student_id | String | 学号 | "2020010101" |
docs/数据对接说明文档.md:121:    "student_id": "2020010101",
docs/数据对接说明文档.md:141:    "student_id": "2020010101",
docs/数据对接说明文档.md:200:curl -X GET "http://dorm-test.example.com/api/dorm/checkout/status?student_id=2020010101" \
docs/数据对接说明文档.md:222:| 学号 | student_id | 文本 | 是 | 学生学号 | 2020010101 |
docs/数据对接说明文档.md:335:| 参数缺失 | 不传student_id | 返回错误码1002 |
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:111:- users表已有class_name字段，API响应中的class_name来自宿舍系统
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:112:- 建议：不需要在applications表存储，直接从users表读取即可
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:83:   - 将添加：提交时设置`counselor_id`、`admin_id`
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:103:- 添加完整的字段更新逻辑（counselor_id、admin_id、current_approver_id、version）
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:39:CREATE TABLE users (
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:46:CREATE TABLE users (
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:51:COMMENT ON TABLE users IS '用户表';
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:52:COMMENT ON COLUMN users.name IS '姓名';
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:82:FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE SET NULL
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:86:FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE PROTECT
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:264:def bind_wechat_to_account(student_id, wechat_openid, password):
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:266:    user = User.objects.filter(student_id=student_id).first()
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:272:            request_data={'student_id': student_id}
docs/discussions/codex-review-2026-05-27/21-final-consensus.md:351:CREATE INDEX idx_student_id ON applications(student_id);
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:76:**理由：** `student_id + name` 已足够唯一标识，避免身份证号在系统间传输。
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:18:    user = models.ForeignKey(User, on_delete=models.PROTECT)  # 改为必需
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:61:    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='applications')
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:65:        User, 
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:72:        User, 
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:82:        User, 
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:106:            models.Index(fields=['student_id']),
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:107:            models.Index(fields=['counselor_id']),
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:108:            models.Index(fields=['admin_id']),
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:131:### 5. users表缺少认证安全字段 - **完全同意**
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:137:class User(AbstractUser):
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:138:    student_id = models.CharField(max_length=20, unique=True)
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:167:            models.Index(fields=['student_id']),
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:197:                student_id=self.student_id,
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:218:ON applications(student_id) 
docs/PROJECT-SUMMARY.md:181:1. **users** - 用户表
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:68:    def get_checkout_status(self, student_id):
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:70:            f'{self.base_url}/api/students/{student_id}/checkout',
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:40:  "student_id": "2020010101",
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:87:    "student_id": "2020001",
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:119:  - 缺点：users表中已有class_name字段，可能冗余
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:133:student_id → name → class_name → dorm_building → dorm_room → bed_number → is_checked_out → ...
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:137:- 学生信息：student_id、name、class_name
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:146:- users表已有class_name字段
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:174:**问题：** class_name在users表和API响应中都有，是否冗余？
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:177:- users表的class_name：学生的实际班级（来自学生信息系统）
docs/discussions/codex-review-2026-05-27/04-database-review.md:24:- users表有`is_deleted`字段（软删除）
docs/discussions/codex-review-2026-05-27/04-database-review.md:25:- applications表有`student_id`外键指向users
docs/discussions/codex-review-2026-05-27/04-database-review.md:31:2. 查询复杂：每个查询需要`AND users.is_deleted=FALSE`
docs/discussions/codex-review-2026-05-27/04-database-review.md:39:        User,
docs/discussions/codex-review-2026-05-27/04-database-review.md:47:CREATE TABLE users_archive (
docs/discussions/codex-review-2026-05-27/04-database-review.md:48:    -- 与users相同结构
docs/discussions/codex-review-2026-05-27/04-database-review.md:94:CREATE INDEX idx_student_status ON applications(student_id, status, created_at);
docs/discussions/codex-review-2026-05-27/04-database-review.md:153:    FOREIGN KEY (user_id) REFERENCES users(id),
docs/discussions/codex-review-2026-05-27/04-database-review.md:164:- 无`counselor_id`（只有`current_approver_id`会变）
docs/discussions/codex-review-2026-05-27/04-database-review.md:165:- 无`admin_id`（谁做的最终审批？）
docs/discussions/codex-review-2026-05-27/04-database-review.md:180:    counselor_id BIGINT COMMENT '辅导员ID',
docs/discussions/codex-review-2026-05-27/04-database-review.md:181:    admin_id BIGINT COMMENT '学工部管理员ID',
docs/discussions/codex-review-2026-05-27/04-database-review.md:190:    FOREIGN KEY (counselor_id) REFERENCES users(id),
docs/discussions/codex-review-2026-05-27/04-database-review.md:191:    FOREIGN KEY (admin_id) REFERENCES users(id),
docs/discussions/codex-review-2026-05-27/04-database-review.md:192:    INDEX idx_counselor_id (counselor_id),
docs/discussions/codex-review-2026-05-27/04-database-review.md:193:    INDEX idx_admin_id (admin_id)
docs/discussions/codex-review-2026-05-27/04-database-review.md:197:### 5. users表缺少认证安全字段
docs/discussions/codex-review-2026-05-27/04-database-review.md:210:CREATE TABLE users (
docs/discussions/codex-review-2026-05-27/04-database-review.md:243:ON applications(student_id) 
docs/discussions/codex-review-2026-05-27/04-database-review.md:253:                student_id=self.student_id,
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:72:- users表已有class_name字段
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:73:- API响应中的class_name直接从users表读取
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:113:| student_id | String | 学号 | 是 | "2020010101" |
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:179:    result = dorm_api.check_status(student_id, timeout=2)
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:182:    enqueue_retry_task(student_id)
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:187:def retry_dorm_check(student_id):
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:188:    result = dorm_api.check_status(student_id)
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:40:- ✅ 添加counselor_id, admin_id, version, certificate_url, certificate_generated_at
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:44:**5. users表安全字段**
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:14:1. **班级-辅导员对应关系应明确列为 P0。** 这是自动分配审批人的核心数据。没有它，系统提交申请时无法稳定设置 `counselor_id` 和 `current_approver_id`，只能退化为人工逐个配置或人工改派。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:46:| 学生基本信息 | CSV/Excel 批量导入 | 教务系统 API | 首版按毕业届别导入更容易落地。字段建议包括 `student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:47:| 辅导员基本信息 | CSV/Excel 批量导入 | 人事系统 API 或手动创建 | 约 50 人规模下，批量导入足够。字段建议包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:48:| 班级-辅导员对应关系 | CSV/Excel 批量导入并强校验 | 教务系统 API | 必须优先支持。建议用 `class_id + counselor_employee_id + effective_term` 表达关系，不要只靠 `class_name`。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无审批人的学生数。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:51:| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 后续对接时只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，不要引入借阅明细。 |
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:69:理由是辅导员规模约 50 人，变化频率低，API 改造投入可能高于收益。但数据结构必须标准化，尤其是 `employee_id` 要能被班级-辅导员映射引用。若学校已有成熟 HR API 或统一身份平台，可在后续升级为 API 同步。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:108:5. **审批人变更后的历史一致性。** 已提交申请中的 `counselor_id` 应保持历史一致，不应因后续班级映射变更自动改写。若需改派，应由管理员显式操作并记录审计日志。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:112:7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:130:3. **定义辅导员基本信息导入模板。** 先确保 counselor 账号存在，且 `employee_id` 可被映射数据引用。
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:151:2. 新增“辅导员基本信息导入”章节，明确 `employee_id`、联系方式和账号状态。
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:95:    existing_user = User.objects.select_for_update().filter(
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:96:        student_id=student_id
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:127:class User(models.Model):
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:134:        User,
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:146:Index(fields=['student_id', 'status', 'created_at'])
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:175:- counselor_id BIGINT（固定辅导员ID）
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:176:- admin_id BIGINT（固定学工部管理员ID）
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:181:### 3.5 users表新增安全字段
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:206:            student_id=self.student_id,
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:246:    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:255:student = models.ForeignKey(User, on_delete=models.PROTECT)
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:256:counselor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:257:current_approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:162:- 使用 Django `AbstractUser`/`AbstractBaseUser` 的 `password` 字段
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:180:示例位置包括 `docs/design/2026-05-27-system-design.md:258` 起的 users 表，以及后续所有核心表。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:207:- `idx_users_student_id`
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:214:users 表对 `student_id`、`wechat_openid` 使用全局唯一。配合 `is_deleted` 软删除后，已删除用户仍会占用学号和 openid。
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:219:CREATE UNIQUE INDEX uniq_users_active_student_id
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:220:ON users(student_id)
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:51:if existing_user := User.objects.filter(student_id=student_id).first():
docs/discussions/codex-review-2026-05-27/01-architecture-review.md:88:        'rest_framework.throttling.UserRateThrottle'
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:33:1. 攻击者用微信注册，使用受害者的student_id
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:67:**问题：** 代码泄露student_id是否存在：
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:68:- "该学号已绑定其他微信账号" → student_id存在
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:69:- "该学号已注册，请输入密码" → student_id存在但无微信
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:70:- 创建新用户 → student_id不存在
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:76:if existing_user := User.objects.filter(student_id=student_id).first():
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:87:**问题：** 两个请求使用相同student_id + 不同openid可能同时通过检查，然后都执行绑定。
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:94:    existing_user = User.objects.select_for_update().filter(
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:95:        student_id=student_id
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:72:    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:169:4. ✅ applications表添加字段（counselor_id, admin_id, version, certificate_url）
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:170:5. ✅ users表添加认证安全字段
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:101:1. `student_id + name` 已足够唯一标识学生
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:35:| 班级-辅导员对应关系 | 完整且必要 | 是自动分配 `counselor_id` 和权限边界的关键数据。 |
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:46:1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:48:3. **账号标识映射。** 当前系统设计中的 `users.student_id` 被用作唯一登录标识，但共识文档给辅导员和管理员使用 `employee_id`。需要明确导入时 `employee_id` 映射到哪个内部字段，或后续模型是否新增统一的 `external_id/employee_id`。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:56:字段整体合理，能支撑首版业务。`student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`is_graduating` 作为必填基本可接受。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:103:3. **历史一致性规则。** 班级映射变更后，不应自动改写已提交申请中的 `counselor_id`；已提交申请如需改派，应由管理员显式操作并记录审计日志。
docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:277:1. `employee_id` 必须全校唯一，并与班级映射中的 `counselor_employee_id` 完全一致。
docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:97:不要在宿舍清退接口中使用 `id_card`，用 `student_id + name` 足够。
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:23:根据系统设计文档（`users`表），系统有3个角色：
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:45:- 学号（student_id）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:71:- 学号（student_id）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:93:- 工号（employee_id）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:118:- 辅导员工号（counselor_employee_id）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:143:- 工号（employee_id）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:172:- 学号（student_id）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:198:- 学号（student_id）
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:225:- 学号（student_id）
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:68:    "student_id": "2020001",
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:84:    "student_id": "2020001",
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:113:| student_id | String | 学号 | 是 | "2020010101" |
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:134:- **理由：** users表已有，避免冗余
docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:61:- 添加字段更新逻辑（counselor_id、admin_id、current_approver_id、version）
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:17:- 每个查询需要`AND users.is_deleted=FALSE` ✓
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:30:class User(models.Model):
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:48:        User,
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:68:student = models.ForeignKey(User, on_delete=models.PROTECT)  # 阻止删除
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:69:counselor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # 允许为空
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:70:current_approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:89:            models.Index(fields=['student_id', 'status', 'created_at'], 
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:141:- `idx_student_status` (student_id, status, created_at)
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:157:   - `idx_student_id` (学生查看自己申请)
docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:205:部分表有`is_deleted`字段（users, applications, attachments），部分表没有（approvals, notifications）。不一致的设计增加理解成本。
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:131:**问题：** 学生提交申请时，系统如何确定 `admin_id`（终审管理员）？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:151:**问题：** 辅导员和管理员使用 `employee_id`，但系统数据库模型中如何存储和映射？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:156:- `users` 表有 `student_id` 字段（学生学号）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:163:| 复用 `student_id` 字段存储 `employee_id` | 不需要改表结构 | 字段名语义不清 | ❌ |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:164:| 新增 `employee_id` 字段 | 语义清晰，扩展性好 | 需要修改表结构 | ✅ |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:168:1. `users` 表增加 `employee_id` 字段（可空）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:169:2. 学生账号：`student_id` 必填，`employee_id` 为空
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:170:3. 辅导员/管理员账号：`employee_id` 必填，`student_id` 为空
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:174:- 学生CSV：`student_id` → `users.student_id`
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:175:- 辅导员CSV：`employee_id` → `users.employee_id`
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:176:- 班级映射CSV：`counselor_employee_id` → 查询 `users` 表中 `employee_id` 匹配的记录
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:182:**问题：** 班级-辅导员映射变更后，已提交申请中的 `counselor_id` 是否自动改写？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:208:| 申请提交时 | 根据当前班级-辅导员映射确定 `counselor_id` |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:209:| 映射变更后，已提交申请 | `counselor_id` **不变**，保持原审批人 |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:210:| 映射变更后，新提交申请 | 使用新映射确定 `counselor_id` |
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:214:- `applications` 表的 `counselor_id` 是快照字段，不关联外键级联更新
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:253:3. 申请提交时使用主辅导员作为 `counselor_id`
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:382:5. 辅导员工号（`employee_id`）是否全校唯一？是否与统一身份认证、人事系统工号一致？
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:458:4. 补充账号标识映射方案（新增 `employee_id` 字段）
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:491:- 补充说明：`employee_id` 必须全校唯一
docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:542:2. **账号标识映射方案：** 我们提出新增 `employee_id` 字段的方案。Codex是否认同这个方案？是否有更好的替代方案？
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:83:   - `counselor_id`
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:84:   - `admin_id`
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:42:| 学号 | student_id | 文本 | 是 | 学生唯一标识 | 2020010101 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:65:    student_id,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:103:| 学号 | student_id | 文本 | 是 | 学生学号 | 2020010101 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:124:    student_id,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:155:| 工号 | employee_id | 文本 | 是 | 辅导员唯一标识 | T2020001 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:168:    employee_id,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:209:| 辅导员工号 | counselor_employee_id | 文本 | 是 | 辅导员工号 | T2020001 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:223:    counselor_employee_id,
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:228:FROM class_counselor_mapping
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:238:- 文件名：`class_counselor_mapping_YYYYMMDD.csv`
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:270:| 工号 | employee_id | 文本 | 是 | 管理员唯一标识 | A2020001 |
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:386:- 班级-辅导员映射表中的counselor_employee_id必须在辅导员表中存在
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:76:        active_users = User.objects.filter(is_active=True)[:100]
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:77:        for user in active_users:
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:208:class StudentUser(HttpUser):
docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:224:class CounselorUser(HttpUser):
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:80:    student_id = request.data['student_id']
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:83:    if user := User.objects.filter(wechat_openid=openid).first():
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:87:    if existing_user := User.objects.filter(student_id=student_id).first():
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:109:    user = User.objects.create(
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:110:        student_id=student_id,
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:150:class LoginThrottle(UserRateThrottle):
docs/discussions/codex-review-2026-05-27/02-architecture-response.md:153:class UploadThrottle(UserRateThrottle):

exec
/bin/bash -lc "rtk rg -n \"users|student_id|employee_id|counselor_id|admin_id|class_id|applications\" . -g '"'!node_modules'"' -g '"'!dist'"' -g '"'!build'"' -g '"'!coverage'"' -g '"'!*.png'"' -g '"'!*.jpg'"'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
./docs/数据对接说明文档.md:67:| student_id | String | 是 | 学号 | "2020010101" |
./docs/数据对接说明文档.md:72:GET /api/dorm/checkout/status?student_id=2020010101&name=张三
./docs/数据对接说明文档.md:85:  "student_id": "2020010101",
./docs/数据对接说明文档.md:104:| student_id | String | 学号 | "2020010101" |
./docs/数据对接说明文档.md:121:    "student_id": "2020010101",
./docs/数据对接说明文档.md:141:    "student_id": "2020010101",
./docs/数据对接说明文档.md:200:curl -X GET "http://dorm-test.example.com/api/dorm/checkout/status?student_id=2020010101" \
./docs/数据对接说明文档.md:222:| 学号 | student_id | 文本 | 是 | 学生学号 | 2020010101 |
./docs/数据对接说明文档.md:335:| 参数缺失 | 不传student_id | 返回错误码1002 |
./docs/PROJECT-SUMMARY.md:181:1. **users** - 用户表
./docs/PROJECT-SUMMARY.md:182:2. **applications** - 离校申请表
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:13:#### 1. applications_history表设计冗余
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:74:- applications_history表（完整快照）
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:131:1. ✓ 删除applications_history表
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:192:- ### 2.9 申请历史表（applications_history）
./docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md:282:1. **立即修改3个CRITICAL问题**（applications_history、微信绑定、SQLAlchemy）
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:131:**问题：** 学生提交申请时，系统如何确定 `admin_id`（终审管理员）？
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:151:**问题：** 辅导员和管理员使用 `employee_id`，但系统数据库模型中如何存储和映射？
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:156:- `users` 表有 `student_id` 字段（学生学号）
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:163:| 复用 `student_id` 字段存储 `employee_id` | 不需要改表结构 | 字段名语义不清 | ❌ |
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:164:| 新增 `employee_id` 字段 | 语义清晰，扩展性好 | 需要修改表结构 | ✅ |
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:168:1. `users` 表增加 `employee_id` 字段（可空）
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:169:2. 学生账号：`student_id` 必填，`employee_id` 为空
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:170:3. 辅导员/管理员账号：`employee_id` 必填，`student_id` 为空
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:174:- 学生CSV：`student_id` → `users.student_id`
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:175:- 辅导员CSV：`employee_id` → `users.employee_id`
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:176:- 班级映射CSV：`counselor_employee_id` → 查询 `users` 表中 `employee_id` 匹配的记录
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:182:**问题：** 班级-辅导员映射变更后，已提交申请中的 `counselor_id` 是否自动改写？
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:208:| 申请提交时 | 根据当前班级-辅导员映射确定 `counselor_id` |
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:209:| 映射变更后，已提交申请 | `counselor_id` **不变**，保持原审批人 |
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:210:| 映射变更后，新提交申请 | 使用新映射确定 `counselor_id` |
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:214:- `applications` 表的 `counselor_id` 是快照字段，不关联外键级联更新
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:237:2. 班级-辅导员映射表中，`class_id` 必须唯一
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:238:3. CSV导入时强校验：同一 `class_id` 不能出现多次
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:252:2. 允许同一 `class_id` 有多条记录，但只能有一个 `is_primary=true`
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:253:3. 申请提交时使用主辅导员作为 `counselor_id`
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:381:4. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:382:5. 辅导员工号（`employee_id`）是否全校唯一？是否与统一身份认证、人事系统工号一致？
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:458:4. 补充账号标识映射方案（新增 `employee_id` 字段）
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:491:- 补充说明：`employee_id` 必须全校唯一
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:496:- 补充说明：`class_id` 必须唯一，不允许重复
./docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:542:2. **账号标识映射方案：** 我们提出新增 `employee_id` 字段的方案。Codex是否认同这个方案？是否有更好的替代方案？
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:76:        active_users = User.objects.filter(is_active=True)[:100]
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:77:        for user in active_users:
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:156:--cov=apps/applications/workflows.py --cov-fail-under=90
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:210:    def browse_applications(self):
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:212:        self.client.get("/api/v1/applications")
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:217:        self.client.post("/api/v1/applications", json={...})
./docs/discussions/codex-review-2026-05-27/18-claude-analysis-part5-performance-testing.md:222:        self.client.post("/api/v1/applications/1/attachments", files={...})
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:86:#### CRITICAL - applications_history表设计冗余
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:89:`applications_history`表存储完整申请快照（JSON），但：
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:100:**删除applications_history表**，改用audit_logs的字段级追踪：
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:121:`applications`表有`version`字段用于乐观锁，但：
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:139:`applications`表有9个索引，包括3个复合索引：
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:141:- `idx_student_status` (student_id, status, created_at)
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:157:   - `idx_student_id` (学生查看自己申请)
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:205:部分表有`is_deleted`字段（users, applications, attachments），部分表没有（approvals, notifications）。不一致的设计增加理解成本。
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:221:1. **删除applications_history表**：用audit_logs字段级追踪替代
./docs/discussions/codex-review-2026-05-27/14-claude-analysis-part1-architecture-database.md:232:1. 删除applications_history表，简化设计
./docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:59:| CRITICAL | applications_history表冗余 | 存储浪费、维护成本 |
./docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:99:### 1. applications_history表
./docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:156:11. ⚠ 删除applications_history表（需讨论）
./docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:180:### 争议1：applications_history表是否保留？
./docs/discussions/codex-review-2026-05-27/20-claude-codex-comparison.md:236:  - applications_history表是否保留？
./docs/superpowers/plans/2026-05-27-implementation-plan.md:106:│   │   ├── applications/       # 离校申请模块
./docs/superpowers/plans/2026-05-27-implementation-plan.md:226:   - 添加字段：student_id、role、wechat_openid等
./docs/discussions/codex-review-2026-05-27/12-remaining-sections-consensus.md:61:- 添加字段更新逻辑（counselor_id、admin_id、current_approver_id、version）
./docs/design/2026-05-27-system-design.md:146:│   ├── applications/      # 离校申请模块
./docs/design/2026-05-27-system-design.md:193:2. **applications（离校申请）**
./docs/design/2026-05-27-system-design.md:246:1. users - 用户表
./docs/design/2026-05-27-system-design.md:247:2. applications - 离校申请表
./docs/design/2026-05-27-system-design.md:253:8. applications_history - 申请历史表
./docs/design/2026-05-27-system-design.md:255:### 2.2 用户表（users）
./docs/design/2026-05-27-system-design.md:260:CREATE TABLE users (
./docs/design/2026-05-27-system-design.md:262:    student_id VARCHAR(20) UNIQUE NOT NULL COMMENT '学号',
./docs/design/2026-05-27-system-design.md:288:    INDEX idx_student_id (student_id),
./docs/design/2026-05-27-system-design.md:304:### 2.3 离校申请表（applications）
./docs/design/2026-05-27-system-design.md:307:CREATE TABLE applications (
./docs/design/2026-05-27-system-design.md:310:    student_id BIGINT NOT NULL COMMENT '学生ID',
./docs/design/2026-05-27-system-design.md:313:    counselor_id BIGINT COMMENT '辅导员ID',
./docs/design/2026-05-27-system-design.md:314:    admin_id BIGINT COMMENT '学工部管理员ID',
./docs/design/2026-05-27-system-design.md:335:    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE PROTECT,
./docs/design/2026-05-27-system-design.md:336:    FOREIGN KEY (counselor_id) REFERENCES users(id) ON DELETE PROTECT,
./docs/design/2026-05-27-system-design.md:337:    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE PROTECT,
./docs/design/2026-05-27-system-design.md:338:    FOREIGN KEY (current_approver_id) REFERENCES users(id) ON DELETE PROTECT,
./docs/design/2026-05-27-system-design.md:340:    INDEX idx_student_id (student_id),
./docs/design/2026-05-27-system-design.md:341:    INDEX idx_counselor_id (counselor_id),
./docs/design/2026-05-27-system-design.md:342:    INDEX idx_admin_id (admin_id),
./docs/design/2026-05-27-system-design.md:347:    INDEX idx_student_status (student_id, status, created_at),
./docs/design/2026-05-27-system-design.md:377:    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
./docs/design/2026-05-27-system-design.md:378:    FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE PROTECT,
./docs/design/2026-05-27-system-design.md:407:    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
./docs/design/2026-05-27-system-design.md:444:    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
./docs/design/2026-05-27-system-design.md:445:    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE PROTECT,
./docs/design/2026-05-27-system-design.md:480:    FOREIGN KEY (updated_by) REFERENCES users(id)
./docs/design/2026-05-27-system-design.md:527:    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE PROTECT,
./docs/design/2026-05-27-system-design.md:557:### 2.9 申请历史表（applications_history）
./docs/design/2026-05-27-system-design.md:562:CREATE TABLE applications_history (
./docs/design/2026-05-27-system-design.md:571:    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
./docs/design/2026-05-27-system-design.md:572:    FOREIGN KEY (changed_by) REFERENCES users(id) ON DELETE PROTECT,
./docs/design/2026-05-27-system-design.md:591:users (用户表)
./docs/design/2026-05-27-system-design.md:592:  ├─1:N─→ applications (学生创建多个申请)
./docs/design/2026-05-27-system-design.md:596:applications (申请表)
./docs/design/2026-05-27-system-design.md:597:  ├─N:1─→ users (申请人)
./docs/design/2026-05-27-system-design.md:598:  ├─N:1─→ users (辅导员)
./docs/design/2026-05-27-system-design.md:599:  ├─N:1─→ users (学工部管理员)
./docs/design/2026-05-27-system-design.md:600:  ├─N:1─→ users (当前审批人)
./docs/design/2026-05-27-system-design.md:604:  └─1:N─→ applications_history (一个申请多个历史版本)
./docs/design/2026-05-27-system-design.md:608:  ├─N:1─→ applications (多条审批记录属于一个申请)
./docs/design/2026-05-27-system-design.md:609:  └─N:1─→ users (审批人)
./docs/design/2026-05-27-system-design.md:612:  └─N:1─→ applications (多个附件属于一个申请)
./docs/design/2026-05-27-system-design.md:615:  ├─N:1─→ users (接收人)
./docs/design/2026-05-27-system-design.md:616:  └─N:1─→ applications (关联申请)
./docs/design/2026-05-27-system-design.md:619:  └─N:1─→ users (操作人)
./docs/design/2026-05-27-system-design.md:622:  └─N:1─→ users (更新人)
./docs/design/2026-05-27-system-design.md:683:  "student_id": "2020001",
./docs/design/2026-05-27-system-design.md:697:      "student_id": "2020001",
./docs/design/2026-05-27-system-design.md:724:      "student_id": "2020001",
./docs/design/2026-05-27-system-design.md:762:  "student_id": "2020001",
./docs/design/2026-05-27-system-design.md:775:      "student_id": "2020001",
./docs/design/2026-05-27-system-design.md:797:  "student_id": "2020001",
./docs/design/2026-05-27-system-design.md:811:      "student_id": "2020001",
./docs/design/2026-05-27-system-design.md:850:POST /api/v1/applications
./docs/design/2026-05-27-system-design.md:875:GET /api/v1/applications?status=pending_counselor&page=1&page_size=20
./docs/design/2026-05-27-system-design.md:902:GET /api/v1/applications/{id}
./docs/design/2026-05-27-system-design.md:913:      "student_id": "2020001",
./docs/design/2026-05-27-system-design.md:941:PUT /api/v1/applications/{id}
./docs/design/2026-05-27-system-design.md:959:POST /api/v1/applications/{id}/submit
./docs/design/2026-05-27-system-design.md:1066:POST /api/v1/applications/{id}/attachments
./docs/design/2026-05-27-system-design.md:1288:    "student_id": "2020001",
./docs/design/2026-05-27-system-design.md:1383:        return obj.student_id == request.user.id
./docs/design/2026-05-27-system-design.md:1427:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
./docs/design/2026-05-27-system-design.md:1428:  - 设置当前审批人：current_approver_id = counselor_id
./docs/design/2026-05-27-system-design.md:1431:  - 创建历史快照：applications_history（version=0, change_reason='提交申请'）
./docs/design/2026-05-27-system-design.md:1443:    - 更新当前审批人：current_approver_id = admin_id
./docs/design/2026-05-27-system-design.md:1446:    - 创建历史快照：applications_history（version=N, change_reason='辅导员审批通过'）
./docs/design/2026-05-27-system-design.md:1454:    - 创建历史快照：applications_history（version=N, change_reason='辅导员驳回'）
./docs/design/2026-05-27-system-design.md:1473:    - 创建历史快照：applications_history（version=N, change_reason='学工部备案通过'）
./docs/design/2026-05-27-system-design.md:1482:    - 创建历史快照：applications_history（version=N, change_reason='学工部驳回'）
./docs/design/2026-05-27-system-design.md:1627:  student_id: 2020001
./docs/design/2026-05-27-system-design.md:1633:    "student_id": "2020001",
./docs/design/2026-05-27-system-design.md:1657:    def get_checkout_status(self, student_id):
./docs/design/2026-05-27-system-design.md:1659:            f'{self.base_url}/api/students/{student_id}/checkout',
./docs/design/2026-05-27-system-design.md:1679:    def verify_clearance(self, student_id):
./docs/design/2026-05-27-system-design.md:1683:                params={"student_id": student_id},
./docs/design/2026-05-27-system-design.md:1727:def verify_dorm_clearance(student_id):
./docs/design/2026-05-27-system-design.md:1729:    return plugin.verify_clearance(student_id)
./docs/design/2026-05-27-system-design.md:1982:def bind_wechat_to_account(student_id, wechat_openid, password):
./docs/design/2026-05-27-system-design.md:1984:    user = User.objects.filter(student_id=student_id).first()
./docs/design/2026-05-27-system-design.md:1990:            request_data={'student_id': student_id}
./docs/design/2026-05-27-system-design.md:2108:        location /api/v1/applications/*/attachments {
./docs/design/2026-05-27-system-design.md:2337:-- users表索引
./docs/design/2026-05-27-system-design.md:2338:CREATE INDEX idx_student_id ON users(student_id);
./docs/design/2026-05-27-system-design.md:2339:CREATE INDEX idx_role ON users(role);
./docs/design/2026-05-27-system-design.md:2340:CREATE INDEX idx_wechat_openid ON users(wechat_openid);
./docs/design/2026-05-27-system-design.md:2341:CREATE INDEX idx_account_locked ON users(account_locked);
./docs/design/2026-05-27-system-design.md:2343:-- applications表索引
./docs/design/2026-05-27-system-design.md:2344:CREATE INDEX idx_student_id ON applications(student_id);
./docs/design/2026-05-27-system-design.md:2345:CREATE INDEX idx_counselor_id ON applications(counselor_id);
./docs/design/2026-05-27-system-design.md:2346:CREATE INDEX idx_admin_id ON applications(admin_id);
./docs/design/2026-05-27-system-design.md:2347:CREATE INDEX idx_status ON applications(status);
./docs/design/2026-05-27-system-design.md:2348:CREATE INDEX idx_application_no ON applications(application_no);
./docs/design/2026-05-27-system-design.md:2349:CREATE INDEX idx_planned_leave_date ON applications(planned_leave_date);
./docs/design/2026-05-27-system-design.md:2351:-- applications表复合索引
./docs/design/2026-05-27-system-design.md:2352:CREATE INDEX idx_approver_status ON applications(current_approver_id, status, submit_time);
./docs/design/2026-05-27-system-design.md:2353:CREATE INDEX idx_student_status ON applications(student_id, status, created_at);
./docs/design/2026-05-27-system-design.md:2354:CREATE INDEX idx_status_deleted ON applications(status, is_deleted, submit_time);
./docs/design/2026-05-27-system-design.md:2464:    cache.delete(f'student:{app.student_id}:applications')
./docs/design/2026-05-27-system-design.md:2593:    result = approve_application(app_id, counselor_id, 'approve')
./docs/design/2026-05-27-system-design.md:2598:    response = client.post('/api/v1/applications', data)
./docs/design/2026-05-27-system-design.md:2604:    response = bind_wechat(student_id='2020001', openid='oXXX', password='wrong')
./docs/design/2026-05-27-system-design.md:2611:    response = client.get('/api/v1/applications', headers={'Authorization': f'Bearer {token}'})
./docs/design/2026-05-27-system-design.md:2630:    bind_wechat(student_id='2020001', openid='oXXX', password='pass')
./docs/design/2026-05-27-system-design.md:2638:    r1 = bind_wechat(student_id='9999999', openid='oXXX', password='pass')
./docs/design/2026-05-27-system-design.md:2640:    r2 = bind_wechat(student_id='2020001', openid='oXXX', password='wrong')
./docs/design/2026-05-27-system-design.md:2642:    r3 = bind_wechat(student_id='2020002', openid='oXXX', password='pass')
./docs/design/2026-05-27-system-design.md:2665:    response = client.post(f'/api/v1/applications/{app_id}/attachments', files={'file': fake_image})
./docs/design/2026-05-27-system-design.md:2678:    approve_application(app_id, counselor_id, 'approve')
./docs/design/2026-05-27-system-design.md:2736:    def view_applications(self):
./docs/design/2026-05-27-system-design.md:2737:        self.client.get("/api/v1/applications")
./docs/design/2026-05-27-system-design.md:2741:        self.client.get("/api/v1/applications/1")
./docs/discussions/codex-review-2026-05-27/04-database-review.md:24:- users表有`is_deleted`字段（软删除）
./docs/discussions/codex-review-2026-05-27/04-database-review.md:25:- applications表有`student_id`外键指向users
./docs/discussions/codex-review-2026-05-27/04-database-review.md:27:- 查询`applications WHERE is_deleted=FALSE`会返回申请，但关联的用户是已删除状态
./docs/discussions/codex-review-2026-05-27/04-database-review.md:31:2. 查询复杂：每个查询需要`AND users.is_deleted=FALSE`
./docs/discussions/codex-review-2026-05-27/04-database-review.md:47:CREATE TABLE users_archive (
./docs/discussions/codex-review-2026-05-27/04-database-review.md:48:    -- 与users相同结构
./docs/discussions/codex-review-2026-05-27/04-database-review.md:69:SELECT * FROM applications 
./docs/discussions/codex-review-2026-05-27/04-database-review.md:92:-- applications表
./docs/discussions/codex-review-2026-05-27/04-database-review.md:93:CREATE INDEX idx_approver_status ON applications(current_approver_id, status, submit_time);
./docs/discussions/codex-review-2026-05-27/04-database-review.md:94:CREATE INDEX idx_student_status ON applications(student_id, status, created_at);
./docs/discussions/codex-review-2026-05-27/04-database-review.md:95:CREATE INDEX idx_status_deleted ON applications(status, is_deleted, submit_time);
./docs/discussions/codex-review-2026-05-27/04-database-review.md:153:    FOREIGN KEY (user_id) REFERENCES users(id),
./docs/discussions/codex-review-2026-05-27/04-database-review.md:159:### 4. applications表缺少关键字段
./docs/discussions/codex-review-2026-05-27/04-database-review.md:164:- 无`counselor_id`（只有`current_approver_id`会变）
./docs/discussions/codex-review-2026-05-27/04-database-review.md:165:- 无`admin_id`（谁做的最终审批？）
./docs/discussions/codex-review-2026-05-27/04-database-review.md:176:CREATE TABLE applications (
./docs/discussions/codex-review-2026-05-27/04-database-review.md:180:    counselor_id BIGINT COMMENT '辅导员ID',
./docs/discussions/codex-review-2026-05-27/04-database-review.md:181:    admin_id BIGINT COMMENT '学工部管理员ID',
./docs/discussions/codex-review-2026-05-27/04-database-review.md:190:    FOREIGN KEY (counselor_id) REFERENCES users(id),
./docs/discussions/codex-review-2026-05-27/04-database-review.md:191:    FOREIGN KEY (admin_id) REFERENCES users(id),
./docs/discussions/codex-review-2026-05-27/04-database-review.md:192:    INDEX idx_counselor_id (counselor_id),
./docs/discussions/codex-review-2026-05-27/04-database-review.md:193:    INDEX idx_admin_id (admin_id)
./docs/discussions/codex-review-2026-05-27/04-database-review.md:197:### 5. users表缺少认证安全字段
./docs/discussions/codex-review-2026-05-27/04-database-review.md:210:CREATE TABLE users (
./docs/discussions/codex-review-2026-05-27/04-database-review.md:243:ON applications(student_id) 
./docs/discussions/codex-review-2026-05-27/04-database-review.md:253:                student_id=self.student_id,
./docs/discussions/codex-review-2026-05-27/04-database-review.md:287:- 无`applications_history`表（申请被驳回重提时，旧数据丢失）
./docs/discussions/codex-review-2026-05-27/04-database-review.md:300:- 是否应添加`applications_history`表用于审计追踪？
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:14:1. **班级-辅导员对应关系应明确列为 P0。** 这是自动分配审批人的核心数据。没有它，系统提交申请时无法稳定设置 `counselor_id` 和 `current_approver_id`，只能退化为人工逐个配置或人工改派。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:46:| 学生基本信息 | CSV/Excel 批量导入 | 教务系统 API | 首版按毕业届别导入更容易落地。字段建议包括 `student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:47:| 辅导员基本信息 | CSV/Excel 批量导入 | 人事系统 API 或手动创建 | 约 50 人规模下，批量导入足够。字段建议包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:48:| 班级-辅导员对应关系 | CSV/Excel 批量导入并强校验 | 教务系统 API | 必须优先支持。建议用 `class_id + counselor_employee_id + effective_term` 表达关系，不要只靠 `class_name`。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无审批人的学生数。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:51:| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 后续对接时只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，不要引入借阅明细。 |
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:69:理由是辅导员规模约 50 人，变化频率低，API 改造投入可能高于收益。但数据结构必须标准化，尤其是 `employee_id` 要能被班级-辅导员映射引用。若学校已有成熟 HR API 或统一身份平台，可在后续升级为 API 同步。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:100:1. **班级唯一标识。** 当前分析偏向 `class_name`，但班级名称可能重复、改名或跨届复用。应要求 `class_id`，`class_name` 只用于展示。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:108:5. **审批人变更后的历史一致性。** 已提交申请中的 `counselor_id` 应保持历史一致，不应因后续班级映射变更自动改写。若需改派，应由管理员显式操作并记录审计日志。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:112:7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:130:3. **定义辅导员基本信息导入模板。** 先确保 counselor 账号存在，且 `employee_id` 可被映射数据引用。
./docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md:151:2. 新增“辅导员基本信息导入”章节，明确 `employee_id`、联系方式和账号状态。
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:96:        student_id=student_id
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:144:# applications表
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:146:Index(fields=['student_id', 'status', 'created_at'])
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:172:### 3.4 applications表新增字段
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:175:- counselor_id BIGINT（固定辅导员ID）
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:176:- admin_id BIGINT（固定学工部管理员ID）
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:181:### 3.5 users表新增安全字段
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:206:            student_id=self.student_id,
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:238:### 3.10 applications_history表
./docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md:304:- ✅ applications_history表
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:179:    result = dorm_api.check_status(student_id, timeout=2)
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:182:    enqueue_retry_task(student_id)
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:187:def retry_dorm_check(student_id):
./docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md:188:    result = dorm_api.check_status(student_id)
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:180:示例位置包括 `docs/design/2026-05-27-system-design.md:258` 起的 users 表，以及后续所有核心表。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:199:applications 表写了 `ON DELETE PROTECT`。这是 Django ORM 的行为，不是 PostgreSQL 外键动作。数据库层应使用 `RESTRICT`/`NO ACTION`，或只在模型层用 `on_delete=PROTECT`。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:207:- `idx_users_student_id`
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:214:users 表对 `student_id`、`wechat_openid` 使用全局唯一。配合 `is_deleted` 软删除后，已删除用户仍会占用学号和 openid。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:219:CREATE UNIQUE INDEX uniq_users_active_student_id
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:220:ON users(student_id)
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:228:共识文档提到“一个学生只能有一个进行中申请”。设计主文档没有在 applications 表中明确部分唯一索引，仅在流程逻辑中描述。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:254:applications_history 表使用 `snapshot TEXT`。在 PostgreSQL + Django 下应优先使用 `JSONField`，便于校验、查询和迁移。评审讨论中也已经确认 JSONField 更合适，但主文档未完全落地。
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:341:location /api/v1/applications/*/attachments
./docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md:347:location ~ ^/api/v1/applications/[^/]+/attachments$ { ... }
./docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:68:    "student_id": "2020001",
./docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:84:    "student_id": "2020001",
./docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:113:| student_id | String | 学号 | 是 | "2020010101" |
./docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:133:- **决策：** 不在applications表存储
./docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md:134:- **理由：** users表已有，避免冗余
./docs/discussions/codex-review-2026-05-27/01-architecture-review.md:51:if existing_user := User.objects.filter(student_id=student_id).first():
./docs/discussions/codex-review-2026-05-27/01-architecture-review.md:79:- 上传垃圾文件（/api/v1/applications/{id}/attachments无速率限制）
./docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:111:- users表已有class_name字段，API响应中的class_name来自宿舍系统
./docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:112:- 建议：不需要在applications表存储，直接从users表读取即可
./docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md:118:  - 如果需要在离校凭证上显示：需要存储到applications表
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:35:| 班级-辅导员对应关系 | 完整且必要 | 是自动分配 `counselor_id` 和权限边界的关键数据。 |
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:46:1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:48:3. **账号标识映射。** 当前系统设计中的 `users.student_id` 被用作唯一登录标识，但共识文档给辅导员和管理员使用 `employee_id`。需要明确导入时 `employee_id` 映射到哪个内部字段，或后续模型是否新增统一的 `external_id/employee_id`。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:56:字段整体合理，能支撑首版业务。`student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`is_graduating` 作为必填基本可接受。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:97:该章节是文档中最关键、也最合理的部分。`class_id` 作为必填是正确的，避免只靠班级名称匹配。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:103:3. **历史一致性规则。** 班级映射变更后，不应自动改写已提交申请中的 `counselor_id`；已提交申请如需改派，应由管理员显式操作并记录审计日志。
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:182:3. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
./docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md:277:1. `employee_id` 必须全校唯一，并与班级映射中的 `counselor_employee_id` 完全一致。
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:78:   - 同意。`is_timeout`在`approvals`表，不在`applications`表
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:83:   - 将添加：提交时设置`counselor_id`、`admin_id`
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:89:   - 将添加：每次状态转换创建`applications_history`快照
./docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md:103:- 添加完整的字段更新逻辑（counselor_id、admin_id、current_approver_id、version）
./docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md:101:1. `student_id + name` 已足够唯一标识学生
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:35:- 6个核心模块（accounts, applications, approvals, attachments, notifications, integrations）
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:50:- applications表的复合索引（idx_approver_status, idx_student_status, idx_status_deleted）
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:53:- applications_history表的必要性
./docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md:83:- 审批历史追踪（applications_history表）
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:39:CREATE TABLE users (
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:46:CREATE TABLE users (
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:51:COMMENT ON TABLE users IS '用户表';
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:52:COMMENT ON COLUMN users.name IS '姓名';
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:82:FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE SET NULL
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:86:FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE PROTECT
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:212:### 争议1：applications_history表
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:222:CREATE TABLE applications_history (
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:230:    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:264:def bind_wechat_to_account(student_id, wechat_openid, password):
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:266:    user = User.objects.filter(student_id=student_id).first()
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:272:            request_data={'student_id': student_id}
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:350:-- applications表（9个索引 → 3个基础索引）
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:351:CREATE INDEX idx_student_id ON applications(student_id);
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:352:CREATE INDEX idx_status ON applications(status);
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:353:CREATE INDEX idx_application_no ON applications(application_no);
./docs/discussions/codex-review-2026-05-27/21-final-consensus.md:453:- ✓ 简化applications_history表
./docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:33:1. 攻击者用微信注册，使用受害者的student_id
./docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:67:**问题：** 代码泄露student_id是否存在：
./docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:68:- "该学号已绑定其他微信账号" → student_id存在
./docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:69:- "该学号已注册，请输入密码" → student_id存在但无微信
./docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:70:- 创建新用户 → student_id不存在
./docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:76:if existing_user := User.objects.filter(student_id=student_id).first():
./docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:87:**问题：** 两个请求使用相同student_id + 不同openid可能同时通过检查，然后都执行绑定。
./docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md:95:        student_id=student_id
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:42:| 学号 | student_id | 文本 | 是 | 学生唯一标识 | 2020010101 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:46:| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2020-01 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:65:    student_id,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:69:    class_id,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:103:| 学号 | student_id | 文本 | 是 | 学生学号 | 2020010101 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:124:    student_id,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:155:| 工号 | employee_id | 文本 | 是 | 辅导员唯一标识 | T2020001 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:168:    employee_id,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:207:| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2020-01 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:209:| 辅导员工号 | counselor_employee_id | 文本 | 是 | 辅导员工号 | T2020001 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:221:    class_id,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:223:    counselor_employee_id,
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:270:| 工号 | employee_id | 文本 | 是 | 管理员唯一标识 | A2020001 |
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:385:- 学生表中的class_id必须在班级-辅导员映射表中存在
./docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md:386:- 班级-辅导员映射表中的counselor_employee_id必须在辅导员表中存在
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:17:- 每个查询需要`AND users.is_deleted=FALSE` ✓
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:51:        related_name='applications'
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:56:        if self.applications.filter(
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:89:            models.Index(fields=['student_id', 'status', 'created_at'], 
./docs/discussions/codex-review-2026-05-27/05-database-response-part1.md:128:# applications表原设计缺少这个索引
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:47:   - 尽管applications表有`current_approver_id`和`version`字段（lines 316-327）
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:80:   - `is_timeout`字段在`approvals`表，不在`applications`表（lines 371-372）
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:83:   - `counselor_id`
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:84:   - `admin_id`
./docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md:90:   - `applications_history`快照
./docs/discussions/codex-review-2026-05-27/26-user-docs-codex-response.md:97:不要在宿舍清退接口中使用 `id_card`，用 `student_id + name` 足够。
./docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:61:### Q1: 是否添加applications_history表？
./docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:145:1. ✅ `applications_history` - 申请历史版本
./docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:169:4. ✅ applications表添加字段（counselor_id, admin_id, version, certificate_url）
./docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:170:5. ✅ users表添加认证安全字段
./docs/discussions/codex-review-2026-05-27/07-database-response-part3.md:175:10. ✅ 添加applications_history表
./docs/discussions/codex-review-2026-05-27/02-architecture-response.md:80:    student_id = request.data['student_id']
./docs/discussions/codex-review-2026-05-27/02-architecture-response.md:87:    if existing_user := User.objects.filter(student_id=student_id).first():
./docs/discussions/codex-review-2026-05-27/02-architecture-response.md:110:        student_id=student_id,
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:40:  "student_id": "2020010101",
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:87:    "student_id": "2020001",
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:119:  - 缺点：users表中已有class_name字段，可能冗余
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:133:student_id → name → class_name → dorm_building → dorm_room → bed_number → is_checked_out → ...
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:137:- 学生信息：student_id、name、class_name
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:146:- users表已有class_name字段
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:147:- applications表没有床号字段
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:150:- [ ] 在applications表添加bed_number字段？
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:174:**问题：** class_name在users表和API响应中都有，是否冗余？
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:177:- users表的class_name：学生的实际班级（来自学生信息系统）
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:186:**问题：** 床号是否需要存储到applications表？
./docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md:204:- class_name vs class_id
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:23:根据系统设计文档（`users`表），系统有3个角色：
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:45:- 学号（student_id）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:71:- 学号（student_id）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:93:- 工号（employee_id）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:118:- 辅导员工号（counselor_employee_id）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:143:- 工号（employee_id）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:172:- 学号（student_id）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:198:- 学号（student_id）
./docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md:225:- 学号（student_id）
./docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:69:**决策：** 不在applications表存储
./docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:72:- users表已有class_name字段
./docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:73:- API响应中的class_name直接从users表读取
./docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:82:- 如果后续需要在离校凭证上显示床号，再添加到applications表
./docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md:113:| student_id | String | 学号 | 是 | "2020010101" |
./docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:39:**4. applications表字段**
./docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:40:- ✅ 添加counselor_id, admin_id, version, certificate_url, certificate_generated_at
./docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:44:**5. users表安全字段**
./docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:62:- ✅ applications_history: 是（良好的审计追踪）
./docs/discussions/codex-review-2026-05-27/08-database-confirmation.md:73:1. applications_history表 ✅
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:52:### 4. applications表缺少关键字段 - **完全同意**
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:61:    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='applications')
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:68:        related_name='counselor_applications',
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:75:        related_name='admin_applications',
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:85:        related_name='pending_applications'
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:106:            models.Index(fields=['student_id']),
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:107:            models.Index(fields=['counselor_id']),
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:108:            models.Index(fields=['admin_id']),
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:131:### 5. users表缺少认证安全字段 - **完全同意**
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:138:    student_id = models.CharField(max_length=20, unique=True)
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:167:            models.Index(fields=['student_id']),
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:197:                student_id=self.student_id,
./docs/discussions/codex-review-2026-05-27/06-database-response-part2.md:218:ON applications(student_id) 
./docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md:76:**理由：** `student_id + name` 已足够唯一标识，避免身份证号在系统间传输。
./docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:68:    def get_checkout_status(self, student_id):
./docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md:70:            f'{self.base_url}/api/students/{student_id}/checkout',

codex
前置审查与原共识对上了：回应里的“只找宿管系统确认”在项目边界下可以成立，但它把“系统边界”和“数据权责/验收风险”有点混在一起了。我会再核对用户表设计和模板约束，重点看 `employee_id` 方案有没有落地冲突。
exec
/bin/bash -lc "rtk nl -ba docs/design/2026-05-27-system-design.md | sed -n '255,345p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   255	### 2.2 用户表（users）
   256	
   257	**说明：** 以下SQL为概念示例，使用类MySQL语法便于阅读。实际实现以Django Model为准，Django ORM会自动生成符合PostgreSQL的DDL语句。
   258	
   259	```sql
   260	CREATE TABLE users (
   261	    id BIGINT PRIMARY KEY AUTO_INCREMENT,
   262	    student_id VARCHAR(20) UNIQUE NOT NULL COMMENT '学号',
   263	    name VARCHAR(50) NOT NULL COMMENT '姓名',
   264	    password_hash VARCHAR(255) COMMENT '密码哈希',
   265	    wechat_openid VARCHAR(100) UNIQUE COMMENT '微信OpenID',
   266	    
   267	    -- 认证安全字段
   268	    password_setup_required BOOLEAN DEFAULT FALSE COMMENT '需要设置密码',
   269	    account_locked BOOLEAN DEFAULT FALSE COMMENT '账户锁定',
   270	    failed_login_attempts INT DEFAULT 0 COMMENT '失败登录次数',
   271	    last_login_at TIMESTAMP COMMENT '最后登录时间',
   272	    last_login_ip VARCHAR(50) COMMENT '最后登录IP',
   273	    wechat_bind_time TIMESTAMP COMMENT '微信绑定时间',
   274	    password_changed_at TIMESTAMP COMMENT '密码修改时间',
   275	    
   276	    phone VARCHAR(20) COMMENT '手机号',
   277	    email VARCHAR(100) COMMENT '邮箱',
   278	    role VARCHAR(20) NOT NULL COMMENT '角色: student/counselor/admin',
   279	    department VARCHAR(100) COMMENT '院系',
   280	    major VARCHAR(100) COMMENT '专业',
   281	    class_name VARCHAR(50) COMMENT '班级',
   282	    grade INT COMMENT '年级',
   283	    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
   284	    is_deleted BOOLEAN DEFAULT FALSE COMMENT '是否删除',
   285	    created_at TIMESTAMP,
   286	    updated_at TIMESTAMP,
   287	    
   288	    INDEX idx_student_id (student_id),
   289	    INDEX idx_role (role),
   290	    INDEX idx_wechat_openid (wechat_openid),
   291	    INDEX idx_account_locked (account_locked),
   292	    
   293	    CONSTRAINT chk_auth_method CHECK (
   294	        (password_hash IS NOT NULL) OR (wechat_openid IS NOT NULL)
   295	    )
   296	) COMMENT='用户表';
   297	```
   298	
   299	**字段说明：**
   300	- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
   301	- `wechat_openid`: 微信授权登录后绑定
   302	- `is_deleted`: 软删除标记
   303	
   304	### 2.3 离校申请表（applications）
   305	
   306	```sql
   307	CREATE TABLE applications (
   308	    id BIGINT PRIMARY KEY AUTO_INCREMENT,
   309	    application_no VARCHAR(50) UNIQUE NOT NULL COMMENT '申请编号',
   310	    student_id BIGINT NOT NULL COMMENT '学生ID',
   311	    
   312	    -- 固定审批人追踪
   313	    counselor_id BIGINT COMMENT '辅导员ID',
   314	    admin_id BIGINT COMMENT '学工部管理员ID',
   315	    
   316	    planned_leave_date DATE NOT NULL COMMENT '计划离校日期',
   317	    status VARCHAR(20) NOT NULL COMMENT '状态',
   318	    current_approver_id BIGINT COMMENT '当前审批人ID',
   319	    submit_time TIMESTAMP COMMENT '提交时间',
   320	    complete_time TIMESTAMP COMMENT '完成时间',
   321	    reject_reason TEXT COMMENT '驳回原因',
   322	    remarks TEXT COMMENT '备注',
   323	    
   324	    -- 凭证追踪
   325	    certificate_url VARCHAR(500) COMMENT '离校凭证URL',
   326	    certificate_generated_at TIMESTAMP COMMENT '凭证生成时间',
   327	    
   328	    -- 乐观锁
   329	    version INT DEFAULT 0 COMMENT '版本号',
   330	    
   331	    is_deleted BOOLEAN DEFAULT FALSE,
   332	    created_at TIMESTAMP,
   333	    updated_at TIMESTAMP,
   334	    
   335	    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE PROTECT,
   336	    FOREIGN KEY (counselor_id) REFERENCES users(id) ON DELETE PROTECT,
   337	    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE PROTECT,
   338	    FOREIGN KEY (current_approver_id) REFERENCES users(id) ON DELETE PROTECT,
   339	    
   340	    INDEX idx_student_id (student_id),
   341	    INDEX idx_counselor_id (counselor_id),
   342	    INDEX idx_admin_id (admin_id),
   343	    INDEX idx_status (status),
   344	    INDEX idx_application_no (application_no),
   345	    INDEX idx_planned_leave_date (planned_leave_date),

exec
/bin/bash -lc "rtk nl -ba docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md | sed -n '1,230p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# 对Codex数据需求审查的回应
     2	
     3	**回应时间：** 2026-05-27  
     4	**回应对象：** `32-codex-data-requirements-review.md`  
     5	**原始文档：** `31-data-source-requirements-consensus.md`
     6	
     7	---
     8	
     9	## 一、核心项目约束澄清
    10	
    11	**重要说明：本项目只对接宿管系统，不直接对接教务、人事、学工等其他系统。**
    12	
    13	### 1.1 项目边界
    14	
    15	本毕业离校系统的数据对接范围限定为：
    16	- **唯一数据源：** 宿管系统
    17	- **数据获取方式：** 通过宿管系统提供的数据库、API或CSV文件
    18	- **数据责任方：** 宿管系统负责人
    19	
    20	### 1.2 为什么只对接宿管系统
    21	
    22	1. **项目定位：** 本系统是宿管系统的配套子系统，不是全校级统一离校平台
    23	2. **数据归集：** 宿管系统已从教务、人事、学工等系统归集了所需数据
    24	3. **实施简化：** 避免多方对接的协调成本和技术复杂度
    25	4. **权责清晰：** 数据质量、更新时效由宿管系统统一负责
    26	
    27	### 1.3 对Codex审查的影响
    28	
    29	基于上述约束，Codex审查中的部分建议需要重新评估：
    30	- ✅ **接受：** 对接方式、字段定义、实施细节的建议
    31	- ❌ **不接受：** 将反馈对象从"宿管系统"改为"多方数据负责人"
    32	- 🔄 **调整：** 待反馈问题需明确"宿管系统能否提供这些数据"
    33	
    34	---
    35	
    36	## 二、对Codex四大核心问题的逐项回应
    37	
    38	### 2.1 问题1：反馈对象错误
    39	
    40	**Codex意见：** 将"提交给宿管系统方"改为"提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人"。
    41	
    42	**我们的回应：** ❌ **不接受此建议**
    43	
    44	**理由：**
    45	
    46	基于项目约束（只对接宿管系统），原文档的反馈对象是正确的：
    47	1. 本系统只对接宿管系统，不直接对接教务、人事、学工
    48	2. 学生、辅导员、班级映射等数据由宿管系统负责提供
    49	3. 宿管系统如何获取这些数据（是否从教务/人事归集）是宿管系统的内部实现
    50	4. 我们的职责是明确需求，由宿管系统确认能否提供
    51	
    52	**但我们接受Codex的隐含提醒：**
    53	
    54	需要在待反馈问题中明确询问宿管系统：
    55	- 这些数据是否在宿管系统数据库中？
    56	- 如果不在，宿管系统能否从其他系统归集后提供？
    57	- 如果无法提供，是否需要调整项目对接范围？
    58	
    59	**修改方案：**
    60	- 保持反馈对象为"宿管系统方"
    61	- 在待反馈问题中增加："宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？如不包含，能否从教务/人事/学工系统归集后提供？"
    62	
    63	---
    64	
    65	### 2.2 问题2：对接方式过激
    66	
    67	**Codex意见：** 学生、辅导员、班级映射的"DB优先"改为"CSV/Excel优先，API/DB增强"。
    68	
    69	**我们的回应：** ✅ **完全接受**
    70	
    71	**理由：**
    72	
    73	1. **实施周期：** CSV/Excel导入最快，DB直连需要安全审批和网络配置
    74	2. **变更频率：** 账号数据变更频率低（学期级），不需要实时同步
    75	3. **风险控制：** CSV导入可以先验证、再导入、可回滚；DB直连风险更高
    76	4. **首版策略：** 先用CSV快速上线，后续根据数据变更频率决定是否升级为API/DB
    77	
    78	**修改方案：**
    79	
    80	| 数据源 | 原方案 | 修改后方案 |
    81	|--------|--------|-----------|
    82	| 学生基本信息 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先** / API或DB视图增强 |
    83	| 辅导员基本信息 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先** / 人事或统一身份API增强 |
    84	| 班级-辅导员对应关系 | DB优先 / API备选 / CSV降级 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
    85	| 宿舍清退数据 | API优先 / DB备选 / CSV降级 | **保持不变**（API优先合理） |
    86	
    87	**特别说明：**
    88	- 宿舍清退数据保持API优先，因为需要实时校验学生提交时的清退状态
    89	- 账号数据采用CSV首版，上线后根据实际变更频率决定是否升级
    90	
    91	---
    92	
    93	### 2.3 问题3：字段定义不一致
    94	
    95	**Codex意见：** `checkout_status` 在本文档中标为可选，但既有字段共识中API响应建议必填。
    96	
    97	**我们的回应：** ✅ **完全接受**
    98	
    99	**理由：**
   100	
   101	1. **业务必要性：** 清退状态是提交前置校验的核心字段，必须明确
   102	2. **一致性：** 应与之前的字段共识保持一致
   103	3. **降级处理：** 即使API查询失败，也应返回 `unknown` 而非空值
   104	
   105	**修改方案：**
   106	
   107	| 字段 | 原定义 | 修改后定义 |
   108	|------|--------|-----------|
   109	| `checkout_status` | 可选 | **必填**，枚举：`completed`/`pending`/`not_started`/`unknown` |
   110	| `checkout_date` | 可选 | **条件必填**：当 `checkout_status = completed` 时必填 |
   111	| `source_updated_at` | 未列出 | **建议新增**：记录外部系统数据更新时间 |
   112	
   113	**枚举值说明：**
   114	- `completed`：已完成清退
   115	- `pending`：清退中（已申请但未完成）
   116	- `not_started`：未开始清退
   117	- `unknown`：查询失败或数据不可用（用于API异常时的降级）
   118	
   119	---
   120	
   121	### 2.4 问题4：缺实施细节
   122	
   123	**Codex意见：** 缺少终审管理员分配规则、账号标识映射、历史审批人一致性规则、多辅导员场景处理。
   124	
   125	**我们的回应：** ✅ **完全接受，需要补充**
   126	
   127	这些确实是实施级关键问题，需要在文档中明确。我们逐项回应：
   128	
   129	#### 4.1 终审管理员分配规则
   130	
   131	**问题：** 学生提交申请时，系统如何确定 `admin_id`（终审管理员）？
   132	
   133	**我们的方案：**
   134	
   135	首版采用**固定终审人**方案：
   136	1. 系统配置表中设置默认终审管理员（1-2人）
   137	2. 所有申请提交时自动分配给默认终审人
   138	3. 管理员可以在后台手动转交给其他管理员
   139	
   140	**后续增强方案（P1）：**
   141	- 轮转分配：按提交顺序轮流分配给管理员组
   142	- 按学院分配：不同学院的申请分配给不同终审人
   143	- 负载均衡：根据管理员当前待审数量智能分配
   144	
   145	**修改方案：** 在文档中增加"终审管理员配置"章节，说明首版采用固定终审人。
   146	
   147	---
   148	
   149	#### 4.2 账号标识映射
   150	
   151	**问题：** 辅导员和管理员使用 `employee_id`，但系统数据库模型中如何存储和映射？
   152	
   153	**我们的方案：**
   154	
   155	当前数据库设计：
   156	- `users` 表有 `student_id` 字段（学生学号）
   157	- 辅导员和管理员账号需要统一标识字段
   158	
   159	**两种方案对比：**
   160	
   161	| 方案 | 优点 | 缺点 | 我们的选择 |
   162	|------|------|------|-----------|
   163	| 复用 `student_id` 字段存储 `employee_id` | 不需要改表结构 | 字段名语义不清 | ❌ |
   164	| 新增 `employee_id` 字段 | 语义清晰，扩展性好 | 需要修改表结构 | ✅ |
   165	
   166	**修改方案：**
   167	
   168	1. `users` 表增加 `employee_id` 字段（可空）
   169	2. 学生账号：`student_id` 必填，`employee_id` 为空
   170	3. 辅导员/管理员账号：`employee_id` 必填，`student_id` 为空
   171	4. 登录时根据账号类型判断使用哪个字段
   172	
   173	**数据导入映射：**
   174	- 学生CSV：`student_id` → `users.student_id`
   175	- 辅导员CSV：`employee_id` → `users.employee_id`
   176	- 班级映射CSV：`counselor_employee_id` → 查询 `users` 表中 `employee_id` 匹配的记录
   177	
   178	---
   179	
   180	#### 4.3 历史审批人一致性规则
   181	
   182	**问题：** 班级-辅导员映射变更后，已提交申请中的 `counselor_id` 是否自动改写？
   183	
   184	**我们的方案：** ✅ **不自动改写，保持历史一致性**
   185	
   186	<thinking>
   187	这是一个重要的业务规则。如果班级映射变更后自动改写已提交申请的审批人，会导致：
   188	1. 审批流程混乱（原审批人已审批，新审批人不知情）
   189	2. 审计追溯困难（无法还原当时的审批人是谁）
   190	3. 权限边界模糊（新审批人可能不应该看到旧申请）
   191	
   192	正确的做法是：
   193	1. 已提交的申请保持原审批人不变
   194	2. 新提交的申请使用新映射
   195	3. 如需改派，由管理员显式操作并记录审计日志
   196	</thinking>
   197	
   198	**理由：**
   199	
   200	1. **审批流程完整性：** 已提交申请的审批人是提交时确定的，不应因后续映射变更而改变
   201	2. **审计追溯：** 保持历史审批人记录，便于追溯当时的审批责任
   202	3. **权限边界：** 新辅导员不应自动获得旧申请的审批权限
   203	
   204	**具体规则：**
   205	
   206	| 场景 | 处理方式 |
   207	|------|----------|
   208	| 申请提交时 | 根据当前班级-辅导员映射确定 `counselor_id` |
   209	| 映射变更后，已提交申请 | `counselor_id` **不变**，保持原审批人 |
   210	| 映射变更后，新提交申请 | 使用新映射确定 `counselor_id` |
   211	| 需要改派审批人 | 管理员显式操作，记录审计日志（操作人、时间、原因） |
   212	
   213	**数据库设计支持：**
   214	- `applications` 表的 `counselor_id` 是快照字段，不关联外键级联更新
   215	- 审计日志表记录审批人变更操作
   216	
   217	---
   218	
   219	#### 4.4 多辅导员场景处理
   220	
   221	**问题：** 一个班级是否可能有多个辅导员？如何处理主辅导员、代理辅导员、临时负责人？
   222	
   223	**我们的方案：** 首版**不支持**多辅导员，后续根据实际需求扩展
   224	
   225	<thinking>
   226	多辅导员场景会增加系统复杂度：
   227	1. 数据模型需要支持一对多关系
   228	2. 审批流程需要确定主审批人
   229	3. 权限边界需要明确（所有辅导员都能审批？还是只有主辅导员？）
   230	4. 通知逻辑需要调整（通知所有辅导员？还是只通知主辅导员？）

exec
/bin/bash -lc "rtk nl -ba docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md | sed -n '231,430p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   231	
   232	首版应该简化，采用一班一主辅导员的模型。如果实际运行中发现确实需要多辅导员支持，再扩展。
   233	</thinking>
   234	
   235	**首版限制：**
   236	1. 一个班级只能映射一个辅导员（主辅导员）
   237	2. 班级-辅导员映射表中，`class_id` 必须唯一
   238	3. CSV导入时强校验：同一 `class_id` 不能出现多次
   239	
   240	**如果实际存在多辅导员场景：**
   241	
   242	| 场景 | 首版处理方式 |
   243	|------|-------------|
   244	| 一班多辅导员 | 只导入主辅导员，其他辅导员不导入 |
   245	| 代理辅导员 | 临时修改班级映射，指向代理辅导员 |
   246	| 辅导员调岗 | 更新班级映射，新申请使用新辅导员 |
   247	
   248	**后续扩展方案（P1）：**
   249	
   250	如果实际需求强烈，可以扩展为：
   251	1. 班级-辅导员映射表增加 `is_primary` 字段（标识主辅导员）
   252	2. 允许同一 `class_id` 有多条记录，但只能有一个 `is_primary=true`
   253	3. 申请提交时使用主辅导员作为 `counselor_id`
   254	4. 所有辅导员都能查看本班申请，但只有主辅导员能审批
   255	
   256	**修改方案：** 在文档中明确说明首版只支持一班一主辅导员，并在待反馈问题中询问宿管系统是否存在多辅导员场景。
   257	
   258	---
   259	
   260	## 三、对其他审查意见的回应
   261	
   262	### 3.1 数据源完整性（第二章）
   263	
   264	**Codex结论：** P0数据源覆盖完整，未遗漏关键数据。
   265	
   266	**我们的回应：** ✅ **认同**
   267	
   268	同意以下判断：
   269	- 图书馆清书、财务结清、学籍状态不列为P0是合理的
   270	- 当前保留截图上传和人工审核的降级方案
   271	- 这些数据不应阻塞首版上线
   272	
   273	### 3.2 字段定义合理性（第三章）
   274	
   275	**Codex建议：**
   276	1. `is_graduating` 建议改名或补充为 `eligible_for_leave`
   277	2. `graduation_year` 示例应与当前项目日期保持一致（2026）
   278	3. `phone` 是否可选需要结合微信绑定策略确认
   279	
   280	**我们的回应：** 🔄 **部分接受**
   281	
   282	| 建议 | 我们的回应 |
   283	|------|-----------|
   284	| `is_graduating` 改名 | ❌ 首版保持不变，字段含义已明确 |
   285	| `graduation_year` 示例改为2026 | ✅ 接受，统一为2026 |
   286	| `phone` 可选性确认 | ✅ 接受，需要在待反馈问题中询问宿管系统 |
   287	
   288	**理由：**
   289	- `is_graduating` 字段名虽不完美，但首版已足够表达"是否为当届毕业生"
   290	- 延期毕业、结业等异常状态可以通过 `is_graduating=false` 排除
   291	- 如果后续需要更细粒度的状态，再扩展为 `graduation_status` 枚举
   292	
   293	### 3.3 对接方式可行性（第四章）
   294	
   295	**Codex建议：**
   296	1. DB直连需要安全边界清晰、只读视图
   297	2. API需补充分页、增量同步、错误码、限流、重试、幂等
   298	3. CSV需补充导入覆盖策略、重复数据处理、失败回滚
   299	
   300	**我们的回应：** ✅ **完全接受**
   301	
   302	这些都是技术实施的关键细节，需要在文档中补充。
   303	
   304	<thinking>
   305	Codex提出的这些技术要求都很合理，是实际对接时必须考虑的问题。我需要在回应中明确：
   306	1. 我们接受这些建议
   307	2. 说明如何在文档中补充这些内容
   308	3. 给出具体的补充方案
   309	</thinking>
   310	
   311	**补充方案：**
   312	
   313	在文档"三、数据源详细说明"的每个数据源章节中，增加"技术要求"小节：
   314	
   315	**DB直连技术要求：**
   316	- 只读账号，不得有写权限
   317	- 使用只读视图或同步库，不直接访问生产业务表
   318	- IP白名单限制，只允许应用服务器访问
   319	- 连接池配置：最大连接数、超时时间、重试策略
   320	
   321	**API技术要求：**
   322	- 分页支持：每页最多100条，支持 `page`/`page_size` 参数
   323	- 增量同步：支持 `updated_after` 参数，只返回指定时间后更新的数据
   324	- 错误码规范：200成功、400参数错误、401认证失败、500服务器错误
   325	- 限流策略：每分钟最多60次请求
   326	- 重试机制：失败后指数退避重试，最多3次
   327	- 幂等性：同一请求多次调用结果一致
   328	
   329	**CSV技术要求：**
   330	- 导入策略：首版采用**全量覆盖**（清空后重新导入）
   331	- 重复数据：按主键（学号/工号/班级ID）去重，保留最后一条
   332	- 失败处理：导入前备份，失败后回滚到备份
   333	- 校验报告：导入后生成校验报告（成功数、失败数、错误明细）
   334	
   335	### 3.4 数据量估算（第五章）
   336	
   337	**Codex意见：** 当前估算基本合理，但需要明确是"当届毕业生"还是"全部学生"。
   338	
   339	**我们的回应：** ✅ **接受，需要明确**
   340	
   341	<thinking>
   342	数据量估算需要明确两个问题：
   343	1. 系统是只服务当届毕业生（约1000人），还是保留多届历史数据（约10000人）？
   344	2. 班级映射数量是否考虑了历史有效期和多辅导员场景？
   345	
   346	这会影响数据库容量设计和性能优化策略。
   347	</thinking>
   348	
   349	**明确说明：**
   350	
   351	| 数据项 | 首版范围 | 容量设计 | 说明 |
   352	|--------|----------|----------|------|
   353	| 学生账号 | 当届毕业生 | 1000人/届 | 只导入当届，历史届别不保留 |
   354	| 系统容量 | 支持多届历史 | 10000人 | 数据库设计按10000人容量 |
   355	| 辅导员账号 | 当前在职 | 50人 | 离职辅导员标记 `is_active=false` |
   356	| 班级映射 | 当届有效映射 | 50-100条 | 首版不考虑历史有效期 |
   357	| 学工部管理员 | 当前在职 | 5人 | 手动创建 |
   358	
   359	**待反馈问题补充：**
   360	- 宿管系统能否只提供当届毕业生数据？
   361	- 是否需要保留历史届别数据用于查询和统计？
   362	
   363	### 3.5 待反馈问题（第六章）
   364	
   365	**Codex建议：** 扩展为面向多方的数据确认清单，新增12个问题。
   366	
   367	**我们的回应：** 🔄 **部分接受，需要调整**
   368	
   369	基于项目约束（只对接宿管系统），我们接受Codex建议的问题方向，但需要调整提问对象和表述。
   370	
   371	**修改方案：**
   372	
   373	将Codex建议的12个问题调整为"向宿管系统确认的问题清单"：
   374	
   375	**数据可用性确认：**
   376	1. 宿管系统数据库是否包含学生基本信息、辅导员信息、班级-辅导员映射？
   377	2. 如不包含，能否从教务/人事/学工系统归集后提供？
   378	3. 能否只提供当届毕业生数据（约1000人），还是必须提供全部学生数据？
   379	
   380	**字段和标识确认：**
   381	4. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
   382	5. 辅导员工号（`employee_id`）是否全校唯一？是否与统一身份认证、人事系统工号一致？
   383	6. 学生是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
   384	
   385	**多辅导员场景确认：**
   386	7. 是否存在一个班级多个辅导员、代理辅导员、临时负责人或辅导员调岗场景？
   387	8. 班级-辅导员映射变更频率如何？是否能提供当前有效映射和历史有效期？
   388	
   389	**对接方式确认：**
   390	9. 优先推荐的对接方式是什么？（DB直连 / API / CSV导入）
   391	10. 各数据源能否提供测试数据、测试环境和字段字典？
   392	11. CSV导入时采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
   393	
   394	**异常处理确认：**
   395	12. 外部系统不可用、数据延迟或查询失败时，业务上允许怎样的人工降级？
   396	13. 是否有统一身份认证或微信绑定前置要求？
   397	14. 是否需要导入手机号/邮箱用于找回密码或二次验证？
   398	
   399	**实施保障确认：**
   400	15. 数据提供方能否承诺导出频率、数据更新时间、联系人和故障响应时间？
   401	
   402	### 3.6 实施建议（第七章）
   403	
   404	**Codex建议：** 调整推荐方案和实施路径。
   405	
   406	**我们的回应：** ✅ **完全接受**
   407	
   408	<thinking>
   409	Codex建议的实施路径非常合理：
   410	1. 先确认数据权责方和联系人
   411	2. 先落地CSV模板
   412	3. 实现导入校验报告
   413	4. 再对接宿舍清退API
   414	5. 上线前冻结数据批次
   415	
   416	这个路径符合敏捷开发的原则：先简单后复杂，先验证后扩展。
   417	</thinking>
   418	
   419	**修改后的实施路径：**
   420	
   421	**阶段1：数据确认（1周）**
   422	1. 向宿管系统提交本需求文档
   423	2. 确认数据可用性、字段定义、对接方式
   424	3. 获取测试数据和字段字典
   425	4. 明确联系人和故障响应方式
   426	
   427	**阶段2：CSV导入实现（2周）**
   428	1. 设计三份CSV模板：学生、辅导员、班级-辅导员映射
   429	2. 实现CSV导入功能和校验逻辑
   430	3. 生成导入校验报告（成功数、失败数、错误明细）

exec
/bin/bash -lc "rtk nl -ba docs/discussions/codex-review-2026-05-27/21-final-consensus.md | sed -n '30,95p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
    30	#### 1.1 修正SQL示例为PostgreSQL语法
    31	
    32	**当前问题：** 设计文档声明PostgreSQL，但SQL示例用MySQL语法
    33	
    34	**修改位置：** `docs/design/2026-05-27-system-design.md` 第2章
    35	
    36	**修改内容：**
    37	```sql
    38	-- 错误（MySQL）
    39	CREATE TABLE users (
    40	    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    41	    name VARCHAR(50) NOT NULL COMMENT '姓名',
    42	    ...
    43	) COMMENT='用户表';
    44	
    45	-- 正确（PostgreSQL）
    46	CREATE TABLE users (
    47	    id BIGSERIAL PRIMARY KEY,
    48	    name VARCHAR(50) NOT NULL,
    49	    ...
    50	);
    51	COMMENT ON TABLE users IS '用户表';
    52	COMMENT ON COLUMN users.name IS '姓名';
    53	```
    54	
    55	或标注：
    56	```
    57	以下SQL为概念示例，实际以Django Model为准
    58	```
    59	
    60	#### 1.2 删除"多数据库支持"残留
    61	
    62	**修改位置：**
    63	- `docs/PROJECT-SUMMARY.md`
    64	- `docs/superpowers/plans/2026-05-27-implementation-plan.md`
    65	
    66	**修改内容：**
    67	```diff
    68	- 支持多数据库（MySQL/PostgreSQL/SQL Server/Oracle）
    69	+ 本项目使用PostgreSQL；外部系统通过API对接
    70	```
    71	
    72	#### 1.3 修正外键约束冲突
    73	
    74	**当前问题：** `NOT NULL` + `ON DELETE SET NULL` 冲突
    75	
    76	**修改位置：** `docs/design/2026-05-27-system-design.md` 第2章
    77	
    78	**修改内容：**
    79	```sql
    80	-- 错误
    81	approver_id BIGINT NOT NULL,
    82	FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE SET NULL
    83	
    84	-- 正确（历史数据用PROTECT）
    85	approver_id BIGINT,
    86	FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE PROTECT
    87	```
    88	
    89	#### 1.4 清理第6章合并残留
    90	
    91	**修改位置：** `docs/design/2026-05-27-system-design.md` 第6章
    92	
    93	**修改内容：** 删除缩进错乱的Python代码残留，修正重复编号
    94	
    95	#### 1.5 统一工作日时限口径

exec
/bin/bash -lc "rtk nl -ba docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md | sed -n '1,170p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1	# 数据源完整性审查与建议
     2	
     3	**审查时间：** 2026-05-27  
     4	**审查对象：** `29-data-source-analysis.md`、`docs/数据对接说明文档.md`、用户设计说明书、系统设计文档  
     5	
     6	---
     7	
     8	## 一、总体结论
     9	
    10	`29-data-source-analysis.md` 的方向是正确的：当前数据对接文档只覆盖宿舍清退，无法完整支撑 student、counselor、admin 三类角色的账号初始化、权限边界和自动审批分配。
    11	
    12	需要调整的重点有两点：
    13	
    14	1. **班级-辅导员对应关系应明确列为 P0。** 这是自动分配审批人的核心数据。没有它，系统提交申请时无法稳定设置 `counselor_id` 和 `current_approver_id`，只能退化为人工逐个配置或人工改派。
    15	2. **首版不应追求所有数据源 API 化。** 对约 1000 名学生、约 50 名辅导员、约 5 名管理员的规模，CSV/Excel 批量导入加严格校验更现实；API 更适合作为后续自动化增强。
    16	
    17	---
    18	
    19	## 二、优先级分类
    20	
    21	### P0：上线必须具备
    22	
    23	| 数据源 | 来源系统 | P0 判定 | 原因 |
    24	|--------|----------|---------|------|
    25	| 学生基本信息 | 教务系统 | P0 | 用于创建学生账号、身份识别、展示院系专业班级、限定毕业离校申请人范围。用户设计说明书已出现“学号、姓名、专业、班级”和“批量导入学生用户”的要求，因此必须写入数据对接文档。 |
    26	| 辅导员基本信息 | 人事系统或人工台账 | P0 | 用于创建 counselor 账号和审批权限主体。实时同步不是 P0，但账号数据本身是 P0。 |
    27	| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
    28	| 宿舍清退数据 | 宿管系统 | P0 | 当前业务把宿舍清退作为提交前校验项，现有对接文档已覆盖。即使保留人工证明降级，正式流程仍应具备自动校验或批量数据导入能力。 |
    29	| 毕业资格/离校资格字段 | 教务系统 | P0 字段，非 P0 独立接口 | 如果系统只导入当届毕业生，可通过导入范围满足；如果导入全量学生，则必须在学生基本信息中带 `graduation_year`、`graduation_status` 或 `eligible_for_leave`。不建议首版单独建设学籍 API。 |
    30	
    31	### P1：可选增强
    32	
    33	| 数据源 | 来源系统 | P1 判定 | 原因 |
    34	|--------|----------|---------|------|
    35	| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
    36	| 图书馆清书状态 | 图书馆系统 | P1 | 当前已有上传截图的人工方案。接口集成能降低审核成本和伪造风险，但不应阻塞首版上线。 |
    37	| 财务结清状态 | 财务系统 | P1 | 当前已有上传截图的人工方案。由于财务状态更敏感，若后续接口条件成熟，优先级可高于图书馆，但仍不是首版 P0。 |
    38	| 独立学籍状态接口 | 教务系统 | P1 | 只有在多届学生并行、延期毕业、结业/退学实时变化等需求明确时，才需要独立 API。首版可并入学生基础数据。 |
    39	
    40	---
    41	
    42	## 三、对接方式建议
    43	
    44	| 数据源 | 推荐方式 | 备选方式 | 关键建议 |
    45	|--------|----------|----------|----------|
    46	| 学生基本信息 | CSV/Excel 批量导入 | 教务系统 API | 首版按毕业届别导入更容易落地。字段建议包括 `student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
    47	| 辅导员基本信息 | CSV/Excel 批量导入 | 人事系统 API 或手动创建 | 约 50 人规模下，批量导入足够。字段建议包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API。 |
    48	| 班级-辅导员对应关系 | CSV/Excel 批量导入并强校验 | 教务系统 API | 必须优先支持。建议用 `class_id + counselor_employee_id + effective_term` 表达关系，不要只靠 `class_name`。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无审批人的学生数。 |
    49	| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入、人工证明降级 | 当前文档策略合理。提交申请时实时性较强，API 价值高；若宿管系统暂不支持 API，则每日文件导入加人工证明降级。 |
    50	| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
    51	| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 后续对接时只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，不要引入借阅明细。 |
    52	| 财务结清状态 | 首版手动上传截图 | API 优先于 CSV | 后续对接时只返回是否结清和结清日期，不同步欠费明细；外部系统失败时保留人工审核通道。 |
    53	| 学籍/毕业资格 | 并入学生基本信息导入 | 教务系统 API | 首版不要单独拆接口。若后续存在延期毕业、结业、退学状态的实时变更，再建设独立同步。 |
    54	
    55	---
    56	
    57	## 四、对五个核心问题的直接回答
    58	
    59	### 1. 学生基本信息是否需要写入数据对接文档？
    60	
    61	需要，且应列为 P0。
    62	
    63	原因不是“方便展示”，而是学生账号、身份识别、申请资格、班级映射都依赖它。当前数据对接文档的目标用户也应从“宿舍管理系统管理员”扩展为“教务系统、人事系统、宿管系统及业务数据负责人”。
    64	
    65	### 2. 辅导员数据源如何对接？
    66	
    67	首版推荐 CSV/Excel 批量导入，不推荐一开始就要求人事系统 API。
    68	
    69	理由是辅导员规模约 50 人，变化频率低，API 改造投入可能高于收益。但数据结构必须标准化，尤其是 `employee_id` 要能被班级-辅导员映射引用。若学校已有成熟 HR API 或统一身份平台，可在后续升级为 API 同步。
    70	
    71	### 3. 班级-辅导员对应关系是否应为 P0？
    72	
    73	应为 P0，而且是当前缺口中风险最高的数据源。
    74	
    75	它直接影响：
    76	
    77	- 学生提交时能否自动设置辅导员审批人；
    78	- 辅导员是否只能查看和审批负责班级；
    79	- 待办通知能否准确发送；
    80	- 审批统计能否按院系、班级、辅导员追踪。
    81	
    82	建议数据对接文档单独增加“审批关系数据”章节，并把导入覆盖率 100% 作为上线验收条件之一。
    83	
    84	### 4. 学工部管理员数据源是否需要对接？
    85	
    86	不建议做外部数据对接，手动创建即可。
    87	
    88	约 5 人的规模下，真正重要的是权限授予、停用、密码重置、操作审计，而不是与人事系统同步。文档应说明由系统管理员在后台维护，不应把它列为 P0 数据接口。
    89	
    90	### 5. 图书馆、财务、学籍是否需要对接？
    91	
    92	图书馆和财务可保持 P1。首版延续截图上传和人工审核，后续按审核量、造假风险、外部系统接口成熟度决定是否对接。若只能先选一个，建议先评估财务结清状态，因为财务数据的业务风险通常高于图书馆清书。
    93	
    94	学籍状态不建议作为首版独立接口，但毕业资格字段必须进入学生基础数据。换句话说，“是否允许提交离校申请”必须有数据依据，只是不一定需要实时 API。
    95	
    96	---
    97	
    98	## 五、遗漏或需补充考虑的数据项
    99	
   100	1. **班级唯一标识。** 当前分析偏向 `class_name`，但班级名称可能重复、改名或跨届复用。应要求 `class_id`，`class_name` 只用于展示。
   101	
   102	2. **组织架构数据。** 院系、专业、年级不仅用于展示，也用于权限过滤、统计导出、异常排查。首版可随学生和辅导员数据导入，不必单独做组织架构接口。
   103	
   104	3. **账号生命周期。** 需要定义新增、更新、停用、毕业归档、辅导员离职/调岗、管理员离岗后的处理规则。
   105	
   106	4. **导入校验和差异报告。** P0 数据导入不能只要求字段格式，还应要求失败明细、重复数据处理、覆盖策略、回滚策略和导入审计日志。
   107	
   108	5. **审批人变更后的历史一致性。** 已提交申请中的 `counselor_id` 应保持历史一致，不应因后续班级映射变更自动改写。若需改派，应由管理员显式操作并记录审计日志。
   109	
   110	6. **多辅导员和代理审批。** 现实中可能有主辅导员、代管辅导员、临时代理。首版可只要求一个主审批人，但后台应预留人工改派能力。
   111	
   112	7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
   113	
   114	8. **离校批次配置。** 开放申请时间、允许离校日期范围、毕业届别可能来自业务配置，而不一定来自教务系统。应作为系统配置纳入实施计划。
   115	
   116	9. **通知联系方式。** `phone`、`email` 对提醒和异常联系有价值；微信 `openid` 应通过用户绑定产生，不应从外部系统导入。
   117	
   118	10. **数据最小化。** 不应为了校验引入身份证号、欠费明细、借阅明细等高敏字段。业务校验只需要结论、日期、来源更新时间和必要的学生标识。
   119	
   120	11. **外部系统不可用时的降级口径。** 需要区分“学生确未完成”“外部系统失败”“系统数据过期”“人工证明待审核”，避免所有异常都被误判为不通过。
   121	
   122	---
   123	
   124	## 六、建议实施顺序
   125	
   126	1. **重构数据对接说明文档目录。** 从单一“宿舍对接”扩展为“账号基础数据、审批关系数据、业务校验数据、降级与审计”四类。
   127	
   128	2. **定义学生基本信息导入模板。** 先支持 CSV/Excel 导入当届毕业生，包含毕业资格字段和班级唯一标识。
   129	
   130	3. **定义辅导员基本信息导入模板。** 先确保 counselor 账号存在，且 `employee_id` 可被映射数据引用。
   131	
   132	4. **实现班级-辅导员映射导入。** 这是最关键步骤。上线前必须校验当届学生 100% 能解析到有效辅导员，否则不应开放提交。
   133	
   134	5. **保留并完善宿舍清退对接。** 当前文档已较完整，下一步应把它纳入统一的校验结果、缓存、失败降级和审计机制。
   135	
   136	6. **手动创建学工部管理员。** 同时补充管理员账号维护和终审人分配规则。
   137	
   138	7. **将毕业资格并入学生数据。** 首版不单独做学籍接口；后续根据延期毕业、多届并行等场景再升级。
   139	
   140	8. **评估财务与图书馆接口。** 首版继续截图上传。若后续审核量大或截图可信度不足，优先财务，再图书馆。
   141	
   142	9. **补齐运营治理能力。** 包括导入审计、失败重试、差异报表、外部数据更新时间展示、人工改派、人工审核日志。
   143	
   144	---
   145	
   146	## 七、建议修改数据对接文档的最小范围
   147	
   148	为了避免文档一次性扩得过大，建议先补充以下最小内容：
   149	
   150	1. 新增“学生基本信息导入”章节，提供 CSV/Excel 模板字段。
   151	2. 新增“辅导员基本信息导入”章节，明确 `employee_id`、联系方式和账号状态。
   152	3. 新增“班级-辅导员对应关系导入”章节，列为 P0，并写明覆盖率和异常报告要求。
   153	4. 将“宿舍清退数据”保留为业务校验数据，并补充与人工证明降级的关系。
   154	5. 在附录中增加三份模板：学生基础数据、辅导员基础数据、班级-辅导员映射。
   155	
   156	---
   157	
   158	## 八、最终建议
   159	
   160	同意 `29-data-source-analysis.md` 对主要缺失数据源的识别，但建议将结论进一步收敛为：
   161	
   162	- **P0 数据：** 学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据、毕业资格字段。
   163	- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
   164	- **首版策略：** 账号和映射数据用 CSV/Excel 批量导入，宿舍清退优先 API，管理员手动维护，图书馆/财务继续截图上传。
   165	- **最高优先级行动：** 立即补充班级-辅导员映射的数据规范和导入校验，这是自动审批闭环的关键缺口。
   166	

exec
/bin/bash -lc "rtk nl -ba docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md | sed -n '430,570p'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   430	3. 生成导入校验报告（成功数、失败数、错误明细）
   431	4. 重点校验：学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射
   432	
   433	**阶段3：宿舍清退API对接（1周）**
   434	1. 对接宿管系统宿舍清退API
   435	2. 实现API失败、超时、数据过期的降级处理
   436	3. 测试API异常场景和人工证明流程
   437	
   438	**阶段4：上线前验收（1周）**
   439	1. 冻结当届数据批次
   440	2. 完成一次全量导入演练
   441	3. 清零异常清单（无效学号、无效工号、未映射班级）
   442	4. 确认终审管理员配置
   443	
   444	**阶段5：上线后优化（按需）**
   445	1. 根据数据变更频率决定是否升级为API/DB同步
   446	2. 根据实际需求决定是否支持多辅导员场景
   447	
   448	---
   449	
   450	## 四、总结和下一步行动
   451	
   452	### 4.1 回应总结
   453	
   454	**完全接受的建议（✅）：**
   455	1. 对接方式从"DB优先"改为"CSV/Excel首版优先，API/DB增强"
   456	2. `checkout_status` 改为必填，增加枚举值
   457	3. 补充终审管理员分配规则
   458	4. 补充账号标识映射方案（新增 `employee_id` 字段）
   459	5. 明确历史审批人一致性规则（不自动改写）
   460	6. 明确首版不支持多辅导员场景
   461	7. 补充DB/API/CSV的技术要求细节
   462	8. 明确数据量估算范围（当届毕业生）
   463	9. 扩展待反馈问题清单
   464	10. 调整实施路径（CSV优先，分阶段实施）
   465	
   466	**不接受的建议（❌）：**
   467	1. 将反馈对象从"宿管系统"改为"多方数据负责人"
   468	   - 理由：项目只对接宿管系统，不直接对接教务/人事/学工
   469	
   470	**部分接受的建议（🔄）：**
   471	1. `is_graduating` 改名：首版保持不变，后续根据需要扩展
   472	2. 待反馈问题：接受问题方向，但调整为"向宿管系统确认"
   473	
   474	### 4.2 需要修改的具体内容
   475	
   476	基于上述回应，我们需要对 `31-data-source-requirements-consensus.md` 进行以下修改：
   477	
   478	**修改1：数据源概述表（第二章）**
   479	- 调整对接方式优先级：学生/辅导员/班级映射改为"CSV/Excel首版优先"
   480	
   481	**修改2：学生基本信息（第三章）**
   482	- `graduation_year` 示例从2024改为2026
   483	- 补充说明：`is_graduating=true` 表示具备本批次离校申请资格
   484	
   485	**修改3：宿舍清退数据（第三章）**
   486	- `checkout_status` 改为必填，增加枚举值说明
   487	- `checkout_date` 改为条件必填
   488	- 新增 `source_updated_at` 字段（建议）
   489	
   490	**修改4：辅导员基本信息（第三章）**
   491	- 补充说明：`employee_id` 必须全校唯一
   492	- 补充说明：`is_active=false` 时的处理规则
   493	
   494	**修改5：班级-辅导员对应关系（第三章）**
   495	- 补充说明：首版只支持一班一主辅导员
   496	- 补充说明：`class_id` 必须唯一，不允许重复
   497	
   498	**修改6：对接方式（第四章）**
   499	- 每个数据源增加"技术要求"小节
   500	- 补充DB/API/CSV的具体技术要求
   501	
   502	**修改7：数据量估算（第五章）**
   503	- 明确说明：学生数据只包含当届毕业生（约1000人）
   504	- 明确说明：系统容量设计按10000人
   505	
   506	**修改8：待反馈问题（第七章）**
   507	- 扩展为15个问题的确认清单
   508	- 增加"数据可用性确认"、"字段和标识确认"、"多辅导员场景确认"等分类
   509	
   510	**修改9：实施建议（第七章）**
   511	- 调整推荐方案：CSV首版优先
   512	- 补充分阶段实施路径（5个阶段）
   513	
   514	**修改10：新增章节**
   515	- 新增"终审管理员配置"章节
   516	- 新增"账号标识映射方案"章节
   517	- 新增"历史审批人一致性规则"章节
   518	- 新增"多辅导员场景说明"章节
   519	
   520	### 4.3 下一步行动
   521	
   522	**立即行动（本次讨论）：**
   523	1. ✅ 已完成：生成本回应文档（33-response-to-codex-data-review.md）
   524	2. 待Codex确认：Codex审查本回应文档，确认我们的理解和方案是否合理
   525	3. 达成共识：基于Codex反馈，形成最终共识
   526	
   527	**后续行动（共识达成后）：**
   528	1. 创建修订版文档：`31-data-source-requirements-consensus-v2.md`
   529	2. 按照4.2节的修改清单逐项修改
   530	3. 提交给宿管系统方反馈
   531	4. 根据宿管系统反馈调整方案
   532	5. 启动实施（按3.6节的5阶段路径）
   533	
   534	### 4.4 需要Codex进一步确认的问题
   535	
   536	<thinking>
   537	我需要列出一些需要Codex进一步确认的问题，特别是我们不接受或部分接受的建议，需要Codex的反馈。
   538	</thinking>
   539	
   540	1. **项目约束确认：** 我们明确项目只对接宿管系统，不直接对接教务/人事/学工。Codex是否认同这个约束下，原文档的反馈对象（宿管系统方）是正确的？
   541	
   542	2. **账号标识映射方案：** 我们提出新增 `employee_id` 字段的方案。Codex是否认同这个方案？是否有更好的替代方案？
   543	
   544	3. **多辅导员场景：** 我们提出首版不支持多辅导员，后续根据需求扩展。Codex是否认同这个策略？是否建议首版就支持？
   545	
   546	4. **实施路径：** 我们接受了CSV首版优先的建议，并补充了5阶段实施路径。Codex是否认同这个路径？是否有需要调整的地方？
   547	
   548	5. **字段定义：** 我们保持 `is_graduating` 字段名不变。Codex是否认同首版保持不变的策略？
   549	
   550	---
   551	
   552	## 五、结语
   553	
   554	感谢Codex的详细审查和建设性建议。本回应文档明确了我们的立场：
   555	
   556	- **核心约束：** 项目只对接宿管系统
   557	- **接受建议：** CSV首版优先、字段定义统一、补充实施细节
   558	- **保持立场：** 反馈对象为宿管系统方
   559	
   560	期待Codex对本回应文档的反馈，以便我们达成最终共识，推进数据对接工作。
   561	

exec
/bin/bash -lc 'rtk rg -n "class_id|class_name|grade|employee_id|username|student_id" docs/templates docs/design/2026-05-27-system-design.md docs/数据对接说明文档.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/数据对接说明文档.md:67:| student_id | String | 是 | 学号 | "2020010101" |
docs/数据对接说明文档.md:72:GET /api/dorm/checkout/status?student_id=2020010101&name=张三
docs/数据对接说明文档.md:85:  "student_id": "2020010101",
docs/数据对接说明文档.md:104:| student_id | String | 学号 | "2020010101" |
docs/数据对接说明文档.md:106:| class_name | String | 班级（可选） | "计算机2020级1班" |
docs/数据对接说明文档.md:121:    "student_id": "2020010101",
docs/数据对接说明文档.md:123:    "class_name": "计算机2020级1班",
docs/数据对接说明文档.md:141:    "student_id": "2020010101",
docs/数据对接说明文档.md:143:    "class_name": "计算机2020级1班",
docs/数据对接说明文档.md:200:curl -X GET "http://dorm-test.example.com/api/dorm/checkout/status?student_id=2020010101" \
docs/数据对接说明文档.md:222:| 学号 | student_id | 文本 | 是 | 学生学号 | 2020010101 |
docs/数据对接说明文档.md:224:| 班级 | class_name | 文本 | 否 | 学生班级 | 计算机2020级1班 |
docs/数据对接说明文档.md:335:| 参数缺失 | 不传student_id | 返回错误码1002 |
docs/design/2026-05-27-system-design.md:262:    student_id VARCHAR(20) UNIQUE NOT NULL COMMENT '学号',
docs/design/2026-05-27-system-design.md:281:    class_name VARCHAR(50) COMMENT '班级',
docs/design/2026-05-27-system-design.md:282:    grade INT COMMENT '年级',
docs/design/2026-05-27-system-design.md:288:    INDEX idx_student_id (student_id),
docs/design/2026-05-27-system-design.md:310:    student_id BIGINT NOT NULL COMMENT '学生ID',
docs/design/2026-05-27-system-design.md:335:    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:340:    INDEX idx_student_id (student_id),
docs/design/2026-05-27-system-design.md:347:    INDEX idx_student_status (student_id, status, created_at),
docs/design/2026-05-27-system-design.md:683:  "student_id": "2020001",
docs/design/2026-05-27-system-design.md:697:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:724:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:762:  "student_id": "2020001",
docs/design/2026-05-27-system-design.md:775:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:797:  "student_id": "2020001",
docs/design/2026-05-27-system-design.md:811:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:913:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:1288:    "student_id": "2020001",
docs/design/2026-05-27-system-design.md:1383:        return obj.student_id == request.user.id
docs/design/2026-05-27-system-design.md:1627:  student_id: 2020001
docs/design/2026-05-27-system-design.md:1633:    "student_id": "2020001",
docs/design/2026-05-27-system-design.md:1635:    "class_name": "计算机2020级1班",
docs/design/2026-05-27-system-design.md:1657:    def get_checkout_status(self, student_id):
docs/design/2026-05-27-system-design.md:1659:            f'{self.base_url}/api/students/{student_id}/checkout',
docs/design/2026-05-27-system-design.md:1679:    def verify_clearance(self, student_id):
docs/design/2026-05-27-system-design.md:1683:                params={"student_id": student_id},
docs/design/2026-05-27-system-design.md:1727:def verify_dorm_clearance(student_id):
docs/design/2026-05-27-system-design.md:1729:    return plugin.verify_clearance(student_id)
docs/design/2026-05-27-system-design.md:1982:def bind_wechat_to_account(student_id, wechat_openid, password):
docs/design/2026-05-27-system-design.md:1984:    user = User.objects.filter(student_id=student_id).first()
docs/design/2026-05-27-system-design.md:1990:            request_data={'student_id': student_id}
docs/design/2026-05-27-system-design.md:2338:CREATE INDEX idx_student_id ON users(student_id);
docs/design/2026-05-27-system-design.md:2344:CREATE INDEX idx_student_id ON applications(student_id);
docs/design/2026-05-27-system-design.md:2353:CREATE INDEX idx_student_status ON applications(student_id, status, created_at);
docs/design/2026-05-27-system-design.md:2464:    cache.delete(f'student:{app.student_id}:applications')
docs/design/2026-05-27-system-design.md:2604:    response = bind_wechat(student_id='2020001', openid='oXXX', password='wrong')
docs/design/2026-05-27-system-design.md:2630:    bind_wechat(student_id='2020001', openid='oXXX', password='pass')
docs/design/2026-05-27-system-design.md:2638:    r1 = bind_wechat(student_id='9999999', openid='oXXX', password='pass')
docs/design/2026-05-27-system-design.md:2640:    r2 = bind_wechat(student_id='2020001', openid='oXXX', password='wrong')
docs/design/2026-05-27-system-design.md:2642:    r3 = bind_wechat(student_id='2020002', openid='oXXX', password='pass')

codex
**结论：方向基本可以接受，但不建议原样进入 v2。主要还有 3 个需要修正的点。**

**发现**
1. [33-response-to-codex-data-review.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:329) 里的 CSV “全量覆盖（清空后重新导入）”有风险。`users` 会被 `applications.student_id/counselor_id/admin_id` 外键引用，不能清空重建。应改为：导入到 staging 表、校验通过后按主键 upsert、缺失记录软停用、保留导入批次和回滚点。
2. [33-response-to-codex-data-review.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:168) 新增 `employee_id` 方案可行，但当前系统设计里 `users.student_id` 是 `UNIQUE NOT NULL`，见 [system-design.md](/home/caohui/projects/graduation-leave-system/docs/design/2026-05-27-system-design.md:262)。若辅导员/管理员 `student_id` 为空，必须同步修改模型约束：`student_id` 可空且仅学生唯一，`employee_id` 可空且仅教职工唯一，并明确 `username`/登录账号如何生成。
3. [33-response-to-codex-data-review.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/33-response-to-codex-data-review.md:381) 你们要求 `class_id` 作为核心映射键是对的，但当前用户表设计只有 `class_name`，没有 `class_id`，见 [system-design.md](/home/caohui/projects/graduation-leave-system/docs/design/2026-05-27-system-design.md:279)。需要把 `class_id` 加入学生用户或学生档案，否则班级-辅导员映射无法稳定落地。

**逐项确认**
1. 项目约束“只对接宿管系统”作为系统集成边界是合理的。  
但文档不要写成“学生、辅导员、班级映射天然由宿管系统负责”。更准确的表述是：本系统只向宿管系统取数；宿管系统需作为数据归集和交付责任方，确认其是否能提供上游数据、字段字典、更新时间、联系人和故障响应。

2. 接受/不接受建议基本合理。  
不接受“直接面向多方反馈”可以成立；接受 CSV 优先、`checkout_status` 必填、历史审批人不自动改写都合理。`is_graduating` 首版保留也可以，但建议至少补一个业务语义说明：`is_graduating=true` 等同于“具备本批次离校申请资格”；更稳的是新增 `eligible_for_leave`。

3. 账号标识映射方案可行，但要补约束。  
推荐保留 `student_id` 和 `employee_id` 两列，不复用字段。需要明确：
`student_id` 仅学生必填；`employee_id` 仅 counselor/admin 必填；分别建条件唯一索引；班级映射只引用 counselor 的 `employee_id`；管理员也用 `employee_id` 但不参与班级映射。

4. 实施路径总体合理。  
建议在阶段 2 前增加“数据模型修订”：`employee_id`、`class_id`、导入批次表、默认终审人配置。CSV 导入阶段不能做物理清空，应做 staging + 校验 + upsert + 软停用。上线前验收还应加两条：所有可申请学生 100% 解析到有效辅导员；提交申请时 100% 能解析到有效终审人。

5. 仍遗漏的关键问题：
- 离校批次配置：毕业届别、开放时间、允许计划离校日期范围。
- 导入审计：上传人、文件哈希、批次号、差异报告、失败明细。
- 停用规则：学生毕业归档、辅导员离职/调岗、管理员离岗后的未完成任务处理。
- 默认终审人失效兜底：默认管理员被停用时禁止上线或阻断提交。
- 正式文档需删除所有 `<thinking>` 段落。

总体判断：可以基于这份回应形成共识，但 v2 修改时先修正“全量覆盖清空”、`employee_id` 约束、`class_id` 落库这三处，否则实施时会撞到数据一致性问题。
tokens used
71,737

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
