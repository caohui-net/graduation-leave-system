# 项目速查手册

**项目**: 毕业生离校申请审批系统  
**状态**: ✅ 生产就绪 + 治理增强  
**更新**: 2026-06-27

> **速查原则**: 遇到问题先查此文档，避免试错。所有命令已验证可执行。

**相关文档**: [DESIGN.md](DESIGN.md) 前端设计规范 | [README.md](README.md) 项目总览 | [CHANGELOG.md](CHANGELOG.md) 变更记录

---

## 📌 关键信息速查

### 项目路径
```bash
PROJECT_ROOT=/home/caohui/projects/graduation-leave-system
```

### Python环境
```bash
# ✅ 正确方式
backend/venv/bin/python3 manage.py <command>

# 或激活venv
cd backend && source venv/bin/activate
python manage.py <command>

# ❌ 错误方式
python manage.py <command>    # 找不到python
python3 manage.py <command>   # 系统Python无Django
```

### Django版本
```bash
backend/venv/bin/python3 -m django --version
# 输出: 5.0
```

---

## 🔌 端口与服务

| 服务 | 端口 | 启动命令 |
|------|------|----------|
| 后端API | 8000 | `cd backend && source venv/bin/activate && python manage.py runserver 0.0.0.0:8000` |
| 前端开发 | 5173 | `cd frontend && npm run dev` |
| 前端生产 | 7788 | `python scripts/serve-frontend.py` |
| PostgreSQL | 5432 | `systemctl status postgresql` |
| Redis | 6379 | `systemctl status redis` (可选) |

### 服务健康检查
```bash
# 后端API
curl http://localhost:8000/api/health

# 前端
curl http://localhost:7788

# 数据库
psql -h localhost -U postgres -d graduation_dev -c "SELECT 1"
```

---

## 🗄️ 数据库操作

### 连接数据库
```bash
# 基本连接
psql -h localhost -U postgres -d graduation_dev

# 带密码
PGPASSWORD=yourpass psql -h localhost -U postgres -d graduation_dev

# 使用环境变量
psql -h $DB_HOST -U $DB_USER -d $DB_NAME
```

### Django Migration
```bash
cd backend && source venv/bin/activate

# 查看状态
python manage.py showmigrations

# 创建migration
python manage.py makemigrations

# 应用migration
python manage.py migrate

# 检查未应用migrations
./scripts/check-migrations.sh

# 检查Schema漂移
./scripts/check-schema-drift.sh
```

### 数据导入
```bash
cd backend && source venv/bin/activate

# 按顺序导入（固定顺序）
python manage.py import_staff --counselors data/counselors_processed.csv
python manage.py import_staff --dorm-managers data/dorm_managers_processed.csv
python manage.py import_students data/file5_students_merged_v2.csv
```

### 数据统计
- 总用户: 6,041
- 学生: 5,946 (is_graduating=True)
- 宿管员: 72
- 辅导员: 20
- 管理员: 3

---

## 📁 目录结构速查

```
graduation-leave-system/
├── backend/                    # Django后端
│   ├── venv/                  # 虚拟环境 (Python 3.14 + Django 5.0)
│   ├── apps/
│   │   ├── users/             # 用户模块
│   │   └── applications/      # 申请模块
│   ├── config/                # Django配置
│   ├── data/                  # 数据导入文件
│   ├── scripts/               # 后端脚本
│   │   ├── check-migrations.sh
│   │   ├── check-schema-drift.sh
│   │   └── validate-config.py
│   └── manage.py
├── frontend/                   # React前端
│   ├── src/
│   └── dist/                  # 构建产物
├── docs/                       # 项目文档
│   ├── 环境执行规范速查.md
│   ├── 数据速查.md
│   ├── 部署检查清单.md
│   └── INDEX.md               # 文档索引
├── scripts/                    # 项目级脚本
│   ├── validate-deployment.sh
│   └── setup-monitoring.sh
└── .github/workflows/         # CI/CD
    └── deployment-check.yml
```

---

## ⚙️ 环境变量速查

### 必需变量
```bash
# 数据库
export DB_HOST=localhost
export DB_NAME=graduation_dev
export DB_USER=postgres
export DB_PASSWORD=yourpassword
export DB_PORT=5432

# Django
export SECRET_KEY=your-secret-key-min-50-chars
export DEBUG=false
export ALLOWED_HOSTS=localhost,127.0.0.1

# 环境标识
export DJANGO_ENV=dev  # dev/staging/production
```

### 可选变量
```bash
# SSO
export SSO_ENABLED=false
export SSO_QGL_APP_ID=
export SSO_QGL_APP_SECRET=

# XG-API
export XG_API_ENABLED=false
export XG_API_BASE_URL=
export XG_API_TIMEOUT=8
```

### 配置验证
```bash
cd backend
python scripts/validate-config.py .env.production
```

---

## 🚀 常用命令速查

### 启动服务
```bash
# 后端
cd backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000

# 前端开发
cd frontend
npm run dev

# 前端生产
python scripts/serve-frontend.py
```

