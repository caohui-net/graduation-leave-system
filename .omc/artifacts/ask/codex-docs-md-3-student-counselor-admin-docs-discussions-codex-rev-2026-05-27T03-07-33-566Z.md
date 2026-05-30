# codex advisor artifact

- Provider: codex
- Exit code: 0
- Created at: 2026-05-27T03:07:33.566Z

## Original task

请审查数据源完整性分析，提供建议。

**背景：**
毕业离校系统的数据对接文档（docs/数据对接说明文档.md）当前只包含学生宿舍清退数据，但系统有3个角色（student、counselor、admin），需要多个外部系统的数据。

**分析文档：**
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md

**核心问题：**

1. 学生基本信息数据源是否需要在数据对接文档中说明？
   - 来源：教务系统
   - 字段：学号、姓名、院系、专业、班级、年级

2. 辅导员数据源如何对接？
   - 基本信息：工号、姓名、手机、邮箱
   - 来源：人事系统
   - 对接方式：API vs CSV？

3. 班级-辅导员对应关系（关键）
   - 用于自动分配审批人
   - 没有此数据需手动配置~1000学生/年
   - 来源：教务系统
   - 优先级：是否应为P0？

4. 学工部管理员数据源
   - 仅~5人
   - 手动创建 vs 数据对接？

5. 可选对接
   - 图书馆清书状态（当前：手动上传截图）
   - 财务结清状态（当前：手动上传截图）
   - 学籍状态（用于毕业生识别）

**期望输出：**

1. 优先级分类：哪些是P0（必需）vs P1（可选）
2. 对接建议：每个数据源推荐API、CSV还是手动
3. 遗漏考虑：分析中未考虑的数据源
4. 实施顺序：建议的对接实施顺序

请将审查结果保存为：docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md

## Final prompt

请审查数据源完整性分析，提供建议。

**背景：**
毕业离校系统的数据对接文档（docs/数据对接说明文档.md）当前只包含学生宿舍清退数据，但系统有3个角色（student、counselor、admin），需要多个外部系统的数据。

**分析文档：**
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md

**核心问题：**

1. 学生基本信息数据源是否需要在数据对接文档中说明？
   - 来源：教务系统
   - 字段：学号、姓名、院系、专业、班级、年级

2. 辅导员数据源如何对接？
   - 基本信息：工号、姓名、手机、邮箱
   - 来源：人事系统
   - 对接方式：API vs CSV？

3. 班级-辅导员对应关系（关键）
   - 用于自动分配审批人
   - 没有此数据需手动配置~1000学生/年
   - 来源：教务系统
   - 优先级：是否应为P0？

4. 学工部管理员数据源
   - 仅~5人
   - 手动创建 vs 数据对接？

5. 可选对接
   - 图书馆清书状态（当前：手动上传截图）
   - 财务结清状态（当前：手动上传截图）
   - 学籍状态（用于毕业生识别）

**期望输出：**

1. 优先级分类：哪些是P0（必需）vs P1（可选）
2. 对接建议：每个数据源推荐API、CSV还是手动
3. 遗漏考虑：分析中未考虑的数据源
4. 实施顺序：建议的对接实施顺序

请将审查结果保存为：docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md

## Raw output

```text
已完成审查并保存到：

[30-codex-data-source-review.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md)

核心结论：

- P0：学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据、毕业资格字段。
- P1：学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
- 首版建议：学生/辅导员/映射数据用 CSV/Excel 批量导入；宿舍清退优先 API；管理员手动维护；图书馆和财务继续截图上传。
- 最高风险缺口：班级-辅导员对应关系，应作为 P0 并要求上线前 100% 覆盖当届学生。


OpenAI Codex v0.134.0
--------
workdir: /home/caohui/projects/graduation-leave-system
model: gpt-5.5
provider: fox
approval: never
sandbox: danger-full-access
reasoning effort: high
reasoning summaries: none
session id: 019e6764-b171-7b02-a97f-493fa1f9886d
--------
user
请审查数据源完整性分析，提供建议。

**背景：**
毕业离校系统的数据对接文档（docs/数据对接说明文档.md）当前只包含学生宿舍清退数据，但系统有3个角色（student、counselor、admin），需要多个外部系统的数据。

**分析文档：**
docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md

**核心问题：**

1. 学生基本信息数据源是否需要在数据对接文档中说明？
   - 来源：教务系统
   - 字段：学号、姓名、院系、专业、班级、年级

2. 辅导员数据源如何对接？
   - 基本信息：工号、姓名、手机、邮箱
   - 来源：人事系统
   - 对接方式：API vs CSV？

3. 班级-辅导员对应关系（关键）
   - 用于自动分配审批人
   - 没有此数据需手动配置~1000学生/年
   - 来源：教务系统
   - 优先级：是否应为P0？

4. 学工部管理员数据源
   - 仅~5人
   - 手动创建 vs 数据对接？

5. 可选对接
   - 图书馆清书状态（当前：手动上传截图）
   - 财务结清状态（当前：手动上传截图）
   - 学籍状态（用于毕业生识别）

**期望输出：**

1. 优先级分类：哪些是P0（必需）vs P1（可选）
2. 对接建议：每个数据源推荐API、CSV还是手动
3. 遗漏考虑：分析中未考虑的数据源
4. 实施顺序：建议的对接实施顺序

请将审查结果保存为：docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
codex
我会先读取仓库里的项目指令和两份相关文档，再把审查意见落到指定的讨论文件里。重点会放在数据源是否支撑三个角色的关键流程，而不是只做字段清单比对。
exec
/bin/bash -lc "sed -n '1,320p' docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md" in /home/caohui/projects/graduation-leave-system
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
| 宿舍清退数据 | 宿管系统 | API/CSV | ✅ 已有 |
| 辅导员基本信息 | 人事系统 | API/CSV | ❌ 缺失 |
| 班级-辅导员对应关系 | 教务系统 | API/CSV | ❌ 缺失 |

### P1（可选，影响用户体验）

| 数据源 | 来源系统 | 对接方式 | 备选方案 |
|--------|----------|----------|----------|
| 学工部管理员信息 | 人事系统 | 手动创建 | 数量少，可手动 |
| 图书馆清书状态 | 图书馆系统 | API/CSV | 手动上传截图 |
| 财务结清状态 | 财务系统 | API/CSV | 手动上传截图 |
| 学籍状态 | 教务系统 | API | 包含在学生信息中 |

---

## 七、关键发现

### 7.1 最严重的缺失

**班级-辅导员对应关系数据源**

- 🔴 **影响：** 系统无法自动分配审批人
- 🔴 **后果：** 需要手动配置每个学生的辅导员（~1000人/届）
- 🔴 **建议：** 必须在数据对接文档中补充

### 7.2 次要缺失

**学生基本信息数据源**

- 🟡 **影响：** 无法批量创建学生账号
- 🟡 **后果：** 需要学生自行注册，或手动导入
- 🟡 **建议：** 建议在数据对接文档中补充

**辅导员基本信息数据源**

- 🟡 **影响：** 无法批量创建辅导员账号
- 🟡 **后果：** 需要手动创建辅导员账号（~50人）
- 🟡 **建议：** 建议在数据对接文档中补充

---

## 八、待与Codex讨论的问题

1. **学生基本信息数据源是否需要在数据对接文档中说明？**
   - 当前文档只说明了宿舍清退数据
   - 学生基本信息是否应该包含？

2. **辅导员数据源的对接方式？**
   - API接口 vs CSV文件导入
   - 是否需要实时同步？

3. **班级-辅导员对应关系的维护方式？**
   - 从教务系统自动同步
   - 还是在本系统中手动配置？

4. **学工部管理员是否需要数据对接？**
   - 数量少（~5人），是否需要对接？
   - 还是手动创建即可？

5. **图书馆、财务系统是否需要对接？**

exec
/bin/bash -lc "sed -n '1,260p' docs/数据对接说明文档.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 毕业生离校申请审批系统 - 数据对接说明文档

**文档版本：** v1.0  
**发布日期：** 2026-05-27  
**目标用户：** 宿舍管理系统管理员、数据对接负责人

---

## 一、对接概述

### 1.1 对接目的

本系统需要与学校现有的**宿舍管理系统**进行数据对接，实现以下功能：

- 学生提交离校申请时，自动验证宿舍是否已清退
- 验证通过后，允许学生继续提交申请
- 验证失败时，提示学生先完成宿舍清退手续

### 1.2 对接方式

本系统支持两种对接方式，按优先级排序：

**方式1：API接口对接（推荐）**
- 宿舍管理系统提供REST API接口
- 本系统调用API实时查询宿舍清退状态
- 优点：实时性高、自动化程度高
- 缺点：需要宿舍管理系统支持API开发

**方式2：数据文件导入（备选）**
- 宿舍管理系统定期导出清退数据文件
- 本系统导入数据文件到本地数据库
- 优点：实施简单、无需开发API
- 缺点：数据有延迟、需要人工操作

### 1.3 对接时间表

| 阶段 | 时间 | 任务 |
|------|------|------|
| 需求确认 | 第1周 | 确认对接方式、数据字段、接口规范 |
| 接口开发 | 第2-3周 | 宿舍管理系统开发API接口（如选择方式1） |
| 联调测试 | 第4周 | 双方系统联调测试 |
| 上线部署 | 第5周 | 正式上线 |

---

## 二、方式1：API接口对接（推荐）

### 2.1 接口规范

**接口名称：** 查询学生宿舍清退状态

**请求方式：** GET 或 POST

**请求地址：** `http://宿舍管理系统域名/api/dorm/checkout/status`

**认证方式：** API Key + IP白名单

**说明：**
- API Key：在请求头中传递，用于身份验证
- IP白名单：限制只有指定IP可以访问
- 两者配合使用，确保安全性

### 2.2 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| student_id | String | 是 | 学号 | "2020010101" |
| name | String | 否 | 姓名（用于验证） | "张三" |

**请求示例（GET）：**
```
GET /api/dorm/checkout/status?student_id=2020010101&name=张三
Host: dorm.example.com
Authorization: Bearer YOUR_API_KEY
```

**请求示例（POST JSON）：**
```json
POST /api/dorm/checkout/status
Host: dorm.example.com
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "student_id": "2020010101",
  "name": "张三"
}
```

### 2.3 响应参数

**成功响应（HTTP 200）：**

| 参数名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| code | Integer | 状态码（0=成功） | 0 |
| message | String | 响应消息 | "查询成功" |
| data | Object | 数据对象 | 见下表 |

**data对象字段：**

| 参数名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| student_id | String | 学号 | "2020010101" |
| name | String | 姓名 | "张三" |
| class_name | String | 班级（可选） | "计算机2020级1班" |
| dorm_building | String | 宿舍楼栋 | "1号楼" |
| dorm_room | String | 宿舍房间号 | "101" |
| bed_number | String | 床号（可选） | "1" |
| is_checked_out | Boolean | 是否已清退 | true |
| checkout_date | String | 清退日期（ISO 8601格式） | "2026-05-20T10:30:00Z" |
| checkout_status | String | 清退状态 | "completed" / "pending" / "not_started" |
| remarks | String | 备注 | "已完成清退，物品已搬离" |

**响应示例（已清退）：**
```json
{
  "code": 0,
  "message": "查询成功",
  "data": {
    "student_id": "2020010101",
    "name": "张三",
    "class_name": "计算机2020级1班",
    "dorm_building": "1号楼",
    "dorm_room": "101",
    "bed_number": "1",
    "is_checked_out": true,
    "checkout_date": "2026-05-20T10:30:00Z",
    "checkout_status": "completed",
    "remarks": "已完成清退，物品已搬离"
  }
}
```

**响应示例（未清退）：**
```json
{
  "code": 0,
  "message": "查询成功",
  "data": {
    "student_id": "2020010101",
    "name": "张三",
    "class_name": "计算机2020级1班",
    "dorm_building": "1号楼",
    "dorm_room": "101",
    "bed_number": "1",
    "is_checked_out": false,
    "checkout_date": null,
    "checkout_status": "not_started",
    "remarks": "尚未办理清退手续"
  }
}
```

**错误响应（HTTP 200，业务错误）：**
```json
{
  "code": 1001,
  "message": "学号不存在",
  "data": null
}
```

**错误响应（HTTP 4xx/5xx）：**
```json
{
  "code": 500,
  "message": "系统内部错误",
  "data": null
}
```

### 2.4 错误码说明

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| 0 | 成功 | 正常处理 |
| 1001 | 学号不存在 | 提示学生检查学号 |
| 1002 | 参数错误 | 检查请求参数 |
| 1003 | 认证失败 | 检查API Key |
| 5000 | 系统内部错误 | 重试或联系管理员 |

### 2.5 接口性能要求

- **响应时间：** < 500ms（P95）
- **可用性：** > 99%
- **并发支持：** > 50 QPS
- **超时时间：** 5秒（本系统设置）

### 2.6 接口测试

**测试环境：**
- 测试地址：`http://dorm-test.example.com/api/dorm/checkout/status`
- 测试API Key：`test_api_key_123456`
- 测试学号：`2020010101`（已清退）、`2020010102`（未清退）

**测试工具：**
```bash
# 使用curl测试
curl -X GET "http://dorm-test.example.com/api/dorm/checkout/status?student_id=2020010101" \
  -H "Authorization: Bearer test_api_key_123456"
```

---

## 三、方式2：数据文件导入（备选）

### 3.1 文件格式

**文件类型：** Excel (.xlsx) 或 CSV (.csv)

**文件命名：** `dorm_checkout_YYYYMMDD.xlsx`（例如：`dorm_checkout_20260527.xlsx`）

**字符编码：** UTF-8（CSV文件）

**导出频率：** 每日一次（建议凌晨1点）

### 3.2 数据字段

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 学号 | student_id | 文本 | 是 | 学生学号 | 2020010101 |
| 姓名 | name | 文本 | 是 | 学生姓名 | 张三 |
| 班级 | class_name | 文本 | 否 | 学生班级 | 计算机2020级1班 |
| 宿舍楼栋 | dorm_building | 文本 | 否 | 宿舍楼栋名称 | 1号楼 |
| 宿舍房间号 | dorm_room | 文本 | 否 | 宿舍房间号 | 101 |
| 床号 | bed_number | 文本 | 否 | 床位号 | 1 |
| 是否已清退 | is_checked_out | 文本 | 是 | 是/否 | 是 |
| 清退日期 | checkout_date | 日期 | 否 | YYYY-MM-DD格式 | 2026-05-20 |
| 清退状态 | checkout_status | 文本 | 否 | 已完成/进行中/未开始 | 已完成 |
| 备注 | remarks | 文本 | 否 | 备注信息 | 已完成清退 |

### 3.3 Excel模板

**下载模板：** `docs/templates/宿舍清退数据模板.csv`

**模板示例：**

| 学号 | 姓名 | 班级 | 宿舍楼栋 | 宿舍房间号 | 床号 | 是否已清退 | 清退日期 | 清退状态 | 备注 |
|------|------|------|----------|------------|------|------------|----------|----------|------|
| 2020010101 | 张三 | 计算机2020级1班 | 1号楼 | 101 | 1 | 是 | 2026-05-20 | 已完成 | 已完成清退，物品已搬离 |
| 2020010102 | 李四 | 计算机2020级1班 | 1号楼 | 102 | 2 | 否 |  | 未开始 | 尚未办理清退手续 |
| 2020010103 | 王五 | 计算机2020级2班 | 2号楼 | 201 | 1 | 是 | 2026-05-21 | 已完成 | 已完成清退 |

### 3.4 CSV格式示例

```csv
学号,姓名,班级,宿舍楼栋,宿舍房间号,床号,是否已清退,清退日期,清退状态,备注
2020010101,张三,计算机2020级1班,1号楼,101,1,是,2026-05-20,已完成,已完成清退，物品已搬离
2020010102,李四,计算机2020级1班,1号楼,102,2,否,,未开始,尚未办理清退手续
2020010103,王五,计算机2020级2班,2号楼,201,1,是,2026-05-21,已完成,已完成清退
```

### 3.5 数据要求

**数据完整性：**
- 必填字段不能为空
- 学号必须唯一
- 日期格式必须正确


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
/bin/bash -lc "pwd && rg --files -g 'AGENTS.md' -g 'docs/**'" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
/home/caohui/projects/graduation-leave-system
docs/templates/宿舍清退数据模板.csv
docs/superpowers/plans/2026-05-27-implementation-plan.md
docs/数据对接说明文档.md
docs/用户设计说明书.md
docs/PROJECT-SUMMARY.md
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
docs/discussions/codex-review-2026-05-27/15-claude-analysis-part2-api-auth.md
docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md
docs/discussions/codex-review-2026-05-27/04-database-review.md
docs/discussions/codex-review-2026-05-27/16-claude-analysis-part3-workflow-integration.md
docs/discussions/codex-review-2026-05-27/25-class-bed-field-consensus.md
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
docs/design/2026-05-27-system-design.md

codex
我已经确认现有对接文档确实只覆盖宿舍清退，分析文档把学生、辅导员、班级映射等缺口列出来了。接下来我会交叉看系统设计和用户说明，确认这些数据源在实际流程里的必要性，避免把“便利项”误判成“上线阻断项”。
exec
/bin/bash -lc "rtk sed -n '261,520p' docs/数据对接说明文档.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
**数据准确性：**
- 学号必须与学生信息系统一致
- 姓名必须与学生信息系统一致
- 清退状态必须真实准确

