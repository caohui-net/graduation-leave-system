# Codex审查 - 剩余章节（Round 2）

**审查时间：** 2026-05-27  
**审查人：** Codex Rescue Agent  
**审查范围：** API设计、审批流程、部署架构、安全设计、性能优化、测试策略

---

## 审查基线

Round 1已确认：
- 项目数据库：PostgreSQL单一数据库
- 外部系统：MySQL/SQL Server/Oracle（API对接）
- 部署方式：本地单实例部署
- 认证增强：5项安全措施
- 数据库设计：8个核心表 + 安全字段 + 复合索引 + 历史表

---

## 第3章：API设计

**裁决：** REVISE

**问题：**

1. **MAJOR**: 微信登录API（lines 698-723）未体现最终确定的绑定/安全流程（lines 1090-1106）：
   - 缺少学生身份验证
   - 缺少受限Token
   - 缺少`select_for_update`事务锁
   - 缺少`wechat_bind`审计日志
   - 缺少通用绑定失败错误

2. **MAJOR**: 配置API仍然建模运行时数据库切换：
   - `GET /configs?config_type=database`（line 1035）
   - `db.type=mysql`（line 1043）
   - 更新为`postgresql`（line 1058）
   - 与PostgreSQL单数据库冲突（lines 50, 1321）

3. **MAJOR**: 申请编号生成时机不一致：
   - API创建时返回`application_no`（lines 768-776）
   - 工作流说提交时生成（lines 1254-1257）
   - 数据库要求`application_no NOT NULL`（line 307）

4. **MAJOR**: 审批API（lines 907-945）缺少：
   - 乐观锁/版本检查
   - 当前审批人验证
   - 尽管applications表有`current_approver_id`和`version`字段（lines 316-327）

5. **MAJOR**: 上传API（lines 950-970）缺少Round 1文件安全要求：
   - MIME类型验证
   - 文件名清理
   - 哈希去重
   - 10MB限制
   - 数据库有`file_hash`字段（line 400）

6. **MINOR**: 创建/上传/删除使用`200`状态码（lines 770, 962, 989）
   - 建议：创建/上传用`201 Created`，删除用`204 No Content`

**建议：**
- 添加`/auth/wechat/bind`、`/auth/password/setup`端点
- 添加身份验证和受限Token端点
- 替换数据库配置示例为外部集成配置（`dorm_integration_type`、`dorm_api_url`、`dorm_db_config`）
- 审批/更新端点要求`version`或`If-Match`
- 文档化角色范围列表语义：学生查看自己记录，辅导员查看分配年级/当前审批人，管理员查看全部

---

## 第5章：审批流程设计

**裁决：** REVISE

**问题：**

1. **MAJOR**: 超时逻辑使用`submit_time__lt=now-24h`（lines 1298-1301）
   - Round 1要求使用`chinese_calendar`计算工作日
   - 排除周末/节假日
   - 使用9:00-17:00工作时间

2. **MAJOR**: `app.is_timeout = True`（lines 1306-1308）与最终数据库不匹配
   - `is_timeout`字段在`approvals`表，不在`applications`表（lines 371-372）

3. **MAJOR**: 工作流未提及设置：
   - `counselor_id`
   - `admin_id`
   - `current_approver_id`
   - 递增`version`
   - 尽管这些字段已确定（lines 310-327）

4. **MAJOR**: 工作流缺少：
   - `applications_history`快照
   - 提交/审批/驳回的审计日志
   - 尽管历史表和审计表已确定（lines 501-577）

5. **MAJOR**: 提交时生成申请编号（line 1256）与API创建和数据库`NOT NULL`冲突

6. **MINOR**: 强制上传宿舍证明（line 1251）应与外部宿舍系统验证和手动降级协调（lines 1332-1333, 1512-1514）

**建议：**
- 按审批节点跟踪超时，不是从原始提交时间
- 使用基于工作日的到期时间辅助函数
- 每次状态转换：验证状态+角色+当前审批人，锁定或检查版本，写入approval/audit/history行，更新`current_approver_id`

---

## 第7章：部署架构设计

**裁决：** REJECT

**问题：**

1. **CRITICAL**: 部署全程使用MySQL：
   - 服务列表（line 1528）
   - 网络架构（line 1545）
   - `depends_on mysql`（lines 1578, 1609）
   - `mysql:8.0`（lines 1584-1590）
   - `mysql_data`（line 1635）
   - `mysqldump`（line 1660）
   - 与PostgreSQL单数据库决策直接冲突（lines 50, 238, 1321）

2. **CRITICAL**: 指定3个Django副本：
   - 服务列表（line 1527）
   - 网络架构（lines 1542-1544）
   - `deploy.replicas: 3`（lines 1580-1581）
   - Round 1确定本地单实例部署（line 52, consensus lines 31-35）

3. **MAJOR**: MinIO作为基线服务（lines 1532, 1621-1632）
   - Round 1确定本地文件存储为基线

