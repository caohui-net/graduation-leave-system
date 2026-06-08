# 青橄榄平台SSO对接模块技术设计

**创建日期：** 2026-06-08  
**状态：** 设计阶段  
**审核：** Gemini三方讨论达成共识（3轮）

---

## 1. 概述

### 1.1 背景

系统需要对接青橄榄平台（goliveplus.cn），实现单点登录（SSO）功能，支持：
- **移动端**：学生/教师通过青橄榄移动应用登录
- **后台管理端**：管理员通过一站式管理平台跳转登录

### 1.2 设计目标

- 创建**功能独立**的SSO对接模块，与核心认证系统解耦
- 支持双端认证流程（移动端C端 + 管理端B端）
- 建立本地用户映射表，减少冗余API调用
- 统一会话管理：交换SSO token为本地JWT

### 1.3 设计原则

- **单一职责原则**：SSO逻辑隔离在独立模块
- **标准OAuth流程**：回调端点交换token，而非middleware拦截
- **性能优先**：本地映射表缓存用户信息
- **容错设计**：青橄榄接口不可用时的降级方案

---

## 2. 架构设计

### 2.1 模块结构

```
backend/apps/sso_qingganlian/
├── __init__.py
├── models.py           # 用户映射表模型
├── client.py           # 青橄榄API客户端封装
├── auth.py             # 签名生成、token验证工具
├── views.py            # API端点（移动端+管理端登录）
├── serializers.py      # 数据序列化
├── urls.py             # 路由配置
├── exceptions.py       # 自定义异常
├── settings.py         # 配置管理（appKey/appSecret）
└── tests/
    ├── test_client.py
    ├── test_auth.py
    └── test_views.py
```

### 2.2 核心组件

#### 2.2.1 用户映射表 (models.py)

```python
class SSOUserMapping(models.Model):
    """青橄榄用户 → 本地用户映射表"""
    
    # 本地用户
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sso_mapping')
    
    # 青橄榄标识
    tenant_code = models.CharField(max_length=50)  # 租户Code
    user_code = models.CharField(max_length=200, unique=True, null=True, blank=True)  # 移动端user_code
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)  # 管理端username
    
    # 用户类型
    user_type = models.CharField(max_length=20, choices=[
        ('mobile_student', '移动端-学生'),
        ('mobile_teacher', '移动端-教师'),
        ('admin', '管理端-管理员'),
    ])
    
    # 青橄榄用户信息快照（避免频繁调用API）
    real_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    identity_name = models.CharField(max_length=50, blank=True)  # 学生/教师/管理员
    role_name = models.CharField(max_length=100, blank=True)  # 青橄榄角色名
    
    # 元数据
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'sso_user_mapping'
        indexes = [
            models.Index(fields=['user_code']),
            models.Index(fields=['username']),
        ]
```

#### 2.2.2 API客户端 (client.py)

```python
class QingganlanClient:
    """青橄榄平台API客户端"""
    
    def __init__(self, app_key: str, app_secret: str, env: str = 'prod'):
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = self._get_base_url(env)
    
    # 移动端接口
    def get_user_code_by_token(self, tenant_code: str, appid: str, saas_wap_token: str) -> dict:
        """Token换取user_code"""
        pass
    
    def get_user_info(self, tenant_code: str, user_code: str, user_type: str) -> dict:
        """获取用户详细信息"""
        pass
    
    # 管理端接口
    def verify_admin_user(self, token: str) -> dict:
        """验证管理员用户"""
        pass
    
    def _generate_signature(self, timestamp: str, rand_str: str, encryption_type: str = 'sha1') -> str:
        """生成签名"""
        pass
```

#### 2.2.3 认证视图 (views.py)

```python
# 移动端登录端点
POST /api/sso/qingganlian/mobile/login
Request Body:
{
    "tenant_code": "C10026",
    "appid": "c6qgh2",
    "saas_wap_token": "..."
}
Response:
{
    "token": "<local_jwt>",
    "user": {
        "id": 123,
        "username": "2024220220323",
        "real_name": "白小娟",
        "role": "student"
    }
}

# 管理端登录端点
POST /api/sso/qingganlian/admin/login
Request Body:
{
    "authorization": "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
Response:
{
    "token": "<local_jwt>",
    "user": {
        "id": 456,
        "username": "golive",
        "real_name": "管理员姓名",
        "role": "admin"
    }
}
```

---

## 3. 认证流程

### 3.1 移动端登录流程

