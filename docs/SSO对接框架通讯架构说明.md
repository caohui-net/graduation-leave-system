# SSO对接框架与本系统通讯架构说明

**文档版本：** v1.0  
**创建日期：** 2026-06-08  
**适用范围：** 毕业离校系统 + 青橄榄平台SSO集成

---

## 1. 架构定位

### 1.1 SSO模块性质

**模块定义：** Django独立应用（App）

```
位置：backend/apps/sso_qingganlian/
性质：功能独立、松耦合
集成方式：INSTALLED_APPS注册
```

**设计原则：**
- 单一职责：只负责SSO登录认证
- 松耦合：通过标准Django User模型与系统集成
- 可插拔：可独立启用/禁用，不影响系统其他功能

### 1.2 在系统中的角色

```
┌─────────────────────────────────────────┐
│         毕业离校系统                      │
│  ┌────────────┐  ┌──────────────────┐   │
│  │ 传统登录   │  │  SSO登录模块     │   │
│  │ (用户名密码)│  │ (青橄榄平台)      │   │
│  └────────────┘  └──────────────────┘   │
│         │               │                │
│         └───────┬───────┘                │
│                 ↓                        │
│         Django User 系统                 │
│                 ↓                        │
│    ┌───────────────────────────┐        │
│    │  业务模块（申请、审批等）   │        │
│    └───────────────────────────┘        │
└─────────────────────────────────────────┘
```

**作用：** 提供青橄榄平台单点登录入口，用户通过青橄榄统一认证后无缝访问系统。

---

## 2. 通讯路径全景

### 2.1 外部通讯（青橄榄 ↔ 本系统）

```
┌──────────────┐
│ 青橄榄平台    │ 用户登录、点击应用
└──────┬───────┘
       │ ① 跳转URL + token参数
       ↓
┌──────────────┐
│ 前端应用      │ 浏览器/小程序
│ (用户侧)      │
└──────┬───────┘
       │ ② HTTP POST /api/sso/qingganlian/mobile/login
       ↓
┌──────────────────────────────────────┐
│ SSO模块 (backend/apps/sso_qingganlian)│
│  - 接收token                          │
│  - 生成签名                           │
└──────┬───────────────────────────────┘
       │ ③ HTTP POST (带签名)
       ↓
┌──────────────┐
│ 青橄榄API     │ 验证token、返回用户信息
└──────┬───────┘
       │ ④ 用户信息JSON
       ↓
┌──────────────────────────────────────┐
│ SSO模块                               │
│  - 创建/更新User                      │
│  - 生成JWT                            │
└──────┬───────────────────────────────┘
       │ ⑤ JWT token
       ↓
┌──────────────┐
│ 前端应用      │ 存储token，后续请求携带
└──────────────┘
```

### 2.2 内部通讯（SSO模块 ↔ 本系统数据库）

```
┌────────────────┐
│ SSO模块        │
└────┬───────────┘
     │ Django ORM (SQL over PostgreSQL wire protocol)
     ↓
┌─────────────────────────────────────┐
│ PostgreSQL 数据库                    │
│                                     │
│  ┌──────────────┐  ┌──────────────┐│
│  │ auth_user    │←─│SSOUserMapping││
│  │ (Django内置) │  │ (SSO模块)    ││
│  └──────┬───────┘  └──────────────┘│
│         │ 外键关联                  │
│         ↓                           │
│  ┌──────────────────────┐          │
│  │ applications         │          │
│  │ (业务模块：申请表)    │          │
│  └──────────────────────┘          │
└─────────────────────────────────────┘
```

**关键关系：**
- `SSOUserMapping.user` → `auth_user.id` (ForeignKey)
- `applications.student` → `auth_user.id` (ForeignKey)
- 通过User模型实现SSO与业务模块的解耦

---

## 3. 详细数据流（登录流程）

### 3.1 Step 1: 前端发起登录请求

**接口：** `POST /api/sso/qingganlian/mobile/login`

