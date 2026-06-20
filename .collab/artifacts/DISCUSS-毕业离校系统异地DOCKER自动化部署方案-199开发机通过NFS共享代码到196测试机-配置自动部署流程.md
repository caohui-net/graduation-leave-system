# 毕业离校系统开发/生产环境拆分方案讨论

**创建时间**: 2026-06-18  
**讨论主题**: 199开发环境 + 196生产环境 架构拆分与自动同步方案  
**状态**: 待讨论

---

## 1. 需求分析

### 1.1 当前架构
```
172.17.12.199 (单机)
├── 开发环境（开发+调试）
└── 生产环境（对外服务）
    ├── 前端: systemd service (端口7788)
    ├── 后端: Docker (端口7787)
    └── 数据库: PostgreSQL Docker
```

### 1.2 目标架构
```
172.17.12.199 (开发机)              172.17.12.196 (生产机)
├── 开发环境                        ├── 生产环境
│   ├── 代码编辑                    │   ├── 前端服务
│   ├── 本地测试                    │   ├── 后端服务
│   └── Git仓库                     │   └── 数据库
└── 代码同步机制 ─────────────────> └── 独立服务管理
```

### 1.3 核心需求
1. **环境隔离**: 开发环境故障不影响生产
2. **代码同步**: 199修改后自动/手动推送到196
3. **服务独立**: 196可独立重启前后端服务
4. **数据隔离**: 开发数据库与生产数据库分离

### 1.4 技术要点
- ✅ 内网环境（172.17.12.0/24网段）
- ✅ Docker部署（容器化易迁移）
- ✅ systemd服务管理（前端）
- ⚠️ 数据库迁移（生产数据需保留）
- ⚠️ 配置差异（端口、域名、密钥）

---

## 2. 技术方案对比

### 2.1 代码同步方案

| 方案 | 实现方式 | 优点 | 缺点 | 推荐度 |
|------|----------|------|------|--------|
| **NFS共享** | 199导出目录，196挂载 | 实时同步，零延迟 | 网络依赖强，199故障影响196 | ⭐⭐ |
| **rsync定时** | cron + rsync | 单向同步，稳定 | 有延迟（cron间隔） | ⭐⭐⭐ |
| **rsync + inotify** | inotifywait监听 + rsync | 准实时，故障隔离 | 需额外监听进程 | ⭐⭐⭐⭐⭐ |
| **Git同步** | 199 push → 196 pull | 版本控制，可回滚 | 手动操作，需Git服务 | ⭐⭐⭐⭐ |
| **CI/CD自动化** | GitHub Actions部署 | 标准化流程，审计日志 | 依赖外部服务 | ⭐⭐⭐⭐⭐ |

### 2.2 服务部署方案

| 组件 | 199开发环境 | 196生产环境 | 说明 |
|------|-------------|-------------|------|
| **前端** | systemd --user | systemd (root级) | 生产用root服务更稳定 |
| **后端** | docker-compose (dev) | docker-compose (prod) | 分离配置文件 |
| **数据库** | PostgreSQL Docker | PostgreSQL Docker | 独立数据卷 |
| **配置** | `.env.dev` | `.env.prod` | 环境变量隔离 |

---

## 3. 推荐方案：rsync + inotify + Git混合模式

### 3.1 方案概述
```
199开发机                          196生产机
├── Git代码仓库                    ├── Git代码仓库
├── inotifywait监听                ├── systemd服务（root级）
│   └── 触发 rsync → 196          └── docker-compose.prod.yml
├── 开发测试环境
└── 手动Git push（重要变更）
```

### 3.2 工作流程
1. **日常开发**: 199编辑代码 → inotify检测 → rsync推送到196 → 196热重载
2. **重要发布**: 199 Git commit → push到远程 → 196 Git pull → 重启服务
3. **紧急回滚**: 196 Git reset + 数据库备份恢复

### 3.3 优势
✅ 准实时同步（inotify延迟<1秒）  
✅ 故障隔离（rsync失败不影响196运行）  
✅ 版本控制（Git提供回滚能力）  
✅ 灵活控制（196可独立管理服务）  
✅ 低成本（无需外部依赖）

