#!/bin/bash
# 提醒脚本：Staging验证通过后提醒标记
# 手动执行: ./scripts/remind-mark-ready.sh

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Staging验证完成"
echo ""
echo "标记为可发布，执行以下命令："
echo ""
echo "  ssh caohui@172.17.12.196 '/opt/graduation-leave-system/scripts/mark-staging-ready.sh'"
echo ""
echo "标记后，生产监测将在5分钟内检测到差异并写入日志："
echo "  /var/log/deployment-alerts.log"
echo ""
echo "查看日志后手动发布到生产："
echo "  ssh caohui@172.17.12.196 'cd /opt/graduation-leave-system && scripts/196-promote-to-prod.sh'"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
