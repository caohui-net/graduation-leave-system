# XG API与项目数据表对比分析

**文档类型：** 数据表结构对比  
**对比方式：** 示例驱动  
**日期：** 2026-06-03

---

## 一、User（用户表）对比

### 1.1 项目需求表结构（学生）

```python
# backend/apps/users/models.py - User模型（学生角色）
class User(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True)  # 学号
    name = models.CharField(max_length=100)                      # 姓名
    role = models.CharField(max_length=20)                       # student
    department = models.CharField(max_length=100)                # 院系
    class_id = models.CharField(max_length=50)                   # 班级ID ⚠️
    is_graduating = models.BooleanField()                        # 是否毕业生 ⚠️
    graduation_year = models.IntegerField()                      # 毕业年份 ⚠️
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=100, null=True)
    active = models.BooleanField(default=True)
```

### 1.2 XG API实际数据结构

```json
{
  "id": 8925,
  "number": "2025110140314",
  "name": "乐绍钧",
  "phone": "15334282752",
  "status": 1,
  "parent_dep": [{"name": "黄冈师范学院", "level": 1}],
  "department": [{"name": "计算机学院", "level": 2}],
  "user_identity": {"id": 4, "name": "学生"}
}
```

### 1.3 字段映射对比表

| 项目字段 | 必填 | XG字段 | 示例值 | 映射状态 | 不符合说明 |
|---------|------|--------|-------|---------|-----------|
| user_id | ✓ | number | "2025110140314" | ✅ 可映射 | - |
| name | ✓ | name | "乐绍钧" | ✅ 可映射 | - |
| role | ✓ | user_identity.name | "学生" | ⚠️ 需适配 | 实际为对象，mapper假设为字符串 |
| department | ✓ | department[0].name | "计算机学院" | ⚠️ 需适配 | 实际为数组，mapper未取[0] |
| **class_id** | **✓** | **缺失** | **无** | **❌ 无法映射** | **XG API未提供班级ID** |
| **is_graduating** | **✓** | **缺失** | **无** | **❌ 无法映射** | **XG API未提供毕业生标识** |
| **graduation_year** | **✓** | **缺失** | **无** | **❌ 无法映射** | **XG API未提供毕业年份** |
| phone | 可选 | phone | "15334282752" | ⚠️ 部分可用 | 20%为空字符串 |
| email | 可选 | 缺失 | 无 | ❌ 无法映射 | XG API未提供邮箱 |
| active | ✓ | status | 1 | ✅ 可映射 | 1→True, 其他→False |

### 1.4 不符合项说明

**❌ 完全缺失（3个P0字段）：**

1. **class_id（班级ID）**
   - **需求描述：** 唯一标识学生所属班级，用于辅导员分配
   - **业务依赖：** `Student.class_id → ClassMapping.class_id → Counselor`
   - **缺失影响：** 无法自动分配审批人，审批流程阻断
   - **示例需求：** `"CS2022-01"` (计算机科学与技术2022级1班)

2. **is_graduating（毕业生标识）**
   - **需求描述：** 布尔值，标识是否为当届毕业生
   - **业务依赖：** 控制离校申请入口，只有`true`才能提交
   - **缺失影响：** 无法判定申请资格，32,039条记录无法筛选目标1,000人
   - **示例需求：** `true` (2026届毕业生) / `false` (非毕业生)

3. **graduation_year（毕业年份）**
   - **需求描述：** 整数，预计毕业年份
   - **业务依赖：** 数据归档、批次管理、统计报表
   - **缺失影响：** 无法区分往届/当届/下届，归档失败
   - **示例需求：** `2026` (2026年毕业)

**⚠️ 结构不匹配（2个P1字段）：**

4. **role (user_identity)**
   - **实际结构：** `{"id": 4, "name": "学生"}` (对象)
   - **mapper假设：** `"1"` 或 `"student"` (字符串)
   - **不符合：** 类型不匹配，导致所有学生被跳过
   - **需要：** 支持对象结构，按 `user_identity.name == "学生"` 判定

5. **department**
   - **实际结构：** `[{"name": "计算机学院", "level": 2}]` (数组)
   - **mapper假设：** 字符串
   - **不符合：** 直接赋值会导致类型错误
   - **需要：** 取 `department[0].name`

---

## 二、ClassMapping（班级-辅导员映射表）对比

### 2.1 项目需求表结构

