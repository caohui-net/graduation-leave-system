# 青橄榄平台SSO对接模块

## 快速开始

### 1. 安装依赖

```bash
pip install python-decouple djangorestframework-simplejwt
```

### 2. 配置环境变量

在项目根目录创建 `.env` 文件（生产环境）或在 `backend/config/settings/dev.py` 中配置：

```bash
# 移动端配置
QGL_MOBILE_APP_KEY=your_mobile_app_key
QGL_MOBILE_APP_SECRET=your_mobile_app_secret
QGL_MOBILE_TENANT_CODE=C10026
QGL_MOBILE_APPID=c6qgh2

# 管理端配置
QGL_ADMIN_APP_KEY=your_admin_app_key
QGL_ADMIN_APP_SECRET=your_admin_app_secret

# 环境设置
QGL_ENV=prod  # dev or prod
```

### 3. 数据库迁移

```bash
cd backend
python manage.py makemigrations sso_qingganlian
python manage.py migrate
```

### 4. 验证配置

```bash
python manage.py shell
>>> from apps.sso_qingganlian import settings as sso_settings
>>> print(sso_settings.QGL_MOBILE_APP_KEY)
>>> print(sso_settings.QGL_ENV)
```

## API端点

### 移动端登录

**POST** `/api/sso/qingganlian/mobile/login`

**请求体：**
```json
{
  "tenant_code": "C10026",
  "appid": "c6qgh2",
  "saas_wap_token": "user_token_from_qingganlian"
}
```

**响应：**
```json
{
  "token": "jwt_access_token",
  "user": {
    "id": 1,
    "username": "2024220220323",
    "real_name": "张三",
    "role": "student",
    "phone": "13800138000"
  }
}
```

### 管理端登录

**POST** `/api/sso/qingganlian/admin/login`

**请求体：**
```json
{
  "authorization": "admin_token_from_qingganlian"
}
```

**响应：**
```json
{
  "token": "jwt_access_token",
  "user": {
    "id": 2,
    "username": "admin001",
    "real_name": "管理员",
    "role": "admin",
    "phone": "13900139000"
  }
}
```

## 错误处理

- `88890006`: TOKEN已使用或已过期 → 返回401
- `88890007`: 用户信息获取失败 → 返回401
- 其他错误码 → 返回400并附带错误信息

## 架构说明

详细设计文档见：`docs/design/2026-06-08-sso-qingganlian-integration.md`

**模块结构：**
- `models.py`: SSOUserMapping用户映射表
- `auth.py`: 签名生成工具
- `client.py`: 青橄榄API客户端
- `serializers.py`: 请求/响应序列化器
- `views.py`: 登录API视图
- `exceptions.py`: 自定义异常
- `settings.py`: 配置管理

**工作流程：**
1. 前端从青橄榄获取token
2. POST到对应登录端点
3. 后端调用青橄榄API验证token并获取用户信息
4. 创建/更新本地User和SSOUserMapping
5. 生成JWT token返回前端

## 安全注意事项

1. **生产环境必须配置真实的APP_KEY和APP_SECRET**
2. 不要将`.env`文件提交到版本控制
3. 使用HTTPS保护API通信
4. JWT token有效期默认1小时（可通过SIMPLE_JWT配置调整）

## 测试

待补充集成测试和单元测试。

## Phase 4优化（已实施）

- [x] 添加日志记录（请求/响应/错误）
- [x] 性能优化（requests.Session连接池）
- [x] 完善错误处理（自定义异常体系）
- [x] API文档生成（本README）
- [ ] 单元测试和集成测试
- [ ] **真实环境联调测试**（待青橄榄平台appKey/appSecret配置）

## 生产部署前提条件

**⚠️ 重要：本模块代码已完成，但尚未与青橄榄平台进行真实联调验证**

部署前必须完成：
1. 获取真实的青橄榄平台appKey/appSecret（联系平台管理员）
2. 配置真实的环境变量（替换.env中的默认值）
3. 执行端到端联调测试，验证：
   - 移动端token换取和用户信息获取
   - 管理端authorization验证
   - 错误场景处理（token过期、用户信息获取失败等）
4. 记录联调测试日志作为验证证据

**当前状态：** 代码开发完成，待真实环境联调验证后可投产。
