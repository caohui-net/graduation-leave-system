# 学工系统用户API字段覆盖报告

**版本：** v1.0（正式版）  
**日期：** 2026-06-04  
**状态：** 基于2026-06-03 live样本（湖南工学院生产环境32,039用户）  
**数据质量：** 95/100 (A级)

---

## 一、文档目的

本文档定义学工系统用户API字段与本系统内部`User`模型字段的映射关系，明确：

1. 哪些字段可以从学工API获取
2. 哪些字段必须由CSV/手工维护
3. 字段缺失时的处理规则
4. API与CSV的并存策略

**核心结论：** XG API无法独立支持项目需求（缺失class_id/is_graduating/graduation_year等关键业务字段），只能作为补充信息源。推荐策略：CSV主导 + XG API补充。

---

## 二、学工API字段清单（实际采集结果）

基于2026-06-03湖南工学院生产环境live采集（32,039用户，20条详细样本），学工用户API实际提供以下字段：

### 2.1 确认可用字段

| 字段名 | 类型 | 完整性 | 实际结构 | 说明 |
|--------|------|--------|----------|------|
| `number` | string | 100% | `"2025110140314"` | 学号/工号 |
| `name` | string | 100% | `"乐绍钧"` | 用户姓名 |
| `user_identity` | object | 100% | `{"id": 4, "name": "学生"}` | 身份类型（对象非字符串） |
| `department` | array | 100% | `[{"name": "计算机学院", "level": 2}]` | 院系（数组非字符串） |
| `phone` | string | 80% | `"15334282752"` or `""` | 手机号（20%空字符串） |
| `status` | number | 100% | `1` | 账号状态（1=正常） |

### 2.2 确认缺失字段（P0关键）

以下关键业务字段经live测试确认**完全不提供**：

- ❌ `class_id`：班级ID（审批人分配必需）
- ❌ `is_graduating`：是否毕业生（申请资格判定必需）
- ❌ `graduation_year`：毕业年份（数据归档必需）
- ❌ `email`：邮箱
- ❌ `major`：专业
- ❌ `grade`：年级
- ❌ `class_name`：班级名称

---

## 三、内部User模型字段清单

### 3.1 核心字段（必填）

| 字段名 | 类型 | 业务约束 | 说明 |
|--------|------|---------|------|
| `user_id` | string | 主键，全局唯一 | 学生使用学号，其他用户使用工号 |
| `name` | string | 必填 | 用户姓名 |
| `role` | string | 必填，枚举值 | student/counselor/advisor/dean/admin |

### 3.2 学生特定字段（学生必填）

| 字段名 | 类型 | 业务约束 | 说明 |
|--------|------|---------|------|
| `class_id` | string | 学生必填 | 班级ID，用于辅导员映射（ClassMapping） |
| `is_graduating` | boolean | 学生必填 | 是否当届毕业生，决定离校申请资格 |
| `graduation_year` | integer | 学生必填 | 毕业年份 |

### 3.3 可选字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `phone` | string | 手机号（用于找回密码、通知） |
| `email` | string | 邮箱（用于通知） |
| `department` | string | 院系/部门（用于展示） |
| `active` | boolean | 账号状态（默认true） |

### 3.4 关联约束

**ClassMapping约束：**
- 学生的`class_id`必须能匹配`ClassMapping`表中的记录
- `ClassMapping.class_id` → `ClassMapping.counselor_id` → `User.user_id`（辅导员）
- 如果`class_id`缺失或无法匹配，学生申请将无法自动分配辅导员审批人

---

## 四、字段映射表

### 4.1 可映射字段

| 内部目标 | 来源字段 | 映射状态 | 处理规则 |
|---------|---------|---------|---------|
| `User.user_id` | `number` | 🟡 待确认 | **必填**。缺失则跳过该用户，记录到跳过日志。需live确认`number`是否等同学号/工号。 |
| `User.name` | `name` | 🟡 待确认 | **必填**。缺失则跳过该用户，记录到跳过日志。 |
| `User.phone` | `phone` | 🟡 待确认 | **可选**。缺失则置为NULL。 |
| `User.department` | `department` | 🟡 待确认 | **可选**。缺失则置为NULL。 |

