#!/bin/bash
# 首次服务器初始化脚本

set -e

REMOTE_USER=${DEPLOY_USER:-root}
REMOTE_HOST=${DEPLOY_HOST}
REMOTE_PATH=${DEPLOY_PATH:-/opt/graduation-leave-system}
GIT_REPO=${GIT_REPO:-https://github.com/your-repo/graduation-leave-system.git}

echo "=== 服务器初始化 ==="
echo "目标: $REMOTE_USER@$REMOTE_HOST"
echo ""

# 1. 安装依赖
echo "1. 安装Docker和Git..."
ssh $REMOTE_USER@$REMOTE_HOST "apt update && apt install -y docker.io docker-compose git curl"

# 2. 克隆代码
echo ""
echo "2. 克隆项目..."
ssh $REMOTE_USER@$REMOTE_HOST "mkdir -p $REMOTE_PATH && cd $REMOTE_PATH && \
    git clone $GIT_REPO . || (cd $REMOTE_PATH && git pull)"

# 3. 配置环境
echo ""
echo "3. 配置生产环境..."
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && \
    cp .env.prod.example .env.prod && \
    echo '请手动编辑 $REMOTE_PATH/.env.prod 配置密钥'"

# 4. 初始化数据库
echo ""
echo "4. 启动服务并初始化..."
ssh $REMOTE_USER@$REMOTE_HOST "cd $REMOTE_PATH && \
    docker-compose -f docker-compose.prod.yml up -d && \
    sleep 15 && \
    docker-compose -f docker-compose.prod.yml exec -T backend python manage.py migrate && \
    docker-compose -f docker-compose.prod.yml exec -T backend python manage.py collectstatic --noinput"

echo ""
echo "=== 初始化完成 ==="
echo "下一步:"
echo "1. 编辑配置: ssh $REMOTE_USER@$REMOTE_HOST 'vim $REMOTE_PATH/.env.prod'"
echo "2. 创建管理员: ssh $REMOTE_USER@$REMOTE_HOST 'cd $REMOTE_PATH && docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser'"
echo "3. 重启服务: ssh $REMOTE_USER@$REMOTE_HOST 'cd $REMOTE_PATH && docker-compose -f docker-compose.prod.yml restart'"
