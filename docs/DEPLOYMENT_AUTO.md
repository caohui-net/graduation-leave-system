# 异地自动化部署指南

## 快速开始

### 1. 配置GitHub Secrets

在GitHub仓库 Settings → Secrets and variables → Actions 添加：

```
DEPLOY_USER=root
DEPLOY_HOST=218.75.196.218
DEPLOY_SSH_KEY=<服务器SSH私钥内容>
```

### 2. 首次部署服务器

```bash
# 设置环境变量
export DEPLOY_USER=root
export DEPLOY_HOST=218.75.196.218
export DEPLOY_PATH=/opt/graduation-leave-system
export GIT_REPO=https://github.com/your-repo/graduation-leave-system.git

# 初始化服务器
chmod +x scripts/setup_server.sh
./scripts/setup_server.sh

# 配置生产环境
ssh $DEPLOY_USER@$DEPLOY_HOST "vim $DEPLOY_PATH/.env.prod"

# 重启服务
ssh $DEPLOY_USER@$DEPLOY_HOST "cd $DEPLOY_PATH && docker-compose -f docker-compose.prod.yml restart"
```

### 3. 自动化部署

推送代码到main分支自动触发部署：

```bash
git add .
git commit -m "feat: 新功能"
git push origin main
```

GitHub Actions自动执行：
1. ✓ 代码checkout
2. ✓ SSH连接服务器
3. ✓ 备份当前版本（配置+数据库+Git SHA）
4. ✓ 拉取最新代码
5. ✓ 构建Docker镜像
6. ✓ 数据库迁移
7. ✓ 滚动更新服务
8. ✓ 健康检查（/readyz端点验证DB连接）
9. ✓ 失败自动回滚（恢复配置+数据库+代码版本）

## 手动部署

```bash
# 部署到生产环境
export DEPLOY_HOST=218.75.196.218
export DEPLOY_USER=root
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## 回滚操作

```bash
# 自动回滚到上一个版本
export DEPLOY_HOST=218.75.196.218
export DEPLOY_USER=root
chmod +x scripts/rollback.sh
./scripts/rollback.sh
```

## 多环境部署

编辑 `deploy.config.yml` 配置多个环境：

```yaml
environments:
  - name: staging
    host: staging.example.com
    branch: develop
  
  - name: production
    host: 218.75.196.218
    branch: main
```

部署到指定环境：

```bash
export DEPLOY_ENV=staging
export DEPLOY_HOST=staging.example.com
./scripts/deploy.sh
```

## 监控与验证

### 查看部署日志
```bash
# GitHub Actions日志
访问：https://github.com/your-repo/actions

# 服务器日志
ssh $DEPLOY_USER@$DEPLOY_HOST "cd $DEPLOY_PATH && docker-compose -f docker-compose.prod.yml logs -f --tail=100"
```

### 健康检查
```bash
curl http://$DEPLOY_HOST:7787/api/applications/
```

### 服务状态
```bash
ssh $DEPLOY_USER@$DEPLOY_HOST "cd $DEPLOY_PATH && docker-compose -f docker-compose.prod.yml ps"
```

## 故障排查

### 部署失败
1. 检查GitHub Actions日志
2. SSH登录服务器查看Docker日志
3. 执行回滚脚本恢复服务

### 健康检查失败
```bash
# 查看后端日志
ssh $DEPLOY_USER@$DEPLOY_HOST "docker logs graduation-leave-system-backend-1"

# 检查数据库连接
ssh $DEPLOY_USER@$DEPLOY_HOST "cd $DEPLOY_PATH && docker-compose -f docker-compose.prod.yml exec backend python manage.py check"
```

### 回滚失败
```bash
# 手动恢复最近的备份
ssh $DEPLOY_USER@$DEPLOY_HOST "ls -lt /tmp/backup_*.tar.gz | head -1"
ssh $DEPLOY_USER@$DEPLOY_HOST "cd $DEPLOY_PATH && tar -xzf /tmp/backup_YYYYMMDD_HHMMSS.tar.gz"
ssh $DEPLOY_USER@$DEPLOY_HOST "cd $DEPLOY_PATH && docker-compose -f docker-compose.prod.yml up -d --force-recreate"
```

## 安全配置

### SSH密钥生成
```bash
ssh-keygen -t ed25519 -C "deploy@graduation-leave-system" -f deploy_key
# 将公钥添加到服务器: ~/.ssh/authorized_keys
# 将私钥内容添加到GitHub Secrets: DEPLOY_SSH_KEY
```

### 环境变量加密
- 敏感信息存储在GitHub Secrets
- 服务器.env.prod文件权限设置为600
- 定期更新密钥

## 性能优化

### 减少部署时间
- 使用Docker层缓存
- 仅构建变更的服务
- 并行执行独立任务

### 零停机部署
当前方案：滚动更新（5-10秒停机）

升级方案（可选）：
- Nginx反向代理 + 蓝绿部署
- 需要双倍资源

## 备份策略

自动备份：
- 每次部署前自动备份
- 保留最近7天备份
- 位置：`/tmp/backup_*.tar.gz`

手动备份：
```bash
ssh $DEPLOY_USER@$DEPLOY_HOST "cd $DEPLOY_PATH && tar -czf ~/manual_backup_$(date +%Y%m%d).tar.gz docker-compose.prod.yml .env.prod"
```
