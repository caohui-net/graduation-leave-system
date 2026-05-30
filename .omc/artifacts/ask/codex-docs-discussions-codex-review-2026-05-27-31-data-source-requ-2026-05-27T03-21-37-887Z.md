# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-05-27T03:21:37.889Z

## Original task

请审查数据源需求共识文档，确认是否完整、合理。

**文档路径：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md

**审查重点：**

1. **数据源完整性**
   - P0数据源是否覆盖系统运行的所有必需数据？
   - 是否遗漏关键数据源？

2. **字段定义合理性**
   - 每个数据源的字段是否足够支撑业务需求？
   - 必填/可选字段划分是否合理？
   - 字段类型和示例是否准确？

3. **对接方式可行性**
   - DB直连、API、CSV三种方式的优先级是否合理？
   - 技术要求是否清晰？
   - 安全措施是否充分？

4. **数据量估算**
   - 学生~1000人、辅导员~50人、班级映射~50条是否合理？

5. **待反馈问题**
   - 向宿管系统方提出的问题是否全面？
   - 是否有遗漏的关键问题？

6. **实施建议**
   - 推荐方案和最小可行方案是否合理？
   - 是否有更好的实施路径？

**期望输出：**
1. 确认文档是否可以提交给用户
2. 指出需要修改或补充的地方
3. 提供具体的修改建议

请将审查结果保存为：docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md

## Final prompt

请审查数据源需求共识文档，确认是否完整、合理。

**文档路径：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md

**审查重点：**

1. **数据源完整性**
   - P0数据源是否覆盖系统运行的所有必需数据？
   - 是否遗漏关键数据源？

2. **字段定义合理性**
   - 每个数据源的字段是否足够支撑业务需求？
   - 必填/可选字段划分是否合理？
   - 字段类型和示例是否准确？

3. **对接方式可行性**
   - DB直连、API、CSV三种方式的优先级是否合理？
   - 技术要求是否清晰？
   - 安全措施是否充分？

4. **数据量估算**
   - 学生~1000人、辅导员~50人、班级映射~50条是否合理？

5. **待反馈问题**
   - 向宿管系统方提出的问题是否全面？
   - 是否有遗漏的关键问题？

6. **实施建议**
   - 推荐方案和最小可行方案是否合理？
   - 是否有更好的实施路径？

**期望输出：**
1. 确认文档是否可以提交给用户
2. 指出需要修改或补充的地方
3. 提供具体的修改建议

请将审查结果保存为：docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md

## Raw output

```text
已完成审查并保存到：

[32-codex-data-requirements-review.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md)

结论：`31` 文档方向正确，P0 数据源基本完整，但不建议原样提交。建议先修 5 点：

1. 反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
2. 学生、辅导员、班级映射首版对接方式从“DB 优先”调整为“CSV/Excel 优先，API/DB 增强”。
3. 统一宿舍清退字段必填性，尤其是 `checkout_status`。
4. 补充终审管理员/终审组配置、账号标识映射、历史审批人一致性规则。
5. 待反馈问题增加数据权责、测试数据、同步策略、异常降级、多辅导员场景确认。

本次只新增审查文档，未改原共识文档；不涉及代码测试。


OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019e6770-c784-7173-bb9b-528a08f780e2
--------
user
请审查数据源需求共识文档，确认是否完整、合理。

**文档路径：**
docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md

**审查重点：**

1. **数据源完整性**
   - P0数据源是否覆盖系统运行的所有必需数据？
   - 是否遗漏关键数据源？

2. **字段定义合理性**
   - 每个数据源的字段是否足够支撑业务需求？
   - 必填/可选字段划分是否合理？
   - 字段类型和示例是否准确？

3. **对接方式可行性**
   - DB直连、API、CSV三种方式的优先级是否合理？
   - 技术要求是否清晰？
   - 安全措施是否充分？

4. **数据量估算**
   - 学生~1000人、辅导员~50人、班级映射~50条是否合理？

5. **待反馈问题**
   - 向宿管系统方提出的问题是否全面？
   - 是否有遗漏的关键问题？

6. **实施建议**
   - 推荐方案和最小可行方案是否合理？
   - 是否有更好的实施路径？

**期望输出：**
1. 确认文档是否可以提交给用户
2. 指出需要修改或补充的地方
3. 提供具体的修改建议

请将审查结果保存为：docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
codex
我会先读取项目约定和目标文档，再对照现有需求/设计资料核查是否有遗漏，最后把审查结论写入指定的 `32-codex-data-requirements-review.md`。
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
/bin/bash -lc "sed -n '1,260p' docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md" in /home/caohui/projects/graduation-leave-system
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

exec
/bin/bash -lc "pwd && rg --files -g 'AGENTS.md' -g 'docs/**' -g '*.md'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
/home/caohui/projects/graduation-leave-system
docs/PROJECT-SUMMARY.md
docs/templates/宿舍清退数据模板.csv
docs/templates/学生基本信息导入模板.csv
docs/templates/班级辅导员对应关系导入模板.csv
docs/templates/辅导员基本信息导入模板.csv
docs/用户设计说明书.md
docs/superpowers/plans/2026-05-27-implementation-plan.md
docs/数据对接说明文档.md
docs/discussions/codex-review-2026-05-27/23-class-bed-field-codex-response.md
docs/design/2026-05-27-system-design.md
docs/discussions/codex-review-2026-05-27/11-remaining-sections-response.md
docs/discussions/codex-review-2026-05-27/13-round3-analysis-request.md
docs/discussions/codex-review-2026-05-27/21-final-consensus.md
docs/discussions/codex-review-2026-05-27/28-user-docs-consensus.md
docs/discussions/codex-review-2026-05-27/06-database-response-part2.md
docs/discussions/codex-review-2026-05-27/09-multi-db-clarification.md
docs/discussions/codex-review-2026-05-27/22-class-bed-field-review-request.md
docs/discussions/codex-review-2026-05-27/24-class-bed-field-claude-response.md
docs/discussions/codex-review-2026-05-27/08-database-confirmation.md
docs/discussions/codex-review-2026-05-27/17-completed-work-only-analysis.md
docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
docs/discussions/codex-review-2026-05-27/00-CONSENSUS-SUMMARY.md
docs/discussions/codex-review-2026-05-27/13-current-project-full-analysis.md
docs/discussions/codex-review-2026-05-27/01-architecture-review.md
docs/discussions/codex-review-2026-05-27/03-auth-review-round3.md
docs/discussions/codex-review-2026-05-27/07-database-response-part3.md
docs/discussions/codex-review-2026-05-27/27-user-docs-claude-response.md
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md
docs/discussions/codex-review-2026-05-27/19-claude-analysis-part6-summary.md
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

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 数据源完整性审查与建议

**审查时间：** 2026-05-27  
**审查对象：** `29-data-source-analysis.md`、`docs/数据对接说明文档.md`、用户设计说明书、系统设计文档  

---

## 一、总体结论

`29-data-source-analysis.md` 的方向是正确的：当前数据对接文档只覆盖宿舍清退，无法完整支撑 student、counselor、admin 三类角色的账号初始化、权限边界和自动审批分配。

需要调整的重点有两点：

1. **班级-辅导员对应关系应明确列为 P0。** 这是自动分配审批人的核心数据。没有它，系统提交申请时无法稳定设置 `counselor_id` 和 `current_approver_id`，只能退化为人工逐个配置或人工改派。
2. **首版不应追求所有数据源 API 化。** 对约 1000 名学生、约 50 名辅导员、约 5 名管理员的规模，CSV/Excel 批量导入加严格校验更现实；API 更适合作为后续自动化增强。

---

## 二、优先级分类

### P0：上线必须具备

| 数据源 | 来源系统 | P0 判定 | 原因 |
|--------|----------|---------|------|
| 学生基本信息 | 教务系统 | P0 | 用于创建学生账号、身份识别、展示院系专业班级、限定毕业离校申请人范围。用户设计说明书已出现“学号、姓名、专业、班级”和“批量导入学生用户”的要求，因此必须写入数据对接文档。 |
| 辅导员基本信息 | 人事系统或人工台账 | P0 | 用于创建 counselor 账号和审批权限主体。实时同步不是 P0，但账号数据本身是 P0。 |
| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
| 宿舍清退数据 | 宿管系统 | P0 | 当前业务把宿舍清退作为提交前校验项，现有对接文档已覆盖。即使保留人工证明降级，正式流程仍应具备自动校验或批量数据导入能力。 |
| 毕业资格/离校资格字段 | 教务系统 | P0 字段，非 P0 独立接口 | 如果系统只导入当届毕业生，可通过导入范围满足；如果导入全量学生，则必须在学生基本信息中带 `graduation_year`、`graduation_status` 或 `eligible_for_leave`。不建议首版单独建设学籍 API。 |

### P1：可选增强

| 数据源 | 来源系统 | P1 判定 | 原因 |
|--------|----------|---------|------|
| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
| 图书馆清书状态 | 图书馆系统 | P1 | 当前已有上传截图的人工方案。接口集成能降低审核成本和伪造风险，但不应阻塞首版上线。 |
| 财务结清状态 | 财务系统 | P1 | 当前已有上传截图的人工方案。由于财务状态更敏感，若后续接口条件成熟，优先级可高于图书馆，但仍不是首版 P0。 |
| 独立学籍状态接口 | 教务系统 | P1 | 只有在多届学生并行、延期毕业、结业/退学实时变化等需求明确时，才需要独立 API。首版可并入学生基础数据。 |

---

## 三、对接方式建议

| 数据源 | 推荐方式 | 备选方式 | 关键建议 |
|--------|----------|----------|----------|
| 学生基本信息 | CSV/Excel 批量导入 | 教务系统 API | 首版按毕业届别导入更容易落地。字段建议包括 `student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
| 辅导员基本信息 | CSV/Excel 批量导入 | 人事系统 API 或手动创建 | 约 50 人规模下，批量导入足够。字段建议包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API。 |
| 班级-辅导员对应关系 | CSV/Excel 批量导入并强校验 | 教务系统 API | 必须优先支持。建议用 `class_id + counselor_employee_id + effective_term` 表达关系，不要只靠 `class_name`。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无审批人的学生数。 |
| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入、人工证明降级 | 当前文档策略合理。提交申请时实时性较强，API 价值高；若宿管系统暂不支持 API，则每日文件导入加人工证明降级。 |
| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 后续对接时只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，不要引入借阅明细。 |
| 财务结清状态 | 首版手动上传截图 | API 优先于 CSV | 后续对接时只返回是否结清和结清日期，不同步欠费明细；外部系统失败时保留人工审核通道。 |
| 学籍/毕业资格 | 并入学生基本信息导入 | 教务系统 API | 首版不要单独拆接口。若后续存在延期毕业、结业、退学状态的实时变更，再建设独立同步。 |

---

## 四、对五个核心问题的直接回答

### 1. 学生基本信息是否需要写入数据对接文档？

需要，且应列为 P0。

原因不是“方便展示”，而是学生账号、身份识别、申请资格、班级映射都依赖它。当前数据对接文档的目标用户也应从“宿舍管理系统管理员”扩展为“教务系统、人事系统、宿管系统及业务数据负责人”。

### 2. 辅导员数据源如何对接？

首版推荐 CSV/Excel 批量导入，不推荐一开始就要求人事系统 API。

理由是辅导员规模约 50 人，变化频率低，API 改造投入可能高于收益。但数据结构必须标准化，尤其是 `employee_id` 要能被班级-辅导员映射引用。若学校已有成熟 HR API 或统一身份平台，可在后续升级为 API 同步。

### 3. 班级-辅导员对应关系是否应为 P0？

应为 P0，而且是当前缺口中风险最高的数据源。

它直接影响：

- 学生提交时能否自动设置辅导员审批人；
- 辅导员是否只能查看和审批负责班级；
- 待办通知能否准确发送；
- 审批统计能否按院系、班级、辅导员追踪。

建议数据对接文档单独增加“审批关系数据”章节，并把导入覆盖率 100% 作为上线验收条件之一。

### 4. 学工部管理员数据源是否需要对接？

不建议做外部数据对接，手动创建即可。

约 5 人的规模下，真正重要的是权限授予、停用、密码重置、操作审计，而不是与人事系统同步。文档应说明由系统管理员在后台维护，不应把它列为 P0 数据接口。

### 5. 图书馆、财务、学籍是否需要对接？

图书馆和财务可保持 P1。首版延续截图上传和人工审核，后续按审核量、造假风险、外部系统接口成熟度决定是否对接。若只能先选一个，建议先评估财务结清状态，因为财务数据的业务风险通常高于图书馆清书。

学籍状态不建议作为首版独立接口，但毕业资格字段必须进入学生基础数据。换句话说，“是否允许提交离校申请”必须有数据依据，只是不一定需要实时 API。

---

## 五、遗漏或需补充考虑的数据项

1. **班级唯一标识。** 当前分析偏向 `class_name`，但班级名称可能重复、改名或跨届复用。应要求 `class_id`，`class_name` 只用于展示。

2. **组织架构数据。** 院系、专业、年级不仅用于展示，也用于权限过滤、统计导出、异常排查。首版可随学生和辅导员数据导入，不必单独做组织架构接口。

3. **账号生命周期。** 需要定义新增、更新、停用、毕业归档、辅导员离职/调岗、管理员离岗后的处理规则。

4. **导入校验和差异报告。** P0 数据导入不能只要求字段格式，还应要求失败明细、重复数据处理、覆盖策略、回滚策略和导入审计日志。

5. **审批人变更后的历史一致性。** 已提交申请中的 `counselor_id` 应保持历史一致，不应因后续班级映射变更自动改写。若需改派，应由管理员显式操作并记录审计日志。

6. **多辅导员和代理审批。** 现实中可能有主辅导员、代管辅导员、临时代理。首版可只要求一个主审批人，但后台应预留人工改派能力。

7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。

8. **离校批次配置。** 开放申请时间、允许离校日期范围、毕业届别可能来自业务配置，而不一定来自教务系统。应作为系统配置纳入实施计划。

9. **通知联系方式。** `phone`、`email` 对提醒和异常联系有价值；微信 `openid` 应通过用户绑定产生，不应从外部系统导入。

10. **数据最小化。** 不应为了校验引入身份证号、欠费明细、借阅明细等高敏字段。业务校验只需要结论、日期、来源更新时间和必要的学生标识。

11. **外部系统不可用时的降级口径。** 需要区分“学生确未完成”“外部系统失败”“系统数据过期”“人工证明待审核”，避免所有异常都被误判为不通过。

---

## 六、建议实施顺序

1. **重构数据对接说明文档目录。** 从单一“宿舍对接”扩展为“账号基础数据、审批关系数据、业务校验数据、降级与审计”四类。

2. **定义学生基本信息导入模板。** 先支持 CSV/Excel 导入当届毕业生，包含毕业资格字段和班级唯一标识。

3. **定义辅导员基本信息导入模板。** 先确保 counselor 账号存在，且 `employee_id` 可被映射数据引用。

4. **实现班级-辅导员映射导入。** 这是最关键步骤。上线前必须校验当届学生 100% 能解析到有效辅导员，否则不应开放提交。

5. **保留并完善宿舍清退对接。** 当前文档已较完整，下一步应把它纳入统一的校验结果、缓存、失败降级和审计机制。

6. **手动创建学工部管理员。** 同时补充管理员账号维护和终审人分配规则。

7. **将毕业资格并入学生数据。** 首版不单独做学籍接口；后续根据延期毕业、多届并行等场景再升级。

8. **评估财务与图书馆接口。** 首版继续截图上传。若后续审核量大或截图可信度不足，优先财务，再图书馆。

9. **补齐运营治理能力。** 包括导入审计、失败重试、差异报表、外部数据更新时间展示、人工改派、人工审核日志。

---

## 七、建议修改数据对接文档的最小范围

为了避免文档一次性扩得过大，建议先补充以下最小内容：

1. 新增“学生基本信息导入”章节，提供 CSV/Excel 模板字段。
2. 新增“辅导员基本信息导入”章节，明确 `employee_id`、联系方式和账号状态。
3. 新增“班级-辅导员对应关系导入”章节，列为 P0，并写明覆盖率和异常报告要求。
4. 将“宿舍清退数据”保留为业务校验数据，并补充与人工证明降级的关系。
5. 在附录中增加三份模板：学生基础数据、辅导员基础数据、班级-辅导员映射。

---

## 八、最终建议

同意 `29-data-source-analysis.md` 对主要缺失数据源的识别，但建议将结论进一步收敛为：

- **P0 数据：** 学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据、毕业资格字段。
- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
- **首版策略：** 账号和映射数据用 CSV/Excel 批量导入，宿舍清退优先 API，管理员手动维护，图书馆/财务继续截图上传。
- **最高优先级行动：** 立即补充班级-辅导员映射的数据规范和导入校验，这是自动审批闭环的关键缺口。


exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 数据源完整性分析

**分析时间：** 2026-05-27  
**分析目的：** 识别数据对接文档中缺失的数据源，确保系统数据完整性

---

## 一、当前数据对接文档现状

**已包含的数据源：**
1. ✅ 学生宿舍清退数据（来源：宿管系统）
   - 用途：验证学生是否完成宿舍清退
   - 对接方式：API接口 或 CSV文件导入

**缺失的数据源：**
- ❌ 管理员数据（辅导员、学工部管理员）
- ❌ 其他可能需要的数据源

---

## 二、系统角色分析

根据系统设计文档（`users`表），系统有3个角色：

| 角色 | 英文名 | 数量 | 职责 | 数据来源 |
|------|--------|------|------|----------|
| 学生 | student | ~1000人/届 | 提交离校申请 | 教务系统 |
| 辅导员 | counselor | ~50人 | 一级审批 | 人事系统 + 教务系统 |
| 学工部管理员 | admin | ~5人 | 终审备案 | 人事系统 |

---

## 三、必需数据源（P0）

### 3.1 学生基本信息

**数据来源：** 教务系统

**用途：**
- 创建学生账号
- 身份验证
- 自动分配审批人（根据班级）

**必需字段：**
- 学号（student_id）
- 姓名（name）
- 院系（department）
- 专业（major）
- 班级（class_name）
- 年级（grade）
- 手机号（phone，可选）
- 邮箱（email，可选）

**对接方式：**
- API接口（推荐）
- CSV文件导入（备选）

**当前状态：** ❌ 未在数据对接文档中说明

---

