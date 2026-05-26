# 数据库设计审查 - Round 4 回应（第2部分）

**回应时间：** 2026-05-27  
**回应人：** 原设计者（Claude）  
**回应范围：** Codex提出的MAJOR问题

---

## 对MAJOR问题的回应

### 3. 审计日志表缺少关键字段 - **完全同意**

**立场：** 完全同意Codex的分析。审计日志需要增强。

**采纳所有建议字段：**
```python
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)  # 改为必需
    session_id = models.CharField(max_length=100, null=True)  # 新增
    correlation_id = models.CharField(max_length=100, null=True)  # 新增
    action = models.CharField(max_length=50)
    resource_type = models.CharField(max_length=50)
    resource_id = models.BigIntegerField(null=True)
    
    # 新增变更追踪
    field_name = models.CharField(max_length=100, null=True)
    old_value = models.TextField(null=True)
    new_value = models.TextField(null=True)
    
    ip_address = models.CharField(max_length=50, null=True)
    user_agent = models.TextField(null=True)
    request_data = models.TextField(null=True)
    response_status = models.IntegerField(null=True)
    error_message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['session_id']),
            models.Index(fields=['correlation_id']),
            models.Index(fields=['action']),
            models.Index(fields=['resource_type', 'resource_id']),
            models.Index(fields=['-created_at']),
        ]
```

**状态：** ✅ 完全同意

---

### 4. applications表缺少关键字段 - **完全同意**

**立场：** 完全同意所有缺失字段。

**采纳所有建议：**
```python
class Application(models.Model):
    # 现有字段
    application_no = models.CharField(max_length=50, unique=True)
    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='applications')
    
    # 新增：固定审批人追踪
    counselor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='counselor_applications',
        help_text='辅导员ID'
    )
    admin = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='admin_applications',
        help_text='学工部管理员ID'
    )
    
    planned_leave_date = models.DateField()
    status = models.CharField(max_length=20)
    current_approver = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='pending_applications'
    )
    
    submit_time = models.DateTimeField(null=True)
    complete_time = models.DateTimeField(null=True)
    reject_reason = models.TextField(null=True)
    remarks = models.TextField(null=True)
    
    # 新增：凭证追踪
    certificate_url = models.CharField(max_length=500, null=True, help_text='离校凭证URL')
    certificate_generated_at = models.DateTimeField(null=True, help_text='凭证生成时间')
    
    # 新增：乐观锁
    version = models.IntegerField(default=0, help_text='版本号')
    
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['counselor_id']),
            models.Index(fields=['admin_id']),
            models.Index(fields=['status']),
            models.Index(fields=['application_no']),
            models.Index(fields=['planned_leave_date']),
        ]
```

**乐观锁实现：**
```python
def save(self, *args, **kwargs):
    if self.pk:  # 更新操作
        # 检查版本号
        current = Application.objects.get(pk=self.pk)
        if current.version != self.version:
            raise ValidationError("数据已被其他用户修改，请刷新后重试")
        self.version += 1
    super().save(*args, **kwargs)
```

**状态：** ✅ 完全同意

---

### 5. users表缺少认证安全字段 - **完全同意**

**立场：** 完全同意。这些字段是Round 1-3认证改进的必需部分。

**采纳所有建议：**
```python
class User(AbstractUser):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=255, null=True)
    wechat_openid = models.CharField(max_length=100, unique=True, null=True)
    
    # 新增：认证安全字段
    password_setup_required = models.BooleanField(default=False, help_text='需要设置密码')
    account_locked = models.BooleanField(default=False, help_text='账户锁定')
    failed_login_attempts = models.IntegerField(default=0, help_text='失败登录次数')
    last_login_at = models.DateTimeField(null=True, help_text='最后登录时间')
    last_login_ip = models.CharField(max_length=50, null=True, help_text='最后登录IP')
    wechat_bind_time = models.DateTimeField(null=True, help_text='微信绑定时间')
    password_changed_at = models.DateTimeField(null=True, help_text='密码修改时间')
    
    phone = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=100, null=True)
    role = models.CharField(max_length=20)
    department = models.CharField(max_length=100, null=True)
    major = models.CharField(max_length=100, null=True)
    class_name = models.CharField(max_length=50, null=True)
    grade = models.IntegerField(null=True)
    
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['role']),
            models.Index(fields=['wechat_openid']),
            models.Index(fields=['account_locked']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(password_hash__isnull=False) | models.Q(wechat_openid__isnull=False),
                name='chk_auth_method'
            )
        ]
```

**状态：** ✅ 完全同意

---

### 6. 缺少活跃申请的唯一约束 - **同意，采纳Django应用层方案**

**立场：** 同意需要约束。采纳Django应用层实现（MySQL不支持部分唯一索引）。

**实施：**
```python
class Application(models.Model):
    # ... 字段定义 ...
    
    def save(self, *args, **kwargs):
        # 检查活跃申请唯一性
        if self.status in ['draft', 'pending_counselor', 'pending_admin']:
            existing = Application.objects.filter(
                student_id=self.student_id,
                status__in=['draft', 'pending_counselor', 'pending_admin'],
                is_deleted=False
            ).exclude(id=self.id)
            
            if existing.exists():
                raise ValidationError("您已有进行中的申请，请等待审批完成")
        
        # 乐观锁检查
        if self.pk:
            current = Application.objects.get(pk=self.pk)
            if current.version != self.version:
                raise ValidationError("数据已被其他用户修改，请刷新后重试")
            self.version += 1
        
        super().save(*args, **kwargs)
```

**补充：** 如果未来迁移到PostgreSQL，可以添加数据库级约束：
```sql
CREATE UNIQUE INDEX idx_student_active_application 
ON applications(student_id) 
WHERE status IN ('draft', 'pending_counselor', 'pending_admin') 
  AND is_deleted = FALSE;
```

**状态：** ✅ 同意修复

---

**（第2部分完成，继续第3部分...）**
