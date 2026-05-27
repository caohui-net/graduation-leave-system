# 数据源需求共识文档

**文档版本：** v2.0  
**创建时间：** 2026-05-27  
**修订时间：** 2026-05-27  
**目的：** 明确毕业离校系统所需的数据源，提交给宿管系统方反馈

---

## 版本变更说明（v1 → v2）

**主要修正：**

1. **CSV导入策略**：从"全量覆盖"改为"staging表 + upsert + 软停用"
2. **数据库模型调整**：
   - users表：`student_id`改为可空，新增`employee_id`和`class_id`字段
   - 新增`class_counselor_mapping`表（班级-辅导员映射）
   - 新增`graduation_batches`表（批次配置）
   - 新增`import_logs`表（导入审计）
   - 拆分staging表：`students_staging`、`counselors_staging`、`class_mapping_staging`
3. **认证约束调整**：增加`password_setup_required`支持CSV预导入账号
4. **对接方式调整**：学生/辅导员/班级映射改为"CSV/Excel首版优先"
5. **约束增强**：学生必须有`class_id`，复用`system_configs`表

**修正依据：**
- Codex第二轮审查（34-codex-second-review-response.md）
- Codex关键问题审查（35-response-to-codex-critical-issues.md）

---

## 一、数据源概述

本系统需要以下数据源支持系统运行：

| 数据源 | 优先级 | 用途 | 对接方式 |
|--------|--------|------|----------|
| 学生基本信息 | P0 | 创建学生账号、身份识别、班级映射 | **CSV/Excel首版优先** / API或DB增强 |
| 宿舍清退数据 | P0 | 验证学生是否完成宿舍清退 | API优先 / DB备选 / CSV降级 |
| 辅导员基本信息 | P0 | 创建辅导员账号、审批权限 | **CSV/Excel首版优先** / 人事或统一身份API增强 |
| 班级-辅导员对应关系 | P0 | 自动分配审批人 | **CSV/Excel首版优先并强校验** / 教务或学工API增强 |
| 学工部管理员信息 | P1 | 创建管理员账号 | 手动创建（~5人） |

**对接方式说明：**
- **CSV/Excel首版优先**：首版采用CSV/Excel批量导入，快速上线，后续根据数据变更频率决定是否升级为API/DB
- **API优先**：调用宿管系统提供的API接口（实时校验场景）
- **DB备选**：直接读取宿管系统数据库（需要安全审批和网络配置）
- **CSV降级**：当无法提供API或DB时，通过CSV文件导入

**首版策略调整理由：**
1. **实施周期**：CSV/Excel导入最快，DB直连需要安全审批和网络配置
2. **变更频率**：账号数据变更频率低（学期级），不需要实时同步
3. **风险控制**：CSV导入可以先验证、再导入、可回滚；DB直连风险更高

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
| 学号 | student_id | 文本 | 是 | 学生唯一标识 | 2022001 |
| 姓名 | name | 文本 | 是 | 学生姓名 | 张三 |
| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
| 专业 | major | 文本 | 是 | 所属专业 | 计算机科学与技术 |
| 班级ID | class_id | 文本 | 是 | 班级唯一标识（核心键） | CS2022-01 |
| 班级名称 | class_name | 文本 | 否 | 班级名称（用于展示） | 计算机科学与技术2022级1班 |
| 年级 | grade | 整数 | 是 | 入学年份 | 2022 |
| 毕业年份 | graduation_year | 整数 | 是 | 预计毕业年份 | 2026 |
| 是否毕业生 | is_graduating | 布尔 | 是 | 是否为当届毕业生 | true |

**可选字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 说明 | 示例 |
|---------------|---------------|----------|------|------|
| 手机号 | phone | 文本 | 用于找回密码或二次验证 | 13800138000 |
| 邮箱 | email | 文本 | 用于通知或找回密码 | zhangsan@example.com |

**字段说明：**
- `class_id`：班级唯一标识，全校唯一，用于映射辅导员（**v2新增必填要求**）
- `class_name`：班级显示名称，可能重复、变更或跨届复用，仅用于展示
- `is_graduating`：标识是否为当届毕业生，`true`表示具备本批次离校申请资格
- `graduation_year`：示例统一为2026（与当前项目日期保持一致）

**CSV模板示例：**

```csv
student_id,name,department,major,class_id,class_name,grade,graduation_year,is_graduating,phone,email
2022001,张三,计算机学院,计算机科学与技术,CS2022-01,计算机科学与技术2022级1班,2022,2026,true,13800138000,zhangsan@example.com
2022002,李四,计算机学院,软件工程,SE2022-01,软件工程2022级1班,2022,2026,true,13800138001,lisi@example.com
```

