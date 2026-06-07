# 当前项目完整分析（Codex）

**分析日期：** 2026-05-27  
**分析范围：** 仓库全部可见文件、设计文档、实施计划、评审讨论记录、依赖文件、目录结构  
**结论级别：** 项目仍处于“设计文档 + 初始骨架”阶段，尚未形成可运行系统

---

## 1. 总体结论

当前仓库已经完成较完整的需求、系统设计、实施计划和多轮评审共识，核心方向基本清晰：Django + DRF 单体后端、PostgreSQL 单数据库、Redis + Celery、本地文件存储、微信登录/通知、宿舍系统优先 API 对接。

但实际代码尚未开始：`backend/apps`、`backend/config/settings`、`backend/utils`、`frontend/mobile`、`frontend/miniprogram`、`docker/nginx`、`docker/scripts` 都是空目录；没有 `manage.py`、Django settings、模型、API、Dockerfile、`docker-compose.yml`、前端 `package.json` 或测试代码。因此当前不能构建、不能运行、不能测试。

最大风险不是“功能缺少”，而是设计文档和实施计划中仍存在多处与既定共识冲突的细节。如果直接按当前计划开工，容易把已经达成的 PostgreSQL 单数据库、单实例部署、文件安全、工作日计算、测试目标等决策重新做偏。

---

## 2. 当前仓库状态

### 2.1 文件与目录

当前可见文件主要包括：

- `.gitignore`
- `backend/requirements/base.txt`
- `backend/requirements/dev.txt`
- `backend/requirements/prod.txt`
- `docs/PROJECT-SUMMARY.md`
- `docs/design/2026-05-27-system-design.md`
- `docs/superpowers/plans/2026-05-27-implementation-plan.md`
- `docs/discussions/codex-review-2026-05-27/*.md`

空目录包括：

- `backend/apps`
- `backend/config/settings`
- `backend/utils`
- `frontend/mobile`
- `frontend/miniprogram`
- `docker/nginx`
- `docker/scripts`

这说明 Phase 1 只完成了目录和 requirements 文件，尚未完成 Django 项目初始化。

### 2.2 Git 工作区

当前工作区已有未提交/未跟踪文件，包括 `.omc/` 下状态文件，以及 `docs/discussions/codex-review-2026-05-27/10-remaining-sections-review.md`、`11-remaining-sections-response.md`、`12-remaining-sections-consensus.md`。本次分析未回退这些文件。

---

## 3. 已完成资产

### 3.1 设计资产

`docs/design/2026-05-27-system-design.md` 内容覆盖较全面：

- 系统架构
- 数据库设计
- API 设计
- 认证授权
- 审批流程
- 外部系统集成
- 部署架构
- 安全设计
- 性能优化
- 测试策略

设计文档已经吸收了多轮评审中的关键结论，例如 PostgreSQL 单数据库、外部系统 API 优先、工作日计算、文件上传安全、API 限流、PostgreSQL 测试环境等。

### 3.2 评审资产

`docs/discussions/codex-review-2026-05-27/` 已形成比较完整的评审链路：

- 架构评审与回应
- 认证安全补充
- 数据库多轮评审
- 多数据库需求澄清
- 剩余章节评审与共识
- 总共识总结

这部分文档是当前项目最有价值的决策记录，应当作为实施基线。

### 3.3 依赖资产

后端 requirements 已经分为 base/dev/prod 三层，这是正确方向。但依赖内容与设计文档还有明显缺口，详见第 5 节。

---

## 4. 关键一致性问题

### 4.1 实施计划仍然残留“多数据库支持”

评审共识已经明确：本项目使用 PostgreSQL 单数据库，外部系统才可能涉及 MySQL/SQL Server/Oracle。

但实施计划仍写着：

