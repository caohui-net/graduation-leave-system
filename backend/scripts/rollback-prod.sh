#!/bin/bash
# 生产环境回滚脚本
set -e

if [ -z "$1" ]; then
    echo "用法: $0 <backup_timestamp>"
    echo "示例: $0 20260623_020000"
    exit 1
fi

TIMESTAMP=$1
BACKUP_DIR="/opt/backups/graduation-leave-system"
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

echo "=== 生产环境回滚 ==="
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "备份文件: $BACKUP_FILE"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ 备份文件不存在"
    exit 1
fi

read -p "确认回滚？输入 'yes': " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "回滚取消"
    exit 0
fi

# 1. 关闭Feature Flag
echo "步骤1: 关闭Feature Flag..."
export ENABLE_STAY_SCHOOL=false
sudo systemctl restart graduation-backend
sleep 3

# 2. 检查是否需要数据库回滚
echo "步骤2: 检查服务状态..."
if curl -f -s http://localhost:8000/api/health/ > /dev/null 2>&1; then
    echo "✅ 服务正常，Feature Flag已关闭"
    exit 0
fi

# 3. 数据库回滚（仅在服务异常时）
echo "步骤3: 数据库回滚..."
psql -U postgres graduation_prod < "$BACKUP_FILE"
echo "✅ 数据库已回滚"

# 4. 重启服务
echo "步骤4: 重启服务..."
sudo systemctl restart graduation-backend
sleep 5

# 5. 验证
if curl -f -s http://localhost:8000/api/health/ > /dev/null 2>&1; then
    echo "✅ 回滚成功"
else
    echo "❌ 回滚后服务仍异常，需要人工介入"
    exit 1
fi
