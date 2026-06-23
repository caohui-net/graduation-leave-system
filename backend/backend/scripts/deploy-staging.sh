#!/bin/bash
# Staging环境部署脚本
set -e

ENVIRONMENT="staging"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== 毕业离校系统 Staging 部署 ==="
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"

# 1. 数据库迁移验证（dry-run）
echo "步骤1: 数据库迁移验证..."
cd "$PROJECT_ROOT/backend"
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=config.staging

python manage.py migrate --dry-run --verbosity 2
if [ $? -ne 0 ]; then
    echo "❌ 迁移验证失败"
    exit 1
fi
echo "✅ 迁移验证通过"

# 2. 执行实际迁移
echo "步骤2: 执行数据库迁移..."
python manage.py migrate --no-input
if [ $? -ne 0 ]; then
    echo "❌ 迁移执行失败"
    exit 1
fi
echo "✅ 迁移执行成功"

# 3. 收集静态文件
echo "步骤3: 收集静态文件..."
python manage.py collectstatic --no-input
echo "✅ 静态文件收集完成"

# 4. 重启服务
echo "步骤4: 重启应用服务..."
sudo systemctl restart graduation-backend-staging
sleep 5

# 5. 健康检查
echo "步骤5: 健康检查..."
HEALTH_URL="${STAGING_URL:-http://localhost:8001}/api/health/"
MAX_RETRIES=10
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -f -s "$HEALTH_URL" > /dev/null 2>&1; then
        echo "✅ 健康检查通过"
        echo "✅ Staging部署成功"
        exit 0
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "等待服务启动... ($RETRY_COUNT/$MAX_RETRIES)"
    sleep 3
done

echo "❌ 健康检查失败"
exit 1