- `docs/superpowers/plans/2026-05-27-implementation-plan.md:18`：支持“多数据库支持”
- `docs/superpowers/plans/2026-05-27-implementation-plan.md:189`：配置数据库连接“支持多数据库”
- `docs/superpowers/plans/2026-05-27-implementation-plan.md:195`：配置“MySQL/PostgreSQL服务”

这会直接误导 Phase 1，把核心数据库支持做复杂。建议立即把实施计划改成：

- 本项目只配置 PostgreSQL
- 外部系统直连作为 integrations 的可选后续能力
- 外部数据库驱动进入 optional requirements，不进入 base

### 4.2 性能目标存在冲突

设计文档第 10 章已经调整为单实例 500 并发用户：

- `docs/design/2026-05-27-system-design.md:2752`
- `docs/design/2026-05-27-system-design.md:2778`

但实施计划仍写：

- `docs/superpowers/plans/2026-05-27-implementation-plan.md:77`：支持 `1000+` 并发用户

建议统一为“峰值 500 并发用户、P95 < 200ms、关键 API 分场景测试”。如果保留 `1000+`，就应重新引入水平扩展、共享文件存储、分布式锁、容量规划和压测基线。

### 4.3 项目总结仍有旧口径

`docs/PROJECT-SUMMARY.md` 同时写了正确口径和旧口径。例如第 153 行仍称“支持多数据库（MySQL/PostgreSQL/SQL Server/Oracle）”。这与第 63 行的“PostgreSQL单数据库、外部系统API优先”冲突。

建议把项目总结改为：

- 本项目数据库：PostgreSQL
- 外部系统：优先 REST API，对无 API 的系统保留只读 SQLAlchemy 备选

---

## 5. 依赖分析

### 5.1 base.txt 过重且缺少关键依赖

`backend/requirements/base.txt` 当前包含：

- Django/DRF/SimpleJWT/CORS/filter
- PostgreSQL 驱动
- MySQL/Oracle/ODBC 驱动
- Celery/Redis
- wechatpy
- tenacity
- bcrypt
- python-decouple

问题：

1. `mysqlclient`、`cx-Oracle`、`pyodbc` 放在 base 中会增加安装失败概率，也不符合 PostgreSQL 单数据库基线。建议拆到 `requirements/integrations.txt` 或按外部直连场景单独安装。
2. 设计中使用了 `python-magic`，但 requirements 没有。
3. 设计中使用了 `chinese_calendar`，但 requirements 没有。
4. 设计中使用了 `requests`，但 requirements 没有直接声明。
5. 设计中使用了 `SQLAlchemy`，但 requirements 没有。
6. 设计中使用了 `cryptography.fernet`，但 requirements 没有。
7. 设计中配置 `django_redis.cache.RedisCache`，但 requirements 没有 `django-redis`。
8. 架构描述提到 `django-storages`，但 requirements 没有。如果基线仅本地文件存储，可以从设计中移除；如果保留存储抽象，应加入依赖。

### 5.2 密码依赖建议

设计文档写“密码使用 bcrypt 加密存储”，requirements 也加入了 `bcrypt`。但 Django 已有成熟 password hasher 体系，不建议自建 `password_hash` 字段和手写 bcrypt 流程。建议：

- 使用 Django `AbstractUser`/`AbstractBaseUser` 的 `password` 字段
- 配置 `PASSWORD_HASHERS`
- 如需 bcrypt，使用 Django 支持的 bcrypt hasher，而不是业务代码直接操作 `bcrypt`

---

## 6. 数据库设计风险

### 6.1 SQL 示例仍是 MySQL 风格，不是 PostgreSQL

设计文档已经声明 PostgreSQL，但表结构示例大量使用 MySQL 语法：

- `AUTO_INCREMENT`
- `COMMENT '...'`
- 表级 `COMMENT='...'`
- 内联 `INDEX ...`
- `ON UPDATE CURRENT_TIMESTAMP`

示例位置包括 `docs/design/2026-05-27-system-design.md:258` 起的 users 表，以及后续所有核心表。

