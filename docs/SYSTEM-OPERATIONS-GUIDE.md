# 毕业生离校申请审批系统 - 操作指南

**版本：** v1.0  
**更新日期：** 2026-06-07  
**状态：** 生产就绪

---

## 系统概述

毕业生离校申请审批系统是一个基于Django的Web应用，支持学生在线提交离校申请，宿管员和辅导员两级审批。

**核心功能：**
- 学生提交离校申请
- 宿管员审批（楼栋内任意宿管员可审批）
- 辅导员审批（按学院匹配）
- 申请状态查询
- 审批记录追踪

**技术栈：**
- 后端：Django 4.2 + Django REST Framework
- 数据库：PostgreSQL 15
- 认证：JWT (SimpleJWT)
- 部署：Docker Compose

---

## 快速开始

### 1. 环境要求

- Docker 20.10+
- Docker Compose 2.0+
- 8GB+ RAM
- 10GB+ 磁盘空间

### 2. 部署步骤

```bash
# 1. 克隆代码
cd /home/caohui/projects/graduation-leave-system

# 2. 启动服务
docker compose up -d

# 3. 等待服务健康检查通过
docker compose ps

# 4. 初始化数据库
docker compose exec backend python manage.py migrate

# 5. 加载测试数据
docker compose exec backend python manage.py seed_data
```

### 3. 验证部署

```bash
# 测试API可访问性
curl http://localhost:8001/api/auth/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2020001","password":"2020001"}'

# 预期返回：JWT token
```

**访问地址：**
- 后端API：http://localhost:8001
- 数据库：localhost:5432

---

## 数据初始化

### 加载测试数据

```bash
# 加载种子数据（包含测试用户）
docker compose exec backend python manage.py seed_data

# 重置数据库（清空申请和审批记录）
docker compose exec backend python manage.py seed_data --reset
```

### 测试账号

**学生账号：**
- 2020001 / 2020001（张三，1号楼，计算机学院）
- 2020002 / 2020002（李四，2号楼，软件学院）

**宿管员账号：**
- M001 / M001（宿管员1，1号楼）
- M002 / M002（宿管员2，2号楼）
- M003 / M003（宿管员3，1号楼）

**辅导员账号：**
- T001 / T001（李老师，计算机学院）
- T002 / T002（王老师，软件学院）

**学工部账号：**
- D001 / D001（赵主任）

---

## 用户操作流程

### 学生操作

**1. 登录系统**
```bash
POST /api/auth/login
{
  "user_id": "2020001",
  "password": "2020001"
}
```

**2. 提交离校申请**
```bash
POST /api/applications/
Authorization: Bearer <access_token>
{
  "reason": "已完成毕业手续",
  "leave_date": "2024-07-01"
}
```

**3. 查询申请状态**
```bash
GET /api/applications/
Authorization: Bearer <access_token>
```

**4. 查看申请详情**
```bash
GET /api/applications/{application_id}/
Authorization: Bearer <access_token>
```

### 宿管员操作

**1. 登录系统**
```bash
POST /api/auth/login
{
  "user_id": "M001",
  "password": "M001"
}
```

**2. 查看待审批列表**
```bash
GET /api/approvals/?decision=pending
Authorization: Bearer <access_token>
```

**3. 审批通过**
```bash
POST /api/approvals/{approval_id}/approve/
Authorization: Bearer <access_token>
{
  "comment": "同意离校"
}
```

**4. 审批驳回**
```bash
POST /api/approvals/{approval_id}/reject/
Authorization: Bearer <access_token>
{
  "comment": "宿舍物品未清理完毕"
}
```

### 辅导员操作

**1. 登录系统**
```bash
POST /api/auth/login
{
  "user_id": "T001",
  "password": "T001"
}
```

**2. 查看待审批列表**
```bash
GET /api/approvals/?decision=pending
Authorization: Bearer <access_token>
```

**3. 审批操作**
```bash
# 通过
POST /api/approvals/{approval_id}/approve/
Authorization: Bearer <access_token>
{
  "comment": "同意"
}

# 驳回
POST /api/approvals/{approval_id}/reject/
Authorization: Bearer <access_token>
{
  "comment": "档案未归还"
}
```

---

## API参考

### 认证接口

**登录**
- **端点：** `POST /api/auth/login`
- **请求：** `{"user_id": "string", "password": "string"}`
- **响应：** `{"access_token": "string", "refresh_token": "string", "user": {...}}`

### 申请接口

**提交申请**
- **端点：** `POST /api/applications/`
- **认证：** Bearer Token
- **请求：** `{"reason": "string", "leave_date": "YYYY-MM-DD"}`
- **响应：** `{"application_id": "string", "status": "pending_dorm_manager", ...}`

**查询申请列表**
- **端点：** `GET /api/applications/`
- **认证：** Bearer Token
- **参数：** `?status=pending_dorm_manager|pending_counselor|approved|rejected&limit=20&offset=0`

**查询申请详情**
- **端点：** `GET /api/applications/{application_id}/`
- **认证：** Bearer Token
- **响应：** 包含申请信息和审批记录

### 审批接口

**查询审批列表**
- **端点：** `GET /api/approvals/`
- **认证：** Bearer Token
- **参数：** `?decision=pending|approved|rejected|all&limit=20&offset=0`

**查询审批详情**
- **端点：** `GET /api/approvals/{approval_id}/`
- **认证：** Bearer Token

**审批通过**
- **端点：** `POST /api/approvals/{approval_id}/approve/`
- **认证：** Bearer Token
- **请求：** `{"comment": "string"}`

