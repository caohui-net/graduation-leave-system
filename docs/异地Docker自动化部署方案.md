# 异地Docker自动化部署方案

**项目：** 毕业离校系统  
**场景：** 199开发机 → 196测试机自动化部署  
**方案版本：** v2.0  
**制定日期：** 2026-06-14  
**更新日期：** 2026-06-14 (修正IP地址，改用rsync选择性同步)

---

## 一、方案概述

### 1.1 部署架构

```
┌─────────────────────────────────────────────────────────────┐
│ 199开发机 (172.17.12.199)                                    │
│ ┌──────────────┐      Git Push/File Change                  │
│ │  代码仓库     │ ─────────────┐                             │
│ │  完整项目     │               │                             │
│ │  +文档/调试   │               ▼                             │
│ └──────────────┘    deployment/deploy-trigger.sh            │
│                     - rsync选择性同步运行时代码              │
│                     - 排除.git/docs/screenshots等            │
│                     - SSH触发196部署                         │
│                                │                             │
│                                │ rsync + SSH                 │
│                                ▼                             │
└─────────────────────────────────┼───────────────────────────┘
                                  │
┌─────────────────────────────────┼───────────────────────────┐
│ 196测试机 (172.17.12.196)       │                            │
│                                ▼                             │
│              /opt/graduation/code/                           │
│              ├── backend/      (运行时代码)                  │
│              ├── demo-web/     (运行时代码)                  │
│              ├── nginx.conf                                  │
│              └── docker-compose.yml                          │
│                                                              │
│ ┌──────────────────────────────────────┐                    │
│ │  /opt/deploy/redeploy.sh              │                    │
│ │  - docker compose down                │                    │
│ │  - docker compose build               │                    │
│ │  - docker compose up -d               │                    │
│ └──────────────────────────────────────┘                    │
│                                                              │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│ │ Backend容器   │  │ Frontend容器  │  │ Nginx容器     │      │
│ │ (本地代码)    │  │ (本地代码)    │  │              │      │
│ └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│ ┌──────────────┐  ┌──────────────┐                         │
│ │ PostgreSQL    │  │ Redis         │  (本地存储)            │
│ └──────────────┘  └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 核心原则

1. **rsync选择性同步** - 仅同步运行时代码到196，排除调试/文档/Git历史
2. **SSH主动推送触发** - 199通知196，不依赖文件监控
3. **代码分离** - 199保留完整项目，196仅部署必要文件
4. **状态数据本地化** - 数据库/Redis在196本地存储

### 1.3 同步内容划分

**199保留（完整项目）：**
- `.git/` - Git提交历史
- `docs/` - 项目文档
- `PRD/` - 需求文档
- `.collab/`, `.wolf/` - 协作记录
- `screenshots/` - 截图
- 调试日志、临时文件

**同步到196（运行时）：**
- `backend/` - 后端代码
- `demo-web/` - 前端代码  
- `nginx.conf` - Nginx配置
- `docker-compose.yml` - 容器编排
- `requirements.txt`, `package.json` - 依赖清单

---

## 二、前置准备

### 2.1 SSH免密登录配置

```bash
# 199机器生成SSH密钥（如未生成）
ssh-keygen -t ed25519 -C "deploy@199"

# 复制公钥到196
ssh-copy-id deploy@172.17.12.196

# 测试免密登录
ssh deploy@172.17.12.196 'echo "SSH连接成功"'
```

### 2.2 196机器目录准备

```bash
# 196机器执行
sudo mkdir -p /opt/graduation/{code,data/{postgres,redis},logs/backend}
sudo useradd -m -s /bin/bash deploy  # 如用户不存在
sudo chown -R deploy:deploy /opt/graduation

# 验证
ls -la /opt/graduation
```

### 2.3 rsync安装

```bash
# 两台机器都需安装rsync
sudo apt update
sudo apt install rsync -y

# 验证
rsync --version
```

---

## 三、部署脚本实现

### 3.1 196测试机部署脚本（/opt/deploy/redeploy.sh）

```bash
#!/bin/bash
set -e

# 配置
CODE_DIR="/opt/graduation/code"
LOG_FILE="/var/log/graduation-deploy.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "==================== 开始部署 ===================="