### 3.2 宿舍清退数据

**数据来源：** 宿管系统

**用途：**
- 验证学生是否完成宿舍清退
- 作为离校申请的前置条件

**必需字段：**
- 学号（student_id）
- 姓名（name）
- 宿舍信息（dorm_building, dorm_room, bed_number）
- 清退状态（is_checked_out, checkout_date）

**对接方式：**
- API接口（推荐）
- CSV文件导入（备选）

**当前状态：** ✅ 已在数据对接文档中详细说明

---

### 3.3 辅导员基本信息

**数据来源：** 人事系统

**用途：**
- 创建辅导员账号
- 分配审批权限

**必需字段：**
- 工号（employee_id）
- 姓名（name）
- 手机号（phone）
- 邮箱（email）
- 院系（department，可选）
- 初始密码（password，或使用工号作为初始密码）

**对接方式：**
- API接口（推荐）
- CSV文件导入（备选）

**当前状态：** ❌ 未在数据对接文档中说明

---

### 3.4 班级-辅导员对应关系

**数据来源：** 教务系统

**用途：**
- 自动分配审批人
- 学生提交申请时，系统根据班级自动找到对应辅导员

**必需字段：**
- 班级名称（class_name）
- 辅导员工号（counselor_employee_id）
- 院系（department）
- 年级（grade）

**对接方式：**
- API接口（推荐）
- CSV文件导入（备选）

**当前状态：** ❌ 未在数据对接文档中说明

**重要性：** 🔴 极高
- 如果没有这个数据，系统无法自动分配审批人
- 需要手动配置每个学生的辅导员，工作量巨大

---

### 3.5 学工部管理员信息

**数据来源：** 人事系统

**用途：**
- 创建学工部管理员账号
- 终审备案权限

**必需字段：**
- 工号（employee_id）
- 姓名（name）
- 手机号（phone）
- 邮箱（email）
- 初始密码（password，或使用工号作为初始密码）

**对接方式：**
- 手动创建（数量少，~5人）
- CSV文件导入（备选）

**当前状态：** ❌ 未在数据对接文档中说明

**重要性：** 🟡 中等
- 数量少，可以手动创建
- 但建议在文档中说明

---

## 四、可选数据源（P1）

### 4.1 图书馆清书状态

**数据来源：** 图书馆系统

**用途：**
- 验证学生是否归还图书
- 作为离校申请的前置条件

**必需字段：**
- 学号（student_id）
- 姓名（name）
- 是否清书（is_cleared）
- 清书日期（clear_date）

**对接方式：**
- API接口（推荐）
- CSV文件导入（备选）

**当前方案：** 学生上传图书馆清书证明截图（手动验证）

**是否需要对接：** 可选
- 如果图书馆系统支持API，建议对接
- 如果不支持，继续使用手动上传方式

---

### 4.2 财务结清状态

**数据来源：** 财务系统

**用途：**
- 验证学生是否结清费用
- 作为离校申请的前置条件

**必需字段：**
- 学号（student_id）
- 姓名（name）
- 是否结清（is_cleared）
- 结清日期（clear_date）

**对接方式：**
- API接口（推荐）
- CSV文件导入（备选）

**当前方案：** 学生上传财务结清截图（手动验证）

**是否需要对接：** 可选
- 如果财务系统支持API，建议对接
- 如果不支持，继续使用手动上传方式

---

### 4.3 学籍状态（毕业生识别）

**数据来源：** 教务系统

**用途：**
- 自动识别毕业生
- 限制只有毕业生可以提交离校申请
- 自动设置计划离校日期范围

**必需字段：**
- 学号（student_id）
- 姓名（name）
- 学籍状态（status：在读/毕业/结业/肄业）
- 毕业时间（graduation_date）
- 年级（grade）

**对接方式：**
- API接口（推荐）
- 包含在学生基本信息中（备选）

**当前方案：** 可能未考虑

**是否需要对接：** 建议对接
- 防止非毕业生误操作
- 自动化程度更高

---

## 五、不需要的数据源

### 5.1 宿管员信息

**原因：**
- 宿舍清退通过外部系统API验证
- 宿管员不需要在本系统中登录
- 不需要宿管员数据

---

## 六、数据源优先级总结

### P0（必需，系统无法运行）

| 数据源 | 来源系统 | 对接方式 | 当前状态 |
|--------|----------|----------|----------|
| 学生基本信息 | 教务系统 | API/CSV | ❌ 缺失 |

exec
/bin/bash -lc "rtk sed -n '261,520p' docs/discussions/codex-review-2026-05-27/31-data-source-requirements-consensus.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:

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