**数据时效性：**
- 建议每日更新一次
- 数据延迟不超过24小时

### 3.6 文件传输方式

**方式A：FTP/SFTP上传**
- 宿舍管理系统自动上传到指定FTP服务器
- 本系统定时下载并导入

**方式B：共享文件夹**
- 宿舍管理系统导出到共享文件夹
- 本系统定时读取并导入

**方式C：手动上传**
- 管理员手动下载文件
- 在本系统管理后台上传导入

---

## 四、数据安全要求

### 4.1 传输安全

- **生产环境建议使用HTTPS协议**（有公网域名和SSL证书时）
- **内网部署可使用HTTP协议**（配合IP白名单和API Key）
- 文件传输必须使用SFTP或加密传输
- API Key必须妥善保管，不得泄露

### 4.2 访问控制

- API接口限制IP白名单访问
- 文件传输账号独立，权限最小化
- 定期更换API Key和传输密码

### 4.3 数据脱敏

- 导出数据不包含敏感信息（身份证号、手机号等）
- 仅包含必要的业务数据

### 4.4 审计日志

- 记录所有API调用日志
- 记录所有文件导入日志
- 日志保留至少90天

---

## 五、联调测试

### 5.1 测试环境准备

**宿舍管理系统方：**
- 提供测试环境API地址或测试数据文件
- 提供测试账号和API Key
- 准备测试数据（至少10条，包含已清退和未清退）

**本系统方：**
- 提供测试环境地址
- 配置宿舍管理系统API地址
- 准备测试学号

### 5.2 测试用例

| 测试场景 | 测试数据 | 预期结果 |
|----------|----------|----------|
| 查询已清退学生 | 学号：2020010101 | 返回is_checked_out=true |
| 查询未清退学生 | 学号：2020010102 | 返回is_checked_out=false |
| 查询不存在学号 | 学号：9999999999 | 返回错误码1001 |
| 参数缺失 | 不传student_id | 返回错误码1002 |
| API Key错误 | 错误的API Key | 返回错误码1003 |
| 超时测试 | 延迟6秒响应 | 本系统超时重试 |

### 5.3 测试验收标准

- ✓ 所有测试用例通过
- ✓ API响应时间 < 500ms
- ✓ 数据准确率 100%
- ✓ 异常处理正确

---

## 六、上线部署

### 6.1 生产环境配置

**API接口方式：**
- 生产环境API地址：`https://dorm.example.com/api/dorm/checkout/status`
- 生产环境API Key：由宿舍管理系统提供
- IP白名单：本系统服务器IP

**文件导入方式：**
- FTP/SFTP地址：由宿舍管理系统提供
- 传输账号密码：由宿舍管理系统提供
- 文件存放路径：`/data/dorm_checkout/`

### 6.2 监控告警

**监控指标：**
- API调用成功率
- API响应时间
- 文件导入成功率
- 数据更新时效性

**告警规则：**
- API调用失败率 > 5%，发送告警
- API响应时间 > 1秒，发送告警
- 文件导入失败，发送告警
- 数据超过48小时未更新，发送告警

### 6.3 应急预案

**API不可用：**
- 自动切换到降级模式（手动上传证明）
- 通知管理员和宿舍管理系统负责人
- 记录降级日志

**数据异常：**
- 暂停自动验证
- 人工审核宿舍清退证明
- 排查数据问题

---

## 七、联系方式

### 7.1 技术对接联系人

**本系统方：**
- 姓名：XXX
- 电话：XXX-XXXX-XXXX
- 邮箱：tech@example.com

**宿舍管理系统方：**
- 姓名：（待填写）
- 电话：（待填写）
- 邮箱：（待填写）

### 7.2 技术支持

**工作时间：** 周一至周五 9:00-18:00  
**紧急联系：** 7×24小时（生产环境故障）

---

## 八、附录

### 附录A：Excel模板文件

模板文件路径：`docs/templates/宿舍清退数据模板.csv`

### 附录B：数据字典

完整数据字典：参考本文档第三章第3.2节

---

**文档结束**

exec
/bin/bash -lc "rtk sed -n '321,520p' docs/discussions/codex-review-2026-05-27/29-data-source-analysis.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
   - 当前方案是手动上传截图
   - 是否需要改为API对接？

6. **学籍状态是否需要单独对接？**
   - 用于识别毕业生
   - 还是包含在学生基本信息中？

---

**文档结束**

exec
/bin/bash -lc "rtk sed -n '1,260p' docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
# 数据源完整性审查与建议

**审查时间：** 2026-05-27  
**审查对象：** `29-data-source-analysis.md`、`docs/数据对接说明文档.md`、用户设计与系统设计相关要求  

---

## 1. Priority Classification

### P0：上线必须具备的数据

| 数据源 | 优先级 | 判定 | 理由 |
|--------|--------|------|------|
| 学生基本信息 | P0 | 必须纳入数据对接文档 | `29-data-source-analysis.md` 第三章 3.1 已列为 P0，用途包括创建学生账号、身份验证、按班级分配审批人。用户设计说明书也明确“学号由学校统一导入”，因此它不是单纯便利项。技术上可用手工 Excel 导入替代 API，但数据源和字段规范必须写进对接文档。 |
| 班级-辅导员对应关系 | P0 | 必须纳入数据对接文档 | `29-data-source-analysis.md` 第三章 3.4 和第七章 7.1 都指出缺失后系统无法自动分配审批人，需要手动配置约 1000 人/届。系统设计中的 `applications.counselor_id`、`current_approver_id` 也依赖该关系在提交时固化审批人。 |
| 辅导员基本信息 | P0 | 必须具备，但实时 API 不是必须 | `29-data-source-analysis.md` 第三章 3.3 将其列为 P0，原因是创建辅导员账号和分配审批权限。约 50 人规模下，CSV/Excel 导入已经可满足上线；API 是运维优化，不是首版硬要求。 |
| 宿舍清退数据 | P0 | 已覆盖，继续保持 P0 | 当前数据对接文档已覆盖宿舍系统。用户设计说明书将宿舍清退作为提交前自动验证项，同时保留手动上传证明作为降级方案。 |
| 学籍/毕业资格 | P0 字段，P1 独立接口 | 应并入学生基本信息首批导入 | `29-data-source-analysis.md` 第四章 4.3 将学籍状态列为 P1，但其用途包含“限制只有毕业生可以提交离校申请”。如果学生基本信息只导入当届毕业生，则不需要独立实时接口；如果导入全校学生，则 `graduation_status` / `graduation_year` / `eligible_for_leave` 必须作为 P0 字段。独立学籍 API 可放到 P1。 |

### P1：提升自动化或审核运营效率的数据

| 数据源 | 优先级 | 判定 | 理由 |
|--------|--------|------|------|
| 学工部管理员信息 | P1 | 不建议做系统级数据对接 | `29-data-source-analysis.md` 第三章 3.5 和第六章均说明管理员约 5 人，可手动创建。这里是账号初始化问题，不是高频数据同步问题。 |
| 图书馆清书状态 | P1 | 可选集成 | `29-data-source-analysis.md` 第四章 4.1 说明当前方案是上传清书证明截图。附件表也已有 `library_clearance` 类型，因此首版可运行；API 集成主要减少截图审核和伪造风险。 |
| 财务结清状态 | P1 | 可选集成，优先级略高于图书馆 | `29-data-source-analysis.md` 第四章 4.2 说明当前方案是上传财务结清截图。考虑费用状态的业务敏感性，若财务系统已有稳定接口，可比图书馆更早做，但不应阻塞首版。 |

---

## 2. Integration Recommendations

| 数据源 | 推荐方式 | 备选方式 | 建议字段/补充要求 |
|--------|----------|----------|------------------|
| 学生基本信息 | CSV/Excel 批量导入作为首版标准方案 | 教务系统 API | 首版按届导入约 1000 人，批量文件更容易落地。字段除分析文档列出的 `student_id`、`name`、`department`、`major`、`class_name`、`grade` 外，建议增加 `class_id`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
| 班级-辅导员对应关系 | CSV/Excel 批量导入，必须有校验报告 | 教务系统 API | 这是 P0 数据，但不要求实时。建议以 `class_id + counselor_employee_id + effective_term` 为主键逻辑，避免只靠班级名称匹配。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无负责人的学生数。 |
| 辅导员基本信息 | CSV/Excel 批量导入 | HR API | 约 50 人，首版 API 收益有限。字段包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API 同步。 |
| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入 | 当前文档策略合理。申请提交时需要实时性，API 价值高；若宿管系统无法提供 API，则保留手动上传证明和文件导入。 |
| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 约 5 人，不建议接 HR API。需要在文档中明确由系统管理员维护，并保留角色授权、停用、重置密码流程。 |
| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 不作为首版阻塞项。若后续对接，建议只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，避免引入借阅明细等非必要个人数据。 |
| 财务结清状态 | 首版手动上传截图 | API 优先于 CSV | 不作为首版阻塞项。若对接，应只返回结清布尔值和日期，不同步欠费明细；失败时保留人工审核通道。 |
| 学籍/毕业资格 | 并入学生基本信息导入 | 教务系统 API | 不建议首版单独建接口。只有在系统长期服务多届、多状态学生，或需要实时处理延期毕业/结业/退学时，再做独立 API。 |

---

## 3. Missing Considerations

1. **班级唯一标识不足。** 当前分析使用 `class_name`，但同名、改名、跨届复用都可能发生。对接文档应优先要求 `class_id`，`class_name` 仅用于展示。

2. **账号生命周期未定义。** 需要明确新增、更新、停用、毕业后归档、辅导员离职/调岗后的处理规则。否则 CSV 导入只能新增，无法可靠处理人员变化。

3. **导入校验与人工修复流程缺失。** P0 数据不只需要字段格式，还需要“导入前校验、导入失败明细、重复数据处理、回滚/覆盖策略、导入审计日志”。

4. **审批人变更后的历史一致性。** 系统设计中申请会固化 `counselor_id`。应明确：已提交申请不随映射变更自动改审批人，除非管理员执行带审计的改派操作。

5. **多辅导员/代理审批场景。** 一个班级可能存在主辅导员、临时代办、请假代理。建议首版至少支持一个主负责人，并在后台预留手动改派能力。

6. **组织架构与权限边界。** 学工部可看全校，辅导员只能看负责班级。除班级映射外，还需要院系、专业、年级等维度用于筛选、统计和异常排查。

7. **数据最小化与敏感信息边界。** 不应为验证身份引入身份证号、欠费明细、借阅明细等高敏字段。此前共识中 `student_id + name` 已足够识别学生，应继续沿用最小字段集。

8. **降级策略需要统一。** 宿舍、图书馆、财务都可能不可用。文档应区分“自动验证失败”“外部系统不可用”“学生确未完成清退/结清”，并定义人工审核入口。

9. **毕业离校批次配置。** 计划离校日期范围、当前开放届别、申请开放/关闭时间不一定来自学生信息本身，可能需要系统配置或教务校历数据。

10. **通知数据来源。** `phone`、`email` 对审批提醒和异常联系有价值；微信 `openid` 应通过用户绑定产生，不应从外部系统导入。

---

## 4. Implementation Sequence

1. **先扩展数据对接文档范围。** 将文档标题和目标用户从“宿舍管理系统对接”扩展为“毕业离校系统数据对接”，拆分为账号基础数据、审批关系数据、业务校验数据三类。

2. **实现学生基本信息导入。** 首版采用 CSV/Excel，支持新增和更新，要求导入当届毕业生或带 `eligible_for_leave` 字段。没有这一步，统一账号、身份验证和申请资格都不稳定。

3. **实现辅导员基本信息导入。** 先用 CSV/Excel 创建约 50 个辅导员账号，确保 `employee_id` 可被后续映射引用。

4. **实现班级-辅导员映射导入和覆盖率校验。** 这是审批自动分配的关键路径。上线前必须达到 100% 当届学生可解析到辅导员；异常学生应进入导入报告而不是运行时才暴露。

5. **保留并完善宿舍清退对接。** 当前文档已较完整，下一步重点是把它接入统一的外部校验/降级策略，而不是继续孤立成唯一数据源。

6. **手动创建学工部管理员账号。** 同时补充后台维护流程，包括新增、停用、密码重置、角色授权审计。

7. **将学籍/毕业资格并入学生导入字段。** 先不要单独建设学籍 API；待多届并行、延期毕业等需求明确后，再升级为教务系统实时同步。

8. **按投入产出评估图书馆和财务接口。** 首版继续截图上传；若实际审核量大、截图造假风险高或外部系统已有成熟 API，则优先财务、再图书馆。

9. **最后补齐运营治理能力。** 包括导入审计、差异报表、外部接口监控、数据更新时间展示、人工改派和人工审核日志。这些不是单个数据源，但决定数据对接上线后的可维护性。

---

## 结论

学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据都应进入数据对接文档，其中班级-辅导员映射是最高风险缺口。首版不应追求所有系统 API 化；对约 1000 名学生和约 50 名辅导员，CSV/Excel 导入加严格校验更现实。管理员账号、图书馆、财务、独立学籍接口属于 P1 或后续增强，不应阻塞核心审批闭环上线。

