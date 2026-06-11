#!/bin/bash
# 配置systemd服务（需要sudo权限）

set -e

cd "$(dirname "$0")/.."

SERVICE_FILE="/etc/systemd/system/graduation-frontend.service"

echo "配置systemd服务需要sudo权限"
echo "请在终端执行以下命令："
echo ""
echo "sudo cp frontend-server.service $SERVICE_FILE"
echo "sudo systemctl daemon-reload"
echo "sudo systemctl enable graduation-frontend"
echo "sudo systemctl start graduation-frontend"
echo ""
echo "查看状态："
echo "sudo systemctl status graduation-frontend"
