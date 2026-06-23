#!/bin/bash
# 生产环境灰度部署脚本
set -e

ENVIRONMENT="production"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BACKUP_DIR="/opt/backups/graduation-leave-system"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "=== 毕业离校系统 生产环境灰度部署 ==="
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "⚠️  生产环境部署，请确认继续..."
read -p "输入 'yes' 继续: " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "部署取消"
    exit 0
fi

# 1. 数据库备份
echo "步骤1: 数据库备份..."
mkdir -p "$BACKUP_DIR"
pg_dump -U postgres graduation_prod > "$BACKUP_DIR/backup_$TIMESTAMP.sql"
if [ $? -ne 0 ]; then
    echo "❌ 数据库备份失败"
    exit 1
fi
echo "✅ 数据库备份完成: $BACKUP_DIR/backup_$TIMESTAMP.sql"

# 2. 执行数据库迁移
echo "步骤2: 执行数据库迁移..."
cd "$PROJECT_ROOT/backend"
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=config.prod
export ENABLE_STAY_SCHOOL=false  # 初始关闭Feature Flag

python manage.py migrate --no-input
if [ $? -ne 0 ]; then
    echo "❌ 迁移失败，开始回滚..."
    psql -U postgres graduation_prod < "$BACKUP_DIR/backup_$TIMESTAMP.sql"
    exit 1
fi
echo "✅ 迁移执行成功"

# 3. 部署代码
echo "步骤3: 部署代码..."
git pull origin main
if [ $? -ne 0 ]; then
    echo "❌ 代码拉取失败"
    exit 1
fi
echo "✅ 代码部署完成"

# 4. 重启服务
echo "步骤4: 重启应用服务..."
sudo systemctl restart graduation-backend
sleep 5

# 5. 烟雾测试
echo "步骤5: 烟雾测试..."
HEALTH_URL="${PROD_URL:-http://localhost:8000}/api/health/"
if ! curl -f -s "$HEALTH_URL" > /dev/null 2>&1; then
    echo "❌ 健康检查失败，开始回滚..."
    git checkout HEAD~1
    sudo systemctl restart graduation-backend
    exit 1
fi
echo "✅ 烟雾测试通过"

# 6. 灰度开启提示
echo ""
echo "✅ 部署成功（Feature Flag已关闭）"
echo "下一步："
echo "  1. 监控系统运行状态（30分钟）"
echo "  2. 确认无误后执行: export ENABLE_STAY_SCHOOL=true && sudo systemctl restart graduation-backend"
echo "  3. 持续监控关键指标"
echo ""
echo "回滚命令: bash $SCRIPT_DIR/rollback-prod.sh $TIMESTAMP"
