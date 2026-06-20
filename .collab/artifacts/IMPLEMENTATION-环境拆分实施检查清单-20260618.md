# 环境拆分实施检查清单

**日期**: 2026-06-18  
**环境**: 199开发机 → 196生产机  
**状态**: 🟢 就绪，可以开始实施

---

## 前置条件验证 ✅

- [x] 199→196 SSH免密登录
- [x] 196 Docker已安装 (29.1.3)
- [x] 196所需软件已安装 (curl/git/age)
- [x] 196所需端口可用 (7787/7788/17787/17788/5432)
- [x] 196磁盘空间充足 (450GB)
- [x] 196内存充足 (28GB)

---

## 实施计划（按R3共识方案）

### 阶段1: 安全加固（1小时）

#### 1.1 SSH密钥加密 (10分钟)
```bash
# 在199上执行
cd ~/.ssh
ssh-keygen -t ed25519 -N "$(openssl rand -base64 32)" -f id_ed25519_prod -C "199-prod-deploy"
eval $(ssh-agent)
ssh-add id_ed25519_prod

# 复制到196
ssh-copy-id -i id_ed25519_prod.pub caohui@172.17.12.196
```

#### 1.2 196限制SSH来源IP (10分钟)
```bash
# 在196上执行
sudo tee /etc/ssh/sshd_config.d/99-restrict-dev.conf <<EOF
Match Address 172.17.12.199
    PasswordAuthentication no
    PubkeyAuthentication yes
EOF

sudo systemctl reload sshd
```

#### 1.3 配置加密（age）(20分钟)
```bash
# 在199上生成age密钥
age-keygen -o ~/.age/key.txt
AGE_PUBLIC=$(age-keygen -y ~/.age/key.txt)

# 加密生产配置
cd ~/projects/graduation-leave-system
age --encrypt --recipient $AGE_PUBLIC .env.prod > .env.prod.age
age --encrypt --recipient $AGE_PUBLIC .env.staging > .env.staging.age

# 将密钥复制到196
scp ~/.age/key.txt caohui@172.17.12.196:~/.age/
```

#### 1.4 代码同步前检查脚本 (20分钟)
```bash
# 在199上创建
cat > ~/scripts/pre-sync-check.sh << 'SCRIPT'
#!/bin/bash
set -e
SOURCE="/home/caohui/projects/graduation-leave-system"

# 敏感信息检测
if grep -rn --include="*.py" --include="*.js" \
    -E "(SECRET_KEY|PASSWORD|API_KEY)\s*=\s*['\"]" \
    "$SOURCE" | grep -v ".env.template"; then
    echo "❌ 发现硬编码敏感信息"
    exit 1
fi

# Python语法检查
find "$SOURCE/backend" -name "*.py" -exec python3 -m py_compile {} \; || {
    echo "❌ Python语法错误"
    exit 1
}

echo "✅ 安全检查通过"
SCRIPT

chmod +x ~/scripts/pre-sync-check.sh
```

**验收**: SSH密钥有密码保护，.env文件已加密，pre-sync-check脚本可执行

---

### 阶段2: 监控告警（30分钟）

#### 2.1 监控脚本 (15分钟)
```bash
# 在199上创建
cat > ~/scripts/monitor-sync.sh << 'SCRIPT'
#!/bin/bash
WEBHOOK="企业微信Webhook地址"

alert() {
    curl -X POST "$WEBHOOK" -H 'Content-Type: application/json' \
        -d "{\"msgtype\":\"text\",\"text\":{\"content\":\"$1\"}}"
}

# 同步服务检查
if ! systemctl --user is-active sync-to-prod.service &>/dev/null; then
    alert "❌ 199同步服务已停止"
fi

# 同步延迟检查
LAST_SYNC=$(stat -c %Y /tmp/sync-to-prod.log 2>/dev/null || echo 0)
if [ $(($(date +%s) - LAST_SYNC)) -gt 600 ]; then
    alert "⚠️ 代码同步超时10分钟"
fi

# 196服务检查
if ! ssh caohui@172.17.12.196 "curl -sf http://localhost:7787/readyz" &>/dev/null; then
    alert "🔴 196后端服务异常"
fi

# 磁盘检查
for host in "localhost" "caohui@172.17.12.196"; do
    DISK=$(ssh $host "df / | awk 'NR==2 {print \$5}' | tr -d %")
    [ "$DISK" -gt 85 ] && alert "⚠️ ${host} 磁盘${DISK}%"
done
SCRIPT

chmod +x ~/scripts/monitor-sync.sh
crontab -l | grep -v monitor-sync | { cat; echo "*/5 * * * * ~/scripts/monitor-sync.sh"; } | crontab -
```

