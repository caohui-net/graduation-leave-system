# 毕业离校系统 - 项目速查手册

**最后更新**: 2026-06-15 08:30

**⚠️ 强制规范**: 任何文件查找、路径定位、环境操作前，必须先查看本文档

---

## 1. 环境配置

### 系统环境
```bash
Python版本: 3.14.4
  - 命令: python3 (非容器环境)
  - 命令: python (Docker容器内)

Docker版本: 29.1.3
  - 命令: docker, docker-compose

操作系统: Ubuntu 26.04 LTS
```

### 后端 (Django)
```bash
框架: Django + Django REST Framework
路径: /home/caohui/projects/graduation-leave-system/backend
Python: 3.14.4 (需虚拟环境或Docker)
虚拟环境: backend/venv
端口: 7787 (宿主机) -> 8000 (容器内)

# 非Docker启动（开发）
cd backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:7787

# Docker启动（推荐）
docker-compose up -d backend
```

### 数据库 (PostgreSQL)
```bash
类型: PostgreSQL 15 (Docker容器)
容器名: graduation-leave-system-db-1
端口: 5432 (宿主机和容器)
数据库名: graduation_leave
用户: postgres
密码: postgres (配置在.env.docker)
数据卷: postgres_data

# 连接数据库
docker exec -it graduation-leave-system-db-1 psql -U postgres -d graduation_leave

# 检查容器状态
docker ps | grep graduation-leave-system
```

### 前端 (HTML静态)
```bash
路径: /home/caohui/projects/graduation-leave-system/demo-web
服务器: systemd --user + python3 -m http.server 7788
服务名: graduation-frontend.service
端口: 7788
入口: index.html (管理端)
移动端回调: mobile-sso-callback.html

# 守护进程管理（用户级systemd服务）
systemctl --user status graduation-frontend
systemctl --user start graduation-frontend
systemctl --user stop graduation-frontend
systemctl --user restart graduation-frontend

# 日志查看
journalctl --user -u graduation-frontend -f              # 实时日志
journalctl --user -u graduation-frontend -n 100          # 最近100行
journalctl --user -u graduation-frontend --since "1 hour ago"  # 指定时间

# 告警日志
cat /tmp/graduation-frontend-alerts.log

# 自动重启配置
# - 失败后10秒自动重启
# - 5分钟内失败≥5次则停止重启，需手动干预：
#   systemctl --user reset-failed graduation-frontend
#   systemctl --user start graduation-frontend

# 本机/内网/外网访问验证
curl --noproxy '*' http://127.0.0.1:7788/
curl --noproxy '*' http://172.17.12.199:7788/
curl --noproxy '*' http://218.75.196.218:7788/
```

### Docker容器状态
```bash
# 查看运行中的容器
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

当前运行容器：
- graduation-leave-system-backend-1  # Django后端，挂载 ./backend:/app
- graduation-leave-system-db-1       # PostgreSQL 15

# 容器内路径
后端应用: /app (挂载自宿主机 ./backend)
数据库数据: /var/lib/postgresql/data (卷 postgres_data)
媒体文件: /app/media (卷 media_data)

# 进入容器
docker exec -it graduation-leave-system-backend-1 bash
docker exec -it graduation-leave-system-db-1 psql -U postgres -d graduation_leave
```

### 关键URL
- 后端API: http://218.75.196.218:7787
- 前端页面: http://218.75.196.218:7788
- SSO回调: /api/sso/qingganlian/callback
- 移动端登录: /api/sso/qingganlian/mobile/login
- SAAS登录: /api/sso/qingganlian/mobile/saas-login
- 管理端登录: /api/sso/qingganlian/admin/login

---

## 2. 目录结构