**请求示例：**
```http
POST /api/sso/qingganlian/mobile/login HTTP/1.1
Content-Type: application/json

{
  "tenant_code": "S10405",
  "appid": "c6qgh2",
  "saas_wap_token": "eyJ0eXAiOiJKV1Qi..."
}
```

**通讯协议：** HTTP/JSON  
**实现位置：** `views.py::mobile_login()`

### 3.2 Step 2: SSO模块调用青橄榄API（获取user_code）

**目标API：** `https://lshospital.goliveplus.cn/open-api/user-center/user-code-by-token`

**请求构造：**
```python
# 生成签名（auth.py）
timestamp = int(time.time())
rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
sign = generate_signature(app_secret, timestamp, rand_str, 'sha1')

# 发送请求（client.py）
response = self.session.post(
    url,
    headers={
        'appKey': 'abc0a32aa8dd94d1f765841abaafd8ba',
        'timestamp': '1717840511',
        'randStr': 'Gc6LGToDKy2AMhXE',
        'sign': 'baeaa6693fb7b9914c9ff9e388654878b8754515',
        'encryptionType': 'sha1'
    },
    data={
        'tenant_code': 'S10405',
        'appid': 'c6qgh2',
        'saas_wap_token': 'eyJ0eXAiOiJKV1Qi...'
    },
    timeout=30
)
```

**通讯协议：** HTTP/Form-Data  
**实现位置：** `client.py::get_user_code_by_token()`

**返回示例：**
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "tenant_code": "S10405",
    "user_code": "oVSaOuOgcbNpbFN-VDdqy0qqo_vc",
    "user_type": "weChat",
    "user_id": 47485
  }
}
```

### 3.3 Step 3: SSO模块调用青橄榄API（获取用户详情）

**目标API：** `https://lshospital.goliveplus.cn/open-api/user-center/user-info`

**请求参数：**
```python
data = {
    'tenant_code': 'S10405',
    'user_code': 'oVSaOuOgcbNpbFN-VDdqy0qqo_vc',
    'user_type': 'weChat'
}
```

**返回示例：**
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "number": "2024220220323",
    "real_name": "张三",
    "phone": "13800138000",
    "identity_name": "学生",
    "role_name": "本科生"
  }
}
```

**实现位置：** `client.py::get_user_info()`

### 3.4 Step 4: SSO模块创建/更新本地User

**数据库操作（ORM）：**
```python
# views.py::mobile_login()

# 1. 创建或获取Django User
user, created = User.objects.get_or_create(
    username='2024220220323',
    defaults={
        'first_name': '张三',
        'is_active': True
    }
)

# SQL等效（由Django ORM生成）：
# INSERT INTO auth_user (username, first_name, is_active)
# VALUES ('2024220220323', '张三', true)
# ON CONFLICT (username) DO NOTHING;
```

**通讯协议：** SQL over PostgreSQL wire protocol  
**驱动：** psycopg2  
**连接池：** Django自动管理

### 3.5 Step 5: SSO模块创建/更新用户映射

**数据库操作（ORM）：**
```python
# views.py::mobile_login()

mapping, _ = SSOUserMapping.objects.update_or_create(
    user_code='oVSaOuOgcbNpbFN-VDdqy0qqo_vc',
    defaults={
        'user': user,
        'tenant_code': 'S10405',
        'user_type': 'weChat',
        'real_name': '张三',
        'phone': '13800138000',
        'identity_name': '学生',
        'role_name': '本科生',
        'last_login_at': timezone.now()
    }
)

# SQL等效：
# INSERT INTO sso_qingganlian_ssousermapping (...)
# VALUES (...)
# ON CONFLICT (user_code) DO UPDATE SET ...;
```

**外键关联：**
- `mapping.user` → `user.id` (User对象引用)

### 3.6 Step 6: SSO模块生成JWT Token

**Token生成（内存操作）：**
```python
# views.py::mobile_login()

from rest_framework_simplejwt.tokens import RefreshToken

refresh = RefreshToken.for_user(user)
access_token = str(refresh.access_token)

