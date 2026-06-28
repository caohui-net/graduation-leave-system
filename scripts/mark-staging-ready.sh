#!/bin/bash
# 测试环境：标记代码已完成测试，可发布到生产
# 执行时机：测试环境验证通过后

set -euo pipefail

FLAG_FILE="/opt/graduation-leave-system-staging/.deployment-ready"
COMMIT=$(git rev-parse HEAD)
TIMESTAMP=$(date -Iseconds)

echo "${COMMIT}|${TIMESTAMP}" > "$FLAG_FILE"
echo "✓ 标记staging已完成测试: $COMMIT ($TIMESTAMP)"
