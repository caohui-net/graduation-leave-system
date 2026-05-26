# 毕业生离校申请审批系统 - 系统设计文档

**项目名称：** 毕业生离校申请审批系统  
**文档版本：** v1.0  
**创建日期：** 2026-05-27  
**设计方案：** Django单体架构 + 容器化部署

---

## 目录

1. [系统架构设计](#1-系统架构设计)
2. [数据库设计](#2-数据库设计)
3. [API设计](#3-api设计)
4. [认证授权设计](#4-认证授权设计)
5. [审批流程设计](#5-审批流程设计)
6. [外部系统集成设计](#6-外部系统集成设计)
7. [部署架构设计](#7-部署架构设计)
8. [安全设计](#8-安全设计)
9. [性能优化设计](#9-性能优化设计)
10. [测试策略](#10-测试策略)

---

## 需求概述

### 业务流程

1. **流程发起：** 毕业生个人申请
   - 登录离校管理系统（挂在微信公众号）
   - 填写离校申请表，明确计划离校日期
   - 上传规定附件（宿舍清退证明、图书馆清书证明、财务结清截图）
   - 提交申请（需提前3个工作日）

2. **一级审批：** 毕业年级辅导员审核
   - 核实学生各项离校手续
   - 同意或驳回（注明原因）
   - 办理时限：1个工作日

3. **终端备案：** 学工部管理科负责人终审
   - 最终备案审核
   - 生成电子离校凭证
   - 办理时限：1个工作日

### 技术选型

- **平台：** iOS/Android + 微信小程序
- **前端：** React Native + 小程序原生
- **后端：** Python Django 4.2 + DRF
- **数据库：** PostgreSQL（本项目）+ 外部系统对接（MySQL/SQL Server/Oracle）
- **认证：** 混合认证（学号+密码 + 微信OAuth2）
- **部署：** Docker容器化部署（本地部署，单实例）

---

## 1. 系统架构设计

### 1.1 整体架构

```
┌─────────────────────────────────────────────┐
│           客户端层(Client Layer)            │
├──────────────┬──────────────┬───────────────┤
│ React Native │ React Native │  微信小程序    │
│   (iOS)      │  (Android)   │               │
└──────────────┴──────────────┴───────────────┘
                      │
                      ↓ HTTPS
┌─────────────────────────────────────────────┐
│         负载均衡层 (Load Balancer)          │
│              Nginx (容器)                   │
└─────────────────────────────────────────────┘
                      │
                      ↓
              ┌──────────────┐
              │   Django     │
              │   App        │
              │  (容器)      │
              │ Gunicorn     │
              │ 4 workers    │
              └──────────────┘
                      │
        ┌─────────────┴─────────────┐
        ↓                           ↓
┌──────────────┐            ┌──────────────┐
│   数据库层    │            │   缓存层      │
│ PostgreSQL   │            │   Redis      │
│  (容器)      │            │  (容器)      │
│              │            │              │
└──────────────┘            └──────────────┘
└──────────────┘                    │
        │                   ┌──────────────┐
        │                   │  任务队列     │
        │                   │  Celery      │
        │                   │  Worker      │
        │                   │  (容器)      │
        │                   └──────────────┘
        ↓
┌──────────────────────────────────────────┐
│         外部系统集成层                    │
├──────────────┬───────────────────────────┤
│ 宿舍管理系统  │  微信公众平台 │ 文件存储   │
│  (HTTP API) │  (OAuth2)    │ (本地/MinIO)│
└──────────────┴───────────────────────────┘
```

### 1.2 技术栈明细

**后端框架：**
- Django 4.2 LTS（长期支持版本）
- Django REST Framework 3.14（API开发）
- django-cors-headers（跨域支持）
- django-filter（过滤查询）

**数据库驱动：**
- mysqlclient（MySQL）
- psycopg2（PostgreSQL）
- mssql-django（SQL Server）
- cx_Oracle（Oracle）

**认证授权：**
- djangorestframework-simplejwt（JWT令牌）
- django-allauth（多认证方式）
- wechatpy（微信SDK）

**任务队列：**
- Celery 5.3（异步任务）
- Redis 7.0（消息代理+缓存）

**文件存储：**
- django-storages（存储抽象层）
- 本地文件系统
- MinIO（可选，本地对象存储）

### 1.3 模块划分

```
graduation_leave/
├── apps/
│   ├── accounts/          # 用户账户模块
│   │   ├── models.py      # 用户模型
│   │   ├── views.py       # 登录/注册API
│   │   ├── serializers.py # 数据序列化
│   │   └── auth.py        # 认证逻辑
│   │
│   ├── applications/      # 离校申请模块
│   │   ├── models.py      # 申请模型
│   │   ├── views.py       # 申请CRUD API
│   │   ├── workflows.py   # 审批流程
│   │   └── states.py      # 状态机定义
│   │
│   ├── approvals/         # 审批管理模块
│   │   ├── models.py      # 审批记录
│   │   ├── views.py       # 审批操作API
│   │   └── permissions.py # 权限控制
│   │
│   ├── attachments/       # 附件管理模块
│   │   ├── models.py      # 附件模型
│   │   ├── views.py       # 上传/下载API
│   │   └── storage.py     # 存储配置
│   │
│   ├── notifications/     # 通知模块
│   │   ├── models.py      # 通知记录
│   │   ├── tasks.py       # Celery异步任务
│   │   └── wechat.py      # 微信推送
│   │
│   └── integrations/      # 外部系统集成
│       ├── dorm_system.py # 宿舍系统对接
│       └── base.py        # 集成基类
│
├── config/                # 配置模块
│   ├── settings/
│   │   ├── base.py        # 基础配置
│   │   ├── dev.py         # 开发环境
│   │   └── prod.py        # 生产环境
│   └── database.py        # 数据库动态配置
│
└── utils/                 # 工具模块
    ├── validators.py      # 数据校验
    ├── exceptions.py      # 异常定义
    └── responses.py       # 统一响应格式
```

**模块职责：**

1. **accounts（用户账户）**
   - 学生/辅导员/学工部用户管理
   - 学号+密码登录
   - 微信OAuth2授权登录
   - JWT令牌生成和验证
   - 用户权限管理

2. **applications（离校申请）**
   - 申请表单创建
   - 申请信息修改
   - 申请状态查询
   - 申请历史记录
   - 离校日期管理

3. **approvals（审批管理）**
   - 辅导员审批操作
   - 学工部备案操作
   - 审批意见记录
   - 驳回原因记录
   - 审批时限监控

4. **attachments（附件管理）**
   - 附件上传（宿舍清退证明、图书馆清书证明、财务结清截图）
   - 附件下载
   - 附件预览
   - 附件存储管理（本地文件系统/MinIO）
   - 附件大小和格式校验
   - 附件与申请关联

5. **notifications（通知模块）**
   - 微信模板消息推送
   - 审批状态变更通知
   - 驳回原因通知
   - 审批完成通知
   - 异步任务队列（Celery）
   - 通知发送记录

6. **integrations（外部系统集成）**
   - 宿舍管理系统API对接
   - 宿舍清退状态查询
   - 外部系统认证
   - 接口重试机制
   - 接口超时处理
   - 插件化设计（便于扩展其他系统）

---

## 2. 数据库设计

### 2.1 数据库概述

**设计原则：**
- 本项目使用PostgreSQL数据库
- 使用 Django ORM 抽象层
- 遵循第三范式（3NF）
- 预留扩展字段
- 软删除设计（Django应用层过滤 + PROTECT外键）
- 外部系统对接支持多种数据库（API优先，SQLAlchemy备选）

**核心表：**
1. users - 用户表
2. applications - 离校申请表
3. approvals - 审批记录表
4. attachments - 附件表
5. notifications - 通知表
6. system_configs - 系统配置表
7. audit_logs - 审计日志表
8. applications_history - 申请历史表

### 2.2 用户表（users）

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(20) UNIQUE NOT NULL COMMENT '学号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    password_hash VARCHAR(255) COMMENT '密码哈希',
    wechat_openid VARCHAR(100) UNIQUE COMMENT '微信OpenID',
    
    -- 认证安全字段
    password_setup_required BOOLEAN DEFAULT FALSE COMMENT '需要设置密码',
    account_locked BOOLEAN DEFAULT FALSE COMMENT '账户锁定',
    failed_login_attempts INT DEFAULT 0 COMMENT '失败登录次数',
    last_login_at TIMESTAMP COMMENT '最后登录时间',
    last_login_ip VARCHAR(50) COMMENT '最后登录IP',
    wechat_bind_time TIMESTAMP COMMENT '微信绑定时间',
    password_changed_at TIMESTAMP COMMENT '密码修改时间',
    
    phone VARCHAR(20) COMMENT '手机号',
    email VARCHAR(100) COMMENT '邮箱',
    role VARCHAR(20) NOT NULL COMMENT '角色: student/counselor/admin',
    department VARCHAR(100) COMMENT '院系',
    major VARCHAR(100) COMMENT '专业',
    class_name VARCHAR(50) COMMENT '班级',
    grade INT COMMENT '年级',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    is_deleted BOOLEAN DEFAULT FALSE COMMENT '是否删除',
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    
    INDEX idx_student_id (student_id),
    INDEX idx_role (role),
    INDEX idx_wechat_openid (wechat_openid),
    INDEX idx_account_locked (account_locked),
    
    CONSTRAINT chk_auth_method CHECK (
        (password_hash IS NOT NULL) OR (wechat_openid IS NOT NULL)
    )
) COMMENT='用户表';
```

**字段说明：**
- `role`: student（学生）、counselor（辅导员）、admin（学工部管理员）
- `wechat_openid`: 微信授权登录后绑定
- `is_deleted`: 软删除标记

### 2.3 离校申请表（applications）

```sql
CREATE TABLE applications (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    application_no VARCHAR(50) UNIQUE NOT NULL COMMENT '申请编号',
    student_id BIGINT NOT NULL COMMENT '学生ID',
    
    -- 固定审批人追踪
    counselor_id BIGINT COMMENT '辅导员ID',
    admin_id BIGINT COMMENT '学工部管理员ID',
    
    planned_leave_date DATE NOT NULL COMMENT '计划离校日期',
    status VARCHAR(20) NOT NULL COMMENT '状态',
    current_approver_id BIGINT COMMENT '当前审批人ID',
    submit_time TIMESTAMP COMMENT '提交时间',
    complete_time TIMESTAMP COMMENT '完成时间',
    reject_reason TEXT COMMENT '驳回原因',
    remarks TEXT COMMENT '备注',
    
    -- 凭证追踪
    certificate_url VARCHAR(500) COMMENT '离校凭证URL',
    certificate_generated_at TIMESTAMP COMMENT '凭证生成时间',
    
    -- 乐观锁
    version INT DEFAULT 0 COMMENT '版本号',
    
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE PROTECT,
    FOREIGN KEY (counselor_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (current_approver_id) REFERENCES users(id) ON DELETE SET NULL,
    
    INDEX idx_student_id (student_id),
    INDEX idx_counselor_id (counselor_id),
    INDEX idx_admin_id (admin_id),
    INDEX idx_status (status),
    INDEX idx_application_no (application_no),
    INDEX idx_planned_leave_date (planned_leave_date),
    INDEX idx_approver_status (current_approver_id, status, submit_time),
    INDEX idx_student_status (student_id, status, created_at),
    INDEX idx_status_deleted (status, is_deleted, submit_time)
) COMMENT='离校申请表';
```

**状态枚举（status）：**
- `draft` - 草稿
- `pending_counselor` - 待辅导员审核
- `pending_admin` - 待学工部备案
- `approved` - 审批通过
- `rejected` - 已驳回

**申请编号规则：**
`LX{YYYYMMDD}{6位序号}` 例如：LX202605270000001

### 2.4 审批记录表（approvals）

```sql
CREATE TABLE approvals (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    application_id BIGINT NOT NULL COMMENT '申请ID',
    approver_id BIGINT NOT NULL COMMENT '审批人ID',
    approver_role VARCHAR(20) NOT NULL COMMENT '审批人角色',
    action VARCHAR(20) NOT NULL COMMENT '操作: approve/reject',
    opinion TEXT COMMENT '审批意见',
    approval_time TIMESTAMP NOT NULL COMMENT '审批时间',
    time_limit INT COMMENT '办理时限(小时)',
    is_timeout BOOLEAN DEFAULT FALSE COMMENT '是否超时',
    created_at TIMESTAMP,
    
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
    FOREIGN KEY (approver_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_application_id (application_id),
    INDEX idx_approver_id (approver_id),
    INDEX idx_approval_time (approval_time),
    INDEX idx_app_time (application_id, approval_time DESC)
) COMMENT='审批记录表';
```

**字段说明：**
- `approver_role`: counselor（辅导员）、admin（学工部）
- `action`: approve（同意）、reject（驳回）
- `time_limit`: 辅导员1个工作日(24小时)，学工部1个工作日(24小时)
- `is_timeout`: 超过时限标记为超时

### 2.5 附件表（attachments）

```sql
CREATE TABLE attachments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    application_id BIGINT NOT NULL COMMENT '申请ID',
    file_name VARCHAR(255) NOT NULL COMMENT '文件名',
    file_path VARCHAR(500) NOT NULL COMMENT '文件路径',
    file_size BIGINT NOT NULL COMMENT '文件大小(字节)',
    file_type VARCHAR(50) NOT NULL COMMENT '文件类型',
    file_hash VARCHAR(64) COMMENT 'SHA256文件哈希',
    attachment_type VARCHAR(50) NOT NULL COMMENT '附件类型',
    upload_time TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
    INDEX idx_application_id (application_id),
    INDEX idx_attachment_type (attachment_type),
    INDEX idx_file_hash (file_hash),
    INDEX idx_app_type (application_id, attachment_type, is_deleted)
) COMMENT='附件表';
```

**附件类型（attachment_type）：**
- `dorm_clearance` - 宿舍清退证明
- `library_clearance` - 图书馆清书证明
- `finance_settlement` - 财务结清截图
- `other` - 其他附件

**文件限制：**
- 单文件最大 10MB
- 支持格式：jpg, png, pdf, doc, docx
- 存储路径：`/data/uploads/{year}/{month}/{application_no}/`

### 2.6 通知表（notifications）

```sql
CREATE TABLE notifications (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '接收用户ID',
    application_id BIGINT COMMENT '关联申请ID',
    notification_type VARCHAR(50) NOT NULL COMMENT '通知类型',
    title VARCHAR(200) NOT NULL COMMENT '通知标题',
    content TEXT NOT NULL COMMENT '通知内容',
    is_read BOOLEAN DEFAULT FALSE COMMENT '是否已读',
    send_status VARCHAR(20) DEFAULT 'pending' COMMENT '发送状态',
    retry_count INT DEFAULT 0 COMMENT '重试次数',
    last_retry_at TIMESTAMP COMMENT '最后重试时间',
    send_time TIMESTAMP COMMENT '发送时间',
    read_time TIMESTAMP COMMENT '阅读时间',
    created_at TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_is_read (is_read),
    INDEX idx_send_status (send_status),
    INDEX idx_user_read_time (user_id, is_read, created_at DESC)
) COMMENT='通知表';
```

**通知类型（notification_type）：**
- `application_submitted` - 申请已提交
- `approval_pending` - 待审批
- `application_approved` - 申请通过
- `application_rejected` - 申请驳回
- `approval_timeout` - 审批超时提醒

**发送状态（send_status）：**
- `pending` - 待发送
- `sent` - 已发送
- `failed` - 发送失败

### 2.7 系统配置表（system_configs）

```sql
CREATE TABLE system_configs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(100) UNIQUE NOT NULL COMMENT '配置键',
    config_value TEXT NOT NULL COMMENT '配置值',
    config_type VARCHAR(20) NOT NULL COMMENT '配置类型',
    description VARCHAR(500) COMMENT '配置说明',
    is_encrypted BOOLEAN DEFAULT FALSE COMMENT '是否加密',
    updated_by BIGINT COMMENT '更新人ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_config_key (config_key),
    FOREIGN KEY (updated_by) REFERENCES users(id)
) COMMENT='系统配置表';
```

**配置类型（config_type）：**
- `storage` - 文件存储配置
- `wechat` - 微信配置
- `notification` - 通知配置
- `workflow` - 流程配置
- `integration` - 外部系统集成配置
- `security` - 安全配置

**核心配置项：**
- `storage.type` - 存储类型（local/minio）
- `wechat.appid` - 微信AppID
- `wechat.secret` - 微信Secret（加密存储）
- `dorm_integration_type` - 宿舍系统集成类型（api/database）
- `dorm_api_url` - 宿舍系统API地址
- `dorm_api_key` - 宿舍系统API密钥（加密存储）
- `dorm_db_config` - 宿舍系统数据库配置（加密存储，JSON格式）
- `audit_log_retention_days` - 审计日志保留天数（默认1095天/3年）
- `encryption_key` - 配置加密密钥（存储在环境变量，不在数据库）

### 2.8 审计日志表（audit_logs）

```sql
CREATE TABLE audit_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL COMMENT '操作用户ID',
    session_id VARCHAR(100) COMMENT '会话ID',
    correlation_id VARCHAR(100) COMMENT '关联ID',
    action VARCHAR(50) NOT NULL COMMENT '操作类型',
    resource_type VARCHAR(50) NOT NULL COMMENT '资源类型',
    resource_id BIGINT COMMENT '资源ID',
    
    -- 变更追踪
    field_name VARCHAR(100) COMMENT '修改字段',
    old_value TEXT COMMENT '修改前值',
    new_value TEXT COMMENT '修改后值',
    
    ip_address VARCHAR(50) COMMENT 'IP地址',
    user_agent TEXT COMMENT '用户代理',
    request_data TEXT COMMENT '请求数据',
    response_status INT COMMENT '响应状态码',
    error_message TEXT COMMENT '错误信息',
    created_at TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_session_id (session_id),
    INDEX idx_correlation_id (correlation_id),
    INDEX idx_action (action),
    INDEX idx_resource_type (resource_type),
    INDEX idx_created_at (created_at),
    INDEX idx_user_action_time (user_id, action, created_at DESC),
    INDEX idx_resource_time (resource_type, resource_id, created_at DESC)
) COMMENT='审计日志表';
```

**操作类型（action）：**
- `login` - 登录
- `logout` - 登出
- `create_application` - 创建申请
- `update_application` - 更新申请
- `approve` - 审批通过
- `reject` - 审批驳回
- `upload_attachment` - 上传附件
- `delete_attachment` - 删除附件
- `update_config` - 更新配置

**资源类型（resource_type）：**
- `user` - 用户
- `application` - 申请
- `approval` - 审批
- `attachment` - 附件
- `config` - 配置

### 2.9 申请历史表（applications_history）

```sql
CREATE TABLE applications_history (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    application_id BIGINT NOT NULL COMMENT '申请ID',
    version INT NOT NULL COMMENT '版本号',
    snapshot TEXT NOT NULL COMMENT '申请快照(JSON)',
    changed_by BIGINT COMMENT '修改人ID',
    change_reason VARCHAR(100) COMMENT '修改原因',
    created_at TIMESTAMP,
    
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_application_id (application_id),
    INDEX idx_version (application_id, version)
) COMMENT='申请历史表';
```

**字段说明：**
- `snapshot`: JSON格式存储申请完整数据
- `change_reason`: 驳回重提、修改申请等
- 每次申请状态变更或内容修改时创建历史记录

### 2.10 数据库关系图

**核心关系：**

```
users (用户表)
  ├─1:N─→ applications (学生创建多个申请)
  ├─1:N─→ approvals (审批人审批多个申请)
  └─1:N─→ notifications (用户接收多个通知)

applications (申请表)
  ├─N:1─→ users (申请人)
  ├─N:1─→ users (辅导员)
  ├─N:1─→ users (学工部管理员)
  ├─N:1─→ users (当前审批人)
  ├─1:N─→ approvals (一个申请多条审批记录)
  ├─1:N─→ attachments (一个申请多个附件)
  ├─1:N─→ notifications (一个申请多条通知)
  └─1:N─→ applications_history (一个申请多个历史版本)
  └─1:N─→ notifications (一个申请触发多个通知)

approvals (审批记录表)
  ├─N:1─→ applications (多条审批记录属于一个申请)
  └─N:1─→ users (审批人)

attachments (附件表)
  └─N:1─→ applications (多个附件属于一个申请)

notifications (通知表)
  ├─N:1─→ users (接收人)
  └─N:1─→ applications (关联申请)

audit_logs (审计日志表)
  └─N:1─→ users (操作人)

system_configs (系统配置表)
  └─N:1─→ users (更新人)
```

**关键约束：**
1. 一个学生可以创建多个申请（不同时间段）
2. 一个申请必须经过2级审批（辅导员→学工部）
3. 每个审批节点记录一条审批记录
4. 附件与申请强关联，申请删除时级联删除附件
5. 通知异步发送，失败不影响主流程

---
## 3. API设计

### 3.1 API设计原则

**RESTful规范：**
- 使用标准HTTP方法（GET/POST/PUT/DELETE）
- 资源导向的URL设计
- 统一的响应格式
- 合理的HTTP状态码

**版本控制：**
- URL版本：`/api/v1/`
- 向后兼容，废弃API保留至少2个版本

**认证方式：**
- JWT Token认证
- Token有效期：7天
- Refresh Token机制

**响应格式：**
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": 1716768467
}
```

**错误响应：**
```json
{
  "code": 400,
  "message": "参数错误",
  "errors": {
    "planned_leave_date": ["日期不能早于今天"]
  },
  "timestamp": 1716768467
}
```

### 3.2 认证相关API

**1. 学号密码登录**
```
POST /api/v1/auth/login
Content-Type: application/json

Request:
{
  "student_id": "2020001",
  "password": "123456"
}

Response:
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "expires_in": 604800,
    "user": {
      "id": 1,
      "student_id": "2020001",
      "name": "张三",
      "role": "student"
    }
  }
}
```

**2. 微信授权登录**
```
POST /api/v1/auth/wechat/login
Content-Type: application/json

Request:
{
  "code": "wx_auth_code"
}

Response (已绑定账户):
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "user": {
      "id": 1,
      "student_id": "2020001",
      "name": "张三",
      "wechat_openid": "oXXXX"
    }
  }
}

Response (未绑定，需要绑定):
{
  "code": 200,
  "message": "需要绑定学号",
  "data": {
    "requires_binding": true,
    "wechat_openid": "oXXXX",
    "temp_token": "eyJhbGc..."
  }
}

Response (新用户，需要设置密码):
{
  "code": 200,
  "message": "需要完成注册",
  "data": {
    "requires_setup": true,
    "limited_token": "eyJhbGc...",
    "scope": "password_setup_only"
  }
}
```

**3. 微信绑定到已有账户**
```
POST /api/v1/auth/wechat/bind
Content-Type: application/json
Authorization: Bearer {temp_token}

Request:
{
  "student_id": "2020001",
  "password": "123456"
}

Response (成功):
{
  "code": 200,
  "message": "绑定成功",
  "data": {
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "user": {
      "id": 1,
      "student_id": "2020001",
      "name": "张三",
      "wechat_openid": "oXXXX"
    }
  }
}

Response (失败):
{
  "code": 400,
  "message": "绑定失败，请联系管理员"
}
```

**4. 设置密码（新用户）**
```
POST /api/v1/auth/password/setup
Content-Type: application/json
Authorization: Bearer {limited_token}

Request:
{
  "student_id": "2020001",
  "password": "NewPass123",
  "verification_code": "123456"
}

Response:
{
  "code": 200,
  "message": "密码设置成功",
  "data": {
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "user": {
      "id": 1,
      "student_id": "2020001",
      "name": "张三"
    }
  }
}
```

**5. 刷新Token**
```
POST /api/v1/auth/refresh
Authorization: Bearer {refresh_token}

Response:
{
  "code": 200,
  "message": "刷新成功",
  "data": {
    "access_token": "eyJhbGc...",
    "expires_in": 604800
  }
}
```

**6. 登出**
```
POST /api/v1/auth/logout
Authorization: Bearer {access_token}

Response:
{
  "code": 200,
  "message": "登出成功"
}
```

### 3.3 申请相关API

**1. 创建申请**
```
POST /api/v1/applications
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "planned_leave_date": "2026-06-15",
  "remarks": "毕业离校"
}

Response:
{
  "code": 201,
  "message": "创建成功",
  "data": {
    "id": 1,
    "status": "draft",
    "planned_leave_date": "2026-06-15",
    "created_at": "2026-05-27T10:00:00Z"
  }
}
```

**2. 获取申请列表**
```
GET /api/v1/applications?status=pending_counselor&page=1&page_size=20
Authorization: Bearer {access_token}

Response:
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 50,
    "page": 1,
    "page_size": 20,
    "items": [
      {
        "id": 1,
        "application_no": "LX202605270000001",
        "student_name": "张三",
        "status": "pending_counselor",
        "planned_leave_date": "2026-06-15",
        "submit_time": "2026-05-27T10:00:00Z"
      }
    ]
  }
}
```

**3. 获取申请详情**
```
GET /api/v1/applications/{id}
Authorization: Bearer {access_token}

Response:
{
  "code": 200,
  "data": {
    "id": 1,
    "application_no": "LX202605270000001",
    "student": {
      "id": 1,
      "student_id": "2020001",
      "name": "张三",
      "department": "计算机学院"
    },
    "status": "pending_counselor",
    "planned_leave_date": "2026-06-15",
    "submit_time": "2026-05-27T10:00:00Z",
    "attachments": [
      {
        "id": 1,
        "file_name": "宿舍清退证明.jpg",
        "attachment_type": "dorm_clearance"
      }
    ],
    "approvals": [
      {
        "approver_name": "李老师",
        "approver_role": "counselor",
        "action": "approve",
        "approval_time": "2026-05-27T14:00:00Z"
      }
    ]
  }
}
```

**4. 更新申请**
```
PUT /api/v1/applications/{id}
Authorization: Bearer {access_token}

Request:
{
  "planned_leave_date": "2026-06-20",
  "remarks": "延后离校"
}

Response:
{
  "code": 200,
  "message": "更新成功"
}
```

**5. 提交申请**
```
POST /api/v1/applications/{id}/submit
Authorization: Bearer {access_token}

Response:
{
  "code": 200,
  "message": "提交成功",
  "data": {
    "status": "pending_counselor",
    "submit_time": "2026-05-27T10:00:00Z"
  }
}
```

### 3.4 审批相关API

**1. 获取待审批列表**
```
GET /api/v1/approvals/pending?page=1&page_size=20
Authorization: Bearer {access_token}

Response:
{
  "code": 200,
  "data": {
    "total": 15,
    "items": [
      {
        "application_id": 1,
        "application_no": "LX202605270000001",
        "student_name": "张三",
        "planned_leave_date": "2026-06-15",
        "submit_time": "2026-05-27T10:00:00Z",
        "time_remaining": 20
      }
    ]
  }
}
```

**2. 审批通过**
```
POST /api/v1/approvals/{application_id}/approve
Authorization: Bearer {access_token}

Request:
{
  "opinion": "材料齐全，同意离校",
  "version": 0
}

Response (成功):
{
  "code": 200,
  "message": "审批成功",
  "data": {
    "status": "pending_admin",
    "next_approver": "学工部",
    "version": 1
  }
}

Response (版本冲突):
{
  "code": 409,
  "message": "申请已被修改，请刷新后重试",
  "data": {
    "current_version": 2
  }
}
```

**3. 审批驳回**
```
POST /api/v1/approvals/{application_id}/reject
Authorization: Bearer {access_token}

Request:
{
  "opinion": "宿舍清退证明不完整，请重新提交",
  "version": 0
}

Response (成功):
{
  "code": 200,
  "message": "已驳回",
  "data": {
    "status": "rejected",
    "version": 1
  }
}

Response (版本冲突):
{
  "code": 409,
  "message": "申请已被修改，请刷新后重试",
  "data": {
    "current_version": 2
  }
}
```

### 3.5 附件相关API

**1. 上传附件**
```
POST /api/v1/applications/{id}/attachments
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

Request:
- file: (binary)
- attachment_type: dorm_clearance

Response (成功):
{
  "code": 201,
  "message": "上传成功",
  "data": {
    "id": 1,
    "file_name": "宿舍清退证明.jpg",
    "file_size": 1024000,
    "file_hash": "a3b2c1d4e5f6...",
    "attachment_type": "dorm_clearance",
    "upload_time": "2026-05-27T10:00:00Z"
  }
}

Response (文件过大):
{
  "code": 400,
  "message": "文件大小超过10MB限制"
}

Response (文件类型不支持):
{
  "code": 400,
  "message": "不支持的文件类型，仅支持jpg、png、pdf、doc、docx"
}

Response (文件已存在):
{
  "code": 409,
  "message": "文件已存在",
  "data": {
    "existing_id": 123,
    "file_hash": "a3b2c1d4e5f6..."
  }
}

安全措施：
- MIME类型验证（python-magic）
- 文件名清理（防止路径遍历）
- SHA256哈希去重
- 大小限制：10MB
- 支持格式：jpg、png、pdf、doc、docx
```

**2. 下载附件**
```
GET /api/v1/attachments/{id}/download
Authorization: Bearer {access_token}

Response: (binary file stream)
```

**3. 删除附件**
```
DELETE /api/v1/attachments/{id}
Authorization: Bearer {access_token}

Response:
{
  "code": 204,
  "message": "删除成功"
}
```

### 3.6 通知相关API

**1. 获取通知列表**
```
GET /api/v1/notifications?is_read=false&page=1
Authorization: Bearer {access_token}

Response:
{
  "code": 200,
  "data": {
    "unread_count": 5,
    "items": [
      {
        "id": 1,
        "title": "申请已通过",
        "content": "您的离校申请已通过辅导员审核",
        "is_read": false,
        "created_at": "2026-05-27T14:00:00Z"
      }
    ]
  }
}
```

**2. 标记已读**
```
PUT /api/v1/notifications/{id}/read
Authorization: Bearer {access_token}

Response:
{
  "code": 200,
  "message": "已标记"
}
```

### 3.7 系统配置API（管理员）

**1. 获取配置**
```
GET /api/v1/configs?config_type=integration
Authorization: Bearer {admin_token}

Response:
{
  "code": 200,
  "data": [
    {
      "config_key": "dorm_integration_type",
      "config_value": "api",
      "description": "宿舍系统集成类型（api/database）"
    },
    {
      "config_key": "dorm_api_url",
      "config_value": "https://dorm.university.edu/api",
      "description": "宿舍系统API地址"
    },
    {
      "config_key": "dorm_api_key",
      "config_value": "***encrypted***",
      "description": "宿舍系统API密钥（加密存储）",
      "is_encrypted": true
    }
  ]
}
```

**2. 更新配置**
```
PUT /api/v1/configs/{key}
Authorization: Bearer {admin_token}

Request:
{
  "config_value": "https://dorm.new-university.edu/api"
}

Response:
{
  "code": 200,
  "message": "更新成功"
}
```

**配置类型说明：**
- `storage` - 文件存储配置
- `wechat` - 微信配置
- `notification` - 通知配置
- `workflow` - 流程配置
- `integration` - 外部系统集成配置（宿舍系统等）
- `security` - 安全配置

---
## 4. 认证授权设计

### 4.1 认证方式

**双通道认证：**
1. **学号+密码认证**
   - 学号作为唯一标识
   - 密码使用 bcrypt 加密存储
   - 支持密码重置（通过手机验证）

2. **微信OAuth2认证**
   - 获取微信授权code
   - 后端换取openid
   - openid绑定学号
   - 首次登录需绑定学号

**认证流程：**
```
学号密码登录：
用户输入学号+密码 → 后端验证 → 生成JWT Token → 返回Token

微信登录（安全增强）：
用户授权 → 获取code → 后端换取openid → 
├─ 已绑定：生成Token
└─ 未绑定：
   ├─ 学号已存在：
   │  ├─ 已绑定其他微信：返回通用错误（防止枚举）
   │  └─ 未绑定微信：要求密码验证 → 事务锁绑定 → 审计日志 → 生成Token
   └─ 学号不存在（新用户）：
      └─ 创建账户 → 强制设置密码 → 学生身份验证 → 生成受限Token
```

**安全增强（Round 1-3共识）：**
1. **学生身份验证**：微信新用户必须验证学生身份（短信/邮件/学生证照片）
2. **受限Token**：未完成密码设置的账户使用受限Token（scope: password_setup_only）
3. **事务锁**：微信绑定操作使用数据库锁（select_for_update）防止竞态
4. **审计日志**：所有绑定操作记录到audit_logs（action: wechat_bind）
5. **通用错误**：绑定失败统一返回"绑定失败，请联系管理员"（防止学号枚举）

### 4.2 JWT Token设计

**Token结构：**
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "user_id": 1,
    "student_id": "2020001",
    "role": "student",
    "exp": 1716768467,
    "iat": 1716163667
  },
  "signature": "..."
}
```

**Token类型：**
- **Access Token**：有效期7天，用于API访问
- **Refresh Token**：有效期30天，用于刷新Access Token
- **Limited Token**：有效期1小时，仅用于密码设置（scope: password_setup_only）

**Token存储：**
- 客户端：存储在本地安全存储（iOS Keychain/Android KeyStore）
- 小程序：存储在wx.storage
- Redis：存储Token黑名单（登出时加入）

### 4.3 权限模型（RBAC）

**角色定义：**
```
student（学生）
├─ 创建申请
├─ 查看自己的申请
├─ 修改草稿状态的申请
├─ 上传附件
└─ 查看通知

counselor（辅导员）
├─ 查看本年级所有申请
├─ 审批申请（通过/驳回）
├─ 查看审批历史
└─ 接收待办通知

admin（学工部管理员）
├─ 查看所有申请
├─ 最终备案审批
├─ 系统配置管理
├─ 用户管理
└─ 数据统计导出
```

**权限矩阵：**
```
资源/操作          | student | counselor | admin
-------------------|---------|-----------|-------
创建申请           | ✓       | ✗         | ✗
查看自己申请       | ✓       | ✗         | ✗
查看本年级申请     | ✗       | ✓         | ✗
查看所有申请       | ✗       | ✗         | ✓
辅导员审批         | ✗       | ✓         | ✗
学工部审批         | ✗       | ✗         | ✓
系统配置           | ✗       | ✗         | ✓
```

### 4.4 权限控制实现

**Django装饰器：**
```python
from functools import wraps
from rest_framework.exceptions import PermissionDenied

def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.user.role not in roles:
                raise PermissionDenied("无权限")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

# 使用
@role_required('counselor', 'admin')
def approve_application(request, application_id):
    pass
```

**DRF权限类：**
```python
from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'

class IsCounselor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'counselor'

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.student_id == request.user.id
```

---

## 5. 审批流程设计

### 5.1 流程状态机

**状态定义：**
```
draft（草稿）
  ↓ submit
pending_counselor（待辅导员审核）
  ↓ approve              ↓ reject
pending_admin        rejected（已驳回）
（待学工部备案）
  ↓ approve
approved（审批通过）
```

**状态转换规则：**
```python
STATE_TRANSITIONS = {
    'draft': ['pending_counselor'],  # 提交
    'pending_counselor': ['pending_admin', 'rejected'],  # 辅导员审批
    'pending_admin': ['approved', 'rejected'],  # 学工部审批
    'rejected': ['pending_counselor'],  # 重新提交
    'approved': []  # 终态
}
```

### 5.2 流程节点定义

**节点1：学生提交申请**
- 触发条件：学生填写完整信息并上传附件
- 前置校验：
  - 计划离校日期 ≥ 当前日期 + 3个工作日
  - 必须上传宿舍清退证明
  - 必须上传图书馆清书证明
  - 必须上传财务结清截图
- 执行动作：
  - 状态变更：draft → pending_counselor
  - 生成申请编号（LX{YYYYMMDD}{6位序号}）
  - 设置审批人：counselor_id（根据学生年级/班级分配）、admin_id（学工部负责人）
  - 设置当前审批人：current_approver_id = counselor_id
  - 初始化版本：version = 0
  - 记录提交时间：submit_time
  - 创建历史快照：applications_history（version=0, change_reason='提交申请'）
  - 记录审计日志：audit_logs（action='create_application', resource_type='application'）
  - 发送通知给辅导员
- 办理时限：无

**节点2：辅导员审核**
- 触发条件：申请状态为 pending_counselor
- 权限要求：辅导员角色 + current_approver_id匹配
- 执行动作：
  - 验证版本号（乐观锁）
  - 同意：
    - 状态变更 → pending_admin
    - 更新当前审批人：current_approver_id = admin_id
    - 递增版本：version += 1
    - 创建审批记录：approvals（approver_role='counselor', action='approve'）
    - 创建历史快照：applications_history（version=N, change_reason='辅导员审批通过'）
    - 记录审计日志：audit_logs（action='approve', resource_type='application'）
    - 通知学工部
  - 驳回：
    - 状态变更 → rejected
    - 清空当前审批人：current_approver_id = NULL
    - 递增版本：version += 1
    - 创建审批记录：approvals（approver_role='counselor', action='reject'）
    - 创建历史快照：applications_history（version=N, change_reason='辅导员驳回'）
    - 记录审计日志：audit_logs（action='reject', resource_type='application'）
    - 通知学生并说明原因
  - 记录审批意见和时间
- 办理时限：1个工作日（按工作时间9:00-17:00计算，排除周末和节假日）
- 超时处理：发送提醒通知

**节点3：学工部备案**
- 触发条件：申请状态为 pending_admin
- 权限要求：学工部管理员角色 + current_approver_id匹配
- 执行动作：
  - 验证版本号（乐观锁）
  - 同意：
    - 状态变更 → approved
    - 清空当前审批人：current_approver_id = NULL
    - 递增版本：version += 1
    - 生成电子离校凭证：certificate_url
    - 记录凭证生成时间：certificate_generated_at
    - 创建审批记录：approvals（approver_role='admin', action='approve'）
    - 创建历史快照：applications_history（version=N, change_reason='学工部备案通过'）
    - 记录审计日志：audit_logs（action='approve', resource_type='application'）
    - 归档申请全记录
    - 通知学生
  - 驳回：
    - 状态变更 → rejected
    - 清空当前审批人：current_approver_id = NULL
    - 递增版本：version += 1
    - 创建审批记录：approvals（approver_role='admin', action='reject'）
    - 创建历史快照：applications_history（version=N, change_reason='学工部驳回'）
    - 记录审计日志：audit_logs（action='reject', resource_type='application'）
    - 通知学生
  - 记录备案意见和时间
- 办理时限：1个工作日（按工作时间9:00-17:00计算，排除周末和节假日）
- 超时处理：发送提醒通知

**节点4：驳回后重新提交**
- 触发条件：申请状态为 rejected
- 执行动作：
  - 学生修改申请内容
  - 补充/更新附件
  - 重新提交 → pending_counselor
  - 流程重新开始

### 5.3 超时处理机制

**超时监控：**
```python
# Celery定时任务，每小时执行一次
from chinese_calendar import is_workday, get_workdays
from datetime import datetime, timedelta

@celery.task
def check_approval_timeout():
    # 查询待审批的申请
    pending_apps = Application.objects.filter(
        status__in=['pending_counselor', 'pending_admin'],
        is_deleted=False
    )
    
    for app in pending_apps:
        # 获取最新审批记录（当前节点）
        latest_approval = app.approvals.filter(
            approver_id=app.current_approver_id
        ).order_by('-created_at').first()
        
        if not latest_approval:
            # 新提交的申请，从submit_time开始计算
            start_time = app.submit_time
        else:
            # 已有审批记录，从上次审批时间开始计算
            start_time = latest_approval.approval_time
        
        # 计算工作日到期时间（1个工作日 = 8小时工作时间）
        due_time = calculate_due_time(start_time, work_hours=8)
        
        if datetime.now() > due_time:
            # 创建超时审批记录
            Approval.objects.create(
                application_id=app.id,
                approver_id=app.current_approver_id,
                approver_role=app.status.replace('pending_', ''),
                action='timeout',
                is_timeout=True,
                time_limit=8
            )
            # 发送提醒通知
            send_timeout_notification(app)

def calculate_due_time(start_time, work_hours=8):
    """
    计算工作日到期时间
    工作时间：9:00-17:00（8小时）
    排除周末和节假日
    """
    current = start_time
    remaining_hours = work_hours
    
    while remaining_hours > 0:
        # 跳过非工作日
        while not is_workday(current.date()):
            current += timedelta(days=1)
            current = current.replace(hour=9, minute=0, second=0)
        
        # 调整到工作时间内
        if current.hour < 9:
            current = current.replace(hour=9, minute=0, second=0)
        elif current.hour >= 17:
            current += timedelta(days=1)
            current = current.replace(hour=9, minute=0, second=0)
            continue
        
        # 计算当天剩余工作时间
        work_end = current.replace(hour=17, minute=0, second=0)
        hours_today = (work_end - current).total_seconds() / 3600
        
        if hours_today >= remaining_hours:
            # 当天可以完成
            current += timedelta(hours=remaining_hours)
            remaining_hours = 0
        else:
            # 需要跨天
            remaining_hours -= hours_today
            current += timedelta(days=1)
            current = current.replace(hour=9, minute=0, second=0)
    
    return current
```

**超时通知：**
- 第1次：办理时限到期时通知审批人
- 第2次：超时4小时后通知审批人上级
- 第3次：超时8小时后通知系统管理员

**降级策略：**
- 外部系统（宿舍管理系统）不可用时，允许手动上传证明文件
- 审批人可选择"跳过验证"并备注原因
- 系统记录降级操作日志

---
## 6. 外部系统集成设计

### 6.1 集成策略（Round 6共识）

**本项目数据库：** PostgreSQL（单一数据库）

**外部系统对接：** 支持多种数据库（MySQL/SQL Server/Oracle）

**集成方案优先级：**
1. **API集成（推荐）**：REST API对接，松耦合
2. **数据库直连（备选）**：SQLAlchemy只读访问，紧耦合
3. **避免**：Django多数据库（不适合外部系统）

### 6.2 宿舍管理系统对接

**集成目的：**
验证学生宿舍清退状态，确保离校手续真实完成。

**方案1：API集成（推荐）**

**接口协议：**
```
HTTP REST API
认证方式：API Key
数据格式：JSON
超时时间：5秒
```

**接口定义：**
```python
# 查询宿舍清退状态
GET /api/dorm/clearance/status
Headers:
  X-API-Key: {api_key}
Params:
  student_id: 2020001

Response:
{
  "code": 200,
  "data": {
    "student_id": "2020001",
    "is_cleared": true,
    "clearance_date": "2026-05-25",
    "room_no": "A101"
  }
}
```

**方案2：数据库直连（备选）**

**使用场景：** 外部系统无API且允许数据库访问

**安全要求：**
- 只读数据库用户
- 加密存储凭证（system_configs.is_encrypted=TRUE）
- 查询超时5秒
- 连接池最大5连接
- 所有查询记录audit_logs

### 6.3 接口实现

**方案1：API客户端（推荐）**
```python
# apps/integrations/dorm_system.py
class DormSystemClient:
    def __init__(self):
        config = SystemConfig.objects.get(config_key='dorm_api_url')
        self.base_url = config.config_value
        self.api_key = SystemConfig.objects.get(config_key='dorm_api_key').get_decrypted_value()
    
    def get_checkout_status(self, student_id):
        response = requests.get(
            f'{self.base_url}/api/students/{student_id}/checkout',
            headers={'X-API-Key': self.api_key},
            timeout=5
        )
        return response.json()
```

**方案2：SQLAlchemy数据库客户端（备选）**
```python
# apps/integrations/external_db.py
from sqlalchemy import create_engine, text
import json

class ExternalDatabaseClient:
    def __init__(self, system_name):
        config = SystemConfig.objects.get(config_key=f'{system_name}_db_config')
        db_config = json.loads(config.get_decrypted_value())
        
        # 构建连接字符串
        if db_config['type'] == 'mysql':
            conn_str = f"mysql+mysqldb://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        elif db_config['type'] == 'sqlserver':
            conn_str = f"mssql+pyodbc://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?driver=ODBC+Driver+17+for+SQL+Server"
        elif db_config['type'] == 'oracle':
            conn_str = f"oracle+cx_oracle://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['service_name']}"
        
        self.engine = create_engine(conn_str, pool_pre_ping=True, pool_size=5, max_overflow=0)
    
    def query(self, sql, params=None):
        with self.engine.connect() as conn:
            result = conn.execute(text(sql), params or {})
            return [dict(row) for row in result]

# 使用示例
class DormSystemClient:
    def __init__(self):
        integration_type = SystemConfig.objects.get(config_key='dorm_integration_type').config_value
        if integration_type == 'api':
            self.client = DormAPIClient()
        else:
            self.db = ExternalDatabaseClient('dorm_system')
    
    def get_checkout_status(self, student_id):
        if hasattr(self, 'client'):
            return self.client.get_checkout_status(student_id)
        else:
            sql = "SELECT is_checked_out, checkout_date FROM dorm_records WHERE student_id = :student_id"
            result = self.db.query(sql, {'student_id': student_id})
            return result[0] if result else None
```

### 6.4 配置存储

**system_configs配置项：**
```sql
-- API集成配置
INSERT INTO system_configs (config_key, config_value, config_type, is_encrypted) VALUES
('dorm_integration_type', 'api', 'integration', FALSE),
('dorm_api_url', 'https://dorm.university.edu/api', 'integration', FALSE),
('dorm_api_key', 'encrypted_key_here', 'integration', TRUE);

-- 数据库集成配置（备选）
INSERT INTO system_configs (config_key, config_value, config_type, is_encrypted) VALUES
('dorm_integration_type', 'database', 'integration', FALSE),
('dorm_db_config', '{"type":"mysql","host":"10.0.1.50","port":3306,"database":"dorm","user":"readonly","password":"encrypted"}', 'integration', TRUE);
```
        self.api_key = settings.DORM_SYSTEM_API_KEY
        self.api_secret = settings.DORM_SYSTEM_API_SECRET
    
    def verify_clearance(self, student_id):
        try:
            response = requests.get(
                f"{self.api_url}/clearance/status",
                params={"student_id": student_id},
                headers={
                    "X-API-Key": self.api_key,
                    "X-API-Secret": self.api_secret
                },
                timeout=5
            )
            return response.json()
        except requests.Timeout:
            raise ExternalSystemTimeout("宿舍系统超时")
        except Exception as e:
            raise ExternalSystemError(f"宿舍系统错误: {str(e)}")
```

### 6.3 错误处理和重试机制

**错误分类：**
```python
class ExternalSystemError(Exception):
    """外部系统基础异常"""
    pass

class ExternalSystemTimeout(ExternalSystemError):
    """超时异常 - 可重试"""
    pass

class ExternalSystemUnavailable(ExternalSystemError):
    """服务不可用 - 可重试"""
    pass

class ExternalSystemAuthError(ExternalSystemError):
    """认证失败 - 不可重试"""
    pass
```

**重试策略：**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),  # 最多重试3次
    wait=wait_exponential(multiplier=1, min=2, max=10),  # 指数退避
    retry=retry_if_exception_type((ExternalSystemTimeout, ExternalSystemUnavailable))
)
def verify_dorm_clearance(student_id):
    plugin = DormSystemPlugin()
    return plugin.verify_clearance(student_id)
```

**降级策略：**
- 外部系统不可用时，允许手动上传证明文件
- 审批人可选择"跳过验证"并备注原因
- 系统记录降级操作日志

---

## 7. 部署架构设计

### 7.1 Docker Compose配置

**服务清单：**
```yaml
services:
  nginx:          # 反向代理
  django-app:     # Django应用（单实例，Gunicorn 4 workers）
  postgres:       # PostgreSQL数据库
  redis:          # 缓存+消息队列
  celery-worker:  # 异步任务
  celery-beat:    # 定时任务
```

**网络架构：**
```
外部网络（公网）
    ↓
Nginx (80/443)
    ↓
内部网络（bridge）
    ├─ django-app:8000 (Gunicorn 4 workers)
    ├─ postgres:5432
    ├─ redis:6379
    ├─ celery-worker
    └─ celery-beat
```

**存储说明：**
- 文件存储：本地文件系统 `/data/uploads`
- MinIO：可选的未来扩展（不在基线部署中）

### 7.2 docker-compose.yml示例

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./static:/static
    depends_on:
      - django-app
    restart: always

  django-app:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    env_file:
      - .env
    depends_on:
      - postgres
      - redis
    restart: always

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: always

  celery-worker:
    build: .
    command: celery -A config worker -l info
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    env_file:
      - .env
    depends_on:
      - redis
      - postgres
    restart: always

  celery-beat:
    build: .
    command: celery -A config beat -l info
    env_file:
      - .env
    depends_on:
      - redis
    restart: always

volumes:
  postgres_data:
  redis_data:
```

**MinIO可选配置（未来扩展）：**
```yaml
# 如需MinIO对象存储，添加以下服务
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_PASSWORD}
    volumes:
      - minio_data:/data
    restart: always

# 并添加volume
volumes:
  minio_data:
```

### 7.3 数据持久化和备份

**持久化目录：**
```
/data/
├── postgres/     # PostgreSQL数据
├── redis/        # Redis数据
├── uploads/      # 上传文件
├── logs/         # 日志文件
└── backups/      # 备份文件
```

**备份策略：**
```bash
# 每日凌晨2点自动备份
0 2 * * * /scripts/backup.sh

# backup.sh
#!/bin/bash
DATE=$(date +%Y%m%d)

# PostgreSQL备份
docker exec postgres pg_dump -U ${DB_USER} ${DB_NAME} > /data/backups/db_${DATE}.sql

# 上传文件备份
tar -czf /data/backups/uploads_${DATE}.tar.gz /data/uploads

# 保留最近30天备份
find /data/backups -name "db_*.sql" -mtime +30 -delete
find /data/backups -name "uploads_*.tar.gz" -mtime +30 -delete
```

**恢复策略：**
```bash
# 恢复数据库
docker exec -i postgres psql -U ${DB_USER} ${DB_NAME} < /data/backups/db_YYYYMMDD.sql

# 恢复上传文件
tar -xzf /data/backups/uploads_YYYYMMDD.tar.gz -C /
```

---
## 8. 安全设计

### 8.1 数据安全

**敏感数据加密：**
- 密码：bcrypt加密存储（cost=12）
- 微信Secret：AES-256加密存储
- 数据库连接密码：环境变量+加密存储

**SQL注入防护：**
- 使用Django ORM参数化查询
- 禁止拼接SQL语句
- 输入参数严格校验

**XSS防护：**
- Django自动转义HTML
- DRF序列化器过滤输入
- CSP头部配置

**CSRF防护：**
- Django CSRF中间件
- API使用JWT Token，豁免CSRF
- 表单提交验证CSRF Token

### 8.2 传输安全

**HTTPS强制：**
```nginx
server {
    listen 80;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}
```

**API安全头：**
```python
SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### 8.3 认证安全

**密码策略：**
- 最小长度8位
- 必须包含字母+数字
- 密码错误5次锁定账户30分钟
- 密码有效期180天

**Token安全：**
- JWT签名算法：HS256
- Secret定期轮换
- Token黑名单机制
- 刷新Token单次使用

---

## 9. 性能优化设计

### 9.1 数据库优化

**索引策略：**
```sql
-- 高频查询字段索引
CREATE INDEX idx_student_id ON users(student_id);
CREATE INDEX idx_status ON applications(status);
CREATE INDEX idx_planned_leave_date ON applications(planned_leave_date);
CREATE INDEX idx_application_id ON approvals(application_id);

-- 复合索引
CREATE INDEX idx_status_submit_time ON applications(status, submit_time);
CREATE INDEX idx_user_read ON notifications(user_id, is_read);
```

**查询优化：**
- 使用select_related减少N+1查询
- 分页查询避免全表扫描
- 只查询需要的字段
- 避免在循环中查询数据库

**连接池配置：**
```python
DATABASES = {
    'default': {
        'CONN_MAX_AGE': 600,  # 连接复用10分钟
        'OPTIONS': {
            'MAX_CONNECTIONS': 100,
            'MIN_CONNECTIONS': 10
        }
    }
}
```

### 9.2 缓存策略

**Redis缓存层级：**
```python
# L1: 用户信息缓存（30分钟）
cache.set(f'user:{user_id}', user_data, 1800)

# L2: 申请状态缓存（5分钟）
cache.set(f'app:{app_id}:status', status, 300)

# L3: 待审批数量缓存（1分钟）
cache.set(f'pending:count:{user_id}', count, 60)
```

**缓存更新策略：**
- 写入时主动失效
- 定时刷新热点数据
- 缓存穿透：空值缓存
- 缓存雪崩：随机过期时间

**Django缓存配置：**
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 50}
        }
    }
}
```

### 9.3 异步处理

**Celery任务队列：**
```python
# 异步上传文件到存储
@celery.task
def upload_to_storage(file_path, attachment_id):
    # 上传逻辑
    pass

# 异步发送通知
@celery.task
def send_notification(user_id, message):
    # 发送微信通知
    pass

# 异步生成离校凭证
@celery.task
def generate_certificate(application_id):
    # 生成PDF
    pass
```

**任务优先级：**
- 高优先级：通知发送
- 中优先级：文件上传
- 低优先级：数据统计

### 9.4 前端优化

**React Native优化：**
- 图片懒加载
- 列表虚拟滚动
- 组件按需加载
- 本地缓存用户信息

**小程序优化：**
- 分包加载
- 图片压缩
- 请求合并
- setData优化

**网络优化：**
- API响应Gzip压缩
- 静态资源CDN加速（本地部署可选）
- 接口请求防抖节流

---

## 10. 测试策略

### 10.1 单元测试

**测试框架：**
- pytest + pytest-django
- 覆盖率目标：80%+

**测试范围：**
```python
# 模型测试
def test_application_status_transition():
    app = Application.objects.create(status='draft')
    app.submit()
    assert app.status == 'pending_counselor'

# 业务逻辑测试
def test_approval_workflow():
    result = approve_application(app_id, counselor_id, 'approve')
    assert result['status'] == 'pending_admin'

# API测试
def test_create_application_api(client):
    response = client.post('/api/v1/applications', data)
    assert response.status_code == 200
```

### 10.2 集成测试

**测试场景：**
- 完整审批流程测试
- 外部系统对接测试
- 文件上传下载测试
- 通知发送测试

**测试工具：**
- pytest-mock（模拟外部系统）
- factory_boy（测试数据工厂）

### 10.3 端到端测试

**测试工具：**
- Appium（移动端自动化）
- 微信开发者工具（小程序测试）

**测试用例：**
1. 学生提交申请完整流程
2. 辅导员审批流程
3. 学工部备案流程
4. 驳回后重新提交流程

### 10.4 性能测试

**测试工具：**
- Locust（压力测试）
- Apache JMeter

**测试指标：**
- 并发用户：1000+
- 响应时间：< 200ms（P95）
- 吞吐量：> 2000 QPS
- 错误率：< 0.1%

---

## 附录

### A. 部署清单

**环境要求：**
- Docker 20.10+
- Docker Compose 2.0+
- 服务器配置：4核8G内存（推荐）

**部署步骤：**
1. 克隆项目代码
2. 配置 `.env` 文件
3. 运行 `docker-compose up -d`
4. 访问管理后台初始化系统
5. 配置数据库连接
6. 配置微信公众号

### B. 运维监控

**监控指标：**
- 系统资源：CPU、内存、磁盘
- 应用性能：响应时间、吞吐量
- 业务指标：申请数量、审批时效
- 错误日志：异常统计、错误率

**告警策略：**
- CPU使用率 > 80%
- 内存使用率 > 85%
- 磁盘使用率 > 90%
- API错误率 > 1%
- 审批超时 > 10个

### C. 技术债务

**已知限制：**
1. 单体架构，高并发扩展受限（可通过水平扩展缓解）
2. 文件存储本地化，需定期清理（建议配置自动清理策略）
3. 微信通知依赖外部服务（需配置降级策略）

**未来优化方向：**
1. 引入消息队列解耦通知服务
2. 实现文件存储分层（热数据/冷数据）
3. 增加数据统计分析功能
4. 支持更多外部系统对接

---

**文档结束**

**版本历史：**
- v1.0 (2026-05-27): 初始版本，完成系统设计
