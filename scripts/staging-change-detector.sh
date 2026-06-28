#!/bin/bash
# Phase 1: 只读监测 - 检测staging与production代码差异
# 部署位置：生产服务器 cron 每5分钟执行

set -euo pipefail

STAGING_HOST="172.17.12.196"
STAGING_FLAG_PATH="/opt/graduation-leave-system-staging/.deployment-ready"
PROD_REPO="/opt/graduation-leave-system"
NOTIFY_LOG="/var/log/deployment-alerts.log"

# 读取staging变更标识
if ! STAGING_FLAG=$(ssh -o ConnectTimeout=5 "caohui@${STAGING_HOST}" "cat ${STAGING_FLAG_PATH} 2>/dev/null"); then
  echo "[$(date -Iseconds)] ⚠️  无法读取staging变更标识" | tee -a "$NOTIFY_LOG"
  exit 1
fi

STAGING_COMMIT="${STAGING_FLAG%%|*}"
STAGING_TIME="${STAGING_FLAG##*|}"

# 读取生产当前commit
cd "$PROD_REPO"
PROD_COMMIT=$(git rev-parse HEAD)

# 比较差异
if [[ "$STAGING_COMMIT" != "$PROD_COMMIT" ]]; then
  echo "[$(date -Iseconds)] 🔔 检测到代码差异" | tee -a "$NOTIFY_LOG"
  echo "  Staging: $STAGING_COMMIT (标记时间: $STAGING_TIME)" | tee -a "$NOTIFY_LOG"
  echo "  Production: $PROD_COMMIT" | tee -a "$NOTIFY_LOG"
  echo "  建议执行: cd /opt/graduation-leave-system && scripts/196-promote-to-prod.sh" | tee -a "$NOTIFY_LOG"
  exit 2
else
  echo "[$(date -Iseconds)] ✓ 代码一致: $PROD_COMMIT" >> "$NOTIFY_LOG"
fi
