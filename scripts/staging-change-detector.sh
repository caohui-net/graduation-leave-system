#!/bin/bash
# Phase 1: 只读监测 - 检测开发机代码与生产代码差异
# 部署位置：196生产服务器 cron 每5分钟执行

set -euo pipefail

DEV_HOST="172.17.12.199"
DEV_REPO="/home/caohui/projects/graduation-leave-system"
FLAG_FILE="/opt/graduation-leave-system/.staging-ready"
NOTIFY_LOG="/var/log/deployment-alerts.log"

# 读取开发机当前commit
if ! DEV_COMMIT=$(ssh -o ConnectTimeout=5 "caohui@${DEV_HOST}" "cd ${DEV_REPO} && git rev-parse HEAD 2>/dev/null"); then
  echo "[$(date -Iseconds)] ⚠️  无法读取开发机commit" | tee -a "$NOTIFY_LOG"
  exit 1
fi

# 读取本地标记的staging已验证commit
if [[ -f "$FLAG_FILE" ]]; then
  STAGING_FLAG=$(cat "$FLAG_FILE")
  STAGING_COMMIT="${STAGING_FLAG%%|*}"
  STAGING_TIME="${STAGING_FLAG##*|}"
else
  echo "[$(date -Iseconds)] ⚠️  未找到staging验证标记" | tee -a "$NOTIFY_LOG"
  exit 1
fi

# 比较开发机最新代码与staging已验证commit
if [[ "$DEV_COMMIT" != "$STAGING_COMMIT" ]]; then
  echo "[$(date -Iseconds)] 🔔 检测到新代码" | tee -a "$NOTIFY_LOG"
  echo "  开发机最新: $DEV_COMMIT" | tee -a "$NOTIFY_LOG"
  echo "  Staging已验证: $STAGING_COMMIT (时间: $STAGING_TIME)" | tee -a "$NOTIFY_LOG"
  echo "  建议先在staging验证新代码，然后执行: scripts/196-promote-to-prod.sh" | tee -a "$NOTIFY_LOG"
  exit 2
else
  echo "[$(date -Iseconds)] ✓ 开发机代码已在staging验证通过，可发布" >> "$NOTIFY_LOG"
fi