# Token结构（JWT标准）
# Header.Payload.Signature
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
# eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiMjAyNDIyMDIyMDMyMyJ9.
# 5kTz9jYp8mHqF_signature_here
```

**实现库：** djangorestframework-simplejwt  
**算法：** HS256（HMAC-SHA256）  
**有效期：** 默认1小时（可配置）

### 3.7 Step 7: 返回给前端

**响应示例：**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 123,
    "username": "2024220220323",
    "real_name": "张三",
    "role": "student",
    "phone": "13800138000"
  }
}
```

**前端处理：**
1. 存储token到localStorage/AsyncStorage
2. 后续API请求携带：`Authorization: Bearer <token>`

---

## 4. 通讯技术实现

### 4.1 HTTP通讯层（外部）

**实现类：** `QingganlanClient` (client.py)

**核心代码：**
```python
class QingganlanClient:
    def __init__(self, app_key, app_secret, env='prod', api_type='mobile'):
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = self.MOBILE_API_BASE[env]
        self.session = requests.Session()  # ← HTTP连接池
    
    def _make_request(self, method, endpoint, data=None, encryption_type='sha1'):
        # 1. 生成签名参数
        timestamp = int(time.time())
        rand_str = self._generate_rand_str()
        sign = generate_signature(self.app_secret, timestamp, rand_str, encryption_type)
        
        # 2. 构造请求
        headers = {
            'appKey': self.app_key,
            'timestamp': str(timestamp),
            'randStr': rand_str,
            'sign': sign,
            'encryptionType': encryption_type
        }
        
        # 3. 发送请求（复用连接）
        response = self.session.post(url, headers=headers, data=data, timeout=30)
        
        # 4. 验证业务错误码
        result = response.json()
        if result.get('code') != 200:
            raise SSOAPIError(result['code'], result.get('msg'))
        
        return result
```

**技术特点：**
- **连接池复用：** `requests.Session()` 自动管理HTTP连接，避免每次请求都创建新连接
- **超时控制：** 30秒超时，防止长时间阻塞
- **签名机制：** SHA1/MD5签名，防止请求篡改
- **错误处理：** 区分HTTP错误和业务错误码

### 4.2 数据库通讯层（内部）

**实现方式：** Django ORM

**连接配置（settings/base.py）：**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='graduation_leave'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='postgres'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 600,  # 连接池：保持连接10分钟
    }
}
```

**通讯协议栈：**
```
Django ORM (Python对象)
    ↓
psycopg2 (数据库驱动)
    ↓
PostgreSQL wire protocol (二进制协议)
    ↓
TCP/IP Socket (网络传输)
    ↓
PostgreSQL Server
```

**示例查询：**
```python
# Python代码（ORM）
user = User.objects.filter(username='2024220220323').first()
mapping = user.ssousermapping_set.first()

# 实际执行的SQL（psycopg2生成）
# SELECT * FROM auth_user WHERE username = '2024220220323' LIMIT 1;
# SELECT * FROM sso_qingganlian_ssousermapping WHERE user_id = 123 LIMIT 1;
```

### 4.3 模块间调用（Python层）

**方式1：通过User外键关联**

```python
# 业务模块（applications/models.py）
from django.contrib.auth.models import User

