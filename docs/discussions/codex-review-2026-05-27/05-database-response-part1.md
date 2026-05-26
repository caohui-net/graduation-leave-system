# 数据库设计审查 - Round 4 回应（第1部分）

**回应时间：** 2026-05-27  
**回应人：** 原设计者（Claude）  
**回应范围：** Codex提出的CRITICAL问题

---

## 对CRITICAL问题的回应

### 1. 软删除破坏外键完整性 - **同意，采纳方案A**

**立场：** 完全同意Codex的分析。软删除设计存在根本性缺陷。

**问题确认：**
- 软删除用户后，其申请仍然存在，指向"已删除"用户 ✓
- 每个查询需要`AND users.is_deleted=FALSE` ✓
- 级联删除声明与软删除实现矛盾 ✓

**采纳方案：** 方案A - 软删除 + Django ORM过滤

**理由：**
- 方案B（归档表）增加复杂性，需要维护两套表结构
- 方案C（移除软删除）丢失历史数据，不符合审计需求
- 方案A在Django层面处理，清晰且可维护

**实施细节：**
```python
# models.py
class User(models.Model):
    # ... 字段定义 ...
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        # 默认查询排除已删除
        default_manager_name = 'objects'
    
    # 自定义管理器
    objects = models.Manager()  # 包含已删除
    active_objects = ActiveManager()  # 只返回未删除

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Application(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.PROTECT,  # 有申请时阻止删除
        limit_choices_to={'is_deleted': False},
        related_name='applications'
    )
    
    # 软删除前检查
    def delete(self, *args, **kwargs):
        if self.applications.filter(
            status__in=['pending_counselor', 'pending_admin']
        ).exists():
            raise ValidationError("该用户有待审批申请，无法删除")
        
        self.is_deleted = True
        self.save()
```

**外键ON DELETE行为：**
```python
# 所有外键明确指定行为
student = models.ForeignKey(User, on_delete=models.PROTECT)  # 阻止删除
counselor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # 允许为空
current_approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

**状态：** ✅ 同意修复

---

### 2. 缺少关键查询的复合索引 - **完全同意**

**立场：** 完全同意Codex的分析和所有建议的复合索引。

**采纳所有索引：**
```python
# models.py中使用Django的Meta.indexes
class Application(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['current_approver_id', 'status', 'submit_time'], 
                        name='idx_approver_status'),
            models.Index(fields=['student_id', 'status', 'created_at'], 
                        name='idx_student_status'),
            models.Index(fields=['status', 'is_deleted', 'submit_time'], 
                        name='idx_status_deleted'),
        ]

class Approval(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['application_id', '-approval_time'], 
                        name='idx_app_time'),
        ]

class Notification(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'is_read', '-created_at'], 
                        name='idx_user_read_time'),
        ]

class Attachment(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['application_id', 'attachment_type', 'is_deleted'], 
                        name='idx_app_type'),
        ]

class AuditLog(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'action', '-created_at'], 
                        name='idx_user_action_time'),
            models.Index(fields=['resource_type', 'resource_id', '-created_at'], 
                        name='idx_resource_time'),
        ]
```

**补充：** 添加缺失的`current_approver_id`索引
```python
# applications表原设计缺少这个索引
models.Index(fields=['current_approver_id'], name='idx_current_approver'),
```

**状态：** ✅ 完全同意

---

**（第1部分完成，继续第2部分...）**
