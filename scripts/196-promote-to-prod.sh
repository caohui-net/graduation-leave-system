#!/bin/bash
set -euo pipefail

PROD=/opt/graduation-leave-system/production
STAGING=/opt/graduation-leave-system/staging
SECRETS=/opt/graduation-leave-system/.secrets/production.env
ENVFILE=/opt/graduation-leave-system/.envs/production.env

EXCLUDES=(
  --exclude='.git' --exclude='backend/venv' --exclude='backend/__pycache__'
  --exclude='.env.*' --exclude='node_modules' --exclude='.claude'
  --exclude='.omc' --exclude='.wolf' --exclude='.trellis' --exclude='.collab'
  --exclude='.codegraph' --exclude='.codex' --exclude='.agents'
  --exclude='.venv*' --exclude='__pycache__' --exclude='backups'
  --exclude='.envs' --exclude='.secrets'
  --exclude='.gemini' --exclude='.planning' --exclude='.understand-anything'
  --exclude='.pytest_cache' --exclude='logs' --exclude='backend/media'
)

echo '=== 检查staging状态 ==='
curl -sf http://localhost:17787/readyz || { echo '❌ Staging未就绪'; exit 1; }

echo '=== 校验部署前提条件 ==='
[[ -f "$SECRETS" ]] || { echo '❌ secrets文件不存在'; exit 1; }
source "$SECRETS"
[[ -n "${SECRET_KEY:-}" ]] || { echo '❌ SECRET_KEY 未设置或为空'; exit 1; }

echo '=== 备份生产环境 ==='
if [ -d "$PROD/backend" ]; then
    BACKUP="/opt/graduation-leave-system/backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP"
    cp -r "$PROD" "$BACKUP/"
    echo "✓ 备份到 $BACKUP"
fi

echo '=== 同步代码到生产 ==='
rsync -av --delete "${EXCLUDES[@]}" "$STAGING/" "$PROD/"

echo '=== 写入生产配置（原子写入）==='
TMPENV=$(mktemp)
chmod 600 "$TMPENV"
printf 'DEBUG=False\nSECRET_KEY=%s\nDB_HOST=db\nDB_PORT=5432\nDB_NAME=graduation_leave\nDB_USER=postgres\nDB_PASSWORD=prod_secure_password\nALLOWED_HOSTS=172.17.12.196,localhost\nCORS_ALLOWED_ORIGINS=http://172.17.12.196:7788\nDATABASE_URL=postgresql://postgres:prod_secure_password@db:5432/graduation_leave\n' \
  "${SECRET_KEY}" > "$TMPENV"
mv "$TMPENV" "$ENVFILE"

echo '=== 重启生产服务 ==='
cd "$PROD"
docker compose -f docker-compose.prod.yml down 2>/dev/null || true
docker compose -f docker-compose.prod.yml up -d

echo '=== 等待容器启动（最多30秒）==='
for i in $(seq 1 6); do
  if docker compose -f docker-compose.prod.yml exec -T backend echo ok >/dev/null 2>&1; then
    break
  fi
  echo "  容器启动中... ($((i*5))s)"
  sleep 5
done

echo '=== 执行数据库迁移（接流量前）==='
MIGRATE_OUT=$(docker compose -f docker-compose.prod.yml exec -T backend python manage.py migrate --noinput 2>&1)
echo "$MIGRATE_OUT" | grep -E 'Applying|No migrations|error' || true
if echo "$MIGRATE_OUT" | grep -qi 'error'; then
  echo '❌ Migration 失败，停止发布'
  exit 1
fi
MIGRATED=1

echo '=== 等待服务就绪（最多90秒）==='
for i in $(seq 1 18); do
  if curl -sf http://localhost:7787/readyz >/dev/null 2>&1; then
    GIT_HASH=$(git -C "$STAGING" rev-parse --short HEAD 2>/dev/null || echo unknown)
    echo "${GIT_HASH}-$(date +%Y%m%d%H%M%S)" > "$PROD/VERSION"
    echo "$(date '+%Y-%m-%d %H:%M:%S') promote SUCCESS staging->production [${GIT_HASH}]" >> /opt/graduation-leave-system/deploy.log
    echo '✅ 生产环境发布成功'
    exit 0
  fi
  echo "  等待中... ($((i*5))s)"
  sleep 5
done

echo '❌ 服务90秒内未就绪'
if [ -n "${BACKUP:-}" ] && [ -z "${MIGRATED:-}" ]; then
  echo '迁移未执行，执行文件回滚...'
  rsync -av --delete "${EXCLUDES[@]}" "$BACKUP/production/" "$PROD/"
  cd "$PROD" && docker compose -f docker-compose.prod.yml down && docker compose -f docker-compose.prod.yml up -d
else
  echo '⚠️  迁移已执行，跳过文件回滚（防止代码/DB不一致）'
  echo '请手动检查服务状态'
fi
exit 1