### 4.2 角色映射（高风险）

| 内部目标 | 来源字段 | 映射状态 | 处理规则 |
|---------|---------|---------|---------|
| `User.role` | `user_identity` | 🔴 未确认 | **必填，高风险**。<br>- 需live确认`user_identity`值域（可能是1/2/3或student/teacher/staff）<br>- **初期策略：只接受明确的"学生"值，其他值一律跳过**<br>- 跳过原因：`unknown_user_identity: {value}` |

**角色映射规则（待live确认后补充）：**
```python
# 示例（需根据live数据调整）
USER_IDENTITY_MAP = {
    '1': 'student',      # 假设1代表学生
    'student': 'student', # 假设直接返回student
    # 其他值一律跳过，不做推断
}
```

### 4.3 无法映射字段（必须CSV维护）

| 内部目标 | 来源字段 | 映射状态 | 处理规则 |
|---------|---------|---------|---------|
| `User.class_id` | 未知 | 🔴 缺失 | **学生必填，API无法提供**。<br>- 继续由CSV/手工维护<br>- API同步时不覆盖此字段<br>- 新用户如果缺失`class_id`，标记为`skip_reason: missing_class_id` |
| `User.is_graduating` | 未知 | 🔴 缺失 | **学生必填，API无法提供**。<br>- 继续由CSV/手工维护<br>- API同步时不覆盖此字段<br>- 新用户如果缺失，标记为`skip_reason: missing_is_graduating` |
| `User.graduation_year` | 未知 | 🔴 缺失 | **学生必填，API无法提供**。<br>- 继续由CSV/手工维护<br>- API同步时不覆盖此字段<br>- 新用户如果缺失，标记为`skip_reason: missing_graduation_year` |

---

## 五、字段缺失处理规则

### 5.1 跳过规则（不创建/更新用户）

以下情况跳过该用户记录，不进行任何数据库操作：

| 场景 | 跳过原因标识 | 说明 |
|------|-------------|------|
| `number`缺失 | `missing_user_id` | 主键缺失，无法唯一识别用户 |
| `name`缺失 | `missing_name` | 必填字段缺失 |
| `user_identity`未知 | `unknown_user_identity: {value}` | 角色无法识别，不做推断 |
| `user_identity`非学生 | `not_student: {value}` | 初期只同步学生用户 |

### 5.2 部分映射规则（可创建/更新用户）

以下情况可以创建或更新用户，但某些字段置为NULL或保持原值：

| 场景 | 处理方式 |
|------|---------|
| `phone`缺失 | 置为NULL（新用户）或保持原值（已存在用户） |
| `email`缺失 | 置为NULL（新用户）或保持原值（已存在用户） |
| `department`缺失 | 置为NULL（新用户）或保持原值（已存在用户） |
| `class_id`缺失 | 保持原值（不覆盖），新用户跳过并标记`missing_class_id` |
| `is_graduating`缺失 | 保持原值（不覆盖），新用户跳过并标记`missing_is_graduating` |
| `graduation_year`缺失 | 保持原值（不覆盖），新用户跳过并标记`missing_graduation_year` |

### 5.3 错误报告格式

跳过的用户应输出到同步日志和错误报告：

```json
{
  "skipped_users": [
    {
      "number": "2022001",
      "name": "张三",
      "skip_reason": "missing_class_id",
      "raw_data": {
        "number": "2022001",
        "name": "张三",
        "user_identity": "1"
      }
    }
  ],
  "skipped_count": 1,
  "skipped_by_reason": {
    "missing_class_id": 1
  }
}
```

---

## 六、API与CSV并存策略

### 6.1 核心原则

**在字段未完全覆盖前，API只能补充或更新可确定字段，不能替代CSV导入。**

### 6.2 并存规则