如果这些 SQL 只是概念草图，应明确标注“伪 SQL，以 Django Model 为准”。如果要作为 PostgreSQL DDL，则必须改为 PostgreSQL 语法或直接给 Django models/migrations。

### 6.2 外键策略存在不可执行组合

多处字段声明 `NOT NULL`，但外键写 `ON DELETE SET NULL`：

- approvals：`approver_id BIGINT NOT NULL`，但外键 `ON DELETE SET NULL`
- audit_logs：`user_id BIGINT NOT NULL`，但外键 `ON DELETE SET NULL`

这在数据库层不可成立。建议：

- 审批记录和审计日志优先保留历史，用户删除应使用软删除或 `PROTECT`
- 如果确实允许置空，则字段必须 nullable
- 审计日志还应考虑保存操作者快照（姓名、角色、学号），避免用户变更后历史语义丢失

### 6.3 `ON DELETE PROTECT` 不是 PostgreSQL DDL

applications 表写了 `ON DELETE PROTECT`。这是 Django ORM 的行为，不是 PostgreSQL 外键动作。数据库层应使用 `RESTRICT`/`NO ACTION`，或只在模型层用 `on_delete=PROTECT`。

### 6.4 索引名在 PostgreSQL 中会冲突

设计文档多表重复使用 `idx_user_id`、`idx_application_id` 等索引名。PostgreSQL 中索引名在 schema 内需要唯一，不能像 MySQL 那样只在表内唯一。

如果使用 Django migrations，Django 会生成唯一名称；如果手写 SQL，需要改成：

- `idx_users_student_id`
- `idx_notifications_user_id`
- `idx_attachments_application_id`
- `idx_approvals_application_id`

### 6.5 软删除与唯一约束冲突

users 表对 `student_id`、`wechat_openid` 使用全局唯一。配合 `is_deleted` 软删除后，已删除用户仍会占用学号和 openid。

建议在 PostgreSQL 中使用条件唯一索引：

```sql
CREATE UNIQUE INDEX uniq_users_active_student_id
ON users(student_id)
WHERE is_deleted = false;
```

Django 中可用 `UniqueConstraint(condition=Q(is_deleted=False))`。

### 6.6 “活跃申请唯一约束”没有落到设计主文档

共识文档提到“一个学生只能有一个进行中申请”。设计主文档没有在 applications 表中明确部分唯一索引，仅在流程逻辑中描述。

建议用数据库级约束兜底：

```python
UniqueConstraint(
    fields=["student"],
    condition=Q(status__in=["draft", "pending_counselor", "pending_admin"], is_deleted=False),
    name="uniq_active_application_per_student",
)
```

### 6.7 审批超时动作与枚举不一致

approvals 表字段说明写 `action: approve/reject`，但超时任务会创建 `action='timeout'`。需要把 `timeout` 加入枚举，或把超时记录拆成独立 `approval_timeouts`/notification 事件，避免审批记录语义混乱。

### 6.8 办理时限“24小时”和“8工作小时”冲突

审批记录字段说明写“1个工作日(24小时)”，第 5 章又写“1个工作日 = 8小时工作时间”。建议统一为：

- SLA 展示：1 个工作日
- 计算口径：工作时间 9:00-17:00，共 8 个工作小时
- 数据字段：存 `due_at`、`sla_work_minutes`，不要只存 `time_limit INT`

### 6.9 历史快照应使用 JSONField

applications_history 表使用 `snapshot TEXT`。在 PostgreSQL + Django 下应优先使用 `JSONField`，便于校验、查询和迁移。评审讨论中也已经确认 JSONField 更合适，但主文档未完全落地。

---

## 7. API 与业务流程风险

### 7.1 204 响应不应带 body

附件删除 API 示例返回：

```json
{
  "code": 204,
  "message": "删除成功"
}
```

