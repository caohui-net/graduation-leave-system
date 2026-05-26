# 设计审查共识总结

**审查时间：** 2026-05-27  
**审查人：** Claude + Codex  
**审查范围：** 系统架构、认证授权、数据库设计、外部系统集成

---

## 审查结论

**所有审查部分已达成共识，可以进入实施阶段。**

---

## 第1部分：系统架构修改（6项）

### 1.1 多数据库支持 → 外部数据库对接

**原设计：** 本项目支持运行在多种数据库上（MySQL/PostgreSQL/SQL Server/Oracle）

**修改后：**
- 本项目使用单一数据库：**PostgreSQL**
- 对接外部系统的多种数据库（宿舍管理系统等）
- 推荐方案：API对接 > SQLAlchemy > Django多DB
- system_configs存储外部数据库连接信息（加密）

### 1.2 架构扩展性

**原设计：** 3个Django副本，水平扩展

**修改后：**
- 单实例部署（校园系统无需水平扩展）
- 移除docker-compose中的`deploy.replicas: 3`
- 文件存储使用本地文件系统（不需要MinIO）

### 1.3 API安全

**新增：**
- Django REST Framework throttling
- Nginx速率限制
- 登录：5次/分钟
- 上传：10次/小时
- 普通API：1000次/小时

### 1.4 文件上传安全

**新增：**
- python-magic MIME类型验证
- 文件名清理（防止路径遍历）
- 文件哈希去重
- 大小限制：10MB

### 1.5 审批超时监控

**修改：**
- 使用chinese_calendar库计算工作日
- 排除周末和节假日
- 工作时间：9:00-17:00
- 升级通知机制

### 1.6 部署架构

**修改：**
- 单Django实例 + Gunicorn(4 workers)
- 本地文件存储
- 峰值负载：500并发用户

---

## 第2部分：认证授权修改（5项强制性安全增强）

### 2.1 学生身份验证

**新增：** 微信新用户必须验证学生身份
- 方案A：短信验证到注册手机
- 方案B：邮件验证到学生邮箱
- 方案C：上传学生证照片人工审核

### 2.2 受限Token范围

**新增：** 不完整账户使用受限token
```python
{
    'user_id': user.id,
    'scope': 'password_setup_only',  # 只能设置密码
    'exp': datetime.utcnow() + timedelta(hours=1)
}
```

### 2.3 事务锁

**新增：** 微信绑定操作使用数据库锁
```python
with transaction.atomic():
    existing_user = User.objects.select_for_update().filter(
        student_id=student_id
    ).first()
```

### 2.4 审计日志

**新增：** 所有绑定操作记录到audit_logs
```python
AuditLog.objects.create(
    action='wechat_bind',
    resource_type='user',
    ip_address=request.META.get('REMOTE_ADDR')
)
```

### 2.5 通用错误消息

**新增：** 防止学号枚举攻击
```python
# 所有绑定失败返回相同消息
raise ValidationError("绑定失败，请联系管理员")
```

---

## 第3部分：数据库设计修改（11项）

### 3.1 软删除策略

**修改：** Django ORM过滤 + PROTECT外键
```python
class User(models.Model):
    is_deleted = models.BooleanField(default=False)
    objects = models.Manager()
    active_objects = ActiveManager()

class Application(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        limit_choices_to={'is_deleted': False}
    )
```

### 3.2 复合索引（6组）

**新增：**
```python
# applications表
Index(fields=['current_approver_id', 'status', 'submit_time'])
Index(fields=['student_id', 'status', 'created_at'])
Index(fields=['status', 'is_deleted', 'submit_time'])

# approvals表
Index(fields=['application_id', '-approval_time'])

# notifications表
Index(fields=['user_id', 'is_read', '-created_at'])

# attachments表
Index(fields=['application_id', 'attachment_type', 'is_deleted'])

# audit_logs表
Index(fields=['user_id', 'action', '-created_at'])
Index(fields=['resource_type', 'resource_id', '-created_at'])
```

### 3.3 audit_logs表增强