---

## 4. 实施方案

### 4.1 网络与权限配置

#### 4.1.1 SSH免密登录（199 → 196）
```bash
# 在199上生成密钥（如未生成）
ssh-keygen -t ed25519 -C "dev-to-prod-sync"

# 复制公钥到196
ssh-copy-id root@172.17.12.196
# 或 ssh-copy-id deploy_user@172.17.12.196

# 测试连接
ssh root@172.17.12.196 "echo 'SSH OK'"
```

#### 4.1.2 防火墙配置（196）
```bash
# 允许199访问196的SSH
sudo ufw allow from 172.17.12.199 to any port 22

# 允许外网访问服务端口
sudo ufw allow 7787/tcp  # 后端API
sudo ufw allow 7788/tcp  # 前端静态
```

---

### 4.2 代码同步配置

#### 4.2.1 rsync脚本（199）
```bash
# /home/caohui/scripts/sync-to-prod.sh
#!/bin/bash
set -e

SOURCE_DIR="/home/caohui/projects/graduation-leave-system"
DEST_HOST="root@172.17.12.196"
DEST_DIR="/opt/graduation-leave-system"

rsync -avz --delete \
  --exclude='.git' \
  --exclude='backend/venv' \
  --exclude='backend/__pycache__' \
  --exclude='backend/*.pyc' \
  --exclude='.env.dev' \
  --exclude='node_modules' \
  --exclude='.claude' \
  --exclude='.omc' \
  --exclude='.wolf' \
  --exclude='.trellis' \
  "$SOURCE_DIR/" "$DEST_HOST:$DEST_DIR/"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Synced to production" >> /tmp/sync-to-prod.log
```

```bash
chmod +x /home/caohui/scripts/sync-to-prod.sh
```

#### 4.2.2 inotify监听服务（199）
```bash
# /home/caohui/.config/systemd/user/sync-to-prod.service
[Unit]
Description=Auto sync code to production server
After=network.target

[Service]
Type=simple
ExecStart=/home/caohui/scripts/sync-to-prod-watch.sh
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
# /home/caohui/scripts/sync-to-prod-watch.sh
#!/bin/bash

SOURCE_DIR="/home/caohui/projects/graduation-leave-system"
SYNC_SCRIPT="/home/caohui/scripts/sync-to-prod.sh"

inotifywait -m -r -e modify,create,delete,move \
  --exclude '\.git|__pycache__|\.pyc$|venv|node_modules|\.claude|\.omc|\.wolf|\.trellis' \
  "$SOURCE_DIR" | while read path action file; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Detected: $action $path$file"
    # 防抖：等待1秒后执行同步（避免频繁触发）
    sleep 1
    "$SYNC_SCRIPT"
done
```

```bash
chmod +x /home/caohui/scripts/sync-to-prod-watch.sh

# 启动监听服务
systemctl --user enable sync-to-prod.service
systemctl --user start sync-to-prod.service

# 查看状态
systemctl --user status sync-to-prod.service
journalctl --user -u sync-to-prod.service -f
```

---

### 4.3 生产环境配置（196）

#### 4.3.1 目录结构
```bash
# 在196上创建目录
sudo mkdir -p /opt/graduation-leave-system
sudo chown -R root:root /opt/graduation-leave-system

# 初始化Git仓库（可选，用于版本控制）
cd /opt/graduation-leave-system
git init
git remote add origin <你的Git仓库地址>
```

#### 4.3.2 生产环境配置文件
```bash
# /opt/graduation-leave-system/.env.prod
DEBUG=False
SECRET_KEY=<生产环境密钥>
DATABASE_URL=postgresql://postgres:prod_password@db:5432/graduation_leave
ALLOWED_HOSTS=172.17.12.196,218.75.196.218
CORS_ALLOWED_ORIGINS=http://172.17.12.196:7788,http://218.75.196.218:7788
```

