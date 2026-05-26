# 数据库设计审查 - Round 4

**审查时间：** 2026-05-27  
**审查人：** Codex Critic Agent  
**审查范围：** 数据库设计（第3节）- 7个核心表

---

## 审查结论

**VERDICT: REVISE**

发现2个CRITICAL问题和4个MAJOR问题，需要修订后才能实施。

---

## CRITICAL问题

### 1. 软删除破坏外键完整性

**证据：** lines 270, 299, 303-304, 363, 365, 398-399, 534

**问题：**
- users表有`is_deleted`字段（软删除）
- applications表有`student_id`外键指向users
- 软删除用户时，其申请仍然存在，指向"已删除"用户
- 查询`applications WHERE is_deleted=FALSE`会返回申请，但关联的用户是已删除状态

**影响：**
1. 数据不一致：活跃申请属于"已删除"用户
2. 查询复杂：每个查询需要`AND users.is_deleted=FALSE`
3. 级联混乱：line 534说"级联删除"但软删除不级联

**修复方案A（推荐）：** 软删除 + 过滤外键
```sql
-- Django ORM方式（更清晰）
class Application(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.PROTECT,  # 有申请时阻止删除
        limit_choices_to={'is_deleted': False}
    )
```

**修复方案B：** 硬删除 + 归档表
```sql
CREATE TABLE users_archive (
    -- 与users相同结构
    deleted_at TIMESTAMP NOT NULL
);
```

**修复方案C：** 完全移除软删除
```sql
-- 移除is_deleted列
-- 使用Django的on_delete=models.CASCADE真实删除
-- 保留audit_logs作为历史记录
```

### 2. 缺少关键查询的复合索引

**证据：** lines 305-308, 339-341, 400-402

**问题：**
最常用的查询会很慢：

**查询1：** "显示辅导员X的待审批申请"
```sql
SELECT * FROM applications 
WHERE status = 'pending_counselor' 
  AND current_approver_id = 123
  AND is_deleted = FALSE
ORDER BY submit_time DESC;

-- 当前索引：idx_status, 无current_approver_id索引
-- 结果：current_approver_id全表扫描
```

**查询2：** "显示用户X的未读通知"
```sql
SELECT * FROM notifications
WHERE user_id = 123
  AND is_read = FALSE
ORDER BY created_at DESC;

-- 当前索引：idx_user_id, idx_is_read（分开）
-- 结果：索引合并或表扫描
```

**修复：** 添加复合索引
```sql
-- applications表
CREATE INDEX idx_approver_status ON applications(current_approver_id, status, submit_time);
CREATE INDEX idx_student_status ON applications(student_id, status, created_at);
CREATE INDEX idx_status_deleted ON applications(status, is_deleted, submit_time);

-- approvals表
CREATE INDEX idx_app_time ON approvals(application_id, approval_time DESC);

-- notifications表
CREATE INDEX idx_user_read_time ON notifications(user_id, is_read, created_at DESC);

-- attachments表
CREATE INDEX idx_app_type ON attachments(application_id, attachment_type, is_deleted);

-- audit_logs表
CREATE INDEX idx_user_action_time ON audit_logs(user_id, action, created_at DESC);
CREATE INDEX idx_resource_time ON audit_logs(resource_type, resource_id, created_at DESC);
```

---

## MAJOR问题

### 3. 审计日志表缺少关键字段

**证据：** lines 457-476, 478-494

**缺失字段：**
- 无`session_id`追踪用户会话
- 无`before_value`/`after_value`追踪数据变更
- 无`correlation_id`追踪关联操作
- `user_id`可空但大多数操作应该必需

**影响：** 无法回答关键审计问题：
- "这个用户在申请#123中改了什么？" → 无before/after值
- "安全事件期间谁批准了这个申请？" → 无会话追踪
- "追踪这个审批工作流中的所有操作" → 无correlation_id

**修复：** 增强audit_logs表
```sql
CREATE TABLE audit_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '操作用户ID',  -- 改为必需
    session_id VARCHAR(100) COMMENT '会话ID',  -- 新增
    correlation_id VARCHAR(100) COMMENT '关联ID',  -- 新增
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    resource_id BIGINT,
    
    -- 新增变更追踪
    field_name VARCHAR(100) COMMENT '修改字段',
    old_value TEXT COMMENT '修改前值',
    new_value TEXT COMMENT '修改后值',
    
    ip_address VARCHAR(50),
    user_agent TEXT,
    request_data TEXT,
    response_status INT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_session_id (session_id),
    INDEX idx_correlation_id (correlation_id)
);
```

### 4. applications表缺少关键字段

**证据：** lines 288-310

**缺失字段：**
- 无`counselor_id`（只有`current_approver_id`会变）
- 无`admin_id`（谁做的最终审批？）
- 无`version`字段用于乐观锁
- 无`certificate_url`（line 42提到"电子离校凭证"）