exec
/bin/bash -lc 'rtk rg -n "student|counselor|admin|辅导员|学工|班级|教务|人事|图书|财务|宿舍|清退|审批人" docs/design docs/用户设计说明书.md docs/PROJECT-SUMMARY.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
docs/PROJECT-SUMMARY.md:13:实现一个完整的毕业生离校申请审批系统，支持学生在线提交离校申请，辅导员和学工部两级审批，附件管理，微信通知推送，以及宿舍管理系统对接。
docs/PROJECT-SUMMARY.md:35:- ✓ 确认系统集成需求（宿舍管理系统）
docs/PROJECT-SUMMARY.md:86:- ✓ 宿舍对接添加class_name和bed_number字段
docs/PROJECT-SUMMARY.md:98:- ✓ P2修复：删除Postman引用、明确认证方式、统一审批时限、修改辅导员权限范围、统一性能指标
docs/PROJECT-SUMMARY.md:132:   - 受众：学校管理人员、辅导员、学工部
docs/PROJECT-SUMMARY.md:136:   - 内容：宿舍管理系统对接规范，包含API接口和数据文件两种方式
docs/PROJECT-SUMMARY.md:137:   - 受众：宿舍管理系统管理员、数据对接负责人
docs/PROJECT-SUMMARY.md:138:   - 附件：`docs/templates/宿舍清退数据模板.csv`
docs/PROJECT-SUMMARY.md:143:- 学生、辅导员、学工部三种角色
docs/PROJECT-SUMMARY.md:150:- 上传附件（宿舍清退证明、图书馆清书证明、财务结清截图）
docs/PROJECT-SUMMARY.md:155:- 两级审批（辅导员→学工部）
docs/PROJECT-SUMMARY.md:173:- 宿舍管理系统对接
docs/PROJECT-SUMMARY.md:236:- 宿舍系统对接
docs/用户设计说明书.md:5:**目标用户：** 学校管理人员、辅导员、学工部
docs/用户设计说明书.md:18:- **辅导员端：** 审批本年级学生的离校申请、查看审批历史、接收待办提醒
docs/用户设计说明书.md:19:- **学工部端：** 审批所有学生的离校申请、查看全校审批统计、导出审批数据
docs/用户设计说明书.md:39:- 学号、姓名、专业、班级
docs/用户设计说明书.md:44:- 宿舍清退证明（照片或PDF）
docs/用户设计说明书.md:45:- 图书馆清书证明（照片或PDF）
docs/用户设计说明书.md:46:- 财务结清截图（照片或PDF）
docs/用户设计说明书.md:51:学生提交 → 辅导员审批 → 学工部审批 → 审批完成
docs/用户设计说明书.md:57:- 辅导员审批：提交后1个工作日内
docs/用户设计说明书.md:58:- 学工部审批：辅导员通过后1个工作日内
docs/用户设计说明书.md:68:- 学生提交申请 → 通知辅导员
docs/用户设计说明书.md:69:- 辅导员审批通过 → 通知学生和学工部
docs/用户设计说明书.md:70:- 辅导员驳回 → 通知学生
docs/用户设计说明书.md:71:- 学工部审批通过 → 通知学生（审批完成）
docs/用户设计说明书.md:72:- 学工部驳回 → 通知学生
docs/用户设计说明书.md:73:- 审批超时 → 通知审批人
docs/用户设计说明书.md:94:**宿舍管理系统对接：**
docs/用户设计说明书.md:95:- 学生提交申请时，系统自动验证宿舍是否已清退
docs/用户设计说明书.md:96:- 验证失败时，提示学生先完成宿舍清退
docs/用户设计说明书.md:116:- 辅导员只能查看负责班级的学生
docs/用户设计说明书.md:117:- 学工部可以查看所有学生
docs/用户设计说明书.md:128:| **辅导员** | 本年级学生 | 审批申请、查看历史、接收通知 |
docs/用户设计说明书.md:129:| **学工部** | 全校学生 | 审批申请、查看统计、导出数据 |
docs/用户设计说明书.md:143:**辅导员权限：**
docs/用户设计说明书.md:144:- ✓ 查看负责班级学生的申请列表
docs/用户设计说明书.md:145:- ✓ 审批负责班级学生的申请（通过/驳回）
docs/用户设计说明书.md:149:- ✗ 审批其他班级学生
docs/用户设计说明书.md:151:**学工部权限：**
docs/用户设计说明书.md:207:A：联系辅导员或系统管理员重置密码。
docs/用户设计说明书.md:221:### 6.2 审批人常见问题
docs/用户设计说明书.md:233:A：学工部用户在"审批统计"页面点击"导出Excel"按钮。
docs/用户设计说明书.md:238:A：准备Excel模板（学号、姓名、专业、班级、辅导员），在管理后台上传。
docs/用户设计说明书.md:246:**Q4：如何对接宿舍管理系统？**
docs/design/2026-05-27-system-design.md:32:   - 上传规定附件（宿舍清退证明、图书馆清书证明、财务结清截图）
docs/design/2026-05-27-system-design.md:35:2. **一级审批：** 毕业年级辅导员审核
docs/design/2026-05-27-system-design.md:40:3. **终端备案：** 学工部管理科负责人终审
docs/design/2026-05-27-system-design.md:102:│ 宿舍管理系统  │  微信公众平台 │ 文件存储   │
docs/design/2026-05-27-system-design.md:168:│       ├── dorm_system.py # 宿舍系统对接
docs/design/2026-05-27-system-design.md:187:   - 学生/辅导员/学工部用户管理
docs/design/2026-05-27-system-design.md:201:   - 辅导员审批操作
docs/design/2026-05-27-system-design.md:202:   - 学工部备案操作
docs/design/2026-05-27-system-design.md:208:   - 附件上传（宿舍清退证明、图书馆清书证明、财务结清截图）
docs/design/2026-05-27-system-design.md:224:   - 宿舍管理系统API对接
docs/design/2026-05-27-system-design.md:225:   - 宿舍清退状态查询
docs/design/2026-05-27-system-design.md:262:    student_id VARCHAR(20) UNIQUE NOT NULL COMMENT '学号',
docs/design/2026-05-27-system-design.md:278:    role VARCHAR(20) NOT NULL COMMENT '角色: student/counselor/admin',
docs/design/2026-05-27-system-design.md:281:    class_name VARCHAR(50) COMMENT '班级',
docs/design/2026-05-27-system-design.md:288:    INDEX idx_student_id (student_id),
docs/design/2026-05-27-system-design.md:300:- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
docs/design/2026-05-27-system-design.md:310:    student_id BIGINT NOT NULL COMMENT '学生ID',
docs/design/2026-05-27-system-design.md:312:    -- 固定审批人追踪
docs/design/2026-05-27-system-design.md:313:    counselor_id BIGINT COMMENT '辅导员ID',
docs/design/2026-05-27-system-design.md:314:    admin_id BIGINT COMMENT '学工部管理员ID',
docs/design/2026-05-27-system-design.md:318:    current_approver_id BIGINT COMMENT '当前审批人ID',
docs/design/2026-05-27-system-design.md:335:    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:336:    FOREIGN KEY (counselor_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:337:    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE PROTECT,
docs/design/2026-05-27-system-design.md:340:    INDEX idx_student_id (student_id),
docs/design/2026-05-27-system-design.md:341:    INDEX idx_counselor_id (counselor_id),
docs/design/2026-05-27-system-design.md:342:    INDEX idx_admin_id (admin_id),
docs/design/2026-05-27-system-design.md:347:    INDEX idx_student_status (student_id, status, created_at),
docs/design/2026-05-27-system-design.md:354:- `pending_counselor` - 待辅导员审核
docs/design/2026-05-27-system-design.md:355:- `pending_admin` - 待学工部备案
docs/design/2026-05-27-system-design.md:368:    approver_id BIGINT NOT NULL COMMENT '审批人ID',
docs/design/2026-05-27-system-design.md:369:    approver_role VARCHAR(20) NOT NULL COMMENT '审批人角色',
docs/design/2026-05-27-system-design.md:387:- `approver_role`: counselor（辅导员）、admin（学工部）
docs/design/2026-05-27-system-design.md:389:- `time_limit`: 辅导员1个工作日(24小时)，学工部1个工作日(24小时)
docs/design/2026-05-27-system-design.md:416:- `dorm_clearance` - 宿舍清退证明
docs/design/2026-05-27-system-design.md:417:- `library_clearance` - 图书馆清书证明
docs/design/2026-05-27-system-design.md:418:- `finance_settlement` - 财务结清截图
docs/design/2026-05-27-system-design.md:496:- `dorm_integration_type` - 宿舍系统集成类型（api/database）
docs/design/2026-05-27-system-design.md:497:- `dorm_api_url` - 宿舍系统API地址
docs/design/2026-05-27-system-design.md:498:- `dorm_api_key` - 宿舍系统API密钥（加密存储）
docs/design/2026-05-27-system-design.md:499:- `dorm_db_config` - 宿舍系统数据库配置（加密存储，JSON格式）
docs/design/2026-05-27-system-design.md:593:  ├─1:N─→ approvals (审批人审批多个申请)
docs/design/2026-05-27-system-design.md:598:  ├─N:1─→ users (辅导员)
docs/design/2026-05-27-system-design.md:599:  ├─N:1─→ users (学工部管理员)
docs/design/2026-05-27-system-design.md:600:  ├─N:1─→ users (当前审批人)
docs/design/2026-05-27-system-design.md:609:  └─N:1─→ users (审批人)
docs/design/2026-05-27-system-design.md:627:2. 一个申请必须经过2级审批（辅导员→学工部）
docs/design/2026-05-27-system-design.md:683:  "student_id": "2020001",
docs/design/2026-05-27-system-design.md:697:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:699:      "role": "student"
docs/design/2026-05-27-system-design.md:724:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:762:  "student_id": "2020001",
docs/design/2026-05-27-system-design.md:775:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:797:  "student_id": "2020001",
docs/design/2026-05-27-system-design.md:811:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:875:GET /api/v1/applications?status=pending_counselor&page=1&page_size=20
docs/design/2026-05-27-system-design.md:890:        "student_name": "张三",
docs/design/2026-05-27-system-design.md:891:        "status": "pending_counselor",
docs/design/2026-05-27-system-design.md:911:    "student": {
docs/design/2026-05-27-system-design.md:913:      "student_id": "2020001",
docs/design/2026-05-27-system-design.md:917:    "status": "pending_counselor",
docs/design/2026-05-27-system-design.md:923:        "file_name": "宿舍清退证明.jpg",
docs/design/2026-05-27-system-design.md:930:        "approver_role": "counselor",
docs/design/2026-05-27-system-design.md:967:    "status": "pending_counselor",
docs/design/2026-05-27-system-design.md:989:        "student_name": "张三",
docs/design/2026-05-27-system-design.md:1015:    "status": "pending_admin",
docs/design/2026-05-27-system-design.md:1016:    "next_approver": "学工部",
docs/design/2026-05-27-system-design.md:1038:  "opinion": "宿舍清退证明不完整，请重新提交",
docs/design/2026-05-27-system-design.md:1080:    "file_name": "宿舍清退证明.jpg",
docs/design/2026-05-27-system-design.md:1154:        "content": "您的离校申请已通过辅导员审核",
docs/design/2026-05-27-system-design.md:1180:Authorization: Bearer {admin_token}
docs/design/2026-05-27-system-design.md:1189:      "description": "宿舍系统集成类型（api/database）"
docs/design/2026-05-27-system-design.md:1194:      "description": "宿舍系统API地址"
docs/design/2026-05-27-system-design.md:1199:      "description": "宿舍系统API密钥（加密存储）",
docs/design/2026-05-27-system-design.md:1209:Authorization: Bearer {admin_token}
docs/design/2026-05-27-system-design.md:1228:- `integration` - 外部系统集成配置（宿舍系统等）
docs/design/2026-05-27-system-design.md:1288:    "student_id": "2020001",
docs/design/2026-05-27-system-design.md:1289:    "role": "student",
docs/design/2026-05-27-system-design.md:1312:student（学生）
docs/design/2026-05-27-system-design.md:1319:counselor（辅导员）
docs/design/2026-05-27-system-design.md:1325:admin（学工部管理员）
docs/design/2026-05-27-system-design.md:1335:资源/操作          | student | counselor | admin
docs/design/2026-05-27-system-design.md:1341:辅导员审批         | ✗       | ✓         | ✗
docs/design/2026-05-27-system-design.md:1342:学工部审批         | ✗       | ✗         | ✓
docs/design/2026-05-27-system-design.md:1364:@role_required('counselor', 'admin')
docs/design/2026-05-27-system-design.md:1375:        return request.user.role == 'student'
docs/design/2026-05-27-system-design.md:1379:        return request.user.role == 'counselor'
docs/design/2026-05-27-system-design.md:1383:        return obj.student_id == request.user.id
docs/design/2026-05-27-system-design.md:1396:pending_counselor（待辅导员审核）
docs/design/2026-05-27-system-design.md:1398:pending_admin        rejected（已驳回）
docs/design/2026-05-27-system-design.md:1399:（待学工部备案）
docs/design/2026-05-27-system-design.md:1407:    'draft': ['pending_counselor'],  # 提交
docs/design/2026-05-27-system-design.md:1408:    'pending_counselor': ['pending_admin', 'rejected'],  # 辅导员审批
docs/design/2026-05-27-system-design.md:1409:    'pending_admin': ['approved', 'rejected'],  # 学工部审批
docs/design/2026-05-27-system-design.md:1410:    'rejected': ['pending_counselor'],  # 重新提交
docs/design/2026-05-27-system-design.md:1421:  - 必须上传宿舍清退证明
docs/design/2026-05-27-system-design.md:1422:  - 必须上传图书馆清书证明
docs/design/2026-05-27-system-design.md:1423:  - 必须上传财务结清截图
docs/design/2026-05-27-system-design.md:1425:  - 状态变更：draft → pending_counselor
docs/design/2026-05-27-system-design.md:1427:  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
docs/design/2026-05-27-system-design.md:1428:  - 设置当前审批人：current_approver_id = counselor_id
docs/design/2026-05-27-system-design.md:1433:  - 发送通知给辅导员
docs/design/2026-05-27-system-design.md:1436:**节点2：辅导员审核**
docs/design/2026-05-27-system-design.md:1437:- 触发条件：申请状态为 pending_counselor
docs/design/2026-05-27-system-design.md:1438:- 权限要求：辅导员角色 + current_approver_id匹配
docs/design/2026-05-27-system-design.md:1442:    - 状态变更 → pending_admin
docs/design/2026-05-27-system-design.md:1443:    - 更新当前审批人：current_approver_id = admin_id
docs/design/2026-05-27-system-design.md:1445:    - 创建审批记录：approvals（approver_role='counselor', action='approve'）
docs/design/2026-05-27-system-design.md:1446:    - 创建历史快照：applications_history（version=N, change_reason='辅导员审批通过'）
docs/design/2026-05-27-system-design.md:1448:    - 通知学工部
docs/design/2026-05-27-system-design.md:1451:    - 清空当前审批人：current_approver_id = NULL
docs/design/2026-05-27-system-design.md:1453:    - 创建审批记录：approvals（approver_role='counselor', action='reject'）
docs/design/2026-05-27-system-design.md:1454:    - 创建历史快照：applications_history（version=N, change_reason='辅导员驳回'）
docs/design/2026-05-27-system-design.md:1461:**节点3：学工部备案**
docs/design/2026-05-27-system-design.md:1462:- 触发条件：申请状态为 pending_admin
docs/design/2026-05-27-system-design.md:1463:- 权限要求：学工部管理员角色 + current_approver_id匹配
docs/design/2026-05-27-system-design.md:1468:    - 清空当前审批人：current_approver_id = NULL
docs/design/2026-05-27-system-design.md:1472:    - 创建审批记录：approvals（approver_role='admin', action='approve'）
docs/design/2026-05-27-system-design.md:1473:    - 创建历史快照：applications_history（version=N, change_reason='学工部备案通过'）
docs/design/2026-05-27-system-design.md:1479:    - 清空当前审批人：current_approver_id = NULL
docs/design/2026-05-27-system-design.md:1481:    - 创建审批记录：approvals（approver_role='admin', action='reject'）
docs/design/2026-05-27-system-design.md:1482:    - 创建历史快照：applications_history（version=N, change_reason='学工部驳回'）
docs/design/2026-05-27-system-design.md:1494:  - 重新提交 → pending_counselor
docs/design/2026-05-27-system-design.md:1509:        status__in=['pending_counselor', 'pending_admin'],
docs/design/2026-05-27-system-design.md:1583:- 第1次：办理时限到期时通知审批人
docs/design/2026-05-27-system-design.md:1584:- 第2次：超时4小时后通知审批人上级
docs/design/2026-05-27-system-design.md:1588:- 外部系统（宿舍管理系统）不可用时，允许手动上传证明文件
docs/design/2026-05-27-system-design.md:1589:- 审批人可选择"跳过验证"并备注原因
docs/design/2026-05-27-system-design.md:1605:### 6.2 宿舍管理系统对接
docs/design/2026-05-27-system-design.md:1608:验证学生宿舍清退状态，确保离校手续真实完成。
docs/design/2026-05-27-system-design.md:1622:# 查询宿舍清退状态
docs/design/2026-05-27-system-design.md:1627:  student_id: 2020001
docs/design/2026-05-27-system-design.md:1633:    "student_id": "2020001",
docs/design/2026-05-27-system-design.md:1657:    def get_checkout_status(self, student_id):
docs/design/2026-05-27-system-design.md:1659:            f'{self.base_url}/api/students/{student_id}/checkout',
docs/design/2026-05-27-system-design.md:1679:    def verify_clearance(self, student_id):
docs/design/2026-05-27-system-design.md:1683:                params={"student_id": student_id},
docs/design/2026-05-27-system-design.md:1692:            raise ExternalSystemTimeout("宿舍系统超时")
docs/design/2026-05-27-system-design.md:1694:            raise ExternalSystemError(f"宿舍系统错误: {str(e)}")
docs/design/2026-05-27-system-design.md:1727:def verify_dorm_clearance(student_id):
docs/design/2026-05-27-system-design.md:1729:    return plugin.verify_clearance(student_id)
docs/design/2026-05-27-system-design.md:1734:- 审批人可选择"跳过验证"并备注原因
docs/design/2026-05-27-system-design.md:1982:def bind_wechat_to_account(student_id, wechat_openid, password):
docs/design/2026-05-27-system-design.md:1984:    user = User.objects.filter(student_id=student_id).first()
docs/design/2026-05-27-system-design.md:1990:            request_data={'student_id': student_id}
docs/design/2026-05-27-system-design.md:2320:- `dorm_api_key` - 宿舍系统API密钥
docs/design/2026-05-27-system-design.md:2321:- `dorm_db_config` - 宿舍系统数据库配置（JSON格式）
docs/design/2026-05-27-system-design.md:2325:- 只有admin角色可查看/编辑加密配置
docs/design/2026-05-27-system-design.md:2338:CREATE INDEX idx_student_id ON users(student_id);
docs/design/2026-05-27-system-design.md:2344:CREATE INDEX idx_student_id ON applications(student_id);
docs/design/2026-05-27-system-design.md:2345:CREATE INDEX idx_counselor_id ON applications(counselor_id);
docs/design/2026-05-27-system-design.md:2346:CREATE INDEX idx_admin_id ON applications(admin_id);
docs/design/2026-05-27-system-design.md:2353:CREATE INDEX idx_student_status ON applications(student_id, status, created_at);
docs/design/2026-05-27-system-design.md:2386:- `idx_approver_status`: 待审批列表查询（按审批人+状态+时间）
docs/design/2026-05-27-system-design.md:2387:- `idx_student_status`: 学生查看自己申请列表
docs/design/2026-05-27-system-design.md:2458:    # 失效审批人的待审批数量缓存
docs/design/2026-05-27-system-design.md:2464:    cache.delete(f'student:{app.student_id}:applications')
docs/design/2026-05-27-system-design.md:2576:    self.status = 'pending_counselor'
docs/design/2026-05-27-system-design.md:2589:    assert app.status == 'pending_counselor'
docs/design/2026-05-27-system-design.md:2593:    result = approve_application(app_id, counselor_id, 'approve')
docs/design/2026-05-27-system-design.md:2594:    assert result['status'] == 'pending_admin'
docs/design/2026-05-27-system-design.md:2604:    response = bind_wechat(student_id='2020001', openid='oXXX', password='wrong')
docs/design/2026-05-27-system-design.md:2630:    bind_wechat(student_id='2020001', openid='oXXX', password='pass')
docs/design/2026-05-27-system-design.md:2638:    r1 = bind_wechat(student_id='9999999', openid='oXXX', password='pass')
docs/design/2026-05-27-system-design.md:2640:    r2 = bind_wechat(student_id='2020001', openid='oXXX', password='wrong')
docs/design/2026-05-27-system-design.md:2642:    r3 = bind_wechat(student_id='2020002', openid='oXXX', password='pass')
docs/design/2026-05-27-system-design.md:2648:def test_student_cannot_approve():
docs/design/2026-05-27-system-design.md:2650:    client.force_authenticate(user=student_user)
docs/design/2026-05-27-system-design.md:2678:    approve_application(app_id, counselor_id, 'approve')
docs/design/2026-05-27-system-design.md:2712:2. 辅导员审批流程
docs/design/2026-05-27-system-design.md:2713:3. 学工部备案流程

exec
/bin/bash -lc 'rtk git status --short' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
 M .omc/state/hud-stdin-cache.json
?? .omc/project-memory.json
?? .omc/sessions/
?? .omc/state/agent-replay-f91e1567-b1b2-4cc2-bd9b-355702bc1ec4.jsonl
?? .omc/state/checkpoints/
?? .omc/state/last-tool-error.json
?? .omc/state/mission-state.json
?? .omc/state/sessions/dcf39a3e-1b72-449a-9897-852c3c7f1253/
?? .omc/state/sessions/f91e1567-b1b2-4cc2-bd9b-355702bc1ec4/
?? .omc/state/subagent-tracking.json
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
?? "\346\257\225\344\270\232\347\246\273\346\240\241\347\263\273\347\273\237\347\224\250\346\210\267\346\226\207\346\241\243.zip"
exec
/bin/bash -lc "rtk sed -n '1360,1450p' docs/design/2026-05-27-system-design.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
        return wrapper
    return decorator

# 使用
@role_required('counselor', 'admin')
def approve_application(request, application_id):
    pass
```

**DRF权限类：**
```python
from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'

class IsCounselor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'counselor'

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.student_id == request.user.id
```

---

## 5. 审批流程设计

### 5.1 流程状态机

**状态定义：**
```
draft（草稿）
  ↓ submit
pending_counselor（待辅导员审核）
  ↓ approve              ↓ reject
pending_admin        rejected（已驳回）
（待学工部备案）
  ↓ approve
approved（审批通过）
```

**状态转换规则：**
```python
STATE_TRANSITIONS = {
    'draft': ['pending_counselor'],  # 提交
    'pending_counselor': ['pending_admin', 'rejected'],  # 辅导员审批
    'pending_admin': ['approved', 'rejected'],  # 学工部审批
    'rejected': ['pending_counselor'],  # 重新提交
    'approved': []  # 终态
}
```

### 5.2 流程节点定义

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
  - 发送通知给辅导员
- 办理时限：无

**节点2：辅导员审核**
- 触发条件：申请状态为 pending_counselor
- 权限要求：辅导员角色 + current_approver_id匹配
- 执行动作：
  - 验证版本号（乐观锁）
  - 同意：
    - 状态变更 → pending_admin
    - 更新当前审批人：current_approver_id = admin_id
    - 递增版本：version += 1
    - 创建审批记录：approvals（approver_role='counselor', action='approve'）
    - 创建历史快照：applications_history（version=N, change_reason='辅导员审批通过'）
    - 记录审计日志：audit_logs（action='approve', resource_type='application'）
    - 通知学工部
  - 驳回：
    - 状态变更 → rejected

exec
/bin/bash -lc "rtk sed -n '230,330p' docs/design/2026-05-27-system-design.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:

---

## 2. 数据库设计

### 2.1 数据库概述

**设计原则：**
- 本项目使用PostgreSQL数据库
- 使用 Django ORM 抽象层
- 遵循第三范式（3NF）
- 预留扩展字段
- 软删除设计（Django应用层过滤 + PROTECT外键）
- 外部系统通过API对接（支持MySQL/SQL Server/Oracle等异构系统）

**核心表：**
1. users - 用户表
2. applications - 离校申请表
3. approvals - 审批记录表
4. attachments - 附件表
5. notifications - 通知表
6. system_configs - 系统配置表
7. audit_logs - 审计日志表
8. applications_history - 申请历史表

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
    

exec
/bin/bash -lc "rtk sed -n '232,252p' docs/用户设计说明书.md" in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
**Q4：如何导出审批数据？**
A：学工部用户在"审批统计"页面点击"导出Excel"按钮。

### 6.3 系统管理问题

**Q1：如何批量导入学生用户？**
A：准备Excel模板（学号、姓名、专业、班级、辅导员），在管理后台上传。

**Q2：如何修改审批时限？**
A：在系统配置页面修改"审批时限"参数（单位：小时）。

**Q3：如何查看系统日志？**
A：在管理后台"审计日志"页面查看，支持按用户、操作、时间筛选。

**Q4：如何对接宿舍管理系统？**
A：参考《数据对接说明文档》，提供API接口或数据导出。

---

## 七、技术支持


codex
我看到了目标文件已经存在且内容方向基本正确，但会按这次问题重新整理成更明确的审查结论：先给 P0/P1 判定，再给每个数据源的推荐接入方式、遗漏项和实施顺序。接下来只改这个指定文件。
apply patch
patch: completed
/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
diff --git a/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md b/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
index 1d05e91d83dcdc2502f89f0c53089a2ebe46ea67..aa0d6707f9ae91a17c3a66923547ae34c0185a41
--- a/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
+++ b/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
@@ -1,93 +1,166 @@
 # 数据源完整性审查与建议
 
 **审查时间：** 2026-05-27  
-**审查对象：** `29-data-source-analysis.md`、`docs/数据对接说明文档.md`、用户设计与系统设计相关要求  
+**审查对象：** `29-data-source-analysis.md`、`docs/数据对接说明文档.md`、用户设计说明书、系统设计文档  
+
+---
+
+## 一、总体结论
+
+`29-data-source-analysis.md` 的方向是正确的：当前数据对接文档只覆盖宿舍清退，无法完整支撑 student、counselor、admin 三类角色的账号初始化、权限边界和自动审批分配。
+
+需要调整的重点有两点：
+
+1. **班级-辅导员对应关系应明确列为 P0。** 这是自动分配审批人的核心数据。没有它，系统提交申请时无法稳定设置 `counselor_id` 和 `current_approver_id`，只能退化为人工逐个配置或人工改派。
+2. **首版不应追求所有数据源 API 化。** 对约 1000 名学生、约 50 名辅导员、约 5 名管理员的规模，CSV/Excel 批量导入加严格校验更现实；API 更适合作为后续自动化增强。
 
 ---
 
-## 1. Priority Classification
+## 二、优先级分类
 
-### P0：上线必须具备的数据
+### P0：上线必须具备
 
-| 数据源 | 优先级 | 判定 | 理由 |
-|--------|--------|------|------|
-| 学生基本信息 | P0 | 必须纳入数据对接文档 | `29-data-source-analysis.md` 第三章 3.1 已列为 P0，用途包括创建学生账号、身份验证、按班级分配审批人。用户设计说明书也明确“学号由学校统一导入”，因此它不是单纯便利项。技术上可用手工 Excel 导入替代 API，但数据源和字段规范必须写进对接文档。 |
-| 班级-辅导员对应关系 | P0 | 必须纳入数据对接文档 | `29-data-source-analysis.md` 第三章 3.4 和第七章 7.1 都指出缺失后系统无法自动分配审批人，需要手动配置约 1000 人/届。系统设计中的 `applications.counselor_id`、`current_approver_id` 也依赖该关系在提交时固化审批人。 |
-| 辅导员基本信息 | P0 | 必须具备，但实时 API 不是必须 | `29-data-source-analysis.md` 第三章 3.3 将其列为 P0，原因是创建辅导员账号和分配审批权限。约 50 人规模下，CSV/Excel 导入已经可满足上线；API 是运维优化，不是首版硬要求。 |
-| 宿舍清退数据 | P0 | 已覆盖，继续保持 P0 | 当前数据对接文档已覆盖宿舍系统。用户设计说明书将宿舍清退作为提交前自动验证项，同时保留手动上传证明作为降级方案。 |
-| 学籍/毕业资格 | P0 字段，P1 独立接口 | 应并入学生基本信息首批导入 | `29-data-source-analysis.md` 第四章 4.3 将学籍状态列为 P1，但其用途包含“限制只有毕业生可以提交离校申请”。如果学生基本信息只导入当届毕业生，则不需要独立实时接口；如果导入全校学生，则 `graduation_status` / `graduation_year` / `eligible_for_leave` 必须作为 P0 字段。独立学籍 API 可放到 P1。 |
+| 数据源 | 来源系统 | P0 判定 | 原因 |
+|--------|----------|---------|------|
+| 学生基本信息 | 教务系统 | P0 | 用于创建学生账号、身份识别、展示院系专业班级、限定毕业离校申请人范围。用户设计说明书已出现“学号、姓名、专业、班级”和“批量导入学生用户”的要求，因此必须写入数据对接文档。 |
+| 辅导员基本信息 | 人事系统或人工台账 | P0 | 用于创建 counselor 账号和审批权限主体。实时同步不是 P0，但账号数据本身是 P0。 |
+| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
+| 宿舍清退数据 | 宿管系统 | P0 | 当前业务把宿舍清退作为提交前校验项，现有对接文档已覆盖。即使保留人工证明降级，正式流程仍应具备自动校验或批量数据导入能力。 |
+| 毕业资格/离校资格字段 | 教务系统 | P0 字段，非 P0 独立接口 | 如果系统只导入当届毕业生，可通过导入范围满足；如果导入全量学生，则必须在学生基本信息中带 `graduation_year`、`graduation_status` 或 `eligible_for_leave`。不建议首版单独建设学籍 API。 |
 
-### P1：提升自动化或审核运营效率的数据
+### P1：可选增强
 
-| 数据源 | 优先级 | 判定 | 理由 |
-|--------|--------|------|------|
-| 学工部管理员信息 | P1 | 不建议做系统级数据对接 | `29-data-source-analysis.md` 第三章 3.5 和第六章均说明管理员约 5 人，可手动创建。这里是账号初始化问题，不是高频数据同步问题。 |
-| 图书馆清书状态 | P1 | 可选集成 | `29-data-source-analysis.md` 第四章 4.1 说明当前方案是上传清书证明截图。附件表也已有 `library_clearance` 类型，因此首版可运行；API 集成主要减少截图审核和伪造风险。 |
-| 财务结清状态 | P1 | 可选集成，优先级略高于图书馆 | `29-data-source-analysis.md` 第四章 4.2 说明当前方案是上传财务结清截图。考虑费用状态的业务敏感性，若财务系统已有稳定接口，可比图书馆更早做，但不应阻塞首版。 |
+| 数据源 | 来源系统 | P1 判定 | 原因 |
+|--------|----------|---------|------|
+| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
+| 图书馆清书状态 | 图书馆系统 | P1 | 当前已有上传截图的人工方案。接口集成能降低审核成本和伪造风险，但不应阻塞首版上线。 |
+| 财务结清状态 | 财务系统 | P1 | 当前已有上传截图的人工方案。由于财务状态更敏感，若后续接口条件成熟，优先级可高于图书馆，但仍不是首版 P0。 |
+| 独立学籍状态接口 | 教务系统 | P1 | 只有在多届学生并行、延期毕业、结业/退学实时变化等需求明确时，才需要独立 API。首版可并入学生基础数据。 |
 
 ---
 
-## 2. Integration Recommendations
+## 三、对接方式建议
 
-| 数据源 | 推荐方式 | 备选方式 | 建议字段/补充要求 |
-|--------|----------|----------|------------------|
-| 学生基本信息 | CSV/Excel 批量导入作为首版标准方案 | 教务系统 API | 首版按届导入约 1000 人，批量文件更容易落地。字段除分析文档列出的 `student_id`、`name`、`department`、`major`、`class_name`、`grade` 外，建议增加 `class_id`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
-| 班级-辅导员对应关系 | CSV/Excel 批量导入，必须有校验报告 | 教务系统 API | 这是 P0 数据，但不要求实时。建议以 `class_id + counselor_employee_id + effective_term` 为主键逻辑，避免只靠班级名称匹配。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无负责人的学生数。 |
-| 辅导员基本信息 | CSV/Excel 批量导入 | HR API | 约 50 人，首版 API 收益有限。字段包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API 同步。 |
-| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入 | 当前文档策略合理。申请提交时需要实时性，API 价值高；若宿管系统无法提供 API，则保留手动上传证明和文件导入。 |
-| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 约 5 人，不建议接 HR API。需要在文档中明确由系统管理员维护，并保留角色授权、停用、重置密码流程。 |
-| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 不作为首版阻塞项。若后续对接，建议只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，避免引入借阅明细等非必要个人数据。 |
-| 财务结清状态 | 首版手动上传截图 | API 优先于 CSV | 不作为首版阻塞项。若对接，应只返回结清布尔值和日期，不同步欠费明细；失败时保留人工审核通道。 |
-| 学籍/毕业资格 | 并入学生基本信息导入 | 教务系统 API | 不建议首版单独建接口。只有在系统长期服务多届、多状态学生，或需要实时处理延期毕业/结业/退学时，再做独立 API。 |
+| 数据源 | 推荐方式 | 备选方式 | 关键建议 |
+|--------|----------|----------|----------|
+| 学生基本信息 | CSV/Excel 批量导入 | 教务系统 API | 首版按毕业届别导入更容易落地。字段建议包括 `student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
+| 辅导员基本信息 | CSV/Excel 批量导入 | 人事系统 API 或手动创建 | 约 50 人规模下，批量导入足够。字段建议包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API。 |
+| 班级-辅导员对应关系 | CSV/Excel 批量导入并强校验 | 教务系统 API | 必须优先支持。建议用 `class_id + counselor_employee_id + effective_term` 表达关系，不要只靠 `class_name`。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无审批人的学生数。 |
+| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入、人工证明降级 | 当前文档策略合理。提交申请时实时性较强，API 价值高；若宿管系统暂不支持 API，则每日文件导入加人工证明降级。 |
+| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
+| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 后续对接时只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，不要引入借阅明细。 |
+| 财务结清状态 | 首版手动上传截图 | API 优先于 CSV | 后续对接时只返回是否结清和结清日期，不同步欠费明细；外部系统失败时保留人工审核通道。 |
+| 学籍/毕业资格 | 并入学生基本信息导入 | 教务系统 API | 首版不要单独拆接口。若后续存在延期毕业、结业、退学状态的实时变更，再建设独立同步。 |
 
 ---
 
-## 3. Missing Considerations
+## 四、对五个核心问题的直接回答
 
-1. **班级唯一标识不足。** 当前分析使用 `class_name`，但同名、改名、跨届复用都可能发生。对接文档应优先要求 `class_id`，`class_name` 仅用于展示。
+### 1. 学生基本信息是否需要写入数据对接文档？
 
-2. **账号生命周期未定义。** 需要明确新增、更新、停用、毕业后归档、辅导员离职/调岗后的处理规则。否则 CSV 导入只能新增，无法可靠处理人员变化。
+需要，且应列为 P0。
 
-3. **导入校验与人工修复流程缺失。** P0 数据不只需要字段格式，还需要“导入前校验、导入失败明细、重复数据处理、回滚/覆盖策略、导入审计日志”。
+原因不是“方便展示”，而是学生账号、身份识别、申请资格、班级映射都依赖它。当前数据对接文档的目标用户也应从“宿舍管理系统管理员”扩展为“教务系统、人事系统、宿管系统及业务数据负责人”。
 
-4. **审批人变更后的历史一致性。** 系统设计中申请会固化 `counselor_id`。应明确：已提交申请不随映射变更自动改审批人，除非管理员执行带审计的改派操作。
+### 2. 辅导员数据源如何对接？
 
-5. **多辅导员/代理审批场景。** 一个班级可能存在主辅导员、临时代办、请假代理。建议首版至少支持一个主负责人，并在后台预留手动改派能力。
+首版推荐 CSV/Excel 批量导入，不推荐一开始就要求人事系统 API。
 
-6. **组织架构与权限边界。** 学工部可看全校，辅导员只能看负责班级。除班级映射外，还需要院系、专业、年级等维度用于筛选、统计和异常排查。
+理由是辅导员规模约 50 人，变化频率低，API 改造投入可能高于收益。但数据结构必须标准化，尤其是 `employee_id` 要能被班级-辅导员映射引用。若学校已有成熟 HR API 或统一身份平台，可在后续升级为 API 同步。
 
-7. **数据最小化与敏感信息边界。** 不应为验证身份引入身份证号、欠费明细、借阅明细等高敏字段。此前共识中 `student_id + name` 已足够识别学生，应继续沿用最小字段集。
+### 3. 班级-辅导员对应关系是否应为 P0？
 
-8. **降级策略需要统一。** 宿舍、图书馆、财务都可能不可用。文档应区分“自动验证失败”“外部系统不可用”“学生确未完成清退/结清”，并定义人工审核入口。
+应为 P0，而且是当前缺口中风险最高的数据源。
 
-9. **毕业离校批次配置。** 计划离校日期范围、当前开放届别、申请开放/关闭时间不一定来自学生信息本身，可能需要系统配置或教务校历数据。
+它直接影响：
+
+- 学生提交时能否自动设置辅导员审批人；
+- 辅导员是否只能查看和审批负责班级；
+- 待办通知能否准确发送；
+- 审批统计能否按院系、班级、辅导员追踪。
+
+建议数据对接文档单独增加“审批关系数据”章节，并把导入覆盖率 100% 作为上线验收条件之一。
+
+### 4. 学工部管理员数据源是否需要对接？
+
+不建议做外部数据对接，手动创建即可。
+
+约 5 人的规模下，真正重要的是权限授予、停用、密码重置、操作审计，而不是与人事系统同步。文档应说明由系统管理员在后台维护，不应把它列为 P0 数据接口。
+
+### 5. 图书馆、财务、学籍是否需要对接？
+
+图书馆和财务可保持 P1。首版延续截图上传和人工审核，后续按审核量、造假风险、外部系统接口成熟度决定是否对接。若只能先选一个，建议先评估财务结清状态，因为财务数据的业务风险通常高于图书馆清书。
+
+学籍状态不建议作为首版独立接口，但毕业资格字段必须进入学生基础数据。换句话说，“是否允许提交离校申请”必须有数据依据，只是不一定需要实时 API。
+
+---
+
+## 五、遗漏或需补充考虑的数据项
+
+1. **班级唯一标识。** 当前分析偏向 `class_name`，但班级名称可能重复、改名或跨届复用。应要求 `class_id`，`class_name` 只用于展示。
+
+2. **组织架构数据。** 院系、专业、年级不仅用于展示，也用于权限过滤、统计导出、异常排查。首版可随学生和辅导员数据导入，不必单独做组织架构接口。
+
+3. **账号生命周期。** 需要定义新增、更新、停用、毕业归档、辅导员离职/调岗、管理员离岗后的处理规则。
+
+4. **导入校验和差异报告。** P0 数据导入不能只要求字段格式，还应要求失败明细、重复数据处理、覆盖策略、回滚策略和导入审计日志。
+
+5. **审批人变更后的历史一致性。** 已提交申请中的 `counselor_id` 应保持历史一致，不应因后续班级映射变更自动改写。若需改派，应由管理员显式操作并记录审计日志。
+
+6. **多辅导员和代理审批。** 现实中可能有主辅导员、代管辅导员、临时代理。首版可只要求一个主审批人，但后台应预留人工改派能力。
+
+7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
+
+8. **离校批次配置。** 开放申请时间、允许离校日期范围、毕业届别可能来自业务配置，而不一定来自教务系统。应作为系统配置纳入实施计划。
+
+9. **通知联系方式。** `phone`、`email` 对提醒和异常联系有价值；微信 `openid` 应通过用户绑定产生，不应从外部系统导入。
+
+10. **数据最小化。** 不应为了校验引入身份证号、欠费明细、借阅明细等高敏字段。业务校验只需要结论、日期、来源更新时间和必要的学生标识。
 
-10. **通知数据来源。** `phone`、`email` 对审批提醒和异常联系有价值；微信 `openid` 应通过用户绑定产生，不应从外部系统导入。
+11. **外部系统不可用时的降级口径。** 需要区分“学生确未完成”“外部系统失败”“系统数据过期”“人工证明待审核”，避免所有异常都被误判为不通过。
 
 ---
 
-## 4. Implementation Sequence
+## 六、建议实施顺序
 
-1. **先扩展数据对接文档范围。** 将文档标题和目标用户从“宿舍管理系统对接”扩展为“毕业离校系统数据对接”，拆分为账号基础数据、审批关系数据、业务校验数据三类。
+1. **重构数据对接说明文档目录。** 从单一“宿舍对接”扩展为“账号基础数据、审批关系数据、业务校验数据、降级与审计”四类。
 
-2. **实现学生基本信息导入。** 首版采用 CSV/Excel，支持新增和更新，要求导入当届毕业生或带 `eligible_for_leave` 字段。没有这一步，统一账号、身份验证和申请资格都不稳定。
+2. **定义学生基本信息导入模板。** 先支持 CSV/Excel 导入当届毕业生，包含毕业资格字段和班级唯一标识。
 
-3. **实现辅导员基本信息导入。** 先用 CSV/Excel 创建约 50 个辅导员账号，确保 `employee_id` 可被后续映射引用。
+3. **定义辅导员基本信息导入模板。** 先确保 counselor 账号存在，且 `employee_id` 可被映射数据引用。
 
-4. **实现班级-辅导员映射导入和覆盖率校验。** 这是审批自动分配的关键路径。上线前必须达到 100% 当届学生可解析到辅导员；异常学生应进入导入报告而不是运行时才暴露。
+4. **实现班级-辅导员映射导入。** 这是最关键步骤。上线前必须校验当届学生 100% 能解析到有效辅导员，否则不应开放提交。
 
-5. **保留并完善宿舍清退对接。** 当前文档已较完整，下一步重点是把它接入统一的外部校验/降级策略，而不是继续孤立成唯一数据源。
+5. **保留并完善宿舍清退对接。** 当前文档已较完整，下一步应把它纳入统一的校验结果、缓存、失败降级和审计机制。
 
-6. **手动创建学工部管理员账号。** 同时补充后台维护流程，包括新增、停用、密码重置、角色授权审计。
+6. **手动创建学工部管理员。** 同时补充管理员账号维护和终审人分配规则。
 
-7. **将学籍/毕业资格并入学生导入字段。** 先不要单独建设学籍 API；待多届并行、延期毕业等需求明确后，再升级为教务系统实时同步。
+7. **将毕业资格并入学生数据。** 首版不单独做学籍接口；后续根据延期毕业、多届并行等场景再升级。
 
-8. **按投入产出评估图书馆和财务接口。** 首版继续截图上传；若实际审核量大、截图造假风险高或外部系统已有成熟 API，则优先财务、再图书馆。
+8. **评估财务与图书馆接口。** 首版继续截图上传。若后续审核量大或截图可信度不足，优先财务，再图书馆。
 
-9. **最后补齐运营治理能力。** 包括导入审计、差异报表、外部接口监控、数据更新时间展示、人工改派和人工审核日志。这些不是单个数据源，但决定数据对接上线后的可维护性。
+9. **补齐运营治理能力。** 包括导入审计、失败重试、差异报表、外部数据更新时间展示、人工改派、人工审核日志。
 
 ---
 
-## 结论
+## 七、建议修改数据对接文档的最小范围
+
+为了避免文档一次性扩得过大，建议先补充以下最小内容：
 
-学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据都应进入数据对接文档，其中班级-辅导员映射是最高风险缺口。首版不应追求所有系统 API 化；对约 1000 名学生和约 50 名辅导员，CSV/Excel 导入加严格校验更现实。管理员账号、图书馆、财务、独立学籍接口属于 P1 或后续增强，不应阻塞核心审批闭环上线。
+1. 新增“学生基本信息导入”章节，提供 CSV/Excel 模板字段。
+2. 新增“辅导员基本信息导入”章节，明确 `employee_id`、联系方式和账号状态。
+3. 新增“班级-辅导员对应关系导入”章节，列为 P0，并写明覆盖率和异常报告要求。
+4. 将“宿舍清退数据”保留为业务校验数据，并补充与人工证明降级的关系。
+5. 在附录中增加三份模板：学生基础数据、辅导员基础数据、班级-辅导员映射。
+
+---
+
+## 八、最终建议
+
+同意 `29-data-source-analysis.md` 对主要缺失数据源的识别，但建议将结论进一步收敛为：
+
+- **P0 数据：** 学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据、毕业资格字段。
+- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
+- **首版策略：** 账号和映射数据用 CSV/Excel 批量导入，宿舍清退优先 API，管理员手动维护，图书馆/财务继续截图上传。
+- **最高优先级行动：** 立即补充班级-辅导员映射的数据规范和导入校验，这是自动审批闭环的关键缺口。
+

diff --git a/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md b/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
index 1d05e91d83dcdc2502f89f0c53089a2ebe46ea67..aa0d6707f9ae91a17c3a66923547ae34c0185a41
--- a/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
+++ b/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
@@ -1,93 +1,166 @@
 # 数据源完整性审查与建议
 
 **审查时间：** 2026-05-27  
-**审查对象：** `29-data-source-analysis.md`、`docs/数据对接说明文档.md`、用户设计与系统设计相关要求  
+**审查对象：** `29-data-source-analysis.md`、`docs/数据对接说明文档.md`、用户设计说明书、系统设计文档  
+
+---
+
+## 一、总体结论
+
+`29-data-source-analysis.md` 的方向是正确的：当前数据对接文档只覆盖宿舍清退，无法完整支撑 student、counselor、admin 三类角色的账号初始化、权限边界和自动审批分配。
+
+需要调整的重点有两点：
+
+1. **班级-辅导员对应关系应明确列为 P0。** 这是自动分配审批人的核心数据。没有它，系统提交申请时无法稳定设置 `counselor_id` 和 `current_approver_id`，只能退化为人工逐个配置或人工改派。
+2. **首版不应追求所有数据源 API 化。** 对约 1000 名学生、约 50 名辅导员、约 5 名管理员的规模，CSV/Excel 批量导入加严格校验更现实；API 更适合作为后续自动化增强。
 
 ---
 
-## 1. Priority Classification
+## 二、优先级分类
 
-### P0：上线必须具备的数据
+### P0：上线必须具备
 
-| 数据源 | 优先级 | 判定 | 理由 |
-|--------|--------|------|------|
-| 学生基本信息 | P0 | 必须纳入数据对接文档 | `29-data-source-analysis.md` 第三章 3.1 已列为 P0，用途包括创建学生账号、身份验证、按班级分配审批人。用户设计说明书也明确“学号由学校统一导入”，因此它不是单纯便利项。技术上可用手工 Excel 导入替代 API，但数据源和字段规范必须写进对接文档。 |
-| 班级-辅导员对应关系 | P0 | 必须纳入数据对接文档 | `29-data-source-analysis.md` 第三章 3.4 和第七章 7.1 都指出缺失后系统无法自动分配审批人，需要手动配置约 1000 人/届。系统设计中的 `applications.counselor_id`、`current_approver_id` 也依赖该关系在提交时固化审批人。 |
-| 辅导员基本信息 | P0 | 必须具备，但实时 API 不是必须 | `29-data-source-analysis.md` 第三章 3.3 将其列为 P0，原因是创建辅导员账号和分配审批权限。约 50 人规模下，CSV/Excel 导入已经可满足上线；API 是运维优化，不是首版硬要求。 |
-| 宿舍清退数据 | P0 | 已覆盖，继续保持 P0 | 当前数据对接文档已覆盖宿舍系统。用户设计说明书将宿舍清退作为提交前自动验证项，同时保留手动上传证明作为降级方案。 |
-| 学籍/毕业资格 | P0 字段，P1 独立接口 | 应并入学生基本信息首批导入 | `29-data-source-analysis.md` 第四章 4.3 将学籍状态列为 P1，但其用途包含“限制只有毕业生可以提交离校申请”。如果学生基本信息只导入当届毕业生，则不需要独立实时接口；如果导入全校学生，则 `graduation_status` / `graduation_year` / `eligible_for_leave` 必须作为 P0 字段。独立学籍 API 可放到 P1。 |
+| 数据源 | 来源系统 | P0 判定 | 原因 |
+|--------|----------|---------|------|
+| 学生基本信息 | 教务系统 | P0 | 用于创建学生账号、身份识别、展示院系专业班级、限定毕业离校申请人范围。用户设计说明书已出现“学号、姓名、专业、班级”和“批量导入学生用户”的要求，因此必须写入数据对接文档。 |
+| 辅导员基本信息 | 人事系统或人工台账 | P0 | 用于创建 counselor 账号和审批权限主体。实时同步不是 P0，但账号数据本身是 P0。 |
+| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
+| 宿舍清退数据 | 宿管系统 | P0 | 当前业务把宿舍清退作为提交前校验项，现有对接文档已覆盖。即使保留人工证明降级，正式流程仍应具备自动校验或批量数据导入能力。 |
+| 毕业资格/离校资格字段 | 教务系统 | P0 字段，非 P0 独立接口 | 如果系统只导入当届毕业生，可通过导入范围满足；如果导入全量学生，则必须在学生基本信息中带 `graduation_year`、`graduation_status` 或 `eligible_for_leave`。不建议首版单独建设学籍 API。 |
 
-### P1：提升自动化或审核运营效率的数据
+### P1：可选增强
 
-| 数据源 | 优先级 | 判定 | 理由 |
-|--------|--------|------|------|
-| 学工部管理员信息 | P1 | 不建议做系统级数据对接 | `29-data-source-analysis.md` 第三章 3.5 和第六章均说明管理员约 5 人，可手动创建。这里是账号初始化问题，不是高频数据同步问题。 |
-| 图书馆清书状态 | P1 | 可选集成 | `29-data-source-analysis.md` 第四章 4.1 说明当前方案是上传清书证明截图。附件表也已有 `library_clearance` 类型，因此首版可运行；API 集成主要减少截图审核和伪造风险。 |
-| 财务结清状态 | P1 | 可选集成，优先级略高于图书馆 | `29-data-source-analysis.md` 第四章 4.2 说明当前方案是上传财务结清截图。考虑费用状态的业务敏感性，若财务系统已有稳定接口，可比图书馆更早做，但不应阻塞首版。 |
+| 数据源 | 来源系统 | P1 判定 | 原因 |
+|--------|----------|---------|------|
+| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
+| 图书馆清书状态 | 图书馆系统 | P1 | 当前已有上传截图的人工方案。接口集成能降低审核成本和伪造风险，但不应阻塞首版上线。 |
+| 财务结清状态 | 财务系统 | P1 | 当前已有上传截图的人工方案。由于财务状态更敏感，若后续接口条件成熟，优先级可高于图书馆，但仍不是首版 P0。 |
+| 独立学籍状态接口 | 教务系统 | P1 | 只有在多届学生并行、延期毕业、结业/退学实时变化等需求明确时，才需要独立 API。首版可并入学生基础数据。 |
 
 ---
 
-## 2. Integration Recommendations
+## 三、对接方式建议
 
-| 数据源 | 推荐方式 | 备选方式 | 建议字段/补充要求 |
-|--------|----------|----------|------------------|
-| 学生基本信息 | CSV/Excel 批量导入作为首版标准方案 | 教务系统 API | 首版按届导入约 1000 人，批量文件更容易落地。字段除分析文档列出的 `student_id`、`name`、`department`、`major`、`class_name`、`grade` 外，建议增加 `class_id`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
-| 班级-辅导员对应关系 | CSV/Excel 批量导入，必须有校验报告 | 教务系统 API | 这是 P0 数据，但不要求实时。建议以 `class_id + counselor_employee_id + effective_term` 为主键逻辑，避免只靠班级名称匹配。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无负责人的学生数。 |
-| 辅导员基本信息 | CSV/Excel 批量导入 | HR API | 约 50 人，首版 API 收益有限。字段包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API 同步。 |
-| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入 | 当前文档策略合理。申请提交时需要实时性，API 价值高；若宿管系统无法提供 API，则保留手动上传证明和文件导入。 |
-| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 约 5 人，不建议接 HR API。需要在文档中明确由系统管理员维护，并保留角色授权、停用、重置密码流程。 |
-| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 不作为首版阻塞项。若后续对接，建议只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，避免引入借阅明细等非必要个人数据。 |
-| 财务结清状态 | 首版手动上传截图 | API 优先于 CSV | 不作为首版阻塞项。若对接，应只返回结清布尔值和日期，不同步欠费明细；失败时保留人工审核通道。 |
-| 学籍/毕业资格 | 并入学生基本信息导入 | 教务系统 API | 不建议首版单独建接口。只有在系统长期服务多届、多状态学生，或需要实时处理延期毕业/结业/退学时，再做独立 API。 |
+| 数据源 | 推荐方式 | 备选方式 | 关键建议 |
+|--------|----------|----------|----------|
+| 学生基本信息 | CSV/Excel 批量导入 | 教务系统 API | 首版按毕业届别导入更容易落地。字段建议包括 `student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
+| 辅导员基本信息 | CSV/Excel 批量导入 | 人事系统 API 或手动创建 | 约 50 人规模下，批量导入足够。字段建议包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API。 |
+| 班级-辅导员对应关系 | CSV/Excel 批量导入并强校验 | 教务系统 API | 必须优先支持。建议用 `class_id + counselor_employee_id + effective_term` 表达关系，不要只靠 `class_name`。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无审批人的学生数。 |
+| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入、人工证明降级 | 当前文档策略合理。提交申请时实时性较强，API 价值高；若宿管系统暂不支持 API，则每日文件导入加人工证明降级。 |
+| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
+| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 后续对接时只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，不要引入借阅明细。 |
+| 财务结清状态 | 首版手动上传截图 | API 优先于 CSV | 后续对接时只返回是否结清和结清日期，不同步欠费明细；外部系统失败时保留人工审核通道。 |
+| 学籍/毕业资格 | 并入学生基本信息导入 | 教务系统 API | 首版不要单独拆接口。若后续存在延期毕业、结业、退学状态的实时变更，再建设独立同步。 |
 
 ---
 
-## 3. Missing Considerations
+## 四、对五个核心问题的直接回答
 
-1. **班级唯一标识不足。** 当前分析使用 `class_name`，但同名、改名、跨届复用都可能发生。对接文档应优先要求 `class_id`，`class_name` 仅用于展示。
+### 1. 学生基本信息是否需要写入数据对接文档？
 
-2. **账号生命周期未定义。** 需要明确新增、更新、停用、毕业后归档、辅导员离职/调岗后的处理规则。否则 CSV 导入只能新增，无法可靠处理人员变化。
+需要，且应列为 P0。
 
-3. **导入校验与人工修复流程缺失。** P0 数据不只需要字段格式，还需要“导入前校验、导入失败明细、重复数据处理、回滚/覆盖策略、导入审计日志”。
+原因不是“方便展示”，而是学生账号、身份识别、申请资格、班级映射都依赖它。当前数据对接文档的目标用户也应从“宿舍管理系统管理员”扩展为“教务系统、人事系统、宿管系统及业务数据负责人”。
 
-4. **审批人变更后的历史一致性。** 系统设计中申请会固化 `counselor_id`。应明确：已提交申请不随映射变更自动改审批人，除非管理员执行带审计的改派操作。
+### 2. 辅导员数据源如何对接？
 
-5. **多辅导员/代理审批场景。** 一个班级可能存在主辅导员、临时代办、请假代理。建议首版至少支持一个主负责人，并在后台预留手动改派能力。
+首版推荐 CSV/Excel 批量导入，不推荐一开始就要求人事系统 API。
 
-6. **组织架构与权限边界。** 学工部可看全校，辅导员只能看负责班级。除班级映射外，还需要院系、专业、年级等维度用于筛选、统计和异常排查。
+理由是辅导员规模约 50 人，变化频率低，API 改造投入可能高于收益。但数据结构必须标准化，尤其是 `employee_id` 要能被班级-辅导员映射引用。若学校已有成熟 HR API 或统一身份平台，可在后续升级为 API 同步。
 
-7. **数据最小化与敏感信息边界。** 不应为验证身份引入身份证号、欠费明细、借阅明细等高敏字段。此前共识中 `student_id + name` 已足够识别学生，应继续沿用最小字段集。
+### 3. 班级-辅导员对应关系是否应为 P0？
 
-8. **降级策略需要统一。** 宿舍、图书馆、财务都可能不可用。文档应区分“自动验证失败”“外部系统不可用”“学生确未完成清退/结清”，并定义人工审核入口。
+应为 P0，而且是当前缺口中风险最高的数据源。
 
-9. **毕业离校批次配置。** 计划离校日期范围、当前开放届别、申请开放/关闭时间不一定来自学生信息本身，可能需要系统配置或教务校历数据。
+它直接影响：
+
+- 学生提交时能否自动设置辅导员审批人；
+- 辅导员是否只能查看和审批负责班级；
+- 待办通知能否准确发送；
+- 审批统计能否按院系、班级、辅导员追踪。
+
+建议数据对接文档单独增加“审批关系数据”章节，并把导入覆盖率 100% 作为上线验收条件之一。
+
+### 4. 学工部管理员数据源是否需要对接？
+
+不建议做外部数据对接，手动创建即可。
+
+约 5 人的规模下，真正重要的是权限授予、停用、密码重置、操作审计，而不是与人事系统同步。文档应说明由系统管理员在后台维护，不应把它列为 P0 数据接口。
+
+### 5. 图书馆、财务、学籍是否需要对接？
+
+图书馆和财务可保持 P1。首版延续截图上传和人工审核，后续按审核量、造假风险、外部系统接口成熟度决定是否对接。若只能先选一个，建议先评估财务结清状态，因为财务数据的业务风险通常高于图书馆清书。
+
+学籍状态不建议作为首版独立接口，但毕业资格字段必须进入学生基础数据。换句话说，“是否允许提交离校申请”必须有数据依据，只是不一定需要实时 API。
+
+---
+
+## 五、遗漏或需补充考虑的数据项
+
+1. **班级唯一标识。** 当前分析偏向 `class_name`，但班级名称可能重复、改名或跨届复用。应要求 `class_id`，`class_name` 只用于展示。
+
+2. **组织架构数据。** 院系、专业、年级不仅用于展示，也用于权限过滤、统计导出、异常排查。首版可随学生和辅导员数据导入，不必单独做组织架构接口。
+
+3. **账号生命周期。** 需要定义新增、更新、停用、毕业归档、辅导员离职/调岗、管理员离岗后的处理规则。
+
+4. **导入校验和差异报告。** P0 数据导入不能只要求字段格式，还应要求失败明细、重复数据处理、覆盖策略、回滚策略和导入审计日志。
+
+5. **审批人变更后的历史一致性。** 已提交申请中的 `counselor_id` 应保持历史一致，不应因后续班级映射变更自动改写。若需改派，应由管理员显式操作并记录审计日志。
+
+6. **多辅导员和代理审批。** 现实中可能有主辅导员、代管辅导员、临时代理。首版可只要求一个主审批人，但后台应预留人工改派能力。
+
+7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
+
+8. **离校批次配置。** 开放申请时间、允许离校日期范围、毕业届别可能来自业务配置，而不一定来自教务系统。应作为系统配置纳入实施计划。
+
+9. **通知联系方式。** `phone`、`email` 对提醒和异常联系有价值；微信 `openid` 应通过用户绑定产生，不应从外部系统导入。
+
+10. **数据最小化。** 不应为了校验引入身份证号、欠费明细、借阅明细等高敏字段。业务校验只需要结论、日期、来源更新时间和必要的学生标识。
 
-10. **通知数据来源。** `phone`、`email` 对审批提醒和异常联系有价值；微信 `openid` 应通过用户绑定产生，不应从外部系统导入。
+11. **外部系统不可用时的降级口径。** 需要区分“学生确未完成”“外部系统失败”“系统数据过期”“人工证明待审核”，避免所有异常都被误判为不通过。
 
 ---
 
-## 4. Implementation Sequence
+## 六、建议实施顺序
 
-1. **先扩展数据对接文档范围。** 将文档标题和目标用户从“宿舍管理系统对接”扩展为“毕业离校系统数据对接”，拆分为账号基础数据、审批关系数据、业务校验数据三类。
+1. **重构数据对接说明文档目录。** 从单一“宿舍对接”扩展为“账号基础数据、审批关系数据、业务校验数据、降级与审计”四类。
 
-2. **实现学生基本信息导入。** 首版采用 CSV/Excel，支持新增和更新，要求导入当届毕业生或带 `eligible_for_leave` 字段。没有这一步，统一账号、身份验证和申请资格都不稳定。
+2. **定义学生基本信息导入模板。** 先支持 CSV/Excel 导入当届毕业生，包含毕业资格字段和班级唯一标识。
 
-3. **实现辅导员基本信息导入。** 先用 CSV/Excel 创建约 50 个辅导员账号，确保 `employee_id` 可被后续映射引用。
+3. **定义辅导员基本信息导入模板。** 先确保 counselor 账号存在，且 `employee_id` 可被映射数据引用。
 
-4. **实现班级-辅导员映射导入和覆盖率校验。** 这是审批自动分配的关键路径。上线前必须达到 100% 当届学生可解析到辅导员；异常学生应进入导入报告而不是运行时才暴露。
+4. **实现班级-辅导员映射导入。** 这是最关键步骤。上线前必须校验当届学生 100% 能解析到有效辅导员，否则不应开放提交。
 
-5. **保留并完善宿舍清退对接。** 当前文档已较完整，下一步重点是把它接入统一的外部校验/降级策略，而不是继续孤立成唯一数据源。
+5. **保留并完善宿舍清退对接。** 当前文档已较完整，下一步应把它纳入统一的校验结果、缓存、失败降级和审计机制。
 
-6. **手动创建学工部管理员账号。** 同时补充后台维护流程，包括新增、停用、密码重置、角色授权审计。
+6. **手动创建学工部管理员。** 同时补充管理员账号维护和终审人分配规则。
 
-7. **将学籍/毕业资格并入学生导入字段。** 先不要单独建设学籍 API；待多届并行、延期毕业等需求明确后，再升级为教务系统实时同步。
+7. **将毕业资格并入学生数据。** 首版不单独做学籍接口；后续根据延期毕业、多届并行等场景再升级。
 
-8. **按投入产出评估图书馆和财务接口。** 首版继续截图上传；若实际审核量大、截图造假风险高或外部系统已有成熟 API，则优先财务、再图书馆。
+8. **评估财务与图书馆接口。** 首版继续截图上传。若后续审核量大或截图可信度不足，优先财务，再图书馆。
 
-9. **最后补齐运营治理能力。** 包括导入审计、差异报表、外部接口监控、数据更新时间展示、人工改派和人工审核日志。这些不是单个数据源，但决定数据对接上线后的可维护性。
+9. **补齐运营治理能力。** 包括导入审计、失败重试、差异报表、外部数据更新时间展示、人工改派、人工审核日志。
 
 ---
 
-## 结论
+## 七、建议修改数据对接文档的最小范围
+
+为了避免文档一次性扩得过大，建议先补充以下最小内容：
 
-学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据都应进入数据对接文档，其中班级-辅导员映射是最高风险缺口。首版不应追求所有系统 API 化；对约 1000 名学生和约 50 名辅导员，CSV/Excel 导入加严格校验更现实。管理员账号、图书馆、财务、独立学籍接口属于 P1 或后续增强，不应阻塞核心审批闭环上线。
+1. 新增“学生基本信息导入”章节，提供 CSV/Excel 模板字段。
+2. 新增“辅导员基本信息导入”章节，明确 `employee_id`、联系方式和账号状态。
+3. 新增“班级-辅导员对应关系导入”章节，列为 P0，并写明覆盖率和异常报告要求。
+4. 将“宿舍清退数据”保留为业务校验数据，并补充与人工证明降级的关系。
+5. 在附录中增加三份模板：学生基础数据、辅导员基础数据、班级-辅导员映射。
+
+---
+
+## 八、最终建议
+
+同意 `29-data-source-analysis.md` 对主要缺失数据源的识别，但建议将结论进一步收敛为：
+
+- **P0 数据：** 学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据、毕业资格字段。
+- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
+- **首版策略：** 账号和映射数据用 CSV/Excel 批量导入，宿舍清退优先 API，管理员手动维护，图书馆/财务继续截图上传。
+- **最高优先级行动：** 立即补充班级-辅导员映射的数据规范和导入校验，这是自动审批闭环的关键缺口。
+

codex
审查结果已经写入指定文件。我会再快速检查一遍文件内容和工作区状态，确认没有误改其他文档。
exec
/bin/bash -lc 'rtk git status --short docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
?? docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
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


diff --git a/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md b/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
index 1d05e91d83dcdc2502f89f0c53089a2ebe46ea67..aa0d6707f9ae91a17c3a66923547ae34c0185a41
--- a/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
+++ b/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
@@ -1,93 +1,166 @@
 # 数据源完整性审查与建议
 
 **审查时间：** 2026-05-27  
-**审查对象：** `29-data-source-analysis.md`、`docs/数据对接说明文档.md`、用户设计与系统设计相关要求  
+**审查对象：** `29-data-source-analysis.md`、`docs/数据对接说明文档.md`、用户设计说明书、系统设计文档  
+
+---
+
+## 一、总体结论
+
+`29-data-source-analysis.md` 的方向是正确的：当前数据对接文档只覆盖宿舍清退，无法完整支撑 student、counselor、admin 三类角色的账号初始化、权限边界和自动审批分配。
+
+需要调整的重点有两点：
+
+1. **班级-辅导员对应关系应明确列为 P0。** 这是自动分配审批人的核心数据。没有它，系统提交申请时无法稳定设置 `counselor_id` 和 `current_approver_id`，只能退化为人工逐个配置或人工改派。
+2. **首版不应追求所有数据源 API 化。** 对约 1000 名学生、约 50 名辅导员、约 5 名管理员的规模，CSV/Excel 批量导入加严格校验更现实；API 更适合作为后续自动化增强。
 
 ---
 
-## 1. Priority Classification
+## 二、优先级分类
 
-### P0：上线必须具备的数据
+### P0：上线必须具备
 
-| 数据源 | 优先级 | 判定 | 理由 |
-|--------|--------|------|------|
-| 学生基本信息 | P0 | 必须纳入数据对接文档 | `29-data-source-analysis.md` 第三章 3.1 已列为 P0，用途包括创建学生账号、身份验证、按班级分配审批人。用户设计说明书也明确“学号由学校统一导入”，因此它不是单纯便利项。技术上可用手工 Excel 导入替代 API，但数据源和字段规范必须写进对接文档。 |
-| 班级-辅导员对应关系 | P0 | 必须纳入数据对接文档 | `29-data-source-analysis.md` 第三章 3.4 和第七章 7.1 都指出缺失后系统无法自动分配审批人，需要手动配置约 1000 人/届。系统设计中的 `applications.counselor_id`、`current_approver_id` 也依赖该关系在提交时固化审批人。 |
-| 辅导员基本信息 | P0 | 必须具备，但实时 API 不是必须 | `29-data-source-analysis.md` 第三章 3.3 将其列为 P0，原因是创建辅导员账号和分配审批权限。约 50 人规模下，CSV/Excel 导入已经可满足上线；API 是运维优化，不是首版硬要求。 |
-| 宿舍清退数据 | P0 | 已覆盖，继续保持 P0 | 当前数据对接文档已覆盖宿舍系统。用户设计说明书将宿舍清退作为提交前自动验证项，同时保留手动上传证明作为降级方案。 |
-| 学籍/毕业资格 | P0 字段，P1 独立接口 | 应并入学生基本信息首批导入 | `29-data-source-analysis.md` 第四章 4.3 将学籍状态列为 P1，但其用途包含“限制只有毕业生可以提交离校申请”。如果学生基本信息只导入当届毕业生，则不需要独立实时接口；如果导入全校学生，则 `graduation_status` / `graduation_year` / `eligible_for_leave` 必须作为 P0 字段。独立学籍 API 可放到 P1。 |
+| 数据源 | 来源系统 | P0 判定 | 原因 |
+|--------|----------|---------|------|
+| 学生基本信息 | 教务系统 | P0 | 用于创建学生账号、身份识别、展示院系专业班级、限定毕业离校申请人范围。用户设计说明书已出现“学号、姓名、专业、班级”和“批量导入学生用户”的要求，因此必须写入数据对接文档。 |
+| 辅导员基本信息 | 人事系统或人工台账 | P0 | 用于创建 counselor 账号和审批权限主体。实时同步不是 P0，但账号数据本身是 P0。 |
+| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
+| 宿舍清退数据 | 宿管系统 | P0 | 当前业务把宿舍清退作为提交前校验项，现有对接文档已覆盖。即使保留人工证明降级，正式流程仍应具备自动校验或批量数据导入能力。 |
+| 毕业资格/离校资格字段 | 教务系统 | P0 字段，非 P0 独立接口 | 如果系统只导入当届毕业生，可通过导入范围满足；如果导入全量学生，则必须在学生基本信息中带 `graduation_year`、`graduation_status` 或 `eligible_for_leave`。不建议首版单独建设学籍 API。 |
 
-### P1：提升自动化或审核运营效率的数据
+### P1：可选增强
 
-| 数据源 | 优先级 | 判定 | 理由 |
-|--------|--------|------|------|
-| 学工部管理员信息 | P1 | 不建议做系统级数据对接 | `29-data-source-analysis.md` 第三章 3.5 和第六章均说明管理员约 5 人，可手动创建。这里是账号初始化问题，不是高频数据同步问题。 |
-| 图书馆清书状态 | P1 | 可选集成 | `29-data-source-analysis.md` 第四章 4.1 说明当前方案是上传清书证明截图。附件表也已有 `library_clearance` 类型，因此首版可运行；API 集成主要减少截图审核和伪造风险。 |
-| 财务结清状态 | P1 | 可选集成，优先级略高于图书馆 | `29-data-source-analysis.md` 第四章 4.2 说明当前方案是上传财务结清截图。考虑费用状态的业务敏感性，若财务系统已有稳定接口，可比图书馆更早做，但不应阻塞首版。 |
+| 数据源 | 来源系统 | P1 判定 | 原因 |
+|--------|----------|---------|------|
+| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
+| 图书馆清书状态 | 图书馆系统 | P1 | 当前已有上传截图的人工方案。接口集成能降低审核成本和伪造风险，但不应阻塞首版上线。 |
+| 财务结清状态 | 财务系统 | P1 | 当前已有上传截图的人工方案。由于财务状态更敏感，若后续接口条件成熟，优先级可高于图书馆，但仍不是首版 P0。 |
+| 独立学籍状态接口 | 教务系统 | P1 | 只有在多届学生并行、延期毕业、结业/退学实时变化等需求明确时，才需要独立 API。首版可并入学生基础数据。 |
 
 ---
 
-## 2. Integration Recommendations
+## 三、对接方式建议
 
-| 数据源 | 推荐方式 | 备选方式 | 建议字段/补充要求 |
-|--------|----------|----------|------------------|
-| 学生基本信息 | CSV/Excel 批量导入作为首版标准方案 | 教务系统 API | 首版按届导入约 1000 人，批量文件更容易落地。字段除分析文档列出的 `student_id`、`name`、`department`、`major`、`class_name`、`grade` 外，建议增加 `class_id`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
-| 班级-辅导员对应关系 | CSV/Excel 批量导入，必须有校验报告 | 教务系统 API | 这是 P0 数据，但不要求实时。建议以 `class_id + counselor_employee_id + effective_term` 为主键逻辑，避免只靠班级名称匹配。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无负责人的学生数。 |
-| 辅导员基本信息 | CSV/Excel 批量导入 | HR API | 约 50 人，首版 API 收益有限。字段包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API 同步。 |
-| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入 | 当前文档策略合理。申请提交时需要实时性，API 价值高；若宿管系统无法提供 API，则保留手动上传证明和文件导入。 |
-| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 约 5 人，不建议接 HR API。需要在文档中明确由系统管理员维护，并保留角色授权、停用、重置密码流程。 |
-| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 不作为首版阻塞项。若后续对接，建议只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，避免引入借阅明细等非必要个人数据。 |
-| 财务结清状态 | 首版手动上传截图 | API 优先于 CSV | 不作为首版阻塞项。若对接，应只返回结清布尔值和日期，不同步欠费明细；失败时保留人工审核通道。 |
-| 学籍/毕业资格 | 并入学生基本信息导入 | 教务系统 API | 不建议首版单独建接口。只有在系统长期服务多届、多状态学生，或需要实时处理延期毕业/结业/退学时，再做独立 API。 |
+| 数据源 | 推荐方式 | 备选方式 | 关键建议 |
+|--------|----------|----------|----------|
+| 学生基本信息 | CSV/Excel 批量导入 | 教务系统 API | 首版按毕业届别导入更容易落地。字段建议包括 `student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
+| 辅导员基本信息 | CSV/Excel 批量导入 | 人事系统 API 或手动创建 | 约 50 人规模下，批量导入足够。字段建议包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API。 |
+| 班级-辅导员对应关系 | CSV/Excel 批量导入并强校验 | 教务系统 API | 必须优先支持。建议用 `class_id + counselor_employee_id + effective_term` 表达关系，不要只靠 `class_name`。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无审批人的学生数。 |
+| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入、人工证明降级 | 当前文档策略合理。提交申请时实时性较强，API 价值高；若宿管系统暂不支持 API，则每日文件导入加人工证明降级。 |
+| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
+| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 后续对接时只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，不要引入借阅明细。 |
+| 财务结清状态 | 首版手动上传截图 | API 优先于 CSV | 后续对接时只返回是否结清和结清日期，不同步欠费明细；外部系统失败时保留人工审核通道。 |
+| 学籍/毕业资格 | 并入学生基本信息导入 | 教务系统 API | 首版不要单独拆接口。若后续存在延期毕业、结业、退学状态的实时变更，再建设独立同步。 |
 
 ---
 
-## 3. Missing Considerations
+## 四、对五个核心问题的直接回答
 
-1. **班级唯一标识不足。** 当前分析使用 `class_name`，但同名、改名、跨届复用都可能发生。对接文档应优先要求 `class_id`，`class_name` 仅用于展示。
+### 1. 学生基本信息是否需要写入数据对接文档？
 
-2. **账号生命周期未定义。** 需要明确新增、更新、停用、毕业后归档、辅导员离职/调岗后的处理规则。否则 CSV 导入只能新增，无法可靠处理人员变化。
+需要，且应列为 P0。
 
-3. **导入校验与人工修复流程缺失。** P0 数据不只需要字段格式，还需要“导入前校验、导入失败明细、重复数据处理、回滚/覆盖策略、导入审计日志”。
+原因不是“方便展示”，而是学生账号、身份识别、申请资格、班级映射都依赖它。当前数据对接文档的目标用户也应从“宿舍管理系统管理员”扩展为“教务系统、人事系统、宿管系统及业务数据负责人”。
 
-4. **审批人变更后的历史一致性。** 系统设计中申请会固化 `counselor_id`。应明确：已提交申请不随映射变更自动改审批人，除非管理员执行带审计的改派操作。
+### 2. 辅导员数据源如何对接？
 
-5. **多辅导员/代理审批场景。** 一个班级可能存在主辅导员、临时代办、请假代理。建议首版至少支持一个主负责人，并在后台预留手动改派能力。
+首版推荐 CSV/Excel 批量导入，不推荐一开始就要求人事系统 API。
 
-6. **组织架构与权限边界。** 学工部可看全校，辅导员只能看负责班级。除班级映射外，还需要院系、专业、年级等维度用于筛选、统计和异常排查。
+理由是辅导员规模约 50 人，变化频率低，API 改造投入可能高于收益。但数据结构必须标准化，尤其是 `employee_id` 要能被班级-辅导员映射引用。若学校已有成熟 HR API 或统一身份平台，可在后续升级为 API 同步。
 
-7. **数据最小化与敏感信息边界。** 不应为验证身份引入身份证号、欠费明细、借阅明细等高敏字段。此前共识中 `student_id + name` 已足够识别学生，应继续沿用最小字段集。
+### 3. 班级-辅导员对应关系是否应为 P0？
 
-8. **降级策略需要统一。** 宿舍、图书馆、财务都可能不可用。文档应区分“自动验证失败”“外部系统不可用”“学生确未完成清退/结清”，并定义人工审核入口。
+应为 P0，而且是当前缺口中风险最高的数据源。
 
-9. **毕业离校批次配置。** 计划离校日期范围、当前开放届别、申请开放/关闭时间不一定来自学生信息本身，可能需要系统配置或教务校历数据。
+它直接影响：
+
+- 学生提交时能否自动设置辅导员审批人；
+- 辅导员是否只能查看和审批负责班级；
+- 待办通知能否准确发送；
+- 审批统计能否按院系、班级、辅导员追踪。
+
+建议数据对接文档单独增加“审批关系数据”章节，并把导入覆盖率 100% 作为上线验收条件之一。
+
+### 4. 学工部管理员数据源是否需要对接？
+
+不建议做外部数据对接，手动创建即可。
+
+约 5 人的规模下，真正重要的是权限授予、停用、密码重置、操作审计，而不是与人事系统同步。文档应说明由系统管理员在后台维护，不应把它列为 P0 数据接口。
+
+### 5. 图书馆、财务、学籍是否需要对接？
+
+图书馆和财务可保持 P1。首版延续截图上传和人工审核，后续按审核量、造假风险、外部系统接口成熟度决定是否对接。若只能先选一个，建议先评估财务结清状态，因为财务数据的业务风险通常高于图书馆清书。
+
+学籍状态不建议作为首版独立接口，但毕业资格字段必须进入学生基础数据。换句话说，“是否允许提交离校申请”必须有数据依据，只是不一定需要实时 API。
+
+---
+
+## 五、遗漏或需补充考虑的数据项
+
+1. **班级唯一标识。** 当前分析偏向 `class_name`，但班级名称可能重复、改名或跨届复用。应要求 `class_id`，`class_name` 只用于展示。
+
+2. **组织架构数据。** 院系、专业、年级不仅用于展示，也用于权限过滤、统计导出、异常排查。首版可随学生和辅导员数据导入，不必单独做组织架构接口。
+
+3. **账号生命周期。** 需要定义新增、更新、停用、毕业归档、辅导员离职/调岗、管理员离岗后的处理规则。
+
+4. **导入校验和差异报告。** P0 数据导入不能只要求字段格式，还应要求失败明细、重复数据处理、覆盖策略、回滚策略和导入审计日志。
+
+5. **审批人变更后的历史一致性。** 已提交申请中的 `counselor_id` 应保持历史一致，不应因后续班级映射变更自动改写。若需改派，应由管理员显式操作并记录审计日志。
+
+6. **多辅导员和代理审批。** 现实中可能有主辅导员、代管辅导员、临时代理。首版可只要求一个主审批人，但后台应预留人工改派能力。
+
+7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
+
+8. **离校批次配置。** 开放申请时间、允许离校日期范围、毕业届别可能来自业务配置，而不一定来自教务系统。应作为系统配置纳入实施计划。
+
+9. **通知联系方式。** `phone`、`email` 对提醒和异常联系有价值；微信 `openid` 应通过用户绑定产生，不应从外部系统导入。
+
+10. **数据最小化。** 不应为了校验引入身份证号、欠费明细、借阅明细等高敏字段。业务校验只需要结论、日期、来源更新时间和必要的学生标识。
 
-10. **通知数据来源。** `phone`、`email` 对审批提醒和异常联系有价值；微信 `openid` 应通过用户绑定产生，不应从外部系统导入。
+11. **外部系统不可用时的降级口径。** 需要区分“学生确未完成”“外部系统失败”“系统数据过期”“人工证明待审核”，避免所有异常都被误判为不通过。
 
 ---
 
-## 4. Implementation Sequence
+## 六、建议实施顺序
 
-1. **先扩展数据对接文档范围。** 将文档标题和目标用户从“宿舍管理系统对接”扩展为“毕业离校系统数据对接”，拆分为账号基础数据、审批关系数据、业务校验数据三类。
+1. **重构数据对接说明文档目录。** 从单一“宿舍对接”扩展为“账号基础数据、审批关系数据、业务校验数据、降级与审计”四类。
 
-2. **实现学生基本信息导入。** 首版采用 CSV/Excel，支持新增和更新，要求导入当届毕业生或带 `eligible_for_leave` 字段。没有这一步，统一账号、身份验证和申请资格都不稳定。
+2. **定义学生基本信息导入模板。** 先支持 CSV/Excel 导入当届毕业生，包含毕业资格字段和班级唯一标识。
 
-3. **实现辅导员基本信息导入。** 先用 CSV/Excel 创建约 50 个辅导员账号，确保 `employee_id` 可被后续映射引用。
+3. **定义辅导员基本信息导入模板。** 先确保 counselor 账号存在，且 `employee_id` 可被映射数据引用。
 
-4. **实现班级-辅导员映射导入和覆盖率校验。** 这是审批自动分配的关键路径。上线前必须达到 100% 当届学生可解析到辅导员；异常学生应进入导入报告而不是运行时才暴露。
+4. **实现班级-辅导员映射导入。** 这是最关键步骤。上线前必须校验当届学生 100% 能解析到有效辅导员，否则不应开放提交。
 
-5. **保留并完善宿舍清退对接。** 当前文档已较完整，下一步重点是把它接入统一的外部校验/降级策略，而不是继续孤立成唯一数据源。
+5. **保留并完善宿舍清退对接。** 当前文档已较完整，下一步应把它纳入统一的校验结果、缓存、失败降级和审计机制。
 
-6. **手动创建学工部管理员账号。** 同时补充后台维护流程，包括新增、停用、密码重置、角色授权审计。
+6. **手动创建学工部管理员。** 同时补充管理员账号维护和终审人分配规则。
 
-7. **将学籍/毕业资格并入学生导入字段。** 先不要单独建设学籍 API；待多届并行、延期毕业等需求明确后，再升级为教务系统实时同步。
+7. **将毕业资格并入学生数据。** 首版不单独做学籍接口；后续根据延期毕业、多届并行等场景再升级。
 
-8. **按投入产出评估图书馆和财务接口。** 首版继续截图上传；若实际审核量大、截图造假风险高或外部系统已有成熟 API，则优先财务、再图书馆。
+8. **评估财务与图书馆接口。** 首版继续截图上传。若后续审核量大或截图可信度不足，优先财务，再图书馆。
 
-9. **最后补齐运营治理能力。** 包括导入审计、差异报表、外部接口监控、数据更新时间展示、人工改派和人工审核日志。这些不是单个数据源，但决定数据对接上线后的可维护性。
+9. **补齐运营治理能力。** 包括导入审计、失败重试、差异报表、外部数据更新时间展示、人工改派、人工审核日志。
 
 ---
 
-## 结论
+## 七、建议修改数据对接文档的最小范围
+
+为了避免文档一次性扩得过大，建议先补充以下最小内容：
 
-学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据都应进入数据对接文档，其中班级-辅导员映射是最高风险缺口。首版不应追求所有系统 API 化；对约 1000 名学生和约 50 名辅导员，CSV/Excel 导入加严格校验更现实。管理员账号、图书馆、财务、独立学籍接口属于 P1 或后续增强，不应阻塞核心审批闭环上线。
+1. 新增“学生基本信息导入”章节，提供 CSV/Excel 模板字段。
+2. 新增“辅导员基本信息导入”章节，明确 `employee_id`、联系方式和账号状态。
+3. 新增“班级-辅导员对应关系导入”章节，列为 P0，并写明覆盖率和异常报告要求。
+4. 将“宿舍清退数据”保留为业务校验数据，并补充与人工证明降级的关系。
+5. 在附录中增加三份模板：学生基础数据、辅导员基础数据、班级-辅导员映射。
+
+---
+
+## 八、最终建议
+
+同意 `29-data-source-analysis.md` 对主要缺失数据源的识别，但建议将结论进一步收敛为：
+
+- **P0 数据：** 学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据、毕业资格字段。
+- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
+- **首版策略：** 账号和映射数据用 CSV/Excel 批量导入，宿舍清退优先 API，管理员手动维护，图书馆/财务继续截图上传。
+- **最高优先级行动：** 立即补充班级-辅导员映射的数据规范和导入校验，这是自动审批闭环的关键缺口。
+

codex
已完成审查并保存到：

[30-codex-data-source-review.md](/home/caohui/projects/graduation-leave-system/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md)

核心结论：

- P0：学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据、毕业资格字段。
- P1：学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
- 首版建议：学生/辅导员/映射数据用 CSV/Excel 批量导入；宿舍清退优先 API；管理员手动维护；图书馆和财务继续截图上传。
- 最高风险缺口：班级-辅导员对应关系，应作为 P0 并要求上线前 100% 覆盖当届学生。
diff --git a/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md b/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
index 1d05e91d83dcdc2502f89f0c53089a2ebe46ea67..aa0d6707f9ae91a17c3a66923547ae34c0185a41
--- a/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
+++ b/docs/discussions/codex-review-2026-05-27/30-codex-data-source-review.md
@@ -1,93 +1,166 @@
 # 数据源完整性审查与建议
 
 **审查时间：** 2026-05-27  
-**审查对象：** `29-data-source-analysis.md`、`docs/数据对接说明文档.md`、用户设计与系统设计相关要求  
+**审查对象：** `29-data-source-analysis.md`、`docs/数据对接说明文档.md`、用户设计说明书、系统设计文档  
+
+---
+
+## 一、总体结论
+
+`29-data-source-analysis.md` 的方向是正确的：当前数据对接文档只覆盖宿舍清退，无法完整支撑 student、counselor、admin 三类角色的账号初始化、权限边界和自动审批分配。
+
+需要调整的重点有两点：
+
+1. **班级-辅导员对应关系应明确列为 P0。** 这是自动分配审批人的核心数据。没有它，系统提交申请时无法稳定设置 `counselor_id` 和 `current_approver_id`，只能退化为人工逐个配置或人工改派。
+2. **首版不应追求所有数据源 API 化。** 对约 1000 名学生、约 50 名辅导员、约 5 名管理员的规模，CSV/Excel 批量导入加严格校验更现实；API 更适合作为后续自动化增强。
 
 ---
 
-## 1. Priority Classification
+## 二、优先级分类
 
-### P0：上线必须具备的数据
+### P0：上线必须具备
 
-| 数据源 | 优先级 | 判定 | 理由 |
-|--------|--------|------|------|
-| 学生基本信息 | P0 | 必须纳入数据对接文档 | `29-data-source-analysis.md` 第三章 3.1 已列为 P0，用途包括创建学生账号、身份验证、按班级分配审批人。用户设计说明书也明确“学号由学校统一导入”，因此它不是单纯便利项。技术上可用手工 Excel 导入替代 API，但数据源和字段规范必须写进对接文档。 |
-| 班级-辅导员对应关系 | P0 | 必须纳入数据对接文档 | `29-data-source-analysis.md` 第三章 3.4 和第七章 7.1 都指出缺失后系统无法自动分配审批人，需要手动配置约 1000 人/届。系统设计中的 `applications.counselor_id`、`current_approver_id` 也依赖该关系在提交时固化审批人。 |
-| 辅导员基本信息 | P0 | 必须具备，但实时 API 不是必须 | `29-data-source-analysis.md` 第三章 3.3 将其列为 P0，原因是创建辅导员账号和分配审批权限。约 50 人规模下，CSV/Excel 导入已经可满足上线；API 是运维优化，不是首版硬要求。 |
-| 宿舍清退数据 | P0 | 已覆盖，继续保持 P0 | 当前数据对接文档已覆盖宿舍系统。用户设计说明书将宿舍清退作为提交前自动验证项，同时保留手动上传证明作为降级方案。 |
-| 学籍/毕业资格 | P0 字段，P1 独立接口 | 应并入学生基本信息首批导入 | `29-data-source-analysis.md` 第四章 4.3 将学籍状态列为 P1，但其用途包含“限制只有毕业生可以提交离校申请”。如果学生基本信息只导入当届毕业生，则不需要独立实时接口；如果导入全校学生，则 `graduation_status` / `graduation_year` / `eligible_for_leave` 必须作为 P0 字段。独立学籍 API 可放到 P1。 |
+| 数据源 | 来源系统 | P0 判定 | 原因 |
+|--------|----------|---------|------|
+| 学生基本信息 | 教务系统 | P0 | 用于创建学生账号、身份识别、展示院系专业班级、限定毕业离校申请人范围。用户设计说明书已出现“学号、姓名、专业、班级”和“批量导入学生用户”的要求，因此必须写入数据对接文档。 |
+| 辅导员基本信息 | 人事系统或人工台账 | P0 | 用于创建 counselor 账号和审批权限主体。实时同步不是 P0，但账号数据本身是 P0。 |
+| 班级-辅导员对应关系 | 教务系统或学工台账 | P0 | 用于提交申请时自动分配一级审批人，也是辅导员“只能查看负责班级学生”的权限边界。没有该关系会造成约 1000 名学生/年的手动配置成本。 |
+| 宿舍清退数据 | 宿管系统 | P0 | 当前业务把宿舍清退作为提交前校验项，现有对接文档已覆盖。即使保留人工证明降级，正式流程仍应具备自动校验或批量数据导入能力。 |
+| 毕业资格/离校资格字段 | 教务系统 | P0 字段，非 P0 独立接口 | 如果系统只导入当届毕业生，可通过导入范围满足；如果导入全量学生，则必须在学生基本信息中带 `graduation_year`、`graduation_status` 或 `eligible_for_leave`。不建议首版单独建设学籍 API。 |
 
-### P1：提升自动化或审核运营效率的数据
+### P1：可选增强
 
-| 数据源 | 优先级 | 判定 | 理由 |
-|--------|--------|------|------|
-| 学工部管理员信息 | P1 | 不建议做系统级数据对接 | `29-data-source-analysis.md` 第三章 3.5 和第六章均说明管理员约 5 人，可手动创建。这里是账号初始化问题，不是高频数据同步问题。 |
-| 图书馆清书状态 | P1 | 可选集成 | `29-data-source-analysis.md` 第四章 4.1 说明当前方案是上传清书证明截图。附件表也已有 `library_clearance` 类型，因此首版可运行；API 集成主要减少截图审核和伪造风险。 |
-| 财务结清状态 | P1 | 可选集成，优先级略高于图书馆 | `29-data-source-analysis.md` 第四章 4.2 说明当前方案是上传财务结清截图。考虑费用状态的业务敏感性，若财务系统已有稳定接口，可比图书馆更早做，但不应阻塞首版。 |
+| 数据源 | 来源系统 | P1 判定 | 原因 |
+|--------|----------|---------|------|
+| 学工部管理员信息 | 人事系统 | P1 | 仅约 5 人，手动创建和维护成本低。需要文档说明维护流程，但不需要系统级数据对接。 |
+| 图书馆清书状态 | 图书馆系统 | P1 | 当前已有上传截图的人工方案。接口集成能降低审核成本和伪造风险，但不应阻塞首版上线。 |
+| 财务结清状态 | 财务系统 | P1 | 当前已有上传截图的人工方案。由于财务状态更敏感，若后续接口条件成熟，优先级可高于图书馆，但仍不是首版 P0。 |
+| 独立学籍状态接口 | 教务系统 | P1 | 只有在多届学生并行、延期毕业、结业/退学实时变化等需求明确时，才需要独立 API。首版可并入学生基础数据。 |
 
 ---
 
-## 2. Integration Recommendations
+## 三、对接方式建议
 
-| 数据源 | 推荐方式 | 备选方式 | 建议字段/补充要求 |
-|--------|----------|----------|------------------|
-| 学生基本信息 | CSV/Excel 批量导入作为首版标准方案 | 教务系统 API | 首版按届导入约 1000 人，批量文件更容易落地。字段除分析文档列出的 `student_id`、`name`、`department`、`major`、`class_name`、`grade` 外，建议增加 `class_id`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
-| 班级-辅导员对应关系 | CSV/Excel 批量导入，必须有校验报告 | 教务系统 API | 这是 P0 数据，但不要求实时。建议以 `class_id + counselor_employee_id + effective_term` 为主键逻辑，避免只靠班级名称匹配。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无负责人的学生数。 |
-| 辅导员基本信息 | CSV/Excel 批量导入 | HR API | 约 50 人，首版 API 收益有限。字段包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API 同步。 |
-| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入 | 当前文档策略合理。申请提交时需要实时性，API 价值高；若宿管系统无法提供 API，则保留手动上传证明和文件导入。 |
-| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 约 5 人，不建议接 HR API。需要在文档中明确由系统管理员维护，并保留角色授权、停用、重置密码流程。 |
-| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 不作为首版阻塞项。若后续对接，建议只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，避免引入借阅明细等非必要个人数据。 |
-| 财务结清状态 | 首版手动上传截图 | API 优先于 CSV | 不作为首版阻塞项。若对接，应只返回结清布尔值和日期，不同步欠费明细；失败时保留人工审核通道。 |
-| 学籍/毕业资格 | 并入学生基本信息导入 | 教务系统 API | 不建议首版单独建接口。只有在系统长期服务多届、多状态学生，或需要实时处理延期毕业/结业/退学时，再做独立 API。 |
+| 数据源 | 推荐方式 | 备选方式 | 关键建议 |
+|--------|----------|----------|----------|
+| 学生基本信息 | CSV/Excel 批量导入 | 教务系统 API | 首版按毕业届别导入更容易落地。字段建议包括 `student_id`、`name`、`department`、`major`、`class_id`、`class_name`、`grade`、`graduation_year`、`eligible_for_leave`、`is_active`。`phone`、`email` 可选。 |
+| 辅导员基本信息 | CSV/Excel 批量导入 | 人事系统 API 或手动创建 | 约 50 人规模下，批量导入足够。字段建议包括 `employee_id`、`name`、`phone`、`email`、`department`、`is_active`、`role=counselor`。如果学校已有统一身份认证或 HR API，再升级为 API。 |
+| 班级-辅导员对应关系 | CSV/Excel 批量导入并强校验 | 教务系统 API | 必须优先支持。建议用 `class_id + counselor_employee_id + effective_term` 表达关系，不要只靠 `class_name`。导入后必须输出未匹配班级、未匹配辅导员、重复映射、无审批人的学生数。 |
+| 宿舍清退数据 | API 优先 | 每日 CSV/Excel 导入、人工证明降级 | 当前文档策略合理。提交申请时实时性较强，API 价值高；若宿管系统暂不支持 API，则每日文件导入加人工证明降级。 |
+| 学工部管理员信息 | 手动创建 | CSV/Excel 导入 | 不建议接 HR API。文档中应说明创建、停用、重置密码、角色授权和审计要求。 |
+| 图书馆清书状态 | 首版手动上传截图 | API 或定期 CSV | 后续对接时只同步 `student_id`、`is_cleared`、`clear_date`、`source_updated_at`，不要引入借阅明细。 |
+| 财务结清状态 | 首版手动上传截图 | API 优先于 CSV | 后续对接时只返回是否结清和结清日期，不同步欠费明细；外部系统失败时保留人工审核通道。 |
+| 学籍/毕业资格 | 并入学生基本信息导入 | 教务系统 API | 首版不要单独拆接口。若后续存在延期毕业、结业、退学状态的实时变更，再建设独立同步。 |
 
 ---
 
-## 3. Missing Considerations
+## 四、对五个核心问题的直接回答
 
-1. **班级唯一标识不足。** 当前分析使用 `class_name`，但同名、改名、跨届复用都可能发生。对接文档应优先要求 `class_id`，`class_name` 仅用于展示。
+### 1. 学生基本信息是否需要写入数据对接文档？
 
-2. **账号生命周期未定义。** 需要明确新增、更新、停用、毕业后归档、辅导员离职/调岗后的处理规则。否则 CSV 导入只能新增，无法可靠处理人员变化。
+需要，且应列为 P0。
 
-3. **导入校验与人工修复流程缺失。** P0 数据不只需要字段格式，还需要“导入前校验、导入失败明细、重复数据处理、回滚/覆盖策略、导入审计日志”。
+原因不是“方便展示”，而是学生账号、身份识别、申请资格、班级映射都依赖它。当前数据对接文档的目标用户也应从“宿舍管理系统管理员”扩展为“教务系统、人事系统、宿管系统及业务数据负责人”。
 
-4. **审批人变更后的历史一致性。** 系统设计中申请会固化 `counselor_id`。应明确：已提交申请不随映射变更自动改审批人，除非管理员执行带审计的改派操作。
+### 2. 辅导员数据源如何对接？
 
-5. **多辅导员/代理审批场景。** 一个班级可能存在主辅导员、临时代办、请假代理。建议首版至少支持一个主负责人，并在后台预留手动改派能力。
+首版推荐 CSV/Excel 批量导入，不推荐一开始就要求人事系统 API。
 
-6. **组织架构与权限边界。** 学工部可看全校，辅导员只能看负责班级。除班级映射外，还需要院系、专业、年级等维度用于筛选、统计和异常排查。
+理由是辅导员规模约 50 人，变化频率低，API 改造投入可能高于收益。但数据结构必须标准化，尤其是 `employee_id` 要能被班级-辅导员映射引用。若学校已有成熟 HR API 或统一身份平台，可在后续升级为 API 同步。
 
-7. **数据最小化与敏感信息边界。** 不应为验证身份引入身份证号、欠费明细、借阅明细等高敏字段。此前共识中 `student_id + name` 已足够识别学生，应继续沿用最小字段集。
+### 3. 班级-辅导员对应关系是否应为 P0？
 
-8. **降级策略需要统一。** 宿舍、图书馆、财务都可能不可用。文档应区分“自动验证失败”“外部系统不可用”“学生确未完成清退/结清”，并定义人工审核入口。
+应为 P0，而且是当前缺口中风险最高的数据源。
 
-9. **毕业离校批次配置。** 计划离校日期范围、当前开放届别、申请开放/关闭时间不一定来自学生信息本身，可能需要系统配置或教务校历数据。
+它直接影响：
+
+- 学生提交时能否自动设置辅导员审批人；
+- 辅导员是否只能查看和审批负责班级；
+- 待办通知能否准确发送；
+- 审批统计能否按院系、班级、辅导员追踪。
+
+建议数据对接文档单独增加“审批关系数据”章节，并把导入覆盖率 100% 作为上线验收条件之一。
+
+### 4. 学工部管理员数据源是否需要对接？
+
+不建议做外部数据对接，手动创建即可。
+
+约 5 人的规模下，真正重要的是权限授予、停用、密码重置、操作审计，而不是与人事系统同步。文档应说明由系统管理员在后台维护，不应把它列为 P0 数据接口。
+
+### 5. 图书馆、财务、学籍是否需要对接？
+
+图书馆和财务可保持 P1。首版延续截图上传和人工审核，后续按审核量、造假风险、外部系统接口成熟度决定是否对接。若只能先选一个，建议先评估财务结清状态，因为财务数据的业务风险通常高于图书馆清书。
+
+学籍状态不建议作为首版独立接口，但毕业资格字段必须进入学生基础数据。换句话说，“是否允许提交离校申请”必须有数据依据，只是不一定需要实时 API。
+
+---
+
+## 五、遗漏或需补充考虑的数据项
+
+1. **班级唯一标识。** 当前分析偏向 `class_name`，但班级名称可能重复、改名或跨届复用。应要求 `class_id`，`class_name` 只用于展示。
+
+2. **组织架构数据。** 院系、专业、年级不仅用于展示，也用于权限过滤、统计导出、异常排查。首版可随学生和辅导员数据导入，不必单独做组织架构接口。
+
+3. **账号生命周期。** 需要定义新增、更新、停用、毕业归档、辅导员离职/调岗、管理员离岗后的处理规则。
+
+4. **导入校验和差异报告。** P0 数据导入不能只要求字段格式，还应要求失败明细、重复数据处理、覆盖策略、回滚策略和导入审计日志。
+
+5. **审批人变更后的历史一致性。** 已提交申请中的 `counselor_id` 应保持历史一致，不应因后续班级映射变更自动改写。若需改派，应由管理员显式操作并记录审计日志。
+
+6. **多辅导员和代理审批。** 现实中可能有主辅导员、代管辅导员、临时代理。首版可只要求一个主审批人，但后台应预留人工改派能力。
+
+7. **学工部默认终审人或终审组。** 系统设计中申请会设置 `admin_id`。如果不是固定 1 人终审，应明确是固定负责人、轮值管理员，还是管理员池抢单/分配。
+
+8. **离校批次配置。** 开放申请时间、允许离校日期范围、毕业届别可能来自业务配置，而不一定来自教务系统。应作为系统配置纳入实施计划。
+
+9. **通知联系方式。** `phone`、`email` 对提醒和异常联系有价值；微信 `openid` 应通过用户绑定产生，不应从外部系统导入。
+
+10. **数据最小化。** 不应为了校验引入身份证号、欠费明细、借阅明细等高敏字段。业务校验只需要结论、日期、来源更新时间和必要的学生标识。
 
-10. **通知数据来源。** `phone`、`email` 对审批提醒和异常联系有价值；微信 `openid` 应通过用户绑定产生，不应从外部系统导入。
+11. **外部系统不可用时的降级口径。** 需要区分“学生确未完成”“外部系统失败”“系统数据过期”“人工证明待审核”，避免所有异常都被误判为不通过。
 
 ---
 
-## 4. Implementation Sequence
+## 六、建议实施顺序
 
-1. **先扩展数据对接文档范围。** 将文档标题和目标用户从“宿舍管理系统对接”扩展为“毕业离校系统数据对接”，拆分为账号基础数据、审批关系数据、业务校验数据三类。
+1. **重构数据对接说明文档目录。** 从单一“宿舍对接”扩展为“账号基础数据、审批关系数据、业务校验数据、降级与审计”四类。
 
-2. **实现学生基本信息导入。** 首版采用 CSV/Excel，支持新增和更新，要求导入当届毕业生或带 `eligible_for_leave` 字段。没有这一步，统一账号、身份验证和申请资格都不稳定。
+2. **定义学生基本信息导入模板。** 先支持 CSV/Excel 导入当届毕业生，包含毕业资格字段和班级唯一标识。
 
-3. **实现辅导员基本信息导入。** 先用 CSV/Excel 创建约 50 个辅导员账号，确保 `employee_id` 可被后续映射引用。
+3. **定义辅导员基本信息导入模板。** 先确保 counselor 账号存在，且 `employee_id` 可被映射数据引用。
 
-4. **实现班级-辅导员映射导入和覆盖率校验。** 这是审批自动分配的关键路径。上线前必须达到 100% 当届学生可解析到辅导员；异常学生应进入导入报告而不是运行时才暴露。
+4. **实现班级-辅导员映射导入。** 这是最关键步骤。上线前必须校验当届学生 100% 能解析到有效辅导员，否则不应开放提交。
 
-5. **保留并完善宿舍清退对接。** 当前文档已较完整，下一步重点是把它接入统一的外部校验/降级策略，而不是继续孤立成唯一数据源。
+5. **保留并完善宿舍清退对接。** 当前文档已较完整，下一步应把它纳入统一的校验结果、缓存、失败降级和审计机制。
 
-6. **手动创建学工部管理员账号。** 同时补充后台维护流程，包括新增、停用、密码重置、角色授权审计。
+6. **手动创建学工部管理员。** 同时补充管理员账号维护和终审人分配规则。
 
-7. **将学籍/毕业资格并入学生导入字段。** 先不要单独建设学籍 API；待多届并行、延期毕业等需求明确后，再升级为教务系统实时同步。
+7. **将毕业资格并入学生数据。** 首版不单独做学籍接口；后续根据延期毕业、多届并行等场景再升级。
 
-8. **按投入产出评估图书馆和财务接口。** 首版继续截图上传；若实际审核量大、截图造假风险高或外部系统已有成熟 API，则优先财务、再图书馆。
+8. **评估财务与图书馆接口。** 首版继续截图上传。若后续审核量大或截图可信度不足，优先财务，再图书馆。
 
-9. **最后补齐运营治理能力。** 包括导入审计、差异报表、外部接口监控、数据更新时间展示、人工改派和人工审核日志。这些不是单个数据源，但决定数据对接上线后的可维护性。
+9. **补齐运营治理能力。** 包括导入审计、失败重试、差异报表、外部数据更新时间展示、人工改派、人工审核日志。
 
 ---
 
-## 结论
+## 七、建议修改数据对接文档的最小范围
+
+为了避免文档一次性扩得过大，建议先补充以下最小内容：
 
-学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据都应进入数据对接文档，其中班级-辅导员映射是最高风险缺口。首版不应追求所有系统 API 化；对约 1000 名学生和约 50 名辅导员，CSV/Excel 导入加严格校验更现实。管理员账号、图书馆、财务、独立学籍接口属于 P1 或后续增强，不应阻塞核心审批闭环上线。
+1. 新增“学生基本信息导入”章节，提供 CSV/Excel 模板字段。
+2. 新增“辅导员基本信息导入”章节，明确 `employee_id`、联系方式和账号状态。
+3. 新增“班级-辅导员对应关系导入”章节，列为 P0，并写明覆盖率和异常报告要求。
+4. 将“宿舍清退数据”保留为业务校验数据，并补充与人工证明降级的关系。
+5. 在附录中增加三份模板：学生基础数据、辅导员基础数据、班级-辅导员映射。
+
+---
+
+## 八、最终建议
+
+同意 `29-data-source-analysis.md` 对主要缺失数据源的识别，但建议将结论进一步收敛为：
+
+- **P0 数据：** 学生基本信息、辅导员基本信息、班级-辅导员映射、宿舍清退数据、毕业资格字段。
+- **P1 数据：** 学工部管理员外部同步、图书馆清书状态、财务结清状态、独立学籍 API。
+- **首版策略：** 账号和映射数据用 CSV/Excel 批量导入，宿舍清退优先 API，管理员手动维护，图书馆/财务继续截图上传。
+- **最高优先级行动：** 立即补充班级-辅导员映射的数据规范和导入校验，这是自动审批闭环的关键缺口。
+

tokens used
73,353

```

## Concise summary

Provider completed successfully. Review the raw output for details.

## Action items

- Review the response and extract decisions you want to apply.
- Capture follow-up implementation tasks if needed.
