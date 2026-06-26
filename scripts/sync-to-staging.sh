#!/bin/bash
# 从开发环境同步代码到196 staging环境
set -euo pipefail

REMOTE_USER="caohui"
REMOTE_HOST="172.17.12.196"
STAGING_PATH="/opt/graduation-leave-system/staging"

EXCLUDES=(
  --exclude='.git' --exclude='backend/venv' --exclude='backend/__pycache__'
  --exclude='.env.*' --exclude='node_modules' --exclude='.claude'
  --exclude='.omc' --exclude='.wolf' --exclude='.trellis' --exclude='.collab'
  --exclude='.codegraph' --exclude='.codex' --exclude='.agents'
  --exclude='.venv*' --exclude='__pycache__' --exclude='backups'
  --exclude='.envs' --exclude='.secrets'
  --exclude='.gemini' --exclude='.planning' --exclude='.understand-anything'
  --exclude='.pytest_cache' --exclude='logs' --exclude='backend/media'
)

echo '=== 同步代码到staging环境 ==='
rsync -av --delete "${EXCLUDES[@]}" \
  ./ "${REMOTE_USER}@${REMOTE_HOST}:${STAGING_PATH}/"

echo '=== 重启staging容器 ==='
ssh "${REMOTE_USER}@${REMOTE_HOST}" \
  "cd ${STAGING_PATH} && docker compose -f docker-compose.staging.yml restart"

echo '=== 数据初始化（辅导员+学生分配）==='
bash "$(dirname "$0")/init-data.sh" staging

echo '✅ 同步完成'
