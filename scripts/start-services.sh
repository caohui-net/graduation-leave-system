#!/bin/bash
# 启动毕业离校系统所有服务

set -e

cd "$(dirname "$0")/.."

echo "=== 启动后端服务 ==="
docker compose up -d

echo "=== 等待后端就绪 ==="
sleep 5

echo "=== 启动前端服务 ==="
if pgrep -f "python3 -m http.server 7788" > /dev/null; then
    echo "前端服务已运行"
else
    cd demo-web
    nohup python3 -m http.server 7788 > ../logs/frontend.log 2>&1 &
    echo "前端服务已启动 (PID: $!)"
fi

echo ""
echo "=== 服务状态 ==="
docker compose ps
echo ""
echo "前端: http://218.75.196.218:7788"
echo "后端: http://218.75.196.218:7787"