**数据范围：**
- 只导入当届毕业生（`is_graduating=true` 且 `graduation_year=2026`）
- 约1000人/届

---

### 2.2 宿舍清退数据

**用途：**
- 验证学生是否完成宿舍清退（提交申请前置条件）
- 展示清退状态和完成时间

**必需字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 学号 | student_id | 文本 | 是 | 学生学号 | 2022001 |
| 姓名 | name | 文本 | 是 | 学生姓名（用于二次验证） | 张三 |
| 清退状态 | checkout_status | 枚举 | **是** | 清退状态（**v2改为必填**） | completed |
| 清退完成时间 | checkout_date | 日期时间 | 条件必填 | 当status=completed时必填 | 2026-05-20 14:30:00 |
| 数据更新时间 | source_updated_at | 日期时间 | 建议 | 外部系统数据更新时间（**v2新增**） | 2026-05-20 15:00:00 |

**枚举值说明（v2修订）：**
- `completed`：已完成清退
- `pending`：清退中（已申请但未完成）
- `not_started`：未开始清退
- `unknown`：查询失败或数据不可用（用于API异常时的降级）

**API响应示例：**

```json
{
  "student_id": "2022001",
  "name": "张三",
  "checkout_status": "completed",
  "checkout_date": "2026-05-20T14:30:00",
  "source_updated_at": "2026-05-20T15:00:00"
}
```

**降级处理：**
- API查询失败时，返回 `checkout_status: "unknown"`
- 系统允许学生提交申请，但需上传宿舍清退证明截图

---

### 2.3 辅导员基本信息

**用途：**
- 创建辅导员账号（用于登录系统）
- 审批权限管理
- 班级-辅导员映射

**必需字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 工号 | employee_id | 文本 | 是 | 辅导员唯一标识（**v2新增**） | T2022001 |
| 姓名 | name | 文本 | 是 | 辅导员姓名 | 王老师 |
| 院系 | department | 文本 | 是 | 所属院系 | 计算机学院 |
| 手机号 | phone | 文本 | 否 | 联系电话 | 13900139000 |
| 邮箱 | email | 文本 | 否 | 联系邮箱 | wanglaoshi@example.com |
| 是否在职 | is_active | 布尔 | 是 | 是否在职（**v2新增**） | true |

**字段说明：**
- `employee_id`：辅导员工号，必须全校唯一，与统一身份认证、人事系统工号一致
- `is_active`：标识是否在职，`false`时不能登录、不能审批，但历史记录可查询

**CSV模板示例：**

```csv
employee_id,name,department,phone,email,is_active
T2022001,王老师,计算机学院,13900139000,wanglaoshi@example.com,true
T2022002,李老师,软件学院,13900139001,lililaoshi@example.com,true
```

**数据范围：**
- 当前在职辅导员
- 约50人

**停用规则（v2新增）：**

| 账号状态 | 登录 | 创建申请 | 审批 | 查看历史 | 接收通知 |
|---------|------|---------|------|---------|---------|
| `is_active=true` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `is_active=false` | ❌ | ❌ | ❌ | ✅（仅自己的） | ❌ |

---

### 2.4 班级-辅导员对应关系

**用途：**
- 学生提交申请时自动分配辅导员审批人
- 支持辅导员变更和历史追溯

**必需字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 班级ID | class_id | 文本 | 是 | 班级唯一标识 | CS2022-01 |
| 班级名称 | class_name | 文本 | 否 | 班级名称（用于展示） | 计算机科学与技术2022级1班 |
| 辅导员工号 | counselor_employee_id | 文本 | 是 | 辅导员工号 | T2022001 |

**可选字段（v2新增）：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 说明 | 示例 |
|---------------|---------------|----------|------|------|
| 生效日期 | effective_from | 日期 | 映射生效日期 | 2026-01-01 |
| 失效日期 | effective_until | 日期 | 映射失效日期，NULL表示长期有效 | NULL |
| 毕业批次ID | graduation_batch_id | 整数 | 关联毕业批次 | 1 |

**字段说明：**
- `class_id`：班级唯一标识，必须全校唯一，不能重复、变更或跨届复用
- `counselor_employee_id`：必须在辅导员表中存在且 `is_active=true`
- 首版只支持一班一主辅导员，同一 `class_id` 不能出现多次

**CSV模板示例：**

```csv
class_id,class_name,counselor_employee_id
CS2022-01,计算机科学与技术2022级1班,T2022001
SE2022-01,软件工程2022级1班,T2022002
```