codex
我已经确认共识文档吸收了上一轮审查的核心方向：学生、辅导员、班级映射、宿舍清退都列为 P0，管理员外部同步降为 P1。接下来我会对照系统设计和用户说明，重点核查字段、流程假设和待反馈问题是否还缺关键项。
exec
/bin/bash -lc 'rtk rg -n "学生|辅导员|管理员|宿舍|图书馆|财务|离校|审批|班级|专业|学院|院系|学号|手机号|openid|微信|账号|用户|users|applications|counselor_id|admin_id|class" docs/用户设计说明书.md docs/design/2026-05-27-system-design.md docs/数据对接说明文档.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/数据对接说明文档.md:1:# 毕业生离校申请审批系统 - 数据对接说明文档
docs/数据对接说明文档.md:5:**目标用户：** 宿舍管理系统管理员、数据对接负责人
docs/数据对接说明文档.md:13:本系统需要与学校现有的**宿舍管理系统**进行数据对接，实现以下功能：
docs/数据对接说明文档.md:15:- 学生提交离校申请时，自动验证宿舍是否已清退
docs/数据对接说明文档.md:16:- 验证通过后，允许学生继续提交申请
docs/数据对接说明文档.md:17:- 验证失败时，提示学生先完成宿舍清退手续
docs/数据对接说明文档.md:24:- 宿舍管理系统提供REST API接口
docs/数据对接说明文档.md:25:- 本系统调用API实时查询宿舍清退状态
docs/数据对接说明文档.md:27:- 缺点：需要宿舍管理系统支持API开发
docs/数据对接说明文档.md:30:- 宿舍管理系统定期导出清退数据文件
docs/数据对接说明文档.md:40:| 接口开发 | 第2-3周 | 宿舍管理系统开发API接口（如选择方式1） |
docs/数据对接说明文档.md:50:**接口名称：** 查询学生宿舍清退状态
docs/数据对接说明文档.md:54:**请求地址：** `http://宿舍管理系统域名/api/dorm/checkout/status`
docs/数据对接说明文档.md:67:| student_id | String | 是 | 学号 | "2020010101" |
docs/数据对接说明文档.md:104:| student_id | String | 学号 | "2020010101" |
docs/数据对接说明文档.md:106:| class_name | String | 班级（可选） | "计算机2020级1班" |
docs/数据对接说明文档.md:107:| dorm_building | String | 宿舍楼栋 | "1号楼" |
docs/数据对接说明文档.md:108:| dorm_room | String | 宿舍房间号 | "101" |
docs/数据对接说明文档.md:123:    "class_name": "计算机2020级1班",
docs/数据对接说明文档.md:143:    "class_name": "计算机2020级1班",
docs/数据对接说明文档.md:159:  "message": "学号不存在",
docs/数据对接说明文档.md:178:| 1001 | 学号不存在 | 提示学生检查学号 |
docs/数据对接说明文档.md:181:| 5000 | 系统内部错误 | 重试或联系管理员 |
docs/数据对接说明文档.md:195:- 测试学号：`2020010101`（已清退）、`2020010102`（未清退）
docs/数据对接说明文档.md:222:| 学号 | student_id | 文本 | 是 | 学生学号 | 2020010101 |
docs/数据对接说明文档.md:223:| 姓名 | name | 文本 | 是 | 学生姓名 | 张三 |
docs/数据对接说明文档.md:224:| 班级 | class_name | 文本 | 否 | 学生班级 | 计算机2020级1班 |
docs/数据对接说明文档.md:225:| 宿舍楼栋 | dorm_building | 文本 | 否 | 宿舍楼栋名称 | 1号楼 |
docs/数据对接说明文档.md:226:| 宿舍房间号 | dorm_room | 文本 | 否 | 宿舍房间号 | 101 |
docs/数据对接说明文档.md:235:**下载模板：** `docs/templates/宿舍清退数据模板.csv`
docs/数据对接说明文档.md:239:| 学号 | 姓名 | 班级 | 宿舍楼栋 | 宿舍房间号 | 床号 | 是否已清退 | 清退日期 | 清退状态 | 备注 |
docs/数据对接说明文档.md:248:学号,姓名,班级,宿舍楼栋,宿舍房间号,床号,是否已清退,清退日期,清退状态,备注
docs/数据对接说明文档.md:258:- 学号必须唯一
docs/数据对接说明文档.md:262:- 学号必须与学生信息系统一致
docs/数据对接说明文档.md:263:- 姓名必须与学生信息系统一致
docs/数据对接说明文档.md:273:- 宿舍管理系统自动上传到指定FTP服务器
docs/数据对接说明文档.md:277:- 宿舍管理系统导出到共享文件夹
docs/数据对接说明文档.md:281:- 管理员手动下载文件
docs/数据对接说明文档.md:298:- 文件传输账号独立，权限最小化
docs/数据对接说明文档.md:303:- 导出数据不包含敏感信息（身份证号、手机号等）
docs/数据对接说明文档.md:318:**宿舍管理系统方：**
docs/数据对接说明文档.md:320:- 提供测试账号和API Key
docs/数据对接说明文档.md:325:- 配置宿舍管理系统API地址
docs/数据对接说明文档.md:326:- 准备测试学号
docs/数据对接说明文档.md:332:| 查询已清退学生 | 学号：2020010101 | 返回is_checked_out=true |
docs/数据对接说明文档.md:333:| 查询未清退学生 | 学号：2020010102 | 返回is_checked_out=false |
docs/数据对接说明文档.md:334:| 查询不存在学号 | 学号：9999999999 | 返回错误码1001 |
docs/数据对接说明文档.md:354:- 生产环境API Key：由宿舍管理系统提供
docs/数据对接说明文档.md:358:- FTP/SFTP地址：由宿舍管理系统提供
docs/数据对接说明文档.md:359:- 传输账号密码：由宿舍管理系统提供
docs/数据对接说明文档.md:380:- 通知管理员和宿舍管理系统负责人
docs/数据对接说明文档.md:385:- 人工审核宿舍清退证明
docs/数据对接说明文档.md:399:**宿舍管理系统方：**
docs/数据对接说明文档.md:415:模板文件路径：`docs/templates/宿舍清退数据模板.csv`
docs/用户设计说明书.md:1:# 毕业生离校申请审批系统 - 用户设计说明书
docs/用户设计说明书.md:5:**目标用户：** 学校管理人员、辅导员、学工部
docs/用户设计说明书.md:13:本系统旨在实现毕业生离校申请的在线化、规范化管理，替代传统纸质审批流程，提高审批效率，减少人工成本。
docs/用户设计说明书.md:17:- **学生端：** 在线提交离校申请、上传证明材料、查看审批进度、接收审批通知
docs/用户设计说明书.md:18:- **辅导员端：** 审批本年级学生的离校申请、查看审批历史、接收待办提醒
docs/用户设计说明书.md:19:- **学工部端：** 审批所有学生的离校申请、查看全校审批统计、导出审批数据
docs/用户设计说明书.md:20:- **系统管理：** 用户管理、权限配置、系统参数设置
docs/用户设计说明书.md:25:- **微信小程序：** 微信内使用，无需安装
docs/用户设计说明书.md:35:学生登录 → 填写申请信息 → 上传证明材料 → 提交申请 → 等待审批
docs/用户设计说明书.md:39:- 学号、姓名、专业、班级
docs/用户设计说明书.md:40:- 计划离校日期
docs/用户设计说明书.md:44:- 宿舍清退证明（照片或PDF）
docs/用户设计说明书.md:45:- 图书馆清书证明（照片或PDF）
docs/用户设计说明书.md:46:- 财务结清截图（照片或PDF）
docs/用户设计说明书.md:48:### 2.2 审批流程
docs/用户设计说明书.md:51:学生提交 → 辅导员审批 → 学工部审批 → 审批完成
docs/用户设计说明书.md:53:         学生修改 ←──────┘
docs/用户设计说明书.md:56:**审批时限：**
docs/用户设计说明书.md:57:- 辅导员审批：提交后1个工作日内
docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
docs/用户设计说明书.md:59:- 超时提醒：系统自动发送微信通知
docs/用户设计说明书.md:61:**审批结果：**
docs/用户设计说明书.md:62:- **通过：** 进入下一审批环节或完成审批
docs/用户设计说明书.md:63:- **驳回：** 学生收到通知，修改后重新提交
docs/用户设计说明书.md:67:**微信通知场景：**
docs/用户设计说明书.md:68:- 学生提交申请 → 通知辅导员
docs/用户设计说明书.md:69:- 辅导员审批通过 → 通知学生和学工部
docs/用户设计说明书.md:70:- 辅导员驳回 → 通知学生
docs/用户设计说明书.md:71:- 学工部审批通过 → 通知学生（审批完成）
docs/用户设计说明书.md:72:- 学工部驳回 → 通知学生
docs/用户设计说明书.md:73:- 审批超时 → 通知审批人
docs/用户设计说明书.md:81:**学号密码登录：**
docs/用户设计说明书.md:83:- 学号由学校统一导入
docs/用户设计说明书.md:84:- 初始密码为学号，首次登录强制修改密码
docs/用户设计说明书.md:87:**微信授权登录：**
docs/用户设计说明书.md:89:- 支持微信消息推送
docs/用户设计说明书.md:94:**宿舍管理系统对接：**
docs/用户设计说明书.md:95:- 学生提交申请时，系统自动验证宿舍是否已清退
docs/用户设计说明书.md:96:- 验证失败时，提示学生先完成宿舍清退
docs/用户设计说明书.md:115:- 学生只能查看自己的申请
docs/用户设计说明书.md:116:- 辅导员只能查看负责班级的学生
docs/用户设计说明书.md:117:- 学工部可以查看所有学生
docs/用户设计说明书.md:127:| **学生** | 本人申请 | 提交申请、查看进度、上传附件 |
docs/用户设计说明书.md:128:| **辅导员** | 本年级学生 | 审批申请、查看历史、接收通知 |
docs/用户设计说明书.md:129:| **学工部** | 全校学生 | 审批申请、查看统计、导出数据 |
docs/用户设计说明书.md:130:| **系统管理员** | 全部功能 | 用户管理、权限配置、系统设置 |
docs/用户设计说明书.md:134:**学生权限：**
docs/用户设计说明书.md:135:- ✓ 创建离校申请
docs/用户设计说明书.md:140:- ✓ 查看审批历史
docs/用户设计说明书.md:141:- ✗ 查看其他学生的申请
docs/用户设计说明书.md:143:**辅导员权限：**
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
docs/用户设计说明书.md:179:- 在线用户：500人
docs/用户设计说明书.md:185:- 学生用户：10,000人
docs/用户设计说明书.md:204:### 6.1 学生常见问题
docs/用户设计说明书.md:207:A：联系辅导员或系统管理员重置密码。
docs/用户设计说明书.md:209:**Q2：微信绑定失败怎么办？**
docs/用户设计说明书.md:210:A：确认学号和密码正确，如仍失败请联系管理员。
docs/用户设计说明书.md:213:A：检查文件大小（<10MB）和格式（jpg/png/pdf/doc/docx），如仍失败请联系管理员。
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
docs/用户设计说明书.md:237:**Q1：如何批量导入学生用户？**
docs/用户设计说明书.md:238:A：准备Excel模板（学号、姓名、专业、班级、辅导员），在管理后台上传。
docs/用户设计说明书.md:240:**Q2：如何修改审批时限？**
docs/用户设计说明书.md:241:A：在系统配置页面修改"审批时限"参数（单位：小时）。
docs/用户设计说明书.md:244:A：在管理后台"审计日志"页面查看，支持按用户、操作、时间筛选。
docs/用户设计说明书.md:246:**Q4：如何对接宿舍管理系统？**
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
docs/design/2026-05-27-system-design.md:140:│   ├── accounts/          # 用户账户模块
docs/design/2026-05-27-system-design.md:141:│   │   ├── models.py      # 用户模型
docs/design/2026-05-27-system-design.md:146:│   ├── applications/      # 离校申请模块
docs/design/2026-05-27-system-design.md:149:│   │   ├── workflows.py   # 审批流程
docs/design/2026-05-27-system-design.md:152:│   ├── approvals/         # 审批管理模块
docs/design/2026-05-27-system-design.md:153:│   │   ├── models.py      # 审批记录
docs/design/2026-05-27-system-design.md:154:│   │   ├── views.py       # 审批操作API
docs/design/2026-05-27-system-design.md:165:│   │   └── wechat.py      # 微信推送
docs/design/2026-05-27-system-design.md:168:│       ├── dorm_system.py # 宿舍系统对接
docs/design/2026-05-27-system-design.md:186:1. **accounts（用户账户）**
docs/design/2026-05-27-system-design.md:187:   - 学生/辅导员/学工部用户管理
docs/design/2026-05-27-system-design.md:188:   - 学号+密码登录
docs/design/2026-05-27-system-design.md:189:   - 微信OAuth2授权登录
docs/design/2026-05-27-system-design.md:191:   - 用户权限管理
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
docs/design/2026-05-27-system-design.md:246:1. users - 用户表
docs/design/2026-05-27-system-design.md:247:2. applications - 离校申请表
docs/design/2026-05-27-system-design.md:248:3. approvals - 审批记录表
docs/design/2026-05-27-system-design.md:253:8. applications_history - 申请历史表
docs/design/2026-05-27-system-design.md:255:### 2.2 用户表（users）
docs/design/2026-05-27-system-design.md:260:CREATE TABLE users (
docs/design/2026-05-27-system-design.md:262:    student_id VARCHAR(20) UNIQUE NOT NULL COMMENT '学号',
docs/design/2026-05-27-system-design.md:265:    wechat_openid VARCHAR(100) UNIQUE COMMENT '微信OpenID',
docs/design/2026-05-27-system-design.md:273:    wechat_bind_time TIMESTAMP COMMENT '微信绑定时间',
docs/design/2026-05-27-system-design.md:276:    phone VARCHAR(20) COMMENT '手机号',
docs/design/2026-05-27-system-design.md:279:    department VARCHAR(100) COMMENT '院系',
docs/design/2026-05-27-system-design.md:280:    major VARCHAR(100) COMMENT '专业',
docs/design/2026-05-27-system-design.md:281:    class_name VARCHAR(50) COMMENT '班级',
docs/design/2026-05-27-system-design.md:290:    INDEX idx_wechat_openid (wechat_openid),
docs/design/2026-05-27-system-design.md:294:        (password_hash IS NOT NULL) OR (wechat_openid IS NOT NULL)
docs/design/2026-05-27-system-design.md:296:) COMMENT='用户表';
docs/design/2026-05-27-system-design.md:300:- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
docs/design/2026-05-27-system-design.md:301:- `wechat_openid`: 微信授权登录后绑定
docs/design/2026-05-27-system-design.md:304:### 2.3 离校申请表（applications）
docs/design/2026-05-27-system-design.md:307:CREATE TABLE applications (
docs/design/2026-05-27-system-design.md:310:    student_id BIGINT NOT NULL COMMENT '学生ID',
docs/design/2026-05-27-system-design.md:312:    -- 固定审批人追踪
docs/design/2026-05-27-system-design.md:313:    counselor_id BIGINT COMMENT '辅导员ID',
docs/design/2026-05-27-system-design.md:314:    admin_id BIGINT COMMENT '学工部管理员ID',
docs/design/2026-05-27-system-design.md:316:    planned_leave_date DATE NOT NULL COMMENT '计划离校日期',
docs/design/2026-05-27-system-design.md:318:    current_approver_id BIGINT COMMENT '当前审批人ID',
docs/design/2026-05-27-system-design.md:325:    certificate_url VARCHAR(500) COMMENT '离校凭证URL',
docs/design/2026-05-27-system-design.md:335:    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:336:    FOREIGN KEY (counselor_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:337:    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:338:    FOREIGN KEY (current_approver_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:341:    INDEX idx_counselor_id (counselor_id),
docs/design/2026-05-27-system-design.md:342:    INDEX idx_admin_id (admin_id),
docs/design/2026-05-27-system-design.md:349:) COMMENT='离校申请表';
docs/design/2026-05-27-system-design.md:354:- `pending_counselor` - 待辅导员审核
docs/design/2026-05-27-system-design.md:356:- `approved` - 审批通过
docs/design/2026-05-27-system-design.md:362:### 2.4 审批记录表（approvals）
docs/design/2026-05-27-system-design.md:368:    approver_id BIGINT NOT NULL COMMENT '审批人ID',
docs/design/2026-05-27-system-design.md:369:    approver_role VARCHAR(20) NOT NULL COMMENT '审批人角色',
docs/design/2026-05-27-system-design.md:371:    opinion TEXT COMMENT '审批意见',
docs/design/2026-05-27-system-design.md:372:    approval_time TIMESTAMP NOT NULL COMMENT '审批时间',
docs/design/2026-05-27-system-design.md:377:    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
docs/design/2026-05-27-system-design.md:378:    FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:383:) COMMENT='审批记录表';
docs/design/2026-05-27-system-design.md:387:- `approver_role`: counselor（辅导员）、admin（学工部）
docs/design/2026-05-27-system-design.md:389:- `time_limit`: 辅导员1个工作日(24小时)，学工部1个工作日(24小时)
docs/design/2026-05-27-system-design.md:407:    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
docs/design/2026-05-27-system-design.md:416:- `dorm_clearance` - 宿舍清退证明
docs/design/2026-05-27-system-design.md:417:- `library_clearance` - 图书馆清书证明
docs/design/2026-05-27-system-design.md:418:- `finance_settlement` - 财务结清截图
docs/design/2026-05-27-system-design.md:431:    user_id BIGINT NOT NULL COMMENT '接收用户ID',
docs/design/2026-05-27-system-design.md:444:    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
docs/design/2026-05-27-system-design.md:445:    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:455:- `approval_pending` - 待审批
docs/design/2026-05-27-system-design.md:458:- `approval_timeout` - 审批超时提醒
docs/design/2026-05-27-system-design.md:480:    FOREIGN KEY (updated_by) REFERENCES users(id)
docs/design/2026-05-27-system-design.md:486:- `wechat` - 微信配置
docs/design/2026-05-27-system-design.md:494:- `wechat.appid` - 微信AppID
docs/design/2026-05-27-system-design.md:495:- `wechat.secret` - 微信Secret（加密存储）
docs/design/2026-05-27-system-design.md:496:- `dorm_integration_type` - 宿舍系统集成类型（api/database）
docs/design/2026-05-27-system-design.md:497:- `dorm_api_url` - 宿舍系统API地址
docs/design/2026-05-27-system-design.md:498:- `dorm_api_key` - 宿舍系统API密钥（加密存储）
docs/design/2026-05-27-system-design.md:499:- `dorm_db_config` - 宿舍系统数据库配置（加密存储，JSON格式）
docs/design/2026-05-27-system-design.md:508:    user_id BIGINT NOT NULL COMMENT '操作用户ID',
docs/design/2026-05-27-system-design.md:521:    user_agent TEXT COMMENT '用户代理',
docs/design/2026-05-27-system-design.md:527:    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:544:- `approve` - 审批通过
docs/design/2026-05-27-system-design.md:545:- `reject` - 审批驳回
docs/design/2026-05-27-system-design.md:551:- `user` - 用户
docs/design/2026-05-27-system-design.md:553:- `approval` - 审批
docs/design/2026-05-27-system-design.md:557:### 2.9 申请历史表（applications_history）
docs/design/2026-05-27-system-design.md:562:CREATE TABLE applications_history (
docs/design/2026-05-27-system-design.md:571:    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
docs/design/2026-05-27-system-design.md:572:    FOREIGN KEY (changed_by) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:591:users (用户表)
docs/design/2026-05-27-system-design.md:592:  ├─1:N─→ applications (学生创建多个申请)
docs/design/2026-05-27-system-design.md:593:  ├─1:N─→ approvals (审批人审批多个申请)
docs/design/2026-05-27-system-design.md:594:  └─1:N─→ notifications (用户接收多个通知)
docs/design/2026-05-27-system-design.md:596:applications (申请表)
docs/design/2026-05-27-system-design.md:597:  ├─N:1─→ users (申请人)
docs/design/2026-05-27-system-design.md:598:  ├─N:1─→ users (辅导员)
docs/design/2026-05-27-system-design.md:599:  ├─N:1─→ users (学工部管理员)
docs/design/2026-05-27-system-design.md:600:  ├─N:1─→ users (当前审批人)
docs/design/2026-05-27-system-design.md:601:  ├─1:N─→ approvals (一个申请多条审批记录)
docs/design/2026-05-27-system-design.md:604:  └─1:N─→ applications_history (一个申请多个历史版本)
docs/design/2026-05-27-system-design.md:607:approvals (审批记录表)
docs/design/2026-05-27-system-design.md:608:  ├─N:1─→ applications (多条审批记录属于一个申请)
docs/design/2026-05-27-system-design.md:609:  └─N:1─→ users (审批人)
docs/design/2026-05-27-system-design.md:612:  └─N:1─→ applications (多个附件属于一个申请)
docs/design/2026-05-27-system-design.md:615:  ├─N:1─→ users (接收人)
docs/design/2026-05-27-system-design.md:616:  └─N:1─→ applications (关联申请)
docs/design/2026-05-27-system-design.md:619:  └─N:1─→ users (操作人)
docs/design/2026-05-27-system-design.md:622:  └─N:1─→ users (更新人)
docs/design/2026-05-27-system-design.md:626:1. 一个学生可以创建多个申请（不同时间段）
docs/design/2026-05-27-system-design.md:627:2. 一个申请必须经过2级审批（辅导员→学工部）
docs/design/2026-05-27-system-design.md:628:3. 每个审批节点记录一条审批记录
docs/design/2026-05-27-system-design.md:676:**1. 学号密码登录**
docs/design/2026-05-27-system-design.md:705:**2. 微信授权登录**
docs/design/2026-05-27-system-design.md:726:      "wechat_openid": "oXXXX"
docs/design/2026-05-27-system-design.md:734:  "message": "需要绑定学号",
docs/design/2026-05-27-system-design.md:737:    "wechat_openid": "oXXXX",
docs/design/2026-05-27-system-design.md:742:Response (新用户，需要设置密码):
docs/design/2026-05-27-system-design.md:754:**3. 微信绑定到已有账户**
docs/design/2026-05-27-system-design.md:777:      "wechat_openid": "oXXXX"
docs/design/2026-05-27-system-design.md:785:  "message": "绑定失败，请联系管理员"
docs/design/2026-05-27-system-design.md:789:**4. 设置密码（新用户）**
docs/design/2026-05-27-system-design.md:850:POST /api/v1/applications
docs/design/2026-05-27-system-design.md:857:  "remarks": "毕业离校"
docs/design/2026-05-27-system-design.md:875:GET /api/v1/applications?status=pending_counselor&page=1&page_size=20
docs/design/2026-05-27-system-design.md:902:GET /api/v1/applications/{id}
docs/design/2026-05-27-system-design.md:915:      "department": "计算机学院"
docs/design/2026-05-27-system-design.md:923:        "file_name": "宿舍清退证明.jpg",
docs/design/2026-05-27-system-design.md:941:PUT /api/v1/applications/{id}
docs/design/2026-05-27-system-design.md:947:  "remarks": "延后离校"
docs/design/2026-05-27-system-design.md:959:POST /api/v1/applications/{id}/submit
docs/design/2026-05-27-system-design.md:973:### 3.4 审批相关API
docs/design/2026-05-27-system-design.md:975:**1. 获取待审批列表**
docs/design/2026-05-27-system-design.md:999:**2. 审批通过**
docs/design/2026-05-27-system-design.md:1006:  "opinion": "材料齐全，同意离校",
docs/design/2026-05-27-system-design.md:1013:  "message": "审批成功",
docs/design/2026-05-27-system-design.md:1031:**3. 审批驳回**
docs/design/2026-05-27-system-design.md:1038:  "opinion": "宿舍清退证明不完整，请重新提交",
docs/design/2026-05-27-system-design.md:1066:POST /api/v1/applications/{id}/attachments
docs/design/2026-05-27-system-design.md:1080:    "file_name": "宿舍清退证明.jpg",
docs/design/2026-05-27-system-design.md:1154:        "content": "您的离校申请已通过辅导员审核",
docs/design/2026-05-27-system-design.md:1175:### 3.7 系统配置API（管理员）
docs/design/2026-05-27-system-design.md:1189:      "description": "宿舍系统集成类型（api/database）"
docs/design/2026-05-27-system-design.md:1194:      "description": "宿舍系统API地址"
docs/design/2026-05-27-system-design.md:1199:      "description": "宿舍系统API密钥（加密存储）",
docs/design/2026-05-27-system-design.md:1225:- `wechat` - 微信配置
docs/design/2026-05-27-system-design.md:1228:- `integration` - 外部系统集成配置（宿舍系统等）
docs/design/2026-05-27-system-design.md:1237:1. **学号+密码认证**
docs/design/2026-05-27-system-design.md:1238:   - 学号作为唯一标识
docs/design/2026-05-27-system-design.md:1242:2. **微信OAuth2认证**
docs/design/2026-05-27-system-design.md:1243:   - 获取微信授权code
docs/design/2026-05-27-system-design.md:1244:   - 后端换取openid
docs/design/2026-05-27-system-design.md:1245:   - openid绑定学号
docs/design/2026-05-27-system-design.md:1246:   - 首次登录需绑定学号
docs/design/2026-05-27-system-design.md:1250:学号密码登录：
docs/design/2026-05-27-system-design.md:1251:用户输入学号+密码 → 后端验证 → 生成JWT Token → 返回Token
docs/design/2026-05-27-system-design.md:1253:微信登录（安全增强）：
docs/design/2026-05-27-system-design.md:1254:用户授权 → 获取code → 后端换取openid → 
docs/design/2026-05-27-system-design.md:1257:   ├─ 学号已存在：
docs/design/2026-05-27-system-design.md:1258:   │  ├─ 已绑定其他微信：返回通用错误（防止枚举）
docs/design/2026-05-27-system-design.md:1259:   │  └─ 未绑定微信：要求密码验证 → 事务锁绑定 → 审计日志 → 生成Token
docs/design/2026-05-27-system-design.md:1260:   └─ 学号不存在（新用户）：
docs/design/2026-05-27-system-design.md:1261:      └─ 创建账户 → 强制设置密码 → 学生身份验证 → 生成受限Token
docs/design/2026-05-27-system-design.md:1267:1. **密码验证**：微信绑定已有账户时需要密码验证
docs/design/2026-05-27-system-design.md:1271:3. ⏸ **学生身份验证**：如发现冒用问题，引入短信/邮件/学生证验证
docs/design/2026-05-27-system-design.md:1275:**理由：** 本系统为内部系统，用户由管理员导入，学号枚举风险低。Phase 1采用核心措施，根据实际需求渐进式引入其他措施。
docs/design/2026-05-27-system-design.md:1312:student（学生）
docs/design/2026-05-27-system-design.md:1319:counselor（辅导员）
docs/design/2026-05-27-system-design.md:1321:├─ 审批申请（通过/驳回）
docs/design/2026-05-27-system-design.md:1322:├─ 查看审批历史
docs/design/2026-05-27-system-design.md:1325:admin（学工部管理员）
docs/design/2026-05-27-system-design.md:1327:├─ 最终备案审批
docs/design/2026-05-27-system-design.md:1329:├─ 用户管理
docs/design/2026-05-27-system-design.md:1341:辅导员审批         | ✗       | ✓         | ✗
docs/design/2026-05-27-system-design.md:1342:学工部审批         | ✗       | ✗         | ✓
docs/design/2026-05-27-system-design.md:1373:class IsStudent(BasePermission):
docs/design/2026-05-27-system-design.md:1377:class IsCounselor(BasePermission):
docs/design/2026-05-27-system-design.md:1381:class IsOwner(BasePermission):
docs/design/2026-05-27-system-design.md:1388:## 5. 审批流程设计
docs/design/2026-05-27-system-design.md:1396:pending_counselor（待辅导员审核）
docs/design/2026-05-27-system-design.md:1401:approved（审批通过）
docs/design/2026-05-27-system-design.md:1408:    'pending_counselor': ['pending_admin', 'rejected'],  # 辅导员审批
docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
docs/design/2026-05-27-system-design.md:1417:**节点1：学生提交申请**
docs/design/2026-05-27-system-design.md:1418:- 触发条件：学生填写完整信息并上传附件
docs/design/2026-05-27-system-design.md:1420:  - 计划离校日期 ≥ 当前日期 + 3个工作日
docs/design/2026-05-27-system-design.md:1421:  - 必须上传宿舍清退证明
docs/design/2026-05-27-system-design.md:1422:  - 必须上传图书馆清书证明
docs/design/2026-05-27-system-design.md:1423:  - 必须上传财务结清截图
docs/design/2026-05-27-system-design.md:1427:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
docs/design/2026-05-27-system-design.md:1428:  - 设置当前审批人：current_approver_id = counselor_id
docs/design/2026-05-27-system-design.md:1431:  - 创建历史快照：applications_history（version=0, change_reason='提交申请'）
docs/design/2026-05-27-system-design.md:1433:  - 发送通知给辅导员
docs/design/2026-05-27-system-design.md:1436:**节点2：辅导员审核**
docs/design/2026-05-27-system-design.md:1438:- 权限要求：辅导员角色 + current_approver_id匹配
docs/design/2026-05-27-system-design.md:1443:    - 更新当前审批人：current_approver_id = admin_id
docs/design/2026-05-27-system-design.md:1445:    - 创建审批记录：approvals（approver_role='counselor', action='approve'）
docs/design/2026-05-27-system-design.md:1446:    - 创建历史快照：applications_history（version=N, change_reason='辅导员审批通过'）
docs/design/2026-05-27-system-design.md:1451:    - 清空当前审批人：current_approver_id = NULL
docs/design/2026-05-27-system-design.md:1453:    - 创建审批记录：approvals（approver_role='counselor', action='reject'）
docs/design/2026-05-27-system-design.md:1454:    - 创建历史快照：applications_history（version=N, change_reason='辅导员驳回'）
docs/design/2026-05-27-system-design.md:1456:    - 通知学生并说明原因
docs/design/2026-05-27-system-design.md:1457:  - 记录审批意见和时间
docs/design/2026-05-27-system-design.md:1463:- 权限要求：学工部管理员角色 + current_approver_id匹配
docs/design/2026-05-27-system-design.md:1468:    - 清空当前审批人：current_approver_id = NULL
docs/design/2026-05-27-system-design.md:1470:    - 生成电子离校凭证：certificate_url
docs/design/2026-05-27-system-design.md:1472:    - 创建审批记录：approvals（approver_role='admin', action='approve'）
docs/design/2026-05-27-system-design.md:1473:    - 创建历史快照：applications_history（version=N, change_reason='学工部备案通过'）
docs/design/2026-05-27-system-design.md:1476:    - 通知学生
docs/design/2026-05-27-system-design.md:1479:    - 清空当前审批人：current_approver_id = NULL
docs/design/2026-05-27-system-design.md:1481:    - 创建审批记录：approvals（approver_role='admin', action='reject'）
docs/design/2026-05-27-system-design.md:1482:    - 创建历史快照：applications_history（version=N, change_reason='学工部驳回'）
docs/design/2026-05-27-system-design.md:1484:    - 通知学生
docs/design/2026-05-27-system-design.md:1492:  - 学生修改申请内容
docs/design/2026-05-27-system-design.md:1507:    # 查询待审批的申请
docs/design/2026-05-27-system-design.md:1514:        # 获取最新审批记录（当前节点）
docs/design/2026-05-27-system-design.md:1523:            # 已有审批记录，从上次审批时间开始计算
docs/design/2026-05-27-system-design.md:1530:            # 创建超时审批记录
docs/design/2026-05-27-system-design.md:1583:- 第1次：办理时限到期时通知审批人
docs/design/2026-05-27-system-design.md:1584:- 第2次：超时4小时后通知审批人上级
docs/design/2026-05-27-system-design.md:1585:- 第3次：超时8小时后通知系统管理员
docs/design/2026-05-27-system-design.md:1588:- 外部系统（宿舍管理系统）不可用时，允许手动上传证明文件
docs/design/2026-05-27-system-design.md:1589:- 审批人可选择"跳过验证"并备注原因
docs/design/2026-05-27-system-design.md:1605:### 6.2 宿舍管理系统对接
docs/design/2026-05-27-system-design.md:1608:验证学生宿舍清退状态，确保离校手续真实完成。
docs/design/2026-05-27-system-design.md:1622:# 查询宿舍清退状态
docs/design/2026-05-27-system-design.md:1635:    "class_name": "计算机2020级1班",
docs/design/2026-05-27-system-design.md:1651:class DormSystemClient:
docs/design/2026-05-27-system-design.md:1692:            raise ExternalSystemTimeout("宿舍系统超时")
docs/design/2026-05-27-system-design.md:1694:            raise ExternalSystemError(f"宿舍系统错误: {str(e)}")
docs/design/2026-05-27-system-design.md:1701:class ExternalSystemError(Exception):
docs/design/2026-05-27-system-design.md:1705:class ExternalSystemTimeout(ExternalSystemError):
docs/design/2026-05-27-system-design.md:1709:class ExternalSystemUnavailable(ExternalSystemError):
docs/design/2026-05-27-system-design.md:1713:class ExternalSystemAuthError(ExternalSystemError):
docs/design/2026-05-27-system-design.md:1734:- 审批人可选择"跳过验证"并备注原因
docs/design/2026-05-27-system-design.md:1915:- 微信Secret：AES-256加密存储
docs/design/2026-05-27-system-design.md:1975:**微信绑定安全措施：**
docs/design/2026-05-27-system-design.md:1982:def bind_wechat_to_account(student_id, wechat_openid, password):
docs/design/2026-05-27-system-design.md:1983:    """微信绑定已有账户"""
docs/design/2026-05-27-system-design.md:1992:        raise ValidationError("绑定失败，请检查学号和密码")
docs/design/2026-05-27-system-design.md:1994:    if user.wechat_openid:
docs/design/2026-05-27-system-design.md:1995:        raise ValidationError("该学号已绑定其他微信")
docs/design/2026-05-27-system-design.md:1998:    user.wechat_openid = wechat_openid
docs/design/2026-05-27-system-design.md:2012:def log_wechat_bind(user_id, wechat_openid, ip_address, success):
docs/design/2026-05-27-system-design.md:2025:- ⏸ 学生身份验证（短信/邮件/学生证）
docs/design/2026-05-27-system-design.md:2028:        raise ValidationError("学号不存在")
docs/design/2026-05-27-system-design.md:2030:    if user.wechat_openid:
docs/design/2026-05-27-system-design.md:2031:        # 通用错误，防止学号枚举
docs/design/2026-05-27-system-design.md:2032:        raise ValidationError("绑定失败，请联系管理员")
docs/design/2026-05-27-system-design.md:2036:        raise ValidationError("绑定失败，请联系管理员")
docs/design/2026-05-27-system-design.md:2038:    # 绑定微信
docs/design/2026-05-27-system-design.md:2039:    user.wechat_openid = wechat_openid
docs/design/2026-05-27-system-design.md:2046:def log_wechat_bind(user_id, wechat_openid, ip_address, success):
docs/design/2026-05-27-system-design.md:2058:5. **通用错误消息（防止学号枚举）**
docs/design/2026-05-27-system-design.md:2061:raise ValidationError("绑定失败，请联系管理员")
docs/design/2026-05-27-system-design.md:2062:# 不暴露具体原因：学号不存在、已绑定其他微信、密码错误等
docs/design/2026-05-27-system-design.md:2085:class LoginRateThrottle(UserRateThrottle):
docs/design/2026-05-27-system-design.md:2088:class UploadRateThrottle(UserRateThrottle):
docs/design/2026-05-27-system-design.md:2108:        location /api/v1/applications/*/attachments {
docs/design/2026-05-27-system-design.md:2126:- 匿名用户：100次/小时
docs/design/2026-05-27-system-design.md:2231:- 用户认证：登录、登出、密码修改、微信绑定
docs/design/2026-05-27-system-design.md:2233:- 审批操作：通过、驳回
docs/design/2026-05-27-system-design.md:2240:class AuditLog(models.Model):
docs/design/2026-05-27-system-design.md:2277:- 按用户查询：`/api/v1/audit-logs?user_id=1`
docs/design/2026-05-27-system-design.md:2289:class SystemConfig(models.Model):
docs/design/2026-05-27-system-design.md:2319:- `wechat_secret` - 微信Secret
docs/design/2026-05-27-system-design.md:2320:- `dorm_api_key` - 宿舍系统API密钥
docs/design/2026-05-27-system-design.md:2321:- `dorm_db_config` - 宿舍系统数据库配置（JSON格式）
docs/design/2026-05-27-system-design.md:2337:-- users表索引
docs/design/2026-05-27-system-design.md:2338:CREATE INDEX idx_student_id ON users(student_id);
docs/design/2026-05-27-system-design.md:2339:CREATE INDEX idx_role ON users(role);
docs/design/2026-05-27-system-design.md:2340:CREATE INDEX idx_wechat_openid ON users(wechat_openid);
docs/design/2026-05-27-system-design.md:2341:CREATE INDEX idx_account_locked ON users(account_locked);
docs/design/2026-05-27-system-design.md:2343:-- applications表索引
docs/design/2026-05-27-system-design.md:2344:CREATE INDEX idx_student_id ON applications(student_id);
docs/design/2026-05-27-system-design.md:2345:CREATE INDEX idx_counselor_id ON applications(counselor_id);
docs/design/2026-05-27-system-design.md:2346:CREATE INDEX idx_admin_id ON applications(admin_id);
docs/design/2026-05-27-system-design.md:2347:CREATE INDEX idx_status ON applications(status);
docs/design/2026-05-27-system-design.md:2348:CREATE INDEX idx_application_no ON applications(application_no);
docs/design/2026-05-27-system-design.md:2349:CREATE INDEX idx_planned_leave_date ON applications(planned_leave_date);
docs/design/2026-05-27-system-design.md:2351:-- applications表复合索引
docs/design/2026-05-27-system-design.md:2352:CREATE INDEX idx_approver_status ON applications(current_approver_id, status, submit_time);
docs/design/2026-05-27-system-design.md:2353:CREATE INDEX idx_student_status ON applications(student_id, status, created_at);
docs/design/2026-05-27-system-design.md:2354:CREATE INDEX idx_status_deleted ON applications(status, is_deleted, submit_time);
docs/design/2026-05-27-system-design.md:2386:- `idx_approver_status`: 待审批列表查询（按审批人+状态+时间）
docs/design/2026-05-27-system-design.md:2387:- `idx_student_status`: 学生查看自己申请列表
docs/design/2026-05-27-system-design.md:2389:- `idx_app_time`: 申请的审批历史（按时间倒序）
docs/design/2026-05-27-system-design.md:2391:- `idx_user_read_time`: 用户未读通知列表
docs/design/2026-05-27-system-design.md:2392:- `idx_user_action_time`: 用户操作审计日志
docs/design/2026-05-27-system-design.md:2435:# L1: 用户信息缓存（30分钟）
docs/design/2026-05-27-system-design.md:2441:# L3: 待审批数量缓存（1分钟）
docs/design/2026-05-27-system-design.md:2458:    # 失效审批人的待审批数量缓存
docs/design/2026-05-27-system-design.md:2463:    # 失效学生的申请列表缓存
docs/design/2026-05-27-system-design.md:2464:    cache.delete(f'student:{app.student_id}:applications')
docs/design/2026-05-27-system-design.md:2467:    """用户信息变更时失效缓存"""
docs/design/2026-05-27-system-design.md:2481:- 审批操作（必须实时）
docs/design/2026-05-27-system-design.md:2511:    # 发送微信通知
docs/design/2026-05-27-system-design.md:2514:# 异步生成离校凭证
docs/design/2026-05-27-system-design.md:2532:- 本地缓存用户信息
docs/design/2026-05-27-system-design.md:2593:    result = approve_application(app_id, counselor_id, 'approve')
docs/design/2026-05-27-system-design.md:2598:    response = client.post('/api/v1/applications', data)
docs/design/2026-05-27-system-design.md:2603:    """测试微信绑定需要密码验证"""
docs/design/2026-05-27-system-design.md:2604:    response = bind_wechat(student_id='2020001', openid='oXXX', password='wrong')
docs/design/2026-05-27-system-design.md:2606:    assert response.json()['message'] == '绑定失败，请联系管理员'
docs/design/2026-05-27-system-design.md:2611:    response = client.get('/api/v1/applications', headers={'Authorization': f'Bearer {token}'})
docs/design/2026-05-27-system-design.md:2615:    """测试微信绑定事务锁（防止竞态）"""
docs/design/2026-05-27-system-design.md:2616:    # 并发绑定同一学号
docs/design/2026-05-27-system-design.md:2629:    """测试微信绑定记录审计日志"""
docs/design/2026-05-27-system-design.md:2630:    bind_wechat(student_id='2020001', openid='oXXX', password='pass')
docs/design/2026-05-27-system-design.md:2637:    # 学号不存在
docs/design/2026-05-27-system-design.md:2638:    r1 = bind_wechat(student_id='9999999', openid='oXXX', password='pass')
docs/design/2026-05-27-system-design.md:2640:    r2 = bind_wechat(student_id='2020001', openid='oXXX', password='wrong')
docs/design/2026-05-27-system-design.md:2641:    # 已绑定其他微信
docs/design/2026-05-27-system-design.md:2642:    r3 = bind_wechat(student_id='2020002', openid='oXXX', password='pass')
docs/design/2026-05-27-system-design.md:2649:    """测试学生无法审批"""
docs/design/2026-05-27-system-design.md:2665:    response = client.post(f'/api/v1/applications/{app_id}/attachments', files={'file': fake_image})
docs/design/2026-05-27-system-design.md:2677:    """测试审批操作记录审计日志"""
docs/design/2026-05-27-system-design.md:2678:    approve_application(app_id, counselor_id, 'approve')
docs/design/2026-05-27-system-design.md:2695:- 完整审批流程测试
docs/design/2026-05-27-system-design.md:2708:- 微信开发者工具（小程序测试）
docs/design/2026-05-27-system-design.md:2711:1. 学生提交申请完整流程
docs/design/2026-05-27-system-design.md:2712:2. 辅导员审批流程
docs/design/2026-05-27-system-design.md:2723:- 并发用户：500（峰值负载）
docs/design/2026-05-27-system-design.md:2732:class GraduationLeaveUser(HttpUser):
docs/design/2026-05-27-system-design.md:2736:    def view_applications(self):
docs/design/2026-05-27-system-design.md:2737:        self.client.get("/api/v1/applications")
docs/design/2026-05-27-system-design.md:2741:        self.client.get("/api/v1/applications/1")
docs/design/2026-05-27-system-design.md:2750:  - 在线用户：500人
docs/design/2026-05-27-system-design.md:2772:6. 配置微信公众号
docs/design/2026-05-27-system-design.md:2779:- 业务指标：申请数量、审批时效
docs/design/2026-05-27-system-design.md:2787:- 审批超时 > 10个
docs/design/2026-05-27-system-design.md:2794:3. 微信通知依赖外部服务（需配置降级策略）

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 数据对接字段补充 - 最终共识

**日期：** 2026-05-27  
**参与方：** Codex (GPT-5.5) + Claude Opus 4.7

---

## 一、审查结论

**状态：** 已修复所有问题，达成共识

**修改内容：**
1. ✓ 统一class_name字段必填性标注为"可选"
2. ✓ 修正Excel示例表格列错位
3. ✓ 统一系统设计文档字段命名

---

## 二、已完成的修复

### 修复1：class_name标注为可选

**文件：** `docs/数据对接说明文档.md:105`

**修改前：**
```
| class_name | String | 班级 | "计算机2020级1班" |
```

**修改后：**
```
| class_name | String | 班级（可选） | "计算机2020级1班" |
```

**理由：** 与文件导入字段表保持一致，宿舍系统可能无法提供班级信息。

---

### 修复2：Excel示例列对齐

**文件：** `docs/数据对接说明文档.md:241`

**修改前：**
```
| 2020010102 | 李四 | 计算机2020级1班 | 1号楼 | 102 | 2 | 否 |  |  | 未开始 | 尚未办理清退手续 |
```
（11列，多出1个空列）

**修改后：**
```
| 2020010102 | 李四 | 计算机2020级1班 | 1号楼 | 102 | 2 | 否 |  | 未开始 | 尚未办理清退手续 |
```
（10列，与表头一致）

**理由：** 确保所有行列数一致，避免用户填写数据时产生混淆。

---

### 修复3：统一字段命名

**文件：** `docs/design/2026-05-27-system-design.md:1629-1642`

**修改前：**
```json
{
  "code": 200,
  "data": {
    "student_id": "2020001",
    "name": "张三",
    "class_name": "计算机2020级1班",
    "is_cleared": true,
    "clearance_date": "2026-05-25",
    "room_no": "A101",
    "bed_number": "1"
  }
}
```

**修改后：**
```json
{
  "code": 200,
  "data": {
    "student_id": "2020001",
    "name": "张三",
    "class_name": "计算机2020级1班",
    "dorm_building": "1号楼",
    "dorm_room": "101",
    "bed_number": "1",
    "is_checked_out": true,
    "checkout_date": "2026-05-25",
    "checkout_status": "completed"
  }
}
```

**字段映射：**
- `is_cleared` → `is_checked_out`
- `clearance_date` → `checkout_date`
- `room_no` → `dorm_building` + `dorm_room`
- 新增 `checkout_status`

**理由：** 统一为数据对接文档的命名规范，确保前后端实现一致。

---

## 三、最终字段定义

### API响应字段（统一版本）

| 字段名 | 类型 | 说明 | 必填 | 示例 |
|--------|------|------|------|------|
| student_id | String | 学号 | 是 | "2020010101" |
| name | String | 姓名 | 是 | "张三" |
| class_name | String | 班级 | **否** | "计算机2020级1班" |
| dorm_building | String | 宿舍楼栋 | 是 | "1号楼" |
| dorm_room | String | 宿舍房间号 | 是 | "101" |
| bed_number | String | 床号 | **否** | "1" |
| is_checked_out | Boolean | 是否已清退 | 是 | true |
| checkout_date | String | 清退日期 | 否 | "2026-05-25" |
| checkout_status | String | 清退状态 | 是 | "completed" |

**可选字段说明：**
- `class_name`：宿舍系统可能无法提供班级信息
- `bed_number`：部分宿舍系统无床号管理
- `checkout_date`：未清退时为null

---

## 四、数据库存储决策

### class_name字段
- **决策：** 不在applications表存储
- **理由：** users表已有，避免冗余

### bed_number字段
- **决策：** 暂不存储
- **理由：** 当前只用于验证，后续按需添加

---

## 五、文档一致性确认

**已更新文档：**
- ✓ `docs/数据对接说明文档.md` - API字段定义
- ✓ `docs/数据对接说明文档.md` - Excel示例
- ✓ `docs/数据对接说明文档.md` - 文件导入字段表
- ✓ `docs/templates/宿舍清退数据模板.csv` - CSV模板
- ✓ `docs/design/2026-05-27-system-design.md` - 系统设计API定义

**字段命名统一：**
- ✓ 所有文档使用相同字段名
- ✓ 所有文档必填性标注一致
- ✓ 所有示例数据格式一致

---

## 六、审查通过确认

**Codex审查：** 3个P2问题已全部修复  
**Claude确认：** 所有修改已应用并验证  
**最终状态：** 通过

**可以进入实施阶段。**

---

**共识达成时间：** 2026-05-27  
**文档版本：** v1.0（最终版）

exec
/bin/bash -lc "rtk sed -n '1,220p' docs/templates/学生基本信息导入模板.csv && rtk sed -n '1,220p' docs/templates/辅导员基本信息导入模板.csv && rtk sed -n '1,220p' docs/templates/班级辅导员对应关系导入模板.csv && rtk sed -n '1,220p' docs/templates/宿舍清退数据模板.csv" in /home/caohui/projects/graduation-leave-system
 succeeded in 127ms:
学号,姓名,班级,宿舍楼栋,宿舍房间号,床号,是否已清退,清退日期,清退状态,备注
2020010101,张三,计算机2020级1班,1号楼,101,1,是,2026-05-20,已完成,已完成清退，物品已搬离
2020010102,李四,计算机2020级1班,1号楼,102,2,否,,未开始,尚未办理清退手续
2020010103,王五,计算机2020级2班,2号楼,201,1,是,2026-05-21,已完成,已完成清退

codex
对照材料里有两个需要特别指出的事实：共识文档的 P0 范围基本完整，但“DB优先”不应无差别推荐给非宿管数据，因为学生和辅导员数据来源更可能是教务/人事或台账；另外文档面向“宿管系统方”时，部分问题已经超出宿管职责，需要改成多系统数据负责人反馈。
exec
/bin/bash -lc "rtk test -f docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md && rtk sed -n '1,220p' docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md || true" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
OUTPUT (last 5 lines):
  sh: 0: Illegal option - 


exec
/bin/bash -lc "rtk sed -n '255,360p' docs/design/2026-05-27-system-design.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
### 2.2 用户表（users）

**说明：** 以下SQL为概念示例，使用类MySQL语法便于阅读。实际实现以Django Model为准，Django ORM会自动生成符合PostgreSQL的DDL语句。

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(20) UNIQUE NOT NULL COMMENT '学号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    password_hash VARCHAR(255) COMMENT '密码哈希',
    wechat_openid VARCHAR(100) UNIQUE COMMENT '微信OpenID',
    
    -- 认证安全字段
    password_setup_required BOOLEAN DEFAULT FALSE COMMENT '需要设置密码',
    account_locked BOOLEAN DEFAULT FALSE COMMENT '账户锁定',
    failed_login_attempts INT DEFAULT 0 COMMENT '失败登录次数',
    last_login_at TIMESTAMP COMMENT '最后登录时间',
    last_login_ip VARCHAR(50) COMMENT '最后登录IP',
    wechat_bind_time TIMESTAMP COMMENT '微信绑定时间',
    password_changed_at TIMESTAMP COMMENT '密码修改时间',
    
    phone VARCHAR(20) COMMENT '手机号',
    email VARCHAR(100) COMMENT '邮箱',
    role VARCHAR(20) NOT NULL COMMENT '角色: student/counselor/admin',
    department VARCHAR(100) COMMENT '院系',
    major VARCHAR(100) COMMENT '专业',
    class_name VARCHAR(50) COMMENT '班级',
    grade INT COMMENT '年级',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    is_deleted BOOLEAN DEFAULT FALSE COMMENT '是否删除',
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    
    INDEX idx_student_id (student_id),
    INDEX idx_role (role),
    INDEX idx_wechat_openid (wechat_openid),
    INDEX idx_account_locked (account_locked),
    
    CONSTRAINT chk_auth_method CHECK (
        (password_hash IS NOT NULL) OR (wechat_openid IS NOT NULL)
    )
) COMMENT='用户表';
```

**字段说明：**
- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
- `wechat_openid`: 微信授权登录后绑定
- `is_deleted`: 软删除标记

### 2.3 离校申请表（applications）

```sql
CREATE TABLE applications (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    application_no VARCHAR(50) UNIQUE NOT NULL COMMENT '申请编号',
    student_id BIGINT NOT NULL COMMENT '学生ID',
    
    -- 固定审批人追踪
    counselor_id BIGINT COMMENT '辅导员ID',
    admin_id BIGINT COMMENT '学工部管理员ID',
    
    planned_leave_date DATE NOT NULL COMMENT '计划离校日期',
    status VARCHAR(20) NOT NULL COMMENT '状态',
    current_approver_id BIGINT COMMENT '当前审批人ID',
    submit_time TIMESTAMP COMMENT '提交时间',
    complete_time TIMESTAMP COMMENT '完成时间',
    reject_reason TEXT COMMENT '驳回原因',
    remarks TEXT COMMENT '备注',
    
    -- 凭证追踪
    certificate_url VARCHAR(500) COMMENT '离校凭证URL',
    certificate_generated_at TIMESTAMP COMMENT '凭证生成时间',
    
    -- 乐观锁
    version INT DEFAULT 0 COMMENT '版本号',
    
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE PROTECT,
    FOREIGN KEY (counselor_id) REFERENCES users(id) ON DELETE PROTECT,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE PROTECT,
    FOREIGN KEY (current_approver_id) REFERENCES users(id) ON DELETE PROTECT,
    
    INDEX idx_student_id (student_id),
    INDEX idx_counselor_id (counselor_id),
    INDEX idx_admin_id (admin_id),
    INDEX idx_status (status),
    INDEX idx_application_no (application_no),
    INDEX idx_planned_leave_date (planned_leave_date),
    INDEX idx_approver_status (current_approver_id, status, submit_time),
    INDEX idx_student_status (student_id, status, created_at),
    INDEX idx_status_deleted (status, is_deleted, submit_time)
) COMMENT='离校申请表';
```

**状态枚举（status）：**
- `draft` - 草稿
- `pending_counselor` - 待辅导员审核
- `pending_admin` - 待学工部备案
- `approved` - 审批通过
- `rejected` - 已驳回

**申请编号规则：**
`LX{YYYYMMDD}{6位序号}` 例如：LX202605270000001

exec
/bin/bash -lc "rtk sed -n '1416,1432p' docs/design/2026-05-27-system-design.md && rtk sed -n '1583,1590p' docs/design/2026-05-27-system-design.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:

**节点1：学生提交申请**
- 触发条件：学生填写完整信息并上传附件
- 前置校验：
  - 计划离校日期 ≥ 当前日期 + 3个工作日
  - 必须上传宿舍清退证明
  - 必须上传图书馆清书证明
  - 必须上传财务结清截图
- 执行动作：
  - 状态变更：draft → pending_counselor
  - 生成申请编号（LX{YYYYMMDD}{6位序号}）
  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
  - 设置当前审批人：current_approver_id = counselor_id
  - 初始化版本：version = 0
  - 记录提交时间：submit_time
  - 创建历史快照：applications_history（version=0, change_reason='提交申请'）
  - 记录审计日志：audit_logs（action='create_application', resource_type='application'）
- 第1次：办理时限到期时通知审批人
- 第2次：超时4小时后通知审批人上级
- 第3次：超时8小时后通知系统管理员

**降级策略：**
- 外部系统（宿舍管理系统）不可用时，允许手动上传证明文件
- 审批人可选择"跳过验证"并备注原因
- 系统记录降级操作日志

exec
/bin/bash -lc 'rtk ls docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md' in /home/caohui/projects/graduation-leave-system
 exited 2 in 0ms:
ls: cannot access 'docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md': No such file or directory

codex
字段层面还有一处和既有共识不一致：宿舍清退字段在 `31` 中把 `checkout_status` 设为可选，但之前字段共识把它作为 API 响应必填枚举。审查文件会把这类问题归成“提交前建议修订”，避免文档带着不一致出去。
codex
我现在会写入审查结果文件，结论采用“内容方向通过，但不建议原样提交；完成少量修订后可提交”的口径，并附上可直接替换到共识文档里的修改建议。
apply patch
patch: completed
/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
diff --git a/docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md b/docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
new file mode 100644
index 0000000000000000000000000000000000000000..404cdb7a4782fe6833890342d4c3111809b9f0a8
--- /dev/null
+++ b/docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
@@ -0,0 +1,316 @@
+# 数据源需求共识文档审查结果
+
+**审查时间：** 2026-05-27  
+**审查对象：** `31-data-source-requirements-consensus.md`  
+**参考材料：** `30-codex-data-source-review.md`、`25-class-bed-field-consensus.md`、`docs/用户设计说明书.md`、`docs/design/2026-05-27-system-design.md`、`docs/数据对接说明文档.md`、`docs/templates/*.csv`
+
+---
+
+## 一、总体结论
+
+**结论：文档方向正确，P0 数据源基本完整；但不建议原样提交给用户。**
+
+建议先做一轮小范围修订后再提交，主要原因是：
+
+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
+2. 对接方式里对学生、辅导员、班级映射默认写“DB 优先”偏激进。首版更合理的路径是：账号与映射数据优先 CSV/Excel 批量导入，宿舍清退优先 API。
+3. 宿舍清退字段与上一轮字段共识存在轻微不一致：`checkout_status` 在本文件中标为可选，但既有字段共识中 API 响应建议必填。
+4. 缺少若干实施级关键问题，例如账号标识映射、终审管理员分配规则、同步覆盖策略、历史审批人不被后续映射变更自动改写等。
+
+修订上述问题后，文档可以作为数据对接需求初稿提交。
+
+---
+
+## 二、数据源完整性审查
+
+### 2.1 P0 数据源覆盖情况
+
+当前 P0 数据源覆盖了系统运行所需的核心闭环：
+
+| 数据源 | 审查结论 | 说明 |
+|--------|----------|------|
+| 学生基本信息 | 完整 | 支撑学生账号、身份识别、班级映射、毕业届别筛选。 |
+| 宿舍清退数据 | 完整 | 支撑提交前置校验，是当前已明确需要自动校验的数据。 |
+| 辅导员基本信息 | 完整 | 支撑辅导员账号和一级审批主体。 |
+| 班级-辅导员对应关系 | 完整且必要 | 是自动分配 `counselor_id` 和权限边界的关键数据。 |
+| 学工部管理员信息 | P1 合理 | 人数少，手动创建比外部对接更合理。 |
+
+### 2.2 未遗漏的部分
+
+图书馆清书状态、财务结清状态、独立学籍状态没有列为 P0 是合理的。当前用户设计和系统设计仍保留截图上传、人工审核和宿舍系统异常时人工降级的方案，因此这三类不应阻塞首版上线。
+
+### 2.3 建议补充的“非数据源但上线必需项”
+
+以下不是外部数据源，但应在文档中补充为实施前提或配置项：
+
+1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
+2. **离校批次配置。** 包括毕业届别、开放申请时间、允许计划离校日期范围。这些可由系统后台配置，不必来自外部系统。
+3. **账号标识映射。** 当前系统设计中的 `users.student_id` 被用作唯一登录标识，但共识文档给辅导员和管理员使用 `employee_id`。需要明确导入时 `employee_id` 映射到哪个内部字段，或后续模型是否新增统一的 `external_id/employee_id`。
+
+---
+
+## 三、字段定义合理性审查
+
+### 3.1 学生基本信息
+
+字段整体合理，能支撑首版业务。`student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`is_graduating` 作为必填基本可接受。
+
+建议调整：
+
+1. `is_graduating` 建议改名或补充为 `eligible_for_leave` / `graduation_status`。  
+   仅“是否毕业生”不足以表达延期毕业、结业、休学、退学、已毕业归档等异常状态。首版可以保留 `is_graduating`，但建议增加一个更直接的离校资格字段。
+
+2. `graduation_year` 示例应与当前项目日期保持一致。  
+   文档创建时间为 2026-05-27，但 SQL 示例使用 `graduation_year = 2024`。建议统一为 `2026` 或说明“示例年份按实际毕业届别替换”。
+
+3. `phone` 是否可选需要结合微信绑定策略确认。  
+   如果登录只依赖学号密码和微信 OAuth，手机号可选合理；如果要支持短信验证、密码找回或紧急联系，手机号应至少在导入模板中强烈建议提供。
+
+### 3.2 宿舍清退数据
+
+核心字段完整，但必填性需要和既有共识统一。
+
+建议调整：
+
+1. `checkout_status` 建议改为必填，且给出枚举：`completed`、`pending`、`not_started`、`unknown`。  
+   既有字段共识已将 `checkout_status` 作为 API 响应必填字段，本文件标为可选会造成实现歧义。
+
+2. `checkout_date` 应明确条件必填：当 `is_checked_out = true` 或 `checkout_status = completed` 时必填，未清退时允许为空。
+
+3. `dorm_building`、`dorm_room`、`bed_number` 可选是可接受的，但应说明这些字段仅用于展示、核对和异常排查，业务判定不得依赖床位文本匹配。
+
+4. 应补充 `source_updated_at`。  
+   对 API 或 CSV 数据都建议记录外部系统数据更新时间，便于区分“未完成清退”和“数据过期/未同步”。
+
+### 3.3 辅导员基本信息
+
+字段基本可用，但有两个风险点：
+
+1. `phone` 标为必填偏强。  
+   如果通知主要走微信，手机号可作为推荐字段而非硬性 P0。若学校确实要求短信/电话通知，则保留必填也合理。建议在文档中说明依据。
+
+2. 缺少账号生命周期字段说明。  
+   `is_active` 已有，但应补充离职、调岗、停用后如何处理其名下未完成审批，以及是否允许历史审批记录继续引用已停用账号。
+
+### 3.4 班级-辅导员对应关系
+
+该章节是文档中最关键、也最合理的部分。`class_id` 作为必填是正确的，避免只靠班级名称匹配。
+
+建议补充：
+
+1. **一班多辅导员场景。** 首版可以要求一个主辅导员，但应明确是否允许同一班级多名辅导员、代理辅导员或临时改派。
+2. **有效期字段。** `effective_term` 可选略弱，建议至少支持 `effective_start_date` / `effective_end_date` 或说明同一届首版只按当前有效映射导入。
+3. **历史一致性规则。** 班级映射变更后，不应自动改写已提交申请中的 `counselor_id`；已提交申请如需改派，应由管理员显式操作并记录审计日志。
+
+### 3.5 学工部管理员信息
+
+手动创建是合理方案。建议补充：
+
+1. 管理员账号创建、停用、重置密码、角色授权和审计要求。
+2. 默认终审人或终审组配置规则。
+3. 管理员离岗后未完成审批任务如何转交。
+
+---
+
+## 四、对接方式可行性审查
+
+### 4.1 当前优先级评价
+
+| 数据源 | 当前写法 | 审查意见 |
+|--------|----------|----------|
+| 学生基本信息 | DB 优先 / API 备选 / CSV 降级 | 建议改为 CSV/Excel 首版优先，DB/API 作为条件成熟后的增强。 |
+| 宿舍清退数据 | API 优先 / DB 备选 / CSV 降级 | 合理。提交前置校验对实时性要求更高，API 价值最大。 |
+| 辅导员基本信息 | DB 优先 / API 备选 / CSV 降级 | 建议改为 CSV/Excel 或手动批量维护优先，人数少且变化低频。 |
+| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
+| 学工部管理员信息 | 手动创建 | 合理。 |
+
+### 4.2 技术要求清晰度
+
+DB、API、CSV 三种方式的技术要求整体清晰，但建议补充：
+
+1. DB 直连只建议在同一内网、安全边界清晰、能提供只读视图的情况下使用。
+2. DB 直连不要直接暴露生产业务表，建议由数据源系统提供只读视图或同步库。
+3. API 需补充分页、增量同步、错误码、限流、重试、幂等和测试环境要求。
+4. CSV 需补充导入覆盖策略：全量覆盖、增量更新、软删除/停用、重复数据处理、失败回滚。
+
+### 4.3 安全措施充分性
+
+已有只读账号、IP 白名单、专用账号、定期换密等措施，方向正确。建议增加：
+
+1. 密钥、数据库密码必须加密存储，不得写入代码仓库或明文配置。
+2. CSV 通过 SFTP 或后台上传时应限制权限，并记录上传人、文件哈希、导入批次和导入结果。
+3. 数据最小化：不采集身份证号、家庭住址、欠费明细、图书借阅明细等高敏字段。
+4. 外部系统异常时要区分“未完成”“查询失败”“数据过期”“人工证明待审”，不能统一判定为不通过。
+
+---
+
+## 五、数据量估算审查
+
+### 5.1 当前估算是否合理
+
+| 数据项 | 当前估算 | 审查结论 |
+|--------|----------|----------|
+| 学生 | 约 1000 人/届 | 合理，但需注明是“当届毕业生”。用户设计说明书中另有“学生用户 10,000 人”的容量指标，二者不冲突。 |
+| 辅导员 | 约 50 人 | 合理。 |
+| 班级映射 | 约 50 条 | 基本合理，但取决于班级粒度和是否存在多辅导员/代理关系。 |
+| 学工部管理员 | 约 5 人 | 合理。 |
+
+### 5.2 建议补充说明
+
+1. 若系统只导入当届毕业生，1000 人规模合理。
+2. 若系统保留多届历史或提前导入低年级学生，容量应按 10,000 学生账号设计。
+3. 班级映射数量不应只按班级数估算；若一个班有主辅导员、代理辅导员、历史有效期，则映射记录可能多于 50 条。
+
+---
+
+## 六、待反馈问题审查
+
+当前问题覆盖了数据库、API、CSV 和数据范围，基本可用，但建议扩展为面向多方的数据确认清单。
+
+### 6.1 建议修改提问对象
+
+将“请宿管系统方反馈以下问题”改为：
+
+> 请教务系统、人事系统、学工部数据负责人、宿管系统方分别确认其可提供的数据范围、字段、对接方式和联系人。
+
+原因：学生、辅导员、班级映射通常不是宿管系统的权责数据。
+
+### 6.2 建议新增问题
+
+1. 学生数据来源是否为教务系统？是否能只提供当届毕业生名单？
+2. 是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
+3. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
+4. 辅导员工号是否全校唯一？是否与统一身份认证、人事系统工号一致？
+5. 是否存在一个班级多个辅导员、代理辅导员、临时负责人或辅导员调岗场景？
+6. 班级-辅导员映射变更频率如何？是否能提供当前有效映射和历史有效期？
+7. 学工部终审人是固定个人、固定角色组、轮值还是人工分配？
+8. 各数据源能否提供测试数据、测试环境和字段字典？
+9. CSV 导入时是否采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
+10. 外部系统不可用、数据延迟或查询失败时，业务上允许怎样的人工降级？
+11. 是否有统一身份认证或微信绑定前置要求？是否需要导入手机号/邮箱用于找回密码或二次验证？
+12. 数据提供方能否承诺导出频率、数据更新时间、联系人和故障响应时间？
+
+---
+
+## 七、实施建议审查
+
+### 7.1 推荐方案
+
+共识文档中的推荐方案整体合理，但“如果宿管系统数据库包含所有数据”这个前提不够现实。学生、辅导员、班级映射不应假设都在宿管系统数据库中。
+
+建议改为：
+
+1. 宿舍清退：优先使用宿管系统 API；若不可用，使用每日 CSV 导入；异常时保留人工证明。
+2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
+3. 辅导员信息：首版优先 CSV/Excel 或后台批量维护；若有统一身份或人事 API，再对接。
+4. 班级-辅导员映射：首版优先 CSV/Excel 强校验，上线前必须 100% 覆盖当届学生。
+5. 学工部管理员：手动创建，同时配置默认终审人或终审组。
+
+### 7.2 最小可行方案
+
+共识文档的最小可行方案合理，可以保留。建议补充两个验收条件：
+
+1. 当届所有可申请学生必须能解析到有效辅导员。
+2. 提交申请时必须能解析到有效终审管理员或终审组。
+
+### 7.3 更好的实施路径
+
+建议按以下顺序实施：
+
+1. 先确认数据权责方和联系人，不把所有问题都压给宿管系统。
+2. 先落地三份基础 CSV/Excel 模板：学生、辅导员、班级-辅导员映射。
+3. 实现导入校验报告，重点校验学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射。
+4. 再对接宿舍清退 API，并把 API 失败、超时、数据过期纳入统一降级处理。
+5. 上线前冻结当届数据批次，完成一次全量导入演练和异常清单清零。
+6. 上线后根据数据变更频率决定是否将学生、辅导员、映射数据升级为 API 或 DB 同步。
+
+---
+
+## 八、具体修改建议
+
+### 8.1 文档目的
+
+建议将：
+
+> 明确毕业离校系统所需的数据源，提交给宿管系统方反馈
+
+修改为：
+
+> 明确毕业离校系统所需的数据源，提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人反馈。
+
+### 8.2 数据源概述表
+
+建议将学生、辅导员、班级映射的对接方式调整为：
+
+| 数据源 | 建议对接方式 |
+|--------|--------------|
+| 学生基本信息 | CSV/Excel 首版优先 / API 或 DB 视图增强 |
+| 辅导员基本信息 | CSV/Excel 或后台批量维护首版优先 / 人事或统一身份 API 增强 |
+| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
+| 宿舍清退数据 | API 优先 / DB 只读视图备选 / CSV 降级 |
+
+### 8.3 学生字段
+
+建议在学生基本信息中增加：
+
+| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
+|---------------|---------------|----------|------|------|------|
+| 离校申请资格 | eligible_for_leave | 布尔 | 建议是 | 是否允许提交本批次离校申请 | true |
+| 学籍/毕业状态 | graduation_status | 文本 | 否 | graduating/delayed/graduated/suspended/withdrawn | graduating |
+
+如不新增字段，至少应说明 `is_graduating=true` 即表示具备本批次离校申请资格。
+
+### 8.4 宿舍清退字段
+
+建议将：
+
+| 字段 | 当前 | 建议 |
+|------|------|------|
+| checkout_status | 可选 | 必填，枚举：completed/pending/not_started/unknown |
+| checkout_date | 可选 | 条件必填：completed 时必填 |
+| source_updated_at | 未列出 | 建议新增，记录外部系统数据更新时间 |
+
+### 8.5 辅导员字段
+
+建议补充说明：
+
+1. `employee_id` 必须全校唯一，并与班级映射中的 `counselor_employee_id` 完全一致。
+2. `phone` 是否必填取决于通知和找回密码方案；如果不依赖短信，可改为建议字段。
+3. `is_active=false` 时不再分配新申请，但历史审批记录仍保留。
+
+### 8.6 班级映射字段
+
+建议增加或说明：
+
+| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 |
+|---------------|---------------|----------|------|------|
+| 是否主辅导员 | is_primary | 布尔 | 否 | 多辅导员场景下标识主审批人 |
+| 生效开始日期 | effective_start_date | 日期 | 否 | 映射开始生效时间 |
+| 生效结束日期 | effective_end_date | 日期 | 否 | 映射结束时间，空表示当前有效 |
+
+首版如果只支持一班一主辅导员，也应在文档中明确限制。
+
+### 8.7 待反馈问题
+
+建议在第七章新增“数据权责方确认”：
+
+1. 每个数据源的权责系统和业务负责人是谁？
+2. 每个数据源由哪一方提供字段字典、测试数据和生产数据？
+3. 每个数据源的联系人、故障响应方式和上线前联调窗口是什么？
+
+---
+
+## 九、最终审查结论
+
+`31-data-source-requirements-consensus.md` 已经覆盖首版上线所需的主要 P0 数据源，字段设计也基本能支撑业务。它可以作为对接需求基础稿。
+
+但在提交给用户或外部系统方之前，建议至少完成以下 5 项修改：
+
+1. 将反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
+2. 将学生、辅导员、班级映射的首版推荐方式从“DB 优先”调整为“CSV/Excel 优先，API/DB 增强”。
+3. 统一宿舍清退字段必填性，特别是 `checkout_status`。
+4. 补充终审管理员/终审组配置、账号标识映射、历史审批人一致性规则。
+5. 在待反馈问题中增加数据权责、测试数据、同步策略、异常降级和多辅导员场景确认。
+
+完成上述修改后，文档可以提交。
+

diff --git a/docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md b/docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
new file mode 100644
index 0000000000000000000000000000000000000000..404cdb7a4782fe6833890342d4c3111809b9f0a8
--- /dev/null
+++ b/docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
@@ -0,0 +1,316 @@
+# 数据源需求共识文档审查结果
+
+**审查时间：** 2026-05-27  
+**审查对象：** `31-data-source-requirements-consensus.md`  
+**参考材料：** `30-codex-data-source-review.md`、`25-class-bed-field-consensus.md`、`docs/用户设计说明书.md`、`docs/design/2026-05-27-system-design.md`、`docs/数据对接说明文档.md`、`docs/templates/*.csv`
+
+---
+
+## 一、总体结论
+
+**结论：文档方向正确，P0 数据源基本完整；但不建议原样提交给用户。**
+
+建议先做一轮小范围修订后再提交，主要原因是：
+
+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
+2. 对接方式里对学生、辅导员、班级映射默认写“DB 优先”偏激进。首版更合理的路径是：账号与映射数据优先 CSV/Excel 批量导入，宿舍清退优先 API。
+3. 宿舍清退字段与上一轮字段共识存在轻微不一致：`checkout_status` 在本文件中标为可选，但既有字段共识中 API 响应建议必填。
+4. 缺少若干实施级关键问题，例如账号标识映射、终审管理员分配规则、同步覆盖策略、历史审批人不被后续映射变更自动改写等。
+
+修订上述问题后，文档可以作为数据对接需求初稿提交。
+
+---
+
+## 二、数据源完整性审查
+
+### 2.1 P0 数据源覆盖情况
+
+当前 P0 数据源覆盖了系统运行所需的核心闭环：
+
+| 数据源 | 审查结论 | 说明 |
+|--------|----------|------|
+| 学生基本信息 | 完整 | 支撑学生账号、身份识别、班级映射、毕业届别筛选。 |
+| 宿舍清退数据 | 完整 | 支撑提交前置校验，是当前已明确需要自动校验的数据。 |
+| 辅导员基本信息 | 完整 | 支撑辅导员账号和一级审批主体。 |
+| 班级-辅导员对应关系 | 完整且必要 | 是自动分配 `counselor_id` 和权限边界的关键数据。 |
+| 学工部管理员信息 | P1 合理 | 人数少，手动创建比外部对接更合理。 |
+
+### 2.2 未遗漏的部分
+
+图书馆清书状态、财务结清状态、独立学籍状态没有列为 P0 是合理的。当前用户设计和系统设计仍保留截图上传、人工审核和宿舍系统异常时人工降级的方案，因此这三类不应阻塞首版上线。
+
+### 2.3 建议补充的“非数据源但上线必需项”
+
+以下不是外部数据源，但应在文档中补充为实施前提或配置项：
+
+1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
+2. **离校批次配置。** 包括毕业届别、开放申请时间、允许计划离校日期范围。这些可由系统后台配置，不必来自外部系统。
+3. **账号标识映射。** 当前系统设计中的 `users.student_id` 被用作唯一登录标识，但共识文档给辅导员和管理员使用 `employee_id`。需要明确导入时 `employee_id` 映射到哪个内部字段，或后续模型是否新增统一的 `external_id/employee_id`。
+
+---
+
+## 三、字段定义合理性审查
+
+### 3.1 学生基本信息
+
+字段整体合理，能支撑首版业务。`student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`is_graduating` 作为必填基本可接受。
+
+建议调整：
+
+1. `is_graduating` 建议改名或补充为 `eligible_for_leave` / `graduation_status`。  
+   仅“是否毕业生”不足以表达延期毕业、结业、休学、退学、已毕业归档等异常状态。首版可以保留 `is_graduating`，但建议增加一个更直接的离校资格字段。
+
+2. `graduation_year` 示例应与当前项目日期保持一致。  
+   文档创建时间为 2026-05-27，但 SQL 示例使用 `graduation_year = 2024`。建议统一为 `2026` 或说明“示例年份按实际毕业届别替换”。
+
+3. `phone` 是否可选需要结合微信绑定策略确认。  
+   如果登录只依赖学号密码和微信 OAuth，手机号可选合理；如果要支持短信验证、密码找回或紧急联系，手机号应至少在导入模板中强烈建议提供。
+
+### 3.2 宿舍清退数据
+
+核心字段完整，但必填性需要和既有共识统一。
+
+建议调整：
+
+1. `checkout_status` 建议改为必填，且给出枚举：`completed`、`pending`、`not_started`、`unknown`。  
+   既有字段共识已将 `checkout_status` 作为 API 响应必填字段，本文件标为可选会造成实现歧义。
+
+2. `checkout_date` 应明确条件必填：当 `is_checked_out = true` 或 `checkout_status = completed` 时必填，未清退时允许为空。
+
+3. `dorm_building`、`dorm_room`、`bed_number` 可选是可接受的，但应说明这些字段仅用于展示、核对和异常排查，业务判定不得依赖床位文本匹配。
+
+4. 应补充 `source_updated_at`。  
+   对 API 或 CSV 数据都建议记录外部系统数据更新时间，便于区分“未完成清退”和“数据过期/未同步”。
+
+### 3.3 辅导员基本信息
+
+字段基本可用，但有两个风险点：
+
+1. `phone` 标为必填偏强。  
+   如果通知主要走微信，手机号可作为推荐字段而非硬性 P0。若学校确实要求短信/电话通知，则保留必填也合理。建议在文档中说明依据。
+
+2. 缺少账号生命周期字段说明。  
+   `is_active` 已有，但应补充离职、调岗、停用后如何处理其名下未完成审批，以及是否允许历史审批记录继续引用已停用账号。
+
+### 3.4 班级-辅导员对应关系
+
+该章节是文档中最关键、也最合理的部分。`class_id` 作为必填是正确的，避免只靠班级名称匹配。
+
+建议补充：
+
+1. **一班多辅导员场景。** 首版可以要求一个主辅导员，但应明确是否允许同一班级多名辅导员、代理辅导员或临时改派。
+2. **有效期字段。** `effective_term` 可选略弱，建议至少支持 `effective_start_date` / `effective_end_date` 或说明同一届首版只按当前有效映射导入。
+3. **历史一致性规则。** 班级映射变更后，不应自动改写已提交申请中的 `counselor_id`；已提交申请如需改派，应由管理员显式操作并记录审计日志。
+
+### 3.5 学工部管理员信息
+
+手动创建是合理方案。建议补充：
+
+1. 管理员账号创建、停用、重置密码、角色授权和审计要求。
+2. 默认终审人或终审组配置规则。
+3. 管理员离岗后未完成审批任务如何转交。
+
+---
+
+## 四、对接方式可行性审查
+
+### 4.1 当前优先级评价
+
+| 数据源 | 当前写法 | 审查意见 |
+|--------|----------|----------|
+| 学生基本信息 | DB 优先 / API 备选 / CSV 降级 | 建议改为 CSV/Excel 首版优先，DB/API 作为条件成熟后的增强。 |
+| 宿舍清退数据 | API 优先 / DB 备选 / CSV 降级 | 合理。提交前置校验对实时性要求更高，API 价值最大。 |
+| 辅导员基本信息 | DB 优先 / API 备选 / CSV 降级 | 建议改为 CSV/Excel 或手动批量维护优先，人数少且变化低频。 |
+| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
+| 学工部管理员信息 | 手动创建 | 合理。 |
+
+### 4.2 技术要求清晰度
+
+DB、API、CSV 三种方式的技术要求整体清晰，但建议补充：
+
+1. DB 直连只建议在同一内网、安全边界清晰、能提供只读视图的情况下使用。
+2. DB 直连不要直接暴露生产业务表，建议由数据源系统提供只读视图或同步库。
+3. API 需补充分页、增量同步、错误码、限流、重试、幂等和测试环境要求。
+4. CSV 需补充导入覆盖策略：全量覆盖、增量更新、软删除/停用、重复数据处理、失败回滚。
+
+### 4.3 安全措施充分性
+
+已有只读账号、IP 白名单、专用账号、定期换密等措施，方向正确。建议增加：
+
+1. 密钥、数据库密码必须加密存储，不得写入代码仓库或明文配置。
+2. CSV 通过 SFTP 或后台上传时应限制权限，并记录上传人、文件哈希、导入批次和导入结果。
+3. 数据最小化：不采集身份证号、家庭住址、欠费明细、图书借阅明细等高敏字段。
+4. 外部系统异常时要区分“未完成”“查询失败”“数据过期”“人工证明待审”，不能统一判定为不通过。
+
+---
+
+## 五、数据量估算审查
+
+### 5.1 当前估算是否合理
+
+| 数据项 | 当前估算 | 审查结论 |
+|--------|----------|----------|
+| 学生 | 约 1000 人/届 | 合理，但需注明是“当届毕业生”。用户设计说明书中另有“学生用户 10,000 人”的容量指标，二者不冲突。 |
+| 辅导员 | 约 50 人 | 合理。 |
+| 班级映射 | 约 50 条 | 基本合理，但取决于班级粒度和是否存在多辅导员/代理关系。 |
+| 学工部管理员 | 约 5 人 | 合理。 |
+
+### 5.2 建议补充说明
+
+1. 若系统只导入当届毕业生，1000 人规模合理。
+2. 若系统保留多届历史或提前导入低年级学生，容量应按 10,000 学生账号设计。
+3. 班级映射数量不应只按班级数估算；若一个班有主辅导员、代理辅导员、历史有效期，则映射记录可能多于 50 条。
+
+---
+
+## 六、待反馈问题审查
+
+当前问题覆盖了数据库、API、CSV 和数据范围，基本可用，但建议扩展为面向多方的数据确认清单。
+
+### 6.1 建议修改提问对象
+
+将“请宿管系统方反馈以下问题”改为：
+
+> 请教务系统、人事系统、学工部数据负责人、宿管系统方分别确认其可提供的数据范围、字段、对接方式和联系人。
+
+原因：学生、辅导员、班级映射通常不是宿管系统的权责数据。
+
+### 6.2 建议新增问题
+
+1. 学生数据来源是否为教务系统？是否能只提供当届毕业生名单？
+2. 是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
+3. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
+4. 辅导员工号是否全校唯一？是否与统一身份认证、人事系统工号一致？
+5. 是否存在一个班级多个辅导员、代理辅导员、临时负责人或辅导员调岗场景？
+6. 班级-辅导员映射变更频率如何？是否能提供当前有效映射和历史有效期？
+7. 学工部终审人是固定个人、固定角色组、轮值还是人工分配？
+8. 各数据源能否提供测试数据、测试环境和字段字典？
+9. CSV 导入时是否采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
+10. 外部系统不可用、数据延迟或查询失败时，业务上允许怎样的人工降级？
+11. 是否有统一身份认证或微信绑定前置要求？是否需要导入手机号/邮箱用于找回密码或二次验证？
+12. 数据提供方能否承诺导出频率、数据更新时间、联系人和故障响应时间？
+
+---
+
+## 七、实施建议审查
+
+### 7.1 推荐方案
+
+共识文档中的推荐方案整体合理，但“如果宿管系统数据库包含所有数据”这个前提不够现实。学生、辅导员、班级映射不应假设都在宿管系统数据库中。
+
+建议改为：
+
+1. 宿舍清退：优先使用宿管系统 API；若不可用，使用每日 CSV 导入；异常时保留人工证明。
+2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
+3. 辅导员信息：首版优先 CSV/Excel 或后台批量维护；若有统一身份或人事 API，再对接。
+4. 班级-辅导员映射：首版优先 CSV/Excel 强校验，上线前必须 100% 覆盖当届学生。
+5. 学工部管理员：手动创建，同时配置默认终审人或终审组。
+
+### 7.2 最小可行方案
+
+共识文档的最小可行方案合理，可以保留。建议补充两个验收条件：
+
+1. 当届所有可申请学生必须能解析到有效辅导员。
+2. 提交申请时必须能解析到有效终审管理员或终审组。
+
+### 7.3 更好的实施路径
+
+建议按以下顺序实施：
+
+1. 先确认数据权责方和联系人，不把所有问题都压给宿管系统。
+2. 先落地三份基础 CSV/Excel 模板：学生、辅导员、班级-辅导员映射。
+3. 实现导入校验报告，重点校验学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射。
+4. 再对接宿舍清退 API，并把 API 失败、超时、数据过期纳入统一降级处理。
+5. 上线前冻结当届数据批次，完成一次全量导入演练和异常清单清零。
+6. 上线后根据数据变更频率决定是否将学生、辅导员、映射数据升级为 API 或 DB 同步。
+
+---
+
+## 八、具体修改建议
+
+### 8.1 文档目的
+
+建议将：
+
+> 明确毕业离校系统所需的数据源，提交给宿管系统方反馈
+
+修改为：
+
+> 明确毕业离校系统所需的数据源，提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人反馈。
+
+### 8.2 数据源概述表
+
+建议将学生、辅导员、班级映射的对接方式调整为：
+
+| 数据源 | 建议对接方式 |
+|--------|--------------|
+| 学生基本信息 | CSV/Excel 首版优先 / API 或 DB 视图增强 |
+| 辅导员基本信息 | CSV/Excel 或后台批量维护首版优先 / 人事或统一身份 API 增强 |
+| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
+| 宿舍清退数据 | API 优先 / DB 只读视图备选 / CSV 降级 |
+
+### 8.3 学生字段
+
+建议在学生基本信息中增加：
+
+| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
+|---------------|---------------|----------|------|------|------|
+| 离校申请资格 | eligible_for_leave | 布尔 | 建议是 | 是否允许提交本批次离校申请 | true |
+| 学籍/毕业状态 | graduation_status | 文本 | 否 | graduating/delayed/graduated/suspended/withdrawn | graduating |
+
+如不新增字段，至少应说明 `is_graduating=true` 即表示具备本批次离校申请资格。
+
+### 8.4 宿舍清退字段
+
+建议将：
+
+| 字段 | 当前 | 建议 |
+|------|------|------|
+| checkout_status | 可选 | 必填，枚举：completed/pending/not_started/unknown |
+| checkout_date | 可选 | 条件必填：completed 时必填 |
+| source_updated_at | 未列出 | 建议新增，记录外部系统数据更新时间 |
+
+### 8.5 辅导员字段
+
+建议补充说明：
+
+1. `employee_id` 必须全校唯一，并与班级映射中的 `counselor_employee_id` 完全一致。
+2. `phone` 是否必填取决于通知和找回密码方案；如果不依赖短信，可改为建议字段。
+3. `is_active=false` 时不再分配新申请，但历史审批记录仍保留。
+
+### 8.6 班级映射字段
+
+建议增加或说明：
+
+| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 |
+|---------------|---------------|----------|------|------|
+| 是否主辅导员 | is_primary | 布尔 | 否 | 多辅导员场景下标识主审批人 |
+| 生效开始日期 | effective_start_date | 日期 | 否 | 映射开始生效时间 |
+| 生效结束日期 | effective_end_date | 日期 | 否 | 映射结束时间，空表示当前有效 |
+
+首版如果只支持一班一主辅导员，也应在文档中明确限制。
+
+### 8.7 待反馈问题
+
+建议在第七章新增“数据权责方确认”：
+
+1. 每个数据源的权责系统和业务负责人是谁？
+2. 每个数据源由哪一方提供字段字典、测试数据和生产数据？
+3. 每个数据源的联系人、故障响应方式和上线前联调窗口是什么？
+
+---
+
+## 九、最终审查结论
+
+`31-data-source-requirements-consensus.md` 已经覆盖首版上线所需的主要 P0 数据源，字段设计也基本能支撑业务。它可以作为对接需求基础稿。
+
+但在提交给用户或外部系统方之前，建议至少完成以下 5 项修改：
+
+1. 将反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
+2. 将学生、辅导员、班级映射的首版推荐方式从“DB 优先”调整为“CSV/Excel 优先，API/DB 增强”。
+3. 统一宿舍清退字段必填性，特别是 `checkout_status`。
+4. 补充终审管理员/终审组配置、账号标识映射、历史审批人一致性规则。
+5. 在待反馈问题中增加数据权责、测试数据、同步策略、异常降级和多辅导员场景确认。
+
+完成上述修改后，文档可以提交。
+

codex
审查文件已写入。我会快速检查生成文件的开头和结尾，确认内容落盘完整、结论清晰。
exec
/bin/bash -lc 'rtk wc -l docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
316

exec
/bin/bash -lc "rtk sed -n '1,80p' docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md" in /home/caohui/projects/graduation-leave-system
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

exec
/bin/bash -lc 'rtk tail -n 60 docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
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

### 8.6 班级映射字段

建议增加或说明：

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 |
|---------------|---------------|----------|------|------|
| 是否主辅导员 | is_primary | 布尔 | 否 | 多辅导员场景下标识主审批人 |
| 生效开始日期 | effective_start_date | 日期 | 否 | 映射开始生效时间 |
| 生效结束日期 | effective_end_date | 日期 | 否 | 映射结束时间，空表示当前有效 |

首版如果只支持一班一主辅导员，也应在文档中明确限制。

### 8.7 待反馈问题

建议在第七章新增“数据权责方确认”：

1. 每个数据源的权责系统和业务负责人是谁？
2. 每个数据源由哪一方提供字段字典、测试数据和生产数据？
3. 每个数据源的联系人、故障响应方式和上线前联调窗口是什么？

---

## 九、最终审查结论

`31-data-source-requirements-consensus.md` 已经覆盖首版上线所需的主要 P0 数据源，字段设计也基本能支撑业务。它可以作为对接需求基础稿。

但在提交给用户或外部系统方之前，建议至少完成以下 5 项修改：

1. 将反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
2. 将学生、辅导员、班级映射的首版推荐方式从“DB 优先”调整为“CSV/Excel 优先，API/DB 增强”。
3. 统一宿舍清退字段必填性，特别是 `checkout_status`。
4. 补充终审管理员/终审组配置、账号标识映射、历史审批人一致性规则。
5. 在待反馈问题中增加数据权责、测试数据、同步策略、异常降级和多辅导员场景确认。

完成上述修改后，文档可以提交。


diff --git a/docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md b/docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
new file mode 100644
index 0000000000000000000000000000000000000000..404cdb7a4782fe6833890342d4c3111809b9f0a8
--- /dev/null
+++ b/docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
@@ -0,0 +1,316 @@
+# 数据源需求共识文档审查结果
+
+**审查时间：** 2026-05-27  
+**审查对象：** `31-data-source-requirements-consensus.md`  
+**参考材料：** `30-codex-data-source-review.md`、`25-class-bed-field-consensus.md`、`docs/用户设计说明书.md`、`docs/design/2026-05-27-system-design.md`、`docs/数据对接说明文档.md`、`docs/templates/*.csv`
+
+---
+
+## 一、总体结论
+
+**结论：文档方向正确，P0 数据源基本完整；但不建议原样提交给用户。**
+
+建议先做一轮小范围修订后再提交，主要原因是：
+
+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
+2. 对接方式里对学生、辅导员、班级映射默认写“DB 优先”偏激进。首版更合理的路径是：账号与映射数据优先 CSV/Excel 批量导入，宿舍清退优先 API。
+3. 宿舍清退字段与上一轮字段共识存在轻微不一致：`checkout_status` 在本文件中标为可选，但既有字段共识中 API 响应建议必填。
+4. 缺少若干实施级关键问题，例如账号标识映射、终审管理员分配规则、同步覆盖策略、历史审批人不被后续映射变更自动改写等。
+
+修订上述问题后，文档可以作为数据对接需求初稿提交。
+
+---
+
+## 二、数据源完整性审查
+
+### 2.1 P0 数据源覆盖情况
+
+当前 P0 数据源覆盖了系统运行所需的核心闭环：
+
+| 数据源 | 审查结论 | 说明 |
+|--------|----------|------|
+| 学生基本信息 | 完整 | 支撑学生账号、身份识别、班级映射、毕业届别筛选。 |
+| 宿舍清退数据 | 完整 | 支撑提交前置校验，是当前已明确需要自动校验的数据。 |
+| 辅导员基本信息 | 完整 | 支撑辅导员账号和一级审批主体。 |
+| 班级-辅导员对应关系 | 完整且必要 | 是自动分配 `counselor_id` 和权限边界的关键数据。 |
+| 学工部管理员信息 | P1 合理 | 人数少，手动创建比外部对接更合理。 |
+
+### 2.2 未遗漏的部分
+
+图书馆清书状态、财务结清状态、独立学籍状态没有列为 P0 是合理的。当前用户设计和系统设计仍保留截图上传、人工审核和宿舍系统异常时人工降级的方案，因此这三类不应阻塞首版上线。
+
+### 2.3 建议补充的“非数据源但上线必需项”
+
+以下不是外部数据源，但应在文档中补充为实施前提或配置项：
+
+1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
+2. **离校批次配置。** 包括毕业届别、开放申请时间、允许计划离校日期范围。这些可由系统后台配置，不必来自外部系统。
+3. **账号标识映射。** 当前系统设计中的 `users.student_id` 被用作唯一登录标识，但共识文档给辅导员和管理员使用 `employee_id`。需要明确导入时 `employee_id` 映射到哪个内部字段，或后续模型是否新增统一的 `external_id/employee_id`。
+
+---
+
+## 三、字段定义合理性审查
+
+### 3.1 学生基本信息
+
+字段整体合理，能支撑首版业务。`student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`is_graduating` 作为必填基本可接受。
+
+建议调整：
+
+1. `is_graduating` 建议改名或补充为 `eligible_for_leave` / `graduation_status`。  
+   仅“是否毕业生”不足以表达延期毕业、结业、休学、退学、已毕业归档等异常状态。首版可以保留 `is_graduating`，但建议增加一个更直接的离校资格字段。
+
+2. `graduation_year` 示例应与当前项目日期保持一致。  
+   文档创建时间为 2026-05-27，但 SQL 示例使用 `graduation_year = 2024`。建议统一为 `2026` 或说明“示例年份按实际毕业届别替换”。
+
+3. `phone` 是否可选需要结合微信绑定策略确认。  
+   如果登录只依赖学号密码和微信 OAuth，手机号可选合理；如果要支持短信验证、密码找回或紧急联系，手机号应至少在导入模板中强烈建议提供。
+
+### 3.2 宿舍清退数据
+
+核心字段完整，但必填性需要和既有共识统一。
+
+建议调整：
+
+1. `checkout_status` 建议改为必填，且给出枚举：`completed`、`pending`、`not_started`、`unknown`。  
+   既有字段共识已将 `checkout_status` 作为 API 响应必填字段，本文件标为可选会造成实现歧义。
+
+2. `checkout_date` 应明确条件必填：当 `is_checked_out = true` 或 `checkout_status = completed` 时必填，未清退时允许为空。
+
+3. `dorm_building`、`dorm_room`、`bed_number` 可选是可接受的，但应说明这些字段仅用于展示、核对和异常排查，业务判定不得依赖床位文本匹配。
+
+4. 应补充 `source_updated_at`。  
+   对 API 或 CSV 数据都建议记录外部系统数据更新时间，便于区分“未完成清退”和“数据过期/未同步”。
+
+### 3.3 辅导员基本信息
+
+字段基本可用，但有两个风险点：
+
+1. `phone` 标为必填偏强。  
+   如果通知主要走微信，手机号可作为推荐字段而非硬性 P0。若学校确实要求短信/电话通知，则保留必填也合理。建议在文档中说明依据。
+
+2. 缺少账号生命周期字段说明。  
+   `is_active` 已有，但应补充离职、调岗、停用后如何处理其名下未完成审批，以及是否允许历史审批记录继续引用已停用账号。
+
+### 3.4 班级-辅导员对应关系
+
+该章节是文档中最关键、也最合理的部分。`class_id` 作为必填是正确的，避免只靠班级名称匹配。
+
+建议补充：
+
+1. **一班多辅导员场景。** 首版可以要求一个主辅导员，但应明确是否允许同一班级多名辅导员、代理辅导员或临时改派。
+2. **有效期字段。** `effective_term` 可选略弱，建议至少支持 `effective_start_date` / `effective_end_date` 或说明同一届首版只按当前有效映射导入。
+3. **历史一致性规则。** 班级映射变更后，不应自动改写已提交申请中的 `counselor_id`；已提交申请如需改派，应由管理员显式操作并记录审计日志。
+
+### 3.5 学工部管理员信息
+
+手动创建是合理方案。建议补充：
+
+1. 管理员账号创建、停用、重置密码、角色授权和审计要求。
+2. 默认终审人或终审组配置规则。
+3. 管理员离岗后未完成审批任务如何转交。
+
+---
+
+## 四、对接方式可行性审查
+
+### 4.1 当前优先级评价
+
+| 数据源 | 当前写法 | 审查意见 |
+|--------|----------|----------|
+| 学生基本信息 | DB 优先 / API 备选 / CSV 降级 | 建议改为 CSV/Excel 首版优先，DB/API 作为条件成熟后的增强。 |
+| 宿舍清退数据 | API 优先 / DB 备选 / CSV 降级 | 合理。提交前置校验对实时性要求更高，API 价值最大。 |
+| 辅导员基本信息 | DB 优先 / API 备选 / CSV 降级 | 建议改为 CSV/Excel 或手动批量维护优先，人数少且变化低频。 |
+| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
+| 学工部管理员信息 | 手动创建 | 合理。 |
+
+### 4.2 技术要求清晰度
+
+DB、API、CSV 三种方式的技术要求整体清晰，但建议补充：
+
+1. DB 直连只建议在同一内网、安全边界清晰、能提供只读视图的情况下使用。
+2. DB 直连不要直接暴露生产业务表，建议由数据源系统提供只读视图或同步库。
+3. API 需补充分页、增量同步、错误码、限流、重试、幂等和测试环境要求。
+4. CSV 需补充导入覆盖策略：全量覆盖、增量更新、软删除/停用、重复数据处理、失败回滚。
+
+### 4.3 安全措施充分性
+
+已有只读账号、IP 白名单、专用账号、定期换密等措施，方向正确。建议增加：
+
+1. 密钥、数据库密码必须加密存储，不得写入代码仓库或明文配置。
+2. CSV 通过 SFTP 或后台上传时应限制权限，并记录上传人、文件哈希、导入批次和导入结果。
+3. 数据最小化：不采集身份证号、家庭住址、欠费明细、图书借阅明细等高敏字段。
+4. 外部系统异常时要区分“未完成”“查询失败”“数据过期”“人工证明待审”，不能统一判定为不通过。
+
+---
+
+## 五、数据量估算审查
+
+### 5.1 当前估算是否合理
+
+| 数据项 | 当前估算 | 审查结论 |
+|--------|----------|----------|
+| 学生 | 约 1000 人/届 | 合理，但需注明是“当届毕业生”。用户设计说明书中另有“学生用户 10,000 人”的容量指标，二者不冲突。 |
+| 辅导员 | 约 50 人 | 合理。 |
+| 班级映射 | 约 50 条 | 基本合理，但取决于班级粒度和是否存在多辅导员/代理关系。 |
+| 学工部管理员 | 约 5 人 | 合理。 |
+
+### 5.2 建议补充说明
+
+1. 若系统只导入当届毕业生，1000 人规模合理。
+2. 若系统保留多届历史或提前导入低年级学生，容量应按 10,000 学生账号设计。
+3. 班级映射数量不应只按班级数估算；若一个班有主辅导员、代理辅导员、历史有效期，则映射记录可能多于 50 条。
+
+---
+
+## 六、待反馈问题审查
+
+当前问题覆盖了数据库、API、CSV 和数据范围，基本可用，但建议扩展为面向多方的数据确认清单。
+
+### 6.1 建议修改提问对象
+
+将“请宿管系统方反馈以下问题”改为：
+
+> 请教务系统、人事系统、学工部数据负责人、宿管系统方分别确认其可提供的数据范围、字段、对接方式和联系人。
+
+原因：学生、辅导员、班级映射通常不是宿管系统的权责数据。
+
+### 6.2 建议新增问题
+
+1. 学生数据来源是否为教务系统？是否能只提供当届毕业生名单？
+2. 是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
+3. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
+4. 辅导员工号是否全校唯一？是否与统一身份认证、人事系统工号一致？
+5. 是否存在一个班级多个辅导员、代理辅导员、临时负责人或辅导员调岗场景？
+6. 班级-辅导员映射变更频率如何？是否能提供当前有效映射和历史有效期？
+7. 学工部终审人是固定个人、固定角色组、轮值还是人工分配？
+8. 各数据源能否提供测试数据、测试环境和字段字典？
+9. CSV 导入时是否采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
+10. 外部系统不可用、数据延迟或查询失败时，业务上允许怎样的人工降级？
+11. 是否有统一身份认证或微信绑定前置要求？是否需要导入手机号/邮箱用于找回密码或二次验证？
+12. 数据提供方能否承诺导出频率、数据更新时间、联系人和故障响应时间？
+
+---
+
+## 七、实施建议审查
+
+### 7.1 推荐方案
+
+共识文档中的推荐方案整体合理，但“如果宿管系统数据库包含所有数据”这个前提不够现实。学生、辅导员、班级映射不应假设都在宿管系统数据库中。
+
+建议改为：
+
+1. 宿舍清退：优先使用宿管系统 API；若不可用，使用每日 CSV 导入；异常时保留人工证明。
+2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
+3. 辅导员信息：首版优先 CSV/Excel 或后台批量维护；若有统一身份或人事 API，再对接。
+4. 班级-辅导员映射：首版优先 CSV/Excel 强校验，上线前必须 100% 覆盖当届学生。
+5. 学工部管理员：手动创建，同时配置默认终审人或终审组。
+
+### 7.2 最小可行方案
+
+共识文档的最小可行方案合理，可以保留。建议补充两个验收条件：
+
+1. 当届所有可申请学生必须能解析到有效辅导员。
+2. 提交申请时必须能解析到有效终审管理员或终审组。
+
+### 7.3 更好的实施路径
+
+建议按以下顺序实施：
+
+1. 先确认数据权责方和联系人，不把所有问题都压给宿管系统。
+2. 先落地三份基础 CSV/Excel 模板：学生、辅导员、班级-辅导员映射。
+3. 实现导入校验报告，重点校验学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射。
+4. 再对接宿舍清退 API，并把 API 失败、超时、数据过期纳入统一降级处理。
+5. 上线前冻结当届数据批次，完成一次全量导入演练和异常清单清零。
+6. 上线后根据数据变更频率决定是否将学生、辅导员、映射数据升级为 API 或 DB 同步。
+
+---
+
+## 八、具体修改建议
+
+### 8.1 文档目的
+
+建议将：
+
+> 明确毕业离校系统所需的数据源，提交给宿管系统方反馈
+
+修改为：
+
+> 明确毕业离校系统所需的数据源，提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人反馈。
+
+### 8.2 数据源概述表
+
+建议将学生、辅导员、班级映射的对接方式调整为：
+
+| 数据源 | 建议对接方式 |
+|--------|--------------|
+| 学生基本信息 | CSV/Excel 首版优先 / API 或 DB 视图增强 |
+| 辅导员基本信息 | CSV/Excel 或后台批量维护首版优先 / 人事或统一身份 API 增强 |
+| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
+| 宿舍清退数据 | API 优先 / DB 只读视图备选 / CSV 降级 |
+
+### 8.3 学生字段
+
+建议在学生基本信息中增加：
+
+| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
+|---------------|---------------|----------|------|------|------|
+| 离校申请资格 | eligible_for_leave | 布尔 | 建议是 | 是否允许提交本批次离校申请 | true |
+| 学籍/毕业状态 | graduation_status | 文本 | 否 | graduating/delayed/graduated/suspended/withdrawn | graduating |
+
+如不新增字段，至少应说明 `is_graduating=true` 即表示具备本批次离校申请资格。
+
+### 8.4 宿舍清退字段
+
+建议将：
+
+| 字段 | 当前 | 建议 |
+|------|------|------|
+| checkout_status | 可选 | 必填，枚举：completed/pending/not_started/unknown |
+| checkout_date | 可选 | 条件必填：completed 时必填 |
+| source_updated_at | 未列出 | 建议新增，记录外部系统数据更新时间 |
+
+### 8.5 辅导员字段
+
+建议补充说明：
+
+1. `employee_id` 必须全校唯一，并与班级映射中的 `counselor_employee_id` 完全一致。
+2. `phone` 是否必填取决于通知和找回密码方案；如果不依赖短信，可改为建议字段。
+3. `is_active=false` 时不再分配新申请，但历史审批记录仍保留。
+
+### 8.6 班级映射字段
+
+建议增加或说明：
+
+| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 |
+|---------------|---------------|----------|------|------|
+| 是否主辅导员 | is_primary | 布尔 | 否 | 多辅导员场景下标识主审批人 |
+| 生效开始日期 | effective_start_date | 日期 | 否 | 映射开始生效时间 |
+| 生效结束日期 | effective_end_date | 日期 | 否 | 映射结束时间，空表示当前有效 |
+
+首版如果只支持一班一主辅导员，也应在文档中明确限制。
+
+### 8.7 待反馈问题
+
+建议在第七章新增“数据权责方确认”：
+
+1. 每个数据源的权责系统和业务负责人是谁？
+2. 每个数据源由哪一方提供字段字典、测试数据和生产数据？
+3. 每个数据源的联系人、故障响应方式和上线前联调窗口是什么？
+
+---
+
+## 九、最终审查结论
+
+`31-data-source-requirements-consensus.md` 已经覆盖首版上线所需的主要 P0 数据源，字段设计也基本能支撑业务。它可以作为对接需求基础稿。
+
+但在提交给用户或外部系统方之前，建议至少完成以下 5 项修改：
+
+1. 将反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
+2. 将学生、辅导员、班级映射的首版推荐方式从“DB 优先”调整为“CSV/Excel 优先，API/DB 增强”。
+3. 统一宿舍清退字段必填性，特别是 `checkout_status`。
+4. 补充终审管理员/终审组配置、账号标识映射、历史审批人一致性规则。
+5. 在待反馈问题中增加数据权责、测试数据、同步策略、异常降级和多辅导员场景确认。
+
+完成上述修改后，文档可以提交。
+

codex
已完成审查并保存到：

[32-codex-data-requirements-review.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md)

结论：`31` 文档方向正确，P0 数据源基本完整，但不建议原样提交。建议先修 5 点：

1. 反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
2. 学生、辅导员、班级映射首版对接方式从“DB 优先”调整为“CSV/Excel 优先，API/DB 增强”。
3. 统一宿舍清退字段必填性，尤其是 `checkout_status`。
4. 补充终审管理员/终审组配置、账号标识映射、历史审批人一致性规则。
5. 待反馈问题增加数据权责、测试数据、同步策略、异常降级、多辅导员场景确认。

本次只新增审查文档，未改原共识文档；不涉及代码测试。
diff --git a/docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md b/docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
new file mode 100644
index 0000000000000000000000000000000000000000..404cdb7a4782fe6833890342d4c3111809b9f0a8
--- /dev/null
+++ b/docs/discussions/codex-review-2026-05-27/32-codex-data-requirements-review.md
@@ -0,0 +1,316 @@
+# 数据源需求共识文档审查结果
+
+**审查时间：** 2026-05-27  
+**审查对象：** `31-data-source-requirements-consensus.md`  
+**参考材料：** `30-codex-data-source-review.md`、`25-class-bed-field-consensus.md`、`docs/用户设计说明书.md`、`docs/design/2026-05-27-system-design.md`、`docs/数据对接说明文档.md`、`docs/templates/*.csv`
+
+---
+
+## 一、总体结论
+
+**结论：文档方向正确，P0 数据源基本完整；但不建议原样提交给用户。**
+
+建议先做一轮小范围修订后再提交，主要原因是：
+
+1. 文档标题和目的写的是“提交给宿管系统方反馈”，但 P0 数据源中的学生基本信息、辅导员信息、班级-辅导员映射通常不属于宿管系统，应改为提交给“教务/人事/学工/宿管等相关数据负责人”共同反馈。
+2. 对接方式里对学生、辅导员、班级映射默认写“DB 优先”偏激进。首版更合理的路径是：账号与映射数据优先 CSV/Excel 批量导入，宿舍清退优先 API。
+3. 宿舍清退字段与上一轮字段共识存在轻微不一致：`checkout_status` 在本文件中标为可选，但既有字段共识中 API 响应建议必填。
+4. 缺少若干实施级关键问题，例如账号标识映射、终审管理员分配规则、同步覆盖策略、历史审批人不被后续映射变更自动改写等。
+
+修订上述问题后，文档可以作为数据对接需求初稿提交。
+
+---
+
+## 二、数据源完整性审查
+
+### 2.1 P0 数据源覆盖情况
+
+当前 P0 数据源覆盖了系统运行所需的核心闭环：
+
+| 数据源 | 审查结论 | 说明 |
+|--------|----------|------|
+| 学生基本信息 | 完整 | 支撑学生账号、身份识别、班级映射、毕业届别筛选。 |
+| 宿舍清退数据 | 完整 | 支撑提交前置校验，是当前已明确需要自动校验的数据。 |
+| 辅导员基本信息 | 完整 | 支撑辅导员账号和一级审批主体。 |
+| 班级-辅导员对应关系 | 完整且必要 | 是自动分配 `counselor_id` 和权限边界的关键数据。 |
+| 学工部管理员信息 | P1 合理 | 人数少，手动创建比外部对接更合理。 |
+
+### 2.2 未遗漏的部分
+
+图书馆清书状态、财务结清状态、独立学籍状态没有列为 P0 是合理的。当前用户设计和系统设计仍保留截图上传、人工审核和宿舍系统异常时人工降级的方案，因此这三类不应阻塞首版上线。
+
+### 2.3 建议补充的“非数据源但上线必需项”
+
+以下不是外部数据源，但应在文档中补充为实施前提或配置项：
+
+1. **终审管理员分配规则。** 系统提交时需要设置 `admin_id`，应明确是固定学工部负责人、管理员组轮转、管理员池分配，还是由后台配置默认终审人。
+2. **离校批次配置。** 包括毕业届别、开放申请时间、允许计划离校日期范围。这些可由系统后台配置，不必来自外部系统。
+3. **账号标识映射。** 当前系统设计中的 `users.student_id` 被用作唯一登录标识，但共识文档给辅导员和管理员使用 `employee_id`。需要明确导入时 `employee_id` 映射到哪个内部字段，或后续模型是否新增统一的 `external_id/employee_id`。
+
+---
+
+## 三、字段定义合理性审查
+
+### 3.1 学生基本信息
+
+字段整体合理，能支撑首版业务。`student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`is_graduating` 作为必填基本可接受。
+
+建议调整：
+
+1. `is_graduating` 建议改名或补充为 `eligible_for_leave` / `graduation_status`。  
+   仅“是否毕业生”不足以表达延期毕业、结业、休学、退学、已毕业归档等异常状态。首版可以保留 `is_graduating`，但建议增加一个更直接的离校资格字段。
+
+2. `graduation_year` 示例应与当前项目日期保持一致。  
+   文档创建时间为 2026-05-27，但 SQL 示例使用 `graduation_year = 2024`。建议统一为 `2026` 或说明“示例年份按实际毕业届别替换”。
+
+3. `phone` 是否可选需要结合微信绑定策略确认。  
+   如果登录只依赖学号密码和微信 OAuth，手机号可选合理；如果要支持短信验证、密码找回或紧急联系，手机号应至少在导入模板中强烈建议提供。
+
+### 3.2 宿舍清退数据
+
+核心字段完整，但必填性需要和既有共识统一。
+
+建议调整：
+
+1. `checkout_status` 建议改为必填，且给出枚举：`completed`、`pending`、`not_started`、`unknown`。  
+   既有字段共识已将 `checkout_status` 作为 API 响应必填字段，本文件标为可选会造成实现歧义。
+
+2. `checkout_date` 应明确条件必填：当 `is_checked_out = true` 或 `checkout_status = completed` 时必填，未清退时允许为空。
+
+3. `dorm_building`、`dorm_room`、`bed_number` 可选是可接受的，但应说明这些字段仅用于展示、核对和异常排查，业务判定不得依赖床位文本匹配。
+
+4. 应补充 `source_updated_at`。  
+   对 API 或 CSV 数据都建议记录外部系统数据更新时间，便于区分“未完成清退”和“数据过期/未同步”。
+
+### 3.3 辅导员基本信息
+
+字段基本可用，但有两个风险点：
+
+1. `phone` 标为必填偏强。  
+   如果通知主要走微信，手机号可作为推荐字段而非硬性 P0。若学校确实要求短信/电话通知，则保留必填也合理。建议在文档中说明依据。
+
+2. 缺少账号生命周期字段说明。  
+   `is_active` 已有，但应补充离职、调岗、停用后如何处理其名下未完成审批，以及是否允许历史审批记录继续引用已停用账号。
+
+### 3.4 班级-辅导员对应关系
+
+该章节是文档中最关键、也最合理的部分。`class_id` 作为必填是正确的，避免只靠班级名称匹配。
+
+建议补充：
+
+1. **一班多辅导员场景。** 首版可以要求一个主辅导员，但应明确是否允许同一班级多名辅导员、代理辅导员或临时改派。
+2. **有效期字段。** `effective_term` 可选略弱，建议至少支持 `effective_start_date` / `effective_end_date` 或说明同一届首版只按当前有效映射导入。
+3. **历史一致性规则。** 班级映射变更后，不应自动改写已提交申请中的 `counselor_id`；已提交申请如需改派，应由管理员显式操作并记录审计日志。
+
+### 3.5 学工部管理员信息
+
+手动创建是合理方案。建议补充：
+
+1. 管理员账号创建、停用、重置密码、角色授权和审计要求。
+2. 默认终审人或终审组配置规则。
+3. 管理员离岗后未完成审批任务如何转交。
+
+---
+
+## 四、对接方式可行性审查
+
+### 4.1 当前优先级评价
+
+| 数据源 | 当前写法 | 审查意见 |
+|--------|----------|----------|
+| 学生基本信息 | DB 优先 / API 备选 / CSV 降级 | 建议改为 CSV/Excel 首版优先，DB/API 作为条件成熟后的增强。 |
+| 宿舍清退数据 | API 优先 / DB 备选 / CSV 降级 | 合理。提交前置校验对实时性要求更高，API 价值最大。 |
+| 辅导员基本信息 | DB 优先 / API 备选 / CSV 降级 | 建议改为 CSV/Excel 或手动批量维护优先，人数少且变化低频。 |
+| 班级-辅导员对应关系 | DB 优先 / API 备选 / CSV 降级 | 建议首版 CSV/Excel 优先并强校验，后续再考虑教务/学工 API。 |
+| 学工部管理员信息 | 手动创建 | 合理。 |
+
+### 4.2 技术要求清晰度
+
+DB、API、CSV 三种方式的技术要求整体清晰，但建议补充：
+
+1. DB 直连只建议在同一内网、安全边界清晰、能提供只读视图的情况下使用。
+2. DB 直连不要直接暴露生产业务表，建议由数据源系统提供只读视图或同步库。
+3. API 需补充分页、增量同步、错误码、限流、重试、幂等和测试环境要求。
+4. CSV 需补充导入覆盖策略：全量覆盖、增量更新、软删除/停用、重复数据处理、失败回滚。
+
+### 4.3 安全措施充分性
+
+已有只读账号、IP 白名单、专用账号、定期换密等措施，方向正确。建议增加：
+
+1. 密钥、数据库密码必须加密存储，不得写入代码仓库或明文配置。
+2. CSV 通过 SFTP 或后台上传时应限制权限，并记录上传人、文件哈希、导入批次和导入结果。
+3. 数据最小化：不采集身份证号、家庭住址、欠费明细、图书借阅明细等高敏字段。
+4. 外部系统异常时要区分“未完成”“查询失败”“数据过期”“人工证明待审”，不能统一判定为不通过。
+
+---
+
+## 五、数据量估算审查
+
+### 5.1 当前估算是否合理
+
+| 数据项 | 当前估算 | 审查结论 |
+|--------|----------|----------|
+| 学生 | 约 1000 人/届 | 合理，但需注明是“当届毕业生”。用户设计说明书中另有“学生用户 10,000 人”的容量指标，二者不冲突。 |
+| 辅导员 | 约 50 人 | 合理。 |
+| 班级映射 | 约 50 条 | 基本合理，但取决于班级粒度和是否存在多辅导员/代理关系。 |
+| 学工部管理员 | 约 5 人 | 合理。 |
+
+### 5.2 建议补充说明
+
+1. 若系统只导入当届毕业生，1000 人规模合理。
+2. 若系统保留多届历史或提前导入低年级学生，容量应按 10,000 学生账号设计。
+3. 班级映射数量不应只按班级数估算；若一个班有主辅导员、代理辅导员、历史有效期，则映射记录可能多于 50 条。
+
+---
+
+## 六、待反馈问题审查
+
+当前问题覆盖了数据库、API、CSV 和数据范围，基本可用，但建议扩展为面向多方的数据确认清单。
+
+### 6.1 建议修改提问对象
+
+将“请宿管系统方反馈以下问题”改为：
+
+> 请教务系统、人事系统、学工部数据负责人、宿管系统方分别确认其可提供的数据范围、字段、对接方式和联系人。
+
+原因：学生、辅导员、班级映射通常不是宿管系统的权责数据。
+
+### 6.2 建议新增问题
+
+1. 学生数据来源是否为教务系统？是否能只提供当届毕业生名单？
+2. 是否存在延期毕业、结业、休学、退学、提前毕业等状态？这些状态是否允许提交离校申请？
+3. `class_id` 是否全校唯一？班级名称是否可能重复、变更或跨届复用？
+4. 辅导员工号是否全校唯一？是否与统一身份认证、人事系统工号一致？
+5. 是否存在一个班级多个辅导员、代理辅导员、临时负责人或辅导员调岗场景？
+6. 班级-辅导员映射变更频率如何？是否能提供当前有效映射和历史有效期？
+7. 学工部终审人是固定个人、固定角色组、轮值还是人工分配？
+8. 各数据源能否提供测试数据、测试环境和字段字典？
+9. CSV 导入时是否采用全量覆盖还是增量更新？停用、删除、调岗如何表达？
+10. 外部系统不可用、数据延迟或查询失败时，业务上允许怎样的人工降级？
+11. 是否有统一身份认证或微信绑定前置要求？是否需要导入手机号/邮箱用于找回密码或二次验证？
+12. 数据提供方能否承诺导出频率、数据更新时间、联系人和故障响应时间？
+
+---
+
+## 七、实施建议审查
+
+### 7.1 推荐方案
+
+共识文档中的推荐方案整体合理，但“如果宿管系统数据库包含所有数据”这个前提不够现实。学生、辅导员、班级映射不应假设都在宿管系统数据库中。
+
+建议改为：
+
+1. 宿舍清退：优先使用宿管系统 API；若不可用，使用每日 CSV 导入；异常时保留人工证明。
+2. 学生基本信息：首版优先使用教务/学工提供的 CSV/Excel 导入；若已有稳定教务 API，可升级为 API。
+3. 辅导员信息：首版优先 CSV/Excel 或后台批量维护；若有统一身份或人事 API，再对接。
+4. 班级-辅导员映射：首版优先 CSV/Excel 强校验，上线前必须 100% 覆盖当届学生。
+5. 学工部管理员：手动创建，同时配置默认终审人或终审组。
+
+### 7.2 最小可行方案
+
+共识文档的最小可行方案合理，可以保留。建议补充两个验收条件：
+
+1. 当届所有可申请学生必须能解析到有效辅导员。
+2. 提交申请时必须能解析到有效终审管理员或终审组。
+
+### 7.3 更好的实施路径
+
+建议按以下顺序实施：
+
+1. 先确认数据权责方和联系人，不把所有问题都压给宿管系统。
+2. 先落地三份基础 CSV/Excel 模板：学生、辅导员、班级-辅导员映射。
+3. 实现导入校验报告，重点校验学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射。
+4. 再对接宿舍清退 API，并把 API 失败、超时、数据过期纳入统一降级处理。
+5. 上线前冻结当届数据批次，完成一次全量导入演练和异常清单清零。
+6. 上线后根据数据变更频率决定是否将学生、辅导员、映射数据升级为 API 或 DB 同步。
+
+---
+
+## 八、具体修改建议
+
+### 8.1 文档目的
+
+建议将：
+
+> 明确毕业离校系统所需的数据源，提交给宿管系统方反馈
+
+修改为：
+
+> 明确毕业离校系统所需的数据源，提交给教务、人事/统一身份、学工部、宿管系统等相关数据负责人反馈。
+
+### 8.2 数据源概述表
+
+建议将学生、辅导员、班级映射的对接方式调整为：
+
+| 数据源 | 建议对接方式 |
+|--------|--------------|
+| 学生基本信息 | CSV/Excel 首版优先 / API 或 DB 视图增强 |
+| 辅导员基本信息 | CSV/Excel 或后台批量维护首版优先 / 人事或统一身份 API 增强 |
+| 班级-辅导员对应关系 | CSV/Excel 首版优先并强校验 / 教务或学工 API 增强 |
+| 宿舍清退数据 | API 优先 / DB 只读视图备选 / CSV 降级 |
+
+### 8.3 学生字段
+
+建议在学生基本信息中增加：
+
+| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
+|---------------|---------------|----------|------|------|------|
+| 离校申请资格 | eligible_for_leave | 布尔 | 建议是 | 是否允许提交本批次离校申请 | true |
+| 学籍/毕业状态 | graduation_status | 文本 | 否 | graduating/delayed/graduated/suspended/withdrawn | graduating |
+
+如不新增字段，至少应说明 `is_graduating=true` 即表示具备本批次离校申请资格。
+
+### 8.4 宿舍清退字段
+
+建议将：
+
+| 字段 | 当前 | 建议 |
+|------|------|------|
+| checkout_status | 可选 | 必填，枚举：completed/pending/not_started/unknown |
+| checkout_date | 可选 | 条件必填：completed 时必填 |
+| source_updated_at | 未列出 | 建议新增，记录外部系统数据更新时间 |
+
+### 8.5 辅导员字段
+
+建议补充说明：
+
+1. `employee_id` 必须全校唯一，并与班级映射中的 `counselor_employee_id` 完全一致。
+2. `phone` 是否必填取决于通知和找回密码方案；如果不依赖短信，可改为建议字段。
+3. `is_active=false` 时不再分配新申请，但历史审批记录仍保留。
+
+### 8.6 班级映射字段
+
+建议增加或说明：
+
+| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 |
+|---------------|---------------|----------|------|------|
+| 是否主辅导员 | is_primary | 布尔 | 否 | 多辅导员场景下标识主审批人 |
+| 生效开始日期 | effective_start_date | 日期 | 否 | 映射开始生效时间 |
+| 生效结束日期 | effective_end_date | 日期 | 否 | 映射结束时间，空表示当前有效 |
+
+首版如果只支持一班一主辅导员，也应在文档中明确限制。
+
+### 8.7 待反馈问题
+
+建议在第七章新增“数据权责方确认”：
+
+1. 每个数据源的权责系统和业务负责人是谁？
+2. 每个数据源由哪一方提供字段字典、测试数据和生产数据？
+3. 每个数据源的联系人、故障响应方式和上线前联调窗口是什么？
+
+---
+
+## 九、最终审查结论
+
+`31-data-source-requirements-consensus.md` 已经覆盖首版上线所需的主要 P0 数据源，字段设计也基本能支撑业务。它可以作为对接需求基础稿。
+
+但在提交给用户或外部系统方之前，建议至少完成以下 5 项修改：
+
+1. 将反馈对象从“宿管系统方”改为“教务、人事/统一身份、学工、宿管等相关数据负责人”。
+2. 将学生、辅导员、班级映射的首版推荐方式从“DB 优先”调整为“CSV/Excel 优先，API/DB 增强”。
+3. 统一宿舍清退字段必填性，特别是 `checkout_status`。
+4. 补充终审管理员/终审组配置、账号标识映射、历史审批人一致性规则。
+5. 在待反馈问题中增加数据权责、测试数据、同步策略、异常降级和多辅导员场景确认。
+
+完成上述修改后，文档可以提交。
+

tokens used
61,800

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
