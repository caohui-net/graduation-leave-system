#!/bin/bash
# 部署环境验证脚本
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo_pass() { echo -e "${GREEN}✓${NC} $1"; }
echo_fail() { echo -e "${RED}✗${NC} $1"; }
echo_warn() { echo -e "${YELLOW}⚠${NC} $1"; }

ERRORS=0

echo "=== 部署环境验证 ==="
echo ""

# 1. 环境变量
echo "检查环境变量..."
[ -n "$DEPLOY_HOST" ] && echo_pass "DEPLOY_HOST: $DEPLOY_HOST" || { echo_fail "DEPLOY_HOST 未设置"; ERRORS=$((ERRORS+1)); }
[ -n "$DEPLOY_USER" ] && echo_pass "DEPLOY_USER: $DEPLOY_USER" || { echo_fail "DEPLOY_USER 未设置"; ERRORS=$((ERRORS+1)); }
echo ""

# 2. SSH连接
echo "检查SSH连接..."
if ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no $DEPLOY_USER@$DEPLOY_HOST "echo ok" > /dev/null 2>&1; then
    echo_pass "SSH连接正常"
else
    echo_fail "SSH连接失败"
    ERRORS=$((ERRORS+1))
fi
echo ""

# 3. 远程环境
echo "检查远程环境..."
REMOTE_CHECK=$(ssh $DEPLOY_USER@$DEPLOY_HOST "command -v docker && command -v git && echo ok" 2>/dev/null || echo "")
if [[ "$REMOTE_CHECK" == *"ok"* ]]; then
    echo_pass "Docker 和 Git 已安装"
else
    echo_fail "缺少 Docker 或 Git"
    ERRORS=$((ERRORS+1))
fi
echo ""

# 4. 远程目录
DEPLOY_PATH=${DEPLOY_PATH:-/opt/graduation-leave-system}
echo "检查远程目录: $DEPLOY_PATH"
if ssh $DEPLOY_USER@$DEPLOY_HOST "test -d $DEPLOY_PATH/.git" 2>/dev/null; then
    echo_pass "项目目录存在"
else
    echo_warn "项目目录不存在，需要首次初始化"
fi
echo ""

# 5. 本地Git状态
echo "检查本地Git状态..."
if git diff-index --quiet HEAD --; then
    echo_pass "工作区干净"
else
    echo_warn "有未提交的更改"
fi
echo ""

# 总结
echo "=== 验证结果 ==="
if [ $ERRORS -eq 0 ]; then
    echo_pass "环境验证通过，可以部署"
    exit 0
else
    echo_fail "发现 $ERRORS 个错误，请修复后重试"
    exit 1
fi