```python
# backend/apps/users/models.py - ClassMapping模型
class ClassMapping(models.Model):
    class_id = models.CharField(max_length=50, primary_key=True)  # 班级ID
    class_name = models.CharField(max_length=200, null=True)      # 班级名称
    counselor = models.ForeignKey(User, on_delete=models.PROTECT) # 辅导员
```

**示例数据需求：**
```python
ClassMapping(
    class_id="CS2022-01",
    class_name="计算机科学与技术2022级1班",
    counselor_id="T2022001"  # 王老师工号
)
```

### 2.2 XG API提供情况

**❌ 完全不提供**

XG用户API只返回用户维度数据，不包含班级-辅导员关系。

### 2.3 不符合项说明

**❌ 完全缺失（整张表）：**

- **需求描述：** 班级ID到辅导员工号的一对一映射关系
- **业务依赖：** 学生提交申请时查找对应辅导员
- **缺失影响：** 即使有class_id也无法分配辅导员
- **数据来源：** 需要教务系统或人事系统独立接口

**必需字段示例：**
| class_id | class_name | counselor_employee_id |
|----------|------------|-----------------------|
| CS2022-01 | 计算机科学与技术2022级1班 | T2022001 |
| SE2022-01 | 软件工程2022级1班 | T2022002 |

---

## 三、对比示例：完整学生记录

### 3.1 项目需要的完整学生数据

```json
{
  "user_id": "2022001",
  "name": "张三",
  "role": "student",
  "department": "计算机学院",
  "class_id": "CS2022-01",           // ⚠️ 关键字段
  "is_graduating": true,             // ⚠️ 关键字段
  "graduation_year": 2026,           // ⚠️ 关键字段
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "active": true
}
```

### 3.2 XG API实际能提供的数据

```json
{
  "number": "2022001",               // ✓ 可映射到user_id
  "name": "张三",                    // ✓ 可映射到name
  "user_identity": {"name": "学生"}, // ⚠️ 需适配到role
  "department": [{"name": "计算机学院"}], // ⚠️ 需适配
  // class_id: 缺失              // ❌ 无法提供
  // is_graduating: 缺失          // ❌ 无法提供
  // graduation_year: 缺失        // ❌ 无法提供
  "phone": "13800138000",            // ✓ 可映射
  // email: 缺失                  // ❌ 无法提供
  "status": 1                        // ✓ 可映射到active
}
```

### 3.3 差异标注

| 数据项 | 项目需要 | XG提供 | 状态 |
|-------|---------|--------|------|
| 学号 | ✓ | ✓ | ✅ 满足 |
| 姓名 | ✓ | ✓ | ✅ 满足 |
| 角色 | ✓ | ⚠️ | ⚠️ 结构不匹配 |
| 院系 | ✓ | ⚠️ | ⚠️ 结构不匹配 |
| **班级ID** | **✓** | **✗** | **❌ 缺失** |
| **是否毕业生** | **✓** | **✗** | **❌ 缺失** |
| **毕业年份** | **✓** | **✗** | **❌ 缺失** |
| 手机号 | ✓ | ⚠️ | ⚠️ 20%空值 |
| 邮箱 | 可选 | ✗ | ❌ 缺失 |
| 账号状态 | ✓ | ✓ | ✅ 满足 |

---

## 四、不符合项汇总表

### 4.1 按影响等级分类

| 等级 | 字段 | 不符合类型 | 示例需求 | XG实际 | 业务影响 |
|-----|------|-----------|---------|--------|---------|
| 🔴 P0 | class_id | 完全缺失 | "CS2022-01" | 无 | 审批人分配失败 |
| 🔴 P0 | is_graduating | 完全缺失 | true | 无 | 申请资格判定失败 |
| 🔴 P0 | graduation_year | 完全缺失 | 2026 | 无 | 数据归档失败 |
| 🔴 P0 | ClassMapping全表 | 完全缺失 | {"CS2022-01":"T2022001"} | 无 | 审批链路中断 |
| 🔴 P0 | 宿舍清退状态 | 不在范围 | "completed" | 无 | 提交阻断失效 |
| 🟡 P1 | user_identity | 结构不匹配 | "student" | {"id":4,"name":"学生"} | mapper需适配 |
| 🟡 P1 | department | 结构不匹配 | "计算机学院" | [{"name":"计算机学院"}] | mapper需适配 |
| 🟡 P1 | phone | 部分空值 | "13800138000" | 20%为"" | 联系失败率上升 |
| 🟡 P1 | email | 完全缺失 | "xx@example.com" | 无 | 通知渠道受限 |
| 🟢 P2 | major | 完全缺失 | "计算机科学与技术" | 无 | 展示信息不完整 |
| 🟢 P2 | grade | 完全缺失 | 2022 | 无 | 展示信息不完整 |
| 🟢 P2 | class_name | 完全缺失 | "计算机2022级1班" | 无 | 展示信息不完整 |