#### 4.3.3 docker-compose.prod.yml
```yaml
# /opt/graduation-leave-system/docker-compose.prod.yml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: prod-graduation-db
    environment:
      POSTGRES_DB: graduation_leave
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: prod_password
    volumes:
      - prod_postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: prod-graduation-backend
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
    env_file:
      - .env.prod
    volumes:
      - ./backend:/app
      - prod_media_data:/app/media
    ports:
      - "7787:8000"
    depends_on:
      - db
    restart: unless-stopped
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4

volumes:
  prod_postgres_data:
  prod_media_data:
```

#### 4.3.4 前端systemd服务（root级，196）
```bash
# /etc/systemd/system/graduation-frontend-prod.service
[Unit]
Description=Graduation Leave System Frontend (Production)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/graduation-leave-system/demo-web
ExecStart=/usr/bin/python3 -m http.server 7788 --bind 0.0.0.0
Restart=always
RestartSec=10

# 日志
StandardOutput=append:/var/log/graduation-frontend.log
StandardError=append:/var/log/graduation-frontend-error.log

[Install]
WantedBy=multi-user.target
```

```bash
# 启动生产服务
sudo systemctl daemon-reload
sudo systemctl enable graduation-frontend-prod.service
sudo systemctl start graduation-frontend-prod.service

# 启动后端
cd /opt/graduation-leave-system
sudo docker-compose -f docker-compose.prod.yml up -d
```

---

### 4.4 服务管理脚本（196）

#### 4.4.1 一键重启脚本
```bash
# /opt/graduation-leave-system/scripts/restart-services.sh
#!/bin/bash
set -e

echo "=== Restarting Production Services ==="

# 重启前端
echo "[1/3] Restarting frontend..."
sudo systemctl restart graduation-frontend-prod.service

# 重启后端
echo "[2/3] Restarting backend..."
cd /opt/graduation-leave-system
sudo docker-compose -f docker-compose.prod.yml restart backend

# 健康检查
echo "[3/3] Health check..."
sleep 5
curl -f http://localhost:7787/readyz || echo "Backend health check failed"
curl -f http://localhost:7788/ || echo "Frontend health check failed"

echo "=== Services restarted successfully ==="
```

```bash
sudo chmod +x /opt/graduation-leave-system/scripts/restart-services.sh
```

#### 4.4.2 状态检查脚本
```bash
# /opt/graduation-leave-system/scripts/check-status.sh
#!/bin/bash

echo "=== Production Service Status ==="
echo ""
echo "Frontend:"
sudo systemctl status graduation-frontend-prod.service --no-pager | head -5
echo ""
echo "Backend:"
sudo docker-compose -f /opt/graduation-leave-system/docker-compose.prod.yml ps
echo ""
echo "Database:"
sudo docker exec prod-graduation-db pg_isready -U postgres
```

```bash
sudo chmod +x /opt/graduation-leave-system/scripts/check-status.sh
```

---

### 4.5 数据库迁移

#### 4.5.1 备份199数据库
```bash
# 在199上执行
docker exec graduation-leave-system-db-1 \
  pg_dump -U postgres graduation_leave | gzip > /tmp/graduation_db_backup_$(date +%Y%m%d).sql.gz
```

#### 4.5.2 导入到196
```bash
# 复制备份文件到196
scp /tmp/graduation_db_backup_*.sql.gz root@172.17.12.196:/tmp/

# 在196上导入
gunzip -c /tmp/graduation_db_backup_*.sql.gz | \
  sudo docker exec -i prod-graduation-db psql -U postgres graduation_leave
```

---

### 4.6 CI/CD调整（可选）

#### 4.6.1 更新 .github/workflows/deploy.yml
```yaml
# 修改部署目标为196
env:
  DEPLOY_USER: root
  DEPLOY_HOST: 172.17.12.196  # 改为生产机IP
  DEPLOY_PATH: /opt/graduation-leave-system

# ... 其余配置不变
```

#### 4.6.2 Git Push触发部署（199）
```bash
# 在199上配置git hooks（可选）
# /home/caohui/projects/graduation-leave-system/.git/hooks/post-commit
#!/bin/bash
echo "Code committed, syncing to production..."
/home/caohui/scripts/sync-to-prod.sh
```

