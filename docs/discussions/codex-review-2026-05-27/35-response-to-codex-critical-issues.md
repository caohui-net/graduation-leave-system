# 对Codex关键问题的修正方案

**回应时间：** 2026-05-27  
**回应对象：** Codex对34号文档的审查（.omc/artifacts/ask/codex-docs-discussions-codex-review-2026-05-27-34-codex-second-rev-2026-05-27T08-21-47-897Z.md）  
**原始文档：** `34-codex-second-review-response.md`

---

## 一、总体回应

**完全接受Codex指出的5个关键问题，逐项修正。**

Codex结论："方向基本可以接受，但不建议原样进入 v2。主要还有 5 个需要修正的点。"

我们认同这5个问题都是实施级关键缺陷，必须在v2文档中修正。

---

## 二、对5个关键问题的逐项修正

### 2.1 问题1：users_staging主键不可用（行45-51）

**Codex意见：** `PRIMARY KEY (student_id, employee_id, role)` 会让可空字段隐式非空，学生没有employee_id、辅导员没有student_id，导入会冲突。

**我们的回应：** ✅ **完全接受，立即修正**

**问题分析：**

原方案的staging表设计：
```sql
CREATE TABLE users_staging (
    student_id VARCHAR(50),
    employee_id VARCHAR(50),
    name VARCHAR(100) NOT NULL,
    role ENUM('student', 'counselor', 'admin') NOT NULL,
    PRIMARY KEY (student_id, employee_id, role)  -- 问题：复合主键让可空字段隐式非空
);
```

冲突场景：
1. 学生导入：`student_id='2022001', employee_id=NULL, role='student'` → 主键包含NULL，插入失败
2. 辅导员导入：`student_id=NULL, employee_id='T001', role='counselor'` → 主键包含NULL，插入失败

**修正方案：按导入类型拆分staging表**

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

**导入流程调整：**

```sql
-- 1. 学生导入
TRUNCATE students_staging;
LOAD DATA INFILE 'students.csv' INTO TABLE students_staging;

-- 2. Upsert到users表
INSERT INTO users (student_id, name, department, major, class_id, role, is_active, ...)
SELECT student_id, name, department, major, class_id, 'student', true, ...
FROM students_staging
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    department = VALUES(department),
    class_id = VALUES(class_id),
    is_active = true,
    updated_at = NOW();

-- 3. 软停用：本次未导入的学生
UPDATE users
SET is_active = false, updated_at = NOW()
WHERE role = 'student'
  AND student_id NOT IN (SELECT student_id FROM students_staging);
```

**优化：使用NOT EXISTS替代NOT IN**

Codex建议用`NOT EXISTS`替代`NOT IN`，避免NULL值问题：

```sql
UPDATE users u
SET is_active = false, updated_at = NOW()
WHERE u.role = 'student'
  AND NOT EXISTS (
      SELECT 1 FROM students_staging s
      WHERE s.student_id = u.student_id
  );
```

---

### 2.2 问题2：缺少class_counselor_mapping表定义（行412）

**Codex意见：** 文档前面依赖它分配辅导员，但数据库模型调整章节没有正式定义它。

**我们的回应：** ✅ **完全接受，立即补充**

**问题分析：**

文档多处引用`class_counselor_mapping`表：
- 行184-188：定义表结构（但只是示例，不是正式定义）
- 行241-243：申请提交时查询该表
- 行412：新增表清单中遗漏

**修正方案：正式定义class_counselor_mapping表**