```
graduation-leave-system/
├── backend/                    # Django后端
│   ├── apps/
│   │   ├── users/             # 用户模型和序列化器
│   │   │   ├── models.py      # User模型（user_id/name/role/building/room_number）
│   │   │   └── serializers.py # AuthUserSerializer
│   │   ├── sso_qingganlian/   # 青橄榄SSO集成
│   │   │   ├── views.py       # 登录接口（mobile_saas_login/mobile_login/admin_login）
│   │   │   ├── callback_views.py # HTML回调处理器
│   │   │   ├── serializers.py # UserInfoSerializer
│   │   │   ├── client.py      # 青橄榄API客户端
│   │   │   ├── settings.py    # SSO配置（含QGL_VERIFY_ADMIN_TOKEN开关）
│   │   │   └── README_SECURITY.md # 安全配置说明
│   │   ├── approvals/         # 审批流程
│   │   │   └── views.py       # 审批接口（含详细错误日志）
│   │   ├── applications/      # 申请管理
│   │   └── middleware/        # 中间件
│   │       ├── error_logging.py   # 全局错误日志中间件
│   │       └── README.md      # 中间件说明
│   ├── venv/                  # Python虚拟环境
│   └── manage.py
├── demo-web/                   # 前端静态页面
│   ├── index.html             # 管理端UI（含审批列表过滤逻辑）
│   └── mobile-sso-callback.html # 移动端SSO回调页面
├── docs/                       # 文档和截图
└── PROJECT-QUICK-REF.md       # 本文件

重要配置文件：
- backend/apps/sso_qingganlian/settings.py - SSO配置
- backend/.env (如果存在) - 环境变量
```

---

## 3. 日志配置（2026-06-15新增）

### 日志文件位置
```bash
主日志: /tmp/backend.log
其他日志: /tmp/backend-*.log
```

### 已覆盖的日志记录
- ✅ SSO登录成功/失败/未授权（logger.info/logger.warning/logger.exception）
- ✅ 批量审批错误（详细记录失败approval_id和原因）
- ✅ 审批导出失败
- ✅ 未捕获异常（通过ErrorLoggingMiddleware自动记录）

### 查看日志
```bash
# 实时监控
tail -f /tmp/backend.log

# 查找批量审批错误
grep "Batch action rejected" /tmp/backend.log

# 查找未授权登录
grep "login rejected" /tmp/backend.log

# 查找未捕获异常
grep "Unhandled exception" /tmp/backend.log
```

### 中间件启用（需手动配置）
编辑Django settings.py，在MIDDLEWARE列表添加：
```python
'apps.middleware.ErrorLoggingMiddleware',
```

---

## 5. 环境变量

### SSO配置
```bash
# 青橄榄移动端
QGL_MOBILE_APP_KEY=cb6f276a42042179e90cd79c4126e075
QGL_MOBILE_APP_SECRET=da02720febcf47071ee5db78c2b068ec
QGL_MOBILE_TENANT_CODE=S10405
QGL_MOBILE_APPID=8uonta

# 青橄榄管理端
QGL_ADMIN_APP_KEY=APPKEY_TBD
QGL_ADMIN_APP_SECRET=APPSECRET_TBD

# 安全开关（默认true）
QGL_VERIFY_ADMIN_TOKEN=true  # false时跳过admin token验证
```

---

## 6. 数据库状态

### 数据库类型
- **PostgreSQL 15** (Docker容器运行)
- 连接信息见"环境配置"章节

### 角色数据完整性（2026-06-15验证）
**有效角色（UserRole枚举）**: student, dorm_manager, counselor, dean, admin

**当前分布**:
- student: 6001
- dorm_manager: 76
- counselor: 24
- admin: 18
- dean: 2

**验证命令**:
```bash
# 检查无效角色（应返回0行）
docker exec graduation-leave-system-db-1 psql -U postgres -d graduation_leave -c \
  "SELECT role, COUNT(*) FROM users WHERE role NOT IN ('student','dorm_manager','counselor','dean','admin') GROUP BY role;"
```