class Application(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    counselor = models.ForeignKey(User, related_name='counselor_applications', ...)
    # ...

# 业务逻辑中获取SSO信息
application = Application.objects.get(id=1)

# 通过User反向查询SSO映射（无需显式导入SSO模块）
sso_mapping = application.student.ssousermapping_set.first()
if sso_mapping:
    real_name = sso_mapping.real_name
    phone = sso_mapping.phone
```

**方式2：直接导入SSO模块**

```python
# 其他模块需要直接访问SSO数据
from apps.sso_qingganlian.models import SSOUserMapping

# 根据青橄榄user_code查询
mapping = SSOUserMapping.objects.filter(
    user_code='oVSaOuOgcbNpbFN-VDdqy0qqo_vc'
).select_related('user').first()

if mapping:
    user = mapping.user
    real_name = mapping.real_name
```

**通讯方式：** Python直接导入（同进程内存访问）  
**耦合度：** 松耦合（通过标准User模型解耦）

---

## 5. 通讯协议总结表

| 通讯类型 | 起点 | 终点 | 协议 | 实现 | 数据格式 | 超时 |
|---------|------|------|------|------|---------|------|
| 前端登录请求 | 浏览器/小程序 | SSO模块API | HTTP/HTTPS | Django REST Framework | JSON | 默认无限制 |
| SSO→青橄榄验证 | SSO模块 | 青橄榄API | HTTP/HTTPS | requests.Session | Form-Data | 30秒 |
| SSO→User表 | SSO模块 | PostgreSQL | SQL | Django ORM + psycopg2 | 二进制 | 默认无限制 |
| SSO→Mapping表 | SSO模块 | PostgreSQL | SQL | Django ORM + psycopg2 | 二进制 | 默认无限制 |
| 业务模块→User | 业务模块 | PostgreSQL | SQL | Django ORM + psycopg2 | 二进制 | 默认无限制 |
| SSO→JWT生成 | SSO模块 | 内存 | 函数调用 | simplejwt库 | Python对象 | 无 |
| 返回前端 | SSO模块API | 浏览器/小程序 | HTTP/HTTPS | Django REST Framework | JSON | 默认无限制 |

---

## 6. 关键通讯组件职责

### 6.1 client.py - 外部通讯核心

**职责：**
- 封装与青橄榄平台的HTTP通讯
- 自动生成签名参数
- 管理HTTP连接池
- 验证API响应

**关键方法：**
- `get_user_code_by_token()` - 移动端：token换user_code
- `get_user_info()` - 移动端：获取用户详情
- `verify_admin_user()` - 管理端：验证authorization

### 6.2 views.py - 内外通讯桥梁

**职责：**
- 接收前端HTTP请求（入口）
- 调用client.py与青橄榄通讯（外部）
- 调用ORM与数据库通讯（内部）
- 调用simplejwt生成JWT（内部）
- 返回JSON响应给前端（出口）

**关键方法：**
- `mobile_login()` - 移动端登录处理
- `admin_login()` - 管理端登录处理

### 6.3 models.py - 数据通讯基础

**职责：**
- 定义数据表结构（ORM模型）
- 提供User外键关联（与系统集成）
- 实现数据持久化（ORM自动生成SQL）

**关键模型：**
- `SSOUserMapping` - 青橄榄用户与本地User的映射表

### 6.4 auth.py - 签名工具

**职责：**
- 生成SHA1/MD5签名
- 保证API请求安全性

**关键函数：**
- `generate_signature()` - 签名生成算法

---

## 7. 通讯性能优化

### 7.1 HTTP连接池（requests.Session）

**优化点：**
- 复用TCP连接，避免每次请求都进行三次握手
- 减少TLS/SSL握手开销

**实现：**
```python
# client.py
self.session = requests.Session()  # 创建一次
response = self.session.post(...)  # 复用连接
```

**性能提升：**
- 单次请求延迟降低约50-200ms（取决于网络）

### 7.2 数据库连接池（Django CONN_MAX_AGE）

**配置：**
```python
DATABASES = {
    'default': {
        # ...
        'CONN_MAX_AGE': 600,  # 连接保持10分钟
    }
}
```

**优化效果：**
- 避免每次请求都创建新数据库连接
- 减少数据库连接建立开销

### 7.3 ORM查询优化

**优化技巧：**
```python
# ❌ 错误：N+1查询问题
users = User.objects.all()
for user in users:
    mapping = user.ssousermapping_set.first()  # 每次查询一次数据库

# ✅ 正确：使用select_related()
users = User.objects.select_related('ssousermapping').all()
for user in users:
    mapping = user.ssousermapping  # 一次查询获取所有数据
```

---

## 8. 通讯安全机制

### 8.1 HTTP通讯安全

**措施：**
1. **HTTPS加密**：所有与青橄榄通讯使用HTTPS
2. **签名验证**：防止请求被篡改
3. **时间戳校验**：防止重放攻击（青橄榄方验证时间戳误差<2分钟）
4. **随机字符串**：增加签名复杂度

### 8.2 数据库通讯安全

**措施：**
1. **参数化查询**：ORM自动防止SQL注入
2. **连接加密**：PostgreSQL支持SSL连接（可选）
3. **权限控制**：数据库用户权限最小化

### 8.3 Token安全

**措施：**
1. **JWT签名**：防止token伪造
2. **有效期限制**：默认1小时过期
3. **HTTPS传输**：防止token被窃听

---

## 9. 通讯监控与日志

### 9.1 日志记录位置

**SSO模块日志（views.py）：**
```python
import logging
logger = logging.getLogger(__name__)

# 登录尝试
logger.info(f"Mobile login attempt: tenant={tenant_code}, appid={appid}")

# 登录成功
logger.info(f"Mobile login success: user={user.username}, role={role}")

# 登录失败
logger.warning(f"Mobile login failed: token expired")
logger.error(f"Mobile login failed: SSO API error {e.code}")
```

### 9.2 日志级别

| 级别 | 场景 | 示例 |
|------|------|------|
| INFO | 正常流程 | 登录尝试、登录成功 |
| WARNING | 预期内的失败 | token过期、用户信息获取失败 |
| ERROR | API错误 | 青橄榄API返回错误码 |
| EXCEPTION | 未预期错误 | 系统异常、数据库错误 |

### 9.3 监控指标建议

**外部通讯监控：**
- 青橄榄API响应时间
- 青橄榄API错误率
- token验证失败率

**内部通讯监控：**
- 数据库查询响应时间
- User创建/更新频率
- JWT生成耗时

---

## 10. 常见问题与排查

### 10.1 外部通讯失败

**症状：** 青橄榄API返回错误或超时

**排查步骤：**
1. 检查网络连通性：`curl https://lshospital.goliveplus.cn`
2. 检查签名生成是否正确（日志中查看sign值）
3. 检查appKey/appSecret配置是否正确
4. 检查时间戳是否准确（服务器时间与标准时间误差<2分钟）

### 10.2 数据库通讯失败

**症状：** ORM操作报错或超时

**排查步骤：**
1. 检查PostgreSQL服务状态：`systemctl status postgresql`
2. 检查数据库连接配置：`.env`文件中的DB_HOST/DB_PORT
3. 检查数据库用户权限：`psql -U postgres -d graduation_leave`
4. 检查表是否存在：`python manage.py showmigrations`

### 10.3 User创建失败

**症状：** IntegrityError或unique约束冲突

**排查步骤：**
1. 检查username是否已存在
2. 检查SSOUserMapping的user_code/username是否为空字符串（应为None）
3. 查看详细错误日志

---

## 11. 总结

### 11.1 通讯架构优势

1. **解耦性好**：SSO模块通过标准User模型与系统集成，可独立部署/升级
2. **性能优化**：HTTP连接池 + 数据库连接池，降低通讯开销
3. **安全可靠**：签名验证 + HTTPS + JWT，多层安全保障
4. **易于监控**：完善的日志记录，便于问题定位

### 11.2 技术栈清单

**外部通讯：**
- HTTP客户端：requests 2.31.0
- 签名算法：hashlib (Python标准库)

**内部通讯：**
- ORM框架：Django 4.2
- 数据库驱动：psycopg2
- 认证库：djangorestframework-simplejwt

**协议支持：**
- HTTP/HTTPS（RESTful API）
- PostgreSQL wire protocol
- JWT (JSON Web Token)

---

**文档结束**

**相关文档：**
- [青橄榄SSO对接技术方案](青橄榄SSO对接技术方案.md)
- [系统设计文档](design/2026-05-27-system-design.md)
- [SSO模块README](../backend/apps/sso_qingganlian/README.md)