---

## 5. 实施步骤清单

### 阶段1：准备工作（预计30分钟）
- [ ] 备份199生产数据库
- [ ] 备份199代码和配置
- [ ] 在196创建目录结构
- [ ] 配置199→196 SSH免密登录
- [ ] 配置196防火墙规则

### 阶段2：代码同步（预计20分钟）
- [ ] 在199创建rsync同步脚本
- [ ] 在199创建inotify监听脚本
- [ ] 在199配置systemd同步服务
- [ ] 手动测试同步（rsync一次）

### 阶段3：生产环境部署（预计40分钟）
- [ ] 在196创建 .env.prod 配置
- [ ] 在196创建 docker-compose.prod.yml
- [ ] 在196导入数据库备份
- [ ] 在196启动Docker服务
- [ ] 在196配置前端systemd服务
- [ ] 验证服务可访问（内网+外网）

### 阶段4：自动化配置（预计20分钟）
- [ ] 在196创建服务管理脚本
- [ ] 在199启动inotify监听服务
- [ ] 测试代码修改自动同步
- [ ] 测试196独立重启服务

### 阶段5：验证与优化（预计30分钟）
- [ ] 功能测试（登录、申请、审批、附件）
- [ ] 性能测试（并发访问）
- [ ] 日志检查（前端/后端/同步日志）
- [ ] 文档更新（PROJECT-QUICK-REF.md）

---

## 6. 风险与应对

| 风险 | 影响 | 概率 | 应对措施 |
|------|------|------|----------|
| **同步失败** | 196代码滞后 | 中 | 监听日志告警 + 手动Git pull备用 |
| **数据库迁移失败** | 生产数据丢失 | 低 | 多重备份 + 迁移前验证 |
| **网络中断** | 同步中断 | 低 | rsync自动重连 + 告警通知 |
| **端口冲突** | 服务启动失败 | 低 | 修改配置文件端口映射 |
| **配置错误** | 服务异常 | 中 | 配置模板 + 健康检查脚本 |

---

## 7. 后续优化建议

### 7.1 监控告警
- 在196部署Prometheus + Grafana监控
- 配置服务异常告警（邮件/企业微信）
- 监控同步日志，检测同步失败

### 7.2 备份策略
- 自动化数据库每日备份（cron + pg_dump）
- 保留最近7天备份
- 异地备份（上传到对象存储）

### 7.3 负载均衡
- 如需高可用，可在196前加Nginx反向代理
- 配置多个后端实例（docker-compose scale）

### 7.4 灰度发布
- 先同步到196测试环境验证
- 验证通过后再切换生产流量

---

## 8. 成本与收益

### 8.1 实施成本
- **时间成本**: 约2-3小时（一次性）
- **硬件成本**: 0（利用现有服务器）
- **维护成本**: 低（自动化同步，偶尔检查日志）

### 8.2 预期收益
- ✅ 环境隔离：开发故障不影响生产
- ✅ 快速迭代：代码修改准实时生效
- ✅ 独立管理：196可独立重启服务
- ✅ 版本控制：Git提供回滚能力
- ✅ 扩展性：后续可接入CI/CD流程

---

## 9. 讨论记录

### 9.1 待讨论问题
1. **同步频率**: inotify实时 vs cron定时？
2. **权限设计**: 196用root还是创建deploy用户？
3. **数据库策略**: 是否需要主从复制？
4. **回滚机制**: Git reset还是保留多版本？
5. **测试环境**: 是否在196额外部署测试环境？

### 9.2 决策记录
（待团队讨论后填写）

---

## 10. 参考文档

- PROJECT-QUICK-REF.md - 项目环境配置
- .github/workflows/deploy.yml - 当前CI/CD配置
- docker-compose.yml - Docker部署配置
- deploy.config.yml - 部署环境配置

---

**文档状态**: 初稿完成，待团队评审  
**下一步**: 团队讨论 → 修订方案 → 实施验证  
**负责人**: （待指定）  
**预计完成时间**: 讨论通过后1个工作日内完成迁移