```sql
CREATE TABLE class_counselor_mapping (
    id INT PRIMARY KEY AUTO_INCREMENT,
    class_id VARCHAR(50) NOT NULL COMMENT '班级唯一标识',
    counselor_employee_id VARCHAR(50) NOT NULL COMMENT '辅导员工号',
    
    -- 有效期和批次
    effective_from DATE COMMENT '生效日期',
    effective_until DATE COMMENT '失效日期',
    graduation_batch_id INT COMMENT '关联毕业批次',
    
    -- 元数据
    is_active BOOLEAN DEFAULT true COMMENT '是否有效',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by INT COMMENT '创建人user_id',
    
    -- 唯一约束：同一班级同一时间只能有一个有效辅导员
    UNIQUE KEY uk_class_active (class_id, is_active),
    
    -- 外键约束
    FOREIGN KEY (counselor_employee_id) REFERENCES users(employee_id) ON DELETE RESTRICT,
    FOREIGN KEY (graduation_batch_id) REFERENCES graduation_batches(id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL,
    
    -- 索引
    INDEX idx_class_id (class_id),
    INDEX idx_counselor_employee_id (counselor_employee_id),
    INDEX idx_graduation_batch_id (graduation_batch_id)
) COMMENT='班级-辅导员映射表';
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| class_id | VARCHAR(50) | 班级唯一标识，如 `CS2022-01` |
| counselor_employee_id | VARCHAR(50) | 辅导员工号，引用 `users.employee_id` |
| effective_from | DATE | 生效日期，支持未来映射变更 |
| effective_until | DATE | 失效日期，NULL表示长期有效 |
| graduation_batch_id | INT | 关联毕业批次，支持多届管理 |
| is_active | BOOLEAN | 是否有效，配合唯一约束确保一班一辅导员 |

**唯一约束说明：**

`UNIQUE KEY uk_class_active (class_id, is_active)` 确保：
- 同一班级只能有一个 `is_active=true` 的映射
- 历史映射可以保留（`is_active=false`）

**外键解析规则：**

```python
def get_counselor_for_class(class_id, graduation_batch_id=None):
    """根据班级ID查询辅导员"""
    query = ClassCounselorMapping.query.filter_by(
        class_id=class_id,
        is_active=True
    )
    
    # 如果指定批次，优先匹配批次
    if graduation_batch_id:
        mapping = query.filter_by(graduation_batch_id=graduation_batch_id).first()
        if mapping:
            return mapping
    
    # 否则返回当前有效映射
    mapping = query.first()
    if not mapping:
        raise ValueError(f"班级 {class_id} 未配置辅导员")
    
    # 检查有效期
    today = date.today()
    if mapping.effective_from and today < mapping.effective_from:
        raise ValueError(f"班级 {class_id} 的辅导员映射尚未生效")
    if mapping.effective_until and today > mapping.effective_until:
        raise ValueError(f"班级 {class_id} 的辅导员映射已失效")
    
    return mapping
```

---

### 2.3 问题3：认证约束冲突（行293-295）

**Codex意见：** 主设计中 `users` 表有 `chk_auth_method` 约束，要求 `password_hash` 或 `wechat_openid` 非空；CSV预导入账号通常还没有密码或微信绑定，会被约束挡住。

**我们的回应：** ✅ **完全接受，立即修正**

**问题分析：**

当前数据库设计（docs/design/2026-05-27-system-design.md:293-295）：
```sql
CONSTRAINT chk_auth_method CHECK (
    (password_hash IS NOT NULL) OR (wechat_openid IS NOT NULL)
)
```

CSV导入场景：
1. 学生CSV导入：只有学号、姓名等基本信息，没有密码或微信openid
2. 插入users表时：`password_hash=NULL, wechat_openid=NULL` → 违反约束，插入失败

**修正方案：调整认证约束，允许预导入账号**

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(50),
    employee_id VARCHAR(50),
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255),
    wechat_openid VARCHAR(100) UNIQUE,
    
    -- 认证状态字段
    password_setup_required BOOLEAN DEFAULT FALSE COMMENT '需要设置密码',
    account_locked BOOLEAN DEFAULT FALSE COMMENT '账户锁定',
    
    role ENUM('student', 'counselor', 'admin') NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- 条件唯一约束
    UNIQUE KEY uk_student_id (student_id),
    UNIQUE KEY uk_employee_id (employee_id),
    
    -- 修正后的认证约束：允许预导入账号
    CONSTRAINT chk_auth_method CHECK (
        (password_hash IS NOT NULL) OR 
        (wechat_openid IS NOT NULL) OR 
        (password_setup_required = true)
    ),
    
    -- 学生/辅导员/管理员标识互斥约束
    CONSTRAINT chk_user_identity CHECK (
        (role = 'student' AND student_id IS NOT NULL AND employee_id IS NULL) OR
        (role IN ('counselor', 'admin') AND employee_id IS NOT NULL AND student_id IS NULL)
    )
);
```

**约束说明：**

修正后的 `chk_auth_method` 允许三种认证状态：
1. `password_hash IS NOT NULL`：已设置密码
2. `wechat_openid IS NOT NULL`：已绑定微信
3. `password_setup_required = true`：预导入账号，待设置密码

**CSV导入时的处理：**

```python
def import_students_from_csv(csv_file):
    for row in csv_file:
        user = User(
            student_id=row['student_id'],
            name=row['name'],
            role='student',
            password_setup_required=True,  # 标记为待设置密码
            is_active=True
        )
        db.session.add(user)
    db.session.commit()
```

**首次登录流程：**

```python
def first_login(student_id, password):
    """学生首次登录设置密码"""
    user = User.query.filter_by(
        student_id=student_id,
        role='student',
        password_setup_required=True
    ).first()
    
    if not user:
        raise ValueError("账号不存在或已设置密码")
    
    # 设置密码
    user.password_hash = hash_password(password)
    user.password_setup_required = False
    db.session.commit()
    
    return user
```

**登录逻辑调整：**