HTTP 204 按规范不应返回响应体。建议统一改为：

- `200` + 标准响应体；或
- `204 No Content` + 空响应体

### 7.2 乐观锁覆盖面不够明确

审批 API 已有 `version` 字段和 409 响应，但更新申请、重新提交、附件变更、生成凭证等也可能改变申请状态或可审批性。建议明确所有会影响审批判断的写操作都必须纳入版本控制。

### 7.3 驳回后重新提交的权限与状态未完全对齐

RBAC 描述中学生只能“修改草稿状态的申请”，但流程允许 rejected 重新提交。需要明确：

- rejected 状态允许学生修改
- 修改后是否仍保留原 application_no
- version 如何递增
- 旧附件是否保留、替换或标记失效

### 7.4 辅导员权限模型过粗

文档写“辅导员查看本年级所有申请”。实际高校场景通常按学院、专业、班级、辅导员负责范围授权，仅年级不足以防止越权。

建议新增 `counselor_assignments` 或在用户/班级模型中维护负责关系，并在查询和审批时同时校验 `current_approver_id`。

### 7.5 微信 openid 不应作为客户端绑定凭据

微信登录未绑定时，API 示例把 `wechat_openid` 返回给客户端。更稳妥的做法是：

- openid 只保存在服务端临时会话、Redis 或加密 temp token claim 中
- 客户端只拿 `temp_token`
- 绑定时后端从 temp token 解析 openid，不信任客户端提交的 openid

---

## 8. 认证与安全风险

### 8.1 Access Token 7 天偏长

设计中 Access Token 有效期为 7 天，Refresh Token 30 天。对审批、附件、个人信息系统来说，7 天 access token 偏长。建议：

- Access Token：15 分钟到 1 小时
- Refresh Token：7 到 30 天
- Refresh Token 轮换并加入黑名单
- 小程序端结合静默刷新

### 8.2 审计日志可能记录敏感数据

audit_logs 设计有 `request_data` 字段。需要明确脱敏策略，否则登录密码、验证码、JWT、微信 code、API 密钥、外部数据库连接串都可能进入审计日志。

建议：

- 审计中间件默认按白名单记录字段
- 对 `password`、`token`、`secret`、`key`、`authorization`、`verification_code` 等字段统一遮蔽
- 加密配置查看操作只记录“访问行为”，不记录明文

### 8.3 文件上传安全还缺少存储隔离要求

已有 MIME 校验、文件名清理、大小限制和哈希去重，这是正确方向。还应补充：

- 上传目录不可被 Nginx 直接执行
- 下载必须经过权限校验视图或内部重定向
- 文件保存名使用 UUID/hash，不使用用户原始文件名作为真实路径
- 对 PDF/DOC/DOCX 只做下载，不做服务端解析渲染
- 对图片预览设置安全响应头

### 8.4 Nginx 限流路径写法不可直接使用

文档示例：

```nginx
location /api/v1/applications/*/attachments
```

Nginx prefix location 不支持这种 `*` 通配写法。应使用正则 location，例如：

```nginx
location ~ ^/api/v1/applications/[^/]+/attachments$ { ... }
```

---

## 9. 外部系统集成风险

### 9.1 第 6 章存在明显合并残留

`docs/design/2026-05-27-system-design.md:1718-1737` 在 SQL 配置代码块后出现了一段缩进错乱的 Python 代码片段，随后 `6.3` 标题又重复出现。这是文档合并残留，容易误导实现。

建议清理为：

- 6.3 API 客户端
- 6.4 SQLAlchemy 备选客户端
- 6.5 配置存储
- 6.6 错误处理、重试、降级

### 9.2 SQLAlchemy 备选能力缺少依赖和边界

文档有 SQLAlchemy 示例，但 requirements 没有 SQLAlchemy。且数据库直连应明确：

