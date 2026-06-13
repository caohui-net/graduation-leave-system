# 毕业离校系统异地Docker自动部署方案

**版本：** v1.0  
**创建时间：** 2026-06-13  
**讨论记录：** `.collab/artifacts/DISCUSS-毕业离校系统异地DOCKER自动化部署方案-*`

---

## 一、方案概述

### 1.1 部署目标

- **开发机（199）：** 172.17.12.199 - 代码开发和 NFS 服务器
- **测试机（196）：** 172.17.12.196 - Docker 部署和服务运行
- **共享方式：** NFS（199→196 单向只读共享）
- **触发方式：** SSH 推送触发（199 主动通知 196 重新部署）

### 1.2 核心架构

```
┌─────────────────┐              ┌─────────────────┐
│   199 开发机    │              │   196 测试机    │
├─────────────────┤              ├─────────────────┤
│ - 代码编辑      │              │ - NFS Client    │
│ - Git 仓库      │  NFS Mount   │ - rsync 本地化  │
│ - NFS Server    │─────────────→│ - Docker 构建   │
│                 │              │ - 服务运行      │
│ [触发脚本]      │  SSH 命令    │                 │
│   trigger.sh────┼─────────────→│ /opt/deploy.sh  │
└─────────────────┘              └─────────────────┘
```

---

## 二、技术约束与风险（基于 Gemini 分析）

### 2.1 关键技术限制

#### ❌ 禁止操作
1. **Docker 直接挂载 NFS 卷** - 会导致数据库文件锁损坏、I/O 性能严重下降
2. **依赖 inotify 自动触发** - NFS 不支持文件系统事件，无法被动监听变化
3. **NFS 存储状态数据** - 数据库、Redis、日志必须用本地存储

#### ⚠️ 必须处理
1. **UID/GID 权限对齐** - 199 NFS server、196 宿主机、Docker 容器三方一致
2. **显式触发机制** - 199 完成修改后主动 SSH 通知 196 部署
3. **本地暂存策略** - 196 用 rsync 将 NFS 内容复制到本地再构建

### 2.2 风险缓解

| 风险 | 缓解措施 |
|------|---------|
| 权限冲突导致容器无法写日志 | NFSv4 配置 all_squash + 固定 UID/GID |
| 构建性能低下 | rsync 到 196 本地 SSD 后再构建 |
| 数据库损坏 | docker-compose.yml 中数据卷用本地路径 |
| 部署失败无通知 | deploy.sh 脚本返回详细日志和错误码 |

---

## 三、实施步骤

### 3.1 阶段一：NFS 配置（199 开发机）

#### 安装 NFS Server

```bash
# 199 执行
sudo apt update
sudo apt install nfs-kernel-server -y
```

#### 配置 NFS 导出

创建 `/etc/exports`：

```bash
# /etc/exports
/home/caohui/projects/graduation-leave-system 172.17.12.196(ro,sync,no_subtree_check,all_squash,anonuid=1000,anongid=1000)
```

**参数说明：**
- `ro` - 只读挂载（196 不能修改 NFS 内容）
- `sync` - 同步写入，确保数据一致性
- `no_subtree_check` - 性能优化
- `all_squash` - 所有用户映射为匿名用户
- `anonuid=1000,anongid=1000` - 匿名用户映射为 UID/GID 1000

#### 启动 NFS 服务

```bash
sudo exportfs -ra
sudo systemctl restart nfs-kernel-server
sudo systemctl enable nfs-kernel-server

# 验证导出
showmount -e 172.17.12.199
```

#### 防火墙配置

```bash
sudo ufw allow from 172.17.12.196 to any port nfs
sudo ufw allow from 172.17.12.196 to any port 2049
```

---

### 3.2 阶段二：测试机配置（196）

#### 安装 NFS Client

```bash
# 196 执行
sudo apt update
sudo apt install nfs-common -y
```

#### 创建挂载点

```bash
sudo mkdir -p /mnt/code-199
sudo chown 1000:1000 /mnt/code-199
```

#### 挂载 NFS

```bash
# 临时挂载测试
sudo mount -t nfs -o ro 172.17.12.199:/home/caohui/projects/graduation-leave-system /mnt/code-199

# 验证
ls -la /mnt/code-199
```

#### 永久挂载（测试通过后）

编辑 `/etc/fstab`：

```bash
172.17.12.199:/home/caohui/projects/graduation-leave-system /mnt/code-199 nfs ro,defaults 0 0
```

#### 创建本地工作目录

```bash
sudo mkdir -p /opt/graduation-leave-system
sudo chown 1000:1000 /opt/graduation-leave-system
```

---

### 3.3 阶段三：部署脚本（196）

#### 创建 `/opt/deploy.sh`