#### 2.2 日志轮转 (10分钟)
```bash
# 在199上
sudo tee /etc/logrotate.d/graduation-sync <<EOF
/tmp/sync-to-prod.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
EOF

# 在196上
ssh caohui@172.17.12.196 "sudo tee /etc/logrotate.d/graduation-system <<'EOF'
/var/log/graduation-*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
EOF"
```

#### 2.3 企业微信Webhook配置 (5分钟)
```bash
# 获取Webhook地址后填入monitor-sync.sh
# 测试告警
~/scripts/monitor-sync.sh
```

**验收**: 监控脚本cron已配置，日志轮转生效，告警测试通过

---

### 阶段3: Staging环境（1.5小时）

#### 3.1 196创建目录结构 (10分钟)
```bash
ssh caohui@172.17.12.196 << 'EOF'
sudo mkdir -p /opt/graduation-leave-system/{staging,production,backups,scripts}
sudo chown -R caohui:caohui /opt/graduation-leave-system
mkdir -p /opt/graduation-leave-system/staging/{backend,demo-web}
mkdir -p /opt/graduation-leave-system/production/{backend,demo-web}
EOF
```

#### 3.2 创建docker-compose配置 (20分钟)
```bash
# 在196上创建staging配置
ssh caohui@172.17.12.196 << 'EOF'
cat > /opt/graduation-leave-system/staging/docker-compose.staging.yml << 'COMPOSE'
version: '3.8'
services:
  db:
    image: postgres:15
    container_name: staging-graduation-db
    environment:
      POSTGRES_DB: graduation_leave
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: staging_password
    volumes:
      - staging_postgres_data:/var/lib/postgresql/data
    ports:
      - "15432:5432"
    restart: unless-stopped

  backend:
    build: ./backend
    container_name: staging-graduation-backend
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
    env_file:
      - .env.staging
    volumes:
      - ./backend:/app
    ports:
      - "17787:8000"
    depends_on:
      - db
    restart: unless-stopped

volumes:
  staging_postgres_data:
COMPOSE
EOF
```

#### 3.3 配置同步脚本 (20分钟)
```bash
# 在199上创建
cat > ~/scripts/sync-to-staging.sh << 'SCRIPT'
#!/bin/bash
set -e

SOURCE="/home/caohui/projects/graduation-leave-system"
DEST="caohui@172.17.12.196:/opt/graduation-leave-system/staging"

# 前置检查
~/scripts/pre-sync-check.sh || exit 1

# 同步代码
rsync -avz --delete \
  --exclude='.git' \
  --exclude='backend/venv' \
  --exclude='backend/__pycache__' \
  --exclude='.env.dev' \
  --exclude='node_modules' \
  --exclude='.claude' \
  --exclude='.omc' \
  --exclude='.wolf' \
  "$SOURCE/" "$DEST/"

echo "[$(date)] Synced to staging" >> /tmp/sync-to-prod.log

# 触发staging重启
ssh caohui@172.17.12.196 "cd /opt/graduation-leave-system/staging && docker-compose -f docker-compose.staging.yml restart backend"
SCRIPT

chmod +x ~/scripts/sync-to-staging.sh
```

#### 3.4 inotify监听服务 (20分钟)
```bash
# 在199上配置systemd服务
cat > ~/.config/systemd/user/sync-to-staging.service << 'SERVICE'
[Unit]
Description=Auto sync code to staging
After=network.target

[Service]
Type=simple
ExecStart=/home/caohui/scripts/sync-watch.sh
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
SERVICE

cat > ~/scripts/sync-watch.sh << 'SCRIPT'
#!/bin/bash
SOURCE="/home/caohui/projects/graduation-leave-system"
SYNC_SCRIPT="/home/caohui/scripts/sync-to-staging.sh"

inotifywait -m -r -e modify,create,delete,move \
  --exclude '\.git|__pycache__|\.pyc$|venv|node_modules|\.claude|\.omc|\.wolf' \
  "$SOURCE" | while read path action file; do
    echo "[$(date)] Detected: $action $path$file"
    sleep 1
    "$SYNC_SCRIPT"
done
SCRIPT

chmod +x ~/scripts/sync-watch.sh
systemctl --user enable sync-to-staging.service
systemctl --user start sync-to-staging.service
```

