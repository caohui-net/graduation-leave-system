# 青橄榄SSO对接技术审查 - Codex

**保存名：** sso-review-codex  
**审查日期：** 2026-06-10  
**审查范围：** `backend/apps/sso_qingganlian/views.py`、SSO映射模型、JWT配置、Docker部署配置、相关测试与文档契约  
**审查结论：** 需要修改。不建议按当前实现直接作为生产形态验收；可以继续联调，但应先修正字段契约、JWT配置与部署安全项。

## 主要发现

### P0-1 管理端字段映射契约不一致

**位置：**
- `backend/apps/sso_qingganlian/views.py:190-215`
- `backend/apps/sso_qingganlian/providers/qingganlian.py:94-103`
- `backend/apps/sso_qingganlian/tests/test_providers.py:51-67`
- `backend/apps/sso_qingganlian/models.py:29-41`

**问题：** 当前 `admin_login` 只读取 `admin_data.get('user_code')`，并通过 `SSOUserMapping.objects.update_or_create(user_code=user_code, ...)` 建立映射。但已有 Provider 实现和测试 fixture 使用的是管理端 `username` 字段，模型里也保留了 `username` 作为“管理端username”。如果真实青橄榄 `verify-user` 只返回 `username`，当前管理端登录会直接返回“管理员标识缺失”。

**影响：** 这是上线前阻断项。e2e 测试通过不能证明真实管理端字段正确，因为测试 mock 返回的是 `user_code`。

**建议：**
1. 向青橄榄确认 `verify-user` 真实脱敏响应样例：到底返回 `username`、`user_code`，还是两者都返回。
2. 若管理端真实字段是 `username`，则 `admin_login` 应使用 `username` 作为本地 `user_id` 或外部唯一键，并写入 `SSOUserMapping.username`。
3. 若青橄榄已改为 `user_code`，则同步修改 Provider、模型注释、测试 fixture 和设计文档，避免双契约长期存在。
4. 更稳妥的模型方向是使用 `provider + external_uid` 作为统一唯一键，`user_code/username` 仅作为青橄榄原始字段快照。

### P0-2 JWT 1天/7天配置未生效，Refresh 也未返回

**位置：**
- `backend/config/settings/base.py:147-158`
- `.env.docker:19-22`
- `backend/apps/sso_qingganlian/views.py:116-123`
- `backend/apps/sso_qingganlian/views.py:228-235`

**问题：** `.env.docker` 写了 `JWT_ACCESS_TOKEN_LIFETIME=86400` 和 `JWT_REFRESH_TOKEN_LIFETIME=604800`，但 `SIMPLE_JWT` 硬编码为 Access 1小时、Refresh 1天。SSO登录响应只返回 `token`，没有返回 `refresh`，因此“Access 1天 / Refresh 7天”当前并未成立。

**建议：**
1. 若目标确认为 Access 1天 / Refresh 7天，在 `SIMPLE_JWT` 中读取环境变量并使用 `timedelta(seconds=...)`。
2. 响应结构明确是否返回 refresh。若前端需要续期，应返回 `refresh`；若不提供 refresh，就不要宣称 refresh 7天有业务意义。
3. 增加测试：解码 token 的 `exp`，断言 access 生命周期符合配置；如返回 refresh，也断言 refresh 生命周期。

### P0-3 生产环境本地密码登录没有真正禁用

**位置：**
- `backend/apps/users/views.py:34-41`
- `backend/apps/users/views.py:66-72`
- `backend/config/settings/prod.py:23-27`

**问题：** 当前只禁用了 `demo_login`，并在 prod 启动时阻止 `DEMO_AUTH_ENABLED=true`。普通 `/api/auth/login` 仍然允许账号密码登录。用户描述中的“生产环境禁用本地密码登录”目前只对演示登录成立，不对普通密码登录成立。

**建议：**
1. 增加显式开关，例如 `PASSWORD_LOGIN_ENABLED=false`。
2. 在生产环境或开关关闭时让 `/api/auth/login` 返回 403。
3. 保留必要的 break-glass 管理入口时，必须有独立强口令策略、IP限制和审计日志，不能混同普通本地登录。