**影响：**
1. 报表不可能："辅导员X本月批准了多少申请？" → 无法查询
2. 并发bug：两个审批人同时批准 → 无乐观锁
3. 凭证追踪：line 1175提到生成凭证，但无处存储

**修复：** 添加缺失字段
```sql
CREATE TABLE applications (
    -- 现有字段...
    
    -- 新增固定审批人追踪
    counselor_id BIGINT COMMENT '辅导员ID',
    admin_id BIGINT COMMENT '学工部管理员ID',
    
    -- 新增凭证追踪
    certificate_url VARCHAR(500) COMMENT '离校凭证URL',
    certificate_generated_at TIMESTAMP COMMENT '凭证生成时间',
    
    -- 新增乐观锁
    version INT DEFAULT 0 COMMENT '版本号',
    
    FOREIGN KEY (counselor_id) REFERENCES users(id),
    FOREIGN KEY (admin_id) REFERENCES users(id),
    INDEX idx_counselor_id (counselor_id),
    INDEX idx_admin_id (admin_id)
);
```

### 5. users表缺少认证安全字段

**证据：** lines 256-278

**基于Round 1-3达成的认证改进，缺失字段：**
- 无`password_setup_required`标志
- 无`account_locked`标志
- 无`failed_login_attempts`计数器
- 无`last_login_at`时间戳
- 无`wechat_bind_time`时间戳

**修复：** 添加安全字段
```sql
CREATE TABLE users (
    -- 现有字段...
    
    -- 新增认证安全字段
    password_setup_required BOOLEAN DEFAULT FALSE COMMENT '需要设置密码',
    account_locked BOOLEAN DEFAULT FALSE COMMENT '账户锁定',
    failed_login_attempts INT DEFAULT 0 COMMENT '失败登录次数',
    last_login_at TIMESTAMP COMMENT '最后登录时间',
    last_login_ip VARCHAR(50) COMMENT '最后登录IP',
    wechat_bind_time TIMESTAMP COMMENT '微信绑定时间',
    password_changed_at TIMESTAMP COMMENT '密码修改时间',
    
    INDEX idx_account_locked (account_locked),
    
    -- Round 1约定的约束
    CONSTRAINT chk_auth_method CHECK (
        (password_hash IS NOT NULL) OR (wechat_openid IS NOT NULL)
    )
);
```

### 6. 缺少活跃申请的唯一约束

**证据：** lines 288-310, 532

**问题：**
- line 532说"一个学生可以创建多个申请"
- 但无约束防止：学生创建多个草稿、同时提交多个申请、待审批时重复提交

**修复：** 添加部分唯一约束
```sql
-- PostgreSQL语法
CREATE UNIQUE INDEX idx_student_active_application 
ON applications(student_id) 
WHERE status IN ('draft', 'pending_counselor', 'pending_admin') 
  AND is_deleted = FALSE;

-- MySQL变通（不支持WHERE）
-- 在Django应用层检查
class Application(models.Model):
    def save(self, *args, **kwargs):
        if self.status in ['draft', 'pending_counselor', 'pending_admin']:
            existing = Application.objects.filter(
                student_id=self.student_id,
                status__in=['draft', 'pending_counselor', 'pending_admin'],
                is_deleted=False
            ).exclude(id=self.id).exists()
            
            if existing:
                raise ValidationError("您已有进行中的申请，请等待审批完成")
        
        super().save(*args, **kwargs)
```

---

## 次要问题

### 7. 时间戳默认值不一致
混合使用`DEFAULT CURRENT_TIMESTAMP`和Django的`auto_now`。

**修复：** 让Django处理时间戳，移除数据库默认值。

### 8. attachments表缺少file_hash字段
Round 1讨论中同意添加文件哈希去重。

**修复：** 添加`file_hash VARCHAR(64)`

### 9. notifications表缺少retry_count
`send_status`追踪失败，但无重试计数器。

**修复：** 添加`retry_count INT DEFAULT 0`

---

## 缺失组件

- 无`applications_history`表（申请被驳回重提时，旧数据丢失）
- 无`approver_delegates`表（辅导员请假时的临时替代）
- 无附件版本控制（学生替换附件时，旧版本丢失）
- 无`user_notification_preferences`表（所有用户收到所有通知）
- 无`api_rate_limits`表（Round 1提到API限流，但无数据追踪）
- 无系统维护模式标志
- 无数据保留策略（audit_logs永久增长）
- 无级联删除规则（line 534提到级联，但外键未指定ON DELETE行为）

---

## 开放问题

- 是否应添加`applications_history`表用于审计追踪？
- audit_logs的数据保留策略？（1年？3年？永久？）
- notifications应该软删除还是90天后硬删除？
- audit_logs的`request_data`应该用TEXT还是JSON类型？
- 是否应添加数据库级触发器强制业务规则？

---

**下一步：** 等待原设计者回应，讨论修复方案。
