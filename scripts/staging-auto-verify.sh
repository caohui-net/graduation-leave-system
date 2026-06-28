#!/bin/bash
# Phase 1.5: Staging自动验证和标记
# 在staging容器健康检查通过后自动执行

set -euo pipefail

STAGING_BACKEND_URL="http://localhost:17787"
STAGING_FRONTEND_URL="http://localhost:17788"
MARK_SCRIPT="/opt/graduation-leave-system/scripts/mark-staging-ready.sh"

# 1. 健康检查
echo "检查staging后端..."
if ! curl -sf "${STAGING_BACKEND_URL}/api/health" >/dev/null; then
  echo "❌ 后端健康检查失败"
  exit 1
fi

echo "检查staging前端..."
if ! curl -sf "${STAGING_FRONTEND_URL}" >/dev/null; then
  echo "❌ 前端健康检查失败"
  exit 1
fi

# 2. 可选：运行自动化测试
# pytest /opt/graduation-leave-system/backend/tests/integration/
# if [ $? -ne 0 ]; then
#   echo "❌ 自动化测试失败"
#   exit 1
# fi

# 3. 验证通过，自动标记
echo "✓ Staging验证通过，自动标记"
"$MARK_SCRIPT"