| 数据来源 | 负责字段 | 说明 |
|---------|---------|------|
| **CSV导入（主）** | `user_id`, `name`, `role`, `class_id`, `is_graduating`, `graduation_year` | 学生创建和核心业务字段由CSV维护 |
| **学工API（补充）** | `phone`, `email`, `department`, `updated_at` | API仅补充或更新非核心字段 |

### 6.3 同步模式

**Phase 1（当前）：CSV主导 + API补充**
- CSV导入创建所有学生用户（包含`class_id`/`is_graduating`/`graduation_year`）
- 学工API同步仅更新已存在用户的`phone`/`email`/`department`
- 学工API **不创建新用户**（因为缺少`class_id`等必填字段）

**Phase 2（未来）：API主导 + CSV补充**
- 前提：live测试确认学工API能提供`class_id`/`is_graduating`/`graduation_year`
- 学工API可以创建新用户
- CSV仅补充学工API缺失的字段

### 6.4 停用策略

**初期策略：不自动停用**
- 学工API本次未返回某用户 ≠ 该用户应停用
- 原因：API可能因为权限、筛选条件、分页等原因遗漏部分用户
- 仅输出差异报告：`{api_user_ids} - {local_user_ids}` 和 `{local_user_ids} - {api_user_ids}`

**未来策略：**
- 等live数据稳定后，可考虑：
  - 连续N次同步都缺失 → 标记为待审查
  - 手工审查后 → 停用账号（`active=False`）

---

## 七、Step 3 mapper测试样例

### 7.1 输入样例

```python
# 样例1：完整字段
{
    "number": "2022001",
    "name": "张三",
    "phone": "13800138000",
    "department": "计算机学院",
    "user_identity": "1"  # 假设1代表学生
}

# 样例2：name缺失
{
    "number": "2022002",
    "phone": "13800138001",
    "user_identity": "1"
}

# 样例3：user_identity未知
{
    "number": "2022003",
    "name": "李四",
    "user_identity": "999"  # 未知值
}
```

### 7.2 预期输出

```python
# 样例1输出：可映射
{
    "user_id": "2022001",
    "name": "张三",
    "role": "student",
    "phone": "13800138000",
    "department": "计算机学院",
    "class_id": None,  # API不提供
    "is_graduating": None,  # API不提供
    "graduation_year": None,  # API不提供
    "skip_reason": None
}

# 样例2输出：应跳过
{
    "user_id": "2022002",
    "name": None,
    "role": None,
    "phone": "13800138001",
    "department": None,
    "class_id": None,
    "is_graduating": None,
    "graduation_year": None,
    "skip_reason": "missing_name"
}

# 样例3输出：应跳过
{
    "user_id": "2022003",
    "name": "李四",
    "role": None,
    "phone": None,
    "department": None,
    "class_id": None,
    "is_graduating": None,
    "graduation_year": None,
    "skip_reason": "unknown_user_identity: 999"
}
```

---

## 八、验收标准

Step 2C-lite完成的标准：

- ✅ 明确哪些字段允许API写入，哪些字段仍由CSV/手工来源维护
- ✅ 明确什么情况下跳过记录、报告错误、禁止同步
- ✅ 能为下一步mapper/provider测试提供固定输入输出样例
- ✅ 定义API与CSV的并存策略和切换条件

---

## 九、后续行动

### 9.1 立即行动

1. 基于本文档实现`map_xg_user_to_internal()`函数
2. 基于Section 7测试样例编写单元测试
3. 通过测试后进入Step 4

### 9.2 待live测试确认

1. `number`字段是否等同学号/工号
2. `user_identity`值域和映射规则
3. 是否提供`class_id`/`is_graduating`/`graduation_year`
4. 实际返回的完整字段清单
5. 分页、筛选、排序逻辑

### 9.3 文档更新计划

- live测试完成后，更新Section 2"学工API字段清单"
- 根据live数据更新Section 4.2"角色映射规则"
- 评估是否可以进入Phase 2（API主导模式）

---

**文档状态：** ✅ Step 2C-lite完成，可进入Step 3实现