**新增字段：**
- session_id VARCHAR(100)
- correlation_id VARCHAR(100)
- field_name VARCHAR(100)
- old_value TEXT
- new_value TEXT

### 3.4 applications表新增字段

**新增：**
- counselor_id BIGINT（固定辅导员ID）
- admin_id BIGINT（固定学工部管理员ID）
- version INT DEFAULT 0（乐观锁）
- certificate_url VARCHAR(500)（离校凭证URL）
- certificate_generated_at TIMESTAMP

### 3.5 users表新增安全字段

**新增：**
- password_setup_required BOOLEAN
- account_locked BOOLEAN
- failed_login_attempts INT
- last_login_at TIMESTAMP
- last_login_ip VARCHAR(50)
- wechat_bind_time TIMESTAMP
- password_changed_at TIMESTAMP

**新增约束：**
```sql
CONSTRAINT chk_auth_method CHECK (
    (password_hash IS NOT NULL) OR (wechat_openid IS NOT NULL)
)
```

### 3.6 活跃申请唯一约束

**新增：** Django应用层验证
```python
def save(self, *args, **kwargs):
    if self.status in ['draft', 'pending_counselor', 'pending_admin']:
        existing = Application.objects.filter(
            student_id=self.student_id,
            status__in=['draft', 'pending_counselor', 'pending_admin'],
            is_deleted=False
        ).exclude(id=self.id)
        
        if existing.exists():
            raise ValidationError("您已有进行中的申请，请等待审批完成")
```

### 3.7 时间戳统一处理

**修改：** 所有模型使用Django auto_now
```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

### 3.8 attachments表新增file_hash

**新增：**
```python
file_hash = models.CharField(max_length=64, help_text='SHA256文件哈希')
```

### 3.9 notifications表新增retry_count

**新增：**
```python
retry_count = models.IntegerField(default=0)
last_retry_at = models.DateTimeField(null=True)
```

### 3.10 applications_history表

**新增表：**
```python
class ApplicationHistory(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    version = models.IntegerField()
    snapshot = models.JSONField()
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    change_reason = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
```

### 3.11 外键ON DELETE行为

**修改：** 所有外键明确指定行为
```python
student = models.ForeignKey(User, on_delete=models.PROTECT)
counselor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
current_approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

---

## 第4部分：外部系统集成修改

### 4.1 集成策略

**新增：** API优先，数据库备选
- 优先：REST API对接
- 备选：SQLAlchemy直连（只读）
- 避免：Django多数据库

### 4.2 配置存储

**新增：** system_configs存储集成配置
```sql
-- API集成
('dorm_integration_type', 'api', 'integration', FALSE)
('dorm_api_url', 'https://dorm.edu/api', 'integration', FALSE)
('dorm_api_key', 'encrypted_key', 'integration', TRUE)

-- 数据库集成
('dorm_integration_type', 'database', 'integration', FALSE)
('dorm_db_config', '{"type":"mysql",...}', 'integration', TRUE)
```

### 4.3 安全要求

**新增：**
1. 所有凭证使用Fernet加密
2. 加密密钥存储在环境变量
3. 只读数据库访问
4. 查询超时：5秒
5. 连接池：最大5连接
6. 所有查询记录到audit_logs

---

## 实施优先级

**Phase 1（必需）：**
- ✅ 所有架构修改
- ✅ 所有认证安全增强
- ✅ 所有数据库修改
- ✅ API对接实现
- ✅ applications_history表
- ✅ 系统维护模式
- ✅ 数据保留策略

**Phase 2（可选）：**
- ⏸ approver_delegates表
- ⏸ 附件版本控制
- ⏸ user_notification_preferences表
- ⏸ SQLAlchemy数据库对接

---

## 下一步行动

1. ✅ 更新系统设计文档（应用所有修改）
2. ✅ 更新实施计划（反映新的技术方案）
3. ✅ 提交所有变更
4. ⏸ 开始Phase 1实施

---

**文档状态：** 共识已达成，准备更新设计文档
