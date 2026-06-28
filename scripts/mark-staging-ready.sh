#!/bin/bash
# 196服务器：标记staging环境已验证当前代码，可同步到production
# 执行时机：staging容器验证通过后
# 执行位置：ssh caohui@172.17.12.196

set -euo pipefail

DEV_HOST="172.17.12.199"
DEV_REPO="/home/caohui/projects/graduation-leave-system"
FLAG_FILE="/opt/graduation-leave-system/.staging-ready"

# 从开发机获取当前commit
COMMIT=$(ssh -o ConnectTimeout=5 "caohui@${DEV_HOST}" "cd ${DEV_REPO} && git rev-parse HEAD")
TIMESTAMP=$(date -Iseconds)

echo "${COMMIT}|${TIMESTAMP}" > "$FLAG_FILE"
echo "✓ 标记staging已验证: $COMMIT ($TIMESTAMP)"
echo "  生产监测脚本将在5分钟内检测到此标记"
