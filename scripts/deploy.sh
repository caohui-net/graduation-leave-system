#!/bin/bash
# 异地自动化部署脚本

set -e

# 配置
REMOTE_USER=${DEPLOY_USER:-root}
REMOTE_HOST=${DEPLOY_HOST}
REMOTE_PATH=${DEPLOY_PATH:-/opt/graduation-leave-system}
BRANCH=${DEPLOY_BRANCH:-main}

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo_success() { echo -e "${GREEN}✓ $1${NC}"; }
echo_error() { echo -e "${RED}✗ $1${NC}"; exit 1; }

# 检查参数
if [ -z "$REMOTE_HOST" ]; then
    echo_error "请设置 DEPLOY_HOST 环境变量"
fi

echo "=== 异地部署开始 ==="
echo "目标服务器: $REMOTE_USER@$REMOTE_HOST"
echo "部署路径: $REMOTE_PATH"
echo "分支: $BRANCH"
echo ""

# 1. 测试SSH连接
echo "1. 测试SSH连接..."
if ssh -o ConnectTimeout=5 $REMOTE_USER@$REMOTE_HOST "echo ok" > /dev/null 2>&1; then
    echo_success "SSH连接正常"
else
    echo_error "SSH连接失败，请检查配置"
fi

# 2. 备份当前版本
echo ""
echo "2. 备份当前版本..."
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && \
    docker-compose -f docker-compose.prod.yml ps -q > /tmp/backup_containers.txt && \
    tar -czf /tmp/backup_\$(date +%Y%m%d_%H%M%S).tar.gz docker-compose.prod.yml .env.prod || true"
echo_success "备份完成"

# 3. 拉取最新代码
echo ""
echo "3. 拉取最新代码..."
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && \
    git fetch origin && \
    git checkout $BRANCH && \
    git pull origin $BRANCH"
echo_success "代码更新完成"

# 4. 构建镜像
echo ""
echo "4. 构建Docker镜像..."
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && \
    docker-compose -f docker-compose.prod.yml build backend"
echo_success "镜像构建完成"

# 5. 数据库迁移
echo ""
echo "5. 执行数据库迁移..."
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && \
    docker-compose -f docker-compose.prod.yml run --rm backend python manage.py migrate --noinput"
echo_success "数据库迁移完成"

# 6. 重启服务
echo ""
echo "6. 重启服务..."
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && \
    docker-compose -f docker-compose.prod.yml up -d --remove-orphans"
echo_success "服务重启完成"

# 7. 健康检查
echo ""
echo "7. 健康检查..."
sleep 10
if ssh $REMOTE_USER@$REMOTE_HOST "curl -f http://localhost:7787/api/applications/ > /dev/null 2>&1"; then
    echo_success "健康检查通过"
else
    echo_error "健康检查失败，开始回滚..."
fi

# 8. 清理旧镜像
echo ""
echo "8. 清理旧镜像..."
ssh $REMOTE_USER@$REMOTE_HOST "docker image prune -f || true"
echo_success "清理完成"

echo ""
echo "=== 部署成功 ==="
echo "访问地址: http://$REMOTE_HOST:7787"