```
[前端] → [青橄榄移动应用] → 获取 saas_wap_token
  ↓
[前端] POST /api/sso/qingganlian/mobile/login
  {
    tenant_code: "C10026",
    appid: "c6qgh2",
    saas_wap_token: "..."
  }
  ↓
[后端] 1. 调用青橄榄 API: Token → user_code
       2. 调用青橄榄 API: user_code → 用户信息
       3. 查询/创建 SSOUserMapping
       4. 查询/创建本地 User (匹配学号/工号)
       5. 生成本地 JWT token
  ↓
[后端] 返回 {token: <local_jwt>, user: {...}}
  ↓
[前端] 存储 token，后续请求携带 Authorization: Bearer <local_jwt>
```

### 3.2 管理端登录流程

```
[用户] → [一站式管理平台] → 点击应用
  ↓
[平台] 跳转 https://graduation-leave-system/?Authorization=bearer%20eyJ0...
  ↓
[前端] 解析 URL 参数，提取 Authorization token
  ↓
[前端] POST /api/sso/qingganlian/admin/login
  {
    authorization: "bearer eyJ0eXAi..."
  }
  ↓
[后端] 1. 调用青橄榄 API: verify-user
       2. 查询/创建 SSOUserMapping
       3. 查询/创建本地 User (管理员角色)
       4. 生成本地 JWT token
  ↓
[后端] 返回 {token: <local_jwt>, user: {...}}
  ↓
[前端] 存储 token，后续请求携带 Authorization: Bearer <local_jwt>
```

---

## 4. 数据映射策略

### 4.1 移动端用户映射

| 青橄榄字段 | 本地User字段 | 映射逻辑 |
|-----------|-------------|---------|
| user_code | SSOUserMapping.user_code | 唯一标识 |
| real_name | User.first_name + last_name | 分割姓名 |
| number | User.username | 学号/工号 |
| identity_name | User角色 | "学生"→student, "教师"→teacher |
| phone | User.email (暂存) | 或扩展User模型 |

### 4.2 管理端用户映射

| 青橄榄字段 | 本地User字段 | 映射逻辑 |
|-----------|-------------|---------|
| username | SSOUserMapping.username | 管理员登录名 |
| name | User.first_name + last_name | 管理员姓名 |
| role_name | User角色 | 映射为admin或custom_role |
| phone | User.email (暂存) | 或扩展User模型 |

### 4.3 本地User创建规则

```python
# 移动端：优先匹配学号/工号
user = User.objects.filter(username=qgl_number).first()
if not user:
    user = User.objects.create(
        username=qgl_number,
        first_name=qgl_real_name[:10],
        last_name=qgl_real_name[10:] if len(qgl_real_name) > 10 else '',
        is_active=True
    )
    # 分配角色
    if qgl_identity == "学生":
        assign_role(user, "student")
    elif qgl_identity == "教师":
        assign_role(user, "teacher")

# 管理端：创建管理员用户
user = User.objects.filter(username=qgl_username).first()
if not user:
    user = User.objects.create(
        username=qgl_username,
        first_name=qgl_name[:10],
        last_name=qgl_name[10:] if len(qgl_name) > 10 else '',
        is_staff=True,
        is_active=True
    )
    assign_role(user, "admin")
```

---

## 5. 配置管理

### 5.1 环境配置

```python
# settings.py or .env

# 青橄榄移动端配置
QGL_MOBILE_APP_KEY = 'abc0a32aa8dd94d1f765841abaafd8ba'
QGL_MOBILE_APP_SECRET = 'b1d2efa9587446d80ce6388e0c0b25131b8dea59'
QGL_MOBILE_TENANT_CODE = 'C10026'  # 默认租户
QGL_MOBILE_APPID = 'c6qgh2'  # 产品标识

# 青橄榄管理端配置
QGL_ADMIN_APP_KEY = 'APPKEY_TBD'  # 需联系青橄榄获取
QGL_ADMIN_APP_SECRET = 'APPSECRET_TBD'

# API地址
QGL_ENV = 'prod'  # 'dev' or 'prod'
QGL_MOBILE_API_BASE = {
    'dev': 'https://dev-lshospital.goliveplus.cn',
    'prod': 'https://dev-lshospital.goliveplus.cn'  # 待确认正式环境地址
}
QGL_ADMIN_API_BASE = {
    'dev': 'https://dev-logisticsplatform.goliveplus.cn',
    'prod': 'https://zhhq.huanghuai.edu.cn'
}
```

---

## 6. 错误处理

### 6.1 青橄榄API错误码

