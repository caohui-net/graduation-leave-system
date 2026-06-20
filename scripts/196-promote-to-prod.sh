#!/bin/bash
set -e

EXCLUDES=(
  --exclude='.git' --exclude='backend/venv' --exclude='backend/__pycache__'
  --exclude='.env.*' --exclude='node_modules' --exclude='.claude'
  --exclude='.omc' --exclude='.wolf' --exclude='.trellis' --exclude='.collab'
  --exclude='.codegraph' --exclude='.codex' --exclude='.agents'
  --exclude='.venv*' --exclude='__pycache__' --exclude='backups'
  --exclude=".gemini" --exclude=".planning" --exclude=".understand-anything" --exclude=".pytest_cache" --exclude="logs" --exclude="backups" --exclude=".secrets" --exclude="backend/media"
)

echo "=== 检查staging状态 ==="
curl -sf http://localhost:17787/readyz || { echo "❌ Staging未就绪"; exit 1; }

echo "=== 备份生产环境 ==="
if [ -d /opt/graduation-leave-system/production/backend ]; then
    BACKUP="/opt/graduation-leave-system/backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP"
    cp -r /opt/graduation-leave-system/production "$BACKUP/"
    echo "✓ 备份到 $BACKUP"
fi

echo "=== 同步代码到生产 ==="
rsync -av --delete "${EXCLUDES[@]}"   /opt/graduation-leave-system/staging/ /opt/graduation-leave-system/production/

source /opt/graduation-leave-system/.secrets/production.env
echo "=== 写入生产配置 ==="
cat > /opt/graduation-leave-system/production/.env.prod << ENVEOF
DEBUG=False
SECRET_KEY=${SECRET_KEY}
DB_HOST=db
DB_PORT=5432
DB_NAME=graduation_leave
DB_USER=postgres
DB_PASSWORD=prod_secure_password
ALLOWED_HOSTS=172.17.12.196,localhost
CORS_ALLOWED_ORIGINS=http://172.17.12.196:7788
DATABASE_URL=postgresql://postgres:prod_secure_password@db:5432/graduation_leave
ENVEOF

echo "=== 重启生产服务 ==="
cd /opt/graduation-leave-system/production
docker compose -f docker-compose.prod.yml down 2>/dev/null || true
docker compose -f docker-compose.prod.yml up -d

echo "=== 等待服务就绪（最多120秒）==="
for i in $(seq 1 24); do
  if curl -sf http://localhost:7787/readyz > /dev/null 2>&1; then
    echo "✅ 生产环境发布成功"
    docker compose -f docker-compose.prod.yml exec -T backend python manage.py migrate --noinput 2>&1 | grep -E "Applying|No migrations|error" || true
    GIT_HASH=$(git -C /opt/graduation-leave-system/staging rev-parse --short HEAD 2>/dev/null || echo unknown)
    echo "${GIT_HASH}-$(date +%Y%m%d%H%M%S)" > /opt/graduation-leave-system/production/VERSION
    echo "$(date '+%Y-%m-%d %H:%M:%S') promote SUCCESS staging→production [${GIT_HASH}]" >> /opt/graduation-leave-system/deploy.log
    exit 0
  fi
  echo "  等待中... ($((i*5))s)"
  sleep 5
done

echo "❌ 生产环境120秒内未就绪，回滚..."
if [ -n "$BACKUP" ]; then
  rsync -av --delete "${EXCLUDES[@]}" "$BACKUP/production/" /opt/graduation-leave-system/production/
  cd /opt/graduation-leave-system/production
  docker compose -f docker-compose.prod.yml down
  docker compose -f docker-compose.prod.yml up -d
fi
exit 1