### 用户表关键字段
```python
User模型字段：
- user_id (CharField, 主键) - 学号/工号
- name (CharField) - 姓名
- role (CharField) - student/teacher/admin
- class_id (CharField, nullable)
- phone (CharField, nullable)
- building (CharField, nullable) - 宿舍楼
- room_number (CharField, nullable) - 房间号
- is_staff (BooleanField)
- active (BooleanField)
```

### 数据统计（2026-06-11）
- 总用户数：6081
- building为NULL：28人（0.5%）
- room_number为NULL：269人（4.4%）

---

## 7. 部署信息

### Docker部署（推荐）
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
docker ps | grep graduation-leave-system

# 重启后端（代码更新后）
docker-compose restart backend

# 查看后端日志
docker-compose logs -f backend

# 停止所有服务
docker-compose down

# 完全清理（包含数据卷）
docker-compose down -v
```

### 后端服务（非Docker）
```bash
# 检查运行状态
pgrep -f "manage.py runserver"

# 启动后端
cd backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:7787

# 重启后端
pkill -f "manage.py runserver"
nohup python manage.py runserver 0.0.0.0:7787 > /tmp/backend.log 2>&1 &
```

### 前端服务
```bash
# 检查dufs状态
pgrep -f "dufs"

# 启动前端（需确认端口和命令）
cd demo-web
dufs -p 7788 --allow-all
```

---

## 8. 最近修改记录

### 2026-06-16 前端内网访问无响应修复
**问题**: 外部 `http://218.75.196.218:7788` 正常，但本机内网 `http://172.17.12.199:7788` 无响应。

**根因**: `scripts/serve-frontend.py` 使用单线程 `HTTPServer`，慢连接占用唯一请求处理线程，导致后续本机/内网请求排队超时。

**修复**: `scripts/serve-frontend.py` 改用 `ThreadingHTTPServer as HTTPServer`，保留原 Cache-Control 逻辑。

**验证**:
- `pytest tests/test_serve_frontend.py -q` → `1 passed`
- `http://127.0.0.1:7788/` → 200
- `http://172.17.12.199:7788/` → 200
- `http://218.75.196.218:7788/` → 200
- 慢连接并发探针 → 正常请求 0.008s 返回 200

### 2026-06-15 数据修复与验证：teacher角色清理
**问题**: 5个用户角色为"teacher"（无效角色，UserRole枚举无此值）
- 92020050 许芸 (兰园10栋)
- 92023035 贺春红 (紫园8栋)
- 92019517 王春兰 (紫园6栋)
- 92023027 孙慧 (兰园4栋)
- 92022002 罗继莲 (柳园1栋)

**修复**: `UPDATE users SET role='dorm_manager' WHERE role='teacher';`

**根因**: 数据导入时角色映射错误，teacher应为dorm_manager

**验证**: 已对照原始Excel文档核实
- ✅ 辅导员数据（20条）：职工号、姓名完全匹配
- ✅ 宿管员数据（76条）：职工号、姓名、楼栋号完全匹配
- ✅ 无数据差异

**教训**: 
- ❌ 错误：AI回复"已无teacher角色"但实际未检查数据库
- ✅ 正确：任何数据声明必须先查询验证
- ⚠️ 强制：role字段只能是 student/dorm_manager/counselor/dean/admin

**验证SQL**:
```sql
-- 检查无效角色
SELECT role, COUNT(*) FROM users 
WHERE role NOT IN ('student','dorm_manager','counselor','dean','admin') 
GROUP BY role;

-- 角色分布（当前：student=6001, dorm_manager=76, counselor=24, admin=18, dean=2）
SELECT role, COUNT(*) FROM users GROUP BY role ORDER BY COUNT(*) DESC;
```

### 2026-06-15 批量审批修复和日志增强
- **commit a7ce238** - 前端：审批列表过滤非当前用户审批（修复批量操作误选问题）
- **commit 68d6ae0** - 后端：批量审批错误详细日志（记录失败approval_id）
- **commit be3852c** - 中间件：全局错误日志（捕获所有未处理异常）

