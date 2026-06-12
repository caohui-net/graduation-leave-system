#!/bin/bash
# 一键自动化部署 - 完整流程
set -e

# 颜色
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo_step() { echo -e "${BLUE}▶ $1${NC}"; }
echo_success() { echo -e "${GREEN}✓ $1${NC}"; }
echo_error() { echo -e "${RED}✗ $1${NC}"; exit 1; }

# 配置检查
REMOTE_USER=${DEPLOY_USER:-root}
REMOTE_HOST=${DEPLOY_HOST}
REMOTE_PATH=${DEPLOY_PATH:-/opt/graduation-leave-system}

[ -z "$REMOTE_HOST" ] && echo_error "Set DEPLOY_HOST environment variable"

echo "=== 自动化部署 ==="
echo "Target: $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH"
echo ""

# 1. 本地测试
echo_step "1. 运行本地测试"
cd backend && python manage.py test --settings=config.settings.test && cd .. || echo_error "Tests failed"
echo_success "Tests passed"

# 2. Git推送
echo_step "2. 推送代码到远程仓库"
git push origin main || echo_error "Git push failed"
echo_success "Code pushed"

# 3. 触发远程部署
echo_step "3. 执行远程部署"
ssh -o ConnectTimeout=5 $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && bash scripts/deploy.sh" || echo_error "Deployment failed"
echo_success "Deployment completed"

# 4. 健康检查验证
echo_step "4. 验证服务健康"
sleep 5
if curl -f http://$REMOTE_HOST:7787/readyz > /dev/null 2>&1; then
    echo_success "Service healthy"
else
    echo_error "Health check failed"
fi

echo ""
echo "=== 部署成功 ==="
echo "访问: http://$REMOTE_HOST:7787"