### P1-1 `@permission_classes([])` 可工作，但建议改为显式 AllowAny 并加登录限流

**位置：**
- `backend/apps/sso_qingganlian/views.py:24-26`
- `backend/apps/sso_qingganlian/views.py:153-155`
- `backend/config/settings/base.py:129-135`

**判断：** SSO登录端点本来就必须匿名访问，因此豁免 JWT 认证方向正确。`@permission_classes([])` 在 DRF 中会覆盖默认权限，实际效果是允许匿名访问；但语义不如 `@permission_classes([AllowAny])` 清晰。

**风险：** 当前没有对 SSO 登录端点使用专门 `@throttle_classes`。虽然全局有 `AnonRateThrottle`，但登录接口通常应更严格，并且应区分移动端/管理端失败频率。

**建议：**
1. 改为 `@permission_classes([AllowAny])`。
2. 为两个 SSO 登录端点增加登录限流，例如复用或扩展 `LoginRateThrottle`。
3. 日志不要记录入站 token；当前没有直接记录 token，这点是正确的。

### P1-2 Docker 配置只适合开发/联调，不是生产部署

**位置：**
- `docker-compose.yml:20-31`
- `.env.docker:9-13`
- `backend/manage.py:9`
- `backend/config/settings/dev.py:4-12`
- `backend/config/settings/prod.py:5-21`

**问题：** compose 使用 `runserver`、源码 volume 热更新、`.env.docker` 中 `DEBUG=True`，且没有设置 `DJANGO_SETTINGS_MODULE=config.settings.prod`。`manage.py` 默认加载 dev settings，dev settings 允许所有 host 和 CORS。`.env.docker` 中 SECRET_KEY 也是 insecure 示例值；如果切到 prod settings 会被 `prod.py` 阻止启动。

**建议：**
1. 保留当前 compose 作为开发/联调配置，但不要把它称为生产部署配置。
2. 新增生产 compose 或部署说明：gunicorn/uwsgi、`DJANGO_SETTINGS_MODULE=config.settings.prod`、非 insecure `SECRET_KEY`、`DEBUG=false`、不挂源码 volume。
3. PostgreSQL 不应在生产公网暴露 `5432`，数据库密码不能是示例值。
4. CORS/ALLOWED_HOSTS 按正式前端域名或 IP 精确配置。

### P1-3 SSO凭证与默认值管理风险

**位置：**
- `backend/apps/sso_qingganlian/settings.py:4-17`
- `backend/config/settings/base.py:170-177`
- `.env.docker:24-29`

**问题：** SSO app key/secret 存在默认值或示例值散落。生产凭证不应出现在仓库文件中，也不应存在可静默使用的默认密钥。

**建议：**
1. 生产环境中 `QGL_ADMIN_APP_KEY`、`QGL_ADMIN_APP_SECRET`、`QGL_MOBILE_APP_KEY`、`QGL_MOBILE_APP_SECRET` 应无默认值必填。
2. 提供 `.env.example` / `.env.docker.example`，真实 `.env.docker` 不纳入版本管理或清理敏感值。
3. 若这些值已经进入 Git 历史，按凭证泄露处理：轮换青橄榄 appsecret。

### P1-4 SSOUserMapping 的唯一键仍偏脆弱

**位置：**
- `backend/apps/sso_qingganlian/models.py:14-41`
- `backend/apps/sso_qingganlian/migrations/0002_add_provider_fields.py:11-19`
- `backend/apps/sso_qingganlian/views.py:101-114`
- `backend/apps/sso_qingganlian/views.py:213-226`

**问题：** 当前模型已有 `provider/external_uid/provider_data`，但 view 没有写入这些字段，迁移回填还把 `external_uid` 设成了 `tenant_code`，这不是用户唯一标识。`user_code` 全局唯一只有在青橄榄明确保证其跨租户、跨端全局唯一时才安全。