**审批驳回**
- **端点：** `POST /api/approvals/{approval_id}/reject/`
- **认证：** Bearer Token
- **请求：** `{"comment": "string"}`

---

## 审批流程说明

### 标准流程

```
学生提交申请
    ↓
宿管员审批（楼栋内任意宿管员可审批）
    ↓
辅导员审批（按学院自动路由）
    ↓
申请完成（状态：approved）
```

### 状态转换

- **pending_dorm_manager** - 等待宿管员审批
- **pending_counselor** - 等待辅导员审批
- **approved** - 已通过
- **rejected** - 已驳回

### 多宿管员协同审批

当学生所在楼栋有多个宿管员时：
1. 系统为所有宿管员创建审批任务
2. 任意一个宿管员审批通过后
3. 其他宿管员的审批自动完成（显示"已由XX完成审批"）

---

## 配置说明

### 环境变量（.env.docker）

```bash
# 数据库配置
DB_ENGINE=django.db.backends.postgresql
DB_NAME=graduation_leave
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Django配置
SECRET_KEY=<生产环境需更换>
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# JWT配置
JWT_SECRET_KEY=<生产环境需更换>
JWT_ACCESS_TOKEN_LIFETIME=3600
JWT_REFRESH_TOKEN_LIFETIME=86400
```

### 生产环境注意事项

**安全配置：**
1. 更换SECRET_KEY和JWT_SECRET_KEY为随机字符串
2. 设置DEBUG=False
3. 配置ALLOWED_HOSTS为实际域名
4. 使用强密码（数据库、用户账号）

**性能优化：**
1. 配置数据库连接池
2. 启用静态文件缓存
3. 配置反向代理（Nginx）
4. 启用HTTPS

---

## 故障排查

### 服务启动失败

**问题：** `docker compose up -d` 失败

**排查步骤：**
```bash
# 查看服务状态
docker compose ps

# 查看日志
docker compose logs backend
docker compose logs db

# 重启服务
docker compose restart

# 完全重建
docker compose down
docker compose up -d --build
```

### 数据库连接失败

**问题：** Backend无法连接数据库

**排查步骤：**
```bash
# 检查数据库健康状态
docker compose ps db

# 测试数据库连接
docker compose exec db psql -U postgres -d graduation_leave -c "SELECT 1;"

# 检查环境变量
docker compose exec backend env | grep DB_
```

### API返回401错误

**问题：** JWT认证失败

**原因：**
- Token过期（默认1小时）
- Token格式错误
- 未携带Authorization header

**解决方案：**
```bash
# 重新登录获取新token
curl http://localhost:8001/api/auth/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2020001","password":"2020001"}'

# 确保请求header正确
Authorization: Bearer <access_token>
```

### API返回403错误

**问题：** 权限不足

**原因：**
- 学生访问审批接口
- 宿管员/辅导员访问非本人审批
- 跨权限访问

**解决方案：**
- 确认用户角色和权限
- 使用正确的账号登录
- 检查审批记录的approver_id

### API返回409错误

**问题：** 冲突错误

**常见情况：**
1. 重复提交申请（学生已有待审批或已通过的申请）
2. 重复审批（审批记录已完成）
3. 状态不匹配（申请状态与审批步骤不符）

**解决方案：**
```bash
# 查询当前申请状态
GET /api/applications/{application_id}/

# 重置测试数据
docker compose exec backend python manage.py seed_data --reset
```

---

## 日常运维

### 查看日志

```bash
# 实时查看backend日志
docker compose logs -f backend

# 查看最近50行日志
docker compose logs backend --tail 50

# 查看数据库日志
docker compose logs db
```

### 数据库备份

```bash
# 备份数据库
docker compose exec db pg_dump -U postgres graduation_leave > backup.sql

# 恢复数据库
docker compose exec -T db psql -U postgres graduation_leave < backup.sql
```

### 更新部署

```bash
# 拉取最新代码
git pull

# 重建并启动服务
docker compose up -d --build

# 执行数据库迁移
docker compose exec backend python manage.py migrate

# 验证服务运行
docker compose ps
```

### 停止服务

```bash
# 停止服务（保留数据）
docker compose stop

# 停止并删除容器（保留数据卷）
docker compose down

# 停止并删除所有数据
docker compose down -v
```

---

## 测试验证

### 运行单元测试

```bash
# 运行所有测试
docker compose exec backend python manage.py test

# 运行特定应用测试
docker compose exec backend python manage.py test apps.applications
docker compose exec backend python manage.py test apps.approvals
```

### 运行Smoke测试

```bash
# 完整审批流程测试
bash tests/smoke_test.sh

# 多宿管员测试
bash tests/test_multi_dorm_manager.sh
```

### API测试脚本

参考 `tests/` 目录下的测试脚本：
- `smoke_test.sh` - 端到端审批流程测试
- `test_multi_dorm_manager.sh` - 多宿管员协同审批测试

---

## 技术支持

**文档目录：**
- 系统设计：`docs/design/2026-05-27-system-design.md`
- 项目总结：`docs/PROJECT-SUMMARY.md`
- API示例：`docs/API-DATA-EXAMPLES.md`
- Codex审查流程：`docs/codex-review-protocol.md`

**常用命令：**
```bash
# Django管理
docker compose exec backend python manage.py --help

# 数据库管理
docker compose exec db psql -U postgres graduation_leave

# 容器管理
docker compose ps
docker compose logs
docker compose restart
docker compose down
```

---

**版本历史：**
- v1.0 (2026-06-07): 初始版本，Docker部署就绪