```python
def authenticate(username, password, role):
    """统一认证入口"""
    # 根据角色查询用户
    if role == 'student':
        user = User.query.filter_by(student_id=username, role='student').first()
    else:
        user = User.query.filter_by(employee_id=username, role=role).first()
    
    if not user:
        return None
    
    # 检查账号状态
    if not user.is_active:
        raise ValueError("账号已停用")
    if user.account_locked:
        raise ValueError("账号已锁定")
    
    # 检查认证方式
    if user.password_setup_required:
        raise ValueError("请先设置密码")
    
    # 验证密码
    if user.password_hash and check_password(password, user.password_hash):
        return user
    
    return None
```

---

### 2.4 问题4：class_id约束不完整（行135-139）

**Codex意见：** 检查约束只检查学生/员工标识互斥，没有检查学生必须有 `class_id`。

**我们的回应：** ✅ **完全接受，立即修正**

**问题分析：**

当前约束只检查 `student_id` 和 `employee_id` 互斥，未检查学生必须有 `class_id`。

**修正方案：**

```sql
-- 增强的检查约束：学生必须有student_id和class_id
CONSTRAINT chk_user_identity CHECK (
    (role = 'student' AND student_id IS NOT NULL AND employee_id IS NULL AND class_id IS NOT NULL) OR
    (role IN ('counselor', 'admin') AND employee_id IS NOT NULL AND student_id IS NULL AND class_id IS NULL)
)
```

**应用层校验：**

```python
def import_students_from_csv(csv_file):
    errors = []
    for row_num, row in enumerate(csv_file, start=1):
        if not row.get('student_id'):
            errors.append({"row": row_num, "field": "student_id", "error": "学号不能为空"})
        if not row.get('class_id'):
            errors.append({"row": row_num, "field": "class_id", "error": "班级ID不能为空"})
    
    if errors:
        raise ValueError(f"CSV校验失败，共 {len(errors)} 个错误")
```

---

### 2.5 问题5：表名重复（行364）

**Codex意见：** 新建 `system_config` 与主设计已有 `system_configs` 重复。

**我们的回应：** ✅ **完全接受，立即修正**

**修正方案：复用既有 `system_configs` 表**

删除新建 `system_config` 表的提议，使用 `system_configs` 表存储默认终审人配置。

**配置示例：**

```sql
INSERT INTO system_configs (config_key, config_value, config_type, description) VALUES
('default_admin_ids', '3,5,7', 'workflow', '默认终审人列表'),
('admin_assignment_mode', 'fixed', 'workflow', '分配模式：fixed/round_robin/load_balance');
```

**分配逻辑：**

```python
def assign_admin(application):
    config = SystemConfig.query.filter_by(config_key='default_admin_ids').first()
    if not config:
        raise ValueError("系统未配置默认终审人")
    
    admin_ids = [int(x.strip()) for x in config.config_value.split(',')]
    available_admins = User.query.filter(
        User.id.in_(admin_ids),
        User.role == 'admin',
        User.is_active == True
    ).all()
    
    if not available_admins:
        raise ValueError("无可用的终审管理员")
    
    application.admin_id = available_admins[0].id
    application.current_approver_id = available_admins[0].id
    return available_admins[0]
```

---

## 三、数据库模型完整清单

基于上述5个问题的修正，完整的数据库模型调整清单：

### 3.1 修改既有表

**users表：**
- `student_id` 改为可空
- 新增 `employee_id` 字段（可空）
- 新增 `class_id` 字段（可空）
- 修改 `chk_auth_method` 约束：增加 `password_setup_required` 条件
- 修改 `chk_user_identity` 约束：增加 `class_id` 必填检查

**applications表：**
- 新增 `graduation_batch_id` 字段（可选，关联批次）

### 3.2 新增表

1. **students_staging** - 学生导入临时表
2. **counselors_staging** - 辅导员导入临时表
3. **class_mapping_staging** - 班级映射导入临时表
4. **class_counselor_mapping** - 班级-辅导员映射表（核心表）
5. **graduation_batches** - 批次配置表
6. **import_logs** - 导入审计日志表

### 3.3 复用既有表

- **system_configs** - 存储默认终审人配置（不新建system_config）

---

## 四、总结

**完全接受Codex的5个关键修正意见：**

1. ✅ users_staging主键改为按类型拆分表，使用NOT EXISTS替代NOT IN
2. ✅ 补充class_counselor_mapping表完整定义
3. ✅ 调整认证约束，增加password_setup_required支持CSV导入
4. ✅ 增强class_id约束，确保学生必须有class_id
5. ✅ 复用system_configs表，删除system_config重复表名

**下一步行动：**

1. 基于本修正方案，创建 `31-data-source-requirements-consensus-v2.md`
2. 整合34号文档和35号文档的所有修正
3. 提交给宿管系统方反馈

**是否可以创建v2：** ✅ **可以**

修正完成后，方向和实施细节都已明确，可以基于此创建v2共识文档。

