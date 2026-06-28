#!/bin/bash
# 提醒脚本：代码推送后提醒验证staging
# 手动执行: ./scripts/remind-verify-staging.sh

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔔 提醒：验证Staging环境"
echo ""
echo "操作步骤："
echo "  1. 等待staging同步代码（NFS/rsync）"
echo "  2. 访问 http://172.17.12.196:17788"
echo "  3. 手动测试功能是否正常"
echo "  4. 验证通过后执行："
echo "     ./scripts/remind-mark-ready.sh"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