# 1. 检查代码目录
if [ ! -d "$CODE_DIR" ]; then
    log "错误: 代码目录不存在: $CODE_DIR"
    exit 1
fi

# 2. 切换到项目目录
cd "$CODE_DIR"
log "当前目录: $(pwd)"

# 3. 停止现有容器
log "停止现有容器..."
docker compose down || true

# 4. 重新构建镜像
log "重新构建Docker镜像..."
docker compose build --no-cache

# 5. 启动容器
log "启动容器..."
docker compose up -d

# 6. 等待服务启动
log "等待服务启动..."
sleep 10

# 7. 健康检查
log "执行健康检查..."
if docker compose ps | grep -q "Up"; then
    log "✓ 服务启动成功"
    docker compose ps
else
    log "✗ 服务启动失败"
    docker compose logs --tail=50
    exit 1
fi

log "==================== 部署完成 ===================="
```

#### 设置脚本权限

```bash
# 196机器执行
sudo mkdir -p /opt/deploy
sudo chown deploy:deploy /opt/deploy
chmod +x /opt/deploy/redeploy.sh
```

### 3.2 199开发机触发脚本（deployment/deploy-trigger.sh）

```bash
#!/bin/bash
set -e

# 配置
REMOTE_USER="deploy"
REMOTE_HOST="172.17.12.196"
REMOTE_CODE_DIR="/opt/graduation/code"
REMOTE_SCRIPT="/opt/deploy/redeploy.sh"
LOCAL_PROJECT_DIR="/home/caohui/projects/graduation-leave-system"
LOG_FILE="$HOME/deploy-trigger.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "==================== 触发远程部署 ===================="

# 1. 检查Git状态（可选）
if [ -d .git ]; then
    COMMIT=$(git rev-parse --short HEAD)
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    log "当前提交: $COMMIT (分支: $BRANCH)"
fi

# 2. rsync同步代码到196（选择性同步）
log "同步代码到196测试机..."
rsync -avz --delete \
    --include='backend/***' \
    --include='demo-web/***' \
    --include='nginx.conf' \
    --include='docker-compose.yml' \
    --include='requirements.txt' \
    --include='package.json' \
    --exclude='.git/' \
    --exclude='docs/' \
    --exclude='PRD/' \
    --exclude='screenshots/' \
    --exclude='.collab/' \
    --exclude='.wolf/' \
    --exclude='*.pyc' \
    --exclude='__pycache__/' \
    --exclude='node_modules/' \
    --exclude='.env' \
    --exclude='*.log' \
    "$LOCAL_PROJECT_DIR/" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_CODE_DIR/"

if [ $? -ne 0 ]; then
    log "✗ rsync同步失败"
    exit 1
fi
log "✓ 代码同步完成"

# 3. 通过SSH触发196部署
log "触发196测试机部署..."
ssh "$REMOTE_USER@$REMOTE_HOST" "bash $REMOTE_SCRIPT" 2>&1 | tee -a "$LOG_FILE"

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    log "✓ 远程部署成功"
else
    log "✗ 远程部署失败"
    exit 1
fi

log "==================== 部署完成 ===================="
```

#### 设置脚本权限

```bash
# 199机器执行
chmod +x deployment/deploy-trigger.sh
```

#### rsync参数说明

- `-a` - archive模式（保留权限、时间戳等）
- `-v` - 显示详细信息
- `-z` - 压缩传输
- `--delete` - 删除目标端多余文件
- `--include/--exclude` - 选择性同步，只传输运行时必需文件

---

## 四、Docker Compose配置优化

### 4.1 修改docker-compose.yml（本地代码路径）

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    volumes:
      # 日志目录（可写，本地存储）
      - /opt/graduation/logs/backend:/app/logs
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/graduation
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    networks:
      - graduation-net

  frontend:
    build:
      context: ./demo-web
      dockerfile: Dockerfile
    networks:
      - graduation-net

  nginx:
    image: nginx:alpine
    ports:
      - "7787:80"
      - "7788:8080"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - backend
      - frontend
    networks:
      - graduation-net

  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: graduation
    volumes:
      - /opt/graduation/data/postgres:/var/lib/postgresql/data
    networks:
      - graduation-net

  redis:
    image: redis:7-alpine
    volumes:
      - /opt/graduation/data/redis:/data
    networks:
      - graduation-net

networks:
  graduation-net:
    driver: bridge
```