**校验要求：**
- 学生表中的 `class_id` 必须在班级映射表中存在
- 班级映射表中的 `counselor_employee_id` 必须在辅导员表中存在
- 导入后输出校验报告：未匹配班级、未匹配辅导员、重复映射、无审批人的学生数

**历史一致性规则（v2新增）：**
- 已提交申请的 `counselor_id` 不自动改写，保持历史一致性
- 新提交申请使用新映射
- 如需改派，由管理员显式操作并记录审计日志

---

### 2.5 学工部管理员信息

**用途：**
- 创建管理员账号（终审权限）
- 系统配置和管理

**必需字段：**

| 字段名（中文） | 字段名（英文） | 数据类型 | 必填 | 说明 | 示例 |
|---------------|---------------|----------|------|------|------|
| 工号 | employee_id | 文本 | 是 | 管理员唯一标识 | A2022001 |
| 姓名 | name | 文本 | 是 | 管理员姓名 | 赵主任 |
| 部门 | department | 文本 | 是 | 所属部门 | 学工部 |
| 手机号 | phone | 文本 | 否 | 联系电话 | 13700137000 |
| 邮箱 | email | 文本 | 否 | 联系邮箱 | zhaozr@example.com |

**数据范围：**
- 约5人
- 首版采用手动创建，不参与批量导入

**默认终审人配置（v2新增）：**
- 系统配置表（`system_configs`）存储默认终审人列表
- 配置项：`default_admin_ids`（如 `3,5,7`）
- 分配模式：`admin_assignment_mode`（fixed/round_robin/load_balance）
- 首版采用固定分配（fixed），使用第一个可用管理员

---

## 三、数据对接方式详细说明

### 3.1 CSV/Excel导入（首版推荐）

**适用场景：**
- 学生基本信息
- 辅导员基本信息
- 班级-辅导员对应关系

**技术要求：**

**文件格式：**
- 编码：UTF-8（避免中文乱码）
- 格式：CSV或Excel（.xlsx）
- 大小限制：单文件不超过10MB
- 行数限制：单文件不超过10000行

**导入策略（v2修订）：**

采用**staging表 + upsert + 软停用**模式：

1. CSV导入到临时staging表（按类型拆分）
2. 存在则更新，不存在则插入（upsert）
3. 本次未导入的账号标记为 `is_active=false`
4. 下次导入重新出现时自动激活

**Staging表设计（v2新增）：**

```sql
-- 学生导入staging表
CREATE TABLE students_staging (
    student_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    major VARCHAR(100),
    class_id VARCHAR(50),
    class_name VARCHAR(100),
    grade INT,
    graduation_year INT,
    is_graduating BOOLEAN,
    phone VARCHAR(20),
    email VARCHAR(100)
);

-- 辅导员导入staging表
CREATE TABLE counselors_staging (
    employee_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100)
);

-- 班级映射导入staging表
CREATE TABLE class_mapping_staging (
    class_id VARCHAR(50) PRIMARY KEY,
    counselor_employee_id VARCHAR(50) NOT NULL
);
```

**导入流程：**

```sql
-- 1. 清空staging表
TRUNCATE students_staging;

-- 2. 导入CSV到staging表
LOAD DATA INFILE 'students.csv' INTO TABLE students_staging;

-- 3. Upsert到users表
INSERT INTO users (student_id, name, department, class_id, role, is_active, password_setup_required, ...)
SELECT student_id, name, department, class_id, 'student', true, true, ...
FROM students_staging
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    department = VALUES(department),
    class_id = VALUES(class_id),
    is_active = true,
    updated_at = NOW();

-- 4. 软停用：本次未导入的学生（使用NOT EXISTS避免NULL问题）
UPDATE users u
SET is_active = false, updated_at = NOW()
WHERE u.role = 'student'
  AND NOT EXISTS (
      SELECT 1 FROM students_staging s
      WHERE s.student_id = u.student_id
  );
```

**校验要求：**
- 必填字段非空校验
- 学号/工号唯一性校验
- 班级ID存在性校验
- 辅导员工号存在性校验
- 重复数据校验

**导入审计（v2新增）：**

```sql
CREATE TABLE import_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    import_type ENUM('student', 'counselor', 'class_mapping') NOT NULL,
    file_name VARCHAR(255),
    file_hash VARCHAR(64),                      -- SHA256
    uploaded_by INT,                            -- 操作人user_id
    total_rows INT,
    success_rows INT,
    failed_rows INT,
    new_rows INT,                               -- 新增
    updated_rows INT,                           -- 更新
    disabled_rows INT,                          -- 软停用
    error_details TEXT,                         -- JSON格式错误明细
    import_status ENUM('pending', 'success', 'partial', 'failed'),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE SET NULL
);
```

