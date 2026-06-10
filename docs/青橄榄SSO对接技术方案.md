# 青橄榄平台SSO对接技术方案

**文档版本：** v1.0  
**创建日期：** 2026-06-08  
**提交方：** 毕业离校系统技术团队  
**审核方：** 青橄榄平台技术团队

---

## 1. 项目概述

### 1.1 对接目标

将毕业离校系统集成到青橄榄一站式管理服务平台，实现单点登录（SSO）功能，让用户通过青橄榄平台统一登录后无缝访问毕业离校系统。

### 1.2 系统角色定位

- **青橄榄平台**：SSO身份提供方，用户统一登录入口
- **毕业离校系统**：第三方应用，SSO服务消费方
- **对接模式**：用户从青橄榄平台跳转到毕业离校系统，携带认证token

### 1.3 技术栈

- **后端框架**：Django 4.2.13 + Django REST Framework 3.15.2
- **认证机制**：JWT (djangorestframework-simplejwt 5.3.1)
- **HTTP客户端**：requests 2.31.0
- **配置管理**：python-decouple 3.8
- **数据库**：PostgreSQL（用户映射表）

---

## 2. 对接架构

### 2.1 总体流程

```
用户 → 青橄榄平台登录
     ↓
  点击"毕业离校系统"应用
     ↓
  青橄榄平台生成token并跳转
     ↓
  毕业离校系统接收token
     ↓
  调用青橄榄API验证token
     ↓
  获取用户信息并创建本地映射
     ↓
  生成系统JWT token
     ↓
  用户自动登录成功
```

### 2.2 模块设计

**独立SSO模块** (`backend/apps/sso_qingganlian/`)

```
sso_qingganlian/
├── models.py          # 用户映射模型
├── auth.py            # 签名生成工具
├── client.py          # 青橄榄API客户端
├── exceptions.py      # 异常定义
├── serializers.py     # 请求/响应序列化
├── views.py           # 登录API视图
├── urls.py            # 路由配置
├── settings.py        # 配置管理
└── README.md          # 模块文档
```

---

## 3. 已实现功能

### 3.1 移动端登录对接

**API端点：** `POST /api/sso/qingganlian/mobile/login`

**请求参数：**
```json
{
  "tenant_code": "S10405",
  "appid": "c6qgh2",
  "saas_wap_token": "用户token"
}
```

**对接青橄榄接口：**
1. `/open-api/user-center/user-code-by-token` - 获取user_code
2. `/open-api/user-center/user-info` - 获取用户详细信息

**响应示例：**
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

### 3.2 管理端登录对接

**API端点：** `POST /api/sso/qingganlian/admin/login`

**请求参数：**
```json
{
  "authorization": "bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**对接青橄榄接口：**
- `/api/open-api/auth/verify-user` - 验证管理端token并获取用户信息

**响应格式：** 同移动端

---

## 4. 安全机制实现

### 4.1 签名验证

**实现方式：** 完全遵循青橄榄平台签名规范

```python
def generate_signature(app_secret, timestamp, rand_str, encryption_type='sha1'):
    """
    1. 将 app_secret、timestamp、rand_str 排序
    2. 拼接为字符串
    3. SHA1/MD5加密生成签名
    """
    params = sorted([app_secret, str(timestamp), rand_str])
    concat_str = ''.join(params)
    if encryption_type.lower() == 'md5':
        return hashlib.md5(concat_str.encode()).hexdigest()
    else:
        return hashlib.sha1(concat_str.encode()).hexdigest()