**注意：** 此配置文件放在196的`/opt/graduation/code/docker-compose.yml`，使用相对路径引用本地代码。

---

## 五、自动化触发方式

### 方式一：Git Hook触发（推荐）

#### 199机器配置post-commit hook

```bash
# 编辑Git hook
vim .git/hooks/post-commit

# 添加以下内容
#!/bin/bash
bash deployment/deploy-trigger.sh
```

```bash
# 设置权限
chmod +x .git/hooks/post-commit
```

**优点：** 每次提交后自动触发  
**缺点：** 只在有Git提交时触发

### 方式二：文件监控触发（inotifywait）

#### 199机器安装inotify-tools

```bash
sudo apt install inotify-tools -y
```

#### 创建监控脚本（deployment/watch-and-deploy.sh）

```bash
#!/bin/bash

WATCH_DIR="/home/caohui/projects/graduation-leave-system"
TRIGGER_SCRIPT="$WATCH_DIR/deployment/deploy-trigger.sh"

echo "开始监控目录: $WATCH_DIR"

inotifywait -m -r -e modify,create,delete,move \
    --exclude '\.git|__pycache__|node_modules|\.swp' \
    "$WATCH_DIR" | while read path action file; do
    
    echo "检测到变化: $path$file ($action)"
    
    # 防抖：等待1秒，避免频繁触发
    sleep 1
    
    # 触发部署
    bash "$TRIGGER_SCRIPT"
    
    # 冷却期：60秒内不再触发
    sleep 60
done
```

```bash
# 设置权限
chmod +x deployment/watch-and-deploy.sh

# 后台运行
nohup bash deployment/watch-and-deploy.sh > /tmp/watch-deploy.log 2>&1 &
```

**优点：** 实时监控文件变化  
**缺点：** 需要常驻进程，可能因网络问题导致NFS inotify不可靠

### 方式三：定时任务触发

#### 199机器配置cron

```bash
# 编辑crontab
crontab -e

# 添加定时任务（每5分钟检查一次）
*/5 * * * * cd /home/caohui/projects/graduation-leave-system && bash deployment/deploy-trigger.sh >> /tmp/cron-deploy.log 2>&1
```

**优点：** 简单可靠，无需常驻进程  
**缺点：** 有延迟，非实时

---

## 六、部署流程

### 6.1 初次部署

#### 步骤1：196机器准备环境

```bash
# 1. 创建目录结构
sudo mkdir -p /opt/graduation/{code,data/{postgres,redis},logs/backend}
sudo useradd -m -s /bin/bash deploy
sudo chown -R deploy:deploy /opt/graduation

# 2. 安装Docker（如未安装）
# sudo apt install docker.io docker-compose-plugin -y
# sudo usermod -aG docker deploy

# 3. 创建部署脚本
sudo mkdir -p /opt/deploy
sudo vim /opt/deploy/redeploy.sh
# 复制3.1节脚本内容

sudo chown deploy:deploy /opt/deploy/redeploy.sh
chmod +x /opt/deploy/redeploy.sh
```

#### 步骤2：199机器配置SSH

```bash
# 1. 生成SSH密钥（如未生成）
ssh-keygen -t ed25519 -C "deploy@199"

# 2. 复制公钥到196
ssh-copy-id deploy@172.17.12.196

# 3. 测试连接
ssh deploy@172.17.12.196 'echo "SSH连接成功"'
```

#### 步骤3：首次同步代码

```bash
# 199机器执行
cd /home/caohui/projects/graduation-leave-system

# 创建触发脚本
mkdir -p deployment
vim deployment/deploy-trigger.sh
# 复制3.2节脚本内容

chmod +x deployment/deploy-trigger.sh

# 首次部署
bash deployment/deploy-trigger.sh
```

#### 步骤4：配置自动触发（Git Hook）

```bash
# 199机器执行
vim .git/hooks/post-commit

# 添加内容：
#!/bin/bash
bash deployment/deploy-trigger.sh

# 设置权限
chmod +x .git/hooks/post-commit
```

