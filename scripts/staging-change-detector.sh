#!/bin/bash
# Phase 1: 只读监测 - 三方对比（开发机/staging验证/生产版本）
# 部署位置：196生产服务器 cron 每5分钟执行

set -euo pipefail

DEV_HOST="172.17.12.199"
DEV_REPO="/home/caohui/projects/graduation-leave-system"
FLAG_FILE="/opt/graduation-leave-system/.staging-ready"
PROD_VERSION_FILE="/opt/graduation-leave-system/.production-version"
NOTIFY_LOG="/var/log/deployment-alerts.log"

# 读取开发机当前commit
if ! DEV_COMMIT=$(ssh -o ConnectTimeout=5 "caohui@${DEV_HOST}" "cd ${DEV_REPO} && git rev-parse HEAD 2>/dev/null"); then
  echo "[$(date -Iseconds)] ⚠️  无法读取开发机commit" | tee -a "$NOTIFY_LOG"
  exit 1
fi

# 读取staging验证标记
if [[ -f "$FLAG_FILE" ]]; then
  STAGING_FLAG=$(cat "$FLAG_FILE")
  STAGING_COMMIT="${STAGING_FLAG%%|*}"
  STAGING_TIME="${STAGING_FLAG##*|}"
else
  echo "[$(date -Iseconds)] ⚠️  未找到staging验证标记" | tee -a "$NOTIFY_LOG"
  exit 1
fi

# 读取生产实际版本
if [[ -f "$PROD_VERSION_FILE" ]]; then
  PROD_VERSION=$(cat "$PROD_VERSION_FILE")
  PROD_COMMIT="${PROD_VERSION%%|*}"
  PROD_TIME="${PROD_VERSION##*|}"
else
  PROD_COMMIT="unknown"
  PROD_TIME="未知"
fi

# 三方对比逻辑
DEV_VS_STAGING="$([[ "$DEV_COMMIT" == "$STAGING_COMMIT" ]] && echo "同步" || echo "有新代码")"
STAGING_VS_PROD="$([[ "$STAGING_COMMIT" == "$PROD_COMMIT" ]] && echo "已部署" || echo "待部署")"

# 告警条件1：开发机有新代码未验证
if [[ "$DEV_COMMIT" != "$STAGING_COMMIT" ]]; then
  echo "[$(date -Iseconds)] 🔔 检测到新代码（未验证）" | tee -a "$NOTIFY_LOG"
  echo "  开发机: $DEV_COMMIT" | tee -a "$NOTIFY_LOG"
  echo "  Staging已验证: $STAGING_COMMIT ($STAGING_TIME)" | tee -a "$NOTIFY_LOG"
  echo "  生产版本: $PROD_COMMIT ($PROD_TIME)" | tee -a "$NOTIFY_LOG"
  echo "  → 建议先在staging验证新代码" | tee -a "$NOTIFY_LOG"
fi

# 告警条件2：staging已验证但未部署到生产
if [[ "$STAGING_COMMIT" != "$PROD_COMMIT" ]] && [[ "$DEV_COMMIT" == "$STAGING_COMMIT" ]]; then
  echo "[$(date -Iseconds)] ⚠️  Staging已验证但未同步到生产" | tee -a "$NOTIFY_LOG"
  echo "  Staging已验证: $STAGING_COMMIT ($STAGING_TIME)" | tee -a "$NOTIFY_LOG"
  echo "  生产版本: $PROD_COMMIT ($PROD_TIME)" | tee -a "$NOTIFY_LOG"
  echo "  → 执行: scripts/196-promote-to-prod.sh" | tee -a "$NOTIFY_LOG"
fi

# 正常状态：三方一致
if [[ "$DEV_COMMIT" == "$STAGING_COMMIT" ]] && [[ "$STAGING_COMMIT" == "$PROD_COMMIT" ]]; then
  echo "[$(date -Iseconds)] ✓ 三方同步：开发/staging/生产版本一致" >> "$NOTIFY_LOG"
fi