```

### 4.2 请求Header配置

所有API请求自动添加以下Header：
- `appKey`：应用标识
- `timestamp`：Unix时间戳
- `randStr`：16位随机字符串
- `sign`：认证签名
- `encryptionType`：加密类型（sha1/md5）

### 4.3 错误码处理

**已实现业务错误码识别：**
- `88890006`：TOKEN已使用或已过期 → 返回401提示重新登录
- `88890007`：用户信息获取失败 → 返回401
- 其他错误 → 返回400并附带详细错误信息

---

## 5. 用户映射机制

### 5.1 映射表结构

**模型：** `SSOUserMapping`

| 字段 | 类型 | 说明 | 约束 |
|------|------|------|------|
| user | ForeignKey | 关联本地User模型 | NOT NULL |
| user_code | CharField(100) | 青橄榄用户code | UNIQUE, NULL允许 |
| username | CharField(150) | 青橄榄用户名 | UNIQUE, NULL允许 |
| tenant_code | CharField(50) | 租户号 | NOT NULL |
| user_type | CharField(20) | 用户类型（weChat/native等） | NOT NULL |
| real_name | CharField(100) | 真实姓名 | NOT NULL |
| phone | CharField(20) | 手机号 | 可选 |
| identity_name | CharField(50) | 身份名称 | NOT NULL |
| role_name | CharField(50) | 角色名称 | 可选 |
| last_login_at | DateTimeField | 最后登录时间 | NOT NULL |

**注：** 表支持空字符串自动转为NULL，避免unique约束冲突。

### 5.2 映射逻辑

```python
# 首次登录：创建本地User + SSOUserMapping
user, created = User.objects.get_or_create(
    username=number,
    defaults={'first_name': real_name, 'is_active': True}
)

# 更新映射关系
SSOUserMapping.objects.update_or_create(
    user_code=user_code,
    defaults={
        'user': user,
        'tenant_code': tenant_code,
        'user_type': user_type,
        'real_name': real_name,
        'last_login_at': timezone.now()
    }
)
```

---

## 6. 配置管理

### 6.1 环境变量配置

**移动端配置：**
```bash
QGL_MOBILE_APP_KEY=abc0a32aa8dd94d1f765841abaafd8ba
QGL_MOBILE_APP_SECRET=b1d2efa9587446d80ce6388e0c0b25131b8dea59
QGL_MOBILE_TENANT_CODE=S10405
QGL_MOBILE_APPID=c6qgh2
```

**管理端配置：**
```bash
QGL_ADMIN_APP_KEY=待青橄榄提供
QGL_ADMIN_APP_SECRET=待青橄榄提供
```

**环境设置：**
```bash
QGL_ENV=prod  # dev或prod，切换测试/正式服务器
```

### 6.2 API地址配置

**移动端API：**
- 测试环境：`https://dev-lshospital.goliveplus.cn`
- 生产环境：`https://lshospital.goliveplus.cn`（待确认）

**管理端API：**
- 测试环境：`https://dev-logisticsplatform.goliveplus.cn`
- 生产环境：`https://zhhq.huanghuai.edu.cn`

---

## 7. 性能与监控

### 7.1 性能优化

**HTTP连接池：**
```python
class QingganlanClient:
    def __init__(self, ...):
        self.session = requests.Session()  # 复用连接，提升性能
```

**超时控制：** 所有API请求设置30秒超时

### 7.2 日志记录