### 6.2 日常部署流程

```bash
# 199机器：开发 → 提交
cd /home/caohui/projects/graduation-leave-system
git add .
git commit -m "feat: 新功能"

# Git Hook自动触发：
#   1. rsync同步代码到196
#   2. SSH触发196执行redeploy.sh
#   3. Docker重建并启动容器

# 验证部署
curl http://172.17.12.196:7787/health
```

---

## 七、监控与日志

### 7.1 查看部署日志

```bash
# 196机器查看部署日志
tail -f /var/log/graduation-deploy.log

# 199机器查看触发日志
tail -f ~/deploy-trigger.log
```

### 7.2 查看容器日志

```bash
# 196机器查看容器日志
cd /mnt/nfs/graduation
docker compose logs -f backend
docker compose logs -f frontend
```

### 7.3 健康检查

```bash
# 196机器检查服务状态
docker compose ps

# 检查NFS挂载
df -h | grep graduation
mountpoint /mnt/nfs/graduation
```

---

## 八、故障排查

### 8.1 rsync同步失败

**症状：** `rsync: connection unexpectedly closed`

**排查：**
```bash
# 测试SSH连接
ssh deploy@172.17.12.196 'echo "SSH正常"'

# 检查远程目录权限
ssh deploy@172.17.12.196 'ls -la /opt/graduation/code'

# 手动测试rsync
rsync -avz --dry-run backend/ deploy@172.17.12.196:/opt/graduation/code/backend/
```

**解决：**
```bash
# 196机器确保目录存在且有权限
ssh deploy@172.17.12.196 'sudo chown -R deploy:deploy /opt/graduation'
```

### 8.2 权限问题

**症状：** 容器内无法写入日志

**排查：**
```bash
# 196机器检查目录权限
ls -la /opt/graduation/logs
docker compose exec backend ls -la /app/logs
```

**解决：**
```bash
# 196机器修改权限
sudo chown -R deploy:deploy /opt/graduation/logs
chmod -R 755 /opt/graduation/logs
```

### 8.3 Docker构建失败

**症状：** `docker compose build` 失败

**排查：**
```bash
# 检查代码目录
ls -la /opt/graduation/code/backend/Dockerfile

# 查看详细错误
cd /opt/graduation/code
docker compose build --no-cache --progress=plain
```

### 8.4 SSH触发失败

**症状：** 199机器执行deploy-trigger.sh无响应

**排查：**
```bash
# 测试SSH连接
ssh deploy@172.17.12.196 'echo "SSH正常"'

# 测试远程脚本
ssh deploy@172.17.12.196 'ls -la /opt/deploy/redeploy.sh'

# 手动执行远程脚本
ssh deploy@172.17.12.196 'bash /opt/deploy/redeploy.sh'
```

### 8.5 rsync排除规则测试

**测试哪些文件会被同步：**
```bash
# 199机器执行dry-run
cd /home/caohui/projects/graduation-leave-system
rsync -avz --dry-run --delete \
    --include='backend/***' \
    --include='demo-web/***' \
    --include='nginx.conf' \
    --include='docker-compose.yml' \
    --exclude='*' \
    ./ deploy@172.17.12.196:/tmp/test-sync/
```

---

## 九、性能优化

### 9.1 rsync增量同步优化

```bash
# 使用--checksum检查文件变化（更精确但慢）
rsync -avz --checksum --delete ...

# 使用--compress-level调整压缩级别（1-9，默认6）
rsync -avz --compress-level=3 ...

# 限制带宽（单位KB/s）
rsync -avz --bwlimit=10000 ...
```

### 9.2 Docker构建缓存

```yaml
# docker-compose.yml添加构建缓存
services:
  backend:
    build:
      context: /mnt/nfs/graduation/backend
      cache_from:
        - graduation-backend:latest
```

### 9.3 分层构建策略

```dockerfile
# Dockerfile优化示例
FROM python:3.11-slim

# 1. 先安装依赖（缓存层）
COPY requirements.txt .
RUN pip install -r requirements.txt

# 2. 再复制代码（变化层）
COPY . /app
WORKDIR /app
```

---

## 十、安全加固

