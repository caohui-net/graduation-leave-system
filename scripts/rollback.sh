#!/bin/bash
# 回滚脚本

set -e

REMOTE_USER=${DEPLOY_USER:-root}
REMOTE_HOST=${DEPLOY_HOST}
REMOTE_PATH=${DEPLOY_PATH:-/opt/graduation-leave-system}

echo "=== 开始回滚 ==="

# 1. 查找最近的备份
BACKUP=$(ssh $REMOTE_USER@$REMOTE_HOST "ls -t /tmp/backup_*.tar.gz 2>/dev/null | head -1")

if [ -z "$BACKUP" ]; then
    echo "✗ 未找到备份文件"
    exit 1
fi

echo "找到备份: $BACKUP"

# 2. 恢复配置
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && tar -xzf $BACKUP"

# 3. 回滚容器
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && docker-compose -f docker-compose.prod.yml up -d --force-recreate"

# 4. 验证
sleep 10
if ssh $REMOTE_USER@$REMOTE_HOST "curl -f http://localhost:7787/api/applications/ > /dev/null 2>&1"; then
    echo "✓ 回滚成功"
else
    echo "✗ 回滚后服务仍异常"
    exit 1
fi

echo "=== 回滚完成 ==="
