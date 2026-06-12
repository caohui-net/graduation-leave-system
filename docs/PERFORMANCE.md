# 数据库性能优化指南

## 连接池配置

已在 `.env.prod.example` 中启用：
```
CONN_MAX_AGE=600  # 连接保持10分钟
```

## 关键索引检查

```sql
-- 检查现有索引
SELECT tablename, indexname, indexdef 
FROM pg_indexes 
WHERE schemaname = 'public' 
ORDER BY tablename, indexname;

-- 推荐添加的索引（如未自动创建）
CREATE INDEX CONCURRENTLY idx_applications_student_id ON applications(student_id);
CREATE INDEX CONCURRENTLY idx_applications_status ON applications(status);
CREATE INDEX CONCURRENTLY idx_applications_created_at ON applications(created_at DESC);
CREATE INDEX CONCURRENTLY idx_approvals_approver ON approvals(approver_id);
CREATE INDEX CONCURRENTLY idx_approvals_decision ON approvals(decision);
CREATE INDEX CONCURRENTLY idx_approvals_created_at ON approvals(created_at DESC);
```

## 查询优化

### 1. 使用select_related减少查询
```python
# 优化前：N+1查询
approvals = Approval.objects.all()
for approval in approvals:
    print(approval.application.student_name)  # 每次额外查询

# 优化后：JOIN查询
approvals = Approval.objects.select_related('application', 'approver').all()
```

### 2. 批量操作使用bulk_create
```python
# 避免循环save
Approval.objects.bulk_create([...])
```

### 3. 分页查询限制
```python
# 默认限制20条，最大100条
limit = min(int(request.GET.get('limit', 20)), 100)
```

## 性能监控

### 开启慢查询日志
```bash
# docker-compose.prod.yml 添加
services:
  db:
    command: postgres -c log_min_duration_statement=200
```

### Django Debug Toolbar（开发环境）
```bash
pip install django-debug-toolbar
# 查看SQL查询数量和执行时间
```

## 缓存策略（未来优化）

```python
# Redis缓存审批统计
from django.core.cache import cache

def get_statistics(request):
    cache_key = f'approval_stats_{user.user_id}'
    stats = cache.get(cache_key)
    if not stats:
        stats = calculate_statistics()
        cache.set(cache_key, stats, 300)  # 5分钟
    return stats
```

## 性能基准

- API响应时间：< 200ms
- 数据库查询：< 50ms
- 并发支持：100 req/s
- 内存使用：< 512MB（backend）