```bash
#!/bin/bash
set -e

PROJECT_NAME="graduation-leave-system"
NFS_SOURCE="/mnt/code-199"
LOCAL_TARGET="/opt/$PROJECT_NAME"
LOG_FILE="/var/log/deploy-$PROJECT_NAME.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting deployment..." | tee -a "$LOG_FILE"

# 1. 验证 NFS 挂载
if ! mountpoint -q "$NFS_SOURCE"; then
    echo "ERROR: NFS not mounted at $NFS_SOURCE" | tee -a "$LOG_FILE"
    exit 1
fi

# 2. rsync 代码到本地
echo "Syncing code from NFS to local..." | tee -a "$LOG_FILE"
rsync -avz --delete \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='node_modules' \
    --exclude='.env.local' \
    "$NFS_SOURCE/" "$LOCAL_TARGET/" | tee -a "$LOG_FILE"

# 3. 进入项目目录
cd "$LOCAL_TARGET"

# 4. 停止现有容器
echo "Stopping existing containers..." | tee -a "$LOG_FILE"
docker-compose down || true

# 5. 构建镜像
echo "Building Docker images..." | tee -a "$LOG_FILE"
docker-compose build --no-cache

# 6. 启动服务
echo "Starting containers..." | tee -a "$LOG_FILE"
docker-compose up -d --remove-orphans

# 7. 验证服务状态
sleep 5
echo "Container status:" | tee -a "$LOG_FILE"
docker-compose ps | tee -a "$LOG_FILE"

# 8. 健康检查
echo "Health check..." | tee -a "$LOG_FILE"
if curl -f http://localhost:8000/api/health/ 2>/dev/null; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Deployment SUCCESS" | tee -a "$LOG_FILE"
    exit 0
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Deployment FAILED - Health check failed" | tee -a "$LOG_FILE"
    docker-compose logs --tail=50 | tee -a "$LOG_FILE"
    exit 1
fi
```

#### 设置权限

```bash
sudo chmod +x /opt/deploy.sh
sudo chown 1000:1000 /opt/deploy.sh
```

---

### 3.4 阶段四：触发脚本（199）

#### 创建 `~/scripts/trigger-deploy-196.sh`

```bash
#!/bin/bash
set -e

TARGET_HOST="172.17.12.196"
TARGET_USER="caohui"
DEPLOY_SCRIPT="/opt/deploy.sh"

echo "Triggering deployment on $TARGET_HOST..."

# SSH 触发部署
ssh "$TARGET_USER@$TARGET_HOST" "bash $DEPLOY_SCRIPT"

if [ $? -eq 0 ]; then
    echo "✅ Deployment triggered successfully"
    echo "🔗 Test URL: http://$TARGET_HOST:8000"
else
    echo "❌ Deployment failed"
    exit 1
fi
```

#### 设置权限

```bash
chmod +x ~/scripts/trigger-deploy-196.sh
```

#### SSH 免密登录配置

```bash
# 199 执行
ssh-keygen -t ed25519 -C "deploy-automation"
ssh-copy-id caohui@172.17.12.196

# 验证
ssh caohui@172.17.12.196 "echo 'SSH OK'"
```

---

### 3.5 阶段五：Docker Compose 配置调整（196）

#### 修改 `docker-compose.yml` - 确保数据卷在本地

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    volumes:
      - ./backend:/app
      - backend-media:/app/media
      - backend-logs:/app/logs
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/graduation_leave
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: graduation_leave
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

volumes:
  postgres-data:
  redis-data:
  backend-media:
  backend-logs:
```

---

## 四、测试验证

### 4.1 NFS 权限验证

```bash
# 196 执行
touch /mnt/code-199/test-write.txt  # 应失败（ro 挂载）
ls -l /mnt/code-199/backend/        # 应成功，UID 1000
```

### 4.2 手动部署测试

```bash
# 196 执行
sudo /opt/deploy.sh
```

### 4.3 触发器测试

```bash
# 199 执行
~/scripts/trigger-deploy-196.sh
```

### 4.4 端到端测试

```bash
# 199 修改代码
echo "# Test" >> backend/README.md

# 触发部署
~/scripts/trigger-deploy-196.sh

# 验证
curl http://172.17.12.196:8000/api/health/
```

---

## 五、故障排查

### NFS 挂载失败
```bash
sudo systemctl status nfs-kernel-server  # 199
showmount -e 172.17.12.199              # 196
```

### Docker 权限错误
```bash
ls -ln /opt/graduation-leave-system/
docker-compose config | grep user
```

### 数据库连接失败
```bash
docker-compose ps
docker-compose logs db
```

---

## 六、未来优化

1. **CI/CD 集成** - GitLab CI / GitHub Actions
2. **监控告警** - Prometheus + Grafana
3. **多环境支持** - test/staging/production

---

**文档状态：** ✅ 已完成  
**讨论记录：** `.collab/artifacts/DISCUSS-毕业离校系统异地DOCKER*`