4. **MAJOR**: 备份脚本是MySQL特定的（line 1660）
   - 不适用于PostgreSQL

**建议：**
- 重写第7章围绕：`nginx`、单个`django-app`（Gunicorn 4 workers）、`postgres`、`redis`、`celery-worker`、`celery-beat`
- 使用`postgres:16`、`postgres_data`、`pg_dump`、本地`/data/uploads`
- MinIO仅作为可选的未来存储模式，不是基线compose的一部分

---

## 第8章：安全设计

**裁决：** REVISE

**问题：**

1. **MAJOR**: 缺少Round 1 API限流：
   - DRF throttling
   - Nginx速率限制
   - 登录5次/分钟
   - 上传10次/小时
   - 普通API 1000次/小时

2. **MAJOR**: 缺少文件上传安全：
   - `python-magic` MIME验证
   - 文件名清理
   - 哈希去重
   - 10MB限制
   - 当前章节仅涵盖通用SQL/XSS/CSRF

3. **MAJOR**: 认证安全章节（lines 1719-1731）未包含最终确定的5项微信/认证加固措施（lines 1101-1106）

4. **MAJOR**: 安全设计未涵盖安全敏感操作的审计日志
   - 尽管`audit_logs`已确定（lines 501-546）

5. **MINOR**: `SECURE_SSL_REDIRECT=True`（line 1712）应仅用于生产环境
   - 本地Docker部署可能需要Nginx后面的内部HTTP

**建议：**
- 添加子章节：速率限制、上传安全、微信绑定安全、审计日志、加密`system_configs`
- 如果需要bcrypt，显式配置Django `BCryptSHA256PasswordHasher`

---

## 第9章：性能优化设计

**裁决：** REVISE

**问题：**

1. **MAJOR**: 索引策略（lines 1741-1750）与最终确定的复合索引不匹配
   - 缺少：`idx_approver_status`、`idx_student_status`、`idx_status_deleted`、`idx_app_time`、`idx_app_type`、`idx_user_read_time`、审计日志复合索引
   - 来自lines 338-347, 377-380, 406-409, 447, 532-533

2. **MAJOR**: Django数据库配置（lines 1758-1768）使用非标准`MAX_CONNECTIONS`/`MIN_CONNECTIONS`选项
   - 对于Django 4.2 + psycopg2不是有效的PostgreSQL连接池设计

3. **MINOR**: 缓存申请状态（lines 1778-1782）可能产生过期审批视图
   - 除非在每次工作流转换时失效

4. **MINOR**: 异步文件上传（lines 1809-1813）需要一致性规则
   - 如果API在持久存储完成前返回成功

**建议：**
- 用最终确定的数据库索引替换索引列表，并将每个映射到其查询：待审批、学生列表、未读通知、审计查找
- 使用`CONN_MAX_AGE` + PgBouncer（如需连接池）
- 不要缓存权限决策；仅缓存计数/状态，并显式失效

---

## 第10章：测试策略

**裁决：** REVISE

**问题：**

1. **MAJOR**: 第10章未说明TDD工作流
   - 实施计划要求"每个功能先写测试，再写实现"（lines 662-663）

2. **MAJOR**: 未要求针对PostgreSQL运行测试
   - SQLite会错过`select_for_update`、PostgreSQL JSON/索引行为、生产数据库语义

3. **MAJOR**: 缺少5项认证加固措施的测试：
   - 身份验证
   - 受限Token范围
   - 事务锁
   - 审计日志
   - 通用绑定错误

4. **MAJOR**: 缺少覆盖：
   - RBAC/对象权限
   - API限流
   - 文件上传MIME/路径/哈希检查
   - 审计日志
   - 工作流历史记录

5. **MAJOR**: 性能目标（lines 1912-1914）说`1000+`用户和`>2000 QPS`
   - Round 1确定单本地实例峰值负载约500并发用户

6. **MINOR**: API测试期望创建响应`200`（line 1878）
   - 如果API变为RESTful，应改为`201`

**建议：**
- 按模块添加测试优先门：模型、服务/工作流、API、权限、集成
- 在CI/开发测试中使用PostgreSQL
- 添加双重审批和微信绑定竞态的并发测试
- 将性能目标与单实例部署对齐，然后用Locust测量

---

## 总结

**需要修改的章节：**
- 第3章（API设计）：REVISE - 5个MAJOR问题
- 第5章（审批流程）：REVISE - 5个MAJOR问题
- 第7章（部署架构）：REJECT - 2个CRITICAL + 2个MAJOR问题，需要完全重写
- 第8章（安全设计）：REVISE - 4个MAJOR问题
- 第9章（性能优化）：REVISE - 2个MAJOR问题
- 第10章（测试策略）：REVISE - 5个MAJOR问题

**最严重问题：**
1. 部署架构使用MySQL而非PostgreSQL（CRITICAL）
2. 部署架构使用3副本而非单实例（CRITICAL）
3. 所有章节与Round 1共识不一致

**下一步：**
逐章讨论并达成共识，然后应用修改。