**建议：**
1. 明确唯一性边界：推荐 `UniqueConstraint(provider, external_uid)`。
2. 移动端 `external_uid=user_code`；管理端按确认结果使用 `username` 或 `user_code`。
3. `tenant_code`、`user_type`、`role_name` 等放入 `provider_data`，保持原始数据可追溯。
4. 注意当前 `user = OneToOneField` 表示一个本地用户只能绑定一个 SSO 身份；如未来同一人同时有移动端和管理端身份，会产生结构限制。

### P2-1 用户属性更新不完整

**位置：**
- `backend/apps/sso_qingganlian/views.py:80-88`
- `backend/apps/sso_qingganlian/views.py:202-210`

**问题：** `get_or_create` 只在首次创建时写入 `name/role/is_staff/active`。后续青橄榄返回姓名、手机号、身份变化时，本地 `User` 不会更新；而返回给前端的是本次 SSO 数据，数据库里的用户数据可能不一致。

**建议：** 登录成功后同步必要字段，至少同步 `name`、`phone`、`role`、`is_staff`，同时谨慎处理角色降级/升级的审计。

### P2-2 响应 schema 与实际响应不一致

**位置：**
- `backend/apps/sso_qingganlian/serializers.py:11-17`
- `backend/apps/sso_qingganlian/views.py:121-129`
- `backend/apps/sso_qingganlian/views.py:233-241`

**问题：** `UserInfoSerializer.id` 是 `IntegerField`，实际返回 `user.user_id` 字符串。OpenAPI 文档会误导前端和联调方。

**建议：** 将 `id` 改为 `CharField`，或返回真实整数主键；当前 User 模型主键是字符串 `user_id`，建议 schema 跟随字符串。

## 对审查要点的直接回答

1. **user_code字段映射是否正确？**  
   移动端基本正确，但前提是青橄榄保证 `user_code` 是用户外部唯一标识。管理端不建议直接认定正确：当前实现与 Provider、测试、模型注释存在 `user_code` vs `username` 契约冲突，必须拿真实 `verify-user` 脱敏样例确认。

2. **JWT有效期1天/7天是否合理？**  
   业务上可以接受，但安全上偏长；如果前端在内网/校园环境且无 refresh 续期接口，Access 1天是可用性优先的选择。关键问题是当前代码没有生效，实际仍是 Access 1小时 / Refresh 1天，且 refresh 未返回。

3. **permission_classes([])安全性？**  
   匿名访问登录端点是正确的，但写法不清晰。建议改为 `AllowAny`，并加专门登录限流。安全性主要依赖青橄榄 token 校验、限流、日志脱敏和 HTTPS，而不是 DRF JWT 权限。

4. **Docker部署配置是否完善？**  
   开发/联调配置基本够用，生产配置不完善。当前 compose 是 runserver + 源码挂载 + dev settings + DEBUG=True，不应作为生产部署验收。

5. **还有哪些遗漏或风险？**  
   主要遗漏是：真实接口字段契约未固化、JWT配置未生效、本地密码登录未禁用、生产部署形态缺失、凭证管理风险、统一外部身份模型未真正使用、User字段更新与响应schema不一致。

## 建议修复顺序

1. 先确认青橄榄管理端 `verify-user` 脱敏响应样例，并修正 `admin_login` 唯一键。
2. 统一 JWT 生命周期：要么代码实现 1天/7天并返回 refresh，要么修正文档。
3. 增加生产禁用普通本地密码登录的开关和测试。
4. SSO端点改 `AllowAny`，增加限流。
5. 拆分开发 compose 和生产部署配置，清理凭证默认值。
6. 补充测试：移动端成功、管理端 username/user_code 字段变体、空标识符、JWT exp、生产禁用密码登录。

## 验证限制

宿主机 Python 环境缺少 Django，无法复跑 `backend/test_sso_e2e.py`、`manage.py check` 或 migrations 检查；审查结论基于静态代码、配置和现有测试文件读取。尝试执行时失败原因是 `ModuleNotFoundError: No module named 'django'`。