### 10.1 rsync使用专用SSH密钥

```bash
# 199机器生成专用部署密钥
ssh-keygen -t ed25519 -f ~/.ssh/deploy_key -C "deploy-only"
ssh-copy-id -i ~/.ssh/deploy_key.pub deploy@172.17.12.196

# 修改触发脚本使用专用密钥
rsync -avz -e "ssh -i ~/.ssh/deploy_key" ...
```

### 10.2 SSH密钥管理

```bash
# 使用专用部署密钥
ssh-keygen -t ed25519 -f ~/.ssh/deploy_key -C "deploy-only"
ssh-copy-id -i ~/.ssh/deploy_key.pub deploy@218.75.196.196

# 修改触发脚本使用专用密钥
ssh -i ~/.ssh/deploy_key deploy@218.75.196.196 "bash $REMOTE_SCRIPT"
```

### 10.3 限制sudo权限

```bash
# 196机器：限制deploy用户只能执行特定命令
sudo visudo
# 添加
deploy ALL=(ALL) NOPASSWD: /bin/mount, /usr/bin/docker, /usr/local/bin/docker-compose
```

---

## 十一、备份与回滚

### 11.1 容器镜像备份

```bash
# 196机器：部署前备份镜像
docker tag graduation-backend:latest graduation-backend:backup-$(date +%Y%m%d-%H%M%S)
docker tag graduation-frontend:latest graduation-frontend:backup-$(date +%Y%m%d-%H%M%S)
```

### 11.2 快速回滚

```bash
# 196机器：回滚到备份镜像
docker compose down
docker tag graduation-backend:backup-20260614-100000 graduation-backend:latest
docker tag graduation-frontend:backup-20260614-100000 graduation-frontend:latest
docker compose up -d
```

### 11.3 数据库备份

```bash
# 196机器：定期备份数据库
docker compose exec postgres pg_dump -U user graduation > /opt/graduation/backups/db-$(date +%Y%m%d).sql
```

---

## 十二、附录

### 12.1 完整文件清单

**199开发机：**
- `deployment/deploy-trigger.sh` - 部署触发脚本
- `.git/hooks/post-commit` - Git提交钩子（可选）
- `deployment/watch-and-deploy.sh` - 文件监控脚本（可选）

**196测试机：**
- `/opt/deploy/redeploy.sh` - 部署执行脚本
- `/etc/fstab` - NFS自动挂载配置
- `/opt/graduation/` - 本地存储目录

### 12.2 端口映射

| 服务 | 容器端口 | 宿主机端口 | 用途 |
|------|---------|----------|------|
| Backend | 8000 | 7787 | API服务 |
| Frontend | 80 | 7788 | Web界面 |
| PostgreSQL | 5432 | - | 数据库（内部） |
| Redis | 6379 | - | 缓存（内部） |

### 12.3 环境变量

**Backend容器：**
```env
DATABASE_URL=postgresql://user:pass@postgres:5432/graduation
REDIS_URL=redis://redis:6379/0
DEBUG=False
SECRET_KEY=your-secret-key
```

### 12.4 同步文件清单

**同步到196的文件：**
- `backend/` - 后端Python代码
- `demo-web/` - 前端HTML/JS/CSS
- `nginx.conf` - Nginx配置
- `docker-compose.yml` - 容器编排
- `requirements.txt` - Python依赖
- `package.json` - Node依赖（如有）

**199独有文件（不同步）：**
- `.git/` - Git历史（~500MB）
- `docs/` - 项目文档
- `PRD/` - 需求文档
- `.collab/`, `.wolf/` - 协作记录
- `screenshots/` - 截图
- `*.log` - 日志文件

### 12.5 参考资料

- rsync官方文档：https://rsync.samba.org/
- Docker Compose文档：https://docs.docker.com/compose/
- SSH免密登录：https://www.ssh.com/academy/ssh/copy-id

---

**文档版本：** v2.0  
**制定人：** Claude（基于Codex+Gemini讨论共识）  
**审核状态：** 待实施验证  
**更新日志：**
- 2026-06-14 v1.0: 初始版本，NFS方案
- 2026-06-14 v2.0: 修正IP地址，改用rsync选择性同步，排除非运行时文件