### 代码检查
```bash
# Migration检查
cd backend && ./scripts/check-migrations.sh

# Schema漂移检测
cd backend && ./scripts/check-schema-drift.sh

# 配置验证
cd backend && python scripts/validate-config.py .env.dev

# 部署验证（项目根目录）
./scripts/validate-deployment.sh
```

### Git操作
```bash
# 查看状态
git status

# 提交代码
git add .
git commit -m "feat: description"
git push

# 查看最近提交
git log --oneline -10
```

---

## 🔧 故障排查速查

### 问题1: command not found
```bash
# 现象
bash: python: command not found

# 原因：系统无python命令，只有python3

# 解决
使用 python3 或 backend/venv/bin/python3
```

### 问题2: No module named 'django'
```bash
# 现象
ImportError: Couldn't import Django

# 原因：使用了系统Python，Django在venv中

# 解决
backend/venv/bin/python3 manage.py <command>
# 或
cd backend && source venv/bin/activate
```

### 问题3: Migration冲突
```bash
# 现象
NodeNotFoundError: Migration dependencies reference nonexistent parent node

# 原因：migration依赖指向不存在的父migration

# 解决
1. 查看实际migration文件: ls backend/apps/users/migrations/00*.py
2. 修正dependencies指向正确的父migration
3. 检查是否有重复编号的migration文件
```

### 问题4: 学生提交申请时返回500错误（草稿创建失败）
```bash
# 现象
POST /api/applications/draft/ 返回500 Internal Server Error
浏览器控制台: IntegrityError: null value in column "class_id"

# 原因
1. 前端：登录后未保存JWT token到localStorage
2. 数据库：部分用户class_id为null，但表约束NOT NULL

# 解决（已修复 - 2026-06-30）
1. 数据库已更新：class_id改为nullable（向后兼容）
2. 前端已修复：登录时保存token到localStorage
3. 如需回滚：执行 backups/rollback_20260630.sql

# 验证
localStorage.getItem('token')  # 应返回JWT token，不是'undefined'
```

### 问题5: 数据库连接失败
```bash
# 现象
psql: could not connect to server

# 检查
systemctl status postgresql  # 检查服务状态
echo $DB_HOST $DB_NAME       # 检查环境变量
psql -h localhost -U postgres -c "SELECT 1"  # 测试连接
```

### 问题5: 前端无响应
```bash
# 现象
curl http://localhost:7788 超时

# 检查
ps aux | grep serve-frontend  # 检查进程
netstat -tuln | grep 7788     # 检查端口
pkill -f serve-frontend.py    # 重启服务
python scripts/serve-frontend.py
```

### 问题6: 登录后会话丢失（HTTP环境）
```bash
# 现象
登录成功但刷新后回到登录页，浏览器控制台显示cookies未设置

# 原因
prod.py配置了SESSION_COOKIE_SECURE=True，要求HTTPS，但内网使用HTTP

# 解决
在.env中添加: FORCE_HTTPS=False
重启服务: pkill -f gunicorn && gunicorn config.wsgi:application --bind 0.0.0.0:7788

# 详见: docs/HTTP-DEPLOYMENT-FIX.md
```

---

## 📋 执行检查清单

### 开始工作前
- [ ] 确认项目目录: `pwd` 
- [ ] 确认venv存在: `ls backend/venv/bin/python3`
- [ ] 确认Django可用: `backend/venv/bin/python3 -m django --version`

### Django操作前
- [ ] 在backend目录或使用完整路径
- [ ] 使用venv Python或激活venv
- [ ] 环境变量已设置

### 数据库操作前
- [ ] PostgreSQL服务运行中
- [ ] 环境变量已设置: `echo $DB_HOST`
- [ ] 连接测试通过

### 部署前
- [ ] Migration检查通过
- [ ] 配置验证通过
- [ ] 数据库已备份
- [ ] 部署验证通过

---

## 🧪 测试账号速查

### 学生
- 2020001 / 2020001 (张三，1号楼，计算机学院)
- 2020002 / 2020002 (李四，2号楼，软件学院)

### 宿管员
- M001 / M001 (1号楼)
- M002 / M002 (2号楼)

### 辅导员
- T001 / T001 (计算机学院)
- T002 / T002 (软件学院)

### API测试
```bash
curl http://localhost:8000/api/auth/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"user_id":"2020001","password":"2020001"}'
```

### E2E业务流程测试
```bash
# 进入测试目录
cd tests/e2e

# 运行所有测试
./run_tests.sh

# 运行指定测试
./run_tests.sh login        # 登录流程
./run_tests.sh stay         # 留校审批

# 详细文档见: tests/e2e/README.md
```

---

**详细文档参考**:
- 环境执行规范: `docs/环境执行规范速查.md`
- 数据导入: `docs/数据速查.md`
- 部署检查: `docs/部署检查清单.md`
- 系统运维: `docs/SYSTEM-OPERATIONS-GUIDE.md`
- 文档索引: `docs/INDEX.md`

**最后更新**: 2026-06-27