- 只读账户
- 只允许参数化查询
- 查询模板白名单
- 连接字符串密码 URL encode
- 查询超时
- 审计日志
- 不参与本项目事务

### 9.3 宿舍系统字段契约不足

当前只描述 `is_cleared`、`clearance_date`、`room_no`。建议补充：

- 外部系统状态码映射
- 未找到学生时如何处理
- 数据过期时间
- 人工跳过验证的审批责任归属
- 外部系统不可用时是否允许提交还是只允许审批时跳过

---

## 10. 部署设计风险

### 10.1 当前没有实际部署文件

仓库没有：

- `Dockerfile`
- `docker-compose.yml`
- `docker/nginx/nginx.conf`
- `docker/scripts/backup.sh`
- `.env.example`

Phase 1 下一步应优先补齐这些文件，而不是继续扩展业务设计。

### 10.2 compose 示例路径不一致

设计文档中 compose 示例使用：

- `build: .`
- `./nginx.conf:/etc/nginx/nginx.conf`
- `./uploads:/app/uploads`

但规划目录是：

- `backend/`
- `docker/nginx/nginx.conf`
- `/data/uploads`

建议确定基准：

- `django-app.build.context: ./backend`
- nginx 配置挂载 `./docker/nginx/nginx.conf`
- 上传目录统一为 `/data/uploads:/app/uploads` 或 `./uploads:/app/uploads`
- 备份脚本与实际 volume 路径保持一致

### 10.3 缺少启动顺序和健康检查

compose 示例只有 `depends_on`，不能保证 Postgres/Redis 已可用。建议添加：

- Postgres healthcheck
- Redis healthcheck
- Django entrypoint 中等待数据库
- `python manage.py migrate`
- `python manage.py collectstatic --noinput`

是否自动执行 migration 需要按部署策略决定，但必须有明确命令。

### 10.4 备份脚本需要改成可执行部署资产

文档里的备份命令方向正确，但实际落地时需要：

- 使用 compose service 名称，而不是假设容器名 `postgres`
- 备份文件落到被持久化的目录
- 失败时返回非 0
- 定期校验恢复
- 文件备份与数据库备份时间点一致性说明

---

## 11. 性能与缓存风险

### 11.1 500 QPS 目标需按接口拆分

单实例 Gunicorn 4 workers 下，`500 并发用户` 与 `>500 QPS` 可能对只读列表接口可达，但对审批写入、附件上传、外部系统调用不现实。建议性能指标按接口分类：

- 登录：P95
- 申请列表：P95/QPS
- 申请提交：P95/QPS
- 审批操作：P95/QPS
- 文件上传：成功率/耗时
- 外部系统查询：超时率/降级率

### 11.2 缓存必须先做权限校验

设计中缓存申请详情、申请状态、学生申请列表。对含个人信息和审批信息的数据，必须保证：

- 缓存 key 包含用户或权限域，或
- 读取缓存前先做对象权限校验，或
- 只缓存非敏感派生数据

否则容易出现越权读取缓存数据。

### 11.3 索引策略需要结合查询再精简

设计列了很多单列索引和复合索引。实施时不建议一次性照搬所有索引，应先根据核心查询建立最小索引集：

- 学生申请列表
- 审批人待办列表
- 通知未读列表
- 审计日志按资源/用户查询
- 附件按申请查询

单列索引如果被复合索引覆盖，应避免重复创建。

---

## 12. 测试策略分析

测试策略方向正确：pytest、PostgreSQL、TDD、覆盖率 80%+、并发测试、文件安全测试、限流测试、审计测试。

当前缺口：

- 没有 pytest 配置
- 没有测试目录
- 没有 PostgreSQL 测试 compose
- dev requirements 缺少 `pytest-mock`、`bandit`、`pre-commit`、`locust` 等计划中提到或实际需要的工具
- 并发测试需要真实 PostgreSQL，SQLite 无法覆盖 `select_for_update`