### 4.2 按数据表分类

**User表：**
- ❌ 完全缺失：5个（class_id, is_graduating, graduation_year, email, major, grade, class_name中5个必填/重要）
- ⚠️ 结构不匹配：2个（user_identity, department）
- ⚠️ 质量问题：1个（phone 20%空值）
- ✅ 满足：3个（user_id, name, active）

**ClassMapping表：**
- ❌ 完全不提供（整张表）

**宿舍清退：**
- ❌ 不在XG用户API范围（需独立接口）

---

## 五、数据需求规格说明

### 5.1 P0关键字段需求规格

#### class_id（班级ID）

**数据类型：** 字符串，最大50字符  
**必填性：** 学生角色必填  
**唯一性：** 全校唯一，不可重复，不可跨届复用  
**格式要求：**
- 推荐格式：`<专业代码><年级>-<班号>`
- 示例：`CS2022-01`（计算机2022级1班）
- 不可使用：部门名、班级名、临时拼接值

**业务规则：**
- 用于ClassMapping表主键
- 一个class_id对应一个辅导员
- 学生提交申请时通过class_id查找审批人

**数据来源建议：**
- 教务系统班级管理模块
- 人事系统组织架构接口
- 手工维护CSV（当前方案）

---

#### is_graduating（毕业生标识）

**数据类型：** 布尔值（true/false）  
**必填性：** 学生角色必填  
**取值规则：**
- `true`：当届毕业生，可提交离校申请
- `false`：非毕业生，无申请权限

**业务规则：**
- 控制离校申请入口
- 只有`is_graduating=true`才能提交申请
- 批次关闭时统一设置为false

**数据来源建议：**
- 教务系统学籍状态接口
- 按毕业年份自动计算
- 手工维护CSV（当前方案）

---

#### graduation_year（毕业年份）

**数据类型：** 整数（4位年份）  
**必填性：** 学生角色必填  
**取值范围：** 1900-2100  
**示例：** 2026

**业务规则：**
- 用于数据归档
- 用于批次管理
- 用于统计报表时间维度

**数据来源建议：**
- 教务系统学籍信息
- 从入学年份+学制计算
- 手工维护CSV（当前方案）

---

#### ClassMapping（班级-辅导员映射）

**表结构：**
```python
class_id: 班级ID（主键）
class_name: 班级名称（可选，用于展示）
counselor_employee_id: 辅导员工号（外键）
```

**数据要求：**
- 必须覆盖所有学生的class_id
- 一个班级只能有一个主辅导员
- 辅导员必须在User表中存在且role=counselor

**业务规则：**
- 学生提交申请时查询 `Student.class_id → ClassMapping → Counselor`
- 辅导员只能审批自己班级的申请

**数据来源建议：**
- 教务系统班级辅导员关系接口
- 人事系统组织架构
- 手工维护CSV（当前方案）

---

### 5.2 补充字段需求规格

#### email（邮箱）

**数据类型：** 字符串，最大100字符  
**必填性：** 可选  
**格式：** 符合邮箱格式规范  
**用途：** 通知、找回密码

---

#### major（专业）

**数据类型：** 字符串，最大100字符  
**必填性：** 建议提供  
**用途：** 展示信息、统计维度

---

#### grade（年级）

**数据类型：** 整数（入学年份）  
**必填性：** 建议提供  
**示例：** 2022  
**用途：** 展示信息、批次计算

---

## 六、结论

### 6.1 符合度评估

**整体符合度：** 30% (3/10核心字段)

**分类统计：**
- ✅ 完全满足：3个（user_id, name, active）
- ⚠️ 部分满足/需适配：3个（role, department, phone）
- ❌ 完全不满足：4个（class_id, is_graduating, graduation_year, ClassMapping）

### 6.2 可用性结论

**XG API ❌ 无法独立支持项目需求**

**原因：**
1. 缺失3个P0关键业务字段
2. 缺失班级-辅导员映射关系
3. 存在结构不匹配问题

**推荐方案：** CSV主导 + XG API补充

---

**文档完成时间：** 2026-06-03T16:20:00Z