### 2026-06-11 SSO token验证开关
- 添加QGL_VERIFY_ADMIN_TOKEN环境变量控制admin_login验证
- 默认开启，对接失败可临时关闭
- 文档：README_SECURITY.md

### commit 2a7f976 - Codex/Gemini审查修复
- [严重] admin_login添加token验证（可开关控制）
- [中等] mobile_login添加安全说明
- [中等] callback端点添加building/room_number字段
- [轻微] UserInfoSerializer id类型改为CharField

### commit e1cf285 - 修复登录卡死问题
- AuthUserSerializer添加building/room_number字段
- 3个SSO登录接口响应添加这两字段
- UserInfoSerializer添加字段定义

---

## 9. 常用命令

### 开发（Docker环境）
```bash
# 进入后端容器
docker exec -it graduation-leave-system-backend-1 bash

# 容器内执行Django命令
docker exec -it graduation-leave-system-backend-1 python manage.py shell
docker exec -it graduation-leave-system-backend-1 python manage.py migrate
docker exec -it graduation-leave-system-backend-1 python manage.py createsuperuser

# 数据库操作
docker exec -it graduation-leave-system-db-1 psql -U postgres -d graduation_leave

# 查看用户数
docker exec -it graduation-leave-system-db-1 psql -U postgres -d graduation_leave -c "SELECT COUNT(*) FROM users_user;"
```

### 开发（非Docker环境）
```bash
# 激活后端环境
cd backend && source venv/bin/activate

# 数据库操作
python manage.py shell

# 查看用户
python manage.py shell -c "from apps.users.models import User; print(User.objects.count())"

# 查看SSO映射
python manage.py shell -c "from apps.sso_qingganlian.models import SSOUserMapping; print(SSOUserMapping.objects.count())"
```

### 测试
```bash
# 测试移动端登录
curl -X POST http://127.0.0.1:7787/api/sso/qingganlian/mobile/login \
  -H "Content-Type: application/json" \
  -d '{"authorization":"test","user_id":"19970545","real_name":"测试","identity_name":"学生"}'

# 测试管理端登录
curl -X POST http://127.0.0.1:7787/api/sso/qingganlian/admin/login \
  -H "Content-Type: application/json" \
  -d '{"authorization":"test","username":"admin001"}'
```

### Git
```bash
# 查看状态
git status

# 最近提交
git log --oneline -5

# 推送
git push
```

---

## 10. 故障排查

### 用户登录卡死
- 检查：AuthUserSerializer和SSO接口响应字段是否一致
- 解决：确保所有登录接口返回完整用户字段（包括building/room_number）

### 管理端对接失败
- 检查：QGL_VERIFY_ADMIN_TOKEN配置
- 临时解决：设置QGL_VERIFY_ADMIN_TOKEN=false
- 日志：查看backend日志中token验证失败原因

### 后端无法启动
- 检查：虚拟环境是否激活
- 检查：端口7787是否被占用
- 日志：查看/tmp/backend.log

---

## 11. 安全注意事项

⚠️ **生产部署必读**

1. **SSO端点访问控制**
   - mobile_login/admin_login信任青橄榄已认证
   - 建议nginx/防火墙限制只允许青橄榄IP访问

2. **token验证开关**
   - QGL_VERIFY_ADMIN_TOKEN默认true（推荐）
   - 仅对接调试时临时设为false
   - 验证关闭会有认证绕过风险

3. **敏感信息**
   - building/room_number非高度敏感但属隐私信息
   - 仅通过认证后的接口返回

---

## 12. OpenWolf集成

- `.wolf/anatomy.md` - 文件结构和token估算
- `.wolf/cerebrum.md` - 项目知识和最佳实践
- `.wolf/memory.md` - 操作日志
- `.omc/project-memory.json` - 项目记忆
- `.omc/session-context.json` - session上下文

---

**使用建议**: Session开始时先读取本文件，避免重复查找配置