**已实现完整日志链路：**

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
logger.exception(f"Mobile login failed: unexpected error")
```

**日志级别：**
- INFO：正常登录尝试和成功
- WARNING：预期内的失败（token过期、用户信息获取失败）
- ERROR：SSO API错误
- EXCEPTION：未预期的系统错误

---

## 8. 部署要求

### 8.1 依赖安装

```bash
pip install python-decouple==3.8
pip install djangorestframework-simplejwt==5.3.1
pip install requests==2.31.0
```

### 8.2 数据库迁移

```bash
cd backend
python manage.py makemigrations sso_qingganlian
python manage.py migrate
```

### 8.3 Django配置

**INSTALLED_APPS：**
```python
INSTALLED_APPS = [
    # ...
    'apps.sso_qingganlian',
]
```

**URL路由：**
```python
urlpatterns = [
    path('api/sso/qingganlian/', include('apps.sso_qingganlian.urls')),
]
```

---

## 9. 测试计划

### 9.1 单元测试（待实施）

- [x] 签名生成算法测试
- [ ] API客户端mock测试
- [ ] 用户映射逻辑测试
- [ ] 异常处理测试

### 9.2 集成测试（待实施）

**测试环境联调：**
1. 配置测试环境appKey/appSecret
2. 从青橄榄测试环境跳转携带token
3. 验证移动端登录流程完整性
4. 验证管理端登录流程完整性
5. 测试错误场景：
   - token过期
   - 无效token
   - 网络超时
   - 用户信息获取失败

**测试数据记录：**
- 请求/响应日志
- 用户映射创建记录
- 错误场景处理结果

### 9.3 生产环境验证（待实施）

1. 配置生产环境appKey/appSecret
2. 小范围用户测试
3. 监控日志和性能指标
4. 完整功能验证

---

## 10. 需要青橄榄方配合事项

### 10.1 应用注册信息确认

**已提供信息：**
- 应用名称：毕业离校系统
- 移动端AppId：c6qgh2
- 移动端AppKey：abc0a32aa8dd94d1f765841abaafd8ba
- 移动端AppSecret：b1d2efa9587446d80ce6388e0c0b25131b8dea59
- 租户号：S10405

**待确认信息：**
- [ ] 管理端AppKey和AppSecret
- [ ] 生产环境API地址（移动端）
- [ ] 应用跳转URL配置（青橄榄平台需配置我们的系统URL）
- [ ] 应用图标和应用描述（在青橄榄平台展示）

### 10.2 测试环境准备

**请求青橄榄方提供：**
1. 测试环境应用配置完成确认
2. 测试账号（用于模拟跳转和登录流程）
3. 测试环境跳转URL示例（包含token参数的完整URL）

### 10.3 接口文档确认

**需要确认的技术细节：**
1. 移动端生产环境API地址是否为 `https://lshospital.goliveplus.cn`？
2. 管理端接口返回的用户字段是否完整？（当前文档未明确role字段获取方式）
3. token有效期是多久？（用于前端刷新逻辑）
4. 并发调用限制？（QPS限制、频率限制）

### 10.4 上线流程

**请求提供上线操作指南：**
1. 生产环境应用提交审核流程
2. 应用上线checklist
3. 应用下线/紧急回滚机制
4. 技术支持联系方式

---

## 11. 当前状态与时间表

### 11.1 当前状态

| 项目 | 状态 | 说明 |
|------|------|------|
| 代码开发 | ✅ 完成 | Phase 1-4全部完成 |
| 单元测试 | ⏳ 待实施 | 需要mock青橄榄API |
| 测试环境联调 | ⏳ 待实施 | 等待青橄榄方配置测试环境 |
| 生产环境验证 | ⏳ 待实施 | 依赖测试环境验证通过 |

### 11.2 时间表（预估）

| 阶段 | 预计时间 | 依赖 |
|------|----------|------|
| 青橄榄方审核技术方案 | 3工作日 | 本文档提交 |
| 测试环境准备 | 2工作日 | 青橄榄方配置 |
| 集成测试 | 3工作日 | 测试环境就绪 |
| 问题修复 | 2工作日 | 测试结果 |
| 生产环境验证 | 1工作日 | 测试通过 |
| 正式上线 | 1工作日 | 验证通过 |

**预计总工期：** 12工作日（约2.5周）

---

## 12. 附录

### 12.1 技术联系人

**毕业离校系统技术团队：**
- 技术负责人：[待填写]
- 联系邮箱：[待填写]
- 联系电话：[待填写]

### 12.2 参考文档

1. `backend/apps/sso_qingganlian/README.md` - 模块使用文档
2. `docs/design/2026-06-08-sso-qingganlian-integration.md` - 详细技术设计文档
3. 青橄榄提供的接口文档：
   - `docs/移动端 - 用户信息获取接口文档.docx`
   - `docs/后台管理端-单点登录对接接口文档.docx`

### 12.3 代码仓库

- Git仓库：[待填写]
- 分支：`main`
- SSO模块代码：`backend/apps/sso_qingganlian/`

---

**文档结束**

**审核要点：**
1. 技术方案是否符合青橄榄平台规范？
2. 安全机制实现是否正确？
3. 接口对接逻辑是否完整？
4. 还有哪些遗漏或需要调整的地方？
5. 测试环境何时可以准备就绪？

**请青橄榄技术团队审核并反馈。**