#### 3.5 促销脚本（staging→production）(20分钟)
```bash
# 在196上创建
ssh caohui@172.17.12.196 << 'EOF'
cat > /opt/graduation-leave-system/scripts/promote-to-prod.sh << 'SCRIPT'
#!/bin/bash
set -e

echo "=== 检查staging ==="
curl -f http://localhost:17787/readyz || { echo "Staging未就绪"; exit 1; }

echo "=== 备份生产 ==="
BACKUP="/opt/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP"
cp -r /opt/graduation-leave-system/production "$BACKUP/"

echo "=== 同步到生产 ==="
rsync -av --delete /opt/graduation-leave-system/staging/ /opt/graduation-leave-system/production/

echo "=== 重启生产 ==="
cd /opt/graduation-leave-system/production
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

sleep 5

echo "=== 健康检查 ==="
curl -f http://localhost:7787/readyz || {
    echo "❌ 生产异常，回滚..."
    rsync -av --delete "$BACKUP/production/" /opt/graduation-leave-system/production/
    docker-compose -f docker-compose.prod.yml up -d
    exit 1
}

echo "✅ 发布成功"
SCRIPT

chmod +x /opt/graduation-leave-system/scripts/promote-to-prod.sh
EOF
```

#### 3.6 验证端到端流程 (20分钟)
```bash
# 在199上修改一个文件，观察同步
echo "# Test sync" >> ~/projects/graduation-leave-system/README.md

# 等待3秒，检查196 staging是否更新
sleep 3
ssh caohui@172.17.12.196 "grep 'Test sync' /opt/graduation-leave-system/staging/README.md" && echo "✅ 同步成功"

# 访问staging
curl http://172.17.12.196:17787/readyz

# 手动促销到生产
ssh caohui@172.17.12.196 "/opt/graduation-leave-system/scripts/promote-to-prod.sh"

# 访问生产
curl http://172.17.12.196:7787/readyz
```

**验收**: 代码修改自动同步staging，促销脚本可用，生产服务正常

---

### 阶段4: 配置统一（1小时）

#### 4.1 拆分base/staging/prod配置 (30分钟)
```bash
# 在199上重构docker-compose
cd ~/projects/graduation-leave-system

# 创建base配置
cat > docker-compose.base.yml << 'BASE'
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: graduation_leave
      POSTGRES_USER: postgres

  backend:
    build: ./backend
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
    volumes:
      - ./backend:/app
    depends_on:
      - db
BASE

# staging覆盖
cat > docker-compose.staging.yml << 'STAGING'
version: '3.8'
services:
  db:
    container_name: staging-db
    environment:
      POSTGRES_PASSWORD: staging_pwd
    ports:
      - "15432:5432"
    volumes:
      - staging_pg_data:/var/lib/postgresql/data

  backend:
    container_name: staging-backend
    ports:
      - "17787:8000"
    env_file:
      - .env.staging

volumes:
  staging_pg_data:
STAGING

# production覆盖
cat > docker-compose.prod.yml << 'PROD'
version: '3.8'
services:
  db:
    container_name: prod-db
    environment:
      POSTGRES_PASSWORD: prod_pwd
    ports:
      - "5432:5432"
    volumes:
      - prod_pg_data:/var/lib/postgresql/data

  backend:
    container_name: prod-backend
    ports:
      - "7787:8000"
    env_file:
      - .env.prod

volumes:
  prod_pg_data:
PROD
```

#### 4.2 更新启动脚本 (20分钟)
```bash
# 在196上更新启动命令
ssh caohui@172.17.12.196 << 'EOF'
# Staging启动
cd /opt/graduation-leave-system/staging
docker-compose -f docker-compose.base.yml -f docker-compose.staging.yml up -d

# Production启动
cd /opt/graduation-leave-system/production
docker-compose -f docker-compose.base.yml -f docker-compose.prod.yml up -d
EOF
```

#### 4.3 验证配置独立性 (10分钟)
```bash
# 检查staging和production使用不同数据库
ssh caohui@172.17.12.196 "docker ps | grep -E 'staging-db|prod-db'"

# 检查端口隔离
ssh caohui@172.17.12.196 "ss -tuln | grep -E '17787|7787|15432|5432'"
```

**验收**: 三环境配置独立，staging/production互不影响

---

## 最终验收标准

- [ ] 199修改代码 → staging自动更新(<10秒)
- [ ] staging验证通过 → 一键促销到production
- [ ] 同步失败 → 企业微信告警
- [ ] 服务异常 → 企业微信告警
- [ ] production部署失败 → 自动回滚
- [ ] 日志轮转生效（不再无限增长）

---

## 实施负责人

- **执行**: （待指定）
- **技术支持**: （待指定）
- **时间窗口**: 周六上午 9:00-13:00（建议）

---

## 回滚方案

**任何阶段出问题**:
```bash
# 停止同步服务
systemctl --user stop sync-to-staging.service

# 196恢复最近备份
ssh caohui@172.17.12.196 "
cd /opt/graduation-leave-system/production
docker-compose down
LATEST=\$(ls -t /opt/backups | head -1)
rsync -av --delete /opt/backups/\$LATEST/production/ ./
docker-compose up -d
"
```

---

**文档状态**: ✅ 就绪，可以开始实施  
**预计完成时间**: 4小时  
**风险等级**: 低（每阶段可回滚）
