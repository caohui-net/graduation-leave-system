# 生产环境部署指南

## 快速部署

### 1. 准备生产配置

```bash
# 复制生产环境配置模板
cp .env.prod.example .env.prod

# 生成安全密钥
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 编辑 .env.prod 填入：
# - DJANGO_SECRET_KEY（上一步生成）
# - JWT_SECRET（任意强密码）
# - DB_PASSWORD（数据库密码）
# - ALLOWED_HOSTS（你的域名）
# - QGL_* （青橄榄SSO凭证）
```

### 2. 启动生产环境

```bash
# 使用生产配置启动
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d

# 初始化数据库
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput

# 创建管理员
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

### 3. 验证部署

```bash
# 检查服务状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f backend

# 健康检查
curl http://localhost:7787/api/applications/
```

## 生产环境优化

### Gunicorn配置（已集成）

```bash
# docker-compose.prod.yml 使用 Gunicorn
command: gunicorn backend.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \          # CPU核心数 * 2 + 1
  --threads 2 \          # 每个worker线程数
  --timeout 60 \         # 请求超时
  --access-logfile - \   # 访问日志输出到stdout
  --error-logfile -      # 错误日志输出到stderr
```

### 资源限制

```yaml
deploy:
  resources:
    limits:
      memory: 2G      # 最大内存
    reservations:
      memory: 512M    # 保留内存
```

### 健康检查

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/api/applications/"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## 性能测试

```bash
# 运行性能测试
chmod +x scripts/performance_test.sh
./scripts/performance_test.sh

# 并发测试（需要apache2-utils）
sudo apt install apache2-utils
ab -n 1000 -c 50 http://localhost:7787/api/applications/
```

## 监控与日志

### 查看实时日志
```bash
docker-compose -f docker-compose.prod.yml logs -f --tail=100 backend
```

### 数据库慢查询监控
```bash
# 已启用慢查询日志（>200ms）
docker-compose -f docker-compose.prod.yml logs db | grep "duration:"
```

## 备份策略

### 数据库备份
```bash
# 备份
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres graduation_leave > backup_$(date +%Y%m%d).sql

# 恢复
docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres graduation_leave < backup_20260612.sql
```

### 媒体文件备份
```bash
# 备份上传文件
tar -czf media_backup_$(date +%Y%m%d).tar.gz -C backend media/
```

## 安全清单

- ✅ DEBUG=False
- ✅ SECRET_KEY随机生成
- ✅ 数据库强密码
- ✅ ALLOWED_HOSTS限制域名
- ✅ CORS配置正确
- ✅ Gunicorn多worker
- ✅ 资源限制配置
- ✅ 健康检查启用
- ⚠️ HTTPS配置（需反向代理）
- ⚠️ 日志收集系统（可选）

## 故障排查

### 容器无法启动
```bash
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml exec backend python manage.py check
```

### 数据库连接失败
```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py dbshell
```

### 性能问题
```bash
# 查看资源使用
docker stats

# 查看慢查询
docker-compose -f docker-compose.prod.yml logs db | grep "duration:" | grep -v "duration: 0"
```

## 更新部署

```bash
# 拉取最新代码
git pull

# 重新构建镜像
docker-compose -f docker-compose.prod.yml build backend

# 应用数据库迁移
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# 重启服务
docker-compose -f docker-compose.prod.yml restart backend
```
