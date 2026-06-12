#!/bin/bash
# 回滚脚本 - 恢复配置+数据库+容器

set -e

REMOTE_USER=${DEPLOY_USER:-root}
REMOTE_HOST=${DEPLOY_HOST}
REMOTE_PATH=${DEPLOY_PATH:-/opt/graduation-leave-system}

echo "=== 开始回滚 ==="

# 1. 查找最近的备份时间戳
LAST_BACKUP=$(ssh $REMOTE_USER@$REMOTE_HOST "cat /tmp/last_backup_timestamp.txt 2>/dev/null || echo ''")

if [ -z "$LAST_BACKUP" ]; then
    echo "✗ 未找到备份记录"
    exit 1
fi

BACKUP_DIR="/tmp/backup_${LAST_BACKUP}"
echo "找到备份: $BACKUP_DIR"

# 2. 验证备份完整性
ssh $REMOTE_USER@$REMOTE_HOST "test -d $BACKUP_DIR && test -f $BACKUP_DIR/config.tar.gz && test -f $BACKUP_DIR/db_dump.sql.gz && test -f $BACKUP_DIR/git_sha.txt" || {
    echo "✗ 备份文件不完整"
    exit 1
}

# 3. 停止当前服务
echo "停止当前服务..."
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && docker-compose -f docker-compose.prod.yml down"

# 4. 恢复配置文件
echo "恢复配置..."
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && tar -xzf $BACKUP_DIR/config.tar.gz"

# 5. 恢复Git版本
BACKUP_SHA=$(ssh $REMOTE_USER@$REMOTE_HOST "cat $BACKUP_DIR/git_sha.txt")
echo "恢复Git版本: $BACKUP_SHA"
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && git checkout $BACKUP_SHA"

# 6. 重启服务（数据库需先启动）
echo "启动数据库..."
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && docker-compose -f docker-compose.prod.yml up -d db"
sleep 5

# 7. 恢复数据库
echo "恢复数据库..."
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && gunzip -c $BACKUP_DIR/db_dump.sql.gz | docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres graduation_leave"

# 8. 启动后端服务
echo "启动后端服务..."
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && docker-compose -f docker-compose.prod.yml up -d backend"

# 9. 健康检查验证
sleep 10
if ssh $REMOTE_USER@$REMOTE_HOST "curl -f http://localhost:7787/readyz > /dev/null 2>&1"; then
    echo "✓ 回滚成功"
else
    echo "✗ 回滚后服务仍异常"
    exit 1
fi

echo "=== 回滚完成 ==="