**错误报告示例：**

```json
{
  "errors": [
    {"row": 5, "field": "student_id", "error": "学号重复"},
    {"row": 12, "field": "class_id", "error": "班级ID不存在"}
  ],
  "warnings": [
    {"row": 8, "field": "phone", "error": "手机号格式不正确"}
  ]
}
```

---

### 3.2 API接口（实时校验场景）

**适用场景：**
- 宿舍清退数据（实时校验）

**技术要求：**

**接口规范：**
- 协议：HTTP/HTTPS
- 方法：GET或POST
- 认证：API Key或OAuth2
- 响应格式：JSON
- 超时时间：5秒

**分页支持：**
- 每页最多100条
- 支持 `page`/`page_size` 参数

**增量同步：**
- 支持 `updated_after` 参数
- 只返回指定时间后更新的数据

**错误码规范：**
- 200：成功
- 400：参数错误
- 401：认证失败
- 404：数据不存在
- 500：服务器错误

**限流策略：**
- 每分钟最多60次请求

**重试机制：**
- 失败后指数退避重试，最多3次

**幂等性：**
- 同一请求多次调用结果一致

---

### 3.3 数据库直连（后续增强）

**适用场景：**
- 数据变更频率高时升级使用

**技术要求：**

**安全边界：**
- 只读账号，不得有写权限
- 使用只读视图或同步库，不直接访问生产业务表
- IP白名单限制，只允许应用服务器访问

**连接池配置：**
- 最大连接数：5
- 超时时间：30秒
- 重试策略：失败后等待5秒重试

**支持数据库：**
- MySQL 5.7+
- SQL Server 2016+
- Oracle 11g+
- PostgreSQL 10+

---

## 四、数据量估算

**明确说明（v2修订）：**

| 数据项 | 首版范围 | 容量设计 | 说明 |
|--------|----------|----------|------|
| 学生账号 | 当届毕业生 | 1000人/届 | 只导入当届（`is_graduating=true` 且 `graduation_year=2026`） |
| 系统容量 | 支持多届历史 | 10000人 | 数据库设计按10000人容量 |
| 辅导员账号 | 当前在职 | 50人 | 离职辅导员标记 `is_active=false` |
| 班级映射 | 当届有效映射 | 50-100条 | 首版不考虑历史有效期 |
| 学工部管理员 | 当前在职 | 5人 | 手动创建 |
| 申请记录 | 当届申请 | 1000条/届 | 每个学生最多1个进行中申请 |

**批次配置（v2新增）：**

```sql
CREATE TABLE graduation_batches (
    id INT PRIMARY KEY AUTO_INCREMENT,
    batch_name VARCHAR(100) NOT NULL,           -- 如 "2026届本科毕业生"
    graduation_year INT NOT NULL,               -- 2026
    is_active BOOLEAN DEFAULT true,             -- 当前批次（仅一个）
    application_start_date DATE,                -- 申请开放时间
    application_end_date DATE,                  -- 申请截止时间
    planned_leave_date_start DATE,              -- 允许的最早离校日期
    planned_leave_date_end DATE,                -- 允许的最晚离校日期
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 约束：仅一个当前批次
    UNIQUE KEY uk_active_batch (is_active) WHERE is_active = true
);
```

**学生导入时只导入当前批次：**

```sql
SELECT * FROM students_external
WHERE is_graduating = true
  AND graduation_year = (SELECT graduation_year FROM graduation_batches WHERE is_active = true);
```

---

## 五、待宿管系统确认的问题清单

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

---

## 六、实施建议

**推荐方案（v2修订）：**

首版采用**CSV/Excel导入 + 宿舍清退API**组合方案：
- 学生、辅导员、班级映射：CSV/Excel批量导入
- 宿舍清退数据：API实时查询
- 后续根据数据变更频率决定是否升级为API/DB同步

**实施路径（v2修订）：**

**阶段1：数据确认（1周）**
1. 向宿管系统提交本需求文档
2. 确认数据可用性、字段定义、对接方式
3. 获取测试数据和字段字典
4. 明确联系人和故障响应方式

**阶段2：CSV导入实现（2周）**
1. 设计三份CSV模板：学生、辅导员、班级-辅导员映射
2. 实现CSV导入功能和校验逻辑
3. 实现staging表和upsert逻辑（v2新增）
4. 实现软停用和重新激活逻辑（v2新增）
5. 实现导入审计日志（v2新增）
6. 生成导入校验报告（成功数、失败数、错误明细）
7. 重点校验：学号唯一、工号唯一、班级映射覆盖率、无效辅导员工号、重复映射

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

