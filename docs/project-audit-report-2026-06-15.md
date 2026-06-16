# 毕业生离校申请审批系统 - 代码审计报告

**审计日期：** 2026-06-15  
**审计范围：** 后端 Django/DRF 代码、认证授权、附件、审批、配置、通知、测试面

## 一、整体结论

项目功能完整，审批事务和基础权限控制做得不错，但生产安全边界偏弱。当前不建议按生产标准直接上线，至少需要先修复 SSO 认证绕过、密钥硬编码、日志泄漏和部分性能问题。

## 二、架构概览

- 后端：Django 4.2 + DRF
- 数据库：PostgreSQL
- 认证：JWT + 青橄榄 SSO
- 核心模块：`users`、`applications`、`approvals`、`attachments`、`notifications`、`sso_qingganlian`

## 三、主要风险

### 1. SSO 认证可被弱化或绕过
**位置：** [`backend/apps/sso_qingganlian/views.py`](../backend/apps/sso_qingganlian/views.py:143)  
**位置：** [`backend/apps/sso_qingganlian/settings.py`](../backend/apps/sso_qingganlian/settings.py:24)

**问题：**
- `mobile_login` 在 `VERIFY_MOBILE_TOKEN=False` 时直接信任请求里的 `user_id`
- `admin_login` 只验证 token 是否有效，没有校验 token 与 `username` 的绑定关系
- 这会把“持有一个可用 token”与“登录指定账号”混在一起

**影响：**
- 账号冒用
- 管理员身份伪造风险
- 生产环境一旦配置失误，风险很高

**修复建议：**
- 生产环境强制开启移动端和管理端 token 验证
- 登录时必须校验 token 解析出的用户身份与请求账号一致
- 禁止仅靠请求参数决定本地登录身份

### 2. 密钥默认值硬编码
**位置：** [`backend/config/settings/base.py`](../backend/config/settings/base.py:11)  
**位置：** [`backend/apps/sso_qingganlian/settings.py`](../backend/apps/sso_qingganlian/settings.py:6)

**问题：**
- `SECRET_KEY`、`QGL_MOBILE_APP_KEY`、`QGL_MOBILE_APP_SECRET` 等存在默认值
- 环境变量缺失时会直接启用默认值

**影响：**
- JWT 签名密钥不安全
- 外部平台凭据泄漏风险
- 配置错误时可能默默降级为不安全状态

**修复建议：**
- 生产环境强制要求这些变量存在
- 去掉敏感配置默认值
- 启动时做 fail-fast 校验

### 3. SSO 客户端打印敏感信息
**位置：** [`backend/apps/sso_qingganlian/client.py`](../backend/apps/sso_qingganlian/client.py:61)

**问题：**
- 请求头、请求体、响应体直接 `print`
- 可能把 token、签名、用户信息写入日志

**影响：**
- 敏感数据泄漏
- 排障日志变成攻击面

**修复建议：**
- 改为结构化日志
- 脱敏 token、签名和个人信息
- 生产环境禁止打印完整请求/响应

### 4. 列表和详情存在 N+1 查询风险
**位置：** [`backend/apps/applications/views.py`](../backend/apps/applications/views.py:67)  
**位置：** [`backend/apps/applications/serializers.py`](../backend/apps/applications/serializers.py:5)  
**位置：** [`backend/apps/approvals/serializers.py`](../backend/apps/approvals/serializers.py:26)

**问题：**
- `SerializerMethodField` 中反复访问 `obj.approvals.all()`
- 列表查询缺少针对审批和学生关联的系统性预取

**影响：**
- 数据量一大，列表接口性能明显下降
- 管理端分页查看时更明显

**修复建议：**
- 在视图中补 `select_related` / `prefetch_related`
- 让序列化器使用预取结果，而不是重复查库

### 5. 附件安全校验偏弱
**位置：** [`backend/apps/attachments/serializers.py`](../backend/apps/attachments/serializers.py:5)  
**位置：** [`backend/apps/attachments/views.py`](../backend/apps/attachments/views.py:144)

**问题：**
- 主要依赖扩展名和客户端 MIME
- 预览逻辑信任存储的 `content_type`

**影响：**
- 伪装文件类型的风险
- 预览链路安全边界不够硬

**修复建议：**
- 继续保留大小限制和扩展名白名单
- 增加服务端真实文件类型探测
- 下载/预览时增加更严格的安全头

### 6. 根路由硬编码外部跳转
**位置：** [`backend/config/urls.py`](../backend/config/urls.py:8)

**问题：**
- `/` 直接跳转到固定公网 IP

**影响：**
- 部署环境不通用
- 迁移和测试环境容易出问题

**修复建议：**
- 改为基于配置项跳转
- 或改为本地健康页/前端入口

## 四、测试与验证

**当前情况：**
- 代码里有不少测试文件，覆盖面不算弱
- 但本次环境里 pytest/测试执行链路不稳定，未能完成可靠的自动化验证

**建议：**
- 先修复 pytest 收集与运行配置
- 补一组针对 SSO、权限、附件下载、审批状态机的回归测试

## 五、修复优先级

### P0
1. 强制 SSO 认证校验
2. 移除硬编码密钥默认值
3. 停止打印敏感请求/响应内容

### P1
1. 修复列表/详情 N+1 查询
2. 加强附件真实文件类型校验
3. 去掉根路由硬编码跳转

### P2
1. 统一 API 错误响应格式
2. 整理 pytest / Django test 运行方式
3. 继续补齐性能和安全回归测试

## 六、建议落地顺序

1. 先封死认证绕过和密钥问题
2. 再处理日志泄漏和附件安全
3. 然后优化查询和测试体系
4. 最后再做部署与性能收敛

