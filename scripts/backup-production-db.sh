#!/bin/bash
set -euo pipefail

# 生产数据库全量备份脚本
# 使用场景: 重大操作前备份、定期备份

BACKUP_DIR="/opt/graduation-leave-system/backups/db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="graduation_leave_prod_${TIMESTAMP}.sql"
PROD_DIR="/opt/graduation-leave-system/production"

echo "=== 生产数据库全量备份 ==="
echo "时间: $(date)"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 检查生产环境是否运行
if [ ! -f "$PROD_DIR/docker-compose.prod.yml" ]; then
    echo "❌ 生产环境配置不存在"
    exit 1
fi

# 使用docker compose exec执行pg_dump
echo "正在备份数据库..."
cd "$PROD_DIR"
docker compose -f docker-compose.prod.yml exec -T db pg_dump \
    -U postgres \
    -d graduation_leave \
    --format=custom \
    --verbose \
    --file=/tmp/${BACKUP_FILE} 2>&1 | grep -E 'dumping|complete'

# 复制备份文件到主机
docker compose -f docker-compose.prod.yml cp db:/tmp/${BACKUP_FILE} "${BACKUP_DIR}/${BACKUP_FILE}"

# 验证备份文件
if [ -f "${BACKUP_DIR}/${BACKUP_FILE}" ]; then
    SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_FILE}" | cut -f1)
    echo "✅ 备份完成"
    echo "文件: ${BACKUP_DIR}/${BACKUP_FILE}"
    echo "大小: ${SIZE}"

    # 记录备份日志
    echo "$(date '+%Y-%m-%d %H:%M:%S') | BACKUP | ${BACKUP_FILE} | ${SIZE}" >> /opt/graduation-leave-system/backup.log

    # 清理容器内临时文件
    docker compose -f docker-compose.prod.yml exec -T db rm -f /tmp/${BACKUP_FILE}

    # 保留最近7天的备份
    find "$BACKUP_DIR" -name "graduation_leave_prod_*.sql" -mtime +7 -delete

    echo ""
    echo "备份文件路径: ${BACKUP_DIR}/${BACKUP_FILE}"
    echo "备份可用于恢复: pg_restore -U postgres -d graduation_leave ${BACKUP_DIR}/${BACKUP_FILE}"
else
    echo "❌ 备份文件未生成"
    exit 1
fi