## 七、数据库模型完整清单（v2新增）

### 7.1 修改既有表

**users表调整：**
- `student_id` 改为可空（原为 `UNIQUE NOT NULL`）
- 新增 `employee_id VARCHAR(50)` 字段（可空）
- 新增 `class_id VARCHAR(50)` 字段（可空）
- 修改 `chk_auth_method` 约束：增加 `password_setup_required = true` 条件
- 修改 `chk_user_identity` 约束：
  ```sql
  CONSTRAINT chk_user_identity CHECK (
      (role = 'student' AND student_id IS NOT NULL AND employee_id IS NULL AND class_id IS NOT NULL) OR
      (role IN ('counselor', 'admin') AND employee_id IS NOT NULL AND student_id IS NULL AND class_id IS NULL)
  )
  ```

**applications表调整：**
- 新增 `graduation_batch_id INT` 字段（可选，关联批次）

### 7.2 新增表

**1. students_staging - 学生导入临时表**
```sql
CREATE TABLE students_staging (
    student_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    major VARCHAR(100),
    class_id VARCHAR(50),
    class_name VARCHAR(100),
    grade INT,
    graduation_year INT,
    is_graduating BOOLEAN,
    phone VARCHAR(20),
    email VARCHAR(100)
);
```

**2. counselors_staging - 辅导员导入临时表**
```sql
CREATE TABLE counselors_staging (
    employee_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100)
);
```

**3. class_mapping_staging - 班级映射导入临时表**
```sql
CREATE TABLE class_mapping_staging (
    class_id VARCHAR(50) PRIMARY KEY,
    counselor_employee_id VARCHAR(50) NOT NULL
);
```

**4. class_counselor_mapping - 班级-辅导员映射表（核心表）**
```sql
CREATE TABLE class_counselor_mapping (
    id INT PRIMARY KEY AUTO_INCREMENT,
    class_id VARCHAR(50) NOT NULL COMMENT '班级唯一标识',
    counselor_employee_id VARCHAR(50) NOT NULL COMMENT '辅导员工号',
    effective_from DATE COMMENT '生效日期',
    effective_until DATE COMMENT '失效日期',
    graduation_batch_id INT COMMENT '关联毕业批次',
    is_active BOOLEAN DEFAULT true COMMENT '是否有效',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT COMMENT '创建人user_id',
    
    UNIQUE KEY uk_class_active (class_id, is_active),
    FOREIGN KEY (counselor_employee_id) REFERENCES users(employee_id) ON DELETE RESTRICT,
    FOREIGN KEY (graduation_batch_id) REFERENCES graduation_batches(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_class_id (class_id),
    INDEX idx_counselor_employee_id (counselor_employee_id)
);
```

**5. graduation_batches - 批次配置表**
```sql
CREATE TABLE graduation_batches (
    id INT PRIMARY KEY AUTO_INCREMENT,
    batch_name VARCHAR(100) NOT NULL,
    graduation_year INT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    application_start_date DATE,
    application_end_date DATE,
    planned_leave_date_start DATE,
    planned_leave_date_end DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**6. import_logs - 导入审计日志表**
```sql
CREATE TABLE import_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    import_type ENUM('student', 'counselor', 'class_mapping') NOT NULL,
    file_name VARCHAR(255),
    file_hash VARCHAR(64),
    uploaded_by INT,
    total_rows INT,
    success_rows INT,
    failed_rows INT,
    new_rows INT,
    updated_rows INT,
    disabled_rows INT,
    error_details TEXT,
    import_status ENUM('pending', 'success', 'partial', 'failed'),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE SET NULL
);
```

### 7.3 复用既有表

**system_configs - 系统配置表**
- 存储默认终审人配置（不新建system_config表）
- 配置项：`default_admin_ids`、`admin_assignment_mode`

---

## 八、总结

**v2文档完成以下修正：**

1. ✅ CSV导入策略从"全量覆盖"改为"staging + upsert + 软停用"
2. ✅ 数据库模型调整：users表增加employee_id和class_id，调整约束
3. ✅ 新增6个表：3个staging表、class_counselor_mapping、graduation_batches、import_logs
4. ✅ 认证约束调整：支持CSV预导入账号（password_setup_required）
5. ✅ 对接方式调整：学生/辅导员/班级映射改为CSV首版优先
6. ✅ 约束增强：学生必须有class_id，复用system_configs表

**下一步行动：**
1. 提交本文档给宿管系统方反馈
2. 根据宿管系统反馈调整方案
3. 启动实施（按六章节的5阶段路径）