| 错误码 | 说明 | 处理策略 |
|-------|-----|---------|
| 500 | 参数错误 | 返回400，提示"登录参数错误" |
| 88890006 | TOKEN已使用或已过期 | 返回401，提示"登录凭证已过期，请重新登录" |
| 88890007 | 用户信息获取失败 | 返回401，提示"用户信息获取失败，请重新登录" |
| 网络超时 | 青橄榄接口不可用 | 返回503，提示"登录服务暂时不可用" |

### 6.2 降级方案

**场景1：青橄榄接口完全不可用**
- 返回503错误，前端显示"登录服务暂时不可用，请稍后重试"
- 已登录用户不受影响（使用本地JWT）

**场景2：用户映射表无记录，青橄榄接口超时**
- 返回503错误，记录日志
- 提示"首次登录失败，请稍后重试"

**场景3：用户映射表有记录，青橄榄接口超时**
- 可选：使用映射表缓存的用户信息创建临时session（仅查询权限）
- 写操作（提交申请）需要实时验证，拒绝请求

---

## 7. 安全考虑

### 7.1 签名校验

- 所有青橄榄API请求必须携带签名
- 签名算法：SHA1/MD5（appSecret + timestamp + randStr排序后拼接）
- timestamp误差不超过2分钟

### 7.2 Token安全

- 青橄榄token仅用于一次性交换，不存储
- 本地JWT使用独立secret，有效期1小时（可配置）
- 刷新token机制（可选）

### 7.3 敏感信息保护

- appKey/appSecret存储在环境变量或加密配置
- 用户映射表不存储密码
- API响应不返回青橄榄原始token

---

## 8. 测试策略

### 8.1 单元测试

- `test_auth.py`：签名生成、验证逻辑
- `test_client.py`：API客户端，使用mock模拟青橄榄接口
- `test_models.py`：用户映射表CRUD

### 8.2 集成测试

- 移动端登录流程：mock青橄榄token → 验证本地JWT生成
- 管理端登录流程：mock一站式平台token → 验证管理员创建
- 错误处理：模拟青橄榄接口错误码

### 8.3 端到端测试

- 使用青橄榄测试环境appKey/appSecret
- 测试完整登录流程（需要青橄榄测试账号）

---

## 9. 实施计划

### Phase 1: 基础架构（1-2天）
- [ ] 创建Django应用：`backend/apps/sso_qingganlian/`
- [ ] 定义models.py：SSOUserMapping模型
- [ ] 实现auth.py：签名生成工具
- [ ] 实现client.py：青橄榄API客户端（移动端接口）

### Phase 2: 移动端登录（1-2天）
- [ ] 实现views.py：移动端登录端点
- [ ] 用户映射逻辑：user_code → 本地User
- [ ] 单元测试 + 集成测试
- [ ] 前端集成（demo-web或移动端）

### Phase 3: 管理端登录（1-2天）
- [ ] 扩展client.py：管理端verify-user接口
- [ ] 实现views.py：管理端登录端点
- [ ] 用户映射逻辑：username → 本地User（管理员）
- [ ] 单元测试 + 集成测试

### Phase 4: 优化与部署（1天）
- [ ] 错误处理完善
- [ ] 日志记录
- [ ] 性能优化（缓存策略）
- [ ] 文档更新
- [ ] 部署到测试环境

---

## 10. 附录

### 10.1 青橄榄API文档参考

- **移动端用户信息获取接口**：`docs/移动端 - 用户信息获取接口文档.docx`
- **后台管理端单点登录对接接口**：`docs/后台管理端-单点登录对接接口文档.docx`

### 10.2 讨论记录

- **三方讨论ID**：DISCUSS-青橄榄平台SSO对接模块设计-用户需求-分析两份对接文档-1780906038
- **讨论结果**：Gemini达成共识（3轮），Codex未参与（json_parse_failed）
- **关键决策**：
  - ✅ 独立Django应用
  - ✅ 用户映射表
  - ✅ Token交换模式（非middleware拦截）
  - ✅ 统一JWT会话管理

### 10.3 待确认事项

- [ ] 青橄榄管理端appKey/appSecret（需联系平台部获取）
- [ ] 青橄榄正式环境API地址（移动端接口文档中测试服和正式服地址相同）
- [ ] 本地User模型是否需要扩展字段（手机号、身份ID等）
- [ ] 是否需要实现token刷新机制
- [ ] 降级策略的具体实施细节

---

**文档版本：** v1.0  
**最后更新：** 2026-06-08  
**审核状态：** Gemini审核通过（3轮共识）
