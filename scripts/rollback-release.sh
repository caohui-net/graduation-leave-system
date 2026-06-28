#!/bin/bash
set -euo pipefail

# 回滚到指定的release版本
# 依赖: release manifest机制（任务#26）
# 用法: rollback-release.sh <release_id>
# 示例: rollback-release.sh 20260628_012345-abc1234

RELEASE_ID="${1:-}"
RELEASES_DIR="/opt/graduation-leave-system/releases"
PROD="/opt/graduation-leave-system/production"

# 参数检查
if [[ -z "$RELEASE_ID" ]]; then
  echo "❌ 用法: $0 <release_id>"
  echo "示例: $0 20260628_012345-abc1234"
  exit 1
fi

RELEASE_PATH="$RELEASES_DIR/$RELEASE_ID"
MANIFEST="$RELEASE_PATH/manifest.json"

# 检查release是否存在
if [[ ! -d "$RELEASE_PATH" ]]; then
  echo "❌ Release不存在: $RELEASE_PATH"
  echo ""
  echo "可用的releases:"
  ls -1 "$RELEASES_DIR" 2>/dev/null || echo "  (无)"
  exit 1
fi

# 检查manifest
if [[ ! -f "$MANIFEST" ]]; then
  echo "❌ Manifest不存在: $MANIFEST"
  echo "此release可能不完整或损坏"
  exit 1
fi

# 读取manifest
echo "=== 读取release信息 ==="
GIT_HASH=$(jq -r '.git_hash' "$MANIFEST")
TIMESTAMP=$(jq -r '.timestamp' "$MANIFEST")
OPERATOR=$(jq -r '.operator // "unknown"' "$MANIFEST")
MIGRATION_BEFORE=$(jq -r '.migration_state.before // "unknown"' "$MANIFEST")
MIGRATION_AFTER=$(jq -r '.migration_state.after // "unknown"' "$MANIFEST")

echo "Release ID: $RELEASE_ID"
echo "Git Hash:   $GIT_HASH"
echo "时间:       $TIMESTAMP"
echo "操作者:     $OPERATOR"
echo ""

# DB migration警告
if [[ "$MIGRATION_BEFORE" != "$MIGRATION_AFTER" ]]; then
  echo "⚠️  警告：此release涉及数据库迁移"
  echo "回滚前状态: $MIGRATION_BEFORE"
  echo "回滚后状态: $MIGRATION_AFTER"
  echo ""
  echo "回滚可能需要手动执行数据库迁移回退"
  echo "请确认："
  echo "  1. 已备份当前数据库"
  echo "  2. 已准备migration回退脚本"
  echo "  3. 了解数据丢失风险"
  echo ""
  read -p "是否继续回滚？(输入 YES 继续): " CONFIRM
  if [[ "$CONFIRM" != "YES" ]]; then
    echo "❌ 回滚已取消"
    exit 1
  fi
fi

# 最后确认
echo "=== 最终确认 ==="
echo "即将回滚生产环境到:"
echo "  Release: $RELEASE_ID"
echo "  Git:     $GIT_HASH"
echo "  时间:    $TIMESTAMP"
echo ""
read -p "确认执行回滚？(输入 YES 继续): " FINAL_CONFIRM
if [[ "$FINAL_CONFIRM" != "YES" ]]; then
  echo "❌ 回滚已取消"
  exit 1
fi

# 备份当前生产环境
echo "=== 备份当前生产环境 ==="
BACKUP_DIR="/opt/graduation-leave-system/backups/rollback-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
rsync -a "$PROD/" "$BACKUP_DIR/" --exclude='media' --exclude='*.log'
echo "✅ 备份完成: $BACKUP_DIR"

# 回滚代码
echo "=== 回滚代码 ==="
rsync -a --delete "$RELEASE_PATH/code/" "$PROD/" \
  --exclude='media' \
  --exclude='*.log' \
  --exclude='.env*'
echo "✅ 代码已回滚"

# 回滚配置（如果manifest中有配置备份）
if [[ -f "$RELEASE_PATH/config.env" ]]; then
  echo "=== 回滚配置 ==="
  cp "$RELEASE_PATH/config.env" "$PROD/.env"
  echo "✅ 配置已回滚"
fi

# 清理Python缓存
echo "=== 清理缓存 ==="
find "$PROD/backend" -type f -name "*.pyc" -delete 2>/dev/null || true
find "$PROD/backend" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# 重启服务
echo "=== 重启服务 ==="
cd "$PROD"
docker-compose restart backend
docker restart prod-graduation-frontend 2>/dev/null || true

# 等待服务启动
echo "=== 等待服务就绪 ==="
sleep 8

# 健康检查
echo "=== 健康检查 ==="
BACKEND_OK=false
FRONTEND_OK=false

if curl -sf http://localhost:8000/api/health > /dev/null 2>&1; then
  echo "✅ 后端健康检查通过"
  BACKEND_OK=true
else
  echo "❌ 后端健康检查失败"
fi

if curl -sf http://localhost:7788 > /dev/null 2>&1; then
  echo "✅ 前端健康检查通过"
  FRONTEND_OK=true
else
  echo "⚠️  前端健康检查失败（或未运行）"
fi

# 记录回滚
echo "=== 记录回滚操作 ==="
echo "$(date -Iseconds) ROLLBACK to $RELEASE_ID ($GIT_HASH) by $(whoami)" >> "$PROD/rollback.log"

# 最终报告
echo ""
echo "=== 回滚完成 ==="
echo "目标版本: $RELEASE_ID"
echo "Git Hash: $GIT_HASH"
echo "备份位置: $BACKUP_DIR"
echo ""

if [[ "$BACKEND_OK" == "true" ]]; then
  echo "✅ 回滚成功"
  exit 0
else
  echo "⚠️  回滚完成，但服务可能未正常启动"
  echo "请检查日志: docker-compose logs -f backend"
  exit 1
fi
