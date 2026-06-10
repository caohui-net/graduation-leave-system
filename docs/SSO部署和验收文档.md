# 青橄榄SSO集成 - 部署文档

## 部署环境

**系统要求:**
- Ubuntu 26.04 LTS
- Docker 29.1.3+
- Docker Compose
- Python 3.11+
- PostgreSQL 15

**端口占用:**
- 7787: Backend API
- 5432: PostgreSQL
- 5000: 文件共享服务(dufs, 可选)

## 部署步骤

### 1. 环境配置

```bash
# 克隆仓库
git clone https://github.com/caohui-net/graduation-leave-system.git
cd graduation-leave-system

# 配置环境变量
cp .env.docker.example .env.docker  # 如果有示例文件
# 或直接编辑 .env.docker
```

**关键配置 (.env.docker):**
```bash
DEBUG=False
SECRET_KEY=<生产密钥>
JWT_SECRET_KEY=<JWT密钥>
ALLOWED_HOSTS=localhost,127.0.0.1,172.17.12.199,218.75.196.218

# 青橄榄SSO凭证
QGL_ADMIN_APP_KEY=cb6f276a42042179e90cd79c4126e075
QGL_ADMIN_APP_SECRET=da02720febcf47071ee5db78c2b068ec
QGL_MOBILE_TENANT_CODE=S10405
QGL_ADMIN_APPID=8uonta
QGL_ENV=prod

# JWT有效期
JWT_ACCESS_TOKEN_LIFETIME=86400    # 1天
JWT_REFRESH_TOKEN_LIFETIME=604800  # 7天

# CORS
CORS_ALLOWED_ORIGINS=http://218.75.196.218:7788

# Demo登录(生产必须禁用)
DEMO_AUTH_ENABLED=false
```

### 2. 启动服务

```bash
# 启动Docker容器
docker compose up -d

# 检查服务状态
docker compose ps

# 查看日志
docker compose logs -f backend
```

### 3. 数据库初始化

```bash
# 执行迁移
docker compose exec backend python manage.py migrate

# 创建超级用户(可选)
docker compose exec backend python manage.py createsuperuser
```

### 4. 验证部署

```bash
# 运行e2e测试
docker compose exec backend python test_sso_e2e.py

# 检查API健康
curl http://localhost:7787/api/health
```

## 青橄榄平台配置

**需要青橄榄方配置:**

1. **回调地址配置:**
   ```
   http://218.75.196.218:7788/admin-sso-callback.html
   ```

2. **应用信息:**
   - 应用名称: 毕业生离校申请审批系统
   - 租户号: S10405
   - APPID: 8uonta

3. **权限配置:**
   - 管理端单点登录权限
   - 移动端用户信息获取权限

## 验收标准

### 功能验收

**1. 管理端登录 (Admin SSO)**
- [ ] 青橄榄平台点击应用图标
- [ ] 自动跳转到 admin-sso-callback.html
- [ ] URL包含authorization参数
- [ ] 自动调用后端API验证
- [ ] 验证成功返回JWT token
- [ ] 自动创建本地User记录
- [ ] 跳转到管理后台首页

**测试URL:** `POST http://218.75.196.218:7787/api/sso/qingganlian/admin/login`

**请求示例:**
```json
{
  "authorization": "bearer <青橄榄token>"
}
```

**预期响应:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "user_code",
    "username": "user_code",
    "real_name": "管理员姓名",
    "role": "admin",
    "phone": "13800138000"
  }
}
```

**2. 移动端登录 (Mobile SSO)**
- [ ] 移动端获取saas_wap_token
- [ ] 调用后端API验证
- [ ] 返回JWT token
- [ ] 自动创建本地User记录
- [ ] 根据identity_name分配角色(学生/教师)

**测试URL:** `POST http://218.75.196.218:7787/api/sso/qingganlian/mobile/login`

**请求示例:**
```json
{
  "tenant_code": "S10405",
  "appid": "8uonta",
  "saas_wap_token": "<青橄榄移动端token>"
}
```

### 安全验收

- [ ] DEBUG=False (生产环境)
- [ ] AllowAny权限明确声明
- [ ] 必须调用青橄榄API验证token
- [ ] user_code空值检查生效
- [ ] 事务保护防止并发竞态
- [ ] API超时配置30s
- [ ] 本地密码登录已禁用

### 性能验证

- [ ] SSO登录响应时间 <3秒
- [ ] API超时设置30s生效
- [ ] 并发10个请求无IntegrityError
- [ ] JWT token有效期正确(1天/7天)

### 数据验证

**检查SSOUserMapping表:**
```sql
SELECT user_code, user_id, user_type, tenant_code, last_login_at 
FROM sso_qingganlian_ssousermapping 
ORDER BY last_login_at DESC 
LIMIT 10;
```

**检查User表:**
```sql
SELECT user_id, name, role, is_staff, active 
FROM users_user 
WHERE user_id IN (SELECT user_id FROM sso_qingganlian_ssousermapping)
LIMIT 10;
```

## 故障排查

### 问题1: 401 Token不正确

**原因:** 
- 青橄榄token已过期
- appkey/appsecret配置错误

**解决:**
```bash
# 检查配置
docker compose exec backend python -c "from apps.sso_qingganlian import settings; print(settings.QGL_ADMIN_APP_KEY)"

# 查看日志
docker compose logs backend | grep "SSO"
```

### 问题2: 用户标识缺失

**原因:** 
- 青橄榄API返回数据不含user_code/number

**解决:**
- 检查API响应日志
- 确认青橄榄API版本和字段名

### 问题3: IntegrityError duplicate key

**原因:** 
- 并发请求导致竞态条件

**验证修复:**
```bash
# 事务保护已添加，检查代码
grep "transaction.atomic" backend/apps/sso_qingganlian/views.py
```

## 监控指标

**推荐监控项:**
- SSO登录成功率
- SSO登录响应时间(p50/p95/p99)
- Token过期率
- 异常登录IP(可选)
- 青橄榄API错误率

**日志关键字:**
```
"Mobile login success"
"Admin login success"
"SSO API error"
"Token expired"
```

## 回滚方案

```bash
# 回滚到上一版本
git checkout <previous-commit>
docker compose down
docker compose up -d --build

# 或使用镜像tag
docker compose down
docker tag graduation-leave-system-backend:latest graduation-leave-system-backend:backup
docker compose up -d
```

## 联系方式

**技术支持:**
- 项目仓库: https://github.com/caohui-net/graduation-leave-system
- 问题反馈: GitHub Issues

**青橄榄平台对接:**
- 需与青橄榄技术支持联系配置回调地址

---

**文档版本:** v1.0  
**更新日期:** 2026-06-10  
**状态:** 生产就绪