建议 Phase 1 就建立最小测试基线：

- `pytest.ini`
- `conftest.py`
- Docker/compose test database
- 一个可运行的健康检查测试
- CI 或本地 `make test`/脚本命令

---

## 13. 前端分析

当前前端仅有空目录。设计计划同时做 React Native 和微信小程序，但需求里明确“挂在微信公众号”，小程序很可能是首要交付端。

建议降低初期交付风险：

1. 先确认首发端：微信小程序优先，React Native 后续。
2. 先产出 OpenAPI/接口契约，避免两个前端各自猜接口。
3. 附件上传、微信授权、Token 刷新、审批待办这四个流程应先做端到端原型。
4. React Native 与小程序不要在第 8-9 周才开始完全介入，至少要在后端 API 定稿时同步验证登录和上传能力。

---

## 14. 推荐修复顺序

### P0：开工前必须修正

1. 更新实施计划，移除本项目“多数据库支持”和 MySQL/PostgreSQL 并列部署说法。
2. 将性能目标统一为单实例 500 并发用户。
3. 修复系统设计文档第 6 章合并残留和重复标题。
4. 明确数据库 DDL 是伪 SQL 还是 PostgreSQL DDL；建议以 Django Model 为准。
5. 调整 requirements：补齐必要依赖，拆出外部数据库可选依赖。
6. 明确软删除 + 唯一约束 + 活跃申请唯一约束的 PostgreSQL 实现。

### P1：Phase 1 应完成

1. 创建可运行 Django 项目：`manage.py`、settings、urls、wsgi/asgi。
2. 创建 Dockerfile、docker-compose、nginx.conf、`.env.example`。
3. 建立 pytest + PostgreSQL 测试基线。
4. 建立基础代码质量工具：black、isort、flake8/mypy、pre-commit。
5. 建立统一响应、异常、审计脱敏、request id/correlation id 基础设施。

### P2：业务模块实施前应定稿

1. 用户模型选择：基于 Django password 体系，不自建 `password_hash`。
2. RBAC 模型：辅导员负责范围不能只靠年级。
3. 审批状态机：明确 rejected 重新提交、version 递增、附件替换规则。
4. 文件存储：真实路径、下载鉴权、预览策略、病毒/恶意文件边界。
5. 宿舍系统集成契约：状态码、超时、降级、人工跳过责任。

---

## 15. 建议的近期任务清单

建议下一次实施直接按以下顺序推进：

1. 清理并更新文档漂移：实施计划、项目总结、设计第 6 章。
2. 调整 requirements：
   - base：Django/DRF/PostgreSQL/Redis/Celery/SimpleJWT/requests/python-magic/chinese-calendar/cryptography/django-redis
   - dev：pytest 工具、pre-commit、安全扫描、压测工具
   - integrations：mysqlclient/pyodbc/Oracle/SQLAlchemy 等可选直连依赖
3. 初始化 Django 项目和 settings 分层。
4. 写 docker-compose 最小可运行环境：Django + Postgres + Redis。
5. 建立第一个测试：Django 启动、数据库连接、健康检查 API。
6. 再进入 accounts 模块，而不是先写完整业务。

---

## 16. 本次未执行的事项

没有运行测试、构建或服务启动，因为当前仓库没有可运行的 Django 项目、Docker 配置或测试代码。当前分析基于静态文件审查。

---

## 17. 最终判断

项目方向是可行的，设计深度已经足够进入实施；但在进入编码前，需要先消除文档和计划中的旧决策残留。尤其是数据库、依赖、部署和认证安全这四类问题，如果不先统一，会在 Phase 1 产生结构性返工。

建议把当前仓库状态定义为：

> 设计评审完成，实施骨架初建；尚未达到“项目初始化完成”。

下一步目标应是把它推进到：

> 本地 Docker 可启动，Django 可访问，PostgreSQL/Redis 可连接，pytest 可运行。
