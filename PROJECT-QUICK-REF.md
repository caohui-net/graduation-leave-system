# 毕业离校系统 - 项目速查手册

**最后更新**: 2026-06-11 23:17

---

## 1. 环境配置

### 后端 (Django)
```bash
路径: /home/caohui/projects/graduation-leave-system/backend
Python: 3.14.4 (需虚拟环境)
虚拟环境: backend/venv
启动: source venv/bin/activate && python manage.py runserver 0.0.0.0:7787
端口: 7787
数据库: SQLite (db.sqlite3)
```

### 前端 (HTML静态)
```bash
路径: /home/caohui/projects/graduation-leave-system/demo-web
服务器: dufs (文件服务器)
端口: 7788 (需确认)
入口: index.html (管理端)
移动端回调: mobile-sso-callback.html
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
│   │   └── approvals/         # 审批流程
│   ├── venv/                  # Python虚拟环境
│   └── manage.py
├── demo-web/                   # 前端静态页面
│   ├── index.html             # 管理端UI
│   └── mobile-sso-callback.html # 移动端SSO回调页面
├── docs/                       # 文档和截图
└── PROJECT-QUICK-REF.md       # 本文件

重要配置文件：
- backend/apps/sso_qingganlian/settings.py - SSO配置
- backend/.env (如果存在) - 环境变量
```

---

## 3. 环境变量

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

## 4. 数据库状态

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

## 5. 部署信息

### 后端服务
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

## 6. 最近修改记录（2026-06-11）

### commit bd91411 - SSO token验证开关
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

## 7. 常用命令

### 开发
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

## 8. 故障排查

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

## 9. 安全注意事项

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

## 10. OpenWolf集成

- `.wolf/anatomy.md` - 文件结构和token估算
- `.wolf/cerebrum.md` - 项目知识和最佳实践
- `.wolf/memory.md` - 操作日志
- `.omc/project-memory.json` - 项目记忆
- `.omc/session-context.json` - session上下文

---

**使用建议**: Session开始时先读取本文件，避免重复查找配置
