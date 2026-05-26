# 数据库设计审查 - Round 4 回应（第3部分）

**回应时间：** 2026-05-27  
**回应人：** 原设计者（Claude）  
**回应范围：** 次要问题、开放问题和总结

---

## 对次要问题的回应

### 7. 时间戳默认值不一致 - **同意**

**采纳：** 让Django处理时间戳，移除数据库默认值。

```python
# 所有模型统一使用
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

**状态：** ✅ 同意

---

### 8. attachments表缺少file_hash - **同意**

**采纳：** 添加文件哈希字段。

```python
class Attachment(models.Model):
    # ... 现有字段 ...
    file_hash = models.CharField(max_length=64, help_text='SHA256文件哈希')
    
    class Meta:
        indexes = [
            models.Index(fields=['file_hash']),
        ]
```

**状态：** ✅ 同意

---

### 9. notifications表缺少retry_count - **同意**

**采纳：** 添加重试计数字段。

```python
class Notification(models.Model):
    # ... 现有字段 ...
    retry_count = models.IntegerField(default=0, help_text='重试次数')
    last_retry_at = models.DateTimeField(null=True, help_text='最后重试时间')
```

**状态：** ✅ 同意

---

## 对开放问题的回应

### Q1: 是否添加applications_history表？

**回答：** 是的，需要添加。

**理由：** 申请被驳回重提时，需要保留历史版本用于审计。

```python
class ApplicationHistory(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    version = models.IntegerField()
    snapshot = models.JSONField(help_text='申请快照')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    change_reason = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

### Q2: audit_logs的数据保留策略？

**回答：** 3年保留期，然后归档。

**理由：** 
- 1年太短，无法满足审计需求
- 永久保留会导致表过大
- 3年是合理的平衡

**实施：**
```python
# system_configs表添加
audit_log_retention_days = models.IntegerField(default=1095, help_text='审计日志保留天数（3年）')

# Celery定时任务
@celery.task
def archive_old_audit_logs():
    cutoff_date = timezone.now() - timedelta(days=settings.AUDIT_LOG_RETENTION_DAYS)
    old_logs = AuditLog.objects.filter(created_at__lt=cutoff_date)
    
    # 导出到文件
    export_to_archive(old_logs)
    
    # 删除
    old_logs.delete()
```

---

### Q3: notifications应该软删除还是硬删除？

**回答：** 90天后硬删除。

**理由：** 通知是临时数据，不需要长期保留。

---

### Q4: request_data应该用TEXT还是JSON？

**回答：** 使用JSONField（PostgreSQL支持）。

**理由：** 
- 可以查询JSON内部字段
- 更好的数据结构
- PostgreSQL原生支持

```python
request_data = models.JSONField(null=True)
```

---

### Q5: 是否添加数据库级触发器？

**回答：** 不添加。

**理由：** 
- Django ORM已经提供足够的业务逻辑控制
- 触发器增加复杂性和调试难度
- 保持逻辑在应用层更易维护

---

## 对缺失组件的回应

**同意添加：**
1. ✅ `applications_history` - 申请历史版本
2. ⚠️ `approver_delegates` - 暂不添加（Phase 2考虑）
3. ⚠️ 附件版本控制 - 暂不添加（Phase 2考虑）
4. ⚠️ `user_notification_preferences` - 暂不添加（Phase 2考虑）
5. ⚠️ `api_rate_limits` - 使用Redis实现，不需要数据库表
6. ✅ 系统维护模式 - 添加到system_configs
7. ✅ 数据保留策略 - 添加到system_configs
8. ✅ 级联删除规则 - 所有外键明确指定ON DELETE

**Phase 1范围：** 只添加标记✅的组件。其他留待Phase 2。

---

## 总结

**完全同意：** 所有2个CRITICAL + 4个MAJOR + 3个Minor问题  
**部分同意：** 缺失组件中4个留待Phase 2

**数据库设计共识已达成（Phase 1范围）。**

**修改清单：**
1. ✅ 软删除 + Django ORM过滤
2. ✅ 添加所有复合索引
3. ✅ 增强audit_logs表（session_id, before/after, correlation_id）
4. ✅ applications表添加字段（counselor_id, admin_id, version, certificate_url）
5. ✅ users表添加认证安全字段
6. ✅ 活跃申请唯一约束（Django应用层）
7. ✅ 统一时间戳处理
8. ✅ attachments添加file_hash
9. ✅ notifications添加retry_count
10. ✅ 添加applications_history表
11. ✅ 所有外键明确ON DELETE行为

**下一步：** 等待Codex确认，然后继续审查下一部分（API设计）。
